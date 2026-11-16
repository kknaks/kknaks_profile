# -*- coding: utf-8 -*-
"""ERD v1.1 산출물 생성기. v1 생성기(erd_build.py)의 함수·사전 빌더를 재사용하고 A·B·C 변경분만 덧씌운다.
입력: 원장 21 + step1-products.json + 스캔 JSON + erd_spec_v11/erd_colmap_v11 + erd-v1.json(나란히 비교)
출력: erd-v1.1.md · erd-v1.1.json · erd-v1.1-column-map.md · erd-v1.1-dictionaries.json · erd-v1.1-resolve.json(+검산 결과 부착)
"""
import hashlib
import importlib.util
import json
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_build as B  # noqa  (v1 함수·원장 로드 재사용. v1 산출물은 다시 쓰지 않는다)
import erd_spec_v11 as S  # noqa
import erd_colmap_v11 as C  # noqa

WORK = HERE
LEDGER = S.LEDGER_DIR
STEP1 = S.STEP1_FILE
norm, mkid, sha256, values_at, distinct_at, md_table = B.norm, B.mkid, B.sha256, B.values_at, B.distinct_at, B.md_table
Dict_, simple_enum = B.Dict_, B.simple_enum
L = B.L
L[STEP1] = json.load(open(os.path.join(WORK, STEP1), encoding="utf-8"))
SCAN = B.SCAN
FILES = B.FILES


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


RESOLVE = load_module("erd_v11_resolve", os.path.join(WORK, "erd-v1.1-resolve.py"))
SCANNER = load_module("bronze_scan", os.path.join(WORK, "bronze-ledger-column-scan.py"))


def scan_step1():
    """bronze-ledger-column-scan.py 의 FileScan 을 그대로 써서 step1 잎 키를 센다 (같은 방식)."""
    return SCANNER.FileScan(os.path.join(WORK, STEP1)).run()


