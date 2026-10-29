---
type: decision
id: DEC-001
title: "월별 매출 리스트 — 운영 명동점 KOS 결제를 품목 한 줄씩 · 에이전시 판정 = 고객 최초 유입 채널 · 수수료는 나중"
status: accepted
product: agency-settlement
created_at: 2026-10-29
updated_at: 2026-10-29
tags:
  - product/agency-settlement
  - feature/monthly-sales
  - doc/decision
  - status/accepted
links:
  baselines: []
  decisions: []
  specs:
    - "[[spec-001-monthly-sales-list|SPEC-001]]"
  works:
    - "[[work-001-monthly-sales-list|WORK-001]]"
  releases: []
  related: []
up: []
sources:
  - "orchestration/work/agency-settlement/_RESUME.md §2 — 2026-10-29 줄 전부"
  - "orchestration/work/agency-settlement/research-agency-attribution.md — 운영 명동점 10-01~10-28 수집본 조사(Q1~Q7)"
---

# 월별 매출 리스트 — 결정

> 기능 계약은 SPEC, 작업 순서는 WORK 가 갖는다. 이 문서는 무엇을 정했는지만 갖는다.
> 결정 원천은 `orchestration/work/agency-settlement/_RESUME.md` §2 — **이 문서와 `_RESUME` 가 다르면 `_RESUME` 가 맞다.**

## Context

병원(운영 명동점)이 에이전시가 데려온 손님의 수수료를 정산하려 한다. 병원과 에이전시가 「이 손님들이 이만큼 결제했다」를 서로 확인하는 것이 쓰임새다. 수수료율은 **손님이 산 상품마다 다르다.** 그래서 먼저 **결제 내역을 상품 한 줄씩 빠짐없이 뽑는 리스트**가 있어야 하고, 수수료 · 에이전시별 보여 주기는 그 리스트 위의 필터로 뒤에 붙인다(사용자 「일단 결제 리스트를 먼저 뽑으면 나중에 보여주는 것만 필터링」).

조사(research-agency-attribution.md)로 확인한 것: 결제 통계 · 품목 통계 둘 다 고객의 최초 유입 채널(`visitorFunnelName`)을 들고 온다 · 10월 승인 수납 392건 전부 품목이 있다 · 품목 금액 합 = 결제 합(444/444) · 결제 수단(카드 · 현금)은 품목과 이어지지 않는다.

근거 칸 표기: **사용자 지시** = 사용자가 말한 것 / **코디 기본값** = 코디 제안 · 사용자에게 통보.

## 근거 개념

- [[no-inference-from-free-text]] — 에이전시는 구조화 필드(최초 유입 채널)로만 판정한다. 메모 · 상세 유입(자유 텍스트)에서 추정하지 않는다

## Decision

| ID | 결정 | 근거 |
|---|---|---|
| D-01 | **첫 화면 = 월별 매출 리스트.** 월을 고르면(기본 = 이번 달 · 10월부터 확인) 그달 결제 내역이 나온다. 수수료 계산 · 에이전시별 필터 · 엑셀은 이번 판 밖 | 사용자 지시 — 「일단 10월 매출 조회 · n월 매출 조회 · 월별 매출 조회를 하는 걸 하자」 · 「수수료율 계산은 일단 나중에」 |
| D-02 | **한 줄 = 품목 하나.** 같은 수납의 품목은 묶어 보인다(수납 → 품목들). 금액은 **품목 금액**. 결제 수단 · 분할 결제는 수납 단위 참고로만 | 사용자 확인 — 「a 손님이 쥬베룩 · 써마지 구매하면」 예시에 「응 맞아」 |
| D-03 | **줄에 보이는 칸**: 결제일 · 손님 이름 · 방문일 · 최초 유입 채널 · 수납 · 상품 · 옵션 · 품목 금액 · 상태(승인 · 취소 · 환불). 이름은 가리지 않는다(병원 내부 화면) | 사용자 지시 — 「이름 · 방문일 · 결제액 같이 보여 줘야지」 |
| D-04 | **에이전시 판정 = 고객의 「최초 유입 채널」**(`visitorFunnelName` · KOS 고객 상세 「최초 유입 채널 정보」). 예약 유입(`reservationFunnelName`)이 아니다 | 사용자 지시(KOS 고객 상세 화면 · 「유입 채널 이걸로 보라고」) |
| D-05 | **데이터 = 운영 명동점 KOS 조회만.** `/queries/` 만 부르고 쓰기는 없다. 원천: ① 결제 통계(`getTransactionStatistics`) · ② 품목 통계(`getPurchaseItemStatistics`) · ③ 이름 · 방문일 = `findScheduleByPurchaseId`(없으면 ④ `getVisitor` 로 이름만) · ⑤ 수납(`getPurchaseSummaries`) — 승인 · 취소 시각과 첫 승인 판정 | 사용자 지시(운영 조회 허용 · 10-29) · 조사 리포트 Q5 · Q6 · `_RESUME` §2(③ 정정 · ⑤ 추가) |
| D-06 | **월 귀속 = 결제 시각(KST) 기준**(① 결제 행이 들어온 달). 취소 · 환불은 취소된 달에 음수 줄로 보인다(원 결제 달을 고치지 않는다). **결제일 칸 = ⑤ 승인 시각**(취소 줄은 취소 시각). **분할 결제가 달을 넘으면 품목 줄은 취소 안 된 첫 승인 결제가 귀속된 달에만**, 다른 달엔 결제 · 취소 줄만 | 코디 기본값 · 사용자 통보 — KOS 결제 통계가 취소를 별도 행 · 취소 시각으로 준다(리포트 Q6) · `_RESUME` §2(분할 결제 · 결제일 줄) |
| D-07 | **선불카드 · 기타 상품도 빼지 않고 보인다** — 품목 종류(`purchaseItemType`)를 칸으로 보여 주고, 충전 · 사용 이중 계산은 뒤의 필터가 정한다. 상품명이 빈 품목은 선불카드명 · 기타 상품명 칸에서 이름을 읽는다 | 코디 기본값 — 「리스트 먼저 · 필터는 나중」(D-01) · 리포트 Q6 ⚠ |
| D-08 | **별도 프로젝트 `agency-settlement`** — 코드 레포 `kknaksss/agency-settlement`(private) 루트에 `back/`(FastAPI) + `front/`(Next.js). cc-prototype 과 같은 방식(문서 · 오케스트레이션)이지만 cc-prototype 의 기능 폴더가 아니다. **디자인 = cc-prototype 것**(`procedure/front` 의 토큰 · 컴포넌트를 `front/` 로 복사 — import 금지) | 사용자 지시 — 「다른 프로젝트인데 cc 같은 거」 · 「디자인 시스템은 cc-prototype 쓸 거야」 · 이름 · 레포는 사용자 선택(10-29) |
| D-09 | **로컬에서만 띄운다.** 운영 고객 이름 · 결제가 보이는 화면이라 배포는 따로 정한다 | 코디 기본값 |

## 열린 것

- 수수료율(상품별) · 에이전시별 보여 주기 · 에이전시 확인 절차 — 다음 판
- 계약에서 남는 것(조회를 요청마다 할지 저장해 둘지 · 이름 · 방문일을 어느 작업에서 읽을지 · 월 경계 시간대)은 SPEC 의 OQ 에 기본값과 함께 둔다
