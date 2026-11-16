# -*- coding: utf-8 -*-
"""결정 묶음 2B 게이트 자료 — `decisions/proposed/templates/` 11 항목을 사람이 고를 수 있게 내용을 채운다.

out/gate/batch2b.json(웹 페이지 입력) · batch2b.md(사람 읽기). 항목·하위 항목마다 options[].decision_payload 는
그 옵션을 고르면 만들어질 결정 파일 본문 그대로(kind·target·new_value 완성형 · status=proposed)다 — `apply_gate.py` 가
status=approved · decided_by · decided_at 을 채워 decisions/batch2b/ 에 쓴다. 결정 없음(지금대로)은 decision_payload=null.

원문은 브론즈 원장에서 locator 로 직접 읽는다(lib.provenance.resolve). recommended 는 원장 근거가 있을 때만 — 없으면 null.
"""
import json
import os
import re
from collections import OrderedDict, defaultdict

from .decisions import validate
from .provenance import parse_loc, rec_str, resolve
from .util import dedupe, md_table, mkid, norm, write_json, write_text

BATCH = "DEC-2026-11-04-B2B"
ERD_REF = "erd-v2.4.md §12"


class G:
    def __init__(self, S, decisions_dir):
        self.S = S
        self.ctx = S.ctx
        self.L = S.ctx["L"]
        self.ids = S.ctx["ids"]
        self.AM = S.ctx["AM"]
        self.AU = S.ctx["AU"]
        self.dicts = S.ctx["dicts"]
        self.store = []
        for root, dirs, files in os.walk(decisions_dir):
            dirs.sort()
            for f in sorted(files):
                if f.endswith(".json") and not f.startswith("_"):
                    try:
                        d = json.load(open(os.path.join(root, f), encoding="utf-8"))
                    except Exception:
                        continue
                    if isinstance(d, dict) and d.get("status") == "approved":
                        self.store.append(d)
        P = S.ctx["proc"]
        self.ref_info = defaultdict(list)
        for slot, rows in list(P["ref_rows"].items()) + [("market-pricing.items[].name", P["mk_rows"])]:
            for r in rows:
                self.ref_info[r["ref_id"]].append({"slot": slot, "label": r["label"], "hint": r["hint"], "result": r["result"], "qualifiers": r.get("qualifiers") or [],
                                                   "family_fragments": r.get("family_fragments") or [], "unresolved_reason": r.get("unresolved_reason"), "row": r})
        self.cat_info = {c["catalog_item_id"]: c for c in P["cat_recs"]}
        self.item_by_cat = {it["cat"]["catalog_item_id"]: (fam, name, it) for (fam, name), it in S.ctx["items"].items()}
        self.unres = defaultdict(list)
        for c in S.conflicts:
            if c["kind"] == "unresolved_reference" and c.get("ref_id"):
                self.unres[c["ref_id"]].extend(c["stable_key"]["locators"])
        self.dup = [c for c in S.conflicts if c["kind"] == "duplicate_candidate"]
        # ERD 꼴 locator(complications 이름 `@M16/4` · 표현 `@<계열>/<순번>` — 결정 target·anchor 용) → 원장 위치 locator(배열 인덱스 · 코드 키)
        from .provenance import loc as _loc
        self.erd2src = {k: _loc(v) for k, v in self.AU.erd2p.items()}   # v3.1 — units31.AdverseUnits.erd2p(이름 · 문구 자리)

    # ------------------------------------------------------------------ 원문
    def ev(self, lc, note=None):
        """locator → 원장 원문. 원장 위치 locator 를 먼저, 안 되면 ERD 꼴 locator 를 원장 위치로 옮겨 읽는다."""
        p = parse_loc(lc)
        src = lc
        try:
            v = resolve(self.L[p["file"]], p["path"], p["rec"])
        except Exception as e:  # noqa: BLE001
            src = self.erd2src.get(lc)
            if src is None:
                v = f"<읽기 실패 {e} — ERD 꼴 locator 대응 없음>"
            else:
                q = parse_loc(src)
                try:
                    v = resolve(self.L[q["file"]], q["path"], q["rec"])
                except Exception as e2:  # noqa: BLE001
                    v = f"<읽기 실패 {e2}>"
        o = OrderedDict([("file", p["file"]), ("locator", lc), ("text", v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))])
        if src and src != lc:
            o["source_locator"] = src
        if note:
            o["note"] = note
        return o

    def evs(self, locs, note=None):
        return [self.ev(x, note) for x in dedupe(locs)]

    # ------------------------------------------------------------------ anchor
    def anchor_locs(self, a):
        s = self.AM.spec.get(a)
        if s and s.get("occ"):
            return list(s["occ"])
        if a in self.item_by_cat:
            return [self.item_by_cat[a][2]["name_loc"]]
        return list(self.unres.get(a, []))

    def anchor_desc(self, a):
        if a in self.item_by_cat:
            fam, name, it = self.item_by_cat[a]
            d = {"anchor": a, "kind": "catalog_item", "label": name, "hint": fam}
        else:
            infos = self.ref_info.get(a, [])
            d = {"anchor": a, "kind": "reference", "label": infos[0]["label"] if infos else None, "hint": infos[0]["hint"] if infos else None,
                 "slots": dedupe(i["slot"] for i in infos)}
        s = self.AM.spec.get(a)
        if s and not s.get("virtual"):
            d["now"] = {"what_kind": s["what_kind"], "what_id": s["what_id"], "what_label": s["what_label"], "site": s["site"], "technique": s["technique"], "status": s["status"]}
        elif a in self.AM.multi:
            d["now"] = {"combo_members": self.AM.multi[a]}
        else:
            d["now"] = {"unresolved": True}
        d["occurrences"] = len(self.anchor_locs(a))
        return d

    def already(self, payload):
        if not payload:
            return []
        out = []
        for d in self.store:
            if d.get("kind") == payload["kind"] and json.dumps(d.get("target"), sort_keys=True, ensure_ascii=False) == json.dumps(payload["target"], sort_keys=True, ensure_ascii=False):
                out.append(d["id"])
        return out

    def dup_key(self, locs):
        want = set(locs)
        for c in self.dup:
            if set(c["stable_key"]["locators"]) == want:
                return c["stable_key"]
        return None

    # ------------------------------------------------------------------ 사전 id
    def event(self, label):
        e = self.ids.event[norm(label)]
        return e["id"]

    def course(self, label):
        return self.ids.course[norm(label)]["id"]

    def site(self, label):
        """부작용 축 부위 — 분해 순서대로 상대 부위 사전 → 부위 사전(§1.5)."""
        if label in (None, "none"):
            return "none"
        if norm(label) in self.ids.rsite:
            return self.ids.rsite[norm(label)]["id"]
        return self.ids.site[norm(label)]["id"]

    def unit_triplet(self, uid):
        u = self.AU.units[uid]
        return {"event_id": u["event_id"], "site_id": u.get("site_id") or "none", "course_id": u["course_id"]}, f"({u['event']}, {u['site'] or 'none'}, {u['course']})"


