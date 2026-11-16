# -*- coding: utf-8 -*-
"""결정 묶음 3 게이트 자료 — `decisions/batch3-proposed/` 의 proposed 결정을 사람이 고를 수 있게 펼친다(엑소좀 EXO-02·05·06 은 6차 빌드에서 ERD v3.1 kind 로 approved — `decisions/batch3/DEC-2026-11-05-B3-EXO-*` · 제안 폴더에서 빠졌다).

out/gate/batch3.json(웹 페이지 입력) · batch3.md(사람 읽기). 스키마는 2B(`lib/gate2b.py`)와 같다 —
항목 {id, kind, title, why, evidence[{file, locator, source_locator?, text, note?}], options[{key, label, effect, builder_applies_now, decision_payload}],
recommended, recommend_reason, subitems[] …}. decision_payload 는 그 옵션을 고르면 만들어질 결정 파일 본문(ERD v3 §5.2 kind 구조체 완성형 ·
status=proposed)이고, `apply_gate.py --gate out/gate/batch3.json --out decisions/batch3b/` 가 approved · decided_by · decided_at 을 채워 쓴다.
결정 없음(지금대로)은 decision_payload=null.

원문은 브론즈 원장에서 locator 로 직접 읽는다(gate2b.G.ev). recommended 는 원장 문장이 명시할 때만 — 없으면 null(추정 금지).
builder_applies_now = 지금 빌더가 그 결정을 거부·대상 없음 없이 받는가(기록만 kind 는 recorded 로 받는다) · 결정 없음은 null.
"""
import copy
import json
import os
import re
from collections import OrderedDict

from .decisions import RECORD_ONLY, validate
from .gate2b import G, node
from .provenance import leaves, rec_str, sub_leaves
from .util import dedupe, md_table, mkid, norm, write_json, write_text

BATCH = "DEC-2026-11-05-B3B"
BATCH_NOTE = "결정 묶음 3B (게이트 out/gate/batch3.json · 묶음 3 proposed 를 사용자가 고름)"
ERD_REF = "erd-v3.1.md §5.2"
PROPOSED_DIR = "batch3-proposed"
EXCLUDED = {  # 5차 때 ERD v3.1 대기(엑소좀 통합 ②⑤⑥) — 6차에서 approved 로 옮겨 제안 폴더에 없다(남아 있으면 게이트에 올리지 않는다)
    "DEC-2026-11-05-B3-P-EXO-02": "ERD v3.1 대기 — 제품 재분류 kind 없음",
    "DEC-2026-11-05-B3-P-EXO-05": "ERD v3.1 대기 — clinical_rule → 제품·기법 관계 없음",
    "DEC-2026-11-05-B3-P-EXO-06": "ERD v3.1 대기 — 동의어 제거 kind 없음",
}

# 기법을 원장 문장이 명시하는 표기(항목 단위). 부정(「정맥주사 절대 금지」)은 그 기법의 명시로 세지 않는다.
ROUTE_PATTERNS = OrderedDict([
    ("intravenous", re.compile(r"정맥\s?(?:주사|수액|내|공급|또는|/)|(?<![A-Za-z])IV(?![A-Za-z])")),
    ("injection", re.compile(r"(?:근육|피하)\s?(?:/\s?(?:근육|피하))?\s?주사")),
])
NEGATION = re.compile(r"^\s*(?:절대\s*)?금지")


def _sr(refs):
    out, seen = [], set()
    for r in refs:
        k = (r.get("kind"), r.get("ref"))
        if k not in seen:
            seen.add(k)
            out.append(OrderedDict([("kind", r["kind"]), ("ref", r["ref"])]))
    return out


def payload(pid, prop, kind, target, new_value, reason, ledger_refs):
    """결정 파일 본문 — 제안 파일의 source_refs(원장 · erd · brief) + 게이트 근거 원장 locator + 제안 파일 자리."""
    refs = list(prop.get("source_refs", [])) + [{"kind": "ledger", "ref": r} for r in ledger_refs] + \
        [{"kind": "brief", "ref": f"silver-v3/decisions/{PROPOSED_DIR}/{prop['_file']}"}, {"kind": "erd", "ref": ERD_REF}]
    return OrderedDict([("id", pid), ("kind", kind), ("target", target), ("new_value", new_value), ("reason", reason), ("decided_by", None), ("decided_at", None),
                        ("status", "proposed"), ("source_refs", _sr(refs)), ("batch", BATCH_NOTE), ("proposal_id", prop["id"])])


def opt(key, label, effect, pl, applies):
    return OrderedDict([("key", key), ("label", label), ("effect", effect), ("builder_applies_now", applies if pl else None), ("decision_payload", pl)])


