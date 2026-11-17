---
type: spec
id: SPEC-001
title: "1층 스키마 — 상담 DM(인스타그램 · 페이스북 메신저) 원본 정규화(SQLite) · 원본 필드 대응 · 건수 기준"
version: 0.2.1
status: accepted
product: consult-analysis
created_at: 2026-11-16
updated_at: 2026-11-16
tags:
  - product/consult-analysis
  - doc/spec
  - status/accepted
links:
  baselines:
    - "[[baseline-001-consult-data|BASE-001]]"
  decisions:
    - "[[decision-001-two-layers|DEC-001]]"
  specs: []
  works:
    - "[[work-001-layer1-load|WORK-001]]"
  releases: []
  related: []
sources:
  - para/projects/summer-star/consult-analysis/10-decision/decision-001-two-layers.md (D-01 ~ D-15 · accepted — D-12 반응 테이블 · D-13 폴더 밖 대화 JSON · D-14 페이스북 메신저 포함 · D-15 채널 칸)
  - para/projects/summer-star/consult-analysis/00-baseline/baseline-001-consult-data.md (원본 실측 — 코디네이터 대략치)
  - reference/2026-11-16-linky-data/ (원본 · gitignore · read-only — 2026-11-16 planner 가 두 채널의 방 JSON 1,916개를 전부 열어 셈. 이 문서의 「실측」은 전부 이 집계다)
---

# 1층 스키마 — 계약

> etl 워커가 그대로 구현하는 계약이다. 원본(Meta 내보내기 JSON)을 **펼치기만** 해서 로컬 SQLite 에 담는다.
> 판단(언어 · 국적 · 문의 유형 · 예약 단계)은 여기 없다 — 2층이다(D-01 · D-05).
>
> SSOT 순서(이기는 순): ① DEC-001 ② 원본 JSON 실측(이 문서 §3 · §7) ③ 이 문서의 기본값.
> 건수는 이 문서 §7 이 기준이다(D-03).
>
> 이 레포는 PUBLIC 이다(D-10). 이 문서에는 구조와 건수만 있다. 고객 이름 · 메시지 본문 · 계정명 · 폴더명은 쓰지 않는다.

## 변경 이력

| 버전 | 날짜 | 내용 |
|---|---|---|
| 0.1.0 | 2026-11-16 | 처음 씀 — 인스타그램 방 폴더 510 · 테이블 · 원본 키 대응 40개 · 키 규칙 · 변환 규칙 · 건수 기준 · 실행 인터페이스 · 열린 것 OQ-101 ~ 103 |
| 0.2.0 | 2026-11-16 | **범위를 두 채널로**(D-14) — 페이스북 메신저 1,405방 · 21,612건 추가 · `conversation.channel`(D-15) · `box` 에 `filtered_threads` · 방 키 = (`channel`, `thread_path`) · 폴더 밖 대화 JSON 1개를 싣는다(D-13 · §4.1) · `reaction` 을 정식 테이블로(D-12) · 원본 키 대응표를 두 채널 합쳐 **43개**로(새 키 `sticker` · `sticker.uri` · `sticker.ai_stickers`) · `attachment.kind` 에 `sticker` · 우리 계정 판별을 채널별로 · 대체 키 순서에 채널 반영 · 건수 기준 §7 을 채널별 + 합계로 다시 셈 · OQ-101 ~ 103 닫음 |
| 0.2.1 | 2026-11-16 | 검수 WARN 반영 — 멈춤 강화(칸 · 건수 · 대응표는 그대로) · **G-12 넓힘**: 보관함 바로 아래에 폴더도 `*.json` 도 아닌 보통 파일(숨김 아님)이 있으면 멈춘다(§1 · §4.1 · W-1) · **G-13 새로**: 원본 파일 읽기 실패(JSON 깨짐 · 비 ASCII 바이트 · 읽기 오류)도 번호와 위치를 찍고 멈춘다(§5.1 · §5.4 · W-2) |

## 0. 근거 표기

- `D-NN` = DEC-001 의 결정. `BASE` = BASE-001.
- 「실측」 = 2026-11-16 planner 가 원본 방 JSON 을 전부 열어 센 값. 대상은 §1 의 1,916개 파일.
- 「기본값」 = 결정 · 실측에서 바로 나오지 않아 이 문서가 정한 구현 기본값. 정책이 아니라 형식(칸 이름 · 값 이름 · 저장 형식)에만 쓴다.
- 채널 표기: **IG** = 인스타그램(`channel = 'instagram'`) · **FB** = 페이스북 메신저(`channel = 'facebook'`).

## 1. 범위 — D-01 · D-02 · D-11 ~ D-15

채널마다 메시지 루트가 하나다. 그 아래 폴더 하나하나가 「보관함」이다.

| 채널 | 메시지 루트(원본 루트 기준) |
|---|---|
| IG | `your_instagram_activity/messages/` |
| FB | `this_profile's_activity_across_facebook/messages/` |

**In** — 실측

| 채널 | 보관함(`box`) | 방 폴더 | 폴더 밖 대화 JSON(D-13) | 방 |
|---|---|---|---|---|
| IG | `inbox` | 495 | 0 | 495 |
| IG | `message_requests` | 15 | 1 | 16 |
| FB | `inbox` | 1,404 | 0 | 1,404 |
| FB | `filtered_threads` | 1 | 0 | 1 |
| **합** | | **1,915** | **1** | **1,916** |

- 보관함은 위 넷이 전부다. 메시지 루트 아래 폴더는 IG 2개 · FB 3개(`stickers_used` 포함)뿐이다.
- 테이블: `conversation` · `customer` · `message` · `attachment`(D-02) · `reaction`(D-12).
- 메시지 루트 아래에 **위 표에 없는 폴더**가 있으면 멈춘다(G-12) — 모르는 보관함을 조용히 건너뛰지 않는다.
- 보관함 **바로 아래**에는 방 폴더와 `*.json` 파일(D-13)만 있어야 한다. 그 밖의 보통 파일(숨김 아님)이 있으면 멈춘다(G-12 · 실측 0) — 모르는 꼴을 조용히 건너뛰지 않는다.

**Out**

