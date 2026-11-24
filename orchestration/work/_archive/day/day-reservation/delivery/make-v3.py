import json, os
D = os.path.dirname(os.path.abspath(__file__))
BASE = "32b83390eb9fbdcd615f86ecad016b6e9c39ee74"
SRC = ("SPEC 원천 = DAY-SPEC-006(stable · 개정 ① ~ ⑪) · DAY-SPEC-000 2026-11-24 개정 · DAY-SPEC-002 개정 ㉗ — Mediness main "
       "32b83390(PR #958 머지 · spec-baseline ready). 구현 = Code PR CENTURION_DAY#272(dev 대상 · 1차 조회 + 원내 현황 + 담당자 줄 + 공지 수정 · 동기화 + 카드 배치 + 동행 그룹 · 세 Delivery 를 한 PR 이 덮음)")
DELTA = ("2026-11-24 재결속 — baseline = 머지된 Mediness main 32b83390(PR #958 · spec-baseline:pending 뗌). 범위 넓힘(사용자 결정 R42 ~ R75 · 코디 계약): "
         "계약 보충 v1 addendum 1 ~ 9(V1 today · open_min · time_gray_spans · 컨텍스트 이름 = 계약 이름 · 문구 근거 표 · 행 경합 = 날짜 쪽 양보(lock_timeout) · 꺾쇠 연타 debounce · 정원 null = 「30분」 · 잠금 전 Redis 10초 캐시 · 권한 행 = 데이터 migration) · "
         "v2 원내 현황 탭(R46 ~ R55 · 금액 = 수납 · 미수 · 결제총액) · v3 공지 수정 + KOS 공지 동기화(R58 ~ R62 · 누른 직원 토큰 직접 쓰기 · 503 kos_unavailable) · "
         "v4 동행 그룹 · 카드 배치(R64 ~ R73 · DAY 전용 새 테이블 · lane · line · rows · bands · 띠 = 진한 primary 테두리만 R75) · 「수납 필요」 = 단계 무관 payment_required(R42) · 다른 날짜 첫 화면 최대 3초 기다림(R43) · 담당자 줄(R56 · R57 · R63). "
         "나눔: #267 = 백엔드 조회 · 원내 금액 · 공지 저장 · 동행 쓰기 · 권한 키 셋 · migration 0018 ~ 0023 / #268 = 동기화(날짜 회차 · 공지 동기화 · 거래 매핑) / #269 = 화면(탭 · 카드 · 배치 · 끌어 놓기 · 공지 편집). 결과 계약이 바뀌어 재승인 대상")

V3 = ("계약 V3(화면 값 · 카드 `cards[]` — 2026-11-24 갱신): {`visit_id`, `group_id`, `start_min`, `end_min`, `lane`(0 ~ 4 · 줄 안 자리), `line`(0 ~ · 그 30분 행 안 몇째 줄), `companion_group_id`(없으면 null), `name`, `nationality`, `is_new`, `state`(예약 상태(취소 · 노쇼)를 먼저 보는 판정 = ①), "
      "`payment_due`(bool — 내원 단계와 상관없이 살아 있는 `visit_task.payment_required` 하나라도 · R42), 담당자 줄 값(상담 대기 · 진행 = 상담사 · 시술 대기 · 진행 = 담당의 · 없으면 「미정」 · 그 밖 단계 없음 — R56 · R57 · R63)} · ~~`stack_index`~~ 없앰(v4). "
      "+ `rows[]`{`start_min`, `end_min`, `lines`}(30분 행 · 전 열 공통) · `bands[]`{`group_id`, `column_id`, `start_min`, `line`, `lane_from`, `lane_to`} · `companion_editable`(오늘 · 앞날 ∧ `reservation.companion` edit). "
      "배치 순서 = 닫힌 카드 뒤 · 동행 그룹 카드 먼저(그룹 생긴 순 → 넣은 순) · 그룹 없는 카드(시작 → 생성) · 한 줄 최대 5 — 판정 = ①(R64 · R70 · R71 · R73) · 띠 색 · 툴팁 글자 · 모양은 ③")
