# -*- coding: utf-8 -*-
"""개체 20종(ERD v3.1) — 원장 잎 → 레코드(값마다 provenance). 속성↔출처 키는 erd-v3.1.json entities[].attrs[].sources 가 정본.
v3: site.kind(V3-5) · product/technique description·media_refs(V3-7 — 값은 새 브론즈 원천이 등록될 때만 · 지금 원천 0 이라 만들지 않는다).
v3.1: adverse_effect 세 칸(V3.1-9 · 경과 없음 · relative_site_text · created_by_phrase · explanations 부록) · adverse_expression 없음(문구 사전 · V3.1-10) ·
person_condition = 조건 단위(사전 · raw_name · phrases 부록 · V3.1-4) · clinical_rule kind disclosure(V3.1-7) · product 의 reclassified_from alias(V3.1-1) · clinical_rule 식별자 = kind + 정규화 문장."""
import re
from collections import OrderedDict, defaultdict

from .core import dref, eref, clean
from .provenance import P, loc, records, sub_leaves, leaves, rec_str
from .util import mkid, norm, dedupe
from .decompose import site_kind_of

MCODE = re.compile(r"^M\d+$")


# ---------------------------------------------------------------------------
def collect(S, etype, rec, file, root, rkey, obj, skip=()):
    """레코드 obj(루트 root · rkey) 아래 잎 중 그 개체 속성의 출처 키에 맞는 것을 칸으로. aliases 는 컬럼 표 표적 `<개체>.aliases`."""
    pats = [x for x in S.ctx["src"][etype] if x[0] in (file, "*")]
    cmap = S.ctx["cmap"]
    for path, r, v in sub_leaves(obj, root, rkey):
        hit = False
        for f, rx, a in pats:
            if rx.match(path):
                if a not in skip:
                    S.leaf_cell(rec, a, file, path, r, v)
                hit = True
                break
        t = cmap.get((file, path))
        if not hit and t and t["dest"] == "개체" and t["target"].startswith(etype + ".") and "(" not in t["target"]:
            # ERD 속성 출처 목록에 없지만 잎 키 행선지 표가 이 개체 속성(`product.licenses.*` 등)으로 보낸 잎 — 키 이름 보존
            a = t["target"].split(".")[1]
            if a != "aliases" and a not in skip:
                S.leaf_cell(rec, a, file, path, r, v)
        if t and t["dest"] == "개체" and t["target"] == f"{etype}.aliases":
            S.alias(rec, v, P(file, path, r))


def leaf_locs(L, file, path, pred):
    """잎 경로 path 의 값이 pred 를 만족하는 locator 전부."""
    out = []
    for p, r, v in leaves(L[file]):
        if p == path and pred(v):
            out.append(P(file, p, r))
    return out


# ---------------------------------------------------------------------------
# source_file
# ---------------------------------------------------------------------------
def build_source_files(S):
    L, erd = S.ctx["L"], S.ctx["erd"]
    for i, s in enumerate(erd["source_files"]):
        rec = S.ent("source_file", mkid("SRC", s["sha256"]), [eref("source_files", s["file"], "sha256")])
        for a in ("file", "sha256", "bytes", "snapshot_date", "trust_tier", "kind", "trust_basis", "trust_flag"):
            S.dattr(rec, "file_name" if a == "file" else a, s.get(a), [eref("source_files", s["file"], a)])
        collect(S, "source_file", rec, s["file"], "", (), L[s["file"]])
        # step1 메타(컬럼 표: generated_at → updated · scope → description)
        if s["file"] == "step1-products.json":
            d = L[s["file"]]
            S.leaf_cell(rec, "updated", s["file"], "generated_at", (), d.get("generated_at"))
            S.leaf_cell(rec, "description", s["file"], "scope", (), d.get("scope"))


