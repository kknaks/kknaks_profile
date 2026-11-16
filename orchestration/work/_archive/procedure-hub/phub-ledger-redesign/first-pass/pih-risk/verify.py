#!/usr/bin/env python3
"""pih-risk.json 1차 조사 독립 검증. 표준 라이브러리만 쓴다. 아무 파일도 쓰지 않는다.

실행 (레포 루트):
  python3 orchestration/work/phub-ledger-redesign/first-pass/pih-risk/verify.py
선택: --results <폴더>  결과 폴더를 다른 위치(변이 시험용 복사본)로 지정
실패가 하나라도 있으면 exit 1.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SRC = REPO / "orchestration/work/phub-recommend/bronze/phub-ledger/pih-risk.json"
EXPECTED_SHA = "cb6e9305113d0b47f447eb314ce3bb34d0278bbc8bdf26bc3303d323028575c8"
RES = Path(sys.argv[sys.argv.index("--results") + 1]).resolve() if "--results" in sys.argv else HERE

fails = []
checks = {}


def check(name, ok, detail=""):
    checks[name] = checks.get(name, 0) + 1
    if not ok:
        fails.append(f"{name}: {detail}")


def esc(k):
    return k.replace("~", "~0").replace("/", "~1")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


start_sha = sha(SRC)
check("source_sha_start", start_sha == EXPECTED_SHA, start_sha)
raw = SRC.read_bytes()
text = raw.decode("utf-8")

# ---- 독립 재파싱: 중복 키를 잡는 hook 으로 Pointer 를 순서대로 다시 만든다
dups = []


class Obj(list):
    """객체를 (키, 값) 쌍 리스트로 보존 — 빈 객체와 빈 배열을 구분한다."""


def hook(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            dups.append(k)
        seen.add(k)
    return Obj(pairs)


tree = json.loads(text, object_pairs_hook=hook)
indep = []  # (pointer, type, value)


def walk(v, p):
    if isinstance(v, list) and not isinstance(v, Obj):
        indep.append((p, "array", None))
        for i, x in enumerate(v):
            walk(x, f"{p}/{i}")
    elif isinstance(v, Obj):
        indep.append((p, "object", None))
        for k, x in v:
            walk(x, f"{p}/{esc(k)}")
    else:
        t = "null" if v is None else "boolean" if isinstance(v, bool) else "number" if isinstance(v, (int, float)) else "string"
        indep.append((p, t, v))


walk(tree, "")
doc = json.loads(text)
check("no_duplicate_keys", not dups, dups)


def load(name):
    p = RES / name
    check(f"exists:{name}", p.exists(), str(p))
    return json.loads(p.read_text()) if p.exists() and name.endswith(".json") else (p.read_text() if p.exists() else None)


sm = load("source-map.json")
mo = load("morphology.json")
ex = load("expressions.json")
cov = load("coverage.json")
for f in ["review.md", "issues.md", "validation.md", "progress.md", "build.py", "segments.json"]:
    check(f"exists:{f}", (RES / f).exists(), f)

check("sourcemap_sha", sm["source"]["sha256"] == EXPECTED_SHA)
check("sourcemap_bytes", sm["source"]["bytes"] == len(raw))
check("sourcemap_escapes", sm["source"]["backslash_escapes"] == text.count("\\"))

# ---- 양방향 대조 (순서 포함)
nodes = sm["nodes"]
sm_ptrs = [n["pointer"] for n in nodes]
ind_ptrs = [p for p, _, _ in indep]
check("pointer_set_equal", set(sm_ptrs) == set(ind_ptrs), f"missing={set(ind_ptrs)-set(sm_ptrs)} extra={set(sm_ptrs)-set(ind_ptrs)}")
check("pointer_order_equal", sm_ptrs == ind_ptrs, "order differs")
check("pointer_unique", len(sm_ptrs) == len(set(sm_ptrs)))
byp = {n["pointer"]: n for n in nodes}
for p, t, v in indep:
    n = byp.get(p)
    if not n:
        continue
    check("type_match", n["type"] == t, p)
    if t not in ("object", "array"):
        check("value_match", n.get("value") == v, p)


def get(ptr):
    cur = doc
    for part in ptr.split("/")[1:] if ptr else []:
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


b = [0]
for ch in text:
    b.append(b[-1] + len(ch.encode("utf-8")))
for n in nodes:
    s, e = n["cp"]
    check("cp_reparse", json.loads(text[s:e]) == get(n["pointer"]), n["pointer"])
    check("byte_cp_agree", n["byte"] == [b[s], b[e]] and raw[b[s]:b[e]].decode() == text[s:e], n["pointer"])
    if n["type"] == "string":
        vs, ve = n["value_cp"]
        check("value_cp_text", text[vs:ve] == n["value"], n["pointer"])
        check("raw_literal", text[s:e] == n["raw_literal"], n["pointer"])
    if "member_key" in n:
        ks, ke = n["member_key"]["cp"]
        check("member_key_text", json.loads(text[ks:ke]) == n["key_or_index"], n["pointer"])
    if n["type"] in ("object", "array"):
        check("child_count", n["child_count"] == len(get(n["pointer"])), n["pointer"])
        check("leaf_flag", n["leaf"] == (n["child_count"] == 0), n["pointer"])
    else:
        check("leaf_flag", n["leaf"] is True, n["pointer"])

# 키 출현
ind_keys = []


def walkk(v, p):
    if isinstance(v, Obj):
        for k, x in v:
            ind_keys.append(f"{p}/{esc(k)}")
            walkk(x, f"{p}/{esc(k)}")
    elif isinstance(v, list):
        for i, x in enumerate(v):
            walkk(x, f"{p}/{i}")


walkk(tree, "")
check("key_occurrences_equal", [k["member_pointer"] for k in sm["keys"]] == ind_keys)
for k in sm["keys"]:
    s, e = k["cp"]
    check("key_cp_text", json.loads(text[s:e]) == k["key"] and text[k["name_cp"][0]:k["name_cp"][1]] == k["key"], k["member_pointer"])

# ---- coverage: 소유 합집합 ↔ 전체 (양방향, 중복 금지)
all_nodes = set(sm_ptrs)
all_leaves = {n["pointer"] for n in nodes if n["leaf"]}
check("cov_all_leaf_list", set(cov["all_leaf_pointers"]) == all_leaves)
check("cov_all_node_list", set(cov["all_node_pointers"]) == all_nodes)
owned = []
owned_leaf = []
owned_keys = []
segplan = json.loads((RES / "segments.json").read_text())["segments"]
check("cov_segments_match_plan", [s["id"] for s in cov["segments"]] == [s["id"] for s in segplan])
for s in cov["segments"]:
    owned += s["owned_nodes"]
    owned_leaf += s["owned_leaf_pointers"]
    owned_keys += s["owned_key_occurrences"]
    check("seg_direct_read", s["direct_read"] is True and s["read_status"] == "read", s["id"])
    check("seg_last_read_pointer", s["last_read_pointer"] in s["owned_nodes"], s["id"])
    rf = RES / s["review_file"]
    check("seg_review_exists", rf.exists(), s["review_file"])
    mf = RES / "manual" / f"{s['id']}.json"
    check("seg_manual_exists", mf.exists(), str(mf))
    # 소유 여부를 계획(prefix)으로 독립 재판정
    for p in s["owned_nodes"]:
        ok = p in s["owns_exact"] or any(p == x or p.startswith(x + "/") for x in s["pointer_prefixes"])
        check("seg_owner_by_plan", ok, f"{s['id']} {p}")
    # 구획 파일에 모든 소유 값이 원문 그대로 실렸는지
    if rf.exists():
        body = rf.read_text()
        for p in s["owned_nodes"]:
            n = byp[p]
            row = next((ln for ln in body.splitlines() if ln.startswith(f"| `{p or '(root)'}` |")), None)
            check("review_row_present", row is not None, f"{s['id']} {p}")
            if row and "value" in n:
                lit = json.dumps(n["value"], ensure_ascii=False).replace("|", "\\|")
                check("review_value_literal", f"| {lit} |" in row, p)
check("cov_owned_nodes_union", set(owned) == all_nodes, f"missing={all_nodes-set(owned)} extra={set(owned)-all_nodes}")
check("cov_owned_nodes_no_dup", len(owned) == len(set(owned)), "duplicate ownership")
check("cov_owned_leaf_union", set(owned_leaf) == all_leaves and len(owned_leaf) == len(set(owned_leaf)))
check("cov_owned_keys_union", sorted(owned_keys) == sorted(ind_keys))
rv = (RES / "review.md").read_text()
for s in cov["segments"]:
    check("review_toc_link", f"(./{s['review_file']})" in rv, s["review_file"])

# ---- 형태소: 적용/제외 대응
recs = mo["records"]
vrec = [r for r in recs if r["role"] == "value"]
krec = [r for r in recs if r["role"] == "field_name"]
check("morph_value_cover", [r["pointer"] for r in vrec] == [n["pointer"] for n in nodes if n["leaf"]], "value records ≠ leaves")
check("morph_key_cover", [r["member_pointer"] for r in krec] == ind_keys)
check("morph_record_ids_unique", len({r["record_id"] for r in recs}) == len(recs))
EXCL_V = [r"^/version$", r"^/updated$", r"^/procedures/\d+/category$", r"^/procedures/\d+/procedure_ref$", r"^/procedures/\d+/pih_risk$"]
EXCL_K = [r"^/notes/[^/]+$", r"^/risk_levels/[^/]+$"]
for r in vrec:
    n = byp[r["pointer"]]
    if n["type"] == "string":
        check("morph_text", r["text"] == n["value"], r["pointer"])
        should_ex = any(re.search(x, r["pointer"]) for x in EXCL_V)
        check("morph_policy_value", r["applied"] != should_ex, r["pointer"])
    else:
        check("morph_nonstring_excluded", not r["applied"], r["pointer"])
for r in krec:
    should_ex = any(re.search(x, r["member_pointer"]) for x in EXCL_K)
    check("morph_policy_key", r["applied"] != should_ex, r["member_pointer"])
for r in recs:
    if r["applied"]:
        check("morph_tokens_nonempty", len(r["tokens"]) > 0, r.get("pointer", r.get("member_pointer")))
        last = 0
        for t in r["tokens"]:
            ok = 0 <= t["start"] <= t["end"] <= len(r["text"]) and t["surface"] == r["text"][t["start"]:t["end"]] and t["start"] >= last
            check("morph_token_span", ok, f"{r['record_id']} {t}")
            last = t["start"]
        # 토큰이 덮지 않은 비공백 문자 0
        covered = set()
        for t in r["tokens"]:
            covered.update(range(t["start"], t["end"]))
        gaps = [i for i, c in enumerate(r["text"]) if not c.isspace() and i not in covered]
        check("morph_no_uncovered_chars", not gaps, f"{r['record_id']} {gaps}")
    else:
        check("morph_exclusion_reason", bool(r.get("exclusion", {}).get("reason")), r["record_id"])
check("morph_counts", mo["counts"]["records"] == len(recs) and mo["counts"]["tokens"] == sum(len(r.get("tokens", [])) for r in recs))
an = mo["analyzer"]
check("morph_analyzer_recorded", an["name"] == "kiwipiepy" and an["version"] == "0.24.1" and an["model_type"] == "cong" and an["num_workers"] == 1)

# 오분절 기록
for o in mo["segmentation_review"]["occurrences"]:
    v = byp[o["pointer"]]["value"]
    check("segrev_text", v[o["span"][0]:o["span"][1]] == o["text"], o)
    check("segrev_file_cp", text[o["file_cp"][0]:o["file_cp"][1]] == o["text"], o)
    check("segrev_status", o["status"] in ("K", "A"), o)
    check("segrev_owner", byp[o["pointer"]]["segment"] == o["segment"], o)

# ---- 표현
voc = set(ex["facet_vocabulary"])
seen = set()
for e in ex["expressions"]:
    n = byp[e["pointer"]]
    v = n["value"]
    s, t = e["span_in_value"]
    check("expr_text", v[s:t] == e["text"], e["expr_id"])
    check("expr_file_cp", text[e["file_cp"][0]:e["file_cp"][1]] == e["text"], e["expr_id"])
    check("expr_file_byte", raw[e["file_byte"][0]:e["file_byte"][1]].decode() == e["text"], e["expr_id"])
    check("expr_full_value", e["full_value"] == v, e["expr_id"])
    ss = e["sentence_span_in_value"]
    check("expr_sentence", ss is not None and ss[0] <= s and t <= ss[1] and e["sentence_text"] == v[ss[0]:ss[1]], e["expr_id"])
    check("expr_facets_vocab", e["facets"] and set(e["facets"]) <= voc, e["expr_id"])
    check("expr_status", e["status"] in ("P", "F", "B", "I", "K"), e["expr_id"])
    check("expr_segment", e["segment"] == n["segment"], e["expr_id"])
    key = (e["pointer"], s, t)
    check("expr_no_dup_span", key not in seen, f"{e['expr_id']} {key}")
    seen.add(key)
eids = {e["expr_id"] for e in ex["expressions"]}
for r in ex["regex_candidates"]:
    v = byp[r["pointer"]]["value"]
    check("regex_text", v[r["span_in_value"][0]:r["span_in_value"][1]] == r["text"], r["cand_id"])
    check("regex_cover_ids", set(r["covered_by_manual"]) <= eids, r["cand_id"])
    for c in r["covered_by_manual"]:
        e = next((x for x in ex["expressions"] if x["expr_id"] == c), None)
        if e is None:
            continue  # regex_cover_ids 가 이미 실패로 기록
        check("regex_cover_real", e["pointer"] == r["pointer"] and e["span_in_value"][0] <= r["span_in_value"][0] and r["span_in_value"][1] <= e["span_in_value"][1], r["cand_id"])
# 모든 언어 텍스트 값(분석 적용 문자열)에 수동 표현이 최소 1개 — 읽고 지나간 흔적
applied_ptrs = {r["pointer"] for r in vrec if r["applied"]}
noexpr = sorted(applied_ptrs - {e["pointer"] for e in ex["expressions"]})
allowed_noexpr = {p for p in applied_ptrs if re.search(r"/subcategory$", p)}
check("expr_every_text_value", set(noexpr) <= allowed_noexpr, noexpr)

# 읽기 검토 보조: 수식·조건·부정·가능성·비교 단서가 수동 표현 구간 밖에 남지 않았는지
# (단서 목록은 검토용 키워드일 뿐 의미 판정이 아니다 — validation.md §3)
CUES = re.compile(r"않|없|미만|이상|가능|드물|거의|약간|매우|가장|비교적|여전히|더욱|최소|가급적|대비|주의|우선|권장|고려|필요 시|사용 시|병합 시|깊이 시|화상 시|에서는|에서도|무관|비[박절선의자]|불충분|부적절|적합하지|등(?=\))|~|\+")
cue_total = 0
for n in nodes:
    if n["type"] != "string" or n["pointer"] not in applied_ptrs:
        continue
    for m in CUES.finditer(n["value"]):
        cue_total += 1
        ok = any(e["pointer"] == n["pointer"] and e["span_in_value"][0] <= m.start() and m.end() <= e["span_in_value"][1] for e in ex["expressions"])
        check("modifier_cue_covered", ok, f"{n['pointer']} '{m.group(0)}' @{m.start()}")

# 언어 텍스트 값의 내용 문자가 수동 표현 구간 밖에 남지 않았는지(구두점·공백·주제 조사 은/는 제외, subcategory 제외)
uncovered_vals = []
for n in nodes:
    if n["type"] != "string" or n["pointer"] not in applied_ptrs or n["pointer"].endswith("/subcategory"):
        continue
    covered_idx = set()
    for e in ex["expressions"]:
        if e["pointer"] == n["pointer"]:
            covered_idx.update(range(*e["span_in_value"]))
    left = "".join(c for i, c in enumerate(n["value"]) if i not in covered_idx and c not in " ,.()·")
    if left not in ("", "은", "는"):
        uncovered_vals.append((n["pointer"], left))
    check("expr_char_coverage", left in ("", "은", "는"), f"{n['pointer']} {left!r}")

# ---- issues.md 참조 대조
iss = (RES / "issues.md").read_text()
for s in cov["segments"]:
    m = json.loads((RES / "manual" / f"{s['id']}.json").read_text())
    for line in m.get("open", []):
        for ref in re.findall(r"issues\.md ([A-Z]\d+)", line):
            check("issue_ref_exists", re.search(rf"^### {ref}\b", iss, re.M) is not None, f"{s['id']} {ref}")

end_sha = sha(SRC)
check("source_sha_end", end_sha == start_sha)

summary = {"results_dir": str(RES), "source_sha_start": start_sha, "source_sha_end": end_sha,
           "nodes": len(nodes), "leaves": len(all_leaves), "key_occurrences": len(ind_keys),
           "morph_records": len(recs), "tokens": mo["counts"]["tokens"],
           "expressions": len(ex["expressions"]), "regex_candidates": len(ex["regex_candidates"]),
           "segmentation_occurrences": len(mo["segmentation_review"]["occurrences"]),
           "segments": len(cov["segments"]), "modifier_cues_checked": cue_total, "check_count": sum(checks.values()),
           "check_kinds": len(checks), "text_values_without_expr(subcategory only)": noexpr,
           "failure_count": len(fails), "failures": fails[:50]}
print(json.dumps(summary, ensure_ascii=False, indent=1))
sys.exit(1 if fails else 0)
