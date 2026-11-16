#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v3.2 검산.
 P. v3.1 검산 전부 재실행(erd-v3.1-check.py · 동결 산출물 · 브론즈 2판) — v3.2 개정이 이전 판·원장을 건드리지 않았다.
 A. 잎 키 행선지(v3.2): 1,072 행 · 미정 0 · 범주 5 · 이동 표 = v3.1 표와 실제로 다른 행 전부 · 새 표적 개체/관계가 ERD 에 있다.
 B. 사전: ERD 값·동의어·순서 = v3.1(파생 항목 제외) · 파생 항목 전부 locator·origin·status · closed 표시 · 변형 쌍/씨앗이 사전에 들어간 것 0.
 C. 출처 키: 개체 속성·관계 출처 'file:path' 가 잎 키에 있다.  D. 바이트: 원장 21 해시 = HASHES.txt.
 R. 재현: erd-v3.2-tuples.py 를 다시 돌려 요약이 erd-v3.2-tuples.json 과 같다 · 규칙을 끄면 erd-v3.1-tuples.json 요약과 같다(회귀).
 O. v3.2 변경: V3.2-0 ~ V3.2-9 각 항목 + 「제거 토큰 보존(버림 0)」·「변형 쌍은 목록 승인(자동 매칭 0)」·「씨앗 후보 전부 locator」·「not_adverse_note 에 사건 조각 0」·「부작용 문구 중 어느 노드에도 안 붙은 것 0」·「새 노드 전부 locator·설명」·「추정 매칭 0」·「basis 없는 상속 0 · 복사 0」.
 U. 사용자 정의 1·3 · 명시 예외 · 정의 2(v3.1 개정판) 유지 · 원칙 B·C 불변.
