---
type: baseline
id: BASE-001
title: "인스타그램 상담 DM 내보내기 — 원본 실측과 분석 요구"
status: raw
product: consult-analysis
source:
  type: conversation
  ref: "사용자 대화 2026-11-16 · reference/2026-11-16-linky-data 실측"
links:
  baselines: []
  decisions:
    - "[[decision-001-two-layers|DEC-001]]"
  specs: []
  works: []
---

# BASE-001 인스타그램 상담 DM 내보내기

## 요구 (사용자)

- 상담 데이터를 분석하고 싶다. 분석 전에 고객 · 대화 · 예약 성공 같은 테이블로 정규화한다.
- 예약 성공 = 상담사가 보낸 예약표를 **고객이 채워 회신한 것**. 회신을 받으면 병원에 전달했다.
- DB 는 로컬 SQLite. 파서와 적재 스크립트는 이 프로젝트에 스크립트로 둔다.
- 원본은 용량이 커서 git 에서 뺀다.

## 원본 실측 (2026-11-16, 코디네이터)

원본: Meta 「Download your information」 내보내기. 클리닉 계정 한 곳의 DM.

| 항목 | 값 |
|---|---|
| 크기 · 파일 | 1.8G · 5,288개 (png 2,342 · json 1,920 · jpg 892 · pdf 114 · mp4 7 · gif 4 · heic 3 · webp 1) |
| 대화방 | `your_instagram_activity/messages/inbox/` 495 · `message_requests/` 16 → 대화 JSON 510개 |
| 메시지 | 7,093건 · 우리 계정 발신 4,617 |
| 기간 | 2025-12-26 ~ 2026-06-26 |
| 방당 메시지 | 중앙값 7 · 최대 117 |
| 페이스북 쪽 | `this_profile's_activity_across_facebook/messages/` — ~~대화 없음~~ → **대화 JSON 1,405개(`inbox` 1,404 · `filtered_threads` 1) · 메시지 21,612건** (2026-11-16 정정 · 코디가 파일 목록 앞부분만 보고 놓침 · SPEC-001 §9.2). 그 밖에 메신저 설정 3개 · 스티커 이미지 |

### 파일 구조

- 방 JSON 최상위 키: `participants`(510) · `messages`(510) · `title` · `is_still_participant` · `thread_path` · `magic_words` · `is_pending`(15) · `joinable_mode`(15)
- `participants[]` 키는 **`name` 하나뿐**. 국적 · 지역 · 연락처 필드 없음
- 509방이 1:1(고객 1명 + 우리 계정), 1방은 상대 없음. 2명이 방 2개에 걸쳐 있다
- `messages[]` 키: `sender_name` · `timestamp_ms` · `is_geoblocked_for_viewer` · `is_unsent_image_by_messenger_kid_parent`(전부) · `content` 6,373 · `photos` 680 · `reactions` 123 · `share` 107 · `files` 5 · `call_duration` 3 · `videos` 2 · `gifs` 1 · `audio_files` 1
- 문자열은 Meta 내보내기 특유의 이중 인코딩(UTF-8 바이트를 latin-1 로 읽은 꼴)이다. `s.encode('latin1').decode('utf8')` 로 복원된다

### 예약표 (키워드 대략치)

| 상황 | 방 수 |
|---|---|
| 영업시간 외 자동응답 — 본문에 **빈 예약표**가 들어 있다 | 150 |
| 상담사가 예약표를 보냄(자동응답 제외) | 56 |
| 고객 메시지에 예약표 칸(姓名 · 國籍 등)이 들어 있음 | 40 |
| 방의 마지막 메시지가 예약표 | 11 |

예약표 칸: 예약 날짜 · 시간 / 여권 영문 이름 / 생년월일 / **國籍** / 성별 / 희망 시술 · 예산 / 통역 필요 여부 / 원장 상담 필요 여부.
문구가 판마다 조금씩 다르다(「★ 預約資訊」 · 「📝 預約表格」 · 「預約表格 ★ 來院日期時間」).

> 정정(2026-11-16): `message_requests/` 는 방 폴더 15 + 폴더 밖 대화 JSON 1 · 같은 이름이 2방에 1개 · 9방에 1개 · 사진은 메시지 680건에 항목 690개 — 상세는 SPEC-001 §9.2.

## 아직 모르는 것

- 상담사 확정 안내 문구의 패턴(있는지부터)
- 고객 메시지 언어 분포
- 예약표 판(版)이 몇 가지인지 전수
