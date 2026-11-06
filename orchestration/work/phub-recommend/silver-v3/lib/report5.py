# -*- coding: utf-8 -*-
"""report.md §13 「5차 빌드 · ERD v3 + 묶음 3」 — 4차(baseline/manifest-4차.json · unresolved_references-4차.json) 대비.

v3 규칙만의 효과와 묶음 3 의 효과를 가르려고 묶음 3 을 뺀 사전으로 분해를 한 번 더 돌린다(수치만 · 산출물에 쓰지 않는다).
"""
import json
import os
from collections import Counter, OrderedDict

from . import decisions as DC
from .decompose import MARKET_SLOT, run_procedure
from .util import md_table, norm

B3 = "DEC-2026-11-05-B3"


def _rows(P):
    out = OrderedDict()
    for slot, rr in list(P["ref_rows"].items()) + [(MARKET_SLOT, P["mk_rows"])]:
        for r in rr:
            out.setdefault(r["ref_id"], r)
    return out


def _cause(r, r4, stop_words):
    if r["result"] == "multi_tuple":
        return "V3-4 부위 여럿(+ · /)"
    if r.get("alternatives"):
        return "V3-4 괄호 안 대안"
    if str(r.get("what_basis", "")).startswith("company_paren") or r.get("company"):
        return "V3-2 괄호 안 회사·제품"
    if r.get("member_mode") == "or" and r["result"] == "combo_ref":
        return "V3-4 `/` 대안(combo or)"
    frags = set(r4.get("fragments") or [])
    if r.get("qualifier_text") and frags and all(norm(f) in stop_words for f in frags):
        return "V3-3 stopwords"
    if r.get("qualifier_text") or r.get("session_index") is not None:
        return "V3-3 stopwords(+ 다른 조각 해소)"
    return "그 밖(규칙 조합)"


