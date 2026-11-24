"""측정 표 → out/tables.md(회차 요약 · 턴별 표). 실행: python3 tables.py"""
import json
from pathlib import Path

O = Path(__file__).resolve().parent / "out"
runs = [("r1_rules1", "1", "1", "초안 1 · 2차 1판(명동점 밖 하위 뺌 · layers 그대로)"),
        ("r1_rules2", "1", "2", "같은 JSON · 2차 2판(명동점 닿는 하위 늘 · 밖은 이름만)"),
        ("r2_rules2", "2", "2", "초안 2(offer · layers 기본 sub · 밖 이어 묻기 all) · 2차 2판"),
        ("r2_rules3", "2", "3", "같은 JSON · 2차 3판(부위만 턴 = 주제 진료항목 대상만 · 이름만 줄은 머리도 이름만)"),
        ("r3_rules3", "3", "3", "초안 2 그대로 다시 호출(흔들림 확인) · 2차 3판 ← **채택**"),
        ("r3_rules4", "3", "4", "같은 JSON · 2차 4판(안 — 명동점 밖 하위의 안전 줄도 이름만)")]
L = ["## 회차 요약", "", "| 회차 | 이해 호출 | 2차 규칙 | 바꾼 것 | 자료 토큰(지금 697,892) | 감소 | 빠짐 | 얇아진 인용(이름만) | JSON 깨짐 | 이해 ms 중앙 / 최대 |",
     "|---|---|---|---|---:|---:|---:|---:|---:|---|"]
for tag, rr, ru, why in runs:
    p = O / f"measure_{tag}.json"
    if not p.exists():
        continue
    s = json.loads(p.read_text())["summary"]
    L.append(f"| {tag} | 호출 {s['json_round']} | {ru} | {why} | {s['new_tok']:,} | {s['cut_pct']}% | {s['miss']}/{s['cited']} ({s['miss_pct']}%) "
             f"| {s.get('thin_cited', '—')} | {s['json_bad']} | {round(s['ms_median'])} / {round(s['ms_max'])} |")
d = json.loads((O / "measure_r3_rules3.json").read_text())
L += ["", "## 턴별(채택 r3_rules3)", "", "| 대화 | 턴 | 말 | JSON kinds | about / layers / scope / lineup | 지금 → 새 토큰 | 감소 | 인용 | 빠짐 | 얇아진 | 이해 ms | 이해 출력 tok |",
      "|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|"]
for p in d["turns"]:
    f = p["fetch"]
    L.append(f"| {p['conv']} | {p['turn']} | {p['question'][:30]} | {', '.join(p['kinds']) or '[]'} | {f['about']} / {f['layers']} / {f['scope']} / {f['lineup']} "
             f"| {p['now_tok']:,} → {p['new_tok']:,} | {p['cut_pct']}% | {p['cited']} | {p['miss']} | {p['thin_cited']} | {round(p['ms'] or 0)} | {(p['usage'] or {}).get('output_tokens')} |")
s = d["summary"]
L.append(f"| **합** | 43 | | | | **{s['now_tok']:,} → {s['new_tok']:,}** | **{s['cut_pct']}%** | {s['cited']} | **{s['miss']}** | {s['thin_cited']} | 중앙 {round(s['ms_median'])} | {s['usage_sum']['output_tokens']} |")
(O / "tables.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
