# planner-fix-8 결과 보고 — 사진 파일 형식 (C24-기본값)

## 상태: done

워크트리 `mediness-mediness/day-chart-photo-spec` · 미커밋 변경 위 · 미커밋. 바꾼 파일 = `products/day/20-spec/spec-002-procedure-board.md` · `20-spec/spec-000-data-model.md` · `log.md`.

형식 = **JPEG · PNG 둘 다**(머리 확인 · 확장자 = 실제 형식대로 `jpg` · `png`) — 올리기 · KOS 가져오기 둘 다. 형식 밖 = 올리기 400 `photo_type` · 가져오기 건너뜀(앞 문장대로). 앞 판 「JPEG 만 · `jpg` 만」은 취소선 + 사유(KOS 웹이 PNG 로 올려 JPEG 만이면 C23 가져오기에서 빠짐).

| 자리(spec-002 줄) | 반영 |
|---|---|
| :431 U-16 올리기 | 형식 = JPEG · PNG(C24) · 여러 장만 OQ-86 |
| :645 API 사진 올리기 행 | `file` = JPEG · PNG |
| :815 매트릭스 형식 밖 | ~~JPEG 아님~~ → JPEG · PNG 아님 |
| :897 토스트 표 `photo_type` | 뜻 바꿈 · 채팅 글자 「JPEG 사진만…」은 뜻이 달라 그대로 못 씀(OQ-88) |
| :1215 규칙 39 | 키 `beforeAfter/{병원 id}/{32 hex}.{jpg \| png}` · ② ⓐ 형식 검사 = JPEG · PNG(밖 400) · ⑪ ⓒ 가져오기 형식 ~~JPEG 만~~ → JPEG · PNG · 그 밖(HEIC 등) 건너뜀 |
| :1356 OQ-86 ⓑ | 앞 기본값 ~~취소선~~ → C24-기본값(둘 다 · 머리 확인 둘 · 코드 `KEY_PATTERN` 에 `png` 더함 · 채팅 키 규칙 그대로) |
| :1366 OQ-96 ⓕ | ~~JPEG 아닌~~ → JPEG · PNG 아닌 |

| 자리(spec-000) | 반영 |
|---|---|
| :1202 `visit_photo.file_key` | 키 `….{jpg \| png}`(확장자 = 실제 형식) |
| :1203 `content_type` | ~~JPEG 만~~ → JPEG · PNG(`image/jpeg` · `image/png`) · 올리기 · 가져오기 둘 다 |

- `log.md` spec-change 1행. OQ 닫은 것 · 새 것 없음(OQ-86 ⓑ 기본값만 바뀜).

## 검증

`python3 scripts/lint-pipeline.py --strict` → **0 error · 263 warning** · `products/day/` 0건(전부 타 제품 — 무관). 바꾼 표 열 수 점검 통과.

## 미결 · 주의

- 코드: 저장소 키 규칙 확장자에 `png` · 용도 폴더 `beforeAfter` 를 더하는 일(채팅 `chat` 규칙은 그대로).
- `photo_type` 토스트 글자는 비어 있음(OQ-88).
