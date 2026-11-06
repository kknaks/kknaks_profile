# 리뷰 리포트 — agency-settlement / code r5 — SPEC-001 0.6.1 ↔ back/ · front/ (WP-BE6 · WP-FE7) (2026-11-03)

워크트리 `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement` · 기준 커밋 `8089f72` + 커밋 전 변경(BE6 · FE7) · read-only. 운영 PG 5434 · 8800 · 3800 · `back/.env` · 운영 KOS 는 건드리지 않았다. 시험은 testcontainers 로만 돌렸다(conftest `TEST_DATABASE_URL` 없음 → testcontainers · `_env_file=None` 확인). 재현 시험은 scratchpad `r5a/` 에만 두었다(레포 밖).

## 판정: FAIL

FAIL 1 · WARN 5 · NOTE 15.

**r4 F-1 은 다시 열리지 않았다.** 고정된 달에서는 상품 받기 · 다른 달 받기 · backfill · [전체 다시 받기] 어느 쪽으로도 키 · 수수료가 바뀌지 않는다. 재현 시험으로 확인했다.

막는 것은 하나다(**F-1**). **열린 달**에서 [전체 다시 받기]를 하거나 증분이 품목을 갈아 끼우면, 사람이 붙인 **수동 연결이 자동 연결에 진다.** 다시 저장할 때 ② 자동을 ⓪ 수동보다 먼저 돌리기 때문이다. §4.11 · §5.5 ⓪ · D-27 의 「이미 `manual` 인 품목은 [전체 다시 받기]가 바꾸지 않음」과 다르다. 이때 비율도 옮겨지지 않고 기록도 남지 않는다. 돈이 바뀌는 것은 드문 꼴(사람이 고른 상품 ≠ 나중에 KOS 가 그 옵션을 붙인 상품)뿐이지만 계약이 다르다.

**검증 수치**
- back `uv run pytest -q` = **296 passed**(1 warning — testcontainers 사용 중단 예고) · 35.0초 · `uv run ruff check .` = All checks passed
- 부분 시험(test_snapshot · links · fees · catalog · product_id · migration_0005) = 79 passed
- 재현 시험 4 = 3 통과(고정 달 키 · 수수료 그대로 · r4 W-2 닫힘 등) · **1 실패 = F-1**
- front `npx tsc --noEmit` 0 · `npm run lint` 0 · `npm run build` 는 돌리지 않음(워크트리 `.next` 를 씀)
- 잠금 잔재 grep
  - back(`locked_at|lockedAt|canLock|month_locked|cannot_lock|confirm_required|/lock|unlock`): `back/app` 에서 읽는 곳 0. 걸리는 것은 `pg_advisory_unlock` · `FROZEN_PURCHASE`(새 정의) · 읽지 않는 칸 · 「없음」을 보는 시험뿐
  - front(`이 달 확정|고치기|lockedAt|canLock|locked|fee-rates/lock|unlock`): **0**
- 코디 실물과 코드가 맞다
  - 0005 씨앗 「이번 달 열림 1 · 지난 달 고정 2」 = `0005_catalog_months.py:117-137`(이번 달 열림 · 저장된 지난 달 `frozen_by=migration`)
  - 옮기기 전과 같은 실결제 = 씨앗이 `items` · `fee_*` · `months` 를 안 건드림(test_116 덤프 비교 · test_118)
  - 스케줄 꺼짐 = `config.py:25` 기본 `False`

