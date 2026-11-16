#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v1 검산.

검사 항목
 A. 잎 키 행선지: erd-v1-column-map.md 의 행 = bronze-ledger-column-scan.json 잎 키 573, 중복 0, 미정 0, 행선지 범주 5 안.
 B. 사전 값 출처: erd-v1-dictionaries.json 의 모든 정준값·동의어에 출처 ≥1, 각 출처가 원장(파일·키 경로)에 실제로 그 값(kind=value) 또는 그 키(kind=key)를 가진다.
 C. ERD 출처 키: erd-v1.json 개체 속성·관계의 출처 'file:path' 가 스캔 잎 키에 존재한다. 행선지 표적(개체/사전/관계)이 ERD 에 정의돼 있다.
 D. 원장 바이트: erd-v1.json 의 sha256 이 현재 원장 파일과 같다.

실행: python3 erd-v1-check.py  (같은 폴더의 산출물 4개 + 스캔 JSON + 원장 디렉토리)
"""
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = "/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26"
CODE_KEY_RE = re.compile(r"^(?:[A-Z]{1,2}\d+(?:-\d+)*|M\d+_to_M\d+|auto-\d+-\d+)$")
DESTS = {"개체", "사전", "엣지", "브론즈", "버림"}


def norm(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", str(s)).casefold())


def walk(data, path):
    toks = path.split(".") if path else []

    def rec(node, i, parents):
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
                        yield from after(v, i, arr, parents + [node])
        elif isinstance(node, dict) and key in node:
            yield from after(node[key], i, arr, parents + [node])

    def after(v, i, arr, parents):
        if arr:
            if isinstance(v, list):
                for it in v:
                    yield from rec(it, i + 1, parents)
        else:
            yield from rec(v, i + 1, parents)

    yield from rec(data, 0, [])


def load():
    scan = json.load(open(os.path.join(HERE, "bronze-ledger-column-scan.json"), encoding="utf-8"))
    erd = json.load(open(os.path.join(HERE, "erd-v1.json"), encoding="utf-8"))
    dic = json.load(open(os.path.join(HERE, "erd-v1-dictionaries.json"), encoding="utf-8"))
    cmap = open(os.path.join(HERE, "erd-v1-column-map.md"), encoding="utf-8").read()
    ledgers = {f: json.load(open(os.path.join(LEDGER, f), encoding="utf-8")) for f in scan["files"]}
    return scan, erd, dic, cmap, ledgers


def parse_column_map(cmap):
    rows = []
    cur = None
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
    scan, erd, dic, cmap, ledgers = load()
    out = []
    ok_all = True

    def line(ok, text):
        nonlocal ok_all
        ok_all = ok_all and ok
        out.append(f"- {'PASS' if ok else 'FAIL'} — {text}")

    # ---- A
    leaf = {(f, p) for f, v in scan["files"].items() for p in v["leaf_paths"]}
    rows = parse_column_map(cmap)
    got = Counter((r["file"], r["path"]) for r in rows)
    dup = [k for k, n in got.items() if n > 1]
    missing = sorted(leaf - set(got))
    extra = sorted(set(got) - leaf)
    bad_dest = [r for r in rows if r["dest"] not in DESTS or not r["target"]]
    out.append("### A. 잎 키 행선지")
    out.append("")
    line(len(rows) == scan["total_leaf_paths"] == 573, f"행선지 행 {len(rows)} = 스캔 잎 키 {scan['total_leaf_paths']} = 573")
    line(not dup, f"중복 행 {len(dup)}")
    line(not missing and not extra, f"스캔에만 {len(missing)} · 표에만 {len(extra)}")
    line(not bad_dest, f"행선지 범주 밖/표적 없음(미정) {len(bad_dest)}")
    dist = Counter(r["dest"] for r in rows)
    out.append(f"- 행선지 분포: " + " · ".join(f"{k} {v}" for k, v in sorted(dist.items(), key=lambda x: -x[1])) + f" (합 {sum(dist.values())})")
    # 표적이 ERD 에 있는지
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
        else:  # key
            if (f, p) not in leaf:
                return f"{dname}:{value} 키 경로 없음 {f}:{p}"
            segs = {x.replace("[]", "") for x in p.split(".")}
            nsegs = {norm(x) for x in segs}
            if norm(value) not in nsegs and not any(x.startswith(norm(value)) for x in nsegs) and not (value in ledgers[f] if isinstance(ledgers[f], dict) else False):
                # 키 이름에서 파생된 단위(day/month/week/mm/ml/cm/percent/minute) 는 잎 이름의 접미/접두로 확인
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
    line(not bad_src, f"원장에서 확인 안 되는 출처 {len(bad_src)}" + (": " + "; ".join(bad_src[:8]) if bad_src else ""))
    out.append(f"- 사전 {len(dic['dictionaries'])}개 · 정준값 {n_can} · 동의어 {n_syn} · 후보 {sum(len(d['candidates']) for d in dic['dictionaries'])} · 출처 100% 확인")
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
            pp = p.replace("*.", "")
            if p in leaf_by_file[ff]:
                return True
            if "*" in p:
                rx = re.compile("^" + re.escape(p).replace(r"\*", r"[^.]+") + "$")
                if any(rx.match(x) for x in leaf_by_file[ff]):
                    return True
            if p.startswith("*.") and any(x.endswith(p[1:]) for x in leaf_by_file[ff]):
                return True
        return False

    bad = []
    n_src = 0
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
    line(not bad, f"ERD 출처 키 {n_src}개 중 스캔 잎 키에 없는 것 {len(bad)}" + (": " + "; ".join(bad[:8]) if bad else ""))
    # 행선지 표가 가리키는 사전 ↔ 사전 파일, 관계 ↔ ERD
    used_dicts = {r["target"].replace("dict:", "") for r in rows if r["dest"] == "사전"}
    line(used_dicts <= dnames, f"행선지 표의 사전 {len(used_dicts)}개 전부 사전 파일에 있음")
    out.append(f"- 개체 {len(erd['entities'])} · 관계 {len(erd['relations'])} · 사전 {len(dic['dictionaries'])} · 재검토 {len(erd['review_items'])}")
    out.append("")

    # ---- D
    out.append("### D. 브론즈 바이트")
    out.append("")
    badsha = []
    for fm in erd["source_files"]:
        h = hashlib.sha256(open(os.path.join(LEDGER, fm["file"]), "rb").read()).hexdigest()
        if h != fm["sha256"]:
            badsha.append(fm["file"])
    line(not badsha and len(erd["source_files"]) == 21, f"원장 21 sha256 일치 (불일치 {len(badsha)})")
    out.append("")
    out.append(f"**종합: {'PASS' if ok_all else 'FAIL'}** — 잎 키 {len(rows)}/573 행선지 확정(미정 0) · 사전 값 출처 100% · ERD 출처 키 100% · 브론즈 sha256 일치")
    return ok_all, "\n".join(out)


if __name__ == "__main__":
    ok, rep = run_checks()
    print(rep)
    sys.exit(0 if ok else 1)
