"""detail_path md 읽기 — 공용 헬퍼.

정보는 DB, 상세는 md(erd.md) — DB 는 `detail_path` 로 가리키기만 하고 본문을
복사하지 않는다. 공개 API 가 응답을 조립할 때 여기로 전문을 읽어 내려준다.

detail_path 가 끊기면(파일을 옮겼거나 지웠으면) 상세 없음으로 그린다 —
None 을 돌려주고 에러로 만들지 않는다(_RESUME.md §4 「detail_path 가 끊기면」).

frontmatter 는 떼고 내려준다 — 메타의 SoT 는 DB 다. note·algorithm 원장처럼
frontmatter 를 유지하는 파일도 있으므로(어드민 프리필이 읽는다) 원장이 아니라
서빙에서 뗀다.
"""

from __future__ import annotations

import re
from pathlib import Path

from config import get_settings

_FRONTMATTER = re.compile(r"^---\n.*?\n---\n+", re.DOTALL)


def read_detail(detail_path: str | None) -> str | None:
    """리포 루트 기준 detail_path 의 md 본문. 없거나 끊겼으면 None."""
    if not detail_path:
        return None
    target = Path(get_settings().repo_root) / detail_path
    if not target.is_file():
        return None
    text = target.read_text(encoding="utf-8")
    return _FRONTMATTER.sub("", text, count=1)
