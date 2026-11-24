# planner-fix-5 결과 보고 — 사진을 DAY 에도 저장 (결정 C22 · C14 뒤집힘)

## 상태: done

워크트리 `mediness-mediness/day-chart-photo-spec` · `b2005927` 위 · 미커밋. 바꾼 파일 = `products/day/20-spec/spec-000-data-model.md` · `20-spec/spec-002-procedure-board.md` · `20-spec.md` · `10-decision.md` · `log.md`.

## 1. SPEC-000 — 새 테이블 `visit_photo`(이름 제안 · **migration 필요**)

| 자리 | 반영 |
|---|---|
| 머리글(개정 2026-11-24 새 줄) · frontmatter `sources` 첫 줄 | C22 요약 · migration 필요 |
| §3 02 `external_ref` 「`entity_type` 값 추가」 | `visit_photo` — 살아 있는 행 = KOS 반영됨 · 없음 = 「KOS 미반영」 · KOS 삭제 성공 시 소프트 삭제 |
| §3 07 `id_photo` 뒤 :1192 `#### visit_photo` | 칸 `id` · `visit_id` · `customer_id` · `category`(before · after) · `file_key · bytes · sha256`(키 `before-after/{병원 id}/{32 hex}.{확장자}` · 5MB) · `content_type` · `created_by_staff_id` · `created_at · updated_at` · `deleted_at` / 인덱스 (`visit_id`, `created_at`) 살아 있는 행 · (`file_key`) / KOS 상태 칸 없음(external_ref) · outbox 안 씀 · 코드 테이블 없음(C13) |

- 선례: `ChatAttachment`(`file_key` · `bytes` · `sha256` · `file_key` 인덱스) · `IdPhoto`(`customer_id` · `visit_id` · `created_by_staff_id` · 「kos_status 칸 두지 않음」) · 병원 = 부모 `visit`(§2 「병원을 아는 방법」).

## 2. SPEC-002 사진 절 (C22 · C22-기본값)

| 자리(줄) | 반영 |
|---|---|
| :45 개정 ㉘ 머리글 | ⑦ 「DAY 저장 없음」 ~~취소선~~ · 「보충 5」 ⑯ 요약 |
| 1차 범위 Out Of Scope | 「DAY 사진 사본 · 보관(C14)」 ~~취소선~~ |
| 화면 구성 | **E65** 「KOS 미반영」 표시 · [다시 시도] 더함 |
| U-16 | 옛 bullet 6개 ~~취소선~~ + 날짜 · 사유 → 새 bullet(목록 = DAY 행만 · KOS 웹 사진 안 보임 · 올리기 = 저장소 + DAY 행 뒤 KOS · 5MB · 삭제 = DAY 소프트 + KOS · 썸네일 · 원본 = DAY 저장소 · 「KOS 미반영」 + [다시 시도] · 실패 갈래) · 권한 · 범위(앱 밖) 그대로 |
| §3 API :643 ~ :648 | 옛 사진 4행 ~~취소선~~ → 새 5행: 목록 · 올리기 · 삭제(`photo_id` = DAY 행 id) · **파일 `GET …/photos/{photo_id}/file`**(썸네일 · 원본 같은 경로) · **다시 시도 `POST …/photos/{photo_id}/kos-retry`**(이름 제안) · 「사진 id」 예외 · 「사진은 KOS 를 기다린다」 · 「썸네일 서버가 받아 주는 이유」 ~~취소선~~ → 새 문장 |
| 매트릭스 | 옛 6줄 ~~취소선~~ → 새 줄: 404 · 413 `photo_too_large` · 400 형식 · 409 / 503 `photo_disabled`(채팅 선례) · 401 토큰 없음(아무것도 안 남김) · KOS 쪽 실패 200(DAY 남김 · 미반영) · KOS 401(DAY 남김 · 세션 끝) · KOS 삭제 실패 200 · 다시 시도 이미 반영 200 |
| 토스트 표 | 미반영 · 다시 시도 글자 비움(OQ-88) · `photo_too_large` · `photo_disabled` = DAY-SPEC-004 글자(웹에 쓸지 OQ-88) |
| §3 「KOS 사진」 :1102 | 목록 경로 = 화면 목록에 안 씀(등록 뒤 · 다시 시도 때 id 찾기만) · 썸네일 · 원본 행 ~~취소선~~ · `fileName` uuid 자리 = DAY 행 id · PUT 바이트 = 다시 시도 때 저장소 · 삭제 행 ~~옛 순서~~ → DAY 커밋 뒤 · external_ref id · 「동기화 없음」 ~~취소선~~ → DAY 원장 |
| :1205 규칙 39 | 옛 판 전체 ~~취소선~~ → 새 판 ① ~ ⑩(목록 · 올리기 ⓐ ~ ⓔ · 다시 시도 · fileName · 삭제 · 썸네일 · 토큰 · 큐 안 씀 · transaction 밖 · 기록 · 앱 밖) |
| §4 결정 짝 표 :1288 · 차이 표 | C14 행 ~~취소선~~ · C22 행 더함 · 「시술전후사진」 행 「DAY 저장 없음」 ~~취소선~~ |
| DB 절 | 「DAY 테이블 · 칸이 없다」 ~~취소선~~ → `visit_photo` · migration 필요 · 저장소 키 규칙에 `before-after` 더함(지금 코드는 `chat` 만) · `photo.kos_retry` |
| OQ-87 ⓒ · OQ-92 | 서명 주소 문장 ~~취소선~~ · 목록 · 그림은 KOS 안 부름 |

