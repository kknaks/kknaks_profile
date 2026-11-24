# 매핑 JSON v3 — 상품 표 추가 리포트(2026-11-20 · data 워커)

브리프: 사용자 결정 11-20(최저가 = 장바구니 진료항목 전부를 덮는 상품 옵션 조합 중 합계 최소). 커밋 0 · silver · gold · 허브 · 앱 코드 수정 0 · 포트 손대지 않음.

## 요약

- `reference/2026-11-19-myeongdong-kos/build_mapping_json_v3.py` 를 새로 만들어 **`myeongdong-mapping-20261120-v3.json`** 을 두 경로에 썼다. 둘 다 git 무시(`data/`)이고 v2 는 남겼다.
- **v3 부터 상품 · 옵션 정본은 `products[]` 다.** `items[].options` 는 v2 호환으로만 남긴다(meta `products_are_canonical` 에도 적었다).
- 카테고리 16 · 상품 150(삭제 0) · 옵션 493(single 456 · group 37) · 이벤트가 있는 옵션 67 · 덮는 옵션이 0 인 진료항목 24.
- items 에서 `option_refs` 를 빼면 v2 와 같다. groups · sites 는 바이트가 같다. 표본 10 의 KOS raw 대조는 10/10 이다.

| 경로 | sha256 |
|---|---|
| `/Users/kknaks/git/clinic_chat/data/kos/myeongdong-mapping-20261120-v3.json` | `94b88022973805bbdc4b2350972e1e99e61a501e058062dc54753287440643f4` |
| `/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/data/kos/myeongdong-mapping-20261120-v3.json` | 같음 |
| (v2 · 그대로) `myeongdong-mapping-20261120.json` 두 경로 | `8ca88c9a…` |

다시 만들기: `python3 build_mapping_json_v3.py 57b420ad… 51e3760a… <out.json>`. items · groups · sites 는 build_mapping_json_v2.py 를 그대로 불러 짓는다. `made_at` 이 매번 바뀌므로 파일 바이트는 실행마다 다르다(v2 와 같음).

## 1. 꼴

최상위: `meta` · `items` · `groups` · `sites`(v2 그대로) · **`product_categories`** · **`products`**.

meta 에 더한 칸은 다음과 같다.
- `version: v3`
- `price_rule`: 옵션 값 = `event_price` 가 있으면 그것, 없으면 `price_amount`
- `products_are_canonical`
- `comp_event_price_note`

### 키

| 키 | 규칙 | 비고 |
|---|---|---|
| `category_key` | `C` + 원본 카테고리 목록 순번(2자리) | KOS id 대신 |
| `product_key` | `P` + 원본 상품 목록(`myeongdong-kos-products-20261119-v2.json` products) 순번(3자리) | 제목은 `title`. 원본 `order` 칸은 150 개 전부 1 이라 순서로 못 쓴다. 그래서 파일 목록 순서를 쓴다(raw `B_products.json` 순서와는 다르다). 삭제된 상품이 있어도 번호를 건너뛸 뿐 밀리지 않는다 |
| `option_key` | `<product_key>-<원본 옵션 순번>` | |

KOS 를 다시 받으면 목록 순서가 바뀔 수 있다. 그때는 키도 바뀐다. 앱은 키를 같은 파일 안에서만 쓴다.

### 상품 「[11월 이벤트] 온다50kj+티타늄30kj」(group 하나)

```json
{
 "product_key": "P015", "title": "[11월 이벤트] 온다50kj+티타늄30kj", "order": 1, "category_keys": ["C01"],
 "is_event": true, "closed": false,
 "options": [{
   "option_key": "P015-1", "title": "[11월 이벤트] 온다50kj+티타늄30kj", "type": "group", "count": null,
   "price_amount": 1100000, "supplied_amount": 1100000, "vat_amount": 110000, "taxation": "TAXABLE",
   "event_price": 590000,
   "additional_prices": [{"visitor_type": "이벤트가", "amount": 590000}],
   "description": null, "closed": null, "display_channels": ["HOMEPAGE"],
   "covers": ["26-DRPTP-OND-50KJ", "26-TTNLF-SPRNT-30KJ"],
   "compositions": [
    {"item_code": "26-DRPTP-OND-50KJ", "count": 1, "unit": {"type": "KJ", "value": 50.0}, "price": 489000,
     "additional_prices": [{"visitor_type": "이벤트가", "amount": 590000}], "comp_event_price_is_option_total": true},
    {"item_code": "26-TTNLF-SPRNT-30KJ", "count": 1, "unit": {"type": "KJ", "value": 30.0}, "price": 611000,
     "additional_prices": [{"visitor_type": "이벤트가", "amount": 590000}], "comp_event_price_is_option_total": true}
   ]}]
}
```

