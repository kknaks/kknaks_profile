# 리뷰 리포트 — day-procedure-board-2 / code — `scripts/seed_demo_board.py` (2026-11-09)

대상: 미추적 `scripts/seed_demo_board.py` · `backend/tests/scripts/{__init__,test_seed_demo_board}.py`
근거: be 브리프 §2 · §3 · §6 · §7(이하 「브리프」) · HAR `고객예약접수시술.har`(경로 · 필드 이름 · enum 값만 봄 — 고객 값은 보지도 옮기지도 않음) · 레포 `AGENTS.md`
실행: KOS 호출 0회. `uv run pytest -q backend/tests/scripts` **14 passed** · `ruff check` · `ruff format --check` 통과 · `tests/architecture` 27 passed.

## 판정: FAIL (1건 — 고치기 쉬움) · WARN 8

---

## FAIL

### F1. 데모 가드가 **공개 키**의 테넌트를 확인하지 않는다 — 첫 쓰기(reserve)는 공개 키의 병원으로 간다
- `scripts/seed_demo_board.py:107-109 · 532` 가드는 `DAY_SEED_KOS_TENANT_ID` 문자열만 본다.
- 공개 API(`exchange-token` · `get-zones` · **`reserve`** · `get-schedule-detail`)는 URL 에 테넌트가 없다. 어느 병원에 쓰는지는 **`DAY_SEED_KOS_OPEN_API_KEY` 가 정한다**(`client.py:162-163 · 190-204`). 내부 API 만 `tenants/{tenant_id}/…` 로 데모에 묶인다(`client.py:165-169`).
- 브리프 §7 「명동점 키(`KOS_API_tenent`) 사용 금지」는 이 키를 막으라는 뜻인데, 실제로 막는 것은 테넌트 id 뿐이다.
- **명동점 키로 돌리면 어디서 멈추나**:
  - 테넌트 id 까지 명동점 값이면 → `:532` 에서 멈춘다. KOS 호출 0회(토큰 교환 전). PASS.
  - 테넌트 id 는 데모이고 **공개 키만 명동점 값이면** → 가드를 지나간다. `exchange-token`·`get-zones` 를 명동점에 보내고(조회), 명동점 zone id 로 데모 내부 `get-rooms` 를 부른다(`:220`). 여기서 방이 비어 `:246` 에서 멈추는지, `reserve`(`:284`, 명동점 zone + 데모 예약 그룹 id)를 KOS 가 거절하는지는 **확인 못 함**(KOS 동작). 지금은 우연히 걸리는 안전장치뿐이고, KOS 가 모르는 zoneId 를 무시하면 **실제 병원에 `[TEST]` 예약이 생긴다**.
- 고치는 법(작음): `masters()` 에서 쓰기 전에 공개 쪽 zone id 가 데모 내부 쪽에 실제로 있는지 확인한다. 예: 기본 예약 그룹 `intervalCapacities[].zoneId`(`mapper.py:237-249` 가 읽는 칸)에 `zone["id"]` 가 없으면 `KosError`. 이 확인은 dry-run 에서도 돈다.

---

## WARN

### W1. 쓰기 timeout · 네트워크 끊김 → 「실패」로만 찍히고 KOS 에 남은 것은 안 보인다(조용히 통과하는 자리)
- `client.py:174-177` 은 httpx 오류를 `KosError("network …")` 로 바꾸고 다시 보내지 않는다 → **중복은 없다**(아래 「재시도 · 중복」 참고).
- 다만 `reserve`(`:284`)가 timeout(30초, `:538`)으로 끝났는데 KOS 는 처리했다면 `schedule_id` 가 빈 채로 `…----  실패(reserve: network ReadTimeout)` 로 찍힌다(`:521`). 예약은 남았는데 표에는 id 가 없다. 다른 단계도 같다 — 예를 들어 `initialize-purchase` 다음에 끊기면 만들다 만 수납이 남는다.
- 사용자가 다시 돌리면(W2) 이렇게 남은 방문 위에 또 쌓인다. 제안: 실패 줄에 「KOS 에 남았을 수 있음 — `[TEST] … MMDD-HHMM-NN` 이름으로 찾기」 한 줄을 붙인다(이름 자체는 찍지 않는다).

