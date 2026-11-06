# -*- coding: utf-8 -*-
"""결정 — 저장소(파일 하나 = 레코드 하나) 읽기 · 검증 · 적용 순서 ⓪①~⑦ (ERD v3.1 §5.2 kind 20 · §5.4).

v3: ① canonical_rename(V3-6 · 코드 기반 개체 id 유지 · 사전 항목 id 재계산 · 옛 id 는 renamed_from) ·
③ tuple_assign(_multi)/adverse_tuple_assign 는 미해결·조합·부위별 anchor(REF- · #m<i> · #s<i>)에도 — 결정이 그 자리를 세운다(V3-9) ·
④ fold_approve 는 접는 anchor 쌍의 ⑦ 을 닫는다(V3-10 · conflicts.close_duplicates_by_fold) · ② canonical_mapping R5:<하위분류 id>(V3-8).
v3.1: ⓪ product_reclassify(V3.1-1 · product_name 사전 code 교체 → PRD- 재계산 · 옛 id 는 reclassified_from) ·
① 안 kind 순서 dictionary_add → canonical_rename → dictionary_remove(V3.1-3 · 동의어/값 제거 · 쓰는 레코드 있으면 거부 · 이력) → phrase_map(V3.1-10 · 문구 사전 지도) ·
③ adverse_tuple_assign = raw_name 단위만 · 세 칸(event_id, site_id, qualifier_id) + courses(R15 엣지 경과) — 옛 네 칸(course_id)은 경과를 courses 로 옮겨 적용 ·
옛 kind=expression(표현 locator)은 그 자리의 문구 사전 항목 지도로 적용(phrase_map 과 같은 효과 · 적용 로그 note) ·
⑤ edge_create: adverse_tuple 세 칸(옛 course 는 attrs.course) · dict_value person_condition(조건 단위) · locator 가 제품 note 문장이면 clinical_rule(product_note) 레코드를 세운다(R32).

빌드는 status=approved 만 적용한다(proposed·rejected 는 목록만). build_reads=true kind 만 실버 값을 바꾸고
나머지(ledger_correction_note · verification_hold · conflict_resolution · scope_review)는 기록만(적용 로그에 recorded).
target 이 파생 id(PRC-/ADV-/CFL-)를 쓰는 결정은 거부한다(§1.1 결정 target).
"""
import copy
import json
import os
import re
from collections import OrderedDict, defaultdict

from .provenance import P, loc, records, rec_str
from .decompose import is_scoped_label_mapping
from .util import mkid, norm, dedupe

STAGE = OrderedDict([("reclassification", "⓪"), ("product_reclassify", "⓪"), ("dictionary_add", "①"), ("canonical_rename", "①"), ("dictionary_remove", "①"), ("phrase_map", "①"), ("canonical_mapping", "②"), ("tuple_assign", "③"), ("tuple_assign_multi", "③"), ("adverse_tuple_assign", "③"),
                     ("fold_approve", "④"), ("event_split", "④"), ("edge_create", "⑤"), ("conflict_override", "⑥"), ("conflict_close", "⑥"), ("exclude", "⑦")])
STAGE_ORDER = ["⓪", "①", "②", "③", "④", "⑤", "⑥", "⑦"]
KIND_ORDER = {"dictionary_add": 0, "canonical_rename": 1, "dictionary_remove": 2, "phrase_map": 3}  # v3.1 ① 안 kind 순서(ERD decision_apply_order_rule)
RECORD_ONLY = {"ledger_correction_note", "verification_hold", "conflict_resolution", "scope_review"}
DERIVED_ID = re.compile(r"\b(PRC|ADV|CFL)-[0-9a-f]{10}\b")
KINDS = set(STAGE) | RECORD_ONLY


def load_store(path):
    """decisions/ 아래 *.json 전부(하위 폴더 포함 · 파일 이름 순). 반환 [(파일 상대경로, 레코드)]."""
    out = []
    for root, dirs, files in os.walk(path):
        dirs.sort()
        for f in sorted(files):
            if f.endswith(".json") and not f.startswith("_"):
                p = os.path.join(root, f)
                with open(p, encoding="utf-8") as fh:
                    rec = json.load(fh)
                if isinstance(rec, dict) and "kind" in rec and "status" in rec:
                    out.append((os.path.relpath(p, path), rec))
    return out


def validate(rec):
    errs = []
    for k in ("id", "kind", "target", "new_value", "reason", "decided_by", "decided_at", "status", "source_refs"):
        if k not in rec:
            errs.append(f"필드 없음 {k}")
    if rec.get("kind") not in KINDS:
        errs.append(f"모르는 kind {rec.get('kind')}")
    if rec.get("status") not in ("proposed", "approved", "rejected"):
        errs.append(f"status {rec.get('status')}")
    m = DERIVED_ID.search(json.dumps(rec.get("target"), ensure_ascii=False))
    if m:
        errs.append(f"target 이 파생 id {m.group(0)} 를 쓴다(§1.1 금지)")
    if rec.get("status") == "approved" and not rec.get("decided_by"):
        errs.append("approved 인데 decided_by 없음")
    return errs


def ordered(decisions):
    """적용 순서 — 단계 ⓪①~⑦ · ① 안은 kind 순서(dictionary_add → canonical_rename → dictionary_remove → phrase_map) · 같은 단계(·kind)는 decided_at 순(같으면 id 순)."""
    def key(d):
        st = STAGE.get(d["kind"], "—")
        return (STAGE_ORDER.index(st) if st in STAGE_ORDER else 99, KIND_ORDER.get(d["kind"], 0) if st == "①" else 0, d.get("decided_at") or "", d["id"])
    return sorted(decisions, key=key)


# ---------------------------------------------------------------------------
# 원장 메모 → 결정(질문 23) — 원장 작성자 결정, approved, decided_at=null
# ---------------------------------------------------------------------------
def ledger_memo_decisions(L, resolver, ids):
    out = []
    n = 0
    tx = L["taxonomy.json"]
    for r, m in records(tx, "modality[]"):
        for si, sc in enumerate(m["subcategories"]):
            for ii, it in enumerate(sc["items"]):
                rr = r + (si, ii)
                cat = mkid("CAT", f"{m['id']}|{it['name']}")
                base = {"decided_by": "원장 작성자(taxonomy.json)", "decided_at": None, "status": "approved"}
                for key, kind in (("verification_needed", "verification_hold"), ("classification_issue", "ledger_correction_note"), ("correction_note", "ledger_correction_note"),
                                  ("reclassified_to", "reclassification"), ("canonical_category", "canonical_mapping")):
                    if key not in it:
                        continue
                    pv = P("taxonomy.json", f"modality[].subcategories[].items[].{key}", rr)
                    n += 1
                    d = dict(base, id=f"DEC-2026-10-26-{n:02d}", kind=kind, source_refs=[{"kind": "ledger", "ref": loc(pv)}], provenance=[pv])
                    if kind == "verification_hold":
                        d.update(target={"catalog_item_id": cat}, new_value={"hold": True}, reason=it[key])
                    elif kind == "ledger_correction_note":
                        d.update(target={"catalog_item_id": cat}, new_value={"note": it[key]}, reason=it[key])
                    elif kind == "reclassification":
                        if it[key] not in ids.mod:
                            d.update(status="rejected", target={"catalog_item_id": cat}, new_value={"modality_id": None}, reason=f"reclassified_to 「{it[key]}」 이 계열 코드가 아니다")
                        else:
                            d.update(target={"catalog_item_id": cat}, new_value={"modality_id": ids.mod[it[key]]["id"]}, reason=f"원장 reclassified_to={it[key]}" + (f" · {it.get('classification_issue')}" if it.get("classification_issue") else ""))
                    elif kind == "canonical_mapping":
                        lab = it[key].split(">")[-1].strip()
                        code = it[key].split()[0]
                        res = resolver.resolve(lab, code, ("modality_subcategory",))
                        sub = ids.sub_by_label.get((code, norm(res.get("canonical")))) if res["status"] == "resolved" else None
                        if sub:
                            d.update(target={"from_ref": cat, "scope": [cat]}, new_value={"to_id": sub[0]["id"]}, reason=f"원장 canonical_category 「{it[key]}」 → 하위분류 사전 일치 {sub[0]['label']}")
                        else:
                            d.update(status="rejected", target={"from_ref": cat, "scope": [cat]}, new_value={"to_id": None},
                                     reason=f"원장 canonical_category 「{it[key]}」 — 하위분류 사전 일치 없음(질문 23: 하위분류 사전 일치만 자동) → 적재하지 않고 ⑨", unresolved_label=lab, unresolved_code=code)
                    if d["status"] == "rejected" and kind == "canonical_mapping":
                        d["_not_loaded"] = True  # 하위분류 사전 일치 없음 — 결정으로 적재하지 않고 ⑨ 로만(질문 23)
                    out.append(d)
    return out


