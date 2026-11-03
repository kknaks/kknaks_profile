# 07 알림 · 접수 · 채팅

2026-11-03 사용자와 정함 — 검토표를 만들고 바로 적용. 공통 규칙은 [README.md](README.md). 검토표: https://claude.ai/artifact/GaQCH46WsrFpi6mFoDxDdc

## 정한 것

- cc 가 직접 만든 기능이다(KOS 미러가 아님). cc 13테이블을 DAY 공통 규칙으로 옮긴다 — uuid · timestamptz(UTC) · 소프트 딜리트 ·
  `account` · `staff` 참조 · 예약/방문은 `visit` 하나 · 파일은 저장소 키(`file_key`).
- KOS 와 주고받는 것 둘 — 문진 제출(`submit-visitor-questionnaire`) · 신분증 사진 업로드(`register-visitor-images`)는 `external_outbox` 로
  보내고 결과도 거기에 둔다. 핵심 테이블에 `kos_status` 같은 칸을 두지 않는다.
- 채팅은 uuid 에 순서가 없으므로 방마다 `seq` 를 둔다 — 안 읽음 · 보이는 경계를 `seq` 로 계산(cc 는 정수 id 순서).
- `push_log` 는 무엇을 보낸 푸시인지만 가리킨다(알림 · 채팅 메시지 · 화면 띄우기) — 호출 · 방문은 알림에서 찾는다.
- `chat_photo` → `chat_attachment`(사진 · 동영상).
- 법적 검토 필요(cc 표시 그대로): 신분증 · 여권 사진 · 고객 문진 · 직원 채팅의 고객 정보 — 보관 기간 · 열람 기록.
- `notice`(KOS 공지 사본)는 예약 현황을 정할 때 다시 본다.

## device · 푸시 기기

| 필드 | 타입 | 필수 | 설명 | cc |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 앱 설치 1개 = 1행 | cc device (id = 앱 deviceId) |
| `account_id` | uuid FK → account | ✓ |  | cc device.account_id |
| `install_id` | varchar UNIQUE | ✓ | 앱 설치 단위 id — 토큰이 바뀌어도 행 하나 | cc device.install_id |
| `push_token` | 암호화 text | ✓ | APNs 토큰 | cc device.token |
| `name · kind` | varchar · enum phone · tablet |  | 기기 이름 · 종류 | cc device.name · kind |
| `last_seen_at` | timestamptz |  | 마지막 접속 | cc device.last_seen_at |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## notification · 알림함

| 필드 | 타입 | 필수 | 설명 | cc |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 발송 1회 × 받는 계정 1 | cc notification |
| `hospital_id` | uuid FK → hospital | ✓ |  |  |
| `account_id` | uuid FK → account | ✓ | 받는 사람 | cc notification.account_id |
| `kind` | enum doctor_call · counselor_call | ✓ |  | cc notification.kind |
| `doctor_call_id` | uuid FK → doctor_call |  | 의사 호출 알림이면 | cc notification.call_id |
| `visit_id` | uuid FK → visit |  |  | cc visit_id · reservation_id (예약 · 방문 합침) |
| `title · body` | varchar · text | ✓ |  | cc notification.title · body |
| `read_at` | timestamptz |  |  | cc notification.read_at |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## notification_setting · 알림 켜기/끄기

| 필드 | 타입 | 필수 | 설명 | cc |
|---|---|---|---|---|
| `account_id · kind` | uuid FK · enum · PK | ✓ | 계정 × 알림 종류 | cc notification_setting |
| `is_enabled` | bool | ✓ |  | cc enabled |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## push_log · 푸시 발송 내역 (쌓기만)

| 필드 | 타입 | 필수 | 설명 | cc |
|---|---|---|---|---|
| `id` | uuid PK | ✓ |  | cc push_log |
| `account_id · device_id` | uuid FK |  |  | cc push_log.account_id · device_id |
| `kind` | enum doctor_call · counselor_call · display · chat | ✓ |  | cc push_log.kind |
| `notification_id · chat_message_id · display_request_id` | uuid FK |  | 무엇을 보낸 푸시인지 — 호출 · 방문은 알림에서 찾는다 | cc push_log (call_id · visit_id · reservation_id 는 뺌) |
| `category` | enum call |  | 알림에서 바로 수락하는 푸시 | cc push_log.category |
| `token_tail` | varchar(6) |  | 기기 토큰 끝 6자리만 | cc push_log.token_tail |
| `status` | enum sent · failed · skipped_no_key · token_removed | ✓ |  | cc push_log.status |
| `apns_status · apns_reason · apns_id` | int · varchar · varchar |  | APNs 응답 | cc push_log.apns_* |
| `attempts` | int | ✓ |  | cc push_log.attempts |
| `sent_at` | timestamptz |  |  | cc push_log.sent_at |
| `created_at` | timestamptz | ✓ | 쌓기만 — 고치거나 지우지 않는다 |  |

