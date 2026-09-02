"""온톨로지 데모 — FastAPI 엔트리 (기록 09).

계층 탐색(브론즈~골드) + KPI 모니터링 + 원인 분석 그래프 + AI 채팅.
라우터는 api/, 화면은 static/ 단일 페이지.
"""

from fastapi import FastAPI

app = FastAPI(title="온톨로지 데모 — 세라미크의원 강남")


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}
