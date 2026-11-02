# WORK-001 WP7 결과 보고 — SPEC 0.2.0: 단계 단위 배정 · 조작 API · 5직군 · 개원 전 시드 · 메모 공개 시점 · KOS 주석

## 상태: done

## 수행 — 파일·모듈 목록

`cc/back/` 만 고쳤다. 커밋 없음. 통역(WS)은 건드리지 않았다.

| 파일 | 변경 |
|---|---|
| `app/domain/board.py` | **새로 씀.** 상태 = customers · steps · staff · resv · log · stepSeq. 방 · 고객 상태 계산(`status_of`, §5.1 문구) · `commit`(상태가 바뀐 고객만 경과 리셋) · 조작 11개(check_in · place · move_sleep · return_room · assign · unassign · add_procedures · reorder · start · finish · discharge) · 막는 조건 · flowStep 전이 · log · **조작마다 §9 KOS 주석**(호출 코드 없음) |
| `app/domain/rooms.py` | 「라운지」→ **접수대기실**(id `reception`) · 「수면실」→ **수면시술실** · `is_treatment_room` |
| `app/service/board_service.py` | 새로 씀 — 읽기(board · 직원 「지금 일」) · 조작 → commit → 저장 → version+1 → SSE · undo(마지막 1개) · reset · snapshot |
| `app/service/staff_service.py` | 로그인 목록(데스크 + 5직군, `frame`) · home 배정형(current · next[] · done[]) / 순회형(내원 목록 · 손 필요 · 오늘 시술) |
| `app/service/patient_service.py` | 환자 상세 §3.4(메모 공개 시점 · 작성자 이름 없음 · 「이전 시술 기록 없음」 제거 · `myActions`) · **시술 후보 §5.4** |
| `app/service/memo_parse.py` | 값 없는 양식 줄 숨김(`고민:` · `H)` · 빈 번호 `1.`) |
| `app/service/snapshot.py` | 시각 필드 일반화(customers · steps · log) |
| `app/seed/build.py` | **개원 전 시드**(예약만) · 5직군(`kos-staff.json` roleTags, §4 규칙) · 0.1.0 재구성 코드 제거. 이름 치환 · 참조 데이터는 그대로 |
| `app/seed/__main__.py` | `build --date` 만(`--at` 없앰) · `CC_KOS_STAFF_PATH` |
| `app/repository/*` | 테이블 `step` · `log` (0.1.0 `history` 대체) |
| `app/api/desk.py`(새) · `board.py` · `staff.py` · `patients.py` · `schemas/requests.py` · `main.py` · `config.py` | §5.2 · §5.3 경로. **0.1.0 `/api/board/*` 조작 경로는 없앰**(`GET /api/board` 만 남음) |
| `.env.example` | `CC_KOS_STAFF_PATH=data/kos-staff.json` 추가 |
| `README.md` | 0.2.0 API — **값 사전 · 응답 예시(board · staff · login · home 두 틀 · patient · candidates) · 조작 표(요청 본문 · 막는 조건 code)** — WP8 이 `types.ts` 를 맞출 기준. 예시 이름은 「의사A」·「상담사A」 꼴(실명 안 씀) |
| `tests/` | `test_flow.py`(§11) · `test_privacy_memo.py` · `test_kos_comments.py` · `helpers.py` · `conftest.py` 새로 · `test_events.py` 수정 · 0.1.0 시험 4개 삭제 |
| `data/seed.json` | `seed build --date 2026-10-09` 로 0.2.0 형식으로 다시 만듦(이전 것은 `seed.20261013-160724.json`). **같은 명령이 `data/cc.db` 도 채웠다** |

