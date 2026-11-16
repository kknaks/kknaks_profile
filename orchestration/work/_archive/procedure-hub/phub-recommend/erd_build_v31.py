# -*- coding: utf-8 -*-
"""ERD v3.1 산출물 생성기. v3 생성기(erd_build_v3.py)를 바탕으로 발주서 erd-v3.1-brief.md 6건 + 코디·사용자 추가 4건(V3.1-7~10)만 덧씌운다(erd_spec_v31 · erd_colmap_v31 · erd-v3.1-tuples.py).
입력: 원장 21 = 브론즈 2판 bronze/phub-ledger/(HASHES.txt 검증) + step1-products.json + 스캔 JSON + erd_spec_v31/erd_colmap_v31 + erd-v1.json(§9.2) + erd-v1.1.json + erd-v3.json·erd-v3-tuples.json(나란히 비교 · 변경 목록 · 결정 이관)
출력: erd-v3.1.md · erd-v3.1.json · erd-v3.1-column-map.md · erd-v3.1-dictionaries.json · erd-v3.1-tuples.json(+검산 결과 부착). 이전 판 파일은 지우지 않는다.
"""
import json
import os
import re
import sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_build as B  # noqa
import erd_spec_v31 as S  # noqa
import erd_build_v3 as B3  # noqa  (원장을 2판으로 바꾼다 · 사전 v3 · mermaid)
import erd_build_v11 as B11  # noqa
import erd_build_v23 as B23  # noqa
import erd_colmap_v31 as C  # noqa

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
TUPLES = load_module("erd_v31_tuples", os.path.join(WORK, "erd-v3.1-tuples.py"))
OUT = {"md": "erd-v3.1.md", "json": "erd-v3.1.json", "cmap": "erd-v3.1-column-map.md", "dict": "erd-v3.1-dictionaries.json", "tuples": "erd-v3.1-tuples.json", "check": "erd-v3.1-check.py"}
RULE_REF = B23.RULE_REF
DERIVED_ID_RE = re.compile(r"\b(PRC|ADV|CFL|PHR|CND)-")
WRITTEN = "2026-11-05"


# ---------------------------------------------------------------------------
# 사전 — v3 47 + person_condition(V3.1-4) + phrase_dictionary(V3.1-10 · 분해 뒤에 채운다) · removed_synonyms 이력(V3.1-3)
# ---------------------------------------------------------------------------
def build_dictionaries_v31():
    DICTS = B3.build_dictionaries_v3()
    # V3.1-3 제거 이력(dictionary 수준) — v3 가 ERD 로 뺀 「공기색전」
    for d in DICTS.values():
        d.removed_synonyms = []
        d.removed_entries = []
    ev = DICTS["adverse_event_type"]
    for e in ev.entries.values():
        for x in e.get("v3_removed_synonyms", []):
            ev.removed_synonyms.append({"value": x["value"], "canonical": e["canonical"], "decision_id": None, "by": "ERD v3(V3-1)", "removed_at": "2026-11-05", "why": x["why"]})
    # V3.1-4 조건 사전
    d = Dict_("person_condition", "사람 조건 사전(condition_dictionary)", "v3.1(V3.1-4): 사람 조건 개체의 식별 사전 — 정준값·동의어·kind(condition|check|age_group · 그 값이 나타난 kind 들)·출처(derived · 사람 조건 이름 9 키 값의 부분 문자열). 초기값은 원장 이름 298 의 분해 조각에서 ERD 가 고른 조건 핵심(부작용 사건 사전과 같은 방식) · 동의어는 괄호 동치·표기 변형뿐 · 뜻이 같은 다른 말은 dictionary_add 결정")
    d.kind = "value"
    d.removed_synonyms, d.removed_entries = [], []
    kind_by = S.CONDITION_KIND_BY_SOURCE
    for r in TUPLES.condition_core_sources(L, S.CONDITION_CORES):
        assert r["sources"], f"조건 사전 값 출처 없음: {r['canonical']}"
        f0, p0, n0 = r["sources"][0]
        kinds = sorted({kind_by[f"{f}:{p}"] for f, p, n in r["sources"]} | {kind_by[f"{f}:{p}"] for _, ss in r["synonyms"] for f, p, n in ss})
        e = d.add_canonical(r["canonical"], f0, p0, n0, kind="derived", kinds=kinds, note=r["note"])
        e["kind"] = "|".join(kinds)
        for f, p, n in r["sources"][1:]:
            e["sources"].append(d.src(f, p, n, "derived"))
        for sv, ss in r["synonyms"]:
            assert ss, f"조건 사전 동의어 출처 없음: {r['canonical']} ~ {sv}"
            link = "표기 변형(derived)" if any(x in sv for x in ("한냉", "냉", "당뇨")) else "괄호 동치(derived)"
            for i, (f, p, n) in enumerate(ss):
                d.add_synonym(norm(r["canonical"]), sv, f, p, n, link=link, kind="derived")
    return DICTS


def phrase_dictionary_json(TUP):
    """V3.1-10 문구 사전 — 분해 결과(erd-v3.1-tuples.json adverse.phrase_dictionary)를 사전 모양으로."""
    entries = []
    for e in TUP["adverse"]["phrase_dictionary"]:
        srcs = Counter()
        for loc in e["locators"]:
            f, rest = loc.split(":", 1)
            p = rest.split("@", 1)[0]
            srcs[(f, p)] += 1
        entries.append(OrderedDict([("id", e["id"]), ("canonical", e["normalized"]), ("normalized", e["normalized"]), ("raw_variants", e["raw_variants"]), ("kinds", e["kinds"]), ("langs", e["langs"]), ("locators", e["locators"]), ("modality_codes", e["modality_codes"]),
                                    ("sources", [{"file": f, "path": p, "n": n, "kind": "phrase"} for (f, p), n in srcs.items()]), ("synonyms", []), ("definition", None),
                                    ("status", e["status"]), ("reasons", e["reasons"]), ("units", e["units"]), ("created_units", e["created_units"]), ("candidates", e["candidates"]), ("parsed", e["parsed"]), ("unregistered", e["unregistered"]), ("translations", e["translations"]), ("citations", e["citations"]), ("accuracy", e["accuracy"])]))
    return {"name": "phrase_dictionary", "label": "안전 문구 사전", "note": "v3.1(V3.1-10): 원장 문구(safety · 타임라인 · 응급 징후 · 문헌 문장 · 환자 설명 · 필수 고지)의 정규화형(norm_v1 + 수식어 제거) 항목 — 단위(사건·부위·물질)로의 지도 · status auto|approved|unlinked · 결정 phrase_map 이 승인·수정 · 다음 스냅샷의 같은 문구는 결정 없이 자동. 분해가 읽는 사전이 아니라 분해가 쓰는 사전(캐시)", "kind": "phrase_index",
            "canonical_count": len(entries), "synonym_count": 0, "candidate_count": 0, "entries": entries, "candidates": [], "removed_synonyms": [], "removed_entries": [],
            "by_status": dict(Counter(e["status"] for e in entries)), "occurrences": sum(len(e["locators"]) for e in entries)}


def dict_json(dicts):
    j = B23.dict_json(dicts)
    for dj, d in zip(j["dictionaries"], dicts.values()):
        dj["removed_synonyms"] = getattr(d, "removed_synonyms", [])
        dj["removed_entries"] = getattr(d, "removed_entries", [])
    j["erd_version"] = S.ERD_VERSION
    j["bronze_version"] = S.BRONZE_VERSION
    j["dictionary_kinds"]["phrase_index"] = "문구 사전(v3.1 V3.1-10) — 분해가 쓰는 정규화형 → 단위 지도 · 결정 phrase_map 으로 승인·수정"
    j["source_kinds"]["phrase"] = "문구 사전 항목: 그 경로의 값(표면형 raw_variants 전부)이 정규화형 항목으로 접힌 것 — 검산은 raw_variants 가 그 경로의 값과 정규화 일치하는지 본다"
    j["values_changed_from_v3"] = {"added_dictionary": ["person_condition(조건 사전 · V3.1-4)", "phrase_dictionary(문구 사전 · V3.1-10 · 분해 결과)"], "added_fields": ["*.removed_synonyms[] / removed_entries[] (V3.1-3 이력 · 「공기색전」 1건 기록)"], "note": "v3 47 사전의 값·동의어·순서는 v3 과 같다(검산 N-11)"}
    j["note"] = "v3.1: 사전 49 = v3 47 + person_condition + phrase_dictionary. 값 변경 0(이력 필드만 추가)"
    return j


def migrate_decisions(v3erd):
    recs, mig = [], []
    for o in v3erd["decisions"]:
        r = OrderedDict((k, o[k]) for k in S.DECISION_COMMON_FIELDS)
        recs.append(r)
        mig.append({"id": r["id"], "v3": {k: o.get(k) for k in ("kind", "decided_by", "decided_at", "status")}, "v3_1": {k: r[k] for k in ("kind", "decided_by", "decided_at", "status")},
                    "derived_id_in_target": bool(DERIVED_ID_RE.search(json.dumps(r["target"], ensure_ascii=False))), "change": "없음(그대로)"})
    recs.append(OrderedDict([("id", "DEC-2026-11-05-27"), ("kind", "scope_review"),
                             ("target", {"erd_ref": "§0 정의 2 개정 · §1.5 · §1.6 · §2.6 product · §2.14 adverse_effect(세 칸) · §2.16 person_condition(사전 단위) · §2.19 clinical_rule · §2 adverse_expression 삭제 · R12 · R15 · R16~R18 · R19/R20 · R29 삭제 · R32 · §4 person_condition·phrase_dictionary · §5.2 kind 20 · 적용 ⓪① · resolve_rules.stopwords", "review_item": "erd-v3.1-brief.md V3.1-1 ~ V3.1-6 + 코디·사용자 추가 V3.1-7 ~ V3.1-10 (2026-11-05)"}),
                             ("new_value", {"disposition": "v3.1: product_reclassify · R32 rule_applies_to · dictionary_remove · 조건 사전(person_condition 단위) · 회·차 자리 · stopwords 겹침 · 필수 고지 clinical_rule(disclosure)+R32 · 안전 문구 수식어 목록 · 사용자 정의 2 개정(단위 (사건, 부위, 물질) · 경과는 엣지) · 문구 사전(phrase_dictionary · adverse_expression/R29 삭제 · 부록 · phrase_map)"}),
                             ("reason", "5차 빌드·적합성 시험에서 드러난 틈 6 + 사용자 결정 4 — 사용자 승인 2026-11-05 「3.1 진행」. ERD 승인 때 approved"),
                             ("decided_by", None), ("decided_at", None), ("status", "proposed"),
                             ("source_refs", [{"kind": "brief", "ref": "erd-v3.1-brief.md"}, {"kind": "erd", "ref": "ERD-V3-CANDIDATES.md v3.1 후보 · ERD-FROZEN.md"}, {"kind": "review", "ref": "silver-v3/out/report.md §13 · batch3-proposed EXO-02/05/06"}])]))
    return recs, mig


def build_column_map(step1_scan):
    return B3.build_column_map.__wrapped__(step1_scan) if hasattr(B3.build_column_map, "__wrapped__") else _build_column_map(step1_scan)


def _build_column_map(step1_scan):
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
    s = B3.mermaid()
    head, _ = s.split("    %% v3:", 1)
    head = "\n".join(ln for ln in head.split("\n") if "R29" not in ln and "ADVERSE_EXPRESSION" not in ln)
    return head + ("    %% v3.1: ADVERSE_EFFECT 단위는 (event, site, qualifier) 세 칸 — 경과는 R15 엣지 속성 · 상대 부위는 none(사용자 정의 2 개정). 원장 문구는 개체가 아니라 PHRASE_DICTIONARY 항목이며 R15.source_phrases · 단위 explanations · 게이트 unlinked_phrases 의 부록(R29 삭제). "
                   "PERSON_CONDITION 은 조건 사전 단위(CND- = kind|정준값 · raw_name) · 문장은 phrases[] 부록. CLINICAL_RULE(disclosure · product_note) → R32 rule_applies_to → PRODUCT|TECHNIQUE|proc_axis. R12 member 에 session_count·session_index. DECISION kind 20(+product_reclassify ⓪ · dictionary_remove ① · phrase_map ①). 원장 = 브론즈 2판")


