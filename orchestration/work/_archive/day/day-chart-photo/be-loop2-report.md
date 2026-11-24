# be-loop2 결과 보고 — e2e 1회차 피드백 (E3 · C28 · C29 · C30 · C31)

## 상태: done (커밋 안 함 · 템플릿 · JS 안 건드림) — SPEC `7c5820d5`(mediness #960 최신) 기준

## 수행
| 항목 | 위치 | 내용 |
|---|---|---|
| **E3** 저장마다 sign-in 안 함 | `services/board_charts.py` `_kos_now` | `build_adapter`(새 클라이언트 · 토큰 없음) → `emr/factory.adapter_for`(병원별 캐시 · 연결 설정이 바뀌면 새로) · 캐시 어댑터는 요청마다 닫지 않음. API 종료 = `runtime/main.py` lifespan 의 `close_adapters()`(이미 있음 — 확인) |
| 〃 전수 확인 | `grep build_adapter(` | 남은 호출처 = `emr/factory.adapter_for` 안(캐시가 만드는 자리) · `services/visit_photo_kos.adapter_of`(사진 — 직원 토큰 경로 · 그대로) · `services/reservation_notice.save`(공지 저장 — 직원 토큰 경로 `staff_notices` · `create/change/delete_notice` 만 · 시스템 계정 sign-in 없음 · 그대로). 시스템 계정 읽기에 새 클라이언트를 쓰던 곳은 `_kos_now` 하나 |
| **C28** 여러 장 | `routers/board_photos.py`(`file` 칸 반복 `form.getlist` · 전체 본문 한도 없앰 · 칸 수 상한 1000) · `services/visit_photos.py`(`_check_files` · `_save_one` · `upload(files)`) · `services/visit_photo_kos.py` `register_many` | 장마다 검사(5MB · JPEG/PNG — 걸린 장만 거절 · 전부 걸리면 첫 장의 그 오류) → 장마다 저장소 + 행 + `photo.upload` 커밋 → KOS = 코드 1번 → 장마다 presigned + PUT(실패 = 그 장만) → 남은 장 `register-visitor-images` **1회**(`사진등록다수.har` 꼴) → 목록 1회에서 uuid 자리로 id → 된 장 ref 커밋 · 실패 장 = 「KOS 미반영」 + 토스트(C27) · 바이트는 장마다 업로드 임시 파일에서 다시 읽음(메모리 한 장) · 행 잠금(P4)은 장마다. 다시 시도도 같은 `register_many`(1장) |
| **C29** 거절 토스트 | `routers/board_messages.py` · `errors.py` `ChartStaffRejected` · `web_errors.board_error_handler` · `services/board_charts.py` · `routers/board.py` | UNSET 에서 `chart_staff_required` · `staff_not_listed` 뺌 · `chart_conflict` 「다른 곳에서 먼저 수정된 내용이 있습니다. 확인 후 다시 저장해 주세요」 · `chart_staff_required` 「담당자를 선택해 주세요」 · `staff_not_listed` 「선택할 수 없는 담당자입니다」 · 차트 저장의 `doctor_not_listed` = 예외의 `message_key`(`chart_staff_not_listed`)로 같은 글자 — **호출 · 수락의 `doctor_not_listed` 글자는 그대로**(SPEC 토스트 표) · 탭 저장 409 응답 `message` = `chart_conflict` 글자 |
| **C30** 탭 동기화 | `routers/board_photos.py` GET | `tick=1`(SPEC 이름 제안) = 작업만 넣고 기다리지 않음 · 지금 DAY 목록 · `poll` 없음 = 넣고 3초 기다림(그대로) · `poll=1` = 다시 읽기만(작업 안 넣음 — SPEC 표 그대로). 잠금 · 도는 중 중복 방지는 작업 쪽 그대로 |
| **C31** KOS 에서 지운 사진 | `services/visit_photo_import.py` `_remove_gone` | 목록 읽은 바로 뒤 · 그 방문 **살아 있는 행** 중 살아 있는 ref 가 KOS 목록(`deleted:false`)에 없는 행(`source` 무관) = 행 + ref 소프트 삭제(파일 그대로) · ref 없는 「KOS 미반영」 행 · **DAY 가 먼저 지운 행은 안 봄(C25 재삭제 몫)** · 목록 읽기 **전에** 생긴 ref 만(목록 읽는 사이 올리기가 등록한 사진을 지우지 않게 — `external_ref.created_at`) · 목록 실패면 판정 안 함 · `photo.import` payload `kosRemoved` |
| 정형 결속 | `.agents/skills/verify-day-chart/specs/source-map.json` | `_kos_now` · `save_chart_tab`(서비스 · 라우트) 해시 다시 잡음 · abstraction 에 캐시 어댑터 한 줄 |

## 테스트
- 새 `tests/day/board/test_board_loop2.py`(11): E3 연속 저장 2회 = 클라이언트 생성(= sign-in) 1회 · 읽기 2회 · `close_adapters` · C29 세 코드 글자 + 호출 `doctor_not_listed` 글자 그대로 · C28 세 장 presigned 3 · register 1 · 한 장 PUT 실패 = 그 장만 미반영 + 토스트 + 다시 시도 · 등록 실패 = 전부 미반영 · 검사에 걸린 장만 거절 / 전부 걸리면 400 · C30 `tick` 은 넣고 안 기다림 · `poll` 은 안 넣음 · C31 반영된 행 정리(DAY 올림 · KOS 가져옴 둘 다) · ref 없는 행 그대로 · DAY 가 먼저 지운 행 = C25 만 · 목록 실패 = 판정 안 함 · 목록 뒤 생긴 ref 안 지움
- 고침: `test_board_chart_conflicts.py` 409 `message`(C29) · `test_board_photo_import.py` payload `kosRemoved` · KOS 에서 지운 사진 = DAY 도 삭제(C31 — 앞 판 「그대로」 뒤집음)
- 가짜(`photo_support`): `fail_upload_at` · `register_calls` · `upload_many`

## 검증
- `scripts/test.sh -q backend/tests/day/board` — **286 passed**
- ruff check · format(backend · scripts) OK · mypy Success 605 files
- 무관(frontend): `backend/tests/architecture/test_web_rules.py::test_day_js_는_innerHTML_로_글자를_넣지_않는다` 실패 — frontend 가 고치는 중인 `day.js` 의 `photosTick`(`swap: "innerHTML"`) 문자열. 그 밖 architecture · devtools 520 passed

## 주의
- 브리프 「사진 탭 GET(그리고 poll)마다 작업을 넣는다」 — SPEC(SoT)은 `poll=1` 을 「다시 읽기 · 작업 안 넣음」으로 두고 10초 확인을 새 `tick=1` 로 정했다. SPEC 대로 했다(탭을 고를 때 = `poll` 없는 GET = 넣음 · 열린 동안 = `tick=1` = 넣음). FE 는 10초마다 `?tick=1` 을 보내야 한다.
- C28 에서 올리기 본문 전체 크기 한도를 없앴다(장 수 한도 없음 — 결정). 장당 5MB 는 서비스가 장마다 본다(Starlette 가 파일을 임시 파일로 흘림). 그래서 리뷰 P5(413 이 404 보다 먼저)는 이제 장당 검사로 404 뒤에 온다.
- C31 은 KOS 목록 응답이 완전하다는 데 기댄다(planner-fix-10 미결과 같음).
