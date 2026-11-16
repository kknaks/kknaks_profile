#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v2.2 검산 (v2.1 검산 A~I 전부 유지 — v2.2 에서 바뀐 기대값은 항목 안에 · + J v2.2 수정 6건). 파일은 erd-v2.2.* 를 읽고 v2.1·v2 산출물과 대조한다.

 A. 잎 키 행선지: erd-v2-column-map.md 의 행 = 원장 스캔 잎 키 573 + step1-products.json 잎 키 499 = 1,072, 중복 0, 미정 0, 범주 5 안, 표적이 ERD 에 정의됨. 이동 표 = v1.1 표와 표적이 다른 행 전부.
 B. 사전 값 출처: erd-v2-dictionaries.json 의 모든 정준값·동의어에 출처 ≥1, 각 출처가 원장/step1 에 실제로 그 값(value)·키(key)·부분 문자열(derived)을 가진다. default 는 course 「미상」 하나만.
 C. ERD 출처 키: erd-v2.json 개체 속성·관계의 출처 'file:path' 가 잎 키에 존재한다.
 D. 바이트: erd-v2.json 의 sha256 이 원장 21 + step1 과 같다.
 E. 분해 규칙 재현: erd-v1.1-resolve.py 를 v2 사전으로 다시 돌려 자리별 (n, 해결, 분해 성공, 미해결) 이 erd-v2.json 및 erd-v1.1.json 의 수치와 같다.
 F. 처분 반영: 부위 사전 21(확장 0) · 기법 사전 = mechanism[] distinct 12 · 처분 19 · complications trust_flag · q14 미배정 0 · 8-2 표 51.
 G. 튜플 실측 재현: erd-v2-tuples.py 를 다시 돌려 요약 수치가 erd-v2.json(tuple_report)·erd-v2-tuples.json 과 같다. 튜플 id = 식별자 규칙(sha256(what|site|technique) / sha256(event|site|course)) 재계산 일치. 분류 항목 521 전부 튜플 있음. 접힌 표 항목 합 = 521. complications 65 전부 표에 있음.
 I. v2.1 접힘 규칙: fallback_to_parent=false(규칙 데이터) · 부모 하위분류 fallback 0 · 접힌 튜플(항목 ≥2)은 세 칸 전부 사전 값·미등록 0 · partial 항목이 섞인 접힌 튜플 0(둘 이상 0 포함) · 미등록 조각 있는 항목은 what=항목 자신(CAT- id · candidate_name = 미등록 조각) · 참조 ②③ partial 0 · 미등록 조각 있는 참조 = 미해결(튜플 없음) · ② 미해결 수 = v1.1 분해 규칙 미해결 수 · 행선지 표·사전 값이 v2 와 동일 · 개체/관계/사전 수 v2 와 같음 · 부작용 접힘 확인(발주서 전제 검증 · NOTE).
 J. v2.2: 미상 포함 튜플 접힘 0 · 버린 조각 0(extra_* 실값) · 상속 기법 0 · ④ 자동 해결마다 conflict 레코드 규칙 명시 · decision kind 7 + 공통 필드 · 기존 결정 22 이관 · course 출처 문장 3곳 동일.
 H. 구조 변경 반영: 개체 21(catalog_item·adverse_expression) · 관계 31(R26~R31) · 사전 46(adverse_event_type·course·relative_site · procedure_name 없음) · target_depth 에 catalog_item · package.kind 에 combo_ref · 사건 사전 값마다 category 7 중 하나 · v1.1 procedure 속성이 catalog_item 에 전부 있음 · 이동 표 행 수 = 실제 달라진 행 수.

