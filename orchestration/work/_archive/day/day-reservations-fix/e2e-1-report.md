# e2e-1 결과 — 로컬 스택(11340 · kos-demo) + KOS DEMO 실물 · #300 · #301 · #302

시각 2026-11-28 15:07 ~ 15:16 KST · 이 워크트리 미커밋 코드 · 스택은 손대지 않음(코디가 시드 `seed-demo --kos-demo` 넣은 뒤 진행). 웹 = 로그인 쿠키 HTTP 조각 · 앱 = 같은 세션으로 `/api` JSON. id 는 앞 8자.

| # | 시험 | 결과 | 수치 · 근거 | 비고 |
|---|---|---|---|---|
| 1 | F6 — 4경로 `qrUrl` 같음 | **O**(기기 쪽 = 데이터 없음) | 방문 `d2798075` · 문진 요청 POST 뒤 SSE `display` 2건(`d2798075`) · `GET /reservations/visits/{id}` 조각 `data-day-res-dp-link` = POST `qrUrl` ✓ · 동행 저장 PUT ✓ · 신분확인 PUT ✓ · 앱 상세 `displays[].qrUrl` = POST ✓ | 기기(태블릿) 0대(`device` 0행) → 기기 줄 POST · 태블릿 `pending` API = **데이터 없음** |
| 2 | 팝오버 | **O**(기기 줄 = 데이터 없음) | `display-targets` questionnaire · scan GET → 요청 0 → 0 · 「링크」 POST 2번 = 같은 링크 · 요청 1행(`6813e844` pending) · 앱 POST = 새 요청 `ffc109c6` pending · 앞 `6813e844` canceled(F-1) · 그 뒤 웹 링크 POST = 앱 요청 링크 다시 씀(요청 수 그대로 2) | 기기 줄(앞 요청 취소 → 새) = 기기 0대라 실물 없음(단위 시험만) |
| 3 | 배치 Rule 15 | **O**(6장 이상 · 띠 = 데이터 없음) | 웹 `data-day-res-rows` · 카드 data 속성 = 앱 JSON `rows` · `cards` **같음**(rows 14 · cards 5) · `openMin` 600 · 첫 행 10:00 ~ 11:00 · 마지막 23:00 ~ 24:00 · 리프팅(60분) `d2798075` 17:00 ~ 18:00 = 1020 ~ 1080 lane 0(행 하나) · `6bf64ef7` 17:30 ~ 18:30 = lane 1(옆 자리 · 18:00 행 넘는 카드) · bands 0 = 0 | 동시 6장 · 동행 띠는 DEMO 데이터 없음(예약 2건만 만듦 — 코디 지시) |
| 4 | KOS 문진 읽기 회차 | **O**(200 은 회차 밖에서 확인) | `day.emr.sync_questionnaires_hospital` 실행 44회(10초마다 일정 회차 뒤) · `{'asked': 3, 'found': 0, 'added': 0}` × 32 → 제출 뒤 `{'asked': 2 …}` × 12(1b9a7c0c 는 6개월 안 DAY 행이 생겨 **건너뜀**) · 400 고객 3명 = 행 0 · 경고(그 고객만 건너뜀) 0 · `read` 행 0 · 중복 0 | 200 경로는 회차 대상 고객이 없어(제출 고객 = 기간 안 → 건너뜀) 회차로는 안 탐 → 같은 어댑터 · mapper 로 서버 공유 토큰 읽기 1회: 1b9a7c0c → 200 · 답 14 · 제출 id 24자 |
| 5 | D46 ② 제출 id | **X / pending** | DAY 고객 웹 링크로 1b9a7c0c(방문 `6bf64ef7`)에 1회 제출 → DAY 200 · 행 `8d6374a0` `web_submit` 저장 · **KOS 제출 응답 = HTTP 500** → `crm_status = failed` · `crm_error = KosError:500` · `external_ref` 없음 · 그런데 **KOS 에는 저장됨**(내부 legacy 읽기 200 · 제출 id `6b0a712a` · `createdDateTimeUtc` 06:14:02Z = DAY 제출 시각 · 답 14) | **제출 응답에서 id 칸 = 확인 못 함**(500 응답 · 서버가 본문을 남기지 않음 · 다시 제출은 1회 허락 밖이라 안 함). read 행은 안 생김(그 고객이 기간 안이라 회차가 건너뜀 — external_ref 로 막힌 게 아님) |
| 6 | 6개월 | **O**(경계 실데이터 없음) | 행 = 2026-11-28 15:14 KST(`web_submit`) · 오늘 KST 2026-11-28 → 기간 안 · 앱 `questionnaire.expired = false` · `actions.questionnaireQr = false` · 웹 「제출됨」 ✓ 「6개월 경과」 없음 · [문진 QR] 버튼 없음 · 제출 없는 방문 `d2798075` = 앱 `questionnaire null` · QR true · 웹 「작성 필요」 · [문진 QR] 있음 | 6개월 지난 행 없음 → 경계는 단위 시험(`test_questionnaire_period_rules.py`)만 |
| 7 | D45 팝오버 중 SSE | 코드 근거 · **코디 눈 확인** | `backend/day/static/day.js:2590` — 모달 안 팝오버가 열려 있으면 `resDetailRun` 이 다시 받기를 미룸 · `:390-399` `closePop` → `day:pop-closed` → `:2606` 그때 한 번 다시 받음 | 브라우저에서 팝오버 열어 둔 채 다른 창에서 요청 만들기 → 닫히지 않는지 |

