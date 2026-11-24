"""0.1.1 다시 셈(검수 P1-1 · P1-3 · P2-2 · P2-5) — 초안 r<N> 프롬프트로 실제 이해 호출 후 2차 규칙 판으로 셈.

모음 셋:
- sample  = 표본 43 턴(measure.load_turns — token-cause PICK 10 대화)
- outside = 표본 밖 지금 시대 장부 턴 전부(자료 있음 · 인용 있음 · kinds_by 있음 — 검수 overfit.py 와 같은 거름 · 19 턴)
- cross   = 표본 대화에서 앞 턴 줄을 인용한 턴 가운데 위 둘에 없는 턴(JSON 만 필요 — 앞 턴 이름만 줄을 다시 읽나)
셈 칸: 감소 · 빠짐 · 상세 잃음(이름만으로 준 인용 가운데 lineup 아님) · lineup 이름만 · 앞 턴 인용(G7 옛 / 새).

실행(앱 venv): cd $A && PYTHONDONTWRITEBYTECODE=1 uv run --no-sync python $W/fetch-plan/run4.py --round 4 --rules 5 [--offline]
"""
from __future__ import annotations

import argparse, asyncio, json, statistics, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "token-cause")); sys.path.insert(0, str(HERE))
import common  # noqa: E402
import jev_measure as jm  # noqa: E402
import measure as M  # noqa: E402


def struct(r, rs, md):
    b = jm.build(r, md)
    sec = common.split_sections(r["llm_user_message"]).get("material", "")
    mls = common.material_lines(sec)
    return {"pre": r["conv_id"][:4], "conv": r["conv_id"], "turn": r["turn"], "row": r,
            "prev": [x for x in rs if x["turn"] < r["turn"]], "b": b,
            "row_obj": {x["obj"]["n"]: x["obj"] for x in mls if x["t"] == "row"},
            "head_of": {n: (x["obj"], len(x["obj"].get("lines") or [])) for x in mls if x["t"] == "head"
                        for n in x["obj"].get("lines") or []}}


def outside_turns(md):
    pres = [p for p, _, _ in jm.PICK]
    by = {}
    for r in jm.rows_of("main"):
        by.setdefault(r["conv_id"], []).append(r)
    out = []
    for cid, rs in sorted(by.items()):
        if any(cid.startswith(p) for p in pres) or cid.startswith("fixE"):
            continue
        rs.sort(key=lambda r: r["turn"])
        for r in rs:
            if common.date_of(r) < "2026-11-18" or not ((r.get("trace") or {}).get("front") or {}).get("kinds_by"):
                continue
            t = struct(r, rs, md)
            if t["b"]["cls"] and any(c["used"] for c in t["b"]["cls"].values()):
                out.append(t)
    return out


def conv_rows():
    out = {}
    for pre, which, _ in jm.PICK:
        rs = sorted([r for r in jm.rows_of(which) if r["conv_id"].startswith(pre) and (which == "replay" or not r["conv_id"].startswith("fixE"))],
                    key=lambda r: r["turn"])
        out[pre] = rs
    return out


def mat_rows(r):
    sec = common.split_sections(r["llm_user_message"]).get("material", "")
    return {x["obj"]["n"] for x in common.material_lines(sec) if x["t"] == "row"}


