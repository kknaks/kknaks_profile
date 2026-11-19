
# [planner] 2차 — KOS → DAY 동기화 스펙(SPEC-002 개정) + SPEC-000 칸 3개 수정

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 맥락이 없다 — 아래 파일이 전부다. 이 워크트리는 너 혼자 쓴다(검수 워커는 네가 끝난 뒤 읽기만).

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/kos-sync-research-report.md` ← **동기화 사실의 SoT**(테스트 계정 · DEMO 테넌트 실호출). 경로 · 요청 키 · 건수 · 「동기화 스펙에서 정할 것」 1~10. **여기 없는 경로 · 필드를 지어내지 마라.**
- `products/day/20-spec/spec-000-data-model.md` §4(새 테이블 · 「외부(KOS)」 열) · §6 OQ — 머지된 #951 그대로(이 워크트리 = origin/main).
- `products/day/20-spec/spec-002-procedure-board.md` — 지금 동기화 계약(특히 「KOS 읽기 — 동기화 추가분」 L795~ · §5 OQ). **이 SPEC 을 개정**한다.
- 지금 동기화 코드(읽기만): `git -C /Users/kknaks/git/CENTURION_DAY show origin/prod:backend/day/tasks/emr.py` · `backend/day/emr/sync.py`(`_apply_schedules` 창 · `mark_absent(within=…)` · `lock_visits`) · `backend/day/emr/kos/client.py`(시스템 계정 자동 해제 S-8) · `backend/day/queries/board.py`(`load_world` = 오늘 `reserved_start_at` 창).
- 앞 판: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/spec-change-report.md` · `review-spec-report-2.md`.

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

#951 로 테이블이 정해졌다. 원장 전환(예약 구현) 전까지 그 테이블을 **KOS → DAY 동기화 + 지난 이력 백필**로 채운다. 조사(위 리포트)로 경로는 확인했다. 이제 **동기화 계약**을 SPEC-002 에 쓴다. 두 조건(상용 운영 중 — 더하기만 · KOS 뗄 것 — `external_ref` 만)은 그대로.

## 3. 사용자 결정 (2026-11-19 · 「추천으로 가자」) — 이대로 쓴다

리포트 「정할 것」 번호:
1. 오늘 고객 시술권 · 카드 = **그 고객의 구매(`lastUpdatedDateTimeUtc`)나 작업 티켓(`ticketConfiguration.ticketId`)이 바뀌었을 때만** 조회(10초 회차 안). 10초마다 전부 하지 않는다.
2. 오늘 밖 고객의 변경 = 공개 거래 통계 · 카드 이벤트 통계를 「지난 회차 시각부터」 받는 **병원 전체 회차 5분마다**(OQ-00-4 닫음).
3. 데이터 원천 = **내부 API**(삭제 구매 보임 · 옵션 → 시술 항목 연결 · 시술권 전체). 공개 통계는 **id 모으기에만**.
4. 시술권 = 내부 `get-ticket-bundles`(전체 상태).
5. KOS 값 → DAY enum = 동기화 스펙의 **매핑 표**. 실측된 값(구매 `PAID` · `REVOKING` · `PREPAID_CARD_ITEM_SUBSTITUTING` · 카드 이벤트 `REFUND` · `amount.type BALANCE` 등)은 SPEC-000 enum 에 더하고, 표본 없는 값(`PAYMENT_CANCEL` · `EXPIRATION` · `SUBTRACT` …)은 OQ. `external_ref.entity_type` 새 값 목록도.
6. `product_option` 옵션 단위 칸 = **뺀다**(메뉴 응답에 없음) — 단위는 `treatment_item.unit` 참조 · 구매 항목은 스냅샷. SPEC-000 1차 8 문구 같이.
7. 응답에 없는 칸(`product_option_composition.ref_single_option_id` 류 · `treatment_item` 가격 · 시간 · 권장 간격) — 구성의 「참조 단품 옵션」 칸은 **뺀다**(구성 = 시술 항목 참조 + 스냅샷). `treatment_item` 가격 · 시간 · 간격은 **칸 유지 + 「KOS 원천 없음 — DAY 원장 뒤 입력」** 표시.
8. 백필 = **전체 기간 · 지운 구매 포함(`deleted_at`) · 시술권 · 카드는 고객 통계로 보유 고객만**. 이벤트 없는 카드 찾기는 OQ.
9. 통계 API = id 나열에만 허용 · 원장 칸 원천으로 쓰지 않는다.
10. 테스트 계정의 두 번째 테넌트 = **실 명동점** — 개발 · 조사 · e2e 는 **`hospitalName` 이 DEMO 인 테넌트만**(스펙 「환경」에 한 줄).

