# be-swagger-1 결과 보고 — ext 스웨거 보강(예약 요청 상태값 · 상태 × 행동 · 오류 코드 · 흐름 · deployment.md)

## 상태: done (설명만 · 동작 · 응답 모양 · 오류 코드 값 안 바꿈 · 커밋 없음 · 로컬 스택 안 건드림)

확인 = `create_ext_app().openapi()`(뽑은 JSON 은 파일로 안 남김).

## ① 고친 파일:줄

| 파일:줄 | 무엇 |
|---|---|
| `backend/day/routers/api/ext_reservation_request_docs.py`(새 · 257줄) | `:18` `FLOW`(앱 머리 흐름 1~7 · 스레드 상태) · `:67` `STATE_TABLE`(상태 × 행동) · `:109` `NOTES`(customer_changed · 검사 순서 · 동기화 때 자동 처리) · `:120` `DESCRIPTION` · `:122-154` E1 ~ E8 경로 설명 · `:158` `COMMON`(공통 401 · 429 · 400 · 503 · 500) · `:202` `responses()`(HTTP 코드마다 `error.code` 표 · 모양 `ExtErrorResponse` · 그 경로에 없는 앱 공통 코드 = 「이 경로에서는 나오지 않음」) · `:218-257` 경로별 오류 표 |
| `backend/day/routers/api/ext_reservation_requests.py:3` · `:27-33` · `:46-168` | 문서 모듈 가리킴 · `Idempotency-Key` 설명(처음 버전 · 댓글을 돌려줌 · `idempotency_conflict`) · E1 ~ E8 `summary` · `description` · `responses` · `updated_since` 설명(오프셋 없으면 KST) |
| `backend/day/routers/api/ext.py:29` · `:253` | 앱 `description` 끝에 `ext_reservation_request_docs.DESCRIPTION` 붙임(기존 글 그대로 · 665줄) |
| `backend/day/schemas/ext_reservation_request.py:27-131` | `_values()` 표 만들기 + `STATUS_DOC` · `CLOSED_REASON_DOC` · `KIND_DOC` · `COMMENT_TYPE_DOC` · `STATE_DOC` · `ACTION_DOC` · `SIDE_DOC` · `ACCEPTED_STATUS_DOC` |
| 같은 파일 `:211` · `:217` | E2 본문 `kind` `change` · `cancel` 설명 |
| 같은 파일 `:237-260` · `:275-318` | `ExtRequestAccepted.kind/status` · `ExtRequestWithdrawn.status` · `ExtRequestSummary.status/customerId/reservationId` · `ExtRequestVersionView.version/kind/client` · `ExtRequestAuthor.side/name` · `ExtRequestCommentView.type/body/versionNumber/proposals/state/action/appliedAt` · `ExtRequestDetail` 칸 전부 |
| `docs/development/deployment.md:180-185` · `:196-197` | 「외부 연동 API 전환」 — `partner` = `linky` · `charty` 줄 지움 → 병원당 원소 하나 · 같은 `hospital_id` 둘 · 예전 `partner` 칸 = 503 `ext_unavailable` · `X-Day-Client` · 병원 단위 분당 60 · 예약 요청 스레드는 DAY 에만 저장(Key Vault 비밀 이름 · env 이름 그대로) |

## ② 상태 × 행동 표(스웨거 앱 머리 최종본 그대로)

| 지금 스레드 | E2 `change` | E2 `cancel` | E3 철회 | E6 댓글 |
|---|---|---|---|---|
| 요청됨 · 확정 — **예약 있음**(확인 대기 포함) | 202 `kind=change` · `requested` | 202 `kind=cancel` · `requested`(병원이 [예약 취소]) | 409 `request_already_applied` | 201 |
| 요청됨 — 예약 없음 · 만든 예약 없음 | 202 `kind=new` · `requested` | 409 `request_not_applied`(철회 E3 을 쓰라) | 200 `closed`(`withdrawn`) | 201 |
| 요청됨 · 확정 — 만든 예약이 그 뒤 취소됨 | 202 `kind=new` · `requested` | 202 `kind=cancel` · **`canceled`**(+ `reservation_applied` `cancel` · 글쓴이 이름 없음) | 200 `closed`(`withdrawn`) | 201 |
| 취소됨 | 202 `kind=new` · `requested`(다시 열림) | 409 `request_finished`(만든 예약 있었음) · `request_not_applied`(없었음) | 200 `closed`(`withdrawn`) | 409 `request_closed` |
| 닫힘 | 202 `kind=new` · `requested`(다시 열림) | 409 `request_finished`(만든 예약 있었음) · `request_not_applied`(없었음) | 200 `closed`(그대로 · `closedReason` 안 바뀜) | 409 `request_closed` |

