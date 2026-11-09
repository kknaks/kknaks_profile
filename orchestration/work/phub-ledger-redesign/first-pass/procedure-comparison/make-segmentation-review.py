"""segmentation-signatures.json 의 서명을 morphology.json 의 모든 값에서 찾아 출현 단위 기록으로 펼친다.
build.py 를 한 번 돌려 morphology.json 이 있어야 한다. 실행 후 build.py 를 다시 돌리면 출현이 검증·반영된다.
실행(레포 루트): python3 orchestration/work/phub-ledger-redesign/first-pass/procedure-comparison/make-segmentation-review.py
"""
import json, os
OUT = os.path.dirname(os.path.abspath(__file__))
sig = json.load(open(os.path.join(OUT, "segmentation-signatures.json"), encoding="utf-8"))
mo = json.load(open(os.path.join(OUT, "morphology.json"), encoding="utf-8"))
occ, nohit = [], []
for s in sig["signatures"]:
    hits = 0
    for r in mo["values"]:
        if s.get("pointer") and r["pointer"] != s["pointer"]:
            continue
        t = r["tokens"]
        n = len(s["tokens"])
        for i in range(len(t) - n + 1):
            if all([t[i + j]["form"], t[i + j]["tag"]] == s["tokens"][j] for j in range(n)) and \
                    (not s.get("zero_length_only") or all(x["span"][0] == x["span"][1] for x in t[i:i + n])):
                a = min(x["span"][0] for x in t[i:i + n]); b = max(x["span"][1] for x in t[i:i + n])
                # 구절 구간: 서명 phrase 가 토큰 구간을 덮는 위치
                txt = r["text"]; pa = -1
                for k in range(max(0, b - len(s["phrase"])), a + 1):
                    if txt[k:k + len(s["phrase"])] == s["phrase"]:
                        pa = k; break
                if pa < 0:
                    raise SystemExit(f"phrase not around tokens: {s['id']} {r['pointer']}")
                occ.append({"signature": s["id"], "pointer": r["pointer"], "phrase": s["phrase"], "phrase_span": [pa, pa + len(s["phrase"])],
                            "tokens": [[x["form"], x["tag"], x["span"]] for x in t[i:i + n]],
                            "kind": s["kind"], "issue": s["issue"], "impact": s["impact"]})
                hits += 1
    if hits == 0:
        nohit.append(s["id"])
if nohit:
    raise SystemExit(f"서명 출현 0: {nohit}")
json.dump({"note": sig["note"], "occurrences": occ}, open(os.path.join(OUT, "segmentation-review.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(occ), "occurrences")
