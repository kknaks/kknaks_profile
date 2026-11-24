"""할 일 3 — 표본 측정: 초안 이해 프롬프트(draft_rules.py 사본)로 소넷을 실제로 불러 턴마다 JSON(`fetch` 포함)을 받고,
그 JSON 대로 2차가 가져왔다면 실릴 「## 자료」 줄을 지금 장부 자료 줄에서 골라 토큰 · 감소 · 빠짐(인용 줄 중 안 실린 것 · 까닭별)을 센다.

표본 = token-cause 와 같은 대화 10 · 자료 있는 턴 43 · 인용 줄 276(`token-cause/jev_measure.py` PICK · build 재사용).
이해 호출 = 앱 `consult/understand.py` 의 `args` · `call` · `turn_message` 그대로(모델 · effort · thinking 끔 같음) — 시스템 글의 규칙만 초안.
허브는 목록(resolve) GET 만. 앱 코드 · 프롬프트 파일 · 데이터 수정 0.

실행(앱 venv):
  cd $A && PYTHONDONTWRITEBYTECODE=1 uv run --no-sync python $W/fetch-plan/measure.py --round 1 [--offline] [--conc 4]
  --offline = out/understand_r<N>.jsonl 에 남긴 JSON 으로 다시 셈(호출 0 · 2차 규칙만 고칠 때)
"""
from __future__ import annotations

import argparse, asyncio, json, re, statistics, sys, time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TC = HERE.parent / "token-cause"
sys.path.insert(0, str(TC)); sys.path.insert(0, str(HERE))
import common  # noqa: E402
import jev_measure as jm  # noqa: E402
import draft_rules  # noqa: E402

LAYERS = {"self": {"자기"}, "inherit": {"자기", "물려받음"}, "sub": {"자기", "물려받음", "하위 시술", "하위 케이스", "하위 제품"}}
NAME_KEYS = re.compile(r"name|^n$")
RULES = 1  # 2차 규칙 판(--rules)


def norm_fetch(j: dict) -> dict:
    f = (j or {}).get("fetch") or {}
    return {"about": f.get("about") or "targets", "kinds": list(f.get("kinds") or []),
            "layers": f.get("layers") if f.get("layers") in LAYERS else "sub",
            "scope": f.get("scope") if f.get("scope") in ("branch", "all") else "branch",
            "lineup": f.get("lineup") if f.get("lineup") in ("none", "names", "detail") else "none",
            "site_filter": list(f.get("site_filter") or [])}


def names_only_bytes(o: dict) -> int:
    return common.b(json.dumps({k: v for k, v in o.items() if NAME_KEYS.search(k)}, ensure_ascii=False)) + 1


_ITEMS: dict | None = None


def item_hub(code: str) -> set[str]:
    """KOS 진료항목 코드 → 허브 코드(table:code) 묶음(매핑 JSON)."""
    global _ITEMS
    if _ITEMS is None:
        _ITEMS = {}
        for it in json.loads(common.MAPPING.read_text())["items"]:
            h = it.get("hub") or {}
            _ITEMS[it["kos_item_code"]] = ({f"procedure_case:{c}" for c in h.get("case_codes") or []}
                                           | {f"procedure:{c}" for c in h.get("procedure_codes") or []}
                                           | {f"product:{p['code']}" for p in h.get("products") or [] if p.get("code")})
    return _ITEMS.get(code, set())


def topic_codes(r: dict) -> set[str]:
    c = r.get("consult") or {}
    for t in c.get("topics") or []:
        if str(t.get("id")) == str(c.get("active_topic")):
            return set().union(set(), *[item_hub(x) for x in t.get("items") or []])
    return set()


def topic_concerns(r: dict) -> set[str]:
    c = r.get("consult") or {}
    act = c.get("active_topic")
    for t in c.get("topics") or []:
        if str(t.get("id")) == str(act):
            return {v.get("name") for v in (t.get("conditions") or {}).get("concern") or [] if v.get("name")}
    return set()


