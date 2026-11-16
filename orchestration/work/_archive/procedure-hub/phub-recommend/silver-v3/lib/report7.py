# -*- coding: utf-8 -*-
"""report.md §15 「7차 빌드 · ERD v3.2」 — 6차(baseline/manifest-6차.json · ERD v3.1) 대비.

결정 적용(옛 결정의 v3.2 새 구조 · 사유) · 변화표(개체 · 관계 · 충돌 · 게이트) · 부작용 문구 분포(exact/new/메모/설명문 · 안 붙음) · 원장 사건 노드 · ⑦ strong/weak ·
타임라인 줄 분포 · 응급 징후 · 고지 · 문헌 · 항목 자신/제품 승격 · ⑨ · R15 상속 basis 분포 · 게이트 5 요약.
"""
import json
import os
from collections import Counter, OrderedDict

from .units32 import ACTIVE
from .util import md_table


def _kv(d):
    return " · ".join(f"{k} {v}" for k, v in d.items()) if d else "—"


def _what_kinds(counts):
    out = Counter()
    for k, v in (counts or {}).items():
        out[k.rsplit(":", 1)[-1]] += v
    return out


def equipment_line(ctx):
    i0 = ctx["proc0"]["v32"]["equipment"]["items"]
    i1 = ctx["proc"]["v32"]["equipment"]["items"]
    reg0 = {x["name"] for x in i0 if x["register"]}
    why = Counter((x["excluded"] or "").split(":")[0] for x in i1 if not x["register"] and x["name"] in reg0)
    already = sorted({x["excluded"].split(":", 1)[1] for x in i1 if not x["register"] and x["name"] in reg0 and (x["excluded"] or "").startswith("already:")})
    return (f"- 장비 자동 등록: 장비 항목 {len(i1)} · 결정 전 등록 {len(reg0)} → 7차 {sum(1 for x in i1 if x['register'])} — 결정 전에 등록되던 것 중 7차에 등록하지 않은 {sum(why.values())}(사유 {_kv(dict(why))}): "
            "approved 결정(dictionary_add · 묶음 1 등)이 이미 그 이름을 사전 값(" + ", ".join(already[:12]) + (" …" if len(already) > 12 else "") + ")으로 두어 「이미 사전 값」이다 — 그 항목도 product 로 승격되는 것은 같다.")


