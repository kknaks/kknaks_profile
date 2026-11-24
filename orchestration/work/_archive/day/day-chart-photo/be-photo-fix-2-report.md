# be-photo-fix-2 결과 보고 — 결정 C25 · C27

## 상태: done (커밋 안 함 · 템플릿 · JS 안 건드림)

## 수행
| 결정 | 위치 | 내용 |
|---|---|---|
| C25 KOS 삭제 다시 하기 | `backend/day/services/visit_photo_import.py` `_redelete` · `_run` | 가져오기 작업 끝(ⓑ 목록 · ⓒ 저장 → ⓘ)에서 그 방문의 **지운 행 중 살아 있는 `external_ref`** 가 남은 행마다 KOS `delete-visitor-images {ids: [그 KOS id]}` → 성공이면 ref 소프트 삭제(`unlink` · 기존 규칙) · 한 행 실패(`EmrError`)는 조용히 다음 탭 열기로(표시 · 토스트 없음 · 작업은 `done`) · 직원 토큰 401 은 그 작업만 멈춤(`failed` · `token_rejected` · 세션 안 끝냄). 같은 작업이 ⓑ 에서 지운 행에 단 ref 도 같은 회차에 정리된다. KOS 를 기다리는 동안 transaction 없음 · 같은 직원 토큰 · `photo.import` payload 에 `kosDeleted`(장수) |
| C27 KOS 실패 토스트 | `backend/day/routers/board_messages.py` `PHOTO_KOS_FAILED_MESSAGE = "KOS 반영에 실패했습니다"`(기존 메시지 모음 — `KOS_FAILED_MESSAGE` 옆) · `routers/board_photos.py` `_render` | `kos_error` 가 있으면(올리기 · 삭제 · 다시 시도 — `photo_code_missing` · `kos_unavailable` 모두) 조각 값 `message` = 그 글자 · 없으면 빈 값. 템플릿(FE)이 이미 `message` 가 있으면 토스트를 그림 |

## 테스트
- `test_board_photo_import.py`
  - `test_C25_KOS_삭제_실패로_남은_사진은_다음_가져오기가_다시_지운다` — 두 장 지움 · KOS 삭제 실패로 ref 남음 → 가져오기(KOS 여전히 실패) = `done` · 0장 · ref 그대로 → 다시 가져오기 = 행마다 삭제 2회 · ref 정리 · DAY 는 지운 그대로 · `kosDeleted: 2` → 그다음 가져오기는 삭제 안 함
  - `test_C25_다시_지우기_중_토큰_401_이면_작업만_멈춤`
  - 고침: `test_DAY_가_올린_KOS_미반영_행은_external_ref_만_지운_행도` — 지운 행에 단 ref 가 같은 작업에서 KOS 삭제 · 정리됨(C25) · 첫 테스트 payload 에 `kosDeleted`
- `test_board_photos.py` `test_C27_KOS_쪽_실패_토스트_올리기_삭제_다시_시도` — 성공 = `message` 빈 값 · 토스트 글자 없음 / 올리기(코드 이름 없음) · 다시 시도(찾기 실패) · 삭제(KOS 삭제 실패) = `message` 「KOS 반영에 실패했습니다」 · 응답 HTML 에 그 글자

## 검증
- `scripts/test.sh -q backend/tests/day/board` — **275 passed**
- ruff: 내가 만진 파일 깨끗 · mypy Success 604 files
- 무관(frontend 파일): `backend/tests/day/web/test_board_page_chart_photos.py:127` E501(C26 테스트 docstring) — frontend 진행 중 파일이라 건드리지 않음

## 주의
- C25 는 그 방문의 사진 탭을 다시 열 때만 돈다 — 다시 열지 않는 방문의 KOS 사진은 남는다(결정 그대로 · planner-fix-9 미결과 같음).
- 다시 시도 API 의 「지운 행 = KOS 삭제만」 갈래는 그대로 둠(SPEC 그대로).
