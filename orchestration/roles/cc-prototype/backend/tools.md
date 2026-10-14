# @cc-prototype-backend — 도구 및 구조

## 작업 위치
- 워크트리·base 는 브리프가 SSOT. 첫 액션: `git branch --show-current` → 기능의 SPEC·WORK(브리프 §1 절대경로) 통독.

## 레이아웃 (SPEC 우선)
```
<기능>/back/pyproject.toml
<기능>/back/app/main.py        FastAPI 앱 · 라우터 등록
<기능>/back/app/api/           router
<기능>/back/app/service/
<기능>/back/app/repository/
<기능>/back/app/schemas/       front 계약
<기능>/back/tests/
<기능>/back/Dockerfile
<기능>/docker-compose.yml      그 기능만 띄운다
```

## 명령
- `cd <기능>/back && uv sync && uv run pytest && uv run ruff check .`
- 로컬 기동은 기능의 SPEC 이 정한 포트로.

## 금지
- 다른 기능 폴더·레포 루트 공용 파일 수정 · 커밋·push·PR · 사용자 포트/프로세스 종료.
