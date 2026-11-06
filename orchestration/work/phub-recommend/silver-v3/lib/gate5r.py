# -*- coding: utf-8 -*-
"""결정 묶음 5 축소본 — 원장 근거로 기계가 정할 수 있는 것은 규칙 결정(decisions/batch5-rule/ · decided_by=rule:<id>)으로, 사람이 볼 것만 게이트에.

산출(빌드가 늘 쓴다 · 재실행 동일): out/gate/batch5-reduced.json·.md · batch5-nodes.md(참고) · batch5-auto-folds.md · batch5-rule-decisions.json
원본 out/gate/batch5.json·.md(432 자리)는 그대로 — 어느 쪽을 쓸지는 사용자가 정한다.
규칙 결정 파일: `python3 build.py --propose5-rules` → decisions/batch5-rule/(status=proposed — 빌드가 읽지 않는다 · 축소본 auto-rules 항목에서 승인하면 같은 파일이 approved 로 바뀐다).

규칙(코디 지시 2026-11-05 · 결정 reason 에 규칙 id 와 출처 locator):
  B5R-A 「X감」↔「X」(~감 접미 · ⑦ suffix_감)       B5R-B 원장 병기 「X (Y)」/「X(Y)」(⑦ paren_pair · 괄호 밖 본 표기 유지)
  B5R-C 띄어쓰기·전각·대소문자만 다름(정규화 같음)   B5R-D 영문 병기(사전 동의어 표의 영문)
  B5R-E 「X 형성」「X 발생」↔「X」(⑦ suffix_형성 · 「X 발생」)
  B5R-ABBR 줄임말 — 「정식명이 줄임말을 접두로 포함」 · 후보 하나 → canonical_mapping(그 조각이 미해결로 남은 참조 anchor 안에서만)
접는 방향: 원장 노드만 접힌다(사전 사건은 접히지 않는다) · 둘 다 원장 노드면 접미가 붙은 쪽(A·E)·괄호 안(B)이 접힌다.
"""
import copy
import json
import os
import re
from collections import Counter, OrderedDict, defaultdict

from .decisions import validate
from .gate2b import node
from .gate3 import leaves_of, opt
from .gate5 import BATCH_NOTE, G5, SEED_FILE, _examples, _h, batch3_items, payload, paren_outer
from .util import dedupe, md_table, mkid, norm, write_json, write_text
from . import v32 as V

RID = "DEC-2026-11-05-B5R"
DECIDED_AT = "2026-11-05"
AUTO = ("B5R-B", "B5R-C", "B5R-D")           # 표기만 다른 것 — 자동 접기
GROUPED = OrderedDict([("B5R-A", "~감 접미"), ("B5R-E", "형성/발생")])   # 뜻이 같은지가 임상 판단 — 규칙 단위 묶음(전부 같다 / 전부 다르다 / 개별)
RULES = OrderedDict([("B5R-A", "「X감」↔「X」(~감 접미)"), ("B5R-B", "원장 병기 「X (Y)」/「X(Y)」 — 괄호 밖 본 표기 유지"), ("B5R-C", "띄어쓰기·전각·대소문자만 다름"),
                     ("B5R-D", "영문 병기(사전 동의어 표의 영문)"), ("B5R-E", "「X 형성」「X 발생」↔「X」"), ("B5R-ABBR", "줄임말 — 정식명이 줄임말을 접두로 포함 · 후보 하나")])
LATIN = re.compile(r"^[A-Za-z][A-Za-z0-9 .\-]*$")


def classify(p, g, dict_entries):
    """⑦ strong 쌍 → (규칙 id, 접히는 노드, 접힐 곳) 또는 None. p = conflict.pair."""
    a, b, bk, rules = p["node"], p["other"], p["other_kind"], p["rules"]
    na, nb = norm(a), norm(b)

    def direction(long_, short_):
        # 원장 노드만 접힌다 — 사전 사건이 끼면 원장 노드 쪽이 접힌다
        if bk == "dictionary":
            return a, b
        return long_, short_

    if na == nb:
        return ("B5R-C",) + direction(a, b)
    if "paren_pair" in rules:
        if bk == "dictionary":
            return ("B5R-B", a, b)
        outer = paren_outer(g.L, a, b)
        if outer:
            return ("B5R-B", b if outer == a else a, outer)
    if "suffix_감" in rules:
        long_, short_ = (a, b) if len(na) > len(nb) else (b, a)
        return ("B5R-A",) + direction(long_, short_)
    if "suffix_형성" in rules or (na.endswith("발생") and na[:-2] == nb) or (nb.endswith("발생") and nb[:-2] == na):
        long_, short_ = (a, b) if len(na) > len(nb) else (b, a)
        return ("B5R-E",) + direction(long_, short_)
    if bk == "dictionary":
        e = dict_entries.get(nb)
        lat = {norm(s_["value"]) for s_ in (e or {}).get("synonyms", []) if LATIN.match(s_["value"])}
        if na in lat:
            return ("B5R-D", a, b)
    return None