# ---------------------------------------------------------------------------
# 사전 단계 — ① dictionary_add · ④ event_split (사전을 바꾸고 분해를 다시 돌린다)
# ---------------------------------------------------------------------------
def apply_dictionary(dic, decisions, log, in_use=None):
    """⓪ product_reclassify · ① dictionary_add → canonical_rename → dictionary_remove(kind 순서 · decisions 는 ordered()) · ④ event_split — 사전을 바꾼다.
    in_use(사전 이름, 항목, 지금 사전 JSON) → 그 값을 쓰는 레코드 예(빈 목록이면 안 씀) — dictionary_remove 값 제거의 거부 판정."""
    d2 = copy.deepcopy(dic)
    D = {x["name"]: x for x in d2["dictionaries"]}
    v33 = d2.get("erd_version") == "v3.3"   # V3.3-E: dictionary_add·event_split 의 new_value category 는 읽지 않는다(사전 키 없음)
    for dec in decisions:
        if dec["kind"] == "product_reclassify":
            apply_product_reclassify(D, dec, log)
            continue
        if dec["kind"] == "canonical_rename":
            apply_rename(D, dec, log)
            continue
        if dec["kind"] == "dictionary_remove":
            apply_remove(D, d2, dec, log, in_use)
            continue
        if dec["kind"] == "dictionary_add":
            name = dec["target"].get("dictionary")
            nv = dec["new_value"]
            if name not in D:
                log.append({"id": dec["id"], "kind": dec["kind"], "stage": "①", "result": "rejected", "why": f"사전 {name} 없음"})
                continue
            if D[name].get("kind") == "phrase_index":
                log.append({"id": dec["id"], "kind": dec["kind"], "stage": "①", "result": "rejected", "why": "문구 사전(phrase_dictionary)은 dictionary_add 가 아니라 phrase_map 으로(§5.2)"})
                continue
            entries = D[name]["entries"]
            src = [{"kind": "decision", "decision_id": dec["id"], "source_refs": dec.get("source_refs", [])}]
            e = next((x for x in entries if norm(x["canonical"]) == norm(nv["canonical"])), None)
            added = []
            if e is None:
                e = {"id": mkid("DIC", f"{name}|{nv['canonical']}"), "canonical": nv["canonical"], "sources": src, "synonyms": [], "definition": None}
                if nv.get("category") is not None and not v33:
                    e["category"] = nv["category"]
                if "code" in nv:
                    e["code"] = nv["code"]
                if name == "product_name" and nv.get("origin") == "taxonomy":
                    # v3.2(V3.2-5) 장비 제품(taxonomy 항목 이름)에 동의어를 다는 결정 — 값은 장비 자동 등록이 세우는 항목과 같은 것(분해가 그 항목에 출처를 합친다)
                    e.update(origin="taxonomy", status="unreviewed", license_status="미확인", kind_note="장비(V3.2-5)")
                if name == "site":
                    e["site_kind"] = nv.get("site_kind", "taxonomy_site_label")
                    e["members"] = None
                    if nv.get("kind"):
                        e["kind"] = nv["kind"]  # V3-5 부위 kind(anatomical|layer|region)
                    if "parent" in nv:
                        e["parent"] = nv["parent"]  # v3.2(V3.2-4) 부위 계층 — 씨앗 승인(정준값 · 개체 id 는 빌드가 site 사전으로 푼다)
                if name == "person_condition" and nv.get("kind"):
                    e["kinds"] = [nv["kind"]]   # v3.1(V3.1-4) 조건 사전 kind(condition|check|age_group)
                    e["kind"] = nv["kind"]
                entries.append(e)
                added.append(nv["canonical"])
            updated = []
            if v33 and name == "site" and e is not None and not added:
                # v3.3: 값이 이미 있는데(앞선 결정이 동의어로 세운 「얼굴 전체」) kind·parent 가 비어 있으면 승인 씨앗의 kind·parent 를 준다(V3.2-4 계층 · 값 변경 아님)
                for k in ("kind", "parent"):
                    if nv.get(k) is not None and e.get(k) is None:
                        e[k] = nv[k]
                        updated.append(k)
                if updated:
                    e.setdefault("sources", []).extend(src)
            taken = {norm(v) for x in entries for v in [x["canonical"]] + [s["value"] for s in x.get("synonyms", [])]}
            for s in nv.get("synonyms", []):
                sv = s["value"] if isinstance(s, dict) else s
                if norm(sv) in taken:
                    continue
                syn = {"value": sv, "link": "decision", "sources": src}
                if isinstance(s, dict) and s.get("is_marketing_name") is not None:
                    syn["is_marketing_name"] = s["is_marketing_name"]
                e["synonyms"].append(syn)
                taken.add(norm(sv))
                added.append(sv)
            log.append({"id": dec["id"], "kind": dec["kind"], "stage": "①", "result": "applied", "dictionary": name, "added": added, **({"updated_fields": updated, "note": "값은 이미 있었다(앞선 결정) — kind·parent 만 채움"} if updated else {})})
    for dec in decisions:
        if dec["kind"] == "event_split":
            E = D["adverse_event_type"]["entries"]
            ev = next((x for x in E if norm(x["canonical"]) == norm(dec["target"].get("event"))), None)
            if ev is None:
                log.append({"id": dec["id"], "kind": dec["kind"], "stage": "④", "result": "rejected", "why": "사건 사전 값 없음"})
                continue
            moved = []
            for ne in dec["new_value"].get("new_events", []):
                syn = [s for s in ne.get("synonyms", [])]
                ev["synonyms"] = [s for s in ev["synonyms"] if norm(s["value"]) not in {norm(x) for x in syn + [ne["canonical"]]}]
                E.append({"id": mkid("DIC", f"adverse_event_type|{ne['canonical']}"), "canonical": ne["canonical"], **({} if v33 else {"category": ne.get("category") or ev.get("category")}),
                          "sources": [{"kind": "decision", "decision_id": dec["id"]}], "synonyms": [{"value": s, "link": "decision", "sources": [{"kind": "decision", "decision_id": dec["id"]}]} for s in syn], "definition": None})
                moved.append(ne["canonical"])
            log.append({"id": dec["id"], "kind": dec["kind"], "stage": "④", "result": "applied", "new_events": moved, "note": "사건 사전을 나누고 부작용 분해를 다시 돌렸다(③ 지정은 다시 적용)"})
    for x in d2["dictionaries"]:
        x["canonical_count"] = len(x["entries"])
        x["synonym_count"] = sum(len(e.get("synonyms", [])) for e in x["entries"])
    return d2


def _find_entry(entries, canonical, code=None):
    return next((x for x in entries if norm(x["canonical"]) == norm(canonical) and (code is None or str(x.get("code")) == str(code))), None)


