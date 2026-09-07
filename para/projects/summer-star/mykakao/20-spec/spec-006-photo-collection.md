---
type: spec
id: MK-SPEC-006
title: "사진 수집 — URL 다운로드·로컬 저장·미디어 서빙·<img> 렌더"
status: draft
product: mykakao
created_at: 2026-09-04
updated_at: 2026-09-04
tags: [product/mykakao, platform/windows, doc/spec, status/draft]
links:
  baselines: ["[[baseline-007-photo-collection]]"]
  decisions: ["[[decision-006-photo-collection]]"]
  specs: ["[[spec-005-settings-collection-queue]]"]
  works: []
  releases: []
  related: ["[[baseline-008-cng-old-photo-decrypt]]"]
---

# 사진 수집 — URL 다운로드·로컬 저장·미디어 서빙·<img> 렌더

실시간 수집 파이프에 사진 처리를 얹는다: 사진 메시지 → talkmedia URL 조회 → 다운로드 → 로컬 미디어 저장 → /api/media 서빙 → 탭2 <img>. win_app 확장(SPEC-005 위). 오래된(만료) 사진 = 유실 표시.

> 구현 = Rust `win_app/`. 새 crate 는 HTTP 다운로드에 필요하면 보고 후. 커밋·PR 코디.

## Context
- 관련: [[decision-006-photo-collection]] / [[baseline-007-photo-collection]].
- In: 사진 수집(URL 다운로드·저장) / 미디어 서빙 / 탭2 렌더 / 유실 placeholder.
- Out: .cng 복호(오래된 사진, [[baseline-008-cng-old-photo-decrypt]]) / 동영상·파일.

## 수집 파이프 (SPEC-005 델타에 추가)
- 델타 수집(import_room / 폴링)에서 **사진 타입 메시지**를 식별(type 코드).
- 그 logId 로 `talkmedia.edb` 조회: chatMsgTokenJunction(logId→token) → tokenInfo(token→url,fileSize,checkSum). talkmedia 는 memory harvest 키로 복호(기존).
- **URL 다운로드**: 200 이면 바이트 확보 → checkSum(SHA1)·fileSize 검증 → 로컬 미디어 스토어 저장. 미디어 상태=`saved`.
- **만료(410/404)**: 저장 못 함 → 상태=`lost`(유실). 재시도 안 함(.cng 범위 밖).
- talkmedia 조회 실패/비사진 = 무시.

## Data Contract
- 미디어 스토어: `%LOCALAPPDATA%\mykakao\media\<chatId>\<logId>.<ext>` (또는 DB blob). 우리 SQLite 에 `media(chat_id, log_id, mime, status[saved|lost|pending], bytes_or_path)` — 구현 택1.
- message 행에 사진 여부 표식(msg_type 로 판별 or media 조인).

## API / 렌더
- `GET /api/media/<chatId>/<logId>` → 저장 이미지 바이트(Content-Type mime). 없으면 404.
- `/api/messages` 응답: 사진 메시지는 `kind:"photo"` + `media_status`(saved|lost|pending) 표식(계약 확장).
- 탭2 대화창: 사진 메시지 →
  - saved → `<img src="/api/media/<chatId>/<logId>">` (지연로드, max-width).
  - pending → 로딩 표시.
  - lost → "유실됨"(수집 전 만료) placeholder + 아이콘.

## Validation (개수/유무만, 이미지·URL·토큰 원값 미출력)
- 최근 사진 있는 방 수집 → talkmedia URL 200 다운로드 → 로컬 저장 → checkSum 일치 → /api/media 200 image. 탭2 <img> 표시(육안).
- 만료 사진 → status=lost, "유실됨" 표시.
- 안전: URL/토큰/checkSum 원값 로그·커밋 비노출(host·status·크기·일치여부만). 원본 읽기만·카톡 무변조·SAC 미변경. 이미지는 로컬 저장·외부 전송 0.

## Work Handoff
- **WORK-008**: win_app — 사진 수집(talkmedia 조회+다운로드+저장) · media 스토어 · /api/media 서빙 · /api/messages 사진 표식 · 탭2 <img>/유실 렌더. allowed_paths `win_app/`. 커밋·PR 코디.

## Open Questions
| ID | Q | Next |
|---|---|---|
| OQ-1 | URL 유효기간 | 운영 관찰 |
| OQ-2 | 저장=파일 vs DB blob | 구현 |
