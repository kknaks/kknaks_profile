#!/usr/bin/env python3
"""실버 9단계(설명 사실) 원장 점검 — 읽기만 · 표준 라이브러리.

1. 낡음: step9-apply.py 를 임시 폴더에 두 번 → 두 번 바이트 같음(결정론) · 정본 step9-explanations.json · .md 와 바이트 같음
2. open 0 · 사람 확인 0 · summary 셈 = 레코드에서 다시 센 값
3. 붙음 레코드: 붙는 노드가 실버(step1 ledger_id · step2 계열 · step5 단위 시술 · step7 고민 노드)에 있음 · section 이 허용 집합(SPEC-005 §4-3 + safety.management) 안
4. 붙이지 않음 · 대조본 · source_conflict 레코드는 노드 0
5. D9-3: ② 칸은 emit 에 숫자 있는 레코드 하나(resolved) · alternatives ∩ emit = ∅ · same_as 로 접힌 레코드는 emit 밖 · ③ 은 multi_source · fact_ids = {노드}#{section}#step9[{원천 경로}]
6. 값 사전 = 원천 reaction_levels · severity_levels 칸 수 · section_map 행이 8단계 실버 레코드를 가리킴
7. 고정 시험 결과(step9-fixtures/result.json) 전부 PASS
--selftest: 원장 사본에 틀린 값 10가지를 넣어 각각 errors 로 잡히는지 본다.
"""
import argparse
import copy
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
SECTIONS = {"overview", "method", "ops", "dose", "market", "timeline", "aftercare", "recovery", "safety.side_effects", "safety.complications",
            "safety.pih", "site_caution", "products", "emergency", "disclosure", "checks", "evidence", "safety.management"}
FILES = ["step9-apply.py", "step9-decisions.json", "step1-products.json", "step2-families.json", "step5-units.json", "step7-concerns.json", "step8-relations.json"]


def silver_nodes(work):
    J = lambda f: json.load(open(work / f, encoding="utf-8"))
    s1, s2, s5, s7 = J("step1-products.json"), J("step2-families.json"), J("step5-units.json"), J("step7-concerns.json")
    con = s7["concerns"]
    concerns = {x["id"] for k in ("categories", "subcategories") for x in con[k] if x.get("node")}
    concerns |= {x["id"] for x in con["items"] if x.get("kind") == "고민"} | {x["id"].split("-")[0] for x in con["extra_items"]}
    return {"product": {x["ledger_id"] for x in s1["items"]}, "family": {f["id"] for f in s2["families"]},
            "unit_procedure": {u["id"] for u in s5["units"]}, "concern": concerns}


def check(o, work, dec):
    errors = []
    E = lambda t, **kw: errors.append(dict(type=t, **kw))
    s = o["summary"]
    if o["open"]:
        E("open 남음", n=len(o["open"]))
    if s.get("human_check"):
        E("사람 확인 남음", n=s["human_check"])
    rec = {r["id"]: r for r in o["records"]}
    nodes = silver_nodes(work)
    if s["records"] != len(o["records"]) or s["attached_records"] != sum(1 for r in o["records"] if r["status"] == "붙음") \
            or s["node_slots"] != len(o["node_slots"]) or s["facts_out"] != sum(len(e["emit"]) for e in o["node_slots"]) \
            or s["value_dictionary"] != len(o["value_dictionary"]) or s["source_conflicts"] != len(o["source_conflicts"]):
        E("summary 셈 불일치")
    for r in o["records"]:
        ns = r["attach"]["nodes"]
        if r["status"] == "붙음":
            if not ns:
                E("붙음인데 노드 없음", id=r["id"])
            for n in ns:
                k, _, i = n.partition(":")
                if i not in nodes.get(k, set()):
                    E("붙는 노드가 실버에 없음", id=r["id"], node=n)
            if r["section"] not in SECTIONS:
                E("section 이 허용 집합 밖", id=r["id"], section=r["section"])
        elif ns:
            E("붙이지 않음 · 대조본인데 노드 있음", id=r["id"], status=r["status"])
    num_re = re.compile(dec["conflict_resolution"]["numeric_regex"])
    zero = dec["conflict_resolution"]["zero_words"]
    has_num = lambda t: bool(num_re.search(t)) or any(z in t for z in zero)
    for e in o["node_slots"]:
        emit = set(e["emit"])
        for rid in e["emit"]:
            if rid not in rec or rec[rid]["status"] != "붙음" or e["node"] not in rec[rid]["attach"]["nodes"]:
                E("emit 레코드가 그 노드에 붙어 있지 않음", node=e["node"], slot=e["slot"], id=rid)
        if e["class"] == "②":
            if sum(1 for x in e["emit"] if has_num(rec[x]["text"])) != 1 or not e.get("resolved") or e["resolved"] not in emit:
                E("② 인데 숫자 값이 하나가 아님(resolved 하나)", node=e["node"], slot=e["slot"])
            if set(e.get("alternatives") or []) & emit:
                E("alternatives 가 emit 에 섞임", node=e["node"], slot=e["slot"])
        if e["class"] == "③" and not e.get("multi_source"):
            E("③ 인데 multi_source 표시 없음", node=e["node"], slot=e["slot"])
        folded = {x for v in (e.get("same_as") or {}).values() for x in v}
        if folded & emit:
            E("same_as 로 접힌 레코드가 emit 에 있음", node=e["node"], slot=e["slot"])
        want = [f"{e['node']}#{e['section']}#step9[{rid[3:]}]" for rid in e["emit"]]
        if e["fact_ids"] != want:
            E("fact_ids 꼴이 G9-1 과 다름", node=e["node"], slot=e["slot"])
    src = Path(dec["source"]["path"])
    raw_n = sum(len(json.load(open(src / "post-procedure-timeline.json", encoding="utf-8")).get("reaction_levels") or {}) for _ in [0]) \
        + len(json.load(open(src / "complications.json", encoding="utf-8")).get("severity_levels") or {})
    if len(o["value_dictionary"]) != raw_n:
        E("값 사전 수가 원천과 다름", got=len(o["value_dictionary"]), raw=raw_n)
    s8 = json.load(open(work / "step8-relations.json", encoding="utf-8"))["safety"]
    ids = {x["id"] for x in s8["complications"] + s8["side_effects"]}
    for x in o["section_map"]:
        if x["silver_id"] not in ids or x["section"] not in SECTIONS:
            E("section_map 이 8단계 실버 레코드 · 허용 section 밖", path=x["path"])
    return errors


