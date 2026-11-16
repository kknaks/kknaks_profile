# -*- coding: utf-8 -*-
"""report.md · manifest.json · ERD 실측 대조."""
import json
import os
from collections import Counter, OrderedDict

from .proposals import STOPWORDS
from .util import dumps, md_table, sha256_bytes, sha256_file, write_json, write_text


def jnorm(x):
    return json.loads(json.dumps(x, ensure_ascii=False, default=str))


def compare(S, tuples_json_path):
    """결정 ⓪~⑦ 적용 전 분해(ERD 사전) 요약 vs ERD 실측(erd-v3.1-tuples.json) 요약 — 키마다(시술 · 부작용 · 조건) + 행 단위."""
    ref = json.load(open(tuples_json_path, encoding="utf-8"))
    rows = []
    P0, A0, C0 = S.ctx.get("cmp_base") or (S.ctx["proc0"], S.ctx["adv0"], S.ctx["cond0"])   # v3.3: 분석기 없는 분해(ERD 실측 조건)
    for part, mine in (("procedure", P0["summary"]), ("adverse", A0["summary"]), ("condition", C0["summary"])):
        rs = (ref.get(part) or {}).get("summary", {})
        for k, v in mine.items():
            if k.startswith("_"):
                continue
            rv = rs.get(k, "(ERD 실측에 없는 키)")
            rows.append({"part": part, "key": k, "build": jnorm(v), "erd": rv, "same": jnorm(v) == rv})
    PT = P0["PT"]
    ra, rc_ = ref.get("adverse") or {}, ref.get("condition") or {}
    rows.append({"part": "procedure", "key": "tuple_ids(순서 포함)", "build": len(PT.tuples), "erd": len(ref["procedure"]["tuples"]), "same": [t for t in PT.tuples] == [t["id"] for t in ref["procedure"]["tuples"]]})
    rows.append({"part": "adverse", "key": "tuple_ids(순서 포함)", "build": len(A0["tuples"]), "erd": len(ra.get("tuples", [])), "same": [t["id"] for t in A0["tuples"]] == [t["id"] for t in ra.get("tuples", [])]})
    me = [(r["locator"], r["unit_ids"]) for r in A0["complications"]]
    rx = [(r["locator"], r["unit_ids"]) for r in ra.get("complications", [])]
    rows.append({"part": "adverse", "key": "complications(locator·단위)", "build": len(me), "erd": len(rx), "same": me == rx})
    me = [(e["id"], e["status"], e["units"]) for e in A0["phrase_dictionary"]]
    rx = [(e["id"], e["status"], e["units"]) for e in ra.get("phrase_dictionary", [])]
    rows.append({"part": "adverse", "key": "phrase_dictionary(PHR·status·단위)", "build": len(me), "erd": len(rx), "same": me == rx})
    me = jnorm([(e["from_"], e["unit"], e["courses"], e["source_phrases"]) for e in A0["edges"]])
    rx = [(e["from_"], e["unit"], e["courses"], e["source_phrases"]) for e in ra.get("edges", [])]
    rows.append({"part": "adverse", "key": "R15 edges(출발·단위·경과·문구)", "build": len(me), "erd": len(rx), "same": me == jnorm(rx)})
    rows.append({"part": "condition", "key": "unit_ids(순서 포함)", "build": len(C0["units"]), "erd": len(rc_.get("units", [])), "same": [u["id"] for u in C0["units"]] == [u["id"] for u in rc_.get("units", [])]})
    cat = [(r["family"], r["name"], r.get("procedure_id"), r["status"]) for r in P0["cat_recs"]]
    rc = [(r["family"], r["name"], r.get("procedure_id"), r["status"]) for r in ref["procedure"]["catalog"]]
    rows.append({"part": "procedure", "key": "catalog(항목→튜플·상태)", "build": len(cat), "erd": len(rc), "same": cat == rc})
    return rows


