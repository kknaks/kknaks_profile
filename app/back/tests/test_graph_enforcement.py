"""KDEV-WORK-007 — enforcement 메커니즘 증명.

report-only 검증기를 enforcement 로 켠 뒤의 4대 메커니즘:
  1. 주입 ERROR → load_persona raise (fail-fast)
  2. 주입 ERROR + GRAPH_ENFORCE=0 → 로드 성공 (kill-switch)
  3. L5 orphan(WARN)만 → 로드 성공 (WARN 은 안 막음)
  4. runtime reload 가 enforce 실패해도 구 데이터 유지·서빙 지속 (워커 크래시 X)

테스트는 conftest 가 GRAPH_ENFORCE=0 전역 기본 → enforce on 케이스는 monkeypatch opt-in.
"""

from pathlib import Path

import pytest

from service.persona_loader import (
    GraphEnforcementError,
    PersonaError,
    _enforce_graph,
)

PERSONA = Path(__file__).resolve().parents[3] / "persona"

_ERROR_V = {"rule": "L1", "level": "ERROR", "node": "x", "detail": "dead link [[ghost]]"}
_WARN_V = {"rule": "L5", "level": "WARN", "node": "y", "detail": "orphan (엣지 0개)"}


class TestEnforceGraphUnit:
    """_enforce_graph 단위 — env kill-switch + ERROR-only + _graph_error."""

    def test_error_raises_when_enforce_on(self, monkeypatch):
        monkeypatch.setenv("GRAPH_ENFORCE", "1")
        with pytest.raises(GraphEnforcementError):
            _enforce_graph({"_graph_violations": [_ERROR_V], "_graph_error": None})

    def test_killswitch_skips(self, monkeypatch):
        monkeypatch.setenv("GRAPH_ENFORCE", "0")
        # ERROR 가 있어도 kill-switch 면 raise 안 함
        _enforce_graph({"_graph_violations": [_ERROR_V], "_graph_error": None})

    def test_warn_only_does_not_raise(self, monkeypatch):
        monkeypatch.setenv("GRAPH_ENFORCE", "1")
        # L5 orphan(WARN) 156개여도 boot 막지 않음
        _enforce_graph({"_graph_violations": [_WARN_V] * 156, "_graph_error": None})

    def test_graph_error_raises(self, monkeypatch):
        monkeypatch.setenv("GRAPH_ENFORCE", "1")
        with pytest.raises(GraphEnforcementError):
            _enforce_graph({"_graph_violations": [], "_graph_error": "ValueError: boom"})

    def test_clean_does_not_raise(self, monkeypatch):
        monkeypatch.setenv("GRAPH_ENFORCE", "1")
        _enforce_graph({"_graph_violations": [_WARN_V], "_graph_error": None})

    def test_is_persona_error_subclass(self):
        # 기존 pre-commit `except PersonaError` 가 공짜로 catch
        assert issubclass(GraphEnforcementError, PersonaError)


class TestLoadPersonaEnforcement:
    """load_persona 통합 — report 산출 뒤 enforce 가 raise 하는지(배선 증명)."""

    def test_injected_error_makes_load_persona_raise(self, monkeypatch):
        # validate_graph 가 ERROR 를 내도록 주입 → load_persona 가 raise (enforce on)
        monkeypatch.setenv("GRAPH_ENFORCE", "1")
        monkeypatch.setattr(
            "service.persona_loader.validate_graph",
            lambda nodes, dups=None: [_ERROR_V],
        )
        from service.persona_loader import load_persona

        with pytest.raises(GraphEnforcementError):
            load_persona(PERSONA)

    def test_injected_error_killswitch_loads(self, monkeypatch):
        # 같은 주입 ERROR 라도 GRAPH_ENFORCE=0 이면 로드 성공
        monkeypatch.setenv("GRAPH_ENFORCE", "0")
        monkeypatch.setattr(
            "service.persona_loader.validate_graph",
            lambda nodes, dups=None: [_ERROR_V],
        )
        from service.persona_loader import load_persona

        data = load_persona(PERSONA)
        assert data["profile"] is not None  # 정상 로드

    def test_injected_warn_only_loads(self, monkeypatch):
        # L5 WARN 만 주입 → enforce on 이어도 로드 성공
        monkeypatch.setenv("GRAPH_ENFORCE", "1")
        monkeypatch.setattr(
            "service.persona_loader.validate_graph",
            lambda nodes, dups=None: [_WARN_V],
        )
        from service.persona_loader import load_persona

        data = load_persona(PERSONA)
        assert data["profile"] is not None

    def test_real_data_enforce_on_boots(self, monkeypatch):
        # 실 데이터(ERROR=0, T-014 아카이브 면제 반영) + enforce on → raise 없음
        monkeypatch.setenv("GRAPH_ENFORCE", "1")
        from service.persona_loader import load_persona

        data = load_persona(PERSONA)
        assert data.get("_graph_error") is None
        errors = [v for v in data["_graph_violations"] if v["level"] == "ERROR"]
        assert errors == []


class TestRuntimeReloadSurvival:
    """runtime reload 가 enforce 실패해도 구 데이터 유지 (워커/webhook 크래시 금지)."""

    def test_reload_data_keeps_previous_on_enforce_failure(self, monkeypatch):
        import main

        sentinel = {"profile": "SENTINEL", "career": [], "projects": [], "notes": {},
                    "contents": [], "daily": [], "algorithms": []}
        main._data = sentinel

        def _raise(_dir):
            raise GraphEnforcementError("injected enforce failure")

        monkeypatch.setattr(main, "load_persona", _raise)

        ok = main.reload_data()
        assert ok is False              # reload 거부
        assert main._data is sentinel   # 구 데이터 그대로 — 서빙 지속, 크래시 없음

    def test_reload_data_returns_true_on_success(self, monkeypatch):
        import main

        called = {"n": 0}

        def _ok():
            called["n"] += 1

        monkeypatch.setattr(main, "load_all", _ok)
        assert main.reload_data() is True
        assert called["n"] == 1
