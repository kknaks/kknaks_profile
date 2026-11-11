# fix — 작업 계획(WP) · 구현 워커 브리프의 바탕

> 2026-11-11 · planner · **4판 갱신(같은 날)**: 피드백 8 · 9 · 10 → WP-BE-3 · WP-APP-3 추가 · 코드 브랜치 `kknaksss/fix-app-re1` · 스펙 브랜치 `kknaksss/fix-app-re1-spec`. 기존 WP 4개는 **끝남**(구현 · 리뷰) — 내용은 고치지 않음.
> 스펙 = mediness `fix-spec` 워크트리 미커밋(1 · 2 · 3판) `products/day/20-spec/spec-003 · 004 · 005 · 000` · `40-architecture/deployment.md`.
> 이 계획은 **스펙을 다시 정하지 않는다** — 모든 동작 · 글자 · 값은 아래가 가리키는 스펙 절이 정본이다. 스펙과 이 계획이 다르면 스펙이 맞다(그리고 planner 에게 알린다).
> Delivery Issue 등록 · GitHub 쓰기 없음(2차 Delivery 마감과 함께 사용자와 따로). 새 `30-work/work-*.md` 없음.
> 코드 워크트리 `CENTURION_DAY/fix`(`kknaksss/fix`) — `AGENTS.md` 계층 · 테스트 규칙을 따른다. 값(키 · Vault 이름 · IP · Team ID)은 브리프 · 리포트 · 로그에 쓰지 않는다.

## 1. WP 나눔

코드 워커 둘(`backend` · `mobile`)이 **같은 워크트리에서 동시에** 돈다 → 경로로 나눈다. `backend` = `backend/` · `scripts/` · `deploy/` · 루트 `pyproject.toml` · `uv.lock` · `docs/development/`. `mobile` = `app/` 만. 두 워커가 같은 파일을 만지는 일은 없다.

| WP | 워커 | 무엇 | 왜 이렇게 나눔 |
|---|---|---|---|
| **WP-BE-1** ✅ 끝남 · 채팅 · 알림 서버 | backend | 그룹 이름 API #22 · 알림 설정 `chat` 종류 · 채팅 푸시 받는 사람 | 앱 WP-APP-2 가 기다리는 서버 계약만 모음 — 작고 먼저 끝나야 함 |
| **WP-BE-2** ✅ 끝남 · 통역 서버 | backend | WS 라우트 · 중계 서비스 · 사전 시드 · 상한 · 설정 · 선택 비밀 · 의존성 · 실물 스크립트 | 앱 변경 없음 · 크기가 큼 · 의존성(`uv.lock`)을 바꿈 → BE-1 과 섞으면 리뷰 · 되돌리기가 어려움 |
| **WP-APP-1** ✅ 끝남 · 시술현황 카드 + 앱 후속 2 | mobile | 모두 완료 상태 · 목록 [귀가 대기] · 확인 필요 표시 · `version >=` · `calls[].canRecall` | 서버 변경 없음(서버 값 소비만) — 바로 시작 가능 |
| **WP-APP-2** ✅ 끝남 · 채팅 · 설정 | mobile | 채팅 403 안내 · 그룹 이름 바꾸기 · 「채팅」 스위치 · 앱 안 배너 | BE-1 계약을 소비 — 가짜 서버로 먼저 짓고 BE-1 뒤 로컬로 확인 |

| **WP-BE-3** 읽음 표시 서버(4판) | backend | `Room.members[]` 에 `lastReadSeq` · `fromSeq` · 새 이벤트 `chat_member_read` | 작음 · 앱 APP-3 의 10번이 기다림 — §3 계약 표로 앱이 동시에 짓는다 |
| **WP-BE-4** 파일 저장소(7판 · 관리 ID · 9판 정정 3 — 환경 = 컨테이너) | backend | 연결 문자열 → VM 관리 ID · 환경 = 컨테이너(`DAY_BLOB_CONTAINER` — dev `dev` · prod `prod`) · 키 `chat/{병원 id}/…` 그대로(환경 접두 없음) · 접근 실패 = 503 `photo_disabled` · 설정 · 배포 계약 | 저장소가 준비됐으나(인프라) 지금 코드로는 붙지 못함 — 이번 작업에 같이(사용자) · **앱 변경 없음** |
| **WP-APP-3** 채팅 화면(4판) | mobile | 길게 누르기 자리(8) · 폰 대화 화면 하단 4메뉴 숨김(9) · 말풍선 읽음 숫자(10) | 셋 다 대화 화면 · 셸 파일에 모임 → 한 WP |

한 워커가 WP 둘을 갖는다 → **워커 안에서는 차례로**(BE-1 → BE-2 · APP-1 → APP-2). 워커끼리는 동시에.

---

## 2. WP 별

### WP-BE-1 채팅 · 알림 서버 — ✅ 끝남

**근거 스펙**: SPEC-004 §3 API #22 · 규칙 「그룹 이름 바꾸기」 · 「알림 끄기」 · 실시간 `chat_room` · 「채팅 푸시」 받는 사람 · 본문 제목 / SPEC-005 §3 「받는 종류」 · 「`chat` 종류의 효과」 · 모델 대조 / SPEC-000 07 `notification_setting` · `chat_room.title`.
**수용 항목**: SPEC-004 C-A14(서버) · C-A20(서버 갈래) · C-A21(서버 — 푸시 0) · SPEC-005 N-A5 · N-A13(서버).

**고칠 파일**(grep 으로 센 것 — `MAX_TITLE` · `create_group` · `room_name(` · `chat_room` 이벤트 · `_receivable` · `settings_of` · `put_setting` · `NotificationSetting` · `is_muted`):

| 파일 | 무엇 |
|---|---|
| `backend/day/routers/api/chat.py` | `PUT /api/chat/rooms/{room_id}/title` 라우트(기존 `mute` 라우트 모양) |
| `backend/day/schemas/chat.py` | `TitleRequest {title: str \| None}`(`GroupRequest.title` 과 같은 칸 규칙 · 모르는 칸 거절은 `_Req` 그대로) |
| `backend/day/services/chat.py` | `rename(…)` — 그룹만(1:1 = `chat_group_only` · `detail` 은 내부 문장) · `_room_for` 범위 · 방 행 잠금 · `strip` · `MAX_TITLE` 40 재사용(넘으면 기존 `chat_invalid` → 400 `invalid_request` `field=title`) · 같은 값 = 200 이벤트 없음 · 시스템 줄 · `last_message_at` · `seq` 안 건드림 · 커밋 뒤 `_room_events(session, room, <지금 멤버 계정 전부>)` |
| `backend/day/services/chat_push.py` | `deliveries` 받는 사람(`:93` 조건)에서 `notification_setting(kind='chat', is_enabled=false, deleted_at null)` 계정 빼기 · 제목은 지금처럼 발송 때 다시 읽은 `room.title`(스펙 W10 문장과 같음 — 바꿀 것 없음) |
| `backend/day/services/notifications.py` | `_receivable` — 원장 목록이면 `doctor_call` · 채팅 활성 직원(`services/chat.py:114-146` 판정과 같게 — 함수 재사용 · 복사 금지)이면 `chat` · 차례 `doctor_call` → `chat` · `put_setting` 은 그대로 동작(받는 종류 검사) |
| `backend/day/queries/chat.py` | 원칙상 변경 없음 — 「활성 직원」 판정이 여기 있으면 재사용만 |

