# -*- coding: utf-8 -*-
"""ERD v3.3 산출물 생성기. v3.2 생성기(erd_build_v32.py)의 원장 적재·잎 키 스캔·도우미를 그대로 쓰고, 발주서 erd-v3.3-brief.md 의 사용자 결정 A~G 를 erd_spec_v33 · erd_colmap_v33 · erd-v3.3-tuples.py 로 덧씌운다.
입력: 원장 21 = 브론즈 3판(bronze/phub-ledger/ · HASHES.txt) · 2판(bronze/phub-ledger-v2/ · 대조) + step1-products.json + 스캔 JSON + erd-v3.2.json · erd-v3.2-dictionaries.json · erd-v3.2-tuples.json(나란히 비교 · 이관) · erd-v3.1-tuples.json
출력: erd-v3.3.md · erd-v3.3.json · erd-v3.3-column-map.md · erd-v3.3-dictionaries.json · erd-v3.3-tuples.json (+검산 결과 부착). 이전 판 파일은 지우지 않는다. 씨앗 후보 파일은 v3.2 것을 그대로 쓴다(승인된 21 은 결정 레코드).
"""
import copy
import hashlib
import json
import os
import sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_build_v31 as B31  # noqa  (원장 적재 · 스캔 · 도우미)
import erd_build_v32 as B32  # noqa  (mermaid)
import erd_spec_v33 as S  # noqa
import erd_colmap_v33 as C  # noqa

B = B31.B
WORK = HERE
STEP1 = B31.STEP1
SCAN = B31.SCAN
md_table, norm, mkid = B.md_table, B.norm, B.mkid
load_module = B31.load_module
TUP = load_module("erd_v33_tuples", os.path.join(WORK, "erd-v3.3-tuples.py"))
OUT = {"md": "erd-v3.3.md", "json": "erd-v3.3.json", "cmap": "erd-v3.3-column-map.md", "dict": "erd-v3.3-dictionaries.json", "tuples": "erd-v3.3-tuples.json", "check": "erd-v3.3-check.py"}
WRITTEN = S.WRITTEN
LEDGER, LEDGER_V2 = S.LEDGER_DIR, S.LEDGER_DIR_V2


def jload(name):
    return json.load(open(os.path.join(WORK, name), encoding="utf-8"))


def roundtrip(x):
    return json.loads(json.dumps(x, ensure_ascii=False, default=lambda o: list(o) if isinstance(o, (set, tuple)) else str(o)))