| 대상 | 실측 | 처분 |
|---|---|---|
| 2층(언어 · 국적 · 문의 유형 · 예약 단계) | — | 이번 범위 아님(D-05 · D-11). 자리는 §8 한 줄 |
| 첨부 파일 자체(사진 · PDF · 영상) | 방 폴더 안 IG 699 · FB 2,647개 | 읽지 않는다. `attachment.uri` 가 경로만 가리킨다(DEC OQ-003) |
| FB `stickers_used/` | 이미지 18개(png 17 · webp 1) | 폴더는 방이 아니다 — 방으로 읽지 않는다. 파일은 `sticker.uri` 가 가리킨다(`attachment` 행 115) |
| IG `secret_conversations.json` | 키 `ig_secret_conversations` → `armadillo_devices`(3) · `calls`(0) | 버림 — 기기 정보뿐이고 대화가 아니다 |
| FB `messaging_settings.json` · `messenger_active_status_settings.json` · `your_messenger_app_install_information.json` | 셋 다 최상위 키 `media` · `label_values` · `fbid`. `participants` · `messages` 없음 | 버림 — 설정 · 설치 정보이고 대화가 아니다 |
| `.DS_Store` 같은 숨김 파일(이름이 `.` 으로 시작) | — | 무시 — 어느 깊이든. 숨김이 아닌 모르는 파일이 보관함 바로 아래 있으면 무시가 아니라 G-12 |

메시지 루트 **바로 아래** 놓인 JSON 파일(위 넷)은 방이 아니다. 보관함 **바로 아래** 놓인 JSON 파일만 방이다(§4.1).

## 2. 테이블 — D-02 · D-04 · D-09 · D-12 · D-15

SQLite. `PRAGMA foreign_keys = ON`. 불리언은 `INTEGER` 0/1. 문자열은 전부 **복원된 값**(§5.1)이다.
PK 는 전부 대체 키(정수)이고, 원본 위치는 UNIQUE 로 따로 잡는다(§4) — 1층 모든 행은
`conversation.source_file` + 순번 칸으로 원본 자리까지 거슬러 올라간다.

### 2.1 `conversation` — 방 1개 = 1행

| 칸 | 타입 | NULL | 뜻 |
|---|---|---|---|
| `conversation_id` | INTEGER | PK | 대체 키. 부여 순서 §4.5 |
| `channel` | TEXT | NOT NULL | `instagram` \| `facebook` — 파일이 놓인 메시지 루트로 정한다(§1 표 · D-15). CHECK |
| `box` | TEXT | NOT NULL | `inbox` \| `message_requests` \| `filtered_threads` — 파일이 놓인 보관함 폴더. CHECK |
| `thread_path` | TEXT | NOT NULL | 원본 `thread_path` 그대로(`<보관함>/<…>`). 방의 자연 키 §4.1 |
| `source_file` | TEXT | NOT NULL · UNIQUE | 원본 루트 기준 상대 경로(방 JSON 파일) |
| `title` | TEXT | NOT NULL | 원본 `title` |
| `owner_name` | TEXT | NOT NULL | `participants[]` 중 우리 계정의 `name`(§4.3) |
| `owner_participant_seq` | INTEGER | NOT NULL | 우리 계정이 `participants[]` 에서 놓인 자리(0부터) |
| `is_still_participant` | INTEGER | NOT NULL | 원본 `is_still_participant` |
| `is_pending` | INTEGER | NULL | 원본 `is_pending`. 키가 없으면 NULL |
| `joinable_mode` | INTEGER | NULL | 원본 `joinable_mode.mode`. 키가 없으면 NULL |
| `joinable_link` | TEXT | NULL | 원본 `joinable_mode.link`. 키가 없으면 NULL · 빈 문자열은 빈 문자열 그대로 |

UNIQUE(`channel`, `thread_path`).

### 2.2 `customer` — 방의 상대 참가자 1명 = 1행

| 칸 | 타입 | NULL | 뜻 |
|---|---|---|---|
| `customer_id` | INTEGER | PK | 대체 키 |
| `conversation_id` | INTEGER | NOT NULL · FK → `conversation` | 이 참가자가 나온 방 |
| `participant_seq` | INTEGER | NOT NULL | `participants[]` 에서 놓인 자리(0부터) |
| `name` | TEXT | NOT NULL | 원본 `participants[].name` |

UNIQUE(`conversation_id`, `participant_seq`). 행 단위가 「사람」이 아니라 「방의 상대」인 이유는 §4.2.

### 2.3 `message` — 메시지 1건 = 1행

| 칸 | 타입 | NULL | 뜻 |
|---|---|---|---|
| `message_id` | INTEGER | PK | 대체 키 |
| `conversation_id` | INTEGER | NOT NULL · FK → `conversation` | |
| `source_idx` | INTEGER | NOT NULL | 원본 `messages[]` 배열에서 놓인 자리(0부터 · 파일 순서) |
| `seq` | INTEGER | NOT NULL | 방 안 시간순 순번(1부터) §4.4 |
| `sender_name` | TEXT | NOT NULL | 원본 `sender_name` |
| `is_owner` | INTEGER | NOT NULL | 보낸 쪽이 그 채널 우리 계정이면 1(§4.3) |
| `customer_id` | INTEGER | NULL · FK → `customer` | 보낸 쪽이 상대면 그 행. `is_owner = 1` 이면 NULL |
| `sent_at_ms` | INTEGER | NOT NULL | 원본 `timestamp_ms` 그대로 |
| `sent_at` | TEXT | NOT NULL | `sent_at_ms` 를 UTC ISO 8601 로(§5.2) |
| `content` | TEXT | NULL | 원본 `content`. 키가 없으면 NULL |
| `call_duration` | INTEGER | NULL | 원본 `call_duration`. 키가 없으면 NULL |
| `is_geoblocked_for_viewer` | INTEGER | NOT NULL | 원본 그대로 |
| `is_unsent_image_by_messenger_kid_parent` | INTEGER | NOT NULL | 원본 그대로 |
| `share_link` | TEXT | NULL | 원본 `share.link` |
| `share_text` | TEXT | NULL | 원본 `share.share_text` |
| `share_original_content_owner` | TEXT | NULL | 원본 `share.original_content_owner` |
| `share_profile_share_name` | TEXT | NULL | 원본 `share.profile_share_name` |
| `share_profile_share_username` | TEXT | NULL | 원본 `share.profile_share_username` |

UNIQUE(`conversation_id`, `source_idx`) · UNIQUE(`conversation_id`, `seq`).

`share` 는 메시지마다 많아야 하나인 객체(배열이 아니다 · 실측 158건)라 `message` 의 칸 다섯으로 담는다.
`share` 키가 있는 메시지 = 다섯 칸 중 하나라도 NULL 이 아닌 행(빈 `share` 객체는 실측 0 · 나오면 G-10).

### 2.4 `attachment` — 첨부 항목 1개 = 1행

