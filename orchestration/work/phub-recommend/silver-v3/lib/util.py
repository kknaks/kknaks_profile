# -*- coding: utf-8 -*-
"""공통: 정규화(norm_v1) · 식별자 · 결정론 JSON 쓰기."""
import hashlib
import json
import os
import re
import unicodedata


def norm(s):
    """norm_v1 — NFKC → casefold → 모든 공백 제거. 그 밖 문자는 그대로(ERD §1.1)."""
    if s is None:
        return None
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", str(s)).casefold())


def mkid(prefix, key):
    """<PREFIX>-<sha256(norm(canonical_key))[:10]> — 참조 구현(erd-v2-tuples.py mkid)과 같은 계산."""
    return f"{prefix}-{hashlib.sha256(norm(key).encode()).hexdigest()[:10]}"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def dedupe(xs):
    return list(dict.fromkeys(xs))


def dumps(obj):
    """결정론 직렬화 — 키 정렬 · 한글 그대로 · 구분자 고정."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=_default)


def _default(o):
    if isinstance(o, (set, frozenset)):
        return sorted(o, key=lambda x: dumps(x))
    if isinstance(o, tuple):
        return list(o)
    raise TypeError(f"직렬화 불가: {type(o)}")


def write_json(path, obj, indent=1):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=indent, default=_default))
        f.write("\n")


def write_jsonl(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(dumps(r))
            f.write("\n")


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text if text.endswith("\n") else text + "\n")


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        out.append("| " + " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in r) + " |")
    return "\n".join(out)
