
# [planner] DAY-SPEC-000 · ERD — 메뉴 · 결제 · 시술권 · 선불카드 · 처방 테이블 반영

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 맥락이 없다 — 아래 파일이 전부다. 이 워크트리는 너 혼자 쓴다(검수 워커는 네가 끝난 뒤 읽기만).

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-18-day-customer/erd-draft.md` ← **계약의 SoT (사용자와 11-18 에 전부 닫은 ERD v1).** 테이블 · 관계 · 핵심 칸 · 정한 것 전부 여기. **여기 없는 건 발명하지 마라.** 「열린 것」 표는 열린 것으로 옮긴다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/har-check-report.md` · `har-check-report-2.md` · `har-check-report-3.md` — KOS 실측 근거(필드 이름 · 값 · 명령). 칸의 「외부(KOS)」 열은 여기서 가져온다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-18-day-customer/customer-erd.md` — 지금 prod 의 고객 쪽 테이블.
- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-03-cc-day/erd/README.md` (공통 규칙) · `04-1-menu.md`(메뉴 원천 — SPEC-000 §4 의 원천) · `05-task.md`(표 형식 본)
- 원본 HAR(필요할 때만 · 개인정보 — 값 옮기지 마라): `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-18-day-customer/har/*.har` · 특히 `수납추가.har`(시술 외 품목) · `결제취소2.har`(취소 뒤 카드 그대로)
- 지금 prod 코드(읽기만): `git -C /Users/kknaks/git/CENTURION_DAY show origin/prod:<path>` — `backend/day/models/` (실제 테이블 · 칸). 경로는 `git -C /Users/kknaks/git/CENTURION_DAY ls-tree -r --name-only origin/prod | grep models` 로 찾아라.

**기대는 개념** — 해당 없음(아래 §2 의 두 조건이 판단 기준이다).

## 2. 배경 / 무엇을 바꾸나

지금 DAY-SPEC-000(0.0.1 · stable)은 「1차 = KOS 연동 기간 · 메뉴 테이블 없이 스냅샷만 · 결제 · 시술권 · 선불카드 없음」이다.
사용자 결정(2026-11-18): **예약 구현 뒤 DAY 가 고객 · 구매 · 시술권 · 선불카드의 원천이 되고 KOS 로 보낸다.** 그래서 메뉴(시술 · 시술 외 품목 · 선불카드 상품) · 구매 · 거래 · 시술권 · 선불카드 · 처방(최소) 테이블을 DAY 에 둔다. ERD v1 이 그 결과다 — 이걸 메디니스 정본(SPEC-000 칸 계약 → `40-architecture/erd.md` 개략도 · 인벤토리)으로 옮긴다.

**두 조건 — 모든 칸 · 문장의 판단 기준 (사용자 11-18 강조)**
1. **상용 서비스가 이미 나가 있다** (CENTURION_DAY prod `a6aa4ba5` · KOS → DAY 동기화 10초/1시간이 돈다).
   - 지금 prod 테이블 · 칸은 **이름 · 타입을 바꾸지 않는다.** 새 테이블 · nullable 새 칸만(더하기). 예: `visit_task.medicines` 유지 · `machines` · `treatment_item_id` · `ticket_id` 추가.
   - 테이블마다 **「prod 에 있음 / 새 테이블 / 칸만 추가」** 를 표시한다(prod 모델을 직접 열어 확인 — 추측 금지).
   - 원장 전환 전(지금)은 새 테이블도 **KOS → DAY 동기화로 채운다** + 기존 고객 이력 **백필**. 전환 뒤엔 DAY → KOS(outbox). 전환 시점 · 절차는 Open Question.
2. **나중에 KOS 를 뗀다.**
   - KOS id · 동기화 칸은 `external_ref` 에만(기존 규칙). 상태 · 종류 enum 은 **DAY 말**(KOS 문자열 · 오타 `ETCETRA_PRODUCT` 는 「외부(KOS)」 열 · 매핑에만).
   - KOS 가 대신 해 주던 일 — 구매 확정 때 시술권 N장 생성 · 선불카드 상품 확정 때 카드 생성 + 충전 이력 · 잔액 · 결제 합계 · 부분 환불 금액 — 을 **DAY 칸만으로 할 수 있는지** 주제마다 한 줄씩 적는다.
   - KOS 응답에만 있고 DAY 가 계산할 수 있는 값(카드 총액 · 티켓별 가격)은 칸으로 두지 않는다(ERD v1 대로).

## 3. 계약

해당 없음(문서 단계). 칸 이름 · 테이블 이름은 ERD v1 그대로 — `treatment` · `treatment_item`(KOS `procedure` · `medicalService` · 기존 SPEC-000 §4 의 `procedure` · `medical_service` 를 이 이름으로 바꾼다 · 피부과엔 「진료」가 없다 — 사용자).

## 4. 먼저 읽을 핵심 파일 (이 워크트리)

