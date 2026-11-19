# customer-erd backend 3단계 결과 보고 — 지난 이력 백필(수동 · KOS 1초 1회 · 내부 API 만)

> **백필은 PR 에서 뺌 — 참고 패치**(사용자 2026-11-19 「백필 내가 한다」). 백필 부분 전부(`runtime/backfill.py` · `services/emr_backfill.py` · `emr/pacing.py` · `client.py` 의 `PacedTransport` · `revoke_own_sign_ins` · `factory.build_backfill_adapter` · `fetch_customer_page` · `release_own_sessions` · `NormalizedCustomerPageData` · `public.py` 내보내기 · `BACKFILL_INPUT_ERROR` · `models/visit.py` + 0010 의 `visit(hospital_id, reserved_start_at)` 인덱스 · `test_backfill*.py` · 규칙 테스트 AST 대상 2 파일 · visit 인덱스 테스트)는 `orchestration/work/customer-erd/backfill-reference.patch`(17 파일 · +1448 / −5) 로 옮겼다. 백필을 뺀 워크트리에 `git apply` 로 그대로 얹힌다(확인함). 비밀값 · 이름 없음(테스트 자리값만). **PR 에 남은 것**: 검수 4 WARN-A · B · D + 빈 본문 수정(오늘 회차 시술권 · 카드 요약) + 그 테스트. 0010 은 다시 「지금 테이블에는 인덱스를 더하지 않는다」(테스트도 그렇게 바꿈). 뺀 뒤 각 1회: 전체 **1831 passed**(백필 테스트 23 빠짐) · `check.sh --pure` 구조 · ruff · format · mypy · Taut 통과(frontend 는 npm 미설치 · 앞과 같음) · migration upgrade → downgrade base → upgrade **24 passed** · `grep -rn backfill backend/` 0(한글 「백필」은 migration · 설정의 데이터 채움 뜻과, 「다음 날 다시 받기」 주석 둘만 남음). 아래 본문은 백필을 넣었을 때의 기록이다(참고 패치의 설명으로 읽는다).

## 상태: done (커밋 · push · PR 없음 — 워크트리 변경만)

