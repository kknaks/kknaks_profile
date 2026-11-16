# -*- coding: utf-8 -*-
"""결정 묶음 1 제안 — status=proposed(빌드가 읽지 않음). 제안마다 원장·조사 근거 locator 필수 · 추정 금지.

1. dictionary_add(product_name) — step1 의 제품·장비 kind + 허가/웹 근거 locator 가 있는 항목
2. dictionary_add(동의어) — 발주서가 지정한 미등록 조각 묶음. 조각이 지정 축 사전의 값과 「괄호 밖 일치 · 괄호 안 일치 · 조합 멤버 일치」로
   닿을 때만(한 계열 사슬 안의 후보 하나). 후보 0 · 다른 계열 둘 이상이면 제안하지 않는다.
3. stopwords — 결정 파일이 아니라 ERD 개정 후보(report 에만)
4. ERD-FROZEN.md 「결정으로 넘긴 것」 — 빈 템플릿(kind 만)
"""
import re
from collections import OrderedDict, defaultdict

from .core import dref
from .provenance import P, loc, leaves, records, rec_str
from .util import mkid, norm, dedupe

PRODUCT_KINDS = {"제품", "장비", "제품(의료기기)", "제품(의약품)"}
EXCLUDE_KINDS = {"확인 불가", "병원 메뉴명", "업체명"}
WEB_TYPES = {"웹(web)", "웹(이번 패스)"}
MCODE = re.compile(r"^M\d+$")
BUNDLE = "DEC-2026-11-04-B1"

SYNONYM_GROUPS = [
    {"fragments": ["전체얼굴", "풀페이스"], "axis": ["site"], "new_canonical": "얼굴 전체", "phrase": r"얼굴\s*전체|전체\s*얼굴",
     "why": "발주서: 전체얼굴·풀페이스 → 부위 「얼굴 전체」"},
    {"fragments": ["HIFU", "RF", "MTS", "필링", "LED", "토닝", "크라이오", "HIFES", "수액", "줄기세포", "CO2", "Nd:YAG", "혈관레이저", "다이오드"],
     "axis": ["modality_subcategory_label", "modality"], "why": "발주서: 해당 하위분류 라벨(근거가 계열 라벨뿐이면 계열)"},
    {"fragments": ["HA", "CaHA", "PLLA", "PCL", "PDO"], "axis": ["ingredient_material"], "why": "발주서: 성분 사전"},
]
STOPWORDS = ["회", "차", "터치업", "유지", "집중", "연말", "하반기", "가을", "관리", "케어", "과도한", "빈도"]

TEMPLATES = [
    ("botox-product-vs-modality", "canonical_mapping", "「보톡스」 product vs modality(검토 1-E)"),
    ("excel-v-plus", "tuple_assign", "엑셀V+"),
    ("same-three-cells-21", "fold_approve", "같은 세 칸 다른 anchor 21조"),
    ("event-split", "event_split", "사건 동의어 분리(과민반응·동상·지방괴사·섬유화·공기색전)"),
    ("paren-synonym-unknown-tuples-4", "adverse_tuple_assign", "괄호 동의어 미상 튜플 4"),
    ("two-event-candidates-10", "adverse_tuple_assign", "같은 사건 후보 둘인 표현 10"),
    ("injection-site-erythema-edema", "adverse_tuple_assign", "「주사 부위 홍반·부종」 부종 부위"),
    ("technique-inheritance-9", "canonical_mapping", "기법 상속 후보 9계열(R5)"),
    ("slash-together-or", "tuple_assign_multi", "`/` 함께/또는"),
    ("volnewmer-m4-m9", "conflict_close", "볼뉴머 M4/M9"),
    ("mface-like", "tuple_assign", "엠페이스류"),
]
TEMPLATE_SHAPES = {
    "canonical_mapping": ({"from_ref": None, "scope": []}, {"to_id": None}),
    "tuple_assign": ({"catalog_item_id": None, "ref_id": None}, {"what_kind": None, "what_id": None, "site_id": None, "technique_id": None}),
    "tuple_assign_multi": ({"catalog_item_id": None, "ref_id": None}, {"tuples": []}),
    "adverse_tuple_assign": ({"locator": None, "kind": None}, {"tuples": []}),
    "fold_approve": ({"anchors": []}, {"keep_anchor": None}),
    "event_split": ({"event": None}, {"new_events": []}),
    "conflict_close": ({"conflict_key": {"kind": None, "locators": []}}, {"verdict": None, "note": ""}),
}


