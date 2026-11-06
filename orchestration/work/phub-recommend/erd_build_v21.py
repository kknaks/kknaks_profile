# -*- coding: utf-8 -*-
"""ERD v2.1 산출물 생성기. v2 생성기(erd_build_v2.py)의 사전 빌더·행선지 표를 재사용하고 시술 튜플 접힘 규칙 1건(erd_spec_v21 · erd-v2.1-tuples.py)만 덧씌운다.
입력: 원장 21 + step1-products.json + 스캔 JSON + erd_spec_v21/erd_colmap_v21 + erd-v1.json(§9.2) + erd-v1.1.json + erd-v2.json·erd-v2-tuples.json(§9.5 나란히 비교 · 변경 목록)
출력: erd-v2.1.md · erd-v2.1.json · erd-v2.1-column-map.md · erd-v2.1-dictionaries.json · erd-v2.1-tuples.json(+검산 결과 부착). v2 파일은 지우지 않는다.
"""
import importlib.util
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
import erd_spec_v21 as S  # noqa
import erd_colmap_v21 as C  # noqa

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
TUPLES = load_module("erd_v21_tuples", os.path.join(WORK, "erd-v2.1-tuples.py"))
OUT = {"md": "erd-v2.1.md", "json": "erd-v2.1.json", "cmap": "erd-v2.1-column-map.md", "dict": "erd-v2.1-dictionaries.json", "tuples": "erd-v2.1-tuples.json", "check": "erd-v2.1-check.py"}


# ---------------------------------------------------------------------------
# 사전 — v1.1 빌더 실행 후 procedure_name → catalog_item_name 개명, 사건·경과·상대 부위 3개 추가
# ---------------------------------------------------------------------------
def build_dictionaries_v21():
    """v2 사전 빌더 그대로(값·순서 동일 · 46)."""
    return B2.build_dictionaries_v2()


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
        ("CATALOG_ITEM", "PRODUCT", "}o--o{", "R3 uses_product"), ("MODALITY", "PRODUCT", "||--o{", "R4 offers_product"),
        ("MODALITY", "TECHNIQUE", "}o--o{", "R5 applies_technique"),
        ("PROCEDURE", "CATALOG_ITEM", "||--o{", "R26 derived_from"), ("PROCEDURE", "MODALITY", "}o--o|", "R27 what"), ("PROCEDURE", "MODALITY_SUBCATEGORY", "}o--o|", "R27 what"), ("PROCEDURE", "PRODUCT", "}o--o|", "R27 what"), ("PROCEDURE", "CATALOG_ITEM", "}o--o|", "R27 what (v2.1 항목 자신)"),
        ("PROCEDURE", "SITE", "}o--o|", "R28 procedure_site"), ("PROCEDURE", "TECHNIQUE", "}o--o|", "technique(dict)"),
        ("PROBLEM", "PROBLEM_SUBCATEGORY", "||--o{", "R6"),
        ("PROBLEM_SUBCATEGORY", "COMPLAINT", "||--o{", "R7 has_complaint"), ("COMPLAINT", "MODALITY", "}o--o{", "R8 addressed_by"),
        ("COMPLAINT", "PROCEDURE", "}o--o{", "R9 recommends"), ("COMPLAINT", "SITE", "}o--o|", "R10 located_at"),
        ("PROBLEM_SUBCATEGORY", "SITE", "}o--o|", "R11 subcategory_site"), ("PACKAGE", "PROCEDURE", "}o--o{", "R12 member"),
        ("PACKAGE", "PROBLEM", "}o--o{", "R13 for_problem"), ("COMPLAINT", "PACKAGE", "}o--o{", "R14 offers_combo"),
        ("PROCEDURE", "ADVERSE_EFFECT", "}o--o{", "R15 may_cause"), ("SITE", "ADVERSE_EFFECT", "}o--o{", "R15 may_cause"),
        ("ADVERSE_EXPRESSION", "ADVERSE_EFFECT", "}o--o|", "R29 expresses"), ("ADVERSE_EFFECT", "ADVERSE_EFFECT", "}o--o{", "R30 leads_to"), ("ADVERSE_EFFECT", "SITE", "}o--o|", "R31 adverse_site"),
        ("PROCEDURE", "PERSON_CONDITION", "}o--o{", "R16 contraindicated_for"), ("PERSON_CONDITION", "PROCEDURE", "}o--o{", "R17 age_group_guidance"),
        ("PROCEDURE", "PROCEDURE", "}o--o{", "R18 interaction"), ("EVIDENCE_STATEMENT", "CITATION", "}o--||", "R19 cites"),
        ("ADVERSE_EXPRESSION", "CITATION", "}o--o|", "R19 cites"), ("CLINICAL_RULE", "CITATION", "}o--o|", "R19 cites"),
        ("MODALITY", "EVIDENCE_STATEMENT", "||--o{", "R20 has_evidence"), ("MODALITY", "ADVERSE_EXPRESSION", "||--o{", "R20 has_evidence"), ("SITE", "ANATOMICAL_STRUCTURE", "}o--o{", "R21 contains"),
        ("SITE", "MODALITY", "}o--o{", "R22 injection_guidance"), ("CONFLICT", "DECISION", "}o--o|", "R24 resolved_by"),
        ("SOURCE_FILE", "CONFLICT", "||--o{", "R25 provenance"),
    ]
    for a, b, c, lab in rels:
        lines.append(f"    {a} {c} {b} : \"{lab}\"")
    lines.append("    %% R9·R12·R15·R16·R17·R18 의 시술 축 끝은 MODALITY|MODALITY_SUBCATEGORY|CATALOG_ITEM|PROCEDURE|PRODUCT 중 하나(target_depth · 튜플 확정 시 PROCEDURE 로 승격). v2.1: PROCEDURE 의 what 은 CATALOG_ITEM 자신일 수도 있다(미등록 조각 있는 항목 · 접히지 않음). ADVERSE_EFFECT 의 event·course 는 값 사전. R25 provenance 는 모든 개체에 닿는다")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 산출물
