# -*- coding: utf-8 -*-
"""결정 묶음 4 — 동의어 제안 게이트(ERD v3.1 · 발주서 silver-build-6-brief.md C).

out/gate/batch4.json(2B 스키마 — 항목 {id, kind, title, why, evidence[{file, locator, text, note?}], options[{key, label, effect, builder_applies_now, decision_payload}],
recommended, recommend_reason, …}) · batch4.md. 옵션의 decision_payload 는 그 옵션을 고르면 그대로 적용되는 결정 파일(dictionary_add · canonical_mapping
완성형 · status=proposed)이고 `apply_gate.py --gate out/gate/batch4.json --out decisions/batch4/` 가 approved 로 쓴다. 지금대로 = decision_payload null.

세 묶음:
  ① adverse-phrase — 문구 사전 unlinked 항목의 미등록 조각(사건 축) 상위 80(조각이 든 문구 자리 수 순) · 사건 사전 후보 ≤3
  ② site-material — 같은 조각 중 부위(site · 상대 부위 · 해부 zone) · 물질(adverse_qualifier · ingredient_material) 사전 후보가 있는 것
  ③ procedure — ⑨ open 미해결 참조의 미등록 조각 상위 60(그 조각이 든 open ⑨ 참조 수 순) · 하위분류 · 제품 · 부위 · 성분 사전 후보 ≤3
후보 근거는 기계 판정만 — 정규화 부분 일치(조각 ⊃ 사전 표면형 · 사전 표면형 ⊃ 조각 · 영문은 낱말 단위) · 원장 병기(「A(B)」 의 한쪽 = 조각 · 다른 쪽 = 사전 표면형 통째) ·
영문 대응(문헌 같은 레코드에서 한글 쪽에 안 잡힌 사건 하나 ↔ 한글 미등록 조각 하나). 추천은 「같은 말」 근거(complications 이름 병기 · 1:1 영문 대응 · 표기 변형 = 사전 값 +
접미 감·함·증 또는 조사 한 글자)가 후보 하나만 가리킬 때뿐 — 문구 병기·그 밖 부분 일치만이면 recommended=null(추정 금지).
effect = 그 옵션을 적용했을 때 닫히는 문구 자리 수(unlinked → auto) · 풀리는 ⑨ 참조 수 — 결정을 넣은 사전으로 그 자리만 다시 분해해 센다(근사 아님).
"""
import copy
import json
import os
import re
from collections import Counter, OrderedDict, defaultdict

from .adverse31 import AdverseUnits31
from .decisions import is_scoped_label_mapping, validate
from .decompose import Ids, Lexicon, MARKET_SLOT, ProcedureTuples, scoped_label_spans, with_alias
from .gate2b import G, node
from .util import dedupe, md_table, mkid, norm, write_json, write_text

BATCH = "DEC-2026-11-05-B4"
BATCH_NOTE = "결정 묶음 4 (동의어 · 게이트 out/gate/batch4.json · 발주서 silver-build-6-brief.md C)"
ERD_REF = "erd-v3.1.md §5.2"
N_ADVERSE, N_PROC = 80, 60
PAREN = re.compile(r"([^()\s/·,]+)\s*\(([^()]+)\)")
ASCII = re.compile(r"^[A-Za-z][A-Za-z\- ]+$")
PROPOSED_DIR = "batch4-proposed"


def opt(key, label, effect, pl, applies=True):
    return OrderedDict([("key", key), ("label", label), ("effect", effect), ("builder_applies_now", applies if pl else None), ("decision_payload", pl)])


def payload(pid, kind, target, new_value, reason, ledger_refs, extra=None):
    refs = [OrderedDict([("kind", "ledger"), ("ref", r)]) for r in dedupe(ledger_refs)] + [OrderedDict([("kind", "erd", ), ("ref", ERD_REF)]),
                                                                                         OrderedDict([("kind", "brief", ), ("ref", "silver-build-6-brief.md C — 결정 묶음 4(동의어)")])]
    p = OrderedDict([("id", pid), ("kind", kind), ("target", target), ("new_value", new_value), ("reason", reason), ("decided_by", None), ("decided_at", None),
                     ("status", "proposed"), ("source_refs", refs), ("batch", BATCH_NOTE)])
    if extra:
        p.update(extra)
    return p


def _surfaces(entries):
    """사전 항목 → [(표면형, 정준값, 항목)] — 정준값·동의어(code 동의어 제외)."""
    out = []
    for e in entries:
        out.append((e["canonical"], e["canonical"], e))
        for s_ in e.get("synonyms", []):
            if s_.get("link") != "code":
                out.append((s_["value"], e["canonical"], e))
    return out


PARTICLES = set("이가은는을를의에도만")
SUFFIXES = set("감함증") | PARTICLES   # 표기 변형 — 명사 + 접미 한 글자(감·함·증) 또는 조사 한 글자


