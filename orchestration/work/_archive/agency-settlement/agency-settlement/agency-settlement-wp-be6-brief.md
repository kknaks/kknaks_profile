# [backend] WP-BE6 — SPEC-001 0.6.0 (+ doc r8 코디 결정)

너는 **agency-settlement `backend` 워커**다(앞 판을 만든 워커면 그 맥락을 써라). 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/backend/role.md`.
⚠ 같은 워크트리 `front/` 병렬 작업 중 — 건드리지 마라. ⚠ 8800 · 3800 · `back/.env` · **운영 PG(5434)** 건드리지 마라 · 운영 KOS 호출 금지(가짜 · dev PG 5433 · testcontainers).
작업 워크트리 `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement`

## SSOT
- SPEC-001 **0.6.0** · WORK-001 5판 **WP-BE6** 행 + 계약 고정점
- **doc r8 코디 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/r8-decisions.md`** — SPEC 과 다르면 이게 이긴다(planner 가 SPEC 을 병렬로 0.6.1 로 맞춤)
- DEC-001 D-24 ~ D-28 · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/_RESUME.md` §2 2026-11-03 줄 · 사용자 수정 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/feedback-2026-11-02-b.md` 7 ~ 22

## 할 것
WP-BE6 행 전부 + r8 결정 + 아래 지킬 것.

## 구현 때 지킬 것 (막지 않음 · BE6 · FE7 브리프로)

### 스냅샷 · 다시 잇기
1. 다시 잇기 SQL 범위 = **품목 달**(`month_purchases.items_here = true` 인 달)의 스냅샷이 **열려 있고** `product_via` 가 자동 못 이음(`option`/`name` 대체 키 · `product_id IS NULL`)인 줄만
   - 지금 `link_products`(`store.py:73`)의 「`product_title` 줄을 늘 NULL 로 지우고 다시 맞춤」 · 「`option` 줄을 늘 다시 씀」(`:74`)은 **없앤다**(이미 이은 줄 안 바꿈)
   - 품목 달이 없는 품목은 건드리지 않는다
   - 품목 달이 [전체 다시 받기]로 옮겨 간 품목(§4.6 ②)도 이미 이은 키는 그대로다(새 달 스냅샷으로 다시 잇지 않음) — 시험 한 줄
2. `product_title` 짝의 「하나로 맞음」은 **그 달 스냅샷 안**(「KOS 삭제됨」 줄 포함)에서 센다. 이름 다듬기는 지금 `btrim(…, WS)` 그대로
3. 상품 받기 = ⑥ ⑦ 다 받은 뒤 한 쓰기 트랜잭션(목록 갈아 끼우기 · 이번 달 스냅샷 더하기 · 열린 달 다시 잇기 · 비율 옮기기 · `catalog_fetches`)
   - ⑦ 상품 0 개면 「삭제됨」 표시 0(OQ-158)
   - 「이번 달」 = 받기 시작 시각 KST
4. 달 1일 마지막 더하기는 ① 에서 받은 목록을 다시 쓴다(KOS 다시 0) · 「삭제됨」 표시 0 · ① 이 실패하면 고정 0
   - 고정은 같은 트랜잭션에서 `frozen_at IS NULL` 일 때만(두 번 고정 0 · `frozen_by` 하나)
5. `fee_rate_months.locked_at` · `FROZEN_PURCHASE` 옛 정의 · `NOT_FROZEN`(지금 `store.py:72`)은 WORK grep 으로 **쓰는 곳을 전부** 세고 새 정의(품목 달 상품 스냅샷 고정)로 바꾼다
   - `backfill_compositions` · `_replace_options` · `link_products` 세 곳이 같은 정의를 쓴다

### 스케줄
6. 다음 21:00 은 `zoneinfo("Asia/Seoul")` 로 셈한다. 시계 · 잠자기는 주입한다. **뜰 때 바로 돌지 않는다.** 닫힐 때는 작업을 취소하되, 돌던 단계의 트랜잭션은 끝나거나 되돌아간다
7. `schedule_runs` 는 시작 때 넣고 끝날 때 고친다
   - 프로세스가 죽어 `finished_at` · `status` 가 null 로 남은 줄은 「끝나지 않음」으로 읽는다(health `lastRun.status = null`). 다음 실행은 그 줄과 상관없이 돈다
   - `skipped` 줄도 남긴다(인스턴스 둘이면 매일 하나씩 — 정상)
