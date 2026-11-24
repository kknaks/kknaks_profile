"""토큰 원인 조사 공용(읽기만) — 장부 · 매핑 · 메시지 절 자르기 · 자료 줄 분류.

앱 코드 · 데이터는 읽기만 한다. 경로는 환경 변수 `A`(앱 워크트리) 로 바꿀 수 있다.
"""

from __future__ import annotations

import json
import os
import re
from collections import defaultdict
from pathlib import Path

A = Path(os.environ.get("A", "/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo"))
W = Path(__file__).resolve().parent
OUT = Path(os.environ.get("OUT_DIR", str(W / "out")))
LEDGER = Path(os.environ.get("LEDGER", str(A / "runs/consult/turns.jsonl")))
MAPPING = A / "data/kos/myeongdong-mapping-20261120-v3.json"  # sha256 d21903f5 (앱 KOS_MAPPING_PATH 와 같은 파일)

HEADS = [  # (절 이름, 머리 줄 앞부분) — prompts/consult.json turn_headers · kos.block_header
    ("judgement", "## 앱 판정"),
    ("close", "### 끝맺음"),
    ("prev", "### 앞 턴"),
    ("consult", "## 상담 상태"),
    ("material", "## 자료"),
    ("kos", "# 명동점 블록"),
    ("question", "## 질문"),
]
SAFETY_KINDS = {"adverse", "contraindication", "recovery", "caution", "avoid"}
SUB_LAYERS = {"하위 시술", "하위 케이스", "하위 제품"}
BY_RANK = {"yes": 0, "entry": 1, "default": 2, "kd11": 3, "kd9": 4}


def load_rows() -> list[dict]:
    return [json.loads(x) for x in LEDGER.read_text().splitlines() if x.strip()]


def answer_rows() -> list[dict]:
    return [r for r in load_rows() if r.get("phase") == "end" and "llm_user_message" in r]


def b(s: str) -> int:
    return len(s.encode("utf-8"))


def split_sections(msg: str) -> dict[str, str]:
    """턴 메시지 → 절 이름: 글. 머리 줄(줄 맨 앞)로 자른다."""
    pos = []
    for name, head in HEADS:
        for m in re.finditer(r"(?m)^" + re.escape(head), msg):
            pos.append((m.start(), name))
    pos.sort()
    out: dict[str, str] = defaultdict(str)
    if pos and pos[0][0] > 0:
        out["other"] += msg[: pos[0][0]]
    for i, (p, name) in enumerate(pos):
        end = pos[i + 1][0] if i + 1 < len(pos) else len(msg)
        out[name] += msg[p:end]
    return dict(out)


def md_sets() -> dict[str, set[str]]:
    d = json.loads(MAPPING.read_text())
    cases, procs, prods = set(), set(), set()
    for it in d["items"]:
        h = it.get("hub") or {}
        cases.update(h.get("case_codes") or [])
        procs.update(h.get("procedure_codes") or [])
        prods.update(p.get("code") for p in h.get("products") or [] if p.get("code"))
    return {"procedure_case": cases, "procedure": procs, "product": prods}


def kind_by(r: dict) -> dict[str, str]:
    f = (r.get("trace") or {}).get("front") or {}
    return {k["code"]: k.get("by") or "" for k in f.get("kinds") or []}


def row_by(kinds: list[str] | None, by: dict[str, str]) -> str:
    if not kinds:
        return ""
    bs = [by.get(k, "?") for k in kinds]
    return min(bs, key=lambda x: BY_RANK.get(x, 9))


def material_lines(sec: str) -> list[dict]:
    """「## 자료」 절 → [{kind: head|row, obj, bytes}] — 한 줄 JSON 만(머리 · 빈 줄 · (없음) 은 head_text)."""
    out = []
    for ln in sec.split("\n")[1:]:
        if not ln.strip():
            continue
        try:
            o = json.loads(ln)
        except ValueError:
            out.append({"t": "text", "obj": None, "bytes": b(ln) + 1})
            continue
        t = "head" if isinstance(o, dict) and "group" in o else ("row" if isinstance(o, dict) and "n" in o else "text")
        out.append({"t": t, "obj": o, "bytes": b(ln) + 1})
    return out


