#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v3.3 검산 — v3.2 의 52 항목(같은 뜻으로 v3.3 산출물에 다시) + A~G 각각 1 이상.
 P.  v3.2 검산 재실행 — 원장 2판(bronze/phub-ledger-v2/)으로 LEDGER 를 바꿔 돌린다(동결 v3.2 산출물·2판 그대로 → 52/52).
 A.  잎 키 행선지: 1,072 행 · 미정 0 · 범주 5 · 이동 0(= v3.2 와 실제로 다른 행) · 표적이 ERD 에 있다(R36 포함) · 타임라인 9 · 미래 칸 3 은 행이 아니다.
 B.  사전: ERD 값·동의어·순서 = v3.2 (바뀐 자리 2: 혈관 폐색 → 폐색 · site +3 — 그것만) · 파생 항목 locator·unreviewed · closed · parent · category 키 0 · provenance 전수 · 출처 없는 값 목록 = 실측 · 폐색 항목 · 부위 3 · 승인 씨앗 21 은 사전에 없음.
 C.  출처 키.  D. 바이트: 3판 HASHES.txt 21 일치 · CHANGELOG 3판 행 · 2판과 다른 파일은 synergy·taxonomy 만.
 R.  재현: erd-v3.3-tuples.py 를 다시 돌려 요약이 erd-v3.3-tuples.json 과 같다 · bronze_version 3.
 O.  v3.2 변경(V3.2-0~9) 항목을 v3.3 산출물(3판)에 다시 — 안 붙은 문구 0 · raw_name 0 · 노드 locator · 원천 · 참조 · 추정 0 · ⑦ 점수 없음 · 참고 실행 값 사전 밖 · 자기 테이블 · 토큰화 locator · 버림 0 · 변형 쌍 승인 · 병기 locator · 씨앗 · 부위 닫힌 목록 · 적용 0 · 장비 · 항목 자신 · 줄임말 · 성분 what · 메모 · 설명문 · 상속 basis · family 참조 · 타임라인 · R15 속성 · 구조 · 결정 레코드.
 S.  검토 S-1~S-4 유지.  U. 사용자 정의 1·2·3 · 명시 예외 · 원칙 A~D 글자 그대로(v3.2 와 같다).
 V3.3-A~G: VA1~5 · VB1~3 · VC1~6 · VD1~4 · VE1~3 · VF1~2 · VG1~5 · UD1(사용자 결정 필요 표는 비어 있다).