def fifth(S, out_dir, baseline_dir, m):
    p4 = os.path.join(baseline_dir, "manifest-4차.json")
    if not os.path.exists(p4):
        return
    b = json.load(open(p4, encoding="utf-8"))["counts"]
    c = m["counts"]
    ctx = S.ctx
    log = m["decisions"]["apply_log"]
    o = ["", "## 13. 5차 빌드 · ERD v3 + 묶음 3", "",
         "4차 = `baseline/manifest-4차.json`(ERD v2.4 · 브론즈 2판 · 결정 묶음 2B 까지) · 5차 = ERD **v3**(`erd-v3.json` · `erd-v3-dictionaries.json` · 빌더 V3-1~V3-10) + `decisions/batch3/` approved "
         f"{sum(1 for x in log if x['id'].startswith(B3))} 건(사용자 2026-11-05 · 발주서 `silver-build-5-brief.md`). 제안 `decisions/batch3-proposed/` 은 빌드가 읽지 않는다(목록 `_INDEX.md`). "
         f"③ 결정 적용 전 분해 = `erd-v3-tuples.json` 요약 차이 {m['erd_comparison']['diff']}/{m['erd_comparison']['keys']}(§5).", ""]

    # ---------------------------------------------------------------- 결정 적용
    def grp(x):
        i = x["id"]
        if i.startswith(B3):
            return "batch3"
        if "-B2B-" in i:
            return "batch2b"
        if "-B2A-" in i:
            return "batch2a"
        if "-B1-" in i:
            return "batch1"
        if i.startswith("DEC-2026-10-26"):
            return "원장 메모"
        return "_bootstrap"
    res = OrderedDict()
    for x in log:
        res.setdefault(grp(x), Counter())[x["result"]] += 1
    o += ["### 결정 적용", "", md_table(["묶음", "applied", "recorded", "rejected", "no_target"], [(k, v.get("applied", 0), v.get("recorded", 0), v.get("rejected", 0), v.get("no_target", 0)) for k, v in res.items()]), ""]
    b3 = [x for x in log if x["id"].startswith(B3)]
    o += [md_table(["kind(묶음 3)", "applied", "rejected", "no_target"], [(k, sum(1 for x in b3 if x["kind"] == k and x["result"] == "applied"), sum(1 for x in b3 if x["kind"] == k and x["result"] == "rejected"), sum(1 for x in b3 if x["kind"] == k and x["result"] == "no_target")) for k in sorted({x["kind"] for x in b3})]), ""]
    bad = [x for x in log if x["result"] in ("rejected", "no_target")]
    o.append("거부·대상 없음: " + ("없음." if not bad else " · ".join(f"`{x['id']}` {x['kind']} {x['result']}({x.get('why')})" for x in bad)))
    listed = [d for d in ctx["decisions_listed"] if d.get("status") == "proposed" and str(d.get("_file", "")).startswith("batch3-proposed")]
    o += ["", f"제안(batch3-proposed · status=proposed · 읽지 않음) {len(listed)} 건 — `decisions/batch3-proposed/_INDEX.md`.", ""]
    # 4차 거부 2 · 미적용 3
    l4 = {x["id"]: x for x in json.load(open(p4, encoding="utf-8"))["decisions"]["apply_log"]}
    lg = {x["id"]: x for x in log}
    AM = ctx["AM"]
    rows5 = _rows(ctx["proc"])
    o += ["### 4차에서 거부·미적용이던 것", ""]
    tab = []
    for did in ("DEC-2026-11-04-B2B-SLS-02", "DEC-2026-11-04-B2B-SLS-09"):
        x = lg.get(did, {})
        a = x.get("anchor")
        r = rows5.get(a, {})
        how = ("자동 해소 — v3 규칙(V3-4 괄호 안 대안)으로 참조가 튜플이 됐고 결정은 그 anchor 에 같은 값을 적용" if r.get("result") == "tuple" and not x.get("established") else "V3-9 — 결정이 미해결 anchor 의 튜플을 세움" if x.get("established") else "—")
        tab.append((did, "tuple_assign outer_only", l4.get(did, {}).get("result"), x.get("result"), f"「{r.get('label')}」 → {r.get('result')}" + (f" · alternatives {[a_['text'] for a_ in r['alternatives']]}" if r.get("alternatives") else ""), how))
    na = os.path.join(ctx["args"].decisions, "batch2b-answers", "_not_applied.json")
    labs = {"slash-together-or/03": "보톡스(턱선+광대)", "slash-together-or/08": "보톡스 이마+미간", "slash-together-or/12": "필러 볼+턱"}
    if os.path.exists(na):
        for k, v in sorted(json.load(open(na, encoding="utf-8")).items()):
            hits = [r for r in rows5.values() if str(r["label"]) == labs.get(k)]
            r = hits[0] if hits else {}
            ts = [AM.tid(AM.spec[a_]) for a_ in r.get("member_anchors", []) if a_ in AM.spec]
            tab.append((k, v["choice"], "결정 안 만듦", "결정 없음(규칙)", f"「{labs.get(k)}」 → {r.get('result')} · 부위 {r.get('sites')} · 튜플 {len(ts)}", "자동 해소 — V3-4 「무엇을 하나 × 부위 여럿」(같은 what 의 튜플 여럿 · R12 member_mode and · anchor #s<i>)" if r.get("result") == "multi_tuple" else "미해결"))
    o += [md_table(["결정·답", "고른 것", "4차", "5차", "참조 지금", "어떻게"], tab), ""]

    # ---------------------------------------------------------------- 변화표
    gk = ["unresolved_references", "unregistered_fragments", "unlinked_expressions", "catalog_partial"]
    o += ["### 게이트 4종", "", md_table(["", "4차", "5차", "변화"], [(k, b["gate"][k], c["gate"][k], f"{c['gate'][k] - b['gate'][k]:+d}") for k in gk]), ""]

    def tbl(title, k1):
        keys = sorted(set(b[k1]) | set(c[k1]), key=lambda x: (len(x), x) if k1 == "relations" else x)
        rows = [(k, b[k1].get(k, 0), c[k1].get(k, 0), c[k1].get(k, 0) - b[k1].get(k, 0)) for k in keys]
        o.extend([f"### {title}", "", md_table(["", "4차", "5차", "변화"], [(r[0], r[1], r[2], f"{r[3]:+d}" if r[3] else "0") for r in rows]), ""])
    tbl("충돌 kind 별", "conflicts")
    n7 = sum(1 for x in S.conflicts if x["kind"] == "duplicate_candidate")
    r7 = [x for x in S.conflicts if x["kind"] == "duplicate_candidate" and x["status"] == "resolved"]
    o += [f"- **⑦ 닫힘(V3-10)**: duplicate_candidate {n7} 중 fold_approve 가 닫은 것 **{len(r7)}**(status=resolved · decision_id · 결정별 " + ", ".join(f"{d}×{n}" for d, n in sorted(Counter(x['decision_id'] for x in r7).items())) + f") · 4차는 0(규칙 없음). "
          f"「쌍의 ⑦」= ⑦ 레코드의 원장 위치가 전부 그 결정의 anchors 위치이고 anchor 둘 이상에 걸친 것 — fold anchor 위치에 하나라도 닿는 open ⑦ 은 {ctx.get('fold_overlap_open', 0)}(한쪽이 접는 anchor 밖 표면형이라 결정이 판정한 쌍이 아님 · conflict_close 몫).", ""]
    tbl("개체", "entities")
    tbl("관계", "relations")

    # ---------------------------------------------------------------- v3 규칙으로 자동 해소
    u4 = json.load(open(os.path.join(baseline_dir, "unresolved_references-4차.json"), encoding="utf-8"))
    u4r = {x["ref_id"]: x for x in u4 if str(x.get("ref_id", "")).startswith("REF-")}
    # 묶음 3 을 뺀 사전(= 4차 결정 + ERD v3 규칙)으로 분해
    nob3 = [d for d in DC.ordered(ctx["decisions_approved"]) if d["kind"] in ("dictionary_add", "canonical_rename", "event_split") and not d["id"].startswith(B3)]
    dic_nob3 = DC.apply_dictionary(ctx["dic0"], nob3, [])
    scoped = [d for d in DC.ordered(ctx["decisions_approved"]) if DC.is_scoped_label_mapping(d) and not d["id"].startswith(B3)]
    Pn = run_procedure(dic_nob3, ctx["erd"]["resolve_rules"], ctx["L"], scoped)
    rows_n = _rows(Pn)
    stop = {norm(w["word"]) for w in ctx["erd"]["resolve_rules"]["step2_decompose"]["stopwords"]["words"]}
    by_v3, by_b3, still = [], [], []
    open9 = {x.get("ref_id") for x in S.conflicts if x["kind"] == "unresolved_reference" and x["status"] == "open"}
    for rid, x in u4r.items():
        rn = rows_n.get(rid)
        r5 = rows5.get(rid)
        if rn and rn["result"] in ("tuple", "combo_ref", "multi_tuple"):
            by_v3.append((rid, x, rn, _cause(rn, x, stop)))
        elif rid not in open9 and r5 is not None:
            by_b3.append((rid, x, r5))
        else:
            still.append((rid, x, r5))
    cz = Counter(z[3] for z in by_v3)
    pv = ctx["proc0"]["summary"]
    st = pv["stopwords"]
    o += ["### v3 규칙으로 자동 해소된 참조", "",
          f"4차 미해결 참조(⑨ · REF- anchor) {len(u4r)} 중 **v3 규칙만으로** 튜플이 된 것 **{len(by_v3)}**(묶음 3 없이 · 4차 결정 사전 + ERD v3 규칙으로 다시 분해) · 묶음 3 사전·지정으로 풀린 것 **{len(by_b3)}** · 남은 것 {len(still)}.", "",
          md_table(["원인(v3 규칙)", "참조"], sorted(cz.items(), key=lambda z: -z[1])), "",
          md_table(["anchor", "라벨", "4차 사유[조각]", "5차", "원인"], [(rid, x["label"], f"{x['reason']}[{','.join(x.get('fragments') or [])}]", f"{rn['result']}" + (f" 부위 {rn.get('sites')}" if rn.get('sites') else "") + (f" «{','.join(rn['qualifier_text'])}»" if rn.get('qualifier_text') else "") + (f" {{{','.join(a['text'] for a in rn['alternatives'])}}}" if rn.get('alternatives') else ""), cause) for rid, x, rn, cause in by_v3]), "",
          f"ERD 실측(결정 전 · ERD 사전 · `erd-v3-tuples.json`)의 같은 규칙 효과: `+` 4곳 중 multi_tuple {sum(1 for x in pv['combo_plus_v2'] if x['result'] == 'multi_tuple')}(필러 팔자+볼 은 「팔자」 미등록 → 묶음 3 SIT-02 로 해소) · 괄호 안 대안 {len(pv['alternatives'])} · stopwords 로 새로 튜플이 된 참조 {st['references_resolved_newly']}(결과가 바뀐 참조 {len(st['references_changed'])}) · 괄호 안 회사·제품 {pv['company_paren']['applied_n']}. "
          f"실버(결정 뒤 사전)에서는 묶음 1·2A 의 동의어(HIFU·RF·얼굴 전체 …)가 더해져 괄호 안 대안 {sum(1 for r in rows5.values() if r.get('alternatives'))} · multi_tuple {sum(1 for r in rows5.values() if r['result'] == 'multi_tuple')} · 회사·제품 괄호 라벨 {len({a['label'] for a in ctx['proc']['PT'].company_applied})}.", ""]
    if by_b3:
        o += ["묶음 3 으로 풀린 참조:", "", md_table(["anchor", "라벨", "4차 사유[조각]", "5차"], [(rid, x["label"], f"{x['reason']}[{','.join(x.get('fragments') or [])}]", r5["result"] + (f" 부위 {r5.get('sites')}" if r5.get('sites') else "")) for rid, x, r5 in by_b3]), ""]

    # ---------------------------------------------------------------- 미해결 사유 · 상위 조각
    o9 = [x for x in S.conflicts if x["kind"] == "unresolved_reference" and x["status"] == "open"]
    reasons = Counter(x.get("reason") for x in o9)
    frag = Counter(f for x in o9 for f in (x.get("fragments") or []))
    o += ["### 미해결(⑨ open) 사유 · 상위 조각", "",
          f"⑨ open {len(o9)}(참조 자리 {sum(1 for x in o9 if str(x.get('ref_id', '')).startswith('REF-'))}) · 사유: " + ", ".join(f"{k}={v}" for k, v in reasons.most_common()) + ".", "",
          "미해결 참조의 미등록 조각 상위 30(참조 수): " + " · ".join(f"`{f}`×{n}" for f, n in frag.most_common(30)), ""]
    # ---------------------------------------------------------------- V3 구현 요약
    o += ["### 빌더 v3(V3-1~V3-10) — 이번 빌드 실측", "",
          md_table(["#", "무엇", "실측(5차)"], [
              ("V3-1", "부작용 수식 칸 qualifier · 네 칸 식별자 · 접두 가름", f"수식 사전 {len(ctx['ids'].qualifier)} · qualifier≠none 단위 {sum(1 for u in ctx['AU'].units.values() if u.get('qualifier_id', 'none') != 'none')} · 접두 가름 {len(ctx['adv']['summary']['prefix_splits'])}(" + ", ".join(f"{a}→{q}+{e}" for a, q, e in ctx['adv']['summary']['prefix_splits']) + ")"),
              ("V3-2", "괄호 안 회사·제품", f"적용 라벨 {len({a['label'] for a in ctx['proc']['PT'].company_applied})}: " + " · ".join(dict.fromkeys(f"「{a['label']}」→{a['product']}" + (f"(회사 {a['company']})" if a['company'] else "(괄호 안 제품)") for a in ctx['proc']['PT'].company_applied))),
              ("V3-3", "stopwords → qualifier_text · session_index", f"qualifier_text 참조 {sum(1 for r in rows5.values() if r.get('qualifier_text'))} · session_index {sum(1 for r in rows5.values() if r.get('session_index') is not None)} · 엣지 속성 R9/R12/R17/R18 qualifier_text {sum(1 for rel in ('R9', 'R12', 'R17', 'R18') for e in S.R.get(rel, []) if any(k.endswith('qualifier_text') for k in e['attrs']))}"),
              ("V3-4", "`+`/`/` · multi_tuple(#s<i>) · member_mode · alternatives", f"multi_tuple {sum(1 for r in rows5.values() if r['result'] == 'multi_tuple')} · 괄호 안 대안 {sum(1 for r in rows5.values() if r.get('alternatives'))} · combo_ref member_mode {dict(Counter(r.get('member_mode') for r in rows5.values() if r['result'] == 'combo_ref'))}"),
              ("V3-5", "site.kind · layer 는 시술 site 금지", f"부위 kind {dict(Counter(ctx['ids'].site_kind.values()))} · 시술 layer site 0 · 부작용 layer 단위 {sum(1 for u in ctx['AU'].units.values() if u.get('site_dict_kind') == 'layer')}"),
              ("V3-6", "canonical_rename", " · ".join(f"{x['renamed'][0]}→{x['renamed'][1]}({x['old_id']}→{x['new_id']})" for x in log if x['kind'] == 'canonical_rename' and x['result'] == 'applied') or "0"),
              ("V3-7", "description·media_refs", "새 브론즈 원천 0 → 값 0(빌더는 출처 있는 값만 싣는다)"),
              ("V3-8", "R5 하위분류 기법(canonical_mapping R5:<하위분류>)", f"적용 {len(ctx.get('r5_sub_decisions', []))} · 제안 batch3-proposed P-TEC-*"),
              ("V3-9", "미해결·조합·#s anchor 에도 ③", f"결정이 세운 자리 {len(AM.established)} · anchor 부재 거부 0"),
              ("V3-10", "fold_approve 가 ⑦ 을 닫음", f"{len(r7)}"),
          ]), ""]
    with open(os.path.join(out_dir, "report.md"), "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(o) + "\n")