### W2. 같은 칸을 다시 돌리면 그대로 중복 — 막는 장치 없음
- `visitor_name`(`:140-142`)은 (칸 · 순번)만으로 정해져 같은 칸을 다시 돌리면 **같은 이름**으로 10명이 또 생긴다. docstring 은 「실행(칸)마다 달라 KOS 가 기존 내원객과 묶지 않는다」라고 하지만, 같은 칸을 두 번 돌리는 경우는 그 반대다. KOS 가 같은 이름을 같은 내원객으로 묶는지는 **확인 못 함**.
- 실패한 사람만 다시 만드는 옵션도 없다. 한 명이 실패해서 다시 돌리면 성공한 9명이 또 생긴다.
- 시드용이라 FAIL 은 아니다. 제안: 이름에 실행 시각 초 또는 짧은 무작위 접미어를 넣는다. 아니면 `--only N` 을 둔다.

### W3. `KosError` 가 아닌 예외는 한 명이 아니라 **전체를 멈춘다**
- `:555-558` 은 `KosError` 만 잡는다. `KeyError`·`IndexError`·`TypeError` 는 위로 올라가서 남은 사람을 건너뛰고 요약(`:563-565`)도 찍지 않는다. 어디까지 만들었는지도 안 남는다.
- 실제로 걸릴 수 있는 자리:
  - `_purchase_item` 의 `conf["procedure"]["id"]`(`:436`). `usable` 필터(`:239-245`)는 `configuration` 이 있는지만 보고 `procedure` 는 보지 않는다. 그리고 이 코드는 `initialize-purchase`(`:335`) **다음에** 돈다. 그래서 수납만 만들어 놓은 채 전체가 멈춘다.
  - `etc["title"]`(`:314`), `room["id"]`(`:327`).
- 브리프 §6.3 「한 명 실패 시 그 사람만 건너뛰고 … 전체 중단 X」를 어긴다(데이터가 정상이면 안 걸린다).
- 제안: `:557` 을 `except Exception as exc:` 로 넓히고 `res.error = type(exc).__name__ + …` 로 남긴다. 예외 메시지에 응답 값이 섞일 수 있으니 이름만 남긴다.

### W4. 국적 코드 — 브리프 §3 「`meta/codes` 조회값으로 맞춘다」와 다르다
- `:63-81` 은 ISO 3166-1 alpha-2 를 코드에 박아 두었다. 근거는 공개 API 문서(`visitorNationality`)다.
- HAR 의 `meta/codes` 요청은 `category = CONSULTATION_RESULT` 하나뿐이다. 국적 분류가 `meta/codes` 에 있는지는 HAR 로 확인할 수 없다(워커 보고 ②와 맞다).
- 공개 문서가 alpha-2 를 요구하는지는 이번 리뷰에서 **확인 못 함**(KOS 조회 금지). 실물에서 10명 모두 2xx 였다는 것은 워커 보고다.
- 브리프에서 벗어난 것이므로 **코디네이터 · 사용자의 승인이 필요**하다. 언어 `TW → None`(`:74`)도 같다.

### W5. 가드 순서를 지키는 테스트가 없다(조용히 통과하는 자리)
- `test_demo_tenant_guard`(`test_seed_demo_board.py:75-80`)는 함수 하나만 확인한다. `run()` 이 **KosClient 를 만들기 전에** 가드를 부르는지는 아무 테스트도 보지 않는다.
- 지금 코드는 맞다(`:532` → `:537`). 하지만 누가 순서를 바꾸면 테스트는 초록인데 토큰 교환이 먼저 나간다.
- 제안: tenant env 를 명동점 값으로 넣고 `KosClient` 를 monkeypatch 한 뒤 `run()` 을 돌려, `SystemExit` 가 나고 KosClient 가 한 번도 만들어지지 않았는지 단언한다. DB · KOS 는 필요 없다. F1 을 고치면 그 확인도 FakeKos(`tests/day/emr/test_kos_client.py` 에 있음)로 같이 막는다.

### W6. 재시도 로직(`detail` 404 · `tickets` 빈 응답 · verify)이 테스트되지 않았고, 고친 뒤 끝까지 다시 돌려 보지도 않았다
- 워커 보고 ①: `exc.args → exc.status` 를 고친 뒤 한 타임을 처음부터 끝까지 다시 돌리지 않았다.
- 코드를 읽어 보면 지금이 맞다. `EmrError.status`(`base.py:27-29`) · `_error_of` 가 `status_code` 를 넘긴다(`client.py:110-112`).
- 그래도 `detail()`(`:253-262`)에서 「404 면 기다림 · 다른 상태면 바로 raise · 마지막은 raise」를 지키는 테스트가 없다. 고친 버그가 다시 들어와도 초록이다. 가짜 client 로 DB 없이 테스트할 수 있다.