def _partial(frag, surfaces, min_len=2):
    """정규화 부분 일치 — 조각 ⊃ 표면형 · 표면형 ⊃ 조각. 영문은 낱말 단위(「blanching」 안의 chin 같은 글자 겹침 제외) ·
    한 글자 표면형은 조각 = 표면형 + 조사 한 글자(이·가·은·는·을·를·의·에·도·만)일 때만."""
    nf = norm(frag)
    out = OrderedDict()
    for surf, canon, e in surfaces:
        ns = norm(surf)
        if not ns or ns == nf:
            continue
        hit = None
        if re.search(r"[a-z]", ns) or re.search(r"[a-z]", nf):
            sw = set(re.findall(r"[a-z0-9]+", surf.casefold()))
            fw_ = set(re.findall(r"[a-z0-9]+", frag.casefold()))
            if fw_ and sw and (fw_ <= sw or sw <= fw_) and all(len(w) >= 2 for w in fw_ | sw):
                hit = f"영문 낱말 「{frag}」 ↔ 「{surf}」"
        elif len(ns) == 1:
            if len(nf) == 2 and nf[0] == ns and nf[1] in PARTICLES:
                hit = f"조각 「{frag}」 = 「{surf}」 + 조사"
        elif len(ns) >= min_len and ns in nf:
            hit = f"조각 「{frag}」 ⊃ 「{surf}」"
        elif len(nf) >= 2 and nf in ns:
            hit = f"「{surf}」 ⊃ 조각 「{frag}」"
        if hit:
            kind = "partial"
            if (len(nf) == len(ns) + 1 and nf.startswith(ns) and nf[-1] in SUFFIXES and len(ns) >= 2) or (len(ns) == len(nf) + 1 and ns.startswith(nf) and ns[-1] in "감함증" and len(nf) >= 2) or \
                    (len(ns) == 1 and len(nf) == 2 and nf[1] in PARTICLES):
                kind = "variant"
                hit += " — 표기 변형(접미 감·함·증 또는 조사 한 글자)"
            out.setdefault(canon, {"canonical": canon, "entry": e, "basis": []})["basis"].append({"kind": kind, "note": hit})
    return out


class G4(G):
    def __init__(self, S, decisions_dir):
        super().__init__(S, decisions_dir)
        self.D = {d["name"]: d for d in S.ctx["dic"]["dictionaries"]}
        self.rules = S.ctx["erd"]["tuple_rules"]["adverse"]
        self.read_fail = []

    def ev(self, lc, note=None):
        o = super().ev(lc, note)
        if str(o["text"]).startswith("<읽기 실패"):
            self.read_fail.append(lc)
        return o

    # ------------------------------------------------------------------ 시뮬레이션
    def dic_with(self, name, mutate):
        """사전 하나만 바꾼 얕은 사본(나머지는 그대로 공유 · 원본 불변)."""
        dic = dict(self.S.ctx["dic"])
        ds = []
        for d in dic["dictionaries"]:
            if d["name"] == name:
                d = copy.deepcopy(d)
                mutate(d)
            ds.append(d)
        dic["dictionaries"] = ds
        return dic

    @staticmethod
    def _add_syn(canonical, syn, code=None):
        def f(d):
            e = next((x for x in d["entries"] if norm(x["canonical"]) == norm(canonical) and (code is None or str(x.get("code")) == str(code))), None)
            if e is None:
                d["entries"].append({"id": mkid("DIC", f"{d['name']}|{canonical}"), "canonical": canonical, "sources": [{"kind": "decision"}], "synonyms": [], "definition": None})
                e = d["entries"][-1]
            if syn and norm(syn) not in {norm(s_["value"]) for s_ in e["synonyms"]} | {norm(e["canonical"])}:
                e["synonyms"].append({"value": syn, "link": "decision", "sources": []})
        return f

    def phrase_closes(self, contexts, name, mutate):
        """문구 자리(문맥 텍스트) 중 그 사전 변경 뒤 auto 가 되는 자리 수."""
        dic = self.dic_with(name, mutate)
        ids = Ids(dic, self.L, self.ctx["erd"]["resolve_rules"])
        AT = AdverseUnits31(ids, self.rules)
        n = 0
        for c in contexts:
            if AT.evaluate(c["text"], {"locator": c["locator"]})["status"] == "auto":
                n += 1
        return n

    def ref_closes(self, refs, name=None, mutate=None, scoped=None):
        """⑨ open 참조 행 중 그 결정 뒤 튜플(또는 조합·부위 여럿)이 되는 행 수 · 그 원장 자리 수."""
        dic = self.dic_with(name, mutate) if name else self.S.ctx["dic"]
        lex = Lexicon(with_alias(dic))
        ids = Ids(dic, self.L, self.ctx["erd"]["resolve_rules"])
        sc = scoped_label_spans([scoped], ids) if scoped else None
        PT = ProcedureTuples(lex, self.ctx["erd"]["resolve_rules"], ids, self.L, sc)
        n = nl = 0
        for r in refs:
            x = PT.run_reference(r["label"], r["hint"], "reference", r["slot"])
            if x["result"] in ("tuple", "combo_ref", "multi_tuple", "node"):
                n += 1
                nl += len(r["locators"])
        return n, nl