**정한 기본값(근거)**
- 올리기 순서 = 검사(토큰 포함 — 아무것도 남기지 않음) → 저장소 → DAY 행 + event 커밋 → transaction 밖 KOS → `external_ref` 커밋(C22-기본값 ①). DAY 행 커밋 실패 = 쓴 파일 지움(채팅 「넘으면 쓰던 파일 지움」 선례).
- 다시 시도 = 먼저 KOS 목록에서 그 `fileName` 을 찾고 있으면 `external_ref` 만(등록됐는데 id 만 못 받은 경우 중복 막음). `fileName` uuid 자리 = DAY 행 id → 새 칸 없이 같은 이름(cc kos-retry 선례 + 중복 방지).
- 삭제 KOS 실패 = DAY 삭제 그대로 · `external_ref` 살아 남음 = 「KOS 삭제 안 됨」 → 같은 다시 시도 API 가 KOS 삭제만 다시(C22-기본값 ④ · 표시 자리 OQ-94).
- 저장소 파일은 삭제 때 지우지 않음(소프트 삭제 · 보관 OQ-95).
- 썸네일 = 원본과 같은 바이트(서버 축소 없음 · OQ-87).

## 3. 그 밖

- `20-spec.md` 시술 현황 In Scope · Out Of Scope 의 「DAY 저장 없음 · DAY 사진 사본」 ~~취소선~~.
- `10-decision.md` 앞 줄(「ESC-001 대상을 넓히지 않는다」) ~~취소선~~ → DAY 가 고객 사진을 보관하게 됨 · ESC-001 과 같은 성격 · board 는 바꾸지 않고 OQ-95 참조만(범위를 넓힐지는 결정권자 몫).
- `log.md` spec-change 1행.
- 새 OQ: **OQ-93**(KOS 웹에서 올린 사진 — 기본값 안 보임) · **OQ-94**(KOS 삭제 실패 · 미반영 표시 자리) · **OQ-95**(사진 보관 · ESC-001 범위).
- 그대로 둔 것: 「서버에서만 쓰기 · 앱 범위 밖」(C15) · 쓰기 큐 안 씀 · KOS 내부 경로 · 직원 토큰 · KOS 호출 동안 transaction 없음.

## 검증

`python3 scripts/lint-pipeline.py --strict` → **0 error · 263 warning** · `products/day/` 0건(전부 타 제품 — 무관). 바꾼 표 열 수 점검 통과.

## 미결 · 주의

- 코드: 저장소 키 규칙(`adapters/storage/contracts.py` `PURPOSE = "chat"` · 확장자 `jpg|mp4`)에 `before-after` · 사진 형식을 더해야 한다 — 형식은 OQ-86(채팅 = JPEG 만 · KOS HAR = png).
- Delivery request(`delivery/request-be-photo.json` · `request-fe.json`)의 계약 K4 · A5(「DAY 저장 0」)는 이번 결정과 어긋난다 — 다시 발행 때 고쳐야 한다(이번 범위 밖 · 손대지 않음).
