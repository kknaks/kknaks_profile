"""DAY-SPEC-000 §3 ↔ backend/day/models 대조표 — #225 리포트용.

실행(레포 루트): PYTHONPATH=backend ENCRYPTION_KEY=<아무 Fernet 키> DB_SCHEMA=day_dev \
  uv run python <이 파일>
SPEC 표(필드 · 타입 · 필수)를 읽어 모델 칸과 맞춘다. 타입 「—」 칸은 보류 · 다른 곳(안 만듦).
"""

import re
import sys

from sqlalchemy import (
    BigInteger, Boolean, Date, DateTime, Enum, Integer, Numeric, String, Text, Time,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID

import day.models  # noqa: F401
from common.crypto import EncryptedJSONB, EncryptedText
from day.db import Base

SPEC = ("/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/"
        "products/day/20-spec/spec-000-data-model.md")
HEAD = re.compile(r"^#{3,5} `?([a-z_]+)`?\s*(?:—|·|$)")
KEYWORDS = ("uuid", "varchar", "text", "bool", "int", "bigint", "numeric", "date", "time",
            "timestamptz", "jsonb", "enum", "암호화", "PK")
# 열린 enum — SPEC 에 값 목록이 없거나 「…」로 열려 있어 문자열 칸으로 둔 것(코디 결정 2)
OPEN_ENUMS = {("customer", "gender"), ("external_ref", "entity_type"), ("visit_task", "unit_type"),
              ("notification_setting", "kind"), ("display_request", "kind"),
              ("identity_check", "status"), ("identity_check", "method"), ("id_photo", "doc_type")}


def split_names(cell: str) -> list[str]:
    names = re.findall(r"`([^`]+)`", cell) or [cell]
    return [p.strip() for n in names for p in re.split(r"\s*·\s*", n) if p.strip()]


def split_types(cell: str, count: int) -> tuple[list[str], bool]:
    tokens = [t.strip() for t in cell.split("·")]
    merged: list[str] = []
    for t in tokens:
        if merged and not t.startswith(KEYWORDS):
            merged[-1] += " · " + t  # enum 값 목록의 나머지
        else:
            merged.append(t)
    pk = False
    if merged and merged[-1] == "PK":
        merged.pop()
        pk = True
    if len(merged) != count:
        merged = [merged[0]] * count if merged else ["—"] * count
    return merged, pk


def parse_spec() -> dict[str, list[tuple[str, str, bool, bool]]]:
    tables: dict[str, list[tuple[str, str, bool, bool]]] = {}
    cur = None
    header: list[str] | None = None
    code = False
    for line in open(SPEC, encoding="utf-8"):
        if line.startswith("## 4."):
            break
        if line.startswith("#"):
            m = HEAD.match(line)
            cur = m.group(1) if m and m.group(1) != "config" else None
            code = "코드 테이블" in line
            header = None
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if code and line.startswith("| `"):
            name = cells[0].strip("`")
            fields = re.findall(r"`([a-z_]+)`", cells[1])
            if "생성/수정 시각" in cells[1]:
                fields += ["created_at", "updated_at"]
            pk = re.findall(r"`([a-z_]+)` \+ `([a-z_]+)` \(PK\)", cells[1])
            pkset = set(pk[0]) if pk else {"id"}
            fields = [x for x in fields if x != "funnel_category" and x != name]
            tables[name] = [(x, "(코드 표 — 타입 미표기)", False, x in pkset) for x in fields]
            continue
        if cur is None:
            continue
        if header is None:
            header = cells
            continue
        if cells[0] and set(cells[0]) <= set("-: "):  # 구분선(빈 칸은 「묶음」 이어짐)
            continue
        hi = {h: i for i, h in enumerate(header)}
        if "필드" not in hi:
            continue
        names = split_names(cells[hi["필드"]])
        types, pk = split_types(cells[hi["타입"]], len(names))
        required = cells[hi["필수"]] == "✓"
        for n, t in zip(names, types, strict=True):
            tables.setdefault(cur, []).append((n, t, required, pk or "PK" in t))
    return tables


def expected_type(spec_type: str):  # noqa: ANN201
    t = spec_type
    if t.startswith("암호화 text"):
        return EncryptedText
    if t.startswith("암호화 JSONB"):
        return EncryptedJSONB
    if t.startswith("uuid"):
        return UUID
    if t.startswith("varchar[]"):
        return (ARRAY, String)
    if t.startswith("enum[]"):
        return (ARRAY, Enum)
    for prefix, cls in (("varchar", String), ("text", Text), ("bool", Boolean),
                        ("bigint", BigInteger), ("int", Integer), ("numeric", Numeric),
                        ("timestamptz", DateTime), ("date", Date), ("time", Time),
                        ("jsonb", JSONB), ("enum", Enum)):
        if t.startswith(prefix):
            return cls
    return None


def type_ok(col, exp) -> bool:  # noqa: ANN001
    if exp is None:
        return True
    if isinstance(exp, tuple):
        return isinstance(col.type, exp[0]) and isinstance(col.type.item_type, exp[1])
    if exp is Text:
        return isinstance(col.type, Text)
    if exp is String:
        return isinstance(col.type, String) and not isinstance(col.type, Text)
    if exp is Integer:
        return isinstance(col.type, Integer) and not isinstance(col.type, BigInteger)
    if exp is DateTime:
        return isinstance(col.type, DateTime) and col.type.timezone
    return isinstance(col.type, exp)


def main() -> int:
    spec = parse_spec()
    models = {t.name: t for t in Base.metadata.tables.values()}
    print(f"SPEC 테이블 {len(spec)} · 모델 테이블 {len(models)} · "
          f"SPEC 만 {sorted(set(spec) - set(models))} · 모델만 {sorted(set(models) - set(spec))}\n")
    print("| 테이블 | SPEC 칸 | 보류(—) | 모델 칸 | 칸 차이 | 타입 | 필수 | PK | 유일 · FK · 비고 |")
    print("|---|---|---|---|---|---|---|---|---|")
    problems = 0
    for name in sorted(spec):
        rows = spec[name]
        made = [r for r in rows if r[1] != "—"]
        held = [r[0] for r in rows if r[1] == "—"]
        table = models[name]
        spec_cols = {r[0] for r in made}
        model_cols = {c.name for c in table.columns}
        extra = sorted(model_cols - spec_cols)
        missing = sorted(spec_cols - model_cols)
        type_bad, req_bad, pk_bad, notes = [], [], [], []
        for field, t, required, pk in made:
            if field not in table.columns:
                continue
            col = table.columns[field]
            exp = expected_type(t)
            if (name, field) in OPEN_ENUMS:
                ok = isinstance(col.type, String)
                notes.append(f"{field}=열린 enum→varchar")
            else:
                ok = type_ok(col, exp)
            if not ok:
                type_bad.append(f"{field}({t}→{col.type})")
            if not t.startswith("(코드") and required != (not col.nullable):
                req_bad.append(f"{field}(SPEC {'✓' if required else '–'} · 모델 "
                               f"{'NOT NULL' if not col.nullable else 'NULL'})")
            if pk != col.primary_key and not t.startswith("(코드"):
                pk_bad.append(field)
            m = re.search(r"varchar\((\d+)\)", t)
            if m and getattr(col.type, "length", None) != int(m.group(1)):
                type_bad.append(f"{field} 길이")
        uniques = [",".join(c.name for c in u.columns) for u in table.constraints
                   if u.__class__.__name__ == "UniqueConstraint"]
        uniques += [c.name for c in table.columns if c.unique]
        fks = len(table.foreign_keys)
        cell = []
        if uniques:
            cell.append("UNIQUE " + " / ".join(f"({u})" for u in sorted(set(uniques))))
        cell.append(f"FK {fks}")
        if extra:
            cell.append("모델에만 " + ",".join(extra))
        if held:
            cell.append("보류 " + ",".join(held))
        cell += sorted(set(notes))
        diff = "없음" if not missing else "SPEC 만 " + ",".join(missing)
        bad = bool(missing or type_bad or req_bad or pk_bad)
        problems += bad
        pk_cols = ",".join(c.name for c in table.primary_key.columns)
        print(f"| `{name}` | {len(rows)} | {len(held)} | {len(model_cols)} | {diff} | "
              f"{'맞음' if not type_bad else '; '.join(type_bad)} | "
              f"{'맞음' if not req_bad else '; '.join(req_bad)} | "
              f"({pk_cols}){'' if not pk_bad else ' 다름 ' + ','.join(pk_bad)} | "
              f"{' · '.join(cell)} |")
    print(f"\n불일치 테이블 {problems}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
