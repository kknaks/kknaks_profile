#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD 적합성 — 시험해야 할 경우의 수를 erd-v3.2.json(+ 사전 이름 · 판은 인자)에서 **기계로** 뽑는다. 손으로 열거하지 않는다.

python3 tests/enumerate_cases.py [--erd ../erd-v3.1.json] [--dict ../erd-v3.1-dictionaries.json] [--out cases.json]

경우 id 규칙(러너가 시험 묶음의 covers 와 대조한다 — 하나라도 빠지면 FAIL):
  kind:<kind>                                  결정 kind 17 — 적용(applied) 또는 기록(recorded · build_reads=false)
  kind:<kind>:<obj>.<field>=<value>            target/new_value 구조체의 분기(`a|b` · enum(...) · `— 원천(… · …)` 목록 · `또는`)
  kind:<kind>:<obj>.<field>                    「둘 중 하나」 필드 분기(`x: … | y: … — 둘 중 하나`)
  ref:<R#>:<from|to>:<ref kind>:<개체>        edge_create ref 구조체 5 × 관계 31 의 양끝 — accept(허용 끝) / reject(허용 밖 · 만들 수 없는 관계)
  rule:<경로>:pos|neg · rule:<경로>[<원소>]     분해 규칙(resolve_rules.step2/step3 · tuple_rules.procedure/adverse)의 잎 키마다 양성·음성 · 목록은 원소마다
  enum:<열거형>=<값>                           분해·튜플 결과 열거형의 값마다(그 값을 내는 fixture 가 있어야 한다)
  conflict:<규칙>:<생애>                       충돌 ④⑥⑦⑧⑨ × 생성 · override · close(verdict 3) · ⑦ fold 닫힘 · ⑨ 결정이 세운 자리 · status 값
  order:… · stable:…                           적용 순서 ⓪①~⑦ (단계마다 kind · 이웃 단계 의존 · 같은 단계 정렬) · 결정 target 안정 키(허용 · 금지 파생 id)
  bronze:… · provenance:… · determinism:…      브론즈 판(HASHES.txt · 1판 ERD 해시 · 거부) · 출처 필수 · 재실행 바이트 동일
