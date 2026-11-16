# -*- coding: utf-8 -*-
"""입력 적재 — 브론즈 22(원장 21 + step1) · ERD · 사전 · 잎 키 행선지 표. SHA256 이 ERD 와 다르면 빌드 거부."""
import json
import os
import re

from .util import sha256_file


class BuildRefused(Exception):
    pass


def bronze_hashes(bronze_dir):
    """브론즈 폴더의 HASHES.txt(`<sha256 앞자리> <파일>`) → {파일: 앞자리}. 없으면 None(1판 — ERD source_files 해시로 검증)."""
    p = os.path.join(bronze_dir, "HASHES.txt")
    if not os.path.exists(p):
        return None
    out = {}
    with open(p, encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2 and re.fullmatch(r"[0-9a-f]{8,64}", parts[0]):
                out[parts[1]] = parts[0]
    return out


def bronze_info(bronze_dir):
    """HASHES.txt 가 있는 브론즈만 — {dir, version(CHANGELOG 최신 판), hashes_file}. 없으면 None(manifest 에 넣지 않는다 · 1판 바이트 동일)."""
    if bronze_hashes(bronze_dir) is None:
        return None
    ver = None
    cl = os.path.join(bronze_dir, "CHANGELOG.md")
    if os.path.exists(cl):
        with open(cl, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^\|\s*(\d+)\s*\|", line)
                if m:
                    ver = max(ver or 0, int(m.group(1)))
    name = os.path.basename(os.path.normpath(bronze_dir))
    return {"dir": name, "version": ver, "label": f"{name} 판 {ver}", "hashes_file": "HASHES.txt", "hashes_sha256": sha256_file(os.path.join(bronze_dir, "HASHES.txt"))}


def expected_hash(erd_source, hashes):
    """기대 해시 — 원장(ledger)은 HASHES.txt 가 있으면 그 앞자리, 없으면 ERD 해시. step1(research_artifact)은 늘 ERD 해시."""
    if erd_source["kind"] == "research_artifact" or hashes is None:
        return erd_source["sha256"], "ERD"
    return hashes.get(erd_source["file"]), "HASHES.txt"


def hash_ok(h, want):
    return want is not None and h.startswith(want) and len(want) >= 8


def load_bronze(erd, bronze_dir, step1_path):
    """22 의 sha256 대조 — 원장 21 은 브론즈 폴더 HASHES.txt(있으면) 또는 erd.source_files, step1 은 erd. 하나라도 다르거나 없으면 BuildRefused."""
    L, meta, errors = {}, {}, []
    hashes = bronze_hashes(bronze_dir)
    for s in erd["source_files"]:
        p = step1_path if s["kind"] == "research_artifact" else os.path.join(bronze_dir, s["file"])
        if not os.path.exists(p):
            errors.append(f"{s['file']}: 파일 없음 ({p})")
            continue
        h = sha256_file(p)
        want, by = expected_hash(s, hashes)
        if not hash_ok(h, want):
            errors.append(f"{s['file']}: sha256 {h[:16]} ≠ {by} {str(want)[:16]}")
            continue
        with open(p, encoding="utf-8") as f:
            L[s["file"]] = json.load(f)
        meta[s["file"]] = {"path": p, "sha256": h, "bytes": os.path.getsize(p)}
    extra = sorted(f for f in os.listdir(bronze_dir) if f.endswith(".json") and f not in L and f not in {e["file"] for e in erd["source_files"]})
    if extra:
        errors.append(f"ERD 에 없는 원장 파일: {extra}")
    if errors:
        raise BuildRefused("; ".join(errors))
    return L, meta


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


_ROW = re.compile(r"^\| (\d+) \| `([^`]*)` \| ([^|]*) \| ([^|]*) \| ([^|]*) \| `([^`]*)` \|(.*)\|$")


def load_column_map(path):
    """erd-v2.4-column-map.md 의 파일별 표 → {(file, path): {dest, target}} (잎 키 1,072)."""
    out = {}
    cur = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^## `([^`]+\.json)` — 잎 키 (\d+)", line)
            if m:
                cur = m.group(1)
                continue
            if line.startswith("## ") and not line.startswith("## `"):
                cur = None
                continue
            if cur is None:
                continue
            m = _ROW.match(line.rstrip("\n"))
            if m:
                out[(cur, m.group(2))] = {"dest": m.group(5).strip(), "target": m.group(6), "type": m.group(3).strip(), "n": m.group(4).strip()}
    return out
