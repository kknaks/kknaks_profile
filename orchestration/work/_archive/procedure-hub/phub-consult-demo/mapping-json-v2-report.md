# 매핑 JSON v2 — 진료항목 + 옵션(가격) + 케이스 매핑 + 부위 좌표 (data 워커 · 2026-11-20)

발주 `task_71115a6b667e` · `ctx_17e6b6cf14d4`(사용자 승인 11-20). 커밋 0 · silver · gold · 허브 레포 · DB · 앱 코드 수정 0 · 사용자 포트 0.

## 1. 결과 한 줄

- 새 스크립트 `reference/2026-11-19-myeongdong-kos/build_mapping_json_v2.py` 로 **`myeongdong-mapping-20261120.json`** 을 만들었다.
  - 같은 두 경로에 같은 바이트로 두었고, 둘 다 `.gitignore:8 data/` 로 무시된다.
  - 옛 `-20261119.json` 과 옛 `build_mapping_json.py` 는 그대로 뒀다.
- items **324** — v1 칸은 옛 JSON 과 324 항목 모두 같다(status · note 만 뜻이 바뀜). 옵션 있음 **300** · 없음 **24** · 옵션 줄 551 · 지운 옵션 0.
- sites **71** = face 32(기존 좌표 26 · 새로 6) · body 39.
- sha256 **da2d0e805abd2394156c5758dc15ae1917a63f908f87948fd69540f806dc91cd**(두 경로 같음) · meta 해시 = gold 57b420ad… · aux 51e3760a…(지금 silver · gold 값).

## 2. 코디 셈과 다른 점 — 옵션 288 / 36 → 300 / 24

- KOS 옵션은 두 꼴이다.
  - **single**(456 개 · `treatment_item_kos_id` 로 진료항목 하나)
  - **group**(37 개 · 묶음 상품 · `treatment_item_kos_id` 없음 · `compositions[]` 에 진료항목 여럿)
- single 만 세면 288 / 36 이고, group 구성까지 넣으면 **300 / 24** 다.
  - 12 진료항목은 group 옵션으로만 팔린다(§6 목록).
  - v5 `상품 옵션 연결 수` 칸은 single + group 셈이다. JSON `options` 길이와 324 항목 모두 같다.
- group 옵션은 구성 진료항목마다 붙였다(같은 옵션이 여러 항목에 나옴).
  - `link: "group"` 과 `compositions[]`(item_code · count · unit · price · additional_prices — 원본 값 · KOS id 대신 진료항목 코드)를 같이 뒀다.
  - **group 의 price_amount 는 묶음 전체 가격**이다. 장바구니 최저가 셈에서 single 과 섞지 않아야 한다.

## 3. 발주 칸 밖으로 더한 칸(원본 그대로)

| 칸 | 왜 |
|---|---|
| `options[].additional_prices` | KOS 옵션의 `이벤트가`(예: 정가 670000 · 이벤트가 350000) — 최저가 추천에 필요. 원본 리스트 그대로 |
| `options[].product_closed` | `closed` 는 옵션 칸(전부 null) · 상품 쪽 `closed` 가 실제 값(상품 150 중 1 true) |
| `options[].link` · `compositions` | §2 |
| `sites{}.parent_code` · `source` | 부위 계층 · 좌표 출처(`face_coords` / `새로 · 워커 초안` / body 빈칸) |
| `meta.version` · `viewbox` · `face_svg` | 좌표 기준 |

- 원본 `tax_free_amount` 는 넣지 않았다(발주 칸 밖 · 전부 0 인지 미확인).
- KOS id(24자 16진)는 JSON 에 0 개다.

## 4. 꼴 — 예시 1 항목(옵션 2 개만 잘라 보임) · 부위 2