# =====================================================================================
# ① ② 부작용 문구 조각
# =====================================================================================
def _phrase_pool(g):
    """unlinked 문구 사전 항목의 미등록 조각 → {조각: {contexts(문구 자리 · 텍스트), entries}} (자리 수 순)."""
    AU = g.AU
    pool = OrderedDict()
    for pid, e in AU.phrases.items():
        if e["status"] != "unlinked":
            continue
        for u in dedupe(e["unregistered"]):
            x = pool.setdefault(u, {"fragment": u, "contexts": [], "entries": []})
            x["entries"].append(pid)
            for c in e["contexts"]:
                x["contexts"].append({"locator": c["locator"], "ledger": AU.ctx_loc(c), "text": c["text"], "kind": c["kind"]})
    return OrderedDict(sorted(pool.items(), key=lambda kv: (-len(kv[1]["contexts"]), kv[0])))


def _texts(g):
    """원장 병기 근거를 찾을 문장 — complications 이름 + 문구 자리 전부(원문 · 원장 위치)."""
    out = []
    for r in g.ctx["adv"]["complications"]:
        out.append(("complications", r["text"], g.erd2src.get(r["locator"], r["locator"])))
    for e in g.AU.phrases.values():
        for c in e["contexts"]:
            out.append(("phrase", c["text"], g.AU.ctx_loc(c)))
    return out


def _paren_index(texts):
    """원장 병기 색인 — 「A(B)」 의 각 쪽 정규화형 → [(다른 쪽, A, B, 출처 종류, locator)] (한 번만 만든다)."""
    idx = defaultdict(list)
    for src, t, lc in texts:
        for a, b in PAREN.findall(t or ""):
            idx[norm(a)].append((b, a, b, src, lc))
            idx[norm(b)].append((a, a, b, src, lc))
    return idx


def _paren_pairs(g, frag, surf_map, pidx, cache=None):
    """원장 병기 — 「A(B)」 에서 한쪽이 조각과, 다른 쪽이 그 축 사전 표면형과 통째로(정규화 완전 일치) 같으면 그 값(근거 locator · 출처 종류)."""
    out = defaultdict(list)
    for y, a, b, src, lc in pidx.get(norm(frag), []):
        canon = surf_map.get(norm(y))
        if canon:
            out[canon].append({"kind": "paren" if src == "complications" else "paren_phrase", "note": f"{'complications 이름' if src == 'complications' else '원장 문구'} 병기 「{a}({b})」", "locator": lc})
    return out


def _event_spans(g):
    AT = g.ctx["adv"]["AT"]

    def spans(text):
        out = []
        for grp in AT.split(text):
            for m in grp["members"]:
                out += [s["canonical"] for s in m["spans"] if s["kind"] == "event"]
        return dedupe(out)
    return spans


def _english_index(g):
    """영문 대응 — 문헌 레코드마다 patient_ko 의 미등록 조각과 영문 statement 의 사건(영문 동의어)을 맞춰 보고, 한글 쪽에 안 잡힌 사건이 하나 · 한글 미등록 조각이 하나일 때만
    둘을 짝으로 둔다(1:1 남는 짝 · 그 밖은 근거 아님)."""
    AT = g.ctx["adv"]["AT"]
    lit = g.L["literature-evidence.json"]["categories"]
    eng = [(s_, canon) for s_, canon, e in _surfaces(g.D["adverse_event_type"]["entries"]) if ASCII.match(s_)]
    out = defaultdict(list)
    for code, cat in lit.items():
        for i, ae in enumerate(cat.get("adverse_effects") or []):
            ko = ae.get("patient_ko") or ""
            st = (ae.get("statement") or "").lower()
            en = dedupe(canon for s_, canon in eng if re.search(r"\b" + re.escape(s_.lower()) + r"\b", st))
            groups = AT.split(ko)
            ko_ev = {s["canonical"] for grp in groups for m in grp["members"] for s in m["spans"] if s["kind"] == "event"}
            un = dedupe(u for grp in groups for m in grp["members"] for u in m["untouched"])
            left = [c for c in en if c not in ko_ev]
            if len(left) == 1 and len(un) == 1:
                hit = next(s_ for s_, canon in eng if canon == left[0] and re.search(r"\b" + re.escape(s_.lower()) + r"\b", st))
                out[norm(un[0])].append((left[0], {"kind": "english", "note": f"문헌 같은 레코드 1:1 — 영문 statement 「{hit}」 ↔ 한글 미등록 「{un[0]}」", "locator": f"literature-evidence.json:categories.{{code}}.adverse_effects[].statement@{code}/{i}"}))
    return out


def _english(eidx, frag):
    out = defaultdict(list)
    for canon, b in eidx.get(norm(frag), []):
        out[canon].append(b)
    return out


def _rank(cands):
    """후보 정렬 — 원장 병기·영문 대응 근거 수 → 부분 일치 → 정준값."""
    def strong(c):
        return sum(2 if b["kind"] in ("paren", "english", "variant") else 1 if b["kind"] == "paren_phrase" else 0 for b in c["basis"])
    return sorted(cands.values(), key=lambda c: (-strong(c), -len(c["basis"]), c["canonical"]))


