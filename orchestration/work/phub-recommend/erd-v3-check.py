#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v3 검산 (v2.4 검산 A~L 전부 유지 — v3 에서 바뀐 기대값은 항목 안에 · + M v3 변경 10건 + 브론즈 2판 해시 + 행선지 전수(2판 잎 키 = 1판) + 「사용자 정의 3 과 명시 예외 유지」). 파일은 erd-v3.* 를 읽고 v2.4·v2.3·v2.2·v2.1·v2 산출물·브론즈 2판과 대조한다.
 원장 = bronze/phub-ledger(2판 · HASHES.txt). 잎 키 스캔(bronze-ledger-column-scan.json)은 1판 것 — 2판을 다시 스캔해 집합이 같은지 본다(A).

 A. 잎 키 행선지: erd-v2-column-map.md 의 행 = 원장 스캔 잎 키 573 + step1-products.json 잎 키 499 = 1,072, 중복 0, 미정 0, 범주 5 안, 표적이 ERD 에 정의됨. 이동 표 = v1.1 표와 표적이 다른 행 전부.
 B. 사전 값 출처: erd-v2-dictionaries.json 의 모든 정준값·동의어에 출처 ≥1, 각 출처가 원장/step1 에 실제로 그 값(value)·키(key)·부분 문자열(derived)을 가진다. default 는 course 「미상」 하나만.
 C. ERD 출처 키: erd-v2.json 개체 속성·관계의 출처 'file:path' 가 잎 키에 존재한다.
 D. 바이트: erd-v2.json 의 sha256 이 원장 21 + step1 과 같다.
 E. 분해 규칙 재현: erd-v1.1-resolve.py 를 v2 사전으로 다시 돌려 자리별 (n, 해결, 분해 성공, 미해결) 이 erd-v2.json 및 erd-v1.1.json 의 수치와 같다.
 F. 처분 반영: 부위 사전 21(확장 0) · 기법 사전 = mechanism[] distinct 12 · 처분 19 · complications trust_flag · q14 미배정 0 · 8-2 표 51.
 G. 튜플 실측 재현: erd-v2-tuples.py 를 다시 돌려 요약 수치가 erd-v2.json(tuple_report)·erd-v2-tuples.json 과 같다. 튜플 id = 식별자 규칙(sha256(what|site|technique) / sha256(event|site|course)) 재계산 일치. 분류 항목 521 전부 튜플 있음. 접힌 표 항목 합 = 521. complications 65 전부 표에 있음.
 I. v2.1 접힘 규칙: fallback_to_parent=false(규칙 데이터) · 부모 하위분류 fallback 0 · 접힌 튜플(항목 ≥2)은 세 칸 전부 사전 값·미등록 0 · partial 항목이 섞인 접힌 튜플 0(둘 이상 0 포함) · 미등록 조각 있는 항목은 what=항목 자신(CAT- id · candidate_name = 미등록 조각) · 참조 ②③ partial 0 · 미등록 조각 있는 참조 = 미해결(튜플 없음) · ② 미해결 수 = v1.1 분해 규칙 미해결 수 · 행선지 표·사전 값이 v2 와 동일 · 개체/관계/사전 수 v2 와 같음 · 부작용 접힘 확인(발주서 전제 검증 · NOTE).
 J. v2.2: 미상 포함 튜플 접힘 0 · 버린 조각 0(extra_* 실값) · 상속 기법 0 · ④ 자동 해결마다 conflict 레코드 규칙 명시 · decision kind 7 + 공통 필드 · 기존 결정 이관(v2.3: 23) · course 출처 문장 3곳 동일.
 K. v2.3: 엣지 끝 분포 실측 존재 · 파생 id(PRC-/ADV-/CFL-)를 target 으로 쓰는 결정 0 · 적용 순서 표 존재(①~⑦) · 결정 kind 16(12+4) · 부작용 미등록 포함 접힘 0(raw_name) · course 규칙 문장(사건에 바로 붙은 수식어만 · LOP 둘) · 기법 잔재 표현 0 · R29 출처 taxonomy safety 11 키.
 M. v3: V3-1 수식 칸(사전·식별자·접힘·exact 불변 실측) · V3-2 회사 괄호(규칙 데이터·후보 전수) · V3-3 stopwords(단어마다 locator·전후) · V3-4 조합 기호(`+`/`/` 전수 · 부위 여럿 · member_mode) · V3-5 부위 kind(layer 5 출처) · V3-6 canonical_rename(kind 17 · 적용 ①) · V3-7 description/media_refs · V3-8 R5 하위분류 · V3-9 anchor 확장 문구 · V3-10 ⑦ 닫음 문구 · 사전 값 변경 셋뿐 · 사용자 정의 3 + 명시 예외 문장 · 2판 해시·잎 키.
 L. v2.4: 부위 상속 0(멤버 밖에서 온 site 0 · 부위 나열·후보 분할·보존 전수) · raw_name course/site 미상 100% · 표현 유래 새 튜플 0 · partial 표현 연결 0 · 틀린 조합 실례(두통×주사 부위) 0 · §5.2/§1.4/§2.3/§2.4/§2.5/§2.14 문구 존재 · 사전 값 불변 · 개체·관계 불변 · 원칙 A~D 문장.
 H. 구조 변경 반영: 개체 21(catalog_item·adverse_expression) · 관계 31(R26~R31) · 사전 46(adverse_event_type·course·relative_site · procedure_name 없음) · target_depth 에 catalog_item · package.kind 에 combo_ref · 사건 사전 값마다 category 7 중 하나 · v1.1 procedure 속성이 catalog_item 에 전부 있음 · 이동 표 행 수 = 실제 달라진 행 수.

