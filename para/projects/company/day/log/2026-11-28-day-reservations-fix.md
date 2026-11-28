# 작업 요약 — day-reservations-fix (day)

기간: `2026-11-27` ~ `2026-11-28`
결과: Code PR CENTURION_DAY#303 dev 머지 · SPEC PR mediness#971 main 머지 · Delivery #300 ~ #302 마감. 태블릿 실기기 확인은 dev 배포 뒤로 남김.

## 1. 무엇을 했나

dev 예약 현황판을 사용자가 직접 써 보고 피드백 여섯 개(F1 ~ F6)를 냈다.
- 카드 옆에 예약을 추가할 자리가 없었다.
- 60분 예약이 한 칸(30분)만 차지했다.
- [문진 QR]에 메뉴가 없었다.
- 문진을 6개월마다 다시 받아야 했다.
- 기기 상태가 모달 안에 별도 카드로 나왔다.
- 태블릿 보내기를 누르면 QR이 떴다가 바로 사라졌다.

조사와 dev 로그로 원인을 확정한 뒤 SPEC 을 개정했다(검수 4번). 이슈를 BE · 웹 · 앱 셋으로 발행하고 세 워커가 병렬로 구현했다. 그 뒤 코드 검수 1회, 로컬 KOS DEMO 실물 e2e, Playwright 화면 검수 2회(headless · headed)를 거쳐 dev 에 머지했다. 진행 중에 KOS 문진 읽기(10초 동기화 뒤 별도 태스크)와 6개월 재작성 규칙도 들어갔다.

## 2. 적용한 기술·개념

- **같은 화면을 그리는 경로마다 같은 입력을 넘기기(F6)** — QR 이 「떴다 사라지는」 원인 · [[contract-surface-enumeration]]
  - 왜 이걸 골랐나: 처음에는 만료 · 시간대 · SSE 를 의심했다. dev 로그와 DB(만료 − 생성 = 600.0초)를 보니 시한 문제가 아니었다. SSE `display` 뒤 웹이 상세를 다시 받는 GET 이 `origin` 을 안 넘겨 `qrUrl = null` 로 그리고 있었다. 같은 상세를 그리는 경로 4곳 중 POST 만 origin 을 넘겼다. 그래서 `public_origin` 을 하나로 모으고 `detail_view(origin)` 을 필수 인자로 바꿨다. 이제 빠뜨리면 mypy 가 잡는다.
  - 무엇이 어려웠나: 사용자 말 「버튼이 순간 사라지는데 어떻게 눌러」를 처음에 「실기기 시험」으로 잘못 읽었다. 화면 증상을 로그와 DB 로 먼저 봤어야 했다.
  - 근거: `be-f6-debug-1-report.md` · `routers/reservation_detail.py` · `session.public_origin`

- **배치를 서버 한 곳에서 계산하고 웹 · 앱은 그리기만(Rule 15)**
  - 왜 이걸 골랐나: 웹(`day.js`)과 앱(Flutter)이 각자 칸을 계산하면 같은 예약이 두 화면에서 다르게 놓인다. 그래서 서버가 `rows` · `cards(lane, line)` · `bands` 를 내고, 화면은 픽셀(웹 140 · 앱 30분 칸 × 2)만 정한다.
  - 무엇이 어려웠나: 「5장 넘으면 아래 줄로 접기」(R64)와 「길이 비례 높이」가 부딪혔다. 접힌 행이 높아지면 행을 넘는 긴 카드의 위치가 흔들린다.
    - 사용자 결정은 두 번 뒤집혔다: 상한 없음 → 5장 유지 + 오픈 시각부터 1시간 행(KOS 꼴).
    - 경계 경우(행 넘는 카드)를 처음엔 「아래 줄 띠를 덮고 찬 자리로 셈」으로 정했다. 그런데 코드 검수가 다섯 자리가 다 덮이면 카드가 겹친다는 것(F-2)을 재현했다. 「두 조각」(시작 행 첫 줄 끝에서 자르고 다음 행 첫 줄에서 이어 그림)으로 바꿨다.
    - 「동행 판정」(R71 · 30분)이 배치와 같은 `_row()` · `ROW_MINUTES` 를 쓰고 있었다. 상수만 60으로 바꾸면 묶기 조건이 조용히 넓어졌을 것이라 함수와 상수를 나눴다.
  - 함께: [[contract-surface-enumeration]](같은 상수 두 뜻) · [[server-rendered-fragments]](서버 한 곳)
  - 근거: spec-006 Functional Rule 15 ⓐ ~ ⓚ · `policies/reservation_layout.py` · `review-delivery-1-report.md` D2 · `review-code-1-report.md` F-2

