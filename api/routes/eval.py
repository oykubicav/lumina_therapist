"""POST /eval/run — async eval trigger. GET /eval/results/{run_id} — status.

Admin gated. Runs structural or response eval in a BackgroundTask so the
HTTP request returns immediately with a run_id. Poll GET /eval/results/{run_id}
for status + summary when done.

MVP uses an in-process task registry (dict) — fine for single-worker dev.
Prod: replace with proper queue (Celery, Dramatiq, or ARQ + Redis).
"""

from __future__ import annotations

import logging
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path
from typing import Dict

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from api.schemas import EvalRunRequest, EvalRunResponse, EvalStatusResponse
from api.deps import require_admin
from pipeline import config as pcfg


router = APIRouter(prefix="/eval", tags=["eval"])
log = logging.getLogger(__name__)


# In-process registry: run_id -> status dict
_REGISTRY: Dict[str, dict] = {}
_LOCK = threading.RLock()


def _register(run_id: str, entry: dict) -> None:
    with _LOCK:
        _REGISTRY[run_id] = entry


def _update(run_id: str, **fields) -> None:
    with _LOCK:
        if run_id in _REGISTRY:
            _REGISTRY[run_id].update(fields)


def _run_eval_subprocess(run_id: str, req: EvalRunRequest) -> None:
    """Kick off `python -m pipeline.<runner>` as a subprocess so any crash
    in the eval doesn't take down the API worker. Capture summary on stdout
    OR read from evals/results/<label>_*_summary.json.
    """
    module = (
        "pipeline.eval_runner" if req.which == "structural"
        else "pipeline.response_eval"
    )
    label = f"{req.label}_{req.which}"
    cmd = [sys.executable, "-m", module, "--label", label, "--top-k", str(req.top_k)]
    if req.filter:
        cmd += ["--filter", req.filter]
    if req.no_llm_critic and req.which == "response":
        cmd += ["--no-llm-critic"]

    _update(run_id, status="running", started_at=time.time())
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(pcfg.ROOT),
            capture_output=True, text=True, timeout=1800,
        )
        if proc.returncode != 0:
            _update(
                run_id,
                status="error",
                finished_at=time.time(),
                error=f"exit {proc.returncode}: {proc.stderr[:500]}",
            )
            return
        # Find latest summary written by that runner with our label
        results_dir = pcfg.EVAL_RESULTS_DIR
        summaries = sorted(results_dir.glob(f"{label}_*_summary.json"))
        if summaries:
            import json
            with open(summaries[-1], encoding="utf-8") as f:
                summary = json.load(f)
        else:
            summary = None
        _update(run_id, status="done", finished_at=time.time(), summary=summary)
    except subprocess.TimeoutExpired:
        _update(run_id, status="error", finished_at=time.time(), error="timeout")
    except Exception as e:
        _update(run_id, status="error", finished_at=time.time(), error=str(e))


@router.post(
    "/run",
    response_model=EvalRunResponse,
    dependencies=[Depends(require_admin)],
)
async def run_eval(req: EvalRunRequest, background: BackgroundTasks):
    run_id = str(uuid.uuid4())
    _register(run_id, {
        "run_id": run_id,
        "status": "queued",
        "which": req.which,
        "requested_at": time.time(),
    })
    background.add_task(_run_eval_subprocess, run_id, req)
    return EvalRunResponse(run_id=run_id, status="queued")


@router.get(
    "/results/{run_id}",
    response_model=EvalStatusResponse,
    dependencies=[Depends(require_admin)],
)
async def get_eval_status(run_id: str):
    with _LOCK:
        entry = _REGISTRY.get(run_id)
    if not entry:
        raise HTTPException(status_code=404, detail=f"run not found: {run_id}")
    return EvalStatusResponse(
        run_id=run_id,
        status=entry.get("status", "queued"),
        started_at=entry.get("started_at"),
        finished_at=entry.get("finished_at"),
        summary=entry.get("summary"),
        error=entry.get("error"),
    )