계산 값은 이 옵션 하나가 두 진료항목을 덮고 590,000(이벤트가)이다. 구성 줄의 590,000 은 줄마다 반복된 묶음 값이라 더하지 않는다.

### 상품 「특수부위보톡스」(single 28)

```json
{
 "product_key": "P135", "title": "특수부위보톡스", "order": 1, "category_keys": ["C03"], "is_event": false, "closed": false,
 "options": [
  {"option_key": "P135-1", "title": "거미스마일 보톡스 앨러간", "type": "single", "count": 1,
   "price_amount": 350000, "supplied_amount": 350000, "vat_amount": 35000, "taxation": "TAXABLE",
   "event_price": null, "additional_prices": [], "description": "거미스마일 보톡스 앨러간", "closed": null,
   "display_channels": ["HOMEPAGE", "GANGNAMUNNI", "KOS_CONNECT"], "covers": ["26-GUMMY-ALLG-50UNIT"]},
  {"option_key": "P135-2", "title": "거미스마일 보톡스 제오민", "…": "…", "price_amount": 200000, "event_price": null, "covers": ["26-GUMMY-ZOMN-50UNIT"]}
  /* … 옵션 28 */
 ]
}
```

single 옵션에는 `compositions` 칸이 없다. group 에만 있다.

### `product_categories[]` 한 줄

```json
{"category_key": "C01", "name": "이벤트", "order": 0, "opened": true, "deleted": false,
 "translations": {"name": {"ja": "イベント", "zh-Hans": "活动", "zh-Hant": "活動", "en": "Event"}}}
```

### `items[].option_refs`

예: `26-BBL-1MODE` → `[{"product_key": "P021", "option_key": "P021-1"}, {"product_key": "P021", "option_key": "P021-2"}]`.

진료항목마다 `option_refs` 수가 v2 `options` 수와 같은지 스크립트가 스스로 검사한다(어긋나면 멈춤). 324 항목이 모두 같았다.

## 2. 셈

| 무엇 | 값 |
|---|---|
| 카테고리 | 16(삭제 0 · 닫힘 0) |
| 상품 | 150(삭제 0 · 닫힘 1 「크라이오 (copy)」 · is_event 64) |
| 옵션 | 493 — single 456 · group 37 · 삭제 0 · 닫힘 0 |
| 이벤트가가 있는 옵션 | 67(`additional_prices` 의 visitor_type 은 「이벤트가」 하나뿐 · 옵션당 최대 1) — 그 가운데 is_event 가 아닌 상품의 옵션 2. 반대로 is_event 상품인데 옵션 이벤트가가 없는 옵션은 44 |
| group 구성 수 | 2개 27 · 3개 5 · 4개 3 · 7개 2 → **구성 2 개 이상 37(전부)**. 덮는 코드 수도 같다 |
| group 정가 = 구성 price 합 | 37/37 |
| 진료항목 324 중 덮는 옵션 0 | **24**(v2 「옵션 없음 24」와 같다) |
| 옵션이 덮는데 items 에 없는 코드 | 0 |

덮는 옵션 0 진료항목 24:

