# -*- coding: utf-8 -*-
"""산출물 쓰기 — out/ (재실행 바이트 동일 · 빌드 시각 없음) + gate + report.md."""
import json
import os
from collections import Counter, OrderedDict, defaultdict

from .core import eref
from .decisions import STAGE, RECORD_ONLY
from .provenance import loc, rec_str
from .util import dumps, md_table, mkid, norm, sha256_bytes, write_json, write_jsonl, write_text

ENTITY_TYPES = ["source_file", "modality", "modality_subcategory", "catalog_item", "procedure", "product", "technique", "site", "anatomical_structure", "problem",
                "problem_subcategory", "complaint", "package", "adverse_effect", "person_condition", "citation", "evidence_statement", "clinical_rule", "conflict", "decision",
                "post_procedure_timeline", "emergency_sign"]   # ERD v3.2 개체 22(v3.1 20 + 타임라인 · 응급 징후)
RELATIONS = [f"R{i}" for i in range(1, 36) if i != 29]   # ERD v3.2 관계 34(R29 없음 · R32 · R33 · R34 · R35) — v3.3 은 relations_of(erd)(+R36 component_of)


def relations_of(erd):
    """ERD 관계 목록(번호 순) — v3.2 이하는 RELATIONS 와 같다 · v3.3 은 R36 이 더 있다(엣지 0 이어도 파일을 쓴다)."""
    ids = [r["id"] for r in erd.get("relations", [])]
    if not ids:
        return list(RELATIONS)
    return sorted(ids, key=lambda x: int(x[1:]))


def finish_record(r):
    prov, seen = [], set()
    for cells in r["attrs"].values():
        for c in cells:
            for p in c.get("prov", []):
                k = loc(p)
                if k not in seen:
                    seen.add(k)
                    prov.append(p)
    for a in r["aliases"]:
        for p in a.get("prov", []):
            k = loc(p)
            if k not in seen:
                seen.add(k)
                prov.append(p)
    out = OrderedDict([("id", r["id"]), ("type", r["type"]), ("status", r["status"]), ("attrs", r["attrs"]), ("aliases", r["aliases"]),
                       ("provenance", sorted(prov, key=lambda p: (p["file"], p["path"], p["rec"]))), ("derived_from", sorted(r["derived_from"]))])
    for k in ("kind_variants",):
        if k in r:
            out[k] = sorted(set(r[k]))
    return out


def erd_to_source_locators(S):
    """ERD 꼴 locator(complications 이름 `@M16/4` · 표현 `@<계열>/<순번>` — 결정 target·anchor 용) → 원장 위치 locator."""
    AU = S.ctx.get("AU") or S.ctx.get("AU_live")
    return {k: loc(v) for k, v in AU.erd2p.items()}


def decision_records(S):
    out = []
    e2s = erd_to_source_locators(S)
    erd_dec = {d["id"]: i for i, d in enumerate(S.ctx["erd"]["decisions"])}
    applied = {x["id"]: x for x in S.apply_log}
    for d in list(S.ctx["decisions_approved"]) + list(S.ctx["decisions_listed"]):
        df = []
        if d["id"] in erd_dec:
            df.append(eref("decisions", d["id"]))
        for p in d.get("provenance", []):
            df.append(loc(p))
        for s in d.get("source_refs", []):
            if s.get("kind") == "ledger" and ".json:" in s.get("ref", ""):
                df.append(e2s.get(s["ref"], s["ref"]))  # ERD 꼴이면 원장 위치로(provenance 는 원장 위치만)
        if not df:
            df.append(f"decisions/{d.get('_file', d['id'])}")
        rec = OrderedDict([("id", d["id"]), ("type", "decision"), ("status", "active"),
                           ("attrs", OrderedDict((k, [{"value": d.get(k), "derived_from": sorted(set(df))}]) for k in ("kind", "target", "new_value", "reason", "decided_by", "decided_at", "status", "source_refs"))),
                           ("aliases", []), ("provenance", [p for p in d.get("provenance", [])]), ("derived_from", sorted(set(df))),
                           ("stage", STAGE.get(d["kind"], "—")), ("build_reads", d["kind"] not in RECORD_ONLY), ("store_file", d.get("_file")),
                           ("apply_result", applied.get(d["id"], {}).get("result") if d["status"] == "approved" else "not_read(status=" + d["status"] + ")")])
        out.append(rec)
    return out