class G3(G):
    def __init__(self, S, decisions_dir):
        super().__init__(S, decisions_dir)
        self.read_fail = []
        self.props = OrderedDict()
        pd = os.path.join(decisions_dir, PROPOSED_DIR)
        for f in sorted(os.listdir(pd)) if os.path.isdir(pd) else []:
            if f.endswith(".json") and not f.startswith("_"):
                d = json.load(open(os.path.join(pd, f), encoding="utf-8"))
                d["_file"] = f
                self.props[d["id"]] = d
        self.site_entries = {norm(e["canonical"]): e for e in self.dicts["site"]["entries"]}
        frag_path = os.path.join(S.ctx["args"].out, "gate", "unregistered_fragments.json")
        self.frag_rows = json.load(open(frag_path, encoding="utf-8")) if os.path.exists(frag_path) else []

    def ev(self, lc, note=None):
        o = super().ev(lc, note)
        if str(o["text"]).startswith("<읽기 실패"):
            self.read_fail.append(lc)
        return o

    def already(self, payload):
        """같은 kind·target 의 approved 결정 — dictionary_add 는 target 이 사전 이름뿐이라 정준값·동의어까지 같아야 같은 결정."""
        out = super().already(payload)
        if payload and payload["kind"] == "dictionary_add":
            nv = payload["new_value"]
            keep = []
            for d in self.store:
                if d["id"] in out and norm(d["new_value"].get("canonical")) == norm(nv.get("canonical")) and \
                        {norm(x if isinstance(x, str) else x.get("value")) for x in nv.get("synonyms") or []} <= {norm(x if isinstance(x, str) else x.get("value")) for x in d["new_value"].get("synonyms") or []}:
                    keep.append(d["id"])
            out = keep
        return out

    def leaf_hits(self, fn, needle, root=None):
        """원장 파일 fn 의 문자열 잎 중 needle 을 담은 것 → locator 목록."""
        out = []
        for p, r, v in leaves(self.L[fn]):
            if isinstance(v, str) and needle in v and (root is None or p.startswith(root)):
                out.append(f"{fn}:{p}@{rec_str(r)}")
        return out


# =====================================================================================
# m5-rename
# =====================================================================================
def item_m5(g, prop):
    tx = g.L["taxonomy.json"]["modality"]
    mi = next(i for i, m in enumerate(tx) if m["id"] == "M5")
    m = tx[mi]
    locs_tax = [f"taxonomy.json:modality[].category@{mi}", f"taxonomy.json:modality[].category_en@{mi}", f"taxonomy.json:modality[].name@{mi}"] + \
        [f"taxonomy.json:modality[].subcategories[].label@{mi}/{si}" for si in range(len(m["subcategories"]))]
    mk = g.L["market-pricing.json"]["categories"]
    mki = [i for i, c in enumerate(mk) if c.get("id") == "M5"]
    pp = g.L["procedure-profiles.json"]["profiles"]
    ppi = next(i for i, p in enumerate(pp) if p["id"] == "M5")
    locs_names = ["literature-evidence.json:categories.{code}.name@M5", "extracted.json:{code}.name@M5"] + \
        [f"market-pricing.json:categories[].name@{i}" for i in mki] + [f"procedure-profiles.json:profiles[].name@{ppi}"]
    ent = next(e for e in g.dicts["modality"]["entries"] if e.get("code") == "M5")
    t, nv = prop["target"], prop["new_value"]
    clash = [e["canonical"] for e in g.dicts["modality"]["entries"] if e is not ent and norm(nv["canonical"]) in {norm(v) for v in [e["canonical"]] + [s["value"] for s in e.get("synonyms", [])]}]
    applies = norm(ent["canonical"]) == norm(t["canonical"]) and not clash
    ev = g.evs(locs_tax, "taxonomy M5 계열 이름·하위분류") + g.evs(locs_names, "다른 원장의 M5 이름")
    pl = payload(f"{BATCH}-REN-03", prop, "canonical_rename", copy.deepcopy(t), copy.deepcopy(nv),
                 f"결정 묶음 3B — 계열 M5 정준 이름 「{t['canonical']}」→「{nv['canonical']}」(V3-6 · 옛 이름은 동의어). " + prop["reason"], locs_tax + locs_names)
    syn = [s["value"] for s in ent.get("synonyms", [])]
    opts = [opt("rename", f"「{nv['canonical']}」로 바꾼다", f"modality 사전 M5 정준값 「{ent['canonical']}」→「{nv['canonical']}」 — MOD-M5·CAT-·PRD- id 는 그대로(코드 기반) · 사전 항목 id(DIC-)는 재계산되고 옛 id {ent['id']} 는 renamed_from · 옛 정준값은 동의어로 내린다. 지금 동의어 {len(syn)}(" + ", ".join(syn[:6]) + (" …" if len(syn) > 6 else "") + ")는 그대로", pl, applies),
            opt("keep", f"지금대로 「{ent['canonical']}」", "결정 없음", None, None)]
    return node("m5-rename", "canonical_rename", f"계열 M5 정준 이름을 「{nv['canonical']}」로 바꿀까?",
                "원장 taxonomy 의 M5 이름은 「PRP/자가혈」이고 하위분류가 PRP·PRF(CGF)·MCT·ACT 등이다. 다른 원장은 M5 를 「PRP 피부재생술」(extracted)·「PRP/엑소좀」(market-pricing · procedure-profiles)·「Platelet-rich plasma (PRP) and exosome therapies」(literature) 로 적는다. M1·M3 와 같은 V3-6 이름 바꾸기 후보(사용자 「자가혈이 더 넓은 개념」 · 추천·미확정).",
                ev, opts, None, f"원장 어디에도 「{nv['canonical']}」라는 이름이 없다 — 새 이름은 사람이 정한다(추천 없음). 엑소좀이 섞인 이름(「PRP/엑소좀」)의 동의어 제외는 6차에서 적용됐다(EXO-06 · dictionary_remove).",
                {"proposal_id": prop["id"], "dictionary_entry": {"id": ent["id"], "code": "M5", "canonical": ent["canonical"], "synonyms": syn},
                 "subcategories": [{"id": sc["id"], "label": sc["label"]} for sc in m["subcategories"]]})


