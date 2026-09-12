# [backend] WP-007 — THE CONNECT(TDL) 회의실 예약 연동: 회의 생성 시 예약 · 사내 참석자=회사 계정 · 사외 참석자=외부인 등록

너는 **sc-ax `backend` 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = 83e3d69, PR #5 브랜치에 이어 쌓음). `backend/` · `Makefile` · `docker-compose.yml`. `frontend/` 읽기만. 커밋 금지.

## 0. 사용자 결정 (2026-09-11)
- **회의실 예약을 데모 범위 안으로** 연다(SPEC §2.2 예외 해제 — planner 가 문서 정렬). 흐름: **서버가 env 의 계정으로 THE CONNECT 에 로그인해 예약**한다.
- 참석자 매핑: **사내 사람 → 회사 계정(the Connect 구성원)으로 던지고, 사외 참석자 → 외부인 등록**.
- 장소에서 「회의실 선택 안 함」이면 호출하지 않는다(이미 FE 기본값).

## 1. 먼저 조사 (읽기 전용, 리포트 §1 에 사실로)
- **참고 코드(정본)**: `/Users/kknaks/git/harness_works/mediness-app/back/app/clients/the_connect.py`(httpx 포팅, 458줄 — 로그인 쿠키·`rooms`·`plan`·`availability`·`list_reservations`·`members`·`create`·`update`·`cancel` · `build_create_reservation_body`(company_id·booker_email·participants 이메일 콤마·notify) · `RoomUnavailableError`·`ReservationPreempted`) · 그 settings(`tdl_base_url`·`tdl_company_id`·`tdl_email`·`tdl_password`·`tdl_notify`·`tdl_http_timeout_seconds` — 파일 위치는 grep) · 계약 `/Users/kknaks/git/harness_works/mediness-mediness/products/mediness/20-spec/spec-151-ax-assistant-reservation.md`(§7.2 gateway). 읽기만 — 그 리포는 건드리지 않는다.
- **외부인 등록**이 the Connect API 에 어떤 형태인지(외부 참석자 등록 엔드포인트·`participants` 에 이메일 아닌 값·`attendees` 표시 문자열 등) — 참고 코드·kernel 힌트·실제 API(로그인 뒤 조회만)로 확인해 **사실**을 적어라. 없으면 「attendees 표시 문자열에 이름 나열」 폴백.
- 사내 참석자 → the Connect 계정 매핑: `members()` 목록과 우리 조직 카탈로그(이메일·이름)를 어떻게 잇는지(이메일 일치 우선, 없으면 이름).

## 2. 계약 (코디 확정)
- **env**: `~/.config/theconnect/env`(코디가 만들어 둠 — `TDL_EMAIL`·`TDL_PASSWORD`. 값 인용·로그 금지). `TDL_BASE_URL`·`TDL_COMPANY_ID`·`TDL_NOTIFY` 는 참고 코드 기본값을 settings 기본으로 두고 env 로 덮어쓰기. Makefile 은 Soniox 와 같은 결(`THECONNECT_ENV_FILE ?= $(HOME)/.config/theconnect/env` 를 api·local-stack 에 source).
- **회의실 목록**: `GET /api/meetings/rooms` → the Connect `rooms()`(캐시 5분) — 정적 목록을 실제 목록으로 교체. FE 는 다음 라운드에 붙인다.
- **예약 시점**: `POST /api/meetings`(예약)에서 `room_id`(새 필드, null 이면 호출 없음)가 오면 회의 생성 트랜잭션 **밖**에서 the Connect `create` → 성공 시 `meetings.room_reservation`(external_id·room name·status booked) 저장, 회의 `location` = 회의실 이름. **실패(RoomUnavailable·인증·네트워크)** → 회의는 만들되 `location` 비우고 응답에 `room_reservation: {status:"failed", reason}` — 화면이 안내. 회의 정보 편집(일시·장소 변경)·삭제(취소)·회의 취소 시 `update`/`cancel` 동기화(실패해도 회의 동작은 그대로, 상태만 남김).
- **참석자 → payload**: 사내 참석자(attendee_ids)는 회사 계정 이메일로 `participants`; 사외(external_attendees 이름)는 §1 에서 확인한 외부인 등록 방식으로; booker = env 계정, `attendees` 표시 이름 = 만든 사람 이름.
- 바로 시작(quick-start)은 호출 없음.
- 응답 노출: external_id·계정 정보 응답 금지(상태·회의실 이름·사유만).

## 3. 검증
```
cd backend && uv run pytest -q <네 테스트> tests/contract/test_meeting_core.py tests/architecture -m 'not integration'. the Connect 는 대역(FakeGateway)으로 — 실제 호출은 §1 조사(조회만)와 코디 실물 1회. 검증 1회
```
테스트: room_id 없으면 호출 0 · 성공 시 저장·location · 실패 시 회의 생성되고 failed 사유 · 사내/사외 참석자 payload 분기 · 수정/취소 동기화 · 계정값 로그 미노출.

## 4. 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: WP-007 THE CONNECT 예약" \
  --body "조사 사실(외부인 등록 방식·계정 매핑) / 변경 파일 / 계약 / 검증 수치 / FE 인계(rooms·room_id·room_reservation) / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — WP-007. 상세는 인박스." --enter
```
