# @day-frontend — 도구 및 구조

- **가장 먼저 읽는다**: `/Users/kknaks/git/CENTURION_DAY` 의 `AGENTS.md`(v2-dev — `git show origin/v2-dev:AGENTS.md`) — 저장소 구조 · 계층 규칙 · 외부 CRM 연동 · 웹 화면 · 앱 규칙의 정본.

## 작업 위치
- 워크트리 · base 는 브리프가 SSOT. 첫 액션: `git branch --show-current` → SPEC · WORK · 시안(브리프 §1 절대경로) 통독.

## 본 (read-only, ref 로 읽는다 — 체크아웃은 rc.2)
- `git -C /Users/kknaks/git/centurion show origin/main:docs/development/medikit-htmx-design-guide.md`
- `origin/main:docs/development/medikit-htmx-kit/` (README · example.html · medikit.css · medikit.js)
- `origin/main:backend/admin/` — `web.py` · `templates/base.html` · `templates/ui.html` · `templates/partials/` · `static/admin.js` · `styles/`

## 명령
- `uv run pytest -q <네가 만든 화면 테스트>` — 1회
- `grep -rn "<script>" <templates>` · `grep -rn "style=" <templates>` 로 인라인 0 확인

## 금지
- 브리프 밖 경로 수정 · 커밋 · push · PR · 사용자 포트/프로세스 종료.
