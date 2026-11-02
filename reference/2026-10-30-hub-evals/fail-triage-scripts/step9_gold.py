#!/usr/bin/env python3
"""step9_gold — SPEC-005 v3.4 §6-8 (b) (c) (d) (e) · (k) 셈(WORK-010 · 결정론 · 읽기만).

(e) 판정 식은 `step9-effect.py` 와 같은 식을 **여기에 다시 적는다**(import 안 함) — 정규화 = recheck2 `norm` 과 같음 · 인용 ⊂ 원문.
다만 9단계 레코드 대신 **골드 export 의 fact 원문**을 쓴다: ① `#step9[` fact → 「실버 9단계로 닫힘」 ② 값 사전 전역 fact(`scope:all#…#value_dictionary[`) →
「값 사전(시맨틱 · 골드 globals)」 ③ section_map 이 가리키는 8단계 fact(CX 관리 · 예방 이동 · SE 잎 새 fact)가 그 section 으로 export 에 있고 인용이 그 원문 안 →
「골드 section 으로(실버 변경 없음)」 ④ ② 의 alternatives 레코드 원문에만(골드 안 나감) → 「alternatives 에만(골드 안 나감)」 ⑤ 그 밖 「안 닫힘」.
옛 export(b031371c)로 돌리면 기준선(9단계 fact 0 · section 이동 없음 → 닫힘 0).

입력(읽기만): `$W/step9-explanations.json` · `$W/step9-research.json`(A2_rows 54 · A5_rows 30 — step9-effect 와 같은 행 · 인용) · gold-export(새 · 옛)
            · (k) runs/runs.jsonl batch b202611011627-a76c8e(rerun-v5a) case3 I-04 판의 시작 노드 → 허브 expand(in-process 또는 --base-url).
출력: build-out/step9-gold/step9-gold-report[.<label>].{md,json} · (k) step9-gold-k.<label>.json — 시간 칸 없음(두 번 바이트 같음).

  facts --export NEW [--old-export OLD] [--label L]                 (b) (c) (d) (e) — 허브 안 부름
  k (--inprocess | --base-url URL) --label {v33,v34,v34m}            (k) 한 판 — v33 · v34: S = side_effects + complications · v34m: S + safety.management
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import recheck2 as R  # noqa: E402 — 허브 호출(rest_call · inprocess_client) 만

E = R.E
W = Path("/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend")
OUT = E / "build-out" / "step9-gold"
OLD_EXPORT = OUT / "gold-export.b031371c4c69cea1.json"
V5A = "b202611011627-a76c8e"
K_SECTIONS = {"v33": ["safety.side_effects", "safety.complications"], "v34": ["safety.side_effects", "safety.complications"],
              "v34m": ["safety.side_effects", "safety.complications", "safety.management"]}
MGMT = re.compile(r"#(management|prevention)(\[\d+\])?$")
PROC = ("unit_procedure:", "product:", "family:")


def norm(s: Any) -> str:
    return re.sub(r"[\s\W_]+", "", str(s).lower())


def load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def se_cx_fact_id(sm: dict[str, Any]) -> str:
    """section_map 행 → 8단계 fact id(`{CX|SE id}#{칸}` · 배열은 `#{칸}[i]`) — 원천 경로의 `complications[k].` 뒤 꼬리."""
    m = re.search(r"\.complications\[\d+\]\.(.+)$", sm["path"])
    return f"{sm['silver_id']}#{m.group(1) if m else sm['field']}"


# ── (b) (c) (d) (e) ────────────────────────────────────────────────────────────
def facts_report(new: dict[str, Any], old: dict[str, Any], s9: dict[str, Any], rs: dict[str, Any]) -> dict[str, Any]:
    nodes = {n["id"] for n in new["nodes"]}
    facts = {f["id"]: f for f in new["facts"]}
    old_facts = {f["id"]: f for f in old["facts"]}
    rec = {r["id"]: r for r in s9["records"]}

    # (b) step9 fact ↔ node_slots emit(정본 노드 쪽)
    want: dict[str, str] = {}
    skipped: collections.Counter[str] = collections.Counter()
    for e in s9["node_slots"]:
        for rid, fid in zip(e["emit"], e["fact_ids"], strict=True):
            if e["node"] in nodes:
                want[fid] = rid
            else:
                skipped[e["node"]] += 1
    got = {k: v for k, v in facts.items() if "#step9[" in k}
    text_same = sum(1 for fid, rid in want.items() if fid in got and got[fid]["text"] == rec[rid]["text"])
    b = {"want": len(want), "got": len(got), "id_set_same": set(want) == set(got), "missing_head": sorted(set(want) - set(got))[:5],
         "extra_head": sorted(set(got) - set(want))[:5], "text_same": text_same, "skipped": sum(skipped.values()), "skipped_nodes": dict(sorted(skipped.items())),
         "facts_out": s9["summary"]["facts_out"], "sum_ok": len(want) + sum(skipped.values()) == s9["summary"]["facts_out"],
         "by_section": dict(sorted(collections.Counter(f["section"] for f in got.values()).items()))}

    # (c) section 별 차(새 − 옛)
    cn, co = collections.Counter(f["section"] for f in facts.values()), collections.Counter(f["section"] for f in old_facts.values())
    c = {"new_total": len(facts), "old_total": len(old_facts), "diff_total": len(facts) - len(old_facts),
         "by_section": {s: cn[s] - co[s] for s in sorted(set(cn) | set(co)) if cn[s] != co[s]},
         "moved_ids": sum(1 for k, f in facts.items() if k in old_facts and old_facts[k]["section"] != f["section"]),
         "moved_by": dict(sorted(collections.Counter(f"{old_facts[k]['section']}→{f['section']}" for k, f in facts.items()
                                                     if k in old_facts and old_facts[k]["section"] != f["section"]).items())),
         "new_ids_by_kind": dict(sorted(collections.Counter("step9" if "#step9[" in k else "value_dictionary" if "#value_dictionary[" in k else
                                                            "SE" if k.startswith("SE-") else "기타" for k in facts if k not in old_facts).items())),
         "globals_value_dictionary": sum(1 for g in new["globals"] if g["kind"] == "value_dictionary")}

    # (d) ② · alternatives
    two = [e for e in s9["node_slots"] if e.get("class") == "②"]
    two_c = [e for e in two if e["node"] in nodes]
    alt_fact_ids = {f"{e['node']}#{e['section']}#step9[{rec[a]['source']['path']}]" for e in s9["node_slots"] for a in e.get("alternatives") or []}
    alt_text_facts = sum(1 for k in alt_fact_ids if k in facts and k not in want)
    meta_alt = sum(len((f["source"].get("meta") or {}).get("alternatives") or []) for f in got.values())
    want_alt = sum(len(e.get("alternatives") or []) for e in s9["node_slots"] if e["node"] in nodes)
    resolved_in = sum(1 for e in two_c if e.get("resolved") in e["emit"] and not set(e.get("alternatives") or []) & set(e["emit"]))
    d = {"slots": len(two), "slots_canonical": len(two_c), "resolved_in_emit_alt_out": resolved_in, "alternatives_text_facts": alt_text_facts,
         "alternatives_meta": meta_alt, "alternatives_want": want_alt, "resolved_fact_present": sum(
             1 for e in two_c if e["fact_ids"][e["emit"].index(e["resolved"])] in facts)}

    # (e) A 행 닫힘(step9-effect 와 같은 분류 이름)
    E9 = [(norm(f["text"]), k) for k, f in sorted(got.items())]
    VD = [(norm(f["text"]), k) for k, f in sorted(facts.items()) if "#value_dictionary[" in k]
    smap = s9["section_map"]
    alt_txt = [(norm(rec[a]["text"]), a) for e in s9["node_slots"] for a in e.get("alternatives") or []]

    def judge(a: dict[str, Any]) -> tuple[str, str]:
        q, p = norm(a.get("quote") or ""), a.get("path") or ""
        if q:
            hit = next((k for t, k in E9 if q in t), None)
            if hit:
                return "실버 9단계로 닫힘", hit
            hit = next((k for t, k in VD if q in t), None)
            if hit:
                return "값 사전(시맨틱 · 골드 globals)", hit
            for sm in smap:
                if sm["path"] == p or sm["path"].startswith(p + ".") or sm["path"].startswith(p + "["):
                    fid = se_cx_fact_id(sm)
                    f = facts.get(fid)
                    if f and f["section"] == sm["section"] and q in norm(f["text"]):
                        return "골드 section 으로(실버 변경 없음)", fid
            hit = next((r for t, r in alt_txt if q in t), None)
            if hit:
                return "alternatives 에만(골드 안 나감)", hit
        return "안 닫힘", "라벨 · 메타 칸 또는 대상 밖"

    e_out = {}
    for key in ("A2", "A5"):
        rows = []
        for a in rs[f"{key}_rows"]:
            v, by = judge(a)
            rows.append({"no": a["no"], "case": a["case"], "item": a["item"], "path": a["path"], "verdict": v, "by": by})
        tally = collections.Counter(r["verdict"] for r in rows)
        closed = sum(n for k, n in tally.items() if k in ("실버 9단계로 닫힘", "값 사전(시맨틱 · 골드 globals)", "골드 section 으로(실버 변경 없음)"))
        e_out[key] = {"rows": len(rows), "closed": closed, "tally": dict(sorted(tally.items())), "detail": rows}
    return {"meta": {"export": new["build"]["build_hash"], "old_export": old["build"]["build_hash"], "step9": s9["version"]},
            "b_step9_facts": b, "c_sections": c, "d_alternatives": d, "e_a_rows": e_out}


# ── (k) case3 I-04 시작 노드 × expand(S) 1쪽의 관리 · 예방 줄 ───────────────────────
def k_nodes(runs_path: Path) -> list[tuple[str, str]]:
    out = []
    for ln in runs_path.open(encoding="utf-8"):
        if not ln.strip():
            continue
        d = json.loads(ln)
        if d.get("batch_id") != V5A:
            continue
        w = (d["cases"]["case3"]["trace"].get("walk") or {})
        if w.get("intent") != "I-04":
            continue
        start = w.get("start_node") or next((x for x in ((w.get("resolve") or {}).get("candidates") or []) if x.startswith(PROC)), None)
        if start:
            out.append((d["question_no"], start))
    return sorted(out)


def k_measure(base: str, client: Any, label: str, runs_path: Path) -> dict[str, Any]:
    secs = K_SECTIONS[label]
    rows, build = [], None
    for no, nid in k_nodes(runs_path):
        st, txt = R.rest_call(base, "expand", {"id": nid, "sections": secs}, client)
        if st != 200:
            rows.append({"no": no, "node": nid, "status": st, "mgmt": None})
            continue
        r = json.loads(txt)
        build = build or (r.get("build") or {}).get("build_hash")
        lines = r.get("facts") or []
        mg = [x["id"] for x in lines if MGMT.search(x["id"]) or x.get("section") == "safety.management"]
        rows.append({"no": no, "node": nid, "status": st, "lines": len(lines), "mgmt": len(mg), "mgmt_head": mg[:3]})
    return {"label": label, "sections": secs, "build_hash": build, "batch": V5A, "rows": rows,
            "nodes": len(rows), "mgmt_total": sum(x["mgmt"] or 0 for x in rows)}


def render(rep: dict[str, Any], ks: dict[str, Any], label: str) -> str:
    b, c, d, e = rep["b_step9_facts"], rep["c_sections"], rep["d_alternatives"], rep["e_a_rows"]
    L = [f"# step9-gold — SPEC-005 v3.4 §6-8 (b)~(e) · (k){' · ' + label if label else ''}", "",
         f"export `{rep['meta']['export']}` · 옛 `{rep['meta']['old_export']}` · {rep['meta']['step9']}", "",
         "## (b) step9 fact", "", f"- 기대(정본 노드 쪽 emit) {b['want']} · export `#step9[` {b['got']} · id 집합 같음 {b['id_set_same']} · 원문 같음 {b['text_same']}",
         f"- 안 실음 {b['skipped']} {b['skipped_nodes']} · 합 = facts_out({b['facts_out']}) {b['sum_ok']} · section {b['by_section']}",
         "", "## (c) section 별 차(새 − 옛)", "", f"- fact {c['old_total']} → {c['new_total']}(+{c['diff_total']}) · {c['by_section']}",
         f"- section 바뀐 id {c['moved_ids']} {c['moved_by']} · 새 id {c['new_ids_by_kind']} · globals value_dictionary {c['globals_value_dictionary']}",
         "", "## (d) ② · alternatives", "", f"- ② 칸 {d['slots']}(정본 {d['slots_canonical']}) · resolved ∈ emit · alternatives ∉ emit {d['resolved_in_emit_alt_out']} · resolved fact 있음 {d['resolved_fact_present']}",
         f"- alternatives 원문 fact {d['alternatives_text_facts']} · 메타 {d['alternatives_meta']}/{d['alternatives_want']}", "", "## (e) A 행 닫힘", ""]
    for key, title in (("A2", "2차 A"), ("A5", "rerun-v5a case3 A")):
        x = e[key]
        L += [f"### {title} — {x['rows']}행 · 닫힘 {x['closed']}", "", "| 판정 | 행 |", "|---|---|"] + [f"| {k} | {v} |" for k, v in x["tally"].items()]
        L += ["", "| 문항 | 케이스 | 경로 | 판정 | 근거 |", "|---|---|---|---|---|"]
        L += [f"| {r['no']} | {r['case']} | `{r['path']}` | {r['verdict']} | `{r['by'][:90]}` |" for r in x["detail"]]
        L.append("")
    if ks:
        L += ["## (k) case3 I-04 시작 노드 × expand(S) 1쪽의 관리 · 예방 줄", ""]
        labs = [x for x in ("v33", "v34", "v34m") if x in ks]
        L += [" · ".join(f"{x}: 빌드 `{ks[x]['build_hash']}` S={ks[x]['sections']} 합 **{ks[x]['mgmt_total']}**" for x in labs), ""]
        if {"v33", "v34m"} <= set(ks):
            L.append(f"③ ≥ ① : {ks['v34m']['mgmt_total'] >= ks['v33']['mgmt_total']}" + (f" · ② − ① = {ks['v34']['mgmt_total'] - ks['v33']['mgmt_total']}" if "v34" in ks else ""))
            L.append("")
        L += ["| 문항 | 노드 | " + " | ".join(labs) + " |", "|---|---|" + "---|" * len(labs)]
        base = ks[labs[0]]["rows"]
        for i, r in enumerate(base):
            L.append(f"| {r['no']} | {r['node']} | " + " | ".join(str(ks[x]["rows"][i]["mgmt"]) for x in labs) + " |")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)
    f = sub.add_parser("facts")
    f.add_argument("--export", type=Path, default=R.BACKEND / "build-out" / "gold-export.json")
    f.add_argument("--old-export", type=Path, default=OLD_EXPORT)
    f.add_argument("--label", default="")
    f.add_argument("--out-dir", type=Path, default=OUT)
    k = sub.add_parser("k")
    g = k.add_mutually_exclusive_group(required=True)
    g.add_argument("--inprocess", action="store_true")
    g.add_argument("--base-url")
    k.add_argument("--label", required=True, choices=sorted(K_SECTIONS))
    k.add_argument("--out-dir", type=Path, default=OUT)
    a = ap.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)
    if a.mode == "k":
        client = R.inprocess_client() if a.inprocess else None
        res = k_measure("http://127.0.0.1:18005" if a.inprocess else a.base_url.rstrip("/"), client, a.label, E / "runs" / "runs.jsonl")
        (a.out_dir / f"step9-gold-k.{a.label}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(json.dumps({k_: v for k_, v in res.items() if k_ != "rows"}, ensure_ascii=False))
        return 0
    rep = facts_report(load(a.export), load(a.old_export), load(W / "step9-explanations.json"), load(W / "step9-research.json"))
    ks = {lab: load(a.out_dir / f"step9-gold-k.{lab}.json") for lab in K_SECTIONS if (a.out_dir / f"step9-gold-k.{lab}.json").exists()}
    if ks:
        rep["k_i04"] = {lab: {kk: v for kk, v in x.items() if kk != "rows"} for lab, x in ks.items()}
    suf = f".{a.label}" if a.label else ""
    (a.out_dir / f"step9-gold-report{suf}.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (a.out_dir / f"step9-gold-report{suf}.md").write_text(render(rep, ks, a.label), encoding="utf-8")
    print(json.dumps({"b": {k_: v for k_, v in rep["b_step9_facts"].items() if not k_.endswith("head")}, "c": rep["c_sections"]["by_section"],
                      "d": rep["d_alternatives"], "e": {k_: (v["closed"], v["tally"]) for k_, v in rep["e_a_rows"].items()}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
