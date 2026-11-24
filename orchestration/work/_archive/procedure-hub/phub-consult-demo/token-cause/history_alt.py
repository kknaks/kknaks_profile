"""할 일 4 — 앞 대화(--resume) 대신 「주제 튜플 + 앞 답 요약」 이면 몇 토큰인가(요약 문장은 만들지 않고 크기만).

이어 턴마다:
- 지금 = decompose 의 history_tok(실측 − 추정).
- A = 주제 튜플(장부 consult.topics 또는 consult_state 이름 JSON) + 앞 질문 전부 + 앞 답 글 전부(<<<근거>>> 꼬리 뺌) + 이번 턴이
      번호로 가리키는 앞 자료 줄(seen_lines) 다시 실음 + 앞 턴에 보내 이번에 안 보낸 명동점 진료항목 줄(LC5) 다시 실음(위 한계).
- B = 주제 튜플 + 바로 앞 질문 · 답 그대로 + 그 전 턴은 턴마다 한 줄 요약(크기 = 지금 시대 답 글 첫 문장 바이트의 중앙값으로 가정)
      + seen_lines 다시 실음.
토큰 = k × 바이트(decompose 의 k).  실행: python3 history_alt.py  → out/history_alt.json · 표준 출력 표
"""

from __future__ import annotations

import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common  # noqa: E402


def answer_text(r):
    raw = r.get("answer_raw") or r.get("answer") or ""
    return raw.split("<<<근거>>>")[0].strip()


def first_sentence(t):
    m = re.search(r"^.*?[.?!요다](\s|$)", t.strip().replace("\n", " "))
    return m.group(0) if m else t[:80]


def topic_tuple(r):
    c = r.get("consult") or {}
    if isinstance(c, dict) and c.get("topics"):
        return json.dumps([{k: v for k, v in t.items() if k != "last"} for t in c["topics"]], ensure_ascii=False)
    st = r.get("consult_state") or {}
    if isinstance(st, dict):
        names = {k: [x.get("name") for x in st.get(k) or [] if isinstance(x, dict)] for k in ("concerns", "subjects", "sites")}
        return json.dumps(names, ensure_ascii=False)
    return json.dumps([t.get("name") for t in r.get("targets") or []], ensure_ascii=False)


