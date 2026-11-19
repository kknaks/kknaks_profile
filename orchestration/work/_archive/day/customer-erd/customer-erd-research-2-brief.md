# [researcher] 2차 — 새 HAR 4개로 시술권 행 수 · 선불카드 충전/이력/취소 확인

너는 **day `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디네이터와 같은 워크트리다. 리포트 파일 1개 말고 아무 파일도 만들거나 고치지 마라(특히 `erd-draft.md`).

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/har-check-report.md` ← **네 1차 리포트.** 「확인 안 됨 — 필요한 HAR」 표가 이번 질문이다. 형식 · 근거 표기 · 금지 규칙은 1차와 같다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-18-day-customer/erd-draft.md` — 초안. 「1차 HAR 확인 뒤 정한 것」 1~9 가 사용자 결정이다(읽기만 · 고치지 마라).
- 1차 브리프 `customer-erd-research-brief.md` §7 범위 제약 · §8 검증 — 그대로 적용.

## 2. 배경

1차에서 새 HAR 6개에 시술권 탭(`get-ticket-bundles`) 호출이 0이라 티켓 행 수 등이 남았다. 사용자가 같은 데모 고객으로 HAR 4개를 더 떴다.

## 3. 계약

해당 없음.

## 4. 입력 — `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-18-day-customer/har/` 의 새 HAR 4개

- `고객정보.har` — 고객 상세(시술권 탭 · 선불카드 · 일정 상세 포함)
- `선불카드생성.har` — 선불카드 생성(충전 이벤트 조회 경로 있음)
- `선불카드결제.har` — 선불카드 상품 결제 흐름(`prepaid-card-product` 있음)
- `선불카드결제취소.har` — 위 결제 취소

1차 HAR 10개는 비교용. 미리 본 새 경로: `purchase/prepaid-card/v1/queries/get-prepaid-card-charging-events` · `get-prepaid-card-visitors` · `procedure-menu/prepaid-card-product/v1/queries/get-prepaid-card-product`.

## 5. allowed_paths

- 리포트 1개만 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/har-check-report-2.md`
- 그 밖 전부 읽기만(1차 리포트도 고치지 마라).

## 6. 할 일

1차 리포트 「확인 안 됨 — 필요한 HAR」 표의 줄마다 **닫힘 / 여전히 확인 안 됨**과 답 · 근거를 적는다. 특히:

- **R1 다회권 티켓** — 크라이오 진정관리 5회 번들의 `ticketSets[].tickets[]` 행 수 · 티켓별 가격(합 · 나머지) · 상태 · 구매 직후 상태. 일정 상세 `ticketConfiguration.round`.
- **R2 결제 취소된 구매의 시술권**(1차 구매 B) · **R3 용량 변경 구매의 시술권**(1차 구매 A — 보톡스 1000 · 쥬베룩 2행이 번들 몇 개인지 · 세트 제목 · unit · 가격).
- **R4 선불카드 충전 이력** — `get-prepaid-card-charging-events` 요청 · 응답 구조, `chargingId` 가 여기 id 인지, 충전 · 사용 · 취소가 각각 이벤트로 남는지.
- **R5 선불카드 상품 결제** — `prepaid-card-product` 구조(메뉴에 선불카드 상품이 따로 있나), 금액 충전이 **구매 · 구매 항목을 만드는지**(항목 `type` 값), 결제 뒤 카드 금액 · 포인트 변화.
- **R6 선불카드 결제 취소** — 취소 거래 모양 · 카드 잔액 복구 · 충전 이벤트 변화.
- **R7 `get-prepaid-card-visitors`** — 무엇인가(카드 공유 고객?) · 구조. 사용자 결정: 선물(구매자 ≠ 소유자)은 지금 없음 — 사실만 적고 결정하지 마라.
- **R8 일정 `purchaseIds[]`** — 일정 상세에 있나.
- **R9 초안 대조** — 새 사실 중 `erd-draft.md` 에 담을 칸이 없는 것 · 「정한 것」 1~9 와 어긋나는 것. 정할 것은 「정할 것」으로만.

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
