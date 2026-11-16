"""recheck.py 시험(읽기만) — 판정 동일성 320/320 · 두 번 같음(시간 칸 뺌) · 크기 셈이 §6-5 표와 같음.

  cd fail-triage-scripts && python3 -m pytest test_recheck.py -q
입력: fail-triage.json · runs.jsonl · build-out/recheck/replay.json · gold-export.e9d30ace08c65bb8.json(없으면 건너뜀).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import recheck as R  # noqa: E402

needs = pytest.mark.skipif(not (R.OUT / "replay.json").is_file() or not (R.OUT / "gold-export.e9d30ace08c65bb8.json").is_file(),
                           reason="replay.json · 옛 export 없음")
pytestmark = needs


@pytest.fixture(scope="module")
def ctx():
    runs = R.load_runs(R.E / "runs" / "runs.jsonl")
    ft = json.loads((R.E / "build-out" / "fail-triage.json").read_text(encoding="utf-8"))
    replay = json.loads((R.OUT / "replay.json").read_text(encoding="utf-8"))
    gold = R.Gold(R.OUT / "gold-export.e9d30ace08c65bb8.json")
    raw = R.Raw(R.RAW)
    qrid = {d["question_no"]: rid for rid, d in runs.items()}
    rec = {}
    for rid in runs:
        rec[(rid, "case2")] = [dict(replay["calls"][c["key"]]) for c in replay["case2"].get(rid, [])]
        h = replay["case3"].get(rid)
        rec[(rid, "case3")] = [dict(replay["calls"][h["key"]])] if h and h.get("key") else []
    for r in ft["rows"]:
        r["run_id"] = qrid[r["question_no"]]
    return runs, ft["rows"], rec, gold, raw


def test_identity_320(ctx):
    runs, rows, rec, gold, raw = ctx
    out = R.run_rows(gold, raw, rows, runs, {}, rec)
    diff = [(x["question_no"], x["case"], x["cls"], x["new"]["cls"], x["sub"], x["new"]["sub"]) for x in out
            if not (x["new"]["cls"] == x["cls"] and x["new"]["sub"] == x["sub"])]
    assert len(out) == 320 and diff == []


def test_current_size_rule(ctx):
    runs = ctx[0]
    s = R.current_sizes(runs)
    assert s["case2_no_error_total"] == 662 and s["case3_total"] == 201
    for t, v in R.CURRENT_MEDIAN.items():
        assert s["case2_no_error"][t]["median"] == v, t
    assert s["case2_no_error"]["recommend"]["n"] == 58 and s["case2_no_error"]["procedure_card"]["n"] == 154
    for t_, v in R.CURRENT_MEDIAN_NO_SECTIONS.items():
        assert s["case2_no_sections"][t_]["median"] == v, t_
    assert s["case2_no_sections"]["procedure_card"]["n"] == 16 and s["case2_no_sections"]["check_conditions"]["n"] == 10


def test_baseline_twice_same_bytes(tmp_path):
    outs = []
    for i in range(2):
        prefix = tmp_path / f"r{i}"
        subprocess.run([sys.executable, str(HERE / "recheck.py"), "baseline", "--out-prefix", str(prefix)], check=True, capture_output=True)
        d = json.loads((tmp_path / f"r{i}.json").read_text(encoding="utf-8"))
        d["meta"].pop("ran_at")
        outs.append(json.dumps(d, sort_keys=True, ensure_ascii=False))
    assert outs[0] == outs[1]