| 칸 | 타입 | NULL | 뜻 |
|---|---|---|---|
| `attachment_id` | INTEGER | PK | 대체 키 |
| `message_id` | INTEGER | NOT NULL · FK → `message` | |
| `kind` | TEXT | NOT NULL | 원본 키 이름 그대로 — `photos` \| `videos` \| `files` \| `gifs` \| `audio_files` \| `sticker`. CHECK |
| `item_idx` | INTEGER | NOT NULL | 그 배열에서 놓인 자리(0부터). `sticker` 는 배열이 아니라 객체라 늘 0 |
| `uri` | TEXT | NOT NULL | 원본 `uri` 그대로(원본 루트 기준 상대 경로) |
| `created_at_s` | INTEGER | NULL | 원본 `creation_timestamp`(초). 키가 없으면 NULL |
| `created_at` | TEXT | NULL | `created_at_s` 를 UTC ISO 8601 로(§5.2). 없으면 NULL |

UNIQUE(`message_id`, `kind`, `item_idx`).

`sticker`(FB 115건)는 메시지마다 많아야 하나인 객체이고 값은 파일 경로 `uri` 하나다 — 첨부 항목과 꼴이 같아
`attachment` 행으로 담는다. 다른 첨부와 달리 `uri` 가 방 폴더가 아니라 `stickers_used/` 를 가리키고,
같은 파일을 여러 메시지가 가리킨다(115행 · 파일 18개).

### 2.5 `reaction` — 반응 1개 = 1행 · D-12

| 칸 | 타입 | NULL | 뜻 |
|---|---|---|---|
| `reaction_id` | INTEGER | PK | 대체 키 |
| `message_id` | INTEGER | NOT NULL · FK → `message` | |
| `item_idx` | INTEGER | NOT NULL | `reactions[]` 에서 놓인 자리(0부터) |
| `actor` | TEXT | NOT NULL | 원본 `reactions[].actor` |
| `is_owner` | INTEGER | NOT NULL | `actor` 가 그 채널 우리 계정이면 1(§4.3) |
| `reaction` | TEXT | NOT NULL | 원본 `reactions[].reaction`(이모지) |

UNIQUE(`message_id`, `item_idx`).

## 3. 원본 키 대응표 — 실측 · 기준 「담을 칸 없는 원본 키 0」

방 JSON 1,916개에 나오는 키 경로는 **43개**다(객체 · 배열 자신 포함). IG 에 40개 · FB 에 36개가 나오고,
둘 다 나오는 것이 33개 · IG 에만 7개 · FB 에만 3개다. 전부 아래에 있다.
건수는 그 키가 나온 횟수(방 수 · 메시지 수 · 항목 수)다. `—` 는 그 채널에 그 키가 한 번도 없다는 뜻이다.

### 3.1 방 최상위 — 8개 + 안쪽 2개

| 원본 키 | IG | FB | 타입 | 처분 |
|---|---|---|---|---|
| `participants` | 511 | 1,405 | 배열 | 펼침 → 우리 계정은 `conversation.owner_name` · 상대는 `customer` 행 |
| `messages` | 511 | 1,405 | 배열 | 펼침 → `message` 행 |
| `title` | 511 | 1,405 | 문자열 | `conversation.title` |
| `is_still_participant` | 511 | 1,405 | 불리언 | `conversation.is_still_participant` |
| `thread_path` | 511 | 1,405 | 문자열 | `conversation.thread_path` |
| `magic_words` | 511 | 1,405 | 배열 | **버림** — 1,916방 전부 빈 배열이라 담을 값이 없다. 비어 있지 않으면 G-9 |
| `is_pending` | 16 | — | 불리언 | `conversation.is_pending` |
| `joinable_mode` | 16 | — | 객체 | 펼침 → 아래 두 칸 |
| `joinable_mode.mode` | 16 | — | 정수 | `conversation.joinable_mode` |
| `joinable_mode.link` | 16 | — | 문자열 | `conversation.joinable_link` |

### 3.2 `participants[]` — 1개

| 원본 키 | IG | FB | 타입 | 처분 |
|---|---|---|---|---|
| `participants[].name` | 1,021 | 2,810 | 문자열 | 우리 계정(IG 511 · FB 1,405) → `conversation.owner_name` · 상대(IG 510 · FB 1,405) → `customer.name`. 자리는 `owner_participant_seq` · `participant_seq` |

### 3.3 `messages[]` 바로 아래 — 14개

| 원본 키 | IG | FB | 타입 | 처분 |
|---|---|---|---|---|
| `sender_name` | 7,094 | 21,612 | 문자열 | `message.sender_name` (+ 파생 `is_owner` · `customer_id`) |
| `timestamp_ms` | 7,094 | 21,612 | 정수 | `message.sent_at_ms` (+ 파생 `sent_at`) |
| `is_geoblocked_for_viewer` | 7,094 | 21,612 | 불리언 | `message.is_geoblocked_for_viewer` |
| `is_unsent_image_by_messenger_kid_parent` | 7,094 | 21,612 | 불리언 | `message.is_unsent_image_by_messenger_kid_parent` |
| `content` | 6,374 | 19,126 | 문자열 | `message.content` |
| `photos` | 680 | 2,232 | 배열 | 펼침 → `attachment`(`kind = 'photos'`) |
| `reactions` | 123 | 236 | 배열 | 펼침 → `reaction` |
| `share` | 107 | 51 | 객체 | 펼침 → `message.share_*` |
| `files` | 5 | 112 | 배열 | 펼침 → `attachment`(`kind = 'files'`) |
| `call_duration` | 3 | 33 | 정수 | `message.call_duration` |
| `videos` | 2 | 1 | 배열 | 펼침 → `attachment`(`kind = 'videos'`) |
| `gifs` | 1 | 3 | 배열 | 펼침 → `attachment`(`kind = 'gifs'`) |
| `audio_files` | 1 | 3 | 배열 | 펼침 → `attachment`(`kind = 'audio_files'`) |
| `sticker` | — | 115 | 객체 | 펼침 → `attachment`(`kind = 'sticker'` · `item_idx = 0`) |

### 3.4 첨부 안쪽 — 11개