- **KOS 문진 읽기 = 내부 API · 일정 회차 뒤 별도 태스크 · 기간 안 건너뜀** · [[public-vs-internal-api]]
  - 왜 이걸 골랐나: 사용자 원칙 「DAY 는 KOS 내부 API 만」(나중에 빼기 쉽게)을 따랐다. 공개 `get-questionnaire-submit` 대신 내부 `…/get-questionnaire-submit/legacy` 를 썼다. 일정 태스크 안에서 부르면 10초 회차 시간이 늘어나 별도 태스크로 뺐다. 호출 수는 「6개월 안에 낸 고객은 건너뜀」으로 줄였다. KOS 는 고객당 한 건만 주고 「바뀐 것만」 경로가 없다.
  - 무엇이 어려웠나: 처음 조사 리포트가 공개 경로를 찾아 왔고 나는 그대로 결정 표에 옮겼다. planner 가 11-19 원칙과 어긋난다고 짚었다. 중복 가르기는 KOS 제출 id(`external_ref`)로 한다. 이 id 가 응답 어느 칸에 오는지는 e2e 2회차에야 확인했다(최상위 `questionnaireId` = 읽기 `id`).
  - 근거: `be-kos-questionnaire-1-report.md` · `services/emr_questionnaire_sync.py` · `e2e-2-report.md` · 메모리 `feedback_day_kos_internal_api_only`

- **HTMX 응답이 트리거 요소를 바꿔 넣은 뒤의 afterRequest** — 링크 복사 · 열기 실패 · [[server-rendered-fragments]]
  - 왜 이걸 골랐나: 단위 · 화면 테스트(TestClient · jsdom)는 다 통과했는데 실제 브라우저에서만 클립보드가 비고 새 탭이 `about:blank` 로 남았다. 응답이 `#modal-root` 를 통째로 바꿔 폼이 문서에서 떨어진 뒤 `htmx:afterRequest` 가 와서 `e.detail.elt` 가 폼이 아니었다. `requestConfig.elt` 로 고쳤다.
  - 무엇이 어려웠나: headless Playwright 가 폼 · 문서 리스너의 `connected` 값을 찍어 보고서야 원인이 나왔다. 같은 settle 이 위치 `style` 속성을 옮기며 CSP `style-src-attr` 위반도 냈다.
  - 근거: `qa-1-report.md` FAIL-1 · WARN-1 · `day.js` `dpLinkAfterRequest`

- **외부 쓰기의 「실패인데 저장됨」** — KOS 문진 제출 500 · [[external-write-queue]]
  - 무엇이 어려웠나: 실물 제출 1회가 HTTP 500 을 받았는데 KOS 에는 저장돼 있었다. OpenAPI 설명 「저장 뒤 고객 정보 갱신」을 보면 갱신 단계 실패가 유력하다. 원인 후보는 휴대폰 국가번호 빈 값이다. DAY 는 실패로 보고 [다시 보내기]를 띄우므로 이중 제출 위험이 있다. 이번에는 KOS 오류 이름만 기록하게 했고(다음 원인 가르기용), 이중 제출 막기는 다음 작업으로 남겼다.
  - 근거: `e2e-1-report.md` 5 · `e2e-2-report.md` · `services/questionnaire_kos.py` `crm_error_of`

## 3. 막혔던 것 / 사고

