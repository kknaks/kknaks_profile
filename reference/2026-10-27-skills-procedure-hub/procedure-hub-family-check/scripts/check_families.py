"""계열 원장 점검 — step2-families.json 의 product_family 전수를 계열 정의 · 1단계 원장과 맞춰 본다.

읽기만 한다. 원장(step2-families.json) · 1단계 원장(step1-products.json)은 고치지 않는다 — 결과는 결정 목록의 재료다.
표준 라이브러리만 쓴다.

    python3 <이 파일> \
        --ledger orchestration/work/phub-recommend/step2-families.json \
        --products orchestration/work/phub-recommend/step1-products.json \
        --out <scratchpad>/family-check.json

본다:
- family 가 정의된 계열(families[].id) · 「계열 밖」 · null(원장님 문의) 중 하나인지 — null 이면 pending_director 여야 한다
- sub_family 가 그 계열의 하위 칸(families[].sub_families)에 있는지 · 하위 칸이 있는 계열인데 null 인 행(사유 같이)
- also_families 코드가 정의된 계열인지 · 주 계열과 겹치지 않는지
- also_sub_families 가 {family, sub_family} 객체이고, family 가 주 또는 보조 계열이며, sub_family 가 그 계열의 칸인지
- open 0 · summary 수치를 다시 센 값과 같은지
- 1단계 active 행 ↔ product_family 행 일치 — 새 행(계열 판정 필요) · 빠진 행(1단계에서 합침 · 빠짐)
- evidence_level 약 목록 · confirm_question 빈 행 · conflict 목록 · pending_director 목록 일치
- 1단계 family.code ↔ family.name 의 M 코드가 다른 행(「현재 계열」을 읽는 칸이 갈리는 행 — 기록 §5-4)

종료 코드: 오류(errors) 0 이면 0, 아니면 1.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

OUT = "계열 밖"
VERDICTS = {"맞음", "옮김", "여러", "계열 밖", "판단 필요"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ledger", required=True, help="step2-families.json")
    ap.add_argument("--products", required=True, help="step1-products.json")
    ap.add_argument("--out", help="결과 JSON 경로(없으면 stdout)")
    a = ap.parse_args()

    L = json.loads(Path(a.ledger).read_text())
    P = json.loads(Path(a.products).read_text())

    fams = {f["id"]: f for f in L["families"]}
    subs = {fid: set(f.get("sub_families") or []) for fid, f in fams.items()}
    rows = L["product_family"]
    errors: list[dict] = []

    def err(kind: str, r: dict | None, msg: str) -> None:
        errors.append({"kind": kind, "ledger_id": r and r["ledger_id"], "display_name": r and r["display_name"], "msg": msg})

    # ── 행 단위 ──
    sub_null = []
    used_subs = collections.defaultdict(set)
    for r in rows:
        fam = r["family"]
        if r.get("verdict") not in VERDICTS:
            err("verdict", r, f"판정 값 「{r.get('verdict')}」 — 허용: {sorted(VERDICTS)}")
        if fam is None:
            if not r.get("pending_director"):
                err("family_null", r, "family null 인데 pending_director 아님")
        elif fam != OUT and fam not in fams:
            err("family_code", r, f"정의 안 된 계열 「{fam}」")
        if fam == OUT and r.get("verdict") != "계열 밖":
            err("verdict", r, "family 「계열 밖」 인데 판정이 「계열 밖」 아님")

        sub = r.get("sub_family")
        if sub is not None:
            if fam not in fams:
                err("sub_family", r, f"하위 「{sub}」 가 있는데 계열이 {fam}")
            elif sub not in subs[fam]:
                err("sub_family", r, f"하위 「{sub}」 가 {fam} 의 칸이 아님 — 칸: {sorted(subs[fam])}")
            else:
                used_subs[fam].add(sub)
        elif fam in fams and subs[fam]:
            sub_null.append({"ledger_id": r["ledger_id"], "display_name": r["display_name"], "family": fam,
                             "basis": r.get("sub_family_basis")})

        also = r.get("also_families") or []
        for c in also:
            if c not in fams:
                err("also_families", r, f"보조 계열 「{c}」 정의 안 됨")
            if c == fam:
                err("also_families", r, f"보조 계열 「{c}」 가 주 계열과 같음")
        for s in r.get("also_sub_families") or []:
            if not isinstance(s, dict) or set(s) != {"family", "sub_family"}:
                err("also_sub_families", r, f"객체 {{family, sub_family}} 아님: {s!r}")
                continue
            if s["family"] != fam and s["family"] not in also:
                err("also_sub_families", r, f"보조 하위의 계열 「{s['family']}」 가 주 · 보조 계열 아님")
            elif s["family"] in fams and s["sub_family"] not in subs[s["family"]]:
                err("also_sub_families", r, f"보조 하위 「{s['sub_family']}」 가 {s['family']} 의 칸이 아님")
            else:
                used_subs[s["family"]].add(s["sub_family"])
            if s["family"] == fam and s["sub_family"] == sub:
                err("also_sub_families", r, "보조 하위가 주 하위와 같음")
        if r.get("evidence_level") == "약" and not r.get("confirm_question"):
            err("confirm_question", r, "근거 약인데 확인 질문 없음")

    ids = [r["ledger_id"] for r in rows]
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    for d in dup:
        errors.append({"kind": "duplicate", "ledger_id": d, "display_name": None, "msg": "product_family 에 두 번"})

    # ── 1단계 원장과 일치 ──
    p_items = {x["ledger_id"]: x for x in P["items"]}
    active = {k for k, x in p_items.items() if x.get("active")}
    have = set(ids)
    new_rows = [{"ledger_id": k, "display_name": p_items[k]["2_names"].get("display_name"),
                 "step1_family": p_items[k]["family"].get("name"), "status": p_items[k]["4_license"].get("status")}
                for k in sorted(active - have)]
    gone_rows = [{"ledger_id": k, "display_name": next(r["display_name"] for r in rows if r["ledger_id"] == k),
                  "step1_active": bool(p_items.get(k, {}).get("active")), "in_step1": k in p_items,
                  "merged_into": p_items.get(k, {}).get("merged_into"), "moved_to": p_items.get(k, {}).get("moved_to")}
                 for k in sorted(have - active)]

    code_name_split = []
    for k in sorted(active):
        f = p_items[k]["family"]
        m = re.match(r"^(M\d+)\b", f.get("name") or "")
        if m and f.get("code") and m.group(1) != f["code"]:
            code_name_split.append({"ledger_id": k, "display_name": p_items[k]["2_names"].get("display_name"),
                                    "step1_code": f["code"], "step1_name": f["name"]})

    # ── 목록 · 수치 ──
    weak = [{"ledger_id": r["ledger_id"], "display_name": r["display_name"], "family": r["family"],
             "sub_family": r.get("sub_family"), "confirm_question": r.get("confirm_question")}
            for r in rows if r.get("evidence_level") == "약"]
    conflicts = [{"ledger_id": r["ledger_id"], "display_name": r["display_name"], "conflict": r["conflict"]}
                 for r in rows if r.get("conflict")]
    pd_rows = {r["ledger_id"] for r in rows if r.get("pending_director")}
    pd_list = {x["ledger_id"] for x in L.get("pending_director") or []}
    if pd_rows != pd_list:
        errors.append({"kind": "pending_director", "ledger_id": None, "display_name": None,
                       "msg": f"행 표시 ↔ 최상위 목록 다름: {sorted(pd_rows ^ pd_list)}"})
    if L.get("open"):
        errors.append({"kind": "open", "ledger_id": None, "display_name": None, "msg": f"open {len(L['open'])}건 — 끝 조건은 open 0"})
    oof = {x["ledger_id"] for x in L.get("out_of_family") or []}
    oof_rows = {r["ledger_id"] for r in rows if r["family"] == OUT}
    if oof != oof_rows:
        errors.append({"kind": "out_of_family", "ledger_id": None, "display_name": None,
                       "msg": f"행 「계열 밖」 ↔ out_of_family 목록 다름: {sorted(oof ^ oof_rows)}"})

    recount = {
        "rows": len(rows),
        "verdicts": dict(collections.Counter(r["verdict"] for r in rows)),
        "open": len(L.get("open") or []),
        "pending_director": len(pd_rows),
        "evidence_weak": len(weak),
        "conflicts": len(conflicts),
        "out_of_family": len(oof_rows),
        "families": len(fams),
    }
    summ = L.get("summary") or {}
    summary_diff = {k: {"summary": summ.get(k), "recount": v} for k, v in recount.items() if summ.get(k) != v}
    if summary_diff:
        errors.append({"kind": "summary", "ledger_id": None, "display_name": None, "msg": f"summary ↔ 다시 센 값 다름: {sorted(summary_diff)}"})

    unused_subs = {fid: sorted(subs[fid] - used_subs[fid]) for fid in fams if subs[fid] - used_subs[fid]}
    by_family = collections.Counter(r["family"] if r["family"] else "family null" for r in rows)

    result = {
        "ledger": a.ledger,
        "products": a.products,
        "ok": not errors and not new_rows and not gone_rows,
        "counts": {**recount, "by_family": dict(by_family), "step1_active": len(active),
                   "new_rows": len(new_rows), "gone_rows": len(gone_rows), "sub_null_in_family_with_cells": len(sub_null),
                   "errors": len(errors)},
        "errors": errors,
        "new_rows": new_rows,
        "gone_rows": gone_rows,
        "summary_diff": summary_diff,
        "evidence_weak": weak,
        "conflicts": conflicts,
        "pending_director": sorted(pd_rows),
        "sub_null": sub_null,
        "unused_sub_cells": unused_subs,
        "step1_code_name_split": code_name_split,
    }
    text = json.dumps(result, ensure_ascii=False, indent=1) + "\n"
    if a.out:
        Path(a.out).write_text(text)
        c = result["counts"]
        print(f"rows {c['rows']} · step1 active {c['step1_active']} · 새 행 {c['new_rows']} · 빠진 행 {c['gone_rows']} · "
              f"오류 {c['errors']} · open {c['open']} · 근거 약 {c['evidence_weak']} · 원장님 문의 {c['pending_director']} · "
              f"충돌 {c['conflicts']} · 하위 null(칸 있는 계열) {c['sub_null_in_family_with_cells']} → {a.out}")
    else:
        sys.stdout.write(text)
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
