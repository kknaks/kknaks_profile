# 리뷰 리포트 — day-app / WP(Delivery request) (2026-11-09)

- 대상: `orchestration/work/day-app/delivery-request.json`(112줄 · CLI 입력 — 원장은 생성될 GitHub Delivery Issue) · `planner-wp-report.md`
- 대조: `wp-brief.md` §3 · `_RESUME.md` 결정 · `review-policy-report.md` · SPEC-003(로컬 리뷰 통과 초안) · mediness `rules/delivery-workflow.md` · `.agents/skills/start-delivery/SKILL.md` · `tools/harness/references/requests.md` · `delivery-request.schema.json`(+ `delivery-issue.schema.json`) · CENTURION_DAY `origin/dev` 91728737
- read-only · CLI `--plan`/`--apply` · GitHub 쓰기 · 승인 receipt 없음

## 판정: WARN

결과 계약 · 범위 · 의존성은 브리프와 맞고, Stable SPEC으로 둔갑시킨 곳도 없다. FAIL은 없다. 다만 **완료 조건에 「이 Delivery 안에서 할 수 없는 실물 검증」이 표시 없이 섞여 있다**(W-1). 경로 2개가 실제와 다르다(W-2). **rollback 하나는 환경 격리를 깨는 방향인데 안전한 롤백처럼 적혔다**(W-3 — 우선 고칠 것). 셋 다 JSON 몇 줄만 고치면 된다.
**이 WP 리뷰 PASS/WARN은 코드 구현 승인도, 실연동 완료도 아니다.** L3 사람 계약 승인 gate는 CLI 결과대로 남는다.

## 통과 확인

| 항목 | 결과 |
|---|---|
| JSON · schema | 파싱 OK · Draft 2020-12 검증 **오류 0**(request + issue `execution` 참조 · `uv run --with jsonschema`). 필수 11칸 모두 있음 · `idempotency_key` 패턴 맞음 |
| 결과 계약 칸 | `day/day-app` · `day` · `products/day` · v1 · **L3** · target `DAY-SPEC-003` · `DAY-SPEC-001` (L2-11) |
| baseline | `b4cd1a004cd99c8e57761ad8cccd434d5e237b38` = 이번에 `git fetch origin main` 한 뒤의 `origin/main`(뒤에 새 커밋 없음). main `products/day/20-spec/`에 SPEC-003 없음 · SPEC-001은 draft · 「앱 환경 연결」 절 없음 → `spec-baseline:pending`이 맞다(delivery-workflow L29 · L54 · start-delivery L19). review_surface L49가 pending · 머지 뒤 재결속(version+1)을 명시했다 — 우회 · ID 바꾸기 없음 |
| 승인 둔갑 | 없음. 「로컬 리뷰 통과 초안」(L49)으로만 부르고, receipt · 사람 승인 주장이 없다 |
| 범위 | target_delta L14-21 = 앱(iOS 폰 · 아이패드 · DAY 기준 · 대리 수락 · 통역 board view · 푸시 앱 쪽) + D-1 + AGENTS 「앱」 문장. 코드 PR 하나 → dev · 사용자 지시 전 머지 금지(L60 · A13) |
| non_goals | D-2 · D-3 서버 전체(L39-40) · 사용자 설정(L41) · 옆 세션(L42) · D-1 밖 backend · SPEC-002 API(L43) · 상담사 호출 · 관리자 추가 · 호출자 제외 · 새 통역 키 · OQ-A1/A9/A11 · 새 문구 · 번역(L44) · 다른 탭 · Android(L45) · 배포 · DB(L46) — 브리프 §3과 일치 · acceptance와 충돌 없음 |
| 정책 3결정 | 통역 = board view · is_admin(L19 · A9) · 푸시 = 호출 대상 그대로 · 서버 몫(A10) · 대리 수락 ≠ 수신(A2 · A10) · 상담사 호출 범위 밖(L44) |
| AC 매핑 | SPEC-003 26개 → A1~A11 **누락 0**: A-1→A1 · A-2 · A-22→A2 · A-3/4/5/23→A3 · A-6/20→A4 · A-7/8/21→A5 · A-18/19→A6 · A-9~12→A7 · A-13→A8 · A-14/14b→A9 · A-15/16/16b/24→A10 · A-17→A11 |
| L3 execution | code_surface · phases · verification · rollback 비어 있지 않음(requests.md L30). 순서 근거(D-1 계약 먼저 → 골격 → 로그인 → 시술 현황 → 푸시 · 통역 더블 → 검증)도 맞음 |
| 코드 근거 | `backend/day/routers/api/auth.py` · `schemas/auth.py` · `services/auth.py` · `backend/common/config.py` · `backend/tests/day/auth/` · `scripts/test.sh` · `deploy/config/{dev,prod}.env`(`DAY_ADMIN_EMAILS=` 빈 값 선례 — env 이름 placeholder와 같은 방식) 모두 dev에 실재. `app/` 없음 = 「새로」와 맞음 |