| # | 볼 것 | 결과 |
|---|---|---|
| ① | 상품 일별 스냅샷 · 고정 뒤 키 · 수수료 | 더하기만 · 「삭제됨」 · KOS 실패 때 쓰기 0 · 품목 달 스냅샷으로 잇기 · 다시 잇기 = 열린 달 못 이은 줄만 · 마지막 더하기 = 옵션 id 만 · 고정 달 `purchase_options` 그대로 — **r4 F-1 · W-1 닫힘**. 열린 달 수동 연결이 다시 받기에 짐 = **F-1** |
| ② | 21시 스케줄 · `run_daily` | 차례 · 달 1일 · 따라잡기 · 겹침(`pg_try_advisory_lock` · 풀 밖 연결 · 프로세스 둘도) · 뜰 때 안 돎 · `--due` 가드 · J4/J6 KOS 0 은 같음. 예외 하나에 루프가 소리 없이 죽음 **W-2** · 닫힐 때 돌던 단계를 끊음 **W-3** |
| ③ | 수동 연결 | 못 이은 품목에만 · 그 달 스냅샷 상품만 · 기록 INSERT 만 · 풀기는 맞음. 자동으로만 이어진 키도 저장됨 **W-1** · 다시 받기 **F-1** · 확인 창 문구 **W-4** |
| ④ | 지난 달 설정 열기 PUT 0 | 자동 `PUT rates: []` = 이번 달만 · 지난 달은 미리 보기 + [저장] 확인 창. 월별 화면 안내가 옛 규칙 **W-5** · 저장 본문 NOTE 9 |
| ⑤ | b-11 ~ 18 · b-22 | 전부 반영. b-22 새는 길 0(고른 줄 = 보이는 줄 ∩ 고른 줄 · 거르기 · 달 바꾸면 풀림 · 다 고르기 = 보이는 줄만). 0원 줄 보통 글자색 |
| ⑥ | schemas ↔ types | 없어진 필드 · 새 필드 · `KeyBy`(`product_title` · `manual` — **r4 W-4 닫힘**) 같음. 상품 연결 null 두 칸 NOTE 13 |

---

## FAIL

### F-1 열린 달 [전체 다시 받기] · 증분 품목 갈아 끼우기가 수동 연결을 자동 연결로 덮는다 — 비율 옮김 · 기록 0

- **코드**
  - `back/app/repository/store.py:588-605` `write_full` 은 이 달 `items_here` 수납마다 `_replace_items`(`:530-545` — `DELETE FROM items` 뒤 `product_id = NULL` 로 넣음)를 한 뒤 `link_items` 를 부른다
  - `back/app/repository/links.py:35-72` `link_items`
    - `:39-41` ② 옵션 id → `:42-62` ② `product_title` 를 먼저 돌린다
    - 그 뒤 `:63-72` ⓪ 수동은 `product_id IS NULL` 로 **아직 못 이은 줄**에만 붙는다
  - `store.py:624-632` 증분 (ii) 갈아 끼우기도 같다
  - 이 두 길에는 `diff_keys` · 비율 옮기기 · 연결 기록이 없다
- **SPEC · DEC**
  - §4.11 「이미 `manual` 이 된 품목 = 수동 그대로(상품 받기 · 다시 잇기 · **[전체 다시 받기] 가 바꾸지 않음** — 스냅샷에 옵션이 나중에 생겨도)」
  - §5.5 ⓪ 「한 번 manual 이 된 품목은 … 그대로」
  - D-27 · r8-decisions F-1(「자동으로 이은 다른 달 품목은 … 나중 [전체 다시 받기] 때도 안 바뀜」 — 그 반대쪽 불변식이 이것)
- **실패 길**(가짜 값 · scratchpad 재현 시험 실패로 확인)
  1. 11월(열린 달) 품목 B1 = `option:o7`(스냅샷에 o7 없음) · 설정 「연결 안 된 품목」에서 P2 로 수동 연결 → `product:P2` · `by=manual` · P2 비율 10% 가 붙음
  2. 21시 상품 받기가 11월 스냅샷에 o7 → P3 을 더함 → 수동 줄은 그대로(맞음 · `product_id IS NULL` 아님)
  3. 11월 [전체 다시 받기](또는 그 수납에 새 결제가 와서 증분이 품목을 갈아 끼움) → B1 이 `product:P3` · `by=product` 로 바뀐다 · `keysBy.manual` 0
  4. P3 비율이 없으면 「미설정 · 수수료 0」, 있으면 P3 비율. 옮김 · 기록 · 경고 0. 설정의 「수동 연결」 목록(`product_links`)엔 그대로 남아 있어 「연결했는데 왜 바뀌었나」
