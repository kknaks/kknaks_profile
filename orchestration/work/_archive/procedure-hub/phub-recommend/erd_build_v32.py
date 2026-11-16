# -*- coding: utf-8 -*-
"""ERD v3.2 산출물 생성기. v3.1 생성기(erd_build_v31.py)의 원장 적재·잎 키 스캔·도우미를 그대로 쓰고, 발주서 erd-v3.2-brief.md 6건 + 코디·사용자 추가(V3.2-0 · 7 · 8 · 9)를 erd_spec_v32 · erd_colmap_v32 · erd-v3.2-tuples.py 로 덧씌운다.
입력: 원장 21 = 브론즈 2판(HASHES.txt) + step1-products.json + 스캔 JSON + erd-v3.1.json · erd-v3.1-dictionaries.json · erd-v3.1-tuples.json(나란히 비교 · 이관)
출력: erd-v3.2.md · erd-v3.2.json · erd-v3.2-column-map.md · erd-v3.2-dictionaries.json · erd-v3.2-tuples.json · erd-v3.2-seed-candidates.json/.md (+검산 결과 부착). 이전 판 파일은 지우지 않는다.
"""
import copy
import json
import os
import sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_build_v31 as B31  # noqa  (원장 2판 적재 · 스캔 · 도우미)
import erd_spec_v32 as S  # noqa
import erd_colmap_v32 as C  # noqa

B = B31.B
WORK = HERE
STEP1 = B31.STEP1
SCAN = B31.SCAN
L = B31.L
md_table, norm, mkid = B.md_table, B.norm, B.mkid
load_module = B31.load_module
TUP = load_module("erd_v32_tuples", os.path.join(WORK, "erd-v3.2-tuples.py"))
OUT = {"md": "erd-v3.2.md", "json": "erd-v3.2.json", "cmap": "erd-v3.2-column-map.md", "dict": "erd-v3.2-dictionaries.json", "tuples": "erd-v3.2-tuples.json", "check": "erd-v3.2-check.py"}
WRITTEN = "2026-11-05"
# 검토 S-1 전(검토 대상 판 · erd-v3.2-review.md 가 센 수치)
REVIEW_BEFORE = {"nodes_before": 335, "absorbed_before": 68, "exact_before": 1331, "new_before": 915, "units_before": 395, "dup_before": 157}


def jload(name):
    return json.load(open(os.path.join(WORK, name), encoding="utf-8"))


def roundtrip(x):
    return json.loads(json.dumps(x, ensure_ascii=False, default=lambda o: list(o) if isinstance(o, (set, tuple)) else str(o)))


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