def apply_product_reclassify(D, dec, log):
    """⓪ product_reclassify(V3.1-1) — product_name 사전 항목의 계열 code 를 새 계열로. PRD-<sha(계열|제품명)> 이 재계산되고 옛 id 는 reclassified_from(alias).
    새 (계열|제품명) 의 항목이 이미 있으면 그 항목으로 합친다(동의어·출처 합침 · 옛 id alias)."""
    t, nv = dec["target"], dec["new_value"]
    entries = D["product_name"]["entries"]
    to = nv.get("to_modality_code")
    mods = {str(e.get("code")) for e in D["modality"]["entries"]}
    e = None
    if t.get("product_id"):
        e = next((x for x in entries if mkid("PRD", f"{x.get('code')}|{x['canonical']}") == t["product_id"] or t["product_id"] in [r["id"] for r in x.get("reclassified_from", [])]), None)
    elif isinstance(t.get("product"), dict) and t["product"].get("dictionary", "product_name") == "product_name":
        e = _find_entry(entries, t["product"].get("canonical"))
    if e is None:
        log.append({"id": dec["id"], "kind": dec["kind"], "stage": "⓪", "result": "rejected", "why": "대상 제품(PRD- 또는 product_name 정준값)이 사전에 없다"})
        return
    if to not in mods:
        log.append({"id": dec["id"], "kind": dec["kind"], "stage": "⓪", "result": "rejected", "why": f"to_modality_code {to} 가 계열 사전 code 가 아니다"})
        return
    old_code = e.get("code")
    old_id = mkid("PRD", f"{old_code}|{e['canonical']}")
    new_id = mkid("PRD", f"{to}|{e['canonical']}")
    if str(old_code) == str(to):
        log.append({"id": dec["id"], "kind": dec["kind"], "stage": "⓪", "result": "no_target", "why": "이미 그 계열"})
        return
    rec = {"id": old_id, "code": old_code, "decision_id": dec["id"]}
    other = next((x for x in entries if x is not e and norm(x["canonical"]) == norm(e["canonical"]) and str(x.get("code")) == str(to)), None)
    if other is not None:
        taken = {norm(v) for v in [other["canonical"]] + [s_["value"] for s_ in other.get("synonyms", [])]}
        for s_ in e.get("synonyms", []):
            if norm(s_["value"]) not in taken:
                other["synonyms"].append(s_)
        other["sources"] = list(other.get("sources", [])) + [x for x in e.get("sources", []) if x not in other.get("sources", [])]
        other.setdefault("reclassified_from", []).append(dict(rec, merged=True))
        entries.remove(e)
        merged = True
    else:
        e["code"] = to
        e.setdefault("reclassified_from", []).append(rec)
        e["sources"] = list(e.get("sources", [])) + [{"kind": "decision", "decision_id": dec["id"], "source_refs": dec.get("source_refs", [])}]
        merged = False
    log.append({"id": dec["id"], "kind": dec["kind"], "stage": "⓪", "result": "applied", "product": e["canonical"], "from_code": old_code, "to_code": to, "old_id": old_id, "new_id": new_id, "merged": merged})


def apply_remove(D, d2, dec, log, in_use=None):
    """① dictionary_remove(V3.1-3) — 동의어 하나(target.synonym) 또는 값 자체. 값 제거는 쓰는 레코드가 있으면 거부(in_use). 이력은 사전의 removed_synonyms / removed_entries."""
    t = dec["target"]
    name = t.get("dictionary")
    if name not in D:
        log.append({"id": dec["id"], "kind": dec["kind"], "stage": "①", "result": "rejected", "why": f"사전 {name} 없음"})
        return
    entries = D[name]["entries"]
    e = _find_entry(entries, t.get("canonical"), t.get("code"))
    if e is None:   # canonical_rename 뒤 — 옛 정준값(renamed_from)으로도 찾는다(같은 항목 · id alias)
        e = next((x for x in entries if any(norm(r.get("canonical")) == norm(t.get("canonical")) for r in x.get("renamed_from", [])) and (t.get("code") is None or str(x.get("code")) == str(t.get("code")))), None)
    if e is None:
        log.append({"id": dec["id"], "kind": dec["kind"], "stage": "①", "result": "rejected", "why": "대상 정준값이 사전에 없다"})
        return
    syn = t.get("synonym")
    if syn:
        hit = [x for x in e.get("synonyms", []) if norm(x["value"]) == norm(syn)]
        if not hit:
            log.append({"id": dec["id"], "kind": dec["kind"], "stage": "①", "result": "rejected", "why": f"동의어 「{syn}」 가 「{e['canonical']}」 에 없다"})
            return
        e["synonyms"] = [x for x in e["synonyms"] if norm(x["value"]) != norm(syn)]
        D[name].setdefault("removed_synonyms", [])
        if not isinstance(D[name]["removed_synonyms"], list):
            D[name]["removed_synonyms"] = []
        for x in hit:
            D[name]["removed_synonyms"].append({"value": x["value"], "canonical": e["canonical"], "decision_id": dec["id"], "removed_at": dec.get("decided_at"), "link": x.get("link")})
        log.append({"id": dec["id"], "kind": dec["kind"], "stage": "①", "result": "applied", "dictionary": name, "canonical": e["canonical"], "removed_synonym": hit[0]["value"]})
        return
    uses = in_use(name, e, d2) if in_use else ["in_use 판정 불가(빌드가 판정 함수를 주지 않음)"]
    if uses:
        log.append({"id": dec["id"], "kind": dec["kind"], "stage": "①", "result": "rejected", "why": "in_use — 그 값을 쓰는 레코드가 있다(먼저 옮기거나 exclude): " + " · ".join(str(u) for u in uses[:5]), "in_use": len(uses)})
        return
    entries.remove(e)
    D[name].setdefault("removed_entries", [])
    if not isinstance(D[name]["removed_entries"], list):
        D[name]["removed_entries"] = []
    D[name]["removed_entries"].append({"canonical": e["canonical"], "id": e["id"], "decision_id": dec["id"], "removed_at": dec.get("decided_at")})
    log.append({"id": dec["id"], "kind": dec["kind"], "stage": "①", "result": "applied", "dictionary": name, "removed_entry": e["canonical"]})


def apply_rename(D, dec, log):
    """① canonical_rename(V3-6 · R-2) — 정준값 교체. 코드 기반 개체 id(MOD-<code> 등)는 정준값과 무관해 그대로.
    사전 항목 id = DIC-sha256(사전|정준값) 재계산 · 옛 id 는 renamed_from · 옛 정준값은 동의어(link=renamed_from).
    new_value.synonyms(빌더 확장 · dictionary_add 와 같은 모양 · is_marketing_name 표시 가능)는 같은 값에 동의어로 더한다."""
    t, nv = dec["target"], dec["new_value"]
    name = t.get("dictionary")
    if name not in D:
        log.append({"id": dec["id"], "kind": dec["kind"], "stage": "①", "result": "rejected", "why": f"사전 {name} 없음"})
        return
    entries = D[name]["entries"]
    e = next((x for x in entries if norm(x["canonical"]) == norm(t.get("canonical")) and (t.get("code") is None or str(x.get("code")) == str(t.get("code")))), None)
    if e is None:
        log.append({"id": dec["id"], "kind": dec["kind"], "stage": "①", "result": "rejected", "why": "대상 정준값(·코드)이 사전에 없다"})
        return
    new = nv.get("canonical")
    clash = [x for x in entries if x is not e and norm(new) in {norm(v) for v in [x["canonical"]] + [s_["value"] for s_ in x.get("synonyms", [])]}]
    if not new or clash:
        log.append({"id": dec["id"], "kind": dec["kind"], "stage": "①", "result": "rejected", "why": "새 정준값이 다른 값의 정준값·동의어다" if clash else "새 정준값 없음"})
        return
    src = [{"kind": "decision", "decision_id": dec["id"], "source_refs": dec.get("source_refs", [])}]
    old, old_id = e["canonical"], e["id"]
    promoted = [s_ for s_ in e.get("synonyms", []) if norm(s_["value"]) == norm(new)]
    e["synonyms"] = [s_ for s_ in e.get("synonyms", []) if norm(s_["value"]) != norm(new)]
    e["canonical"] = new
    e["id"] = mkid("DIC", f"{name}|{new}")
    e.setdefault("renamed_from", []).append({"id": old_id, "canonical": old, "decision_id": dec["id"], "promoted_synonym": [s_["value"] for s_ in promoted]})
    e["renamed_by"] = dec["id"]
    if nv.get("old_as_synonym", True):
        syn = {"value": old, "link": "renamed_from", "sources": src}
        if nv.get("is_marketing_name") is not None:
            syn["is_marketing_name"] = nv["is_marketing_name"]
        e["synonyms"].append(syn)
    taken = {norm(v) for x in entries for v in [x["canonical"]] + [s_["value"] for s_ in x.get("synonyms", [])]}
    added = []
    for s_ in nv.get("synonyms", []) or []:
        sv = s_["value"] if isinstance(s_, dict) else s_
        if norm(sv) in taken:
            for x in e["synonyms"]:
                if norm(x["value"]) == norm(sv) and isinstance(s_, dict) and s_.get("is_marketing_name") is not None:
                    x["is_marketing_name"] = s_["is_marketing_name"]
            continue
        syn = {"value": sv, "link": "decision", "sources": src}
        if isinstance(s_, dict) and s_.get("is_marketing_name") is not None:
            syn["is_marketing_name"] = s_["is_marketing_name"]
        e["synonyms"].append(syn)
        taken.add(norm(sv))
        added.append(sv)
    log.append({"id": dec["id"], "kind": dec["kind"], "stage": "①", "result": "applied", "dictionary": name, "code": e.get("code"), "renamed": [old, new], "old_id": old_id, "new_id": e["id"], "added": added})