def product_proposals(S):
    L = S.ctx["L"]
    D = S.ctx["dicts"]
    taken = {}
    items_by_name = {}
    for e in D["catalog_item_name"]["entries"]:
        items_by_name[norm(e["canonical"])] = e
    for name in ("product_name", "modality", "modality_subcategory_label", "site"):
        for e in D[name]["entries"]:
            for v in [e["canonical"]] + [s["value"] for s in e.get("synonyms", [])]:
                taken.setdefault(norm(v), name)
    props, excluded = OrderedDict(), []
    for r, it in records(L["step1-products.json"], "items[]"):
        kind = it["1_identity"]["kind"]
        dn = it["2_names"]["display_name"]
        base = {"ledger_id": it["ledger_id"], "display_name": dn, "kind": kind, "locator": loc(P("step1-products.json", "items[].2_names.display_name", r))}
        pid = S.ctx["step1_product"][r[0]]
        if S.E["product"][pid]["attrs"].get("origin", [{}])[0].get("value") == "ledger":
            excluded.append(dict(base, reason="이미 원장 제품(product_name 사전)에 닿음 — 추가 불필요"))
            continue
        if kind in EXCLUDE_KINDS:
            excluded.append(dict(base, reason=f"1_identity.kind 「{kind}」 — 발주서 제외 목록"))
            continue
        if kind not in PRODUCT_KINDS:
            excluded.append(dict(base, reason=f"1_identity.kind 「{kind}」 — 발주서 포함 kind(제품·장비·제품(의료기기)·제품(의약품)) 밖"))
            continue
        if not it.get("active", True):
            excluded.append(dict(base, reason="active=false(조사 산출물에서 비활성 항목)"))
            continue
        ev = []
        for j, lic in enumerate(it["4_license"].get("licenses") or []):
            key = "source" if lic.get("source") else "license_no"
            ev.append({"kind": "license", "ref": loc(P("step1-products.json", f"items[].4_license.licenses[].{key}", r + (j,))), "detail": f"{lic.get('license_no')} · {lic.get('official_name') or lic.get('item') or ''}".strip()})
        for j, e in enumerate(it.get("evidence") or []):
            if isinstance(e, str) and re.match(r"^(web:\s*)?https?://", e.strip()):
                ev.append({"kind": "web", "ref": loc(P("step1-products.json", "items[].evidence[]", r + (j,))), "detail": e})
            elif isinstance(e, dict) and e.get("type") in WEB_TYPES:
                for k, u in enumerate(e.get("urls") or []):
                    ev.append({"kind": "web", "ref": loc(P("step1-products.json", "items[].evidence[].urls[]", r + (j, k))), "detail": u})
        if not ev:
            excluded.append(dict(base, reason="허가 건(licenses[])·웹 근거(web URL) locator 없음"))
            continue
        code = it["family"]["code"] if MCODE.match(str(it["family"]["code"])) else "survey"
        key = norm(dn)
        if norm(dn) in taken:
            excluded.append(dict(base, reason=f"대표 이름이 이미 사전 {taken[norm(dn)]} 값과 같다(정규화 일치) — 제품 사전에 넣으면 다른 사전 값과 겹친다(사람 판단)"))
            continue
        p = props.setdefault(key, {"codes": [], "canonical": dn, "synonyms": [], "items": [], "evidence": [], "kind": set()})
        if code not in p["codes"]:
            p["codes"].append(code)
        p["items"].append(base)
        p["kind"].add(kind)
        p["evidence"] += ev
        cand = []
        if it["2_names"].get("ledger_name"):
            cand.append((it["2_names"]["ledger_name"], loc(P("step1-products.json", "items[].2_names.ledger_name", r))))
        for j, s in enumerate(it["2_names"].get("search_names") or []):
            cand.append((s["name"], loc(P("step1-products.json", "items[].2_names.search_names[].name", r + (j,)))))
        for v, lc in cand:
            if norm(v) == norm(dn) or any(norm(v) == norm(x[0]) for x in p["synonyms"]):
                continue
            p["synonyms"].append((v, lc))
    # 동의어 충돌(다른 제안·기존 사전) 제거
    count = defaultdict(int)
    for p in props.values():
        for v, _ in p["synonyms"]:
            count[norm(v)] += 1
    out = []
    for i, (key, p) in enumerate(props.items()):
        syn, dropped = [], []
        for v, lc in p["synonyms"]:
            if norm(v) in taken:
                dropped.append({"value": v, "locator": lc, "why": f"이미 사전 {taken[norm(v)]} 값"})
            elif norm(v) in items_by_name and norm(v) != norm(p["canonical"]):
                dropped.append({"value": v, "locator": lc, "why": f"다른 분류 항목 이름 「{items_by_name[norm(v)]['canonical']}」 과 같다 — 그 항목의 what 을 바꾸게 된다"})
            elif count[norm(v)] > 1 or any(norm(v) == norm(q["canonical"]) for q in props.values()):
                dropped.append({"value": v, "locator": lc, "why": "다른 제안 제품과 겹치는 이름"})
            else:
                syn.append((v, lc))
        codes = sorted(p["codes"], key=lambda c: (c == "survey", int(c[1:]) if c.startswith("M") and c[1:].isdigit() else 0))
        code = "|".join(c for c in codes if c != "survey") or "survey"
        item_note = f" · 분류 항목 「{items_by_name[norm(p['canonical'])]['canonical']}」 이름과 같다 — 승인되면 그 항목 튜플의 what 이 이 제품이 된다(겹침 규칙 8-11: 참조 자리에서는 항목 우선)" if norm(p["canonical"]) in items_by_name else ""
        refs = [{"kind": "ledger", "ref": x["locator"]} for x in p["items"]] + [{"kind": "ledger", "ref": e["ref"]} for e in p["evidence"]] + [{"kind": "ledger", "ref": lc} for _, lc in syn] + [{"kind": "brief", "ref": "silver-build-brief.md 결정 묶음 1-1"}]
        out.append(OrderedDict([("id", f"{BUNDLE}-PRD-{i + 1:03d}"), ("kind", "dictionary_add"), ("target", {"dictionary": "product_name"}),
                                ("new_value", {"canonical": p["canonical"], "synonyms": [v for v, _ in syn], "category": None, "code": code}),
                                ("reason", f"step1 조사 산출물 — 1_identity.kind {sorted(p['kind'])} · 근거 {len([e for e in p['evidence'] if e['kind'] == 'license'])} 허가 건 · {len([e for e in p['evidence'] if e['kind'] == 'web'])} 웹 · ledger_id {', '.join(x['ledger_id'] for x in p['items'])}{item_note}"),
                                ("decided_by", None), ("decided_at", None), ("status", "proposed"), ("source_refs", refs),
                                ("evidence", p["evidence"]), ("synonyms_dropped", dropped)]))
    return out, excluded


