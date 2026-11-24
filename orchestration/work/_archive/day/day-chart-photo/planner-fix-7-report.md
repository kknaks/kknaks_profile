# planner-fix-7 결과 보고 — 문서 검수 review-doc-4 W1 ~ W9

## 상태: done

워크트리 `mediness-mediness/day-chart-photo-spec` · 미커밋 변경 위 · 미커밋. 바꾼 파일 = `products/day/20-spec/spec-002-procedure-board.md` · `20-spec/spec-000-data-model.md` · `20-spec/spec-004-internal-chat.md` · `log.md`.

| W | 자리(파일:줄) | 반영 |
|---|---|---|
| W1 | spec-002 :1362 OQ-92 | 행 끝 `|` 밖 보충을 기본값 칸 안으로(표 4칸 → 3칸) · 「토큰이 없으면 사진 보기도 세션 만료」 ~~취소선~~ · 토큰 쓰는 곳 = 올리기 · 삭제 · 다시 시도(⑦) + **가져오기 작업의 KOS 읽기(⑪ ⓓ)** · 목록 · 파일 열기는 토큰 검사 안 함 |
| W2 | spec-002 :1215 규칙 39 ⑪ ⓑ · :1366 OQ-96 ⓔ | 「기본값(코디)」 — **지운 「KOS 미반영」 행도 센다** → 그 행에 `external_ref` → 「KOS 삭제 안 됨」 → ③ 으로 KOS 삭제 · 지운 사진이 `source = kos` 로 되살아나지 않음 |
| W3 | 규칙 39 ③ | 다시 시도 「그 행의 `fileName`」 ~~취소선~~ → **`fileName` uuid 자리 = 그 행 id** 로 찾음(⑪ ⓑ 와 같은 방법 · 고객 이름 변경에 안 흔들림 · 기본값(코디)) |
| W4 | 규칙 39 ⑪ ⓒ · :815 매트릭스 · 토스트 표 · :1356 OQ-86 ⓑ ⓓ · spec-000 `content_type` | 「기본값(코디)」 = **채팅 사진과 같게 JPEG 만 · 머리 확인 · 확장자 `jpg`**(DAY-SPEC-004 「첨부 저장」 · `contracts.py` `KEY_PATTERN` 의 `jpg`) · 형식 밖 = 400 `photo_type`(제안 · 채팅 `chat_photo_type` 꼴 · 글자 OQ-88) · 가져오기에서 JPEG 아닌 KOS 사진(png 등)은 **건너뜀**(OQ-96 ⓕ) — 사용자 확인 전 |
| W5 | 규칙 39 ⑪ ⓒ · spec-000 `visit_photo.created_at` | 가져온 행 `created_at` = 가져온 시각 — §2 「외부 생성 시각」과 다른 **이유** = KOS 사진 목록 응답에 생성 시각 칸이 없다(HAR 응답 키 `id` · `fileName` · `category` · `equipment` · `memo` · `scheduleId` · `visitorId` · `source` · `deleted` · `shootingDateTimeUtc` — 찍은 시각은 `shot_at`) |
| W6 | 매트릭스 :825 · :826 · 삭제 실패 줄 | 새 줄: 삭제 · 다시 시도의 KOS 401 = `session_expired`(올리기와 같은 갈래 · 세션 끝냄) · 다시 시도 + 저장소 꺼짐 = 409 / 503 `photo_disabled`(행 상태 그대로 · id 만 찾으면 되는 경우는 저장소 없이 `external_ref`) · 「KOS 삭제 실패 200」 줄은 401 을 뺀 실패로 범위를 적음 |
| W7 | :1110 「KOS 사진 — 직접 호출」 첫머리 | 「(C23) 가져오기는 중앙 작업이 부르고 토큰 = 탭을 연 직원(`staff_id` 의 `external_session` · ⑪ ⓓ)」 한 줄 |
| W8 | spec-004 :425 채팅 키 행 | `before-after` 언급은 남기고 「(2026-11-24 — 전후 사진 폴더 이름은 ~~`before-after`~~ **`beforeAfter`** …)」 한 줄 덧붙임(채팅 키 규칙 그대로) |
| W9 | :1323 DB 절 | 첫머리 「(개정 ㉘ **차트 탭 저장**) migration 없음」 · 사진 쪽 「(개정 ㉘ 시술전후사진 — C22 · C23) … migration 필요」로 범위 붙임 |

- `log.md` spec-change 1행. 10-decision 은 바꿀 것 없음(escalation 없음).
- 결정 파일에 없는 정책은 모두 「기본값(코디)」 + OQ(OQ-86 ⓑ ⓓ · OQ-96 ⓔ ⓕ)로 두었다.
- 고쳐 둔 사실 하나: W4 처음 초안에 「채팅은 형식 오류 코드를 따로 두지 않는다」고 쓰려다 DAY-SPEC-004 :410 `chat_photo_type` 이 있음을 확인하고 `photo_type`(같은 꼴)로 바꿈.

## 검증

`python3 scripts/lint-pipeline.py --strict` → **0 error · 263 warning** · `products/day/` 0건(전부 타 제품 — 무관). 바꾼 표 열 수 점검 통과(OQ-92 행 포함).

## 미결 · 주의

- W4 기본값(JPEG 만)이면 **KOS 웹에서 png 로 올린 사진은 가져오기에서 빠진다**(HAR 의 KOS 웹 업로드 = png). 사용자 확인 때 png 를 받을지 같이 볼 것(OQ-86 ⓑ).
- 코드 키 규칙(`contracts.py` `PURPOSE = "chat"`)에 `beforeAfter` 를 더하는 일은 코드 몫.