**확인만(바꾸지 않음)**: `backend/day/models/misc.py`(`NotificationSetting.kind` 는 `String` — migration 없음) · `backend/day/services/chat_events.py`(새 이벤트 없음 · `chat_room` 재사용) · `backend/day/routers/api/notifications.py`(경로 · 모양 그대로) · `backend/day/errors.py`(새 코드 없음).

**새로 만들 파일**: 없음.

**하지 말 것**: migration · 새 이벤트 종류 · 그룹 이름 바꿈 시스템 줄(SPEC-004 OQ-C14) · `notification` 행에 채팅 쓰기 · 알림 목록에 채팅 넣기 · 방별 `is_muted` 를 전체 스위치로 바꾸기.

**시험**(자기 것만 · `uv run pytest -q -m "not infra"` 로 고치는 중 · 끝에 `scripts/test.sh -q` · `uv run ruff check backend`):
- `backend/tests/day/chat/test_chat_api.py` — #22: 그룹 성공 · 공백 · null · 41자 400 `field=title` · 같은 값 200 이벤트 0 · 1:1 400 `chat_group_only` · 나간 사람 · 다른 병원 404 · 비활성 403 · 시스템 줄 0 · `last_message_at` 그대로
- `backend/tests/day/chat/test_chat_stream.py` — 이름 바꿈 뒤 지금 멤버 전부(바꾼 사람 다른 연결 포함)에게 `chat_room` · 나간 멤버 · 다른 병원 연결엔 없음
- `backend/tests/day/chat/test_chat_concurrency.py` — 동시 두 바꾸기 = 직렬 · 나중 것 남음(infra)
- `backend/tests/day/chat/test_devices_push.py` — `chat` 끈 계정 = 받는 사람에서 빠짐 · 방 `is_muted` 와 OR · 저장 없음 = 받음 · 이름 바꾼 뒤 푸시 제목 = 새 이름
- `backend/tests/day/notifications/test_notifications_api.py` · `test_notification_units.py` — 받는 종류(원장 = 둘 · 일반 활성 직원 = `chat` · 시스템 계정 · 비활성 = 빈 목록) · 차례 · `PUT chat` · 받지 않는 종류 400

**실물 몫**: 워커 = 로컬 day-local 로 API · SSE 확인 / 코디 = dev 배포 뒤 로그 · `push_log` / 사용자 = 실기기(§7).

### WP-BE-2 통역 서버 — ✅ 끝남

**근거 스펙**: SPEC-003 §3 「통역 — 앱 · 서버 계약」 전체(연결 · 인증 / 프레임 / 오류 / 서버 동작(정리 · 연결 시간 상한 포함) / 동시 세션 상한 / 사전 / 설정 · 배포 / 원천과 다른 곳) · U-15 · OQ-A39 ~ A46 · I-1 ~ I-5 / deployment.md env 표 `DAY_SONIOX_API_KEY` · `DAY_INTERPRET_MAX_SESSIONS` · 미결 2줄.
**수용 항목**: SPEC-003 A-14 · A-14b · **A-44**(서버 단위 — 자리 반납 갈래 포함) · **A-45**(실제 Soniox — 구현 워커) · A-47(구현 워커 · 로컬 키 비움 · `error.code`) · A-46 은 사용자(§7).

**고칠 파일**(grep — `api_routers` · lifespan · `day_apns_*` · `OPTIONAL_SECRETS` · `DAY_APNS_*` 를 쓰는 곳 전부):

| 파일 | 무엇 |
|---|---|
| `backend/day/public.py` | `api_routers()` 에 통역 라우터 · 사전 적재 함수 하나 내보냄(runtime 은 `day.public` 만 import) |
| `backend/runtime/main.py` | `lifespan` 에서 `day.public` 의 사전 적재 호출(깨지면 기동 실패) · 로그 `glossary seed loaded: version=…` |
| `backend/common/config.py` | `day_soniox_api_key: SecretStr = SecretStr("")` · `day_interpret_max_sessions: int = Field(default=6, ge=1, …)`(`day_apns_concurrency` 와 같은 꼴) |
| `scripts/deploy/day_vm.py` | `OPTIONAL_SECRETS` 에 `"DAY_SONIOX_API_KEY": "soniox-api-key"`(한 줄 값 · `MULTILINE_SECRETS` 아님 → `FORBIDDEN_CONFIG_KEYS` 자동 포함) |
| `deploy/config/dev.env` · `deploy/config/prod.env` | 주석에 선택 비밀 이름 `day-<env>-soniox-api-key` 추가 · 상한은 기본값이면 안 적음(바꿀 때만) — **기존 값 줄은 건드리지 않는다** |
| `deploy/compose.local.yaml` | api 환경에 `DAY_SONIOX_API_KEY: ${DAY_SONIOX_API_KEY:-}` · `DAY_INTERPRET_MAX_SESSIONS`(APNs 줄과 같은 꼴) |
| `deploy/local.env.example` | 두 이름 · 빈 값 · 설명 |
| `pyproject.toml` · `uv.lock` | `opencc-python-reimplemented` 추가 · `websockets` 를 직접 의존으로 적을지는 워커 판단(이미 잠금에 있음) |
| `backend/tests/deploy/test_day_vm.py` · `backend/tests/deploy/test_chat_env_contract.py` | 선택 비밀 · env 계약 목록에 새 이름(이 시험들이 이름 목록을 고정하고 있음) |
| `backend/tests/common/test_config.py` | 두 칸 기본값 · 범위 |
| `docs/development/deployment.md` | env 이름 · 선택 비밀 한 줄(값 없음) — 그 문서에 env 표가 있으면 |

**새로 만들 파일**:

| 새 파일(제안 — AGENTS.md 「같은 파일 이름」 · 계층 규칙) | 원천 |
|---|---|
| `backend/day/routers/api/interpret.py` | ipwa `back/app/api/interpret.py` — **인증을 다시 씀**: 헤더 Bearer 만(`day/session.py _bearer` 규칙) · `async with get_async_session()` 안 `sessions.current_session(token, "bearer")` + `require_permission(BOARD, VIEW)` · 실패 = `accept` 전 `close(1008)` · DB 세션 닫은 뒤 `accept` · 쿼리 토큰 · Origin 처리 없음 · router 에서 DB 직접 금지 |
| `backend/day/services/interpret/{__init__,session,soniox,assembler,chinese,langs}.py`(또는 `services/interpret_*.py` 로 펼침 — 워커 판단 · 이유를 리포트에) | ipwa `back/app/service/interpret/*` — **기록기(`records`) 부분 제거** · 동시 세션 자리(잡기 · 어떤 경로든 한 번만 반납 — `finally` · 취소 포함) · `session_limit` 오류 · 키 이름 · 로그 문구에 env 이름 없게(원천 `log.warning("SONIOX_API_KEY 가 비어 있다…")` 같은 문장은 DAY 이름으로) |
| `backend/day/services/glossary.py` + 값 묶음은 `backend/day/dtos/glossary.py` | ipwa `back/app/service/glossary.py` |
| `backend/day/seed/glossary.json` | ipwa `back/seed/glossary.json` **바이트 그대로**(`sha256` 을 리포트에) |
| `backend/tests/day/interpret/` 아래 시험 | ipwa `back/tests/test_interpret.py` · `test_context.py` · `test_seed.py` · `conftest.py` · `seed_tables.py` 를 DAY fixture 로 + 인증 · 상한 · 자리 반납 갈래(A-44) |
| `scripts/interpret_live_check.py` | ipwa `back/scripts/live_check.py` 의 seed · idle · zhhant 갈래만(A-45) · 키는 env 에서만 읽고 출력하지 않음 |