## display_request · 고객 화면 띄우기 (QR)

| 필드 | 타입 | 필수 | 설명 | cc |
|---|---|---|---|---|
| `id` | uuid PK | ✓ |  | cc display_request |
| `hospital_id` | uuid FK → hospital | ✓ |  |  |
| `visit_id` | uuid FK → visit | ✓ |  | cc reservation_id (예약 · 방문 합침) — 고객은 방문에서 |
| `kind` | enum | ✓ | 띄울 화면 종류(문진 등) | cc display_request.kind |
| `device_id` | uuid FK → device |  | 띄울 기기 | cc display_request.device_id |
| `qr_token_hash · qr_nonce` | varchar | ✓ | QR 토큰은 해시만 · 고객 문진 웹 토큰 | cc display_request |
| `status` | enum pending · opened · done · canceled · expired | ✓ |  | cc display_request.status |
| `created_by_staff_id` | uuid FK → staff | ✓ |  | cc display_request.created_by |
| `expires_at · opened_at · closed_at` | timestamptz |  |  | cc display_request |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## identity_check · 신분 확인 표시

| 필드 | 타입 | 필수 | 설명 | cc |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 표시만 — 접수 조건 아님 | cc identity_check |
| `customer_id` | uuid FK → customer | ✓ |  | cc identity_check.customer_id |
| `status · method` | enum · enum | ✓ | 확인 결과 · 방법(여권 스캔 등) | cc identity_check.status · method |
| `device_id` | uuid FK → device |  | 확인한 기기 | cc identity_check.device |
| `id_photo_id` | uuid FK → id_photo |  |  | cc identity_check.photo_id |
| `checked_at` | timestamptz | ✓ |  | cc identity_check.checked_at |
| `checked_by_staff_id` | uuid FK → staff | ✓ |  | cc identity_check.actor |
| `event_id` | uuid FK → event_log |  |  | cc identity_check.event_id |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## id_photo · 신분증 · 여권 사진

| 필드 | 타입 | 필수 | 설명 | cc |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 파일은 저장소에 — 법적 검토 필요(cc 표시 그대로) | cc id_photo |
| `customer_id` | uuid FK → customer | ✓ |  | cc id_photo.customer_id |
| `visit_id` | uuid FK → visit |  |  | cc id_photo.reservation_id |
| `doc_type` | enum passport · id_card … | ✓ |  | cc id_photo.doc_type |
| `file_key · bytes · sha256` | varchar · int · varchar | ✓ | 저장소 키(파일 이름 대신) · 크기 · 해시 | cc file_name · bytes · sha256 |
| `created_by_staff_id` | uuid FK → staff | ✓ |  | cc id_photo.created_by |
| `KOS 업로드 상태` | — |  | KOS 고객 이미지로 올리기 — external_outbox 로 보내고 결과도 거기에(핵심 테이블에 kos_status 를 두지 않는다) | cc id_photo.kos_status · kos_error |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## questionnaire_history · 문진 이력

| 필드 | 타입 | 필수 | 설명 | cc |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 방문별 문진 — 법적 검토 필요(cc 표시 그대로) | cc questionnaire_history |
| `customer_id` | uuid FK → customer | ✓ |  | cc questionnaire_history.customer_id |
| `visit_id` | uuid FK → visit |  |  | cc questionnaire_history.reservation_id |
| `submitted_at` | timestamptz | ✓ | 제출 시각 | cc kos_submitted_at |
| `source` | enum read · app_submit · web_submit | ✓ | 외부에서 읽음 · 앱 제출 · 고객 웹 제출 | cc questionnaire_history.source |
| `language` | varchar |  |  | cc questionnaire_history.language |
| `answers` | jsonb | ✓ | 문항 · 답 — 문진 원문 | cc questionnaire_history.answers |
| `device_id · display_request_id` | uuid FK |  |  | cc questionnaire_history |
| `fetched_at` | timestamptz |  | 외부에서 읽은 시각 | cc questionnaire_history.fetched_at |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ | 제출은 external_outbox 로 KOS 에 보낸다 |  |

