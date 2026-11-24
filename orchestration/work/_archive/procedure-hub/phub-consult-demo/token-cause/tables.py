"""decompose.json → 리포트 표(markdown). 실행: python3 tables.py [out/decompose.json ...] > out/tables.md"""

from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SECS = [("judgement", "앱 판정"), ("close", "끝맺음"), ("prev", "앞 턴"), ("consult", "상담 상태"), ("material", "## 자료"),
        ("kos", "명동점 블록"), ("question", "질문")]


def pct(a, t):
    return f"{100 * a / t:.1f}%" if t else "-"


def fmt(x):
    return f"{round(x):,}"


def era_group(t):
    return "now(understand·11-18~)" if not t["era"].startswith("before") else "before(11-17 · jev)"


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def main(paths):
    for p in paths:
        d = json.loads(Path(p).read_text())
        k = d["k_tok_per_byte"]
        T = d["turns"]
        print(f"\n## 원본 {p} · 턴 {len(T)} · k = {k:.4f} 토큰/바이트 · 절편 {d['a_by_prompt']} · 맞춤 {d['fit']}\n")
        # 1. 시대별 전체 비율
        groups = defaultdict(list)
        for t in T:
            groups[era_group(t)].append(t)
        rows = []
        for g, ts in groups.items():
            tot = sum(t["tokens_total"] for t in ts)
            sysm = sum(t["system_tok"] for t in ts)
            hist = sum(t["history_tok"] for t in ts)
            secs = Counter()
            for t in ts:
                secs.update(t["sec_tok"])
            r = [g, len(ts), fmt(tot), fmt(tot / len(ts)), fmt(max(t["tokens_total"] for t in ts)),
                 pct(sysm, tot), pct(hist, tot)]
            r += [pct(secs[s], tot) for s, _ in SECS]
            rows.append(r)
        print("### 전체 — 절별 몫(토큰 합 기준)\n")
        print(table(["시대", "턴", "입력 합", "턴 평균", "턴 최대", "시스템+CLI", "앞 대화(--resume)"] + [n for _, n in SECS], rows))
        # 2. 턴별(지금 시대)
        print("\n### 턴별(지금 시대 · 입력 큰 순 상위 25)\n")
        cur = [t for t in T if not t["era"].startswith("before")]
        rows = []
        for t in sorted(cur, key=lambda t: -t["tokens_total"])[:25]:
            s = t["sec_tok"]
            rows.append([t["conv"][:4] + (t["conv"][-4:] if t["conv"].startswith("fixE") else ""), t["turn"],
                         t["date"], "실측" if t["sent"] else "추정(안 보냄)", fmt(t["tokens_total"]), fmt(t["system_tok"]),
                         fmt(t["history_tok"]), fmt(s.get("material", 0)), fmt(s.get("kos", 0)),
                         fmt(s.get("judgement", 0) + s.get("close", 0) + s.get("prev", 0)), fmt(s.get("consult", 0)),
                         f'{t["mat_used_rows"]}/{t["mat_rows"]}', (t["question"] or "")[:22]])
        print(table(["대화", "턴", "날", "토큰", "입력", "시스템", "앞 대화", "자료", "명동점", "판정", "상태", "인용/줄", "질문"], rows))
        # 3. 대화별
        print("\n### 대화별(지금 시대)\n")
        byc = defaultdict(list)
        for t in cur:
            byc[t["conv"]].append(t)
        rows = []
        for c, ts in sorted(byc.items(), key=lambda x: -sum(t["tokens_total"] for t in x[1])):
            tot = sum(t["tokens_total"] for t in ts)
            rows.append([c[:4] + (c[-4:] if c.startswith("fixE") else ""), len(ts), fmt(tot), fmt(max(t["tokens_total"] for t in ts)),
                         pct(sum(t["history_tok"] for t in ts), tot), pct(sum(t["sec_tok"].get("material", 0) for t in ts), tot),
                         pct(sum(t["sec_tok"].get("kos", 0) for t in ts), tot), pct(sum(t["system_tok"] for t in ts), tot)])
        print(table(["대화", "턴", "입력 합", "턴 최대", "앞 대화", "자료", "명동점", "시스템"], rows))
        # 4. 자료 종류 · 층 · 까닭
        for key, title in (("kind_bytes", "종류"), ("layer_bytes", "층"), ("by_bytes", "종류를 고른 까닭(by)")):
            agg = Counter()
            for t in cur:
                agg.update(t[key])
            tot = sum(agg.values())
            print(f"\n### 「## 자료」 {title}별(지금 시대 · 바이트 → 토큰 = × k)\n")
            print(table([title, "토큰(추정)", "자료 안 몫"], [[n, fmt(v * k), pct(v, tot)] for n, v in agg.most_common()]))
        # 5. 낭비
        agg = Counter()
        for t in cur:
            agg.update(t["waste_bytes"])
        mat_tot = sum(sum(t["kind_bytes"].values()) for t in cur)
        hist_tot = sum(t["history_tok"] for t in cur)
        all_tot = sum(t["tokens_total"] for t in cur)
        print("\n### 낭비(지금 시대) — 「## 자료」 줄: 답 근거(<<<근거>>>)에 인용됐나\n")
        names = {"used": "인용됨(쓰임)", "unused_but_safety_or_explicit": "안 쓰임 · 안전/명시 대상(지우면 안 됨)",
                 "unused_kd9": "안 쓰임 · KD9 덧붙인 종류", "unused_sub_not_md": "안 쓰임 · 명동점에 안 닿는 하위 층",
                 "unused_summary": "안 쓰임 · 목록 요약 줄", "unused_other": "안 쓰임 · 그 밖",
                 "dup_names": "(겹침) 같은 줄 안 같은 이름 반복"}
        rows = [[names.get(n, n), fmt(agg[n] * k), pct(agg[n], mat_tot), pct(agg[n] * k, all_tot)] for n in names]
        rows.append(["앞 대화 재전송(--resume 이력 전체)", fmt(hist_tot), "-", pct(hist_tot, all_tot)])
        print(table(["몫", "토큰(추정)", "자료 안 몫", "입력 전체 몫"], rows))
        # 6. 앞 대화 증가
        print("\n### 앞 대화(--resume) 몫 — 대화 안 턴 차례별(지금 시대)\n")
        byn = defaultdict(list)
        for t in cur:
            if t["mode"] == "resume" and t["sent"]:
                byn[t["turn"]].append(t)
        rows = []
        for n in sorted(byn):
            ts = byn[n]
            rows.append([n, len(ts), fmt(statistics.median(t["history_tok"] for t in ts)),
                         fmt(max(t["history_tok"] for t in ts)),
                         pct(sum(t["history_tok"] for t in ts), sum(t["tokens_total"] for t in ts)),
                         fmt(statistics.median(t["history_pred_tok"] for t in ts))])
        print(table(["턴", "턴 수", "앞 대화 중앙", "최대", "그 턴 입력 중 몫", "예측(k × 앞 메시지+답 바이트) 중앙"], rows))


if __name__ == "__main__":
    main(sys.argv[1:] or [str(HERE / "out/decompose.json")])
