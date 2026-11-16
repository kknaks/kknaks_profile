"""problem-combos 1차 결과 독립 검증. 레포 루트에서:
  python3 orchestration/work/phub-ledger-redesign/first-pass/problem-combos/verify.py
원본·결과를 읽기만 한다. 실패가 하나라도 있으면 exit 1.
build.py 를 import 하지 않고 표준 json 으로 원본을 다시 열거한다.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "../../../phub-recommend/bronze/phub-ledger/problem-combos.json"))
EXPECTED_SHA = "74453c724800975ef7f3fa8b81546fe69fa014bfbc7a8f7e60c75774c2cf2262"
fails = []
checks = []


def check(name, ok, detail=""):
    checks.append((name, bool(ok), detail))
    if not ok:
        fails.append(f"{name}: {detail}")


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f)


def sha_file():
    return hashlib.sha256(open(SRC, "rb").read()).hexdigest()


sha_start = sha_file()
check("원본 해시(시작)", sha_start == EXPECTED_SHA, sha_start)
raw_b = open(SRC, "rb").read()
raw = raw_b.decode("utf-8")

# ---- 독립 열거
dups = []


def hook(pairs):
    ks = [k for k, _ in pairs]
    if len(ks) != len(set(ks)):
        dups.append(ks)
    return dict(pairs)


data = json.loads(raw, object_pairs_hook=hook)
check("중복 키 없음", not dups, str(dups))


def esc(k):
    return k.replace("~", "~0").replace("/", "~1")


ref = {}  # pointer -> (type, value|len, keys)
order = []


def walk(x, p):
    order.append(p)
    if isinstance(x, dict):
        ref[p] = ("object", len(x), list(x.keys()))
        for k, v in x.items():
            walk(v, p + "/" + esc(k))
    elif isinstance(x, list):
        ref[p] = ("array", len(x), None)
        for i, v in enumerate(x):
            walk(v, f"{p}/{i}")
    else:
        t = "string" if isinstance(x, str) else "boolean" if isinstance(x, bool) else "null" if x is None else "number"
        ref[p] = (t, x, None)


walk(data, "")
leaves = [p for p in order if ref[p][0] not in ("object", "array") or ref[p][1] == 0]
empties = [p for p in order if (ref[p][0] in ("object", "array") and ref[p][1] == 0) or ref[p][1] in ("", None)]

# ---- source-map
sm = load("source-map.json")
check("source-map 해시", sm["source"]["sha256"] == EXPECTED_SHA)
nodes = {n["pointer"]: n for n in sm["nodes"]}
check("source-map 노드 Pointer 중복 없음", len(nodes) == len(sm["nodes"]))
sm_set, ref_set = set(nodes), set(ref)
check("원본→source-map 누락 없음", not (ref_set - sm_set), str(sorted(ref_set - sm_set)[:5]))
check("source-map→원본 불필요 항목 없음", not (sm_set - ref_set), str(sorted(sm_set - ref_set)[:5]))
check("source-map 노드 순서 = 문서 순서", [n["pointer"] for n in sm["nodes"]] == order)
bad = []
for p, (t, v, keys) in ref.items():
    n = nodes.get(p)
    if not n:
        continue
    if n["type"] != t:
        bad.append((p, "type"))
    if t in ("object", "array"):
        if n["length"] != v:
            bad.append((p, "length"))
        if t == "object" and n["keys"] != keys:
            bad.append((p, "key order"))
    elif n["value"] != v or type(n["value"]) is not type(v):
        bad.append((p, "value"))
    s, e = n["literal_span"]
    if json.loads(raw[s:e]) != (v if t not in ("object", "array") else json.loads(raw[s:e])):
        bad.append((p, "literal"))
    if t in ("object", "array"):
        lit = json.loads(raw[s:e])
        if (len(lit) if lit is not None else -1) != v:
            bad.append((p, "container literal"))
    bs, be = n["literal_byte_span"]
    if raw_b[bs:be].decode("utf-8") != raw[s:e]:
        bad.append((p, "byte span"))
    if t == "string":
        cs, ce = n["content_span"]
        if raw[cs:ce] != v:
            bad.append((p, "content span"))
    for kl in n.get("key_literal_spans", []):
        a, b = kl["span"]
        if json.loads(raw[a:b]) != kl["key"] or raw_b[kl["byte_span"][0]:kl["byte_span"][1]].decode() != raw[a:b]:
            bad.append((p, "key span " + kl["key"]))
check("값·자료형·키순서·리터럴/바이트/내용 구간 재현", not bad, str(bad[:5]))
check("빈 값 0건(review 주장과 일치)", not empties, str(empties[:5]))

# ---- coverage
cov = load("coverage.json")
check("coverage 해시", cov["source_sha256"] == EXPECTED_SHA)
owned = [p for s in cov["segments"] for p in s["owned_pointers"]]
check("구획 소유 중복 없음", len(owned) == len(set(owned)), str(len(owned) - len(set(owned))))
check("원본 전체 경로 = 구획 소유 합집합(양방향)", set(owned) == ref_set,
      f"누락 {sorted(ref_set - set(owned))[:5]} 불필요 {sorted(set(owned) - ref_set)[:5]}")
owned_leaf = [p for s in cov["segments"] for p in s["owned_leaf_pointers"]]
check("말단·빈 컨테이너 = 구획 말단 합집합(양방향·중복 없음)", sorted(owned_leaf) == sorted(leaves) and len(owned_leaf) == len(set(owned_leaf)))
check("coverage all_pointers = 원본", cov["all_pointers"] == order)
for s in cov["segments"]:
    sid = s["segment_id"]
    check(f"{sid} 직접 읽기 상태", s["direct_read"] == "read", s["direct_read"])
    check(f"{sid} 기계 추출", s["machine_extracted"] is True)
    mpath = os.path.join(HERE, s["direct_read_record"])
    rpath = os.path.join(HERE, s["review_file"])
    check(f"{sid} 수동 기록 파일 실재", os.path.isfile(mpath), mpath)
    check(f"{sid} review 파일 실재", os.path.isfile(rpath), rpath)
    if not (os.path.isfile(mpath) and os.path.isfile(rpath)):
        continue
    man = json.load(open(mpath, encoding="utf-8"))
    body = open(rpath, encoding="utf-8").read()
    miss_ptr = [p for p in s["owned_pointers"] if p and f"`{p}`" not in body]
    check(f"{sid} review 에 소유 Pointer 전부", not miss_ptr, str(miss_ptr[:3]))
    miss_val = [p for p in s["owned_pointers"] if ref[p][0] == "string" and str(ref[p][1]).replace("|", "\\|") not in body]
    check(f"{sid} review 에 원문 값 전부(원문 그대로)", not miss_val, str(miss_val[:3]))
    for o in man["observations"]:
        if not (o["pointer"] in ref or re.sub(r"\*", "0", o["pointer"]) in ref):
            fails.append(f"{sid} 관찰 Pointer 무효 {o['pointer']}")
    # 관찰 Pointer 는 이 구획 소유 범위 안(S0 제외)
    if sid != "S0":
        root = s["owned_pointers"][0]
        out = [o["pointer"] for o in man["observations"] if not o["pointer"].startswith(root)]
        check(f"{sid} 관찰 Pointer 가 구획 안", not out, str(out))
    for e in man["expressions"]:
        if e["text"] not in str(ref.get(e["pointer"], ("", ""))[1]):
            fails.append(f"{sid} 수동 표현이 원문에 없음 {e['pointer']} {e['text']}")
    check(f"{sid} 관찰·표현 기록 있음", len(man["observations"]) > 0 and len(man["expressions"]) > 0)

# ---- review.md 목차
rv = open(os.path.join(HERE, "review.md"), encoding="utf-8").read()
for s in cov["segments"]:
    check(f"review.md 목차에 {s['review_file']}", f"]({s['review_file']})" in rv)
check("review.md 1차 종료·전체 완료 아님 표시", "1차 범위 종료" in rv and "원장 전체 완료 아님" in rv)
for col in ["problem_id", "problem", "tierLabel", "productTier", "priceRange", "expectedResult", "salesPitch", "upsellHook", "clinicalRationale", "riskBenefit"]:
    check(f"컬럼 구성 표에 원본 컬럼명 {col}", f"/{col}`" in rv)

# ---- morphology
mo = load("morphology.json")
check("morphology 해시", mo["source"]["sha256"] == EXPECTED_SHA)
check("분석기 기록", mo["analyzer"]["name"] == "kiwipiepy" and mo["analyzer"]["version"] == "0.24.1" and mo["analyzer"]["model_type"] == "cong" and mo["analyzer"]["num_workers"] == 1)
recs = mo["value_records"]
str_leaves = [p for p in order if ref[p][0] == "string"]
check("문자열 말단 = 형태소 기록(순서·1:1)", [r["pointer"] for r in recs] == str_leaves)
check("비문자열 말단 없음(숫자·불리언·null 0)", all(ref[p][0] == "string" for p in leaves))
rules = [(re.compile(x["pointer_pattern"]), x["reason"]) for x in mo["exclusions_rule"]]
bad = []
for r in recs:
    if r["text"] != ref[r["pointer"]][1]:
        bad.append((r["pointer"], "text"))
    rule = next((why for pat, why in rules if pat.match(r["pointer"])), None)
    if rule:
        if r["applied"] or r.get("exclude_reason") != rule or r["tokens"]:
            bad.append((r["pointer"], "exclude"))
    else:
        if not r["applied"] or not r["tokens"]:
            bad.append((r["pointer"], "apply"))
    for t in r["tokens"]:
        zw = t["start"] == t["end"]
        if not (0 <= t["start"] <= t["end"] <= len(r["text"])) or r["text"][t["start"]:t["end"]] != t["surface"] or zw != t.get("zero_width"):
            bad.append((r["pointer"], "token span"))
            break
    # 공백 아닌 문자는 모두 어떤 토큰 구간에 덮임
    covered = set()
    for t in r["tokens"]:
        covered.update(range(t["start"], t["end"]))
    if r["applied"]:
        un = [i for i, ch in enumerate(r["text"]) if not ch.isspace() and i not in covered]
        if un:
            bad.append((r["pointer"], f"미덮음 {un[:3]}"))
check("형태소 적용/제외·토큰 구간·전문자 덮음", not bad, str(bad[:5]))
check("레코드 ID 중복 없음", len({r["record_id"] for r in recs}) == len(recs))
# 필드명
occ = sorted((f["owner_pointer"], f["key"]) for f in mo["field_name_occurrences"])
exp_occ = sorted((p, k) for p, (t, v, keys) in ref.items() if t == "object" for k in keys)
check("필드명 출현 = 원본 모든 키 출현", occ == exp_occ, f"{len(occ)} vs {len(exp_occ)}")
check("필드명 토큰 기록(고유 키 전부)", set(mo["field_name_tokens"]) == {k for _, k in exp_occ})
bad = [k for k in mo["known_missegmentations"] if ref[k["pointer"]][1][k["span"][0]:k["span"][1]] != k["text"]]
check("알려진 오분절 구간 재현", not bad, str(bad[:3]))
check("알려진 오분절 상태 K", all(k["status"] == "K" for k in mo["known_missegmentations"]))

# ---- expressions
ex = load("expressions.json")
check("expressions 해시", ex["source"]["sha256"] == EXPECTED_SHA)
bad, keys = [], set()
for e in ex["expressions"]:
    v = ref[e["pointer"]][1]
    if v[e["span"][0]:e["span"][1]] != e["text"] or raw[e["file_span"][0]:e["file_span"][1]] != e["text"]:
        bad.append(e["expr_id"])
    k = (e["pointer"], tuple(e["span"]), e["kind"], e["method"])
    if k in keys:
        bad.append("dup " + e["expr_id"])
    keys.add(k)
check("표현 구간·파일 구간 재현·생성 중복 없음", not bad, str(bad[:5]))
check("수동 표현 전부 위치 확인", not ex["manual_unlocated"])
man_total = sum(len(json.load(open(os.path.join(HERE, s["direct_read_record"]), encoding="utf-8"))["expressions"]) for s in cov["segments"])
man_src = {e["manual_source"] for e in ex["expressions"] if e["method"] == "manual"}
check("수동 기록 표현 → expressions 전부 반영", len(man_src) == man_total, f"{len(man_src)} vs {man_total}")
bad = [s for s in ex["sentences"] if ref[s["pointer"]][1][s["span"][0]:s["span"][1]] != s["text"]]
check("문장 구간 재현", not bad, str(bad[:3]))
applied = {r["pointer"] for r in recs if r["applied"]}
check("적용 값 모두 문장 구간 보유", applied == {s["pointer"] for s in ex["sentences"]})

# ---- 그 밖의 산출물
for f in ["review.md", "source-map.json", "morphology.json", "expressions.json", "issues.md", "validation.md", "coverage.json", "progress.md", "build.py"]:
    check(f"산출물 실재 {f}", os.path.isfile(os.path.join(HERE, f)))
iss = open(os.path.join(HERE, "issues.md"), encoding="utf-8").read() if os.path.isfile(os.path.join(HERE, "issues.md")) else ""
all_ids = {i["id"] for s in cov["segments"] for i in json.load(open(os.path.join(HERE, s["direct_read_record"]), encoding="utf-8"))["issues"]}
check("구획 미결 ID 전부 issues.md 에", all(i in iss for i in all_ids), str(sorted(i for i in all_ids if i not in iss)))

sha_end = sha_file()
check("원본 해시(끝) 불변", sha_end == sha_start == EXPECTED_SHA, sha_end)

for name, ok, d in checks:
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f" — {d}"))
for f in fails:
    if not any(f.startswith(n) for n, ok, _ in checks if not ok):
        print("FAIL " + f)
print(f"\n{len(checks)} checks, {len(fails)} failures; nodes={len(ref)} leaves={len(leaves)} strings={len(str_leaves)}")
sys.exit(1 if fails else 0)
