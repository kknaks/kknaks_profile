"""slug 파싱·정규화 (KDEV-WORK-018 P3).

**순수 함수만 둔다** — 도메인도 DB 도 HTTP 도 모른다(`40-architecture/system`
「백엔드 계층 규약」). 여기 있는 것들은 문자열을 문자열로 바꾸거나 형태를 판정할 뿐이라
service·repository 어느 쪽에서 불러도 같은 답을 낸다.
"""

from __future__ import annotations

import re

#: `github.com/owner/name` · `https://github.com/owner/name` 어느 쪽이든 받는다.
_REPO_URL = re.compile(r"(?:https?://)?(?:www\.)?github\.com/([^/\s]+/[^/\s#?]+)")

#: 제품 디렉토리명. 소문자·숫자·하이픈. 앞뒤 하이픈과 연속 하이픈을 막는다 —
#: 경로가 되는 값이라 `--` 나 `-x` 를 허용하면 사람이 읽을 때 오타와 구분이 안 된다.
_PRODUCT_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

#: `P-15`. 두 자리 이상을 허용한다 — 100번째 카드에서 형식이 바뀌면 정렬이 깨진다.
_CARD_ID = re.compile(r"^P-(\d{2,})$")


def parse_repo_slug(raw: str) -> str | None:
    """`owner/name` 을 뽑는다. 못 읽으면 `None`.

    URL 접두를 떼는 것이 핵심이다 — 안 떼면 클론 URL 이
    `github.com/github.com/owner/name` 이 된다.
    """
    match = _REPO_URL.search(raw or "")
    if match:
        return match.group(1).removesuffix(".git")
    cleaned = (raw or "").strip().strip("/")
    if cleaned.count("/") != 1 or " " in cleaned or not cleaned:
        return None
    owner, _, name = cleaned.partition("/")
    return cleaned if owner and name else None


def is_valid_product_slug(value: str) -> bool:
    """디렉토리명으로 쓸 수 있는 형태인가. **경로 조립 전에 본다.**"""
    return bool(_PRODUCT_SLUG.match(value or ""))


def product_dir(slug: str) -> str:
    """제품 디렉토리의 **레포 루트 기준 상대 경로**.

    경로를 DB 에 저장하지 않고 여기서 만든다 — 저장하면 `slug` 와 두 벌이 되어
    한쪽만 고쳐지는 날 어긋난다(KDEV-DEC-017 C안 기각).
    """
    return f"products/{slug}"


def next_card_id(existing: list[str]) -> str:
    """`P-NN` 채번. 기존 최대값 + 1.

    **결번을 메우지 않는다.** 지워진 카드의 번호를 재사용하면 자산 경로
    (`/assets/projects/P-NN/`)가 과거 이미지를 가리킨다(KDEV-DEC-017 D6).
    """
    numbers = [
        int(m.group(1)) for raw in existing if (m := _CARD_ID.match(str(raw).strip()))
    ]
    return f"P-{max(numbers, default=0) + 1:02d}"
