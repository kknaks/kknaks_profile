# -*- coding: utf-8 -*-
"""결정 묶음 6 게이트 자료 — ERD v3.3 · 8차 뒤 남는 자리(발주서 silver-build-8-brief.md §4).

out/gate/batch6.json(2B 스키마 · 웹 페이지 입력) · batch6.md(사람 읽기) · batch6-weak.json(⑦ weak — 게이트에 올리지 않음).
묶음(자리 수는 묶음별로 센다 · 추천은 원장이 말할 때만):
  ledger-nodes        새 사건 노드(정식 노드 · 종류 질문 없음 · 목록만 — 옵션 없음)
  dup-strong          ⑦ strong 쌍(접미사 20 닫힌 뒤 남은 open) — 같은 사건(어느 쪽 유지 · 나머지 말은 속성·문구 보존) / 다른 사건 / 보류 · 원장 병기 「X(Y)」만 추천
  sentence-b          문장꼴(b) — 분석기가 절로 본 토막만 있는 문구(노드 없음 · status=sentence) — 메모(phrase_map units []) / 부작용(단위 지정 · 사용자) / 보류
  ambiguous           애매 — 분석기 판정 애매(ANOM · T1-pred · T1-none · T1-partial · T3 tie) · 노드에 규칙 밖 명사가 붙은 것
  occlusion-embolism  폐색 ≠ 색전 — 한 문구에 둘이 같이 나온 자리(지금 둘 다 단위 · 확인만)
  r30-candidates      R30 leads_to 후보(색전 → 폐색 · 폐색 → 괴사 · edge_create · 사용자)
  batch3              결정 묶음 3 미결(out/gate/batch3.json 그대로 · 공기색전 v3.2 갱신 — gate5 와 같다)
  r1-candidates       R1 후보(새) — 관형어·부사어 하나로 뗀 말 중 R1 목록·수식어 138 밖(ERD 규칙 데이터 변경 · scope_review 기록)
  mxx-prefix          synergy 「Mxx-」 접두 라벨(원장 4판 후보 · 결정 아님)
decision_payload = 그 옵션을 고르면 만들어질 결정 파일 본문(status=proposed) — `python3 apply_gate.py --gate out/gate/batch6.json --out decisions/batch6/ --answers answers.json`.
"""
import copy
import json
import os
import re
from collections import Counter, OrderedDict, defaultdict

from .decisions import validate
from .gate2b import G, node
from .gate3 import leaves_of, opt
from .gate5 import G5, batch3_items, _examples, _where, paren_outer
from .util import dedupe, md_table, mkid, norm, write_json, write_text

BATCH = "DEC-2026-11-06-B6"
BATCH_NOTE = "결정 묶음 6 (게이트 out/gate/batch6.json · ERD v3.3 · 8차 뒤 남는 자리 — 새 노드 · ⑦ strong · 문장꼴(b) · 애매 · 폐색/색전 · R30 · 묶음 3 · R1 후보 · Mxx-)"
ERD_REF = "erd-v3.3.md §0.2 · §1.3 · §1.5 · §5 · §12"
AMBIG_KINDS = ("ANOM", "T1-pred", "T1-none", "T1-partial")


def _h(s):
    return mkid("X", s)[2:]


def payload(pid, kind, target, new_value, reason, ledger_refs, extra_refs=()):
    refs, seen = [], set()
    for r in [{"kind": "ledger", "ref": x} for x in ledger_refs] + [{"kind": "erd", "ref": ERD_REF}, {"kind": "brief", "ref": "silver-build-8-brief.md §4"}] + list(extra_refs):
        k = (r["kind"], r["ref"])
        if k not in seen:
            seen.add(k)
            refs.append(OrderedDict([("kind", r["kind"]), ("ref", r["ref"])]))
    return OrderedDict([("id", pid), ("kind", kind), ("target", target), ("new_value", new_value), ("reason", reason), ("decided_by", None), ("decided_at", None),
                        ("status", "proposed"), ("source_refs", refs), ("batch", BATCH_NOTE)])