def _recommend(cands):
    """추천 — 같은 말이라는 기계 근거(complications 이름 병기 · 문헌 1:1 영문 대응 · 표기 변형: 사전 값 + 접미 감·함·증 / 조사 한 글자)가 후보 하나만 가리킬 때.
    문구 병기(원인·예시·부위를 가리지 않음)·그 밖 부분 일치만이면 null."""
    strong = [c for c in cands if any(b["kind"] in ("paren", "english", "variant") for b in c["basis"])]
    if len(strong) == 1 and strong[0].get("dictionary") == "adverse_qualifier":
        return None, "표기 변형 근거는 있으나 수식 사전 「필러」「지방」은 시술명과 겹친다(ERD v3.1 검토 D-6 · 열린 결정) — 물질로 읽을지는 사람이 정한다(추천 없음)"
    if len(strong) == 1:
        c = strong[0]
        return c, "같은 말이라는 근거가 후보 하나만 가리킨다 — " + " · ".join(dedupe(b["note"] for b in c["basis"] if b["kind"] in ("paren", "english", "variant")))[:300]
    if len(strong) > 1:
        return None, "같은 말 근거가 후보 둘 이상을 가리킨다(추천 없음)"
    if cands:
        return None, "근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)"
    return None, "사전 후보 근거 없음(추천 없음)"


def item_adverse(g, i, x, texts, ev_spans, kind_tag, axis, cands_map, merged):
    frag = x["fragment"]
    ctxs = x["contexts"]
    ev = [g.ev(c["ledger"] or c["locator"], f"문구 사전 unlinked · {c['kind']}") for c in ctxs]
    ledger = [c["ledger"] for c in ctxs if c["ledger"]]
    cands = _rank(cands_map)[:3]
    rec_c, rec_reason = _recommend(cands)
    opts = []
    for j, c in enumerate(cands):
        e = c["entry"]
        dname = c.get("dictionary", axis)
        nv = OrderedDict([("canonical", c["canonical"]), ("synonyms", [frag]), ("category", None)])
        if dname == "product_name":
            nv["code"] = e.get("code")
        pl = payload(f"{BATCH}-{kind_tag}-{i:03d}{chr(97 + j)}", "dictionary_add", {"dictionary": dname}, nv,
                     f"결정 묶음 4 — 문구 조각 「{frag}」 을 {dname} 「{c['canonical']}」 의 동의어로(근거: " + " · ".join(dedupe(b["note"] for b in c["basis"]))[:200] + ")",
                     ledger + [b["locator"] for b in c["basis"] if b.get("locator")], {"proposal_item": f"b4-{kind_tag.lower()}/{i:03d}"})
        n = g.phrase_closes(ctxs, dname, G4._add_syn(c["canonical"], frag, e.get("code") if dname == "product_name" else None))
        opts.append(opt(f"syn_{j + 1}", f"{dname} 「{c['canonical']}」 의 동의어", f"닫히는 문구 자리 {n}/{len(ctxs)}(unlinked → auto) · 근거 " + " · ".join(dedupe(b["note"] for b in c["basis"]))[:160], pl))
        c["closes"] = n
    if axis == "adverse_event_type" and x.get("standalone"):
        pl = payload(f"{BATCH}-{kind_tag}-{i:03d}n", "dictionary_add", {"dictionary": "adverse_event_type"}, OrderedDict([("canonical", frag), ("synonyms", []), ("category", None)]),
                     f"결정 묶음 4 — 문구 조각 「{frag}」 을 새 사건 값으로(원장 문구에서 멤버 하나 전체로 {x['standalone']} 자리)", ledger, {"proposal_item": f"b4-{kind_tag.lower()}/{i:03d}"})
        n = g.phrase_closes(ctxs, "adverse_event_type", G4._add_syn(frag, None))
        opts.append(opt("new_event", f"새 사건 「{frag}」(분류 미정)", f"닫히는 문구 자리 {n}/{len(ctxs)} · 원장 문구에서 멤버 하나 전체로 쓰인 자리 {x['standalone']}", pl))
    opts.append(opt("keep", "지금대로(미등록 · 게이트)", "결정 없음 — 문구는 unlinked 로 남는다", None))
    rec = f"syn_{cands.index(rec_c) + 1}" if rec_c else None
    title = f"문구 조각 「{frag}」 — " + (f"{', '.join(c['canonical'] for c in cands)} 중 어느 값의 동의어인가?" if cands else "사전 후보 없음 — 새 값으로 둘까?")
    why = (f"문구 사전 unlinked 항목 {len(x['entries'])}(문구 자리 {len(ctxs)})에 미등록 조각으로 남아 그 문구가 단위에 닿지 못한다(원칙 D). "
           f"후보는 {axis} 사전의 정규화 부분 일치·원장 병기·영문 대응뿐(유사도 없음).")
    it = node(f"b4-{kind_tag.lower()}/{i:03d}", "dictionary_add", title, why, ev, opts, rec, rec_reason,
              {"fragment": frag, "dictionary": axis, "phrase_entries": x["entries"], "phrase_locators": len(ctxs),
               "candidates": [{"canonical": c["canonical"], "dictionary": c.get("dictionary", axis), "basis": c["basis"], "closes_phrases": c.get("closes")} for c in cands]})
    merged.append(it)
    return it