def conflict_records(S):
    out = []
    for c in S.conflicts:
        df = sorted(set(c["stable_key"]["locators"]))
        rec = OrderedDict([("id", c["id"]), ("type", "conflict"), ("status", c["status"]), ("attrs", OrderedDict((k, [{"value": c.get(k), "derived_from": df or ["conflict:" + c["id"]]}]) for k in
                                                                                                          ("kind", "rule_ref", "target_type", "target_id", "field", "stable_key", "values", "resolution_rule", "chosen_value", "close_verdict", "status", "decision_id"))),
                           ("aliases", []), ("provenance", [{"file": v["source_file"], "path": v["source_path"], "rec": v["rec"]} for v in c["values"] if v.get("source_file")]), ("derived_from", df)])
        out.append(rec)
    return out


def write_all(S, out_dir, base_cmp, gate_counts_holder):
    os.makedirs(out_dir, exist_ok=True)
    # 엔티티
    recs = {}
    for t in ENTITY_TYPES:
        if t == "conflict":
            rows = conflict_records(S)
        elif t == "decision":
            rows = decision_records(S)
        else:
            rows = [finish_record(r) for r in S.E.get(t, {}).values()]
        rows.sort(key=lambda r: r["id"])
        recs[t] = rows
    # R23 · R24 · R25
    for c in S.conflicts:
        if c.get("target_id"):
            tt = c["target_type"] if c["target_type"] in ENTITY_TYPES else None
            if tt:
                S.edge("R23", "conflict", c["id"], tt, c["target_id"], [], {}, derived_from=c["stable_key"]["locators"])
    erd_refs = {x["target"].get("erd_ref") for x in S.ctx["erd"]["decisions"]}
    skipped_erd = []
    for d in S.ctx["decisions_approved"]:
        tgt = d["target"]
        for k, tt in (("catalog_item_id", "catalog_item"), ("from_ref", None), ("ref_id", "reference")):
            v = tgt.get(k)
            if isinstance(v, str) and v.startswith("CAT-") and v in S.E["catalog_item"]:
                S.edge("R24", "decision", d["id"], "catalog_item", v, [], {}, derived_from=[d["id"]])
        if tgt.get("erd_ref"):
            if tgt["erd_ref"] in erd_refs:
                S.edge("R24", "decision", d["id"], "erd", tgt["erd_ref"], [], {}, derived_from=[d["id"]])
            elif d["id"] not in skipped_erd:
                skipped_erd.append(d["id"])
        if tgt.get("conflict_key"):
            for c in S.conflicts:
                if c["stable_key"] == tgt["conflict_key"]:
                    S.edge("R24", "decision", d["id"], "conflict", c["id"], [], {}, derived_from=[d["id"]])
        if tgt.get("dictionary"):
            S.edge("R24", "decision", d["id"], "dictionary", tgt["dictionary"], [], {}, derived_from=[d["id"]])
        if d["kind"] == "product_reclassify":   # v3.1 — 끝은 새 PRD-(옛 id 는 alias)
            nid = next((x.get("new_id") for x in S.apply_log if x["id"] == d["id"] and x.get("result") == "applied"), None)
            if nid and nid in S.E["product"]:
                S.edge("R24", "decision", d["id"], "product", nid, [], {}, derived_from=[d["id"]])
        if d["kind"] == "phrase_map":   # v3.1 — 끝은 문구 사전 항목(PHR-)
            pid = next((x.get("phrase_id") for x in S.apply_log if x["id"] == d["id"] and x.get("result") == "applied"), None)
            if pid:
                S.edge("R24", "decision", d["id"], "dictionary", pid, [], {}, derived_from=[d["id"]])
    if skipped_erd:
        S.note("R24 erd 끝", f"scope_review {len(skipped_erd)} 건({', '.join(skipped_erd)})의 target.erd_ref 가 ERD 결정 레코드의 erd_ref 가 아니다(§12 `/` 같은 ERD 본문 자리) — erd 노드가 없어 R24 엣지를 만들지 않았다(기록만 kind · 결정 레코드는 decision.jsonl 에 있음)")
    src_id = {s["file"]: mkid("SRC", s["sha256"]) for s in S.ctx["erd"]["source_files"]}
    for t in ENTITY_TYPES:
        for r in recs[t]:
            byf = defaultdict(list)
            for p in r["provenance"]:
                byf[p["file"]].append(p)
            for f, ps in sorted(byf.items()):
                S.edge("R25", t, r["id"], "source_file", src_id[f], [], {"paths": {"value": sorted({p["path"] for p in ps}), "derived_from": sorted({loc(p) for p in ps})},
                                                                          "record_locators": {"value": sorted({p["rec"] for p in ps}), "derived_from": sorted({loc(p) for p in ps})}}, derived_from=sorted({loc(p) for p in ps}))
    for t, rows in recs.items():
        write_jsonl(os.path.join(out_dir, "entities", f"{t}.jsonl"), rows)
    edges = {}
    rels = relations_of(S.ctx["erd"])
    for rel in rels:
        es = S.R.get(rel, [])
        for e in es:
            e["provenance"] = sorted(e["provenance"], key=lambda p: (p["file"], p["path"], p["rec"]))
            e["derived_from"] = sorted(set(e["derived_from"]))
        es = sorted(es, key=lambda e: (e["from"]["type"], str(e["from"]["id"]), e["to"]["type"], str(e["to"]["id"]), dumps(e["provenance"]), dumps(e["attrs"])))
        edges[rel] = es
        write_jsonl(os.path.join(out_dir, "relations", f"{rel}.jsonl"), es)
    unknown = sorted(set(S.R) - set(rels))
    if unknown:
        raise AssertionError(f"모르는 관계: {unknown}")
    # 사전(결정 ① 반영 후 + ⑦ 제외 표시)
    dic = json.loads(json.dumps(S.ctx["dic"], ensure_ascii=False))
    for x in S.ctx.get("excluded_dict_values", []):
        for d in dic["dictionaries"]:
            if d["name"] == x.get("dictionary"):
                for e in d["entries"]:
                    if norm(e["canonical"]) == norm(x.get("canonical")):
                        e["excluded"] = {"decision_id": x["decision_id"]}
    pd = next((d for d in dic["dictionaries"] if d["name"] == "phrase_dictionary"), None)
    if pd is not None:
        pj = phrase_dictionary_json(S)
        pd.update(pj)
        live = next((d for d in S.ctx["dic"]["dictionaries"] if d["name"] == "phrase_dictionary"), None)
        if live is not None:
            S.ctx["dic"] = dict(S.ctx["dic"], dictionaries=[dict(d, **pj) if d is live else d for d in S.ctx["dic"]["dictionaries"]])   # 결정 뒤 문구 사전(보고·커버리지가 읽는다 · 원 사전 객체는 그대로)
    write_json(os.path.join(out_dir, "dictionaries.json"), dic)
    # 충돌
    write_jsonl(os.path.join(out_dir, "conflicts.jsonl"), [OrderedDict((k, c[k]) for k in c) for c in sorted(S.conflicts, key=lambda c: (c["rule_ref"], c["kind"], c["id"]))])
    if S.excluded:
        write_jsonl(os.path.join(out_dir, "excluded.jsonl"), sorted(S.excluded, key=dumps))
    gc = write_gate(S, out_dir)
    gate_counts_holder.update(gc)
    return recs, edges


