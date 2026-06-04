"""메모리 inverted index — notes 검색 (mvp: substring 매칭).

수백 노트 수준에선 substring 매칭이 한국어 토크나이저보다 단순·robust.
formal 토큰 인덱스는 spec-02 §3.9 후속 작업으로.
"""

from __future__ import annotations

from core.i18n import i18n


def search_notes(notes: dict[str, dict], query: str, lang: str = "ko") -> list[dict]:
    """notes(id→note dict) 안에서 query 매칭 → notes.recent[] 형식 list.

    title 매치 우선, body 매치 차순. 같은 우선순위 안에서는 date desc.
    """
    if not query:
        return []
    q = query.lower().strip()
    title_hits: list[tuple[str, dict]] = []
    body_hits: list[tuple[str, dict]] = []

    for nid, n in notes.items():
        title = i18n(n.get("title", ""), lang)
        body = n.get("body", "")
        if q in title.lower():
            title_hits.append((nid, n))
        elif q in body.lower():
            body_hits.append((nid, n))

    # 같은 그룹 내 date desc 정렬
    def by_date(t: tuple[str, dict]) -> str:
        return t[1].get("date", "")

    title_hits.sort(key=by_date, reverse=True)
    body_hits.sort(key=by_date, reverse=True)

    return [_to_recent(nid, n, lang) for nid, n in title_hits + body_hits]


def _to_recent(nid: str, n: dict, lang: str) -> dict:
    """spec-02 §3.7 응답 형식 — id/title/date/path."""
    return {
        "id": nid,
        "title": i18n(n.get("title", ""), lang),
        "date": n.get("date"),
        "path": n.get("group", ""),  # cluster id (label 가공은 frontend 책임)
    }