```json
{
 "kos_item_code": "26-BBL-CLER-FACE",
 "kos_item_name": "BBL 클리어 (페이스)",
 "kos_procedure": "BBL HERO (페이스)",
 "kos_machine": "BBL HERO",
 "kos_medicine": "해당 없음",
 "kos_unit": "",
 "kos_description": "",
 "kos_option_count": 3,
 "kos_status": "PUBLISHED",
 "site_tiers": {
  "t1": "얼굴",
  "t2": "",
  "t3": ""
 },
 "site_scope": "얼굴 전체",
 "hub": {
  "procedure_codes": [
   "PRC-006"
  ],
  "case_codes": [
   "CAS-063"
  ],
  "site_codes": [
   "SITE-007"
  ],
  "products": [
   {
    "code": "PRD-323",
    "name": "BBL클리어",
    "from": "구성1"
   }
  ]
 },
 "status": "매핑됨",
 "note": "",
 "options": [
  {
   "product_title": "BBL HERO (FACE)",
   "product_is_event": false,
   "product_closed": false,
   "option_title": "BBL 클리어 (트러블) 1회",
   "type": "single",
   "count": 1,
   "price_amount": 550000,
   "supplied_amount": 550000,
   "vat_amount": 55000,
   "taxation": "TAXABLE",
   "additional_prices": [],
   "description": null,
   "closed": null,
   "display_channels": [
    "HOMEPAGE",
    "GANGNAMUNNI",
    "KOS_CONNECT"
   ],
   "link": "single"
  },
  {
   "product_title": "[BBL HERO 런칭E] [포에버영,스킨타이트,클리어 모드] 택 1 +백옥주사  1회",
   "product_is_event": true,
   "product_closed": false,
   "option_title": "BBL 클리어 + 백옥주사 1회",
   "type": "group",
   "count": null,
   "price_amount": 670000,
   "supplied_amount": 670000,
   "vat_amount": 67000,
   "taxation": "TAXABLE",
   "additional_prices": [
    {
     "visitor_type": "이벤트가",
     "amount": 350000
    }
   ],
   "description": null,
   "closed": null,
   "display_channels": [
    "HOMEPAGE",
    "GANGNAMUNNI",
    "KOS_CONNECT"
   ],
   "link": "group",
   "compositions": [
    {
     "item_code": "26-BBL-CLER-FACE",
     "count": 1,
     "unit": {
      "type": "UnitType_UNKNOWN",
      "value": 0.0
     },
     "price": 550000,
     "additional_prices": []
    },
    {
     "item_code": "26-SJS-BJS",
     "count": 1,
     "unit": {
      "type": "UnitType_UNKNOWN",
      "value": 0.0
     },
     "price": 120000,
     "additional_prices": []
    }
   ]
  }
 ]
}
```

```json
{
 "SITE-145": {
  "name": "귀밑샘",
  "parent_code": "SITE-121",
  "region": "face",
  "shape": "pair",
  "points": [
   [
    0.1831,
    0.5236
   ],
   [
    0.8169,
    0.5236
   ]
  ],
  "source": "새로 · 워커 초안"
 },
 "SITE-101": {
  "name": "팔뚝",
  "parent_code": "SITE-100",
  "region": "body",
  "shape": "list",
  "points": [],
  "source": ""
 }
}
```

## 5. status · note

| status(v5 「상태」 원문) | 수 | note(v5 확인 필요 이유 — 원문 조각) |
|---|---|---|
| 매핑됨 | 295 | 빈칸 |
| 허브 대상 아님 | 13 | v5 `시술 근거`(예 「마취 — 시술 아님」) |
| 매핑됨(제품 확인 필요) | 8 | v5 `채움 메모` 의 「구성N 확인 필요: …」 조각 |
| 시술 확인 필요 | 6 | v5 `채움 메모` 의 「시술 확인 필요: …」 조각 |
| 매핑됨(확인 필요: BBL 필터) | 2 | v5 `채움 메모` 의 「11-20 BBL 매핑: … 병원 확인」 조각 |