# =====================================================================================
# 1. 새 사건 노드 — 목록만
# =====================================================================================
def node_items(g, S, strong_by_node, amb_by_node, solo):
    A = S.ctx["adv"]
    nodes = sorted(A["ledger_events"], key=lambda n: (-len(n["locators"]), n["canonical"]))
    ent_of = defaultdict(list)
    for e in A["phrase_dictionary"]:
        for ev in e.get("ledger_events") or []:
            ent_of[ev].append(e)
    name_of = defaultdict(list)
    for r in A["complications"]:
        for sp in r.get("spans") or []:
            if sp[0] == "event":
                name_of[sp[1]].append(r)
    subs = []
    for n in nodes:
        nm = n["canonical"]
        ctxs = n["contexts"]
        where = _where(ctxs)
        ev = _examples(g, ctxs)
        ents = ent_of.get(nm, [])
        names = name_of.get(nm, [])
        subs.append(node(f"node/{n['id']}", "ledger_event", f"새 사건 노드 「{nm}」",
                         f"핵심어 「{nm}」 · 원장 {len(n['locators'])} 자리 · 계열 {', '.join(where['modalities']) or '—'} · 문구 사전 {len(ents)} 항목 · 이름 {len(names)} · 단독 출현 {solo.get(norm(nm), 0)}" +
                         (f" · ⑦ strong 상대 {', '.join(strong_by_node[nm])}" if strong_by_node.get(nm) else "") + (f" · 애매: {' / '.join(amb_by_node[nm])}" if amb_by_node.get(nm) else ""),
                         ev, [], None, "정식 노드(사용자 2026-11-06 — 종류 질문 없음 · 목록만). 결정은 ⑦ strong(dup-strong)·애매(ambiguous) 자리에서.",
                         OrderedDict([("node", OrderedDict([("id", n["id"]), ("canonical", nm), ("core_tokens", n.get("core_tokens")), ("n_locators", len(n["locators"])), ("locators", n["locators"]), ("where", where),
                                                            ("phrase_entries", [e["id"] for e in ents]), ("names", [r["locator"] for r in names]), ("solo_strict", solo.get(norm(nm), 0)),
                                                            ("strong_partners", strong_by_node.get(nm, [])), ("ambiguous", amb_by_node.get(nm, []))])), ("ask", False)])))
    return node("ledger-nodes", "ledger_event", f"새 사건 노드 {len(subs)} — 정식 노드 · 목록만(질문 없음)",
                "V3.2-0 노드 원칙 + V3.3-B 분석기: 부작용 문구의 토막에 사전 사건이 0 이면 핵심어(명사 · 명사형 어절)가 새 사건 노드다. 사용자 2026-11-06: 종류(category) 질문은 없다(원장 출처 0) · 노드는 정식 노드.",
                [], [], None, "목록만", {"subitems": subs, "ask": False})


