"""GET /api/posts, /api/posts/{id} — 공개 글 (KDEV-DEC-021 / KDEV-SPEC-001).

`persona/posts/` 는 `resources/source/` 와 **1:1** 이고 자료 하나를 압축한 글이다.
타입이 둘인데 갈리는 기준은 **누가 말한 것인가**다.

    post_article  자료가 말한 요지를 압축      (스크랩)
    post_note     내가 이해한 것을 내 언어로   (공부)

목록·상세 모양은 `contents` 를 그대로 따른다 — 화면이 같은 규약을 두 번 배우지
않게 하려는 것이고, 다른 점은 영상이 없어 `youtubeId`·`duration` 이 없다는 것뿐이다.
"""

from fastapi import APIRouter, HTTPException, Query

from core.i18n import apply_i18n

router = APIRouter()

#: 목록 카드가 쓰는 필드. 본문(`body`)은 **상세에서만** 낸다 — 글 수십 개의 전문을
#: 목록 응답에 실으면 첫 화면이 통째로 무거워진다.
_CARD = ("id", "type", "title", "date", "summary", "tags", "stack", "up")


def _card(post: dict) -> dict:
    return {k: post.get(k) for k in _CARD}


@router.get("/api/posts")
def get_posts(
    lang: str = Query("ko", pattern="^(ko|en)$"),
    limit: int = Query(50, ge=1, le=200),
    type: str | None = Query(None, pattern="^(post_article|post_note)$"),
):
    from main import get_data

    items = get_data().get("posts", [])  # 이미 date desc 정렬
    if type:
        items = [p for p in items if p.get("type") == type]

    response = {
        "posts": {
            "subtitle": {"ko": "읽고 정리한 것", "en": "What I read and wrote up"},
            "totalCount": len(items),
        },
        "posts[]": [_card(p) for p in items[:limit]],
    }
    return apply_i18n(response, lang)


@router.get("/api/posts/{post_id}")
def get_post_detail(post_id: str, lang: str = Query("ko", pattern="^(ko|en)$")):
    from main import get_data

    items = get_data().get("posts", [])
    idx = next((i for i, p in enumerate(items) if p.get("id") == post_id), None)
    if idx is None:
        raise HTTPException(404, f"post not found: {post_id}")

    item = items[idx]
    # date desc 정렬이라 index 0 이 최신 — `contents` 상세와 같은 규약이다.
    newer = items[idx - 1] if idx > 0 else None
    older = items[idx + 1] if idx + 1 < len(items) else None

    response = {
        "posts.detail": {
            **_card(item),
            "body": item.get("body", ""),
            "newer": {"id": newer["id"], "title": newer["title"]} if newer else None,
            "older": {"id": older["id"], "title": older["title"]} if older else None,
        }
    }
    return apply_i18n(response, lang)