def manifest(S, args, recs, edges, cmp_rows, gate_counts, out_dir):
    meta = S.ctx["meta"]
    m = OrderedDict()
    m["builder"] = "silver-v3 build.py"
    m["erd"] = {"file": os.path.basename(args.erd), "sha256": sha256_file(args.erd), "version": S.ctx["erd"]["erd_version"]}
    m["dictionaries"] = {"file": os.path.basename(args.dict), "sha256": sha256_file(args.dict)}
    m["column_map"] = {"file": os.path.basename(args.colmap), "sha256": sha256_file(args.colmap)}
    m["inputs"] = OrderedDict((f, {"sha256": v["sha256"], "bytes": v["bytes"]}) for f, v in sorted(meta.items()))
    m["inputs_count"] = len(meta)
    if S.ctx.get("bronze"):  # 브론즈 2판~ (HASHES.txt) — 1판은 넣지 않는다(바이트 동일)
        m["bronze_version"] = S.ctx["bronze"]
    m["decisions"] = OrderedDict([
        ("approved_read", [{"id": d["id"], "kind": d["kind"], "store_file": d.get("_file"), "origin": "store" if d.get("_file") else "ledger_memo(taxonomy.json · 질문 23)"} for d in S.ctx["decisions_approved"]]),
        ("apply_log", S.apply_log),
        ("listed_not_read", [{"id": d["id"], "status": d["status"], "kind": d["kind"], "store_file": d.get("_file")} for d in S.ctx["decisions_listed"]]),
        ("invalid", S.ctx["decisions_invalid"]),
    ])
    m["counts"] = {"entities": {t: len(r) for t, r in recs.items()}, "relations": {k: len(v) for k, v in edges.items()}, "gate": gate_counts,
                   "conflicts": {f"{c[0]} {c[1]} {c[2]}": n for c, n in sorted(Counter((x["rule_ref"], x["kind"], x["status"]) for x in S.conflicts).items())},
                   "product_origin": dict(sorted(Counter(r["attrs"]["origin"][0]["value"] for r in recs["product"]).items())),
                   "product_ids": sorted(r["id"] for r in recs["product"]),
                   "procedure_by_origin_what": dict(sorted(Counter("+".join(r["attrs"]["origins"][0]["value"]) + ":" + r["attrs"]["what_kind"][0]["value"] for r in recs["procedure"]).items()))}
    m["erd_comparison"] = {"keys": len(cmp_rows), "diff": sum(1 for r in cmp_rows if not r["same"])}
    files = []
    for root, dirs, fs in os.walk(out_dir):
        dirs.sort()
        for f in sorted(fs):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, out_dir)
            if rel in ("manifest.json",):
                continue
            files.append((rel, sha256_file(p)))
    m["outputs"] = OrderedDict(sorted(files))
    m["determinism_key"] = sha256_bytes(dumps({"inputs": m["inputs"], "erd": m["erd"]["sha256"], "dict": m["dictionaries"]["sha256"], "decisions": [d["id"] for d in S.ctx["decisions_approved"]], "outputs": m["outputs"]}).encode())
    m["note"] = "빌드 시각은 manifest 밖(재실행 바이트 동일). 시각이 필요하면 build.py 표준 출력에만 찍는다."
    write_json(os.path.join(out_dir, "manifest.json"), m)
    return m


