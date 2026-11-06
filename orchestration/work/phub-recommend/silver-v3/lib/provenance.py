# -*- coding: utf-8 -*-
"""원장 locator — `<파일>:<잎 키 경로>@<레코드 키>`.

잎 키 경로는 컬럼 스캔(bronze-ledger-column-scan.py)과 같은 접기 규칙: 배열 → `[]`, 코드형 키 → `{code}`.
레코드 키(rec) = 경로의 `[]`·`{code}` 마다 실제 배열 위치·키를 `/` 로 이은 것(없으면 `-`).
예: `complications.json:categories[].complications[].severity@3/12` · `extracted.json:{code}.overview@M1`.
ERD 가 따로 정한 locator(complications 이름 `@M16/12` · 표현 `@<계열>/<순번>`)는 anchor·결정 target 용으로 레코드에 따로 둔다(erd_locator).
"""
import re

CODE_KEY_RE = re.compile(r"^(?:[A-Z]{1,2}\d+(?:-\d+)*|M\d+_to_M\d+|auto-\d+-\d+)$")


def fold_key(k):
    return "{code}" if CODE_KEY_RE.match(k) else k


def is_leaf(v):
    return not ((isinstance(v, dict) and v) or (isinstance(v, list) and v))


def leaves(v, path="", rec=()):
    """(path, rec, value) — 잎 = 스칼라 · null · 빈 배열 · 빈 객체."""
    if isinstance(v, dict) and v:
        for k, c in v.items():
            fk = fold_key(k)
            np = f"{path}.{fk}" if path else fk
            yield from leaves(c, np, rec + ((k,) if fk == "{code}" else ()))
        return
    if isinstance(v, list) and v:
        for i, x in enumerate(v):
            yield from leaves(x, path + "[]", rec + (i,))
        return
    yield path, rec, v


def rec_str(rec):
    return "/".join(str(x) for x in rec) if rec else "-"


def P(file, path, rec):
    """provenance 한 칸."""
    return {"file": file, "path": path, "rec": rec_str(rec) if isinstance(rec, tuple) else rec}


def loc(p):
    return f"{p['file']}:{p['path']}@{p['rec']}"


def parse_loc(s):
    file, rest = s.split(":", 1)
    path, rec = rest.rsplit("@", 1)
    return {"file": file, "path": path, "rec": rec}


_SEG = re.compile(r"([^.\[\]]+)((?:\[\])*)")


def split_path(path):
    """`a.b[].{code}.c[][]` → [('a',0),('b',1),('{code}',0),('c',2)]"""
    out = []
    for part in path.split(".") if path else []:
        m = _SEG.fullmatch(part)
        if not m:
            raise ValueError(f"경로 해석 불가: {path}")
        out.append((m.group(1), len(m.group(2)) // 2))
    return out


def resolve(data, path, rec):
    """locator → 값. 없으면 KeyError. 빈 경로(파일 루트 잎)는 rec '-'."""
    keys = [] if rec in ("-", "") else rec.split("/")
    v = data
    ki = 0
    for name, n_arr in split_path(path):
        if name == "{code}":
            k = keys[ki]
            ki += 1
            if not isinstance(v, dict) or k not in v:
                raise KeyError(k)
            v = v[k]
        else:
            if not isinstance(v, dict) or name not in v:
                raise KeyError(name)
            v = v[name]
        for _ in range(n_arr):
            i = int(keys[ki])
            ki += 1
            if not isinstance(v, list) or i >= len(v):
                raise KeyError(i)
            v = v[i]
    if ki != len(keys):
        raise KeyError("rec 길이 불일치")
    return v


def records(data, root):
    """루트 경로(`modality[]` · `{code}` · `categories.{code}` · `zones[]`)의 레코드 → (rec, obj). 루트 '' 는 파일 자체."""
    def go(v, segs, rec):
        if not segs:
            yield rec, v
            return
        (name, n_arr), rest = segs[0], segs[1:]
        if name == "{code}":
            if isinstance(v, dict):
                for k, c in v.items():
                    if CODE_KEY_RE.match(k):
                        yield from arr(c, n_arr, rest, rec + (k,))
            return
        if not isinstance(v, dict) or name not in v:
            return
        yield from arr(v[name], n_arr, rest, rec)

    def arr(v, n, rest, rec):
        if n == 0:
            yield from go(v, rest, rec)
            return
        if isinstance(v, list):
            for i, x in enumerate(v):
                yield from arr(x, n - 1, rest, rec + (i,))

    yield from go(data, split_path(root), ())


def sub_leaves(obj, root, rec):
    """레코드 obj(루트 경로 root · rec) 아래 잎 전부 — 경로는 파일 기준 전체 경로."""
    for p, r, v in leaves(obj):
        if p:
            full = f"{root}.{p}" if root and not p.startswith("[]") else (root + p if root else p)
        else:
            full = root
        yield full, rec + r, v