def payload(pid, kind, target, new_value, reason, refs, extra=None):
    p = OrderedDict([("id", pid), ("kind", kind), ("target", target), ("new_value", new_value), ("reason", reason), ("decided_by", None), ("decided_at", None),
                     ("status", "proposed"), ("source_refs", [{"kind": "ledger", "ref": r} for r in dedupe(refs)] + [{"kind": "erd", "ref": ERD_REF}])])
    if extra:
        p.update(extra)
    return p


def opt(key, label, effect, pl):
    return OrderedDict([("key", key), ("label", label), ("effect", effect), ("decision_payload", pl)])


def node(id_, kind, title, why, evidence, options, recommended, reason, extra=None):
    o = OrderedDict([("id", id_), ("kind", kind), ("title", title), ("why", why), ("evidence", evidence), ("options", options),
                     ("recommended", recommended), ("recommend_reason", reason)])
    if extra:
        o.update(extra)
    return o


# =====================================================================================
# 항목 11
# =====================================================================================
def item_botox(g):
    pb = g.ids.prod[norm("보톡스")]
    mod = g.ids.mod["M1"]
    anchors = [a for a, s in g.AM.spec.items() if not s.get("virtual") and s["what_id"] == pb["id"]]
    prod_locs = []
    for fn in ("products.json", "taxonomy.json"):
        from .provenance import leaves
        for p, r, v in leaves(g.L[fn]):
            if p.endswith("products[].name") and v == "보톡스":
                prod_locs.append(f"{fn}:{p}@{rec_str(r) if isinstance(r, tuple) else r}")
    mi = next(i for i, m in enumerate(g.L["taxonomy.json"]["modality"]) if m["id"] == "M1")
    cat_loc = f"taxonomy.json:modality[].category@{mi}"
    occ = [x for a in anchors for x in g.anchor_locs(a)]
    ev = g.evs(prod_locs, "제품 이름 자리") + g.evs([cat_loc], "계열 이름 자리(M1)") + g.evs(occ, "「보톡스」가 PRD 로 풀린 참조 자리")
    pl = payload(f"{BATCH}-BTX-01", "canonical_mapping", {"from_ref": pb["id"], "scope": anchors}, {"to_id": mod["id"]},
                 "결정 묶음 2B — 「보톡스」를 참조 자리에서 계열 M1(MOD) 로 읽는다(검토 1-C)", prod_locs + [cat_loc] + occ)
    opts = [opt("to_modality", "계열 M1 「보톡스」로 읽는다", f"참조 anchor {len(anchors)} 의 튜플 what 이 PRD-보톡스 → MOD-M1(계열)로 바뀐다. 튜플 id 가 바뀌고(anchor 는 그대로) 엣지가 따라간다. 제품 노드 PRD-보톡스(products[] 자리 R9 등)는 그대로", pl),
            opt("keep_product", "지금대로 제품 PRD-보톡스", "결정 없음 — 분해 규칙 6(계열·제품 양쪽이면 product) 그대로", None)]
    return node("botox-product-vs-modality", "canonical_mapping", "참조 자리의 「보톡스」를 제품(PRD-보톡스)으로 둘까, 계열(M1 보톡스)로 읽을까?",
                "원장에 「보톡스」가 제품 이름(products.json botulinum_toxin.products[] · taxonomy modality[].products[])이면서 계열 M1 의 이름(taxonomy modality[].category)으로도 있다. 분해 규칙 6 은 양쪽에 닿으면 product 로 정할 뿐, 원장이 어느 뜻인지는 말하지 않는다.",
                ev, opts, None, "원장이 두 뜻을 다 갖고 있어 어느 쪽이라는 근거가 없다(추천 없음).",
                {"anchors": [g.anchor_desc(a) for a in anchors], "related": ["same-three-cells-21 의 PRD-보톡스 조(REF-9a0f3675e7 · REF-23605eeac1)와 함께 본다"]})


EVENT_SPLITS = [("과민반응", "아나필락시스", []), ("동상", "괴사", ["Frostbite"]), ("지방괴사", "괴사", ["Fat Necrosis"]), ("섬유화", "경결", []), ("공기색전", "색전", [])]


def item_event_split(g):
    A = g.ctx["adv"]
    subs = []
    for i, (term, orig, eng) in enumerate(EVENT_SPLITS, 1):
        ent = next(e for e in g.dicts["adverse_event_type"]["entries"] if e["canonical"] == orig)
        names = [r["locator"] for r in A["comp_rows"] if term in r["text"]]
        exprs = [r["locator"] for r in A["expr_rows"] if term in r["text"]]
        pl = payload(f"{BATCH}-EVS-{i:02d}", "event_split", {"event": orig}, {"new_events": [{"canonical": term, "synonyms": eng, "category": ent.get("category")}]},
                     f"결정 묶음 2B — 사건 사전 「{orig}」에서 「{term}」을 따로 세운다(검토 2-C)", names + exprs)
        subs.append(node(f"event-split/{term}", "event_split", f"「{term}」을 「{orig}」과 다른 사건으로 나눌까?",
                         f"사건 사전에서 「{term}」은 「{orig}」의 동의어다(complications 이름에서 온 동의어). 같은 사건인지는 임상 판단(⑩ 사람만)이라 기계가 정하지 않는다. 나누면 이 말이 든 이름·표현이 다시 분해된다.",
                         g.evs(names, "complications 이름") + g.evs(exprs, "표현 원문"),
                         [opt("split", f"「{term}」을 새 사건으로", f"사건 사전에 「{term}」(category {ent.get('category')}) 가 생기고 「{orig}」 동의어에서 빠진다" + (f"(영문 {', '.join(eng)} 도 같이 옮긴다)" if eng else "") + f". 이름 {len(names)} · 표현 {len(exprs)} 이 다시 분해되어 단위·R29 가 바뀐다", pl),
                          opt("keep", f"지금대로 「{orig}」의 동의어", "결정 없음", None)],
                         None, "같은 사건인지는 임상 판단이고 원장이 둘을 가르는 문장을 두지 않았다(추천 없음).",
                         {"dictionary_entry": {"canonical": orig, "id": ent["id"], "category": ent.get("category"), "synonyms": [s["value"] for s in ent["synonyms"]]}}))
    return node("event-split", "event_split", "사건 사전의 동의어 5 개를 따로 세울까?(하위 5)", "사건 사전이 다른 사건일 수 있는 말을 동의어로 묶어 두었다(검토 2-C). 하위 항목마다 따로 고른다.",
                [], [], None, "하위 항목마다", {"subitems": subs})