# ---------------------------------------------------------------------------
# modality · modality_subcategory · catalog_item
# ---------------------------------------------------------------------------
def build_modality(S):
    L, ids = S.ctx["L"], S.ctx["ids"]
    tx = L["taxonomy.json"]
    mods = {}
    for r, m in records(tx, "modality[]"):
        rec = S.ent("modality", ids.mod[m["id"]]["id"], [loc(P("taxonomy.json", "modality[].id", r))])
        mods[m["id"]] = rec
        collect(S, "modality", rec, "taxonomy.json", "modality[]", r, m)
        if m.get("products"):
            S.dattr(rec, "products_present", True, [loc(P("taxonomy.json", "modality[].products[].id", r + (0,)))])
    for file, root in [("extracted.json", "{code}"), ("patient-education.json", "categories[]"), ("procedure-profiles.json", "profiles[]"),
                       ("consent-checklist.json", "categories[]"), ("market-pricing.json", "categories[]")]:
        for r, obj in records(L[file], root):
            code = r[-1] if root == "{code}" else obj.get("id")
            rec = mods.get(code)
            if rec is None:
                S.unresolved_code(file, root, r, code)
                continue
            collect(S, "modality", rec, file, root, r, obj)
            if root != "{code}" and "id" in obj:
                rec["derived_from"].append(loc(P(file, f"{root}.id", r)))
            if file == "extracted.json":
                S.alias(rec, obj.get("procedure_id"), P(file, "{code}.procedure_id", r))
    # pih-risk notes.{code} — M1_to_M7 는 M1..M7 전개(③ · DEC-…-14)
    for k, v in L["pih-risk.json"]["notes"].items():
        p = P("pih-risk.json", "notes.{code}", (k,))
        m = re.match(r"^M(\d+)_to_M(\d+)$", k)
        codes = [f"M{i}" for i in range(int(m.group(1)), int(m.group(2)) + 1)] if m else [k]
        for c in codes:
            if c in mods:
                S.attr(mods[c], "pih_note", clean("pih-risk.json", "notes.{code}", v), p)
    # literature-evidence 빈 섹션 = null(질문 13) · 값 있는 섹션 = 문장 수
    for r, obj in records(L["literature-evidence.json"], "categories.{code}"):
        rec = mods.get(r[-1])
        if rec is None:
            continue
        cnt = OrderedDict()
        df = []
        for sec in ("moa", "adverse_effects", "effects"):
            xs = obj.get(sec)
            if xs:
                cnt[sec] = len(xs)
                df.append(loc(P("literature-evidence.json", f"categories.{{code}}.{sec}[].statement", r + (0,))))
            else:
                cnt[sec] = None
                df.append(loc(P("literature-evidence.json", f"categories.{{code}}.{sec}", r)))
        S.dattr(rec, "evidence_statement_count", cnt, df)
    # timeline id — timeline name 이 계열명과 정규화 일치할 때만 alias
    for r, t in records(L["post-procedure-timeline.json"], "timelines[]"):
        code = t["category"].split("-")[0]
        if code in mods and norm(t["name"]) == norm(L["taxonomy.json"]["modality"][[m["id"] for m in tx["modality"]].index(code)]["category"]):
            S.alias(mods[code], t["id"], P("post-procedure-timeline.json", "timelines[].id", r))
    # products.json 섹션 키(category_id 단일 코드일 때)
    for k, v in L["products.json"].items():
        if isinstance(v, dict) and isinstance(v.get("category_id"), str) and v["category_id"] in mods:
            S.dalias(mods[v["category_id"]], k, [loc(P("products.json", f"{k}.category_id", ()))])
    return mods


def build_subcategories(S):
    L, ids = S.ctx["L"], S.ctx["ids"]
    subs = {}
    for r, sc in records(L["taxonomy.json"], "modality[].subcategories[]"):
        e = ids.sub[sc["id"]]
        rec = S.ent("modality_subcategory", e["id"], [loc(P("taxonomy.json", "modality[].subcategories[].id", r)), loc(P("taxonomy.json", "modality[].subcategories[].label", r))])
        collect(S, "modality_subcategory", rec, "taxonomy.json", "modality[].subcategories[]", r, sc)
        S.alias(rec, sc["id"], P("taxonomy.json", "modality[].subcategories[].id", r))
        if sc.get("items"):
            S.dattr(rec, "items_present", True, [loc(P("taxonomy.json", "modality[].subcategories[].items[].id", r + (0,)))])
        subs[sc["id"]] = (rec, r, e["family"])
    return subs


def build_catalog(S):
    L = S.ctx["L"]
    D = S.ctx["proc"]
    cat_by_key = {(c["family"], c["name"]): c for c in D["cat_recs"]}
    items = {}
    for r, m in records(L["taxonomy.json"], "modality[]"):
        for si, sc in enumerate(m["subcategories"]):
            for ii, it in enumerate(sc["items"]):
                rr = r + (si, ii)
                c = cat_by_key[(m["id"], it["name"])]
                nloc = loc(P("taxonomy.json", "modality[].subcategories[].items[].name", rr))
                rec = S.ent("catalog_item", c["catalog_item_id"], [loc(P("taxonomy.json", "modality[].id", r)), nloc])
                collect(S, "catalog_item", rec, "taxonomy.json", "modality[].subcategories[].items[]", rr, it)
                S.dattr(rec, "tuple_status", c["status"], [nloc])
                S.dattr(rec, "unregistered_fragments", list(c.get("unregistered", [])), [nloc])
                S.dattr(rec, "family_code", m["id"], [loc(P("taxonomy.json", "modality[].id", r))])
                items[(m["id"], it["name"])] = {"rec": rec, "r": rr, "sub": sc["id"], "item": it, "cat": c, "name_loc": nloc}
    S.ctx["items"] = items
    return items