- 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd` · base `origin/dev` `bbd9220a`(시작 때 fetch — 나아가지 않음)
- 실행: `python -m runtime.backfill --hospital <uuid> --from YYYY-MM [--to YYYY-MM-DD] [--stage schedules|purchases|tickets|cards|all] [--dry-run] [--resume]`

## 0. 검수 4 WARN 정리

| | 반영 | 파일 |
|---|---|---|
| WARN-A | 5분 회차 잔재 삭제 — `sale_reads` 의 `stat_limit` · `stat_max_pages` · `_utc` · 「공개 통계」 주석 · 「5분 회차」 주석(`sale_reads` · `kos/__init__` · `sync_purchases`) | `emr/kos/sale_reads.py` · `emr/kos/__init__.py` · `emr/sync_purchases.py` |
| WARN-B | 오늘 구매 메시지 = `{published_at, sales}`(`sales_message`). `run_sales` 가 `sales` 잠금 안에서 병원별 Redis `day:emr:sales_published_at:{병원}` 와 비교 — 같거나 오래된 메시지는 **세고 버린다**(`sales.stale_message` · KOS · DB 0). 성공하면 그 시각을 적는다. 메시지 읽기(`sales_from_payload`)는 `run_sales_message` 로 `_isolated` **안**에서 | `services/emr_sale_sync.py` · `tasks/emr.py` |
| WARN-C | 코드 변경 없음 — 아래 「prod 첫 기준 정보 때 확인」 | |
| WARN-D | KOS 가 **명시적으로 `deleted:true`** 를 준 시술 항목(옵션 · 구성 `medicalService` 중 id 마다 가장 늦게 고친 것)만 `deleted_at` + `is_present_in_source=false`(기존 `mark_absent` 그대로). 옵션에서 빠진 것은 그대로 · 다시 살아 있다고 오면 되살림 | `emr/kos/sale_reads.py`(`deleted_services`) · `normalized_sale.py` · `emr/sync_menu.py` |

## 1. 수행 — 파일

새 파일
- `backend/day/services/emr_backfill.py` — 백필(옵션 · 달 창 · 4 단계 · 진행 위치 · 요약)
- `backend/runtime/backfill.py` — 실행 진입점(`python -m runtime.backfill` · 이미지 `WORKDIR /app/backend` 그대로 · `runtime.worker` 와 같은 자리). `day/` 최상위에는 Taut 역할이 파일마다 등록돼 있어(`register_connection` 처럼) `taut.toml` 을 고치지 않으려고 이미 진입점 역할(bootstrap)이 있는 `runtime/` 에 뒀다
- `backend/day/emr/pacing.py` — `KosPacer`(요청 사이 ≥ 1.0초 · 시계 · 잠 바꿔 끼움 · 호출 · 재시도 수)
- 테스트 `tests/day/emr/test_backfill_rules.py`(15 · DB 없음) · `tests/day/emr/test_backfill.py`(4 · infra)

고친 파일(운영 동작 그대로 · 더하기만)
- `emr/kos/client.py` — `PacedTransport`(모든 요청 앞 `pacer.wait` · 429 · 5xx · 연결 오류는 `2 · 4 · 8 · 16`초 쉬고 다시 · 상한 4 · 재시도도 1초 간격) · `KosClient.revoke_own_sign_ins(since)`(이 클라이언트 UA 표시 · `since` 뒤 로그인만). `KosClient` 의 기존 메서드 · 운영 전송은 그대로
- `emr/factory.py` — `build_backfill_adapter`(운영 캐시 `adapter_for` 와 따로 · 표시 `backfill` · `PacedTransport` · 쓰기 없음)
- `emr/base.py` · `emr/kos/__init__.py` · `emr/kos/sale_reads.py` · `normalized_sale.py` — `fetch_customer_page`(내부 `visitor/v2/queries/get-visitors` · id · 전체 수만) · `release_own_sessions`
- `emr/kos/sale_reads.py` — 시술권 · 카드 요약의 **2xx 빈 본문 = 0 건**(아래 실물 발견)
- `day/public.py` — 백필 · `EmrError` 내보내기 · `common/error_codes.py` — `BACKFILL_INPUT_ERROR`(Taut: 예외마다 코드 하나)
- `day/models/visit.py` · `migrations/versions/20261119_0010_sale_tables.py` — `ix_visit_hospital_id_reserved_start_at (hospital_id, reserved_start_at) WHERE deleted_at IS NULL`(지금 테이블에 더하는 인덱스는 이것 하나 · downgrade 에서 지움)
- 테스트: `test_sale_sync_rules.py`(메시지 모양 · AST 검사 대상에 백필 2 파일) · `test_sale_sync_runs.py`(WARN-B) · `test_sale_sync.py`(WARN-D) · `test_kos_sale_mapper.py`(WARN-D · 빈 본문) · `tests/migrations/test_sale_tables_migration.py`(visit 인덱스 하나)

## 2. 동작 — 계약 대조

| 계약 | 구현 |
|---|---|
| 수동 실행 · 운영 스케줄 · worker 에 안 붙음 | 진입점만 · taskiq 태스크 · 스케줄 0 |
| 어제까지 · 오늘 이상 거부 | `--to` 기본 = 어제(병원 현지) · 오늘 이상 → 종료 1 · 달 창의 끝 = `--to` 다음 날 0시(오늘 0시를 넘지 않음) |
| KOS 1초 1회(재시도 포함) · 429 · 5xx 재시도(상한) | `PacedTransport` + `KosPacer` — sign-in · 사용자 계정 · 로그인 목록 · 해제까지 모든 요청 |
| 공개 API 0 | 새 코드 `"open"` 호출 · `/open/` 경로 0(AST 테스트 · grep) · 어댑터 `ApiKind = Literal["internal"]` |
| 세션 표시 `backfill` · 기기 제한이면 이 표시만 · 끝나면 자기 세션 해제 | 표시를 `backfill` 로 바꾼 클라이언트 — 기존 자동 해제(`_revoke_oldest_own`)가 같은 UA 만 보므로 운영 · 사람 세션에 닿지 않는다. 끝(실패해도 `finally`)에 `revoke_own_sign_ins(시작 - 30초)` |
| 순서 ① ~ ④ | ① 달마다 `fetch_schedules`(구역 = 내부 get-zones) → **운영 `apply_schedules` 그대로**(고객 · 방문 · 작업 · 사라짐은 그 달 창 안) + `apply_prescriptions` ② 그 달 `purchaseIds` → 80 개씩 `get-purchase-summaries`(`includeDeleted`) → `apply_purchases`(items + pendingItems · 거래 · 담당 · 조정) ③ 구매가 있는 고객(이번 실행 + DAY) → `get-ticket-bundles` → `apply_tickets` → 받은 달들의 작업 참조 `apply_task_refs` ④ `get-visitors` 전체 장(20 개씩 · 0 부터) → DAY 에 있는 고객만 `get-prepaid-card-summaries` → `apply_cards` → 바뀐 카드만(`changed_cards`) 이벤트 · 공유 고객 → `apply_card_details` · `link_transaction_cards` |
| 고객 upsert 는 기존 규칙대로 | 고객 행은 ① 일정 반영(`apply_schedules`)으로만 들어온다. 고객 목록(`get-visitors`)은 **나열에만** 쓴다(그 응답 모양이 일정 안 고객과 달라 — 전화 · 메모 칸 이름 다름 — 매핑하면 새 규칙이 된다). DAY 에 없는 고객은 카드를 받지 않고 센다(`customer_not_in_day`) |
| 새 쓰기 길 금지 | 쓰기는 2단계 · 운영과 같은 `apply_*` 함수뿐 · 소프트 딜리트만 · 물리 DELETE 0(AST 테스트) |
| `--dry-run` | KOS 는 읽고 DB 는 쓰지 않는다(읽기 조회만) · 진행 위치도 안 씀 · 받은 건수만 |
| `--resume` · 진행 위치 | 병원별 Redis `day:emr:backfill:{병원}` = `{schedules: 마지막 끝난 달, purchases: 달, tickets: 고객 순번, cards_page: 장}`(30일 만료 · 새 테이블 없음). `--resume` 없이 돌리면 처음부터(위치는 덮어씀) |
| 끝에 요약 | 단계별 받음 · 씀 · 건너뜀 · 초 + KOS 호출 · 해제한 로그인 · 전체 초 |
| 개인정보 | 출력 · 로그 = 건수 · 단계 · 달 · 장 · DAY 병원 id 뿐. 실패는 예외 이름(외부 CRM 오류만 HTTP 상태 · 오류 이름 — `EmrError` 약속상 본문 · 키 없음) |
| `visit` 날짜 인덱스 | 0010 · 살아 있는 행만(0009 관례) |

- 이어 받기 한계: 같은 실행 안에서 단계 사이에 넘기는 값(선불카드 상품 항목 → 카드 · 카드 결제 거래 → 이력)은 메모리라, 단계를 나눠 따로 돌리면 그 연결 칸이 비어 있을 수 있다(다음 오늘 회차 · `--stage all` 다시 돌리기가 채운다 · upsert 는 「있던 값 둠」).
- `get-visitors` 는 `lastVisitedDateTimeUtc` 내림차순(HAR 의 정렬 그대로)이라, 돌리는 사이 방문한 고객은 앞으로 옮겨 다른 장에서 한 번 더 · 또는 한 장 밀려 빠질 수 있다 — 그 고객은 오늘 고객이라 10초 회차가 받는다.

## 3. 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest -q tests/day/emr/test_backfill_rules.py tests/day/emr/test_sale_sync_rules.py tests/day/emr/test_kos_sale_mapper.py tests/day/emr/test_kos_client.py` | **75 passed** |
| `./scripts/test.sh -q backend/tests/day/emr/test_backfill.py`(격리 PG · Redis) | **4 passed** |
| `./scripts/test.sh -q`(전체) | **1854 passed** |
| `./scripts/test.sh --pure -q` | **1479 passed** · 375 deselected |
| `./scripts/check.sh --pure` | 구조 · ruff · format · mypy · Taut audit/check 통과 · frontend 단계만 npm 미설치(무관 · 앞과 같음) |
| grep `"open"` · `/open/` · `delete(` · `DELETE FROM` · `session.delete`(백필 3 파일) | **0** |

