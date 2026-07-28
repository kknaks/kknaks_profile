"""교안 형식의 단일 출처 로더 (KDEV-WORK-015 P3 보정).

교안을 만드는 경로가 둘이다 — 승인 게이트의 `derived` 스테이지와 기존
`content_enrich` 잡. 처음에는 8개 섹션 명세를 **양쪽 프롬프트에 각각 적었는데**,
그건 `reference`·`concept` 에서 없앤 이중 SoT 를 교안에서 다시 만드는 것이었다.
한쪽만 고치는 날 두 경로의 산출물이 조용히 갈라진다.

`templates/content.md` 를 SoT 로 두고 양쪽이 그것을 **불러다 쓴다.**

지식 노트처럼 "에이전트가 레포를 읽게" 하지 않는 이유는, `content_enrich` 가
`cwd` 없이 호출돼 레포에 접근할 수 없기 때문이다. 두 경로에 서로 다른 방식을
쓰느니 **한 파일을 양쪽이 싣는** 편이 단순하고, 어차피 고칠 곳은 한 곳이다.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger("kknaks-back.content-format")

TEMPLATE_PATH = "templates/content.md"

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
    """`templates/content.md` 전문.

    프롬프트에 그대로 실린다 — 형식을 고치려면 그 파일만 고친다.
    """
    if repo_root is None:
        import config

        repo_root = config.repo_root()
    return _read(str(repo_root / TEMPLATE_PATH))


def reset_cache() -> None:
    """테스트용 — 파일을 바꾼 뒤 다시 읽게 한다."""
    _read.cache_clear()