# =====================================================================================
# m16-technique
# =====================================================================================
def _routes(g, it, rr):
    """항목 하나 — 원장 문장이 명시하는 기법 표기. {technique: [(locator, 구절)]}"""
    out = OrderedDict()
    for p, r, v in sub_leaves(it, "modality[].subcategories[].items[]", rr):
        if not isinstance(v, str):
            continue
        for tech, pat in ROUTE_PATTERNS.items():
            for mm in pat.finditer(v):
                if NEGATION.match(v[mm.end():]):
                    continue
                a = max(0, mm.start() - 12)
                out.setdefault(tech, []).append((f"taxonomy.json:{p}@{rec_str(r)}", v[a:mm.end() + 12]))
    return out


def item_m16(g, props):
    tx = g.L["taxonomy.json"]["modality"]
    mi = next(i for i, m in enumerate(tx) if m["id"] == "M16")
    m = tx[mi]
    pp = g.L["procedure-profiles.json"]["profiles"]
    ppi = next(i for i, p in enumerate(pp) if p["id"] == "M16")
    fam_locs = [f"procedure-profiles.json:profiles[].mechanism[]@{ppi}/{k}" for k in range(len(pp[ppi]["mechanism"]))] + [f"taxonomy.json:modality[].extracted.mechanism@{mi}"]
    fam_tech = list(dict.fromkeys(pp[ppi]["mechanism"]))
    by_sub = {p["target"]["from_ref"][3:]: p for p in props}
    subs = []
    for si, sc in enumerate(m["subcategories"]):
        if sc["id"] not in by_sub:
            continue
        prop = by_sub[sc["id"]]
        sub_locs = [f"taxonomy.json:modality[].subcategories[].label@{mi}/{si}"] + ([f"taxonomy.json:modality[].subcategories[].description@{mi}/{si}"] if "description" in sc else [])
        ev = g.evs(sub_locs, "하위분류") + g.evs(fam_locs, "계열 M16 기법(R5)·기전")
        scope_items, refs = [], list(sub_locs) + fam_locs
        for ii, it in enumerate(sc["items"]):
            rr = (mi, si, ii)
            cat = mkid("CAT", f"M16|{it['name']}")
            nloc = f"taxonomy.json:modality[].subcategories[].items[].name@{rec_str(rr)}"
            mloc = f"taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@{rec_str(rr)}"
            rt = _routes(g, it, rr)
            route = list(rt)[0] if len(rt) == 1 else ("both" if len(rt) > 1 else None)
            phr = "; ".join(f"{t}: " + " / ".join(dedupe(f"「{x[1]}」" for x in xs)) for t, xs in rt.items())
            ev += g.evs([nloc], f"항목 이름 — 기법 표기 {phr or '없음'}")
            if isinstance(it.get("extracted"), dict) and "mechanism" in it["extracted"]:
                ev += g.evs([mloc], "항목 기전 문장")
                refs.append(mloc)
            route_locs = dedupe(x[0] for xs in rt.values() for x in xs if x[0] != mloc)
            ev += g.evs(route_locs, "기법 표기가 나오는 문장")
            refs += [nloc] + route_locs
            s = g.AM.spec.get(cat)
            scope_items.append(OrderedDict([("catalog_item_id", cat), ("name", it["name"]), ("now_technique", s["technique"] if s else None), ("now_technique_id", s["technique_id"] if s else None),
                                            ("route_stated", route), ("route_phrases", {t: [x[1] for x in xs] for t, xs in rt.items()})]))
        all_scope = [x["catalog_item_id"] for x in scope_items]
        if sorted(all_scope) != sorted(prop["target"]["scope"]):
            raise AssertionError(f"{prop['id']} scope 가 하위분류 {sc['id']} 항목과 다르다")
        prop_tech = next(t["label"] for t in g.ids.tech.values() if mkid("TEC", t["label"]) == prop["new_value"]["to_id"])
        cands = dedupe(fam_tech + [prop_tech] + [x["route_stated"] for x in scope_items if x["route_stated"] in ROUTE_PATTERNS])
        opts, explicit = [], {}
        for tech in cands:
            te = {"id": mkid("TEC", g.ids.tech[norm(tech)]["label"])}
            stated = [x for x in scope_items if x["route_stated"] == tech]
            explicit[tech] = stated
            other = [x for x in scope_items if x["route_stated"] not in (tech, None)]
            none_now = [x for x in scope_items if x["now_technique_id"] == "none"]

            def mk(key, scope, label, extra_eff):
                n_none = sum(1 for x in scope_items if x["catalog_item_id"] in scope and x["now_technique_id"] == "none")
                pl = payload(f"{BATCH}-TEC-{sc['id']}", prop, "canonical_mapping", OrderedDict([("from_ref", f"R5:{sc['id']}"), ("scope", scope)]), OrderedDict([("to_id", te["id"])]),
                             f"결정 묶음 3B — V3-8 하위분류 {sc['id']} 「{sc['label']}」 기본 기법 {tech}(scope {len(scope)}). " + extra_eff, refs)
                eff = f"scope {len(scope)} 항목 중 지금 technique=none 인 {n_none} 튜플의 technique 칸이 {te['id']}({tech}) 로 · R5 하위분류 {sc['id']} → {tech} 엣지(basis canonical_mapping)가 생긴다. " + extra_eff
                opts.append(opt(key, label, eff, pl, n_none > 0))

            note_all = ("원장이 다른 기법이라 적은 항목도 들어간다: " + ", ".join(f"{x['name']}({x['route_stated']})" for x in other) + ". ") if other else ""
            unstated = [x["name"] for x in scope_items if x["route_stated"] is None]
            mk(f"{tech}_all", all_scope, f"{tech} — 하위분류 항목 전부({len(all_scope)})",
               note_all + (f"원장이 기법을 적지 않은 항목 {len(unstated)}: " + ", ".join(unstated) + "." if unstated else ""))
            if stated and len(stated) < len(scope_items):
                rest = [x["name"] for x in scope_items if x not in stated]
                mk(f"{tech}_stated", [x["catalog_item_id"] for x in stated], f"{tech} — 원장이 그렇게 적은 항목만({len(stated)})",
                   f"나머지 {len(rest)}(" + ", ".join(rest) + ")은 technique 그대로.")
        opts.append(opt("keep", "지금대로(technique none)", "결정 없음", None, None))
        full = [t for t in cands if len(explicit[t]) == len(scope_items)]
        best = sorted(((len(v), t) for t, v in explicit.items() if v), reverse=True)
        if full:
            rec, rr_ = f"{full[0]}_all", f"항목 {len(scope_items)} 전부의 원장 문장이 {full[0]} 를 명시한다."
        elif best and (len(best) == 1 or best[0][0] > best[1][0]):
            t = best[0][1]
            rec = f"{t}_stated"
            others = [x for x in scope_items if x["route_stated"] != t]
            rr_ = f"원장 문장이 {t} 를 명시한 항목 {best[0][0]} 만 — " + ", ".join(x["name"] for x in explicit[t]) + ". 나머지는 " + \
                ", ".join(f"{x['name']}({'기법 표기 없음' if x['route_stated'] is None else ('정맥·근육 둘 다' if x['route_stated'] == 'both' else x['route_stated'])})" for x in others) + " 라 넣지 않는다."
        else:
            rec, rr_ = None, "항목 원장 문장이 기법(정맥·근육·피하 주사)을 적지 않는다 — 하위분류 라벨·설명만으로는 기법을 정하지 않는다(추천 없음)."
        subs.append(node(f"m16-technique/{sc['id']}", "canonical_mapping", f"M16 하위분류 {sc['id']} 「{sc['label']}」 항목 {len(scope_items)} 의 기법을 무엇으로 둘까?",
                         "계열 M16 의 R5 기법은 intravenous 하나지만 DCA·지방분해주사처럼 정맥이 아닌 항목이 있어 계열 일괄 상속을 하지 않는다(ERD §9.5.6). V3-8 은 하위분류 단위로 기본 기법을 지정한다 — 항목마다 원장이 적은 기법 표기를 같이 본다.",
                         ev, opts, rec, rr_, {"proposal_id": prop["id"], "subcategory": {"id": sc["id"], "label": sc["label"], "sub_id": g.ids.sub[sc["id"]]["id"]},
                                              "family_technique": fam_tech, "scope_items": scope_items, "route_patterns": {t: p.pattern for t, p in ROUTE_PATTERNS.items()}}))
    return node("m16-technique", "canonical_mapping", f"M16 수액치료 하위분류별 기법 지정(하위 {len(subs)})",
                "V3-8 — 하위분류 단위 기본 기법(canonical_mapping R5:<하위분류 id>). 하위 항목마다 고른다. 기법 후보 = 계열 R5 기법 · 제안 기법 · 항목 원장이 적은 기법.",
                [], [], None, "하위 항목마다", {"subitems": subs})


