#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""실버 빌더 — 동결 ERD v3.1(2026-11-05 · ERD-FROZEN v3.1 절).

python3 build.py --bronze <원장 21 디렉토리> --erd ../erd-v3.1.json --dict ../erd-v3.1-dictionaries.json --decisions decisions/ --out out/
  [--step1 ../step1-products.json] [--colmap ../erd-v3.1-column-map.md] [--tuples ../erd-v3.1-tuples.json] [--tuples-prev ../erd-v3-tuples.json]
  [--bootstrap]  decisions/_bootstrap/ 를 ERD 의 approved 결정으로 (다시) 쓴다
  [--propose]    decisions/proposed/ 에 결정 묶음 1 제안을 쓴다(이미 approved/rejected 로 바뀐 파일은 덮지 않는다)
  [--propose4]   decisions/batch4-proposed/ 에 결정 묶음 4(동의어) 제안을 쓴다(게이트 옵션마다 · 같은 규칙)

표준 라이브러리만. 재실행 = out/ 바이트 동일(빌드 시각은 표준 출력에만).
"""
import argparse
import json
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lib import pipeline  # noqa: E402
from lib.load import BuildRefused, load_json  # noqa: E402
from lib.proposals import product_proposals, synonym_proposals, templates  # noqa: E402
from lib.gate3 import build_gate_3  # noqa: E402
from lib.gate4 import build_gate_4, write_proposals  # noqa: E402
from lib.gate5 import build_gate_5  # noqa: E402
from lib.gate5r import build_reduced  # noqa: E402
from lib.report import write_all  # noqa: E402
from lib.reportmd import compare, manifest, report, fifth_build_section, fourth_build_section, second_build_section, third_build_section, sixth_build_section, seventh_build_section  # noqa: E402
from lib.util import write_json, write_text, md_table  # noqa: E402

ERD_DIR = os.path.dirname(HERE)


def parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bronze", default=os.path.join(ERD_DIR, "bronze", "phub-ledger"))  # 원장의 집(2판~) · 1판 = /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26
    ap.add_argument("--step1", default=os.path.join(ERD_DIR, "step1-products.json"))
    ap.add_argument("--erd", default=os.path.join(ERD_DIR, "erd-v3.3.json"))
    ap.add_argument("--dict", default=os.path.join(ERD_DIR, "erd-v3.3-dictionaries.json"))
    ap.add_argument("--colmap", default=os.path.join(ERD_DIR, "erd-v3.3-column-map.md"))
    ap.add_argument("--tuples", default=os.path.join(ERD_DIR, "erd-v3.3-tuples.json"))
    ap.add_argument("--tuples-prev", default=os.path.join(ERD_DIR, "erd-v3.2-tuples.json"), help="이전 판 실측(v3) — 참조 구현 adverse summary 의 v3 대조 키(v3_comparison · 수식어 표 v3_unregistered)를 같은 값으로 만든다")
    ap.add_argument("--kiwi-cache", default=os.path.join(HERE, "cache", "kiwi-cache.json"), help="v3.3 분석기(kiwipiepy) 결과 정본 캐시(판 + 등록 사전 해시 + 문구) — 빌드가 읽은 항목은 out/kiwi-cache.json 으로도 쓴다")
    ap.add_argument("--kiwi-python", default=os.path.join(HERE, ".venv-kiwi", "bin", "python"), help="kiwipiepy 0.24 가 있는 인터프리터(캐시에 없는 문구가 있을 때만 부른다)")
    ap.add_argument("--repro7", default=os.path.join(HERE, "baseline", "manifest-7차-repro.json"), help="7차 재현 빌드(v3.2 · 원장 2판 · 8차 lib)의 manifest — 있으면 report §16 에 determinism key 대조를 적는다")
    ap.add_argument("--decisions", default=os.path.join(HERE, "decisions"))
    ap.add_argument("--seeds", default=os.path.join(ERD_DIR, "erd-v3.2-seed-candidates.json"), help="ERD v3.2 사전 씨앗 후보(승인용) — 게이트 5 씨앗 묶음")
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    ap.add_argument("--baseline", default=os.path.join(HERE, "baseline", "manifest-1차.json"), help="1차 manifest — 있으면 report.md 에 2차 대조 절")
    ap.add_argument("--bootstrap", action="store_true")
    ap.add_argument("--propose", action="store_true")
    ap.add_argument("--propose5-rules", action="store_true", help="decisions/batch5-rule/ 에 규칙 자동 결정(proposed · decided_by=rule:<id>)을 쓴다(사람이 바꾼 파일은 덮지 않는다)")
    ap.add_argument("--propose4", action="store_true", help="decisions/batch4-proposed/ 에 결정 묶음 4(동의어) 제안 파일을 쓴다(게이트 out/gate/batch4.json 옵션마다 · status 가 proposed 가 아닌 파일은 덮지 않는다)")
    return ap.parse_args()


def write_bootstrap(args):
    erd = load_json(args.erd)
    d = os.path.join(args.decisions, "_bootstrap")
    os.makedirs(d, exist_ok=True)
    n = 0
    for i, rec in enumerate(erd["decisions"]):
        if rec["status"] != "approved":
            continue
        r = dict(rec)
        r["erd_pointer"] = f"{os.path.basename(args.erd)}#/decisions/{i}"
        write_json(os.path.join(d, f"{rec['id']}.json"), r)
        n += 1
    return n


def safe_write_proposal(path, rec):
    if os.path.exists(path):
        cur = load_json(path)
        if cur.get("status") != "proposed":
            return "kept(status=" + str(cur.get("status")) + ")"
    write_json(path, rec)
    return "written"


def main():
    args = parse()
    t0 = time.time()
    if args.bootstrap:
        print(f"_bootstrap: {write_bootstrap(args)} 건")
    try:
        S = pipeline.run(args)
    except BuildRefused as e:
        print(f"빌드 거부: {e}", file=sys.stderr)
        sys.exit(2)
    # 결정 묶음 1 제안
    prods, excluded = product_proposals(S)
    syns, notp = synonym_proposals(S)
    tpls = templates()
    pb = {}
    for p in syns:
        for f in p["new_value"]["synonyms"] or [p["new_value"]["canonical"]]:
            pb[("procedure", f)] = p["id"]
    for x in notp:
        pb.setdefault(("procedure", x["fragment"]), "제안 안 함: " + x["why"][:60])
    S.ctx["proposal_by_fragment"] = pb
    if args.propose:
        pd = os.path.join(args.decisions, "proposed")
        os.makedirs(pd, exist_ok=True)
        res = {}
        keep = {f"{p['id']}.json" for p in prods + syns} | {os.path.join("templates", f"{slug}.json") for slug, _ in tpls}
        for root, _, fs in os.walk(pd):
            for f in fs:
                rel = os.path.relpath(os.path.join(root, f), pd)
                if f.endswith(".json") and not f.startswith("_") and rel not in keep and load_json(os.path.join(root, f)).get("status") == "proposed":
                    os.remove(os.path.join(root, f))
        for p in prods + syns:
            res[p["id"]] = safe_write_proposal(os.path.join(pd, f"{p['id']}.json"), p)
        for slug, t in tpls:
            res[t["id"]] = safe_write_proposal(os.path.join(pd, "templates", f"{slug}.json"), t)
        write_json(os.path.join(pd, "_excluded_step1_products.json"), excluded)
        write_json(os.path.join(pd, "_not_proposed_fragments.json"), notp)
        idx = ["# 결정 묶음 1 — 제안(status=proposed · 빌드가 읽지 않음)", "",
               "승인: 파일의 status 를 approved 로, decided_by·decided_at 을 채운다(id 는 그대로 써도 된다). 빌드는 decisions/ 아래 approved 만 적용한다.", "",
               md_table(["id", "kind", "사전", "정준값", "동의어", "근거 locator 수"], [(p["id"], p["kind"], p["target"]["dictionary"], p["new_value"]["canonical"], ", ".join(p["new_value"]["synonyms"]), len(p["source_refs"])) for p in prods + syns]),
               "", f"제외(제품) {len(excluded)} → `_excluded_step1_products.json` · 제안 안 한 조각 {len(notp)} → `_not_proposed_fragments.json` · 빈 템플릿 {len(tpls)} → `templates/`"]
        write_text(os.path.join(pd, "_INDEX.md"), "\n".join(idx))
    # 산출물
    if os.path.isdir(args.out):
        shutil.rmtree(args.out)
    os.makedirs(args.out)
    gc = {}
    recs, edges = write_all(S, args.out, None, gc)
    cmp_rows = compare(S, args.tuples)
    write_json(os.path.join(args.out, "erd_comparison.json"), cmp_rows)
    nh = report(S, recs, edges, cmp_rows, gc, {"products": prods, "excluded": excluded, "synonyms": syns, "not_proposed": notp, "templates": tpls}, args.out)
    # 결정 묶음 2B 게이트는 3차 고정본(decisions/batch2b-answers/_gate-batch2b-3차.json)으로 답이 끝났다 — 6차(v3.1)부터 다시 만들지 않는다
    g3 = build_gate_3(S, args.out)  # 결정 묶음 3 게이트 자료(out/gate/batch3.json · .md — batch3-proposed)
    g4 = build_gate_4(S, args.out)  # 결정 묶음 4 게이트 자료(out/gate/batch4.json · .md — 동의어 제안)
    g5 = build_gate_5(S, args.out, args.seeds) if (S.ctx.get("is32") and not S.ctx.get("is33")) else None   # 결정 묶음 5(v3.2 노드 단위 · out/gate/batch5.json · .md · batch5-weak.json)
    S.ctx["gate5"] = g5
    g5r = None  # 축소본 생성 비활성(사용자 「되돌려」 2026-11-05)
    S.ctx["gate5r"] = g5r
    g6 = None
    if S.ctx.get("is33"):
        from lib.gate6 import build_gate_6
        from lib.util import write_json as _wj
        _wj(os.path.join(args.out, "kiwi-cache.json"), S.ctx["analyzer"].used_dump())   # 분석기 캐시 산출(이번 빌드가 읽은 항목만 · 재실행 바이트 동일)
        g6 = build_gate_6(S, args.out)   # 결정 묶음 6(v3.3 · out/gate/batch6.json · .md · batch6-weak.json)
    S.ctx["gate6"] = g6
    if args.propose4:
        g4["proposals_written"] = write_proposals(S, S.ctx["gate4_items"], args.decisions)  # decisions/batch4-proposed/
    m = manifest(S, args, recs, edges, cmp_rows, gc, args.out)
    if any(d["id"].startswith("DEC-2026-11-04-B1") for d in S.ctx["decisions_approved"]):
        second_build_section(S, args.out, args.baseline, m)
        m = manifest(S, args, recs, edges, cmp_rows, gc, args.out)
    if any(d["id"].startswith("DEC-2026-11-04-B2A") for d in S.ctx["decisions_approved"]):
        third_build_section(S, args.out, os.path.dirname(args.baseline), m)
        m = manifest(S, args, recs, edges, cmp_rows, gc, args.out)
    if any(d["id"].startswith("DEC-2026-11-04-B2B") for d in S.ctx["decisions_approved"]):
        fourth_build_section(S, args.out, os.path.dirname(args.baseline), m)
        m = manifest(S, args, recs, edges, cmp_rows, gc, args.out)
    if any(d["id"].startswith("DEC-2026-11-05-B3") for d in S.ctx["decisions_approved"]):
        fifth_build_section(S, args.out, os.path.dirname(args.baseline), m)
        m = manifest(S, args, recs, edges, cmp_rows, gc, args.out)
    if S.ctx["erd"].get("erd_version") in ("v3.1", "v3.2", "v3.3"):
        sixth_build_section(S, args.out, os.path.dirname(args.baseline), m, g4)   # v3.2 빌드는 6차 절(baseline/report-14-6차.md)을 그대로 붙인다
        m = manifest(S, args, recs, edges, cmp_rows, gc, args.out)
    if S.ctx["erd"].get("erd_version") == "v3.2":
        seventh_build_section(S, args.out, os.path.dirname(args.baseline), m, g5)
        m = manifest(S, args, recs, edges, cmp_rows, gc, args.out)
    if S.ctx["erd"].get("erd_version") == "v3.3":
        from lib.report8 import eighth, frozen_section
        frozen_section(args.out, os.path.dirname(args.baseline), "report-15-7차.md")   # 7차 절은 7차 빌드가 쓴 그대로(기록 보존)
        eighth(S, args.out, os.path.dirname(args.baseline), m, g6, args)
        m = manifest(S, args, recs, edges, cmp_rows, gc, args.out)
    print(json.dumps({"entities": m["counts"]["entities"], "relations": m["counts"]["relations"], "gate": gc, "erd_diff": m["erd_comparison"], "proposals": {"products": len(prods), "synonyms": len(syns), "templates": len(tpls)}, "hold": nh, "gate_3": g3, "gate_4": g4, "gate_5": g5, "gate_5_reduced": g5r, "gate_6": g6,
                      "analyzer": S.ctx["analyzer"].stats() if S.ctx.get("analyzer") else None}, ensure_ascii=False))
    print(f"빌드 {time.time() - t0:.1f}s · out={args.out}")


if __name__ == "__main__":
    main()