def rule_decisions(S, g):
    """규칙 결정(proposed · decided_by=rule:<id>) — 접기 · 줄임말 매핑. 반환 (결정 목록, 접기 표, 매핑 표, 규칙 밖 ⑦)."""
    A = S.ctx["adv"]
    nodes = {n["canonical"]: n for n in A["ledger_events"]}
    dict_entries = {}
    for e in g.dicts["adverse_event_type"]["entries"]:
        if e.get("origin") != "ledger":
            for v in [e["canonical"]] + [s_["value"] for s_ in e.get("synonyms", [])]:
                dict_entries.setdefault(norm(v), e)
    strong = [c for c in S.ctx.get("ledger_dup_conflicts", []) if c.get("grade") == "strong" and c["status"] == "open"]
    cand = []
    for c in strong:
        r = classify(c["pair"], g, dict_entries)
        if r:
            cand.append((c, r))
    by_src = defaultdict(set)
    for c, (rid, src, tgt) in cand:
        by_src[src].add(norm(tgt))
    folds, decs, rest = [], [], []
    seen = set()
    group_of = {}
    for c, (rid, src, tgt) in cand:
        if rid in GROUPED:            # 뜻이 같은지가 임상 판단인 규칙(~감 · 형성/발생) — 자동 적용 금지 · 규칙 단위 묶음으로 게이트(코디 정정 2026-11-05)
            group_of[c["id"]] = (rid, src, tgt)
            rest.append((c, f"규칙 묶음 {rid} {RULES[rid]}"))
            continue
        if len(by_src[src]) > 1:      # 같은 노드가 서로 다른 곳으로 접히는 후보 둘 이상 — 규칙으로 못 정한다(게이트)
            rest.append((c, f"{src} 의 접힐 곳 후보 {len(by_src[src])}"))
            continue
        if (src, norm(tgt)) in seen:
            continue
        seen.add((src, norm(tgt)))
        n = nodes.get(src)
        refs = [g.src(l) for l in (n["locators"] if n else [])]
        dk = c["pair"]["erd_key"]
        reason = (f"규칙 {rid} {RULES[rid]} — ⑦ strong 「{c['pair']['node']}」↔「{c['pair']['other']}」(표기 규칙 {', '.join(c['pair']['rules'])} · 안정 키 {dk}) · 원장 노드 「{src}」(원장 {len(refs)} 자리: "
                  + ", ".join(refs[:6]) + (" …" if len(refs) > 6 else "") + f")를 「{tgt}」에 접는다(동의어 · 단위 id 는 접힐 곳 기준). 원장 근거로 기계가 정함(코디 지시 2026-11-05).")
        d = payload(f"{RID}-F-{_h(dk)}", "fold_approve", OrderedDict([("dictionary", "adverse_event_type"), ("canonical", src), ("into", tgt)]), OrderedDict([("keep", tgt)]), reason, refs,
                    [{"kind": "erd", "ref": dk}, {"kind": "brief", "ref": f"rule:{rid}"}])
        d.update(decided_by=f"rule:{rid}", decided_at=DECIDED_AT, batch="결정 묶음 5 규칙(batch5-rule · 원장 근거 자동 · 사용자 승인 전 proposed)", rule_id=rid, _store="batch5-rule")
        decs.append(d)
        folds.append(OrderedDict([("rule", rid), ("node", src), ("into", tgt), ("into_kind", "dictionary" if norm(tgt) in dict_entries else "ledger"), ("pair", [c["pair"]["node"], c["pair"]["other"]]),
                                  ("rules", c["pair"]["rules"]), ("locators", len(refs)), ("decision", d["id"]), ("conflict", c["id"])]))
    auto_ids = {f["conflict"] for f in folds}
    rest += [(c, "규칙 밖(뜻이 다를 수 있다)") for c in strong if c["id"] not in auto_ids and not any(c is x[0] for x in rest)]
    # 줄임말 — 정식명이 줄임말을 접두로 포함 · 후보 하나
    seeds = json.load(open(S.ctx["seeds_path"], encoding="utf-8"))
    rows = [r for r in seeds["seeds"]["product_abbrev"]["rows"] if r.get("status") == "proposed"]
    nfrag = Counter(r["fragment"] for r in rows)
    P = S.ctx["proc"]
    refrows = [r for v in P["ref_rows"].values() for r in v] + list(P["mk_rows"])
    maps, abbr_rest = [], []
    for r in rows:
        if r["rule"] != "정식명이 줄임말을 접두로 포함" or nfrag[r["fragment"]] != 1:
            abbr_rest.append((r, "후보 둘 이상" if nfrag[r["fragment"]] > 1 else "규칙 밖(조각이 제품명을 접두로 포함)"))
            continue
        pe = S.ctx["ids"].prod.get(norm(r["product"]))
        scope = sorted({x["ref_id"] for x in refrows if x.get("ref_id") and x.get("result") == "unresolved" and any(norm(u if isinstance(u, str) else u.get("text")) == norm(r["fragment"]) for u in x.get("unregistered") or [])})
        if pe is None or not scope:
            maps.append(OrderedDict([("fragment", r["fragment"]), ("product", r["product"]), ("decision", None), ("why", "제품 레코드 없음" if pe is None else "이 조각이 미해결로 남은 참조 없음(이미 다른 결정·사전으로 풀림 · 결정 만들지 않음)"), ("n", r["n"])]))
            continue
        refs = [g.src(l) for l in r.get("locators") or []]
        key = f"abbr|{r['fragment']}|{r['product']}"
        reason = (f"규칙 B5R-ABBR {RULES['B5R-ABBR']} — 조각 「{r['fragment']}」 → 제품 「{r['product']}」({r.get('product_origin')} · {pe['id']}) · 이 조각이 미해결로 남은 참조 {len(scope)} 안에서만(scope) · 원장 {len(refs)} 자리: "
                  + ", ".join(refs[:6]) + (" …" if len(refs) > 6 else "") + " · 출처 erd-v3.2-seed-candidates.json product_abbrev")
        d = payload(f"{RID}-M-{_h(key)}", "canonical_mapping", OrderedDict([("from_ref", r["fragment"]), ("scope", scope)]), OrderedDict([("to_id", pe["id"])]), reason, refs,
                    [{"kind": "erd", "ref": f"{SEED_FILE}#seeds/product_abbrev"}, {"kind": "brief", "ref": "rule:B5R-ABBR"}])
        d.update(decided_by="rule:B5R-ABBR", decided_at=DECIDED_AT, batch="결정 묶음 5 규칙(batch5-rule · 원장 근거 자동 · 사용자 승인 전 proposed)", rule_id="B5R-ABBR", _store="batch5-rule")
        decs.append(d)
        maps.append(OrderedDict([("fragment", r["fragment"]), ("product", r["product"]), ("decision", d["id"]), ("scope", scope), ("n", r["n"])]))
    return decs, folds, maps, rest, abbr_rest, group_of


