"""step9_gold 시험(WORK-010 WP-0) — 두 번 바이트 같음 · 기준선 셈(옛 export · 9단계 fact 0 · 닫힘 0) · 판정 식 고정 입력.

  cd fail-triage-scripts && python3 -m pytest test_step9_gold.py -q
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import step9_gold as G  # noqa: E402

needs = pytest.mark.skipif(not G.OLD_EXPORT.exists(), reason="옛 export 사본 없음")


def test_norm_and_section_map_fact_id():
    assert G.norm("약 1개월 완전 발현, 3-6개월 유지") == "약1개월완전발현36개월유지"
    assert G.se_cx_fact_id({"path": "complications.categories[0].complications[0].management", "silver_id": "SE-M1-01", "field": "management"}) == "SE-M1-01#management"
    assert G.se_cx_fact_id({"path": "complications.categories[0].complications[3].risk_factors[2]", "silver_id": "SE-M1-04", "field": "risk_factors"}) == "SE-M1-04#risk_factors[2]"
    assert G.MGMT.search("CX-M1-05#prevention") and G.MGMT.search("SE-M7-06#management") and not G.MGMT.search("CX-M1-05#mechanism")


def test_judge_fixed_input():
    s9 = {"version": "t", "summary": {"facts_out": 2}, "value_dictionary": [],
          "records": [{"id": "S9:a", "text": "효과 3개월", "source": {"path": "a"}}, {"id": "S9:b", "text": "효과 6개월", "source": {"path": "b"}}],
          "node_slots": [{"node": "unit_procedure:U", "section": "recovery", "class": "②", "resolved": "S9:a", "emit": ["S9:a"], "alternatives": ["S9:b"],
                          "fact_ids": ["unit_procedure:U#recovery#step9[a]"]},
                         {"node": "product:X", "section": "overview", "class": "한 원천", "emit": ["S9:b"], "fact_ids": ["product:X#overview#step9[b]"]}],
          "section_map": [{"path": "complications.categories[0].complications[0].management", "silver_id": "CX-1", "field": "management", "section": "safety.management"}]}
    new = {"build": {"build_hash": "n"}, "nodes": [{"id": "unit_procedure:U"}], "globals": [],
           "facts": [{"id": "unit_procedure:U#recovery#step9[a]", "text": "효과 3개월", "section": "recovery", "source": {"meta": {"alternatives": [{"record": "S9:b"}]}}},
                     {"id": "CX-1#management", "text": "냉찜질", "section": "safety.management", "source": {}}]}
    old = {"build": {"build_hash": "o"}, "nodes": [], "globals": [], "facts": [{"id": "CX-1#management", "text": "냉찜질", "section": "safety.complications", "source": {}}]}
    rs = {"A2_rows": [{"no": "Q1", "case": "case2", "item": "accuracy", "path": "x", "quote": "효과 3개월"},
                      {"no": "Q2", "case": "case2", "item": "accuracy", "path": "y", "quote": "효과 6개월"},
                      {"no": "Q3", "case": "case2", "item": "accuracy", "path": "complications.categories[0].complications[0].management", "quote": "냉찜질"},
                      {"no": "Q4", "case": "case2", "item": "accuracy", "path": "z", "quote": "없는 말"}], "A5_rows": []}
    rep = G.facts_report(new, old, s9, rs)
    v = [r["verdict"] for r in rep["e_a_rows"]["A2"]["detail"]]
    assert v == ["실버 9단계로 닫힘", "alternatives 에만(골드 안 나감)", "골드 section 으로(실버 변경 없음)", "안 닫힘"]
    assert rep["e_a_rows"]["A2"]["closed"] == 2
    assert rep["b_step9_facts"]["want"] == 1 and rep["b_step9_facts"]["skipped"] == 1 and rep["b_step9_facts"]["sum_ok"]
    assert rep["d_alternatives"] == {**rep["d_alternatives"], "alternatives_meta": 1, "alternatives_text_facts": 0, "resolved_in_emit_alt_out": 1}
    assert rep["c_sections"]["moved_by"] == {"safety.complications→safety.management": 1}
    # 옛 export(section 이동 없음)로는 section 판정이 닫히지 않음
    assert G.facts_report(old | {"nodes": [{"id": "unit_procedure:U"}]}, old, s9, rs)["e_a_rows"]["A2"]["closed"] == 0


@needs
def test_baseline_counts_and_twice_same_bytes(tmp_path):
    outs = []
    for lab in ("t1", "t2"):
        subprocess.run([sys.executable, str(HERE / "step9_gold.py"), "facts", "--export", str(G.OLD_EXPORT), "--label", lab, "--out-dir", str(tmp_path)],
                       check=True, capture_output=True)
        outs.append((tmp_path / f"step9-gold-report.{lab}.json").read_bytes())
    assert outs[0] == outs[1]
    rep = json.loads(outs[0])
    assert rep["b_step9_facts"]["got"] == 0 and rep["b_step9_facts"]["want"] == 5273 and rep["b_step9_facts"]["skipped"] == 39
    assert rep["e_a_rows"]["A2"]["rows"] == 54 and rep["e_a_rows"]["A5"]["rows"] == 30
    assert rep["e_a_rows"]["A2"]["closed"] == 0 and rep["e_a_rows"]["A5"]["closed"] == 0