# =====================================================================================
# site-synonyms
# =====================================================================================
def _zone_sites(g, frag):
    """anatomy-danger-zones 의 zone 중 frag 가 문장에 나오는 것 → (zone 사전 부위 정준값, locators)."""
    out = OrderedDict()
    zs = g.L["anatomy-danger-zones.json"]["zones"]
    syn = {}
    for e in g.dicts["site"]["entries"]:
        for v in [e["canonical"]] + [s["value"] for s in e.get("synonyms", [])]:
            syn.setdefault(norm(v), e["canonical"])
    for lc in g.leaf_hits("anatomy-danger-zones.json", frag, "zones[]"):
        zi = int(lc.rsplit("@", 1)[1].split("/")[0])
        z = zs[zi]
        site = syn.get(norm(z.get("id") or "")) or syn.get(norm(z.get("name_en") or ""))
        out.setdefault(site, []).append(lc)
    return out


def item_site(g, props):
    subs = []
    for i, prop in enumerate(props, 1):
        nv = prop["new_value"]
        canon = nv["canonical"]
        frags = list(nv.get("synonyms") or []) or [canon]
        exists = norm(canon) in g.site_entries
        locs, axis_n, cfl = [], OrderedDict(), []
        for f in frags:
            for r in g.frag_rows:
                if r["fragment"] == f:
                    locs += r["locators"]
                    axis_n[r["axis"]] = axis_n.get(r["axis"], 0) + r["count"]
                    cfl.append(r["conflict_id"])
        zone = OrderedDict()
        for f in frags:
            for s, ls in _zone_sites(g, f).items():
                zone.setdefault(s, OrderedDict())[f] = ls
        zone_locs = dedupe(x for d in zone.values() for ls in d.values() for x in ls)
        prop_locs = [r["ref"] for r in prop.get("source_refs", []) if r["kind"] == "ledger"]
        raw = []
        if not locs:  # 미등록 조각이 아니다 → 원장 전체에서 그 말이 나오는 자리
            for fn in sorted(g.L):
                if fn.endswith(".json"):
                    for f in frags:
                        raw += g.leaf_hits(fn, f)
        ev = g.evs(locs, "조각이 나오는 원장 자리(미등록 ⑧)") + g.evs([x for x in raw if x not in locs], "원장에 그 말이 나오는 자리(미등록 조각 아님)") + \
            g.evs([x for x in zone_locs if x not in locs + raw], "anatomy-danger-zones 의 zone 문장") + g.evs([x for x in prop_locs if x not in locs + raw + zone_locs], "제안 근거")
        refs = dedupe(locs + raw + zone_locs + prop_locs)
        axis_txt = " · ".join(f"{'시술' if a == 'procedure' else '부작용'} 축 {n}" for a, n in axis_n.items()) or "미등록 조각 0"

        def add_payload(target_canon, kind_extra=None):
            v = OrderedDict([("canonical", target_canon), ("category", None)])
            if kind_extra:
                v.update(kind_extra)
            v["synonyms"] = list(nv.get("synonyms") or [])
            return payload(f"{BATCH}-SIT-{i:02d}", prop, "dictionary_add", OrderedDict([("dictionary", "site")]), v,
                           f"결정 묶음 3B — 부위 사전 「{target_canon}」" + (f" += {', '.join(v['synonyms'])}" if v["synonyms"] else " 새 값") + " (해부 이름 → 부위). " + prop["reason"], refs)

        opts = []
        if exists or not nv.get("synonyms"):
            kx = OrderedDict((k, nv[k]) for k in ("site_kind", "kind") if k in nv)
            lab = f"「{canon}」의 동의어로 " + ", ".join(frags) if nv.get("synonyms") else f"새 부위 「{canon}」" + (f"(kind {nv['kind']})" if nv.get("kind") else "")
            eff = (f"부위 사전 「{canon}」({g.site_entries[norm(canon)].get('kind')})에 동의어 " + ", ".join(frags) + " 를 더한다" if exists else
                   f"부위 사전에 새 값 「{canon}」(kind {nv.get('kind')} · site_kind {nv.get('site_kind')})을 세운다 — SIT- 개체가 하나 는다") + \
                f" · 그 조각이 나오는 자리({axis_txt})가 다시 분해된다"
            opts.append(opt("propose", lab, eff, add_payload(canon, kx if not exists else None), True))
        # 다른 부위(≤3) — ① 조각이 anatomy-danger-zones 문장에 나오는 zone 의 부위 ② 부위 이름(「/」 조각)이 조각 안에 있거나 조각을 품음
        # ③ 부위 이름이 조각의 첫 글자로 시작 — 조각이 여럿이면 조각마다 ②·③ 중 하나가 맞아야 한다. 같은 묶음 안은 사전 순.
        alts, basis = [], {}
        for s in zone:
            if s and norm(s) != norm(canon) and s not in alts:
                alts.append(s)
                basis[s] = "zone 문장: " + ", ".join(f"「{f}」" for f in zone[s])
        for rank, test, why in ((2, lambda f, p: p in f or f in p, "부위 이름이 조각 안에 있음"), (3, lambda f, p: p.startswith(f[:1]), "부위 이름이 조각 첫 글자로 시작")):
            for e in g.dicts["site"]["entries"]:
                c = e["canonical"]
                if e.get("kind") == "layer" or norm(c) == norm(canon) or c in alts:
                    continue
                parts = [x.strip() for x in c.split("/")]
                if all(any(test(f, p) or (rank == 3 and (p in f or f in p)) for p in parts) for f in frags):
                    alts.append(c)
                    basis[c] = why
        alts = alts[:3]
        if nv.get("synonyms"):
            for c in alts:
                why = basis[c]
                opts.append(opt(f"alt:{c}", f"「{c}」의 동의어로 " + ", ".join(frags),
                                f"부위 사전 「{c}」({g.site_entries[norm(c)].get('kind')})에 동의어 " + ", ".join(frags) + f" 를 더한다(후보 근거 — {why}) · 그 조각이 나오는 자리({axis_txt})가 다시 분해된다",
                                add_payload(c), True))
        opts.append(opt("keep", "지금대로(미등록 유지)", "결정 없음 — ⑧ open 유지" if cfl else "결정 없음", None, None))
        # 추천: 조각마다 zone 문장이 있고 그 zone 이 전부 제안 부위일 때만
        ok = bool(nv.get("synonyms")) and all(f in zone.get(canon, {}) for f in frags) and all(s == canon for s in zone)
        if ok:
            rec = "propose"
            rr_ = "anatomy-danger-zones 의 「" + canon + "」 zone 문장이 " + ", ".join(f"「{f}」" for f in frags) + " 를 그 zone 안에서 적는다(다른 zone 에는 안 나온다)."
        else:
            rec = None
            if not zone:
                rr_ = "해부 문서(anatomy-danger-zones)에 " + ", ".join(f"「{f}」" for f in frags) + " 가 없다 — 어느 부위인지 원장이 말하지 않는다(추천 없음)."
            else:
                rr_ = "zone 문장이 " + "; ".join(f"「{s}」 zone 에 " + ", ".join(f"「{f}」" for f in d) for s, d in zone.items()) + " — " + \
                    ("제안 부위 하나로 모이지 않는다" if any(s != canon for s in zone) else "조각 일부만 나온다") + "(추천 없음)."
            if not nv.get("synonyms"):
                rr_ = "새 region 값(ERD §12 후보)이다 — 원장은 「바디」를 고민(problem P12)·목적 라벨로만 갖고 부위로 정하지 않는다(추천 없음)." if canon == "바디" else rr_
        title = (f"해부 이름 " + ", ".join(f"「{f}」" for f in frags) + f" 를 부위 「{canon}」로 읽을까?") if nv.get("synonyms") else f"부위 사전에 region 「{canon}」을 세울까?"
        subs.append(node(f"site-synonyms/{i:02d}", "dictionary_add", title,
                         "해부 이름·부위 조각이 부위 사전에 없어 미등록(⑧)이거나 사전 정합이 안 맞는다. 「교근 → 사각턱」(B3-SIT-01)과 같은 원칙으로 부위 동의어를 더할지 사람이 정한다.",
                         ev, opts, rec, rr_, {"proposal_id": prop["id"], "fragments": frags, "axis_counts": axis_n, "conflict_ids": cfl,
                                              "zone_sites": {str(s): list(d) for s, d in zone.items()}, "now_site": (g.site_entries[norm(canon)]["id"] if exists else None)}))
    return node("site-synonyms", "dictionary_add", f"해부 이름 → 부위 동의어(하위 {len(subs)})", "사용자 2026-11-05 「광경근→목 · 코끝→코 등」 — 미등록 조각에서 추출한 제안. 하위 항목마다 고른다.",
                [], [], None, "하위 항목마다", {"subitems": subs})