def item_excel(g):
    a = "CAT-af03bac034"
    fam, name, it = g.item_by_cat[a]
    s = g.AM.spec[a]
    plus = g.ids.prod[norm("엑셀 V+")]
    base = g.ids.prod[norm("엑셀V")]
    rec = it["name_loc"].rsplit("@", 1)[1]
    det = f"taxonomy.json:modality[].subcategories[].items[].detail@{rec}"
    dec = json.load(open(os.path.join(g.ctx["args"].decisions, "batch1", "DEC-2026-11-04-B1-PRD-061.json"), encoding="utf-8"))
    st1 = [r["ref"] for r in dec["source_refs"] if r["kind"] == "ledger"]
    ev = g.evs([it["name_loc"], det], "분류 항목") + g.evs(st1, "step1 조사(결정 묶음 1 B1-PRD-061 의 근거)") + g.evs(g.anchor_locs("REF-43a22d6f4b"), "「엑셀V」 참조 자리")
    refs = [it["name_loc"], det] + st1

    def ta(pid, w):
        return payload(pid, "tuple_assign", {"catalog_item_id": a}, {"what_kind": "product", "what_id": w["id"], "site_id": "none", "technique_id": "none"},
                       f"결정 묶음 2B — 엑셀V+ 의 what 을 {w['label']} 로 고정(검토 1-D)", refs)
    opts = [opt("keep", "지금대로(제품 「엑셀 V+」)", f"결정 없음 — 결정 묶음 1(B1-PRD-061)로 이미 what = 제품 「{s['what_label']}」({s['what_id']})", None),
            opt("pin_plus", "제품 「엑셀 V+」로 고정", "tuple_assign 으로 같은 값을 결정에 박는다 — 제품 사전이 바뀌어도 이 항목은 엑셀 V+", ta(f"{BATCH}-EXV-01", plus)),
            opt("to_excelv", "제품 「엑셀V」로", f"what 을 {base['id']}(엑셀V)로 — 「+」 를 버린 v2.4 분해 결과로 되돌린다", ta(f"{BATCH}-EXV-01", base)),
            opt("self", "분류 항목 자신(CAT)", "what = 분류 항목 자신(catalog_item) — 제품 노드와 잇지 않는다",
                payload(f"{BATCH}-EXV-01", "tuple_assign", {"catalog_item_id": a}, {"what_kind": "catalog_item", "what_id": a, "site_id": "none", "technique_id": "none"}, "결정 묶음 2B — 엑셀V+ 의 what 을 항목 자신으로(검토 1-D)", refs))]
    return node("excel-v-plus", "tuple_assign", "분류 항목 「엑셀V+」[M8]의 what 을 무엇으로 둘까?",
                "v2.4 분해는 「엑셀V+」의 `+` 뒤 빈 멤버를 버려 what = 엑셀V 로 만들었다(검토 1-D). 결정 묶음 1 에서 step1 의 「엑셀 V+」가 제품 사전에 들어가 지금은 what = 제품 「엑셀 V+」다. 이대로 둘지 사람이 확인한다.",
                ev, opts, "keep", "원장 taxonomy detail 「큐테라 532/1064nm」 과 step1 허가 「수허 20-31 호」가 「엑셀 V+」를 별도 장비로 적는다 — 지금 값이 원장과 맞아 결정이 필요 없다.",
                {"anchors": [g.anchor_desc(a)]})


def item_injection_site(g):
    lc = "complications.json:categories[].complications[].name@M1/2"
    A = g.ctx["adv"]
    m1 = [r for r in A["expr_rows"] if r.get("modality") == "M1" and any(c.get("event") == "부종" and c.get("site") == "주사 부위" for c in r["candidates"])]
    cur = [g.unit_triplet(u) for u in g.AU.name_units[lc]]
    tup = [{"event_id": g.event("홍반"), "site_id": g.site("주사 부위"), "course_id": g.course("미상")}, {"event_id": g.event("부종"), "site_id": g.site("주사 부위"), "course_id": g.course("미상")}]
    pl = payload(f"{BATCH}-ISE-01", "adverse_tuple_assign", {"locator": lc, "kind": "raw_name"}, {"tuples": tup},
                 "결정 묶음 2B — 「주사 부위 홍반·부종」의 부종에도 주사 부위를 준다(§9.6.2b · 검토 v2.4 결정 2)", [lc] + [r["locator"] for r in m1])
    return node("injection-site-erythema-edema", "adverse_tuple_assign", "complications 「주사 부위 홍반·부종」[M1]의 부종도 「주사 부위」로 볼까?",
                "원칙 C(수식어는 같은 멤버 안의 사건에만)로 기계는 「주사 부위」를 홍반에만 주고 부종은 부위 none 으로 뒀다. 「·」 앞뒤가 한 부위를 공유하는지는 문장 해석이라 기계가 끌어오지 않는다.",
                g.evs([lc], "대상 이름") + g.evs([r["locator"] for r in m1], "M1 원장의 「주사/주입 부위 … 부종」 표현"),
                [opt("both_site", "홍반·부종 둘 다 주사 부위", "이 이름의 단위가 (홍반, 주사 부위, 미상) + (부종, 주사 부위, 미상) 으로 바뀐다 — (부종, 주사 부위, 미상) 단위가 없으면 결정이 세운다. 원래 (부종, none, 미상) 은 다른 이름이 쓰면 남는다", pl),
                 opt("keep", "지금대로(부종은 none)", "결정 없음 — 지금 " + " + ".join(c[1] for c in cur), None)],
                "both_site", f"같은 M1 원장이 「주입 부위 부종」「주사 부위 부종, 멍」 등 부종을 주사 부위에 둔 표현을 {len(m1)} 곳 적는다(위 evidence).",
                {"target_kind_note": "target.kind 는 raw_name — 빌더는 complications 이름 locator 를 kind=raw_name 으로 받는다(이 이름 자체는 dict 튜플)"})


