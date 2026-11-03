# @day-researcher — 도구

- **가장 먼저 읽는다**: `/Users/kknaks/git/CENTURION_DAY` 의 `AGENTS.md`(v2-dev — `git show origin/v2-dev:AGENTS.md`) — 저장소 구조 · 계층 규칙 · 외부 CRM 연동 · 웹 화면 · 앱 규칙의 정본.

- 읽을 곳(전부 read-only):
  - 기존 코드: `/Users/kknaks/git/CENTURION_DAY` — `origin/stg` ref 로만 읽는다. 사용자 체크아웃 · 작업트리 파일 수정 금지
  - 참고: `/Users/kknaks/git/toy_pr2/cc-prototype` (origin/main)
  - 문서: `/Users/kknaks/git/harness_works/mediness-mediness` (origin/main)
- 첫 액션: 브리프 §1 의 질문 목록 통독.
- 산출물은 브리프가 지정한 경로의 리포트 1개.

## KOS 확인 (조회만)
- 사용법 · 키 위치 · HAR 위치는 `orchestration/config/projects/day.json` 의 `repos.reference_kos.notes` 가 정본.
- 조회(queries)와 토큰 받기만. commands(생성 · 수정 · 삭제 · 단계 변경) 금지. 데모 지점 키(`KOS_API_tenent_dev`)만 — 명동점 키 금지.
- 공개 API 에 없는 건 HAR · HAR 리포트로 확인하고, 그래도 없으면 추측하지 말고 `[질문]` 으로 HAR 를 요청한다.
- 응답 원문 · 개인정보를 리포트에 붙이지 않는다 — 필드 이름 · 타입 · 건수만.

## 데이터 기본 규칙
- `orchestration/config/projects/day.json` 의 `data_rules` 를 먼저 읽는다 — 원장 · 동기화 · 사본 범위 · 외부 연결 · 차트번호.