- **범위**
  - 고정 달은 해당 없다: 스냅샷이 늘지 않아 ② 가 다시 못 잇고 ⓪ 가 다시 붙는다(재현 시험 2 통과)
  - P3 = P2(사람이 KOS 가 나중에 붙일 상품을 맞게 고름)면 돈은 같다
  - 21시 스케줄 ③ 이 이번 달 증분을 매일 돌리므로, 새 결제가 붙은 수납에서 저절로 생길 수 있다(사람 손 없이)
- **고칠 것**(BE)
  - (권장) 저장 길의 `link_items` 를 이렇게 바꾼다: 갈아 끼우기 **전** 그 수납의 `by=manual` 줄을 기억해 두거나, alt key 가 `product_links` 에 있고 전에 manual 이던 품목은 ⓪ 를 ② 보다 먼저 적용한다
    - 「자동으로 못 이은 품목에만」(D-27)은 **처음 연결할 때**의 범위다. 이미 manual 이 된 품목은 그대로 두는 것이 §4.11 이다
  - 시험: 위 재현(열린 달 수동 → 스냅샷에 옵션 생김 → `refresh=full` · 증분 (ii) → `by=manual` · 수수료 그대로)

---

## WARN

### W-1 상품 연결 `PUT` 이 「자동으로 이미 이어진 키」도 받아 잠든 연결을 저장한다

- **코드**
  - `back/app/repository/settings_store.py:265-272` 이 키 검사를 「그 alt key 를 가진 상품 품목이 있음」으로 한다(자동으로 이은 품목 포함)
  - `:276-299` 은 바꿀 품목(못 이음 · manual)이 0 이어도 `product_links` 를 넣고 `link` 기록(`items=0`)을 남긴다
- **SPEC**: §4.11 연결 대상 = 「상품 id 로 못 이은 키만」 · 검사 「저장된 품목에 그 키가 있음」 · D-27
- **실패 길**(재현)
  - `option:o1`(11월 자동 → `product:P1`)에 `PUT {key:"option:o1", productId:"P2"}` → 200 · `product_links` 에 `('option:o1','P2')` · 기록 1
  - 뒤에 o1 이 스냅샷에 없는 달의 품목이 이 키로 오면 아무도 모르게 P2 · `by=manual` 로 붙는다
  - 화면(LinksView)은 못 이은 키만 보여 손으로는 드물다. API · 옛 화면 탭 · 재시도로 생길 수 있다
- **고칠 것**: 못 이은 품목 · manual 품목이 하나 이상 있을 때만 받고, 아니면 400 `bad_link` · 시험 1

### W-2 스케줄 루프가 `DomainError` 밖 예외 하나에 소리 없이 끝난다 — health 는 계속 「켜짐 · 다음 실행」

- **코드**
  - `back/app/service/schedule.py:88-91` `loop()` 는 `DomainError` 만 잡는다
  - `_steps` 의 단계마다도 `DomainError` 만 잡는다(`:128,141,154,161`)
  - `KeyError` · 검증 오류 · 감싸지 않은 `httpx` 예외는 `run_once`(`:101-104`)를 빠져나간다 → `schedule_finish` 없음(`schedule_runs.status NULL`) → 작업 끝
  - `main.py:109-111` 은 닫힐 때 `CancelledError` 만 눌러 그 예외가 종료 때 터진다
  - `schedule.py:76` 은 그 뒤에도 `enabled=true` · `nextDueAt` 을 낸다
- **SPEC**: §4.12 「한 단계 실패가 다음 단계 · 다음 21:00 을 막지 않는다 · 실패는 기록」
- **실패 길**: KOS 가 낯선 응답을 한 번 주면 그날부터 21시 실행 0, 달 1일 앞 달 마감 · 고정도 안 됨. 사람은 health 를 보고 돌고 있다고 믿는다(배포 · 스케줄 켬 때의 자리 · 지금 로컬은 꺼짐)
- **고칠 것**: `loop()` 에서 `Exception` 을 잡아 클래스 이름만 로그 · 단계의 비도메인 예외는 `failed`(코드 `internal`)로 기록하고 다음 단계로 · 시험 1(가짜 KOS 가 `KeyError` → 다음 실행 돎)

