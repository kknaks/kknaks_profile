"""procedure-comparison 1차 조사 산출물 독립 재검증.

build.py 코드를 쓰지 않고 원본과 출력 파일만 읽는다. 표준 라이브러리만 사용. 어떤 파일도 쓰지 않는다.
실행(레포 루트): python3 orchestration/work/phub-ledger-redesign/first-pass/procedure-comparison/verify.py
실패가 하나라도 있으면 종료 코드 1.
"""
import hashlib
import json
import os
import re
import sys

OUT = os.path.dirname(os.path.abspath(__file__))
SRC = "orchestration/work/phub-recommend/bronze/phub-ledger/procedure-comparison.json"
EXPECTED_SHA = "eba7ae5af919ef77ff52cb07b2f6117b458751319f530f38cf30c61e94989571"
if not os.path.exists(SRC):
    sys.exit(f"원본 없음 — 레포 루트에서 실행: {SRC}")
raw = open(SRC, "rb").read()
text = raw.decode("utf-8")
fails, counts = [], {}


def ok(cond, msg):
    if not cond:
        fails.append(msg)


def tick(name, n=1):
    counts[name] = counts.get(name, 0) + n


# 중복 키를 독립적으로 감지
dup_found = []


def hook(pairs):
    ks = [k for k, _ in pairs]
    if len(ks) != len(set(ks)):
        dup_found.append(ks)
    return dict(pairs)


data = json.loads(text, object_pairs_hook=hook)
ok(not dup_found, f"duplicate keys in source: {dup_found}")

load = lambda n: json.load(open(os.path.join(OUT, n), encoding="utf-8"))
sm, mo, ex = load("source-map.json"), load("morphology.json"), load("expressions.json")
seg = load("segmentation-review.json")
review = open(os.path.join(OUT, "review.md"), encoding="utf-8").read()

# 1. 해시
h = hashlib.sha256(raw).hexdigest()
ok(h == EXPECTED_SHA, f"source sha256 changed: {h}")
for name, d in (("source-map", sm), ("morphology", mo), ("expressions", ex)):
    ok(d["source"]["sha256_start"] == d["source"]["sha256_end"] == h, f"hash record {name}")
ok(sm["source"]["bytes"] == len(raw) and sm["source"]["code_points"] == len(text), "size record")
ok(sm["source"]["backslash_escapes"] == text.count("\\"), "escape count record")


def res(p):
    cur = data
    for part in p.split("/")[1:] if p else []:
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


# 2. 노드 → 원문
tmap = {dict: "object", list: "array", str: "string", bool: "boolean", int: "number", float: "number", type(None): "null"}
bytes_of = [0]
for ch in text:
    bytes_of.append(bytes_of[-1] + len(ch.encode("utf-8")))
for n in sm["nodes"]:
    try:
        v = res(n["pointer"])
    except Exception:
        fails.append("pointer unresolved " + n["pointer"])
        continue
    a, b = n["span"]
    lit = text[a:b]
    ok(tmap[type(v)] == n["type"], "type " + n["pointer"])
    ok(json.loads(lit) == v, "span reparse " + n["pointer"])
    ok(n["byte_span"] == [bytes_of[a], bytes_of[b]], "byte_span " + n["pointer"])
    ok(raw[n["byte_span"][0]:n["byte_span"][1]].decode("utf-8") == lit, "byte decode " + n["pointer"])
    if n["type"] in ("array", "object"):
        ok(n["length"] == len(v), "length " + n["pointer"])
        if n["type"] == "object":
            ok(n["children_keys"] == list(v.keys()), "key order " + n["pointer"])
    else:
        ok(n["value"] == v and type(n["value"]) == type(v), "value " + n["pointer"])
        ok(n["json_literal"] == lit, "json_literal " + n["pointer"])
    if n["type"] == "string":
        va, vb = n["value_span"]
        ok(va == a + 1 and vb == b - 1, "value_span bounds " + n["pointer"])
        ok((text[va:vb] == v) == n["decoded_equals_literal_interior"], "decoded flag " + n["pointer"])
    tick("nodes")

# 3. 원문 → 노드 (역방향)
allp = []


def walk(v, p):
    allp.append(p)
    if isinstance(v, dict):
        for k, c in v.items():
            walk(c, p + "/" + k.replace("~", "~0").replace("/", "~1"))
    elif isinstance(v, list):
        for i, c in enumerate(v):
            walk(c, f"{p}/{i}")


walk(data, "")
nptrs = [n["pointer"] for n in sm["nodes"]]
ok(len(nptrs) == len(set(nptrs)), "duplicate node pointers")
ok(set(allp) == set(nptrs) and len(allp) == len(nptrs), f"bidirectional nodes {len(allp)} vs {len(nptrs)}")
nkeys = sum(len(res(p)) for p in allp if isinstance(res(p), dict))
ok(len(sm["keys"]) == nkeys, f"key count {len(sm['keys'])} vs {nkeys}")
for k in sm["keys"]:
    ok(json.loads(text[k["span"][0]:k["span"][1]]) == k["key"], "key span " + k["value_pointer"])
    ok(k["value_pointer"] in set(nptrs), "key pointer " + k["value_pointer"])
ok(sorted(f["field_name"] for f in mo["field_names"]) == sorted({k["key"] for k in sm["keys"]}), "field name set")
ok(sum(f["occurrence_count"] for f in mo["field_names"]) == len(sm["keys"]), "field occurrence total")

