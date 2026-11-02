# @mykakao-be — 도구 및 구조

## 작업 디렉토리
- 실제 작업 위치·base 는 dispatch brief 의 `작업 워크트리`·`base 브랜치`가 SSOT
- **첫 액션**: 워크트리에서 `git branch --show-current` 확인 → `README.md` → `backend/` 를 읽는다

## 탐색 경로 (레포 루트 기준)
```
backend/main.py        # FastAPI — REST + SSE + 요약 + 정적 서빙
backend/db.py          # 키 주입 SQLAlchemy 엔진 (mode=ro, NullPool)
backend/models.py      # NTChatRoom / NTChatMessage / NTUser
backend/extract.py     # device UUID + user_id 복구 + 키 유도 (⚠ macOS 전용)
backend/summarize.py   # 메시지 조회 → 프롬프트 조립 → codex submit/stream
backend/tests/         # pytest
frontend/              # (FE 담당 — 수정 금지)
worker/ docker-compose.yml Dockerfile.worker   # (infra 담당 — 수정 금지)
```

## 자주 쓰는 명령
- `python -m pytest -q backend/tests/<파일>`
- 기동은 `./run.sh` (macOS 전제) — 워커가 직접 띄우지 않는다. 실기동 검증은 코디네이터 몫

## 금지 사항
- `frontend/`·`worker/`·compose 수정 금지 · 문서 SoT 수정 금지 (코디네이터)
- git commit·push·PR 금지 — 워크트리에 변경만 남긴다
- 카톡 원본 DB 쓰기·복사·키 값 로깅 금지