- `products/day/20-spec/spec-000-data-model.md` — §1(범위 · 주제 표) · §2 공통 규칙 · §3 주제별 표 형식 · §4 메뉴(자체 운영) · §6 OQ. **표 형식(묶음 · 필드 · 타입 · 필수 · 설명 · 외부(KOS))을 그대로 따른다.**
- `products/day/40-architecture/erd.md` — 개략도 · 인벤토리 · 「ERD 갱신 규칙」(SPEC-000 먼저 → 개략도 · 인벤토리).
- `products/day/40-architecture/system.md` §「원장 두 단계」(133~) — 지금 사실(연동 기간 = KOS 원장)과 새 결정의 관계.
- `products/day/20-spec.md` · `products/day/README.md` — SPEC 목록 · 범위 문장(「메뉴는 설계만 · 1차는 스냅샷만」 문장들).
- `products/day/10-decision.md` 머리말 — **구현 · 계약 결정은 SPEC 본문에 둔다(DEC 엔티티 없음).** 결정권자 escalation 이 아니면 여기에 쓰지 않는다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 구현 단계

1. **SPEC-000 고치기** (버전 올림 · `last_updated` 2026-11-18 · `sources` 에 위 SSOT 경로 추가)
   - §1 범위 · 주제 표: 메뉴 · 결제 · 시술권 · 선불카드 · 처방이 들어온다. 원장 전환 결정(2026-11-18 · 사용자) 한 단락.
   - 메뉴 절(지금 §4): 「1차에서 만들지 않음」 해제 · 이름 변경(`treatment` · `treatment_item` · `treatment_item_medicine` · `treatment_item_machine`) · `product_option` 옵션 단위 칸 · 새 테이블 `etcetera_product_category` · `etcetera_product` · `prepaid_card_product`. `etc_task_type` 등 기존 것은 그대로 둔다(ERD v1 이 말하지 않은 건 건드리지 않는다).
   - 새 주제 절 — 구매(`purchase` · `purchase_item` · `purchase_price_adjustment` · `purchase_transaction` · `purchase_assignee`) · 시술권(`ticket_bundle` · `ticket_set` · `ticket`) · 선불카드(`prepaid_card` · `prepaid_card_customer` · `prepaid_card_ledger`) · 처방(`prescription`). 테이블마다 칸 표 + 「정한 것」(ERD v1 의 근거 번호) + 「결제 취소 ≠ 환불」 표 + KOS 없이 되는지 한 줄 + prod 표시.
   - 기존 테이블에 더하는 칸: `visit_task`(`treatment_item_id` · `ticket_id` · `machines`) — 05 절 표에 「추가(2026-11-18)」로. 다른 기존 표는 ERD v1 이 말한 것만.
   - `purchase_price_adjustment` · `purchase_assignee` 처럼 ERD v1 이 칸을 안 적은 테이블은 HAR 리포트에서 확인된 칸만 · 없으면 「칸 미정 — OQ」.
   - §6 OQ: ERD v1 「열린 것」 표 전부 + 원장 전환 시점 · 절차 + 백필 범위 + 시술 외 품목 과세 출처.
2. **`40-architecture/erd.md`**: 갱신 규칙대로 — 1차 관계도에 새 관계 · 메뉴 관계도 이름 변경 · 「1차에서 만들지 않음」 정리 · 인벤토리 표에 새 테이블(책임 1줄 · 핵심 키) · 개수 문장.
3. **`40-architecture/system.md`** 「원장 두 단계」: 지금 사실은 그대로 두고 「예약 구현 뒤 DAY 원장으로 전환(2026-11-18 결정 · 시점은 SPEC-000 OQ)」 한 줄. 그 이상 고치지 않는다.
4. `20-spec.md` · `README.md` 의 「메뉴는 설계만 · 1차는 스냅샷만」 문장 · SPEC-000 범위 요약을 맞춘다(그 문장만).
5. 검증(§8) 후 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/spec-change-report.md` — 바꾼 파일 · 절 · 새 테이블 수 · prod 표시 표 · KOS 없이 되는지 표 · ERD v1 과 다르게 쓴 곳(있으면 이유) · lint 결과.

## 7. 범위 제약 — 하지 말 것

- ERD v1 에 없는 테이블 · 칸 · 정책을 만들지 마라. 열린 것은 OQ 로.
- HAR 값(고객 이름 · 전화 · 차트번호 · 직원 실명 · 메모 · KOS id · tenant id)을 문서에 옮기지 마라 — 필드 이름 · 타입 · 건수 · 상품 이름(메뉴 이름은 공개 정보)만.
- SPEC-001~005 · WORK · 화면 문서는 건드리지 않는다(SPEC-000 범위 밖 영향이 보이면 리포트에 「영향」으로만).
- `10-decision.md` 에 DEC 를 만들지 마라.
- 커밋 · push · PR 금지.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- ERD v1 의 테이블 이름 전부가 SPEC-000 에 칸 표로 있는지 grep 표(테이블 → SPEC-000 줄)를 리포트에 남긴다.
- 개인정보 grep: `grep -nE '01[0-9]-?[0-9]{3,4}-?[0-9]{4}|[0-9a-f]{24}' <바꾼 파일>` 0 건.
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --from term_0b073cd0-5d97-47e2-8cfa-362508da4e65 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
