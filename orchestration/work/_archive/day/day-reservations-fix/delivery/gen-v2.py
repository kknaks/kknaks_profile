import json
SRC=("[계약 원천] mediness draft PR #971 브랜치 kknaksss/day-reservations-fix-spec ad317cf4f2e3c6124331db90c09c178697f2131e(+ Delivery 발행 커밋 99085866 — 30-work Spec Coverage · log) — 문서 검수 review-doc-1 ~ 4 반영 · 미머지(구현 끝난 뒤 사람이 머지). 이 Issue 의 baseline = origin/main b9ac374e — CLI 가 main 판 target SPEC 이 stable 이라 spec-baseline:ready 로 정함 · 그러나 main 판 DAY-SPEC-006 · 007 · 000 · 002 · 003 은 개정 전이라 계약의 근거가 아니다 · #971 머지 뒤 같은 idempotency key · 다음 contract_version · 새 main SHA 로 재결속.")
CONTRACT=("[BE ↔ 웹 · 앱 계약 — 세 Delivery 공통 · 이름 고정 · 세 Issue 에 같은 글자] "
"① 배치 값(DAY-SPEC-006 Functional Rule 15 ⓐ ~ ⓙ — 살아 있는 배치 정의는 이것 하나): 예약 판 값(웹 조각 렌더 값 · 앱 `GET /api/reservations?date=` · 스트림 같은 값)에 "
"`rows[] {start_min, end_min, lines}`(오픈 시각 `open_min` 부터 1시간 행 · 오픈 전 예약 있으면 1시간씩 앞으로 · 마감 뒤 24:00 까지 · 정각 아닌 오픈 = 오픈 시각 경계 · 마지막 행 24:00 자름) · "
"`cards[] {lane(0 ~ 4), line(0 ~), start_min, end_min}` · "
"`bands[] {group_id, column_id, start_min, end_min, line, lane_from, lane_to}`(동행 띠 = 멤버를 다 감싸는 상자 — start_min = 멤버 가장 이른 시작 · end_min = 멤버 가장 늦은 끝 · 행을 넘으면 ⓖ 그림 규칙 · DAY-SPEC-006 U-9 · OQ-R43 닫힘). "
"놓는 순서 = 시작 시각 → 같은 시작이면 R73 · 동행 = 이웃 자리 · 이어진 빈 자리 첫 묶음(OQ-R43) · 그 시각에 겹치지 않는 가장 앞 자리 · 한 줄 5 자리 넘치면 그 행 아래 줄 · 행을 넘는 카드 = ⓖ(지나는 아래 줄 띠도 덮고 찬 자리로 셈 · 아래 줄 카드는 행 끝 자름) · `rows[].lines` = 그 행 어느 열이든 가장 큰 line + 1(전 열 공통) · 열 폭 = 한 줄 자리 수 최댓값(최대 5) × 카드 폭 + 사이 + 왼쪽 여백 + 오른쪽 70. "
"앱 JSON 은 camelCase(Row `startMin` · `endMin` · `lines` / Card `startMin` · `endMin` · `lane` · `line` / Band `groupId` · `columnId` · `startMin` · `endMin` · `line` · `laneFrom` · `laneTo` — Band `endMin` 새 칸). 화면은 받은 값으로만 그리고 다시 계산하지 않는다 · 픽셀(1시간 행 기본 높이 = 웹 140px · 앱 지금 30분 칸 × 2 · 카드 폭)만 화면마다(ⓗ). "
"② [+] 툴팁용 열 값: 웹 = 열 `title` · `interval_minutes` · 앱 JSON = 기존 Column `title` · `intervalMinutes`(새 칸 없음). "
"③ 예약 상세: 웹 · 앱 상세 `questionnaire.expired: bool`(DAY-SPEC-007 앱 JSON 짝 · 그 고객 마지막 살아 있는 `questionnaire_history` 가 기간(env · 기본 6개월 · KST 날짜 + n 달력 개월 D49) 밖이면 true · 행 없음 = `questionnaire` null) · 웹 · 앱 글자 「6개월 경과」(결정 글자 · 새 문구 아님) · [문진 QR] 보이기(`actions.questionnaireQr`)도 같은 조건. "
"④ 팝오버: 기기 목록 = `GET /reservations/visits/{visit_id}/display-targets?kind=`(지금 구현 · DAY-SPEC-007 API 표) · 요청 만들기 = `POST /reservations/visits/{visit_id}/display-requests`(form `kind` · `device_id` — [문진 QR] 「링크 복사하기」 · 「링크 열기」 = device 없는 요청 · 열린 링크 요청 있으면 다시 씀(D44) · 기기 줄 = 앞 요청 취소 → 새 요청 · [여권 스캔] = 기기 줄만 · 기기 줄 모양 = 기기명 · 점(초록 연결 · 빨강 미연결) · 상태 · 미연결 줄도 보이고 누름 · **고르면 그때 요청 생성** — 버튼 누름만으로는 요청 없음 · DAY-SPEC-007 규칙 2 · 7 · 케이스 고침 8 줄). "
"⑤ F6: 상세를 그리는 모든 경로가 같은 origin 을 넘겨 진행 값(`displays[].qrUrl`)이 같다(DAY-SPEC-007 규칙 9).")
SCOPE="2026-11-27 v2 — Delivery 검수 review-delivery-1 WARN D1 ~ D9 반영(승인 전 · v1 승인 없음): 공통 계약 ① bands[] (end_min) · 동행 이어진 빈 자리 · ② 열 칸 이름 고정 · ④ 기기 줄 모양 · [계약 원천] 상태 말 하나로(ready) · BE R71 동행 판정 30분 분리 · origin 하나 · 다시 보내기 대상 · 웹 누르기 · 놓기 30분 단위(코디 기본값) · 앱 30분 전제 자리 · 입구 파일 보충. SPEC 본문 변경 없음."
def load(n): return json.load(open(f"{n}-request-v1.json"))
def common(d):
    d["contract_version"]=2; d["scope_delta"]=SCOPE
    d["target_delta"][0]=SRC; d["target_delta"][1]=CONTRACT
    d["review_surface"][0]=SRC; d["review_surface"][1]=CONTRACT
