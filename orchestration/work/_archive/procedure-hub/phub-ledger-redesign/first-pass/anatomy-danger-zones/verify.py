#!/usr/bin/env python3
"""anatomy-danger-zones 1차 수집 결과 독립 검증. 표준 라이브러리만 쓴다. 파일을 쓰지 않는다.

레포 루트에서:  python3 orchestration/work/phub-ledger-redesign/first-pass/anatomy-danger-zones/verify.py
실패가 하나라도 있으면 종료 코드 1.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "../../../../.."))
SRC = os.path.join(REPO, "orchestration/work/phub-recommend/bronze/phub-ledger/anatomy-danger-zones.json")
EXPECTED_SHA = "34b2a2de737a2770828ce52e49c3f4f17dc54c21ad9754362c24ebf4fced69a4"

fails = []
checks = 0


def check(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f)


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


h_start = sha(SRC)
check(h_start == EXPECTED_SHA, "원본 해시가 기대값과 다름: %s" % h_start)
with open(SRC, "rb") as f:
    raw = f.read()
text = raw.decode("utf-8")

# ---- 독립 열거(중복 키 감지)
dups = []


def hook(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            dups.append(k)
        seen.add(k)
    return dict(pairs)


doc = json.loads(text, object_pairs_hook=hook)
check(not dups, "중복 키: %s" % dups)

truth = {}   # pointer -> (type, value or size)


def tname(v):
    if isinstance(v, dict):
        return "object"
    if isinstance(v, list):
        return "array"
    if isinstance(v, str):
        return "string"
    if isinstance(v, bool):
        return "boolean"
    if v is None:
        return "null"
    return "integer" if isinstance(v, int) else "number"


order = []


def walk(v, p):
    order.append(p)
    t = tname(v)
    truth[p] = (t, len(v) if t in ("object", "array") else v)
    if t == "object":
        for k, x in v.items():
            walk(x, p + "/" + k.replace("~", "~0").replace("/", "~1"))
    elif t == "array":
        for i, x in enumerate(v):
            walk(x, "%s/%d" % (p, i))


walk(doc, "")
leaves_truth = {p for p, (t, v) in truth.items() if t not in ("object", "array") or v == 0}

# ---- source-map
sm = load("source-map.json")
check(sm["source"]["sha256"] == EXPECTED_SHA, "source-map 해시 불일치")
check(sm["source"]["bytes"] == len(raw) and sm["source"]["codepoints"] == len(text), "크기 불일치")
nodes = sm["nodes"]
ptrs = [n["pointer"] for n in nodes]
check(len(ptrs) == len(set(ptrs)), "source-map 포인터 중복")
check(set(ptrs) == set(truth), "source-map 경로 집합 ≠ 원문: 누락 %s / 불필요 %s" % (
    sorted(set(truth) - set(ptrs))[:5], sorted(set(ptrs) - set(truth))[:5]))
check(ptrs == order, "source-map 문서 순서가 원문 순서와 다름")
byte_of = [0]
for ch in text:
    byte_of.append(byte_of[-1] + len(ch.encode("utf-8")))
prev = -1
for n in nodes:
    p = n["pointer"]
    if p not in truth:
        continue
    t, v = truth[p]
    check(n["json_type"] == t, "자료형 불일치 %s" % p)
    if t in ("object", "array"):
        check(n["size"] == v, "크기 불일치 %s" % p)
    else:
        check(n["value"] == v and type(n["value"]) is type(v), "값 불일치 %s" % p)
    s, e = n["literal_cp_span"]
    lit = text[s:e]
    sub = json.loads(lit)
    ref = doc
    for tok in (p[1:].split("/") if p else []):
        tok = tok.replace("~1", "/").replace("~0", "~")
        ref = ref[int(tok)] if isinstance(ref, list) else ref[tok]
    check(sub == ref, "리터럴 구간 재현 실패 %s" % p)
    bs, be = n["literal_byte_span"]
    check(raw[bs:be].decode("utf-8") == lit and bs == byte_of[s] and be == byte_of[e], "바이트 구간 불일치 %s" % p)
    check(s > prev, "구간 순서 역전 %s" % p)
    prev = s
    if t == "string":
        a, b = n["string_content_cp_span"]
        check(text[a:b] == v and a == s + 1 and b == e - 1, "문자열 내용 구간 불일치 %s" % p)
        check(raw[n["string_content_byte_span"][0]:n["string_content_byte_span"][1]].decode() == v, "문자열 바이트 구간 %s" % p)
    if t in ("integer", "number"):
        check(n.get("number_literal") == lit, "숫자 리터럴 불일치 %s" % p)
    if n.get("key") is not None:
        ks, ke = n["key_literal_cp_span"]
        check(json.loads(text[ks:ke]) == n["key"], "키 구간 불일치 %s" % p)
    check(n["is_leaf"] == (p in leaves_truth), "말단 표시 불일치 %s" % p)

# ---- coverage: 양방향 소유 대조
cov = load("coverage.json")
check(cov["source_sha256"] == EXPECTED_SHA, "coverage 해시")
owned = []
owned_leaves = []
for s in cov["sections"]:
    owned += s["owned_pointers"]
    owned_leaves += s["owned_leaf_pointers"]
    check(s["direct_read"] == "done", "구획 직접 읽기 미완 %s" % s["id"])
    check(s["machine_extracted"] is True, "기계 추출 미완 %s" % s["id"])
    check(os.path.isfile(os.path.join(HERE, s["review_file"])), "리뷰 파일 없음 %s" % s["review_file"])
    check(set(s["owned_leaf_pointers"]) <= set(s["owned_pointers"]), "말단 소유가 노드 소유 밖 %s" % s["id"])
    for sp in s.get("shared_context_not_owned", []):
        check(sp not in s["owned_pointers"], "공유 문맥을 소유로 기록 %s %s" % (s["id"], sp))
    # 구획 소유 규칙 독립 재계산
    for p in s["owned_pointers"]:
        m = re.match(r"^/zones/(\d+)(/|$)", p)
        exp = "S%02d" % (int(m.group(1)) + 1) if m else "S00"
        check(exp == s["id"], "구획 배정 규칙 위반 %s → %s" % (p, s["id"]))
check(len(owned) == len(set(owned)), "구획 간 소유 중복: %d" % (len(owned) - len(set(owned))))
check(set(owned) == set(truth), "소유 합집합 ≠ 원문 경로: 누락 %s / 불필요 %s" % (
    sorted(set(truth) - set(owned))[:5], sorted(set(owned) - set(truth))[:5]))
check(len(owned_leaves) == len(set(owned_leaves)) and set(owned_leaves) == leaves_truth, "말단 소유 합집합 불일치")
check(cov["reading_log"]["remaining"] == [], "남은 구획 있음")
check([s["id"] for s in cov["sections"]] == ["S%02d" % i for i in range(12)], "구획 목록")

# ---- review 문서(분할) 대조: 모든 노드 행·원문 값
def md(s):
    return str(s).replace("|", "\\|").replace("\n", "<br>")


review = read("review.md")
nodemap = {n["pointer"]: n for n in nodes}
for s in cov["sections"]:
    check("(%s)" % s["review_file"] in review, "review.md 에 구획 링크 없음 %s" % s["id"])
    part = read(s["review_file"])
    rows = {}
    for line in part.splitlines():
        m = re.match(r"^\| (\d+) \| `([^`]*)` \| `([^`]*)` \| ([^|]*) \| ([^|]*) \| (.*) \|$", line)
        if m:
            rows[m.group(2)] = line
    for p in s["owned_pointers"]:
        key = p or "(root)"
        line = rows.get(key)
        check(line is not None, "review 파트에 행 없음 %s %s" % (s["id"], key))
        if line is None:
            continue
        t, v = truth[p]
        n = nodemap[p]
        if t == "string":
            check(line.endswith("| %s |" % md(v)), "review 원문 값 불일치 %s" % p)
        elif t in ("integer", "number"):
            check(line.endswith("| `%s` |" % n["number_literal"]), "review 숫자 리터럴 불일치 %s" % p)
        colname = n["key"] if n["key"] is not None else None
        if colname is not None:
            check("| `%s` | `%s` |" % (key, colname) in line, "review 원본 컬럼명 불일치 %s" % p)
    check("## 잠정 관찰" in part and "## 원문 값" in part, "review 파트 절 구성 %s" % s["id"])
# 컬럼 구성 표: 모든 경로 패턴 행
pats = {re.sub(r"/\d+(?=/|$)", "/*", p) or "(root)" for p in truth}
for pt in pats:
    check("| `%s` |" % pt in review, "컬럼 구성 표에 패턴 없음 %s" % pt)

# ---- morphology: 적용/제외 대응
mo = load("morphology.json")
str_leaves = {p for p in leaves_truth if truth[p][0] == "string"}
num_leaves = {p for p in leaves_truth if truth[p][0] in ("integer", "number")}
applied = [r["pointer"] for r in mo["text_values"]]
excl = [r["pointer"] for r in mo["excluded"]]
check(len(applied) == len(set(applied)) and len(excl) == len(set(excl)), "형태소 기록 중복")
check(not (set(applied) & set(excl)), "적용·제외 동시")
check(set(applied) | set(excl) == leaves_truth, "적용∪제외 ≠ 전체 말단")
check(num_leaves <= set(excl), "숫자 말단 제외 누락")
for r in mo["excluded"]:
    check(bool(r.get("reason")), "제외 사유 없음 %s" % r["pointer"])
for r in mo["text_values"]:
    p = r["pointer"]
    v = truth[p][1]
    check(r["value"] == v, "형태소 값 불일치 %s" % p)
    base = nodemap[p]["string_content_cp_span"][0]
    check(r["file_cp_span"] == nodemap[p]["string_content_cp_span"], "형태소 파일 구간 %s" % p)
    last = 0
    for t in r["tokens"]:
        a, b = t["span"]
        check(0 <= a <= b <= len(v), "토큰 구간 범위 %s" % p)
        check(v[a:b] == t["surface"], "토큰 표면 불일치 %s %s" % (p, t))
        check(t["file_cp_span"] == [base + a, base + b] and text[base + a:base + b] == t["surface"], "토큰 파일 구간 %s" % p)
        check(t["form_equals_surface"] == (t["form"] == t["surface"]), "form 비교 표시 %s" % p)
        check(a >= last or b == a or t["form_equals_surface"] is False, "토큰 순서 %s" % p)
        last = max(last, a)
    check(len(r["tokens"]) > 0, "토큰 0 %s" % p)
keys = set()
for n in nodes:
    if n.get("key") is not None:
        keys.add(n["key"])
check({f["field_name"] for f in mo["field_names"]} == keys, "필드명 분석 집합 ≠ 전체 키")
for f in mo["field_names"]:
    check(sorted(f["pointers"]) == sorted(n["pointer"] for n in nodes if n.get("key") == f["field_name"]), "필드명 출현 %s" % f["field_name"])
for o in mo["segmentation_review"]["occurrences"]:
    v = truth[o["pointer"]][1]
    check(v[o["span"][0]:o["span"][1]] == o["term"], "분절 관찰 구간 %s" % o["pointer"])
for o in mo["number_unit_review"]["occurrences"]:
    v = truth[o["pointer"]][1]
    check(v[o["span"][0]:o["span"][1]] == o["text"], "수치 관찰 구간 %s" % o["pointer"])
for o in mo["cue_review"]["occurrences"]:
    v = truth[o["pointer"]][1]
    check(v[o["span"][0]:o["span"][1]] == o["cue"], "단서 관찰 구간 %s" % o["pointer"])
an = mo["analyzer"]
check(an["kiwipiepy"] == "0.24.1" and an["model_type"] == "cong" and an["num_workers"] == 1, "분석기 설정 기록")

# ---- expressions
ex = load("expressions.json")
man = load("manual-review.json")
ids = [e["id"] for e in ex["manual"]] + [e["id"] for e in ex["regex_candidates"]]
check(len(ids) == len(set(ids)), "표현 ID 중복")
src_manual = [(sid, e[0], e[1]) for sid, sec in man["sections"].items() for e in sec["expressions"]]
got_manual = [(e["section"], e["pointer"], e["text"]) for e in ex["manual"]]
check(src_manual == got_manual, "수동 표현 기록 ≠ manual-review.json")
check(set(man["sections"]) == {s["id"] for s in cov["sections"]}, "manual-review 구획 누락")
seen = set()
for e in ex["manual"]:
    v = truth[e["pointer"]][1]
    a, b = e["span"]
    check(v[a:b] == e["text"] and e["whole_value"] == v, "수동 표현 구간 %s" % e["id"])
    fa, fb = e["file_cp_span"]
    check(text[fa:fb] == e["text"], "수동 표현 파일 구간 %s" % e["id"])
    check(raw[e["file_byte_span"][0]:e["file_byte_span"][1]].decode() == e["text"], "수동 표현 바이트 구간 %s" % e["id"])
    k = (e["pointer"], a, b)
    check(k not in seen, "수동 표현 중복 생성 %s" % e["id"])
    seen.add(k)
for e in ex["regex_candidates"] + ex["clause_segments"]:
    v = truth[e["pointer"]][1]
    a, b = e["span"]
    check(v[a:b] == e["text"], "후보/절 구간 %s" % e.get("id", e["pointer"]))
    check(text[e["file_cp_span"][0]:e["file_cp_span"][1]] == e["text"], "후보/절 파일 구간 %s" % e.get("id", e["pointer"]))
# 정규식 후보 독립 재계산(같은 패턴으로 개수·구간 일치)
recount = []
for p in sorted(str_leaves, key=lambda x: nodemap[x]["document_order"]):
    for name, pat in ex["regex_patterns"].items():
        for m in re.finditer(pat, truth[p][1]):
            recount.append((p, name, m.start(), m.end()))
got = [(e["pointer"], e["pattern"], e["span"][0], e["span"][1]) for e in ex["regex_candidates"]]
check(sorted(recount) == sorted(got), "정규식 후보 재계산 불일치 (%d vs %d)" % (len(recount), len(got)))

# ---- 관찰·미결 참조
issues = read("issues.md")
for sid, sec in man["sections"].items():
    for o in sec["observations"]:
        check(o[0] in ("A", "B", "C", "I", "P", "F", "K"), "관찰 상태 문자 %s" % o)
        for p in o[1]:
            check(p in truth, "관찰 근거 Pointer 없음 %s" % p)
        if o[3]:
            check(("### %s" % o[3]) in issues, "issues.md 에 미결 ID 없음 %s" % o[3])
for m in re.finditer(r"`(/[^`\s*]*)`", issues):
    check(m.group(1) in truth, "issues.md Pointer 가 원문에 없음 %s" % m.group(1))

h_end = sha(SRC)
check(h_end == h_start, "검증 중 원본 해시 변경")

print("source sha256 start=%s end=%s" % (h_start, h_end))
print("nodes=%d leaves=%d string_leaves=%d number_leaves=%d" % (len(truth), len(leaves_truth), len(str_leaves), len(num_leaves)))
print("sections=%d owned_union=%d text_values=%d excluded=%d field_names=%d" % (
    len(cov["sections"]), len(set(owned)), len(applied), len(excl), len(mo["field_names"])))
print("manual_expressions=%d regex_candidates=%d clause_segments=%d" % (
    len(ex["manual"]), len(ex["regex_candidates"]), len(ex["clause_segments"])))
print("checks=%d fails=%d" % (checks, len(fails)))
for f in fails[:50]:
    print("FAIL:", f)
sys.exit(1 if fails else 0)
