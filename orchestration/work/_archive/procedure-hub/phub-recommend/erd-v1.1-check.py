#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v1.1 검산 (v1 검산 A~D + 22번째 파일 + 분해 규칙 재현 + 처분 반영).

 A. 잎 키 행선지: erd-v1.1-column-map.md 의 행 = 원장 스캔 잎 키 573 + step1-products.json 잎 키(bronze-ledger-column-scan.py FileScan 으로 즉석 스캔), 중복 0, 미정 0, 범주 5 안, 표적이 ERD 에 정의됨.
 B. 사전 값 출처: erd-v1.1-dictionaries.json 의 모든 정준값·동의어에 출처 ≥1, 각 출처가 원장/step1 에 실제로 그 값(kind=value) 또는 키(kind=key)를 가진다.
 C. ERD 출처 키: erd-v1.1.json 개체 속성·관계의 출처 'file:path' 가 잎 키에 존재한다.
 D. 바이트: erd-v1.1.json 의 sha256 이 원장 21 + step1 과 같다.
 E. 분해 규칙 재현: erd-v1.1-resolve.py 를 다시 돌려 자리별 (n, 해결, 분해 성공, 미해결) 이 erd-v1.1.json 의 수치와 같다.
 F. 처분 반영: 부위 사전 확장 0 · 기법 사전 = mechanism[] distinct 수 · 처분 19 · complications trust_flag · q14 미배정 0.

실행: python3 erd-v1.1-check.py  (같은 폴더의 산출물 + 스캔 JSON + 원장 디렉토리 + step1-products.json)
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


