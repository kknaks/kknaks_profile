# -*- coding: utf-8 -*-
"""참조 자리의 원장 위치(occurrence) — decompose.slot_items 와 같은 자리·같은 (label, hint) 변환을 원장 locator 와 함께.

참조 행은 자리마다 (label, hint) 하나(같은 라벨·힌트 = 같은 참조 · REF-). 엣지는 위치마다 하나(원장 레코드 단위)라
엣지의 provenance 는 그 위치의 locator 다.
"""
from collections import OrderedDict

from .decompose import split_code, seq_category_item, MARKET_SLOT
from .provenance import P, records


def occurrences(L, lex):
    """{slot: [(label, hint, P, ctx)]} — ctx 는 엣지를 만들 때 필요한 상위 레코드 위치."""
    O = OrderedDict((k, []) for k in [
        "synergy.links[].from/to (노드 52)", "problem-packages.procedures[].name (시술 종류 29)", "problem-packages.combos[].combo[] (멤버 29)",
        "problem-packages.procedures[].products[] (제품 34)", "procedure-comparison.procedures[].name (39)", "treatment-optimization.optimal_combo[] (57)",
        "treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)", "treatment-optimization.annual_plans.schedule[].procedures[] (29)",
        "treatment-sequence.sequence_order[].categories[] (19)", "treatment-sequence.incompatible_same_day[].pair[] (14 distinct)",
        "treatment-sequence.minimum_intervals from/to (14 distinct)", "treatment-sequence.common_combos[].sequence[] (22 distinct)",
        "post-procedure-timeline.timelines[].name (10)", MARKET_SLOT])
    for r, l in records(L["synergy.json"], "links[]"):
        for side in ("from", "to"):
            code, lab = split_code(l[side])
            O["synergy.links[].from/to (노드 52)"].append((lab, code, P("synergy.json", f"links[].{side}", r), {"r": r, "side": side}))
    for r, pr in records(L["problem-packages.json"], "problems[].complaints[].procedures[]"):
        O["problem-packages.procedures[].name (시술 종류 29)"].append((pr["name"], pr["category"], P("problem-packages.json", "problems[].complaints[].procedures[].name", r), {"r": r}))
        for j, x in enumerate(pr.get("products") or []):
            O["problem-packages.procedures[].products[] (제품 34)"].append((x, None, P("problem-packages.json", "problems[].complaints[].procedures[].products[]", r + (j,)), {"r": r, "j": j}))
    for r, cb in records(L["problem-packages.json"], "problems[].complaints[].combos[]"):
        for j, x in enumerate(cb.get("combo") or []):
            O["problem-packages.combos[].combo[] (멤버 29)"].append((x, None, P("problem-packages.json", "problems[].complaints[].combos[].combo[]", r + (j,)), {"r": r, "j": j}))
    for r, pr in records(L["procedure-comparison.json"], "comparisons[].procedures[]"):
        O["procedure-comparison.procedures[].name (39)"].append((pr["name"], pr["category"], P("procedure-comparison.json", "comparisons[].procedures[].name", r), {"r": r}))
    for r, sv in records(L["treatment-optimization.json"], "by_concern[].severity_levels[]"):
        for j, x in enumerate(sv.get("optimal_combo") or []):
            O["treatment-optimization.optimal_combo[] (57)"].append((x, None, P("treatment-optimization.json", "by_concern[].severity_levels[].optimal_combo[]", r + (j,)), {"r": r, "j": j}))
    for r, g in records(L["treatment-optimization.json"], "by_age_group[]"):
        for k in ("recommended_base", "avoid", "upgrade"):
            for j, x in enumerate(g.get(k) or []):
                O["treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)"].append((x, None, P("treatment-optimization.json", f"by_age_group[].{k}[]", r + (j,)), {"r": r, "j": j, "relation_kind": k}))
    for r, s in records(L["treatment-optimization.json"], "annual_plans[].schedule[]"):
        for j, x in enumerate(s.get("procedures") or []):
            O["treatment-optimization.annual_plans.schedule[].procedures[] (29)"].append((x, None, P("treatment-optimization.json", "annual_plans[].schedule[].procedures[]", r + (j,)), {"r": r, "j": j}))
    for r, s in records(L["treatment-sequence.json"], "sequence_order[]"):
        for j, c in enumerate(s.get("categories") or []):
            lab, hint, _ = seq_category_item(c, lex)
            O["treatment-sequence.sequence_order[].categories[] (19)"].append((lab, hint, P("treatment-sequence.json", "sequence_order[].categories[]", r + (j,)), {"r": r, "j": j, "raw": c}))
    for r, p in records(L["treatment-sequence.json"], "incompatible_same_day[]"):
        for j, x in enumerate(p.get("pair") or []):
            O["treatment-sequence.incompatible_same_day[].pair[] (14 distinct)"].append((x, None, P("treatment-sequence.json", "incompatible_same_day[].pair[]", r + (j,)), {"r": r, "j": j}))
    for r, m in records(L["treatment-sequence.json"], "minimum_intervals[]"):
        for side in ("from", "to"):
            O["treatment-sequence.minimum_intervals from/to (14 distinct)"].append((m[side], None, P("treatment-sequence.json", f"minimum_intervals[].{side}", r), {"r": r, "side": side}))
    for r, c in records(L["treatment-sequence.json"], "common_combos[]"):
        for j, x in enumerate(c.get("sequence") or []):
            O["treatment-sequence.common_combos[].sequence[] (22 distinct)"].append((x, None, P("treatment-sequence.json", "common_combos[].sequence[]", r + (j,)), {"r": r, "j": j}))
    for r, t in records(L["post-procedure-timeline.json"], "timelines[]"):
        O["post-procedure-timeline.timelines[].name (10)"].append((t["name"], split_code(t["category"])[0], P("post-procedure-timeline.json", "timelines[].name", r), {"r": r}))
    for r, it in records(L["market-pricing.json"], "categories[].items[]"):
        cat = L["market-pricing.json"]["categories"][r[0]]
        O[MARKET_SLOT].append((it["name"], cat["id"], P("market-pricing.json", "categories[].items[].name", r), {"r": r}))
    return O