def _paren_split(v):
    m = re.match(r"^\s*(.*?)\s*\(([^()]*)\)\s*(.*)$", v)
    if not m:
        return v.strip(), None
    return (m.group(1) + " " + m.group(3)).strip(), m.group(2).strip()


def _members(v):
    return [x.strip() for x in re.split(r"[/+·,]", v) if x.strip()]


def synonym_proposals(S):
    """조각 → 지정 축 사전 값(근거 locator) — 한 계열 사슬 안의 후보 하나일 때만."""
    D = S.ctx["dicts"]
    di = S.ctx["dic_index"]
    gate = {c["fragment"]: c for c in S.ctx["unreg_gate"] if c["axis"] == "procedure"}
    out, not_proposed = [], []
    n = 0
    for g in SYNONYM_GROUPS:
        if g.get("new_canonical"):
            occ_refs = []
            for f in g["fragments"]:
                c = gate.get(f)
                if c:
                    occ_refs += [f"{v['source_file']}:{v['source_path']}@{v['rec']}" for v in c["values"]]
            phrase = []
            for fn in sorted(S.ctx["L"]):
                for p, r, v in leaves(S.ctx["L"][fn]):
                    if isinstance(v, str) and len(v) < 80 and re.search(g["phrase"], v):
                        phrase.append(loc(P(fn, p, r)))
            frs = [f for f in g["fragments"] if gate.get(f)]
            if not frs or not phrase:
                for f in g["fragments"]:
                    not_proposed.append({"fragment": f, "why": "원장에 그 라벨(「얼굴 전체」류) 문자열이 없다"})
                continue
            n += 1
            out.append(OrderedDict([("id", f"{BUNDLE}-SYN-{n:03d}"), ("kind", "dictionary_add"), ("target", {"dictionary": g["axis"][0]}),
                                    ("new_value", {"canonical": g["new_canonical"], "synonyms": frs, "category": None, "site_kind": "taxonomy_site_label"}),
                                    ("reason", f"{g['why']} — 조각 {frs} 는 원장에서 부위 수식(괄호·앞말)으로 쓰였고, 「얼굴 전체/전체 얼굴」 문자열이 원장에 {len(phrase)} 곳. 사전 site 의 「얼굴」과는 별개 정준값으로 둔다(같은지는 사람 판단)"),
                                    ("decided_by", None), ("decided_at", None), ("status", "proposed"),
                                    ("source_refs", [{"kind": "ledger", "ref": x} for x in dedupe(phrase + occ_refs)] + [{"kind": "brief", "ref": "silver-build-brief.md 결정 묶음 1-2"}]),
                                    ("evidence", {"label_phrase_locators": phrase, "fragment_occurrence_locators": dedupe(occ_refs)})]))
            continue
        for f in g["fragments"]:
            c = gate.get(f)
            if not c:
                not_proposed.append({"fragment": f, "why": "1차 빌드 시술 축 미등록 조각에 없다"})
                continue
            exact = [(ax, e["canonical"]) for ax in g["axis"] for e in D[ax]["entries"] if norm(f) in {norm(e["canonical"])} | {norm(x["value"]) for x in e.get("synonyms", [])}]
            if exact:
                order = S.ctx["erd"]["resolve_rules"]["step2_decompose"]["dictionary_order"]
                not_proposed.append({"fragment": f, "why": f"이미 사전 값({', '.join(f'{a}:{b}' for a, b in exact)}) — 추가할 것 없음. 미등록인 까닭은 §1.3 분해 사전 순서 {order}+modality 에 그 사전이 없어서(ERD 개정 후보 · report)"})
                continue
            cands = []
            for ax in g["axis"]:
                for ei, e in enumerate(D[ax]["entries"]):
                    vals = [("canonical", e["canonical"], dref(ax, e, "canonical")[0])] + [("synonym", s["value"], dref(ax, e, f"synonym:{s['value']}")[0]) for si, s in enumerate(e.get("synonyms", []))]
                    for vk, v, ptr_ in vals:
                        outer, inner = _paren_split(v)
                        rule = None
                        if norm(outer) == norm(f) and inner is not None:
                            rule = f"괄호 밖 일치 「{v}」"
                        elif inner is not None and norm(inner) == norm(f):
                            rule = f"괄호 안 일치 「{v}」"
                        elif any(norm(x) == norm(f) for x in _members(outer)) or (inner is not None and any(norm(x) == norm(f) for x in _members(inner))):
                            rule = f"조합 멤버 일치 「{v}」"
                        if rule and norm(v) != norm(f):
                            cands.append({"dictionary": ax, "canonical": e["canonical"], "code": e.get("code"), "rule": rule, "pointer": ptr_, "value": v})
            chains = {str(x.get("code")).split("|")[0] if x.get("code") else None for x in cands}
            if not cands:
                not_proposed.append({"fragment": f, "why": f"지정 축({', '.join(g['axis'])}) 사전 값과 괄호 밖·괄호 안·조합 멤버 일치가 없다 — 근거 없음"})
                continue
            if len(chains) > 1:
                not_proposed.append({"fragment": f, "why": "후보가 둘 이상 계열에 걸친다: " + " · ".join(f"{x['dictionary']}:{x['canonical']}[{x.get('code')}]" for x in cands)})
                continue
            # 한 계열 사슬 — 가장 구체(하위분류 > 계열 · 성분은 단일)
            pick = sorted(cands, key=lambda x: ({"modality_subcategory_label": 0, "ingredient_material": 0, "modality": 1, "site": 0}.get(x["dictionary"], 2), x["canonical"]))
            distinct = dedupe((x["dictionary"], x["canonical"]) for x in pick if x["dictionary"] == pick[0]["dictionary"])
            if len(distinct) > 1:
                not_proposed.append({"fragment": f, "why": "같은 축에 후보 둘 이상: " + " · ".join(f"{a}:{b}" for a, b in distinct)})
                continue
            t = pick[0]
            label_locs = []
            src_paths = {"modality_subcategory_label": [("taxonomy.json", "modality[].subcategories[].label")], "modality": None, "ingredient_material": None, "site": None}
            for e in D[t["dictionary"]]["entries"]:
                if e["canonical"] != t["canonical"]:
                    continue
                for s in e.get("sources", []) + [s for sy in e.get("synonyms", []) if sy["value"] == t["value"] for s in sy.get("sources", [])]:
                    if s.get("file") in S.ctx["L"]:
                        for p, r, v in leaves(S.ctx["L"][s["file"]]):
                            if p == s["path"] and isinstance(v, str) and (norm(v) == norm(t["value"]) or norm(v) == norm(t["canonical"]) or (norm(f) in [norm(m) for m in _members(v)])):
                                label_locs.append(loc(P(s["file"], p, r)))
            label_locs = dedupe(label_locs)
            occ_refs = [f"{v['source_file']}:{v['source_path']}@{v['rec']}" for v in c["values"]]
            if not label_locs:
                not_proposed.append({"fragment": f, "why": f"후보 {t['dictionary']}:{t['canonical']} 의 원장 라벨 locator 를 찾지 못함"})
                continue
            new_canon = t["canonical"]
            syns = [f]
            n += 1
            note = ""
            if t["dictionary"] == "ingredient_material":
                note = " · 성분 사전은 §1.3 분해 사전 순서에 없어 승인돼도 시술 튜플은 바뀌지 않는다(분해에 쓰려면 ERD 개정 — report)"
            if t["dictionary"] == "modality" and "modality_subcategory_label" in g["axis"]:
                note += " · 하위분류 라벨 근거는 없고 계열 라벨에만 근거가 있어 계열 동의어로 제안"
            out.append(OrderedDict([("id", f"{BUNDLE}-SYN-{n:03d}"), ("kind", "dictionary_add"), ("target", {"dictionary": t["dictionary"]}),
                                    ("new_value", {"canonical": new_canon, "synonyms": syns, "category": None} if not (t["dictionary"] == "ingredient_material" and norm(new_canon) == norm(f)) else {"canonical": new_canon, "synonyms": [], "category": None}),
                                    ("reason", f"{g['why']} — 조각 「{f}」 ↔ {t['dictionary']} 「{t['canonical']}」({t.get('code') or '-'}) : {t['rule']}{note}"),
                                    ("decided_by", None), ("decided_at", None), ("status", "proposed"),
                                    ("source_refs", [{"kind": "ledger", "ref": x} for x in label_locs] + [{"kind": "erd", "ref": t["pointer"]}] + [{"kind": "ledger", "ref": x} for x in dedupe(occ_refs)] + [{"kind": "brief", "ref": "silver-build-brief.md 결정 묶음 1-2"}]),
                                    ("evidence", {"fragment": f, "fragment_count": c["count"], "target": t, "label_locators": label_locs, "fragment_occurrence_locators": dedupe(occ_refs)})]))
    keep = out
    return keep, not_proposed


def templates():
    out = []
    for slug, kind, what in TEMPLATES:
        t, nv = TEMPLATE_SHAPES[kind]
        out.append((slug, OrderedDict([("id", f"{BUNDLE}-TPL-{slug}"), ("template", True), ("kind", kind), ("target", t), ("new_value", nv), ("reason", ""),
                                       ("decided_by", None), ("decided_at", None), ("status", "proposed"),
                                       ("source_refs", [{"kind": "erd", "ref": f"ERD-FROZEN.md 「결정으로 넘긴 것」: {what}"}]), ("note", f"빈 템플릿 — 값은 사람이 채운다({what})")])))
    return out