def item_mface(g):
    subs = []
    pairs = [("엠페이스", ["CAT-05d25fb165", "CAT-96a86bdbe8"], "CAT-05d25fb165"), ("라라젯", ["CAT-494e06af10", "CAT-53cb7ccd54"], None)]
    for i, (nm, anchors, keep) in enumerate(pairs, 1):
        locs = [g.item_by_cat[a][2]["name_loc"] for a in anchors]
        dets = ["taxonomy.json:modality[].subcategories[].items[].detail@" + x.rsplit("@", 1)[1] for x in locs]
        subl = []
        for x in locs:
            r = x.rsplit("@", 1)[1].split("/")
            subl.append(f"taxonomy.json:modality[].subcategories[].label@{r[0]}/{r[1]}")
        key = g.dup_key(locs)
        refs = locs + dets + subl
        ev = g.evs(locs, "분류 항목 이름") + g.evs(dets, "detail") + g.evs(subl, "그 항목의 하위분류")
        extra_ev = []
        if nm == "엠페이스":
            dec = json.load(open(os.path.join(g.ctx["args"].decisions, "batch1", "DEC-2026-11-04-B1-PRD-104.json"), encoding="utf-8"))
            st1 = [r["ref"] for r in dec["source_refs"] if r["kind"] == "ledger"]
            extra_ev = g.evs(st1, "step1 조사(B1-PRD-104 — 엠페이스 = EMFACE)")
            refs += st1
        opts = []
        k = keep or anchors[0]
        opts.append(opt("fold", f"같은 것 — 합친다(keep {k})", f"두 항목의 튜플을 {k} 의 튜플로 합친다(나머지 튜플 id 는 alias · R26·엣지 이동). ⑦ duplicate_candidate 는 현재 빌더가 fold 로 닫지 않는다",
                        payload(f"{BATCH}-MFC-{i:02d}", "fold_approve", {"anchors": anchors}, {"keep_anchor": k}, f"결정 묶음 2B — 「{nm}」 두 분류 항목은 같은 시술", refs)))
        if key:
            opts.append(opt("not_same", "다른 것 — 따로 둔다", "⑦ duplicate_candidate 를 not_same 으로 닫는다(dismissed) · 튜플은 각자",
                            payload(f"{BATCH}-MFC-{i:02d}", "conflict_close", {"conflict_key": key}, {"verdict": "not_same", "note": f"「{nm}」 두 분류 항목은 다른 시술"}, f"결정 묶음 2B — 「{nm}」 두 분류 항목은 다른 것", refs)))
        opts.append(opt("keep", "지금대로(판정 보류)", "결정 없음 — ⑦ open 유지", None))
        if nm == "엠페이스":
            rec, rr = "fold", "두 항목이 같은 하위분류(M10-1 페이셜 EMS)에 있고 detail 이 둘 다 BTL 의 HIFES 장비(「BTL · RF+HIFES」「BTL안면HIFES」)이며, step1 조사가 「엠페이스」의 검색명으로 EMFACE 를 적는다. keep 은 원장 id 가 붙은 M10-1-1(엠페이스(EMFACE))."
        else:
            rec, rr = "not_same", "원장이 두 항목을 서로 다른 하위분류(M15-2 딥클렌징 · M15-6 주입장비)에 두고 detail 도 다르다(「」 · 「공기압 약물주입」)."
        subs.append(node(f"mface-like/{nm}", "fold_approve|conflict_close", f"분류 항목 「{nm}」 두 개를 같은 시술로 합칠까?",
                         "원장 taxonomy 에 같은 이름(괄호만 다름)의 항목이 둘 있다. 표면형만 비슷한 것은 ⑦ 후보로 올라가고, 같은 것인지는 사람이 정한다.",
                         ev + extra_ev, opts, rec, rr, {"anchors": [g.anchor_desc(a) for a in anchors], "conflict_key": key}))
    return node("mface-like", "fold_approve|conflict_close", "엠페이스류 — 이름이 거의 같은 분류 항목 쌍을 합칠까?(하위 2)", "괄호만 다른 같은 이름 항목 쌍(검토 1-G · §9.5.3).", [], [], None, "하위 항목마다", {"subitems": subs})


PAREN = [("#36", "M9/4", "drop_unknown", "괄호 안 「따끔거림·저림·감각둔화」는 사건 사전에서 전부 바깥 「감각이상」(감각 이상)의 동의어다 — 괄호가 새 사건을 더하지 않는다."),
         ("#45", "M14/2", None, "(감각 이상, 미상)은 괄호 안이 아니라 바깥 「·」 뒤 「저림」에서 나온다 — 「일시적」이 「저림」에도 걸리는지 원장이 말하지 않는다."),
         ("#46", "M14/3", "drop_unknown", "괄호 안 (Erythema / Edema)는 바깥 「홍반·부종」의 영문 표기다 — Erythema·Edema 는 사건 사전에서 홍반·부종의 동의어."),
         ("#58", "M16/4", None, "(경결, 일시)는 괄호 안 「일시적 섬유화」에서 나온다 — 섬유화를 경결로 볼지가 event-split/섬유화 결정에 달려 있다.")]


def item_paren(g):
    A = g.ctx["adv"]
    rows = {r["locator"]: r for r in A["comp_rows"]}
    subs = []
    for i, (no, rec, recm, rr) in enumerate(PAREN, 1):
        lc = f"complications.json:categories[].complications[].name@{rec}"
        cur = [g.unit_triplet(u) for u in g.AU.name_units[lc]]
        opts = []
        seen = set()
        known = [c for c in cur if "미상" not in c[1]]
        unknown = [c for c in cur if "미상" in c[1]]
        if no in ("#36", "#45"):
            keep_t = [c for c in cur if c[1].endswith("일시)")]
        elif no == "#46":
            keep_t = [c for c in cur if c[1] != "(홍반, none, 미상)"]
        else:
            keep_t = [c for c in cur if c[1].endswith("일시)")]
        pl = payload(f"{BATCH}-PAR-{i:02d}", "adverse_tuple_assign", {"locator": lc, "kind": "raw_name"}, {"tuples": [c[0] for c in keep_t]},
                     f"결정 묶음 2B — 「{rows[lc]['text']}」의 괄호 안 동의어가 만든 미상 튜플을 뺀다(§9.6.2a · 검토 v2.4 {no})", [lc])
        opts.append(opt("drop_unknown", "미상 튜플을 뺀다 → " + " + ".join(c[1] for c in keep_t), "이 이름의 단위가 " + " + ".join(c[1] for c in keep_t) + " 로 바뀐다. 빠진 단위는 다른 이름이 쓰면 남는다", pl))
        if no == "#58":
            alt = [c for c in cur if c[1].endswith("미상)")]
            opts.append(opt("only_unknown", "(경결, none, 미상) 하나만", "괄호 안 「일시적 섬유화」의 경과를 쓰지 않는다",
                            payload(f"{BATCH}-PAR-{i:02d}", "adverse_tuple_assign", {"locator": lc, "kind": "raw_name"}, {"tuples": [c[0] for c in alt]}, f"결정 묶음 2B — 「{rows[lc]['text']}」 → (경결, 미상) 하나", [lc])))
        opts.append(opt("keep", "지금대로(" + " + ".join(c[1] for c in cur) + ")", "결정 없음", None))
        subs.append(node(f"paren-synonym-unknown-tuples-4/{no}", "adverse_tuple_assign", f"「{rows[lc]['text']}」의 같은 사건 미상 튜플을 뺄까?",
                         "괄호 안 동의어·영문 표기는 다른 멤버라(원칙 C) 바깥 수식어(일시적)를 받지 못하고 같은 사건의 (·, 미상) 튜플을 따로 만든다. 원문이 사건 하나를 두 번 적은 것인지는 기계가 정하지 않는다.",
                         g.evs([lc], "complications 이름"), opts, recm, rr, {"now": [c[1] for c in cur], "target_kind_note": "target.kind=raw_name — complications 이름 locator(이 이름 자체는 dict 튜플)"}))
    return node("paren-synonym-unknown-tuples-4", "adverse_tuple_assign", "괄호 안 동의어가 만든 같은 사건의 미상 튜플 4(하위 4)", "검토 v2.4 ②-1 #36 · #45 · #46 · #58.", [], [], None, "하위 항목마다", {"subitems": subs})


def _core(label, quals, fams):
    t = str(label)
    for k, v in quals:
        if k == "spec":
            t = t.replace(v, " ")
    for f in fams:
        t = t.replace(f.split(":", 1)[1], " ")
        for part in f.split(":", 1)[1].split("/"):
            t = t.replace(part, " ")
    t = re.sub(r"[()\[\]]", " ", t)
    return norm(t)


