# -*- coding: utf-8 -*-
"""report.md §14 「6차 빌드 · ERD v3.1 + 엑소좀 approved」 — 5차(baseline/manifest-5차.json · ERD v3 · 묶음 3) 대비.

변화표(개체 · 관계 · 게이트 · 충돌) · 결정 적용(엑소좀 EXO-02·05·06 · 옛 네 칸/옛 표현 지정의 v3.1 변환) · 문구 사전 항목·status ·
단위(사건별 조합) · R15(레코드 · (출발, 단위) distinct · 경과) · 조건 단위 · 묶음 4 제안 요약.
"""
import json
import os
from collections import Counter, OrderedDict

from .util import md_table

EXO = "DEC-2026-11-05-B3-EXO"


def _kv(d):
    return " · ".join(f"{k} {v}" for k, v in d.items()) if d else "—"


def sixth(S, out_dir, baseline_dir, m, g4=None):
    p5 = os.path.join(baseline_dir, "manifest-5차.json")
    if not os.path.exists(p5):
        return
    b = json.load(open(p5, encoding="utf-8"))["counts"]
    c = m["counts"]
    ctx = S.ctx
    log = m["decisions"]["apply_log"]
    AU, CU = ctx["AU"], ctx["CU"]
    A0, C0 = ctx["adv0"]["summary"], ctx["cond0"]["summary"]
    o = ["", "## 14. 6차 빌드 · ERD v3.1 + 엑소좀 approved", "",
         "5차 = `baseline/manifest-5차.json`(ERD v3 · 결정 묶음 3 approved 24 까지) · 6차 = ERD **v3.1**(`erd-v3.1.json` · `erd-v3.1-dictionaries.json` · 빌더 V3.1-1~10 · 발주서 `silver-build-6-brief.md`) "
         f"+ 엑소좀 EXO-02·05·06 을 v3.1 kind 로 올린 결정 {sum(1 for x in log if x['id'].startswith(EXO))} 건(`decisions/batch3/DEC-2026-11-05-B3-EXO-*` · 사용자 확정 방향). "
         f"③ 결정 적용 전 분해 = `erd-v3.1-tuples.json` 요약 차이 {m['erd_comparison']['diff']}/{m['erd_comparison']['keys']}(§5 · 시술 · 부작용 · 조건 + 행 대조).", ""]

    # ---------------------------------------------------------------- 결정 적용
    res = Counter((x["kind"], x["result"]) for x in log)
    o += ["### 결정 적용(6차)", "", md_table(["kind", "applied", "recorded", "rejected", "no_target"], [(k, *(res.get((k, r), 0) for r in ("applied", "recorded", "rejected", "no_target"))) for k in sorted({x["kind"] for x in log})]), ""]
    bad = [x for x in log if x["result"] in ("rejected", "no_target")]
    o.append("거부·대상 없음: " + ("없음 — 기존 결정(_bootstrap · batch1 · 2a · 2b · 3) 전부 v3.1 빌더가 받았다." if not bad else ""))
    for x in bad:
        o.append(f"- `{x['id']}` {x['kind']} — {x['result']}: {x.get('why')}")
    conv4 = [x for x in log if x["kind"] == "adverse_tuple_assign" and "옛 네 칸" in str(x.get("note")) and "표현은 개체가 아니다" not in str(x.get("note"))]
    convx = [x for x in log if x["kind"] == "adverse_tuple_assign" and "표현은 개체가 아니다" in str(x.get("note"))]
    conv_e = [x for x in log if x["kind"] == "edge_create" and "옛 네 칸" in str(x.get("note"))]
    o += ["", "v3.1 로 옮겨 적용한 옛 결정(거부 아님 · 적용 로그 note):", "",
          f"- 옛 네 칸 adverse_tuple_assign(raw_name) {len(conv4)} — course_id 를 단위에서 빼 그 이름 → 단위 R15 엣지의 course 로(미상은 null) · 상대 부위 site_id 는 none(relative_site_text): " + ", ".join(f"`{x['id'].split('-', 4)[-1]}`" for x in conv4),
          f"- 옛 adverse_tuple_assign(kind=expression) {len(convx)} — 표현은 개체가 아니므로(V3.1-10) 그 자리의 문구 사전 항목 지도로 적용(phrase_map 과 같은 효과 · status=approved · 같은 정규화형 자리 전부): "
          + ", ".join(f"`{x['id'].split('-', 4)[-1]}`→{x.get('phrase_id')}" for x in convx),
          f"- 옛 네 칸 edge_create(adverse_tuple) {len(conv_e)} — R30 이라 경과 자리 없음(세 칸 끝 · 경과 「미상」 버림 아님 = 원래 null): " + ", ".join(f"`{x['id'].split('-', 4)[-1]}`" for x in conv_e), ""]
    exo = [x for x in log if x["id"].startswith(EXO)]
    o += ["#### 엑소좀(EXO-02·05·06 · v3.1 kind)", "", md_table(["결정", "kind", "단계", "결과", "내용"], [(x["id"].replace("DEC-2026-11-05-B3-", ""), x["kind"], x["stage"], x["result"],
          (f"{x.get('product')}: {x.get('from_code')}→{x.get('to_code')} · {x.get('old_id')} → {x.get('new_id')}(옛 id alias)" if x["kind"] == "product_reclassify" else
           f"{x.get('dictionary')} 「{x.get('canonical')}」 동의어 「{x.get('removed_synonym')}」 제거" if x["kind"] == "dictionary_remove" else ", ".join(x.get("ends") or []))) for x in exo]), ""]
    r4 = [e for e in S.R.get("R4", []) if e["attrs"].get("reclassified_from_modality")]
    r32e = [e for e in S.R.get("R32", []) if e["attrs"].get("basis", {}).get("value") == "edge_create"]
    rule = next((r for r in S.E["clinical_rule"].values() if r["attrs"]["kind"][0]["value"] == "product_note"), None)
    o.append(f"- ② 재분류: R4 {len(r4)} 엣지가 M5 → M4 로 옮겨졌다(reclassified_from_modality · decision_id · section_key 보존). 제품 레코드 id 는 새 PRD-, 옛 id 는 alias.")
    if rule:
        o.append(f"- ⑤ 임상 규칙: clinical_rule(product_note) 「{rule['attrs']['text'][0]['value']}」(`{rule['attrs']['source_locator'][0]['value']}`) → R32 {len(r32e)}(scope=product · severity=prohibited · basis=edge_create) — ASCEplus · EXOSOME SKIN · 셀엑소좀. "
                 "기법=주사 끝은 만들지 않았다(R32 scope=all 은 주사 전체에 걸린다 · 발주서는 제품만).")
    o.append("- ⑥ 「PRP/엑소좀」 M5 동의어 제거 — 효과: treatment-optimization optimal_combo 「PRP/엑소좀」 이 계열 통째 일치가 아니라 `/` 대안(PRP · 엑소좀)으로 분해돼 combo_ref 패키지 +1 · R12 +3, "
             "그리고 그 이름을 그대로 쓰는 원장 계열 레코드 이름 2 곳(market-pricing categories[4].name · procedure-profiles profiles[4].name)이 사전 modality 밖 값 ⑧ 2 로 드러났다(원장 불변 · 판정은 conflict_close 또는 이름 결정).")
    o.append("")

    # ---------------------------------------------------------------- 변화표
    def tbl(title, k1, rename=None):
        keys = list(dict.fromkeys(list(b[k1]) + list(c[k1])))
        if k1 == "relations":
            keys = sorted(keys, key=lambda x: int(x[1:]))
        rows = []
        for k in keys:
            bv, cv = b[k1].get(k, 0), c[k1].get(k, 0)
            note = (rename or {}).get(k, "")
            rows.append((k, bv, cv, f"{cv - bv:+d}" if isinstance(bv, int) and isinstance(cv, int) and cv != bv else ("0" if bv == cv else "—"), note))
        o.extend([f"### {title}", "", md_table(["", "5차", "6차", "변화", "비고"], rows), ""])
    tbl("개체", "entities", {"adverse_expression": "v3.1 삭제(V3.1-10 · 문구 사전)", "adverse_effect": "세 칸 단위(V3.1-9) · 문구가 세운 조합 포함", "person_condition": "조건 단위(V3.1-4 · 사전 + raw_name)",
                             "clinical_rule": "+ disclosure(V3.1-7) · product_note(EXO-05) · 식별자 정규화 문장", "product": "엑소좀 2 재분류(id 재계산 · 수 그대로)", "conflict": "아래 충돌 표"})
    tbl("관계", "relations", {"R29": "v3.1 삭제", "R32": "v3.1 신설 — 고지 ledger + edge_create", "R15": "이름(이름마다) + 문구((출발, 단위) 마다 · source_phrases)", "R19": "문헌 adverse_effects 인용은 문구 사전 citations[]",
                              "R20": "끝 evidence_statement 만", "R31": "상대 부위 끝 없음(none)", "R16": "끝 = 조건 단위(원칙 B 로 문장 하나가 단위 둘이면 엣지 둘)", "R12": "session_count(V3.1-5) · EXO-06 combo"})
    gk = [("unresolved_references", "unresolved_references"), ("unregistered_fragments", "unregistered_fragments"), ("unlinked_expressions", "unlinked_phrases"), ("catalog_partial", "catalog_partial")]
    o.extend(["### 게이트", "", md_table(["", "5차", "6차", "비고"], [
        (f"{k5}→{k6}" if k5 != k6 else k5, b["gate"].get(k5, 0), c["gate"].get(k6, 0), "표현 레코드(자리) → 문구 사전 unlinked 항목 · 자리 " + str(c["gate"].get("unlinked_phrase_locators")) if k5 != k6 else
         ("⑧ 부작용 조각은 수식어 목록(V3.1-8)으로 줄고 고지 109 문장의 새 토큰으로 는다 · 조각 행 = (축, 조각)" if k5 == "unregistered_fragments" else "")) for k5, k6 in gk]), ""])
    tbl("충돌 kind 별", "conflicts")

    # ---------------------------------------------------------------- 문구 사전
    st = Counter(e["status"] for e in AU.phrases.values())
    nloc = sum(len(e["locators"]) for e in AU.phrases.values())
    nloc_by = Counter()
    for e in AU.phrases.values():
        nloc_by[e["status"]] += len(e["locators"])
    o += ["### 문구 사전(V3.1-10)", "",
          md_table(["", "결정 전(ERD 실측)", "6차(결정 뒤)"], [
              ("항목", A0["phrase_entries"], len(AU.phrases)),
              ("status(항목)", _kv(A0["phrase_entries_by_status"]), _kv(dict(st))),
              ("문구 자리(고지 포함 · 번역 제외)", A0["phrase_occurrences"] - A0["phrase_translations"], nloc),
              ("자리 status", _kv(Counter({k: v for k, v in A0["phrase_occurrences_by_status"].items()}) + Counter({"(고지)": A0["disclosures"]["n"]})), _kv(dict(nloc_by))),
              ("문구가 세운 단위(조합)", A0["units_created_by_phrases"], sum(1 for u in AU.units.values() if u.get("created_by_phrase"))),
              ("부록: R15 source_phrases 에 오른 항목", "—", len({p for e in S.R.get("R15", []) for p in (e["attrs"].get("source_phrases") or {}).get("value", [])})),
              ("부록: 게이트 unlinked_phrases", A0["phrase_entries_by_status"].get("unlinked"), c["gate"].get("unlinked_phrases")),
          ]), "",
          "결정 뒤 auto 가 는 것은 ① 사전 결정(DICT-COURSE-01 「지속」 · 동의어·부위 추가 등)으로 조각이 사전 값이 된 문구, approved 는 옛 표현 지정(TEV · ADV-COURSE)이 문구 사전 지도로 옮겨진 항목이다. 항목 id(PHR-)는 정규화형 유도라 경과·사전 값이 바뀌면 정규화형이 갈린다(ERD §1.1 S-5 — 지금 approved 항목은 결정 locator 로 다시 찾으므로 끊기지 않는다).", ""]

    # ---------------------------------------------------------------- 단위
    units = list(AU.units.values())
    dict_u = [u for u in units if u["event_kind"] == "dict"]
    by_ev = OrderedDict()
    for u in sorted(dict_u, key=lambda u: (u["event"], u["site"] or "", u["qualifier"] or "")):
        by_ev.setdefault(u["event"], []).append(u)
    combos = sorted(by_ev.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    o += ["### 단위(V3.1-9 · 사건, 부위, 물질)", "",
          f"단위 {len(units)}(사전 {len(dict_u)} + raw_name {len(units) - len(dict_u)}) — 결정 전(ERD) {A0['tuples_total']}(사전 {A0['tuples_dict']} + raw {A0['tuples_raw_name']}). "
          f"사건 {len(by_ev)} 중 조합이 둘 이상인 사건 {sum(1 for _, us in combos if len(us) >= 2)} · 하나뿐 {sum(1 for _, us in combos if len(us) == 1)}. 문구가 세운 조합 {sum(1 for u in units if u.get('created_by_phrase'))} · 결정이 세운 단위 {sum(1 for u in units if 'decision' in u['origins'])}.", "",
          md_table(["사건", "조합", "단위 (부위 · 물질 · 출처)"], [(ev, len(us), " · ".join(f"({u['site'] or 'none'}" + (f":{u['site_dict_kind']}" if u.get("site_dict_kind") else "") + f", {u['qualifier'] or 'none'}"
                                                                                                 + (" ← 문구" if u.get("created_by_phrase") else " ← 결정" if "decision" in u["origins"] and "complications" not in u["origins"] else "") + ")" for u in us)) for ev, us in combos]), ""]

    # ---------------------------------------------------------------- R15
    r15 = S.R.get("R15", [])
    pairs = {(e["from"]["type"], e["from"]["id"], e["to"]["id"]) for e in r15}
    wc = [e for e in r15 if (e["attrs"].get("course") or {}).get("value")]
    ph = [e for e in r15 if (e["attrs"].get("source_phrases") or {}).get("value")]
    o += ["### R15 may_cause(경과 = 엣지 속성 · 원칙 C)", "",
          md_table(["", "결정 전(ERD · (출발, 단위) distinct)", "6차"], [
              ("엣지", A0["edges_total"], f"레코드 {len(r15)} · (출발, 단위) distinct {len(pairs)}"),
              ("이름 유래 / 문구 유래", f"{A0['edges_from_names']} / {A0['edges_from_phrases']}", f"{sum(1 for e in r15 if not (e['attrs'].get('source_phrases') or {}).get('value') and 'pih_risk' not in e['attrs'])} / {len(ph)} (+ pih-risk {sum(1 for e in r15 if 'pih_risk' in e['attrs'])})"),
              ("경과 있는 엣지", A0["edges_with_course"], len(wc)),
              ("경과 값별", _kv(A0["edges_by_course"]), _kv(dict(Counter(co for e in wc for co in e["attrs"]["course"]["value"])))),
              ("고지 유래(disclosure)", A0["edges_disclosure"], sum(1 for e in r15 if (e["attrs"].get("disclosure") or {}).get("value"))),
          ]), "",
          "이름 유래 엣지는 이름마다 하나(severity·incidence 같은 속성이 이름의 것)라 레코드 수가 (출발, 단위) distinct 보다 많다. 경과는 그 단위 후보의 경과만 — 검산 V3.1-9 가 문구 엣지마다 확인한다(S-1).", ""]

    # ---------------------------------------------------------------- 조건
    cu = list(CU.units.values())
    o += ["### 조건 단위(V3.1-4)", "",
          f"이름 자리 {C0['occurrences']} · distinct {C0['names_distinct']}(kind 포함 {C0['names_distinct_with_kind']}) → 단위 **{len(cu)}**(사전 {sum(1 for u in cu if u['name_kind'] == 'dict')} + raw_name {sum(1 for u in cu if u['name_kind'] == 'raw_name')}) · "
          f"kind {_kv(dict(Counter(u['kind'] for u in cu)))} · 문장 부록 {sum(len(u['phrases']) for u in cu)}(원칙 B 로 문장 하나가 단위 둘이면 둘에 붙는다) · R16 {c['relations'].get('R16')} · R17 {c['relations'].get('R17')}. "
          "5차의 person_condition 298(문자열 식별)은 v3.1 에서 쓰지 않는다 — 결정 B3-R16-01·02 의 끝(locator)은 그 문장의 조건 단위로 닿았다.", ""]

    # ---------------------------------------------------------------- 묶음 4
    if g4:
        o += ["### 결정 묶음 4 제안(동의어 · proposed — 빌드가 읽지 않음)", "",
              f"`decisions/batch4-proposed/` {g4.get('proposals', 0)} · 게이트 `out/gate/batch4.json`(2B 스키마) 고를 자리 {g4.get('leaves')} · 추천 있음 {g4.get('recommended')} · 추천 없음 {g4.get('not_recommended')}. "
              f"① 부작용 문구 조각 {g4.get('adverse', 0)} · ② 부위·물질 조각 {g4.get('site_material', 0)} · ③ 시술 조각 {g4.get('procedure', 0)}. 승인하면 닫히는 문구 자리 합 {g4.get('closes_phrases', 0)} · 참조 합 {g4.get('closes_references', 0)}(추천대로 고를 때 · 항목 effect).", ""]
    with open(os.path.join(out_dir, "report.md"), "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(o) + "\n")
