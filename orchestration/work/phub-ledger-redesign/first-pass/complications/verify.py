#!/usr/bin/env python3
"""complications.json 1차 조사 결과 독립 검증. 아무 파일도 쓰지 않는다. 실패가 있으면 종료 코드 1.

레포 루트에서:  python3 orchestration/work/phub-ledger-redesign/first-pass/complications/verify.py
변이 시험용:    --source <원본 사본> --dir <결과 폴더 사본>  (기록된 해시와 비교하는 검사는 그대로 돈다)

build.py 의 스캐너를 쓰지 않고 표준 json 파서(object_pairs_hook)로 원본을 다시 읽어 대조한다.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/complications.json"

ap = argparse.ArgumentParser()
ap.add_argument("--source", default=str(REPO / SRC_REL))
ap.add_argument("--dir", default=str(HERE))
args = ap.parse_args()
SRC, OUT = Path(args.source), Path(args.dir)

fails = []
checks = {}


def check(name, ok, detail=""):
    checks[name] = checks.get(name, 0) + 1
    if not ok:
        fails.append(f"{name}: {detail}")


raw = SRC.read_bytes()
h_start = hashlib.sha256(raw).hexdigest()
text = raw.decode("utf-8")

dups = []


def hook(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            dups.append(k)
        seen.add(k)
    return pairs  # 순서 보존 리스트


tree = json.loads(text, object_pairs_hook=hook)
check("no_duplicate_keys_in_source", not dups, dups)


def esc(k):
    return k.replace("~", "~0").replace("/", "~1")


expect = {}      # pointer -> (type, value)
key_order = {}   # object pointer -> [keys]
plain = json.loads(text)


def collect(x, ptr):
    if isinstance(x, dict):
        expect[ptr] = ("object", None)
        key_order[ptr] = list(x.keys())
        for k, v in x.items():
            collect(v, f"{ptr}/{esc(k)}")
    elif isinstance(x, list):
        expect[ptr] = ("array", None)
        for i, v in enumerate(x):
            collect(v, f"{ptr}/{i}")
    elif isinstance(x, str):
        expect[ptr] = ("string", x)
    elif isinstance(x, bool):
        expect[ptr] = ("boolean", x)
    elif x is None:
        expect[ptr] = ("null", None)
    else:
        expect[ptr] = ("number", x)


collect(plain, "")


def resolve(ptr):
    cur = plain
    if ptr == "":
        return cur
    for part in ptr.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def load(name):
    return json.loads((OUT / name).read_text())


sm = load("source-map.json")
mo = load("morphology.json")
ex = load("expressions.json")
ob = load("manual-observations.json")
review = (OUT / "review.md").read_text()

# ---------------- 원본 식별
for nm, d in (("source-map", sm), ("morphology", mo), ("expressions", ex)):
    s = d["source"]
    check("recorded_sha256_start", s["sha256_start"] == h_start, f"{nm} {s['sha256_start']} != {h_start}")
    check("recorded_sha256_end", s["sha256_end"] == h_start, f"{nm} {s['sha256_end']} != {h_start}")
    check("recorded_size", s["size_bytes"] == len(raw) and s["code_points"] == len(text), nm)
    check("recorded_path", s["path"] == SRC_REL, nm)

# ---------------- 노드 양방향 대응
nodes = sm["nodes"]
ptrs = [n["pointer"] for n in nodes]
check("node_pointer_unique", len(ptrs) == len(set(ptrs)), "duplicate pointers in source-map")
check("node_set_equal", set(ptrs) == set(expect),
      f"missing={sorted(set(expect) - set(ptrs))[:5]} extra={sorted(set(ptrs) - set(expect))[:5]}")
check("node_count", len(nodes) == len(expect), f"{len(nodes)} != {len(expect)}")
prev_start = -1
for n in nodes:
    p = n["pointer"]
    if p not in expect:
        continue
    t, v = expect[p]
    check("node_type", n["type"] == t, f"{p} {n['type']} != {t}")
    a, b = n["span"]
    lit = text[a:b]
    try:
        check("node_span_reproduces_value", json.loads(lit) == resolve(p), p)
    except Exception as e:
        check("node_span_reproduces_value", False, f"{p} {e}")
    check("node_span_order", a > prev_start or p == "", p)
    prev_start = a
    ba, bb = n["byte_span"]
    check("node_byte_span", raw[ba:bb].decode("utf-8") == lit, p)
    if t != "object" and t != "array":
        check("node_value", n["value"] == v and type(n["value"]) is type(v), p)
        check("node_literal", n["literal"] == lit, p)
    if t == "string":
        va, vb = n["value_span"]
        check("string_value_span", text[va:vb] == v and va == a + 1 and vb == b - 1, p)
        vba, vbb = n["value_byte_span"]
        check("string_value_byte_span", raw[vba:vbb].decode("utf-8") == v, p)
    if t == "object":
        check("object_children_order", n["children"] == key_order[p], p)
    if t in ("object", "array"):
        check("container_length", n["length"] == len(resolve(p)), p)

# ---------------- 키 출현
keys = sm["keys"]
exp_keys = [(op, k, i) for op, ks in key_order.items() for i, k in enumerate(ks)]
got_keys = [(k["object_pointer"], k["key"], k["order_in_object"]) for k in keys]
check("key_occurrences_equal", sorted(exp_keys) == sorted(got_keys) and len(got_keys) == len(set(got_keys)),
      f"{len(exp_keys)} vs {len(got_keys)}")
for k in keys:
    a, b = k["span"]
    check("key_span", text[a:b].startswith('"') and json.loads(text[a:b]) == k["key"], k["value_pointer"])
    check("key_byte_span", raw[k["byte_span"][0]:k["byte_span"][1]].decode() == text[a:b], k["value_pointer"])
    check("key_value_pointer", k["value_pointer"] == f"{k['object_pointer']}/{esc(k['key'])}", k["value_pointer"])
check("duplicate_keys_recorded_empty", sm["duplicate_keys"] == [], "source-map 이 중복 키를 기록함")
# field_name_occurrences
fno = sm["field_name_occurrences"]
for k in {k for _, k, _ in exp_keys}:
    occ = sorted(p for pats in fno.get(k, {}).values() for p in pats)
    exp_occ = sorted(f"{op}/{esc(kk)}" for op, kk, _ in exp_keys if kk == k)
    check("field_name_occurrences", occ == exp_occ, k)
check("field_name_set", set(fno) == {k for _, k, _ in exp_keys}, "field name set")

# ---------------- 형태소 적용·제외
strings = {p: v for p, (t, v) in expect.items() if t == "string"}
ana = mo["values"]
exc = mo["excluded_values"]
ap_ = [x["pointer"] for x in ana]
ep_ = [x["pointer"] for x in exc]
check("morph_no_dup", len(ap_) == len(set(ap_)) and len(ep_) == len(set(ep_)), "dup pointer")
check("morph_disjoint", not (set(ap_) & set(ep_)), sorted(set(ap_) & set(ep_))[:5])
check("morph_cover_all_strings", set(ap_) | set(ep_) == set(strings),
      f"missing={sorted(set(strings) - set(ap_) - set(ep_))[:5]}")
check("morph_no_non_string", all(expect[p][0] == "string" for p in ap_ + ep_), "non-string analyzed")
for x in exc:
    p = x["pointer"]
    check("excluded_value_matches", x["value"] == strings.get(p), p)
    check("excluded_reason_present", bool(x["reason"]), p)
    ok = (re.fullmatch(r"/categories/\d+/id", p) or re.fullmatch(r"/categories/\d+/complications/\d+/severity", p)
          or not re.search(r"[A-Za-z0-9가-힣]", x["value"])
          or (p.endswith("/evidence") and all(re.match(r"(https?://|[a-z0-9.-]+\.(com|org|net|gov)/)", s.strip())
                                              for s in x["value"].split(";") if s.strip())))
    check("excluded_reason_consistent", bool(ok), p)
for x in ana:
    p = x["pointer"]
    v = strings.get(p)
    check("analyzed_text_matches", x["text"] == v, p)
    fa, fb = x["file_span_of_text"]
    check("analyzed_file_span", text[fa:fb] == v, p)
    if re.fullmatch(r"/categories/\d+/(id|complications/\d+/severity)", p):
        check("code_not_analyzed", False, p)
    for s0, s1 in x["url_subspans"]:
        check("url_subspan_shape", re.match(r"(https?://|[a-z0-9.-]+\.(com|org|net|gov)/)", v[s0:s1]) is not None, p)
    last = -1
    for i, t in enumerate(x["tokens"]):
        a, b = t["span"]
        check("token_index", t["i"] == i, p)
        check("token_span_in_value", 0 <= a < b <= len(v) or (a == b and 0 <= a <= len(v)), f"{p} {t}")
        check("token_surface", v[a:b] == t["surface"], f"{p} {t}")
        check("token_form_flag", t["form_equals_surface"] == (t["form"] == t["surface"]), p)
        check("token_order", a >= last, f"{p} {t}")
        last = a
        check("token_has_tag_lemma", bool(t["tag"]) and t["lemma"] is not None, p)
    check("analyzed_has_tokens", len(x["tokens"]) > 0, p)
fn = {f["field_name"]: f for f in mo["field_names"]}
check("field_names_analyzed_all", set(fn) == {k for _, k, _ in exp_keys}, "field_names set")
for k, f in fn.items():
    check("field_name_count", f["occurrence_count"] == sum(1 for _, kk, _ in exp_keys if kk == k), k)
    for t in f["tokens"]:
        check("field_name_token_surface", k[t["span"][0]:t["span"][1]] == t["surface"], k)
an = mo["analyzer"]
check("analyzer_recorded", an["kiwipiepy"] == "0.24.1" and an["model_type"] == "cong" and an["num_workers"] == 1, an)

# ---------------- 오분절 표시
amap = {x["pointer"]: x for x in ana}
rules = {r["id"]: r for r in mo["segmentation_review_rules"]}
cnt = {}
for o in mo["segmentation_review"]:
    v = amap.get(o["pointer"])
    check("seg_pointer_analyzed", v is not None, o["id"])
    if not v:
        continue
    a, b = o["phrase_span"]
    check("seg_phrase", v["text"][a:b] == o["phrase"], o["id"])
    toks = [v["tokens"][i] for i in o["token_indexes"]]
    check("seg_raw_tokens", [[t["form"], t["tag"], t["span"]] for t in toks] == o["raw_tokens"], o["id"])
    r = rules.get(o["rule"])
    check("seg_rule_exists", r is not None, o["id"])
    if r:
        check("seg_rule_tokens", [[t[0], t[1]] for t in o["raw_tokens"]] == r["raw_tokens"], o["id"])
        check("seg_rule_phrase", r["phrase"] == o["phrase"], o["id"])
    check("seg_status_not_corrected", "교정 아님" in o["status"], o["id"])
    cnt[o["rule"]] = cnt.get(o["rule"], 0) + 1
for rid, r in rules.items():
    check("seg_rule_count", cnt.get(rid, 0) == r["occurrences_flagged"] and r["occurrences_flagged"] > 0, rid)
seg_ids = [o["id"] for o in mo["segmentation_review"]]
check("seg_id_unique", len(seg_ids) == len(set(seg_ids)), "dup seg id")

# ---------------- 표현
exprs = ex["expressions"]
ids = [e["id"] for e in exprs]
check("expr_ids_sequential", ids == [f"E{i:05d}" for i in range(len(exprs))], "ids")
sig = set()
for e in exprs:
    p = e["pointer"]
    v = strings.get(p)
    check("expr_pointer_string", v is not None, e["id"])
    if v is None:
        continue
    a, b = e["span"]
    check("expr_span_text", 0 <= a < b <= len(v) and v[a:b] == e["text"], e["id"])
    if e.get("keyword_span"):
        ka, kb = e["keyword_span"]
        check("expr_keyword_span", v[ka:kb] == e["keyword"] and a <= ka and kb <= b, e["id"])
    if e.get("clause_span"):
        ca, cb = e["clause_span"]
        check("expr_clause_contains", ca <= a and b <= cb <= len(v), e["id"])
    s = (p, a, b, e["category_candidate"], e["method"], e.get("keyword"), e.get("manual_id"))
    check("expr_no_exact_duplicate", s not in sig, e["id"])
    sig.add(s)
whole = {e["pointer"] for e in exprs if e["category_candidate"] == "segment.value"}
check("expr_every_string_has_value_segment", whole == set(strings), sorted(set(strings) - whole)[:5])
man = load("manual-expressions.json")["expressions"]
mids = {e["manual_id"] for e in exprs if e.get("manual_id")}
check("manual_expressions_all_placed", mids == {m["id"] for m in man}, "manual ids")
for e in exprs:
    for u in (amap.get(e["pointer"]) or {}).get("url_subspans", []):
        if e["category_candidate"] not in ("segment.value", "segment.sentence", "segment.clause", "segment.parenthetical") \
                and not e["category_candidate"].startswith("manual."):
            check("expr_not_inside_url", not (e["span"][0] < u[1] and u[0] < e["span"][1]), e["id"])

# ---------------- 관찰 근거
for o in ob["observations"]:
    for evd in o["evidence"]:
        p = evd["pointer"]
        check("obs_pointer_valid", p in expect, f"{o['id']} {p}")
        if evd.get("quote"):
            check("obs_quote_in_value", p in strings and evd["quote"] in strings[p], f"{o['id']} {p}")
    check("obs_in_review", f"**{o['id']}**" in review, o["id"])


# ---------------- review.md 전수 대응(원본 컬럼명·Pointer·원문 값이 같은 행)
def md(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


rows = [l for l in review.splitlines() if l.startswith("| `")]
rowset = set(rows)
for p, v in strings.items():
    field = p.split("/")[-1] if not p.split("/")[-1].isdigit() else f"{p.split('/')[-2]}[{p.split('/')[-1]}]"
    if p.startswith("/categories/") and p.count("/") == 3:  # 카테고리 id·name 은 제목줄
        check("review_category_heading", f"`{p.rsplit('/', 1)[0]}`" in review and md(v) in review, p)
        continue
    check("review_row_exact", f"| `{field}` | `{p}` | {md(v)} |" in rowset, p)
comps = [(ci, mi, c) for ci, cat in enumerate(plain["categories"]) for mi, c in enumerate(cat["complications"])]
for ci, mi, c in comps:
    base = f"/categories/{ci}/complications/{mi}"
    check("review_item_heading", f"#### `{base}`" in review, base)
    if not c["risk_factors"]:
        check("review_empty_array_row", f"| `risk_factors` | `{base}/risk_factors` | [] (빈 배열) |" in rowset, base)
n_absent = sum(1 for _, _, c in comps for f in ("duration", "evidence") if f not in c)
check("review_absent_key_rows", review.count("| — | (키 없음) |") == n_absent, f"{review.count('| — | (키 없음) |')} != {n_absent}")

h_end = hashlib.sha256(SRC.read_bytes()).hexdigest()
check("source_hash_unchanged_during_verify", h_end == h_start, h_end)

summary = {"source_sha256": h_start, "nodes": len(nodes), "keys": len(keys), "strings": len(strings),
           "analyzed": len(ana), "excluded": len(exc), "tokens": sum(len(x["tokens"]) for x in ana),
           "segmentation_flags": len(mo["segmentation_review"]), "expressions": len(exprs),
           "observations": len(ob["observations"]), "check_kinds": len(checks),
           "check_runs": sum(checks.values()), "failure_count": len(fails)}
print(json.dumps(summary, ensure_ascii=False, indent=1))
for f in fails[:50]:
    print("FAIL", f)
sys.exit(1 if fails else 0)