def g2_kinds(j: dict, F: dict, jk: set) -> set:
    """G2 — 앱 `kinds_pick.decide` 의 KS1 · KS3 · KS6 갈래만(KD9 없음 · KS7 기본 덧붙임은 셈 밖).
    about = topic 이면 대상 = 지금 주제 칸(고민 → KS3 indication) + 이번 턴 부위."""
    sys.path.insert(0, str(common.A))
    from clinic_chat.walk.kinds import ATTR4, DEFAULTS, ENTRY_KIND, HOME_RANGE, kinds_for_table, range_of
    tables = [t.get("table") for t in j.get("targets") or [] if isinstance(t, dict) and t.get("table")]
    if F["about"] == "topic":
        tables = tables + ["concern"]
    attr = bool(tables) and all(t in ATTR4 for t in tables)
    by = set(jk)
    for t in tables:
        e = ENTRY_KIND.get(t)
        if e and range_of(e, t, attr):
            by.add(e)
    if not any(range_of(x, t, attr) for x in by for t in tables):
        for t in tables:
            home = ATTR_START_NAME if attr else HOME_RANGE.get(t)
            ks = [x for x in DEFAULTS.get(home or "", ()) if range_of(x, t, attr)] or list(kinds_for_table(t, attr))
            by |= set(ks)
    if RULES >= 6 and "concern" in tables:  # 2차 G2(0.1.1 · 검수 P1-3) — 고민 입구는 후보의 개요도(명동점 밖 후보는 G4 로 이름만)
        by.add("overview")
    return by


ATTR_START_NAME = "attr_start"