def score(turns, res, k):
    per, tot = [], Counter()
    last = {}
    for t, u in zip(turns, res):
        prev = last.get(t["conv"])
        t["prev_thin_owners"] = set(prev[1]) if prev and prev[0] == t["turn"] - 1 or (prev and t["prev"] and t["prev"][-1]["turn"] == prev[0]) else set()
        sc = M.select(t, u["json"] or {}, k)
        last[t["conv"]] = (t["turn"], sc["thin_owners"])
        cls = t["b"]["cls"]
        thin_rows = sc["thin_rows"]
        lose = [x for x in thin_rows if "lineup" not in x["kind"]]
        sc["lose_detail"], sc["lineup_names"] = len(lose), len(thin_rows) - len(lose)
        sc["lose_rows"] = lose
        per.append({"conv": t["conv"][:4], "turn": t["turn"], "question": t["row"]["question"], "json_ok": bool(u["json"]),
                    "ms": u["ms"], "out_tok": (u["usage"] or {}).get("output_tokens"), **sc})
        for kk in ("now_tok", "new_tok", "cited", "miss", "lose_detail", "lineup_names"):
            tot[kk] += sc[kk]
        tot["json_bad"] += 0 if u["json"] else 1
    tot["cut_pct"] = round(100 * (1 - tot["new_tok"] / tot["now_tok"]), 1) if tot["now_tok"] else 0
    # 시대(재검수 P2-10) — 장부 줄의 `trace.front.kinds_by`: jev(Jev 종류 고르기 · 11-18) · understand · default(지금 앱)
    eras = {}
    for t, p in zip(turns, per):
        e = ((t["row"].get("trace") or {}).get("front") or {}).get("kinds_by") or "?"
        p["era"] = e
        g = eras.setdefault(e, Counter())
        g["turns"] += 1
        for kk in ("now_tok", "new_tok", "cited", "miss", "lose_detail", "lineup_names"):
            g[kk] += p[kk]
    for nm, members in (("now", ("understand", "default")),):
        g = Counter()
        for e in members:
            g.update(eras.get(e, Counter()))
        eras[nm] = g
    for g in eras.values():
        g["cut_pct"] = round(100 * (1 - g["new_tok"] / g["now_tok"]), 1) if g["now_tok"] else 0
    tot["eras"] = {kk: dict(v) for kk, v in eras.items()}
    tot["turns"] = len(per)
    ms = [p["ms"] for p in per if p["ms"]]
    tot["ms_median"], tot["ms_max"] = (round(statistics.median(ms)), round(max(ms))) if ms else (0, 0)
    tot["out_tok_median"] = statistics.median([p["out_tok"] or 0 for p in per]) if per else 0
    return per, dict(tot)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, default=4)
    ap.add_argument("--rules", type=int, default=5)
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()
    M.RULES = a.rules
    md = common.md_sets()
    k = json.loads((HERE.parent / "token-cause/out/decompose.json").read_text())["k_tok_per_byte"]
    sample = M.load_turns(md)
    outside = outside_turns(md)
    rows = conv_rows()
    have = {(t["conv"], t["turn"]) for t in sample}
    cross = []
    for pre, rs in rows.items():
        mats = {r["turn"]: mat_rows(r) for r in rs}
        for r in rs:
            if (r["conv_id"], r["turn"]) in have:
                continue
            if common.cited_rows(r) - mats[r["turn"]]:
                cross.append(struct(r, rs, md))
    sets = {"sample": sample, "outside": outside, "cross": cross}
    print({kk: len(v) for kk, v in sets.items()}, flush=True)
    res = {}
    for name, ts in sets.items():
        p = HERE / f"out/understand_r{a.round}_{name}.jsonl"
        if a.offline:
            res[name] = [json.loads(x) for x in p.read_text().splitlines()]
        else:
            res[name] = asyncio.run(M.call_all(ts, a.round, 4))
            (HERE / f"out/understand_r{a.round}.jsonl").rename(p)
    out = {}
    for name in ("sample", "outside"):
        per, tot = score(sets[name], res[name], k)
        out[name] = {"summary": tot, "turns": per}
        print(name, json.dumps(tot, ensure_ascii=False))
    # 앞 턴 인용(P1-1) — 근원 턴에서 빠졌나 · 이름만이었나 · 이름만이면 인용 턴의 JSON 으로 G7(새)이면 상세를 다시 읽나
    jmap = {}
    for name in ("sample", "cross"):
        for t, u in zip(sets[name], res[name]):
            jmap[(t["conv"], t["turn"])] = u["json"] or {}
    smap = {(t["conv"], t["turn"]): t for t in sample}
    cross_rows = []
    for pre, rs in rows.items():
        mats = {r["turn"]: mat_rows(r) for r in rs}
        for r in rs:
            for n in sorted(common.cited_rows(r) - mats[r["turn"]]):
                src = [tt for tt in mats if tt < r["turn"] and n in mats[tt]]
                if not src:
                    cross_rows.append({"conv": pre, "turn": r["turn"], "n": n, "src": None, "state": "근원 모름"}); continue
                s = src[-1]
                st = smap.get((r["conv_id"], s))
                if st is None:
                    cross_rows.append({"conv": pre, "turn": r["turn"], "n": n, "src": s, "state": "근원 턴 표본 밖"}); continue
                sc = M.select(st, jmap.get((r["conv_id"], s)) or {}, k)
                if n not in sc["keep"]:
                    state = "근원에서 빠짐"
                elif n not in sc["thin"]:
                    state = "근원에서 전체"
                else:
                    pseudo = dict(st); pseudo["row"] = r  # 인용 턴의 말 · 주제 + 근원 줄
                    sc2 = M.select(pseudo, jmap.get((r["conv_id"], r["turn"])) or {}, k)
                    re_full = n in sc2["keep"] and n not in sc2["thin"]
                    f = (jmap.get((r["conv_id"], r["turn"])) or {}).get("fetch") or {}
                    state = ("이름만 → 이 턴 상세 다시 실림(G7 새)" if re_full else "이름만 → 이 턴도 이름만") + f" · scope={f.get('scope')}"
                cross_rows.append({"conv": pre, "turn": r["turn"], "n": n, "src": s, "state": state,
                                   "kind": st["b"]["cls"].get(n, {}).get("kind"), "q": r["question"][:30]})
    out["cross"] = {"rows": cross_rows, "count": dict(Counter(x["state"].split(" · ")[0] for x in cross_rows))}
    print("cross", json.dumps(out["cross"]["count"], ensure_ascii=False))
    for x in cross_rows:
        if "이름만" in x["state"] or "빠짐" in x["state"]:
            print("  ", x)
    (HERE / f"out/run{a.round}_rules{a.rules}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=list))


if __name__ == "__main__":
    main()