| 원본 키 | IG | FB | 타입 | 처분 |
|---|---|---|---|---|
| `photos[].uri` | 690 | 2,528 | 문자열 | `attachment.uri` |
| `photos[].creation_timestamp` | 689 | 2,528 | 정수(초) | `attachment.created_at_s` (+ 파생 `created_at`) |
| `videos[].uri` | 2 | 1 | 문자열 | `attachment.uri` |
| `videos[].creation_timestamp` | 1 | 1 | 정수(초) | `attachment.created_at_s` |
| `files[].uri` | 5 | 112 | 문자열 | `attachment.uri` |
| `files[].creation_timestamp` | 5 | 112 | 정수(초) | `attachment.created_at_s` |
| `gifs[].uri` | 1 | 3 | 문자열 | `attachment.uri` |
| `audio_files[].uri` | 1 | 3 | 문자열 | `attachment.uri` |
| `audio_files[].creation_timestamp` | 1 | 3 | 정수(초) | `attachment.created_at_s` |
| `sticker.uri` | — | 115 | 문자열 | `attachment.uri` |
| `sticker.ai_stickers` | — | 115 | 배열 | **버림** — 115건 전부 빈 배열이라 담을 값이 없다. 비어 있지 않으면 G-9 |

`gifs[]` · `sticker` 에는 `creation_timestamp` 키가 없다(실측 0).

### 3.5 `reactions[]` · `share` 안쪽 — 7개

| 원본 키 | IG | FB | 타입 | 처분 |
|---|---|---|---|---|
| `reactions[].actor` | 123 | 236 | 문자열 | `reaction.actor` (+ 파생 `is_owner`) |
| `reactions[].reaction` | 123 | 236 | 문자열 | `reaction.reaction` |
| `share.link` | 104 | 51 | 문자열 | `message.share_link` |
| `share.share_text` | 72 | 9 | 문자열 | `message.share_text` |
| `share.original_content_owner` | 50 | — | 문자열 | `message.share_original_content_owner` |
| `share.profile_share_name` | 4 | — | 문자열 | `message.share_profile_share_name` |
| `share.profile_share_username` | 4 | — | 문자열 | `message.share_profile_share_username` |

### 3.6 대조

| | IG | FB | 두 채널 합(겹침 제거) |
|---|---|---|---|
| 원본에서 센 키 경로 | 40 | 36 | **43** (§3.1 10 · §3.2 1 · §3.3 14 · §3.4 11 · §3.5 7) |
| 칸으로 간 값 키 | 29 | 24 | 30 |
| 펼쳐서 행 · 칸이 된 그릇(객체 · 배열) | 10 | 10 | 11 (`participants` · `messages` · `joinable_mode` · `photos` · `videos` · `files` · `gifs` · `audio_files` · `sticker` · `reactions` · `share`) |
| 버림 + 이유 | 1 | 2 | 2 (`magic_words` · `sticker.ai_stickers`) |
| **처분 안 된 키** | **0** | **0** | **0** |

30 + 11 + 2 = 43.

## 4. 키 규칙

### 4.1 방 찾기 · 방 키 — (`channel`, `thread_path`) · D-13 · D-15

**방 찾기** — 채널의 메시지 루트 아래 보관함 폴더마다:

| 꼴 | 방 | `source_file` | `thread_path` 대조(G-4) |
|---|---|---|---|
| 보관함 아래 **폴더** — 안에 `message_*.json` 이 정확히 1개 | 그 폴더 = 방 1개 | `<메시지 루트>/<보관함>/<폴더명>/message_1.json` | `thread_path` = `<보관함>/<폴더명>` |
| 보관함 **바로 아래 `*.json` 파일**(폴더 밖 · D-13) | 그 파일 = 방 1개 | `<메시지 루트>/<보관함>/<파일명>` | `thread_path` 의 첫 마디 = `<보관함>` (뒤 마디는 대조할 폴더가 없다) |

- `channel` 은 메시지 루트로, `box` 는 보관함 폴더로 정한다. 둘 다 파일이 놓인 자리에서 나오는 사실이다(D-15).
- 폴더 밖 JSON 실측(IG `message_requests` 1개): 방 꼴 그대로(§3 의 키만) · 참가자 2 · 메시지 1건(상대 발신 · `content` 만 · 첨부 0) ·
  `thread_path` 가 `message_requests/<…>` 인데 그 이름의 폴더는 없고 다른 방과 겹치지 않는다 · 파일명은 `thread_path` 뒤 마디와 다르다.
- 보관함 바로 아래 JSON 이 방 꼴이 아니면(`participants` · `messages` 가 없으면) G-1 · G-2 로 멈춘다.
- 보관함 바로 아래 것은 위 표의 두 꼴과 숨김 파일뿐이어야 한다. **폴더도 `*.json` 도 아닌 보통 파일**(숨김 아님)이 있으면 G-12 로 멈춘다(실측 0). 방 폴더 **안**의 다른 파일 · 폴더(첨부)는 보지 않는다(§1 Out).

**방 키** — 실측

| | IG | FB |
|---|---|---|
| 방 폴더의 `thread_path` = `<보관함>/<폴더명>` | 510 / 510 | 1,405 / 1,405 |
| `thread_path` 가 채널 안에서 서로 다름 | 511 / 511 | 1,405 / 1,405 |
| `thread_path` 마디 수 2 · 전부 ASCII | 511 | 1,405 |
| 폴더명이 `<핸들>_<숫자>` 꼴 / 숫자뿐 | 500 / 10 | 1,405 / 0 |

- 두 채널 사이에 겹치는 `thread_path` 는 **0**이다. 그래도 두 채널 다 `inbox/…` 로 시작하고 겹치지 말란 보장이 원본에 없어,
  방의 자연 키는 **(`channel`, `thread_path`)** 로 잡는다(UNIQUE).
- PK 는 대체 키 `conversation_id` 다 — `thread_path` 에는 계정 핸들이 들어 있어 다른 테이블로 번지지 않게 한다.
- 폴더명은 **쪼개지 않는다** — 뒤의 숫자가 무엇인지 원본에 설명이 없다.

### 4.2 고객 키 — 방의 상대 참가자 1명 = 1행 (실측 · D-01)

| | IG | FB |
|---|---|---|
| 참가자 2명인 방(우리 계정 + 상대 1) | 510 | 1,405 |
| 참가자 1명인 방(우리 계정뿐 · 메시지 전부 우리 발신) | 1 | 0 |
| `customer` 행 | 510 | 1,405 |
| 상대 이름 종류 | 501 | 1,391 |
| 같은 이름이 2방에 나옴 | 이름 1개 | 이름 6개 |
| 같은 이름이 9방에 나옴 | 이름 1개 | 이름 1개 |

