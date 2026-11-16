# -*- coding: utf-8 -*-
"""충돌 — ④ auto_resolved_by_trust · ⑥ value_conflict(open) · ⑦ duplicate_candidate · ⑧ unregistered_value · ⑨ unresolved_reference.
전부 stable_key = {kind, locators 정렬} 을 가진다(결정은 이것만 가리킨다)."""
import re
from collections import Counter, OrderedDict, defaultdict

from .core import dref
from .decompose import MARKET_SLOT
from .provenance import P, loc, leaves, records, rec_str
from .util import mkid, norm, dedupe

NAME_KEYS = {"name", "label", "cc", "cc_group", "category", "from", "to", "from_name", "to_name", "procedures", "products", "combo",
             "optimal_combo", "sequence", "pair", "categories", "recommended_base", "problem", "subcategory", "title", "patient_name",
             "target", "goal", "phase", "type", "tier", "tierLabel", "productTier", "unit", "level", "group", "ingredient", "material",
             "manufacturer", "primary_concerns", "upgrade", "avoid", "incompatible", "modality_ref", "procedure_ref", "name_ko", "name_en",
             "category_en", "concern", "concern_en", "subtitle", "plan_name", "age", "age_group", "rule", "icon", "id", "procedure_id"}
CODE_VAL_RE = re.compile(r"^[MP]\d+(?:-\d+)*$")
STEP1_MFDS = re.compile(r"식약처.*API")


def trust_of(S, file, path, r=None):
    """§5.1 신뢰 순위 — products.json mfds 만 2 · step1 허가 필드는 licenses[].source 가 `식약처.*API` 일 때 2."""
    if file == "products.json" and path.endswith(".mfds"):
        return 2
    if file == "step1-products.json" and r is not None and "4_license.licenses[]" in path:
        try:
            lic = S.ctx["L"]["step1-products.json"]["items"][r[0]]["4_license"]["licenses"][r[1]]
            if STEP1_MFDS.search(str(lic.get("source", ""))):
                return 2
        except (IndexError, KeyError, TypeError):
            pass
    return S.ctx["trust"][file]


def V(S, value, file, path, r):
    return {"value": value, "source_file": file, "source_path": path, "rec": rec_str(r) if isinstance(r, tuple) else r, "trust_tier": trust_of(S, file, path, r if isinstance(r, tuple) else None)}


class DictIndex:
    """사전 46 전체 — 정규화 완전 일치 색인(후보 근거용 · 추정 없음)."""

    def __init__(self, dic):
        self.idx = defaultdict(list)
        for di, d in enumerate(dic["dictionaries"]):
            for ei, e in enumerate(d["entries"]):
                self.idx[norm(e["canonical"])].append({"dictionary": d["name"], "canonical": e["canonical"], "code": e.get("code"), "basis": "정준값 완전 일치", "pointer": dref(d["name"], e, "canonical")[0]})
                for si, s in enumerate(e.get("synonyms", [])):
                    self.idx[norm(s["value"])].append({"dictionary": d["name"], "canonical": e["canonical"], "code": e.get("code"), "basis": f"동의어 「{s['value']}」 완전 일치", "pointer": dref(d["name"], e, f"synonym:{s['value']}")[0]})

    def hits(self, frag):
        return self.idx.get(norm(frag), [])


def frag_candidates(S, frag, hint):
    """조각 후보 ≤3 — ① §1.3 계열 밖 모호(둘 이상 계열에 닿음) ② 사전 46 정규화 완전 일치. 근거 명시 · 추정 금지."""
    out = []
    R = S.ctx["proc"]["PT"].R
    c = R.classify(frag, hint)
    if c and c["kind"] == "ambiguous":
        for kind in R.PRIMARY:
            for code, canon in sorted(R.lex.hits(kind, frag)):
                out.append({"dictionary": {"procedure": "catalog_item_name", "product": "product_name", "modality_subcategory": "modality_subcategory_label"}[kind], "canonical": canon, "code": code,
                            "basis": f"§1.3 계열 밖 모호 — 계열 {','.join(c['codes'])} 둘 이상에 닿음(힌트 {hint})"})
    for h in S.ctx["dindex"].hits(frag):
        if not any(o["dictionary"] == h["dictionary"] and o["canonical"] == h["canonical"] for o in out):
            out.append(h)
    return out[:3]