실행: python3 erd-v3.2-check.py
"""
import importlib.util
import json
import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
STEP1 = "step1-products.json"
DESTS = {"개체", "사전", "엣지", "브론즈", "버림"}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def J(name):
    return json.load(open(os.path.join(HERE, name), encoding="utf-8"))


def parse_cmap(text):
    rows, cur = [], None
    for line in text.splitlines():
        m = re.match(r"^## `([^`]+\.json)`", line)
        if m:
            cur = m.group(1)
            continue
        if cur and line.startswith("| ") and not line.startswith("| #") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
            if len(cells) >= 7 and cells[0].isdigit():
                rows.append({"file": cur, "path": cells[1].strip("`"), "dest": cells[4], "target": cells[5].strip("`"), "note": cells[6]})
    return rows


def run_checks():
    out, ok_all = [], True

    def line(ok, text):
        nonlocal ok_all
        ok_all = ok_all and bool(ok)
        out.append(f"- {'PASS' if ok else 'FAIL'} — {text}")

    erd, dic, tup = J("erd-v3.2.json"), J("erd-v3.2-dictionaries.json"), J("erd-v3.2-tuples.json")
    e31, d31, t31 = J("erd-v3.1.json"), J("erd-v3.1-dictionaries.json"), J("erd-v3.1-tuples.json")
    seeds = J("erd-v3.2-seed-candidates.json")
    scan = J("bronze-ledger-column-scan.json")
    T = load_module("t32chk", os.path.join(HERE, "erd-v3.2-tuples.py"))

    # ---- P
    out.append("### P. v3.1 검산 재실행")
    try:
        c31 = load_module("chk31", os.path.join(HERE, "erd-v3.1-check.py"))
        ok31, rep31 = c31.run_checks()
        n_pass = rep31.count("- PASS")
        n_fail = rep31.count("- FAIL")
        line(ok31 and n_fail == 0, f"erd-v3.1-check.py 재실행 PASS {n_pass} · FAIL {n_fail}(동결 v3.1 산출물 · 브론즈 2판 그대로)")
    except Exception as ex:  # noqa
        line(False, f"erd-v3.1-check.py 실행 실패: {ex!r}")

    # ---- A
    out.append("### A. 잎 키 행선지")
    cm = parse_cmap(open(os.path.join(HERE, "erd-v3.2-column-map.md"), encoding="utf-8").read())
    cm31 = parse_cmap(open(os.path.join(HERE, "erd-v3.1-column-map.md"), encoding="utf-8").read())
    keys = {(r["file"], r["path"]) for r in cm}
    leaf = {(f, p) for f, v in scan["files"].items() for p in v["leaf_paths"]}
    line(len(cm) == 1072 and len(keys) == len(cm), f"행 {len(cm)} = 1,072 · 중복 {len(cm) - len(keys)}")
    line(leaf <= keys, f"원장 잎 키 {len(leaf)} 전부 행선지 있음(빠짐 {len(leaf - keys)})")
    line(all(r["dest"] in DESTS for r in cm) and not any(r["dest"] == "미정" for r in cm), f"범주 5 안 · 미정 0")
    b31 = {(r["file"], r["path"]): f"{r['dest']}:{r['target']}" for r in cm31}
    diff = {(r["file"], r["path"]) for r in cm if b31.get((r["file"], r["path"])) != f"{r['dest']}:{r['target']}"}
    mv = {(m["file"], m["path"]) for m in erd["column_map_moves_v3_2"]}
    line(diff == mv, f"이동 표 {len(mv)} = v3.1 과 실제로 다른 행 {len(diff)}")
    ents = {e["key"] for e in erd["entities"]}
    rels = {r["id"] for r in erd["relations"]}
    dnames = {d["name"] for d in dic["dictionaries"]}
    bad = []
    for r in cm:
        if r["dest"] == "개체" and r["target"].split(".")[0].split("(")[0] not in ents:
            bad.append(r["target"])
        if r["dest"] == "엣지" and r["target"].split(".")[0].split("(")[0] not in rels:
            bad.append(r["target"])
        if r["dest"] == "사전" and r["target"].replace("dict:", "") not in dnames:
            bad.append(r["target"])
    line(not bad, f"표적이 ERD 에 정의됨(어긋남 {len(bad)}: {bad[:5]})")
    tl = [r for r in cm if r["file"] == "post-procedure-timeline.json" and r["path"].startswith("timelines[]")]
    line(all(r["target"].startswith("post_procedure_timeline") or r["target"].startswith("R33") for r in tl) and len(tl) == 9, f"타임라인 행 {len(tl)} 전부 post_procedure_timeline · R33(V3.2-9)")

    # ---- B
    out.append("### B. 사전")
    D = {d["name"]: d for d in dic["dictionaries"]}
    D31 = {d["name"]: d for d in d31["dictionaries"]}
    same = []
    for n, d in D31.items():
        if n == "phrase_dictionary":
            continue
        a = [(e["canonical"], [s["value"] for s in e.get("synonyms", [])]) for e in d["entries"]]
        b = [(e["canonical"], [s["value"] for s in e.get("synonyms", [])]) for e in D[n]["entries"] if e.get("origin") not in ("ledger", "taxonomy")]
        if a != b:
            same.append(n)
    line(not same and set(D31) == set(D), f"사전 {len(D)} = v3.1 이름 · ERD 값·동의어·순서 불변(어긋난 사전 {same})")
    der = [(n, e) for n, d in D.items() for e in d["entries"] if e.get("origin") in ("ledger", "taxonomy")]
    line(all(e.get("status") == "unreviewed" and (e.get("locators") or [s.get("locator") for s in e.get("sources", [])]) for n, e in der) and {n for n, e in der} <= {"adverse_event_type", "product_name"},
         f"파생 항목 {len(der)}(사건 {sum(1 for n, e in der if n == 'adverse_event_type')} · 장비 제품 {sum(1 for n, e in der if n == 'product_name')}) 전부 unreviewed · locator 있음 · 열린 사전(사건·제품)에만")
    cl = {n: D[n].get("closed") for n in ("site", "relative_site", "course", "adverse_qualifier", "adverse_event_type", "ingredient_material", "product_name")}
    line(cl == {"site": True, "relative_site": True, "course": True, "adverse_qualifier": True, "adverse_event_type": False, "ingredient_material": False, "product_name": False}, f"닫힌 목록 표시 {cl}")
    line(all("parent" in e for e in D["site"]["entries"]), "site 항목 parent 필드(V3.2-4)")

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
    miss = [s for e in erd["entities"] for a in e["attrs"] for s in a["sources"] if not has_key(s)] + [s for r in erd["relations"] for s in r["sources"] if not has_key(s)]
    line(not miss, f"개체 속성·관계 출처 키 전부 잎 키(없는 것 {len(miss)}: {miss[:4]})")

    # ---- D
    out.append("### D. 바이트")
    bc = T.bronze_check(T.LEDGER)
    line(bc["hashes_file"] and not bc["mismatch"], f"브론즈 2판 HASHES.txt 21 일치(불일치 {bc['mismatch']})")

    # ---- R
    out.append("### R. 재현 · 회귀")
    dj, rules, rrules, L, v31 = T.load_all32()
    R = T.run_everything(T.base_dictionary(dj), rules, L, rrules, v31)
    for ax in ("procedure", "adverse", "condition"):
        a = json.loads(json.dumps(R[ax]["summary"], ensure_ascii=False, default=str))
        line(a == tup[ax]["summary"], f"{ax} 요약 재실행 = erd-v3.2-tuples.json")
    rg = R["v32"]["regression_v31"]
    line(all(v["same"] for v in rg.values()), "규칙을 끄면(FLAGS_OFF) v3.1 실측과 같다 — " + " · ".join(f"{k} {v['keys']} 키 {v['same']}" for k, v in rg.items()))
    ad = R["adverse"]
    s = ad["summary"]

    # ---- O
    out.append("### O. v3.2 변경")
    # V3.2-0
    line(s["adverse_unattached"] == 0, f"V3.2-0 부작용 문구 중 어느 노드에도 안 붙은 것 {s['adverse_unattached']}(exact {s['safety_by_status'].get('exact')} · new {s['safety_by_status'].get('new')})")
    line(s["complications_raw_name"] == 0 and "unlinked" not in s["safety_by_status"], f"V3.2-0 raw_name 단위 {s['complications_raw_name']} · unlinked 상태 없음")
    line(s["ledger_events_without_locator"] == 0 and s["ledger_events_without_description"] == 0 and all(n["contexts"] and n["locators"] for n in ad["ledger_events"]), f"V3.2-0 새 사건 노드 {s['ledger_events']} 전부 locator·설명(원장 문맥) 있음")
    origins = Counter(o for t in ad["tuples"] for o in t["origins"])
    line(set(origins) <= {"complications", "safety_phrase"}, f"V3.2-0 단위를 세운 원천은 부작용 문구 종류뿐 — {dict(origins)}")
    units = {t["id"] for t in ad["tuples"]}
    refs = [u for T_ in ad["timelines"] for P in T_["phases"] for ln in P["lines"] for u in ln["adverse_ref"]] + [u for x in ad["emergency_signs"] + ad["disclosures"] + ad["literature"] for u in x["adverse_ref"]]
    line(set(refs) <= units, f"V3.2-0 다른 테이블 참조 {len(refs)} 전부 이미 있는 단위(세운 단위 0)")
    ev_ok = {norm_ for norm_ in []}
    base_ev = {T.norm(e["canonical"]) for e in D["adverse_event_type"]["entries"] if e.get("origin") != "ledger"} | {T.norm(sv["value"]) for e in D["adverse_event_type"]["entries"] if e.get("origin") != "ledger" for sv in e.get("synonyms", [])}
    led = {T.norm(n["canonical"]) for n in ad["ledger_events"]}
    bad_ev = [t["event"] for t in ad["tuples"] if T.norm(t["event"]) not in base_ev | led]
    line(not bad_ev, f"V3.2-0 추정 매칭 0 — 단위 사건 전부 ERD 사전 값 또는 원장 사건 노드(그 밖 {len(bad_ev)})")
    line(all(d["rules"] and "score" not in d for d in ad["duplicate_pairs"]), f"V3.2-0 ⑦ 후보 {len(ad['duplicate_pairs'])} 전부 표기 규칙 근거 · 점수 없음 · 접힘 적용 0(사전 동의어 추가 0)")
    line(not any(sv.get("link") == "projection" for d in dic["dictionaries"] for e in d["entries"] for sv in e.get("synonyms", [])), "참고 실행(씨앗 승인 가정) 값이 사전 파일에 들어간 것 0")
    line(len(ad["emergency_signs"]) > 0 and len(ad["disclosures"]) == 109 and len(ad["literature"]) == 32, f"V3.2-0 emergency_sign {len(ad['emergency_signs'])} · 고지 {len(ad['disclosures'])} · 문헌 {len(ad['literature'])} 자기 테이블")
    # V3.2-1
    tw = R["v32"]["tokenizer_words"]
    line(all(w["locators"] for w in tw), f"V3.2-1 토큰화 목록 {len(tw)} 원소마다 locator ≥1(없는 것 {[w['word'] for w in tw if not w['locators']]})")
    T.CUR.update(flags=dict(T.FLAGS_V32))
    AT = T.AdverseUnits32(T.V3.Ids3(T.base_dictionary(dj), L, rrules), rules["adverse"])
    lost = []
    for kind, f, p, loc, text in [(x[1], x[2], x[3], x[4], x[5]) for x in T.ledger_texts(L) if x[0] == "adverse"]:
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
                continue   # 멤버 나눔 기호(ADV_MEMBER_SPLIT) — 구조로 보존
            if nt not in cov and not any(nt in c for c in cov):   # 분해기는 공백 토큰 단위라 「줄입니다.[3][9]」처럼 붙은 꼴로 보존된다
                lost.append((loc, t))
    line(not lost, f"V3.2-1 제거 토큰 보존(버림 0) — 부작용 축 원장 문구 전수 재분해 · 어디에도 없는 토큰 {len(lost)} {lost[:4]}")
    # V3.2-2
    vp = R["v32"]["variant_pairs"]
    line(all(p_["status"] == "proposed" and p_["applied"] is False for p_ in vp) and len(seeds["variant_pairs"]) == len(vp), f"V3.2-2 변형 쌍 {len(vp)} 전부 목록 승인(proposed · applied=false · 자동 매칭 0)")
    gl = ad["gloss_pairs"]
    line(all(x["locator"] for x in gl), f"V3.2-2 병기 쌍 {len(gl)} 전부 locator")
    # V3.2-3/4/6
    rows = [(k, r) for k, v in seeds["seeds"].items() for r in v["rows"] if r.get("status") == "proposed"]
    line(all(r.get("locators") and (r.get("n", 0) >= 2 or len(r["locators"]) >= 2) for k, r in rows if k not in ("site", "product_abbrev")) and all(r.get("locators") for k, r in rows if k == "product_abbrev") and all((r.get("locators") or any(x["locators"] for x in r.get("synonyms", []))) for k, r in rows if k == "site"),
         f"V3.2-3 씨앗 후보(proposed) {len(rows)} 전부 locator · 빈도 ≥2 또는 locator ≥2(V3.2-5 줄임말 목록은 쌍 전부 · locator 있음)")
    site_vals = {r["value"] for r in seeds["seeds"]["site"]["rows"]}
    need = ["이마", "미간", "눈가", "눈밑", "눈꺼풀", "코", "코끝", "팔자주름", "볼", "광대", "턱", "턱선", "사각턱", "입술", "목", "목주름", "복부", "옆구리", "팔뚝", "허벅지", "종아리", "힙", "등", "가슴", "겨드랑이", "손", "발", "두피", "얼굴 전체", "바디 전체", "피부", "피하 지방층", "근육", "혈관", "점막", "주사 부위", "시술 부위"]
    line(set(need) <= site_vals and all(r["kind"] in ("anatomical", "region", "layer", "relative") and (r["parent"] is None or r["parent"] in site_vals) for r in seeds["seeds"]["site"]["rows"]), f"V3.2-4 부위 닫힌 목록 {len(site_vals)} · 발주서 값 전부 · kind 4 · parent 는 목록 안")
    line([e["canonical"] for e in D["site"]["entries"]] == [e["canonical"] for e in D31["site"]["entries"]] and [e["canonical"] for e in D["ingredient_material"]["entries"]] == [e["canonical"] for e in D31["ingredient_material"]["entries"]], "V3.2-3 씨앗 적용 0 — site · ingredient_material 값 = v3.1")
    eqp = R["equipment"]["products"]
    line(all(p_["origin"] == "taxonomy" and p_["license_status"] == "미확인" and p_["status"] == "unreviewed" for p_ in eqp), f"V3.2-5 장비 제품 {len(eqp)} 전부 origin=taxonomy · license_status=미확인 · unreviewed")
    b, a = R["v32"]["before"], R["v32"]["after"]
    line(a["catalog_self"] < b["catalog_self"] and a["catalog_by_what_kind"].get("product", 0) > b["catalog_by_what_kind"].get("product", 0), f"V3.2-5 항목 자신 {b['catalog_self']} → {a['catalog_self']} · product {b['catalog_by_what_kind'].get('product')} → {a['catalog_by_what_kind'].get('product')}")
    ab = seeds["seeds"]["product_abbrev"]["rows"]
    line(all(r["status"] in ("proposed", "⑦") for r in ab), f"V3.2-5 줄임말 후보 {len(ab)} 전부 승인 묶음(자동 아님)")
    ingv = {T.norm(e["canonical"]) for e in D["ingredient_material"]["entries"]}
    iw = [r for r in R["procedure"]["catalog"] if r.get("what_kind") == "ingredient"]
    PT = {t["id"]: t for t in R["procedure"]["tuples"]}
    line(all(T.norm(PT[r["procedure_id"]]["what_label"]) in ingv for r in iw) and "ingredient" in erd["enums"]["procedure.what_kind"], f"V3.2-6 성분 what {len(iw)} 전부 성분 사전 값 · what_kind 열거형")
    # V3.2-7
    notes = [m for m in ad["memo_phrases"] if m["status"] == "note"]
    line(all(not m["events_seen"] for m in notes), f"V3.2-7 not_adverse_note {len(notes)} 전부 사건 조각 0")
    line(all(m["why"] for m in ad["memo_phrases"] if m["status"] == "sentence") and set(e["status"] for e in ad["phrase_dictionary"]) <= {"exact", "new"}, "V3.2-7 설명문 판정 근거 있음 · 문구 사전 status ∈ exact|new(+메모 note|sentence)")
    # V3.2-8
    line(s["inheritance_missing_basis"] == 0 and s["inheritance_copied_values"] == 0, f"V3.2-8 basis 없는 상속 {s['inheritance_missing_basis']} · 복사된 값 {s['inheritance_copied_values']}")
    fam_keys = {f"R15:{e['from'][1]}→{e['unit']}" for e in ad["edges"] if e["from"][0] == "modality"}
    badref = [x for e in ad["edges"] for x in e["inheritance"] if x["basis"] == "family" and str(x["ref"]).startswith("R15:") and x["ref"] not in fam_keys and e["from"][0] != "modality"]
    line(not badref, f"V3.2-8 family 참조 전부 실제 계열 엣지(어긋남 {len(badref)})")
    # V3.2-9
    line(s["timelines"] == 10 and s["timeline_lines"] == 435 and s["timeline_phases"] == 43, f"V3.2-9 타임라인 {s['timelines']} · 단계 {s['timeline_phases']} · 줄 {s['timeline_lines']}")
    r15 = next(r for r in erd["relations"] if r["id"] == "R15")
    line(not {"period", "phase_label", "reaction_level"} & {x["name"] for x in r15["attrs"]} and {"timeline_refs", "inheritance"} <= {x["name"] for x in r15["attrs"]}, "V3.2-9 R15 period/phase_label/reaction_level → timeline_refs 참조 · V3.2-8 inheritance 속성")
    # 구조
    line(len(erd["entities"]) == 22 and len(erd["relations"]) == 34 and len(erd["decision_kinds"]) == 20 and {"R33", "R34", "R35"} <= rels and {"post_procedure_timeline", "emergency_sign"} <= ents, "구조: 개체 22 · 관계 34(R33·R34·R35) · 결정 kind 20")
    line(len(erd["decisions"]) == len(e31["decisions"]) + 1 and erd["decisions"][:len(e31["decisions"])] == e31["decisions"], f"결정 레코드 v3.1 {len(e31['decisions'])} 이관 그대로 + DEC-28(proposed)")

    # ---- 검토 S-1 ~ S-4
    out.append("### S. 검토 반영(erd-v3.2-review.md S-1~S-4)")
    dict_words = base_ev
    absorbed = [n["canonical"] for n in ad["ledger_events"] if any(T.norm(w) in dict_words for w in n["canonical"].split()) and T.norm(n["canonical"]) not in dict_words]
    line(not absorbed, f"S-1 사전 사건을 낱말로 품은 원장 노드 0(사전 사건은 exact · 옆 토큰은 side) — 있음 {absorbed[:5]}")
    hz = next((e for e in ad["phrase_dictionary"] if "시술 후 일시적인 홍조와 부종" in e["raw_variants"]), None)
    line(hz is not None and {c["event"] for c in hz["candidates"]} >= {"부종", "홍조"}, "S-1 실례 「시술 후 일시적인 홍조와 부종」→ 부종 exact + 홍조 new")
    line(all(d["existing_kind"] in ("dictionary", "ledger") and d["grade"] in ("strong", "weak") for d in ad["duplicate_pairs"]) and all(r in ("substring",) or r.startswith("prefix") or r == "first_syllable" for d in ad["duplicate_pairs"] if d["grade"] == "weak" for r in d["rules"]),
         f"S-2 ⑦ 는 노드끼리(사전 ↔ 노드 {sum(1 for d in ad['duplicate_pairs'] if d['existing_kind'] == 'dictionary')} · 노드 ↔ 노드 {sum(1 for d in ad['duplicate_pairs'] if d['existing_kind'] == 'ledger')}) · strong {s['dup_pairs_strong']} / weak {s['dup_pairs_weak']}(weak 는 부분 문자열·접두·첫 음절만 · 기본 게이트 아님)")
    BAN = ("raw_name", "unlinked", "adverse_expression", "RAW:", "R29")
    ae = next(e for e in erd["entities"] if e["key"] == "adverse_effect")
    fields = json.dumps({"attrs": ae["attrs"], "identity": ae["identity"], "R15": next(r for r in erd["relations"] if r["id"] == "R15"), "enums": {k: v for k, v in erd["enums"].items() if k.startswith("adverse")},
                         "id_rule": erd["id_rule"]["adverse_effect"], "ata": next(k for k in erd["decision_kinds"] if k["kind"] == "adverse_tuple_assign")}, ensure_ascii=False)
    hits = {b: fields.count(b) for b in BAN if b in fields}
    cmrows = [r for r in cm if any(b in r["note"] for b in BAN) and "person_condition" not in r["note"] and "조건" not in r["note"]]
    line(not hits and not cmrows and not any(k.startswith("adverse_expression.") for k in erd["enums"]) and "table_line.ref_status" in erd["enums"],
         f"S-3 정의 표(adverse_effect 속성·식별자 · R15 · 부작용 열거형 · id_rule · adverse_tuple_assign)·행선지 비고에 옛 잔재 0(남은 {hits} · 행 {len(cmrows)}) · table_line.ref_status")
    tw_ = {(w["kind"], w["word"]) for w in tw}
    line({("predicate", "는"), ("relaxed", "시"), ("relaxed", "이")} <= tw_ and all(w["locators"] for w in tw if w["kind"] in ("predicate", "relaxed")), f"S-4 토큰화 보강(관형형·연결형 {sum(1 for w in tw if w['kind'] == 'predicate')} · relaxed {sum(1 for w in tw if w['kind'] == 'relaxed')}) 원소마다 locator")

    # ---- U
    out.append("### U. 사용자 정의")
    line(erd["user_definitions"] == e31["user_definitions"] and erd["user_definitions_v31"] == e31["user_definitions_v31"] and erd["explicit_exception_v31"] == e31["explicit_exception_v31"], "정의 1·2(v3.1 개정판)·3 · 명시 예외 글자 그대로")
    p31 = {x["key"]: x["text"] for x in e31["principles"]}
    p32 = {x["key"]: x["text"] for x in erd["principles"]}
    line(p31["B"] == p32["B"] and p31["C"] == p32["C"] and p31["A"] != p32["A"] and p31["D"] != p32["D"], "원칙 B·C 불변 · A·D 는 v3.2 문장(사용자 결정)")
    n_pass, n_fail = sum(1 for x in out if x.startswith("- PASS")), sum(1 for x in out if x.startswith("- FAIL"))
    head = f"**{'PASS' if ok_all else 'FAIL'} {n_pass}/{n_pass + n_fail}**"
    return ok_all, head + "\n\n" + "\n".join(out)


if __name__ == "__main__":
    ok, rep = run_checks()
    print(rep)
    raise SystemExit(0 if ok else 1)
