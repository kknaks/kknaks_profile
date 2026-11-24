"""할 일 0 — 비용 전체 셈(장부 읽기만 · LLM 0). 답 턴 출력 토큰 · 이해 호출 토큰 갈래 · 비용 몫(API 표준 단가 무게).

무게 가정(Sonnet API 표준 단가 비 · 입력 1 기준): input 1 · cache_creation 1.25 · cache_read 0.1 · output 5.
CLI 구독 과금과는 다르다 — 몫 비교용.
실행: python3 cost.py [장부 경로] → out/cost.json · out/cost.md
"""
import json, statistics, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = Path(sys.argv[1] if len(sys.argv) > 1 else "/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/runs/consult/turns.jsonl")
WGT = {"input": 1.0, "creation": 1.25, "read": 0.1, "output": 5.0}

rows = [json.loads(x) for x in LEDGER.read_text().splitlines() if x.strip()]
end = [r for r in rows if r.get("phase") == "end" and (r.get("asked_at") or "")[:10] >= "2026-11-18"]

def g(d, k):
    return int((d or {}).get(k) or 0)

ans = []   # 답 호출
und = []   # 이해 호출
und_missing = defaultdict(int)
for r in end:
    t = r.get("tokens")
    if t:
        ans.append({"conv": r["conv_id"][:4], "turn": r["turn"], "input": g(t, "input_tokens"),
                    "creation": g(t, "cache_creation_input_tokens"), "read": g(t, "cache_read_input_tokens"),
                    "output": g(t, "output_tokens")})
    u = ((r.get("consult") or {}).get("understand") or {})
    if not u:
        und_missing["understand 없음(0.4 이전 · 실패)"] += 1
        continue
    us = u.get("usage") or {}
    if not us:
        und_missing["usage 없음"] += 1
        continue
    if "cache_creation_input_tokens" not in us:
        und_missing["usage 에 cache_creation 칸 없음(앱이 안 남김)"] += 1
    und.append({"conv": r["conv_id"][:4], "turn": r["turn"], "input": g(us, "input_tokens"),
                "creation": g(us, "cache_creation_input_tokens"), "read": g(us, "cache_read_input_tokens"),
                "output": g(us, "output_tokens"), "thinking": us.get("thinking_tokens"),
                "sys_bytes": (u.get("input_bytes") or {}).get("system"), "msg_bytes": (u.get("input_bytes") or {}).get("message"),
                "ms": u.get("ms"), "api_ms": u.get("api_ms")})

def tot(xs, k):
    return sum(x[k] for x in xs)

def cost(xs):
    return {k: tot(xs, k) * WGT[k] for k in WGT}

out = {"ledger_rows": len(rows), "era_end_rows": len(end), "answer_turns": len(ans), "understand_calls": len(und),
       "understand_missing": dict(und_missing), "weights": WGT}
for name, xs in (("answer", ans), ("understand", und)):
    o = {k: tot(xs, k) for k in ("input", "creation", "read", "output")}
    inp = o["input"] + o["creation"] + o["read"]
    o["input_all"] = inp
    o["output_per_turn_median"] = statistics.median([x["output"] for x in xs]) if xs else 0
    o["output_per_turn_max"] = max([x["output"] for x in xs]) if xs else 0
    o["output_over_input"] = round(o["output"] / inp, 4) if inp else None
    o["cost_weighted"] = {k: round(v) for k, v in cost(xs).items()}
    out[name] = o
cw_all = sum(out["answer"]["cost_weighted"].values()) + sum(out["understand"]["cost_weighted"].values())
out["share"] = {f"{n}.{k}": round(out[n]["cost_weighted"][k] / cw_all * 100, 1)
                for n in ("answer", "understand") for k in WGT}
out["cost_weighted_total"] = round(cw_all)
# 이해 호출 시스템 글 캐시 — 같은 대화 안 시스템 바이트가 턴마다 바뀌나
by_conv = defaultdict(list)
for x in und:
    by_conv[x["conv"]].append(x)
sys_change = sum(1 for xs in by_conv.values() for a, b in zip(xs, xs[1:]) if a["sys_bytes"] != b["sys_bytes"])
out["understand_cache"] = {
    "calls_with_read": sum(1 for x in und if x["read"] > 0),
    "calls_with_creation": sum(1 for x in und if x["creation"] > 0),
    "calls_read_0": sum(1 for x in und if x["read"] == 0),
    "sys_bytes_distinct": sorted({x["sys_bytes"] for x in und if x["sys_bytes"]}),
    "sys_bytes_change_within_conv": sys_change,
    "read_median": statistics.median([x["read"] for x in und]) if und else 0,
    "input_median": statistics.median([x["input"] for x in und]) if und else 0,
    "output_median": statistics.median([x["output"] for x in und]) if und else 0,
    "ms_median": statistics.median([x["ms"] for x in und if x["ms"]]) if und else 0,
}
(HERE / "out").mkdir(exist_ok=True)
(HERE / "out/cost.json").write_text(json.dumps({**out, "answer_rows": ans, "understand_rows": und}, ensure_ascii=False, indent=1))
print(json.dumps(out, ensure_ascii=False, indent=1))