- 26-BBL-2MODE · 26-CARE-CHOOSE1 · 26-PRP-CANNULA · 26-PEELING-1 · 26-DHJBT-HTS-50UNIT
- WHITENING IV DRIP + VITAMIN IV DRIP · 26-BDBT-HTS-100UNIT · 26-BRJJG-CO2-1QUANTITY · 26---- 수액 무제한 · 26-SEUK-HTS-2CC
- 26- 엑소제 · 26-JTJJS-BRKR-3CC · 26-Avalanche-25 · 26-JJGM-CO2-100QUANTITY · 26-JJGM-CO2-1QUANTITY
- 26-HIBOTOX-3AREA · 26-CHSBT-ALLG/ZOMN/COTX/HTS-50UNIT(4) · 26-Avalanche-18 · 26-TBT-HTS-50UNIT · 26-Avalanche-19
- 26-PTNZP-JBRSK-1CC

장바구니에 이 가운데 하나라도 있으면, 그 항목을 덮는 조합이 없다.

## 3. 구성 줄 이벤트가 = 묶음 합계 반복(실측 근거)

group 37 가운데 구성 줄에 「이벤트가」가 있는 것은 12 다. 나머지 25 는 구성 줄에 이벤트가가 없다.

- 한 옵션 안에서 이벤트가가 있는 구성 줄은 **모두 같은 값**이다. 구성 price 는 줄마다 다르다(온다 489,000 · 티타늄 611,000 인데 둘 다 590,000).
- 그 값을 구성 수만큼 더하면 옵션 정가보다 커진다(590,000 × 2 = 1,180,000 > 1,100,000). 그러니 구성 몫이 아니라 묶음 합계다.
- 12 가운데 8 은 그 값이 옵션 `event_price` 와 같다.
- **4 는 다르다.** 대부분 같은 상품의 형제 옵션 이벤트가가 남아 있는 꼴이다:

| 상품 / 옵션 | 옵션 event_price | 구성 줄 이벤트가 |
|---|---|---|
| [11월 이벤트] 울쎄라피프라임300샷+온다30kj+… / …벨라콜린2cc | 1,259,000 | 1,190,000(형제 옵션 값) · 셋째 줄 없음 |
| [11월 이벤트] 포텐자(N팁)+엑소좀2.5cc+크라이오+모델링팩 / 4구성 옵션 | 355,000 | 350,000(형제 옵션 값) · 뒤 두 줄 없음 |
| [11월 이벤트] 피코토닝+티타늄50kj+리쥬란… / 리쥬란HB2cc+백옥 | 760,000 | 690,000(형제 옵션 값) · 넷째 줄 없음 |
| [국내DB]My Pick [온다40KJ/ 티타늄40KJ…] / 티타늄40KJ | 199,000 | 230,000(첫 줄만) |

그래서 구성 줄마다 `comp_event_price_is_option_total`(구성 줄에 이벤트가가 있으면 true)을 두고, **계산은 옵션 `event_price` 만 쓴다**. 구성 줄 `additional_prices` 는 원본 그대로 남겼다. 위 4 건은 KOS 쪽 입력 흔적으로 보인다. 병원 확인 대상으로 넘긴다(고치지 않음).

## 4. 검증

- **items · groups · sites**: v3 `items` 에서 `option_refs` 를 빼면 v2 파일(8ca88c9a)의 `items` 와 같다(같은 들여쓰기로 직렬화해 비교). `groups` · `sites` 바이트가 같다. meta 는 version · made_at 과 새 칸 3 만 다르다.
- **표본 10 원본 대조**(KOS raw `raw/B_products.json` 에서 상품 · 옵션 id 로 찾음 · 고정 seed): group 4 · 이벤트 single 3 · 일반 single 3. 상품 · 옵션 제목, type, count, 정가 · 공급가 · VAT · 과세, covers(raw `medicalService.configuration.code`), additional 수를 봤고 **10/10 일치**했다.
  - P052-1 · P125-2 · P043-1 · P036-1(group)
  - P061-4 · P020-1 · P071-1(이벤트 single)
  - P054-2 · P112-19 · P056-2(single)
- 대조 스크립트: scratchpad `v3_verify.py`(일회성).

## 5. 남은 것

- 덮는 옵션 0 진료항목 24 를 화면에서 어떻게 보일지(최저가 계산 불가 표시)는 앱 단계에서 정한다.
- 위 §3 의 4 건은 병원에서 구성 줄 이벤트가를 확인할 대상이다(계산에는 영향 없음).
