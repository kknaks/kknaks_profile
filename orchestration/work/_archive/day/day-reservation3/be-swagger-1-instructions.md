# [backend] ext 스웨거 보강 — 예약 요청 상태값 · 전이 · 오류 코드 · 흐름 (be-swagger-1)

너는 day `backend` 워커다. 맥락이 없으면 먼저 읽어라: 브리프 `day-reservation3-be-brief.md`(규칙 · 완료 보고 §9 그대로) · 코드 레포 `AGENTS.md`.

워크트리 그대로: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation3` (미커밋 변경 위에 이어서 · 커밋 · push 금지).

## 왜

링키 개발자가 「상태값 분류가 어떻게 되어 있나」를 물었다. 지금 `/api/ext/docs` 에는 enum **이름만** 있고 뜻 · 전이 · 오류 코드가 없다. 링키 · 차티 · 다음 외부 페이지 개발자가 **스웨거만 보고** 붙을 수 있게 한다(사용자 11-27 「이거 스웨거에 적어 주고」).

## 근거(이 밖의 내용을 지어 넣지 않는다)

- SPEC-008 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation3-spec/products/day/20-spec/spec-008-reservation-request.md`
- 단, SPEC 과 **코드가 다르면 코드가 맞다**(e2e 뒤 바뀐 것: 생성에 W18 없음 · 판정 = 이름(대소문자 · 띄어쓰기 무시) + 식별값(생년월일 · 연락처 · SNS · 이메일) 하나 이상 정확히 같음 · 국적은 둘 다 있을 때만 비교 · 식별값 하나 이상 필수 · 이미 취소된 예약에 cancel = 202 + 취소됨). 다른 곳은 리포트에 표로.
- 코드: `day/schemas/ext_reservation_request.py` · `day/routers/api/ext_reservation_requests.py` · `day/services/reservation_request_ext*.py` · `day/policies/reservation_request.py` · `day/routers/api/ext.py`(공통 오류)

## 할 것 (스웨거 = 코드의 description · 스키마 · responses)

1. **enum 값마다 뜻** — `status` · `closedReason` · `kind` · 댓글 `type` · `state` · `action` · `author.side` · `ExtRequestWithdrawn.status`. Field description 에 「값 = 뜻 · 언제 붙나」 표(마크다운)로. (예: `folded` = 병원이 KOS 등록 실패로 접음 · `expired` 는 코드가 실제로 붙이는 조건 그대로)
2. **상태 전이 · 할 수 있는 행동** — 스레드 상태 × (E2 change · E2 cancel · E3 withdraw · E6 comment) → 202/200/201 또는 409(+ `error.code`). 쓰기 확인 대기 중(`pending_version_id`) 409 도. 확정 뒤 새 버전이 오면 다시 `requested` 등. **코드에서 실제 분기를 읽어** 만든다. 앱 `description`(ext 앱 머리) 또는 E2 · E3 설명에 표로.
3. **오류 코드** — 경로마다 나올 수 있는 `error.code` 와 HTTP 코드 · 뜻을 각 경로 `responses` description 에(공통 401 `ext_unauthorized` · 429 `too_many_requests` · 400 `invalid_request` · 503 등 + 이번 409 `request_finished` 등 전부). 코드에서 `_failure` · 도메인 예외 → ext 매핑을 **전부 grep** 해서 센다(목록 밖을 놓치지 말 것).
4. **흐름 설명** — 앱 description 에 짧게: 초진 · 재진 판정(위 규칙 · 2명 이상 = 병원이 「고객 확인 필요」 댓글 → `customerId` 넣은 새 버전) · 병원 처리 알기(E4 `updated_since` 폴링 → E5 `reservation_applied` 댓글 · `customerId` · `reservationId`) · 변경 요청(`change_request` · `proposals` · `waiting` → 새 버전이면 `superseded`) · 버전 번호는 서버가 매김 · 생성 전 change = `new` 기록 · `Idempotency-Key` · 키는 병원당 하나 + 선택 `X-Day-Client`.
5. **문서 낡은 곳** — `docs/development/deployment.md` 「외부 연동 API 전환」: `partner` = `linky` · `charty` 설명이 이번 변경(병원당 키 하나 · `partner` 제거)과 다르다 → 코드 기준으로 고친다(Key Vault 비밀 이름 · env 이름은 그대로).

## 하지 말 것

- 동작 · 응답 모양 · 오류 코드 값 바꾸지 않는다(설명만). 바꿔야 맞는 곳을 찾으면 고치지 말고 리포트에.
- 값 · 키 · 비밀 출력 금지.

## 검증

- `scripts/test.sh` 관련 시험(`tests/day/test_ext_contract.py` · `tests/architecture/test_api_contracts.py` · 예약 요청 시험) 통과 · `scripts/check.sh --pure` 통과.
- 로컬 스택(11140)은 코디가 띄운 것 — 건드리지 말고, 스웨거 JSON 은 `create_ext_app().openapi()` 로 뽑아 확인. 뽑은 JSON 은 커밋하지 않는다.

## 리포트 `be-swagger-1-report.md` (이 폴더)

① 고친 파일:줄 ② 상태 × 행동 표(최종본 그대로) ③ 오류 코드 표(경로 · HTTP · code · 뜻) ④ SPEC 과 코드가 다른 곳 ⑤ 검증 수치.

완료 보고는 브리프 §9 두 명령 그대로 · subject `backend 완료: ext 스웨거 보강`.