### W7. `--date` 만 주고 `--slot` 을 안 주면 엉뚱한 칸 · 지난 칸을 막지 않는다
- `slot_start(now, day, None)`(`:121-125`)은 「지금 다음 칸의 시각」을 주어진 날짜에 붙인다. 23:45 KST 에 `--date <오늘>` 로 돌리면 다음 칸이 00:00 이라 **오늘 00:00**(이미 지난 칸)이 된다. 테스트는 이 경우를 보지 않는다(`test_seed_demo_board.py:45-50`).
- `--slot 09:00` 처럼 지난 칸이나 지난 날짜도 그대로 보낸다. KOS 가 받아 주는지는 확인 못 함.
- `--count` 에 상한이 없다(`:572`). `--count 1000` 을 넣으면 한 칸에 1000명을 그대로 쓴다.
- 제안: 지난 칸이면 거부하거나 경고하고, `--count` 에 상한(예: 30)을 둔다.

### W8. 「끝에 실패 사유 출력」 — 사유가 사람마다 진행 중에 찍히고, 끝에는 숫자만 나온다
- 브리프 §6.3 은 「끝에 실패 사유 출력」이다. 지금은 `:560` 에서 한 줄씩 사유를 찍고, `:564` 는 개수만 찍는다. 10명이면 읽는 데 문제는 없다. 다만 브리프 문구와는 다르다. 끝 요약에 실패한 사람의 번호 · 단계 · 사유를 다시 찍으면 맞는다.

---

## 항목별 대조

### 브리프 §3 사용법
| 항목 | 판정 | 근거 |
|---|---|---|
| `--slot` 없으면 지금(KST) 다음 30분 칸 | 지킴 | `:112-116` · 테스트 `:31-42`(경계 · 자정 넘김) |
| `--date` 없으면 오늘(KST) | 지킴 | `:129` `now.astimezone(KST).date()`. 23:45 이후 다음 칸은 다음 날 00:00(테스트 `:37`) — 자연스럽다 |
| `--slot` 30분 경계 검사 | 지킴 | `:127-128` · 테스트 `:53-56`. 잘못 넣으면 사용법 안내 없이 traceback 이 나온다(사소) |
| `--count` 기본 10 · 넘으면 반복 | 지킴 | `:133-137 · 572` · 테스트 `:59-65` |
| 국적 10개(한 · 중 · 일 · 대만 · 홍콩 · 미 · 태 · 베 · 싱 · 몽) | 지킴 | `:70-81` |
| 국적 코드 = `meta/codes` 조회값 | **어김** | W4 |
| 이름 `[TEST]` · 개인 값 가짜 | 지킴 | `:142`. 전화 · 이메일은 아예 보내지 않는다(워커 ③ — 실제 번호로 알림이 갈 위험이 없어 더 안전) |
| 오더 메모 「테스트 오더 메모 n」 | 지킴 | `:414` |
| 시술 · 방 = 조회 결과에서 | 지킴 | `:220-245 · 306 · 326 · 333`. 이름을 지어내지 않는다 |
| 끝 출력 = 국적 · id 끝 4자리 · 단계, 이름 · 전화 없음 | 지킴 | `:520-523` |

### 브리프 §6 · §7
| 항목 | 판정 | 근거 |
|---|---|---|
| 한 명 실패 → 그 사람만 건너뜀 | 일부 | `KosError` 만 그렇다. W3 |
| 순수 로직 테스트 · KOS 호출 없음 | 지킴 | 테스트 파일에 네트워크 없음. 가드 순서는 W5 |
| 데모 지점에서만 · 명동점 키 금지 | **어김(일부)** | F1 |
| `backend/day/` · DB · migration 안 만짐 | 지킴 | `git status` 미추적 2개(스크립트 · 테스트 폴더)뿐 |
| `KosClient` 재사용 · 새 HTTP 클라이언트 없음 | 지킴 | `:47 · 537-539` |
| 기존 데모 데이터를 고치거나 지우지 않음 | 지킴 | 모든 쓰기가 이번 실행에서 만든 `sid` · `purchase_id` 에만 간다. `tickets()` 는 `purchaseId` 로 이번 수납의 시술권만 고른다(`:390`) |
| 키 · 토큰 · 고객 값이 출력 · 로그에 없음 | 지킴 | 아래 「개인 값 · 키」 |