# ---------------------------------------------------------------------------
def phrase_dictionary_json(S):
    """v3.1(V3.1-10) 문구 사전 — 결정(phrase_map · 옛 표현 지정) 뒤 상태 · ERD erd_build_v31.phrase_dictionary_json 과 같은 모양(+ ledger_locators · decision_ids · mapped)."""
    AU = S.ctx["AU"]
    entries = []
    for pid, e in AU.phrases.items():
        srcs = Counter()
        for lc in e["locators"] + [tr["locator"] for tr in e.get("translations", [])]:
            f, rest = lc.split(":", 1)
            srcs[(f, rest.split("@", 1)[0])] += 1
        for acc in e.get("accuracy", []):   # 문헌 정확도 메타(항목 accuracy[] · 그 레코드의 잎)
            for k, fld in (("score", "accuracy_score"), ("note", "accuracy_note"), ("added_at", "added_at")):
                if acc.get(k) is not None:
                    srcs[("literature-evidence.json", f"categories.{{code}}.adverse_effects[].{fld}")] += 1
        cands = []
        for c in e["candidates"]:
            c2 = dict(c)
            if c2.get("unit_id") and c2["unit_id"] not in AU.units:
                c2["unit_id"] = None
                c2["exists"] = False
            cands.append(c2)
        x = OrderedDict([("id", pid), ("canonical", e["normalized"]), ("normalized", e["normalized"]), ("raw_variants", e["raw_variants"]), ("kinds", e["kinds"]), ("langs", e["langs"]), ("locators", e["locators"]),
                         ("ledger_locators", [AU.ctx_loc(c) for c in e["contexts"]]), ("modality_codes", e["modality_codes"]),
                         ("sources", [{"file": f, "path": p, "n": n, "kind": "phrase"} for (f, p), n in srcs.items()]), ("synonyms", []), ("definition", None),
                         ("status", e["status"]), ("reasons", e["reasons"]), ("units", e["units"]), ("created_units", [u for u in e["created_units"] if u in AU.units]), ("candidates", cands), ("parsed", e["parsed"]),
                         ("unregistered", e["unregistered"]), ("translations", e["translations"]), ("citations", e["citations"]), ("accuracy", e["accuracy"])])
        if e.get("decision_ids"):
            x["decision_ids"] = list(e["decision_ids"])
            x["mapped_by"] = e.get("mapped_by")
            x["mapped_courses"] = e.get("mapped_courses")
        if S.ctx.get("is33") and e.get("why") is not None:
            x["why"] = e["why"]   # v3.3: 메모·설명문·문장꼴(b)·애매의 까닭(analyzer: sentence_b | ambiguous | predicate · judge_phrase 는 why 목록)
        entries.append(x)
    return {"canonical_count": len(entries), "entries": entries, "by_status": dict(Counter(e["status"] for e in entries)), "occurrences": sum(len(e["locators"]) for e in entries)}