# ---------------------------------------------------------------------------
# product (원장 59 + step1 395)
# ---------------------------------------------------------------------------
def build_products(S, resolver):
    L, ids = S.ctx["L"], S.ctx["ids"]
    prods = {}
    by_norm = {}
    D = {d["name"]: d for d in S.ctx["dic"]["dictionaries"]}
    for di, e in enumerate(D["product_name"]["entries"]):
        pid = mkid("PRD", f"{e['code']}|{e['canonical']}")
        rec = S.ent("product", pid, dref("product_name", e))
        S.dattr(rec, "origin", "ledger" if not any(x.get("kind") == "decision" and not any(r.get("decision_id") == x.get("decision_id") for r in e.get("reclassified_from", [])) for x in e.get("sources", [])) else "survey", dref("product_name", e))
        for r in e.get("reclassified_from", []):
            # V3.1-1 product_reclassify — 옛 PRD- 는 alias(결정·엣지가 옛 id 로 가리킨 것은 이것으로 닿는다)
            S.dalias(rec, r["id"], [r["decision_id"]])
            S.dattr(rec, "reclassified_from", [{"id": x["id"], "code": x["code"], "decision_id": x["decision_id"]} for x in e["reclassified_from"]], [x["decision_id"] for x in e["reclassified_from"]])
            S.ctx.setdefault("prd_reclass", {})[pid] = {"old_id": r["id"], "from_code": r["code"], "to_code": e["code"], "decision_id": r["decision_id"]}
        prods[pid] = rec
        by_norm[norm(e["canonical"])] = pid
        for s in e.get("synonyms", []):
            by_norm.setdefault(norm(s["value"]), pid)
    S.ctx["prod_by_norm"] = by_norm
    member = defaultdict(lambda: defaultdict(list))  # pid -> file -> [rec]
    # products.json 섹션
    for k, v in L["products.json"].items():
        if not isinstance(v, dict):
            continue
        for i, pr in enumerate(v.get("products", [])):
            r = (i,)
            root = f"{k}.products[]"
            pid = by_norm.get(norm(pr["name"]))
            if pid is None:
                S.note(f"products.json:{root}.name@{i}", f"제품명 「{pr['name']}」 이 product_name 사전에 없다 — 레코드 없이 ⑨")
                continue
            rec = prods[pid]
            collect(S, "product", rec, "products.json", root, r, pr)
            S.dalias(rec, k, [loc(P("products.json", f"{k}.products[].name", r))])
            member[pid]["products.json"].append((k, i))
            if pr.get("note") and "별도 제품 아님" in pr["note"]:
                S.dattr(rec, "not_separate_product", True, [loc(P("products.json", f"{k}.products[].note", r))])
    # taxonomy modality[].products[]
    for r, pr in records(L["taxonomy.json"], "modality[].products[]"):
        pid = by_norm.get(norm(pr["name"]))
        if pid is None:
            S.note(f"taxonomy.json:modality[].products[].name@{rec_str(r)}", f"제품명 「{pr['name']}」 이 product_name 사전에 없다")
            continue
        rec = prods[pid]
        collect(S, "product", rec, "taxonomy.json", "modality[].products[]", r, pr)
        member[pid]["taxonomy.json"].append(r)
        if pr.get("note") and "별도 제품 아님" in str(pr["note"]):
            S.dattr(rec, "not_separate_product", True, [loc(P("taxonomy.json", "modality[].products[].note", r))])
    # step1 — B 규칙(이름 분해·동의어)으로만 원장 대응 · 아니면 origin=survey
    step1_map = {}
    for r, it in records(L["step1-products.json"], "items[]"):
        fam = it["family"]["code"] if MCODE.match(str(it["family"]["code"])) else None
        names = [("display_name", it["2_names"]["display_name"], P("step1-products.json", "items[].2_names.display_name", r))]
        if it["2_names"].get("ledger_name"):
            names.append(("ledger_name", it["2_names"]["ledger_name"], P("step1-products.json", "items[].2_names.ledger_name", r)))
        for j, s in enumerate(it["2_names"].get("search_names") or []):
            names.append(("search_name", s["name"], P("step1-products.json", "items[].2_names.search_names[].name", r + (j,))))
        matched = None
        for role, nm, pv in names:
            res = resolver.resolve(nm, fam, ("product", "procedure"))
            if res["status"] == "resolved" and res["depth"] == "product":
                matched = (role, nm, pv, res)
                break
            if res["status"] == "resolved" and res["depth"] == "procedure" and res.get("overlap") and "product" in res["overlap"]:
                matched = (role, nm, pv, res)
                break
        if matched:
            res = matched[3]
            pid = by_norm.get(norm(res["canonical"]))
            if pid is None:
                # procedure 와 겹친 제품 — 제품 사전에서 같은 이름
                ph = resolver.lex.hits("product", matched[1])
                pid = by_norm.get(norm(sorted(ph)[0][1])) if ph else None
        else:
            pid = None
        if pid is None:
            key = f"{fam or 'survey'}|{it['2_names']['display_name']}"
            pid = mkid("PRD", key)
            rec = S.ent("product", pid, [loc(names[0][2])] + ([loc(P("step1-products.json", "items[].family.code", r))] if fam else []))
            S.dattr(rec, "origin", "survey", [loc(names[0][2])])
            S.dattr(rec, "name", it["2_names"]["display_name"], [loc(names[0][2])])
            prods[pid] = rec
        else:
            rec = prods[pid]
            S.dattr(rec, "step1_match", {"role": matched[0], "name": matched[1]}, [loc(matched[2])], replace=False)
        collect(S, "product", rec, "step1-products.json", "items[]", r, it)
        S.alias(rec, it["ledger_id"], P("step1-products.json", "items[].ledger_id", r))
        step1_map[r[0]] = pid
    S.ctx["step1_product"] = step1_map
    S.ctx["product_member"] = member
    return prods


# ---------------------------------------------------------------------------
# technique · site · anatomical_structure
# ---------------------------------------------------------------------------
def build_techniques(S):
    L = S.ctx["L"]
    di = S.ctx["dic_index"]["technique"]
    techs = {}
    for i, e in enumerate(S.ctx["dicts"]["technique"]["entries"]):
        provs = leaf_locs(L, "procedure-profiles.json", "profiles[].mechanism[]", lambda v, c=e["canonical"]: norm(v) == norm(c))
        rec = S.ent("technique", mkid("TEC", e["canonical"]), dref("technique", e) + [loc(p) for p in provs])
        for p in provs:
            S.attr(rec, "name", e["canonical"], p)
        if not provs:
            S.dattr(rec, "name", e["canonical"], dref("technique", e, "canonical"))
        S.dattr(rec, "dictionary_id", e["id"], dref("technique", e, "id"))
        techs[e["canonical"]] = rec
    return techs