def adverse_items(g):
    pool = _phrase_pool(g)
    texts = _texts(g)
    pidx = _paren_index(texts)
    eidx = _english_index(g)
    AT = g.ctx["adv"]["AT"]
    standalone = Counter()
    for e in g.AU.phrases.values():
        if e["status"] != "unlinked":
            continue
        for grp in AT.split(e["raw_variants"][0]):
            for m in grp["members"]:
                if len(m["untouched"]) == 1 and not m["spans"] and not m.get("modifiers") and norm(m["text"]) == norm(m["untouched"][0]):
                    standalone[m["untouched"][0]] += len(e["locators"])
    ev_surf = _surfaces(g.D["adverse_event_type"]["entries"])
    site_surf = _surfaces(g.D["site"]["entries"])
    rsite_surf = _surfaces(g.D["relative_site"]["entries"])
    qual_surf = _surfaces(g.D["adverse_qualifier"]["entries"])
    ingr_surf = _surfaces(g.D.get("ingredient_material", {"entries": []})["entries"])
    ev_map = {norm(s_): canon for s_, canon, e in ev_surf}
    site_map = {norm(s_): canon for s_, canon, e in site_surf}
    adverse, sitemat = [], []
    for frag, x in pool.items():
        x["standalone"] = standalone.get(frag, 0)
        ev_c = _partial(frag, ev_surf)
        for canon, bs in _paren_pairs(g, frag, ev_map, pidx).items():
            ev_c.setdefault(canon, {"canonical": canon, "entry": next(e for e in g.D["adverse_event_type"]["entries"] if e["canonical"] == canon), "basis": []})["basis"] += bs
        for canon, bs in _english(eidx, frag).items():
            ev_c.setdefault(canon, {"canonical": canon, "entry": next(e for e in g.D["adverse_event_type"]["entries"] if e["canonical"] == canon), "basis": []})["basis"] += bs
        sm = OrderedDict()
        for dname, surf in (("site", site_surf), ("relative_site", rsite_surf), ("adverse_qualifier", qual_surf), ("ingredient_material", ingr_surf)):
            for canon, c in _partial(frag, surf).items():
                c["dictionary"] = dname
                sm[(dname, canon)] = c
        for canon, bs in _paren_pairs(g, frag, site_map, pidx).items():
            e = next(e for e in g.D["site"]["entries"] if e["canonical"] == canon)
            sm.setdefault(("site", canon), {"canonical": canon, "entry": e, "basis": [], "dictionary": "site"})["basis"] += bs
        if sm and not ev_c:
            sitemat.append((frag, x, OrderedDict((f"{k[0]}:{k[1]}", v) for k, v in sm.items())))
        else:
            adverse.append((frag, x, ev_c))
    items_a, items_s, merged = [], [], []
    for i, (frag, x, cm) in enumerate(adverse[:N_ADVERSE]):
        items_a.append(item_adverse(g, i + 1, x, texts, None, "ADV", "adverse_event_type", cm, merged))
    for i, (frag, x, cm) in enumerate(sitemat):
        fixed = OrderedDict()
        for k, c in cm.items():
            fixed[c["canonical"] if len({v["canonical"] for v in cm.values()}) == len(cm) else k] = c
        items_s.append(item_adverse(g, i + 1, x, texts, None, "SIT", "site", fixed, merged))
    return items_a, items_s, len(adverse), len(sitemat)