# =====================================================================================
# 2. ⑦ strong
# =====================================================================================
def dup_items(g, S, strong):
    A = S.ctx["adv"]
    nodes = {n["canonical"]: n for n in A["ledger_events"]}
    ev_dict = {norm(e["canonical"]): e for e in g.dicts["adverse_event_type"]["entries"] if e.get("origin") != "ledger"}
    subs = []
    for c in strong:
        d = c["pair"]
        a, b, bk = d["node"], d["other"], d["other_kind"]
        na = nodes.get(a)
        ev = [dict(x, note=f"「{a}」 " + x.get("note", "")) for x in _examples(g, na["contexts"] if na else [])]
        refs = [g.src(l) for l in (na["locators"] if na else [])]
        if bk == "ledger":
            nb = nodes.get(b)
            ev += [dict(x, note=f"「{b}」 " + x.get("note", "")) for x in _examples(g, nb["contexts"] if nb else [])]
            refs += [g.src(l) for l in (nb["locators"] if nb else [])]
            bdesc = f"원장 노드 「{b}」 원장 {len(nb['locators']) if nb else 0} 자리"
        else:
            e = ev_dict.get(norm(b)) or {}
            bdesc = f"사전 사건 「{b}」(동의어 {', '.join(s_['value'] for s_ in e.get('synonyms', [])[:6]) or '없음'})"
        pid = f"{BATCH}-D-{_h(d['erd_key'])}"
        short, long_ = (a, b) if len(norm(a)) <= len(norm(b)) else (b, a)
        opts = []
        # 같은 사건 — X 유지(Y 는 동의어 · Y 의 나머지 말은 속성·문구 raw_variants 보존)
        for keep in (short, long_):
            other = b if keep == a else a
            other_is_node = other in nodes
            if other_is_node:
                pl = payload(pid, "fold_approve", OrderedDict([("dictionary", "adverse_event_type"), ("canonical", other), ("into", keep)]), OrderedDict([("keep", keep)]),
                             f"결정 묶음 6 — ⑦ strong 「{a}」 ↔ 「{b}」 같은 사건 · 「{keep}」 유지(규칙 {', '.join(d['rules'])}) · 「{other}」 는 그 동의어(원문은 raw_variants 보존)", refs, [{"kind": "erd", "ref": d["erd_key"]}])
                eff = f"「{other}」 노드 자리 전부 「{keep}」 단위로 · 이 ⑦ resolved" + (" · 긴 쪽의 남는 말은 속성(수식어·부위)으로 분해되지 않고 문구 사전 raw_variants 에만 남는다(속성 분해는 결정 kind 없음 · ERD 질문)" if keep == short else "")
                opts.append(opt(f"same:keep:{keep}", f"같은 사건 — 「{keep}」 유지({'짧은 쪽' if keep == short else '긴 쪽이 사건'})", eff, pl, True))
            else:
                opts.append(opt(f"same:keep:{keep}", f"같은 사건 — 「{keep}」 유지({'짧은 쪽' if keep == short else '긴 쪽이 사건'}) · 결정 kind 없음", f"사전 사건 「{other}」 를 노드 「{keep}」 에 접는 kind 가 없다(canonical_rename 은 이름만 바꾼다) — ERD 질문", None, None))
        opts.append(opt("different", "다른 사건", "둘 다 유지 — 이 ⑦ dismissed(close_verdict not_same)",
                        payload(pid, "conflict_close", OrderedDict([("conflict_key", copy.deepcopy(c["stable_key"]))]), OrderedDict([("verdict", "not_same"), ("note", f"「{a}」 ≠ 「{b}」")]),
                                f"결정 묶음 6 — ⑦ strong 「{a}」 ↔ 「{b}」 다르다(not_same)", refs, [{"kind": "erd", "ref": d["erd_key"]}]), True))
        opts.append(opt("hold", "보류", "결정 없음(⑦ open 그대로)", None, None))
        rec, why = None, "표기 규칙만 맞는 후보 — 같은 것인지는 원장이 말하지 않는다(추천 없음)."
        if "paren_pair" in d["rules"]:
            outer = b if bk == "dictionary" else paren_outer(g.L, a, b)
            if outer:
                rec, why = f"same:keep:{outer}", f"원장이 「{a}」와 「{b}」를 병기 「X(Y)」로 적었다 — 같은 것 · 괄호 밖 본 표기 「{outer}」 쪽 유지."
        subs.append(node(f"dup/{_h(d['erd_key'])}", "duplicate_candidate", f"⑦ 「{a}」 ↔ 「{b}」 — 같은 사건인가?",
                         f"원장 노드 「{a}」 원장 {len(na['locators']) if na else 0} 자리 ↔ {bdesc} · 규칙 {', '.join(d['rules'])}(strong) · 안정 키 {d['erd_key']}",
                         ev, opts, rec, why, OrderedDict([("pair", d), ("conflict_id", c["id"]), ("stable_key", c["stable_key"])])))
    return node("dup-strong", "duplicate_candidate", f"⑦ strong {len(subs)} 쌍 — 같은 사건(어느 쪽 유지) / 다른 사건 / 보류",
                "V3.2-0 ⑦ 노드끼리 · strong = 원장 병기 X(Y) · 접미 감각(사용자 결정 없음) · 짧은 쪽이 긴 쪽의 낱말 · 자모 1 치환. 접미사 ~감·~증·~형성 쌍 20 은 결정 6-A 로 닫혔다(resolved · 여기 없음).",
                [], [], None, "하위 항목마다(원장 병기 쌍만 추천)", {"subitems": subs})


# =====================================================================================
# 3. 문장꼴(b) · 4. 애매
# =====================================================================================
def phrase_items(g, S, kind_key, item_id, title, why_text):
    AU = S.ctx["AU"]
    subs = []
    for pid, e in AU.phrases.items():
        if e["status"] != "sentence":
            continue
        w = e.get("why") or {}
        if w.get("analyzer") != kind_key:
            continue
        locs = [c["locator"] for c in e["contexts"]]
        ev = [g.ev(l, f"원문 · {c.get('kind')} · {c.get('modality')}") for l, c in zip(locs[:3], e["contexts"][:3])]
        refs = [g.src(l) for l in locs]
        an = (e.get("parsed") or {}).get("analyzer") or []
        segs = [OrderedDict([("segment", x["segment"]), ("kind", x["kind"]), ("rules", x["rules"]), ("amb", x.get("amb"))]) for x in an]
        hint = dedupe(x.get("remainder_hint") for x in S.ctx["AU"].A["AT"].seglog if x["locator"] in locs and x.get("remainder_hint")) if hasattr(S.ctx["AU"].A["AT"], "seglog") else []
        dpid = f"{BATCH}-P-{pid[4:]}"
        opts = [opt("memo", "부작용 아님 → 메모(phrase_map units [])", "문구 사전 항목 status approved · 단위 없음 — R15 에 오르지 않는다",
                    payload(dpid, "phrase_map", OrderedDict([("phrase_id", pid)]), OrderedDict([("units", []), ("courses", None), ("status", "approved")]),
                            f"결정 묶음 6 — {title} 「{e['raw_variants'][0]}」 는 부작용 문구가 아니다(메모)", refs), True),
                opt("adverse", "부작용 — 단위 지정(사용자가 units 를 적는다 · 세 칸 사전 값)", "phrase_map(units=[(사건, 부위, 물질) …]) — 지정값은 사전 값이어야 한다 · 여기서는 본문을 만들지 않는다", None, None),
                opt("hold", "보류", "결정 없음(status sentence 그대로 · 노드 없음)", None, None)]
        subs.append(node(f"{item_id}/{pid}", "phrase_dictionary", f"{title} 「{e['raw_variants'][0][:60]}」",
                         f"자리 {len(locs)} · 분석기 토막 {len(segs)} · 행선지 힌트 {', '.join(hint) or '—'}(낱말 목록 · 추천 아님) · 판정 {', '.join(w.get('analyzer_kinds') or [])}",
                         ev, opts, None, "행선지(타임라인·고지·설명문·부작용)는 원장이 말하지 않는다 — 추천 없음.",
                         OrderedDict([("phrase_id", pid), ("normalized", e["normalized"]), ("raw_variants", e["raw_variants"]), ("locators", locs), ("segments", segs), ("hint", hint)])))
    return node(item_id, "phrase_dictionary", f"{title} {len(subs)} — 메모 / 부작용(단위 지정) / 보류", why_text, [], [], None, "하위 항목마다", {"subitems": subs})