def report(S, recs, edges, cmp_rows, gate_counts, proposals, out_dir):
    cs = S.conflicts
    o = []
    A = o.append
    A(f"# 실버 빌드 리포트 — ERD {S.ctx['erd'].get('erd_version')}(동결)")
    A("")
    _inp = ("원장은 " + S.ctx["bronze"]["label"] + " · HASHES.txt 일치 · step1 sha256 ERD 일치") if S.ctx.get("bronze") else "sha256 ERD 일치"
    _a = S.ctx["args"]
    A("입력: 브론즈 22(원장 21 + step1-products.json) " + _inp + f" · ERD `{os.path.basename(_a.erd)}` · 사전 `{os.path.basename(_a.dict)}` · 잎 키 행선지 `{os.path.basename(_a.colmap)}`. 결정은 status=approved 만 읽었다. §1~§9 는 이번 빌드 수치, §10~ 은 빌드 차수별 대조.")
    A("")
    A("## 1. 개체별 레코드 수")
    A("")
    A(md_table(["개체", "레코드"], [(t, len(r)) for t, r in recs.items()]))
    A("")
    A("## 2. 관계별 엣지 수")
    A("")
    A(md_table(["관계", "엣지", "비고"], [(k, len(v), REL_NOTE.get(k, "")) for k, v in edges.items()]))
    A("")
    A("## 3. 충돌 — kind · 규칙 · 상태")
    A("")
    A(md_table(["kind", "rule", "status", "건"], [(k[0], k[1], k[2], n) for k, n in sorted(Counter((c["kind"], c["rule_ref"], c["status"]) for c in cs).items())]))
    A("")
    A(f"합계 {len(cs)} · ⑦⑧⑨ {sum(1 for c in cs if c['kind'] in ('duplicate_candidate', 'unregistered_value', 'unresolved_reference'))}")
    A("")
    A("## 4. gate 목록")
    A("")
    A(md_table(["목록", "건"], [("unresolved_references (⑨)", gate_counts["unresolved_references"]), ("unregistered_fragments (⑧ · 조각+사전 밖 값)", gate_counts["unregistered_fragments"]),
                              ("unlinked_phrases (문구 사전 unlinked 항목 · 자리)", f"{gate_counts['unlinked_phrases']} · 자리 {gate_counts['unlinked_phrase_locators']}"), ("catalog_partial (항목 자신 시술)", gate_counts["catalog_partial"]),
                              ("conflicts.md ⑦ duplicate_candidate", gate_counts["conflicts_md_duplicate"]), ("conflicts.md ⑥ open", gate_counts["conflicts_md_open_value"]), ("conflicts.md ④ auto", gate_counts["conflicts_md_auto"])]))
    A("")
    A(f"## 5. ERD 실측({os.path.basename(S.ctx['args'].tuples)}) 대조 — 결정 ⓪~⑦ 적용 전 분해(ERD 사전 · 시술 · 부작용 단위·문구 사전 · 조건 단위)")
    A("")
    diff = [r for r in cmp_rows if not r["same"]]
    A(f"키 {len(cmp_rows)} · 차이 **{len(diff)}**. 대표 수치:")
    A("")
    pick = ["catalog_items", "catalog_distinct_tuples", "tuples_total", "edge_ends_total_n", "edge_ends_total", "reference_total", "market_pricing", "unregistered_distinct", "unregistered_total",
            "complications_names", "complications_distinct_tuples", "complications_distinct_tuples_raw", "tuples_status", "phrase_entries", "phrase_entries_by_status", "edges_total", "units_created_by_phrases",
            "units_total", "units_dict", "units_raw", "tuple_ids(순서 포함)", "complications(locator·단위)", "phrase_dictionary(PHR·status·단위)", "R15 edges(출발·단위·경과·문구)", "unit_ids(순서 포함)", "catalog(항목→튜플·상태)"]
    rows = []
    for r in cmp_rows:
        if r["key"] in pick:
            short = lambda v: (json.dumps(v, ensure_ascii=False)[:120])  # noqa
            rows.append((r["part"], r["key"], short(r["build"]), short(r["erd"]), "같음" if r["same"] else "**다름**"))
    A(md_table(["축", "키", "빌드", "ERD 실측", "대조"], rows))
    A("")
    if diff:
        A("다른 키 — 어느 쪽이 틀렸는지:")
        for r in diff:
            A(f"- {r['part']}.{r['key']}: 빌드 {json.dumps(r['build'], ensure_ascii=False)[:200]} / ERD {json.dumps(r['erd'], ensure_ascii=False)[:200]}")
    else:
        A("전부 같다 — 분해 모듈(lib/decompose.py · lib/adverse31.py)이 참조 구현 erd-v3.1-tuples.py 와 같은 튜플·단위·문구 사전 항목·조건 단위·같은 id·같은 등록 순서를 낸다(행 단위 대조 포함).")
    A("")
    changed = [x for x in S.apply_log if x.get("result") == "applied"]
    A(f"결정 적용 뒤(실버 산출물) 수치는 적용된 결정만큼 다를 수 있다 — 이번 빌드에서 값을 바꾼(applied) 결정 {len(changed)} 건: " + (", ".join(f"{x['id']}({x['kind']} {x.get('stage')})" for x in changed) or "없음") + ". 나머지는 기록만(recorded):")
    A("")
    A(md_table(["결정", "kind", "단계", "결과"], [(x["id"], x["kind"], x.get("stage"), x.get("result") + (f" · {x.get('anchors') or x.get('note') or ''}" if x.get("result") else "")) for x in S.apply_log]))
    A("")
    A("## 6. 결정 묶음 1 제안 (decisions/proposed/ · status=proposed · 빌드가 읽지 않음)")
    A("")
    A(md_table(["묶음", "건"], [("1. 제품 사전 확장 dictionary_add(product_name)", len(proposals["products"])), ("   제외 목록(확인 불가·병원 메뉴명·업체명·kind 밖·근거 없음·이미 원장 등)", len(proposals["excluded"])),
                              ("2. 동의어 dictionary_add", len(proposals["synonyms"])), ("   제안하지 않은 조각(근거 없음·둘 이상 후보·이미 사전 값)", len(proposals["not_proposed"])), ("4. 빈 템플릿", len(proposals["templates"]))]))
    A("")
    A("제안하지 않은 동의어 조각:")
    for x in proposals["not_proposed"]:
        A(f"- 「{x['fragment']}」 — {x['why']}")
    A("")
    A("제품 제외 목록 사유별: " + ", ".join(f"{k}={v}" for k, v in Counter(x["reason"].split(" — ")[0] if "—" in x["reason"] else x["reason"] for x in proposals["excluded"]).most_common()))
    A("")
    A("## 7. ERD 개정 후보 (결정 파일로 만들지 않음)")
    A("")
    unreg = S.ctx["proc0"]["summary"]["_unregistered_all"]
    if S.ctx["erd"].get("erd_version") == "v3.1":
        A("- v3 의 「제품 계열 재분류 kind 없음 · 동의어 제거 kind 없음 · clinical_rule → 제품/기법 관계 없음」은 v3.1 에서 닫혔다(product_reclassify ⓪ · dictionary_remove ① · R32) — 엑소좀 EXO-02·05·06 을 그 kind 로 적용(§14).")
        A("- **R12 밖 회·차** — R9/R17/R18 자리의 「N회」「N차」는 엣지 속성 자리가 없어 qualifier_text 로만 남는다(V3.1-5 그대로).")
        A("- **적합성 열거기 범위** — tests/enumerate_cases.py 의 RULE_ROOTS·RESULT_ENUMS 는 정적 목록이라 tuple_rules.condition · 문구 사전 status/shape 외 열거형은 경우로 뽑히지 않는다(ERD §12 「열거기 개정 몫」 · 이번 발주는 2,514 경우).")
    elif S.ctx["erd"].get("erd_version") == "v3":
        A("- ~~resolve_rules.stopwords~~ — ERD v3(V3-3)에 들어갔다(단어 19 · 결정 전 분해에서 미등록 조각이 아니라 qualifier_text). 지금 남은 미등록 횟수: " + ", ".join(f"`{w}`×{unreg.get(w, 0)}" for w in STOPWORDS) + ".")
    else:
        A("- **resolve_rules.stopwords**(발주서 결정 묶음 1-3) — 수식어 제외 목록. 1차 빌드 시술 축 미등록 횟수: " + ", ".join(f"`{w}`×{unreg.get(w, 0)}" for w in STOPWORDS) + ". 규칙 데이터 변경이라 ERD 개정(v3) 사안이다.")
    A("- **분해 사전 순서에 성분 사전(ingredient_material) 없음** — CaHA·PLLA·PCL·PDO 는 이미 성분 사전 정준값인데 §1.3 사전 순서(product → modality_subcategory → procedure → site → spec → product_tier)에 성분 사전이 없어 미등록 조각이 된다. 동의어 추가로는 안 풀린다.")
    A("")
    cov_n, miss = coverage(S, out_dir)
    A(f"## 8. 잎 키 행선지 대조 ({os.path.basename(S.ctx['args'].colmap)} 1,072 · 브론즈만/버림 제외)")
    A("")
    A(f"행선지(개체·엣지·사전) 잎 키 {cov_n} 중 실버 값·엣지·충돌·사전 출처에 locator 로 닿은 것 {cov_n - len(miss)} · 안 닿은 것 {len(miss)}:")
    A("")
    A(md_table(["파일", "잎 키", "표적", "까닭"], [(f, p, t, MISS_WHY.get((f, p), "—")) for (f, p), t in miss]))
    A("")
    A("## 9. 해석 보류")
    A("")
    if S.notes:
        for n in S.notes:
            A(f"- {n['where']}: {n['text']}")
    for x in HOLD:
        A(f"- {x}")
    A("")
    A(f"해석 보류 {len(S.notes) + len(HOLD)} 건.")
    write_text(os.path.join(out_dir, "report.md"), "\n".join(o))
    return len(S.notes) + len(HOLD)


