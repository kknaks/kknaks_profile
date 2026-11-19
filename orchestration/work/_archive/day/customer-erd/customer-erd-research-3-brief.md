# [researcher] 3차 — 환불 · 시술 사용 후 환불 · 선불카드 공유 · 시술권2

너는 **day `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디네이터와 같은 워크트리다. 리포트 파일 1개 말고 아무 파일도 만들거나 고치지 마라(특히 `erd-draft.md`).

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/har-check-report.md` · `har-check-report-2.md` ← 네 1 · 2차 리포트. 형식 · 근거 표기 · 금지 규칙 같다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-18-day-customer/erd-draft.md` — 초안. 「1차 HAR 확인 뒤 정한 것」 6(공유 고객 추가) · 9(가격은 번들에만 · 부분 환불 (b))이 이번에 바뀐 사용자 결정이다(읽기만).
- 1차 브리프 `customer-erd-research-brief.md` §7 범위 제약 · §8 검증 — 그대로.

## 2. 배경

사용자가 KOS 에 **환불** 흐름(취소와 다름)과 **선불카드 공유 고객**이 있다는 걸 보여 줬다. 코디가 훑어본 것(검증 대상 — 그대로 믿지 말고 확인):
- 환불 = `start-purchase-refund` → `mark-purchase-items-for-refund{refundingItems[{targetItemId, adjustedPrice}]}` → `add-canceled-transaction` → (`add-transaction`) → `complete-purchase-refund`. 상태 `REFUNDED` · `PARTIALLY_REFUNDED` · 진행 `REFUNDING`.
- 크라이오 5회권 1회 사용 뒤 환불: adjustedPrice 65,780 · 전액 취소 −328,900 → 재결제 +65,780 → `PARTIALLY_REFUNDED`.
- `환불1` · `환불2` 는 **선불카드 상품(멤버십)** 환불로 보인다. `환불2` 는 한 구매가 `REFUNDING` 으로 끝난다.
- 공유: `add-visitor-to-prepaid-card{id, visitorId}` · `get-prepaid-card-visitors → [{visitorId, owner}]`.

## 3. 계약

해당 없음.

## 4. 입력 — `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-18-day-customer/har/`

- `환불1.har` · `환불2.har` · `시술사용후환불.har` · `시술권2.har` · `선불카드공유.har`
- 앞 HAR 들은 비교용.

## 5. allowed_paths

- 리포트 1개만 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/har-check-report-3.md`
- 그 밖 전부 읽기만.

## 6. 할 일

- **S1 환불 흐름** — 명령마다 요청 body 전체 키 · 순서 · 응답. `refundingItems` 한 건 구조(`adjustedPrice` 분해 포함) · `revokingItems` 와의 차이. 상태 · 진행 값 전이표(구매 단위). 취소(1차 `add-canceled-transaction` 단독)와 환불의 차이를 표로.
- **S2 부분 환불 금액** — `시술사용후환불` 의 adjustedPrice 가 「번들 ÷ 회차 × 쓴 횟수」와 맞는지 · 화면이 금액을 계산해 준 흔적(조회 경로 · 이벤트)이 있는지 · 직원이 고친 흔적이 있는지. 환불 뒤 구매 항목 `price` · `priceV2` · `basePrice` 가 바뀌는지.
- **S3 시술 사용** — `시술사용후환불` 앞부분 `add-flow-tasks` → `change-tasks-*` 로 티켓이 `USED` 가 되는 지점 · 작업이 티켓을 가리키는 칸(`ticketConfiguration{ticketId, round}`) · round 값(1차 · 2차에서 확인 안 됨).
- **S4 환불된 시술권** — 환불 뒤 티켓이 어떻게 되나. HAR 에 환불 뒤 시술권 조회가 없으면 「확인 안 됨」. `시술권2.har` 는 어느 시점인지(환불 1 · 2 와의 순서) 확인하고 그 안의 번들 · 티켓 상태 표.
- **S5 선불카드 상품 환불** — `환불1` · `환불2`: 환불 뒤 카드 잔액 · 충전 이벤트 · 카드 존재(삭제/사용 완료?) · `REFUNDING` 으로 끝난 구매가 무엇인지. 사용자 의견: 「취소하면 카드도 소프트 딜리트돼야 하지 않나 · KOS 에도 취소 이력 남겨야」 — KOS 가 실제로 무엇을 하는지만 적어라.
- **S6 선불카드 공유** — `선불카드공유.har`: 추가 명령 · 목록 응답 전후 · `owner` · 공유 고객이 카드를 쓸 때 이력(`visitor`)이 어떻게 남는지(있으면). 제거 명령이 있는지.
- **S7 초안 대조** — 새 사실 중 `erd-draft.md` 에 담을 칸 없는 것 · 정한 것과 어긋나는 것 · 정할 것(결정 금지). 특히: 구매 상태값 목록 · `purchase_item` 환불 표시/조정 금액 칸 · 선불카드 상품 환불 시 카드.
- 리포트 끝에 「여전히 확인 안 됨 — 필요한 HAR」 표.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