def ambiguous_node_items(g, S, amb_by_node, strong_by_node):
    A = S.ctx["adv"]
    nodes = {n["canonical"]: n for n in A["ledger_events"]}
    subs = []
    for nm, reasons in sorted(amb_by_node.items(), key=lambda kv: (-len(nodes[kv[0]]["locators"]) if kv[0] in nodes else 0, kv[0])):
        n = nodes.get(nm)
        if n is None:
            continue
        ev = _examples(g, n["contexts"])
        refs = [g.src(l) for l in n["locators"]]
        pid = f"{BATCH}-A-{n['id'][4:]}"
        opts = [opt("keep", "노드 그대로", "결정 없음", None, None),
                opt("not_adverse", "부작용 아님 → 메모", "노드를 세우지 않는다(토큰은 explanation 보존) · 이 노드만 사건인 문구는 메모(note)",
                    payload(pid, "exclude", OrderedDict([("kind", "dictionary_value"), ("key", OrderedDict([("dictionary", "adverse_event_type"), ("canonical", nm)]))]), OrderedDict([("excluded", True)]),
                            f"결정 묶음 6 — 애매 노드 「{nm}」 는 부작용이 아니다 → 메모", refs), True)]
        for other in strong_by_node.get(nm, []):
            opts.append(opt(f"fold:{other}", f"접기 → 「{other}」(⑦ strong 상대)", f"「{nm}」 는 「{other}」 의 동의어",
                            payload(pid, "fold_approve", OrderedDict([("dictionary", "adverse_event_type"), ("canonical", nm), ("into", other)]), OrderedDict([("keep", other)]),
                                    f"결정 묶음 6 — 애매 노드 「{nm}」 를 「{other}」 에 접는다", refs), True))
        subs.append(node(f"ambiguous/node/{n['id']}", "ledger_event", f"애매 노드 「{nm}」", f"원장 {len(n['locators'])} 자리 · 애매: " + " / ".join(reasons), ev, opts, None,
                         "규칙 밖(사전 사건에 R1·R2 밖 명사가 붙음 · 괄호 안 절반) — 원장이 말하지 않는다(추천 없음).", OrderedDict([("node", OrderedDict([("id", n["id"]), ("canonical", nm), ("locators", n["locators"]), ("ambiguous", reasons)]))])))
    return subs


# =====================================================================================
# 5. 폐색/색전 · 6. R30 후보
# =====================================================================================
CAUSAL = re.compile(r"인한|의한|으로 인|일으킬|일으키|유발|이어질|이어지|→|로 인해|때문")