def build_sites(S):
    L, ids = S.ctx["L"], S.ctx["ids"]
    di = S.ctx["dic_index"]["site"]
    zones = {z["id"]: (r, z) for r, z in records(L["anatomy-danger-zones.json"], "zones[]")}
    sites = {}
    for i, e in enumerate(S.ctx["dicts"]["site"]["entries"]):
        sid = ids.site[norm(e["canonical"])]["id"]
        rec = S.ent("site", sid, dref("site", e))
        S.dattr(rec, "site_kind", e.get("site_kind"), dref("site", e, "site_kind"))
        S.dattr(rec, "kind", site_kind_of(e), dref("site", e, "kind"))  # V3-5 anatomical|layer|region(relative 는 사전 relative_site)
        if e.get("site_kind") == "backbone" and e.get("zone_id") in zones:
            r, z = zones[e["zone_id"]]
            collect(S, "site", rec, "anatomy-danger-zones.json", "zones[]", r, z)
            S.alias(rec, z["id"], P("anatomy-danger-zones.json", "zones[].id", r))
        else:
            provs = leaf_locs(L, "taxonomy.json", "problem[].subcategories[].label", lambda v, c=e["canonical"]: norm(v) == norm(c))
            for p in provs:
                S.attr(rec, "name_ko", e["canonical"], p)
            if not provs:
                S.dattr(rec, "name_ko", e["canonical"], dref("site", e, "canonical"))
        if e.get("members"):
            S.dattr(rec, "members", [ids.site[norm(m)]["id"] for m in e["members"] if norm(m) in ids.site], dref("site", e, "members"))
        if "parent" in e:   # v3.2(V3.2-4) 부위 계층 — 사전 항목 parent(v3.1 값은 null · 값은 씨앗 승인으로만)
            S.dattr(rec, "parent", ids.site[norm(e["parent"])]["id"] if e.get("parent") and norm(e["parent"]) in ids.site else None, dref("site", e, "parent"))
        sites[e["canonical"]] = rec
    return sites


def build_structures(S):
    L = S.ctx["L"]
    out = {}
    for kind, path in (("vessel", "zones[].vessels[]"), ("nerve", "zones[].nerves[]")):
        for r, x in records(L["anatomy-danger-zones.json"], path):
            aid = mkid("ANA", x["name"])
            nloc = P("anatomy-danger-zones.json", f"{path}.name", r)
            rec = S.ent("anatomical_structure", aid, [loc(nloc)])
            S.attr(rec, "name_raw", x["name"], nloc)
            S.dattr(rec, "kind", kind, [loc(nloc)])
            if kind == "nerve" and "type" in x:
                S.leaf_cell(rec, "nerve_type", "anatomy-danger-zones.json", f"{path}.type", r, x["type"])
            S.alias(rec, x["name"], nloc)
            out.setdefault(aid, rec)
    return out


# ---------------------------------------------------------------------------
# problem · problem_subcategory · complaint
# ---------------------------------------------------------------------------
def build_problems(S):
    L = S.ctx["L"]
    probs, psubs, comps = {}, {}, {}
    for r, p in records(L["taxonomy.json"], "problem[]"):
        rec = S.ent("problem", mkid("PRB", p["id"]), [loc(P("taxonomy.json", "problem[].id", r))])
        collect(S, "problem", rec, "taxonomy.json", "problem[]", r, p)
        probs[p["id"]] = rec
        for si, sc in enumerate(p["subcategories"]):
            sr = r + (si,)
            srec = S.ent("problem_subcategory", mkid("PSB", f"{p['id']}|{sc['label']}"), [loc(P("taxonomy.json", "problem[].subcategories[].id", sr))])
            collect(S, "problem_subcategory", srec, "taxonomy.json", "problem[].subcategories[]", sr, sc)
            S.alias(srec, sc["id"], P("taxonomy.json", "problem[].subcategories[].id", sr))
            psubs[(p["id"], norm(sc["label"]))] = (srec, sr, sc, p["id"])
            for ii, it in enumerate(sc.get("items") or []):
                ir = sr + (ii,)
                crec = S.ent("complaint", mkid("CMP", f"{p['id']}|{sc['label']}|{it['name']}"), [loc(P("taxonomy.json", "problem[].subcategories[].items[].name", ir))])
                collect(S, "complaint", crec, "taxonomy.json", "problem[].subcategories[].items[]", ir, it)
                if it.get("modality_ref"):
                    S.dattr(crec, "modality_ref_present", True, [loc(P("taxonomy.json", "problem[].subcategories[].items[].modality_ref[]", ir + (0,)))])
                comps.setdefault((p["id"], norm(it["name"])), []).append((crec, ir, it, srec))
    S.ctx["problems"], S.ctx["psubs"], S.ctx["tx_complaints"] = probs, psubs, comps
    return probs, psubs, comps


