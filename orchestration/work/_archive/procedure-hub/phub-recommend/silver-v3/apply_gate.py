#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""게이트 답 → 결정 파일. 게이트 자료(out/gate/batch2b.json · batch3.json · batch4.json — 같은 스키마)에서 사용자가 고른 옵션의 decision_payload 를 그대로 파일로 쓴다.

python3 apply_gate.py --answers answers.json [--out decisions/batch2b/] [--gate out/gate/batch2b.json]
                      [--recommended] [--dry-run] [--decided-by 사용자(이건학)] [--date YYYY-MM-DD] [--note ...] [--force]
묶음 3: python3 apply_gate.py --gate out/gate/batch3.json --out decisions/batch3b/ --answers answers.json
묶음 4: python3 apply_gate.py --gate out/gate/batch4.json --out decisions/batch4/ --answers answers.json   (동의어 · 하위 id 예 "b4-adv/011")
묶음 5: python3 apply_gate.py --gate out/gate/batch5.json --answers answers.json   (ERD v3.2 노드 단위 → decisions/batch5/ · 하위 id 예 "node/DIC-…" · "dup/…" · "seed-site/…")
  (--out 을 안 주면 게이트 파일 이름으로 정한다: batch2b.json → decisions/batch2b/ · batch3.json → decisions/batch3b/ · batch4.json → decisions/batch4/ · batch5.json → decisions/batch5/)

answers.json = {"<항목 id 또는 하위 id>": "<옵션 key>" | {"choice": "<옵션 key>", "note": "<사용자 메모 — reason 에 붙는다>"}, ...}
  - 하위 항목이 있는 항목은 하위 id(예 "same-three-cells-21/07")로 답한다. 항목 id 에 답하면 그 항목의 하위 전부에 같은 key 를 쓴다
    (그 key 가 없는 하위는 오류).
  - --recommended: 답이 없는 자리를 recommended 로 채운다(recommended=null 인 자리는 비워 둔다) — 「전부 추천대로」는 빈 {} + --recommended.
  - 옵션의 decision_payload 가 null(결정 없음 · 지금대로)이면 파일을 쓰지 않는다.
