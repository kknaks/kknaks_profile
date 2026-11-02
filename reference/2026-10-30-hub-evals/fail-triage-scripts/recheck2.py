#!/usr/bin/env python3
"""recheck2 — SPEC-005 v3.2 §6-5 재인용 대조(WORK-007 WP-0 · WP-6).

판정 식은 `triage.py` · `recheck.py` 와 같은 식을 **여기에 다시 적는다**(import 안 함 · F-6):
정규화 = 소문자 · 공백 · 기호 제거 · 양방향 포함(골드 쪽 8자 이상) · 3-gram 80% = 부분 일치 · fact id 일치 · **엣지 id 일치**(§6-5 v3.2).

입력 = `build-out/fail-triage2.json`(b_rows 186 · c_rows 18 · rows 320) + `runs/runs.jsonl` batch b202610311552-d39a4d(182문항)
     + `build-out/recheck/replay2.json`(rerun-v3 실제 호출 676 · 같은 입력 · intent · sections 그대로) + gold-export(옛 d3a1abd5 · 새 v3.2)
     + `build-out/recheck2/b186-clauses.json`(SPEC §8 조항 열 · make-clauses 로 뽑음 · 161 조항 행 + 닫지 않는 행 25)

모드
  make-clauses                          SPEC-005 §8 표 → b186-clauses.json(문항 · 케이스 · 항목 · 조항 · 메모)
  baseline   --export-old PATH          옛 export + replay2 기록 응답 → 320행 재분류 동일성 · B 186 닫힘 · 크기 → recheck2-report.baseline.{md,json}
  rerun      --export-new PATH (--base-url URL | --inprocess)
                                        676 호출을 같은 입력으로 다시 보내 B 186 닫힘(조항 닿는 161 기준) · C3 5 원문 칸 · Q003 반대 조건 · 크기 → recheck2-report.{md,json}
시간 칸은 .json 머리 `meta.ran_at` 하나뿐(결정론 비교는 그 칸을 뺀다).
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

E = Path(os.environ.get("HUB_EVALS_DIR", "/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-30-hub-evals"))
RAW = Path(os.environ.get("PHUB_RAW_DIR", "/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26"))
BACKEND = Path(os.environ.get("PHUB_BACKEND_DIR", "/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend"))
SPEC = Path(os.environ.get("PHUB_SPEC_PATH", "/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-005.md"))
OUT = E / "build-out" / "recheck2"
BATCH = "b202610311552-d39a4d"
CARD_TOOLS = ("recommend", "procedure_card", "pair_check", "check_conditions", "compare", "combos", "neighbors")  # T2~T8
ALL_TOOLS = ("recommend", "procedure_card", "pair_check", "check_conditions", "compare", "combos", "neighbors", "resolve", "vocab")
ITEM = {"accuracy": "정확성", "safety": "안전", "candidates": "후보", "uncertainty": "불확실", "on_topic": "질문에 답함"}
ITEM_INV = {v: k for k, v in ITEM.items()}
# §5-0-1 A1-9 표(기본 응답 중앙 · p95 · 바이트) — 끝 조건 (ii). procedure_card 는 단위 · 제품 / 계열 따로
SIZE_CAPS: dict[str, tuple[int, int]] = {
    "recommend": (12000, 24000), "procedure_card:unit": (6000, 12000), "procedure_card:family": (10000, 20000), "pair_check": (10000, 20000),
    "check_conditions": (12000, 24000), "compare": (12000, 24000), "combos": (12000, 24000), "neighbors": (6000, 12000),
    "resolve": (2000, 4000), "vocab": (8000, 16000), "peek": (2500, 8000), "expand": (8000, 16000), "case3_path": (20000, 60000),  # peek 2,500/8,000 = 코디 11-01 D
}
# (iii) C3 — fact 없는 행 5(Q014 c2 · Q054 c3 · Q190 c3 · Q221 c3 + Q069 c2) · Q203 c2 는 vocab 만이라 밖 · Q003 ×2 는 반대 조건
C3_ROWS = [("Q014", "case2"), ("Q054", "case3"), ("Q069", "case2"), ("Q190", "case3"), ("Q221", "case3")]
C3_OUT = [("Q203", "case2", "vocab 만 호출 — 밖")]
Q003_SC = "SC-jawline-M1"
Q003_BOTOX_JAW_UNIT = "unit_procedure:U5-016"  # 보톡스 턱선 단위 시술(실물 M1 · key.site 턱선) — 추천 응답에 M1 카드가 없을 때 반대 조건 둘째 절 확인용
NOT_CLOSABLE_CLAUSES = ("X0", "N-다른계열", "N-제품수준", "N-9단계", "N-조항없음", "N-데이터")
# 코디 11-01 결정 4) — 데이터상 불가 행(허브 규칙으로 못 닫음)을 닫지 않는 행으로: (문항, 케이스, 항목) → 사유
NOT_CLOSABLE_DATA = {
    ("Q007", "case2", "safety"): "N-데이터 — concern:J10 추천 카드 0(treats 가 단위 시술로 안 닿음) · 응답에 시술 노드 없음",
    ("Q007", "case3", "safety"): "N-데이터 — concern:J10 추천 카드 0 · 응답에 시술 노드 없음",
    ("Q018", "case3", "safety"): "N-데이터 — K8-0253(C-KEL)은 family:M2 대상 주장 · 입력은 M1(product:M1-2-1 · U5-001)",
    ("Q192", "case3", "accuracy"): "N-데이터 — K8-0110(C-BMI)은 family:M14 대상 주장 · 카드는 family:M9",
    ("Q126", "case2", "accuracy"): "N-데이터 — K8-0230(C-DERM)은 family:M15 대상 주장 · 입력 U5-030 은 M8",
    ("Q169", "case3", "accuracy"): "N-데이터 — product_family basis 는 C4′ 제품 행인데 I-09(check_conditions) 동봉에 C4 없음(§5-13 표)",
}


# ── 판정 식(triage.py · recheck.py 와 같은 식) ───────────────────────────────
def norm(s: Any) -> str:
    return re.sub(r"[\s\W_]+", "", str(s).lower())


def grams(s: str, n: int = 3) -> set[str]:
    return {s[i:i + n] for i in range(len(s) - n + 1)}


def flat(o: Any, p: str = ""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from flat(v, f"{p}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from flat(v, f"{p}[{i}]")
    elif isinstance(o, str) and len(o) >= 2:
        yield p, o


class Gold:
    """gold-export 한 벌 — 문자열 색인(fact · 노드 이름 · 노드 silver 속성 · 엣지 속성 · globals) · 인접 · owner 해소."""

    def __init__(self, path: Path) -> None:
        self.path = path
        g = json.loads(path.read_text(encoding="utf-8"))
        self.hash = g["build"]["build_hash"]
        self.nodes = {n["id"]: n for n in g["nodes"]}
        self.facts = {f["id"]: f for f in g["facts"]}
        self.edges_by_id = {e["id"]: e for e in g["edges"]}
        self.kinds = sorted({n["kind"] for n in g["nodes"]})
        self.entries: list[tuple[str, str, dict[str, Any]]] = []
        for f in g["facts"]:
            self.entries.append((norm(f["text"]), "fact", {"fact_id": f["id"], "owner_id": f["owner_id"], "section": f["section"], "text": f["text"],
                                                         "attached_to": f.get("attached_to") or []}))
        for n in g["nodes"]:
            self.entries.append((norm(n["name"]), "node_name", {"node_id": n["id"], "text": n["name"]}))
            for p, s in flat(n["attrs"].get("silver") or {}, "silver"):
                self.entries.append((norm(s), "node_attr", {"node_id": n["id"], "path": p, "text": s}))
        for e in g["edges"]:
            for p, s in flat(e.get("attrs") or {}, "attrs"):
                self.entries.append((norm(s), "edge_attr", {"edge_id": e["id"], "kind": e["kind"], "from": e["from_id"], "to": e["to_id"], "path": p, "text": s}))
        for x in g["globals"]:
            for p, s in flat(x.get("payload") or {}, "payload"):
                self.entries.append((norm(s), "global", {"global_id": x["id"], "path": p, "text": s}))
        self.entries = [e for e in self.entries if len(e[0]) >= 2]
        self.inv: dict[str, set[int]] = collections.defaultdict(set)
        for i, (ns, _, _) in enumerate(self.entries):
            if len(ns) >= 8:
                for gr in grams(ns):
                    self.inv[gr].add(i)
        self.adj: dict[str, set[str]] = collections.defaultdict(set)
        for e in g["edges"]:
            self.adj[e["from_id"]].add(e["to_id"])
            self.adj[e["to_id"]].add(e["from_id"])

    def gold_match(self, q: str) -> tuple[str | None, list[tuple[str, str, dict[str, Any]]]]:
        """tier exact: 포함(양방향 · 짧은 인용은 골드 쪽이 2배+4 안) · weak: 짧은 인용이 긴 문장 안에서만 · partial: 3-gram ≥ 0.8."""
        hits, weak = [], 0
        for i, (ns, kind, ref) in enumerate(self.entries):
            if q in ns:
                if len(q) >= 8 or len(ns) <= 2 * len(q) + 4:
                    hits.append(i)
                else:
                    weak += 1
            elif len(ns) >= 8 and ns in q:
                hits.append(i)
        if hits:
            return "exact", [self.entries[i] for i in hits[:40]]
        if weak:
            return "weak", []
        if len(q) >= 12:
            cnt: collections.Counter = collections.Counter()
            gq = grams(q)
            for gr in gq:
                for i in self.inv.get(gr, ()):
                    cnt[i] += 1
            part = sorted(((c / len(gq), i) for i, c in cnt.items() if c / len(gq) >= 0.8), reverse=True)
            if part:
                return "partial", [self.entries[i] for _, i in part[:20]]
        return None, []

    def fam_of(self, nid: str) -> str | None:
        n = self.nodes.get(nid)
        if not n:
            return None
        if n["kind"] == "family":
            return nid
        return (n["attrs"].get("gold") or {}).get("family") or None

    def owner_nodes(self, ref: dict[str, Any]) -> tuple[str, list[str]]:
        oid = ref["owner_id"]
        if oid in self.nodes:
            return "node", [oid]
        f = self.facts[ref["fact_id"]]
        meta = f["source"].get("meta") or {}
        if oid.startswith("scope:"):
            return "scope", [t for t in (meta.get("target_keys") or []) if t in self.nodes]
        if oid.startswith("procedure_relation:"):
            e = self.edges_by_id.get(oid)
            a = (e or {}).get("attrs", {})
            return "pair", ([x for x in (a.get("a"), a.get("b")) if x in self.nodes] if e else [])
        return "combo", []

    def owners_of(self, k: str, ref: dict[str, Any]) -> list[str]:
        if k == "fact":
            return self.owner_nodes(ref)[1]
        if k in ("node_attr", "node_name"):
            return [ref["node_id"]]
        if k == "edge_attr":
            return [x for x in (ref["from"], ref["to"]) if x in self.nodes]
        return []


class Raw:
    def __init__(self, d: Path) -> None:
        self.files = {fn[:-5]: json.loads((d / fn).read_text(encoding="utf-8")) for fn in sorted(os.listdir(d)) if fn.endswith(".json")}

    def quote_at(self, path: str, quote: str) -> bool:
        file = path.split(".")[0]
        if file not in self.files:
            return False
        cur: Any = self.files[file]
        for key, idx in re.findall(r"\.?([^.\[\]]+)|\[(\d+)\]", path[len(file) + 1:]):
            if idx != "":
                if not isinstance(cur, list) or int(idx) >= len(cur):
                    return False
                cur = cur[int(idx)]
            else:
                if not isinstance(cur, dict) or key not in cur:
                    return False
                cur = cur[key]
        return norm(quote) in norm(json.dumps(cur, ensure_ascii=False))


# ── 호출 ─────────────────────────────────────────────────────────────────────
def call_key(tool: str, args: Any) -> str:
    return hashlib.md5(json.dumps([tool, args], sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def rest_call(base: str, tool: str, args: dict[str, Any] | None, client: Any = None) -> tuple[int, str]:
    """REST 호출 — hub_rest.call 과 같은 도구 → 경로. 입력은 기록 그대로(intent · sections 포함 · 더하지 않음)."""
    a = dict(args or {})
    get_tools = {"procedure_card": lambda: ("GET", f"/procedures/{a.pop('id')}"), "check_conditions": lambda: ("GET", f"/procedures/{a.pop('id')}/checks"),
                 "neighbors": lambda: ("GET", f"/nodes/{a.pop('id')}/neighbors"), "combos": lambda: ("GET", "/combos"),
                 "resolve": lambda: ("GET", "/resolve"), "vocab": lambda: ("GET", "/vocab"),
                 "peek": lambda: ("GET", f"/nodes/{a.pop('id')}/peek")}
    post_tools = {"recommend": "/recommend", "pair_check": "/pairs", "compare": "/compare"}
    try:
        if tool == "expand":
            method, path, params, body = "POST", f"/nodes/{a.pop('id')}/expand", None, a
        elif tool in post_tools:
            method, path, params, body = "POST", post_tools[tool], None, a
        elif tool in get_tools:
            if "id" not in a and tool in ("procedure_card", "check_conditions", "neighbors", "peek"):
                return -2, "no id"
            method, path = get_tools[tool]()
            params = {k: (",".join(v) if isinstance(v, list) else v) for k, v in a.items() if v is not None}
            body = None
        else:
            return -3, f"unknown tool {tool}"
    except KeyError:
        return -2, "no id"
    if client is not None:  # in-process(TestClient)
        r = client.request(method, f"{base}/procedure-hub/gold{path}", params=params, json=body)
        return r.status_code, r.text
    url = base.rstrip("/") + "/procedure-hub/gold" + urllib.parse.quote(path, safe="/:") + (("?" + urllib.parse.urlencode({k: str(v) for k, v in params.items()})) if params else "")  # 경로의 한글 id(조합 RC-OP-Acne-경미 등) 인코딩 — TestClient 와 같은 요청
    data = json.dumps(body).encode() if body is not None else None
    rq = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"} if data else {})
    try:
        with urllib.request.urlopen(rq, timeout=120) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as ex:
        return ex.code, ex.read().decode()
    except Exception as ex:  # noqa: BLE001
        return -1, str(ex)


def load_runs(path: Path, batch: str = BATCH) -> dict[str, dict[str, Any]]:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            d = json.loads(line)
            if d.get("batch_id") == batch:
                out[d["run_id"]] = d
    return out


def inprocess_client() -> Any:
    """같은 앱(TestClient · 발행본 DB 적재). env RECHECK2_FRESH_BUILD=1 이면 발행 전 코드 · 입력으로 메모리 빌드를 끼운다(발행 · 18005 손대지 않음)."""
    sys.path.insert(0, str(BACKEND))
    sys.path.insert(0, str(BACKEND / "scripts"))
    from _gold_client import GoldClient  # type: ignore  # noqa: PLC0415
    c = GoldClient.inprocess().http
    if os.environ.get("RECHECK2_FRESH_BUILD"):
        from app.graph_main import container  # type: ignore  # noqa: PLC0415
        from app.modules.gold import tools as T  # type: ignore  # noqa: PLC0415
        from app.modules.gold.build import build_gold  # type: ignore  # noqa: PLC0415
        from app.modules.gold.inputs import read_dir  # type: ignore  # noqa: PLC0415
        from app.modules.gold.memory import GoldGraph  # type: ignore  # noqa: PLC0415
        inp = Path(os.environ.get("GOLD_INPUT_DIR", "/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend"))
        b = build_gold(read_dir(inp))
        g = GoldGraph.from_content(b.content, build={"id": "fresh-" + b.build_hash, "build_hash": b.build_hash, "published_at": "fresh"})
        T.warm_sections(g)
        container.gold_state().graph = g
    return c


# ── 분류(triage.py 와 같은 규칙) ───────────────────────────────────────────────
def node_ids_in(gold: Gold, obj: Any) -> set[str]:
    out = set()
    pat = re.compile(r"^(?:" + "|".join(gold.kinds) + r"):")
    for _, s in flat(obj):
        if pat.match(s) and s in gold.nodes:
            out.add(s)

    def keys(o: Any) -> None:
        if isinstance(o, dict):
            for k, v in o.items():
                if k in gold.nodes:
                    out.add(k)
                keys(v)
        elif isinstance(o, list):
            for v in o:
                keys(v)
    keys(obj)
    return out


def fact_ids_in(obj: Any) -> set[str]:
    return {f["id"] for f in (obj.get("facts") or []) if isinstance(f, dict) and f.get("id")} if isinstance(obj, dict) else set()


def more_cards_in(obj: Any) -> set[str]:
    s: set[str] = set()

    def rec(o: Any) -> None:
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "more_cards" and isinstance(v, list):
                    s.update(x for x in v if isinstance(x, str))
                rec(v)
        elif isinstance(o, list):
            for v in o:
                rec(v)
    rec(obj)
    return s


def text_fields_in(obj: Any) -> list[str]:
    """(iii) 원문 칸 = `text` 값 중 같은 객체에 `id` 가 있는 것(facts[] · claims[] 행) — 노드 이름 · 속성 문자열 · 본문 아무 데나는 아님."""
    out: list[str] = []

    def rec(o: Any) -> None:
        if isinstance(o, dict):
            if isinstance(o.get("text"), str) and "id" in o:
                out.append(o["text"])
            for k, v in o.items():
                if k == "names" and isinstance(v, dict):  # 응답 머리 names(금기 · 조건 · 합병증 짧은 이름 전부 · 코디 11-01 D)
                    out.extend(x for x in v.values() if isinstance(x, str))
                elif k == "emergency_signs" and isinstance(v, dict):
                    out.extend(x for xs in v.values() for x in (xs if isinstance(xs, list) else []) if isinstance(x, str))
                else:
                    rec(v)
        elif isinstance(o, list):
            for v in o:
                rec(v)
    rec(obj)
    return out


class HubContext:
    """한 문항 · 한 케이스의 허브 응답 묶음 — 분류와 닫힘 판정의 재료."""

    def __init__(self, gold: Gold, calls: list[dict[str, Any]], jev: dict[str, Any] | None, hub_trace: dict[str, Any]) -> None:
        self.tools_called = [c["tool"] for c in calls]
        self.calls = calls
        self.hub_text = ""
        self.returned: set[str] = set()
        self.hub_facts: set[str] = set()
        self.more_cards: set[str] = set()
        self.req_sections: dict[str, set[str]] = collections.defaultdict(set)
        self.resolve_cands: set[str] = set()
        self.pair_procs: set[str] = set()
        self.all_req_sections: set[str] = set()
        self.errors: list[dict[str, Any]] = []
        self.objs: list[dict[str, Any]] = []
        self.text_norm = ""
        self.jev, self.hub_trace = jev, hub_trace
        for c in calls:
            inp = c.get("input") or {}
            if c["tool"] in ("pair_check", "compare"):
                self.pair_procs |= set(inp.get("procedures") or [])
            self.all_req_sections |= set(inp.get("sections") or [])
            if c["status"] != 200:
                self.errors.append({"tool": c["tool"], "input": inp, "status": c["status"], "text": c["text"][:200]})
                continue
            try:
                o = json.loads(c["text"])
            except ValueError:
                continue
            self.hub_text += c["text"]
            self.objs.append({"tool": c["tool"], "input": inp, "obj": o, "text": c["text"]})
            self.text_norm += norm("\n".join(text_fields_in(o)))
            ids = node_ids_in(gold, o)
            self.returned |= ids
            self.hub_facts |= fact_ids_in(o)
            self.more_cards |= more_cards_in(o)
            if c["tool"] == "resolve":
                for m in o.get("matches") or []:
                    for cd in m.get("candidates") or []:
                        self.resolve_cands.add(cd["id"])
            else:
                for i in ids:
                    self.req_sections[i] |= set(inp.get("sections") or [])
        if hub_trace.get("resolve"):
            self.resolve_cands |= set((hub_trace.get("resolve") or {}).get("candidates") or [])
        self.hub_norm = norm(self.hub_text)
        self.reach_direct = set(self.returned) | {gold.fam_of(i) for i in self.returned if gold.fam_of(i)}
        self.reach_1hop = set(self.reach_direct)
        for i in self.returned:
            self.reach_1hop |= gold.adj.get(i, set())


def short_edge(eid: str) -> str:
    """엣지 id 의 응답 표기 — procedure_relation:E8-0169 → E8-0169 · requires_check:K8-…:C-… 는 그대로(응답 edges[] 도 같은 꼴)."""
    return eid.split(":", 1)[1] if eid.startswith("procedure_relation:") else eid


def in_hub(q: str, hits: list[tuple[str, str, dict[str, Any]]], ctx: HubContext, broad: bool = False) -> tuple[bool, str | None]:
    """triage 와 같은 식(인용 포함 · facts[].id · 골드 문장 포함). broad(§6-5 닫힘 판정)는 응답 JSON 어디든 fact id · 엣지 id(따옴표 안)도 센다."""
    hit_fact_ids = {ref["fact_id"] for _, k, ref in hits if k == "fact"}
    if len(q) >= 6 and q in ctx.hub_norm:
        return True, "인용 포함"
    both = hit_fact_ids & ctx.hub_facts
    if both:
        return True, "facts[].id " + sorted(both)[0]
    for ns, k, ref in hits:
        if len(ns) >= 8 and ns in ctx.hub_norm:
            return True, "골드 문장 포함"
    if broad:
        for fid in sorted(hit_fact_ids):
            if f'"{fid}"' in ctx.hub_text:
                return True, "fact id 만(동봉 · more_ids · claims id) " + fid
        for eid in sorted({ref["edge_id"] for _, k, ref in hits if k == "edge_attr"}):
            if f'"{eid}"' in ctx.hub_text or f'"{short_edge(eid)}"' in ctx.hub_text:
                return True, "엣지 id " + eid
    return False, None


PRIO = ["slim 카드 밖 섹션", "섹션 요청했는데도", "recommend 상한", "scope(claim) fact · 대상 slim", "scope(claim) fact · 대상 섹션", "쌍 관계 fact — 쌍 맞음",
        "이웃 노드", "scope(claim) fact · 대상 이웃", "조합(CC · 레시피) fact — combos 불렀", "노드 속성(full", "엣지 속성 — 양끝", "노드 이름만 일치(노드 도달)",
        "쌍 관계 fact — 쌍 도구 불렀으나", "쌍 관계 fact — pair", "조합(CC · 레시피) fact — combos 안", "경로가 그 노드", "scope(claim) fact · 대상 경로",
        "노드 속성 · ", "엣지 속성 · ", "노드 이름만 일치 · ", "scope(claim) fact · 대상 노드 없음", "전역"]


def _rank(t: str) -> int:
    t2 = re.sub(r"^노드 속성\((\w+) · full 카드 전용\)", "노드 속성(full", t)
    t2 = re.sub(r"^노드 속성\((\w+)\) · ", "노드 속성 · ", t2)
    return next((i for i, p in enumerate(PRIO) if t2.startswith(p)), 99)


def classify(gold: Gold, raw: Raw, row: dict[str, Any], ctx: HubContext, case: str) -> dict[str, Any]:
    """fail-triage 행 하나 → cls · sub(+ 판정 재료). triage.py 와 같은 규칙."""
    ev = row["evidence"]
    quote = ev["quote"]
    q = norm(quote)
    out: dict[str, Any] = {"cls": None, "sub": None, "gold_match_tier": None, "gold_hits": [], "gold_owner_nodes": [], "reach": None}
    if not raw.quote_at(ev["path"], quote):
        out.update(cls="D", sub="evidence 가 원장 경로와 안 맞음")
        return out
    if len(q) < 4:
        out.update(cls="미분류", sub=f"인용이 너무 짧음({quote!r}) — 문자열 대조 불가")
        return out
    tier, hits = gold.gold_match(q)
    out["gold_match_tier"] = tier
    out["gold_hits"] = [{"kind": k, **{kk: vv for kk, vv in ref.items() if kk != "text"}, "text": ref["text"][:120]} for _, k, ref in hits[:8]]
    if tier is None:
        out.update(cls="A", sub="골드에 없음")
        return out
    if tier == "partial":
        out.update(cls="미분류", sub="골드에 부분 일치만(3-gram ≥0.8) — 원문 그대로는 없음")
        return out
    if tier == "weak":
        out.update(cls="미분류", sub="짧은 인용(8자 미만)이 골드의 긴 문장 안에서만 발견 — 같은 사실인지 대조 불가")
        return out
    own: list[str] = []
    for _, k, ref in hits:
        for o in gold.owners_of(k, ref):
            if o not in own:
                own.append(o)
    out["gold_owner_nodes"] = own
    out["reach"] = ("returned" if any(o in ctx.returned for o in own) else "direct(family-of-unit)" if any(o in ctx.reach_direct for o in own)
                    else "1hop" if any(o in ctx.reach_1hop for o in own) else ("none" if own else "no-node-owner"))
    hit, how = in_hub(q, hits, ctx)
    if hit:
        out.update(cls="C", sub="허브 응답에 있음 · 답이 놓침" + ("(답: 정보 없음 류 표현 있음)" if row.get("answer_says_unknown") else ""), how=how)
        return out
    subs: list[tuple[str, dict[str, Any]]] = []
    jev = ctx.jev
    for ns, k, ref in hits:
        if k == "fact":
            okind, ons = gold.owner_nodes(ref)
            sec = ref["section"]
            if okind == "pair":
                called = set(ctx.tools_called) & {"pair_check", "compare"}
                fams_called = {gold.fam_of(p) for p in ctx.pair_procs if gold.fam_of(p)} | set(ctx.pair_procs)
                ends = set(ons)
                if not called:
                    subs.append(("쌍 관계 fact — pair_check/compare 안 부름", ref))
                elif ends and ends <= fams_called:
                    subs.append((("쌍 관계 fact — 쌍 맞음 · evidence 섹션 안 요청(claims id 만)" if "evidence" not in ctx.all_req_sections
                                  else "쌍 관계 fact — 쌍 맞음 · evidence 요청했는데도 안 실림"), ref))
                else:
                    subs.append(("쌍 관계 fact — 쌍 도구 불렀으나 다른 쌍", ref))
                continue
            if okind == "combo":
                subs.append((("조합(CC · 레시피) fact — combos 안 부름" if "combos" not in ctx.tools_called else "조합(CC · 레시피) fact — combos 불렀으나 안 실림"), ref))
                continue
            pre = "" if okind == "node" else "scope(claim) fact · 대상 "
            if not ons:
                subs.append((("step8 메모(step8_notes) fact — 어느 노드에도 안 붙음(도구로 못 꺼냄)" if "step8_notes" in ref["fact_id"] else pre + "대상 노드 없음"), ref))
                continue
            on = next((o for o in ons if o in ctx.more_cards), None)
            if on:
                subs.append((pre + "recommend 상한(more_cards) 밖", ref))
                continue
            on = next((o for o in ons if o in ctx.reach_direct), None)
            if on:
                if sec in ctx.req_sections.get(on, set()) or any(sec in ctx.req_sections.get(i, set()) for i in ctx.returned if gold.fam_of(i) == on) \
                        or (okind == "scope" and sec == "checks" and "check_conditions" in ctx.tools_called):
                    subs.append((pre + "섹션 요청했는데도 응답에 없음(section 매핑 밖)", ref))
                else:
                    tag = pre + "slim 카드 밖 섹션(section 안 요청)"
                    if case == "case3" and jev:
                        if sec in (jev.get("sections_dropped") or []):
                            tag += " · Jev 상위4 밖"
                        elif (jev.get("info") or {}).get(sec, 0) < 0.5:
                            tag += " · Jev noul<0.5(안 고름)"
                        elif sec in (jev.get("sections") or []):
                            tag += " · Jev 골랐으나 도구가 그 섹션 안 줌"
                        else:
                            tag += " · 이 도구는 sections 안 받음"
                    subs.append((tag, ref))
                continue
            on = next((o for o in ons if o in ctx.reach_1hop), None)
            if on:
                subs.append((pre + "이웃 노드(1-hop) — 도구가 안 펼침", ref))
                continue
            subs.append((pre + "경로가 그 노드에 안 닿음", ref))
        elif k == "node_attr":
            on = ref["node_id"]
            nk = gold.nodes[on]["kind"]
            subs.append(((f"노드 속성({nk} · full 카드 전용)" if on in ctx.reach_direct else f"노드 속성({nk}) · 노드에 안 닿음"), ref))
        elif k == "node_name":
            on = ref["node_id"]
            subs.append((("노드 이름만 일치(노드 도달)" if on in ctx.reach_direct else "노드 이름만 일치 · 노드에 안 닿음"), ref))
        elif k == "edge_attr":
            subs.append((("엣지 속성 — 양끝 도달" if (ref["from"] in ctx.reach_direct or ref["to"] in ctx.reach_direct) else "엣지 속성 · 양끝 노드에 안 닿음"), ref))
        else:
            subs.append(("전역(globals) 속성", ref))
    subs.sort(key=lambda x: _rank(x[0]))
    best = subs[0]
    out.update(cls="B", sub=best[0], gold_owner=best[1].get("owner_id") or best[1].get("node_id") or best[1].get("edge_id"), gold_section=best[1].get("section"))
    return out


def coarse(s: str) -> str:
    if s.startswith("slim 카드 밖 섹션") or s.startswith("scope(claim) fact · 대상 slim"):
        return "① slim 카드 밖 섹션(section 안 요청)"
    if "섹션 요청했는데도" in s:
        return "② 섹션은 요청했는데 그 fact 가 section 매핑에 안 실림"
    if "recommend 상한" in s:
        return "③ recommend 상한(more_cards)"
    if s.startswith("쌍 관계 fact"):
        return "④ 쌍 관계 fact(pair_check · compare)"
    if "이웃 노드" in s or "경로가 그 노드" in s or "노드에 안 닿음" in s:
        return "⑤ 의도 경로 · 도구가 그 노드에 안 닿음"
    if "full 카드 전용" in s:
        return "⑥ 노드 속성(full 카드 전용 · slim 에 없음)"
    if s.startswith("엣지 속성"):
        return "⑦ 엣지 속성에만 있음(fact 아님)"
    if "step8_notes" in s or s.startswith("조합"):
        return "⑧ 어느 노드에도 안 붙은 fact(step8 메모 · CC 조합)"
    return "⑨ 기타"


# ── 크기 ───────────────────────────────────────────────────────────────────────
def stat(xs: list[int]) -> dict[str, Any]:
    if not xs:
        return {"n": 0}
    s = sorted(xs)
    return {"n": len(s), "median": int(statistics.median(s)), "p95": s[min(len(s) - 1, int(round(0.95 * (len(s) - 1))))], "max": s[-1]}


def tool_bucket(tool: str, inp: dict[str, Any]) -> str:
    if tool == "procedure_card":
        return "procedure_card:family" if str(inp.get("id", "")).startswith("family:") else "procedure_card:unit"
    return tool


def size_table(calls: list[dict[str, Any]], case3_keys: set[str]) -> dict[str, Any]:
    """도구별 바이트 — 기본 응답(요청 sections 없음) · sections 있음 따로 · case3 경로 호출 따로 · §5-0-1 표 대조."""
    base: dict[str, list[int]] = collections.defaultdict(list)
    withs: dict[str, list[int]] = collections.defaultdict(list)
    c3: list[int] = []
    c3_by: dict[str, list[int]] = collections.defaultdict(list)
    for c in calls:
        if c["status"] != 200:
            continue
        n = len(c["text"].encode("utf-8"))
        inp = c.get("input") or {}
        b = tool_bucket(c["tool"], inp)
        (withs if inp.get("sections") else base)[b].append(n)
        if c.get("key") in case3_keys:
            c3.append(n)
            c3_by[b].append(n)
    out: dict[str, Any] = {}
    for t in list(SIZE_CAPS):
        if t == "case3_path":
            continue
        d, w = stat(base[t]), stat(withs[t])
        cap_m, cap_p = SIZE_CAPS[t]
        out[t] = {"default": d, "with_sections": w, "case3_path": stat(c3_by[t]), "cap_median": cap_m, "cap_p95": cap_p,
                  "pass": d.get("median") is None or (d["median"] <= cap_m and d["p95"] <= cap_p)}
    s3 = stat(c3)
    out["case3_path"] = {"default": s3, "cap_median": SIZE_CAPS["case3_path"][0], "cap_p95": SIZE_CAPS["case3_path"][1],
                         "pass": s3.get("median") is None or (s3["median"] <= SIZE_CAPS["case3_path"][0] and s3["p95"] <= SIZE_CAPS["case3_path"][1])}
    return out


def recorded_case3_sizes(runs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """fail-triage2.json case3_sizes 와 같은 셈(hub.result_bytes · n=159)."""
    xs = [((d["cases"]["case3"].get("trace") or {}).get("hub") or {}).get("result_bytes") for d in runs.values()]
    xs = [x for x in xs if x]
    return {"n": len(xs), "median": int(statistics.median(xs)), "p95": sorted(xs)[int(0.95 * (len(xs) - 1))]}


# ── 조항 fixture(SPEC §8) ──────────────────────────────────────────────────────
def make_clauses(spec: Path, out: Path) -> list[dict[str, Any]]:
    lines = spec.read_text(encoding="utf-8").splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("## 8. 부록"))
    rows = []
    for ln in lines[start:]:
        if not ln.startswith("| "):
            continue
        cells = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(cells) < 10 or not re.fullmatch(r"\d+", cells[0]):
            continue
        clause = cells[8].replace("*", "")
        key = (cells[1], cells[2], ITEM_INV[cells[3]])
        data_why = NOT_CLOSABLE_DATA.get(key)
        rows.append({"n": int(cells[0]), "question_no": cells[1], "case": cells[2], "item": ITEM_INV[cells[3]], "sub2": cells[4],
                     "gold_owner_section": cells[5], "ids": cells[6].strip("`"), "calls": cells[7], "clause": clause, "memo": cells[9],
                     "spec_clause": clause, "not_closable": clause in NOT_CLOSABLE_CLAUSES or bool(data_why),
                     **({"not_closable_why": data_why, "clause": "N-데이터"} if data_why else {})})
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"source": "SPEC-005.md §8 표(0.3.3)", "n": len(rows), "rows": rows}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return rows


# ── 실행 ──────────────────────────────────────────────────────────────────────
def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=("make-clauses", "baseline", "rerun"))
    p.add_argument("--base-url", default="http://127.0.0.1:18005")
    p.add_argument("--inprocess", action="store_true")
    p.add_argument("--fail-triage2", type=Path, default=E / "build-out" / "fail-triage2.json")
    p.add_argument("--runs", type=Path, default=E / "runs" / "runs.jsonl")
    p.add_argument("--replay", type=Path, default=E / "build-out" / "recheck" / "replay2.json")
    p.add_argument("--clauses", type=Path, default=OUT / "b186-clauses.json")
    p.add_argument("--export-old", type=Path, default=OUT / "gold-export.d3a1abd52f70afe9.json")
    p.add_argument("--export-new", type=Path, default=BACKEND / "build-out" / "gold-export.json")
    p.add_argument("--out-prefix", type=Path, default=None)
    p.add_argument("--save-responses", type=Path, default=None)
    a = p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.mode == "make-clauses":
        rows = make_clauses(SPEC, a.clauses)
        print(f"clauses — {len(rows)} rows · " + " · ".join(f"{k} {v}" for k, v in collections.Counter(r['clause'] for r in rows).most_common()) + f" → {a.clauses}")
        return 0
    runs = load_runs(a.runs)
    ft = json.loads(a.fail_triage2.read_text(encoding="utf-8"))
    clauses = json.loads(a.clauses.read_text(encoding="utf-8"))["rows"]
    clause_of = {(r["question_no"], r["case"], r["item"]): r for r in clauses}
    raw = Raw(RAW)
    replay = json.loads(a.replay.read_text(encoding="utf-8"))
    qrid = {d["question_no"]: rid for rid, d in runs.items()}
    case3_keys = {h["key"] for h in replay["case3"].values() if h}
    prefix = a.out_prefix or (OUT / ("recheck2-report.baseline" if a.mode == "baseline" else "recheck2-report"))
    meta: dict[str, Any] = {"mode": a.mode, "ran_at": datetime.now(UTC).isoformat(), "batch": BATCH, "export_old": {"path": str(a.export_old)},
                            "replay": {"path": str(a.replay), "build_hash": replay.get("build_hash"), "unique_calls": len(replay["calls"]),
                                       "meta_replay_unique": ft["meta"]["replay_unique"]},
                            "runs": str(a.runs), "fail_triage2_rows": len(ft["rows"]), "b_rows": len(ft["b_rows"]), "clauses": len(clauses),
                            "judge": ("triage.py · recheck.py 와 같은 식 — norm(소문자 · 공백 · 기호 제거) · 양방향 포함(골드 쪽 8자 이상) · 3-gram 0.8 부분 · fact id 일치 · "
                                      "닫힘 = 응답 JSON 전체의 fact id ∪ 엣지 id(따옴표 안) 또는 정규화 인용 · 같은 식을 이 파일에 적음(import 안 함)")}
    # 기록 응답으로 묶음 재구성(replay2)
    def rec_calls(rid: str, case: str) -> list[dict[str, Any]]:
        if case == "case2":
            return [{**replay["calls"][c["key"]], "key": c["key"], "rec_bytes": c["rec_bytes"]} for c in replay["case2"].get(rid, [])]
        h = replay["case3"].get(rid)
        return [{**replay["calls"][h["key"]], "key": h["key"], "rec_bytes": h["rec_bytes"]}] if h else []
    gold_old = Gold(a.export_old)
    meta["export_old"]["build_hash"] = gold_old.hash
    # 판정 동일성 — 옛 export + 기록 응답으로 fail-triage2 rows 320 재분류
    ident_same, ident_diff = 0, []
    for row in ft["rows"]:
        if row["case"] == "case1":
            ident_same += 1
            continue
        rid = qrid[row["question_no"]]
        tr = runs[rid]["cases"][row["case"]].get("trace") or {}
        ctx = HubContext(gold_old, rec_calls(rid, row["case"]), tr.get("jev") if row["case"] == "case3" else None, (tr.get("hub") or {}) if row["case"] == "case3" else {})
        res = classify(gold_old, raw, row, ctx, row["case"])
        if res["cls"] == row["cls"] and res["sub"] == row["sub"]:
            ident_same += 1
        else:
            ident_diff.append({"question_no": row["question_no"], "case": row["case"], "old": [row["cls"], row["sub"]], "new": [res["cls"], res["sub"]]})
    identity = {"rows": len(ft["rows"]), "same": ident_same, "diff": ident_diff}
    # 대상 응답
    if a.mode == "baseline":
        gold_new = gold_old
        meta["export_new"] = {"path": str(a.export_old), "build_hash": gold_old.hash, "note": "baseline — 옛 export · 기록 응답(replay2)"}
        meta["target"] = "replay2(기록 응답)"
        calls_new = {(rid, case): rec_calls(rid, case) for rid in runs for case in ("case2", "case3")}
        all_calls = [{**c, "key": k} for k, c in replay["calls"].items()]
    else:
        gold_new = Gold(a.export_new)
        meta["export_new"] = {"path": str(a.export_new), "build_hash": gold_new.hash}
        client = inprocess_client() if a.inprocess else None
        meta["target"] = "inprocess" if a.inprocess else a.base_url
        meta["knobs"] = {k: os.environ[k] for k in sorted(os.environ) if k.startswith("GOLD_")}
        cache: dict[str, dict[str, Any]] = {}
        all_calls = []
        for k in sorted(replay["calls"]):
            c = replay["calls"][k]
            st, txt = rest_call(a.base_url, c["tool"], c["input"], client)
            cache[k] = {"tool": c["tool"], "input": c["input"], "status": st, "text": txt, "key": k}
            all_calls.append(cache[k])
        calls_new = {}
        for rid in runs:
            calls_new[(rid, "case2")] = [{**cache[c["key"]], "rec_bytes": c["rec_bytes"]} for c in replay["case2"].get(rid, [])]
            h = replay["case3"].get(rid)
            calls_new[(rid, "case3")] = [{**cache[h["key"]], "rec_bytes": h["rec_bytes"]}] if h else []
        meta["target_build_hash"] = next((json.loads(c["text"]).get("build", {}).get("build_hash") for c in all_calls if c["status"] == 200), None)
        if a.save_responses:
            a.save_responses.write_text(json.dumps(all_calls, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    # B 186 닫힘 — 새 export 로 gold_match 갱신 뒤 응답 대조 · (a) 응답 안 · (b) 추가 호출 1(코디 11-01)
    results = []
    extra_cache: dict[str, tuple[int, str]] = {}
    if a.mode == "baseline":
        client = None
    for r in ft["b_rows"]:
        rid, case = qrid[r["question_no"]], r["case"]
        tr = runs[rid]["cases"][case].get("trace") or {}
        ctx = HubContext(gold_new, calls_new[(rid, case)], tr.get("jev") if case == "case3" else None, (tr.get("hub") or {}) if case == "case3" else {})
        q = norm(r["evidence"]["quote"])
        tier, hits = gold_new.gold_match(q)
        closed, how = (in_hub(q, hits, ctx, broad=True) if tier == "exact" else (False, None))
        cl = clause_of[(r["question_no"], case, r["item"])]
        fids = [ref["fact_id"] for _, k, ref in hits if k == "fact"]
        eids = [ref["edge_id"] for _, k, ref in hits if k == "edge_attr"]
        owners = sorted({o for _, k, ref in hits for o in gold_new.owners_of(k, ref)})
        intent = None
        if case == "case3":
            intent = ((ctx.hub_trace.get("input") or {}).get("intent")) or ((ctx.jev or {}).get("intent"))
        why = None
        closed_a = closed
        closed_b, how_b = (False, None)
        if not closed_a and a.mode == "rerun" and not cl["not_closable"]:
            closed_b, how_b = reach_one_call(gold_new, ctx, fids, a.base_url, client, extra_cache)
        closed = closed_a or closed_b
        if not closed:
            why = not_closed_why(gold_new, ctx, fids, eids, owners, cl)
        results.append({"question_no": r["question_no"], "case": case, "item": r["item"], "intent": intent, "sub": r["sub"], "group": coarse(r["sub"]),
                        "clause": cl["clause"], "not_closable": cl["not_closable"], "not_closable_why": cl.get("not_closable_why"),
                        "gold_owner": r.get("gold_owner"), "gold_section": r.get("gold_section"),
                        "path": r["evidence"]["path"], "new_gold_tier": tier, "new_fact_ids": fids[:6], "new_edge_ids": eids[:4], "owners": owners[:6],
                        "closed": closed, "closed_a": closed_a, "closed_b": closed_b, "how_b": how_b,
                        "closed_with_text": bool(closed_a and how and not how.startswith(("fact id 만", "엣지 id"))), "how": how,
                        "calls": [{"tool": c["tool"], "status": c["status"], "sections": (c.get("input") or {}).get("sections"), "intent": (c.get("input") or {}).get("intent")} for c in calls_new[(rid, case)]],
                        "errors": ctx.errors, "why": why})
    reach = [x for x in results if not x["not_closable"]]
    nc = [x for x in results if x["not_closable"]]
    closed_reach = sum(1 for x in reach if x["closed"])
    closed_all = sum(1 for x in results if x["closed"])
    n273 = ft["c_rate"]["n"]
    spec161 = [x for x in results if x["clause"] not in ("X0", "N-다른계열", "N-제품수준", "N-9단계", "N-조항없음")]  # SPEC §8 161(데이터 불가 6 포함)
    rate = {"reach161": {"n": len(reach), "closed": closed_reach, "rate": round(closed_reach / len(reach), 4) if reach else None, "target": 0.9,
                         "pass": bool(reach) and closed_reach / len(reach) >= 0.9,
                         "a_only": sum(1 for x in reach if x["closed_a"]), "b_only": sum(1 for x in reach if x["closed_b"] and not x["closed_a"]),
                         "note": "닫힘 = (a) 응답 안 id · 인용 ∪ (b) 응답 노드에서 expand/sections 한 번(코디 11-01 2)) · 분모 = SPEC §8 161 − 데이터 불가 6"},
            "spec161": {"n": len(spec161), "closed": sum(1 for x in spec161 if x["closed"]), "a_only": sum(1 for x in spec161 if x["closed_a"])},
            "reach161_with_text": {"n": len(reach), "closed": sum(1 for x in reach if x["closed_with_text"]), "note": "원문(facts[] · 인용 · 골드 문장)으로 닫힌 행만(보고)"},
            "b186": {"n": len(results), "closed": closed_all, "rate": round(closed_all / len(results), 4) if results else None, "cap": round(len(reach) / len(results), 4)},
            "fail273": {"n": n273, "closed": closed_all, "rate": round(closed_all / n273, 4) if n273 else None},
            "not_closable25": {"n": len(nc), "closed": sum(1 for x in nc if x["closed"]), "by_clause": dict(collections.Counter(x["clause"] for x in nc)),
                               "rows": [{"question_no": x["question_no"], "case": x["case"], "item": x["item"], "clause": x["clause"], "closed": x["closed"], "why": x.get("not_closable_why")} for x in nc]}}

    def table(key: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = collections.OrderedDict()
        for x in sorted(rows, key=lambda x: str(x[key] or "?")):
            g_ = out.setdefault(str(x[key] or "?"), {"n": 0, "closed": 0, "not_closable": 0})
            g_["n"] += 1
            g_["closed"] += int(x["closed"])
            g_["not_closable"] += int(x["not_closable"])
        return out
    by_clause = table("clause", results)
    by_group = table("group", results)
    by_intent = table("intent", results)
    by_case = table("case", results)
    by_tool = collections.OrderedDict()
    for x in sorted(results, key=lambda x: ",".join(dict.fromkeys(c["tool"] for c in x["calls"] if c["tool"] in CARD_TOOLS)) or "—"):
        k = ",".join(dict.fromkeys(c["tool"] for c in x["calls"] if c["tool"] in CARD_TOOLS)) or "—"
        g_ = by_tool.setdefault(k, {"n": 0, "closed": 0, "not_closable": 0})
        g_["n"] += 1
        g_["closed"] += int(x["closed"])
        g_["not_closable"] += int(x["not_closable"])
    # (iii) C3 5 — 정규화 인용이 원문 칸(text 값 중 같은 객체에 id 가 있는 것)에 · Q003 반대 조건
    c3_rows = []
    for cr in ft["c_rows"]:
        key = (cr["question_no"], cr["case"])
        if key not in C3_ROWS and key != ("Q003", "case2") and key != ("Q003", "case3") and key not in {(q, c) for q, c, _ in C3_OUT}:
            continue
        rid = qrid[cr["question_no"]]
        calls = calls_new[(rid, cr["case"])]
        ctx = HubContext(gold_new, calls, None, {})
        q = norm(cr["evidence"]["quote"])
        tier_, hits_ = gold_new.gold_match(q)
        in_text = (len(q) >= 6 and q in ctx.text_norm) or bool({ref["fact_id"] for _, k, ref in hits_ if k == "fact"} & ctx.hub_facts) \
            or any(len(ns) >= 8 and ns in ctx.text_norm for ns, _, _ in hits_)  # triage 와 같은 식을 원문 칸에만
        row: dict[str, Any] = {"question_no": cr["question_no"], "case": cr["case"], "c_sub": cr["c_sub"], "fact": cr["c_info"].get("fact"), "quote_len": len(q),
                               "in_text_fields": in_text, "in_body_anywhere": len(q) >= 6 and q in ctx.hub_norm,
                               "calls": [c["tool"] + ("" if c["status"] == 200 else f"({c['status']})") for c in calls]}
        if key in C3_ROWS:
            row["kind"] = "C3 분모 5"
            row["pass"] = in_text
        elif cr["question_no"] == "Q003":
            row["kind"] = "Q003 반대 조건(C1′ 엉뚱한 연결)"
            row.update(q003_reverse(gold_new, ctx))
            if not row["botox_cards"] and a.mode == "rerun":  # 추천 응답에 보톡스(M1) 카드가 없으면 보톡스 턱선 단위 카드(T3 · I-03 C1′)로 따로 확인
                st, txt = rest_call(a.base_url, "procedure_card", {"id": Q003_BOTOX_JAW_UNIT, "intent": "I-03"}, client if a.inprocess else None)
                row["botox_jaw_card"] = {"unit": Q003_BOTOX_JAW_UNIT, "status": st, "has_sc": st == 200 and Q003_SC in txt}
                row["sc_present_in_botox_jaw_cards"] = bool(row["botox_jaw_card"]["has_sc"])
            row["pass"] = row["sc_absent_in_thread_cards"] and row["sc_present_in_botox_jaw_cards"]
        else:
            row["kind"] = "분모 밖 — " + next(w for q_, c_, w in C3_OUT if (q_, c_) == key)
            row["pass"] = None
        c3_rows.append(row)
    c3_rows.sort(key=lambda x: (x["question_no"], x["case"]))
    c3_den = [x for x in c3_rows if x["kind"] == "C3 분모 5"]
    c3 = {"den": len(c3_den), "pass_n": sum(1 for x in c3_den if x["pass"]), "pass": len(c3_den) == 5 and all(x["pass"] for x in c3_den),
          "q003": [x for x in c3_rows if x["question_no"] == "Q003"], "q003_pass": all(x["pass"] for x in c3_rows if x["question_no"] == "Q003"), "rows": c3_rows}
    errors = [c for c in all_calls if c["status"] != 200]
    err_summary = collections.Counter(f"{c['tool']} {c['status']} {c['text'][:90]}" for c in errors)
    sizes = size_table(all_calls, case3_keys)
    report = {"meta": meta, "identity": identity, "rate": rate, "by_clause": by_clause, "by_group": by_group, "by_intent": by_intent, "by_case": by_case, "by_tool": by_tool,
              "c3": c3, "errors": {"n": len(errors), "summary": dict(err_summary.most_common()),
                                    "rows": [{"tool": c["tool"], "input": c["input"], "status": c["status"], "text": c["text"][:160]} for c in sorted(errors, key=lambda c: c["key"])]},
              "sizes": sizes, "sizes_recorded_case3": recorded_case3_sizes(runs), "rows": results, "not_closed_rows": [x for x in results if not x["closed"]]}
    Path(str(prefix) + ".json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    Path(str(prefix) + ".md").write_text(render(report), encoding="utf-8")
    (OUT / "sizes.json").write_text(json.dumps({"meta": {k: v for k, v in meta.items() if k != "ran_at"}, "sizes": sizes}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8") if a.mode == "rerun" else None
    print(f"{a.mode} — identity {ident_same}/{len(ft['rows'])} · B 닫힘 {closed_reach}/{len(reach)}(a {rate['reach161']['a_only']} + b {rate['reach161']['b_only']}) · {closed_all}/{len(results)}(186) · C3 {c3['pass_n']}/{c3['den']} · Q003 {c3['q003_pass']} · 오류 {len(errors)} · case3 경로 중앙 {sizes['case3_path']['default'].get('median')} → {prefix}.md")
    return 0


def q003_reverse(gold: Gold, ctx: HubContext) -> dict[str, Any]:
    """Q003 — SC-jawline-M1 이 실리프팅(M9) 카드에 없고 보톡스(M1) 턱 단위 카드에는 있음(recommend cards[] · 카드 JSON 문자열 기준)."""
    thread, botox = [], []
    for o in ctx.objs:
        if o["tool"] != "recommend":
            continue
        for card in o["obj"].get("cards") or []:
            s = json.dumps(card, ensure_ascii=False)
            fam = card.get("family") or gold.fam_of(card.get("id", ""))
            if fam == "family:M9":
                thread.append((card["id"], Q003_SC in s))
            elif fam == "family:M1":
                botox.append((card["id"], Q003_SC in s))
    return {"thread_cards": thread, "botox_cards": botox,
            "sc_absent_in_thread_cards": bool(thread) and not any(x for _, x in thread),
            "sc_present_in_botox_jaw_cards": bool(botox) and any(x for _, x in botox)}


def _request_nodes(c: dict[str, Any]) -> list[str]:
    inp = c.get("input") or {}
    out: list[str] = []
    for k in ("id", "procedure", "prior"):
        v = inp.get(k)
        if isinstance(v, str):
            out.append(v)
    out += [x for x in (inp.get("procedures") or []) if isinstance(x, str)]
    return out


def reach_one_call(gold: Gold, ctx: HubContext, fids: list[str], base: str, client: Any, cache: dict[str, tuple[int, str]]) -> tuple[bool, str | None]:
    """(b) 코디 11-01 — 응답에 나온 노드에서 expand(sections=[그 fact 의 section]) 또는 pair_check(sections=evidence) 한 번(≤1 추가 호출)으로 그 fact id 에 닿음.
    후보 노드 = fact 의 owner · attached_to · (엣지 owner 면 양끝) · 단위 시술의 계열 중 응답 JSON 에 나온 것(최대 6) — 실제로 불러 확인(결정론 · 캐시)."""
    def call(tool: str, args: dict[str, Any]) -> tuple[int, str]:
        k = call_key(tool, args)
        if k not in cache:
            cache[k] = rest_call(base, tool, args, client)
        return cache[k]
    for fid in fids:
        f = gold.facts.get(fid)
        if not f:
            continue
        sec = f["section"]
        oid = f["owner_id"]
        owners: list[str] = [a for a in (f.get("attached_to") or []) if a in gold.nodes]
        if oid in gold.nodes:
            owners.insert(0, oid)
        e = gold.edges_by_id.get(oid) or gold.edges_by_id.get(oid.split("#", 1)[0])
        ends: list[str] = []
        if e:
            for side in ("from_id", "to_id"):
                x = e[side] or ""
                ends += [y for y in (x[11:].split("|") if x.startswith("candidates:") else [x]) if y in gold.nodes]
        cands = [n for n in owners + ends if n in ctx.returned]
        cands += [gold.fam_of(n) for n in owners if gold.fam_of(n) in ctx.returned and gold.fam_of(n) not in cands]
        # 응답에 나온 시술 노드(요청 노드 먼저 · 그 다음 응답 순)도 후보 — expand(n, sections=[sec]) 가 그 노드의 section 매핑(계열 상속 주장 · 합병증 잎 · 부착 메모)으로 닿는지 실제로 불러 봄
        req_nodes = [x for c in ctx.calls for x in _request_nodes(c) if x in gold.nodes]
        procs = [n for n in req_nodes + sorted(ctx.returned) if gold.nodes.get(n, {}).get("kind") in ("unit_procedure", "family", "product", "combo") and n not in cands]
        cands += procs
        for n in list(dict.fromkeys(cands))[:8]:
            st, txt = call("expand", {"id": n, "sections": [sec]})
            page, prev = 1, None
            while st == 200 and txt != prev and f'"{fid}"' not in txt and "facts_uncut" in txt and (json.loads(txt).get("more") or {}).get(sec):  # v3.3 쪽 넘김(WORK-008 · 같은 section = 1 추가 호출로 셈)
                page, prev = page + 1, txt
                st, txt = call("expand", {"id": n, "sections": [sec], "page": page})
            if st == 200 and f'"{fid}"' in txt:
                return True, f"expand({n}, sections=[{sec}])" + (f" page {page}" if page > 1 else "")
        if oid.startswith("procedure_relation:") and ends:
            ins = [n for n in ends if n in ctx.returned or gold.fam_of(n) in ctx.returned]
            procs = list(dict.fromkeys([n for n in ins if gold.nodes[n]["kind"] in ("unit_procedure", "family", "product")]))[:2]
            if procs:
                st, txt = call("pair_check", {"procedures": procs, "sections": ["evidence"]})
                if st == 200 and f'"{fid}"' in txt:
                    return True, f"pair_check({procs}, sections=[evidence])"
    return False, None


def not_closed_why(gold: Gold, ctx: HubContext, fids: list[str], eids: list[str], owners: list[str], cl: dict[str, Any]) -> dict[str, Any]:
    """닫히지 않은 행의 사유(행 단위 재셈 · W-3) — 호출 · 응답 노드 도달 · 요청 section · fact section · 조항."""
    secs = sorted({gold.facts[f]["section"] for f in fids if f in gold.facts})
    owner_hit = [o for o in owners if o in ctx.returned]
    fam_hit = [o for o in owners if o in ctx.reach_direct and o not in ctx.returned]
    hop = [o for o in owners if o in ctx.reach_1hop and o not in ctx.reach_direct]
    if not ctx.tools_called:
        reason = "허브 안 부름"
    elif not (set(ctx.tools_called) & set(CARD_TOOLS)):
        reason = "resolve · vocab 만"
    elif ctx.errors and len(ctx.errors) == len(ctx.calls):
        reason = "호출 전부 오류(기록 입력 오류)"
    elif owner_hit:
        reason = "응답 노드 도달 — fact 가 응답 어느 칸에도 없음(section 매핑 · 동봉 · 색인 밖)"
    elif fam_hit:
        reason = "계열 도달 — 단위 · 제품 수준 fact 가 by_unit · 색인 밖"
    elif hop:
        reason = "1-hop 이웃 — 동봉 · 색인에 그 노드 id 가 없음"
    elif owners:
        reason = "경로가 그 노드에 안 닿음"
    else:
        reason = "owner 노드 없음(scope · combo · 엣지)"
    return {"reason": reason, "fact_sections": secs, "owner_returned": owner_hit[:4], "family_reached": fam_hit[:4], "one_hop": hop[:4],
            "requested_sections": sorted(ctx.all_req_sections), "clause": cl["clause"], "memo": cl["memo"][:80]}


def render(rep: dict[str, Any]) -> str:
    m, r = rep["meta"], rep["rate"]
    L = [f"# recheck2 — {m['mode']} · B 186 재인용 대조(SPEC-005 v3.2 §6-5)", "",
         f"배치 `{m['batch']}` · 옛 export `{m['export_old']['build_hash']}` · 새 export `{m['export_new']['build_hash']}` · 대상 {m.get('target')} · 대상 빌드 {m.get('target_build_hash', m['replay'].get('build_hash'))} · replay2 유일 호출 {m['replay']['unique_calls']}(= meta.replay_unique {m['replay']['meta_replay_unique']})",
         f"판정: {m['judge']}", "",
         "## 1. 판정 동일성(옛 export + 기록 응답 → fail-triage2 rows 재분류)", "",
         f"- cls · sub 같음 **{rep['identity']['same']}/{rep['identity']['rows']}**" + ("" if not rep["identity"]["diff"] else " · 다른 행: " + json.dumps(rep["identity"]["diff"][:10], ensure_ascii=False)), "",
         "## 2. B 재인용률 (i)", "",
         "| 기준 | 분모 | 닫힘 | 비율 | 목표 | 판정 |", "|---|---|---|---|---|---|",
         f"| 조항 닿는 행(SPEC 161 − 데이터 불가 6) | {r['reach161']['n']} | {r['reach161']['closed']} (a {r['reach161']['a_only']} + b {r['reach161']['b_only']}) | {r['reach161']['rate']} | ≥ 0.9 | {'PASS' if r['reach161']['pass'] else 'FAIL'} |",
         f"| SPEC §8 161 그대로 | {r['spec161']['n']} | {r['spec161']['closed']} (a {r['spec161']['a_only']}) | {round(r['spec161']['closed'] / r['spec161']['n'], 4)} | 보고 | — |",
         f"| (보고) 161 중 원문으로 닫힘(fact · 엣지 id 만 제외) | {r['reach161_with_text']['n']} | {r['reach161_with_text']['closed']} | {round(r['reach161_with_text']['closed'] / r['reach161_with_text']['n'], 4) if r['reach161_with_text']['n'] else None} | 보고 | — |",
         f"| B 186 | {r['b186']['n']} | {r['b186']['closed']} | {r['b186']['rate']} | 보고(상한 {r['b186']['cap']}) | — |",
         f"| 2차 실패 273 | {r['fail273']['n']} | {r['fail273']['closed']} | {r['fail273']['rate']} | 보고 | — |",
         f"| 닫지 않는 행 25(SPEC §8 X0 · N) | {r['not_closable25']['n']} | {r['not_closable25']['closed']} | — | 분자 · 분모 밖 | {json.dumps(r['not_closable25']['by_clause'], ensure_ascii=False)} |", "",
         "### 조항별", "", "| 조항 | 행 | 닫힘 | 닫지 않는 행 |", "|---|---|---|---|"]
    for k, v in rep["by_clause"].items():
        L.append(f"| {k} | {v['n']} | {v['closed']} | {v['not_closable']} |")
    for title, key in (("묶음 ①~⑨", "by_group"), ("의도별(case3 hub.input.intent · case2 —)", "by_intent"), ("케이스별", "by_case"), ("도구별(카드 도구 호출 묶음)", "by_tool")):
        L += ["", f"### {title}", "", "| 키 | 행 | 닫힘 | 닫지 않는 행 |", "|---|---|---|---|"]
        for k, v in rep[key].items():
            L.append(f"| {k} | {v['n']} | {v['closed']} | {v['not_closable']} |")
    L += ["", f"### 닫지 않는 행 {r['not_closable25']['n']}(SPEC §8 25 + 데이터 불가 6 · 코디 11-01)", "", "| 문항 | 케이스 | 항목 | 조항 | 사유 | 닫힘(참고) |", "|---|---|---|---|---|---|"]
    for x in r["not_closable25"]["rows"]:
        L.append(f"| {x['question_no']} | {x['case']} | {ITEM[x['item']]} | {x['clause']} | {x.get('why') or ''} | {'○' if x['closed'] else ''} |")
    L += ["", "### (b) 로 닫힌 행(응답 노드 + 추가 호출 1)", "", "| 문항 | 케이스 | 조항 | fact | 추가 호출 |", "|---|---|---|---|---|"]
    for x in rep["rows"]:
        if x.get("closed_b") and not x.get("closed_a"):
            L.append(f"| {x['question_no']} | {x['case']} | {x['clause']} | {(x['new_fact_ids'] or ['—'])[0][:70]} | {x['how_b']} |")
    L += ["", "### 닫히지 않은 행 전부(사유 · 행 단위)", "", "| 문항 | 케이스 | 항목 | 의도 | 조항 | 빠진 칸 | 골드 owner#section | 새 fact id | 호출 | 사유 | 닫지 않는 행 |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in rep["not_closed_rows"]:
        calls = ",".join(dict.fromkeys(c["tool"] + ("" if c["status"] == 200 else f"({c['status']})") for c in x["calls"]))
        L.append(f"| {x['question_no']} | {x['case']} | {ITEM[x['item']]} | {x['intent'] or '—'} | {x['clause']} | {x['sub'][:36]} | {x['gold_owner']}{('#' + x['gold_section']) if x.get('gold_section') else ''} | {(x['new_fact_ids'] or x['new_edge_ids'] or ['—'])[0][:70]} | {calls} | {(x['why'] or {}).get('reason', '')} | {'○' if x['not_closable'] else ''} |")
    c3 = rep["c3"]
    L += ["", f"## 3. (iii) C3 fact 없는 행 5 → 원문 칸 안 {c3['pass_n']}/{c3['den']} ({'PASS' if c3['pass'] else 'FAIL'}) · Q003 반대 조건 {'PASS' if c3['q003_pass'] else 'FAIL'}", "",
          "| 문항 | 케이스 | 구분 | fact | 원문 칸 안 | 본문 아무 데나 | 호출 | 판정 |", "|---|---|---|---|---|---|---|---|"]
    for x in c3["rows"]:
        extra = ""
        if x["question_no"] == "Q003":
            extra = f" · 실리프팅 카드 {x.get('thread_cards')} · 보톡스 카드 {x.get('botox_cards')}"
        L.append(f"| {x['question_no']} | {x['case']} | {x['kind']} | {x.get('fact') or '—'} | {x['in_text_fields']} | {x['in_body_anywhere']} | {','.join(x['calls'])}{extra} | {x['pass']} |")
    L += ["", "## 4. 오류(기록 입력 오류 호출 — 분모 · 오류 셈 밖 · W5-D14)", "", f"- 200 아님 {rep['errors']['n']}"]
    for k, v in rep["errors"]["summary"].items():
        L.append(f"  - {v} × {k}")
    L += ["", "## 5. 응답 크기 (ii) — 기본 응답 = 요청 sections 없는 호출 · §5-0-1 표", "",
          "| 도구 | 기본 n | 중앙 | p95 | 최대 | 상한 중앙 / p95 | 판정 | sections 있음 n / 중앙 / p95 / 최대 | case3 경로 n / 중앙 / p95 |", "|---|---|---|---|---|---|---|---|---|"]
    for t, v in rep["sizes"].items():
        d = v["default"]
        if t == "case3_path":
            L.append(f"| **case3 경로 합(159)** | {d.get('n', 0)} | {d.get('median', '–')} | {d.get('p95', '–')} | {d.get('max', '–')} | {v['cap_median']} / {v['cap_p95']} | {'PASS' if v['pass'] else 'FAIL'} | | |")
            continue
        w, c3s = v["with_sections"], v["case3_path"]
        L.append(f"| {t} | {d.get('n', 0)} | {d.get('median', '–')} | {d.get('p95', '–')} | {d.get('max', '–')} | {v['cap_median']} / {v['cap_p95']} | {'PASS' if v['pass'] else 'FAIL'} | {w.get('n', 0)} / {w.get('median', '–')} / {w.get('p95', '–')} / {w.get('max', '–')} | {c3s.get('n', 0)} / {c3s.get('median', '–')} / {c3s.get('p95', '–')} |")
    sc = rep["sizes_recorded_case3"]
    L += ["", f"기록 case3 hub.result_bytes(fail-triage2 case3_sizes 셈): n {sc['n']} · 중앙 {sc['median']} · p95 {sc['p95']}", ""]
    return "\n".join(L)


if __name__ == "__main__":
    raise SystemExit(main())