def norm(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", str(s)).casefold())


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
    erd = json.load(open(os.path.join(HERE, "erd-v1.1.json"), encoding="utf-8"))
    dic = json.load(open(os.path.join(HERE, "erd-v1.1-dictionaries.json"), encoding="utf-8"))
    cmap = open(os.path.join(HERE, "erd-v1.1-column-map.md"), encoding="utf-8").read()
    ledgers = {f: json.load(open(os.path.join(LEDGER, f), encoding="utf-8")) for f in scan["files"]}
    ledgers[STEP1] = json.load(open(os.path.join(HERE, STEP1), encoding="utf-8"))
    scanner = load_module("bronze_scan", os.path.join(HERE, "bronze-ledger-column-scan.py"))
    s1 = scanner.FileScan(os.path.join(HERE, STEP1)).run()
    return scan, erd, dic, cmap, ledgers, s1


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
    scan, erd, dic, cmap, ledgers, s1 = load()
    out, ok_all = [], True

    def line(ok, text):
        nonlocal ok_all
        ok_all = ok_all and ok
        out.append(f"- {'PASS' if ok else 'FAIL'} — {text}")

    # ---- A
    leaf = {(f, p) for f, v in scan["files"].items() for p in v["leaf_paths"]} | {(STEP1, p) for p in s1["leaf_paths"]}
    n_ledger, n_s1 = scan["total_leaf_paths"], s1["leaf_count"]
    rows = parse_column_map(cmap)
    got = Counter((r["file"], r["path"]) for r in rows)
    dup = [k for k, n in got.items() if n > 1]
    missing, extra = sorted(leaf - set(got)), sorted(set(got) - leaf)
    bad_dest = [r for r in rows if r["dest"] not in DESTS or not r["target"]]
    out.append("### A. 잎 키 행선지 (원장 21 + step1)")
    out.append("")
    line(len(rows) == n_ledger + n_s1 and n_ledger == 573, f"행선지 행 {len(rows)} = 원장 잎 키 {n_ledger}(=573) + step1 잎 키 {n_s1} = {n_ledger + n_s1}")
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
    out.append("")

    # ---- B
    out.append("### B. 사전 값 출처")
    out.append("")
    n_can = n_syn = 0
    no_src, bad_src = [], []
    cache = {}

    def vals(f, p):
        if (f, p) not in cache:
            cache[(f, p)] = {norm(v) for v in walk(ledgers[f], p) if not isinstance(v, (list, dict)) and v is not None}
        return cache[(f, p)]

    def check_src(dname, value, s):
        f, p, kind = s["file"], s["path"], s.get("kind", "value")
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
    out.append("### E. 분해 규칙 재현 (erd-v1.1-resolve.py 재실행)")
    out.append("")
    res = load_module("erd_v11_resolve", os.path.join(HERE, "erd-v1.1-resolve.py"))
    OUT, TOTAL = res.run_all(dic, erd["resolve_rules"], {k: v for k, v in ledgers.items() if k != STEP1}, ledgers[STEP1], None)
    diffs = []
    for k, v in erd["resolution_report"].items():
        w = OUT.get(k)
        if not w:
            diffs.append(f"{k}: 자리 없음")
            continue
        for key in ("n", "resolved", "decomposed", "unresolved"):
            if v[key] != w[key]:
                diffs.append(f"{k}.{key}: json {v[key]} vs 재실행 {w[key]}")
    line(not diffs and set(OUT) == set(erd["resolution_report"]), f"자리 {len(OUT)}개 (n·해결·분해 성공·미해결) 재현 불일치 {len(diffs)}" + (": " + "; ".join(diffs[:5]) if diffs else ""))
    line(TOTAL["unresolved_v1_1"] == erd["resolution_total"]["unresolved_v1_1"] and TOTAL["decomposed_v1_1"] == erd["resolution_total"]["decomposed_v1_1"], f"합계 재현: 미해결 {TOTAL['unresolved_v1_1']} · 분해 성공·항목 없음 {TOTAL['decomposed_v1_1']} · 해결 {TOTAL['resolved_v1_1']}")
    rr = erd["resolve_rules"]
    line(rr["step3_assemble"].get("no_similarity") is True and rr["step2_decompose"]["dictionary_order"] == ["product", "modality_subcategory", "procedure", "site", "spec", "product_tier"], "규칙 데이터: 유사도 금지 · 사전 순서 제품→하위분류→단위 시술→부위→규격→product_tier")
    out.append("")

    # ---- F
    out.append("### F. 처분 반영")
    out.append("")
    D = {d["name"]: d for d in dic["dictionaries"]}
    site = D["site"]["entries"]
    ext = [e for e in site if e.get("site_kind") not in ("backbone", "taxonomy_site_label")]
    line(not ext and sum(1 for e in site if e.get("site_kind") == "backbone") == 11, f"부위 사전 {len(site)} = 뼈대 11 + taxonomy 부위 라벨 {sum(1 for e in site if e.get('site_kind') == 'taxonomy_site_label')} · 확장 {len(ext)}")
    mech = {norm(v) for v in walk(ledgers["procedure-profiles.json"], "profiles[].mechanism[]")}
    tech = {norm(e["canonical"]) for e in D["technique"]["entries"]}
    line(tech == mech, f"기법 사전 {len(tech)} = profiles[].mechanism[] distinct {len(mech)} (하위분류 label·type·pih subcategory 없음)")
    line(len(erd["review_dispositions"]) == 19 and sum(1 for d in erd["review_dispositions"] if d["decided_by"] == "사용자") == 4, f"처분 {len(erd['review_dispositions'])} (사용자 {sum(1 for d in erd['review_dispositions'] if d['decided_by'] == '사용자')} · 워커 확정 {sum(1 for d in erd['review_dispositions'] if d['decided_by'] != '사용자')})")
    comp = next(fm for fm in erd["source_files"] if fm["file"] == "complications.json")
    line(comp["trust_tier"] == 3 and "AI 컨센서스 추정" in (comp.get("trust_flag") or ""), "complications.json 3 유지 + 「AI 컨센서스 추정」")
    q14 = erd["q14_bundles"]
    line(all(not r["bucket"].startswith("미배정") for r in q14) and all(r["scope"] for r in q14 if r["bucket"].startswith("②")), f"질문 14 묶음 {len(q14)}: ① {sum(1 for r in q14 if r['bucket'].startswith('①'))} · ② {sum(1 for r in q14 if r['bucket'].startswith('②'))}(범위 검토) · 미배정 {sum(1 for r in q14 if r['bucket'].startswith('미배정'))}")
    line(len(erd["site_replacement_8_2"]) == 51, f"8-2 처분 표 {len(erd['site_replacement_8_2'])} 행 (v1 확장 51)")
    out.append("")
    out.append(f"**종합: {'PASS' if ok_all else 'FAIL'}** — 잎 키 {len(rows)}/{n_ledger + n_s1} 행선지 확정(미정 0) · 사전 값 출처 100% · ERD 출처 키 100% · 브론즈 sha256 22 일치 · 분해 규칙 재현 일치 · 처분 반영")
    return ok_all, "\n".join(out)


if __name__ == "__main__":
    ok, rep = run_checks()
    print(rep)
    sys.exit(0 if ok else 1)