테스트가 덮는 것: 1초 간격(가짜 시계 · 요청 0.2초여도 간격 1.0) · 429 → 503 → 200 재시도(쉰 2 · 4초) · 상한 넘으면 마지막 응답 · 4xx 재시도 없음 · 오늘 · 내일 거부 · 인자 검사 · 달 창(병원 현지 · 해 넘김 · 마지막 = 어제 끝) · 종료 코드(접속값 담긴 예외 문자열을 찍지 않음) · 백필 어댑터 표시 `backfill` · `PacedTransport` · 자기 표시 · 시작 뒤 로그인만 해제(운영 · 사람 · 옛 것 둠) · **드라이런 DB 쓰기 0 · 진행 위치 0** · 실행 → 다시 실행(새 표 쓴 행 0 · 카드 이력 다시 안 받음 · 테이블 건수 같음) · 오늘 방문 그대로 · 지운 구매 소프트 딜리트 · DAY 에 없는 고객 카드 건너뜀 · 이어 받기(끝난 달 · 구매 · 고객 목록 장 건너뜀) · 연결 · 기준 정보 없으면 시작 안 함 · WARN-B 옛 메시지 버림 · 깨진 메시지는 그 태스크만 실패 · WARN-D 명시 삭제만 · 되살림 · 빈 본문 · visit 인덱스 하나.

