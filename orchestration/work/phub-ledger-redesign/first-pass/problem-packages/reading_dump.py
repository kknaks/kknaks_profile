"""읽기용 덤프: 구획별 원문을 complaint 블록 단위로 reading/Sxx.txt 에 쓴다.
행 접두 = 상대 Pointer(complaints/i, procedures/j=P j, combos/k=B k, alternatives/m=A m).
읽기 보조 출력일 뿐 판단 기록이 아니다(판단은 manual-review.json)."""
import json
from pp_common import load, HERE

raw, text, root, nodes, dups = load()
d = json.loads(text)
(HERE / "reading").mkdir(exist_ok=True)
for f in (HERE / "reading").glob("S*.txt"):
    f.unlink()
s0 = [f"/version = {d['version']!r}", f"/updated = {d['updated']!r}",
      f"/description = {d['description']!r}", f"/problems array[{len(d['problems'])}]"]
(HERE / "reading" / "S00.txt").write_text("\n".join(s0) + "\n", encoding="utf-8")
for pi, p in enumerate(d["problems"]):
    L = [f"/problems/{pi}  problem_id={p['problem_id']!r} problem={p['problem']!r} complaints[{len(p['complaints'])}]"]
    for ci, c in enumerate(p["complaints"]):
        L.append(f"\n## c{ci} /problems/{pi}/complaints/{ci}  cc={c['cc']!r} | cc_detail={c['cc_detail']!r} | cc_group={c['cc_group']!r}")
        for j, pr in enumerate(c["procedures"]):
            L.append(f"  P{j} name={pr['name']!r} category={pr['category']!r} role={pr['role']!r} products={pr['products']}")
        if not c["combos"]:
            L.append("  combos=[] (빈 배열)")
        for k, cb in enumerate(c["combos"]):
            L.append(f"  B{k} name={cb['name']!r} combo={cb['combo']}")
            L.append(f"     reason={cb['reason']!r}")
            L.append(f"     evidence={cb['evidence']!r}")
        for m, a in enumerate(c["alternatives"]):
            L.append(f"  A{m} {a!r}")
    (HERE / "reading" / f"S{pi+1:02d}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("ok")
