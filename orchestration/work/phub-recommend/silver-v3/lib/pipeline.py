# -*- coding: utf-8 -*-
"""빌드 순서(ERD v3.1) — 입력 검증 → 결정 읽기 → 사전(⓪ product_reclassify · ① dictionary_add → canonical_rename → dictionary_remove · ④ event_split) → 분해(시술 · 부작용 단위·문구 사전 · 조건 단위)
→ ① phrase_map → 개체 → ⓪ reclassification ②③④ → 관계 → ⑤ → 충돌(V3-10 fold 의 ⑦ 닫음) → ⑥ → ⑦."""
import json
import os
from collections import OrderedDict

from . import conflicts as CF
from . import decisions as DC
from . import entities as EN
from . import entities32 as EN32
from . import relations as RL
from .adverse31 import run_adverse31, run_condition
from . import v32 as V32
from .units32 import AdverseUnits32
from .anchors import build_anchor_map
from .units31 import AdverseUnits, CondUnits
from .core import Silver, compile_sources
from .decompose import MARKET_SLOT, Lexicon, Resolver, is_scoped_label_mapping, run_procedure, with_alias
from .load import bronze_info, load_bronze, load_column_map, load_json
from . import core
from .provenance import P, loc
from .refs import occurrences
from .util import mkid, norm


