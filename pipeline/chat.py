"""chat.py — CLI runner for manual testing.

Usage:
    # single message
    python3 -m pipeline.chat "Sürekli nabzımı kontrol ediyorum, kalbim hızlı atıyor."

    # interactive REPL
    python3 -m pipeline.chat --interactive
    python3 -m pipeline.chat -i

    # dry-run — no LLM call, just print the composed prompt
    python3 -m pipeline.chat --dry-run "Ölmek istiyorum"

    # mock provider — plumbing test without API key
    CBT_LLM_PROVIDER=mock python3 -m pipeline.chat "Ölmek istiyorum"

    # verbose (show retrieved cards + timing)
    python3 -m pipeline.chat -v "..."

Notes:
    - If ANTHROPIC_API_KEY is not set AND provider is not mock/local, the
      composer call will raise. Set the key or switch provider.
    - PII redaction runs inside llm_adapter before every LLM call.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

from . import config
from . import composer
from . import orchestrator
from . import llm_adapter


# Rendering
def _print_turn(turn: "orchestrator.Turn", verbose: bool = False) -> None:
    print("=" * 78)
    print(f"USER MESSAGE:\n  {turn.user_message}")
    print()
    print(f"SAFETY:")
    print(f"  route         : {turn.safety.final_route}")
    print(f"  allow_cbt     : {turn.safety.allow_cbt}")
    print(f"  highest_risk  : {turn.safety.highest_risk}")
    print(f"  matched cards : {turn.safety.safety_card_ids or '[]'}")
    if turn.safety.matches:
        for m in turn.safety.matches:
            sig_preview = ", ".join(m.matched_signals[:3])
            print(f"    - {m.card_id:40s} strength={m.match_strength:.2f}  ({sig_preview})")
    print()

    if verbose:
        print(f"RETRIEVED ({len(turn.retrieved)}):")
        for r in turn.retrieved:
            print(f"  {r.score:5.2f}  {r.card_id:32s} [{r.topic:14s}]  {r.title_tr}")
        print()
        print(f"TIMING (ms):")
        for k, v in turn.timing_ms.items():
            print(f"  {k:14s} {v:8.1f}")
        print()

    print(f"CRITIC: {'PASS' if turn.critic['passed'] else 'FAIL ' + str(turn.critic['findings'])}  "
          f"(method={turn.critic['method']})")
    print(f"BRANCH: {turn.branch}   MODEL: {turn.model}   PROVIDER: {turn.provider}")
    print("-" * 78)
    print("RESPONSE:")
    print()
    print(turn.response_text)
    print("=" * 78)


# Dry-run — just print the prompt
def _dry_run(user_message: str) -> None:
    from . import safety_classifier
    from . import retriever
    safety = safety_classifier.classify(user_message, enable_layer3=True)
    retrieved = retriever.retrieve(
        user_message,
        safety_card_ids=safety.safety_card_ids or None,
        allow_cbt=safety.allow_cbt,
    )
    prompt = composer._build_user_prompt(user_message, safety, retrieved)
    print("=" * 78)
    print(f"USER MESSAGE: {user_message}")
    print()
    print(f"SAFETY: route={safety.final_route} allow_cbt={safety.allow_cbt} "
          f"risk={safety.highest_risk} cards={safety.safety_card_ids or '[]'}")
    print(f"RETRIEVED: {[r.card_id for r in retrieved]}")
    print("=" * 78)
    print("SYSTEM PROMPT:")
    print("-" * 78)
    print(composer.SYSTEM_PROMPT_TR)
    print("=" * 78)
    print("USER PROMPT (what composer sends to LLM):")
    print("-" * 78)
    print(prompt)
    print("=" * 78)
    print("(dry-run — no LLM call was made)")



# Interactive REPL
def _interactive_loop(verbose: bool) -> None:
    print()
    print("CBT chat — interactive.  Ctrl-D or blank line to exit.")
    print(f"Provider: {config.LLM_PROVIDER}   Composer model: {config.LLM_MODEL_COMPOSER}")
    print("-" * 78)
    turn_no = 0
    while True:
        try:
            user_message = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_message:
            break
        turn_no += 1
        try:
            t0 = time.time()
            turn = orchestrator.respond(user_message)
            dur = (time.time() - t0) * 1000
            _print_turn(turn, verbose=verbose)
            print(f"(wall {dur:.0f} ms)")
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")
            if verbose:
                import traceback
                traceback.print_exc()



# Main
def main() -> int:
    parser = argparse.ArgumentParser(description="CBT chat manual test runner.")
    parser.add_argument("message", nargs="?", help="User message (Turkish).")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive REPL.")
    parser.add_argument("--dry-run", action="store_true", help="Print prompt only, no LLM call.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show retrieved cards + timing.")
    parser.add_argument("--mock", action="store_true", help="Force provider=mock.")
    args = parser.parse_args()

    if args.mock:
        os.environ["CBT_LLM_PROVIDER"] = "mock"

    # Register mock handlers if provider is mock
    if os.environ.get("CBT_LLM_PROVIDER") == "mock":
        composer.register_composer_mocks()
        # Force config reload for provider
        import importlib
        importlib.reload(config)

    if args.interactive:
        _interactive_loop(verbose=args.verbose)
        return 0

    if not args.message:
        parser.print_help()
        return 1

    if args.dry_run:
        _dry_run(args.message)
        return 0

    try:
        turn = orchestrator.respond(args.message)
        _print_turn(turn, verbose=args.verbose)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        print("Hint: export ANTHROPIC_API_KEY=... or run with --mock for offline test.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
