---
sot: here
status: active
---

# Agency Settlement

에이전시 수수료 정산 PoC. 병원(운영 명동점)과 에이전시가 「이 손님들이 이만큼 결제했다」를 서로 확인하는 것이 쓰임새다.
첫 판은 **운영 KOS 결제를 월 단위로 품목 한 줄씩 보여 주는 리스트**(DEC-001). 수수료율(상품별) · 에이전시별 보여 주기는 그 위의 다음 판.
cc-prototype 과 **같은 방식**(문서 = 이 폴더 · 코드 = 별도 레포 · 오케스트레이션)의 별도 프로젝트이고, 디자인만 cc-prototype `procedure/front` 를 복사해 쓴다.

## 코드 위치

| 항목 | 경로 |
|---|---|
| 코드 레포 | `https://github.com/kknaksss/agency-settlement`(private) · 로컬 `/Users/kknaks/git/toy_pr2/agency-settlement` |
| 디자인 원천 | `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/front` (읽기만 · 복사) |
| 오케스트레이션 설정 | `orchestration/config/projects/agency-settlement.json` |

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | 조사 리포트(운영 KOS · 레포 밖 private 보관) | — |
| Decision | DEC-001 accepted (D-01 ~ D-18) | — |
| Spec | SPEC-001 0.4.3 draft (구현 동기) | OQ-132 사용자 답 |
| Work | WORK-001 1 · 2 · 3판 완료 · 코드 PR kknaksss/agency-settlement#1 | 사용자 화면 확인 · 마감 |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | [입력](00-baseline/README.md) |
| 10-decision | [결정](10-decision/README.md) |
| 20-spec | [스펙](20-spec/README.md) |
| 30-work | [구현 계획](30-work/README.md) |

## 최근 로그

- 2026-10-29: 구현 — 운영 KOS 조회 전용 · SQLite 저장/증분 · 에이전트별 탭 · 엑셀 · 최종 결제만(D-18) · 코드 PR #1

- 2026-10-29: 착수 — 운영 명동점 KOS 조사 · 에이전시 판정 = 고객 최초 유입 채널 · 월별 매출 리스트(DEC-001 · SPEC-001 · WORK-001). cc-prototype 안에 잘못 두었던 문서를 이 프로젝트로 옮김