def seventh(S, out_dir, baseline_dir, m, g5=None):
    p6 = os.path.join(baseline_dir, "manifest-6차.json")
    if not os.path.exists(p6):
        return
    b = json.load(open(p6, encoding="utf-8"))["counts"]
    c = m["counts"]
    ctx = S.ctx
    log = m["decisions"]["apply_log"]
    AU = ctx["AU"]
    A, A0 = ctx["adv"], ctx["adv0"]
    s0, s1 = A0["summary"], A["summary"]
    P0, P1 = ctx["proc0"]["summary"], ctx["proc"]["summary"]
    o = ["", "## 15. 7차 빌드 · ERD v3.2", "",
         "6차 = `baseline/manifest-6차.json`(ERD v3.1 · 결정 457) · 7차 = ERD **v3.2**(`erd-v3.2.json` · `erd-v3.2-dictionaries.json` 의 파생 항목(원장 사건 노드 · 장비 제품)은 빼고 분해가 다시 세운다 · 빌더 `lib/v32.py` · 발주서 `silver-build-7-brief.md`). "
         f"③ 결정 적용 전 분해 = `erd-v3.2-tuples.json` 요약 차이 {m['erd_comparison']['diff']}/{m['erd_comparison']['keys']}(§5 · 행 대조는 check ③). 결정은 6차와 같은 저장소(새 결정 0) — 옛 결정을 v3.2 구조로 옮겨 적용했다.", ""]

    # ---------------------------------------------------------------- 결정
    res = Counter((x["kind"], x["result"]) for x in log)
    o += ["### 결정 적용(7차)", "", md_table(["kind", "applied", "recorded", "rejected", "no_target"], [(k, *(res.get((k, r), 0) for r in ("applied", "recorded", "rejected", "no_target"))) for k in sorted({x["kind"] for x in log})]), ""]
    bad = [x for x in log if x["result"] in ("rejected", "no_target")]
    o.append("거부·대상 없음: " + ("**0** — 기존 결정(_bootstrap · batch1 · 2a · 2b · 3) 전부 v3.2 빌더가 받았다." if not bad else f"{len(bad)}"))
    for x in bad:
        o.append(f"- `{x['id']}` {x['kind']} — {x['result']}: {x.get('why')}")
    nm = [x for x in log if x["kind"] == "adverse_tuple_assign" and x.get("replaced_units") is not None]
    ph = [x for x in log if x["kind"] == "adverse_tuple_assign" and x.get("phrase_id")]
    tl = [x for x in log if x["kind"] == "adverse_tuple_assign" and x.get("line_locator")]
    o += ["", "v3.2 새 구조로 옮겨 적용한 옛 결정(거부 아님 · 사유는 적용 로그 note):", "",
          f"- 옛 이름 단위(raw_name) 대상 adverse_tuple_assign **{len(nm)}** — v3.2 에는 이름 단위가 없다(V3.2-0 노드 원칙). 같은 locator 의 이름 단위(원장 사건 노드 · 사전 사건)를 지정 단위로 대체:", ""]
    o.append(md_table(["결정", "이름 locator", "v3.2 분해 단위(대체 전)", "지정 단위"], [(x["id"].split("-", 4)[-1], x["locator"].split("@")[-1],
                                                                                  ", ".join(f"{AU.units[u]['event'] if u in AU.units else u}" for u in x["replaced_units"]) or "—",
                                                                                  ", ".join(f"({AU.units[u]['event']}, {AU.units[u].get('site') or 'none'}, {AU.units[u].get('qualifier') or 'none'})" for u in x["units"] if u in AU.units)) for x in nm]))
    o += ["", f"- 옛 표현 지정(kind=expression · 부작용 문구 자리) **{len(ph)}** — 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · status approved): " + ", ".join(f"`{x['id'].split('-', 4)[-1]}`→{x['phrase_id']}" for x in ph),
          f"- 옛 표현 지정(타임라인 줄) **{len(tl)}** — v3.2 타임라인 줄은 문구 사전이 아니라 자기 테이블(post_procedure_timeline · V3.2-9) — 그 줄의 참조(adverse_ref · R34)를 지정 단위로 · 경과는 계열 R15 경과: "
          + ", ".join(f"`{x['id'].split('-', 4)[-1]}`({x['locator'].split('@')[-1]} → 줄 {x['line_locator'].split('@')[-1]} · 경과 {', '.join(x['courses']) or '—'})" for x in tl), ""]

    # ---------------------------------------------------------------- 변화표
    def tbl(title, k1, notes=None):
        keys = list(dict.fromkeys(list(b.get(k1, {})) + list(c.get(k1, {}))))
        if k1 == "relations":
            keys = sorted(keys, key=lambda x: int(x[1:]))
        rows = []
        for k in keys:
            bv, cv = b.get(k1, {}).get(k, 0), c.get(k1, {}).get(k, 0)
            rows.append((k, bv, cv, f"{cv - bv:+d}" if isinstance(bv, int) and isinstance(cv, int) and cv != bv else ("0" if bv == cv else "—"), (notes or {}).get(k, "")))
        o.extend([f"### {title}", "", md_table(["", "6차", "7차", "변화", "비고"], rows), ""])
    eqp = ctx.get("equipment_products", [])
    tbl("개체", "entities", {"adverse_effect": "원장 사건 노드 단위(V3.2-0) · 이름 단위(raw_name) 없음", "product": f"장비 제품 자동 등록 {len(eqp)}(origin=taxonomy · V3.2-5) — 그중 step1 제품과 이름이 닿아 합친 것 포함",
                             "evidence_statement": "+ 문헌 adverse_effects 32(kind=adverse_effects · V3.2-0)", "post_procedure_timeline": "v3.2 신설(V3.2-9)", "emergency_sign": "v3.2 신설(V3.2-0)",
                             "procedure": "토큰화·성분 what·장비 승격", "conflict": "아래 충돌 표", "person_condition": "토큰화(V3.2-1)로 raw_name 일부가 사전 단위로"})
    tbl("관계", "relations", {"R15": "(출발, 단위) 마다 하나 · 이름+문구+타임라인+응급 참조 · inheritance · layer", "R33": "v3.2 신설", "R34": "v3.2 신설(줄 → 단위 참조)", "R35": "v3.2 신설",
                              "R4": "+ 장비 제품(계열 → 제품)", "R19": "+ 문헌 adverse_effects 인용", "R20": "+ 계열 → adverse_effects 근거", "R31": "단위가 는 만큼", "R3": "장비 승격(항목 이름 = 제품)", "R27": "성분 what 튜플은 R27 끝 없음(해석 보류)"})
    tbl("충돌 kind 별", "conflicts")
    gk = ["unresolved_references", "unregistered_fragments", "unlinked_phrases", "unlinked_phrase_locators", "catalog_partial", "conflicts_md_duplicate"]
    o.extend(["### 게이트", "", md_table(["", "6차", "7차", "비고"], [(k, b["gate"].get(k, 0), c["gate"].get(k, 0),
                                                                  {"unlinked_phrases": "v3.2 부작용 축에 미연결 상태 없음(새 노드 · 메모 · 설명문)", "unregistered_fragments": "부작용 문구 미등록 조각은 핵심어 노드 · side · 설명으로(⑧ 은 시술·조건 축 위주)",
                                                                   "conflicts_md_duplicate": "+ ⑦ 원장 사건 노드 쌍(strong · weak) · 장비 제품 ↔ 기존 제품"}.get(k, "")) for k in gk]), ""])

    # ---------------------------------------------------------------- 부작용 문구 분포
    pst = Counter(e["status"] for e in AU.phrases.values())
    ploc = Counter()
    for e in AU.phrases.values():
        ploc[e["status"]] += len(e["locators"])
    unatt = sum(len(e["locators"]) for e in AU.phrases.values() if e["status"] in ACTIVE and not e["units"])
    o += ["### 부작용 문구 분포(V3.2-0 · V3.2-7)", "",
          md_table(["", "결정 전(ERD 실측)", "7차(결정 뒤)"], [
              ("부작용 문구 자리", s0["safety_occurrences"], sum(ploc.values())),
              ("자리 status", _kv(s0["safety_by_status"]), _kv(dict(ploc))),
              ("문구 사전 항목(부작용) · 메모 항목", f"{s0['safety_entries']} · {s0['memo_entries']}", f"{sum(v for k, v in pst.items() if k in ACTIVE)} · {sum(v for k, v in pst.items() if k not in ACTIVE)}"),
              ("항목 status", _kv(s0["safety_entries_by_status"]) + " + 메모 " + _kv(s0["memo_entries_by_status"]), _kv(dict(pst))),
              ("어느 단위에도 안 붙은 부작용 문구(unlinked)", s0["adverse_unattached"], unatt),
              ("complications 이름 65", _kv(s0["complications_by_status"]), _kv(dict(Counter(r["status32"] for r in A["complications"])))),
          ]), "",
          "exact = 사전 사건에 닿음 · new = 핵심어 새 노드에 닿음 · note = 메모(사건 0 + 메모 어휘) · sentence = 설명문(문턱) · approved = 옛 표현 지정이 문구 사전 지도로. 미연결 상태는 없다(ERD §0.2).", ""]

    # ---------------------------------------------------------------- 노드 · ⑦
    dups = ctx.get("ledger_dup_conflicts", [])
    gr = Counter((x.get("grade"), x["status"]) for x in dups)
    eqd = ctx.get("equipment_dup_conflicts", [])
    gone = sorted({n["canonical"] for n in A0["ledger_events"]} - {n["canonical"] for n in A["ledger_events"]})
    new = sorted({n["canonical"] for n in A["ledger_events"]} - {n["canonical"] for n in A0["ledger_events"]})
    units = list(AU.units.values())
    o += ["### 원장 사건 노드 · ⑦ duplicate_candidate", "",
          md_table(["", "결정 전(ERD 실측)", "7차(결정 뒤)"], [
              ("원장 사건 노드(origin=ledger · unreviewed)", s0["ledger_events"], s1["ledger_events"]),
              ("부작용 단위 · event_kind", f"{s0['units_total']}", f"{len(units)} · {_kv(dict(Counter(u['event_kind'] for u in units)))}"),
              ("⑦ 노드 쌍 strong / weak", f"{s0['dup_pairs_strong']} / {s0['dup_pairs_weak']}", f"{s1['dup_pairs_strong']} / {s1['dup_pairs_weak']} (충돌 레코드 {_kv({f'{k[0]}·{k[1]}': v for k, v in gr.items()})})"),
              ("⑦ 장비 제품 ↔ 기존 제품(접두)", "13(씨앗 ⑦)", len(eqd)),
          ]), "",
          f"결정 전 → 7차 노드 차이: 빠짐 {', '.join(gone) or '없음'} · 새로 {', '.join(new) or '없음'} — 이미 approved 인 ① 사전 결정(부위·동의어 추가)이 그 토막의 조각을 사전 값으로 만들어 핵심어가 남지 않았다.", ""]

    # ---------------------------------------------------------------- 타임라인 · 응급 · 고지 · 문헌
    lines = [ln for _, _, ln in AU.lines.values()]
    by_lv = OrderedDict()
    for lv in ("normal", "abnormal", "caution", "emergency"):
        by_lv[lv] = Counter(ln["ref_status"] for ln in lines if ln["reaction_level"] == lv)
    r33 = S.R.get("R33", [])
    o += ["### 타임라인 줄 · 응급 징후 · 고지 · 문헌(자기 테이블 · 참조만)", "",
          md_table(["", "결정 전(ERD 실측)", "7차(결정 뒤)"], [
              ("타임라인 · 단계 · 줄", f"{s0['timelines']} · {s0['timeline_phases']} · {s0['timeline_lines']}", f"{len(AU.timelines)} · {sum(len(T['phases']) for T in AU.timelines)} · {len(lines)}"),
              ("줄 상태", _kv(s0["timeline_lines_by_status"]), _kv(dict(Counter(ln['ref_status'] for ln in lines)))),
              ("R34 timeline_refers", s0["r34"], c["relations"].get("R34", 0)),
              ("응급 징후(SGN) · 상태", f"{s0['emergency_signs']} · {_kv(s0['emergency_signs_by_status'])}", f"{len(AU.signs)} · {_kv(dict(Counter(x['ref_status'] for x in AU.signs)))}"),
              ("R35 sign_refers", s0["r35"], c["relations"].get("R35", 0)),
              ("필수 고지 자리 · 상태", f"{s0['disclosures']} · {_kv(s0['disclosures_by_status'])}", f"{len(AU.disclosures)} · {_kv(dict(Counter(x['ref_status'] for x in AU.disclosures)))}"),
              ("문헌 adverse_effects · 상태", f"{s0['literature']} · {_kv(s0['literature_by_status'])}", f"{len(AU.literature)} · {_kv(dict(Counter(x['ref_status'] for x in AU.literature)))}"),
          ]), "",
          md_table(["반응 등급", "ref", "ref_partial", "none", "normal_memo"], [(lv, *(cn.get(k, 0) for k in ("ref", "ref_partial", "none", "normal_memo"))) for lv, cn in by_lv.items()]), "",
          f"- R33 has_timeline {len(r33)}: 끝 " + _kv(dict(Counter(e['from']['type'] for e in r33))) + " — 타임라인 이름이 튜플로 풀리면 그 튜플, 아니면 category 계열(V3.2-9).",
          f"- 결정이 바꾼 줄: " + (", ".join(f"{ln['locator'].split('@')[-1]}({', '.join(ln['decision_ids'])})" for ln in lines if ln.get("decision_ids")) or "없음") + " · 참조 끝이 사라져 뺀 참조: " + str(len(getattr(AU, "dropped_refs", []))), ""]

    # ---------------------------------------------------------------- 항목 자신 · 제품 승격 · 성분 what · ⑨
    wk6 = _what_kinds(b.get("procedure_by_origin_what"))
    wk7 = _what_kinds(c.get("procedure_by_origin_what"))
    cat_self6 = sum(v for k, v in (b.get("procedure_by_origin_what") or {}).items() if k.startswith("catalog_item") and k.endswith(":catalog_item"))
    cat_self7 = sum(v for k, v in (c.get("procedure_by_origin_what") or {}).items() if k.startswith("catalog_item") and k.endswith(":catalog_item"))
    o += ["### 항목 자신 · 제품 승격 · 성분 what(V3.2-5 · V3.2-6)", "",
          md_table(["", "6차", "결정 전(ERD v3.2 실측)", "7차"], [
              ("분류 항목 → what_kind(항목 521)", "—", _kv(P0["catalog_by_what_kind"]), _kv(P1["catalog_by_what_kind"])),
              ("항목 자신이 시술(분류 항목 원천 튜플 what=catalog_item)", cat_self6, P0["catalog_self_items"], cat_self7),
              ("튜플 what_kind(전체)", _kv(dict(wk6)), _kv(P0["tuples_by_what_kind"]), _kv(dict(wk7))),
              ("장비 제품 자동 등록(origin=taxonomy)", 0, len(ctx["proc0"]["v32"]["equipment"]["products"]), len(eqp)),
          ]), "",
          equipment_line(ctx),
          f"- 성분 what(분류 항목): " + (", ".join(f"{r['name']}[{r['family']}]" for r in ctx["proc"]["cat_recs"] if r.get("what_kind") == "ingredient") or "없음") + " · R27 끝 없는 성분 what 튜플 " + str(len(ctx.get("r27_skipped", []))) + "(성분은 사전 값 · 개체 아님 — 해석 보류)", ""]
    u6p = os.path.join(baseline_dir, "unresolved_references-6차.json")
    if os.path.exists(u6p):
        u6 = json.load(open(u6p, encoding="utf-8"))
        cur = json.load(open(os.path.join(out_dir, "gate", "unresolved_references.json"), encoding="utf-8"))
        k6 = {(r["slot"], r["label"], r["hint"]) for r in u6}
        k7 = {(r["slot"], r["label"], r["hint"]) for r in cur}
        o += ["### ⑨ 미해결 참조", "", f"6차 {len(u6)} → 7차 **{len(cur)}** — 풀림 {len(k6 - k7)} · 새로 {len(k7 - k6)}. 사유별(7차) " + _kv(dict(Counter(r['reason'] for r in cur).most_common(8))), ""]
        if k6 - k7:
            o.append("풀린 참조: " + " · ".join(f"「{l}」@{h or '—'}" for s_, l, h in sorted(k6 - k7, key=str)[:40]))
        if k7 - k6:
            o.append("새로 미해결: " + " · ".join(f"「{l}」@{h or '—'}" for s_, l, h in sorted(k7 - k6, key=str)[:40]))
        o.append("")

    # ---------------------------------------------------------------- R15 상속
    rows = ctx.get("r15_v32", [])
    r15 = S.R.get("R15", [])
    items = [x for x in rows if x[1] == "item"]
    attrs = ["severity", "incidence", "onset", "duration", "mechanism", "management", "prevention", "risk_factors"]
    by = {a: Counter() for a in attrs}
    for _, _, _, inh in items:
        for x in inh:
            by[x["attr"]][x["basis"]] += 1
    byf = {a: Counter() for a in attrs}
    for _, layer, _, inh in rows:
        if layer == "family":
            for x in inh:
                byf[x["attr"]][x["basis"]] += 1
    o += ["### R15 may_cause · 속성 상속(V3.2-8 · 참조만)", "",
          f"R15 {len(r15)}(결정 전 ERD (출발, 단위) {s0['edges_total']}) · layer {_kv(dict(Counter(x[1] for x in rows)))} · 타임라인 참조가 있는 엣지 {sum(1 for e in r15 if (e['attrs'].get('timeline_refs') or {}).get('value'))} · 응급 참조 {sum(1 for e in r15 if (e['attrs'].get('emergency_sign_refs') or {}).get('value'))} · "
          f"경과 있는 엣지 {sum(1 for e in r15 if (e['attrs'].get('course') or {}).get('value'))} · basis 없는 상속 {sum(1 for x in rows for i in x[3] if not i.get('basis'))} · 값 복사 {sum(1 for x in rows for i in x[3] if 'value' in i)}.", "",
          "항목·제품 출발(layer=item) — 속성마다 basis:", "",
          md_table(["속성", "item", "family", "unit", "none"], [(a, *(by[a].get(k, 0) for k in ("item", "family", "unit", "none"))) for a in attrs]), "",
          "계열 출발(layer=family) — 속성마다 basis:", "",
          md_table(["속성", "family", "unit", "none"], [(a, *(byf[a].get(k, 0) for k in ("family", "unit", "none"))) for a in attrs]), ""]

    # ---------------------------------------------------------------- 게이트 5
    if g5:
        bi = g5["by_item"]
        o += ["### 결정 묶음 5 게이트(노드 단위 · `out/gate/batch5.json`·`.md`)", "",
              md_table(["묶음", "자리", "추천"], [(k, v["leaves"], v["recommended"]) for k, v in bi.items()]), "",
              f"고를 자리 {g5['leaves']} · 옵션 {g5['options']} · 추천 {g5['recommended']} · 원문 {g5['evidence']}(읽기 실패 {g5['read_fail']}) · ⑦ weak {g5['weak']} 은 `batch5-weak.json`(게이트에 올리지 않음). "
              "고른 답 → `python3 apply_gate.py --gate out/gate/batch5.json --answers answers.json`(→ decisions/batch5/).", ""]
        r5 = S.ctx.get("gate5r")
        if r5:
            o += [f"축소본(`out/gate/batch5-reduced.json`·`.md` · 사람이 볼 것만 · 원본은 그대로): 고를 자리 **{r5['leaves']}** — " + " · ".join(f"{k} {v}" for k, v in r5["by_item"].items()) +
                  f". 규칙 자동 결정 {r5['rule_decisions']}(접기 {r5['auto_folds']} {_kv(r5['folds_by_rule'])} · 줄임말 매핑 {r5['abbrev_maps']} · 만들지 않음 {r5['abbrev_skipped']}) — `decisions/batch5-rule/`(proposed · 빌드가 읽지 않음) · "
                  f"원장 사건 노드는 게이트에서 빼고 `batch5-nodes.md`(참고) · 자동 접기 목록 `batch5-auto-folds.md`.", ""]
    with open(os.path.join(out_dir, "report.md"), "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(o) + "\n")