- `participants[]` 에는 `name` 하나뿐이고 계정 id 가 없다(BASE). **이름이 같다고 같은 사람이라 할 근거가 원본에 없다** — 9방에 걸친 이름은 계정 고유 이름이 아니라 일반 표시 이름으로 보인다.
- 그래서 1층은 이름으로 묶지 않는다. 채널 안에서도, 채널 사이에서도(두 채널에 다 나오는 이름 26개) 묶지 않는다. 묶는 것은 판단이고 판단은 2층이다(D-01).
- `customer` = 방마다 우리 계정이 아닌 참가자 1명당 1행 → **1,915행**. 상대 없는 방 1개(IG)는 `customer` 행이 없다.
- 같은 이름은 `GROUP BY name` 으로 언제든 찾는다. 사람 단위로 묶는 표가 필요하면 2층에서 `customer_id` 를 가리켜 만든다.
- 방에 우리 계정 아닌 참가자가 2명 이상이면(단체방 · 실측 0) 참가자마다 1행이다 — UNIQUE 가 `(conversation_id, participant_seq)` 인 이유.

### 4.3 우리 계정 판별 — 채널별 규칙 (실측)

계정명을 코드 · 문서 · 인자 기본값에 적지 않는다. 적재 때 원본에서 구한다. **채널마다 따로** 구한다 — 두 채널의 우리 계정 이름은 서로 다르다(실측).

채널 하나에 대해:

1. **그 채널 모든 방의 `participants[]` 에 공통으로 들어 있는 이름**을 구한다.
2. 그 이름이 **정확히 1개**면 그 채널의 우리 계정이다. 0개 · 2개 이상이면 멈춘다(G-6).
3. 대조: 그 이름이 그 채널 `sender_name` 최다 발신자와 같아야 한다. 다르면 멈춘다(G-6).

| 실측 | IG | FB |
|---|---|---|
| 공통 이름 수 | 1 (511방 전부) | 1 (1,405방 전부) |
| 그 이름의 발신(채널 최다) | 4,617 | 15,363 |
| `participants[]` 안 자리 1번 / 0번 | 497 / 14 | 1,405 / 0 |
| `sender_name` 이 그 방 참가자가 아닌 메시지 | 0 | 0 |
| `actor` 가 그 방 참가자가 아닌 반응 | 0 | 0 |

- `conversation.owner_name` = 그 방 채널의 우리 계정 이름.
- `message.is_owner` = `sender_name` 이 그 방 채널의 우리 계정 이름과 같으면 1.
- `message.customer_id` = `is_owner = 0` 이면 같은 방 `customer` 중 `name` 이 `sender_name` 과 같은 행. 못 찾으면 멈춘다(G-7).
- `reaction.is_owner` 도 같은 규칙.
- 자리(`participants[]` 순서)로는 판별하지 않는다 — IG 에서 14방이 다르다.

### 4.4 메시지 순번 (실측)

| | IG | FB |
|---|---|---|
| 메시지 2건 이상인 방 — 전부 `timestamp_ms` 내림차순(같거나 작아짐) | 502 / 502 | 1,388 / 1,388 |
| 메시지 1건인 방 | 9 | 17 |
| 같은 방에서 `timestamp_ms` 가 겹쳐 남는 메시지(행 수 − 서로 다른 값 수) | 1 | 3 |

- 원본 `messages[]` 는 **최신이 먼저**다. 시각이 겹치는 메시지가 있어 시각만으로는 순서 · 키가 되지 않는다.
- `source_idx` = 배열 자리(0부터). 원본 위치이자 방 안 자연 키.
- `seq` = 방의 메시지 수 − `source_idx` (1부터 · 시간순). 시각이 같으면 배열에서 뒤에 있는 것이 먼저다.
- 내림차순이 깨진 방이 나오면 멈춘다(G-8) — `seq` 가 시간순이라는 전제가 깨진다.

### 4.5 대체 키 부여 순서 — 기본값

다시 적재해도 같은 id 가 나오게 한다(2층이 「근거 메시지 id」로 가리킨다 — D-05).

- `conversation_id` — (`channel`, `thread_path`) 오름차순(문자열 바이트 순)으로 1부터. `facebook` 이 `instagram` 보다 앞이다 →
  실측 기준 1 ~ 1,405 가 FB · 1,406 ~ 1,916 이 IG.
- `customer_id` — (`conversation_id`, `participant_seq`) 순으로 1부터.
- `message_id` — (`conversation_id`, `seq`) 순으로 1부터.
- `attachment_id` — (`message_id`, 종류 순서 `photos` · `videos` · `files` · `gifs` · `audio_files` · `sticker`, `item_idx`) 순으로 1부터.
- `reaction_id` — (`message_id`, `item_idx`) 순으로 1부터.

원본이 바뀌면(방이 늘면) id 도 바뀐다. 원본을 다시 받으면 2층도 다시 만든다.

## 5. 변환 규칙

### 5.1 이중 인코딩 복원 — D-04

- 규칙: 원본 JSON 의 **모든 문자열 값**에 `s.encode('latin1').decode('utf8')` 를 적용한다. 칸 · 채널을 고르지 않는다 — ASCII 문자열은 적용해도 그대로다.
- 원본 파일의 바이트는 1,916개 전부 ASCII 뿐이다(비 ASCII 는 `\u00XX` 이스케이프). `json` 으로 읽은 뒤 복원한다.
  이 전제가 깨진 파일(비 ASCII 바이트가 있음) · JSON 으로 읽히지 않는 파일 · 열 수 없는 파일은 G-13 으로 멈춘다 — 복원 규칙이 ASCII 이스케이프 꼴을 전제로 하기 때문이다.
- 복원에 실패하는 값이 하나라도 있으면 멈춘다(G-3). 조용히 원래 값을 넣지 않는다.
- DB 에는 복원된 값만 둔다. 원래 꼴은 `encode('utf8').decode('latin1')` 로 되돌아간다.

| 실측 | IG | FB |
|---|---|---|
| 문자열 값 | 16,706 | 49,652 |
| 복원 실패 | 0 | 0 |
| 복원 뒤 C1 제어 문자(U+0080 ~ U+009F) · U+FFFD 가 남은 값 | 0 | 0 |

비 ASCII 값이 실제로 있던 칸(복원이 일을 한 자리) — 「비 ASCII / 전체」:

| 원본 키 | IG | FB |
|---|---|---|
| `messages[].content` | 5,988 / 6,374 | 18,849 / 19,126 |
| `messages[].sender_name` | 1,002 / 7,094 | 17,742 / 21,612 |
| `participants[].name` | 214 / 1,021 | 1,931 / 2,810 |
| `title` | 214 / 511 | 1,405 / 1,405 |
| `reactions[].reaction` | 123 / 123 | 236 / 236 |
| `reactions[].actor` | 26 / 123 | 178 / 236 |
| `share.share_text` | 50 / 72 | 5 / 9 |
| `share.link` | 3 / 104 | 0 / 51 |
| `share.profile_share_name` | 2 / 4 | — |