# ---------------------------------------------------------------------------
# 튜플 단계 — ② ③ ④(fold)
# ---------------------------------------------------------------------------
def what_of_id(ctx, wid):
    ids = ctx["ids"]
    for m in ids.mod.values():
        if m["id"] == wid:
            return "modality", m
    for s in ids.sub.values():
        if s["id"] == wid:
            return "modality_subcategory", s
    for p in ids.prod.values():
        if p["id"] == wid:
            return "product", p
    for (fam, name), it in ctx["items"].items():
        if it["cat"]["catalog_item_id"] == wid:
            return "catalog_item", {"id": wid, "label": name, "family": fam}
    return None, None


def site_of_id(ctx, sid):
    if sid in (None, "none"):
        return "none", None
    for s in ctx["ids"].site.values():
        if s["id"] == sid:
            return sid, s["label"]
    return None, None


def tech_of_id(ctx, tid):
    if tid in (None, "none"):
        return "none", None
    for e in ctx["dicts"]["technique"]["entries"]:
        if tid in (e["id"], mkid("TEC", e["canonical"])):
            return e["id"], e["canonical"]
    return None, None


def apply_tuples(ctx, AM, AU, decisions, log):
    for dec in decisions:
        k, t, nv = dec["kind"], dec["target"], dec["new_value"]
        if k == "canonical_mapping" and is_scoped_label_mapping(dec):
            hits = list(ctx["proc"]["PT"].scoped_hits.get(dec["id"], []))
            resolved = []
            for a in hits:
                for sa in [a] + [x for x in AM.spec if x.startswith(a + "#")]:
                    if sa in AM.spec and not AM.spec[sa].get("virtual"):
                        AM.spec[sa]["decision_ids"].append(dec["id"])
                        resolved.append(sa)
            log.append({"id": dec["id"], "kind": k, "stage": "②", "result": "applied" if hits else "no_target", "anchors": hits, "resolved_anchors": resolved,
                        "note": "라벨 조각 from_ref 를 scope anchor 의 분해에서만 to_id 로 읽었다(미해결 참조 · 분해 단계)"})
            continue
        if k == "canonical_mapping":
            scope = t.get("scope") or []
            anchors = list(AM.spec) if scope == ["*"] else [a for a in scope if a in AM.spec]
            fr, to = t.get("from_ref"), nv.get("to_id")
            hit = []
            if fr and fr.startswith("R5:"):
                tid_, tname = tech_of_id(ctx, to)
                key = fr[3:]
                sub = ctx["ids"].sub.get(key)          # V3-8: R5:<하위분류 id> — 그 하위분류 아래 항목(CAT-)·같은 계열 참조만
                for a in anchors:
                    s = AM.spec[a]
                    if s.get("virtual") or s["technique_id"] != "none" or tid_ is None:
                        continue
                    if sub is None and str(s.get("family")) != key:
                        continue
                    if sub is not None:
                        it = ctx["item_by_id_cat"].get(a.split("#", 1)[0])
                        if (it is not None and it["sub"] != key) or (it is None and str(s.get("family")) != sub["family"]):
                            continue
                    s["technique_id"], s["technique"], s["technique_origin"] = tid_, tname, "decision"
                    s["decision_ids"].append(dec["id"])
                    hit.append(a)
                if hit and sub is not None:
                    ctx.setdefault("r5_sub_decisions", []).append({"id": dec["id"], "subcategory": key, "technique_id": tid_, "technique": tname})
            else:
                wk, w = what_of_id(ctx, to)
                for a in anchors:
                    s = AM.spec[a]
                    if s.get("virtual") or w is None:
                        continue
                    if fr == a or (fr.startswith("CAT-") and a == fr) or s["what_id"] == fr or norm(s.get("what_label")) == norm(fr):
                        s["what_kind"], s["what_id"], s["what_label"], s["family"] = wk, w["id"], w["label"], w.get("family")
                        s["decision_ids"].append(dec["id"])
                        hit.append(a)
            log.append({"id": dec["id"], "kind": k, "stage": "②", "result": "applied" if hit else "no_target", "anchors": hit})
        elif k == "tuple_assign":
            a = t.get("catalog_item_id") or t.get("ref_id")
            wk, w = what_of_id(ctx, nv.get("what_id"))
            sid, slab = site_of_id(ctx, nv.get("site_id"))
            tid_, tname = tech_of_id(ctx, nv.get("technique_id"))
            if w is None or sid is None or tid_ is None:
                log.append({"id": dec["id"], "kind": k, "stage": "③", "result": "rejected", "why": "dictionary — 지정 값(what/site/technique)이 사전·실버에 없다"})
                continue
            if sid != "none" and ctx["ids"].site_kind.get(norm(slab)) == "layer":
                log.append({"id": dec["id"], "kind": k, "stage": "③", "result": "rejected", "why": "V3-5 — layer 부위는 시술 site 칸에 넣지 않는다"})
                continue
            est = a not in AM.spec
            if est and AM.establish(a, dec["id"]) is None:
                log.append({"id": dec["id"], "kind": k, "stage": "③", "result": "rejected", "why": "anchor 가 원장 참조·분류 항목이 아니다"})
                continue
            was_multi = a in AM.multi
            s = AM.reassign_base(a, dec["id"]) if was_multi else AM.spec[a]
            s.update(what_kind=wk, what_id=w["id"], what_label=w["label"], family=w.get("family"), site_id=sid, site=slab, technique_id=tid_, technique=tname, technique_origin="decision" if tname else "none", status="complete")
            s["decision_ids"] = s.get("decision_ids", []) + [dec["id"]]
            for kk in ("unregistered_fragments", "candidate_name", "extra_primaries", "extra_sites"):
                s.setdefault(kk, [])
            log.append({"id": dec["id"], "kind": k, "stage": "③", "result": "applied", "anchor": a, **({"established": True} if est else {}), **({"replaced_members": True} if was_multi else {})})
        elif k == "tuple_assign_multi":
            a = t.get("catalog_item_id") or t.get("ref_id")
            vals = []
            for i, tt in enumerate(nv.get("tuples", [])):
                wk, w = what_of_id(ctx, tt.get("what_id"))
                sid, slab = site_of_id(ctx, tt.get("site_id"))
                tid_, tname = tech_of_id(ctx, tt.get("technique_id"))
                if w is None or sid is None or tid_ is None or (sid != "none" and ctx["ids"].site_kind.get(norm(slab)) == "layer"):
                    vals = None
                    break
                vals.append((wk, w, sid, slab, tid_, tname))
            if not vals or len(vals) < 2:
                log.append({"id": dec["id"], "kind": k, "stage": "③", "result": "rejected", "why": "dictionary — 지정 튜플 값이 사전·실버에 없거나(layer 부위 포함) 둘 미만"})
                continue
            est = a not in AM.spec
            if est and AM.establish(a, dec["id"]) is None:
                log.append({"id": dec["id"], "kind": k, "stage": "③", "result": "rejected", "why": "anchor 가 원장 참조·분류 항목이 아니다"})
                continue
            if a in AM.multi:
                AM.reassign_base(a, dec["id"])
            base = AM.spec[a]
            same_what = len({v[1]["id"] for v in vals}) == 1
            mode = "and" if same_what else (nv.get("member_mode") or "and")
            subs = []
            for i, (wk, w, sid, slab, tid_, tname) in enumerate(vals):
                sa = f"{a}#{'s' if same_what else 'm'}{i}"  # V3-4 · R-3: 같은 what × 부위 여럿 = #s<i> · 그 밖 = #m<i>
                AM.spec[sa] = {"anchor": sa, "what_kind": wk, "what_id": w["id"], "what_label": w["label"], "family": w.get("family"), "site_id": sid, "site": slab, "technique_id": tid_, "technique": tname,
                               "technique_origin": "decision" if tname else "none", "origins": list(base.get("origins", [])), "occ": list(base.get("occ", [])), "status": "complete", "unregistered_fragments": [],
                               "candidate_name": [], "extra_primaries": [], "extra_sites": [], "decision_ids": [dec["id"]], "member_mode": mode}
                AM.dropped.pop(sa, None)
                AM.redirect.pop(sa, None)
                subs.append(sa)
            AM.multi[a] = subs
            base["virtual"] = True
            base["member_mode"] = mode
            base.setdefault("decision_ids", []).append(dec["id"])
            log.append({"id": dec["id"], "kind": k, "stage": "③", "result": "applied", "anchor": a, "sub_anchors": subs, "member_mode": mode, "shape": "multi_tuple" if same_what else "combo_ref", **({"established": True} if est else {})})
        elif k == "adverse_tuple_assign":
            apply_adverse_assign(ctx, AU, dec, log)
    for dec in decisions:
        if dec["kind"] == "fold_approve" and is_node_fold(dec):
            continue   # v3.2 원장 사건 노드 접기 — 분해 단계에서 적용(log_node_decisions)
        if dec["kind"] == "fold_approve":
            anchors, keep = dec["target"].get("anchors", []), dec["new_value"].get("keep_anchor")
            if keep not in anchors or any(a not in AM.spec for a in anchors) or len(anchors) < 2:
                log.append({"id": dec["id"], "kind": "fold_approve", "stage": "④", "result": "rejected", "why": "anchors/keep_anchor 가 실버에 없다"})
                continue
            for a in anchors:
                if a != keep:
                    AM.redirect[a] = keep
            AM.spec[keep].setdefault("decision_ids", []).append(dec["id"])
            ctx.setdefault("folds", []).append({"id": dec["id"], "anchors": list(anchors), "keep": keep})
            log.append({"id": dec["id"], "kind": "fold_approve", "stage": "④", "result": "applied", "keep": keep, "folded": [a for a in anchors if a != keep]})