def sha16(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# 브론즈 3판 검증 · 2판 대조
# ---------------------------------------------------------------------------
def bronze_meta():
    hashes = {}
    for line in open(S.BRONZE_HASHES, encoding="utf-8"):
        h, f = line.split()
        hashes[f] = h
    rows, mism, changed = [], [], []
    for f in B31.FILES:
        full = hashlib.sha256(open(os.path.join(LEDGER, f), "rb").read()).hexdigest()
        v2 = hashlib.sha256(open(os.path.join(LEDGER_V2, f), "rb").read()).hexdigest() if os.path.exists(os.path.join(LEDGER_V2, f)) else None
        ok = full.startswith(hashes.get(f, "∅"))
        if not ok:
            mism.append(f)
        if v2 and v2 != full:
            changed.append(f)
        rows.append({"file": f, "sha256": full, "hashes_txt": hashes.get(f), "match": ok, "v2_sha256": v2, "changed_from_v2": bool(v2 and v2 != full)})
    changelog = open(S.BRONZE_CHANGELOG, encoding="utf-8").read()
    return {"version": S.BRONZE_VERSION, "date": S.BRONZE_DATE, "dir": "bronze/phub-ledger", "previous_dir": "bronze/phub-ledger-v2", "hashes_file": "bronze/phub-ledger/HASHES.txt", "files": rows, "mismatch": mism, "changed_from_v2": changed,
            "changelog_has_row_3": any(line.startswith("| 3 |") for line in changelog.splitlines()), "changelog": changelog}


# ---------------------------------------------------------------------------
# 잎 키 행선지
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


def write_column_map(colrows, step1_scan, rescan, bronze):
    moves33 = [{"file": f, "path": p, "v3_2": a, "v3_3": b} for f, p, a, b in C.MOVES_V33]
    notes33 = [{"file": f, "path": p, "target": t, "note": n} for f, p, t, n in C.NOTE_CHANGES_V33]
    dest_counter = Counter(r["dest"] for r in colrows)
    md = ["# ERD v3.3 — 잎 키 행선지 표 (원장 21 · 브론즈 3판 + step1-products.json)", "",
          f"**v3.2 와 행선지·표적이 다른 행은 {len(moves33)} 개다** — v3.3 은 소개정(A~G)이라 이동 0. 비고만 바뀐 행 {len(notes33)}(G 3판 synergy·taxonomy · C 사건 사전 R2·부위 3·승인 씨앗 · E category 삭제 · B 분석기 · F 설계안 참고). 그 밖 행선지·표적·비고는 v3.2 와 같다(검산 A). 규칙 `erd_colmap_v33.py`.", "",
          f"브론즈 3판 잎 키 재스캔: 원장 21 잎 키 {rescan['leaf_count_v2']} = 1판 스캔 {rescan['leaf_count_v1']} · 파일별 집합 차이 {len(rescan['diff'])}(3판은 synergy 값·taxonomy 항목 2 가 바뀌었고 키 모양은 그대로). 3판에서 2판과 바이트가 다른 파일 {len(bronze['changed_from_v2'])}: {', '.join(bronze['changed_from_v2'])}.", "",
          f"작성 {WRITTEN} · 원장 잎 키 {sum(1 for r in colrows if r['file'] != STEP1)} + step1 {step1_scan['leaf_count']} = {len(colrows)} · 행선지 범주 5: 개체 / 사전 / 엣지 / 브론즈 / 버림 · **미정 0**", "",
          "## 이동 표 (v3.2 → v3.3)", "", (md_table(["#", "파일", "경로", "v3.2", "v3.3"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['v3_2']}`", f"`{m['v3_3']}`") for i, m in enumerate(moves33)]) if moves33 else "(없음 — 이동 0)"), "",
          "## 비고 변경 (v3.2 → v3.3 · 표적 동일)", "", md_table(["#", "파일", "경로", "표적", "추가된 비고"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['target']}`", m["note"]) for i, m in enumerate(notes33)]), "",
          f"## 미래 칸 — 원장 칸 없음 (V3.3-A 제품 구성품 · 1,072 행에 들지 않는다 · 값 0)", "",
          "구성품(팁·카트리지·핸드피스·트랜스듀서)은 원장 21 어느 칸에도 값으로 없다(§9.18: 주의·설명 문장 안에만 · 시술 라벨 자리 0). 아래는 그 칸이 생길 때의 행선지를 미리 적은 것이다 — 지금은 행이 아니다.", "",
          md_table(["#", "미래 칸(원장에 없음)", "행선지", "표적", "비고"], [(i + 1, f"`{a}`", b, f"`{c}`", d) for i, (a, b, c, d) in enumerate(C.FUTURE_COLUMNS_V33)]), "",
          "## 요약", "", md_table(["행선지", "원장 21", "step1", "합계"], [(k, sum(1 for r in colrows if r["dest"] == k and r["file"] != STEP1), sum(1 for r in colrows if r["dest"] == k and r["file"] == STEP1), v) for k, v in sorted(dest_counter.items(), key=lambda x: -x[1])] + [("합계", sum(1 for r in colrows if r["file"] != STEP1), sum(1 for r in colrows if r["file"] == STEP1), len(colrows))]), ""]
    for f in B31.FILES + [STEP1]:
        rs = [r for r in colrows if r["file"] == f]
        md.append(f"## `{f}` — 잎 키 {len(rs)}")
        md.append("")
        md.append(md_table(["#", "경로", "타입", "횟수", "행선지", "표적", "비고"], [(i + 1, f"`{r['path']}`", r["type"], r["count"], r["dest"], f"`{r['target']}`", r["note"]) for i, r in enumerate(rs)]))
        md.append("")
    open(os.path.join(WORK, OUT["cmap"]), "w", encoding="utf-8").write("\n".join(md))
    return moves33, notes33


# ---------------------------------------------------------------------------
# 사전 — v3.2 ERD 값 + (C) 폐색·부위 3 + (E) category 삭제 + provenance + 파생 항목(원장 사건 노드 · 장비 제품 · category 없음) + 문구 사전
# ---------------------------------------------------------------------------
def finalize_dictionaries(dj, R, changes):
    D = {d["name"]: d for d in dj["dictionaries"]}
    prov = R["v33"]["provenance"]["by_id"]
    # 새 부위 3 — sources 를 실측 locator 에서 채운다(파일·경로 · kind=value · 부분 문자열 자리)
    for e in D["site"]["entries"]:
        if e.get("added_in") == "v3.3(V3.3-C(2))" and not e["sources"]:
            srows = next((s for s in R["v33"]["r2_dictionary"]["sites_added"] if s["value"] == e["canonical"]), None)
            if srows:
                for pth, n in srows["substring_paths"].items():
                    f, p = pth.split(":", 1)
                    e["sources"].append({"file": f, "path": p, "n": n, "kind": "value(부분 문자열 · 실측)"})
                e["token_locators"] = srows["token_locators"]
    for d in dj["dictionaries"]:
        for e in d["entries"]:
            if e["id"] in prov:
                e["provenance"] = prov[e["id"]]
    ev = D["adverse_event_type"]
    dup = {}
    for x in R["adverse"]["duplicate_pairs"]:
        dup.setdefault(x["new_id"], []).append({"existing": x["existing"], "rules": x["rules"], "stable_key": x["stable_key"]})
    for n in R["adverse"]["ledger_events"]:
        srcs = Counter()
        for loc in n["locators"]:
            f, rest = loc.split(":", 1)
            srcs[(f, rest.split("@", 1)[0])] += 1
        ev["entries"].append(OrderedDict([("id", n["id"]), ("canonical", n["canonical"]), ("sources", [{"file": f, "path": p, "n": c, "kind": "ledger_core"} for (f, p), c in srcs.items()]), ("synonyms", []), ("definition", None),
                                          ("origin", "ledger"), ("status", "unreviewed"), ("locators", n["locators"]), ("contexts", n["contexts"][:8]), ("core_tokens", n.get("core_tokens", [])), ("duplicate_candidates", dup.get(n["id"], [])),
                                          ("provenance", {"status": "ledger", "match": "core", "n": len(n["locators"]), "locators": n["locators"][:12]})]))
    pn = D["product_name"]
    for p in R["equipment"]["products"]:
        p = dict(p)
        p["provenance"] = {"status": "ledger", "match": "value", "n": len(p["sources"]), "locators": [s["locator"] for s in p["sources"] if s.get("locator")][:12]}
        pn["entries"].append(p)
    A = R["adverse"]
    entries = []
    for e in A["phrase_dictionary"] + A["memo_phrases"]:
        entries.append(OrderedDict([("id", e["id"]), ("canonical", e["normalized"]), ("normalized", e["normalized"]), ("status", e["status"]), ("raw_variants", e["raw_variants"]), ("locators", e["locators"]), ("synonyms", []), ("sources", []), ("definition", None),
                                    ("units", e.get("units", [])), ("ledger_events", e.get("ledger_events", [])), ("candidates", e.get("candidates", [])), ("parsed", e.get("parsed")), ("why", e.get("why"))]))
    dj["dictionaries"].append({"name": "phrase_dictionary", "label": "부작용 문구 사전", "kind": "phrase_index", "closed": None, "note": "v3.3: v3.2(V3.2-0 · V3.2-7) 그대로 — 부작용 문구 종류(safety.*)만 · status exact|new|approved|note|sentence · unlinked 없음 · 「혈관 폐색」 원문은 raw_variants 로 보존(V3.3-C) · 원장 3판",
                               "canonical_count": len(entries), "entries": entries, "candidates": [], "removed_synonyms": [], "removed_entries": [], "by_status": dict(Counter(e["status"] for e in entries)), "occurrences": sum(len(e["locators"]) for e in entries)})
    dj["erd_version"] = S.ERD_VERSION
    dj["bronze_version"] = S.BRONZE_VERSION
    dj["closed_rule"] = S.OPEN_CLOSED_RULE
    dj["v33_base_changes"] = changes
    dj["values_changed_from_v3_2"] = {"erd_values": "v3.2 49 사전의 ERD 값·동의어·순서 그대로 — 바뀐 자리는 둘뿐: adverse_event_type 「혈관 폐색」→「폐색」(V3.3-C(1) · R2 를 사전 값에도 · 옛 id alias · 분해 꼴) · site +3(동맥·정맥·안동맥 · V3.3-C(2) · 사용자 승인)",
                                      "removed_fields": ["adverse_event_type.entries[].category(V3.3-E · 원장 출처 0)", "adverse_event_type.entries[].category_review"], "added_fields": ["*.entries[].provenance(원장 locator 실측 · status ledger|ledger(key)|erd_default|missing)", "site.entries[].parent_id", "adverse_event_type 「폐색」.decomposed_from · aliases"],
                                      "derived_entries": {"adverse_event_type(origin=ledger)": len(R["adverse"]["ledger_events"]), "product_name(origin=taxonomy)": len(R["equipment"]["products"])}, "phrase_dictionary": "v3.3 재생성(3판 · 부작용 문구만)",
                                      "unsourced_values": len(R["v33"]["provenance"]["unsourced"]), "approved_seeds_not_in_dictionary": {"site": len(S.SEED_APPROVED_V33["site"]), "ingredient_material": len(S.SEED_APPROVED_V33["ingredient_material"])}}
    dj["note"] = "v3.3: 사전 49(이름 그대로) · ERD 값 변경 2 자리(C) · category 삭제(E) · 값마다 provenance · 원장이 종류를 선언한 열린 사전(사건 · 장비 제품)에 파생 항목(unreviewed) · 분해는 파생 항목을 빼고 돈다(erd-v3.3-tuples.py base_dictionary33) · 승인 씨앗 21 은 결정 레코드(8차)라 여기 없음"
    return dj


# ---------------------------------------------------------------------------
# erd-v3.3.json
# ---------------------------------------------------------------------------
def build_json(v32, colrows, moves33, notes33, dj, R, bronze, rescan=None):
    erd = copy.deepcopy(v32)
    # 원장 3판 — source_files 의 해시·바이트·판 번호(1판 대조 필드는 그대로 두고 2판 대조를 더한다)
    rows3 = {r["file"]: r for r in bronze["files"]}
    for sf in erd["source_files"]:
        r = rows3.get(sf["file"])
        if r is None:
            continue
        path = os.path.join(LEDGER, sf["file"])
        sf.update({"sha256": r["sha256"], "hashes_txt": r["hashes_txt"], "bronze_version": 3, "bytes": os.path.getsize(path), "v2_sha256": r["v2_sha256"], "changed_from_v2": r["changed_from_v2"], "path_dir": "bronze/phub-ledger"})
        try:
            top = json.load(open(path, encoding="utf-8"))
            for k in ("version", "updated"):
                if isinstance(top, dict) and k in top:
                    sf[k] = top[k]
        except Exception:  # noqa
            pass
    erd["bronze_version"] = 3
    if rescan is not None:
        erd["bronze_leaf_rescan"] = rescan
    ent_json = [{"key": e["key"], "prefix": e["prefix"], "label": e["label"], "definition": e["definition"], "identity": e["identity"], "beyond_minimum": e.get("beyond_minimum", False), "aliases": e["aliases"],
                 "attrs": [{"name": a[0], "type": a[1], "required": a[2], "sources": a[3], "rule": a[4]} for a in e["attrs"]]} for e in S.ENTITIES]
    rel_json = [{**r, "attrs": [{"name": a[0], "type": a[1], "note": a[2]} for a in r["attrs"]]} for r in S.RELATIONS]
    X = R["v33"]
    decisions = list(v32["decisions"]) + [OrderedDict([("id", "DEC-2026-11-06-29"), ("kind", "scope_review"),
                                                       ("target", {"erd_ref": "§1.3 tokenize(B) · §1.4 component(A) · §1.5 R2 사전 값·접미사 표기 꼴·category 삭제(C·D·E) · §2 product·site·adverse_effect · R27 · R30 · R31 · R36 · §4 사전(폐색 · 부위 3 · provenance) · §5 dictionary_add·event_split·fold_approve·canonical_rename 비고 · §9 실측 3판(G) · §9.24 설계안(F · 적용 0)",
                                                                   "review_item": "erd-v3.3-brief.md A~G (사용자 결정 2026-11-06)"}),
                                                       ("new_value", {"disposition": " · ".join(f"{a} {b}" for a, b, c, d in S.CHANGE_LIST_V33)}),
                                                       ("reason", "사용자 결정 2026-11-06(구성품 · 형태소 분석기 · R2 사전 값·부위 3·폐색≠색전 · 접미사 표기 꼴 · category 삭제 · 세분 묶음 설계안 · 원장 3판). ERD 승인 때 approved · 사전 값 변경 2 자리(폐색 · 부위 3)는 이 레코드가 근거"),
                                                       ("decided_by", None), ("decided_at", None), ("status", "proposed"), ("source_refs", [{"kind": "brief", "ref": "erd-v3.3-brief.md"}, {"kind": "review", "ref": "HANDOFF-2026-11-05.md 「11-06 추가」 · silver-v3/out-dryrun3/report.md §8 · bronze/phub-ledger/CHANGELOG.md 3"}])])]
    upd = OrderedDict([
        ("erd_version", S.ERD_VERSION), ("previous_version", S.PREVIOUS_VERSION), ("status", "draft — 사용자 승인 전"), ("written", WRITTEN), ("bronze", {k: v for k, v in bronze.items() if k != "changelog"}),
        ("user_definitions_v33_note", S.USER_DEFINITIONS_V33_NOTE), ("user_definitions_v32_note", v32["user_definitions_v32_note"]),
        ("tokenize_rule", S.TOKENIZE_RULE_V33), ("tokenize_rule_v32_assist", S.V32.TOKENIZE_RULE), ("analyzer_rule", S.ANALYZER_RULE),
        ("component_rule", S.COMPONENT_RULE), ("future_columns_v3_3", [{"column": a, "dest": b, "target": c, "note": d} for a, b, c, d in S.FUTURE_COLUMNS_V33]),
        ("r2_dictionary_rule", S.R2_DICT_RULE), ("occlusion_embolism_rule", S.OCCLUSION_EMBOLISM_RULE), ("suffix_variant_rule", S.SUFFIX_VARIANT_RULE), ("category_delete_rule", S.CATEGORY_DELETE_RULE), ("f_bundle_rule", S.F_BUNDLE_RULE), ("ledger3_rule", S.LEDGER3_RULE), ("g_kind_assessment", S.G_KIND_ASSESSMENT),
        ("normalize_rule", S.NORMALIZE_RULE), ("id_rule", S.ID_RULE),
        ("resolve_rules", roundtrip(S.RESOLVE_RULES)), ("tuple_rules", roundtrip(S.TUPLE_RULES)), ("closed_dictionaries", S.CLOSED_DICTIONARIES),
        ("entities", ent_json), ("relations", roundtrip(rel_json)), ("enums", S.ERD_ENUMS), ("proc_axis_edges", S.PROC_AXIS_EDGES),
        ("decision_kinds", [{"kind": k, "build_reads": br, "target": t, "new_value": nv, "note": n, "new_in_v3_1": k in S.DECISION_KINDS_NEW_V31, "note_changed_in_v3_2": S.DECISION_KINDS_NOTE_V32.get(k), "note_changed_in_v3_3": S.DECISION_KINDS_NOTE_V33.get(k)} for k, br, t, nv, n in S.DECISION_KINDS]),
        ("decisions", decisions),
        ("column_map_summary", {"leaf_paths": len(colrows), "by_dest": dict(Counter(r["dest"] for r in colrows)), "by_entity": dict(Counter(r["target"].split(".")[0] for r in colrows if r["dest"] == "개체")), "by_relation": dict(Counter(r["target"].split(".")[0].split("(")[0] for r in colrows if r["dest"] == "엣지"))}),
        ("column_map_moves_v3_3", moves33), ("column_map_note_changes_v3_3", notes33),
        ("dictionaries_summary", [{"name": d["name"], "label": d["label"], "kind": d.get("kind", "value"), "closed": d.get("closed"), "canonical": len(d["entries"]), "erd_values": sum(1 for e in d["entries"] if e.get("origin") not in ("ledger", "taxonomy")) if d["name"] != "phrase_dictionary" else 0, "derived": sum(1 for e in d["entries"] if e.get("origin") in ("ledger", "taxonomy")), "synonyms": sum(len(e.get("synonyms", [])) for e in d["entries"])} for d in dj["dictionaries"]]),
        ("tuple_report", {"procedure": R["procedure"]["summary"], "adverse": R["adverse"]["summary"], "condition": R["condition"]["summary"]}),
        ("tuple_report_v3_2", v32.get("tuple_report")),
        ("v3_3_measure", {"deltas": X["deltas"], "before_v32_ledger2": R["v32"]["before"], "baseline_v32_ledger3": R["v32"]["baseline_v32_ledger3"], "after": R["v32"]["after"], "projection_approved_seeds": R["v32"]["projection"],
                          "component": {k: v for k, v in X["component"].items() if k != "rows"}, "kiwi": X["kiwi"], "r2_dictionary": {k: v for k, v in X["r2_dictionary"].items() if k != "old_value_phrases"}, "seeds_approved": X["seeds_approved"], "suffix": X["suffix"],
                          "category": X["category"], "f_bundle": {k: v for k, v in X["f_bundle"].items() if k not in ("depth_rows", "thread_rows")}, "ledger3": {k: v for k, v in (X["ledger3"] or {}).items() if k not in ("changed_examples", "synergy_slot_rows_v3", "kind_assessment")},
                          "provenance_summary": X["provenance"]["summary"], "unsourced_values": X["provenance"]["unsourced"], "ledger_events": len(R["adverse"]["ledger_events"]), "duplicate_pairs": len(R["adverse"]["duplicate_pairs"]), "equipment_products": len(R["equipment"]["products"]), "r33": R["r33"]}),
        ("user_decisions_needed", [{"item": a, "where": b, "options": c, "decision": d} for a, b, c, d in S.USER_DECISIONS_NEEDED]),
        ("category_touched_v3_3", [{"artifact": a, "where": b, "v32_count": c, "disposition": d} for a, b, c, d in S.CATEGORY_TOUCHED_V33]),
        ("change_list_v3_3", [{"no": a, "what": b, "where": c, "item": d} for a, b, c, d in S.CHANGE_LIST_V33]),
    ])
    erd.update(upd)
    for k in ("user_definitions_v31", "explicit_exception_v31", "user_definitions", "principles", "principles_v31", "rule_zero", "phrase_kind_table", "node_rule", "open_closed_rule"):
        erd[k] = v32[k]
    erd["phrase_dictionary_summary"] = {"entries": len(R["adverse"]["phrase_dictionary"]) + len(R["adverse"]["memo_phrases"]), "by_status": dict(Counter(e["status"] for e in R["adverse"]["phrase_dictionary"] + R["adverse"]["memo_phrases"]))}
    for k in ("column_map_moves_v3_2", "column_map_note_changes_v3_2", "v3_2_measure", "change_list_v3_2"):
        erd.setdefault(k, v32.get(k))
    return erd


def mermaid():
    s = B32.mermaid()
    return s + ("\n    PRODUCT }o--|| PRODUCT : \"R36 component_of (kind=component · 값 0)\"\n    PROCEDURE }o--o| PRODUCT : \"R27 what (component · 값 0)\"\n"
                "    %% v3.3: product.kind product|component · R36 component_of(원장 칸 없음 · 값 0) · 토큰화 = 형태소 분석기(kiwipiepy 0.24) · 사건 사전 값에도 R2(혈관 폐색 → 폐색 + 혈관) · 부위 동맥·정맥·안동맥 · 접미사 ~감·~증·~형성 = 표기 꼴 · adverse_event_type.category 삭제 · 원장 = 브론즈 3판")


# ---------------------------------------------------------------------------
# erd-v3.3.md
# ---------------------------------------------------------------------------
def build_md(erd, colrows, dj, R, v32, moves33, notes33, bronze, changes):
    o = []
    A = o.append
    X = R["v33"]
    A("# ERD v3.3 — 피부과 시술 허브 메달리온 시맨틱 정의")
    A("")
    A(f"작성 {WRITTEN} · 상태 **초안(사용자 승인 전)** · 원장 = 브론즈 **3판** `bronze/phub-ledger/`(HASHES.txt 21 일치 · CHANGELOG 3 · 2판 `bronze/phub-ledger-v2/` 보존) + step1 · 발주서 `erd-v3.3-brief.md`(사용자 결정 2026-11-06 「erd 다 정해서 빌드 해보고」 · 변경 A~G). 동결 v3.2(`ERD-FROZEN.md` v3.2 절)를 바탕으로 한 **소개정** — 사용자 정의 1·2·3 · 명시 예외 · 원칙 A~D 글자 그대로 · 바뀌는 것은 A~G 뿐.")
    A("")
    A(f"기계용 동본 `erd-v3.3.json` · 값 사전 `erd-v3.3-dictionaries.json`(49 · 값 변경 2 자리 · category 삭제 · provenance) · 행선지 `erd-v3.3-column-map.md`(이동 {len(moves33)} · 비고 {len(notes33)} · 미래 칸 {len(S.FUTURE_COLUMNS_V33)}) · 실측 `erd-v3.3-tuples.py`(→ `erd-v3.3-tuples.json` · §9 · 3판) · 검산 `erd-v3.3-check.py`(§10). 생성기 `erd_spec_v33.py`·`erd_colmap_v33.py`·`erd_build_v33.py`. 이전 판 산출물은 그대로 두었다. **v3.2 → v3.3 변경 목록은 §11**, 「사용자 결정 필요」 §12, 「출처 없는 값」 §13, 관찰 §14.")
    A("")
    A(f"**개체 {len(S.ENTITIES)}(그대로) · 관계 {len(S.RELATIONS)}(34 + R36 component_of) · 사전 {len(dj['dictionaries'])} · 결정 kind {len(S.DECISION_KINDS)}(그대로 · 새 kind 0 — §5 G 검토) · 행선지 {len(colrows)}(이동 0 · 미래 칸 {len(S.FUTURE_COLUMNS_V33)})**.")
    A("")
    A("## 0. 사용자 정의 · 첫 규칙 · 원칙 (v3.2 글자 그대로)")
    A("")
    A("동결 원문(ERD-FROZEN · 글자 그대로):")
    A("")
    for n, t in S.USER_DEFINITIONS:
        A(f"{n}. {t}")
    A("")
    A("v3.1 문장(정의 2 개정판 · v3.3 도 이것을 쓴다):")
    A("")
    for x in erd["user_definitions_v31"]:
        A(f"{x['no']}. {x['text']}")
    A("")
    A(f"**명시 예외(v3.1 개정판 · 유지)**: {erd['explicit_exception_v31']}")
    A("")
    A(f"**v3.3 과 정의의 관계**: {S.USER_DEFINITIONS_V33_NOTE}")
    A("")
    A("### 0.1 첫 규칙 — 문구 종류 분류 먼저 (V3.2-0 · 그대로)")
    A("")
    A(S.RULE_ZERO)
    A("")
    A(md_table(["문구 종류", "원장 자리", "자기 테이블", "부작용과의 관계"], S.PHRASE_KIND_TABLE))
    A("")
    A("### 0.2 부작용 축 노드 원칙 (V3.2-0 · 그대로 · v3.3: 토큰화는 §1.3 분석기 · 사전 값에도 R2 는 §1.5)")
    A("")
    A(S.NODE_RULE)
    A("")
    A(S.OPEN_CLOSED_RULE)
    A("")
    A("**원칙(A~D · v3.2 글자 그대로)**: " + " ".join(f"**{k}.** {v}" for k, v in S.PRINCIPLES))
    A("")
    A("## 1. 규칙")
    A("")
    A("층(브론즈 · 시맨틱 · 실버 · 골드)은 v3.2 §1 그대로. v3.3: 원장은 3판(G) · 토큰화는 형태소 분석기(B · 실버 lib 몫) · 사건 사전 값에도 R2(C). 지식은 원장 21(3판·2판)·컬럼 스캔·erd-v3.2 산출물·발주서·HANDOFF-2026-11-05(「11-06 추가」)·ERD-FROZEN·`ERD-V3-CANDIDATES.md`·`silver-v3/out-dryrun{,2,3}/report.md`·`bronze/phub-ledger/CHANGELOG.md` 에서만 가져왔다(silver-v3/lib 는 열지 않았다).")
    A("")
    A("### 1.1 정규화 norm_v2 · norm_v3(d) · 식별자")
    A("")
    A(f"- norm_v1(v3.1 그대로): " + " → ".join(S.NORMALIZE_RULE["steps"]))
    A(f"- norm_v2(V3.2-2 그대로): " + " · ".join(S.V32.NORM_V2["steps"]) + f" — {S.V32.NORM_V2['note']}")
    A(f"- **norm_v3(V3.3-D)**: " + " · ".join(S.NORMALIZE_RULE["v3_3"]["steps"][-1:]) + f" — {S.NORMALIZE_RULE['v3_3']['note']}")
    for k in ("adverse_effect", "ledger_event", "equipment_product", "product_component", "post_procedure_timeline", "emergency_sign", "phrase", "product"):
        A(f"- 식별자 `{k}`: {S.ID_RULE[k]}")
    A(f"- 결정 target · 접힘 조건 · locator 규칙은 v3.2 §1.1 그대로(`erd-v3.3.json → id_rule`).")
    A("")
    A("### 1.2 다이어그램")
    A("")
    A("```mermaid")
    A(mermaid())
    A("```")
    A("")
    A("### 1.3 토큰화 = 형태소 분석기 (V3.3-B · v3.2 목록은 보조)")
    A("")
    A(S.TOKENIZE_RULE_V33)
    A("")
    tk = S.RESOLVE_RULES["tokenize"]
    A(f"- 분석기: {tk['analyzer']['name']} {tk['analyzer']['version_pinned']}(판 고정 · `{tk['analyzer']['interpreter']}`) · 핵심어 품사 {tk['analyzer']['core_pos']} · 핵심어 불가 {tk['analyzer']['not_core_pos']} · 절 판정 「{tk['analyzer']['clause']}」 · 수식어 아님 {tk['analyzer']['not_modifier']} · 서술 표지 {tk['analyzer']['predicate_markers']} · 등록할 사전 표면형 {X['kiwi']['user_words']}(실측 §9.19).")
    A(f"- 순서: " + " → ".join(tk["order"]) + f" · 보존 {tk['preserved_as']}.")
    A(f"- **분석기 보조 목록(analyzer_assist · v3.2 V3.2-1 목록 그대로 · 규칙 아님)** — 조사 {len(tk['particles'])}: " + " · ".join(tk["particles"]))
    A(f"  - 용언 어미 {len(tk['verb_endings'])}: " + " · ".join(tk["verb_endings"]) + f" · 문법 낱말 {len(tk['grammar_words'])}: " + " · ".join(tk["grammar_words"]) + f" · relaxed 접미 {len(tk['relaxed_suffixes'])} · predicate 어미 {len(tk['predicate_endings'])} — 원소마다 locator(§9.11).")
    A("- 참조 분해 3단계 · stopwords · 회사 괄호 · 조합 기호 · 회·차 · 겹침은 v3.1 §1.3 그대로(`resolve_rules`). v3.2 토큰화 문장은 `erd-v3.3.json → tokenize_rule_v32_assist`.")
    A("")
    A("### 1.4 시술 튜플 — what 규칙 v3.3 (V3.3-A 구성품 · V3.2-5 장비 · V3.2-6 성분 · V3.3-F 설계안)")
    A("")
    A(S.COMPONENT_RULE)
    A("")
    A(S.EQUIP_RULE)
    A("")
    A(S.INGREDIENT_RULE)
    A("")
    A(S.F_BUNDLE_RULE)
    A("")
    A("그 밖 §1.4(접힘 · site · technique · 엣지 끝)는 v3.2 그대로.")
    A("")
    A("### 1.5 부작용 단위·문구 (V3.3-C R2 사전 값 · V3.3-D 접미사 · V3.3-E category 삭제 · V3.2 그대로)")
    A("")
    A("- 단위 = (사건, 부위, 물질) 세 칸 · 경과는 R15 · 상대 부위 none · 수식어 목록(V3.1-8) — v3.2 그대로. **노드 원칙**: §0.2 그대로.")
    A(f"- {S.R2_DICT_RULE}")
    A(f"- {S.OCCLUSION_EMBOLISM_RULE}")
    A(f"- {S.SUFFIX_VARIANT_RULE}")
    A(f"- {S.CATEGORY_DELETE_RULE}")
    A(f"- **문구 종류 판정(V3.2-7 그대로)**: {S.PHRASE_KIND_RULE}")
    pk = S.TUPLE_RULES["phrase_kinds"]
    A(f"  - 메모 어휘 {len(pk['note_words'])} · 설명문 문턱(멤버 토큰 ≥{pk['sentence_min_tokens']} · 문법 ≥{pk['sentence_min_grammar']} · 라틴 비율 ≥{pk['sentence_latin_ratio']}) · 대체 핵심어 {pk['fallback_core']} · 핵심어 제외 {pk['core_exclude']} — 전부 **분석기 보조 목록**(V3.3-B) · ⑦ 규칙 {pk['dup_rules']} · 표기 꼴 접미 {pk['spelling_variant_suffixes']} · 대표 이름(현상) {pk['canonical_phenomenon_names']}.")
    A(f"- **R15 속성 상속(V3.2-8 그대로)**: {S.INHERIT_RULE}")
    A("")
    A("### 1.6 사람 조건 — v3.2 그대로 + 토큰화는 분석기(V3.3-B)")
    A("")
    A("조건 사전·완전 일치·raw_name 단위·문장 부록은 v3.1 §1.6 그대로. v3.3: 조사·어미를 떼는 것은 분석기 품사(J*·E*)로 — 목록은 보조. 실측 §9.7 · §9.10.")
    A("")
    A("### 1.7 사전 씨앗 규칙 (V3.2-3 · V3.2-4 그대로 · V3.3-C 승인 씨앗은 결정 레코드)")
    A("")
    A(S.SEED_RULE)
    A("")
    A(S.TUPLE_RULES["site_closed"]["rule"])
    A("")
    A(f"**승인 씨앗(V3.3-C(4))** — {S.SEED_APPROVED_NOTE}. 부위 15: " + " · ".join(f"{v}({k} · parent {p or '—'})" for v, k, p in S.SEED_APPROVED_V33["site"]) + " · 성분 6: " + " · ".join(v for v, _, _ in S.SEED_APPROVED_V33["ingredient_material"]) + ". locator 는 §9.21. 이 값들은 **erd-v3.3-dictionaries.json 에 없다**(8차 dictionary_add 뒤 사전 값이 된다).")
    A("")
    A("사전 닫힘: " + " · ".join(f"{k} {'닫힘' if v else '열림'}" for k, v in S.CLOSED_DICTIONARIES.items()) + " · 그 밖 사전은 씨앗 규칙 대상 아님(closed=null).")
    A("")
    A("### 1.8 자기 테이블 — 타임라인 · 응급 징후 · 고지 · 문헌 (V3.2-9 · V3.2-0 그대로)")
    A("")
    for t in (S.TIMELINE_RULE, S.SIGN_RULE, S.DISCLOSURE_RULE_V32, S.LITERATURE_RULE):
        A(f"- {t}")
    A("")
    A("### 1.9 원장 3판 (V3.3-G)")
    A("")
    A(S.LEDGER3_RULE)
    A("")
    A("## 2. 개체 목록")
    A("")
    A(f"개체 {len(S.ENTITIES)}(v3.2 그대로). v3.3 에서 바뀐 것: product(kind product|component · component_of · component_kind — 값 0) · procedure(what_kind component) · site(동맥·정맥·안동맥 · parent 값) · adverse_effect(정의 비고 — R2 사전 값 · 폐색 ≠ 색전). 새 개체 0(F 설계안 F-3 의 procedure_spec 은 적용하지 않았다).")
    A("")
    for i, e in enumerate(S.ENTITIES):
        A(f"### 2.{i + 1} `{e['key']}` — {e['label']} (접두 `{e['prefix']}`)")
        A("")
        A(f"- 정의: {e['definition']}")
        A(f"- 식별자: {e['identity']}")
        A(f"- aliases: {e['aliases']}")
        A("")
        A(md_table(["속성", "타입", "필수", "출처 원장 키", "규칙"], [(a[0], a[1], "○" if a[2] else "", "<br>".join(f"`{s}`" for s in a[3]) if a[3] else "(파생/ERD 정의)", a[4]) for a in e["attrs"]]))
        A("")
    A("## 3. 관계 목록")
    A("")
    A(f"관계 {len(S.RELATIONS)}. v3.3: **R36 component_of**(product(kind=component) → product · 값 0) 신설 · R27 끝에 product(kind=component) · R30 비고(후보 제안) · R31 비고(부위 3). 엣지 끝 규칙: " + S.EDGE_END_RULE)
    A("")
    for r in S.RELATIONS:
        A(f"### {r['id']} `{r['name']}` — {r['from']} → {r['to']} ({r['card']})")
        A("")
        if r["attrs"]:
            A(md_table(["엣지 속성", "타입", "비고"], [(a[0], a[1], a[2]) for a in r["attrs"]]))
            A("")
        A("- 출처: " + (", ".join(f"`{s}`" for s in r["sources"]) if r["sources"] else "(ERD 정의)"))
        if r.get("note"):
            A(f"- 규칙: {r['note']}")
        A("")
    A("### 3.1 ERD 정의 열거형")
    A("")
    A(md_table(["열거형", "값"], [(k, ", ".join(map(str, v))) for k, v in S.ERD_ENUMS.items()]))
    A("")
    A("## 4. 값 사전")
    A("")
    pv = X["provenance"]
    A(f"`erd-v3.3-dictionaries.json` — {len(dj['dictionaries'])} 사전. ERD 값·동의어·순서는 v3.2 와 같고 바뀐 자리는 둘: adverse_event_type **「혈관 폐색」→「폐색」**(V3.3-C(1) · 옛 id `{changes['event_decomposed'][0]['old_id']}` alias · decomposed_from) · site **+3**(동맥 · 정맥 · 안동맥 · V3.3-C(2)). 뺀 것: `category`·`category_review`(V3.3-E · {X['category']['v32'].get('erd-v3.2-dictionaries.json:category')} 자리). 더한 것: 값마다 `provenance`(원장 locator 실측 · §9.26) · 열린 사전의 파생 항목(adverse_event_type origin=ledger {len(R['adverse']['ledger_events'])} · product_name origin=taxonomy {len(R['equipment']['products'])} — status=unreviewed · category 없음) · 문구 사전 v3.3(3판).")
    A("")
    A(md_table(["사전", "종류", "closed", "ERD 값", "파생 항목", "동의어", "출처 ledger", "ledger(key)", "미선언(v3.3 추가)", "erd_default", "missing"],
               [(d["name"], d.get("kind", "value"), d.get("closed"), sum(1 for e in d["entries"] if e.get("origin") not in ("ledger", "taxonomy")) if d["name"] != "phrase_dictionary" else "—", sum(1 for e in d["entries"] if e.get("origin") in ("ledger", "taxonomy")) if d["name"] != "phrase_dictionary" else len(d["entries"]), sum(len(e.get("synonyms", [])) for e in d["entries"]),
                 pv["summary"]["by_dictionary"].get(d["name"], {}).get("ledger", 0), pv["summary"]["by_dictionary"].get(d["name"], {}).get("ledger(key)", 0), pv["summary"]["by_dictionary"].get(d["name"], {}).get("ledger(경로 미선언 · v3.3 추가 값)", 0), pv["summary"]["by_dictionary"].get(d["name"], {}).get("erd_default", 0), pv["summary"]["by_dictionary"].get(d["name"], {}).get("missing", 0)) for d in dj["dictionaries"]]))
    A("")
    A(f"**출처 없는 값 {len(pv['unsourced'])}**(§13 전수 · 삭제하지 않았다 — 사용자). 승인 씨앗 21(§1.7 · §9.21)은 이 파일에 없다.")
    A("")
    A("## 5. 결정")
    A("")
    A(f"결정 kind {len(S.DECISION_KINDS)}(v3.2 그대로 · **새 kind 0** · 비고만 바뀐 kind: " + " · ".join(f"`{k}`({v})" for k, v in S.DECISION_KINDS_NOTE_V33.items()) + "). 적용 순서 ⓪①~⑦ · target 안정 키 · 빌드는 approved 만 — v3.1 §5 그대로.")
    A("")
    A(md_table(["kind", "빌드 적용", "target", "new_value", "비고"], [(f"`{k}`", "○" if br else "기록만", t, nv, n[:300]) for k, br, t, nv, n in S.DECISION_KINDS]))
    A("")
    A(S.G_KIND_ASSESSMENT)
    A("")
    A(f"결정 레코드: v3.2 의 {len(v32['decisions'])} 이관(모양·값 그대로) + DEC-2026-11-06-29(v3.3 개정 · scope_review · proposed). 승인 씨앗 21(dictionary_add) · 접미사 쌍 20(fold_approve) · R30 후보(edge_create)는 **레코드로 만들지 않았다** — 8차 결정 묶음의 자리(§9.21 · §9.22 · §9.20).")
    A("")
    A("## 6~8. 원장 파일 매핑 · 질문 25 · 처분")
    A("")
    A(f"v3.1 §6~§8 그대로. 브론즈 3판: 2판과 바이트가 다른 파일 {len(bronze['changed_from_v2'])}({', '.join(bronze['changed_from_v2'])}) · HASHES.txt 21 일치 · CHANGELOG 3판 행 {'있음' if bronze['changelog_has_row_3'] else '없음'}. 잎 키 행선지 변경은 `erd-v3.3-column-map.md`(이동 0 · 비고 {len(notes33)} · 미래 칸 {len(S.FUTURE_COLUMNS_V33)}).")
    A("")
    A("## 9. 실측 (`erd-v3.3-tuples.py` 실제 실행 · 원장 3판 · 숫자는 목표가 아니다)")
    A("")
    A("### 9.5 시술 튜플 (v3.3 · 3판 · v3.2 2판 열과 나란히)")
    A("")
    A(TUP.V31.procedure_md(R, v32["tuple_report"]["procedure"]))
    A("")
    A(TUP.V31.condition_md(R))
    A("")
    A("### 9.9~9.17 v3.2 실측(3판 재생성) · 9.18~9.27 v3.3 실측")
    A("")
    A(TUP.full_md(R))
    A("")
    A("## 10. 검산 결과")
    A("")
    A("`erd-v3.3-check.py` 를 독립 실행한 출력을 그대로 붙였다.")
    A("")
    return "\n".join(o)


def change_log(R, v32, colrows, moves33, notes33, dj, changes):
    X = R["v33"]
    s = R["adverse"]["summary"]
    b, g, a = R["v32"]["before"], R["v32"]["baseline_v32_ledger3"], R["v32"]["after"]
    o = []
    A = o.append
    A("## 11. v3.2 → v3.3 변경 목록")
    A("")
    c = X["component"]
    k = X["kiwi"]
    r2 = X["r2_dictionary"]
    sf = X["suffix"]
    ce = X["category"]
    fb = X["f_bundle"]
    g3 = X["ledger3"] or {}
    meas = {
        "V3.3-A": f"구성품 값 0 · 원장 자리 {c['occurrences']}(라벨 자리 {len(c['label_slot_hits'])}) · 미래 칸 {len(S.FUTURE_COLUMNS_V33)} · R36 엣지 0 · what_kind=component 0",
        "V3.3-B": f"kiwipiepy {k['version']}(고정 {k['pinned']} · 일치 {k['pinned_ok']}) · 등록할 사전 표면형 {k['user_words']} · 보조 목록 {len(R['v32']['tokenizer_words'])} 원소 locator 보존",
        "V3.3-C": f"폐색 단위 {r2['event_units'][0]['n_units']}((폐색, 혈관) 있음 {bool(r2['event_units'][0]['unit_event_site'])}) · 옛 표면형 남음 {len(r2['old_surface_in_dictionary'])} · 붙은 꼴 노드 {len(r2['attached_form_nodes'])} · 부위 3(토큰 자리 {'/'.join(str(x['n_token']) for x in r2['sites_added'])} · 부분 문자열 {'/'.join(str(x['n_substring']) for x in r2['sites_added'])}) · 폐색↔색전 공유 동의어 {len(r2['occlusion_embolism']['shared_synonyms'])} · R30 후보 {len(r2['r30_candidates'])}(엣지 0) · 승인 씨앗 21(사전 값 아님)",
        "V3.3-D": f"쌍 20(이 실측 ⑦ strong 로 서는 쌍 {sf['dup_suffix_pairs_in_20']}) · 3쌍 사용자 · ⑦ suffix 쌍 {sf['dup_suffix_pairs_total']} · 사전에 더한 동의어 0",
        "V3.3-E": f"v3.2 category 자리 {ce['v32'].get('erd-v3.2-dictionaries.json:category')}+{ce['v32'].get('erd-v3.2-dictionaries.json:category_review')}+{ce['v32'].get('erd-v3.2-tuples.json:event_category')}+{ce['v32'].get('erd-v3.2.json:decision_kinds.new_value 「category」')} → v3.3 0 · 7 라벨 원장 잎 값 자리 {_sum7(ce)}",
        "V3.3-F": f"깊이·세기 라벨 자리 {fb['depth_label_slots']}(⑨ {fb['depth_slot_results'].get('unresolved', 0)}) · 뗀 뒤 충돌 묶음 {fb['collision_groups']} · 실 재질/형태 자리 {fb['thread_label_slots']} · 성분 what {fb['ingredient_what']} · 설계안 3 · 적용 0",
        "V3.3-G": f"분류 항목 {g3.get('catalog_items_v2')} → {g3.get('catalog_items')} · synergy 바뀐 자리 {g3.get('synergy_changed_slots')} · synergy 자리 ⑨ {g3.get('synergy_slot_result_v2', {}).get('unresolved')} → {g3.get('synergy_slot_result_v3', {}).get('unresolved')} · 남은 「Mxx-」 {g3.get('synergy_prefixed_distinct_v3')}종 {g3.get('synergy_prefixed_slots_v3')}자리 · 새 kind 0",
    }
    chk = {"V3.3-A": "VA1~VA5", "V3.3-B": "VB1~VB3", "V3.3-C": "VC1~VC6 · B7~B9", "V3.3-D": "VD1~VD4", "V3.3-E": "VE1~VE3 · B5", "V3.3-F": "VF1~VF2", "V3.3-G": "VG1~VG5 · D1~D3 · R1~R4"}
    A(md_table(["#", "무엇", "어디서 반영", "검산", "실측(v3.3 · 3판)"], [(no, what, where, chk[no], meas.get(no, "")) for no, what, where, item in S.CHANGE_LIST_V33]))
    A("")
    A(f"- 개체 22 → {len(S.ENTITIES)} · 관계 34 → {len(S.RELATIONS)}(+R36) · 사전 49 → {len(dj['dictionaries'])}(이름 그대로 · 값 변경 2 자리) · 결정 kind 20 → {len(S.DECISION_KINDS)} · 행선지 이동 {len(moves33)} · 비고 {len(notes33)} · 결정 레코드 {len(v32['decisions'])} → {len(v32['decisions']) + 1}.")
    A(f"- 실측 요약 델타(§9.27): " + " · ".join(f"{d['key']} {d['v32_ledger2']} → {d['v32_ledger3']}(G) → {d['v33_ledger3']}(C·E)" for d in X["deltas"] if d["delta_total"]) + ".")
    A("")
    A("## 12. 사용자 결정 필요 — A~G 안에서 애매한 것(빈 자리 · 추측으로 메우지 않았다)")
    A("")
    A(md_table(["#", "항목", "어디서 나왔나", "선택지", "결정"], [(i + 1, a, b, c, d or "(비어 있음)") for i, (a, b, c, d) in enumerate(S.USER_DECISIONS_NEEDED)]))
    A("")
    A("## 13. 출처 없는 값 — v3.2 사전 값 중 원장 locator 가 없는 것 전수(삭제는 사용자)")
    A("")
    pv = X["provenance"]
    A(f"ERD 사전 값 {pv['summary']['total']} 전수 대조(§9.26) — 상태별 {' · '.join(f'{k} {v}' for k, v in pv['summary']['by_status'].items())}.")
    A("")
    A(md_table(["#", "사전", "id", "값", "동의어", "선언한 출처", "상태", "왜"], [(i + 1, u["dictionary"], u["id"], u["canonical"], ", ".join(u["synonyms"]) or "—", ", ".join(f"`{x}`" for x in u["declared"]) or "—", u["status"], u["why"]) for i, u in enumerate(pv["unsourced"])]) if pv["unsourced"] else "(없음)")
    A("")
    A("## 14. v3.3 밖 관찰 — 결정·다음 판 후보 (레코드는 만들지 않았다)")
    A("")
    obs = [
        ("8차 결정 묶음", f"승인 씨앗 21(dictionary_add · §9.21) · 접미사 쌍 20(fold_approve · 자극감은 canonical_rename 함께 · §9.22) · R30 후보 {len(r2['r30_candidates'])}(edge_create · 사용자) · ⑦ strong {s['dup_pairs_strong']} 닫기", "dictionary_add · fold_approve · canonical_rename · edge_create · conflict_close"),
        ("붙은 꼴 「혈관폐색」", f"이 실측(목록 규칙)에서는 새 노드(자리 {r2['attached_form_nodes'][0]['n_locators'] if r2['attached_form_nodes'] else 0}) — 분석기(8차)가 (폐색, 혈관)으로 가른다(dryrun3 N3). 8차 뒤 이 노드가 남으면 fold_approve", "실버 빌더 · fold_approve"),
        ("「Vascular Occlusion」", "사용자 결정대로 폐색의 동의어 — complications 이름 「혈관폐색/색전 (Vascular Occlusion/Embolism)」의 영문 쪽이 (폐색, none) 단위 1 을 세운다(부위 말이 영문 안에 있어 R2 가 닿지 않음 · §9.20). 두면 단위 (폐색, none)·(폐색, 혈관) 둘 — 사용자 판단", "adverse_tuple_assign · phrase_map"),
        ("원장 4판 후보", f"synergy 「Mxx-」 접두 {g3.get('synergy_prefixed_distinct_v3')}종 {g3.get('synergy_prefixed_slots_v3')}자리 · 「CO2 프랙셔널 레이저」류 3곳 · 「ASCE+엑소좀」(HANDOFF) — 사용자 답 대기", "원장(브론즈) · ERD 아님"),
        ("ledger(key) 값", f"frequency_class·reaction_level·unit·condition_level 의 {pv['summary']['by_status'].get('ledger(key)', 0)} 값은 원장 **키 이름**이 값이다(출처 종류 key) — 값 자체는 원장 잎에 없다. 출처는 있으나 「값 출처」의 뜻이 다르므로 §4 표에 따로 센다", "scope_review"),
        ("F 묶음", "설계안 3 중 하나를 고르면 그때 ERD 개정(개체·식별자 변경이라 결정 레코드로는 못 한다) · 깊이·세기 4 값(심부·딥·얕은·약한)은 그때까지 ⑨", "ERD 다음 판"),
        ("v3.2 동결 승계", "v3.2 §12 의 열린 항목(원장 사건 노드 접기 · 핵심어 품질 · raw_name 옛 결정 · 정상 줄 · 조건 축 노드 원칙 · 씨앗 잡음)은 그대로", "v3.2 §12"),
    ]
    A(md_table(["어디", "무엇", "decision kind / 자리"], obs))
    return "\n".join(o)


def _sum7(ce):
    lab = (ce.get("ledger_occurrences_of_7_labels") or {}).get("exact_value_occurrences") or {}
    return " · ".join(f"{k} {v}" for k, v in lab.items())


def main():
    v32 = jload("erd-v3.2.json")
    v32tup = jload("erd-v3.2-tuples.json")
    v31tup = jload("erd-v3.1-tuples.json")
    dic32 = jload("erd-v3.2-dictionaries.json")
    bronze = bronze_meta()
    assert not bronze["mismatch"], f"브론즈 3판 HASHES.txt 불일치: {bronze['mismatch']}"
    rescan = B31.B3.rescan_v2()
    step1_scan = B31.B11.scan_step1()
    colrows = build_column_map(step1_scan)
    moves33, notes33 = write_column_map(colrows, step1_scan, rescan, bronze)
    base, changes = TUP.prepare_base_v33(dic32)
    rules, rrules = roundtrip(S.TUPLE_RULES), roundtrip(S.RESOLVE_RULES)
    rules["adverse"]["adverse_stopwords"] = v32["tuple_rules"]["adverse"]["adverse_stopwords"]
    rules["condition"] = v32["tuple_rules"]["condition"]
    for p_ in ("erd-v3.3.json", "erd-v3.3-dictionaries.json"):
        if os.path.exists(os.path.join(WORK, p_)):
            os.remove(os.path.join(WORK, p_))
    L3 = {f: json.load(open(os.path.join(LEDGER, f), encoding="utf-8")) for f in os.listdir(LEDGER) if f.endswith(".json")}
    L2 = {f: json.load(open(os.path.join(LEDGER_V2, f), encoding="utf-8")) for f in os.listdir(LEDGER_V2) if f.endswith(".json")}
    step1 = json.load(open(os.path.join(WORK, STEP1), encoding="utf-8"))
    R = TUP.run_everything33(base, rules, L3, rrules, v31tup, v32tup, dic32=dic32, L2=L2, changes=changes, step1=step1)
    dj = finalize_dictionaries(base, R, changes)
    json.dump(dj, open(os.path.join(WORK, OUT["dict"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    json.dump(TUP.slim(R), open(os.path.join(WORK, OUT["tuples"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    erd = build_json(v32, colrows, moves33, notes33, dj, R, bronze, rescan)
    erd["tuple_rules"] = rules
    erd["resolve_rules"] = rrules
    json.dump(erd, open(os.path.join(WORK, OUT["json"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = build_md(erd, colrows, dj, R, v32, moves33, notes33, bronze, changes)
    cl = change_log(R, v32, colrows, moves33, notes33, dj, changes)
    open(os.path.join(WORK, OUT["md"]), "w", encoding="utf-8").write(md + "(검산 실행 중)\n\n" + cl + "\n")
    chk = load_module("chk33", os.path.join(WORK, OUT["check"]))
    ok, report = chk.run_checks()
    open(os.path.join(WORK, OUT["md"]), "w", encoding="utf-8").write(md + report + "\n\n" + cl + "\n")
    with open(os.path.join(WORK, OUT["cmap"]), "a", encoding="utf-8") as f:
        f.write("## 검산 결과\n\n" + report + "\n")
    print("OK" if ok else "FAIL")
    print(report)


if __name__ == "__main__":
    main()
