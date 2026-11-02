# [writer 2차] mediness prod 에서 4명의 조직 정보로 시드를 채울 수 있는지 조사 (READ-ONLY)

너는 1차(시드 경로 조사)를 끝낸 writer 다. 1차 산출물을 먼저 읽어라:
- `orchestration/work/strong-hajin-deploy/research-seed-path.md`
- `reference/2026-09-30-strong-hain-seed/README.md` + CSV 9개 (시드 양식 — 조직도 전체로 확장됨)

## 질문
mediness **prod** DB 에 있는 **구성원A · 구성원C · 구성원B · 구성원D** 네 사람의 조직 정보로
시드 양식 9표를 채울 수 있는가. 표·열마다 「mediness 의 어디(테이블.열)에서 온다 / 없다」를 판정하라.

## 접근 (config mediness.json environments)
- `ssh medi-me` → `/opt/homebrew/bin/kubectl` (절대경로 필수) → namespace `mediness-prod`
- 파드 python 은 `/app/.venv/bin/python`. DB 접속 정보는 파드 env 에서 쓴다 — **값을 출력·기록하지 마라**
- 스키마 파악은 mediness 코드(모델)나 `information_schema` 로

## 절대 규칙
- **SELECT 만.** INSERT/UPDATE/DELETE/DDL·alembic·seed·재시작·rollout 금지. 트랜잭션은 read-only 로 연다(`SET TRANSACTION READ ONLY` 또는 `default_transaction_read_only`)
- 네 명 외 다른 사람의 행은 조회 결과에 싣지 마라(조직 단위·직급 목록 같은 어휘는 네 명이 쓰는 것만)
- 리포트에 **전화·생년월일 값은 적지 않는다** — 「있음/없음」만. 이름·메일·조직명·직급·직위는 적어도 된다
- 코드·para·양식 CSV 수정 금지. 이번엔 **채우지 않는다** — 채울 수 있는지만 본다

## 산출물 (이 파일 하나)
`orchestration/work/strong-hajin-deploy/research-mediness-org.md`
1. 결론: 채울 수 있다/부분/없다 한 문단
2. 4명 각각 찾았나(동명이인·없음 포함), 로그인 메일
3. 시드 표·열 ↔ mediness 테이블.열 대응표 (organization_units·grades·positions·jobs·members·appointments·memberships·job_assignments·logins). 없는 것은 「없음」
4. 4명이 속한 조직 트리(상위까지), 직급·직위·직무 값 — 전화·생년월일 제외
5. 갭과 Open Questions (값 변환 규칙이 필요한 곳 — 예: mediness 권한 → role_key)
6. 실행한 쿼리 목록(값 없이 문장만)

## 완료 보고
브리프 §9 와 같은 두 채널. task-id `task_b12450b8e256` · dispatch-id `ctx_9d693170f05a` · 코디 `term_8d586fcb-a104-4f31-9f5f-fd3b659a1d24`.