# =====================================================================================
# ③ 시술 조각(⑨ open)
# =====================================================================================
def proc_items(g):
    refs = []
    for c in g.S.conflicts:
        if c["kind"] != "unresolved_reference" or c["status"] != "open" or not c.get("ref_id") or c.get("reason") != "unregistered":
            continue
        refs.append({"label": c.get("label"), "hint": c.get("hint"), "slot": c.get("slot"), "ref_id": c["ref_id"], "fragments": c.get("fragments") or [], "locators": c["stable_key"]["locators"]})
    by = defaultdict(list)
    for r in refs:
        for f in dedupe(r["fragments"]):
            by[f].append(r)
    ranked = sorted(by.items(), key=lambda kv: (-len(kv[1]), -sum(len(r["locators"]) for r in kv[1]), kv[0]))[:N_PROC]
    subs = []
    for e in g.D["modality_subcategory_label"]["entries"]:
        subs.append((e["canonical"], e["canonical"], e))
    prod = _surfaces(g.D["product_name"]["entries"])
    site = _surfaces(g.D["site"]["entries"])
    ingr = _surfaces(g.D.get("ingredient_material", {"entries": []})["entries"])
    lab_texts = [(r["label"], r["locators"][0] if r["locators"] else None) for r in refs] + [(it["item"]["name"], it["name_loc"]) for it in g.ctx["items"].values()]
    items = []
    for i, (frag, rr) in enumerate(ranked):
        cm = OrderedDict()
        for dname, surf in (("modality_subcategory_label", subs), ("product_name", prod), ("site", site), ("ingredient_material", ingr)):
            for canon, c in _partial(frag, surf).items():
                c["dictionary"] = dname
                cm[(dname, canon, str(c["entry"].get("code")))] = c
        # 원장 병기 — 라벨·항목 이름의 「A(B)」 한쪽이 조각, 다른 쪽이 제품·하위분류 사전 값
        for t, lc in lab_texts:
            for a, b in PAREN.findall(t or ""):
                for x, y in ((a, b), (b, a)):
                    if norm(x) != norm(frag):
                        continue
                    for dname, surf in (("product_name", prod), ("modality_subcategory_label", subs)):
                        for s_, canon, e in surf:
                            if norm(s_) == norm(y):
                                cm.setdefault((dname, canon, str(e.get("code"))), {"canonical": canon, "entry": e, "basis": [], "dictionary": dname})["basis"].append(
                                    {"kind": "paren_phrase", "note": f"원장 이름 병기 「{a}({b})」", "locator": lc})
        cands = _rank(cm)[:3]
        rec_c, rec_reason = _recommend(cands)
        locs = dedupe(l for r in rr for l in r["locators"])
        ev = [g.ev(l, "⑨ open 미해결 참조(미등록 조각)") for l in locs]
        scope = sorted({r["ref_id"] for r in rr})
        opts = []
        for j, c in enumerate(cands):
            e, dname = c["entry"], c["dictionary"]
            pid = f"{BATCH}-PRC-{i + 1:03d}{chr(97 + j)}"
            basis = " · ".join(dedupe(b["note"] for b in c["basis"]))[:200]
            if dname in ("modality_subcategory_label", "product_name"):
                to = None
                if dname == "product_name":
                    to = (g.ids.prod.get(norm(c["canonical"])) or {}).get("id")
                else:
                    hit = g.ids.sub_by_label.get((e.get("code"), norm(c["canonical"])))
                    to = hit[0]["id"] if hit else None
                if to is None:
                    continue
                dec = OrderedDict([("kind", "canonical_mapping"), ("target", {"from_ref": frag, "scope": scope}), ("new_value", {"to_id": to})])
                pl = payload(pid, "canonical_mapping", dec["target"], dec["new_value"], f"결정 묶음 4 — 참조 조각 「{frag}」 을 그 참조들(⑨ {len(scope)})에서 {dname} 「{c['canonical']}」({to})로 읽는다(근거: {basis})",
                             locs + [b["locator"] for b in c["basis"] if b.get("locator")], {"proposal_item": f"b4-prc/{i + 1:03d}"})
                n, nl = g.ref_closes(rr, scoped=dict(pl, status="approved"))
                opts.append(opt(f"map_{j + 1}", f"{dname} 「{c['canonical']}」({e.get('code')})로 읽기(그 참조 자리만)", f"풀리는 ⑨ 참조 {n}/{len(rr)}(원장 자리 {nl}) · 근거 {basis[:140]}", pl))
                c["closes"] = n
            else:
                nv = OrderedDict([("canonical", c["canonical"]), ("synonyms", [frag]), ("category", None)])
                pl = payload(pid, "dictionary_add", {"dictionary": dname}, nv, f"결정 묶음 4 — 참조 조각 「{frag}」 을 {dname} 「{c['canonical']}」 의 동의어로(근거: {basis})",
                             locs + [b["locator"] for b in c["basis"] if b.get("locator")], {"proposal_item": f"b4-prc/{i + 1:03d}"})
                n, nl = g.ref_closes(rr, dname, G4._add_syn(c["canonical"], frag))
                note = " · 성분 사전은 §1.3 분해 사전 순서 밖이라 참조를 풀지 않는다" if dname == "ingredient_material" else ""
                opts.append(opt(f"syn_{j + 1}", f"{dname} 「{c['canonical']}」 의 동의어", f"풀리는 ⑨ 참조 {n}/{len(rr)}(원장 자리 {nl}){note} · 근거 {basis[:140]}", pl))
                c["closes"] = n
        cands = [c for c in cands if "closes" in c]
        rec_c = rec_c if rec_c in cands else None
        opts.append(opt("keep", "지금대로(⑨ 미해결)", "결정 없음", None))
        rec = next((o["key"] for o, c in zip(opts, cands) if c is rec_c), None) if rec_c else None
        if rec_c is None and cands and rec_reason.startswith("원장이"):
            rec_reason = "추천 후보가 결정으로 옮겨지지 않는다(추천 없음)"
        title = f"참조 조각 「{frag}」 — " + (f"{', '.join(c['canonical'] for c in cands)} 중 무엇인가?" if cands else "하위분류·제품·부위·성분 사전 후보 없음")
        why = (f"⑨ open 미해결 참조 {len(rr)}(원장 자리 {len(locs)})가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). "
               "하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).")
        items.append(node(f"b4-prc/{i + 1:03d}", "canonical_mapping" if any(o["decision_payload"] and o["decision_payload"]["kind"] == "canonical_mapping" for o in opts) else "dictionary_add",
                          title, why, ev, opts, rec, rec_reason,
                          {"fragment": frag, "references": [{"ref_id": r["ref_id"], "label": r["label"], "hint": r["hint"], "slot": r["slot"]} for r in rr],
                           "candidates": [{"canonical": c["canonical"], "dictionary": c["dictionary"], "code": c["entry"].get("code"), "basis": c["basis"], "closes_references": c.get("closes")} for c in cands]}))
    return items, len(by)


