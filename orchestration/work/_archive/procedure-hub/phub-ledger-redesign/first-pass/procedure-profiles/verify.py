"""산출물 독립 재검증 — build.py 코드를 쓰지 않고 출력 파일과 원본만 읽는다. 표준 라이브러리만 사용.
실행(레포 루트): python3 orchestration/work/phub-ledger-redesign/first-pass/procedure-profiles/verify.py
"""
import hashlib, json, os, sys
OUT = os.path.dirname(os.path.abspath(__file__))
SRC = "orchestration/work/phub-recommend/bronze/phub-ledger/procedure-profiles.json"
raw = open(SRC, "rb").read(); text = raw.decode("utf-8"); data = json.loads(text)
h = hashlib.sha256(raw).hexdigest()
sm = json.load(open(os.path.join(OUT, "source-map.json"))); mo = json.load(open(os.path.join(OUT, "morphology.json")))
ex = json.load(open(os.path.join(OUT, "expressions.json")))
fails = []
def ok(c, msg):
    if not c: fails.append(msg)
def res(p):
    cur = data
    for part in p.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur
ok(h == sm["source"]["sha256_start"] == sm["source"]["sha256_end"] == mo["source"]["sha256_start"] == ex["source"]["sha256_start"], "hash")
# 모든 노드 포인터 해소 + span 재파싱 값 일치 + 자료형
tmap = {dict: "object", list: "array", str: "string", bool: "boolean", int: "number", float: "number", type(None): "null"}
for n in sm["nodes"]:
    v = res(n["pointer"])
    ok(tmap[type(v)] == n["type"], "type " + n["pointer"])
    ok(json.loads(text[n["span"][0]:n["span"][1]]) == v, "span " + n["pointer"])
    ok(raw[n["byte_span"][0]:n["byte_span"][1]].decode() == text[n["span"][0]:n["span"][1]], "byte " + n["pointer"])
    if "value" in n: ok(n["value"] == v and type(n["value"]) == type(v), "value " + n["pointer"])
# 역방향: 원본의 모든 경로가 노드에 있는가
ptrs = {n["pointer"] for n in sm["nodes"]}; allp = []
def walk(v, p):
    allp.append(p)
    if isinstance(v, dict): [walk(c, p + "/" + k.replace("~", "~0").replace("/", "~1")) for k, c in v.items()]
    elif isinstance(v, list): [walk(c, f"{p}/{i}") for i, c in enumerate(v)]
walk(data, "")
ok(set(allp) == ptrs and len(allp) == len(sm["nodes"]), "bidirectional")
ok(len(sm["keys"]) == sum(len(v) for p in allp for v in [res(p)] if isinstance(v, dict)), "key count")
for k in sm["keys"]: ok(text[k["span"][0]:k["span"][1]] == json.dumps(k["key"], ensure_ascii=False), "keyspan " + k["value_pointer"])
# 문자열 값 = 형태소 적용 ∪ 제외 (서로소)
strs = {n["pointer"] for n in sm["nodes"] if n["type"] == "string"}
ap = [r["pointer"] for r in mo["values"]]; xp = [e["pointer"] for e in mo["excluded_values"]]
ok(len(ap) == len(set(ap)) and len(xp) == len(set(xp)) and not (set(ap) & set(xp)) and set(ap) | set(xp) == strs, "morph partition")
for r in mo["values"]:
    ok(res(r["pointer"]) == r["text"], "morph text " + r["pointer"])
    fs = r["file_span_of_text"]; ok(text[fs[0]:fs[1]] == r["text"], "morph filespan " + r["pointer"])
    for t in r["tokens"]:
        ok(r["text"][t["span"][0]:t["span"][1]] == t["surface"] and t["span"][0] < t["span"][1], "tok " + r["pointer"])
        ok(text[fs[0] + t["span"][0]:fs[0] + t["span"][1]] == t["surface"], "tok filespan " + r["pointer"])
for s in mo["segmentation_review"]:
    tx = res(s["pointer"])
    for form, tag, sp in s["tokens"]: ok(sp[0] < len(tx) and sp[1] <= len(tx), "segrev " + s["pointer"])
