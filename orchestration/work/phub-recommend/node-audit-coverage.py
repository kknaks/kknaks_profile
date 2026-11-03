"""원장 21 파일 모든 잎 값 → 골드(567677ed) 커버리지 전수 — 읽기 전용 · 결정론.

판정(앞이 이김): ① 골드 fact 원문 ② 골드 노드 · 엣지 · globals 속성(fact 아님) ③ 실버 정본 11 파일에만 ④ 실버에도 없음.
정규화 = triage 식(소문자 · 공백 · 기호 제거). 8자 이상 = 포함(원장 값 ⊂ 골드 문자열) → 없으면 조각 합(골드 문자열 ⊂ 원장 값 · 덮은 글자 ≥ 80%)
→ 없으면 3-gram ≥ 0.8(한 문자열). 8자 미만 = 같음 또는 골드 문자열(길이 ≤ 2×+4) 안 포함(triage 짧은 인용 규칙).
경로 = 배열 인덱스 → [] · 코드 키 → {code} · products 분류 키 → {category}(source-map 칸 정의와 같음 — 517 칸 전부 일치 확인).
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = Path("/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26")
GOLD = Path("/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/build-out/gold-export.json")
SILVER = ["step1-products.json", "step2-families.json", "step3-sites.json", "step3-lexicon.json", "step4-techniques.json",
          "step5-units.json", "step6-packages.json", "step7-concerns.json", "step8-relations.json", "step9-explanations.json",
          "semantic.json"]
RARE = 4000  # 이보다 흔한 3-gram 은 후보 찾기에서 뺌(검증은 전체 gram)


def norm(s) -> str:
    return re.sub(r"[\s\W_]+", "", str(s).lower())


def grams(s: str, n: int = 3) -> set[str]:
    return {s[i:i + n] for i in range(len(s) - n + 1)}


def fold(fn: str, p: str) -> str:
    segs = p.split(".")
    if fn == "products.json" and segs and segs[0] not in ("version", "updated", "description"):
        segs[0] = "{category}"
    return ".".join(re.sub(r"^[A-Z]{1,3}\d+(\[\])?$", lambda m: "{code}" + (m.group(1) or ""), s) for s in segs)


def raw_leaves(o, p=""):
    """(경로, 값) — 스칼라 배열은 경로 그대로, 객체 배열은 []."""
    if isinstance(o, dict):
        for k, v in o.items():
            yield from raw_leaves(v, f"{p}.{k}" if p else k)
    elif isinstance(o, list):
        for x in o:
            yield from raw_leaves(x, p + "[]" if isinstance(x, (dict, list)) else p)
    else:
        yield p, o


def scalars(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from scalars(v, f"{p}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from scalars(v, f"{p}[{i}]")
    elif isinstance(o, (str, int, float)) and not isinstance(o, bool):
        yield p, o


class Tier:
    def __init__(self, name: str, entries: list[tuple[str, str]]):
        """entries = (정규화 문자열, 위치 설명)."""
        self.name = name
        seen: dict[str, str] = {}
        for ns, where in entries:
            if ns and ns not in seen:
                seen[ns] = where
        self.items = sorted(seen.items())
        self.exact = dict(self.items)
        self.big = "\x00".join(ns for ns, _ in self.items)
        self.starts = []
        pos = 0
        for ns, _ in self.items:
            self.starts.append(pos)
            pos += len(ns) + 1
        self.short_sub: dict[str, int] = {}
        for ns, _ in self.items:
            if len(ns) <= 19:
                for i in range(len(ns)):
                    for j in range(i + 1, len(ns) + 1):
                        s = ns[i:j]
                        if self.short_sub.get(s, 99) > len(ns):
                            self.short_sub[s] = len(ns)
        post = collections.defaultdict(list)
        self.g = []
        for idx, (ns, _) in enumerate(self.items):
            gs = grams(ns) if len(ns) >= 8 else set()
            self.g.append(gs)
            for gr in gs:
                post[gr].append(idx)
        self.post = {k: v for k, v in post.items() if len(v) <= RARE}
        self.rare_n = [sum(1 for gr in gs if gr in self.post) for gs in self.g]

    def where_of(self, pos: int) -> str:
        import bisect
        i = bisect.bisect_right(self.starts, pos) - 1
        return self.items[i][1]

    def match(self, q: str) -> tuple[str | None, str]:
        if not q:
            return None, ""
        if q in self.exact:
            return "같음", self.exact[q]
        if len(q) < 8:
            m = self.short_sub.get(q)
            if m is not None and m <= 2 * len(q) + 4:
                return "짧은 포함", ""
            return None, ""
        p = self.big.find(q)
        if p >= 0:
            return "포함", self.where_of(p)
        gq = grams(q)
        cnt: collections.Counter = collections.Counter()
        for gr in gq:
            for i in self.post.get(gr, ()):
                cnt[i] += 1
        # 조각 합: 골드 문자열(≥8)이 원장 값 안에 통째로
        cover = [False] * len(q)
        best_piece = ""
        for i, c in sorted(cnt.items()):
            ns = self.items[i][0]
            if len(ns) >= 8 and c >= self.rare_n[i] and len(ns) <= len(q):
                k = q.find(ns)
                while k >= 0:
                    for t in range(k, k + len(ns)):
                        cover[t] = True
                    best_piece = best_piece or self.items[i][1]
                    k = q.find(ns, k + 1)
        if sum(cover) >= 0.8 * len(q):
            return "조각 합", best_piece
        if len(q) >= 12:
            best, bi = 0.0, -1
            for i, c in sorted(cnt.items()):
                if c >= 0.5 * len(gq):
                    r = len(gq & self.g[i]) / len(gq)
                    if r > best:
                        best, bi = r, i
            if best >= 0.8:
                return "3gram", self.items[bi][1]
        return None, ""


def build_tiers():
    g = json.loads(GOLD.read_text(encoding="utf-8"))
    t1, t2, t2m, t3 = [], [], [], []
    for f in g["facts"]:
        t1.append((norm(f["text"]), f"fact:{f['section']}:{f['owner_id'].split(':')[0]}"))
        for p, s in scalars(f["source"].get("meta") or {}, "meta"):
            t2m.append((norm(s), f"fact_meta:{f['section']}{re.sub(r'\[[0-9]+\]', '[]', p)}"))
    for n in g["nodes"]:
        t2.append((norm(n["name"]), f"node_name:{n['kind']}"))
        for p, s in scalars(n.get("attrs") or {}, "attrs"):
            t2.append((norm(s), f"node_attr:{n['kind']}{re.sub(r'\[[0-9]+\]', '[]', p)}"))
    for e in g["edges"]:
        for p, s in scalars(e.get("attrs") or {}, "attrs"):
            t2.append((norm(s), f"edge_attr:{e['kind']}{re.sub(r'\[[0-9]+\]', '[]', p)}"))
        for p, s in scalars(e.get("resolved") or {}, "resolved"):
            t2.append((norm(s), f"edge_resolved:{e['kind']}{re.sub(r'\[[0-9]+\]', '[]', p)}"))
        for p, s in scalars(e.get("evidence") or {}, "evidence"):
            t2.append((norm(s), f"edge_evidence:{e['kind']}{re.sub(r'\[[0-9]+\]', '[]', p)}"))
    for x in g["globals"]:
        for p, s in scalars(x.get("payload") or {}, "payload"):
            t2.append((norm(s), f"global:{x['kind']}"))
    for fn in SILVER:
        for p, s in scalars(json.loads((HERE / fn).read_text(encoding="utf-8"))):
            t3.append((norm(s), f"{fn}{re.sub(r'\[[0-9]+\]', '[]', p)}"))
    return g["build"]["build_hash"], [Tier("①", t1), Tier("②", t2), Tier("②m", t2m), Tier("③", t3)]


def main() -> None:
    sm = json.loads((HERE / "source-map.json").read_text(encoding="utf-8"))
    smf = {(f["file"], f["path"]): f for f in sm["fields"]}
    bundles = {b["id"]: b for b in sm["bundles"]}
    gh, tiers = build_tiers()
    rows: dict[tuple[str, str], dict] = {}
    cache: dict[str, tuple[str, str, str]] = {}
    for fn in sorted(os.listdir(RAW)):
        d = json.loads((RAW / fn).read_text(encoding="utf-8"))
        for p, v in raw_leaves(d):
            key = (fn, fold(fn, p))
            r = rows.setdefault(key, {"file": fn, "path": key[1], "leaves": 0, "구조값": 0, "빈 값": 0,
                                      "①": 0, "②": 0, "②m": 0, "③": 0, "④": 0, "how": collections.Counter(),
                                      "where": collections.Counter(), "ex": {},
                                      "long": collections.Counter(), "short": collections.Counter()})
            r["leaves"] += 1
            if v is None or isinstance(v, bool):
                r["구조값"] += 1
                continue
            q = norm(v)
            if not q:
                r["빈 값"] += 1
                continue
            if q not in cache:
                res = ("④", "", "")
                for t in tiers:
                    how, where = t.match(q)
                    if how:
                        res = (t.name, how, where)
                        break
                cache[q] = res
            tier, how, where = cache[q]
            if tier == "②m":
                r["②m"] += 1
                tier = "②"
            r[tier] += 1
            r["long" if len(q) >= 8 else "short"][tier] += 1
            if how:
                r["how"][f"{tier}{how}"] += 1
            if where:
                r["where"][f"{tier} {where}"] += 1
            r["ex"].setdefault(tier, str(v)[:120])
    out_rows = []
    for (fn, path), r in sorted(rows.items()):
        f = smf.get((fn, path)) or {}
        kinds = {x.get("kind") for x in f.get("destinations", [])}
        klass = "메타 · 보관" if kinds and kinds <= {"리니지", "버림", "원문 보관"} else "내용"
        n = r["leaves"] - r["구조값"] - r["빈 값"]
        out_rows.append({
            "file": fn, "path": path, "class": klass, "leaves": r["leaves"], "judged": n, "구조값": r["구조값"], "빈 값": r["빈 값"],
            "①": r["①"], "②": r["②"], "②m(fact 부가칸)": r["②m"], "③": r["③"], "④": r["④"],
            "long": {k: r["long"][k] for k in ("①", "②", "③", "④")}, "short": {k: r["short"][k] for k in ("①", "②", "③", "④")},
            "rate": {k: round(r[k] / n, 3) if n else None for k in ("①", "②", "③", "④")},
            "how": dict(sorted(r["how"].items())), "where_top": [w for w, _ in sorted(r["where"].items(), key=lambda x: (-x[1], x[0]))[:3]],
            "examples": dict(sorted(r["ex"].items())),
            "source_map": {"what": f.get("what"), "status": f.get("status"), "bundle": f.get("bundle"),
                           "destinations": [{k: x.get(k) for k in ("stage", "kind", "target", "status", "basis")} for x in f.get("destinations", [])],
                           "recommend": f.get("recommend") or (bundles.get(f.get("bundle")) or {}).get("recommend")},
        })
    tot = collections.Counter()
    by_file = collections.defaultdict(collections.Counter)
    for r in out_rows:
        for k in ("leaves", "judged", "구조값", "빈 값", "①", "②", "②m(fact 부가칸)", "③", "④"):
            tot[k] += r[k]
            tot[f"{r['class']}:{k}"] += r[k]
            by_file[r["file"]][k] += r[k]
        for lc in ("long", "short"):
            for k, v in r[lc].items():
                tot[f"{lc}{k}"] += v
                by_file[r["file"]][f"{lc}{k}"] += v
    res = {"gold_build": gh, "raw_dir": str(RAW), "silver_files": SILVER, "fields": len(out_rows),
           "total": dict(tot), "by_file": {k: dict(v) for k, v in sorted(by_file.items())}, "rows": out_rows}
    json.dump(res, sys.stdout, ensure_ascii=False, indent=1, sort_keys=False)


if __name__ == "__main__":
    main()
