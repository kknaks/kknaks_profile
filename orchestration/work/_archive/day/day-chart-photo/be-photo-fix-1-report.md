# be-photo-fix-1 결과 보고 — review-code-3 P1 · P4 · P7

## 상태: done (커밋 안 함 · P2 · P3 · P6 안 건드림 · P5 기록만)

## 수행
| 항목 | 위치 | 내용 |
|---|---|---|
| P1 한 장씩 받고 저장 | `emr/base.py` · `emr/kos/photos.py` `download_photos(token, file_names, max_bytes)` → `AsyncIterator[PhotoDownloadData]`(새 `emr/normalized_photo.py`) · `emr/kos/staff_client.py` `get_bytes(url, max_bytes)` | 서명 1회(실패면 첫 장 전에 `EmrError` — 그대로 작업 실패) → 주소마다 GET 해 **한 장씩 내줌** · 한 장 GET 실패 · 한도 넘음 = 그 장만 `data=None`(원인 종류만 · 주소 없음) |
| 〃 | `services/visit_photo_import.py` `_run` | 받는 즉시 `_store_one`(저장소 + 행 + ref 한 transaction 커밋) · 실패한 장 = `skipped` + 기록 메모 · 메모리엔 한 장씩 |
| P4 행 잠금 | `services/visit_photos.py` `_kos_lock(photo_id)` = `try_lock("day:lock:photo_kos:{행 id}", photo_import_lock_seconds)`(가져오기 잠금과 같은 꼴 · 기다리지 않음) | 올리기의 KOS 단계 · 다시 시도의 「찾기 → 없으면 등록」 전체를 감쌈. 다시 시도가 잠금을 못 얻으면(올리기 · 다른 다시 시도가 등록 중) 아무것도 안 하고 200 + 지금 목록(`photo.kos_retry` 기록도 안 함) |
| P7 `_known` | `visit_photo_import._known` | 「이미 들어온 KOS id」를 그 방문 행에 달린 ref 로 좁힘(join `visit_photo.visit_id`). 다른 방문 행에 달린 같은 KOS id 는 `link` 유일 제약이 막고 그 행 · 파일을 버림(기존 길) |
| P7 시간 상한 | `run_import` | 작업 = `asyncio.timeout(photo_import_lock_seconds − LOCK_MARGIN_SECONDS(10))` — 잠금이 풀리기 전에 끝남 · 넘으면 `failed` · stage `timeout` · 이미 커밋한 사진은 남음 |
| P7 크기 한도 | 위 `get_bytes` · `_run` | 받는 원본 = `PHOTO_MAX_BYTES`(5MB · 올리기와 같음) — 조각으로 받다 넘으면 끊고 그 장만 건너뜀 |

## 테스트(새 · 고침)
- `test_board_photo_import.py`: `test_P1_두_장_중_한_장_받기_실패면_한_장은_남는다`(1장 커밋 · skipped 1 · 다음 실행은 고장 난 장만 다시 받음) · `test_P7_받는_원본은_5MB_까지_넘는_장은_건너뜀` · `test_P7_이미_들어온_KOS_id_판정은_그_방문_행만_본다` · `test_P7_작업은_잠금_수명보다_먼저_끝난다`
- `test_board_photos.py`: `test_P4_같은_행을_동시에_등록하면_KOS_등록은_1회`(올리기가 register 안에서 멈춘 사이 다시 시도 → 등록 1회 · ref 1 · kos_retry 기록 0)
- `test_kos_photo_mapper.py`: 한 장씩 · GET 실패 · 한도 넘음이 그 장만 None
- 가짜(`photo_support.FakePhotoKos`): `download_photos` 비동기 한 장씩 · `broken` · `gate`

## 검증
- `scripts/test.sh -q backend/tests/day/board` + 사진 mapper · 정책 — 285 passed
- ruff check · format --check(backend · scripts) OK · mypy Success 604 files

## 기록만(P5)
- 올리기 검사 순서 — 라우터 `_form`(본문 5MB 넘음 413 · multipart 오류 400)이 서비스 `chartable`(404)보다 먼저다. SPEC 규칙 39 ② ⓐ 순서(… 404 → 400 → 413)와 다르다. 본문을 끝까지 읽지 않는 장점과 맞바꾼 것 — 고치지 않음.

## 주의
- **SPEC 문장과 다름(브리프 지시)**: 규칙 39 ⑪ ⓒ 는 「크기 한도(5MB)는 올리기 한도라 가져오기에는 걸지 않는다(기본값 · OQ-96)」인데, 브리프대로 가져오기에도 5MB 를 걸었다 — SPEC 문구는 planner 몫.
- 행 잠금은 기다리지 않는다 — 겹친 다시 시도는 그 순간 「KOS 미반영」으로 그려지고, 다음 탭 다시 읽기에서 반영됨으로 바뀐다.
