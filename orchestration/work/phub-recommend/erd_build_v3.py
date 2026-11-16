# -*- coding: utf-8 -*-
"""ERD v3 산출물 생성기. v2.4 생성기(erd_build_v24.py)를 바탕으로 발주서 erd-v3-brief.md 의 변경 10건(erd_spec_v3 · erd_colmap_v3 · erd-v3-tuples.py)만 덧씌운다.
입력: 원장 21 = 브론즈 2판 bronze/phub-ledger/(HASHES.txt 검증) + step1-products.json + 스캔 JSON(1판 · 잎 키 집합은 2판과 같음 — 검산 A) + erd_spec_v3/erd_colmap_v3 + erd-v1.json(§9.2) + erd-v1.1.json + erd-v2.4.json·erd-v2.4-tuples.json(§9.5·§9.6 나란히 비교 · 변경 목록 · 결정 이관)
출력: erd-v3.md · erd-v3.json · erd-v3-column-map.md · erd-v3-dictionaries.json · erd-v3-tuples.json(+검산 결과 부착). 이전 판 파일은 지우지 않는다.
"""
import hashlib
import json
import os
import re
import sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_build as B  # noqa
import erd_spec_v3 as S  # noqa

# 원장 = 브론즈 2판. erd_build.L 은 모듈 import 때 1판을 읽으므로 여기서 2판으로 바꾼다(모든 values_at/distinct_at 가 이 L 을 읽는다)
LEDGER = S.LEDGER_DIR
for f in list(B.L.keys()):
    B.L[f] = json.load(open(os.path.join(LEDGER, f), encoding="utf-8"))
B.LEDGER = LEDGER
import erd_build_v11 as B11  # noqa
import erd_build_v23 as B23  # noqa
import erd_build_v24 as B24  # noqa
import erd_colmap_v3 as C  # noqa

WORK = HERE
STEP1 = S.STEP1_FILE
norm, mkid, sha256, values_at, distinct_at, md_table = B.norm, B.mkid, B.sha256, B.values_at, B.distinct_at, B.md_table
Dict_ = B.Dict_
L = B.L
SCAN = B.SCAN
FILES = B.FILES
load_module = B11.load_module
RESOLVE = B11.RESOLVE
TUPLES = load_module("erd_v3_tuples", os.path.join(WORK, "erd-v3-tuples.py"))
OUT = {"md": "erd-v3.md", "json": "erd-v3.json", "cmap": "erd-v3-column-map.md", "dict": "erd-v3-dictionaries.json", "tuples": "erd-v3-tuples.json", "check": "erd-v3-check.py"}
RULE_REF = B23.RULE_REF
DERIVED_ID_RE = re.compile(r"\b(PRC|ADV|CFL)-")
WRITTEN = "2026-11-05"


# ---------------------------------------------------------------------------
# 브론즈 2판 검증 · 1판 대조
# ---------------------------------------------------------------------------
def bronze_meta():
    hashes = {}
    for line in open(S.BRONZE_HASHES, encoding="utf-8"):
        h, f = line.split()
        hashes[f] = h
    rows, mism, changed = [], [], []
    for f in FILES:
        full = sha256(os.path.join(LEDGER, f))
        v1 = sha256(os.path.join(S.LEDGER_DIR_V1, f)) if os.path.exists(os.path.join(S.LEDGER_DIR_V1, f)) else None
        ok = full.startswith(hashes.get(f, "∅"))
        if not ok:
            mism.append(f)
        if v1 and v1 != full:
            changed.append(f)
        rows.append({"file": f, "sha256": full, "hashes_txt": hashes.get(f), "match": ok, "v1_sha256": v1, "changed_from_v1": bool(v1 and v1 != full)})
    changelog = open(S.BRONZE_CHANGELOG, encoding="utf-8").read()
    return {"version": S.BRONZE_VERSION, "date": S.BRONZE_DATE, "dir": "bronze/phub-ledger", "hashes_file": "bronze/phub-ledger/HASHES.txt", "files": rows, "mismatch": mism, "changed_from_v1": changed, "changelog": changelog,
            "name_diff": name_diff()}


def name_diff():
    """1판 ↔ 2판 문자열 값 차이(전수)."""
    out = []
    for f in FILES:
        a = open(os.path.join(S.LEDGER_DIR_V1, f), encoding="utf-8").read()
        b = open(os.path.join(LEDGER, f), encoding="utf-8").read()
        if a == b:
            continue
        sa, sb = set(re.findall(r'"([^"]*)"', a)), set(re.findall(r'"([^"]*)"', b))
        out.append({"file": f, "v1_only": sorted(sa - sb), "v2_only": sorted(sb - sa)})
    return out


# ---------------------------------------------------------------------------
# 사전 — v2.4 + adverse_qualifier(V3-1) + site kind·조직층 5(V3-5) − 사건 동의어 「공기색전」(V3-1)
# ---------------------------------------------------------------------------
def _count(src, value):
    return sum(1 for v, _ in values_at(*src) if v and norm(value) in norm(str(v)))


def build_dictionaries_v3():
    DICTS = B24.build_dictionaries_v24()
    # --- V3-5 site: kind + layer 값
    d = DICTS["site"]
    for e in d.entries.values():
        e["kind"] = "region" if e["canonical"] in S.SITE_REGION_VALUES else "anatomical"
    for canon, src, syns, note in S.SITE_LAYERS:
        n = _count(src, canon)
        assert n > 0, f"조직층 값 출처 없음: {canon} {src}"
        e = d.add_canonical(canon, src[0], src[1], n, kind="derived", site_kind="layer", members=None)
        e["kind"] = "layer"
        e["layer_note"] = note
        for f, p in S.SITE_LAYER_EXTRA_SOURCES.get(canon, []):
            n2 = _count((f, p), canon)
            assert n2 > 0, f"조직층 값 출처 없음: {canon} {f}:{p}"
            e["sources"].append(d.src(f, p, n2, "derived"))
        for sv, ss in syns:
            ns = _count(ss, sv)
            assert ns > 0, f"조직층 동의어 출처 없음: {canon} ~ {sv}"
            d.add_synonym(norm(canon), sv, ss[0], ss[1], ns, link="표기 변형(derived)", kind="derived")
    d.note = (d.note or "") + " · v3(V3-5): 값마다 kind ∈ {anatomical, relative(relative_site 사전), layer, region} · 조직층 5(피부 · 피하 지방층 · 근육 · 혈관 · 점막 · site_kind=layer · anatomy 층 정보·complications 출처) · region = 얼굴. 시술 튜플 site 칸에는 anatomical·region 만"
    # --- V3-1 사건 동의어 「공기색전」 제거(수식 + 사건으로 가른다)
    ev = DICTS["adverse_event_type"]
    e = ev.entries[norm("색전")]
    removed = [s for s in e["synonyms"] if norm(s["value"]) == norm("공기색전")]
    e["synonyms"] = [s for s in e["synonyms"] if norm(s["value"]) != norm("공기색전")]
    e["v3_removed_synonyms"] = [{"value": s["value"], "why": "V3-1: 수식 공기 + 사건 색전 — 동의어가 아니라 (색전, none, 미상, 공기)"} for s in removed]
    ev.note = (ev.note or "") + " · v3(V3-1): 「공기색전」은 색전의 동의어에서 뺐다(접두 수식 공기 + 사건 색전) — 사전 값 변경은 이것 하나"
    # --- V3-1 수식 사전
    d = Dict_("adverse_qualifier", "부작용 수식(물질·기전)", "v3(V3-1): 부작용 튜플의 선택 수식 칸. 물질(공기 · 필러 · 지방 · 혈전) · 기전(역행성). 값·동의어 전부 원장 잎 키 값의 부분 문자열(kind=derived). 없음 = none(값). 사전에 없는 조각은 미등록(사전 추가는 결정 dictionary_add)")
    d.kind = "value"
    for canon, kind, src, syns, note in S.ADVERSE_QUALIFIERS:
        n = _count(src, canon)
        assert n > 0, f"수식 사전 값 출처 없음: {canon} {src}"
        e = d.add_canonical(canon, src[0], src[1], n, kind="derived", qualifier_kind=kind)
        e["kind"] = kind
        e["note"] = note
        for f, p in S.ADVERSE_QUALIFIER_EXTRA_SOURCES.get(canon, []):
            n2 = _count((f, p), canon)
            assert n2 > 0, f"수식 사전 값 출처 없음: {canon} {f}:{p}"
            e["sources"].append(d.src(f, p, n2, "derived"))
        for sv, ss in syns:
            ns = _count(ss, sv)
            assert ns > 0, f"수식 동의어 출처 없음: {canon} ~ {sv}"
            d.add_synonym(norm(canon), sv, ss[0], ss[1], ns, link="표기 변형(derived)", kind="derived")
    DICTS["adverse_qualifier"] = d
    return DICTS


def dict_json(dicts):
    j = B23.dict_json(dicts)
    j["erd_version"] = S.ERD_VERSION
    j["bronze_version"] = S.BRONZE_VERSION
    j["values_changed_from_v2_4"] = {"added_dictionary": ["adverse_qualifier(5)"], "added_values": ["site: 피부 · 피하 지방층 · 근육 · 혈관 · 점막 (kind=layer)"], "removed_synonyms": ["adverse_event_type 색전 ~ 공기색전 (V3-1)"], "added_fields": ["site[].kind", "adverse_qualifier[].kind"], "note": "그 밖 45 사전의 값·동의어·순서는 v2.4 와 같다(검산 M-11)"}
    j["note"] = "v3: 사전 47 = v2.4 46 + adverse_qualifier. site 에 조직층 5 값(kind=layer)과 kind 필드. 사건 사전 동의어 「공기색전」 제거. 그 밖 값 불변"
    return j