def run(args):
    erd = load_json(args.erd)
    dic0 = load_json(args.dict)
    is33 = erd.get("erd_version") == "v3.3"
    is32 = erd.get("erd_version") in ("v3.2", "v3.3")   # v3.3 은 v3.2 경로 + 분석기(V3.3-B) · R2 사전 값(C) · category 삭제(E) · product.kind(A)
    ANZ = None
    if is33:
        from .analyzer import Analyzer
        ANZ = Analyzer(getattr(args, "kiwi_cache", None), getattr(args, "kiwi_python", None))
    if is32:
        dic0 = V32.base_dictionary(dic0)   # v3.2: 사전 파일의 파생 항목(원장 사건 노드 · 장비 제품)은 빼고 분해가 다시 세운다(참조 구현과 같다)
    core.set_erd_files(args.erd, args.dict)
    L, meta = load_bronze(erd, args.bronze, args.step1)
    prev = load_json(args.tuples_prev) if getattr(args, "tuples_prev", None) and os.path.exists(args.tuples_prev) else None
    binfo = bronze_info(args.bronze)
    bver = (binfo or {}).get("version") or 1
    cmap = load_column_map(args.colmap)
    trust = {s["file"]: s["trust_tier"] for s in erd["source_files"]}

    # --- 결정 저장소
    store = DC.load_store(args.decisions)
    invalid, approved, listed = [], [], []
    for f, d in store:
        errs = DC.validate(d)
        if errs:
            invalid.append({"file": f, "id": d.get("id"), "errors": errs})
            continue
        (approved if d["status"] == "approved" else listed).append(dict(d, _file=f))

    # --- ⓪ product_reclassify · ① 사전(dictionary_add → canonical_rename → dictionary_remove) · ④ event_split → 분해
    log = []
    trules = erd["tuple_rules"]
    dict_decs = [d for d in DC.ordered(approved) if d["kind"] in ("product_reclassify", "dictionary_add", "canonical_rename", "dictionary_remove", "event_split")]

    node_folds, not_adverse, node_decs = {}, {}, []
    if is32:
        node_folds, not_adverse, node_decs = DC.node_decisions(approved)
    XS = {}

    def decompose(dic_, with_nodes=True):
        if is32:
            P_, A_, C_, X_ = V32.run_v32(dic_, erd, L, scoped_decs, bver, node_folds=node_folds if with_nodes else None, not_adverse=not_adverse if with_nodes else None, analyzer=ANZ)
            XS["last"] = X_
            P_["v32"] = X_
            return P_, A_, C_
        P_ = run_procedure(dic_, erd["resolve_rules"], L, scoped_decs, prev_tuples=None, bronze_version=bver)
        A_ = run_adverse31(P_["ids"], trules, L, prev)
        C_ = run_condition(dic_, trules["condition"], L)
        return P_, A_, C_

    def in_use(name, entry, dic_now):
        """dictionary_remove 값 제거 판정 — 지금 사전으로 분해했을 때 그 값을 쓰는 자리(시술 조각 · 부작용 조각 · 조건 조각) · 개체 식별 사전이면 그 개체 레코드."""
        if name in DC.dict_entities(erd, dic_now):
            return [f"{name} 값은 개체 식별(개체 레코드가 그 값을 쓴다)"]
        P_, A_, C_ = decompose(dic_now)
        canon = entry["canonical"]
        kind_of = {"product_name": "product", "modality": "modality", "modality_subcategory_label": "modality_subcategory", "catalog_item_name": "procedure", "site": "site", "unit": "spec", "product_tier": "product_tier",
                   "adverse_event_type": "event", "course": "course", "relative_site": "relative", "adverse_qualifier": "qualifier"}
        uses = []
        k = kind_of.get(name)
        if k:
            for r in P_["cat_recs"] + [r for v in P_["ref_rows"].values() for r in v] + P_["mk_rows"]:
                for g in r.get("groups") or []:
                    for m in g["members"]:
                        for sp in m["spans"]:
                            kk, cc = (sp[0], sp[1]) if not isinstance(sp, dict) else (sp["kind"], sp["canonical"])
                            if kk == k and norm(cc) == norm(canon):
                                uses.append(f"시술 「{r.get('label') or r.get('name')}」")
            for r in A_["complications"] + A_["phrase_dictionary"]:
                for sp in r.get("spans") or []:
                    if sp[0] == k and norm(sp[1]) == norm(canon):
                        uses.append(f"부작용 「{r.get('text') or r.get('normalized')}」")
        if name == "person_condition":
            uses += [f"조건 「{r['text']}」" for r in C_["phrases"] if canon in r["condition_fragments"]]
        return dedupe(uses)

    scoped_decs = [d for d in DC.ordered(approved) if is_scoped_label_mapping(d)]
    dic = DC.apply_dictionary(dic0, dict_decs, log, in_use) if dict_decs else dic0
    # ② canonical_mapping 중 라벨 조각 · scope=REF- 는 분해 때 그 anchor 안에서만 읽는다(미해결 참조는 튜플이 없다)
    scoped_saved = scoped_decs
    scoped_decs = []
    proc0, adv0, cond0 = decompose(dic0, with_nodes=False)
    cmp_base = None
    if is33:
        # v3.3: ERD 실측(erd-v3.3-tuples.py)은 분석기 없이 돈다 — ③ 대조·§5 는 분석기 없는 목록 규칙 분해로(실버 산출은 분석기 분해 · 차이는 report §16)
        Pb, Ab, Cb, Xb = V32.run_v32(dic0, erd, L, scoped_decs, bver, analyzer=None)
        Pb["v32"] = Xb
        cmp_base = (Pb, Ab, Cb)
    scoped_decs = scoped_saved
    if is32 and node_decs:
        node_decs = DC.validate_node_decisions(node_decs, node_folds, not_adverse, dic, adv0, log)
    if dict_decs or scoped_decs or node_decs:
        proc, adv, cond = decompose(dic)
    else:
        proc, adv, cond = proc0, adv0, cond0
    if is32:
        dic = V32.silver_dictionary(proc["v32"]["dic"], adv, node_decs, v33=is33)   # 결정 ① 뒤 사전 + 장비 제품(origin=taxonomy) + 원장 사건 노드(origin=ledger) · 접힌/뺀 노드 이력
    ids = proc["ids"]
    lex = proc["lex"]
    resolver = Resolver(lex, erd["resolve_rules"], ids)

    # --- 원장 메모 결정(⓪ · 질문 23) — 빌드가 적재하는 원장 작성자 결정
    memo = DC.ledger_memo_decisions(L, resolver, ids)
    for d in memo:
        if d.get("_not_loaded"):
            continue
        (approved if d["status"] == "approved" else listed).append(d)

    ctx = {"L": L, "erd": erd, "dic": dic, "dic0": dic0, "cmap": cmap, "trust": trust, "meta": meta, "proc": proc, "adv": adv, "cond": cond, "proc0": proc0, "adv0": adv0, "cond0": cond0, "ids": ids,
           "src": compile_sources(erd), "dicts": {d["name"]: d for d in dic["dictionaries"]}, "dic_index": {d["name"]: i for i, d in enumerate(dic["dictionaries"])},
           "occ": occurrences(L, lex), "args": args, "bronze": binfo}
    ctx["dindex"] = CF.DictIndex(dic)
    ctx["is33"] = is33
    ctx["analyzer"] = ANZ
    ctx["cmp_base"] = cmp_base
    S = Silver(ctx)
    S.apply_log = log
    ordered = DC.ordered(approved)
    # --- ① phrase_map(문구 사전 지도 · ① 끝 — 분해 뒤 · 지정 단위는 사전 값을 읽는다)
    AU = AdverseUnits32(ctx) if is32 else AdverseUnits(ctx)
    ctx["is32"] = is32
    if is32:
        DC.log_node_decisions(ctx, adv, node_decs, log)
    ctx["AU_live"] = AU
    ctx["CU"] = CondUnits(ctx)
    DC.apply_phrase_maps(ctx, AU, [d for d in ordered if d["kind"] == "phrase_map"], log)

    # --- 개체
    EN.build_source_files(S)
    EN.build_modality(S)
    EN.build_subcategories(S)
    EN.build_catalog(S)
    ctx["item_by_id"] = {it["item"]["id"]: it for it in ctx["items"].values()}
    ctx["item_by_id_cat"] = {it["cat"]["catalog_item_id"]: it for it in ctx["items"].values()}
    EN.build_products(S, resolver)
    if is32:
        EN32.products_v32(S)
    if is33:
        EN32.products_v33(S)
    EN.build_techniques(S)
    EN.build_sites(S)
    EN.build_structures(S)
    EN.build_problems(S)
    EN.build_pp_complaints(S)
    EN.build_conditions(S)
    EN.build_citations(S)
    EN.build_evidence(S)
    if is32:
        EN32.evidence_adverse(S)
    EN.build_rules(S)
    EN.build_packages(S)
    # combo_ref 패키지(참조 자리 조합)
    combo = {}
    rows = list(proc["ref_rows"].items()) + [(MARKET_SLOT, proc["mk_rows"])]
    for slot, rr in rows:
        occs = [o for o in ctx["occ"][slot]]
        for r in rr:
            if r["result"] == "combo_ref":
                pv = [o[2] for o in occs if (o[0], o[1]) == tuple(r["_in"])]
                rec = S.ent("package", mkid("PKG", f"combo_ref|{r['ref_id']}"), [loc(p) for p in pv])
                if "kind" not in rec["attrs"]:
                    S.dattr(rec, "kind", "combo_ref", [loc(p) for p in pv])
                    S.dattr(rec, "name", r["label"], [loc(p) for p in pv])
                    S.dattr(rec, "ref_id", r["ref_id"], [loc(p) for p in pv])
                combo[(slot, tuple(r["_in"]))] = rec["id"]
    ctx["combo_pkg"] = combo

    # --- anchor 지도(결정 전) — 분해기 튜플 집합과 같아야 한다
    AM = build_anchor_map(ctx)
    pre = set(AM.tuples())
    if pre != set(proc["PT"].tuples):
        raise AssertionError(f"anchor 지도 튜플 ≠ 분해기 튜플: {len(pre ^ set(proc['PT'].tuples))}")
    ctx["AM_live"] = AM

    # --- ⓪ reclassification (R2 만) · product_reclassify 는 사전 단계에서 적용했다(PRD- 재계산)
    recl = {}
    for d in ordered:
        if d["kind"] == "reclassification":
            recl[d["target"]["catalog_item_id"]] = {"id": d["id"], "modality_id": d["new_value"]["modality_id"]}
            log.append({"id": d["id"], "kind": d["kind"], "stage": "⓪", "result": "applied", "note": "R2 재배치만 — CAT- id 불변(3-B′)"})
    ctx["reclass"] = recl
    dup_sub = {}
    for sid, e in ids.sub.items():
        dup_sub.setdefault(e["id"], []).append(sid)
    for k, v in dup_sub.items():
        if len(v) > 1:
            S.note("modality_subcategory 식별자", f"하위분류 {v} 는 같은 계열·같은 라벨이라 식별자 규칙(계열 코드 + 정규화 label)상 한 레코드 {k} — id 는 alias 로 둘 다 보존(74 → 73)")
    if recl:
        S.note("⓪ reclassification", "reclassified_to 는 계열(M 코드)만 준다 — 재배치될 하위분류가 결정에 없어 R2 엣지는 원 하위분류에서 두고 reclassified_modality_id·decision_id 속성으로 표시했다(하위분류 지정은 사람 결정 몫)")

    # --- ② ③ ④(fold)
    DC.apply_tuples(ctx, AM, AU, [d for d in ordered if d["kind"] in ("canonical_mapping", "tuple_assign", "tuple_assign_multi", "adverse_tuple_assign", "fold_approve")], log)
    ctx["edge_units"] = []
    DC.prepare_edge_units(ctx, AU, [d for d in ordered if d["kind"] == "edge_create"], ctx["edge_units"])
    AU.finish()
    EN.build_procedures(S, AM)
    EN.build_adverse(S, AU)
    if is32:
        EN32.after_units(S, AU)

    # --- 관계
    RL.build_relations(S, AU)
    RL.finalize(S, AM, AU)
    DC.apply_edges(S, AM, AU, [d for d in ordered if d["kind"] == "edge_create"], log)

    # --- 충돌
    CF.reference_conflicts(S)
    CF.value_conflicts(S)
    CF.duplicate_candidates(S)
    if is32:
        CF.ledger_duplicates(S)
        for f in ctx.get("node_folds_applied", []):   # 노드 fold_approve 가 닫은 ⑦ 수(V3-10 과 같은 생애 · 적용 로그 closed_duplicates)
            n = sum(1 for c in S.conflicts if c["kind"] == "duplicate_candidate" and c["status"] == "resolved" and c.get("decision_id") == f["id"])
            for x in log:
                if x["id"] == f["id"] and x["kind"] == "fold_approve":
                    x["closed_duplicates"] = n
    CF.unregistered_conflicts(S)
    CF.dict_value_conflicts(S)
    for d in memo:
        if d["kind"] == "canonical_mapping" and d.get("_not_loaded"):
            S.unresolved_ref("canonical_mapping", "taxonomy.json:modality[].subcategories[].items[].canonical_category", d["unresolved_label"], d["unresolved_code"], d["provenance"],
                             "canonical_category 가 하위분류 사전에 없다(질문 23)", [d["unresolved_label"]], ref_id=d["target"]["from_ref"])
    ctx["fold_closed"] = CF.close_duplicates_by_fold(S, AM)   # V3-10
    ctx["fold_overlap_open"] = CF.duplicate_fold_overlap(S, AM)
    for f in ctx.get("folds", []):
        n = sum(1 for x in ctx["fold_closed"] if x["decision"] == f["id"])
        for x in log:
            if x["id"] == f["id"] and x["kind"] == "fold_approve":
                x["closed_duplicates"] = n
    DC.apply_conflicts(S, [d for d in ordered if d["kind"] in ("conflict_override", "conflict_close")], log)
    DC.apply_excludes(S, AM, [d for d in ordered if d["kind"] == "exclude"], log)

    # --- 기록만 kind
    for d in ordered:
        if d["kind"] in DC.RECORD_ONLY:
            log.append({"id": d["id"], "kind": d["kind"], "stage": "—", "result": "recorded", "note": "build_reads=false — 값을 바꾸지 않음"})
    S.ctx["decisions_approved"] = ordered
    S.ctx["decisions_listed"] = listed
    S.ctx["decisions_invalid"] = invalid
    S.ctx["AM"], S.ctx["AU"] = AM, AU
    return S


from .util import dedupe  # noqa: E402