`thread_path` · `uri` 전부(`sticker.uri` 포함) · `joinable_mode.link` · `share.original_content_owner` · `share.profile_share_username` 은 두 채널 다 전부 ASCII 다.

### 5.2 시각 — 기본값

- `timestamp_ms` 는 13자리 정수(밀리초 · Unix epoch) — 두 채널 28,706건 전부. `sent_at_ms` 에 **그대로** 둔다(원본 값).
- `sent_at` = UTC ISO 8601, 밀리초까지, `Z` 붙임 — `YYYY-MM-DDTHH:MM:SS.sssZ`. 문자열 정렬이 시간순이 된다.
- `creation_timestamp` 는 10자리 정수(**초**) — IG 696건 · FB 2,644건 전부. `created_at_s` 에 그대로 · `created_at` 은 `YYYY-MM-DDTHH:MM:SSZ`.
- 시간대는 UTC 하나만 저장한다. 한국 시각은 조회 때 만든다(`datetime(sent_at_ms / 1000, 'unixepoch', '+9 hours')`).
  영업시간 같은 해석은 2층이다.

| 범위(실측) | 가장 이른 | 가장 늦은 |
|---|---|---|
| IG | `2025-12-26T07:47:20.927Z` | `2026-06-26T06:16:02.338Z` |
| FB | `2026-01-09T18:19:11.724Z` | `2026-06-26T06:38:41.939Z` |

### 5.3 방당 파일 수 (실측)

- 방 폴더 1,915개(IG 510 · FB 1,405) 전부 `message_1.json` **하나뿐**이다. `message_2.json` 이상은 두 채널 어디에도 없다.
- 방 폴더에 `message_*.json` 이 없거나 2개 이상이면 멈춘다(G-5). 여러 파일을 잇는 규칙은 이 원본에서 확인할 수 없어 만들지 않는다.

### 5.4 멈추는 자리 — 조용히 통과하지 않는다

아래는 전부 **적재 중단 · 0 이 아닌 종료 코드 · DB 를 남기지 않음**이다. 실측에서는 두 채널 다 전부 0건이다.

| # | 조건 | 근거 |
|---|---|---|
| G-1 | §3 대응표에 없는 키가 나옴(어느 깊이든 · 어느 채널이든) | 「담을 칸 없는 원본 키 0」 |
| G-2 | 대응표와 타입이 다름(예: `share` 가 배열 · `sticker` 가 배열) | §3 타입 칸 |
| G-3 | 문자열 복원 실패 | §5.1 |
| G-4 | `thread_path` 대조 실패(§4.1 표) 또는 (`channel`, `thread_path`) 중복 | §4.1 |
| G-5 | 방 폴더에 `message_*.json` 이 없거나 2개 이상 | §5.3 |
| G-6 | 채널의 우리 계정이 1개로 정해지지 않음 · 그 채널 최다 발신자와 다름 | §4.3 |
| G-7 | `sender_name` · `actor` 가 그 방 참가자가 아님 | §4.3 |
| G-8 | `messages[]` 가 내림차순이 아님 | §4.4 |
| G-9 | `magic_words` · `sticker.ai_stickers` 가 비어 있지 않음 | §3 버림의 전제 |
| G-10 | `share` 가 빈 객체 | §2.3 |
| G-11 | 한 방 `participants[]` 안에 같은 이름이 둘 | §4.3 `customer_id` 찾기의 전제 |
| G-12 | 메시지 루트 아래에 §1 표에 없는 폴더가 있음(`stickers_used` 제외) · 메시지 루트 자체가 없음 · 보관함 바로 아래에 폴더도 `*.json` 도 아닌 보통 파일(숨김 아님)이 있음 | §1 · §4.1 |
| G-13 | 원본 방 JSON 파일 읽기 실패 — 열 수 없음(읽기 오류) · 비 ASCII 바이트가 있음 · JSON 으로 읽히지 않음 | §5.1 |

G-1 은 채널을 가리지 않는다 — 대응표의 키는 어느 채널에서 나와도 받는다(`—` 칸은 「이번 원본에 없었다」일 뿐 금지가 아니다).

멈출 때 내는 말에는 **채널 · 보관함 · 그 안에서 몇 번째 방인지 · 키 경로 · 규칙 번호**만 쓴다. 이름 · 본문 · 폴더명을 찍지 않는다(§6.3).
G-13 도 같다 — 파일을 못 읽어도 채널 · 보관함 · 몇 번째 방인지는 정해져 있으니 그것과 규칙 번호를 찍는다(키 경로는 없다). 번호 없는 「예기치 않은 오류」로 끝내지 않는다. G-12 의 보통 파일은 채널 · 보관함 · 규칙 번호만 찍는다(파일명은 찍지 않는다).

## 6. 실행 인터페이스 — D-09 · D-10

### 6.1 위치 · 인자

| 스크립트 | 일 |
|---|---|
| `para/projects/summer-star/consult-analysis/scripts/load_layer1.py` | 원본 → SQLite 적재(두 채널을 한 번에) |
| `para/projects/summer-star/consult-analysis/scripts/verify_layer1.py` | 원본을 **따로 다시 세어** DB · §7 과 대조 |

| 인자 | 뜻 | 기본값 |
|---|---|---|
| `--source` | 원본 루트(두 채널 폴더가 바로 아래 있는 폴더) | 없음 — 필수 |
| `--db` | SQLite 파일 경로 | 없음 — 필수 |

- 기본 경로를 코드에 박지 않는다. 쓰는 값은 `--source reference/2026-11-16-linky-data` ·
  `--db para/projects/summer-star/consult-analysis/data/layer1.sqlite`(둘 다 gitignore · D-09).
- 채널을 고르는 인자는 두지 않는다 — 두 채널이 늘 한 DB 에 같이 들어간다(D-14). 한쪽 메시지 루트가 없으면 G-12.
- **표준 라이브러리만**(`json` · `sqlite3` · `argparse` · `pathlib` 등). 외부 패키지 0.
- 실행은 `python3 -I`(원본 폴더의 코드가 끼어들지 않게).
- 원본 폴더에는 아무것도 쓰지 않는다(읽기만).

### 6.2 다시 돌릴 때