V4 = ("계약 V4(화면 값 · 필터 · 패널 — 2026-11-24 갱신): `filter`(그대로 — 수를 세는 곳 = ① · ③ 은 다시 세지 않음) · `notice`{`id`(DAY notice id · 없으면 null), `content`(그 날짜 첫 공지 · 없으면 null), `editable`(date ≥ 오늘 KST ∧ `reservation.notice` edit), `date`}(v3) · "
      "`inhouse`{`chips[]`, `items[]`}(v2 — 대상 = 오늘 · 판정(대상 · cat · 배지 · 금액 · 순번) = ① · 화면은 칩으로 거르고 순번으로 줄 세우기만) · 예약 요청 칸 제목 「예약 요청」은 ③ 템플릿 글자")
V1 = ("계약 V1 보충(addendum 1 · 2): `today`(병원 현지 오늘) · `open_min`(그날 가장 이른 운영 시작 · 그룹 0개면 null) · `axis.time_gray_spans[]`(open_min 전 ∪ 오늘이면 지금 정시 전 · 지난 날이면 끝까지 — 계산 = ①) · 템플릿 컨텍스트 이름 = 계약 이름 그대로 최상위(`date` · `weekday` · `is_today` · `today` · `now_min` · `open_min` · `axis` · `columns` · `cards` · `rows` · `bands` · `filter` · `notice` · `inhouse` · `companion_editable`)")

def load(n): return json.load(open(os.path.join(D, f"request-{n}.json"), encoding="utf-8"))

def common(r):
    r["contract_version"] = 3
    r["spec_baseline_revision"] = BASE
    r["scope_delta"] = DELTA
    r["review_surface"][0] = SRC
    return r

def swap_v(lst):
    out = []
    for x in lst:
        if x.startswith("계약 V3("): out.append(V3)
        elif x.startswith("계약 V4("): out.append(V4)
        else: out.append(x)
        if x.startswith("계약 V1("): out.append(V1)
    return out