# =====================================================================================
# air-embolism-qualifier
# =====================================================================================
def _unit3(g, t):
    """옛 네 칸 제안 튜플(event_id, site_id, course_id, qualifier_id) → v3.1 세 칸 + 경과(R15) · 상대 부위는 none."""
    def lab(table, i):
        return next((e["label"] for e in table.values() if e["id"] == i), None)
    ev = lab(g.ids.event, t["event_id"])
    qu = lab(g.ids.qualifier, t.get("qualifier_id")) if t.get("qualifier_id", "none") != "none" else "none"
    sid = t.get("site_id", "none")
    rel = lab(g.ids.rsite, sid) if sid != "none" else None
    if rel:
        sid = "none"
    si = "none" if sid == "none" else next((e["label"] for e in g.ids.site.values() if e["id"] == sid), sid)
    co = lab(g.ids.course, t["course_id"]) if t.get("course_id") else None
    return {"event_id": t["event_id"], "site_id": sid, "qualifier_id": t.get("qualifier_id", "none")}, f"({ev}, {si}, {qu})", ([co] if co and co != "미상" else [])


def item_air(g, prop):
    from .units31 import unit_id3
    lc = prop["target"]["locator"]
    A = g.ctx["adv"]
    exprs = dedupe(r["locator"] for r in A["phrase_occurrences"] if not r.get("translation") and "공기색전" in str(r["text"]))
    ledger = [r["ref"] for r in prop.get("source_refs", []) if r["kind"] == "ledger"]
    ev = g.evs([lc], "대상 complications 이름") + g.evs([x for x in exprs if x not in ledger], "「공기색전」이 든 문구") + g.evs([x for x in ledger if x != lc and x not in exprs], "제안 근거")
    now = []
    for u in g.AU.name_units.get(lc, []):
        x = g.AU.units[u]
        now.append(f"({x['event']}, {x.get('site') or 'none'}, {x.get('qualifier') or 'none'})")
    conv = [_unit3(g, t) for t in prop["new_value"]["tuples"]]
    tup = [c[0] for c in conv]
    labs = [c[1] for c in conv]
    courses = dedupe(x for c in conv for x in c[2])
    exist = [unit_id3(t["event_id"], t["site_id"], t["qualifier_id"]) in g.AU.units for t in tup]
    nv = {"tuples": tup, "courses": courses or None}
    pl = payload(f"{BATCH}-ADV-01", prop, "adverse_tuple_assign", copy.deepcopy(prop["target"]), nv,
                 "결정 묶음 3B — " + prop["reason"] + " (v3.1: 세 칸 단위 + R15 경과로 옮김)", [g.erd2src.get(x, x) for x in [lc] + exprs])
    opts = [opt("assign", "지정 → " + " + ".join(labs), "이 이름의 단위가 " + " + ".join(labs) + " 로 바뀐다(" + ", ".join(f"{l} {'있는 단위' if e else '결정이 세움'}" for l, e in zip(labs, exist)) +
                ") · 「카테터 관련」 조각은 이 이름의 단위에 남지 않는다" + (f" · R15 경과 {courses}" if courses else "") + ". 지금 " + (" + ".join(now) or "단위 없음"), pl, True),
            opt("keep", "지금대로(" + (" + ".join(now) or "단위 없음") + ")", "결정 없음", None, None)]
    return node("air-embolism-qualifier", "adverse_tuple_assign", "complications 「공기색전·카테터 관련 감염」[M16]에 (색전, none, 공기) 수식 단위를 세울까?",
                "V3-1 수식 칸으로 「공기색전」은 (색전 · 수식 공기)로 읽힌다(문구 「공기색전 의심」은 이미 그렇게 갈린다). 이 이름은 「카테터 관련」 조각 때문에 사건 하나로 다 읽히지 않는다 — 「카테터 관련」은 감염의 원인 문맥이고 사전 밖 조각이라 버릴지·사전에 넣을지는 사람이 정한다.",
                ev, opts, None, "원장은 「카테터 관련」을 어떻게 다룰지(버림·부위·수식) 말하지 않는다 — 감염 단위에서 그 조각을 빼는 판단이 남아 있다(추천 없음).",
                {"proposal_id": prop["id"], "now": now, "proposed": labs, "target_kind_note": "target.kind=raw_name — complications 이름 ERD 꼴 locator(@M16/10) · v3.1 세 칸(옛 제안의 경과 미상은 엣지 null)"})


