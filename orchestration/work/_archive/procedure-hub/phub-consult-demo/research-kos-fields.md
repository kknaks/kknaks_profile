# 명동점 KOS 응답 칸 전수 · JSON v2

> researcher · 2026-11-19 · 읽기만 · KOS 를 다시 부르지 않았다.
> 원천은 `reference/2026-11-19-myeongdong-kos/raw/`(A ~ F 원응답 · gitignore)다. v2 는 `myeongdong-kos-products-20261119-v2.json`(gitignore)이고 v1 은 그대로 두었다.
> 이 문서에는 칸 이름 · 셈 · 짧은 값만 적는다. 가격은 「숫자」, id 는 「(id)」 로만 쓴다.

## 한눈 표

| 무엇 | 수 |
|---|---|
| 키 경로(A ~ F · 중첩 · 배열 안 · 배열 길이 포함) | **230** |
| v1 에 옮김 ○ | 82 |
| v1 에 없음 → v2 에 더함 | **76** |
| 옮길 필요 없음 — 배열 길이 19 · 값 하나(KRW) 22 · 같은 id 의 다른 칸으로 닿음 11 · 이름과 같음 4 · 늘 비어 있음 2 | 58 |
| v1 · v2 둘 다 없음 — 가격 세부(공급가 · 부가세 · 면세 · 과세 · 수가 유형 id) | 14 |
| v2 counts = v1 counts | **같음**(10 칸 모두) |
| 놓쳤던 핵심 | 시술 항목 `description` **15 항목 · KOS 시술 10**(지방분해주사 계열) — 글은 1 종(병원 확인 배합) |

## 1. 특히 볼 칸

| 칸 | 채움 / 전체 | 「-」 | v1 | v2 이름 |
|---|---|---|---|---|
| 시술 항목 `medicalService.description`(단품 · 구성) | 43 / 456 · 1 / 95(고유 항목 **15** · 글 **1 종**) | 0 | ✗ | `treatment_items[].description` |
| 시술 항목 `medicalService.caution` | 0 / 456 · 0 / 95 | | ✗ | `treatment_items[].caution`(모두 null) |
| 시술 항목 `translsMap.caution` | 76 항목에 칸이 있음 · 번역이 든 것 **1**(「[추가옵션] 포트라 10KJ 추가 (단독 사용 불가)」 의 en · ja · zh) | | ✗ | `treatment_items[].translations.caution` |
| 시술 항목 `translsMap.title` | 335 / 456 · 74 / 95 | | ✗ | `treatment_items[].translations.title` |
| 시술 항목 `priceAmount` | 2 / 456 · 2 / 95 | | ✗ | `treatment_items[].price_amount`(숫자) |
| 상품 `description` | 150 / 150 · **「-」 60** · 쓸 글 90(고유 89) | 60 | ✗ | `products[].description`(「-」 → null) |
| 상품 `caution` · `cautions[]` | 0 / 150 · 빈 글 `[""]` 85 · `[]` 65 | | ✗ | `products[].caution` · `cautions`(모두 비어 있음) |
| 상품 `displayPeriod` · `offeringPeriod` | 56 / 150 · 56 / 150 | | ✗ | `display_period` · `offering_period` {start, end} |
| 상품 `badges[]` | 150 개 모두 길이 0 | | ✗ | `badges`(모두 []) |
| 상품 `targetCountryCodes[]` | 150 / 150 · 값 KR · ETC | | ✗ | `target_country_codes` |
| 상품 `medicineAndMachines[]` | 상품 142 · 236 줄 · 고유 73 | | ✗ | `products[].medicine_and_machines` |
| 상품 `translsMap`(title · description) | 102 · 76 행 | 1 | ✗ | `products[].translations`(103 상품) |
| 옵션 `description` | 493 / 493 · **「-」 212** · 쓸 글 281 | 212 | ✗ | `options[].description` |
| 옵션 `displayChannels[]` | 808 값 · HOMEPAGE · GANGNAMUNNI · KOS_CONNECT | | ✗ | `options[].display_channels` |
| 옵션 `frequentlyUsedOption` | 493 모두 false | | ✗ | `frequently_used_option` |
| 옵션 `badges[]` · `promotionConfigurations[]` | 493 모두 길이 0 | | ✗ | `badges` · `promotion_configurations`(모두 []) |
| 옵션 `procedure.id` | 456 / 456 | | ✗ | `options[].treatment_kos_id` |
| 옵션 `medicineAndMachines[]` | 옵션 438 · 고유 70 | | ✗ | `options[].medicine_and_machines` |
| 옵션 `translsMap`(title · description) | 310 · 237 | 1 | ✗ | `options[].translations` |
| 구성 `price.additional[]`(이벤트가) | 구성 29 줄 | | ✗ | `compositions[].additional_prices`(숫자) |
| 구성 `medicineAndMachines[]` | 91 줄 | | ○(약품 · 기기로 합침) | + `compositions[].medicine_and_machines` |
| 카테고리 · 품목 · 선불 · 기타 작업 `translsMap` | 15 · 0 · 8 · 0 행 | | ✗ | `translations` |
| 시술 `createDate` · `categoryIds` · `searchPhoneticName` | 827 · 길이 0 · 이름과 다른 것 1 | | ✗ | `created_at` · `category_ids` · `search_phonetic_name` |
| 품목 분류 `default` · `category` | 14 · 값 1 종 | | ✗ | `default` · `category_type` |

- **빈 표지 「-」** 는 상품 description 60, 옵션 description 212, 번역 description 각 1 이다. v2 에서는 모두 null 이다. 빈 글 `""` 도 null 로 두었다.
- 개인정보 · 테넌트 칸은 응답에 없다. v2 grep 결과 이메일 · 휴대폰 · JWT · `tenant` · `bearer` 모두 0 이다.
- 스크립트는 `fetch_kos_products.py` 의 `enrich_v2`(v2 전용 · `--from-raw --v2` 에서만)다. 호출 코드와 v1 `build` 는 그대로이고, v1 을 다시 만들면 바이트까지 같다(`cmp`).

## 2. 설명 칸에서 매핑 근거 찾기

