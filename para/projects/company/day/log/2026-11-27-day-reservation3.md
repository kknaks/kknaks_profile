
# 작업 요약 — day-reservation3 (day)

기간: `2026-11-26` ~ `2026-11-27`
결과: dev 머지 · 배포 완료(CENTURION_DAY#299 `65506f35` · 스펙 mediness#968 `d0fcc23a` stable · Delivery #297) · prod 는 다음 배포(키 먼저 전달)

## 1. 무엇을 했나

예약 현황판 오른쪽 「예약 요청」 칸은 앞 작업(R3 · R32)에서 미뤄 둔 자리였다. 링키(외부 예약 대행)가 보낸 요청을 병원 코디가 받아 KOS 예약으로 만드는 길이 없어서, 이번에 **슬랙 스레드처럼 한 예약 = 한 스레드**로 지었다. 링키가 버전(신규 · 수정 · 취소)을 올리고, 병원은 댓글 · 변경 요청 · [예약 생성/수정/취소]로만 답한다. ext 에 E1 ~ E8 을 새로 열고, 생성 버튼 하나가 초진이면 KOS 고객 찾기 → 고객 등록 → 예약, 재진이면 예약 한 건을 KOS 에 쓰고 다시 읽어 확인한다. 시안 v15 → SPEC-008(4차 검수) → 코드(2차 검수) → 실제 KOS 데모 e2e 2회 → dev 배포까지 갔고, 마지막 날 링키 개발자 질문으로 ext 스웨거에 상태값 뜻 · 상태 × 행동 · 오류 코드를 다 적었다. 덤으로 셸 메뉴 「홈」→「현황」 · 로그인 뒤 = 예약 현황.

## 2. 적용한 기술·개념

- **확인 대기 잠금(쓰기 확인 전엔 스레드를 잠근다)** [[external-write-queue]] — 외부(KOS) 쓰기가 비동기 큐로 나가는 동안 같은 스레드에 새 버전 · 버튼이 오면 이중 예약이 난다
  - 왜 이걸 골랐나: 「쓰기 실패하면 대기를 푼다」가 자연스러워 보였는데, 실패 = 결과 불명(KOS 엔 들어갔을 수 있음)이라 푸는 순간 다시 [예약 생성]이 열려 같은 예약이 두 번 생긴다(문서 검수 2차 FAIL). 대기는 **확인될 때까지** 두고, 사람이 「KOS 등록 실패」(= 접음)를 눌러야만 푼다
  - 무엇이 어려웠나: 같은 구멍이 입구마다 다시 났다 — 3차에서 공용 retry 두 경로가 접은 행을 다시 보냄 → 스레드 행은 공용 retry 409 `request_thread_write`. 4차에서 「재전송 입구 전수」로 grep 해서 닫았다
  - 근거: `review-doc-2-report.md` · `review-doc-3-report.md` · `backend/day/services/reservation_writes.py:360` · SPEC-008 U-7
- **외부 API 는 실물 probe 로 본문을 정한다** — KOS 「당일 지정 상담사」 칸 · update 한 본문에 메모 + 유입 · create-visitor 이메일
  - 왜 이걸 골랐나: DAY 코드만 보고 「KOS 에 상담사 칸 없음」이라 단정했다가 사용자 스크린샷으로 틀린 게 드러났다. 그래서 SPEC 에 「구현 전 실물 확인」 OQ 로 두고 HAR + 데모 지점 실호출로 정했다
  - 무엇이 어려웠나: probe 결과 `reserve` 최상위 `counselor` 가 바로 먹어서 SPEC 이 계획한 W18(생성 뒤 상담사 따로 쓰기)이 필요 없어졌다 — 문서 계약이 실물보다 한 단계 많았다. 상담사 지우기는 `counselor: {}` 여야 지워진다(e2e 1 에서 빈 값이 안 가던 것)
  - 근거: `be-probe-1-report.md` · `be-probe-2-report.md` · `e2e-1-report.md` · `backend/day/emr/kos/writes.py:141`
- **같은 고객 판정 = 이름 + 식별값 하나 이상** — 초진/재진을 DAY 사본에서 가른다
  - 왜 이걸 골랐나: 처음 안은 이름 + 생년월일 필수였는데 KOS 고객 등록 조건이 「이름 + (연락처 · SNS · 이메일 · 여권 · 생년월일 중 하나)」였다(사용자 KOS 오류 화면). 판정도 같은 조합으로 맞추고, 2명 이상이면 후보 화면 대신 「고객 확인 필요」 댓글 → 링키가 `customerId` 넣은 새 버전(사용자: 후보 화면 필요 없음)
  - 무엇이 어려웠나: e2e 에서 이름만으로는 KOS 중복 고객을 못 찾아 초진으로 새로 만들 뻔했다 → W1 에 이메일까지 실었다
  - 근거: `backend/day/services/reservation_request_ext.py:219` · `e2e-1-report.md` ①
- **멱등 재시도 = 처음 응답을 저장해 돌려준다** [[idempotency]] — `Idempotency-Key`
  - 왜 이걸 골랐나: 버전 행에서 다시 계산하면 병원 동기화가 같은 버전에 뒤늦게 붙이는 `reservation_applied` 때문에 재시도 응답이 바뀐다. 응답을 만든 자리에서 `accepted_status` 를 저장하는 쪽이 결정적이다
  - 근거: `be-swagger-2-report.md` · migration `20261126_0031`
- **스웨거를 계약서로** — enum 이름만 있던 ext 문서에 값 뜻 · 상태 × 행동 · 경로별 `error.code` · 흐름을 코드 description 으로
  - 왜 이걸 골랐나: 외부 개발자가 「상태값 분류가 어떻게 되냐」를 물었다. 별도 md 만 쓰면 코드와 어긋난다 → 원문은 코드(스웨거), 안내서 md 는 그걸 근거로만
  - 근거: `backend/day/routers/api/ext_reservation_request_docs.py` · `reference/2026-11-26-reservation-request/linky-ext-reservation-request-guide.md`

## 3. 막혔던 것 / 사고

- **키 형식을 바꾸는 배포를 키 전달보다 먼저 했다** [[secret-store]] → dev 배포 직후 링키 · 차티가 옛 키로 401 · 같은 IP 실패 누적으로 429 → 로그(`ext_call … 401`)로 원인 확인 → 새 키 전달로 풀림. 형식이 바뀌는 비밀은 **전달 → 확인 → 배포** 순서. prod 는 그렇게 한다
- **Key Vault 방화벽** — 로컬 IP 가 막혀 비밀을 못 넣음 → 11-11 방식대로 day-vm SOCKS(`ssh -D`)로 REST PUT · 이전 버전이 남아 되돌릴 수 있다
- **0031 을 배포 전에 고쳤더니 로컬 DB 와 어긋남** → 0030 으로 내렸다 올림 · 시연 데이터 다시 만듦. 로컬 스택 재시작 때 TIME_WAIT 로 포트 probe 가 「Address already in use」 → 잠깐 기다리면 풀림
- **스펙 PR 이 main 과 개정 번호 충돌**(#964 가 SPEC-007 고침 6 · #298 이 번호 바꿈) → 우리 커밋을 하나로 합쳐 한 번만 rebase · 우리 번호만 다음 번호로(006 ⑮ · 007 고침 7) · 옛 log 행까지 바꾼 실수는 검수(X1)가 잡음
- **코디 판단 실수 셋(사용자 교정)** — KOS 상담사 칸 없다고 단정 · 원장 1:1 상담을 KOS 체크로 · 당일 미방문 자동 처리를 스레드에 넣자고 함 → 「고객 → 링키 → 병원 흐름에서 논의하는 거잖아」로 범위를 좁힘

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-26 | 스레드 하나 = 예약 하나 · 버전은 늘 링키가 · 병원 거절 버튼 없음 · 상태 = 요청됨 · 확정 · 취소됨 · 닫힘 | 사용자 |
| 2026-11-26 | ext 키 = 병원당 하나(`partner` 제거) · 보낸 곳 = 선택 헤더 `X-Day-Client` · 새 키 발급 | 사용자 「ext키가 병원당 하나」 · 「새키를 만들고」 |
| 2026-11-26 | 유입 = 보내는 쪽이 골라 필수 · KOS 없는 칸은 메모에 「필드: 내용」 줄로 합침 · 담당자 = 누른 직원 | 사용자 |
| 2026-11-26 | 판정 = 이름(대소문자 · 띄어쓰기 무시) + 식별값 하나 이상 · 후보 화면 없음 | 사용자 「이름 + 조건 조합」 · 「그렇게 가자」 |
| 2026-11-26 | 웹 알림 = ADMIN · COORDINATOR · 문구 「답변 대기중」 · 「KOS 등록 실패」 | 사용자 |
| 2026-11-27 | 스웨거에 상태값 · 상태 × 행동 · 오류 코드 · 흐름 · 재시도 = 처음 응답 그대로 | 사용자 「이거 스웨거에 적어주고」 · SPEC |
| 2026-11-27 | 셸 「홈」→「현황」 · 로그인 뒤 = 예약 현황 · 현황 화면은 모든 직원이 봄 | 사용자 |
| 2026-11-27 | prod 키는 prod 배포 때 따로 새로 | 사용자 |

## 5. 날짜별 로그

- `2026-11-26` 시안 v10 → v15 확정 · ext 요청 본문 · 결정 RQ1 ~ RQ44 · SPEC-008 4차 검수 · Delivery #297 · BE/FE 구현 · 코드 2차 검수 · KOS probe 2 · e2e 1
- `2026-11-27` e2e 2 · 에이전시 요청 페이지 시안 v1 · ext 스웨거 보강 · 링키 안내서 · 셸 메뉴 · CENTURION_DAY#299 dev 배포 · dev Key Vault 새 키 · SPEC-008 stable(#968) · Delivery 마감 · 아카이브

## 6. 산출물


프로젝트와 당시 작업 문서는 `sync-work-links.py`가 만드는 작업 목차로 연결한다.
아래에는 판단의 근거가 된 리포트·PR·커밋을 구체적으로 남긴다.

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/968 (`d0fcc23a`)
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/299 (dev `65506f35`)

- `kknaksss/day-reservation3` → `dev`
  - `8a5ee874` feat(reservation): 예약 요청 스레드 — ext 요청 API · 예약 현황 「예약 요청」 · KOS 생성/수정/취소 · 셸 메뉴 현황 (#297)
- 리포트: `review-doc-1..5-report.md` · `review-code-1/2-report.md` · `be-probe-1/2-report.md` · `e2e-1/2-report.md` · `be-swagger-1/2-report.md` · `fe-nav-1-report.md` · `cleanup-1-report.md` · `agency-design-1-report.md`

## 7. 잔여

- **prod 배포** — prod 키 새로(병원마다 한 줄) → 링키 · 차티에 먼저 전달 · 확인 → Key Vault `day-prod-ext-partner-grants` 교체와 배포를 같이
- **외부 에이전시 요청 페이지** — 시안 v1(`design/20261127_에이전시요청_v1.html`) 사용자 피드백 · 질문 3(접근 방식 · 모바일 · 재진 고르기 `/customers/lookup`) → 새 작업 단위로
- 기획 통보: 정책 15 와 다름(후보 화면 없음 · 판정 규칙 · OQ-Q22) · 남은 문구(OQ-Q04) · OQ-Q05 · Q08 열린 채
- KOS 데모 지점에 시험 고객(중복 2명 포함) 남김 — 시험 예약은 0건으로 정리
- taewoo 리뷰(ext 키 변경) — PR #299 본문에 요청

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/day/day-reservation3/README|day-reservation3]]
<!-- work-links:end -->
