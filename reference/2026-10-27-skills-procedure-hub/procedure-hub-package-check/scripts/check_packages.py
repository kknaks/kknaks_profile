"""패키지 원장 점검 — 5단계가 6단계로 넘긴 패키지 원천 행을 다시 뽑아 step6-packages.json · step6-decisions.json 과 맞춰 보고, 구성 엣지 원문을 원천 칸에서 따로 다시 찾는다.

읽기만 한다. 원장(step6-packages.json · .md) · 결정(step6-decisions.json) · 5단계 정본(step5-units.json) · 원천은 고치지 않는다 —
결과는 결정 목록의 재료다. 표준 라이브러리만 쓴다.

    python3 <이 파일> \
        --work orchestration/work/phub-recommend \
        --out <scratchpad>/package-check.json      # --source <원천 폴더> 로 새 스냅샷을 볼 수 있다

본다(지금 원천 기준 — 가상 문장 시험은 하지 않는다. _RESUME §2 10-29 6단계 「끝 조건 open 0 + 패키지인데 구성 없음 0」):
- 패키지 원천 행 — step5-units.json ledger[] 행선지 「6단계 패키지」 + market[] kind 「6단계 패키지」 를 다시 뽑는다
  (step5-decisions.json ledger[] 의 dest 와도 대 본다 — 5단계 정본과 결정이 다르면 오류)
  - 원천 행인데 결정 packages[] 에 없음 = open(결정 없는 패키지 원천 행) · 결정에 있는데 원천 행 아님 = stale · 한 행이 두 패키지 = 오류
  - 원장 이름이 원천 taxonomy 이름과 다름 = open · 시장가 이름이 원천 market-pricing 에 없음 = open
- 구성 엣지(unit 있는 구성) — 원문 낱말을 원천 칸에서 다시 찾는다
  원장 패키지 = 이름 · detail · extracted overview · mechanism / 시장가 패키지 = 시장가 행 이름 / 회차 묶음 = 5단계 시장가 행 to 가 그 키를 부름 · sessions 같음
  - 어디에도 없음 = 오류(원천에 없는 구성) · extracted indications 에만 있음 = 오류(적응증은 구성 아님)
- 키 실재 — 엣지 unit · 슬롯 candidates · missing_unit 아닌 키가 step5-units.json units[] 에 있는가
- 슬롯 · 근거 약 — 슬롯은 원천 질문 있어야 · 근거 약 엣지도 원천 질문 있어야 · 질문 id 가 origin_questions[] 에 있어야
- 구성도 질문도 없는 패키지 = open — 0 이어야
- 시그니처 노출 — kind 「병원 시그니처」인데 recommendable = 오류 · kind 가 결정 kinds[] 밖 = 오류
- 메뉴 묶음 — menu_group 이 있으면 그 원장 행이 원천 taxonomy 의 같은 라벨 하위에 있는가 · 그 하위가 non_packages[] 에 있는가
- 가격 원문 — 원장 price_raw 가 원천 detail 안 글자 그대로인가
- 넘겨받은 것 — step5 handoffs 「2단계 deferred」 의 6단계 행이 결정 handoffs[] 에 · covered_by 가 non_packages[] 에
- 원장 open[] · stale_decisions[] · summary 셈(패키지 · kind · 추천 노출 · 엣지 · 근거 약 · 슬롯 · 원천 행)

숫자는 이 파일에 적지 않는다(고정 assert 없음) — 셈은 전부 출력이다.
종료 코드: errors 0 · open 0 이면 0, 아니면 1.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

SIGNATURE = "병원 시그니처"


def norm(s) -> str:
    return re.sub(r"\s+", "", str(s or ""))


def pieces(text: str) -> list[str]:
    """구성 원문을 찾을 낱말로 — 원문 그대로 · 괄호 앞 · 괄호 안 · 「×」 앞."""
    out = [text]
    head = re.split(r"[(×]", text)[0]
    out.append(head)
    out += re.findall(r"\(([^)]*)\)", text)
    return [norm(p) for p in out if len(norm(p)) > 1 or norm(p) == norm(text)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--work", required=True, help="orchestration/work/phub-recommend")
    ap.add_argument("--source", help="원천 폴더(없으면 결정 source.path)")
    ap.add_argument("--out", help="결과 JSON 경로(없으면 stdout)")
    a = ap.parse_args()

    W = Path(a.work)
    J = lambda p: json.loads(Path(p).read_text())
    DEC = J(W / "step6-decisions.json")
    LED = J(W / "step6-packages.json")
    S5 = J(W / DEC["canon"]["step5"])
    D5 = J(W / "step5-decisions.json")
    SRC = Path(a.source or DEC["source"]["path"])
    TAX = J(SRC / "taxonomy.json")
    MKT = J(SRC / "market-pricing.json")

    errors, opened, stale = [], [], []

    def err(t, msg, **kw):
        errors.append(dict(type=t, msg=msg, **kw))

    def op(t, **kw):
        opened.append(dict(type=t, **kw))

    UNITS = {u["id"]: u for u in S5["units"]}
    ITEMS = {i["id"]: (s["id"], s["label"], i) for m in TAX["modality"] for s in m["subcategories"] for i in s["items"]}
    SUBS = {s["id"]: s for m in TAX["modality"] for s in m["subcategories"]}
    MROWS = {i["name"]: i for c in MKT["categories"] for i in c["items"]}
    S5M = {r["name"]: r for r in S5["market"]}
    OQ = {q["id"] for q in DEC["origin_questions"]}
    KINDS = set(DEC["kinds"])
    NP = {n["id"]: n for n in DEC["non_packages"]}

    # ── 1. 패키지 원천 행 ──
    src_l = {r["id"]: r for r in S5["ledger"] if r["dest"] == "6단계 패키지"}
    src_m = {r["name"]: r for r in S5["market"] if r["kind"] == "6단계 패키지"}
    d5_l = {d["id"] for d in D5["ledger"] if d.get("dest") == "6단계 패키지"}
    if d5_l != set(src_l):
        err("5단계 정본 ↔ 결정 어긋남", "step5-units ledger 「6단계 패키지」 ≠ step5-decisions ledger dest",
            only_canon=sorted(set(src_l) - d5_l), only_decision=sorted(d5_l - set(src_l)))
    cov_l, cov_m = collections.Counter(), collections.Counter()
    for d in DEC["packages"]:
        if d["source"] == "ledger":
            cov_l[d["ledger_id"]] += 1
        else:
            for n in d.get("market_names") or []:
                cov_m[n] += 1
    for k, r in src_l.items():
        if not cov_l[k]:
            op("결정 없는 패키지 원천 행", id=k, name=r["name"])
    for k in src_m:
        if not cov_m[k]:
            op("결정 없는 패키지 원천 행", name=k)
    for k, v in list(cov_l.items()) + list(cov_m.items()):
        if v > 1:
            err("패키지 원천 행 겹침", f"{k} 가 패키지 {v} 개에", id=k)
    stale += [["packages", k] for k in cov_l if k not in src_l]
    stale += [["packages", k] for k in cov_m if k not in src_m]

    # ── 2. 패키지마다 ──
    edges, slots, pk_rows = [], [], []
    by_evidence = collections.Counter()
    for d in DEC["packages"]:
        pid = d["id"]
        if d["kind"] not in KINDS:
            err("kind 값 밖", f"{pid} kind {d['kind']}", id=pid)
        if d["kind"] == SIGNATURE and d["recommendable"]:
            err("시그니처 추천 노출", f"{pid} {d['name']} 병원 시그니처인데 recommendable", id=pid)
        fields = {}  # 칸 이름 → 글자
        indications = ""
        if d["source"] == "ledger":
            lid = d["ledger_id"]
            if lid not in ITEMS:
                op("패키지 원장 항목이 원천에 없음", id=lid)
                continue
            sub_id, sub_label, it = ITEMS[lid]
            if it["name"] != d["name"]:
                op("패키지 원장 이름 바뀜", id=lid, decision=d["name"], source=it["name"])
            ex = it.get("extracted") or {}
            fields = {"name": it["name"], "detail": it.get("detail") or "", "overview": ex.get("overview") or "", "mechanism": ex.get("mechanism") or ""}
            indications = json.dumps(ex.get("indications") or {}, ensure_ascii=False)
            if d.get("price_raw") and d["price_raw"] not in fields["detail"]:
                err("가격 원문 없음", f"{pid} price_raw 「{d['price_raw']}」 가 원천 detail 에 없음", id=pid)
            mg = d.get("menu_group")
            if mg:
                lab = re.search(r"「(.+)」", mg)
                if not lab or lab.group(1) != sub_label:
                    err("메뉴 묶음 어긋남", f"{pid} menu_group 「{mg}」 ↔ 원천 하위 「{sub_label}」({sub_id})", id=pid)
                if sub_id not in NP:
                    err("메뉴 묶음 결정 없음", f"{pid} 원천 하위 {sub_id} 가 non_packages[] 에 없음", id=pid)
        else:
            for n in d.get("market_names") or []:
                if n not in MROWS:
                    op("패키지 시장가 행이 원천에 없음", name=n)
                fields[f"market:{n}"] = n
        hay = {k: norm(v) for k, v in fields.items()}
        for n in d.get("market_names") or []:  # 회차 = 5단계 시장가 행 sessions 와 같아야
            ss = {c.get("sessions") for c in d.get("components") or [] if c.get("sessions")}
            if ss and ss != {(S5M.get(n) or {}).get("sessions")}:
                err("회차 어긋남", f"{pid} 구성 sessions {sorted(ss)} ↔ 5단계 시장가 「{n}」 sessions {(S5M.get(n) or {}).get('sessions')}", id=pid)
        comps = d.get("components") or []
        has_q = False
        for i, c in enumerate(comps):
            q = c.get("origin_question")
            if q and q not in OQ:
                err("원천 질문 id 없음", f"{pid} #{i + 1} {q}", id=pid)
                q = None
            has_q = has_q or bool(q)
            for u in [c.get("unit")] + (c.get("candidates") or []):
                if u and u not in UNITS:
                    err("키 없음", f"{pid} #{i + 1} {u} 가 step5 units 에 없음", id=pid, unit=u)
            if not c.get("unit"):
                if not q:
                    op("구성 키도 질문도 없음", id=pid, text=c["text"])
                slots.append(dict(package=pid, text=c["text"], candidates=c.get("candidates") or [], missing_unit=c.get("missing_unit"), origin_question=q))
                continue
            if c.get("evidence_level") == "약" and not q:
                op("근거 약 구성인데 원천 질문 없음", id=pid, text=c["text"])
            # 원문 낱말을 원천 칸에서 다시 찾는다
            found = []
            for p in pieces(c["text"]):
                found += [k for k, v in hay.items() if p in v and k not in found]
            ev = None
            if found:
                ev = "원천 " + " · ".join(k.split(":")[0] for k in found)
            elif c.get("sessions") and any(c["unit"] in str((S5M.get(n) or {}).get("to") or "") for n in d.get("market_names") or []):
                ev = "5단계 시장가 행 to(회차)"
            elif any(p in norm(indications) for p in pieces(c["text"])):
                err("적응증에서 온 구성", f"{pid} 「{c['text']}」 가 indications 에만 있음", id=pid, text=c["text"])
            else:
                err("원천에 없는 구성", f"{pid} 「{c['text']}」 가 이름 · detail · overview · mechanism · 시장가 이름에 없음", id=pid, text=c["text"])
            by_evidence[ev or "없음"] += 1
            edges.append(dict(package=pid, text=c["text"], unit=c["unit"], unit_name=UNITS.get(c["unit"], {}).get("name"),
                              evidence_level=c.get("evidence_level"), origin_question=q, found_in=ev))
        n_edge = sum(1 for e in edges if e["package"] == pid)
        n_slot = sum(1 for s in slots if s["package"] == pid)
        if not comps:
            op("패키지인데 구성 없음", id=pid, name=d["name"])
        elif n_edge == 0 and not has_q:
            op("구성도 질문도 없는 패키지", id=pid, name=d["name"])
        pk_rows.append(dict(id=pid, name=d["name"], kind=d["kind"], recommendable=d["recommendable"], menu_group=d.get("menu_group"),
                            edges=n_edge, slots=n_slot))

    # ── 3. 묶음 이름 · 넘겨받은 것 ──
    for n in DEC["non_packages"]:
        if n["id"] not in SUBS:
            stale.append(["non_packages", n["id"]])
        elif SUBS[n["id"]]["label"] != n["label"]:
            op("묶음 이름 바뀜", id=n["id"], decision=n["label"], source=SUBS[n["id"]]["label"])
    HD = {h["source"]: h for h in DEC["handoffs"]}
    s5h = [h for h in S5["handoffs"]["2단계 deferred"] if h["deferred_to"] == "6단계"]
    for h in s5h:
        d = HD.get(h["source"])
        if d is None:
            op("넘겨받은 것 행선지 없음", id=h["source"])
            continue
        for c in d["covered_by"]:
            if c not in NP:
                err("넘겨받은 것 행선지 키 없음", f"{h['source']} → {c} 가 non_packages[] 에 없음", id=c)
    stale += [["handoffs", k] for k in HD if k not in {h["source"] for h in s5h}]

    # ── 4. 원장 대조 ──
    if LED["open"]:
        err("원장 open", f"step6-packages.json open {len(LED['open'])}", open=LED["open"])
    if LED["stale_decisions"]:
        err("원장 낡은 결정", f"step6-packages.json stale {len(LED['stale_decisions'])}", stale=LED["stale_decisions"])
    S = LED["summary"]
    recount = dict(packages=len(pk_rows), by_kind=dict(collections.Counter(p["kind"] for p in pk_rows)),
                   recommendable=sum(p["recommendable"] for p in pk_rows), edges=len(edges),
                   edges_weak=sum(1 for e in edges if e["evidence_level"] == "약"), slots=len(slots),
                   source_rows=dict(ledger=len(src_l), market=len(src_m)))
    for k, v in recount.items():
        if S.get(k) != v:
            err("summary 불일치", f"{k}: 원장 {S.get(k)} ≠ 다시 센 값 {v}")
    led_edges = {(e["package"], e["text"], e["unit"]) for e in LED["contains"]}
    if led_edges != {(e["package"], e["text"], e["unit"]) for e in edges}:
        err("원장 낡음", "step6-packages.json contains ≠ 결정 구성 — step6-apply.py 재실행 필요")

    fx = W / "step6-fixtures" / "result.json"
    fixture = None
    if fx.exists():
        r = J(fx)
        fixture = dict(passed=r["passed"], total=r["total"])

    res = dict(
        source=dict(path=str(SRC), package_rows=recount["source_rows"]),
        recount=recount,
        packages_full=sum(1 for p in pk_rows if p["edges"] and not p["slots"]),
        packages_no_edge=[p["id"] for p in pk_rows if not p["edges"]],
        signature=[p["id"] for p in pk_rows if p["kind"] == SIGNATURE],
        edges_by_evidence=dict(by_evidence.most_common()),
        slots=slots,
        slots_missing_unit=[s for s in slots if s["missing_unit"]],
        non_packages=len(DEC["non_packages"]), handoffs=len(s5h),
        origin_questions=len(DEC["origin_questions"]), source_fix=len(DEC["source_fix"]),
        fixture_result=fixture,
        packages=pk_rows, edges=edges,
        open=opened, stale_decisions=stale, errors=errors,
        totals=dict(open=len(opened), stale=len(stale), errors=len(errors)))
    out = json.dumps(res, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(out)
    else:
        print(out)
    print(json.dumps(dict(res["totals"], packages=len(pk_rows), edges=len(edges), slots=len(slots),
                          no_edge=len(res["packages_no_edge"])), ensure_ascii=False), file=sys.stderr)
    return 0 if not errors and not opened else 1


if __name__ == "__main__":
    sys.exit(main())