## WARN

### W-1. 완료 조건에 Delivery 안에서 끝낼 수 없는 실물 검증이 표시 없이 들어 있다

- **자리**: `acceptance` A3(L26 「실물은 prod 배포 뒤」) · A1 · A2 · A4 · A5 · A7(L24-30 「실물(dev)」)
- **근거**: 브리프 §3 · §4 「앱 코드 완료와 통합 완료 기준을 섞지 않는다」, SPEC-003 §4 「앱 구현 완료(더블) / 통합 검증 완료(실물)」. A9 · A10은 「실물은 … 이 Delivery 의 완료 조건이 아니다」라고 적었는데, A3는 같은 성격(prod 배포는 non_goals L46)인데도 그 표시가 없다. 그리고 「실물(dev)」이 무엇을 뜻하는지 정해져 있지 않다.
  - 이미 dev에 배포된 board API에 개발 빌드로 붙는 확인이라면 머지 전에 할 수 있다(SPEC-003 「D-1 전 동작」).
  - D-1을 포함한 이 PR 코드를 dev에 올린 뒤의 확인이라면 머지가 필요하다. dev push는 곧 배포이고, 머지는 사용자 지시 전 금지다(L60).
  - `review-delivery`는 PR head에서 acceptance를 판정한다(requests.md). 그래서 위 둘이 섞이면 conformant 판정을 내릴 수 없다.
- **고칠 안**: (1) A3에 「prod 실물(데모 넘김 · prod 행 0)은 이 Delivery 완료 조건 아님 — prod 배포 뒤 통합 검증」을 붙인다. (2) acceptance 앞부분이나 review_surface에 정의 한 줄을 넣는다. 「Delivery 완료 = 더블 + 기존 dev 서버(91728737 board API)에 개발 빌드로 붙인 확인. D-1 서버 칸이 필요한 실물(A3 · A4 hospital 대상 비교 · A6 정식 빌드)은 머지 · 배포 뒤 통합 검증」. 새 정책은 아니다. SPEC-003의 더블 / 실물 구분을 request에 옮기는 것이다.

### W-2. 경로 2개가 실제와 다르다(「실제 context에서 확인한 항목만」 — requests.md L30)

- **자리**: `execution.code_surface` L72 `local.env.example` · `verification` L96 · `acceptance` A12 L35 `tests/architecture`
- **근거**: dev 91728737 실물은 `deploy/local.env.example`(루트에 없음)과 `backend/tests/architecture`(루트 `tests/` 없음)다.
- **고칠 안**: 두 경로를 `deploy/local.env.example` · `backend/tests/architecture`로 바꾼다. 같이 `uv run pytest -q backend/tests/day/auth`의 infra 테스트는 `scripts/test.sh`가 요구하는 로컬 compose(PostgreSQL · Redis)가 있어야 돈다는 점을 verification에 한 줄 적는다. 이것은 착수 조건이 아니라 실행 환경이다.

