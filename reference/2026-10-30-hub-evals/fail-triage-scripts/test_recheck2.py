"""recheck2 · reach 시험(WORK-007 WP-0) — 두 번 바이트 같음(시간 칸 분리) · 676 = meta.replay_unique · 판정 동일성 320/320 · 크기 셈 = fail-triage2 case3_sizes.

  cd fail-triage-scripts && python3 -m pytest test_recheck2.py -q   (baseline 리포트가 build-out/recheck2/ 에 있어야 함)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import recheck2 as R  # noqa: E402

OUT = R.OUT
BASE = OUT / "recheck2-report.baseline.json"
needs = pytest.mark.skipif(not BASE.exists() or not (R.E / "build-out" / "recheck" / "replay2.json").exists(), reason="baseline 리포트 · replay2 없음")


def _strip(d: dict) -> dict:
    d = json.loads(json.dumps(d))
    d["meta"].pop("ran_at", None)
    return d


@needs
def test_baseline_twice_same_bytes(tmp_path):
    p1, p2 = tmp_path / "a", tmp_path / "b"
    for p in (p1, p2):
        subprocess.run([sys.executable, str(HERE / "recheck2.py"), "baseline", "--out-prefix", str(p)], check=True, capture_output=True)
    a, b = _strip(json.loads((str(p1) + ".json" and Path(str(p1) + ".json")).read_text())), _strip(json.loads(Path(str(p2) + ".json").read_text()))
    assert json.dumps(a, ensure_ascii=False, sort_keys=True) == json.dumps(b, ensure_ascii=False, sort_keys=True)


@needs
def test_replay_unique_and_identity_and_sizes():
    rep = json.loads(BASE.read_text(encoding="utf-8"))
    ft = json.loads((R.E / "build-out" / "fail-triage2.json").read_text(encoding="utf-8"))
    assert rep["meta"]["replay"]["unique_calls"] == 676 == ft["meta"]["replay_unique"]
    assert rep["identity"]["same"] == rep["identity"]["rows"] == 320 and rep["identity"]["diff"] == []
    assert rep["sizes_recorded_case3"]["median"] == ft["case3_sizes"]["median"] == 46539
    assert rep["sizes_recorded_case3"]["p95"] == ft["case3_sizes"]["p95"] == 170989
    assert rep["rate"]["b186"]["n"] == 186 and rep["rate"]["reach161"]["n"] == 155 and rep["rate"]["not_closable25"]["n"] == 31  # 161 − 데이터 불가 6(코디 11-01 4)) · 25 + 6
    assert rep["rate"]["spec161"]["n"] == 161


@needs
def test_clauses_fixture_matches_spec_counts():
    rows = json.loads((OUT / "b186-clauses.json").read_text(encoding="utf-8"))["rows"]
    import collections
    c = collections.Counter(r["clause"] for r in rows)
    assert len(rows) == 186
    spec = collections.Counter(r["spec_clause"] for r in rows)  # SPEC §8 표 그대로
    assert spec["C7′"] == 40 and spec["C2′"] == 32 and spec["§5-14′"] == 29 and spec["F-F"] == 18 and spec["C3′"] == 14 and spec["C14′"] == 11 and spec["C9′"] == 8
    assert spec["C6′"] == 4 and spec["C1′"] == 3 and spec["C4′"] == 1 and spec["F-D′"] == 1 and spec["X0"] == 16 and sum(v for k, v in spec.items() if k.startswith("N-")) == 9
    assert c["N-데이터"] == 6 and sum(1 for r in rows if r["not_closable"]) == 31  # 코디 11-01 4) 데이터 불가 6 → 닫지 않는 행


@needs
def test_judge_same_as_recheck():
    """판정 식 동일성 — norm · gold_match · in_hub 가 recheck.py 와 같은 결과(같은 export · 같은 인용)."""
    sys.path.insert(0, str(HERE))
    import recheck as R1  # noqa: PLC0415
    assert R.norm(" A-b c_d ") == R1.norm(" A-b c_d ") == "abcd"
    g1, g2 = R1.Gold(OUT / "gold-export.d3a1abd52f70afe9.json"), R.Gold(OUT / "gold-export.d3a1abd52f70afe9.json")
    for q in ("켈로이드체질", "교근전연상방주사하악변연신경협근신경마비위험", "612개월"):
        t1, h1 = g1.gold_match(q)
        t2, h2 = g2.gold_match(q)
        assert t1 == t2 and [r.get("fact_id") for _, _, r in h1] == [r.get("fact_id") for _, _, r in h2]


@needs
def test_reach_baseline_exists_and_deterministic(tmp_path):
    rep = json.loads((OUT / "reach-report.baseline.json").read_text(encoding="utf-8"))
    assert rep["rate"]["reach161"]["n"] == 161 and rep["rate"]["b186"]["n"] == 186
    p1, p2 = tmp_path / "r1", tmp_path / "r2"
    for p in (p1, p2):
        subprocess.run([sys.executable, str(HERE / "reach.py"), "--baseline", "--out-prefix", str(p)], check=True, capture_output=True, env={**__import__("os").environ, "DATABASE_URL": "sqlite+aiosqlite:///:memory:"})
    a, b = _strip(json.loads(Path(str(p1) + ".json").read_text())), _strip(json.loads(Path(str(p2) + ".json").read_text()))
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
