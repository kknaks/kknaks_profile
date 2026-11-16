"""실버 9단계 효과 재셈 — 2차 A 54 · rerun-v5a case3 A 30 중 9단계 레코드로 닫히는 행(행 단위 · 결정론 · 읽기만).

판정(행마다): A 행 인용(정규화 · recheck2 와 같은 norm)이
  ① 9단계 node_slots 가 골드로 내보낼 레코드(emit) 원문 안에 있음 → 「실버 9단계로 닫힘」
  ② ②(숫자 다름)의 alternatives 원문에만 있음 → 「alternatives 에만(골드 안 나감)」
  ③ 8단계 실버 그대로 · 9단계 section 표(section_map)에 그 원천 경로가 있음 → 「골드 section 으로(실버 변경 없음)」
  ④ 값 사전(value_dictionary)에 있음 → 「값 사전(시맨틱 · 골드 globals)」
  그 밖 → 「안 닫힘」(사유 = 원천 경로 꼴)
조사 판(step9-research.json A2_rows · A5_rows)의 판정과 행마다 대조한다.
입력: step9-explanations.json · step9-research.json · reference/2026-10-30-hub-evals(fail-triage2.json · runs · quality — 읽기만)
출력: step9-effect.json · step9-effect.md
"""
from __future__ import annotations

import json
import re
from pathlib import Path

W = Path(__file__).resolve().parent


def norm(s) -> str:
    return re.sub(r"[\s\W_]+", "", str(s).lower())


def main() -> int:
    o = json.loads((W / "step9-explanations.json").read_text(encoding="utf-8"))
    rs = json.loads((W / "step9-research.json").read_text(encoding="utf-8"))
    rec = {r["id"]: r for r in o["records"]}
    emit, alt = {}, {}
    for e in o["node_slots"]:
        for rid in e["emit"]:
            emit.setdefault(rid, []).append(e["node"])
        for rid in e.get("alternatives") or []:
            alt.setdefault(rid, []).append(e["node"])
    E = [(norm(rec[r]["text"]), r, n) for r, n in sorted(emit.items())]
    A = [(norm(rec[r]["text"]), r, n) for r, n in sorted(alt.items())]
    smap = {x["path"]: x for x in o["section_map"]}
    vd = [norm(x["text"]) for x in o["value_dictionary"]]

    def judge(a):
        q = norm(a.get("quote") or "")
        p = a.get("path") or ""
        if q:
            hit = [(r, n) for t, r, n in E if q in t]
            if hit:
                return "실버 9단계로 닫힘", hit[0][0], sorted({x for _, n in hit for x in n})[:4]
            if any(q in t for t in vd):
                return "값 사전(시맨틱 · 골드 globals)", "value_dictionary", ["scope:all"]
            sm = [x for k, x in smap.items() if k == p or k.startswith(p + ".") or k.startswith(p + "[")]
            if sm:
                return "골드 section 으로(실버 변경 없음)", sm[0]["section"], [sm[0]["node"]]
            ah = [(r, n) for t, r, n in A if q in t]
            if ah:
                return "alternatives 에만(골드 안 나감)", ah[0][0], sorted({x for _, n in ah for x in n})[:4]
        return "안 닫힘", "라벨 · 메타 칸 또는 대상 밖", []

    out = {}
    for key in ("A2", "A5"):
        rows = []
        for a in rs[f"{key}_rows"]:
            v, why, nodes = judge(a)
            prev = a["closes"]
            prev_map = {"예": "실버 9단계로 닫힘", "골드 빌드로(실버 변경 없음)": "골드 section 으로(실버 변경 없음)", "아니오": "안 닫힘"}[prev]
            if a.get("rule") == "R9-7" and prev == "예":
                prev_map = "값 사전(시맨틱 · 골드 globals)"
            rows.append({"no": a["no"], "case": a["case"], "item": a["item"], "path": a["path"], "verdict": v, "by": why, "nodes": nodes,
                         "research": prev_map, "same_as_research": v == prev_map})
        tally = {}
        for r in rows:
            tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
        out[key] = {"rows": len(rows), "tally": dict(sorted(tally.items())), "diff_vs_research": [r for r in rows if not r["same_as_research"]], "detail": rows}
    (W / "step9-effect.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    L = ["# 실버 9단계 효과 재셈 — A 행 닫힘(행 단위)", "", "> `step9-effect.py`(결정론 · 읽기만) · 레코드 `step9-explanations.json` · 조사 판 판정 `step9-research.json` 과 행마다 대조.", ""]
    for key, title in (("A2", "2차 A(rerun-v3 · fail-triage2 cls=A)"), ("A5", "rerun-v5a case3 A(gold_match 무히트 · 조사 셈 30)")):
        x = out[key]
        L += [f"## {title} — {x['rows']}행", "", "| 판정 | 행 |", "|---|---|"] + [f"| {k} | {v} |" for k, v in x["tally"].items()]
        L += ["", f"조사 판과 다른 행: {len(x['diff_vs_research'])}", "", "| 문항 | 케이스 | 원장 경로 | 판정 | 근거 | 붙는 노드 | 조사 판 |", "|---|---|---|---|---|---|---|"]
        for r in x["detail"]:
            L.append(f"| {r['no']} | {r['case']} | `{r['path']}` | {r['verdict']} | {r['by'][:60]} | {' · '.join(r['nodes'])} | {r['research']}{'' if r['same_as_research'] else ' ← 다름'} |")
        L.append("")
    (W / "step9-effect.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(json.dumps({k: {"rows": v["rows"], "tally": v["tally"], "diff": len(v["diff_vs_research"])} for k, v in out.items()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