- **DB 를 새로 만든다.** 있던 파일에 덧붙이지 않는다.
- `<db>.tmp` 에 만들고 전부 성공하면 `<db>` 로 바꿔치기한다. 중간에 멈추면 `.tmp` 를 지우고 있던 `<db>` 는 건드리지 않는다.
- 적재는 한 트랜잭션이다. 같은 원본이면 몇 번을 돌려도 같은 행 · 같은 id 다(§4.5).

### 6.3 출력 — 고객 정보 0

- 표준 출력 · 표준 오류 · 로그에는 **건수와 규칙 번호만** 쓴다. 이름 · 계정명 · 본문 · 폴더명 · `thread_path` · `uri` 를 찍지 않는다.
- `load_layer1.py` 는 끝에 채널별 · 테이블별 행 수를 찍는다.
- `verify_layer1.py` 는 §7 의 줄마다 · 칸(IG · FB · 합)마다 「기준 · 원본 재집계 · DB」 세 값과 일치 여부를 찍고, 전부 같으면 종료 코드 0 · 하나라도 다르면 1.
- 스크립트 · 주석 · 테스트에 계정명 · 고객 이름 · 본문 예시를 넣지 않는다(레포는 PUBLIC).

## 7. 건수 기준 — D-03 · 실측

적재 뒤 **모든 줄 · 모든 칸이 같아야 끝**이다. 값은 2026-11-16 planner 가 원본 1,916개에서 센 것이다.
`—` 는 합을 내지 않는 줄이다(채널별로만 대조).

### 7.1 `conversation` · `customer`

| # | 무엇 | IG | FB | 합 |
|---|---|---|---|---|
| C-01 | `conversation` 행 | 511 | 1,405 | 1,916 |
| C-02 | `box = 'inbox'` | 495 | 1,404 | 1,899 |
| C-03 | `box = 'message_requests'` | 16 | 0 | 16 |
| C-04 | `box = 'filtered_threads'` | 0 | 1 | 1 |
| C-05 | `source_file` 이 폴더 밖 JSON 인 방(D-13) | 1 | 0 | 1 |
| C-06 | `is_still_participant = 1` | 511 | 0 | 511 |
| C-07 | `is_pending` NULL 아님 (전부 1 · 전부 `message_requests`) | 16 | 0 | 16 |
| C-08 | `joinable_mode` NULL 아님 (전부 값 1 · `joinable_link` 전부 빈 문자열 · `inbox` 15 · `message_requests` 1) | 16 | 0 | 16 |
| C-09 | `owner_name` 값 종류 | 1 | 1 | 2 |
| C-10 | `owner_participant_seq` = 1 / = 0 | 497 / 14 | 1,405 / 0 | 1,902 / 14 |
| C-11 | `customer` 행 | 510 | 1,405 | 1,915 |
| C-12 | `customer.name` 값 종류 | 501 | 1,391 | — |
| C-13 | `customer` 행이 없는 `conversation` | 1 | 0 | 1 |
| C-14 | `title` 이 그 방 `customer.name` 과 같은 방 | 510 | 0 | 510 |
| C-15 | (`channel`, `thread_path`) 값 종류 / `thread_path` 만의 값 종류 | 511 / 511 | 1,405 / 1,405 | 1,916 / 1,916 |

### 7.2 `message`

| # | 무엇 | IG | FB | 합 |
|---|---|---|---|---|
| M-01 | `message` 행 | 7,094 | 21,612 | 28,706 |
| M-02 | `inbox` 방의 메시지 | 7,067 | 21,574 | 28,641 |
| M-03 | `message_requests` 방 / `filtered_threads` 방의 메시지 | 27 / 0 | 0 / 38 | 27 / 38 |
| M-04 | `is_owner = 1` | 4,617 | 15,363 | 19,980 |
| M-05 | `is_owner = 0` (전부 `customer_id` NULL 아님) | 2,477 | 6,249 | 8,726 |
| M-06 | `content` NULL 아님 | 6,374 | 19,126 | 25,500 |
| M-07 | `call_duration` NULL 아님 / 그중 0 이 아닌 것 | 3 / 0 | 33 / 1 | 36 / 1 |
| M-08 | `is_geoblocked_for_viewer = 1` | 0 | 0 | 0 |
| M-09 | `is_unsent_image_by_messenger_kid_parent = 1` | 0 | 0 | 0 |
| M-10 | `share_*` 다섯 칸 중 하나라도 NULL 아님 | 107 | 51 | 158 |
| M-11 | `share_link` / `share_text` NULL 아님 | 104 / 72 | 51 / 9 | 155 / 81 |
| M-12 | `share_original_content_owner` / `share_profile_share_name` / `share_profile_share_username` NULL 아님 | 50 / 4 / 4 | 0 / 0 / 0 | 50 / 4 / 4 |
| M-13 | `content` · `call_duration` · `share_*` 전부 NULL 이고 첨부 · 반응도 없는 행 | 22 | 20 | 42 |
| M-14 | 방당 메시지 수 최소 / 중앙값 / 최대 | 1 / 7 / 117 | 1 / 9 / 372 | — |
| M-15 | 같은 방에서 `sent_at_ms` 가 겹쳐 남는 행(행 수 − 서로 다른 (`conversation_id`, `sent_at_ms`) 수) | 1 | 3 | 4 |
| M-16 | `sent_at` 최소 | `2025-12-26T07:47:20.927Z` | `2026-01-09T18:19:11.724Z` | — |
| M-17 | `sent_at` 최대 | `2026-06-26T06:16:02.338Z` | `2026-06-26T06:38:41.939Z` | — |
| M-18 | 메시지가 전부 우리 발신인 방 / 전부 상대 발신인 방 | 3 / 17 | 17 / 10 | 20 / 27 |

### 7.3 `attachment`

행 수:

| # | 종류(`kind`) | IG | FB | 합 |
|---|---|---|---|---|
| A-01 | `photos` | 690 | 2,528 | 3,218 |
| A-02 | `videos` | 2 | 1 | 3 |
| A-03 | `files` | 5 | 112 | 117 |
| A-04 | `gifs` | 1 | 3 | 4 |
| A-05 | `audio_files` | 1 | 3 | 4 |
| A-06 | `sticker` | 0 | 115 | 115 |
| A-07 | **합** | **699** | **2,762** | **3,461** |

그 종류가 있는 메시지 수:

| # | 종류 | IG | FB | 합 |
|---|---|---|---|---|
| A-08 | `photos` | 680 | 2,232 | 2,912 |
| A-09 | `videos` / `files` / `gifs` / `audio_files` / `sticker` | 2 / 5 / 1 / 1 / 0 | 1 / 112 / 3 / 3 / 115 | 3 / 117 / 4 / 4 / 115 |
| A-10 | 첨부가 하나라도 있는 메시지 | 689 | 2,466 | 3,155 |