# ① be-read (#267)
r = common(load("be-read"))
r["title"] = "DAY 예약 현황 ① 백엔드 — 조회 · 원내 금액 · 공지 저장 · 동행 쓰기 · 권한 · migration 0018 ~ 0023 (DAY-SPEC-006)"
r["target_specs"] = ["DAY-SPEC-006", "DAY-SPEC-000", "DAY-SPEC-002"]
td = swap_v(r["target_delta"])
td = [x.replace("권한 키 reservation view — 모든 직무에 기본값 행(R31", "권한 키 reservation view — 모든 직무에 기본값 행 · 이미 있던 직무 = 데이터 migration `0018_reservation_permission`(R31 · R45") for x in td]
td += [
 "다른 날짜 첫 화면 = 그 날짜 최신화 끝 표시를 최대 3초(설정) 기다린 뒤 그림 · 넘거나 실패면 지금 사본(R43 · R30) · 10초 안에 받은 날짜는 안 기다림",
 "원내 현황(계약 v2 · R46 ~ R55): 오늘 방문 중 접수 ~ 귀가 대기 · 칩 · 정렬 순번 · 「수납 필요」(R42) · 「수납 완료」(R48 · R55) · 금액 수납(거래 합 − 선불카드 차감) · 미수(R50 · R54 정정 · 옵션가 + VAT) · 결제총액 = 합(R51) — 판정은 서버(`policies/reservation_amounts.py` · `policies/reservation_inhouse.py`)",
 "담당자 줄(R56 · R57 · R63): 상담사 = 원내 현황 상담 실장과 같은 판정 · 담당의 = 시술 현황 담당의 판정 · 시작 순으로 담당의가 정해진 첫 줄 · 없으면 「미정」",
 "공지 저장(계약 v3 · R58 ~ R62): `PUT /reservations/notice`(form date · content · notice_id) — 누른 직원 KOS 토큰으로 KOS 공지 create / change-content / delete 를 그 요청 안에서 직접 부름(쓰기 큐 안 씀) · 저장 뒤 그 날짜 다시 읽어 DAY `notice` · `external_ref(entity_type = notice)` 맞춤 · 200 공지 조각 · 400 · 403(`reservation.notice` edit) · 409 notice_past_date · 409 kos_rejected · 503 kos_unavailable",
 "동행 쓰기(계약 v4 · R65 ~ R73): `PUT /reservations/companions`(visit_id · target_visit_id — 묶기 · 옮기기) · `PUT /reservations/companions/leave`(visit_id — 풀기) · DAY 에만 · KOS 를 부르지 않음 · 검사 순서 400 → 404 → 409 companion_past_date(끈 · 놓은 카드 둘 다 지난 날 아님) → 409 companion_condition(같은 날 KST ∧ 같은 열 ∧ 같은 30분 행 ∧ 닫힘 아님) · 바꾸기 전에 전부 · 1명 남으면 그룹 없음 · 자동 빠짐(R67) 정리 함수 · event_log companion_join / companion_leave · 나중 저장이 이김 · 200 = #reservation-main 조각",
 "권한 키 셋(DAY-SPEC-002 개정 ㉗): `reservation` view · `reservation.notice` edit · `reservation.companion` edit — 기본 모든 직무 · 이미 있던 직무 = 데이터 migration(0018 · 0021 · 0023)",
 "migration 0018 ~ 0023(dev `0017_ext_catalog` 뒤 · DAY-SPEC-000 2026-11-24 개정): 0018 reservation 권한 · 0019 `purchase_transaction.status` + spent · requested · failed · 0020 `ix_purchase_visit_id` · `ix_visit_task_visit_id` · 0021 공지 권한 · 0022 `companion_group` · `companion_member`(부분 유일 visit_id) · 0023 동행 권한",
]
r["target_delta"] = td
r["acceptance"] = [a.replace("A4: SPEC-006 케이스 매트릭스(401 · 403 · 400 날짜 형식 · 그룹 0 · 예약 0 · 취소 · 노쇼 · 수납 필요 귀가 대기만 · 정원 구역 0 / 2+ = 비움)", "A4: SPEC-006 케이스 매트릭스(401 · 403 · 400 날짜 형식 · 그룹 0 · 예약 0 · 취소 · 노쇼 · 수납 필요 = 단계 무관 R42 · 정원 null = 「30분」 · 6건 이상 줄 접기)") for a in r["acceptance"]]
r["acceptance"] += [
 "A6: 원내 현황 금액이 R52 실측 기준값(수납 451,000 · 미수 66,000 · 결제총액 517,000 / 수납 0 · 미수 110,000 · 110,000 / 선불카드 정리 날 0 · 0 · 0)을 fixture 테스트로 재현하고 칩 · 정렬 · 배지가 계약 v2 대로",
 "A7: 공지 저장 — create / change-content / delete 분기 · 저장 대상 고르기(R62 ②) · 403 · 409 · 503 · 저장 뒤 다시 읽기 실패 = 방금 저장한 글 — KOS 가짜 어댑터 테스트",
 "A8: 동행 — 묶기 · 옮기기 · 풀기 · 1명 남음 · 자동 빠짐 · 검사 순서와 409 두 갈래(지난 날 하나만 · 날짜 다름 포함) · 바꾸기 전 전부 검사 · event_log 두 줄 · 배치(lane · line · rows · bands) 순서 R73 — 테스트",
 "A9: migration 0018 ~ 0023 upgrade → downgrade → upgrade 왕복 · `alembic heads` 하나 · 권한 데이터 migration 은 기존 행을 건드리지 않음",
]
r["non_goals"] = [
 "화면 템플릿 · day.js(Delivery ③)",
 "중앙 날짜 최신화 작업 · 공지 동기화 · 거래 매핑(Delivery ②)",
 "예약 등록 · 변경 · 상세 모달 · 예약 요청 내용 · 근무표(R1 ~ R5 · R15)",
 "0018 ~ 0023 밖의 새 테이블 · 칸 · migration · `visit` 칸 추가",
 "원내 현황 · 시술 현황의 동행 표시(R68)",
 "직원 앱 JSON",
]
r["review_surface"] += ["공지 저장이 KOS 결과를 기다리는 유일한 쓰기인지(R59) · 동행은 KOS 를 부르지 않는지(R65)", "금액 판정이 R49 ~ R55 와 같은지", "migration 번호 · revision 이 dev 0017 뒤로 이어지는지"]
ex = r["execution"]
ex["code_surface"] = [
 "backend/day/routers/reservations.py", "backend/day/services/reservations.py · reservation_notice.py · reservation_companions.py",
 "backend/day/queries/reservations.py · reservation_inhouse.py · reservation_staff.py",
 "backend/day/policies/reservations.py · reservation_layout.py · reservation_amounts.py · reservation_inhouse.py · reservation_staff.py · permissions.py",
 "backend/day/presentation/reservations.py · reservation_inhouse.py", "backend/day/dtos/reservation.py · reservation_inhouse.py",
 "backend/day/models/companion.py", "backend/day/emr/kos/notices.py(공지 쓰기 · 읽기)", "backend/day/services/default_permissions.py", "backend/day/menu.py",
 "backend/migrations/versions/20261123_0018 ~ 0023_*.py",
]
ex["domain_candidates"] = ["reservation_group · capacity · timetable · day_off · visit · customer · visit_task · purchase · purchase_item · purchase_transaction · notice · external_ref · companion_group · companion_member · job_role_permission · event_log"]
ex["dependencies"] = ["② #268 — 계약 T · 공지 동기화 · 거래 매핑만 맞추면 병렬", "③ #269 — 계약 S · V0 ~ V4 · v2 ~ v4 만 맞추면 병렬", "세 Delivery 가 한 Code PR #272 로 들어감 · 실물 e2e 는 그 PR 에서"]
ex["phases"] = ["P1 권한 키 · 기본값 행 · migration 0018", "P2 조회 service · view model", "P3 화면 라우트 · 최신화 요청 넣기 · 3초 기다림", "P4 원내 현황 · 담당자 줄 · migration 0019 · 0020", "P5 공지 저장 · migration 0021", "P6 카드 배치 · 동행 쓰기 · migration 0022 · 0023", "P7 테스트 · 실물 e2e"]
ex["verification"] = ["backend pytest(조회 · 권한 · 케이스 매트릭스 · KOS 호출 0 · 요청 넣기 횟수 · 원내 금액 · 공지 · 동행 · migration 왕복)", "실물 e2e(로컬 · KOS 데모)"]
ex["rollback"] = ["Code PR revert + alembic downgrade 0023 → 0017(권한 행 삭제 · 동행 두 테이블 삭제 · 두 인덱스 삭제 · 0019 downgrade 는 spent · requested · failed 거래 행을 지움 — 다음 구매 동기화가 매핑 밖으로 다시 뺌)"]
json.dump(r, open(os.path.join(D, "request-v3-be-read.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ② be-refresh (#268)
r = common(load("be-refresh"))
r["title"] = "DAY 예약 현황 ② 백엔드 — 동기화: 다른 날짜 최신화 · 공지 동기화 · 거래 매핑 (DAY-SPEC-006)"
r["target_specs"] = ["DAY-SPEC-006", "DAY-SPEC-000"]
r["target_delta"] += [
 "행 경합 = 날짜 쪽이 양보(addendum 4): 날짜 반영 transaction 에 짧은 잠금 대기 상한(`SET LOCAL lock_timeout` · 설정) · 고객 행 정렬 순서 · 부딪히면 날짜 쪽 error(중간 상태 없음) · 오늘 회차 그대로",
 "잠금 전 Redis 10초 캐시(addendum 8): (병원 · 날짜) 「최근 10초 안에 최신화함」 표시가 있으면 task 도 잠금도 안 함 · 최신화 시작 때 세움 · 실패면 지움 · 「병원당 동시 1개」는 없음 · 최신화 끝 표시는 ① 의 3초 기다림(R43)이 읽음",
 "공지 동기화(R60 · R62): 오늘 = 10초 일정 회차 · 다른 날짜 = 날짜 최신화 회차에 KOS `get-notices`(그 날 · deleted:false)를 붙여 DAY `notice` 를 그 날짜 통째로 맞춤 · KOS id = `external_ref(entity_type = notice)` · 실패는 따로(회차를 오류로 만들지 않음 · 이전 사본 · 경고 로그) · C1 묶음 밖",
 "거래 매핑 넓힘(R53 · DAY-SPEC-000 2026-11-24 개정): 상태 SPENT · REQUESTED · FAILED · 수단 PLATFORM · EASY_PAY · MEDICAL_LOAN — 오늘 구매 회차 · 날짜 최신화가 같은 매핑(enum 값 추가 migration 0019 는 ① #267)",
 "동기화 뒤 동행 정리(R67): 일정 반영 뒤 조건이 깨진 동행 멤버를 빼는 정리 함수(① #267 제공)를 부름 · 실패는 회차 오류 아님",
]
r["acceptance"] += [
 "A7: 공지 동기화 — 오늘 회차 · 날짜 회차가 그 날짜 공지를 통째로 맞추고(추가 · 수정 · 지움) 공지 실패가 일정 회차를 실패로 만들지 않는다 — 테스트",
 "A8: 거래 상태 5값 · 수단 7종이 행을 빼지 않고 저장된다 · 7종 밖 값은 그 행을 뺀다 — 매퍼 테스트",
 "A9: Redis 10초 캐시 · lock_timeout 양보 — 10초 안 두 번째 요청 = task 0 · 경합 시 날짜 쪽 error · 중간 상태 없음 — 테스트",
]
r["non_goals"] = [n for n in r["non_goals"] if not n.startswith("공지")] + ["공지 쓰기(① #267)", "기준 정보 동기화 변경"]
r["non_goals"] = [n.replace("새 테이블 · 칸 · migration", "새 테이블 · 칸 · migration(migration 은 ① #267)") for n in r["non_goals"]]
ex = r["execution"]
ex["code_surface"] = ["backend/day/tasks/emr.py(`day.sync_reservation_date_hospital` — 계약 T)", "backend/day/services/emr_date_sync.py(새 — 날짜 회차 · 잠금 · 캐시)", "backend/day/services/emr_sync.py", "backend/day/emr/sync_notices.py · emr/kos/mapper_notice.py · emr/normalized_notice.py(공지 동기화)", "backend/day/emr/kos/mapper_sale_values.py(거래 매핑)", "backend/day/emr/sync_references.py", "backend/common/config.py(lock_timeout · 캐시 · 기다림 설정)"]
ex["dependencies"] = ["① #267 — 계약 T · 동행 정리 함수 · migration 0019 만 맞추면 병렬", "세 Delivery 가 한 Code PR #272 로 들어감 · 실물 e2e 는 그 PR 에서"]
ex["phases"] = ex["phases"] + ["P5 공지 동기화(오늘 · 날짜)", "P6 거래 매핑 넓힘 · Redis 10초 캐시 · lock_timeout 양보"]
ex["verification"] = ["backend pytest — C1 · C2 · C3 · 동시 요청 · 오늘 회차 회귀 · 공지 동기화 · 거래 매핑 · 캐시 · 양보", "실물 e2e(로컬 · KOS 데모)"]
ex["rollback"] = ["Code PR revert — 이 Delivery 몫 migration 없음 · 받아 둔 다른 날짜 행 · 공지 사본은 다음 동기화와 같은 모양이라 남아도 무해"]
json.dump(r, open(os.path.join(D, "request-v3-be-refresh.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ③ fe (#269)
r = common(load("fe"))
r["title"] = "DAY 예약 현황 ③ 화면 — 탭 · 카드 · 배치 · 끌어 놓기 · 공지 편집 (Jinja2 + HTMX · day.js · DAY-SPEC-006)"
r["target_delta"] = swap_v(r["target_delta"]) + [
 "오른쪽 패널 탭 「공지 / 예약」 · 「원내 현황」(R46 · 기본 = 공지 / 예약) · 원내 현황 카드 = 시안 `stageCard`(이름 · 배지 · 단계 · 접수 = 예약 일시 / 국적 · 상담 실장 줄 「미정」 · 금액 세 줄) · 칩으로 거르고 `order_*` 로 줄 세움 · 빈 목록 「해당하는 고객이 없어요」 · 고른 탭 · 칩은 폴링 · 날짜 이동 뒤에도 유지(계약 v2 · R47 · R48 · R56)",
 "표 카드 담당자 한 줄(R57) · 「수납 필요」 = V3 `payment_due` 그대로(R42) · 정원 null 열 머리 = 「30분」만(addendum 7)",
 "배치(R64 · R70 · R71): 카드 폭 140 · 한 줄 최대 5 · 시간 행 높이 = `lines` × 70 · 카드 높이 한 줄 고정 66 · top = 행 top + `line` × 70 — 받은 값으로만 그림",
 "끌어 놓기(계약 v4 · R66 · R69): `companion_editable` 일 때 카드 끌기 → 다른 카드 위 = 묶기 PUT · 띠 밖 빈 곳 = 풀기 PUT · 같은 그룹 위 / 그룹 없는 카드 빈 곳 = 요청 없음 · 끄는 동안 폴링 미룸 · 실패 = 제자리 + 시술 현황과 같은 oob 토스트(R71) · 띠 = 진한 primary 굵은 테두리만 · 글자 없음(R75 — R72 꼬리표 · R74 책갈피 뒤집음)",
 "공지 편집(계약 v3 · R58): 「수정하기」(editable 일 때 · 날짜 오른쪽) → 제자리 textarea + 글자 수(2,000) + [취소] · [저장] · 편집 중 폴링이 공지 칸을 덮지 않음 · 성공 「공지를 저장했어요」 · 실패 = 글 그대로 + 「저장하지 못했습니다」 · 「다시 시도」",
 "꺾쇠 연타 debounce(addendum 6): 마지막으로 멈춘 날짜만 요청 · 문구 근거 표 `tests/architecture/test_screen_copy.py` 는 시안 글자만 · 행마다 시안 줄 번호(addendum 3)",
]
r["acceptance"] += [
 "A5: 원내 현황 탭 · 칩 · 정렬 · 카드 · 빈 상태 · 탭 유지가 계약 v2 가짜 값으로 렌더 · DOM 테스트",
 "A6: 끌어 놓기 — 묶기 · 풀기 · 요청 없음 두 경우 · 실패 제자리 + oob 토스트 · 끄는 동안 폴링 미룸 · 띠에 글자 없음 — DOM 테스트",
 "A7: 공지 편집 — 수정하기 보임 조건 · 글자 수 · 취소 · 저장 성공 · 실패 · 다시 시도 · 편집 중 폴링이 덮지 않음 — DOM 테스트",
 "A8: 배치 — rows · lines · lane · line 으로 행 높이 · 카드 top · 6번째 카드 아래 줄 · debounce 마지막 날짜만 — DOM 테스트",
]
r["non_goals"] = [
 "백엔드 조회 · 공지 저장 · 동행 쓰기 · 권한(Delivery ①) · 동기화(Delivery ②)",
 "카드 누르기 동작(끌기 밖) · 상세 모달 · 예약 요청 내용 · 근무표 · 고객 검색 · 고객 등록(R1 ~ R5 · R15 · R33)",
 "원내 현황 · 시술 현황의 동행 표시(R68)",
 "낡음 표시(OQ-R21 · 2루프)",
]
ex = r["execution"]
ex["code_surface"] = ["backend/day/templates/reservations.html", "backend/day/templates/partials/reservations_main.html · reservations_notice.html · reservations_parts.html", "backend/day/static/day.js · day.css", "backend/day/styles/app.css", "backend/day/templates/ui.html · icons.html", "scripts/frontend/tests/res-*.test.mjs(DOM 테스트)", "backend/tests/architecture/test_screen_copy.py(문구 근거 표 — addendum 3)"]
ex["dependencies"] = ["① #267 — 계약 S · V0 ~ V4 · v2 ~ v4 만 맞추면 가짜 값으로 병렬", "세 Delivery 가 한 Code PR #272 로 들어감 · 실물 e2e 는 그 PR 에서"]
ex["phases"] = ex["phases"] + ["P5 원내 현황 탭 · 담당자 줄", "P6 공지 편집", "P7 배치 · 끌어 놓기 · 띠"]
ex["verification"] = ["템플릿 렌더 테스트(pytest) · CSP 검사 · DOM 테스트(scripts/frontend/tests)", "실물 e2e(로컬 · KOS 데모) · 시안 대조"]
json.dump(r, open(os.path.join(D, "request-v3-fe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