def dup_bytes(o: dict, same: dict | None = None) -> int:
    """한 줄 안에서 같은 값이 두 번 이상 나오는 칸(뒤 것)의 바이트 — 「같은 이름 반복」 셈. 묶음 머리 `same` 값과 같은 칸도 센다."""
    seen = {str(v) for v in (same or {}).values() if isinstance(v, str) and len(v) >= 2}
    n = 0

    def walk(x):
        nonlocal n
        if isinstance(x, dict):
            for k, v in x.items():
                if isinstance(v, str) and len(v) >= 2:
                    if v in seen:
                        n += b(json.dumps({k: v}, ensure_ascii=False)) - 1  # `"k": "v", ` 근사
                    else:
                        seen.add(v)
                elif isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk({k: v for k, v in o.items() if k != "n"})
    return n


def cited_rows(r: dict) -> set[int]:
    """답이 근거로 단 줄 번호 — 장부 `answer_lines` ∪ 답 원문 `<<<근거>>>` 꼬리(`N: a,b,c`)."""
    used = {int(n) for a in r.get("answer_lines") or [] for n in a.get("rows") or []}
    raw = r.get("answer_raw") or ""
    i = raw.find("<<<근거>>>")
    if i >= 0:
        for ln in raw[i:].split("\n")[1:]:
            k, _, v = ln.partition(":")
            if k.strip().isdigit():
                used |= {int(x) for x in re.findall(r"\d+", v)}
    return used


def classify_material(r: dict, md: dict[str, set[str]]) -> list[dict]:
    """이번 턴 「## 자료」 의 줄마다 {n, bytes(머리 몫 나눔 포함), kind, layer, by, summary, used, safety, explicit, md_reach, dup}."""
    sec = split_sections(r["llm_user_message"]).get("material", "")
    lines = material_lines(sec)
    nl = {x["n"]: x for x in (r.get("material") or {}).get("new_lines") or []}
    by = kind_by(r)
    used = cited_rows(r)
    tcodes = {t.get("code") for t in r.get("targets") or []}
    heads: dict[int, tuple[int, dict]] = {}
    for x in lines:
        if x["t"] == "head":
            o = x["obj"]
            ns = o.get("lines") or []
            for n in ns:
                heads[n] = (x["bytes"] // max(1, len(ns)), o)
    out = []
    for x in lines:
        if x["t"] != "row":
            continue
        o = x["obj"]
        n = o["n"]
        hb, ho = heads.get(n, (0, {}))
        meta = nl.get(n, {})
        lay = meta.get("layer")
        role = (lay or {}).get("role") if isinstance(lay, dict) else None
        holder = ((lay or {}).get("holder") or {}) if isinstance(lay, dict) else {}
        summary = bool(o.get("summary") or meta.get("summary"))
        kinds = meta.get("kind") or []
        ht, hc = holder.get("holder_table"), holder.get("holder_code")
        reach = None
        if role in SUB_LAYERS and ht in md:
            reach = hc in md[ht]
        out.append({
            "n": n, "bytes": x["bytes"] + hb, "row_bytes": x["bytes"], "head_bytes": hb,
            "kind": "+".join(kinds) if kinds else ("summary:" + (meta.get("rule") or "AP4") if summary else "?"),
            "kinds": kinds, "gold_table": meta.get("gold_table"),
            "layer": role or ("요약 줄" if summary else "층 표시 없음"),
            "by": row_by(kinds, by) if kinds else ("summary" if summary else "?"),
            "summary": summary, "used": n in used,
            "safety": bool(set(kinds) & SAFETY_KINDS),
            "explicit": bool(hc and hc in tcodes) or bool(meta.get("silver_id") in tcodes),
            "md_reach": reach, "holder": f"{ht}:{hc}" if ht else None,
            "dup": dup_bytes(o, ho.get("same")),
        })
    return out


def turn_tokens(r: dict) -> int:
    t = r.get("tokens") or {}
    return int(t.get("input_tokens") or 0) + int(t.get("cache_creation_input_tokens") or 0) + int(
        t.get("cache_read_input_tokens") or 0)


def date_of(r: dict) -> str:
    return (r.get("asked_at") or "")[:10]


def era(r: dict) -> str:
    kb = ((r.get("trace") or {}).get("front") or {}).get("kinds_by")
    d = date_of(r)
    if d < "2026-11-18":
        return f"before-11-18({kb})"
    return str(kb)