8. 스케줄의 단계는 **HTTP 와 같은 서비스 함수**를 부른다(§4.5 판단표 · 달 잠금 · 쓰기 잠금 · 줄 선 요청). 스케줄 전용 받기 코드를 따로 두지 않는다
   - 풀 연결: 스케줄도 달 세션 연결을 하나 쥔다 → code r4 W-3(풀 60초) 꼴. 받기 동시 달 수 제한과 같이 본다
9. `run_daily --due` 가 **지금보다 뒤면 거절**(운영 11월을 미리 고정하는 길을 코드가 막음 — WORK 주의 · L37 를 사람에게만 맡기지 않음)
   - `--due` 의 21:00 이 아닌 시각도 거절
10. 스케줄 켜짐 + J4 · J6 값 없는 요청 = `none`. `refresh=new` · J2 는 그대로다. front 는 스케줄 상태를 모르니 화면 문구를 바꾸지 않는다(OQ-166)

### 수동 연결
11. PUT 은 쓰기 잠금 · 한 트랜잭션이다
    - ① `product_links`
    - ② 품목 키(F-1 에서 정한 범위 · `product_via = 'manual'`)
    - ③ 비율 옮기기(품목이 있는 달마다 · 새 키가 비었을 때만 · `fee_rate_changes` note)
    - ④ `product_link_changes`
    - 어느 하나라도 틀리면 0
12. 풀기(`null`): 열린 달 품목은 자동 규칙으로, 고정된 달 품목은 대체 키로 돌린다. 대체 키는 `items.option_id` · 이름으로 다시 만든다(따로 저장할 필요 없음 · 지금 칸으로 충분)
13. 대상 키 검사: `name:ETCETRA_PRODUCT:` · `name:PREPAID_CARD_PRODUCT:` · 키 없음 → 400 `bad_link`. `productId` 는 `month` 스냅샷에 있어야 한다(「삭제됨」 줄 됨)
14. `product_link_changes` · `schedule_runs` 권한: 앞쪽 = `SELECT` · `INSERT` 만 · 뒤쪽 = `+ UPDATE` · DELETE 0(#117 에 앱 계정으로 확인)

### 돈 · 셈
15. `counts.unlinkedItems`(줄 수 · `/api/sales`)와 설정 `unlinkedKeys`(키 수)는 **같은 판정 함수**로 센다(보이는 품목 줄 · `PRODUCT_OPTION` · 대체 키 · 연결 없음)
16. 0005 씨앗: 「저장된 지난 달」 = `months` 의 이번 달(KST · 올리는 시각) 앞 달 전부 · `first_seen_at` = `catalog_fetches` 마지막 · `items` · `fee_*` 값 바뀜 0(#116 덤프 비교)
    - 운영 PG 는 **백업 뒤**(L33) 올린다

### front
17. b-22: 카테고리 알약 · 찾기 · 「미설정만」 · 달 · 보기를 바꾸면 선택을 0 으로 비운다
    - [적용]의 대상은 그 순간 **보이는 줄 ∩ 고른 줄**로 한 번 더 거른다(state 가 남아도 안 보이는 줄에 안 감)
    - 지난 달 [저장] 확인 창 · [전체 다시 받기] 지난 달 문구 한 줄 · 확정 UI grep 0
18. 「연결 안 된 품목」 확인 창은 `otherMonths` 를 그대로 보인다(F-1 에서 정한 뜻). 결과 줄 「품목 n줄 연결 · 비율 옮김 c · 충돌 x」의 0 인 것은 뺀다

---

## 검증
```
cd back && uv run ruff check . && uv run pytest -q
```
보고에 완료 조건 · 지킬 것 한 줄씩. 마이그레이션 왕복 · 스케줄 시험(시계 가짜)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_2b0bc5fd-c40c-4f07-9364-469e17c51a65 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WP-BE6" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] backend: <질문>" --enter`