### HAR 와 비교(경로 · 순서 · 본문 모양)
- **순서**: HAR 쓰기 순서와 같다. `recept → (get-ticket-bundles · get-etcetera-tasks) → add-flow-tasks(ETCETERA) → get-rooms → change-tasks-room → change-flow-step → search-product-option-summaries → initialize-purchase → add-pending-purchase-items → register-purchase → add-transaction → accept-purchase → get-ticket-bundles → add-flow-tasks(PROCEDURE) → change-order-memo`. PASS.
- **본문 필드**: 쓰기 10개 모두 HAR 와 필드 이름 · 구조가 같다. `recept {scheduleId}` · ETCETERA 작업 · `change-tasks-room {scheduleId, sequences:[1], roomId}` · `change-flow-step {id, step=CONSULTATION_WAITING}` · `initialize-purchase {id, visitorId, assigneeId, assigneeIds}` · 품목(`optionConfiguration` · `medicalService.configuration` · `price/priceV2/basePrice`) · `register-purchase` · `add-transaction`(CASH · APPROVED · `cashConfiguration {}` · `paymentDateTime`) · `accept-purchase` · PROCEDURE 작업(`round {total:1,current:1}` 은 HAR 값과 같음) · `change-order-memo`. PASS.
- **앞 응답에서 넘겨받는 id**: `scheduleId`(reserve) → visitor.id(공개 상세) → 수납 id · 품목 id · 거래 id 는 클라이언트가 만든 uuid(HAR 도 클라이언트가 정함) → 시술권 id(`get-ticket-bundles`, 이번 `purchaseId` 로 고름). PASS.
- **HAR 에 없는 것(지어낸 자리)**:
  1. `reserve`(공개 reserveV2) — 브리프가 허용했다. 응답에서 `scheduleId` 를 data 밖 최상위에서 읽는다(`:284`). 문서와 맞는지는 확인 못 함(실물 성공은 워커 보고).
  2. `get-schedule-detail`(공개) · `get-zones`(공개) · `get-reservation-groups {deleted:false}`(내부) — 조회 경로다. 앞의 둘은 레포 sync 가 이미 쓰는 경로다(`day/emr/kos/__init__.py:45`, fixture README). 쓰기 아님. PASS.
  3. 마지막 `change-flow-step step=PROCEDURE_WAITING` — HAR 에 없다(워커 ⑤). `writes.py:45 · 56` 과 같은 내부 경로 `{id, step}` 이다. `writes.py` 는 이 값을 「cc 근거 · 데모 연결 전용(TRIAL_STEPS)」으로 둔다. 데모 전용 스크립트라 맞는 쓰임이다. 브리프 §2 의 「**공개** change-flow-step(DAY writes.py 가 쓰는 것)」은 브리프 안에서 앞뒤가 안 맞는다(writes.py 는 내부 경로를 쓴다). 코드는 writes.py 쪽을 따랐다. PASS(브리프 문구는 고쳐야 함).
  4. HAR 의 `get-products`(v3)는 부르지 않는다. 옵션 요약만으로 품목을 만든다. 쓰기 본문 모양은 HAR 와 같다. PASS.
  5. 방은 기타 작업(seq 1)에만 붙인다(워커 ④) — HAR 와 같다(`sequences:[1]`).

### 재시도 · 중복 쓰기(「조용히 통과하는 자리」 1순위)
- `KosClient.call`(`client.py:258-271`): 401 일 때만 토큰을 다시 받아 **한 번 더 보낸다**. 401 은 인증에서 막힌 것이라 KOS 가 처리하지 않았다 → 중복 없음.
- 그 밖의 4xx · 5xx · 네트워크 오류는 다시 보내지 않는다(`:268-269 · 174-177`).
- 스크립트의 재시도 3곳 — `detail()`(`:253-262`), `tickets()`(`:378-396`), verify 반복(`:421-430`) — 은 **모두 조회**다. 쓰기는 반복문 안에 없다.
- → **쓰기를 두 번 보내는 자리는 없다.** 남은 위험은 「보냈는데 응답을 못 받은」 경우(W1)와 「다시 돌린」 경우(W2)다.