그 밖:

| # | 무엇 | IG | FB | 합 |
|---|---|---|---|---|
| A-11 | `created_at_s` NULL — `photos` / `videos` / `gifs` / `sticker` (`files` · `audio_files` 는 0) | 1 / 1 / 1 / 0 | 0 / 0 / 3 / 115 | 1 / 1 / 4 / 115 |
| A-12 | `created_at_s` NULL 합 | 3 | 118 | 121 |
| A-13 | `sticker` 가 아닌 행의 `uri` 값 종류(= 행 수 · 겹침 0) | 699 | 2,647 | 3,346 |
| A-14 | `sticker` 행의 `uri` 값 종류 | 0 | 18 | 18 |
| A-15 | `uri` 가 가리키는 파일이 원본 폴더에 있는 행 | 699 | 2,762 | 3,461 |
| A-16 | `sticker` 가 아닌 행 중 `uri` 가 자기 방 폴더(`<source_file 의 폴더>/`) 아래인 행 | 699 | 2,647 | 3,346 |
| A-17 | `sticker` 행 중 `uri` 가 `<FB 메시지 루트>/stickers_used/` 아래인 행 | 0 | 115 | 115 |
| A-18 | 한 메시지의 `photos` 개수 최대 | 3 | 12 | — |
| A-19 | `photos` 가 1개 / 2개 / 3개 이상인 메시지 | 671 / 8 / 1 | 2,045 / 124 / 63 | 2,716 / 132 / 64 |
| A-20 | 보관함별 행 — `inbox` | 692 | 2,725 | 3,417 |
| A-21 | 보관함별 행 — `message_requests` / `filtered_threads` | 7 / 0 | 0 / 37 | 7 / 37 |

A-15 는 파일이 있는지만 본다. 열지 않는다(DEC OQ-003).

### 7.4 `reaction` — D-12

| # | 무엇 | IG | FB | 합 |
|---|---|---|---|---|
| R-01 | `reaction` 행 | 123 | 236 | 359 |
| R-02 | 반응이 있는 메시지(메시지당 전부 1개) | 123 | 236 | 359 |
| R-03 | `is_owner = 1` | 64 | 130 | 194 |
| R-04 | `is_owner = 0` | 59 | 106 | 165 |
| R-05 | `reaction` 값 종류 | 8 | 12 | — |

### 7.5 복원

| # | 무엇 | IG | FB | 합 |
|---|---|---|---|---|
| E-01 | 모든 TEXT 칸에서 C1 제어 문자(U+0080 ~ U+009F) · U+FFFD 가 든 값 | 0 | 0 | 0 |
| E-02 | `content` 에 비 ASCII 가 든 행 | 5,988 | 18,849 | 24,837 |
| E-03 | 원본 재집계의 문자열 값 수 | 16,706 | 49,652 | 66,358 |
| E-04 | 복원 실패 | 0 | 0 | 0 |

## 8. 2층에서 붙는 자리 — D-05

2층(언어 · 국적 · 문의 유형 · 예약 단계)은 **따로 만든 테이블**이 `message_id` · `conversation_id` · `customer_id` 를 FK 로 가리켜 붙는다 — 1층 테이블에는 칸을 더하지 않는다. 설계는 이 문서 범위가 아니다.

## 9. 열린 것 · 주의

### 9.1 닫힌 것

| ID | 무엇 | 답 | 근거 |
|---|---|---|---|
| OQ-101 | `reactions[]` 를 어디에 담나 | **A** — 다섯 번째 테이블 `reaction`(§2.5) | D-12 |
| OQ-102 | 폴더 밖 대화 JSON 1개를 싣나 | **A** — 싣는다(§4.1) | D-13 |
| OQ-103 | 페이스북 메신저 대화를 1층에 넣나 | **B** — 같은 1층에 넣는다(§1) · 채널 칸(§2.1) | D-14 · D-15 |

### 9.2 열린 것

없다. 0.2.0 에서 새로 나온 자리(`sticker` · `sticker.ai_stickers` · `filtered_threads` · 채널별 우리 계정)는
전부 원본 실측에서 처분이 정해졌다(§2.4 · §3.4 · §1 · §4.3).

### 9.3 BASE-001 과 다른 자리 — 고치지 않았다(범위 밖) · 보고만

| BASE-001 | 실측 |
|---|---|
| `message_requests/` 16 → 대화 JSON 510개 | IG 대화 JSON 은 **511개**다 — 방 폴더 510(`inbox` 495 · `message_requests` 15) + 폴더 밖 1(D-13) |
| 메시지 7,093건 · 우리 계정 발신 4,617 | 폴더 밖 1건을 더해 IG 7,094(우리 발신은 그대로 4,617) · 두 채널 합 28,706(우리 발신 19,980) |
| 기간 2025-12-26 ~ 2026-06-26 | IG 는 맞다. FB 는 2026-01-09 ~ 2026-06-26 |
| 방당 메시지 중앙값 7 · 최대 117 | IG 는 맞다. FB 는 중앙값 9 · 최대 372 |
| 「509방이 1:1 · 1방은 상대 없음 · 2명이 방 2개에 걸쳐 있다」 | IG 510방이 1:1 · 1방 상대 없음. 같은 이름이 2방에 나오는 것 1개 · **9방**에 나오는 것 1개(§4.2). FB 는 1,405방 전부 1:1 |
| `messages[]` 키 목록 · `photos` 680 | IG 기준이고 680 은 메시지 수다(항목 690). FB 에는 `sticker` 가 더 있다(§3.3) |

### 9.4 주의

- `customer` 는 「사람」이 아니라 「방의 상대」다(§4.2). 「고객 수 1,915」를 사람 수로 읽지 않는다. 같은 사람이 두 채널로 들어왔는지도 1층은 모른다.
- `thread_path` · `source_file` · `uri` 에는 계정 핸들이 들어 있다. DB 안에서만 쓰고 문서 · 출력으로 옮기지 않는다.
- FB 방은 1,405개 전부 `is_still_participant` 가 거짓이고 `title` 이 상대 이름과 같지 않다(C-06 · C-14). 원본 값 그대로 담는다 — 뜻은 해석하지 않는다.
- `sticker` 행은 `uri` 가 겹친다(115행 · 18종). `uri` 에 UNIQUE 를 걸지 않는다.