실행: python3 erd-v3.3-check.py
"""
import importlib.util
import json
import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
STEP1 = "step1-products.json"
DESTS = {"개체", "사전", "엣지", "브론즈", "버림"}
LEDGER_V2 = os.path.join(HERE, "bronze", "phub-ledger-v2")
LEDGER = os.path.join(HERE, "bronze", "phub-ledger")


def load_module(name, path, patch=None):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if patch:
        patch(m)
    return m


def _patch_v2(m):
    """v3.2 이하 검산·실측 모듈의 LEDGER 를 2판으로(동결 산출물은 2판 실측이다)."""
    if hasattr(m, "LEDGER"):
        m.LEDGER = LEDGER_V2
    for a in ("V31", "V3", "V24", "V23", "V22", "V2", "V11"):
        sub = getattr(m, a, None)
        if sub is not None and hasattr(sub, "LEDGER"):
            sub.LEDGER = LEDGER_V2
    if hasattr(m, "load_module"):
        m.load_module = lambda n, p: load_module(n, p, _patch_v2)


def J(name):
    return json.load(open(os.path.join(HERE, name), encoding="utf-8"))


def parse_cmap(text):
    rows, cur = [], None
    for line in text.splitlines():
        m = re.match(r"^## `([^`]+\.json)`", line)
        if m:
            cur = m.group(1)
            continue
        if line.startswith("## ") and not m:
            cur = None
        if cur and line.startswith("| ") and not line.startswith("| #") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
            if len(cells) >= 7 and cells[0].isdigit():
                rows.append({"file": cur, "path": cells[1].strip("`"), "dest": cells[4], "target": cells[5].strip("`"), "note": cells[6]})
    return rows


def _count_key(x, key):
    n = 0
    if isinstance(x, dict):
        n += 1 if key in x else 0
        for v in x.values():
            n += _count_key(v, key)
    elif isinstance(x, list):
        for v in x:
            n += _count_key(v, key)
    return n


def run_checks():
    out, ok_all = [], True

    def line(ok, text):
        nonlocal ok_all
        ok_all = ok_all and bool(ok)
        out.append(f"- {'PASS' if ok else 'FAIL'} — {text}")

    erd, dic, tup = J("erd-v3.3.json"), J("erd-v3.3-dictionaries.json"), J("erd-v3.3-tuples.json")
    e32, d32, t32 = J("erd-v3.2.json"), J("erd-v3.2-dictionaries.json"), J("erd-v3.2-tuples.json")
    seeds32 = J("erd-v3.2-seed-candidates.json")
    scan = J("bronze-ledger-column-scan.json")
    T = load_module("t33chk", os.path.join(HERE, "erd-v3.3-tuples.py"))
    S = T.S33
    X = tup["v33"]
    s = tup["adverse"]["summary"]
    ad = tup["adverse"]
    D = {d["name"]: d for d in dic["dictionaries"]}
    D32 = {d["name"]: d for d in d32["dictionaries"]}
    ents = {e["key"] for e in erd["entities"]}
    rels = {r["id"] for r in erd["relations"]}

    # ---- P
    out.append("### P. v3.2 검산 재실행(원장 2판)")
    try:
        c32 = load_module("chk32", os.path.join(HERE, "erd-v3.2-check.py"), _patch_v2)
        ok32, rep32 = c32.run_checks()
        n_pass, n_fail = rep32.count("- PASS"), rep32.count("- FAIL")
        line(ok32 and n_fail == 0, f"[P1] erd-v3.2-check.py 재실행(LEDGER → bronze/phub-ledger-v2) PASS {n_pass} · FAIL {n_fail}(동결 v3.2 산출물 · 브론즈 2판 그대로)")
    except Exception as ex:  # noqa
        line(False, f"[P1] erd-v3.2-check.py 실행 실패: {ex!r}")

    # ---- A
    out.append("### A. 잎 키 행선지")
    cm_text = open(os.path.join(HERE, "erd-v3.3-column-map.md"), encoding="utf-8").read()
    cm = parse_cmap(cm_text)
    cm32 = parse_cmap(open(os.path.join(HERE, "erd-v3.2-column-map.md"), encoding="utf-8").read())
    keys = {(r["file"], r["path"]) for r in cm}
    leaf = {(f, p) for f, v in scan["files"].items() for p in v["leaf_paths"]}
    line(len(cm) == 1072 and len(keys) == len(cm), f"[A1] 행 {len(cm)} = 1,072 · 중복 {len(cm) - len(keys)}")
    line(leaf <= keys, f"[A2] 원장 잎 키 {len(leaf)} 전부 행선지 있음(빠짐 {len(leaf - keys)})")
    line(all(r["dest"] in DESTS for r in cm) and not any(r["dest"] == "미정" for r in cm), "[A3] 범주 5 안 · 미정 0")
    b32 = {(r["file"], r["path"]): f"{r['dest']}:{r['target']}" for r in cm32}
    diff = {(r["file"], r["path"]) for r in cm if b32.get((r["file"], r["path"])) != f"{r['dest']}:{r['target']}"}
    mv = {(m["file"], m["path"]) for m in erd["column_map_moves_v3_3"]}
    line(diff == mv and len(mv) == 0, f"[A4] 이동 표 {len(mv)} = v3.2 와 실제로 다른 행 {len(diff)}(v3.3 은 이동 0)")
    dnames = {d["name"] for d in dic["dictionaries"]}
    bad = []
    for r in cm:
        if r["dest"] == "개체" and r["target"].split(".")[0].split("(")[0] not in ents:
            bad.append(r["target"])
        if r["dest"] == "엣지" and r["target"].split(".")[0].split("(")[0] not in rels:
            bad.append(r["target"])
        if r["dest"] == "사전" and r["target"].replace("dict:", "") not in dnames:
            bad.append(r["target"])
    line(not bad, f"[A5] 표적이 ERD 에 정의됨(어긋남 {len(bad)}: {bad[:5]})")
    tl = [r for r in cm if r["file"] == "post-procedure-timeline.json" and r["path"].startswith("timelines[]")]
    line(all(r["target"].startswith("post_procedure_timeline") or r["target"].startswith("R33") for r in tl) and len(tl) == 9, f"[A6] 타임라인 행 {len(tl)} 전부 post_procedure_timeline · R33")
    fut = re.findall(r"^\| \d+ \| `products\.\*\.products\[\]\.components\[\]\.[a-z]+` \|", cm_text, re.M)
    line(len(fut) == len(S.FUTURE_COLUMNS_V33) == 3 and len(erd["future_columns_v3_3"]) == 3 and not any("components[]" in r["path"] for r in cm), f"[A7] V3.3-A 미래 칸 {len(fut)} 은 별도 절(1,072 행 밖) · json future_columns_v3_3 {len(erd['future_columns_v3_3'])}")

    # ---- B
    out.append("### B. 사전")
    same = []
    for n, d in D32.items():
        if n == "phrase_dictionary":
            continue
        a = [(e["canonical"], [sv["value"] for sv in e.get("synonyms", [])]) for e in d["entries"] if e.get("origin") not in ("ledger", "taxonomy")]
        b = [(e["canonical"], [sv["value"] for sv in e.get("synonyms", [])]) for e in D[n]["entries"] if e.get("origin") not in ("ledger", "taxonomy")]
        if n == "adverse_event_type":
            a = [(("폐색" if c == "혈관 폐색" else c), [x for x in ss if x != "혈관 폐색"]) for c, ss in a]
        if n == "site":
            b = b[:len(a)]
        if a != b:
            same.append(n)
    line(not same and set(D32) == set(D), f"[B1] 사전 {len(D)} = v3.2 이름 · ERD 값·동의어·순서 불변 — 허용된 변경 2(혈관 폐색 → 폐색 · site +3)만(어긋난 사전 {same})")
    der = [(n, e) for n, d in D.items() for e in d["entries"] if e.get("origin") in ("ledger", "taxonomy")]
    line(all(e.get("status") == "unreviewed" and (e.get("locators") or [sv.get("locator") for sv in e.get("sources", [])]) for n, e in der) and {n for n, e in der} <= {"adverse_event_type", "product_name"},
         f"[B2] 파생 항목 {len(der)}(사건 {sum(1 for n, e in der if n == 'adverse_event_type')} · 장비 제품 {sum(1 for n, e in der if n == 'product_name')}) 전부 unreviewed · locator 있음 · 열린 사전에만")
    cl = {n: D[n].get("closed") for n in ("site", "relative_site", "course", "adverse_qualifier", "adverse_event_type", "ingredient_material", "product_name")}
    line(cl == {"site": True, "relative_site": True, "course": True, "adverse_qualifier": True, "adverse_event_type": False, "ingredient_material": False, "product_name": False}, f"[B3] 닫힌 목록 표시 {cl}")
    sites = {e["canonical"]: e for e in D["site"]["entries"]}
    line(all("parent" in e for e in D["site"]["entries"]) and sites.get("동맥", {}).get("parent") == "혈관" and sites.get("정맥", {}).get("parent") == "혈관" and sites.get("안동맥", {}).get("parent") == "동맥", "[B4] site 항목 parent 필드 전부 · 동맥→혈관 · 정맥→혈관 · 안동맥→동맥")
    n_cat = sum(_count_key(d["entries"], "category") + _count_key(d["entries"], "category_review") for d in dic["dictionaries"])
    line(n_cat == 0, f"[B5] V3.3-E 사전 항목의 category·category_review 키 {n_cat}(v3.2 {X['category']['v32'].get('erd-v3.2-dictionaries.json:category')} + {X['category']['v32'].get('erd-v3.2-dictionaries.json:category_review')})")
    erd_entries = [e for d in dic["dictionaries"] if d["name"] != "phrase_dictionary" for e in d["entries"] if e.get("origin") not in ("ledger", "taxonomy")]
    no_prov = [e["canonical"] for e in erd_entries if not e.get("provenance") or not e["provenance"].get("status")]
    uns = X["provenance"]["unsourced"]
    uns_ids = {u["id"] for u in uns}
    uns_dict = {e["id"] for e in erd_entries if e.get("provenance", {}).get("status") in ("missing", "erd_default")}
    line(not no_prov and uns_ids == uns_dict and all(e["provenance"].get("locators") for e in erd_entries if e["id"] not in uns_ids),
         f"[B6] ERD 사전 값 {len(erd_entries)} 전부 provenance(상태 {dict(Counter(e['provenance']['status'] for e in erd_entries))}) · 출처 없는 값 {len(uns)} = 실측 목록(§13) · 나머지 locator ≥1")
    pe = next((e for e in D["adverse_event_type"]["entries"] if e["canonical"] == "폐색"), None)
    surf33 = T.T32.all_surfaces(T.base_dictionary33(dic))
    line(pe is not None and pe["id"] == T.mkid("DIC", "adverse_event_type|폐색") and "DIC-34071e9965" in pe.get("aliases", []) and {sv["value"] for sv in pe["synonyms"]} == {"Vascular Occlusion"} and T.norm("혈관 폐색") not in surf33 and pe.get("decomposed_from", {}).get("site") == "혈관" and not any(e["canonical"] == "혈관 폐색" for e in D["adverse_event_type"]["entries"]),
         f"[B7] V3.3-C 「혈관 폐색」→「폐색」(id 재계산 · 옛 id alias · Vascular Occlusion 동의어 · 분해 꼴 site 혈관 · 옛 글자는 사전 표면형 아님)")
    s3 = [sites.get(v) for v, k, p, b_ in S.SITE_ADDED_V33]
    line(all(e and e["kind"] == "layer" and e.get("added_in") and e["id"] == T.mkid("DIC", f"site|{e['canonical']}") and e["sources"] and e["provenance"]["locators"] for e in s3), f"[B8] V3.3-C 부위 3(동맥 · 정맥 · 안동맥) kind layer · id · sources(실측) · provenance locator")
    appr = [v for v, *_ in S.SEED_APPROVED_V33["site"]] + [v for v, *_ in S.SEED_APPROVED_V33["ingredient_material"]]
    in_dict = [v for v in appr if T.norm(v) in surf33]
    line(not in_dict and len(appr) == 21, f"[B9] V3.3-C 승인 씨앗 21 은 ERD 사전 값이 아니다(결정 레코드 · 8차)(사전에 있는 것 {in_dict})")

    # ---- C
    out.append("### C. 출처 키")
    s1 = set(load_module("bscan", os.path.join(HERE, "bronze-ledger-column-scan.py")).FileScan(os.path.join(HERE, STEP1)).run()["leaf_paths"])
    allk = {f"{f}:{p}" for f, p in leaf} | {f"{STEP1}:{p}" for p in s1}

    def has_key(k):
        if k in allk or k.startswith("*:"):
            return True
        if "*" in k:
            rx = re.compile("^" + re.escape(k).replace(r"\*", r"[^.:]+") + "$")
            return any(rx.match(x) for x in allk)
        return False
    miss = [sv for e in erd["entities"] for a in e["attrs"] for sv in a["sources"] if not has_key(sv)] + [sv for r in erd["relations"] for sv in r["sources"] if not has_key(sv)]
    line(not miss, f"[C1] 개체 속성·관계 출처 키 전부 잎 키(없는 것 {len(miss)}: {miss[:4]})")

    # ---- D
    out.append("### D. 바이트 · 3판")
    bc = T.bronze_check(LEDGER)
    line(bc["hashes_file"] and not bc["mismatch"], f"[D1] 브론즈 3판 HASHES.txt 21 일치(불일치 {bc['mismatch']})")
    cl3 = open(os.path.join(LEDGER, "CHANGELOG.md"), encoding="utf-8").read()
    line(any(ln.startswith("| 3 |") for ln in cl3.splitlines()) and erd["bronze"]["version"] == 3 and tup["bronze_version"] == 3, "[D2] CHANGELOG 3판 행 · erd.bronze.version 3 · 실측 bronze_version 3")
    hd = {x["file"] for x in X["bronze"]["hashes_changed_from_v2"]}
    line(os.path.isdir(LEDGER_V2) and hd == {"synergy.json", "taxonomy.json"}, f"[D3] 2판 보존 · 3판에서 바이트가 다른 파일 = {sorted(hd)}(synergy · taxonomy 만)")

    # ---- R
    out.append("### R. 재현")
    dic_, dic32, rules, rrules, L, L2, v31, v32, changes, step1 = T.load_all33()
    R = T.run_everything33(dic_, rules, L, rrules, v31, v32, dic32=dic32, L2=L2, changes=changes, step1=step1)
    for ax in ("procedure", "adverse", "condition"):
        a = json.loads(json.dumps(R[ax]["summary"], ensure_ascii=False, default=str))
        line(a == tup[ax]["summary"], f"[R-{ax}] {ax} 요약 재실행 = erd-v3.3-tuples.json")
    rep = json.loads(json.dumps({k: R["v33"][k] for k in ("component", "suffix", "category", "f_bundle", "deltas")}, ensure_ascii=False, default=str))
    rep["component"].pop("rows", None)
    cmp_ = {k: X[k] for k in ("component", "suffix", "category", "f_bundle", "deltas")}
    cmp_["component"] = {k: v for k, v in cmp_["component"].items() if k != "rows"}
    line(rep == json.loads(json.dumps(cmp_, ensure_ascii=False, default=str)) and R["procedure"]["summary"]["bronze_version"] == 3, "[R4] v3.3 실측(component · suffix · category · f_bundle · deltas) 재실행 = json · bronze_version 3")

    # ---- O (v3.2 변경 항목을 v3.3 산출물에 다시)
    out.append("### O. v3.2 변경(V3.2-0~9) 유지 — v3.3 산출물(3판)")
    line(s["adverse_unattached"] == 0, f"[O1] 부작용 문구 중 어느 노드에도 안 붙은 것 {s['adverse_unattached']}(exact {s['safety_by_status'].get('exact')} · new {s['safety_by_status'].get('new')})")
    line(s["complications_raw_name"] == 0 and "unlinked" not in s["safety_by_status"], f"[O2] raw_name 단위 {s['complications_raw_name']} · unlinked 상태 없음")
    line(s["ledger_events_without_locator"] == 0 and s["ledger_events_without_description"] == 0 and all(n["contexts"] and n["locators"] for n in ad["ledger_events"]), f"[O3] 새 사건 노드 {s['ledger_events']} 전부 locator·설명(원장 문맥) 있음")
    origins = Counter(o for t in ad["tuples"] for o in t["origins"])
    line(set(origins) <= {"complications", "safety_phrase"}, f"[O4] 단위를 세운 원천은 부작용 문구 종류뿐 — {dict(origins)}")
    units = {t["id"] for t in ad["tuples"]}
    refs = [u for T_ in ad["timelines"] for P in T_["phases"] for ln in P["lines"] for u in ln["adverse_ref"]] + [u for x in ad["emergency_signs"] + ad["disclosures"] + ad["literature"] for u in x["adverse_ref"]]
    line(set(refs) <= units, f"[O5] 다른 테이블 참조 {len(refs)} 전부 이미 있는 단위(세운 단위 0)")
    base_ev = {T.norm(e["canonical"]) for e in D["adverse_event_type"]["entries"] if e.get("origin") != "ledger"} | {T.norm(sv["value"]) for e in D["adverse_event_type"]["entries"] if e.get("origin") != "ledger" for sv in e.get("synonyms", [])}
    led = {T.norm(n["canonical"]) for n in ad["ledger_events"]}
    bad_ev = [t["event"] for t in ad["tuples"] if T.norm(t["event"]) not in base_ev | led]
    line(not bad_ev, f"[O6] 추정 매칭 0 — 단위 사건 전부 ERD 사전 값 또는 원장 사건 노드(그 밖 {len(bad_ev)})")
    line(all(d["rules"] and "score" not in d for d in ad["duplicate_pairs"]), f"[O7] ⑦ 후보 {len(ad['duplicate_pairs'])} 전부 표기 규칙 근거 · 점수 없음 · 접힘 적용 0")
    line(not any(sv.get("link") == "projection" for d in dic["dictionaries"] for e in d["entries"] for sv in e.get("synonyms", [])) and not any(e.get("link") == "projection" for d in dic["dictionaries"] for e in d["entries"]), "[O8] 참고 실행(승인 씨앗 21 적용 가정) 값이 사전 파일에 들어간 것 0")
    line(len(ad["emergency_signs"]) > 0 and len(ad["disclosures"]) == 109 and len(ad["literature"]) == 32, f"[O9] emergency_sign {len(ad['emergency_signs'])} · 고지 {len(ad['disclosures'])} · 문헌 {len(ad['literature'])} 자기 테이블")
    tw = tup["v32"]["tokenizer_words"]
    line(all(w["locators"] for w in tw) and len(tw) == 82, f"[O10] 분석기 보조 목록 {len(tw)} 원소마다 locator ≥1(없는 것 {[w['word'] for w in tw if not w['locators']]})")
    T.CUR.update(flags=dict(T.T32.FLAGS_V32))
    AT = T.T32.AdverseUnits32(T.V3.Ids3(T.base_dictionary33(dic_), L, rrules), rules["adverse"])
    lost = []
    for kind, f, p, loc, text in [(x[1], x[2], x[3], x[4], x[5]) for x in T.T32.ledger_texts(L) if x[0] == "adverse"]:
        gs = AT.split(text, None)
        cov = set()
        for g in gs:
            for m in g["members"]:
                for sp in m["spans"]:
                    cov |= {T.norm(w) for w in sp["text"].split()}
                for k in ("untouched", "gloss", "explanation", "side", "predicate"):
                    cov |= {T.norm(x if isinstance(x, str) else x["text"]) for x in m.get(k, [])}
                cov |= {T.norm(x["text"]) for x in m.get("modifiers", [])}
                cov |= {T.norm(x["of"]) for x in m.get("grammar", [])}
                cov |= {T.norm(x["text"]) for x in m.get("grammar", [])}
        for t in T.raw_tokens(text):
            nt = T.norm(t)
            if nt in ("및", "또는", "--"):
                continue
            if nt not in cov and not any(nt in c for c in cov):
                lost.append((loc, t))
    line(not lost, f"[O11] 제거 토큰 보존(버림 0) — 부작용 축 원장 문구 전수 재분해 · 어디에도 없는 토큰 {len(lost)} {lost[:4]}")
    vp = tup["v32"]["variant_pairs"]
    line(all(p_["status"] == "proposed" and p_["applied"] is False for p_ in vp), f"[O12] 변형 쌍 {len(vp)} 전부 목록 승인(proposed · applied=false · 자동 매칭 0)")
    line(all(x["locator"] for x in ad["gloss_pairs"]), f"[O13] 병기 쌍 {len(ad['gloss_pairs'])} 전부 locator")
    seeds = tup["v32"]["seeds"]
    rows = [(k, r) for k, v in seeds.items() for r in v["rows"] if r.get("status") == "proposed"]
    line(all(r.get("locators") and (r.get("n", 0) >= 2 or len(r["locators"]) >= 2) for k, r in rows if k not in ("site", "product_abbrev")) and all(r.get("locators") for k, r in rows if k == "product_abbrev") and all((r.get("locators") or any(x["locators"] for x in r.get("synonyms", []))) for k, r in rows if k == "site"),
         f"[O14] 씨앗 후보(proposed) {len(rows)} 전부 locator · 빈도 ≥2 또는 locator ≥2")
    site_vals = {r["value"] for r in seeds["site"]["rows"]}
    need = ["이마", "미간", "눈가", "눈밑", "눈꺼풀", "코", "코끝", "팔자주름", "볼", "광대", "턱", "턱선", "사각턱", "입술", "목", "목주름", "복부", "옆구리", "팔뚝", "허벅지", "종아리", "힙", "등", "가슴", "겨드랑이", "손", "발", "두피", "얼굴 전체", "바디 전체", "피부", "피하 지방층", "근육", "혈관", "점막", "주사 부위", "시술 부위", "동맥", "정맥", "안동맥"]
    line(set(need) <= site_vals and all(r["kind"] in ("anatomical", "region", "layer", "relative") and (r["parent"] is None or r["parent"] in site_vals) for r in seeds["site"]["rows"]), f"[O15] 부위 닫힌 목록 {len(site_vals)}(v3.2 42 + 동맥·정맥·안동맥) · kind 4 · parent 는 목록 안")
    line([e["canonical"] for e in D["site"]["entries"]][:len(D32["site"]["entries"])] == [e["canonical"] for e in D32["site"]["entries"]] and [e["canonical"] for e in D["site"]["entries"]][len(D32["site"]["entries"]):] == ["동맥", "정맥", "안동맥"] and [e["canonical"] for e in D["ingredient_material"]["entries"]] == [e["canonical"] for e in D32["ingredient_material"]["entries"]],
         "[O16] 씨앗 적용 0 — site = v3.2 26 + 사용자 승인 3(동맥·정맥·안동맥) · ingredient_material = v3.2 10(승인 6 은 8차)")
    eqp = tup["equipment"]["products"]
    line(all(p_["origin"] == "taxonomy" and p_["license_status"] == "미확인" and p_["status"] == "unreviewed" for p_ in eqp), f"[O17] 장비 제품 {len(eqp)} 전부 origin=taxonomy · license_status=미확인 · unreviewed")
    b, a = tup["v32"]["before"], tup["v32"]["after"]
    line(a["catalog_self"] <= b["catalog_self"] and a["catalog_by_what_kind"].get("product", 0) >= b["catalog_by_what_kind"].get("product", 0), f"[O18] 항목 자신 {b['catalog_self']}(v3.2) → {a['catalog_self']} · product {b['catalog_by_what_kind'].get('product')} → {a['catalog_by_what_kind'].get('product')}")
    ab = seeds["product_abbrev"]["rows"]
    line(all(r["status"] in ("proposed", "⑦") for r in ab), f"[O19] 줄임말 후보 {len(ab)} 전부 승인 묶음(자동 아님)")
    ingv = {T.norm(e["canonical"]) for e in D["ingredient_material"]["entries"]}
    iw = [r for r in tup["procedure"]["catalog"] if r.get("what_kind") == "ingredient"]
    PT = {t["id"]: t for t in tup["procedure"]["tuples"]}
    line(all(T.norm(PT[r["procedure_id"]]["what_label"]) in ingv for r in iw) and "ingredient" in erd["enums"]["procedure.what_kind"], f"[O20] 성분 what {len(iw)} 전부 성분 사전 값 · what_kind 열거형")
    notes = [m for m in ad["memo_phrases"] if m["status"] == "note"]
    line(all(not m["events_seen"] for m in notes), f"[O21] not_adverse_note {len(notes)} 전부 사건 조각 0")
    line(all(m["why"] for m in ad["memo_phrases"] if m["status"] == "sentence") and set(e["status"] for e in ad["phrase_dictionary"]) <= {"exact", "new"}, "[O22] 설명문 판정 근거 있음 · 문구 사전 status ∈ exact|new(+메모 note|sentence)")
    line(s["inheritance_missing_basis"] == 0 and s["inheritance_copied_values"] == 0, f"[O23] basis 없는 상속 {s['inheritance_missing_basis']} · 복사된 값 {s['inheritance_copied_values']}")
    fam_keys = {f"R15:{e['from'][1]}→{e['unit']}" for e in ad["edges"] if e["from"][0] == "modality"}
    badref = [x for e in ad["edges"] for x in e["inheritance"] if x["basis"] == "family" and str(x["ref"]).startswith("R15:") and x["ref"] not in fam_keys and e["from"][0] != "modality"]
    line(not badref, f"[O24] family 참조 전부 실제 계열 엣지(어긋남 {len(badref)})")
    line(s["timelines"] == 10 and s["timeline_lines"] == 435 and s["timeline_phases"] == 43, f"[O25] 타임라인 {s['timelines']} · 단계 {s['timeline_phases']} · 줄 {s['timeline_lines']}")
    r15 = next(r for r in erd["relations"] if r["id"] == "R15")
    line(not {"period", "phase_label", "reaction_level"} & {x["name"] for x in r15["attrs"]} and {"timeline_refs", "inheritance"} <= {x["name"] for x in r15["attrs"]}, "[O26] R15 period/phase_label/reaction_level → timeline_refs 참조 · inheritance 속성")
    line(len(erd["entities"]) == 22 and len(erd["relations"]) == 35 and len(erd["decision_kinds"]) == 20 and {"R33", "R34", "R35", "R36"} <= rels and {"post_procedure_timeline", "emergency_sign"} <= ents, "[O27] 구조: 개체 22 · 관계 35(34 + R36) · 결정 kind 20(새 kind 0)")
    line(len(erd["decisions"]) == len(e32["decisions"]) + 1 and erd["decisions"][:len(e32["decisions"])] == e32["decisions"] and erd["decisions"][-1]["status"] == "proposed", f"[O28] 결정 레코드 v3.2 {len(e32['decisions'])} 이관 그대로 + DEC-29(proposed) · 승인 씨앗·접미사 쌍·R30 은 레코드 0")

    # ---- S
    out.append("### S. 검토 반영 유지(erd-v3.2-review.md S-1~S-4)")
    absorbed = [n["canonical"] for n in ad["ledger_events"] if any(T.norm(w) in base_ev for w in n["canonical"].split()) and T.norm(n["canonical"]) not in base_ev]
    line(not absorbed, f"[S1] 사전 사건을 낱말로 품은 원장 노드 0 — 있음 {absorbed[:5]}")
    hz = next((e for e in ad["phrase_dictionary"] if "시술 후 일시적인 홍조와 부종" in e["raw_variants"]), None)
    line(hz is not None and {c["event"] for c in hz["candidates"]} >= {"부종", "홍조"}, "[S1b] 실례 「시술 후 일시적인 홍조와 부종」→ 부종 exact + 홍조 new")
    line(all(d["existing_kind"] in ("dictionary", "ledger") and d["grade"] in ("strong", "weak") for d in ad["duplicate_pairs"]), f"[S2] ⑦ 는 노드끼리 · strong {s['dup_pairs_strong']} / weak {s['dup_pairs_weak']}")
    BAN = ("raw_name", "unlinked", "adverse_expression", "RAW:", "R29")
    ae = next(e for e in erd["entities"] if e["key"] == "adverse_effect")
    fields = json.dumps({"attrs": ae["attrs"], "identity": ae["identity"], "R15": r15, "enums": {k: v for k, v in erd["enums"].items() if k.startswith("adverse")}, "id_rule": erd["id_rule"]["adverse_effect"], "ata": next(k for k in erd["decision_kinds"] if k["kind"] == "adverse_tuple_assign")}, ensure_ascii=False)
    hits = {b_ for b_ in BAN if b_ in fields}
    line(not hits and not any(k.startswith("adverse_expression.") for k in erd["enums"]) and "table_line.ref_status" in erd["enums"], f"[S3] 정의 표에 옛 잔재 0(남은 {hits}) · table_line.ref_status")
    tw_ = {(w["kind"], w["word"]) for w in tw}
    line({("predicate", "는"), ("relaxed", "시"), ("relaxed", "이")} <= tw_, "[S4] 토큰화 보강 목록(관형형·relaxed) 보존 — 역할은 분석기 보조")

    # ---- U
    out.append("### U. 사용자 정의")
    line(erd["user_definitions"] == e32["user_definitions"] and erd["user_definitions_v31"] == e32["user_definitions_v31"] and erd["explicit_exception_v31"] == e32["explicit_exception_v31"], "[U1] 정의 1·2(v3.1 개정판)·3 · 명시 예외 글자 그대로(v3.2 와 같다)")
    line(erd["principles"] == e32["principles"] and erd["rule_zero"] == e32["rule_zero"] and erd["node_rule"] == e32["node_rule"], "[U2] 원칙 A~D · §0 첫 규칙 · 노드 원칙 글자 그대로(v3.2 와 같다 · v3.3 은 소개정)")

    # ---- V3.3-A
    out.append("### V3.3-A 제품 구성품(구조만 · 값 0)")
    pr = next(e for e in erd["entities"] if e["key"] == "product")
    pa = {a["name"]: a for a in pr["attrs"]}
    line({"kind", "component_of", "component_kind"} <= set(pa) and pa["kind"]["type"] == "enum(product|component)" and erd["enums"].get("product.kind") == ["product", "component"], "[VA1] product.kind enum(product|component) · component_of · component_kind 속성 · 열거형")
    r36 = next((r for r in erd["relations"] if r["id"] == "R36"), None)
    line(r36 is not None and r36["name"] == "component_of" and r36["from"] == "product(kind=component)" and r36["to"] == "product" and r36["card"] == "N:1" and not r36["sources"], "[VA2] R36 component_of: product(kind=component) → product (N:1) · 출처 (ERD 정의 · 원장 칸 없음)")
    r27 = next(r for r in erd["relations"] if r["id"] == "R27")
    line("component" in erd["enums"]["procedure.what_kind"] and "product(kind=component)" in r27["to"], "[VA3] what_kind 열거형에 component · R27 끝에 product(kind=component)(성분 what 과 대칭)")
    c = X["component"]
    line(c["label_slot_hits"] == [] and X["f_bundle"]["component_what"] == 0 and not any(r.get("what_kind") == "component" for r in tup["procedure"]["catalog"]) and c["occurrences"] > 0,
         f"[VA4] 값 0 — 구성품 말이 든 원장 자리 {c['occurrences']}(주의·설명 문장) 중 시술 라벨 자리 {len(c['label_slot_hits'])} · what_kind=component 0 · R36 엣지 0 · 「포텐자 팁」 {c['phrase_포텐자_팁']}")
    line(len(erd["future_columns_v3_3"]) == 3 and all("components[]" in x["column"] for x in erd["future_columns_v3_3"]) and erd["tuple_rules"]["component"]["values"] == 0, "[VA5] 미래 칸 3(원장 칸 없음) · tuple_rules.component.values 0")

    # ---- V3.3-B
    out.append("### V3.3-B 토큰화 = 형태소 분석기")
    tk = erd["resolve_rules"]["tokenize"]
    line("kiwipiepy" in tk["rule"] and "0.24" in tk["rule"] and "형태소" in tk["rule"] and tk["analyzer"]["version_pinned"] == "0.24" and "조사·어미 목록에서 뗀다" in tk["rule"] and tk["rule"].startswith("**토큰화(V3.3-B"), "[VB1] §1.3 규칙 문장 교체 — 형태소 분석기 kiwipiepy · 판 고정 0.24 · 핵심어 = 명사 + ㅁ/음 명사형 · 문장꼴 = 절 · 괄호·서술")
    line(tk.get("list_role") == "analyzer_assist" and erd["tuple_rules"]["phrase_kinds"].get("list_role") == "analyzer_assist" and len(tk["particles"]) == 27 and len(tk["verb_endings"]) == 18 and len(tk["grammar_words"]) == 21 and tk.get("assist_rule_v32"), "[VB2] v3.2 목록(조사 27 · 어미 18 · 문법 21 · relaxed · predicate · note_words …)은 분석기 보조 목록(analyzer_assist)으로 보존")
    k = X["kiwi"]
    line(k["available"] and k["pinned_ok"] is True and k["user_words"] > 0, f"[VB3] 설치 kiwipiepy {k['version']} = 고정 판 {k['pinned']}.x · 등록할 사전 표면형 {k['user_words']}")

    # ---- V3.3-C
    out.append("### V3.3-C 부작용 사전 · 부위")
    r2 = X["r2_dictionary"]
    eu = r2["event_units"][0] if r2["event_units"] else {}
    line(bool(eu.get("unit_event_site")) and not r2["old_surface_in_dictionary"] and eu.get("n_units", 0) >= 1 and any(t["event"] == "폐색" and t["site"] == "혈관" for t in ad["tuples"]), f"[VC1] R2 를 사전 값에도 — (폐색, 혈관) 단위 {eu.get('unit_event_site')} · 폐색 단위 {eu.get('n_units')} · 옛 글자 표면형 0")
    line(all(x["n_substring"] > 0 for x in r2["sites_added"]) and all(x["id"] == T.mkid("DIC", f"site|{x['value']}") for x in r2["sites_added"]) and any(t["event"] == "폐색" and t["site"] in ("동맥", "안동맥") for t in ad["tuples"]),
         f"[VC2] 부위 3 원장 locator(부분 문자열 {'/'.join(str(x['n_substring']) for x in r2['sites_added'])} · 토큰 {'/'.join(str(x['n_token']) for x in r2['sites_added'])}) · (폐색, 동맥)·(폐색, 안동맥) 단위 있음")
    oe = r2["occlusion_embolism"]
    line(not oe["shared_synonyms"] and not oe["dup_pairs_between"] and oe["same_unit"] is False, f"[VC3] 폐색 ≠ 색전 — 공유 동의어 0 · ⑦ 쌍 0 · 한 단위로 접힌 자리 0(둘 다 나온 문구 {len(oe['phrases_with_both'])})")
    rc = r2["r30_candidates"]
    line(len(rc) >= 2 and {(x["from"], x["to"]) for x in rc} == {("색전", "폐색"), ("폐색", "괴사")} and all(x["locator"] and x["status"].startswith("proposed") for x in rc) and r2["r30_edges"] == 0 and not any(d["kind"] == "edge_create" for d in erd["decisions"][len(e32["decisions"]):]),
         f"[VC4] R30 후보 {len(rc)}(색전→폐색 · 폐색→괴사) 전부 원장 locator · 제안(엣지 0 · edge_create 레코드 0)")
    sa = X["seeds_approved"]
    line(len(sa["site"]) == 15 and len(sa["ingredient_material"]) == 6 and all(x["status"] == "승인됨 · 8차 적용" and x["in_erd_dictionary"] is False and x["ledger_evidence"] for x in sa["site"] + sa["ingredient_material"]),
         f"[VC5] 승인 씨앗 부위 15 · 성분 6 — 「승인됨 · 8차 적용」 · 원장 근거(값 또는 동의어 locator) 전부 · 사전 값 아님")
    ud = {x["item"] for x in erd["user_decisions_needed"]}
    line(any("정맥염" in x for x in ud) and any("혈관외유출" in x for x in ud) and any(e["canonical"] == "정맥염" for e in D["adverse_event_type"]["entries"]) and any(e["canonical"] == "혈관외유출" for e in D["adverse_event_type"]["entries"]), "[VC6] 정맥염 · 혈관외유출 — 분해하지 않고 「사용자 결정 필요」(사전 값 그대로)")

    # ---- V3.3-D
    out.append("### V3.3-D 접미사 표기 꼴")
    pk = erd["tuple_rules"]["phrase_kinds"]
    sf = X["suffix"]
    line("표기 꼴" in pk.get("suffix_variant_rule", "") and pk.get("spelling_variant_suffixes") == ["감", "증", "형성"] and len(pk["suffix_pairs_v33"]) == 20 and all(r["canonical_in_user_list"] for r in sf["pairs"]), "[VD1] 규칙 문장 · 접미 3(감·증·형성) · 쌍 20 · 대표 이름 전부 사용자 목록(현상 이름) 안")
    line(len(pk["non_suffix_pairs_user"]) == 3 and sum(1 for x in ud if "압통감" in x and "저림감" in x and "가려움증" in x) == 1, "[VD2] 접미사 아닌 3쌍(압통감·저림감·가려움증)은 「사용자 결정 필요」")
    line(sf["pairs_already_same_dictionary_value"] == 0 and sf["dup_suffix_pairs_in_20"] == 20, f"[VD3] 20 쌍을 위해 사전에 더한 동의어 0 · 20 쌍 전부 이 실측에서도 ⑦ strong(fold_approve 자리)")
    dr = pk["dup_rules"]["strong"]
    line(any("suffix_감|증|형성" in x and "표기 꼴" in x for x in dr) and any("suffix_감각" in x and "⑦" in x for x in dr) and any("「감각」" in x for x in ud), "[VD4] ⑦ strong 규칙에서 감·증·형성(표기 꼴)과 감각(⑦ 후보 · 사용자 결정 없음) 분리")

    # ---- V3.3-E
    out.append("### V3.3-E category 삭제")
    n_json = sum(1 for kd in erd["decision_kinds"] if "category" in (kd.get("new_value") or ""))
    n_tup = _count_key(tup["adverse"]["tuples"], "event_category")
    n_enum = sum(1 for kk in erd["enums"] if "category" in kk and "subcategory" not in kk)
    line(n_cat == 0 and n_json == 0 and n_tup == 0 and n_enum == 0 and X["category"]["v33"]["tuples:event_category"] == 0, f"[VE1] category 키 0 — 사전 {n_cat} · 결정 kind new_value {n_json}(v3.2 2) · 실측 단위 event_category {n_tup}(v3.2 {X['category']['v32'].get('erd-v3.2-tuples.json:event_category')}) · 열거형 {n_enum}")
    ct = erd["category_touched_v3_3"]
    line(len(ct) >= 9 and X["category"]["v32"].get("erd-v3.2-dictionaries.json:category") == 302 and X["category"]["v32"].get("erd-v3.2-tuples.json:event_category") == 328, f"[VE2] 삭제가 미친 자리 전수 표 {len(ct)} 행 · v3.2 실측(사전 302 · review 40 · 단위 328 · kind 2)")
    lab = X["category"]["ledger_occurrences_of_7_labels"]["exact_value_occurrences"]
    line(all(lab[x] == 0 for x in ("국소 일시 반응", "염증/감염", "구조/이물", "전신", "신경")) and len(erd["tuple_rules"]["adverse"]["classification_from_ledger_only"]) == 3, f"[VE3] 7 라벨 중 복합 라벨 5 는 원장 잎 값 0회(색소·혈관은 낱말로만) · 분류는 원장 값 3(severity · frequency_class · course)")

    # ---- V3.3-F
    out.append("### V3.3-F 세분 묶음 설계안(적용 0)")
    fb = X["f_bundle"]
    line(len(fb["options"]) == 3 and fb["applied"] is None and all(re.search(r"\d", fb["impact"][o["option"].split()[0]]) for o in fb["options"]) and fb["depth_label_slots"] > 0, f"[VF1] 설계안 3(F-1 복합 키 · F-2 technique 속성 · F-3 별도 개체) · 영향 수치(실측 · 깊이 라벨 자리 {fb['depth_label_slots']} · 충돌 묶음 {fb['collision_groups']} · 실 재질/형태 {fb['thread_label_slots']}) · 적용 None")
    attr_names = {a["name"] for e in erd["entities"] for a in e["attrs"] if e["key"] in ("procedure", "technique")}
    line(not ({"depth", "intensity", "spec", "material", "shape"} & attr_names) and "procedure_spec" not in ents and not any(r["id"] == "R37" for r in erd["relations"]) and any("F-1" in x for x in ud), "[VF2] 어느 안도 적용 안 함 — procedure·technique 에 depth·intensity·spec·material·shape 속성 0 · procedure_spec 개체·R37 없음 · 「사용자 결정 필요」에 F 항목")

    # ---- V3.3-G
    out.append("### V3.3-G 원장 3판 · 결정 kind 검토")
    g = X["ledger3"]
    line(tup["procedure"]["summary"]["catalog_items"] == 523 and g["catalog_items_v2"] == 521 and tup["procedure"]["summary"]["bronze_version"] == 3, f"[VG1] 분류 항목 {g['catalog_items_v2']} → {tup['procedure']['summary']['catalog_items']} · bronze_version 3")
    line(g["synergy_changed_slots"] == 59 and g["synergy_changed_links"] == 51, f"[VG2] synergy 바뀐 자리 {g['synergy_changed_slots']}(CHANGELOG 59) · 링크 {g['synergy_changed_links']} · 남은 「Mxx-」 {g['synergy_prefixed_distinct_v3']}종 {g['synergy_prefixed_slots_v3']}자리(4판 후보 · 사용자 결정 필요)")
    line({x["name"] for x in g["new_taxonomy_items"]} == {"저출력레이저(LLLT)", "다이오드 레이저"} and all(x["subcategory"] == "M8-6" and x["catalog"] for x in g["new_taxonomy_items"]), f"[VG3] M8-6 신설 항목 2 = CHANGELOG · 분류 항목 튜플 있음")
    line("새 kind 는 만들지 않는다" in erd["g_kind_assessment"] and "조합 절차" in erd["g_kind_assessment"] and len(erd["decision_kinds"]) == 20 and "조합" in next(kd["note"] for kd in erd["decision_kinds"] if kd["kind"] == "canonical_rename"), "[VG4] 「이름 교체 + 부위 분리」 kind 검토 — 새 kind 0 · 조합 절차 문장 · canonical_rename 비고")
    line(g["synergy_slot_result_v3"].get("unresolved", 0) < g["synergy_slot_result_v2"].get("unresolved", 0) and len(g["synergy_prefixed_values"]) == g["synergy_prefixed_distinct_v3"], f"[VG5] synergy 자리 ⑨ {g['synergy_slot_result_v2'].get('unresolved')} → {g['synergy_slot_result_v3'].get('unresolved')}(정식 이름 효과 · 실측)")

    # ---- 사용자 결정 필요
    out.append("### UD. 사용자 결정 필요")
    line(len(erd["user_decisions_needed"]) >= 8 and all(x["decision"] == "" for x in erd["user_decisions_needed"]), f"[UD1] 「사용자 결정 필요」 {len(erd['user_decisions_needed'])} 행 전부 빈 자리(추측으로 메우지 않았다)")

    n_pass, n_fail = sum(1 for x in out if x.startswith("- PASS")), sum(1 for x in out if x.startswith("- FAIL"))
    head = f"**{'PASS' if ok_all else 'FAIL'} {n_pass}/{n_pass + n_fail}**"
    return ok_all, head + "\n\n" + "\n".join(out)


if __name__ == "__main__":
    ok, rep = run_checks()
    print(rep)
    raise SystemExit(0 if ok else 1)