def select(turn: dict, j: dict, k: float) -> dict:
    """2차 결정론 — JSON 대로 고른 줄 · 토큰 · 빠짐 까닭."""
    r, b = turn["row"], turn["b"]
    cls, cands, always = b["cls"], b["cands"], set(b["always"])
    F = norm_fetch(j)
    if RULES == 7 and j.get("kind") == "follow" and turn.get("prev"):  # 2차 G4b(0.1.1) — 같은 대상을 이어 물으면 앞 턴 이름만 줄도 상세
        pu = ((turn["prev"][-1].get("consult") or {}).get("understand") or {}).get("accepted") or {}
        pcodes = {x.get("code") for x in pu.get("targets") or []}
        now = {x.get("code") for x in j.get("targets") or [] if isinstance(x, dict)}
        if now and now <= pcodes:
            F = {**F, "scope": "all", "scope_from": "follow"}
    jk = set(j.get("kinds") or []) | set(F["kinds"])
    q = r.get("question") or ""
    tcodes = {t.get("code") for t in j.get("targets") or [] if isinstance(t, dict)}
    g2 = g2_kinds(j, F, jk) if RULES >= 5 else set()
    follow_same = False
    if RULES >= 8 and j.get("kind") == "follow" and turn.get("prev"):
        pu = ((turn["prev"][-1].get("consult") or {}).get("understand") or {}).get("accepted") or {}
        now = {x.get("code") for x in j.get("targets") or [] if isinstance(x, dict)}
        follow_same = bool(now) and now <= {x.get("code") for x in pu.get("targets") or []}
    tcon = topic_concerns(r)
    tcodes_topic = topic_codes(r)
    row_obj, head_of = turn["row_obj"], turn["head_of"]

    def names_bytes(n, o, c):
        """이름만 줄 — 줄 이름 칸 + (R3) 머리도 이름 칸만(머리 몫 나눔)."""
        hb = c["head_bytes"]
        if RULES >= 3 and n in head_of:
            ho, cnt = head_of[n]
            hb = names_only_bytes(ho.get("same") or {}) // max(1, cnt)
        return min(c["bytes"], names_only_bytes(o) + hb)

    owner = {}
    for c in cands:
        for n in c["rows"]:
            owner[n] = c

    def explicit(c):
        if not c:
            return False
        code = c["key"].partition(":")[2]
        nm = re.sub(r"\(.*\)$", "", c["name"])
        return code in tcodes or (len(nm) >= 2 and nm in q)

    keep, why_drop, sizes = {}, {}, Counter()
    thin = set()  # 이름만으로 줄인 줄(인용 줄이면 「얇아진 인용」)
    for n, c in cls.items():
        if n in always:
            keep[n] = c["bytes"]; sizes["요약 · 머리"] += c["bytes"]; continue
        cd = owner.get(n)
        role = c["layer"] if c["layer"] in LAYERS["sub"] else None
        if RULES >= 8 and follow_same and cd and cd["key"] in turn.get("prev_thin_owners", set()):
            keep[n] = c["bytes"]; sizes["앞 턴 이름만 주인(이어 물음)"] += c["bytes"]; continue  # 2차 G4b(0.1.1)
        if explicit(cd):
            keep[n] = c["bytes"]; sizes["명시 대상(강제)"] += c["bytes"]; continue
        if c["safety"]:
            if RULES == 4 and F["scope"] == "branch" and cd and cd["md"] is False and cd["role"] not in ("자기", "물려받음"):
                o = row_obj.get(n) or {}  # 2차 R4(안) — 명동점 밖 하위의 안전 줄은 이름만
                keep[n] = names_bytes(n, o, c); thin.add(n); sizes["안전 · 명동점 밖 이름만"] += keep[n]; continue
            keep[n] = c["bytes"]; sizes["안전(강제)"] += c["bytes"]; continue
        kinds = set(c["kinds"])
        if RULES >= 5:  # 2차 G2(0.1.1) — 새 JSON 으로 종류를 다시 셈: fetch.kinds ∪ kinds ∪ KS3 입구 종류 · 다 비면 KS6 기본 묶음
            ok_kind = bool(kinds & g2)
        elif jk:
            ok_kind = bool(kinds & jk) or c["by"] == "entry"
        else:
            ok_kind = c["by"] != "kd9"
        if not ok_kind:
            why_drop[n] = "종류(KD9 덧붙임)" if c["by"] == "kd9" else "종류(안 물음)"; continue
        o = row_obj.get(n) or {}
        cn = {o.get("concern_name"), o.get("asked_concern_name")} - {None, ""}
        if F["about"] == "topic" and tcon and cn and not (cn & tcon):
            why_drop[n] = "주제 밖(부위만 턴)"; continue
        if (RULES >= 3 and F["about"] == "topic" and not cn and cd and not cd["key"].startswith("name:")
                and tcodes_topic and cd["key"] not in tcodes_topic):
            why_drop[n] = "주제 밖(부위만 턴)"; continue  # 2차 R3 — 부위만 턴: 지금 주제 진료항목에 닿는 대상 줄만
        md_in = bool(cd and cd["md"])
        if RULES >= 2 and md_in and role in ("하위 시술", "하위 케이스", "하위 제품"):
            pass  # 2차 R2 — 명동점 진료항목에 닿는 하위 층은 layers 와 무관하게 읽는다
        elif role and role not in LAYERS[F["layers"]]:
            why_drop[n] = f"층({role})"; continue
        out_md = F["scope"] == "branch" and cd and cd["md"] is False and cd["role"] not in ("자기", "물려받음")
        if out_md and RULES < 2:
            why_drop[n] = "범위(명동점 안 닿음)"; continue
        if out_md:  # 2차 R2 — 명동점 밖 하위 · 후보 행은 이름 칸만(폭은 빠짐없이 · 깊이는 명동점만)
            keep[n] = names_bytes(n, o, c); thin.add(n); sizes["명동점 밖 · 이름만"] += keep[n]; continue
        bb = c["bytes"]
        if "lineup" in kinds and F["lineup"] == "names":
            bb = names_bytes(n, o, c)
            thin.add(n)
        keep[n] = bb
        sizes[f"{'+'.join(sorted(kinds)) or '?'} · {c['layer']} · {'명동점' if (cd or {}).get('md') else ('밖' if (cd or {}).get('md') is False else '-')}"] += bb
    cited = {n for n, c in cls.items() if c["used"]}
    now_b = sum(c["bytes"] for c in cls.values())
    kb = sum(keep.values())
    miss = sorted(cited - set(keep))
    have_kinds = {x for c in cls.values() for x in c["kinds"]}
    return {"keep": sorted(keep), "thin": sorted(thin), "thin_owners": sorted({owner[n]["key"] for n in thin if n in owner}), "now_tok": round(now_b * k), "new_tok": round(kb * k), "cut_pct": round(100 * (1 - kb / now_b), 1) if now_b else 0,
            "cited": len(cited), "miss": len(miss), "thin_cited": len(cited & thin), "thin_rows": [{"n": n, "kind": cls[n]["kind"], "layer": cls[n]["layer"], "owner": (owner.get(n) or {}).get("name")} for n in sorted(cited & thin)], "miss_why": Counter(why_drop[n] for n in miss),
            "miss_rows": [{"n": n, "why": why_drop[n], "kind": cls[n]["kind"], "layer": cls[n]["layer"],
                           "owner": (owner.get(n) or {}).get("name")} for n in miss],
            "need_more_kinds": sorted((g2 or jk) - have_kinds), "fetch": F, "kinds": sorted(jk), "g2": sorted(g2),
            "sizes_top": dict(Counter({k_: round(v * k) for k_, v in sizes.items()}).most_common(6))}


