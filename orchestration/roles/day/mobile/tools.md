# @day-mobile — 도구 및 구조

- **가장 먼저 읽는다**: `/Users/kknaks/git/CENTURION_DAY` 의 `AGENTS.md`(dev — `git show origin/dev:AGENTS.md`) — 저장소 구조 · 계층 규칙 · 외부 CRM 연동 · 웹 화면 · 앱 규칙의 정본.

## 작업 위치
- 워크트리 · base 는 브리프가 SSOT. 첫 액션: `git branch --show-current` → SPEC · WORK · 시안(브리프 §1 절대경로) 통독.

## 명령
- `cd app && flutter analyze && flutter test && flutter build ios --no-codesign` — 각 1회(전체 빌드는 Phase 마지막)

## 금지
- 브리프 밖 경로 수정 · 서명 · 업로드 · 커밋 · push · PR.