def stopword_locators(TUP):
    st = {w["word"]: w for w in TUP["procedure"]["summary"]["stopwords"]["words"]}
    out = []
    for w in S.RESOLVE_RULES["step2_decompose"]["stopwords"]["words"]:
        m = st.get(w["word"], {})
        out.append(dict(w, locators=m.get("locators", []), hits=m.get("hits", 0)))
    return out


def adverse_stopword_locators(TUP):
    a = TUP["adverse"]["summary"]["adverse_stopwords"]
    byw = {w["word"]: w for w in a["words"]}
    byp = {p["regex"]: p for p in a["patterns"]}
    sw = S.TUPLE_RULES["adverse"]["adverse_stopwords"]
    sw["words"] = [dict(w, locators=byw.get(w["word"], {}).get("locators", []), hits=byw.get(w["word"], {}).get("hits", 0)) for w in sw["words"]]
    sw["patterns"] = [dict(p, locators=byp.get(p["regex"], {}).get("locators", []), hits=byp.get(p["regex"], {}).get("hits", 0)) for p in sw["patterns"]]


def condition_marker_locators(TUP):
    m = {x["word"]: x for x in TUP["condition"]["summary"]["markers"]}
    S.TUPLE_RULES["condition"]["markers_measured"] = [{"word": w, "hits": m.get(w, {}).get("hits", 0), "locators": m.get(w, {}).get("locators", [])} for w in S.CONDITION_MARKERS]


