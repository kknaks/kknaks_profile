# -*- coding: utf-8 -*-
"""ERD v2.3 산출물 생성기. v2.2 생성기(erd_build_v22.py)를 바탕으로 2차 독립 검토 반영 수정 7건(erd_spec_v23 · erd_colmap_v23 · erd-v2.3-tuples.py)만 덧씌운다.
입력: 원장 21 + step1-products.json + 스캔 JSON + erd_spec_v23/erd_colmap_v23 + erd-v1.json(§9.2) + erd-v1.1.json + erd-v2.2.json·erd-v2.2-tuples.json(§9.5·§9.6 나란히 비교 · 변경 목록 · 결정 이관)
출력: erd-v2.3.md · erd-v2.3.json · erd-v2.3-column-map.md · erd-v2.3-dictionaries.json · erd-v2.3-tuples.json(+검산 결과 부착). 이전 판 파일은 지우지 않는다.
"""
import json
import os
import re
import sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_build as B  # noqa
import erd_build_v11 as B11  # noqa
import erd_build_v2 as B2  # noqa
import erd_build_v22 as B22  # noqa
import erd_spec_v23 as S  # noqa
import erd_colmap_v23 as C  # noqa

WORK = HERE
LEDGER = S.LEDGER_DIR
STEP1 = S.STEP1_FILE
norm, mkid, sha256, values_at, distinct_at, md_table = B.norm, B.mkid, B.sha256, B.values_at, B.distinct_at, B.md_table
Dict_ = B.Dict_
L = B.L
SCAN = B.SCAN
FILES = B.FILES
load_module = B11.load_module
RESOLVE = B11.RESOLVE
TUPLES = load_module("erd_v23_tuples", os.path.join(WORK, "erd-v2.3-tuples.py"))
OUT = {"md": "erd-v2.3.md", "json": "erd-v2.3.json", "cmap": "erd-v2.3-column-map.md", "dict": "erd-v2.3-dictionaries.json", "tuples": "erd-v2.3-tuples.json", "check": "erd-v2.3-check.py"}
RULE_REF = {"value_conflict": "⑥", "duplicate_candidate": "⑦", "unregistered_value": "⑧", "unresolved_reference": "⑨"}


# ---------------------------------------------------------------------------
# 사전 — v2.2 와 값 동일. 경과 사전 비고만 v2.3 경과 규칙 문장(§1.5·§2.14·§4 동일)
# ---------------------------------------------------------------------------
def build_dictionaries_v23():
    DICTS = B2.build_dictionaries_v2()
    d = Dict_("course", "부작용 경과", S.COURSE_RULE)
    d.kind = "value"
    for canon, syns, src in S.COURSES:
        if src is None:
            d.add_canonical(canon, "(ERD 정의)", "(default)", 0, kind="default")
            continue
        n = sum(1 for v, _ in values_at(*src) if v and norm(canon) in norm(v))
        assert n > 0, f"경과 사전 정준값 출처 없음: {canon}"
        d.add_canonical(canon, src[0], src[1], n, kind="derived")
        for sv, ss in syns:
            ns = sum(1 for v, _ in values_at(*ss) if v and norm(sv) in norm(v))
            assert ns > 0, f"경과 사전 동의어 출처 없음: {canon} ~ {sv}"
            d.add_synonym(norm(canon), sv, ss[0], ss[1], ns, link="수식어(derived)", kind="derived")
    DICTS["course"] = d
    return DICTS


DERIVED_ID_RE = re.compile(r"\b(PRC|ADV|CFL)-")


def migrate_decisions(v22erd):
    """v2.2 결정 23 을 그대로 이관(모양 동일 · target 에 파생 id 0 확인) + v2.3 개정 DEC-24(proposed)."""
    recs, mig = [], []
    for o in v22erd["decisions"]:
        r = OrderedDict((k, o[k]) for k in S.DECISION_COMMON_FIELDS)
        recs.append(r)
        mig.append({"id": r["id"], "v2_2": {k: o.get(k) for k in ("kind", "decided_by", "decided_at", "status")}, "v2_3": {k: r[k] for k in ("kind", "decided_by", "decided_at", "status")},
                    "derived_id_in_target": bool(DERIVED_ID_RE.search(json.dumps(r["target"], ensure_ascii=False))), "change": "없음(그대로) — target 은 ERD 절·항목 번호(안정 키)"})
    recs.append(OrderedDict([("id", "DEC-2026-11-04-24"), ("kind", "scope_review"),
                             ("target", {"erd_ref": "§1.1 locator · §1.5 경과·접힘 규칙 · §2.5 procedure.technique_id · §2.7 technique · §2.14 adverse_effect · §2.15 adverse_expression.match_status · §2.20 conflict.stable_key · §2.21 decision · §3 엣지 끝 규칙(R3·R9·R12·R15·R16·R17·R18) · R29 출처 · R30 · §5 적용 순서 · §5.2 kind 16", "review_item": "erd-v2.2-review.md ⑥ 1~6 (발주서 7건)"}),
                             ("new_value", {"disposition": "v2.3: 엣지 끝 = 시술 튜플 · 경과는 사건에 바로 붙은 수식어만 · 부작용 미등록 조각 접힘 금지(raw_name) · 결정 kind +4(edge_create · tuple_assign_multi · adverse_tuple_assign · conflict_close) · 결정 target 안정 키 + 적용 순서 ①~⑦ · 기법 잔재 제거 · R29 출처 +11"}),
                             ("reason", "2차 독립 검토 동결 전 구조 7건 전부 수용 — 제안 2026-11-04. ERD 승인 때 approved"),
                             ("decided_by", None), ("decided_at", None), ("status", "proposed"),
                             ("source_refs", [{"kind": "brief", "ref": "erd-v2.3-brief.md (사용자 승인 「진행하자」)"}, {"kind": "review", "ref": "erd-v2.2-review.md ⑥"}])]))
    return recs, mig


def dict_json(dicts):
    return OrderedDict([("erd_version", S.ERD_VERSION), ("bronze_snapshot", S.SNAPSHOT), ("normalize_rule", S.NORMALIZE_RULE["name"]),
                        ("source_kinds", {"value": "그 경로의 값 자체", "key": "그 경로의 키 이름(또는 섹션 키)이 값 — 단수/복수 차이 허용", "derived": "그 경로의 합성값에서 ③ 형식 교정으로 잘라낸 부분값(원문의 부분 문자열)",
                                          "default": "ERD 정의 기본값 — 원장에 값이 없는 자리를 채우는 정의값(course 「미상」 하나뿐)"}),
                        ("dictionary_kinds", {"value": "값 사전(열거·라벨)", "entity_name_index": "개체 이름 색인 — B 분해 규칙이 읽는 제품·하위분류·분류 항목 이름(개체의 식별 이름을 사전 모양으로 노출)"}),
                        ("dictionaries", [dict(d.to_json(), kind=getattr(d, "kind", "value")) for d in dicts.values()])])


def build_column_map(step1_scan):
    rows = []
    for f, v in SCAN["files"].items():
        for p, st in v["leaf_paths"].items():
            r = C.resolve(f, p)
            if r is None:
                raise RuntimeError(f"미정 {f} {p}")
            rows.append({"file": f, "path": p, "type": "/".join(st["types"].keys()), "count": st["count"], "dest": r[1], "target": r[2], "note": r[3]})
    for p, st in step1_scan["leaf_paths"].items():
        r = C.resolve(STEP1, p)
        if r is None:
            raise RuntimeError(f"미정 {STEP1} {p}")
        rows.append({"file": STEP1, "path": p, "type": "/".join(st["types"].keys()), "count": st["count"], "dest": r[1], "target": r[2], "note": r[3]})
    return rows


def mermaid():
    lines = ["erDiagram"]
    rels = [
        ("MODALITY", "MODALITY_SUBCATEGORY", "||--o{", "R1 has_subcategory"), ("MODALITY_SUBCATEGORY", "CATALOG_ITEM", "||--o{", "R2 has_catalog_item"),
        ("PROCEDURE", "PRODUCT", "}o--o{", "R3 uses_product (항목 튜플)"), ("MODALITY", "PRODUCT", "||--o{", "R4 offers_product"),
        ("MODALITY", "TECHNIQUE", "}o--o{", "R5 applies_technique"),
        ("PROCEDURE", "CATALOG_ITEM", "||--o{", "R26 derived_from"), ("PROCEDURE", "MODALITY", "}o--o|", "R27 what"), ("PROCEDURE", "MODALITY_SUBCATEGORY", "}o--o|", "R27 what"), ("PROCEDURE", "PRODUCT", "}o--o|", "R27 what"), ("PROCEDURE", "CATALOG_ITEM", "}o--o|", "R27 what (항목 자신)"),
        ("PROCEDURE", "SITE", "}o--o|", "R28 procedure_site"), ("PROCEDURE", "TECHNIQUE", "}o--o|", "technique(dict)"),
        ("PROBLEM", "PROBLEM_SUBCATEGORY", "||--o{", "R6"),
        ("PROBLEM_SUBCATEGORY", "COMPLAINT", "||--o{", "R7 has_complaint"), ("COMPLAINT", "MODALITY", "}o--o{", "R8 addressed_by"),
        ("COMPLAINT", "PROCEDURE", "}o--o{", "R9 recommends"), ("COMPLAINT", "SITE", "}o--o|", "R10 located_at"),
        ("PROBLEM_SUBCATEGORY", "SITE", "}o--o|", "R11 subcategory_site"), ("PACKAGE", "PROCEDURE", "}o--o{", "R12 member"),
        ("PACKAGE", "PROBLEM", "}o--o{", "R13 for_problem"), ("COMPLAINT", "PACKAGE", "}o--o{", "R14 offers_combo"),
        ("PROCEDURE", "ADVERSE_EFFECT", "}o--o{", "R15 may_cause"), ("SITE", "ADVERSE_EFFECT", "}o--o{", "R15 may_cause"),
        ("ADVERSE_EXPRESSION", "ADVERSE_EFFECT", "}o--o|", "R29 expresses"), ("ADVERSE_EFFECT", "ADVERSE_EFFECT", "}o--o{", "R30 leads_to (edge_create)"), ("ADVERSE_EFFECT", "SITE", "}o--o|", "R31 adverse_site"),
        ("PROCEDURE", "PERSON_CONDITION", "}o--o{", "R16 contraindicated_for"), ("PERSON_CONDITION", "PROCEDURE", "}o--o{", "R17 age_group_guidance"),
        ("PROCEDURE", "PROCEDURE", "}o--o{", "R18 interaction"), ("EVIDENCE_STATEMENT", "CITATION", "}o--||", "R19 cites"),
        ("ADVERSE_EXPRESSION", "CITATION", "}o--o|", "R19 cites"), ("CLINICAL_RULE", "CITATION", "}o--o|", "R19 cites"),
        ("MODALITY", "EVIDENCE_STATEMENT", "||--o{", "R20 has_evidence"), ("MODALITY", "ADVERSE_EXPRESSION", "||--o{", "R20 has_evidence"), ("SITE", "ANATOMICAL_STRUCTURE", "}o--o{", "R21 contains"),
        ("SITE", "MODALITY", "}o--o{", "R22 injection_guidance"), ("CONFLICT", "DECISION", "}o--o|", "R24 resolved_by"),
        ("SOURCE_FILE", "CONFLICT", "||--o{", "R25 provenance"),
    ]
    for a, b, c, lab in rels:
        lines.append(f"    {a} {c} {b} : \"{lab}\"")
    lines.append("    %% v2.3: R3·R9·R12·R15·R16·R17·R18 의 시술 축 끝은 PROCEDURE 튜플(참조가 튜플로 해결되면 · 기본). MODALITY|MODALITY_SUBCATEGORY|PRODUCT 노드가 끝인 것은 참조가 그 층까지만 적혀 있을 때뿐(target_depth). PROCEDURE 의 what 은 CATALOG_ITEM 자신일 수도 있고 미상 칸이 있으면 anchor(CAT-/REF-) 튜플 — 접힘은 세 칸 전부 사전 값일 때만. ADVERSE_EFFECT 도 미등록 조각이 있는 이름은 raw_name(anchor=원장 locator) 튜플. DECISION 은 안정 키(CAT-/REF-/locator/고정 id/사전 값/conflict.stable_key)로만 닿는다(R24). R25 provenance 는 모든 개체에 닿는다")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 산출물