def after_folds(S, folds, rest):
    """규칙 접기를 적용했다고 보고 남는 ⑦ strong 쌍 — 접힌 노드는 접힐 곳으로 바꿔 표기 규칙을 다시 대고(V.dup_rules · 같은 규칙) strong 만 남긴다. 사전 ↔ 사전은 ⑦ 아님."""
    fm = {norm(f["node"]): f["into"] for f in folds}

    def res(x):
        seen = set()
        while norm(x) in fm and norm(x) not in seen:
            seen.add(norm(x))
            x = fm[norm(x)]
        return x
    nodes = {norm(n["canonical"]) for n in S.ctx["adv"]["ledger_events"]}
    kr = S.ctx["erd"]["tuple_rules"]["phrase_kinds"]
    out, seen = [], set()
    for c, why in rest:
        a, b = res(c["pair"]["node"]), res(c["pair"]["other"])
        changed = (a, b) != (c["pair"]["node"], c["pair"]["other"])
        if norm(a) == norm(b):
            continue
        a_led, b_led = norm(a) in nodes and norm(a) not in fm, norm(b) in nodes and norm(b) not in fm
        if not a_led and not b_led:
            continue                                              # 사전 ↔ 사전(또는 접힌 노드 둘) — ⑦ 아님
        if changed:
            h = V.dup_rules(norm(a), norm(b), kr, [norm(w) for w in a.split()], [norm(w) for w in b.split()])
            if not any(gr == "strong" for _, gr in h):
                continue
        k = frozenset((norm(a), norm(b)))
        if k in seen:
            continue
        seen.add(k)
        out.append((c, a if a_led else b, b if a_led else a, changed, why))
    return out