def build_pp_complaints(S):
    """problem-packages complaints → (problem_id, 이름) 유일 일치 결합(질문 9). 둘 이상이면 ⑥ 충돌 + 자기 레코드, 없으면 자기 레코드."""
    L = S.ctx["L"]
    comps = S.ctx["tx_complaints"]
    pp_map = {}
    for r, p in records(L["problem-packages.json"], "problems[]"):
        for ci, c in enumerate(p["complaints"]):
            cr = r + (ci,)
            key = (p["problem_id"], norm(c["cc"]))
            hits = comps.get(key, [])
            ccloc = P("problem-packages.json", "problems[].complaints[].cc", cr)
            if len(hits) == 1:
                crec = hits[0][0]
            else:
                crec = S.ent("complaint", mkid("CMP", f"{p['problem_id']}|{c.get('cc_group')}|{c['cc']}|problem-packages"), [loc(ccloc)])
                if len(hits) >= 2:
                    S.conflict("value_conflict", "⑥", "complaint", None, "name(problem_id, 이름) 결합",
                               [{"value": h[2]["name"], "source_file": "taxonomy.json", "source_path": "problem[].subcategories[].items[].name", "rec": rec_str(h[1]), "trust_tier": 3} for h in hits]
                               + [{"value": c["cc"], "source_file": "problem-packages.json", "source_path": "problems[].complaints[].cc", "rec": rec_str(cr), "trust_tier": 3}],
                               "질문 9: (problem_id, 이름) 일치가 유일하지 않다 → 결합하지 않음(⑥ open)", "open")
            collect(S, "complaint", crec, "problem-packages.json", "problems[].complaints[]", cr, c)
            if c.get("combos"):
                S.dattr(crec, "combos_present", True, [loc(P("problem-packages.json", "problems[].complaints[].combos[].name", cr + (0,)))])
            pp_map[cr] = crec
    S.ctx["pp_complaints"] = pp_map
    # 이름만으로 중복(같은 이름이 여러 고민·하위분류) — 발주서 기본값 9 / ERD 6
    byname = defaultdict(list)
    for (pid, nm), hs in comps.items():
        for h in hs:
            byname[nm].append(h)
    for nm, hs in byname.items():
        if len(hs) >= 2:
            S.conflict("value_conflict", "⑥", "complaint", None, "name(이름만)",
                       [{"value": h[2]["name"], "source_file": "taxonomy.json", "source_path": "problem[].subcategories[].items[].name", "rec": rec_str(h[1]), "trust_tier": 3} for h in hs],
                       "§9.3 주호소 이름 중복 — 이름이 같은 주호소가 여러 자리(⑥ open · 결합 키는 (problem_id, 하위분류, 이름))", "open")
    return pp_map


# ---------------------------------------------------------------------------
# person_condition · citation · evidence_statement · clinical_rule
# ---------------------------------------------------------------------------
def build_conditions(S):
    """v3.1(V3.1-4) 조건 단위 — 사전 단위(CND-sha(kind|정준값)) · raw_name 단위(CND-sha(RAW:kind|정규화 원문)). 원장 문장 자리는 phrases[] 부록(개체 아님)."""
    L = S.ctx["L"]
    CU = S.ctx["CU"]
    D = {d["name"]: d for d in S.ctx["dic"]["dictionaries"]}
    pc = {norm(e["canonical"]): e for e in D["person_condition"]["entries"]}
    conds = {}
    for uid, u in CU.units.items():
        locs = [loc(P(*ph["ledger"])) for ph in u["phrases"]]
        rec = S.ent("person_condition", uid, locs)
        if u["name_kind"] == "dict":
            e = pc[norm(u["name"])]
            S.dattr(rec, "name", u["name"], dref("person_condition", e, "canonical"))
            S.dattr(rec, "dictionary_id", e["id"], dref("person_condition", e, "id"))
        else:
            for ph in u["phrases"]:
                S.attr(rec, "name", ph["text"], P(*ph["ledger"]))
            S.dattr(rec, "dictionary_id", None, locs)
        S.dattr(rec, "name_kind", u["name_kind"], locs)
        S.dattr(rec, "kind", u["kind"], locs)
        S.dattr(rec, "candidate_name", list(u["candidate_name"]), locs)
        S.dattr(rec, "condition_fragments", list(u["condition_fragments"]), locs)
        S.dattr(rec, "qualifier_text", list(u["qualifier_text"]), locs)
        S.dattr(rec, "anchor", loc(P(*u["phrases"][0]["ledger"])) if u["name_kind"] == "raw_name" else None, locs)
        S.dattr(rec, "status", u["status"], locs)
        S.dattr(rec, "phrases", [OrderedDict([("text", ph["text"]), ("kind", ph["kind"]), ("locator", loc(P(*ph["ledger"]))), ("erd_locator", ph["locator"]), ("modality_code", ph["modality_code"]), ("level_hint", ph["level_hint"]),
                                              ("match", ph["match"]), ("condition_fragments", ph["condition_fragments"]), ("unregistered_fragments", ph["unregistered_fragments"]), ("qualifier_text", ph["qualifier_text"]),
                                              ("explanation_text", ph["explanation_text"])]) for ph in u["phrases"]], locs)
        conds[uid] = rec
    for r, u in records(L["pre-procedure-checklist.json"], "universal_checks[]"):
        for uid in CU.of(P("pre-procedure-checklist.json", "universal_checks[].label", r)):
            rec = conds[uid]
            collect(S, "person_condition", rec, "pre-procedure-checklist.json", "universal_checks[]", r, u, skip=("name",))
            S.dattr(rec, "universal", True, [loc(P("pre-procedure-checklist.json", "universal_checks[].label", r))])
            S.alias(rec, u["id"], P("pre-procedure-checklist.json", "universal_checks[].id", r))
    for r, g in records(L["treatment-optimization.json"], "by_age_group[]"):
        for uid in CU.of(P("treatment-optimization.json", "by_age_group[].age", r)):
            collect(S, "person_condition", conds[uid], "treatment-optimization.json", "by_age_group[]", r, g, skip=("name",))
    S.ctx["conds"] = conds
    return conds


