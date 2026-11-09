# @day-reviewer — 도구

- **가장 먼저 읽는다**: `/Users/kknaks/git/CENTURION_DAY` 의 `AGENTS.md`(dev — `git show origin/dev:AGENTS.md`) — 저장소 구조 · 계층 규칙 · 외부 CRM 연동 · 웹 화면 · 앱 규칙의 정본.

- `git diff <base>...HEAD` + untracked 로 범위 산정.
- 수정 · 테스트 실행 금지(결과가 필요하면 워커 리포트를 인용). 문서 모드의 lint-pipeline 1회만 예외.

## 데이터 기본 규칙
- `orchestration/config/projects/day.json` 의 `data_rules` 를 먼저 읽는다 — 원장 · 동기화 · 사본 범위 · 외부 연결 · 차트번호.