## 4. DEMO 실물 (로컬 · 버리는 PG16 · Redis7 · 테스트 계정 · DEMO 테넌트만 · `--from 2026-08` · 어제까지)

순서: 기준 정보 → 오늘 일정 · 오늘 구매(앞) → **드라이런 → 실행 → 다시 실행** → 오늘 일정 · 오늘 구매(뒤).

| | 드라이런 | 실행 1 | 실행 2 |
|---|---|---|---|
| 종료 · 벽시계 | 0 · 753초 | 0 · 752초 | 0 · 733초 |
| KOS 호출 · 해제한 로그인 | 752 · 1 | 748 · 1 | 730 · 1 |
| ① 일정 받음 / 씀 / 건너뜀 | 1,315 / 0 / 2 · 6.4초 | 1,315 / 6,820 / 4 · 10.2초 | 1,315 / 5,445* / 4 · 9.6초 |
| ② 구매 받음 / 씀 | 447 / 0 · 7.7초 | 447 / 1,856 · 7.1초 | 447 / **0** · 7.2초 |
| ③ 시술권(고객 140) 번들 받음 / 씀 / 건너뜀 | 429 / 0 / 0 · 140초 | 429 / 1,932 / 7 · 142초 | 429 / **0** / 7 · 142초 |
| ④ 카드 받음 / 씀(DAY 에 없는 고객) | 36 / 0 (11) · 596초 | 33 / 32 (13) · 591초 | 17 / **0** (13) · 573초 |
| 테이블(실행 뒤) | 앞과 같음(쓰기 0) | 방문 1,319 · 작업 786 · 고객 545 · 구매 408 · 항목 543 · 거래 407 · 번들 429 · 티켓 536 · 카드 15 · 이력 33 · 공유 1 · 처방 0 | **실행 1 과 같음** |

\* ① 의 「씀」은 운영 일정 반영(`apply_schedules` · 생성 바인딩 `SyncTable`)이 **보낸 행 수**다(그 함수는 값이 같아도 upsert 한다 — 기존 동작 그대로 · 바꾸지 않음). 테이블 건수 · 값은 같다. 새 표 단계(②③④)는 「실제로 바뀐 행」이라 0.

- **오늘 행 그대로**: 오늘 방문 · 작업의 칸 해시(단계 · 방 · 지움 · 수정 시각)가 백필 전후 같음 · 오늘 이후 방문 4 그대로.
- **2단계에서 건너뛴 지난 시술권이 풀림**: 오늘 구매 회차의 `ticket_bundle.purchase_item_missing` **21 → 0**(백필이 출처 구매를 넣어서).
- 시술권 건너뜀 7 = 매핑 실패 번들(표 밖 상태 · 필수 칸 없음 등 — 기존 규칙 그대로 센다).
- 카드는 ④ 가 **바뀐 카드만** 이벤트를 다시 받아 실행 2 의 이력 호출이 줄었다(받음 36 → 17).
- 소요: 한 번에 약 12 ~ 13분 — ④ 고객 목록(28장) + DAY 고객마다 카드 요약 1회가 대부분(약 590초). 1초 1회라 **고객 수 × 1초** 가 하한이다.
- KOS 세션: 백필은 매번 자기 로그인 1개를 해제했다(표시 `backfill` 남은 것 0). 이 확인 스크립트가 연 `local` 로그인 2개도 해제 · 남은 것 0. 컨테이너 0.

### 실물에서 찾은 것 (고침)

- **KOS 는 받을 게 없는 고객의 `get-ticket-bundles` 에 2xx 빈 본문을 준다**(본문 없음 → `data` 없음). 처음 실물 세 번이 모두 여기서 `EmrError`(종료 2)로 멈췄다. 이건 **2단계 오늘 회차에도 같은 길**이다 — 그런 고객이 오늘 바뀐 고객이 되면 시술권 · 카드 단계가 10초마다 실패하고 대기 집합에 남는다. → 시술권 · 카드 요약(둘 다 사라짐을 판단하지 않는 읽기)만 **빈 본문 = 0 건**. 구매 · 카드 이력 · 공유 고객(사라짐을 판단)은 그대로 모양이 틀리면 실패.
- 진단을 위해 명령이 외부 CRM 오류의 HTTP 상태 · 오류 이름을 찍게 하고(본문 · 키 없음), 단계 · 달 · 장 진행 로그(건수만)를 표준오류로 낸다.

