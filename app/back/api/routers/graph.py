"""GET /api/graph — 전역 지식그래프 (KDEV-WORK-008 §API 계약, KDEV-SPEC-002 §4).

읽기 전용. `get_data()["_graph"]` (notes + products 결합 그래프) 를 메모리 dict 그대로 반환.
`_graph_error` 가 있어도 200 + 빈 그래프 — 부팅 차단은 enforce(WORK-007)가 별도로 담당.
"""

from fastapi import APIRouter

router = APIRouter()

_EMPTY = {"nodes": [], "edges": [], "backlinks": {}}


@router.get("/api/graph")
def get_graph():
    """전역 그래프 — nodes[{id,type,title,archived}] / edges[{source,target,type,dir}] / backlinks{stem:[stem]}."""
    from main import get_data

    return get_data().get("_graph") or _EMPTY
