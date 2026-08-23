#!/usr/bin/env python3
"""Freeze a product's full doc tree into a versioned archive snapshot.

버전 컷오프: 배포/심사 시점에 `products/<product>/` 전체(00~70)를
`products/<product>/_archive/<version>/` 로 복사하고, 복사본의 frontmatter를
archived 로 마킹한다. cut 전에는 release gate를 통과해야 한다.
기본은 live 문서를 그대로 두며, `--reset-current`를 주면 archive freeze 후
work cycle을 다음 버전 시작 상태로 carry/reset 한다.

검증기(product_doc_pipeline.py)는 `products/` 최상위만 제품으로 순회하고
release/work/runbook 글롭이 모두 비재귀라, 중첩된 `_archive/` 복사본은
재검증되지 않는다 (archived 마킹이 파이프라인을 깨지 않음).

Usage:
    python3 .agent/scripts/product_version_cutoff.py <product> <version> [옵션]

    <product>   제품 slug (예: mac-remote)
    <version>   버전 (예: 1.0.1 또는 v1.0.1 — v 접두는 자동 정규화)

옵션:
    --date YYYY-MM-DD   archived_at 날짜 (기본: 오늘, KST)
    --no-assets         70-runbook/assets 등 바이너리 자산 제외 (.md/.txt/.json만)
    --no-release-gate   release gate 검증을 건너뜀
    --reset-current     freeze 후 live 30-work를 다음 cycle 상태로 reset
    --dry-run           복사하지 않고 무엇을 할지 출력만
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

KST = timezone(timedelta(hours=9))
ROOT = Path(__file__).resolve().parents[2]
PRODUCTS_DIR = ROOT / "products"

# 복사 시 무조건 제외 (아카이브 중첩 방지 + 잡파일)
EXCLUDE_NAMES = {"_archive", ".DS_Store", ".git", ".obsidian"}
# --no-assets 일 때 보존할 텍스트 확장자
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".csv"}
VERSION_RE = re.compile(r"^v?\d+\.\d+\.\d+([.\-+].+)?$")


def normalize_version(raw: str) -> str:
    value = raw.strip()
    if not VERSION_RE.match(value):
        raise SystemExit(f"invalid version: {raw!r} (예: 1.0.1 또는 v1.0.1)")
    return value if value.startswith("v") else f"v{value}"


def git_short_head() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip()
    except Exception:
        return "unknown"


def run_release_gate(product: str) -> None:
    cmd = [
        sys.executable,
        str(ROOT / ".agent/scripts/product_doc_pipeline.py"),
        "--strict",
        "--release-gate",
        "--product",
        product,
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)


def make_ignore(no_assets: bool):
    def _ignore(dir_path: str, names: list[str]) -> set[str]:
        ignored = {n for n in names if n in EXCLUDE_NAMES}
        if no_assets:
            for n in names:
                p = Path(dir_path) / n
                if p.is_file() and p.suffix.lower() not in TEXT_SUFFIXES:
                    ignored.add(n)
        return ignored

    return _ignore


def mark_frontmatter(text: str, version: str, archived_at: str) -> str:
    """frontmatter가 있으면 archived 마킹. 없으면 원문 그대로."""
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    head = text[4:end]
    body = text[end + 5 :]
    lines = head.split("\n")

    out: list[str] = []
    inserted_meta = False
    in_status_tag = False
    for line in lines:
        # status: X → status: archived (+ original_status)
        m = re.match(r"^status:\s*(.+?)\s*$", line)
        if m and not inserted_meta:
            original = m.group(1).strip().strip('"')
            out.append("status: archived")
            out.append(f"original_status: {original}")
            out.append(f"archived_version: {version}")
            out.append(f"archived_at: {archived_at}")
            inserted_meta = True
            continue
        # tags 의 - status/X → - status/archived
        if re.match(r"^\s*-\s*status/", line):
            indent = line[: len(line) - len(line.lstrip())]
            out.append(f"{indent}- status/archived")
            continue
        out.append(line)

    # status 라인이 없던 문서(예: 일부 index)면 메타를 frontmatter 끝에 추가
    if not inserted_meta:
        out.append(f"archived_version: {version}")
        out.append(f"archived_at: {archived_at}")

    return "---\n" + "\n".join(out) + "\n---\n" + body


WIKILINK_RE = re.compile(r"\[\[([^\[\]]+)\]\]")
MD_LINK_RE = re.compile(r"\]\(([^)]+?\.md)\)")


def file_prefix(version: str) -> str:
    """`v1.0.1` → `v1_0_1-` (파일명/링크 prefix용)."""
    return "v" + version.lstrip("v").replace(".", "_") + "-"


def rewrite_wikilinks(text: str, rename: dict[str, str]) -> str:
    """archive 내 wikilink target을 prefix된 사본 이름으로 바꾼다.

    동일 basename이 live와 archive에 둘 생기면 Obsidian이 전역 basename으로
    모호하게 해석해 live 링크까지 오염되므로, 아카이브 사본 파일명에 버전
    prefix를 달아 유니크하게 만들고 내부 링크도 그 사본을 가리키게 한다.
    """
    def _repl(m: re.Match) -> str:
        inner = m.group(1)
        parts = re.split(r"(\\?\|)", inner, maxsplit=1)  # target, [sep, alias]
        target = parts[0]
        if target in rename:
            return "[[" + rename[target] + "".join(parts[1:]) + "]]"
        return m.group(0)

    return WIKILINK_RE.sub(_repl, text)


def rewrite_md_links(text: str, rename: dict[str, str]) -> str:
    """archive 내 마크다운 상대링크 `](dir/name.md)` 의 basename을 prefix한다."""
    def _repl(m: re.Match) -> str:
        target = m.group(1)
        slash = target.rfind("/")
        head, base = (target[: slash + 1], target[slash + 1 :]) if slash >= 0 else ("", target)
        stem = base[:-3]  # strip .md
        if stem in rename:
            return f"]({head}{rename[stem]}.md)"
        return m.group(0)

    return MD_LINK_RE.sub(_repl, text)


def process_archive(dest: Path, version: str, archived_at: str) -> tuple[int, int]:
    """frontmatter 마킹 + wikilink/링크 prefix 갱신 + 파일명 prefix 리네임."""
    prefix = file_prefix(version)
    md_files = sorted(dest.rglob("*.md"))
    rename = {p.stem: prefix + p.stem for p in md_files}

    marked = 0
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        new = mark_frontmatter(text, version, archived_at)
        new = rewrite_wikilinks(new, rename)
        new = rewrite_md_links(new, rename)
        if new != text:
            path.write_text(new, encoding="utf-8")
            marked += 1

    renamed = 0
    for path in md_files:
        target = path.parent / (prefix + path.name)
        path.rename(target)
        renamed += 1

    return marked, renamed


def read_meta(vdir: Path) -> tuple[str, str]:
    """버전 폴더의 마킹된 .md 중 하나에서 (archived_version, archived_at)."""
    for path in sorted(vdir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        version = at = "-"
        for line in text.split("\n", 60):
            if line.startswith("archived_version:"):
                version = line.split(":", 1)[1].strip()
            elif line.startswith("archived_at:"):
                at = line.split(":", 1)[1].strip()
            elif line.strip() == "---" and version != "-":
                break
        if version != "-" and at != "-":
            return version, at
    return "-", "-"


def write_archive_index(archive_dir: Path, product: str) -> None:
    rows = []
    for vdir in sorted(p for p in archive_dir.iterdir() if p.is_dir() and p.name.startswith("v")):
        md_count = sum(1 for _ in vdir.rglob("*.md"))
        version, at = read_meta(vdir)
        if version == "-":
            version = vdir.name
        rows.append((version, at, md_count))
    # 최신 버전 위로
    rows.sort(key=lambda r: r[0], reverse=True)

    lines = [
        "# Archive Index",
        "",
        "규칙: `rules/product-doc-pipeline.md`",
        "",
        f"> `{product}` 의 버전 컷오프 스냅샷. **읽기 전용 — 수정하지 않는다.** live 문서는 상위 디렉토리.",
        "> 각 버전 폴더는 컷오프 시점의 제품 문서 전체(00~70) 동결본이며 frontmatter가 `status: archived` 로 마킹돼 있다.",
        "",
        "## 동결 버전",
        "",
        "| Version | Archived At | Docs |",
        "|---|---|---|",
    ]
    for version, at, md_count in rows:
        lines.append(f"| {version} | {at} | {md_count} |")
    lines.append("")
    (archive_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


def chmod_readonly(path: Path) -> None:
    for child in path.rglob("*"):
        mode = child.stat().st_mode
        child.chmod(mode & ~0o222)
    path.chmod(path.stat().st_mode & ~0o222)


def section_bounds(lines: list[str], header: str) -> tuple[int, int] | None:
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == header)
    except StopIteration:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return start, end


def reset_table_section(lines: list[str], header: str) -> tuple[list[str], int]:
    bounds = section_bounds(lines, header)
    if bounds is None:
        return lines, 0
    start, end = bounds
    out = lines[: start + 1]
    kept_table_lines = 0
    removed = 0
    for line in lines[start + 1 : end]:
        if line.lstrip().startswith("|"):
            if kept_table_lines < 2:
                out.append(line)
                kept_table_lines += 1
            else:
                removed += 1
            continue
        out.append(line)
    out.extend(lines[end:])
    return out, removed


def carry_spec_coverage(lines: list[str], version: str) -> tuple[list[str], int]:
    bounds = section_bounds(lines, "## Spec Coverage")
    if bounds is None:
        return lines, 0
    start, end = bounds
    row_re = re.compile(r"^(\|\s*[^|]+\s*\|)([^|]*)\|([^|]*)\|(.*)$")
    out = lines[: start + 1]
    changed = 0
    for line in lines[start + 1 : end]:
        match = row_re.match(line)
        if match and not re.fullmatch(r"\|?\s*-+", line.replace("|", "")):
            first_cell = match.group(1)
            if "Spec" in first_cell or "---" in first_cell:
                out.append(line)
            else:
                out.append(f"{first_cell} (carried @{version}) | draft |{match.group(4)}")
                changed += 1
        else:
            out.append(line)
    out.extend(lines[end:])
    return out, changed


def reset_current(product_dir: Path, version: str) -> tuple[int, int, int]:
    """Reset live work cycle after archive freeze.

    Our repo uses `30-work/README.md` plus `30-work/work-*.md`, not the
    mediness single-file `30-work.md` model. So the safe carry/reset is:
    clear current work index rows, mark spec coverage carried, and remove
    live work body files that were just frozen into the archive.
    """
    work_index = product_dir / "30-work/README.md"
    removed_rows = carried_rows = removed_files = 0
    if work_index.exists():
        lines = work_index.read_text(encoding="utf-8").splitlines()
        lines, removed_rows = reset_table_section(lines, "## Work 목록")
        lines, carried_rows = carry_spec_coverage(lines, version)
        work_index.write_text("\n".join(lines) + "\n", encoding="utf-8")

    work_dir = product_dir / "30-work"
    if work_dir.exists():
        for path in sorted(work_dir.glob("work-*.md")):
            path.unlink()
            removed_files += 1
    return removed_rows, carried_rows, removed_files


def dir_size(path: Path) -> str:
    total = float(sum(p.stat().st_size for p in path.rglob("*") if p.is_file()))
    for unit in ("B", "K", "M"):
        if total < 1024:
            return f"{total:.0f}{unit}" if unit == "B" else f"{total:.1f}{unit}"
        total /= 1024
    return f"{total:.1f}G"


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze a product doc tree into a versioned archive.")
    parser.add_argument("product", help="제품 slug (예: mac-remote)")
    parser.add_argument("version", help="버전 (예: 1.0.1)")
    parser.add_argument("--date", help="archived_at (YYYY-MM-DD, 기본 오늘 KST)")
    parser.add_argument("--no-assets", action="store_true", help="바이너리 자산 제외")
    parser.add_argument("--no-release-gate", action="store_true", help="release gate 검증 생략")
    parser.add_argument("--reset-current", action="store_true", help="archive freeze 후 live work cycle reset")
    parser.add_argument("--dry-run", action="store_true", help="복사 없이 계획만 출력")
    args = parser.parse_args()

    version = normalize_version(args.version)
    archived_at = args.date or datetime.now(KST).strftime("%Y-%m-%d")

    src = PRODUCTS_DIR / args.product
    if not src.is_dir():
        raise SystemExit(f"product not found: products/{args.product}")

    archive_dir = src / "_archive"
    dest = archive_dir / version
    if dest.exists():
        raise SystemExit(f"archive already exists: {dest.relative_to(ROOT)} (덮어쓰지 않음)")

    md_total = sum(1 for p in src.rglob("*.md") if "_archive" not in p.parts)
    commit = git_short_head()

    print("Product Version Cutoff")
    print(f"- product: {args.product}")
    print(f"- version: {version}")
    print(f"- archived_at: {archived_at}")
    print(f"- source commit: {commit}")
    print(f"- dest: {dest.relative_to(ROOT)}")
    print(f"- md files (source): {md_total}")
    print(f"- assets: {'제외 (--no-assets)' if args.no_assets else '포함'}")
    print(f"- release gate: {'생략' if args.no_release_gate else '필수'}")
    print(f"- reset current: {'yes' if args.reset_current else 'no'}")

    if args.dry_run:
        print("- dry-run: 복사하지 않음")
        return 0

    if not args.no_release_gate:
        run_release_gate(args.product)

    archive_dir.mkdir(exist_ok=True)
    shutil.copytree(src, dest, ignore=make_ignore(args.no_assets))
    marked, renamed = process_archive(dest, version, archived_at)
    write_archive_index(archive_dir, args.product)
    chmod_readonly(dest)

    reset_summary = None
    if args.reset_current:
        reset_summary = reset_current(src, version)

    print(f"- copied: {dir_size(dest)}")
    print(f"- file prefix: {file_prefix(version)}")
    print(f"- marked archived: {marked} md files")
    print(f"- renamed (prefix): {renamed} md files")
    print("- readonly: yes")
    if reset_summary is not None:
        removed_rows, carried_rows, removed_files = reset_summary
        print(
            f"- current reset: work rows {removed_rows}, spec coverage carried {carried_rows}, work files removed {removed_files}"
        )
    print(f"- index: {(archive_dir / 'README.md').relative_to(ROOT)}")
    print("- done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