실행: python3 erd-v3-check.py  (같은 폴더의 산출물 + 스캔 JSON + 원장 디렉토리 + step1-products.json)
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
LEDGER = os.path.join(HERE, "bronze", "phub-ledger")   # 브론즈 2판(원장의 집)
LEDGER_V1 = "/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26"
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
    erd = json.load(open(os.path.join(HERE, "erd-v3.json"), encoding="utf-8"))
    dic = json.load(open(os.path.join(HERE, "erd-v3-dictionaries.json"), encoding="utf-8"))
    cmap = open(os.path.join(HERE, "erd-v3-column-map.md"), encoding="utf-8").read()
    V2 = {"erd": json.load(open(os.path.join(HERE, "erd-v2.json"), encoding="utf-8")), "dic": json.load(open(os.path.join(HERE, "erd-v2-dictionaries.json"), encoding="utf-8")),
          "cmap": open(os.path.join(HERE, "erd-v2-column-map.md"), encoding="utf-8").read(), "tup": json.load(open(os.path.join(HERE, "erd-v2-tuples.json"), encoding="utf-8"))}
    V2["v21"] = {"erd": json.load(open(os.path.join(HERE, "erd-v2.1.json"), encoding="utf-8")), "dic": json.load(open(os.path.join(HERE, "erd-v2.1-dictionaries.json"), encoding="utf-8")),
                 "cmap": open(os.path.join(HERE, "erd-v2.1-column-map.md"), encoding="utf-8").read(), "tup": json.load(open(os.path.join(HERE, "erd-v2.1-tuples.json"), encoding="utf-8"))}
    V2["v22"] = {"erd": json.load(open(os.path.join(HERE, "erd-v2.2.json"), encoding="utf-8")), "dic": json.load(open(os.path.join(HERE, "erd-v2.2-dictionaries.json"), encoding="utf-8")),
                 "cmap": open(os.path.join(HERE, "erd-v2.2-column-map.md"), encoding="utf-8").read(), "tup": json.load(open(os.path.join(HERE, "erd-v2.2-tuples.json"), encoding="utf-8"))}
    V2["v23"] = {"erd": json.load(open(os.path.join(HERE, "erd-v2.3.json"), encoding="utf-8")), "dic": json.load(open(os.path.join(HERE, "erd-v2.3-dictionaries.json"), encoding="utf-8")),
                 "cmap": open(os.path.join(HERE, "erd-v2.3-column-map.md"), encoding="utf-8").read(), "tup": json.load(open(os.path.join(HERE, "erd-v2.3-tuples.json"), encoding="utf-8"))}
    V2["v24"] = {"erd": json.load(open(os.path.join(HERE, "erd-v2.4.json"), encoding="utf-8")), "dic": json.load(open(os.path.join(HERE, "erd-v2.4-dictionaries.json"), encoding="utf-8")),
                 "cmap": open(os.path.join(HERE, "erd-v2.4-column-map.md"), encoding="utf-8").read(), "tup": json.load(open(os.path.join(HERE, "erd-v2.4-tuples.json"), encoding="utf-8"))}
    V2["md"] = open(os.path.join(HERE, "erd-v3.md"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, "erd-v3.md")) else ""
    cmap11 = open(os.path.join(HERE, "erd-v1.1-column-map.md"), encoding="utf-8").read()
    erd11 = json.load(open(os.path.join(HERE, "erd-v1.1.json"), encoding="utf-8"))
    tup = json.load(open(os.path.join(HERE, "erd-v3-tuples.json"), encoding="utf-8"))
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
    moves23 = erd.get("column_map_moves_v2_3", [])
    moves24 = erd.get("column_map_moves_v2_4", [])
    mv = {(m["file"], m["path"]) for m in moves} | {(m["file"], m["path"]) for m in moves22} | {(m["file"], m["path"]) for m in moves23} | {(m["file"], m["path"]) for m in moves24}
    line(len(changed) == len(mv) and {(c[0], c[1]) for c in changed} == mv, f"이동 표 v1.1→v2 {len(moves)} + v2.1→v2.2 {len(moves22)} + v2.2→v2.3 {len(moves23)} + v2.3→v2.4 {len(moves24)} + v2.4→v3 {len(erd.get('column_map_moves_v3', []))} = v1.1 표와 표적이 다른 행 {len(changed)} (같은 집합)")
    moves3 = erd.get("column_map_moves_v3", [])
    mv |= {(m["file"], m["path"]) for m in moves3}
    rows24 = parse_column_map(V2["v24"]["cmap"])
    m24 = {(r["file"], r["path"]): (r["dest"], r["target"]) for r in rows24}
    ch24 = {(r["file"], r["path"]) for r in rows if m24.get((r["file"], r["path"])) != (r["dest"], r["target"])}
    notes3 = erd.get("column_map_note_changes_v3", [])
    n3 = {(m["file"], m["path"]) for m in notes3}
    line(ch24 == set() and len(rows24) == len(rows) and len(moves3) == 0 and len(notes3) >= 30 and n3 <= leaf and ("변화 없음" in cmap), f"v2.4 표와 표적이 다른 행 {len(ch24)} = 이동 표 v2.4→v3 {len(moves3)} (이동 0 · 변화 없음 명시 · 비고만 바뀐 행 {len(notes3)} 전부 실제 잎 키)")
    # 2판 잎 키 재스캔 = 1판 (행선지 전수)
    rescan3 = erd.get("bronze_leaf_rescan", {})
    scanner = load_module("bronze_scan2", os.path.join(HERE, "bronze-ledger-column-scan.py"))
    s2 = {}
    for f in scan["files"]:
        s2[f] = set(scanner.FileScan(os.path.join(LEDGER, f)).run()["leaf_paths"])
    diff2 = {f: (sorted(set(scan["files"][f]["leaf_paths"]) - s2[f]), sorted(s2[f] - set(scan["files"][f]["leaf_paths"]))) for f in scan["files"] if set(scan["files"][f]["leaf_paths"]) != s2[f]}
    line(not diff2 and sum(len(v) for v in s2.values()) == n_ledger and rescan3.get("leaf_count_v2") == n_ledger and not rescan3.get("diff"), f"브론즈 2판 잎 키 재스캔 {sum(len(v) for v in s2.values())} = 1판 {n_ledger} · 파일별 집합 차이 {len(diff2)}" + (": " + "; ".join(f"{f}: 1판만 {a} / 2판만 {b}" for f, (a, b) in diff2.items()) if diff2 else " (전부 같다 — 2판은 이름 6곳만 바뀜)"))
    rows23 = parse_column_map(V2["v23"]["cmap"])
    m23 = {(r["file"], r["path"]): (r["dest"], r["target"]) for r in rows23}
    ch23 = {(r["file"], r["path"]) for r in rows if m23.get((r["file"], r["path"])) != (r["dest"], r["target"])}
    notes24 = V2["v24"]["erd"].get("column_map_note_changes_v2_4", [])
    line(ch23 == set() and len(rows23) == len(rows) and len(moves24) == 0 and len(notes24) == 41, f"v2.3 표와 표적이 다른 행 {len(ch23)} = 이동 표 v2.3→v2.4 {len(moves24)} (이동 0 · v2.4 비고 변경 {len(notes24)})")
    rows22 = parse_column_map(V2["v22"]["cmap"])
    m22 = {(r["file"], r["path"]): (r["dest"], r["target"]) for r in rows22}
    ch22 = {(r["file"], r["path"]) for r in rows if m22.get((r["file"], r["path"])) != (r["dest"], r["target"])}
    notes23 = erd.get("column_map_note_changes_v2_3", [])
    line(ch22 == {(m["file"], m["path"]) for m in moves23} and len(rows22) == len(rows) and len(moves23) == 0 and len(notes23) == 30, f"v2.2 표와 표적이 다른 행 {len(ch22)} = 이동 표 v2.2→v2.3 {len(moves23)} (이동 0 · 비고만 바뀐 행 {len(notes23)}: 시술 축 참조 자리 16 + pih procedure_ref + timeline category + taxonomy safety 11 + complications name)")
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
    badsha, badtxt = [], []
    hashes = {}
    for ln in open(os.path.join(LEDGER, "HASHES.txt"), encoding="utf-8"):
        h, f = ln.split()
        hashes[f] = h
    for fm in erd["source_files"]:
        path = os.path.join(LEDGER, fm["file"]) if fm["file"] != STEP1 else os.path.join(HERE, STEP1)
        full = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if full != fm["sha256"]:
            badsha.append(fm["file"])
        if fm["file"] != STEP1 and (not full.startswith(hashes.get(fm["file"], "∅")) or fm.get("hashes_txt") != hashes.get(fm["file"]) or fm.get("bronze_version") != 2):
            badtxt.append(fm["file"])
    changed = [fm["file"] for fm in erd["source_files"] if fm.get("changed_from_v1")]
    v1ok = all((hashlib.sha256(open(os.path.join(LEDGER_V1, fm["file"]), "rb").read()).hexdigest() == fm["v1_sha256"]) == True for fm in erd["source_files"] if fm["file"] != STEP1) if os.path.isdir(LEDGER_V1) else True
    line(not badsha and not badtxt and len(erd["source_files"]) == 22 and len(hashes) == 21 and erd.get("bronze_version") == 2 and erd["bronze"]["version"] == 2, f"원장 21(브론즈 2판 bronze/phub-ledger) + step1 sha256 일치 (파일 {len(erd['source_files'])}, 불일치 {len(badsha)}) · HASHES.txt 21 과 접두 일치(불일치 {len(badtxt)}) · 판 2 기록")
    line(sorted(changed) == ["treatment-optimization.json", "treatment-sequence.json"] and v1ok and len(erd["bronze"]["name_diff"]) == 2 and sum(len(d["v2_only"]) for d in erd["bronze"]["name_diff"]) == 5, f"1판 대조: 바뀐 파일 {changed} (CHANGELOG 6곳 = treatment-optimization 2 + treatment-sequence 4 · distinct 새 이름 {sum(len(d['v2_only']) for d in erd['bronze']['name_diff'])}) · 1판 sha256 기록 일치 {v1ok}")
    s1m = next(fm for fm in erd["source_files"] if fm["file"] == STEP1)
    line(s1m["kind"] == "research_artifact" and s1m["trust_tier"] == 3 and "tier2_when" in s1m.get("trust_tier_rule", {}), f"step1 = research_artifact · 기본 3 · 허가 필드 조건부 2 ({s1m['trust_tier_rule']['tier2_licenses']}/{s1m['trust_tier_rule']['licenses_total']} 건)")
    out.append("")

    # ---- E
    out.append("### E. 분해 규칙 재현 (erd-v1.1-resolve.py 를 v2 사전으로 재실행)")
    out.append("")
    res = load_module("erd_v11_resolve", os.path.join(HERE, "erd-v1.1-resolve.py"))
    tuples_mod = load_module("erd_v3_tuples", os.path.join(HERE, "erd-v3-tuples.py"))
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
    allowed_slots = ("treatment-optimization", "treatment-sequence", "부위 사전")
    bad11 = [d for d in diffs11 if not d.startswith(allowed_slots)]
    line(not bad11, f"v1.1·v2 수치와 같음 — 2판에서 이름이 바뀐 treatment-optimization·treatment-sequence 자리와 부위 사전(v3 조직층 5)만 다를 수 있다(그 자리 차이 {len(diffs11) - len(bad11)} · 그 밖 불일치 {len(bad11)})" + (": " + "; ".join(bad11[:5]) if bad11 else "") + ("; 허용된 차이: " + "; ".join(diffs11[:8]) if diffs11 else ""))
    line(TOTAL["unresolved_v1_1"] == erd["resolution_total"]["unresolved_v1_1"] and TOTAL["decomposed_v1_1"] == erd["resolution_total"]["decomposed_v1_1"], f"합계 재현: 미해결 {TOTAL['unresolved_v1_1']} · 분해 성공·항목 없음 {TOTAL['decomposed_v1_1']} · 해결 {TOTAL['resolved_v1_1']}")
    rr = erd["resolve_rules"]
    line(rr["step3_assemble"].get("no_similarity") is True and rr["step2_decompose"]["dictionary_order"] == ["product", "modality_subcategory", "procedure", "site", "spec", "product_tier"], "규칙 데이터: 유사도 금지 · 사전 순서 제품→하위분류→분류 항목(procedure 자리 = catalog_item_name)→부위→규격→product_tier")
    out.append("")

    # ---- F
    out.append("### F. 처분 반영 (v1.1 그대로)")
    out.append("")
    D = {d["name"]: d for d in dic["dictionaries"]}
    site = D["site"]["entries"]
    ext = [e for e in site if e.get("site_kind") not in ("backbone", "taxonomy_site_label", "layer")]
    line(not ext and sum(1 for e in site if e.get("site_kind") == "backbone") == 11 and sum(1 for e in site if e.get("site_kind") == "layer") == 5 and len(site) == 26, f"부위 사전 {len(site)} = 뼈대 11 + taxonomy 부위 라벨 {sum(1 for e in site if e.get('site_kind') == 'taxonomy_site_label')} + v3 조직층 {sum(1 for e in site if e.get('site_kind') == 'layer')} · 확장 {len(ext)} (공유 사전 유지)")
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
    out.append("### G. 튜플 실측 재현 (erd-v2.4-tuples.py 재실행)")
    out.append("")
    TUP = tuples_mod.run_all(dic, erd["tuple_rules"], {k: v for k, v in ledgers.items() if k != STEP1}, erd["resolve_rules"], V2["v24"]["tup"])
    gd = []
    for axis in ("procedure", "adverse"):
        a, b, c = TUP[axis]["summary"], erd["tuple_report"][axis], tup[axis]["summary"]
        for k in a:
            if k in ("unregistered_top30_by_origin", "unregistered_by_origin", "unregistered_all", "unregistered_top30", "course_split_examples", "lop", "site_list_merges_all", "multi_candidate_splits_all", "unattached_fragments_all", "candidate_units_not_existing_all", "site_outside_member_examples", "expressions_partial_linked_examples", "principles",
                     "combo_labels_all", "combo_plus_v2", "stopwords", "company_paren", "v24_reference_changes", "multi_tuples", "alternatives", "families_mixed_detail", "inheritance_candidates", "qualifier_names_all", "qualifier_expressions_all", "qualifier_tuples_all", "qualifier_in_raw_dict_tuples", "layer_site_tuples_all", "layer_site_candidates_all", "layer_site_extra_all", "v24_comparison", "prefix_splits"):
                continue
            if json.dumps(a[k], ensure_ascii=False, sort_keys=True, default=str) != json.dumps(b.get(k), ensure_ascii=False, sort_keys=True, default=str) or json.dumps(a[k], ensure_ascii=False, sort_keys=True, default=str) != json.dumps(c.get(k), ensure_ascii=False, sort_keys=True, default=str):
                gd.append(f"{axis}.{k}")
    line(not gd, f"요약 수치 재현 불일치 {len(gd)} (erd-v3.json tuple_report · erd-v3-tuples.json 과 비교 · 목록형 키는 M 에서 따로)" + (": " + "; ".join(gd[:6]) if gd else ""))
    ps, as_ = TUP["procedure"]["summary"], TUP["adverse"]["summary"]
    same_ids = {t["id"] for t in TUP["procedure"]["tuples"]} == {t["id"] for t in tup["procedure"]["tuples"]} and {t["id"] for t in TUP["adverse"]["tuples"]} == {t["id"] for t in tup["adverse"]["tuples"]}
    line(same_ids, f"튜플 id 집합 재현 일치 (시술 {len(TUP['procedure']['tuples'])} · 부작용 {len(TUP['adverse']['tuples'])})")
    DK = ("product", "modality_subcategory", "modality")

    def prc_id(t):
        alld = t["what_kind"] in DK and t["site_id"] != "none" and t["technique_id"] != "none"
        return mkid("PRC", f"{t['what_id']}|{t['site_id']}|{t['technique_id']}" + ("" if alld else f"|{t['anchor']}")), alld
    badid = [t["id"] for t in TUP["procedure"]["tuples"] if prc_id(t)[0] != t["id"] or prc_id(t)[1] != t["all_dict_values"] or (t["anchor"] is None) != t["all_dict_values"]]
    ev_id = {e["canonical"]: e["id"] for e in D["adverse_event_type"]["entries"]}

    ql_id = {e["canonical"]: e["id"] for e in D["adverse_qualifier"]["entries"]}

    def adv_id(t):
        if t["event_kind"] == "raw_name":
            return mkid("ADV", f"RAW:{t['anchor']}|{t['site_id']}|{t['course_id']}|none|{t['anchor']}"), f"RAW:{t['anchor']}"
        return mkid("ADV", f"{ev_id[t['event']]}|{t['site_id']}|{t['course_id']}|{t['qualifier_id']}"), ev_id[t["event"]]
    badid += [t["id"] for t in TUP["adverse"]["tuples"] if adv_id(t)[0] != t["id"] or adv_id(t)[1] != t["event_id"] or (t["anchor"] is None) != (t["event_kind"] == "dict") or t["all_dict_values"] != (t["event_kind"] == "dict") or (t["qualifier_id"] != "none") != bool(t["qualifier"]) or (t["qualifier"] and ql_id.get(t["qualifier"]) != t["qualifier_id"])]
    line(not badid, f"식별자 규칙 재계산 불일치 {len(badid)} (v2.2: 세 칸 전부 사전 값이면 PRC-sha256(what_id|site_id|technique_id), 아니면 …|anchor · v3: ADV-sha256(event_id|site_id|course_id|qualifier_id · 없으면 none) / raw_name 은 ADV-sha256(RAW:anchor|none|미상|none|anchor) · anchor ⇔ raw_name · qualifier_id ⇔ qualifier)")
    cat = TUP["procedure"]["catalog"]
    n_items = sum(1 for m in ledgers["taxonomy.json"]["modality"] for sc in m["subcategories"] for _ in sc["items"])
    line(len(cat) == n_items == 521 and all(r.get("procedure_id") for r in cat), f"분류 항목 {len(cat)} (= taxonomy 항목 {n_items}) 전부 튜플 있음 (없는 것 {sum(1 for r in cat if not r.get('procedure_id'))})")
    fold_sum = sum(f["n_items"] for f in TUP["procedure"]["folded"])
    multi_extra = sum(len(r["member_ids"]) - 1 for r in cat if r["result"] == "multi_tuple")
    line(fold_sum == 521 + multi_extra and len(TUP["procedure"]["folded"]) == ps["catalog_distinct_tuples"], f"접힌 표 항목 합 {fold_sum} = 521 + 부위 여럿 항목의 추가 튜플 {multi_extra} · 튜플 {len(TUP['procedure']['folded'])} = distinct {ps['catalog_distinct_tuples']} (521 → {ps['catalog_distinct_tuples']})")
    comp_n = sum(len(c["complications"]) for c in ledgers["complications.json"]["categories"])
    named = {n for f in TUP["adverse"]["folded"] for n in f["names"]}
    comp_rows = TUP["adverse"]["complications"]
    line(comp_n == 65 == len(comp_rows) and all(r["tuple_ids"] for r in comp_rows), f"complications 이름 {comp_n} 전부 튜플 있음 (없는 것 {sum(1 for r in comp_rows if not r['tuple_ids'])}) · 접힌 표에 등장하는 이름 {len(named)}")
    line(all("catalog_item" in t["origins"] or "reference" in t["origins"] or "market_pricing" in t["origins"] for t in TUP["procedure"]["tuples"]) and all(t["sources"] for t in TUP["adverse"]["tuples"]), "튜플마다 원천(출처 이름·문구) ≥1")
    tech_fam = {pr["id"]: pr["mechanism"] for pr in ledgers["procedure-profiles.json"]["profiles"]}
    bad_t = [t["id"] for t in TUP["procedure"]["tuples"] if t["technique_origin"] not in ("fragment", "none") or (t["technique_origin"] == "none") != (t["technique_id"] == "none")]
    line(not bad_t, f"technique_origin ∈ {{fragment, none}} · none ⇔ technique_id none (위반 {len(bad_t)}) — v2.1 항목 「상속 기법 = R5 단일 기법」은 v2.2 에서 「상속 0」(J-3)으로 바뀜 · 상속 불가 계열 {ps['families_without_single_technique']}")
    unk = [t["id"] for t in TUP["procedure"]["tuples"] if t["what_kind"] not in ("modality", "modality_subcategory", "product", "catalog_item")]
    line(not unk and all(t["site_id"] == "none" or (t["site"] in {e["canonical"] for e in site} and next(e for e in site if e["canonical"] == t["site"]).get("kind") != "layer") for t in TUP["procedure"]["tuples"]), f"what ∈ {{modality, modality_subcategory, product, catalog_item(v2.1)}} 위반 {len(unk)} · site ∈ 부위 사전(anatomical·region) | none — layer 는 시술 site 칸에 없다(v3)")
    line(all(t["course"] in {e["canonical"] for e in D["course"]["entries"]} for t in TUP["adverse"]["tuples"]) and all(t["site_kind"] in ("site", "relative", "none") for t in TUP["adverse"]["tuples"]) and all(t["event_kind"] in ("dict", "raw_name") for t in TUP["adverse"]["tuples"]) and all(t["event"] in ev_id for t in TUP["adverse"]["tuples"] if t["event_kind"] == "dict") and all(t["status"] in ("complete", "partial", "unresolved") for t in TUP["adverse"]["tuples"]) and all((t["qualifier"] is None) or (t["qualifier"] in ql_id) for t in TUP["adverse"]["tuples"]), "부작용 튜플 course ∈ 경과 사전 · site ∈ {site, relative, none} · qualifier ∈ 수식 사전 | none(v3) · event_kind ∈ {dict, raw_name} · status ∈ {complete, partial, unresolved} · dict 튜플 event ∈ 사건 사전")
    out.append(f"- 시술: 분류 항목 521 → 튜플 {ps['catalog_distinct_tuples']} · 참조 ② {ps['reference_total']['n']} → 튜플 {ps['reference_total']['tuple']} + combo_ref {ps['reference_total']['combo_ref']} + 미해결 {ps['reference_total']['unresolved']} + 불가 {ps['reference_total']['none']} · ③ 122 → 튜플 {ps['market_pricing']['tuple']} + combo_ref {ps['market_pricing']['combo_ref']} + 불가 {ps['market_pricing']['none']} · 전체 튜플 {ps['tuples_total']} · site none 비율 {ps['tuples_site_none_ratio']} · technique none 비율 {ps['tuples_technique_none_ratio']} · 미등록 조각 distinct {ps['unregistered_distinct']}")
    out.append(f"- 부작용: complications 65 → 튜플 {as_['complications_distinct_tuples']}(사전 {as_['complications_distinct_tuples_dict']} + raw_name {as_['complications_distinct_tuples_raw']}) · 사건 사전 {as_['event_dictionary_values']} · 표현 {as_['expressions_total']['n']} (linked {as_['expressions_total']['linked']} · partial {as_['expressions_total']['match_status'].get('partial', 0)} · unlinked {as_['expressions_total']['unlinked']}) · 전체 튜플 {as_['tuples_total']} · 미등록 조각 distinct {as_['unregistered_distinct']}")
    out.append("")

    # ---- H
    out.append("### H. 구조 변경 반영")
    out.append("")
    ek = [e["key"] for e in erd["entities"]]
    line(len(ek) == 21 and "catalog_item" in ek and "adverse_expression" in ek and "procedure" in ek and "adverse_effect" in ek, f"개체 {len(ek)} = v1.1 19 + catalog_item + adverse_expression (v3 불변)")
    rids = [r["id"] for r in erd["relations"]]
    line(len(rids) == 31 and all(f"R{i}" in rids for i in range(26, 32)), f"관계 {len(rids)} = v1.1 25 + R26~R31")
    line(len(dnames) == 47 and {"adverse_event_type", "course", "relative_site", "catalog_item_name", "adverse_qualifier"} <= dnames and "procedure_name" not in dnames, f"사전 {len(dnames)} = v1.1 43 + 사건·경과·상대 부위 + v3 adverse_qualifier (procedure_name → catalog_item_name 개명)")
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
    line("catalog_item" not in erd["enums"]["target_depth"] and "procedure" in erd["enums"]["target_depth"] and set(erd["enums"]["target_depth"]) == {"modality", "subcategory", "procedure", "product"}, f"target_depth = {erd['enums']['target_depth']} (v2.3: catalog_item 은 끝이 아니다 — v2 항목 「catalog_item 추가」는 K-1 로 대체)")
    line("combo_ref" in erd["enums"]["package.kind"], "package.kind 에 combo_ref")
    ev = D["adverse_event_type"]["entries"]
    line(all(e.get("category") in CATEGORIES for e in ev) and all(s.get("kind") == "derived" and s["file"] == "complications.json" for e in ev for s in e["sources"]), f"사건 사전 {len(ev)} 값마다 category ∈ 7 분류 · 출처 전부 complications.json 이름(derived) · 동의어 {sum(len(e['synonyms']) for e in ev)}")
    cs = {e["canonical"] for e in D["course"]["entries"]}
    line(cs == {"일시", "지연", "영구", "재발", "미상"}, f"경과 사전 = {sorted(cs)}")
    rs = {e["canonical"] for e in D["relative_site"]["entries"]}
    line(rs == {"주사 부위", "시술 부위"}, f"상대 부위 사전 = {sorted(rs)}")
    ee_rule = erd["edge_end_rule"]
    promoted = [r["id"] for r in erd["relations"] if r["id"] in ("R3", "R9", "R12", "R15", "R16", "R17", "R18") and ee_rule in (r["note"] or "") and "승격" not in (r["note"] or "")]
    line(len(promoted) == 7, f"시술 축 엣지 7(R3·R9·R12·R15·R16·R17·R18)에 v2.3 엣지 끝 규칙 기록(승격 규칙 0): {promoted} — v2 항목 「승격 규칙」은 K-1 로 대체")
    line(len(erd["decisions"]) == 26, f"결정 레코드 {len(erd['decisions'])} = 처분 19 + 구조 변경 2 + v2.1 접힘 규칙 1 + v2.2 개정 1 + v2.3 개정 1 + v2.4 개정 1 (이관 25 · J-6) + v3 개정 1")
    out.append("")

    # ---- I (v2.1 항목 — v2.2 기대값)
    out.append("### I. v2.1 접힘 규칙 (v2.1 항목 유지 · v2.2 에서 바뀐 기대값은 항목 안에)")
    out.append("")
    V21 = V2["v21"]
    rr3 = erd["resolve_rules"]["step3_assemble"]
    tr = erd["tuple_rules"]["procedure"]
    line(rr3.get("fallback_to_parent") is False and tr.get("fallback_to_parent") is False and erd["tuple_rules"]["name"] == "tuples_v3", f"규칙 데이터: resolve_rules.step3_assemble.fallback_to_parent={rr3.get('fallback_to_parent')} · tuple_rules.procedure.fallback_to_parent={tr.get('fallback_to_parent')} · tuple_rules.name={erd['tuple_rules']['name']}")
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
    stop_res = Counter(x["slot"] for x in ps["stopwords"]["references_changed"] if x["before"].startswith("unresolved:unregistered") and not x["after"].startswith("unresolved:unregistered"))
    for k, v in ps["reference_slots"].items():
        w = OUT.get(k)
        if w is not None and w["unresolved"] - stop_res.get(k, 0) != v["unresolved_by_reason"].get("unregistered", 0):
            ud.append(f"{k}: 분해 규칙 {w['unresolved']} − stopwords 로 풀림 {stop_res.get(k, 0)} vs 튜플(unregistered) {v['unresolved_by_reason'].get('unregistered', 0)}")
    mk_key = next((k for k in OUT if k.startswith("market-pricing")), None)
    if mk_key and OUT[mk_key]["unresolved"] - stop_res.get(mk_key, 0) != ps["market_pricing"]["unresolved_by_reason"].get("unregistered", 0):
        ud.append(f"{mk_key}: 분해 규칙 {OUT[mk_key]['unresolved']} vs 튜플 {ps['market_pricing']['unresolved_by_reason'].get('unregistered', 0)}")
    line(not ud, f"미해결(사유 unregistered) 수 = v1.1 분해 규칙(§9.2 · stopwords 없음) 미해결 수 − stopwords 로 풀린 참조 {sum(stop_res.values())} — 자리별 불일치 {len(ud)} (v2.2 는 그 위에 multi_*/unusable 미해결이 더해진다)" + (": " + "; ".join(ud[:6]) if ud else ""))
    d21 = {d["name"]: d for d in V2["v24"]["dic"]["dictionaries"]}
    d1 = {d["name"]: d for d in dic["dictionaries"]}
    V3_CHANGED = {"site", "adverse_event_type", "adverse_qualifier"}
    same_dic = set(d1) - V3_CHANGED == set(d21) - V3_CHANGED and all([(e["canonical"], tuple(s_["value"] for s_ in e["synonyms"])) for e in d1[n]["entries"]] == [(e["canonical"], tuple(s_["value"] for s_ in e["synonyms"])) for e in d21[n]["entries"]] for n in d1 if n not in V3_CHANGED)
    c21 = {e["canonical"]: [s_["value"] for s_ in e["synonyms"]] for e in d21["course"]["entries"]}
    c22 = {e["canonical"]: [s_["value"] for s_ in e["synonyms"]] for e in d1["course"]["entries"]}
    dropped = sorted({(k, x) for k, v in c21.items() for x in v} - {(k, x) for k, v in c22.items() for x in v})
    line(same_dic and list(c21) == list(c22) and c21 == c22 and not dropped, f"사전 {len(d1)}: v3 가 바꾼 셋(site · adverse_event_type · adverse_qualifier) 밖 {len(d1) - 3} 개는 값·동의어·순서 = v2.4 · course 정준값 5·동의어 동일 · 뺀 동의어 {dropped}")
    line(len(erd["entities"]) == len(V21["erd"]["entities"]) == 21 and len(erd["relations"]) == len(V21["erd"]["relations"]) == 31 and [e["key"] for e in erd["entities"]] == [e["key"] for e in V21["erd"]["entities"]] and [r["id"] for r in erd["relations"]] == [r["id"] for r in V21["erd"]["relations"]], f"구조 = v2.1 = v2.2 (개체 {len(erd['entities'])} · 관계 {len(erd['relations'])} · 같은 키·순서)")
    pe = next(e for e in erd["entities"] if e["key"] == "procedure")
    r27 = next(r for r in erd["relations"] if r["id"] == "R27")
    line("catalog_item" in erd["enums"]["procedure.what_kind"] and any(a["name"] == "candidate_name" for a in pe["attrs"]) and "catalog_item" in r27["to"], f"procedure.what_kind = {erd['enums']['procedure.what_kind']} · candidate_name 속성 · R27 → {r27['to']}")
    line(ps["catalog_distinct_tuples"] == len(TUP["procedure"]["folded"]) and sum(f["n_items"] for f in TUP["procedure"]["folded"]) == 521, f"521 → {ps['catalog_distinct_tuples']} (v2.1 {V21['tup']['procedure']['summary']['catalog_distinct_tuples']} · v2 {V2['tup']['procedure']['summary']['catalog_distinct_tuples']}) · 접힌 표 항목 합 521")
    V22T = V2["v23"]["tup"]["adverse"]["summary"]
    comp_rows = TUP["adverse"]["complications"]
    raw_names = [r for r in comp_rows if r["unregistered"]]
    line(as_["complications_names_raw"] == sum(1 for r in comp_rows if r["unregistered"] or r["extra_sites"] or r["extra_courses"]) and all(r["event_kind"] == "raw_name" and len(r["tuple_ids"]) == 1 for r in raw_names) and all(r["event_kind"] == "dict" for r in comp_rows if not (r["unregistered"] or r["extra_sites"] or r["extra_courses"])),
         f"부작용 튜플 ≠ v2.1·v2.2 (v2.3 수정 2·3 · v2.4 1·2·3): 미등록 조각 있는 complications 이름 {len(raw_names)} 전부 raw_name 튜플 하나씩 · 미등록 0 인 이름 {len(comp_rows) - len(raw_names)} 은 사전 튜플(붙지 않은 조각이 남으면 raw) — v2.3 65 → {V22T['complications_distinct_tuples']} / v2.4 65 → {as_['complications_distinct_tuples']} · 표현 linked v2.3 {V22T['expressions_total']['linked']} → v2.4 exact {as_['expressions_total']['linked']}")
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
    shape = {"dictionary_add": ["dictionary", "canonical", "synonyms", "category"], "tuple_assign": ["catalog_item_id", "ref_id", "what_kind", "what_id", "site_id", "technique_id"], "fold_approve": ["anchors", "keep_anchor"],
             "event_split": ["event", "new_events"], "canonical_mapping": ["from_ref", "to_id", "scope"], "conflict_override": ["conflict_key", "chosen_value"], "exclude": ["kind", "key"]}  # v2.3: fold_approve·conflict_override·exclude 개형(K-2)
    bad_shape = [k for k in need if k not in dk or not dk[k]["build_reads"] or not all(x in (dk[k]["target"] + dk[k]["new_value"]) for x in shape[k])]
    bad_rec = [d["id"] for d in erd["decisions"] if list(d.keys()) != common or not isinstance(d["target"], dict) or not isinstance(d["new_value"], dict) or d["status"] not in ("proposed", "approved", "rejected") or d["kind"] not in erd["enums"]["decision.kind"]
               or (d["status"] == "proposed" and (d["decided_by"] is not None or d["decided_at"] is not None)) or (d["status"] == "approved" and not d["decided_by"]) or not d["source_refs"]]
    line(set(need) <= set(erd["enums"]["decision.kind"]) and not bad_shape and [a["name"] for a in de["attrs"]] == common and erd["enums"]["decision.status"] == ["proposed", "approved", "rejected"] and "approved" in erd["decision_build_rule"] and not bad_rec,
         f"J-5 decision kind 7 {need} 전부 enum·표(target/new_value 구조체 필드)·build_reads · kind 총 {len(erd['enums']['decision.kind'])} · 개체 속성 = 공통 필드 {len(common)} · 「{erd['decision_build_rule'][:40]}…」 · 레코드 모양 위반 {len(bad_rec)}" + (f": {bad_rec[:4]}" if bad_rec else "") + f" · 형태 위반 {bad_shape}")
    # J-6 이관 22
    old = {d["id"]: d for d in V2["v24"]["erd"]["decisions"]}
    new = {d["id"]: d for d in erd["decisions"]}
    mig = erd.get("decisions_migration", [])
    bad_mig = [i_ for i_ in old if i_ not in new or new[i_]["kind"] != old[i_]["kind"] or new[i_]["target"] != old[i_]["target"] or new[i_]["status"] != old[i_]["status"]]
    prop = sorted(i_[-2:] for i_ in old if new.get(i_, {}).get("status") == "proposed")
    appr = sum(1 for i_ in old if new.get(i_, {}).get("status") == "approved")
    line(len(old) == 25 and not bad_mig and len(mig) == 25 and prop == ["20", "21", "22", "23", "24", "25"] and appr == 19 and all(new[f"DEC-2026-11-04-{n}"]["decided_by"] is None for n in ("20", "21", "22", "23", "24", "25")) and new.get("DEC-2026-11-05-26", {}).get("status") == "proposed",
         f"J-6 기존 결정 {len(old)}(v2.4) 전부 이관(id·kind·target·status 유지 · 누락/변경 {len(bad_mig)}) · 이관 표 {len(mig)} · approved {appr}(처분 19) · proposed {prop}(decided_by·decided_at null) · 신규 {sorted(set(new) - set(old))}")
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
    # ---- K (v2.3)
    out.append("### K. v2.3 수정 7건 (발주서 erd-v2.3-brief.md)")
    out.append("")
    END_KINDS = ["procedure", "modality", "subcategory", "product", "unresolved"]
    TT3 = {t["id"]: t for t in TUP["procedure"]["tuples"]}
    ee_rows = TUP["procedure"]["edge_ends"]
    ee_json = erd.get("edge_ends", {})
    bad_ee = []
    for r_ in ee_rows:
        if sum(r_[k] for k in END_KINDS) != r_["n"] or r_["n"] != len(r_["ends"]):
            bad_ee.append(f"{r_['slot']}: 합 불일치")
        for e in r_["ends"]:
            if e["end_kind"] not in END_KINDS:
                bad_ee.append(f"{r_['slot']}: {e['label']} 끝 종류 {e['end_kind']}")
            elif e["end_kind"] == "procedure":
                ids_ = e["end_id"] if isinstance(e["end_id"], list) else [e["end_id"]]
                if not ids_ or any(i_ not in TT3 for i_ in ids_) or e["target_depth"] != "procedure":
                    bad_ee.append(f"{r_['slot']}: {e['label']} procedure 끝이 튜플이 아님")
            elif e["end_kind"] in ("modality", "subcategory", "product") and (not e["end_id"] or e["target_depth"] != e["end_kind"]):
                bad_ee.append(f"{r_['slot']}: {e['label']} 노드 끝 id 없음")
            if e.get("via_catalog_item") and not str(e["via_catalog_item"]).startswith("CAT-"):
                bad_ee.append(f"{r_['slot']}: via 가 CAT- 아님")
    # 텍스트 자리: 참조 결과 ⇔ 끝 종류
    ref_all = {(k, r_["label"], r_.get("hint")): r_ for k, v in TUP["procedure"]["references"].items() for r_ in v}
    for r_ in ee_rows:
        if r_["kind"] != "text" or r_["relation"] == "—":
            continue
        prod_slot = "products[]" in r_["slot"]
        for e in r_["ends"]:
            ref = ref_all.get((r_["slot"], e["label"], e.get("hint")))
            if ref is None:
                bad_ee.append(f"{r_['slot']}: {e['label']} 참조 행 없음")
                continue
            want = ("product" if prod_slot else "procedure") if ref["result"] in ("tuple", "combo_ref", "multi_tuple") else ref["end_kind"] if ref["result"] == "node" else "unresolved"
            if e["end_kind"] != want:
                bad_ee.append(f"{r_['slot']}: {e['label']} {ref['result']} → {e['end_kind']} (기대 {want})")
    rels_cov = set(r_["relation"] for r_ in ee_rows if r_["relation"] != "—")
    has_958 = "#### 9.5.8" in md if md else True
    tot = erd["tuple_report"]["procedure"]["edge_ends_total"]
    line(not bad_ee and rels_cov == {"R3", "R9", "R12", "R15", "R16", "R17", "R18"} and ee_json.get("rows") and len(ee_json["rows"]) == len(ee_rows) and ee_json["total"] == tot and has_958 and erd["enums"]["edge_end_kind"] == END_KINDS
         and all(r_["result"] != "tuple" for v in TUP["procedure"]["references"].values() for r_ in v if str(r_["label"]).startswith("M") and r_.get("what_basis") in ("modality_code", "subcategory_id")),
         f"K-1 엣지 끝 분포 실측 존재 — 자리 {len(ee_rows)}(텍스트 {sum(1 for r_ in ee_rows if r_['kind']=='text' and r_['relation']!='—')} + 코드·레코드 {sum(1 for r_ in ee_rows if r_['kind']=='code')} · ③ 참고 1) · 관계 {sorted(rels_cov, key=lambda x: int(x[1:]))} · 건 {erd['tuple_report']['procedure']['edge_ends_total_n']}: {tot} · 끝 종류 전부 {END_KINDS} 안 · 참조 결과 ⇔ 끝 종류 위반 {len(bad_ee)}" + (": " + "; ".join(bad_ee[:5]) if bad_ee else "") + f" · 코드 참조 node {erd['tuple_report']['procedure']['code_references_node']}(튜플 0) · md §9.5.8 {has_958}")
    # K-2 파생 id target 0
    DER = re.compile(r"\b(PRC|ADV|CFL)-")
    bad_tgt = [d["id"] for d in erd["decisions"] if DER.search(json.dumps(d["target"], ensure_ascii=False))]
    bad_kind_tgt = [k["kind"] for k in erd["decision_kinds"] if DER.search(k["target"])]
    tr_rule = erd.get("decision_target_rule", "")
    line(not bad_tgt and not bad_kind_tgt and all(x in tr_rule for x in ("PRC-", "ADV-", "CFL-", "금지", "locator")) and "stable_key" in {a["name"] for a in next(e for e in erd["entities"] if e["key"] == "conflict")["attrs"]},
         f"K-2 파생 id(PRC-/ADV-/CFL-)를 target 으로 쓰는 결정 {len(bad_tgt)} / {len(erd['decisions'])} · kind 표 target 에 파생 id {len(bad_kind_tgt)} / {len(erd['decision_kinds'])} · target 규칙(json decision_target_rule · §1.1) 금지 명시 · conflict.stable_key 속성")
    # K-3 적용 순서
    ORDER = [["dictionary_add", "canonical_rename"], ["canonical_mapping"], ["tuple_assign", "tuple_assign_multi", "adverse_tuple_assign"], ["fold_approve", "event_split"], ["edge_create"], ["conflict_override", "conflict_close"], ["exclude"]]
    ao = erd.get("decision_apply_order", [])
    br_kinds = [k["kind"] for k in erd["decision_kinds"] if k["build_reads"] and k["kind"] != "reclassification"]
    in_order = [k_ for st in ao for k_ in st["kinds"]]
    sec54 = ("### 5.4" in md and md.count("| ①") >= 1 and "| ⑦" in md) if md else True
    line([st["kinds"] for st in ao] == ORDER and [st["stage"] for st in ao] == ["①", "②", "③", "④", "⑤", "⑥", "⑦"] and sorted(in_order) == sorted(br_kinds) and len(in_order) == len(set(in_order)) and "decided_at" in erd.get("decision_apply_order_rule", "") and sec54,
         f"K-3 적용 순서 표 존재 — {' → '.join(st['stage'] + ' ' + '/'.join(st['kinds']) for st in ao)} · 빌드 적용 kind {len(br_kinds)} 전부 한 번씩(reclassification 은 ⓪) · 같은 단계 decided_at 순 · md §5.4 {sec54}")
    # K-4 kind 16
    new4 = {"edge_create": ["relation", "from_ref", "to_ref", "attrs"], "tuple_assign_multi": ["catalog_item_id", "ref_id", "tuples"], "adverse_tuple_assign": ["locator", "raw_name", "expression", "tuples", "event_id", "site_id", "course_id"], "conflict_close": ["conflict_key", "verdict", "not_same", "both_valid", "needs_source", "note"]}
    bad4 = [k_ for k_, fs in new4.items() if k_ not in dk or not dk[k_]["build_reads"] or not all(f_ in (dk[k_]["target"] + dk[k_]["new_value"]) for f_ in fs)]
    line(len(erd["enums"]["decision.kind"]) == 17 and len(erd["decision_kinds"]) == 17 and not bad4 and all(dk[k_].get("new_in_v2_3") for k_ in new4) and erd["enums"].get("conflict.close_verdict") == ["not_same", "both_valid", "needs_source"] and "edge_create" in next(r for r in erd["relations"] if r["id"] == "R30")["note"],
         f"K-4 결정 kind {len(erd['enums']['decision.kind'])} = 12 + 4({', '.join(new4)}) + v3 1(canonical_rename) · 구조체 필드 위반 {bad4} · conflict.close_verdict enum · R30 은 edge_create 로만")
    # K-5 부작용 미등록 포함 접힘 0
    AF = TUP["adverse"]["folded"]
    comp_rows3 = TUP["adverse"]["complications"]
    af2 = [f for f in AF if f["n_names"] >= 2]
    bad_af = [f["event"] for f in af2 if f["unregistered"] or f["event_kind"] != "dict" or not f["all_dict_values"]]
    raw_t = [t for t in TUP["adverse"]["tuples"] if t["event_kind"] == "raw_name"]
    bad_raw = [t["id"] for t in raw_t if len({s_["locator"] for s_ in t["sources"]}) != 1 or not (t["candidate_name"] or t["extra_sites"] or t["extra_courses"] or t.get("extra_qualifiers")) or t["anchor"] != t["sources"][0]["locator"] or "complications" not in t["origins"] or t["all_dict_values"]]
    bad_comp = [r_["text"] for r_ in comp_rows3 if (bool(r_["unregistered"] or r_["extra_sites"] or r_["extra_courses"] or r_.get("extra_qualifiers")) != (r_["event_kind"] == "raw_name")) or (r_["event_kind"] == "raw_name" and len(r_["tuple_ids"]) != 1)]
    ex_rows = TUP["adverse"]["expressions"]

    def _clean(r_):
        pk = r_.get("patient_ko") or {}
        return not (r_["unregistered"] or r_["extra_sites"] or r_["extra_courses"] or r_.get("extra_qualifiers") or pk.get("unregistered") or pk.get("extra_sites") or pk.get("extra_courses") or pk.get("extra_qualifiers"))
    bad_ex = [r_["text"][:30] for r_ in ex_rows if r_["match_status"] != ("exact" if (r_["tuple_ids_union"] and _clean(r_) and all(c["exists"] for c in (r_.get("candidates_union") or r_["candidates"]))) else "unlinked") or (r_["match_status"] == "unlinked" and r_["tuple_ids_union"])]
    sec966 = ("#### 9.6.6" in md and "미등록 조각 있는 이름이 섞인 튜플 **0**" in md) if md else True
    line(not bad_af and not bad_raw and not bad_comp and not bad_ex and as_["folded_with_partial_name"] == 0 and as_["expressions_raw_name_tuples"] == 0 and erd["enums"]["adverse_effect.event_kind"] == ["dict", "raw_name"] and erd["enums"]["adverse_expression.match_status"] == ["exact", "unlinked"] and "세 칸 전부 사전 값일 때만" in erd["adverse_fold_rule"] and "수식 칸" in erd["adverse_fold_rule"] and sec966,
         f"K-5 부작용 미등록 포함 접힘 0 — 접힌 튜플 {len(af2)} 전부 사전 값·미등록 0(위반 {len(bad_af)}) · raw_name 튜플 {len(raw_t)} = 미등록 조각 있는 이름 {sum(1 for r_ in comp_rows3 if r_['unregistered'])} (이름마다 하나 · anchor=locator · 위반 {len(bad_raw) + len(bad_comp)}) · 65 → {as_['complications_distinct_tuples']}(사전 {as_['complications_distinct_tuples_dict']} + raw {as_['complications_distinct_tuples_raw']}) · 표현 raw_name 0 · match_status 위반 {len(bad_ex)} (v2.4: exact {as_['expressions_total']['match_status'].get('exact', 0)} · unlinked {as_['expressions_total']['match_status'].get('unlinked', 0)}) · md §9.6.6 {sec966}")
    # K-6 course 규칙
    cr3 = erd.get("course_rule", "")
    lop = as_.get("lop", [])
    lop_ok = bool(lop) and all({tuple(t[:3]) for t in (x["dict_tuples"] or x["tuples"])} >= {("통증", None, "미상"), ("통증", None, "지연")} for x in lop)
    bad_cb = [r_["text"][:30] for r_ in comp_rows3 + ex_rows if r_.get("event_kind", "dict") == "dict" for t in r_["tuples"] if t[2] != "미상" and t[3] != "member"]
    line(all(x in cr3 for x in ("사건에 바로 붙은 수식어만", "수식어가 붙은 사건에만 경과를 주고 나머지는 미상", "(통증, 미상) + (통증, 지연)")) and lop_ok and not bad_cb and erd["tuple_rules"]["adverse"].get("course") == cr3 and (not md or md.count("사건에 바로 붙은 수식어만") >= 3),
         f"K-6 course 규칙 문장(사건에 바로 붙은 수식어만 · 사건 둘 이상이면 수식어 붙은 사건에만 · LOP 둘) — §1.5·§2.14·§4(J-7 동일) · LOP 실측 {[x['dict_tuples'] or x['tuples'] for x in lop]} · 미상 아닌 경과가 멤버 밖에서 온 튜플 {len(bad_cb)}" + (": " + "; ".join(bad_cb[:4]) if bad_cb else ""))
    # K-7 기법 잔재(상속) 표현 0
    te = next(e for e in erd["entities"] if e["key"] == "technique")
    pe3 = next(e for e in erd["entities"] if e["key"] == "procedure")
    tid_attr = next(a for a in pe3["attrs"] if a["name"] == "technique_id")
    wid_attr = next(a for a in pe3["attrs"] if a["name"] == "what_id")
    to_attr = next(a for a in pe3["attrs"] if a["name"] == "technique_origin")
    def auto_inherit(text):
        """자동 상속 표현 — 「상속」이 결정 문맥(canonical_mapping · 결정 · V3-8 · 자동 아님)이 아닌 문장에 있는 수"""
        n = 0
        for sent in re.split(r"[.·|]", text):
            if "상속" in sent and not any(k_ in sent for k_ in ("결정", "canonical_mapping", "V3-8", "자동 아님", "자동 상속", "상속 없음", "상속은 하지 않는다", "붙이지 않는다", "후보")):
                n += 1
        return n
    json_hits = sum(auto_inherit(x) for x in (te["definition"], tid_attr["rule"], to_attr["rule"], pe3["definition"], erd["tuple_rules"]["procedure"]["technique"]))
    md_hits, md_scope = None, None
    if md:
        body = md.split("\n## 10. ")[0]
        a53 = body.find("### 5.3 ")
        b53 = body.find("### 5.4 ")
        scope = body[:a53] + body[b53:] if a53 >= 0 and b53 > a53 else body
        md_hits = auto_inherit(scope)
        md_scope = "§1~§9(§5.3 결정 레코드 원문 제외 · v3: 「상속」이 결정 문맥(V3-8 · canonical_mapping)에 쓰인 문장은 자동 상속 표현이 아니다)"
    line(json_hits == 0 and (md_hits == 0 if md_hits is not None else True) and tid_attr["sources"] == wid_attr["sources"] and not any("mechanism" in s_ for s_ in tid_attr["sources"]) and "procedure-profiles.json:profiles[].mechanism[]" in {s_ for d_ in dic["dictionaries"] if d_["name"] == "technique" for e_ in d_["entries"] for s_ in [f"{x['file']}:{x['path']}" for x in e_["sources"]]},
         f"K-7 기법 잔재 표현 0 — json(technique.definition · procedure.technique_id/technique_origin 규칙 · procedure 정의 · tuple_rules.technique) 「상속」 {json_hits} · md {md_scope or '빌드 후'} 「상속」 {md_hits if md_hits is not None else '빌드 후'} · technique_id 출처 = what_id 출처(이름 키 {len(tid_attr['sources'])}) · mechanism[] 은 기법 사전(§4) 출처로만")
    # K-8 R29 출처 11
    r29 = next(r for r in erd["relations"] if r["id"] == "R29")
    keys11 = erd.get("r29_taxonomy_safety_keys", [])
    aex = next(e for e in erd["entities"] if e["key"] == "adverse_expression")
    aex_text_src = set(next(a for a in aex["attrs"] if a["name"] == "text")["sources"])
    line(len(keys11) == 11 and all(k_.startswith("taxonomy.json:") and ".extracted.safety." in k_ for k_ in keys11) and set(keys11) <= set(r29["sources"]) and aex_text_src <= set(r29["sources"]) and all(src_exists(k_) for k_ in keys11) and "match_status" in {a["name"] for a in r29["attrs"]},
         f"K-8 R29 출처 {len(r29['sources'])} = v2.2 {len(V2['v22']['erd']['relations'][[r['id'] for r in V2['v22']['erd']['relations']].index('R29')]['sources'])} + taxonomy safety 11(계열 {sum(1 for k_ in keys11 if k_.startswith('taxonomy.json:modality[].extracted'))} · 항목 {sum(1 for k_ in keys11 if 'items[]' in k_)} · 제품 {sum(1 for k_ in keys11 if 'products[]' in k_)}) · adverse_expression.text 출처 {len(aex_text_src)} ⊆ R29 출처 · 11 키 전부 잎 키 존재")
    out.append("")
    # ---- L (v2.4)
    out.append("### L. v2.4 수정 6건 (발주서 erd-v2.4-brief.md · 원칙 A~D)")
    out.append("")
    L_SECTION_MARK = True
    all_rows = comp_rows3 + ex_rows + [dict(r_["patient_ko"], text=r_["patient_ko"]["text"], kind="patient_text") for r_ in ex_rows if r_.get("patient_ko")]
    # L-1 부위 상속 0 · 부위 나열 · 후보 분할 · 보존 · 두통×주사 부위 0
    out_site = [(r_["text"][:30], t[:3]) for r_ in all_rows for t in r_["tuples"] if t[1] and (len(t) < 5 or t[4] not in ("member", "site_list"))]
    merges = [m for r_ in all_rows for m in (r_.get("site_list_merges") or [])]
    bad_merge = [m for m in merges if not m["site_members"] or not m["events"] or len(m["sites"]) < 2]
    splits = [r_ for r_ in all_rows if r_.get("b_splits")]
    bad_split = [r_["text"][:30] for r_ in splits for t in r_["b_splits"] if not (t[3] >= 2 or t[4] >= 2)]
    # 분할: 후보 수만큼 튜플이 실제로 있나
    for r_ in splits:
        for ev in {t[0] for t in r_["b_splits"]}:
            ns = max(t[3] for t in r_["b_splits"] if t[0] == ev) or 1
            nc = max(t[4] for t in r_["b_splits"] if t[0] == ev) or 1
            nq = max((t[6] for t in r_["b_splits"] if t[0] == ev), default=1) or 1
            ev_t = [t for t in r_["tuples"] if t[0] == ev]
            if len({t[1] for t in ev_t if t[1]}) < (ns if ns >= 2 else 0) or len({t[2] for t in ev_t if t[2] != "미상"}) < (nc if nc >= 2 else 0) or len({t[5] for t in ev_t if len(t) > 5 and t[5]}) < (nq if nq >= 2 else 0) or len(ev_t) < ns * nc * nq:
                bad_split.append(r_["text"][:30] + " 후보 수 ≠ 튜플 수")
    unatt = [r_ for r_ in all_rows if r_["extra_sites"] or r_["extra_courses"] or r_.get("extra_qualifiers")]
    bad_unatt = [r_["text"][:30] for r_ in unatt if (r_.get("kind", "complications") == "complications" and r_["event_kind"] != "raw_name") or (r_.get("kind", "complications") != "complications" and r_.get("match_status", "unlinked") != "unlinked")]
    hx = [(r_["text"][:30], t[:3]) for r_ in all_rows for t in r_["tuples"] if t[0] == "두통" and t[1] == "주사 부위"] + [t["id"] for t in TUP["adverse"]["tuples"] if t["event"] == "두통" and t["site"] == "주사 부위"]
    hx_cand = [c["would_be_id"] for r_ in ex_rows for c in (r_.get("candidates_union") or r_["candidates"]) if c["event"] == "두통" and c["site"] == "주사 부위"]
    site_rule = erd.get("site_rule", "")
    sec962b = ("#### 9.6.2b" in md and "멤버 밖(같은 묶음 · outer · 이름 전체)에서 온 site 가 들어간 튜플·후보 **0**" in md and "「두통 × 주사 부위」류 틀린 조합: 튜플·후보 **0**" in md) if md else True
    sec15_site = ("### 1.5" in md and "부위(site) 규칙(v2.4 수정 1" in md and site_rule in md) if md else True
    line(not out_site and as_["site_outside_member"] == 0 and not bad_merge and len(merges) == as_["site_list_merges"] and not bad_split and len(splits) == as_["multi_candidate_splits"] and not bad_unatt and len(unatt) == as_["unattached_fragments_texts"] and not hx and not hx_cand and as_["headache_x_injection_site"] == 0
         and all(x in site_rule for x in ("사건이 놓인 멤버", "멤버 밖", "부위마다 튜플", "extra_sites")) and erd["tuple_rules"]["adverse"].get("site") == site_rule and erd["tuple_rules"]["adverse"].get("site_member_only") is True and sec962b and sec15_site
         and all(t.get("site_basis") in ("member", "site_list") for t in TUP["adverse"]["tuples"] if t["event_kind"] == "dict" and t["site_id"] != "none") and all(t["site_id"] == "none" for t in TUP["adverse"]["tuples"] if t["event_kind"] == "dict" and t.get("site_basis") is None),
         f"L-1 부위 상속 0(2-A′ · 원칙 B·C) — 이름·표현·patient_ko {len(all_rows)} 문자열의 튜플·후보 전수: 멤버 밖에서 온 site {len(out_site)} · 부위 나열 합치기 {len(merges)}(구조 위반 {len(bad_merge)} · 「이마/눈가 당김감」 {sum(1 for m in merges if '이마' in m['sites'] and '눈가' in m['sites'])}) · 후보 둘 이상 분할 {len(splits)}(위반 {len(bad_split)}) · 붙지 않은 조각 보존 {len(unatt)} 문자열(이름→raw_name · 표현→unlinked 위반 {len(bad_unatt)}) · 두통×주사 부위 튜플·후보 {len(hx) + len(hx_cand)} · dict 튜플 site_basis ∈ {{member, site_list}} · json site_rule=tuple_rules.adverse.site · md §1.5 부위 규칙 {sec15_site} · §9.6.2b {sec962b}")
    # L-2 raw_name 칸 none/미상 100%
    raw4 = [t for t in TUP["adverse"]["tuples"] if t["event_kind"] == "raw_name"]
    bad_rawcell = [t["id"] for t in raw4 if t["site_id"] != "none" or t["course"] != "미상" or t["site_kind"] != "none" or t["qualifier_id"] != "none" or t.get("dict_tuples") is None or t.get("raw_reason") not in ("unregistered", "unattached_fragments", "unregistered+unattached_fragments")]
    lop4 = [r_ for r_ in comp_rows3 if "LOP" in r_["text"]]
    lop_raw_ok = bool(lop4) and all(r_["event_kind"] == "raw_name" and r_["tuples"][0][1] is None and r_["tuples"][0][2] == "미상" and {tuple(t[:3]) for t in r_["dict_tuples"]} >= {("통증", None, "미상"), ("통증", None, "지연")} for r_ in lop4)
    raw_rule = erd.get("raw_name_rule", "")
    rc = as_["raw_cells"]
    sec962c = ("#### 9.6.2c" in md and f"site none **{len(raw4)}/{len(raw4)}** · course 미상 **{len(raw4)}/{len(raw4)}**" in md) if md else True
    line(not bad_rawcell and rc["n"] == len(raw4) and rc["site_none"] == len(raw4) and rc["course_unknown"] == len(raw4) and lop_raw_ok and all(x in raw_rule for x in ("course·site 를 주지 않는다", "none", "미상", "dict_tuples")) and erd["tuple_rules"]["adverse"].get("raw_name") == raw_rule and "RAW:<anchor>|none|" in erd["id_rule"]["adverse_effect"] and sec962c and (not md or raw_rule in md),
         f"L-2 raw_name course/site 미상 100%(2-B′) — raw 튜플 {len(raw4)}: site none {rc['site_none']} · course 미상 {rc['course_unknown']} · 위반 {len(bad_rawcell)} · dict_tuples 보존 {rc['with_dict_tuples']} · LOP raw 칸 (none, 미상) · 사전 분해 (통증, 미상)+(통증, 지연) 보존 {lop_raw_ok} · 사유 {rc['by_reason']} · json raw_name_rule=tuple_rules.adverse.raw_name · id_rule RAW:anchor|none|미상 · md §1.5·§9.6.2c {sec962c}")
    # L-3 표현 유래 새 튜플 0 · partial 연결 0 · exact 만 R29
    units = {(t["event_id"], t["site_id"], t["course_id"], t["qualifier_id"]): t["id"] for t in TUP["adverse"]["tuples"] if t["event_kind"] == "dict"}
    new_t = [t["id"] for t in TUP["adverse"]["tuples"] if "complications" not in t["origins"] or not any(s_["origin"] == "complications" for s_ in t["sources"])]
    partial_linked = [r_["text"][:30] for r_ in ex_rows if r_["tuple_ids_union"] and not _clean(r_)]
    bad_cand = []
    for r_ in ex_rows:
        for c in (r_.get("candidates_union") or r_["candidates"]):
            key = (c["event_id"], c["site_id"], c["course_id"])
            key = (c["event_id"], c["site_id"], c["course_id"], c["qualifier_id"])
            if c["exists"] != (key in units) or (c["exists"] and c["unit_id"] != units[key]) or c["would_be_id"] != mkid("ADV", f"{c['event_id']}|{c['site_id']}|{c['course_id']}|{c['qualifier_id']}"):
                bad_cand.append(r_["text"][:30])
        if r_["match_status"] == "exact" and (set(r_["tuple_ids_union"]) != {c["unit_id"] for c in (r_.get("candidates_union") or r_["candidates"])} or r_["unlinked_reasons"]):
            bad_cand.append(r_["text"][:30] + " exact≠후보")
        if r_["match_status"] == "unlinked" and not r_["unlinked_reasons"]:
            bad_cand.append(r_["text"][:30] + " unlinked 사유 없음")
    r29_4 = next(r for r in erd["relations"] if r["id"] == "R29")
    ms_attr = next(a for a in r29_4["attrs"] if a["name"] == "match_status")
    aex4 = next(e for e in erd["entities"] if e["key"] == "adverse_expression")
    aex_attrs = {a["name"]: a for a in aex4["attrs"]}
    expr_rule = erd.get("expression_rule", "")
    sec964 = ("#### 9.6.4" in md and "표현에서 새로 생긴 튜플: **0**" in md and "partial 인데 연결된 표현 **0**" in md) if md else True
    line(not new_t and as_["expressions_new_tuples"] == 0 and as_["expressions_raw_name_tuples"] == 0 and not partial_linked and as_["expressions_partial_linked"] == 0 and not bad_cand and as_["tuples_total"] == as_["complications_distinct_tuples"]
         and ms_attr["type"] == "enum(exact)" and aex_attrs["match_status"]["type"] == "enum(exact|unlinked)" and {"candidates", "unlinked_reasons", "extra_sites", "extra_courses"} <= set(aex_attrs) and erd["enums"].get("adverse_expression.unlinked_reason") == ["unregistered", "unattached_fragments", "no_unit", "no_event"]
         and all(x in expr_rule for x in ("가리키기만", "세 칸 완전 일치", "exact", "unlinked", "candidates", "새 단위")) and erd["tuple_rules"]["adverse"].get("expressions") == expr_rule and erd["tuple_rules"]["adverse"].get("expressions_create_units") is False and sec964 and (not md or expr_rule in md),
         f"L-3 표현 유래 새 튜플 0(2-C′ · 원칙 D) — 튜플 {as_['tuples_total']} = complications 65 유래 {as_['complications_distinct_tuples']}(표현만의 튜플 {len(new_t)}) · 표현 {len(ex_rows)}: exact {as_['expressions_total']['match_status'].get('exact', 0)} · unlinked {as_['expressions_total']['match_status'].get('unlinked', 0)} · partial(미등록·붙지 않은 조각) 인데 연결 {len(partial_linked)} · 후보 exists/would_be_id/exact⇔후보 전부 일치 위반 {len(bad_cand)} · 기존 단위에 없는 후보 단위 {as_['candidate_units_not_existing']} · R29 match_status enum(exact) · adverse_expression.match_status enum(exact|unlinked) + candidates·unlinked_reasons · json expression_rule=tuple_rules.adverse.expressions · md §1.5·§9.6.4 {sec964}")
    # L-4 §5.2 adverse_tuple_assign 대상 문구
    ata = dk["adverse_tuple_assign"]["note"]
    sec52 = ("### 5.2" in md and "표현 레코드 전부(exact 포함" in md.split("### 5.2", 1)[1].split("### 5.3", 1)[0]) if md else True
    line(all(x in ata for x in ("raw_name 튜플 전부", "표현 레코드 전부", "exact 포함")) and "partial/unlinked 표현)" not in ata and sec52 and (not md or "exact 포함" in next(a for a in aex4["attrs"] if a["name"] == "match_status")["rule"]),
         f"L-4 §5.2 adverse_tuple_assign 대상 문구(3-A′) — json note 「raw_name 튜플 전부 · 표현 레코드 전부(exact 포함)」 · md §5.2 {sec52} · §2.15 match_status 규칙에 「exact 도 대상」")
    # L-5 CAT- 계열 코드 = taxonomy 트리 위치 (§1.4·§2.3·§2.4·§5.2) + 실측 일치
    cfr = erd.get("cat_family_rule", "")
    tree_fam = {}
    for m_ in ledgers["taxonomy.json"]["modality"]:
        for sc_ in m_["subcategories"]:
            for it_ in sc_["items"]:
                tree_fam[(m_["id"], it_["name"])] = m_["id"]
    bad_cat = [r_["name"] for r_ in cat if r_["catalog_item_id"] != mkid("CAT", f"{tree_fam.get((r_['family'], r_['name']), '?')}|{r_['name']}")]
    recl = [(m_["id"], it_["name"], it_["reclassified_to"]) for m_ in ledgers["taxonomy.json"]["modality"] for sc_ in m_["subcategories"] for it_ in sc_["items"] if "reclassified_to" in it_]
    recl_ok = all(any(r_["family"] == fam and r_["name"] == nm and r_["catalog_item_id"] == mkid("CAT", f"{fam}|{nm}") for r_ in cat) for fam, nm, _ in recl)
    ex_ok = mkid("CAT", "M9|소프라노티타늄") in {r_["catalog_item_id"] for r_ in cat} and mkid("CAT", "M4|볼뉴머") in {r_["catalog_item_id"] for r_ in cat} and mkid("CAT", "M9|볼뉴머") in {r_["catalog_item_id"] for r_ in cat}

    def sec(md_, head, nxt):
        a0 = md_.find(head)
        b0 = md_.find(nxt, a0 + 5)
        return md_[a0:b0] if a0 >= 0 else ""
    secs5 = {k: ("taxonomy 트리 위치" in sec(md, h, n)) for k, h, n in (("§1.4", "### 1.4 ", "### 1.5 "), ("§2.3", "### 2.3 ", "### 2.4 "), ("§2.4", "### 2.4 ", "### 2.5 "), ("§5.2", "### 5.2 ", "### 5.3 "))} if md else {}
    cat_ent = next(e for e in erd["entities"] if e["key"] == "catalog_item")
    sub_ent = next(e for e in erd["entities"] if e["key"] == "modality_subcategory")
    line(all(x in cfr for x in ("taxonomy 트리 위치", "reclassification", "R2", "CAT- id 는 바꾸지 않는다")) and "taxonomy 트리 위치" in cat_ent["identity"] and "taxonomy 트리 위치" in sub_ent["definition"] and "taxonomy 트리 위치" in dk["reclassification"]["note"] and "taxonomy 트리 위치" in erd["id_rule"]["catalog_item"] and erd["tuple_rules"]["procedure"].get("cat_family") == cfr
         and not bad_cat and recl_ok and ex_ok and (not md or all(secs5.values())),
         f"L-5 CAT- 계열 코드 = taxonomy 트리 위치(3-B′) — json cat_family_rule · id_rule.catalog_item · catalog_item.identity · modality_subcategory 정의 · reclassification 비고 · tuple_rules.procedure.cat_family · md {secs5 or '빌드 후'} · 실측: 분류 항목 {len(cat)} 전부 CAT- = sha256(트리 계열|이름) (위반 {len(bad_cat)}) · reclassified_to 항목 {len(recl)} 도 트리 위치 {recl_ok} · 소프라노 티타늄 M9 · 볼뉴머 M4/M9 {ex_ok}")
    # L-6 site_id 출처 = 이름·참조 키 19 (§2.5 · §2.14)
    sid_attr = next(a for a in pe3["attrs"] if a["name"] == "site_id")
    adv4 = next(e for e in erd["entities"] if e["key"] == "adverse_effect")
    srk = next(a for a in adv4["attrs"] if a["name"] == "site_ref_kind")
    sri = next(a for a in adv4["attrs"] if a["name"] == "site_ref_id")
    v23_sid = next(a for a in next(e for e in V2["v23"]["erd"]["entities"] if e["key"] == "procedure")["attrs"] if a["name"] == "site_id")
    sec25 = sec(md, "### 2.5 ", "### 2.6 ") if md else ""
    sec214 = sec(md, "### 2.14 ", "### 2.15 ") if md else ""
    row25 = next((l_ for l_ in sec25.splitlines() if l_.startswith("| site_id ")), "")
    row214 = next((l_ for l_ in sec214.splitlines() if l_.startswith("| site_ref_id ")), "")
    line(sid_attr["sources"] == wid_attr["sources"] and len(sid_attr["sources"]) == 19 and all(src_exists(s_) for s_ in sid_attr["sources"]) and v23_sid["sources"] == [] and srk["sources"] == sri["sources"] == ["complications.json:categories[].complications[].name"]
         and (not md or ("(파생/ERD 정의)" not in row25 and "taxonomy.json:modality[].subcategories[].items[].name" in row25 and "(파생/ERD 정의)" not in row214 and "complications.json:categories[].complications[].name" in row214)),
         f"L-6 site_id 출처(3-C′) — procedure.site_id 출처 {len(sid_attr['sources'])} = what_id 출처(v2.3 은 {len(v23_sid['sources'])}) · 전부 잎 키 존재 · adverse_effect.site_ref_kind/site_ref_id 출처 = complications 이름 키 · md §2.5·§2.14 행에 「(파생/ERD 정의)」 없음")
    # L-7 사전 값 불변 · 개체·관계 불변
    e24 = V2["v24"]["erd"]
    same_struct = [e["key"] for e in erd["entities"]] == [e["key"] for e in e24["entities"]] and [(r["id"], r["name"], r["to"]) for r in erd["relations"]] == [(r["id"], r["name"], r["to"]) for r in e24["relations"]] and [r["from"] for r in erd["relations"] if r["id"] != "R5"] == [r["from"] for r in e24["relations"] if r["id"] != "R5"]
    line(same_struct and len(erd["entities"]) == 21 and len(erd["relations"]) == 31 and len(dic["dictionaries"]) == 47 and dic.get("values_changed_from_v2_4"),
         f"L-7(v3) 개체·관계 구조 = v2.4(개체 {len(erd['entities'])} · 관계 {len(erd['relations'])} · 키·이름·끝 같음 · R5 from 만 확장) · 사전 {len(dic['dictionaries'])} = 46 + adverse_qualifier · 값 변경은 json values_changed_from_v2_4 에 셋뿐(M-11 이 전수 대조)")
    # L-8 원칙 A~D 문장(발주서 그대로)
    PR = {"A": "미상 칸이 하나라도 있으면 다른 이름과 접지 않는다.", "B": "조각을 버리지 않는다. 한 칸에 후보가 둘이면 단위를 둘로 나누거나(부위 「이마/눈가」→ 둘) 미해결로 둔다.",
          "C": "수식어(경과·부위)는 **같은 멤버 안에서 바로 붙은 사건**에만 준다. 이름 전체에서 끌어오지 않는다.", "D": "표현(adverse_expression)은 단위를 **가리키기만** 한다. 표현에서 새 단위를 만들지 않는다."}
    pj = {p_["key"]: p_["text"] for p_ in erd.get("principles", [])}
    tp = {p_["key"]: p_["text"] for p_ in erd["tuple_rules"].get("principles", [])}
    sec15 = sec(md, "### 1.5 ", "## 2. ") if md else ""
    line(pj == PR and tp == PR and (not md or all(v_ in sec15 for v_ in PR.values())) and json.dumps(TUP.get("principles"), ensure_ascii=False) == json.dumps(PR, ensure_ascii=False),
         f"L-8 원칙 A~D 문장 — json principles·tuple_rules.principles·tuples.json principles = 발주서 문장 그대로 {pj == PR and tp == PR} · md §1.5 에 네 문장 {all(v_ in sec15 for v_ in PR.values()) if md else '빌드 후'}")
    # L-9 K-5/K-6 와의 정합: 접힘 0 · course 멤버만 유지
    line(as_["folded_with_partial_name"] == 0 and as_["complications_folded_with_unregistered"] == 0 and as_.get("course_member_only") is True and as_.get("site_member_only") is True and as_.get("expressions_create_units") is False,
         f"L-9 v2.3 규칙 유지 — 미등록 포함 접힘 {as_['folded_with_partial_name']} · course_member_only {as_.get('course_member_only')} · site_member_only {as_.get('site_member_only')} · expressions_create_units {as_.get('expressions_create_units')}")

    # ---- M (v3 · 발주서 10건)
    out.append("### M. v3 변경 10건 (발주서 erd-v3-brief.md · 각각 반영 여부 + 실측) + 브론즈 2판 + 사용자 정의 3·명시 예외")
    out.append("")
    import erd_spec_v3 as S3  # noqa
    rr2 = erd["resolve_rules"]["step2_decompose"]
    rr3 = erd["resolve_rules"]["step3_assemble"]
    TR = erd["tuple_rules"]
    AE = next(e for e in erd["entities"] if e["key"] == "adverse_effect")
    AX = next(e for e in erd["entities"] if e["key"] == "adverse_expression")
    SI = next(e for e in erd["entities"] if e["key"] == "site")
    PR = next(e for e in erd["entities"] if e["key"] == "product")
    TE = next(e for e in erd["entities"] if e["key"] == "technique")
    R5 = next(r for r in erd["relations"] if r["id"] == "R5")
    R12 = next(r for r in erd["relations"] if r["id"] == "R12")
    R29m = next(r for r in erd["relations"] if r["id"] == "R29")
    aattr = {a["name"]: a for a in AE["attrs"]}
    xattr = {a["name"]: a for a in AX["attrs"]}
    def secm(head, nxt):
        return sec(md, head, nxt) if md else ""
    # M-1 V3-1
    ql = D.get("adverse_qualifier", {"entries": []})["entries"]
    ql_ok = len(ql) == 5 and {e["canonical"] for e in ql} == {"공기", "필러", "지방", "혈전", "역행성"} and all(e.get("kind") in ("물질", "기전") and e["sources"] and all(s_["kind"] == "derived" for s_ in e["sources"]) for e in ql)
    ev24 = next(d for d in V2["v24"]["dic"]["dictionaries"] if d["name"] == "adverse_event_type")
    syn24 = {s_["value"] for e in ev24["entries"] if e["canonical"] == "색전" for s_ in e["synonyms"]}
    syn3 = {s_["value"] for e in D["adverse_event_type"]["entries"] if e["canonical"] == "색전" for s_ in e["synonyms"]}
    ps3 = TUP["procedure"]["summary"]
    cmpv = as_.get("v24_comparison") or {}
    TA = TUP["adverse"]["tuples"]
    q_bad = [t["id"] for t in TA if (t["qualifier"] and t.get("qualifier_basis") not in ("member", "prefix_split")) or (t["event_kind"] == "raw_name" and t["qualifier_id"] != "none")]
    cand_q_bad = [r_["text"][:30] for r_ in ex_rows for c in (r_.get("candidates_union") or r_["candidates"]) if c["qualifier"] and c.get("qualifier_basis") not in ("member", "prefix_split")]
    raw_air = [t for t in TA if t["event_kind"] == "raw_name" and "공기색전" in t["event"]]
    air_ok = bool(raw_air) and any(tuple(x[:4]) == ("색전", None, "미상", "공기") for x in raw_air[0]["dict_tuples"]) and ("공기색전", "공기", "색전") in [tuple(x) for x in as_["prefix_splits"]]
    sec967 = "#### 9.6.7" in md if md else True
    line(ql_ok and "공기색전" in syn24 and "공기색전" not in syn3 and {"qualifier", "qualifier_id", "qualifier_basis", "extra_qualifiers"} <= set(aattr) and "qualifier" in xattr["candidates"]["type"] and "extra_qualifiers" in xattr and "qualifier_id" in erd["id_rule"]["adverse_effect"]
         and erd.get("qualifier_rule") == TR["adverse"].get("qualifier") and "수식 칸" in erd["adverse_fold_rule"] and TR["adverse"].get("qualifier_none_is_value") is True and erd["enums"].get("adverse_qualifier.kind") == ["물질", "기전"] and "qualifier" in next(a for a in R29m["attrs"] if a["name"] == "matched_fragments")["type"]
         and not q_bad and not cand_q_bad and air_ok and sec967 and (not md or erd["qualifier_rule"] in md),
         f"M-1 V3-1 수식 칸 — 사전 adverse_qualifier {len(ql)}(물질 {sum(1 for e in ql if e.get('kind') == '물질')} · 기전 {sum(1 for e in ql if e.get('kind') == '기전')} · 출처 derived) · 사건 동의어 「공기색전」 v2.4 {'있음' if '공기색전' in syn24 else '없음'} → v3 {'제거' if '공기색전' not in syn3 else '남음'} · adverse_effect qualifier/qualifier_id/qualifier_basis/extra_qualifiers · 표현 candidates 네 칸 · id_rule 네 칸 · json qualifier_rule=tuple_rules.adverse.qualifier · 접힘 규칙에 수식 칸 · R29 matched_fragments · 실측: 멤버 밖 수식 {len(q_bad) + len(cand_q_bad)} · raw qualifier none · 「공기색전」→ 공기+색전 {air_ok}(dict_tuples 보존) · qualifier≠none 튜플 {as_['qualifier_tuples']} · md §9.6.7 {sec967}")
    line(cmpv.get("dict_fold_groups_same") is True and cmpv.get("raw_names_same") is True and cmpv.get("exact_v24") == cmpv.get("exact_v3") == as_["expressions_total"]["linked"] and not cmpv.get("match_status_diff") and not cmpv.get("linked_units_diff") and cmpv.get("tuples_v24") == cmpv.get("tuples_v3") == as_["tuples_total"],
         f"M-1′ 수식 칸이 기존 접힘·표현 연결을 깨지 않는다 — v2.4 대조: 사전 튜플 접힘 그룹 {cmpv.get('dict_fold_groups_v24')} = {cmpv.get('dict_fold_groups_v3')} 같음 {cmpv.get('dict_fold_groups_same')} · raw 이름 {cmpv.get('raw_names_v24')} = {cmpv.get('raw_names_v3')} · exact {cmpv.get('exact_v24')} = {cmpv.get('exact_v3')} · match_status 바뀐 표현 {len(cmpv.get('match_status_diff', []))} · 연결 단위 바뀐 표현 {len(cmpv.get('linked_units_diff', []))} · 튜플 {cmpv.get('tuples_v24')} = {cmpv.get('tuples_v3')}")
    # M-2 V3-2
    cp = ps3["company_paren"]
    applied_refs = [r_ for r_ in ref_rows if str(r_.get("what_basis", "")).startswith("company_paren")] + [r_ for r_ in cat if str(r_.get("what_basis", "")).startswith("company_paren")]
    line("company_paren" in rr2 and rr2["company_paren"]["rule"] == erd.get("company_paren_rule") == TR["procedure"].get("company_paren") and cp["candidates"] >= 9 and len(cp["botox_allergan_sites"]) == 9 and all(c["touches"] == "-" for c in cp["botox_allergan_sites"]) and cp["applied_n"] == len(applied_refs) and cp["touch_manufacturer"] + cp["touch_product"] + cp["no_touch"] == cp["candidates"] and ("#### 9.5.9" in md if md else True),
         f"M-2 V3-2 괄호 안 회사·제품 — 규칙 데이터 resolve_rules.company_paren=tuple_rules.procedure.company_paren · 후보 전수 {cp['candidates']}(회사 닿음 {cp['touch_manufacturer']} · 제품 닿음 {cp['touch_product']} · 안 닿음 {cp['no_touch']}) · 「보톡스(엘러간)」·「더모톡신」 자리 {len(cp['botox_allergan_sites'])} 전부 사전에 안 닿음(엘≠앨) · 적용 {cp['applied_n']} = what_basis company_paren 인 항목·참조 {len(applied_refs)} · md §9.5.9")
    # M-3 V3-3
    sw = rr2.get("stopwords", {})
    words = sw.get("words", [])
    st3 = ps3["stopwords"]
    brief12 = ["회", "차", "터치업", "유지", "집중", "연말", "하반기", "가을", "관리", "케어", "과도한", "빈도"]
    no_loc = [w["word"] for w in words if not w.get("locators")]
    in_dic = [w["word"] for w in st3["words"] if w["in_dictionary"]]
    swset = {norm(w["word"]) for w in words}
    leak = [(r_["label"], u) for r_ in ref_rows for u in r_.get("unregistered", []) if norm(u) in swset] + [(r_["name"], u) for r_ in cat for u in r_.get("unregistered", []) if norm(u) in swset]
    r12a = {a["name"] for a in R12["attrs"]}
    line(words and len(words) == 19 and set(brief12) <= {w["word"] for w in words} and not no_loc and not in_dic and not leak and {"session_index", "qualifier_text", "member_mode", "alternatives"} <= r12a and all("qualifier_text" in {a["name"] for a in next(r for r in erd["relations"] if r["id"] == rid)["attrs"]} for rid in ("R9", "R17", "R18"))
         and st3["unregistered_total_after"] <= st3["unregistered_total_before"] and st3["unregistered_distinct_after"] <= st3["unregistered_distinct_before"] and erd.get("stopword_rule") == sw.get("rule") == TR["procedure"].get("stopwords") and ("#### 9.5.10" in md if md else True),
         f"M-3 V3-3 stopwords — 규칙 데이터 단어 {len(words)}(발주서 12 전부 + 원장 실측 {len(words) - 12}) · locator 없는 단어 {len(no_loc)}{no_loc or ''} · 사전 값과 겹침 {len(in_dic)} · 미등록 조각에 새어 나온 stopword {len(leak)} · 전후 distinct {st3['unregistered_distinct_before']}→{st3['unregistered_distinct_after']} · 총 {st3['unregistered_total_before']}→{st3['unregistered_total_after']} · R12 session_index/qualifier_text · R9/R17/R18 qualifier_text · md §9.5.10")
    # M-4 V3-4
    cb = ps3["combo_labels_all"]
    plus4 = ps3["combo_plus_v2"]
    mt = [r_ for r_ in ref_rows if r_["result"] == "multi_tuple"]
    TT4 = {t["id"]: t for t in TUP["procedure"]["tuples"]}
    bad_mt = [r_["label"] for r_ in mt if len(r_["member_ids"]) != len(r_["sites"]) or len(r_["sites"]) < 2 or r_["member_mode"] != "and" or len({TT4[x]["what_id"] for x in r_["member_ids"]}) != 1 or any(not str(TT4[x]["anchor"]).endswith(f"#s{i}") for i, x in enumerate(r_["member_ids"])) or sorted(TT4[x]["site"] for x in r_["member_ids"]) != sorted(r_["sites"])]
    alt = [r_ for r_ in ref_rows if r_.get("alternatives")]
    bad_alt = [r_["label"] for r_ in alt if r_["result"] != "tuple" or r_.get("member_mode") != "or" or len(r_["alternatives"]) < 2]
    cr = [r_ for r_ in ref_rows if r_["result"] == "combo_ref"]
    bad_cr = [r_["label"] for r_ in cr if r_.get("member_mode") not in ("and", "or")]
    ms_left = [r_["label"] for r_ in ref_rows if r_.get("unresolved_reason") == "multi_site" and any(ch in str(r_["label"]) for ch in "+/")]
    slash_opt_seq = [c for c in cb if "/" in c["label"] and c["slot"].startswith(("treatment-optimization", "treatment-sequence"))]
    plus_v1 = {c["label"]: c["v1_name"] for c in plus4}
    line("combo" in rr3 and rr3["combo"]["rule"] == erd.get("combo_rule") == TR["procedure"].get("combo") and "member_mode" in r12a and erd["enums"].get("R12.member_mode") == ["and", "or"] and "member_mode" in next(e for e in erd["entities"] if e["key"] == "package")["definition"]
         and len(plus_v1) == 4 and set(plus_v1) == {"보톡스(턱선+광대)", "보톡스 이마+미간", "필러 볼+턱", "필러 팔자+볼"} and all(plus_v1[k] for k in plus_v1) and len(cb) >= 16 and len(slash_opt_seq) >= 12
         and not bad_mt and len(mt) == ps3["reference_total"]["multi_tuple"] and ps3["edge_ends_multi_tuple"] == len(mt) and not bad_alt and not bad_cr and not ms_left and ("#### 9.5.11" in md if md else True),
         f"M-4 V3-4 조합 기호 — 규칙 데이터 resolve_rules.step3_assemble.combo=tuple_rules.procedure.combo · R12 member_mode(enum and|or) · 실측 `+`/`/` 라벨 전수 {len(cb)}(treatment-optimization·sequence 의 `/` {len(slash_opt_seq)} ≥ 12 · 2판 `+` 4곳 전부 1판 이름 대조) · 「무엇을 하나 × 부위 여럿」 {len(mt)}(구조 위반 {len(bad_mt)} · 엣지 끝 multi_tuple {ps3['edge_ends_multi_tuple']}) · 괄호 안 대안 {len(alt)}(위반 {len(bad_alt)}) · combo_ref member_mode 없음 {len(bad_cr)} · 기호가 있는데 multi_site 로 남은 참조 {len(ms_left)} · md §9.5.11")
    # M-5 V3-5
    site3 = D["site"]["entries"]
    layers = [e for e in site3 if e.get("kind") == "layer"]
    kinds_ok = all(e.get("kind") in ("anatomical", "relative", "layer", "region") for e in site3)
    site24 = next(d for d in V2["v24"]["dic"]["dictionaries"] if d["name"] == "site")["entries"]
    first21 = [(e["canonical"], tuple(s_["value"] for s_ in e["synonyms"])) for e in site3[:21]] == [(e["canonical"], tuple(s_["value"] for s_ in e["synonyms"])) for e in site24]
    lay_src = all(e["sources"] and all(s_["kind"] == "derived" for s_ in e["sources"]) and e.get("site_kind") == "layer" for e in layers)
    line(kinds_ok and len(layers) == 5 and {e["canonical"] for e in layers} == {"피부", "피하 지방층", "근육", "혈관", "점막"} and lay_src and first21 and len(site3) == 26 and "kind" in {a["name"] for a in SI["attrs"]} and erd["enums"].get("site.kind") == ["anatomical", "relative", "layer", "region"] and erd.get("site_kind_rule")
         and ps3["tuples_layer_site"] == 0 and len(D["relative_site"]["entries"]) == 2 and all(t.get("site_dict_kind") in (None, "relative", "anatomical", "layer", "region") for t in TA) and ("#### 9.6.8" in md if md else True),
         f"M-5 V3-5 부위 kind — site {len(site3)} = v2.4 21(값·순서 그대로 {first21}) + layer 5({', '.join(e['canonical'] for e in layers)} · 출처 derived {lay_src}) · 값마다 kind ∈ 4 {kinds_ok}(분포 {as_['site_dictionary_by_kind']}) · site.kind 속성 · enum · relative_site 2 불변 · 시술 site 칸의 layer {ps3['tuples_layer_site']} · 부작용 layer 튜플 {as_['layer_site_tuples']} · 후보 {as_['layer_site_candidates']} · md §9.6.8")
    # M-6 V3-6
    dk3 = {k["kind"]: k for k in erd["decision_kinds"]}
    cr6 = dk3.get("canonical_rename")
    ao3 = erd["decision_apply_order"]
    line(cr6 is not None and cr6["build_reads"] and cr6.get("new_in_v3") and all(x in (cr6["target"] + cr6["new_value"]) for x in ("dictionary", "canonical", "old_as_synonym", "is_marketing_name")) and "canonical_rename" in erd["enums"]["decision.kind"] and len(erd["enums"]["decision.kind"]) == 17 and "canonical_rename" in ao3[0]["kinds"] and ao3[0]["stage"] == "①" and "canonical_rename" in erd["decision_apply_order_rule"] and erd.get("rename_rule") and ("canonical_rename" in secm("### 5.2 ", "### 5.3 ") if md else True),
         f"M-6 V3-6 canonical_rename — kind 17(신설 1) · build_reads · target(dictionary·code·canonical) · new_value(canonical·old_as_synonym·is_marketing_name) · 적용 ① {ao3[0]['kinds']} · md §5.2")
    # M-7 V3-7
    pa7 = {a["name"]: a for a in PR["attrs"]}
    ta7 = {a["name"]: a for a in TE["attrs"]}
    line({"description", "media_refs"} <= set(pa7) and {"description", "media_refs"} <= set(ta7) and all("locator" in pa7["description"]["rule"] and "sha256" in x["media_refs"]["type"] for x in (pa7, ta7)) and erd["enums"].get("media_refs.kind") == ["photo", "diagram", "video", "document"] and erd.get("media_rule") and ("media_refs" in secm("### 2.6 ", "### 2.7 ") and "media_refs" in secm("### 2.7 ", "### 2.8 ") if md else True),
         "M-7 V3-7 description·media_refs — product·technique 속성(출처 locator 필수 · path·sha256·captured_at·source·kind) · enum media_refs.kind · md §2.6(product)·§2.7(technique)")
    # M-8 V3-8
    inh3 = TUP["procedure"]["inheritance_candidates"]
    line(R5["from"] == "modality|modality_subcategory" and "basis" in {a["name"] for a in R5["attrs"]} and erd.get("r5_subcategory_rule") and inh3 and all(c.get("by_subcategory") and sum(b["catalog_items"] for b in c["by_subcategory"]) == c["catalog_items"] and all(b["from_ref"].startswith("R5:") for b in c["by_subcategory"]) for c in inh3) and any(c["from_ref"] == "R5:M16" and len(c["by_subcategory"]) >= 2 for c in inh3) and ("하위분류" in secm("#### 9.5.6", "#### 9.5.7") if md else True),
         f"M-8 V3-8 기법 상속 하위분류 단위 — R5 from {R5['from']} · basis · 후보 {len(inh3)} 계열 전부 하위분류별 scope(항목 수 합 일치) · M16 수액(R5 기법 intravenous 하나 · 하위분류 {next((len(c['by_subcategory']) for c in inh3 if c['from_ref'] == 'R5:M16'), 0)} — 하위분류별 지정 자리) · R5 기법 둘 이상·없음 계열 {ps3['families_without_single_technique']} · md §9.5.6")
    # M-9 V3-9
    line(all("미해결" in dk3[k]["note"] or "V3-9" in dk3[k]["note"] for k in ("tuple_assign", "tuple_assign_multi", "adverse_tuple_assign")) and "미해결" in erd.get("decision_target_rule", "") and erd.get("decision_anchor_rule") and "거부하지 않는다" in erd["decision_anchor_rule"] and (erd["decision_anchor_rule"] in md if md else True),
         "M-9 V3-9 결정 적용 대상 확장 — tuple_assign·tuple_assign_multi·adverse_tuple_assign 비고 · target 규칙(미해결·조합 REF-) · 빌더 규칙 문장(anchor 부재로 거부하지 않는다) · md §5")
    # M-10 V3-10
    q7 = next(q for q in erd["quality_rules"] if q["no"] == "⑦")["rule"]
    cst = next(a for a in next(e for e in erd["entities"] if e["key"] == "conflict")["attrs"] if a["name"] == "status")["rule"]
    line("fold_approve" in q7 and "resolved" in q7 and "⑦" in dk3["fold_approve"]["note"] and "fold_approve" in cst and erd.get("fold_close_rule") and (erd["fold_close_rule"] in md if md else True),
         "M-10 V3-10 fold_approve 가 ⑦ 을 닫는다 — 규칙 ⑦ 문장 · fold_approve 비고 · conflict.status 비고 · fold_close_rule · md §5")
    # M-11 사전 값 변경 셋뿐
    d24 = {d["name"]: d for d in V2["v24"]["dic"]["dictionaries"]}
    d3 = {d["name"]: d for d in dic["dictionaries"]}
    strip = lambda e: {k: v for k, v in e.items() if k not in ("kind", "layer_note", "v3_removed_synonyms")}  # noqa
    same_other = all(json.dumps([strip(e) for e in d3[n]["entries"]], ensure_ascii=False, sort_keys=True) == json.dumps([strip(e) for e in d24[n]["entries"]], ensure_ascii=False, sort_keys=True) and d3[n]["candidates"] == d24[n]["candidates"] for n in d24 if n not in ("site", "adverse_event_type"))
    site_same21 = json.dumps([strip(e) for e in d3["site"]["entries"][:21]], ensure_ascii=False, sort_keys=True) == json.dumps([strip(e) for e in d24["site"]["entries"]], ensure_ascii=False, sort_keys=True)
    ev_same = all(json.dumps(strip(a), ensure_ascii=False, sort_keys=True) == json.dumps(strip(b), ensure_ascii=False, sort_keys=True) for a, b in zip(d3["adverse_event_type"]["entries"], d24["adverse_event_type"]["entries"]) if a["canonical"] != "색전") and len(d3["adverse_event_type"]["entries"]) == len(d24["adverse_event_type"]["entries"])
    ev_diff = syn24 - syn3
    line(same_other and site_same21 and ev_same and ev_diff == {"공기색전"} and set(d3) - set(d24) == {"adverse_qualifier"} and dic.get("values_changed_from_v2_4"),
         f"M-11 사전 값 변경은 셋뿐 — v2.4 46 사전 중 site·adverse_event_type 밖 44 개 값·동의어·후보 동일 {same_other} · site 앞 21 동일 {site_same21}(+layer 5) · 사건 사전 동일 {ev_same}(색전 동의어 차이 {sorted(ev_diff)}) · 새 사전 {sorted(set(d3) - set(d24))}")
    # M-12 사용자 정의 3 + 명시 예외
    frozen = open(os.path.join(HERE, "ERD-FROZEN.md"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, "ERD-FROZEN.md")) else ""
    ud = erd.get("user_definitions", [])
    ud_ok = len(ud) == 3 and all(u["text"] in frozen for u in ud) and erd.get("explicit_exception", "").split(" v3:")[0].strip() in frozen.replace("**", "")
    sec0 = secm("### 0. ", "**원칙(") if md else ""
    line(ud_ok and (not md or all(u["text"] in sec0 for u in ud)) and "명시 예외" in erd.get("user_definitions_v3_note", "") and TR.get("user_definitions") and TR.get("explicit_exception") and "none·미상은 값" not in "" and as_.get("qualifier_none_is_value") is True and TUP.get("qualifier_none_is_value") is True,
         f"M-12 사용자 정의 3 과 명시 예외 유지 — 정의 3 문장 = ERD-FROZEN 동결 조건 문장 {ud_ok} · 명시 예외 문장 = ERD-FROZEN(v3 덧말 제외) · json user_definitions·explicit_exception·tuple_rules 에 같은 문장 · 부작용 none·미상·qualifier none 은 값(tuples.json qualifier_none_is_value) · md §0")
    # M-13 2판 잎 키·해시 요약
    line(erd.get("bronze_version") == 2 and erd["bronze"]["mismatch"] == [] and rescan3.get("leaf_count_v2") == rescan3.get("leaf_count_v1") == 573 and not rescan3.get("diff"),
         f"M-13 브론즈 2판 — HASHES.txt 불일치 {len(erd['bronze']['mismatch'])} · 2판 잎 키 {rescan3.get('leaf_count_v2')} = 1판 {rescan3.get('leaf_count_v1')} · 파일별 차이 {len(rescan3.get('diff', {}))} · 바뀐 파일 {erd['bronze']['changed_from_v1']}")
    out.append("")
    out.append(f"**종합: {'PASS' if ok_all else 'FAIL'}** (NOTE {len(notes)}) — 잎 키 {len(rows)}/{n_ledger + n_s1} 행선지 확정(미정 0 · v2.4 대비 이동 0 · 비고 변경 {len(erd.get('column_map_note_changes_v3', []))} · 2판 잎 키 = 1판) · 사전 값 출처 100% · ERD 출처 키 100% · 브론즈 2판 sha256 21 + HASHES.txt + step1 일치 · 분해 규칙 재현 일치 · 튜플 실측 재현 일치 · 구조 v2.4 그대로(R5 from 확장) · v2.1~v2.4 항목 유지 · v3 10건 각각 반영·실측(수식 칸이 접힘·exact 를 깨지 않음 · `+`/`/` 전수 · stopwords locator · 회사 괄호 후보 전수 · 조직층 5 · kind 17 · R5 하위분류 · anchor 확장 · ⑦ 닫음) · 사전 값 변경 셋뿐 · 사용자 정의 3 + 명시 예외 유지" + (" · NOTE: " + " / ".join(notes) if notes else ""))
    return ok_all, "\n".join(out)


if __name__ == "__main__":
    ok, rep = run_checks()
    print(rep)
    sys.exit(0 if ok else 1)