# ---------------------------------------------------------------------------
def write_outputs(colrows, dicts, step1_scan, v1erd, v11erd, v2erd, v2tup):
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
    # §9.2 — v1.1 분해 규칙 재실행(사전 값 동일 · 색인 이름만 비춤)
    v1rep = v1erd.get("resolution_report") if v1erd else None
    RES, TOTAL = RESOLVE.run_all(TUPLES.with_alias(dic_json), S.RESOLVE_RULES, L, L[STEP1], v1rep)
    # 튜플 실측 (①②③ · 부작용)
    TUP = TUPLES.run_all(dic_json, S.TUPLE_RULES, L, S.RESOLVE_RULES)
    json.dump(TUP, open(os.path.join(WORK, OUT["tuples"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    IDX = B.Index()
    CONF = B11.conflict_estimates_v11(IDX, RES)
    Q14 = B11.q14_bundles_v11()
    SITE_TABLE = B11.site_replacement_table(dicts)
    res_summary = OrderedDict()
    for k, v in RES.items():
        res_summary[k] = {kk: vv for kk, vv in v.items() if kk != "rows"}
        res_summary[k]["v1"] = ({"n": v1rep[k]["n"], "resolved": v1rep[k]["resolved"], "unresolved": v1rep[k]["unresolved"], "by_depth": v1rep[k]["by_depth"]} if v1rep and k in v1rep else None)
    decisions = []
    for no, (who, what, where) in S.DISPOSITIONS.items():
        decisions.append({"id": f"DEC-2026-11-04-{no:02d}", "kind": "scope_review" if no in (2, 4, 5) else "conflict_resolution", "what": f"재검토 8-{no}: {what}", "why": "ERD v1.1 발주서 §A (사용자 승인 「그렇게 진행하자」)",
                          "who": "사용자" if who == "사용자" else "워커 처리 · 사용자 승인", "when": "2026-11-04", "applies_to": where, "status": "applied(v1.1)"})
    decisions.append({"id": "DEC-2026-11-04-20", "kind": "scope_review", "what": "구조 변경 ①: 시술 축을 catalog_item(분류 항목 그대로)과 procedure(what×site×technique 튜플)로 분리", "why": "ERD v2 발주서 (사용자 승인 「진행하자」)", "who": "사용자", "when": "2026-11-04", "applies_to": "§2 catalog_item·procedure · R2·R3·R26~R28 · §1.4 · §9.5", "status": "applied(v2)"})
    decisions.append({"id": "DEC-2026-11-04-21", "kind": "scope_review", "what": "구조 변경 ②: 부작용을 사건 사전 + 경과 사전 + adverse_effect(event×site×course 튜플) + adverse_expression(원문)으로 분리", "why": "ERD v2 발주서 (사용자 승인 「진행하자」)", "who": "사용자", "when": "2026-11-04", "applies_to": "§2 adverse_effect·adverse_expression · R15·R19·R20·R29~R31 · §1.5 · §9.6", "status": "applied(v2)"})
    decisions.append({"id": "DEC-2026-11-04-22", "kind": "scope_review", "what": "v2.1: 시술 튜플 접힘 규칙 수정 — 이름 조각이 전부 사전 값일 때만 접힘, 미등록 조각 있으면 what=분류 항목 자신(catalog_item), 부모 하위분류 fallback 삭제, 참조 ②③는 미등록 조각 있으면 미해결", "why": "ERD v2.1 발주서 (v2 §9.5.2 에서 서로 다른 제품·부위가 같은 시술로 접힌 것 확인)", "who": "사용자", "when": "2026-11-04", "applies_to": "§1.4 what 규칙 · procedure.what_kind/candidate_name · R26·R27 · resolve_rules.fallback_to_parent · §9.5", "status": "applied(v2.1)"})
    moves = [{"file": f, "path": p, "v1_1": a, "v2": b} for f, p, a, b in C.MOVES]
    ps, as_ = TUP["procedure"]["summary"], TUP["adverse"]["summary"]
    erd = OrderedDict([
        ("erd_version", S.ERD_VERSION), ("previous_version", "v2"), ("status", "draft — 사용자 승인 전"), ("written", "2026-11-04"), ("bronze_snapshot", S.SNAPSHOT),
        ("layers", {"bronze": "원장 21 그대로 + 조사 산출물 step1-products.json 1 (바이트 보존, SHA256 식별)", "semantic": "이 ERD + 값 사전 + 분해 규칙(참조 §1.3 · 튜플 §1.4/§1.5), 승인이 정본 조건, 버전 개정", "silver": "ERD 를 따르는 정규화 레코드, 모든 값에 (file, path) 출처", "gold": "실버 조합 뷰, 새 사실 금지"}),
        ("normalize_rule", S.NORMALIZE_RULE), ("id_rule", S.ID_RULE), ("resolve_rules", S.RESOLVE_RULES), ("tuple_rules", S.TUPLE_RULES),
        ("source_files", files_meta),
        ("entities", ent_json), ("relations", rel_json), ("enums", S.ERD_ENUMS),
        ("quality_rules", [{"no": a, "class": b, "rule": c} for a, b, c in S.QUALITY_RULES]),
        ("synonym_key_normalization", v1erd["synonym_key_normalization"] if v1erd else {}),
        ("q25", [{"no": n, "answer": a} for n, a in S.Q25]),
        ("review_dispositions", [{"no": no, "title": B.REVIEW[no - 1]["title"], "decided_by": who, "disposition": what, "applied_at": where} for no, (who, what, where) in S.DISPOSITIONS.items()]),
        ("decisions", decisions),
        ("site_replacement_8_2", SITE_TABLE),
        ("q14_bundles", Q14),
        ("step1_column_scan", {"file": STEP1, "leaf_count": step1_scan["leaf_count"], "bytes": step1_scan["bytes"], "method": "bronze-ledger-column-scan.py FileScan (같은 접기 규칙)", "top_level": step1_scan["top_level"]}),
        ("column_map_summary", {"leaf_paths": len(colrows), "by_file_group": {"ledger_21": sum(1 for r in colrows if r["file"] != STEP1), "step1": sum(1 for r in colrows if r["file"] == STEP1)},
                                "by_dest": dict(dest_counter), "by_dest_ledger_21": dict(Counter(r["dest"] for r in colrows if r["file"] != STEP1)), "by_dest_step1": dict(Counter(r["dest"] for r in colrows if r["file"] == STEP1)),
                                "by_entity": dict(Counter(r["target"].split(".")[0] for r in colrows if r["dest"] == "개체")), "by_dict": dict(Counter(r["target"] for r in colrows if r["dest"] == "사전")),
                                "by_relation": dict(Counter(r["target"].split(".")[0].split("(")[0] for r in colrows if r["dest"] == "엣지"))}),
        ("column_map_moves", moves),
        ("dictionaries_summary", [{"name": d.name, "label": d.label, "kind": getattr(d, "kind", "value"), "canonical": len(d.entries), "synonyms": sum(len(e["synonyms"]) for e in d.entries.values()), "candidates": len(d.candidates)} for d in dicts.values()]),
        ("resolution_report", res_summary), ("resolution_total", TOTAL),
        ("tuple_report", {"procedure": ps, "adverse": as_}),
        ("tuple_report_v2", {"procedure": (v2erd or {}).get("tuple_report", {}).get("procedure"), "adverse": (v2erd or {}).get("tuple_report", {}).get("adverse")}),
        ("conflict_estimates", CONF),
    ])
    json.dump(erd, open(os.path.join(WORK, OUT["json"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    # column map md
    md = ["# ERD v2.1 — 잎 키 행선지 표 (원장 21 + step1-products.json)", "", "**v2 와 동일하다.** v2.1 은 시술 튜플의 what 결정 규칙만 바꾸었고 잎 키 행선지(1,072 행)·이동 표는 `erd-v2-column-map.md` 와 한 행도 다르지 않다(검산 A 에서 행 단위로 대조). 아래 표는 같은 규칙(`erd_colmap_v21.py` = `erd_colmap_v2.py`)으로 다시 생성한 것이다.", "",
          f"작성 2026-11-04 · 입력 `bronze-ledger-column-scan.json`(원장 잎 키 {sum(1 for r in colrows if r['file'] != STEP1)}) + `step1-products.json` 잎 키 {step1_scan['leaf_count']}(`bronze-ledger-column-scan.py` 와 같은 방식으로 스캔) = {len(colrows)} · 행선지 범주 5: 개체 / 사전 / 엣지 / 브론즈 / 버림 · **미정 0**", "",
          f"표적 표기: `entity.attr` · `dict:<사전>` · `R#.attr`(관계 번호는 erd-v2.1.md §3) · `bronze` · `drop`. v1.1 과 달라진 행 {len(moves)}(아래 이동 표) — 구조 변경 ①(procedure.* → catalog_item.*) · ②(adverse_effect.name → dict:adverse_event_type / adverse_expression.*). 그 밖은 v1.1 그대로.", "",
          "## 이동 표 (v1.1 → v2)", "", md_table(["#", "파일", "경로", "v1.1", "v2"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['v1_1']}`", f"`{m['v2']}`") for i, m in enumerate(moves)]), "",
          "## 요약", "", md_table(["행선지", "원장 21", "step1", "합계"], [(k, sum(1 for r in colrows if r["dest"] == k and r["file"] != STEP1), sum(1 for r in colrows if r["dest"] == k and r["file"] == STEP1), v) for k, v in sorted(dest_counter.items(), key=lambda x: -x[1])] + [("합계", sum(1 for r in colrows if r["file"] != STEP1), sum(1 for r in colrows if r["file"] == STEP1), len(colrows))]), ""]
    for f in FILES + [STEP1]:
        rs = [r for r in colrows if r["file"] == f]
        md.append(f"## `{f}` — 잎 키 {len(rs)}" + (" (조사 산출물 · 22번째 브론즈 원천)" if f == STEP1 else ""))
        md.append("")
        md.append(md_table(["#", "경로", "타입", "횟수", "행선지", "표적", "비고"], [(i + 1, f"`{r['path']}`", r["type"], r["count"], r["dest"], f"`{r['target']}`", r["note"]) for i, r in enumerate(rs)]))
        md.append("")
    open(os.path.join(WORK, OUT["cmap"]), "w", encoding="utf-8").write("\n".join(md))
    return erd, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, moves


# ---------------------------------------------------------------------------
# erd-v2.1.md
# ---------------------------------------------------------------------------
def build_erd_md(erd, colrows, dicts, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, v1erd, moves, v2tup):
    o = []
    A = o.append
    v1rep = v1erd.get("resolution_report", {}) if v1erd else {}
    T = S.TUPLE_RULES
    A("# ERD v2.1 — 피부과 시술 허브 메달리온 시맨틱 정의")
    A("")
    A("작성 2026-11-04 · 상태 **초안(사용자 승인 전)** · 브론즈 스냅샷 2026-10-26 (+ 조사 산출물 step1 10-29) · 발주서 `erd-v2.1-brief.md` (v2 발주서 `erd-v2-brief.md` · v1.1 `erd-v1.1-brief.md` · v1 `erd-v1-brief.md` 의 입력·금지·기준·질문 기본값·처분 유지)")
    A("")
    A("기계용 동본 `erd-v2.1.json` · 값 사전 `erd-v2.1-dictionaries.json`(v2 와 값 동일) · 잎 키 행선지 `erd-v2.1-column-map.md`(v2 와 동일) · 분해 규칙 실행 `erd-v1.1-resolve.py`(§9.2, v1.1 그대로 재실행) · 튜플 실측 `erd-v2.1-tuples.py`(결과 `erd-v2.1-tuples.json`, §9.5 v2 수치와 나란히 · §9.6) · 검산 `erd-v2.1-check.py` (결과 §10). v1·v1.1·v2 산출물은 그대로 두었다. v2 → v2.1 변경 목록은 §11, 범위 밖 관찰은 §12 (v1.1 → v2 변경 목록은 `erd-v2.md` §11).")
    A("")
    A("**v2.1 의 범위는 시술 튜플 접힘 규칙 1건뿐이다.** v2 §9.5.2 에서 분류 항목 이름이 어느 사전에도 안 닿으면 what 을 부모 하위분류로 떨어뜨려 하위분류 아래 항목이 전부 한 튜플로 접혔다(M15-1 케미컬필링 60 · M9-1 HIFU 13 · M1-3 용도별 9 …) — 서로 다른 제품·부위가 같은 시술로 접힌 것이다. v2.1: **이름 조각이 전부 사전에 닿았을 때만** 사전 값으로 조립하고 그때만 접힌다. 하나라도 미등록이면 what = 그 분류 항목 자신(what_kind=`catalog_item`, 미등록 조각은 `candidate_name`), 부모 하위분류 fallback 삭제(`fallback_to_parent: false`), 참조 ②③는 미등록 조각 있으면 미해결(⑨). 구조(개체 21 · 관계 31 · 사전 46 · 행선지 1,072)·부작용 튜플은 v2 그대로. ERD 는 설계다 — 데이터는 안 고치고, 사전 값·동의어 추가는 이번 범위가 아니다(미등록은 목록만).")
    A("")
    A("## 1. 범위와 층")
    A("")
    A("| 층 | 무엇 | 규칙 |")
    A("|---|---|---|")
    A("| 브론즈 | 원장 21개 JSON 그대로 + `step1-products.json`(조사 산출물) | 바이트 보존·수정 금지. 파일 SHA256 이 식별자(§6 표). 원장 스냅샷 2026-10-26, step1 10-29 |")
    A("| 시맨틱 | 이 ERD + 값 사전 + 분해 규칙(참조 §1.3 · 튜플 §1.4/§1.5) | 문서. 사용자 승인이 정본 조건. 버전으로 개정(v1 → v1.1 → v2 → v2.1 → …) |")
    A("| 실버 | ERD 를 따르는 정규화 레코드 | **모든 값은 (파일, 잎 키 경로) 출처를 가진다.** 출처 없는 값 금지. 충돌은 둘 다 보관 |")
    A("| 골드 | 실버 조합 뷰 | 실버에 없는 사실을 만들지 않는다. 충돌 미판정 레코드 제외 |")
    A("")
    A("지식은 원장 21개·컬럼 리포트·스캔 결과·v1/v1.1/v2 산출물·`step1-products.json` 에서만 가져왔다. step2·step3·source-map·DATA-001·DEC-*·silver-*·`_archive/` 는 열지 않았다.")
    A("")
    A("### 1.1 정규화(「같은 것」판정)와 식별자")
    A("")
    A(f"- 정규화 `{S.NORMALIZE_RULE['name']}`: " + " → ".join(S.NORMALIZE_RULE["steps"]))
    A(f"- {S.NORMALIZE_RULE['note']}")
    A(f"- 식별자: `{S.ID_RULE['format']}`. canonical_key 는 개체별(§2 각 표의 「식별자」). {S.ID_RULE['canonical_key']}")
    A(f"- survey 제품: {S.ID_RULE['survey_products']}")
    A(f"- **v2 튜플 식별자** — procedure: `{S.ID_RULE['procedure']}` · adverse_effect: `{S.ID_RULE['adverse_effect']}` · catalog_item: {S.ID_RULE['catalog_item']} · adverse_expression: {S.ID_RULE['adverse_expression']}")
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
    A("v1.1 의 세 단계를 **데이터**(`erd-v2.1.json → resolve_rules`)로 적고 `erd-v1.1-resolve.py` 가 그대로 실행한다. v2 에서 바뀐 것은 사전 순서의 「단위 시술」 자리가 `catalog_item_name`(분류 항목 이름 색인)을 읽는다는 것뿐이고, v2.1 은 규칙 데이터에 `fallback_to_parent: false` 를 명시했다(3단계 조립의 what 결정 — §1.4). 유사도·추측은 없다.")
    A("")
    A(f"1. **계열 확정** — {R['step1_family']['what']}. 자리별 힌트: " + " · ".join(f"{k}: `{v}`" for k, v in R["step1_family"]["slot_hints"].items()) + f". 코드 정규식 `{R['step1_family']['code_regex']}`")
    A(f"2. **이름 분해** — 괄호 안을 뗀다(`{R['step2_decompose']['paren_regex']}`). 조합 기호 `{'` `'.join(R['step2_decompose']['combo_symbols'])}` 로 멤버를 나눈다. 조각마다 사전 순서 **{' → '.join(R['step2_decompose']['dictionary_order'])}**(procedure = catalog_item_name) 로 완전 일치를 시도한다(계열 사전에 닿으면 kind=modality). 규격 정규식 `{R['step2_decompose']['spec_regex']}` + unit 사전. {R['step2_decompose']['secondary_rule']}. {R['step2_decompose']['scope_rule']}. {R['step2_decompose']['overlap_rule']}.")
    A(f"3. **조립** — 튜플 ({', '.join(R['step3_assemble']['tuple'])}). (a) resolved: {R['step3_assemble']['resolved']} (b) 분해 성공·항목 없음: {R['step3_assemble']['decomposed']} (c) unresolved: {R['step3_assemble']['unresolved']}")
    A(f"   - **fallback_to_parent = {R['step3_assemble']['fallback_to_parent']}** — {R['step3_assemble']['fallback_to_parent_note']}")
    A("")
    A("결과는 §9.2 에 v1 수치와 나란히(v1.1 과 같은 수치 — 사전 값이 같다). (a)·(b) 의 결과는 §1.4 의 튜플 규칙으로 한 번 더 내려가 procedure 튜플이 되고, (c) 미해결은 v2.1 에서 튜플을 만들지 않는다(§9.5.4).")
    A("")
    A("### 1.4 시술 튜플 분해 규칙 (구조 변경 ① · v2.1 what 결정 규칙 교체 · 데이터 `erd-v2.1.json → tuple_rules.procedure` · `erd-v2.1-tuples.py` 실행)")
    A("")
    P = T["procedure"]
    A(f"- 입력: ① {P['input']['catalog_items']} · ② {P['input']['references']}")
    A(f"- 조각: {P['fragments']}")
    A(f"- 조합: {P['combo']}")
    A(f"- fallback_to_parent: **{P['fallback_to_parent']}** (v2.1)")
    A("- what(필수) — v2.1 규칙:")
    for i, w in enumerate(P["what"], 1):
        A(f"  {i}. {w}")
    A(f"- site: {P['site']}")
    A(f"- technique: {P['technique']}")
    A(f"- 수식 조각: {P['qualifiers']}")
    A(f"- 식별자: `{P['id']}` · 상태: {P['status']}")
    A("")
    A("### 1.5 부작용 튜플 분해 규칙 (구조 변경 ② · v2 그대로 · 데이터 `erd-v2.1.json → tuple_rules.adverse`)")
    A("")
    Q = T["adverse"]
    A(f"- 입력: {Q['input']['complications']} · 표현: {Q['input']['phrases']}")
    A(f"- 분해: {Q['split']}")
    A(f"- 튜플: {Q['tuple']}")
    A(f"- 타임라인 normal: {Q['normal_phrases']}")
    A(f"- 문헌: {Q['literature']}")
    A(f"- 식별자: `{Q['id']}` · 상태: {Q['status']}")
    A("")
    A("## 2. 개체 목록")
    A("")
    A(f"개체 {len(S.ENTITIES)}개 — v2 와 같다(v1.1 19 + `catalog_item` + `adverse_expression`). 발주서 최소 목록 11 + 추가 {sum(1 for e in S.ENTITIES if e.get('beyond_minimum'))}(표시 ★). v2.1 에서 바뀐 것은 `procedure` 의 what 정의(what_kind 에 catalog_item · 속성 candidate_name 추가)와 `catalog_item` 정의 문구뿐. 그 밖 19 개체는 v2 그대로.")
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
    A(f"관계 {len(S.RELATIONS)}개 — v2 와 같다(v1.1 25 + R26~R31). v2.1 에서 바뀐 것은 R26·R27 비고(R27 끝에 catalog_item 추가)뿐. `proc_axis` = modality | modality_subcategory | catalog_item | procedure | product. 시너지·순서·간격·시술간 금기는 **R18 하나**의 `kind` 속성. 참조 끝점은 §1.3 규칙으로 정해지고, 「분해 성공·항목 없음」이면 엣지가 튜플(조합)을 가리킨다. v2 승격 규칙(R3·R9·R12·R15·R16·R17·R18): 참조가 분류 항목에 닿으면 target_depth=catalog_item, 그 항목의 튜플이 확정(complete)이면 procedure 로 승격(via_catalog_item 보존) — 규칙만 적고 값은 실버 빌드에서.")
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
    A(f"전부 `erd-v2.1-dictionaries.json` — **v2 와 값·순서 동일**. 값 사전 {nval} + 개체 이름 색인 {nidx}(B 분해 규칙이 읽는 제품명·하위분류 라벨·분류 항목 이름) = {len(dicts)}. v1.1 43 → v2/v2.1 {len(dicts)}: 추가 adverse_event_type(사건) · course(경과) · relative_site(상대 부위) · 개명 procedure_name → catalog_item_name(값 동일). 부위 사전 21 · 기법 사전 12 유지(공유 사전).")
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
    A("- `course`: " + " · ".join(f"{e['canonical']}(동의어: {', '.join(s['value'] for s in e['synonyms']) or '—'} · 출처 {e['sources'][0]['file']}:{e['sources'][0]['path']})" for e in dicts["course"].entries.values()))
    A("- `relative_site`: " + " · ".join(f"{e['canonical']}(동의어: {', '.join(s['value'] for s in e['synonyms']) or '—'})" for e in dicts["relative_site"].entries.values()))
    A("")
    A("## 5. 충돌·결정 개체 정의 + 규칙 ①~⑩ + 신뢰 순위")
    A("")
    A("충돌(`conflict`)·결정(`decision`) 개체 정의는 §2. v1.1 의 재검토 처분 19 건은 결정 레코드 19 개로, v2 구조 변경 2건은 결정 레코드 2 개(DEC-2026-11-04-20·21), v2.1 접힘 규칙 수정은 1 개(DEC-2026-11-04-22)로 `erd-v2.1.json → decisions` 에 미리 적재한다.")
    A("")
    A(md_table(["#", "분류", "규칙"], S.QUALITY_RULES))
    A("")
    A("빈값과 「없음」: 안 적힌 것(키 없음·null·빈 배열·빈 문자열) = null(미입력). 명시적으로 없다고 적힌 것만 빈 목록. step1 의 「확인 불가」·「근거 없음」·「해당 없음」은 값이다(null 아님). 튜플의 site none·technique none·course 미상은 「값이 없음」이 아니라 축의 정의값이다(튜플 식별자에 들어간다). 단계 끝 = 컬럼 행선지 미정 0 · 충돌 미판정 0.")
    A("")
    A("### 5.1 원장 신뢰 순위 (파일별 · 21 + step1) — v1.1 그대로")
    A("")
    A(md_table(["순위", "파일", "종류", "근거 키", "표시", "비고"], [(t, f"`{f}`", S.SOURCE_KIND[f], b, S.TRUST_FLAGS.get(f, ""), n) for f, t, b, n in sorted(S.SOURCE_FILES, key=lambda x: (x[1], x[0]))]))
    A("")
    s1 = next(fm for fm in erd["source_files"] if fm["file"] == STEP1)
    A(f"`products.json` 의 `products[].mfds` 필드만 2(식약처 허가)로 격상한다. `complications.json` 은 8-1 처분으로 3 유지 + 「AI 컨센서스 추정」 — v2 의 사건 사전 뼈대가 이 파일이므로 사건 값에도 같은 표시가 따라간다. `step1-products.json` 은 조사 산출물: 허가 건 `licenses[].source` 가 `{S.STEP1_TIER2_SOURCE_RE}` 에 맞는 {s1['trust_tier_rule']['tier2_licenses']}/{s1['trust_tier_rule']['licenses_total']} 건의 허가·회사·공식명 필드만 2, 그 밖은 3.")
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
    A("v2 에서 답이 바뀐 질문은 없다. 질문 10·11 의 「단위 시술 개체」는 v2 에서 분류 항목(catalog_item)을 뜻하고, 그 위에 튜플(procedure)이 §1.4 로 얹힌다.")
    A("")
    A("## 8. 기본값 재검토 — 처분 결과 (v1.1 그대로)")
    A("")
    A("v1 §8 의 19 건 처분은 v1.1 에서 확정됐고 v2·v2.1 은 바꾸지 않는다. 각 건은 결정 레코드(`erd-v2.1.json → decisions`)로 남는다.")
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
    A("### 9.2 격리 목록 — 참조 해결, v1 vs v1.1 규칙 (v2 재실행 · 같은 수치)")
    A("")
    A("v1 = 완전 일치만. v1.1 규칙(§1.3)을 v2.1 사전(= v2 사전)으로 `erd-v1.1-resolve.py` 를 다시 돌린 수치 — 사전 값이 같으므로 v1.1·v2 와 같다. 「분해 성공·항목 없음」은 조각이 전부 사전에 닿았지만 taxonomy 항목 하나로 떨어지지 않은 참조. 미해결은 사전에 없는 조각이 하나라도 있는 참조. v2.1 에서는 해결·분해 성공만 §1.4 로 procedure 튜플이 되고 미해결은 튜플을 만들지 않는다(§9.5.4 — v2 는 미등록 조각이 있어도 힌트 계열·부모 층으로 partial 튜플을 만들었다). 고민 자리·pih id 자리는 v1 규칙 그대로.")
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
    A("### 9.3 충돌 예상 수 (v1.1 그대로 재계산)")
    A("")
    A(md_table(["종류", "무엇", "건"], [(c["kind"], c["what"], c["n"]) for c in CONF]))
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
    A("### 9.5 시술 튜플 실측 (v2.1 접힘 규칙 · `erd-v2.1-tuples.py` 실제 실행 · v2 수치와 나란히 · 숫자는 목표가 아니다)")
    A("")
    A("규칙은 §1.4(v2.1). 분류 항목은 **자기 이름을 색인에서 제외**하고 분해했다(자기 참조 금지). 같은 튜플 = 같은 시술이며, 접힌 표(9.5.2)는 **세 칸이 전부 사전 값인 것만** 남고 사용자가 「같은 게 맞다」고 볼 수 있도록 **전부** 보인다. 미등록 조각이 있는 항목은 항목 자신이 what 이라 9.5.3 에 하나씩 있다(candidate_name 열). 부위 사전 21 · 기법 사전 12 는 v1.1 그대로라 「전체얼굴」「풀페이스」같은 조각은 미등록이고, 기법은 R5 기법이 하나인 계열에서만 상속된다. v2 열은 `erd-v2-tuples.json` 의 수치.")
    A("")
    A(TUPLES.procedure_md(TUP, (v2tup or {}).get("procedure", {}).get("summary")))
    A("")
    A("### 9.6 부작용 튜플 실측 (구조 변경 ② · v2 그대로 · `erd-v2.1-tuples.py` 가 v2 부작용 분해기를 그대로 실행)")
    A("")
    A("규칙은 §1.5(v2 그대로 · 손대지 않았다). 사건 사전 뼈대는 complications 65 이름의 분해 조각(§4.1)이고, 다른 파일의 문구는 그 사전으로만 분해했다(사전 추가 없음). 접힌 표(9.6.2)는 65 이름이 어느 튜플로 갔는지 **전부** 보인다. 9.6.6 은 v2.1 발주서의 검산 항목(미등록 조각 있는 이름이 접혔는가).")
    A("")
    A(TUPLES.adverse_md(TUP))
    A("")
    A("## 10. 검산 결과")
    A("")
    A("`erd-v2.1-check.py` 를 독립 실행한 출력을 그대로 붙였다(같은 폴더에서 `python3 erd-v2.1-check.py`). v2 검산 항목 전부(A 잎 키 행선지 · B 사전 값 출처 · C ERD 출처 키·표적 · D 브론즈 sha256 · E 분해 규칙 재현 · F 처분 반영 · G 튜플 실측 재현 · H 구조 변경 반영) + I v2.1 접힘 규칙(fallback 0 · partial 항목이 둘 이상 접힌 튜플 0 · 접힌 튜플 세 칸 전부 사전 값 · 참조 partial 0 · 행선지·사전 v2 와 동일 · 부작용 접힘 확인).")
    A("")
    return "\n".join(o)


def change_log(erd, dicts, TUP, colrows, v2erd, v2tup, moves):
    o = []
    A = o.append
    ps, as_ = TUP["procedure"]["summary"], TUP["adverse"]["summary"]
    v2 = (v2tup or {}).get("procedure", {}).get("summary", {})
    v2a = (v2tup or {}).get("adverse", {}).get("summary", {})
    ne2 = len(v2erd["entities"]) if v2erd else 21
    nr2 = len(v2erd["relations"]) if v2erd else 31
    nd2 = len(v2erd["dictionaries_summary"]) if v2erd else 46
    A("## 11. v2 → v2.1 변경 목록")
    A("")
    A("| 묶음 | 무엇 | v2 | v2.1 |")
    A("|---|---|---|---|")
    A("| 규칙 | 분류 항목 what (§1.4) | 이름이 제품 색인에 닿으면 product, 아니면 **부모 하위분류**(가장 구체적인 계열 층). 미등록 조각이 있어도 하위분류 튜플로 접힘(partial) | 조각이 **전부** 사전에 닿았을 때만 사전 값 what(product > 하위분류)으로 조립·접힘. 하나라도 미등록이면 what = **항목 자신**(what_kind=catalog_item · candidate_name 보존 · partial). 전부 닿았어도 primary 없으면 항목 자신(complete). 부모 하위분류 fallback 삭제 |")
    A("| 규칙 | 다른 분류 항목에 닿은 조각 | 그 항목의 튜플 what 을 그대로 씀 | 그 항목의 what 이 사전 값일 때만. 항목 자신이 what 인 항목(예: 젠틀맥스프로)에 닿은 항목(젠틀맥스프로+)은 접지 않고 자기 자신 |")
    A("| 규칙 | 조각(통째 일치) | 바로 분해(사전 값 안의 괄호·조합 기호도 쪼갬 → 「PRP/자가혈」「리쥬란 HB+」가 미등록) | v1.1 3단계 (a) **통째 일치를 먼저** 본다(분류 항목은 자기 이름 제외) — 참조 미해결 수가 v1.1 §9.2 ⑨ 와 자리별로 같다(검산 I) |")
    A("| 규칙 | 참조 ②·③ | 미등록 조각이 있어도 what 이 정해지면(힌트 계열·분류 항목·제품) partial 튜플 | 미등록 조각이 있으면 **미해결(⑨)** · 튜플 없음(부모 층으로 접지 않음). partial 참조 튜플 0 |")
    A("| 규칙 데이터 | `resolve_rules.step3_assemble.fallback_to_parent` | 없음 | **false** (+ note) · `tuple_rules.procedure.fallback_to_parent=false` · `tuple_rules.name` tuples_v2 → tuples_v2_1 · `resolve_rules.name` decompose_v1_1 → decompose_v2_1 |")
    A(f"| 개체 | procedure | what_kind ∈ {{modality, modality_subcategory, product}} · 속성 8 | what_kind ∈ {{…, **catalog_item**}} · what_id 에 CAT- 허용 · 속성 **candidate_name**(str[]) 추가 · status 비고 · 정의 문구. 개체 수 {ne2} → {len(S.ENTITIES)} (변화 없음) |")
    A(f"| 관계 | R26 · R27 | R27 → modality\\|modality_subcategory\\|product | R27 → … \\|**catalog_item** · R26 비고(CAT- what 튜플은 1:1). 관계 수 {nr2} → {len(S.RELATIONS)} (변화 없음) |")
    A(f"| 열거형 | procedure.what_kind | 3 값 | 4 값(+catalog_item). 열거형 수 {len(v2erd['enums']) if v2erd else '—'} → {len(S.ERD_ENUMS)} |")
    A(f"| 사전 | 46 | 값·순서 동일 | 값·순서 동일({nd2} → {len(dicts)}) · 파일명만 erd-v2.1-dictionaries.json |")
    A(f"| 행선지 | 잎 키 1,072 · 이동 {len(moves)} | 동일 | **동일**(erd-v2.1-column-map.md = v2 · 검산 A 행 단위 대조) |")
    A(f"| 실측 ① | 분류 항목 521 → 튜플 | **{v2.get('catalog_distinct_tuples')}** (접힌 튜플 {v2.get('catalog_tuples_with_2plus_items')} 에 항목 {v2.get('catalog_items_in_folded_tuples')} · 부모 하위분류 fallback {v2.get('catalog_by_what_basis', {}).get('parent_subcategory')}) | **{ps['catalog_distinct_tuples']}** (접힌 튜플 {ps['catalog_tuples_with_2plus_items']} 에 항목 {ps['catalog_items_in_folded_tuples']} · 전부 세 칸 사전 값 {ps['catalog_folded_all_dict_values']}/{ps['catalog_tuples_with_2plus_items']} · fallback {ps['catalog_fallback_to_parent']} · 항목 자신 what {ps['catalog_self_items']}) |")
    A(f"| 실측 ① | what_kind 분포(항목) | {', '.join(f'{k}={v}' for k, v in v2.get('catalog_by_what_kind', {}).items())} | {', '.join(f'{k}={v}' for k, v in ps['catalog_by_what_kind'].items())} |")
    A(f"| 실측 ② | 참조 {ps['reference_total']['n']} | 튜플 {v2.get('reference_total', {}).get('tuple')} + combo {v2.get('reference_total', {}).get('combo_ref')} + 불가 {v2.get('reference_total', {}).get('none')} (partial {v2.get('reference_total', {}).get('partial')}) · distinct {v2.get('reference_total', {}).get('distinct_tuples')} | 튜플 {ps['reference_total']['tuple']} + combo {ps['reference_total']['combo_ref']} + **미해결 {ps['reference_total']['unresolved']}** + 불가 {ps['reference_total']['none']} (partial {ps['reference_total']['partial']}) · distinct {ps['reference_total']['distinct_tuples']} |")
    A(f"| 실측 ③ | market-pricing 122 | 튜플 {v2.get('market_pricing', {}).get('tuple')} (partial {v2.get('market_pricing', {}).get('partial')}) · distinct {v2.get('market_pricing', {}).get('distinct_tuples')} | 튜플 {ps['market_pricing']['tuple']} + **미해결 {ps['market_pricing']['unresolved']}** · distinct {ps['market_pricing']['distinct_tuples']} |")
    A(f"| 실측 합 | 튜플 전체 | **{v2.get('tuples_total')}** ({', '.join(f'{k}={v}' for k, v in v2.get('tuples_by_what_kind', {}).items())}) · site none {v2.get('tuples_site_none_ratio')} · technique none {v2.get('tuples_technique_none_ratio')} | **{ps['tuples_total']}** ({', '.join(f'{k}={v}' for k, v in ps['tuples_by_what_kind'].items())}) · site none {ps['tuples_site_none_ratio']}(사전 값 what 만 {ps['tuples_dict_what_site_none_ratio']}) · technique none {ps['tuples_technique_none_ratio']} |")
    A(f"| 실측 | 미등록 조각 | distinct {v2.get('unregistered_distinct')} · 총 {v2.get('unregistered_total')} | distinct {ps['unregistered_distinct']} · 총 {ps['unregistered_total']} — 사전은 안 바뀌었다. 차이는 통째 일치를 먼저 봐서(v1.1 ⑨ 와 같은 판정) 「PRP/자가혈」「마이크로니들링(MTS)」「리쥬란 HB+」「바이오스티뮬레이터/콜라겐부스터」가 더 이상 쪼개지지 않는 분. 분류 항목 분은 candidate_name 으로 튜플에 보존 |")
    A(f"| 부작용 | §9.6 | 65 → {v2a.get('complications_distinct_tuples')} · 튜플 {v2a.get('tuples_total')} | **그대로**(65 → {as_['complications_distinct_tuples']} · 튜플 {as_['tuples_total']}). 검산 항목 9.6.6 추가: 둘 이상 이름이 접힌 튜플 {as_['folded_with_2plus_names']} 중 미등록 조각 있는 이름이 섞인 것 {as_['folded_with_partial_name']} — 발주서 전제(이미 적용)와 다름, 손대지 않음 |")
    A(f"| 결정 레코드 | 21 | — | 22 (+DEC-2026-11-04-22 v2.1 접힘 규칙) |")
    A(f"| 생성기·검산 | `*_v2.py` · `erd-v2-tuples.py` · `erd-v2-check.py` | — | `erd_spec_v21.py`·`erd_colmap_v21.py`·`erd_build_v21.py` · `erd-v2.1-tuples.py`(v2 분해기 위에 what 규칙만 교체 · 부작용은 v2 코드 재사용) · `erd-v2.1-check.py`(v2 항목 전부 + I) |")
    A("")
    A("v2 산출물과 생성기는 지우지 않았다. §2~§8·§9.1~§9.4·§9.6 은 v2 그대로(재실행 수치 동일). v1.1 → v2 변경 목록은 `erd-v2.md` §11.")
    A("")
    A("## 12. v2.1 밖 관찰 (손대지 않았다 — 다음 판 또는 실버 빌드 결정 묶음)")
    A("")
    fold2 = [f for f in TUP["procedure"]["folded"] if f["n_items"] >= 2]
    obs = [
        f"**부작용 튜플의 접힘**(§9.6.6): 둘 이상 이름이 접힌 부작용 튜플 {as_['folded_with_2plus_names']} 중 {as_['folded_with_partial_name']} 는 미등록 조각(「기저 위험」「반응」「시술 직후」「카테터 관련」…)이 있는 이름을 포함한다. 발주서는 「같은 원칙이 이미 적용돼 있다」고 전제했지만 §1.5 는 event×site×course 가 사전 값이면 접는다(수식 조각은 접힘 조건이 아니다). 시술 축과 같은 규칙(미등록 조각 있으면 접지 않음)을 부작용에도 적용할지는 사용자 결정 — 예: 「감염」5 이름 중 「공기색전·카테터 관련 감염」은 갈라진다.",
        f"**접힌 튜플 {len(fold2)}**(§9.5.2): " + " · ".join(f"{f['what']}({f['n_items']}: {', '.join(f['items'])})" for f in fold2) + ". 볼뉴머(M4·M9 같은 이름 두 항목)은 같은 제품, 「클라리티2 (혈관)」·「피코슈어 프락셀」은 제품 + 하위분류 라벨 조각(혈관·프락셀)이 전부 사전에 닿아 제품 튜플로 접혔다 — 하위분류 조각은 extra_primaries 로만 남는다. 「같은 시술」로 볼지는 사용자 확인.",
        f"**항목 자신이 what 인 튜플 {ps['catalog_self_items']}**: 제품 사전(59)에 없는 제품형 이름이 대부분이다(candidate_name). 제품 사전을 넓히면(step1 395 등 — 실버 빌드 결정 후보) 그만큼 what=product 로 바뀌고 같은 제품끼리만 접힌다. 사전 추가라 범위 밖.",
        f"**참조 미해결 ② {ps['reference_total']['unresolved']} · ③ {ps['market_pricing']['unresolved']}**: v2 에서 힌트 계열·분류 항목으로 partial 튜플이 되던 참조가 v2.1 에서는 튜플 없이 미해결로 남는다(엣지는 v1.1 ⑨ 대로 target_label 만). 미등록 조각 상위(§9.5.6)는 통째 일치로 빠진 4 라벨 분 말고는 v2 와 같다 — 사전 추가가 곧 해결 수.",
        "참조(②③)가 분류 항목 이름에 **통째로** 닿고 그 항목의 what 이 항목 자신이면(PRP·레이저토닝·서브시전·피코토닝·슈링크 …) 그 항목의 CAT- 튜플로 간다 — 부모 층이 아니라 항목 자신이므로 접힘이 아니다. 「실리프팅(PDO/PCL)」처럼 괄호 안 조각이 항목 자신 what 인 항목에 닿는 참조는 그 항목 튜플(PDO·PCL)로 가고 outer 「실리프팅」은 계열 조각(extra).",
        "**technique 상속**: 항목 자신이 what 인 튜플에도 §1.4 technique 규칙(R5 기법이 하나인 계열 상속)을 그대로 적용했다(발주서 「site/technique 는 닿은 조각만」은 부모 하위분류에서 끌어오지 않는다는 뜻으로 읽었다 — 상속은 하위분류가 아니라 계열 R5). 상속을 끄면 technique none 비율이 오른다. 사용자 확인.",
        "분류 항목 「목주름/턱선」(M1)은 조합 기호 `/` 가 있지만 「목주름」이 미등록이라 조합 판정 전에 항목 자신으로 갔다(site=턱선 · candidate_name=목주름). 미등록 조각 규칙이 조합 규칙보다 먼저다.",
        "「사각턱」「승모근」(M1)은 조각이 전부 닿았지만(부위) primary 가 없어 항목 자신 what + site 다(complete). v2 에서는 부모 하위분류(M1-3 용도별)로 접혔다. 「젠틀맥스프로+」는 「젠틀맥스프로」(항목 자신 what)에 닿아 자기 자신(complete · 접지 않음).",
        "v2 §12 의 관찰 11 건(R5 기법 둘 이상 계열 · 미등록 조각 축 판정 · 사전 순서 · 제품 사전 확장 · 타 계열 제품 · 사건 사전 category · safety_phrase · R30 · 문헌 unlinked · 충돌 표 · 기타 하위분류 · market-pricing 가격)은 그대로 유효하다. 그중 「제품형 이름이 부모 하위분류로 접힌다」(v2 §12-4)는 v2.1 로 해소됐다(접히지 않음) — 제품 사전 확장은 여전히 범위 밖.",
    ]
    for i, x in enumerate(obs, 1):
        A(f"{i}. {x}")
    A("")
    A(f"관찰 {len(obs)} 건. 전부 「나중에 정리」가 아니라 손대지 않은 항목의 기록이다.")
    return "\n".join(o)


def main():
    v1erd = json.load(open(os.path.join(WORK, "erd-v1.json"), encoding="utf-8"))
    v11erd = json.load(open(os.path.join(WORK, "erd-v1.1.json"), encoding="utf-8"))
    v2erd = json.load(open(os.path.join(WORK, "erd-v2.json"), encoding="utf-8"))
    v2tup = json.load(open(os.path.join(WORK, "erd-v2-tuples.json"), encoding="utf-8"))
    step1_scan = B11.scan_step1()
    colrows = build_column_map(step1_scan)
    dicts = build_dictionaries_v21()
    erd, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, moves = write_outputs(colrows, dicts, step1_scan, v1erd, v11erd, v2erd, v2tup)
    md = build_erd_md(erd, colrows, dicts, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, v1erd, moves, v2tup)
    chk = load_module("chk21", os.path.join(WORK, OUT["check"]))
    ok, report = chk.run_checks()
    md += report + "\n\n" + change_log(erd, dicts, TUP, colrows, v2erd, v2tup, moves) + "\n"
    open(os.path.join(WORK, OUT["md"]), "w", encoding="utf-8").write(md)
    with open(os.path.join(WORK, OUT["cmap"]), "a", encoding="utf-8") as f:
        f.write("## 검산 결과\n\n" + report + "\n")
    print("OK" if ok else "FAIL")
    print(report)
    print("dests", Counter(r["dest"] for r in colrows), "moves", len(moves))
    print("dicts", len(dicts), "entities", len(S.ENTITIES), "relations", len(S.RELATIONS))
    ps, as_ = TUP["procedure"]["summary"], TUP["adverse"]["summary"]
    print("procedure: catalog", ps["catalog_items"], "->", ps["catalog_distinct_tuples"], "| folded", ps["catalog_tuples_with_2plus_items"], "| fallback", ps["catalog_fallback_to_parent"], "| what", ps["catalog_by_what_kind"], "| tuples", ps["tuples_total"], "| site none", ps["tuples_site_none_ratio"], "| tech none", ps["tuples_technique_none_ratio"])
    print("adverse: 65 ->", as_["complications_distinct_tuples"], "| events", as_["event_dictionary_values"], "| tuples", as_["tuples_total"], "| expr", as_["expressions_total"], "| unreg", as_["unregistered_distinct"])


if __name__ == "__main__":
    main()