- 예약 있음 스레드에 **다른 고객**으로 `change` = 400 `customer_changed` — 새 요청(E1)으로. 예약이 없으면 막지 않음.
- `change` 본문 검사(400 · 404 `customer_not_found`)는 위 판정보다 먼저 · 없는 스레드는 늘 404 `request_not_found`(본문 검사보다 먼저).
- 병원 동기화 때마다: 요청됨 ∧ 예약 없음 ∧ 확인 대기 아님 ∧ 마지막 버전 `start` 지남 → `closed`(`expired`) · 마지막 버전 `cancel` 인데 예약이 이미 없음 → `canceled`(+ `reservation_applied` `cancel`).
- 근거 분기: `policies/reservation_request.py` `booked` · `recorded_kind` · `withdraw_outcome` · `customer_changed` · `expires` · `cancel_done` · `services/reservation_request_ext.py` `add_version` · `withdraw` · `comment` · `services/reservation_request_settle.py` `_settle_one` · `_expire` · `services/reservation_request_actions.py` `dismiss_failure`(`folded`).

## ③ 오류 코드 표(경로 · HTTP · code · 뜻)

공통(E1 ~ E8 모두 · `routers/api/ext.py` `partner` · `_middleware` · `_validate` · `grants` · `rate_limit` — 검사 순서 401 → 429 → 400):

| HTTP | code | 뜻 |
|---|---|---|
| 400 | `invalid_request` | 입력 형식 · 필수 · 길이 · 모르는 키 · 경로 UUID · `X-Day-Client` 형식 |
| 401 | `ext_unauthorized` | 키 없음 · 틀림 · 키 병원이 쓰이지 않음 |
| 405 | `http_error` | 그 경로에 없는 메서드 |
| 429 | `too_many_requests` | 병원 분당 60 · 같은 IP 인증 안 된 실패 분당 10 |
| 500 | `internal_error` | 처리 중 오류 |
| 503 | `ext_unavailable` | 연동 설정 오류(병원당 키 둘 등) · Redis(호출 제한) 확인 불가 |

경로별(`services/reservation_request_ext.py` · `_ext_reads.py` 의 `_error` · `_invalid` · `_not_found` · `_conflict` 전부 grep — 이 밖의 raise 없음 · `threads` · `lock_hospital` 은 오류 안 냄):

| 경로 | HTTP | code | 뜻 |
|---|---|---|---|
| E1 · E2 `change` | 400 | `invalid_request` | `groupId` · `funnelId` 목록 밖 · `doctorStaffId`(원장 직무) · `counselorStaffId` 목록 밖 · 식별값 하나도 없음 |
| E1 · E2 `change` | 400 | `request_past_start` | 지난 시각 |
| E1 · E2 `change` | 400 | `memo_too_long` | 합친 메모 1000자 넘음 |
| E1 · E2 `change` | 404 | `customer_not_found` | `customerId` 가 그 병원 고객 아님 |
| E1 · E2 · E6 | 409 | `idempotency_conflict` | 같은 키 · 다른 본문 |
| E2 | 400 | `customer_changed` | 예약 있음 스레드에 다른 고객 `change` |
| E2 · E3 · E5 · E6 | 404 | `request_not_found` | 그 병원에 없는 `requestId` |
| E2 | 409 | `request_not_applied` | 만든 예약 없는 스레드에 `cancel` |
| E2 | 409 | `request_finished` | 취소됨 · 닫힘 스레드에 `cancel`(만든 예약 있었음) |
| E3 | 409 | `request_already_applied` | 예약 있음 · 확인 대기 |
| E4 | 400 | `invalid_request` | `cursor` · `updated_since` 형식 |
| E6 | 400 | `invalid_request` | `type` ≠ `message` · 빈 `body` |
| E6 | 409 | `request_closed` | 취소됨 · 닫힘 |
| E7 · E8 | — | 공통만 | |

