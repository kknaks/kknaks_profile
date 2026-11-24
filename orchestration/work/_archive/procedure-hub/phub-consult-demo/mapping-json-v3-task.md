# [data] 매핑 JSON v3 — 상품 표(products · categories) 추가 (사용자 결정 11-20)

너는 procedure-hub 데이터 워커다. 커밋 0 · 서브에이전트 0 · silver · gold · 허브 · 앱 코드 수정 0 · 사용자 포트 손대지 마라.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · `R=$P/reference/2026-11-19-myeongdong-kos` · 지금 v2 = `myeongdong-mapping-20261120.json`(8ca88c9a · `$R/build_mapping_json_v2.py` · `$W/mapping-json-v2-report.md`) · KOS 상품 원본 `$R/myeongdong-kos-products-20261119-v2.json`(+ `$R/raw/`)

## 목표
최저가 = 장바구니 진료항목 전부를 덮는 **상품 옵션 조합 중 합계 최소**(이벤트가 있으면 이벤트가 · 없으면 정가). 앱이 JSON 하나로 계산하게 상품 단위 표를 둔다. 값은 KOS 원본 그대로(합치거나 짓지 않음).

## 할 일
1. `build_mapping_json_v3.py` → **`myeongdong-mapping-20261120-v3.json`**(두 경로 · git 무시 확인 · v2 는 남김).
2. `product_categories[]`: 원본 그대로(name · order · opened · deleted · 번역 — KOS id 대신 순번 키).
3. `products[]`(삭제 제외 · 150 안팎 — 셈): `product_key`(안정 키 — 원본 순서 + 제목) · `title` · `category_keys` · `is_event` · `closed` · `options[]`:
   - `option_key` · `title` · `type`(single / group) · `count` · `price_amount`(정가) · `supplied_amount` · `vat_amount` · `taxation` · `event_price`(옵션 단위 `additional_prices` 의 visitor_type 「이벤트가」 amount · 없으면 null) · `additional_prices`(원본 그대로) · `description` · `closed` · `display_channels`
   - `covers[]`: 이 옵션이 덮는 진료항목 코드(single = 1 개 · group = 구성 전부 — 구성 줄 원본(count · unit · price · additional_prices)도 `compositions[]` 로 · 단 **구성 줄의 이벤트가는 옵션 합계가 반복된 값**이라 따로 표시(`comp_event_price_is_option_total: true` 같은 칸)하고 리포트에 실측 근거).
4. `items[]` 에 `option_refs[]`(이 진료항목을 덮는 product_key · option_key 목록) — v2 의 items[].options 는 남기되 리포트에 「v3 부터 products 가 정본」 표기.
5. 셈 · 검증: 옵션 수 · single / group · 이벤트가 있는 옵션 수 · 진료항목별 덮는 옵션 0 인 것(24 근처) · group 중 구성이 2 개 이상인 것 · 표본 10 원본 대조 · items · groups · sites 는 v2 와 바이트 같음.
6. 리포트 `$W/mapping-json-v3-report.md`: 꼴 예시(상품 「[11월 이벤트] 온다50kj+티타늄30kj」 · 「특수부위보톡스」) · 셈 · 두 경로 sha.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_55eba57e-07c1-4210-b8b4-f44cf7865f50 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: 매핑 JSON v3" --body "상품 / 옵션 / 이벤트가 / sha"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] data JSON v3 완료 — <한 줄>. 상세는 인박스." --enter
```