# ---------------------------------------------------------------------------
def reference_conflicts(S):
    """⑨ — 참조 자리 행(자리 · 라벨 · 힌트) 중 튜플·노드가 안 된 것. locators = 그 자리의 원장 위치 전부."""
    D = S.ctx["proc"]
    occ = S.ctx["occ"]
    rows = list(D["ref_rows"].items()) + [(MARKET_SLOT, D["mk_rows"])]
    for slot, rr in rows:
        by = defaultdict(list)
        for lab, hint, pv, _ in occ[slot]:
            by[(lab, hint)].append(pv)
        AM = S.ctx.get("AM_live")
        for r in rr:
            if r["result"] in ("tuple", "combo_ref", "multi_tuple", "node"):
                continue
            pvs = by[tuple(r["_in"])]
            frags = r.get("unregistered", [])
            cands = OrderedDict((f, frag_candidates(S, f, r.get("hint"))) for f in frags)
            if r["result"] == "unresolved" and r.get("unresolved_reason") != "unregistered":
                cands = OrderedDict(("(조각 둘 이상)", [{"basis": f"§1.4 {r.get('unresolved_reason')} — 닿은 조각(둘 이상)", "fragments": r.get("detail")}]) for _ in [0])
            c = S.unresolved_ref(D_REL(slot), slot, r["label"], r.get("hint"), pvs, r.get("unresolved_reason") or r.get("reason") or r["result"], frags,
                                 partial=[f"{k}:{v}" for g in r.get("groups", []) for m in g["members"] for k, v in m["spans"]], candidates=cands, ref_id=r.get("ref_id"))
            # V3-9 — 결정(tuple_assign/_multi)이 이 미해결 참조의 튜플을 세웠으면 ⑨ 는 그 결정으로 닫힌다(레코드는 남긴다)
            est = AM.established.get(r.get("ref_id")) if AM is not None else None
            if est and AM.resolve(r["ref_id"]):
                c["status"] = "resolved"
                c["decision_id"] = est


def close_duplicates_by_fold(S, AM):
    """V3-10 — fold_approve(approved)가 접는 anchor 쌍의 ⑦ duplicate_candidate 를 status=resolved · decision_id 로 닫는다.
    「쌍의 ⑦」= ⑦ 레코드의 원장 위치(locators)가 전부 그 결정의 anchors 의 원장 위치이고 서로 다른 anchor 둘 이상에 걸친 것(같은 것 판정 · close_verdict 없음).
    한쪽이라도 접는 anchor 밖의 위치(다른 자리의 표면형)를 가지면 그 ⑦ 은 이 결정이 판정한 쌍이 아니라 그대로 둔다."""
    out = []
    for f in S.ctx.get("folds", []):
        loc2a = {}
        for a in f["anchors"]:
            sp = AM.spec.get(a) or {}
            for o in sp.get("occ", []):
                loc2a.setdefault(o, set()).add(a)
        for c in S.conflicts:
            if c["kind"] != "duplicate_candidate" or c["status"] != "open":
                continue
            locs = c["stable_key"]["locators"]
            if not locs or any(l not in loc2a for l in locs):
                continue
            touched = set().union(*(loc2a[l] for l in locs))
            if len(touched) < 2:
                continue
            c["status"] = "resolved"
            c["decision_id"] = f["id"]
            c["resolution_rule"] = c["resolution_rule"] + f" · V3-10 fold_approve {f['id']} 가 접는 anchor 쌍 — 같은 것으로 판정(닫힘)"
            out.append({"conflict": c["id"], "decision": f["id"], "anchors": sorted(touched)})
    return out


def duplicate_fold_overlap(S, AM):
    """보고용 — fold 결정의 anchor 위치에 하나라도 닿는 open ⑦(쌍이 아닌 것 포함) 수."""
    n = 0
    occ = set()
    for f in S.ctx.get("folds", []):
        for a in f["anchors"]:
            occ |= set((AM.spec.get(a) or {}).get("occ", []))
    for c in S.conflicts:
        if c["kind"] == "duplicate_candidate" and c["status"] == "open" and any(l in occ for l in c["stable_key"]["locators"]):
            n += 1
    return n


