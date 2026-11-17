## 마감 — contract v2 · plan 승인 · 머지 · dev 배포

**결과 계약** contract_version 2 · baseline `51f85837`(mediness#946 머지) · plan_digest `sha256:9db0b7aa001862acaa45c83b93a337616cbe41fa698488bdd97a138934240fa5` — 담당자 kknaksss 승인(2026-11-17 · 로컬 확인 뒤).

### 들어간 것
- K-1 KOS sign-in 401 을 본문 `message == SignInLimitExceeded` 로 「기기 제한」 판정(틀린 비밀번호와 가름)
- K-2 시스템 계정 — KOS 요청 UA 끝 환경 표시(`KOS_CLIENT_TAG` local/dev/prod) · 막혔을 때만 같은 UA 로그인 중 가장 오래된 1개 해제 → 1회 재시도 · 표시 없으면 정리 안 함
- K-3 직원 — **웹만** 기기 선택 단계(KOS 화면 글자 · 병원 고르기와 같은 틀 · 「처음으로」 없음) → `POST /login/device` → 해제 → 다시 로그인 → 기존 흐름. 비밀번호는 Redis 5분 암호문 임시 값에만(종류 표시 · 꺼내면 지움)
- 앱 JSON 로그인 = 지금과 같은 401 `invalid_credentials`(새 코드 · 새 단계 없음 · 앱 코드 변경 0)
- K-4 로그아웃 때 KOS 해제 안 함(변경 없음)
- 같은 PR 의 SPEC-002 개정 ㉓ — 차트 여는 곳 = 시술명 영역 전체(툴팁 「차트 작성」만) · 정렬 탭 「시술대기 순」 · 「방별 순」
- migration 0

### 근거
- Code PR CENTURION_DAY#257 머지 — dev `a6aa4ba5`
- Spec PR mediness#946 머지 — main `51f85837`(SPEC-001 개정 ⑨ · SPEC-003 ⑱ · SPEC-002 ㉓ · SPEC-000)
- 검증: backend 전체 1359 passed · ruff 통과 · 코드 검수 PASS(FAIL 0) · 로컬 day-local 사용자 확인 · 로컬 시스템 계정 세션 `(local)` 표시 실물 확인 · lint-pipeline --strict 0 error
- dev 배포: GitHub Actions `DAY dev` run 44062996534 성공

### 남은 것 (이 Issue 밖)
- prod 배포 — 2026-11-17 20시(사용자) · `KOS_CLIENT_TAG=prod` · migration 없음
- 배포 뒤 표시 없는 옛 시스템 계정 KOS 세션 한 번 정리(자동 정리 대상 아님)
- 앱 기기 선택 단계 — 다음 앱 버전(OQ-K14)
- 열린 것: OQ-K6 목록에서 DAY 서버 로그인 구분 · OQ-K11 해제 뒤 다른 DAY 세션 KOS 쓰기 실물 · OQ-K16 시스템 계정 로그인 쌓임 원인

spec-sync closeout 은 제품 레포 Delivery 에서 돌지 않는 알려진 제약(mediness#749 — dashboard projection digest 없음)이라 이 댓글과 close 로 대신한다.
