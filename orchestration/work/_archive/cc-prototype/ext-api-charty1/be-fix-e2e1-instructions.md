# backend 4차 — 로컬 e2e 에서 찾은 lookup 502 (실물 버그)

원 브리프 제약 그대로(커밋 금지 · KOS 호출 0 · 사용자 포트 금지 · public). 코디가 커밋 `c4876bd` 위에 로컬 e2e 를 돌리다 찾았다.

## 무엇이 깨졌나
- 데모 KOS 에서 **선불카드가 있는 고객**(시술권 묶음 12)을 lookup → `502 kos_unavailable`. 선불카드는 정상, 원인은 시술권.
- 내부 `ticket/v1/queries/get-ticket-bundles` 의 묶음 12 중 4가 `price = {currency}` 만 온다(**`value` 칸 없음**). 4개 모두 장이 `USED` 만 · `CANCELED` 만인 묶음. 같은 고객의 공개 `get-ticket-bundles`(옛 원천)는 4묶음 모두 `value` float 이 있다. 내부는 protobuf JSON 이라 **0 값을 빼고 보내는 것**으로 보인다(금액 0 묶음).
- `app/service/ext.py` `_ticket()` 은 `price.value` 가 숫자가 아니면 `BadGateway` → lookup 전체 502. 그리고 **거르기(`_live`) 전에** `_ticket()` 을 부르므로 내지도 않을 다 쓴 묶음 때문에 전체가 깨진다.

## 코디 기본값(planner 가 SPEC 0.4.5 · DEC-012 에 같이 적는다)
1. **거르기를 먼저** — 장 상태로 산 묶음(`AVAILABLE` 또는 `IN_USE` 1장 이상)만 골라 낸 뒤 모양 검사 · 칸 만들기를 한다. 걸러진 묶음의 모양은 보지 않는다.
2. 내부 원천의 **`price` 가 객체인데 `value` 가 없으면 0**으로 본다(protobuf 0 생략). `price` 자체가 없거나 객체가 아니거나 `value` 가 숫자가 아닌 다른 꼴(문자열 등)이면 지금처럼 502.
3. 시험: ① `price: {currency}` 만인 **산** 묶음 → `bundlePrice.value = 0` · 200 ② `price: {currency}` 만인 다 쓴 묶음이 섞여도 200 · 그 묶음은 안 나옴 ③ `price` 없음 → 502 그대로 ④ `fake_kos` 기본 내부 시술권 응답에 KOS0 처럼 value 없는 다 쓴 묶음을 하나 섞어 둔다(다른 시험이 실물 모양을 보게). 각각 변이로 잡히는지 확인.
4. 공개 시술권 쪽(기존 코드 · 다른 경로가 쓰면)은 건드리지 않는다.

검증: `uv run pytest -q tests/test_ext_lookup.py tests/test_ext_lookup2.py` → 전체 1번 · ruff. 보고 두 채널(고친 곳 파일:줄 · 수치).