"""
import argparse
import json
import os
import re
import sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ERD_DIR = os.path.dirname(os.path.dirname(HERE))
REF_KINDS_RE = re.compile(r"kind:\s*((?:[a-z_]+\\?\|)+[a-z_]+)")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# 구조체 문자열 파싱 — `obj(name: TYPE — 설명, …)` 의 최상위 필드
# ---------------------------------------------------------------------------
def top_fields(s):
    """`obj(a: X, b: Y — z, c: obj(d, e))` → [(a, 'X'), (b, 'Y — z'), (c, 'obj(d, e)')] — 괄호 깊이 0 의 `,` 로 나눈다."""
    m = re.match(r"^\s*obj\((.*)\)\s*$", s, re.S)
    if not m:
        return []
    body, out, depth, cur = m.group(1), [], 0, ""
    for ch in body:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
            continue
        cur += ch
    if cur.strip():
        out.append(cur)
    fields = []
    for f in out:
        f = f.strip()
        mm = re.match(r"^([a-z_]+)\s*:\s*(.*)$", f, re.S)
        fields.append((mm.group(1), mm.group(2).strip()) if mm else (f, ""))
    return fields


def field_branches(obj, field, desc):
    """한 필드의 분기 — `a|b|c`(식별자 대안) · enum(...) · `— 원천 참조(… · …)` 목록 · `X 또는 Y`."""
    out = []
    typ = desc.split("—")[0]
    em = re.search(r"enum\(([^)]*)\)", desc)
    if em:
        out += [f"{obj}.{field}={v.strip()}" for v in em.group(1).split("|")]
    elif re.fullmatch(r"\s*(?:[a-z_]+\|)+[a-z_]+\s*", typ):
        out += [f"{obj}.{field}={v.strip()}" for v in typ.split("|")]
    lm = re.search(r"—[^(]*\(([^()]*·[^()]*)\)", desc)
    if lm:
        out += [f"{obj}.{field}={norm_label(v)}" for v in lm.group(1).split("·")]
    if " 또는 " in desc and not lm:
        for part in re.split(r"\s또는\s", desc.split("—", 1)[-1]):
            out += [f"{obj}.{field}={norm_label(v)}" for v in split_outside_parens(part, " · ")]
    return out


def split_outside_parens(s, sep):
    out, depth, cur, i = [], 0, "", 0
    while i < len(s):
        ch = s[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if depth == 0 and s.startswith(sep, i):
            out.append(cur)
            cur, i = "", i + len(sep)
            continue
        cur += ch
        i += 1
    out.append(cur)
    return [x for x in out if x.strip()]


def norm_label(v):
    """분기 이름 — 괄호 설명(닫히지 않은 꼬리 포함)을 떼고 공백을 _ 로."""
    v = re.sub(r"\([^()]*\)?", "", v.strip())
    v = re.sub(r"\s+", "_", v.strip(" _·"))
    return v


def decision_kind_cases(erd):
    cases = []
    for k in erd["decision_kinds"]:
        kind = k["kind"]
        cases.append(case(f"kind:{kind}", "kind", f"erd-v3.1.json#/decision_kinds/{kind}", "applied" if k["build_reads"] is True else "recorded"))
        for objname in ("target", "new_value"):
            fields = top_fields(k[objname])
            # 「둘 중 하나」 — `x: … | y: … — 둘 중 하나` 가 한 필드 칸에 붙어 온다
            for name, desc in fields:
                alt = re.findall(r"\|\s*([a-z_]+)\s*:", desc)
                if alt and "둘 중 하나" in desc:
                    for f in [name] + alt:
                        cases.append(case(f"kind:{kind}:{objname}.{f}", "kind", f"erd-v3.1.json#/decision_kinds/{kind}/{objname}", "applied"))
                    continue
                if name == "key" and "|" in desc:  # exclude.key: CAT-id | REF-id | 원장 locator | obj(dictionary, canonical) — kind enum 이 같은 분기를 낸다
                    continue
                for b in field_branches(objname, name, desc):
                    cases.append(case(f"kind:{kind}:{b}", "kind", f"erd-v3.1.json#/decision_kinds/{kind}/{objname}", "applied"))
        # edge_create 의 ref 구조체 kind(비고 문장)
        rm = REF_KINDS_RE.search(k.get("note", ""))
        if rm:
            for v in rm.group(1).replace("\\", "").split("|"):
                cases.append(case(f"kind:{kind}:ref.kind={v}", "kind", f"erd-v3.1.json#/decision_kinds/{kind}/note", "applied"))
    return cases


# ---------------------------------------------------------------------------
# ref 구조체 × 관계 양끝
# ---------------------------------------------------------------------------
def ref_kinds(erd):
    k = next(x for x in erd["decision_kinds"] if x["kind"] == "edge_create")
    return REF_KINDS_RE.search(k["note"]).group(1).replace("\\", "").split("|")


def entity_keys(erd):
    return [e["key"] for e in erd["entities"]]


def meta_types(erd):
    """「임의 개체」를 끝으로 받는 관계의 출발 개체(R23 conflict · R24 decision) — 결정·충돌 기록 개체 자신은 ref 구조체로 가리킬 수 없다."""
    out = []
    for r in erd["relations"]:
        if "임의" in r["to"]:
            out += [t.strip() for t in r["from"].split("|")]
    return out


def proc_axis(erd):
    # ERD §3 · edge_end_kinds(procedure · modality · subcategory · product · unresolved) → 개체 이름
    m = {"subcategory": "modality_subcategory"}
    return [m.get(x, x) for x in erd["edge_end_kinds"] if x != "unresolved"]


def allowed(erd, rel, side):
    """관계 끝 문자열 → 허용 개체 종류. `proc_axis` 전개 · `x(y)` 의 괄호(부분 종류)는 x · `(임의 개체|엣지)`·`(모든 개체…)` 는 개체 전부."""
    r = next(x for x in erd["relations"] if x["id"] == rel)
    s = r[side]
    ents = entity_keys(erd)
    if "임의" in s or "모든" in s:
        return list(ents)
    out = []
    for t in s.split("|"):
        t = re.sub(r"\(.*?\)", "", t).strip()
        if t == "proc_axis":
            out += proc_axis(erd)
        elif t in ents:
            out.append(t)
    return out


def producible(erd, dic, kind):
    """ref kind → 그것이 풀릴 수 있는 개체 종류(ERD §5.2 ref 구조체 문장 · 개체 정의에서)."""
    ents = entity_keys(erd)
    if kind in ("anchor", "procedure_tuple"):
        # anchor: CAT-/REF- (§1.1 anchor → 그 튜플) · tuple: obj(what_id, site_id, technique_id) — 시술 튜플
        return ["procedure"]
    if kind == "adverse_tuple":
        return ["adverse_effect"]
    if kind == "dict_value":
        # 사전 값이 곧 개체 식별인 개체: 개체 이름 = 사전 이름(또는 사전 이름의 _label · _name 접미 제거)
        names = {d["name"] for d in dic["dictionaries"]}
        out = []
        for e in ents:
            if e in names or f"{e}_label" in names or f"{e}_name" in names:
                out.append(e)
        return out
    if kind == "locator":
        # 원장 locator → 그 잎을 출처로 가진 실버 레코드 — 원장 출처 속성이 있는 개체 전부(기록 개체 conflict·decision 제외)
        meta = set(meta_types(erd))
        return [e["key"] for e in erd["entities"] if e["key"] not in meta and any(".json:" in s for a in e["attrs"] for s in a["sources"])]
    return []


def ref_cases(erd, dic):
    cases = []
    kinds = ref_kinds(erd)
    prod = {k: producible(erd, dic, k) for k in kinds}
    for r in erd["relations"]:
        rel = r["id"]
        al = {side: allowed(erd, rel, side) for side in ("from", "to")}
        creatable = all(any(t in al[side] for k in kinds for t in prod[k]) for side in ("from", "to"))
        for side in ("from", "to"):
            for k in kinds:
                for t in prod[k]:
                    ok = creatable and t in al[side]
                    cases.append(case(f"ref:{rel}:{side}:{k}:{t}", "ref", f"erd-v3.1.json#/relations/{rel}/{side}", "accept" if ok else "reject",
                                      relation=rel, side=side, ref_kind=k, end_type=t, creatable=creatable, allowed=al[side]))
    return cases


# ---------------------------------------------------------------------------
# 분해 규칙 · 열거형
# ---------------------------------------------------------------------------
RULE_ROOTS = [("resolve_rules", "step2_decompose"), ("resolve_rules", "step3_assemble"), ("tuple_rules", "procedure"), ("tuple_rules", "adverse"),
              ("resolve_rules", "tokenize"), ("tuple_rules", "phrase_kinds"), ("tuple_rules", "equipment")]   # v3.2: 토큰화 · 문구 종류·노드·⑦ 규칙 · 장비 자동 등록(빌더가 읽는 규칙 데이터 · 씨앗 규칙은 ERD 승인 묶음이라 빌더 밖)
RESULT_ENUMS = ["reference.result", "reference.unresolved_reason", "reference.status", "procedure.what_kind", "procedure.status", "procedure.technique_origin", "catalog_item.tuple_status",
                "target_depth", "R12.member_mode", "adverse_effect.event_kind", "adverse_effect.status", "adverse_effect.raw_reason", "adverse_effect.site_basis", "adverse_effect.site_ref_kind",
                "adverse_effect.qualifier_basis", "adverse_expression.match_status", "adverse_expression.unlinked_reason", "site.kind",
                # v3.2 — 분해·결과 열거형(없는 판에서는 건너뛴다)
                "phrase_dictionary.status", "table_line.ref_status", "R15.inheritance.basis", "R15.layer", "product.origin", "evidence_statement.kind", "tokenize.kind"]


def walk(v, path):
    if isinstance(v, dict):
        for k, x in v.items():
            yield from walk(x, f"{path}.{k}")
    else:
        yield path, v


def list_item_label(x):
    if isinstance(x, dict):
        return x.get("word") or x.get("value") or json.dumps(x, ensure_ascii=False)
    s = str(x)
    return s if len(s) <= 24 else None


def rule_cases(erd):
    cases = []
    for a, b in RULE_ROOTS:
        if b not in erd[a]:
            continue
        for path, v in walk(erd[a][b], f"{a}.{b}"):
            src = f"erd-v3.1.json#/{path.replace('.', '/')}"
            if isinstance(v, list):
                for i, x in enumerate(v):
                    lab = list_item_label(x)
                    cases.append(case(f"rule:{path}[{lab if lab is not None else i}]", "rule", src, "pos"))
                cases.append(case(f"rule:{path}:neg", "rule", src, "neg"))
            else:
                cases.append(case(f"rule:{path}:pos", "rule", src, "pos"))
                cases.append(case(f"rule:{path}:neg", "rule", src, "neg"))
    for en in RESULT_ENUMS:
        for v in erd["enums"].get(en, []):   # 판마다 열거형이 다르다(v3.2: adverse_expression.* · raw_reason 없음)
            cases.append(case(f"enum:{en}={v}", "rule", f"erd-v3.1.json#/enums/{en}", "produced"))
    return cases


# ---------------------------------------------------------------------------
# 충돌 · 적용 순서 · 안정 키 · 브론즈
# ---------------------------------------------------------------------------
def conflict_cases(erd):
    cases = []
    stage6 = next(s["kinds"] for s in erd["decision_apply_order"] if s["stage"] == "⑥")
    verdicts = erd["enums"]["conflict.close_verdict"]
    for rr in erd["enums"]["conflict.rule_ref"]:
        cases.append(case(f"conflict:{rr}:create", "conflict", "erd-v3.1.json#/enums/conflict.rule_ref", "created"))
        for k in stage6:
            if k == "conflict_close":
                for v in verdicts:
                    cases.append(case(f"conflict:{rr}:conflict_close={v}", "conflict", "erd-v3.1.json#/decision_kinds/conflict_close", "dismissed"))
            else:
                cases.append(case(f"conflict:{rr}:{k}", "conflict", f"erd-v3.1.json#/decision_kinds/{k}", "resolved"))
    for s in erd["enums"]["conflict.status"]:
        cases.append(case(f"conflict:status={s}", "conflict", "erd-v3.1.json#/enums/conflict.status", "produced"))
    if erd.get("fold_close_rule"):
        cases.append(case("conflict:⑦:fold_approve_closes_pair", "conflict", "erd-v3.1.json#/fold_close_rule", "resolved"))
        cases.append(case("conflict:⑦:fold_approve_not_pair", "conflict", "erd-v3.1.json#/fold_close_rule", "open"))
    if erd.get("decision_anchor_rule"):
        cases.append(case("conflict:⑨:established_by_decision", "conflict", "erd-v3.1.json#/decision_anchor_rule", "resolved"))
    cases.append(case("conflict:stable_key:no_target", "conflict", "erd-v3.1.json#/id_rule/conflict_decision_ids", "no_target"))
    return cases


def order_cases(erd):
    cases = []
    stages = erd["decision_apply_order"]
    for s in stages:
        for k in s["kinds"]:
            cases.append(case(f"order:{s['stage']}:{k}", "order", "erd-v3.1.json#/decision_apply_order", "stage"))
    for a, b in zip(stages, stages[1:]):
        cases.append(case(f"order:{a['stage']}->{b['stage']}", "order", "erd-v3.1.json#/decision_apply_order", "depends"))
    for k in erd["decision_kinds"]:
        if "적용 ⓪" in k.get("note", ""):
            cases.append(case(f"order:⓪:{k['kind']}", "order", f"erd-v3.1.json#/decision_kinds/{k['kind']}", "stage"))
    if "decided_at" in erd["decision_apply_order_rule"]:
        cases.append(case("order:same_stage=decided_at", "order", "erd-v3.1.json#/decision_apply_order_rule", "sorted"))
    if "id 순" in erd["decision_apply_order_rule"]:
        cases.append(case("order:same_stage=id", "order", "erd-v3.1.json#/decision_apply_order_rule", "sorted"))
    for s in erd["enums"]["decision.status"]:
        cases.append(case(f"order:status={s}", "order", "erd-v3.1.json#/decision_build_rule", "applied" if s == "approved" else "listed"))
    # 결정 target 안정 키 — 허용 키 · 금지 파생 id
    rule = erd["decision_target_rule"]
    allow, forbid = rule.split("**금지**")[0], rule.split("**금지**")[1].split("·")[0:4]
    for p in sorted(set(re.findall(r"\b(CAT|REF|MOD|SUB|PRD|SIT|TEC)-", allow))):
        cases.append(case(f"stable:allow:{p}-", "order", "erd-v3.1.json#/decision_target_rule", "accepted"))
    for p in sorted(set(re.findall(r"#([ms])<i>", allow))):
        cases.append(case(f"stable:allow:#{p}<i>", "order", "erd-v3.1.json#/decision_target_rule", "accepted"))
    for word, cid in (("원장 locator", "locator"), ("사전 값", "dict_value"), ("conflict 안정 키", "conflict_key")):
        if word in allow:
            cases.append(case(f"stable:allow:{cid}", "order", "erd-v3.1.json#/decision_target_rule", "accepted"))
    for p in sorted(set(re.findall(r"\b(PRC|ADV|CFL)-", rule.split("**금지**")[1]))):
        cases.append(case(f"stable:forbid:{p}-", "order", "erd-v3.1.json#/decision_target_rule", "rejected"))
    return cases


def bronze_cases(erd):
    b = erd["bronze"]
    cases = []
    if b.get("hashes_file"):
        cases += [case("bronze:hashes_txt:match", "bronze", "erd-v3.1.json#/bronze/hashes_file", "built"),
                  case("bronze:hashes_txt:mismatch", "bronze", "erd-v3.1.json#/bronze/hashes_file", "refused"),
                  case("bronze:hashes_txt:missing_file", "bronze", "erd-v3.1.json#/bronze/hashes_file", "refused"),
                  case("bronze:hashes_txt:extra_file", "bronze", "erd-v3.1.json#/bronze/hashes_file", "refused")]
    if b.get("changelog") or any(str(k).startswith("changelog") for k in b):   # v3.3: bronze.changelog_has_row_3(판 행 확인) — CHANGELOG 판은 manifest bronze_version 에
        cases.append(case("bronze:changelog:version", "bronze", "erd-v3.1.json#/bronze/changelog", "manifest"))
    if erd.get("previous_version") and any(s.get("v1_sha256") for s in erd["source_files"]):
        cases.append(case("bronze:v1:erd_hash_without_hashes_txt", "bronze", "erd-v3.1.json#/source_files", "built"))
    cases.append(case("bronze:step1:erd_hash", "bronze", "erd-v3.1.json#/source_files", "refused"))
    if "출처" in erd["layers"]["silver"]:
        cases += [case("provenance:every_value", "bronze", "erd-v3.1.json#/layers/silver", "all"),
                  case("provenance:value_without_source_fails", "bronze", "erd-v3.1.json#/layers/silver", "refused")]
    cases.append(case("determinism:rerun_bytes", "bronze", "erd-v3.1.json#/layers/silver", "identical"))
    return cases


def case(id_, category, source, expect, **kw):
    d = OrderedDict([("id", id_), ("category", category), ("source", source), ("expect", expect)])
    d.update(kw)
    return d


def enumerate_all(erd, dic):
    cases = decision_kind_cases(erd) + ref_cases(erd, dic) + rule_cases(erd) + conflict_cases(erd) + order_cases(erd) + bronze_cases(erd)
    seen, out = set(), []
    fname = f"erd-{erd.get('erd_version', 'v3.1')}.json"
    for c in cases:
        c["source"] = c["source"].replace("erd-v3.1.json", fname)   # 경우의 출처 = 읽은 ERD 판
        if c["id"] in seen:
            continue
        seen.add(c["id"])
        out.append(c)
    return out


def summary(cases):
    by = Counter(c["category"] for c in cases)
    ref = Counter(c["expect"] for c in cases if c["category"] == "ref")
    return OrderedDict([("total", len(cases)), ("by_category", dict(by)), ("ref_accept_reject", dict(ref))])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--erd", default=os.path.join(ERD_DIR, "erd-v3.3.json"))
    ap.add_argument("--dict", default=os.path.join(ERD_DIR, "erd-v3.3-dictionaries.json"))
    ap.add_argument("--out")
    a = ap.parse_args()
    cases = enumerate_all(load(a.erd), load(a.dict))
    doc = OrderedDict([("erd", os.path.basename(a.erd)), ("summary", summary(cases)), ("cases", cases)])
    s = json.dumps(doc, ensure_ascii=False, indent=1)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(s + "\n")
        print(json.dumps(doc["summary"], ensure_ascii=False))
    else:
        sys.stdout.write(s + "\n")


if __name__ == "__main__":
    main()
