"""고민 원장 점검 — 고민 표현 · 엣지 원천 행을 원천에서 다시 뽑아 step7-concerns.json · step7-decisions.json 과 맞춰 보고,
자동 대응(완전 일치) · 엣지 부위 · 엣지 원천 구조를 원장 표시와 따로 다시 가린다.

읽기만 한다. 원장(step7-concerns.json · .md) · 결정(step7-decisions.json) · 앞 단계 정본(step3 · 5 · 6) · 원천은 고치지 않는다 —
결과는 결정 목록의 재료다. 표준 라이브러리만 쓴다.

    python3 <이 파일> \
        --work orchestration/work/phub-recommend \
        --out <scratchpad>/concern-check.json      # --source <원천 폴더> 로 새 스냅샷을 볼 수 있다

본다(지금 원천 기준 — 가상 문장 시험은 하지 않는다. _RESUME §2 10-29 7단계 「끝 조건 open 0」):
- 고민 노드 — taxonomy problem 의 대분류 · 중분류 · 항목 id 가 원장 concerns 에 다 있는가(없으면 open) ·
  고민 노드(node true · 항목 kind 「고민」)가 taxonomy 또는 결정 extra_concern_items 에 있는가(없으면 오류)
- 고민 표현 — 원천 9곳(problem-packages 대분류 · CC / problem-combos / 최적화 고민 · 연령 주 고민 / synergy target /
  레시피 goal / 비교 / 3단계 넘김(deferred · strings handoff) / 6단계 메뉴 분류)의 표현을 다시 뽑는다
  - 원천에 있는데 원장 대응표에 없음 = open · 원장 대응표에 있는데 원천에 없음 = stale
- 자동 대응 = 완전 일치만(R5 · 검수 F1) — 게이트를 건너뛴 행마다 원천 말을 그 칸에서 다시 잘라
  대상 이름(대분류 이름 · 원천 이름 · 중분류 라벨 · 항목 이름 · 목적 이름, 「쳐짐 → 처짐」 치환만)과 글자 비교. 다르면 오류
  - 결정 대응표 행의 match 가 「완전」으로 시작하는데 원천 말 ≠ 대상 이름 = 오류(결정 쪽 같은 꼴)
  - 결정 대응표 target ≠ 원장 행 target = 오류(원장 낡음 — 게이트 답을 결정에 넣고 apply 를 안 돌림)
  - 확인 대기 행마다 gate_initial 이 있고 원천 질문(「원천(사람 확인 게이트)」)이 같은 수인가
- 엣지 원천 구조(R7) — 엣지마다 원천 칸에서 다시 찾는다
  ① modality_ref = 항목 modality_ref 에 그 계열 · ① P1 detail = P1 항목 detail 에 결정 낱말 · ② = 그 고민 combos 의 계열 ·
  ③ = 그 CC procedures 에 그 이름 · ④ = 그 고민 · 단계 optimal_combo 에 그 이름 · ⑤ = 항목 이름 그대로(P1 밖) ·
  ⑥ = 5단계 units[].purposes · product_evidence 목적 · ⑦ = 6단계 non_packages(7단계 넘김)
  - 못 찾음 = 오류(원천 구조에 없는 엣지) · 일곱 갈래 밖 source = 오류(적응증 · 효과 문장 · 8단계 원천 유래)
  - 원천 구조 행 수 ↔ 엣지 수(③ CC procedures · ④ optimal_combo · ⑤ 시술 이름 항목 · ⑥ purposes) 다르면 오류(빠진 엣지)
- 엣지 부위(검수 F2 · W2 · v2 W2) — 엣지 단위 시술 부위 ∈ 앵커 부위(또는 하위 · 「얼굴」 = 얼굴 전체) ∪ 부위 무관 특수 부위
  - 어긋남 = 오류(앵커 부위 밖) · 「그 부위 단위 시술 없음 · 후보 전부」인데 no_unit_at_site 표시 없음 = 오류 ·
    「후보 전부」인데 그 계열에 앵커 부위 단위 시술이 실제로 있음 = 오류(부위로 내렸어야)
  - 엣지 · 추천 조합 구성의 단위 시술이 step5-units 에 없음 = 오류
- 영업 문구 — salesPitch · upsellHook 는 default_response false · 레시피 환자 설명 · 비유는 true(R9)
- 원장 open[] · stale_decisions[] · summary 셈(대응표 · 게이트 · 엣지 · 부위 검사 · 추천 조합 · 8단계 메모)

숫자는 이 파일에 적지 않는다(고정 assert 없음) — 셈은 전부 출력이다.
종료 코드: errors 0 · open 0 이면 0, 아니면 1.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

EDGE_SOURCES = ("① ", "② ", "③ ", "④ ", "⑤ ", "⑥ ", "⑦ ", "⑧ ")  # ⑧ = 결정 노드 → 단위 시술(사용자 결정 · extra_concern_items[].units)
GATE_Q = "사람(규칙 밖 고민 표현 · R20)"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--work", required=True, help="orchestration/work/phub-recommend")
    ap.add_argument("--source", help="원천 폴더(없으면 결정 source.path)")
    ap.add_argument("--out", help="결과 JSON 경로(없으면 stdout)")
    a = ap.parse_args()

    W = Path(a.work)
    J = lambda p: json.loads(Path(p).read_text())
    DEC = J(W / "step7-decisions.json")
    LED = J(W / "step7-concerns.json")
    S3 = J(W / DEC["canon"]["step3"])
    S5 = J(W / DEC["canon"]["step5"])
    S6 = J(W / DEC["canon"]["step6"])
    SRC = Path(a.source or DEC["source"]["path"])
    TAX = J(SRC / "taxonomy.json")
    PP = J(SRC / "problem-packages.json")
    PC = J(SRC / "problem-combos.json")
    CR = J(SRC / "combo-recipes.json")
    TO = J(SRC / "treatment-optimization.json")
    CMP = J(SRC / "procedure-comparison.json")
    SYN = J(SRC / "synergy.json")

    errors, opened, stale = [], [], []

    def err(t, msg, **kw):
        errors.append(dict(type=t, msg=msg, **kw))

    def op(t, **kw):
        opened.append(dict(type=t, **kw))

    rename = DEC["rename"]

    def norm(s) -> str:
        s = str(s or "")
        for x, y in rename.items():
            s = s.replace(x, y)
        return re.sub(r"\s+", "", s)

    UNITS = {u["id"]: u for u in S5["units"]}
    C = LED["concerns"]

    # ── 1. 고민 노드 ──
    tax_ids = set()
    for P in TAX["problem"]:
        tax_ids.add(P["id"])
        for s in P["subcategories"]:
            tax_ids.add(s["id"])
            for i in s["items"]:
                tax_ids.add(i["id"])
    led_ids = {x["id"] for k in ("categories", "subcategories", "items") for x in C[k]}
    extra_dec = {x["id"] for x in DEC["extra_concern_items"]}
    for i in sorted(tax_ids - led_ids):
        op("원장에 없는 taxonomy 고민 칸", id=i)
    stale += [["concerns", i] for i in sorted(led_ids - tax_ids)]
    nodes = ([c["id"] for c in C["categories"] if c["node"]] + [s["id"] for s in C["subcategories"] if s["node"]]
             + [i["id"] for i in C["items"] if i["kind"] == "고민"] + [x["id"] for x in C["extra_items"]])
    for n in nodes:
        if n not in tax_ids and n not in extra_dec:
            err("원천 밖 고민 노드", f"{n} 이 taxonomy problem 에도 결정 extra_concern_items 에도 없음", id=n)
    for x in C["extra_items"]:
        if x["id"] not in extra_dec:
            err("원천 밖 고민 노드", f"원장 extra_items {x['id']} 가 결정에 없음", id=x["id"])

    # 대상 이름(완전 일치 비교용)
    names = collections.defaultdict(set)
    for c in C["categories"]:
        names[c["id"]] |= {norm(c["name"]), norm(c["source_name"])}
    for s in C["subcategories"]:
        names[s["id"]].add(norm(s["source_label"]))
        if s.get("concern"):
            names[s["id"]].add(norm(s["concern"]))
    for i in C["items"] + C["extra_items"]:
        names[i["id"]].add(norm(i["name"]))
    for p in LED["purposes"]:
        names[f"목적:{p['name']}"].add(norm(p["name"]))

    # ── 2. 고민 표현 — 원천에서 다시 뽑기 ──
    def word(source, field, text):
        if field == "complaints[].cc":
            return text.split(" [")[0]
        if field == "comparisons[].id · title":
            return text.split(" / ", 1)[1]
        if source == "step3 strings handoff":
            return text.split(" → ", 1)[1]
        if source == "step6 non_packages":
            return text.split(" ", 1)[1]
        return text

    src_rows = set()
    for P in PP["problems"]:
        src_rows.add(("problem-packages", "problems[].problem", P["problem"]))
        for c in P["complaints"]:
            src_rows.add(("problem-packages", "complaints[].cc", f"{c['cc']} [{c['cc_detail']}]"))
    for c in PC["combos"]:
        src_rows.add(("problem-combos", "combos[].problem", c["problem"]))
    for c in TO["by_concern"]:
        src_rows.add(("treatment-optimization", "by_concern[].concern", c["concern"]))
    for g in TO["by_age_group"]:
        for x in g["primary_concerns"]:
            src_rows.add(("treatment-optimization", "by_age_group[].primary_concerns", x))
    for l in SYN["links"]:
        if l.get("target") is not None:
            src_rows.add(("synergy", "links[].target", l["target"]))
    for r in CR["recipes"]:
        src_rows.add(("combo-recipes", "recipes[].goal", r["goal"]))
    for c in CMP["comparisons"]:
        src_rows.add(("procedure-comparison", "comparisons[].id · title", f"{c['id']} / {c['title']}"))
    for d in S3["deferred"]:
        if d["stage"] == "7단계 고민":
            src_rows.add(("step3 deferred", "deferred[].string", d["string"]))
    for x in S3["strings"]:
        for h in x.get("handoff") or []:
            if "7" in str(h.get("stage", "")):
                src_rows.add(("step3 strings handoff", "strings[].handoff", f"{x['string']} → {h['part']}"))
    for n in S6["non_packages"]:
        if n["to"].startswith("7단계"):
            src_rows.add(("step6 non_packages", "menu label", f"{n['id']} {n['label']}"))
    led_rows = {(r["source"], r["field"], r["text"]) for r in LED["correspondence"] if not r["field"].startswith("(역방향)")}
    for s_, f_, t_ in sorted(src_rows - led_rows):
        op("원장 대응표에 없는 고민 표현", source=s_, field=f_, text=t_)
    stale += [["correspondence", list(k)] for k in sorted(led_rows - src_rows)]

    # ── 3. 대응표 — 완전 일치 · 규칙(R12~R19) 자동 · 규칙 밖만 사람 질문(R20 · 10-29 게이트 → 규칙) ──
    auto_rows, gate_rows, exact_but_gated = [], [], []
    rule_ids = {r["id"] for r in DEC["rules"]} | {j["id"] for j in DEC["judgements"]}
    valid_t = set(names)
    unr = {(x["source"], x["text"]) for x in DEC.get("concern_unresolved") or []}
    for n_, r in enumerate(LED["correspondence"]):
        w = word(r["source"], r["field"], r["text"])
        ex = bool(r["target"]) and all(norm(w) in names.get(t, set()) for t in r["target"])
        if not r.get("human_check"):
            auto_rows.append(n_)
            if r.get("gate_status") == "자동(완전 일치)" and r["source"] != "problem-packages" and r.get("match") != "P id 직결" and not ex:
                err("완전 일치라 적힌 자동 대응인데 원천 말 ≠ 대상 이름", f"#{n_} {r['source']} 「{w}」 → {r['target']}",
                    row=n_, source=r["source"], text=r["text"], target=r["target"], match=r.get("match"))
            if r.get("gate_status") == "자동(규칙)":
                ids = set(re.findall(r"\b(R\d+|J\d+)\b", r.get("match") or ""))
                if not ids and "완전 일치" not in (r.get("match") or ""):
                    err("규칙 자동 대응인데 규칙 표시 없음", f"#{n_} {r['text']} — match 「{r.get('match')}」", row=n_)
                if ids - rule_ids:
                    err("규칙 자동 대응이 없는 규칙을 가리킴", f"#{n_} {r['text']} → {sorted(ids - rule_ids)}", row=n_)
                if not r["target"] and not ({"J5", "R19"} & ids):
                    err("규칙 자동 대응인데 대상 없음", f"#{n_} {r['text']}", row=n_)
            for t in r["target"]:
                if t not in valid_t:
                    err("대응 대상이 고민 · 목적 노드 아님", f"#{n_} {r['text']} → {t}", row=n_, target=t)
        else:
            gate_rows.append(n_)
            if "gate_initial" not in r:
                err("사람 질문인데 후보 칸 없음", f"#{n_} {r['text']}", row=n_)
            if r["source"] != "problem-packages" and (r["source"], r.get("source_word_key") or w) not in unr and not any(k[0] == r["source"] and k[1] in (r["text"], w, r["text"].split(" ", 1)[-1]) for k in unr):
                err("사람 질문인데 결정 concern_unresolved 없음", f"#{n_} {r['source']} 「{r['text']}」", row=n_)
            if ex:
                exact_but_gated.append(dict(row=n_, source=r["source"], text=r["text"], target=r["target"], match=r.get("match")))
    gate_q = [q for q in LED["origin_questions"] if q["to"] == GATE_Q]
    if len(gate_q) != len(gate_rows):
        err("사람 질문 수 ≠ 규칙 밖 행 수", f"질문 {len(gate_q)} · 규칙 밖 {len(gate_rows)}")

    # 원장 낡음 — 결정 · 원천으로 apply 를 임시 폴더에 다시 돌려 대응표 대상이 같은지(규칙은 apply 가 계산한다)
    dec_rows = len(DEC.get("concern_unresolved") or [])
    with tempfile.TemporaryDirectory() as td:
        pr = subprocess.run([sys.executable, str(W / "step7-apply.py"), "--out", td] + (["--source", str(SRC)] if a.source else []), capture_output=True, text=True)
        if pr.returncode != 0:
            err("apply 재실행 실패", pr.stderr.strip()[-300:])
        else:
            fresh = J(Path(td) / "step7-concerns.json")["correspondence"]
            if len(fresh) != len(LED["correspondence"]):
                err("원장 낡음(대응 행 수 ≠ 재실행)", f"원장 {len(LED['correspondence'])} · 재실행 {len(fresh)} — step7-apply.py 재실행")
            for r0, r1 in zip(LED["correspondence"], fresh):
                if (r0["text"], list(r0["target"]), r0.get("human_check")) != (r1["text"], list(r1["target"]), r1.get("human_check")):
                    err("원장 낡음(대응 target ≠ 결정 · 규칙)", f"「{r0['text']}」 원장 {r0['target']} · 재실행 {r1['target']} — step7-apply.py 재실행", text=r0["text"])

    # ── 4. 엣지 원천 구조 ──
    items_by_id = {}
    for P in TAX["problem"]:
        for s in P["subcategories"]:
            for i in s["items"]:
                items_by_id[i["id"]] = dict(i, category=P["id"], subcategory=s["id"])
    led_items = {i["id"]: i for i in C["items"]}
    cc_proc = {}
    for P in PP["problems"]:
        for c in P["complaints"]:
            cc_proc.setdefault(f"{P['problem_id']}:{c['cc']}", []).extend(p["name"] for p in c["procedures"])
    combo_fams = collections.defaultdict(set)
    for c in PC["combos"]:
        for p in c["packages"]:
            combo_fams[c["problem_id"]] |= set(p["procedures"])
    opt = {}
    for c in TO["by_concern"]:
        for s in c["severity_levels"]:
            opt[f"{c['concern']}|{s['level']}"] = list(s["optimal_combo"])
    unit_purposes = {u["id"]: set(u["purposes"]) for u in S5["units"]}
    pe_purposes = collections.defaultdict(set)
    for x in S5["rules"]["product_link"]["technique_compat"]["product_evidence"]:
        for e in x["evidence"]:
            pe_purposes[e["purpose"]] |= set(x["units"])
    np7 = {n["id"]: n for n in S6["non_packages"] if n["to"].startswith("7단계")}
    p1_words = DEC["p1_detail_words"]

    def inner(basis):
        m = re.search(r"「(.*?)」", basis or "")
        return m.group(1) if m else None

    by_src = collections.Counter()
    for k, e in enumerate(LED["edges"]):
        s = e["source"]
        sid = e.get("source_id")
        by_src[s[:2]] += 1
        ok, why = True, ""
        if not s.startswith(EDGE_SOURCES):
            err("원천 구조 밖 엣지(적응증 · 효과 문장 · 8단계 원천 유래)", f"#{k} source 「{s}」", edge=k)
            continue
        if s.startswith("① taxonomy modality_ref"):
            it = items_by_id.get(sid)
            ok = bool(it) and e["to_family"] in it["modality_ref"]
            why = "항목 modality_ref 에 그 계열 없음"
        elif s.startswith("① P1 detail"):
            it = items_by_id.get(sid)
            tbl = p1_words["concern"] if "고민" in s else p1_words["purpose"]
            ok = bool(it) and it["category"] == "P1" and any(w in it["detail"] for w in tbl)
            why = "P1 항목 detail 에 결정 낱말 없음"
        elif s.startswith("②"):
            ok = e["to_family"] in combo_fams.get(sid, set())
            why = "problem-combos 그 고민 계열에 없음"
        elif s.startswith("③"):
            ok = (e.get("evidence") or {}).get("name") in cc_proc.get(sid, [])
            why = "CC procedures 에 그 이름 없음"
        elif s.startswith("④"):
            ok = inner(e["basis"]) in opt.get(sid, [])
            why = "optimal_combo 에 그 이름 없음"
        elif s.startswith("⑤"):
            it = items_by_id.get(sid)
            ok = bool(it) and it["category"] != "P1" and inner(e["basis"]) == it["name"] and led_items.get(sid, {}).get("kind") == "시술 이름"
            why = "항목이 없거나 이름 · 갈래(시술 이름)가 다름"
        elif s.startswith("⑥ 5단계 units"):
            ok = e["from"].startswith("목적:") and e["from"][3:] in unit_purposes.get(sid, set())
            why = "5단계 단위 시술 purposes 에 그 목적 없음"
        elif s.startswith("⑥ 5단계 목적 키"):
            p = e["from"][3:]
            ok = p in pe_purposes and set(e["to_units"]) <= pe_purposes[p]
            why = "5단계 product_evidence 에 그 목적 · 단위 시술 없음"
        elif s.startswith("⑧"):
            xd = {x["id"]: x for x in DEC["extra_concern_items"]}.get(sid) or {}
            ok = e["from"] == sid and set(e["to_units"]) <= set(xd.get("units") or [])
            why = "결정 노드 units 에 그 단위 시술 없음"
        elif s.startswith("⑦"):
            ok = sid in np7
            why = "6단계 non_packages(7단계 넘김)에 없음"
        if not ok:
            err("원천 구조에 없는 엣지", f"#{k} {s} {sid} — {why}", edge=k, source=s, source_id=sid)
        for u in e["to_units"]:
            if u not in UNITS:
                err("엣지 단위 시술 없음", f"#{k} {u}", edge=k, unit=u)

    # 원천 구조 행 수 ↔ 엣지 수(빠진 엣지)
    want_n = {
        "③": sum(len(c["procedures"]) for P in PP["problems"] for c in P["complaints"]
                 if any(i["category"] == P["problem_id"] and i["name"] == c["cc"] for i in items_by_id.values())),
        "④": sum(len(v) for v in opt.values()),
        "⑤": sum(1 for i in C["items"] if i["kind"] == "시술 이름" and i["category"] != "P1"),
        "⑥": sum(len(u["purposes"]) for u in S5["units"]),
    }
    got6 = sum(1 for e in LED["edges"] if e["source"].startswith("⑥ 5단계 units"))
    for k_, v in want_n.items():
        g = got6 if k_ == "⑥" else by_src[k_ + " "]
        if g != v:
            err("원천 구조 행 수 ≠ 엣지 수", f"{k_}: 원천 {v} · 엣지 {g}", path=k_)

    # ── 5. 엣지 부위 ──
    child = collections.defaultdict(list)
    for n in S3["nodes"]:
        if n["parent"]:
            child[n["parent"]].append(n["name"])

    def desc(x):
        out = [x]
        for c in child.get(x, []):
            out += desc(c)
        return out

    def want(sites):
        return set(sum([desc(s) if s != "얼굴" else ["얼굴 전체"] for s in sites], []))

    site_free = set(DEC["site_rules"]["site_free"])
    site_check = collections.Counter()
    for k, e in enumerate(LED["edges"]):
        us = [u for u in e["to_units"] if u in UNITS]
        sites = e.get("anchor_sites") or []
        if not sites or not us:
            site_check["앵커 부위 없음"] += 1
            continue
        w_ = want(sites)
        fl = e.get("resolve_flag") or ""
        if "후보 전부" in e["lowering"] + " " + e["basis"] or "no_unit_at_site" in fl:
            site_check["그 부위 단위 시술 없음 · 후보 전부(표시)"] += 1
            if e["lowering"].startswith("그 부위 단위 시술 없음") and "no_unit_at_site" not in fl:
                err("후보 전부인데 no_unit_at_site 표시 없음", f"#{k} {e['source']} {e.get('source_id')}", edge=k)
            if e["lowering"].startswith("그 부위 단위 시술 없음"):
                fams = {UNITS[u]["key"]["family"] for u in us}
                at = [u["id"] for u in S5["units"] if u["key"]["family"] in fams and u["key"]["site"] in w_]
                if at:
                    err("후보 전부인데 앵커 부위 단위 시술 있음(부위로 내렸어야)", f"#{k} {e['source']} {e.get('source_id')} 부위 {sites} → {at}",
                        edge=k, units_at_site=at)
            continue
        out_ = [u for u in us if UNITS[u]["key"]["site"] not in w_ and UNITS[u]["key"]["site"] not in site_free]
        if out_:
            site_check["부위 밖"] += 1
            err("엣지 단위 시술이 앵커 부위 밖", f"#{k} {e['source']} {e.get('source_id')} 부위 {sites} → {out_}",
                edge=k, sites=sites, units=out_)
        else:
            site_check["부위 안"] += 1

    # ── 6. 추천 조합 — 키 실재 · 영업 문구 ──
    def comp_units(c):
        for x in (c.get("components") or []) + (c.get("members") or []) + (c.get("upgrade") or []):
            yield from x.get("units") or []
        for m in c.get("schedule") or []:
            for x in m["items"]:
                yield from x.get("units") or []

    for c in LED["combos"]:
        for u in comp_units(c):
            if u not in UNITS:
                err("추천 조합 단위 시술 없음", f"{c['id']} {u}", combo=c["id"], unit=u)
        if c.get("sales_copy") and c["sales_copy"].get("default_response") is not False:
            err("영업 문구 기본 응답 포함", f"{c['id']}", combo=c["id"])
        if c.get("consult_copy") and c["consult_copy"].get("default_response") is not True:
            err("상담 문구 기본 응답 제외", f"{c['id']}", combo=c["id"])

    # ── 7. 원장 대조 ──
    if LED["open"]:
        err("원장 open", f"step7-concerns.json open {len(LED['open'])}", open=LED["open"])
    if LED["stale_decisions"]:
        err("원장 낡은 결정", f"step7-concerns.json stale {len(LED['stale_decisions'])}", stale=LED["stale_decisions"])
    S = LED["summary"]
    corr = LED["correspondence"]
    E_ = LED["edges"]
    recount = {
        ("correspondence", "rows"): len(corr),
        ("correspondence", "human_check"): len(gate_rows),
        ("correspondence", "gate_status"): dict(collections.Counter(r["gate_status"] for r in corr)),
        ("correspondence", "by_source"): dict(collections.Counter(r["source"] for r in corr)),
        ("edges", "total"): len(E_),
        ("edges", "by_source"): dict(collections.Counter(e["source"] for e in E_)),
        ("edges", "to_units"): sum(1 for e in E_ if e["to_units"]),
        ("edges", "family_only"): sum(1 for e in E_ if not e["to_units"] and e["to_family"]),
        ("edges", "unit_pairs"): sum(len(e["to_units"]) for e in E_),
        ("edges", "site_check"): dict(site_check),
        ("combos", "total"): len(LED["combos"]),
        ("combos", "by_kind"): dict(collections.Counter(c["kind"] for c in LED["combos"])),
        ("combos", "sales_copy_default_excluded"): sum(1 for c in LED["combos"] if c.get("sales_copy")),
        ("step8_notes", "total"): len(LED["step8_notes"]),
        ("concern_nodes", "total"): len(nodes),
    }
    for (g, k_), v in recount.items():
        if S.get(g, {}).get(k_) != v:
            err("summary 불일치", f"{g}.{k_}: 원장 {S.get(g, {}).get(k_)} ≠ 다시 센 값 {v}")

    fx = W / "step7-fixtures" / "result.json"
    fixture = None
    if fx.exists():
        r = J(fx)
        fixture = dict(passed=r["passed"], total=r["total"])

    gate_by_source = collections.Counter(corr[i]["source"] for i in gate_rows)
    res = dict(
        source=dict(path=str(SRC), expression_rows=len(src_rows), decision_table_rows=dec_rows),
        recount={f"{g}.{k_}": v for (g, k_), v in recount.items()},
        concern_nodes=dict(total=len(nodes), from_decision=len(C["extra_items"])),
        correspondence=dict(auto=len(auto_rows), gate=len(gate_rows), gate_by_source=dict(gate_by_source.most_common()),
                            exact_but_gated=exact_but_gated),
        edges=dict(by_path={k: v for k, v in sorted(by_src.items())}, structure_rows=want_n, site_check=dict(site_check)),
        origin_questions=dict(total=len(LED["origin_questions"]), by_to=dict(collections.Counter(q["to"] for q in LED["origin_questions"]))),
        source_fix=len(LED["source_fix_candidates"]),
        fixture_result=fixture,
        open=opened, stale_decisions=stale, errors=errors,
        totals=dict(open=len(opened), stale=len(stale), errors=len(errors)))
    out = json.dumps(res, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(out)
    else:
        print(out)
    print(json.dumps(dict(res["totals"], auto=len(auto_rows), gate=len(gate_rows), edges=len(E_),
                          site_out=site_check.get("부위 밖", 0)), ensure_ascii=False), file=sys.stderr)
    return 0 if not errors and not opened else 1


if __name__ == "__main__":
    sys.exit(main())