### W-3. rollback 「데모 이메일 env를 비우면 기존 동작」은 환경 격리를 깨는 방향(fail-open)인데 안전한 롤백처럼 적혔다 (코디 지시 검수 포인트)

- **자리**: `execution.rollback` L106
- **근거**: SPEC-001 §3 「낱말」에 따르면 `DAY_DEMO_LOGIN_EMAILS`가 비면 기능이 꺼진다. 그러면 알려진 데모(심사) 계정이 **prod 일반 인증 경로**로 들어간다. prod KOS sign-in이 일어나고, prod 스키마의 병원 연결로 후보가 정해진다.
  - prod가 KOS 데모 연결을 뺄지는 아직 미결이다(mobile-deployment M-18 · 옆 PR #920이 `is_demo`를 지움).
  - 데모 병원이 prod에 연결돼 있으면 심사관이 **prod 서버 · prod DB**로 로그인한다. 이것은 사용자 결정 「심사관은 운영 데이터를 조작하지 않음 · 데모 → dev」에 어긋난다.
  - 연결돼 있지 않으면 `no_connected_hospital`이 뜬다.
  - 어느 쪽이든 「기존 로그인 동작으로 돌아감」은 기능상 맞지만 **환경 격리를 지키는 롤백은 아니다.**
- 같은 SPEC에 fail-closed 길이 이미 있다. `DAY_DEMO_API_BASE`가 비었거나 정규화에 실패하면 넘김이 꺼지고, 데모 계정 로그인은 `environment_unavailable`(503)이 된다(SPEC-001 「데모 연결 대상」 줄 · 매트릭스). 이메일 목록은 그대로 둔 채 dev 넘김만 막으면 심사관이 prod로 새지 않는다.
- **고칠 안**: rollback을 둘로 나눈다. ① 코드 revert — 정식 앱은 「환경 칸 필수」라 칸이 사라지면 로그인 실패(fail-closed)다. 웹 · `client=web`은 원래대로다. ② 데모 넘김을 멈출 때는 **`DAY_DEMO_LOGIN_EMAILS`는 두고 `DAY_DEMO_API_BASE`를 비워** 데모 계정을 503으로 막는다. 「이메일 목록 비우기」는 데모 계정을 prod 인증으로 보내므로 롤백 수단에서 빼거나, 「심사 중 금지 · prod 데모 연결 없음을 확인한 경우만」 조건을 붙인다. 새 정책이 아니라 SPEC-001에 이미 있는 동작을 고르는 것이다.

## 참고(판정 밖)

- 코디 `start-delivery --plan` 결과(코디 메시지): `execution_state=ready` · `spec_baseline_state=pending` · `missing_target_specs=[DAY-SPEC-003, DAY-SPEC-001]` · `next_action=review-delivery-plan/human_gate`. 규칙(delivery-workflow L29 · L54)과 일치한다. SPEC-001도 main에서는 draft라 missing으로 잡혔고, 이것도 pending의 근거로 맞다.
- A8 · verification L97 「시뮬레이터 화면 검수 — 사용자 · 리뷰어」: reviewer 워커는 시뮬레이터 조작이 금지된 경우가 있으니, 실행 주체를 「사용자(또는 앱 워커 스크린샷)」로 적어 두면 판정이 쉬워진다.
- 옆 세션 PR #920과의 SPEC-001 머지 순서(review_surface L53)는 SPEC PR 단계 몫 — 이 request는 올바르게 노출만 했다.

## 남은 것

- 사용자 응답 대기 정책은 없다(통역 · 푸시 대상 확정됨). 열린 것은 SPEC 보류대로 둔다 — OQ-A1 · A9 · A11 · 문구 OQ.
- 서버 D-2 · D-3은 미구현 · 담당 미배정이다. Apple · 서명 · TestFlight · APNs/Soniox 키 · 서버 env는 사용자 몫이다(착수 조건 아님 · 실물 조건).
- GitHub Issue는 아직 없다. 순서: 코디 `--plan` → L3 사람 승인 → `--apply`. SPEC PR 머지 뒤 version 2로 baseline ready에 재결속한다.