def build_reduced(S, out_dir, seeds_path, propose_dir=None):
    S.ctx["seeds_path"] = seeds_path
    g = G5(S, S.ctx["args"].decisions)
    decs, folds, maps, rest, abbr_rest, group_of = rule_decisions(S, g)
    remain = after_folds(S, folds, rest)
    A = S.ctx["adv"]
    nodes = {n["canonical"]: n for n in A["ledger_events"]}
    items = []
    # ---- 0. 규칙 결정(한 자리) — 승인하면 decisions/batch5-rule/ 의 같은 파일이 approved
    ev0 = []
    for d in decs:
        lr = [r["ref"] for r in d["source_refs"] if r["kind"] == "ledger"][:1]
        ev0 += [dict(x, note=f"{d['rule_id']} {d['target'].get('canonical') or d['target'].get('from_ref')} → {d['target'].get('into') or d['new_value'].get('to_id')}") for x in g.evs(lr)]
    pls = [dict(copy.deepcopy(d)) for d in decs]
    items.append(node("auto-rules", "fold_approve", f"규칙 자동 결정 {len(decs)}(접기 {len(folds)} · 줄임말 매핑 {sum(1 for m in maps if m['decision'])}) — 그대로 승인할까?",
                      "표기만 다른 것(띄어쓰기·전각·대소문자 · 원장 병기 X(Y) · 사전에 이미 있는 영문 동의어)의 접기와 줄임말 매핑(정식명 접두 · 후보 하나). ~감 · 형성/발생 처럼 뜻이 같은지가 임상 판단인 규칙은 여기 없다(규칙 묶음 자리). 승인하면 decisions/batch5-rule/ 의 파일이 approved 로 바뀌어 다음 빌드가 적용한다. 목록은 batch5-auto-folds.md.",
                      ev0, [OrderedDict([("key", "approve_all"), ("label", "전부 승인"), ("effect", f"접기 {len(folds)} · 매핑 {sum(1 for m in maps if m['decision'])} 이 다음 빌드에 적용"), ("builder_applies_now", True),
                                         ("decision_payload", None), ("decision_payloads", pls)]),
                            opt("keep", "승인하지 않는다(규칙 결정은 proposed 로 남는다)", "결정 없음", None, None)],
                      "approve_all", "표기만 다르다(원장 병기 · 표기 · 사전 영문 동의어) · 줄임말은 정식명 접두 후보 하나 — 원장이 같은 것을 다르게 적은 것이다.", {"rules": {k: v for k, v in RULES.items() if k in AUTO or k == "B5R-ABBR"}, "folds": folds, "maps": maps}))
    # ---- 1. 남는 ⑦ strong — 규칙 묶음(~감 · 형성/발생 · 기타)마다: 묶음 한 자리(전부 같다 / 전부 다르다 / 개별) + 쌍마다 개별 자리
    groups = OrderedDict([(k, []) for k in list(GROUPED) + ["OTHER"]])
    nnorm = {norm(x) for x in nodes}
    for c, a, b, changed, why in remain:
        gr = group_of.get(c["id"])
        if gr and not changed:
            rid, src, tgt = gr
            a, b = src, tgt                      # 규칙 방향(접미가 붙은 쪽 · 원장 노드가 접힌다)
            gk = rid
        else:
            gk = "OTHER"
        bk = "ledger" if norm(b) in nnorm else "dictionary"
        na, nb = nodes.get(a), nodes.get(b)
        ev = [dict(x, note=f"「{a}」 " + x.get("note", "")) for x in _examples(g, na["contexts"] if na else [])]
        if nb:
            ev += [dict(x, note=f"「{b}」 " + x.get("note", "")) for x in _examples(g, nb["contexts"])]
        refs = [g.src(l) for l in (na["locators"] if na else []) + (nb["locators"] if nb else [])]
        key = f"duplicate_candidate|adverse_event_type|{a}|{b}"
        pid = f"DEC-2026-11-05-B5-D-{_h(key)}"
        same = payload(pid, "fold_approve", OrderedDict([("dictionary", "adverse_event_type"), ("canonical", a), ("into", b)]), OrderedDict([("keep", b)]), f"결정 묶음 5 — ⑦ 「{a}」↔「{b}」 같다 · 「{b}」 유지", refs, [{"kind": "erd", "ref": key}])
        opts = [opt(f"same:keep:{b}", f"같다 — 접기(「{b}」 쪽 유지)", f"「{a}」는 「{b}」의 동의어 · 이 ⑦ resolved", same, True)]
        if bk == "ledger":
            opts.append(opt(f"same:keep:{a}", f"같다 — 접기(「{a}」 쪽 유지)", f"「{b}」는 「{a}」의 동의어 · 이 ⑦ resolved",
                            payload(pid, "fold_approve", OrderedDict([("dictionary", "adverse_event_type"), ("canonical", b), ("into", a)]), OrderedDict([("keep", a)]), f"결정 묶음 5 — ⑦ 「{a}」↔「{b}」 같다 · 「{a}」 유지", refs, [{"kind": "erd", "ref": key}]), True))
        ck = OrderedDict([("kind", "duplicate_candidate"), ("pair", key)]) if changed or gr else copy.deepcopy(c["stable_key"])
        diff = payload(pid, "conflict_close", OrderedDict([("conflict_key", ck)]), OrderedDict([("verdict", "not_same"), ("note", f"「{a}」 ≠ 「{b}」")]), f"결정 묶음 5 — ⑦ 「{a}」↔「{b}」 다르다", refs, [{"kind": "erd", "ref": key}])
        opts.append(opt("different", "다르다", "둘 다 유지 — 이 ⑦ dismissed(not_same)", diff, True))
        opts.append(opt("hold", "보류", "결정 없음(⑦ open 그대로)", None, None))
        groups[gk].append((node(f"dup-{gk}/{_h(key)}", "duplicate_candidate", f"⑦ 「{a}」 ↔ 「{b}」 — 같은가?",
                                f"{why} · 표기 규칙 {', '.join(c['pair']['rules'])}" + (f" · 규칙 접기 뒤 쌍(원래 「{c['pair']['node']}」↔「{c['pair']['other']}」)" if changed else ""),
                                ev, opts, None, "뜻이 같은지는 임상 판단 — 사람이 본다(추천 없음 · 묶음 자리에서 한 번에 고를 수 있다).",
                                OrderedDict([("pair", OrderedDict([("node", a), ("other", b), ("other_kind", bk), ("rules", c["pair"]["rules"])])), ("from_conflict", c["id"]), ("after_rule_folds", changed)])), same, diff))
    titles = dict(GROUPED, OTHER="기타(낱말 포함 · ~증 · 자모 등 — 뜻이 다를 수 있는 쌍)")
    for gk, rows in groups.items():
        if not rows:
            continue
        leaves = [x[0] for x in rows]
        sames = [copy.deepcopy(x[1]) for x in rows]
        diffs = [copy.deepcopy(x[2]) for x in rows]
        srcs = Counter(x["target"]["canonical"] for x in sames)
        consistent = gk != "OTHER" and all(v == 1 for v in srcs.values())
        gopts = []
        if consistent:
            gopts.append(OrderedDict([("key", "all_same"), ("label", f"전부 같다({len(rows)} 쌍 접기 · 규칙 방향)"), ("effect", "쌍마다 「접미가 붙은 쪽 → 바탕」 접기(fold_approve) · 사전 사건은 접히지 않는다"),
                                      ("builder_applies_now", True), ("decision_payload", None), ("decision_payloads", sames)]))
        gopts.append(OrderedDict([("key", "all_different"), ("label", f"전부 다르다({len(rows)} 쌍)"), ("effect", "쌍마다 ⑦ dismissed(conflict_close not_same)"), ("builder_applies_now", True), ("decision_payload", None), ("decision_payloads", diffs)]))
        gopts.append(opt("individual", "개별 — 아래 쌍 자리에서 하나씩", "이 자리는 결정 없음(쌍 자리 답이 결정이 된다)", None, None))
        grp_leaf = node(f"dup-{gk}/all", "duplicate_candidate", f"⑦ {titles[gk]} {len(rows)} 쌍 — 한 번에 고를까?",
                        f"규칙 {gk if gk != 'OTHER' else '없음'} · 쌍 목록은 이 묶음의 개별 자리" + ("" if consistent or gk == "OTHER" else " · 같은 노드가 둘 이상으로 접혀 「전부 같다」는 뺐다"),
                        [], gopts, None, "규칙이 표기는 맞아도 뜻이 같은지는 임상 판단 — 사용자가 고른다(추천 없음). 묶음 자리와 개별 자리를 함께 답하면 apply_gate 가 같은 쌍 다른 답을 거부한다.",
                        {"pairs": [[x[0]["pair"]["node"], x[0]["pair"]["other"]] for x in rows]})
        items.append(node(f"dup-{gk}", "duplicate_candidate", f"⑦ strong — {titles[gk]} {len(rows)} 쌍", "규칙 단위 묶음 + 쌍마다 개별 자리.", [], [], None, "묶음 자리 또는 개별 자리", {"subitems": [grp_leaf] + leaves}))
    # ---- 2. 씨앗 — 사전별 일괄 한 자리
    seeds = json.load(open(seeds_path, encoding="utf-8"))
    for grp, dname, title in (("site", "site", "부위"), ("ingredient_material", "ingredient_material", "성분"), ("product_abbrev", "product_name", "줄임말·옛 이름")):
        rows = [r for r in seeds["seeds"][grp]["rows"] if r.get("status") == "proposed"]
        if grp == "product_abbrev":
            keep = {(r["fragment"], r["product"]) for r, _ in abbr_rest}
            rows = [r for r in rows if (r["fragment"], r["product"]) in keep]
        adds, excls, ev = [], OrderedDict(), []
        for r in rows:
            val = r.get("value") or f"{r['fragment']}→{r['product']}"
            key = f"{grp}|{r.get('value') or r.get('fragment')}|{r.get('product', '')}"
            pid = f"DEC-2026-11-05-B5-S-{_h(key)}"
            refs = [g.src(l) for l in r.get("locators") or []]
            if grp == "site":
                nv = OrderedDict([("canonical", r["value"]), ("synonyms", [x["value"] for x in r.get("synonyms", []) if x.get("n")]), ("category", None), ("kind", r["kind"]), ("parent", r.get("parent"))])
            elif grp == "ingredient_material":
                nv = OrderedDict([("canonical", r["value"]), ("synonyms", []), ("category", None)])
            else:
                pe = next((e for e in g.dicts["product_name"]["entries"] if norm(e["canonical"]) == norm(r["product"])), None)
                nv = OrderedDict([("canonical", r["product"]), ("synonyms", [r["fragment"]]), ("category", None)])
                if pe is not None and pe.get("code") is not None:
                    nv["code"] = pe.get("code")
                if r.get("product_origin") == "taxonomy":
                    nv["origin"] = "taxonomy"
            p_add = payload(pid, "dictionary_add", OrderedDict([("dictionary", dname)]), nv, f"결정 묶음 5 — 씨앗 일괄 승인({title}) 「{val}」(erd-v3.2-seed-candidates.json)", refs, [{"kind": "erd", "ref": f"{SEED_FILE}#seeds/{grp}"}])
            p_add["seed_value"] = val
            p_no = payload(pid, "scope_review", OrderedDict([("erd_ref", f"{SEED_FILE}#seeds/{grp}"), ("review_item", val)]), OrderedDict([("disposition", f"씨앗 제외 — {title} 사전에 넣지 않는다")]),
                           f"결정 묶음 5 — 씨앗 제외({title}) 「{val}」 — 기록만", refs, [{"kind": "erd", "ref": f"{SEED_FILE}#seeds/{grp}"}])
            adds.append(p_add)
            excls[val] = p_no
            ev += [dict(x, note=f"「{val}」 " + (r.get("basis") or r.get("rule") or r.get("kind") or "") + f" · 원장 {r['n']} 자리") for x in g.evs((r.get("locators") or [])[:1])]
        o_all = OrderedDict([("key", "approve_all"), ("label", "전부 승인"), ("effect", f"{title} {len(adds)} 값 전부 사전에(dictionary_add)"), ("builder_applies_now", True), ("decision_payload", None), ("decision_payloads", adds)])
        o_sel = OrderedDict([("key", "select"), ("label", "제외할 것 선택"), ("effect", "answers 에 {\"choice\": \"select\", \"exclude\": [값 …]} — 고른 값은 제외 기록(scope_review) · 나머지는 승인"), ("builder_applies_now", True),
                             ("decision_payload", None), ("decision_payloads", adds), ("exclude_payloads", excls)])
        why = {"site": seeds["seeds"]["site"].get("why_closed"), "ingredient_material": seeds["seeds"]["ingredient_material"].get("why_not_auto")}.get(grp) or \
            "줄임말 후보 둘 이상(리쥬란 · 울트라 · 피코)과 「조각이 제품명을 접두로 포함」 — 정식명 접두 · 후보 하나는 규칙 B5R-ABBR 로 자동"
        items.append(node(f"seed-{grp}", "dictionary_add", f"씨앗 — {title} {len(adds)} 일괄 승인?", why, ev, [o_all, o_sel], None, "씨앗은 승인 절차 — 원장이 값을 선언하지 않는다(추천 없음).",
                          {"table": [OrderedDict([("value", a["seed_value"]), ("new_value", a["new_value"]), ("locators", len([r for r in a["source_refs"] if r["kind"] == "ledger"]))]) for a in adds]}))
    # ---- 3. 묶음 3 미결 그대로
    b3p = os.path.join(out_dir, "gate", "batch3.json")
    items += batch3_items(g, S, json.load(open(b3p, encoding="utf-8")) if os.path.exists(b3p) else [])
    for it, s_ in leaves_of(items):
        for o in s_["options"]:
            for p_ in ([o["decision_payload"]] if o.get("decision_payload") else []) + list(o.get("decision_payloads") or []) + list((o.get("exclude_payloads") or {}).values()):
                errs = [e for e in validate(dict(p_, decided_by="x")) if "decided_by" not in e]
                if errs:
                    raise AssertionError(f"{s_['id']} {o['key']}: {errs}")
    if g.read_fail:
        raise AssertionError(f"원장 읽기 실패 {len(g.read_fail)}: {g.read_fail[:5]}")
    gd = os.path.join(out_dir, "gate")
    write_json(os.path.join(gd, "batch5-reduced.json"), items)
    write_json(os.path.join(gd, "batch5-rule-decisions.json"), [{k: v for k, v in d.items() if k != "_store"} for d in decs])
    write_text(os.path.join(gd, "batch5-reduced.md"), render(items, folds, maps))
    write_text(os.path.join(gd, "batch5-auto-folds.md"), auto_md(folds, maps, abbr_rest))
    write_text(os.path.join(gd, "batch5-nodes.md"), nodes_md(g, S))
    if propose_dir:
        os.makedirs(propose_dir, exist_ok=True)
        for d in decs:
            path = os.path.join(propose_dir, d["id"] + ".json")
            body = {k: v for k, v in d.items() if k != "_store"}
            if os.path.exists(path) and json.load(open(path, encoding="utf-8")).get("status") != "proposed":
                continue   # 사람이 바꾼 파일은 덮지 않는다
            write_json(path, body)
    lv = list(leaves_of(items))
    return {"leaves": len(lv), "by_item": OrderedDict((it["id"], len(it.get("subitems") or [it])) for it in items), "auto_folds": len(folds), "folds_by_rule": dict(Counter(f["rule"] for f in folds)),
            "abbrev_maps": sum(1 for m in maps if m["decision"]), "abbrev_skipped": sum(1 for m in maps if not m["decision"]), "strong_remaining": sum(len(it["subitems"]) - 1 for it in items if it["id"].startswith("dup-")), "groups": OrderedDict((it["id"], len(it["subitems"]) - 1) for it in items if it["id"].startswith("dup-")), "read_fail": len(g.read_fail), "rule_decisions": len(decs)}


