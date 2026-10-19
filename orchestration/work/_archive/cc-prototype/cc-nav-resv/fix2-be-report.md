# fix2-BE 결과 보고 — SPEC-002 0.3.0 §4 · §5.1
## 상태: done (커밋·push·PR 안 함)

## 수행 — 파일
- 고친 파일: `app/domain/board.py`(person_fields/person_of · memo_adds · ticket_used · `add_memo` 조작 · check_in `memo` · finish 시술권 차감 주석, OPERATIONS 13→14) · `app/service/board_service.py`(check_in memo · add_memo · board customers/resv/staff.work 칸) · `app/service/bundles.py`(§4 · `holdings`) · `app/service/patient_service.py` · `app/service/staff_service.py` · `app/service/memos.py`(`append` · 오늘 카드 상담 메모 덧붙임) · `app/seed/build.py`(`person()` → resv 줄에 싣기) · `app/schemas/requests.py`(MemoItem · MemoBody · CheckInBody.memo) · `app/api/desk.py`(`POST /api/desk/memo`)
- 테스트: 새 `tests/test_fix2.py`(10) · `tests/test_flow.py::test_6` 을 §4 계약으로 고침(옛 SPEC-001 §5.4 3번 동작을 단언하던 부분) · `tests/test_kos_comments.py` 조작 수 13→14 · `tests/fixtures/scenario/seed.json` sch-1(VIP) · sch-2(KR) 에 칸 추가
- 로컬 데이터: `cc/back/data/scenario/seed.json`(gitignore) visitor 8명에 칸 추가. 바꾸기 전 사본 = 스크래치패드 `scenario-seed.before.json`. `*.orig` · 실명 대응표는 안 만들고 안 열었다. `data/seed.json` · `data/cc.db` 는 **안 건드림** → 반영은 코디가 `uv run python -m app.seed build` (8610 서버 DB 를 다시 채우므로 코디 몫)

## 1. 시드 — 바꾼 고객 · 값 (전부 가짜)
| 시각 | 이름(가짜) | 국적 | phoneticName | phone | categories |
|---|---|---|---|---|---|
| 10:00 | LIU JIA HUI | TW | 류자후이 | +886 900 000 101 | [] |
| 10:30 | CHEN XIAO WEN | TW | 천샤오원 | +886 900 000 102 | [] |
| 11:00 | 김하늘 | KR | null(한국인) | +82 10 0000 0103 | [] |
| 11:30 | WANG YI TING (재내원) | TW | 왕이팅 | +886 900 000 104 | **[{name:"vip500",color:"CYAN"}]** ← VIP 1명 |
| 13:00 | CHAN MEI LING | HK | 찬메이링 | +852 9000 0105 | [] |
| 14:00 | LIN YA CHEN | TW | 린야천 | +886 900 000 106 | [] |
| 15:00 | TANAKA YUKI | JP | 다나카 유키 | +81 90 0000 0107 | [] |
| 15:30 | HUANG SHU FEN | TW | 황수펀 | +886 900 000 108 | [] |
- 번호는 국가번호 + 0 채움 + 끝 3자리 일련번호(검색 시연용으로 서로 다르게)
- `seed build`: `build.person(visitor)` → `{phoneticName, phone, vip}` 를 **상태의 resv 줄**에 싣는다(vip = categories 중 이름이 `vip` 로 시작). 참조 문서 visitor 에서는 phone · phoneticName 을 계속 뺀다(정본 하나). `seed save` 는 상태 resv 줄을 그대로 저장하므로 칸이 따라간다(테스트 확인). 메모리 build 로 실제 시나리오 8명 값 확인함
- 칸이 없는 예전 시드/DB 는 응답이 `null · null · false`