- 「매핑됨」 이 아닌 29 항목 모두 note 가 있다(빈 note 0).
- v1 은 status 를 둘로 접고(시술 확인 필요 / 매핑됨) note 를 고정 문구로 썼다. v2 는 원문을 그대로 쓴다.
- `kos_status` 는 KOS 진료항목 원본 `status` 다. 324 모두 `PUBLISHED` 다.
  - v5 `게시여부` 「게시됨」 은 이 값을 번역한 것이다.
  - v2 상품 파일 `treatment_items` 에는 300 개뿐이라 `raw/G_medical_services.json`(324)에서 읽었다. 300 개는 두 파일의 id · 코드가 같다(스크립트 assert).

## 6. 옵션 없는 진료항목

옵션 없음 **24**(single · group 둘 다 없음 · v5 옵션 연결 수 0):

| 진료항목 코드 | 진료항목 | status | v5 옵션 수 |
|---|---|---|---|
| 26-BBL-2MODE | BBL HERO (2가지 모드) | 매핑됨(확인 필요: BBL 필터) | 0 |
| 26-CARE-CHOOSE1 | 맞춤형 관리 케어 프로그램 (LDM 6'/SONO/오투덤 택 1) | 매핑됨 | 0 |
| 26-PRP-CANNULA | 프로디젠 PRP 양볼(케뉼라) | 매핑됨 | 0 |
| 26-PEELING-1 | 필링 1종 선택 | 매핑됨 | 0 |
| 26-DHJBT-HTS-50UNIT | 다한증보톡스 하이톡스 | 매핑됨 | 0 |
| WHITENING IV DRIP + VITAMIN IV DRIP | 프리미엄미백+비타민수액 | 허브 대상 아님 | 0 |
| 26-BDBT-HTS-100UNIT | 바디보톡스 하이톡스 | 매핑됨 | 0 |
| 26-BRJJG-CO2-1QUANTITY | 비립종 제거 2mm 이하 | 매핑됨 | 0 |
| 26---- | 수액 무제한 | 허브 대상 아님 | 0 |
| 26-SEUK-HTS-2CC | 스킨보톡스 하이톡스 | 매핑됨 | 0 |
| 26- | 엑소제 | 매핑됨 | 0 |
| 26-JTJJS-BRKR-3CC | 벨라콜린 이중턱 지방분해주사 | 매핑됨 | 0 |
| 26-Avalanche-25 | 아발란체 제모 (인중) | 매핑됨 | 0 |
| 26-JJGM-CO2-100QUANTITY | CO2 얼굴/목 전체 50개까지 | 매핑됨 | 0 |
| 26-JJGM-CO2-1QUANTITY | 점 제거 2mm 이하 | 매핑됨 | 0 |
| 26-HIBOTOX-3AREA | 국산 주름 보톡스 3부위 (하이톡스) | 매핑됨 | 0 |
| 26-CHSBT-ALLG-50UNIT | 침샘보톡스 앨러간 | 매핑됨 | 0 |
| 26-CHSBT-ZOMN-50UNIT | 침샘보톡스 제오민 | 매핑됨 | 0 |
| 26-CHSBT-COTX-50UNIT | 침샘보톡스 코어톡스 | 매핑됨 | 0 |
| 26-CHSBT-HTS-50UNIT | 침샘보톡스 하이톡스 | 매핑됨 | 0 |
| 26-Avalanche-18 | 아발란체 제모 (턱끝) | 매핑됨 | 0 |
| 26-TBT-HTS-50UNIT | 턱보톡스 하이톡스 | 매핑됨 | 0 |
| 26-Avalanche-19 | 아발란체 제모 (턱밑) | 매핑됨 | 0 |
| 26-PTNZP-JBRSK-1CC | 포텐자 펌핑팁+쥬베룩 스킨 | 매핑됨 | 0 |

group 옵션으로만 팔리는 **12**(코디 셈 「36 없음」 에서 빠지는 것):

| 진료항목 코드 | 진료항목 | 옵션 수 |
|---|---|---|
| 26-BBL-1MODE | BBL HERO (1가지 모드) | 2 |
| 26-PACK-M | 모델링팩 | 1 |
| 26-MJRFL-VLTR-1CC | 목주름필러 벨로테로 | 1 |
| 26-CERAFIT-30 | 바디 지방분해주사 | 1 |
| 26-BDFLU-SLST | 바디필러 셀레스텔라 무제한 | 2 |
| 26-SPB-50PULSE | 소프웨이브 | 3 |
| 26-SKLT-SKLT | 스컬트라 | 1 |
| 26-SKBST-RJR2-2CC | 리쥬란 HB | 1 |
| 26-SKBST-EXO-2.5CC | 엑소좀 | 2 |
| 26-JNSTN-PCLB | 제네시스토닝 | 3 |
| 26-BOTOX-3AREA | 국산 주름 보톡스 3부위 (코어톡스) | 2 |
| 26-TTNLF-SPRNT-40KJ | 티타늄리프팅 | 1 |

## 7. 부위

- 대상: items `hub.site_codes` 66 + 조상 → **71**. region 은 site 계층으로 정했다. 얼굴(SITE-007) 아래가 face, 그 밖이 body 다.
- **face 32**

  | 출처 · shape | 수 |
  |---|---|
  | face_coords · point | 10 |
  | face_coords · pair | 11 |
  | face_coords · area | 3 |
  | face_coords · line | 1 |
  | face_coords · none | 1 |
  | **새로 · pair** | 4 |
  | **새로 · area** | 2 |

  - point / pair 인데 점이 빈 것은 0 이다.
- **body 39**: shape `list` · points `[]`.
  - 전신 · 몸 · 목 · 겨드랑이 · 팔뚝 · 허벅지 안 · 밖 · 승마 · 부유방 · 브라라인 등이다.
  - **목(SITE-079)** 은 face_coords 에 점이 있지만 site 계층상 몸(SITE-147) 아래라 body 다(발주 규칙대로). 얼굴 그림에 목을 찍고 싶으면 사람 판단이 필요하다.
- 코드 → 이름은 site.csv `name_ko` 그대로다.

### 새로 찍은 좌표(워커 초안 · design-face-0.svg 윤곽 보고 · viewBox 픽셀 → 비율)

| 코드 | 이름 | shape | 왼쪽 점(px) | 자리 |
|---|---|---|---|---|
| SITE-121 | 귀 | pair | (42, 440) | 귓바퀴 위쪽(이개 089 · 이주 091 위) |
| SITE-123 | 심부볼 | pair | (178, 612) | 볼 051 아래 · 팔자 바깥 |
| SITE-145 | 귀밑샘 | pair | (108, 555) | 귓불 앞 · 아래턱 가지 위 |
| SITE-146 | 턱밑샘 | pair | (205, 800) | 턱선 아래 · 턱각 안쪽 |
| SITE-141 | 나비존 | area | — | 코 양옆 · 광대 아래 넓은 영역(라벨) |
| SITE-144 | 침샘 | area | — | 귀밑샘 + 턱밑샘을 묶는 말(라벨) |

- 오른쪽 점은 가운데 줄(x = 295)로 뒤집었다. face_coords 의 `_pair` 와 같은 식이다.
- 눈 확인은 `face-coords-preview.html` 로 한다. 빨강이 새로 찍은 점, 파랑이 기존 좌표다. 점 없는 부위 · 몸 목록은 오른쪽에 있다.

## 8. 검증

| 항목 | 결과 |
|---|---|
| items | 324 · v1 칸 옛 JSON 과 같음 324/324 |
| 옵션 가격 = 원본 | 표본 10(시드 20261120 무작위)의 price · supplied · vat · taxation · count · type · description · closed 가 원본과 같다(10/10). (상품명, 옵션명) 쌍은 원본에서 유일하다 |
| deleted 옵션 | 0(원본에도 0 · 스크립트가 거름) |
| options 길이 = v5 옵션 연결 수 | 324/324 |
| sites 에 items 부위 빠짐 | 0 |
| face point / pair 좌표 빈 것 | 0 |
| 두 경로 해시 | 같음 `da2d0e80…` |
| git 무시 | 두 경로 `.gitignore:8 data/` |
| KOS id | 0 |

## 9. 열린 것

- 새 좌표 6 — 사용자 눈 확인이 필요하다(미리보기).
- 목(SITE-079)을 face 로 둘지 정해야 한다(§7).
- group 옵션을 장바구니에서 어떻게 셀지 정해야 한다(§2). 묶음 가격 · 이벤트가(additional_prices)를 어떤 값으로 최저가를 낼지는 앱 쪽 결정이다.
- 앱 코드는 아직 이 파일을 읽지 않는다(수정 0).
  - 이름: `-20261119` → `-20261120`.
  - 바뀐 칸: `status` 값 5 종 · `options` · `sites`.

## 10. 파일

- `reference/2026-11-19-myeongdong-kos/build_mapping_json_v2.py`(새 · 옛 스크립트 그대로)
- `/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/data/kos/myeongdong-mapping-20261120.json` · `/Users/kknaks/git/clinic_chat/data/kos/myeongdong-mapping-20261120.json`
- `orchestration/work/phub-consult-demo/face-coords-preview.html` · 이 리포트

## 11. 덧붙임 — 얼굴 부위 전부 대표점(코디 · 사용자 결정 11-20)

얼굴 부위는 전부 대표점을 갖는다. area · line · none 꼴은 없앴다.

- 점 없던 7 부위에 대표점을 찍었다(design-face-0.svg 윤곽 보고 · source `대표점 · 워커 초안`). 스크립트 `REP_FACE`.
- 기존 point · pair 좌표는 그대로다(face_coords 21 · 새로 4).
- 스크립트는 얼굴 부위가 point / pair 가 아니거나 점이 비면 멈춘다.

| 코드 | 이름 | 전 shape | 대표점 | 점(px · 왼쪽) | 자리 |
|---|---|---|---|---|---|
| SITE-007 | 얼굴 | area | point | (295, 470) | 얼굴 가운데 — 비근부 041 · 코등 036 사이 |
| SITE-013 | 하안면 | area | point | (295, 715) | 코 아래 ~ 턱 가운데 — 하순 064 · 턱 072 사이 |
| SITE-088 | 머리 | area | point | (295, 112) | 정수리 084 위 · 머리 윤곽 안 |
| SITE-141 | 나비존 | area(새로) | pair | (160, 500) | 눈밑 024 ~ 광대 056 사이 |
| SITE-144 | 침샘 | area(새로) | pair | (160, 690) | 귀밑샘 145 ~ 턱밑샘 146 사이 |
| SITE-085 | 헤어라인 | line | point | (295, 200) | 이마 014 위 머리선 가운데 |
| SITE-070 | 잇몸 | none | point | (295, 660) | 입 위치 — 윗입술 062 · 입 057 사이(점이 겹쳐 보임) |

### 부위 셈

- 전체 71 = face 32 · body 39.
- face 32 는 전부 점이다.

  | 출처 | point | pair |
  |---|---|---|
  | face_coords | 10 | 11 |
  | 새로 · 워커 초안 | 0 | 4 |
  | 대표점 · 워커 초안 | 5 | 2 |

- area · line · none 은 0 이다.

### 파일 · 해시

- `face-coords-preview.html` 을 다시 만들었다. 색은 셋이다.
  - 파랑: 기존
  - 빨강: 새 부위
  - 초록: 대표점
- 오른쪽 목록은 이번에 찍은 점이다. 몸 목록은 그대로다.
- JSON 두 경로를 다시 만들었다. sha256 **8ca88c9a008b1cdb91031516132da50d64caca22b85cf8ad395c0128587d1863** 이고 두 경로가 같다(전 `da2d0e80…`).
  - items · options · status 셈은 이전과 같다(324 · 300 / 24 · 551).
  - `.gitignore data/` 무시는 그대로다.
- 눈 확인할 자리
  - 잇몸(입과 겹침)
  - 얼굴 대표점(애교살 라벨 근처)
