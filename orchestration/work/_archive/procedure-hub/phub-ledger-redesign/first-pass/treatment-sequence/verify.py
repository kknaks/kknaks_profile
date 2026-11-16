"""treatment-sequence 1차 수집 결과의 독립 검증.

실행(레포 루트에서): python3 orchestration/work/phub-ledger-redesign/first-pass/treatment-sequence/verify.py
표준 라이브러리만 쓴다. build.py 코드를 가져오지 않는다. 어떤 파일도 쓰지 않는다.
실패가 하나라도 있으면 종료 코드 1.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../../../../.."))
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/treatment-sequence.json"
SRC = os.path.join(ROOT, SRC_REL)
EXPECTED_SHA = "e2f74d41d75a0b4b9d1f6216ccc17402af64bbd455b1c1627395a819ce76cfaf"

fails = []
results = []


def ok(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    if not cond:
        fails.append(f"{name}: {detail}")


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f)


raw = open(SRC, "rb").read()
sha0 = hashlib.sha256(raw).hexdigest()
text = raw.decode("utf-8")
ok("원본 해시 = 기록 해시", sha0 == EXPECTED_SHA, sha0)

SM = load("source-map.json")
MO = load("morphology.json")
EX = load("expressions.json")
for nm, d in (("source-map", SM), ("morphology", MO), ("expressions", EX)):
    ok(f"{nm} source 해시 시작/끝", d["source"]["sha256_start"] == sha0 and d["source"].get("sha256_end") == sha0)
    ok(f"{nm} source 크기", d["source"]["size_bytes"] == len(raw) and d["source"]["code_points"] == len(text))

# ---- 독립 파싱: 중복 키 감지 + 전체 위치 열거
dups = []


def hook(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            dups.append(k)
        seen.add(k)
    return dict(pairs)


ref = json.loads(text, object_pairs_hook=hook)
ok("중복 키 0 (독립 파서)", not dups and SM["duplicate_keys"] == [], str(dups))


def ep(k):
    return k.replace("~", "~0").replace("/", "~1")


WALK = {}
KEYS = []


def walk(o, p):
    WALK[p] = o
    if isinstance(o, dict):
        for k, v in o.items():
            KEYS.append((p, k, p + "/" + ep(k)))
            walk(v, p + "/" + ep(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{p}/{i}")


walk(ref, "")
NODES = {n["pointer"]: n for n in SM["nodes"]}
ok("노드 수 = 독립 열거 수", len(SM["nodes"]) == len(WALK) == len(NODES), f"{len(SM['nodes'])} vs {len(WALK)}")
ok("노드 집합 양방향 일치", set(NODES) == set(WALK), str(set(NODES) ^ set(WALK)))


def tname(v):
    if isinstance(v, bool):
        return "boolean"
    if isinstance(v, int):
        return "integer"
    if isinstance(v, float):
        return "number"
    if isinstance(v, str):
        return "string"
    if v is None:
        return "null"
    return "object" if isinstance(v, dict) else "array"


b_at = [0]
for ch in text:
    b_at.append(b_at[-1] + len(ch.encode("utf-8")))
bad = []
for p, v in WALK.items():
    n = NODES.get(p)
    if n is None:
        continue
    if n["type"] != tname(v):
        bad.append(("type", p))
    a, b = n["span"]
    if json.loads(text[a:b]) != v:
        bad.append(("span", p))
    if n["byte_span"] != [b_at[a], b_at[b]]:
        bad.append(("byte_span", p))
    if raw[n["byte_span"][0]:n["byte_span"][1]].decode("utf-8") != text[a:b]:
        bad.append(("bytes", p))
    if n["type"] in ("object", "array"):
        if n["length"] != len(v):
            bad.append(("length", p))
        if n["type"] == "object" and n["children"] != list(v.keys()):
            bad.append(("children-order", p))
    else:
        if n["value"] != v or tname(n["value"]) != tname(v):
            bad.append(("value", p))
        if n["json_literal"] != text[a:b]:
            bad.append(("literal", p))
    if n["type"] == "string":
        va, vb = n["value_span"]
        if text[va:vb] != v or va != a + 1 or vb != b - 1:
            bad.append(("value_span", p))
ok("노드별 자료형·값·span·byte_span·value_span·자식 순서", not bad, str(bad[:5]))

# 루트 span 이 파일 전체를 덮는지 (앞뒤 누락 없음)
ok("루트 span = 파일 전체", NODES[""]["span"] == [0, len(text)] or text[:NODES[""]["span"][0]].strip() == "" and text[NODES[""]["span"][1]:].strip() == "")

# ---- 키 출현
kp = [(k["object_pointer"], k["key"], k["value_pointer"]) for k in SM["keys"]]
ok("키 출현 양방향 일치(순서 포함)", kp == KEYS, f"{len(kp)} vs {len(KEYS)}")
kb = [k for k in SM["keys"] if text[k["span"][0]:k["span"][1]] != json.dumps(k["key"], ensure_ascii=False)]
ok("키 span 원문 재현", not kb, str(kb[:2]))
fo = {}
for o, k, vp in KEYS:
    fo.setdefault(k, []).append(vp)
ok("field_name_occurrences = 키 출현", {k: sorted(sum(v.values(), [])) for k, v in SM["field_name_occurrences"].items()}
   == {k: sorted(v) for k, v in fo.items()})

# ---- 형태소 적용/제외
strs = {p for p, v in WALK.items() if isinstance(v, str)}
an = [v["pointer"] for v in MO["values"]]
ex = [v["pointer"] for v in MO["excluded_values"]]
ok("문자열 = 분석 ⊔ 제외 (중복·누락 없음)", set(an) | set(ex) == strs and not set(an) & set(ex)
   and len(an) == len(set(an)) and len(ex) == len(set(ex)), f"str={len(strs)} an={len(an)} ex={len(ex)}")
ok("제외 항목마다 사유·원문 값", all(e["reason"] and e["value"] == WALK[e["pointer"]] for e in MO["excluded_values"]))
nonstr = {p for p, v in WALK.items() if not isinstance(v, (str, dict, list))}
ok("비문자열 말단 전부 기록", {x["pointer"] for x in MO["non_string_leaves"]} == nonstr
   and all(x["json_literal"] == NODES[x["pointer"]]["json_literal"] for x in MO["non_string_leaves"]), f"{len(nonstr)}")
ok("필드명 분석 = 전체 키 이름", {f["field_name"] for f in MO["field_names"]} == set(fo)
   and all(f["occurrence_count"] == len(fo[f["field_name"]]) for f in MO["field_names"]))
tb, gaps = [], []
for v in MO["values"]:
    s = WALK[v["pointer"]]
    if v["text"] != s or text[v["file_span_of_text"][0]:v["file_span_of_text"][1]] != s:
        tb.append(("text", v["pointer"]))
    cov = [False] * len(s)
    for t in v["tokens"]:
        a, b = t["span"]
        if not (0 <= a <= b <= len(s)) or s[a:b] != t["surface"] or (t["form_equals_surface"] != (t["form"] == t["surface"])):
            tb.append(("token", v["pointer"], t["form"]))
        for i in range(a, b):
            cov[i] = True
    for i, c in enumerate(cov):
        if not c and not s[i].isspace():
            gaps.append((v["pointer"], i, s[i]))
ok("형태소 surface = 값[span]·값 = 원문", not tb, str(tb[:5]))
# 토큰에 덮이지 않은 비공백 문자: Kiwi 가 이모지 변형 선택자 등 일부 문자를 따로 내지 않을 수 있다 → 기록과 비교
ok("형태소 미포함 비공백 문자 0", not gaps, str(gaps[:10]))

# ---- 오분절 기록
VT = {v["pointer"]: v for v in MO["values"]}
sb = []
ids = set()
for r in MO["segmentation_review"]["occurrences"]:
    v = VT.get(r["pointer"])
    a, b = r["phrase_span"]
    if v is None or v["text"][a:b] != r["phrase"]:
        sb.append(("phrase", r["id"]))
        continue
    got = [[t["form"], t["tag"], t["span"]] for t in v["tokens"] if t["span"][0] >= a and t["span"][1] <= b]
    if got != r["raw_tokens"]:
        sb.append(("raw", r["id"]))
    if r["id"] in ids:
        sb.append(("dup-id", r["id"]))
    ids.add(r["id"])
ok("오분절 기록 원문·원시 토큰 재현", not sb, str(sb[:5]))
on_disk = load("segmentation-review.json")
ok("morphology 안 오분절 기록 = segmentation-review.json", on_disk == MO["segmentation_review"])

# ---- 복합 표현
eb, sig, eids = [], set(), set()
for e in EX["expressions"]:
    p = e["pointer"]
    s = WALK.get(p)
    if not isinstance(s, str):
        eb.append(("ptr", e["id"]))
        continue
    a, b = e["span"]
    if not (0 <= a < b <= len(s)) or s[a:b] != e["text"]:
        eb.append(("span", e["id"]))
    k = (p, a, b, e["category_candidate"], e["method"])
    if k in sig:
        eb.append(("dup", e["id"]))
    sig.add(k)
    if e["id"] in eids:
        eb.append(("dup-id", e["id"]))
    eids.add(e["id"])
ok("표현 Pointer·구간 원문 재현·생성 중복 0", not eb, str(eb[:5]))
segv = {e["pointer"] for e in EX["expressions"] if e["category_candidate"] == "segment.value"}
ok("분석 값마다 segment.value 1건", segv == set(an))
ok("제외 값에는 표현 없음", not ({e["pointer"] for e in EX["expressions"]} & set(ex)))
MAN = load("manual-expressions.json")
mids = {e.get("manual_id") for e in EX["expressions"] if e["method"] == "manual(직접 읽기)"}
ok("수동 표현 전부 반영", mids == {m["id"] for m in MAN["phrases"]}, f"{len(mids)}/{len(MAN['phrases'])}")
fpb = [fp["id"] for fp in MAN["known_false_positives"]
       if not any(e["pointer"] == fp["pointer"] and e["span"] == fp["span"] and e["category_candidate"] == fp["category_candidate"]
                  for e in EX["expressions"])]
ok("알려진 오탐 기록 ↔ 표현 대응", not fpb, str(fpb))
segids = {r["id"] for r in MO["segmentation_review"]["occurrences"]}
ok("오태깅 유래 오탐 → 오분절 기록 존재", all(fp["segmentation_id"] in segids for fp in MAN["known_false_positives"] if fp["segmentation_id"]))

# ---- review.md: 모든 말단 Pointer 와 원문 값이 실제로 보이는지
rv = open(os.path.join(HERE, "review.md"), encoding="utf-8").read()
miss = []
for p, v in WALK.items():
    if isinstance(v, (dict, list)) or p == "":
        continue
    if f"`{p}`" not in rv:
        miss.append(("ptr", p))
    shown = v if isinstance(v, str) else NODES[p]["json_literal"]
    if str(shown).replace("|", "\\|") not in rv:
        miss.append(("value", p))
ok("review.md 에 모든 말단 Pointer·원문 값", not miss, str(miss[:5]))
for col in fo:
    if f"`{col}`" not in rv:
        miss.append(("col", col))
ok("review.md 에 모든 원본 컬럼명", not [m for m in miss if m[0] == "col"])

# ---- 원본 불변(끝)
sha1 = hashlib.sha256(open(SRC, "rb").read()).hexdigest()
ok("원본 해시 불변(verify 시작/끝)", sha0 == sha1 == EXPECTED_SHA, sha1)

for name, c, d in results:
    print(f"[{'OK' if c else 'FAIL'}] {name}" + (f" — {d}" if d and not c else ""))
print(f"checks={len(results)} failure_count={len(fails)}")
sys.exit(1 if fails else 0)
