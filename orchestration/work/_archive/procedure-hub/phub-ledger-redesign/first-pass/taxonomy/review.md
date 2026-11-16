# taxonomy.json — 1차 조사 (읽기용 목차)

## 상태

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/taxonomy.json` · sha256 `5492d0d4354406477206cb46f1bb735ca684d2d4a218c11d31e7889b20f4e8fe` · 660679 bytes
- 구획 53개 중 직접 읽기 완료 53개 (구획별 상태는 아래 목차와 `coverage.json`)
- 상세 상태·미결: [`validation.md`](validation.md) · [`issues.md`](issues.md) · 진행: [`progress.md`](progress.md)
- 이 문서와 review-part 는 원문 값(원본 컬럼명 그대로)과 잠정 관찰을 다른 칸·절로 분리한다. 관찰은 의미 확정이 아니다.

| 항목 | 값 |
|---|---|
| 1차 범위 종료 | 예 — 전 구획 직접 읽기·구조/값·형태소/표현 수집·기계 검증·읽기 검토 완료(근거 `validation.md`) |
| 원장 전체 완료 | **아니오** — 원문 부족(B)·원문 내 불일치(I)·후속 의미 조사(F)·알려진 분석 한계(K)가 남아 있다(`issues.md`) |
| 원문 노드 | 17593 (말단·빈 컨테이너 11931) |
| 구조 | modality 17 · subcategories 74 · items 523 · products 59 · problem 14 · problem subcategories 53 · problem items 117 |
| 형태소 | 적용 10844 · 제외 985(사유 기록) · 토큰 98254 · 필드명 57 · 알려진 오분절 표시 2023 |
| 표현 | 정규식 후보 10974 · 직접 읽기 수집 1073 |
| 사용자 결정 필요(C) | 0 — 원본 변경 후보는 후속 확인 후보(F/I)로 기록, 지금 선택 요청 없음 |

- *batch-03 검토 후 기록 보완:* 「표현」 정규식 후보는 패턴에 든 단서만 잡는다. `자제`·`깊`·`권장`·`… 시` 같은 단서는 표현 기록에 빠진 출현이 있다. 표현 목록만 보고 탐색하지 말고 원문 문맥을 다시 읽어야 한다(`issues.md` K-EXPR01, 열림). M16 `/modality/15/products` 빈 배열은 뜻 미상 관찰로 `issues.md` OBS-M16-PRODUCTS 에 적었다. 이 줄은 `build.py` 생성물이 아니어서 rebuild 하면 사라진다.

## 컬럼 구성 표

경로 패턴의 `*` 는 배열 인덱스. 출현 수는 원문 노드 수. 「선택적」은 같은 부모 패턴 출현 수보다 적게 나오는 필드. 예시는 첫 출현 원문 값과 Pointer.

| 원본 컬럼명/경로 패턴 | 자료형 | 중첩 구조 | 출현 수 | 선택적 | 빈 값 출현 | 원문 예시 | 예시 Pointer |
|---|---|---|---|---|---|---|---|
| `(루트)` | object 1 | object{modality, problem} | 1 |  | 0 | (객체) | `(루트)` |
| `/modality` | array 1 | array[17] | 1 |  | 0 | (배열) | `/modality` |
| `/modality/*` | object 17 | object{id, category, category_en, group, subcategories, extracted, products, name} | 17 |  | 0 | (객체) | `/modality/0` |
| `/modality/*/id` | string 17 | 말단 | 17 |  | 0 | M1 | `/modality/0/id` |
| `/modality/*/category` | string 17 | 말단 | 17 |  | 0 | 보톡스 | `/modality/0/category` |
| `/modality/*/category_en` | string 17 | 말단 | 17 |  | 0 | Botulinum Toxin | `/modality/0/category_en` |
| `/modality/*/group` | string 17 | 말단 | 17 |  | 0 | 주사/주입 | `/modality/0/group` |
| `/modality/*/subcategories` | array 17 | array[3] | 17 |  | 0 | (배열) | `/modality/0/subcategories` |
| `/modality/*/subcategories/*` | object 74 | object{id, label, items} | 74 |  | 0 | (객체) | `/modality/0/subcategories/0` |
| `/modality/*/subcategories/*/id` | string 74 | 말단 | 74 |  | 0 | M1-2 | `/modality/0/subcategories/0/id` |
| `/modality/*/subcategories/*/label` | string 74 | 말단 | 74 |  | 0 | 수입 | `/modality/0/subcategories/0/label` |
| `/modality/*/subcategories/*/items` | array 74 | array[4] | 74 |  | 2 (예: `/modality/14/subcategories/14/items`) | (배열) | `/modality/0/subcategories/0/items` |
| `/modality/*/subcategories/*/items/*` | object 523 | object{id, name, detail, extracted} | 523 |  | 0 | (객체) | `/modality/0/subcategories/0/items/0` |
| `/modality/*/subcategories/*/items/*/id` | string 523 | 말단 | 523 |  | 0 | M1-2-1 | `/modality/0/subcategories/0/items/0/id` |
| `/modality/*/subcategories/*/items/*/name` | string 523 | 말단 | 523 |  | 0 | 보톡스(엘러간) | `/modality/0/subcategories/0/items/0/name` |
| `/modality/*/subcategories/*/items/*/detail` | string 523 | 말단 | 523 |  | 22 (예: `/modality/2/subcategories/2/items/0/detail`) | 오리지널 · 900kDa 복합체 | `/modality/0/subcategories/0/items/0/detail` |
| `/modality/*/subcategories/*/items/*/extracted` | object 523 | object{overview, mechanism, indications, safety, onset_duration, aftercare} | 523 |  | 2 (예: `/modality/7/subcategories/5/items/13/extracted`) | (객체) | `/modality/0/subcategories/0/items/0/extracted` |
| `/modality/*/subcategories/*/items/*/extracted/overview` | string 521 | 말단 | 521 | 예 (521/523) | 0 | 오리지널 보톡스, 900kDa 복합체 제형 | `/modality/0/subcategories/0/items/0/extracted/overview` |
| `/modality/*/subcategories/*/items/*/extracted/mechanism` | string 521 | 말단 | 521 | 예 (521/523) | 0 | 신경 말단에서 SNARE 복합체(SNAP-25)를 절단하여 아세틸콜린 분비를 차단, 근육 수축을 억제한다. 900kDa 복합체 형태로 보조단백질…(전체는 해당 Pointer) | `/modality/0/subcategories/0/items/0/extracted/mechanism` |
| `/modality/*/subcategories/*/items/*/extracted/indications` | object 521 | object{primary, extended} | 521 | 예 (521/523) | 0 | (객체) | `/modality/0/subcategories/0/items/0/extracted/indications` |
| `/modality/*/subcategories/*/items/*/extracted/indications/primary` | array 521 | array[4] | 521 |  | 0 | (배열) | `/modality/0/subcategories/0/items/0/extracted/indications/primary` |
| `/modality/*/subcategories/*/items/*/extracted/indications/primary/*` | string 1656 | 말단 | 1656 |  | 0 | 미간주름 | `/modality/0/subcategories/0/items/0/extracted/indications/primary/0` |
| `/modality/*/subcategories/*/items/*/extracted/indications/extended` | array 4 | array[2] | 4 | 예 (4/521) | 0 | (배열) | `/modality/0/subcategories/0/items/0/extracted/indications/extended` |
| `/modality/*/subcategories/*/items/*/extracted/indications/extended/*` | string 10 | 말단 | 10 |  | 0 | 눈썹 올리기 | `/modality/0/subcategories/0/items/0/extracted/indications/extended/0` |
| `/modality/*/subcategories/*/items/*/extracted/safety` | object 521 | object{common, serious} | 521 | 예 (521/523) | 0 | (객체) | `/modality/0/subcategories/0/items/0/extracted/safety` |
| `/modality/*/subcategories/*/items/*/extracted/safety/common` | array 521 | array[4] | 521 |  | 0 | (배열) | `/modality/0/subcategories/0/items/0/extracted/safety/common` |
| `/modality/*/subcategories/*/items/*/extracted/safety/common/*` | string 1278 | 말단 | 1278 |  | 0 | 주입부위 부종 | `/modality/0/subcategories/0/items/0/extracted/safety/common/0` |
| `/modality/*/subcategories/*/items/*/extracted/safety/serious` | array 187 | array[2] | 187 | 예 (187/521) | 0 | (배열) | `/modality/0/subcategories/0/items/0/extracted/safety/serious` |
| `/modality/*/subcategories/*/items/*/extracted/safety/serious/*` | string 422 | 말단 | 422 |  | 0 | 안검하수(눈꺼풀 처짐) | `/modality/0/subcategories/0/items/0/extracted/safety/serious/0` |
| `/modality/*/subcategories/*/items/*/extracted/onset_duration` | object 521 | object{onset, duration} | 521 | 예 (521/523) | 0 | (객체) | `/modality/0/subcategories/0/items/0/extracted/onset_duration` |
| `/modality/*/subcategories/*/items/*/extracted/onset_duration/onset` | string 520 | 말단 | 520 | 예 (520/521) | 0 | 3-7일 이내 효과 시작, 2-4주 점진적 개선, 1개월 완전 효과 | `/modality/0/subcategories/0/items/0/extracted/onset_duration/onset` |
| `/modality/*/subcategories/*/items/*/extracted/onset_duration/duration` | string 521 | 말단 | 521 |  | 0 | 3-4개월 | `/modality/0/subcategories/0/items/0/extracted/onset_duration/duration` |
| `/modality/*/subcategories/*/items/*/extracted/aftercare` | array 521 | array[4] | 521 | 예 (521/523) | 0 | (배열) | `/modality/0/subcategories/0/items/0/extracted/aftercare` |
| `/modality/*/subcategories/*/items/*/extracted/aftercare/*` | string 1914 | 말단 | 1914 |  | 0 | 시술 후 2-3일 간 과도한 운동 피하기 | `/modality/0/subcategories/0/items/0/extracted/aftercare/0` |
| `/modality/*/subcategories/*/items/*/extracted/safety/note` | string 4 | 말단 | 4 | 예 (4/521) | 0 | 반복 시술 시 교근 섬유화 위험 약 1.5% | `/modality/0/subcategories/0/items/1/extracted/safety/note` |
| `/modality/*/subcategories/*/items/*/extracted/onset_duration/peak` | string 7 | 말단 | 7 | 예 (7/521) | 0 | 1개월 | `/modality/0/subcategories/0/items/1/extracted/onset_duration/peak` |
| `/modality/*/subcategories/*/items/*/extracted/onset_duration/peak_effect` | string 8 | 말단 | 8 | 예 (8/521) | 0 | 1개월 완전 효과 발현 | `/modality/0/subcategories/1/items/2/extracted/onset_duration/peak_effect` |
| `/modality/*/subcategories/*/items/*/extracted/indications/secondary` | array 9 | array[3] | 9 | 예 (9/521) | 0 | (배열) | `/modality/0/subcategories/1/items/3/extracted/indications/secondary` |
| `/modality/*/subcategories/*/items/*/extracted/indications/secondary/*` | string 18 | 말단 | 18 |  | 0 | 팔자주름 | `/modality/0/subcategories/1/items/3/extracted/indications/secondary/0` |
| `/modality/*/subcategories/*/items/*/extracted/safety/common_adverse_effects` | array 2 | array[3] | 2 | 예 (2/521) | 0 | (배열) | `/modality/0/subcategories/1/items/3/extracted/safety/common_adverse_effects` |
| `/modality/*/subcategories/*/items/*/extracted/safety/common_adverse_effects/*` | string 6 | 말단 | 6 |  | 0 | 주입 부위 부종 | `/modality/0/subcategories/1/items/3/extracted/safety/common_adverse_effects/0` |
| `/modality/*/subcategories/*/items/*/extracted/safety/serious_adverse_effects` | array 2 | array[3] | 2 | 예 (2/521) | 0 | (배열) | `/modality/0/subcategories/1/items/3/extracted/safety/serious_adverse_effects` |
| `/modality/*/subcategories/*/items/*/extracted/safety/serious_adverse_effects/*` | string 6 | 말단 | 6 |  | 0 | 근력 약화 | `/modality/0/subcategories/1/items/3/extracted/safety/serious_adverse_effects/0` |
| `/modality/*/subcategories/*/items/*/extracted/safety/contraindications` | array 4 | array[3] | 4 | 예 (4/521) | 0 | (배열) | `/modality/0/subcategories/1/items/7/extracted/safety/contraindications` |
| `/modality/*/subcategories/*/items/*/extracted/safety/contraindications/*` | string 11 | 말단 | 11 |  | 0 | 임신/수유 중 | `/modality/0/subcategories/1/items/7/extracted/safety/contraindications/0` |
| `/modality/*/subcategories/*/items/*/verification_needed` | string 1 | 말단 | 1 | 예 (1/523) | 0 | 식약처 허가 번호 및 임상시험 근거 확인 전까지 '신규 허가' 표현 사용 금지. 확인 전에는 임상·광고에 사용 지양 | `/modality/0/subcategories/1/items/9/verification_needed` |
| `/modality/*/subcategories/*/items/*/extracted/safety/long_term` | array 1 | array[1] | 1 | 예 (1/521) | 0 | (배열) | `/modality/0/subcategories/2/items/0/extracted/safety/long_term` |
| `/modality/*/subcategories/*/items/*/extracted/safety/long_term/*` | string 1 | 말단 | 1 |  | 0 | 반복 시술 시 1.5% 교근 섬유화 위험 | `/modality/0/subcategories/2/items/0/extracted/safety/long_term/0` |
| `/modality/*/subcategories/*/items/*/extracted/onset_duration/maintenance` | string 1 | 말단 | 1 | 예 (1/521) | 0 | 반복 시술 권장 | `/modality/0/subcategories/2/items/4/extracted/onset_duration/maintenance` |
| `/modality/*/extracted` | object 17 | object{overview, mechanism, indications, contraindications, safety, onset_duration, aftercare, related_techniques} | 17 |  | 0 | (객체) | `/modality/0/extracted` |
| `/modality/*/extracted/overview` | string 17 | 말단 | 17 |  | 0 | 보톡스는 근육을 일시적으로 쉬게 만드는 주사제다. 원래 눈 떨림이나 근육 경련 치료에 쓰였지만, 주름을 펴는 효과가 알려지면서 1990년대부터 …(전체는 해당 Pointer) | `/modality/0/extracted/overview` |
| `/modality/*/extracted/mechanism` | string 17 | 말단 | 17 |  | 0 | 보톡스는 근육에 명령을 전달하는 신경 끝부분에 작용한다. 신경이 근육에 '움직여라'는 신호(아세틸콜린)를 보내는 걸 차단해서, 근육이 힘을 못 …(전체는 해당 Pointer) | `/modality/0/extracted/mechanism` |
| `/modality/*/extracted/indications` | object 17 | object{primary, extended} | 17 |  | 0 | (객체) | `/modality/0/extracted/indications` |
| `/modality/*/extracted/indications/primary` | array 17 | array[4] | 17 |  | 0 | (배열) | `/modality/0/extracted/indications/primary` |
| `/modality/*/extracted/indications/primary/*` | string 56 | 말단 | 56 |  | 0 | 미간주름 (눈썹 사이 찡그리면 생기는 세로 주름) | `/modality/0/extracted/indications/primary/0` |
| `/modality/*/extracted/indications/extended` | array 17 | array[19] | 17 |  | 0 | (배열) | `/modality/0/extracted/indications/extended` |
| `/modality/*/extracted/indications/extended/*` | string 100 | 말단 | 100 |  | 0 | 눈썹 올리기 | `/modality/0/extracted/indications/extended/0` |
| `/modality/*/extracted/contraindications` | object 17 | object{absolute, relative} | 17 |  | 0 | (객체) | `/modality/0/extracted/contraindications` |
| `/modality/*/extracted/contraindications/absolute` | array 17 | array[4] | 17 |  | 0 | (배열) | `/modality/0/extracted/contraindications/absolute` |
| `/modality/*/extracted/contraindications/absolute/*` | string 53 | 말단 | 53 |  | 0 | 보톡스 성분(알부민)에 알레르기가 있는 경우 | `/modality/0/extracted/contraindications/absolute/0` |
| `/modality/*/extracted/contraindications/relative` | array 17 | array[2] | 17 |  | 0 | (배열) | `/modality/0/extracted/contraindications/relative` |
| `/modality/*/extracted/contraindications/relative/*` | string 55 | 말단 | 55 |  | 0 | 임신 중이거나 수유 중일 때는 미루는 게 좋음 | `/modality/0/extracted/contraindications/relative/0` |
| `/modality/*/extracted/safety` | object 17 | object{common, uncommon, serious} | 17 |  | 0 | (객체) | `/modality/0/extracted/safety` |
| `/modality/*/extracted/safety/common` | array 17 | array[7] | 17 |  | 0 | (배열) | `/modality/0/extracted/safety/common` |
| `/modality/*/extracted/safety/common/*` | string 59 | 말단 | 59 |  | 0 | 주사 부위 통증 | `/modality/0/extracted/safety/common/0` |
| `/modality/*/extracted/safety/uncommon` | array 17 | array[4] | 17 |  | 0 | (배열) | `/modality/0/extracted/safety/uncommon` |
| `/modality/*/extracted/safety/uncommon/*` | string 45 | 말단 | 45 |  | 0 | 표정이 어색해지는 느낌 (마스크 쓴 것 같은 얼굴) | `/modality/0/extracted/safety/uncommon/0` |
| `/modality/*/extracted/safety/serious` | array 15 | array[2] | 15 | 예 (15/17) | 0 | (배열) | `/modality/0/extracted/safety/serious` |
| `/modality/*/extracted/safety/serious/*` | string 37 | 말단 | 37 |  | 0 | 드물게 메스꺼움, 피로감, 감기 비슷한 증상 (20년간 치명적 부작용 보고 없음) | `/modality/0/extracted/safety/serious/0` |
| `/modality/*/extracted/onset_duration` | object 17 | object{onset, peak, duration} | 17 |  | 0 | (객체) | `/modality/0/extracted/onset_duration` |
| `/modality/*/extracted/onset_duration/onset` | string 17 | 말단 | 17 |  | 0 | 시술 후 12시간~4일 사이에 효과가 나타나기 시작 | `/modality/0/extracted/onset_duration/onset` |
| `/modality/*/extracted/onset_duration/peak` | string 17 | 말단 | 17 |  | 0 | 약 1주일 후 원하는 만큼 효과 도달 | `/modality/0/extracted/onset_duration/peak` |
| `/modality/*/extracted/onset_duration/duration` | string 17 | 말단 | 17 |  | 0 | 3~6개월 유지 (사람마다 다름) | `/modality/0/extracted/onset_duration/duration` |
| `/modality/*/extracted/aftercare` | array 17 | array[2] | 17 |  | 0 | (배열) | `/modality/0/extracted/aftercare` |
| `/modality/*/extracted/aftercare/*` | string 53 | 말단 | 53 |  | 0 | 주사 직후 시술 부위를 강하게 누르거나 문지르지 않기 (확산 방지 목적, 자세 제한의 독립 효과는 RCT에서 확인되지 않음) | `/modality/0/extracted/aftercare/0` |
| `/modality/*/extracted/related_techniques` | array 17 | array[2] | 17 |  | 0 | (배열) | `/modality/0/extracted/related_techniques` |
| `/modality/*/extracted/related_techniques/*` | string 51 | 말단 | 51 |  | 0 | 메조보톡스 (더모톡신) — 피부 탄력 개선, 리프팅 효과 | `/modality/0/extracted/related_techniques/0` |
| `/modality/*/products` | array 17 | array[11] | 17 |  | 7 (예: `/modality/5/products`) | (배열) | `/modality/0/products` |
| `/modality/*/products/*` | object 59 | object{id, name, name_en, manufacturer, country, mfds, extracted} | 59 |  | 0 | (객체) | `/modality/0/products/0` |
| `/modality/*/products/*/id` | string 59 | 말단 | 59 |  | 0 | M1-P-0 | `/modality/0/products/0/id` |
| `/modality/*/products/*/name` | string 59 | 말단 | 59 |  | 0 | 보톡스 | `/modality/0/products/0/name` |
| `/modality/*/products/*/name_en` | string 59 | 말단 | 59 |  | 0 | Botox | `/modality/0/products/0/name_en` |
| `/modality/*/products/*/manufacturer` | string 59 | 말단 | 59 |  | 0 | 앨러간/애브비 | `/modality/0/products/0/manufacturer` |
| `/modality/*/products/*/country` | string 59 | 말단 | 59 |  | 0 | US | `/modality/0/products/0/country` |
| `/modality/*/products/*/mfds` | boolean 42, null 17 | 말단 | 59 |  | 0 | true | `/modality/0/products/0/mfds` |
| `/modality/*/products/*/extracted` | object 59 | object{overview, mechanism, indications, safety, onset_duration, aftercare} | 59 |  | 0 | (객체) | `/modality/0/products/0/extracted` |
| `/modality/*/products/*/extracted/overview` | string 59 | 말단 | 59 |  | 0 | Clostridium botulinum Type A 신경독소를 정제한 근육이완제로, 표정주름 및 과다발한 개선을 위한 미용시술 제품입니다. | `/modality/0/products/0/extracted/overview` |
| `/modality/*/products/*/extracted/mechanism` | string 59 | 말단 | 59 |  | 0 | SNARE 복합체(SNAP-25)를 절단하여 신경근접합부에서 아세틸콜린의 분비를 차단합니다. 900kDa 복합체 형태로 공급되며, 활성 성분인 …(전체는 해당 Pointer) | `/modality/0/products/0/extracted/mechanism` |
| `/modality/*/products/*/extracted/indications` | object 59 | object{primary} | 59 |  | 0 | (객체) | `/modality/0/products/0/extracted/indications` |
| `/modality/*/products/*/extracted/indications/primary` | array 59 | array[4] | 59 |  | 0 | (배열) | `/modality/0/products/0/extracted/indications/primary` |
| `/modality/*/products/*/extracted/indications/primary/*` | string 256 | 말단 | 256 |  | 0 | 표정주름(미간, 이마, 눈가) | `/modality/0/products/0/extracted/indications/primary/0` |
| `/modality/*/products/*/extracted/safety` | object 59 | object{common, note} | 59 |  | 0 | (객체) | `/modality/0/products/0/extracted/safety` |
| `/modality/*/products/*/extracted/safety/common` | array 59 | array[4] | 59 |  | 0 | (배열) | `/modality/0/products/0/extracted/safety/common` |
| `/modality/*/products/*/extracted/safety/common/*` | string 222 | 말단 | 222 |  | 0 | 주입 부위 통증, 부종, 멍 | `/modality/0/products/0/extracted/safety/common/0` |
| `/modality/*/products/*/extracted/safety/note` | string 1 | 말단 | 1 | 예 (1/59) | 0 | 반복 시술 시 1.5% 교근 섬유화 가능 | `/modality/0/products/0/extracted/safety/note` |
| `/modality/*/products/*/extracted/onset_duration` | object 59 | object{onset, duration} | 59 |  | 0 | (객체) | `/modality/0/products/0/extracted/onset_duration` |
| `/modality/*/products/*/extracted/onset_duration/onset` | string 59 | 말단 | 59 |  | 0 | 2-3일부터 효과 시작 | `/modality/0/products/0/extracted/onset_duration/onset` |
| `/modality/*/products/*/extracted/onset_duration/duration` | string 59 | 말단 | 59 |  | 0 | 1개월 완전 효과, 3-4개월 지속 | `/modality/0/products/0/extracted/onset_duration/duration` |
| `/modality/*/products/*/extracted/aftercare` | array 59 | array[5] | 59 |  | 0 | (배열) | `/modality/0/products/0/extracted/aftercare` |
| `/modality/*/products/*/extracted/aftercare/*` | string 238 | 말단 | 238 |  | 0 | 시술 직후 시술 부위 압박·문지름 자제 (자세 제한의 확산 방지 효과는 근거 제한적) | `/modality/0/products/0/extracted/aftercare/0` |
| `/modality/*/products/*/extracted/onset_duration/peak_effect` | string 5 | 말단 | 5 | 예 (5/59) | 0 | 1개월 완전 효과 | `/modality/0/products/2/extracted/onset_duration/peak_effect` |
| `/modality/*/products/*/extracted/onset_duration/diffusion` | string 1 | 말단 | 1 | 예 (1/59) | 0 | 1U당 1.5-3cm 확산 | `/modality/0/products/5/extracted/onset_duration/diffusion` |
| `/modality/*/products/*/note` | string 5 | 말단 | 5 | 예 (5/59) | 0 | 중국 수출명 | `/modality/0/products/10/note` |
| `/modality/*/name` | string 17 | 말단 | 17 |  | 0 | 보톡스 | `/modality/0/name` |
| `/modality/*/products/*/extracted/indications/secondary` | array 7 | array[2] | 7 | 예 (7/59) | 0 | (배열) | `/modality/1/products/0/extracted/indications/secondary` |
| `/modality/*/products/*/extracted/indications/secondary/*` | string 14 | 말단 | 14 |  | 0 | 혼합층 주입 | `/modality/1/products/0/extracted/indications/secondary/0` |
| `/modality/*/products/*/extracted/safety/serious` | array 31 | array[2] | 31 | 예 (31/59) | 0 | (배열) | `/modality/1/products/0/extracted/safety/serious` |
| `/modality/*/products/*/extracted/safety/serious/*` | string 62 | 말단 | 62 |  | 0 | 실명(미간 38.8%, 코 25.5%) | `/modality/1/products/0/extracted/safety/serious/0` |
| `/modality/*/subcategories/*/description` | string 3 | 말단 | 3 | 예 (3/74) | 0 | 무세포동종진피(hADM, human Acellular Dermal Matrix) 기반 ECM 스킨부스터. 인체 진피 조직에서 세포를 제거하고 E…(전체는 해당 Pointer) | `/modality/2/subcategories/5/description` |
| `/modality/*/products/*/ingredient` | string 9 | 말단 | 9 | 예 (9/59) | 0 | PCL | `/modality/2/products/0/ingredient` |
| `/modality/*/subcategories/*/items/*/classification_issue` | string 2 | 말단 | 2 | 예 (2/523) | 0 | 이 엔트리는 M4(스킨부스터) 섹션에 잘못 등재됨 — 볼뉴머는 클래시스(Classys)의 6.78MHz 모노폴라 RF 리프팅 장비이며, 주사제가…(전체는 해당 Pointer) | `/modality/3/subcategories/1/items/8/classification_issue` |
| `/modality/*/subcategories/*/items/*/is_marketing_name` | boolean 6 | 말단 | 6 | 예 (6/523) | 0 | true | `/modality/3/subcategories/1/items/13/is_marketing_name` |
| `/modality/*/subcategories/*/items/*/ingredient_basis` | string 6 | 말단 | 6 | 예 (6/523) | 0 | 히알루론산(비가교 또는 저분자 HA) + 비타민(C/B 계열) 혼합. 제품·클리닉별 배합 상이 | `/modality/3/subcategories/1/items/13/ingredient_basis` |
| `/modality/*/subcategories/*/items/*/canonical_category` | string 6 | 말단 | 6 | 예 (6/523) | 0 | M4 스킨부스터 > 비가교 HA 메조테라피 | `/modality/3/subcategories/1/items/13/canonical_category` |
| `/modality/*/subcategories/*/items/*/naming_caveat` | string 6 | 말단 | 6 | 예 (6/523) | 0 | '꿀광'은 효과 묘사용 마케팅명으로 표준화된 단일 제제가 아님. 실제 사용 성분·농도는 클리닉별로 상이하므로 상담 시 실제 성분과 허가 제품명 …(전체는 해당 Pointer) | `/modality/3/subcategories/1/items/13/naming_caveat` |
| `/modality/*/products/*/type` | string 24 | 말단 | 24 | 예 (24/59) | 0 | PRP키트 | `/modality/4/products/0/type` |
| `/modality/*/products/*/material` | string 5 | 말단 | 5 | 예 (5/59) | 0 | PDO | `/modality/6/products/0/material` |
| `/modality/*/products/*/extracted/safety/common_side_effects` | array 1 | array[4] | 1 | 예 (1/59) | 0 | (배열) | `/modality/6/products/1/extracted/safety/common_side_effects` |
| `/modality/*/products/*/extracted/safety/common_side_effects/*` | string 4 | 말단 | 4 |  | 0 | 부종 | `/modality/6/products/1/extracted/safety/common_side_effects/0` |
| `/modality/*/products/*/extracted/safety/contraindications` | array 1 | array[1] | 1 | 예 (1/59) | 0 | (배열) | `/modality/6/products/2/extracted/safety/contraindications` |
| `/modality/*/products/*/extracted/safety/contraindications/*` | string 1 | 말단 | 1 |  | 0 | PDO+비가교HA 병합 금기(24-72시간 내 시술 금지) | `/modality/6/products/2/extracted/safety/contraindications/0` |
| `/modality/*/subcategories/*/items/*/correction_note` | string 1 | 말단 | 1 | 예 (1/523) | 0 | 이전 데이터에 '808nm 다이오드 제모 레이저'로 잘못 기재돼 있었음. 실제 사양은 클래시스 공식 제품 페이지(https://classys.c…(전체는 해당 Pointer) | `/modality/7/subcategories/4/items/11/correction_note` |
| `/modality/*/subcategories/*/items/*/reclassified_to` | string 1 | 말단 | 1 | 예 (1/523) | 0 | M8 | `/modality/8/subcategories/1/items/4/reclassified_to` |
| `/problem` | array 1 | array[14] | 1 |  | 0 | (배열) | `/problem` |
| `/problem/*` | object 14 | object{id, category, category_en, subcategories} | 14 |  | 0 | (객체) | `/problem/0` |
| `/problem/*/id` | string 14 | 말단 | 14 |  | 0 | P1 | `/problem/0/id` |
| `/problem/*/category` | string 14 | 말단 | 14 |  | 0 | 쁘띠시술 | `/problem/0/category` |
| `/problem/*/category_en` | string 14 | 말단 | 14 |  | 0 | Petit Procedure | `/problem/0/category_en` |
| `/problem/*/subcategories` | array 14 | array[7] | 14 |  | 0 | (배열) | `/problem/0/subcategories` |
| `/problem/*/subcategories/*` | object 53 | object{id, label, items} | 53 |  | 0 | (객체) | `/problem/0/subcategories/0` |
| `/problem/*/subcategories/*/id` | string 53 | 말단 | 53 |  | 0 | P1-1 | `/problem/0/subcategories/0/id` |
| `/problem/*/subcategories/*/label` | string 53 | 말단 | 53 |  | 0 | 코 | `/problem/0/subcategories/0/label` |
| `/problem/*/subcategories/*/items` | array 53 | array[2] | 53 |  | 0 | (배열) | `/problem/0/subcategories/0/items` |
| `/problem/*/subcategories/*/items/*` | object 117 | object{id, name, detail, modality_ref} | 117 |  | 0 | (객체) | `/problem/0/subcategories/0/items/0` |
| `/problem/*/subcategories/*/items/*/id` | string 117 | 말단 | 117 |  | 0 | auto-63-1774737181584 | `/problem/0/subcategories/0/items/0/id` |
| `/problem/*/subcategories/*/items/*/name` | string 117 | 말단 | 117 |  | 0 | 코필러 | `/problem/0/subcategories/0/items/0/name` |
| `/problem/*/subcategories/*/items/*/detail` | string 117 | 말단 | 117 |  | 0 | 콧대/코끝 | `/problem/0/subcategories/0/items/0/detail` |
| `/problem/*/subcategories/*/items/*/modality_ref` | array 117 | array[1] | 117 |  | 26 (예: `/problem/0/subcategories/6/items/0/modality_ref`) | (배열) | `/problem/0/subcategories/0/items/0/modality_ref` |
| `/problem/*/subcategories/*/items/*/modality_ref/*` | string 105 | 말단 | 105 |  | 0 | M2 | `/problem/0/subcategories/0/items/0/modality_ref/0` |

## 구획 목차

| 구획 | 범위 | 단위 | 소유 노드 | 읽기 상태 | 값 문서 |
|---|---|---|---|---|---|
| S000 | 루트 컨테이너 | root | 3 | read | [review-part-S000.md](review-part-S000.md) |
| S001 | M1 보톡스 | id … M1-1 items/7 (17단위) | 406 | read | [review-part-S001.md](review-part-S001.md) |
| S002 | M1 보톡스 | M1-1 items/8 … M1-3 items/6 (13단위) | 349 | read | [review-part-S002.md](review-part-S002.md) |
| S003 | M1 보톡스 | M1-3 items/7 … M1-P-3 (12단위) | 393 | read | [review-part-S003.md](review-part-S003.md) |
| S004 | M1 보톡스 | M1-P-4 … name (8단위) | 232 | read | [review-part-S004.md](review-part-S004.md) |
| S005 | M2 필러 | id … M2-1 items/14 (20단위) | 406 | read | [review-part-S005.md](review-part-S005.md) |
| S006 | M2 필러 | M2-1 items/15 … M2-3 items/1 (14단위) | 379 | read | [review-part-S006.md](review-part-S006.md) |
| S007 | M2 필러 | extracted … name (11단위) | 313 | read | [review-part-S007.md](review-part-S007.md) |
| S008 | M3 바이오스티뮬레이터/콜라겐부스터 | id … M3-3 items/2 (19단위) | 391 | read | [review-part-S008.md](review-part-S008.md) |
| S009 | M3 바이오스티뮬레이터/콜라겐부스터 | M3-3 items/3 … products 컨테이너 (12단위) | 327 | read | [review-part-S009.md](review-part-S009.md) |
| S010 | M3 바이오스티뮬레이터/콜라겐부스터 | M3-P-0 … name (7단위) | 190 | read | [review-part-S010.md](review-part-S010.md) |
| S011 | M4 스킨부스터 | id … M4-2 items/6 (20단위) | 416 | read | [review-part-S011.md](review-part-S011.md) |
| S012 | M4 스킨부스터 | M4-2 items/7 … auto-new-M4-1775360442 items/0 (15단위) | 374 | read | [review-part-S012.md](review-part-S012.md) |
| S013 | M4 스킨부스터 | auto-new-M4-1775360442 items/1 … name (13단위) | 335 | read | [review-part-S013.md](review-part-S013.md) |
| S014 | M5 PRP/자가혈 | id … name (18단위) | 381 | read | [review-part-S014.md](review-part-S014.md) |
| S015 | M6 지방이식 | id … name (11단위) | 165 | read | [review-part-S015.md](review-part-S015.md) |
| S016 | M7 실리프팅 | id … M7-3 items/2 (17단위) | 381 | read | [review-part-S016.md](review-part-S016.md) |
| S017 | M7 실리프팅 | M7-3 items/3 … M7-3 items/15 (13단위) | 313 | read | [review-part-S017.md](review-part-S017.md) |
| S018 | M7 실리프팅 | M7-3 items/16 … M7-P-2 (13단위) | 356 | read | [review-part-S018.md](review-part-S018.md) |
| S019 | M7 실리프팅 | M7-P-3, M7-P-4, name | 71 | read | [review-part-S019.md](review-part-S019.md) |
| S020 | M8 레이저 | id … M8-1 items/11 (17단위) | 340 | read | [review-part-S020.md](review-part-S020.md) |
| S021 | M8 레이저 | M8-1 items/12 … M8-2 items/7 (13단위) | 367 | read | [review-part-S021.md](review-part-S021.md) |
| S022 | M8 레이저 | M8-2 items/8 … M8-4 items/2 (11단위) | 359 | read | [review-part-S022.md](review-part-S022.md) |
| S023 | M8 레이저 | M8-4 items/3 … M8-5 items/5 (13단위) | 385 | read | [review-part-S023.md](review-part-S023.md) |
| S024 | M8 레이저 | M8-5 items/6 … M8-6 items/7 (15단위) | 370 | read | [review-part-S024.md](review-part-S024.md) |
| S025 | M8 레이저 | M8-6 items/8 … M8-P-2 (15단위) | 376 | read | [review-part-S025.md](review-part-S025.md) |
| S026 | M8 레이저 | M8-P-3, M8-P-4, M8-P-5, name | 100 | read | [review-part-S026.md](review-part-S026.md) |
| S027 | M9 기기 리프팅 | id … M9-1 items/11 (17단위) | 353 | read | [review-part-S027.md](review-part-S027.md) |
| S028 | M9 기기 리프팅 | M9-1 items/12 … M9-2 items/8 (13단위) | 365 | read | [review-part-S028.md](review-part-S028.md) |
| S029 | M9 기기 리프팅 | M9-2 items/9 … M9-4 items/3 (14단위) | 346 | read | [review-part-S029.md](review-part-S029.md) |
| S030 | M9 기기 리프팅 | M9-4 items/4 … M9-P-5 (13단위) | 386 | read | [review-part-S030.md](review-part-S030.md) |
| S031 | M9 기기 리프팅 | M9-P-6, name | 34 | read | [review-part-S031.md](review-part-S031.md) |
| S032 | M10 HIFES/EMS | id … name (18단위) | 307 | read | [review-part-S032.md](review-part-S032.md) |
| S033 | M11 니들RF | id … M11-1 items/12 (18단위) | 355 | read | [review-part-S033.md](review-part-S033.md) |
| S034 | M11 니들RF | extracted … name (7단위) | 177 | read | [review-part-S034.md](review-part-S034.md) |
| S035 | M12 마이크로니들링(MTS) | id … name (15단위) | 263 | read | [review-part-S035.md](review-part-S035.md) |
| S036 | M13 플라즈마 | id … name (12단위) | 150 | read | [review-part-S036.md](review-part-S036.md) |
| S037 | M14 크라이오리포라이시스 | id … name (13단위) | 179 | read | [review-part-S037.md](review-part-S037.md) |
| S038 | M15 메디컬스킨케어 | id … M15-1 items/18 (24단위) | 478 | read | [review-part-S038.md](review-part-S038.md) |
| S039 | M15 메디컬스킨케어 | M15-1 items/19 … M15-1 items/36 (18단위) | 422 | read | [review-part-S039.md](review-part-S039.md) |
| S040 | M15 메디컬스킨케어 | M15-1 items/37 … M15-1 items/55 (19단위) | 414 | read | [review-part-S040.md](review-part-S040.md) |
| S041 | M15 메디컬스킨케어 | M15-1 items/56 … M15-3 items/5 (19단위) | 440 | read | [review-part-S041.md](review-part-S041.md) |
| S042 | M15 메디컬스킨케어 | M15-3 items/6 … auto-M15-1775360912 items/1 (18단위) | 458 | read | [review-part-S042.md](review-part-S042.md) |
| S043 | M15 메디컬스킨케어 | auto-M15-1775360998 items/0 … auto-1775361777 items/10 (19단위) | 472 | read | [review-part-S043.md](review-part-S043.md) |
| S044 | M15 메디컬스킨케어 | auto-1775361777 items/11 … auto-1775402620 items/2 (19단위) | 445 | read | [review-part-S044.md](review-part-S044.md) |
| S045 | M15 메디컬스킨케어 | auto-1775402620 items/3 … name (10단위) | 206 | read | [review-part-S045.md](review-part-S045.md) |
| S046 | M16 수액치료 | id … M16-3 items/2 (23단위) | 458 | read | [review-part-S046.md](review-part-S046.md) |
| S047 | M16 수액치료 | M16-3 items/3 … M16-DCA items/5 (17단위) | 417 | read | [review-part-S047.md](review-part-S047.md) |
| S048 | M16 수액치료 | M16-DCA items/6 … M16-new-1774325959851 items/2 (17단위) | 411 | read | [review-part-S048.md](review-part-S048.md) |
| S049 | M16 수액치료 | M16-new-1774325959851 items/3 … name (14단위) | 291 | read | [review-part-S049.md](review-part-S049.md) |
| S050 | M17 줄기세포치료 | id … name (17단위) | 316 | read | [review-part-S050.md](review-part-S050.md) |
| S051 | problem | id … subcategories 컨테이너 (117단위) | 644 | read | [review-part-S051.md](review-part-S051.md) |
| S052 | problem | P10-1 items/0 … P14-4 items/1 (56단위) | 328 | read | [review-part-S052.md](review-part-S052.md) |

