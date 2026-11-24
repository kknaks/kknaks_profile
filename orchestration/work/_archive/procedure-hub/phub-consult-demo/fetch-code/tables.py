"""replay54.json · 실물 재생 장부 → 리포트 표(markdown). 실행: python3 tables.py <옛 장부> <재생 장부 off> <재생 장부 on> > out/tables.md

실물 재생 장부(병원 가격이 든 명동점 블록 포함)는 스크래치에 두고 여기서는 수 · 답 앞 2 줄만 뽑는다.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = HERE.parent
sys.path.insert(0, str(W / "token-cause"))
import common  # noqa: E402

NO_INFO = re.compile(r"정보(가|는)? ?없|자료(가|에)? ?없|안내할 (자료|정보)가 없")


def table(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])


def rows_of(p):
    return [json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()]


def replay54():
    d = json.loads((HERE / "out/replay54.json").read_text())
    out = []
    for name in ("sample", "outside"):
        s = d[name]["summary"]
        for e, g in [("전체", s)] + list(s["eras"].items()):
            out.append([name, e, g["turns"], f'{g["now_tok"]:,} → {g["new_tok"]:,}', f'−{g["cut_pct"]}%',
                        f'{g["miss"]} / {g["cited"]}', g["lose_detail"], g["lineup_names"]])
    print("### ① ② ③ 표본 43 · 지금 시대 밖 11 — 앱 프롬프트 0.6.0-draft 실제 이해 호출 + 앱 `fetch_read.decide`\n")
    print(table(["모음", "시대", "턴", "「## 자료」 토큰(× k 0.458)", "감소", "빠짐 / 인용", "상세 잃음", "lineup 이름만"], out))
    print()
    for name in ("sample", "outside"):
        s = d[name]["summary"]
        print(f"- {name}: JSON 깨짐 {s['json_bad']} · fetch 빠짐 {s['fetch_missing']} · fetch 고침 턴 {s['fetch_fixed_turns']} · "
              f"이해 출력 중앙 {s['out_tok_median']} 토큰 · 이해 ms 중앙 {s['ms_median']}")
    lose = [(t["conv"], t["turn"], x) for n in ("sample", "outside") for t in d[n]["turns"] for x in t["lose"]]
    print("\n상세 잃음 줄:\n")
    print(table(["턴", "줄", "까닭", "종류", "주인"], [[f"{c} T{t}", x["n"], x["why"], "+".join(x["kind"]), x["owner"]] for c, t, x in lose]))
    # ④ offered
    rows, diff = [], Counter()
    for n in ("sample", "outside"):
        for t in d[n]["turns"]:
            o = t["offered"]
            old, new = set(o["old"]), set(o["new"])
            if old != new or o.get("old_kd9"):
                rows.append([f'{t["conv"]} T{t["turn"]}', (t["question"] or "")[:22], ",".join(sorted(o.get("old_kd9") or [])) or "-",
                             ",".join(sorted(old)) or "-", ",".join(sorted(new)) or "-",
                             ",".join(sorted(set(o.get("old_kinds") or []) - set(o.get("new_kinds") or []))) or "-",
                             ",".join(sorted(set(o.get("new_kinds") or []) - set(o.get("old_kinds") or []))) or "-"])
            diff["same" if old == new else "changed"] += 1
    print(f"\n### ④ offered(KD11) 전후 — 같은 입구 · 옛 = 장부 `trace.front.offered`(KD9 있음) · 새 = 앱 `kinds_pick.decide`(KS5 끔 · fetch.kinds) · 같음 {diff['same']} · 달라짐 {diff['changed']}\n")
    print(table(["턴", "질문", "옛 kd9 종류", "옛 offered", "새 offered", "읽는 종류 빠짐(옛−새)", "읽는 종류 더함(새−옛)"], rows))


def tok4(c):
    return f'{c.get("input") if c.get("input") is not None else "null"}/{c.get("cache_creation") if c.get("cache_creation") is not None else "null"}/' \
           f'{c.get("cache_read") if c.get("cache_read") is not None else "null"}/{c.get("output") if c.get("output") is not None else "null"}'


def old_calls(r):
    t = r.get("tokens") or {}
    u = ((r.get("consult") or {}).get("understand") or {}).get("usage") or {}
    return ({"input": u.get("input_tokens"), "cache_creation": u.get("cache_creation_input_tokens"),
             "cache_read": u.get("cache_read_input_tokens"), "output": u.get("output_tokens")},
            {"input": t.get("input_tokens"), "cache_creation": t.get("cache_creation_input_tokens"),
             "cache_read": t.get("cache_read_input_tokens"), "output": t.get("output_tokens")})


def total(c):
    return sum(int(c.get(k) or 0) for k in ("input", "cache_creation", "cache_read"))


def live(old_main, old_replay, off_p, on_p):
    old = {}
    for p, pre in ((old_main, ("03b8", "73bd")), (old_replay, ("fixEecc6",))):
        for r in rows_of(p):
            if r.get("phase") == "end" and any(r["conv_id"].startswith(x) for x in pre) and (p == old_replay or not r["conv_id"].startswith("fixE")):
                old.setdefault(r["conv_id"][:4] if not r["conv_id"].startswith("fixE") else "ecc6", {})[r["turn"]] = r
    names = json.loads((HERE / "out/live_on.json").read_text())
    names_off = json.loads((HERE / "out/live_off.json").read_text())
    on = {r["conv_id"]: {} for r in []}
    on_rows = [r for r in rows_of(on_p) if r.get("phase") == "end"]
    off_rows = [r for r in rows_of(off_p) if r.get("phase") == "end"]
    by_on = {(r["conv_id"], r["turn"]): r for r in on_rows}
    by_off = {(r["conv_id"], r["turn"]): r for r in off_rows}
    print("\n### 실물 3 대화 — 전(옛 장부) → 후(이번 앱 · 잘라 내기 켬) · 칸 = input / cache_creation / cache_read / output\n")
    rows, held = [], []
    sums = Counter()
    for nm in ("03b8", "ecc6", "73bd"):
        cid = names[nm]["conv_id"]
        cid_off = names_off[nm]["conv_id"]
        for t in names[nm]["turns"]:
            n = t["turn"]
            o = old.get(nm, {}).get(n)
            r = by_on.get((cid, n))
            ro = by_off.get((cid_off, n))
            ou, oa = old_calls(o) if o else ({}, {})
            calls = {c["role"]: c for c in ((r or {}).get("tokens") or {}).get("calls") or []}
            nu, na = calls.get("understand") or {}, calls.get("answer") or {}
            mat_old = common.b(common.split_sections(o["llm_user_message"]).get("material", "")) if o and o.get("llm_user_message") else None
            mat_new = common.b(common.split_sections(r["llm_user_message"]).get("material", "")) if r and r.get("llm_user_message") else None
            ans = ((r or {}).get("answer") or "").strip().split("\n")
            ans2 = " / ".join(x.strip() for x in ans if x.strip())[:0]
            noinfo = len(NO_INFO.findall((r or {}).get("answer") or ""))
            f = ((r or {}).get("consult") or {}).get("fetch") or {}
            rows.append([f"{nm} T{n}", t["q"][:18], tok4(ou) if o else "-", tok4(nu), tok4(oa) if o else "-", tok4(na),
                         f"{total(oa):,} → {total(na):,}" if o else f"- → {total(na):,}",
                         f"{mat_old:,} → {mat_new:,}" if mat_old is not None and mat_new is not None else f"- → {mat_new}",
                         f'{f.get("about")}/{",".join(f.get("kinds") or []) or "[]"}/{f.get("scope")}/{f.get("lineup")}', noinfo])
            if o:
                sums["old_ans"] += total(oa); sums["new_ans"] += total(na)
                sums["old_mat"] += mat_old or 0; sums["new_mat"] += mat_new or 0
            sums["new_und_cc"] += int(nu.get("cache_creation") or 0)
            # 맞추지 않은 턴(잘라 내기 끔) — 인용 줄 vs 판단
            if ro:
                cited = common.cited_rows(ro)
                would = {x["n"]: x.get("fetch_would") for x in (ro.get("material") or {}).get("new_lines") or [] if x.get("fetch_would")}
                nl = {x["n"]: x for x in (ro.get("material") or {}).get("new_lines") or []}
                miss = [k for k in cited if (would.get(k) or "").startswith("drop")]
                lose = [k for k in cited if (would.get(k) or "").startswith("names") and "lineup" not in (nl.get(k) or {}).get("kind", [])]
                lname = [k for k in cited if (would.get(k) or "").startswith("names") and "lineup" in (nl.get(k) or {}).get("kind", [])]
                und = ((ro.get("consult") or {}).get("understand") or {})
                mat_off = common.b(common.split_sections(ro["llm_user_message"]).get("material", "")) if ro.get("llm_user_message") else 0
                held.append([f"{nm} T{n}", "ok" if und.get("parsed") is not None else f'깨짐 {und.get("error")}',
                             "있음" if (und.get("parsed") or {}).get("fetch") is not None else "없음",
                             len(cited & set(nl)), len(miss), len(lose), len(lname), f"{mat_off:,}",
                             dict(Counter((v or ":").split(":")[0] for v in would.values()))])
    print(table(["턴", "말", "이해 전", "이해 후", "답 전", "답 후", "답 입력 합 전 → 후", "「## 자료」 바이트 전 → 후", "fetch(about/kinds/scope/lineup)", "「정보 없음」 류 문장"], rows))
    print(f"\n합(전이 있는 턴): 답 입력 {sums['old_ans']:,} → {sums['new_ans']:,} · 「## 자료」 바이트 {sums['old_mat']:,} → {sums['new_mat']:,} · 이해 캐시 쓰기(새로 남김) 합 {sums['new_und_cc']:,}")
    print("\n### 맞추지 않은 새 턴(11-23 · 잘라 내기 끔으로 다 실은 답의 인용 줄 ↔ 2차 판단)\n")
    print(table(["턴", "이해 JSON", "fetch", "인용 줄", "빠짐(뺌)", "상세 잃음(이름만)", "lineup 이름만", "「## 자료」 바이트(끔)", "판단 수"], held))


def answers(on_p):
    names = json.loads((HERE / "out/live_on.json").read_text())
    by = {(r["conv_id"], r["turn"]): r for r in rows_of(on_p) if r.get("phase") == "end"}
    print("\n### 답 앞 2 줄(잘라 내기 켬)\n")
    rows = []
    for nm in ("03b8", "ecc6", "73bd"):
        for t in names[nm]["turns"]:
            r = by.get((names[nm]["conv_id"], t["turn"])) or {}
            ls = [x.strip() for x in (r.get("answer") or "").split("\n") if x.strip()][:2]
            rows.append([f"{nm} T{t['turn']}", " / ".join(ls).replace("|", "¦")[:160]])
    print(table(["턴", "답 앞 2 줄"], rows))


if __name__ == "__main__":
    replay54()
    if len(sys.argv) >= 5:
        live(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        answers(sys.argv[4])
