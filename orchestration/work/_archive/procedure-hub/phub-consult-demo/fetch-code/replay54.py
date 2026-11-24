"""SPEC-011 WP-1 · WP-2 완료 조건 ①② ③ ④ — 앱 프롬프트(pick 0.6.0-draft)로 실제 이해 호출 → 앱 2차 함수(`consult.fetch_read`)로 셈.

모음 = fetch-plan `run4.py` 와 같은 표본 43 + 표본 밖(지금 시대) 턴. 시대 판정 = `kinds_by` + `consult.understand` 기록 유무(검수 P2-15).
셈 = 장부 자료 줄(지금 앱이 실은 그대로)에 앱 `fetch_read.decide` 를 돌려 전체 · 이름만 · 뺌 → 바이트(줄 + 머리 몫) × k.
  빠짐 = 인용 줄이 뺌 · 상세 잃음 = 인용 줄이 이름만(lineup 아님) · lineup 이름만 = 따로.
④ offered(KD11) 전후 = 장부 `trace.front.offered`(옛 앱 · KD9 있음) ↔ 앱 `kinds_pick.decide`(KS5 끔 · fetch.kinds) 를 같은 입구로.
⑤ (잼) 입구 목록 「명동점 없음」 표지 — FR13b 02af T3 · FR14 dc78 T4 두 턴만 표지 단 목록으로 다시 불러 scope 를 본다(`--mark`).

실행(앱 venv): cd $A && PYTHONDONTWRITEBYTECODE=1 uv run --no-sync python $W/fetch-code/replay54.py [--offline] [--mark]
"""
from __future__ import annotations

import argparse, asyncio, json, re, statistics, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = HERE.parent
sys.path.insert(0, str(W / "token-cause")); sys.path.insert(0, str(W / "fetch-plan"))
import common  # noqa: E402
import jev_measure as jm  # noqa: E402
import measure as M  # noqa: E402
import run4  # noqa: E402

sys.path.insert(0, str(common.A))
from clinic_chat.consult import fetch_read as fr  # noqa: E402
from clinic_chat.consult import kinds_pick as kp  # noqa: E402
from clinic_chat.consult import verify as vf  # noqa: E402
from clinic_chat.walk.calls import Entry  # noqa: E402

OUT = HERE / "out"
APP_PICK = json.loads((common.A / "prompts/consult.json").read_text())["pick"]


def era(r: dict) -> str:
    kb = ((r.get("trace") or {}).get("front") or {}).get("kinds_by") or "?"
    if not (r.get("consult") or {}).get("understand"):
        return "jev"
    return kb


def lines_of(r: dict) -> tuple[list[fr.Line], dict, dict]:
    sec = common.split_sections(r["llm_user_message"]).get("material", "")
    mls = common.material_lines(sec)
    nl = {x["n"]: x for x in (r.get("material") or {}).get("new_lines") or []}
    head_of, row_obj = {}, {}
    for x in mls:
        if x["t"] == "head":
            for n in x["obj"].get("lines") or []:
                head_of[n] = x["obj"]
        elif x["t"] == "row":
            row_obj[x["obj"]["n"]] = x["obj"]
    out = []
    for n, o in row_obj.items():
        m = nl.get(n, {})
        if o.get("summary") or m.get("summary"):
            out.append(fr.Line(key=str(n), kinds=[], layer=None, silver_table=None, silver_id=None, row=o))
            continue
        row = {**((head_of.get(n) or {}).get("same") or {}), **o}
        out.append(fr.Line(key=str(n), kinds=list(m.get("kind") or []), layer=m.get("layer") if isinstance(m.get("layer"), dict) else None,
                           silver_table=m.get("silver_table"), silver_id=m.get("silver_id"), row=row))
    return out, head_of, row_obj


def cur_topic(r: dict) -> dict | None:
    c = r.get("consult") or {}
    return next((t for t in c.get("topics") or [] if str(t.get("id")) == str(c.get("active_topic"))), None)