def migrate_decisions(v24erd):
    recs, mig = [], []
    for o in v24erd["decisions"]:
        r = OrderedDict((k, o[k]) for k in S.DECISION_COMMON_FIELDS)
        recs.append(r)
        mig.append({"id": r["id"], "v2_4": {k: o.get(k) for k in ("kind", "decided_by", "decided_at", "status")}, "v3": {k: r[k] for k in ("kind", "decided_by", "decided_at", "status")},
                    "derived_id_in_target": bool(DERIVED_ID_RE.search(json.dumps(r["target"], ensure_ascii=False))), "change": "없음(그대로)"})
    recs.append(OrderedDict([("id", "DEC-2026-11-05-26"), ("kind", "scope_review"),
                             ("target", {"erd_ref": "§1.3 resolve_rules(stopwords · company_paren · combo) · §1.4 · §1.5 수식 칸 · §2.5 product · §2.6 technique · §2.7 site.kind · §2.14 adverse_effect.qualifier · §2.15 candidates · §2.21 decision · R5 · R12 · R29 · R31 · §4 사전(adverse_qualifier · site layer) · §5 kind 17 · 적용 ① · 규칙 ⑦", "review_item": "erd-v3-brief.md V3-1 ~ V3-10 (ERD-V3-CANDIDATES.md V3-1~8 + 빌더 제약 2)"}),
                             ("new_value", {"disposition": "v3: 부작용 수식 칸 qualifier · 괄호 안 회사·제품 규칙 · stopwords · 조합 기호 확정(+ 함께 · / 부위 함께·대안 또는 · 부위 여럿 → 튜플 여럿 · member_mode) · 부위 kind(layer 5) · canonical_rename · description/media_refs · R5 하위분류 · 결정 anchor 확장 · fold_approve 가 ⑦ 닫음. 원장 = 브론즈 2판"}),
                             ("reason", "실버 빌드 1~4차에서 드러난 구조·규칙 변경 — 사용자 승인 2026-11-05 「v3 진행하자」. ERD 승인 때 approved"),
                             ("decided_by", None), ("decided_at", None), ("status", "proposed"),
                             ("source_refs", [{"kind": "brief", "ref": "erd-v3-brief.md"}, {"kind": "erd", "ref": "ERD-V3-CANDIDATES.md · ERD-FROZEN.md"}])]))
    return recs, mig


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


def rescan_v2():
    """2판 잎 키를 컬럼 스캐너와 같은 방식으로 다시 센다 — 1판 스캔과 집합 대조(검산 A)."""
    SC = B11.SCANNER
    out = {}
    for f in FILES:
        out[f] = SC.FileScan(os.path.join(LEDGER, f)).run()
    diff = {}
    for f in FILES:
        a = set(SCAN["files"][f]["leaf_paths"])
        b = set(out[f]["leaf_paths"])
        if a != b:
            diff[f] = {"v1_only": sorted(a - b), "v2_only": sorted(b - a)}
    return {"leaf_count_v2": sum(v["leaf_count"] for v in out.values()), "leaf_count_v1": SCAN["total_leaf_paths"], "diff": diff}


def mermaid():
    s = B24.mermaid()
    head, _ = s.split("    %% v2.4:", 1)
    return head + ("    %% v3: ADVERSE_EFFECT 튜플은 (event, site, course, qualifier?) — 수식 칸(사전 adverse_qualifier · 없음 = none 값)이 식별자에 든다. SITE 값마다 kind(anatomical|relative|layer|region · 조직층 5). "
                   "R5 는 MODALITY|MODALITY_SUBCATEGORY → TECHNIQUE. R12 member 에 member_mode(and|or) — 「무엇을 하나 × 부위 여럿」 참조는 같은 what 의 PROCEDURE 튜플 여럿(anchor REF-…#s<i>). "
                   "PRODUCT·TECHNIQUE 에 description·media_refs(브론즈 밖 에셋 참조). DECISION kind 17(+canonical_rename) · tuple_assign(_multi)·adverse_tuple_assign 는 미해결·조합 anchor 에도 · fold_approve 가 ⑦ CONFLICT 를 닫는다. 원장 = 브론즈 2판")


def stopword_locators(TUP):
    """규칙 데이터(resolve_rules.stopwords.words[].locators)를 실측으로 채운다."""
    st = {w["word"]: w for w in TUP["procedure"]["summary"]["stopwords"]["words"]}
    out = []
    for w in S.RESOLVE_RULES["step2_decompose"]["stopwords"]["words"]:
        m = st.get(w["word"], {})
        out.append(dict(w, locators=m.get("locators", []), hits=m.get("hits", 0)))
    return out