# ---------------------------------------------------------------------------
def write_outputs(colrows, dicts, step1_scan, v1erd, v11erd, v22erd, v22tup):
    tiers = {f: (t, basis, note) for f, t, basis, note in S.SOURCE_FILES}
    files_meta = []
    for f in FILES + [STEP1]:
        data = L[f]
        meta = {}
        if isinstance(data, dict):
            for k in ["version", "updated", "description", "consensus_method", "source_method", "currency", "note", "generated_at", "scope"]:
                if isinstance(data.get(k), (str, int)):
                    meta[k] = str(data[k])
        t, basis, note = tiers[f]
        path = os.path.join(LEDGER, f) if f != STEP1 else os.path.join(WORK, f)
        fm = {"file": f, "kind": S.SOURCE_KIND[f], "path_dir": "ledger" if f != STEP1 else "work", "sha256": sha256(path), "bytes": os.path.getsize(path),
              "snapshot_date": S.SNAPSHOT if f != STEP1 else "2026-10-29", "trust_tier": t, "trust_basis": basis, "trust_note": note, "trust_flag": S.TRUST_FLAGS.get(f),
              "version": meta.get("version"), "updated": meta.get("updated") or meta.get("generated_at"), "method": meta.get("consensus_method") or meta.get("source_method"),
              "leaf_paths": SCAN["files"][f]["leaf_count"] if f != STEP1 else step1_scan["leaf_count"]}
        if f == STEP1:
            n2 = sum(1 for v, _ in values_at(STEP1, "items[].4_license.licenses[].source") if v and re.search(S.STEP1_TIER2_SOURCE_RE, v))
            ntot = sum(1 for _ in values_at(STEP1, "items[].4_license.licenses[].license_no"))
            fm["trust_tier_rule"] = {"tier2_when": f"items[].4_license.licenses[].source =~ /{S.STEP1_TIER2_SOURCE_RE}/", "tier2_licenses": n2, "licenses_total": ntot, "else": 3}
            fm["items"] = len(L[STEP1]["items"])
        files_meta.append(fm)
    dest_counter = Counter(r["dest"] for r in colrows)
    ent_json = [{"key": e["key"], "prefix": e["prefix"], "label": e["label"], "definition": e["definition"], "identity": e["identity"], "beyond_minimum": e.get("beyond_minimum", False), "aliases": e["aliases"],
                 "attrs": [{"name": a[0], "type": a[1], "required": a[2], "sources": a[3], "rule": a[4]} for a in e["attrs"]]} for e in S.ENTITIES]
    rel_json = [{**r, "attrs": [{"name": a[0], "type": a[1], "note": a[2]} for a in r["attrs"]]} for r in S.RELATIONS]
    dj = dict_json(dicts)
    json.dump(dj, open(os.path.join(WORK, OUT["dict"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    dic_json = json.load(open(os.path.join(WORK, OUT["dict"]), encoding="utf-8"))
    v1rep = v1erd.get("resolution_report") if v1erd else None
    RES, TOTAL = RESOLVE.run_all(TUPLES.with_alias(dic_json), S.RESOLVE_RULES, L, L[STEP1], v1rep)
    TUP = TUPLES.run_all(dic_json, S.TUPLE_RULES, L, S.RESOLVE_RULES)
    TUP["procedure"]["v21_none_fold_split"] = TUPLES.v21_split(TUP)
    json.dump(TUP, open(os.path.join(WORK, OUT["tuples"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    IDX = B.Index()
    CONF = B11.conflict_estimates_v11(IDX, RES)
    for c in CONF:
        c["rule_ref"] = RULE_REF.get(c["kind"])
        c["status_on_build"] = "open"
        c["close_kind"] = "conflict_close(not_same) · fold_approve" if c["kind"] == "duplicate_candidate" else "conflict_override · conflict_close" if c["kind"] == "value_conflict" else "dictionary_add · conflict_close" if c["kind"] == "unregistered_value" else "tuple_assign(_multi) · dictionary_add · conflict_close(needs_source)"
    Q14 = B11.q14_bundles_v11()
    SITE_TABLE = B11.site_replacement_table(dicts)
    res_summary = OrderedDict()
    for k, v in RES.items():
        res_summary[k] = {kk: vv for kk, vv in v.items() if kk != "rows"}
        res_summary[k]["v1"] = ({"n": v1rep[k]["n"], "resolved": v1rep[k]["resolved"], "unresolved": v1rep[k]["unresolved"], "by_depth": v1rep[k]["by_depth"]} if v1rep and k in v1rep else None)
    decisions, decisions_migration = migrate_decisions(v22erd)
    moves = [{"file": f, "path": p, "v1_1": a, "v2": b} for f, p, a, b in C.MOVES]
    moves22 = [{"file": f, "path": p, "v2_1": a, "v2_2": b} for f, p, a, b in C.MOVES_V22]
    moves23 = [{"file": f, "path": p, "v2_2": a, "v2_3": b} for f, p, a, b in C.MOVES_V23]
    notes23 = [{"file": f, "path": p, "target": t, "note": n} for f, p, t, n in C.NOTE_CHANGES_V23]
    ps, as_ = TUP["procedure"]["summary"], TUP["adverse"]["summary"]
    EE_rows = [{k: v for k, v in r.items() if k != "ends"} for r in TUP["procedure"]["edge_ends"]]
    erd = OrderedDict([
        ("erd_version", S.ERD_VERSION), ("previous_version", "v2.2"), ("status", "draft — 사용자 승인 전"), ("written", "2026-11-04"), ("bronze_snapshot", S.SNAPSHOT),
        ("layers", {"bronze": "원장 21 그대로 + 조사 산출물 step1-products.json 1 (바이트 보존, SHA256 식별)", "semantic": "이 ERD + 값 사전 + 분해 규칙(참조 §1.3 · 튜플 §1.4/§1.5), 승인이 정본 조건, 버전 개정", "silver": "ERD 를 따르는 정규화 레코드, 모든 값에 (file, path) 출처", "gold": "실버 조합 뷰, 새 사실 금지"}),
        ("normalize_rule", S.NORMALIZE_RULE), ("id_rule", S.ID_RULE), ("fold_condition", S.FOLD_CONDITION), ("course_rule", S.COURSE_RULE), ("adverse_fold_rule", S.ADVERSE_FOLD_RULE), ("locator_rule", S.LOCATOR_RULE),
        ("edge_end_rule", S.EDGE_END_RULE), ("edge_end_kinds", S.EDGE_END_KINDS), ("proc_axis_edges", S.PROC_AXIS_EDGES),
        ("resolve_rules", S.RESOLVE_RULES), ("tuple_rules", S.TUPLE_RULES),
        ("source_files", files_meta),
        ("entities", ent_json), ("relations", rel_json), ("enums", S.ERD_ENUMS),
        ("quality_rules", [{"no": a, "class": b, "rule": c} for a, b, c in S.QUALITY_RULES]),
        ("synonym_key_normalization", v1erd["synonym_key_normalization"] if v1erd else {}),
        ("q25", [{"no": n, "answer": a} for n, a in S.Q25]),
        ("review_dispositions", [{"no": no, "title": B.REVIEW[no - 1]["title"], "decided_by": who, "disposition": what, "applied_at": where} for no, (who, what, where) in S.DISPOSITIONS.items()]),
        ("decision_kinds", [{"kind": k, "build_reads": br, "target": t, "new_value": nv, "note": n, "new_in_v2_2": k in S.DECISION_KINDS_NEW, "new_in_v2_3": k in S.DECISION_KINDS_NEW_V23, "reshaped_in_v2_3": S.DECISION_KINDS_RESHAPED_V23.get(k)} for k, br, t, nv, n in S.DECISION_KINDS]),
        ("decision_common_fields", S.DECISION_COMMON_FIELDS), ("decision_build_rule", S.DECISION_BUILD_RULE),
        ("decision_target_rule", S.DECISION_TARGET_RULE),
        ("decision_apply_order", [{"stage": st, "kinds": ks, "why": why} for st, ks, why in S.DECISION_APPLY_ORDER]), ("decision_apply_order_rule", S.DECISION_APPLY_ORDER_RULE),
        ("decisions", decisions), ("decisions_migration", decisions_migration),
        ("site_replacement_8_2", SITE_TABLE),
        ("q14_bundles", Q14),
        ("step1_column_scan", {"file": STEP1, "leaf_count": step1_scan["leaf_count"], "bytes": step1_scan["bytes"], "method": "bronze-ledger-column-scan.py FileScan (같은 접기 규칙)", "top_level": step1_scan["top_level"]}),
        ("column_map_summary", {"leaf_paths": len(colrows), "by_file_group": {"ledger_21": sum(1 for r in colrows if r["file"] != STEP1), "step1": sum(1 for r in colrows if r["file"] == STEP1)},
                                "by_dest": dict(dest_counter), "by_dest_ledger_21": dict(Counter(r["dest"] for r in colrows if r["file"] != STEP1)), "by_dest_step1": dict(Counter(r["dest"] for r in colrows if r["file"] == STEP1)),
                                "by_entity": dict(Counter(r["target"].split(".")[0] for r in colrows if r["dest"] == "개체")), "by_dict": dict(Counter(r["target"] for r in colrows if r["dest"] == "사전")),
                                "by_relation": dict(Counter(r["target"].split(".")[0].split("(")[0] for r in colrows if r["dest"] == "엣지"))}),
        ("column_map_moves", moves), ("column_map_moves_v2_2", moves22), ("column_map_moves_v2_3", moves23), ("column_map_note_changes_v2_3", notes23),
        ("dictionaries_summary", [{"name": d.name, "label": d.label, "kind": getattr(d, "kind", "value"), "canonical": len(d.entries), "synonyms": sum(len(e["synonyms"]) for e in d.entries.values()), "candidates": len(d.candidates)} for d in dicts.values()]),
        ("resolution_report", res_summary), ("resolution_total", TOTAL),
        ("tuple_report", {"procedure": ps, "adverse": as_}),
        ("tuple_report_v2_2", {"procedure": (v22erd or {}).get("tuple_report", {}).get("procedure"), "adverse": (v22erd or {}).get("tuple_report", {}).get("adverse")}),
        ("edge_ends", {"rows": EE_rows, "total": ps["edge_ends_total"], "total_n": ps["edge_ends_total_n"], "by_relation": ps["edge_ends_by_relation"], "slots": ps["edge_ends_slots"]}),
        ("v21_none_fold_split", TUP["procedure"]["v21_none_fold_split"]),
        ("technique_inheritance_candidates", TUP["procedure"]["inheritance_candidates"]),
        ("r29_taxonomy_safety_keys", S.R29_TAXONOMY_SAFETY_KEYS),
        ("conflict_estimates", CONF),
    ])
    json.dump(erd, open(os.path.join(WORK, OUT["json"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = ["# ERD v2.3 — 잎 키 행선지 표 (원장 21 + step1-products.json)", "",
          f"**v2.2 와 행선지·표적이 다른 행은 {len(moves23)} 개다(이동 없음).** 비고만 바뀐 행 {len(notes23)}(아래 「비고 변경 v2.2 → v2.3」 — 수정 1: 시술 축 참조 자리 16 + pih procedure_ref + timeline category 에 「끝 = procedure 튜플」 · 수정 7: taxonomy safety 잎 키 11 에 「R29 출처」 · 수정 2·3: complications name). 그 밖 행선지·표적·비고는 v2.2 와 같다(검산 A 행 단위 대조). 규칙 `erd_colmap_v23.py`.", "",
          f"작성 2026-11-04 · 입력 `bronze-ledger-column-scan.json`(원장 잎 키 {sum(1 for r in colrows if r['file'] != STEP1)}) + `step1-products.json` 잎 키 {step1_scan['leaf_count']}(`bronze-ledger-column-scan.py` 와 같은 방식으로 스캔) = {len(colrows)} · 행선지 범주 5: 개체 / 사전 / 엣지 / 브론즈 / 버림 · **미정 0**", "",
          f"표적 표기: `entity.attr` · `dict:<사전>` · `R#.attr`(관계 번호는 erd-v2.3.md §3) · `bronze` · `drop`. v1.1 과 달라진 행 {len(moves)}(v2 구조 변경 ①② · 아래 이동 표 v1.1 → v2) + v2.2 {len(moves22)} + v2.3 {len(moves23)}.", "",
          "## 비고 변경 (v2.2 → v2.3 · 표적 동일)", "", md_table(["#", "파일", "경로", "표적", "추가된 비고"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['target']}`", m["note"]) for i, m in enumerate(notes23)]), "",
          "## 이동 표 (v2.1 → v2.2)", "", md_table(["#", "파일", "경로", "v2.1", "v2.2"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['v2_1']}`", f"`{m['v2_2']}`") for i, m in enumerate(moves22)]), "",
          "## 이동 표 (v1.1 → v2)", "", md_table(["#", "파일", "경로", "v1.1", "v2"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['v1_1']}`", f"`{m['v2']}`") for i, m in enumerate(moves)]), "",
          "## 요약", "", md_table(["행선지", "원장 21", "step1", "합계"], [(k, sum(1 for r in colrows if r["dest"] == k and r["file"] != STEP1), sum(1 for r in colrows if r["dest"] == k and r["file"] == STEP1), v) for k, v in sorted(dest_counter.items(), key=lambda x: -x[1])] + [("합계", sum(1 for r in colrows if r["file"] != STEP1), sum(1 for r in colrows if r["file"] == STEP1), len(colrows))]), ""]
    for f in FILES + [STEP1]:
        rs = [r for r in colrows if r["file"] == f]
        md.append(f"## `{f}` — 잎 키 {len(rs)}" + (" (조사 산출물 · 22번째 브론즈 원천)" if f == STEP1 else ""))
        md.append("")
        md.append(md_table(["#", "경로", "타입", "횟수", "행선지", "표적", "비고"], [(i + 1, f"`{r['path']}`", r["type"], r["count"], r["dest"], f"`{r['target']}`", r["note"]) for i, r in enumerate(rs)]))
        md.append("")
    open(os.path.join(WORK, OUT["cmap"]), "w", encoding="utf-8").write("\n".join(md))
    return erd, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, moves, moves22, moves23, notes23


# ---------------------------------------------------------------------------
# erd-v2.3.md
# ---------------------------------------------------------------------------
def build_erd_md(erd, colrows, dicts, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, v1erd, moves, v22tup, moves22, moves23, notes23):
    o = []
    A = o.append
    v1rep = v1erd.get("resolution_report", {}) if v1erd else {}
    T = S.TUPLE_RULES
    ps, as_ = TUP["procedure"]["summary"], TUP["adverse"]["summary"]
    A("# ERD v2.3 — 피부과 시술 허브 메달리온 시맨틱 정의")
    A("")
    A("작성 2026-11-04 · 상태 **초안(사용자 승인 전)** · 브론즈 스냅샷 2026-10-26 (+ 조사 산출물 step1 10-29) · 발주서 `erd-v2.3-brief.md` · 근거 `erd-v2.2-review.md`(2차 독립 검토 ⑥ 동결 전 7건 전부 수용) · 이전 발주서(`erd-v2.2-brief.md` · `erd-v2.1-brief.md` · `erd-v2-brief.md` · `erd-v1.1-brief.md` · `erd-v1-brief.md`)의 입력·금지·기준·질문 기본값·처분 유지")
    A("")
    A(f"기계용 동본 `erd-v2.3.json` · 값 사전 `erd-v2.3-dictionaries.json`(v2.2 와 값·동의어 동일, 경과 사전 비고만 §1.5 경과 규칙) · 잎 키 행선지 `erd-v2.3-column-map.md`(v2.2 대비 이동 {len(moves23)} · 비고 변경 {len(notes23)}) · 분해 규칙 실행 `erd-v1.1-resolve.py`(§9.2, 그대로 재실행) · 튜플 실측 `erd-v2.3-tuples.py`(결과 `erd-v2.3-tuples.json`, §9.5·§9.6 v2.2 수치와 나란히 + §9.5.8 엣지 끝 분포) · 검산 `erd-v2.3-check.py` (결과 §10). 이전 판 산출물은 그대로 두었다. **v2.2 → v2.3 변경 목록(검토 번호 대응)은 §11**, 동결 후 결정 레코드로 갈 것의 자리는 §12.")
    A("")
    A("**v2.3 의 범위는 2차 독립 검토 ⑥ 「동결 전 꼭 고칠 것」 7건(발주서 번호)뿐이다.** "
      "① 시술 축 엣지의 끝 = 시술 튜플(R3·R9·R12·R15·R16·R17·R18 · 계열·하위분류·제품 노드는 참조가 그 층까지만 적혔을 때뿐 · target_depth · 실측 §9.5.8) · "
      "② 경과(course)는 사건에 바로 붙은 수식어만(§1.5 문자 그대로) · "
      "③ 부작용도 미등록 조각이 있으면 접지 않는다(raw_name 튜플 · candidate_name · 접힘은 세 칸 전부 사전 값일 때만 · §9.6 재실측) · "
      "④ 결정 kind 4종 추가(edge_create · tuple_assign_multi · adverse_tuple_assign · conflict_close → 16) · "
      "⑤ 결정 target 은 안정 키만(PRC-/ADV-/CFL- 금지) + 적용 순서 ①~⑦ 고정(§5 표) · "
      "⑥ 기법 잔재 제거(§2.7 정의 · technique_id 출처 = 이름 키 → 기법 사전) · "
      "⑦ R29 출처에 taxonomy.json safety 잎 키 11 추가. "
      "구조(개체 21 · 관계 31 · 사전 46 · 행선지 1,072)와 시술 분해 규칙(①②③)은 v2.2 그대로. 검토의 「동결 후 결정 레코드로」는 범위 밖(갈 자리만 §12). ERD 는 설계다 — 데이터는 안 고치고, 사전 값·동의어 추가는 범위 밖.")
    A("")
    A("## 1. 범위와 층")
    A("")
    A("| 층 | 무엇 | 규칙 |")
    A("|---|---|---|")
    A("| 브론즈 | 원장 21개 JSON 그대로 + `step1-products.json`(조사 산출물) | 바이트 보존·수정 금지. 파일 SHA256 이 식별자(§6 표). 원장 스냅샷 2026-10-26, step1 10-29 |")
    A("| 시맨틱 | 이 ERD + 값 사전 + 분해 규칙(참조 §1.3 · 튜플 §1.4/§1.5) | 문서. 사용자 승인이 정본 조건. 버전으로 개정(v1 → v1.1 → v2 → v2.1 → v2.2 → v2.3 → …) |")
    A("| 실버 | ERD 를 따르는 정규화 레코드 | **모든 값은 (파일, 잎 키 경로) 출처를 가진다.** 출처 없는 값 금지. 충돌은 둘 다 보관 |")
    A("| 골드 | 실버 조합 뷰 | 실버에 없는 사실을 만들지 않는다. 충돌 미판정 레코드 제외 |")
    A("")
    A("지식은 원장 21개·컬럼 리포트·스캔 결과·erd-v* 산출물과 발주서·검토서·`step1-products.json` 에서만 가져왔다. step2·step3·source-map·DATA-001·DEC-*·silver-*·`_archive/` 는 열지 않았다.")
    A("")
    A("### 1.1 정규화(「같은 것」판정)와 식별자")
    A("")
    A(f"- 정규화 `{S.NORMALIZE_RULE['name']}`: " + " → ".join(S.NORMALIZE_RULE["steps"]))
    A(f"- {S.NORMALIZE_RULE['note']}")
    A(f"- 식별자: `{S.ID_RULE['format']}`. canonical_key 는 개체별(§2 각 표의 「식별자」). {S.ID_RULE['canonical_key']}")
    A(f"- survey 제품: {S.ID_RULE['survey_products']}")
    A(f"- **튜플 식별자** — procedure(v2.2): `{S.ID_RULE['procedure']}` · reference anchor: {S.ID_RULE['reference']} · adverse_effect(v2.3): `{S.ID_RULE['adverse_effect']}` · catalog_item: {S.ID_RULE['catalog_item']} · adverse_expression: {S.ID_RULE['adverse_expression']}")
    A(f"- **접힘 조건(v2.2 · 문자 그대로): 「{S.FOLD_CONDITION}」** — {S.FOLD_RULE}.")
    A(f"- **부작용 접힘 조건(v2.3)**: {S.ADVERSE_FOLD_RULE}.")
    A(f"- **원장 locator(v2.3)**: {S.LOCATOR_RULE}.")
    A(f"- **결정 target(v2.3)**: {S.DECISION_TARGET_RULE}. 충돌: {S.ID_RULE['conflict_decision_ids']}.")
    A("- 「같은 것」 = 정규화 완전 일치(①) + 사전 동의어(②)만 자동. 참조 문자열은 §1.3 분해 규칙으로 조각내어 조각 단위로 같은 판정을 한다. 튜플은 조각이 가리키는 개체·사전 값의 조합이 같을 때 같은 것이다. 유사도·추측 매칭은 ⑦ 후보로만.")
    A("")
    A("### 1.2 다이어그램 (개체·관계만)")
    A("")
    A("```mermaid")
    A(mermaid())
    A("```")
    A("")
    A("### 1.3 참조 해결 — 결정론 분해 규칙 (v1.1 B · 그대로)")
    A("")
    R = S.RESOLVE_RULES
    A("v1.1 의 세 단계를 **데이터**(`erd-v2.3.json → resolve_rules`)로 적고 `erd-v1.1-resolve.py` 가 그대로 실행한다. v2 에서 바뀐 것은 사전 순서의 「단위 시술」 자리가 `catalog_item_name`(분류 항목 이름 색인)을 읽는다는 것, v2.1 은 `fallback_to_parent: false`, v2.2 는 3단계 미해결 사유에 「조각 둘 이상 · 못 쓰는 primary」. v2.3 은 바꾸지 않았다. 유사도·추측은 없다.")
    A("")
    A(f"1. **계열 확정** — {R['step1_family']['what']}. 자리별 힌트: " + " · ".join(f"{k}: `{v}`" for k, v in R["step1_family"]["slot_hints"].items()) + f". 코드 정규식 `{R['step1_family']['code_regex']}`")
    A(f"2. **이름 분해** — 괄호 안을 뗀다(`{R['step2_decompose']['paren_regex']}`). 조합 기호 `{'` `'.join(R['step2_decompose']['combo_symbols'])}` 로 멤버를 나눈다. 조각마다 사전 순서 **{' → '.join(R['step2_decompose']['dictionary_order'])}**(procedure = catalog_item_name) 로 완전 일치를 시도한다(계열 사전에 닿으면 kind=modality). 규격 정규식 `{R['step2_decompose']['spec_regex']}` + unit 사전. {R['step2_decompose']['secondary_rule']}. {R['step2_decompose']['scope_rule']}. {R['step2_decompose']['overlap_rule']}.")
    A(f"3. **조립** — 튜플 ({', '.join(R['step3_assemble']['tuple'])}). (a) resolved: {R['step3_assemble']['resolved']} (b) 분해 성공·항목 없음: {R['step3_assemble']['decomposed']} (c) unresolved: {R['step3_assemble']['unresolved']}")
    A(f"   - **fallback_to_parent = {R['step3_assemble']['fallback_to_parent']}** — {R['step3_assemble']['fallback_to_parent_note']}")
    A("")
    A("결과는 §9.2 에 v1 수치와 나란히(v1.1 과 같은 수치 — 사전 값이 같다). (a)·(b) 의 결과는 §1.4 의 튜플 규칙으로 한 번 더 내려가 procedure 튜플이 되고, (c) 미해결은 튜플을 만들지 않는다. v2.3: 그 튜플이 곧 엣지의 끝이다(§3 엣지 끝 규칙 · §9.5.8).")
    A("")
    A("### 1.4 시술 튜플 분해 규칙 (구조 변경 ① · v2.2 수정 1·2·3 그대로 · v2.3 엣지 끝 · 데이터 `erd-v2.3.json → tuple_rules.procedure` · `erd-v2.3-tuples.py` 실행)")
    A("")
    P = T["procedure"]
    A(f"- 입력: ① {P['input']['catalog_items']} · ② {P['input']['references']}")
    A(f"- 조각: {P['fragments']}")
    A(f"- 조합: {P['combo']}")
    A(f"- fallback_to_parent: **{P['fallback_to_parent']}** (v2.1) · technique_inheritance: **{P['technique_inheritance']}** (v2.2) · fold_condition: **{P['fold_condition']}** (v2.2)")
    A(f"- 접힘(v2.2): {P['fold_rule']}")
    A("- what(필수) — v2.2 규칙:")
    for i, w in enumerate(P["what"], 1):
        A(f"  {i}. {w}")
    A(f"- site: {P['site']}")
    A(f"- technique: {P['technique']}")
    A(f"- 수식 조각: {P['qualifiers']}")
    A(f"- extra(v2.2): {P['extra']}")
    A(f"- 식별자: `{P['id']}` · 상태: {P['status']}")
    A(f"- **코드 참조(v2.3)**: {P['code_references']}")
    A(f"- **엣지 끝(v2.3)**: {P['edge_end']}")
    A("")
    A("### 1.5 부작용 튜플 분해 규칙 (구조 변경 ② · v2.3 수정 2·3 · 데이터 `erd-v2.3.json → tuple_rules.adverse`)")
    A("")
    Q = T["adverse"]
    A(f"- 입력: {Q['input']['complications']} · 표현: {Q['input']['phrases']}")
    A(f"- 분해: {Q['split']}")
    A(f"- 튜플: {Q['tuple']}")
    A(f"- **경과(course) 규칙(v2.3 · §2.14 · §4 와 같은 문장)**: {Q['course']}")
    A(f"- **접힘 조건(v2.3)**: {Q['fold_rule']}")
    A(f"- **raw_name 튜플(v2.3)**: {Q['raw_name']}")
    A(f"- **표현(v2.3)**: {Q['expressions']}")
    A(f"- 원장 locator: {Q['locator']}")
    A(f"- 타임라인 normal: {Q['normal_phrases']}")
    A(f"- 문헌: {Q['literature']}")
    A(f"- 식별자: `{Q['id']}` · 상태: {Q['status']}")
    A("")
    A("## 2. 개체 목록")
    A("")
    A(f"개체 {len(S.ENTITIES)}개 — v2·v2.1·v2.2 와 같다. 발주서 최소 목록 11 + 추가 {sum(1 for e in S.ENTITIES if e.get('beyond_minimum'))}(표시 ★). v2.3 에서 바뀐 것: `technique`(정의 — 수정 6) · `procedure`(technique_id 출처·규칙 — 수정 6 · 정의에 엣지 끝) · `adverse_effect`(정의·식별자·event_kind·anchor·all_dict_values·candidate_name·event_fragments·extra_* — 수정 2·3) · `adverse_expression`(match_status partial · 식별자 = locator) · `conflict`(stable_key · close_verdict — 수정 5) · `decision`(kind 16 · target 안정 키 — 수정 4·5). 그 밖 15 개체는 v2.2 그대로.")
    A("")
    for e in S.ENTITIES:
        star = " ★" if e.get("beyond_minimum") else ""
        A(f"### 2.{S.ENTITIES.index(e)+1} `{e['key']}` — {e['label']}{star} (접두 `{e['prefix']}`)")
        A("")
        A(f"- 정의: {e['definition']}")
        A(f"- 식별자(canonical_key): {e['identity']}")
        A(f"- aliases: {e['aliases']}")
        A("")
        A(md_table(["속성", "타입", "필수", "출처 원장 키", "정규화·규칙"], [(a[0], a[1], "○" if a[2] else "", "<br>".join(f"`{s}`" for s in a[3]) if a[3] else "(파생/ERD 정의)", a[4]) for a in e["attrs"]]))
        A("")
    A("## 3. 관계 목록")
    A("")
    A(f"관계 {len(S.RELATIONS)}개 — v2·v2.1·v2.2 와 같다(v1.1 25 + R26~R31). v2.3 에서 바뀐 것: R3·R9·R12·R15·R16·R17·R18 의 끝 규칙·target_depth·via_catalog_item(수정 1) · R29 출처 +11·match_status(수정 7·3) · R30 비고(edge_create) · R23·R24 비고(안정 키). "
      "`proc_axis` = procedure(기본) | modality | modality_subcategory | product — **v2.3 엣지 끝 규칙**: " + S.EDGE_END_RULE + " 시너지·순서·간격·시술간 금기는 **R18 하나**의 `kind` 속성.")
    A("")
    for r in S.RELATIONS:
        A(f"### {r['id']} `{r['name']}` — {r['from']} → {r['to']} ({r['card']})")
        A("")
        if r["attrs"]:
            A(md_table(["엣지 속성", "타입", "비고"], [(a[0], a[1], a[2]) for a in r["attrs"]]))
            A("")
        A("- 출처: " + (", ".join(f"`{s}`" for s in r["sources"]) if r["sources"] else "(ERD 정의 · 실버 빌더 생성)"))
        if r["note"]:
            A(f"- 규칙: {r['note']}")
        A("")
    A("### 3.1 ERD 정의 열거형 (원장 출처 없음 — 값 사전과 구분)")
    A("")
    A(md_table(["열거형", "값"], [(k, ", ".join(v)) for k, v in S.ERD_ENUMS.items()]))
    A("")
    A("## 4. 값 사전 목록")
    A("")
    nval = sum(1 for d in dicts.values() if getattr(d, "kind", "value") == "value")
    nidx = sum(1 for d in dicts.values() if getattr(d, "kind", "value") != "value")
    A(f"전부 `erd-v2.3-dictionaries.json` — **v2.2 와 값·동의어·순서 동일**(v2.3 은 사전을 바꾸지 않는다), 경과 사전(course)의 비고만 §1.5 경과 규칙 문장(v2.3 · 세 곳 동일). 값 사전 {nval} + 개체 이름 색인 {nidx}(B 분해 규칙이 읽는 제품명·하위분류 라벨·분류 항목 이름) = {len(dicts)}. 부위 사전 21 · 기법 사전 12 유지(공유 사전).")
    A("")
    A(md_table(["사전", "종류", "라벨", "정준값", "동의어", "후보", "출처 키"], [(d.name, getattr(d, "kind", "value"), d.label, len(d.entries), sum(len(e["synonyms"]) for e in d.entries.values()), len(d.candidates), ", ".join(sorted({f"`{s['file']}:{s['path']}`" for e in d.entries.values() for s in e["sources"]} | {f"`{s['file']}:{s['path']}`" for e in d.entries.values() for sy in e["synonyms"] for s in sy["sources"]})[:6]) + (" …" if len({(s['file'], s['path']) for e in d.entries.values() for s in e["sources"]}) > 6 else "")) for d in dicts.values()]))
    A("")
    A("사전 하나에 비고가 있는 것:")
    A("")
    for d in dicts.values():
        if d.note:
            A(f"- `{d.name}`: {d.note}")
    A("")
    A("### 4.1 사건 사전(adverse_event_type) 전체 — 값 · 분류 · 동의어 · 출처 횟수")
    A("")
    de = dicts["adverse_event_type"]
    A(md_table(["#", "사건", "category", "동의어(표기 변형)", "65 이름 중 출현", "분류 확인 필요"], [(i + 1, e["canonical"], e["category"], ", ".join(s["value"] for s in e["synonyms"]) or "—", e["sources"][0]["n"], "○" if e.get("category_review") else "") for i, e in enumerate(de.entries.values())]))
    A("")
    A("분류 「확인 필요」 표시는 ERD 가 배정했지만 경계가 애매한 값(화상·수포·경결·비대칭·두통). 사용자가 다른 category 로 옮기면 사전 데이터만 바꾸면 된다.")
    A("")
    A("### 4.2 경과 사전(course) · 상대 부위 사전(relative_site)")
    A("")
    A(f"- **경과 규칙(v2.3 · §1.5 · §2.14 와 같은 문장)**: {dicts['course'].note}")
    A("- `course`: " + " · ".join(f"{e['canonical']}(동의어: {', '.join(s['value'] + '[' + s['sources'][0]['path'].split('.')[-1] + ']' for s in e['synonyms']) or '—'} · 출처 {e['sources'][0]['file']}:{e['sources'][0]['path']})" for e in dicts["course"].entries.values()))
    A("- `relative_site`: " + " · ".join(f"{e['canonical']}(동의어: {', '.join(s['value'] for s in e['synonyms']) or '—'})" for e in dicts["relative_site"].entries.values()))
    A("")
    A("## 5. 충돌·결정 개체 정의 + 규칙 ①~⑩ + 신뢰 순위 + 결정 적용 순서")
    A("")
    A("충돌(`conflict`)·결정(`decision`) 개체 정의는 §2. 결정 레코드는 §5.2 의 모양으로 `erd-v2.3.json → decisions` 에 적재한다 — v2.2 의 23 을 그대로 이관(처분 19 approved · DEC-20~23 proposed) + v2.3 개정 DEC-24(proposed). 이관 표 §5.3. **v2.3: 결정 target 은 안정 키만, 적용 순서는 §5.4 표.**")
    A("")
    A(md_table(["#", "분류", "규칙"], S.QUALITY_RULES))
    A("")
    A("빈값과 「없음」: 안 적힌 것(키 없음·null·빈 배열·빈 문자열) = null(미입력). 명시적으로 없다고 적힌 것만 빈 목록. step1 의 「확인 불가」·「근거 없음」·「해당 없음」은 값이다(null 아님). "
      "**시술 튜플의 site none·technique none 은 미상이며 식별자 값이 아니다(v2.2 · 검토 1-A)** — 미상 칸이 있으면 식별자에 anchor(CAT-/REF-)를 섞어 항목·참조마다 고유하고 접히지 않는다(접힘 조건 「" + S.FOLD_CONDITION + "」). "
      "**부작용 튜플(v2.3 · 검토 2-B)**: 미등록 조각이 있는 complications 이름은 raw_name 튜플(anchor=원장 locator)로 접히지 않고, 접힘은 세 칸 전부 사전 값일 때만 — 부작용의 site none·course 미상은 v2 그대로 축의 정의값(식별자에 들어간다 — 검토 2-D 는 동결 후 scope_review · §12). "
      "단계 끝 = 컬럼 행선지 미정 0 · 충돌 미판정(open) 0 — auto_resolved_by_trust 는 판정된 것(④)이지만 레코드로 남고, v2.3 은 값을 고르지 않는 판정(conflict_close)으로도 open 을 닫을 수 있다.")
    A("")
    A("**규칙 ④ (v2.2 · 사용자 결정으로 유지 + 기록)**: " + S.RULE4 + ".")
    A("")
    A("### 5.1 원장 신뢰 순위 (파일별 · 21 + step1) — v1.1 그대로")
    A("")
    A(md_table(["순위", "파일", "종류", "근거 키", "표시", "비고"], [(t, f"`{f}`", S.SOURCE_KIND[f], b, S.TRUST_FLAGS.get(f, ""), n) for f, t, b, n in sorted(S.SOURCE_FILES, key=lambda x: (x[1], x[0]))]))
    A("")
    s1 = next(fm for fm in erd["source_files"] if fm["file"] == STEP1)
    A(f"`products.json` 의 `products[].mfds` 필드만 2(식약처 허가)로 격상한다. `complications.json` 은 8-1 처분으로 3 유지 + 「AI 컨센서스 추정」 — v2 의 사건 사전 뼈대가 이 파일이므로 사건 값에도 같은 표시가 따라간다. `step1-products.json` 은 조사 산출물: 허가 건 `licenses[].source` 가 `{S.STEP1_TIER2_SOURCE_RE}` 에 맞는 {s1['trust_tier_rule']['tier2_licenses']}/{s1['trust_tier_rule']['licenses_total']} 건의 허가·회사·공식명 필드만 2, 그 밖은 3.")
    A("")
    A("### 5.2 결정 kind — 빌드가 읽는 모양 (v2.2 검토 3-B · v2.3 수정 4·5)")
    A("")
    A(f"공통 필드: {' · '.join(S.DECISION_COMMON_FIELDS)}. status ∈ {{{', '.join(S.DECISION_STATUS)}}}. **{S.DECISION_BUILD_RULE}.** target·new_value 는 문자열이 아니라 kind 별 구조체다. kind {len(S.DECISION_KINDS)} = v2.2 12 + v2.3 신설 4(" + " · ".join(f"`{k}`" for k in S.DECISION_KINDS_NEW_V23) + "). v2.3 에서 모양이 바뀐 kind: " + " · ".join(f"`{k}`({v})" for k, v in S.DECISION_KINDS_RESHAPED_V23.items()) + ".")
    A("")
    A(f"**target 규칙(v2.3 · 검토 3-B)**: {S.DECISION_TARGET_RULE}.")
    A("")
    A(md_table(["kind", "v2.2 신설", "v2.3 신설·개형", "빌드 적용", "적용 단계", "target", "new_value", "비고"],
               [(f"`{k}`", "○" if k in S.DECISION_KINDS_NEW else "", "신설" if k in S.DECISION_KINDS_NEW_V23 else ("개형" if k in S.DECISION_KINDS_RESHAPED_V23 else ""), "○" if br else "기록만",
                 next((st for st, ks, _ in S.DECISION_APPLY_ORDER if k in ks), "⓪" if k == "reclassification" else "—"), t, nv, n) for k, br, t, nv, n in S.DECISION_KINDS]))
    A("")
    A("### 5.3 결정 레코드 — v2.2 의 23 이관 + v2.3 1 (전부)")
    A("")
    A(md_table(["id", "kind", "target", "new_value", "decided_by", "decided_at", "status", "source_refs"],
               [(d["id"], d["kind"], json.dumps(d["target"], ensure_ascii=False)[:200], json.dumps(d["new_value"], ensure_ascii=False)[:160], d["decided_by"] or "null", d["decided_at"] or "null", d["status"], " · ".join(x["ref"] for x in d["source_refs"])) for d in erd["decisions"]]))
    A("")
    A(f"이관(v2.2 → v2.3): 23 레코드 전부 모양·값 그대로(target 은 ERD 절·항목 번호라 안정 키 규칙에 맞는다 — 파생 id 포함 {sum(1 for m in erd['decisions_migration'] if m['derived_id_in_target'])} · 검산 K-2). DEC-24 는 v2.3 개정 기록(proposed) — ERD 승인 때 decided_by=사용자 · decided_at=승인일 · approved.")
    A("")
    A("원장 메모(질문 23 · §9.4)는 실버 빌드가 결정 레코드로 적재한다 — verification_needed → `verification_hold` · classification_issue/correction_note → `ledger_correction_note` · canonical_category → `canonical_mapping`(target.from_ref=CAT-id, target.scope=[그 CAT-id], new_value.to_id=SUB-id, 하위분류 사전 일치만) · reclassified_to → `reclassification`(적용 ⓪). 원문은 reason, decided_by=`원장 작성자(taxonomy.json)`, status=approved, decided_at=null.")
    A("")
    A("### 5.4 결정 적용 순서 (v2.3 · 검토 3-B)")
    A("")
    A(S.DECISION_APPLY_ORDER_RULE + ".")
    A("")
    A(md_table(["단계", "kind", "왜 이 자리인가"], [(st, " / ".join(f"`{k}`" for k in ks), why) for st, ks, why in S.DECISION_APPLY_ORDER]))
    A("")
    A("## 6. 원장 파일 21 + step1 → 개체 매핑 요약")
    A("")
    rows = []
    for fm in erd["source_files"]:
        f = fm["file"]
        rs = [r for r in colrows if r["file"] == f]
        ents = Counter(r["target"].split(".")[0] for r in rs if r["dest"] == "개체" and not r["target"].startswith("source_file"))
        rels = Counter(r["target"].split(".")[0].split("(")[0] for r in rs if r["dest"] == "엣지")
        dcts = Counter(r["target"] for r in rs if r["dest"] == "사전")
        drops = [r["path"] for r in rs if r["dest"] in ("버림", "브론즈")]
        main = ", ".join(f"{k}({v})" for k, v in ents.most_common(3))
        sub = ", ".join(f"{k}({v})" for k, v in ents.most_common()[3:]) + ("; " if ents.most_common()[3:] and rels else "") + ", ".join(f"{k}({v})" for k, v in rels.most_common())
        rows.append((f"`{f}`", fm["trust_tier"], fm["sha256"][:12], fm["leaf_paths"], main or "—", sub or "—", ", ".join(k.replace("dict:", "") for k in dcts) or "—", f"{len(drops)}: " + ", ".join(f"`{d}`" for d in drops[:3]) + (" …" if len(drops) > 3 else "") if drops else "0"))
    A(md_table(["파일", "순위", "sha256(12)", "잎", "주 개체", "부 개체·엣지", "사전", "브론즈만/버림"], rows))
    A("")
    A(f"`step1-products.json` 전체 SHA256 `{s1['sha256']}` · {s1['bytes']} bytes · 항목 {s1['items']} · 잎 키 {s1['leaf_paths']}. 브론즈만 {sum(1 for r in colrows if r['file'] == STEP1 and r['dest'] == '브론즈')} 은 설계·식별자·작업 상태·집계·파생 복사본(v1.1 §C 규칙).")
    A("")
    A("### 6.1 옮긴 키 (v1.1 → v2 이동 표)")
    A("")
    A(md_table(["#", "파일", "경로", "v1.1", "v2"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['v1_1']}`", f"`{m['v2']}`") for i, m in enumerate(moves)]))
    A("")
    A("## 7. 질문 25 답 — v1.1 그대로")
    A("")
    A(md_table(["#", "답 (발주서 §6 기본값 적용 · v1.1 개정분 7·8·10·11·14·16·24 유지)"], S.Q25))
    A("")
    A("v2 에서 답이 바뀐 질문은 없다. 질문 10·11 의 「단위 시술 개체」는 v2 에서 분류 항목(catalog_item)을 뜻하고, 그 위에 튜플(procedure)이 §1.4 로 얹힌다. v2.3: 질문 5(pih procedure_ref 가장 구체 수준)·7(코드+라벨)의 끝은 §3 엣지 끝 규칙대로 — 항목 id 면 그 항목의 튜플, 하위분류 id 면 subcategory, M 코드면 modality.")
    A("")
    A("## 8. 기본값 재검토 — 처분 결과 (v1.1 그대로)")
    A("")
    A("v1 §8 의 19 건 처분은 v1.1 에서 확정됐고 v2 이후 바꾸지 않는다. 각 건은 결정 레코드(`erd-v2.3.json → decisions` · §5.3, status approved)로 남는다.")
    A("")
    A(md_table(["#", "항목", "처분 주체", "처분(확정)", "반영 위치"], [(f"8-{no}", B.REVIEW[no - 1]["title"], who, what, where) for no, (who, what, where) in S.DISPOSITIONS.items()]))
    A("")
    A("### 8-2 표 — v1 부위 사전 「(확장)」 51 의 처분 (v1.1 그대로)")
    A("")
    A(md_table(["값", "cc_group 횟수", "재배치", "사유"], [(r["value"], r["cc_group_n"], r["dest"], r["reason"]) for r in SITE_TABLE]))
    A("")
    kept = [r for r in SITE_TABLE if r["dest"].startswith("부위")]
    A(f"부위 사전 유지 {len(kept)} · problem_subcategory_label 로 {len(SITE_TABLE) - len(kept)}. 부위 사전 최종 = 뼈대 11 + taxonomy 부위 라벨 {len(kept)} = **{len(dicts['site'].entries)}** (확장 0) — v2 의 공유 부위 사전.")
    A("")
    A("## 9. ERD 승인 때 사용자가 볼 것")
    A("")
    A("### 9.1 사전 표 (정준값 수 · 동의어 · 후보)")
    A("")
    A(md_table(["사전", "정준값", "동의어", "후보(미연결)"], [(d.name, len(d.entries), sum(len(e["synonyms"]) for e in d.entries.values()), "; ".join(c["value"] for c in d.candidates) or "—") for d in dicts.values()]))
    A("")
    A("핵심 사전 정준값 전체:")
    A("")
    for name in ["modality", "problem", "site", "technique", "course", "relative_site", "license_status", "license_kind", "license_state"]:
        d = dicts[name]
        A(f"- `{name}` ({len(d.entries)}): " + " · ".join((e["canonical"] + (f"[{e['code']}]" if e.get("code") else "") + (f"({e['site_kind']})" if e.get("site_kind") == "taxonomy_site_label" else "")) for e in d.entries.values()))
    A(f"- `adverse_event_type` ({len(dicts['adverse_event_type'].entries)}): " + " · ".join(e["canonical"] + f"[{e['category']}]" for e in dicts["adverse_event_type"].entries.values()))
    A(f"- `problem_subcategory_label` ({len(dicts['problem_subcategory_label'].entries)}): " + " · ".join(e["canonical"] + f"[{e['code']}]" + ("(부위)" if e.get("is_site") else "") for e in dicts["problem_subcategory_label"].entries.values()))
    A("")
    A("### 9.2 격리 목록 — 참조 해결, v1 vs v1.1 규칙 (v2.3 재실행 · 같은 수치)")
    A("")
    A("v1 = 완전 일치만. v1.1 규칙(§1.3)을 v2.3 사전(분해에 쓰는 값은 v2 와 같다)으로 `erd-v1.1-resolve.py` 를 다시 돌린 수치 — v1.1·v2·v2.1·v2.2 와 같다. 「분해 성공·항목 없음」은 조각이 전부 사전에 닿았지만 taxonomy 항목 하나로 떨어지지 않은 참조. 미해결은 사전에 없는 조각이 하나라도 있는 참조. 해결·분해 성공만 §1.4 로 procedure 튜플이 되고(그 튜플이 엣지의 끝 · §9.5.8), v2.2 부터 그중 조각이 둘 이상(primary·site·technique)인 것도 튜플 단계에서 미해결로 보낸다. 고민 자리·pih id 자리는 v1 규칙 그대로.")
    A("")
    A(RESOLVE.side_by_side(RES, v1rep))
    A("")
    A(f"합계(부위 사전·step1 제외): 미해결 참조(⑨) v1 **{TOTAL.get('unresolved_v1')}** → v1.1/v2 **{TOTAL['unresolved_v1_1']}** · 분해 성공·항목 없음 **{TOTAL['decomposed_v1_1']}** · 해결 **{TOTAL['resolved_v1_1']}**.")
    A("")
    A("미해결 사유 상위 조각(전 자리 합산, 사전에 없는 조각): " + " · ".join(f"`{f}`×{n}" for f, n in TOTAL["top_untouched_fragments"][:40]))
    A("")
    for k, v in RES.items():
        if v["unresolved_labels"] and not k.startswith("step1"):
            A(f"- **{k}** 미해결 {v['unresolved']}: " + " · ".join(f"`{l}`" + (f"@{h}" if h else "") + "(" + ",".join(u) + ")" for l, h, u, _ in v["unresolved_labels"]))
        if v["decomposed_labels"] and not k.startswith("step1"):
            A(f"- **{k}** 분해 성공·항목 없음 {v['decomposed']}: " + " · ".join(f"`{l}`" + (f"@{h}" if h else "") + f"[{sh}]" for l, h, sh, _ in v["decomposed_labels"]))
    A("")
    st = RES["step1-products.items[] display/ledger/search 이름 → 원장 제품 (395)"]
    shp = Counter(r.get("shape") for r in st["rows"] if r["status"] == "decomposed")
    A(f"step1 395 → 원장 제품 대응(B 규칙만): 대응 {st['resolved']} (원장 제품 59 중 {st['ledger_products_covered']}종, 이름 역할 {st['matched_by']}) · 분해 성공·항목 없음 {st['decomposed']} ({', '.join(f'{k}={v}' for k, v in shp.items())}) · 미해결 {st['unresolved']} → **origin=survey {st['survey_products']}** (그중 step1 active=false {st['inactive_items']}). `non_product_depth:procedure` 는 이름이 제품 목록 59 가 아니라 taxonomy 분류 항목(521)과 통째 일치한 것 — v2 에서는 catalog_item 에 닿은 것이며 제품 개체로는 survey 이고 R3(uses_product) 후보로 기록한다.")
    A("")
    A("질문 14 두 묶음(modality_ref 빈 26 항목 · 8-5 처분 반영, 미배정 0) — v1.1 그대로:")
    A("")
    A(md_table(["고민", "하위분류", "항목", "묶음", "발주서 목록 일치", "범위"], [(r["problem"], r["subcategory"], r["name"], r["bucket"], ", ".join(r["matched"]) or "—", r["scope"]) for r in Q14]))
    A("")
    A("### 9.3 충돌 예상 수 (v1.1 그대로 재계산 · v2.2 rule_ref 열 · v2.3 닫는 kind 열)")
    A("")
    A(md_table(["종류", "rule_ref", "무엇", "건", "닫는 결정 kind(v2.3)"], [(c["kind"], c["rule_ref"], c["what"], c["n"], c["close_kind"]) for c in CONF]))
    A("")
    A("v2.2 규칙 ④: 이 표는 원장 파일 단위 예상(순위가 같은 출처끼리의 ⑥ 와 ⑦⑧⑨)이다. 순위가 다른 출처끼리의 값 충돌은 실버 빌드가 레코드마다 ④ 로 자동 채택하면서 **그때마다** conflict(status=auto_resolved_by_trust · chosen_value · values[].trust_tier · rule_ref=④ · stable_key)를 남긴다 — 건수는 빌드 산출물에서 센다(이 표에 미리 세지 않는다). v2.3: 모든 conflict 는 stable_key(kind + 출처 locator 쌍)를 가지며 결정은 그 키로만 가리킨다. step1 6_companies.conflicts 12 는 허가 값(trust 2 조건부)과 다른 출처 값의 쌍이라 빌드 때 레코드별 trust_tier 로 ④/⑥ 이 갈린다.")
    A("")
    for c in CONF:
        if c["detail"] and isinstance(c["detail"], list):
            A(f"- {c['what']}: " + "; ".join(str(x) for x in c["detail"]))
    A("")
    A(f"합계: value_conflict {sum(c['n'] for c in CONF if c['kind']=='value_conflict')} · duplicate_candidate {sum(c['n'] for c in CONF if c['kind']=='duplicate_candidate')} · unregistered_value {sum(c['n'] for c in CONF if c['kind']=='unregistered_value')} · unresolved_reference {TOTAL['unresolved_v1_1']}(+ step1 모호 {sum(c['n'] for c in CONF if c['kind']=='unresolved_reference')}). 전부 사람 판정 전 `open`. v2 에서 「complications 합병증 표기 변형 6」은 사건 사전 동의어로 접히므로(§9.6.2) ⑦ 후보가 아니라 ② 동의어 병합이 된다 — 표의 수는 v1.1 그대로 두고 §12 에 적는다.")
    A("")
    A("### 9.4 결정 개체로 미리 적재될 원장 메모 (질문 23) — v1 과 같음")
    A("")
    tx = L["taxonomy.json"]
    rows = []
    for m in tx["modality"]:
        for sc in m["subcategories"]:
            for it in sc["items"]:
                for k in ["classification_issue", "reclassified_to", "correction_note", "verification_needed", "canonical_category"]:
                    if k in it:
                        rows.append((m["id"], it["id"], it["name"], k, str(it[k])[:70] + ("…" if len(str(it[k])) > 70 else "")))
    A(md_table(["계열", "항목 id", "항목", "키", "값"], rows))
    A("")
    A("### 9.5 시술 튜플 실측 (v2.3 · `erd-v2.3-tuples.py` 실제 실행 · v2.2 수치와 나란히 · 숫자는 목표가 아니다)")
    A("")
    A("규칙은 §1.4(v2.2 그대로 + v2.3 코드 참조·엣지 끝). 분류 항목은 **자기 이름을 색인에서 제외**하고 분해했다(자기 참조 금지). 접힘 조건은 「" + S.FOLD_CONDITION + "」 — 접힌 표(9.5.2)에는 그것만 남는다. technique 는 이름 조각이 기법 사전에 닿은 것뿐이다(fragment " + str(ps["tuples_technique_origin"].get("fragment", 0)) + " / 튜플 " + str(ps["tuples_total"]) + ") — 미상 칸이 있는 튜플은 식별자에 anchor 가 들어가 접히지 않는다(세 칸 전부 사전 값 튜플 " + str(ps["tuples_all_dict_values"]) + "). v2.3: M 코드·하위분류 id 만 적힌 참조 " + str(ps["code_references_node"]) + " 건은 튜플이 아니라 노드 끝(§9.5.4 `node` · §9.5.8). 이 수는 규칙대로의 결과이며 목표가 아니다. v2.2 열은 `erd-v2.2-tuples.json` 의 수치.")
    A("")
    A(TUPLES.procedure_md(TUP, (v22tup or {}).get("procedure", {}).get("summary")))
    A("")
    A("### 9.6 부작용 튜플 실측 (구조 변경 ② · v2.3 수정 2·3 · `erd-v2.3-tuples.py` 실행 · v2.2 수치와 나란히)")
    A("")
    A("규칙은 §1.5(v2.3): 경과는 사건에 바로 붙은 수식어만(멤버 안) · 미등록 조각이 있는 complications 이름은 raw_name 튜플(이름마다 고유 · anchor=원장 locator) · 접힘은 세 칸 전부 사전 값일 때만 · 표현은 raw_name 을 만들지 않고 match_status 로 구분. 사건 사전 뼈대는 complications 65 이름의 분해 조각(§4.1 · 값 불변). 접힌 표(9.6.2)는 65 이름이 어느 튜플로 갔는지 **전부** 보인다. 검토 2-C(사건 동의어)·2-D(none·미상 식별자)는 동결 후 결정(§12).")
    A("")
    A(TUPLES.adverse_md(TUP, (v22tup or {}).get("adverse", {}).get("summary")))
    A("")
    A("## 10. 검산 결과")
    A("")
    A("`erd-v2.3-check.py` 를 독립 실행한 출력을 그대로 붙였다(같은 폴더에서 `python3 erd-v2.3-check.py`). v2.2 검산 항목 전부(A 잎 키 행선지 · B 사전 값 출처 · C ERD 출처 키·표적 · D 브론즈 sha256 · E 분해 규칙 재현 · F 처분 반영 · G 튜플 실측 재현 · H 구조 · I v2.1 접힘 규칙 · J v2.2 수정 6건 — v2.3 에서 바뀐 기대값은 항목 안에 적었다) + K v2.3(엣지 끝 분포 실측 존재 · 파생 id 를 target 으로 쓰는 결정 0 · 적용 순서 표 존재 · 결정 kind 16(12+4) · 부작용 미등록 포함 접힘 0 · course 규칙 문장 · 기법 잔재 표현 0 · R29 출처 11 키).")
    A("")
    return "\n".join(o)


def change_log(erd, dicts, TUP, colrows, v22erd, v22tup, moves23, notes23):
    o = []
    A = o.append
    ps, as_ = TUP["procedure"]["summary"], TUP["adverse"]["summary"]
    v = (v22tup or {}).get("procedure", {}).get("summary", {})
    va = (v22tup or {}).get("adverse", {}).get("summary", {})
    ee = erd["edge_ends"]
    A("## 11. v2.2 → v2.3 변경 목록 (검토 번호 대응 · 발주서 7건)")
    A("")
    A("| 발주 # | 검토 | 무엇 | v2.2 | v2.3 |")
    A("|---|---|---|---|---|")
    A(f"| 1 | 1-A | 시술 축 엣지의 끝 (§3 머리 · R3·R9·R12·R15·R16·R17·R18 규칙·target_depth·via_catalog_item · §1.4 · 다이어그램) | 「분류 항목에 닿으면 catalog_item, complete 면 procedure 로 승격」 — 통째로 일치하는 참조의 끝은 그 깊이의 노드(PRD-/MOD-) · M 코드 끝은 튜플 입력 밖 | **참조가 튜플로 해결됐으면 procedure 튜플 id 가 끝**(anchor 튜플도) · modality/subcategory/product 노드는 참조가 그 층까지만 적혔을 때뿐(target_depth) · catalog_item 은 끝이 아니다(항목 전부 튜플) · M 코드·하위분류 id 만인 참조는 튜플을 만들지 않고 노드 끝(`node` {ps['code_references_node']}) · R3 from = procedure · enum target_depth = {', '.join(erd['enums']['target_depth'])} |")
    A(f"| 1 | 1-A 실측 | §9.5.8 엣지 자리별 끝 분포 | 없음 | 텍스트 자리 {ee['slots']['text']} + 코드·레코드 자리 {ee['slots']['code']} (관계 {', '.join(ee['slots']['relations'])}) · 건 {ee['total_n']}: {', '.join(f'{k}={n}' for k, n in ee['total'].items())} |")
    A(f"| 2 | 2-A | 경과(course) 출처 (§1.5 · §2.14 · §4 같은 문장) | 멤버 → 같은 묶음 → outer → 이름 전체 유일값 순으로 상속(LOP → 통증×지연 하나) | **사건에 바로 붙은 수식어(같은 멤버)만.** 이름 안에 사건이 둘 이상이면 수식어가 붙은 사건에만 경과, 나머지 미상 — 「통증·불편감 및 지연성 통증(LOP)」→ (통증, 미상) + (통증, 지연) 둘(§9.6.2a · 이름 자체는 미등록 조각 때문에 raw_name). site 는 v2 그대로 |")
    A(f"| 3 | 2-B | 부작용 접힘 조건 (§1.1 · §1.5 · §2.14 · §2.15) | 미등록 조각이 있어도 세 축이 사전 값이면 접힘(§9.6.6 12 튜플) | **미등록 조각이 있는 이름은 접지 않는다** — raw_name 튜플(event_kind · anchor=원장 locator · candidate_name · event_fragments·extra_* 실값) · 접힘은 세 칸 전부 사전 값일 때만 · 표현은 raw_name 없이 R29 match_status=partial |")
    A(f"| 3 | 2-B 실측 | §9.6 | 65 → {va.get('complications_distinct_tuples')} · 접힌 튜플 {va.get('complications_tuples_with_2plus_names')} (미등록 섞임 {va.get('folded_with_partial_name')}) · 튜플 {va.get('tuples_total')} | 65 → **{as_['complications_distinct_tuples']}**(사전 {as_['complications_distinct_tuples_dict']} + raw_name {as_['complications_distinct_tuples_raw']}) · 접힌 튜플 {as_['complications_tuples_with_2plus_names']} (미등록 섞임 **{as_['folded_with_partial_name']}**) · 튜플 {as_['tuples_total']}(사전 {as_['tuples_dict']} + raw {as_['tuples_raw_name']}) · 표현 linked {as_['expressions_total']['linked']}/{as_['expressions_total']['n']} 중 partial {as_['expressions_total']['match_status'].get('partial', 0)} |")
    A(f"| 4 | 3-A | 결정 kind (§2.21 · §5.2) | 12 | **16** — 신설 `edge_create`(relation · from_ref · to_ref · attrs) · `tuple_assign_multi`(catalog_item/ref → tuples[]) · `adverse_tuple_assign`(locator raw_name/expression → tuples[](event_id, site_id, course_id)) · `conflict_close`(conflict_key → verdict not_same/both_valid/needs_source · note). R30 은 edge_create 로만 값이 생긴다 |")
    A("| 5 | 3-B | 결정 target 안정 키 + 적용 순서 (§1.1 · §2.20 · §2.21 · §5.2 · §5.4) | fold_approve.target=procedure_ids(PRC-) · conflict_override.target=conflict_id(CFL-) · exclude.target=아무 id · canonical_mapping.scope str · 적용 순서 없음 | **target 은 CAT-/REF-/원장 locator/고정 id/사전 값/conflict.stable_key 만, PRC-/ADV-/CFL- 금지**(검산 K-2) · fold_approve → anchors/keep_anchor · conflict_override/close → conflict_key · exclude → (kind, key) · canonical_mapping.scope → anchor 목록 · conflict.stable_key(kind + 출처 locator 쌍) · **적용 순서 ① dictionary_add ② canonical_mapping ③ tuple_assign/_multi/adverse_tuple_assign ④ fold_approve/event_split ⑤ edge_create ⑥ conflict_override/conflict_close ⑦ exclude**(같은 단계는 decided_at 순 · §5.4 표) |")
    A("| 6 | 1-B | 기법 잔재 (§2.7 정의 · §2.5 technique_id 출처) | §2.7 「R5 의 계열 기법을 상속하되…」 · technique_id 출처 procedure-profiles mechanism[] | §2.7 정의에서 그 문장 삭제(계열 기본값을 붙이지 않는다 · canonical_mapping approved 때만) · technique_id 출처 = 이름·참조 자리 키(what_id 와 같다) — 사전은 §4 technique · 본문(§1~§9·§12)에 「상속」 표현 0(검산 K-7 · §10 검산 출력·§11 변경 목록의 인용만 남는다) |")
    A(f"| 7 | 3-C | R29 출처 (§3 R29) | 11 키(literature 2 · consent 1 · timeline 4 · extracted 4) | **+ taxonomy.json safety 잎 키 11**(계열 3 · 항목 5 · 제품 3) = {len(next(r for r in erd['relations'] if r['id']=='R29')['sources'])} — §9.6.3 연결 1,405 건의 출처 · R29 속성 match_status |")
    A(f"| — | — | 결정 레코드 | 23 | 23 이관(그대로) + DEC-24(v2.3 개정 · proposed) = {len(erd['decisions'])} |")
    A(f"| — | — | 행선지(column-map) | — | 이동 {len(moves23)} · 비고 변경 {len(notes23)}(시술 축 참조 자리 16 + pih procedure_ref + timeline category + taxonomy safety 11 + complications name) |")
    A(f"| — | — | 규칙 데이터 | tuple_rules.name tuples_v2_2 · resolve_rules.name decompose_v2_2 | tuples_v2_3 · decompose_v2_3 · json edge_end_rule · edge_end_kinds · proc_axis_edges · adverse_fold_rule · locator_rule · decision_target_rule · decision_apply_order · tuple_rules.procedure.edge_end/code_references · tuple_rules.adverse.fold_rule/raw_name/expressions/locator · id_rule.adverse_effect/locator/decision_target · enums event_kind·close_verdict·edge_end_kind·apply_order |")
    A(f"| — | — | 실측 ① | 521 → {v.get('catalog_distinct_tuples')} · what {', '.join(f'{k}={n}' for k, n in v.get('catalog_by_what_kind', {}).items())} | **그대로** 521 → {ps['catalog_distinct_tuples']} · what {', '.join(f'{k}={n}' for k, n in ps['catalog_by_what_kind'].items())} · 상태 {', '.join(f'{k}={n}' for k, n in ps['catalog_status'].items())} |")
    A(f"| — | — | 실측 ②③ | ② 튜플 {v.get('reference_total', {}).get('tuple')} + combo {v.get('reference_total', {}).get('combo_ref')} + 미해결 {v.get('reference_total', {}).get('unresolved')} · ③ 튜플 {v.get('market_pricing', {}).get('tuple')} + 미해결 {v.get('market_pricing', {}).get('unresolved')} | ② 튜플 {ps['reference_total']['tuple']} + combo {ps['reference_total']['combo_ref']} + node {ps['reference_total']['node']} + 미해결 {ps['reference_total']['unresolved']} · ③ 튜플 {ps['market_pricing']['tuple']} + 미해결 {ps['market_pricing']['unresolved']} |")
    A(f"| — | — | 실측 합 | 튜플 **{v.get('tuples_total')}** ({', '.join(f'{k}={n}' for k, n in v.get('tuples_by_what_kind', {}).items())}) | 튜플 **{ps['tuples_total']}** ({', '.join(f'{k}={n}' for k, n in ps['tuples_by_what_kind'].items())}) — 코드 참조 {ps['code_references_node']} 이 노드 끝으로 빠짐 · 세 칸 전부 사전 값 {ps['tuples_all_dict_values']} · anchor 둘 이상 {ps['tuples_with_2plus_anchors']} |")
    A("| — | — | 생성기·검산 | `*_v22.py` · `erd-v2.2-tuples.py` · `erd-v2.2-check.py` | `erd_spec_v23.py`·`erd_colmap_v23.py`·`erd_build_v23.py` · `erd-v2.3-tuples.py`(v2.2 분해기 위에 수정 1 코드 참조·엣지 끝 분포 · 부작용 분해기 v2.3) · `erd-v2.3-check.py`(v2.2 항목 전부 + K) |")
    A("")
    A("개체 21 · 관계 31 · 사전 46 · 잎 키 1,072 의 수는 그대로다. 이전 판 산출물·생성기는 지우지 않았다. v2.1 → v2.2 변경 목록은 `erd-v2.2.md` §11.")
    A("")
    A("## 12. 동결 후 결정 레코드로 갈 것 — 검토의 「동결 후」 항목 자리 (이번 범위 아님 · 레코드는 만들지 않았다)")
    A("")
    rows = [
        ("1-C", "「보톡스」 product(PRD-) vs modality(MOD-) — 같은 what 으로 볼지", "canonical_mapping", "target.from_ref=PRD-보톡스(또는 MOD-) · scope=[anchor…] · new_value.to_id"),
        ("1-D", "엑셀V+ 의 what(항목 자신 또는 별도 제품)", "tuple_assign", "target.catalog_item_id=CAT-"),
        ("2-C", "사건 사전 동의어 과민반응·동상·지방괴사·섬유화·공기색전 — 분리할지", "event_split", "target.event, new_value.new_events[]"),
        ("2-D", "부작용의 site none·course 미상을 정의 1 과 같이(식별자 값 아님) 다룰지", "scope_review", "ERD 규칙 개정 — 결정 후 다음 판(v2.3 은 정의값으로 둔다 · §1.5 접힘 조건)"),
        ("1-G · §9.5.3", "볼뉴머 M4/M9 · 엠페이스/엠페이스(EMFACE) · 라라젯/라라젯 (클렌징) 류 — 같은 것인지", "fold_approve(anchors) 또는 conflict_close(not_same)", "v2.3 에서 anchor(CAT-)로 가리킨다"),
        ("§9.5.6", "R5 계열 기법 후보 " + str(len(TUP["procedure"]["inheritance_candidates"])) + " 계열", "canonical_mapping", "target.from_ref=R5:<계열> · scope=§9.5.6 의 CAT- 목록"),
        ("§9.5.3 · §9.5.4", "ambiguous 3 · multi_site·multi_primary 미해결(보톡스 이마/미간 · 필러 볼/턱 · 이마 주름 (수입) …) · 미등록 조각", "tuple_assign_multi · tuple_assign · dictionary_add", "v2.3 kind 가 생겼다"),
        ("§9.6.6 · 9.6.2 (raw)", "raw_name 튜플 " + str(as_["complications_distinct_tuples_raw"]) + " — 「주사 통증 / 불편감」「공기색전·카테터 관련 감염」「구형구축 (…섬유성 결절)」「통증·불편감 및 지연성 통증(LOP)」 등 (사건, 부위, 경과) 지정 · 「주사」→ 주사 부위 같은 부위 동의어", "adverse_tuple_assign · dictionary_add", "target.locator=complications 이름의 원장 locator"),
        ("§9.6.2a", "수식어가 붙지 않은 사건의 경과(「일시적 홍반·부종」의 부종 등) — 미상으로 둘지 지정할지", "adverse_tuple_assign", "v2.3 규칙은 미상"),
        ("§9.6.3", "partial 표현 " + str(as_["expressions_total"]["match_status"].get("partial", 0)) + " · unlinked " + str(as_["expressions_total"]["unlinked"]), "adverse_tuple_assign(kind=expression) · dictionary_add", "target.locator=표현 레코드 locator"),
        ("R30", "인과(혈관 폐색 → 피부 괴사 등)", "edge_create", "target.relation=R30 · from_ref/to_ref=(event, site, course)"),
        ("§1.4 조합 `/`", "「함께」로 읽을지 「또는」으로 읽을지(실리프팅(PDO/PCL) 등)", "scope_review", "ERD 규칙"),
        ("R15 from site", "부위가 원인인 끝(site)을 남길지 — 출처 키 없음", "scope_review", "확인 항목"),
        ("DEC-20~24", "승인", "같은 레코드 status → approved · decided_by · decided_at", "ERD 승인 때"),
        ("§12-3", "제품 사전 확장(step1 395)", "dictionary_add 묶음", "target.dictionary=product_name"),
    ]
    A(md_table(["검토", "무엇", "decision kind", "비고"], rows))
    A("")
    A("전부 「나중에 정리」가 아니라 kind 와 target 자리가 정해진 결정 목록이다 — v2.3 의 kind 16 과 안정 키 규칙으로 전부 담긴다(검토 ③ 표의 「못 담는다」 4 종류가 edge_create · tuple_assign_multi · adverse_tuple_assign · conflict_close 로 닫혔다).")
    return "\n".join(o)


def main():
    v1erd = json.load(open(os.path.join(WORK, "erd-v1.json"), encoding="utf-8"))
    v11erd = json.load(open(os.path.join(WORK, "erd-v1.1.json"), encoding="utf-8"))
    v22erd = json.load(open(os.path.join(WORK, "erd-v2.2.json"), encoding="utf-8"))
    v22tup = json.load(open(os.path.join(WORK, "erd-v2.2-tuples.json"), encoding="utf-8"))
    step1_scan = B11.scan_step1()
    colrows = build_column_map(step1_scan)
    dicts = build_dictionaries_v23()
    erd, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, moves, moves22, moves23, notes23 = write_outputs(colrows, dicts, step1_scan, v1erd, v11erd, v22erd, v22tup)
    md = build_erd_md(erd, colrows, dicts, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, v1erd, moves, v22tup, moves22, moves23, notes23)
    cl = change_log(erd, dicts, TUP, colrows, v22erd, v22tup, moves23, notes23)
    open(os.path.join(WORK, OUT["md"]), "w", encoding="utf-8").write(md + "(검산 실행 중)\n\n" + cl + "\n")  # 검산 J·K 가 본문 절을 읽는다
    chk = load_module("chk23", os.path.join(WORK, OUT["check"]))
    ok, report = chk.run_checks()
    md += report + "\n\n" + cl + "\n"
    open(os.path.join(WORK, OUT["md"]), "w", encoding="utf-8").write(md)
    with open(os.path.join(WORK, OUT["cmap"]), "a", encoding="utf-8") as f:
        f.write("## 검산 결과\n\n" + report + "\n")
    print("OK" if ok else "FAIL")
    print(report)
    print("dests", Counter(r["dest"] for r in colrows), "moves", len(moves), "moves22", len(moves22), "moves23", len(moves23), "notes23", len(notes23))
    print("dicts", len(dicts), "entities", len(S.ENTITIES), "relations", len(S.RELATIONS), "decisions", len(erd["decisions"]), "kinds", len(S.DECISION_KINDS))
    ps, as_ = TUP["procedure"]["summary"], TUP["adverse"]["summary"]
    print("procedure: catalog", ps["catalog_items"], "->", ps["catalog_distinct_tuples"], "| tuples", ps["tuples_total"], ps["tuples_by_what_kind"], "| node", ps["code_references_node"], "| edge ends", ps["edge_ends_total"], ps["edge_ends_total_n"])
    print("adverse: 65 ->", as_["complications_distinct_tuples"], "(dict", as_["complications_distinct_tuples_dict"], "raw", as_["complications_distinct_tuples_raw"], ") | tuples", as_["tuples_total"], "| folded w/ unregistered", as_["folded_with_partial_name"], "| expr", as_["expressions_total"])


if __name__ == "__main__":
    main()