### W-3 닫힐 때 돌던 단계를 끊는다 — 실행 기록이 영원히 「끝나지 않음」

- **코드**
  - `back/app/main.py:108-111` 은 `task.cancel()` 로 돌던 `sales.get` · `catalog.refresh` 를 `await` 자리에서 끊는다
  - `asyncio.to_thread` 안 일은 계속 돌다가 `store.close()`(`:114`) 뒤 닫힌 풀에 닿을 수 있다
  - `schedule_runs` 행은 `status NULL` 로 남는다(`schemas/sales.py:193` 주석이 인정)
- **SPEC**: §4.12 「닫힐 때 … 돌던 단계는 끝까지 · 새 단계는 시작 안 함」
- **돈**: KOS 받기는 한 트랜잭션이라 쓰다 만 것이 없다 → 돈 0. 기록 · health `lastRun` 만 틀린다
- **고칠 것**: 멈춤 깃발(단계 사이에서 봄) → 정해진 시간까지 기다린 뒤 store 닫기

### W-4 상품 연결 확인 창이 D-27 과 반대로 말한다 — 「다른 달 품목도 바뀔 수 있어요」가 늘 나온다

- **코드**: `front/components/settings/LinksView.tsx:270-276` 은 늘 「같은 키의 다른 달 품목도 이 상품으로 이어지고, 수수료율이 그 상품 비율로 바뀔 수 있어요」를 보인다. 「같이 바뀌는 다른 달: …」은 `otherMonths` 가 있을 때만 따로 붙는다
- **SPEC**: §3.0.5(0.6.1) 「같은 키로 **아직 못 이은** <otherMonths> 품목도 … 이어지고」 · 「0 개면 그 구절 뺌 · 자동으로 이은 품목은 안 바뀜」 · D-27 · doc r8 F-1
- **실패 길**: 11월 `option:o7` 연결 · 10월 같은 옵션은 자동으로 이어져 `otherMonths=[]` → 창은 「다른 달도 바뀜」이라 말한다. 사람은 취소하거나, 10월이 바뀌었다고 믿는다. [바꾸기]도 같은 글
- **고칠 것**: 글 한 줄(`otherMonths` 를 넣고 0 개면 구절 뺌)

### W-5 월별 화면 안내가 옛 규칙 — 「설정에서 이 달을 열면 앞 달 값으로 시작해요」

- **코드**: `front/components/monthly/SummaryLine.tsx:67`(`fees.exists = false` 일 때)
- **SPEC**: §3.0.5 · §4.8 · §6.10(0.6.1 · doc r8 W-2) — 열기만으로 스냅샷을 만드는 것은 이번 달뿐 · 지난 달은 미리 보기 → [저장] 확인 창 때 만듦
- **실패 길**: 10월(스냅샷 없음) 월별 화면 안내대로 설정에서 10월을 연다 → 아무것도 안 만들어짐 → 월별로 돌아와도 여전히 전부 미설정 · 수수료 0. 지난 달이면 「설정에서 [저장]을 누르면」으로
- **고칠 것**: 이번 달 / 지난 달로 글 가름

---

## NOTE