def render(items, folds, maps):
    lv = list(leaves_of(items))
    o = ["# 결정 묶음 5 축소본 — 사람이 볼 것만(규칙 자동 결정은 한 자리)", "",
         f"고를 자리 {len(lv)}. 원본 `batch5.json`(432 자리)은 그대로 — 어느 쪽을 쓸지는 사용자가 정한다. 원장 사건 노드는 게이트에서 뺐다(원장 칸 safety·complications 이름이 「부작용」이라고 말한다 · unreviewed 그대로 · 목록 `batch5-nodes.md`). "
         "고른 답 → `python3 apply_gate.py --gate out/gate/batch5-reduced.json --answers answers.json`(씨앗 「제외할 것 선택」은 {\"choice\": \"select\", \"exclude\": [값 …]}).", "",
         md_table(["묶음", "자리", "비고"], [(it["id"], len(it.get("subitems") or [it]), it["title"]) for it in items]), "",
         f"## auto-rules — 규칙 자동 결정(접기 {len(folds)} · 줄임말 매핑 {sum(1 for m in maps if m['decision'])})", "", "목록 `batch5-auto-folds.md`. 승인하면 decisions/batch5-rule/ 의 같은 id 파일이 approved.", ""]
    for it in items:
        if it["id"].startswith("dup-"):
            g0, pairs = it["subitems"][0], it["subitems"][1:]
            o += [f"## {it['id']} — {it['title']}", "", f"묶음 자리 `{g0['id']}` 옵션: " + " · ".join(f"`{x['key']}` {x['label']}" for x in g0["options"]), "",
                  md_table(["#", "개별 자리", "노드(접히는 쪽)", "상대", "표기 규칙", "규칙 접기 뒤"], [(i + 1, s["id"], s["pair"]["node"], s["pair"]["other"], ", ".join(s["pair"]["rules"]), "○" if s["after_rule_folds"] else "") for i, s in enumerate(pairs)]), ""]
        elif it["id"].startswith("seed-"):
            o += [f"## {it['id']} — {it['title']}", "", it["why"], "", md_table(["#", "값", "사전 값(new_value)", "원장 자리"], [(i + 1, r["value"], json.dumps(r["new_value"], ensure_ascii=False)[:90], r["locators"]) for i, r in enumerate(it["table"])]), ""]
        elif it["id"] not in ("auto-rules",):
            for s in (it.get("subitems") or [it]):
                o += [f"## {s['id']} — {s['title']}", "", md_table(["옵션", "뜻", "결정"], [(x["key"], x["label"], (f"{x['decision_payload']['kind']} `{x['decision_payload']['id']}`" if x.get("decision_payload") else "결정 없음")) for x in s["options"]]),
                      f"\n추천: **{s['recommended'] or '—'}** — {s['recommend_reason']}", ""]
    return "\n".join(o)