# =====================================================================================
def build_gate_4(S, out_dir):
    g = G4(S, S.ctx["args"].decisions)
    items_a, items_s, n_a, n_s = adverse_items(g)
    items_p, n_p = proc_items(g)
    top = [node("adverse-phrase", "dictionary_add", f"① 부작용 문구 조각 → 사건 사전 동의어(상위 {len(items_a)} / 조각 {n_a})",
                "문구 사전 unlinked 항목에서 사건을 못 찾은 미등록 조각 — 조각이 든 문구 자리 수 순. 하위 항목마다 고른다.", [], [], None, "하위 항목마다", {"subitems": items_a}),
           node("site-material", "dictionary_add", f"② 부작용 문구의 부위·조직·물질 조각(하위 {len(items_s)})",
                "같은 미등록 조각 중 부위(site · 상대 부위) · 물질(adverse_qualifier · 성분) 사전 후보가 있는 것. 하위 항목마다 고른다.", [], [], None, "하위 항목마다", {"subitems": items_s}),
           node("procedure-fragment", "canonical_mapping", f"③ 시술 쪽 남은 조각(⑨ open · 상위 {len(items_p)} / 조각 {n_p})",
                "⑨ open 미해결 참조의 미등록 조각 — 그 조각이 든 open ⑨ 참조 수 순. 하위 항목마다 고른다.", [], [], None, "하위 항목마다", {"subitems": items_p})]
    for it in top:
        for s in it["subitems"]:
            for o in s["options"]:
                p = o["decision_payload"]
                if p:
                    errs = [e for e in validate(dict(p, decided_by="x")) if "decided_by" not in e]
                    if errs:
                        raise AssertionError(f"{s['id']} {o['key']}: {errs}")
            s["already_decided"] = dedupe(x for o in s["options"] for x in g.already(o["decision_payload"]))
            if s["recommended"] is not None and s["recommended"] not in [o["key"] for o in s["options"]]:
                raise AssertionError(f"{s['id']} recommended {s['recommended']} 없음")
    if g.read_fail:
        raise AssertionError(f"원장 읽기 실패 {len(g.read_fail)}: {g.read_fail[:5]}")
    os.makedirs(os.path.join(out_dir, "gate"), exist_ok=True)
    write_json(os.path.join(out_dir, "gate", "batch4.json"), top)
    leaves = [s for it in top for s in it["subitems"]]
    rec = [s for s in leaves if s["recommended"] is not None]

    def eff(s, key):
        o = next((o for o in s["options"] if o["key"] == key), None)
        m = re.search(r"(?:닫히는 문구 자리|풀리는 ⑨ 참조) (\d+)", o["effect"]) if o else None
        return int(m.group(1)) if m else 0
    closes_ph = sum(eff(s, s["recommended"]) for s in rec if not s["id"].startswith("b4-prc"))
    closes_ref = sum(eff(s, s["recommended"]) for s in rec if s["id"].startswith("b4-prc"))
    best_ph = sum(max([eff(s, o["key"]) for o in s["options"] if o["decision_payload"]] or [0]) for s in leaves if not s["id"].startswith("b4-prc"))
    best_ref = sum(max([eff(s, o["key"]) for o in s["options"] if o["decision_payload"]] or [0]) for s in leaves if s["id"].startswith("b4-prc"))
    summ = {"items": len(top), "leaves": len(leaves), "adverse": len(items_a), "site_material": len(items_s), "procedure": len(items_p),
            "recommended": len(rec), "not_recommended": len(leaves) - len(rec), "recommended_by_group": {t["id"]: sum(1 for s in t["subitems"] if s["recommended"]) for t in top},
            "closes_phrases": closes_ph, "closes_references": closes_ref, "closes_phrases_best_option": best_ph, "closes_references_best_option": best_ref,
            "proposals": sum(1 for s in leaves for o in s["options"] if o["decision_payload"]), "evidence": sum(len(s["evidence"]) for s in leaves), "read_fail": len(g.read_fail)}
    write_text(os.path.join(out_dir, "gate", "batch4.md"), render_md(top, summ))
    S.ctx["gate4_items"] = top
    return summ