def build_citations(S):
    L = S.ctx["L"]
    cits = {}

    def get(kind, key, df):
        cid = mkid("CIT", key)
        rec = S.ent("citation", cid, df)
        if "kind" not in rec["attrs"]:
            S.dattr(rec, "kind", kind, df)
        cits[cid] = rec
        return rec

    lit = L["literature-evidence.json"]
    for sec in ("moa", "adverse_effects", "effects"):
        root = f"categories.{{code}}.{sec}[].citations[]"
        for r, c in records(lit, root):
            key = f"pmid:{c['pmid']}" if c.get("pmid") else f"doi:{c['doi']}" if c.get("doi") else f"url:{c.get('oa_url')}" if c.get("oa_url") else f"text:{c.get('title')}"
            rec = get("pubmed", key, [loc(P("literature-evidence.json", f"{root}.pmid", r))])
            collect(S, "citation", rec, "literature-evidence.json", root, r, c)
    for r, cm in records(L["complications.json"], "categories[].complications[]"):
        if cm.get("evidence"):
            pv = P("complications.json", "categories[].complications[].evidence", r)
            for u in [x.strip() for x in cm["evidence"].split(";") if x.strip()]:
                rec = get("url", f"url:{u}", [loc(pv)])
                S.attr(rec, "url", u, pv, raw_value=cm["evidence"])
    for p, r, v in leaves(L["step1-products.json"]):
        if p in ("items[].evidence[].urls[]", "items[].4_license.distribution_sources[].url") and isinstance(v, str) and v:
            pv = P("step1-products.json", p, r)
            rec = get("url", f"url:{v}", [loc(pv)])
            S.attr(rec, "url", v, pv)
        if p == "items[].4_license.distribution_sources[].text" and isinstance(v, str) and v:
            pv = P("step1-products.json", p, r)
            rec = get("guideline_text", f"text:{norm(v)}", [loc(pv)])
            S.attr(rec, "text", v, pv)
    for file, path, kind in [("extracted.json", "{code}.source", "textbook"), ("treatment-optimization.json", "combination_rules[].evidence", "guideline_text"),
                             ("treatment-sequence.json", "minimum_intervals[].source", "guideline_text"), ("anatomy-danger-zones.json", "zones[].tissue_data.rhinion_data_source", "guideline_text")]:
        for p, r, v in leaves(L[file]):
            if p == path and isinstance(v, str) and v.strip():
                pv = P(file, p, r)
                rec = get(kind, f"text:{norm(v)}", [loc(pv)])
                S.attr(rec, "text", v, pv)
    S.ctx["cits"] = cits
    return cits


def cit_key(c):
    return mkid("CIT", f"pmid:{c['pmid']}" if c.get("pmid") else f"doi:{c['doi']}" if c.get("doi") else f"url:{c.get('oa_url')}" if c.get("oa_url") else f"text:{c.get('title')}")


def build_evidence(S):
    L = S.ctx["L"]
    out = {}
    for sec, kind in (("moa", "moa"), ("effects", "effect")):
        root = f"categories.{{code}}.{sec}[]"
        for r, x in records(L["literature-evidence.json"], root):
            sloc = P("literature-evidence.json", f"{root}.statement", r)
            rec = S.ent("evidence_statement", mkid("EVS", f"{r[0]}|{kind}|{x['statement']}"), [loc(sloc)])
            S.dattr(rec, "kind", kind, [loc(sloc)])
            S.dattr(rec, "modality_code", r[0], [loc(sloc)])
            collect(S, "evidence_statement", rec, "literature-evidence.json", root, r, x)
            out[rec["id"]] = (rec, r, x, sec)
    S.ctx["evs"] = out
    return out


def rule_id(kind, text):
    """clinical_rule 식별자 = kind + 정규화 문장(ERD §2.18 · v3.1 id_rule.clinical_rule)."""
    return mkid("RUL", f"{kind}|{norm(text)}")