def main():
    d = json.loads((HERE / "out/decompose.json").read_text())
    k = d["k_tok_per_byte"]
    dec = {(t["conv"], t["turn"]): t for t in d["turns"]}
    rows = common.answer_rows()
    by_sess = defaultdict(list)
    for r in rows:
        by_sess[r["llm"].get("session_id")].append(r)
    cur = [r for r in rows if not common.era(r).startswith("before")]
    summ_b = statistics.median(common.b(first_sentence(answer_text(r))) for r in cur if answer_text(r))
    out = []
    for sid, rs in by_sess.items():
        rs.sort(key=lambda r: (r.get("asked_at") or "", r.get("turn") or 0))
        sent = []
        line_bytes = {}
        kos_code_bytes = {}  # LC5 — 앞 턴에 보낸 명동점 진료항목(다시 안 보냄) · 코드당 바이트 ≈ 그 턴 블록 바이트 / 코드 수(위 한계)
        for r in rs:
            t = dec[(r["conv_id"], r.get("turn"))]
            if r["llm"].get("mode") == "resume" and t["sent"] and not common.era(r).startswith("before") and sent:
                prev = sent[-1]
                seen = (r.get("material") or {}).get("seen_lines") or []
                seen_b = sum(line_bytes.get(n, 0) for n in seen)
                topic_b = common.b(topic_tuple(prev))
                qa = [common.b(x.get("question") or "") + common.b(answer_text(x)) for x in sent]
                kos_b = sum(kos_code_bytes.values())
                A = topic_b + sum(qa) + seen_b + kos_b
                B = topic_b + qa[-1] + summ_b * (len(sent) - 1) + seen_b + kos_b
                out.append({"conv": r["conv_id"][:4], "turn": r.get("turn"), "prev_turns": len(sent),
                            "now_tok": t["history_tok"], "A_tok": round(k * A), "B_tok": round(k * B),
                            "topic_tok": round(k * topic_b), "seen_lines": len(seen), "seen_tok": round(k * seen_b), "kos_resend_tok": round(k * kos_b),
                            "total_now": t["tokens_total"]})
            if t["sent"]:
                sent.append(r)
                kb = (r.get("llm") or {}).get("kos_block") or {}
                kos_sec = common.b(common.split_sections(r["llm_user_message"]).get("kos", ""))
                for c in kb.get("codes") or []:
                    kos_code_bytes.setdefault(c, kos_sec / max(1, len(kb["codes"])))
                for x in common.material_lines(common.split_sections(r["llm_user_message"]).get("material", "")):
                    if x["t"] == "row":
                        line_bytes[x["obj"]["n"]] = x["bytes"]
    (HERE / "out/history_alt.json").write_text(json.dumps({"summary_bytes_assumed": summ_b, "turns": out},
                                                          ensure_ascii=False, indent=1))
    print(f"요약 한 줄 가정 = {summ_b} 바이트 ≈ {round(k * summ_b)} 토큰 (지금 시대 답 첫 문장 중앙)\n")
    print("| 턴 차례 | 턴 수 | 지금 앞 대화 중앙 | A(주제+앞 질문·답 전부+다시 볼 줄) 중앙 | B(주제+바로 앞 답+그 전 한 줄씩+다시 볼 줄) 중앙 | 다시 볼 줄 중앙 | 명동점 다시 실음 중앙 | A 감소 | B 감소 |")
    print("|---|---|---|---|---|---|---|---|---|")
    byn = defaultdict(list)
    for x in out:
        byn[x["turn"]].append(x)
    for n in sorted(byn):
        xs = byn[n]
        now = sum(x["now_tok"] for x in xs)
        A = sum(x["A_tok"] for x in xs)
        B = sum(x["B_tok"] for x in xs)
        print(f'| {n} | {len(xs)} | {statistics.median(x["now_tok"] for x in xs):,.0f} | {statistics.median(x["A_tok"] for x in xs):,.0f} | '
              f'{statistics.median(x["B_tok"] for x in xs):,.0f} | {statistics.median(x["seen_tok"] for x in xs):,.0f} | {statistics.median(x["kos_resend_tok"] for x in xs):,.0f} | '
              f'{100 - 100 * A / now:.0f}% | {100 - 100 * B / now:.0f}% |')
    now = sum(x["now_tok"] for x in out)
    A = sum(x["A_tok"] for x in out)
    B = sum(x["B_tok"] for x in out)
    tot = sum(x["total_now"] for x in out)
    kos = sum(x["kos_resend_tok"] for x in out)
    print(f"\n아래 한계(명동점 다시 실음 뺌): A {A - kos:,}({100 - 100 * (A - kos) / now:.1f}% 감소 · 입력 {100 * (now - A + kos) / tot:.1f}% 줄어듦)"
          f" · B {B - kos:,}({100 - 100 * (B - kos) / now:.1f}% 감소 · 입력 {100 * (now - B + kos) / tot:.1f}% 줄어듦)")
    print(f"\n합: 이어 턴 {len(out)} · 지금 앞 대화 {now:,} → A {A:,}({100 - 100 * A / now:.1f}% 감소) · B {B:,}({100 - 100 * B / now:.1f}% 감소)"
          f" · 그 턴들 입력 합 {tot:,} 중 앞 대화 몫 {100 * now / tot:.1f}% → A 면 입력 {100 * (now - A) / tot:.1f}% · B 면 {100 * (now - B) / tot:.1f}% 줄어듦")


if __name__ == "__main__":
    main()
