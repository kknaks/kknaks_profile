# 리뷰 리포트 — customer-erd / code 5 (빈 본문 수정 · 검수 4 WARN 정리 · 개인정보) (2026-11-19)

> **백필 제외** — 코디 지시(사용자 「백필 내가 한다」): `runtime/backfill` · `PacedTransport` · `KosPacer` · 진행 위치 · `visit` 인덱스 · 백필 테스트는 이번 PR 에서 빠지므로 판정하지 않았다. 지시서 1 ~ 4 · 7 은 보지 않았다. 볼 것 = 지시서 5 · 6 · 8.

- 기준: `git diff origin/dev` + 미추적 · 워커 리포트 `be-3-report.md` 「0」 · 「실물에서 찾은 것」(diff 로 재확인)

## 판정: **PASS (FAIL 0 · WARN 1)**

| 볼 것 | 판정 |
|---|---|
| 5. 빈 본문 수정(2단계 오늘 회차에도 닿음) | **PASS**(WARN-1) |
| 6. WARN-A · B · D 닫힘 | **PASS** |
| 8. 개인정보 | **PASS** |
| 직원이 실물에서 만날 자리 | **없음** — 판 · 앱 변경 0. 오히려 빈 본문 수정으로 「받을 게 없는 고객이 오늘 바뀐 고객이 되면 시술권 · 카드 단계가 10초마다 실패」하던 길이 닫힌다(운영 이득 · PR 설명에 적을 것) |

## 5. 빈 본문 수정 — PASS (WARN-1)

- 위치: `backend/day/emr/kos/sale_reads.py:126-138` `_rows(..., empty_ok=False)` — `empty_ok` 이고 응답이 `{}` 일 때만 0 건. `{}` 는 기존 `KosClient._json`(`client.py:296-303` · 이번 diff 밖 · 그대로)이 **2xx 이고 본문 바이트가 없을 때** 만 돌려준다. 4xx · 5xx 는 그 전에 오류(`post_kos`) · JSON 인데 `data` 가 배열이 아니면 여전히 `EmrError`.
- 켠 곳은 둘뿐: `fetch_ticket_bundles`(`:260-269`) · `fetch_prepaid_cards`(`:277-284`). 둘 다 **사라짐을 판단하지 않는 읽기**다 —
  - 시술권: `apply_tickets` 는 응답에서 빠진 번들을 지우지 않는다(OQ-73 · `sync_tickets.py` 의 `soft_delete` 는 같은 구매 항목의 「옛 번들 → 새 번들」 교체 `_retire_other_bundles` 하나뿐 · 번들이 0 이면 호출 대상 0).
  - 카드: `apply_cards` 는 카드 행을 지우지도 되살리지도 않는다.
  → 빈 본문이 진짜 0 건이든 KOS 의 일시 이상이든 **소프트 딜리트는 생기지 않는다** ✓.
- 사라짐을 판단하는 읽기(구매 묶음 · 카드 이력 · 공유 고객 · 메뉴)는 `empty_ok` 없이 그대로 실패 — 테스트 `test_kos_sale_mapper.py:425` `test_시술권_카드_요약은_빈_본문을_0_건으로_본다` 가 카드 상세 · 구매는 `EmrError` 임을 같이 본다 ✓.
- **WARN-1 (부작용 하나)**: 빈 본문 고객의 오늘 작업 티켓은 「받아도 안 풀림」으로 검수 3 FAIL-1 의 집합(`day:emr:sale_unresolved_tickets:{병원}` · 오늘 끝까지)에 들어간다. 빈 본문이 KOS 의 **일시 이상**이었다면 그 고객의 시술권은 그날 다시 안 받는다 — 구매가 바뀌거나 작업 `ticketId` 가 바뀌면 다시 받으므로 놓치는 범위는 「구매 변경 없는 그날의 티켓 상태(`in_use` → `used`)」 정도. 데이터 손실 아님(다음 날 다시). 그대로 둬도 되는 수준 — 사용자 판단.

## 6. WARN-A · B · D — PASS

### WARN-A (죽은 코드) — 닫힘
- `sale_reads.py` 의 `stat_limit` · `stat_max_pages` · `_utc` · 「공개 통계」 주석, `kos/__init__.py` 「· 통계」, `sync_purchases.py` 「5분 회차」 주석 → grep 0. 남은 `emr_sale_sync.py:9` 는 「5분 회차를 뺐다」는 **현재 설명**이라 맞음.