def _legacy_tuple(ctx, AU, x):
    """옛 네 칸 지정(event_id, site_id, course_id, qualifier_id) → (단위 세 칸 사전 id, 경과 정준값 목록) · v3.1: 경과는 R15 엣지 속성 · 상대 부위는 none."""
    co = []
    cid = x.get("course_id")
    if cid and cid != "none":
        c = AU._by_id(ctx["ids"].course, cid)
        if c is None:
            return None, None
        if c["label"] != "미상":
            co = [c["label"]]
    return (x.get("event_id"), x.get("site_id", "none"), x.get("qualifier_id", "none")), co


def apply_adverse_assign(ctx, AU, dec, log):
    """③ adverse_tuple_assign(v3.1) — target.kind=raw_name(complications 이름 locator) · new_value.tuples = 세 칸 사전 id(없으면 결정이 세운다) · courses = R15 경과.
    옛 네 칸(course_id)은 경과를 그 단위의 R15 경과로 옮긴다. 옛 target.kind=expression(표현 locator)은 그 자리의 문구 사전 항목 지도로 적용(phrase_map 과 같은 효과)."""
    t, nv = dec["target"], dec["new_value"]
    lc, kind = t.get("locator"), t.get("kind")
    uids, cbu, legacy = [], {}, False
    v31_courses = AU.course_labels(nv.get("courses")) if nv.get("courses") is not None else None
    if nv.get("courses") is not None and v31_courses is None:
        log.append({"id": dec["id"], "kind": "adverse_tuple_assign", "stage": "③", "result": "rejected", "why": "dictionary — courses 가 경과 사전 값이 아니다"})
        return
    for x in nv.get("tuples", []):
        if "course_id" in x:
            legacy = True
            key, co = _legacy_tuple(ctx, AU, x)
            if key is None:
                uids = None
                break
        else:
            key, co = (x.get("event_id"), x.get("site_id", "none"), x.get("qualifier_id", "none")), []
        u = AU.unit_for(key[0], key[1], key[2], dec["id"])
        if u is None:
            uids = None
            break
        uids.append(u)
        cbu[u] = dedupe(cbu.get(u, []) + co + (v31_courses or []))
    if not uids:
        log.append({"id": dec["id"], "kind": "adverse_tuple_assign", "stage": "③", "result": "rejected", "why": "dictionary — 지정 단위의 사전 id(사건·부위·수식·경과)가 없다"})
        return
    uids = dedupe(uids)
    note = "옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9)" if legacy else None
    v32 = bool(ctx.get("is32"))
    if kind in ("raw_name", "name") and lc in AU.name_units:
        before = list(AU.name_units[lc])
        AU.assign_name(lc, uids, cbu, dec["id"])
        if v32:
            ev_before = [AU.units[u]["event"] for u in before if u in AU.units]
            note = (("v3.2: 이름 단위(raw_name)는 없다 — " if kind == "raw_name" else "v3.2: ") + "이 이름의 단위(" + (", ".join(f"{e}{'·원장 노드' if norm(e) in AU.ledger else ''}" for e in ev_before) or "없음")
                    + ")를 지정 단위로 대체(V3.2-0 · 같은 locator)") + (" · " + note if note else "")
        log.append({"id": dec["id"], "kind": "adverse_tuple_assign", "stage": "③", "result": "applied", "locator": lc, "units": uids, "courses": {u: cbu[u] for u in uids}, **({"replaced_units": before} if v32 else {}), **({"note": note} if note else {})})
    elif kind in ("expression", "phrase") and lc in AU.loc_phrase:
        pid = AU.loc_phrase[lc]
        courses = dedupe(c for u in uids for c in cbu[u])
        was = AU.phrases[pid]["status"]
        AU.map_phrase(pid, uids, courses, dec["id"], f"adverse_tuple_assign({kind})")
        msg = ("v3.2: 옛 표현 지정 → 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · 같은 정규화형 자리 전부 · 항목 status " + was + " → approved)") if v32 else \
            "v3.1: 표현은 개체가 아니다(V3.1-10) — 옛 표현 지정을 그 자리의 문구 사전 항목 지도로 적용(phrase_map 과 같은 효과 · 같은 정규화형 자리 전부)"
        log.append({"id": dec["id"], "kind": "adverse_tuple_assign", "stage": "③", "result": "applied", "locator": lc, "phrase_id": pid, "units": uids, "courses": courses,
                    "note": msg + (" · " + note if note else "")})
    elif v32 and kind in ("expression", "phrase") and hasattr(AU, "line_of") and AU.line_of(lc):
        ll = AU.line_of(lc)
        courses = dedupe(c for u in uids for c in cbu[u])
        before = list(AU.lines[ll][2]["adverse_ref"])
        AU.assign_line(ll, uids, courses, dec["id"])
        log.append({"id": dec["id"], "kind": "adverse_tuple_assign", "stage": "③", "result": "applied", "locator": lc, "line_locator": ll, "units": uids, "courses": courses, "replaced_refs": before,
                    "note": "v3.2: 타임라인 줄은 문구 사전이 아니라 자기 테이블(post_procedure_timeline · V3.2-9) — 옛 표현 지정을 그 줄의 참조(adverse_ref · R34)로 옮기고 경과는 계열 R15 엣지 경과로(지정 단위가 없으면 결정이 세운다)" + (" · " + note if note else "")})
    else:
        log.append({"id": dec["id"], "kind": "adverse_tuple_assign", "stage": "③", "result": "rejected", "why": "locator 가 부작용 이름·문구 자리(또는 옛 표현·타임라인 줄)에 없다"})