def D_REL(slot):
    from .decompose import SLOT_RELATION
    return SLOT_RELATION.get(slot, "price_items")


# ---------------------------------------------------------------------------
def value_conflicts(S):
    L = S.ctx["L"]
    # 질문 2 — modality 본문 extracted.json vs taxonomy modality[].extracted (같은 순위 3 = ⑥)
    for mid, rec in S.E["modality"].items():
        for a in ("overview", "mechanism", "onset", "peak", "duration", "indications_primary", "indications_extended", "aftercare", "related_techniques"):
            cells = [c for c in rec["attrs"].get(a, []) if "prov" in c and c["prov"][0]["file"] in ("extracted.json", "taxonomy.json")]
            byf = OrderedDict()
            for c in cells:
                p = c["prov"][0]
                byf.setdefault(p["file"], []).append(c)
            if len(byf) < 2:
                continue
            listy = a.startswith("indications") or a in ("aftercare", "related_techniques")
            vals = []
            for f, cs in byf.items():
                p0 = cs[0]["prov"][0]
                if listy:
                    path = p0["path"][:-2] if p0["path"].endswith("[]") else p0["path"]
                    rec_ = "/".join(p0["rec"].split("/")[:-1]) or "-"
                    vals.append({"value": [c["value"] for c in cs], "source_file": f, "source_path": path, "rec": rec_, "trust_tier": trust_of(S, f, path)})
                else:
                    vals.append({"value": cs[0]["value"], "source_file": f, "source_path": p0["path"], "rec": p0["rec"], "trust_tier": trust_of(S, f, p0["path"])})
            keyv = [tuple(norm(x) for x in v["value"]) if listy else norm(v["value"]) for v in vals]
            if len(set(keyv)) > 1:
                resolve_by_trust(S, "modality", mid, a, vals, "질문 2 — extracted.json vs taxonomy modality[].extracted 본문")
    # 질문 3 — 제품 속성 products.json vs taxonomy(mfds 는 2 vs 3 → ④)
    for pid, rec in S.E["product"].items():
        for a in ("name_en", "manufacturer", "country", "mfds", "ingredient_material", "product_type", "note"):
            cells = [c for c in rec["attrs"].get(a, []) if "prov" in c and c["prov"][0]["file"] in ("products.json", "taxonomy.json")]
            byf = OrderedDict()
            for c in cells:
                byf.setdefault(c["prov"][0]["file"], c)
            if len(byf) < 2:
                continue
            vals = [V(S, c["value"], c["prov"][0]["file"], c["prov"][0]["path"], c["prov"][0]["rec"]) for c in byf.values()]
            for v in vals:
                v["trust_tier"] = trust_of(S, v["source_file"], v["source_path"])
            if len({norm(v["value"]) if v["value"] is not None else None for v in vals}) > 1:
                resolve_by_trust(S, "product", pid, a, vals, "질문 3 — products.json vs taxonomy modality[].products[]")
    # 질문 3 — 제품 목록 소속 차이(한쪽에만 있는 제품)
    for pid, m in S.ctx["product_member"].items():
        if bool(m.get("products.json")) != bool(m.get("taxonomy.json")):
            f = "products.json" if m.get("products.json") else "taxonomy.json"
            if f == "products.json":
                k, i = m[f][0]
                v = [V(S, L["products.json"][k]["products"][i]["name"], f, f"{k}.products[].name", (i,))]
            else:
                r = m[f][0]
                v = [V(S, L["taxonomy.json"]["modality"][r[0]]["products"][r[1]]["name"], f, "modality[].products[].name", r)]
            S.conflict("value_conflict", "⑥", "product", pid, "membership(products.json ↔ taxonomy products)", v,
                       f"질문 3 — {f} 에만 있는 제품(다른 쪽 목록에 없음) · ⑥ open", "open")
    # step1 6_companies.conflicts — 허가 값 vs 다른 출처(「덮어쓰지 않음」)
    for r, cf in records(L["step1-products.json"], "items[].6_companies.conflicts[]"):
        it = L["step1-products.json"]["items"][r[0]]
        lic_tier = 2 if any(STEP1_MFDS.search(str(l.get("source", ""))) for l in (it["4_license"].get("licenses") or [])) else 3
        vals = [{"value": cf.get("license"), "source_file": "step1-products.json", "source_path": "items[].6_companies.conflicts[].license", "rec": rec_str(r), "trust_tier": lic_tier},
                {"value": cf.get("other"), "source_file": "step1-products.json", "source_path": "items[].6_companies.conflicts[].other", "rec": rec_str(r), "trust_tier": 3}]
        c = resolve_by_trust(S, "product", S.ctx["step1_product"][r[0]], f"companies.{cf.get('field')}", vals, f"step1 6_companies.conflicts — {cf.get('note') or ''} (source: {cf.get('source')})")
        c["context"] = [{"key": k, "value": cf.get(k), "locator": f"step1-products.json:items[].6_companies.conflicts[].{k}@{rec_str(r)}"} for k in ("field", "source", "note") if k in cf]
    # pih procedure_ref 항목 이름 vs pih name
    items_by_id = S.ctx["item_by_id"]
    for r, p in records(L["pih-risk.json"], "procedures[]"):
        it = items_by_id.get(p["procedure_ref"])
        if not it:
            continue
        a, b = p["name"], it["item"]["name"]
        if norm(a) == norm(b):
            continue
        strip = lambda s: norm(re.sub(r"\([^()]*\)", "", s))  # noqa
        vals = [V(S, a, "pih-risk.json", "procedures[].name", r), V(S, b, "taxonomy.json", "modality[].subcategories[].items[].name", it["r"])]
        if strip(a) == strip(b):
            S.conflict("duplicate_candidate", "⑦", "catalog_item", it["cat"]["catalog_item_id"], "name(pih 괄호 보충)", vals, "§9.3 pih name 이 항목명과 괄호 보충만 다름 — source_label 로 보존 · ⑦ 후보", "open")
        else:
            S.conflict("value_conflict", "⑥", "catalog_item", it["cat"]["catalog_item_id"], "name(pih procedure_ref)", vals, "§9.3 같은 id 에 괄호를 벗겨도 다른 이름 · ⑥ open", "open")


