---
type: baseline
id: BASE-009
title: "전체현황판 「현황 › 예약 현황」 — 예약 → 접수 → 상담 → 귀가 정산(KOS 데모 지점 조사 15건)"
status: raw
product: cc-prototype
feature: procedure
source:
  type: conversation
  ref: "사용자 대화 2026-10-26(orchestration/work/overall-board/_RESUME.md §2 2026-10-26 줄 · §1 메모) · workflow-v3 · KOS 조사 리포트 15건 · KOS HAR 19개(gitignore)"
links:
  baselines:
    - "[[baseline-004-reservation-idea|BASE-004]]"
    - "[[baseline-008-procedure-board|BASE-008]]"
  decisions:
    - "[[decision-006-reservation-board|DEC-006]]"
  specs: []
  works: []
  releases: []
  related: []
created_at: 2026-10-26
updated_at: 2026-10-26
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/baseline
  - status/raw
---

# 전체현황판 「현황 › 예약 현황」

> 입력 기록이다. **새로 정한 것은 없다** — 정한 것은 DEC-006 이 갖는다. 이 문서는 무엇이 들어왔고 어디에 있는지,
> 그리고 그것을 읽고 **이해한 것**만 적는다.

## 들어온 것

2026-10-23 사용자가 시술 현황판을 「Ceramique 전체현황판」 시안으로 올리면서 **예약 현황은 「workflow 예약 구간 → KOS API 조사」 순서로 따로 간다**고 정했다(`_RESUME` 10-23). 2026-10-26 하루 동안 사용자와 예약 구간을 한 단계씩 닫았다 — 스케줄 표 · 예약 등록 · 이동 · 취소 · 접수(방 배정) · 상담 · 수납 · 귀가. 단계마다 KOS 화면 HAR 을 사용자가 떠 주고, researcher 가 데모 지점에서 조회(일부는 허가 받은 쓰기)로 확인했다. 같은 날 끝에 사용자 지시:

> **「코드까지 다 작성해서 알려줘 — e2e 로컬 해보게」**

BASE-004(10-10 예약 아이디어 — Linky → cc → KOS)의 「병원은 cc 에서 KOS 등록」 쪽이 이번에 구체화됐다. Linky(본사 예약 요청) 쪽은 아직 자리만이다.

## 원천