def apply_phrase_maps(ctx, AU, decisions, log):
    """① phrase_map(V3.1-10) — 문구 사전 항목(PHR- 또는 normalized)의 지도를 사람이 정한다: units(세 칸 사전 정준값 · 없으면 none · [] = 부작용 아님) · courses(경과 덮어쓰기)."""
    for dec in decisions:
        t, nv = dec["target"], dec["new_value"]
        pid = AU.phrase_of(t)
        if pid is None:
            log.append({"id": dec["id"], "kind": "phrase_map", "stage": "①", "result": "no_target", "why": "문구 사전에 그 PHR-·정규화형 항목이 없다"})
            continue
        uids, bad = [], None
        for u in nv.get("units") or []:
            key, why = AU.labels_to_ids(u.get("event"), u.get("site"), u.get("qualifier"))
            if key is None:
                bad = why
                break
            uid = AU.unit_for(key[0], key[1], key[2], dec["id"], key[3])
            if uid is None:
                bad = "단위를 세울 수 없다"
                break
            uids.append(uid)
        courses = None
        if bad is None and nv.get("courses") is not None:
            courses = AU.course_labels(nv["courses"])
            if courses is None:
                bad = "courses 가 경과 사전 값이 아니다"
        if bad:
            log.append({"id": dec["id"], "kind": "phrase_map", "stage": "①", "result": "rejected", "why": "dictionary — " + bad})
            continue
        AU.map_phrase(pid, dedupe(uids), courses, dec["id"], "phrase_map")
        log.append({"id": dec["id"], "kind": "phrase_map", "stage": "①", "result": "applied", "phrase_id": pid, "units": dedupe(uids), "courses": courses, "locators": len(AU.phrases[pid]["locators"])})


# ---------------------------------------------------------------------------
# ⑤ edge_create · ⑥ conflict · ⑦ exclude
# ---------------------------------------------------------------------------
def ref_to_end(ctx, AM, AU, ref):
    k = ref.get("kind")
    if k == "anchor":
        ids = AM.resolve(ref.get("anchor"))
        return [("procedure", i) for i in ids]
    if k == "procedure_tuple":
        tt = ref.get("tuple", {})
        for tid, t in AM.tuples().items():
            if (t["what_id"], t["site_id"], t["technique_id"]) == (tt.get("what_id"), tt.get("site_id"), tt.get("technique_id")):
                return [("procedure", tid)]
        return []
    if k == "adverse_tuple":
        key, _ = AU.labels_to_ids(*_tuple3(ref.get("tuple", {})))
        if key is None:
            return []
        from .units31 import unit_id3
        uid = unit_id3(key[0], key[1], key[2])
        return [("adverse_effect", uid)] if uid in AU.units else []
    if k == "locator":
        lc = ref.get("locator")
        if lc in AU.name_units:
            return [("adverse_effect", u) for u in AU.name_units[lc]]
        return []
    return []


def _tuple3(tt):
    """ref 구조체 adverse_tuple — v3.1 세 칸(event, site, qualifier · 없음은 none). 옛 네 칸의 course 는 엣지 속성(attrs.course)으로 간다."""
    return tt.get("event"), tt.get("site") or "none", tt.get("qualifier") or "none"


def prepare_edge_units(ctx, AU, decisions, log_note):
    """⑤ edge_create 의 adverse_tuple 끝(세 칸 사전 값)이 기존 단위에 없으면 결정이 단위를 세운다(§5.2 adverse_tuple_assign 와 같은 규칙 · 사전 값만).
    개체 적재(build_adverse) 전에 돌아 단위 레코드가 생긴다."""
    from .units31 import unit_id3
    for dec in decisions:
        if dec["kind"] != "edge_create":
            continue
        for side in ("from_ref", "to_ref"):
            ref = dec["target"].get(side) or {}
            if ref.get("kind") != "adverse_tuple":
                continue
            key, why = AU.labels_to_ids(*_tuple3(ref.get("tuple", {})))
            if key is None:
                continue
            uid = AU.unit_for(key[0], key[1], key[2], dec["id"], key[3])
            if uid:
                AU.edge_units.append(uid)
                log_note.append({"decision": dec["id"], "side": side, "unit": uid, "tuple": ref.get("tuple")})


PROC_AXIS = ("procedure", "modality", "modality_subcategory", "product")
DEPTH = {"procedure": "procedure", "modality": "modality", "modality_subcategory": "subcategory", "product": "product"}


def allowed_ends(erd, rel, side):
    """erd.relations[R#].from/to → 허용 개체 종류. proc_axis = procedure|modality|modality_subcategory|product · `x(y)`(부분 종류 표기)는 x ·
    `(임의 개체|엣지)`·`(모든 개체·엣지·속성값)` 은 개체 전부(엣지·속성값은 ref 구조체가 가리키지 못한다)."""
    r = next((x for x in erd["relations"] if x["id"] == rel), None)
    if r is None:
        return None
    ents = [e["key"] for e in erd["entities"]]
    s = str(r[side])
    if "임의" in s or "모든" in s:
        return list(ents)
    out = []
    for t in s.split("|"):
        t = re.sub(r"\(.*?\)", "", t).strip()
        out += list(PROC_AXIS) if t == "proc_axis" else [t]
    return out


def dict_entities(erd, dic):
    """사전 이름 → 그 사전 값이 곧 식별인 개체(개체 이름 = 사전 이름 · 또는 사전 이름의 _label/_name 접미 제거) — ERD §5.2 ref 구조체 dict_value 의 끝."""
    names = {d["name"] for d in dic["dictionaries"]}
    out = {}
    for e in erd["entities"]:
        for n in (e["key"], f"{e['key']}_label", f"{e['key']}_name"):
            if n in names:
                out[n] = (e["key"], e["prefix"])
    return out


def dict_value_end(S, dv):
    """dict_value(사전 이름 + 정준값 · 또는 고정 id) → (개체 종류, id) · 실패면 (None, 사유)."""
    ctx = S.ctx
    de = dict_entities(ctx["erd"], ctx["dic"])
    rid = dv.get("id")
    if rid:
        pre = str(rid).split("-")[0]
        typ = next((t for t, p in de.values() if p == pre), None)
        return (typ, rid) if typ and rid in S.E.get(typ, {}) else (None, f"고정 id {rid} 가 사전 값 개체 레코드가 아니다")
    name, canon = dv.get("dictionary"), dv.get("canonical")
    if name not in de:
        return None, f"사전 {name} 은 개체를 식별하는 사전이 아니다(dict_value 끝 없음)"
    typ = de[name][0]
    e = next((x for x in ctx["dicts"][name]["entries"] if norm(x["canonical"]) == norm(canon)), None)
    if e is None:
        return None, f"사전 {name} 에 정준값 「{canon}」 없음"
    ids, code = ctx["ids"], e.get("code")
    single = code is not None and "|" not in str(code)
    if typ == "modality":
        rid = ids.mod.get(code, {}).get("id")
    elif typ == "modality_subcategory":
        hit = ids.sub_by_label.get((code, norm(e["canonical"]))) if single else None
        rid = hit[0]["id"] if hit else None
    elif typ == "product":
        rid = (ids.prod.get(norm(e["canonical"])) or {}).get("id")
    elif typ == "site":
        rid = (ids.site.get(norm(e["canonical"])) or {}).get("id")
    elif typ == "technique":
        rid = mkid("TEC", e["canonical"])
    elif typ == "person_condition":
        # v3.1(V3.1-4) 조건 단위 CND-sha(kind|정준값) — kind 가 둘 이상이면 dict.kind 로 가른다(없으면 모호)
        kinds = [dv["kind"]] if dv.get("kind") else (e.get("kinds") or ([e["kind"]] if e.get("kind") else []))
        cands = [mkid("CND", f"{k_}|{e['canonical']}") for k_ in kinds]
        cands = [c for c in cands if c in S.E.get("person_condition", {})]
        if len(cands) != 1:
            return None, f"dict_value person_condition|{canon} 의 조건 단위가 {len(cands)} 개(kind {kinds}) — dict.kind 로 하나를 고른다" if cands else f"dict_value person_condition|{canon} 의 조건 단위가 실버에 없다"
        rid = cands[0]
    elif typ == "problem":
        rid = mkid("PRB", code) if code else None
    elif typ == "problem_subcategory":
        rid = mkid("PSB", f"{code}|{e['canonical']}") if single else None
    elif typ == "catalog_item":
        rid = mkid("CAT", f"{code}|{e['canonical']}") if single else None
    else:
        rid = None
    if rid is None or rid not in S.E.get(typ, {}):
        return None, f"dict_value {name}|{canon} 의 {typ} 레코드가 실버에 없다(계열 둘 이상이면 모호)"
    return typ, rid