### `--dry-run`
- 쓰는 것 없음. PASS. 나가는 요청은 `exchange-token` · `sign-in` · `get-user-account`(`:542`)과 조회 5개(`:211-237`)뿐이고 `:548-551` 에서 return 한다. 업무 데이터에 쓰는 요청은 0개다. sign-in 이 KOS 에 로그인 기록을 남기는지는 업무 데이터가 아니라 따지지 않는다.
- 가드(`:532`)가 dry-run 판단보다 먼저 돈다. 테넌트가 데모가 아니면 dry-run 이라도 토큰 교환 전에 멈춘다.

### 개인 값 · 키 · 토큰
- 출력에 나가는 값: 칸 시각, 기준 정보 개수, 번호 · 국적 코드 · 국적 이름 · schedule id 끝 4자리 · 단계, 오류 메시지. 오류 메시지는 `KosError` 의 「HTTP 상태 + className 끝」, 아니면 스크립트가 만든 고정 문구다(`client.py:102-112`). 응답 본문 · 키 · 토큰 · 이름 · 테넌트 id 는 찍지 않는다. PASS.
- 로그: 스크립트가 logging 을 설정하지 않아 기본이 WARNING 이다. client 의 INFO 로그(라벨 `demo-seed` 만 있음)도 나오지 않는다. httpx 는 WARNING 으로 묶여 있다(`client.py:32`). PASS.
- 테넌트 id `6a793cd92416d118817a09b1` 이 코드에 상수로 박혀 있다(`:53`). 이 값은 비밀이 아니라 **가드 기준값**이다. 브리프 §7 이 이 값을 직접 지정했다. 다만 레포 `AGENTS.md` 의 「부재값은 env 로 연다」와는 결이 다르다. 가드는 「env 와 무관한 고정 기준」이어야 의미가 있어서 박아 둔 것은 맞는 선택이라고 본다(참고).
- 예외 W3 의 traceback 에는 키 이름(`'procedure'`)만 나오고 값은 나오지 않는다.

### 테스트가 실제로 막는 것
| 대상 | 막음? | 근거 |
|---|---|---|
| KST 30분 경계 · 딱 맞는 시각 · 자정 넘김 | 예 | `test_seed_demo_board.py:31-42` |
| UTC 입력 → KST | 일부 | `:45-50`(04:29Z 하나). UTC 로는 전날이고 KST 로는 다음 날인 시각(예: 15:10Z)에 `--slot` 을 준 경우는 없다. 코드는 맞다(`:129`) |
| `--date` 만 줄 때 | 일부 | W7 |
| 국적 순환 | 예 | `:59-65` |
| 가드 함수 | 예 | `:75-80` |
| 가드가 네트워크보다 먼저 | **아니오** | W5 |
| 공개 키 테넌트 | **아니오** | F1 |
| 404 재시도 · 다른 상태 바로 실패 | **아니오** | W6 |
| 가격 합산 · 시각 문자열 · 빠진 것 확인 | 예 | `:83-119` |

---

## 직원이 실물에서 만날 자리
- 같은 칸을 두 번 돌리면 현황판 14:30 칸에 같은 이름의 `[TEST]` 20명이 생긴다(W2). 반쯤 만든 방문(접수만 됨 · 수납만 됨)이 「대기」 칸에 섞일 수 있다(W1 · W3).
- 데모 지점에 수납 · 시술권 · 현금 거래가 사람당 하나씩 쌓인다. 지우는 방법이 없다(브리프가 지우기를 막았다). 데모 지점의 매출 · 정산 화면에 보인다.
- 국적이 KOS 화면에서 제대로 보이는지(alpha-2 를 KOS 가 국적으로 읽는지)는 워커 실물 결과에 기대고 있다(W4).

## 참고(기존 부채 · 무관)
- 경로 상수가 `day/emr/kos/__init__.py`(`PATH_GROUPS` 등)와 스크립트(`:84-100`)에 따로 있다. 지금은 값이 같다. 스크립트라 그대로 둬도 된다.
- 브리프 §2 「공개 change-flow-step(DAY writes.py 가 쓰는 것)」 — writes.py 는 내부 경로를 쓴다. 브리프 문구를 고칠 것.
- 테스트는 `importlib` 로 스크립트를 읽는다(`test_seed_demo_board.py:18-27`). 그래서 import 할 때 `sys.path.insert`(`:45`)가 테스트 프로세스 전체에 적용된다. 해는 없다.
