"""legacy notes (jekyll/obsidian 스타일) → kknaks-profile spec 형식 변환.

156 파일 frontmatter 일괄 정리 + 폴더 rename + 평평한 mock 삭제.

처리:
- date: multi-format → 'YYYY.MM.DD' 정규화
- tags: 단일 string 또는 list → 항상 list
- links: [] 빈 배열 추가 (사용자/skill이 차차 박음)
- 불필요 jekyll 메타 제거 (category, permalink, updated, layout 등)
- type/id/group 안 박음 (백엔드 _auto_enrich_note가 자동 추출)

별도:
- 'BackendSchool(멋사)' 폴더 rename → 'BackendSchool'
- legacy mock 'notes/python-asyncio.md' (평평하게 박힌 시드) 삭제

Usage: python3 app/scripts/migrate_legacy_notes.py
"""

from __future__ import annotations

import datetime
from pathlib import Path

import frontmatter

REPO = Path(__file__).resolve().parents[2]
NOTES = REPO / "persona" / "notes"

DROP_FIELDS = {"category", "permalink", "updated", "layout", "header"}


def normalize_date(d) -> str:
    if isinstance(d, (datetime.date, datetime.datetime)):
        return d.strftime("%Y.%m.%d")
    return str(d).strip().split()[0].replace("-", ".")


def migrate_one(path: Path) -> None:
    post = frontmatter.load(path)
    md = dict(post.metadata)

    if "date" in md:
        md["date"] = normalize_date(md["date"])

    if "tags" in md and isinstance(md["tags"], str):
        md["tags"] = [md["tags"]]
    elif "tags" not in md:
        md["tags"] = []

    md.setdefault("links", [])

    for f in DROP_FIELDS:
        md.pop(f, None)

    new_post = frontmatter.Post(post.content, **md)
    path.write_text(frontmatter.dumps(new_post, sort_keys=False), encoding="utf-8")


def main() -> None:
    bs_old = NOTES / "BackendSchool(멋사)"
    bs_new = NOTES / "BackendSchool"
    if bs_old.is_dir() and not bs_new.exists():
        bs_old.rename(bs_new)
        print(f"renamed {bs_old.name} → {bs_new.name}")

    legacy_mock = NOTES / "python-asyncio.md"
    if legacy_mock.exists() and legacy_mock.is_file():
        legacy_mock.unlink()
        print(f"removed legacy mock: {legacy_mock.relative_to(REPO)}")

    count = 0
    for md_file in sorted(NOTES.rglob("*.md")):
        try:
            migrate_one(md_file)
            count += 1
        except Exception as e:
            print(f"  ! skip {md_file.relative_to(NOTES)}: {e}")
    print(f"migrated {count} files")


if __name__ == "__main__":
    main()