def build_rules(S):
    L = S.ctx["L"]
    out = {}
    specs = [("treatment-sequence.json", "principles[]", "principle"), ("treatment-optimization.json", "optimization_principles[]", "principle")]
    for file, path, kind in specs:
        for p, r, v in leaves(L[file]):
            if p == path:
                pv = P(file, p, r)
                rec = S.ent("clinical_rule", rule_id(kind, v), [loc(pv)])
                S.dattr(rec, "kind", kind, [loc(pv)])
                S.attr(rec, "text", v, pv)
                S.dattr(rec, "source_locator", loc(pv), [loc(pv)], replace=False)
    for r, x in records(L["treatment-optimization.json"], "combination_rules[]"):
        pv = P("treatment-optimization.json", "combination_rules[].rule", r)
        rec = S.ent("clinical_rule", rule_id("combination_rule", x["rule"]), [loc(pv)])
        S.dattr(rec, "kind", "combination_rule", [loc(pv)])
        S.dattr(rec, "source_locator", loc(pv), [loc(pv)], replace=False)
        collect(S, "clinical_rule", rec, "treatment-optimization.json", "combination_rules[]", r, x)
        out[rec["id"]] = (rec, r, x)
    csf = L["anatomy-danger-zones.json"].get("critical_safety_facts") or {}
    for k, v in csf.items():
        pv = P("anatomy-danger-zones.json", f"critical_safety_facts.{k}", ())
        rec = S.ent("clinical_rule", rule_id("critical_safety_fact", v), [loc(pv)])
        S.dattr(rec, "kind", "critical_safety_fact", [loc(pv)])
        S.attr(rec, "text", v, pv)
        S.dattr(rec, "topic", k, [loc(pv)])
        S.dattr(rec, "source_locator", loc(pv), [loc(pv)], replace=False)
    # v3.1(V3.1-7) 필수 고지 — 문장마다 clinical_rule(kind=disclosure · 같은 정규화 문장은 레코드 하나) · R32(basis=ledger)는 관계에서
    AU = S.ctx.get("AU_live")
    disc = OrderedDict()
    for r, c in records(L["consent-checklist.json"], "categories[]"):
        for i, x in enumerate(c.get("mandatory_disclosures") or []):
            pv = P("consent-checklist.json", "categories[].mandatory_disclosures[]", r + (i,))
            rec = S.ent("clinical_rule", rule_id("disclosure", x), [loc(pv)])
            if "kind" not in rec["attrs"]:
                S.dattr(rec, "kind", "disclosure", [loc(pv)])
            S.attr(rec, "text", x, pv)
            S.dattr(rec, "source_locator", loc(pv), [loc(pv)], replace=False)
            d = disc.setdefault(rec["id"], {"rec": rec, "codes": [], "code_prov": [], "phrases": []})
            if c["id"] not in d["codes"]:
                d["codes"].append(c["id"])
                d["code_prov"].append(loc(P("consent-checklist.json", "categories[].id", r)))
            erd_loc = f"consent-checklist.json:categories[].mandatory_disclosures[]@{c['id']}/{i}"
            if AU is not None and erd_loc in AU.loc_phrase and AU.loc_phrase[erd_loc] not in d["phrases"]:
                d["phrases"].append(AU.loc_phrase[erd_loc])
            S.ctx.setdefault("disclosure_edges", []).append((rec["id"], c["id"], pv, r))
    for rid, d in disc.items():
        S.dattr(d["rec"], "modality_codes", d["codes"], d["code_prov"])
        S.dattr(d["rec"], "phrase_ids", d["phrases"], [loc(c["prov"][0]) for c in d["rec"]["attrs"]["text"]])
    S.ctx["rules_combo"] = out
    return out


# ---------------------------------------------------------------------------
# package
# ---------------------------------------------------------------------------
def build_packages(S):
    L = S.ctx["L"]
    pk = {}

    def mk(kind, file, name, parent, df):
        pid = mkid("PKG", f"{kind}|{file}|{name}|{parent}")
        rec = S.ent("package", pid, df)
        if "kind" not in rec["attrs"]:
            S.dattr(rec, "kind", kind, df)
        return rec

    for r, c in records(L["problem-combos.json"], "combos[]"):
        for pi, pg in enumerate(c["packages"]):
            rr = r + (pi,)
            nl = P("problem-combos.json", "combos[].packages[].name", rr)
            rec = mk("consult_package", "problem-combos.json", pg["name"], c["problem_id"], [loc(nl)])
            collect(S, "package", rec, "problem-combos.json", "combos[].packages[]", rr, pg)
            S.alias(rec, pg.get("id"), P("problem-combos.json", "combos[].packages[].id", rr))
            pk[("problem-combos.json", rr)] = rec
    for r, x in records(L["combo-recipes.json"], "recipes[]"):
        nl = P("combo-recipes.json", "recipes[].name", r)
        rec = mk("recipe", "combo-recipes.json", x["name"], "", [loc(nl)])
        collect(S, "package", rec, "combo-recipes.json", "recipes[]", r, x)
        S.alias(rec, x.get("id"), P("combo-recipes.json", "recipes[].id", r))
        pk[("combo-recipes.json", r)] = rec
    for r, x in records(L["treatment-sequence.json"], "common_combos[]"):
        nl = P("treatment-sequence.json", "common_combos[].name", r)
        rec = mk("session_combo", "treatment-sequence.json", x["name"], "", [loc(nl)])
        collect(S, "package", rec, "treatment-sequence.json", "common_combos[]", r, x)
        pk[("treatment-sequence.json", r)] = rec
    for r, p in records(L["problem-packages.json"], "problems[]"):
        for ci, c in enumerate(p["complaints"]):
            for bi, b in enumerate(c.get("combos") or []):
                rr = r + (ci, bi)
                nl = P("problem-packages.json", "problems[].complaints[].combos[].name", rr)
                rec = mk("cc_combo", "problem-packages.json", b["name"], f"{p['problem_id']}|{c['cc']}|{'+'.join(b.get('combo') or [])}", [loc(nl)])
                collect(S, "package", rec, "problem-packages.json", "problems[].complaints[].combos[]", rr, b)
                pk[("problem-packages.json", rr)] = rec
    for r, c in records(L["treatment-optimization.json"], "by_concern[]"):
        for si, sv in enumerate(c["severity_levels"]):
            rr = r + (si,)
            nl = P("treatment-optimization.json", "by_concern[].severity_levels[].level", rr)
            name = f"{c['concern']} · {sv['level']}"
            rec = mk("optimization_plan", "treatment-optimization.json", name, "", [loc(P("treatment-optimization.json", "by_concern[].concern", r)), loc(nl)])
            if "name" not in rec["attrs"]:
                S.dattr(rec, "name", name, [loc(P("treatment-optimization.json", "by_concern[].concern", r)), loc(nl)])
            collect(S, "package", rec, "treatment-optimization.json", "by_concern[].severity_levels[]", rr, sv)
            pk[("treatment-optimization.json/by_concern", rr)] = rec
    for r, x in records(L["treatment-optimization.json"], "annual_plans[]"):
        nl = P("treatment-optimization.json", "annual_plans[].plan_name", r)
        rec = mk("annual_plan", "treatment-optimization.json", x["plan_name"], x.get("age_group", ""), [loc(nl)])
        collect(S, "package", rec, "treatment-optimization.json", "annual_plans[]", r, x)
        pk[("treatment-optimization.json/annual", r)] = rec
    for r, x in records(L["procedure-comparison.json"], "comparisons[]"):
        nl = P("procedure-comparison.json", "comparisons[].title", r)
        rec = mk("comparison", "procedure-comparison.json", x["title"], x.get("id", ""), [loc(nl)])
        collect(S, "package", rec, "procedure-comparison.json", "comparisons[]", r, x)
        S.alias(rec, x.get("id"), P("procedure-comparison.json", "comparisons[].id", r))
        pk[("procedure-comparison.json", r)] = rec
    S.ctx["pkgs"] = pk
    return pk