def _locator_index(S):
    """원장 locator → 그 locator 를 provenance(칸 prov · 레코드 provenance · derived_from)로 가진 실버 레코드 [(type, id)]."""
    idx = S.ctx.get("_loc_index")
    if idx:
        return idx
    from .provenance import loc as _loc
    idx = {}
    for et, recs in S.E.items():
        for rid, rec in recs.items():
            seen = set()
            for cells in list(rec["attrs"].values()) + [rec.get("aliases", [])]:
                for c in cells:
                    for p in c.get("prov", []):
                        seen.add(_loc(p))
            seen |= {d for d in rec.get("derived_from", []) if ".json:" in d}
            for l in seen:
                idx.setdefault(l, []).append((et, rid))
    S.ctx["_loc_index"] = idx
    return idx


PRODUCT_NOTE_PATH = re.compile(r"^(?:[^.\[\]]+\.products\[\]|modality\[\]\.products\[\])\.(note|legal_warning|regulatory_status)$")


def ensure_product_note_rule(S, lc, dec_id=None):
    """v3.1(V3.1-2) — locator 가 제품 note·legal_warning·regulatory_status 문장이면 clinical_rule(kind=product_note) 레코드를 세운다(값 자동 생성 아님 · edge_create 가 가리킬 때만)."""
    from .provenance import parse_loc, resolve
    try:
        p = parse_loc(lc)
    except ValueError:
        return None
    if p["file"] not in ("products.json", "taxonomy.json") or not PRODUCT_NOTE_PATH.match(p["path"]):
        return None
    try:
        v = resolve(S.ctx["L"][p["file"]], p["path"], p["rec"])
    except (KeyError, ValueError, IndexError, TypeError):
        return None
    if not isinstance(v, str) or not v.strip():
        return None
    rid = mkid("RUL", f"product_note|{norm(v)}")
    new = rid not in S.E.get("clinical_rule", {})
    rec = S.ent("clinical_rule", rid, [lc])
    if new:
        S.dattr(rec, "kind", "product_note", [lc])
        S.dattr(rec, "source_locator", lc, [lc])
        S.dattr(rec, "phrase_ids", None, [lc])
    if not any(lc == f"{q['file']}:{q['path']}@{q['rec']}" for c in rec["attrs"].get("text", []) for q in c.get("prov", [])):
        S.attr(rec, "text", v, p)
    if dec_id:
        ds = rec["attrs"].get("decision_ids", [{"value": []}])[0]["value"]
        S.dattr(rec, "decision_ids", sorted(set(ds) | {dec_id}), sorted(set(ds) | {dec_id}))
    S.ctx["_loc_index"] = None
    return rid


def ref_to_end_full(S, AM, AU, ref, allowed, dec_id=None):
    """ERD v3 §5.2 edge_create ref 구조체 → [(type, id, depth)] · 실패면 ([], 사유).
    dict_value = 사전 값이 곧 식별인 개체 전부(계열·하위분류·제품·기법·부위·고민·고민 하위분류·분류 항목 — dict_entities) · 고정 id(MOD-/SUB-/PRD-/SIT-/TEC-/…) ·
    locator = provenance 가 일치하는 실버 레코드(개체 종류 무관 · 관계 허용 끝만)."""
    k = ref.get("kind")
    if k == "dict_value":
        dv = ref.get("dict") or {}
        typ, rid = dict_value_end(S, dv)
        if typ is None:
            return [], rid
        if allowed is not None and typ not in allowed:
            return [], f"dict_value 끝 종류 {typ} 가 관계 허용 끝 {allowed} 밖"
        return [(typ, rid, DEPTH.get(typ))], None
    if k == "locator":
        lc = ref.get("locator")
        if lc in AU.name_units and (allowed is None or "adverse_effect" in allowed):
            return [("adverse_effect", u, None) for u in AU.name_units[lc]], None
        if allowed is not None and "clinical_rule" in allowed:
            ensure_product_note_rule(S, lc, dec_id)
        hits = _locator_index(S).get(lc, [])
        if ref.get("entity"):
            hits = [h for h in hits if h[0] == ref["entity"]]
        ok = [h for h in hits if allowed is None or h[0] in allowed]
        if not hits:
            return [], f"locator {lc} 를 provenance 로 가진 실버 레코드 없음"
        if not ok:
            return [], f"locator {lc} 의 레코드 종류 {sorted({h[0] for h in hits})} 가 관계 허용 끝 {allowed} 밖"
        if len(ok) > 1:
            return [], f"locator {lc} 가 허용 끝 레코드 둘 이상 {ok[:4]} — 모호(entity 를 지정해야 한다)"
        return [(ok[0][0], ok[0][1], DEPTH.get(ok[0][0]))], None
    out = [(t, i, DEPTH.get(t)) for t, i in ref_to_end(S.ctx, AM, AU, ref)]
    if not out:
        return [], f"{k} ref 가 실버 레코드로 풀리지 않는다"
    if allowed is not None and any(t not in allowed for t, _, _ in out):
        return [], f"{k} 끝 종류가 관계 허용 끝 {allowed} 밖"
    return out, None


def apply_edges(S, AM, AU, decisions, log):
    for dec in decisions:
        if dec["kind"] != "edge_create":
            continue
        t = dec["target"]
        rel = t.get("relation")
        fs, why_f = ref_to_end_full(S, AM, AU, t.get("from_ref", {}), allowed_ends(S.ctx["erd"], rel, "from"), dec["id"])
        ts, why_t = ref_to_end_full(S, AM, AU, t.get("to_ref", {}), allowed_ends(S.ctx["erd"], rel, "to"), dec["id"])
        legacy_course = [x.get("tuple", {}).get("course") for x in (t.get("from_ref", {}), t.get("to_ref", {})) if x.get("kind") == "adverse_tuple" and "course" in (x.get("tuple") or {})]
        if not fs or not ts:
            log.append({"id": dec["id"], "kind": "edge_create", "stage": "⑤", "result": "rejected", "why": "양끝이 실버 레코드로 풀리지 않는다 — " + " · ".join(w for w in (why_f, why_t) if w)})
            continue
        made, merged, ends = 0, 0, []
        for f in fs:
            for x in ts:
                same = [e for e in S.R.get(rel, []) if e["from"]["type"] == f[0] and e["from"]["id"] == f[1] and e["to"]["type"] == x[0] and e["to"]["id"] == x[1]]
                if same:
                    # 같은 양끝 엣지가 이미 있다 — 중복 생성 대신 decision_id 를 덧붙인다
                    for e in same:
                        c = e["attrs"].setdefault("decision_ids", {"value": [], "derived_from": []})
                        if dec["id"] not in c["value"]:
                            c["value"].append(dec["id"])
                            c["derived_from"].append(dec["id"])
                        if dec["id"] not in e["derived_from"]:
                            e["derived_from"].append(dec["id"])
                    merged += 1
                else:
                    attrs = {k: {"value": v, "derived_from": [dec["id"]]} for k, v in (dec["new_value"].get("attrs") or {}).items()}
                    lc_ = [c for c in legacy_course if c and c != "미상"]
                    if rel == "R15" and lc_ and "course" not in attrs:
                        attrs["course"] = {"value": dedupe(lc_), "derived_from": [dec["id"]]}  # 옛 네 칸 ref 의 경과 → R15 엣지 속성(v3.1)
                    if f[2]:
                        attrs["from_target_depth"] = {"value": f[2], "derived_from": [dec["id"]]}
                    if x[2]:
                        attrs["to_target_depth"] = {"value": x[2], "derived_from": [dec["id"]]}
                    attrs["decision_id"] = {"value": dec["id"], "derived_from": [dec["id"]]}
                    S.edge(rel, f[0], f[1], x[0], x[1], [], attrs, derived_from=[dec["id"]])
                    made += 1
                ends.append(f"{f[0]}:{f[1]}→{x[0]}:{x[1]}")
        log.append({"id": dec["id"], "kind": "edge_create", "stage": "⑤", "result": "applied", "relation": rel, "created": made, "merged_into_existing": merged, "ends": ends,
                    **({"note": "옛 네 칸 adverse_tuple — 경과 " + ", ".join(str(c) for c in legacy_course) + (" → R15.course" if rel == "R15" else " — 이 관계에 경과 자리 없음(단위 세 칸만 · v3.1)")} if legacy_course else {})})


