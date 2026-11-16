# @interpret-pwa-backend — 도구 및 구조

## 작업 위치
- 워크트리·base 는 브리프가 SSOT. 첫 액션: `git branch --show-current` → SPEC·WORK(브리프 §1 절대경로) 통독.

## 레이아웃 (SPEC 우선)
```
back/pyproject.toml
back/app/main.py        FastAPI 앱 · 라우터 등록
back/app/api/           router
back/app/service/
back/app/repository/
back/app/schemas/       front 계약
back/tests/
back/Dockerfile
docker-compose.yml      back · front 를 띄운다
```

## 명령
- `cd back && uv sync && uv run pytest && uv run ruff check .`
- 로컬 기동은 SPEC 이 정한 포트로.

## 금지
- front/ 수정 · 커밋·push·PR · 사용자 포트/프로세스 종료.