def cut_turn(r: dict, j: dict, kos, md, k: float) -> dict:
    lines, head_of, row_obj = lines_of(r)
    cls = {x["n"]: x for x in common.classify_material(r, {"procedure_case": set(), "procedure": set(), "product": set()})}
    plan = fr.Plan.of(vf.fetch_of(j.get("fetch")))
    plan.layers = "sub"
    tg = [t for t in j.get("targets") or [] if isinstance(t, dict)]
    tables = [t.get("table") for t in tg if t.get("table")] + ["site" for s in j.get("sites") or [] if s and "site" not in [t.get("table") for t in tg]]
    cur = cur_topic(r)
    ctx = fr.Ctx(targets={t.get("code") for t in tg}, question=r.get("question") or "", md=md,
                 g2=fr.g2_kinds(tables, list(j.get("kinds") or []), plan),
                 topic_concerns={v.get("name") for v in ((cur or {}).get("conditions") or {}).get("concern") or [] if v.get("name")},
                 topic_codes=fr.topic_codes(kos, (cur or {}).get("items")))
    dec = fr.decide(lines, plan, ctx)
    cited = common.cited_rows(r)
    now_b = new_b = 0
    miss, lose, lineup_names, why = [], [], 0, Counter()
    for ln in lines:
        n = int(ln.key)
        c = cls.get(n) or {"bytes": 0, "head_bytes": 0}
        now_b += c["bytes"]
        fate, w = dec.get(ln.key, ("full", ""))
        why[f"{fate}:{w}"] += 1
        if fate == "full":
            new_b += c["bytes"]
        elif fate == "names":
            o = row_obj.get(n) or {}
            body = common.b(json.dumps({"n": n, **fr.names_only({kk: v for kk, v in o.items() if kk not in ("n", "marks")})}, ensure_ascii=False)) + 1
            ho = head_of.get(n)
            hb = (common.b(json.dumps(fr.names_only((ho or {}).get("same") or {}), ensure_ascii=False)) // max(1, len((ho or {}).get("lines") or []))) if ho else 0
            new_b += min(c["bytes"], body + hb)
        if n in cited:
            if fate == "drop":
                miss.append({"n": n, "why": w, "kind": ln.kinds})
            elif fate == "names":
                if "lineup" in ln.kinds:
                    lineup_names += 1
                else:
                    lose.append({"n": n, "why": w, "kind": ln.kinds, "owner": fr.owner(ln)[1]})
    return {"now_tok": round(now_b * k), "new_tok": round(new_b * k), "cited": len(cited & {int(x.key) for x in lines}),
            "miss": miss, "lose": lose, "lineup_names": lineup_names, "fetch": plan.view(), "g2": sorted(ctx.g2),
            "lines": dict(why)}


def offered_cmp(r: dict, j: dict) -> dict:
    old = [o.get("code") for o in ((r.get("trace") or {}).get("front") or {}).get("offered") or []]
    ents = [Entry(t["table"], t["code"], t.get("name") or "", "target") for t in r.get("targets") or [] if t.get("table") and t.get("code")]
    acc_kinds = ((((r.get("consult") or {}).get("understand") or {}).get("accepted")) or {}).get("kinds") or []
    if not ents:
        return {"old": old, "new": [], "old_kd9": [], "new_kinds": []}
    f = vf.fetch_of(j.get("fetch"))
    new = kp.decide(ents, list(j.get("kinds") or acc_kinds), {}, fetch_kinds=f["kinds"])
    old_by = {x.get("code"): x.get("by") for x in ((r.get("trace") or {}).get("front") or {}).get("kinds") or []}
    return {"old": old, "new": [o["code"] for o in new.offered], "old_kd9": sorted(k_ for k_, b in old_by.items() if b == "kd9"),
            "old_kinds": sorted(old_by), "new_kinds": sorted(new.kinds), "new_by": new.by}


async def call_all(turns, conc: int, mark: bool = False) -> list[dict]:
    from clinic_chat.clients.hub_rest import HubRest
    from clinic_chat.config import load_settings
    from clinic_chat.consult import entry_list as el_mod, understand as und

    s = load_settings()
    hub = HubRest(s.hub_rest_url, page_limit=s.hub_page_limit)
    el = await el_mod.load(hub, aliases=s.chat_pick_aliases == "on", cache=False)
    system = und.system_text(APP_PICK, el)
    if mark:
        system = mark_list(system)
    sem = asyncio.Semaphore(conc)
    res: list = [None] * len(turns)

    async def one(i, t):
        prev = t["prev"]
        obj = ((prev[-1].get("consult") or {}).get("after") or {}) if prev else {}
        msg = und.turn_message(prev, obj, t["row"]["question"], APP_PICK, s, el, topics=M_brief(prev, s))
        async with sem:
            raw = await und.call(s, system, msg)
        try:
            j = vf.parse(raw.output_raw)
        except vf.UnderstandJSONError:
            j = None
        res[i] = {"conv": t["conv"][:8], "turn": t["turn"], "question": t["row"]["question"], "json": j,
                  "bad_raw_bytes": None if j else len((raw.output_raw or "").encode()), "error": raw.error, "ms": raw.ms,
                  "usage": raw.usage, "models": raw.models, "sys_bytes": common.b(system), "msg_bytes": common.b(msg)}
        print(f"  {t['conv'][:4]} T{t['turn']} {raw.ms}ms {'OK' if j else 'BAD'} fetch={'Y' if j and 'fetch' in j else 'N'}", flush=True)

    await asyncio.gather(*(one(i, t) for i, t in enumerate(turns)))
    return res


def M_brief(prev, s):
    from clinic_chat.consult import items_view as iv, topics as tp
    if not prev:
        return None
    c = prev[-1].get("consult") or {}
    topics = c.get("topics") or []
    cur = next((t for t in topics if str(t.get("id")) == str(c.get("active_topic"))), None)

    def one(t):
        return {"id": str(t["id"]), "conds": iv.cond_names(t.get("conditions")), "n": len(t.get("items") or []),
                "slots": iv.cond_tuple(t.get("conditions"))}
    pv = tp.visible_prev(topics, cur, s.chat_topic_max) if cur else []
    return {"current": one(cur) if cur else None, "prev": [one(t) for t in pv]}


def mark_list(system: str) -> str:
    """(잼) 입구 목록의 시술 · 케이스 · 제품 줄 가운데 명동점 매핑에 없는 코드 뒤에 표지 「(명동점 없음)」."""
    md = common.md_sets()
    out = []
    table = None
    for ln in system.split("\n"):
        m = re.match(r"^## .*\(table = (\w+)\)$", ln)
        if m:
            table = m.group(1)
        else:
            mm = re.match(r"^(\S+) ", ln)
            if table in md and mm and mm.group(1) not in md[table]:
                ln = ln + " (명동점 없음)"
        out.append(ln)
    return "\n".join(out)


def summarize(per: list[dict]) -> dict:
    g = Counter()
    for p in per:
        g["turns"] += 1
        for kk in ("now_tok", "new_tok", "cited", "lineup_names"):
            g[kk] += p[kk]
        g["miss"] += len(p["miss"]); g["lose_detail"] += len(p["lose"])
    g["cut_pct"] = round(100 * (1 - g["new_tok"] / g["now_tok"]), 1) if g["now_tok"] else 0
    return dict(g)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--mark", action="store_true")
    a = ap.parse_args()
    from clinic_chat.consult import kos_map
    kos = kos_map.load(common.MAPPING)
    md = fr.md_sets(kos)
    k = json.loads((W / "token-cause/out/decompose.json").read_text())["k_tok_per_byte"]
    mdset = common.md_sets()
    sample = M.load_turns(mdset)
    outside = [t for t in run4.outside_turns(mdset) if era(t["row"]) != "jev"]
    sets = {"sample": sample, "outside": outside}
    OUT.mkdir(exist_ok=True)
    print({kk: len(v) for kk, v in sets.items()}, flush=True)
    if a.mark:
        pick = [t for t in sample if (t["conv"][:4], t["turn"]) in (("02af", 3), ("dc78", 4))]
        res = asyncio.run(call_all(pick, 2, mark=True))
        base = {(x["conv"][:4], x["turn"]): x for x in (json.loads(l) for l in (OUT / "understand_sample.jsonl").read_text().splitlines())}
        rows = []
        for t, u in zip(pick, res):
            b0 = base.get((t["conv"][:4], t["turn"])) or {}
            rows.append({"turn": f"{t['conv'][:4]} T{t['turn']}", "q": t["row"]["question"],
                         "scope_plain": ((b0.get("json") or {}).get("fetch") or {}).get("scope"),
                         "scope_marked": ((u["json"] or {}).get("fetch") or {}).get("scope"),
                         "sys_bytes_marked": u["sys_bytes"], "sys_bytes_plain": b0.get("sys_bytes"),
                         "cut_plain": cut_turn(t["row"], b0.get("json") or {}, kos, md, k) if b0 else None,
                         "cut_marked": cut_turn(t["row"], u["json"] or {}, kos, md, k)})
        (OUT / "mark_check.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
        for x in rows:
            print(x["turn"], x["q"], x["scope_plain"], "->", x["scope_marked"], "lose", len((x["cut_plain"] or {}).get("lose", [])), "->", len(x["cut_marked"]["lose"]))
        return
    res = {}
    for name, ts in sets.items():
        p = OUT / f"understand_{name}.jsonl"
        if a.offline:
            res[name] = [json.loads(x) for x in p.read_text().splitlines()]
        else:
            res[name] = asyncio.run(call_all(ts, 4))
            p.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in res[name]))
    out = {}
    for name, ts in sets.items():
        per = []
        for t, u in zip(ts, res[name]):
            j = u["json"] or {}
            c = cut_turn(t["row"], j, kos, md, k)
            per.append({"conv": t["conv"][:4], "turn": t["turn"], "question": t["row"]["question"], "era": era(t["row"]),
                        "json_ok": bool(u["json"]), "fetch_present": bool(u["json"] and "fetch" in u["json"]),
                        "fetch_fixed": vf.fetch_of(j.get("fetch"))["fixed"], "ms": u["ms"], "usage": u["usage"],
                        "offered": offered_cmp(t["row"], j), **c})
        eras = {}
        for e in sorted({p["era"] for p in per}):
            eras[e] = summarize([p for p in per if p["era"] == e])
        out[name] = {"summary": {**summarize(per), "eras": eras, "json_bad": sum(1 for p in per if not p["json_ok"]),
                                 "fetch_missing": sum(1 for p in per if p["json_ok"] and not p["fetch_present"]),
                                 "fetch_fixed_turns": sum(1 for p in per if p["fetch_fixed"]),
                                 "out_tok_median": statistics.median([(p["usage"] or {}).get("output_tokens") or 0 for p in per]),
                                 "ms_median": statistics.median([p["ms"] or 0 for p in per])},
                     "turns": per}
        print(name, json.dumps(out[name]["summary"], ensure_ascii=False), flush=True)
    (OUT / "replay54.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=list))


if __name__ == "__main__":
    main()