MISS_WHY = {
    ("extracted.json", "{code}.safety.serious"): "값이 null 2(M10·M13) = 미입력(질문 17) — 엣지 없음",
    ("procedure-comparison.json", "comparisons[].procedures[].asian_skin_note"): "그 비교 행의 시술 이름이 미해결(⑨) — 끝이 없어 R12 엣지가 없다(⑨ 레코드에 이름 locator)",
    ("treatment-sequence.json", "minimum_intervals[].reason"): "reason 이 있는 간격 행은 한쪽 끝 이상이 미해결(⑨) — R18 엣지가 없다",
    ("step1-products.json", "items[].6_companies.conflicts"): "명시적 빈 목록 384 = 충돌 없음 — 레코드가 생기지 않는다",
}


def coverage(S, out_dir):
    seen = set()

    def addd(d):
        if ".json:" in d and "#" not in d:
            fl, rest = d.split(":", 1)
            seen.add((fl, rest.rsplit("@", 1)[0]))
    for f in os.listdir(os.path.join(out_dir, "entities")):
        for l in open(os.path.join(out_dir, "entities", f), encoding="utf-8"):
            r = json.loads(l)
            for p in r.get("provenance", []):
                seen.add((p["file"], p["path"]))
            for d in r.get("derived_from", []):
                addd(d)
            for cells in list(r["attrs"].values()) + [r.get("aliases", [])]:
                for c in cells:
                    for p in c.get("prov", []):
                        seen.add((p["file"], p["path"]))
                    for d in c.get("derived_from", []):
                        addd(d)
    for f in os.listdir(os.path.join(out_dir, "relations")):
        for l in open(os.path.join(out_dir, "relations", f), encoding="utf-8"):
            e = json.loads(l)
            for p in e["provenance"]:
                seen.add((p["file"], p["path"]))
            for c in e["attrs"].values():
                for p in c.get("prov", []):
                    seen.add((p["file"], p["path"]))
    for c in S.conflicts:
        for v in c["values"]:
            if v.get("source_file"):
                seen.add((v["source_file"], v["source_path"]))
        for x in c.get("context", []):
            addd(x["locator"])
    for d in S.ctx["dic"]["dictionaries"]:
        for e in d["entries"]:
            for s_ in e.get("sources", []) + [s for sy in e.get("synonyms", []) for s in sy.get("sources", [])]:
                if "file" in s_:
                    seen.add((s_["file"], s_["path"]))
    cm = S.ctx["cmap"]
    keys = [k for k, v in cm.items() if v["dest"] not in ("브론즈", "버림")]
    miss = [(k, cm[k]["target"]) for k in keys if k not in seen]
    return len(keys), miss


REL_NOTE = {"R23": "conflict → target(target_id 있는 것만)", "R24": "결정(approved) → 대상", "R25": "레코드 × 원장 파일(값 단위 provenance 는 레코드의 provenance[])", "R30": "결정 edge_create 로만 — 1차 0",
            "R27": "튜플 → what", "R28": "튜플 → site(none 제외)", "R31": "부작용 → site · 상대 부위(사전 값)"}
