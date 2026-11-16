#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v1.1 — 참조 해결 결정론 분해 규칙(B) 실행기.

입력(같은 폴더): erd-v1.1-dictionaries.json(사전·이름 색인) · erd-v1.1.json(resolve_rules — 없으면 erd_spec_v11.RESOLVE_RULES) · erd-v1.json(v1 수치, 나란히 비교용)
      원장 21(/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26) · step1-products.json
출력: 표준 출력에 자리별 v1 vs v1.1 표 + erd-v1.1-resolve.json(행 단위 결과)

규칙은 전부 데이터(erd-v1.1.json → resolve_rules)다. 이 스크립트는 그 데이터를 그대로 실행한다. 유사도·추측 없음.
실행: python3 erd-v1.1-resolve.py
"""
import json
import os
import re
import sys
import unicodedata
from collections import Counter, OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = "/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26"
STEP1 = "step1-products.json"


def norm(s):
    if s is None:
        return None
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", str(s)).casefold())


# ---------------------------------------------------------------------------
# 사전 색인
# ---------------------------------------------------------------------------
class Lexicon:
    """erd-v1.1-dictionaries.json 의 사전 7개(modality · product_name · modality_subcategory_label · procedure_name · site · unit · product_tier)를 정규화 키로 색인."""

    def __init__(self, dic_json):
        D = {d["name"]: d for d in dic_json["dictionaries"]}
        self.idx = {k: defaultdict(set) for k in ["modality", "product", "modality_subcategory", "procedure", "site", "unit", "product_tier"]}
        src = {"modality": "modality", "product": "product_name", "modality_subcategory": "modality_subcategory_label", "procedure": "procedure_name",
               "site": "site", "unit": "unit", "product_tier": "product_tier"}
        for kind, dname in src.items():
            for e in D[dname]["entries"]:
                code = e.get("code")
                keys = [e["canonical"]] + [s["value"] for s in e.get("synonyms", [])]
                for k in keys:
                    self.idx[kind][norm(k)].add((code, e["canonical"]))
        self.sub_ids = {s["value"] for e in D["modality_subcategory_label"]["entries"] for s in e.get("synonyms", []) if s.get("link") == "code"}
        self.site_entries = D["site"]["entries"]

    def hits(self, kind, text):
        return self.idx[kind].get(norm(text), set())


# ---------------------------------------------------------------------------
# 분해 규칙 실행
# ---------------------------------------------------------------------------
class Resolver:
    PRIMARY = ("product", "modality_subcategory", "procedure")
    DEPTH = {"modality": "modality", "modality_subcategory": "subcategory", "procedure": "procedure", "product": "product"}

    def __init__(self, lex, rules):
        self.lex = lex
        self.rules = rules
        s2 = rules["step2_decompose"]
        self.paren_re = re.compile(s2["paren_regex"])
        self.combo_re = re.compile("[" + re.escape("".join(s2["combo_symbols"])) + "]")
        self.spec_re = re.compile(s2["spec_regex"])
        self.order = s2["dictionary_order"]
        self.code_re = re.compile(rules["step1_family"]["code_regex"])

    @staticmethod
    def _in_family(code, family):
        return code is not None and family is not None and family in str(code).split("|")

    def primary(self, text, family, types=None):
        """제품·하위분류·단위 시술 조각 판정. 계열 안 우선, 없으면 전 계열(다른 계열 조합 멤버). 겹침은 overlap_rule.
        계열 힌트가 없고 조각이 여러 계열에 닿으면 모호."""
        kinds_allowed = [k for k in self.PRIMARY if types is None or k in types]
        allhits = {k: (self.lex.hits(k, text) if k in kinds_allowed else set()) for k in self.PRIMARY}
        if not any(allhits.values()):
            return None
        scoped = {k: {h for h in v if self._in_family(h[0], family)} for k, v in allhits.items()}
        use, cross = (scoped, False) if family and any(scoped.values()) else (allhits, family is not None)
        kinds = [k for k in self.PRIMARY if use[k]]
        kind = "procedure" if "procedure" in kinds else "modality_subcategory" if "modality_subcategory" in kinds else "product"
        hs = use[kind]
        codes = set()
        for h in hs:
            codes |= set(str(h[0]).split("|"))
        if len(codes) > 1 and not (family and family in codes):
            return {"kind": "ambiguous", "text": text, "codes": sorted(codes), "overlap": kinds}
        h = sorted(hs, key=lambda x: str(x))[0]
        code = family if (family and family in codes) else h[0]
        return {"kind": kind, "text": text, "code": code, "canonical": h[1], "overlap": kinds if len(kinds) > 1 else None, "cross_family": cross}

    def classify(self, text, family, types=None):
        """조각 하나 → 닿은 사전(kind) 또는 None. 순서: 계열 → 제품 → 하위분류 → 단위 시술 → 부위 → 규격 → product_tier."""
        t = text.strip()
        if not t:
            return None
        if types is None or "modality" in types:
            m = self.lex.hits("modality", t)
            if m:
                codes = {h[0] for h in m}
                if len(codes) == 1:
                    c = next(iter(codes))
                    return {"kind": "modality", "text": t, "code": c, "canonical": next(iter(m))[1]}
        p = self.primary(t, family, types)
        if p:
            return p
        s = self.lex.hits("site", t)
        if s:
            return {"kind": "site", "text": t, "canonical": next(iter(s))[1]}
        nt = unicodedata.normalize("NFKC", t)
        if self.spec_re.match(nt) or self.lex.hits("unit", t):
            return {"kind": "spec", "text": t, "canonical": nt}
        tier = self.lex.hits("product_tier", t)
        if tier:
            return {"kind": "product_tier", "text": t, "canonical": next(iter(tier))[1]}
        return None

    def whole(self, label, family, types=None):
        """통째 일치(괄호·조합 없이 하나의 사전 값). v1 과 같은 의미의 resolved."""
        c = self.classify(label, family, types)
        if c and c["kind"] in ("modality", "product", "modality_subcategory", "procedure") and (types is None or c["kind"] in types):
            return c
        return None

    def resolve(self, label, hint=None, types=None):
        label = str(label)
        family = hint
        w = self.whole(label, family, types)
        if w:
            return {"label": label, "hint": hint, "status": "resolved", "depth": self.DEPTH[w["kind"]], "family": w.get("code") or family,
                    "target": f"{self.DEPTH[w['kind']]}:{w.get('code')}:{w['canonical']}", "overlap": w.get("overlap"), "spans": [w], "untouched": []}
        # 2. 분해
        parens = self.paren_re.findall(label)
        outer = self.paren_re.sub(" ", label)
        groups = [("outer", outer)] + [("inner", p) for p in parens]
        fragments = []
        for where, g in groups:
            for part in self.combo_re.split(g):
                part = part.strip(" ·")
                if part:
                    fragments.append((where, part))
        spans, untouched = [], []
        for where, frag in fragments:
            c = self.classify(frag, family)
            if c and c["kind"] != "ambiguous":
                c["where"] = where
                spans.append(c)
                continue
            toks = frag.split()
            i = 0
            while i < len(toks):
                found = None
                for j in range(len(toks), i, -1):
                    span = " ".join(toks[i:j])
                    h = self.classify(span, family)
                    if h and h["kind"] != "ambiguous":
                        found = (h, j)
                        break
                if found:
                    found[0]["where"] = where
                    spans.append(found[0])
                    i = found[1]
                else:
                    amb = self.classify(toks[i], family)
                    untouched.append({"text": toks[i], "where": where, "reason": "모호(계열 " + ",".join(amb["codes"]) + ")" if amb and amb["kind"] == "ambiguous" else "사전 없음"})
                    i += 1
        # 1. 계열 확정(힌트 없으면 이름의 계열 동의어)
        if family is None:
            mods = [s for s in spans if s["kind"] == "modality"]
            prim = [s for s in spans if s["kind"] in self.PRIMARY and s.get("code") and "|" not in str(s["code"])]
            if mods:
                family = mods[0]["code"]
            elif len(prim) == 1:
                family = prim[0]["code"]
        primaries = [s for s in spans if s["kind"] in ("modality",) + self.PRIMARY]
        sites = [s["canonical"] for s in spans if s["kind"] == "site"]
        specs = [s["canonical"] for s in spans if s["kind"] == "spec"]
        tiers = [s["canonical"] for s in spans if s["kind"] == "product_tier"]
        tup = {"family": family, "primaries": [(s["kind"], s.get("code"), s["canonical"]) for s in primaries], "sites": sites, "specs": specs, "tiers": tiers}
        if untouched:
            return {"label": label, "hint": hint, "status": "unresolved", "depth": None, "family": family, "target": None, "tuple": tup,
                    "partial": [(s["kind"], s["canonical"]) for s in spans], "untouched": untouched, "spans": spans}
        shape = "combo" if len(primaries) >= 2 else "single_primary_qualified" if len(primaries) == 1 else "qualifier_only"
        return {"label": label, "hint": hint, "status": "decomposed", "depth": None, "family": family, "target": None, "tuple": tup, "shape": shape, "spans": spans, "untouched": []}


# ---------------------------------------------------------------------------
# 자리(slot) 정의 — v1 §9.2 와 같은 자리
# ---------------------------------------------------------------------------
def slot_items(L, lex):
    """{slot_name: (note, [(label, hint, types)])}"""
    MC = re.compile(r"^(M\d+)(?:[-_ ](.+))?$")

    def split_code(s):
        m = MC.match(s)
        return (m.group(1), m.group(2)) if m else (None, s)

    S = OrderedDict()
    nodes = Counter()
    for l in L["synergy.json"]["links"]:
        nodes[l["from"]] += 1
        nodes[l["to"]] += 1
    S["synergy.links[].from/to (노드 52)"] = ("코드로 계열 확정 후 이름을 분해", [(lab, code, None) for nd in nodes for code, lab in [split_code(nd)]])
    pp = L["problem-packages.json"]
    seen = OrderedDict()
    for p in pp["problems"]:
        for c in p["complaints"]:
            for pr in c["procedures"]:
                seen[(pr["name"], pr["category"])] = 1
    S["problem-packages.procedures[].name (시술 종류 29)"] = ("질문 10", [(n, h, None) for n, h in seen])
    seen = Counter(x for p in pp["problems"] for c in p["complaints"] for cb in c["combos"] for x in cb["combo"])
    S["problem-packages.combos[].combo[] (멤버 29)"] = ("힌트 없음", [(n, None, None) for n in seen])
    seen = Counter(x for p in pp["problems"] for c in p["complaints"] for pr in c["procedures"] for x in pr["products"])
    S["problem-packages.procedures[].products[] (제품 34)"] = ("제품 사전만", [(n, None, ("product",)) for n in seen])
    pc = L["procedure-comparison.json"]
    S["procedure-comparison.procedures[].name (39)"] = ("질문 11", [(pr["name"], pr["category"], None) for c in pc["comparisons"] for pr in c["procedures"]])
    to = L["treatment-optimization.json"]
    seen = Counter(x for c in to["by_concern"] for s in c["severity_levels"] for x in s["optimal_combo"])
    S["treatment-optimization.optimal_combo[] (57)"] = ("", [(n, None, None) for n in seen])
    seen = Counter(x for g in to["by_age_group"] for k in ["recommended_base", "avoid", "upgrade"] for x in g.get(k, []))
    S["treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)"] = ("", [(n, None, None) for n in seen])
    seen = Counter(x for pl in to["annual_plans"] for s in pl["schedule"] for x in s["procedures"])
    S["treatment-optimization.annual_plans.schedule[].procedures[] (29)"] = ("`토닝 4회` 횟수 섞임 → 규격 조각", [(n, None, None) for n in seen])
    ts = L["treatment-sequence.json"]
    items = []
    for s in ts["sequence_order"]:
        for c in s["categories"]:
            code, lab = split_code(c)
            if code and lab is None:
                items.append(("__MODALITY__" + code, code, None))
            elif code and c in lex.sub_ids:
                items.append(("__SUBID__" + c, code, None))
            else:
                items.append((lab if lab else c, code, None))
    S["treatment-sequence.sequence_order[].categories[] (19)"] = ("질문 7: 실존 하위분류 id 는 id 로, 코드만은 계열로, 코드+라벨은 라벨을 분해", items)
    S["treatment-sequence.incompatible_same_day[].pair[] (14 distinct)"] = ("", [(x, None, None) for p in ts["incompatible_same_day"] for x in p["pair"]])
    S["treatment-sequence.minimum_intervals from/to (14 distinct)"] = ("", [(x, None, None) for m in ts["minimum_intervals"] for x in (m["from"], m["to"])])
    S["treatment-sequence.common_combos[].sequence[] (22 distinct)"] = ("", [(x, None, None) for c in ts["common_combos"] for x in c["sequence"]])
    ppt = L["post-procedure-timeline.json"]
    S["post-procedure-timeline.timelines[].name (10)"] = ("category 계열에는 항상 붙고, 이름은 분해", [(t["name"], split_code(t["category"])[0], None) for t in ppt["timelines"]])
    mp = L["market-pricing.json"]
    S["market-pricing.items[].name (122)"] = ("질문 11", [(i["name"], c["id"], None) for c in mp["categories"] for i in c["items"]])
    return S


def run_slot(R, items):
    rows, seen = [], set()
    for label, hint, types in items:
        if (label, hint) in seen:
            continue
        seen.add((label, hint))
        if isinstance(label, str) and label.startswith("__MODALITY__"):
            code = label[12:]
            rows.append({"label": code, "hint": code, "status": "resolved", "depth": "modality", "family": code, "target": f"modality:{code}", "untouched": [], "spans": []})
            continue
        if isinstance(label, str) and label.startswith("__SUBID__"):
            sid = label[9:]
            rows.append({"label": sid, "hint": hint, "status": "resolved", "depth": "subcategory", "family": hint, "target": f"subcategory:{hint}:{sid}", "untouched": [], "spans": []})
            continue
        rows.append(R.resolve(label, hint, types))
    return rows


def summarize(name, note, rows):
    res = [r for r in rows if r["status"] == "resolved"]
    dec = [r for r in rows if r["status"] == "decomposed"]
    unr = [r for r in rows if r["status"] == "unresolved"]
    return {"note": note, "n": len(rows), "resolved": len(res), "decomposed": len(dec), "unresolved": len(unr),
            "by_depth": dict(Counter(r["depth"] for r in res)), "by_shape": dict(Counter(r["shape"] for r in dec)),
            "untouched_fragments": dict(Counter(u["text"] for r in unr for u in r["untouched"])),
            "decomposed_labels": [(r["label"], r["hint"], r.get("shape"), r.get("tuple")) for r in dec],
            "unresolved_labels": [(r["label"], r["hint"], [u["text"] for u in r["untouched"]], r.get("partial", [])) for r in unr],
            "rows": rows}


def run_all(dic_json, rules, L, step1, v1_report=None):
    lex = Lexicon(dic_json)
    R = Resolver(lex, rules)
    OUT = OrderedDict()
    for name, (note, items) in slot_items(L, lex).items():
        OUT[name] = summarize(name, note, run_slot(R, items))
    # pih-risk procedure_ref — id 깊이 (분해 대상 아님)
    tx = L["taxonomy.json"]
    sub_ids = {sc["id"] for m in tx["modality"] for sc in m["subcategories"]}
    item_ids = {it["id"] for m in tx["modality"] for sc in m["subcategories"] for it in sc["items"]}
    mod_ids = {m["id"] for m in tx["modality"]}
    rows = []
    for p in L["pih-risk.json"]["procedures"]:
        ref = p["procedure_ref"]
        depth = "procedure" if ref in item_ids else "subcategory" if ref in sub_ids else "modality" if ref in mod_ids else None
        rows.append({"label": p["name"], "hint": ref, "status": "resolved" if depth else "unresolved", "depth": depth, "family": ref.split("-")[0], "target": f"{depth}:{ref}", "untouched": [] if depth else [{"text": ref, "reason": "id 없음"}], "spans": []})
    OUT["pih-risk.procedure_ref (26)"] = summarize("pih", "질문 5 깊이 — id 참조라 분해 규칙 대상 아님(v1 과 같은 판정)", rows)
    # 고민 사전 일치 — 고민 축은 v1 규칙(정규화 일치 + 동의어)을 v1.1 사전으로 다시 센다 (B 는 시술 참조 자리의 규칙)
    D = {d["name"]: d for d in dic_json["dictionaries"]}
    pidx = {}
    for e in D["problem"]["entries"]:
        pidx[norm(e["canonical"])] = e
        for s in e["synonyms"]:
            pidx[norm(s["value"])] = e
    to = L["treatment-optimization.json"]
    pc = L["procedure-comparison.json"]
    rows = []

    def prow(label, hint):
        e = pidx.get(norm(label))
        rows.append({"label": label, "hint": hint, "status": "resolved" if e else "unresolved", "depth": "problem" if e else None, "family": None,
                     "target": f"problem:{e['code']}:{e['canonical']}" if e else None, "untouched": [] if e else [{"text": label, "reason": "고민 사전 없음"}], "spans": []})
    for c in to["by_concern"]:
        prow(c["concern"], None)
    for c in pc["comparisons"]:
        e = pidx.get(norm(c["id"])) or pidx.get(norm(c["title"]))
        rows.append({"label": f"{c['id']} / {c['title']}", "hint": None, "status": "resolved" if e else "unresolved", "depth": "problem" if e else None, "family": None,
                     "target": f"problem:{e['code']}:{e['canonical']}" if e else None, "untouched": [] if e else [{"text": c["id"], "reason": "고민 사전 없음"}], "spans": []})
    for g in to["by_age_group"]:
        for x in g["primary_concerns"]:
            prow(x, g["age"])
    OUT["고민 사전 일치 (concern 8 · comparison 9 · primary_concerns 17)"] = summarize("problem", "질문 12 — 고민 축은 사전 일치(v1 규칙) 그대로", rows)
    # 부위 사전
    se = lex.site_entries
    bb = sum(1 for e in se if e.get("site_kind") == "backbone")
    tl = [e["canonical"] for e in se if e.get("site_kind") == "taxonomy_site_label"]
    OUT["부위 사전 (뼈대 11 + 확장)"] = {"note": "질문 24 · 8-2 처분: 확장 0, taxonomy 부위 라벨 10", "n": len(se), "resolved": bb + len(tl), "decomposed": 0, "unresolved": 0,
                                   "by_depth": {"backbone": bb, "taxonomy_site_label": len(tl), "extension": 0}, "by_shape": {}, "untouched_fragments": {},
                                   "decomposed_labels": [], "unresolved_labels": [], "rows": []}
    # taxonomy canonical_category → 하위분류
    rows = []
    for m in tx["modality"]:
        for sc in m["subcategories"]:
            for it in sc["items"]:
                if "canonical_category" in it:
                    lab = it["canonical_category"].split(">")[-1].strip()
                    code = it["canonical_category"].split()[0]
                    r = R.resolve(lab, code, ("modality_subcategory",))
                    r["label"] = it["canonical_category"]
                    r["hint"] = it["name"]
                    rows.append(r)
    OUT["taxonomy canonical_category → 하위분류 (6)"] = summarize("canon", "질문 23 — 하위분류 사전만", rows)
    # step1 제품 ↔ 원장 59 제품 대응 (C) — B 규칙으로만
    rows = []
    for it in step1["items"]:
        fam = it["family"]["code"] if re.match(r"^M\d+$", it["family"]["code"]) else None
        names = [("display_name", it["2_names"]["display_name"])]
        if it["2_names"].get("ledger_name"):
            names.append(("ledger_name", it["2_names"]["ledger_name"]))
        names += [("search_name", s["name"]) for s in it["2_names"].get("search_names", [])]
        best = None
        tried = []
        for role, nm in names:
            r = R.resolve(nm, fam, ("product", "procedure"))
            tried.append((role, nm, r["status"], r.get("target")))
            if r["status"] == "resolved" and r["depth"] == "product":
                best = {"role": role, "name": nm, "target": r["target"]}
                break
            if r["status"] == "resolved" and r["depth"] == "procedure" and r.get("overlap") and "product" in r["overlap"]:
                best = {"role": role, "name": nm, "target": r["target"].replace("procedure:", "product:")}
                break
        if best:
            rows.append({"label": it["2_names"]["display_name"], "hint": fam, "status": "resolved", "depth": "product", "family": fam, "target": best["target"], "matched_by": best["role"], "matched_name": best["name"], "ledger_id": it["ledger_id"], "active": it["active"], "untouched": [], "spans": []})
        else:
            dec = [t for t in tried if t[2] == "decomposed"]
            r0 = R.resolve(names[0][1], fam)
            r0.update({"label": it["2_names"]["display_name"], "hint": fam, "ledger_id": it["ledger_id"], "active": it["active"], "tried": tried})
            if r0["status"] == "resolved":  # 제품이 아닌 깊이(계열·하위분류·시술)로만 통째 일치 → origin=survey, 깊이는 기록
                r0["status"] = "decomposed"
                r0["shape"] = "non_product_depth:" + r0["depth"]
                r0["tuple"] = {"family": fam, "primaries": [(r0["depth"], r0.get("family"), r0["target"])], "sites": [], "specs": [], "tiers": []}
            elif dec and r0["status"] != "decomposed":  # 다른 이름(검색 이름 등)이 분해 성공 → 그 결과로
                r0["status"] = "decomposed"
                r0["shape"] = "single_primary_qualified(other_name)"
                r0["untouched"] = []
            rows.append(r0)
    s = summarize("step1", "C: step1 395 → 원장 59 제품 대응은 B 규칙(이름 분해·동의어)으로만. resolved = 원장 제품(origin=ledger 대응), 그 외 = origin=survey", rows)
    s["ledger_products_covered"] = len({r["target"] for r in rows if r["status"] == "resolved"})
    s["matched_by"] = dict(Counter(r.get("matched_by") for r in rows if r["status"] == "resolved"))
    s["survey_products"] = s["n"] - s["resolved"]
    s["inactive_items"] = sum(1 for r in rows if not r["active"])
    OUT["step1-products.items[] display/ledger/search 이름 → 원장 제품 (395)"] = s
    # 전체 집계
    total = OrderedDict()
    excl = ("부위 사전 (뼈대 11 + 확장)", "step1-products.items[] display/ledger/search 이름 → 원장 제품 (395)")
    total["unresolved_v1_1"] = sum(v["unresolved"] for k, v in OUT.items() if k not in excl)
    total["decomposed_v1_1"] = sum(v["decomposed"] for k, v in OUT.items() if k not in excl)
    total["resolved_v1_1"] = sum(v["resolved"] for k, v in OUT.items() if k not in excl)
    frag = Counter()
    for k, v in OUT.items():
        if k not in excl:
            for f, n in v["untouched_fragments"].items():
                frag[f] += n
    total["top_untouched_fragments"] = frag.most_common(40)
    if v1_report:
        total["unresolved_v1"] = sum(v["unresolved"] for k, v in v1_report.items() if not k.startswith("부위 사전"))
    return OUT, total


def side_by_side(OUT, v1_report):
    lines = ["| 참조 자리 | 건 | v1 해결 | v1 미해결 | v1.1 해결(깊이) | v1.1 분해 성공·항목 없음(모양) | v1.1 미해결 | 미해결 사유 상위 조각 |", "|---|---|---|---|---|---|---|---|"]
    for k, v in OUT.items():
        v1 = (v1_report or {}).get(k)
        d = ", ".join(f"{a}={b}" for a, b in v["by_depth"].items()) or "—"
        sh = ", ".join(f"{a}={b}" for a, b in v["by_shape"].items()) or "—"
        top = " · ".join(f"`{f}`×{n}" for f, n in Counter(v["untouched_fragments"]).most_common(5)) or "—"
        lines.append(f"| {k} | {v['n']} | {v1['resolved'] if v1 else '—'} | {v1['unresolved'] if v1 else '—'} | {v['resolved']} ({d}) | {v['decomposed']} ({sh}) | {v['unresolved']} | {top} |")
    return "\n".join(lines)


def load_all():
    dic = json.load(open(os.path.join(HERE, "erd-v1.1-dictionaries.json"), encoding="utf-8"))
    try:
        rules = json.load(open(os.path.join(HERE, "erd-v1.1.json"), encoding="utf-8"))["resolve_rules"]
    except FileNotFoundError:
        sys.path.insert(0, HERE)
        import erd_spec_v11
        rules = erd_spec_v11.RESOLVE_RULES
    files = [f for f in os.listdir(LEDGER) if f.endswith(".json")]
    L = {f: json.load(open(os.path.join(LEDGER, f), encoding="utf-8")) for f in files}
    step1 = json.load(open(os.path.join(HERE, STEP1), encoding="utf-8"))
    v1 = None
    p = os.path.join(HERE, "erd-v1.json")
    if os.path.exists(p):
        v1 = json.load(open(p, encoding="utf-8")).get("resolution_report")
    return dic, rules, L, step1, v1


def main():
    dic, rules, L, step1, v1 = load_all()
    OUT, total = run_all(dic, rules, L, step1, v1)
    print(side_by_side(OUT, v1))
    print()
    print("합계(부위 사전·step1 제외): v1 미해결", total.get("unresolved_v1"), "→ v1.1 해결", total["resolved_v1_1"], "· 분해 성공·항목 없음", total["decomposed_v1_1"], "· 미해결", total["unresolved_v1_1"])
    print("미해결 사유 상위 조각:", " · ".join(f"{f}×{n}" for f, n in total["top_untouched_fragments"][:25]))
    json.dump({"erd_version": "v1.1", "rules": rules["name"], "slots": OUT, "total": total}, open(os.path.join(HERE, "erd-v1.1-resolve.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("→ erd-v1.1-resolve.json")


if __name__ == "__main__":
    main()