def occlusion_items(g, S, erd):
    AU = S.ctx["AU"]
    from .v32 import CUR
    texts = [(ax, kind, lc, text) for ax, kind, f, p, lc, text, mod in (CUR.get("texts") or []) if ax == "adverse"]
    ev_by_loc = defaultdict(list)
    for e in AU.phrases.values():
        for c in e["contexts"]:
            for u in e["units"]:
                ev_by_loc[c["locator"]].append(AU.units[u]["event"] if u in AU.units else u)
    for lc, uids in AU.name_units.items():
        for u in uids:
            ev_by_loc[lc].append(AU.units[u]["event"] if u in AU.units else u)
    co, r30 = [], []
    rules = erd["tuple_rules"]["adverse"].get("r30_candidate_rules") or []
    for ax, kind, lc, text in texts:
        t = str(text)
        if "폐색" in t and "색전" in t:
            co.append((lc, t, dedupe(ev_by_loc.get(lc, [])), bool(re.search(r"폐색\s*/\s*색전|색전\s*/\s*폐색", t))))
        for r in rules:
            if any(w in t for w in r["from_words"]) and any(w in t for w in r["to_words"]):
                r30.append((f"{r['from']}→{r['to']}", lc, t, bool(CAUSAL.search(t))))
    subs = []
    for lc, t, evs, slash in co:
        subs.append(node(f"occlusion/{_h(lc)}", "adverse_effect", f"폐색 ≠ 색전 — 「{t[:50]}」", f"사건 {', '.join(evs) or '—'} · `/` 대안 {slash} · 한 단위로 접힌 것 0(V3.3-C(3))",
                         [g.ev(lc, "원문")], [opt("both", "지금대로(두 사건 · 접지 않음)", "결정 없음", None, None), opt("hold", "보류", "결정 없음", None, None)], None,
                         "사용자 2026-11-06 폐색 ≠ 색전 — 확인만(추천 없음).", OrderedDict([("locator", lc), ("events", evs), ("slash", slash)])))
    occ = node("occlusion-embolism", "adverse_effect", f"폐색 ≠ 색전 — 한 문구에 둘 {len(subs)}", "V3.3-C(3): 접지 않고 동의어로도 두지 않는다 · 「혈관폐색/색전」의 `/` 는 대안.", [], [], None, "하위 항목마다", {"subitems": subs})
    by = defaultdict(list)
    for key, lc, t, causal in r30:
        by[key].append((lc, t, causal))
    subs2 = []
    for key, rows in by.items():
        fr, to = key.split("→")
        pid = f"{BATCH}-R30-{_h(key)}"
        refs = [g.src(lc) for lc, _, _ in rows]
        pl = payload(pid, "edge_create", OrderedDict([("relation", "R30"), ("from_ref", OrderedDict([("kind", "adverse_tuple"), ("tuple", OrderedDict([("event", fr), ("site", "none"), ("qualifier", "none")]))])),
                                                      ("to_ref", OrderedDict([("kind", "adverse_tuple"), ("tuple", OrderedDict([("event", to), ("site", "none"), ("qualifier", "none")]))]))]),
                     OrderedDict([("attrs", OrderedDict([("basis", "edge_create"), ("source_locators", [lc for lc, _, _ in rows])]))]),
                     f"결정 묶음 6 — R30 leads_to {fr} → {to}(원장 한 문구에 두 사건 말 · 인과 표지 {sum(1 for _, _, c in rows if c)}/{len(rows)})", refs)
        subs2.append(node(f"r30/{_h(key)}", "edge_create", f"R30 leads_to 후보 {fr} → {to}", f"원장 자리 {len(rows)} · 인과 표지 있는 자리 {sum(1 for _, _, c in rows if c)}",
                          [g.ev(lc, "인과 표지 " + ("예" if c else "—")) for lc, _, c in rows[:8]],
                          [opt("approve", "edge_create R30 approved", f"adverse_effect({fr}, none, none) → ({to}, none, none) 엣지 1(양끝 단위가 있어야 한다 · 없으면 결정이 세운다)", pl, True), opt("hold", "보류", "결정 없음(R30 엣지 0)", None, None)],
                          None, "원장은 인과를 구조화하지 않았다 — 제안만(ERD §9.20 · §12-10 · 추천 없음).", OrderedDict([("pair", key), ("rows", [OrderedDict([("locator", lc), ("text", t), ("causal_marker", c)]) for lc, t, c in rows])])))
    r30i = node("r30-candidates", "edge_create", f"R30 leads_to 후보 {len(subs2)}(자리 {len(r30)})", "ERD v3.3 §9.20 R30 후보 — edge_create 는 사용자(§12-10).", [], [], None, "하위 항목마다", {"subitems": subs2})
    return occ, r30i