def apply_conflicts(S, decisions, log):
    by = {}
    for c in S.conflicts:
        by.setdefault(json.dumps(c["stable_key"], ensure_ascii=False, sort_keys=True), []).append(c)
    for dec in decisions:
        if dec["kind"] not in ("conflict_override", "conflict_close"):
            continue
        key = json.dumps(dec["target"].get("conflict_key"), ensure_ascii=False, sort_keys=True)
        cs = by.get(key, [])
        ck = dec["target"].get("conflict_key") or {}
        if not cs and ck.get("pair"):
            # v3.2 ⑦ 노드 쌍 — ERD 안정 키 duplicate_candidate|adverse_event_type|가|나 로 찾는다(다른 결정이 노드 자리를 옮겨 locators 가 바뀌어도 같은 쌍)
            want = frozenset(str(ck["pair"]).split("|")[2:])   # 쌍은 순서 없이(duplicate_candidate|adverse_event_type|가|나)
            cs = [c for c in S.conflicts if c["kind"] == ck.get("kind") and c["stable_key"].get("pair") and frozenset(c["stable_key"]["pair"].split("|")[2:]) == want]
        if not cs:
            log.append({"id": dec["id"], "kind": dec["kind"], "stage": "⑥", "result": "no_target", "why": "stable_key 일치 충돌 없음"})
            continue
        for c in cs:
            c["decision_id"] = dec["id"]
            if dec["kind"] == "conflict_override":
                c["chosen_value"] = dec["new_value"].get("chosen_value")
                c["status"] = "resolved"
            else:
                c["close_verdict"] = dec["new_value"].get("verdict")
                c["close_note"] = dec["new_value"].get("note")
                c["status"] = "dismissed"
        log.append({"id": dec["id"], "kind": dec["kind"], "stage": "⑥", "result": "applied", "conflicts": [c["id"] for c in cs]})


def apply_excludes(S, AM, decisions, log):
    from .provenance import loc as _loc
    for dec in decisions:
        if dec["kind"] != "exclude" or is_node_exclude(dec):
            continue   # v3.2 원장 사건 노드 = 부작용 아님 — 분해 단계에서 적용(log_node_decisions)
        k, key = dec["target"].get("kind"), dec["target"].get("key")
        n = 0
        if k in ("catalog_item", "reference"):
            if key in AM.spec:
                AM.excluded[key] = dec["id"]
                n = 1
            if k == "catalog_item" and key in S.E["catalog_item"]:
                S.excluded.append({"type": "catalog_item", "id": key, "decision_id": dec["id"]})
                S.E["catalog_item"][key]["status"] = "excluded"
        elif k == "ledger_record":
            for et, recs in S.E.items():
                for rid, rec in recs.items():
                    provs = [_loc(p) for cells in rec["attrs"].values() for c in cells for p in c.get("prov", [])]
                    if key in provs or key in rec["derived_from"]:
                        rec["status"] = "excluded"
                        S.excluded.append({"type": et, "id": rid, "decision_id": dec["id"]})
                        n += 1
        elif k == "dictionary_value":
            S.ctx.setdefault("excluded_dict_values", []).append(dict(key, decision_id=dec["id"]))
            n = 1
        log.append({"id": dec["id"], "kind": "exclude", "stage": "⑦", "result": "applied" if n else "no_target", "n": n})


# ---------------------------------------------------------------------------
# v3.2(V3.2-0) — 원장 사건 노드 결정: fold_approve(사전 값 쌍) · exclude(dictionary_value · 부작용 아님)
# 분해가 핵심어 노드를 세울 때 읽는다(lib.v32 CUR node_folds · not_adverse) — 적용 단계 표시는 ④ · ⑦ 그대로(사전 단계 event_split 처럼 분해 전에 걸린다)
# ---------------------------------------------------------------------------
def is_node_fold(d):
    t = d.get("target") or {}
    return d.get("kind") == "fold_approve" and t.get("dictionary") == "adverse_event_type"


def is_node_exclude(d):
    t = d.get("target") or {}
    k = t.get("key")
    return d.get("kind") == "exclude" and t.get("kind") == "dictionary_value" and isinstance(k, dict) and k.get("dictionary") == "adverse_event_type"


def node_decisions(approved):
    """approved 결정 중 원장 사건 노드 결정 → (folds {norm(노드): 접힐 곳 정준값}, not_adverse {norm(노드): 결정 id}, 결정 목록)."""
    folds, excl, decs = OrderedDict(), OrderedDict(), []
    for d in ordered(approved):
        t, nv = d["target"], d["new_value"]
        if is_node_fold(d):
            into = t.get("into") or nv.get("keep")
            if t.get("canonical") and into:
                folds[norm(t["canonical"])] = into
            decs.append(d)
        elif is_node_exclude(d):
            excl[norm(t["key"].get("canonical") or "")] = d["id"]
            decs.append(d)
    return folds, excl, decs


def validate_node_decisions(decs, folds, excl, dic, adv0, log):
    """노드 결정의 대상 확인 — 노드는 결정 전 분해(adv0)의 원장 사건 노드여야 하고, 접힐 곳은 사건 사전 값(① 뒤)이거나 다른 원장 노드여야 한다. 아니면 거부(분해 지도에서 뺀다)."""
    nodes = {norm(n["canonical"]) for n in adv0["ledger_events"]}
    D = {d["name"]: d for d in dic["dictionaries"]}
    ev = {norm(v) for e in D["adverse_event_type"]["entries"] for v in [e["canonical"]] + [s["value"] for s in e.get("synonyms", [])]}
    bad = []
    for d in decs:
        if is_node_fold(d):
            k = norm(d["target"].get("canonical") or "")
            into = d["target"].get("into") or d["new_value"].get("keep")
            why = None
            if k not in nodes:
                why = f"「{d['target'].get('canonical')}」 은 결정 전 분해의 원장 사건 노드가 아니다"
            elif not into or norm(into) == k:
                why = "접힐 곳(target.into · new_value.keep)이 없거나 자기 자신"
            elif norm(into) not in ev and norm(into) not in nodes:
                why = f"접힐 곳 「{into}」 이 사건 사전 값도 원장 사건 노드도 아니다"
            if why:
                folds.pop(k, None)
                bad.append(d["id"])
                log.append({"id": d["id"], "kind": "fold_approve", "stage": "④", "result": "rejected", "why": why})
        else:
            k = norm(d["target"]["key"].get("canonical") or "")
            if k not in nodes:
                excl.pop(k, None)
                bad.append(d["id"])
                log.append({"id": d["id"], "kind": "exclude", "stage": "⑦", "result": "no_target", "why": f"「{d['target']['key'].get('canonical')}」 은 결정 전 분해의 원장 사건 노드가 아니다(사전 값 제외는 dictionary_remove)"})
    return [d for d in decs if d["id"] not in bad]


def log_node_decisions(ctx, adv, decs, log):
    """분해 뒤 — 노드 결정이 실제로 닿은 자리(접힌 자리 · 뺀 자리)를 적용 로그에."""
    fh = {norm(k): v for k, v in adv.get("fold_hits", {}).items()}
    eh = defaultdict(list)
    for lc, cores in adv.get("excluded_hits", {}).items():
        for c in cores:
            eh[norm(c)].append(lc)
    for d in decs:
        if is_node_fold(d):
            k = norm(d["target"]["canonical"])
            hits = fh.get(k, [])
            into = d["target"].get("into") or d["new_value"].get("keep")
            log.append({"id": d["id"], "kind": "fold_approve", "stage": "④", "result": "applied" if hits else "no_target", "node": d["target"]["canonical"], "into": into, "locators": len(hits),
                        "note": "v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음)"})
            ctx.setdefault("node_folds_applied", []).append({"id": d["id"], "node": d["target"]["canonical"], "into": into, "locators": [x[0] for x in hits]})
        else:
            k = norm(d["target"]["key"]["canonical"])
            hits = eh.get(k, [])
            log.append({"id": d["id"], "kind": "exclude", "stage": "⑦", "result": "applied" if hits else "no_target", "node": d["target"]["key"]["canonical"], "locators": len(hits),
                        "note": "v3.2(V3.2-0 · V3.2-7): 원장 사건 노드 = 부작용 아님 — 노드를 세우지 않고 그 토큰은 설명(보존) · 사건이 남지 않은 문구는 메모(note)"})
            ctx.setdefault("node_excludes_applied", []).append({"id": d["id"], "node": d["target"]["key"]["canonical"], "locators": hits})
