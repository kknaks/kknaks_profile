# @mykakao-be — 기술 스택

- Python + FastAPI + Uvicorn
- SQLAlchemy 2.0 + sqlcipher3 (SQLCipher 복호화 드라이버)
- open-kknaks 2.0.2 (AgentClient/RedisBroker — 제출·스트림 구독) + codex CLI
- Redis (큐 브로커) — NAMESPACE=`mykakao`, QUEUES=`default`
- SSE (Server-Sent Events) — 실시간 메시지 스트림 + 요약 스트림
- pytest

> `requirements.txt` 가 의존성 SSOT다. pyproject·uv 는 이 레포에 없다.

## 핵심 원칙
- 최소 변경 · 기존 컨벤션 우선 · 테스트 없이 완료 선언 금지 · 원본 DB 는 읽기만
