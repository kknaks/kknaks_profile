"""단위 시술 원장 점검 — 원천 원장 항목 521 을 다시 펼쳐 step5-units.json · step5-decisions.json 과 맞춰 보고, 제품 → 단위 시술 상속 쌍마다 기법 근거를 따로 다시 가린다.

읽기만 한다. 원장(step5-units.json · .md) · 결정(step5-decisions.json) · 앞 단계 정본(step1 · 2 · 3 · 4) · 원천은 고치지 않는다 —
결과는 결정 목록의 재료다. 표준 라이브러리만 쓴다.

    python3 <이 파일> \
        --work orchestration/work/phub-recommend \
        --out <scratchpad>/unit-check.json        # --source <원천 폴더> 로 새 스냅샷을 볼 수 있다

본다(지금 원천 기준 — 가상 문장 시험은 하지 않는다. _RESUME §2 10-28 「끝 조건 = 지금 원천 기준」 · 5단계 검수 v3 PASS 판):
- 원장 항목 521 — 원천 taxonomy modality[].subcategories[].items[] 를 다시 펼친다
  - 펼쳤는데 결정 ledger[] 에 없는 id = open(결정 없는 원장 항목) · 결정에 있는데 원천에 없는 id = stale · 이름이 바뀐 id = open
  - 행선지 값이 9종 밖 = 오류 · 행선지별 셈 · 원장 summary.ledger_521 과 같은지
  - **시술인데 단위 시술 없음**(행선지 단위 시술 · 제품 + 단위 시술 · 다른 단계 이름인데 원장 units 빈칸) = open — 0 이어야
- 단위 시술 키 — 계열(step2) · 하위(그 계열 칸) · 성분(M16 만) · 부위(step3 노드 · 특수 부위 · 묶음 아님) · 기법(step4 노드) · 키 겹침 · 이름 겹침 · 원천 근거(sources) 없음
- 상속 쌍 기법 근거 — 원장 product_links[].inherited_candidates 쌍마다 근거 종류를 따로 가린다(step5-apply.py compat 과 같은 결정 · 다른 코드):
  제품 출처 · 계열 기법 하나 · S7(기법 안 갈리는 계열) · 계열 근거(종류 · 하위 · product_map) · 4단계 가드 · 장비 속성 · 매질이 기법을 정함 → 어느 것도 아니면 오류(기법 근거 없는 쌍)
  가드 밖 기법 · 계열 · 하위 어긋남도 오류
- 추천 가능 제품인데 단위 시술 0 — 목록(계열 밖 · 원천 질문 예외 · 예외 결정 없음). 예외 결정(원장 행 origin_question) 없는 것 = open
- 원장 open[] · stale_decisions[] · summary 셈

종료 코드: errors 0 · open 0 이면 0, 아니면 1.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

DESTS = {"제품", "제품 + 단위 시술", "단위 시술", "6단계 패키지", "다른 단계 이름", "시술 아님(다른 단계)", "값", "시술 아님", "원장님 문의"}
PROC_DEST = ("단위 시술", "제품 + 단위 시술", "다른 단계 이름")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--work", required=True, help="orchestration/work/phub-recommend")
    ap.add_argument("--source", help="원천 폴더(없으면 결정 source.path)")
    ap.add_argument("--out", help="결과 JSON 경로(없으면 stdout)")
    a = ap.parse_args()

    W = Path(a.work)
    J = lambda p: json.loads(Path(p).read_text())
    DEC = J(W / "step5-decisions.json")
    LED = J(W / "step5-units.json")
    S1, S2, S3, S4 = (J(W / DEC["canon"][k]) for k in ("step1", "step2", "step3", "step4"))
    SRC = Path(a.source or DEC["source"]["path"])
    TAX = J(SRC / "taxonomy.json")

    errors, opened, stale = [], [], []

    def err(t, msg, **kw):
        errors.append(dict(type=t, msg=msg, **kw))

    def op(t, **kw):
        opened.append(dict(type=t, **kw))

    PROD = {x["ledger_id"]: x for x in S1["items"]}
    ACTIVE = {k for k, x in PROD.items() if x.get("active")}
    FAM = {f["id"]: f for f in S2["families"]}
    PF = {p["ledger_id"]: p for p in S2["product_family"]}
    SITE = {n["name"]: n for n in S3["nodes"]}
    SPECIAL = DEC["special_sites"]
    TECH = {n["id"]: n for n in S4["nodes"]}
    FDEF = {f["family"]: f for f in S4["family_defaults"]}
    HINT = {h["ledger_id"]: h for h in S4["device_attrs"]["technique_hints"]}
    PULSES = set(S4["dictionaries"]["pulse_mode"])
    pname = lambda lid: PROD[lid]["2_names"]["display_name"] if lid in PROD else lid

    # ── 1. 원장 항목 521 ──
    src_items = [(m["id"], i) for m in TAX["modality"] for s in m["subcategories"] for i in s["items"]]
    dec_led = {d["id"]: d for d in DEC["ledger"]}
    led_rows = {r["id"]: r for r in LED["ledger"]}
    src_ids = set()
    for fam, it in src_items:
        lid = it["id"]
        src_ids.add(lid)
        d = dec_led.get(lid)
        if d is None:
            op("결정 없는 원장 항목", id=lid, name=it["name"], source_family=fam)
            continue
        if d["name"] != it["name"]:
            op("원장 항목 이름 바뀜", id=lid, decision=d["name"], source=it["name"])
        if d["dest"] not in DESTS:
            err("원장 행선지 값 밖", f"{lid} {d['dest']}", id=lid)
    for lid in dec_led:
        if lid not in src_ids:
            stale.append(dict(where="ledger", id=lid, name=dec_led[lid]["name"]))
    if set(led_rows) != src_ids:
        err("원장 낡음", f"원장 ledger 행 {len(led_rows)} ≠ 원천 원장 항목 {len(src_ids)} — step5-apply.py 재실행 필요",
            only_ledger=sorted(set(led_rows) - src_ids), only_source=sorted(src_ids - set(led_rows)))
    by_dest = collections.Counter(dec_led[i]["dest"] if i in dec_led else None for i in src_ids)
    proc_no_unit = []
    for lid in sorted(src_ids):
        r = led_rows.get(lid)
        d = dec_led.get(lid)
        if not d or d["dest"] not in PROC_DEST:
            continue
        if not r or not r.get("units"):
            proc_no_unit.append(dict(id=lid, name=d["name"], dest=d["dest"]))
            op("시술인데 단위 시술 없음", id=lid, name=d["name"])
        if r and d and r.get("dest") != d["dest"]:
            err("원장 낡음", f"{lid} 원장 행선지 {r.get('dest')} ≠ 결정 {d['dest']}", id=lid)
    counted_521 = dict(
        total=len(src_ids),
        products=by_dest["제품"],
        procedures=sum(by_dest[k] for k in PROC_DEST),
        procedures_with_unit=sum(by_dest[k] for k in PROC_DEST) - len(proc_no_unit),
        procedures_by_dest={k: by_dest[k] for k in PROC_DEST},
        package_6=by_dest["6단계 패키지"],
        not_procedure={k: by_dest[k] for k in ("시술 아님", "값", "시술 아님(다른 단계)")},
        pending_director=by_dest["원장님 문의"],
        no_decision=by_dest[None],
    )
    said_521 = LED["summary"]["ledger_521"]
    for k, v in counted_521.items():
        if said_521.get(k) != v:
            err("summary 불일치", f"ledger_521.{k}: 원장 {said_521.get(k)} ≠ 다시 센 값 {v}")

    # ── 2. 단위 시술 키 ──
    UNITS = {u["id"]: u for u in LED["units"]}
    keys, names = {}, collections.Counter()
    for i, u in UNITS.items():
        k = u["key"]
        bad = []
        if k["family"] not in FAM:
            bad.append(f"계열 {k['family']} 없음(step2)")
        elif k.get("sub_family") and k["sub_family"] not in FAM[k["family"]]["sub_families"]:
            bad.append(f"하위 {k['sub_family']} 가 {k['family']} 칸 아님")
        if k.get("ingredient") and k["family"] != "M16":
            bad.append("성분 칸은 M16 만")
        if k["site"] not in SITE and k["site"] not in SPECIAL:
            bad.append(f"부위 {k['site']} 없음(step3 · 특수 부위)")
        elif k["site"].endswith("(묶음)"):
            bad.append("묶음 부위는 키를 만들지 않음(S5)")
        if k["technique"] not in TECH:
            bad.append(f"기법 {k['technique']} 없음(step4)")
        kt = (k["family"], k.get("sub_family"), k.get("ingredient"), k.get("ingredient_of"), k["site"], k["technique"])
        if kt in keys:
            bad.append(f"키 겹침 {keys[kt]}")
        keys[kt] = i
        if not u.get("sources"):
            bad.append("원천 근거(sources) 없음")
        if bad:
            err("단위 시술 키 오류", f"{i} {u['name']}: " + " · ".join(bad), unit=i)
        names[u["name"]] += 1
    for n, c in names.items():
        if c > 1:
            err("단위 시술 이름 겹침", n)
    dec_units = {u["id"] for u in DEC["units"]}
    if dec_units != set(UNITS):
        err("원장 낡음", f"결정 units {len(dec_units)} ≠ 원장 units {len(UNITS)}", only_decision=sorted(dec_units - set(UNITS)), only_ledger=sorted(set(UNITS) - dec_units))

    # ── 3. 상속 쌍 기법 근거(step5-decisions product_link_rule — compat 과 다른 코드로) ──
    PLR = DEC["product_link_rule"]
    TC = PLR["technique_compat"]
    TREQ = {r["technique"]: r for r in TC["requires"]}
    GUARD = {p: g for g in PLR["guards"] for p in g["products"]}
    FEV = {e["family"]: e for e in TC["family_evidence"]}
    PEV = collections.defaultdict(set)
    for e in TC.get("product_evidence") or []:
        PEV[e["product"]].update(e["units"])
    key_sub_fams = {u["key"]["family"] for u in UNITS.values() if u["key"].get("sub_family")}
    split = key_sub_fams | {f for f, d in FDEF.items() if d["also"]}
    sub_techs = collections.defaultdict(set)
    for u in UNITS.values():
        if u["key"].get("sub_family"):
            sub_techs[(u["key"]["family"], u["key"]["sub_family"])].add(u["key"]["technique"])

    def single(f, t):
        d = FDEF.get(f)
        return bool(d) and not d["also"] and d["default"] == t and not TECH[t].get("children")

    def allowed_pulses(req, mediums):
        return set(req["pulse_mode_any"]) | {x for m in mediums for x in (req.get("pulse_mode_by_medium") or {}).get(m, [])}

    def hint_meets(h, req, mediums):
        if "pulse_mode_any" in req:
            return bool(set(h["pulse_mode"]) & allowed_pulses(req, mediums))
        if "modes_any" in req:
            return bool(set(h["modes"]) & set(req["modes_any"]))
        return None

    def conditioned(t, medium):
        r = TREQ.get(t) or {}
        if "modes_any" in r:
            return True
        if "pulse_mode_any" in r:
            return not PULSES <= allowed_pulses(r, [medium])
        return False

    def medium_decides(f, sub, t):
        ts = sub_techs[(f, sub)]
        parted = any(x != y and TECH[x].get("parent") != y and TECH[y].get("parent") != x for x in ts for y in ts)
        return not parted and not any(conditioned(x, sub) for x in ts)

    def family_techs(lid, f, subs):
        e = FEV[f]
        if lid in (e.get("product_map") or {}):
            return set(e["product_map"][lid]["techniques"])
        sb = [m for ff, m in subs if ff == f and m]
        kind = (PROD[lid].get("1_identity") or {}).get("kind") or ""
        out = set()
        for m in sb:
            out |= set((e.get("sub_family_map") or {}).get(m, [])) | set(e.get("sub_family_any") or [])
        if not sb or not e.get("kind_only_without_sub"):
            for w, ts in (e.get("kind_map") or {}).items():
                if (kind == w) if e.get("kind_exact") else (w in kind):
                    out = set(ts) if e.get("kind_overrides") else out | set(ts)
        return out or None

    def evidence(lid, i, subs):
        """이 쌍의 기법 근거 종류 — None 이면 근거 없음."""
        k = UNITS[i]["key"]
        f, t, sub = k["family"], k["technique"], k.get("sub_family")
        if i in PEV.get(lid, ()):
            return "제품 출처"
        if f not in split:
            return "S7(기법 안 갈리는 계열)"
        if single(f, t):
            return "계열 기법 하나"
        if f in FEV:
            ts = family_techs(lid, f, subs)
            if ts is not None:
                return "계열 근거(종류 · 하위 · 출처)" if t in ts else None
            if sub and lid in GUARD:
                return "4단계 가드"
            if sub and medium_decides(f, sub, t):
                return "매질이 기법을 정함"
            return None
        h, req = HINT.get(lid), TREQ.get(t)
        if sub:
            ok = hint_meets(h, req, [sub]) if h and req else None
            if ok is False:
                return None
            if ok:
                return "장비 속성"
            return "매질이 기법을 정함" if medium_decides(f, sub, t) else None
        ok = hint_meets(h, req, [m for ff, m in subs if ff == f]) if h and req else None
        return "장비 속성" if ok else None

    stored_by_p = collections.defaultdict(set)
    for i, u in UNITS.items():
        for up in u.get("uses_product") or []:
            stored_by_p[up["product"]].add(i)
            if up["product"] not in ACTIVE:
                err("저장 uses_product 제품이 1단계 active 아님", f"{i} ← {up['product']}", unit=i, product=up["product"])
            g = GUARD.get(up["product"])
            if g and u["key"]["technique"] not in g["allowed_techniques"]:
                err("가드 밖 기법", f"저장 {i} ← {up['product']} 기법 {u['key']['technique']}", unit=i, product=up["product"])

    ev_count = collections.Counter()
    ev_by_family = collections.defaultdict(collections.Counter)
    no_evidence = []
    links = {x["product"]: x for x in LED["product_links"]}
    for lid in sorted(ACTIVE):
        if lid not in links:
            err("원장 낡음", f"1단계 active 제품 {lid} 가 product_links 에 없음", product=lid)
    for x in LED["product_links"]:
        lid = x["product"]
        pf = PF.get(lid)
        if lid not in ACTIVE or pf is None:
            err("상속 제품이 1단계 active · 2단계에 없음", lid, product=lid)
            continue
        fams = [pf["family"]] + list(pf.get("also_families") or [])
        subs = {(pf["family"], pf.get("sub_family"))} | {(s["family"], s["sub_family"]) for s in pf.get("also_sub_families") or []}
        for i in x["inherited_candidates"]:
            if i not in UNITS:
                err("상속 쌍 키 없음", f"{lid} → {i}", product=lid, unit=i)
                continue
            k = UNITS[i]["key"]
            if k["family"] not in fams or (k.get("sub_family") and (k["family"], k["sub_family"]) not in subs):
                err("상속 쌍 계열 · 하위 어긋남", f"{x['name']} → {i} {UNITS[i]['name']}", product=lid, unit=i)
                continue
            g = GUARD.get(lid)
            if g and k["technique"] not in g["allowed_techniques"]:
                err("가드 밖 기법", f"상속 {x['name']} → {i} 기법 {k['technique']}", product=lid, unit=i)
                continue
            e = evidence(lid, i, subs)
            if e is None:
                no_evidence.append(dict(product=lid, name=x["name"], unit=i, unit_name=UNITS[i]["name"], technique=k["technique"]))
                err("기법 근거 없는 상속 쌍", f"{x['name']} → {i} {UNITS[i]['name']}({k['technique']})", product=lid, unit=i)
                continue
            ev_count[e] += 1
            ev_by_family[k["family"]][e] += 1
        if set(x["stored_units"]) != stored_by_p.get(lid, set()):
            err("원장 낡음", f"{lid} product_links.stored_units ≠ 단위 시술 uses_product", product=lid)

    # ── 4. 추천 가능 제품인데 단위 시술 0 ──
    rec0 = []
    for x in LED["product_links"]:
        if not x["recommendable"] or x["stored_units"] or x["inherited_candidates"]:
            continue
        oq = (dec_led.get(x["product"]) or {}).get("origin_question")
        if x["family"] in (None, "계열 밖"):
            kind = "계열 밖 · 원장님 문의(단위 시술 없음)"
        elif oq:
            kind = "예외(원천 질문)"
        else:
            kind = "예외 결정 없음"
            op("추천 가능 제품인데 단위 시술 0 · 예외 결정 없음", product=x["product"], name=x["name"])
        rec0.append(dict(product=x["product"], name=x["name"], family=x["family"], sub_family=x["sub_family"], kind=kind, origin_question=oq,
                         excluded=x.get("technique_excluded") or []))

    # ── 5. 원장 open · stale ──
    if LED["open"]:
        err("원장 open", f"step5-units.json open {len(LED['open'])}", open=LED["open"])
    if LED["stale_decisions"]:
        err("원장 낡은 결정", f"step5-units.json stale {len(LED['stale_decisions'])}", stale=LED["stale_decisions"])
    S = LED["summary"]
    for k, v in (("units", len(UNITS)), ("origin_questions", len(LED["origin_questions"])), ("staff_questions", len(LED["staff_questions"]))):
        if S.get(k) != v:
            err("summary 불일치", f"{k}: 원장 {S.get(k)} ≠ 다시 센 값 {v}")

    fx = W / "step5-fixtures" / "result.json"
    fixture = None
    if fx.exists():
        r = J(fx)
        fixture = dict(passed=r["passed"], total=r["total"])

    pairs = sum(len(x["inherited_candidates"]) for x in LED["product_links"])
    res = dict(
        source=dict(path=str(SRC), ledger_items=len(src_ids)),
        ledger_521=counted_521, ledger_by_dest={str(k): v for k, v in by_dest.most_common()},
        procedures_without_unit=proc_no_unit,
        units=dict(total=len(UNITS), by_family=dict(collections.Counter(u["key"]["family"] for u in UNITS.values())),
                   by_site_basis_default=sum(1 for u in UNITS.values() if str(u.get("site_basis") or "").startswith("기본값")),
                   special_sites=dict(collections.Counter(u["key"]["site"] for u in UNITS.values() if u["key"]["site"] in SPECIAL)),
                   ingredient_unknown=[i for i, u in UNITS.items() if u["key"].get("ingredient") == "미상"]),
        inheritance=dict(pairs=pairs, products_with_pairs=sum(1 for x in LED["product_links"] if x["inherited_candidates"]),
                         excluded_pairs=sum(len(x.get("technique_excluded") or []) for x in LED["product_links"]),
                         stored_pairs=sum(len(v) for v in stored_by_p.values()), stored_products=len(stored_by_p),
                         by_evidence=dict(ev_count.most_common()),
                         by_family={f: dict(c) for f, c in sorted(ev_by_family.items())},
                         no_evidence=no_evidence,
                         product_evidence_excluded=TC.get("product_evidence_excluded") or []),
        recommendable_zero_units=rec0,
        recommendable_total=sum(1 for x in LED["product_links"] if x["recommendable"]),
        origin_questions=len(LED["origin_questions"]), staff_questions=len(LED["staff_questions"]),
        fixture_result=fixture,
        open=opened, stale_decisions=stale, errors=errors,
        totals=dict(open=len(opened), stale=len(stale), errors=len(errors)))
    out = json.dumps(res, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(out)
    else:
        print(out)
    print(json.dumps(dict(res["totals"], ledger=len(src_ids), procedures=counted_521["procedures"], procedures_without_unit=len(proc_no_unit),
                          units=len(UNITS), pairs=pairs, no_evidence=len(no_evidence), recommendable_zero=len(rec0)), ensure_ascii=False), file=sys.stderr)
    return 0 if not errors and not opened else 1


if __name__ == "__main__":
    sys.exit(main())