### WARN-B (늦은 옛 메시지 · 메시지 읽기 격리) — 닫힘
- 메시지 = `{published_at, sales}`(`emr_sale_sync.py:126-130`) · 발행 시각 = 일정 회차 **뒤** `utc_now()`(`tasks/emr.py:80`).
- `run_sales`(`emr_sale_sync.py:357-367`) 가 **`sales` 잠금 안에서** 병원별 `day:emr:sales_published_at:{병원}` 과 비교해 `published_at <= last` 이면 `sales.stale_message` 로 세고 끝(KOS · DB 0). **성공한 회차만** 그 시각을 적는다(`:376-383` · 만료 7일).
- 정상 메시지를 버릴 위험: 버리는 것은 「이미 처리한 것보다 **먼저 발행된**」 메시지뿐이고, 그 내용은 더 새 메시지가 이미 반영했다 → 잃는 정보 없음. 실패한 회차는 시각을 안 적으므로 다음 메시지가 버려지지 않는다. 같은 마이크로초 두 메시지(`<=`)는 사실상 없음. 서버 시계가 뒤로 튀면 그만큼(초 단위) 버려질 수 있으나 10초 뒤 메시지가 다시 덮음. 새 태스크(`day.emr.sync_sales_hospital`)는 prod 에 아직 없어 옛 모양 메시지 호환 문제 없음 ✓.
- 메시지 읽기: `run_sales_message`(`:328-335`)로 옮겨 `_isolated` **안**(`tasks/emr.py:105`) ✓. 테스트 `test_sale_sync_runs.py:233` 옛 메시지 버림 · `:252` 깨진 메시지는 그 태스크만 실패 ✓.

### WARN-D (명시 삭제 시술 항목) — 닫힘
- `sale_reads.py:86-112` — 같은 id 는 `updatedDateTimeUtc` 가장 늦은 것 하나(`_all_services` → `_latest`) · 그게 `deleted:true` 면 `deleted_services`, 아니면 `menu_services`(한 id 가 양쪽에 동시에 들어가지 않음).
- `sync_menu.py:253 · 279-288` `_explicitly_deleted_items` — DAY 에 있는 그 항목만 기존 `mark_absent`(`deleted_at` + `is_present_in_source=false`). 옵션에서 **빠진** 것은 여전히 손대지 않음 · 살아 있다고 다시 오면 upsert(`deleted_at=None`) · `link` 로 되살림 ✓. 테스트 `test_sale_sync.py:276` `test_KOS_가_명시적으로_지운_시술_항목만_지움_표시` ✓.
- 기기 · 약물은 KOS 가 개별 `deleted` 를 주지 않아(구성 항목 목록) 지금처럼 지우지 않음 — 지시(진료항목만)와 같음.

## 8. 개인정보 — PASS

- 이번 범위의 로그: `sync_purchases.py:271`(DAY 구매 id · 건수) · `tasks/emr.py:56 · 83`(병원 DAY id · 예외 이름) — 이름 · 전화 · KOS id · 토큰 0.
- 메시지(`sales_payload`)는 외부 id · sequence · 기기 이름 스냅샷뿐(고객 이름 · 연락처 · 메모 없음) — Redis 브로커에 남는 값이라 확인 ✓.
- 고정본 · 새 테스트: 전화 패턴 · JWT(`eyJ…`) · `Bearer` 토큰 · 실 uuid 패턴 grep 0 · id 는 `vis-1` · `card-1` · `pur-1` 꼴.

## 직접 실행 (백필 테스트 제외)

| 명령 | 결과 |
|---|---|
| `cd backend && uv run pytest -q tests/day/emr/test_sale_sync_rules.py tests/day/emr/test_kos_sale_mapper.py tests/day/emr/test_kos_client.py tests/migrations/test_sale_tables_migration.py` | **68 passed** |
| `uv run pytest -q tests/day -k "sale or emr" --deselect tests/day/emr/test_backfill_rules.py` | **187 passed · 65 skipped**(infra) |
| `./scripts/test.sh -q backend/tests/day/emr/test_sale_sync.py backend/tests/day/emr/test_sale_sync_runs.py`(자체 격리 compose) | **18 passed** |
| `./scripts/test.sh -q`(전체 · 백필 테스트 포함한 현재 워크트리) | **1854 passed** |

- 참고: 백필을 PR 에서 뺄 때 같이 빠져야 할 것(이번 판정 밖 · 코디 확인용): `runtime/backfill.py` · `services/emr_backfill.py` · `emr/pacing.py` · `client.py` 의 `PacedTransport` · `revoke_own_sign_ins` · `factory.build_backfill_adapter` · `base.py` · `kos/__init__.py` · `sale_reads.py` 의 `fetch_customer_page` · `release_own_sessions` · `public.py` · `error_codes.BACKFILL_INPUT_ERROR` · `models/visit.py` + 0010 의 `visit` 인덱스 · `test_backfill*.py` · `test_sale_sync_rules.py` AST 대상 목록의 백필 2 파일 · `test_sale_tables_migration.py` 의 visit 인덱스 테스트. 빈 본문 수정(`_rows(empty_ok)`)은 **남겨야** 한다(오늘 회차 수정).

## FAIL 고칠 곳

**없음.**

## 사용자 판단

1. WARN-1 — 빈 본문 고객의 티켓을 「그날 다시 안 받음」 집합에 넣는 것을 그대로 둘지(지금: 구매 · 티켓 변경 때만 다시).