def resolve_by_trust(S, ttype, tid, field, vals, why):
    tiers = {v["trust_tier"] for v in vals}
    if len(tiers) > 1:
        best = min(tiers)
        chosen = [v["value"] for v in vals if v["trust_tier"] == best]
        if len({norm(x) if x is not None and not isinstance(x, list) else str(x) for x in chosen}) == 1:
            return S.conflict("value_conflict", "④", ttype, tid, field, vals, f"④ 신뢰 순위 {best} 값 자동 채택 — {why}", "auto_resolved_by_trust", chosen_value=chosen[0])
    return S.conflict("value_conflict", "⑥", ttype, tid, field, vals, f"④ 로 안 풀림(같은 순위) — {why} · ⑥ open", "open")


# ---------------------------------------------------------------------------
def normalize_name(s):
    s = s.lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"[\s_\-/·,.]+", "", s)
    return s


def duplicate_candidates(S):
    L = S.ctx["L"]
    # 컬럼 리포트 §3.10 규칙 그대로(이름류 키 · 24자 이하 · 정규화 같고 표면형 2 이상) — 원장 21
    hits = defaultdict(list)
    for f in sorted(x["file"] for x in S.ctx["erd"]["source_files"] if x["kind"] == "ledger"):
        for p, r, v in leaves(L[f]):
            if not isinstance(v, str):
                continue
            s = v.strip()
            last = p.rsplit(".", 1)[-1].replace("[]", "")
            if 0 < len(s) <= 24 and "\n" not in s and last in NAME_KEYS:
                hits[s].append((f, p, r))
    groups = defaultdict(set)
    for nm in hits:
        n = normalize_name(nm)
        if len(n) >= 2:
            groups[n].add(nm)
    comp_path = "categories[].complications[].name"
    AT = S.ctx["adv"]["AT"]
    n_skip = 0
    for n, forms in sorted(groups.items()):
        if len(forms) < 2 or all(CODE_VAL_RE.match(f) or re.match(r"^[MP]\d+(-\d+)*-", f) for f in forms):
            continue
        occ = [(f, x) for f in sorted(forms) for x in hits[f]]
        # §9.3 비고 — complications 합병증 표기 변형은 v2 에서 사건 사전 동의어로 같은 단위에 접힌다(⑦ 아님)
        if all(x[0] == "complications.json" and x[1] == comp_path for _, x in occ):
            # v3.1 — 같은 단위(세 칸)로 접히면 ⑦ 아님
            units = {tuple(sorted((c["event"], str(c["site"]), str(c["qualifier"])) for c in AT.unit_candidates(AT.assemble(AT.split(f))[0]))) for f in forms}
            if len(units) == 1:
                n_skip += 1
                continue
        vals = [V(S, f, x[0], x[1], x[2]) for f, x in occ]
        S.conflict("duplicate_candidate", "⑦", "surface_variant", None, f"표면형 변형 「{n}」", vals, "컬럼 리포트 §3.10 규칙(괄호·공백·영/한·대소문자만 다름) — ⑦ 후보(같은 것 판정 아님)", "open")
    S.ctx["dup_skipped_complications"] = n_skip
    # taxonomy 항목 이름 중복(계열 간)
    byname = defaultdict(list)
    for (fam, name), it in S.ctx["items"].items():
        byname[norm(name)].append(it)
    for nm, its in byname.items():
        fams = {i["cat"]["family"] for i in its}
        if len(its) >= 2 and len(fams) >= 2:
            S.conflict("duplicate_candidate", "⑦", "catalog_item", None, "name(계열 간 중복)",
                       [V(S, i["item"]["name"], "taxonomy.json", "modality[].subcategories[].items[].name", i["r"]) for i in its],
                       "§2.4 중복 이름은 계열 코드로 구분 → ⑦ 후보(CAT- 는 각자)", "open")
    # 질문 21 — mechanism regenerative / regeneration
    regen = [P("procedure-profiles.json", p, r) for p, r, v in leaves(L["procedure-profiles.json"]) if p == "profiles[].mechanism[]" and v in ("regenerative", "regeneration")]
    if regen:
        S.conflict("duplicate_candidate", "⑦", "technique", None, "name(regenerative/regeneration)",
                   [V(S, L["procedure-profiles.json"]["profiles"][int(p["rec"].split('/')[0])]["mechanism"][int(p["rec"].split('/')[1])], p["file"], p["path"], tuple(int(x) for x in p["rec"].split('/'))) for p in regen],
                   "질문 21 — 사전에 둘 다 정준값 · ⑦ 후보", "open")