def item_same_three(g):
    erd_dir = os.path.dirname(os.path.abspath(g.ctx["args"].erd))
    t = json.load(open(os.path.join(erd_dir, "erd-v2.4-tuples.json"), encoding="utf-8"))["procedure"]["tuples"]
    grp = OrderedDict()
    for x in t:
        grp.setdefault((x["what_id"], x["site_id"], x["technique_id"]), []).append(x)
    grp = [(k, v) for k, v in grp.items() if len(v) > 1]
    subs = []
    for i, (k, v) in enumerate(grp, 1):
        anchors = [x["anchor"] for x in v]
        descs = [g.anchor_desc(a) for a in anchors]
        now = {(d["now"].get("what_id"), g.AM.spec[d["anchor"]]["site_id"], g.AM.spec[d["anchor"]]["technique_id"]) for d in descs}
        still = len(now) == 1
        label0 = v[0]["what_label"]
        cores = []
        for a in anchors:
            if a in g.cat_info:
                c = g.cat_info[a]
                cores.append(_core(c["name"], c.get("qualifiers") or [], c.get("family_fragments") or []))
            else:
                inf = g.ref_info[a][0]
                cores.append(_core(inf["label"], inf["qualifiers"], inf["family_fragments"]))
        locs = [x for a in anchors for x in g.anchor_locs(a)]
        cats = [a for a in anchors if a.startswith("CAT-")]
        issue = []
        for a in cats:
            rec = g.item_by_cat[a][2]["name_loc"].rsplit("@", 1)[1]
            fam, name, it = g.item_by_cat[a]
            if "classification_issue" in _item_raw(g, rec):
                issue.append((a, f"taxonomy.json:modality[].subcategories[].items[].classification_issue@{rec}"))
        if cats:
            ok = [a for a in cats if a not in {x[0] for x in issue}] or cats
            keep = sorted(ok)[0]
        else:
            keep = sorted(anchors, key=lambda a: (descs[anchors.index(a)]["hint"] is None, -descs[anchors.index(a)]["occurrences"], a))[0]
        opts = []
        refs = locs + [x[1] for x in issue]
        pl = payload(f"{BATCH}-S3C-{i:02d}", "fold_approve", {"anchors": anchors}, {"keep_anchor": keep}, f"결정 묶음 2B — 같은 세 칸({label0} × none × none)의 anchor {len(anchors)} 을 하나로(검토 1-E)", refs)
        opts.append(opt("fold", f"같은 시술 — 합친다(keep {keep})", f"anchor {len(anchors)} 의 튜플을 {keep} 의 튜플로 합친다 — 나머지 튜플 id 는 alias, R26·엣지·출처가 keep 튜플로 옮겨진다", pl))
        name_locs = [g.item_by_cat[a][2]["name_loc"] for a in cats]
        key = g.dup_key(name_locs) if len(cats) == len(anchors) else None
        if key:
            opts.append(opt("not_same", "다른 것 — 따로 둔다", "⑦ duplicate_candidate 를 not_same 으로 닫는다",
                            payload(f"{BATCH}-S3C-{i:02d}", "conflict_close", {"conflict_key": key}, {"verdict": "not_same", "note": f"{label0} anchor 들은 다른 시술"}, "결정 묶음 2B — 같은 세 칸이지만 다른 것", refs)))
        opts.append(opt("keep", "지금대로 따로", "결정 없음 — 미상 칸 때문에 anchor 마다 튜플(정의 1)", None))
        if not still:
            recm, rr = "keep", "현재 빌드에서는 세 칸이 이미 다르다: " + " · ".join(f"{d['anchor']}→{d['now'].get('what_label')}" for d in descs) + " — 결정 묶음 1(제품 사전)로 갈렸다. 합칠 대상이 아니다."
        elif len(set(cores)) == 1:
            recm = "fold"
            rr = "원장 표기에서 규격 조각(spec)·같은 계열명 조각·괄호·공백을 빼면 전부 「" + str(label_of_core(g, anchors[0])) + "」 같은 문자열이고, 갈린 까닭은 자리의 계열 힌트·규격뿐이다."
            if issue:
                rr += " keep 은 classification_issue 가 없는 쪽 — " + "; ".join(f"{a} 원장 메모: 「{g.ev(l)['text'][:60]}…」" for a, l in issue)
        else:
            recm, rr = None, "원장 표기가 규격·계열명만이 아니라 낱말이 다르다(" + " · ".join(dedupe(str(d["label"]) for d in descs)) + ") — 같은 시술이라는 원장 근거가 없다."
        subs.append(node(f"same-three-cells-21/{i:02d}", "fold_approve", f"「{label0}」 × none × none 인 anchor {len(anchors)} 을 한 시술로 합칠까?",
                         "세 칸(what·site·technique)이 같지만 site·technique 가 미상이라 정의 1 대로 anchor 마다 따로 둔 튜플이다. 합치는 것은 「같은 시술」이라는 판단이라 사람이 정한다(fold_approve).",
                         g.evs(locs), opts, recm, rr, {"three_cells_erd": {"what_id": k[0], "site_id": k[1], "technique_id": k[2], "what_label": label0}, "still_same_now": still, "anchors": descs, "conflict_key": key}))
    return node("same-three-cells-21", "fold_approve", "같은 세 칸 · 다른 anchor 21 조를 합칠까?(하위 21)", "ERD v2.4 실측(erd-v2.4-tuples.json)에서 (what, site, technique) 가 같은데 anchor 가 달라 갈린 21 조(검토 1-E).",
                [], [], None, "하위 항목마다", {"subitems": subs})


def label_of_core(g, a):
    if a in g.cat_info:
        return g.cat_info[a]["name"]
    return g.ref_info[a][0]["label"]


def _item_raw(g, rec):
    r = [int(x) for x in rec.split("/")]
    tx = g.L["taxonomy.json"]["modality"]
    return tx[r[0]]["subcategories"][r[1]]["items"][r[2]]


