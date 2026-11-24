"""할 일 1 · 2 · 4 — 답 턴 입력 분해 · 낭비 셈 · 앞 대화 재전송(LLM 호출 0).

토큰 셈: 장부 `tokens`(실제 = input + cache_creation + cache_read)로 바이트→토큰 비 `k` 를 맞춘다 —
첫 턴(`llm.mode == new` · 앞 대화 0)만 써서 `T = a[프롬프트 판] + k × 메시지 바이트`(판마다 절편 · 기울기 공통, 최소제곱).
`a` = 시스템 글 + CLI 고정 몫. 절마다 토큰 = k × 바이트(추정). 이어 턴의 앞 대화 = T − a − k × 이번 메시지 바이트(실측 − 추정).

실행: python3 decompose.py   → out/decompose.json · out/turns.csv · 표준 출력 요약
"""

from __future__ import annotations

import csv
import json
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from common import (OUT, A, answer_rows, b, classify_material, date_of, era, md_sets, split_sections,  # noqa: E402
                    turn_tokens)


def fit(rows):
    """첫 턴 → 공통 기울기 k · 판별 절편 a."""
    pts = [(r["prompts"]["consult_now"], b(r["llm_user_message"]), turn_tokens(r)) for r in rows
           if r["llm"].get("mode") == "new" and turn_tokens(r) > 0]
    groups = defaultdict(list)
    for g, x, y in pts:
        groups[g].append((x, y))
    num = den = 0.0
    for v in groups.values():
        mx = statistics.mean(x for x, _ in v)
        my = statistics.mean(y for _, y in v)
        num += sum((x - mx) * (y - my) for x, y in v)
        den += sum((x - mx) ** 2 for x, _ in v)
    k = num / den
    a = {g: statistics.mean(y - k * x for x, y in v) for g, v in groups.items()}
    resid = [y - (a[g] + k * x) for g, x, y in pts]
    return k, a, {"n_points": len(pts), "n_groups": len(groups), "resid_abs_max": round(max(map(abs, resid)), 1),
                  "resid_abs_mean": round(statistics.mean(map(abs, resid)), 1)}


def system_bytes() -> dict:
    """지금 판 시스템 글 바이트(앱 적재기 그대로 · 읽기만)."""
    sys.path.insert(0, str(A))
    from clinic_chat.consult import prompt as pm  # noqa: PLC0415

    p = pm.load(A / "prompts/consult.json")
    t = p.system_text_v3 or p.system_text
    full = t + ("\n\n" + "\n".join(p.kos["rules"]) if p.kos else "")
    return {"system_v3_bytes": b(t), "with_kos_rules_bytes": b(full)}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    rows = answer_rows()
    md = md_sets()
    k, a, fitinfo = fit(rows)
    a_default = statistics.median(a.values())
    try:
        sysb = system_bytes()
    except Exception as e:  # noqa: BLE001
        sysb = {"error": str(e)[:200]}
    # 세션별 앞 턴 바이트(메시지 + 답 원문)
    by_sess = defaultdict(list)
    for r in rows:
        by_sess[r["llm"].get("session_id")].append(r)
    prev_bytes = {}
    for sid, rs in by_sess.items():
        rs.sort(key=lambda r: (r.get("asked_at") or "", r.get("turn") or 0))
        acc = 0
        for r in rs:
            prev_bytes[id(r)] = acc
            if turn_tokens(r) > 0:  # 보낸 턴만 세션에 남는다(fold · 오류 턴은 안 보냄)
                acc += b(r["llm_user_message"]) + b(r.get("answer_raw") or "")
    out = []
    agg_kind = Counter()
    agg_layer = Counter()
    agg_by = Counter()
    for r in rows:
        secs = split_sections(r["llm_user_message"])
        sb = {n: b(t) for n, t in secs.items()}
        T = turn_tokens(r)
        g = r["prompts"]["consult_now"]
        a_g = a.get(g, a_default)
        msg_b = b(r["llm_user_message"])
        sent = T > 0
        if not sent:  # 안 보낸 턴(FT5 fold) — 실측 없음: 추정 = a + k × (메시지 + 앞 대화)
            hist = k * prev_bytes[id(r)]
            T_est = round(a_g + k * msg_b + hist)
        else:
            hist = T - a_g - k * msg_b if r["llm"].get("mode") == "resume" else 0.0
            T_est = T
        mat = classify_material(r, md)
        kinds = Counter()
        layers = Counter()
        bys = Counter()
        waste = Counter()
        for x in mat:
            kinds[x["kind"]] += x["bytes"]
            layers[x["layer"]] += x["bytes"]
            bys[x["by"]] += x["bytes"]
            waste["dup_names"] += x["dup"]
            if x["used"]:
                waste["used"] += x["bytes"]
                continue
            if x["safety"] or x["explicit"]:
                waste["unused_but_safety_or_explicit"] += x["bytes"]
            elif x["by"] == "kd9":
                waste["unused_kd9"] += x["bytes"]
            elif x["md_reach"] is False:
                waste["unused_sub_not_md"] += x["bytes"]
            elif x["summary"]:
                waste["unused_summary"] += x["bytes"]
            else:
                waste["unused_other"] += x["bytes"]
        rec = {
            "conv": r["conv_id"], "c4": r["conv_id"][:4], "turn": r.get("turn"), "date": date_of(r), "era": era(r),
            "mode": r["llm"].get("mode"), "prompt": g[:8], "tokens_real": T, "sent": sent, "tokens_total": T_est,
            "error": (r.get("error") or {}).get("kind") if isinstance(r.get("error"), dict) else r.get("error"),
            "app_est_tokens": round((8454 + 3336 + msg_b) / 3),
            "tokens_parts": r.get("tokens"), "msg_bytes": msg_b,
            "sec_bytes": sb, "sec_tok": {n: round(k * v) for n, v in sb.items()},
            "system_tok": round(a_g), "history_tok": round(hist),
            "history_pred_tok": round(k * prev_bytes[id(r)]), "prev_bytes": prev_bytes[id(r)],
            "mat_rows": len(mat), "mat_used_rows": sum(x["used"] for x in mat),
            "kind_bytes": dict(kinds), "layer_bytes": dict(layers), "by_bytes": dict(bys), "waste_bytes": dict(waste),
            "question": r.get("question"),
            "kinds": [f'{x["code"]}:{x.get("by")}' for x in ((r.get("trace") or {}).get("front") or {}).get("kinds") or []],
        }
        out.append(rec)
        if r["llm"].get("mode"):
            agg_kind.update(kinds)
            agg_layer.update(layers)
            agg_by.update(bys)
    res = {"k_tok_per_byte": k, "a_by_prompt": {g[:8]: round(v) for g, v in a.items()}, "fit": fitinfo,
           "system_bytes_now": sysb, "turns": out}
    (OUT / "decompose.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    cols = ["c4", "turn", "date", "era", "mode", "sent", "tokens_real", "tokens_total", "system_tok", "history_tok", "history_pred_tok"]
    secn = ["judgement", "close", "prev", "consult", "material", "kos", "question"]
    with (OUT / "turns.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols + [f"tok_{s}" for s in secn] + ["mat_rows", "mat_used_rows"])
        for x in out:
            w.writerow([x[c] for c in cols] + [x["sec_tok"].get(s, 0) for s in secn] + [x["mat_rows"], x["mat_used_rows"]])
    print(json.dumps({k2: res[k2] for k2 in ("k_tok_per_byte", "a_by_prompt", "fit", "system_bytes_now")},
                     ensure_ascii=False))
    print("turns", len(out))


if __name__ == "__main__":
    main()