# ---------------------------------------------------------------------------
# 사전 — v1 빌더 실행 후 site · technique 재작성, 사전 7개 추가
# ---------------------------------------------------------------------------
def build_dictionaries_v11():
    DICTS = B.build_dictionaries()
    tx = L["taxonomy.json"]
    # --- site (8-2)
    d = Dict_("site", "부위", "8-2 처분: 뼈대 = anatomy 11 zone(kind=backbone) + taxonomy 부위 라벨 10(kind=taxonomy_site_label). 「(확장)」 정준값 0. 부위가 아닌 하위분류 라벨 41 은 problem_subcategory_label 로(§8-2 표). 복합 라벨은 `/` 분해 멤버")
    for z in L["anatomy-danger-zones.json"]["zones"]:
        d.add_canonical(z["name_ko"], "anatomy-danger-zones.json", "zones[].name_ko", 1, site_kind="backbone", zone_id=z["id"], name_en=z["name_en"], members=None)
        d.add_synonym(norm(z["name_ko"]), z["id"], "anatomy-danger-zones.json", "zones[].id", 1, link="id-join")
        d.add_synonym(norm(z["name_ko"]), z["name_en"], "anatomy-danger-zones.json", "zones[].name_en", 1, link="id-join")
    keep = {norm(x) for x in S.SITE_LABELS_KEEP}
    cc_counts = distinct_at("problem-packages.json", "problems[].complaints[].cc_group")
    lab_counts = distinct_at("taxonomy.json", "problem[].subcategories[].label")
    for v, n in lab_counts.items():
        if norm(v) not in keep:
            continue
        e = d.find(v)
        if e is not None:
            d.add_synonym(norm(e["canonical"]), v, "taxonomy.json", "problem[].subcategories[].label", n, link="exact")
        else:
            d.add_canonical(v, "taxonomy.json", "problem[].subcategories[].label", n, site_kind="taxonomy_site_label", members=None)
        if v in cc_counts:
            d.add_synonym(norm(d.find(v)["canonical"]), v, "problem-packages.json", "problems[].complaints[].cc_group", cc_counts[v], link="exact")
    for e in d.entries.values():
        if "/" in e["canonical"]:
            parts = [p.strip() for p in e["canonical"].split("/")]
            found = [d.find(p) for p in parts]
            e["members"] = [f["canonical"] for f in found] if all(found) and all(f["canonical"] != e["canonical"] for f in found) else None
    # --- technique (8-4)
    d = Dict_("technique", "기법", "8-4 처분: 원장에서 기법 키(mechanism)로 명시된 값만 — procedure-profiles mechanism[] 12. 하위분류 label·energy_device type·pih subcategory 는 뺐다")
    for v, n in distinct_at("procedure-profiles.json", "profiles[].mechanism[]").items():
        d.add_canonical(v, "procedure-profiles.json", "profiles[].mechanism[]", n)
    # --- problem_subcategory_label (8-2 재배치 행선지)
    d = Dict_("problem_subcategory_label", "고민 하위분류 라벨", "정준값 = taxonomy problem[].subcategories[].label 53(코드 연결). problem-packages cc_group 은 (problem_id, label) 일치로 동의어 등록(= R7 그룹). 부위 라벨 10 은 site 사전에도")
    cc_pairs = Counter()
    for v, ctx in values_at("problem-packages.json", "problems[].complaints[].cc_group"):
        pid = next(p for p in ctx["parents"] if isinstance(p, dict) and "problem_id" in p)["problem_id"]
        cc_pairs[(pid, v)] += 1
    for p in tx["problem"]:
        for sc in p["subcategories"]:
            e = d.add_canonical(sc["label"], "taxonomy.json", "problem[].subcategories[].label", 1, code=p["id"], subcategory_id=sc["id"], is_site=norm(sc["label"]) in keep)
            if e["code"] != p["id"]:
                e["code"] = e["code"] + "|" + p["id"]
            d.add_synonym(norm(sc["label"]), sc["id"], "taxonomy.json", "problem[].subcategories[].id", 1, link="code")
            if (p["id"], sc["label"]) in cc_pairs:
                d.add_synonym(norm(sc["label"]), sc["label"], "problem-packages.json", "problems[].complaints[].cc_group", cc_pairs[(p["id"], sc["label"])], link="exact(problem_id+label)")
    # --- 이름 색인 3 (B 분해 규칙이 읽는 개체 이름 사전)
    d = Dict_("product_name", "제품명 색인", "B 규칙 사전 순서 1. 개체 product 의 이름 색인(taxonomy modality[].products + products.json). code = 계열(여러 계열이면 `|`). name_en 동의어", )
    d.kind = "entity_name_index"
    for m in tx["modality"]:
        for pr in m["products"]:
            e = d.add_canonical(pr["name"], "taxonomy.json", "modality[].products[].name", 1, code=m["id"])
            if m["id"] not in e["code"].split("|"):
                e["code"] += "|" + m["id"]
            if pr.get("name_en"):
                d.add_synonym(norm(pr["name"]), pr["name_en"], "taxonomy.json", "modality[].products[].name_en", 1)
    for sec, body in L["products.json"].items():
        if isinstance(body, dict):
            cid = body["category_id"]
            cid = cid if isinstance(cid, str) else "|".join(cid)
            for pr in body["products"]:
                e = d.find(pr["name"])
                if e is None:
                    e = d.add_canonical(pr["name"], "products.json", f"{sec}.products[].name", 1, code=cid)
                else:
                    d.add_synonym(norm(e["canonical"]), pr["name"], "products.json", f"{sec}.products[].name", 1, link="exact")
                if pr.get("name_en"):
                    d.add_synonym(norm(e["canonical"]), pr["name_en"], "products.json", f"{sec}.products[].name_en", 1)
    d = Dict_("modality_subcategory_label", "계열 하위분류 라벨 색인", "B 규칙 사전 순서 2. 개체 modality_subcategory 의 label 색인. 같은 라벨이 여러 계열(기타·추가)이면 code `|`. 하위분류 id 는 link=code 동의어")
    d.kind = "entity_name_index"
    for m in tx["modality"]:
        for sc in m["subcategories"]:
            e = d.add_canonical(sc["label"], "taxonomy.json", "modality[].subcategories[].label", 1, code=m["id"])
            if m["id"] not in e["code"].split("|"):
                e["code"] += "|" + m["id"]
            d.add_synonym(norm(sc["label"]), sc["id"], "taxonomy.json", "modality[].subcategories[].id", 1, link="code")
    d = Dict_("procedure_name", "단위 시술명 색인", "B 규칙 사전 순서 3. 개체 procedure 의 이름 색인(taxonomy 항목 521). 중복 이름(볼뉴머)은 code `|`")
    d.kind = "entity_name_index"
    for m in tx["modality"]:
        for sc in m["subcategories"]:
            for it in sc["items"]:
                e = d.add_canonical(it["name"], "taxonomy.json", "modality[].subcategories[].items[].name", 1, code=m["id"])
                if m["id"] not in e["code"].split("|"):
                    e["code"] += "|" + m["id"]
    # --- step1 허가 사전 3 (C)
    simple_enum("license_status", "허가 상태(step1 판정)", [(STEP1, "items[].4_license.status")], note="C: 「확인 불가」도 값 그대로(null 아님). 신뢰 3(판정)")
    simple_enum("license_kind", "허가 종류", [(STEP1, "items[].4_license.kind"), (STEP1, "items[].4_license.licenses[].kind"), (STEP1, "items[].4_license.history[].kind")], note="의약품/의료기기. null = 미입력")
    simple_enum("license_state", "허가 건 상태", [(STEP1, "items[].4_license.licenses[].state"), (STEP1, "items[].4_license.history[].state")], note="연결 허가는 전부 `정상`, 이력 허가는 취소·취하·만료. `취하 2013-06-30` 처럼 날짜가 붙은 값은 원문 보존(③ 분해는 실버 빌더)")
    return DICTS


def site_replacement_table(DICTS):
    """8-2: v1 확장 51 의 처분 표."""
    v1 = json.load(open(os.path.join(WORK, "erd-v1-dictionaries.json"), encoding="utf-8"))
    v1site = next(d for d in v1["dictionaries"] if d["name"] == "site")
    ext = [e for e in v1site["entries"] if not e.get("is_backbone")]
    psl = DICTS["problem_subcategory_label"]
    rows = []
    for e in ext:
        v = e["canonical"]
        kept = DICTS["site"].find(v)
        pe = psl.find(v)
        cc_n = sum(s["n"] for s in e["sources"] if s["file"] == "problem-packages.json")
        if kept and kept.get("site_kind") == "taxonomy_site_label":
            dest = "부위 사전 유지 (taxonomy 부위 라벨)" + (f" · 멤버 {'+'.join(kept['members'])}" if kept.get("members") else "")
        else:
            dest = f"problem_subcategory_label ({pe['code']} 하위분류 {pe.get('subcategory_id')})" if pe else "problem_subcategory_label"
        rows.append({"value": v, "cc_group_n": cc_n, "dest": dest, "reason": "실제 해부 부위" if kept and kept.get("site_kind") == "taxonomy_site_label" else "증상·치료 유형·목적 라벨 — 부위 아님"})
    return rows


