# 리뷰 리포트 — day-chart-photo / code 검수 3 (WP② 시술전후사진 · be-photo-1 · fe-photo-1) (2026-11-24)

- 대상: 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo` 미커밋 변경(사진 서버 · 사진 탭 화면)
- 근거: SPEC-002 U-16 · 규칙 39 ① ~ ⑪ · SPEC-000 `visit_photo`(mediness `4d9214af`) · 결정 C8 ~ C13 · C22 · C22-기본값 · C23 · C24-기본값 · 계약 보충 3(K4)
- read-only. 파일 수정 없음.

## 판정: WARN

FAIL 은 없다. 관문 3개 모두 통과했다. migration 은 SPEC-000 과 같다. 올리기 · 삭제 · 다시 시도 · 파일 · 가져오기는 규칙 39 의 순서와 transaction 경계를 지킨다.
WARN 중 둘은 실물에서 드러날 가능성이 높다.
- **P1**: 가져오기에서 KOS 사진 한 장이 실패하면 그 방문의 사진이 한 장도 들어오지 않는다. 테스트 이름은 「이미 커밋한 사진은 남고」인데, 실제로는 이 성질을 확인하지 않는다.
- **P2**: 「KOS 삭제 안 됨」 행에 닿는 화면 길이 없다. 그 KOS 사진은 아무 표시 없이 KOS 에 남는다(사용자 확인 필요).

## 관문 명령(1회씩)

| 명령 | 결과 |
|---|---|
| `scripts/test.sh -q backend/tests/day` | **1849 passed** (191.6s · exit 0) |
| `cd backend && uv run ruff check day tests` | All checks passed |
| `cd scripts/frontend && npm run -s check` | 118 pass · 0 fail |

## 1. migration 0024 — PASS
- `backend/migrations/versions/20261124_0024_visit_photo.py` — 칸이 SPEC-000 §07 `visit_photo` 표와 같다(`id` · `visit_id` · `customer_id` · `category` · `file_key` · `bytes` · `sha256` · `content_type` · `source` · `created_by_staff_id` nullable · `shot_at` · `created_at` · `updated_at` · `deleted_at`).
- 인덱스는 SPEC 과 같다: (`visit_id`,`shot_at`) `WHERE deleted_at IS NULL` · (`file_key`).
- enum `photo_category`(before · after) · `photo_source`(day · kos).
- 데이터 규칙: 소프트 삭제 칸 · 시각 칸 전부 `timestamptz`(UTC) · 업체 전용 칸 0(KOS id 는 `external_ref` `entity_type = visit_photo`) · 반영 상태 칸 없음.
- down 은 인덱스 → 테이블 → enum 순으로 지운다. `tests/migrations/test_visit_photo_migration.py`(up → down → up) · `test_alembic` HEAD 0024.

## 2. 올리기 — PASS (P4 · P5 낮음)
| 항목 | 위치 | 판정 |
|---|---|---|
| 순서: 저장소(transaction 밖) → 행 + `photo.upload` 커밋(실패면 파일 지움) → transaction 밖 KOS → `external_ref` 커밋 | `services/visit_photos.py:284-330` | PASS(규칙 39 ② ⓑ ~ ⓔ) |
| 직원 토큰 = 그 세션의 `external_session`(다른 직원 · 시스템 계정 안 씀) · 없으면 401 · 아무것도 안 남김 | `visit_photos.py:101-112` · `:280` | PASS(C10 · ⑦) |
| KOS 401 = 행 남김 · 세션 끝냄 · 401 | `visit_photos.py:233-254` | PASS(⑦) |
| 이름 매칭(`get-codes` 두 번 · 이름 같은 첫 코드) · 못 찾으면 KOS 에 아무것도 안 올림 · `photo_code_missing` | `services/visit_photo_kos.py:239-264` | PASS(C13) |
| KOS 쪽 실패 = 200 · 행 남김 · `kos_rejected` 1행 · 「KOS 미반영」 | `visit_photos.py:202-230` | PASS(C22-기본값 ①) — 토스트는 P3 |
| 다시 시도가 같은 사진을 두 번 등록하지 않음: 먼저 `get-visitor-images` 에서 `fileName` uuid 자리(= 행 id)를 찾고, 있으면 ref 만 단다 · `fileName` 이 행 id 로 정해져 늘 같다 | `visit_photos.py:452-490` · `visit_photo_kos.py:228-236` · `policies/photos.py:43-51` | PASS(③ · ④) — 동시성은 P4 |
| 형식 = JPEG · PNG 머리 · 확장자는 실제 형식 · 크기 5MB(본문 5MB + 64KB 넘으면 끝까지 읽지 않음) | `policies/photos.py:27-32` · `routers/board_photos.py:116-141` · `visit_photos.py:151-158` | PASS(C24-기본값 · C22-기본값 ⑤) |
| 저장소가 꺼짐 = 409 `photo_disabled` · 접근 실패 = 503 | `visit_photos.py:74-88` · `:166-170` | PASS |
| 키 `beforeAfter/{병원}/{32hex}.{jpg\|png}` · 키 모양 검사 | `adapters/storage/contracts.py` · `blob.py` 주석 | PASS(C22) |
| `event_log` payload 에 파일 이름 · 키 · 주소 · 토큰 없음 | `visit_photos.py:303-311` · `:213-227` | PASS(⑨) |

## 3. 삭제 · 파일 열기 — PASS (P2)
- 삭제: 소프트 삭제 + `photo.delete` 커밋 → transaction 밖에서 KOS 삭제(살아 있는 ref 가 있을 때) → 성공하면 ref 소프트 삭제 · 실패하면 DAY 는 지운 그대로 · ref 남김 · 200(`visit_photos.py:341-402`). 저장소 파일은 지우지 않는다(OQ-95). **PASS(⑤)** — 다만 P2.
- 권한: 목록 · 파일 = `board` view · 올리기 · 삭제 · 다시 시도 = `board` edit(`routers/board_photos.py:105` · `:150` · `:178` · `:196` · `:218`). 보기 권한이면 조각에 올리기 · 삭제 · 다시 시도가 없다(`board_photos.html`).
- `no-store` · `inline` · `nosniff` · `Content-Length`(`board_photos.py:46-50` · `:226-236`). 형식은 DB `content_type` 을 쓴다.
- 다른 방문 · 병원 photo_id: `chartable`(그 병원 · 차트를 열 수 있는 방문)과 `_row`(`row.visit_id == visit_id` · 지운 행 404)가 둘 다 막는다(`visit_photos.py:91-121`). 테스트 `test_board_photos.py` 404 행(다른 병원 · 다른 방문 사진 · 지운 행). **PASS.**

## 4. C23 가져오기 — PASS (P1 · P7)
| 항목 | 위치 | 판정 |
|---|---|---|
| 화면 요청은 작업을 넣기만 한다(Redis `queued` + `kiq`) · 최대 3초 기다림 · 안 끝나면 `reread` · `poll=1` 은 작업을 넣지 않음 | `services/visit_photo_import.py:103-152` · `routers/board_photos.py:101-113` | PASS(⑪ · OQ-97) |
| 잠금 = `try_lock` 같은 방문 · 못 얻으면 `skipped_running` · 도는 중이면 새로 넣지 않음 | `visit_photo_import.py:167-197` · 테스트 `test_같은_방문은_잠금으로_한_번만` | PASS(ⓐ) |
| `external_ref` 로 중복 막기 = 이미 들어온 KOS id 건너뜀 · 들일 때 `on_conflict_do_nothing` → 충돌이면 그 행 · 파일 버림 | `visit_photo_import.py:243-268` · `:343-372` · `visit_photo_kos.py:161-188` | PASS(ⓑ · ⓒ) |
| DAY 가 올린 미반영 행(지운 행 포함)은 ref 만 단다 | `visit_photo_import.py:301-326` · 테스트 `test_DAY_가_올린_KOS_미반영_행은_external_ref_만_지운_행도` | PASS — 다만 P2 |
| PNG · JPEG 만 · HEIC 등 건너뜀(셈) · 「시술 전」 · 「시술 후」 밖 건너뜀 | `:318-322` · `:338-341` | PASS(C24-기본값 · OQ-85 ⓐ) |
| 받은 파일 검증 = 머리(매직 바이트)만 · 크기 한도 없음 | `:338` | PASS(OQ-96 기본값) — P7 |
| 토큰 = 탭 연 직원의 만료 안 된 토큰(`outbox_delivery.staff_token`) · 없으면 실패 · 401 = 그 작업만 멈춤 | `:229-240` · `:294-295` · 테스트 `test_KOS_401_은_그_작업만_멈추고_세션은_그대로` | PASS(ⓓ) |
| KOS 에서 지워진 사진 = DAY 그대로 | DAY 행을 지우는 코드 없음 | PASS(ⓕ · OQ-96) |
| 같은 방문을 동시에 열 때: 두 요청이 모두 `queued` + `kiq` → 하나만 잠금 · 다른 하나 `skipped_running` · 늦게 돈 두 번째 작업은 `linked` 로 건너뜀 | 위 | PASS |
| 실패 조용히 · `photo.import` 1행 · 경고 로그 · 끝 표시(`failed`) | `:170-197` · `:200-226` | PASS(ⓔ · OQ-98) |
| 10초 동기화 · 차트 열기 · 판에는 넣지 않음 | 작업을 넣는 곳 = 사진 GET 하나 | PASS(ⓖ) |

## 5. 화면 — PASS (P3 · P6)
- 실패 자리: `board_chart_parts.html` 사진 패널 `.day-photos__failed[data-day-photos-failed]`(아이콘만 · role=alert · hidden) · `day.js:1585-1594` `photosLoaded` — 사진 GET 이 못 받으면 보이고, 받으면 감춘다.
- `reread`: `board_photos.html` 끝의 `hx-get …?poll=1` · `load delay:5s` 한 번(JS 없음 · 작업을 넣지 않음).
- 미반영 표시: `is-unsynced` + 경고 아이콘(E65) + edit 면 [다시 시도] 아이콘 버튼.
- 지어 넣은 글자 0: 묶음 제목 = 서버 값 · 버튼 · 표시 = 아이콘만 · aria-label 없음(OQ-88 — 사용자 확인 대기).
- 인라인 script · `style=` 0(두 템플릿 검색 결과 0) · 썸네일 = DAY 경로(`data:` · 서명 주소 없음 · CSP `img-src 'self'`).

## WARN

### P1 (중간) 가져오기 — KOS 사진 하나만 실패해도 그 방문 전부가 들어오지 않는다. 고장 난 사진이 하나 있으면 탭을 열 때마다 같은 자리에서 실패한다
- 위치: `backend/day/emr/kos/photos.py:111-122` `download_photos` — 서명 1회 뒤 **모든 주소를 먼저 받는다**. 한 GET 만 실패해도 `KosError` 가 나고 아무것도 돌려주지 않는다. `services/visit_photo_import.py:286-289` 에서 저장(`_store_one`)은 다 받은 다음에야 시작한다.
- 근거: 규칙 39 ⑪ ⓒ · ⓔ 「사진마다 짧은 transaction · **이미 커밋한 사진은 남는다**(사진마다 커밋)」. 지금 코드에서는 받기 실패가 늘 「0장 커밋」이다. 사진마다 커밋하는 장점이 「저장소 실패」 한 갈래에만 남는다.
- 조용히 통과하는 자리: `tests/day/board/test_board_photo_import.py:103` `test_실패는_조용히_이미_커밋한_사진은_남고_기록_1행` 은 사진 **1장**으로 `imported == 0` 만 확인한다. 2장 중 1장만 실패할 때 1장이 남는지는 아무 테스트도 보지 않는다.
- 제안: `download_photos` 가 사진마다 (바이트 | 실패)를 돌려주게 한다. 그리고 받는 즉시 한 장씩 저장한다(메모리도 한 장씩). 실패한 장은 `skipped` 로 센다.

### P2 (중간 · 사용자 확인 필요) 「KOS 삭제 안 됨」 행에 닿는 화면 길이 없다 — KOS 삭제가 실패하면 KOS 에 사진이 말없이 남는다
- 위치: 삭제 KOS 실패 → DAY `deleted_at` · ref 살아 있음(`visit_photos.py:359-365`). 목록은 살아 있는 행만 그린다(`:128-133`). 그래서 [다시 시도] 버튼이 나오지 않는다. 다시 시도의 「지운 행 · ref 있음 = KOS 삭제만」 갈래(`:430-432`)는 화면에서 부를 수 없다. fe-photo-1 보고도 「목록에서 빠지는 행이라 그리지 않음」이라고 적었다.
- 같은 상태가 하나 더 생긴다: 올리기의 KOS 등록이 진행 중일 때 사용자가 사진을 지운다 → 등록이 끝나 ref 가 달린다(`_kos_register` → `link`). 또는 가져오기가 지운 행에 ref 를 단다(`visit_photo_import.py:312-316`). 두 경우 모두 KOS 에 사진이 남는다.
- 토스트도 없다. 삭제 KOS 실패 = 200 · `kos_error` 만 있고 `message=""`(P3)이라 직원은 KOS 에 남았는지 알 수 없다.
- 근거: C22-기본값 ④ 「DAY 는 삭제 · **KOS 삭제 재시도 표시**(OQ)」 · 규칙 39 ⑤ 「→ ③ 으로 다시(표시 자리 · 글자 OQ-94)」. 서버 길은 있다. 표시 자리가 없을 뿐이다.
- 정할 것: OQ-94 표시 자리(예: 묶음 아래 「KOS 에 남은 사진 N」 + [다시 시도]). 아니면 다음 탭 열기 때 가져오기 작업이 그 KOS 삭제를 다시 하게 할지.

### P3 (낮음 · 사용자 확인 필요) KOS 쪽 실패(올리기 · 삭제 · 다시 시도)에 토스트가 없다
- 위치: `routers/board_photos.py:76-90` — `kos_error` 를 넘기지만 `message=""` 다. 템플릿은 `message` 만 그린다(`board_photos.html` 끝).
- 근거: 규칙 39 ② 「200 + 실패 토스트」. 글자가 OQ-88 이라 비워 둔 것은 계약 보충 3 대로다. 결과적으로 올리기 실패는 빨간 아이콘으로만 보이고, 삭제 실패는 아무 표시도 없다(P2). 글자가 정해지면 `kos_error` → `message` 한 줄로 열 수 있다.

### P4 (낮음) 다시 시도 · 올리기의 KOS 등록에 잠금이 없다 — 「찾기 → 없으면 등록」 사이에 같은 사진을 두 번 등록할 수 있다
- 위치: `visit_photos.py:452-490`(찾기와 등록이 잠금 없이 이어짐) · `visit_photo_kos.py:161-188`(`link` 의 유일 제약은 KOS id 기준이라 **KOS id 가 다른 두 등록**은 막지 못함 · 반환값 무시).
- 순서: 올리기가 KOS 등록 중(PUT ~ register 수 초) → 다른 직원이 같은 탭을 열면 그 행이 「KOS 미반영」으로 보임 → [다시 시도] → `find_external` 이 아직 없음 → 등록 → KOS 에 같은 사진 두 장 · DAY ref 두 줄(같은 행). 같은 화면의 htmx 두 번 클릭은 요청 잠금으로 겹치지 않는다.
- 제안: 다시 시도 · 올리기 KOS 단계에 행 단위 Redis 잠금(가져오기 잠금과 같은 꼴)을 둔다. 드물어서 다음 고침으로 넘겨도 된다.

### P5 (낮음) 올리기 검사 순서 — 큰 본문 · multipart 오류가 404 방문보다 먼저 나온다
- 위치: `routers/board_photos.py:156`(`_form` → 413 · 400) → 서비스 `chartable`(404). SPEC 규칙 39 ② ⓐ 의 순서는 401 → 403 → **404** → 400 → 413 이다. 5MB 를 넘는 파일을 없는 방문에 올리면 404 대신 413 이 나온다. 본문을 끝까지 읽지 않는 장점과 맞바꾼 것이라 기록만 한다.

### P6 (낮음 · 사용자 확인 필요) 삭제는 확인 없이 한 번 누르면 KOS 까지 지운다
- `board_photos.html` `[data-day-photo-delete]` — 확인 창 없음. 삭제 확인 글자 = OQ-88(디자이너 · 사용자 몫)이라 짓지 않았다. 계약대로다. 실물에서는 잘못 누르면 바로 KOS 삭제가 일어난다.

### P7 (낮음) 가져오기 자원 — 원본 전부를 메모리에 받고 · 병원 전체 사진 KOS id 를 매번 읽는다 · 잠금 120초
- `emr/kos/photos.py:121-122`(모든 원본 `resp.content` · 크기 한도 없음 — OQ-96 기본값) · `visit_photo_import.py:246-255` `_known`(그 병원 `visit_photo` ref 전부 — 시간이 갈수록 커짐 · 방문으로 좁힐 수 있음) · `photo_import_lock_seconds=120` 보다 오래 돌면 두 번째 작업이 겹친다(유일 제약이 중복을 막아 결과는 맞지만, 같은 원본을 두 번 받는다). P1 을 고칠 때 같이 보면 된다.

### P8 (참고 · OQ-87) 썸네일 = 원본 바이트
- 탭을 열면 사진마다 최대 5MB(가져온 사진은 한도 없음)를 받는다. 서버 축소 없음이 SPEC 기본값(OQ-87)이다. 실물에서는 속도로 드러난다.

## 6. 조용히 통과하는 자리(FakeKos · disk 라 못 보는 것)
1. **KOS `fileName` 과 uuid 자리**: 실물 KOS 가 `fileName` 을 그대로 돌려주는지 본다(고객 이름의 공백 · 특수문자 · 길이 제한 · 이름을 바꾸는 저장). 다시 시도 · 가져오기의 중복 막기는 이 한 가지에만 기댄다.
2. **서명 주소 순서**: `signed_urls` 는 「보낸 순서」를 가정한다(`emr/kos/mapper_photo.py:32-38`). KOS 가 순서를 바꾸면 사진과 바이트가 엇갈려 저장된다. 길이만 확인하기 때문이다.
3. **presigned `PUT` 의 `Content-Type`**: S3 서명에 Content-Type 이 들어 있으면 `image/png` 등이 거절될 수 있다. FakeKos 는 무엇이든 받는다.
4. **KOS 일정 사진 탭에 보이는지**(`scheduleId` · `source=HOSPITAL` · 분류 · 장비 · 메모) — 응답 고정본은 가짜 값이다.
5. **worker 실프로세스**: 작업은 함수로 직접 실행해 확인했다. `taskiq worker … day.tasks` 에서 `day.import_visit_photos` 가 등록되는지, broker · Redis 표시가 실제로 도는지는 보지 않았다(be-photo-1 「실행 못 함」).
6. **Azure Blob `beforeAfter` 폴더**: 관리 ID 로 쓰기 · 읽기 권한이 있는지 본다(dev 컨테이너).
7. **P1** — 테스트가 1장만 쓰므로 부분 실패가 드러나지 않는다.

## 7. 최종 실물 e2e 체크리스트(로컬 · KOS 데모 지점 · 시험 고객 · WP① ② ③ 이 모두 들어간 상태 · 1회)

### 차트(WP① ③)
1. 간호관리 여러 줄 → [저장] 1회 → 요청 1개 · 바뀐 줄만(DevTools 폼 칸) · 그 탭 「최근 저장」만 바뀜 · KOS 간호관리 메모 = 쓴 글
2. 의사차트 탭 따로 [저장] → 간호관리 「최근 저장」 그대로
3. 수락 · 진행중 줄에서 의사차트 집도의 변경 → [저장] → 판 카드 · 원장 상태 갱신 · KOS 집도의 → 메모 순서
4. 충돌 (i): 창을 연 뒤 KOS 웹에서 같은 줄 메모 수정 → 10초 넘게 기다렸다 DAY [저장] → 409 · 저장 0 · 칸 = KOS 글 + 줄바꿈 + 내 글 → 다시 [저장] → 200 · KOS = 이어 붙인 글
5. 충돌 (ii)(C18): KOS 수정 직후(10초 안) DAY [저장] → 409 → 15초 뒤 다시 [저장] → **200 · KOS 글 한 번**
6. 응답 유실(C19): [저장] 직후 DevTools offline → 다시 연결 → 같은 [저장] → **200 · 이력 1**
7. CRLF(C20): KOS 에서 여러 줄 메모 → 동기화 뒤 그 줄 [저장] → 409 아님
8. 보내는 중 잠금(C21-기본값): [저장]을 누르고 응답 전 글 칸 입력 → 입력 안 됨 · 응답 뒤 풀림 · offline 실패면 풀리고 [저장] 켜짐
9. 미저장 ✕ · Esc → 확인 창 · 바깥 누르기 → 아무 일 없음 · 「계속 쓰기」 → 그대로 · 「버리고 닫기」 → 요청 0 · 미저장 없으면 ✕ 바로 닫힘 · 탭을 옮겨도 쓴 글 남음
10. 담당자 비운 줄 → [저장] → 오류 토스트 · form 그대로 · 저장 0
11. (review-code-2 N1) 집도의가 둘인 의사차트 줄: KOS 충돌 → 동기화가 지나고 → 다시 [저장] → 또 409 가 나는지
12. 보기 권한 계정 → [저장] 없음 · 글 칸 읽기만 · 사진 올리기 · 삭제 · 다시 시도 없음
13. 헤더 「이름 직군」 — 간호 · 원장 · 직군 둘 이상(이름만) · 판 · 예약 · kit 화면

### 사진(WP② ③)
14. 사진 탭 첫 열기 → (KOS 에 사진 없음) 두 묶음 · 빈 칸 · 실패 자리 안 보임
15. 「시술 전」 · 「시술 후」에 JPEG 1장 · PNG 1장 올림 → 조각 갱신 · 썸네일 · KOS 웹 그 일정 사진 탭에 보임(분류 · 장비 「태블릿」 · 메모 「{고객} 고객 시술 전 / 후」 · 찍은 시각) · Azure `beforeAfter/{병원}/…` 에 파일
16. 썸네일 누르기 → 새 창 원본 · 응답 헤더 `Cache-Control: no-store` · `inline` · `nosniff`
17. 1장 삭제 → DAY 목록에서 빠짐 · KOS 사진 탭에서 사라짐
18. KOS 웹에서 그 일정에 PNG 1장을 직접 올림 → DAY 사진 탭 다시 열기 → 3초 안에, 아니면 5초 뒤 `poll` 로 보임(`source=kos`) · 한 번 더 열어도 두 장이 되지 않음
19. 두 창에서 같은 방문 사진 탭을 동시에 열기 → 가져온 사진 한 장씩(중복 없음)
20. KOS 웹에서 그 사진 삭제 → DAY 에는 남음(OQ-96)
21. (P1) KOS 에 사진 2장 · 그중 1장은 HEIC 또는 깨진 파일 → 다른 1장이 들어오는지(HEIC = 건너뜀 · 받기 실패 = 지금은 전부 0장)
22. KOS 분류 · 장비 코드 이름이 없는 지점(또는 이름을 바꿔 둠) → 올리기 → 행 남음 · 「KOS 미반영」 아이콘 · [다시 시도] → 이름을 되돌린 뒤 → 반영 · KOS 에 한 장만
23. 올리기 중 KOS 끊김(DevTools 로는 안 됨 — 연결 설정을 잠깐 틀리게) → 「KOS 미반영」 → [다시 시도] → KOS 에 **한 장만**(이미 등록됐으면 찾기만)
24. (P2) 삭제 중 KOS 실패 → DAY 에서 빠짐 · KOS 에 남는지 · 화면 표시가 없는지 기록
25. 5MB 넘는 파일 → 413 오류 토스트 · GIF/HEIC → 400 `photo_type` · 저장소 끈 설정 → 409 `photo_disabled`
26. KOS 직원 토큰 만료 상태로 올리기 → 401 → 로그인 화면(`session_expired`) · 행 남지 않음
27. 사진 탭 GET 이 실패하게(서버 끄기) → 실패 자리(경고 아이콘) 보임 · 다시 탭 고르면 다시 읽음
28. 다른 병원 · 다른 방문의 `photo_id` 로 `/file` 직접 열기 → 404

## 사용자 확인 필요(결정 문제 — SPEC 재논의 아님 · 기록만)
- P2: 「KOS 삭제 안 됨」 표시 자리(OQ-94) — 아니면 다음 탭 열기 때 작업이 KOS 삭제를 다시 할지
- P3 · P6: KOS 실패 토스트 · 삭제 확인 글자(OQ-88)
- P1: 받기 실패 한 장 = 그 장만 건너뜀으로 고칠지(SPEC ⑪ ⓔ 문장과 맞추는 쪽 — 결정이라기보다 구현 고침)

## 참고(무관 · 기존)
- 차트 쪽 review-code-2 N1(의사 동기화 이력 집도의 기준) · N2(`README.md:200` 테스트 파일 이름)는 이번 범위 밖이다. 아직 열려 있다.
