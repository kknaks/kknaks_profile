"""patient-education.json 1차 조사 독립 검증 — 레포 루트에서:

  python3 orchestration/work/phub-ledger-redesign/first-pass/patient-education/verify.py

표준 라이브러리만 쓴다. build.py·pe_common.py 를 import 하지 않는다(독립 재구현).
원본과 결과 파일을 읽기만 하고 어떤 파일도 쓰지 않는다. 실패가 하나라도 있으면 exit 1.
"""
import copy
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
SRC = os.path.join(REPO, "orchestration/work/phub-recommend/bronze/phub-ledger/patient-education.json")
EXPECTED_SHA = "6c96520c514b76ef7f93d7f685e53023afe91b05133a9b9ca5db0a95d42d91ac"
REQUIRED = ["review.md", "source-map.json", "morphology.json", "expressions.json", "issues.md", "validation.md",
            "coverage.json", "progress.md", "build.py", "verify.py", "segments.json", "observations.json"]

fails = []
checks = 0


def check(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
    return cond


def load(name):
    return json.load(open(os.path.join(HERE, name), encoding="utf-8"))


raw0 = open(SRC, "rb").read()
sha0 = hashlib.sha256(raw0).hexdigest()
check(sha0 == EXPECTED_SHA, "원본 해시 불일치(시작): %s" % sha0)
text = raw0.decode("utf-8")
c2b = [0]
for ch in text:
    c2b.append(c2b[-1] + len(ch.encode("utf-8")))

for f in REQUIRED:
    check(os.path.isfile(os.path.join(HERE, f)), "필수 파일 없음: %s" % f)

# ---- 독립 구조 열거 (json 모듈 · 중복 키 감지)
dups = []


def hook(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            dups.append(k)
        seen.add(k)
    return dict(pairs)


data = json.loads(text, object_pairs_hook=hook)
check(not dups, "중복 키: %r" % dups)


def esc(k):
    return k.replace("~", "~0").replace("/", "~1")


walk = []  # (pointer, type, value_or_None, child_count)


def go(x, p):
    if isinstance(x, dict):
        walk.append((p, "object", None, len(x)))
        for k, v in x.items():
            go(v, p + "/" + esc(k))
    elif isinstance(x, list):
        walk.append((p, "array", None, len(x)))
        for i, v in enumerate(x):
            go(v, p + "/" + str(i))
    else:
        t = "null" if x is None else "boolean" if isinstance(x, bool) else "number" if isinstance(x, (int, float)) else "string"
        walk.append((p, t, x, None))


go(data, "")
W = {w[0]: w for w in walk}
all_ptrs = [w[0] for w in walk]
leaf_ptrs = [w[0] for w in walk if w[1] not in ("object", "array") or w[3] == 0]
str_ptrs = [w[0] for w in walk if w[1] == "string"]


def resolve(p):
    x = data
    for part in p.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        x = x[int(part)] if isinstance(x, list) else x[part]
    return x


# ---- source-map
sm = load("source-map.json")
check(sm["source_sha256"] == sha0, "source-map 해시")
check(sm["source_bytes"] == len(raw0) and sm["source_codepoints"] == len(text), "source-map 크기")
smn = sm["nodes"]
sm_ptrs = [n["pointer"] for n in smn]
check(len(sm_ptrs) == len(set(sm_ptrs)), "source-map Pointer 중복")
check(set(sm_ptrs) == set(all_ptrs), "source-map ↔ 원문 Pointer 양방향 불일치: 누락 %s 초과 %s" % (sorted(set(all_ptrs) - set(sm_ptrs))[:5], sorted(set(sm_ptrs) - set(all_ptrs))[:5]))
check(sm_ptrs == all_ptrs, "source-map 문서 순서(배열 순서) 불일치")
for n in smn:
    p = n["pointer"]
    w = W.get(p)
    if not check(w is not None, "source-map 유령 Pointer %s" % p):
        continue
    check(n["type"] == w[1], "자료형 %s" % p)
    s, e = n["literal_cp"]
    check(n["literal_byte"] == [c2b[s], c2b[e]], "literal_byte %s" % p)
    check(raw0[c2b[s]:c2b[e]].decode("utf-8") == text[s:e], "바이트↔코드포인트 %s" % p)
    check(json.loads(text[s:e]) == resolve(p), "literal 구간 원문 재현 %s" % p)
    if w[1] in ("object", "array"):
        check(n["child_count"] == w[3], "자식 수 %s" % p)
        check(n["empty_container"] == (w[3] == 0), "빈 컨테이너 표시 %s" % p)
    else:
        check(n["value"] == w[2] and type(n["value"]) is type(w[2]), "값 %s" % p)
        if w[1] == "string":
            vs, ve = n["value_cp"]
            check(text[vs:ve] == w[2], "value_cp 원문 재현 %s" % p)
            check((vs, ve) == (s + 1, e - 1), "value_cp↔literal %s" % p)
            check(n["value_byte"] == [c2b[vs], c2b[ve]], "value_byte %s" % p)
            check(n["has_escape"] == ("\\" in text[s:e]), "이스케이프 표시 %s" % p)
    if "key_literal_cp" in n:
        ks, ke = n["key_literal_cp"]
        check(json.loads(text[ks:ke]) == p.rsplit("/", 1)[1].replace("~1", "/").replace("~0", "~"), "키 구간 %s" % p)
        check(text[ke:e].lstrip().startswith(":"), "키 뒤 콜론 %s" % p)
c = sm["counts"]
check(c["nodes"] == len(walk) and c["leaf_pointers"] == len(leaf_ptrs) and c["strings"] == len(str_ptrs), "source-map counts")

# ---- coverage (구획 소유 양방향)
cov = load("coverage.json")
check(cov["source_sha256"] == sha0, "coverage 해시")
check(cov["all_node_pointers"] == all_ptrs, "coverage 전체 Pointer 목록")
check(cov["all_leaf_pointers"] == leaf_ptrs, "coverage 말단 목록")


def expect_seg(p):
    m = re.match(r"^/categories/(\d+)(/|$)", p)
    return "S%02d" % (int(m.group(1)) + 1) if m else "S00"


owner = {}
for s in cov["segments"]:
    sid = s["segment"]
    for p in s["owned_pointers"]:
        check(p not in owner, "구획 소유 중복 %s (%s, %s)" % (p, owner.get(p), sid))
        owner[p] = sid
        check(expect_seg(p) == sid, "구획 규칙 위반 %s → %s" % (p, sid))
    check(set(s["owned_leaf_pointers"]) == {p for p in s["owned_pointers"] if p in set(leaf_ptrs)}, "구획 말단 %s" % sid)
    check(s["direct_read"] == "direct_read", "직접 읽기 미완료 구획 %s (%s)" % (sid, s["direct_read"]))
    check(s["machine_extracted"] is True, "기계 추출 미완료 %s" % sid)
    check(s["last_read_pointer"] in s["owned_pointers"], "마지막 읽은 Pointer 가 구획 밖 %s" % sid)
    check(os.path.isfile(os.path.join(HERE, s["review_file"])), "구획 review 파일 없음 %s" % s["review_file"])
    check(s["manual_record"] and os.path.isfile(os.path.join(HERE, s["manual_record"])), "구획 수동 기록 없음 %s" % sid)
    for cr in s["context_refs"]:
        check(cr in W, "공동 참조 Pointer 없음 %s" % cr)
        check(cr not in s["owned_pointers"], "공동 참조가 소유로도 잡힘 %s" % cr)
check(set(owner) == set(all_ptrs), "구획 소유 합집합 ↔ 원문 불일치: 누락 %s 초과 %s" % (sorted(set(all_ptrs) - set(owner))[:5], sorted(set(owner) - set(all_ptrs))[:5]))
check(set(leaf_ptrs) <= set(owner), "말단 미배정")
check(len(cov["segments"]) == 1 + len(data["categories"]), "구획 수")
for s in cov["segments"]:
    m = json.load(open(os.path.join(HERE, s["manual_record"]), encoding="utf-8"))
    check(m["read_status"] == s["direct_read"] and m["last_read_pointer"] == s["last_read_pointer"], "coverage ↔ manual 읽기 상태 %s" % s["segment"])

# ---- morphology
mo = load("morphology.json")
check(mo["source_sha256"] == sha0, "morphology 해시")
an = mo["analyzer"]
check(an["name"] == "kiwipiepy" and an["version"] == "0.24.1" and an["model_type"] == "cong" and an["num_workers"] == 1, "분석기 설정 기록")
app = {v["pointer"]: v for v in mo["values"]}
exc = {v["pointer"]: v for v in mo["excluded"]}
check(not (set(app) & set(exc)), "적용·제외 중복")
check(set(app) | set(exc) == set(str_ptrs), "적용∪제외 ↔ 문자열 값 불일치: 누락 %s" % sorted(set(str_ptrs) - set(app) - set(exc))[:5])
for p, e in exc.items():
    check(bool(e.get("reason")) and e["value"] == W[p][2], "제외 사유/값 %s" % p)
    check(re.match(r"^/version$|^/updated$|^/categories/\d+/id$", p) is not None, "예상 밖 제외 %s" % p)
smv = {n["pointer"]: n for n in smn}
ntok = 0
for p, a in app.items():
    v = W[p][2]
    check(a["value"] == v, "형태소 입력값 %s" % p)
    check(len(a["tokens"]) > 0, "토큰 0 %s" % p)
    vs = smv[p]["value_cp"][0]
    for t in a["tokens"]:
        ntok += 1
        check(0 <= t["start"] <= t["end"] <= len(v), "토큰 구간 범위 %s" % p)
        check(v[t["start"]:t["end"]] == t["surface"], "토큰 surface 재현 %s %r" % (p, t))
        check(t["file_cp"] == [vs + t["start"], vs + t["end"]] and text[t["file_cp"][0]:t["file_cp"][1]] == t["surface"], "토큰 file_cp %s" % p)
        check(bool(t["form"]) and bool(t["tag"]), "토큰 form/tag 비어 있음 %s" % p)
    # 원문 비공백 문자는 모두 어떤 토큰 구간에 들어가야 한다(누락 검사)
    covered = set()
    for t in a["tokens"]:
        covered.update(range(t["start"], t["end"]))
    miss = [i for i, ch in enumerate(v) if not ch.isspace() and i not in covered]
    check(not miss, "형태소 미포함 문자 %s %r" % (p, [v[i] for i in miss][:5]))
check(mo["counts"]["tokens"] == ntok, "토큰 수 집계")
keys_in_src = set()
for w in walk:
    if w[0] and not re.search(r"/\d+$", w[0]):
        keys_in_src.add(w[0].rsplit("/", 1)[1])
check({f["key"] for f in mo["field_names"]} == keys_in_src, "필드명 적용/제외 기록 ↔ 원문 키 집합")
for k in mo["known_missegmentation"]:
    p = k["pointer"]
    check(p in app, "오분절 기록 Pointer %s" % p)
    v = W[p][2]
    s, e = k["span"]
    check(v[s:e] == k["surface"], "오분절 구간 재현 %s" % p)
    toks = " ".join("%s/%s" % (t["form"], t["tag"]) for t in app[p]["tokens"] if t["start"] < e and t["end"] > s or (t["start"] == t["end"] and s <= t["start"] <= e))
    check(k["observed_analysis"] in toks, "오분절 관찰 분석이 원시 토큰과 불일치 %s %s" % (p, k["surface"]))

# ---- expressions
ex = load("expressions.json")
check(ex["source_sha256"] == sha0, "expressions 해시")
seen = set()
expr_ptrs = set()
for x in ex["expressions"]:
    p = x["pointer"]
    if not check(p in W and W[p][1] == "string", "표현 Pointer %s" % p):
        continue
    v = W[p][2]
    s, e = x["span_in_value"]
    check(v[s:e] == x["text"], "표현 구간 재현 %s %r" % (x["id"], x["text"]))
    vs = smv[p]["value_cp"][0]
    check(x["file_cp"] == [vs + s, vs + e] and text[vs + s:vs + e] == x["text"], "표현 file_cp %s" % x["id"])
    check(x["file_byte"] == [c2b[vs + s], c2b[vs + e]] and raw0[x["file_byte"][0]:x["file_byte"][1]].decode("utf-8") == x["text"], "표현 file_byte %s" % x["id"])
    check((p, s, e) not in seen, "표현 중복 생성 %s %s" % (x["id"], x["text"]))
    seen.add((p, s, e))
    check(owner.get(p) == x["segment"], "표현 구획 %s" % x["id"])
    check(set(x["facets"]) <= set(ex["facet_vocabulary"]), "정의 없는 facet %s %s" % (x["id"], x["facets"]))
    expr_ptrs.add(p)
check(set(app) <= expr_ptrs, "직접 읽기 표현이 없는 언어 값: %s" % sorted(set(app) - expr_ptrs)[:5])
# 각 언어 값의 모든 문장(종결부호 단위 또는 값 전체)이 표현 기록으로 덮였는지 — 문장 탈락 검사
for p in app:
    v = W[p][2]
    spans = [x["span_in_value"] for x in ex["expressions"] if x["pointer"] == p]
    nonspace = [i for i, ch in enumerate(v) if not ch.isspace()]
    unc = [i for i in nonspace if not any(s <= i < e for s, e in spans)]
    # 괄호·구분 기호만 남는 것은 허용하지 않는다 — 모든 비공백 문자가 어떤 표현 안에 있어야 한다
    check(not unc, "표현 기록에 덮이지 않은 원문 문자 %s %r" % (p, "".join(v[i] for i in unc)[:40]))
rc = ex["regex_candidates"]
for r in rc:
    v = W[r["pointer"]][2]
    s, e = r["span_in_value"]
    check(v[s:e] == r["match"], "정규식 후보 구간 %s" % r["id"])
    if not r["covered_by_manual_phrase"]:
        check(r.get("review") in ("covered_by_sentence_only", "false_positive"), "정규식 후보 미판정 %s" % r["id"])
    check(bool(r["covered_by_manual_any"]), "정규식 후보가 어떤 수동 기록에도 없음 %s" % r["id"])
check("패턴 일치분뿐" in ex["method"]["regex"], "정규식 한계 문구")

# ---- observations / issues / review 문서 대조
ob = load("observations.json")
issues = open(os.path.join(HERE, "issues.md"), encoding="utf-8").read()
for o in ob["observations"]:
    check(o["pointer"] in W, "관찰 Pointer %s" % o["id"])
    check(o["status"] in "ABCFIKP", "관찰 상태 %s" % o["id"])
    check(o["id"] in issues, "issues.md 에 관찰 없음 %s" % o["id"])
check(sum(1 for o in ob["observations"] if o["status"] == "C") == 0 or "C" in issues, "C 표시")
for i, k in enumerate(mo["known_missegmentation"], 1):
    check(("| K%d | `%s` | %s |" % (i, k["pointer"], k["surface"])) in issues, "issues.md 오분절 K%d" % i)
review = open(os.path.join(HERE, "review.md"), encoding="utf-8").read()
for s in cov["segments"]:
    check("review-part-%s.md" % s["segment"] in review, "review.md 목차에 %s 없음" % s["segment"])
    part = open(os.path.join(HERE, s["review_file"]), encoding="utf-8").read()
    for p in s["owned_pointers"]:
        row = "| `%s` |" % (p or "/")
        check(row in part, "review-part 에 Pointer 행 없음 %s" % p)
        w = W[p]
        if w[1] not in ("object", "array"):
            lit = json.dumps(w[2], ensure_ascii=False).replace("|", "\\|")
            line = next((ln for ln in part.splitlines() if ln.startswith(row)), "")
            check(lit in line, "review-part 원문 값 불일치 %s" % p)
            key = p.rsplit("/", 1)[1]
            check(("| %s |" % (key if not key.isdigit() else "[%s]" % key)) in line, "review-part 원본 컬럼명 %s" % p)
    for x in ex["expressions"]:
        if x["segment"] == s["segment"]:
            check(("| %s |" % x["id"]) in part, "review-part 표현 %s" % x["id"])
    for o in ob["observations"]:
        if o["segment"] == s["segment"]:
            check(("| %s |" % o["id"]) in part, "review-part 관찰 %s" % o["id"])
for fp in sorted({re.sub(r"/\d+", "/*", p) or "/" for p in all_ptrs}):
    check(("| `%s` |" % fp) in review, "컬럼 구성 표에 경로 패턴 없음 %s" % fp)

# ---- 변이 시험: 검사가 실제로 잡는지(메모리 안에서만)
def owners_ok(segs):
    o = {}
    for s in segs:
        for p in s["owned_pointers"]:
            if p in o:
                return False
            o[p] = 1
    return set(o) == set(all_ptrs)


m1 = copy.deepcopy(cov["segments"])
m1[5]["owned_pointers"] = m1[5]["owned_pointers"][:-1]
m2 = copy.deepcopy(cov["segments"])
m2[2]["owned_pointers"].append(m2[3]["owned_pointers"][0])
x0 = ex["expressions"][100]
v0 = W[x0["pointer"]][2]
mut_span_detected = v0[x0["span_in_value"][0] + 1:x0["span_in_value"][1] + 1] != x0["text"]
check(owners_ok(cov["segments"]) and not owners_ok(m1) and not owners_ok(m2) and mut_span_detected, "변이 시험(누락·중복·구간 이동) 검출 실패")

# ---- 원본 불변(끝)
sha1 = hashlib.sha256(open(SRC, "rb").read()).hexdigest()
check(sha1 == sha0, "원본 해시 변경(끝)")

print("source_sha256 start=%s end=%s" % (sha0, sha1))
print("nodes=%d leaf=%d strings=%d segments=%d applied=%d excluded=%d tokens=%d expressions=%d regex=%d known_missegmentation=%d observations=%d" % (
    len(walk), len(leaf_ptrs), len(str_ptrs), len(cov["segments"]), len(app), len(exc), ntok, len(ex["expressions"]), len(rc), len(mo["known_missegmentation"]), len(ob["observations"])))
print("checks=%d failures=%d" % (checks, len(fails)))
for f in fails[:50]:
    print("FAIL:", f)
sys.exit(1 if fails else 0)