# =====================================================================================
# 7. R1 후보 · 8. Mxx-
# =====================================================================================
def r1_candidate_items(g, S, erd):
    from .adverse33 import analyzer_texts, word_info
    from .v32 import CUR
    AT = S.ctx["AU"].A["AT"]
    an = getattr(AT, "an", None)
    if an is None:
        return node("r1-candidates", "scope_review", "R1 후보 0", "분석기 없음", [], [], None, "—", {"subitems": []})
    stop = {norm(w["word"]) for w in erd["tuple_rules"]["adverse"]["adverse_stopwords"]["words"]}
    cnt, ex, locs = Counter(), {}, defaultdict(list)
    for ax, kind, f, p, lc, text, mod in (CUR.get("texts") or []):
        if ax != "adverse" or kind not in ("complication_name", "safety_phrase"):
            continue
        for part in analyzer_texts(text)[1:]:
            try:
                wi = word_info(an, part, AT.r1)
            except Exception:  # noqa: BLE001
                continue
            if wi["sent"]:
                continue
            for w in wi["mod_words"]:
                k = w.strip("*'\"“”‘’.…`~!?,")
                if norm(k) in stop or norm(k) in AT.r1:
                    continue
                cnt[k] += 1
                ex.setdefault(k, (lc, text))
                if lc not in locs[k]:
                    locs[k].append(lc)
    subs = []
    for w, n in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0])):
        pid = f"{BATCH}-R1-{_h(w)}"
        refs = [g.src(l) for l in locs[w][:12]]
        pl = payload(pid, "scope_review", OrderedDict([("erd_ref", "erd-v3.3.json#/tuple_rules/adverse/adverse_stopwords"), ("review_item", w)]), OrderedDict([("disposition", f"R1 수식어 목록에 「{w}」 추가(ERD 규칙 데이터 변경 · 다음 판)")]),
                     f"결정 묶음 6 — R1 후보 「{w}」(관형어·부사어 하나 · 출현 {n}) — 기록만(ERD 규칙 데이터는 ERD 개정으로)", refs)
        subs.append(node(f"r1/{_h(w)}", "scope_review", f"R1 후보 「{w}」", f"출현 {n} · 지금은 분석기 품사 규칙(관형어 하나 = 수식어)으로 떼어 parsed.misc(by=analyzer_n2)에 보존 — R1 목록에는 없다",
                         [g.ev(ex[w][0], f"원문 예 · 출현 {n}")], [opt("add_r1", "R1 목록에 넣는다(기록 · ERD 다음 판)", "scope_review 기록만 — 빌드 값 불변", pl, True), opt("no", "넣지 않는다", "결정 없음(분석기 규칙은 그대로 떼어 보존)", None, None)],
                         None, "목록 추가는 ERD 규칙 데이터 변경 — 원장이 말하지 않는다(추천 없음).", OrderedDict([("word", w), ("n", n), ("locators", locs[w])])))
    return node("r1-candidates", "scope_review", f"R1 후보(새) {len(subs)} — 관형어·부사어 하나로 뗀 말 중 R1 목록·수식어 138 밖", "V3.3-B: 절 없이 명사 앞에 붙은 관형어 하나는 수식어(보존). 목록(R1)에 더할지는 ERD 규칙 데이터 변경(사용자).", [], [], None, "하위 항목마다", {"subitems": subs})


def mxx_items(g, S):
    L = S.ctx["L"]
    cnt, locs = Counter(), defaultdict(list)
    for i, l in enumerate(L["synergy.json"]["links"]):
        for k in ("from", "to"):
            if re.match(r"^M\d+-", l[k]):
                cnt[l[k]] += 1
                locs[l[k]].append(f"synergy.json:links[].{k}@{i}")
    subs = []
    for lab, n in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0])):
        subs.append(node(f"mxx/{_h(lab)}", "ledger", f"synergy 「{lab}」 — Mxx- 접두", f"자리 {n} · 원장 4판 후보(3판에서 59 자리는 정식 이름으로 · 남은 34종 171 자리)",
                         [g.ev(l, "synergy from/to") for l in locs[lab][:2]], [opt("unify", "4판에서 정식 이름으로 통일(원장 수정 · 결정 아님)", "브론즈 4판 몫 — 실버 결정 없음", None, None), opt("keep", "그대로", "결정 없음", None, None)],
                         None, "원장 수정 여부 — 사용자 답 대기(HANDOFF).", OrderedDict([("label", lab), ("n", n), ("locators", locs[lab])])))
    return node("mxx-prefix", "ledger", f"synergy 「Mxx-」 접두 {len(subs)}종(자리 {sum(cnt.values())}) — 원장 4판 후보", "V3.3-G 원장 3판 뒤 남은 「Mxx-」 접두 — 4판 후보(사용자 답 대기) · 실버 결정이 아니다.", [], [], None, "하위 항목마다", {"subitems": subs})