# =====================================================================================
# 기록·제안(scope_review · edge_create 등 나머지)
# =====================================================================================
def item_records(g, props):
    subs = []
    for prop in props:
        ledger = [r["ref"] for r in prop.get("source_refs", []) if r["kind"] == "ledger"]
        ev = g.evs(ledger, "제안 근거")
        if prop["id"].endswith("NEC-01"):
            extra = [g.erd2src.get(r["locator"], r["locator"]) for r in g.ctx["adv"]["complications"] if "피부 괴사" in str(r["text"])] + \
                [g.erd2src.get(r["locator"], r["locator"]) for r in g.ctx["adv"]["phrase_occurrences"] if not r.get("translation") and "피부 괴사" in str(r["text"])]
            ev += g.evs([x for x in dedupe(extra) if x not in ledger], "「피부 괴사」가 든 이름·표현")
            ledger += [x for x in dedupe(extra) if x not in ledger]
        suf = prop["id"].replace("DEC-2026-11-05-B3-P-", "")
        pl = payload(f"{BATCH}-{suf}", prop, prop["kind"], copy.deepcopy(prop["target"]), copy.deepcopy(prop["new_value"]), "결정 묶음 3B — " + prop["reason"], [x for x in ledger if x not in [r["ref"] for r in prop.get("source_refs", [])]])
        rec_only = prop["kind"] in RECORD_ONLY
        opts = [opt("record", "기록만 확인", ("기록만 — 빌드 값은 바뀌지 않는다(결정 저장소에 approved 로 남고 적용 로그는 recorded)" if rec_only else f"{prop['kind']} 결정으로 쓴다"), pl, True),
                opt("keep", "지금대로(제안으로 둔다)", "결정 없음", None, None)]
        disp = prop["new_value"].get("disposition") or json.dumps(prop["new_value"], ensure_ascii=False)
        subs.append(node(f"records/{suf}", prop["kind"], f"{prop['target'].get('review_item') or prop['id']} — 기록으로 남길까?",
                         disp, ev, opts, None, "기록만 kind — 값 판단이 아니라 ERD 개정 기록이라 사람이 확인한다(추천 없음).", {"proposal_id": prop["id"], "target": prop["target"]}))
    return node("records", "scope_review", f"그 밖 기록·제안(하위 {len(subs)})", "빌더가 값을 바꾸지 않는 기록만 kind — 확인하면 결정 저장소에 approved 로 남는다.",
                [], [], None, "하위 항목마다", {"subitems": subs})