실행: python3 erd-v2.2-check.py  (같은 폴더의 산출물 + 스캔 JSON + 원장 디렉토리 + step1-products.json)
"""
import hashlib
import importlib.util
import json
import os
import re
import sys
import unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = "/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26"
STEP1 = "step1-products.json"
CODE_KEY_RE = re.compile(r"^(?:[A-Z]{1,2}\d+(?:-\d+)*|M\d+_to_M\d+|auto-\d+-\d+)$")
DESTS = {"개체", "사전", "엣지", "브론즈", "버림"}
CATEGORIES = {"국소 일시 반응", "염증/감염", "혈관", "신경", "색소", "구조/이물", "전신"}


def norm(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", str(s)).casefold())


def mkid(prefix, key):
    return f"{prefix}-{hashlib.sha256(norm(key).encode()).hexdigest()[:10]}"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def walk(data, path):
    toks = path.split(".") if path else []

    def rec(node, i):
        if i == len(toks):
            yield node
            return
        tok = toks[i]
        arr = tok.endswith("[]")
        key = tok[:-2] if arr else tok
        if key == "{code}":
            if isinstance(node, dict):
                for k, v in node.items():
                    if CODE_KEY_RE.match(k):
                        yield from after(v, i, arr)
        elif isinstance(node, dict) and key in node:
            yield from after(node[key], i, arr)

    def after(v, i, arr):
        if arr:
            if isinstance(v, list):
                for it in v:
                    yield from rec(it, i + 1)
        else:
            yield from rec(v, i + 1)

    yield from rec(data, 0)


def load():
    scan = json.load(open(os.path.join(HERE, "bronze-ledger-column-scan.json"), encoding="utf-8"))
    erd = json.load(open(os.path.join(HERE, "erd-v2.2.json"), encoding="utf-8"))
    dic = json.load(open(os.path.join(HERE, "erd-v2.2-dictionaries.json"), encoding="utf-8"))
    cmap = open(os.path.join(HERE, "erd-v2.2-column-map.md"), encoding="utf-8").read()
    V2 = {"erd": json.load(open(os.path.join(HERE, "erd-v2.json"), encoding="utf-8")), "dic": json.load(open(os.path.join(HERE, "erd-v2-dictionaries.json"), encoding="utf-8")),
          "cmap": open(os.path.join(HERE, "erd-v2-column-map.md"), encoding="utf-8").read(), "tup": json.load(open(os.path.join(HERE, "erd-v2-tuples.json"), encoding="utf-8"))}
    V2["v21"] = {"erd": json.load(open(os.path.join(HERE, "erd-v2.1.json"), encoding="utf-8")), "dic": json.load(open(os.path.join(HERE, "erd-v2.1-dictionaries.json"), encoding="utf-8")),
                 "cmap": open(os.path.join(HERE, "erd-v2.1-column-map.md"), encoding="utf-8").read(), "tup": json.load(open(os.path.join(HERE, "erd-v2.1-tuples.json"), encoding="utf-8"))}
    V2["md"] = open(os.path.join(HERE, "erd-v2.2.md"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, "erd-v2.2.md")) else ""
    cmap11 = open(os.path.join(HERE, "erd-v1.1-column-map.md"), encoding="utf-8").read()
    erd11 = json.load(open(os.path.join(HERE, "erd-v1.1.json"), encoding="utf-8"))
    tup = json.load(open(os.path.join(HERE, "erd-v2.2-tuples.json"), encoding="utf-8"))
    ledgers = {f: json.load(open(os.path.join(LEDGER, f), encoding="utf-8")) for f in scan["files"]}
    ledgers[STEP1] = json.load(open(os.path.join(HERE, STEP1), encoding="utf-8"))
    scanner = load_module("bronze_scan", os.path.join(HERE, "bronze-ledger-column-scan.py"))
    s1 = scanner.FileScan(os.path.join(HERE, STEP1)).run()
    return scan, erd, dic, cmap, cmap11, erd11, tup, ledgers, s1, V2


def parse_column_map(cmap):
    rows, cur = [], None
    for line in cmap.splitlines():
        m = re.match(r"^## `([^`]+\.json)`", line)
        if m:
            cur = m.group(1)
            continue
        if cur and line.startswith("| ") and not line.startswith("| #") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
            if len(cells) >= 7 and cells[0].isdigit():
                rows.append({"file": cur, "path": cells[1].strip("`"), "dest": cells[4], "target": cells[5].strip("`")})
    return rows


def run_checks():
    scan, erd, dic, cmap, cmap11, erd11, tup, ledgers, s1, V2 = load()
    out, ok_all = [], True
    notes = []

    def note(text):
        notes.append(text)
        out.append(f"- NOTE — {text}")

    def line(ok, text):
        nonlocal ok_all
        ok_all = ok_all and ok
        out.append(f"- {'PASS' if ok else 'FAIL'} — {text}")

    # ---- A
    leaf = {(f, p) for f, v in scan["files"].items() for p in v["leaf_paths"]} | {(STEP1, p) for p in s1["leaf_paths"]}
    n_ledger, n_s1 = scan["total_leaf_paths"], s1["leaf_count"]
    rows = parse_column_map(cmap)
    rows11 = parse_column_map(cmap11)
    got = Counter((r["file"], r["path"]) for r in rows)
    dup = [k for k, n in got.items() if n > 1]
    missing, extra = sorted(leaf - set(got)), sorted(set(got) - leaf)
    bad_dest = [r for r in rows if r["dest"] not in DESTS or not r["target"]]
    out.append("### A. 잎 키 행선지 (원장 21 + step1 · 이동 표)")
    out.append("")
    line(len(rows) == n_ledger + n_s1 and n_ledger == 573 and len(rows) == 1072, f"행선지 행 {len(rows)} = 원장 잎 키 {n_ledger}(=573) + step1 잎 키 {n_s1} = {n_ledger + n_s1} (=1,072)")
    line(not dup, f"중복 행 {len(dup)}")
    line(not missing and not extra, f"스캔에만 {len(missing)} · 표에만 {len(extra)}" + (": " + "; ".join(f"{a}:{b}" for a, b in (missing + extra)[:5]) if missing or extra else ""))
    line(not bad_dest, f"행선지 범주 밖/표적 없음(미정) {len(bad_dest)}")
    dist = Counter(r["dest"] for r in rows)
    dist1 = Counter(r["dest"] for r in rows if r["file"] == STEP1)
    out.append("- 행선지 분포(전체): " + " · ".join(f"{k} {v}" for k, v in sorted(dist.items(), key=lambda x: -x[1])) + f" (합 {sum(dist.values())}) · step1 만: " + " · ".join(f"{k} {v}" for k, v in sorted(dist1.items(), key=lambda x: -x[1])) + f" (합 {sum(dist1.values())})")
    ents = {e["key"] for e in erd["entities"]}
    rels = {r["id"] for r in erd["relations"]}
    dnames = {d["name"] for d in dic["dictionaries"]}
    bad_t = []
    for r in rows:
        t = r["target"]
        if r["dest"] == "개체" and t.split(".")[0].split("(")[0] not in ents:
            bad_t.append(r)
        elif r["dest"] == "사전" and t.replace("dict:", "") not in dnames:
            bad_t.append(r)
        elif r["dest"] == "엣지" and re.match(r"^R\d+", t) and re.match(r"^R\d+", t).group(0) not in rels:
            bad_t.append(r)
    line(not bad_t, f"표적이 ERD 에 정의되지 않은 행 {len(bad_t)}" + (": " + "; ".join(f"{b['file']} {b['path']} → {b['target']}" for b in bad_t[:5]) if bad_t else ""))
    m11 = {(r["file"], r["path"]): (r["dest"], r["target"]) for r in rows11}
    changed = [(r["file"], r["path"], m11.get((r["file"], r["path"])), (r["dest"], r["target"])) for r in rows if m11.get((r["file"], r["path"])) != (r["dest"], r["target"])]
    moves = erd.get("column_map_moves", [])
    moves22 = erd.get("column_map_moves_v2_2", [])
    mv = {(m["file"], m["path"]) for m in moves} | {(m["file"], m["path"]) for m in moves22}
    line(len(changed) == len(mv) and {(c[0], c[1]) for c in changed} == mv, f"이동 표 v1.1→v2 {len(moves)} + v2.1→v2.2 {len(moves22)} = v1.1 표와 표적이 다른 행 {len(changed)} (같은 집합)")
    rows21 = parse_column_map(V2["v21"]["cmap"])
    m21 = {(r["file"], r["path"]): (r["dest"], r["target"]) for r in rows21}
    ch21 = {(r["file"], r["path"]) for r in rows if m21.get((r["file"], r["path"])) != (r["dest"], r["target"])}
    line(ch21 == {(m["file"], m["path"]) for m in moves22} and len(rows21) == len(rows), f"v2.1 표와 표적이 다른 행 {len(ch21)} = 이동 표 v2.1→v2.2 {len(moves22)} (같은 집합 · " + ", ".join(f"{m['path'].rsplit('.', 1)[-1]}: {m['v2_1'].split(':', 1)[1]}→{m['v2_2'].split(':', 1)[1]}" for m in moves22) + ")")
    line(not any("procedure." in r["target"] for r in rows if r["dest"] == "개체"), f"procedure.* 행선지 0 (v1.1 procedure 행은 전부 catalog_item.* 로) · catalog_item 행 {sum(1 for r in rows if r['target'].startswith('catalog_item'))} · adverse_expression 행 {sum(1 for r in rows if r['target'].startswith('adverse_expression'))} · adverse_effect.name 행 {sum(1 for r in rows if r['target'] == 'adverse_effect.name')}")
    out.append("")

    # ---- B
    out.append("### B. 사전 값 출처")
    out.append("")
    n_can = n_syn = 0
    no_src, bad_src, defaults = [], [], []
    cache = {}

    def vals(f, p):
        if (f, p) not in cache:
            cache[(f, p)] = {norm(v) for v in walk(ledgers[f], p) if not isinstance(v, (list, dict)) and v is not None}
        return cache[(f, p)]

    def check_src(dname, value, s):
        f, p, kind = s["file"], s["path"], s.get("kind", "value")
        if kind == "default":
            defaults.append(f"{dname}:{value}")
            return None
        if f not in ledgers:
            return f"{dname}:{value} 파일 없음 {f}"
        if kind == "value":
            if (f, p) not in leaf:
                return f"{dname}:{value} 잎 키 아님 {f}:{p}"
            if norm(value) not in vals(f, p):
                return f"{dname}:{value} 값이 {f}:{p} 에 없음"
        elif kind == "derived":
            if (f, p) not in leaf:
                return f"{dname}:{value} 잎 키 아님 {f}:{p}"
            if not any(norm(value) in v for v in vals(f, p)):
                return f"{dname}:{value} 가 {f}:{p} 값의 부분 문자열이 아님"
        else:
            if (f, p) not in leaf:
                return f"{dname}:{value} 키 경로 없음 {f}:{p}"
            segs = {x.replace("[]", "") for x in p.split(".")}
            nsegs = {norm(x) for x in segs}
            if norm(value) not in nsegs and not any(x.startswith(norm(value)) for x in nsegs) and not (value in ledgers[f] if isinstance(ledgers[f], dict) else False):
                leafname = p.rsplit(".", 1)[-1].replace("[]", "")
                aliases = {"day": "days", "month": "month", "week": "week", "mm": "mm", "ml": "ml", "cm": "cm", "percent": "percent", "minute": "time"}
                if not (value in aliases and (aliases[value] in leafname.lower() or leafname.lower().endswith(aliases[value]) or leafname in ("prepTime", "durationMin", "durationMax"))):
                    return f"{dname}:{value} 가 경로 {f}:{p} 의 키/섹션 이름이 아님"
        return None

    for d in dic["dictionaries"]:
        for e in d["entries"]:
            n_can += 1
            if not e["sources"]:
                no_src.append(f"{d['name']}:{e['canonical']}")
            for s in e["sources"]:
                err = check_src(d["name"], e["canonical"], s)
                if err:
                    bad_src.append(err)
            for sy in e["synonyms"]:
                n_syn += 1
                if not sy["sources"]:
                    no_src.append(f"{d['name']}:{e['canonical']}~{sy['value']}")
                for s in sy["sources"]:
                    err = check_src(d["name"], sy["value"], s)
                    if err:
                        bad_src.append(err)
    line(not no_src, f"출처 없는 사전 값 {len(no_src)} / 정준값 {n_can} + 동의어 {n_syn}")
    line(not bad_src, f"원장/step1 에서 확인 안 되는 출처 {len(bad_src)}" + (": " + "; ".join(bad_src[:8]) if bad_src else ""))
    line(defaults == ["course:미상"], f"출처 kind=default 는 {defaults} 하나뿐 (ERD 정의값)")
    nval = sum(1 for d in dic["dictionaries"] if d.get("kind", "value") == "value")
    out.append(f"- 사전 {len(dic['dictionaries'])}개(값 사전 {nval} + 이름 색인 {len(dic['dictionaries']) - nval}) · 정준값 {n_can} · 동의어 {n_syn} · 후보 {sum(len(d['candidates']) for d in dic['dictionaries'])} · 출처 100% 확인")
    out.append("")

    # ---- C
    out.append("### C. ERD 출처 키·표적")
    out.append("")
    leaf_by_file = {}
    for f, p in leaf:
        leaf_by_file.setdefault(f, set()).add(p)

    def src_exists(s):
        if ":" not in s:
            return False
        f, p = s.split(":", 1)
        files = list(leaf_by_file) if f == "*" else [f]
        for ff in files:
            if ff not in leaf_by_file:
                continue
            if p in leaf_by_file[ff]:
                return True
            if "*" in p:
                rx = re.compile("^" + re.escape(p).replace(r"\*", r"[^.]+") + "$")
                if any(rx.match(x) for x in leaf_by_file[ff]):
                    return True
            if p.startswith("*.") and any(x.endswith(p[1:]) for x in leaf_by_file[ff]):
                return True
        return False

    bad, n_src = [], 0
    for e in erd["entities"]:
        for a in e["attrs"]:
            for s in a["sources"]:
                n_src += 1
                if not src_exists(s):
                    bad.append(f"{e['key']}.{a['name']} ← {s}")
    for r in erd["relations"]:
        for s in r["sources"]:
            n_src += 1
            if not src_exists(s):
                bad.append(f"{r['id']} ← {s}")
    line(not bad, f"ERD 출처 키 {n_src}개 중 잎 키에 없는 것 {len(bad)}" + (": " + "; ".join(bad[:8]) if bad else ""))
    used_dicts = {r["target"].replace("dict:", "") for r in rows if r["dest"] == "사전"}
    line(used_dicts <= dnames, f"행선지 표의 사전 {len(used_dicts)}개 전부 사전 파일에 있음")
    out.append(f"- 개체 {len(erd['entities'])} · 관계 {len(erd['relations'])} · 사전 {len(dic['dictionaries'])} · 처분 {len(erd['review_dispositions'])} · 결정 레코드 {len(erd['decisions'])}")
    out.append("")

    # ---- D
    out.append("### D. 브론즈 바이트 (원장 21 + step1)")
    out.append("")
    badsha = []
    for fm in erd["source_files"]:
        path = os.path.join(LEDGER, fm["file"]) if fm["file"] != STEP1 else os.path.join(HERE, STEP1)
        if hashlib.sha256(open(path, "rb").read()).hexdigest() != fm["sha256"]:
            badsha.append(fm["file"])
    line(not badsha and len(erd["source_files"]) == 22, f"원장 21 + step1 sha256 일치 (파일 {len(erd['source_files'])}, 불일치 {len(badsha)})")
    s1m = next(fm for fm in erd["source_files"] if fm["file"] == STEP1)
    line(s1m["kind"] == "research_artifact" and s1m["trust_tier"] == 3 and "tier2_when" in s1m.get("trust_tier_rule", {}), f"step1 = research_artifact · 기본 3 · 허가 필드 조건부 2 ({s1m['trust_tier_rule']['tier2_licenses']}/{s1m['trust_tier_rule']['licenses_total']} 건)")
    out.append("")

    # ---- E
    out.append("### E. 분해 규칙 재현 (erd-v1.1-resolve.py 를 v2 사전으로 재실행)")
    out.append("")
    res = load_module("erd_v11_resolve", os.path.join(HERE, "erd-v1.1-resolve.py"))
    tuples_mod = load_module("erd_v22_tuples", os.path.join(HERE, "erd-v2.2-tuples.py"))
    OUT, TOTAL = res.run_all(tuples_mod.with_alias(dic), erd["resolve_rules"], {k: v for k, v in ledgers.items() if k != STEP1}, ledgers[STEP1], None)
    diffs, diffs11 = [], []
    for k, v in erd["resolution_report"].items():
        w = OUT.get(k)
        if not w:
            diffs.append(f"{k}: 자리 없음")
            continue
        for key in ("n", "resolved", "decomposed", "unresolved"):
            if v[key] != w[key]:
                diffs.append(f"{k}.{key}: json {v[key]} vs 재실행 {w[key]}")
            if erd11["resolution_report"].get(k, {}).get(key) != w[key]:
                diffs11.append(f"{k}.{key}: v1.1 {erd11['resolution_report'].get(k, {}).get(key)} vs v2 {w[key]}")
    line(not diffs and set(OUT) == set(erd["resolution_report"]), f"자리 {len(OUT)}개 (n·해결·분해 성공·미해결) 재현 불일치 {len(diffs)}" + (": " + "; ".join(diffs[:5]) if diffs else ""))
    line(not diffs11, f"v1.1·v2 수치와 같음 (불일치 {len(diffs11)}) — 사전 값 동일" + (": " + "; ".join(diffs11[:5]) if diffs11 else ""))
    line(TOTAL["unresolved_v1_1"] == erd["resolution_total"]["unresolved_v1_1"] and TOTAL["decomposed_v1_1"] == erd["resolution_total"]["decomposed_v1_1"], f"합계 재현: 미해결 {TOTAL['unresolved_v1_1']} · 분해 성공·항목 없음 {TOTAL['decomposed_v1_1']} · 해결 {TOTAL['resolved_v1_1']}")
    rr = erd["resolve_rules"]
    line(rr["step3_assemble"].get("no_similarity") is True and rr["step2_decompose"]["dictionary_order"] == ["product", "modality_subcategory", "procedure", "site", "spec", "product_tier"], "규칙 데이터: 유사도 금지 · 사전 순서 제품→하위분류→분류 항목(procedure 자리 = catalog_item_name)→부위→규격→product_tier")
    out.append("")

    # ---- F
    out.append("### F. 처분 반영 (v1.1 그대로)")
    out.append("")
    D = {d["name"]: d for d in dic["dictionaries"]}
    site = D["site"]["entries"]
    ext = [e for e in site if e.get("site_kind") not in ("backbone", "taxonomy_site_label")]
    line(not ext and sum(1 for e in site if e.get("site_kind") == "backbone") == 11 and len(site) == 21, f"부위 사전 {len(site)} = 뼈대 11 + taxonomy 부위 라벨 {sum(1 for e in site if e.get('site_kind') == 'taxonomy_site_label')} · 확장 {len(ext)} (공유 사전 유지)")
    mech = {norm(v) for v in walk(ledgers["procedure-profiles.json"], "profiles[].mechanism[]")}
    tech = {norm(e["canonical"]) for e in D["technique"]["entries"]}
    line(tech == mech and len(tech) == 12, f"기법 사전 {len(tech)} = profiles[].mechanism[] distinct {len(mech)}")
    line(len(erd["review_dispositions"]) == 19 and sum(1 for d in erd["review_dispositions"] if d["decided_by"] == "사용자") == 4, f"처분 {len(erd['review_dispositions'])} (사용자 {sum(1 for d in erd['review_dispositions'] if d['decided_by'] == '사용자')} · 워커 확정 {sum(1 for d in erd['review_dispositions'] if d['decided_by'] != '사용자')})")
    comp = next(fm for fm in erd["source_files"] if fm["file"] == "complications.json")
    line(comp["trust_tier"] == 3 and "AI 컨센서스 추정" in (comp.get("trust_flag") or ""), "complications.json 3 유지 + 「AI 컨센서스 추정」")
    q14 = erd["q14_bundles"]
    line(all(not r["bucket"].startswith("미배정") for r in q14) and all(r["scope"] for r in q14 if r["bucket"].startswith("②")), f"질문 14 묶음 {len(q14)}: ① {sum(1 for r in q14 if r['bucket'].startswith('①'))} · ② {sum(1 for r in q14 if r['bucket'].startswith('②'))}(범위 검토) · 미배정 {sum(1 for r in q14 if r['bucket'].startswith('미배정'))}")
    line(len(erd["site_replacement_8_2"]) == 51, f"8-2 처분 표 {len(erd['site_replacement_8_2'])} 행 (v1 확장 51)")
    out.append("")

    # ---- G
    out.append("### G. 튜플 실측 재현 (erd-v2.2-tuples.py 재실행)")
    out.append("")
    TUP = tuples_mod.run_all(dic, erd["tuple_rules"], {k: v for k, v in ledgers.items() if k != STEP1}, erd["resolve_rules"])
    gd = []
    for axis in ("procedure", "adverse"):
        a, b, c = TUP[axis]["summary"], erd["tuple_report"][axis], tup[axis]["summary"]
        for k in a:
            if k in ("unregistered_top30_by_origin", "unregistered_by_origin", "unregistered_all", "unregistered_top30"):
                continue
            if json.dumps(a[k], ensure_ascii=False, sort_keys=True, default=str) != json.dumps(b.get(k), ensure_ascii=False, sort_keys=True, default=str) or json.dumps(a[k], ensure_ascii=False, sort_keys=True, default=str) != json.dumps(c.get(k), ensure_ascii=False, sort_keys=True, default=str):
                gd.append(f"{axis}.{k}")
    line(not gd, f"요약 수치 재현 불일치 {len(gd)} (erd-v2.2.json tuple_report · erd-v2.2-tuples.json 과 비교)" + (": " + "; ".join(gd[:6]) if gd else ""))
    ps, as_ = TUP["procedure"]["summary"], TUP["adverse"]["summary"]
    same_ids = {t["id"] for t in TUP["procedure"]["tuples"]} == {t["id"] for t in tup["procedure"]["tuples"]} and {t["id"] for t in TUP["adverse"]["tuples"]} == {t["id"] for t in tup["adverse"]["tuples"]}
    line(same_ids, f"튜플 id 집합 재현 일치 (시술 {len(TUP['procedure']['tuples'])} · 부작용 {len(TUP['adverse']['tuples'])})")
    DK = ("product", "modality_subcategory", "modality")

    def prc_id(t):
        alld = t["what_kind"] in DK and t["site_id"] != "none" and t["technique_id"] != "none"
        return mkid("PRC", f"{t['what_id']}|{t['site_id']}|{t['technique_id']}" + ("" if alld else f"|{t['anchor']}")), alld
    badid = [t["id"] for t in TUP["procedure"]["tuples"] if prc_id(t)[0] != t["id"] or prc_id(t)[1] != t["all_dict_values"] or (t["anchor"] is None) != t["all_dict_values"]]
    badid += [t["id"] for t in TUP["adverse"]["tuples"] if t["id"] != mkid("ADV", f"{D['adverse_event_type']['entries'][[e['canonical'] for e in D['adverse_event_type']['entries']].index(t['event'])]['id']}|{t['site_id']}|{t['course_id']}")]
    line(not badid, f"식별자 규칙 재계산 불일치 {len(badid)} (v2.2: 세 칸 전부 사전 값이면 PRC-sha256(what_id|site_id|technique_id), 아니면 PRC-sha256(what_id|site_id|technique_id|anchor) · ADV-sha256(event_id|site_id|course_id))")
    cat = TUP["procedure"]["catalog"]
    n_items = sum(1 for m in ledgers["taxonomy.json"]["modality"] for sc in m["subcategories"] for _ in sc["items"])
    line(len(cat) == n_items == 521 and all(r.get("procedure_id") for r in cat), f"분류 항목 {len(cat)} (= taxonomy 항목 {n_items}) 전부 튜플 있음 (없는 것 {sum(1 for r in cat if not r.get('procedure_id'))})")
    fold_sum = sum(f["n_items"] for f in TUP["procedure"]["folded"])
    line(fold_sum == 521 and len(TUP["procedure"]["folded"]) == ps["catalog_distinct_tuples"], f"접힌 표 항목 합 {fold_sum} = 521 · 튜플 {len(TUP['procedure']['folded'])} = distinct {ps['catalog_distinct_tuples']} (521 → {ps['catalog_distinct_tuples']})")
    comp_n = sum(len(c["complications"]) for c in ledgers["complications.json"]["categories"])
    named = {n for f in TUP["adverse"]["folded"] for n in f["names"]}
    comp_rows = TUP["adverse"]["complications"]
    line(comp_n == 65 == len(comp_rows) and all(r["tuple_ids"] for r in comp_rows), f"complications 이름 {comp_n} 전부 튜플 있음 (없는 것 {sum(1 for r in comp_rows if not r['tuple_ids'])}) · 접힌 표에 등장하는 이름 {len(named)}")
    line(all("catalog_item" in t["origins"] or "reference" in t["origins"] or "market_pricing" in t["origins"] for t in TUP["procedure"]["tuples"]) and all(t["sources"] for t in TUP["adverse"]["tuples"]), "튜플마다 원천(출처 이름·문구) ≥1")
    tech_fam = {pr["id"]: pr["mechanism"] for pr in ledgers["procedure-profiles.json"]["profiles"]}
    bad_t = [t["id"] for t in TUP["procedure"]["tuples"] if t["technique_origin"] not in ("fragment", "none") or (t["technique_origin"] == "none") != (t["technique_id"] == "none")]
    line(not bad_t, f"technique_origin ∈ {{fragment, none}} · none ⇔ technique_id none (위반 {len(bad_t)}) — v2.1 항목 「상속 기법 = R5 단일 기법」은 v2.2 에서 「상속 0」(J-3)으로 바뀜 · 상속 불가 계열 {ps['families_without_single_technique']}")
    unk = [t["id"] for t in TUP["procedure"]["tuples"] if t["what_kind"] not in ("modality", "modality_subcategory", "product", "catalog_item")]
    line(not unk and all(t["site_id"] == "none" or t["site"] in {e["canonical"] for e in site} for t in TUP["procedure"]["tuples"]), f"what ∈ {{modality, modality_subcategory, product, catalog_item(v2.1)}} 위반 {len(unk)} · site ∈ 부위 사전 21 | none")
    line(all(t["course"] in {e["canonical"] for e in D["course"]["entries"]} for t in TUP["adverse"]["tuples"]) and all(t["site_kind"] in ("site", "relative", "none") for t in TUP["adverse"]["tuples"]), "부작용 튜플 course ∈ 경과 사전 · site ∈ {site, relative, none}")
    out.append(f"- 시술: 분류 항목 521 → 튜플 {ps['catalog_distinct_tuples']} · 참조 ② {ps['reference_total']['n']} → 튜플 {ps['reference_total']['tuple']} + combo_ref {ps['reference_total']['combo_ref']} + 미해결 {ps['reference_total']['unresolved']} + 불가 {ps['reference_total']['none']} · ③ 122 → 튜플 {ps['market_pricing']['tuple']} + combo_ref {ps['market_pricing']['combo_ref']} + 불가 {ps['market_pricing']['none']} · 전체 튜플 {ps['tuples_total']} · site none 비율 {ps['tuples_site_none_ratio']} · technique none 비율 {ps['tuples_technique_none_ratio']} · 미등록 조각 distinct {ps['unregistered_distinct']}")
    out.append(f"- 부작용: complications 65 → 튜플 {as_['complications_distinct_tuples']} · 사건 사전 {as_['event_dictionary_values']} · 표현 {as_['expressions_total']['n']} (linked {as_['expressions_total']['linked']} · unlinked {as_['expressions_total']['unlinked']}) · 전체 튜플 {as_['tuples_total']} · 미등록 조각 distinct {as_['unregistered_distinct']}")
    out.append("")

    # ---- H
    out.append("### H. 구조 변경 반영")
    out.append("")
    ek = [e["key"] for e in erd["entities"]]
    line(len(ek) == 21 and "catalog_item" in ek and "adverse_expression" in ek and "procedure" in ek and "adverse_effect" in ek, f"개체 {len(ek)} = v1.1 19 + catalog_item + adverse_expression")
    rids = [r["id"] for r in erd["relations"]]
    line(len(rids) == 31 and all(f"R{i}" in rids for i in range(26, 32)), f"관계 {len(rids)} = v1.1 25 + R26~R31")
    line(len(dnames) == 46 and {"adverse_event_type", "course", "relative_site", "catalog_item_name"} <= dnames and "procedure_name" not in dnames, f"사전 {len(dnames)} = v1.1 43 + 사건·경과·상대 부위 (procedure_name → catalog_item_name 개명)")
    v11_proc = next(e for e in erd11["entities"] if e["key"] == "procedure")
    v2_cat = next(e for e in erd["entities"] if e["key"] == "catalog_item")
    missing_attrs = [a["name"] for a in v11_proc["attrs"] if a["name"] not in {b["name"] for b in v2_cat["attrs"]}]
    missing_src = [s for a in v11_proc["attrs"] for s in a["sources"] if s not in {ss for b in v2_cat["attrs"] for ss in b["sources"]}]
    line(not missing_attrs and not missing_src and v2_cat["identity"].startswith("계열 코드 + 정규화 항목 이름"), f"v1.1 procedure 속성 {len(v11_proc['attrs'])}·출처 전부 catalog_item 에 있음 (빠진 속성 {len(missing_attrs)} · 빠진 출처 {len(missing_src)}) · 식별자 규칙 동일")
    v2_proc = next(e for e in erd["entities"] if e["key"] == "procedure")
    pa = {a["name"] for a in v2_proc["attrs"]}
    line({"what_kind", "what_id", "site_id", "technique_id"} <= pa and "튜플" in v2_proc["definition"], "procedure = 튜플(what_kind·what_id·site_id·technique_id)")
    v2_adv = next(e for e in erd["entities"] if e["key"] == "adverse_effect")
    aa = {a["name"] for a in v2_adv["attrs"]}
    line({"event", "site_ref_kind", "site_ref_id", "course"} <= aa and "name" not in aa, "adverse_effect = 튜플(event·site_ref·course) · 문자열 name 식별자 없음")
    v2_aex = next(e for e in erd["entities"] if e["key"] == "adverse_expression")
    aex_src = {s for a in v2_aex["attrs"] for s in a["sources"]}
    v11_adv = next(e for e in erd11["entities"] if e["key"] == "adverse_effect")
    v11_name_src = set(next(a for a in v11_adv["attrs"] if a["name"] == "name")["sources"]) - {"complications.json:categories[].complications[].name"}
    line(v11_name_src <= aex_src, f"v1.1 adverse_effect.name 의 문구 출처 {len(v11_name_src)}개 전부 adverse_expression 에 있음 (빠진 것 {len(v11_name_src - aex_src)})")
    line("catalog_item" in erd["enums"]["target_depth"] and "procedure" in erd["enums"]["target_depth"], f"target_depth = {erd['enums']['target_depth']}")
    line("combo_ref" in erd["enums"]["package.kind"], "package.kind 에 combo_ref")
    ev = D["adverse_event_type"]["entries"]
    line(all(e.get("category") in CATEGORIES for e in ev) and all(s.get("kind") == "derived" and s["file"] == "complications.json" for e in ev for s in e["sources"]), f"사건 사전 {len(ev)} 값마다 category ∈ 7 분류 · 출처 전부 complications.json 이름(derived) · 동의어 {sum(len(e['synonyms']) for e in ev)}")
    cs = {e["canonical"] for e in D["course"]["entries"]}
    line(cs == {"일시", "지연", "영구", "재발", "미상"}, f"경과 사전 = {sorted(cs)}")
    rs = {e["canonical"] for e in D["relative_site"]["entries"]}
    line(rs == {"주사 부위", "시술 부위"}, f"상대 부위 사전 = {sorted(rs)}")
    promoted = [r["id"] for r in erd["relations"] if r["id"] in ("R3", "R9", "R12", "R15", "R16", "R17", "R18") and "승격" in r["note"]]
    line(len(promoted) == 7, f"시술 축 엣지 7(R3·R9·R12·R15·R16·R17·R18)에 catalog_item·승격 규칙 기록: {promoted}")
    line(len(erd["decisions"]) == 23, f"결정 레코드 {len(erd['decisions'])} = 처분 19 + 구조 변경 2 + v2.1 접힘 규칙 1 (이관 22 · J-6) + v2.2 개정 1")
    out.append("")

    # ---- I (v2.1 항목 — v2.2 기대값)
    out.append("### I. v2.1 접힘 규칙 (v2.1 항목 유지 · v2.2 에서 바뀐 기대값은 항목 안에)")
    out.append("")
    V21 = V2["v21"]
    rr3 = erd["resolve_rules"]["step3_assemble"]
    tr = erd["tuple_rules"]["procedure"]
    line(rr3.get("fallback_to_parent") is False and tr.get("fallback_to_parent") is False and erd["tuple_rules"]["name"] == "tuples_v2_2", f"규칙 데이터: resolve_rules.step3_assemble.fallback_to_parent={rr3.get('fallback_to_parent')} · tuple_rules.procedure.fallback_to_parent={tr.get('fallback_to_parent')} · tuple_rules.name={erd['tuple_rules']['name']}")
    cat = TUP["procedure"]["catalog"]
    fb = [r["name"] for r in cat if str(r.get("what_basis", "")).startswith("parent_subcategory")]
    line(not fb and ps["catalog_fallback_to_parent"] == 0, f"부모 하위분류 fallback 항목 {len(fb)} (v2: {V2['tup']['procedure']['summary']['catalog_by_what_basis'].get('parent_subcategory')})")
    fold2 = [f for f in TUP["procedure"]["folded"] if f["n_items"] >= 2]
    bad_fold = [f for f in fold2 if not f["all_dict_values"] or f["unregistered"] or f["status"] != "complete"]
    line(not bad_fold, f"접힌 튜플(항목 ≥2) {len(fold2)} 전부 세 칸 사전 값(v2.2: site·technique none 도 불가) — 위반 {len(bad_fold)} · 접힌 항목 수 {sum(f['n_items'] for f in fold2)} (v2.1: 튜플 {V21['tup']['procedure']['summary']['catalog_tuples_with_2plus_items']} · 항목 {V21['tup']['procedure']['summary']['catalog_items_in_folded_tuples']})")
    pf1 = [f for f in fold2 if any(s_ != "complete" for s_ in f["item_status"])]
    line(not pf1, f"partial·ambiguous 항목이 섞인 접힌 튜플 {len(pf1)}")
    bad_self = []
    for r in cat:
        if r["result"] != "tuple":
            bad_self.append(f"{r['name']}: result={r['result']}")
            continue
        if r.get("unregistered"):
            if r["what_kind"] != "catalog_item" or r["status"] != "partial" or r.get("candidate_name") != r["unregistered"]:
                bad_self.append(f"{r['name']}: 미등록 있는데 what={r['what_kind']}/{r['status']}/cand={r.get('candidate_name')}")
        if r["what_kind"] == "catalog_item":
            t = next(t for t in TUP["procedure"]["tuples"] if t["id"] == r["procedure_id"])
            if t["what_id"] != mkid("CAT", f"{r['family']}|{r['name']}") or t.get("candidate_name") != r["unregistered"] or t["anchor"] != t["what_id"]:
                bad_self.append(f"{r['name']}: CAT id/candidate_name/anchor 불일치")
    n_self = sum(1 for r in cat if r.get("what_kind") == "catalog_item")
    line(not bad_self, f"미등록 조각 있는 항목 {sum(1 for r in cat if r.get('unregistered'))} 전부 what=항목 자신(CAT- id · partial · candidate_name = 미등록 조각 · anchor = CAT-) — 위반 {len(bad_self)}" + (": " + "; ".join(bad_self[:5]) if bad_self else "") + f" · 항목 자신 what {n_self} (사유 {ps['catalog_self_by_reason']})")
    self_ids = {t["id"] for t in TUP["procedure"]["tuples"] if t["what_kind"] == "catalog_item"}
    multi = [f for f in TUP["procedure"]["folded"] if f["procedure_id"] in self_ids and f["n_items"] >= 2]
    line(not multi, f"항목 자신(CAT-) what 튜플 {len(self_ids)} 은 전부 항목 1개(접힘 0) — 위반 {len(multi)}")
    ref_rows = [r for v in TUP["procedure"]["references"].values() for r in v] + TUP["procedure"]["market_pricing"]
    bad_ref = [r["label"] for r in ref_rows if (bool(r.get("unregistered")) != (r.get("unresolved_reason") == "unregistered")) or (r["result"] == "unresolved" and (r.get("procedure_id") or r.get("member_ids"))) or (r["result"] in ("tuple", "combo_ref") and r.get("status") != "complete")]
    n_unres = sum(1 for r in ref_rows if r["result"] == "unresolved")
    line(not bad_ref and ps["reference_total"]["partial"] == 0 and ps["market_pricing"]["partial"] == 0, f"참조 ②③ {len(ref_rows)}: 미등록 조각 있음 ⇔ 미해결(unregistered) · 미해결은 튜플 없음 · 위반 {len(bad_ref)} · partial 튜플 0 · 미해결 ② {ps['reference_total']['unresolved']} + ③ {ps['market_pricing']['unresolved']} = {n_unres} (사유 ② {ps['reference_total']['unresolved_by_reason']} · ③ {ps['market_pricing']['unresolved_by_reason']})")
    ref_tids = {x for r in ref_rows for x in ([r.get("procedure_id")] if r["result"] == "tuple" else r.get("member_ids", [])) if x}
    TT = {t["id"]: t for t in TUP["procedure"]["tuples"]}
    bad_part = [x for x in ref_tids if TT[x]["status"] != "complete" and TT[x]["what_kind"] != "catalog_item"]
    line(not bad_part, f"참조가 닿은 튜플 {len(ref_tids)} 중 partial·ambiguous 인 것은 항목 자신(CAT-) 튜플뿐 (사전 값 what 인데 아닌 것 {len(bad_part)})")
    ud = []
    for k, v in ps["reference_slots"].items():
        w = OUT.get(k)
        if w is not None and w["unresolved"] != v["unresolved_by_reason"].get("unregistered", 0):
            ud.append(f"{k}: 분해 규칙 {w['unresolved']} vs 튜플(unregistered) {v['unresolved_by_reason'].get('unregistered', 0)}")
    mk_key = next((k for k in OUT if k.startswith("market-pricing")), None)
    if mk_key and OUT[mk_key]["unresolved"] != ps["market_pricing"]["unresolved_by_reason"].get("unregistered", 0):
        ud.append(f"{mk_key}: 분해 규칙 {OUT[mk_key]['unresolved']} vs 튜플 {ps['market_pricing']['unresolved_by_reason'].get('unregistered', 0)}")
    line(not ud, f"미해결(사유 unregistered) 수 = v1.1 분해 규칙(§9.2) 미해결 수 — 자리별 불일치 {len(ud)} (v2.2 는 그 위에 multi_*/unusable 미해결이 더해진다)" + (": " + "; ".join(ud[:6]) if ud else ""))
    d21 = {d["name"]: d for d in V21["dic"]["dictionaries"]}
    d1 = {d["name"]: d for d in dic["dictionaries"]}
    same_dic = set(d1) == set(d21) and all([(e["canonical"], tuple(s_["value"] for s_ in e["synonyms"])) for e in d1[n]["entries"]] == [(e["canonical"], tuple(s_["value"] for s_ in e["synonyms"])) for e in d21[n]["entries"]] for n in d1 if n != "course")
    c21 = {e["canonical"]: [s_["value"] for s_ in e["synonyms"]] for e in d21["course"]["entries"]}
    c22 = {e["canonical"]: [s_["value"] for s_ in e["synonyms"]] for e in d1["course"]["entries"]}
    dropped = sorted({(k, x) for k, v in c21.items() for x in v} - {(k, x) for k, v in c22.items() for x in v})
    line(same_dic and list(c21) == list(c22) and not ({(k, x) for k, v in c22.items() for x in v} - {(k, x) for k, v in c21.items() for x in v}), f"사전 {len(d1)}: course 밖 45 개는 값·동의어·순서 = v2.1 · course 정준값 5 동일 · 추가 동의어 0 · 뺀 동의어 {dropped} (수정 6 · J-7)")
    line(len(erd["entities"]) == len(V21["erd"]["entities"]) == 21 and len(erd["relations"]) == len(V21["erd"]["relations"]) == 31 and [e["key"] for e in erd["entities"]] == [e["key"] for e in V21["erd"]["entities"]] and [r["id"] for r in erd["relations"]] == [r["id"] for r in V21["erd"]["relations"]], f"구조 = v2.1 (개체 {len(erd['entities'])} · 관계 {len(erd['relations'])} · 같은 키·순서)")
    pe = next(e for e in erd["entities"] if e["key"] == "procedure")
    r27 = next(r for r in erd["relations"] if r["id"] == "R27")
    line("catalog_item" in erd["enums"]["procedure.what_kind"] and any(a["name"] == "candidate_name" for a in pe["attrs"]) and "catalog_item" in r27["to"], f"procedure.what_kind = {erd['enums']['procedure.what_kind']} · candidate_name 속성 · R27 → {r27['to']}")
    line(ps["catalog_distinct_tuples"] == len(TUP["procedure"]["folded"]) and sum(f["n_items"] for f in TUP["procedure"]["folded"]) == 521, f"521 → {ps['catalog_distinct_tuples']} (v2.1 {V21['tup']['procedure']['summary']['catalog_distinct_tuples']} · v2 {V2['tup']['procedure']['summary']['catalog_distinct_tuples']}) · 접힌 표 항목 합 521")
    adv_same = {t["id"] for t in TUP["adverse"]["tuples"]} == {t["id"] for t in V21["tup"]["adverse"]["tuples"]} and as_["complications_distinct_tuples"] == V21["tup"]["adverse"]["summary"]["complications_distinct_tuples"] and json.dumps(as_["expressions"], sort_keys=True) == json.dumps(V21["tup"]["adverse"]["summary"]["expressions"], sort_keys=True)
    line(adv_same, f"부작용 튜플 = v2.1 과 동일 (튜플 id 집합 · 65 → {as_['complications_distinct_tuples']} · 표현 연결 수) — 수정 6 은 값이 바뀌지 않는다")
    note(f"부작용 접힘(검토 2-C·2-D · v2.2 범위 밖): 둘 이상 이름이 접힌 부작용 튜플 {as_['folded_with_2plus_names']} 중 미등록 조각 있는 이름이 섞인 튜플 {as_['folded_with_partial_name']} — 손대지 않았다(§12)")
    out.append("")

    # ---- J (v2.2)
    out.append("### J. v2.2 수정 6건 (발주서 erd-v2.2-brief.md)")
    out.append("")
    # J-1 미상 포함 튜플 접힘 0
    T = TUP["procedure"]["tuples"]
    bad_anchor = []
    for t in T:
        anchors = {s_["anchor"] for s_ in t["sources"]}
        texts = {norm(s_["matched_text"]) for s_ in t["sources"]}
        if not t["all_dict_values"] and (len(anchors) != 1 or anchors != {t["anchor"]} or len(texts) != 1):
            bad_anchor.append(t["id"])
    none_fold_cat = [f for f in TUP["procedure"]["folded"] if f["n_items"] >= 2 and not f["all_dict_values"]]
    line(not bad_anchor and not none_fold_cat, f"J-1 미상 포함 튜플 접힘 0 — 미상 칸(site/technique none)이 있거나 what=CAT- 인 튜플 {sum(1 for t in T if not t['all_dict_values'])} 전부 anchor 하나 · 정규화 라벨 하나(같은 라벨 = ① 만 같은 튜플) · 위반 {len(bad_anchor)} · 미상 포함 분류 항목 접힘 {len(none_fold_cat)} · 세 칸 전부 사전 값 튜플 {sum(1 for t in T if t['all_dict_values'])}")
    fc = erd.get("fold_condition")
    md = V2["md"]
    line(fc == "세 칸 전부 사전 값일 때만" and tr.get("fold_condition") == fc and fc in tr.get("fold_rule", "") and fc in erd["id_rule"]["procedure"] and (not md or md.count(fc) >= 3), f"J-1 접힘 조건 문자 그대로 「{fc}」 — json fold_condition · tuple_rules.procedure.fold_condition/fold_rule · id_rule.procedure" + (f" · md {md.count(fc)} 곳" if md else " · md 는 빌드 후"))
    sp = TUP["procedure"].get("v21_none_fold_split") or tuples_mod.v21_split(TUP, V21["tup"])
    v21_three = [f for f in V21["tup"]["procedure"]["folded"] if f["n_items"] >= 2]
    sp_cat = [x for x in sp if any(d["origin"] == "catalog_item" for d in x["dest"]) and sum(1 for d in x["dest"] if d["origin"] == "catalog_item") >= 2]
    line(sp and all(x["split"] for x in sp) and len(sp_cat) == len(v21_three) == 3, f"J-1 v2.1 의 미상 칸 있는데 라벨이 합쳐진 튜플 {len(sp)} (§9.5.2 분류 항목 3 + 참조) → v2.2 전부 갈라짐 {sum(1 for x in sp if x['split'])}/{len(sp)} · 분류 항목 접힘 3 → {ps['catalog_tuples_with_2plus_items']}")
    # J-2 버린 조각 0
    bad_drop = []
    for r in cat:
        if r.get("extra_primaries") is None or r.get("extra_sites") is None:
            bad_drop.append(f"{r['name']}: extra null")
            continue
        f = r["fragments"]
        if r["what_kind"] in DK:
            nonfam = [x for x in f["primaries"] if x not in r.get("family_fragments", [])]
            if r["extra_primaries"] or r["extra_sites"] or len(set(f["sites"])) > 1 or len(set(f["techniques"])) > 1 or len(nonfam) > 1:
                bad_drop.append(f"{r['name']}: 사전 값 what 인데 조각 둘 이상/extra 있음")
        else:
            placed = [r["site"]] if r.get("site") else []
            if sorted(set(f["sites"])) != sorted(set(placed + r["extra_sites"])) or sorted(f["primaries"]) != sorted(r["extra_primaries"]):
                bad_drop.append(f"{r['name']}: 항목 자신인데 조각 일부만 extra")
    for r in ref_rows:
        if r["result"] == "tuple" and r.get("what_basis") not in ("modality_code", "subcategory_id"):
            f = r["fragments"]
            nonfam = [x for x in f["primaries"] if x not in r.get("family_fragments", [])]
            if r.get("extra_primaries") != [] or r.get("extra_sites") != [] or len(set(f["sites"])) > 1 or len(set(f["techniques"])) > 1 or len(nonfam) > 1:
                bad_drop.append(f"ref {r['label']}: 튜플인데 조각 둘 이상/extra 있음")
        if r["result"] == "unresolved" and (r.get("extra_primaries") is None or r.get("extra_sites") is None or r["extra_sites"] != r["fragments"]["sites"]):
            bad_drop.append(f"ref {r['label']}: 미해결인데 extra 실값 아님")
    t_extra_null = [t["id"] for t in T if "extra_sites" in t and t["extra_sites"] is None]
    cases = {}
    for r in ref_rows:
        if r["label"] in ("IPL 제모", "사각턱 (수입)", "사각턱 (국산)", "필러 볼/턱", "보톡스(턱선/광대)"):
            cases[r["label"]] = r["result"] + ":" + str(r.get("unresolved_reason"))
    v21rule8 = "primary 가 여럿이고 조합이 아니면 각 조각의 최종 what 종류로 product > modality_subcategory > modality 순"
    rule8_gone = not any(v21rule8 in w for w in tr["what"])
    line(not bad_drop and not t_extra_null and rule8_gone and cases and all(v_.startswith("unresolved") for v_ in cases.values()), f"J-2 버린 조각 0 — 분류 항목 521 · 참조 {len(ref_rows)} 의 extra_primaries/extra_sites 전부 실값(null 0) · 사전 값 what 인데 primary/site/technique 둘 이상 0 · 항목 자신 튜플은 조각 전부 extra 에 · 위반 {len(bad_drop)}" + (": " + "; ".join(bad_drop[:4]) if bad_drop else "") + f" · v2.1 규칙 8 삭제 {rule8_gone} · 검토 사례 {cases}")
    # J-3 상속 기법 0
    inh = sum(1 for t in T if t["technique_origin"] == "inherited") + sum(1 for r in cat if r.get("technique_origin") == "inherited")
    single = sorted(f for f, v in tech_fam.items() if len(set(v)) == 1)
    cand = TUP["procedure"]["inheritance_candidates"]
    line(inh == 0 and ps["technique_inherited"] == 0 and "inherited" not in erd["enums"]["procedure.technique_origin"] and tr.get("technique_inheritance") is False and sorted(c["from_ref"][3:] for c in cand) == single and all(c["kind"] == "canonical_mapping" for c in cand),
         f"J-3 상속 기법 0 (v2.1 inherited {V21['tup']['procedure']['summary']['tuples_technique_origin'].get('inherited')}) · enum procedure.technique_origin={erd['enums']['procedure.technique_origin']} · tuple_rules.technique_inheritance=false · canonical_mapping 후보 {len(cand)} 계열 = R5 단일 기법 계열 {single}")
    # J-4 ④
    q4 = next(q for q in erd["quality_rules"] if q["no"] == "④")["rule"]
    ce = next(e for e in erd["entities"] if e["key"] == "conflict")
    ca = {a["name"]: a for a in ce["attrs"]}
    line(all(k in q4 for k in ("auto_resolved_by_trust", "chosen_value", "trust_tier", "rule_ref=④", "conflict_override", "채택마다 conflict 레코드")) and "auto_resolved_by_trust" in erd["enums"]["conflict.status"] and "④" in erd["enums"]["conflict.rule_ref"]
         and {"rule_ref", "chosen_value"} <= set(ca) and "trust_tier" in ca["values"]["type"] and "auto_resolved_by_trust" in ca["status"]["type"] and "conflict_override" in erd["enums"]["decision.kind"],
         f"J-4 ④ 유지 + 기록 — 품질 규칙 ④ 에 「채택마다 conflict 레코드」(status=auto_resolved_by_trust · chosen_value · values[].trust_tier · rule_ref=④ · 뒤집기 conflict_override) · conflict.status={erd['enums']['conflict.status']} · conflict 속성 rule_ref·chosen_value · §9.3 rule_ref 열 {all(c.get('rule_ref') for c in erd['conflict_estimates'])}")
    # J-5 decision kind 7 + 공통 필드
    need = ["dictionary_add", "tuple_assign", "fold_approve", "event_split", "canonical_mapping", "conflict_override", "exclude"]
    dk = {k["kind"]: k for k in erd["decision_kinds"]}
    de = next(e for e in erd["entities"] if e["key"] == "decision")
    common = ["id", "kind", "target", "new_value", "reason", "decided_by", "decided_at", "status", "source_refs"]
    shape = {"dictionary_add": ["dictionary", "canonical", "synonyms", "category"], "tuple_assign": ["catalog_item_id", "ref_id", "what_kind", "what_id", "site_id", "technique_id"], "fold_approve": ["procedure_ids", "keep_id"],
             "event_split": ["event", "new_events"], "canonical_mapping": ["from_ref", "to_id", "scope"], "conflict_override": ["conflict_id", "chosen_value"], "exclude": ["id"]}
    bad_shape = [k for k in need if k not in dk or not dk[k]["build_reads"] or not all(x in (dk[k]["target"] + dk[k]["new_value"]) for x in shape[k])]
    bad_rec = [d["id"] for d in erd["decisions"] if list(d.keys()) != common or not isinstance(d["target"], dict) or not isinstance(d["new_value"], dict) or d["status"] not in ("proposed", "approved", "rejected") or d["kind"] not in erd["enums"]["decision.kind"]
               or (d["status"] == "proposed" and (d["decided_by"] is not None or d["decided_at"] is not None)) or (d["status"] == "approved" and not d["decided_by"]) or not d["source_refs"]]
    line(set(need) <= set(erd["enums"]["decision.kind"]) and not bad_shape and [a["name"] for a in de["attrs"]] == common and erd["enums"]["decision.status"] == ["proposed", "approved", "rejected"] and "approved" in erd["decision_build_rule"] and not bad_rec,
         f"J-5 decision kind 7 {need} 전부 enum·표(target/new_value 구조체 필드)·build_reads · kind 총 {len(erd['enums']['decision.kind'])} · 개체 속성 = 공통 필드 {len(common)} · 「{erd['decision_build_rule'][:40]}…」 · 레코드 모양 위반 {len(bad_rec)}" + (f": {bad_rec[:4]}" if bad_rec else "") + f" · 형태 위반 {bad_shape}")
    # J-6 이관 22
    old = {d["id"]: d for d in V21["erd"]["decisions"]}
    new = {d["id"]: d for d in erd["decisions"]}
    mig = erd.get("decisions_migration", [])
    bad_mig = [i_ for i_ in old if i_ not in new or new[i_]["kind"] != old[i_]["kind"]]
    prop = sorted(i_[-2:] for i_ in old if new.get(i_, {}).get("status") == "proposed")
    appr = sum(1 for i_ in old if new.get(i_, {}).get("status") == "approved")
    line(len(old) == 22 and not bad_mig and len(mig) == 22 and prop == ["20", "21", "22"] and appr == 19 and all(new[f"DEC-2026-11-04-{n}"]["decided_by"] is None for n in ("20", "21", "22")),
         f"J-6 기존 결정 {len(old)} 전부 이관(id·kind 유지 · 누락/변경 {len(bad_mig)}) · 이관 표 {len(mig)} · approved {appr}(처분 19) · proposed {prop}(검토 3-E: decided_by·decided_at null) · 신규 {sorted(set(new) - set(old))}")
    # J-7 course 문장 3곳
    cr = erd.get("course_rule")
    adv = next(e for e in erd["entities"] if e["key"] == "adverse_effect")
    ac = next(a for a in adv["attrs"] if a["name"] == "course")
    dc = d1["course"]
    secs = {}
    if md:
        for key, head in (("§1.5", "### 1.5 "), ("§2.14", "### 2.14 "), ("§4", "## 4. ")):
            a0 = md.find(head)
            b0 = md.find("\n## ", a0 + 5) if head.startswith("## ") else md.find("\n### ", a0 + 5)
            secs[key] = cr in md[a0:b0] if a0 >= 0 else False
    bad_src = [s_ for e in dc["entries"] for s_ in e["sources"] + [x for sy in e["synonyms"] for x in sy["sources"]] if s_["path"].endswith(".duration") or s_["path"].endswith(".incidence")]
    line(cr and erd["tuple_rules"]["adverse"].get("course") == cr and ac["rule"] == cr and dc["note"] == cr and not any(x.endswith(".duration") or x.endswith(".incidence") for x in ac["sources"]) and not bad_src and (not md or all(secs.values())),
         f"J-7 course 출처 문장 3곳 동일 — tuple_rules.adverse.course(§1.5) · adverse_effect.course 규칙(§2.14) · 경과 사전 비고(§4) = 같은 문자열 · md 절별 {secs or '빌드 후'} · course 속성·사전 출처에 duration/incidence 0 (사전 출처 위반 {len(bad_src)})")
    out.append("")
    out.append(f"**종합: {'PASS' if ok_all else 'FAIL'}** (NOTE {len(notes)}) — 잎 키 {len(rows)}/{n_ledger + n_s1} 행선지 확정(미정 0 · v2.1 대비 이동 {len(moves22)}) · 사전 값 출처 100% · ERD 출처 키 100% · 브론즈 sha256 22 일치 · 분해 규칙 재현 일치(v1.1 과 동일) · 튜플 실측 재현 일치 · 구조 v2.1 그대로 · v2.2: 미상 포함 접힘 0 · 버린 조각 0 · 상속 0 · ④ 기록 규칙 · decision kind 7 + 공통 필드 · 이관 22 · course 문장 3곳" + (" · NOTE: " + " / ".join(notes) if notes else ""))
    return ok_all, "\n".join(out)


if __name__ == "__main__":
    ok, rep = run_checks()
    print(rep)
    sys.exit(0 if ok else 1)