def item_slash(g):
    P = g.ctx["proc"]
    rows = OrderedDict()
    for slot, rr in list(P["ref_rows"].items()) + [("market-pricing.items[].name", P["mk_rows"])]:
        for r in rr:
            if "/" in str(r["label"]) and (r["result"] == "combo_ref" or r.get("unresolved_reason") in ("multi_site", "combo_outside_fragment")):
                rows.setdefault(r["ref_id"], r)
    subs = []
    skipped = []
    for slot, rr in list(P["ref_rows"].items()) + [("market-pricing.items[].name", P["mk_rows"])]:
        for r in rr:
            if "/" in str(r["label"]) and r["ref_id"] not in rows and r["result"] not in ("tuple",):
                skipped.append(f"{r['label']} — {r.get('unresolved_reason')} {r.get('unregistered')}")
    for i, (rid, r) in enumerate(rows.items(), 1):
        members = r.get("member_anchors") or []
        locs = dedupe(x for m in members for x in g.AM.spec[m]["occ"]) if members else g.anchor_locs(rid)
        if not locs:
            locs = list(g.unres.get(rid, []))
        groups = r.get("groups") or []
        opts = []
        if r["result"] == "combo_ref":
            mem = [g.AM.spec[m] for m in members]
            fams = {m["family"] for m in mem}
            opts.append(opt("together", "「함께」 — 지금대로 조합", "결정 없음 — package(kind=combo_ref) 멤버 " + " + ".join(str(m["what_label"]) for m in mem) + " 를 함께 쓰는 조합", None))
            if len(fams) == 1 and list(fams)[0] in g.ids.mod:
                mo = g.ids.mod[list(fams)[0]]
                opts.append(opt("or_parent", f"「또는」 — 공통 계열 {mo['label']} 하나로", f"tuple_assign 으로 참조를 계열 {mo['label']}({mo['id']}) 튜플 하나로 — 조합 package 가 없어진다",
                                payload(f"{BATCH}-SLS-{i:02d}", "tuple_assign", {"ref_id": rid}, {"what_kind": "modality", "what_id": mo["id"], "site_id": "none", "technique_id": "none"}, f"결정 묶음 2B — 「{r['label']}」의 `/` 는 「또는」 — 공통 계열로 읽는다", locs)))
            opts.append(opt("or_record", "「또는」 — 기록만(ERD 규칙 개정 사유)", "scope_review 기록 — 빌드 값은 바뀌지 않는다(조합 규칙 `/` 는 ERD 규칙이라 v3 에서 고친다)",
                            payload(f"{BATCH}-SLS-{i:02d}", "scope_review", {"erd_ref": f"§1.4 조합 규칙 `/` · {rid}", "review_item": "§12 `/`"}, {"disposition": f"「{r['label']}」의 `/` 는 「또는」"}, f"결정 묶음 2B — 「{r['label']}」의 `/` 해석 기록", locs)))
            now = "combo_ref " + " + ".join(str(m["what_label"]) for m in mem)
        else:
            spans = [s for gg in groups for m in gg["members"] for s in m["spans"]]
            prims = [s for s in spans if s[0] in ("product", "modality_subcategory", "modality", "procedure")]
            sites = [s[1] for s in spans if s[0] == "site"]
            now = f"미해결 ⑨ ({r.get('unresolved_reason')})"
            if r["unresolved_reason"] == "multi_site" and len(prims) == 1:
                w = _what_of(g, prims[0], r["hint"])
                if w:
                    tup = [{"what_kind": w[0], "what_id": w[1]["id"], "site_id": g.ids.site[norm(sname)]["id"], "technique_id": "none"} for sname in sites]
                    opts.append(opt("per_site", "부위마다 튜플(" + " · ".join(f"{w[1]['label']}×{sname}" for sname in sites) + ")",
                                    "tuple_assign_multi — 참조 자리라 package(combo_ref)로 멤버마다 R12. ⚠ 현재 빌더는 미해결 참조 anchor 에 ③ 을 적용하지 못한다(AM.spec 에 없음 · rejected) — 빌더 보강 필요",
                                    payload(f"{BATCH}-SLS-{i:02d}", "tuple_assign_multi", {"ref_id": rid}, {"tuples": tup}, f"결정 묶음 2B — 「{r['label']}」 = 부위마다 튜플", locs)))
            if r["unresolved_reason"] == "combo_outside_fragment":
                outer = [s for s in prims if s[0] == "modality_subcategory"]
                inner = [s for s in prims if s[0] == "product"]
                if outer:
                    w = _what_of(g, outer[0], r["hint"])
                    if w:
                        opts.append(opt("outer_only", f"「또는」 — 바깥 {w[1]['label']} 하나(괄호 안 제품은 예시)", "tuple_assign — ⚠ 현재 빌더는 미해결 참조 anchor 에 ③ 을 적용하지 못한다(빌더 보강 필요)",
                                        payload(f"{BATCH}-SLS-{i:02d}", "tuple_assign", {"ref_id": rid}, {"what_kind": w[0], "what_id": w[1]["id"], "site_id": "none", "technique_id": "none"}, f"결정 묶음 2B — 「{r['label']}」 = {w[1]['label']}", locs)))
                if len(inner) >= 2:
                    ws = [_what_of(g, s, r["hint"]) for s in inner]
                    if all(ws):
                        opts.append(opt("inner_each", "괄호 안 제품마다 튜플(" + " · ".join(w[1]["label"] for w in ws) + ")", "tuple_assign_multi — package(combo_ref) · ⚠ 현재 빌더는 미해결 참조 anchor 에 ③ 을 적용하지 못한다(빌더 보강 필요)",
                                        payload(f"{BATCH}-SLS-{i:02d}", "tuple_assign_multi", {"ref_id": rid}, {"tuples": [{"what_kind": w[0], "what_id": w[1]["id"], "site_id": "none", "technique_id": "none"} for w in ws]}, f"결정 묶음 2B — 「{r['label']}」 = 괄호 안 제품마다", locs)))
            opts.append(opt("keep", "지금대로 미해결", "결정 없음 — ⑨ open 유지", None))
        subs.append(node(f"slash-together-or/{i:02d}", "tuple_assign|tuple_assign_multi|scope_review", f"「{r['label']}」의 `/` 는 「함께」인가 「또는」인가?",
                         "분해 규칙은 조합 기호 `/` 를 `+` 와 같이 「함께」(조합)로 읽는다. 원장 문장이 대안(또는)을 뜻하는지는 문맥 판단이라 기계가 정하지 않는다.",
                         g.evs(locs), opts, None, "원장이 `/` 의 뜻을 따로 적지 않았다(추천 없음).", {"ref_id": rid, "hint": r["hint"], "now": now}))
    return node("slash-together-or", "tuple_assign_multi|scope_review", f"조합 기호 `/` — 「함께」/「또는」(하위 {len(subs)})",
                "`/` 로 나뉜 멤버가 전부 사전 값이라 `/` 의 해석만 남은 참조 자리 전부(combo_ref · multi_site · combo_outside_fragment). 미등록 조각이 같이 있는 자리는 `/` 만으로 풀리지 않아 뺐다.",
                [], [], None, "하위 항목마다", {"subitems": subs, "not_included": dedupe(skipped)})


def _what_of(g, span, hint):
    k, c = span
    if k == "product":
        e = g.ids.prod.get(norm(c))
        return ("product", e) if e else None
    if k == "modality":
        if norm(c) in g.ids.prod:  # §1.4 what 규칙 6 — 계열·제품 양쪽이면 product
            return ("product", g.ids.prod[norm(c)])
        for code, m in g.ids.mod.items():
            if norm(m["label"]) == norm(c):
                return ("modality", m)
        return None
    if k == "modality_subcategory":
        for (fam, lab), es in g.ids.sub_by_label.items():
            if lab == norm(c) and (hint is None or fam == hint):
                return ("modality_subcategory", es[0])
        for (fam, lab), es in g.ids.sub_by_label.items():
            if lab == norm(c):
                return ("modality_subcategory", es[0])
    return None