def leaves_of(items):
    for it in items:
        if it.get("subitems"):
            for s in it["subitems"]:
                yield it, s
        else:
            yield it, it


def build_gate_3(S, out_dir):
    g = G3(S, S.ctx["args"].decisions)
    props = [p for pid, p in g.props.items() if pid not in EXCLUDED]
    used = set()

    def take(pred):
        xs = [p for p in props if pred(p) and p["id"] not in used]
        used.update(p["id"] for p in xs)
        return xs

    items = []
    m5 = take(lambda p: p["kind"] == "canonical_rename")
    for p in m5:
        items.append(item_m5(g, p))
    tec = take(lambda p: p["kind"] == "canonical_mapping" and str(p["target"].get("from_ref", "")).startswith("R5:M16"))
    if tec:
        items.append(item_m16(g, tec))
    sit = take(lambda p: p["kind"] == "dictionary_add" and p["target"].get("dictionary") == "site")
    if sit:
        items.append(item_site(g, sit))
    adv = take(lambda p: p["kind"] == "adverse_tuple_assign")
    for p in adv:
        items.append(item_air(g, p))
    rest = take(lambda p: True)
    if rest:
        items.append(item_records(g, rest))
    for it, s in leaves_of(items):
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
    write_json(os.path.join(out_dir, "gate", "batch3.json"), items)
    write_text(os.path.join(out_dir, "gate", "batch3.md"), render_md(items, [(pid, why) for pid, why in EXCLUDED.items() if pid in g.props]))
    n_leaf = sum(1 for _ in leaves_of(items))
    rec = sum(1 for _, s in leaves_of(items) if s["recommended"] is not None)
    n_ev = sum(len(s["evidence"]) for _, s in leaves_of(items))
    return {"items": len(items), "leaves": n_leaf, "subitems": sum(len(i.get("subitems") or []) for i in items), "recommended": rec, "not_recommended": n_leaf - rec,
            "proposals": len(props), "excluded": len([p for p in g.props if p in EXCLUDED]), "evidence": n_ev, "read_fail": len(g.read_fail)}