def write_column_map(colrows, step1_scan, rescan):
    moves32 = [{"file": f, "path": p, "v3_1": a, "v3_2": b} for f, p, a, b in C.MOVES_V32]
    notes32 = [{"file": f, "path": p, "target": t, "note": n} for f, p, t, n in C.NOTE_CHANGES_V32]
    dest_counter = Counter(r["dest"] for r in colrows)
    md = ["# ERD v3.2 — 잎 키 행선지 표 (원장 21 · 브론즈 2판 + step1-products.json)", "",
          f"**v3.1 과 행선지·표적이 다른 행은 {len(moves32)} 개다** — V3.2-9 타임라인 9 행(→ post_procedure_timeline · R33) + V3.2-0 응급 징후 1(→ emergency_sign) + 문헌 adverse_effects 8(→ evidence_statement · kind=adverse_effects). 비고만 바뀐 행 {len(notes32)}. 그 밖 행선지·표적·비고는 v3.1 과 같다(검산 A). 규칙 `erd_colmap_v32.py`.", "",
          f"브론즈 2판 잎 키 재스캔: 원장 21 잎 키 {rescan['leaf_count_v2']} = 1판 {rescan['leaf_count_v1']} · 파일별 집합 차이 {len(rescan['diff'])}.", "",
          f"작성 {WRITTEN} · 원장 잎 키 {sum(1 for r in colrows if r['file'] != STEP1)} + step1 {step1_scan['leaf_count']} = {len(colrows)} · 행선지 범주 5: 개체 / 사전 / 엣지 / 브론즈 / 버림 · **미정 0**", "",
          "## 이동 표 (v3.1 → v3.2)", "", md_table(["#", "파일", "경로", "v3.1", "v3.2"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['v3_1']}`", f"`{m['v3_2']}`") for i, m in enumerate(moves32)]), "",
          "## 비고 변경 (v3.1 → v3.2 · 표적 동일)", "", md_table(["#", "파일", "경로", "표적", "추가된 비고"], [(i + 1, f"`{m['file']}`", f"`{m['path']}`", f"`{m['target']}`", m["note"]) for i, m in enumerate(notes32)]), "",
          f"## 비고 정리 (검토 S-3 · 표적 그대로) — 옛 구조 문장(표현 개체 · R29 · raw_name · unlinked)을 지운 행 {len(C.SCRUBBED_V32)}", "", md_table(["#", "파일", "경로", "표적"], [(i + 1, f"`{f}`", f"`{p}`", f"`{t}`") for i, (f, p, t) in enumerate(C.SCRUBBED_V32)]), "",
          "## 요약", "", md_table(["행선지", "원장 21", "step1", "합계"], [(k, sum(1 for r in colrows if r["dest"] == k and r["file"] != STEP1), sum(1 for r in colrows if r["dest"] == k and r["file"] == STEP1), v) for k, v in sorted(dest_counter.items(), key=lambda x: -x[1])] + [("합계", sum(1 for r in colrows if r["file"] != STEP1), sum(1 for r in colrows if r["file"] == STEP1), len(colrows))]), ""]
    for f in B31.FILES + [STEP1]:
        rs = [r for r in colrows if r["file"] == f]
        md.append(f"## `{f}` — 잎 키 {len(rs)}")
        md.append("")
        md.append(md_table(["#", "경로", "타입", "횟수", "행선지", "표적", "비고"], [(i + 1, f"`{r['path']}`", r["type"], r["count"], r["dest"], f"`{r['target']}`", r["note"]) for i, r in enumerate(rs)]))
        md.append("")
    open(os.path.join(WORK, OUT["cmap"]), "w", encoding="utf-8").write("\n".join(md))
    return moves32, notes32


# ---------------------------------------------------------------------------
# 사전 — v3.1 값 그대로 + closed · site.parent 필드 + 파생 항목(원장 사건 노드 · 장비 제품) + 문구 사전 v3.2
# ---------------------------------------------------------------------------
def base_dictionaries():
    dj = jload("erd-v3.1-dictionaries.json")
    dj = copy.deepcopy(dj)
    dj["dictionaries"] = [d for d in dj["dictionaries"] if d["name"] != "phrase_dictionary"]
    for d in dj["dictionaries"]:
        d["closed"] = S.CLOSED_DICTIONARIES.get(d["name"])
        if d["name"] == "site":
            for e in d["entries"]:
                e.setdefault("parent", None)
    return dj


def finalize_dictionaries(dj, R):
    D = {d["name"]: d for d in dj["dictionaries"]}
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
                                          ("category", None), ("origin", "ledger"), ("status", "unreviewed"), ("locators", n["locators"]), ("contexts", n["contexts"][:8]), ("core_tokens", n.get("core_tokens", [])), ("duplicate_candidates", dup.get(n["id"], []))]))
    pn = D["product_name"]
    for p in R["equipment"]["products"]:
        pn["entries"].append(p)
    A = R["adverse"]
    entries = []
    for e in A["phrase_dictionary"] + A["memo_phrases"]:
        entries.append(OrderedDict([("id", e["id"]), ("canonical", e["normalized"]), ("normalized", e["normalized"]), ("status", e["status"]), ("raw_variants", e["raw_variants"]), ("locators", e["locators"]), ("synonyms", []), ("sources", []), ("definition", None),
                                    ("units", e.get("units", [])), ("ledger_events", e.get("ledger_events", [])), ("candidates", e.get("candidates", [])), ("parsed", e.get("parsed")), ("why", e.get("why"))]))
    dj["dictionaries"].append({"name": "phrase_dictionary", "label": "부작용 문구 사전", "kind": "phrase_index", "closed": None, "note": "v3.2(V3.2-0 · V3.2-7): 부작용 문구 종류(safety.*)만 · status exact|new|approved|note|sentence · unlinked 없음 · 분해가 쓰는 사전(캐시)",
                               "canonical_count": len(entries), "entries": entries, "candidates": [], "removed_synonyms": [], "removed_entries": [], "by_status": dict(Counter(e["status"] for e in entries)), "occurrences": sum(len(e["locators"]) for e in entries)})
    dj["erd_version"] = S.ERD_VERSION
    dj["closed_rule"] = S.OPEN_CLOSED_RULE
    dj["values_changed_from_v3_1"] = {"erd_values": "v3.1 49 사전의 ERD 값·동의어·순서 불변(검산 O-2)", "added_fields": ["*.closed", "site.entries[].parent(null)", "파생 항목 origin/status"],
                                      "derived_entries": {"adverse_event_type(origin=ledger)": len(R["adverse"]["ledger_events"]), "product_name(origin=taxonomy)": len(R["equipment"]["products"])}, "phrase_dictionary": "v3.2 재작성(부작용 문구만)"}
    dj["note"] = "v3.2: 사전 49(이름 그대로) · ERD 값 불변 · 원장이 종류를 선언한 열린 사전(사건 · 장비 제품)에 파생 항목(unreviewed) · 분해는 파생 항목을 빼고 돈다(erd-v3.2-tuples.py base_dictionary)"
    return dj


# ---------------------------------------------------------------------------
# erd-v3.2.json
# ---------------------------------------------------------------------------
def build_json(v31, colrows, moves32, notes32, dj, R, report=None):
    erd = copy.deepcopy(v31)
    ent_json = [{"key": e["key"], "prefix": e["prefix"], "label": e["label"], "definition": e["definition"], "identity": e["identity"], "beyond_minimum": e.get("beyond_minimum", False), "aliases": e["aliases"],
                 "attrs": [{"name": a[0], "type": a[1], "required": a[2], "sources": a[3], "rule": a[4]} for a in e["attrs"]]} for e in S.ENTITIES]
    rel_json = [{**r, "attrs": [{"name": a[0], "type": a[1], "note": a[2]} for a in r["attrs"]]} for r in S.RELATIONS]
    v32 = R["v32"]
    decisions = list(v31["decisions"]) + [OrderedDict([("id", "DEC-2026-11-05-28"), ("kind", "scope_review"),
                                                       ("target", {"erd_ref": "§0 첫 규칙 · 원칙 A·D · §1.1 norm_v2 · §1.3 tokenize · §1.4 성분 what · 장비 · §1.5 노드 원칙·문구 종류 · §1.7 씨앗 · §1.8 테이블 · §2 adverse_effect·clinical_rule·evidence_statement·product·procedure·site·post_procedure_timeline·emergency_sign · R15 · R33 · R34 · R35 · §4 closed", "review_item": "erd-v3.2-brief.md V3.2-1 ~ V3.2-6 + 코디·사용자 추가 V3.2-0 · V3.2-7 · V3.2-8 · V3.2-9 (2026-11-05)"}),
                                                       ("new_value", {"disposition": " · ".join(f"{a} {b}" for a, b, c in S.CHANGE_LIST_V32)}),
                                                       ("reason", "6차 실측(미연결 1,032 · ⑨ 260 · 미등록 2,352) — 사용자 승인 2026-11-05 「v3.2 진행」 + 사용자 결정(분류 먼저 · 사전에 없으면 새 노드 · 타임라인 테이블 · R15 상속 · 메모 분리). ERD 승인 때 approved"),
                                                       ("decided_by", None), ("decided_at", None), ("status", "proposed"), ("source_refs", [{"kind": "brief", "ref": "erd-v3.2-brief.md"}, {"kind": "review", "ref": "silver-v3/out/report.md §14 · out/gate/batch4"}])])]
    upd = OrderedDict([
        ("erd_version", S.ERD_VERSION), ("previous_version", S.PREVIOUS_VERSION), ("status", "draft — 사용자 승인 전"), ("written", WRITTEN),
        ("user_definitions_v32_note", S.USER_DEFINITIONS_V32_NOTE), ("rule_zero", S.RULE_ZERO), ("phrase_kind_table", [{"kind": a, "ledger": b, "table": c, "relation": d} for a, b, c, d in S.PHRASE_KIND_TABLE]),
        ("node_rule", S.NODE_RULE), ("open_closed_rule", S.OPEN_CLOSED_RULE), ("principles", [{"key": k, "text": v} for k, v in S.PRINCIPLES]), ("principles_v31", v31["principles"]),
        ("normalize_rule", S.NORMALIZE_RULE), ("id_rule", S.ID_RULE), ("tokenize_rule", S.TOKENIZE_RULE), ("phrase_kind_rule", S.PHRASE_KIND_RULE), ("inherit_rule", S.INHERIT_RULE), ("timeline_rule", S.TIMELINE_RULE), ("sign_rule", S.SIGN_RULE),
        ("disclosure_rule", S.DISCLOSURE_RULE_V32), ("literature_rule", S.LITERATURE_RULE), ("seed_rule", S.SEED_RULE), ("site_dict_rule", S.SITE_DICT_RULE), ("equip_rule", S.EQUIP_RULE), ("ingredient_rule", S.INGREDIENT_RULE),
        ("raw_name_rule", "v3.2(V3.2-0): 없음 — " + S.NODE_RULE), ("expression_rule", S.RULE_ZERO),
        ("resolve_rules", roundtrip(S.RESOLVE_RULES)), ("tuple_rules", roundtrip(S.TUPLE_RULES)), ("closed_dictionaries", S.CLOSED_DICTIONARIES),
        ("entities", ent_json), ("relations", roundtrip(rel_json)), ("enums", S.ERD_ENUMS), ("proc_axis_edges", S.PROC_AXIS_EDGES),
        ("decision_kinds", [{"kind": k, "build_reads": br, "target": t, "new_value": nv, "note": n, "new_in_v3_1": k in S.DECISION_KINDS_NEW_V31, "note_changed_in_v3_2": S.DECISION_KINDS_NOTE_V32.get(k)} for k, br, t, nv, n in S.DECISION_KINDS]),
        ("decisions", decisions),
        ("column_map_summary", {"leaf_paths": len(colrows), "by_dest": dict(Counter(r["dest"] for r in colrows)), "by_entity": dict(Counter(r["target"].split(".")[0] for r in colrows if r["dest"] == "개체")), "by_relation": dict(Counter(r["target"].split(".")[0].split("(")[0] for r in colrows if r["dest"] == "엣지"))}),
        ("column_map_moves_v3_2", moves32), ("column_map_note_changes_v3_2", notes32),
        ("dictionaries_summary", [{"name": d["name"], "label": d["label"], "kind": d.get("kind", "value"), "closed": d.get("closed"), "canonical": len(d["entries"]), "erd_values": sum(1 for e in d["entries"] if e.get("origin") not in ("ledger", "taxonomy")) if d["name"] != "phrase_dictionary" else 0, "derived": sum(1 for e in d["entries"] if e.get("origin") in ("ledger", "taxonomy")), "synonyms": sum(len(e.get("synonyms", [])) for e in d["entries"])} for d in dj["dictionaries"]]),
        ("tuple_report", {"procedure": R["procedure"]["summary"], "adverse": R["adverse"]["summary"], "condition": R["condition"]["summary"]}),
        ("tuple_report_v3_1", v31.get("tuple_report")),
        ("v3_2_measure", {"before": v32["before"], "after": v32["after"], "projection": v32["projection"], "regression_v31": v32["regression_v31"], "disappeared_by_tokenizer": v32["disappeared_by_tokenizer"],
                          "variant_pairs": len(v32["variant_pairs"]), "seeds": {k: {"rows": len(v["rows"]), "proposed": sum(1 for r in v["rows"] if r.get("status") == "proposed")} for k, v in v32["seeds"].items()},
                          "ledger_events": len(R["adverse"]["ledger_events"]), "duplicate_pairs": len(R["adverse"]["duplicate_pairs"]), "equipment_products": len(R["equipment"]["products"]), "r33": R["r33"]}),
        ("change_list_v3_2", [{"no": a, "what": b, "where": c} for a, b, c in S.CHANGE_LIST_V32]),
    ])
    for k in ("user_definitions_v31", "explicit_exception_v31"):
        upd[k] = v31[k]
    erd.update(upd)
    for k in ("phrase_dictionary_rule", "phrase_shape_rule"):
        erd[k] = v31[k] + " — v3.2: " + S.PHRASE_KIND_RULE
    erd["phrase_dictionary_summary"] = {"entries": len(R["adverse"]["phrase_dictionary"]) + len(R["adverse"]["memo_phrases"]), "by_status": dict(Counter(e["status"] for e in R["adverse"]["phrase_dictionary"] + R["adverse"]["memo_phrases"]))}
    return erd


def mermaid():
    s = B31.mermaid()
    return s + ("\n    POST_PROCEDURE_TIMELINE }o--o{ ADVERSE_EFFECT : \"R34 timeline_refers\"\n    PROCEDURE }o--o| POST_PROCEDURE_TIMELINE : \"R33 has_timeline\"\n    EMERGENCY_SIGN }o--o{ ADVERSE_EFFECT : \"R35 sign_refers\"\n"
                "    %% v3.2: 부작용 단위에는 부작용 문구(이름 · safety.*)만 — 사건이 사전에 없으면 원장 사건 노드(⑦) · 타임라인·응급 징후·고지·문헌은 참조만 · R15 속성 상속(item → family → unit · basis)")


# ---------------------------------------------------------------------------
# erd-v3.2.md
# ---------------------------------------------------------------------------
def build_md(erd, colrows, dj, R, v31, moves32, notes32):
    o = []
    A = o.append
    Dn = {d["name"]: d for d in dj["dictionaries"]}
    ad = R["adverse"]["summary"]
    v32 = R["v32"]
    A("# ERD v3.2 — 피부과 시술 허브 메달리온 시맨틱 정의")
    A("")
    A(f"작성 {WRITTEN} · 상태 **초안(사용자 승인 전)** · 원장 = 브론즈 2판 `bronze/phub-ledger/`(HASHES.txt 21 일치) + step1 · 발주서 `erd-v3.2-brief.md`(사용자 승인 2026-11-05 「v3.2 진행」 · 변경 6건) + 코디·사용자 추가(2026-11-05): **V3.2-0** 문구 종류 분류 먼저(§0 첫 규칙) · 부작용 축 노드 원칙 교체(사전에 없으면 새 노드 + ⑦) · **V3.2-7** 메모 분리 · **V3.2-8** R15 3층 상속 · **V3.2-9** 타임라인 개체. 동결 v3.1(`ERD-FROZEN.md` v3.1 절)을 바탕으로 한다 — 사용자 정의 1·3·명시 예외 유지 · 정의 2 는 v3.1 개정판 유지 · 원칙 A·D 문장 개정(사용자 결정).")
    A("")
    A(f"기계용 동본 `erd-v3.2.json` · 값 사전 `erd-v3.2-dictionaries.json`(49 · ERD 값 불변 · closed · 파생 항목) · 행선지 `erd-v3.2-column-map.md`(이동 {len(moves32)} · 비고 {len(notes32)}) · 실측 `erd-v3.2-tuples.py`(→ `erd-v3.2-tuples.json` · §9) · 씨앗 후보 `erd-v3.2-seed-candidates.json/.md`(승인용) · 검산 `erd-v3.2-check.py`(§10). 생성기 `erd_spec_v32.py`·`erd_colmap_v32.py`·`erd_build_v32.py`. 이전 판 산출물은 그대로 두었다. **v3.1 → v3.2 변경 목록은 §11**, 관찰은 §12.")
    A("")
    A(f"**개체 {len(S.ENTITIES)}(v3.1 20 + post_procedure_timeline + emergency_sign) · 관계 {len(S.RELATIONS)}(31 + R33 + R34 + R35) · 사전 {len(dj['dictionaries'])} · 결정 kind {len(S.DECISION_KINDS)}(그대로) · 행선지 {len(colrows)}(이동 {len(moves32)})**.")
    A("")
    A("## 0. 사용자 정의 · 첫 규칙 · 원칙")
    A("")
    A("동결 원문(ERD-FROZEN · 글자 그대로):")
    A("")
    for n, t in S.USER_DEFINITIONS:
        A(f"{n}. {t}")
    A("")
    A("v3.1 문장(정의 2 개정판 · v3.2 도 이것을 쓴다):")
    A("")
    for x in erd["user_definitions_v31"]:
        A(f"{x['no']}. {x['text']}")
    A("")
    A(f"**명시 예외(v3.1 개정판 · 유지)**: {erd['explicit_exception_v31']}")
    A("")
    A(f"**v3.2 와 정의의 관계**: {S.USER_DEFINITIONS_V32_NOTE}")
    A("")
    A("### 0.1 첫 규칙 — 문구 종류 분류 먼저 (V3.2-0)")
    A("")
    A(S.RULE_ZERO)
    A("")
    A(md_table(["문구 종류", "원장 자리", "자기 테이블", "부작용과의 관계"], S.PHRASE_KIND_TABLE))
    A("")
    A("### 0.2 부작용 축 노드 원칙 (V3.2-0 교체)")
    A("")
    A(S.NODE_RULE)
    A("")
    A(S.OPEN_CLOSED_RULE)
    A("")
    A("**원칙(A·D 는 v3.2 문장 · B·C 그대로)**: " + " ".join(f"**{k}.** {v}" for k, v in S.PRINCIPLES))
    A("")
    A("## 1. 규칙")
    A("")
    A("층(브론즈 · 시맨틱 · 실버 · 골드)은 v3.1 §1 그대로. v3.2: 실버에서 원장 문구는 자기 테이블의 레코드(타임라인 줄 · 응급 징후 · 고지 · 근거 문장) 또는 부작용 문구 사전 항목이며, 부작용 단위는 부작용 문구 종류만 세운다. 지식은 원장 21(2판)·컬럼 리포트·스캔·erd-v* 산출물·발주서·검토서·ERD-FROZEN·`silver-v3/out/report.md` §14·`silver-v3/out/gate/batch4.*`·`silver-v3/README.md` 에서만 가져왔다(금지 목록은 열지 않았다).")
    A("")
    A("### 1.1 정규화 norm_v2 · 식별자")
    A("")
    A(f"- norm_v1(v3.1 그대로): " + " → ".join(S.NORMALIZE_RULE["steps"]))
    A(f"- **norm_v2(V3.2-2)**: " + " · ".join(S.NORM_V2["steps"]) + f" — {S.NORM_V2['note']}")
    for k in ("adverse_effect", "ledger_event", "equipment_product", "post_procedure_timeline", "emergency_sign", "phrase", "product"):
        A(f"- 식별자 `{k}`: {S.ID_RULE[k]}")
    A(f"- 결정 target · 접힘 조건 · locator 규칙은 v3.1 §1.1 그대로(`erd-v3.2.json → id_rule`).")
    A("")
    A("### 1.2 다이어그램")
    A("")
    A("```mermaid")
    A(mermaid())
    A("```")
    A("")
    A("### 1.3 토큰화 (V3.2-1) · 분해 규칙")
    A("")
    A(S.TOKENIZE_RULE)
    A("")
    tk = S.RESOLVE_RULES["tokenize"]
    A(f"- 조사 {len(tk['particles'])}: " + " · ".join(tk["particles"]))
    A(f"- 용언 어미 {len(tk['verb_endings'])}: " + " · ".join(tk["verb_endings"]))
    A(f"- 문법 낱말 {len(tk['grammar_words'])}: " + " · ".join(tk["grammar_words"]))
    A("- 참조 분해 3단계 · stopwords · 회사 괄호 · 조합 기호 · 회·차 · 겹침은 v3.1 §1.3 그대로(`resolve_rules`). 실측 §9.11.")
    A("")
    A("### 1.4 시술 튜플 — what 규칙 v3.2 (V3.2-5 장비 · V3.2-6 성분)")
    A("")
    A(S.EQUIP_RULE)
    A("")
    A(S.INGREDIENT_RULE)
    A("")
    A("그 밖 §1.4(접힘 · site · technique · 엣지 끝)는 v3.1 그대로.")
    A("")
    A("### 1.5 부작용 단위·문구 (V3.2-0 노드 원칙 · V3.2-7 · V3.2-8)")
    A("")
    A("- 단위 = (사건, 부위, 물질) 세 칸 · 경과는 R15 · 상대 부위 none · 수식어 목록(V3.1-8) — v3.1 그대로.")
    A(f"- **노드 원칙**: §0.2.")
    A(f"- **문구 종류 판정(V3.2-7)**: {S.PHRASE_KIND_RULE}")
    pk = S.TUPLE_RULES["phrase_kinds"]
    A(f"  - 메모 어휘 {len(pk['note_words'])}: " + " · ".join(pk["note_words"]) + f" · 설명문 문턱: 멤버 토큰 ≥{pk['sentence_min_tokens']} · 문법 ≥{pk['sentence_min_grammar']} · 라틴 비율 ≥{pk['sentence_latin_ratio']} · 대체 핵심어 {pk['fallback_core']} · 핵심어 제외 {pk['core_exclude']} · ⑦ 규칙 {pk['dup_rules']}.")
    A(f"- **R15 속성 상속(V3.2-8)**: {S.INHERIT_RULE}")
    A("")
    A("### 1.6 사람 조건 — v3.1 그대로 + 토큰화(V3.2-1)")
    A("")
    A("조건 사전·완전 일치·raw_name 단위·문장 부록은 v3.1 §1.6 그대로. v3.2: 조사·어미를 떼고 어간을 다시 사전에 댄다(「자가면역질환이」→ 자가면역질환 + 이) — v3.1 §12 의 「조사 분리 False」를 토큰화 규칙으로 바꾼 것이다. 실측 §9.7 · §9.10.")
    A("")
    A("### 1.7 사전 씨앗 규칙 (V3.2-3 · V3.2-4 신설)")
    A("")
    A(S.SEED_RULE)
    A("")
    A(S.SITE_DICT_RULE)
    A("")
    A("사전 닫힘: " + " · ".join(f"{k} {'닫힘' if v else '열림'}" for k, v in S.CLOSED_DICTIONARIES.items()) + " · 그 밖 사전은 v3.2 씨앗 규칙 대상 아님(closed=null · 정하지 않았다).")
    A("")
    A("### 1.8 자기 테이블 — 타임라인 · 응급 징후 · 고지 · 문헌 (V3.2-9 · V3.2-0)")
    A("")
    for t in (S.TIMELINE_RULE, S.SIGN_RULE, S.DISCLOSURE_RULE_V32, S.LITERATURE_RULE):
        A(f"- {t}")
    A("")
    A("## 2. 개체 목록")
    A("")
    A(f"개체 {len(S.ENTITIES)}. v3.2 에서 바뀐 것: adverse_effect(event_kind dict|ledger · general_* · raw_name 속성 삭제) · clinical_rule(parsed · adverse_ref · phrase_ids 삭제) · evidence_statement(kind adverse_effects · adverse_ref) · product(origin taxonomy) · procedure(what_kind ingredient · ingredient_fragments · grammar_tokens) · site(parent) · decision(비고) · 신설 post_procedure_timeline · emergency_sign.")
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
    A(f"관계 {len(S.RELATIONS)}. v3.2: **R15**(timeline_refs · emergency_sign_refs · inheritance · layer · period/phase_label/reaction_level/disclosure 삭제) · R19/R20 비고 · 신설 **R33 has_timeline · R34 timeline_refers · R35 sign_refers**. 엣지 끝 규칙: " + S.EDGE_END_RULE)
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
    A(f"`erd-v3.2-dictionaries.json` — {len(dj['dictionaries'])} 사전. ERD 값·동의어·순서는 v3.1 과 같다(검산 O-2). 더한 것: 사전마다 `closed` · site 항목 `parent`(null) · 열린 사전의 파생 항목(adverse_event_type origin=ledger {len(R['adverse']['ledger_events'])} · product_name origin=taxonomy {len(R['equipment']['products'])} — status=unreviewed · 분해는 이것을 빼고 돈다) · 문구 사전 v3.2(부작용 문구만).")
    A("")
    A(md_table(["사전", "종류", "closed", "ERD 값", "파생 항목", "동의어"], [(d["name"], d.get("kind", "value"), d.get("closed"), sum(1 for e in d["entries"] if e.get("origin") not in ("ledger", "taxonomy")) if d["name"] != "phrase_dictionary" else "—", sum(1 for e in d["entries"] if e.get("origin") in ("ledger", "taxonomy")) if d["name"] != "phrase_dictionary" else len(d["entries"]), sum(len(e.get("synonyms", [])) for e in d["entries"])) for d in dj["dictionaries"]]))
    A("")
    A("## 5. 결정")
    A("")
    A(f"결정 kind {len(S.DECISION_KINDS)}(v3.1 그대로 · 비고만 바뀐 kind: " + " · ".join(f"`{k}`({v})" for k, v in S.DECISION_KINDS_NOTE_V32.items()) + "). 적용 순서 ⓪①~⑦ · target 안정 키 · 빌드는 approved 만 — v3.1 §5 그대로.")
    A("")
    A(md_table(["kind", "빌드 적용", "target", "new_value", "비고"], [(f"`{k}`", "○" if br else "기록만", t, nv, n[:300]) for k, br, t, nv, n in S.DECISION_KINDS]))
    A("")
    A(f"결정 레코드: v3.1 의 {len(v31['decisions'])} 이관(모양·값 그대로) + DEC-2026-11-05-28(v3.2 개정 · scope_review · proposed).")
    A("")
    A("## 6~8. 원장 파일 매핑 · 질문 25 · 처분")
    A("")
    A("v3.1 §6~§8 그대로(브론즈 2판 해시 동일 · 질문 답·처분 변경 없음). 잎 키 행선지 변경은 `erd-v3.2-column-map.md`.")
    A("")
    A("## 9. 실측 (`erd-v3.2-tuples.py` 실제 실행 · 숫자는 목표가 아니다)")
    A("")
    A("### 9.5 시술 튜플 (v3.2 규칙 · v3.1 열과 나란히)")
    A("")
    A(TUP.V31.procedure_md(R, v31["tuple_report"]["procedure"]))
    A("")
    A(TUP.V31.condition_md(R))
    A("")
    A("### 9.9~9.17 v3.2 실측")
    A("")
    A(TUP.v32_md(R))
    A("")
    A("## 10. 검산 결과")
    A("")
    A("`erd-v3.2-check.py` 를 독립 실행한 출력을 그대로 붙였다.")
    A("")
    return "\n".join(o)


def change_log(R, v31, colrows, moves32, notes32, dj):
    b, a, p = R["v32"]["before"], R["v32"]["after"], R["v32"]["projection"]["R"]
    s = R["adverse"]["summary"]
    S_ = R["v32"]["seeds"]
    o = []
    A = o.append
    A("## 11. v3.1 → v3.2 변경 목록")
    A("")
    rows = []
    meas = {
        "V3.2-0": f"부작용 문구 {s['safety_occurrences']} → exact {s['safety_by_status'].get('exact', 0)} · new {s['safety_by_status'].get('new', 0)} · 메모 {s['safety_by_status'].get('note', 0)} · 설명문 {s['safety_by_status'].get('sentence', 0)} · unlinked 0 · 원장 사건 노드 {s['ledger_events']} · ⑦ {s['dup_pairs']} · raw_name {b['raw_name_units']} → 0 · 응급 징후 {s['emergency_signs']}({s['r35']} 참조)",
        "V3.2-1": f"목록 {len(R['v32']['tokenizer_words'])} · 사라진 조각 부작용 {R['v32']['disappeared_by_tokenizer']['adverse']['distinct']} · 시술 {R['v32']['disappeared_by_tokenizer']['procedure']['distinct']} · 조건 {R['v32']['disappeared_by_tokenizer']['condition']['distinct']}",
        "V3.2-2": f"병기 쌍 {len(R['adverse']['gloss_pairs']) + len(R.get('gloss_pairs_other', []))} · 자모 변형 쌍 {len(R['v32']['variant_pairs'])}(적용 0)",
        "V3.2-3": "승인 묶음 " + " · ".join(f"{k} {sum(1 for r in v['rows'] if r.get('status') == 'proposed')}/{len(v['rows'])}" for k, v in S_.items()),
        "V3.2-4": f"부위 닫힌 목록 {len(S_['site']['rows'])}(기존 {sum(1 for r in S_['site']['rows'] if r['existing'])} · 새 후보 {sum(1 for r in S_['site']['rows'] if r['status'] == 'proposed')})",
        "V3.2-5": f"장비 제품 자동 {a['equipment_products']} · 항목 자신 {b['catalog_self']} → {a['catalog_self']} · 줄임말 후보 {len(S_['product_abbrev']['rows'])}",
        "V3.2-6": f"성분 what {a['ingredient_what']} · 성분 후보 {sum(1 for r in S_['ingredient_material']['rows'] if r.get('status') == 'proposed')}",
        "V3.2-7": f"메모 {s['safety_by_status'].get('note', 0)} · 설명문 {s['safety_by_status'].get('sentence', 0)}(자리) · 항목 {s['memo_entries']}",
        "V3.2-8": f"항목 엣지 {s['inheritance_item_edges']} · basis 없음 {s['inheritance_missing_basis']} · 복사 {s['inheritance_copied_values']}",
        "V3.2-9": f"타임라인 {s['timelines']} · 단계 {s['timeline_phases']} · 줄 {s['timeline_lines']}({', '.join(f'{k} {v}' for k, v in s['timeline_lines_by_status'].items())}) · R34 {s['r34']}",
    }
    for no, what, where in S.CHANGE_LIST_V32:
        rows.append((no, what, where, meas.get(no, "")))
    A(md_table(["#", "무엇", "어디서 반영", "실측(v3.2)"], rows))
    A("")
    A(f"- 개체 20 → {len(S.ENTITIES)} · 관계 31 → {len(S.RELATIONS)} · 사전 49 → {len(dj['dictionaries'])}(이름 그대로) · 결정 kind 20 → {len(S.DECISION_KINDS)} · 행선지 이동 {len(moves32)} · 비고 {len(notes32)} · 결정 레코드 {len(v31['decisions'])} → {len(v31['decisions']) + 1}.")
    A(f"- 적용 전후 핵심: ⑨ {b['unresolved_9']} → {a['unresolved_9']}(씨앗 승인 가정 {p['unresolved_9']}) · 항목 자신 {b['catalog_self']} → {a['catalog_self']}({p['catalog_self']}) · 문구 unlinked 항목 {b['phrase_entries_by_status'].get('unlinked')} → 0 · 부작용 미등록 조각 {b['adverse_unregistered_distinct']}/{b['adverse_unregistered_total']} → 부작용 문구 종류 {a['adverse_kind_unregistered']}(참조 테이블 {a['reference_tables_unregistered_distinct']}/{a['reference_tables_unregistered_total']}).")
    A("")
    A("**검토 반영 S-1~S-4**(`erd-v3.2-review.md` · 판 번호 v3.2 그대로 · 개체·관계·kind 변경 없음):")
    A("")
    rv = R["v32"].get("review", {})
    A(f"- **S-1 핵심어 범위**: 멤버를 접속 조사로 토막 내고, 사전 사건이 닿는 토막은 그 사건에 exact(옆 미등록 토큰은 side 보존 · 노드 후보 목록) · 사전 사건이 0 인 토막만 핵심어 새 노드(§0.2 · 원칙 A · json node_rule · tuples.py _apply_cores). 원장 사건 노드 {rv.get('nodes_before', '—')} → **{s['ledger_events']}** · 사전 사건을 품은 노드 {rv.get('absorbed_before', '—')} → 0 · 부작용 문구 exact {rv.get('exact_before', '—')} → {s['safety_by_status'].get('exact', 0)} · new {rv.get('new_before', '—')} → {s['safety_by_status'].get('new', 0)} · 단위 {rv.get('units_before', '—')} → {s['units_total']}.")
    A(f"- **S-2 ⑦ 범위**: 노드끼리(사전 ↔ 노드 · 노드 ↔ 노드 · 원장 병기 X(Y)) · strong/weak 등급 — ⑦ {rv.get('dup_before', '—')} → {s['dup_pairs']}(strong {s['dup_pairs_strong']} 기본 게이트 · weak {s['dup_pairs_weak']} 표시만 · 노드 ↔ 노드 {s['dup_pairs_node_node']}).")
    A(f"- **S-3 잔재 정리**: adverse_effect 속성 표(event · status · origins · extra_* · 식별자) · R15 규칙 문장 · 열거형(adverse_expression.* · adverse_effect.raw_reason 삭제 · status complete · reference.ref_status → table_line.ref_status) · adverse_tuple_assign target · id_rule · tuple_rules.adverse · 행선지 비고 {len(C.SCRUBBED_V32)} 행에서 옛 문장을 지웠다(조건 축 raw_name 은 다른 개념이라 유지 · 검산 S-3).")
    A(f"- **S-4 토큰화 보강**: relaxed 접미(에서·으로·이·가·을·를·의·에·「~시」 · 어간 한글 2자 이상) · 용언 꼴 predicate(-는·-된·-운·-지고·-하게·-하므로·-되며) · 접속 조사 토막 경계 — 원소마다 locator(§9.11).")
    A("")
    A("## 12. v3.2 밖 관찰 — 결정·다음 판 후보 (레코드는 만들지 않았다)")
    A("")
    obs = [
        ("원장 사건 노드 접기", f"⑦ strong {s['dup_pairs_strong']} 은 fold_approve / conflict_close 결정 묶음의 자리(단계 끝 = open 0) · weak {s['dup_pairs_weak']} 은 표시만 — weak 를 게이트에 올릴지는 결정. side 토큰(사전 사건 옆 미등록)은 노드 후보 목록 — 부위·수식어 사전 추가로 풀리는 것이 대부분", "fold_approve · conflict_close · dictionary_add"),
        ("핵심어 품질", "핵심어는 원장 문구 그대로라 「근력 약화」「하악변연신경 손상」 같은 좋은 노드와 「만져지는」「들어가 괴사」처럼 용언·조각이 남은 노드가 함께 나온다(unreviewed) — 판정은 fold_approve · adverse_tuple_assign · phrase_map. 수식어 목록(V3.1-8) misc 의 내용어(약화·악화·변화 …)는 대체 핵심어로만 썼다", "fold_approve · 규칙 데이터 개정"),
        ("raw_name 대상 옛 결정", "v3.1 까지 raw_name 단위를 target 으로 한 결정(adverse_tuple_assign · 실버 B2B/B3 10 건)은 이름 locator 로 그대로 닿는다 — 실버 빌더는 v3.2 에서 그 locator 의 핵심어 노드를 지정 단위로 대체해야 한다(빌더 개정 몫)", "실버 빌더"),
        ("정상 줄 해석", "V3.2-9 「정상 줄은 참조 없는 경과 메모」와 V3.2-7 「타임라인 normal 은 R15 reaction_level=normal 기존 경로 유지」를 함께 지키려고, 정상 줄도 이미 있는 단위에 닿으면 참조하고 닿지 않으면 정상 메모로 두었다 — 정상 줄은 늘 참조하지 않는 쪽이 맞다면 결정", "scope_review"),
        ("응급 징후 · 시술 전 확인", "응급 징후는 V3.2-0 표대로 자기 테이블(emergency_sign)로 올렸다. pre-procedure-checklist 는 person_condition(kind=check)이 이미 원장 표를 그대로 두고 있어 구조를 바꾸지 않았다(규칙 문장 「— 대기 원칙」은 v3.1 §12 그대로 열려 있음)", "scope_review"),
        ("조건 축 노드 원칙", "부작용 축과 같은 「사전에 없으면 핵심어 노드」를 조건 축(raw_name 210)에 적용할지는 이번 범위 밖 — 조건의 raw_name 단위가 이미 「자기 자신 노드」 역할을 한다", "scope_review"),
        ("씨앗 묶음 잡음", "성분 문맥(바로 옆 토큰)·시술 조각·자모 변형 쌍은 규칙이 넓게 뽑는다(심부·약한 · 부족↔부종) — 승인 묶음이라 적용 0 이지만 고를 양이 많다. 「등」은 부위와 수식어가 같은 꼴(동형어 표시)", "dictionary_add"),
        ("참고 실행", f"부위·성분 씨앗을 전부 승인하면 ⑨ {a['unresolved_9']} → {p['unresolved_9']} · 항목 자신 {a['catalog_self']} → {p['catalog_self']} — 숫자는 목표가 아니고 승인 판단의 참고", "—"),
        ("v3.1 동결 승계", "v3.1 §12 의 열린 항목(조건 kind 식별자 · R32 제품 note · 수식 사전 겹침 등)은 그대로", "v3.1 §12"),
    ]
    A(md_table(["어디", "무엇", "decision kind / 자리"], obs))
    return "\n".join(o)


def main():
    v31 = jload("erd-v3.1.json")
    v31tup = jload("erd-v3.1-tuples.json")
    bronze = B31.B3.bronze_meta()
    assert not bronze["mismatch"], f"브론즈 2판 HASHES.txt 불일치: {bronze['mismatch']}"
    rescan = B31.B3.rescan_v2()
    step1_scan = B31.B11.scan_step1()
    colrows = build_column_map(step1_scan)
    moves32, notes32 = write_column_map(colrows, step1_scan, rescan)
    base = base_dictionaries()
    rules, rrules = roundtrip(S.TUPLE_RULES), roundtrip(S.RESOLVE_RULES)
    rules["adverse"]["adverse_stopwords"] = v31["tuple_rules"]["adverse"]["adverse_stopwords"]
    rules["condition"] = v31["tuple_rules"]["condition"]
    for p_ in ("erd-v3.2.json",):
        if os.path.exists(os.path.join(WORK, p_)):
            os.remove(os.path.join(WORK, p_))
    Lfull = {f: json.load(open(os.path.join(TUP.LEDGER, f), encoding="utf-8")) for f in os.listdir(TUP.LEDGER) if f.endswith(".json")}
    prev = None
    pp = os.path.join(WORK, OUT["tuples"])
    if os.path.exists(pp):
        prev = json.load(open(pp, encoding="utf-8"))["adverse"]["summary"]
    R = TUP.run_everything(base, rules, Lfull, rrules, v31tup)
    R["v32"]["review"] = REVIEW_BEFORE
    dj = finalize_dictionaries(base, R)
    json.dump(dj, open(os.path.join(WORK, OUT["dict"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    json.dump(TUP.slim(R), open(os.path.join(WORK, OUT["tuples"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    TUP.seed_files(R)
    erd = build_json(v31, colrows, moves32, notes32, dj, R)
    erd["tuple_rules"] = rules
    erd["resolve_rules"] = rrules
    json.dump(erd, open(os.path.join(WORK, OUT["json"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = build_md(erd, colrows, dj, R, v31, moves32, notes32)
    cl = change_log(R, v31, colrows, moves32, notes32, dj)
    open(os.path.join(WORK, OUT["md"]), "w", encoding="utf-8").write(md + "(검산 실행 중)\n\n" + cl + "\n")
    chk = load_module("chk32", os.path.join(WORK, OUT["check"]))
    ok, report = chk.run_checks()
    open(os.path.join(WORK, OUT["md"]), "w", encoding="utf-8").write(md + report + "\n\n" + cl + "\n")
    with open(os.path.join(WORK, OUT["cmap"]), "a", encoding="utf-8") as f:
        f.write("## 검산 결과\n\n" + report + "\n")
    print("OK" if ok else "FAIL")
    print(report)


if __name__ == "__main__":
    main()