## 5. dev 서버 — 드라이런 · 실행 방법 (실행은 코디 · 사용자)

dev VM(`ssh day-vm` — 접속 값은 사용자 `~/.config/day/infra.json`)에서 dev api 컨테이너 안. 이미지에 `backend/` 만 있고 `WORKDIR /app/backend` 라 모듈 경로 그대로 돈다. DB · Redis · 암호화 키 · KOS 주소는 컨테이너 앱 설정, KOS 접속값은 그 병원의 `crm_connection`(명령줄 · env 로 받지 않음).

```sh
# 0) 병원 id 확인(연결이 있는 병원 · 기준 정보가 이미 돈 병원이어야 한다 — 아니면 종료 1)
# 1) 드라이런 — KOS 만 읽고 DB 0 · 건수 · 시간 · 호출 수를 본다
docker exec day-dev-api-1 python -m runtime.backfill --hospital <병원 uuid> --from 2026-08 --dry-run
# 2) 실행 — 길어서 VM 의 tmux / nohup 안에서
nohup docker exec day-dev-api-1 python -m runtime.backfill --hospital <병원 uuid> --from 2026-08 \
  > ~/backfill-$(date +%Y%m%d-%H%M).log 2>&1 &
# 3) 끊기면 같은 인자 + --resume (끝난 달 · 고객 순번 · 고객 목록 장부터)
docker exec day-dev-api-1 python -m runtime.backfill --hospital <병원 uuid> --from 2026-08 --resume
# 4) 다시 한 번 돌려 새 표 「씀」 이 0 인지 확인(멱등)
```

- 컨테이너 이름은 compose project `day-dev` 의 `api` 서비스(`docker compose -p day-dev ps` 로 확인).
- **예상 시간**: 데모(고객 ~560 · 4달) 기준 약 12 ~ 13분/회. 실 병원은 「고객 수 × 1초 + 구매 있는 고객 × 1초 + 달 수 + 구매 수 ÷ 80」 정도 — 고객 1만이면 약 3 ~ 4시간.
- 운영 worker 와 같은 시스템 계정을 쓰지만 표시가 `backfill` 이라 기기 제한 자동 해제가 worker(`dev`) 세션을 끊지 않는다. 다만 시스템 계정의 **동시 로그인 수가 꽉 찬** 상태면 백필 sign-in 이 실패한다(자기 표시 세션이 없어 해제할 게 없음 → 종료 2 · `SignInLimitExceeded`) — 그때는 KOS 웹 「기기 제한」에서 사람이 정리.
- 종료 코드: `0` 끝남 · `1` 인자 · 연결 · 기준 정보 없음 · `2` 그 밖 실패(이름 · 외부 오류면 HTTP 상태).
- `0010` 이 그 환경에 먼저 적용돼 있어야 한다(새 테이블 · visit 인덱스). visit 인덱스 만들기는 `visit` 쓰기를 잠깐 막는다(일반 `CREATE INDEX` · 행 수만큼).

## 6. 이슈 · 코디가 확인할 것

1. **2단계 버그 함께 고침** — 위 「빈 본문」(오늘 회차 시술권 · 카드 단계가 반복 실패할 수 있던 길). 운영 영향이 있는 수정이라 PR 설명에 적어 주길.
2. **WARN-C(그대로 · 확인 권고)** — prod 첫 기준 정보 회차 전후로 구역 수 · `skipped.zone` 을 한 번 본다(내부 구역 목록이 닫힌 · 지운 구역을 함께 줄 수 있는지는 데모로만 확인).
3. 실행 진입점 위치를 `runtime/backfill.py` 로 했다(브리프 「scripts/ 또는 backend 명령 모듈 — 관례를 보고」). `day/backfill.py` 로 두려면 `taut.toml` 에 역할 한 줄이 필요하다.
4. 고객 목록 응답의 고객(일정이 한 번도 없는 고객)은 DAY 에 고객 행이 없어 카드를 받지 않는다(데모 13명) — 고객 행을 고객 목록에서 만들려면 그 응답 → 고객 매핑 규칙을 SPEC 에 정해야 한다(새 규칙이라 하지 않음).
5. 백필의 오늘 창 보호는 「`--to` < 오늘」 하나로 지킨다. 같은 시각에 오늘 회차가 돌아도 쓰는 방문이 겹치지 않는다(오늘 방문은 창 밖). 시술권 · 카드는 고객 단위라 겹칠 수 있으나 upsert · 행 잠금으로 같은 결과.
