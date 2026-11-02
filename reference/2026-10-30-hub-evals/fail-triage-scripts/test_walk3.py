"""walk3 시험(WORK-008 WP-0) — 두 번 바이트 같음(시간 칸 분리) · 기준선 476 재계산 = 기록 바이트(차 ≤ 1) · 재생 규칙 고정 입력 · 68 = 식으로 뽑은 행 수.

  cd fail-triage-scripts && python3 -m pytest test_walk3.py -q   (기준선 리포트가 build-out/walk3/ 에 · 두 번 시험은 backend venv · DB 발행본이 있어야 함)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import walk3 as W  # noqa: E402

BASE = W.OUT / "walk3-report.baseline.json"
PY = W.R.BACKEND / ".venv" / "bin" / "python"
ENV_FILE = W.R.BACKEND / "envs" / ".env.gold"


def _rec(steps: list[tuple[str, list[str]]], stop: str) -> dict:
    return {"intent": "I-02", "stop": stop, "steps": [{"node": n, "jev": {"picked": p}} for n, p in steps]}


def _fake(sizes: dict[tuple[str, str | None], int]):
    """노드 · section 마다 정해 둔 크기의 새 꼴 응답(facts 줄 1 · 한 줄은 cut) — 이웃 호출은 이웃 수만큼 작게."""
    calls: list[tuple[str, tuple, tuple, tuple]] = []

    def ex(node, sections=None, neighbors=None, fact_ids=None, intent=None, full=False):
        calls.append((node, tuple(sections or ()), tuple(neighbors or ()), tuple(fact_ids or ())))
        s = (sections or [None])[0]
        n = sizes.get((node, s), 100)
        facts = [] if fact_ids else [{"id": f"{node}#{s}#1", "line": "x"}, {"id": f"{node}#{s}#2", "line": "y…", "cut": True}] if s else []
        body = {"pad": "a" * max(0, n - 60), "facts": facts, "claude_contract": {"allowed": "facts_uncut"}}
        return body
    return ex, calls


def test_replay_rules_fixed_record():
    # 걸음 2 기록(budget 으로 멈춤) → 기록 2 걸음 재생 · 이웃 큐(넣은 순서) 로 이어 감 · 그 판 Jev section ∩ peek section(peek 순) · 이웃 안 고름
    rec = _rec([("a", ["section:overview", "n1", "n2"]), ("n1", ["section:checks", "section:overview", "n3"])], "budget")
    ex, calls = _fake({})
    peek = {"n2": ["checks", "method", "overview"], "n3": ["overview"]}
    r = W.replay(rec, ex, lambda n: peek[n], line_form=True)
    assert r["visited"] == ["a", "n1", "n2", "n3"] and r["steps"] == 4 and r["stop"] == "steps" and r["continued"] == 2
    walk_calls = [c for c in calls if not c[3]]
    assert walk_calls[0] == ("a", ("overview",), ("n1", "n2"), ())  # 이웃은 첫 호출에 같이
    assert walk_calls[1:3] == [("n1", ("checks",), ("n3",), ()), ("n1", ("overview",), (), ())]  # section 하나씩
    assert walk_calls[3:6] == [("n2", ("checks",), (), ()), ("n2", ("overview",), (), ()), ("n3", ("overview",), (), ())]  # peek 순 · 이웃 안 고름
    assert r["cut_n"] == 6 and len(r["full"]) == 6 and len(r["listed"]) == 12
    # 예산: 처음 넘는 호출은 통째로 빼고 그 걸음에서 멈춤
    ex2, _ = _fake({("a", "overview"): 15000, ("n1", "checks"): 6000})
    r2 = W.replay(rec, ex2, lambda n: peek[n], line_form=True)
    assert r2["stop"] == "budget" and r2["steps"] == 2 and r2["visited"] == ["a", "n1"] and r2["bytes"] < W.BUDGET
    # 기록 stop 이 enough 면 같은 자리에서 멈춤 · 옛 꼴은 이어 가지 않음
    r3 = W.replay(_rec([("a", ["section:overview"])], "enough"), ex, lambda n: [], line_form=True)
    assert r3["steps"] == 1 and r3["stop"] == "enough"
    r4 = W.replay(rec, ex, lambda n: peek[n], line_form=False)
    assert r4["steps"] == 2 and r4["stop"] == "budget"


def test_no_data_rows_formula():
    d = json.loads((W.E / "build-out" / "rerun-v4-vs-v3.json").read_text(encoding="utf-8"))
    rows = W.no_data_rows(d)
    assert sum(1 for _, r in rows if r["case"] == "case3") == 68
    assert sum(1 for _, r in rows if r["case"] == "case2") == 51


@pytest.mark.skipif(not BASE.exists(), reason="기준선 리포트 없음")
def test_baseline_recompute_matches_record():
    rep = json.loads(BASE.read_text(encoding="utf-8"))
    aw = rep["a_walk_calls"]
    assert rep["meta"]["form"] == "v3.2 sections"
    assert aw["recorded_app_bytes"]["n"] == 476 and aw["mismatch_n"] <= 1 and aw["same_as_recorded"] >= 475
    assert rep["e_walk"]["replay"]["steps_mean"] == rep["e_walk"]["recorded"]["steps_mean"] == 1.84
    assert rep["f_reach_case3"]["rows"] == 68


@pytest.mark.skipif(not PY.exists() or not ENV_FILE.exists(), reason="backend venv · env 없음")
def test_twice_same_bytes(tmp_path):
    env = dict(os.environ)
    for ln in ENV_FILE.read_text(encoding="utf-8").splitlines():
        if "=" in ln and not ln.lstrip().startswith("#"):
            k, v = ln.split("=", 1)
            env.setdefault(k.strip(), v.strip())
    outs = []
    for lab in ("t1", "t2"):
        subprocess.run([str(PY), str(HERE / "walk3.py"), "--inprocess", "--label", lab, "--out-dir", str(tmp_path)], check=True, capture_output=True, env=env, cwd=str(W.R.BACKEND))
        outs.append((tmp_path / f"walk3-report.{lab}.json").read_bytes() + (tmp_path / f"sizes.{lab}.json").read_bytes())
    assert outs[0] == outs[1]