## 2. 응답 칸 — 고객이 나오는 곳 전부 (grep 결과)
| # | 응답 | 위치 | 칸 |
|---|---|---|---|
| 1 | `GET /api/board` customers[] | board_service.customer_view | phoneticName · phone · vip |
| 2 | `GET /api/board` resv[] | board_service.board | 〃 (내부 `memoAdds` 는 뺀다) |
| 3 | `GET /api/board` staff[].work[] (customerName) | board_service.staff_work | 〃 |
| 4 | `GET /api/patients/{id}` (환자 상세 = 예약 상세 · 직원 환자 상세 공용) | patient_service.detail | 〃 |
| 5 | `GET /api/staff/{id}/home` 배정형 current · next[] · done[] | staff_service._item | 〃 |
| 6 | `GET /api/staff/{id}/home` 순회형 patients[] | staff_service._rounds | 〃 |
- 정본은 상태 resv 줄 하나(`B.person_of`) — 접수 전 고객도 같은 값
- 해당 없음: `/api/reservations`(예약관리 데모 — 링키 가짜 고객, 자체 `customer.reading` 있음) · `/api/staff`(직원) · 통역(고객 칸 없음) · procedure-candidates(시술 묶음)

## 3. 시술권 차감 시점
- **지금까지(조사)**: 차감을 따로 기록하는 곳이 없었다. 「사용됨」 = **동선 단계에 ticketId 가 붙은 것 전부**로 계산 — ① check-in(시술권 묶음 선택) ② add-procedures ③ payment_complete(오늘 결제분 단계에 ticketId 연결). 그래서 `보유 n/m` 의 n 이 접수 순간 줄었다(patient_service `tickets` = 후보 left, `_chart` 「보유 시술권」 = available − 동선 ticketId)
- **바꾼 것**: `B.ticket_used(steps)` = **state == done 인 단계의 ticketId**만. `bundles.holdings()` 가 n = AVAILABLE − 완료된 회차, m = 묶음 전체 장 수. patient `tickets` · chart 「보유 시술권」 둘 다 이걸 쓴다. 진행 안 함(skipped)·노쇼·진행 중은 안 빠짐(테스트). 차감 = `finish` 순간이라 따로 저장 없음(undo 도 자연히 되돌림)
- KOS 주석: `finish` 의 시술 + ticketId 갈래에 「시술권 차감(ticketId 사용 처리): 공개 없음 · 내부 미확인 — KOS 요청」(SPEC-001 §9 형식)
- 후보 묶음의 회원 고르기(다음 1장)는 여전히 「동선에 들어간 ticketId」를 피한다 — 같은 장을 두 단계에 못 넣게

## 4. 추가 요청 메모 — `POST /api/desk/memo {scheduleId, category, text}`
- category = `reservation` | `consultation`(그 밖 400 invalid_request) · text strip 후 비면 400 `empty_memo` · 없는 일정 404 `reservation_not_found` · 응답 `{version}` + SSE + log(`memo`) · undo 대상
- 저장: 상태 resv 줄 `memoAdds: {reservation: [...], consultation: [...]}` (응답엔 안 나감). 접수 전 예약도 가능
- 보이는 곳(환자 상세):
  - `reservationMemo` = 원문 + `\n` + 덧붙인 줄들(원문 비면 줄만)
  - 오늘 방문 카드 `visits[0].consultation` = (상담 종료 뒤면 이벤트 상담 원문) + 덧붙인 줄들. **잠금(locked=true) 중에도 덧붙인 줄만 들어 있다** — 공개 시점 예외. 상담 종료 이벤트가 채워도 줄은 끝에 남는다(테스트)
- `POST /api/desk/check-in` 선택 `memo: {category, text}` → 같은 처리. **빈 text 면 접수 전체 400**(접수도 안 됨) — front 는 메모가 없으면 `memo` 칸을 빼고 보낸다
- KOS 주석: add_memo — 예약 = 공식 `changeReservationMemo`, 상담 = 공식 `updateScheduleConsultationInfo`(원문 + 덧붙인 줄 전체 쓰기) · check_in 의 memo 갈래에도 같은 주석

## 5. §4 시술 후보 정정 (`bundles.build`)
- 보유 시술권 후보: 접수 전(cust 없음 = 접수 모달) → 보인다 / 접수 뒤 상담 종료 전 → **없음** / 상담 종료 뒤 → 보인다
- 묶음의 회차(AVAILABLE 장)가 하나라도 동선에 있으면 그 묶음 통째로 뺀다 → E2E batch-2 #2(포텐자 6/10 칩 재등장) 해결
- 오늘 결제분 · 원장 상담 후보는 그대로