# ---------------------------------------------------------------------------
# 산출물
# ---------------------------------------------------------------------------
def write_outputs(colrows, dicts, step1_scan, v1erd, v11erd, v24erd, v24tup, bronze, rescan):
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
    TUP = TUPLES.run_all(dic_json, S.TUPLE_RULES, L, S.RESOLVE_RULES, v24tup)
    TUP["procedure"]["v21_none_fold_split"] = TUPLES.v21_split(TUP)
    # stopwords locator 실측 → 규칙 데이터에 적재(출처 없는 단어 0 이어야 한다 — 검산 M-3)
    S.RESOLVE_RULES["step2_decompose"]["stopwords"]["words"] = stopword_locators(TUP)
    json.dump(TUP, open(os.path.join(WORK, OUT["tuples"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    IDX = B.Index()
    CONF = B11.conflict_estimates_v11(IDX, RES)
    for c in CONF:
        c["rule_ref"] = RULE_REF.get(c["kind"])
        c["status_on_build"] = "open"
        c["close_kind"] = "conflict_close(not_same) · fold_approve(v3: 접는 쌍의 ⑦ 을 닫는다)" if c["kind"] == "duplicate_candidate" else "conflict_override · conflict_close" if c["kind"] == "value_conflict" else "dictionary_add · conflict_close" if c["kind"] == "unregistered_value" else "tuple_assign(_multi · v3: 미해결 anchor 에도) · dictionary_add · conflict_close(needs_source)"
    Q14 = B11.q14_bundles_v11()
    SITE_TABLE = B11.site_replacement_table(dicts)
    res_summary = OrderedDict()
    for k, v in RES.items():
        res_summary[k] = {kk: vv for kk, vv in v.items() if kk != "rows"}
        res_summary[k]["v1"] = ({"n": v1rep[k]["n"], "resolved": v1rep[k]["resolved"], "unresolved": v1rep[k]["unresolved"], "by_depth": v1rep[k]["by_depth"]} if v1rep and k in v1rep else None)
        res_summary[k]["v2_4"] = ({kk: v24erd["resolution_report"][k].get(kk) for kk in ("n", "resolved", "decomposed", "unresolved")} if v24erd and k in v24erd.get("resolution_report", {}) else None)
    decisions, decisions_migration = migrate_decisions(v24erd)
    moves = [{"file": f, "path": p, "v1_1": a, "v2": b} for f, p, a, b in C.MOVES]
    moves22 = [{"file": f, "path": p, "v2_1": a, "v2_2": b} for f, p, a, b in C.MOVES_V22]
    moves23 = [{"file": f, "path": p, "v2_2": a, "v2_3": b} for f, p, a, b in C.MOVES_V23]
    moves24 = [{"file": f, "path": p, "v2_3": a, "v2_4": b} for f, p, a, b in C.MOVES_V24]
    moves3 = [{"file": f, "path": p, "v2_4": a, "v3": b} for f, p, a, b in C.MOVES_V3]
    notes3 = [{"file": f, "path": p, "target": t, "note": n} for f, p, t, n in C.NOTE_CHANGES_V3]
    ps, as_ = TUP["procedure"]["summary"], TUP["adverse"]["summary"]
    EE_rows = [{k: v for k, v in r.items() if k != "ends"} for r in TUP["procedure"]["edge_ends"]]
    erd = OrderedDict([
        ("erd_version", S.ERD_VERSION), ("previous_version", S.PREVIOUS_VERSION), ("status", "draft — 사용자 승인 전"), ("written", WRITTEN), ("bronze_snapshot", S.SNAPSHOT), ("bronze_version", S.BRONZE_VERSION), ("bronze", {k: v for k, v in bronze.items() if k != "files"}), ("bronze_leaf_rescan", rescan),
        ("layers", {"bronze": "원장 21(브론즈 2판 bronze/phub-ledger · HASHES.txt) + 조사 산출물 step1-products.json 1 (바이트 보존, SHA256 식별)", "semantic": "이 ERD + 값 사전 + 분해 규칙(참조 §1.3 · 튜플 §1.4/§1.5), 승인이 정본 조건, 버전 개정", "silver": "ERD 를 따르는 정규화 레코드, 모든 값에 (file, path) 출처", "gold": "실버 조합 뷰, 새 사실 금지"}),
        ("user_definitions", [{"no": n, "text": t} for n, t in S.USER_DEFINITIONS]), ("user_definitions_v3", [{"no": n, "text": t} for n, t in S.USER_DEFINITIONS_V3]), ("explicit_exception", S.EXPLICIT_EXCEPTION), ("user_definitions_v3_note", S.USER_DEFINITIONS_V3_NOTE),
        ("principles", [{"key": k, "text": v} for k, v in S.PRINCIPLES]),
        ("normalize_rule", S.NORMALIZE_RULE), ("id_rule", S.ID_RULE), ("fold_condition", S.FOLD_CONDITION), ("course_rule", S.COURSE_RULE), ("site_rule", S.SITE_RULE), ("raw_name_rule", S.RAW_NAME_RULE), ("expression_rule", S.EXPRESSION_RULE),
        ("adverse_fold_rule", S.ADVERSE_FOLD_RULE), ("locator_rule", S.LOCATOR_RULE), ("cat_family_rule", S.CAT_FAMILY_RULE),
        ("qualifier_rule", S.QUALIFIER_RULE), ("company_paren_rule", S.COMPANY_PAREN_RULE), ("stopword_rule", S.STOPWORD_RULE), ("combo_rule", S.COMBO_RULE), ("site_kind_rule", S.SITE_KIND_RULE), ("rename_rule", S.RENAME_RULE), ("media_rule", S.MEDIA_RULE), ("r5_subcategory_rule", S.R5_SUBCAT_RULE), ("decision_anchor_rule", S.DECISION_ANCHOR_RULE), ("fold_close_rule", S.FOLD_CLOSE_RULE),
        ("adverse_qualifiers", [{"canonical": c, "kind": k, "source": f"{src[0]}:{src[1]}", "synonyms": [{"value": sv, "source": f"{ss[0]}:{ss[1]}"} for sv, ss in syns], "note": n} for c, k, src, syns, n in S.ADVERSE_QUALIFIERS]),
        ("site_layers", [{"canonical": c, "source": f"{src[0]}:{src[1]}", "synonyms": [{"value": sv, "source": f"{ss[0]}:{ss[1]}"} for sv, ss in syns], "note": n} for c, src, syns, n in S.SITE_LAYERS]),
        ("edge_end_rule", S.EDGE_END_RULE), ("edge_end_kinds", S.EDGE_END_KINDS), ("proc_axis_edges", S.PROC_AXIS_EDGES),
        ("resolve_rules", S.RESOLVE_RULES), ("tuple_rules", S.TUPLE_RULES),
        ("source_files", files_meta),
        ("entities", ent_json), ("relations", rel_json), ("enums", S.ERD_ENUMS),
        ("quality_rules", [{"no": a, "class": b, "rule": c} for a, b, c in S.QUALITY_RULES]),
        ("synonym_key_normalization", v1erd["synonym_key_normalization"] if v1erd else {}),
        ("q25", [{"no": n, "answer": a} for n, a in S.Q25]),
        ("review_dispositions", [{"no": no, "title": B.REVIEW[no - 1]["title"], "decided_by": who, "disposition": what, "applied_at": where} for no, (who, what, where) in S.DISPOSITIONS.items()]),
        ("decision_kinds", [{"kind": k, "build_reads": br, "target": t, "new_value": nv, "note": n, "new_in_v2_2": k in S.DECISION_KINDS_NEW, "new_in_v2_3": k in S.DECISION_KINDS_NEW_V23, "reshaped_in_v2_3": S.DECISION_KINDS_RESHAPED_V23.get(k), "new_in_v3": k in S.DECISION_KINDS_NEW_V3, "note_changed_in_v3": S.DECISION_KINDS_NOTE_V3.get(k)} for k, br, t, nv, n in S.DECISION_KINDS]),
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
        ("column_map_moves", moves), ("column_map_moves_v2_2", moves22), ("column_map_moves_v2_3", moves23), ("column_map_moves_v2_4", moves24), ("column_map_moves_v3", moves3),
        ("column_map_note_changes_v2_3", v24erd.get("column_map_note_changes_v2_3", [])), ("column_map_note_changes_v2_4", v24erd.get("column_map_note_changes_v2_4", [])), ("column_map_note_changes_v3", notes3),
        ("dictionaries_summary", [{"name": d.name, "label": d.label, "kind": getattr(d, "kind", "value"), "canonical": len(d.entries), "synonyms": sum(len(e["synonyms"]) for e in d.entries.values()), "candidates": len(d.candidates)} for d in dicts.values()]),
        ("resolution_report", res_summary), ("resolution_total", TOTAL),
        ("tuple_report", {"procedure": ps, "adverse": as_}),
        ("tuple_report_v2_4", {"procedure": (v24erd or {}).get("tuple_report", {}).get("procedure"), "adverse": (v24erd or {}).get("tuple_report", {}).get("adverse")}),
        ("edge_ends", {"rows": EE_rows, "total": ps["edge_ends_total"], "total_n": ps["edge_ends_total_n"], "by_relation": ps["edge_ends_by_relation"], "slots": ps["edge_ends_slots"], "member_mode": ps["edge_ends_member_mode"], "multi_tuple": ps["edge_ends_multi_tuple"]}),
        ("v21_none_fold_split", TUP["procedure"]["v21_none_fold_split"]),
        ("technique_inheritance_candidates", TUP["procedure"]["inheritance_candidates"]),
        ("r29_taxonomy_safety_keys", S.R29_TAXONOMY_SAFETY_KEYS),
        ("conflict_estimates", CONF),
        ("change_list", [{"no": a, "what": b, "where": c} for a, b, c in S.CHANGE_LIST]),
    ])
    json.dump(erd, open(os.path.join(WORK, OUT["json"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = ["# ERD v3 — 잎 키 행선지 표 (원장 21 · 브론즈 2판 + step1-products.json)", "",
          f"**v2.4 와 행선지·표적이 다른 행은 {len(moves3)} 개다(이동 없음 · 변화 없음을 명시).** 비고만 바뀐 행 {len(notes3)}(아래 「비고 변경 v2.4 → v3」 — V3-1 수식 출처 · V3-3·V3-4 참조 자리 {len(C.REF_KEYS)} · V3-5 조직층 출처 · V3-2 회사 괄호 후보 자리 · V3-8). 그 밖 행선지·표적·비고는 v2.4 와 같다(검산 A 행 단위 대조). 규칙 `erd_colmap_v3.py`.", "",
          f"브론즈 2판 잎 키 재스캔: 원장 21 잎 키 {rescan['leaf_count_v2']} = 1판 {rescan['leaf_count_v1']} · 파일별 집합 차이 {len(rescan['diff'])}(2판은 이름 6곳만 바뀌어 키 구조가 같다).", "",
          f"작성 {WRITTEN} · 입력 `bronze-ledger-column-scan.json`(원장 잎 키 {sum(1 for r in colrows if r['file'] != STEP1)}) + `step1-products.json` 잎 키 {step1_scan['leaf_count']} = {len(colrows)} · 행선지 범주 5: 개체 / 사전 / 엣지 / 브론즈 / 버림 · **미정 0**", "",
          f"표적 표기: `entity.attr` · `dict:<사전>` · `R#.attr`(관계 번호는 erd-v3.md §3) · `bronze` · `drop`. v1.1 과 달라진 행 {len(moves)} + v2.2 {len(moves22)} + v2.3 {len(moves23)} + v2.4 {len(moves24)} + v3 {len(moves3)}.", "",
          "## 비고 변경 (v2.4 → v3 · 표적 동일)", "", md_table(["#", "파일", "경로", "표적", "추가된 비고"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['target']}`", m["note"]) for i, m in enumerate(notes3)]), "",
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
    return erd, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, moves, moves22, moves23, moves24, moves3, notes3


# ---------------------------------------------------------------------------
# erd-v3.md
# ---------------------------------------------------------------------------
def build_erd_md(erd, colrows, dicts, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, v1erd, moves, v24tup, moves3, notes3):
    o = []
    A = o.append
    v1rep = v1erd.get("resolution_report", {}) if v1erd else {}
    T = S.TUPLE_RULES
    ps, as_ = TUP["procedure"]["summary"], TUP["adverse"]["summary"]
    va = (v24tup or {}).get("adverse", {}).get("summary", {})
    bro = erd["bronze"]
    A("# ERD v3 — 피부과 시술 허브 메달리온 시맨틱 정의")
    A("")
    A(f"작성 {WRITTEN} · 상태 **초안(사용자 승인 전)** · 원장 = **브론즈 2판** `bronze/phub-ledger/`({bro['date']} · HASHES.txt 21 전부 일치 · 1판 {S.SNAPSHOT} 스냅샷과의 차이 = CHANGELOG 6곳 — 바뀐 파일 {', '.join(bro['changed_from_v1'])}) + 조사 산출물 step1 10-29 · 발주서 `erd-v3-brief.md`(사용자 승인 2026-11-05 「v3 진행하자」) · 근거 `ERD-V3-CANDIDATES.md` V3-1~8 + 실버 빌드 빌더 제약 2(V3-9·10) · 동결 v2.4(`ERD-FROZEN.md`)의 **사용자 정의 3 과 명시 예외는 그대로** · 이전 발주서(v1 ~ v2.4)의 입력·금지·기준·질문 기본값·처분 유지")
    A("")
    A(f"기계용 동본 `erd-v3.json` · 값 사전 `erd-v3-dictionaries.json`(v2.4 46 + `adverse_qualifier` = 47 · site 에 조직층 5 값 + kind · 사건 동의어 「공기색전」 제거 · 그 밖 값 불변) · 잎 키 행선지 `erd-v3-column-map.md`(v2.4 대비 이동 {len(moves3)} — 변화 없음 · 비고 변경 {len(notes3)} · 2판 잎 키 재스캔 = 1판) · 분해 규칙 실행 `erd-v1.1-resolve.py`(§9.2 · 2판 원장으로 재실행) · 튜플 실측 `erd-v3-tuples.py`(결과 `erd-v3-tuples.json`, §9.5·§9.6 v2.4 와 나란히 + 신설 §9.5.9~11 · §9.6.7~8) · 검산 `erd-v3-check.py` (결과 §10). 이전 판 산출물은 그대로 두었다. **v2.4 → v3 변경 목록(V3-# 대응)은 §11**, v3 밖 관찰은 §12.")
    A("")
    A("**v3 의 범위는 발주서의 변경 10건뿐이다.** " + " · ".join(f"**{a}** {b}({c.split(' · ')[0]})" for a, b, c in S.CHANGE_LIST) + ". **개체 21 · 관계 31(R5 from · R12 속성) · 사전 47(+adverse_qualifier) · 행선지 1,072** — 그 밖 개체·관계·규칙은 v2.4 그대로. 사전 값·동의어·매핑·접힘 승인·충돌 판정은 결정 레코드이며 ERD 를 열지 않는다(ERD-FROZEN) — v3 가 사전에 손댄 것은 구조가 요구한 셋뿐(조직층 5 · 수식 5 · 「공기색전」 동의어 1).")
    A("")
    A("### 0. 사용자 정의 3 · 명시 예외 (ERD-FROZEN · 그대로)")
    A("")
    A("동결 원문(ERD-FROZEN 동결 조건 · 글자 그대로):")
    A("")
    for n, t in S.USER_DEFINITIONS:
        A(f"{n}. {t}")
    A("")
    A("v3 승계 문장(R-4 · 정의 2 에 선택 수식 칸 · 정의 3 kind 17 · 안정 키에 #s<i>):")
    A("")
    for n, t in S.USER_DEFINITIONS_V3:
        A(f"{n}. {t}")
    A("")
    A(f"**명시 예외(사용자 결정 2026-11-04)**: {S.EXPLICIT_EXCEPTION}")
    A("")
    A(f"**v3 와 정의의 관계**: {S.USER_DEFINITIONS_V3_NOTE}")
    A("")
    A("**원칙(v2.4 · 시술 축 v2.1~v2.3 과 동일하게 부작용 축에 적용 · 그대로)**: " + " ".join(f"**{k}.** {v}" for k, v in S.PRINCIPLES))
    A("")
    A("## 1. 범위와 층")
    A("")
    A("| 층 | 무엇 | 규칙 |")
    A("|---|---|---|")
    A(f"| 브론즈 | 원장 21개 JSON(**브론즈 2판** `bronze/phub-ledger/` · 원장의 집) + `step1-products.json`(조사 산출물) | 바이트 보존·수정 금지. 파일 SHA256 이 식별자(§6 표 · HASHES.txt). 1판 = `phub-stg-2026-10-26/`(스냅샷 {S.SNAPSHOT}) · 2판 = 1판 복사 + CHANGELOG(부위 나열 `/` → `+` 6곳 · {bro['date']}). 원장을 고칠 때는 파일을 고치고 CHANGELOG 한 줄 — 빌드는 HASHES.txt 로 검증한다 |")
    A("| 시맨틱 | 이 ERD + 값 사전 + 분해 규칙(참조 §1.3 · 튜플 §1.4/§1.5) | 문서. 사용자 승인이 정본 조건. 버전으로 개정(v1 → … → v2.4(동결) → v3 → …) |")
    A("| 실버 | ERD 를 따르는 정규화 레코드 | **모든 값은 (파일, 잎 키 경로) 출처를 가진다.** 출처 없는 값 금지. 충돌은 둘 다 보관 |")
    A("| 골드 | 실버 조합 뷰 | 실버에 없는 사실을 만들지 않는다. 충돌 미판정 레코드 제외 |")
    A("")
    A("지식은 원장 21(2판)·1판(대조)·컬럼 리포트·스캔 결과·erd-v* 산출물·발주서·검토서·`step1-products.json`·`ERD-FROZEN.md`·`ERD-V3-CANDIDATES.md`·`silver-v3/decisions/_batch3-candidates.md`·`silver-v3/out/report.md`·`silver-v3/README.md` 에서만 가져왔다. step2·step3·source-map·DATA-001·DEC-*·silver-*(silver-v3 제외)·silver-v3/lib·`_archive/` 는 열지 않았다 — ERD 가 빌더를 따라가지 않는다.")
    A("")
    A("**브론즈 2판 CHANGELOG(1판과의 차이 전부)**:")
    A("")
    for d in bro["name_diff"]:
        A(f"- `{d['file']}`: 1판 {', '.join('「' + x + '」' for x in d['v1_only'])} → 2판 {', '.join('「' + x + '」' for x in d['v2_only'])}")
    A("")
    A("### 1.1 정규화(「같은 것」판정)와 식별자")
    A("")
    A(f"- 정규화 `{S.NORMALIZE_RULE['name']}`: " + " → ".join(S.NORMALIZE_RULE["steps"]))
    A(f"- {S.NORMALIZE_RULE['note']}")
    A(f"- 식별자: `{S.ID_RULE['format']}`. canonical_key 는 개체별(§2 각 표의 「식별자」). {S.ID_RULE['canonical_key']}")
    A(f"- survey 제품: {S.ID_RULE['survey_products']}")
    A(f"- 사전 항목 id(v3 · R-2): {S.ID_RULE['dictionary_entry']}")
    A(f"- **튜플 식별자** — procedure(v2.2 · v3 #s<i>): `{S.ID_RULE['procedure']}` · reference anchor: {S.ID_RULE['reference']} · adverse_effect(**v3 · 수식 칸 포함**): `{S.ID_RULE['adverse_effect']}` · catalog_item(v2.4 계열 코드 고정): {S.ID_RULE['catalog_item']} · adverse_expression: {S.ID_RULE['adverse_expression']} · 표현 후보: {S.ID_RULE['adverse_expression_candidates']}")
    A(f"- **접힘 조건(v2.2 · 문자 그대로): 「{S.FOLD_CONDITION}」** — {S.FOLD_RULE}.")
    A(f"- **부작용 접힘 조건(v3)**: {S.ADVERSE_FOLD_RULE}.")
    A(f"- **원장 locator(v2.3)**: {S.LOCATOR_RULE}.")
    A(f"- **결정 target(v3)**: {S.DECISION_TARGET_RULE}. 충돌: {S.ID_RULE['conflict_decision_ids']}.")
    A("- 「같은 것」 = 정규화 완전 일치(①) + 사전 동의어(②)만 자동. 참조 문자열은 §1.3 분해 규칙으로 조각내어 조각 단위로 같은 판정을 한다. 튜플은 조각이 가리키는 개체·사전 값의 조합이 같을 때 같은 것이다. 유사도·추측 매칭은 ⑦ 후보로만.")
    A("")
    A("### 1.2 다이어그램 (개체·관계만)")
    A("")
    A("```mermaid")
    A(mermaid())
    A("```")
    A("")
    A("### 1.3 참조 해결 — 결정론 분해 규칙 (v1.1 B · **v3: stopwords · 괄호 안 회사·제품 · 조합 기호 확정**)")
    A("")
    R = S.RESOLVE_RULES
    A("v1.1 의 세 단계를 **데이터**(`erd-v3.json → resolve_rules`)로 적고 `erd-v1.1-resolve.py`(§9.2)와 `erd-v3-tuples.py`(§1.4 · stopwords·회사 괄호·조합 기호는 여기서 실행)가 그대로 실행한다. v2 → catalog_item_name · v2.1 fallback_to_parent=false · v2.2 미해결 사유 · v2.3·v2.4 불변 · **v3**: 2단계에 stopwords(V3-3)·company_paren(V3-2), 3단계에 combo(V3-4). 유사도·추측은 없다.")
    A("")
    A(f"1. **계열 확정** — {R['step1_family']['what']}. 자리별 힌트: " + " · ".join(f"{k}: `{v}`" for k, v in R["step1_family"]["slot_hints"].items()) + f". 코드 정규식 `{R['step1_family']['code_regex']}`")
    A(f"2. **이름 분해** — 괄호 안을 뗀다(`{R['step2_decompose']['paren_regex']}`). 조합 기호 `{'` `'.join(R['step2_decompose']['combo_symbols'])}` 로 멤버를 나눈다(**v3 기호 뜻**: " + " · ".join(f"`{k}` {v}" for k, v in R["step2_decompose"]["combo_symbols_meaning"].items()) + f"). 조각마다 사전 순서 **{' → '.join(R['step2_decompose']['dictionary_order'])}**(procedure = catalog_item_name) 로 완전 일치를 시도한다(계열 사전에 닿으면 kind=modality). 규격 정규식 `{R['step2_decompose']['spec_regex']}` + unit 사전. {R['step2_decompose']['secondary_rule']}. {R['step2_decompose']['scope_rule']}. {R['step2_decompose']['overlap_rule']}.")
    sw = R["step2_decompose"]["stopwords"]
    A(f"   - **stopwords(v3 · V3-3)**: {sw['rule']} 단어 {len(sw['words'])}: " + " · ".join(f"`{w['word']}`({w['origin']} · locator {len(w.get('locators', []))})" for w in sw["words"]) + f". 회차 `{sw['session_regex']}` → session_index · 횟수 `{sw['count_regex']}` → count. 실측 §9.5.10")
    A(f"   - **괄호 안 회사·제품(v3 · V3-2)**: {R['step2_decompose']['company_paren']['rule']} 실측 §9.5.9")
    A(f"3. **조립** — 튜플 ({', '.join(R['step3_assemble']['tuple'])}). (a) resolved: {R['step3_assemble']['resolved']} (b) 분해 성공·항목 없음: {R['step3_assemble']['decomposed']} (c) unresolved: {R['step3_assemble']['unresolved']}")
    A(f"   - **fallback_to_parent = {R['step3_assemble']['fallback_to_parent']}** — {R['step3_assemble']['fallback_to_parent_note']}")
    A(f"   - **조합 기호(v3 · V3-4)**: {R['step3_assemble']['combo']['rule']} 실측 §9.5.11")
    A("")
    A("결과는 §9.2 에 v1 수치와 나란히(§9.2 는 v1.1 코드 재실행 — 2판 원장이라 바뀐 이름 4 참조의 수치만 v2.4 와 다르다). (a)·(b) 의 결과는 §1.4 의 튜플 규칙으로 한 번 더 내려가 procedure 튜플이 되고, (c) 미해결은 튜플을 만들지 않는다(v3: 미해결 참조의 REF- 도 결정 target). 그 튜플이 곧 엣지의 끝이다(§3 엣지 끝 규칙 · §9.5.8).")
    A("")
    A("### 1.4 시술 튜플 분해 규칙 (구조 변경 ① · v2.2 수정 1·2·3 · v2.3 엣지 끝 · v2.4 계열 코드 고정 · **v3 V3-2·V3-3·V3-4·V3-5** · 데이터 `erd-v3.json → tuple_rules.procedure` · `erd-v3-tuples.py` 실행)")
    A("")
    P = T["procedure"]
    A(f"- 입력: ① {P['input']['catalog_items']} · ② {P['input']['references']}")
    A(f"- **계열 코드(v2.4 · 검토 3-B′)**: {P['cat_family']}")
    A(f"- 조각: {P['fragments']}")
    A(f"- **stopwords(v3)**: {P['stopwords']}")
    A(f"- **괄호 안 회사·제품(v3)**: {P['company_paren']}")
    A(f"- **조합(v3 · 확정)**: {P['combo']}")
    A(f"- 조합(v2.2 문장 · 참고): {P['combo_v22']}")
    A(f"- fallback_to_parent: **{P['fallback_to_parent']}** (v2.1) · technique_inheritance: **{P['technique_inheritance']}** (v2.2 · v3 V3-8 은 결정 scope 만 넓힌다) · fold_condition: **{P['fold_condition']}** (v2.2)")
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
    A("### 1.5 부작용 튜플 분해 규칙 (구조 변경 ② · v2.3 · v2.4 원칙 A~D · **v3 V3-1 수식 칸 · V3-5 조직층** · 데이터 `erd-v3.json → tuple_rules.adverse`)")
    A("")
    Q = T["adverse"]
    A(f"- **원칙(v2.4 · 발주서 문장 그대로)**: {Q['principles']}")
    A(f"- 입력: {Q['input']['complications']} · 표현: {Q['input']['phrases']}")
    A(f"- 분해: {Q['split']}")
    A(f"- 튜플: {Q['tuple']}")
    A(f"- **경과(course) 규칙(v2.3 · §2.14 · §4 와 같은 문장)**: {Q['course']}")
    A(f"- **부위(site) 규칙(v2.4 수정 1 · 원칙 B·C)**: {Q['site']}")
    A(f"- **수식(qualifier) 규칙(v3 · V3-1)**: {Q['qualifier']}")
    A(f"- **접힘 조건(v3)**: {Q['fold_rule']}")
    A(f"- **raw_name 튜플(v2.4 수정 2)**: {Q['raw_name']}")
    A(f"- **표현(v2.4 수정 3 · 원칙 D · v3 네 칸)**: {Q['expressions']}")
    A(f"- 원장 locator: {Q['locator']}")
    A(f"- 타임라인 normal: {Q['normal_phrases']}")
    A(f"- 문헌: {Q['literature']}")
    A(f"- 식별자: `{Q['id']}` · 상태: {Q['status']}")
    A("")
    A("## 2. 개체 목록")
    A("")
    A(f"개체 {len(S.ENTITIES)}개 — v2 ~ v2.4 와 같다. v3 에서 바뀐 것: `site`(kind 열거형 · 조직층 5 — V3-5) · `product`·`technique`(description · media_refs — V3-7) · `technique`·`modality_subcategory`(R5 하위분류 — V3-8) · `adverse_effect`(qualifier · qualifier_id · qualifier_basis · extra_qualifiers · 식별자 — V3-1) · `adverse_expression`(candidates 네 칸 — V3-1) · `package`(member_mode — V3-4) · `conflict`(status 비고 — V3-10) · `decision`(kind 17 — V3-6 · V3-9 · V3-10). 그 밖은 v2.4 그대로.")
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
    A(f"관계 {len(S.RELATIONS)}개 — v2 ~ v2.4 와 같다(v1.1 25 + R26~R31). v3 에서 바뀐 것: **R5** from = modality|modality_subcategory · basis(V3-8) · **R12** member_mode · session_index · qualifier_text · alternatives(V3-3·V3-4) · R9/R17/R18 qualifier_text · alternatives · member_mode · R29 네 칸(V3-1) · R31 layer(V3-5) · R15 비고. "
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
    A(f"전부 `erd-v3-dictionaries.json` — v2.4 46 + **`adverse_qualifier`(V3-1)** = {len(dicts)} (값 사전 {nval} + 개체 이름 색인 {nidx}). **값 변경은 셋뿐**(검산 M-11): ① site 에 조직층 5(피부 · 피하 지방층 · 근육 · 혈관 · 점막 · kind=layer · 출처 anatomy 층 정보·complications) + 값마다 kind ② adverse_qualifier 5(공기 · 필러 · 지방 · 혈전 · 역행성 · 출처) ③ adverse_event_type 「색전」의 동의어 「공기색전」 제거(수식 + 사건). 그 밖 45 사전의 값·동의어·순서 = v2.4. 부위 사전 21 → {len(dicts['site'].entries)} · 기법 사전 12 유지.")
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
    A(md_table(["#", "사건", "category", "동의어(표기 변형)", "65 이름 중 출현", "분류 확인 필요", "v3 제거 동의어"], [(i + 1, e["canonical"], e["category"], ", ".join(s["value"] for s in e["synonyms"]) or "—", e["sources"][0]["n"], "○" if e.get("category_review") else "", ", ".join(x["value"] for x in e.get("v3_removed_synonyms", [])) or "") for i, e in enumerate(de.entries.values())]))
    A("")
    A("### 4.2 경과 사전(course) · 상대 부위 사전(relative_site) · **수식 사전(adverse_qualifier · v3)** · **부위 사전 kind(v3)**")
    A("")
    A(f"- **경과 규칙(v2.3 · §1.5 · §2.14 와 같은 문장)**: {dicts['course'].note}")
    A("- `course`: " + " · ".join(f"{e['canonical']}(동의어: {', '.join(s['value'] + '[' + s['sources'][0]['path'].split('.')[-1] + ']' for s in e['synonyms']) or '—'} · 출처 {e['sources'][0]['file']}:{e['sources'][0]['path']})" for e in dicts["course"].entries.values()))
    A("- `relative_site`: " + " · ".join(f"{e['canonical']}(동의어: {', '.join(s['value'] for s in e['synonyms']) or '—'})" for e in dicts["relative_site"].entries.values()))
    A(f"- **`adverse_qualifier`(V3-1)**: {dicts['adverse_qualifier'].note}")
    A("")
    A(md_table(["#", "수식", "종류", "동의어", "출처(파일:키 · 횟수)", "비고"], [(i + 1, e["canonical"], e["kind"], ", ".join(s["value"] for s in e["synonyms"]) or "—", " · ".join(f"`{s['file']}:{s['path']}`×{s['n']}" for s in e["sources"]), e.get("note", "")) for i, e in enumerate(dicts["adverse_qualifier"].entries.values())]))
    A("")
    A(f"- **`site` kind(V3-5)**: {S.SITE_KIND_RULE}")
    A("")
    A(md_table(["#", "부위", "kind", "site_kind(출처 종류)", "동의어", "출처(파일:키 · 횟수)"], [(i + 1, e["canonical"], e.get("kind"), e.get("site_kind"), ", ".join(s["value"] for s in e["synonyms"]) or "—", " · ".join(f"`{s['file']}:{s['path']}`×{s['n']}" for s in e["sources"])) for i, e in enumerate(dicts["site"].entries.values())]))
    A("")
    A("## 5. 충돌·결정 개체 정의 + 규칙 ①~⑩ + 신뢰 순위 + 결정 적용 순서")
    A("")
    A("충돌(`conflict`)·결정(`decision`) 개체 정의는 §2. 결정 레코드는 §5.2 의 모양으로 `erd-v3.json → decisions` 에 적재한다 — v2.4 의 25 를 그대로 이관 + v3 개정 DEC-26(proposed). 이관 표 §5.3. **결정 target 은 안정 키만(v2.3 · v3: 미해결·조합 REF- 도) · 적용 순서는 §5.4 표(① 에 canonical_rename).**")
    A("")
    A(md_table(["#", "분류", "규칙"], S.QUALITY_RULES))
    A("")
    A("빈값과 「없음」: 안 적힌 것(키 없음·null·빈 배열·빈 문자열) = null(미입력). 명시적으로 없다고 적힌 것만 빈 목록. step1 의 「확인 불가」·「근거 없음」·「해당 없음」은 값이다(null 아님). "
      "**시술 튜플의 site none·technique none 은 미상이며 식별자 값이 아니다(v2.2)** — 미상 칸이 있으면 식별자에 anchor(CAT-/REF-)를 섞어 항목·참조마다 고유하고 접히지 않는다. "
      "**부작용 튜플(v2.4 원칙 A~D · 명시 예외 · v3 수식 칸)**: 미등록 조각이 있거나 사건에 붙지 않은 조각이 남은 이름은 raw_name 튜플로 접히지 않고, 접힘은 네 칸 전부 사전 값일 때만 — 부작용의 site none·course 미상·qualifier none 은 명시 예외의 값(식별자에 들어간다). 표현은 단위를 만들지 않는다. "
      "단계 끝 = 컬럼 행선지 미정 0 · 충돌 미판정(open) 0 — v3: fold_approve 가 접는 쌍의 ⑦ 을 닫고(V3-10), conflict_close 가 나머지를 닫는다.")
    A("")
    A("**규칙 ④ (v2.2 · 사용자 결정으로 유지 + 기록)**: " + S.RULE4 + ".")
    A("")
    A(f"**V3-10**: {S.FOLD_CLOSE_RULE}")
    A("")
    A(f"**V3-9**: {S.DECISION_ANCHOR_RULE}")
    A("")
    A("### 5.1 원장 신뢰 순위 (파일별 · 21 + step1) — v1.1 그대로 (브론즈 2판도 같은 파일·같은 순위)")
    A("")
    A(md_table(["순위", "파일", "종류", "근거 키", "표시", "비고"], [(t, f"`{f}`", S.SOURCE_KIND[f], b, S.TRUST_FLAGS.get(f, ""), n) for f, t, b, n in sorted(S.SOURCE_FILES, key=lambda x: (x[1], x[0]))]))
    A("")
    s1 = next(fm for fm in erd["source_files"] if fm["file"] == STEP1)
    A(f"`products.json` 의 `products[].mfds` 필드만 2(식약처 허가)로 격상한다. `complications.json` 은 8-1 처분으로 3 유지 + 「AI 컨센서스 추정」. `step1-products.json` 은 조사 산출물: 허가 건 {s1['trust_tier_rule']['tier2_licenses']}/{s1['trust_tier_rule']['licenses_total']} 건의 허가·회사·공식명 필드만 2, 그 밖은 3. v3(V3-7): description·media_refs 를 채울 **새 브론즈 원천(조사 파일)**도 research_artifact 로 같은 표에 등록하고 locator 를 준다 — 지금은 없다.")
    A("")
    A("### 5.2 결정 kind — 빌드가 읽는 모양 (v2.2 · v2.3 · v2.4 · **v3: canonical_rename · anchor 확장 · ⑦ 닫음**)")
    A("")
    A(f"공통 필드: {' · '.join(S.DECISION_COMMON_FIELDS)}. status ∈ {{{', '.join(S.DECISION_STATUS)}}}. **{S.DECISION_BUILD_RULE}.** target·new_value 는 문자열이 아니라 kind 별 구조체다. kind {len(S.DECISION_KINDS)} = v2.3 16 + v3 신설 1(`canonical_rename` · V3-6). v3 에서 비고가 바뀐 kind: " + " · ".join(f"`{k}`({v})" for k, v in S.DECISION_KINDS_NOTE_V3.items()) + ".")
    A("")
    A(f"**target 규칙(v3)**: {S.DECISION_TARGET_RULE}.")
    A("")
    A(f"**canonical_rename(V3-6)**: {S.RENAME_RULE}")
    A("")
    A(md_table(["kind", "v2.2 신설", "v2.3 신설·개형", "v3", "빌드 적용", "적용 단계", "target", "new_value", "비고"],
               [(f"`{k}`", "○" if k in S.DECISION_KINDS_NEW else "", "신설" if k in S.DECISION_KINDS_NEW_V23 else ("개형" if k in S.DECISION_KINDS_RESHAPED_V23 else ""), "신설" if k in S.DECISION_KINDS_NEW_V3 else ("비고" if k in S.DECISION_KINDS_NOTE_V3 else ""), "○" if br else "기록만",
                 next((st for st, ks, _ in S.DECISION_APPLY_ORDER if k in ks), "⓪" if k == "reclassification" else "—"), t, nv, n) for k, br, t, nv, n in S.DECISION_KINDS]))
    A("")
    A("### 5.3 결정 레코드 — v2.4 의 25 이관 + v3 1 (전부)")
    A("")
    A(md_table(["id", "kind", "target", "new_value", "decided_by", "decided_at", "status", "source_refs"],
               [(d["id"], d["kind"], json.dumps(d["target"], ensure_ascii=False)[:200], json.dumps(d["new_value"], ensure_ascii=False)[:160], d["decided_by"] or "null", d["decided_at"] or "null", d["status"], " · ".join(x["ref"] for x in d["source_refs"])) for d in erd["decisions"]]))
    A("")
    A(f"이관(v2.4 → v3): 25 레코드 전부 모양·값 그대로(파생 id 포함 {sum(1 for m in erd['decisions_migration'] if m['derived_id_in_target'])} · 검산 K-2). DEC-26 은 v3 개정 기록(proposed) — ERD 승인 때 decided_by=사용자 · decided_at=승인일 · approved. 실버 결정 묶음(batch1·2A·2B · 276 레코드)은 실버 저장소에 있고 ERD 는 kind·target 모양만 정한다.")
    A("")
    A("### 5.4 결정 적용 순서 (v2.3 · **v3 ① 에 canonical_rename**)")
    A("")
    A(S.DECISION_APPLY_ORDER_RULE + ".")
    A("")
    A(md_table(["단계", "kind", "왜 이 자리인가"], [(st, " / ".join(f"`{k}`" for k in ks), why) for st, ks, why in S.DECISION_APPLY_ORDER]))
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
    A(f"`step1-products.json` 전체 SHA256 `{s1['sha256']}` · {s1['bytes']} bytes · 항목 {s1['items']} · 잎 키 {s1['leaf_paths']}. 2판 해시는 `bronze/phub-ledger/HASHES.txt`(16자리 접두)와 전부 일치(검산 D) · 1판과 다른 파일 {len(bro['changed_from_v1'])}.")
    A("")
    A("### 6.1 옮긴 키 (v1.1 → v2 이동 표)")
    A("")
    A(md_table(["#", "파일", "경로", "v1.1", "v2"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['v1_1']}`", f"`{m['v2']}`") for i, m in enumerate(moves)]))
    A("")
    A("## 7. 질문 25 답 — v1.1 그대로")
    A("")
    A(md_table(["#", "답 (발주서 §6 기본값 적용 · v1.1 개정분 7·8·10·11·14·16·24 유지)"], S.Q25))
    A("")
    A("v3 에서 답이 바뀐 질문은 없다. 질문 24(부위 사전)의 값은 v3 에서 조직층 5 가 더해졌고 kind 가 생겼다(§4.2) — 답의 뼈대(anatomy 11 + taxonomy 부위 라벨 10)는 그대로.")
    A("")
    A("## 8. 기본값 재검토 — 처분 결과 (v1.1 그대로)")
    A("")
    A("v1 §8 의 19 건 처분은 v1.1 에서 확정됐고 v2 이후 바꾸지 않는다. 각 건은 결정 레코드(`erd-v3.json → decisions` · §5.3, status approved)로 남는다.")
    A("")
    A(md_table(["#", "항목", "처분 주체", "처분(확정)", "반영 위치"], [(f"8-{no}", B.REVIEW[no - 1]["title"], who, what, where) for no, (who, what, where) in S.DISPOSITIONS.items()]))
    A("")
    A("### 8-2 표 — v1 부위 사전 「(확장)」 51 의 처분 (v1.1 그대로)")
    A("")
    A(md_table(["값", "cc_group 횟수", "재배치", "사유"], [(r["value"], r["cc_group_n"], r["dest"], r["reason"]) for r in SITE_TABLE]))
    A("")
    kept = [r for r in SITE_TABLE if r["dest"].startswith("부위")]
    A(f"부위 사전 유지 {len(kept)} · problem_subcategory_label 로 {len(SITE_TABLE) - len(kept)}. 부위 사전 최종 = 뼈대 11 + taxonomy 부위 라벨 {len(kept)} + v3 조직층 5 = **{len(dicts['site'].entries)}** (확장 0 · 조직층은 확장이 아니라 kind=layer 값).")
    A("")
    A("## 9. ERD 승인 때 사용자가 볼 것")
    A("")
    A("### 9.1 사전 표 (정준값 수 · 동의어 · 후보)")
    A("")
    A(md_table(["사전", "정준값", "동의어", "후보(미연결)"], [(d.name, len(d.entries), sum(len(e["synonyms"]) for e in d.entries.values()), "; ".join(c["value"] for c in d.candidates) or "—") for d in dicts.values()]))
    A("")
    A("핵심 사전 정준값 전체:")
    A("")
    for name in ["modality", "problem", "site", "technique", "course", "relative_site", "adverse_qualifier", "license_status", "license_kind", "license_state"]:
        d = dicts[name]
        A(f"- `{name}` ({len(d.entries)}): " + " · ".join((e["canonical"] + (f"[{e['code']}]" if e.get("code") else "") + (f"({e['kind']})" if name in ("site", "adverse_qualifier") and e.get("kind") else "")) for e in d.entries.values()))
    A(f"- `adverse_event_type` ({len(dicts['adverse_event_type'].entries)}): " + " · ".join(e["canonical"] + f"[{e['category']}]" for e in dicts["adverse_event_type"].entries.values()))
    A(f"- `problem_subcategory_label` ({len(dicts['problem_subcategory_label'].entries)}): " + " · ".join(e["canonical"] + f"[{e['code']}]" + ("(부위)" if e.get("is_site") else "") for e in dicts["problem_subcategory_label"].entries.values()))
    A("")
    A("### 9.2 격리 목록 — 참조 해결, v1 vs v1.1 규칙 (v3 · 브론즈 2판으로 재실행)")
    A("")
    A("v1 = 완전 일치만. v1.1 규칙(§1.3 · v1.1 코드 그대로 — stopwords·회사 괄호·조합 기호는 §1.4 실측에서)을 v3 사전으로 `erd-v1.1-resolve.py` 를 2판 원장에 다시 돌린 수치. 2판에서 이름이 바뀐 참조(보톡스 이마+미간 · 보톡스(턱선+광대) · 필러 볼+턱 · 필러 팔자+볼)만 v2.4 와 다를 수 있다(v2.4 열 비교). 고민 자리·pih id 자리는 v1 규칙 그대로.")
    A("")
    A(RESOLVE.side_by_side(RES, v1rep))
    A("")
    A(f"합계(부위 사전·step1 제외): 미해결 참조(⑨) v1 **{TOTAL.get('unresolved_v1')}** → v1.1 규칙 **{TOTAL['unresolved_v1_1']}** · 분해 성공·항목 없음 **{TOTAL['decomposed_v1_1']}** · 해결 **{TOTAL['resolved_v1_1']}**. v2.4(1판): " + " · ".join(f"{k.split(' (')[0]} 미해결 {v['v2_4']['unresolved']}→{v['unresolved']}" for k, v in erd["resolution_report"].items() if v.get("v2_4") and v["v2_4"]["unresolved"] != v["unresolved"]) + " (그 밖 자리는 같다).")
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
    A("### 9.3 충돌 예상 수 (v1.1 그대로 재계산 · v2.2 rule_ref 열 · v2.3 닫는 kind 열 · v3 fold_approve 가 ⑦ 을 닫는다)")
    A("")
    A(md_table(["종류", "rule_ref", "무엇", "건", "닫는 결정 kind(v3)"], [(c["kind"], c["rule_ref"], c["what"], c["n"], c["close_kind"]) for c in CONF]))
    A("")
    A("v2.2 규칙 ④: 이 표는 원장 파일 단위 예상이다. 순위가 다른 출처끼리의 값 충돌은 실버 빌드가 레코드마다 ④ 로 자동 채택하면서 그때마다 conflict 를 남긴다. v2.3: 모든 conflict 는 stable_key 를 가지며 결정은 그 키로만 가리킨다. **v3(V3-10)**: fold_approve(approved)가 접는 anchor 쌍의 ⑦ duplicate_candidate 는 그 결정으로 닫힌다(status=resolved · decision_id) — 4차 빌드의 ⑦ open 156 중 fold_approve 21 이 닿는 쌍이 그 자리.")
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
    A("v2.4: 위 reclassified_to 가 적용돼도(⓪) 그 항목의 CAT- id 는 트리 위치의 계열 코드로 계산한 값 그대로다 — R2 만 바뀐다(§2.4 · 3-B′).")
    A("")
    A("### 9.5 시술 튜플 실측 (v3 · `erd-v3-tuples.py` 실제 실행 · 브론즈 2판 · v2.4(1판) 수치와 나란히 · 숫자는 목표가 아니다)")
    A("")
    A("규칙은 §1.4(v3: stopwords · 회사 괄호 · 조합 기호 확정 · layer 는 시술 site 아님). 분류 항목은 **자기 이름을 색인에서 제외**하고 분해했다. 접힘 조건은 「" + S.FOLD_CONDITION + "」. technique 는 이름 조각이 기법 사전에 닿은 것뿐(fragment " + str(ps["tuples_technique_origin"].get("fragment", 0)) + " / 튜플 " + str(ps["tuples_total"]) + "). M 코드·하위분류 id 만 적힌 참조 " + str(ps["code_references_node"]) + " 건은 노드 끝. v2.4 열은 `erd-v2.4-tuples.json`(1판)의 수치 — 바뀐 것은 §9.5.11 「v2.4 와 결과가 다른 참조 전부」에 원인과 함께.")
    A("")
    A(TUPLES.procedure_md(TUP, (v24tup or {}).get("procedure", {}).get("summary")))
    A("")
    A("### 9.6 부작용 튜플 실측 (구조 변경 ② · v2.4 원칙 A~D · **v3 V3-1 수식 칸 · V3-5 조직층** · `erd-v3-tuples.py` 실행 · v2.4 와 나란히)")
    A("")
    A("규칙은 §1.5(v3): 경과·부위·수식은 사건이 놓인 멤버 안의 조각만(원칙 C) · 한 칸에 후보가 둘이면 튜플 둘(원칙 B) · 붙지 않은 조각은 extra_* 보존 · raw_name 튜플은 칸 none/미상/none · 접힘은 네 칸 전부 사전 값일 때만(명시 예외 — none·미상·qualifier none 은 값) · 표현은 단위를 가리키기만(원칙 D). 사건 사전 뼈대는 complications 65 이름의 분해 조각(§4.1 · 동의어 「공기색전」만 뺌). **수식 칸이 기존 접힘·표현 연결을 깨지 않는지는 §9.6.7 의 v2.4 대조로 보인다.**")
    A("")
    A(TUPLES.adverse_md(TUP, va))
    A("")
    A("## 10. 검산 결과")
    A("")
    A("`erd-v3-check.py` 를 독립 실행한 출력을 그대로 붙였다(같은 폴더에서 `python3 erd-v3-check.py`). v2.4 검산 항목 전부(A 잎 키 행선지 · B 사전 값 출처 · C ERD 출처 키·표적 · D 브론즈 sha256(2판 HASHES.txt) · E 분해 규칙 재현 · F 처분 반영 · G 튜플 실측 재현 · H 구조 · I v2.1 · J v2.2 · K v2.3 · L v2.4 — v3 에서 바뀐 기대값은 항목 안에 적었다) + M v3 변경 10건(각각 반영 여부 + 실측: 수식 칸 접힘·exact 불변 · 회사 괄호 후보 전수 · stopwords locator · `+`/`/` 16건 · 조직층 · kind 17 · description/media_refs · R5 · anchor 규칙 · ⑦ 닫음 · 사용자 정의 3 과 명시 예외 유지 · 2판 잎 키 = 1판).")
    A("")
    return "\n".join(o)


def change_log(erd, dicts, TUP, colrows, v24erd, v24tup, moves3, notes3):
    o = []
    A = o.append
    ps, as_ = TUP["procedure"]["summary"], TUP["adverse"]["summary"]
    v = (v24tup or {}).get("procedure", {}).get("summary", {})
    va = (v24tup or {}).get("adverse", {}).get("summary", {})
    cmp = as_.get("v24_comparison") or {}
    cp = ps["company_paren"]
    st = ps["stopwords"]
    A("## 11. v2.4 → v3 변경 목록 (V3-# 대응 · 발주서 10건)")
    A("")
    A("| # | 무엇 | 어디서 반영 | v2.4 | v3 (실측) |")
    A("|---|---|---|---|---|")
    A(f"| V3-1 | 부작용 수식 칸 qualifier | {S.CHANGE_LIST[0][2]} | (event, site, course) · 「공기색전」= 색전 동의어 | (event, site, course, qualifier?) · 사전 adverse_qualifier {as_['qualifier_dictionary_values']}(공기·필러·지방·혈전·역행성 · 출처) · 식별자 네 칸 · 수식 든 이름 {as_['qualifier_names']} · 표현 {as_['qualifier_expressions']} · qualifier≠none 튜플 {as_['qualifier_tuples']} · 접두 가름 {len(as_['prefix_splits'])}(「공기색전」→ 공기 + 색전) · **v2.4 대조: 접힘 그룹 같음 {cmp.get('dict_fold_groups_same')} · raw 이름 같음 {cmp.get('raw_names_same')} · exact {cmp.get('exact_v24')} → {cmp.get('exact_v3')} · match_status 바뀐 표현 {len(cmp.get('match_status_diff', []))}** |")
    A(f"| V3-2 | 괄호 안 회사·제품 규칙 | {S.CHANGE_LIST[1][2]} | 제품 동의어 일치로만 우연히 | resolve_rules.company_paren · 후보 {cp['candidates']}(회사 닿음 {cp['touch_manufacturer']} · 제품 닿음 {cp['touch_product']} · 안 닿음 {cp['no_touch']}) · 적용 {cp['applied_n']} — 「엘러간」≠「앨러간/애브비」라 회사 동의어 dictionary_add 뒤 적용 |")
    A(f"| V3-3 | stopwords | {S.CHANGE_LIST[2][2]} | 미등록 조각 distinct {v.get('unregistered_distinct')} · 총 {v.get('unregistered_total')} | 단어 {st['words_total']}(locator 있음 {st['words_with_locator']}) · 미등록 조각 전 distinct {st['unregistered_distinct_before']}/총 {st['unregistered_total_before']} → 후 distinct {st['unregistered_distinct_after']}/총 {st['unregistered_total_after']} · 결과 바뀐 참조 {len(st['references_changed'])}(새로 튜플 {st['references_resolved_newly']}) · R12 session_index |")
    A(f"| V3-4 | 조합 기호 확정 · 부위 여럿 · member_mode | {S.CHANGE_LIST[3][2]} | `/` 뜻 미정(§12 scope_review) · 부위 둘 → multi_site ⑨ · combo_ref 에 and/or 없음 | 라벨 {ps['combo_labels']} 전수: {', '.join(f'{k} {n}' for k, n in ps['combo_by_result'].items())} · member_mode {', '.join(f'{k} {n}' for k, n in ps['combo_member_mode'].items())} · 「무엇을 하나 × 부위 여럿」 {len(ps['multi_tuples'])}(자리 기준 · 라벨 {' · '.join(dict.fromkeys(m['label'] for m in ps['multi_tuples']))}) · 괄호 안 대안 {len(ps['alternatives'])} · 2판 `+` 4곳: {' · '.join(dict.fromkeys(c['label'] + '→' + c['result'] for c in ps['combo_plus_v2']))} · 엣지 끝 and {ps['edge_ends_member_mode']['and']} · or {ps['edge_ends_member_mode']['or']} |")
    A(f"| V3-5 | 부위 kind · 조직층 5 | {S.CHANGE_LIST[4][2]} | 부위 21(backbone 11 + 라벨 10) · kind 없음 | 부위 {as_['site_dictionary_values']}({', '.join(f'{k} {n}' for k, n in as_['site_dictionary_by_kind'].items())}) · layer 값 피부·피하 지방층·근육·혈관·점막(출처) · 시술 site 칸의 layer {ps['tuples_layer_site']}(layer 조각 항목 {ps['catalog_with_layer_fragments']}) · 부작용 layer 튜플 {as_['layer_site_tuples']} · 후보 {as_['layer_site_candidates']} · 붙지 않은 layer 조각 {as_['layer_site_extra']} |")
    A(f"| V3-6 | canonical_rename | {S.CHANGE_LIST[5][2]} | kind 16 · 정준값 교체 수단 없음(dictionary_add 는 새 값) | kind {len(S.DECISION_KINDS)} · canonical_rename(target dictionary/code/canonical · new_value canonical/old_as_synonym/is_marketing_name) · 적용 ① · 값(M1·M3·M5)은 묶음 3 결정 |")
    A(f"| V3-7 | description · media_refs | {S.CHANGE_LIST[6][2]} | 없음 | product·technique 에 description(출처 locator 필수) · media_refs[](path·sha256·captured_at·source·kind ∈ photo/diagram/video/document) · 새 브론즈 원천 입구 · 지금은 null |")
    A(f"| V3-8 | 기법 상속 하위분류 단위 | {S.CHANGE_LIST[7][2]} | R5 modality → technique · 후보 scope = 계열 CAT- 목록 | R5 from modality\\|modality_subcategory · basis · 후보 {len(TUP['procedure']['inheritance_candidates'])} 계열 × 하위분류별 scope · M16 수액 = R5 기법 intravenous 하나지만 하위분류 {next((len(c['by_subcategory']) for c in TUP['procedure']['inheritance_candidates'] if c['from_ref'] == 'R5:M16'), 0)}(DCA·지방분해주사 포함) → 하위분류별·항목별 지정 자리 · R5 기법 둘 이상·없음 계열 {', '.join(ps['families_without_single_technique'])} |")
    A(f"| V3-9 | 결정 anchor 확장 | {S.CHANGE_LIST[8][2]} | anchor 가 튜플이 없으면 rejected(4차 HIFU 2건) | tuple_assign·tuple_assign_multi·adverse_tuple_assign 가 미해결·조합 anchor(REF- · REF-…#m<i>)에도 — 결정이 튜플을 세운다 · 미해결 참조 {ps['reference_total']['unresolved'] + ps['market_pricing']['unresolved']} 전부가 target 후보 |")
    A(f"| V3-10 | fold_approve 가 ⑦ 닫음 | {S.CHANGE_LIST[9][2]} | ⑦ 은 conflict_close(not_same)·fold_approve 로 닫는다고만 | fold_approve(approved) → 접는 anchor 쌍의 ⑦ status=resolved · decision_id · 규칙 ⑦ 문장 · conflict.status 비고 |")
    A(f"| — | 브론즈 | §1 · §6 · json bronze | 1판 phub-stg-2026-10-26 | **2판** bronze/phub-ledger(HASHES.txt 21 일치 · 1판과 다른 파일 {len(erd['bronze']['changed_from_v1'])} · 이름 6곳) · 2판 잎 키 재스캔 {erd['bronze_leaf_rescan']['leaf_count_v2']} = 1판 {erd['bronze_leaf_rescan']['leaf_count_v1']} · 파일별 차이 {len(erd['bronze_leaf_rescan']['diff'])} |")
    A(f"| — | 결정 레코드 | §5.3 | 25 | 25 이관 + DEC-26(v3 개정 · proposed) = {len(erd['decisions'])} |")
    A(f"| — | 행선지(column-map) | — | — | 이동 {len(moves3)}(변화 없음) · 비고 변경 {len(notes3)} |")
    A(f"| — | 사전 | §4 | 46 | **{len(dicts)}**(+adverse_qualifier) · 값 변경 셋(조직층 5 · 수식 5 · 「공기색전」 동의어 제거) · 그 밖 불변(검산 M-11) |")
    A(f"| — | 실측 시술 | §9.5 | 521 → {v.get('catalog_distinct_tuples')} · 튜플 {v.get('tuples_total')} · 엣지 끝 {v.get('edge_ends_total_n')} | 521 → {ps['catalog_distinct_tuples']} · 튜플 {ps['tuples_total']} · 엣지 끝 {ps['edge_ends_total_n']}: {', '.join(f'{k}={n}' for k, n in ps['edge_ends_total'].items())} · 참조 ② 미해결 {v.get('reference_total', {}).get('unresolved')} → {ps['reference_total']['unresolved']} · ③ {v.get('market_pricing', {}).get('unresolved')} → {ps['market_pricing']['unresolved']} · v2.4 와 다른 참조 {len(ps['v24_reference_changes'])} |")
    A(f"| — | 실측 부작용 | §9.6 | 65 → {va.get('complications_distinct_tuples')} · 튜플 {va.get('tuples_total')} · exact {va.get('expressions_total', {}).get('linked')} | 65 → {as_['complications_distinct_tuples']}(사전 {as_['complications_distinct_tuples_dict']} + raw {as_['complications_distinct_tuples_raw']}) · 튜플 {as_['tuples_total']} · exact {as_['expressions_total']['linked']} · 표현 유래 0 |")
    A("| — | 생성기·검산 | — | `*_v24.py` · `erd-v2.4-tuples.py` · `erd-v2.4-check.py` | `erd_spec_v3.py`·`erd_colmap_v3.py`·`erd_build_v3.py` · `erd-v3-tuples.py` · `erd-v3-check.py`(v2.4 항목 전부 + M) |")
    A("")
    A("**검토 반영 R-1~R-4**(`erd-v3-review.md` · 판 번호 v3 그대로 · 실측 재실행 없음): R-1 §1.1 결정 target 규칙·§5.2 tuple_assign/tuple_assign_multi·fold_approve anchors 에 `REF-…#s<i>` 명시 · R-2 canonical_rename = 코드 기반 개체 id 유지 + DIC- id 재계산·옛 id alias(§1.1 id_rule.dictionary_entry · §5.2) · R-3 tuple_assign_multi 비고 = 같은 what × 부위 여럿이면 multi_tuple(R12 and · #s<i>), 대안·함께면 combo_ref(new_value.member_mode) · R-4 §0 에 v3 승계 문장(정의 2 세 칸 + 선택 수식 칸 · 정의 3 kind 17), R30·target 규칙의 「세 쌍」→ 네 쌍.")
    A("")
    A("개체 21 · 관계 31 · 잎 키 1,072 의 수는 그대로다. 사용자 정의 3 과 명시 예외는 뜻 그대로(§0 동결 원문 + v3 승계 문장 · 검산 M-12). 이전 판 산출물·생성기는 지우지 않았다. v2.3 → v2.4 변경 목록은 `erd-v2.4.md` §11.")
    A("")
    A("## 12. v3 밖 관찰 — 결정 레코드로 갈 것 · 다음 판 후보 (이번 범위 아님 · 레코드는 만들지 않았다)")
    A("")
    rows = [
        ("V3-2 후속", "회사 사전 동의어 「엘러간」→「앨러간/애브비」 · 「더모톡신」은 회사가 아니라 시술/기법(묶음 3 후보) — 규칙이 적용되려면 사전 값이 먼저", "dictionary_add(manufacturer)", "§9.5.9 후보 표"),
        ("V3-3 후속", "stopwords 가 떼도 남는 조각(HIFU · RF · 필링 · MTS · LED · 두피 · 바디 …)은 사전 값 결정 — 실버 묶음 1·2A 가 이미 일부를 넣었다(ERD 사전은 그대로)", "dictionary_add", "§9.5.7"),
        ("V3-4 후속", "「필러 팔자+볼」의 「팔자」(부위 사전 팔자주름의 동의어?) · 「HIFU(슈링크/울쎄라)」류 바깥 조각 미등록 → 사전 뒤 규칙 적용 또는 tuple_assign_multi(미해결 anchor · V3-9)", "dictionary_add(site) · tuple_assign_multi", "§9.5.11"),
        ("V3-5 후속", "「혈관 막힘으로 인한 피부 괴사」의 후보 (괴사, 혈관) 처럼 원인 자리의 층 조각이 같은 멤버라 부위 후보가 되는 표현(§9.6.8 · 단위 없음 · 결정에서 거름) · 「피부 괴사」「지방괴사」→ (괴사, 피부)·(괴사, 피하 지방층) 지정 · region 값 바디·두피 추가 · 「교근」→ 사각턱 동의어", "adverse_tuple_assign · dictionary_add(site)", "§9.6.8 · _batch3 후보"),
        ("V3-1 후속", "접두 가름이 「혈전정맥염」→ 혈전 + 정맥염 도 낸다(규칙 결과 · 후보 (정맥염, none, 미상, 혈전) 은 단위 없음 · 사람이 볼 것) · 「섬유화」(경결 동의어)를 기전 수식으로 옮길지 · 「필러 색전」「지방 색전증」 표현의 후보 단위(색전, none, 미상, 필러/지방)를 세울지(adverse_tuple_assign kind=expression · 결정이 단위를 세운다) · 수식 사전 확장(세균 · 바이러스 · 헤르페스 …)", "event_split · adverse_tuple_assign · dictionary_add(adverse_qualifier)", "§9.6.7"),
        ("V3-6 값", "M1 「보톡스」→「보툴리눔 톡신」 · M3 → 「바이오스티뮬레이터」 · M5 → 「자가혈 유래 시술」(묶음 3 결정 · is_marketing_name 콜라겐부스터)", "canonical_rename", "§5.2"),
        ("V3-7 값", "현장 기기 사진 109장(reference/2026-10-27-reference-image)·기법 설명을 조사 파일(research_artifact)로 등록해 locator 를 준 뒤 채운다", "새 브론즈 원천 등록(§5.1 표)", "§2.5 · §2.6"),
        ("V3-8 값", "M16 수액 하위분류별 기본 기법(intravenous vs 피하/근육) · 후보 9계열의 하위분류별 승인", "canonical_mapping(R5:<하위분류 id>)", "§9.5.6"),
        ("동결 §12 승계", "1-C 보톡스 product↔modality · 1-D 엑셀V+ · 1-E 같은 세 칸 다른 anchor · 2-C 사건 동의어 분리(과민반응·동상·지방괴사·섬유화) · 2-D none·미상 식별자(명시 예외로 닫힘) · 볼뉴머 M4/M9 · 엠페이스류 · R30 인과 · DEC-20~26 승인 · 제품 사전 확장", "v2.4 §12 그대로", "결정 레코드"),
        ("원천 수정 요청", "원장의 `/` 가 두 뜻(부위 함께·대안)으로 섞여 쓰임 — 2판이 부위 나열 6곳을 `+` 로 고쳤다. 남은 `/` 는 전부 대안으로 읽는다(V3-4) — 남은 부위 나열 `/` 가 있으면 CHANGELOG 로", "원천(브론즈 판)", "§9.5.11 전수 표"),
        ("§9.2", "v1.1 코드(erd-v1.1-resolve.py)는 stopwords·조합 규칙을 모른다 — §9.2 는 v1.1 수치 연속성용이고 v3 규칙 실측은 §9.5. 다음 판에서 §9.2 를 v3 규칙으로 통일할지", "scope_review", "문구"),
    ]
    A(md_table(["어디", "무엇", "decision kind / 자리", "근거"], rows))
    A("")
    A("전부 kind 와 target 자리가 정해진 목록이다 — v3 의 kind 17 과 안정 키 규칙(미해결·조합 REF- 포함)으로 전부 담긴다.")
    return "\n".join(o)


def main():
    v1erd = json.load(open(os.path.join(WORK, "erd-v1.json"), encoding="utf-8"))
    v11erd = json.load(open(os.path.join(WORK, "erd-v1.1.json"), encoding="utf-8"))
    v24erd = json.load(open(os.path.join(WORK, "erd-v2.4.json"), encoding="utf-8"))
    v24tup = json.load(open(os.path.join(WORK, "erd-v2.4-tuples.json"), encoding="utf-8"))
    bronze = bronze_meta()
    assert not bronze["mismatch"], f"브론즈 2판 HASHES.txt 불일치: {bronze['mismatch']}"
    rescan = rescan_v2()
    step1_scan = B11.scan_step1()
    colrows = build_column_map(step1_scan)
    dicts = build_dictionaries_v3()
    erd, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, moves, moves22, moves23, moves24, moves3, notes3 = write_outputs(colrows, dicts, step1_scan, v1erd, v11erd, v24erd, v24tup, bronze, rescan)
    md = build_erd_md(erd, colrows, dicts, RES, TOTAL, TUP, CONF, Q14, SITE_TABLE, v1erd, moves, v24tup, moves3, notes3)
    cl = change_log(erd, dicts, TUP, colrows, v24erd, v24tup, moves3, notes3)
    open(os.path.join(WORK, OUT["md"]), "w", encoding="utf-8").write(md + "(검산 실행 중)\n\n" + cl + "\n")
    chk = load_module("chk3", os.path.join(WORK, OUT["check"]))
    ok, report = chk.run_checks()
    md += report + "\n\n" + cl + "\n"
    open(os.path.join(WORK, OUT["md"]), "w", encoding="utf-8").write(md)
    with open(os.path.join(WORK, OUT["cmap"]), "a", encoding="utf-8") as f:
        f.write("## 검산 결과\n\n" + report + "\n")
    print("OK" if ok else "FAIL")
    print(report)
    print("dests", Counter(r["dest"] for r in colrows), "moves3", len(moves3), "notes3", len(notes3))
    print("dicts", len(dicts), "entities", len(S.ENTITIES), "relations", len(S.RELATIONS), "decisions", len(erd["decisions"]), "kinds", len(S.DECISION_KINDS))
    ps, as_ = TUP["procedure"]["summary"], TUP["adverse"]["summary"]
    print("procedure: catalog", ps["catalog_items"], "->", ps["catalog_distinct_tuples"], "| tuples", ps["tuples_total"], "| edge ends", ps["edge_ends_total"], ps["edge_ends_total_n"], "| combo", ps["combo_by_result"], "| stop", ps["stopwords"]["unregistered_total_before"], "->", ps["stopwords"]["unregistered_total_after"], "| company", ps["company_paren"]["applied_n"])
    print("adverse: 65 ->", as_["complications_distinct_tuples"], "| tuples", as_["tuples_total"], "| exact", as_["expressions_total"]["linked"], "| qualifier names", as_["qualifier_names"], "| cmp", {k: v for k, v in (as_.get("v24_comparison") or {}).items() if "diff" not in k})


if __name__ == "__main__":
    main()
