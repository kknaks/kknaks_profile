"""온톨로지 데모 — FastAPI 엔트리.

**백엔드는 API 서버다**(DEC-004 D3) — 템플릿·static 페이지를 내보내지 않는다.
화면은 `app/front/` 의 3페이지가 갖고, 이 앱은 그 페이지가 부르는 계약만 제공한다.

전 API 앞에 접속 게이트가 선다(SPEC-003 S-5). 세션 없으면 401 `NO_SESSION` 이고,
비인증 경로는 `/health` 와 `/api/auth/session` **둘뿐**이다 — 예외를 늘리지 않는다.
"""

from fastapi import Depends, FastAPI

from api.auth_router import router as auth_router
from api.deps import require_session
from api.layers_router import router as layers_router
from api.monitoring_router import graph_router, kpi_router
from db.connection import build_stamp, connect_ro

app = FastAPI(
    title="온톨로지 데모 — 세라미크의원 강남",
    description="계층 탐색 · KPI 모니터링 · 원인 분석 그래프. 데이터는 일 1회 갱신된다.",
)

app.include_router(auth_router)
app.include_router(layers_router)
app.include_router(kpi_router)
app.include_router(graph_router)


@app.get("/health")
def health() -> dict:
    """기동 확인 — 세션 없이 부를 수 있는 유일한 비인증 경로(게이트 밖)."""
    return {"ok": True}


@app.get("/api/meta/build", dependencies=[Depends(require_session)])
def build_info() -> dict:
    """빌드 표식 — 서빙 중인 DB 가 어느 빌드인지.

    표식이 없으면 미빌드·실패 빌드다. 조회 API 는 그 상태에서 503 을 낸다.

    **세션 뒤에 둔다.** 행수·노드수는 PII 가 아니지만 데이터셋 규모라 미인증으로 내보낼
    이유가 없고, AC-1(「세션 없이 부른 **모든** API 가 401」)의 예외를 늘리지 않는다.
    """
    try:
        conn = connect_ro(require_build=False)
    except FileNotFoundError:
        return {"built": False, "reason": "DB 파일이 없다"}
    try:
        stamp = build_stamp(conn)
    finally:
        conn.close()
    if stamp is None:
        return {"built": False, "reason": "빌드 표식이 없다 — 게이트를 통과하지 못한 DB"}
    return {"built": True, **dict(stamp)}
