# be-photo-1 결과 보고 — WP② 시술전후사진 서버 (DAY 저장 + KOS 등록 + KOS 가져오기)

## 상태: done (커밋 안 함 · 템플릿 · JS · CSS 안 건드림 · KOS 실물 쓰기 안 함)

SPEC 기준 = mediness `4d9214af`(PR #960) · 결정 C8 ~ C13 · C22 · C22-기본값 · C23 · C24-기본값 · 조각 계약 = `contract-k3-header-note-1.md` 보충 3(그대로 구현).

## 수행 — 파일
| 층 | 파일 | 내용 |
|---|---|---|
| migration | `backend/migrations/versions/20261124_0024_visit_photo.py`(새 · 0023 뒤 · dev 에 새 migration 없음 확인 `git fetch origin dev`) | `visit_photo` + enum `photo_category`(before · after) · `photo_source`(day · kos) · 인덱스 (`visit_id`,`shot_at`) WHERE 살아 있는 행 · (`file_key`) — SPEC-000 칸 그대로 |
| 모델 · 값 | `day/models/photo.py` · `models/__init__.py` · `enums/photo.py` · `identifiers.py`(`VisitPhotoId` · `ExternalPhotoId`) · `dtos/photos.py` · `common/error_codes.py`(`photo_type` · `photo_code_missing`) · `common/config.py`(`photo_import_wait_seconds`=3 · `photo_import_lock_seconds`=120) | |
| 저장소 | `adapters/storage/contracts.py`(`PHOTO_PURPOSE = "beforeAfter"` · 키 검사 = `chat/…/(jpg\|mp4)` 또는 `beforeAfter/{병원}/{32hex}.(jpg\|png)` · `new_key(…, purpose)`) · `blob.py` 주석의 `before-after` → `beforeAfter` | 채팅 저장소(`DAY_CHAT_STORAGE` · disk/blob · 관리 ID) 그대로 재사용 |
| KOS | `emr/normalized_photo.py` · `emr/kos/mapper_photo.py` · `emr/kos/photos.py`(`KosPhotos` mixin) · `emr/kos/staff_client.py`(`put_bytes` · `get_bytes`) · `emr/base.py`(업체 공통 인터페이스 6개 — 지원 안 하면 `WriteNotSupportedError`) · `emr/kos/__init__.py` | 7 경로 전부 내부 · 직원 토큰 · `kos-client-uri = <web>/<tenant>/reservation/schedule/`(HAR) · PUT/GET 은 인증 헤더 없음 · 주소 · 토큰 로그 없음 |
| 규칙 | `policies/photos.py` | JPEG · PNG 머리 · 5MB · 제목 「시술 전」 · 「시술 후」 · 장비 「태블릿」 · KOS `fileName` = `{고객}_{YYYYMMDD}_{행 id 32hex}.{ext}` · uuid 자리 찾기 · 메모 「{고객} 고객 시술 전/후」 |
| 서비스 | `services/visit_photos.py`(목록 · 올리기 · 삭제 · 다시 시도 · 파일) · `services/visit_photo_kos.py`(짧은 읽기 · 등록 7단계 · `external_ref` link/unlink · 기록) · `services/visit_photo_import.py`(C23 넣기 · 기다림 · 작업 본문) | |
| 태스크 | `day/tasks/photos.py` `day.import_visit_photos(visit_id, staff_id)` · `tasks/__init__.py` 등록 | 주기 없음 · 10초 동기화에 안 넣음 |
| 라우트 | `routers/board_photos.py`(새) · `main.py` 등록 · `errors.py` `PhotoError` · `web_errors.py` `photo_error_handler` | 경로 5개(보충 3) · 실패 = `X-Day-Error` + `HX-Reswap: none` + 토스트 조각(message 빈 값) |
| 표현 | `presentation/photos.py` | `photos = {visit_id, edit, reread, groups: [{category, title, items: [{photo_id, shot_at, kos_synced}]}]}` — 빈 묶음도 둠 |

## 동작 요약
- **올리기**: 404 방문 → 400 category · 파일 → 413(본문 5MB+머리 넘으면 끝까지 안 읽음) → 400 `photo_type` → 409/503 `photo_disabled` → 401 토큰(이 순서 전부 「아무것도 남기지 않음」) → 저장소(transaction 밖) → 행 + `photo.upload` 커밋(실패면 쓴 파일 지움) → transaction 밖 KOS(codes 두 번 이름 매칭 → presigned → PUT → register → 목록에서 uuid 자리로 id) → `external_ref` 커밋. KOS 실패 = 200 · 행 남김 · `kos_synced: false` · `kos_rejected` 기록 · KOS 401 = 세션 끝냄 → 세션 만료.
- **삭제**: 소프트 삭제 + `photo.delete` 커밋 → 살아 있는 `external_ref` 면 KOS 삭제 → 성공이면 `external_ref` 소프트 삭제 · 실패면 200 + 「KOS 삭제 안 됨」(ref 남음) · 저장소 파일 안 지움.
- **다시 시도**: 살아 있는 행 · ref 없음 = KOS 목록에서 uuid 자리로 먼저 찾기(있으면 ref 만 · 중복 등록 없음) → 없으면 저장소에서 읽어 등록 / 지운 행 · ref 있음 = KOS 삭제만 / 그 밖 아무것도 안 함 · `photo.kos_retry`.
- **파일**: DAY 저장소 바이트 · `no-store` · `inline` · `nosniff` · 지운 행 404 · 꺼짐 409. 화면 요청은 KOS 를 안 부름.
- **목록 + 가져오기(C23)**: `poll` 없으면 Redis 표시 `queued` + `kiq`(도는 중이면 안 넣고 기다림) → 최대 3초 `done`/`failed` 기다림 → 안 끝나면 `reread: true`. 작업 = 방문 잠금(`try_lock` · 못 얻으면 `skipped_running`) → 짧은 읽기 → `get-visitor-images` 1회 → uuid 자리가 이 방문 DAY 행(지운 행 포함)이면 ref 만 · 이미 들어온 KOS id 건너뜀 · 두 묶음 밖 건너뜀 → 원본 서명 1회 → GET → JPEG/PNG 만(HEIC 등 건너뜀) → 사진마다 저장소 + 행(`source=kos` · `created_by` 없음 · `shot_at`=KOS) + ref 한 transaction(유일 제약 충돌이면 그 행 · 파일 버림) · 실패 조용히 · `photo.import` 1행 · 토큰 = 탭 연 직원(`outbox_delivery.staff_token` · 없으면 실패 · 시스템 계정 안 씀) · 작업 안 401 = 그 작업만 멈춤(세션 안 끝냄) · KOS 에서 지워진 사진 DAY 그대로.
- `event_log` payload 에 파일 이름 · 저장소 키 · 주소 · 토큰 없음(테스트로 확인).

## 테스트
- `tests/day/board/test_board_photos.py`(23) · `test_board_photo_import.py`(10) — 매트릭스 행별: 404(다른 병원 · 다른 방문 사진 · 지운 행) · 400 × 2 · 413 · 400 `photo_type` · 409 / 503 `photo_disabled` · 401 토큰 없음 · KOS 쪽 실패 200(코드 이름 없음 · upload · register · codes 오류 · 외부 id 없음) · KOS 401 · 삭제 KOS 실패 200 · 다시 시도(이미 반영 · 이미 삭제 · 저장소 꺼짐 · 등록됐는데 id 못 찾음 = 찾기만) · 가져오기 실패(list · download · 토큰 · 고객 id 없음) · 잠금 · 지운 사진 그대로 · `poll`
- `tests/day/test_photo_policy.py` · `tests/day/emr/test_kos_photo_mapper.py`(응답 고정본 `fixtures/kos_visitor_images.json` · `kos_codes_image_category.json` — 값 가짜)
- `tests/migrations/test_visit_photo_migration.py`(up → down → up · 인덱스 · enum 거절 · 타입 지움) · 기존 `test_alembic` HEAD 0024 · `test_models` · `test_column_snapshot` · `test_enum_labels` 갱신

## 검증
- `scripts/test.sh -q` 전체 1회: 2664 passed · 3 failed(새 테이블 · enum 스냅샷 수) → 고친 뒤 그 3 파일 106 passed
- `scripts/test.sh -q backend/tests/day/board` + 사진 순수 · mapper · migration — 282 passed
- migration up/down = 격리 테스트 DB(`scripts/test.sh` 전용 PostgreSQL) — `test_visit_photo_migration` · `test_alembic` downgrade base → upgrade · `alembic check` 차이 없음
- ruff check · format --check(backend · scripts) OK · mypy Success 604 files

## SPEC · 계약과 다른 곳 / 코디가 확인할 것
- **KOS 쪽 실패 200 의 토스트**: SPEC 은 「200 + 실패 토스트」 · 보충 3 은 message 빈 값이면 토스트 없음(OQ-88). 조각에 `message=""` 와 함께 `kos_error`(`photo_code_missing` · `kos_unavailable`)를 더 넘긴다(보충 3 에 없는 이름 — 템플릿이 쓰지 않으면 무해). 글자가 정해지면 FE 가 쓸 값.
- **401**: 웹 화면은 기존 `SessionExpired` 처리(HTMX = `HX-Redirect: /login?reason=session_expired`) — 공지 저장과 같음.
- **코드 고르기**: 같은 이름 첫 코드(C13) · `closed` 는 보지 않음(OQ-89 확인 안 됨).
- **KOS `fileName` 날짜** = 병원 현지 날짜(OQ-89 ⓑ 기본값으로 둠).
- 작업 안 직원 토큰 = 그 직원의 살아 있는 어떤 세션 토큰이든(쓰기 큐 규칙 24 와 같은 고르기) — 탭을 연 바로 그 세션은 아님.
- 실행 못 함: 실물 e2e(KOS 데모 · 코디 몫) · worker 실프로세스(작업은 함수로 직접 실행해 확인).
