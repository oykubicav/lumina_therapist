"""llm_adapter sağlayıcı sınırı testleri.

Anthropic SDK v1.0 (Ağustos 2026) temperature/top_p/top_k parametrelerini
Messages imzasından kaldırdı. Göndermek çağrı anında TypeError veriyor ve
bütün /chat isteklerini fallback'e düşürüyor. Bu dosya o parametrenin
Anthropic'e gitmediğini kilitliyor.
"""

import sys
import types

import pytest


class _KaydedenMessages:
    """v1.0 davranışını taklit eder: sampling parametrelerini reddeder."""

    YASAK = ("temperature", "top_p", "top_k")

    def __init__(self):
        self.son_cagri = None

    def create(self, **kw):
        for ad in self.YASAK:
            if ad in kw:
                raise TypeError(
                    f"Messages.create() got an unexpected keyword argument '{ad}'"
                )
        self.son_cagri = kw
        blok = types.SimpleNamespace(text="tamam")
        return types.SimpleNamespace(content=[blok], model_dump=lambda: {})


@pytest.fixture()
def sahte_anthropic(monkeypatch):
    messages = _KaydedenMessages()

    class SahteClient:
        def __init__(self, api_key=None):
            self.messages = messages

    modul = types.ModuleType("anthropic")
    modul.Anthropic = SahteClient
    monkeypatch.setitem(sys.modules, "anthropic", modul)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sahte-anahtar")
    return messages


def test_temperature_anthropice_gonderilmiyor(sahte_anthropic, monkeypatch):
    from pipeline import llm_adapter

    resp = llm_adapter.llm_complete(
        system="s", user="u", provider="anthropic", max_tokens=64, temperature=0.0
    )

    assert resp.text == "tamam"
    assert "temperature" not in sahte_anthropic.son_cagri
    assert set(sahte_anthropic.son_cagri) == {"model", "max_tokens", "system", "messages"}


def test_sampling_parametreleri_hicbiri_gonderilmiyor(sahte_anthropic):
    from pipeline import llm_adapter

    llm_adapter.llm_complete(
        system="s", user="u", provider="anthropic", max_tokens=64, temperature=0.7
    )

    for ad in _KaydedenMessages.YASAK:
        assert ad not in sahte_anthropic.son_cagri


def test_cagiranlar_hala_temperature_verebiliyor(sahte_anthropic):
    """Boru hattındaki 12 çağrı yeri temperature geçiyor — imza korunmalı."""
    from pipeline import llm_adapter

    for t in (0.0, 0.3, 1.0):
        r = llm_adapter.llm_complete(
            system="s", user="u", provider="anthropic", max_tokens=32, temperature=t
        )
        assert r.text == "tamam"
