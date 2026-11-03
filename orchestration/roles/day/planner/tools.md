# @day-planner — 도구 및 제한

- **가장 먼저 읽는다**: `/Users/kknaks/git/CENTURION_DAY` 의 `AGENTS.md`(v2-dev — `git show origin/v2-dev:AGENTS.md`) — 저장소 구조 · 계층 규칙 · 외부 CRM 연동 · 웹 화면 · 앱 규칙의 정본.

## 작업 디렉토리
- 실제 작업 위치와 base 는 dispatch brief 의 `작업 워크트리` · `base 브랜치`가 SSOT 다
- **첫 액션**: brief 의 작업 워크트리에서 `README.md` · `AGENTS.md` · `context/products.md`(DAY 행) · `products/day/` 인덱스

## 읽기 전용 참고
- 기존 코드: `/Users/kknaks/git/CENTURION_DAY` 의 `origin/stg` ref (`git show origin/stg:<path>`) — 체크아웃 수정 금지
- 참고 레포: `/Users/kknaks/git/toy_pr2/cc-prototype`

## 금지 사항
- canonical(`/Users/kknaks/git/harness_works/mediness-mediness`) 수정 금지 — 워크트리에서만 작업
- `products/day/` 밖 파일 수정 금지 · git commit · push · PR 금지

## KOS 확인 (조회만)
- 사용법 · 키 위치 · HAR 위치는 `orchestration/config/projects/day.json` 의 `repos.reference_kos.notes` 가 정본.
- 조회(queries)와 토큰 받기만. commands(생성 · 수정 · 삭제 · 단계 변경) 금지. 데모 지점 키(`KOS_API_tenent_dev`)만 — 명동점 키 금지.
- 공개 API 에 없는 건 HAR · HAR 리포트로 확인하고, 그래도 없으면 추측하지 말고 `[질문]` 으로 HAR 를 요청한다.
- 응답 원문 · 개인정보를 리포트에 붙이지 않는다 — 필드 이름 · 타입 · 건수만.

## 데이터 기본 규칙
- `orchestration/config/projects/day.json` 의 `data_rules` 를 먼저 읽는다 — 원장 · 동기화 · 사본 범위 · 외부 연결 · 차트번호.