1. **(F-1 이웃) 스냅샷 없는 달을 다시 받으면 `product:` 키가 대체 키로 내려간다.** `write_full` 이 품목을 다시 저장하는데 그 달 스냅샷이 없으면 ② 가 못 잇는다. §5.5 ② 「새로 저장하는 품목이면 대체 키」가 글자로는 허락한다. 씨앗이 없는 저장 달(0005 때 상품 목록이 비었음)에서만 생기는 꼴이다 — 9 · 10월은 씨앗으로 고정돼 해당 없음. OQ 한 줄 권장
2. **고정 달 다시 받기는 키를 고정 씨앗에서 다시 만든다.** 0.5.x 규칙(「옵션이 목록에서 빠진 행은 상품 id 를 그대로 둠」)으로 이어졌던 줄이 9 · 10월 [전체 다시 받기]에서 `option:` 으로 돌아갈 수 있다. 9 · 10월 = 테스트 데이터(운영 기준 11월부터 · D-28 꼴)라 낮음. 재현은 키 · 수수료 그대로였다
3. **수수료율 PUT 의 줄 검사가 쓰기 트랜잭션 밖**(`fees.py:253-258` 읽기 → `put_rates` 따로). 줄은 늘기만 해서 사실상 무해
4. **KOS ⑦ 가 상품 0 개면** 마지막 목록이 비고(`settings_store.py:42-60`) 이번 달 스냅샷 머리가 `exists=true` · 상품 0 으로 생긴다(`links.py:137-140`). 「삭제됨」 표시는 0 개일 때 안 함(맞음). 달 마지막 더하기가 빈 목록에서 더할 것이 없다는 것만 응답 수(`products=0`)로 보인다
5. **스케줄 시작 행 실패 때 잠금 연결**: `schedule.py:94-95` — 잠금을 잡은 뒤 `schedule_start` 가 try 밖. 그 INSERT 가 실패하면 잠금 연결을 명시적으로 풀지 않는다(GC 로 닫힘). try 안으로
6. **늦게 깬 실행이 옛 `due` 로 돈다**(`schedule.py:84-89`): 10-31 21:00 몫이 11-01 22:00 에 돌면 10월 매출은 닫히나 10월 상품 스냅샷 고정은 다음 날 `catch_up`. 무해 · 「놓친 실행 = 기록 없음」과 기록 꼴이 다르다(배포 때)
7. **`0005` 내리기**: `0005:164-166` 옛 CHECK 를 다시 걸 때 `manual` 행이 있으면 실패. 시험 DB 전용이지만 먼저 NULL 로 하거나 `NOT VALID`
8. **달 1일 21:00 전에 `0005` 를 올리면** 씨앗이 앞 달을 바로 고정한다(`0005:124-128` · 매출은 아직 `current` 일 수 있음). SPEC 대로(씨앗 = 저장된 지난 달 전부) · LIVE5 순서에 적어 둘 것
9. **지난 달 「이 값으로 저장」 본문 = 바꾼 키만**(`SettingsScreen.tsx:150-154` · 안 바꿨으면 `rates: []`) ↔ §3.0.5 「그때 `rates` = 보이는 값 전부」. 미리 보기 GET 과 PUT 사이에 복사 원천(앞 달)이 바뀌면, 사람이 확인한 값과 저장된 값이 다를 수 있다
10. **「미설정만」에서 율을 치면 첫 글자에 줄이 사라진다**(`SettingsScreen.tsx:197` — 거르기가 입력 중 값으로 봄). b-22 새는 길은 아님(`selRows = shown ∩ sel` · `:201`)
11. **PDF · 미리보기의 0원 미설정 줄 주황 「미설정」**(r4 NOTE 6 그대로 · `statements.py:299-300` · `StatementPreview.tsx:46`). 0원 금액 · 수수료 글자는 보통 색(W-3 반영) · 주석 ② · `unsetItems` 는 0원을 빼므로 짝 없는 주황
12. **설정 브라우저 뒤로가기**(popstate) 미확인(r4 NOTE 9 그대로) · **배지** — id 끝 4자리 = 같은 이름일 때만 · `by=product` · `inCatalog=false` 줄 배지 없음(r4 NOTE 10 그대로)
13. **상품 연결 타입 null**: back `LinkedKeyOut.productTitle` · `CandidateOut.title` = `str | None`(`schemas/settings.py`) ↔ front `string`(`types.ts` `LinkedRow` · `LinkCandidate`) — null 이면 「→ 」 빈 글. `LinkedKeyOut.otherMonths` 는 front 타입에 없음(런타임에 씀). `ProductsRefreshResponse` 새 필드는 front 선택(`?`)
14. **월별 `closed` 칩 「✓ 확정 · 저장됨」**(`SalesScreen.tsx:261`) — 3판 매출 상태 칩(§3.1 그대로)이나, 수수료 「확정」이 없어진 판이라 수수료가 잠긴 것으로 읽힐 수 있다
15. **J4/J6 문**은 env 깃발(`sales.py:405`)을 본다(`scheduler.enabled` 는 KOS 설정까지 봄). 깃발 켬 + KOS 빔이면 저장본만 → 어느 쪽이든 KOS 0 · 일관