# =====================================================================================
def build_gate_6(S, out_dir):
    g = G5(S, S.ctx["args"].decisions)
    erd = S.ctx["erd"]
    AT = S.ctx["AU"].A["AT"]
    dups = S.ctx.get("ledger_dup_conflicts", [])
    strong = [c for c in dups if c.get("grade") == "strong" and c["status"] == "open"]
    weak = [c for c in dups if c.get("grade") == "weak" and c["status"] == "open"]
    strong_by_node = defaultdict(list)
    for c in strong:
        strong_by_node[c["pair"]["node"]].append(c["pair"]["other"])
        if c["pair"]["other_kind"] == "ledger":
            strong_by_node[c["pair"]["other"]].append(c["pair"]["node"])
    amb_by_node = defaultdict(list)
    nodes = {norm(n["canonical"]): n["canonical"] for n in S.ctx["adv"]["ledger_events"]}
    for r in getattr(AT, "seglog", []):
        if r["kind"] == "node" and r["amb"]:
            for t in r["target"]:
                if norm(t) in nodes:
                    for a in r["amb"]:
                        if a not in amb_by_node[nodes[norm(t)]]:
                            amb_by_node[nodes[norm(t)]].append(a)
    solo = getattr(AT, "solo_strict", Counter())
    items = [node_items(g, S, strong_by_node, amb_by_node, solo), dup_items(g, S, strong),
             phrase_items(g, S, "sentence_b", "sentence-b", "문장꼴(b)", "V3.3-B: 절(용언+어미 · 논항 · 의존명사)이 있고 사전 사건이 0 인 토막 — 노드를 세우지 않고 사람 판정(status=sentence · 원문 보존)."),
             ]
    amb_phr = phrase_items(g, S, "ambiguous", "ambiguous", "애매", "분석기 판정 애매(후보 전부 이상 꼴 · 조사 붙은 명사형 · 명사 없음 · 명사 아닌 형태소 버림) 또는 사전 사건에 규칙 밖 명사가 붙은 노드 — 사람 판정.")
    amb_phr["subitems"] = amb_phr["subitems"] + ambiguous_node_items(g, S, amb_by_node, strong_by_node)
    amb_phr["title"] = f"애매 {len(amb_phr['subitems'])} — 문구 {sum(1 for s in amb_phr['subitems'] if s['id'].startswith('ambiguous/PHR'))} · 노드 {sum(1 for s in amb_phr['subitems'] if s['id'].startswith('ambiguous/node'))}"
    items.append(amb_phr)
    occ, r30 = occlusion_items(g, S, erd)
    items += [occ, r30]
    b3p = os.path.join(out_dir, "gate", "batch3.json")
    items3 = json.load(open(b3p, encoding="utf-8")) if os.path.exists(b3p) else []
    b3 = batch3_items(g, S, items3)
    for it in b3:   # V3.3-E: dictionary_add new_value 의 category 는 v3.3 kind 구조체에 없다 — 묶음 3 옵션 본문에서 뗀다(값은 null 이었다)
        for s_ in (it.get("subitems") or [it]):
            for o in s_["options"]:
                pl = o.get("decision_payload")
                if pl and isinstance(pl.get("new_value"), dict) and pl["new_value"].get("category", 0) is None:
                    pl["new_value"] = OrderedDict((k, v) for k, v in pl["new_value"].items() if k != "category")
    items.append(node("batch3", "batch3", f"결정 묶음 3 미결 {sum(len(it.get('subitems') or [it]) for it in b3)}", "out/gate/batch3.json 그대로(gate5 와 같다 · 공기색전은 v3.2 물질 칸 기준) — 사용자 미결.", [], [], None, "하위 항목마다",
                      {"subitems": [s for it in b3 for s in (it.get("subitems") or [it])]}))
    items.append(r1_candidate_items(g, S, erd))
    items.append(mxx_items(g, S))
    ids = set()
    for it, s in leaves_of(items):
        if s["id"] in ids:
            raise AssertionError(f"게이트 자리 id 중복 {s['id']}")
        ids.add(s["id"])
        for o in s["options"]:
            p = o["decision_payload"]
            if p:
                errs = [e for e in validate(dict(p, decided_by="x")) if "decided_by" not in e]
                if errs:
                    raise AssertionError(f"{s['id']} {o['key']}: {errs}")
        s["already_decided"] = dedupe(x for o in s["options"] for x in g.already(o["decision_payload"]))
        if s.get("recommended") is not None and s["recommended"] not in [o["key"] for o in s["options"]]:
            raise AssertionError(f"{s['id']} recommended {s['recommended']} 없음")
    if g.read_fail:
        raise AssertionError(f"원장 읽기 실패 {len(g.read_fail)}: {g.read_fail[:5]}")
    gd = os.path.join(out_dir, "gate")
    os.makedirs(gd, exist_ok=True)
    write_json(os.path.join(gd, "batch6.json"), items)
    nodes_ = {n["canonical"]: n for n in S.ctx["adv"]["ledger_events"]}
    weak_rows = [OrderedDict([("conflict_id", c["id"]), ("pair", c["pair"]), ("stable_key", c["stable_key"]),
                              ("node_locators", nodes_.get(c["pair"]["node"], {}).get("locators", [])),
                              ("other_locators", nodes_.get(c["pair"]["other"], {}).get("locators", []) if c["pair"]["other_kind"] == "ledger" else [])]) for c in weak]
    write_json(os.path.join(gd, "batch6-weak.json"), weak_rows)
    lv = list(leaves_of(items))
    per = OrderedDict()
    for it in items:
        subs = it.get("subitems") or [it]
        per[it["id"]] = {"leaves": len(subs), "ask": sum(1 for s in subs if s["options"]), "recommended": sum(1 for s in subs if s.get("recommended") is not None), "options": sum(len(s["options"]) for s in subs)}
    write_text(os.path.join(gd, "batch6.md"), render_md(items, weak_rows, per))
    return {"items": len(items), "leaves": len(lv), "by_item": per, "ask": sum(v["ask"] for v in per.values()), "recommended": sum(v["recommended"] for v in per.values()), "weak": len(weak_rows),
            "evidence": sum(len(s["evidence"]) for _, s in lv), "read_fail": len(g.read_fail), "options": sum(len(s["options"]) for _, s in lv)}