# ---------------------------------------------------------------------------
def unregistered_conflicts(S):
    """⑧ — 분해에서 어느 사전에도 닿지 않은 조각(축별 distinct 하나 = 레코드 하나) + 사전 밖 값."""
    D, A = S.ctx["proc"], S.ctx["adv"]
    occ = S.ctx["occ"]
    rows_proc = defaultdict(list)   # frag -> [(where, P)]
    for c in D["cat_recs"]:
        it = S.ctx["items"][(c["family"], c["name"])]
        for u in c.get("unregistered", []):
            rows_proc[u].append(("taxonomy.json:modality[].subcategories[].items[].name", P("taxonomy.json", "modality[].subcategories[].items[].name", it["r"])))
    for slot, rr in list(D["ref_rows"].items()) + [(MARKET_SLOT, D["mk_rows"])]:
        by = defaultdict(list)
        for lab, hint, pv, _ in occ[slot]:
            by[(lab, hint)].append(pv)
        for r in rr:
            for u in r.get("unregistered", []):
                for pv in by[tuple(r["_in"])][:1]:
                    rows_proc[u].append((slot, pv))
    rows_adv = defaultdict(list)
    for r in A["complications"]:
        for u in r["unregistered"]:
            rows_adv[u].append(("complications.json:categories[].complications[].name", P("complications.json", "categories[].complications[].name", r["rec"])))
    # v3.1 — 문구 사전 항목(unlinked)의 미등록 조각 · 자리마다(게이트 unlinked_phrases 와 같은 조각)
    AU = S.ctx.get("AU_live")
    for pid, e in (AU.phrases.items() if AU is not None else []):
        if e["status"] != "unlinked":
            continue
        for u in e["unregistered"]:
            for c in e["contexts"]:
                if c.get("rec") is not None:
                    rows_adv[u].append((f"{c['file']}:{c['path']}", P(c["file"], c["path"], c["rec"])))
    gate = []
    for axis, rows in (("procedure", rows_proc), ("adverse", rows_adv)):
        for frag in sorted(rows, key=lambda f: (-len(rows[f]), f)):
            occs = rows[frag]
            where = Counter(w for w, _ in occs)
            cands = S.ctx["dindex"].hits(frag)[:3]
            vals = [V(S, frag, p["file"], p["path"], p["rec"]) for _, p in occs]
            c = S.conflict("unregistered_value", "⑧", f"{axis}_fragment", None, f"미등록 조각 「{frag}」", vals,
                           f"§1.4/§1.5 분해에서 어느 사전에도 닿지 않은 조각({axis} 축) — 사전 추가는 결정 dictionary_add", "open",
                           extra={"fragment": frag, "axis": axis, "count": len(occs), "where": dict(where), "axis_candidates": cands})
            gate.append(c)
    S.ctx["unreg_gate"] = gate


