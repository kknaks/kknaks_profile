---
type: work
id: WORK-008
title: "전체현황판 시술 현황 다음 판 — 상태 2계층 · 드래그 놓기(W2) · 카드 한글 발음"
status: draft
product: cc-prototype
feature: procedure
work_type: enhancement
owner: kknaks
progress: 0
created_at: 2026-10-27
updated_at: 2026-10-27
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/work
  - status/draft
links:
  baselines:
    - "[[baseline-008-procedure-board|BASE-008]]"
  decisions:
    - "[[decision-005-procedure-board|DEC-005]]"
  specs:
    - "[[spec-003-procedure-board|SPEC-003]]"
    - "[[spec-005-reservation-board|SPEC-005]]"
  works:
    - "[[work-006-overall-board-undo|WORK-006]]"
  releases: []
  related: []
sources:
  - "orchestration/work/overall-board/_RESUME.md §2 (2026-10-26 「상태 = 2계층」 · 2026-10-27 시술 현황 줄) · §1 「시술 현황판 상태값도 2계층」 메모"
  - "orchestration/work/overall-board/review-code-r1.md W2"
  - "orchestration/work/overall-board/procedure-review-doc-r5-dispositions.md W1 ~ W5 (r8)"
  - "cc-prototype overall-board procedure/ (branch kknaksss/overall-board-2 901267f — 읽기만)"
---

# 전체현황판 시술 현황 다음 판 — 상태 2계층 · 드래그 놓기 · 한글 발음