def load_turns(md: dict) -> list[dict]:
    out = []
    for pre, which, why in jm.PICK:
        rows = [r for r in jm.rows_of(which) if r["conv_id"].startswith(pre) and (which == "replay" or not r["conv_id"].startswith("fixE"))]
        rows.sort(key=lambda r: r["turn"])
        for r in rows:
            bld = jm.build(r, md)
            if not bld["cls"]:
                continue
            sec = common.split_sections(r["llm_user_message"]).get("material", "")
            mls = common.material_lines(sec)
            row_obj = {x["obj"]["n"]: x["obj"] for x in mls if x["t"] == "row"}
            head_of = {n: (x["obj"], len(x["obj"].get("lines") or [])) for x in mls if x["t"] == "head"
                       for n in x["obj"].get("lines") or []}
            out.append({"pre": pre, "which": which, "conv": r["conv_id"], "turn": r["turn"], "row": r,
                        "prev": [x for x in rows if x["turn"] < r["turn"]], "b": bld, "row_obj": row_obj, "head_of": head_of})
    return out


async def call_all(turns, rnd: int, conc: int) -> list[dict]:
    sys.path.insert(0, str(common.A))
    from clinic_chat.clients.hub_rest import HubRest
    from clinic_chat.config import load_settings
    from clinic_chat.consult import entry_list as el_mod, understand as und, items_view as iv, topics as tp
    s = load_settings()
    hub = HubRest(s.hub_rest_url, page_limit=s.hub_page_limit)
    el = await el_mod.load(hub, aliases=s.chat_pick_aliases == "on", cache=False)
    pick = draft_rules.build(rnd)
    system = und.system_text(pick, el)
    (HERE / "out").mkdir(exist_ok=True)
    (HERE / f"out/draft_pick_r{rnd}.json").write_text(json.dumps({k: v for k, v in pick.items()}, ensure_ascii=False, indent=1))

    def brief(prev):
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

    sem = asyncio.Semaphore(conc)
    res = [None] * len(turns)

    async def one(i, t):
        prev = t["prev"]
        obj = ((prev[-1].get("consult") or {}).get("after") or {}) if prev else {}
        msg = und.turn_message(prev, obj, t["row"]["question"], pick, s, el, topics=brief(prev))
        async with sem:
            raw = await und.call(s, system, msg)
        txt = raw.output_raw or ""
        i0, i1 = txt.find("{"), txt.rfind("}")  # 앱 verify.parse 와 같은 꼴(첫 { ~ 마지막 })
        try:
            j = json.loads(txt[i0:i1 + 1]) if 0 <= i0 < i1 else None
        except ValueError:
            j = None
        res[i] = {"conv": t["conv"][:8], "turn": t["turn"], "question": t["row"]["question"], "json": j, "raw": None if j else txt[:1500],
                  "error": raw.error, "ms": raw.ms, "api_ms": raw.api_ms, "usage": raw.usage,
                  "sys_bytes": common.b(system), "msg_bytes": common.b(msg)}
        print(f"  {t['conv'][:4]} T{t['turn']} {raw.ms}ms {'OK' if j else 'BAD'}", flush=True)

    await asyncio.gather(*(one(i, t) for i, t in enumerate(turns)))
    with open(HERE / f"out/understand_r{rnd}.jsonl", "w") as f:
        for x in res:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--from-round", type=int, default=None, help="--offline 일 때 읽을 JSON 회차")
    ap.add_argument("--conc", type=int, default=4)
    ap.add_argument("--rules", type=int, default=1, help="2차 규칙 판 — 1 첫 판 · 2 명동점 닿는 하위 늘 · 밖은 이름만 · 3 부위만 턴은 주제 진료항목 대상만 · 이름만 줄은 머리도 이름만 · 4(안) 명동점 밖 하위 안전 줄도 이름만 · 5 = 3 + G2 종류를 새 JSON 으로 다시 셈(KS3 입구 · KS6 기본) · 6 = 5 + 고민 입구에 overview · 7(안) = 6 + 같은 대상 follow 면 scope all · 8 = 6 + 같은 대상 follow 면 앞 턴 이름만 주인의 줄은 상세")
    a = ap.parse_args()
    global RULES
    RULES = a.rules
    md = common.md_sets()
    k = json.loads((TC / "out/decompose.json").read_text())["k_tok_per_byte"]
    turns = load_turns(md)
    print("turns with material", len(turns), "cited", sum(sum(1 for c in t["b"]["cls"].values() if c["used"]) for t in turns))
    if a.offline:
        src = a.from_round or a.round
        res = [json.loads(x) for x in (HERE / f"out/understand_r{src}.jsonl").read_text().splitlines()]
    else:
        res = asyncio.run(call_all(turns, a.round, a.conc))
    per = []
    for t, u in zip(turns, res):
        j = u["json"] or {}
        sc = select(t, j, k)
        per.append({"conv": t["conv"][:4], "turn": t["turn"], "question": t["row"]["question"],
                    "old_kinds": [x["code"] + ":" + x["by"] for x in ((t["row"].get("trace") or {}).get("front") or {}).get("kinds") or []],
                    "json_ok": bool(u["json"]), "ms": u["ms"], "usage": u["usage"], **sc})
    tot_now = sum(p["now_tok"] for p in per); tot_new = sum(p["new_tok"] for p in per)
    cited = sum(p["cited"] for p in per); miss = sum(p["miss"] for p in per)
    why = Counter()
    for p in per:
        why.update(p["miss_why"])
    summ = {"round": a.round, "rules": a.rules, "json_round": a.from_round or a.round, "turns": len(per), "now_tok": tot_now, "new_tok": tot_new,
            "cut_pct": round(100 * (1 - tot_new / tot_now), 1), "cited": cited, "miss": miss,
            "miss_pct": round(100 * miss / cited, 1), "thin_cited": sum(p["thin_cited"] for p in per), "miss_why": dict(why), "miss_turns": sum(1 for p in per if p["miss"]),
            "json_bad": sum(1 for p in per if not p["json_ok"]),
            "ms_median": statistics.median([p["ms"] for p in per if p["ms"]]),
            "ms_max": max([p["ms"] for p in per if p["ms"]]),
            "usage_sum": {kk: sum(int((p["usage"] or {}).get(kk) or 0) for p in per)
                          for kk in ("input_tokens", "cache_read_input_tokens", "output_tokens")}}
    tag = f"r{a.round}_rules{a.rules}" + (f"_from{a.from_round}" if a.from_round else "")
    (HERE / f"out/measure_{tag}.json").write_text(json.dumps({"summary": summ, "turns": per}, ensure_ascii=False, indent=1, default=list))
    print(json.dumps(summ, ensure_ascii=False, indent=1))
    for p in per:
        print(f"{p['conv']} T{p['turn']} {p['question'][:28]!r:32} kinds={p['kinds']} f={p['fetch']['about']}/{p['fetch']['layers']}/{p['fetch']['scope']}/{p['fetch']['lineup']} "
              f"{p['now_tok']}→{p['new_tok']} miss {p['miss']}/{p['cited']} {dict(p['miss_why'])} more={p['need_more_kinds']}")


if __name__ == "__main__":
    main()