def item_technique(g):
    erd_dir = os.path.dirname(os.path.abspath(g.ctx["args"].erd))
    cands = json.load(open(os.path.join(erd_dir, "erd-v2.4-tuples.json"), encoding="utf-8"))["procedure"]["inheritance_candidates"]
    prof = g.L["procedure-profiles.json"]["profiles"]
    subs = []
    for i, c in enumerate(cands, 1):
        fam = c["from_ref"].split(":")[1]
        pi = next(j for j, p in enumerate(prof) if p["id"] == fam)
        mlocs = [f"procedure-profiles.json:profiles[].mechanism[]@{pi}/{k}" for k in range(len(prof[pi]["mechanism"]))]
        tid = mkid("TEC", c["to_technique"])
        scope = c["scope"]
        now_none = [a for a in scope if a in g.AM.spec and g.AM.spec[a]["technique_id"] == "none"]
        name_locs = [g.item_by_cat[a][2]["name_loc"] for a in scope if a in g.item_by_cat]
        pl = payload(f"{BATCH}-TEC-{i:02d}", "canonical_mapping", {"from_ref": c["from_ref"], "scope": scope}, {"to_id": tid},
                     f"결정 묶음 2B — 계열 {fam} 기법 「{c['to_technique']}」을 분류 항목 {len(scope)} 튜플에 붙인다(§9.5.6)", mlocs + name_locs)
        subs.append(node(f"technique-inheritance-9/{fam}", "canonical_mapping", f"계열 {fam} 의 기법 「{c['to_technique']}」을 그 계열 분류 항목 {len(scope)} 개 튜플에 붙일까?",
                         "procedure-profiles 의 계열 mechanism 이 하나뿐인 계열이다(R5). v2.2 부터 계열 값을 항목 튜플에 자동 상속하지 않는다 — 항목마다의 기법은 원장에 따로 없어 붙이는 것은 사람 결정이다.",
                         g.evs(mlocs, f"계열 {fam} mechanism") + g.evs(name_locs, "scope 분류 항목 이름"),
                         [opt("apply", f"붙인다 → technique {c['to_technique']}", f"scope {len(scope)} 항목 중 지금 technique=none 인 {len(now_none)} 튜플의 technique 칸이 {tid} 로 — 세 칸 중 둘이 사전 값이 되고 튜플 id 가 바뀐다(site 미상이면 여전히 anchor)", pl),
                          opt("keep", "지금대로 none", "결정 없음", None)],
                         None, "계열 단위 mechanism 만 있고 항목 단위 원장 근거가 없다(추천 없음).", {"from_ref": c["from_ref"], "to_technique": c["to_technique"], "to_id": tid, "scope_items": c["items"]}))
    return node("technique-inheritance-9", "canonical_mapping", "계열 기법 상속 후보 9 계열(하위 9)", "§9.5.6 — R5 계열 기법이 하나인 계열. scope = 그 계열 분류 항목 CAT- 목록(erd-v2.4-tuples.json inheritance_candidates).",
                [], [], None, "하위 항목마다", {"subitems": subs})


def item_two_event(g):
    A = g.ctx["adv"]
    rows = {r["locator"]: r for r in A["expr_rows"]}
    subs = []
    i = 0
    for lc, x in g.AU.expr_link.items():
        if x["match_status"] != "exact" or len(x["unit_ids"]) < 2:
            continue
        evs = [g.AU.units[u]["event"] for u in x["unit_ids"]]
        if len(set(evs)) == len(evs):
            continue
        i += 1
        text = rows[lc]["text"]
        trip = [g.unit_triplet(u) for u in x["unit_ids"]]
        opts = []
        for j, (t, lab) in enumerate(trip):
            opts.append(opt(f"only_{j + 1}", f"{lab} 하나", f"이 표현의 R29 가 {lab} 하나에만 붙는다",
                            payload(f"{BATCH}-TEV-{i:02d}", "adverse_tuple_assign", {"locator": lc, "kind": "expression"}, {"tuples": [t]}, f"결정 묶음 2B — 표현 「{text}」 → {lab}", [lc])))
        opts.append(opt("keep", "지금대로 둘 다(" + " + ".join(t[1] for t in trip) + ")", "결정 없음", None))
        paren = re.search(r"\(([^)]*)\)", text)
        recm, rr = None, "괄호가 아니라 「및」으로 이어진 다른 멤버다 — 「주입 부위」가 「불편감」에도 걸리는지 원장이 말하지 않는다."
        if paren:
            inner = paren.group(1).strip()
            ev_in = g.ids.event_surface.get(norm(inner))
            outer_ev = {g.AU.units[u]["event"] for u in x["unit_ids"]}
            spec = [k for k, (t, lab) in enumerate(trip) if not (lab.endswith("none, 미상)"))]
            if ev_in and ev_in in outer_ev and len(spec) == 1:
                recm = f"only_{spec[0] + 1}"
                rr = f"괄호 안 「{inner}」은 사건 사전에서 바깥 사건 「{ev_in}」의 동의어(complications 이름 출처)라 괄호가 새 사건을 더하지 않는다 — 원문은 사건 하나({trip[spec[0]][1]})다."
        subs.append(node(f"two-event-candidates-10/{i:02d}", "adverse_tuple_assign", f"표현 「{text}」을 단위 하나로 볼까?",
                         "exact 표현인데 같은 사건의 후보가 둘이라 R29 가 단위 둘에 붙는다(괄호·「및」 뒤는 다른 멤버라 수식어를 받지 못한다). 원문이 사건 하나인지는 기계가 정하지 않는다.",
                         g.evs([lc]), opts, recm, rr, {"now": [t[1] for t in trip]}))
    return node("two-event-candidates-10", "adverse_tuple_assign", f"같은 사건 후보가 둘인 exact 표현 {i}(하위 {i})", "검토 v2.4 ②-2 — exact 651 중 같은 사건 후보 둘.", [], [], None, "하위 항목마다", {"subitems": subs})


