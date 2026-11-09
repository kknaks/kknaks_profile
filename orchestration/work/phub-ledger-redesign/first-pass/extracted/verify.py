#!/usr/bin/env python3
"""extracted.json 1차 조사 결과 — 독립 검증.

레포 루트에서:  python3 orchestration/work/phub-ledger-redesign/first-pass/extracted/verify.py
(선택) --results DIR  다른 결과 폴더(변이 시험용) · --source FILE  다른 원본
원본·결과를 읽기만 한다. 아무 파일도 쓰지 않는다. 실패가 하나라도 있으면 exit 1.
build.py 의 스캐너를 쓰지 않고 표준 json 파서(object_pairs_hook)로 원문을 다시 열거한다.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/extracted.json"
EXPECTED_SHA = "b829d499e3e3fd7f6119f2dc23092cf50f7c13e57ee18e9d3131a14c7e350f2c"

ap = argparse.ArgumentParser()
ap.add_argument("--results", default=str(HERE))
ap.add_argument("--source", default=str(ROOT / SRC_REL))
args = ap.parse_args()
R = Path(args.results)
SRC = Path(args.source)

fails = []
checks = []


def check(name, ok, detail=""):
    checks.append((name, bool(ok)))
    if not ok:
        fails.append(f"{name}: {detail}")


def load(name):
    return json.loads((R / name).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- 원본
raw0 = SRC.read_bytes()
h_start = hashlib.sha256(raw0).hexdigest()
check("source.sha256 = 기대값", h_start == EXPECTED_SHA, h_start)
text = raw0.decode("utf-8")

dups = []


def hook(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            dups.append(k)
        seen.add(k)
    return {"__pairs__": pairs}


tree = json.loads(text, object_pairs_hook=hook)
check("원본 중복 키 0", not dups, dups)

truth = {}  # pointer -> (type, value or len, keys)


def esc(k):
    return k.replace("~", "~0").replace("/", "~1")


def walk(x, ptr):
    if isinstance(x, dict) and "__pairs__" in x:
        ks = [k for k, _ in x["__pairs__"]]
        truth[ptr] = ("object", len(ks), ks)
        for k, v in x["__pairs__"]:
            walk(v, ptr + "/" + esc(k))
    elif isinstance(x, list):
        truth[ptr] = ("array", len(x), None)
        for i, v in enumerate(x):
            walk(v, f"{ptr}/{i}")
    else:
        t = {str: "string", bool: "boolean", int: "number", float: "number", type(None): "null"}[type(x)]
        truth[ptr] = (t, x, None)


walk(tree, "")
leaves_truth = {p for p, (t, v, _) in truth.items() if t not in ("object", "array") or v == 0}

# ---------------------------------------------------------------- 결과 파일 실재
required = ["review.md", "source-map.json", "morphology.json", "expressions.json", "issues.md", "validation.md",
            "coverage.json", "build.py", "verify.py", "manual-expressions.json", "manual-observations.json",
            "segmentation-review.json", "reading-log.json"]
for f in required:
    check(f"파일 실재 {f}", (R / f).exists(), f)
if any(x.startswith("파일 실재") for x in fails):
    print("\n".join(fails))
    sys.exit(1)

sm = load("source-map.json")
mo = load("morphology.json")
ex = load("expressions.json")
cov = load("coverage.json")
mexp = load("manual-expressions.json")
mobs = load("manual-observations.json")
segr = load("segmentation-review.json")

# ---------------------------------------------------------------- source-map 양방향
check("source-map.sha256 = 원본", sm["source"]["sha256"] == h_start)
check("source-map.bytes = 원본", sm["source"]["bytes"] == len(raw0))
check("source-map.code_points = 원본", sm["source"]["code_points"] == len(text))
nodes = sm["nodes"]
ptrs = [n["pointer"] for n in nodes]
check("source-map Pointer 중복 0", len(ptrs) == len(set(ptrs)), len(ptrs) - len(set(ptrs)))
missing = set(truth) - set(ptrs)
extra = set(ptrs) - set(truth)
check("원문 경로 → source-map 누락 0", not missing, sorted(missing)[:5])
check("source-map → 원문 없는 경로 0", not extra, sorted(extra)[:5])
check("노드 순서 = 원문 문서 순서", ptrs == list(truth), "order")
b_of = [0]
for ch in text:
    b_of.append(b_of[-1] + len(ch.encode("utf-8")))
bad_val = bad_span = bad_byte = bad_key = 0
for n in nodes:
    t, v, ks = truth[n["pointer"]]
    if n["type"] != t:
        bad_val += 1
        continue
    if t in ("object", "array"):
        if n["length"] != v or (t == "object" and n["keys"] != ks):
            bad_val += 1
    else:
        if n["value"] != v or type(n["value"]) is not type(v):
            bad_val += 1
    s, e = n["span"]
    lit = text[s:e]
    try:
        dec = json.loads(lit, object_pairs_hook=lambda p: {"__pairs__": p})
    except Exception:
        bad_span += 1
        continue
    if t not in ("object", "array"):
        if dec != v or lit != n["literal"]:
            bad_span += 1
    else:
        if (t == "array" and not lit.startswith("[")) or (t == "object" and not lit.startswith("{")):
            bad_span += 1
    if n["byte_span"] != [b_of[s], b_of[e]] or raw0[n["byte_span"][0]:n["byte_span"][1]].decode("utf-8") != lit:
        bad_byte += 1
    if t == "string":
        vs, ve = n["value_span"]
        if (vs, ve) != (s + 1, e - 1) or (n["decoded_equals_literal_inner"] != (text[vs:ve] == v)):
            bad_span += 1
    if n["key"] is not None:
        ks_, ke_ = n["key_span"]
        if json.loads(text[ks_:ke_]) != n["key"]:
            bad_key += 1
check("값·자료형·길이·키 순서 원문 일치", bad_val == 0, bad_val)
check("span 원문 재현(리터럴 디코드 = 값)", bad_span == 0, bad_span)
check("byte_span 원문 재현", bad_byte == 0, bad_byte)
check("key_span 원문 재현", bad_key == 0, bad_key)
fo = sm["field_name_occurrences"]
occ_ptrs = sorted(p for v in fo.values() for p in [o["pointer"] for o in v])
true_keyed = sorted(p for p in truth if p != "" and not p.split("/")[-1].isdigit())
check("필드명 출현 = 원문 키 출현(양방향)", occ_ptrs == true_keyed, (len(occ_ptrs), len(true_keyed)))

# ---------------------------------------------------------------- coverage 양방향
secs = cov["sections"]
owned = [p for s in secs for p in s["owned_pointers"]]
check("coverage 소유 Pointer 중복 0", len(owned) == len(set(owned)), len(owned) - len(set(owned)))
check("원문 경로 → coverage 소유 누락 0", not (set(truth) - set(owned)), sorted(set(truth) - set(owned))[:5])
check("coverage 소유 → 원문 없는 경로 0", not (set(owned) - set(truth)), sorted(set(owned) - set(truth))[:5])
own_leaves = [p for s in secs for p in s["owned_leaf_pointers"]]
check("원문 말단(빈 컨테이너 포함) = 구획 소유 말단 합집합", sorted(own_leaves) == sorted(leaves_truth),
      (len(own_leaves), len(leaves_truth)))
for s in secs:
    check(f"coverage {s['id']} 직접 읽음", s["direct_read"] == "직접 읽음", s["direct_read"])
    check(f"coverage {s['id']} review 파일 실재", (R / s["review_file"]).exists(), s["review_file"])
    for c in s["context_refs"]:
        if c.startswith("("):
            continue
        check(f"coverage {s['id']} 문맥 참조 실재 {c}", c in truth, c)
    if s["id"] != "S00":
        pre = s["pointer_prefix"]
        check(f"coverage {s['id']} 소유 = 접두 범위 전체",
              set(s["owned_pointers"]) == {p for p in truth if p == pre or p.startswith(pre + "/")}, pre)
check("coverage 남은 구획 0", cov["remaining_sections"] == [], cov["remaining_sections"])
check("coverage 원본 해시", cov["source"]["sha256"] == h_start)

# ---------------------------------------------------------------- review 분할 문서 대조
sec_of = {p: s for s in secs for p in s["owned_pointers"]}


def md(v):
    return str(v).replace("|", "\\|")


rev_text = {}
for s in secs:
    rev_text[s["review_file"]] = (R / s["review_file"]).read_text(encoding="utf-8")
miss_rev = []
for p, (t, v, ks) in truth.items():
    s = sec_of.get(p)
    if s is None:
        miss_rev.append(p + " (담당 구획 없음)")
        continue
    doc = rev_text[s["review_file"]]
    shown = '`""`' if p == "" else f"`{p}`"
    rows = [ln for ln in doc.splitlines() if ln.startswith("|") and shown in ln.split("|")[3 if p else 3]]
    if p == "":
        rows = [ln for ln in doc.splitlines() if ln.startswith("| 1 | (루트) | `\"\"`")]
    if not rows:
        miss_rev.append(p)
        continue
    row = rows[0]
    if t == "string" and f"| {md(v)} |" not in row:
        miss_rev.append(p)
    elif t == "null" and "| null |" not in row:
        miss_rev.append(p)
    elif t in ("object", "array") and f"{t} · {v}" not in row:
        miss_rev.append(p)
    if p and t != "object" or (p and t == "object"):
        fp = None
        parts = p.split("/")[2:]
        if parts:
            fp = ""
            for q in parts:
                fp += f"[{q}]" if q.isdigit() else (("." if fp else "") + q)
            if f"`{fp}`" not in row:
                miss_rev.append(p + " (원본 컬럼명)")
check("모든 원문 노드가 담당 review 파일에 Pointer·원본 컬럼명·원문 값으로 실림", not miss_rev, miss_rev[:5])
rv = (R / "review.md").read_text(encoding="utf-8")
for s in secs:
    if s["id"] != "S00":
        check(f"review.md 목차 → {s['review_file']}", f"(./{s['review_file']})" in rv, s["review_file"])
check("review.md 상태에 1차 범위·원장 전체 완료 아님 표기", "1차 범위" in rv and "원장 전체 완료 아님" in rv)
check("review.md 미치환 자리표시 0", "{{" not in rv)

# ---------------------------------------------------------------- 형태소 적용/제외
strings = {p for p, (t, v, _) in truth.items() if t == "string"}
an = {a["pointer"]: a for a in mo["analyzed"]}
exl = {e["pointer"]: e for e in mo["excluded"]}
check("분석·제외 겹침 0", not (set(an) & set(exl)), sorted(set(an) & set(exl))[:5])
check("말단 → 분석 또는 제외 누락 0", not (leaves_truth - set(an) - set(exl)), sorted(leaves_truth - set(an) - set(exl))[:5])
check("분석·제외 → 원문 말단 아닌 것 0", not ((set(an) | set(exl)) - leaves_truth), sorted((set(an) | set(exl)) - leaves_truth)[:5])
check("제외마다 사유 기록", all(e.get("reason") for e in mo["excluded"]))
EXCL_KEYS = {"procedure_id", "extracted_at", "updated", "guardrail_version", "source_type"}
bad_rule = [p for p in strings if (p.split("/")[-1] in EXCL_KEYS) != (p in exl)]
check("제외 규칙(코드·날짜·버전·열거 키)과 실제 제외 일치", not bad_rule, bad_rule[:5])
bad_tok = 0
for p, a in an.items():
    v = truth[p][1]
    if a["value"] != v:
        bad_tok += 1
    for t in a["tokens"]:
        s, e = t["span"]
        if not (0 <= s <= e <= len(v)) or v[s:e] != t["surface"]:
            bad_tok += 1
check("형태소 토큰 surface = 값[span]", bad_tok == 0, bad_tok)
an_cfg = mo["analyzer"]
check("분석기 설정 기록(kiwipiepy 0.24.1 · cong · 스레드 1)",
      an_cfg.get("kiwipiepy") == "0.24.1" and an_cfg.get("model_type") == "cong" and an_cfg.get("num_workers") == 1, an_cfg)
check("코드 포인트 = UTF-16 단위(BMP 밖 0)", all(ord(c) <= 0xFFFF for c in text))
fn = {f["field_name"] for f in mo["field_names"]}
check("필드명 분석 = 원문 서로 다른 키", fn == set(fo), (fn ^ set(fo)))
# 오분절 표시 ↔ 토큰
bad_seg = 0
for r in segr["occurrences"]:
    v = truth[r["pointer"]][1]
    s, e = r["span"]
    if v[s:e] != r["text"]:
        bad_seg += 1
        continue
    toks = [t for t in an[r["pointer"]]["tokens"] if t["span"][0] < e and t["span"][1] > s]
    if [f"{t['form']}/{t['tag']}" for t in toks] != r["raw_tokens"]:
        bad_seg += 1
    if not all(r["id"] in t.get("review_marks", []) for t in toks):
        bad_seg += 1
check("오분절 표시 원문·원시 토큰·토큰 표시 대응", bad_seg == 0, bad_seg)
marked_tok_ids = {m for a in mo["analyzed"] for t in a["tokens"] for m in t.get("review_marks", [])}
check("토큰 표시 → 오분절 기록 실재", marked_tok_ids == {r["id"] for r in segr["occurrences"]}, marked_tok_ids ^ {r["id"] for r in segr["occurrences"]})
check("morphology 표시 수 = segmentation-review", len(mo["segmentation_review"]) == len(segr["occurrences"]))

# ---------------------------------------------------------------- 표현
bad_ex = 0
dupk = set()
dup = 0
ids = set()
for e in ex["expressions"]:
    p = e["pointer"]
    if p not in strings:
        bad_ex += 1
        continue
    v = truth[p][1]
    s, z = e["span"]
    if not (0 <= s <= z <= len(v)) or v[s:z] != e["text"]:
        bad_ex += 1
    if e["section"] != (sec_of.get(p) or {}).get("id"):
        bad_ex += 1
    k = (p, s, z, e["category_candidate"])
    if k in dupk:
        dup += 1
    dupk.add(k)
    ids.add(e["id"])
check("표현 후보 text = 값[span] · 구획 일치", bad_ex == 0, bad_ex)
check("표현 후보 (Pointer,구간,범주) 중복 생성 0", dup == 0, dup)
check("표현 후보 ID 유일", len(ids) == len(ex["expressions"]))
segval = {e["pointer"] for e in ex["expressions"] if e["category_candidate"] == "segment.value"}
check("모든 문자열 값에 segment.value 후보", segval == strings, len(strings - segval))
mids = {e.get("manual_id") for e in ex["expressions"] if e.get("manual_id")}
check("수동 표현 전부 expressions 에 배치", mids == {m["id"] for m in mexp["expressions"]}, len(mids))
bad_m = [m["id"] for m in mexp["expressions"] if m["text"] not in truth.get(m["pointer"], ("", ""))[1]]
check("수동 표현 원문 실재", not bad_m, bad_m)
bad_q = 0
for e in ex["expressions"]:
    if e["category_candidate"] == "quantity_unit_time" and re.search(r"[A-Za-z]\d|\d[A-Za-z]", re.sub(r"(?<=\d)mm\b", "", e["text"])):
        bad_q += 1
check("수량 후보에 코드 속 숫자(G6PD 등) 0 — 단위 mm 는 허용", bad_q == 0, bad_q)

# ---------------------------------------------------------------- 관찰
bad_o = []
oids = set()
for o in mobs["observations"]:
    oids.add(o["id"])
    for ev in o["evidence"]:
        if ev["pointer"] not in truth:
            bad_o.append(o["id"])
        elif ev.get("quote"):
            t, v, _ = truth[ev["pointer"]]
            if t != "string" or ev["quote"] not in v:
                bad_o.append(o["id"])
check("관찰 근거 Pointer·인용 원문 실재", not bad_o, bad_o[:5])
check("관찰 ID 유일", len(oids) == len(mobs["observations"]))
for s in secs:
    doc = rev_text[s["review_file"]]
    for oid in s["manual_observation_ids"]:
        if f"**{oid}**" not in doc:
            fails.append(f"관찰 {oid} 가 {s['review_file']} 에 없음")
    if s["id"] != "S00":
        for mid in s["manual_expression_ids"]:
            if f"| {mid} |" not in doc:
                fails.append(f"수동 표현 {mid} 가 {s['review_file']} 에 없음")
        for rid in s["segmentation_review_ids"]:
            if f"| {rid} |" not in doc:
                fails.append(f"오분절 {rid} 가 {s['review_file']} 에 없음")
checks.append(("관찰·수동 표현·오분절이 담당 review 파일에 실림", True))
iss = (R / "issues.md").read_text(encoding="utf-8")
refs = {r for o in mobs["observations"] for r in o.get("issue_refs", [])}
miss_ref = [r for r in refs if f"**{r}**" not in iss]
check("관찰이 가리키는 미결 ID 가 issues.md 에 실재", not miss_ref, miss_ref)

# ---------------------------------------------------------------- 별도 읽기 검토 보조 기록
rr = load("reading-review-uncovered.json")
bad_rr = [u["pointer"] for u in rr["uncovered"] + rr["marker_hits"]
          if u["pointer"] not in strings or truth[u["pointer"]][1][u["span"][0]:u["span"][1]] != u["text"]]
check("읽기 검토 미포착 어절 기록 원문 재현", not bad_rr, bad_rr[:5])

# ---------------------------------------------------------------- 해시 끝
h_end = hashlib.sha256(SRC.read_bytes()).hexdigest()
check("원본 해시 시작 = 끝", h_start == h_end, h_end)

print(f"source sha256 start={h_start} end={h_end}")
print(f"원문 노드 {len(truth)} · 말단 {len(leaves_truth)} · 문자열 {len(strings)} · 구획 {len(secs)} · 분석 {len(an)} · 제외 {len(exl)} · "
      f"표현 {len(ex['expressions'])} · 관찰 {len(mobs['observations'])} · 오분절 표시 {len(segr['occurrences'])}")
print(f"checks={len(checks)} failures={len(fails)}")
for f in fails:
    print("FAIL", f)
sys.exit(1 if fails else 0)