def rep(lst,i,old,new):
    assert old in lst[i],(old,lst[i][:80]); lst[i]=lst[i].replace(old,new)
# BE
be=load("wp1-be"); common(be); td=be["target_delta"]; ac=be["acceptance"]; ex=be["execution"]
i=[k for k,x in enumerate(td) if x.startswith("배치 값")][0]
td[i]+=" · **R71 동행 판정(`can_join` · `valid_members` — `policies/reservation_layout.py:75-87` · `:115-116` `_row` · `:29` `ROW_MINUTES` · `services/reservation_companions.py:31`)은 30분 그대로 — 배치 행(60분)과 함수 · 상수를 나눔**(R71 = 같은 30분 행 · DAY-SPEC-006 U-9 그대로) · 띠 값 `bands[]` 에 `end_min`(멤버 가장 늦은 끝)을 더함(앱 Band `endMin`)."
i=[k for k,x in enumerate(td) if x.startswith("F6")][0]
td[i]+=" · `public_origin` 이 두 벌(`routers/reservation_displays.py:46` · `routers/api/displays.py:55`) — 하나로 모으거나 두 함수가 같은 값임을 테스트로 고정 · 앱 상세 `routers/api/reservations.py:104` 도 그 값."
i=[k for k,x in enumerate(td) if x.startswith("문진 6개월")][0]
td[i]+=" · 고객 단위로 바꾸면 다시 보내기(`services/questionnaire_kos.py:146-158` 「그 방문 마지막 행」)는 **제출 행만** 대상(`source = read` 행 제외)."
rep(ac,0,"mypy 가 origin 없는 호출을 잡음","mypy 가 origin 없는 호출을 잡음 · origin 함수 하나(또는 두 `public_origin` 같은 값 테스트)")
rep(ac,1,"같은 시작 R73 · 동행 이웃)","같은 시작 R73 · 동행 이웃 = 이어진 빈 자리 첫 묶음 · 띠 `bands[]` start_min ~ end_min = 멤버 가장 이른 시작 ~ 가장 늦은 끝) · **R71 동행 판정은 30분 그대로 — 1시간 행 안 30분 경계를 넘는 두 카드(예: 12:10 · 12:40)는 묶이지 않음 · 자동 빠짐도 30분 기준**")
rep(ac,3,"[문진 QR] 보이기 같은 조건","[문진 QR] 보이기 같은 조건 · 다시 보내기 대상 = 제출 행만(read 행 제외)")
rep(ac,4,"[여권 스캔] 기기만","[여권 스캔] 기기만 · 다시 보내기가 read 행을 잡지 않음")
i=[k for k,x in enumerate(be["review_surface"]) if x.startswith("동작 변화")][0]
be["review_surface"][i]+=" · 고객 차트 「초진 설문」(`queries/customers.py:449-454` — 이미 고객 단위 마지막 행)에도 `source = read`(KOS 에서 낸 문진) 행이 보이게 됨(DAY-SPEC-000 개정 ④ 사본 귀결)."
ex["code_surface"][1]+=" · policies/reservation_layout.py `can_join` · `valid_members` · `_row` · `ROW_MINUTES`(동행 30분 분리) · services/reservation_companions.py(:31)"
ex["code_surface"].insert(2,"backend/day/schemas/reservations.py(Card `endMin` · Band `endMin` · Row · Column) · schemas/reservation_detail.py(:171 · :225-246 `questionnaire.expired`)")
ex["code_surface"][0]+=" · routers/api/displays.py `public_origin`(:55 — 두 벌)"
ex["code_surface"][4 if False else [k for k,x in enumerate(ex["code_surface"]) if "questionnaire_reads" in x][0]]+=" · services/questionnaire_kos.py(:146-158 다시 보내기 대상) · queries/customers.py(:449-454 차트 초진 설문 — 읽기만 확인)"
ex["open_questions"]=[x for x in ex["open_questions"] if "OQ-R46" not in x]
ex["phases"][1]+=" · 동행 판정 30분 분리 · bands end_min"
# WEB
web=load("wp2-web"); common(web); td=web["target_delta"]; ac=web["acceptance"]; ex=web["execution"]
i=[k for k,x in enumerate(td) if x.startswith("Rule 15 그리기")][0]
td[i]=td[i].replace("동행 띠 = 멤버를 다 감싸는 상자","동행 띠 = `bands[]` 값으로(start_min ~ end_min · line · lane_from ~ lane_to · 멤버를 다 감싸는 상자 · 행을 넘으면 ⓖ)")
td.insert(i+1,"누르기 · 놓기 시각(코디 기본값 · 지금 동작 유지 · 결정 다시 여는 것 아님): 표 빈 칸 누르기 · 옮기기 놓을 자리의 시각 = **30분 단위 그대로** · y ↔ 분은 행 높이를 따른 매핑(`resY`) — `static/day.js:2347` `RES_SLOT_MIN = 30` · `:3058-3066`(y → 시각 · 빈 칸) · `:2074`(현재 시각 선 기본 y `/ 30 × 70`)을 1시간 행 높이(lines × 140) 매핑으로. F1 [+] 은 그룹 간격(U-10). SPEC 한 줄(DAY-SPEC-007 표 빈 칸 누르기 「열 × 30분 칸」)은 머지 뒤 재결속 때.")
i=[k for k,x in enumerate(td) if x.startswith("[문진 QR]")][0]
td[i]=td[i].replace("[여권 스캔] = 기기 줄 팝오버(F5","[여권 스캔] = 기기 줄 팝오버(줄 = 기기명 · 점(초록 연결 · 빨강 미연결) · 상태 · 미연결 줄도 보이고 누름 · F5")
rep(ac,1,"행 넘는 카드","행 넘는 카드 · 동행 띠 = bands 값(멤버 길이가 다르면 가장 늦은 끝까지) · 빈 칸 누르기 · 놓기 시각 30분 단위(1시간 행 안 위 반 · 아래 반)")
rep(ac,2,"여권 기기 줄","여권 기기 줄(줄 = 기기명 [점] 상태 · 미연결 줄도 누름)")
ex["code_surface"][1]+="(day.js:2197-2300 resLayout · :2074 현재 시각 선 · :2347 RES_SLOT_MIN · :3058-3066 놓을 자리 · 빈 칸)"
ex["code_surface"][0]+="(reservations_parts.html:67-73 카드 · :93-130 rows · 띠 · 현재 시각 선)"
ex["phases"][1]+=" · 띠 bands · 누르기 · 놓기 30분 매핑"
# APP
app=load("wp3-app"); common(app); td=app["target_delta"]; ac=app["acceptance"]; ex=app["execution"]
i=[k for k,x in enumerate(td) if x.startswith("앱 예약현황 표")][0]
td[i]=td[i].replace("을 바꿈 ·","을 바꿈 · **시간 칸 선 · 회색 글자(`:313-321` 30분마다) · rows 없을 때 대체 행(`:173-174` 30분) = 1시간 행 · 띠 = `bands` 값으로(`:351-363` · Band `endMin` — 멤버 가장 늦은 끝까지 · 행을 넘으면 ⓖ)** ·",1)
rep(ac,0,"15분 1/4)","15분 1/4 · 시간 칸 1시간 · 대체 행 1시간 · 동행 띠 = bands 값)")
ex["code_surface"][0]="app/lib/ui/reservation_table.dart(:52 고정 66 · :173-174 대체 행 · :249 열 폭 · :313-321 시간 칸 · :351-363 띠 · :374-378 카드) · reservation_screen.dart · reservation_detail.dart"
ex["phases"][1]+=" · 시간 칸 · 대체 행 · 띠 bands"
for n,r in [("wp1-be",be),("wp2-web",web),("wp3-app",app)]:
    json.dump(r,open(f"{n}-request-v2.json","w"),ensure_ascii=False,indent=1)
print("ok")