# ---------------------------------------------------------------------------
# 산출물
# ---------------------------------------------------------------------------
def write_outputs(colrows, dicts, step1_scan, v1erd, v11erd, v3erd, v3tup, bronze, rescan):
    tiers = {f: (t, basis, note) for f, t, basis, note in S.SOURCE_FILES}
    files_meta = []
    bro = {r["file"]: r for r in bronze["files"]}
    for f in FILES + [STEP1]:
        data = L[f]
        meta = {}
        if isinstance(data, dict):
            for k in ["version", "updated", "description", "consensus_method", "source_method", "currency", "note", "generated_at", "scope"]:
                if isinstance(data.get(k), (str, int)):
                    meta[k] = str(data[k])
        t, basis, note = tiers[f]
        path = os.path.join(LEDGER, f) if f != STEP1 else os.path.join(WORK, f)
        fm = {"file": f, "kind": S.SOURCE_KIND[f], "path_dir": "bronze/phub-ledger" if f != STEP1 else "work", "sha256": sha256(path), "bytes": os.path.getsize(path),
              "snapshot_date": S.SNAPSHOT if f != STEP1 else "2026-10-29", "bronze_version": S.BRONZE_VERSION if f != STEP1 else None, "hashes_txt": bro[f]["hashes_txt"] if f != STEP1 else None, "v1_sha256": bro[f]["v1_sha256"] if f != STEP1 else None, "changed_from_v1": bro[f]["changed_from_v1"] if f != STEP1 else None,
              "trust_tier": t, "trust_basis": basis, "trust_note": note, "trust_flag": S.TRUST_FLAGS.get(f),
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
    TUP = TUPLES.run_all(dic_json, S.TUPLE_RULES, L, S.RESOLVE_RULES, v3tup)
    TUP["procedure"]["v21_none_fold_split"] = TUPLES.V3.v21_split(TUP)
    # 규칙 데이터에 실측 적재
    S.RESOLVE_RULES["step2_decompose"]["stopwords"]["words"] = stopword_locators(TUP)
    S.RESOLVE_RULES["step2_decompose"]["stopwords"]["overlap"] = TUP["procedure"]["summary"]["stopwords"]["overlap"]
    adverse_stopword_locators(TUP)
    condition_marker_locators(TUP)
    json.dump(TUP, open(os.path.join(WORK, OUT["tuples"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    # V3.1-10 문구 사전을 사전 파일에
    dj["dictionaries"].append(phrase_dictionary_json(TUP))
    json.dump(dj, open(os.path.join(WORK, OUT["dict"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    dic_json = json.load(open(os.path.join(WORK, OUT["dict"]), encoding="utf-8"))
    IDX = B.Index()
    CONF = B11.conflict_estimates_v11(IDX, RES)
    for c in CONF:
        c["rule_ref"] = RULE_REF.get(c["kind"])
        c["status_on_build"] = "open"
        c["close_kind"] = "conflict_close(not_same) · fold_approve(v3: 접는 쌍의 ⑦ 을 닫는다)" if c["kind"] == "duplicate_candidate" else "conflict_override · conflict_close" if c["kind"] == "value_conflict" else "dictionary_add · conflict_close · v3.1: 문구는 phrase_map · 조건은 dictionary_add(person_condition)" if c["kind"] == "unregistered_value" else "tuple_assign(_multi · v3: 미해결 anchor 에도) · dictionary_add · conflict_close(needs_source)"
    Q14 = B11.q14_bundles_v11()
    SITE_TABLE = B11.site_replacement_table(dicts)
    res_summary = OrderedDict()
    for k, v in RES.items():
        res_summary[k] = {kk: vv for kk, vv in v.items() if kk != "rows"}
        res_summary[k]["v1"] = ({"n": v1rep[k]["n"], "resolved": v1rep[k]["resolved"], "unresolved": v1rep[k]["unresolved"], "by_depth": v1rep[k]["by_depth"]} if v1rep and k in v1rep else None)
        res_summary[k]["v3"] = ({kk: v3erd["resolution_report"][k].get(kk) for kk in ("n", "resolved", "decomposed", "unresolved")} if v3erd and k in v3erd.get("resolution_report", {}) else None)
    decisions, decisions_migration = migrate_decisions(v3erd)
    moves = [{"file": f, "path": p, "v1_1": a, "v2": b} for f, p, a, b in C.MOVES]
    moves22 = [{"file": f, "path": p, "v2_1": a, "v2_2": b} for f, p, a, b in C.MOVES_V22]
    moves23 = [{"file": f, "path": p, "v2_2": a, "v2_3": b} for f, p, a, b in C.MOVES_V23]
    moves24 = [{"file": f, "path": p, "v2_3": a, "v2_4": b} for f, p, a, b in C.MOVES_V24]
    moves3 = [{"file": f, "path": p, "v2_4": a, "v3": b} for f, p, a, b in C.MOVES_V3]
    moves31 = [{"file": f, "path": p, "v3": a, "v3_1": b} for f, p, a, b in C.MOVES_V31]
    notes31 = [{"file": f, "path": p, "target": t, "note": n} for f, p, t, n in C.NOTE_CHANGES_V31]
    ps, as_, cs = TUP["procedure"]["summary"], TUP["adverse"]["summary"], TUP["condition"]["summary"]
    EE_rows = [{k: v for k, v in r.items() if k != "ends"} for r in TUP["procedure"]["edge_ends"]]
    pd_ = dic_json["dictionaries"][-1]
    erd = OrderedDict([
        ("erd_version", S.ERD_VERSION), ("previous_version", S.PREVIOUS_VERSION), ("status", "draft — 사용자 승인 전"), ("written", WRITTEN), ("bronze_snapshot", S.SNAPSHOT), ("bronze_version", S.BRONZE_VERSION), ("bronze", {k: v for k, v in bronze.items() if k != "files"}), ("bronze_leaf_rescan", rescan),
        ("layers", {"bronze": "원장 21(브론즈 2판 bronze/phub-ledger · HASHES.txt) + 조사 산출물 step1-products.json 1 (바이트 보존, SHA256 식별)", "semantic": "이 ERD + 값 사전 + 문구 사전 + 분해 규칙(참조 §1.3 · 튜플 §1.4/§1.5 · 조건 §1.6), 승인이 정본 조건, 버전 개정", "silver": "ERD 를 따르는 정규화 레코드, 모든 값에 (file, path) 출처 · 문구·조건 문장은 개체가 아니라 부록", "gold": "실버 조합 뷰(동의서 뷰 포함), 새 사실 금지"}),
        ("user_definitions", [{"no": n, "text": t} for n, t in S.USER_DEFINITIONS]), ("user_definitions_v3", [{"no": n, "text": t} for n, t in S.USER_DEFINITIONS_V3]), ("user_definitions_v31", [{"no": n, "text": t} for n, t in S.USER_DEFINITIONS_V31]),
        ("explicit_exception", S.EXPLICIT_EXCEPTION), ("explicit_exception_v31", S.EXPLICIT_EXCEPTION_V31), ("user_definitions_v3_note", S.USER_DEFINITIONS_V3_NOTE), ("user_definitions_v31_note", S.USER_DEFINITIONS_V31_NOTE),
        ("principles", [{"key": k, "text": v} for k, v in S.PRINCIPLES]), ("principles_v24", [{"key": k, "text": v} for k, v in S.V3.PRINCIPLES]),
        ("normalize_rule", S.NORMALIZE_RULE), ("id_rule", S.ID_RULE), ("fold_condition", S.FOLD_CONDITION), ("course_rule", S.COURSE_RULE), ("site_rule", S.SITE_RULE), ("raw_name_rule", S.RAW_NAME_RULE), ("expression_rule", S.EXPRESSION_RULE),
        ("adverse_fold_rule", S.ADVERSE_FOLD_RULE), ("locator_rule", S.LOCATOR_RULE), ("cat_family_rule", S.CAT_FAMILY_RULE),
        ("qualifier_rule", S.QUALIFIER_RULE), ("company_paren_rule", S.COMPANY_PAREN_RULE), ("stopword_rule", S.STOPWORD_RULE), ("combo_rule", S.COMBO_RULE), ("site_kind_rule", S.SITE_KIND_RULE), ("rename_rule", S.RENAME_RULE), ("media_rule", S.MEDIA_RULE), ("r5_subcategory_rule", S.R5_SUBCAT_RULE), ("decision_anchor_rule", S.DECISION_ANCHOR_RULE), ("fold_close_rule", S.FOLD_CLOSE_RULE),
        ("product_reclassify_rule", S.PRODUCT_RECLASSIFY_RULE), ("r32_rule", S.R32_RULE), ("dictionary_remove_rule", S.DICTIONARY_REMOVE_RULE), ("condition_rule", S.CONDITION_RULE), ("session_rule", S.SESSION_RULE), ("stopword_overlap_rule", S.STOPWORD_OVERLAP_RULE), ("disclosure_rule", S.DISCLOSURE_RULE), ("adverse_stopword_rule", S.ADVERSE_STOPWORD_RULE), ("unit_rule", S.UNIT_RULE), ("phrase_dictionary_rule", S.PHRASE_DICTIONARY_RULE), ("phrase_shape_rule", S.PHRASE_SHAPE_RULE), ("phrase_map_rule", S.PHRASE_MAP_RULE),
        ("adverse_qualifiers", [{"canonical": c, "kind": k, "source": f"{src[0]}:{src[1]}", "synonyms": [{"value": sv, "source": f"{ss[0]}:{ss[1]}"} for sv, ss in syns], "note": n} for c, k, src, syns, n in S.ADVERSE_QUALIFIERS]),
        ("site_layers", [{"canonical": c, "source": f"{src[0]}:{src[1]}", "synonyms": [{"value": sv, "source": f"{ss[0]}:{ss[1]}"} for sv, ss in syns], "note": n} for c, src, syns, n in S.SITE_LAYERS]),
        ("condition_cores", [{"canonical": c, "synonyms": syns, "note": n} for c, syns, n in S.CONDITION_CORES]), ("condition_markers", S.CONDITION_MARKERS), ("condition_kind_by_source", S.CONDITION_KIND_BY_SOURCE),
        ("edge_end_rule", S.EDGE_END_RULE), ("edge_end_kinds", S.EDGE_END_KINDS), ("proc_axis_edges", S.PROC_AXIS_EDGES),
        ("resolve_rules", S.RESOLVE_RULES), ("tuple_rules", S.TUPLE_RULES),
        ("source_files", files_meta),
        ("entities", ent_json), ("relations", rel_json), ("enums", S.ERD_ENUMS),
        ("quality_rules", [{"no": a, "class": b, "rule": c} for a, b, c in S.QUALITY_RULES]),
        ("synonym_key_normalization", v1erd["synonym_key_normalization"] if v1erd else {}),
        ("q25", [{"no": n, "answer": a} for n, a in S.Q25]),
        ("review_dispositions", [{"no": no, "title": B.REVIEW[no - 1]["title"], "decided_by": who, "disposition": what, "applied_at": where} for no, (who, what, where) in S.DISPOSITIONS.items()]),
        ("decision_kinds", [{"kind": k, "build_reads": br, "target": t, "new_value": nv, "note": n, "new_in_v2_2": k in S.DECISION_KINDS_NEW, "new_in_v2_3": k in S.DECISION_KINDS_NEW_V23, "reshaped_in_v2_3": S.DECISION_KINDS_RESHAPED_V23.get(k), "new_in_v3": k in S.DECISION_KINDS_NEW_V3, "note_changed_in_v3": S.DECISION_KINDS_NOTE_V3.get(k), "new_in_v3_1": k in S.DECISION_KINDS_NEW_V31, "note_changed_in_v3_1": S.DECISION_KINDS_NOTE_V31.get(k)} for k, br, t, nv, n in S.DECISION_KINDS]),
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
        ("column_map_moves", moves), ("column_map_moves_v2_2", moves22), ("column_map_moves_v2_3", moves23), ("column_map_moves_v2_4", moves24), ("column_map_moves_v3", moves3), ("column_map_moves_v3_1", moves31),
        ("column_map_note_changes_v2_3", v3erd.get("column_map_note_changes_v2_3", [])), ("column_map_note_changes_v2_4", v3erd.get("column_map_note_changes_v2_4", [])), ("column_map_note_changes_v3", v3erd.get("column_map_note_changes_v3", [])), ("column_map_note_changes_v3_1", notes31),
        ("dictionaries_summary", [{"name": d["name"], "label": d["label"], "kind": d.get("kind", "value"), "canonical": len(d["entries"]), "synonyms": sum(len(e["synonyms"]) for e in d["entries"]), "candidates": len(d["candidates"])} for d in dic_json["dictionaries"]]),
        ("resolution_report", res_summary), ("resolution_total", TOTAL),
        ("tuple_report", {"procedure": ps, "adverse": as_, "condition": cs}),
        ("tuple_report_v3", {"procedure": (v3erd or {}).get("tuple_report", {}).get("procedure"), "adverse": (v3erd or {}).get("tuple_report", {}).get("adverse")}),
        ("edge_ends", {"rows": EE_rows, "total": ps["edge_ends_total"], "total_n": ps["edge_ends_total_n"], "by_relation": ps["edge_ends_by_relation"], "slots": ps["edge_ends_slots"], "member_mode": ps["edge_ends_member_mode"], "multi_tuple": ps["edge_ends_multi_tuple"]}),
        ("phrase_dictionary_summary", {"entries": pd_["canonical_count"], "occurrences": pd_["occurrences"], "by_status": pd_["by_status"]}),
        ("r32_candidates", TUP["r32_candidates"]), ("product_reclassify_examples", TUP["product_reclassify"]),
        ("v21_none_fold_split", TUP["procedure"]["v21_none_fold_split"]),
        ("technique_inheritance_candidates", TUP["procedure"]["inheritance_candidates"]),
        ("r29_taxonomy_safety_keys", S.R29_TAXONOMY_SAFETY_KEYS),
        ("conflict_estimates", CONF),
        ("change_list", [{"no": a, "what": b, "where": c} for a, b, c in S.CHANGE_LIST]), ("change_list_v3_1", [{"no": a, "what": b, "where": c} for a, b, c in S.CHANGE_LIST_V31]),
    ])
    json.dump(erd, open(os.path.join(WORK, OUT["json"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = ["# ERD v3.1 — 잎 키 행선지 표 (원장 21 · 브론즈 2판 + step1-products.json)", "",
          f"**v3 와 행선지·표적이 다른 행은 {len(moves31)} 개다** — V3.1-7 consent mandatory_disclosures 1(modality 속성 → clinical_rule.text) + V3.1-10 표현 관련 28(개체 adverse_expression.* → 사전 dict:phrase_dictionary). 비고만 바뀐 행 {len(notes31)}(아래 「비고 변경 v3 → v3.1」 — V3.1-4 조건 사전 출처·단위 식별 · V3.1-2 제품 note 후보 · V3.1-5 회·차 자리 · V3.1-9 단위 세 칸·경과 엣지 · V3.1-6 겹침). 그 밖 행선지·표적·비고는 v3 과 같다(검산 A 행 단위 대조). 규칙 `erd_colmap_v31.py`.", "",
          f"브론즈 2판 잎 키 재스캔: 원장 21 잎 키 {rescan['leaf_count_v2']} = 1판 {rescan['leaf_count_v1']} · 파일별 집합 차이 {len(rescan['diff'])}.", "",
          f"작성 {WRITTEN} · 입력 `bronze-ledger-column-scan.json`(원장 잎 키 {sum(1 for r in colrows if r['file'] != STEP1)}) + `step1-products.json` 잎 키 {step1_scan['leaf_count']} = {len(colrows)} · 행선지 범주 5: 개체 / 사전 / 엣지 / 브론즈 / 버림 · **미정 0**", "",
          f"표적 표기: `entity.attr` · `dict:<사전>` · `R#.attr`(관계 번호는 erd-v3.1.md §3) · `bronze` · `drop`. v1.1 과 달라진 행 {len(moves)} + v2.2 {len(moves22)} + v2.3 {len(moves23)} + v2.4 {len(moves24)} + v3 {len(moves3)} + v3.1 {len(moves31)}.", "",
          "## 이동 표 (v3 → v3.1)", "", md_table(["#", "파일", "경로", "v3", "v3.1"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['v3']}`", f"`{m['v3_1']}`") for i, m in enumerate(moves31)]), "",
          "## 비고 변경 (v3 → v3.1 · 표적 동일)", "", md_table(["#", "파일", "경로", "표적", "추가된 비고"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['target']}`", m["note"]) for i, m in enumerate(notes31)]), "",
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
    return erd, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, moves, moves22, moves23, moves24, moves3, moves31, notes31, dic_json


# ---------------------------------------------------------------------------
# erd-v3.1.md
# ---------------------------------------------------------------------------
def build_erd_md(erd, colrows, dicts, dic_json, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, v1erd, moves, v3tup, moves31, notes31):
    o = []
    A = o.append
    v1rep = v1erd.get("resolution_report", {}) if v1erd else {}
    T = S.TUPLE_RULES
    ps, as_, cs = TUP["procedure"]["summary"], TUP["adverse"]["summary"], TUP["condition"]["summary"]
    v3s = (v3tup or {}).get("procedure", {}).get("summary")
    v3a = (v3tup or {}).get("adverse", {}).get("summary", {})
    bro = erd["bronze"]
    D = {d["name"]: d for d in dic_json["dictionaries"]}
    A("# ERD v3.1 — 피부과 시술 허브 메달리온 시맨틱 정의")
    A("")
    A(f"작성 {WRITTEN} · 상태 **초안(사용자 승인 전)** · 원장 = **브론즈 2판** `bronze/phub-ledger/`({bro['date']} · HASHES.txt 21 전부 일치 · 1판과의 차이 = CHANGELOG 6곳) + 조사 산출물 step1 10-29 · 발주서 `erd-v3.1-brief.md`(사용자 승인 2026-11-05 「3.1 진행」 · 변경 6건) + 코디·사용자 추가 4건(V3.1-7 동의서 · V3.1-8 안전 문구 수식어 · V3.1-9 사용자 정의 2 개정 · V3.1-10 문구 사전/부록 · 2026-11-05) · 근거 `ERD-V3-CANDIDATES.md` v3.1 후보 · `silver-v3/out/report.md` §13 · batch3-proposed EXO-02/05/06 · 동결 v3(`ERD-FROZEN.md`)의 **사용자 정의 1·3 과 명시 예외의 논리는 그대로, 정의 2 는 사용자 결정으로 개정** · 이전 발주서(v1 ~ v3)의 입력·금지·기준·질문 기본값·처분 유지")
    A("")
    A(f"기계용 동본 `erd-v3.1.json` · 값 사전 `erd-v3.1-dictionaries.json`(v3 47 + `person_condition` + `phrase_dictionary` = {len(dic_json['dictionaries'])} · 값 변경 0 · 제거 이력 필드) · 잎 키 행선지 `erd-v3.1-column-map.md`(v3 대비 이동 {len(moves31)} · 비고 변경 {len(notes31)}) · 분해 규칙 실행 `erd-v1.1-resolve.py`(§9.2) · 튜플·단위·문구·조건 실측 `erd-v3.1-tuples.py`(결과 `erd-v3.1-tuples.json`, §9.5·§9.6 v3 와 나란히 + 신설 §9.5.12~13 · §9.6 전면 · §9.7 · §9.8) · 검산 `erd-v3.1-check.py` (결과 §10). 이전 판 산출물은 그대로 두었다. **v3 → v3.1 변경 목록(V3.1-# 대응)은 §11**, v3.1 밖 관찰은 §12.")
    A("")
    A("**v3.1 의 범위는 변경 10건뿐이다.** " + " · ".join(f"**{a}** {b}" for a, b, c in S.CHANGE_LIST_V31) + f". **개체 {len(S.ENTITIES)}(v3 21 − adverse_expression) · 관계 {len(S.RELATIONS)}(v3 31 − R29 + R32) · 사전 {len(dic_json['dictionaries'])}(+person_condition · +phrase_dictionary) · 결정 kind {len(S.DECISION_KINDS)} · 행선지 1,072(이동 {len(moves31)})** — 그 밖 개체·관계·규칙은 v3 그대로. 사전 값·동의어·매핑·접힘 승인·충돌 판정은 결정 레코드이며 ERD 를 열지 않는다(ERD-FROZEN) — v3.1 이 사전에 더한 것은 구조가 요구한 조건 사전과 분해가 쓰는 문구 사전뿐(기존 47 사전의 값은 불변 · 검산 N-11).")
    A("")
    A("### 0. 사용자 정의 3 · 명시 예외 (ERD-FROZEN 동결 원문 · v3 승계 · **v3.1 개정(정의 2 · 사용자 결정 2026-11-05)**)")
    A("")
    A("동결 원문(ERD-FROZEN 동결 조건 · 글자 그대로):")
    A("")
    for n, t in S.USER_DEFINITIONS:
        A(f"{n}. {t}")
    A("")
    A("v3 승계 문장(R-4):")
    A("")
    for n, t in S.USER_DEFINITIONS_V3:
        A(f"{n}. {t}")
    A("")
    A("**v3.1 문장(정의 2 는 사용자 결정으로 개정 · 정의 3 은 kind 20 · 적용 ⓪①):**")
    A("")
    for n, t in S.USER_DEFINITIONS_V31:
        A(f"{n}. {t}")
    A("")
    A(f"**명시 예외(사용자 결정 2026-11-04 · 동결 원문)**: {S.EXPLICIT_EXCEPTION}")
    A("")
    A(f"**명시 예외(v3.1 개정 · 사용자 결정 2026-11-05)**: {S.EXPLICIT_EXCEPTION_V31}")
    A("")
    A(f"**v3.1 과 정의의 관계**: {S.USER_DEFINITIONS_V31_NOTE}")
    A("")
    A("**원칙(v2.4 A~C 그대로 · D 는 v3.1 문장)**: " + " ".join(f"**{k}.** {v}" for k, v in S.PRINCIPLES))
    A("")
    A("v2.4 원칙 D 원문(참고): " + dict(S.V3.PRINCIPLES)["D"])
    A("")
    A("## 1. 범위와 층")
    A("")
    A("| 층 | 무엇 | 규칙 |")
    A("|---|---|---|")
    A(f"| 브론즈 | 원장 21개 JSON(**브론즈 2판** `bronze/phub-ledger/` · 원장의 집) + `step1-products.json`(조사 산출물) | 바이트 보존·수정 금지. 파일 SHA256 이 식별자(§6 표 · HASHES.txt). 1판 = `phub-stg-2026-10-26/` · 2판 = 1판 복사 + CHANGELOG(부위 나열 `/` → `+` 6곳 · {bro['date']}) |")
    A("| 시맨틱 | 이 ERD + 값 사전 + **문구 사전**(v3.1) + 분해 규칙(참조 §1.3 · 튜플 §1.4 · 단위 §1.5 · 조건 §1.6) | 문서. 사용자 승인이 정본 조건. 버전으로 개정(v1 → … → v3(동결) → v3.1 → …) |")
    A("| 실버 | ERD 를 따르는 정규화 레코드 | **모든 값은 (파일, 잎 키 경로) 출처를 가진다.** 출처 없는 값 금지. 충돌은 둘 다 보관. v3.1: 원장 문구·조건 문장은 개체가 아니라 엣지·단위의 **부록**(source_phrases · phrases · explanations) 또는 게이트 목록(unlinked_phrases) |")
    A("| 골드 | 실버 조합 뷰 | 실버에 없는 사실을 만들지 않는다. 충돌 미판정 레코드 제외. v3.1: 동의서 뷰(계열별 고지 R32 + R16 금기 + 응급 징후 문구 R15)는 골드에서 조립 가능하다 |")
    A("")
    A("지식은 원장 21(2판)·컬럼 리포트·스캔 결과·erd-v* 산출물·발주서·검토서·`step1-products.json`·`ERD-FROZEN.md`·`ERD-V3-CANDIDATES.md`·`silver-v3/out/report.md` §13·`silver-v3/README.md`·`silver-v3/decisions/batch3-proposed/DEC-*-EXO-0{2,5,6}.json`·`silver-v3/tests/enumerate_cases.py`(읽기만) 에서만 가져왔다. step2·step3·source-map·DATA-001·DEC-*·silver-*(위 예외 제외)·silver-v3/lib·`_archive/` 는 열지 않았다.")
    A("")
    A("### 1.1 정규화(「같은 것」판정)와 식별자")
    A("")
    A(f"- 정규화 `{S.NORMALIZE_RULE['name']}`: " + " → ".join(S.NORMALIZE_RULE["steps"]))
    A(f"- {S.NORMALIZE_RULE['note']}")
    A(f"- 식별자: `{S.ID_RULE['format']}`. canonical_key 는 개체별(§2 각 표의 「식별자」). {S.ID_RULE['canonical_key']}")
    A(f"- survey 제품: {S.ID_RULE['survey_products']}")
    A(f"- 제품(v3.1 · V3.1-1): {S.ID_RULE['product']}")
    A(f"- 사전 항목 id(v3 · R-2): {S.ID_RULE['dictionary_entry']}")
    A(f"- **튜플·단위 식별자** — procedure(v2.2 · v3 #s<i>): `{S.ID_RULE['procedure']}` · reference anchor: {S.ID_RULE['reference']} · **adverse_effect(v3.1 · 세 칸)**: `{S.ID_RULE['adverse_effect']}` · **person_condition(v3.1)**: {S.ID_RULE['person_condition']} · **문구 사전 항목(v3.1)**: {S.ID_RULE['phrase']} · clinical_rule(v3.1): {S.ID_RULE['clinical_rule']} · catalog_item(v2.4 계열 코드 고정): {S.ID_RULE['catalog_item']} · 표현(v3.1): {S.ID_RULE['adverse_expression']} · 문구 후보: {S.ID_RULE['adverse_expression_candidates']}")
    A(f"- **접힘 조건(v2.2 · 문자 그대로): 「{S.FOLD_CONDITION}」** — {S.FOLD_RULE}.")
    A(f"- **부작용 접힘 조건(v3.1)**: {S.ADVERSE_FOLD_RULE}.")
    A(f"- **원장 locator(v2.3)**: {S.LOCATOR_RULE}.")
    A(f"- **결정 target(v3.1)**: {S.DECISION_TARGET_RULE}. 충돌: {S.ID_RULE['conflict_decision_ids']}.")
    A("- 「같은 것」 = 정규화 완전 일치(①) + 사전 동의어(②)만 자동. 참조·문구·조건 문자열은 분해 규칙으로 조각내어 조각 단위로 같은 판정을 한다. 튜플·단위는 조각이 가리키는 개체·사전 값의 조합이 같을 때 같은 것이다. 유사도·추측 매칭은 ⑦ 후보로만.")
    A("")
    A("### 1.2 다이어그램 (개체·관계만)")
    A("")
    A("```mermaid")
    A(mermaid())
    A("```")
    A("")
    A("### 1.3 참조 해결 — 결정론 분해 규칙 (v1.1 B · v3 stopwords·회사 괄호·조합 기호 · **v3.1 회·차 자리 · stopwords 겹침**)")
    A("")
    R = S.RESOLVE_RULES
    A("v1.1 의 세 단계를 **데이터**(`erd-v3.1.json → resolve_rules`)로 적고 `erd-v1.1-resolve.py`(§9.2)와 `erd-v3.1-tuples.py`(§1.4)가 그대로 실행한다. v3.1: 2단계 stopwords 에 session_rule(V3.1-5)·overlap(V3.1-6). 유사도·추측은 없다.")
    A("")
    A(f"1. **계열 확정** — {R['step1_family']['what']}. 자리별 힌트: " + " · ".join(f"{k}: `{v}`" for k, v in R["step1_family"]["slot_hints"].items()) + f". 코드 정규식 `{R['step1_family']['code_regex']}`")
    A(f"2. **이름 분해** — 괄호 안을 뗀다(`{R['step2_decompose']['paren_regex']}`). 조합 기호 `{'` `'.join(R['step2_decompose']['combo_symbols'])}` 로 멤버를 나눈다(기호 뜻: " + " · ".join(f"`{k}` {v}" for k, v in R["step2_decompose"]["combo_symbols_meaning"].items()) + f"). 조각마다 사전 순서 **{' → '.join(R['step2_decompose']['dictionary_order'])}**(procedure = catalog_item_name) 로 완전 일치를 시도한다. 규격 정규식 `{R['step2_decompose']['spec_regex']}` + unit 사전. {R['step2_decompose']['secondary_rule']}. {R['step2_decompose']['scope_rule']}. {R['step2_decompose']['overlap_rule']}.")
    sw = R["step2_decompose"]["stopwords"]
    A(f"   - **stopwords(v3 · V3-3 · v3.1 V3.1-5/6)**: {sw['rule']} 단어 {len(sw['words'])}: " + " · ".join(f"`{w['word']}`({w['origin']} · locator {len(w.get('locators', []))})" for w in sw["words"]) + f". 회차 `{sw['session_regex']}` → {sw['session_target']} · 횟수 `{sw['count_regex']}` → {sw['count_target']}. 실측 §9.5.10 · §9.5.12")
    A(f"   - **회·차 자리(v3.1 · V3.1-5)**: {sw['session_rule']}")
    A(f"   - **사전 값 겹침(v3.1 · V3.1-6)**: {sw['overlap_rule']} 실측 겹침 {len(sw['overlap'])}: " + (" · ".join(f"`{o['word']}` ↔ " + ", ".join(f"{h['name']}:{h['canonical']}({h['as']})" for h in o["dictionaries"]) for o in sw["overlap"]) or "없음") + " (§9.5.13)")
    A(f"   - **괄호 안 회사·제품(v3 · V3-2)**: {R['step2_decompose']['company_paren']['rule']} 실측 §9.5.9")
    A(f"3. **조립** — 튜플 ({', '.join(R['step3_assemble']['tuple'])}). (a) resolved: {R['step3_assemble']['resolved']} (b) 분해 성공·항목 없음: {R['step3_assemble']['decomposed']} (c) unresolved: {R['step3_assemble']['unresolved']}")
    A(f"   - **fallback_to_parent = {R['step3_assemble']['fallback_to_parent']}** — {R['step3_assemble']['fallback_to_parent_note']}")
    A(f"   - **조합 기호(v3 · V3-4)**: {R['step3_assemble']['combo']['rule']} 실측 §9.5.11")
    A("")
    A("결과는 §9.2 에 v1 수치와 나란히. (a)·(b) 의 결과는 §1.4 의 튜플 규칙으로 한 번 더 내려가 procedure 튜플이 되고, (c) 미해결은 튜플을 만들지 않는다(미해결 참조의 REF- 도 결정 target). 그 튜플이 곧 엣지의 끝이다(§3 엣지 끝 규칙 · §9.5.8).")
    A("")
    A("### 1.4 시술 튜플 분해 규칙 (구조 변경 ① · v2.2~v2.4 · v3 V3-2~5 · **v3.1 V3.1-5** · 데이터 `erd-v3.1.json → tuple_rules.procedure`)")
    A("")
    P = T["procedure"]
    A(f"- 입력: ① {P['input']['catalog_items']} · ② {P['input']['references']}")
    A(f"- **계열 코드(v2.4 · 검토 3-B′)**: {P['cat_family']}")
    A(f"- 조각: {P['fragments']}")
    A(f"- **stopwords(v3 · v3.1)**: {P['stopwords']}")
    A(f"- **회·차(v3.1)**: {P['session']}")
    A(f"- **괄호 안 회사·제품(v3)**: {P['company_paren']}")
    A(f"- **조합(v3 · 확정)**: {P['combo']}")
    A(f"- fallback_to_parent: **{P['fallback_to_parent']}** (v2.1) · technique_inheritance: **{P['technique_inheritance']}** (v2.2 · V3-8) · fold_condition: **{P['fold_condition']}** (v2.2)")
    A(f"- 접힘(v2.2): {P['fold_rule']}")
    A("- what(필수) — v2.2 규칙 + v3:")
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
    A("### 1.5 부작용 단위·문구 규칙 (구조 변경 ② · v2.3/v2.4 원칙 · v3 V3-1 수식 칸·V3-5 조직층 · **v3.1 V3.1-8 수식어 · V3.1-9 단위 세 칸·경과 엣지 · V3.1-10 문구 사전** · 데이터 `erd-v3.1.json → tuple_rules.adverse`)")
    A("")
    Q = T["adverse"]
    A(f"- **원칙(v3.1 문장)**: {Q['principles']}")
    A(f"- 입력: {Q['input']['complications']} · 문구: {Q['input']['phrases']}")
    A(f"- **단위(v3.1 · V3.1-9)**: {Q['unit']}")
    A(f"- 분해: {Q['split']}")
    A(f"- 단위 후보: {Q['tuple']}")
    A(f"- **경과(course) 규칙(v2.3 · v3.1 엣지)**: {Q['course']}")
    A(f"- **부위(site) 규칙(v2.4 · v3.1 상대 부위 none)**: {Q['site']}")
    A(f"- **수식(qualifier) 규칙(v3 · V3-1)**: {Q['qualifier']}")
    A(f"- **접힘 조건(v3.1)**: {Q['fold_rule']}")
    A(f"- **raw_name 단위(v2.4 · v3.1 칸)**: {Q['raw_name']}")
    A(f"- **안전 문구 수식어 목록(v3.1 · V3.1-8)**: {Q['adverse_stopwords']['rule']} 단어 {len(Q['adverse_stopwords']['words'])}(class 별 " + " · ".join(f"{k} {n}" for k, n in Counter(w['class'] for w in Q['adverse_stopwords']['words']).items()) + f") · 패턴 {len(Q['adverse_stopwords']['patterns'])}. 목록·locator 전수 §9.6.9.")
    A(f"- **문구 사전(v3.1 · V3.1-10)**: {Q['phrase_dictionary']}")
    A(f"- **phrase_shape(v3.1)**: {Q['phrase_shape']}")
    A(f"- **필수 고지(v3.1 · V3.1-7)**: {Q['disclosure']}")
    A(f"- 타임라인 normal: {Q['normal_phrases']}")
    A(f"- 문헌: {Q['literature']} v3.1: statement 와 patient_ko 는 각각 문구 사전 항목(각자 판정) · patient_en/zh/ja 는 statement 항목의 translations[].")
    A(f"- 원장 locator: {Q['locator']}")
    A(f"- 식별자: `{Q['id']}` · 상태: {Q['status']}")
    A("")
    A("### 1.6 사람 조건 분해 규칙 (**v3.1 신설 · V3.1-4** · 데이터 `erd-v3.1.json → tuple_rules.condition`)")
    A("")
    Cn = T["condition"]
    A(f"- 입력: {Cn['input']['names']} · 사전: {Cn['input']['dictionary']}")
    A(f"- **규칙**: {Cn['rule']}")
    A(f"- 분해: {Cn['split']}")
    A(f"- 표지어 {len(Cn['markers'])}: " + " · ".join(f"`{m['word']}`(locator {len(m['locators'])})" for m in Cn.get("markers_measured", [{'word': w, 'locators': []} for w in Cn['markers']])) + ". 동의어 규칙: " + " / ".join(Cn["synonym_rules"]))
    A(f"- 접힘 조건: {Cn['fold_condition']} · 식별자: {Cn['id']} · 문장: {Cn['phrases']} · 유사도 {Cn['no_similarity']} 금지 · 조사 분리 {Cn['particle_split']}")
    A("- 실측 §9.7.")
    A("")
    A("## 2. 개체 목록")
    A("")
    A(f"개체 {len(S.ENTITIES)}개 — v3 21 에서 `adverse_expression` 을 뺐다(V3.1-10 · 문구는 개체가 아니라 문구 사전 항목·부록). v3.1 에서 바뀐 것: `product`(reclassified_from · V3.1-1) · `modality`(mandatory_disclosures 속성 삭제 · V3.1-7) · `adverse_effect`(세 칸 · 경과 없음 · relative_site_text · created_by_phrase · explanations — V3.1-9/10) · `person_condition`(사전 단위 식별 · phrases[] 부록 — V3.1-4) · `clinical_rule`(kind disclosure·product_note · source_locator · modality_codes · phrase_ids — V3.1-2/7) · `decision`(kind 20) · `evidence_statement`·`conflict`(정의 한 줄). 그 밖은 v3 그대로.")
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
    A(f"관계 {len(S.RELATIONS)}개 — v3 31 에서 R29 expresses 를 빼고(V3.1-10) R32 rule_applies_to 를 더했다(V3.1-2). v3.1 에서 바뀐 것: **R12** session_count(V3.1-5) · R9/R17/R18 qualifier_text 비고 · **R15** course(엣지 속성 · V3.1-9) · source_phrases·degree/timing/incidence/condition 참조·created_by_phrase·disclosure(V3.1-10/7) · R16/R17/R18 source_phrases · 조건 단위 끝(V3.1-4) · R19 from · R20 to(V3.1-10) · R30/R31 세 칸 · R3/R4/R27 product_reclassify 비고. "
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
    A("v3.1: `adverse_expression.*` 열거형 키는 문구 사전 항목의 kind·status·사유를 뜻한다(개체는 없다 · 키 이름은 적합성 열거기 `tests/enumerate_cases.py` 의 정적 목록과 맞추려 유지). `phrase_dictionary.*` 가 같은 값의 정식 이름.")
    A("")
    A(md_table(["열거형", "값"], [(k, ", ".join(v)) for k, v in S.ERD_ENUMS.items()]))
    A("")
    A("## 4. 값 사전 목록")
    A("")
    nval = sum(1 for d in dic_json["dictionaries"] if d.get("kind", "value") == "value")
    nidx = sum(1 for d in dic_json["dictionaries"] if d.get("kind", "value") == "entity_name_index")
    nphr = sum(1 for d in dic_json["dictionaries"] if d.get("kind") == "phrase_index")
    A(f"전부 `erd-v3.1-dictionaries.json` — v3 47 + **`person_condition`(V3.1-4 · 조건 사전)** + **`phrase_dictionary`(V3.1-10 · 문구 사전 · 분해 결과)** = {len(dic_json['dictionaries'])} (값 사전 {nval} + 개체 이름 색인 {nidx} + 문구 색인 {nphr}). **기존 47 사전의 값·동의어·순서는 v3 과 같다**(검산 N-11). 모든 사전에 제거 이력 필드 removed_synonyms[]/removed_entries[](V3.1-3 · 지금 adverse_event_type 「공기색전」 1건 = v3 가 ERD 로 뺀 것 · by=ERD v3).")
    A("")
    A(md_table(["사전", "종류", "라벨", "정준값", "동의어", "후보", "출처 키"], [(d["name"], d.get("kind", "value"), d["label"], len(d["entries"]), sum(len(e["synonyms"]) for e in d["entries"]), len(d["candidates"]), ", ".join(sorted({f"`{s['file']}:{s['path']}`" for e in d["entries"] for s in e["sources"]} | {f"`{s['file']}:{s['path']}`" for e in d["entries"] for sy in e["synonyms"] for s in sy["sources"]})[:6]) + (" …" if len({(s['file'], s['path']) for e in d["entries"] for s in e["sources"]}) > 6 else "")) for d in dic_json["dictionaries"]]))
    A("")
    A("사전 하나에 비고가 있는 것:")
    A("")
    for d in dic_json["dictionaries"]:
        if d.get("note"):
            A(f"- `{d['name']}`: {d['note']}")
    A("")
    A("### 4.1 사건 사전(adverse_event_type) 전체 — 값 · 분류 · 동의어 · 출처 횟수 · 제거 이력")
    A("")
    de = D["adverse_event_type"]
    A(md_table(["#", "사건", "category", "동의어(표기 변형)", "65 이름 중 출현", "분류 확인 필요", "v3 제거 동의어"], [(i + 1, e["canonical"], e["category"], ", ".join(s["value"] for s in e["synonyms"]) or "—", e["sources"][0]["n"], "○" if e.get("category_review") else "", ", ".join(x["value"] for x in e.get("v3_removed_synonyms", [])) or "") for i, e in enumerate(de["entries"])]))
    A("")
    A(f"제거 이력(removed_synonyms · V3.1-3): " + (" · ".join(f"「{x['value']}」(정준값 {x['canonical']} · by {x['by']} · {x['removed_at']})" for x in de.get("removed_synonyms", [])) or "없음"))
    A("")
    A("### 4.2 경과 사전(course) · 상대 부위 사전(relative_site) · 수식 사전(adverse_qualifier) · 부위 사전 kind")
    A("")
    A(f"- **경과 규칙(v2.3 · v3.1 엣지 속성)**: {Q['course']}")
    A("- `course`: " + " · ".join(f"{e['canonical']}(동의어: {', '.join(s['value'] for s in e['synonyms']) or '—'})" for e in D["course"]["entries"]) + " — v3.1: 단위 칸이 아니라 R15.course")
    A("- `relative_site`: " + " · ".join(f"{e['canonical']}(동의어: {', '.join(s['value'] for s in e['synonyms']) or '—'})" for e in D["relative_site"]["entries"]) + " — v3.1: 단위 부위 칸은 none · relative_site_text 보존")
    A(f"- `adverse_qualifier`: " + " · ".join(f"{e['canonical']}({e['kind']})" for e in D["adverse_qualifier"]["entries"]))
    A(f"- `site` kind: " + " · ".join(f"{k} {n}" for k, n in Counter(e.get("kind") for e in D["site"]["entries"]).items()) + " — v3.1 단위 부위 칸은 anatomical·layer·region 만")
    A("")
    A("### 4.3 조건 사전(person_condition · **v3.1 · V3.1-4**) 전체 — 값 · kind · 동의어 · 출처 횟수")
    A("")
    dc = D["person_condition"]
    A(f"- 정준값 {len(dc['entries'])} · 동의어 {sum(len(e['synonyms']) for e in dc['entries'])} · kind 분포 {dict(Counter(e.get('kind') for e in dc['entries']))} · 값·동의어 전부 derived(사람 조건 이름 9 키 값의 부분 문자열). 실측 §9.7.0: 쓰인 값 {cs['dictionary_values_used']}/{cs['dictionary_values']}.")
    A("")
    A(md_table(["#", "정준값", "kind", "동의어", "출처(파일:키 · 횟수)", "비고"], [(i + 1, e["canonical"], e.get("kind"), ", ".join(s["value"] for s in e["synonyms"]) or "—", " · ".join(f"`{s['file'].split('.')[0]}:{s['path'].split('.')[-1]}`×{s['n']}" for s in e["sources"]), e.get("note", "")[:90]) for i, e in enumerate(dc["entries"])]))
    A("")
    A("### 4.4 문구 사전(phrase_dictionary · **v3.1 · V3.1-10**) — 요약 (항목 전부는 §9.6.12)")
    A("")
    pd_ = D["phrase_dictionary"]
    A(f"- 항목 {pd_['canonical_count']}(자리 {pd_['occurrences']}) · status {dict(pd_['by_status'])}. {pd_['note']}")
    A("")
    A("## 5. 충돌·결정 개체 정의 + 규칙 ①~⑩ + 신뢰 순위 + 결정 적용 순서")
    A("")
    A("충돌(`conflict`)·결정(`decision`) 개체 정의는 §2. 결정 레코드는 §5.2 의 모양으로 `erd-v3.1.json → decisions` 에 적재한다 — v3 의 26 을 그대로 이관 + v3.1 개정 DEC-27(proposed). 이관 표 §5.3. **결정 target 은 안정 키만(v2.3 · v3 미해결·조합 REF- · v3.1 PRD- alias · CND- 사전 값 · PHR-) · 적용 순서는 §5.4 표(⓪ product_reclassify · ① 에 dictionary_remove · phrase_map).**")
    A("")
    A(md_table(["#", "분류", "규칙"], S.QUALITY_RULES))
    A("")
    A("빈값과 「없음」: 안 적힌 것(키 없음·null·빈 배열·빈 문자열) = null(미입력). 명시적으로 없다고 적힌 것만 빈 목록. step1 의 「확인 불가」·「근거 없음」·「해당 없음」은 값이다(null 아님). "
      "**시술 튜플의 site none·technique none 은 미상이며 식별자 값이 아니다(v2.2)** — 미상 칸이 있으면 식별자에 anchor(CAT-/REF-)를 섞어 항목·참조마다 고유하고 접히지 않는다. "
      "**부작용 단위(v3.1 · 세 칸)**: 미등록 조각이 있거나 사건에 붙지 않은 조각이 남은 이름은 raw_name 단위로 접히지 않고, 접힘은 세 칸 전부 사전 값일 때만 — 부위 none·물질 none 은 명시 예외의 값(식별자에 들어간다) · 경과는 R15 엣지 속성. 문구는 미등록 조각이 섞인 단위를 만들지 않는다(원칙 D). "
      "단계 끝 = 컬럼 행선지 미정 0 · 충돌 미판정(open) 0 — fold_approve 가 접는 쌍의 ⑦ 을 닫고(V3-10), conflict_close 가 나머지를 닫는다 · 문구 unlinked 는 게이트 unlinked_phrases(phrase_map 의 몫).")
    A("")
    A("**규칙 ④ (v2.2 · 사용자 결정으로 유지 + 기록)**: " + S.RULE4 + ".")
    A("")
    A(f"**V3-10**: {S.FOLD_CLOSE_RULE}")
    A("")
    A(f"**V3-9**: {S.DECISION_ANCHOR_RULE}")
    A("")
    A(f"**V3.1-1**: {S.PRODUCT_RECLASSIFY_RULE}")
    A("")
    A(f"**V3.1-3**: {S.DICTIONARY_REMOVE_RULE}")
    A("")
    A(f"**V3.1-10 phrase_map**: {S.PHRASE_MAP_RULE}")
    A("")
    A("### 5.1 원장 신뢰 순위 (파일별 · 21 + step1) — v1.1 그대로 (브론즈 2판도 같은 파일·같은 순위)")
    A("")
    A(md_table(["순위", "파일", "종류", "근거 키", "표시", "비고"], [(t, f"`{f}`", S.SOURCE_KIND[f], b, S.TRUST_FLAGS.get(f, ""), n) for f, t, b, n in sorted(S.SOURCE_FILES, key=lambda x: (x[1], x[0]))]))
    A("")
    s1 = next(fm for fm in erd["source_files"] if fm["file"] == STEP1)
    A(f"`products.json` 의 `products[].mfds` 필드만 2(식약처 허가)로 격상한다. `complications.json` 은 8-1 처분으로 3 유지 + 「AI 컨센서스 추정」. `step1-products.json` 은 조사 산출물: 허가 건 {s1['trust_tier_rule']['tier2_licenses']}/{s1['trust_tier_rule']['licenses_total']} 건의 허가·회사·공식명 필드만 2, 그 밖은 3. v3(V3-7): description·media_refs 를 채울 새 브론즈 원천(조사 파일)도 research_artifact 로 같은 표에 등록하고 locator 를 준다 — 지금은 없다.")
    A("")
    A("### 5.2 결정 kind — 빌드가 읽는 모양 (v2.2 · v2.3 · v2.4 · v3 · **v3.1: product_reclassify ⓪ · dictionary_remove ① · phrase_map ①**)")
    A("")
    A(f"공통 필드: {' · '.join(S.DECISION_COMMON_FIELDS)}. status ∈ {{{', '.join(S.DECISION_STATUS)}}}. **{S.DECISION_BUILD_RULE}.** target·new_value 는 문자열이 아니라 kind 별 구조체다. kind {len(S.DECISION_KINDS)} = v3 17 + v3.1 신설 3(`product_reclassify` · `dictionary_remove` · `phrase_map`). v3.1 에서 비고가 바뀐 kind: " + " · ".join(f"`{k}`({v})" for k, v in S.DECISION_KINDS_NOTE_V31.items()) + ".")
    A("")
    A(f"**target 규칙(v3.1)**: {S.DECISION_TARGET_RULE}.")
    A("")
    A(f"**canonical_rename(V3-6)**: {S.RENAME_RULE}")
    A("")
    A(md_table(["kind", "v2.2 신설", "v2.3 신설·개형", "v3", "v3.1", "빌드 적용", "적용 단계", "target", "new_value", "비고"],
               [(f"`{k}`", "○" if k in S.DECISION_KINDS_NEW else "", "신설" if k in S.DECISION_KINDS_NEW_V23 else ("개형" if k in S.DECISION_KINDS_RESHAPED_V23 else ""), "신설" if k in S.DECISION_KINDS_NEW_V3 else ("비고" if k in S.DECISION_KINDS_NOTE_V3 else ""), "신설" if k in S.DECISION_KINDS_NEW_V31 else ("비고" if k in S.DECISION_KINDS_NOTE_V31 else ""), "○" if br else "기록만",
                 next((st for st, ks, _ in S.DECISION_APPLY_ORDER if k in ks), "⓪" if k in ("reclassification", "product_reclassify") else "—"), t, nv, n) for k, br, t, nv, n in S.DECISION_KINDS]))
    A("")
    A("### 5.3 결정 레코드 — v3 의 26 이관 + v3.1 1 (전부)")
    A("")
    A(md_table(["id", "kind", "target", "new_value", "decided_by", "decided_at", "status", "source_refs"],
               [(d["id"], d["kind"], json.dumps(d["target"], ensure_ascii=False)[:200], json.dumps(d["new_value"], ensure_ascii=False)[:160], d["decided_by"] or "null", d["decided_at"] or "null", d["status"], " · ".join(x["ref"] for x in d["source_refs"])) for d in erd["decisions"]]))
    A("")
    A(f"이관(v3 → v3.1): 26 레코드 전부 모양·값 그대로(파생 id 포함 {sum(1 for m in erd['decisions_migration'] if m['derived_id_in_target'])} · 검산 K-2). DEC-27 은 v3.1 개정 기록(proposed) — ERD 승인 때 decided_by=사용자 · decided_at=승인일 · approved. 실버 결정 묶음(batch1·2A·2B·3)은 실버 저장소에 있고 ERD 는 kind·target 모양만 정한다.")
    A("")
    A("### 5.4 결정 적용 순서 (v2.3 · v3 ① canonical_rename · **v3.1 ⓪ product_reclassify · ① dictionary_remove·phrase_map**)")
    A("")
    A(S.DECISION_APPLY_ORDER_RULE + ".")
    A("")
    A(md_table(["단계", "kind", "왜 이 자리인가"], [("⓪", "`reclassification` / `product_reclassify`", "원장 적재 때 — 분해·R2/R4·엣지가 새 계열을 읽는다(v3.1: product_reclassify 는 PRD- 재계산 · 옛 id alias)")] + [(st, " / ".join(f"`{k}`" for k in ks), why) for st, ks, why in S.DECISION_APPLY_ORDER]))
    A("")
    A("## 6. 원장 파일 21(브론즈 2판) + step1 → 개체 매핑 요약")
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
        rows.append((f"`{f}`", fm["trust_tier"], fm["sha256"][:12], ("2판 ✎" if fm.get("changed_from_v1") else "2판 = 1판") if f != STEP1 else "—", fm["leaf_paths"], main or "—", sub or "—", ", ".join(k.replace("dict:", "") for k in dcts) or "—", f"{len(drops)}: " + ", ".join(f"`{d}`" for d in drops[:3]) + (" …" if len(drops) > 3 else "") if drops else "0"))
    A(md_table(["파일", "순위", "sha256(12)", "브론즈 판", "잎", "주 개체", "부 개체·엣지", "사전", "브론즈만/버림"], rows))
    A("")
    A(f"`step1-products.json` 전체 SHA256 `{s1['sha256']}` · {s1['bytes']} bytes · 항목 {s1['items']} · 잎 키 {s1['leaf_paths']}. 2판 해시는 `bronze/phub-ledger/HASHES.txt` 와 전부 일치(검산 D).")
    A("")
    A("### 6.1 옮긴 키 (v1.1 → v2 이동 표 · v3 → v3.1 이동 표는 column-map 파일)")
    A("")
    A(md_table(["#", "파일", "경로", "v1.1", "v2"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['v1_1']}`", f"`{m['v2']}`") for i, m in enumerate(moves)]))
    A("")
    A("## 7. 질문 25 답 — v1.1 그대로")
    A("")
    A(md_table(["#", "답 (발주서 §6 기본값 적용 · v1.1 개정분 7·8·10·11·14·16·24 유지)"], S.Q25))
    A("")
    A("v3.1 에서 답이 바뀐 질문은 없다. 질문 19(문구 정제)는 v3.1 에서 문구 사전이 정규화형을 들고 원문은 raw_variants 로 보존한다 — 답의 뜻(원문 브론즈 · 정제는 실버 규칙)은 그대로.")
    A("")
    A("## 8. 기본값 재검토 — 처분 결과 (v1.1 그대로)")
    A("")
    A("v1 §8 의 19 건 처분은 v1.1 에서 확정됐고 v2 이후 바꾸지 않는다. 각 건은 결정 레코드(`erd-v3.1.json → decisions` · §5.3, status approved)로 남는다.")
    A("")
    A(md_table(["#", "항목", "처분 주체", "처분(확정)", "반영 위치"], [(f"8-{no}", B.REVIEW[no - 1]["title"], who, what, where) for no, (who, what, where) in S.DISPOSITIONS.items()]))
    A("")
    A("### 8-2 표 — v1 부위 사전 「(확장)」 51 의 처분 (v1.1 그대로)")
    A("")
    A(md_table(["값", "cc_group 횟수", "재배치", "사유"], [(r["value"], r["cc_group_n"], r["dest"], r["reason"]) for r in SITE_TABLE]))
    A("")
    kept = [r for r in SITE_TABLE if r["dest"].startswith("부위")]
    A(f"부위 사전 유지 {len(kept)} · problem_subcategory_label 로 {len(SITE_TABLE) - len(kept)}. 부위 사전 최종 = 뼈대 11 + taxonomy 부위 라벨 {len(kept)} + v3 조직층 5 = **{len(D['site']['entries'])}**.")
    A("")
    A("## 9. ERD 승인 때 사용자가 볼 것")
    A("")
    A("### 9.1 사전 표 (정준값 수 · 동의어 · 후보)")
    A("")
    A(md_table(["사전", "정준값", "동의어", "후보(미연결)"], [(d["name"], len(d["entries"]), sum(len(e["synonyms"]) for e in d["entries"]), "; ".join(c["value"] for c in d["candidates"]) or "—") for d in dic_json["dictionaries"]]))
    A("")
    A("핵심 사전 정준값 전체:")
    A("")
    for name in ["modality", "problem", "site", "technique", "course", "relative_site", "adverse_qualifier", "license_status", "license_kind", "license_state"]:
        d = D[name]
        A(f"- `{name}` ({len(d['entries'])}): " + " · ".join((e["canonical"] + (f"[{e['code']}]" if e.get("code") else "") + (f"({e['kind']})" if name in ("site", "adverse_qualifier") and e.get("kind") else "")) for e in d["entries"]))
    A(f"- `adverse_event_type` ({len(D['adverse_event_type']['entries'])}): " + " · ".join(e["canonical"] + f"[{e['category']}]" for e in D["adverse_event_type"]["entries"]))
    A(f"- `person_condition` ({len(D['person_condition']['entries'])}): " + " · ".join(e["canonical"] + f"({e.get('kind')})" for e in D["person_condition"]["entries"]))
    A(f"- `problem_subcategory_label` ({len(D['problem_subcategory_label']['entries'])}): " + " · ".join(e["canonical"] + f"[{e['code']}]" + ("(부위)" if e.get("is_site") else "") for e in D["problem_subcategory_label"]["entries"]))
    A("")
    A("### 9.2 격리 목록 — 참조 해결, v1 vs v1.1 규칙 (v3.1 · 브론즈 2판으로 재실행)")
    A("")
    A("v1 = 완전 일치만. v1.1 규칙(§1.3 · v1.1 코드 그대로 — stopwords·회사 괄호·조합 기호·회차는 §1.4 실측에서)을 v3.1 사전(조건·문구 사전은 분해가 읽지 않는다)으로 `erd-v1.1-resolve.py` 를 2판 원장에 다시 돌린 수치 — v3 와 같다.")
    A("")
    A(RESOLVE.side_by_side(RES, v1rep))
    A("")
    A(f"합계(부위 사전·step1 제외): 미해결 참조(⑨) v1 **{TOTAL.get('unresolved_v1')}** → v1.1 규칙 **{TOTAL['unresolved_v1_1']}** · 분해 성공·항목 없음 **{TOTAL['decomposed_v1_1']}** · 해결 **{TOTAL['resolved_v1_1']}**.")
    A("")
    A("미해결 사유 상위 조각(전 자리 합산, 사전에 없는 조각 · v1.1 코드 — stopwords 적용 전): " + " · ".join(f"`{f}`×{n}" for f, n in TOTAL["top_untouched_fragments"][:40]))
    A("")
    for k, v in RES.items():
        if v["unresolved_labels"] and not k.startswith("step1"):
            A(f"- **{k}** 미해결 {v['unresolved']}: " + " · ".join(f"`{l}`" + (f"@{h}" if h else "") + "(" + ",".join(u) + ")" for l, h, u, _ in v["unresolved_labels"]))
        if v["decomposed_labels"] and not k.startswith("step1"):
            A(f"- **{k}** 분해 성공·항목 없음 {v['decomposed']}: " + " · ".join(f"`{l}`" + (f"@{h}" if h else "") + f"[{sh}]" for l, h, sh, _ in v["decomposed_labels"]))
    A("")
    st = RES["step1-products.items[] display/ledger/search 이름 → 원장 제품 (395)"]
    shp = Counter(r.get("shape") for r in st["rows"] if r["status"] == "decomposed")
    A(f"step1 395 → 원장 제품 대응(B 규칙만): 대응 {st['resolved']} (원장 제품 59 중 {st['ledger_products_covered']}종, 이름 역할 {st['matched_by']}) · 분해 성공·항목 없음 {st['decomposed']} ({', '.join(f'{k}={v}' for k, v in shp.items())}) · 미해결 {st['unresolved']} → **origin=survey {st['survey_products']}** (그중 step1 active=false {st['inactive_items']}).")
    A("")
    A("질문 14 두 묶음(modality_ref 빈 26 항목 · 8-5 처분 반영, 미배정 0) — v1.1 그대로:")
    A("")
    A(md_table(["고민", "하위분류", "항목", "묶음", "발주서 목록 일치", "범위"], [(r["problem"], r["subcategory"], r["name"], r["bucket"], ", ".join(r["matched"]) or "—", r["scope"]) for r in Q14]))
    A("")
    A("### 9.3 충돌 예상 수 (v1.1 그대로 재계산 · v2.2 rule_ref 열 · v2.3 닫는 kind 열 · v3 fold_approve · v3.1 phrase_map)")
    A("")
    A(md_table(["종류", "rule_ref", "무엇", "건", "닫는 결정 kind(v3.1)"], [(c["kind"], c["rule_ref"], c["what"], c["n"], c["close_kind"]) for c in CONF]))
    A("")
    A("v2.2 규칙 ④: 이 표는 원장 파일 단위 예상이다. v2.3: 모든 conflict 는 stable_key 를 가지며 결정은 그 키로만 가리킨다. v3(V3-10): fold_approve 가 접는 쌍의 ⑦ 을 닫는다. v3.1: 문구 unlinked(게이트 unlinked_phrases)·조건 raw_name 은 ⑧ 미등록 조각 — phrase_map · dictionary_add(person_condition) 의 몫.")
    A("")
    for c in CONF:
        if c["detail"] and isinstance(c["detail"], list):
            A(f"- {c['what']}: " + "; ".join(str(x) for x in c["detail"]))
    A("")
    A(f"합계: value_conflict {sum(c['n'] for c in CONF if c['kind']=='value_conflict')} · duplicate_candidate {sum(c['n'] for c in CONF if c['kind']=='duplicate_candidate')} · unregistered_value {sum(c['n'] for c in CONF if c['kind']=='unregistered_value')} · unresolved_reference {TOTAL['unresolved_v1_1']}(+ step1 모호 {sum(c['n'] for c in CONF if c['kind']=='unresolved_reference')}). 전부 사람 판정 전 `open`.")
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
    A("v2.4: 위 reclassified_to 가 적용돼도(⓪) 그 항목의 CAT- id 는 트리 위치의 계열 코드로 계산한 값 그대로다 — R2 만 바뀐다(§2.4). v3.1: 제품의 계열 교체는 product_reclassify(⓪ · PRD- 재계산 · alias).")
    A("")
    A("### 9.5 시술 튜플 실측 (v3.1 · `erd-v3.1-tuples.py` 실제 실행 · 브론즈 2판 · v3 수치와 나란히 · 숫자는 목표가 아니다)")
    A("")
    A("규칙은 §1.4(v3.1: 회·차 자리 · stopwords 겹침 외에는 v3 그대로 — 시술 축 분해 결과는 v3 과 같다 · 검산 G). 분류 항목은 **자기 이름을 색인에서 제외**하고 분해했다. 접힘 조건은 「" + S.FOLD_CONDITION + "」. v3 열은 `erd-v3-tuples.json` 의 수치.")
    A("")
    A(TUPLES.procedure_md(TUP, v3s))
    A("")
    A("### 9.6 부작용 단위·문구 실측 (구조 변경 ② · **v3.1 V3.1-8/9/10** · `erd-v3.1-tuples.py` 실행 · v3 와 나란히)")
    A("")
    A("규칙은 §1.5(v3.1): 단위 = (사건, 부위, 물질) · 상대 부위는 none · 경과는 R15 엣지 · 부위·경과·수식은 사건이 놓인 멤버 안의 조각만(원칙 C) · 한 칸에 후보가 둘이면 단위 둘(원칙 B) · raw_name 단위는 칸 none/none(원칙 A) · 접힘은 세 칸 전부 사전 값일 때만 · 문구는 정규화형 항목이 되고 조각 전부 사전 값이면 단위를 세운다(auto · 원칙 D 의 v3.1 문장) · 아니면 unlinked 게이트. **숫자는 목표가 아니다.**")
    A("")
    A(TUPLES.adverse_md(TUP, v3a))
    A("")
    A(TUPLES.condition_md(TUP))
    A("")
    A(TUPLES.disclosure_md(TUP))
    A("")
    A("## 10. 검산 결과")
    A("")
    A("행선지 표본 안내: 잎 키 1,072 행 전부의 행선지는 `erd-v3.1-column-map.md`(파일별 표 · 이동 표 · 비고 변경 표)에 있고 검산 A 가 전수를 대조한다 — 「표본 20」은 ERD 산출물이 아니라 독립 검토가 그 표에서 뽑아 만드는 것이다(v2.4·v3 때도 검토서에만 있었다).")
    A("")
    A("`erd-v3.1-check.py` 를 독립 실행한 출력을 그대로 붙였다(같은 폴더에서 `python3 erd-v3.1-check.py`). v3 검산 항목 전부(A~M — v3.1 에서 바뀐 기대값은 항목 안에 적었다) + N v3.1 변경 10건(각각 반영 여부 + 실측 · 검산·실측 스크립트가 실제로 센다) + 적합성 열거기(`silver-v3/tests/enumerate_cases.py`)가 새 kind·관계를 읽는지 + 「사용자 정의 1·3 과 명시 예외 논리 유지 · 정의 2 개정 문장」.")
    A("")
    return "\n".join(o)


def change_log(erd, dic_json, TUP, colrows, v3erd, v3tup, moves31, notes31):
    o = []
    A = o.append
    ps, as_, cs = TUP["procedure"]["summary"], TUP["adverse"]["summary"], TUP["condition"]["summary"]
    v = (v3tup or {}).get("procedure", {}).get("summary", {})
    va = (v3tup or {}).get("adverse", {}).get("summary", {})
    cmp = as_.get("v3_comparison") or {}
    ss = ps["session_summary"]
    sw = ps["stopwords"]
    asw = as_["adverse_stopwords"]
    dsc = as_["disclosures"]
    pb = as_["phrase_buckets"]
    A("## 11. v3 → v3.1 변경 목록 (V3.1-# 대응 · 발주서 6건 + 추가 4건)")
    A("")
    A("| # | 무엇 | 어디서 반영 | v3 | v3.1 (실측) |")
    A("|---|---|---|---|---|")
    pr = TUP["product_reclassify"]
    A(f"| V3.1-1 | 결정 kind product_reclassify(⓪) | {S.CHANGE_LIST_V31[0][2]} | 제품 계열 교체 수단 없음(EXO-02 제안) | kind {len(S.DECISION_KINDS)} · ⓪ 적용 · PRD- 재계산+alias · R4 이동 · 제품 끝 엣지 새 id · 대상 예 {len(pr['examples'])}(" + " · ".join(f"{x['product']} {x['current_id']}→{x['new_id']}" for x in pr["examples"]) + f") · 제품 {pr['products_total']} |")
    rc = TUP["r32_candidates"]
    A(f"| V3.1-2 | 관계 R32 rule_applies_to | {S.CHANGE_LIST_V31[1][2]} | clinical_rule → 제품·기법 관계 없음(EXO-05) | R32(scope · severity · source_locator · decision_id · basis ledger\\|edge_create · target_depth) · clinical_rule kind +product_note · 출처 후보 {len(rc)}(제품 {len({x['product'] for x in rc})} · 키 {dict(Counter(x['key'] for x in rc))}) · 값은 edge_create |")
    rs = dic_json["dictionaries"]
    A(f"| V3.1-3 | 결정 kind dictionary_remove(①) | {S.CHANGE_LIST_V31[2][2]} | 동의어 제거 수단 없음(D-6 · EXO-06) | kind {len(S.DECISION_KINDS)} · 동의어/값 제거(쓰는 레코드 있으면 거부) · 이력 removed_synonyms/removed_entries(사전 {len(rs)} 전부 필드 · 「공기색전」 1 기록) · ① 에서 add·rename 뒤 |")
    A(f"| V3.1-4 | 조건 사전 · 조건 단위 · 문장 부록 | {S.CHANGE_LIST_V31[3][2]} | person_condition 식별 = 문자열 298 · 이소트레티노인 12 문장 흩어짐 | 사전 person_condition {cs['dictionary_values']}(동의어 {cs['dictionary_synonyms']} · 쓰인 값 {cs['dictionary_values_used']}) · 표지어 {len(cs['markers'])} · **이름 {cs['names_distinct']} → 단위 {cs['units_total']}**(kind 포함 {cs['names_distinct_with_kind']} → 사전 단위 {cs['units_dict']} + raw {cs['units_raw']}) · 완전 일치로 접힌 이름 {cs['names_dict']} · raw 이름 {cs['names_raw']} · 접힌 사전 단위(이름 ≥2) {cs['dict_units_with_2plus_names']} · 문장 부록 {cs['phrases']} · 이소트레티노인·레티노이드 문장 {len(cs['isotretinoin'])}(사전 단위로 간 것 {sum(1 for x in cs['isotretinoin'] if x['status'] == 'exact')}) |")
    A(f"| V3.1-5 | 회·차 자리 | {S.CHANGE_LIST_V31[4][2]} | 「회 → count」 문장만 · 속성 자리 없음 | R12 session_count·session_index · R9/R17/R18 qualifier_text · 실측 규격 토큰 {ss['total']}(회 {ss['by_kind'].get('회', 0)} · 차 {ss['by_kind'].get('차', 0)}) → R12.session_index {ss['r12_session_index']} · R12.session_count {ss['r12_session_count']} · qualifier_text {ss['to_qualifier_text']} |")
    A(f"| V3.1-6 | stopwords 겹침 | {S.CHANGE_LIST_V31[5][2]} | 「사전 값과 겹치는 단어는 없다」(분해 사전 7 기준) | 규칙 「통째 일치 먼저 · stopword 는 조각에만」 · 겹침 목록(사전 {sw['dictionaries_checked']} 전수) {len(sw['overlap'])}: " + (" · ".join(f"{o_['word']}↔" + ",".join(h['name'] for h in o_['dictionaries']) for o_ in sw["overlap"]) or "없음") + " · 검산 N-6 |")
    A(f"| V3.1-7 | 필수 고지 → clinical_rule(disclosure) + R32 + 문구 사전 | {S.CHANGE_LIST_V31[6][2]} | modality.mandatory_disclosures 문자열 속성 | 고지 {dsc['n']}(계열 {dsc['modalities']}) → clinical_rule {dsc['distinct_sentences']} · R32(ledger) {dsc['n']} · 문구 사전 항목 {dsc['phrase_entries']}(auto {dsc['auto']} · unlinked {dsc['unlinked']}) · column-map 이동 1 · 동의서 뷰는 골드 |")
    A(f"| V3.1-8 | 안전 문구 수식어 목록 | {S.CHANGE_LIST_V31[7][2]} | 수식어가 미등록 조각(경미한 172 · 후 93 · …) | 단어 {asw['words_total']}(class {dict(asw['by_class'])} · locator 있음 {asw['words_with_locator']}) · 패턴 {len(asw['patterns'])} · 적중 {asw['hits_total']} · 미등록 조각 v3 distinct {va.get('unregistered_distinct')}/총 {va.get('unregistered_total')} → distinct {as_['unregistered_distinct']}/총 {as_['unregistered_total']}(v3.1 은 고지 109 문장 포함 · 총은 줄고 distinct 는 고지의 새 토큰으로 는다) · 조각 분류 전수 {as_['fragment_classes_total']}(분류 밖 {len(as_['fragment_classes_unclassified'])}) |")
    A(f"| V3.1-9 | 사용자 정의 2 개정 — 단위 (사건, 부위, 물질) · 경과는 엣지 | {S.CHANGE_LIST_V31[8][2]} | (사건, 부위, 경과, 수식) · 65 → {va.get('complications_distinct_tuples')} · 단위 {va.get('tuples_total')} | 65 → **{as_['complications_distinct_tuples']}**(사전 {as_['complications_distinct_tuples_dict']} + raw {as_['complications_distinct_tuples_raw']}) · 이름 유래 엣지 {as_['complications_edges']}(course {dict(as_['complications_edge_courses'])}) · 상대 부위 none 단위 {as_['tuples_with_relative_site_text']} · 조합 하나뿐인 사건 {as_['events_with_1_combo']}/{len(as_['event_combo_table'])}(부종 {next((e['combos'] for e in as_['event_combo_table'] if e['event'] == '부종'), '—')}) |")
    A(f"| V3.1-10 | 문구 사전 · 표현 개체/R29 삭제 · 부록 · phrase_map | {S.CHANGE_LIST_V31[9][2]} | 표현 개체 {cmp.get('expressions_v3')}(+환자 설명 {cmp.get('patient_text_records_v3')}) · exact {cmp.get('exact_v3')} · unlinked {cmp.get('unlinked_v3')} · 표현 유래 단위 0 | 문구 자리 {as_['phrase_occurrences_without_disclosure']}(+고지 {dsc['n']}) → 항목 **{as_['phrase_entries']}**(auto {as_['phrase_entries_by_status'].get('auto', 0)} · unlinked {as_['phrase_entries_by_status'].get('unlinked', 0)}) · 자리 auto {as_['phrase_occurrences_by_status'].get('auto', 0)} · 단위 {as_['units_before_phrases']} → {as_['units_after_phrases']}(문구가 세운 조합 {as_['units_created_by_phrases']} · 전부 세 칸 사전 값 {as_['units_created_all_dict']}) · R15 엣지(from, 단위) {as_['edges_total']}(이름 {as_['edges_from_names']} + 문구 {as_['edges_from_phrases']} · 경과 있음 {as_['edges_with_course']}) · **부록 합 {pb.get('edge_attachment', 0)} + {pb.get('unit_explanation', 0)} + {pb.get('gate', 0)} = {sum(pb.values())} = {as_['phrase_occurrences_without_disclosure']}** · 개체 21 → {len(S.ENTITIES)} · 관계 31 → {len(S.RELATIONS)} · kind phrase_map |")
    A(f"| — | 결정 레코드 | §5.3 | 26 | 26 이관 + DEC-27(v3.1 개정 · proposed) = {len(erd['decisions'])} |")
    A(f"| — | 행선지(column-map) | — | — | 이동 {len(moves31)}(고지 1 + 표현 28) · 비고 변경 {len(notes31)} |")
    A(f"| — | 사전 | §4 | 47 | **{len(rs)}**(+person_condition · +phrase_dictionary) · 기존 값 불변(검산 N-11) |")
    A(f"| — | 실측 시술 | §9.5 | 521 → {v.get('catalog_distinct_tuples')} · 튜플 {v.get('tuples_total')} · 엣지 끝 {v.get('edge_ends_total_n')} | 521 → {ps['catalog_distinct_tuples']} · 튜플 {ps['tuples_total']} · 엣지 끝 {ps['edge_ends_total_n']}(v3 과 같다 · 회·차는 속성만) |")
    A("| — | 생성기·검산 | — | `*_v3.py` · `erd-v3-tuples.py` · `erd-v3-check.py` | `erd_spec_v31.py`·`erd_colmap_v31.py`·`erd_build_v31.py` · `erd-v3.1-tuples.py` · `erd-v3.1-check.py`(v3 항목 전부 + N) |")
    A("")
    A("**사용자 정의·명시 예외**: 정의 1·3 과 명시 예외의 논리는 그대로(§0 동결 원문 · 검산 N-12). 정의 2 는 사용자 결정(2026-11-05)으로 개정 — 단위 (사건, 부위, 물질) · 상대 부위 none · 경과는 R15 엣지 · 표현은 가리키기만(문구 사전 · 부록 · 미등록 조각이 섞인 단위 0). 명시 예외는 「부위 none · 물질 none 은 값」. 원칙 D 문장 개정.")
    A("")
    A("**검토 반영 S-1~S-5**(`erd-v3.1-review.md` · 판 번호 v3.1 그대로 · 개체·관계·kind 변경 없음): S-1 R15.course 는 항목 전체 parsed.courses 가 아니라 그 단위 후보 parsed.candidates[].courses(이름은 그 사건 멤버의 경과)에서만 — 실측 재실행(R15 course 분포 §9.6.4) · 검산 N-9 에 멤버 수준 검사(「주사 부위 일시적 부종 및 멍」의 멍 엣지 null) · S-2 §1.5 수식 규칙·json qualifier_rule·tuple_rules.adverse.qualifier 를 세 칸으로(course_id·네 칸 exact 잔재 0) · S-3 R29·adverse_expression·경과 칸 잔재 제거(다이어그램 · §1.5 normal · §2.14 aliases/site_ref_id/all_dict_values · dictionary_remove in_use · §2.15 번호 · §9.5.8 자리 라벨) · S-4 §0 명시 예외 예문(멍은 (멍, none, none)) · S-5 §1.1 PHR- 안정 키 조건(경과·수식어·사전 변경 → raw_variants 재귀속 · 옛 id alias) · 「지속」 stale 문장 삭제 · R15.course 비고에 경과 값 집합 = course 사전(DICT-COURSE-01 로 확장).")
    A("")
    A("**v2.4 「두 쪽 전부」 문헌 규칙**: v3.1 은 문구 사전이 정규화형 단위라 statement(영문)와 patient_ko(한글)를 각각 항목으로 두고 각자 판정한다 — 레코드 단위의 「both」 규칙은 사라진다(statement 항목은 영문 토큰이 미등록이라 대개 unlinked · patient_ko 항목이 닿는다 · 번역 en/zh/ja 는 statement 항목의 translations 이며 그 레코드가 닿은 단위의 explanations 부록).")
    A("")
    A("## 12. v3.1 밖 관찰 — 결정 레코드로 갈 것 · 다음 판 후보 (이번 범위 아님 · 레코드는 만들지 않았다)")
    A("")
    unreg_top = ", ".join(f"{f}×{n}" for f, n in cs["unregistered_top"][:8])
    adv_top = ", ".join(f"{f}×{n}" for f, n in as_["unregistered_all"][:10])
    rows = [
        ("V3.1-4 후속", f"raw_name 조건 {cs['units_raw']} 의 미등록 조각 상위({unreg_top}) — 조사가 붙은 토큰(「자가면역질환이」「감염이」) 이 가장 큰 원인 · 완전 일치 원칙상 ERD 가 조사 분리를 하지 않으므로 dictionary_add(person_condition · 동의어 = 조각 또는 원문 전체)로 접는다 · 「심장박동기 ↔ 심박조율기」「레이노 현상 ↔ 레이노 증후군」「G6PD 결핍 ↔ 결핍증」 같은 뜻 병합도 결정 · kind 를 식별자에서 빼면(발주서 「(+ kind)」) 「자가면역 질환」 1건이 합쳐진다 — 사용자 결정", "dictionary_add(person_condition) · scope_review(식별자 kind)", "§9.7.0"),
        ("V3.1-4 후속", "조건의 「범위」 괄호(「켈로이드 체질(박리성 레이저)」「탈장 여부 (복부 시술 시)」)는 시술 축 조각인데 지금은 미등록 → raw_name. 괄호 안이 §1.3 으로 proc_axis 에 닿으면 R16.applies_when 속성으로 올리는 규칙은 다음 판 후보", "scope_review", "§9.7.0 접힌 표"),
        ("V3.1-8 후속", f"수식어 목록 밖 미등록 조각 상위({adv_top}) — 사건·부위 후보(홍조 · 손상 · 알레르기 · 건조감 …)는 dictionary_add(adverse_event_type · site) · 조사 결합 토큰(멍이 · 피부가 · 부위가)은 완전 일치 원칙상 목록에 못 넣는다 · 「이상」(감각 이상 vs 24시간 이상)처럼 뜻이 둘인 토큰은 목록 밖 · 빈도 <4 수식어(뚜렷한 …) 추가는 규칙 데이터 개정", "dictionary_add · 규칙 데이터 개정", "§9.6.5 · §9.6.9"),
        ("V3.1-8 후속", "「지속」은 승인된 실버 결정 DICT-COURSE-01(dictionary_add · course · ①)로 들어온다 — 적용 뒤 「지속」「지속적」「잔여」「점진적으로 커지는」은 경과로 읽히고 그 문구의 정규화형(PHR-)이 갈린다(§1.1 안정 키 조건 · raw_variants 재귀속). 남는 것: 「경결감」 동의어 · course 「미상」 값(엣지 null 이라 뜻 없음) 제거 · 수식어 목록에서 지속/지속적 제거 · 「일시적으로」「일시적인」 경과 동의어 추가", "dictionary_add · dictionary_remove · 규칙 데이터", "§9.6.9 · 검토 ③"),
        ("V3.1-9 후속", "절대 부위가 「시술 자리와 무관」한지는 ERD 가 판정하지 않는다 — 사전 site 의 anatomical·layer·region 조각은 전부 단위 칸(이마/눈가 당김감 → 단위 4 · 혈관 폐색(미간·코) → 2). 시술 자리와 같은 절대 부위를 none 으로 접을지는 결정(fold 는 세 칸이 달라 불가 · adverse_tuple_assign/phrase_map 으로 지정)", "adverse_tuple_assign · phrase_map", "§9.6.10"),
        ("V3.1-10 후속", f"unlinked 문구 항목 {as_['phrase_entries_by_status'].get('unlinked', 0)}(자리 {as_['phrase_occurrences_by_status'].get('unlinked', 0)}) 은 게이트 unlinked_phrases — phrase_map 결정 묶음의 자리 · 사유 {dict(as_['phrase_unlinked_reasons'])} · 고지 109 는 전부 unlinked(긴 문장 · 미등록 토큰) → 고지의 부작용 조각 연결은 phrase_map 으로", "phrase_map", "§9.6.3 · §9.8"),
        ("V3.1-10 후속", "문구 사전 항목 id PHR- 는 정규화형 유도라 수식어 목록이 바뀌면 바뀔 수 있다(규칙 데이터 개정 = ERD 개정) · approved 항목의 이관 규칙(옛 정규화형 → 새 정규화형 alias)은 다음 판", "scope_review", "§1.1"),
        ("V3.1-2 후속", "제품 note 규칙 문장 후보 14 중 어느 것이 규칙인지(「화장품 허가. 주사/주입 사용 금지」 → severity prohibited · R32 to 엑소좀 제품·기법 주사) · severity 열거(prohibited·caution·info)는 v3.1 기본값 — 사용자 확인", "edge_create(R32) · scope_review", "§9.7.2"),
        ("V3.1-7 후속", "pre-procedure-checklist checks[].label 의 규칙 문장(「— 대기 원칙」류)을 clinical_rule 로 올릴지 — 지금은 조건 단위(check)의 raw_name · 같은 문장이 조건이면서 규칙", "scope_review", "§9.7.0"),
        ("적합성 열거기", "tests/enumerate_cases.py 의 RESULT_ENUMS·RULE_ROOTS 는 정적 목록 — v3.1 의 tuple_rules.condition · phrase_dictionary.* 열거형은 열거되지 않는다(열거기 개정 몫 · ERD 는 adverse_expression.* 키 이름을 유지해 깨지지 않게 했다)", "silver-v3/tests 개정", "§10 N-13"),
        ("동결 §12 승계", "v3 §12 의 V3-1~8 후속·동결 승계 항목은 그대로(사전 값·동의어·매핑은 결정)", "v3 §12 그대로", "결정 레코드"),
    ]
    A(md_table(["어디", "무엇", "decision kind / 자리", "근거"], rows))
    A("")
    A("전부 kind 와 target 자리가 정해진 목록이다 — v3.1 의 kind 20 과 안정 키 규칙(미해결·조합 REF- · PRD- alias · CND- 사전 값 · PHR-)으로 전부 담긴다.")
    return "\n".join(o)


def main():
    v1erd = json.load(open(os.path.join(WORK, "erd-v1.json"), encoding="utf-8"))
    v11erd = json.load(open(os.path.join(WORK, "erd-v1.1.json"), encoding="utf-8"))
    v3erd = json.load(open(os.path.join(WORK, "erd-v3.json"), encoding="utf-8"))
    v3tup = json.load(open(os.path.join(WORK, "erd-v3-tuples.json"), encoding="utf-8"))
    bronze = B3.bronze_meta()
    assert not bronze["mismatch"], f"브론즈 2판 HASHES.txt 불일치: {bronze['mismatch']}"
    rescan = B3.rescan_v2()
    step1_scan = B11.scan_step1()
    colrows = _build_column_map(step1_scan)
    dicts = build_dictionaries_v31()
    erd, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, moves, moves22, moves23, moves24, moves3, moves31, notes31, dic_json = write_outputs(colrows, dicts, step1_scan, v1erd, v11erd, v3erd, v3tup, bronze, rescan)
    md = build_erd_md(erd, colrows, dicts, dic_json, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, v1erd, moves, v3tup, moves31, notes31)
    cl = change_log(erd, dic_json, TUP, colrows, v3erd, v3tup, moves31, notes31)
    open(os.path.join(WORK, OUT["md"]), "w", encoding="utf-8").write(md + "(검산 실행 중)\n\n" + cl + "\n")
    chk = load_module("chk31", os.path.join(WORK, OUT["check"]))
    ok, report = chk.run_checks()
    md += report + "\n\n" + cl + "\n"
    open(os.path.join(WORK, OUT["md"]), "w", encoding="utf-8").write(md)
    with open(os.path.join(WORK, OUT["cmap"]), "a", encoding="utf-8") as f:
        f.write("## 검산 결과\n\n" + report + "\n")
    print("OK" if ok else "FAIL")
    print(report)
    ps, as_, cs = TUP["procedure"]["summary"], TUP["adverse"]["summary"], TUP["condition"]["summary"]
    print("dests", Counter(r["dest"] for r in colrows), "moves31", len(moves31), "notes31", len(notes31))
    print("dicts", len(dic_json["dictionaries"]), "entities", len(S.ENTITIES), "relations", len(S.RELATIONS), "decisions", len(erd["decisions"]), "kinds", len(S.DECISION_KINDS))
    print("adverse: 65 ->", as_["complications_distinct_tuples"], "| units", as_["units_before_phrases"], "->", as_["units_after_phrases"], "| phrases", as_["phrase_occurrences"], "entries", as_["phrase_entries"], as_["phrase_entries_by_status"], "| edges", as_["edges_total"])
    print("condition:", cs["names_to_units"])


if __name__ == "__main__":
    main()