def render_md(items, excluded):
    leaves = list(leaves_of(items))
    rec = sum(1 for _, s in leaves if s["recommended"] is not None)
    o = ["# 결정 묶음 3 — 게이트 자료(proposed 를 사용자가 고른다)", "",
         f"상위 {len(items)} · 고를 자리(하위 항목 · 하위 없는 항목) {len(leaves)} · 추천 있음 {rec} · 추천 없음 {len(leaves) - rec}.",
         "원문은 브론즈 원장에서 locator 로 직접 읽었다. 추천은 원장 문장이 명시할 때만 — 없으면 「—」. 고른 결과는 "
         "`python3 apply_gate.py --gate out/gate/batch3.json --out decisions/batch3b/ --answers answers.json` 으로 결정 파일이 된다(answers = {항목 id 또는 하위 id: 옵션 key}).", ""]
    if excluded:
        o += ["게이트에 올리지 않은 제안: " + " · ".join(f"{pid.replace('DEC-2026-11-05-B3-P-', '')}({why})" for pid, why in excluded), ""]
    o += [md_table(["자리", "질문", "추천"], [(s["id"], s["title"], s["recommended"] or "—") for _, s in leaves]), ""]
    for it in items:
        o += [f"## {it['id']} — {it['title']}", "", it["why"], ""]
        for s in (it.get("subitems") or [it]):
            if s is not it:
                o += [f"### {s['id']} — {s['title']}", "", s["why"], ""]
            o += ["**원장 원문**", ""]
            ev = s["evidence"]
            for e in ev[:14]:
                txt = str(e["text"]).replace("\n", " ")
                o.append(f"- `{e['locator']}` — 「{txt[:160]}」" + (f" ({e['note']})" if e.get("note") else ""))
            if len(ev) > 14:
                o.append(f"- … 외 {len(ev) - 14} 곳(batch3.json evidence 전부)")
            o.append("")
            o.append(md_table(["옵션", "뜻", "적용되면", "결정", "지금 빌더"], [(f"**{x['key']}**" if x["key"] == s["recommended"] else x["key"], x["label"], x["effect"],
                                                                         (f"{x['decision_payload']['kind']} `{x['decision_payload']['id']}`" if x["decision_payload"] else "결정 없음"),
                                                                         {True: "적용", False: "⚠ 대상 없음", None: "—"}[x["builder_applies_now"]]) for x in s["options"]]))
            o.append("")
            o.append(f"추천: **{s['recommended'] or '—'}** — {s['recommend_reason']}")
            if s.get("already_decided"):
                o.append(f"이미 승인된 같은 결정: {', '.join(s['already_decided'])}")
            o.append("")
    return "\n".join(o)