# ---------------------------------------------------------------------------
# procedure (튜플) — anchor 지도에서
# ---------------------------------------------------------------------------
def build_procedures(S, AM):
    """AM = anchors.AnchorMap(결정 ②③④ 적용 뒤). 튜플 id 마다 레코드 하나."""
    ids = S.ctx["ids"]
    for tid, t in AM.tuples().items():
        df = sorted(set(t["occ"]))
        rec = S.ent("procedure", tid, df)
        for a in ("what_kind", "what_id", "site_id", "technique_id", "technique_origin", "anchor", "all_dict_values", "status"):
            S.dattr(rec, a, t[a], df)
        S.dattr(rec, "origins", sorted(t["origins"]), df)
        S.dattr(rec, "unregistered_fragments", t["unregistered_fragments"], df)
        S.dattr(rec, "candidate_name", t["candidate_name"], df)
        S.dattr(rec, "extra_primaries", t["extra_primaries"], df)
        S.dattr(rec, "extra_sites", t["extra_sites"], df)
        S.dattr(rec, "anchors", sorted(t["anchors"]), df)
        if S.ctx.get("is32"):   # v3.2(V3.2-1 · V3.2-6 · V3.2-2) — 이름·참조 분해의 보존 조각(칸 아님)
            S.dattr(rec, "grammar_tokens", list(t.get("grammar_tokens") or []), df)
            S.dattr(rec, "ingredient_fragments", list(t.get("ingredient_fragments") or []), df)
            if t.get("gloss"):
                S.dattr(rec, "gloss", list(t["gloss"]), df)
        if t.get("decision_ids"):
            S.dattr(rec, "decision_ids", sorted(t["decision_ids"]), sorted(t["decision_ids"]))
        if t.get("alias_ids"):
            for a in t["alias_ids"]:
                rec["aliases"].append({"value": a, "derived_from": df})


# ---------------------------------------------------------------------------
# adverse_effect(v3.1 세 칸) — 문구는 개체가 아니다(문구 사전 · 부록)
# ---------------------------------------------------------------------------
ADV_ATTRS = ("event_kind", "event", "event_id", "event_category", "site_kind", "site", "site_id", "site_dict_kind", "qualifier", "qualifier_id", "qualifier_basis", "status", "anchor", "all_dict_values",
             "candidate_name", "event_fragments", "extra_sites", "extra_courses", "extra_qualifiers", "dict_tuples", "raw_reason", "site_basis", "unregistered_fragments", "relative_site_text", "created_by_phrase")


ADV_ATTRS_V32 = ("event_kind", "event", "event_id", "event_category", "site_kind", "site", "site_id", "site_dict_kind", "qualifier", "qualifier_id", "qualifier_basis", "status", "all_dict_values",
                 "extra_sites", "extra_qualifiers", "site_basis", "relative_site_text", "created_by_phrase", "event_origin_locators", "general_description", "general_management", "side_fragments")
ADV_ATTRS_V33 = tuple(a for a in ADV_ATTRS_V32 if a != "event_category")   # v3.3(V3.3-E): 사건 사전 category 삭제 — 단위 레코드에 event_category 없음


def build_adverse(S, AU):
    """AU = units31.AdverseUnits(결정 ①③④⑤ 적용 · finish 뒤). v3.2: 이름 단위(raw_name) 속성 없음 · event_kind dict|ledger · 일반값 참조(V3.2-8) · side_fragments. v3.3: event_category 없음."""
    attrs = ADV_ATTRS_V33 if S.ctx.get("is33") else (ADV_ATTRS_V32 if S.ctx.get("is32") else ADV_ATTRS)
    for uid, u in AU.units.items():
        df = sorted(set(u["occ"]))
        rec = S.ent("adverse_effect", uid, df)
        for a in attrs:
            S.dattr(rec, {"site_kind": "site_ref_kind", "site_id": "site_ref_id"}.get(a, a), u.get(a), df)
        S.dattr(rec, "origins", sorted(set(u["origins"])), df)
        S.dattr(rec, "explanations", u.get("explanations") or [], df)
        if u.get("decision_ids"):
            S.dattr(rec, "decision_ids", sorted(u["decision_ids"]), sorted(u["decision_ids"]))