def dict_value_conflicts(S):
    """⑧ — 사전 값 자리(사전 출처 kind=value)의 값이 사전 정준값·동의어에 없음. `-` 자리표시자는 null(질문 18)이지만 사전 밖 값으로 기록."""
    L = S.ctx["L"]
    for d in S.ctx["dic"]["dictionaries"]:
        if d.get("kind") != "value":
            continue
        vals = {norm(e["canonical"]) for e in d["entries"]} | {norm(s["value"]) for e in d["entries"] for s in e.get("synonyms", [])}
        # 그 잎 키의 행선지가 이 사전 자체(컬럼 표 표적 dict:<사전>)인 자리만 — 섞인 자리(부위·고민 하위분류 라벨 등)는 사전 밖 값이 아니다
        paths = {(f, p) for (f, p), t in S.ctx["cmap"].items() if t["target"] == f"dict:{d['name']}"}
        for f, path in sorted(paths):
            if f not in L or d["name"] in ("adverse_event_type", "course", "relative_site"):
                continue
            for p, r, v in leaves(L[f]):
                if p != path or v is None or isinstance(v, (bool, dict, list)):
                    continue
                if norm(v) not in vals:
                    S.conflict("unregistered_value", "⑧", "dictionary_value", None, f"사전 {d['name']} 밖 값 「{v}」", [V(S, v, f, p, r)],
                               f"§5 ⑧ 사전 밖 값 — 사전 {d['name']} 정준값·동의어에 없음" + (" · `-` 자리표시자 = null(질문 18)" if str(v).strip() == "-" else ""), "open",
                               extra={"fragment": v, "axis": f"dict:{d['name']}", "count": 1, "where": {f"{f}:{p}": 1}, "axis_candidates": []})


# ---------------------------------------------------------------------------
# v3.2(V3.2-0 · V3.2-5) ⑦ duplicate_candidate — 원장 사건 노드끼리(노드 ↔ 사전 사건 · 노드 ↔ 노드 · strong/weak) · 장비 제품 ↔ 기존 제품(접두)
# 표기 규칙만(유사도 점수 없음 · 참조 구현 duplicate_pairs) — 접기는 fold_approve(사전 값 쌍) · 아님은 conflict_close(not_same)
# ---------------------------------------------------------------------------
def _node_values(S, AU, locs, label):
    vals = []
    for lc in locs:
        p = AU.erd2p.get(lc)
        if p is not None:
            vals.append(V(S, label, p["file"], p["path"], p["rec"]))
    return vals