## 검증
- `uv run pytest` → **75 passed**(이전 65 + test_fix2 10개, test_6 은 고쳐서 유지) · `uv run ruff check .` → All checks passed
- 기능 폴더 밖 import 없음(grep). 8610 · 3610 프로세스 · data/cc.db 안 건드림 — 예시 JSON 은 임시 DB

## 계약 대조
| SPEC-002 0.3.0 | 결과 |
|---|---|
| §5.1 시드 3칸 · 가짜 값 · VIP 1명(vip500/CYAN) | 같음 |
| §5.1 응답 phoneticName · phone · vip(bool, vip 로 시작) — board customers · reservations · 환자 상세 · 직원 홈 | 같음 + board staff.work 도 |
| §5.1 차감 = finish · n 은 완료만 · KOS 주석 | 같음 |
| §5.1 memo API · 빈 text 400 · 덧붙임 · 바로 보임 · 상담 종료 뒤에도 유지 · check-in memo · KOS 주석 2종 | 같음 |
| §4 후보 정정 A · B | 같음 |

## front 에 넘길 것 / 주의
1. `lib/memo.tsx` todayBlocks 는 `!v.locked` 일 때만 상담 내용을 그린다 → 잠금 중 덧붙인 상담 메모 줄이 안 보인다. **`v.consultation` 이 있으면 그린다**로 바꿔야 §5.1 「바로 보인다」가 된다(잠금 중엔 덧붙인 줄만 들어 있음)
2. check-in 에 빈 memo 를 보내면 접수가 400 — 메모 입력이 비면 `memo` 칸을 빼라
3. CheckInModal 은 procedure-candidates 를 접수 전에 읽으므로 보유 시술권 줄은 그대로 나온다. 자동 체크 제거(D-31)는 front 몫
4. patient `tickets` = 묶음 전부 n/m(동선 여부 무관, n 은 완료만 차감) — 「보유 시술권 n/m」 표시에 그대로
5. 1차 동작 변경(범위 안): 보유 n/m 이 접수 때 안 줄고 시술 완료 때 준다 · 상담 종료 전 [시술 추가]에 보유 시술권 후보가 없다

## 응답 JSON 예시 (테스트 픽스처 시드, 임시 DB)
```
### board.resv[sch-1]
{
 "scheduleId": "sch-1",
 "time": "10:00",
 "name": "LIN MEI",
 "isNew": true,
 "nationality": "TW",
 "phoneticName": "린메이",
 "phone": "+886 900 000 001",
 "vip": true,
 "st": "booked"
}

### POST /api/desk/check-in (memo 포함) → 200
{
 "version": 2
}

### POST /api/desk/memo → 200
{
 "version": 3
}

### POST /api/desk/memo 빈 text → 400
{
 "error": {
  "code": "empty_memo",
  "message": "메모 내용을 적어 주세요"
 }
}

### board.customers[sch-1]
{
 "scheduleId": "sch-1",
 "name": "LIN MEI",
 "isNew": true,
 "nationality": "TW",
 "location": "reception",
 "prevRoom": null,
 "phoneticName": "린메이",
 "phone": "+886 900 000 001",
 "vip": true,
 "status": {
  "key": "reception",
  "label": "접수 후 대기",
  "need": null
 },
 "steps": "…"
}

### GET /api/patients/sch-1 (발췌)
{
 "name": "LIN MEI",
 "phoneticName": "린메이",
 "phone": "+886 900 000 001",
 "vip": true,
 "reservationMemo": "**1시 전 아웃 희망**\n26.10.9/본사/리프팅/동행2명/데스크\n상담사A 지정 요청\n우산 맡김",
 "tickets": [],
 "visits[0]": {
  "date": "2026-10-09",
  "today": true,
  "locked": true,
  "counselors": [],
  "consultation": "목 주름도 상담 원함",
  "orderMemo": null,
  "procedures": [],
  "assigneeMemos": []
 }
}

```