시술 항목 · 옵션 · 상품의 description · caution 을 KOS 시술 124 별로 모았다(옵션이 가리키는 시술 항목 기준).

| 글의 자리 | 글이 있는 KOS 시술 |
|---|---|
| 시술 항목 description | **10** |
| 옵션 description | 82 |
| 상품 description | 88 |
| 시술 항목 caution 번역 | 1(포트라) |
| caution 원문 | 0 |
| 합(하나라도) | 97 |

### 2-1. 시술 항목 description — 병원 확인 배합(1 종 · 15 항목)

> 실제 사용 약물 구성(병원 확인, 8/25): 하프셀라인 100cc + 아미노 5A + 알포콜린 5A + 엘카르니틴 5A + 하이랙스 3A + 밀리핏 1A + 페니 4A + 비본 0.4cc + 리도카인 20cc. 대표 약물은 최대 용량 성분인 하프셀라인으로 지정.

- **KOS 시술 10**: 바디 지방분해주사 · 복부 · 볼 · 부유방 · 브라라인 · 얼굴 · 옆구리 · 이중턱 · 팔 · 허벅지 지방분해주사
- 성분 9 개를 허브 제품 이름(`s_product` · g_entry product)과 대 보았다.

| 성분 | 정확 · 정규화 일치 | 허브 이름이 성분 글자를 포함 |
|---|---|---|
| 하프셀라인 | 0 | 0 |
| 아미노 | 0 | 0 |
| 알포콜린 | 0 | 0 |
| 엘카르니틴 | 0 | 0 |
| 하이랙스 | 0 | 0 |
| **밀리핏** | 0 | **PRD-729 밀리핏주사**(약제 · `s_product_procedure` → PRC-123) |
| 페니 | 0 | 0 |
| 비본 | 0 | 0 |
| 리도카인 | 0 | 0 |

- 「밀리핏 → PRD-729」 는 글자 포함으로만 닿았다(「주사」 가 더 붙음). 매핑에 쓴 근거는 사용자 결정(11-19)이다 — 매핑 CSV 갱신은 `research-kos-map.md` §0 에 있다.

### 2-2. 옵션 · 상품 description

- 허브 제품 이름(2 글자 이상)이 글 안에 들어 있는 KOS 시술은 **34** 다.
- 묶음 상품의 설명이 그 묶음의 모든 시술에 붙어서 잡음이 많다. 예: 목주름필러에 「소프웨이브」, 바디 지방분해주사에 「온다」, 쥬베룩에 「포텐자」 · 「더마샤인」.
  - 「그 시술의 제품」 이라는 근거가 되지 않는다. **매핑에 반영하지 않았다**(추정 금지).
  - 이미 이름 · 약품 · 기기로 닿은 제품과 같은 글자(예: 보톡스 줄의 「보톡스 · 제오민 · 코어톡스」)가 대부분이다.
- 시술 항목 **title**(v1 에 있음)에는 약품 · 기기 이름이 더 많다. 예: 「콧볼보톡스 하이톡스」 · 「아발란체 여성제모 (팔 하완)」. 이번 범위(description · caution)가 아니라 셈하지 않았다 → 정할 것 F-2.

## 3. 정할 것

| # | 무엇 |
|---|---|
| F-1 | 가격 세부 14 칸(공급가 · 부가세 · 면세 · 과세 · 수가 유형 id)을 v2 에 더할지 — 지금은 금액 · 이벤트가만 있다 |
| F-2 | 시술 항목 title 안의 약품 · 기기 · 부위 낱말(예: 하이톡스 · 아발란체 · 팔 하완)을 매핑 근거로 쓸지 |
| F-3 | 옵션 · 상품 description 을 상담 화면 문구(상품 설명)로 쓸지 — 「-」 를 뺀 쓸 글은 옵션 281 · 상품 90 |
| F-4 | 이 원응답을 다시 받는 주기 — 설명 칸이 병원 쪽에서 언제 바뀌는지(예: 「병원 확인 8/25」) |

## 4. 확인 안 됨

- 배합 글이 15 항목에만 있는 까닭(다른 시술 항목에는 병원 확인 글이 없는지, 아직 안 쓴 것인지).
- 시술 항목 `translsMap.caution` 이 원문 `caution` 없이 번역만 있는 까닭(1 항목).

## 부록. 칸 전수 표(A ~ F)

v1 칸의 뜻은 아래와 같다.
- ○ = v1 에 옮김
- ✗ → v2 = v2 에 더함
- – = 옮길 필요 없음(까닭을 함께 적음)
- ✗(가격 세부) = 둘 다 없음

「채움」 은 null · 빈 글 · 빈 배열을 뺀 수이고, 「-」 는 빈 표지 수다.

### A 카테고리 — 응답 16 행

| 경로 | 타입 | 채움 / 전체 | 다른 값 | 「-」 | 값 보기 | v1 |
|---|---|---|---|---|---|---|
| `.deleted` | 참거짓 | 16 / 16 | 1 |  | `False` | ○ |
| `.id` | 글 | 16 / 16 | 16 |  | (id) | ○ |
| `.name` | 글 | 16 / 16 | 16 |  | `이벤트` · `시그니처 라인` · `보톡스` | ○ |
| `.opened` | 참거짓 | 16 / 16 | 1 |  | `True` | ○ |
| `.order` | 정수 | 16 / 16 | 16 |  | `0` · `1` · `2` | ○ |
| `.translsMap.name.translation.en` | 글 | 15 / 15 | 15 |  | `Event` · `Signature Line` · `Botox` | ✗ → v2 |
| `.translsMap.name.translation.ja` | 글 | 15 / 15 | 15 |  | `イベント` · `シグネチャーライン` · `ボトックス` | ✗ → v2 |
| `.translsMap.name.translation.zh-Hans` | 글 | 15 / 15 | 15 |  | `活动` · `招牌系列` · `肉毒素` | ✗ → v2 |
| `.translsMap.name.translation.zh-Hant` | 글 | 15 / 15 | 15 |  | `活動` · `招牌系列` · `肉毒桿菌` | ✗ → v2 |