---

## 확인함 (같음)

- **① 스냅샷 · 고정**
  - 상품 받기
    - 마지막 목록 갈아 끼움 + 이번 달 스냅샷에 더하기만(있는 줄은 보이는 값 갱신 · `deleted_in_kos` 풀림 · id · 키 안 바뀜) · 사라진 것 = 「삭제됨」(목록이 0 개면 표시 안 함)
    - KOS 둘 다 받은 뒤에만 씀(`links.py:129-173` · `catalog.py:79-92`)
    - 고정 달 `snapshot_add` = None(`links.py:134-136`)
  - 다시 잇기 = `open_scope` · `product_id IS NULL` 만(`settings_store.py:69-71` · `links.py:24-41`)
  - 고정 달 키 원천
    - `replace_options_in` 이 품목 달이 고정된 수납을 건너뜀(`store.py:450-479` · `FROZEN_PURCHASE` = 품목 달 상품 스냅샷 `frozen_at` · `links.py:21-22` — **r4 W-1 닫힘**)
    - backfill 은 같은 seq · 같은 옵션 id 의 `option_type` · 구성만(`store.py:481-492`)
  - 재현 시험 2: 고정 10월 `option:o7` 이 상품 받기(같은 title 추가 · 같은 title 둘 · o7 목록 복귀) · 10월 `refresh=full` 뒤에도 키 · 수수료 그대로 — **r4 F-1 닫힘**
  - 달 마지막
    - 더하기(`mark_deleted=False`) → 옵션 id 로만 다시 잇기(`title=False` · W-5) → `frozen_at IS NULL` 일 때만 고정 · 한 쓰기 트랜잭션(`settings_store.py:79-94` · `links.py:176-179`)
    - 고정은 스케줄 · `run_daily` 만(`frozen_by` = `schedule` / `catch_up` / 씨앗 `migration`)
  - 비율 옮기기 = 그 품목 달 수수료 스냅샷만 · 새 키가 비었을 때만 · 아니면 `conflicts` · 옛 줄 남김 · `set` 기록(`links.py:99-116`)
- **② 스케줄 · `run_daily`**
  - 기본 꺼짐(`config.py:25` · `.env.example:19` 이름만)
  - 뜰 때 안 돎(`next_due` 까지 잠 · test_110)
  - KOS 설정 비면 안 켜짐 + 로그 한 줄(`main.py:103-104`)
  - 21:00 KST 상수 · 서버 시간대와 무관하게 `Asia/Seoul`(`schedule.py:28-42`)
  - 차례 ① 상품 → ② 지난 달(이른 달부터 · 열린 스냅샷 달 ∪ `current` 매출 달 · (a) `sales.get(m,"new")` = 같은 판단표 · 달 잠금 (b) `close_month`) → ③ 이번 달(`:131-157`)
  - ① 실패면 고정 0 · (a) 실패면 그 달 고정 0 · 단계마다 트랜잭션 · `ok`/`partial`/`failed` + 첫 오류 코드
  - 겹침 = `pg_try_advisory_lock(41003,0)` · 풀 밖 연결(프로세스 둘도 · 풀 안 잡음 · `store.py:200-223`) → `skipped` 기록 · test_108(사람 받기와 겹쳐도 한 번)
  - `schedule_runs.steps` = 달 · 상태 · 수만
  - `run_daily --due`: 꼴 틀림 · 21:00 아님 · 지금보다 뒤 = 거절(exit 2 · 행 0 · `run_daily.py:21-32` · test_111) · 같은 `run_once` · 같은 잠금
  - 켜지면 `refresh` 없는 J4/J6 요청 KOS 0(`sales.py:400-409` · test_110)
  - health `schedule{enabled, nextDueAt, lastRun{dueAt,status,finishedAt}}`