def write_gate(S, out_dir):
    g = os.path.join(out_dir, "gate")
    cs = S.conflicts
    # ⑨
    unres = [c for c in cs if c["kind"] == "unresolved_reference"]
    rows = []
    for c in sorted(unres, key=lambda c: (c.get("slot") or "", c.get("label") or "", c["id"])):
        rows.append(OrderedDict([("conflict_id", c["id"]), ("status", c["status"]), ("relation", c.get("relation")), ("slot", c.get("slot")), ("label", c.get("label")), ("hint", c.get("hint")),
                                 ("reason", c.get("reason")), ("fragments", c.get("fragments")), ("partial", c.get("partial")), ("candidates", c.get("candidates")), ("ref_id", c.get("ref_id")),
                                 ("locators", c["stable_key"]["locators"]), ("stable_key", c["stable_key"])]))
    write_json(os.path.join(g, "unresolved_references.json"), rows)
    md = ["# 미해결 참조(⑨ unresolved_reference) — 자리별", "", f"총 {len(rows)} 행 · 후보는 사전 일치(정규화 완전 일치)·§1.3 계열 밖 모호만 — 추정 없음 · 결정 kind: tuple_assign(_multi) · dictionary_add · conflict_close(needs_source)", ""]
    byslot = defaultdict(list)
    for r in rows:
        byslot[r["slot"]].append(r)
    for slot in sorted(byslot):
        md.append(f"## {slot} ({len(byslot[slot])})")
        md.append("")
        md.append(md_table(["#", "참조 문자열", "힌트", "사유", "미등록 조각", "닿은 조각(partial)", "후보(≤3 · 근거)", "위치 수"],
                           [(i + 1, r["label"], r["hint"] or "—", r["reason"], ", ".join(r["fragments"] or []) or "—", ", ".join(r["partial"] or []) or "—",
                             "; ".join(f"{f}→" + ", ".join(f"{x.get('dictionary', '')}:{x.get('canonical', x.get('fragments', ''))}({x.get('basis')})" for x in v) for f, v in (r["candidates"] or {}).items() if v) or "없음",
                             len(r["locators"])) for i, r in enumerate(byslot[slot])]))
        md.append("")
    write_text(os.path.join(g, "unresolved_references.md"), "\n".join(md))
    # ⑧
    unreg = [c for c in cs if c["kind"] == "unregistered_value"]
    prop_by = S.ctx.get("proposal_by_fragment", {})
    rows8 = []
    for c in sorted(unreg, key=lambda c: (c.get("axis") or "", -(c.get("count") or 0), str(c.get("fragment")))):
        rows8.append(OrderedDict([("conflict_id", c["id"]), ("status", c["status"]), ("axis", c.get("axis")), ("fragment", c.get("fragment")), ("count", c.get("count")), ("where", c.get("where")),
                                  ("axis_candidates", c.get("axis_candidates")), ("proposal", prop_by.get((c.get("axis"), c.get("fragment")))), ("locators", c["stable_key"]["locators"])]))
    write_json(os.path.join(g, "unregistered_fragments.json"), rows8)
    md = ["# 미등록 조각(⑧ unregistered_value)", "", f"총 {len(rows8)} 행(축별 distinct 조각 하나 = 행 하나 · 사전 밖 값 포함). 축 후보 = 사전 46 정규화 완전 일치만(근거 포인터) — 추정 없음.", ""]
    for ax in sorted({r["axis"] for r in rows8}):
        rr = [r for r in rows8 if r["axis"] == ax]
        md.append(f"## {ax} ({len(rr)} · 총 {sum(r['count'] for r in rr)})")
        md.append("")
        md.append(md_table(["#", "조각", "횟수", "등장 자리(횟수)", "축 후보(사전 일치)", "결정 묶음 1"],
                           [(i + 1, r["fragment"], r["count"], " · ".join(f"{k}×{v}" for k, v in sorted(r["where"].items(), key=lambda x: -x[1])[:4]),
                             ", ".join(f"{x['dictionary']}:{x['canonical']}" for x in r["axis_candidates"] or []) or "—", r["proposal"] or "—") for i, r in enumerate(rr)]))
        md.append("")
    write_text(os.path.join(g, "unregistered_fragments.md"), "\n".join(md))
    # 문구 사전 unlinked(V3.1-10 · 게이트 unlinked_phrases — 조각·후보 보존 · 결정 phrase_map 의 재료)
    AU = S.ctx["AU"]
    rowsx = []
    for pid, e in AU.phrases.items():
        if e["status"] != "unlinked":
            continue
        rowsx.append(OrderedDict([("phrase_id", pid), ("normalized", e["normalized"]), ("raw_variants", e["raw_variants"]), ("kinds", e["kinds"]), ("locators", e["locators"]),
                                  ("ledger_locators", [AU.ctx_loc(c) for c in e["contexts"]]), ("reasons", e["reasons"]), ("unregistered", e["unregistered"]),
                                  ("candidates", [{k: c.get(k) for k in ("event", "site", "qualifier", "courses", "exists", "would_be_id")} for c in e["candidates"]]),
                                  ("extra_sites", e.get("extra_sites")), ("extra_courses", e.get("extra_courses")), ("extra_qualifiers", e.get("extra_qualifiers")), ("phrase_shape", e["parsed"]["phrase_shape"])]))
    write_json(os.path.join(g, "unlinked_phrases.json"), rowsx)
    nloc = sum(len(r["locators"]) for r in rowsx)
    md = ["# 문구 사전 unlinked(게이트 unlinked_phrases · V3.1-10)", "", f"항목 {len(rowsx)} · 문구 자리 {nloc} — 원칙 D: 미등록 조각이 섞인 문구는 단위를 만들지 않는다. 결정 phrase_map 의 재료(candidates · 미등록 조각).", "",
          md_table(["kind", "항목", "사유(항목 · 중복 셈)"], [(k, n, ", ".join(f"{a}={b}" for a, b in Counter(x for r in rowsx if k in r["kinds"] for x in r["reasons"]).most_common())) for k, n in Counter(k for r in rowsx for k in r["kinds"]).most_common()]), "",
          md_table(["#", "PHR-", "정규화형", "표면형(첫)", "자리", "사유", "미등록 조각", "후보(event, site, qualifier · 있음?)"],
                   [(i + 1, r["phrase_id"], r["normalized"][:40], r["raw_variants"][0][:60], len(r["locators"]), ",".join(r["reasons"]), ", ".join(r["unregistered"])[:60] or "—",
                     " · ".join(f"({c['event']},{c['site'] or 'none'},{c['qualifier'] or 'none'}{'·있음' if c['exists'] else ''})" for c in r["candidates"]) or "—") for i, r in enumerate(rowsx)])]
    write_text(os.path.join(g, "unlinked_phrases.md"), "\n".join(md))
    # 항목 자신 시술
    rowsc, others = [], Counter()
    for tid, r in sorted(S.E["procedure"].items()):
        if r["attrs"]["what_kind"][0]["value"] == "catalog_item":
            cat = S.E["catalog_item"].get(r["attrs"]["what_id"][0]["value"])
            if r["attrs"]["status"][0]["value"] != "partial" or "catalog_item" not in r["attrs"]["origins"][0]["value"]:
                others[(r["attrs"]["status"][0]["value"], ",".join(r["attrs"]["origins"][0]["value"]))] += 1
                continue
            rowsc.append(OrderedDict([("procedure_id", tid), ("catalog_item_id", r["attrs"]["what_id"][0]["value"]), ("name", cat["attrs"]["name"][0]["value"] if cat else None),
                                      ("family", cat["attrs"]["family_code"][0]["value"] if cat else None), ("status", r["attrs"]["status"][0]["value"]), ("candidate_name", r["attrs"]["candidate_name"][0]["value"]),
                                      ("extra_primaries", r["attrs"]["extra_primaries"][0]["value"]), ("extra_sites", r["attrs"]["extra_sites"][0]["value"])]))
    rowsc.sort(key=lambda r: (r["family"] or "", r["name"] or ""))
    write_json(os.path.join(g, "catalog_partial.json"), rowsc)
    md = ["# 항목 자신이 시술인 분류 항목(what_kind=catalog_item · status=partial)", "", f"총 {len(rowsc)} — 이름 조각에 미등록이 있어 항목 자신이 what · candidate_name = 미등록 조각(사전 추가는 dictionary_add · 지정은 tuple_assign). "
          + "같은 what_kind=catalog_item 이지만 partial 이 아닌 튜플(목록 밖): " + (", ".join(f"{k[0]}[{k[1]}]={v}" for k, v in sorted(others.items())) or "없음"), "",
          md_table(["#", "계열", "항목", "상태", "candidate_name", "닿은 primary(extra)"], [(i + 1, r["family"], r["name"], r["status"], ", ".join(r["candidate_name"]) or "—", ", ".join(r["extra_primaries"]) or "—") for i, r in enumerate(rowsc)])]
    write_text(os.path.join(g, "catalog_partial.md"), "\n".join(md))
    # 충돌 md
    dup = [c for c in cs if c["kind"] == "duplicate_candidate"]
    openv = [c for c in cs if c["kind"] == "value_conflict" and c["status"] == "open"]
    auto = [c for c in cs if c["status"] == "auto_resolved_by_trust"]
    md = ["# 충돌 — open · auto_resolved 요약", "", md_table(["kind", "rule", "status", "건"], [(k[0], k[1], k[2], n) for k, n in sorted(Counter((c["kind"], c["rule_ref"], c["status"]) for c in cs).items())]), "",
          f"## ⑥ value_conflict open ({len(openv)})", "", md_table(["#", "대상", "필드", "값(출처 · 순위)", "규칙"], [(i + 1, f"{c['target_type']}:{c['target_id'] or '-'}", c["field"], " ‖ ".join(f"{str(v['value'])[:50]} [{v['source_file']}:{v['source_path']}@{v['rec']} · {v['trust_tier']}]" for v in c["values"][:4]), c["resolution_rule"]) for i, c in enumerate(sorted(openv, key=lambda c: (c['target_type'], c['field'], c['id'])))]), "",
          f"## ⑦ duplicate_candidate ({len(dup)})", "", md_table(["#", "대상", "필드", "표면형(출처)", "규칙"], [(i + 1, c["target_type"], c["field"], " ‖ ".join(f"{v['value']} [{v['source_file']}]" for v in c["values"][:6]) + (" …" if len(c["values"]) > 6 else ""), c["resolution_rule"]) for i, c in enumerate(sorted(dup, key=lambda c: (c['target_type'], c['field'])))]), "",
          f"## ④ auto_resolved_by_trust ({len(auto)})", "", md_table(["#", "대상", "필드", "채택 값", "값(출처 · 순위)"], [(i + 1, f"{c['target_type']}:{c['target_id']}", c["field"], str(c["chosen_value"])[:60], " ‖ ".join(f"{str(v['value'])[:40]} [{v['source_file']} · {v['trust_tier']}]" for v in c["values"])) for i, c in enumerate(auto)]), "",
          "⑧ 미등록·사전 밖 값 → `unregistered_fragments.md` · ⑨ 미해결 참조 → `unresolved_references.md`"]
    write_text(os.path.join(g, "conflicts.md"), "\n".join(md))
    return {"unresolved_references": len(rows), "unregistered_fragments": len(rows8), "unlinked_phrases": len(rowsx), "unlinked_phrase_locators": nloc, "catalog_partial": len(rowsc), "conflicts_md_duplicate": len(dup), "conflicts_md_open_value": len(openv), "conflicts_md_auto": len(auto)}