### B 상품 — 응답 150 행

| 경로 | 타입 | 채움 / 전체 | 다른 값 | 「-」 | 값 보기 | v1 |
|---|---|---|---|---|---|---|
| `.badges[]#len` | 배열 길이 | 150 / 150 | 1 |  | `0` | ✗ → v2 |
| `.categories[]#len` | 배열 길이 | 150 / 150 | 2 |  | `1` · `2` | – 길이(배열 자체로 옮김) |
| `.categories[].id` | 글 | 151 / 151 | 16 |  | (id) | ○ |
| `.categories[].name` | 글 | 151 / 151 | 16 |  | `이벤트` · `메디컬 스킨케어` · `보톡스` | – 같은 id 의 칸으로(카테고리 · 시술 목록) |
| `.categories[].translsMap.name.translation.en` | 글 | 132 / 132 | 15 |  | `Event` · `Medical Skincare` · `Botox` | – 같은 id 의 칸으로(카테고리 · 시술 목록) |
| `.categories[].translsMap.name.translation.ja` | 글 | 132 / 132 | 15 |  | `イベント` · `メディカルスキンケア` · `ボトックス` | – 같은 id 의 칸으로(카테고리 · 시술 목록) |
| `.categories[].translsMap.name.translation.zh-Hans` | 글 | 132 / 132 | 15 |  | `活动` · `医疗皮肤管理` · `肉毒素` | – 같은 id 의 칸으로(카테고리 · 시술 목록) |
| `.categories[].translsMap.name.translation.zh-Hant` | 글 | 132 / 132 | 15 |  | `活動` · `醫療皮膚管理` · `肉毒桿菌` | – 같은 id 의 칸으로(카테고리 · 시술 목록) |
| `.caution` | 글 | 0 / 150 | 0 |  |  | ✗ → v2 |
| `.cautions[]` | 글 | 0 / 85 | 0 |  |  | ✗ → v2 |
| `.cautions[]#len` | 배열 길이 | 150 / 150 | 2 |  | `1` · `0` | – 길이(배열 자체로 옮김) |
| `.closed` | 참거짓 | 150 / 150 | 2 |  | `False` · `True` | ○ |
| `.deleted` | 참거짓 | 150 / 150 | 1 |  | `False` | ○ |
| `.description` | 글 | 150 / 150 | 90 | 60 | `-` · `1년간 회원가` · `데일리 케어관리` | ✗ → v2 |
| `.displayPeriod.endDateTimeUtc` | 글 | 56 / 56 | 4 |  | `2026-10-24T15:00Z` · `2026-12-31T15:00Z` · `2026-11-30T15:00Z` | ✗ → v2 |
| `.displayPeriod.startDateTimeUtc` | 글 | 56 / 56 | 5 |  | `2026-10-23T15:00Z` · `2026-09-30T15:00Z` · `2026-09-17T15:00Z` | ✗ → v2 |
| `.id` | 글 | 150 / 150 | 150 |  | (id) | ○ |
| `.isEvent` | 참거짓 | 150 / 150 | 2 |  | `False` · `True` | ○ |
| `.medicineAndMachines[]#len` | 배열 길이 | 150 / 150 | 8 |  | `1` · `12` · `0` | – 길이(배열 자체로 옮김) |
| `.medicineAndMachines[].id` | 글 | 236 / 236 | 73 |  | (id) | ✗ → v2 |
| `.medicineAndMachines[].name` | 글 | 236 / 236 | 73 |  | `포트라` · `온다` · `소프웨이브` | ✗ → v2 |
| `.offeringPeriod.endDateTimeUtc` | 글 | 56 / 56 | 4 |  | `2026-10-24T15:00Z` · `2026-12-31T15:00Z` · `2026-11-30T15:00Z` | ✗ → v2 |
| `.offeringPeriod.startDateTimeUtc` | 글 | 56 / 56 | 6 |  | `2026-10-23T15:00Z` · `2026-09-30T15:00Z` · `2026-10-30T15:00Z` | ✗ → v2 |
| `.options[]#len` | 배열 길이 | 150 / 150 | 18 |  | `1` · `11` · `4` | – 길이(배열 자체로 옮김) |
| `.options[].badges[]#len` | 배열 길이 | 493 / 493 | 1 |  | `0` | ✗ → v2 |
| `.options[].compositions[]#len` | 배열 길이 | 493 / 493 | 5 |  | `0` · `2` · `7` | – 길이(배열 자체로 옮김) |
| `.options[].compositions[].count` | 정수 | 95 / 95 | 3 |  | `1` · `5` · `10` | ○ |
| `.options[].compositions[].medicalService.caution` | 글 | 0 / 95 | 0 |  |  | ✗ → v2 |
| `.options[].compositions[].medicalService.configuration.code` | 글 | 95 / 95 | 51 |  | `26-THM3-600SHOT` · `26-SMJ-THM3-225SHOT` · `26-ONDRP-OND-100KJ` | ○ |
| `.options[].compositions[].medicalService.configuration.healthcareReimbursement` | 글 | 95 / 95 | 1 |  | `NON_REIMBURSABLE` | ○ |
| `.options[].compositions[].medicalService.configuration.machines[]#len` | 배열 길이 | 95 / 95 | 2 |  | `1` · `0` | – 길이(배열 자체로 옮김) |
| `.options[].compositions[].medicalService.configuration.machines[].id` | 글 | 62 / 62 | 15 |  | (id) | ○ |
| `.options[].compositions[].medicalService.configuration.machines[].name` | 글 | 62 / 62 | 15 |  | `써마지FLX` · `온다` · `소프라노티타늄` | ○ |
| `.options[].compositions[].medicalService.configuration.machines[].searchPhoneticName` | 글 | 62 / 62 | 15 |  | `써마지FLX` · `온다` · `소프라노티타늄` | – 이름과 같음 |
| `.options[].compositions[].medicalService.configuration.medicines[]#len` | 배열 길이 | 95 / 95 | 2 |  | `0` · `1` | – 길이(배열 자체로 옮김) |
| `.options[].compositions[].medicalService.configuration.medicines[].id` | 글 | 29 / 29 | 16 |  | (id) | ○ |
| `.options[].compositions[].medicalService.configuration.medicines[].name` | 글 | 29 / 29 | 16 |  | `코어톡스` · `쥬비덤 스킨바이브` · `보톡스` | ○ |
| `.options[].compositions[].medicalService.configuration.medicines[].searchPhoneticName` | 글 | 29 / 29 | 16 |  | `코어톡스` · `쥬비덤 스킨바이브` · `보톡스` | – 이름과 같음 |
| `.options[].compositions[].medicalService.configuration.procedure.categoryIds[]#len` | 배열 길이 | 95 / 95 | 1 |  | `0` | – 길이(배열 자체로 옮김) |
| `.options[].compositions[].medicalService.configuration.procedure.id` | 글 | 95 / 95 | 32 |  | (id) | ○ |
| `.options[].compositions[].medicalService.configuration.procedure.name` | 글 | 95 / 95 | 32 |  | `써마지FLX` · `아이써마지` · `온다리프팅 (바디)` | – 같은 id 의 칸으로(카테고리 · 시술 목록) |
| `.options[].compositions[].medicalService.configuration.procedure.searchPhoneticName` | 글 | 95 / 95 | 32 |  | `써마지FLX` · `아이써마지` · `온다리프팅 (바디)` | – 같은 id 의 칸으로(카테고리 · 시술 목록) |
| `.options[].compositions[].medicalService.configuration.taxation` | 글 | 95 / 95 | 1 |  | `TAXABLE` | ○ |
| `.options[].compositions[].medicalService.configuration.unit.type` | 글 | 51 / 51 | 6 |  | `SHOT` · `KJ` · `CC` | ○ |
| `.options[].compositions[].medicalService.configuration.unit.value` | 실수 | 51 / 51 | 12 |  | `600.0` · `225.0` · `100.0` | ○ |
| `.options[].compositions[].medicalService.deleted` | 참거짓 | 95 / 95 | 1 |  | `False` | ✗ → v2 |
| `.options[].compositions[].medicalService.description` | 글 | 1 / 95 | 1 |  | `실제 사용 약물 구성(병원 확인, 8/25)…` | ✗ → v2 |
| `.options[].compositions[].medicalService.draftedDateTimeUtc` | 글 | 95 / 95 | 51 |  | `2026-08-27T02:48:13.968Z` · `2026-08-27T02:48:13.746Z` · `2026-08-27T02:48:15.806Z` | ✗ → v2 |
| `.options[].compositions[].medicalService.id` | 글 | 95 / 95 | 51 |  | (id) | ○ |
| `.options[].compositions[].medicalService.priceAmount.currency` | 글 | 2 / 2 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].compositions[].medicalService.priceAmount.value` | 정수 | 2 / 2 | 1 |  | 숫자 | ✗ → v2 |
| `.options[].compositions[].medicalService.status` | 글 | 95 / 95 | 1 |  | `PUBLISHED` | ○ |
| `.options[].compositions[].medicalService.title` | 글 | 95 / 95 | 45 |  | `써마지 FLX` · `아이 써마지` · `온다리프팅 바디` | ○ |
| `.options[].compositions[].medicalService.translsMap.caution.translation.en` | 글 | 1 / 1 | 1 |  | `[Additional Option] Fort…` | ✗ → v2 |
| `.options[].compositions[].medicalService.translsMap.caution.translation.ja` | 글 | 1 / 1 | 1 |  | `【追加オプション】Fortra 10KJ 追加（…` | ✗ → v2 |
| `.options[].compositions[].medicalService.translsMap.caution.translation.zh-Hans` | 글 | 1 / 1 | 1 |  | `[追加选项】Fortra 10KJ 追加（不可单…` | ✗ → v2 |
| `.options[].compositions[].medicalService.translsMap.caution.translation.zh-Hant` | 글 | 1 / 1 | 1 |  | `【追加選項】Fortra 10KJ 追加（不可單…` | ✗ → v2 |
| `.options[].compositions[].medicalService.translsMap.title.translation.en` | 글 | 74 / 74 | 33 |  | `Thermage FLX` · `Eye Thermage` · `ONDA Lifting Body` | ✗ → v2 |
| `.options[].compositions[].medicalService.translsMap.title.translation.ja` | 글 | 74 / 74 | 33 |  | `サーマクール FLX` · `アイサーマクール` · `オンダリフト BODY` | ✗ → v2 |
| `.options[].compositions[].medicalService.translsMap.title.translation.zh-Hans` | 글 | 74 / 74 | 33 |  | `美版热玛吉第五代` · `眼部美版热玛吉` · `Onda 提升 身体` | ✗ → v2 |
| `.options[].compositions[].medicalService.translsMap.title.translation.zh-Hant` | 글 | 74 / 74 | 33 |  | `鳳凰電波 FLX` · `眼部鳳凰電波` · `Onda 提升 身體` | ✗ → v2 |
| `.options[].compositions[].medicalService.updatedDateTimeUtc` | 글 | 95 / 95 | 51 |  | `2026-08-27T02:48:14Z` · `2026-08-27T02:48:13.798Z` · `2026-08-27T02:48:15.837Z` | ○ |
| `.options[].compositions[].medicineAndMachines[]#len` | 배열 길이 | 95 / 95 | 2 |  | `1` · `0` | – 길이(배열 자체로 옮김) |
| `.options[].compositions[].medicineAndMachines[].id` | 글 | 91 / 91 | 31 |  | (id) | ○ |
| `.options[].compositions[].medicineAndMachines[].name` | 글 | 91 / 91 | 31 |  | `써마지FLX` · `온다` · `소프라노티타늄` | ○ |
| `.options[].compositions[].price.additional[]#len` | 배열 길이 | 95 / 95 | 2 |  | 숫자 | – 길이(배열 자체로 옮김) |
| `.options[].compositions[].price.additional[].amount.currency` | 글 | 29 / 29 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].compositions[].price.additional[].amount.value` | 정수 | 29 / 29 | 9 |  | 숫자 | ✗ → v2 |
| `.options[].compositions[].price.additional[].suppliedAmount.currency` | 글 | 29 / 29 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].compositions[].price.additional[].suppliedAmount.value` | 정수 | 29 / 29 | 9 |  | 숫자 | ✗(가격 세부 · 정할 것) |
| `.options[].compositions[].price.additional[].taxFreeAmount.currency` | 글 | 29 / 29 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].compositions[].price.additional[].taxFreeAmount.value` | 정수 | 29 / 29 | 1 |  | 숫자 | ✗(가격 세부 · 정할 것) |
| `.options[].compositions[].price.additional[].taxation` | 글 | 29 / 29 | 1 |  | `TAXABLE` | ✗(가격 세부 · 정할 것) |
| `.options[].compositions[].price.additional[].vatAmount.currency` | 글 | 29 / 29 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].compositions[].price.additional[].vatAmount.value` | 정수 | 29 / 29 | 9 |  | 숫자 | ✗(가격 세부 · 정할 것) |
| `.options[].compositions[].price.additional[].visitorType.id` | 글 | 29 / 29 | 1 |  | (id) | ✗(가격 세부 · 정할 것) |
| `.options[].compositions[].price.additional[].visitorType.name` | 글 | 29 / 29 | 1 |  | `이벤트가` | ✗ → v2 |
| `.options[].compositions[].price.amount.currency` | 글 | 95 / 95 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].compositions[].price.amount.value` | 정수 | 95 / 95 | 57 |  | 숫자 | ○ |
| `.options[].compositions[].price.suppliedAmount.currency` | 글 | 95 / 95 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].compositions[].price.suppliedAmount.value` | 정수 | 95 / 95 | 57 |  | 숫자 | ✗(가격 세부 · 정할 것) |
| `.options[].compositions[].price.taxFreeAmount.currency` | 글 | 95 / 95 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].compositions[].price.taxFreeAmount.value` | 정수 | 95 / 95 | 1 |  | 숫자 | ✗(가격 세부 · 정할 것) |
| `.options[].compositions[].price.taxation` | 글 | 95 / 95 | 1 |  | `TAXABLE` | ✗(가격 세부 · 정할 것) |
| `.options[].compositions[].price.vatAmount.currency` | 글 | 95 / 95 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].compositions[].price.vatAmount.value` | 정수 | 95 / 95 | 57 |  | 숫자 | ✗(가격 세부 · 정할 것) |
| `.options[].compositions[].procedure.categoryIds[]#len` | 배열 길이 | 95 / 95 | 1 |  | `0` | – 길이(배열 자체로 옮김) |
| `.options[].compositions[].procedure.createDate` | 글 | 0 / 95 | 0 |  |  | – 비어 있음 |
| `.options[].compositions[].procedure.id` | 글 | 95 / 95 | 32 |  | (id) | ○ |
| `.options[].compositions[].procedure.name` | 글 | 95 / 95 | 32 |  | `써마지FLX` · `아이써마지` · `온다리프팅 (바디)` | – 같은 id 의 칸으로(카테고리 · 시술 목록) |
| `.options[].compositions[].title` | 글 | 0 / 95 | 0 |  |  | ○ |
| `.options[].compositions[].unit.type` | 글 | 95 / 95 | 7 |  | `SHOT` · `KJ` · `CC` | ○ |
| `.options[].compositions[].unit.value` | 실수 | 95 / 95 | 13 |  | `600.0` · `225.0` · `100.0` | ○ |
| `.options[].count` | 정수 | 456 / 456 | 5 |  | `1` · `2` · `5` | ○ |
| `.options[].deleted` | 참거짓 | 493 / 493 | 1 |  | `False` | ○ |
| `.options[].description` | 글 | 493 / 493 | 145 | 212 | `-` · `2회 무료` · `라라필 1회 시술` | ✗ → v2 |
| `.options[].displayChannels[]` | 글 | 808 / 808 | 3 |  | `HOMEPAGE` · `GANGNAMUNNI` · `KOS_CONNECT` | ✗ → v2 |
| `.options[].displayChannels[]#len` | 배열 길이 | 493 / 493 | 3 |  | `3` · `0` · `1` | – 길이(배열 자체로 옮김) |
| `.options[].frequentlyUsedOption` | 참거짓 | 493 / 493 | 1 |  | `False` | ✗ → v2 |
| `.options[].id` | 글 | 493 / 493 | 493 |  | (id) | ○ |
| `.options[].medicalService.caution` | 글 | 0 / 456 | 0 |  |  | ✗ → v2 |
| `.options[].medicalService.configuration.code` | 글 | 456 / 456 | 288 |  | `26-11-1` · `26-11` · `26-SPB-200PULSE` | ○ |
| `.options[].medicalService.configuration.healthcareReimbursement` | 글 | 456 / 456 | 1 |  | `NON_REIMBURSABLE` | ○ |
| `.options[].medicalService.configuration.machines[]#len` | 배열 길이 | 456 / 456 | 2 |  | `1` · `0` | – 길이(배열 자체로 옮김) |
| `.options[].medicalService.configuration.machines[].id` | 글 | 192 / 192 | 23 |  | (id) | ○ |
| `.options[].medicalService.configuration.machines[].name` | 글 | 192 / 192 | 23 |  | `포트라` · `온다` · `소프웨이브` | ○ |
| `.options[].medicalService.configuration.machines[].searchPhoneticName` | 글 | 192 / 192 | 23 |  | `포트라` · `온다` · `소프웨이브` | – 이름과 같음 |
| `.options[].medicalService.configuration.medicines[]#len` | 배열 길이 | 456 / 456 | 2 |  | `0` · `1` | – 길이(배열 자체로 옮김) |
| `.options[].medicalService.configuration.medicines[].id` | 글 | 246 / 246 | 47 |  | (id) | ○ |
| `.options[].medicalService.configuration.medicines[].name` | 글 | 246 / 246 | 47 |  | `다이어트수액` · `감초주사` · `마늘주사` | ○ |
| `.options[].medicalService.configuration.medicines[].searchPhoneticName` | 글 | 246 / 246 | 47 |  | `다이어트수액` · `감초주사` · `마늘주사` | – 이름과 같음 |
| `.options[].medicalService.configuration.procedure.categoryIds[]#len` | 배열 길이 | 456 / 456 | 1 |  | `0` | – 길이(배열 자체로 옮김) |
| `.options[].medicalService.configuration.procedure.id` | 글 | 456 / 456 | 119 |  | (id) | ○ |
| `.options[].medicalService.configuration.procedure.name` | 글 | 456 / 456 | 119 |  | `포트라` · `온다리프팅 (페이스)` · `소프웨이브` | – 같은 id 의 칸으로(카테고리 · 시술 목록) |
| `.options[].medicalService.configuration.procedure.searchPhoneticName` | 글 | 456 / 456 | 119 |  | `포트라` · `온다리프팅 (페이스)` · `소프웨이브` | – 같은 id 의 칸으로(카테고리 · 시술 목록) |
| `.options[].medicalService.configuration.taxation` | 글 | 456 / 456 | 1 |  | `TAXABLE` | ○ |
| `.options[].medicalService.configuration.unit.type` | 글 | 222 / 222 | 9 |  | `PULSE` · `SHOT` · `CC` | ○ |
| `.options[].medicalService.configuration.unit.value` | 실수 | 222 / 222 | 28 |  | `200.0` · `600.0` · `2.5` | ○ |
| `.options[].medicalService.deleted` | 참거짓 | 456 / 456 | 1 |  | `False` | ✗ → v2 |
| `.options[].medicalService.description` | 글 | 43 / 456 | 1 |  | `실제 사용 약물 구성(병원 확인, 8/25)…` | ✗ → v2 |
| `.options[].medicalService.draftedDateTimeUtc` | 글 | 456 / 456 | 288 |  | `2026-11-17T06:15:39.148Z` · `2026-11-17T06:14:23.757Z` · `2026-08-27T02:48:12.324Z` | ✗ → v2 |
| `.options[].medicalService.id` | 글 | 456 / 456 | 288 |  | (id) | ○ |
| `.options[].medicalService.priceAmount.currency` | 글 | 2 / 2 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].medicalService.priceAmount.value` | 정수 | 2 / 2 | 1 |  | 숫자 | ✗ → v2 |
| `.options[].medicalService.status` | 글 | 456 / 456 | 1 |  | `PUBLISHED` | ○ |
| `.options[].medicalService.title` | 글 | 456 / 456 | 268 |  | `포트라 60KJ` · `온다리프팅 얼굴 60KJ` · `소프웨이브` | ○ |
| `.options[].medicalService.translsMap.caution.translation.en` | 글 | 1 / 1 | 1 |  | `[Additional Option] Fort…` | ✗ → v2 |
| `.options[].medicalService.translsMap.caution.translation.ja` | 글 | 1 / 1 | 1 |  | `【追加オプション】Fortra 10KJ 追加（…` | ✗ → v2 |
| `.options[].medicalService.translsMap.caution.translation.zh-Hans` | 글 | 1 / 1 | 1 |  | `[追加选项】Fortra 10KJ 追加（不可单…` | ✗ → v2 |
| `.options[].medicalService.translsMap.caution.translation.zh-Hant` | 글 | 1 / 1 | 1 |  | `【追加選項】Fortra 10KJ 追加（不可單…` | ✗ → v2 |
| `.options[].medicalService.translsMap.title.translation.en` | 글 | 335 / 335 | 188 |  | `Sofwave` · `Thermage FLX` · `Ultherapy PRIME` | ✗ → v2 |
| `.options[].medicalService.translsMap.title.translation.ja` | 글 | 335 / 335 | 188 |  | `ソフウェーブ` · `サーマクール FLX` · `ウルセラピープライム` | ✗ → v2 |
| `.options[].medicalService.translsMap.title.translation.zh-Hans` | 글 | 335 / 335 | 188 |  | `索夫波` · `美版热玛吉第五代` · `美版超声刀二代` | ✗ → v2 |
| `.options[].medicalService.translsMap.title.translation.zh-Hant` | 글 | 335 / 335 | 188 |  | `索夫波` · `鳳凰電波 FLX` · `美版音波二代` | ✗ → v2 |
| `.options[].medicalService.updatedDateTimeUtc` | 글 | 456 / 456 | 302 |  | `2026-11-17T06:15:39.206Z` · `2026-11-17T06:14:23.798Z` · `2026-08-27T02:48:12.362Z` | ○ |
| `.options[].medicineAndMachines[]#len` | 배열 길이 | 493 / 493 | 2 |  | `1` · `0` | – 길이(배열 자체로 옮김) |
| `.options[].medicineAndMachines[].id` | 글 | 438 / 438 | 70 |  | (id) | ✗ → v2 |
| `.options[].medicineAndMachines[].name` | 글 | 438 / 438 | 70 |  | `포트라` · `온다` · `소프웨이브` | ✗ → v2 |
| `.options[].price.additional[]#len` | 배열 길이 | 493 / 493 | 2 |  | 숫자 | – 길이(배열 자체로 옮김) |
| `.options[].price.additional[].amount.currency` | 글 | 67 / 67 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].price.additional[].amount.value` | 정수 | 67 / 67 | 36 |  | 숫자 | ○ |
| `.options[].price.additional[].suppliedAmount.currency` | 글 | 67 / 67 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].price.additional[].suppliedAmount.value` | 정수 | 67 / 67 | 41 |  | 숫자 | ✗(가격 세부 · 정할 것) |
| `.options[].price.additional[].taxFreeAmount.currency` | 글 | 67 / 67 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].price.additional[].taxFreeAmount.value` | 정수 | 67 / 67 | 1 |  | 숫자 | ✗(가격 세부 · 정할 것) |
| `.options[].price.additional[].taxation` | 글 | 67 / 67 | 1 |  | `TAXABLE` | ✗(가격 세부 · 정할 것) |
| `.options[].price.additional[].vatAmount.currency` | 글 | 67 / 67 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].price.additional[].vatAmount.value` | 정수 | 67 / 67 | 41 |  | 숫자 | ✗(가격 세부 · 정할 것) |
| `.options[].price.additional[].visitorType.id` | 글 | 67 / 67 | 1 |  | (id) | ✗(가격 세부 · 정할 것) |
| `.options[].price.additional[].visitorType.name` | 글 | 67 / 67 | 1 |  | `이벤트가` | ○ |
| `.options[].price.amount.currency` | 글 | 493 / 493 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].price.amount.value` | 정수 | 493 / 493 | 98 |  | 숫자 | ○ |
| `.options[].price.suppliedAmount.currency` | 글 | 493 / 493 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].price.suppliedAmount.value` | 정수 | 493 / 493 | 146 |  | 숫자 | ○ |
| `.options[].price.taxFreeAmount.currency` | 글 | 493 / 493 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].price.taxFreeAmount.value` | 정수 | 493 / 493 | 1 |  | 숫자 | ○ |
| `.options[].price.taxation` | 글 | 493 / 493 | 1 |  | `TAXABLE` | ○ |
| `.options[].price.vatAmount.currency` | 글 | 493 / 493 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.options[].price.vatAmount.value` | 정수 | 493 / 493 | 146 |  | 숫자 | ○ |
| `.options[].procedure.categoryIds[]#len` | 배열 길이 | 456 / 456 | 1 |  | `0` | – 길이(배열 자체로 옮김) |
| `.options[].procedure.createDate` | 글 | 0 / 456 | 0 |  |  | – 비어 있음 |
| `.options[].procedure.id` | 글 | 456 / 456 | 119 |  | (id) | ✗ → v2 |
| `.options[].procedure.name` | 글 | 456 / 456 | 119 |  | `포트라` · `온다리프팅 (페이스)` · `소프웨이브` | – 같은 id 의 칸으로(카테고리 · 시술 목록) |
| `.options[].promotionConfigurations[]#len` | 배열 길이 | 493 / 493 | 1 |  | `0` | ✗ → v2 |
| `.options[].title` | 글 | 493 / 493 | 491 |  | `[DB 블랙 1년권] 포트라 60KJ` · `[DB 블랙 1년권] 온다 60KJ` · `[DB 블랙 1년권] 소프웨이브 200샷` | ○ |
| `.options[].translsMap.description.translation.en` | 글 | 237 / 237 | 108 | 1 | `-` · `A topical anesthetic tha…` · `Anesthetic injected dire…` | ✗ → v2 |
| `.options[].translsMap.description.translation.ja` | 글 | 237 / 237 | 107 | 1 | `-` · `肌表面の感覚を一時的に鈍らせる局所麻酔剤` · `施術部位に麻酔薬を直接注入し、痛みを一時的に遮断` | ✗ → v2 |
| `.options[].translsMap.description.translation.zh-Hans` | 글 | 237 / 237 | 107 | 1 | `-` · `暂时钝化皮肤表面感觉的局部麻醉剂` · `在施术部位直接注射麻醉药,暂时阻断疼痛` | ✗ → v2 |
| `.options[].translsMap.description.translation.zh-Hant` | 글 | 237 / 237 | 107 | 1 | `-` · `暫時鈍化皮膚表面感覺的區域性麻醉劑` · `在施術部位直接注射麻醉藥,暫時阻斷疼痛` | ✗ → v2 |
| `.options[].translsMap.title.translation.en` | 글 | 310 / 310 | 301 |  | `Ion Vitamin Whitening Ca…` · `Cryo Soothing Care 1 Ses…` · `Cryo Soothing Care 5 Ses…` | ✗ → v2 |
| `.options[].translsMap.title.translation.ja` | 글 | 310 / 310 | 301 |  | `イオンビタミン美白管理 1回` · `クライオ鎮静管理 1回` · `クライオ鎮静管理 5回` | ✗ → v2 |
| `.options[].translsMap.title.translation.zh-Hans` | 글 | 310 / 310 | 301 |  | `离子维生素C美白护理 1次` · `Cryo 冷冻镇静护理 1次` · `Cryo 冷冻镇静护理 5次` | ✗ → v2 |
| `.options[].translsMap.title.translation.zh-Hant` | 글 | 310 / 310 | 301 |  | `IONZYME 離子美白管理 1次` · `Cryo 冷凍鎮靜護理 1次` · `Cryo 冷凍鎮靜護理 5次` | ✗ → v2 |
| `.options[].type` | 글 | 493 / 493 | 2 |  | `SINGLE` · `GROUP` | ○ |
| `.order` | 정수 | 150 / 150 | 1 |  | `1` | ○ |
| `.targetCountryCodes[]` | 글 | 298 / 298 | 2 |  | `KR` · `ETC` | ✗ → v2 |
| `.targetCountryCodes[]#len` | 배열 길이 | 150 / 150 | 2 |  | `2` · `1` | – 길이(배열 자체로 옮김) |
| `.title` | 글 | 150 / 150 | 150 |  | `[DB 블랙 1년권] 포트라 60KJ` · `[DB 블랙 1년권] 온다 60KJ` · `[DB 블랙 1년권] 소프웨이브 200샷` | ○ |
| `.translsMap.description.translation.en` | 글 | 76 / 76 | 74 | 1 | `Delivers highly concentr…` · `Rapid cooling and soothi…` · ` -` | ✗ → v2 |
| `.translsMap.description.translation.ja` | 글 | 75 / 75 | 73 | 1 | `高濃縮イオン化ビタミンCを肌の深層へ浸透` · `施術後の急速クーリング鎮静ケア。赤みの鎮静/むく…` · ` -` | ✗ → v2 |
| `.translsMap.description.translation.zh-Hans` | 글 | 75 / 75 | 73 | 1 | `将高浓缩离子化维生素C渗透至皮肤深层` · `施术后快速冷却镇静护理。对红肿镇静/浮肿管理效果…` · ` -` | ✗ → v2 |
| `.translsMap.description.translation.zh-Hant` | 글 | 75 / 75 | 73 | 1 | `將高濃縮離子化維生素C滲透至皮膚深層` · `施術後快速冷卻鎮靜護理。對紅腫鎮靜/浮腫管理效果…` · ` -` | ✗ → v2 |
| `.translsMap.title.translation.en` | 글 | 102 / 102 | 99 |  | `Ion Vitamin Whitening Ca…` · `Cryo` · `[November Event]Lara Pee…` | ✗ → v2 |
| `.translsMap.title.translation.ja` | 글 | 101 / 101 | 98 |  | `イオンビタミン美白管理` · `クライオ` · `[11月限定キャンペーン]ララピール/パンプキン…` | ✗ → v2 |
| `.translsMap.title.translation.zh-Hans` | 글 | 101 / 101 | 98 |  | `离子维生素C美白护理` · `Cryo` · `【11月限定活动】拉拉焕肤/南瓜换肤/白金焕肤 …` | ✗ → v2 |
| `.translsMap.title.translation.zh-Hant` | 글 | 100 / 100 | 97 |  | `IONZYME 離子美白管理` · `Cryo` · `【11月限定優惠】拉拉煥膚/南瓜煥膚/白金煥膚 …` | ✗ → v2 |

