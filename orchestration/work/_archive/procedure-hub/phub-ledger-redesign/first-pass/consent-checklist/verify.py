"""consent-checklist 1차 수집 독립 검증. 원본과 결과 파일을 읽기만 한다(쓰기 없음).

실행(레포 루트): python3 orchestration/work/phub-ledger-redesign/first-pass/consent-checklist/verify.py
  --selftest : 메모리 안에서 결과를 일부러 망가뜨려 검출되는지 확인(파일 변경 없음)
실패가 하나라도 있으면 exit 1.
build.py 를 import 하지 않는다. 원본 구조는 json 표준 파서(object_pairs_hook)로 따로 열거한다.
"""
import copy
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "../../../phub-recommend/bronze/phub-ledger/consent-checklist.json"))
EXPECTED_SHA = "4e138ffb64414995483e4201396bc4f185ec34e4d150f825ec151b0fe07512e5"
REQUIRED = ["review.md", "source-map.json", "morphology.json", "expressions.json", "issues.md", "validation.md",
            "coverage.json", "build.py", "manual-observations.json", "manual-expressions.json",
            "segmentation-review.json", "expression-review.json"]


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f) if name.endswith(".json") else f.read()


def esc(seg):
    return str(seg).replace("~", "~0").replace("/", "~1")