- **③ 수동 연결**
  - 키 꼴 = `option:` · `name:PRODUCT_OPTION:` 만(`product_key.py:92` + DB CHECK `0005:76`) · `productId` = 그 달 `catalog_month_products` 에 있음(`settings_store.py:262-264`)
  - 같은 연결 다시 = 기록 0 · 바꾸는 품목 = 못 이음 · manual 만(D-27) · `result.months` = 바뀐 품목의 품목 달
  - 풀기 = 열린 달은 자동으로 · 고정 달은 대체 키로(#115)
  - 기록 표 앱 계정 SELECT/INSERT 만(`0005:146-153`)
  - 쓰기 막기(Host · Origin · JSON 415)가 `PUT /api/product-links` 에도(`main.py:72-82` · `test_write_guard.py:12-13`)
- **④ 수수료율**
  - 어느 달이든 PUT(잠금 검사 0) · `_ensure` 복사 = 쓰기 잠금 안(`settings_store.py:166-178`)
  - **r4 W-2 닫힘**: 3판 `{kind,name}` 400 · `rows` 밖 키 400(`fees.py:60-73,253-256` · 재현 4)
  - 식 = 정수 반올림 그대로(`fees.py:51-56`)
  - front: 자동 `PUT rates: []` = `!exists && !past` 만(`SettingsScreen.tsx:83-84`) · 지난 달 = 미리 보기 띠 + 「M월 수수료율을 바꿀까요? … 바꾼 기록은 남아요」 [아니요] [바꿀게요](`:528-543`)
- **잠금 지움**
  - `/api/fee-rates/lock` · `/unlock` 404(`test_privacy_app.py:76-85`) · `month_locked` · `cannot_lock` · `confirm_required` · `canLock` · `lockedAt` 0 · 경로 10
  - [전체 다시 받기] 늘 켜짐 + `closed` 달 확인 창 「이미 내려받은 거래 명세서와 금액이 달라질 수 있어요」
  - zip 확인 창 「확정 전」 줄 지움 · PDF 주석 ① 「(저장 MM-DD HH:mm)」(미리보기 `StatementPreview.tsx:56` · back `statements.py:316-317`)
- **0005**
  - 더하기만(새 표 7 · 새 칸 · CHECK 바꾸기 = `0002` 의 기본 이름 `items_product_via_check` 그대로 · 값 변경 0)
  - 권한 = 기록 표 SELECT/INSERT · `schedule_runs` SELECT/INSERT/UPDATE · 나머지 다섯 SELECT/INSERT/UPDATE/DELETE · 시퀀스 USAGE
  - 왕복 · 권한(test_117)
  - `0001` ~ `0004` diff = `upgrade/downgrade(**_kw)` 서명뿐 · DDL 0 → 이미 올린 DB 에 영향 0
  - 새 오류 `store_busy` 503(`store.py:126-129`) · `bad_link` 400
- **⑤ 화면**
  - b-11 설정 상단 안내 지움
  - b-12 일괄 대상 글 = 「전체 n개」 · 「<카테고리> · '<말>' · 미설정 n개」 · 「고른 상품 n개」(`SettingsScreen.tsx:205-206`)
  - b-13 율 입력 아래 안내 0(빨강 + `title`)
  - b-15 건수 줄 회색 글 지움 · b-16 결산 표 위 회색 글 지움(`SalesScreen.tsx:196`)
  - b-17 월별 기본 펼침 · 채널 탭 기본 접힘 · 탭 · 달마다 다시(`SalesScreen.tsx:115-127`)
  - b-18 머리 · 줄 같은 `GRID_COLS` · 종류 · 상품 · 옵션 왼쪽 · 옵션 넓게 · 폰 카드 같은 차례(`format.ts:8-15` · `PurchaseGroup.tsx:209-245,289-292`)
  - b-22
    - 칩 · 찾기 · 미설정만 바꾸면 고른 것 풀림(`:186-197`) · 달 · 보기 바꾸면 다시 그림(키 `${month}#${view}`)
    - `selRows = shown ∩ sel` · 다 고르기 = 보이는 줄만 · [적용] 뒤 풀림 · 고른 것 없이 [적용] = 「<대상>에 적용할까요?」
    - 안 보이는 줄에 적용되는 길 0
  - 0원 줄 보통 글자색(`PurchaseGroup.tsx:16-31`)
  - 배지 「KOS 삭제됨」 · 「연결 안 됨」(PRODUCT_OPTION · `option`/`name` · 누르면 `?view=links`) · 「수동 연결」
  - 보기 「수수료율 | 연결 안 된 품목 n」(0 이면 흐림)
  - LinksView = 목록 · 키 종류 회색 글 · otherMonths 줄 · 후보(찾기 · 카테고리 · 「KOS 삭제됨」 · 「사용 중지」 · id 끝) · 확인 창 · 풀기 · note ≤ 200 · 결과 줄 · 스냅샷 없음 안내(받기 버튼은 이번 달만)
  - 설정 상품 받기 결과 한 줄(0 은 뺌)
- **⑥ 계약**
  - 없어진 `fees.locked/lockedAt` · `lockedAt` · `canLock`(양쪽)
  - 새 `fees.savedAt` · `catalog{month,exists,frozenAt,updatedAt,unlinkedKeys}` · `counts.unlinkedItems/manualLinkedItems` · `KeyBy` = `product · product_title · option · name · manual`(`types.ts:105` ↔ `schemas/sales.py:89`)
  - `/fee-rates` `catalog.{rekeyedItems,carriedRates,conflicts,addedProducts,addedOptions,markedDeleted,snapshot}` · `unlinkedKeys` · `rows[].deletedInKos/inCatalog`
  - `/product-links` GET/PUT 본문 · `result{items,months,carriedRates,conflicts}` · `api.ts` 경로 · JSON · `{key,productId,note}` · 오류 `{error:{code,message}}` · `bad_link` · `store_busy` 토스트
  - NOTE 13 빼고 같음

## 고객이 실물에서 만날 자리

- **(F-1)** 11월 「연결 안 된 품목」을 손으로 이어 비율을 넣었는데, 며칠 뒤(상품 받기 · 그 수납에 새 결제 · [전체 다시 받기]) 그 품목이 다른 상품으로 바뀌어 「미설정」이나 다른 비율이 됨 — 설정 「수동 연결」 목록엔 그대로 남아 있음
- **(W-4)** 연결 확인 창이 「다른 달 품목도 바뀔 수 있어요」라고 겁줌 — 실제로는 바뀌는 달 0
- **(W-5)** 10월 화면 안내대로 설정에서 10월을 열었는데 수수료가 여전히 0 — 지난 달은 [저장]을 눌러야 시작됨
- **(W-1)** 이미 이어진 키를 API · 옛 탭으로 연결하면 200 · 기록만 남고, 나중 달 품목이 엉뚱한 상품으로 붙을 수 있음
- **(W-2 · W-3)** 스케줄을 켠 뒤(배포 때) 한 번의 이상한 KOS 응답 뒤로 21시 실행이 멈췄는데 health 는 「다음 실행 21:00」 · 껐다 켜면 마지막 실행 기록이 「끝나지 않음」
- (NOTE 10) 「미설정만」으로 걸러 율을 치면 첫 글자에 줄이 사라짐
- (NOTE 11) 명세서 0원 줄의 주황 「미설정」 · (NOTE 12) 설정 뒤로가기에 저장 안 한 값이 사라짐

## 참고(기존 부채)

- r4 F-1(상품 받기 → 잠긴 달 수수료) · W-1(다른 달 받기가 키 원천을 바꿈) · W-2(PUT 키 검사) · W-4(`KeyBy`) **닫힘**. r4 W-3(풀 60초)은 `store_busy` 503 으로 바뀜(0.5.3)
- r4 NOTE 6 · 9 · 10 은 그대로(위 NOTE 11 · 12)
- OQ-132 · OQ-153 · OQ-154(서비스 표시 — 병원 담당자) 열림 · 스케줄 켜기 · 서버 · 로그인은 배포 때(§1.2)