def ledger_duplicates(S):
    A, A0, AU = S.ctx["adv"], S.ctx["adv0"], S.ctx["AU_live"]
    nodes = {n["canonical"]: n for n in A["ledger_events"]}
    nodes0 = {n["canonical"]: n for n in A0["ledger_events"]}
    out = []

    def mk(d, node_tab, status, decision_id=None):
        a = node_tab.get(d["new"])
        vals = _node_values(S, AU, a["locators"] if a else [], d["new"])
        extra_locs = []
        if d["existing_kind"] == "ledger":
            b = node_tab.get(d["existing"])
            vals += _node_values(S, AU, b["locators"] if b else [], d["existing"])
        else:
            extra_locs.append(f"dict:adverse_event_type|{d['existing']}")
        c = S.conflict("duplicate_candidate", "⑦", "adverse_event_type", d["new_id"], f"원장 사건 노드 「{d['new']}」 ↔ 「{d['existing']}」({'사전 사건' if d['existing_kind'] == 'dictionary' else '원장 노드'})", vals,
                       f"V3.2-0 노드끼리 ⑦ — 표기 규칙 {', '.join(d['rules'])} · 등급 {d['grade']}" + (" (기본 게이트)" if d["grade"] == "strong" else " (표시만 · 기본 게이트 아님)") + " — 같은 것 판정 아님(접기는 fold_approve · 아님은 conflict_close)",
                       status, extra={"extra_locators": extra_locs, "pair": OrderedDict([("node", d["new"]), ("node_id", d["new_id"]), ("other", d["existing"]), ("other_kind", d["existing_kind"]), ("rules", d["rules"]), ("grade", d["grade"]), ("erd_key", d["stable_key"])]),
                                      "grade": d["grade"]})
        if decision_id:
            c["decision_id"] = decision_id
        out.append(c)
        return c

    for d in A["duplicate_pairs"]:
        mk(d, nodes, "open")
    # fold_approve(사전 값 쌍)이 접은 쌍 — 결정 전 분해의 ⑦ 을 resolved 로 남긴다(V3-10 과 같은 생애)
    for f in S.ctx.get("node_folds_applied", []):
        for d in A0["duplicate_pairs"]:
            pair = {norm(d["new"]), norm(d["existing"])}
            if pair == {norm(f["node"]), norm(f["into"])}:
                c = mk(d, nodes0, "resolved", f["id"])
                c["resolution_rule"] += f" · fold_approve {f['id']} 가 접었다(같은 것으로 판정 · 닫힘)"
    S.ctx["ledger_dup_conflicts"] = out
    # 장비 제품(origin=taxonomy) ↔ 기존 제품 — 정규화 이름이 서로를 접두로(V3.2-5 · 줄임말 길이 하한)
    eq = S.ctx["erd"]["tuple_rules"]["equipment"]
    mn = eq.get("abbrev_min_len", 2)
    pn = S.ctx["dicts"]["product_name"]["entries"]
    base = {}
    for e in pn:
        if e.get("origin") == "taxonomy":
            continue
        for v in [e["canonical"]] + [s_["value"] for s_ in e.get("synonyms", [])]:
            base.setdefault(norm(v), e["canonical"])
    tx_pos = {}
    for mi, m in enumerate(S.ctx["L"]["taxonomy.json"]["modality"]):
        for si, sc in enumerate(m["subcategories"]):
            for ii, it in enumerate(sc["items"]):
                tx_pos[f"{m['id']}/{si}/{ii}"] = (mi, si, ii)
    eq_out = []
    for e in pn:
        if e.get("origin") != "taxonomy":
            continue
        pk = norm(e["canonical"])
        for qk, canon in sorted(base.items()):
            if qk != pk and min(len(pk), len(qk)) >= mn and (pk.startswith(qk) or qk.startswith(pk)):
                vals = [V(S, e["canonical"], "taxonomy.json", "modality[].subcategories[].items[].name", tx_pos[s_["locator"].split("@", 1)[1]]) for s_ in e.get("sources", []) if s_.get("locator") and s_["locator"].split("@", 1)[1] in tx_pos]
                c = S.conflict("duplicate_candidate", "⑦", "product", None, f"장비 제품 「{e['canonical']}」 ↔ 제품 「{canon}」(접두)", vals,
                               "V3.2-5 자동 장비 제품 ↔ 기존 제품(정규화 이름 접두) — ⑦ 후보(같은 것 판정 아님 · 접기는 dictionary_add 동의어 · 아님은 conflict_close)", "open",
                               extra={"extra_locators": [f"dict:product_name|{canon}"], "pair": OrderedDict([("equipment", e["canonical"]), ("product", canon), ("rule", "prefix")])})
                eq_out.append(c)
    S.ctx["equipment_dup_conflicts"] = eq_out