**하지 말 것**: 앱(`app/`) 수정 · 기록기 · `INTERPRET_RECORD_DIR` · `?token=` · Origin 허용 출처 · `GLOSSARY_CONTEXT_MAX_CHARS` env · 시드 값 수정 · 병원별 사전 · 사전 API · accept 뒤 close 1008 · 연결 중 세션 재확인(OQ-A40) · 수명 · 무활동 상한(OQ-A46 — 사용자 답 전) · `message` 에 env 이름 · 받은 값 · DB 테이블 · migration.

**시험**: `uv run pytest -q -m "not infra" backend/tests/day/interpret backend/tests/deploy backend/tests/common/test_config.py` · 인증 갈래는 DB 가 필요하면 infra 표시 · 끝에 `scripts/test.sh -q` · `uv run ruff check backend` · **`backend/tests/architecture/test_import_boundaries.py` 가 그대로 통과해야 한다**(고치지 않음). 실물 A-45 = `scripts/interpret_live_check.py` 로 dev 키(사용자가 넣은 Key Vault 값을 로컬로 가져오는 방법은 코디와 정함 — 워커가 Vault 에 직접 손대지 않음).

**실물 몫**: 워커 = A-44 · A-45 · A-47 / 코디 = dev 배포 · 로그 시드 버전 확인 / 사용자 = A-46(§7).

### WP-APP-1 시술현황 카드 + 앱 후속 2 — ✅ 끝남

**근거 스펙**: SPEC-003 개정 ⑧ · U-3(5상태 · 겹침 · 모두 완료 카드 [귀가 대기] · 확인 필요 표시 · 겹침 표 · 기준 토큰) · U-4 5번 · U-9 · U-12(`version`) · U-4 [재호출](`calls[].canRecall`) · OQ-A33 · A37 · A38 · A44.
**수용 항목**: A-9 · A-22 · A-28 · A-33 · A-37 · A-41 · A-42 · A-43.

**고칠 파일**(grep — `needsCheck` · `allDone` · `canHome` · `snap.version` · `canRecall`):

| 파일 | 무엇 |
|---|---|
| `app/lib/ui/board_screen.dart` | 카드 테두리 빨강 · 굵기 제거(`:296`) · `_box` · `_callBox` 에 확인 필요 = 바탕 `Ms.red100` + 왼쪽 띠 `Ms.red`(겹침 표 (가) — 상태 글자 색 유지 · 20분 초과는 띠만) · `_nowBox` 맨 앞에 `card.allDone` → 「시술 모두 완료」 / 「마지막 종료 HH:MM」(오른쪽 비움) · 모두 완료 카드 맨 아래 [귀가 대기] 줄(`card.canHome && me.canEditBoard` · 왼쪽 글자 없음 · `board.home(visitId, ok: OkToast.home(…))` · 잠금 키 `home:{visitId}` = 룸 상세와 같음) |
| `app/lib/ui/room_screen.dart` | `canRecallCall`(`:22-23`) → 그 호출의 `calls[].canRecall` · 「마지막 종료」 계산을 카드와 같이 쓰게 꺼냄(`:580-585` — 같은 함수 · 복사 금지) |
| `app/lib/model/board.dart` | `calls[]` 항목에 `canRecall` 읽기 · `tasks[].canRecall` 소비 제거(OQ-A33) |
| `app/lib/data/board_stream.dart` | `:213` `snap.version > current` → `>=`(같은 값 받음) · 머리 주석(`:3`) 맞춤 |
| `app/lib/ui/format.dart` | 필요하면 「마지막 종료」 계산 함수 자리 |

**하지 말 것**: 서버 판정 다시 하기(`canHome` · `needs` · `canRecall`) · 새 글자 · 새 색 토큰 · 웹 변경 · 상태값 추가.

**시험**(`app/` 에서 `fvm flutter analyze` · `fvm flutter test`): `app/test/ui/status_box_test.dart`(5상태 · 모두 완료 · 마취 겹침 = 모두 완료) · `app/test/ui/actions_test.dart`(목록 [귀가 대기] 노출 · 보기만 직무 없음 · 토스트 · 409 · 잠금 공유) · `app/test/data/board_stream_test.dart`(같은 version 받음 · 미만 버림 · `calls[].canRecall`) · `app/test/ui/app_flow_test.dart` · `app/test/ui/session_race_test.dart`(기존 기대 갱신) · `app/test/support/fixtures.dart`(`calls[].canRecall` · 모두 완료 카드) · 캡처 `test/capture/visual_capture_test.dart` 에 모두 완료 · 확인 필요 장면(눈 확인용).

**실물 몫**: 워커 = 시뮬레이터 캡처 / 코디 = 캡처 눈 확인(토큰) / 사용자 = TestFlight(§7).

### WP-APP-2 채팅 · 설정 — ✅ 끝남

**근거 스펙**: SPEC-004 U-1 「채팅 거절」 · U-7 「그룹 이름 바꾸기」 · U-8 「채팅 전체 알림 끔」 · 케이스 매트릭스 · OQ-C11 ~ C15 / SPEC-005 U-3 「채팅」 스위치 · S-5.
**수용 항목**: C-A19 · C-A20(앱) · C-A21(앱 — 배너) · N-A10 · N-A13(앱).

**고칠 파일**(grep — `_forbidden` · `isForbidden` · `BoardForbiddenBody` · `forbiddenMessage` · `connectingLine` · `그룹 이름` · `chat_room` · `notification-settings` · `banner`):

| 파일 | 무엇 |
|---|---|
| `app/lib/chat/chat_state.dart` | 403 → 채팅 메모리 비움 + 「거절」 상태(토스트 **없음** — 조작 중 403 포함) · 앞으로 올 때 · 다시 로그인 · 앱 다시 열 때만 한 번 다시 읽음 · 앱 안 배너 조건에 `chat` 설정 값(없으면 켜짐) · 이름 바꾸기 호출 |
| `app/lib/chat/chat_stream.dart` | `:99-102` 403 이면 재연결 멈춤(연결 실패 · 끊김과 구별) |
| `app/lib/chat/chat_kit.dart` | 연결 줄(`:475` 「서버에 연결 중…」)을 거절 상태에선 숨김 |
| `app/lib/chat/screens/chat_list_screen.dart` | 거절 상태면 본문 = 권한 없음 안내(아래 위젯) |
| `app/lib/ui/shell.dart` | `BoardForbiddenBody`(`:347`) 를 채팅에서도 쓰게(같은 글자 · [로그아웃] — 이름 · 위치 정리만 · 글자 그대로) |
| `app/lib/chat/screens/chat_info_screen.dart` | 「그룹 이름」 줄 편집(그룹만) · [✓] 「저장」 · [✕] 「수정 취소」(`chat_room_screen.dart:588 · 638` 의 아이콘 · 접근성 이름 재사용) · 40자 · 같은 값이면 ✓ 꺼짐 · 성공 토스트 없음 · 오류 = 기존 글자 |
| `app/lib/chat/chat_api.dart` | `PUT /api/chat/rooms/{id}/title` |
| `app/lib/chat/chat_model.dart` · `app/lib/chat/chat_copy.dart` | `Room` 갱신 · 오류 글자 고르기(새 글자 없음) |
| `app/lib/notify/notification_settings.dart` · `notification_model.dart` · `notification_api.dart` | `chat` → 「채팅」 줄 · 차례 = 서버 차례 · 값을 채팅 상태로 넘김 |
| `app/lib/notify/notification_controller.dart` · `app/lib/state/push_coordinator.dart` | 로그인 · 자동 로그인 뒤 · 앞으로 올 때 설정 다시 읽기(이미 있는 갱신 자리에 붙임) |