def render_md(items, weak_rows, per):
    lv = list(leaves_of(items))
    o = ["# 결정 묶음 6 — 게이트 자료(ERD v3.3 · 8차 뒤 남는 자리)", "",
         f"묶음 {len(items)} · 자리 {len(lv)}(물을 자리 {sum(v['ask'] for v in per.values())} · 목록만 {len(lv) - sum(v['ask'] for v in per.values())}) · 추천 있음 {sum(v['recommended'] for v in per.values())} · ⑦ weak {len(weak_rows)} 은 `batch6-weak.json`(게이트에 올리지 않음).",
         "원문은 브론즈 원장에서 locator 로 직접 읽었다. 추천은 원장이 말할 때만(병기 쌍) — 없으면 「—」. "
         "고른 결과는 `python3 apply_gate.py --gate out/gate/batch6.json --out decisions/batch6/ --answers answers.json` 으로 결정 파일이 된다(answers = {자리 id: 옵션 key}).", "",
         md_table(["묶음", "자리", "물을 자리", "옵션", "추천"], [(k, v["leaves"], v["ask"], v["options"], v["recommended"]) for k, v in per.items()]), ""]
    for it in items:
        o += [f"## {it['id']} — {it['title']}", "", it["why"], ""]
        subs = it.get("subitems") or [it]
        if it["id"] == "ledger-nodes":
            o.append(md_table(["#", "노드", "원장 횟수", "단독 출현", "계열", "원문 예", "⑦ strong 상대", "애매"],
                              [(i + 1, s["node"]["canonical"], s["node"]["n_locators"], s["node"]["solo_strict"], ", ".join(s["node"]["where"]["modalities"]) or "—",
                                " / ".join(f"「{str(e['text'])[:40]}」" for e in s["evidence"][:2]), ", ".join(s["node"]["strong_partners"]) or "—", " / ".join(s["node"]["ambiguous"])[:80] or "—") for i, s in enumerate(subs)]))
            o.append("")
            continue
        if it["id"] == "dup-strong":
            o.append(md_table(["#", "노드", "상대", "상대 종류", "규칙", "추천", "근거"], [(i + 1, s["pair"]["node"], s["pair"]["other"], s["pair"]["other_kind"], ", ".join(s["pair"]["rules"]), s["recommended"] or "—", s["recommend_reason"][:60]) for i, s in enumerate(subs)]))
            o.append("")
            continue
        if it["id"] in ("sentence-b", "ambiguous", "mxx-prefix", "r1-candidates", "occlusion-embolism"):
            o.append(md_table(["#", "자리", "제목", "왜", "원문 예"], [(i + 1, s["id"], s["title"][:50], s["why"][:100], " / ".join(f"「{str(e['text'])[:40]}」" for e in s["evidence"][:1])) for i, s in enumerate(subs)]))
            o.append("")
            continue
        for s in subs:
            if s is not it:
                o += [f"### {s['id']} — {s['title']}", "", s["why"], ""]
            for e in s["evidence"][:8]:
                o.append(f"- `{e['locator']}` — 「{str(e['text']).replace(chr(10), ' ')[:140]}」" + (f" ({e['note']})" if e.get("note") else ""))
            o.append("")
            if s["options"]:
                o.append(md_table(["옵션", "뜻", "적용되면", "결정"], [(f"**{x['key']}**" if x["key"] == s.get("recommended") else x["key"], x["label"], x["effect"], (f"{x['decision_payload']['kind']} `{x['decision_payload']['id']}`" if x["decision_payload"] else "결정 없음")) for x in s["options"]]))
                o.append(f"\n추천: **{s.get('recommended') or '—'}** — {s['recommend_reason']}\n")
    return "\n".join(o)
