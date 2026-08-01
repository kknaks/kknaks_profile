"""교안 형식의 단일 출처 로더 (KDEV-WORK-015 P3 보정).

교안을 만드는 경로가 둘이다 — 승인 게이트의 `derived` 스테이지와 기존
`content_enrich` 잡. 처음에는 8개 섹션 명세를 **양쪽 프롬프트에 각각 적었는데**,
그건 `reference`·`concept` 에서 없앤 이중 SoT 를 교안에서 다시 만드는 것이었다.
한쪽만 고치는 날 두 경로의 산출물이 조용히 갈라진다.

`templates/persona/content.md` 를 SoT 로 두고 양쪽이 그것을 **불러다 쓴다.**

지식 노트처럼 "에이전트가 레포를 읽게" 하지 않는 이유는, `content_enrich` 가
`cwd` 없이 호출돼 레포에 접근할 수 없기 때문이다. 두 경로에 서로 다른 방식을
쓰느니 **한 파일을 양쪽이 싣는** 편이 단순하고, 어차피 고칠 곳은 한 곳이다.
"""

from __future__ import annotations

import logging
import re
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger("kknaks-back.content-format")

TEMPLATE_PATH = "templates/persona/content.md"

#: 파일명 slug 로 쓸 수 없는 문자.
_SLUG_RE = re.compile(r"[^a-z0-9]+")
#: 제목이 비거나 전부 비-ASCII 라 slug 를 못 만들 때.
_FALLBACK_SLUG = "content"


def content_slug(title_en: str) -> str:
    """교안 파일명의 뒷부분 — `C-023-database-selection-guide` 의 `database-selection-guide`.

    **`C-023.md` 로는 안 된다.** 로더가 `{id}-` 를 파일명 prefix 로 요구한다
    (spec-01 §6.1, `persona_loader` contents 검사). 규약을 어기면 파일이 거부되는
    데서 끝나지 않고 **persona 로드 전체가 실패해** 사이트가 옛 데이터를 계속
    서빙한다 — 콘텐츠 갱신이 통째로 멈춘다.

    교안 형식과 같은 이유로 여기 둔다 — 게이트(`derived`)와 `content_enrich` 잡이
    **같은 규약으로 이름을 지어야** 한쪽만 고쳐지는 날이 오지 않는다.
    """
    slug = _SLUG_RE.sub("-", (title_en or "").lower()).strip("-")
    # 너무 길면 파일명이 다루기 어려워진다. 단어 경계에서 자른다.
    if len(slug) > 60:
        slug = slug[:60].rsplit("-", 1)[0]
    return slug or _FALLBACK_SLUG


def content_stem(content_id: str, title: dict | str | None) -> str:
    """`{id}-{slug}` — 교안 파일명 stem."""
    title_en = title.get("en", "") if isinstance(title, dict) else (title or "")
    return f"{content_id}-{content_slug(str(title_en))}"

#: 파일을 못 읽었을 때의 최소 골격. 교안이 통째로 무너지는 것보다 낫지만,
#: **경고를 남긴다** — 조용히 다른 형식으로 나가면 나중에 알아채기 어렵다.
FALLBACK = """교안은 아래 8개 H2 섹션을 순서대로 빠짐없이 포함한다.

## 개요 / ## 배경 / 사전 지식 / ## 핵심 개념 / ## 작동 원리 /
## 코드 예시 / ## 함정·실수 / ## 베스트 프랙티스 / ## 참고
"""


@lru_cache(maxsize=4)
def _read(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8").strip()
    except OSError:
        logger.warning("%s 를 읽지 못해 축약 형식으로 대체한다", path)
        return FALLBACK


def content_format(repo_root: Path | None = None) -> str:
    """`templates/persona/content.md` 전문.

    프롬프트에 그대로 실린다 — 형식을 고치려면 그 파일만 고친다.
    """
    if repo_root is None:
        import config

        repo_root = config.repo_root()
    return _read(str(repo_root / TEMPLATE_PATH))


#: 잔디 산출물 형식도 같은 이유로 여기 둔다 (KDEV-WORK-017 P2 / KDEV-SPEC-012).
#: `compose` 스테이지가 이 둘을 불러다 프롬프트를 만든다 — 규칙을 파이썬 문자열에
#: 복사하면 교안에서 없앤 이중 SoT 를 daily·career 에서 다시 만드는 것이 된다.
DAILY_TEMPLATE_PATH = "templates/persona/daily.md"
CAREER_TEMPLATE_PATH = "templates/persona/career.md"

DAILY_FALLBACK = """daily 는 frontmatter(type·date·auto·counts·summary)와 본문으로 이뤄진다.
counts 는 코드가 채우므로 AI 가 세지 않는다. summary 는 {ko: [], en: []} 이고 활동
단위마다 한 줄이며, 활동이 0인 카테고리는 줄을 만들지 않는다. 본문은 1200자 이내.
"""

CAREER_FALLBACK = """career 본문은 ## 무슨 일 하는지 / ## 담당 영역 / ## 챌린지 /
## 배운 점 / ## 대표 작업 다섯 섹션이다. 갱신은 append 가 아니라 기존 줄을 더 정확하게
만드는 것이고, ## 챌린지·## 배운 점 은 각 5~7줄을 넘지 않는다. bullets·period·
is_current 같은 사람 전용 필드는 갱신안에 담지 않는다.
"""


def _persona_format(path: str, fallback: str, repo_root: Path | None) -> str:
    if repo_root is None:
        import config

        repo_root = config.repo_root()
    text = _read(str(repo_root / path))
    return text if text and text != FALLBACK else fallback


def daily_format(repo_root: Path | None = None) -> str:
    """`templates/persona/daily.md` 전문."""
    return _persona_format(DAILY_TEMPLATE_PATH, DAILY_FALLBACK, repo_root)


def career_format(repo_root: Path | None = None) -> str:
    """`templates/persona/career.md` 전문."""
    return _persona_format(CAREER_TEMPLATE_PATH, CAREER_FALLBACK, repo_root)


def reset_cache() -> None:
    """테스트용 — 파일을 바꾼 뒤 다시 읽게 한다."""
    _read.cache_clear()