## 4. 백필이 지금 시술현황에 주는 영향 — 코디가 prod 코드로 확인한 것 (스펙에 「백필 안전 규칙」 절로)

- 판(`load_world`)은 **오늘 `reserved_start_at` 창만** 읽는다 → 지난 방문은 판에 안 뜬다.
- 10초 동기화의 사라짐 처리는 **오늘 창 안 방문만**(`mark_absent(within=in_window)`) · 작업은 이번 응답 방문의 작업만 → 백필한 지난 행을 지우지 않는다. 백필도 같은 함수를 쓰면 **자기 창 안에서만** 지운다.
- `emr/` 동기화는 알림을 보내지 않는다(알림은 `tasks/notifications.py`) → 지난 작업을 넣어도 푸시가 안 나간다.
- `lock_visits` 는 방문별 advisory lock — 지난 방문만 잡으므로 오늘 판과 안 겹친다.
- 위험과 규칙(스펙에 박을 것):
  ① **백필 창은 어제까지** — 오늘은 10초 루프 몫(겹치면 같은 방문을 두 곳에서 쓴다).
  ② **KOS 세션** — 백필을 별도 프로세스로 돌리면 같은 시스템 계정 · 같은 UA 표시라 S-8 자동 해제가 **돌고 있는 worker 의 세션을 끊을 수 있다** → 백필은 worker 안에서 같은 토큰으로 돌리거나 다른 표시를 쓴다(어느 쪽인지 정할 것 · 추천 = worker 안 · 같은 토큰).
  ③ `visit_flow_log` — 백필은 지난 방문의 **마지막 단계 1줄**만 남긴다(전체 단계 이력은 KOS 가 안 준다) — 이력 화면이 생기면 그 차이를 안다.
  ④ `visit` 에 `(hospital_id, reserved_start_at)` 인덱스가 **없다**(prod 모델 확인) — 백필로 행이 늘기 전에 마이그레이션으로 더한다.
  ⑤ 호출 간격 · 한 회차 상한(KOS 부하) · 실패 시 이어 하기(어디까지 했나 기록).

## 5. allowed_paths

- `products/day/`

## 6. 구현 단계

1. **SPEC-002 개정** — 「KOS 읽기 — 동기화 추가분」 근처에 새 절(번호는 이 SPEC 관례): 루프별 호출 표(10초 · 5분 · 1시간 · 백필) · 테이블별 원천 경로(리포트 Q1) · 「바뀐 것만」 판단 규칙 · upsert / 사라짐 / `deleted` 규칙 · 매핑 표(KOS 값 → DAY enum · `external_ref.entity_type`) · 백필 절차(방문 월 단위 → 구매 묶음 → 시술권 고객별 → 카드) · 「백필 안전 규칙」(§4) · 환경(DEMO 만). 개정 기록 · `last_updated`.
2. **SPEC-000** — 결정 6 · 7 칸 수정 · 결정 5 의 enum 추가 · §6 OQ 정리(닫힌 것 표시 · 새 OQ). 칸 · 타입을 바꾸는 곳은 「2026-11-19 개정」 표시.
3. 필요하면 `40-architecture/erd.md` · `system.md` 를 맞춘다(칸이 빠진 것 · 동기화 주기 문장).
4. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/spec-sync-report.md` — 바꾼 곳 · 결정 → 줄 대응표 · lint.

## 7. 범위 제약

- 리포트 · 위 결정에 없는 정책 금지 → OQ. WORK · 코드 · SPEC-001/003~005 금지(영향은 리포트에만).
- HAR · 실호출 값(이름 · id · 테넌트)을 옮기지 마라. version 은 올리지 않는다(규칙).
- 커밋 · push · PR 금지.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- 결정 1~10 · §4 규칙 ①~⑤ 가 스펙 어느 줄에 있는지 대응표.
- 개인정보 grep 0(`[0-9a-f]{24}` · 전화 꼴).

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