def auto_md(folds, maps, abbr_rest):
    o = ["# 결정 묶음 5 — 규칙 자동 결정 목록(decisions/batch5-rule/ · proposed · decided_by=rule:<id>)", "",
         "자동 규칙(표기만 다른 것): " + " · ".join(f"**{k}** {v}" for k, v in RULES.items() if k in AUTO or k == "B5R-ABBR") +
         " — 「~감」(B5R-A) · 「형성/발생」(B5R-E)은 뜻이 같은지가 임상 판단이라 자동 적용하지 않고 축소본 규칙 묶음 자리(dup-B5R-A · dup-B5R-E)로 갔다.", "",
         f"## 접기 {len(folds)}", "", md_table(["#", "규칙", "접히는 노드", "접힐 곳", "종류", "⑦ 쌍", "표기 규칙", "원장 자리", "결정"],
                                             [(i + 1, f["rule"], f["node"], f["into"], f["into_kind"], " ↔ ".join(f["pair"]), ", ".join(f["rules"]), f["locators"], f["decision"]) for i, f in enumerate(folds)]), "",
         f"## 줄임말 매핑(B5R-ABBR) {sum(1 for m in maps if m['decision'])} · 만들지 않음 {sum(1 for m in maps if not m['decision'])}", "",
         md_table(["조각", "제품", "결정", "scope(미해결 참조)", "만들지 않은 사유"], [(m["fragment"], m["product"], m["decision"] or "—", len(m.get("scope") or []), m.get("why") or "") for m in maps]), "",
         f"## 줄임말 — 게이트에 남긴 것 {len(abbr_rest)}", "", md_table(["조각", "제품", "사유"], [(r["fragment"], r["product"], why) for r, why in abbr_rest])]
    return "\n".join(o)


def nodes_md(g, S):
    A = S.ctx["adv"]
    nodes = sorted(A["ledger_events"], key=lambda n: (-len(n["locators"]), n["canonical"]))
    o = ["# 원장 사건 노드(참고 · 게이트 아님)", "",
         f"{len(nodes)} 노드 — 원장 칸(safety.common/serious/long_term … · complications 이름)이 「부작용」이라고 말한 핵심어. status=unreviewed 그대로 · 종류(category) 미분류 허용(코디 지시 2026-11-05).", "",
         md_table(["#", "노드", "id", "원장 횟수", "계열", "원문 예(최대 3)"],
                  [(i + 1, n["canonical"], n["id"], len(n["locators"]), ", ".join(dedupe(c.get("modality") for c in n["contexts"] if c.get("modality"))),
                    " / ".join(f"「{str(c.get('text'))[:40]}」" for c in list({c.get('text'): c for c in n["contexts"]}.values())[:3])) for i, n in enumerate(nodes)])]
    return "\n".join(o)
