# @ontology-be — 도구 및 구조

## 작업 디렉토리
- 실제 작업 위치·base 는 dispatch brief 의 `작업 워크트리`·`base 브랜치`가 SSOT
- **첫 액션**: 워크트리에서 `git branch --show-current` 확인 →
  `app/ontology-agent/pyproject.toml` → 구조를 Glob 으로 파악

## 탐색 경로 (레포 루트 기준)
```
app/ontology-agent/main.py     # FastAPI 엔트리
app/ontology-agent/config.py   # 설정 (ONTOLOGY_DATA_DIR 등 env)
app/ontology-agent/build/      # 브론즈 적재 + 실버·골드 빌드 (DB 이식)
app/ontology-agent/tools/      # MCP 서버 — 조회 도구 4종
app/ontology-agent/api/        # 화면·채팅 API 라우터
app/ontology-agent/static/     # 단일 페이지
app/ontology-agent/tests/      # pytest
```

## 참조 전용 (수정 금지)
```
app/back/service/chat/         # open-kknaks 제출·스트림 패턴 (submission·runtime·consumer)
app/back/config.py             # pydantic-settings 패턴
app/mcp/                       # FastMCP HTTP 서버 패턴
<브리프 §1 의 원천 절대경로>     # 기존 빌드 스크립트·데이터 — read-only
```

## 자주 쓰는 명령
- `cd app/ontology-agent && uv run pytest -q tests/<파일>`
- `cd app/ontology-agent && ONTOLOGY_DATA_DIR=<브리프 지정 경로> uv run python -m build.<모듈>`

## 금지 사항
- `app/back/`·`app/front/`·`app/mcp/`·`para/`·`orchestration/`·`reference/` 수정 금지
- 원천 데이터 복사·커밋 금지 (PII — gitignore 대상)
- git commit·push·PR 금지 — 워크트리에 변경만 남긴다
