# 리뷰 리포트 — SPEC-001 전체 권한 계정 한 줄 · #230 contract v5 (2026-11-06)

**대상**
- mediness 워크트리 `spec-001-login-session.md` diff(규칙 9 아래 한 줄)
- `delivery/v2-board-backend.json`(v5)을 `v2-board-backend.v4.json` 과 대조
- Issue #230(메타 `contract_version=5`)

**기준**: 원천 `erd/04-staff.md` L134 「전체 권한 계정」

lint `--strict` → 0 error · `products/day/` 경고 0.

## 판정: PASS

### SPEC-001 줄 ↔ 원천 L134

새 줄은 규칙 9(L297) 아래 하위 항목(L298)으로 들어갔다. 원천과 한 칸씩 맞춰 봤다.

| 원천 L134 | SPEC-001 L298 | 판정 |
|---|---|---|
| env `DAY_ADMIN_EMAILS`(KOS 로그인 이메일 목록) | 같음 | 같음 |
| `job_role_permission` 과 관계없이 모든 권한 | 같음 | 같음 |
| 권한 검사 한 곳에서만 보고 | 같음 | 같음 |
| 이 경로로 통과한 요청은 로그에 표시 | 같음 | 같음 |
| 가짜 계정을 만들지 않는다(실제 KOS 계정을 env 로 열기만) | 같음 | 같음 |
| 권한 표 시드는 만들지 않는다 | 같음 | 같음 |
| 값은 사용자가 직접 env 에 넣는다(dev = local.env · 운영 = 비움 또는 실제 관리자) | 같음 | 같음 |
| 근거 | (사용자 2026-11-06 · 원천 04 「전체 권한 계정」) | 맞음 |

원천에 없는 내용은 들어가지 않았다.

### #230 v5 — v4 와 다른 것

v4 와 줄 단위로 비교했다. 바뀐 것은 아래 셋뿐이다. 위험 L3 · target · Non-Goal · Review Surface · execution 은 v4 그대로다.

| 자리 | 바뀐 것 | 판정 |
|---|---|---|
| Target Delta | 한 줄 추가 — 권한 검사(`board` · `board.accept`)에 `DAY_ADMIN_EMAILS` 를 반영한다 · 검사는 한 곳에서만 · 통과한 요청은 로그에 표시 · 가짜 계정 · 시드 없음 · `*.env.example` 엔 이름만 | 지시 범위대로 |
| A10 | 신설 — 목록 계정은 통과하고 로그가 남는다 · 목록 밖 계정은 권한 행대로 · 예시 파일엔 값 없음(단위 · API 테스트) | 지시 범위대로 |
| A8 | 끝에 한 문장 추가 — 「데모 계정은 `DAY_ADMIN_EMAILS`(사용자 local.env)로 시술 현황을 연다」 | 지시 범위대로 · 나머지 문장(W8 대기 포함)은 그대로 |

### 라벨

`delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending` — **승인 없음**.

## 참고 (지적 아님)

- SPEC-001 케이스 매트릭스의 `forbidden` 줄은 「직무에 권한 행이 없으면 모든 동작이 여기」 그대로다. 규칙 9 의 하위 항목이 예외를 정하므로 모순은 아니다. 다음 판에 그 줄에 「(전체 권한 계정 제외 — 규칙 9)」를 덧붙이면 읽는 사람이 놓치지 않는다.
- 「권한 검사 한 곳」은 #227 이 만든 `session.py` `require_permission` 이 된다. #230 이 그 함수를 고치게 된다는 점만 구현 브리프에 적어 두면 된다.