def enumerate_source(raw):
    dups = []

    def hook(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                dups.append(k)
            seen.add(k)
        return dict(pairs)

    data = json.loads(raw.decode("utf-8"), object_pairs_hook=hook)
    nodes = {}

    def walk(x, ptr):
        if isinstance(x, dict):
            nodes[ptr] = ("object", len(x), None)
            for k, v in x.items():
                walk(v, ptr + "/" + esc(k))
        elif isinstance(x, list):
            nodes[ptr] = ("array", len(x), None)
            for i, v in enumerate(x):
                walk(v, f"{ptr}/{i}")
        else:
            t = "string" if isinstance(x, str) else "boolean" if isinstance(x, bool) else "null" if x is None else "number"
            nodes[ptr] = (t, None, x)

    walk(data, "")
    return data, nodes, dups


def resolve(data, ptr):
    if ptr == "":
        return data
    cur = data
    for seg in ptr[1:].split("/"):
        seg = seg.replace("~1", "/").replace("~0", "~")
        cur = cur[int(seg)] if isinstance(cur, list) else cur[seg]
    return cur


def run_checks(raw, R):
    fails = []
    stats = {}

    def check(cond, msg):
        if not cond:
            fails.append(msg)

    sha = hashlib.sha256(raw).hexdigest()
    check(sha == EXPECTED_SHA, f"원본 해시 불일치 {sha}")
    data, src_nodes, dups = enumerate_source(raw)
    text = raw.decode("utf-8")
    check(not dups, f"원본 중복 키 {dups}")

    # 1. source-map ↔ 원본 양방향
    sm = R["source-map.json"]
    check(sm["source"]["sha256"] == sha, "source-map 해시 불일치")
    check(sm["source"]["size_bytes"] == len(raw), "source-map 크기 불일치")
    sm_ptrs = [n["pointer"] for n in sm["nodes"]]
    check(len(sm_ptrs) == len(set(sm_ptrs)), "source-map Pointer 중복")
    check(set(sm_ptrs) == set(src_nodes), f"source-map↔원본 Pointer 차이 누락={sorted(set(src_nodes)-set(sm_ptrs))[:5]} 초과={sorted(set(sm_ptrs)-set(src_nodes))[:5]}")
    # 원본 순서(문서 순서) 유지
    check(sm_ptrs == list(src_nodes), "source-map 노드 순서가 원본 순서와 다름")
    for n in sm["nodes"]:
        p = n["pointer"]
        if p not in src_nodes:
            continue
        t, ln, v = src_nodes[p]
        check(n["type"] == t, f"{p} 자료형 {n['type']}≠{t}")
        if ln is not None:
            check(n.get("length") == ln, f"{p} 길이 불일치")
        else:
            check(n.get("value") == v and type(n.get("value")) is type(v), f"{p} 값 불일치")
        a, b = n["literal_cp"]
        ba, bb = n["literal_byte"]
        lit = text[a:b]
        check(raw[ba:bb].decode("utf-8") == lit, f"{p} 바이트/코드포인트 구간 불일치")
        try:
            check(json.loads(lit) == resolve(data, p), f"{p} 리터럴 구간 재현 실패")
        except Exception as ex:
            fails.append(f"{p} 리터럴 파싱 실패 {ex}")
        if n["leaf"]:
            check(n.get("literal") == lit, f"{p} literal 칸 불일치")
    for k in sm["key_occurrences"]:
        a, b = k["literal_cp"]
        check(json.loads(text[a:b]) == k["key"], f"키 구간 재현 실패 {k['member_pointer']}")
        check(k["member_pointer"] in src_nodes, f"키 Pointer 없음 {k['member_pointer']}")
    n_members = sum(ln for p, (t, ln, v) in src_nodes.items() if t == "object")
    check(len(sm["key_occurrences"]) == n_members, "키 출현 수 ≠ 객체 멤버 수")
    stats["nodes"] = len(src_nodes)
    stats["leaves"] = sum(1 for t, ln, v in src_nodes.values() if ln is None)

    # 2. coverage: 소유 합집합 = 전체, 중복 없음, 상태·리뷰 실재
    cov = R["coverage.json"]
    owned = [p for s in cov["sections"] for p in s["owned"]]
    check(len(owned) == len(set(owned)), f"구획 소유 중복 {[p for p in set(owned) if owned.count(p) > 1][:5]}")
    check(set(owned) == set(src_nodes), f"구획 소유↔원본 차이 누락={sorted(set(src_nodes)-set(owned))[:5]} 초과={sorted(set(owned)-set(src_nodes))[:5]}")
    review = R["review.md"]
    obs = R["manual-observations.json"]
    for s in cov["sections"]:
        check(s["read_status"] == "직접 읽음", f"{s['id']} 읽기 상태 {s['read_status']}")
        check(obs["sections"].get(s["id"], {}).get("read_status") == s["read_status"], f"{s['id']} 읽기 기록 불일치")
        check(os.path.exists(os.path.join(HERE, s["review_file"])), f"{s['id']} 리뷰 파일 없음")
        check(f"\n## {s['id']}\n" in review, f"{s['id']} 리뷰 절 없음")
        for c in s["context"]:
            check(c in src_nodes, f"{s['id']} 문맥 Pointer 없음 {c}")
    check(set(obs["sections"]) == {s["id"] for s in cov["sections"]}, "관찰 기록 구획 ≠ coverage 구획")
    check(obs["last_read"]["remaining_sections"] == [], "남은 구획이 있음")

    # 3. review.md: 모든 노드 행 + 말단 원문 값 그대로
    rows = {}
    for line in review.splitlines():
        m = re.match(r"^\| `([^`]*)` \| `([^`]*)` \| ([^|]+) \| (.*) \|$", line)
        if m:
            rows.setdefault(m.group(2), []).append((m.group(1), m.group(4)))
    for p, (t, ln, v) in src_nodes.items():
        key = p or "(루트)"
        check(len(rows.get(key, [])) == 1, f"review 행 수 {key} = {len(rows.get(key, []))}")
        if rows.get(key) and ln is None:
            col, cellv = rows[key][0]
            check(cellv.replace("\\|", "|") == str(v), f"review 원문 값 불일치 {p}")
            last = p.rsplit("/", 1)[1]
            if last.isdigit():
                parent = p.rsplit("/", 2)[1]
                check(col == f"{parent}[{last}]", f"review 컬럼명 {col} ≠ 원본 {parent}[{last}]")
            else:
                check(col == last, f"review 컬럼명 {col} ≠ 원본 {last}")
    for sid, o in obs["sections"].items():
        for ob in o["observations"]:
            try:
                v = resolve(data, ob["pointer"])
            except Exception:
                fails.append(f"관찰 Pointer 없음 {ob['pointer']}")
                continue
            check(isinstance(v, str) and ob["quote"] in v, f"관찰 인용 불일치 {sid} {ob['pointer']}")
            sec = next((s for s in cov["sections"] if ob["pointer"] in s["owned"]), None)
            check(sec is not None and sec["id"] == sid, f"관찰 구획 귀속 오류 {sid} {ob['pointer']}")

    # 4. morphology: 적용∪제외 = 말단 전체, 구간 재현, 문자 덮기
    mo = R["morphology.json"]
    leaves = {p for p, (t, ln, v) in src_nodes.items() if ln is None}
    applied = [r["pointer"] for r in mo["records"]]
    excl = [e["pointer"] for e in mo["excluded"] if "pointer" in e]
    check(len(applied) == len(set(applied)), "형태소 적용 중복")
    check(not set(applied) & set(excl), "적용·제외 겹침")
    check(set(applied) | set(excl) == leaves, f"적용∪제외 ≠ 말단 누락={sorted(leaves-set(applied)-set(excl))[:5]}")
    for e in mo["excluded"]:
        check(bool(e.get("reason")), f"제외 사유 없음 {e}")
    fnames = {k["key"] for k in sm["key_occurrences"]}
    check({e["field_name"] for e in mo["excluded"] if "field_name" in e} == fnames, "필드명 적용/제외 기록 누락")
    tok_total = 0
    for r in mo["records"]:
        v = resolve(data, r["pointer"])
        check(r["value"] == v, f"형태소 값 불일치 {r['pointer']}")
        covered = [False] * len(v)
        for t in r["tokens"]:
            tok_total += 1
            s, e = t["start"], t["end"]
            check(0 <= s < e <= len(v), f"토큰 구간 범위 밖 {r['pointer']} {t}")
            check(t["surface"] == v[s:e], f"토큰 surface 불일치 {r['pointer']} {t['i']}")
            for k in range(s, min(e, len(v))):
                covered[k] = True
        miss = [i for i, ch in enumerate(v) if not covered[i] and not ch.isspace()]
        check(not miss, f"토큰이 덮지 않은 문자 {r['pointer']} {[v[i] for i in miss][:5]}")
    check(tok_total == mo["token_count"], "토큰 수 불일치")
    stats["tokens"] = tok_total
    # 알려진 오분절: 서명 재매칭 = 기록
    seg = R["segmentation-review.json"]
    recs = {r["pointer"]: r for r in mo["records"]}
    rec_occ = {(o["signature"], o["pointer"], o["start"], o["end"]) for o in mo["known_segmentation_issues"]["occurrences"]}
    re_occ = set()
    for sg in seg["signatures"]:
        seq = [tuple(x) for x in sg["seq"]]
        n = 0
        for r in mo["records"]:
            T = r["tokens"]
            for i in range(len(T) - len(seq) + 1):
                if all((T[i+k]["form"], T[i+k]["tag"]) == seq[k] for k in range(len(seq))):
                    if "context_prev_tag" in sg and not (i > 0 and T[i-1]["tag"] == sg["context_prev_tag"]):
                        continue
                    n += 1
                    re_occ.add((sg["id"], r["pointer"], T[i]["start"], T[i+len(seq)-1]["end"]))
        check(n == sg["expected_occurrences"], f"오분절 서명 {sg['id']} 출현 {n}≠{sg['expected_occurrences']}")
    check(re_occ == rec_occ, "오분절 출현 기록 ≠ 재매칭")
    for o in mo["known_segmentation_issues"]["occurrences"]:
        v = recs[o["pointer"]]["value"]
        check(v[o["start"]:o["end"]] == o["surface"], f"오분절 구간 재현 실패 {o}")
    stats["known_segmentation_occurrences"] = len(rec_occ)

    # 5. expressions: 구간 재현, 완전 중복 없음, 수동·검토 규칙 반영
    ex = R["expressions.json"]["items"]
    ids = [x["id"] for x in ex]
    check(len(ids) == len(set(ids)), "표현 ID 중복")
    keyset = [(x["pointer"], x["start"], x["end"], x["category"], x["method"]) for x in ex]
    check(len(keyset) == len(set(keyset)), "표현 완전 중복(pointer·구간·범주·방법)")
    for x in ex:
        try:
            v = resolve(data, x["pointer"])
        except Exception:
            fails.append(f"표현 Pointer 없음 {x['id']}")
            continue
        check(x["pointer"] in applied, f"표현이 분석 제외 값에 있음 {x['id']}")
        check(0 <= x["start"] < x["end"] <= len(v) and v[x["start"]:x["end"]] == x["text"], f"표현 구간 재현 실패 {x['id']}")
    man = R["manual-expressions.json"]["items"]
    man_out = {x.get("manual_id") for x in ex if x["method"] == "manual:direct_read"}
    check(man_out == {m["id"] for m in man}, "수동 표현 누락/초과")
    exr = R["expression-review.json"]["rules"]
    for rule in exr:
        hit = [x for x in ex if any(rv["rule"] == rule["id"] for rv in x.get("review", []))]
        check(len(hit) == rule["expected_matches"], f"표현 검토 규칙 {rule['id']} 반영 {len(hit)}")
        for x in hit:
            check(x["method"] == rule["method"] and x["pointer"] == rule["pointer"] and x["start"] == rule["start"], f"규칙 {rule['id']} 대상 불일치")
    # 문장 단위 후보가 모든 분석 값의 비공백 문자를 덮는다
    for p in applied:
        v = resolve(data, p)
        cov_c = [False] * len(v)
        for x in ex:
            if x["pointer"] == p and x["category"] == "sentence_or_value":
                for k in range(x["start"], x["end"]):
                    cov_c[k] = True
        check(all(cov_c[i] or v[i].isspace() for i in range(len(v))), f"문장 후보가 값을 다 덮지 않음 {p}")
    stats["expressions"] = len(ex)

    # 6. 산출 파일 실재 + 다른 위치 파일 없음 확인용 목록
    for f in REQUIRED:
        check(os.path.exists(os.path.join(HERE, f)), f"산출 파일 없음 {f}")
    return fails, stats


def main():
    with open(SRC, "rb") as f:
        raw = f.read()
    sha_start = hashlib.sha256(raw).hexdigest()
    R = {n: load(n) for n in ["source-map.json", "coverage.json", "review.md", "manual-observations.json",
                              "morphology.json", "segmentation-review.json", "expressions.json",
                              "manual-expressions.json", "expression-review.json"]}
    fails, stats = run_checks(raw, R)
    result = {"failure_count": len(fails), "failures": fails[:50], "stats": stats}
    if "--selftest" in sys.argv:
        muts = {
            "drop_source_node": lambda R: R["source-map.json"]["nodes"].pop(100),
            "drop_owned_pointer": lambda R: R["coverage.json"]["sections"][5]["owned"].pop(),
            "dup_owned_pointer": lambda R: R["coverage.json"]["sections"][1]["owned"].append("/categories/3/id"),
            "unread_section": lambda R: R["coverage.json"]["sections"][9].update(read_status="미읽음"),
            "shift_token_span": lambda R: R["morphology.json"]["records"][10]["tokens"][0].update(start=1),
            "alter_review_value": lambda R: R.update({"review.md": R["review.md"].replace("| 켈로이드 체질 |", "| 켈로이드 |", 1)}),
            "shift_expression": lambda R: R["expressions.json"]["items"][3].update(start=R["expressions.json"]["items"][3]["start"] + 1),
            "drop_morph_record": lambda R: R["morphology.json"]["records"].pop(),
        }
        st = {}
        for name, fn in muts.items():
            R2 = copy.deepcopy(R)
            fn(R2)
            f2, _ = run_checks(raw, R2)
            st[name] = "검출" if f2 else "미검출"
        st["mutated_source_bytes"] = "검출" if run_checks(raw.replace("필러".encode(), "필라".encode(), 1), R)[0] else "미검출"
        result["selftest"] = st
        if any(v != "검출" for v in st.values()):
            fails.append("selftest 미검출 있음")
    with open(SRC, "rb") as f:
        sha_end = hashlib.sha256(f.read()).hexdigest()
    result["source_sha256_start"] = sha_start
    result["source_sha256_end"] = sha_end
    if sha_start != sha_end:
        fails.append("검증 중 원본 변경")
    result["failure_count"] = len(fails)
    print(json.dumps(result, ensure_ascii=False, indent=1))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
