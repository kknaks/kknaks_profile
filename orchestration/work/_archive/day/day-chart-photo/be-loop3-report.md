# be-loop3 결과 보고 — 코드 검수 4 · e2e 2회차 (C33 · C34 · W3 · W5 · W6 · W7)

## 상태: done (커밋 안 함 · 템플릿 · JS 안 건드림) — SPEC `8ab5e2d2`(mediness #960 최신)

## 수행
| 항목 | 위치 | 내용 |
|---|---|---|
| **C33** 앞단 | `deploy/caddy/Caddyfile`(이 블록만) | `day_proxy` 스니펫(dev · prod 둘 다 이 스니펫을 import) — `@photo_upload`(POST `/board/visits/*/photos`) = `request_body max_size 100MiB` · `@other_body`(그 matcher 의 not) = 6MiB 그대로. 두 matcher 가 겹치지 않게 했다(겹치면 작은 쪽이 이겨 100MiB 가 안 먹음). `caddy:2` 이미지로 `caddy validate` — **Valid configuration** |
| 〃 서버 | `routers/board_photos.py` `_form` · `BODY_MAX_BYTES = 100MiB` | 본문 전체 100MiB — `Content-Length` 넘으면 바로 · 흘려 받다 넘으면 그 자리에서 413 `photo_too_large`(끝까지 안 읽음) · 장당 5MB · 장 수 한도 없음은 그대로 |
| **C34** | `emr/normalized_photo.py` `NormalizedVisitPhotosData(photos, skipped)` · `emr/kos/photos.py` `visit_photos`(매핑 실패 수를 돌려줌) · `emr/base.py` · `services/visit_photo_kos.py`(`.photos`) · `services/visit_photo_import.py` `_remove_gone` | ⓐ 목록에 매핑 실패가 하나라도 있으면 그 회차 삭제 판정 안 함 ⓑ 목록이 비었는데 KOS 반영된 살아 있는 행이 있으면 판정 안 함 — 가져오기 · C25 재삭제는 그대로 돈다 · 기록 메모 `kos_removed:unmapped` · `kos_removed:empty_list` |
| **W3** | `services/visit_photos.py` `upload` · `dtos/photos.py` `PhotoActionData.rejected` · `routers/board_photos.py` `_message` · `routers/board_messages.py` `PHOTO_SKIPPED_MESSAGE = ""` | 코디 답대로 — 빠진 장(검사 `photo_type` · `photo_too_large` · 저장소가 멈춰 남은 장 `photo_disabled`)이 하나라도 있으면 **기존 `message` 하나**에 요약 토스트 글자를 넣는다(KOS 실패 글자가 있으면 「 · 」로 이음). 글자는 사용자 확인 중이라 **상수만 · 빈 값**(빈 값이면 토스트 없음). 조각 값 `rejected`(코드 목록)는 기록용으로 넘김 |
| **W5** | `visit_photo_import._redelete` | 지운 행 · 살아 있는 ref 중, 이 회차 KOS 목록이 **온전하고**(매핑 실패 0) 그 KOS id 가 목록에 없고 ref 가 목록 읽기 전에 생긴 것이면 KOS 를 부르지 않고 ref 만 소프트 삭제(10초마다 실패 호출 쌓이지 않게) · 목록이 온전하지 않으면 지금처럼 KOS 삭제 |
| **W6** | `emr/factory.py` `adapter_for` · `close_adapters` | 고르기 · 만들기 · 바꿔 끼우기 사이에 `await` 없음 → 동시 첫 호출이 하나만 만든다 · 연결 설정이 바뀌면 옛 어댑터를 바로 닫지 않고 `_retired` 에 두었다가 `close_adapters`(API · worker 종료) 때 닫음 — 쓰는 중인 요청이 닫힌 클라이언트를 만나 500 이 나지 않게 |
| **W7** | (코드 변경 없음 · 테스트로 고정) | 서버 목록은 늘 `deleted_at IS NULL` 행만 · 가져오기도 지운 행을 되살리지 않음(uuid 자리 맞춤은 ref 만 담) — 삭제 뒤 `tick` 목록에 지운 사진이 없음을 테스트로 확인. 엇갈린 응답의 화면 처리는 frontend 몫 |

## 테스트
- 새 `tests/day/board/test_board_loop3.py`(10): C33 상한 넘으면 413 · 아무것도 안 남김 · 기본값 100MiB / C34 ⓐ 매핑 실패면 판정 안 함 · 가져오기는 함 · 온전하면 판정 / C34 ⓑ 빈 목록 / W3 형식 · 크기 걸린 장 `rejected` · `message` 빈 값 · 글자를 넣으면 KOS 실패와 한 토스트로 이음 · 저장소 중간 멈춤 = 남은 장 `photo_disabled` / W5 목록에 없으면 삭제 호출 없이 ref 정리 · 목록에 있으면 지금처럼 · 목록이 온전하지 않으면 지금처럼 / W6 동시 5회 = 생성 1 · 교체한 옛 것은 종료 때 닫힘 / W7
- `tests/deploy/test_deploy_contract.py`: Caddyfile — 올리기 matcher · 100MiB · 그 밖 6MiB · `request_body` 2개
- `tests/day/emr/test_kos_photo_mapper.py`: 목록 `skipped`(매핑 실패 수)
- 고침: `test_board_loop2.py` C31 두 테스트 — 빈 목록 가드(C34 ⓑ) 때문에 다른 분류 KOS 사진 하나를 남김 · `photo_support` 가짜 `unmapped`

## 검증
- `scripts/test.sh -q backend/tests/architecture backend/tests/day/board` — **613 passed**
- devtools(정형 결속) 203 passed · ruff check · format OK · mypy Success 606 files
- `caddy validate`(`caddy:2` 이미지 · 가짜 도메인 env) — Valid

## 주의
- W3 요약 토스트 글자 = 사용자 답 대기(제안 「올리지 못한 사진이 있습니다 (JPEG · PNG, 5MB 이하만)」) — 정해지면 `board_messages.PHOTO_SKIPPED_MESSAGE` 한 줄만 바꾸면 된다.
- 앞단 413(C33 — Caddy 응답 · DAY 코드 없음)의 화면 토스트는 frontend 몫(글자 OQ-88).
- W6: API · worker 가 각각 시스템 계정 세션을 오래 쥔다 — 로컬 · dev · prod 가 같은 KOS 시스템 계정이면 5개 한도 확인(review-code-4 그대로 · 실물 몫).
- deployment.md 의 앞단 상한 줄(planner-fix-11)과 Caddyfile 값(100MiB · 6MiB) 일치.
