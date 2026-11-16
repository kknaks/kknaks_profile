#!/usr/bin/env python3
"""pre-procedure-checklist 1차 수집 결과 독립 검증.

레포 루트에서:  python3 orchestration/work/phub-ledger-redesign/first-pass/pre-procedure-checklist/verify.py
표준 라이브러리만 쓴다. 어떤 파일도 쓰지 않는다. 실패가 하나라도 있으면 exit 1.
build.py 의 스캐너를 재사용하지 않고 원본을 따로 파싱해 대조한다.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SRC = ROOT / "orchestration/work/phub-recommend/bronze/phub-ledger/pre-procedure-checklist.json"
REQUIRED = ["review.md", "source-map.json", "morphology.json", "expressions.json", "issues.md", "validation.md",
            "coverage.json", "progress.md", "build.py", "manual/segment-notes.json"]

fails = []
checks = 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def esc_ptr(k):
    return k.replace("~", "~0").replace("/", "~1")


def walk(v, ptr, out):
    """독립 순회: (pointer → (type, value|None, child_count))"""
    if isinstance(v, dict):
        out[ptr] = ("object", None, len(v))
        for k, c in v.items():
            walk(c, ptr + "/" + esc_ptr(k), out)
    elif isinstance(v, list):
        out[ptr] = ("array", None, len(v))
        for i, c in enumerate(v):
            walk(c, f"{ptr}/{i}", out)
    else:
        t = "null" if v is None else "boolean" if isinstance(v, bool) else "number" if isinstance(v, (int, float)) else "string"
        out[ptr] = (t, v, None)


def ptr_get(doc, ptr):
    cur = doc
    if ptr == "":
        return cur
    for part in ptr[1:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def main():
    raw0 = SRC.read_bytes()
    sha0 = hashlib.sha256(raw0).hexdigest()
    text = raw0.decode("utf-8")
    # 바이트 오프셋 독립 계산
    cum = [0]
    for ch in text:
        cum.append(cum[-1] + len(ch.encode("utf-8")))

    dups = []

    def hook(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                dups.append(k)
            seen.add(k)
        return dict(pairs)

    doc = json.loads(text, object_pairs_hook=hook)
    for f in REQUIRED:
        ok((HERE / f).exists(), f"필수 파일 없음: {f}")
    sm = json.loads((HERE / "source-map.json").read_text(encoding="utf-8"))
    mo = json.loads((HERE / "morphology.json").read_text(encoding="utf-8"))
    ex = json.loads((HERE / "expressions.json").read_text(encoding="utf-8"))
    cov = json.loads((HERE / "coverage.json").read_text(encoding="utf-8"))
    notes = json.loads((HERE / "manual/segment-notes.json").read_text(encoding="utf-8"))

    # 1. 원본 식별
    ok(sm["source"]["sha256"] == sha0, "source-map sha256 불일치")
    ok(cov["source_sha256"] == sha0, "coverage sha256 불일치")
    ok(sm["source"]["bytes"] == len(raw0), "bytes 불일치")
    ok(sm["source"]["codepoints"] == len(text), "codepoints 불일치")
    ok(sm["duplicate_keys"] == [] and dups == [], f"중복 키 기록/실측 불일치 {dups}")
    ok((len(sm["escapes"]) == 0) == ("\\" not in text), "이스케이프 기록 불일치")

    # 2. 구조·값 양방향
    truth = {}
    walk(doc, "", truth)
    nodes = sm["nodes"]
    mp = {}
    for n in nodes:
        ok(n["pointer"] not in mp, f"source-map 노드 중복 {n['pointer']}")
        mp[n["pointer"]] = n
    ok(set(mp) == set(truth), f"노드 집합 불일치: 누락 {sorted(set(truth)-set(mp))[:5]} 불필요 {sorted(set(mp)-set(truth))[:5]}")
    order_truth = list(truth)
    ok([n["pointer"] for n in nodes] == order_truth, "노드 문서 순서 불일치")
    for p, (t, v, cc) in truth.items():
        n = mp.get(p)
        if not n:
            continue
        ok(n["json_type"] == t, f"자료형 불일치 {p}")
        if cc is not None:
            ok(n["child_count"] == cc, f"child_count 불일치 {p}")
            ok(n["is_empty_container"] == (cc == 0), f"빈 컨테이너 표시 불일치 {p}")
        else:
            ok(n["value"] == v and type(n["value"]) is type(v), f"값 불일치 {p}")
        s, e = n["literal_cp"]
        ok(json.loads(text[s:e]) == ptr_get(doc, p), f"리터럴 cp 구간 재현 실패 {p}")
        bs, be = n["literal_byte"]
        ok(raw0[bs:be].decode("utf-8") == text[s:e] and [cum[s], cum[e]] == [bs, be], f"리터럴 byte 구간 실패 {p}")
        if n.get("key") is not None:
            ks, ke = n["key_literal_cp"]
            ok(json.loads(text[ks:ke]) == n["key"], f"키 구간 실패 {p}")
            ok(raw0[n["key_literal_byte"][0]:n["key_literal_byte"][1]].decode() == text[ks:ke], f"키 byte 구간 실패 {p}")
        if t == "string":
            vs, ve = n["value_cp_in_file"]
            if not n["has_escape"]:
                ok(text[vs:ve] == v, f"값 내용 구간 실패 {p}")
    leaves = [p for p, (t, _, _) in truth.items() if t not in ("object", "array")]
    ok(sm["counts"]["leaves"] == len(leaves), "말단 수 불일치")
    ok(sm["counts"]["nodes"] == len(truth), "노드 수 불일치")
    # 필드명 출현
    key_truth = {}
    for p in truth:
        if p:
            k = p.rsplit("/", 1)[1]
            if not isinstance(ptr_get(doc, p.rsplit("/", 1)[0] or ""), list):
                key_truth.setdefault(k.replace("~1", "/").replace("~0", "~"), []).append(p)
    ok({k: v["pointers"] for k, v in sm["field_name_occurrences"].items()} == key_truth, "필드명 출현 기록 불일치")

    # 3. coverage — 구획 소유 양방향
    owned = {}
    seg_ids = [s["id"] for s in cov["segments"]]
    for s in cov["segments"]:
        for p in s["owned_pointers"]:
            ok(p not in owned, f"구획 중복 소유 {p}: {owned.get(p)} & {s['id']}")
            owned[p] = s["id"]
        ok(set(s["owned_leaf_pointers"]) == {p for p in s["owned_pointers"] if p in leaves}, f"{s['id']} 말단 목록 불일치")
        ok(s["direct_reading"] == "read", f"{s['id']} 직접 읽기 미완료({s['direct_reading']})")
        rf = HERE / s["review_file"]
        ok(rf.exists(), f"{s['id']} review 파일 없음")
        if rf.exists():
            body = rf.read_text(encoding="utf-8")
            rows = {}
            for line in body.splitlines():
                m = re.match(r"^\| `([^`]*)` \| ", line)
                if m and line.count(" | ") >= 5:
                    ok(m.group(1) not in rows, f"{s['review_file']} 값 표 행 중복 {m.group(1)}")
                    rows.setdefault(m.group(1), line)
            for p in s["owned_pointers"]:
                row = rows.get(p or "(root)")
                ok(row is not None, f"{s['review_file']} 에 Pointer 행 없음 {p}")
                if row is None:
                    continue
                n = mp[p]
                name = n["key"] if n["key"] is not None else (f"[{n['index']}]" if n["index"] is not None else "(root)")
                ok(row.startswith(f"| `{p or '(root)'}` | `{name}` | {n['json_type']}"), f"{s['review_file']} 행의 컬럼명/자료형 불일치 {p}")
                if n["json_type"] == "string":
                    ok(f" | {n['value'].replace('|', chr(92) + '|')} | " in row, f"{s['review_file']} 행에 원문 값 없음 {p}")
            ns = [x for x in notes["segments"] if x["id"] == s["id"]][0]
            for o in ns["observations"]:
                ok(o.replace("|", "\\|") in body, f"{s['review_file']} 관찰 누락")
    ok(set(owned) == set(truth), f"구획 소유 합집합 ≠ 전체: 누락 {sorted(set(truth)-set(owned))[:5]} 불필요 {sorted(set(owned)-set(truth))[:5]}")
    for p, sid in owned.items():
        ok(mp[p]["segment"] == sid, f"source-map 구획 표시 불일치 {p}")
    rv = (HERE / "review.md").read_text(encoding="utf-8")
    for sid in seg_ids:
        ok(f"review-part-{sid}.md" in rv, f"review.md 목차에 {sid} 없음")
    ok(sorted(x.name for x in HERE.glob("review-part-*.md")) == sorted(f"review-part-{s}.md" for s in seg_ids), "review-part 파일 집합 불일치")
    # 컬럼 구성 표: 모든 경로 패턴 행
    pats = {re.sub(r"/\d+", "/*", p) or "(root)" for p in truth}
    for pat in pats:
        ok(f"| `{pat}` |" in rv, f"review.md 컬럼 구성 표에 패턴 없음 {pat}")

    # 4. 형태소 적용/제외 대응
    strings = {p for p, (t, _, _) in truth.items() if t == "string"}
    rec_p = [r["pointer"] for r in mo["records"]]
    exc_p = [r["pointer"] for r in mo["excluded"]]
    ok(len(rec_p) == len(set(rec_p)) and len(exc_p) == len(set(exc_p)), "형태소 기록 중복")
    ok(set(rec_p) | set(exc_p) == strings and not (set(rec_p) & set(exc_p)), "문자열 말단 적용/제외 분할 불일치")
    for r in mo["excluded"]:
        ok(bool(r["reason"]) and r["value"] == truth[r["pointer"]][1], f"제외 사유/값 이상 {r['pointer']}")
    for r in mo["records"]:
        v = truth[r["pointer"]][1]
        ok(r["text"] == v, f"형태소 원문 불일치 {r['pointer']}")
        last = 0
        for t in r["tokens"]:
            ok(0 <= t["start"] < t["end"] <= len(v), f"토큰 구간 범위 {r['pointer']}")
            ok(t["surface"] == v[t["start"]:t["end"]], f"토큰 표면형 재현 실패 {r['pointer']} {t}")
            ok(text[t["file_cp"][0]:t["file_cp"][1]] == t["surface"], f"토큰 file_cp 재현 실패 {r['pointer']}")
            if t["start"] < last:
                # 축약 음절(예: 필러→피/VV+ᆯ러/EC)은 앞 구간 안에서 시작하고 표시가 있어야만 허용, 시작 역행 금지
                ok(t.get("span_shared_with_prev") is True and prev["start"] <= t["start"] < prev["end"],
                   f"토큰 겹침/역순 {r['pointer']} {t}")
                last = max(last, t["end"])
            else:
                ok(t.get("span_shared_with_prev") is False, f"겹침 표시 오류 {r['pointer']} {t}")
                last = t["end"]
            prev = t
        # 공백 외 문자 전부 토큰이 덮는지
        covered = set()
        for t in r["tokens"]:
            covered.update(range(t["start"], t["end"]))
        un = [i for i, ch in enumerate(v) if not ch.isspace() and i not in covered]
        ok(not un, f"토큰 미포함 문자 {r['pointer']} {[v[i] for i in un]}")
        for snt in r["sentences"]:
            ok(v[snt["start"]:snt["end"]] == snt["text"], f"문장 구간 실패 {r['pointer']}")
    ok({f["field_name"] for f in mo["field_names"]} == set(key_truth), "필드명 형태소 기록 집합 불일치")
    for f in mo["field_names"]:
        ok(f["occurrence_pointers"] == key_truth[f["field_name"]], f"필드명 출현 포인터 불일치 {f['field_name']}")
    ok(mo["analyzer"]["version"] == "0.24.1" and mo["analyzer"]["model_type"] == "cong" and mo["analyzer"]["num_workers"] == 1, "분석기 설정 기록 불일치")
    # 알려진 오분절
    recmap = {r["pointer"]: r for r in mo["records"]}
    for k in mo["known_errors"]:
        r = recmap.get(k["pointer"])
        ok(r is not None, f"오분절 기록 pointer 가 분석 대상 아님 {k['pointer']}")
        if not r:
            continue
        ok(k["surface"] in r["text"], f"오분절 표면형 원문에 없음 {k}")
        want = k["raw_tokens"].split(" ")
        # 'form/TAG' 쌍 (form 에 공백이 있는 경우 raw_tokens 문자열 전체로 대조)
        seq = [f"{t['form']}/{t['tag']}" for t in r["tokens"]]
        joined = " ".join(seq)
        ok(k["raw_tokens"] in joined, f"오분절 원시 토큰이 실제 분석에 없음 {k['pointer']} {k['raw_tokens']}")
        ok(bool(k["impact"]), "오분절 영향 비어 있음")
        # span = 디코딩된 값 문자열의 코드포인트 [start,end) — 범위·재현·유일성
        sp = k.get("span")
        ok(isinstance(sp, list) and len(sp) == 2 and all(isinstance(x, int) for x in sp), f"오분절 span 형식 {k['pointer']}")
        if isinstance(sp, list) and len(sp) == 2:
            ok(0 <= sp[0] < sp[1] <= len(r["text"]), f"오분절 span 범위 밖 {k['pointer']} {sp}")
            ok(r["text"][sp[0]:sp[1]] == k["surface"], f"오분절 span 재현 실패 {k['pointer']} {sp}")
            ok(truth[k["pointer"]][1][sp[0]:sp[1]] == k["surface"], f"오분절 span 원본 재현 실패 {k['pointer']}")
        ok(r["text"].count(k["surface"]) == 1, f"오분절 표면형이 값에서 1회가 아님 {k['pointer']}")
    # 레코드별 known_errors ↔ 전역 known_errors 동등성
    rec_ke = [k for r in mo["records"] for k in r["known_errors"]]
    ok(sorted(json.dumps(k, ensure_ascii=False, sort_keys=True) for k in rec_ke)
       == sorted(json.dumps(k, ensure_ascii=False, sort_keys=True) for k in mo["known_errors"]), "레코드별 오분절 ≠ 전역 오분절")
    for r in mo["records"]:
        ok(r["known_errors"] == [k for k in mo["known_errors"] if k["pointer"] == r["pointer"]], f"레코드 오분절 순서·내용 불일치 {r['pointer']}")

    # 5. 표현 구간 재현 + 자동 후보 재계산
    for a in ex["auto_candidates"]:
        v = truth[a["pointer"]][1]
        ok(v[a["start"]:a["end"]] == a["match"] and text[a["file_cp"][0]:a["file_cp"][1]] == a["match"], f"자동 후보 구간 실패 {a}")
    recomputed = set()
    for pat in ex["method"]["patterns"]:
        for r in mo["records"]:
            for m in re.finditer(pat["regex"], r["text"]):
                recomputed.add((pat["id"], r["pointer"], m.start(), m.end()))
    got = {(a["pattern"], a["pointer"], a["start"], a["end"]) for a in ex["auto_candidates"]}
    ok(got == recomputed and len(got) == len(ex["auto_candidates"]), "자동 후보 재계산 불일치/중복")
    mkeys = set()
    for m in ex["manual_expressions"]:
        v = truth[m["pointer"]][1]
        ok(v[m["start"]:m["end"]] == m["text"] and text[m["file_cp"][0]:m["file_cp"][1]] == m["text"], f"수동 표현 구간 실패 {m['text']}")
        key = (m["pointer"], m["start"], m["end"])
        ok(key not in mkeys, f"수동 표현 중복 생성 {key}")
        mkeys.add(key)
        ok(owned.get(m["pointer"]) == m["segment"], f"수동 표현 구획 불일치 {m['pointer']}")
    n_manual_notes = sum(len(s["manual_expressions"]) for s in notes["segments"])
    ok(n_manual_notes == len(ex["manual_expressions"]), "수동 기록 ↔ expressions.json 수 불일치")

    # 6. issues
    iss = (HERE / "issues.md").read_text(encoding="utf-8")
    for s in notes["segments"]:
        for i in s["issues"]:
            ok(i["code"] in "ABCKPFI", f"미결 코드 이상 {i['id']}")
            ok(f"{i['code']}-{i['id']}" in iss, f"issues.md 누락 {i['id']}")
            for p in i.get("pointers", []):
                ok(p in truth, f"미결 pointer 무효 {i['id']} {p}")
    for i in notes.get("global_issues", []):
        ok(f"{i['code']}-{i['id']}" in iss, f"issues.md 전역 누락 {i['id']}")
        for p in i.get("pointers", []):
            ok(p in truth, f"전역 미결 pointer 무효 {i['id']} {p}")

    # 정보: 수동 표현이 없는 분석 대상 값(실패 아님)
    with_manual = {m["pointer"] for m in ex["manual_expressions"]}
    no_manual = [r["pointer"] for r in mo["records"] if r["pointer"] not in with_manual]

    raw1 = SRC.read_bytes()
    ok(hashlib.sha256(raw1).hexdigest() == sha0, "검증 중 원본 해시 변경")

    print(f"source sha256 start={sha0}")
    print(f"source sha256 end  ={hashlib.sha256(raw1).hexdigest()}")
    print(f"nodes={len(truth)} leaves={len(leaves)} strings={len(strings)} analyzed={len(rec_p)} excluded={len(exc_p)} "
          f"segments={len(seg_ids)} auto={len(ex['auto_candidates'])} manual={len(ex['manual_expressions'])} known_errors={len(mo['known_errors'])}")
    print(f"info: 수동 표현 없는 분석 대상 값 {len(no_manual)}개: {no_manual}")
    print(f"checks={checks} failures={len(fails)}")
    for f in fails[:50]:
        print("FAIL", f)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