HOLD = [
    "참조 구현 `erd-v3.1-tuples.py` 는 `erd-v3-tuples.py`(→ v2.4 → … · `erd-v1.1-resolve.py`)를 import 한다 — 분해를 옮기려고 그 사슬을 읽었다(이전 실버 설계·값은 읽지 않았다). summary 의 v3 대조 키(adverse.v3_comparison · 수식어 표 v3_unregistered)는 `erd-v3-tuples.json` 을 함께 읽어 같은 값을 만든다(--tuples-prev) · v24_reference_changes 는 참조 구현과 같이 빈 목록.",
    "same_session_order(treatment-sequence) — ERD 는 modality·modality_subcategory 속성으로만 적었는데 라벨 참조가 시술 튜플로 풀린 3 건(IPL·프락셔널·혈관 @M8)은 그 procedure 레코드의 같은 이름 속성으로 두었다.",
    "R19 출처 — extracted.json {code}.source(교과서) 는 modality → citation, step1 근거 URL 은 product → citation 으로 이었다(ERD R19 from 은 evidence_statement·clinical_rule 만 적음 · 컬럼 표 비고 「→ R19」를 따름). 문헌 adverse_effects 의 인용은 문구 사전 항목 citations[](v3.1).",
    "R15 엣지 레코드 — complications 이름 유래는 이름마다(엣지 속성 severity·incidence… 가 이름의 것이라) · 문구 유래는 (출발, 단위) 마다 하나(source_phrases 부록 · course = 그 단위 후보의 경과 합). 참조 구현의 (출발, 단위) distinct 수는 §14 에 함께 적는다.",
    "clinical_rule 식별자 — ERD §2.18 「kind + 정규화 문장」대로 정규화(norm_v1) 문장으로 계산한다(5차까지는 원문 그대로 해시 — RUL- 값이 바뀐다 · 결정이 RUL- 를 가리키지 않아 영향 없음).",
    "dictionary_add 의 new_value 모양(canonical, synonyms, category)에 product_name 의 계열 code 자리가 없다 — 제안 파일은 new_value.code 를 더했다(승인 때 확인).",
    "⑦ 「procedure-profiles mechanism · 제조사 · purpose_label 유사값 4쌍 = 6」 중 purpose_label 4쌍은 ERD 가 쌍을 적지 않아 만들지 않았다(유사도 판정 금지). regenerative/regeneration(질문 21)과 클래시스/클래시스(Classys)(§3.10 규칙에 걸림)만 레코드.",
    "conflict.stable_key — ⑧ unregistered_value 는 같은 원장 위치(locator)에 미등록 조각이 여럿이라 {kind, locators} 만으로는 겹친다 → ⑧ 에 한해 stable_key.value(조각)를 더했다. 같은 kind·같은 출처 쌍이 두 규칙에 걸리면(pih 괄호 보충 ⑦ = §3.10 표면형 ⑦) 레코드 하나로 합치고 also 에 둘째 규칙을 남겼다.",
    "④ 자동 해결은 같은 사실에 순위가 다른 출처가 있을 때만 생긴다 — 순위가 갈리는 자리는 products.json mfds(2) vs taxonomy mfds(3)와 step1 허가 값(licenses[].source 가 식약처 API 면 2) vs 다른 출처(3)뿐이고, 1차에서 값이 다른 것은 step1 1 건이다(mfds 는 두 출처 값이 다른 제품 0).",
]


