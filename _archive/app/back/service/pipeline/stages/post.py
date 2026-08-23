"""`post` 스테이지 — 공개 글 (KDEV-DEC-020 D3 / KDEV-DEC-021).

`persona/posts/` 의 글 하나를 만든다. `resources/source/` 의 원본 정리와 **1:1** 이고
`up:` 으로 그것을 가리킨다 — `up:` 이 하나라는 것이 「한 글 = 한 자료」의 제약이다.

타입이 둘이다. 갈리는 기준은 **누가 말한 것인가**다.

    post_article  자료가 말한 요지를 압축      (스크랩)
    post_note     내가 이해한 것을 내 언어로   (공부)

`derived`(교안)와 다른 자리다 — 교안은 **학습 가능한 장문**이고 글은 **핵심 압축**이다.
유튜브는 교안을 만들고(`derived`), 블로그·공부 노트는 글을 만든다.

형식 규칙을 이 프롬프트에 복사하지 않는다. 양식 원천은 `templates/persona/post-*.md`
한 곳이고, 복사하는 순간 한쪽만 고쳐지는 날 조용히 어긋난다.
"""

from __future__ import annotations

import re
from typing import Any

import frontmatter

from ..executor import AgentStage
from ..gates import GateError, GenerationInput
from .common import (
    OUTPUT_CONTRACT,
    context_payload,
    parse_note_output,
)

POSTS_DIR = "persona/posts"

#: 글 stem 은 날짜를 붙이지 않는다 — 자료의 날짜는 `up:` 이 가리키는 source 가 갖는다.
POST_STEM_RE = re.compile(r"(?!\d{4}-\d{2}-\d{2})[a-z0-9]+(?:-[a-z0-9]+)*")

POST_TYPES = ("post_article", "post_note")

INSTRUCTION = """이 자료의 **공개 글**(post) 을 작성하라.

작성 전에 양식을 **반드시 읽어라.** 이 프롬프트에 복사돼 있지 않다.

1. `rules/persona-artifacts.md` — 공개 글의 규약
2. `templates/persona/post-article.md` — **스크랩**(자료가 말한 요지) 을 쓸 때
3. `templates/persona/post-note.md` — **공부**(내가 이해한 것) 를 쓸 때

읽지 않고 쓰면 형식이 어긋나 발행 전 검증에서 거부된다.

지켜야 할 것:
- `type` 은 `post_article` 또는 `post_note` 다. **누가 말한 것인가**로 고른다 —
  자료의 요지면 article, 내가 이해한 것이면 note.
- `up:` 에 이 글이 압축한 **source stem 하나**를 넣는다. 여럿을 묶는 글은 이 계열이 아니다.
- 본문은 다섯 절이다: 주제 · 개념(mermaid) · 사용 예시 · 리스크 · 비슷한 개념.
- 개념 상세를 여기 쓰지 않는다. 요지만 쓰고 `[[concept]]` 로 위임한다 — 상세의 SoT 는
  `resources/concept/` 한 곳이다.
- 「리스크」를 비우지 않는다. 비면 대개 덜 읽은 것이다.
- 예시를 지어내지 않는다. 자료에 없으면 쓰지 않는다.

{output}"""


def check_post(stem: str, content: str) -> dict[str, Any]:
    """게이트 시점의 가벼운 검사. 전체 검증은 발행 직전에 돈다.

    `check_note` 를 쓰지 않는 이유는 **타입이 둘**이라서다 — 그쪽은 `expected_type`
    하나만 받는다.
    """
    if not POST_STEM_RE.fullmatch(stem):
        raise GateError("INVALID_NOTE_STEM", f"'{stem}' 은 파일명 규약에 맞지 않는다")
    try:
        post = frontmatter.loads(content)
    except Exception as exc:  # noqa: BLE001
        raise GateError("INVALID_NOTE_OUTPUT", f"frontmatter 파싱 실패: {exc}") from exc

    meta = post.metadata
    declared = meta.get("type")
    if declared not in POST_TYPES:
        raise GateError(
            "INVALID_NOTE_OUTPUT",
            f"type 이 {declared} 다 — {' 또는 '.join(POST_TYPES)} 여야 한다",
        )

    missing = [f for f in ("title", "date") if not meta.get(f)]
    if missing:
        raise GateError("MISSING_NOTE_FIELD", f"필수 필드 누락: {', '.join(missing)}")

    declared_id = str(meta.get("id") or "").strip()
    if declared_id and declared_id != stem:
        raise GateError("INVALID_NOTE_OUTPUT", f"id({declared_id}) 와 stem({stem}) 이 다르다")

    # **`up:` 은 정확히 하나다.** 이것이 「한 글 = 한 자료」의 제약이고, 여럿을 묶는
    # 글은 이 계열이 아니라는 판정이 여기서 난다.
    raw_up = meta.get("up") or []
    ups = [raw_up] if isinstance(raw_up, str) else list(raw_up)
    if len(ups) != 1:
        raise GateError(
            "INVALID_POST_UP",
            f"up: 은 source stem 하나여야 한다 — {len(ups)}개다",
        )
    return meta


class PostStage(AgentStage):
    """open-kknaks 로 공개 글 초안을 만든다."""

    source = "pipeline-post"

    def prompt(self, request: GenerationInput) -> str:
        return INSTRUCTION.format(output=OUTPUT_CONTRACT)

    def payload(self, request: GenerationInput) -> dict[str, Any]:
        return context_payload(request)

    def parse(self, raw: str, request: GenerationInput) -> dict[str, Any]:
        stem, content = parse_note_output(raw)
        meta = check_post(stem, content)
        return {
            "filename_stem": stem,
            "content": content,
            "note_type": meta["type"],
            # 경로는 시스템이 조립한다 — `persona/posts/` 는 flat 이다.
            "target_path": f"{POSTS_DIR}/{stem}.md",
        }
