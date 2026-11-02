#!/usr/bin/env python3
"""recheck — SPEC-005 §6-5 재인용 대조(WORK-005 WP-0 · WP-7).

판정 식은 `triage.py` 와 같은 식을 **여기에 다시 적는다**(triage.py 는 모듈 수준에서 파일을 읽고 쓰므로 import 하지 않음 · F-6):
정규화 = 소문자 · 공백 · 기호 제거 · 양방향 포함(골드 쪽 8자 이상) · 3-gram 80% = 부분 일치 · fact id 일치.

모드
  make-replay --base-url URL            runs.jsonl 의 호출 묶음(case2 도구 호출 전부 · case3 hub 경로)을 같은 입력으로 다시 불러 replay.json
  baseline   --export-old PATH          옛 export + replay.json(기록 응답)으로 320행 재분류(동일성) · B 닫힘(기대 0) · 크기 표 → recheck-report.baseline.{md,json}
  rerun      --export-new PATH (--base-url URL | --inprocess)
                                        실패 174문항 호출을 intent(행 jev_intent) 와 함께 다시 보내 B 205 행 닫힘 · 오류 · 크기 → recheck-report.{md,json}
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
OUT = E / "build-out" / "recheck"
CARD_TOOLS = ("recommend", "procedure_card", "pair_check", "check_conditions", "compare", "combos", "neighbors")  # T2~T8
ALL_TOOLS = ("recommend", "procedure_card", "pair_check", "check_conditions", "compare", "combos", "neighbors", "resolve", "vocab")
UNKNOWN = re.compile(r"정보 ?없음|정보가 없|자료에 없|확인되지 않|확인할 수 없|모르|알 수 없|안내하기 어렵|찾지 못")
CAUSES = [("「정보 없음」인데 원장엔 있음", lambda f, tr: bool(re.search(r"정보 ?없음|정보가 없|자료에 없|없다고|없습니다라고|확인되지 않|모른다", f["claim"]))),
          ("빠진 안전 정보", lambda f, tr: f["item"] == "safety"),
          ("이름 못 찾음", lambda f, tr: bool(tr.get("missing")) or bool(re.search(r"찾지 못|인식하지|이름", f["claim"]))),
          ("엉뚱한 시술", lambda f, tr: bool(re.search(r"엉뚱|다른 시술|관련 없|무관|잘못된 시술|해당하지 않는 시술", f["claim"]))),
          ("빠진 연결", lambda f, tr: f["item"] in ("accuracy", "on_topic", "candidates")),
          ("기타", lambda f, tr: True)]
# §6-5 「닫지 않는 행」 19 — (문항, 케이스, 골드 owner 접두) · 재인용률 분자 · 분모(186)에서 뺀다
NOT_CLOSABLE = [
    ("Q117", "case2", "combo_component:"), ("Q119", "case2", "combo_component:"), ("Q121", "case2", "combo_component:"),
    ("Q149", "case3", "combo_component:"), ("Q149", "case3", "combo_component:"), ("Q156", "case2", "combo_component:"),
    ("Q156", "case3", "combo_component:"), ("Q156", "case3", "combo_component:"), ("Q192", "case3", "combo_component:"),
    ("Q234", "case3", "combo_component:"),
    ("Q123", "case3", "concern:P8-2"), ("Q228", "case2", "product:auto-M15-1775401780659"), ("Q118", "case2", "treats:"),
    ("Q050", "case3", "combo:RC-CP-volume"), ("Q138", "case2", "combo:RC-CP-skin_texture"),
    ("Q068", "case2", "unit_procedure:U5-090"), ("Q070", "case2", "unit_procedure:U5-034"), ("Q082", "case3", "package:P6-09"),
    ("Q084", "case3", "product:M9-2-2"),
]
# 코디 10-31 ④ — 이번 범위 밖으로 옮긴 행 21(1-hop 다른 계열 원문 10 · 쌍 양끝 아님 6 · 기록 호출 오류 2 · 기타 3) · 사유를 표에
NOT_CLOSABLE_SCOPE = [
    ("Q004", "case3", "procedure_relation:E8-0129", "쌍 양끝 아님 — recommend 만 호출 · E8-0129 는 입력 쌍 아님"),
    ("Q026", "case3", "procedure_relation:E8-0026", "쌍 양끝 아님 — combos 만 호출"),
    ("Q097", "case3", "procedure_relation:E8-0028", "쌍 양끝 아님 — E8-0028 은 M11↔M5 단위 · 입력 M11 × M8"),
    ("Q114", "case3", "procedure_relation:none", "쌍 양끝 아님 — 엣지 없는 주장(procedure_relation:none)"),
    ("Q134", "case2", "procedure_relation:E8-0081", "쌍 양끝 아님 — E8-0081 은 M3↔M8 · 비교한 둘은 M8"),
    ("Q134", "case3", "procedure_relation:E8-0081", "쌍 양끝 아님 — E8-0081 은 M3↔M8 · 비교한 둘은 M8"),
    ("Q068", "case2", "family:M3", "1-hop 다른 계열 원문 — M4 카드에 M3 disclosure"),
    ("Q087", "case3", "family:M12", "1-hop 다른 계열 원문 — M11 비교에 M12 recovery"),
    ("Q106", "case3", "unit_procedure:U5-028", "1-hop 다른 노드 원문 — 비교 입력 밖 단위(U5-028) 타임라인"),
    ("Q124", "case3", "product:M8-4-1", "1-hop 다른 노드 원문 — 카드 시술이 안 쓰는 제품의 부작용"),
    ("Q165", "case3", "family:M15", "1-hop 다른 계열 원문 — M8 카드에 M15 타임라인"),
    ("Q176", "case3", "family:M15", "1-hop 다른 계열 원문 — M8 카드에 M15 side_effects"),
    ("Q176", "case3", "family:M15", "1-hop 다른 계열 원문 — M8 카드에 M15 disclosure"),
    ("Q191", "case3", "complication:CX-M11-01", "1-hop 다른 계열 원문 — 비교 입력 밖 M11 합병증"),
    ("Q222", "case3", "family:M11", "1-hop 다른 계열 원문 — 카드 계열 밖 M11 overview"),
    ("Q239", "case3", "complication:CX-M1-05", "1-hop 다른 노드 원문 — 합병증 상세(mechanism) · I-04 C6 는 이름 · id"),
    ("Q106", "case2", "unit_procedure:U5-028", "기록 호출 오류 — procedure_card 400(잘못된 sections 값)"),
    ("Q120", "case2", "check_condition:C-ISO", "기록 호출 오류 — check_conditions 404(없는 id)"),
    ("Q015", "case3", "unit_procedure:U5-091", "기타 — 비교 입력 밖 단위(U5-091)의 pih source"),
    ("Q113", "case3", "unit_procedure:U5-023", "기타 — 비교 입력 밖 단위(U5-023)의 pih fitzpatrick_note"),
    ("Q165", "case2", "unit_procedure:U5-034", "기타 — 카드 계열 밖 단위(U5-034 · M15) 타임라인"),
]
# §6-5 현 중앙값 표(case2 오류 제외) · v3 상한 = ×2.5(코디 10-31 ③ — recommend 18KB · pair 18KB · compare 20KB)
CURRENT_MEDIAN = {"recommend": 7262, "procedure_card": 17180, "pair_check": 7200, "check_conditions": 24206, "compare": 7997,
                  "combos": 9537, "neighbors": 6544, "resolve": 1059, "vocab": 6314}
CURRENT_MEDIAN_NO_SECTIONS = {"recommend": 6567, "procedure_card": 1447, "pair_check": 7151, "check_conditions": 115, "compare": 7268,
                              "combos": 9537, "neighbors": 5633, "resolve": 1059, "vocab": 5501}
LIMIT = {t: int(v * 2.5) for t, v in CURRENT_MEDIAN.items()}
LIMIT.update({"recommend": 18000, "pair_check": 18000, "compare": 20000})


# ── 판정 식(triage.py 와 같은 식) ────────────────────────────────────────────
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


# ── 호출 묶음(replay.py 와 같은 묶음) ─────────────────────────────────────────
def call_key(tool: str, args: Any) -> str:
    return hashlib.md5(json.dumps([tool, args], sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def rest_call(base: str, tool: str, args: dict[str, Any] | None, intent: str | None, client: Any = None) -> tuple[int, str]:
    """REST 호출 — hub_rest.call 과 같은 도구 → 경로. intent 는 GET 쿼리 · POST 본문에 더한다(없으면 안 더함)."""
    a = dict(args or {})
    if intent:
        a["intent"] = intent
    get_tools = {"procedure_card": lambda: ("GET", f"/procedures/{a.pop('id')}"), "check_conditions": lambda: ("GET", f"/procedures/{a.pop('id')}/checks"),
                 "neighbors": lambda: ("GET", f"/nodes/{a.pop('id')}/neighbors"), "combos": lambda: ("GET", "/combos"),
                 "resolve": lambda: ("GET", "/resolve"), "vocab": lambda: ("GET", "/vocab")}
    post_tools = {"recommend": "/recommend", "pair_check": "/pairs", "compare": "/compare"}
    try:
        if tool in post_tools:
            method, path, params, body = "POST", post_tools[tool], None, a
        elif tool in get_tools:
            if "id" not in a and tool in ("procedure_card", "check_conditions", "neighbors"):
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
    url = base.rstrip("/") + "/procedure-hub/gold" + path + (("?" + urllib.parse.urlencode({k: str(v) for k, v in params.items()})) if params else "")
    data = json.dumps(body).encode() if body is not None else None
    rq = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"} if data else {})
    try:
        with urllib.request.urlopen(rq, timeout=60) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as ex:
        return ex.code, ex.read().decode()
    except Exception as ex:  # noqa: BLE001
        return -1, str(ex)


def load_runs(path: Path) -> dict[str, dict[str, Any]]:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            d = json.loads(line)
            out[d["run_id"]] = d
    return out


def call_bundle(runs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """run_id → case2 도구 호출 목록 · case3 hub 경로 1번(도구 · 입력 · 기록 바이트)."""
    out: dict[str, Any] = {"case2": {}, "case3": {}}
    for rid, d in runs.items():
        out["case2"][rid] = [{"tool": tc["tool"], "input": tc.get("input"), "rec_bytes": tc.get("output_bytes"), "rec_err": tc.get("is_error")}
                             for tc in (d["cases"]["case2"].get("trace") or {}).get("tool_calls", [])]
        c3 = d["cases"]["case3"]
        tr3 = c3.get("trace") or {}
        hub = tr3.get("hub") or {}
        out["case3"][rid] = {"tool": hub.get("tool"), "input": hub.get("input"), "rec_bytes": hub.get("result_bytes"), "missing": hub.get("missing"),
                             "path": hub.get("path")} if hub else None
        # 오류 15(case3 I-09 계열 id → checks 400) — 예외가 trace.hub 갱신 전에 났으므로 case3.py plan_path(I-09) 규칙으로 입력을 되살린다
        m = re.search(r"GET /procedures/([^/]+)/checks", c3.get("error") or "")
        if m and not hub.get("tool"):
            jev = tr3.get("jev") or {}
            cond = (jev.get("slots", {}).get("check_condition") or {}).get("value")
            inp: dict[str, Any] = {"id": m.group(1), "conditions": [cond] if cond else None}
            if jev.get("sections"):
                inp["sections"] = list(jev["sections"])
            out["case3"][rid] = {"tool": "check_conditions", "input": inp, "rec_bytes": None, "missing": None, "path": "I-09", "reconstructed_from_error": c3.get("error")[:120]}
    return out


def make_replay(base: str, runs_path: Path, out: Path) -> dict[str, Any]:
    runs = load_runs(runs_path)
    bundle = call_bundle(runs)
    calls: dict[str, dict[str, Any]] = {}
    for rid in sorted(runs):
        for c in bundle["case2"][rid]:
            k = call_key(c["tool"], c["input"])
            if k not in calls:
                st, txt = rest_call(base, c["tool"], c["input"], None)
                calls[k] = {"tool": c["tool"], "input": c["input"], "status": st, "text": txt}
            c["key"] = k
        h = bundle["case3"][rid]
        if h and h.get("tool"):
            k = call_key(h["tool"], h["input"])
            if k not in calls:
                st, txt = rest_call(base, h["tool"], h["input"], None)
                calls[k] = {"tool": h["tool"], "input": h["input"], "status": st, "text": txt}
            h["key"] = k
    rep = {"base_url": base, "build_hash": _build_hash_of(calls), "calls": calls, "case2": bundle["case2"], "case3": bundle["case3"]}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    return rep


def _build_hash_of(calls: dict[str, dict[str, Any]]) -> str | None:
    for c in calls.values():
        if c["status"] == 200:
            try:
                return json.loads(c["text"]).get("build", {}).get("build_hash")
            except ValueError:
                continue
    return None


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


class HubContext:
    """한 문항 · 한 케이스의 허브 응답 묶음 — 분류와 닫힘 판정의 재료."""

    def __init__(self, gold: Gold, calls: list[dict[str, Any]], jev: dict[str, Any] | None, hub_trace: dict[str, Any]) -> None:
        self.tools_called = [c["tool"] for c in calls]
        self.hub_text = ""
        self.returned: set[str] = set()
        self.hub_facts: set[str] = set()
        self.more_cards: set[str] = set()
        self.req_sections: dict[str, set[str]] = collections.defaultdict(set)
        self.resolve_cands: set[str] = set()
        self.pair_procs: set[str] = set()
        self.all_req_sections: set[str] = set()
        self.errors: list[dict[str, Any]] = []
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


def in_hub(q: str, hits: list[tuple[str, str, dict[str, Any]]], ctx: HubContext, broad: bool = False) -> tuple[bool, str | None]:
    """triage 와 같은 식(인용 포함 · facts[].id · 골드 문장 포함). broad(§6-5 닫힘 판정)는 동봉 · 본문 어디든 fact id(따옴표 안)도 센다."""
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
                return True, "fact id 만(동봉 · claims id) " + fid
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
    """fail-triage.json 행 하나 → cls · sub(+ 판정 재료). triage.py 와 같은 규칙."""
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


# ── 묶음 ①~⑧(fail-triage report 와 같은 식) ───────────────────────────────────
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


# ── 크기 셈(§6-5 F-5 규칙) ───────────────────────────────────────────────────
def current_sizes(runs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    c2: dict[str, list[int]] = collections.defaultdict(list)
    c2n: dict[str, list[int]] = collections.defaultdict(list)
    c3: dict[str, list[int]] = collections.defaultdict(list)
    for d in runs.values():
        for tc in (d["cases"]["case2"].get("trace") or {}).get("tool_calls", []):
            if tc.get("output_bytes") is None:
                continue
            if not (tc.get("input") or {}).get("sections"):  # 「sections 없음」 열은 오류 응답도 셈(§6-5 표 check_conditions 10/115)
                c2n[tc["tool"]].append(tc["output_bytes"])
            if tc.get("is_error"):
                continue
            c2[tc["tool"]].append(tc["output_bytes"])
        hub = (d["cases"]["case3"].get("trace") or {}).get("hub") or {}
        if hub.get("tool") and hub.get("result_bytes") is not None:
            c3[hub["tool"]].append(hub["result_bytes"])
    med = lambda xs: int(statistics.median(xs)) if xs else None  # noqa: E731  (§6-5 표는 소수점 버림)
    return {"case2_no_error": {t: {"n": len(v), "median": med(v)} for t, v in sorted(c2.items())}, "case2_no_error_total": sum(len(v) for v in c2.values()),
            "case2_no_sections": {t: {"n": len(v), "median": med(v)} for t, v in sorted(c2n.items())},
            "case3": {t: {"n": len(v), "median": med(v)} for t, v in sorted(c3.items())}, "case3_total": sum(len(v) for v in c3.values())}


def size_table(calls: list[dict[str, Any]]) -> dict[str, Any]:
    """재실행 호출의 도구별 바이트 — 기본 응답(요청 sections 없음) · sections 있는 호출 따로 · 중앙 · p95 · 최대."""
    base: dict[str, list[int]] = collections.defaultdict(list)
    withs: dict[str, list[int]] = collections.defaultdict(list)
    for c in calls:
        if c["status"] != 200:
            continue
        n = len(c["text"].encode("utf-8"))
        (withs if (c.get("input") or {}).get("sections") else base)[c["tool"]].append(n)

    def stat(xs: list[int]) -> dict[str, Any]:
        if not xs:
            return {"n": 0}
        s = sorted(xs)
        return {"n": len(s), "median": int(statistics.median(s)), "p95": s[min(len(s) - 1, int(round(0.95 * (len(s) - 1))))], "max": s[-1]}
    out = {}
    for t in ALL_TOOLS:
        b = stat(base[t])
        lim = LIMIT.get(t)
        out[t] = {"default": b, "with_sections": stat(withs[t]), "limit": lim, "current_median": CURRENT_MEDIAN.get(t),
                  "current_median_no_sections": CURRENT_MEDIAN_NO_SECTIONS.get(t),
                  "pass": (b.get("median") is None) or (lim is None) or (b["median"] <= lim)}
    return out


# ── 실행 ──────────────────────────────────────────────────────────────────────
def run_rows(gold: Gold, raw: Raw, rows: list[dict[str, Any]], runs: dict[str, dict[str, Any]], responses: dict[str, dict[str, Any]],
             per_case_calls: dict[tuple[str, str], list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """행마다 분류 — responses 는 (run_id, case) → HubContext 재료."""
    out = []
    for row in rows:
        rid = next(r for r, d in runs.items() if d.get("question_no") == row["question_no"]) if "run_id" not in row else row["run_id"]
        d = runs[rid]
        case = row["case"]
        cs = d["cases"][case]
        tr = cs.get("trace") or {}
        jev = tr.get("jev") if case == "case3" else None
        hub_trace = (tr.get("hub") or {}) if case == "case3" else {}
        ctx = HubContext(gold, per_case_calls[(rid, case)], jev, hub_trace)
        res = classify(gold, raw, row, ctx, case)
        out.append({**{k: row[k] for k in ("question_no", "case", "item", "jev_intent", "evidence", "cls", "sub", "tools_called")}, "run_id": rid,
                    "new": res, "errors": ctx.errors, "returned_nodes": sorted(ctx.returned)[:40]})
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=("make-replay", "baseline", "rerun"))
    p.add_argument("--base-url", default="http://127.0.0.1:18005")
    p.add_argument("--inprocess", action="store_true", help="rerun 을 포트 없이 같은 앱(TestClient · 발행본 DB 적재)으로")
    p.add_argument("--fail-triage", type=Path, default=E / "build-out" / "fail-triage.json")
    p.add_argument("--runs", type=Path, default=E / "runs" / "runs.jsonl")
    p.add_argument("--replay", type=Path, default=OUT / "replay.json")
    p.add_argument("--export-old", type=Path, default=OUT / "gold-export.e9d30ace08c65bb8.json")
    p.add_argument("--export-new", type=Path, default=BACKEND / "build-out" / "gold-export.json")
    p.add_argument("--out-prefix", type=Path, default=None, help="출력 파일 머리(기본 recheck-report · baseline 은 recheck-report.baseline)")
    p.add_argument("--save-responses", type=Path, default=None, help="rerun 응답 전부를 json 으로(결정론 대조용)")
    a = p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.mode == "make-replay":
        rep = make_replay(a.base_url, a.runs, a.replay)
        ok = sum(1 for c in rep["calls"].values() if c["status"] == 200)
        print(f"replay — unique calls {len(rep['calls'])} · 200 {ok} · build {rep['build_hash']} → {a.replay}")
        return 0
    runs = load_runs(a.runs)
    ft = json.loads(a.fail_triage.read_text(encoding="utf-8"))
    rows = ft["rows"]
    raw = Raw(RAW)
    replay = json.loads(a.replay.read_text(encoding="utf-8"))
    qrid = {d["question_no"]: rid for rid, d in runs.items()}
    for r in rows:
        r["run_id"] = qrid[r["question_no"]]
    prefix = a.out_prefix or (OUT / ("recheck-report.baseline" if a.mode == "baseline" else "recheck-report"))
    meta: dict[str, Any] = {"mode": a.mode, "ran_at": datetime.now(UTC).isoformat(), "export_old": {"path": str(a.export_old)},
                            "replay": {"path": str(a.replay), "build_hash": replay.get("build_hash"), "unique_calls": len(replay["calls"])},
                            "runs": str(a.runs), "fail_triage_rows": len(rows), "judge": "triage.py 와 같은 식 — norm(소문자 · 공백 · 기호 제거) · 양방향 포함(골드 쪽 8자 이상) · 3-gram 0.8 부분 · fact id 일치 · 같은 식을 이 파일에 적음(import 안 함)"}
    # 기록 응답으로 묶음 재구성
    rec_calls: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for rid in runs:
        rec_calls[(rid, "case2")] = [{**replay["calls"][c["key"]]} for c in replay["case2"].get(rid, [])]
        h = replay["case3"].get(rid)
        rec_calls[(rid, "case3")] = [{**replay["calls"][h["key"]]}] if h and h.get("key") else []
    gold_old = Gold(a.export_old)
    meta["export_old"]["build_hash"] = gold_old.hash
    # 동일성: 옛 export + 기록 응답으로 320행 재분류
    ident = run_rows(gold_old, raw, rows, runs, {}, rec_calls)
    same = sum(1 for x in ident if x["new"]["cls"] == x["cls"] and x["new"]["sub"] == x["sub"])
    diff = [{"question_no": x["question_no"], "case": x["case"], "old": [x["cls"], x["sub"]], "new": [x["new"]["cls"], x["new"]["sub"]]}
            for x in ident if not (x["new"]["cls"] == x["cls"] and x["new"]["sub"] == x["sub"])]
    identity = {"rows": len(ident), "same": same, "diff": diff}
    sizes_current = current_sizes(runs)
    B = [r for r in rows if r["cls"] == "B"]
    den = [r for r in B if set(r["tools_called"]) & set(CARD_TOOLS)]
    no_call = [r for r in B if not r["tools_called"]]
    only_resolve = [r for r in B if r["tools_called"] and not (set(r["tools_called"]) & set(CARD_TOOLS))]
    # 닫지 않는 행 19 — (문항 · 케이스 · owner 접두) 로 행 고정
    nc_rows: list[dict[str, Any]] = []
    nc_reason: dict[int, str] = {}
    pool = list(den)
    for q, c, pre in NOT_CLOSABLE:
        hit = next((r for r in pool if r["question_no"] == q and r["case"] == c and str(r.get("gold_owner") or "").startswith(pre) and r not in nc_rows), None)
        if hit:
            nc_rows.append(hit)
            nc_reason[id(hit)] = "§6-5 표"
    for q, c, pre, why in NOT_CLOSABLE_SCOPE:  # 코디 10-31 ④(사용자 재정정으로 적용)
        hit = next((r for r in pool if r["question_no"] == q and r["case"] == c and str(r.get("gold_owner") or "").startswith(pre) and r not in nc_rows), None)
        if hit:
            nc_rows.append(hit)
            nc_reason[id(hit)] = why
    nc_ids = {id(r) for r in nc_rows}
    reach_rows = [r for r in den if id(r) not in nc_ids]
    if a.mode == "baseline":
        gold_new, calls_new = gold_old, rec_calls
        meta["export_new"] = {"path": str(a.export_old), "build_hash": gold_old.hash, "note": "baseline — 옛 export · 기록 응답"}
        all_calls = list(replay["calls"].values())
    else:
        gold_new = Gold(a.export_new)
        meta["export_new"] = {"path": str(a.export_new), "build_hash": gold_new.hash}
        client = None
        if a.inprocess:
            sys.path.insert(0, str(BACKEND))
            sys.path.insert(0, str(BACKEND / "scripts"))
            from _gold_client import GoldClient  # type: ignore  # noqa: PLC0415
            client = GoldClient.inprocess().http
            meta["target"] = "inprocess"
        else:
            meta["target"] = a.base_url
        failed_rids = sorted({r["run_id"] for r in rows} | {rid for rid, h in replay["case3"].items() if h and h.get("reconstructed_from_error")})  # + 오류 15 문항
        intent_of = {(r["run_id"], r["case"]): (r["jev_intent"] if r["jev_intent"] and r["jev_intent"] != "?" else None) for r in rows}
        cache: dict[str, dict[str, Any]] = {}
        calls_new = {}
        all_calls = []
        for rid in failed_rids:
            for case in ("case2", "case3"):
                intent = intent_of.get((rid, case))
                calls = []
                for c in rec_calls[(rid, case)]:
                    k = call_key(c["tool"], c["input"]) + ":" + (intent or "")
                    if k not in cache:
                        st, txt = rest_call(a.base_url, c["tool"], c["input"], intent, client)
                        cache[k] = {"tool": c["tool"], "input": c["input"], "intent": intent, "status": st, "text": txt}
                        all_calls.append(cache[k])
                    calls.append(cache[k])
                calls_new[(rid, case)] = calls
        new_hash = _build_hash_of({k: v for k, v in cache.items()})
        meta["target_build_hash"] = new_hash
        if a.save_responses:
            a.save_responses.write_text(json.dumps([{k: v for k, v in c.items()} for c in all_calls], ensure_ascii=False, sort_keys=True), encoding="utf-8")
    # B 닫힘 판정 — 새 export 로 gold_match 갱신 뒤 재실행 응답 대조
    results = []
    for r in den:
        rid, case = r["run_id"], r["case"]
        d = runs[rid]
        tr = d["cases"][case].get("trace") or {}
        ctx = HubContext(gold_new, calls_new[(rid, case)], tr.get("jev") if case == "case3" else None, (tr.get("hub") or {}) if case == "case3" else {})
        q = norm(r["evidence"]["quote"])
        tier, hits = gold_new.gold_match(q)
        closed, how = (in_hub(q, hits, ctx, broad=True) if tier == "exact" else (False, None))
        strict = bool(closed and how and not how.startswith("fact id 만"))
        results.append({"question_no": r["question_no"], "case": r["case"], "item": r["item"], "intent": r["jev_intent"], "sub": r["sub"], "group": coarse(r["sub"]),
                        "gold_owner": r.get("gold_owner"), "gold_section": r.get("gold_section"), "path": r["evidence"]["path"],
                        "not_closable": id(r) in nc_ids, "old_gold_hits": [h.get("fact_id") or h.get("node_id") or h.get("edge_id") for h in (r.get("gold_hits") or [])][:6],
                        "new_gold_tier": tier, "new_gold_hits": [ref.get("fact_id") or ref.get("node_id") or ref.get("edge_id") for _, _, ref in hits[:6]],
                        "closed": closed, "closed_with_text": strict, "how": how, "calls": [{"tool": c["tool"], "status": c["status"], "intent": c.get("intent")} for c in calls_new[(rid, case)]],
                        "errors": ctx.errors})
    closed_reach = sum(1 for x in results if x["closed"] and not x["not_closable"])
    closed_all = sum(1 for x in results if x["closed"])
    closed_nc = sum(1 for x in results if x["closed"] and x["not_closable"])
    strict_reach = sum(1 for x in results if x["closed_with_text"] and not x["not_closable"])
    n_reach = len(reach_rows)
    rate = {"reach": {"n": n_reach, "closed": closed_reach, "rate": round(closed_reach / n_reach, 4) if n_reach else None, "target": 0.9, "pass": n_reach > 0 and closed_reach / n_reach >= 0.9},
            "reach_with_text": {"n": n_reach, "closed": strict_reach, "rate": round(strict_reach / n_reach, 4) if n_reach else None, "note": "원문(facts[] · 인용 · 골드 문장)으로 닫힌 행만 — fact id 만 실린 행 제외(보고용 · 더 엄격)"},
            "den205": {"n": len(den), "closed": closed_all, "rate": round(closed_all / len(den), 4) if den else None},
            "b239": {"n": len(B), "closed": closed_all, "rate": round(closed_all / len(B), 4) if B else None},
            "not_closable": {"n": len(nc_rows), "closed": closed_nc, "spec19": sum(1 for r in nc_rows if nc_reason[id(r)] == "§6-5 표"), "scope_out": sum(1 for r in nc_rows if nc_reason[id(r)] != "§6-5 표"),
                             "rows": [{"question_no": r["question_no"], "case": r["case"], "gold_owner": r.get("gold_owner"), "why": nc_reason[id(r)]} for r in nc_rows]},
            "outside": {"no_hub_call": len(no_call), "resolve_vocab_only": len(only_resolve)}}
    by_group = collections.OrderedDict()
    for x in sorted(results, key=lambda x: x["group"]):
        g_ = by_group.setdefault(x["group"], {"n": 0, "closed": 0, "not_closable": 0})
        g_["n"] += 1
        g_["closed"] += int(x["closed"])
        g_["not_closable"] += int(x["not_closable"])
    by_intent = collections.OrderedDict()
    for x in sorted(results, key=lambda x: x["intent"] or "?"):
        g_ = by_intent.setdefault(x["intent"] or "?", {"n": 0, "closed": 0, "not_closable": 0})
        g_["n"] += 1
        g_["closed"] += int(x["closed"])
        g_["not_closable"] += int(x["not_closable"])
    checks15 = [c for c in all_calls if c["tool"] == "check_conditions" and str((c.get("input") or {}).get("id", "")).startswith("family:")]
    c3_fam = []
    for rid, h in replay["case3"].items():
        if h and h.get("tool") == "check_conditions" and str((h.get("input") or {}).get("id", "")).startswith("family:"):
            k = h.get("key")
            c3_fam.append({"question_no": runs[rid].get("question_no"), "id": h["input"]["id"],
                           "status": next((c["status"] for c in all_calls if c["tool"] == "check_conditions" and c["input"] == h["input"]), (replay["calls"][k]["status"] if k else None))})
    errors = [c for c in all_calls if c["status"] != 200]
    err_summary = collections.Counter(f"{c['tool']} {c['status']} {c['text'][:80]}" for c in errors)
    sizes = size_table(all_calls)
    report = {"meta": meta, "identity": identity, "rate": rate, "by_group": by_group, "by_intent": by_intent,
              "checks_family": {"n": len(checks15), "ok": sum(1 for c in checks15 if c["status"] == 200), "ids": sorted({c["input"]["id"] for c in checks15}),
                                "case3_15": {"n": len(c3_fam), "ok": sum(1 for x in c3_fam if x["status"] == 200), "rows": sorted(c3_fam, key=lambda x: x["question_no"] or "")}},
              "errors": {"n": len(errors), "summary": dict(err_summary.most_common())}, "sizes": sizes, "sizes_current_rule": sizes_current,
              "rows": results, "not_closed_rows": [x for x in results if not x["closed"]]}
    Path(str(prefix) + ".json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    Path(str(prefix) + ".md").write_text(render(report), encoding="utf-8")
    print(f"{a.mode} — identity {same}/{len(ident)} · B 닫힘 {closed_reach}/{n_reach}(닿는 행) · {closed_all}/{len(den)}(205) · checks family {report['checks_family']['ok']}/{report['checks_family']['n']} · 오류 {len(errors)} → {prefix}.md")
    return 0


def render(rep: dict[str, Any]) -> str:
    m, r = rep["meta"], rep["rate"]
    L = [f"# recheck — {m['mode']} · B 재인용 대조(SPEC-005 §6-5)", "",
         f"옛 export `{m['export_old']['build_hash']}` · 새 export `{m['export_new']['build_hash']}` · 대상 {m.get('target', '기록 응답(replay)')} · 대상 빌드 {m.get('target_build_hash', m['replay'].get('build_hash'))} · replay 유일 호출 {m['replay']['unique_calls']}",
         f"판정: {m['judge']}", "",
         "## 1. 판정 동일성(옛 export + 기록 응답 → fail-triage 320행 재분류)", "",
         f"- cls · sub 같음 **{rep['identity']['same']}/{rep['identity']['rows']}**" + ("" if not rep["identity"]["diff"] else " · 다른 행: " + json.dumps(rep["identity"]["diff"][:10], ensure_ascii=False)), "",
         "## 2. B 재인용률", "",
         "| 기준 | 분모 | 닫힘 | 비율 | 목표 | 판정 |", "|---|---|---|---|---|---|",
         f"| 조항이 닿는 행 | {r['reach']['n']} | {r['reach']['closed']} | {r['reach']['rate']} | ≥ 0.9(§6-5 · V-7 은 측정값으로 보고) | {'PASS' if r['reach']['pass'] else 'FAIL'} |",
         f"| (보고) 닿는 행 중 원문으로 닫힘(fact id 만 제외) | {r['reach_with_text']['n']} | {r['reach_with_text']['closed']} | {r['reach_with_text']['rate']} | 보고 | — |",
         f"| 분모 205(카드 도구 호출 있던 B) | {r['den205']['n']} | {r['den205']['closed']} | {r['den205']['rate']} | 보고 | — |",
         f"| B 239 | {r['b239']['n']} | {r['b239']['closed']} | {r['b239']['rate']} | 보고 | — |",
         f"| 닫지 않는 행(§6-5 표 {r['not_closable']['spec19']} + 코디 10-31 범위 밖 {r['not_closable']['scope_out']}) | {r['not_closable']['n']} | {r['not_closable']['closed']} | — | 분자 · 분모 밖 | — |",
         f"| 분모 밖 | 허브 안 부름 {r['outside']['no_hub_call']} · resolve · vocab 만 {r['outside']['resolve_vocab_only']} | | | | |", "",
         "### 묶음 ①~⑧", "", "| 묶음 | 행 | 닫힘 | 닫지 않는 행 |", "|---|---|---|---|"]
    for k, v in rep["by_group"].items():
        L.append(f"| {k} | {v['n']} | {v['closed']} | {v['not_closable']} |")
    L += ["", "### 의도별(행 jev_intent)", "", "| 의도 | 행 | 닫힘 | 닫지 않는 행 |", "|---|---|---|---|"]
    for k, v in rep["by_intent"].items():
        L.append(f"| {k} | {v['n']} | {v['closed']} | {v['not_closable']} |")
    L += ["", f"### 닫지 않는 행 {r['not_closable']['n']}(§6-5 표 19 + 코디 10-31 범위 밖 {r['not_closable']['scope_out']})", "", "| 문항 | 케이스 | 골드 owner | 사유 |", "|---|---|---|---|"]
    for x in r["not_closable"]["rows"]:
        L.append(f"| {x['question_no']} | {x['case']} | {x['gold_owner']} | {x['why']} |")
    L += ["", "### 닫히지 않은 행 전부(사유)", "", "| 문항 | 케이스 | 의도 | 묶음 | 빠진 칸 | 골드 owner#section | 새 gold tier | 호출 | 닫지 않는 행 |", "|---|---|---|---|---|---|---|---|---|"]
    for x in rep["not_closed_rows"]:
        L.append(f"| {x['question_no']} | {x['case']} | {x['intent']} | {x['group'][:1]} | {x['sub'][:40]} | {x['gold_owner']}{('#' + x['gold_section']) if x.get('gold_section') else ''} | {x['new_gold_tier']} | {','.join(dict.fromkeys(c['tool'] + ('' if c['status'] == 200 else f'({c['status']})') for c in x['calls']))} | {'○' if x['not_closable'] else ''} |")
    c = rep["checks_family"]
    c3 = c["case3_15"]
    L += ["", "## 3. 오류", "", f"- case3 경로 `GET /procedures/family:M*/checks` 15건: {c3['ok']}/{c3['n']} 200 — " + ", ".join(f"{x['question_no']}({x['id'].split(':')[1]} {x['status']})" for x in c3["rows"]),
          f"- 호출 묶음 전체의 family checks {c['ok']}/{c['n']} 200 ({', '.join(c['ids'])})", f"- 재실행 오류(200 아님) {rep['errors']['n']}"]
    for k, v in rep["errors"]["summary"].items():
        L.append(f"  - {v} × {k}")
    L += ["", "## 4. 응답 크기(재실행 · 바이트) — 기본 응답 = 요청 sections 없는 호출", "",
          "| 도구 | 기본 n | 중앙 | p95 | 최대 | 상한(현 ×2.5 · 코디 10-31 ③) | 판정 | sections 있는 호출 n / 중앙 | 현 중앙(§6-5) | 현 sections 없음 |", "|---|---|---|---|---|---|---|---|---|---|"]
    for t, v in rep["sizes"].items():
        d, w = v["default"], v["with_sections"]
        L.append(f"| {t} | {d.get('n', 0)} | {d.get('median', '–')} | {d.get('p95', '–')} | {d.get('max', '–')} | {v['limit']} | {'PASS' if v['pass'] else 'FAIL'} | {w.get('n', 0)} / {w.get('median', '–')} | {v['current_median']} | {v['current_median_no_sections']} |")
    sc = rep["sizes_current_rule"]
    L += ["", f"현 중앙값 재계산(runs.jsonl · F-5 규칙): case2 오류 제외 {sc['case2_no_error_total']} · case3 {sc['case3_total']} — " +
          " · ".join(f"{t} {v['n']}/{v['median']}" for t, v in sc["case2_no_error"].items()), ""]
    return "\n".join(L)


if __name__ == "__main__":
    raise SystemExit(main())