시술 현황 화면 세 가지를 바꾼다 — ① 상태 표시를 예약 현황과 같은 **2계층**(주 상태 · 부상태)으로 ② 카드 드래그를 **판 안 어디에 놓든** 미리보기 자리로 확정(review-code-r1 W2) ③ 카드 고객 이름 오른쪽에 **한글 발음**. 계약은 **SPEC-003 0.6.0**(§5.12 「놓는 곳」 · **§5.14** · §6.3 · §9 #27 ~ #32 · 부록 K) — 이 문서는 빌드 계획만 적고 계약을 다시 쓰지 않는다.

> 1 파일 = 1 work = **빌드 계획**. 결정 원천 = `_RESUME` §2 2026-10-26 · 10-27 줄(SPEC-003 부록 K.1 대응표). 웹 화면 정본 = 배포된 구현본 — 시안과 대조하지 않는다.

## Meta

- Covers spec: SPEC-003 0.6.0(r7) — §5.2 · §5.9 · §5.12 · §5.14 · §6.2 · §6.3 · §6.4 · §9 #27 ~ #32 · §10 OQ-534 ~ OQ-537 · §10.1 #4 · #5
- 코드 레포: `kknaksss/cc-prototype` — 범위 **`procedure/front/**` 만** · **예외(r8)**: `procedure/back/app/service/fake_board.py` **예시 값만**(WP-FE3 — 카드 수 5 유지 · 이미 있는 카드의 값만 · back 시험 `tests/test_contract.py` 가 카드 5장을 본다). 그 밖의 back · 스냅샷 · `procedure/app/` · infra 는 건드리지 않는다(2계층 = 보여 주는 방법 · `phoneticName` 은 스냅샷에 이미 있음 — `back/app/schemas/board.py` `Customer.phoneticName`)
- base: 같은 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` · branch `kknaksss/overall-board-2`(③ 예약 잔여와 같은 branch · PR 하나 — `_RESUME` 10-27 「다음 판 = 한 slug · 한 PR」)
- 워커: frontend(WP-FE1 ~ FE3 — 한 워커가 차례로 또는 한 브리프) · reviewer · 코디(E2E)
- 검증은 WP 마다 그 범위만(tsc · lint · 가짜 보드 스크린샷). 전체 검증(build · compose · 데모 지점)은 WP-E2E 에서 한 번
- 배포: 이번 문서 범위 밖 — 사용자 E2E 통과 뒤 코디가 정한다

## 계약 고정점

| 고정점 | 값 | SPEC-003 |
|---|---|---|
| 상태 값 | 스냅샷 `cards[].state`(`waiting` · `doing` · `home`) · `procedures[].state`(`wait` · `doing` · `done`) **그대로** — front 가 2계층으로 바꿔 보인다 | §5.2 · §5.14 |
| 이름 · 색 | 예약 현황 구현 `components/reservations/view.tsx` 의 `phaseStyle` · `MAIN_TONE` · `stateText` 꼴 **값 그대로** — 시술 현황이 값을 새로 정하지 않는다(복사해 갈라지게 두지 않는다 — 가져다 쓰거나 공용 자리로 옮긴다 · 값 · 예약 현황 화면은 바뀌지 않아야 한다) | §5.14 |
| 놓기 | 판 = 가운데 흰 판(스크롤 컨테이너) 전체 — 가장자리 12px 포함(r8) · 판 안 놓기 = 마지막 미리보기 순서 저장 · 판 밖 · 취소 = 원래 순서 · 저장 API `PUT /api/board/order` 그대로 | §5.12 · §6.3 · §7.3 |
| 발음 | `card.customer.phoneticName` · 없으면 안 그림 · 이름 오른쪽 · 발음이 먼저 줄어듦 | §6.3 |

## Work Packages

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| **WP-FE1** | **상태 2계층** — §5.14 대조표 ● 줄 전부: ① 카드 머리 상태 Badge(덮어쓰기 「확인 필요」 · 「마취 중」은 그대로) ② 제목 줄 범례 ③ 현황 탭 「대기」 점 ④ 고객 탭 줄 Badge ⑤ 검색 결과 상태 글자 ⑥ 시술 줄 부상태 칩(자리 = §5.9 「오른쪽 칸 차례」 · 완료 Badge → 회색 칩 · 진행 줄 바탕 그대로) ⑦ 고객 탭 번호 원 시술 줄 글자 「진행 중」 → 「진행」(대조표 #14). `STATE_NAME` · `STATE_BADGE` 를 쓰는 곳을 **전부 grep 해서** 2계층으로 바꾼다(위 목록 밖에서 나오면 보고서에 적고 같은 규칙) | §5.14 · §5.9 · §6.2 · §6.3 · §6.4 | frontend | `procedure/front/components/procedures/**` · `procedure/front/app/(main)/procedures/live/page.tsx` · (공용으로 옮길 때만) `procedure/front/components/reservations/view.tsx` · 새 공용 파일 1개 | ○ 줄(덮어쓰기 · 이유 글자 · 원장 상태 · 되돌리기 글자 · 빈 상태)은 그대로 · 노란 「시술 대기」 0 · 예약 현황 화면 값 무변경 · 가짜 보드 스크린샷(대기 · 진행 · 귀가 대기 카드 · 세 줄 칩 · 범례 · 필터) | `cd procedure/front && npx tsc --noEmit && npm run lint` · `grep -rn "STATE_BADGE\|'warning'" components/procedures app/\(main\)/procedures` → 상태 Badge 용 0(「수납 필요」 warning 은 남음) | 대기 |
| **WP-FE2** | **드래그 놓기 W2** — 흰 판(스크롤 컨테이너 · 가장자리 12px 포함 — r8)에서도 `dragenter` · `dragover` 를 받아 놓기를 허락하고 `drop` 이면 마지막 미리보기(`drag.start` · `drag.from` · `drag.over` 의 방향 따라 끼우기) 순서로 저장 · 미리보기 = 시작 순서면 저장 없음 · 틈 · 빈 칸 · 귀가 대기 카드 위에서는 미리보기를 지우거나 바꾸지 않는다 · 판 밖 놓기 · Esc = 지금 `onEnd` 그대로(원래 순서). 카드의 `drop` 과 판의 `drop` 이 두 번 저장하지 않게(한 번만 — 저장 함수 한 곳) | §5.12 「놓는 곳」 · 「귀가 대기 카드」 · §6.3 드래그 | frontend | `procedure/front/app/(main)/procedures/live/page.tsx` · `procedure/front/components/procedures/OrderCard.tsx` · `view.ts`(필요하면) | §9 #29 · #30 이 로컬에서 재현 · 놓을 때 `PUT /api/board/order` 요청 수 = 1(틈) · 0(판 밖 · Esc · 미리보기 없음) — 브라우저 네트워크 탭으로 적는다 · 필터 중 · 경합(§5.12 「놓은 뒤 화면」) 회귀 없음 | tsc · lint · 가짜 보드는 순서 저장 403 이라(§6.3) **네트워크 요청 수만** 본다 — 화면 순서는 WP-E2E | 대기 |
| **WP-FE3** | **카드 한글 발음** — 고객 줄 차례 점 → 이름 → 발음 → 국적 → 첫/재내원 → 수납 필요 · `caption-md-400 gray-500` · 빈 값이면 요소 없음 · 이름 · 발음 한 줄 말줄임(발음이 먼저) · `title` 로 전체 · 가짜 보드 예시에 발음 있음 · 없음 · 긴 이름 + 긴 발음 각 1장(지어낸 값 — 실명 금지) | §6.3 | frontend | `procedure/front/components/procedures/OrderCard.tsx` · `procedure/back/app/service/fake_board.py`(예시 값만 · back 파일은 이것 하나 — Meta 예외(r8)) | 카드 폭 300 에서 칩 · 배지가 안 줄어들고 발음이 먼저 `…` · 스크린샷 3장 · (r8) 가짜 보드 **카드 수 5 유지 · 이미 있는 카드의 값만 바꾼다**(카드를 더하거나 빼지 않는다) | tsc · lint · (r8) `cd procedure/back && uv run pytest -q`(수 그대로) | 대기 |
| **WP-E2E** | **리뷰 + 코디 E2E(데모 지점)** — reviewer: SPEC-003 부록 K.1 의 절 전부 ↔ 코드 · K.2 기본값이 코드에 그대로인지 · §5.14 대조표 ● 줄 전부 바뀌고 ○ 줄 그대로인지 · 예약 현황 화면 값 무변경. FAIL 은 모아서 한 번에 수정 발주. 코디: `npm run build` · compose 재기동 → 데모 지점 §9 **#27 ~ #32**(브라우저 2개 · #32 에 (r8) 예약 현황 회귀 = SPEC-005 §9 #42 부상태 색 그대로) → 사용자 로컬 E2E(③ 예약 잔여와 같은 batch 로 모아도 된다 · 피드백은 모아서 한 번에) | §9 | reviewer · 코디 · frontend(수정) | `procedure/front/**` | 리뷰 PASS · §9 #27 ~ #32 통과(r8 — SPEC-005 §9 #42 부상태 색 그대로 포함) · 사용자 E2E 통과 | `cd procedure/front && npx tsc --noEmit && npm run lint && npm run build` · `cd procedure/back && uv run pytest -q`(수 그대로 — 바뀐 back 은 `fake_board.py` 예시 값뿐 · r8) | 대기 |

## 병렬

```text
WP-FE1 ─┐
WP-FE2 ─┼─ WP-E2E
WP-FE3 ─┘
```

- 세 WP 는 서로 다른 관심사지만 **같은 파일**(`OrderCard.tsx` · `live/page.tsx`)을 만진다 → 워커 하나가 차례로(FE1 → FE2 → FE3) 하거나, 한 브리프로 묶는다. 둘로 나누면 같은 파일 충돌
- back 이 없다 → BE 를 기다릴 것이 없다. 가짜 보드(`PROC_FAKE_BOARD`)로 FE1 · FE3 스크린샷 · 실제 back(데모 지점)으로 FE2

## 하지 않는 것

- back · 스냅샷 모양 · DB · KOS 쪽 — 2계층은 front 표시 · 발음은 이미 스냅샷에 있음 (예외: 가짜 보드 `fake_board.py` 예시 값 — Meta · r8)
- 시술실 앱(`procedure/app/`) — 2계층 · 발음은 SPEC-003 §10.1 앱 후속 4 · 5(웹 기준)
- 시술 차트(KOS 간호관리차트 · 의사차트 · 시술 메모) — 이번 판은 workflow-v2 「시술 차트 — 흐름 초안」까지(계약 아님 · 사용자 흐름 결정 + KOS 쓰기 HAR 뒤 다음 판)
- KOS 실시간 소켓 검토 · SPEC-003 OQ-528(K5) — 따로
- 시안 파일 수정 · 시안 대조 — 웹은 구현본이 정본

## 주의

- public 레포 — KOS 키 · 토큰 · 실명 · 연락처 · KOS id 값을 코드 · 가짜 보드 예시 · 스크린샷 · 리포트에 넣지 않는다(발음 예시도 지어낸 값)
- 워커는 사용자 포트(3600 · 8600 · 3700 · 8700)의 사용자 프로세스를 죽이지 않는다
- 코디: 커밋 뒤 compose 를 다시 올리고 E2E(옛 코드가 떠 있는 채로 확인 금지)
- 완료는 사용자 표면(웹 시술 현황 화면)에서 — 스크린샷 · tsc 만으로 done 하지 않는다

## 열린 것 (2026-10-27)

| 무엇 | 지금(기본값) | 근거 |
|---|---|---|
| 시술 줄 칩 자리 · 진행 줄 바탕 | 오른쪽 칸 · 바탕 그대로 | SPEC-003 OQ-534 |
| 덮어쓰기(확인 필요 · 마취 중)가 2계층을 가림 | 그대로 | SPEC-003 OQ-535 |
| 발음을 카드 밖에도 | 카드만 | SPEC-003 OQ-536 |
| 범례 = 주 상태 색 vs 카드 Badge 꼴 | 카드 Badge 꼴 | SPEC-003 OQ-537 |