- **사용자 결정을 되묻다가 질책** — 「60분이면 2칸」은 이미 말한 결정인데 겹침 배치를 계속 물었다. 그 뒤 결정은 바로 표에 적고 경계 경우만 기본값을 정해 알리는 방식으로 바꿨다.
- **공개 API 경로를 결정 표에 옮김** — 조사 리포트를 그대로 옮겼다. 사용자 「내부 API 만」 → 메모리로 남김. 조사 브리프에 「내부 경로를 찾아라 · 공개는 대안 아님」을 쓴다.
- **SPEC 검수 4회** — 1시간 행으로 바꾸며 옛 「30분 = 1칸 · 60분 = 2칸」 문장이 여러 문서에 취소선 없이 남았다. 차수마다 넓힌 grep 으로 하나씩 더 나왔다. 처음부터 「옛 문구 전부 grep · 취소선 밖 0」을 지시서 완료 조건에 넣었어야 했다.
- **로컬 e2e 준비** — 새 워크트리 env 를 복사하면서 포트만 바꾸고 `DATABASE_URL` · `REDIS_URL` 포트를 안 바꿔 첫 기동이 실패했다. 새 DB 라 DEMO 연결 시드(`seed-demo --kos-demo`)가 없어 로그인 403. 오늘 DEMO 방문이 전부 취소 상태라 시험 예약을 만들었는데, e2e 가 끝나며 취소해 버려 QA 가 쓸 방문이 없었다. 다시 만들었다.
- **실기기 미검증** — 로컬에 등록 태블릿이 0대라 기기 줄 모양 · 태블릿 표시 · D45(팝오버 연 채 다시 그리기)를 화면으로 못 봤다. dev 배포 뒤 확인으로 남겼다.
- **KOS 시험 문진은 지울 길이 없음** — 제출 2건이 DEMO 에 남았다(OpenAPI · HAR · 코드 어디에도 삭제 경로 없음).

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-27 | F1 오른쪽 여백 = 카드 반 폭(70) · 점선 [+] · 툴팁 「그룹 \| 시작 ~ 끝」 | 사용자 「카드 반 칸 정도」 · KOS 꼴 |
| 2026-11-27 | 팝오버는 한 단계 — [문진 QR] = 링크 복사하기 · 링크 열기 / 기기 줄 · [여권 스캔] = 기기 줄 | 사용자 「왜 QR 은 2뎁스야」 · 「여권이랑 통일」 |
| 2026-11-27 | DAY 의 KOS 호출 = 내부 API 만 | 사용자 「나중에 빼기 편하게」 |
| 2026-11-27 | KOS 문진 읽기 = 10초 일정 회차 뒤 별도 태스크 · 6개월 안 건너뜀 | 사용자 「10초마다 받아올 때 같이」 · 호출 줄이기 |
| 2026-11-27 | ~~겹침 상한 없음~~ → 5장 규칙 유지 + 오픈 시각부터 1시간 행 | 사용자 「5장 넘으면 좌우 스크롤이 많아져서 내려가야 해」 |
| 2026-11-27 | 검수는 코드 끝에 한 번(Issue 마다 안 함) | 사용자 |
| 2026-11-28 | ~~R45 아래 줄 띠 덮음~~ → 행 넘는 카드 = 두 조각 | 코드 검수 F-2(겹침 재현) |
| 2026-11-28 | 링크 다시 쓰기 = 웹 팝오버만 · 시한 안만(앱은 늘 새 요청) | 코드 검수 F-1 · qa-2 관찰 |
| 2026-11-28 | [+] · 빈 칸 누르기 시각 단위 = 그룹 간격 | qa-1 W-a(60분 그룹 :30 칸 = 시간 빈 값) |
| 2026-11-28 | 진행 칸 = 「남은 시간」만 · 이중 제출 · 국가번호 = 다음 작업 | 사용자 「추천으로」 |

## 5. 날짜별 로그

- `2026-11-27` 피드백 F1 ~ F6 · 조사 · F6 원인(origin) · KOS 문진 실물 · SPEC 개정과 검수 4회 · Issue #300 ~ #302 · BE · 웹 · 앱 병렬 구현
- `2026-11-28` 코드 검수(FAIL 2 → PASS) · 로컬 e2e 2회(제출 id 확인 · 500 원인) · Playwright 화면 검수 2회(headed 는 사용자가 봄) · Code PR #303 · SPEC #971 머지 · Delivery 마감

## 6. 산출물

- spec PR: MediSolveAIDev/mediness#971
- code PR: MediSolveAIDev/CENTURION_DAY#303 (Delivery #300 · #301 · #302)
- 리포트: `research-1-report.md` · `be-f6-debug-1-report.md` · `be-kos-questionnaire-1-report.md` · `review-doc-1 ~ 4-report.md` · `review-delivery-1-report.md` · `review-code-1 · 2-report.md` · `e2e-1 · 2-report.md` · `qa-1 · 2-report.md`(스크린샷 `qa-1/` · `qa-2/`)

## 7. 잔여

- dev 배포 뒤 태블릿 실기기: 기기 줄 `기기명 [점] 상태` · 태블릿에 문진 표시 · D45 (OQ-D53)
- 다음 작업(새 slug): 예약 · 접수 · 상담 · 시술 모달 디자인 + OQ-D50 이중 제출 막기 · OQ-D51 국가번호 · OQ-D52 「6개월 경과」 고객 옛 건강정보 표시
- 앱 `board_messages_contract_test` 기존 실패(웹 `memo_too_long` 이 앱 `copy.dart` 에 없음 · #299 부터)
- KOS DEMO 시험 문진 2건(고객 `1b9a7c0c` · `f68fd438`) — 지우기 경로 없음
- 파비콘 404(모든 페이지 · 기존)

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/day/day-reservations-fix/README|day-reservations-fix]]
<!-- work-links:end -->