def second_build_section(S, out_dir, baseline_path, m):
    """「2차 빌드 · 결정 묶음 1 적용」 — 1차(결정 묶음 1 전) manifest 와 수치 대조.
    3차 이후에는 2차 수치를 `baseline/manifest-2차.json`(결정 묶음 2A 전 2차 빌드 manifest)에서 읽는다."""
    if not baseline_path or not os.path.exists(baseline_path):
        return
    b = json.load(open(baseline_path, encoding="utf-8"))["counts"]
    p2 = os.path.join(os.path.dirname(baseline_path), "manifest-2차.json")
    m2 = json.load(open(p2, encoding="utf-8")) if os.path.exists(p2) and any(d["id"].startswith("DEC-2026-11-04-B2A") for d in S.ctx["decisions_approved"]) else m
    c = m2["counts"]
    applied = [x for x in m2["decisions"]["apply_log"] if x.get("result") == "applied" and x["id"].startswith("DEC-2026-11-04-B1")]
    o = ["", "## 10. 2차 빌드 · 결정 묶음 1 적용", "",
         f"1차 = 결정 묶음 1 적용 전(`baseline/manifest-1차.json` · 같은 빌더로 `decisions/batch1/` 없이 빌드) · 2차 = `decisions/batch1/` approved {len(applied)} 건 적용(① dictionary_add — 제품 "
         f"{sum(1 for x in applied if '-PRD-' in x['id'])} · 동의어 {sum(1 for x in applied if '-SYN-' in x['id'])}). ③ ERD 실측 대조는 결정 전 분해 기준이라 그대로 차이 0.", ""]

    def tbl(title, k1, k2=None):
        keys = sorted(set(b[k1]) | set(c[k1]), key=lambda x: (len(x), x) if k1 == "relations" else x)
        rows = [(k, b[k1].get(k, 0), c[k1].get(k, 0), c[k1].get(k, 0) - b[k1].get(k, 0)) for k in keys]
        o.extend([f"### {title}", "", md_table(["", "1차", "2차", "변화"], [(r[0], r[1], r[2], f"{r[3]:+d}" if r[3] else "0") for r in rows]), ""])
    tbl("개체", "entities")
    tbl("관계", "relations")
    gk = ["unresolved_references", "unregistered_fragments", "unlinked_expressions", "catalog_partial"]
    o.extend(["### 게이트 4종", "", md_table(["", "1차", "2차", "변화"], [(k, b["gate"][k], c["gate"][k], f"{c['gate'][k] - b['gate'][k]:+d}") for k in gk]), ""])
    tbl("충돌 kind 별", "conflicts")
    gone = sorted(set(b["product_ids"]) - set(c["product_ids"]))
    new = sorted(set(c["product_ids"]) - set(b["product_ids"]))
    pb, pc = b["procedure_by_origin_what"], c["procedure_by_origin_what"]
    def grp(d, pred):
        return sum(v for k, v in d.items() if pred(k))
    ref_d = grp(pc, lambda k: k.split(":")[0] == "reference") - grp(pb, lambda k: k.split(":")[0] == "reference")
    mk_d = grp(pc, lambda k: k.split(":")[0] == "market_pricing") - grp(pb, lambda k: k.split(":")[0] == "market_pricing")
    cat_b, cat_c = grp(pb, lambda k: "catalog_item" in k.split(":")[0]), grp(pc, lambda k: "catalog_item" in k.split(":")[0])
    selfb, selfc = grp(pb, lambda k: k.endswith(":catalog_item")), grp(pc, lambda k: k.endswith(":catalog_item"))
    o.append(f"- **제품 {b['entities']['product']}→{c['entities']['product']}**: 제품 사전에 들어간 step1 이름으로 B 규칙 대응이 바뀌어, 따로 있던 survey 레코드 {len(gone)} 개가 사전 제품 레코드로 합쳐졌다(새 id {len(new)} · origin {b['product_origin']} → {c['product_origin']}).")
    o.append(f"- **시술 {b['entities']['procedure']}→{c['entities']['procedure']}**: 1차 미해결이던 참조·시장가 이름이 새 사전 값(제품·HIFU/RF 등 동의어)으로 풀려 튜플이 됐다 — 참조 자리 튜플 {ref_d:+d} · 시장가 튜플 {mk_d:+d}. 분류 항목 튜플은 {cat_b}→{cat_c}(항목 자신이 what 인 튜플 {selfb}→{selfc}, 나머지는 what 이 제품 등 사전 값으로 바뀌었지만 anchor 가 남아 항목마다 하나 — 수는 그대로).")
    with open(os.path.join(out_dir, "report.md"), "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(o) + "\n")


def third_build_section(S, out_dir, baseline_dir, m):
    """「3차 빌드 · 결정 묶음 2A」 — 2차(baseline/manifest-2차.json) 대비 수치."""
    p2 = os.path.join(baseline_dir, "manifest-2차.json")
    if not os.path.exists(p2):
        return
    b = json.load(open(p2, encoding="utf-8"))["counts"]
    p3 = os.path.join(baseline_dir, "manifest-3차.json")
    if os.path.exists(p3) and any(d["id"].startswith("DEC-2026-11-04-B2B") for d in S.ctx["decisions_approved"]):
        m = json.load(open(p3, encoding="utf-8"))  # 4차 이후 — 3차 수치는 저장해 둔 3차 manifest 에서
    c = m["counts"]
    logs = [x for x in m["decisions"]["apply_log"] if x["id"].startswith("DEC-2026-11-04-B2A")]
    o = ["", "## 11. 3차 빌드 · 결정 묶음 2A", "",
         f"2차 = `baseline/manifest-2차.json`(결정 묶음 1 까지) · 3차 = `decisions/batch2a/` approved {len(logs)} 건(사용자 2026-11-04 「진행」 — 코디 추천 매핑). "
         "① dictionary_add 7(조각 → 계열·하위분류 동의어) · ② canonical_mapping 1(「HA」 — 계열 힌트 M2 참조 자리에서만). ③ ERD 실측 대조는 결정 전 분해 기준이라 그대로 차이 0.", "",
         "### 결정별 적용", "",
         md_table(["결정", "kind", "단계", "결과", "내용"], [(x["id"], x["kind"], x["stage"], x["result"],
                   (f"{x.get('dictionary')} += {', '.join(x.get('added', []))}" if x["kind"] == "dictionary_add" else f"scope anchor {len(x.get('anchors', []))} 중 튜플로 풀림 {len(x.get('resolved_anchors', []))}")) for x in logs]), ""]

    def tbl(title, k1):
        keys = sorted(set(b[k1]) | set(c[k1]), key=lambda x: (len(x), x) if k1 == "relations" else x)
        rows = [(k, b[k1].get(k, 0), c[k1].get(k, 0), c[k1].get(k, 0) - b[k1].get(k, 0)) for k in keys]
        o.extend([f"### {title}", "", md_table(["", "2차", "3차", "변화"], [(r[0], r[1], r[2], f"{r[3]:+d}" if r[3] else "0") for r in rows]), ""])
    gk = ["unresolved_references", "unregistered_fragments", "unlinked_expressions", "catalog_partial"]
    o.extend(["### 게이트 4종", "", md_table(["", "2차", "3차", "변화"], [(k, b["gate"][k], c["gate"][k], f"{c['gate'][k] - b['gate'][k]:+d}") for k in gk]), ""])
    tbl("충돌 kind 별", "conflicts")
    tbl("개체", "entities")
    tbl("관계", "relations")
    pb, pc = b["procedure_by_origin_what"], c["procedure_by_origin_what"]
    def grp(d, pred):
        return sum(v for k, v in d.items() if pred(k))
    ref_d = grp(pc, lambda k: k.split(":")[0] == "reference") - grp(pb, lambda k: k.split(":")[0] == "reference")
    mk_d = grp(pc, lambda k: k.split(":")[0] == "market_pricing") - grp(pb, lambda k: k.split(":")[0] == "market_pricing")
    o.append(f"- **시술 {b['entities']['procedure']}→{c['entities']['procedure']}**: 2차 미해결이던 참조·시장가 이름이 새 동의어(크라이오·수액·줄기세포 → 계열 · 혈관레이저·다이오드 → M8 하위분류 · CO2·Nd:YAG → M8 계열)와 「HA」(힌트 M2 자리)로 풀려 튜플이 됐다 — 참조 자리 튜플 {ref_d:+d} · 시장가 튜플 {mk_d:+d}. 분류 항목 튜플은 그대로.")
    o.append("- **「HA」 → M2 계열(하위분류 미지정)**: 원장 M2 하위분류에 「HA 필러」 라벨이 없다 — 「국산 HA」(M2-1)·「수입 HA」(M2-2) 둘이라 「HA」 하나로는 가를 근거가 없어 계열 M2 로 읽었다. 계열 힌트 M4 인 참조 자리는 0 이라 M4 「HA (물광)」 결정은 만들지 않았다. 힌트 없는 참조 5 개(원장 자리 8)는 결정 없음(미해결 유지).")
    o.append("- 조각이 풀렸어도 같은 이름에 다른 미등록 조각(「810nm」「볼륨」「프랙셔널」 등)이 남은 참조는 그대로 미해결이다 — 조각 수 감소와 미해결 참조 수 감소가 같지 않다.")
    with open(os.path.join(out_dir, "report.md"), "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(o) + "\n")


def fourth_build_section(S, out_dir, baseline_dir, m):
    """「4차 빌드 · 브론즈 2판 + 결정 묶음 2B」 — 3차(baseline/manifest-3차.json) 대비.
    5차 이후에는 4차 빌드가 쓴 절을 그대로 붙인다(baseline/report-12-4차.md · 4차 기록 보존)."""
    frozen = os.path.join(baseline_dir, "report-12-4차.md")
    if os.path.exists(frozen) and any(d["id"].startswith("DEC-2026-11-05-B3") for d in S.ctx["decisions_approved"]):
        with open(frozen, encoding="utf-8") as f:
            txt = f.read()
        with open(os.path.join(out_dir, "report.md"), "a", encoding="utf-8", newline="\n") as f:
            f.write("\n" + txt.rstrip("\n") + "\n")
        return
    p3 = os.path.join(baseline_dir, "manifest-3차.json")
    if not os.path.exists(p3):
        return
    from .provenance import parse_loc, resolve
    b = json.load(open(p3, encoding="utf-8"))["counts"]
    c = m["counts"]
    logs = [x for x in m["decisions"]["apply_log"] if x["id"].startswith("DEC-2026-11-04-B2B")]
    res = Counter(x["result"] for x in logs)
    bz = S.ctx.get("bronze")
    o = ["", "## 12. 4차 빌드 · 브론즈 2판 + 결정 묶음 2B", "",
         f"3차 = `baseline/manifest-3차.json`(브론즈 1판 · 결정 묶음 2A 까지) · 4차 = 원장 {(bz['label'] + '(HASHES.txt 검증 · manifest `bronze_version`)') if bz else '1판(ERD 해시)'} + `decisions/batch2b/` approved {len(logs)} 건(사용자 게이트 답 2026-11-05).", "",
         "### 결정 묶음 2B 적용", "",
         md_table(["결과", "건"], sorted(res.items())), "",
         md_table(["kind", "applied", "recorded", "rejected", "no_target"], [(k, *(sum(1 for x in logs if x["kind"] == k and x["result"] == r) for r in ("applied", "recorded", "rejected", "no_target"))) for k in sorted({x["kind"] for x in logs})]), ""]
    bad = [x for x in logs if x["result"] in ("rejected", "no_target")]
    if bad:
        o += ["거부·대상 없음:", ""] + [f"- `{x['id']}` {x['kind']} — {x['result']}: {x.get('why')}" for x in bad] + [""]
    na = os.path.join(S.ctx["args"].decisions, "batch2b-answers", "_not_applied.json")
    if os.path.exists(na):
        nd = json.load(open(na, encoding="utf-8"))
        o += ["결정을 만들지 않은 답(원장 2판으로 해소):", ""] + [f"- `{k}` = {v['choice']} — {v['why']}" for k, v in sorted(nd.items())] + [""]
    # 브론즈 2판으로 이름이 바뀐 3차 미해결 참조
    pu = os.path.join(baseline_dir, "unresolved_references-3차.json")
    if os.path.exists(pu):
        old = json.load(open(pu, encoding="utf-8"))
        cur = {r["ref_id"] for r in S.ctx.get("unres_rows", [])} if S.ctx.get("unres_rows") else None
        curlab = {}
        for cf in S.conflicts:
            if cf["kind"] == "unresolved_reference" and cf.get("ref_id"):
                curlab.setdefault(cf["ref_id"], cf.get("label"))
        changed = []
        for r in old:
            if r["ref_id"] in curlab:
                continue
            news = []
            for lc in r["locators"]:
                p = parse_loc(lc)
                try:
                    v = resolve(S.ctx["L"][p["file"]], p["path"], p["rec"])
                except Exception:  # noqa: BLE001
                    v = None
                if isinstance(v, str) and v != r["label"]:
                    news.append(v)
            if news:
                nl = sorted(set(news))
                still = [rid for rid, lab in curlab.items() if lab in nl]
                changed.append((r["ref_id"], r["label"], " · ".join(nl), "미해결(⑨) " + ", ".join(sorted(set(still))) if still else "해결"))
        changed = sorted(set(changed))
        n_res = sum(1 for x in changed if x[3] == "해결")
        o += ["### 브론즈 2판으로 바뀐 참조", "",
              f"3차 미해결 참조 중 2판에서 원장 이름이 바뀐 것 {len(changed)} — 그중 해결 {n_res} · 새 이름으로도 미해결 {len(changed) - n_res}.", "",
              md_table(["3차 anchor", "1판 이름", "2판 이름", "4차"], changed), ""]
        if changed and n_res < len(changed):
            o.append("- `+` 로 바뀐 이름은 §1.4 조합 규칙상 primary 를 가진 멤버가 하나뿐이라(「보톡스 이마」+「미간」) 조합이 아니라 부위 둘(multi_site) → 여전히 ⑨. 1판 anchor 를 가리키던 per_site 답 3(slash 03·08·12)은 anchor 가 없어 결정을 만들지 않았다 — 새 anchor 에 다시 정하려면 tuple_assign_multi 를 미해결 참조에 적용하는 빌더 보강이 먼저다.")
            o.append("")

    def tbl(title, k1):
        keys = sorted(set(b[k1]) | set(c[k1]), key=lambda x: (len(x), x) if k1 == "relations" else x)
        rows = [(k, b[k1].get(k, 0), c[k1].get(k, 0), c[k1].get(k, 0) - b[k1].get(k, 0)) for k in keys]
        o.extend([f"### {title}", "", md_table(["", "3차", "4차", "변화"], [(r[0], r[1], r[2], f"{r[3]:+d}" if r[3] else "0") for r in rows]), ""])
    gk = ["unresolved_references", "unregistered_fragments", "unlinked_expressions", "catalog_partial"]
    o.extend(["### 게이트 4종", "", md_table(["", "3차", "4차", "변화"], [(k, b["gate"][k], c["gate"][k], f"{c['gate'][k] - b['gate'][k]:+d}") for k in gk]), ""])
    tbl("충돌 kind 별", "conflicts")
    tbl("개체", "entities")
    tbl("관계", "relations")
    with open(os.path.join(out_dir, "report.md"), "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(o) + "\n")


def fifth_build_section(S, out_dir, baseline_dir, m):
    """「5차 빌드 · ERD v3 + 묶음 3」 — 6차(ERD v3.1)부터는 5차 빌드가 쓴 절을 그대로 붙인다(baseline/report-13-5차.md · 5차 기록 보존)."""
    frozen = os.path.join(baseline_dir, "report-13-5차.md")
    if os.path.exists(frozen) and S.ctx["erd"].get("erd_version") != "v3":
        with open(frozen, encoding="utf-8") as f:
            txt = f.read()
        with open(os.path.join(out_dir, "report.md"), "a", encoding="utf-8", newline="\n") as f:
            f.write("\n" + txt.rstrip("\n") + "\n")
        return
    from .report5 import fifth
    fifth(S, out_dir, baseline_dir, m)


def sixth_build_section(S, out_dir, baseline_dir, m, g4=None):
    """「6차 빌드 · ERD v3.1」 — 7차(ERD v3.2)부터는 6차 빌드가 쓴 절을 그대로 붙인다(baseline/report-14-6차.md · 6차 기록 보존)."""
    frozen = os.path.join(baseline_dir, "report-14-6차.md")
    if os.path.exists(frozen) and S.ctx["erd"].get("erd_version") != "v3.1":
        with open(frozen, encoding="utf-8") as f:
            txt = f.read()
        with open(os.path.join(out_dir, "report.md"), "a", encoding="utf-8", newline="\n") as f:
            f.write("\n" + txt.rstrip("\n") + "\n")
        return
    from .report6 import sixth
    sixth(S, out_dir, baseline_dir, m, g4)


def seventh_build_section(S, out_dir, baseline_dir, m, g5=None):
    from .report7 import seventh
    seventh(S, out_dir, baseline_dir, m, g5)
