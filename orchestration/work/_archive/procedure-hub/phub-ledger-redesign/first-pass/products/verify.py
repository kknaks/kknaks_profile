"""products.json 1차 산출물 독립 재검증 — build.py 코드를 쓰지 않고 원본과 출력 파일만 읽는다. 표준 라이브러리만.
실행(레포 루트): python3 orchestration/work/phub-ledger-redesign/first-pass/products/verify.py
파일을 쓰지 않는다. 실패가 하나라도 있으면 exit 1.
"""
import hashlib, json, os, re, sys

OUT = os.path.dirname(os.path.abspath(__file__))
SRC = "orchestration/work/phub-recommend/bronze/phub-ledger/products.json"
raw = open(SRC, "rb").read()
text = raw.decode("utf-8")
fails = []


def ok(c, msg):
    if not c:
        fails.append(msg)


dups = []


def hook(pairs):
    ks = [k for k, _ in pairs]
    if len(ks) != len(set(ks)):
        dups.append(ks)
    return dict(pairs)


data = json.loads(text, object_pairs_hook=hook)
H = hashlib.sha256(raw).hexdigest()
L = lambda n: json.load(open(os.path.join(OUT, n), encoding="utf-8"))
sm, mo, ex = L("source-map.json"), L("morphology.json"), L("expressions.json")
segrev, man, obs = L("segmentation-review.json"), L("manual-expressions.json"), L("observations.json")


def res(p):
    cur = data
    for part in p.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def has(p):
    try:
        res(p)
        return True
    except (KeyError, IndexError, ValueError, TypeError):
        return False


# 1. 해시·중복 키
ok(H == sm["source"]["sha256_start"] == sm["source"]["sha256_end"] == mo["source"]["sha256_start"] == ex["source"]["sha256_start"], "hash")
ok(sm["source"]["size_bytes"] == len(raw) and sm["source"]["code_points"] == len(text), "size")
ok(not dups and sm["duplicate_keys"] == [], "duplicate keys")

# 2. 노드 정방향: 포인터 해소·자료형·값·span·byte_span·value_span·literal
tmap = {dict: "object", list: "array", str: "string", bool: "boolean", int: "number", float: "number", type(None): "null"}
bo = [0]
for ch in text:
    bo.append(bo[-1] + len(ch.encode("utf-8")))
ptrs = [n["pointer"] for n in sm["nodes"]]
ok(len(ptrs) == len(set(ptrs)), "pointer unique")
for n in sm["nodes"]:
    p = n["pointer"]
    if not has(p):
        ok(False, "unresolvable " + p)
        continue
    v = res(p)
    ok(tmap[type(v)] == n["type"], "type " + p)
    s, e = n["span"]
    ok(json.loads(text[s:e]) == v, "span " + p)
    ok(n["byte_span"] == [bo[s], bo[e]] and raw[n["byte_span"][0]:n["byte_span"][1]].decode() == text[s:e], "byte " + p)
    if "value" in n:
        ok(n["value"] == v and type(n["value"]) == type(v), "value " + p)
    if n["type"] == "string":
        a, b = n["value_span"]
        ok(a == s + 1 and b == e - 1 and text[a:b] == v and not n["has_escape"], "value_span " + p)
    if n["literal"] is not None:
        ok(text[s:e] == n["literal"], "literal " + p)
    if isinstance(v, dict):
        ok(n["member_keys"] == list(v.keys()), "member order " + p)
    if isinstance(v, (dict, list)):
        ok(n["length"] == len(v), "length " + p)

# 3. 역방향: 원본 모든 경로가 노드에
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
ok(set(allp) == set(ptrs) and len(allp) == len(ptrs), "bidirectional nodes")
# 키: 개수·구간·출현 위치
nkeys = sum(len(res(p)) for p in allp if isinstance(res(p), dict))
ok(len(sm["keys"]) == nkeys, "key count")
for k in sm["keys"]:
    ok(text[k["span"][0]:k["span"][1]] == json.dumps(k["key"], ensure_ascii=False), "keyspan " + k["value_pointer"])
    ok(k["value_pointer"] in set(ptrs), "key ptr " + k["value_pointer"])
fo = sorted(p for d in sm["field_name_occurrences"].values() for ps in d.values() for p in ps)
ok(fo == sorted(k["value_pointer"] for k in sm["keys"]), "field name occurrences")

# 4. 형태소 적용/제외 분할 + 토큰 구간
strs = {n["pointer"] for n in sm["nodes"] if n["type"] == "string"}
ap = [r["pointer"] for r in mo["values"]]
xp = [e["pointer"] for e in mo["excluded_values"]]
ok(len(ap) == len(set(ap)) and len(xp) == len(set(xp)) and not set(ap) & set(xp) and set(ap) | set(xp) == strs, "morph partition")
for e in mo["excluded_values"]:
    ok(e.get("reason") and e.get("rule") and res(e["pointer"]) == e["value"], "excluded reason " + e["pointer"])