# 표현: 구간 재현 + id 유일 + 완전 중복 없음
ids = set(); keys = set()
for x in ex["expressions"]:
    tx = res(x["pointer"])
    ok(isinstance(tx, str) and tx[x["span"][0]:x["span"][1]] == x["text"] and x["text"], "expr " + x["id"])
    ok(x["id"] not in ids, "dup id " + x["id"]); ids.add(x["id"])
    k = (x["pointer"], tuple(x["span"]), x["category_candidate"], x["method"]); ok(k not in keys, "dup expr " + x["id"]); keys.add(k)
ok({x["pointer"] for x in ex["expressions"] if x["category_candidate"] == "segment.value"} == set(ap), "value segment coverage")
# 출현 단위 오태깅 판정 ↔ 토큰 ↔ 표시 ↔ 파생 표현
occ = json.load(open(os.path.join(OUT, "segmentation-occurrence-review.json")))
tags = set(occ["scope"]["sweep_tags"]); sigs = {tuple(x) for x in occ["scope"]["signatures"]}
okeys = {}
for o in occ["occurrences"]:
    k = (o["pointer"], o["span"][0], o["span"][1], o["form"], o["tag"]); ok(k not in okeys, "occ dup"); okeys[k] = o["verdict"]
live = {(r["pointer"], t["span"][0], t["span"][1], t["form"], t["tag"]) for r in mo["values"] for t in r["tokens"]
        if t["tag"] in tags or (t["form"], t["tag"]) in sigs}
ok(live == set(okeys), "occurrence coverage (missing %d, stale %d)" % (len(live - set(okeys)), len(set(okeys) - live)))
marked = {(s["pointer"], tk[2][0], tk[2][1], tk[0], tk[1]) for s in mo["segmentation_review"] for tk in s["tokens"]}
for k, v in okeys.items():
    ok((v != "correct") == (k in marked), "occ<->segrev " + str(k))
for s in mo["segmentation_review"]:
    ok(s.get("status", "").startswith("표시됨(교정 아님)"), "segrev status")
tokset = {(r["pointer"], t["span"][0], t["span"][1], t["form"], t["tag"]) for r in mo["values"] for t in r["tokens"]}
for s in mo["segmentation_review"]:
    for tk in s["tokens"]: ok((s["pointer"], tk[2][0], tk[2][1], tk[0], tk[1]) in tokset, "segrev token exists")
der = 0
for x in ex["expressions"]:
    if x["category_candidate"] == "modifier_phrase":
        st = x.get("source_token"); ok(st is not None, "modifier source " + x["id"])
        if st:
            v = okeys.get((x["pointer"], st["span"][0], st["span"][1], st["form"], st["tag"]), "correct")
            flagged = "오태깅 유래" in (x.get("review") or "")
            ok((v != "correct") == flagged, "derived fp " + x["id"]); der += flagged
er = json.load(open(os.path.join(OUT, "expression-review.json")))["entries"]
for e_ in er:
    m_ = [x for x in ex["expressions"] if x["pointer"] == e_["pointer"] and x["span"] == e_["span"] and x["category_candidate"] == e_["category_candidate"]]
    ok(len(m_) == 1 and m_[0]["text"] == e_["text"] and (m_[0].get("review") or "").startswith("false_positive"), "expr-review " + e_["pointer"])
ok(sum(1 for x in ex["expressions"] if (x.get("review") or "").startswith("false_positive")) == len(er) + der, "fp total")
print(json.dumps({"sha256": h, "occurrences": len(okeys), "occ_non_correct": sum(v != "correct" for v in okeys.values()),
                  "mistag_derived_fp": der, "expr_review_entries": len(er), "nodes": len(sm["nodes"]), "paths": len(allp), "keys": len(sm["keys"]), "morph_values": len(ap),
                  "excluded": len(xp), "tokens": sum(len(r["tokens"]) for r in mo["values"]), "expressions": len(ex["expressions"]),
                  "segmentation_review": len(mo["segmentation_review"]), "failures": fails[:20], "failure_count": len(fails)}, ensure_ascii=False, indent=1))
sys.exit(1 if fails else 0)