## 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| `CC_CAPTURE_DIR=<캡처> uv run pytest` (cc/back) | **41 passed**(새 0.2.0 시험 14 · 통역 16 · SSE 1 · …) — 모두 **임시 DB**(사용자 `data/cc.db` · `seed.json` 안 씀) |
| `uv run ruff check .` | **All checks passed** |
| `seed build --date 2026-10-09` | 예약 27(취소 1) · 고객 0 · 단계 0 · 로그 0 · 직원 17 = 의사 4 · 상담사 3 · 피부관리사 3 · 간호사 4 · 코디 3 |
| KOS 주석 | 조작 함수 11개 **전부** 주석 있음(블록 17개 — assign 은 단계 종류별 4, start · finish 는 2씩). 시험이 「Op 를 돌려주는 공개 함수 = OPERATIONS = 주석 있는 함수」를 확인 |
| KOS 호출 코드 | **0** — `app/` 코드 줄(주석 제외)에 `kos-solution.com` · `exchange-token` · `/queries/` · `/commands/` 0건, HTTP 클라이언트 import 는 통역(`interpret/soniox.py`)뿐(시험) |
| 기능 폴더 밖 import · 사용자 포트 | 없음 · 8600(pid 78960, 옛 코드로 떠 있음)은 건드리지 않음 |

§11 대응(API 시험, 화면 빼고):
1. `test_1_seed_is_before_opening` — 예약만, 고객 · 직원 일 비어 있음, 방 이름 변경. 응답 전체 실명 · 이메일 0(`test_no_real_names_emails_phones` — 모든 예약 접수 뒤 board · staff · 직원 17명 home · 환자 27명 상세 · 후보 27개 전부, 실명 331개 원문 · 정규화 대조 → 고객 자리 0, 직원 이메일 0, `chartNumber`·`dateOfBirth`·`phoneNumber`·`email` 키 0)
2. `test_2_first_visit_consult_flow_reveals_memos` — 접수(상담) → 접수대기실 → 방 → 상담사 배정 → **상담사 home `next` 에 뜸** → 시작 · 종료 → 오더 · 상담 메모가 이때 열림(전에는 `order`·`consult` null)
3. `test_3_procedures_reorder_assign_start_finish` — 후보 3개 추가 → 순서 바꾸기 → 원장 상담 종료 「원장 대기 · 세팅 준비」 → 시술1 의사 A 시작 · 종료 → 「다음 단계 대기」 · 순회형 `need: next` → 시술2 피부관리사 시작 · 종료
4. `test_4_sleep_room_holds_original` — 수면시술실 이동 → 원래 방 `room_held` → 원래 방으로
5. `test_5_discharge_midway_skips_rest` — 남은 단계 `skipped` · 방 비움 · log 에 「진행 안 함」 2줄 + discharge
6. `test_6_revisit_candidates_include_tickets` — ⚠ 아래 이슈 1
8. `test_kos_comments.py`
- 그 밖: 막는 조건 · undo(`test_blocks_and_undo`) · reset · save(`test_reset_and_save`) · 5직군 로그인 · 틀(`test_7…`) · 작성자 이름 없음 · 빈 양식 줄 없음 · `**` 원문 유지 · 「이전 시술 기록 없음」 없음 · 주의 공개 시점

## 계약 대조 — SPEC-001 0.2.0

| 항목 | 판정 | 비고 |
|---|---|---|
| §4 5직군 · 복수 태그 규칙 · 마취용 제외 · 그날 나온 직원만 · 이메일 없음 | 같음 | 「나온 칸」= 작업 의사(+호출 의사) · 상담 기록 상담사(+상담 의사) · 작업 담당 · 기타 업무. **예약 담당(`reservationAssignee`)만으로 나온 4명은 뺐다**(§4 ① 목록에 없는 칸) |
| §5.1 상태 모델 · 방 상태 문구 · 경과 · flowStep | 같음 + 정한 것(이슈 2) | 응답에 `status{key,label,need}` · `steps` 를 고객 안에 넣었다 |
| §5.2 읽기 6개 | 같음 | `GET /api/patients/{id}?staffId=` 로 버튼(`myActions`). board 에 `now` · `corridors`, staff 에 `work`(지금 일) |
| §5.3 조작 12개 · 막는 조건 400 · `{version}` · SSE · log | 같음 | 경로 · 본문 그대로. 막는 조건마다 `code`(README 표). 없는 id 는 404 |
| §5.4 후보 | 같음 | 작업(PROCEDURE · ETCETERA) + 보유 시술권, `ticketId` 겹치면 하나, 동선에 들어간 것 제외. `source`(task/ticket) · ETCETERA 의 `kosTitle` 추가 |
| §3.4 메모 공개 · 작성자 없음 · 시술 이력 · `**` · 빈 양식 줄 | 같음 | |
| §6 개원 전 시드 · reset · save | 같음 | |
| §7 로그인 | 같음 | `frame` 추가(desk · assigned · rounds) |
| §9 주석 | 같음 + 3개 | 표에 없는 move-sleep · return-room(「방: 공개 없음 — KOS 요청」) · unassign(「공개 없음 — KOS 요청(담당자 · 집도의 해제)」) |
| §10 `CC_KOS_STAFF_PATH` | 같음 | |
| 현장 접수(0.1.0 addendum `scheduleId:null`) | **없앰** | 0.2.0 §5.3 check-in 은 `scheduleId` 필수 |