# 제외는 코드·날짜·버전·자리표시뿐인가
for e in mo["excluded_values"]:
    v, p = e["value"], e["pointer"]
    ok(p in ("/version", "/updated") or re.fullmatch(r"M\d+", v) or re.fullmatch(r"[A-Z]{2}", v) or v == "-", "exclusion scope " + p)
ok(sorted(o["value_pointer"] for o in mo["field_names"]["occurrences"]) == sorted(k["value_pointer"] for k in sm["keys"]), "fieldname exclusion coverage")
ntok = zero = 0
for r in mo["values"]:
    ok(res(r["pointer"]) == r["text"], "morph text " + r["pointer"])
    fs = r["file_span_of_text"]
    ok(text[fs[0]:fs[1]] == r["text"], "morph filespan " + r["pointer"])
    covered = set()
    for t in r["tokens"]:
        ntok += 1
        s, e = t["span"]
        ok(0 <= s <= e <= len(r["text"]) and r["text"][s:e] == t["surface"], "tok " + r["pointer"])
        ok(t["file_span"] == [fs[0] + s, fs[0] + e] and text[fs[0] + s:fs[0] + e] == t["surface"], "tok file " + r["pointer"])
        ok(t["byte_span"] == [bo[fs[0] + s], bo[fs[0] + e]], "tok byte " + r["pointer"])
        ok(t["lemma"] is not None, "lemma field " + r["pointer"])
        zero += s == e
        covered.update(range(s, e))
    ok(all(i in covered for i, c in enumerate(r["text"]) if not c.isspace()), "token coverage " + r["pointer"])
# 알려진 오분절 표시 ↔ 실제 토큰
tokset = {(r["pointer"], t["span"][0], t["span"][1], t["form"], t["tag"]) for r in mo["values"] for t in r["tokens"]}
ids = set()
for o in segrev["occurrences"]:
    ok(o["id"] not in ids and o["status"] == "표시됨(교정 아님)" and o["impact"], "segrev meta " + o["id"])
    ids.add(o["id"])
    for f, tg, sp in o["tokens"]:
        ok((o["pointer"], sp[0], sp[1], f, tg) in tokset, f"segrev token {o['id']} {f}/{tg}{sp}")
ok(mo["segmentation_review"] == segrev, "segrev embedded copy")

# 5. 표현
eids, ekeys = set(), set()
for x in ex["expressions"]:
    tx = res(x["pointer"])
    s, e = x["span"]
    ok(isinstance(tx, str) and tx[s:e] == x["text"] and x["text"] and x["value_text"] == tx, "expr " + x["id"])
    ok(text[x["file_span"][0]:x["file_span"][1]] == x["text"], "expr file " + x["id"])
    ok(x["id"] not in eids, "dup id " + x["id"])
    eids.add(x["id"])
    k = (x["pointer"], tuple(x["span"]), x["category_candidate"], x["method"])
    ok(k not in ekeys, "dup expr " + x["id"])
    ekeys.add(k)
ok({x["pointer"] for x in ex["expressions"] if x["category_candidate"] == "segment.value"} == strs, "value segment coverage")
# 수동 표현: 모두 반영
mids = {x["manual_id"] for x in ex["expressions"] if x["method"] == "manual:read"}
ok(mids == {m["mid"] for m in man["expressions"]}, "manual coverage")
for m in man["expressions"]:
    ok(m["viewpoint"] in man["viewpoints"], "viewpoint " + m["mid"])

# 6. 관찰 포인터
for o in obs["observations"]:
    for p in o["pointers"]:
        ok(has(p), "obs pointer " + o["id"] + " " + p)

# 7. review.md 가 모든 말단 값을 원본 키·포인터와 함께 싣는가
rv = open(os.path.join(OUT, "review.md"), encoding="utf-8").read()
top, rest = rv.split("## 2.", 1)[0], rv.split("## 3.", 1)[1].split("## 4.", 1)[0]
rv = top + rest  # §1(최상위 스칼라) + §3(항목별 값)만 대조. §2 예시 칸으로 우연히 통과하지 않게
leaf = [n for n in sm["nodes"] if n["type"] not in ("object", "array")]
for n in leaf:
    lit = n["literal"].replace("|", "\\|")
    ok(f"| {lit} | `{n['pointer']}` |" in rv, "review leaf " + n["pointer"])

# 8. 끝 해시
ok(hashlib.sha256(open(SRC, "rb").read()).hexdigest() == H, "hash end")

print(json.dumps({"sha256": H, "nodes": len(ptrs), "keys": len(sm["keys"]), "strings": len(strs),
                  "morph_applied": len(ap), "morph_excluded": len(xp), "tokens": ntok, "zero_length_tokens": zero,
                  "segrev": len(segrev["occurrences"]), "expressions": len(ex["expressions"]),
                  "manual": len(man["expressions"]), "observations": len(obs["observations"]),
                  "review_leaf_rows": len(leaf), "failure_count": len(fails)}, ensure_ascii=False))
for f in fails[:50]:
    print("FAIL", f)
sys.exit(1 if fails else 0)