**하지 말 것**: 새 화면 글자(「채팅」 스위치 이름은 사용자 확정) · 방별 `muted` 값을 전체 스위치로 바꾸기 · 403 때 세션 지우기 · 시스템 줄 그리기 · 시술현황 · 통역 파일.

**시험**: `app/test/chat/chat_state_test.dart`(403 → 거절 · 토스트 0 · 재연결 0 · 앞으로 올 때 한 번 · 배너 억제 · `chat` 없으면 켜짐) · `app/test/chat/chat_contract_test.dart`(#22 요청 · 응답 · `chat_room` 반영) · `app/test/ui/chat_ui_test.dart`(안내 화면 · 이름 바꾸기 ✓ ✕) · `app/test/notify/notification_contract_test.dart` · `app/test/ui/notification_ui_test.dart`(「채팅」 줄) · `app/test/state/push_coordinator_test.dart` · `app/test/support/chat_fake.dart` · `notify_fake.dart`(가짜 서버 갱신) · 캡처 `test/capture/chat_capture_test.dart`.

**실물 몫**: 워커 = 가짜 서버 + BE-1 뒤 로컬 day-local / 사용자 = 두 기기 · TestFlight(§7).

### WP-BE-3 읽음 표시 서버 (4판)

**근거 스펙**: SPEC-004 개정 ④ · U-2 「메시지별 읽음 표시」 · §3 「응답 모양」 `Member` · 규칙 「읽음」 · 「읽음 표시 계약」 · 「실시간」 표 `chat_member_read` · 연결 직후 메우기 / SPEC-000 07 `chat_member`.
**수용 항목**: SPEC-004 C-A11(7종) · **C-A24**.

**고칠 파일**(grep — `chat_read` · `last_read_seq` · `room_views` · `.sender()` · `EVENTS` · 지금 미커밋 코드 기준):

| 파일 | 무엇 |
|---|---|
| `backend/day/queries/chat.py` | `room_views` 의 멤버 쿼리(`select(ChatMember.room_id, ChatMember.account_id)`)에 `from_seq` · `last_read_seq` 칸을 더하고 `member_list` 항목에 `lastReadSeq` · `fromSeq` — **새 쿼리 없이 칸만**(C-A24 「쿼리 수 늘지 않음」) |
| `backend/day/services/chat.py` | `read`(`:949~`) — 올리기 전 값과 비교해 **실제로 올랐을 때만** 커밋 뒤 `chat_member_read {roomId, accountId, lastReadSeq}` 를 그 방 지금 멤버 중 읽은 사람 아닌 계정에게(기존 `chat_read` 는 그대로 나에게) · 받는 멤버 목록은 기존 이벤트 받는 사람을 고르는 함수 재사용 |
| `backend/day/services/chat_events.py` | `EVENTS` 에 `chat_member_read` 추가 · 머리 주석 7종 |
| `backend/day/routers/api/chat.py` | 원칙상 변경 없음(응답 모양은 서비스 · 쿼리가 만듦) — 스트림 이벤트 거르기가 라우터에 있으면 그 목록만 |

**확인만**: `backend/day/models/misc.py`(칸 있음 · migration 없음) · `backend/tests/day/test_column_snapshot.py` · `test_constraints.py`(바뀌면 안 됨).

**하지 말 것**: migration · `Message` 에 수 싣기 · 읽음마다 `chat_room` 보내기 · 읽음 요청(#15) 규칙 바꾸기 · 푸시 · `unread` · `unreadRooms` 바꾸기 · 서버 쪽 추가 묶음(타이머).

**시험**: `backend/tests/day/chat/test_chat_api.py`(**`Room` 을 돌려주는 모든 HTTP** — 목록 #2 · 1:1 열기 #3 · 만들기 #4 · 초대 #5 · 이름 바꾸기 #22 — 응답 `members[].lastReadSeq` · `fromSeq` · 정정 2 W4) · `test_chat_stream.py`(**정정 1: 보내기는 `chat_member_read` 를 내지 않고 보낸 사람 `lastReadSeq` 는 다음 `Room.members[]` 에 그 seq 로 실림** · 오를 때만 다른 지금 멤버에게 · 같은/낮은/0 seq = 0 · 나간 멤버 · 다른 병원 연결 0 · 읽은 사람은 `chat_read` 만) · `test_chat_units.py` · `test_chat_concurrency.py`(동시 읽음 — 단조 · 같은 값 이벤트 중복 허용 · 값이 내려가지 않음) · `test_chat_queries.py`(있으면 — 쿼리 수). 명령 = 위 BE 와 같음(`uv run pytest -q -m "not infra"` · `scripts/test.sh -q` · `uv run ruff check backend`).

**실물 몫**: 워커 = 로컬 day-local 두 계정 SSE / 사용자 = §7.

### WP-BE-4 파일 저장소 — 관리 ID · 환경 = 컨테이너 (7판 · 9판 정정 3)

**근거 스펙**: `40-architecture/deployment.md` 「파일 저장소(Blob) — 구조 · 인증 · 규칙」(정본 · 용도 폴더 셋 = `chat` 씀 · `identity` · `before-after` 이름만 예약 — 이름 셋 사용자 확정 · 컨테이너 = 환경별 설정값 · 8판) · env 표 · Key Vault 줄 / SPEC-004 개정 ⑤ · §3 「첨부 저장 · 열기」(저장소 · 키 · 저장소 꺼짐 · **저장소 접근 실패**) · 오류 표 `photo_disabled` · 케이스 매트릭스 · C-3 / SPEC-000 07 `chat_attachment.file_key`.
**수용 항목**: SPEC-004 **C-A26**(서버 단위) · **C-A27**(실물 ① 워커 · 코디 / ② 사용자) · C-A9 · C-A10 회귀.

**고칠 파일**(grep — `from_connection_string` · `day_chat_blob` · `DAY_CHAT_BLOB` · `chat-blob` · `new_key` · `check_key` · `KEY_PATTERN` 를 **쓰는 곳 전부** · 지금 미커밋 코드 기준):

| 파일 | 무엇 |
|---|---|
| `backend/day/services/chat_storage.py` | **9판 정정 3**: `KEY_PATTERN` · `new_key` · `check_key` 는 지금 모양 `chat/{hospital_id}/{32 hex}.{jpg\|mp4}` **그대로**(7판에 더한 `{APP_ENV}/` 접두 · 「키 환경 = 설정 `app_env`」 검사 · 옛 키 거절을 걷어 냄 — 환경은 컨테이너) · `BlobStorage.from_settings` → 계정 주소 + 컨테이너 + **관리 ID 자격 증명**(`azure.identity.aio.ManagedIdentityCredential` — 다른 자격 증명으로 넘어가는 체인 쓰지 않음) · 자격 증명 · 클라이언트는 처음 쓸 때 만들고 재사용(기동 막지 않음) · 연결 20초 · 읽기 60초 명시 · `storage_from` = `blob` 이면 `day_blob_account_url` · `day_blob_container` 둘 다 있을 때만 · 머리 주석 · **8판**: 관리 ID 토큰 받기 30초(`TOKEN_TIMEOUT = 30` · `asyncio.timeout` 감쌈 · 넘으면 503) · `ResourceNotFoundError` 의 `error_code` 로 `ContainerNotFound` = 접근 실패(503) / `BlobNotFound` = 없음(404) · 재사용 범위 = 프로세스에 자격 증명 하나 · 컨테이너 클라이언트 하나(요청마다 HTTP 세션 새로 만들지 않음) · **앱 종료 때 닫기**(lifespan — `runtime/main.py` 를 `day.public` 경유로) · 컨테이너 이름은 **설정에서만** 온다(코드에 `dev` · `prod` 등 특정 이름 없음) |
| `backend/day/services/chat.py` | 올리기(사진 · 동영상) · 열기 · 첨부 전달에서 저장소 **접근 실패**(인증 · 403 · 컨테이너 없음 · 시간 초과 · 그 밖 Azure 오류)를 503 `photo_disabled` 로(쓰던 키 지우기 시도는 지금 길 그대로) — `new_key` 호출 자리(`upload_photo` · `upload_video`) · `get_storage` 자리(전달 · 열기) · 로그는 원인 종류 · 키 앞자리만 |
| `backend/day/errors.py` | `photo_disabled` 503 을 만드는 함수 하나(글자 · code 그대로 · 새 code 없음) |
| `backend/common/config.py` | **더함** `day_blob_account_url: str` · `day_blob_container: str`(비밀 아님) · **없앰** `day_chat_blob_container` · `day_chat_blob_connection_string` · `day_chat_storage` · `day_chat_storage_dir` 는 그대로 |
| `scripts/deploy/day_vm.py` | `OPTIONAL_SECRETS` 에서 `DAY_CHAT_BLOB_CONNECTION_STRING` 줄 없앰(선택 비밀 = APNs · Soniox 둘) · **없앤 키 이름은 일반 설정 금지 목록에 따로 남긴다**(`FORBIDDEN_CONFIG_KEYS` 가 `OPTIONAL_SECRETS` 에서 오므로 빼면 Git 일반 설정에 그 비밀이 들어가는 길이 열림 — 8판 W5) · `test_day_vm.py`(없앤 키도 config 에 있으면 거절) 유지 |
| `deploy/config/dev.env` · `deploy/config/prod.env` | `DAY_CHAT_STORAGE=blob` · `DAY_BLOB_ACCOUNT_URL=` · `DAY_BLOB_CONTAINER=` 줄(9판 정정 3 — `dev.env`: 계정 주소 = 안내문 값(코디 · 앞 지시) · `DAY_BLOB_CONTAINER=dev` · `DAY_CHAT_STORAGE=blob` / `prod.env`: **값 넣지 않음** — 칸 · 주석만 · prod 배포 때 사용자가 `prod` 등) · `DAY_CHAT_BLOB_CONTAINER` 줄과 연결 문자열 주석 없앰 · 관리 ID 주석 |
| `deploy/compose.local.yaml` · `deploy/local.env.example` | 옛 이름 → 새 이름(로컬은 `disk` 그대로 — Blob 칸은 비움 · 설명) |
| `deploy/Dockerfile` | 확인만(디스크 폴더 `/var/lib/day/chat` — 로컬 디스크용 그대로 · 그 안에 `chat/…` 가 생김 — 지금과 같은 모양) |
| `pyproject.toml` · `uv.lock` | `azure-identity` 추가(aio 쓰는 판) |
| `docs/development/deployment.md` | 선택 비밀 줄 · env 이름 · 관리 ID 한 단락(값 없음) |
| `backend/tests/day/chat/test_chat_units.py` | (8판) 가짜 저장소가 **SDK 예외 모양 그대로**(`ResourceNotFoundError` + `error_code` `ContainerNotFound` / `BlobNotFound`) 던짐 · 토큰 30초 넘김 = 503 · 종료 때 닫기 · 키 모양(`chat/{병원 id}/…` — 환경 폴더 단언 걷어 냄 · 9판) · 「컨테이너 이름은 설정에서만」 단언 · 설정 갈래(주소 · 컨테이너) · 관리 ID 팩토리(가짜) · 시간 상한 인자 · 접근 실패 → 503 |
| `backend/tests/day/chat/test_chat_attachments.py` · `conftest.py` | 디스크 · 가짜 Blob 로 기존 시험이 새 키로 그대로 · 접근 실패 갈래(올리기 · 열기 · 전달) |
| `backend/tests/deploy/test_chat_env_contract.py` · `test_day_vm.py` · `backend/tests/common/test_config.py` | 계약 목록에서 연결 문자열 · `DAY_CHAT_BLOB_CONTAINER` 빼고 `DAY_BLOB_ACCOUNT_URL` · `DAY_BLOB_CONTAINER` 더함 · 선택 비밀 둘 · **dev · prod `DAY_BLOB_CONTAINER` 가 같은 값이라고 단정하지 않음**(환경별 값 — 결정 2) · 없앤 비밀 키 이름 config 거절 유지 |

**확인 · 고칠 수도 있는 자리**(8판): `backend/day/routers/api/chat.py` 열기 스트림(`StreamingResponse(opened.storage.read(...))`) — 본문을 보내기 시작한 뒤 저장소 실패 = 응답 끊김(503 아님) · 끊김 로그에 키 앞자리만 / `backend/runtime/main.py` lifespan 닫기(`day.public` 경유 · `test_import_boundaries`) / `backend/day/public.py`(닫기 함수 노출).

**확인만**: `deploy/compose.yaml`(api 환경이 `env_file` 로 오는지 — 새 칸이 따로 줄 필요 없는지) · Docker 안 관리 ID(IMDS) = 코디가 dev api 컨테이너에서 토큰 받기 확인(2026-11-11) — 코드 · compose 변경 없음 예상 · **앱(`app/`) = 변경 없음**: 앱은 올리기 · 열기 경로 · 응답 모양이 그대로이고, 409 `photo_disabled` = 토스트 · 5xx = 「보내지 못했어요」 + [다시 보내기](`app/lib/chat/chat_state.dart` 보내기 `on ApiError` — 4xx 지움 · 그 밖 `SendState.failed`) · 열기 실패(404 아님) = 그리지 않음(`_load` 가 null) — 첨부가 켜지면 지금 올리기 길이 그대로 돈다.

**하지 말 것**: 저장소 계정 · 주소 · 컨테이너 · 리소스 그룹 · VM · 로그인 계정 **값**을 코드 · 문서 · 시험 · 리포트에 쓰기 · 연결 문자열 · 계정 키 · SAS 경로 남기기 · 다른 자격 증명으로 넘어가는 체인(`DefaultAzureCredential`) · 로컬에서 Blob 붙는 길 · `identity` · `before-after` 폴더에 쓰는 코드 · 옛 키 옮기기 · 새 오류 code · 새 화면 글자 · 앱 수정 · 기동 때 저장소 확인으로 기동 막기 · Key Vault · 저장소 설정 바꾸기(사람 몫).

**시험**: `uv run pytest -q -m "not infra" backend/tests/day/chat backend/tests/deploy backend/tests/common` · 끝에 `scripts/test.sh -q` · `uv run ruff check backend` · `test_import_boundaries` 통과.

**실물 몫**: ① 코디 — dev 설정에 주소 · 컨테이너 값 넣기(값은 사용자 로컬 안내문) · dev 배포 ② 구현 워커(또는 코디) — dev api 컨테이너에서 관리 ID 로 ⓐ 올리기 → 속성 → 범위 읽기(206) → 지우기 ⓑ 컨테이너 `dev` 안 경로 `chat/{병원 id}/…` 확인(`dev` 있음 — 정정 4 · 관리 ID 목록 읽기는 코디 확인) ⓒ 없는 키 열기 = 404(C-A27 ①) · 503 길은 단위 시험으로만 ③ 사용자 — TestFlight 사진 · 동영상 보내기 · 받기(C-A27 ② · §7).

### WP-APP-3 채팅 화면 (4판 — 8 · 9 · 10 · 5판 정정 1 · 6판 정정 2 포함)

**근거 스펙**: SPEC-004 개정 ④ · U-4 「자리가 맞아야 한다」(8) · U-2 「하단 4메뉴 — 폰 대화 화면에서는 숨긴다」(9) · U-2 「메시지별 읽음 표시」(10) · 케이스 매트릭스 3줄 · OQ-C16 ~ C18 / SPEC-003 U-2 예외 줄(개정 ⑩).
**수용 항목**: SPEC-004 **C-A22** · **C-A23** · **C-A25** · C-A16 · C-A12(회귀).

**고칠 파일**(grep — `_menu(` · `localToGlobal` · `_TabBar` · `chatTabActive` · `isFirst` · `Member(` · `Member.fromJson` · `lastReadSeq` · `chat_read` · 지금 미커밋 코드 기준):

| 파일 | 무엇 |
|---|---|
| `app/lib/chat/screens/chat_room_screen.dart` | (8) `_menu` — 지금은 `findRenderObject` → `localToGlobal` 로 길게 누른 순간 한 번 잰 `rect` 에 고정(줄 번호 대신 이름) — 화면이 다시 잡힌 뒤의 말풍선 자리에 복사본 · 메뉴가 붙게(방법은 워커: 키보드를 닫지 않고 띄우기 / 닫힌 뒤 다시 재기 — 이유를 리포트에) · (10) `_content`(`:278~` 시각 칸)에 안 읽은 사람 수(시각 위 · `Ms.primary` · 0 이면 없음 · 시스템 · 지운 · 보내는 중 · 실패 없음) — 복사본도 같은 `_content` 를 그리므로 함께 |
| `app/lib/ui/shell.dart` | (9) 탭바 그리기 조건(`if (!keyboard) _TabBar(...)`) — 폰에서 채팅 탭이 루트(목록)가 아니면 숨김 · **아래 안전 영역**(정정 2 W5): 본문에서 아래 padding 을 빼는 자리(`removePadding(removeBottom: true)` — 탭바가 안전 영역을 먹는다는 전제)를 탭을 숨긴 경우에도 맞게 → 대화 화면(키보드 닫힘) 입력줄 · 방 정보 · 모아보기 · 새 대화 · 초대의 맨 아래 요소가 안전 영역 위 · 아이패드 레일 그대로 · 다른 탭 · 키보드 규칙 그대로 · 채팅 스택이 루트인지 아는 값은 이미 있는 채팅 내비게이터에서(`:178` `popUntil((r) => r.isFirst)` 근처) |
| `app/lib/chat/chat_model.dart` | `Member` 에 `lastReadSeq` · `fromSeq`(없으면 0) · 안 읽은 사람 수 계산 함수 하나(메시지 seq · 보낸 사람 · 멤버 목록 → 수) |
| `app/lib/chat/chat_stream.dart` | `chat_member_read` 이벤트 읽기(모르는 이벤트 무시 규칙 그대로) |
| `app/lib/chat/chat_state.dart` | `chat_member_read` → 그 방 그 멤버 `lastReadSeq` 올림(낮으면 무시 · 단조) · **정정 1**: 메시지를 받는 모든 길(`case 'chat_message'` 등 실시간 · 목록 읽기 · `since` 메우기 · 전달)에서 보낸 사람 `lastReadSeq = max(지금, seq)`(시스템 줄 제외) · `Room.members[]` 가 오는 모든 길(`case 'chat_room'` · 목록 · 재연결 `GET /rooms` · HTTP 응답)에서 **멤버마다 max 로 합치기**(다시 들어온 멤버만 새로 · 빠진 멤버는 목록에 있느냐 · `active` 로) · `chat_read` → 「나」 멤버 줄도 max · **정정 2**: 「보고 있는 방」이면 화면에 그린 메시지까지 나를 읽은 것으로 셈(읽음 요청 전에도 · 방을 열 때도) · `ChatState.watching` 판정 자체는 바꾸지 않음(탭을 숨겨도 `chatTabActive` 그대로 — C-A23 · 줄 번호 대신 이름) |
| `app/lib/chat/screens/chat_list_screen.dart` · `chat_info_screen.dart` | 탭 숨김 범위 확인(목록 = 보임 · 방 정보 = 숨김) — 바꿀 것이 있으면만 |

**하지 말 것**: 새 화면 글자 · 새 색 토큰 · 서버에 수를 요구 · 읽음 요청 횟수 늘리기 · 아이패드 레일 · 시술현황 · 설정 탭 동작 · 키보드 밖 셸 규칙 바꾸기 · 목록 Badge · 탭 배지 계산 바꾸기.

**시험**(`fvm flutter analyze` · `fvm flutter test`): `app/test/ui/chat_ui_test.dart`(8 — 키보드 높이를 바꾼 상태에서 길게 누르기 · 복사본 자리 = 말풍선 자리 · 메뉴 화면 안 / 10 — 숫자 그리기 · 0 사라짐 · 갈래) · `app/test/chat/chat_state_test.dart`(`chat_member_read` · `chat_read` · 재연결 · 초대 · 나가기 · 비활성 · **정정 1 갈래**: 받은 뒤 읽음 요청 전에 답장 · 옛 `Room` 이 나중에 옴 · `chat_member_read` 순서 뒤바뀜 · 전달 · 나갔다 다시 들어온 멤버 · **정정 2 갈래**: 보고 있는 방에서 받은 메시지에 내 숫자 안 뜸 · 보고 있지 않으면 뜸 · `chat_member_read`(B=12) 뒤 옛 `chat_room`(B=9) · **가짜 서버(`chat_fake.dart`)가 이벤트 순서를 일부러 바꿔 보냄**) · 아래 안전 영역 시험 + 아래 inset 이 있는 기기 크기 캡처 1장(W5) · `app/test/chat/chat_contract_test.dart`(`Member` 새 칸) · `app/test/support/chat_fake.dart`(가짜 서버 새 칸 · 이벤트) · `app/test/ui/app_flow_test.dart` · `actions_test.dart` · `session_race_test.dart` · `notification_ui_test.dart`(탭바를 찾는 기존 시험 — 9 로 기대가 바뀌는 곳만) · 캡처 `test/capture/chat_capture_test.dart`(키보드 열림 길게 누르기 · 숫자 · 탭 없는 대화 장면).

**실물 몫**: 워커 = 시뮬레이터 캡처 · 가짜 서버 → BE-3 뒤 로컬 두 계정 / 사용자 = 실기기(§7 — 그림 8 재현 · 두 계정 이상 읽음).

---

## 3. WP 사이 계약 (서버 BE-1 ↔ 앱 APP-2 — 같은 표를 본다)

| 무엇 | 요청 | 응답 · 이벤트 | 오류(`{detail, code, field}`) | 스펙 |
|---|---|---|---|---|
| 그룹 이름 #22 | `PUT /api/chat/rooms/{roomId}/title` · Bearer · 본문 `{"title": string \| null}` · 모르는 칸 = 400 | 200 `Room`(요청 계정 기준 — `id · kind · title · name · members · memberCount · muted · unread · lastMessage · lastMessageAt · createdAt · fromSeq · lastReadSeq`) · 같은 이름이면 200 · 이벤트 없음 | 400 `chat_group_only`(1:1 · `detail` 내부 문장 · 앱은 code 로만) · 400 `invalid_request` `field=title`(41자 이상) · 404 `chat_room_not_found` · 403 `forbidden` · 401 | SPEC-004 §3 #22 · 규칙 |
| 이름 바뀜 알림 | — | SSE `GET /api/chat/stream` 이벤트 `chat_room` `{"room": Room}`(받는 계정 기준) — 지금 멤버 전부(바꾼 사람 다른 기기 포함) | — | SPEC-004 §3 「실시간」 |
| 알림 설정 읽기 | `GET /api/me/notification-settings` | `{"items": [{"kind": "doctor_call", "enabled": bool}, {"kind": "chat", "enabled": bool}]}` — 받는 종류만 · 차례 `doctor_call` → `chat` · 저장 없으면 `true` · `chat` 이 없으면 앱은 켜짐으로 봄 | 401 | SPEC-005 §3 #3 · 받는 종류 |
| 알림 설정 쓰기 | `PUT /api/me/notification-settings` `{"kind": "chat", "enabled": bool}` | `{"items": …}`(위와 같은 모양) | 400 `setting_not_allowed`(받는 종류 아님) · 400 `invalid_request` | SPEC-005 §3 #4 |
| 채팅 푸시 | (서버 발송) | `kind: "chat"` 본문 그대로 · `chat` 끈 계정에는 안 감 · 제목 그룹 = 「{보낸 사람} · {방 이름}」(발송 작업이 방을 읽는 때의 이름) | — | SPEC-004 §3 「채팅 푸시」 |
| 채팅 403 | 모든 채팅 HTTP · 스트림 | — | 403 `forbidden` → 앱 거절 안내 | SPEC-004 U-1 · 권한 표 |

**읽음 표시(4판 · BE-3 ↔ APP-3)**

| 무엇 | 요청 | 응답 · 이벤트 | 스펙 |
|---|---|---|---|
| 멤버 읽은 자리 | `GET /api/chat/rooms` 등 `Room` 이 나오는 모든 곳(목록 #2 · 1:1 열기 #3 · 만들기 #4 · 초대 #5 · 이름 바꾸기 #22 · `chat_room` 이벤트) | `Room.members[]` 항목 = `{id, name, role, active, me, lastReadSeq: int, fromSeq: int}`(지금 멤버만 · 「나」 맨 위 그대로) | SPEC-004 §3 `Member` |
| 다른 멤버가 읽음 | (서버 발송 — 읽음 #15 가 실제로 올렸을 때) | SSE `chat_member_read` `{"roomId": uuid, "accountId": uuid, "lastReadSeq": int}` — 그 방 지금 멤버 중 읽은 사람 아닌 계정 · 읽은 사람은 기존 `chat_read` | SPEC-004 §3 「실시간」 |
| 수 세기(앱) | — | 메시지 `seq` · 보낸 사람 · `members[]` → 수 = 지금 멤버 중 보낸 사람 아님 · `active` · `fromSeq < seq` · `lastReadSeq < seq` · 시스템 · 지운 · 보내는 중 · 실패 = 없음 · 0 = 없음 | SPEC-004 U-2 |
| 멤버 읽은 자리 합치기(앱 · 정정 1 — `correction-read-1.md`) | — | ① 그 방 메시지를 어느 길로 받든(실시간 `chat_message` · 목록 · `since` 메우기 · 전달) 보낸 사람 `lastReadSeq = max(지금, 그 seq)` · 시스템 줄 제외 ② `lastReadSeq` 는 `Room.members[]`(목록 · `chat_room` · 응답) / `chat_member_read` / ① 어느 길이든 **더 클 때만** 올림 · 예외 = 나갔다 다시 들어온 멤버(새 멤버 줄)는 받은 값으로 새로 ③ 서버 변경 없음 — 보내기는 `chat_member_read` 를 내지 않음 | SPEC-004 U-2 「멤버 읽은 자리 합치기」 · 읽음 표시 계약 |
| 보고 있는 방 표시(앱 · 정정 2 — `correction-read-2.md` · 코디 기본값) | — | 「보고 있는 방」이면 화면에 그린 메시지까지 나를 읽은 것으로 셈(읽음 요청 전에도) · 아니면 내 `lastReadSeq` · 서버 변경 없음 | SPEC-004 U-2 · OQ-C17 |

통역(BE-2)은 앱과 새 계약이 없다 — 앱이 이미 가진 계약(SPEC-003 §3 「통역」 프레임 표)에 서버를 맞춘다.

## 4. 순서 · 의존

```
backend : BE-1 ──▶ BE-2 ──▶ BE-3(4판)          (BE-1 · BE-2 끝남)
mobile  : APP-1 ──▶ APP-2 ──▶ APP-3(4판)        (APP-1 · APP-2 끝남)
7판     : BE-4(파일 저장소) — 앱 변경 없음 · 다른 WP 와 파일이 안 겹침(`chat_storage.py` · 설정 · 배포) → BE-3 뒤 backend 워커 · dev 배포 뒤 실물
4판     : BE-3 ∥ APP-3 — 앱은 §3 읽음 계약 표 + 가짜 서버로 동시에 짓고, BE-3 뒤 로컬 두 계정으로 C-A25 확인 · 8 · 9 는 서버와 무관
```

- 동시에: BE-1 ∥ APP-1 · BE-2 ∥ APP-2.
- 먼저: BE-1 이 끝나야 APP-2 의 로컬 실물 확인(#22 · `chat` 설정 · 푸시 받는 사람). APP-2 코드는 §3 표 + 가짜 서버로 먼저 지을 수 있다.
- BE-2 는 앱과 무관 — 앱 쪽 기다림 없음. 실물 A-46 은 BE-2 dev 배포 뒤.
- 배포: 서버 먼저 dev 배포해도 옛 앱에 해가 없다(옛 앱은 모르는 kind 를 안 그림 · #22 를 안 부름). 앱은 다음 TestFlight 빌드(번호 2 이상)에.

## 5. 통역 원천 가져오기 규칙 (WP-BE-2)

- 원천 = **interpret-pwa `origin/main` `17c26b5`**. 로컬 canonical(`/Users/kknaks/git/toy_pr2/interpret-pwa`)의 `main` 은 뼈대 커밋뿐이라 파일을 **`git -C /Users/kknaks/git/toy_pr2/interpret-pwa show origin/main:<path>`** 로 읽는다(체크아웃 · 수정 금지). 복사(import 아님) · 파일 머리에 원천 경로 · ref 를 적는다.

| 원천 파일(`back/…`) | DAY 자리 | 어떻게 |
|---|---|---|
| `app/api/interpret.py` | `backend/day/routers/api/interpret.py` | 인증 다시 씀(§2 BE-2) |
| `app/service/interpret/session.py` | `backend/day/services/interpret/session.py` | 그대로 + 기록기 제거 · 자리 잡기/반납 · `session_limit` |
| `app/service/interpret/soniox.py` | 같은 폴더 | 그대로(`{"keep_alive": true}` 판 · `CONNECT_TIMEOUT = 10`) |
| `app/service/interpret/assembler.py` · `chinese.py` · `langs.py` · `__init__.py` | 같은 폴더 | 그대로 |
| `app/service/glossary.py` | `backend/day/services/glossary.py`(+ `dtos/glossary.py`) | 그대로(위치만) |
| `seed/glossary.json` | `backend/day/seed/glossary.json` | 바이트 그대로 |
| `app/container.py` 중 통역 부분 | `day/public.py` · 서비스 팩토리 | DAY 모양으로 다시(Soniox 팩토리 주입 · 사전 적재 · context) |
| `app/config.py` 중 통역 칸 | `common/config.py` | `DAY_SONIOX_API_KEY` · `DAY_INTERPRET_MAX_SESSIONS` 만 |
| `tests/test_interpret.py` · `test_context.py` · `test_seed.py` · `conftest.py` · `seed_tables.py` | `backend/tests/day/interpret/` | DAY fixture · 인증으로 고쳐서 |
| `scripts/live_check.py` | `scripts/interpret_live_check.py` | seed · idle · zhhant 갈래만 |
| **가져오지 않음**: `app/service/records.py` · `tests/test_records.py` · `scripts/import_glossary.py` · `tests/test_import_glossary.py` · 앞단(front) 전부 | — | 기록 없음(OQ-A39) · 시드는 이미 있음 |

## 6. 위험 (사용자 · 코디가 알 것)

| 위험 | 무엇이 일어나나 | 대응 |
|---|---|---|
| **깨진 시드 = api 기동 실패** | 통역 사전 파일 하나가 깨지면 api 가 뜨지 않아 **로그인 · 시술현황 · 채팅 · 알림 전부가 멈춘다**(원천 그대로 · SPEC-003 「사전」) | 시드는 바이트 그대로만 · 시험 `test_seed` 가 CI 에서 같은 검사 · 배포 확인이 기동 실패를 잡아 롤백 — **사용자에게 이 점을 알린다** |
| `runtime` → `day.public` 경계 | lifespan 에서 `day.services…` 를 직접 import 하면 `test_import_boundaries` 실패 | 적재 함수를 `day.public` 로만 노출 |
| OpenCC × Python 3.13 | `opencc-python-reimplemented` 가 3.13 에서 안 돌면 번체 자막 · `t2s` 실패(I-3) | 서버 단위 시험 번체 갈래로 먼저 확인 · 막히면 planner 에게(스펙 변경 필요) |
| Caddy `request_body` 6MiB | 업그레이드 뒤 스트림에 걸리면 듣는 시간 약 3분 20초에 통역이 끊김(I-2) | A-46 긴 세션 · 걸리면 앞단에서 통역 경로만 푸는 안을 워커가 제안(배포 문서 갱신 · 사용자 승인) |
| 이벤트 루프 막힘 · 메모리 | 사전 줄이기 · OpenCC 가 동기라 api 하나(worker 1)의 SSE · API 가 함께 느려질 수 있음 · dev api 메모리 상한은 예상치(I-4) | 기동 때 7개 언어 context 미리 만들기 · 시간 재서 리포트 · 배포 뒤 `docker stats` |
| Soniox 동시 한도 | 원천 주석 「TTS 동시 한도 3」이 사실이고 키 단위라면 상한 6 보다 먼저 막힘 · dev · prod 가 같은 공용 키(I-1) | A-45 때 확인 · 6 보다 작으면 사용자에게 상한 다시 묻기 |
| 자리 누수 | 반납 경로 하나만 빠져도 상한 6 이 금방 참 | A-44 반납 갈래 전부 · 어떤 경로든 `finally` 한 번 |
| 오래 열린 세션 | 수명 상한 없음 → 드로어를 열어 둔 기기가 자리를 쥠 | 사용자 질문 OQ-A46(답 전엔 상한 없음) |

## 7. 배포 뒤 사용자 실기기 확인 (한곳에)

dev 배포(서버) + TestFlight 다음 빌드(앱) 뒤:

| # | 확인 | 스펙 |
|---|---|---|
| 1 | 시술현황: 시술이 모두 끝난 방 카드 = 「시술 모두 완료」 / 「마지막 종료」 · 카드 아래 [귀가 대기] · 누르면 토스트 · 카드 빠짐 · 확인 필요 카드 = 테두리 없이 상자만 옅은 빨강 + 왼쪽 띠 | SPEC-003 A-41 ~ A-43 |
| 2 | 채팅 403(권한 없는 계정 · 비활성): 「서버에 연결 중…」이 남지 않고 권한 없음 안내 + [로그아웃] · 앱을 뒤로 보냈다 앞으로 오면 한 번 다시 봄 | SPEC-004 C-A19 |
| 3 | 그룹 방 정보에서 이름 바꾸기(✓ · ✕) · 다른 기기 · 다른 참여자 화면이 바로 바뀜 · 대화에 줄이 생기지 않음 · 그 뒤 푸시 제목이 새 이름 | SPEC-004 C-A20 |
| 4 | 설정 「알림」 「채팅」 끔 → 모든 방 푸시 · 배너 없음 · 방별 「알림」 값 그대로 · 다시 켜면 방별대로 · **두 기기**: 다른 기기의 배너는 그 기기가 다음에 앞으로 올 때부터 0 | SPEC-004 C-A21 · SPEC-005 N-A13 |
| 5 | 통역: [통역하기] → 연결 → 한국어 · 고객 언어 한 마디씩 → 자막 양쪽 · 번역 음성 · 언어 바꾸기 · [종료] · (코디) 서버 로그 시드 버전 | SPEC-003 A-46 · A-14 |
| 6 | 통역 긴 세션: **듣는 상태 누적 약 3분 20초 이상**(번역 음성 재생 · 멈춤 시간은 빼고) 끊기지 않는지 | SPEC-003 A-46 · I-2 |
| 7 | (앞 판 미확인) 실기기 푸시 수신 · 원장 호출 알림 | `_RESUME` §1 |
| 8 | (4판) 채팅 대화에서 **키보드를 연 채** 말풍선 길게 누르기 → 복사본 · 메뉴가 그 말풍선 자리에(그림 8 재현이 안 됨) | SPEC-004 C-A22 |
| 9 | (4판) 폰: 채팅 목록 = 하단 4메뉴 보임 · 대화 · 방 정보 = 숨김 · 키보드를 열고 닫아도 입력줄 아래 탭이 다시 나오지 않음 · 아이패드 레일 그대로 | SPEC-004 C-A23 |
| 11 | (7판) 사진 · 동영상 보내기 · 받기(다른 계정) · 크게 보기 · 재생 · 모아보기 — 저장소가 켜진 뒤 | SPEC-004 C-A27 ② |
| 10 | (4판) 두 계정 이상: 그룹 · 1:1 에서 말풍선 옆 숫자가 읽을 때마다 줄고 0 이면 사라짐 · 다른 기기 화면도 바로 | SPEC-004 C-A25 |