## 제출 id 위치(D46 ②)
- KOS 제출(`visitor/open/v1/commands/submit-visitor-questionnaire`) 응답 = **HTTP 500** — 본문 칸은 볼 수 없었다(서버는 상태 · 오류 이름만 남김 · `crm_error = KosError:500`).
- KOS 쪽 실제 저장 id(내부 읽기 `id`) = `6b0a712a…`(24자 · 16진 ObjectId 꼴). 제출 응답 id 가 이것과 같은지 = **미확인**.

## 버그 · 위험(원인 file:line)
1. **KOS 가 500 을 주고도 제출을 저장** → DAY 는 「실패」 + [다시 보내기] 를 띄움 — 누르면 KOS 에 **같은 문진이 두 번** 들어감(KOS 쪽 원인 · DAY 판정은 계약대로). 위치: `backend/day/services/questionnaire_kos.py:103-109`(2xx 아니면 failed) · `:187-193` [다시 보내기] 대상. 오류 이름을 못 남김: `:105` `f"{type(exc).__name__}:{status}"` — `KosError.name`(className) 을 안 실어 500 원인을 가를 근거가 없음. 500 원인 후보(확인 안 됨): 생년월일이 KOS 고객에 없어 시험 값을 넣음 · 첫 보기만 고름.
2. (버그 아님 · 기록) 미리 채움 `gender = GENDER_UNSPECIFIED`(18자) 그대로 보내면 400 `field=gender`(`schemas/public_questionnaire.py:118` max 16) — 화면은 `day.js:6356` 에서 FEMALE · MALE 외 값은 비워 고객이 고르게 하므로 실제 경로는 안 막힘.

## 남긴 상태
- KOS DEMO: 예약 2건 만들고 취소함 — `d2798075`(고객 `b26e24e0` · KOS `6b051a9e` · 리프팅 17:00 ~ 18:00) · `6bf64ef7`(고객 `1b9a7c0c` · KOS `6b083e1b` · 17:30 ~ 18:30) — 취소 쓰기 confirmed · 다음 동기화에서 KOS 값 `canceled`(15:15:14 KST) 확인. 그 고객들의 앞 취소 예약(`5c39a496` · `a294bc82`)은 안 건드림.
- KOS DEMO: 고객 `1b9a7c0c`(KOS `6b083e1b`)에 **문진 제출 1건**(KOS 제출 id `6b0a712a`) — 생년월일 칸은 KOS 고객 값이 비어 시험 값 `19900101` · 성별 FEMALE(미지정이라 고름) · 질문마다 첫 보기(14문항 · INPUT_BOX 1문항 건너뜀) · 약관 동의. KOS 에서 지울지는 코디 판단.
- DAY 로컬 DB: `questionnaire_history` `8d6374a0`(web_submit · failed) · 띄우기 요청 4행(방문 취소로 시한 지나면 expired) · 신분확인 기록 2행(true → false 되돌림 · DAY 전용) · 동행 저장 1회(빈 목록 · 변화 없음).
- KOS 로그인: 테스트 계정 활성 로그인 2개(06:07:54 첫 로그인 403 때 · 06:09:24) **둘 다 해제 → 0개**. DAY 세션 로그아웃. 내 KOS 읽기는 서버 공유 토큰(Redis)으로 해서 시스템 계정 새 로그인 없음.

## 코디 눈 확인
1. D45 — 예약 상세에서 [문진 QR] 팝오버를 연 채 다른 창 · 앱에서 같은 방문 요청 만들기 → 팝오버가 안 닫히고, 닫으면 진행 칸이 새로 그려짐.
2. 「링크 복사하기」 클립보드 · 「링크 열기」 새 탭(브라우저 동작).
3. 18:00 행을 넘는 17:30 카드의 두 조각 그림 · 1시간 행 높이(웹 140) · 앱 표.
4. 기기 줄(초록 · 빨강 점) — 기기 0대라 실물 없음(태블릿 로그인 필요).