쓰는 파일: <out>/<payload id>.json — payload 그대로 + status=approved · decided_by · decided_at · approval_note · gate_answer.
같은 kind·target 을 가리키는 결정이 둘 이상 나오면(예 볼뉴머: volnewmer-m4-m9 와 same-three-cells-21/07) 내용이 같으면 하나만 쓰고,
다르면 거부한다(exit 1).
"""
import argparse
import copy
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lib.decisions import validate  # noqa: E402


def leaves(items):
    for it in items:
        subs = it.get("subitems") or []
        if subs:
            for s in subs:
                yield it, s
        else:
            yield it, it


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--answers", required=True)
    ap.add_argument("--gate", default=os.path.join(HERE, "out", "gate", "batch2b.json"))
    ap.add_argument("--out", default=None, help="기본: batch2b.json → decisions/batch2b/ · batch3.json → decisions/batch3b/ · batch4.json → decisions/batch4/ · batch5.json → decisions/batch5/")
    ap.add_argument("--recommended", action="store_true", help="답 없는 자리를 recommended 로")
    ap.add_argument("--dry-run", action="store_true", help="쓰지 않고 무엇을 쓸지만 출력")
    ap.add_argument("--decided-by", default="사용자(이건학)")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--note", default=None, help="기본: 「결정 묶음 2B|3B|4 — 게이트에서 사용자가 고름」(게이트 파일 이름으로)")
    ap.add_argument("--force", action="store_true", help="이미 있는 다른 내용의 파일을 덮는다")
    a = ap.parse_args()
    gname = os.path.basename(a.gate)
    sub, tag = ("batch5", "5") if "batch5" in gname else ("batch4", "4") if "batch4" in gname else ("batch3b", "3B") if "batch3" in gname else ("batch2b", "2B")  # 그 밖(2B 고정본 _gate-batch2b-3차.json 등)은 예전 기본값 2B
    if a.out is None:
        a.out = os.path.join(HERE, "decisions", sub)
    if a.note is None:
        a.note = f"결정 묶음 {tag} — 게이트에서 사용자가 고름"

    items = json.load(open(a.gate, encoding="utf-8"))
    answers = json.load(open(a.answers, encoding="utf-8"))
    by_id = {s["id"]: (it, s) for it, s in leaves(items)}
    tops = {it["id"]: it for it in items}
    errs = []
    chosen = {}  # leaf id -> option key
    notes = {}   # leaf id -> 사용자 메모(결정 reason 에 붙인다)
    excl = {}   # 묶음 5 축소본 씨앗 「제외할 것 선택」 — {"choice": "select", "exclude": [값 …]}
    for k, v in list(answers.items()):
        if isinstance(v, dict) and v.get("exclude") is not None:
            excl[k] = list(v["exclude"])
        if isinstance(v, dict):  # {"choice": key, "note": 메모} 꼴도 받는다
            if v.get("note"):
                if k in tops and tops[k].get("subitems"):
                    for s_ in tops[k]["subitems"]:
                        notes[s_["id"]] = v["note"]
                else:
                    notes[k] = v["note"]
            answers[k] = v = v["choice"]
    for k, v in answers.items():
        if k in by_id:
            chosen[k] = v
        elif k in tops and tops[k].get("subitems"):
            for s in tops[k]["subitems"]:
                chosen[s["id"]] = v
        else:
            errs.append(f"모르는 자리 {k}")
    if a.recommended:
        for lid, (_, s) in by_id.items():
            if lid not in chosen and s.get("recommended") is not None:
                chosen[lid] = s["recommended"]

    plan, skipped, seen, warns = [], [], {}, []
    work = []   # (자리, 옵션 key, 옵션, 결정 본문)
    for lid, key in chosen.items():
        _, s = by_id[lid]
        o = next((x for x in s["options"] if x["key"] == key), None)
        if o is None:
            errs.append(f"{lid}: 옵션 {key} 없음 (있는 것 {[x['key'] for x in s['options']]})")
            continue
        many = o.get("decision_payloads")
        if o.get("decision_payload") is None and many:
            # 일괄 옵션(묶음 5 축소본) — 결정 여럿 · select 는 exclude 값을 제외 기록(scope_review)으로
            ex = set(excl.get(lid, []))
            unknown = ex - {x.get("seed_value") for x in many}
            if unknown:
                errs.append(f"{lid}: exclude 값 {sorted(unknown)} 이 표에 없다")
                continue
            for q in many:
                work.append((lid, key, o, o["exclude_payloads"][q["seed_value"]] if key == "select" and q.get("seed_value") in ex else q))
            continue
        if o.get("decision_payload") is None:
            skipped.append((lid, key))
            continue
        work.append((lid, key, o, o["decision_payload"]))
    for lid, key, o, p in work:
        if o.get("builder_applies_now") is False:
            warns.append(f"{lid}: {key} — 지금 빌더가 이 결정을 적용할 대상이 없다(builder_applies_now=false · apply_log no_target/rejected 예상)")
        d = copy.deepcopy(p)
        d.pop("seed_value", None)
        rule_by = d.get("decided_by") if str(d.get("decided_by") or "").startswith("rule:") else None   # 규칙 결정은 decided_by=rule:<id> 그대로(사용자 승인은 approval_note)
        d.update(status="approved", decided_by=rule_by or a.decided_by, decided_at=d.get("decided_at") if rule_by else a.date, approval_note=a.note + (f" · 승인 {a.decided_by} {a.date}" if rule_by else ""),
                 gate_answer={"item": lid, "option": key, "label": o["label"]})
        if notes.get(lid):
            d["reason"] = d["reason"] + " · 사용자 메모: " + notes[lid]
            d["gate_answer"]["note"] = notes[lid]
        store = d.pop("_store", None)
        ve = validate(d)
        if ve:
            errs.append(f"{lid}: {ve}")
            continue
        tk = d["kind"] + json.dumps(d["target"], sort_keys=True, ensure_ascii=False)
        if d["kind"] == "event_split":  # 한 사건에서 여러 값을 따로 떼는 것은 서로 다른 결정(동상 · 지방괴사 ← 괴사)
            tk += json.dumps(sorted(e["canonical"] for e in d["new_value"]["new_events"]), ensure_ascii=False)
        if d["kind"] == "dictionary_add":  # target 이 사전 이름뿐 — 값(정준값·동의어)마다 다른 결정
            tk += json.dumps([d["new_value"].get("canonical"), sorted(str(x if isinstance(x, str) else x.get("value")) for x in d["new_value"].get("synonyms") or [])], ensure_ascii=False)
        if tk in seen:
            if json.dumps(seen[tk][1], sort_keys=True, ensure_ascii=False) == json.dumps(d["new_value"], sort_keys=True, ensure_ascii=False):
                skipped.append((lid, f"{key} (= {seen[tk][0]} 와 같은 결정 — 하나만 쓴다)"))
                continue
            errs.append(f"{lid} 와 {seen[tk][0]} 가 같은 kind·target 을 다르게 정한다 — 한쪽만 답한다")
            continue
        seen[tk] = (lid, d["new_value"])
        ids = [x[1]["id"] for x in plan]
        if d["id"] in ids:
            errs.append(f"{lid}: 결정 id {d['id']} 중복")
            continue
        if store:
            d["_store"] = store
        plan.append((lid, d))

    if "batch5" in gname:
        # 묶음 5 — 원장 사건 노드 하나에 서로 다른 처분(부작용 맞음 · 아님 · 접기)을 함께 고르면 거부(노드 자리와 ⑦ 쌍 자리에서 같은 노드를 다르게)
        per = {}
        for lid, d in plan:
            t = d["target"]
            node_ = (d["new_value"].get("canonical") if d["kind"] == "dictionary_add" and t.get("dictionary") == "adverse_event_type" else
                     (t.get("key") or {}).get("canonical") if d["kind"] == "exclude" else t.get("canonical") if d["kind"] == "fold_approve" and t.get("dictionary") == "adverse_event_type" else None)
            if node_ is None:
                continue
            act = (d["kind"], json.dumps(d["new_value"], sort_keys=True, ensure_ascii=False))
            if node_ in per and per[node_][1] != act:
                errs.append(f"노드 「{node_}」 에 처분이 둘 — {per[node_][0]} 와 {lid} (한 자리만 답한다)")
            per.setdefault(node_, (lid, act))
        # 같은 ⑦ 쌍을 묶음 자리와 개별 자리에서 「같다」·「다르다」로 다르게 고르면 거부
        verdict = {}
        for lid, d in plan:
            t = d["target"]
            if d["kind"] == "fold_approve" and t.get("dictionary") == "adverse_event_type":
                k, v = frozenset((t.get("canonical"), t.get("into"))), "same"
            elif d["kind"] == "conflict_close" and (t.get("conflict_key") or {}).get("pair"):
                k, v = frozenset(t["conflict_key"]["pair"].split("|")[2:]), "different"
            else:
                continue
            if k in verdict and verdict[k][1] != v:
                errs.append(f"⑦ 쌍 {sorted(k)} 을 {verdict[k][0]} 와 {lid} 가 다르게 고른다 — 한쪽만 답한다")
            verdict.setdefault(k, (lid, v))
    if errs:
        print("오류:", *errs, sep="\n  ", file=sys.stderr)
        sys.exit(1)
    print(f"답 {len(chosen)} 자리 → 결정 파일 {len(plan)} · 결정 없음(지금대로) {len(skipped)} → {a.out}")
    for w in warns:
        print("  ⚠", w)
    for lid, d in sorted(plan, key=lambda x: x[1]["id"]):
        print(f"  {d['id']}  {d['kind']:<22} ← {lid} = {d['gate_answer']['option']}")
    for lid, key in sorted(skipped):
        print(f"  (결정 없음)  ← {lid} = {key}")
    if a.dry_run:
        print("드라이런 — 쓰지 않았다")
        return
    os.makedirs(a.out, exist_ok=True)
    for _, d in plan:
        store = d.pop("_store", None)
        od = os.path.join(HERE, "decisions", store) if store else a.out   # 규칙 결정은 제 자리(decisions/batch5-rule/)의 proposed 파일을 approved 로
        os.makedirs(od, exist_ok=True)
        path = os.path.join(od, d["id"] + ".json")
        body = json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
        prev_proposed = os.path.exists(path) and json.load(open(path, encoding="utf-8")).get("status") == "proposed"
        if os.path.exists(path) and open(path, encoding="utf-8").read() != body and not a.force and not prev_proposed:
            print(f"이미 있는 다른 내용 {path} — --force 로 덮는다", file=sys.stderr)
            sys.exit(1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)
    print(f"썼다 → {a.out}")


if __name__ == "__main__":
    main()