## chat_room · 채팅방

| 필드 | 타입 | 필수 | 설명 | cc |
|---|---|---|---|---|
| `id` | uuid PK | ✓ |  | cc chat_room |
| `hospital_id` | uuid FK → hospital | ✓ | 병원 안 채팅 |  |
| `kind` | enum direct · group | ✓ |  | cc chat_room.kind |
| `direct_key` | varchar UNIQUE |  | 1:1 만 「작은 account id:큰 account id」 | cc chat_room.direct_key |
| `title` | varchar |  |  | cc chat_room.title |
| `created_by_account_id` | uuid FK → account | ✓ |  | cc chat_room.created_by |
| `last_message_at` | timestamptz |  | 방 목록 정렬 | cc chat_room.last_message_at |
| `last_seq` | bigint | ✓ | 방의 마지막 메시지 순번 — uuid 는 순서가 없어서 순번을 따로 둔다 | cc 정수 id 순서 |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## chat_member · 채팅방 멤버

| 필드 | 타입 | 필수 | 설명 | cc |
|---|---|---|---|---|
| `room_id · account_id` | uuid FK · PK | ✓ | 행은 지우지 않는다(나가기 = left_at) | cc chat_member |
| `joined_at · left_at · hidden_at · last_viewed_at` | timestamptz |  |  | cc chat_member |
| `last_read_seq` | bigint | ✓ | 안 읽음 = seq > 이 값 | cc last_read_message_id |
| `from_seq` | bigint | ✓ | 보이는 경계 — seq > 이 값만 본다(들어온 뒤 대화만) | cc from_message_id |
| `is_muted` | bool | ✓ |  | cc muted |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## chat_message · 메시지

| 필드 | 타입 | 필수 | 설명 | cc |
|---|---|---|---|---|
| `id` | uuid PK | ✓ |  | cc chat_message |
| `room_id` | uuid FK → chat_room | ✓ |  | cc chat_message.room_id |
| `seq` | bigint | ✓ | 방 안 순번 — (room_id, seq) 유일 | cc 정수 id |
| `account_id` | uuid FK → account | ✓ | 보낸 사람 | cc chat_message.account_id |
| `kind` | enum text · photo · video · system | ✓ |  | cc chat_message.kind |
| `body` | text |  |  | cc chat_message.body |
| `attachment_id` | uuid FK → chat_attachment |  |  | cc chat_message.photo_id |
| `client_id` | varchar |  | 앱이 만든 id — (account_id, client_id) 유일 · 중복 전송 막기 | cc chat_message.client_id |
| `edited_at` | timestamptz |  | 마지막으로 고친 시각 | cc chat_message.edited_at |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ | 소프트 딜리트 · 보존 기간 없음(cc 그대로) | cc chat_message.deleted_at |

## chat_attachment · 첨부 (사진 · 동영상)

| 필드 | 타입 | 필수 | 설명 | cc |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 전달본 = 같은 파일을 가리키는 새 행 | cc chat_photo |
| `room_id · account_id · message_id` | uuid FK |  |  | cc chat_photo |
| `kind` | enum photo · video | ✓ |  | cc chat_photo.kind |
| `file_key · bytes · sha256` | varchar · int · varchar | ✓ |  | cc chat_photo.file_name · bytes · sha256 |
| `width · height` | int |  |  | cc chat_photo |
| `duration_ms · thumb_file_key` | int · varchar |  | 동영상만 | cc chat_photo.duration_ms · thumb_file_name |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  | cc chat_photo.deleted_at |

## notice · KOS 공지 사본

| 필드 | 타입 | 필수 | 설명 | cc |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 예약 현황 화면 공지 — 예약 현황을 정할 때 다시 본다 | cc notice |
| `hospital_id` | uuid FK → hospital | ✓ |  |  |
| `content` | text | ✓ |  | cc notice.content |
| `released_at` | timestamptz |  |  | cc notice.released_at |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ | 외부 id 는 external_ref | cc notice.deleted · synced_at |