# 4. 형태소 적용 ∪ 제외 = 모든 문자열 값 (서로소)
strs = {n["pointer"] for n in sm["nodes"] if n["type"] == "string"}
ap = [r["pointer"] for r in mo["values"]]
xp = [e["pointer"] for e in mo["excluded_values"]]
ok(len(ap) == len(set(ap)) and len(xp) == len(set(xp)), "morph duplicates")
ok(not (set(ap) & set(xp)) and set(ap) | set(xp) == strs, "morph partition")
for e in mo["excluded_values"]:
    ok(res(e["pointer"]) == e["value"] and e["reason"], "excluded record " + e["pointer"])
an = mo["analyzer"]
ok(an["version"] == "0.24.1" and an["model_type"] == "cong" and an["num_workers"] == 1, "analyzer settings")
TOK = {}
for r in mo["values"]:
    tx = res(r["pointer"])
    ok(tx == r["text"], "morph text " + r["pointer"])
    fa, fb = r["file_span_of_text"]
    ok(text[fa:fb] == tx, "morph file span " + r["pointer"])
    prev = 0
    for t in r["tokens"]:
        s, e = t["span"]
        ok(0 <= s <= e <= len(tx), "token bounds " + r["pointer"])
        ok(tx[s:e] == t["surface"], "token surface " + r["pointer"])
        ok(s >= prev - 1, "token order " + r["pointer"])
        prev = e
        if s == e:
            tick("zero_length_tokens")
        tick("tokens")
    TOK[r["pointer"]] = {(t["form"], t["tag"], t["span"][0], t["span"][1]) for t in r["tokens"]}
    # 토큰이 덮지 않은 비공백 문자가 없는가
    cov = set()
    for t in r["tokens"]:
        cov.update(range(t["span"][0], t["span"][1]))
    ok(all(i in cov for i, ch in enumerate(tx) if not ch.isspace()), "uncovered chars " + r["pointer"])

# 5. 오분절 표시 출현 = 실제 토큰
mseg = mo["segmentation_review"]
ok(len(mseg) == len(seg["occurrences"]), "segmentation review count")
for o in mseg:
    tx = res(o["pointer"])
    a, b = o["phrase_span"]
    ok(tx[a:b] == o["phrase"], "seg phrase " + o["pointer"])
    for form, tag, sp in o["tokens"]:
        ok((form, tag, sp[0], sp[1]) in TOK.get(o["pointer"], set()), f"seg token {o['pointer']} {form}")
    tick("segmentation_occurrences")
for f in mo["auto_flags"]:
    ok((f["form"], f["tag"], f["span"][0], f["span"][1]) in TOK[f["pointer"]], "auto flag " + f["pointer"])

# 6. 표현 후보
ids, keys = set(), set()
for x in ex["expressions"]:
    tx = res(x["pointer"])
    ok(isinstance(tx, str) and x["text"] and tx[x["span"][0]:x["span"][1]] == x["text"], "expr span " + x["id"])
    ok(x["id"] not in ids, "dup id " + x["id"])
    ids.add(x["id"])
    k = (x["pointer"], tuple(x["span"]), x["category_candidate"], x["method"])
    ok(k not in keys, "dup expr " + x["id"])
    keys.add(k)
    st = x.get("source_token")
    if st:
        ok((st["form"], st["tag"], st["span"][0], st["span"][1]) in TOK[x["pointer"]], "expr source token " + x["id"])
    tick("expressions")
ok({x["pointer"] for x in ex["expressions"] if x["category_candidate"] == "segment.value"} == set(ap), "segment.value coverage")
rv = load("expression-review.json")["items"]
ekeys = {(x["pointer"], tuple(x["span"]), x["category_candidate"]) for x in ex["expressions"]}
for i in rv:
    ok((i["pointer"], tuple(i["span"]), i["category_candidate"]) in ekeys, "review item missing " + i["pointer"])
ok(sum(1 for x in ex["expressions"] if "review" in x) >= len(rv), "review applied")
manual = load("manual-expressions.json")["expressions"]
mtexts = {x["text"] for x in ex["expressions"] if x["method"] == "manual(직접 읽기)"}
for m in manual:
    ok(m["text"] in mtexts, "manual no hit " + m["text"])

# 7. review.md 에 모든 말단 값이 원본 컬럼명·Pointer 와 함께 있는가
lines_by_ptr = {}
for line in review.splitlines():
    for p in re.findall(r"`(/[^`]*)`", line):
        lines_by_ptr.setdefault(p, []).append(line)
for n in sm["nodes"]:
    if n["type"] in ("array", "object"):
        continue
    v = n["value"]
    cell = str(v).replace("|", "\\|") if n["type"] == "string" else json.dumps(v)
    ls = lines_by_ptr.get(n["pointer"], [])
    ok(any(cell in l for l in ls), "review.md value missing " + n["pointer"])
    if isinstance(n["key"], str):
        ok(any(f"| {n['key']} |" in l for l in ls), "review.md column name missing " + n["pointer"])
    tick("review_leaf_values")

print(json.dumps({"source_sha256": h, "counts": counts, "failure_count": len(fails), "failures": fails[:50]},
                 ensure_ascii=False, indent=1))
sys.exit(1 if fails else 0)