### C 시술 — 응답 827 행

| 경로 | 타입 | 채움 / 전체 | 다른 값 | 「-」 | 값 보기 | v1 |
|---|---|---|---|---|---|---|
| `.categoryIds[]#len` | 배열 길이 | 827 / 827 | 1 |  | `0` | ✗ → v2 |
| `.createDate` | 글 | 827 / 827 | 827 |  | `2026-08-27T02:44:32.577Z` · `2026-08-27T02:44:32.623Z` · `2026-08-27T02:44:32.661Z` | ✗ → v2 |
| `.deleted` | 참거짓 | 827 / 827 | 1 |  | `False` | ○ |
| `.id` | 글 | 827 / 827 | 827 |  | (id) | ○ |
| `.name` | 글 | 827 / 827 | 827 |  | `슈링크유니버스더마` · `울핏` · `아이울쎄라` | ○ |
| `.searchPhoneticName` | 글 | 827 / 827 | 827 |  | `슈링크유니버스더마` · `울핏` · `아이울쎄라` | ✗ → v2 |

### D 시술 외 품목 — 응답 14 행

| 경로 | 타입 | 채움 / 전체 | 다른 값 | 「-」 | 값 보기 | v1 |
|---|---|---|---|---|---|---|
| `.category.category` | 글 | 14 / 14 | 1 |  | `ETCETRA_PRODUCT_CATEGORY` | ✗ → v2 |
| `.category.closed` | 참거짓 | 14 / 14 | 1 |  | `False` | ○ |
| `.category.default` | 참거짓 | 14 / 14 | 1 |  | `False` | ✗ → v2 |
| `.category.id` | 글 | 14 / 14 | 3 |  | (id) | ○ |
| `.category.name` | 글 | 14 / 14 | 3 |  | `화장품` · `약 처방` · `문서 발급` | ○ |
| `.category.order` | 정수 | 14 / 14 | 3 |  | `2` · `0` · `3` | ○ |
| `.id` | 글 | 14 / 14 | 14 |  | (id) | ○ |
| `.price.currency` | 글 | 14 / 14 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.price.value` | 정수 | 14 / 14 | 10 |  | 숫자 | ○ |
| `.title` | 글 | 14 / 14 | 14 |  | `PP크림` · `울쎄라팩 1장` · `울쎄라팩 1박스 (4장)` | ○ |

### E 선불카드(closed false) — 응답 8 행

| 경로 | 타입 | 채움 / 전체 | 다른 값 | 「-」 | 값 보기 | v1 |
|---|---|---|---|---|---|---|
| `.balance.currency` | 글 | 8 / 8 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.balance.value` | 정수 | 8 / 8 | 8 |  | 숫자 | ○ |
| `.closed` | 참거짓 | 8 / 8 | 1 |  | `False` | ○ |
| `.description` | 글 | 8 / 8 | 4 |  | `3인 사용` · `본인만 사용 가능` · `2인 사용` | ○ |
| `.expirationDurationInDays` | 정수 | 8 / 8 | 1 |  | `365` | ○ |
| `.id` | 글 | 8 / 8 | 8 |  | (id) | ○ |
| `.order` | 정수 | 8 / 8 | 8 |  | `7` · `5` · `4` | ○ |
| `.point.currency` | 글 | 8 / 8 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.point.value` | 정수 | 8 / 8 | 8 |  | 숫자 | ○ |
| `.price.currency` | 글 | 8 / 8 | 1 |  | `KRW` | – 값 하나(KRW) |
| `.price.value` | 정수 | 8 / 8 | 8 |  | 숫자 | ○ |
| `.title` | 글 | 8 / 8 | 8 |  | `VIP 플랜2` · `프리미엄 플랜` · `S플랜 멤버십4` | ○ |
| `.translsMap.title.translation.en` | 글 | 8 / 8 | 8 |  | `VIP Plan 2` · `Premium Plan` · `S Plan Membership 4` | ✗ → v2 |
| `.translsMap.title.translation.ja` | 글 | 8 / 8 | 8 |  | `VIPプラン2` · `プレミアムプラン` · `Sプラン メンバーシップ4` | ✗ → v2 |
| `.translsMap.title.translation.zh-Hans` | 글 | 8 / 8 | 8 |  | `VIP方案2` · `高级方案` · `S方案会员4` | ✗ → v2 |
| `.translsMap.title.translation.zh-Hant` | 글 | 8 / 8 | 8 |  | `VIP方案2` · `高級方案` · `S方案會員4` | ✗ → v2 |

### E 선불카드(closed true) — 응답 0 행

행 0 — 칸 없음.


### F 기타 작업 — 응답 4 행

| 경로 | 타입 | 채움 / 전체 | 다른 값 | 「-」 | 값 보기 | v1 |
|---|---|---|---|---|---|---|
| `.deleted` | 참거짓 | 4 / 4 | 1 |  | `False` | ○ |
| `.id` | 글 | 4 / 4 | 4 |  | (id) | ○ |
| `.title` | 글 | 4 / 4 | 4 |  | `방 점유/원장 상담` · `마취` · `시트팩` | ○ |