def main():
    AP = argparse.ArgumentParser()
    AP.add_argument("--work", required=True)
    AP.add_argument("--out", required=True)
    AP.add_argument("--selftest", action="store_true")
    a = AP.parse_args()
    work = Path(a.work).resolve()
    dec = json.load(open(work / "step9-decisions.json", encoding="utf-8"))
    o = json.load(open(work / "step9-explanations.json", encoding="utf-8"))
    errors = check(o, work, dec)
    outs = []
    for _ in range(2):
        td = Path(tempfile.mkdtemp())
        p = subprocess.run([sys.executable, str(work / "step9-apply.py"), "--out", str(td)], capture_output=True, text=True)
        outs.append((p.returncode, td))
    if any(c != 0 for c, _ in outs):
        errors.append(dict(type="step9-apply 실행 실패"))
    else:
        for f in ("step9-explanations.json", "step9-explanations.md"):
            b1, b2 = (outs[0][1] / f).read_bytes(), (outs[1][1] / f).read_bytes()
            if b1 != b2:
                errors.append(dict(type="결정론 아님 — 두 번 실행 바이트 다름", file=f))
            if b1 != (work / f).read_bytes():
                errors.append(dict(type="정본 낡음 — 재생성 결과와 바이트 다름", file=f))
    for _, td in outs:
        shutil.rmtree(td, ignore_errors=True)
    fx = work / "step9-fixtures" / "result.json"
    if not fx.exists() or json.load(open(fx, encoding="utf-8")).get("fail"):
        errors.append(dict(type="고정 시험 FAIL 또는 결과 없음"))
    selftest = []
    if a.selftest:
        emit2 = next(e for e in o["node_slots"] if e["class"] == "②")
        e3 = next(e for e in o["node_slots"] if e["class"] == "③")
        unat = next(r for r in o["records"] if r["status"].startswith("붙이지 않음"))
        att = next(r for r in o["records"] if r["status"] == "붙음")

        def t(name, expect, fn):
            m = copy.deepcopy(o)
            fn(m)
            got = {x["type"] for x in check(m, work, dec)}
            selftest.append(dict(tamper=name, expect=expect, caught=expect in got))

        t("open 하나 넣음", "open 남음", lambda m: m["open"].append({"type": "x"}))
        t("② 에 alternatives 섞음", "alternatives 가 emit 에 섞임",
          lambda m: next(e for e in m["node_slots"] if e["node"] == emit2["node"] and e["slot"] == emit2["slot"])["emit"].append(emit2["alternatives"][0]))
        t("② resolved 지움", "② 인데 숫자 값이 하나가 아님(resolved 하나)",
          lambda m: next(e for e in m["node_slots"] if e["node"] == emit2["node"] and e["slot"] == emit2["slot"]).update(resolved=None))
        t("③ multi_source 지움", "③ 인데 multi_source 표시 없음",
          lambda m: next(e for e in m["node_slots"] if e["node"] == e3["node"] and e["slot"] == e3["slot"]).pop("multi_source"))
        t("원문 보관에 노드 붙임", "붙이지 않음 · 대조본인데 노드 있음",
          lambda m: next(r for r in m["records"] if r["id"] == unat["id"])["attach"].update(nodes=["family:M1"]))
        t("실버에 없는 노드", "붙는 노드가 실버에 없음",
          lambda m: next(r for r in m["records"] if r["id"] == att["id"])["attach"]["nodes"].append("unit_procedure:U5-999"))
        t("section 비움", "section 이 허용 집합 밖", lambda m: next(r for r in m["records"] if r["id"] == att["id"]).update(section=None))
        t("값 사전 하나 지움", "값 사전 수가 원천과 다름", lambda m: m["value_dictionary"].pop())
        t("summary 셈 바꿈", "summary 셈 불일치", lambda m: m["summary"].update(records=m["summary"]["records"] + 1))
        t("fact id 꼴 바꿈", "fact_ids 꼴이 G9-1 과 다름", lambda m: m["node_slots"][0]["fact_ids"].__setitem__(0, "x"))
    out = dict(work=str(work), summary=o["summary"], errors=errors, selftest=selftest)
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    s = o["summary"]
    print(f"레코드 {s['records']} · 붙음 {s['attached_records']} · 칸 {s['node_slots']} · fact {s['facts_out']} · D9-3 {json.dumps(s['d93'], ensure_ascii=False)} · "
          f"open {s['open']} · errors {len(errors)}" + (f" · selftest {sum(x['caught'] for x in selftest)}/{len(selftest)} 잡힘" if selftest else "") + f" → {a.out}")
    return 1 if errors or (selftest and not all(x["caught"] for x in selftest)) else 0


if __name__ == "__main__":
    raise SystemExit(main())
