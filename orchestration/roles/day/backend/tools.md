# @day-backend — 도구 및 구조

- **가장 먼저 읽는다**: `/Users/kknaks/git/CENTURION_DAY` 의 `AGENTS.md`(dev — `git show origin/dev:AGENTS.md`) — 저장소 구조 · 계층 규칙 · 외부 CRM 연동 · 웹 화면 · 앱 규칙의 정본.

## 작업 위치
- 워크트리 · base 는 브리프가 SSOT. 첫 액션: `git branch --show-current` → SPEC · WORK(브리프 §1 절대경로) 통독.

## 레이아웃
- 레포 `AGENTS.md` 「저장소 구조」가 정본. 범위는 `backend/` 중 브리프가 지정한 곳.

## 명령
- `cd backend && uv sync && uv run pytest <네가 만든 테스트> && uv run ruff check <네가 만진 파일>`

## 금지
- 브리프 밖 경로 수정 · 커밋 · push · PR · 사용자 포트/프로세스 종료.

## KOS 확인 (조회만)
- 사용법 · 키 위치 · HAR 위치는 `orchestration/config/projects/day.json` 의 `repos.reference_kos.notes` 가 정본.
- 조회(queries)와 토큰 받기만. commands(생성 · 수정 · 삭제 · 단계 변경) 금지. 데모 지점 키(`KOS_API_tenent_dev`)만 — 명동점 키 금지.
- 공개 API 에 없는 건 HAR · HAR 리포트로 확인하고, 그래도 없으면 추측하지 말고 `[질문]` 으로 HAR 를 요청한다.
- 응답 원문 · 개인정보를 리포트에 붙이지 않는다 — 필드 이름 · 타입 · 건수만.

## 데이터 기본 규칙
- `orchestration/config/projects/day.json` 의 `data_rules` 를 먼저 읽는다 — 원장 · 동기화 · 사본 범위 · 외부 연결 · 차트번호.
