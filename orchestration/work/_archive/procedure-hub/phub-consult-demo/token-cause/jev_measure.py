"""할 일 3 — Jev 문서 방식(llms.txt §2 · §3) 측정: 후보마다 Noul 하나 · 한 요청(fan-out) · 지시문 영어.

후보 = 그 턴 「## 자료」 에 실린 묶음의 (주인 노드 × 칸) — 주인 = 층 표지의 holder(케이스 · 제품 · 시술 · 계열) 또는 묶음 머리 이름.
후보 줄 = ID · 이름 · 연결 이유(층 · 명동점 진료항목 닿음) · 칸(영어 종류 이름). state = question · targets · unresolved · candidates.
고른 후보의 줄만 읽었다고 치고 「## 자료」 토큰 · 빠짐(지금 답이 인용한 줄 중 안 고른 것)을 임계값별로 센다.
Jev 응답은 out/jev_raw.jsonl 에 남기고 `--offline` 으로 다시 셈(호출 0).

실행(앱 venv · 키는 앱 .env — 값 출력 0):
  cd $A && PYTHONDONTWRITEBYTECODE=1 uv run --no-sync python $W/token-cause/jev_measure.py [--dry] [--offline]
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common  # noqa: E402

KIND_EN = {
    "overview": "what it is (overview, category, device/material/method)",
    "mechanism": "how it works (mechanism / principle)",
    "indication": "what it is used for / what is done for a concern",
    "outcome": "effects and how long they take / last",
    "lineup": "what belongs under it (products, procedures, cases)",
    "adverse": "side effects / adverse events",
    "recovery": "recovery / downtime",
    "contraindication": "who should not have it (patient conditions)",
    "avoid": "what must not be combined with it",
    "combo": "what goes well together with it",
    "package": "packages / programs that include it or target a concern",
    "same_day": "whether things can be done on the same day",
    "order_interval": "order, interval, repeat interval",
    "offer": "products for sale and prices",
}
ROLE_EN = {"자기": "the asked target itself", "물려받음": "inherited from a parent category of the asked target",
           "하위 시술": "a procedure under the asked target", "하위 케이스": "a treatment case under the asked target",
           "하위 제품": "a product/device under the asked target", None: "listed for the asked concern or body site"}
PICK = [  # (대화 앞 글자, 장부, 고른 까닭)
    ("03b8", "main", "고민 → 고민 추가 → 부위 → 제품 셋 → 원리 질문 → 전반 설명(41k 자료) — 사용자 지목"),
    ("fixEecc6", "replay", "고민 → 부위만(「얼굴에」 — 기본 묶음 indication 19만 토큰) — 사용자 지목 · 장부 판은 접힘이라 테스트 고침 E 재생 장부"),
    ("73bd", "main", "고민 → 부위 둘 → 부위별 시술 — 사용자 지목"),
    ("3016", "main", "부작용 질문(자료 80k · 지금 시대 최대 턴)"),
    ("a7d7", "main", "보톡스 고르기 → 원리 질문 「볼뉴머가 머야」 · 긴 대화(8 턴)"),
    ("a578", "main", "기기 리프팅 추천(자료 21k) → 제품 → 효과 확인 「슈링크로 턱라인 …돼?」"),
    ("5bce", "main", "시술 한정 질문 「미간주름에 보톡스만 가능해?」(자료 27k)"),
    ("dc78", "main", "제품(써마지) · 회차 질문 · 9 턴"),
    ("02af", "main", "부위+고민(이마주름) · 0.5 명동점 블록 · 오늘 판"),
    ("7897", "main", "시술 개요 「볼뉴머에 대해서 설명해줄래」"),
]
THRESH = (0.3, 0.5, 0.7)
# 테스트 고침 E 재생 장부(병원 가격 포함 — 폴더에 복사하지 않고 원래 자리에서 읽는다)
REPLAY = Path(os.environ.get("REPLAY_LEDGER", "/private/tmp/claude-501/-Users-kknaks-orca-workspaces-clinic-chat-phub-consult-demo/"
                             "a6af7bd8-5374-42fc-854f-496eb6878c39/scratchpad/fixEchat/turns.jsonl"))
CHUNK = 80  # 요청 하나 후보 수 — state + 질문 전체 64k 토큰 · 질문 하나 32k 한도 아래로(실측 usage 로 확인)


def rows_of(which: str) -> list[dict]:
    common.LEDGER = REPLAY if which == "replay" else common.A / "runs/consult/turns.jsonl"
    return common.answer_rows()


def owner_of(meta: dict, head: dict, row: dict | None = None) -> tuple[str, str, str | None]:
    """(주인 키, 이름, 층) — holder 가 있으면 그 코드 · lineup 줄은 줄의 holder_name · role."""
    row = row or {}
    lay = meta.get("layer") if isinstance(meta.get("layer"), dict) else None
    if lay:
        h = lay.get("holder") or {}
        return f'{h.get("holder_table")}:{h.get("holder_code")}', h.get("holder_name") or "", lay.get("role")
    st = meta.get("silver_table")
    if st in ("procedure_case", "product", "procedure", "modality"):
        same = head.get("same") or {}
        if row.get("holder_name"):
            return f"{st}:{meta.get('silver_id')}", row["holder_name"], row.get("role")
        nm = same.get("name_ko") or same.get("procedure_name") or same.get("candidate_name") or same.get("subject_name") or ""
        site = same.get("case_site_name") or same.get("site_name") or ""
        return f"{st}:{meta.get('silver_id')}", f"{nm}({site})" if site else nm, None
    same = head.get("same") or {}
    nm = same.get("target_name") or same.get("candidate_name") or (head.get("marks") or {}).get("speak_name") or \
        same.get("procedure_name") or same.get("concern_name") or "?"
    site = same.get("case_site_name") or ""
    return f"name:{nm}|{site}", f"{nm}({site})" if site else nm, None


def md_reach(key: str, md: dict) -> bool | None:
    t, _, c = key.partition(":")
    return (c in md[t]) if t in md else None


def build(r: dict, md: dict) -> dict:
    msg = r["llm_user_message"]
    sec = common.split_sections(msg).get("material", "")
    lines = common.material_lines(sec)
    nl = {x["n"]: x for x in (r.get("material") or {}).get("new_lines") or []}
    cls = {x["n"]: x for x in common.classify_material(r, md)}
    head_of = {}
    row_obj = {}
    for x in lines:
        if x["t"] == "head":
            for n in x["obj"].get("lines") or []:
                head_of[n] = x["obj"]
        elif x["t"] == "row":
            row_obj[x["obj"]["n"]] = x["obj"]
    cands: dict[tuple, dict] = {}
    always = []
    for n, c in cls.items():
        meta = nl.get(n, {})
        if c["summary"] or not meta.get("kind"):
            always.append(n)
            continue
        key, name, role = owner_of(meta, head_of.get(n, {}), row_obj.get(n))
        facet = meta["kind"][0]
        k = (key, facet)
        if k not in cands:
            reach = md_reach(key, md)
            rel = ROLE_EN.get(role, ROLE_EN[None])
            if role in common.SUB_LAYERS or role is None:
                rel += {True: "; offered at the Myeongdong branch", False: "; not offered at the Myeongdong branch",
                        None: ""}[reach]
            cands[k] = {"key": key, "name": name, "facet": facet, "relation": rel, "rows": [], "role": role,
                        "md": reach}
        cands[k]["rows"].append(n)
    by = common.kind_by(r)
    unresolved = [KIND_EN[k] for k, v in by.items() if v in ("yes", "entry", "top") and k in KIND_EN]
    if not unresolved:
        unresolved = [KIND_EN[k] for k, v in by.items() if v == "default" and k in KIND_EN]
    unresolved.append("key safety information for the procedure the customer is considering")
    clist = list(cands.values())
    state = {
        "question": r.get("question") or "",
        "targets": [t.get("name") for t in r.get("targets") or []],
        "unresolved": unresolved,
        "candidates": [{"id": f"c{i}", "name": c["name"], "relation": c["relation"], "facet": KIND_EN.get(c["facet"], c["facet"])}
                       for i, c in enumerate(clist)],
    }
    return {"state": state, "cands": clist, "always": always, "cls": cls}


def chunks(state: dict) -> list[tuple[dict, list[int]]]:
    """후보가 많으면 나눈다 — 같은 question · targets · unresolved 에 후보 조각만 바꿔 여러 요청(동시)."""
    allc = state["candidates"]
    out = []
    for s in range(0, len(allc), CHUNK):
        idx = list(range(s, min(s + CHUNK, len(allc))))
        st = {**state, "candidates": [allc[i] for i in idx]}
        out.append((st, idx))
    return out


def questions_for(st: dict) -> dict:
    from typesafe_sdk import Noul  # noqa: PLC0415

    return {f"relevant_{j}": Noul(instructions=(
        f"Does `candidates[{j}]` help answer `question` by supplying one of the items in `unresolved`?"))
        for j in range(len(st["candidates"]))}


async def ask_all(jobs):
    sys.path.insert(0, str(common.A))
    from clinic_chat.clients.jev_client import make_client  # noqa: PLC0415
    from clinic_chat.config import load_settings  # noqa: PLC0415

    client = make_client(load_settings())
    if client is None:
        raise SystemExit("TYPESAFE_API_KEY 없음")
    from typesafe_sdk import RetryPolicy  # noqa: F401,PLC0415

    sem = asyncio.Semaphore(4)

    async def one(tag, st, idx):
        async with sem:
            t = time.perf_counter()
            try:
                res = await client.system_one(state=st, questions=questions_for(st))
                err = None
            except Exception as e:  # noqa: BLE001
                res, err = None, f"{type(e).__name__}: {str(e)[:200]}"
            ms = round((time.perf_counter() - t) * 1000, 1)
        out = {"tag": tag, "idx": idx, "ms": ms, "error": err, "n_q": len(idx),
               "state_bytes": len(json.dumps(st, ensure_ascii=False).encode())}
        if res is not None:
            out["model"] = getattr(res, "model", None)
            out["nouls"] = {k: float(v.noul) for k, v in (res.nouls or {}).items()}
            u = getattr(res, "usage", None)
            out["usage"] = (u.model_dump() if hasattr(u, "model_dump") else dict(u)) if u is not None else None
        return out

    # 턴 하나의 조각은 동시에(fan-out) · 턴 사이도 동시 4
    res = await asyncio.gather(*(one(tag, st, idx) for tag, st, idx in jobs))
    close = getattr(client, "close", None) or getattr(client, "aclose", None)
    if close:
        r = close()
        if asyncio.iscoroutine(r):
            await r
    return res


def score(turn, nouls_by_idx, k):
    """임계값 · 규칙별 → {tok, pct, miss, cited}."""
    cls, cands, always = turn["cls"], turn["cands"], turn["always"]
    cited = {n for n, c in cls.items() if c["used"]}
    now_b = sum(c["bytes"] for c in cls.values())
    tcodes = {t.get("code") for t in turn["row"].get("targets") or []}
    q = turn["row"].get("question") or ""

    def explicit(c):
        code = c["key"].partition(":")[2]
        nm = re.sub(r"\(.*\)$", "", c["name"])
        return code in tcodes or (len(nm) >= 2 and nm in q)

    def measure(keep_rows: set[int], minus_dup=False):
        kept = keep_rows | set(always)
        b = sum(cls[n]["bytes"] - (cls[n]["dup"] if minus_dup else 0) for n in kept)
        miss = cited - kept
        return {"tok": round(b * k), "pct": round(100 * b / now_b, 1) if now_b else None, "miss": len(miss),
                "cited": len(cited), "rows": len(kept)}

    out = {"now": measure(set(cls))}
    for th in THRESH:
        sel = {i for i, c in enumerate(cands) if nouls_by_idx.get(i, 0.0) >= th}
        rows = {n for i in sel for n in cands[i]["rows"]}
        out[f"jev_{th}"] = measure(rows)
        owners = {cands[i]["key"] for i in sel} | {c["key"] for c in cands if explicit(c)}
        forced = sel | {i for i, c in enumerate(cands) if explicit(c)} | {
            i for i, c in enumerate(cands) if c["facet"] in common.SAFETY_KINDS and c["key"] in owners}
        out[f"jev_{th}_forced"] = measure({n for i in forced for n in cands[i]["rows"]})
    not_md = {n for c in cands if c["md"] is False and c["role"] not in ("자기", "물려받음") for n in c["rows"]}
    det = {n for n, c in cls.items() if c["by"] != "kd9" and c["md_reach"] is not False and n not in not_md}
    out["det"] = measure(det, minus_dup=True)
    for th in (0.5,):
        sel = {i for i, c in enumerate(cands) if nouls_by_idx.get(i, 0.0) >= th}
        rows = {n for i in sel for n in cands[i]["rows"]}
        owners = {cands[i]["key"] for i in sel} | {c["key"] for c in cands if explicit(c)}
        forced = sel | {i for i, c in enumerate(cands) if explicit(c)} | {
            i for i, c in enumerate(cands) if c["facet"] in common.SAFETY_KINDS and c["key"] in owners}
        rows = {n for i in forced for n in cands[i]["rows"]}
        out["det+jev_0.5_forced"] = measure(rows & det | {n for n in rows if cls[n]["explicit"] or cls[n]["safety"]},
                                            minus_dup=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()
    md = common.md_sets()
    k = json.loads((HERE / "out/decompose.json").read_text())["k_tok_per_byte"]
    turns = []
    for pre, which, why in PICK:
        for r in rows_of(which):
            if r["conv_id"].startswith(pre) and (which == "replay" or not r["conv_id"].startswith("fixE")):
                t = build(r, md)
                t.update({"row": r, "tag": f'{pre}:{r["turn"]}', "why": why})
                turns.append(t)
    print("turns", len(turns), "with material", sum(1 for t in turns if t["cands"]),
          "candidates", sum(len(t["cands"]) for t in turns), "max", max(len(t["cands"]) for t in turns))
    raw_p = HERE / "out/jev_raw.jsonl"
    if a.dry:
        for t in turns:
            print(t["tag"], len(t["cands"]), len(t["cls"]), len(json.dumps(t["state"], ensure_ascii=False).encode()))
        print(json.dumps(turns[0]["state"], ensure_ascii=False)[:1500])
        return
    if not a.offline:
        jobs = []
        for t in turns:
            if t["cands"]:
                for st, idx in chunks(t["state"]):
                    jobs.append((t["tag"], st, idx))
        t0 = time.perf_counter()
        res = asyncio.run(ask_all(jobs))
        wall = round((time.perf_counter() - t0) * 1000)
        with raw_p.open("w") as f:
            for x in res:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
        print("requests", len(res), "errors", sum(1 for x in res if x["error"]), "wall_ms", wall)
    raw = [json.loads(x) for x in raw_p.read_text().splitlines()]
    by_tag = defaultdict(dict)
    meta = defaultdict(lambda: {"ms": [], "req": 0, "models": set(), "err": 0})
    for x in raw:
        for j, i in enumerate(x["idx"]):
            if x.get("nouls"):
                by_tag[x["tag"]][i] = x["nouls"].get(f"relevant_{j}", 0.0)
        m = meta[x["tag"]]
        m["ms"].append(x["ms"])
        m["req"] += 1
        m["err"] += bool(x["error"])
        if x.get("model"):
            m["models"].add(x["model"])
    out = []
    for t in turns:
        s = score(t, by_tag.get(t["tag"], {}), k)
        m = meta.get(t["tag"], {"ms": [], "req": 0, "models": set(), "err": 0})
        nv = list(by_tag.get(t["tag"], {}).values())
        out.append({"tag": t["tag"], "why": t["why"], "question": t["row"].get("question"), "cands": len(t["cands"]),
                    "rows": len(t["cls"]), "score": s, "req": m["req"], "err": m["err"],
                    "ms_max": max(m["ms"]) if m["ms"] else 0, "ms_sum": sum(m["ms"]), "models": sorted(m["models"]),
                    "noul_dist": {"n": len(nv), "lt0.3": sum(v < 0.3 for v in nv), "0.3-0.7": sum(0.3 <= v < 0.7 for v in nv),
                                  "ge0.7": sum(v >= 0.7 for v in nv),
                                  "median": round(statistics.median(nv), 3) if nv else None},
                    "cand_sample": [{**{kk: c[kk] for kk in ("name", "facet", "relation")},
                                     "noul": round(by_tag.get(t["tag"], {}).get(i, -1), 3),
                                     "cited": any(t["cls"][n]["used"] for n in c["rows"])}
                                    for i, c in enumerate(t["cands"])][:400]})
    (HERE / "out/jev_measure.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("saved", len(out))


if __name__ == "__main__":
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    main()