| 무엇 | 어디 |
|---|---|
| 결정 이력(SoT) | `orchestration/work/overall-board/_RESUME.md` §2 2026-10-26 줄 · §1 2026-10-26 메모 2줄(상담사 앱 알림 · 시술 현황판 2계층) |
| 업무 흐름(사용자와 닫음) | `reference/2026-10-26-cc-reservation/workflow-v3.md`(r2 · 418줄) |
| 화면 시안 | `reference/2026-10-23-cc-overall-board/design/Ceramique 전체현황판.dc.html` 「예약 현황」 `M:93-715` · 분석 `orchestration/work/overall-board/design-analysis-report.md` §3 · §6 · §7.2 · §9 · §10 · §11 |
| KOS 조사 리포트 15건(모두 2026-10-26) | `orchestration/work/overall-board/` 의 `reservation-read-report.md` · `reservation-questionnaire-report.md` · `reservation-visitor-update-report.md` · `reservation-create-report.md` · `reservation-room-report.md` · `reservation-reception-test-report.md` · `reservation-memo-test-report.md` · `reservation-move-cancel-report.md` · `reservation-consultation-report.md` · `reservation-payment-discharge-report.md` · `reservation-postpay-report.md` · `reservation-postpay-check-report.md` · `reservation-timeaxis-report.md` · `reservation-prescription-report.md` · `reservation-prescription-detail-report.md` |
| KOS HAR 19개 | `reference/2026-10-23-cc-overall-board/har/` — 예약현황_조회 · 설문전송 · 설문내용 · 고객정보 수정 · 예약 · 방배정 · 예약이동 · 예약상세_수정 · 예약취소 · 예약취소_되돌리기 · 예약부도 · 상담 · 수납 · 귀가 · 수납필요 추가 · 수납필요 확인 · 예약그룹 · 처방전 · 처방전상세. **전부 gitignore — 이름만 적는다.** 처방전 두 개는 데모가 아닌 실제 지점 HAR 이라 값을 어디에도 옮기지 않는다 |
| 같은 앱의 지금 계약 | DEC-005 · SPEC-003 0.5.1(시술 현황) · SPEC-004 0.3.2(계정 · 역할 · 앱) |
| 지금 코드 | `kknaksss/cc-prototype` 브랜치 `kknaksss/overall-board` `procedure/`(PR #6 · `d05cd88`) — KOS 클라이언트 · 동기화 · 계정 · 이벤트 로그 · 헤더 「현황」 드롭다운이 이미 있다 |

## 이해한 것

### 무엇을 만드는 화면인가

- 데스크(코디)가 데스크 PC 에서 쓰는 **하루 예약 판**이다. KOS 웹의 「예약 현황」(예약 그룹 칸 × 시각)과 같은 모양이고, 시안이 그 위에 예약 상세 · 등록 모달 · 오른쪽 패널을 얹었다
- 시술 현황(v2)이 「수납 뒤 ~ 귀가 대기」라면, 예약 현황은 그 **앞 구간**(예약 → 접수 → 상담)과 **뒤 끝**(귀가 대기 정산 → 귀가 완료)이다. 둘은 같은 KOS 일정을 본다

### 현장이 지금 KOS 에서 하는 일(AS-IS)

- **예약**: KOS 예약 화면 → 고객 검색 / 신규 고객 창 → 예약. 이동은 KOS [이동] 버튼(드래그 없음). 취소 · 부도는 사유 하나로 갈린다
- **접수 → 방 배정**: KOS 의 방 지정 화면(시술 진행판)은 시술 대기만 보여서, 화면 세 곳을 오가며 **접수 → 「방 배정」 기타 작업 추가 → 시술 대기로 올림 → 방 지정 → 상담 대기로 되돌림** 순으로 쓰기 5번을 한다
- **상담**: 상담사 지정 → 상담사가 방에서 KOS [상담 시작] · 상담 기록 · 시술 추가 · 수납 → 시술 대기 전환까지 KOS 에서 직접 한다. KOS 에는 상담사 「호출」이 없다
- **수납 · 귀가**: 수납은 KOS 수납 화면에서 쓰기 5번. 결제 뒤 추가 시술(후납)은 작업의 「수납 필요」로 뜨고, 수납 확정 때 꺼진다. 귀가는 단계 변경 한 번
- **처방전**: KOS 일정 상세의 「기타 업무」 탭에서 처방전 창을 열어 인쇄한다

### KOS 에서 확인된 것(리포트 요약 — 값은 적지 않는다)

- 하루 예약 카드는 내부 조회 1번(`get-schedules-for-reservation`)으로, 또는 공개 조회 8번으로 같은 집합이 온다. 칸 = 예약 그룹(데모 13개 · 운영 10–20시 · 간격 15/30/60분 · 정원은 구역별)
- 데모 지점 쓰기 시험으로 확인된 것: 접수 묶음(접수 → 「방 배정」 작업 → 방 지정 → 상담 대기, 시술 대기를 거치지 않아도 됨) · 공개 접수(`changeFlowStep RECEPTION`) · 공개 이동(`updateReservationV2`) · 공개 취소 · 부도 · 내부 취소 되돌리기 · 특이사항(`visitor.memo`) 쓰기
- HAR 로만 본 것(ccc 실호출 없음): 내부 예약 생성의 모든 칸 · 신규 고객 생성 · 내부 이동 · 상담사 지정 · 기존 고객 개인 정보 수정 · 귀가(`COMPLETED`)
- KOS 에 없는 것: 신분 확인 상태 · 상담사 지금 상태 · 상담사 호출 · 「상담 완료」 · 「후납 금액」 · 처방전 조회 공개 API · 본사 예약 요청 · 접수한 직원
- KOS 문진은 고객당 1건이고 다시 제출하면 덮어쓴다. 문진 제출은 성별 · 휴대폰 · 주소를 고객 정보에 반영한다
- 쓰기 뒤 조회에 보이기까지 0 ~ 3초가 걸린다. KOS 웹은 일정 변경을 소켓으로 받는다

### 사용자가 말한 방향(결정은 DEC-006)

- KOS 와 ccc 는 같은 데이터를 쓴다 — ccc DB 는 KOS 사본을 갖고 KOS 에 칸이 있으면 KOS 가 기준
- 시안이 정본이지만 KOS 와 다르면 KOS 칸에 맞춰 시안을 고친다 · KOS 에 없으면 안 쓰고 있으면 칸을 만든다
- 웹이 정본 · 앱(QR 문진 · 신분증 스캐너 · 상담사 알림)은 나중에 웹에 맞춘다
- 예약 구간은 상담사가 KOS 를 직접 조작한다 — 시술 구간의 「현장은 KOS 를 조작하지 않는다」(DEC-005 D-10)와 범위가 다르다

## 열린 것(입력 단계에서)

정할 것 42행은 workflow-v3 「정할 것」에 있다. 이번 판에 필요한 기본값 · 남은 질문은 SPEC-005 §10 이 갖는다.