# ---------------------------------------------------------------------------
# 행선지 표 (원장 21 + step1)
# ---------------------------------------------------------------------------
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


def q14_bundles_v11():
    rows = B.q14_bundles()
    oral = {norm(x) for x in S.Q14_ORAL_DRUGS}
    for r in rows:
        if norm(r["name"]) in oral:
            r["bucket"] = "② 계열 없음 격리(범위 검토)"
            r["matched"] = ["경구약(8-5 처분)"]
        if r["bucket"].startswith("②"):
            r["scope"] = "피부과 허브 범위 밖 — 범위 검토"
        else:
            r["scope"] = ""
    return rows


def conflict_estimates_v11(IDX, RES):
    E = B.conflict_estimates(IDX)
    n_conf = sum(1 for _ in values_at(STEP1, "items[].6_companies.conflicts[].field"))
    E.append({"kind": "value_conflict", "what": "step1 6_companies.conflicts — 허가 제조사 vs 다른 출처(「덮어쓰지 않음」 그대로 적재)", "n": n_conf, "detail": []})
    st = RES["step1-products.items[] display/ledger/search 이름 → 원장 제품 (395)"]
    amb = [r["label"] for r in st["rows"] if r["status"] == "unresolved" and any("모호" in u.get("reason", "") for u in r["untouched"])]
    E.append({"kind": "unresolved_reference", "what": "step1 이름이 둘 이상 계열의 원장 제품/항목에 닿아 모호(계열 힌트 없음)", "n": len(amb), "detail": amb})
    return E


def mermaid():
    return B.mermaid().replace("MODALITY }o--o{ TECHNIQUE", "MODALITY }o--o{ TECHNIQUE")