## 이슈 · 코디가 확인할 것

1. **§11-6 재내원 고객 — 10-09 에 보여 줄 고객이 없다.** 10-09 재방문(`isNew=false`)은 **취소된 테스트 행 1건뿐**이라 접수할 수 없다. API 쪽(보유 시술권이 후보로 나옴 · 작업과 겹치면 하나 · 접수하면 동선에 들어감)은 보유 시술권이 있는 첫 방문 고객(1명)으로 시험했다. 기본 체크(재내원 → 후보 전부)는 front 몫이고, 시연에서 보이려면 데이터 결정이 필요하다(다른 날 고객을 넣을지 · 이 시나리오를 뺄지)
2. **SPEC 에 없어서 정한 것**(최소로):
   - 첫 단계가 미배정인 고객(방에 막 들어옴)의 방 상태 = 「다음 단계 대기」(`need: next`). 단계가 없거나 다 끝나면 「귀가 대기」
   - flowStep: 방에 넣을 때 상담 단계가 없으면 RECEPTION 그대로 · 상담사 상담 종료(남은 단계 있음)와 시술 종료(남은 단계 있음)는 바꾸지 않음(SPEC 표에 있는 전이만)
   - 메모 공개: **접수 전**에는 오더 · 상담 메모를 숨김(상담 단계 유무를 아직 모름)
   - 방에 넣기는 접수대기실 → 관리실 · 2인관리실만(시안 freeRooms). 수면시술실 이동은 관리실에서만. 순서 바꾸기는 단계 전부 또는 남은 단계 전부를 받음. 접수 때 단계 0개 허용
   - 상단 카드 상담실장 · 원장 = **관제 배정**(KOS `consultation.counselor` · 작업 의사는 하루 끝 값이라 개원 전 시드에서 미래를 보여 줌)
3. **차트 「오늘 결제」 · 「서비스(0원)」는 처음부터 보인다** — KOS 하루 끝 결제 품목이라 개원 전 시드에서도 그날 결제가 보인다(결제 시각을 관제가 모름). 숨길지 정할 것
4. `data/cc.db` — 지시대로 `seed build` 가 다시 채웠다. **8600 서버는 옛 코드로 떠 있어 재시작 전에는 응답이 깨진다**(코디 재시작 예정). 옛 `history` 테이블은 남아 있지만 안 쓴다
5. **WP8 front 가 바꿔야 할 것**: 조작 경로 `/api/desk/*` · 단계 단위 모델(`customers[].steps` · `stepId`) · 직원 `frame` · home 두 틀 · `location`(`reception`) · `status` · `myActions` · 시술권 `tickets[]` 는 `{name,left,total}` 만(0.1.0 의 `expires`·`role`·`sleep` 추정값 삭제). README 에 예시
6. api-source-audit 의 추정 22개 중 남은 것: 직원 직군은 이제 KOS 태그(복수 태그는 §4 규칙) · 경과 · 동선 · 위치는 관제 조작 값(추정 아님). 예약 탭 시술 · 원장은 KOS 칸 그대로 빈 값