앱 공통 `responses` 에 있는 404 · 409 · 502 등은 그 경로에서 안 나오면 「이 경로에서는 나오지 않음」으로 적음(앱 공통 모양 = `ExtErrorResponse` 유지). 502 는 E1 ~ E8 어디서도 안 나옴.

## ④ SPEC 과 코드가 다른 곳(코드 기준으로 적음)

| 곳 | SPEC-008 | 코드(스웨거에 적은 것) |
|---|---|---|
| 예약 없음 ∧ `visit_id` 있음 ∧ 요청됨 · 확정에 `cancel`(§3 상태표 · 케이스 매트릭스 · Rule 3) | 409 `request_finished` | **202 · `canceled`** + `reservation_applied` `cancel`(누른 직원 없음) — e2e 1 ④ 고침 · 취소됨 · 닫힘은 409 그대로 |
| E2 응답 `status`(E2 행) | 늘 `"requested"` | 위 경우 `"canceled"` |
| 판정 Rule 1 · 시안/기획안과 다른 곳 표 | 이름 + 생년월일 | 이름(대소문자 · 띄어쓰기 무시) + 식별값(생년월일 · 연락처 · SNS · 이메일) 하나 이상 같음 · 국적은 둘 다 있을 때만 |
| 요청 본문 `customer.birthDate` | 필수 ✓ | 선택 — phone · sns · email · birthDate 중 하나 이상 필수 |
| [예약 생성] KOS 쓰기 표 · W18 | W3 → (상담사) W18 | W3 `reserve` 에 `counselor` 를 바로 실음 · W18 없음(W18 은 [예약 수정]에서 바뀌거나 지울 때만 · 지우기 = `counselor: {}`) |
| 초진 W1 본문 | 이메일 없음(W2 만 `email`) | W1 에도 `email`(KOS 가 이름 + 이메일로 찾음 · be-probe-2) |
| 자동 처리(Rule 5) | `expired` 만 | 동기화 때 마지막 버전 `cancel` ∧ 예약 없음 → `canceled` 도(검수 W11) |
| E2 다른 고객 `change` | (OQ-Q15) | 400 `customer_changed` |

**코드를 고쳐야 맞을 수 있는 곳(안 고침 · 스웨거엔 지금 동작 그대로 적음)**:
- E1 · E2 `Idempotency-Key` 재시도(`reservation_request_ext.py` `_replay`) 응답 `status` 가 **늘 `"requested"`** — 처음 응답이 `canceled` 였던 E2 `cancel` 재시도는 `requested` 로 온다(SPEC 「처음 응답 그대로」와 다름). E2 설명에 「`status` 는 `requested` 로 온다 · 지금 상태는 E5」로 적어 둠. 고치려면 재생 때 처음 상태를 저장하거나 지금 스레드 상태를 돌려주면 된다 — 결정 필요.

## ⑤ 검증

- `scripts/check.sh --pure` = **통과**(ruff · format · mypy · taut audit/check · frontend · 시험 2420 passed · 877 deselected · `.local/checks/20261127-102707-91759`). 첫 두 번은 다른 워커가 고치던 `backend/day/menu.py:5` E501 로 멈췄다(내 파일 아님 · 안 건드림 · 그 뒤 고쳐져 통과).
- `scripts/test.sh` 관련 시험(`test_ext_contract` · `architecture/test_api_contracts` · `test_ext_reads` · 예약 요청 rules · flow · actions_flow · writes_plan) = **262 passed**.
- `create_ext_app().openapi()` 확인: E1 ~ E8 `summary` 붙음 · E2 응답 키 = 202 · 400 · 401 · 404 · 405 · 409 · 429 · 500 · 502 · 503(422 는 `/openapi.json` 에서 빠짐) · 409 표 3줄 · 모양 `$ref ExtErrorResponse` · `closedReason` 값 표 · 앱 머리 상태 × 행동 표 렌더 확인.