# ---------------------------------------------------------------------------
# 산출물
# ---------------------------------------------------------------------------
def write_outputs(colrows, dicts, step1_scan, v1erd):
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
    # dictionaries 먼저 (resolve 가 읽는다)
    dj = OrderedDict([("erd_version", S.ERD_VERSION), ("bronze_snapshot", S.SNAPSHOT), ("normalize_rule", S.NORMALIZE_RULE["name"]),
                      ("source_kinds", {"value": "그 경로의 값 자체", "key": "그 경로의 키 이름(또는 섹션 키)이 값 — 단수/복수 차이 허용", "derived": "그 경로의 합성값에서 ③ 형식 교정으로 잘라낸 부분값(원문의 부분 문자열)"}),
                      ("dictionary_kinds", {"value": "값 사전(열거·라벨)", "entity_name_index": "개체 이름 색인 — B 분해 규칙이 읽는 제품·하위분류·단위 시술 이름(개체의 식별 이름을 사전 모양으로 노출)"}),
                      ("dictionaries", [dict(d.to_json(), kind=getattr(d, "kind", "value")) for d in dicts.values()])])
    json.dump(dj, open(os.path.join(WORK, "erd-v1.1-dictionaries.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # resolve (B)
    dic_json = json.load(open(os.path.join(WORK, "erd-v1.1-dictionaries.json"), encoding="utf-8"))
    v1rep = v1erd.get("resolution_report") if v1erd else None
    RES, TOTAL = RESOLVE.run_all(dic_json, S.RESOLVE_RULES, L, L[STEP1], v1rep)
    json.dump({"erd_version": S.ERD_VERSION, "rules": S.RESOLVE_RULES["name"], "slots": RES, "total": TOTAL}, open(os.path.join(WORK, "erd-v1.1-resolve.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    IDX = B.Index()
    CONF = conflict_estimates_v11(IDX, RES)
    Q14 = q14_bundles_v11()
    SITE_TABLE = site_replacement_table(dicts)
    res_summary = OrderedDict()
    for k, v in RES.items():
        res_summary[k] = {kk: vv for kk, vv in v.items() if kk != "rows"}
        res_summary[k]["v1"] = ({"n": v1rep[k]["n"], "resolved": v1rep[k]["resolved"], "unresolved": v1rep[k]["unresolved"], "by_depth": v1rep[k]["by_depth"]} if v1rep and k in v1rep else None)
    decisions = []
    for no, (who, what, where) in S.DISPOSITIONS.items():
        decisions.append({"id": f"DEC-2026-11-04-{no:02d}", "kind": "scope_review" if no in (2, 4, 5) else "conflict_resolution", "what": f"재검토 8-{no}: {what}", "why": "ERD v1.1 발주서 §A (사용자 승인 「그렇게 진행하자」)",
                          "who": "사용자" if who == "사용자" else "워커 처리 · 사용자 승인", "when": "2026-11-04", "applies_to": where, "status": "applied(v1.1)"})
    erd = OrderedDict([
        ("erd_version", S.ERD_VERSION), ("previous_version", "v1"), ("status", "draft — 사용자 승인 전"), ("written", "2026-11-04"), ("bronze_snapshot", S.SNAPSHOT),
        ("layers", {"bronze": "원장 21 그대로 + 조사 산출물 step1-products.json 1 (바이트 보존, SHA256 식별)", "semantic": "이 ERD + 값 사전 + 분해 규칙, 승인이 정본 조건, 버전 개정", "silver": "ERD 를 따르는 정규화 레코드, 모든 값에 (file, path) 출처", "gold": "실버 조합 뷰, 새 사실 금지"}),
        ("normalize_rule", S.NORMALIZE_RULE), ("id_rule", S.ID_RULE), ("resolve_rules", S.RESOLVE_RULES),
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
        ("dictionaries_summary", [{"name": d.name, "label": d.label, "kind": getattr(d, "kind", "value"), "canonical": len(d.entries), "synonyms": sum(len(e["synonyms"]) for e in d.entries.values()), "candidates": len(d.candidates)} for d in dicts.values()]),
        ("resolution_report", res_summary), ("resolution_total", TOTAL),
        ("conflict_estimates", CONF),
    ])
    json.dump(erd, open(os.path.join(WORK, "erd-v1.1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    # column map md
    md = ["# ERD v1.1 — 잎 키 행선지 표 (원장 21 + step1-products.json)", "",
          f"작성 2026-11-04 · 입력 `bronze-ledger-column-scan.json`(원장 잎 키 {sum(1 for r in colrows if r['file'] != STEP1)}) + `step1-products.json` 잎 키 {step1_scan['leaf_count']}(`bronze-ledger-column-scan.py` 와 같은 방식으로 스캔) = {len(colrows)} · 행선지 범주 5: 개체 / 사전 / 엣지 / 브론즈 / 버림 · **미정 0**", "",
          "표적 표기: `entity.attr` · `dict:<사전>` · `R#.attr`(관계 번호는 erd-v1.1.md §3) · `bronze` · `drop`. v1 과 달라진 원장 행 6: cc_group(8-2) · problem 하위분류 label · modality 하위분류 label(8-4) · energy_device type(8-4) · pih subcategory(8-4) · profiles mechanism[](8-4).", "",
          "## 요약", "", md_table(["행선지", "원장 21", "step1", "합계"], [(k, sum(1 for r in colrows if r["dest"] == k and r["file"] != STEP1), sum(1 for r in colrows if r["dest"] == k and r["file"] == STEP1), v) for k, v in sorted(dest_counter.items(), key=lambda x: -x[1])] + [("합계", sum(1 for r in colrows if r["file"] != STEP1), sum(1 for r in colrows if r["file"] == STEP1), len(colrows))]), ""]
    for f in FILES + [STEP1]:
        rs = [r for r in colrows if r["file"] == f]
        md.append(f"## `{f}` — 잎 키 {len(rs)}" + (" (조사 산출물 · 22번째 브론즈 원천)" if f == STEP1 else ""))
        md.append("")
        md.append(md_table(["#", "경로", "타입", "횟수", "행선지", "표적", "비고"], [(i + 1, f"`{r['path']}`", r["type"], r["count"], r["dest"], f"`{r['target']}`", r["note"]) for i, r in enumerate(rs)]))
        md.append("")
    open(os.path.join(WORK, "erd-v1.1-column-map.md"), "w", encoding="utf-8").write("\n".join(md))
    return erd, RES, TOTAL, CONF, Q14, SITE_TABLE


# ---------------------------------------------------------------------------
# erd-v1.1.md
# ---------------------------------------------------------------------------
def build_erd_md(erd, colrows, dicts, RES, TOTAL, CONF, Q14, SITE_TABLE, v1erd):
    o = []
    A = o.append
    v1rep = v1erd.get("resolution_report", {}) if v1erd else {}
    A("# ERD v1.1 — 피부과 시술 허브 메달리온 시맨틱 정의")
    A("")
    A("작성 2026-11-04 · 상태 **초안(사용자 승인 전)** · 브론즈 스냅샷 2026-10-26 (+ 조사 산출물 step1 10-29) · 발주서 `erd-v1.1-brief.md` (v1 발주서 `erd-v1-brief.md` 의 기준·금지·기본값 유지)")
    A("")
    A("기계용 동본 `erd-v1.1.json` · 값 사전 `erd-v1.1-dictionaries.json` · 잎 키 행선지 `erd-v1.1-column-map.md` · 분해 규칙 실행 `erd-v1.1-resolve.py`(결과 `erd-v1.1-resolve.json`) · 검산 `erd-v1.1-check.py` (결과 §10). v1 산출물은 그대로 두었다. 변경 목록은 §11.")
    A("")
    A("## 1. 범위와 층")
    A("")
    A("| 층 | 무엇 | 규칙 |")
    A("|---|---|---|")
    A("| 브론즈 | 원장 21개 JSON 그대로 + `step1-products.json`(조사 산출물) | 바이트 보존·수정 금지. 파일 SHA256 이 식별자(§6 표). 원장 스냅샷 2026-10-26, step1 10-29 |")
    A("| 시맨틱 | 이 ERD + 값 사전 + 분해 규칙(§1.3) | 문서. 사용자 승인이 정본 조건. 버전으로 개정(v1 → v1.1 → …) |")
    A("| 실버 | ERD 를 따르는 정규화 레코드 | **모든 값은 (파일, 잎 키 경로) 출처를 가진다.** 출처 없는 값 금지. 충돌은 둘 다 보관 |")
    A("| 골드 | 실버 조합 뷰 | 실버에 없는 사실을 만들지 않는다. 충돌 미판정 레코드 제외 |")
    A("")
    A("지식은 원장 21개·컬럼 리포트·v1 산출물·`step1-products.json` 에서만 가져왔다. step2·step3·source-map·DATA-001·DEC-*·silver-*·`_archive/` 는 열지 않았다.")
    A("")
    A("### 1.1 정규화(「같은 것」판정)와 식별자")
    A("")
    A(f"- 정규화 `{S.NORMALIZE_RULE['name']}`: " + " → ".join(S.NORMALIZE_RULE["steps"]))
    A(f"- {S.NORMALIZE_RULE['note']}")
    A(f"- 식별자: `{S.ID_RULE['format']}`. canonical_key 는 개체별(§2 각 표의 「식별자」). {S.ID_RULE['canonical_key']}")
    A(f"- survey 제품: {S.ID_RULE['survey_products']}")
    A("- 「같은 것」 = 정규화 완전 일치(①) + 사전 동의어(②)만 자동. 참조 문자열은 §1.3 분해 규칙으로 조각내어 조각 단위로 같은 판정을 한다. 유사도·추측 매칭은 ⑦ 후보로만.")
    A("")
    A("### 1.2 다이어그램 (개체·관계만)")
    A("")
    A("```mermaid")
    A(mermaid())
    A("```")
    A("")
    A("### 1.3 참조 해결 — 결정론 분해 규칙 (B · 규칙 ⑨ 개정)")
    A("")
    R = S.RESOLVE_RULES
    A("v1 은 「완전 일치만」이었다. v1.1 은 아래 세 단계를 **데이터**(`erd-v1.1.json → resolve_rules`)로 적고 `erd-v1.1-resolve.py` 가 그대로 실행한다. 실버 빌더도 같은 데이터를 읽는다. 유사도·추측은 없다.")
    A("")
    A(f"1. **계열 확정** — {R['step1_family']['what']}. 자리별 힌트: " + " · ".join(f"{k}: `{v}`" for k, v in R["step1_family"]["slot_hints"].items()) + f". 코드 정규식 `{R['step1_family']['code_regex']}`")
    A(f"2. **이름 분해** — 괄호 안을 뗀다(`{R['step2_decompose']['paren_regex']}`). 조합 기호 `{'` `'.join(R['step2_decompose']['combo_symbols'])}` 로 멤버를 나눈다. 조각마다 사전 순서 **{' → '.join(R['step2_decompose']['dictionary_order'])}** 로 완전 일치를 시도한다(계열 사전에 닿으면 kind=modality). 규격 정규식 `{R['step2_decompose']['spec_regex']}` + unit 사전. {R['step2_decompose']['secondary_rule']}. {R['step2_decompose']['scope_rule']}. {R['step2_decompose']['overlap_rule']}.")
    A(f"3. **조립** — 튜플 ({', '.join(R['step3_assemble']['tuple'])}). (a) resolved: {R['step3_assemble']['resolved']} (b) 분해 성공·항목 없음: {R['step3_assemble']['decomposed']} (c) unresolved: {R['step3_assemble']['unresolved']}")
    A("")
    A("결과는 §9.2 에 v1 수치와 나란히. 실버 빌더는 (b) 의 튜플을 그대로 레코드로 보존하고 가격·시너지·순서를 그 조합에 단다.")
    A("")
    A("## 2. 개체 목록")
    A("")
    A(f"개체 {len(S.ENTITIES)}개 (v1 과 같은 19). 발주서 최소 목록 11 + 추가 {sum(1 for e in S.ENTITIES if e.get('beyond_minimum'))}(표시 ★). v1.1 에서 속성이 바뀐 개체: source_file(kind·trust_flag) · product(step1 출처 키 11 속성 추가 · origin) · technique(8-4) · site(8-2) · modality_subcategory · problem_subcategory · complaint(cc_group_raw) · conflict(step1 회사 충돌) · citation(step1 URL).")
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
    A(f"관계 {len(S.RELATIONS)}개 (v1 과 같은 25). `proc_axis` = modality | modality_subcategory | procedure | product. 시너지·순서·간격·시술간 금기는 **R18 하나**의 `kind` 속성. 참조 끝점은 §1.3 규칙으로 정해지고, 「분해 성공·항목 없음」이면 엣지가 튜플(조합)을 가리킨다.")
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
    A(f"전부 `erd-v1.1-dictionaries.json`. 값 사전 {nval} + 개체 이름 색인 {nidx}(B 분해 규칙이 읽는 제품명·하위분류 라벨·단위 시술명) = {len(dicts)}. v1 36 → v1.1 {len(dicts)}: 추가 problem_subcategory_label(8-2) · license_status · license_kind · license_state(C) · 이름 색인 3(B). 바뀐 사전: site(62→{len(dicts['site'].entries)}) · technique(95→{len(dicts['technique'].entries)}).")
    A("")
    A(md_table(["사전", "종류", "라벨", "정준값", "동의어", "후보", "출처 키"], [(d.name, getattr(d, "kind", "value"), d.label, len(d.entries), sum(len(e["synonyms"]) for e in d.entries.values()), len(d.candidates), ", ".join(sorted({f"`{s['file']}:{s['path']}`" for e in d.entries.values() for s in e["sources"]} | {f"`{s['file']}:{s['path']}`" for e in d.entries.values() for sy in e["synonyms"] for s in sy["sources"]})[:6]) + (" …" if len({(s['file'], s['path']) for e in d.entries.values() for s in e["sources"]}) > 6 else "")) for d in dicts.values()]))
    A("")
    A("사전 하나에 비고가 있는 것:")
    A("")
    for d in dicts.values():
        if d.note:
            A(f"- `{d.name}`: {d.note}")
    A("")
    A("## 5. 충돌·결정 개체 정의 + 규칙 ①~⑩ + 신뢰 순위")
    A("")
    A("충돌(`conflict`)·결정(`decision`) 개체 정의는 §2.18·§2.19. v1.1 의 재검토 처분 19 건은 결정 레코드 19 개로 `erd-v1.1.json → decisions` 에 미리 적재한다(사용자 판단 4 · 워커 처리 확정 15).")
    A("")
    A(md_table(["#", "분류", "규칙"], S.QUALITY_RULES))
    A("")
    A("빈값과 「없음」: 안 적힌 것(키 없음·null·빈 배열·빈 문자열) = null(미입력). 명시적으로 없다고 적힌 것만 빈 목록. step1 의 「확인 불가」·「근거 없음」·「해당 없음」은 값이다(null 아님). 단계 끝 = 컬럼 행선지 미정 0 · 충돌 미판정 0.")
    A("")
    A("### 5.1 원장 신뢰 순위 (파일별 · 21 + step1)")
    A("")
    A(md_table(["순위", "파일", "종류", "근거 키", "표시", "비고"], [(t, f"`{f}`", S.SOURCE_KIND[f], b, S.TRUST_FLAGS.get(f, ""), n) for f, t, b, n in sorted(S.SOURCE_FILES, key=lambda x: (x[1], x[0]))]))
    A("")
    s1 = next(fm for fm in erd["source_files"] if fm["file"] == STEP1)
    A(f"`products.json` 의 `products[].mfds` 필드만 2(식약처 허가)로 격상한다. `complications.json` 은 8-1 처분으로 3 유지 + 「AI 컨센서스 추정」. `step1-products.json` 은 조사 산출물: 허가 건 `licenses[].source` 가 `{S.STEP1_TIER2_SOURCE_RE}` 에 맞는 {s1['trust_tier_rule']['tier2_licenses']}/{s1['trust_tier_rule']['licenses_total']} 건의 허가·회사·공식명 필드만 2, 그 밖(emedi 검색·KPIC·판정·메모·search_names)은 3. 4등급 파일 안의 「교과서」표현은 AI 합의 라벨이지 실제 교과서가 아니다.")
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
    A(f"`step1-products.json` 전체 SHA256 `{s1['sha256']}` · {s1['bytes']} bytes · 항목 {s1['items']} · 잎 키 {s1['leaf_paths']}. 브론즈만 {sum(1 for r in colrows if r['file'] == STEP1 and r['dest'] == '브론즈')} 은 설계·식별자·작업 상태·집계·파생 복사본(§C 규칙).")
    A("")
    A("## 7. 질문 25 답")
    A("")
    A(md_table(["#", "답 (발주서 §6 기본값 적용 · v1.1 개정분은 7·8·10·11·14·16·24)"], S.Q25))
    A("")
    A("## 8. 기본값 재검토 — 처분 결과")
    A("")
    A("v1 §8 의 19 건을 발주서 §A 대로 처분했다. 사용자 판단 4(8-1·8-2·8-4·8-5), 나머지 15 는 v1 에서 한 처리를 확정. 각 건은 결정 레코드(`erd-v1.1.json → decisions`)로 남는다.")
    A("")
    A(md_table(["#", "항목", "처분 주체", "처분(확정)", "v1.1 반영 위치"], [(f"8-{no}", B.REVIEW[no - 1]["title"], who, what, where) for no, (who, what, where) in S.DISPOSITIONS.items()]))
    A("")
    A("### 8-2 표 — v1 부위 사전 「(확장)」 51 의 처분")
    A("")
    A(md_table(["값", "cc_group 횟수", "재배치", "사유"], [(r["value"], r["cc_group_n"], r["dest"], r["reason"]) for r in SITE_TABLE]))
    A("")
    kept = [r for r in SITE_TABLE if r["dest"].startswith("부위")]
    A(f"부위 사전 유지 {len(kept)} · problem_subcategory_label 로 {len(SITE_TABLE) - len(kept)}. 부위 사전 최종 = 뼈대 11 + taxonomy 부위 라벨 {len(kept)} = **{len(dicts['site'].entries)}** (확장 0). 복합 라벨의 멤버: " + " · ".join(f"{e['canonical']}→{'+'.join(e['members'])}" for e in dicts["site"].entries.values() if e.get("members")) + ".")
    A("")
    A("## 9. ERD 승인 때 사용자가 볼 것")
    A("")
    A("### 9.1 사전 표 (정준값 수 · 동의어 · 후보)")
    A("")
    A(md_table(["사전", "정준값", "동의어", "후보(미연결)"], [(d.name, len(d.entries), sum(len(e["synonyms"]) for e in d.entries.values()), "; ".join(c["value"] for c in d.candidates) or "—") for d in dicts.values()]))
    A("")
    A("핵심 사전 정준값 전체:")
    A("")
    for name in ["modality", "problem", "site", "technique", "license_status", "license_kind", "license_state"]:
        d = dicts[name]
        A(f"- `{name}` ({len(d.entries)}): " + " · ".join((e["canonical"] + (f"[{e['code']}]" if e.get("code") else "") + (f"({e['site_kind']})" if e.get("site_kind") == "taxonomy_site_label" else "")) for e in d.entries.values()))
    A(f"- `problem_subcategory_label` ({len(dicts['problem_subcategory_label'].entries)}): " + " · ".join(e["canonical"] + f"[{e['code']}]" + ("(부위)" if e.get("is_site") else "") for e in dicts["problem_subcategory_label"].entries.values()))
    A("")
    A("### 9.2 격리 목록 — 참조 해결, v1 vs v1.1 (자리별 · 같은 행 집합)")
    A("")
    A("v1 = 완전 일치만. v1.1 = §1.3 분해 규칙을 `erd-v1.1-resolve.py` 로 실제 돌린 수치. 「분해 성공·항목 없음」은 조각이 전부 사전에 닿았지만 taxonomy 항목 하나로 떨어지지 않은 참조(조합 보존). 미해결은 사전에 없는 조각이 하나라도 있는 참조이며 닿은 조각은 부분 결과로 `erd-v1.1-resolve.json` 에 있다. 사전 순서 때문에 M1 의 `(수입)`·`(국산)` 은 product_tier 가 아니라 M1 하위분류 라벨(수입/국산)에 먼저 닿아 combo 모양이 된다 — 규칙대로의 결과이며 순서를 바꾸려면 데이터(dictionary_order)만 바꾸면 된다. 고민 자리·pih id 자리는 v1 규칙 그대로(분해 규칙은 시술 참조 자리의 규칙).")
    A("")
    A(RESOLVE.side_by_side(RES, v1rep))
    A("")
    A(f"합계(부위 사전·step1 제외): 미해결 참조(⑨) v1 **{TOTAL.get('unresolved_v1')}** → v1.1 **{TOTAL['unresolved_v1_1']}** · 분해 성공·항목 없음 **{TOTAL['decomposed_v1_1']}** · 해결 **{TOTAL['resolved_v1_1']}**.")
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
    A(f"step1 395 → 원장 제품 대응(B 규칙만): 대응 {st['resolved']} (원장 제품 59 중 {st['ledger_products_covered']}종, 이름 역할 {st['matched_by']}) · 분해 성공·항목 없음 {st['decomposed']} ({', '.join(f'{k}={v}' for k, v in shp.items())}) · 미해결 {st['unresolved']} → **origin=survey {st['survey_products']}** (그중 step1 active=false {st['inactive_items']}). `non_product_depth:procedure` 는 이름이 제품 목록 59 가 아니라 taxonomy 단위 시술 항목(521)과 통째 일치한 것 — 제품 개체로는 survey 이고 R3(uses_product) 후보로 기록한다. 미해결 사유 상위 조각: " + " · ".join(f"`{f}`×{n}" for f, n in Counter(st["untouched_fragments"]).most_common(15)))
    A("")
    A("질문 14 두 묶음(modality_ref 빈 26 항목 · 8-5 처분 반영, 미배정 0):")
    A("")
    A(md_table(["고민", "하위분류", "항목", "묶음", "발주서 목록 일치", "범위"], [(r["problem"], r["subcategory"], r["name"], r["bucket"], ", ".join(r["matched"]) or "—", r["scope"]) for r in Q14]))
    A("")
    A("### 9.3 충돌 예상 수")
    A("")
    A(md_table(["종류", "무엇", "건"], [(c["kind"], c["what"], c["n"]) for c in CONF]))
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
    A("## 10. 검산 결과")
    A("")
    A("`erd-v1.1-check.py` 를 독립 실행한 출력을 그대로 붙였다(같은 폴더에서 `python3 erd-v1.1-check.py`). 검사 A 잎 키 행선지(원장 573 + step1) · B 사전 값 출처 · C ERD 출처 키·표적 · D 브론즈 sha256(21 + step1) · E 분해 규칙 재현(`erd-v1.1-resolve.py` 재실행 = `erd-v1.1.json` 수치) · F 처분 반영(부위 확장 0 · 기법 12 · 처분 19).")
    A("")
    return "\n".join(o)


def change_log(erd, dicts, RES, TOTAL, colrows, v1erd):
    o = []
    A = o.append
    v1d = {d["name"]: d for d in v1erd["dictionaries_summary"]} if v1erd else {}
    A("## 11. v1 → v1.1 변경 목록")
    A("")
    A("| 묶음 | 무엇 | v1 | v1.1 |")
    A("|---|---|---|---|")
    A(f"| A 8-1 | complications.json 신뢰 순위 | 3 + 표시 | 3 유지 + trust_flag 「AI 컨센서스 추정」 |")
    A(f"| A 8-2 | 부위 사전 | 62 (뼈대 11 + 확장 51) | {len(dicts['site'].entries)} (뼈대 11 + taxonomy 부위 라벨 {len(dicts['site'].entries) - 11}, 확장 0). 41 → problem_subcategory_label(신설 {len(dicts['problem_subcategory_label'].entries)}) · cc_group 행선지 dict:site → dict:problem_subcategory_label · R10/R11 규칙 |")
    A(f"| A 8-4 | 기법 사전 | 95 (하위분류 label 64 포함) | {len(dicts['technique'].entries)} (mechanism[] 만) · R5 출처 1 · energy_device type → product_type 만 · pih subcategory → R15.subcategory_label |")
    A(f"| A 8-5 | 질문 14 미배정 4 | 미배정 | ② 「피부과 허브 범위 밖」 격리(경구약 4) · 미배정 0 |")
    A(f"| A 나머지 15 | 재검토 → 처분 결과 | 「물을 것」 | 워커 처리 확정 · 결정 레코드 19 |")
    A(f"| B | 규칙 ⑨ 참조 해결 | 완전 일치만 | 결정론 분해 규칙(§1.3) 데이터화 · `erd-v1.1-resolve.py` · §9.2 v1 vs v1.1 (미해결 {TOTAL.get('unresolved_v1')} → {TOTAL['unresolved_v1_1']}, 분해 성공·항목 없음 {TOTAL['decomposed_v1_1']}) |")
    A(f"| B | 사전 | 36 | {len(dicts)} (+ 이름 색인 3: product_name·modality_subcategory_label·procedure_name) |")
    s1 = next(fm for fm in erd["source_files"] if fm["file"] == STEP1)
    st = RES["step1-products.items[] display/ledger/search 이름 → 원장 제품 (395)"]
    A(f"| C | 브론즈 원천 | 21 | 22 (`step1-products.json` research_artifact · sha256 `{s1['sha256'][:12]}` · 잎 {s1['leaf_paths']} · 허가 필드 조건부 2) |")
    A(f"| C | product 속성 | 22 | {len(next(e for e in S.ENTITIES if e['key']=='product')['attrs'])} (+origin·survey_ledger_id·survey_names·survey_family_code·license_status·license_kind·licenses·license_history·spec·companies·survey_note) |")
    A(f"| C | 사전 | — | license_status {len(dicts['license_status'].entries)} · license_kind {len(dicts['license_kind'].entries)} · license_state {len(dicts['license_state'].entries)} |")
    A(f"| C | step1 ↔ 원장 59 대응 | — | B 규칙만: 대응 {st['resolved']} · origin=survey {st['survey_products']} |")
    A(f"| C | 잎 키 행선지 | 573 | {len(colrows)} (573 + step1 {sum(1 for r in colrows if r['file']==STEP1)}) · 미정 0 |")
    A(f"| 공통 | 개체 / 관계 | 19 / 25 | 19 / 25 (속성·규칙만 변경) |")
    A(f"| 공통 | 열거형 | {len(v1erd['enums']) if v1erd else '—'} | {len(S.ERD_ENUMS)} (+product.origin·site.site_kind·source_file.kind·reference.status·reference.decomposed_shape) |")
    A("")
    A("v1 산출물(`erd-v1.*`·생성기 `erd_spec.py`·`erd_colmap.py`·`erd_build.py`)은 지우지 않았다. v1.1 생성기는 `erd_spec_v11.py`·`erd_colmap_v11.py`·`erd_build_v11.py`(v1 모듈을 읽어 변경분만 덧씌움).")
    return "\n".join(o)


def main():
    v1erd = json.load(open(os.path.join(WORK, "erd-v1.json"), encoding="utf-8"))
    step1_scan = scan_step1()
    colrows = build_column_map(step1_scan)
    dicts = build_dictionaries_v11()
    erd, RES, TOTAL, CONF, Q14, SITE_TABLE = write_outputs(colrows, dicts, step1_scan, v1erd)
    md = build_erd_md(erd, colrows, dicts, RES, TOTAL, CONF, Q14, SITE_TABLE, v1erd)
    chk = load_module("chk11", os.path.join(WORK, "erd-v1.1-check.py"))
    ok, report = chk.run_checks()
    md += report + "\n\n" + change_log(erd, dicts, RES, TOTAL, colrows, v1erd) + "\n"
    open(os.path.join(WORK, "erd-v1.1.md"), "w", encoding="utf-8").write(md)
    with open(os.path.join(WORK, "erd-v1.1-column-map.md"), "a", encoding="utf-8") as f:
        f.write("## 검산 결과\n\n" + report + "\n")
    print("OK" if ok else "FAIL")
    print(report)
    print("dests", Counter(r["dest"] for r in colrows), "step1", Counter(r["dest"] for r in colrows if r["file"] == STEP1))
    print("dicts", len(dicts), "site", len(dicts["site"].entries), "technique", len(dicts["technique"].entries))
    print("unresolved v1", TOTAL.get("unresolved_v1"), "v1.1", TOTAL["unresolved_v1_1"], "decomposed", TOTAL["decomposed_v1_1"], "resolved", TOTAL["resolved_v1_1"])


if __name__ == "__main__":
    main()