def write_proposals(S, items, decisions_dir):
    """decisions/batch4-proposed/ — 옵션 결정 본문을 파일 하나씩(status=proposed · 빌드가 읽지 않음) · 같은 항목의 옵션은 서로 배타(게이트에서 하나만)."""
    pd = os.path.join(decisions_dir, PROPOSED_DIR)
    os.makedirs(pd, exist_ok=True)
    keep, res = set(), Counter()
    rows = []
    for it in items:
        for s in it["subitems"]:
            for o in s["options"]:
                p = o["decision_payload"]
                if not p:
                    continue
                fn = f"{p['id']}.json"
                keep.add(fn)
                path = os.path.join(pd, fn)
                body = dict(p, gate_item=s["id"], gate_option=o["key"], gate_recommended=(s["recommended"] == o["key"]), effect=o["effect"])
                if os.path.exists(path):
                    cur = json.load(open(path, encoding="utf-8"))
                    if cur.get("status") != "proposed":
                        res["kept"] += 1
                        continue
                write_json(path, body)
                res["written"] += 1
                rows.append((s["id"], o["key"], "★" if s["recommended"] == o["key"] else "", p["kind"], p["id"], o["label"][:50], o["effect"][:70]))
    for f in os.listdir(pd):
        if f.endswith(".json") and not f.startswith("_") and f not in keep and json.load(open(os.path.join(pd, f), encoding="utf-8")).get("status") == "proposed":
            os.remove(os.path.join(pd, f))
    idx = ["# 결정 묶음 4 — 동의어 제안 (status=proposed · 빌드가 읽지 않음)", "",
           "게이트 `out/gate/batch4.json`(·`.md`)의 옵션마다 결정 파일 하나. **같은 항목(gate_item)의 옵션은 서로 배타** — 게이트에서 하나만 고른다:",
           "`python3 apply_gate.py --gate out/gate/batch4.json --out decisions/batch4/ --answers answers.json [--recommended]`(answers = {항목 id: 옵션 key}).",
           "추천(★)은 원장 병기·영문 대응이 후보 하나만 가리킬 때뿐 — 부분 일치만이면 추천 없음(추정 금지).", "",
           md_table(["항목", "옵션", "추천", "kind", "결정 id", "뜻", "effect"], rows)]
    write_text(os.path.join(pd, "_INDEX.md"), "\n".join(idx))
    return dict(res)


def render_md(items, summ):
    leaves = [(it, s) for it in items for s in it["subitems"]]
    o = ["# 결정 묶음 4 — 동의어 게이트 자료(proposed 를 사용자가 고른다)", "",
         f"① 부작용 문구 조각 {summ['adverse']} · ② 부위·물질 조각 {summ['site_material']} · ③ 시술 조각 {summ['procedure']} — 고를 자리 {summ['leaves']} · 추천 있음 {summ['recommended']} · 추천 없음 {summ['not_recommended']}.",
         f"추천대로 고르면 닫히는 문구 자리 {summ['closes_phrases']} · 풀리는 ⑨ 참조 {summ['closes_references']}(항목마다 가장 많이 닫는 옵션을 고르면 문구 {summ['closes_phrases_best_option']} · 참조 {summ['closes_references_best_option']} — 겹침 미반영 · 항목별 합).",
         "후보 근거는 정규화 부분 일치 · 원장 병기(「A(B)」) · 영문 대응(문헌 같은 레코드)뿐 — 유사도·추정 없음. 추천은 원장 병기·영문 대응이 후보 하나만 가리킬 때만. effect 는 그 결정을 넣은 사전으로 그 자리만 다시 분해해 센 값.",
         "고른 결과: `python3 apply_gate.py --gate out/gate/batch4.json --out decisions/batch4/ --answers answers.json`(answers = {하위 id: 옵션 key}).", "",
         md_table(["자리", "조각", "후보(근거)", "추천", "추천 effect"], [(s["id"], s.get("fragment"), " / ".join(f"{c['canonical']}({','.join(dedupe(b['kind'] for b in c['basis']))})" for c in s.get("candidates", [])) or "—",
                                                                    s["recommended"] or "—", (next((x["effect"] for x in s["options"] if x["key"] == s["recommended"]), "—")[:60] if s["recommended"] else "—")) for _, s in leaves]), ""]
    for it in items:
        o += [f"## {it['id']} — {it['title']}", "", it["why"], ""]
        for s in it["subitems"]:
            o += [f"### {s['id']} — {s['title']}", "", s["why"], "", "**원장 원문**", ""]
            for e in s["evidence"][:10]:
                txt = str(e["text"]).replace("\n", " ")
                o.append(f"- `{e['locator']}` — 「{txt[:140]}」")
            if len(s["evidence"]) > 10:
                o.append(f"- … 외 {len(s['evidence']) - 10} 곳(batch4.json evidence 전부)")
            o.append("")
            o.append(md_table(["옵션", "뜻", "적용되면", "결정"], [(f"**{x['key']}**" if x["key"] == s["recommended"] else x["key"], x["label"], x["effect"],
                                                              (f"{x['decision_payload']['kind']} `{x['decision_payload']['id']}`" if x["decision_payload"] else "결정 없음")) for x in s["options"]]))
            o.append("")
            o.append(f"추천: **{s['recommended'] or '—'}** — {s['recommend_reason']}")
            if s.get("already_decided"):
                o.append(f"이미 승인된 같은 결정: {', '.join(s['already_decided'])}")
            o.append("")
    return "\n".join(o)