def item_volnewmer(g):
    anchors = ["CAT-8e550f4613", "CAT-102bed4c6f"]
    locs = [g.item_by_cat[a][2]["name_loc"] for a in anchors]
    key = g.dup_key(locs)
    issue = "taxonomy.json:modality[].subcategories[].items[].classification_issue@" + locs[0].rsplit("@", 1)[1]
    dets = ["taxonomy.json:modality[].subcategories[].items[].detail@" + x.rsplit("@", 1)[1] for x in locs]
    pl_ = [x for x in g.evs(["products.json:energy_device.products[].name@4"])]
    refs = locs + dets + [issue]
    opts = [opt("fold", "같은 것 — M9 쪽으로 합친다(keep CAT-102bed4c6f)", "M4 항목 튜플을 M9 항목 튜플로 합친다(alias · R26·엣지 이동). ⑦ 는 현재 빌더가 fold 로 닫지 않는다",
                payload(f"{BATCH}-VOL-01", "fold_approve", {"anchors": anchors}, {"keep_anchor": "CAT-102bed4c6f"}, "결정 묶음 2B — 볼뉴머 M4/M9 는 같은 장비(원장 classification_issue)", refs)),
            opt("not_same", "다른 것 — 따로 둔다", "⑦ 를 not_same 으로 닫는다", payload(f"{BATCH}-VOL-01", "conflict_close", {"conflict_key": key}, {"verdict": "not_same", "note": "볼뉴머 M4 · M9 항목은 다른 시술"}, "결정 묶음 2B — 볼뉴머 M4/M9 다름", refs)),
            opt("both_valid", "둘 다 맞다 — 둘 다 둔다", "⑦ 를 both_valid 로 닫는다(실버·골드 둘 다)", payload(f"{BATCH}-VOL-01", "conflict_close", {"conflict_key": key}, {"verdict": "both_valid", "note": "볼뉴머 M4 · M9 둘 다 유지"}, "결정 묶음 2B — 볼뉴머 M4/M9 둘 다", refs)),
            opt("keep", "지금대로(⑦ open)", "결정 없음", None)]
    return node("volnewmer-m4-m9", "fold_approve|conflict_close", "분류 항목 「볼뉴머」 M4(스킨부스터)와 M9(기기 리프팅)는 같은 것인가?",
                "같은 이름이 두 계열 트리에 있다. CAT- 는 트리 위치로 고정이라 둘은 다른 anchor 이고, 같은 제품 what 으로 풀렸지만 site·technique 미상이라 접히지 않는다. ⑦ duplicate_candidate 로 올라 있다.",
                g.evs(locs, "분류 항목 이름") + g.evs(dets, "detail") + g.evs([issue], "원장 메모(classification_issue)") + pl_,
                opts, "fold", "원장 M4 항목에 classification_issue 「이 엔트리는 M4(스킨부스터) 섹션에 잘못 등재됨 — … 카테고리를 M9-2(RF)로 통합 관리 필요」가 적혀 있다 — M9 항목으로 합친다.",
                {"anchors": [g.anchor_desc(a) for a in anchors], "conflict_key": key, "related": ["same-three-cells-21 의 볼뉴머 조와 같은 대상 — 한쪽만 고른다"]})


ITEMS = [("botox-product-vs-modality", item_botox), ("event-split", item_event_split), ("excel-v-plus", item_excel), ("injection-site-erythema-edema", item_injection_site),
         ("mface-like", item_mface), ("paren-synonym-unknown-tuples-4", item_paren), ("same-three-cells-21", item_same_three), ("slash-together-or", item_slash),
         ("technique-inheritance-9", item_technique), ("two-event-candidates-10", item_two_event), ("volnewmer-m4-m9", item_volnewmer)]


def leaves_of(items):
    for it in items:
        if it.get("subitems"):
            for s in it["subitems"]:
                yield it, s
        else:
            yield it, it


def build_gate_2b(S, out_dir):
    g = G(S, S.ctx["args"].decisions)
    items = []
    for tid, fn in ITEMS:
        it = fn(g)
        it["template"] = f"decisions/proposed/templates/{tid}.json"
        items.append(it)
    # 검증 · 이미 승인된 같은 결정 표시
    for it, s in leaves_of(items):
        for o in s["options"]:
            p = o["decision_payload"]
            if p:
                errs = [e for e in validate(dict(p, decided_by="x")) if "decided_by" not in e]
                if errs:
                    raise AssertionError(f"{s['id']} {o['key']}: {errs}")
        s["already_decided"] = dedupe(x for o in s["options"] for x in g.already(o["decision_payload"]))
        for o in s["options"]:
            p = o["decision_payload"]
            if p and p["kind"] in ("tuple_assign", "tuple_assign_multi"):
                a = p["target"].get("ref_id") or p["target"].get("catalog_item_id")
                ok = a in g.AM.spec and not g.AM.spec[a].get("virtual")
                o["builder_applies_now"] = ok
                if not ok and "빌더 보강" not in o["effect"]:
                    o["effect"] += " · ⚠ 현재 빌더는 이 anchor(미해결·조합 참조)에 ③ 을 적용하지 못한다(apply_log rejected) — 빌더 보강 필요"
        if s["recommended"] is not None and s["recommended"] not in [o["key"] for o in s["options"]]:
            raise AssertionError(f"{s['id']} recommended {s['recommended']} 없음")
    os.makedirs(os.path.join(out_dir, "gate"), exist_ok=True)
    write_json(os.path.join(out_dir, "gate", "batch2b.json"), items)
    write_text(os.path.join(out_dir, "gate", "batch2b.md"), render_md(items))
    n_leaf = sum(1 for _ in leaves_of(items))
    rec = sum(1 for _, s in leaves_of(items) if s["recommended"] is not None)
    return {"items": len(items), "leaves": n_leaf, "subitems": sum(len(i.get("subitems") or []) for i in items), "recommended": rec, "not_recommended": n_leaf - rec}


def render_md(items):
    leaves = list(leaves_of(items))
    rec = sum(1 for _, s in leaves if s["recommended"] is not None)
    o = ["# 결정 묶음 2B — 게이트 자료(사용자가 직접 정할 11 항목)", "",
         f"상위 {len(items)} · 고를 자리(하위 항목 · 하위 없는 항목) {len(leaves)} · 추천 있음 {rec} · 추천 없음 {len(leaves) - rec}.",
         "원문은 브론즈 원장에서 locator 로 직접 읽었다. 추천은 원장 근거가 있을 때만 — 없으면 「—」. 고른 결과는 `python3 apply_gate.py --answers answers.json` 으로 결정 파일이 된다(answers = {항목 id 또는 하위 id: 옵션 key}).", "",
         md_table(["자리", "질문", "추천"], [(s["id"], s["title"], s["recommended"] or "—") for _, s in leaves]), ""]
    for it in items:
        o += [f"## {it['id']} — {it['title']}", "", it["why"], ""]
        for s in (it.get("subitems") or [it]):
            if s is not it:
                o += [f"### {s['id']} — {s['title']}", "", s["why"], ""]
            o.append("**원장 원문**")
            o.append("")
            ev = s["evidence"]
            for e in ev[:12]:
                txt = str(e["text"]).replace("\n", " ")
                o.append(f"- `{e['locator']}` — 「{txt[:160]}」" + (f" ({e['note']})" if e.get("note") else ""))
            if len(ev) > 12:
                o.append(f"- … 외 {len(ev) - 12} 곳(batch2b.json evidence 전부)")
            o.append("")
            o.append(md_table(["옵션", "뜻", "적용되면", "결정"], [(f"**{x['key']}**" if x["key"] == s["recommended"] else x["key"], x["label"], x["effect"],
                                                                   (f"{x['decision_payload']['kind']} `{x['decision_payload']['id']}`" if x["decision_payload"] else "결정 없음")) for x in s["options"]]))
            o.append("")
            o.append(f"추천: **{s['recommended'] or '—'}** — {s['recommend_reason']}")
            if s.get("already_decided"):
                o.append(f"이미 승인된 같은 결정: {', '.join(s['already_decided'])}")
            o.append("")
        if it.get("not_included"):
            o += ["`/` 가 있지만 뺀 자리(미등록 조각이 함께 있어 `/` 만으로 풀리지 않음):", ""] + [f"- {x}" for x in it["not_included"]] + [""]
    return "\n".join(o)
