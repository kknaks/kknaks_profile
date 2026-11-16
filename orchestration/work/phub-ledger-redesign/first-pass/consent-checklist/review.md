# consent-checklist.json — 1차 수집 읽기용 결과

> **상태: 1차 수집 범위 종료 보고(코디 확인 전) · 원장 전체 완료 아님.** 열린 미결은 [issues.md](./issues.md), 검증은 [validation.md](./validation.md).

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/consent-checklist.json` · 21047 bytes · sha256 `4e138ffb64414995483e4201396bc4f185ec34e4d150f825ec151b0fe07512e5`
- 노드 376 (말단 306 · 컨테이너 70 · 빈 값 0) · 중복 키 0
- 형태소: Kiwi 0.24.1 cong · 적용 값 287 · 토큰 3770 → [morphology.json](./morphology.json)
- 표현 후보 929 (수동 68) → [expressions.json](./expressions.json)
- 구획·읽기 상태 → [coverage.json](./coverage.json) · 원문 위치·리터럴 구간 → [source-map.json](./source-map.json)

원문 값 칸에는 원본 문자열을 그대로 싣는다(Markdown 표 안의 `|` 만 `\|` 로 이스케이프). 잠정 관찰은 각 구획 아래 별도 표에 있으며 원문 칸과 섞지 않는다.

## 컬럼 구성

| 원본 컬럼명 / 경로 패턴 | 자료형 · 중첩 | 출현 | 원문 예시 | 예시 위치 |
|---|---|---|---|---|
| `/` | object · 키 4 (version, updated, description, categories) | 1 | — | `` (빈 Pointer = 루트) |
| `/version` | string | 1 | 1.3 | `/version` |
| `/updated` | string (날짜 모양) | 1 | 2026-07-26 | `/updated` |
| `/description` | string | 1 | 시술별 필수 고지 항목. 법적 동의서 기반 mandatory disclosure, 금기사항, 응급 징후 | `/description` |
| `/categories` | array of object · 길이 17 | 1 | — | `/categories` |
| `/categories/*` | object · 키 5 (id, name, mandatory_disclosures, contraindications, emergency_signs) · 전 항목 동일 키·순서 | 17 | — | `/categories/0` |
| `/categories/*/id` | string | 17 | M1 | `/categories/0/id` |
| `/categories/*/name` | string · `/` 포함 변형 있음 | 17 | 바이오스티뮬레이터/콜라겐부스터 | `/categories/2/name` |
| `/categories/*/mandatory_disclosures` | array of string · 길이 5~8 · 빈 배열 0 | 17 | — | `/categories/0/mandatory_disclosures` |
| `/categories/*/mandatory_disclosures/*` | string · 빈 문자열 0 | 109 | 보톡스는 영구적이 아니며 3-6개월 후 효과가 소실됩니다 | `/categories/0/mandatory_disclosures/0` |
| `/categories/*/contraindications` | array of string · 길이 5~8 · 빈 배열 0 | 17 | — | `/categories/0/contraindications` |
| `/categories/*/contraindications/*` | string · 빈 문자열 0 | 105 | 임신 및 수유 중 | `/categories/0/contraindications/0` |
| `/categories/*/emergency_signs` | array of string · 길이 2~5 · 빈 배열 0 | 17 | — | `/categories/0/emergency_signs` |
| `/categories/*/emergency_signs/*` | string · 빈 문자열 0 | 55 | 호흡 곤란 | `/categories/0/emergency_signs/0` |
| `/categories/*/{mandatory_disclosures,contraindications,emergency_signs}/*` (변형: 여러 문장) | string · 문장 여러 개(마침표+공백 경계) | 6 | 주입형 엑소좀·줄기세포 배양액(conditioned media) 제품은 국내에서 '도포용 화장품'으로만 허가… | `/categories/16/mandatory_disclosures/0` |

선택적 필드·null·숫자·불리언·빈 컨테이너·빈 문자열은 없다(source-map.json counts 와 verify 로 확인).

## 구획 목차

| 구획 | 범위 | 소유 노드 | 말단 | 읽기 상태 |
|---|---|---|---|---|
| [S00](#s00) | 루트 메타데이터 | 5 | 3 | 직접 읽음 |
| [S01](#s01) | /categories/0 M1 보톡스 | 23 | 19 | 직접 읽음 |
| [S02](#s02) | /categories/1 M2 필러 | 25 | 21 | 직접 읽음 |
| [S03](#s03) | /categories/2 M3 바이오스티뮬레이터/콜라겐부스터 | 22 | 18 | 직접 읽음 |
| [S04](#s04) | /categories/3 M4 스킨부스터 | 18 | 14 | 직접 읽음 |
| [S05](#s05) | /categories/4 M5 PRP/자가혈 | 19 | 15 | 직접 읽음 |
| [S06](#s06) | /categories/5 M6 지방이식 | 22 | 18 | 직접 읽음 |
| [S07](#s07) | /categories/6 M7 실리프팅 | 22 | 18 | 직접 읽음 |
| [S08](#s08) | /categories/7 M8 레이저 | 26 | 22 | 직접 읽음 |
| [S09](#s09) | /categories/8 M9 기기 리프팅 | 23 | 19 | 직접 읽음 |
| [S10](#s10) | /categories/9 M10 HIFES/EMS | 21 | 17 | 직접 읽음 |
| [S11](#s11) | /categories/10 M11 니들RF | 22 | 18 | 직접 읽음 |
| [S12](#s12) | /categories/11 M12 마이크로니들링(MTS) | 21 | 17 | 직접 읽음 |
| [S13](#s13) | /categories/12 M13 플라즈마 | 19 | 15 | 직접 읽음 |
| [S14](#s14) | /categories/13 M14 크라이오리포라이시스 | 23 | 19 | 직접 읽음 |
| [S15](#s15) | /categories/14 M15 메디컬스킨케어 | 23 | 19 | 직접 읽음 |
| [S16](#s16) | /categories/15 M16 수액치료 | 20 | 16 | 직접 읽음 |
| [S17](#s17) | /categories/16 M17 줄기세포치료 | 22 | 18 | 직접 읽음 |

## S00

**루트 메타데이터** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `(루트)` | `(루트)` | object · 길이 4 | — |
| `version` | `/version` | string | 1.3 |
| `updated` | `/updated` | string | 2026-07-26 |
| `description` | `/description` | string | 시술별 필수 고지 항목. 법적 동의서 기반 mandatory disclosure, 금기사항, 응급 징후 |
| `categories` | `/categories` | array · 길이 17 | — |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S00-1 | `/description` | 법적 동의서 기반 mandatory disclosure, 금기사항, 응급 징후 | description 의 세 이름이 카테고리 객체의 세 배열 키(mandatory_disclosures·contraindications·emergency_signs)와 순서상 대응해 보인다. 근거 동의서 문서 자체·출처 표기는 원장 안에 없다. | P·B |
| S00-2 | `/updated` | 2026-07-26 | 파일 단위 날짜 하나만 있다. 항목별 갱신일·출처는 없다. | B |

## S01

**/categories/0 M1 보톡스** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/0/id`, `/categories/0/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[0]` | `/categories/0` | object · 길이 5 | — |
| `id` | `/categories/0/id` | string | M1 |
| `name` | `/categories/0/name` | string | 보톡스 |
| `mandatory_disclosures` | `/categories/0/mandatory_disclosures` | array · 길이 7 | — |
| `mandatory_disclosures[0]` | `/categories/0/mandatory_disclosures/0` | string | 보톡스는 영구적이 아니며 3-6개월 후 효과가 소실됩니다 |
| `mandatory_disclosures[1]` | `/categories/0/mandatory_disclosures/1` | string | 시술 후 일시적 멍, 부종, 두통이 발생할 수 있습니다 |
| `mandatory_disclosures[2]` | `/categories/0/mandatory_disclosures/2` | string | 드물게 안검하수(눈꺼풀 처짐), 표정 비대칭이 발생할 수 있습니다 |
| `mandatory_disclosures[3]` | `/categories/0/mandatory_disclosures/3` | string | 임산부 및 수유부는 시술이 불가합니다 |
| `mandatory_disclosures[4]` | `/categories/0/mandatory_disclosures/4` | string | 반복 시술 시 항체가 형성되어 효과가 감소할 수 있습니다 |
| `mandatory_disclosures[5]` | `/categories/0/mandatory_disclosures/5` | string | 시술 후 2-3일간 과도한 운동, 사우나, 음주를 피해야 합니다 |
| `mandatory_disclosures[6]` | `/categories/0/mandatory_disclosures/6` | string | 주사 부위를 강하게 문지르면 독소가 확산되어 원치 않는 부위에 영향을 줄 수 있습니다 |
| `contraindications` | `/categories/0/contraindications` | array · 길이 6 | — |
| `contraindications[0]` | `/categories/0/contraindications/0` | string | 임신 및 수유 중 |
| `contraindications[1]` | `/categories/0/contraindications/1` | string | 신경근접합부 질환(중증근무력증 등) |
| `contraindications[2]` | `/categories/0/contraindications/2` | string | 보톡스 성분 과민반응 병력 |
| `contraindications[3]` | `/categories/0/contraindications/3` | string | 시술 부위 감염 |
| `contraindications[4]` | `/categories/0/contraindications/4` | string | 아미노글리코시드 항생제 복용 중 |
| `contraindications[5]` | `/categories/0/contraindications/5` | string | 항응고제 복용 중(출혈 위험 증가) |
| `emergency_signs` | `/categories/0/emergency_signs` | array · 길이 4 | — |
| `emergency_signs[0]` | `/categories/0/emergency_signs/0` | string | 호흡 곤란 |
| `emergency_signs[1]` | `/categories/0/emergency_signs/1` | string | 연하 곤란(삼키기 어려움) |
| `emergency_signs[2]` | `/categories/0/emergency_signs/2` | string | 심한 알레르기 반응(두드러기, 호흡곤란) |
| `emergency_signs[3]` | `/categories/0/emergency_signs/3` | string | 발음 장애 또는 시력 변화 |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S01-1 | `/categories/0/mandatory_disclosures/0` | 3-6개월 후 효과가 소실됩니다 | 시간 = 효과 소실 시점(기준 시점은 시술로 읽히나 명시는 '후'만). '-' 는 범위로 읽힌다(잠정). | P |
| S01-2 | `/categories/0/mandatory_disclosures/2` | 드물게 안검하수(눈꺼풀 처짐), 표정 비대칭이 발생할 수 있습니다 | '드물게' 가 쉼표로 나열된 두 사건 모두를 수식하는지, 앞 사건만인지 원문만으로 확정 불가. 괄호는 앞말의 풀이. | B |
| S01-3 | `/categories/0/mandatory_disclosures/5` | 시술 후 2-3일간 과도한 운동, 사우나, 음주를 피해야 합니다 | '과도한' 이 운동만 수식하는지 사우나·음주까지인지 불명. 시간=관리 기간(회피). | B |
| S01-4 | `/categories/0/mandatory_disclosures/6` | 강하게 문지르면 독소가 확산되어 원치 않는 부위에 영향을 줄 수 있습니다 | 조건(강하게 문지르면) → 결과(확산 → 영향)의 인과 연쇄. '원치 않는 부위' 는 회피 부위 성격의 부위 역할(잠정). | P |
| S01-5 | `/categories/0/contraindications/5` | 항응고제 복용 중(출혈 위험 증가) | 괄호 = 금기 사유. 상태 표현 '복용 중' 은 시점 조건. | P |
| S01-6 | `/categories/0/emergency_signs/2` | 심한 알레르기 반응(두드러기, 호흡곤란) | 괄호 = 예시 증상. 같은 구획 emergency_signs/0 '호흡 곤란' 과 띄어쓰기만 다른 '호흡곤란' 이 함께 나온다(표기 변이, 병합 판단은 후속). | F |

## S02

**/categories/1 M2 필러** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/1/id`, `/categories/1/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[1]` | `/categories/1` | object · 길이 5 | — |
| `id` | `/categories/1/id` | string | M2 |
| `name` | `/categories/1/name` | string | 필러 |
| `mandatory_disclosures` | `/categories/1/mandatory_disclosures` | array · 길이 8 | — |
| `mandatory_disclosures[0]` | `/categories/1/mandatory_disclosures/0` | string | 필러 주입 시 혈관폐색이 발생할 수 있으며, 0.04mL로도 안동맥 폐색이 가능하여 실명에 이를 수 있습니다 |
| `mandatory_disclosures[1]` | `/categories/1/mandatory_disclosures/1` | string | 혈관폐색 시 피부 괴사, 뇌졸중이 발생할 수 있습니다 |
| `mandatory_disclosures[2]` | `/categories/1/mandatory_disclosures/2` | string | HA 필러는 히알루로니다아제로 용해가 가능하지만, 비HA 필러(PMMA, CaHA 등)는 용해가 불가합니다 |
| `mandatory_disclosures[3]` | `/categories/1/mandatory_disclosures/3` | string | 필러 주입 후 결절, 육아종, 이물반응이 발생할 수 있으며 수개월~수년 후 지연성으로 나타나기도 합니다 |
| `mandatory_disclosures[4]` | `/categories/1/mandatory_disclosures/4` | string | 비대칭, 과교정, 필러 이동 가능성이 있습니다 |
| `mandatory_disclosures[5]` | `/categories/1/mandatory_disclosures/5` | string | 감염 시 농양 형성, 바이오필름이 발생할 수 있습니다 |
| `mandatory_disclosures[6]` | `/categories/1/mandatory_disclosures/6` | string | HA 필러의 지속 기간은 6-18개월이며, 개인차가 있습니다 |
| `mandatory_disclosures[7]` | `/categories/1/mandatory_disclosures/7` | string | 시술 전후 치과 시술 시 반드시 의료진에게 알려야 합니다 |
| `contraindications` | `/categories/1/contraindications` | array · 길이 6 | — |
| `contraindications[0]` | `/categories/1/contraindications/0` | string | 임신 및 수유 중 |
| `contraindications[1]` | `/categories/1/contraindications/1` | string | 시술 부위 활동성 감염 또는 염증 |
| `contraindications[2]` | `/categories/1/contraindications/2` | string | 자가면역 질환(루푸스, 류마티스 관절염 등) |
| `contraindications[3]` | `/categories/1/contraindications/3` | string | 필러 성분 과민반응 병력 |
| `contraindications[4]` | `/categories/1/contraindications/4` | string | 켈로이드 체질 |
| `contraindications[5]` | `/categories/1/contraindications/5` | string | 항응고제 복용 중(출혈/멍 위험 증가) |
| `emergency_signs` | `/categories/1/emergency_signs` | array · 길이 5 | — |
| `emergency_signs[0]` | `/categories/1/emergency_signs/0` | string | 시술 부위 급격한 백색 변화(blanching) — 혈관폐색 의심 |
| `emergency_signs[1]` | `/categories/1/emergency_signs/1` | string | 심한 통증(주입 시 통상적 수준을 초과하는 통증) |
| `emergency_signs[2]` | `/categories/1/emergency_signs/2` | string | 시력 변화 또는 시야 장애 — 안동맥 폐색 의심, 즉시 응급실 |
| `emergency_signs[3]` | `/categories/1/emergency_signs/3` | string | 피부 청색증 또는 그물반(livedo reticularis) |
| `emergency_signs[4]` | `/categories/1/emergency_signs/4` | string | 시술 부위 수일 후 점진적으로 커지는 경결/결절 |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S02-1 | `/categories/1/mandatory_disclosures/0` | 0.04mL로도 안동맥 폐색이 가능하여 실명에 이를 수 있습니다 | 수치 0.04mL 는 '로도'(양보·최소량)와 함께 폐색 가능성의 조건. 부위(안동맥)는 부작용 발생 부위 역할. 0.04mL 의 근거 출처는 없다. | P·B |
| S02-2 | `/categories/1/mandatory_disclosures/2` | HA 필러는 히알루로니다아제로 용해가 가능하지만, 비HA 필러(PMMA, CaHA 등)는 용해가 불가합니다 | 대비 구조(가능하지만/불가). 재질별로 성질이 갈림 → 재질·제품 축 필요(후속). '등' 은 열린 목록. | F |
| S02-3 | `/categories/1/mandatory_disclosures/3` | 수개월~수년 후 지연성으로 나타나기도 합니다 | 발현 시점(지연) 범위 표현. 수치 없음. '기도' 는 가능성/일부 경우. | P |
| S02-4 | `/categories/1/mandatory_disclosures/7` | 시술 전후 치과 시술 시 반드시 의료진에게 알려야 합니다 | 다른 시술(치과 시술)을 참조하는 조건. 연결 대상 확정은 후속(원장 간). | F |
| S02-5 | `/categories/1/emergency_signs/0` | 시술 부위 급격한 백색 변화(blanching) — 혈관폐색 의심 | '—' 뒤는 징후가 의심하게 하는 원인 사건. 징후↔의심 사건 관계(잠정). | P |
| S02-6 | `/categories/1/emergency_signs/2` | 즉시 응급실 | 징후에 붙은 행동 지시. 다른 응급 징후 대부분에는 행동 지시가 없다. | P |
| S02-7 | `/categories/1/contraindications/5` | 출혈/멍 위험 증가 | '/' 가 대안인지 병렬인지 README 규칙(시술명 대상)으로는 판단 불가 — 여기서는 사건 나열로 보이나 확정 아님. | F |

## S03

**/categories/2 M3 바이오스티뮬레이터/콜라겐부스터** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/2/id`, `/categories/2/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[2]` | `/categories/2` | object · 길이 5 | — |
| `id` | `/categories/2/id` | string | M3 |
| `name` | `/categories/2/name` | string | 바이오스티뮬레이터/콜라겐부스터 |
| `mandatory_disclosures` | `/categories/2/mandatory_disclosures` | array · 길이 7 | — |
| `mandatory_disclosures[0]` | `/categories/2/mandatory_disclosures/0` | string | 효과가 즉시 나타나지 않으며, 콜라겐 생성에 2-3개월이 소요됩니다 |
| `mandatory_disclosures[1]` | `/categories/2/mandatory_disclosures/1` | string | 결절(nodule), 이물반응(granuloma)이 발생할 수 있으며, 특히 입술·눈 주위 같은 얇은 피부에 주입 시 위험이 높습니다 |
| `mandatory_disclosures[2]` | `/categories/2/mandatory_disclosures/2` | string | PLLA(폴리유산, 스컬트라) 주입 시 결절 발생률은 약 5-10%입니다 |
| `mandatory_disclosures[3]` | `/categories/2/mandatory_disclosures/3` | string | CaHA(래디에스) 주입 후 영구적 결절이 드물게 보고됩니다 |
| `mandatory_disclosures[4]` | `/categories/2/mandatory_disclosures/4` | string | 정확한 희석 비율과 주입 깊이가 중요하며, 시술자 경험에 따라 결과가 달라질 수 있습니다 |
| `mandatory_disclosures[5]` | `/categories/2/mandatory_disclosures/5` | string | 보통 3-5회 반복 시술이 필요하며, 효과 지속은 1-2년입니다 |
| `mandatory_disclosures[6]` | `/categories/2/mandatory_disclosures/6` | string | 스컬트라 시술 후 부드러운 마사지는 선택 사항입니다(이른바 5-5-5 규칙의 결절 예방 효과는 임상연구에서 미입증). 결절 예방은 적절한 희석·수화·주입 깊이에 달려 있습니다. |
| `contraindications` | `/categories/2/contraindications` | array · 길이 6 | — |
| `contraindications[0]` | `/categories/2/contraindications/0` | string | 임신 및 수유 중 |
| `contraindications[1]` | `/categories/2/contraindications/1` | string | 시술 부위 활동성 감염 |
| `contraindications[2]` | `/categories/2/contraindications/2` | string | 자가면역 질환 |
| `contraindications[3]` | `/categories/2/contraindications/3` | string | 켈로이드 체질 |
| `contraindications[4]` | `/categories/2/contraindications/4` | string | 이물반응/육아종 병력 |
| `contraindications[5]` | `/categories/2/contraindications/5` | string | 입술, 눈꺼풀 등 얇은 피부 부위(PLLA) |
| `emergency_signs` | `/categories/2/emergency_signs` | array · 길이 3 | — |
| `emergency_signs[0]` | `/categories/2/emergency_signs/0` | string | 시술 부위 점점 커지는 딱딱한 결절 |
| `emergency_signs[1]` | `/categories/2/emergency_signs/1` | string | 발열과 함께 시술 부위 발적·동통(감염 의심) |
| `emergency_signs[2]` | `/categories/2/emergency_signs/2` | string | 심한 알레르기 반응(두드러기, 호흡곤란) |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S03-1 | `/categories/2/name` | 바이오스티뮬레이터/콜라겐부스터 | 카테고리 이름 자체에 '/' 가 있다. 같은 대상의 두 이름인지 두 계열인지 원문만으로 불명. | B·F |
| S03-2 | `/categories/2/mandatory_disclosures/1` | 특히 입술·눈 주위 같은 얇은 피부에 주입 시 위험이 높습니다 | '얇은' = 피부 두께(주입 깊이 아님). '·' 부위 나열. 조건(주입 시) → 위험 증가. 위험 대상 사건은 앞 절의 결절·이물반응으로 읽힌다(잠정). | P |
| S03-3 | `/categories/2/mandatory_disclosures/2` | 결절 발생률은 약 5-10%입니다 | 수치의 분모·대상 집단·출처 없음. PLLA(폴리유산, 스컬트라) 주입 시에 한정. | B |
| S03-4 | `/categories/2/mandatory_disclosures/6` | 이른바 5-5-5 규칙의 결절 예방 효과는 임상연구에서 미입증 | 근거 상태(미입증) 진술. '5-5-5 규칙' 의 내용 자체는 원문에 없다. | B |
| S03-5 | `/categories/2/mandatory_disclosures/6` | 결절 예방은 적절한 희석·수화·주입 깊이에 달려 있습니다. | 이 값만 마침표로 끝나는 두 문장 구성. '수화' 는 형태소 분석 오분절 후보(issues K 참조). | P·K |
| S03-6 | `/categories/2/contraindications/5` | 입술, 눈꺼풀 등 얇은 피부 부위(PLLA) | 괄호 PLLA 가 금기의 적용 재질 범위 한정으로 읽힌다(잠정). 부위가 '회피 부위' 역할. | P |
| S03-7 | `/categories/2/emergency_signs/1` | 발열과 함께 시술 부위 발적·동통(감염 의심) | '함께' = 동반 조건. 괄호 = 의심 원인. | P |

## S04

**/categories/3 M4 스킨부스터** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/3/id`, `/categories/3/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[3]` | `/categories/3` | object · 길이 5 | — |
| `id` | `/categories/3/id` | string | M4 |
| `name` | `/categories/3/name` | string | 스킨부스터 |
| `mandatory_disclosures` | `/categories/3/mandatory_disclosures` | array · 길이 5 | — |
| `mandatory_disclosures[0]` | `/categories/3/mandatory_disclosures/0` | string | 시술 후 일시적 멍, 부종, 발적이 발생할 수 있으며 1-7일 지속됩니다 |
| `mandatory_disclosures[1]` | `/categories/3/mandatory_disclosures/1` | string | 효과 유지를 위해 주기적인 반복 시술이 필요합니다(보통 3-4주 간격 3회) |
| `mandatory_disclosures[2]` | `/categories/3/mandatory_disclosures/2` | string | HA 기반 제품은 알레르기 반응이 드물지만 가능합니다 |
| `mandatory_disclosures[3]` | `/categories/3/mandatory_disclosures/3` | string | 시술 후 주입 부위에 일시적 작은 돌기(papule)가 보일 수 있으며 수일 내 흡수됩니다 |
| `mandatory_disclosures[4]` | `/categories/3/mandatory_disclosures/4` | string | 연어주사(PDRN) 등 해양유래 성분은 해산물 알레르기 환자에서 주의가 필요합니다 |
| `contraindications` | `/categories/3/contraindications` | array · 길이 5 | — |
| `contraindications[0]` | `/categories/3/contraindications/0` | string | 임신 및 수유 중 |
| `contraindications[1]` | `/categories/3/contraindications/1` | string | 시술 부위 감염 또는 활동성 피부질환 |
| `contraindications[2]` | `/categories/3/contraindications/2` | string | 제품 성분 과민반응 병력 |
| `contraindications[3]` | `/categories/3/contraindications/3` | string | 해산물 알레르기(PDRN/연어주사 시) |
| `contraindications[4]` | `/categories/3/contraindications/4` | string | 항응고제 복용 중(출혈 위험 증가) |
| `emergency_signs` | `/categories/3/emergency_signs` | array · 길이 2 | — |
| `emergency_signs[0]` | `/categories/3/emergency_signs/0` | string | 심한 알레르기 반응(두드러기, 호흡곤란, 안면부종) |
| `emergency_signs[1]` | `/categories/3/emergency_signs/1` | string | 시술 부위 심한 감염 징후(발열, 농, 심한 발적) |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S04-1 | `/categories/3/mandatory_disclosures/0` | 1-7일 지속됩니다 | 지속 기간이 앞의 세 사건(멍·부종·발적) 공통인지 사건별인지 불명. | B |
| S04-2 | `/categories/3/mandatory_disclosures/1` | (보통 3-4주 간격 3회) | '간격' = 반복 시술 간격, '3회' = 회차. '보통' 은 빈도/관행 수식. | P |
| S04-3 | `/categories/3/mandatory_disclosures/2` | 알레르기 반응이 드물지만 가능합니다 | 빈도(드묾)+가능성 동시 진술. 대상 = HA 기반 제품. | P |
| S04-4 | `/categories/3/mandatory_disclosures/4` | 연어주사(PDRN) 등 해양유래 성분은 해산물 알레르기 환자에서 주의가 필요합니다 | 같은 구획 contraindications/3 '해산물 알레르기(PDRN/연어주사 시)' 와 같은 대상을 고지(주의)와 금기 두 수준으로 기록. 수준 차이는 원문 그대로 보존, 통합 판단은 후속. | I·F |

## S05

**/categories/4 M5 PRP/자가혈** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/4/id`, `/categories/4/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[4]` | `/categories/4` | object · 길이 5 | — |
| `id` | `/categories/4/id` | string | M5 |
| `name` | `/categories/4/name` | string | PRP/자가혈 |
| `mandatory_disclosures` | `/categories/4/mandatory_disclosures` | array · 길이 5 | — |
| `mandatory_disclosures[0]` | `/categories/4/mandatory_disclosures/0` | string | 본인의 혈액을 채취하여 사용하므로 채혈 과정이 필요합니다 |
| `mandatory_disclosures[1]` | `/categories/4/mandatory_disclosures/1` | string | 효과가 개인차가 크며, 과학적 근거가 아직 제한적인 부분이 있습니다 |
| `mandatory_disclosures[2]` | `/categories/4/mandatory_disclosures/2` | string | 시술 후 멍, 부종이 발생할 수 있으며 1-2주 지속될 수 있습니다 |
| `mandatory_disclosures[3]` | `/categories/4/mandatory_disclosures/3` | string | 효과 발현까지 2-4주가 소요되며, 3-6회 반복 시술이 권장됩니다 |
| `mandatory_disclosures[4]` | `/categories/4/mandatory_disclosures/4` | string | 혈소판 기능에 영향을 주는 약물(아스피린, NSAIDs) 복용 시 효과가 감소할 수 있습니다 |
| `contraindications` | `/categories/4/contraindications` | array · 길이 6 | — |
| `contraindications[0]` | `/categories/4/contraindications/0` | string | 혈소판 기능 장애 또는 혈액 질환 |
| `contraindications[1]` | `/categories/4/contraindications/1` | string | 항응고제 복용 중 |
| `contraindications[2]` | `/categories/4/contraindications/2` | string | 활동성 감염 또는 패혈증 |
| `contraindications[3]` | `/categories/4/contraindications/3` | string | 암 환자 또는 혈액암 |
| `contraindications[4]` | `/categories/4/contraindications/4` | string | 임신 및 수유 중 |
| `contraindications[5]` | `/categories/4/contraindications/5` | string | NSAIDs 복용 중(채혈 전 1주일 중단 필요) |
| `emergency_signs` | `/categories/4/emergency_signs` | array · 길이 2 | — |
| `emergency_signs[0]` | `/categories/4/emergency_signs/0` | string | 채혈 부위 또는 시술 부위 심한 감염 징후(발열, 농, 심한 발적) |
| `emergency_signs[1]` | `/categories/4/emergency_signs/1` | string | 알레르기 반응(자가혈이지만 첨가제에 반응 가능) |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S05-1 | `/categories/4/mandatory_disclosures/4` | 혈소판 기능에 영향을 주는 약물(아스피린, NSAIDs) 복용 시 효과가 감소할 수 있습니다 | 같은 구획 contraindications/5 'NSAIDs 복용 중(채혈 전 1주일 중단 필요)' 과 같은 약물이 고지(효과 감소)·금기 양쪽에 나온다. | I·F |
| S05-2 | `/categories/4/contraindications/5` | 채혈 전 1주일 중단 필요 | 기준 시점 = 채혈(시술 아님). 방향 = 이전. 관리 지시가 금기 배열 안에 있다. | P |
| S05-3 | `/categories/4/contraindications/3` | 암 환자 또는 혈액암 | '또는' 나열이 상하 관계(혈액암 ⊂ 암)인지 독립 항목인지 원문 판단 불가. | F |
| S05-4 | `/categories/4/emergency_signs/1` | 알레르기 반응(자가혈이지만 첨가제에 반응 가능) | 괄호 = 원인 대상(첨가제). 첨가제 종류 원문 없음. | B |

## S06

**/categories/5 M6 지방이식** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/5/id`, `/categories/5/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[5]` | `/categories/5` | object · 길이 5 | — |
| `id` | `/categories/5/id` | string | M6 |
| `name` | `/categories/5/name` | string | 지방이식 |
| `mandatory_disclosures` | `/categories/5/mandatory_disclosures` | array · 길이 6 | — |
| `mandatory_disclosures[0]` | `/categories/5/mandatory_disclosures/0` | string | 이식된 지방의 생착률은 30-70%로 개인차가 크며, 예측이 어렵습니다 |
| `mandatory_disclosures[1]` | `/categories/5/mandatory_disclosures/1` | string | 과교정 후 흡수를 감안하여 시술하지만, 비대칭 또는 울퉁불퉁함이 발생할 수 있습니다 |
| `mandatory_disclosures[2]` | `/categories/5/mandatory_disclosures/2` | string | 채취 부위(복부, 허벅지 등)에도 멍, 부종, 통증이 발생합니다 |
| `mandatory_disclosures[3]` | `/categories/5/mandatory_disclosures/3` | string | 지방 색전증(fat embolism)은 매우 드물지만 생명을 위협할 수 있습니다 |
| `mandatory_disclosures[4]` | `/categories/5/mandatory_disclosures/4` | string | 석회화, 오일 시스트(oil cyst) 형성 가능성이 있습니다 |
| `mandatory_disclosures[5]` | `/categories/5/mandatory_disclosures/5` | string | 생착 결과 확인까지 3개월 이상 소요되며, 추가 시술이 필요할 수 있습니다 |
| `contraindications` | `/categories/5/contraindications` | array · 길이 6 | — |
| `contraindications[0]` | `/categories/5/contraindications/0` | string | 임신 및 수유 중 |
| `contraindications[1]` | `/categories/5/contraindications/1` | string | 채취할 지방이 부족한 경우 |
| `contraindications[2]` | `/categories/5/contraindications/2` | string | 혈액 응고 장애 |
| `contraindications[3]` | `/categories/5/contraindications/3` | string | 활동성 감염 |
| `contraindications[4]` | `/categories/5/contraindications/4` | string | 조절되지 않는 당뇨 |
| `contraindications[5]` | `/categories/5/contraindications/5` | string | 흡연(생착률 저하) |
| `emergency_signs` | `/categories/5/emergency_signs` | array · 길이 4 | — |
| `emergency_signs[0]` | `/categories/5/emergency_signs/0` | string | 심한 호흡곤란, 흉통(지방색전증 의심) |
| `emergency_signs[1]` | `/categories/5/emergency_signs/1` | string | 시술 부위 급격한 부종 및 심한 통증 |
| `emergency_signs[2]` | `/categories/5/emergency_signs/2` | string | 고열(38.5°C 이상)과 시술 부위 발적(감염 의심) |
| `emergency_signs[3]` | `/categories/5/emergency_signs/3` | string | 시력 변화(안면 지방이식 시 혈관 폐색 의심) |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S06-1 | `/categories/5/mandatory_disclosures/0` | 생착률은 30-70%로 개인차가 크며, 예측이 어렵습니다 | % 는 생착률(이식 지방 중 남는 비율로 읽힘) — 환자 발생률과 다른 종류의 수치. 출처 없음. | P·B |
| S06-2 | `/categories/5/mandatory_disclosures/2` | 채취 부위(복부, 허벅지 등)에도 멍, 부종, 통증이 발생합니다 | 부위 역할 = 채취 부위(시술 대상 부위와 다름). '발생합니다' 는 가능성 표지 없음(단정). | P |
| S06-3 | `/categories/5/mandatory_disclosures/3` | 매우 드물지만 생명을 위협할 수 있습니다 | 빈도(매우 드묾)와 심각도(생명 위협) 동시. | P |
| S06-4 | `/categories/5/emergency_signs/2` | 고열(38.5°C 이상) | 수치·단위·비교(이상) 이 '고열' 을 정의. 원장 내 유일한 체온 수치. | P |
| S06-5 | `/categories/5/emergency_signs/3` | 시력 변화(안면 지방이식 시 혈관 폐색 의심) | 괄호 안에 적용 조건(안면 지방이식 시)과 의심 원인이 함께 있다. | P |
| S06-6 | `/categories/5/contraindications/1` | 채취할 지방이 부족한 경우 | 질환이 아닌 시술 가능 조건이 금기 배열에 있다. | P |

## S07

**/categories/6 M7 실리프팅** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/6/id`, `/categories/6/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[6]` | `/categories/6` | object · 길이 5 | — |
| `id` | `/categories/6/id` | string | M7 |
| `name` | `/categories/6/name` | string | 실리프팅 |
| `mandatory_disclosures` | `/categories/6/mandatory_disclosures` | array · 길이 7 | — |
| `mandatory_disclosures[0]` | `/categories/6/mandatory_disclosures/0` | string | 시술 후 일시적 당김감, 부종, 멍이 발생하며 1-2주 지속됩니다 |
| `mandatory_disclosures[1]` | `/categories/6/mandatory_disclosures/1` | string | 실이 만져지거나 피부 위로 돌출(extrusion)될 수 있습니다 |
| `mandatory_disclosures[2]` | `/categories/6/mandatory_disclosures/2` | string | 비대칭이 발생할 수 있으며, 교정 시술이 필요할 수 있습니다 |
| `mandatory_disclosures[3]` | `/categories/6/mandatory_disclosures/3` | string | 감염, 실 이동, 실 주위 농양이 드물게 발생합니다 |
| `mandatory_disclosures[4]` | `/categories/6/mandatory_disclosures/4` | string | 입을 크게 벌리거나 과도한 표정 사용 시 실이 끊어지거나 이동할 수 있습니다 |
| `mandatory_disclosures[5]` | `/categories/6/mandatory_disclosures/5` | string | PDO/PLLA/PCL 등 실 재질에 따라 지속 기간이 다릅니다(6개월-2년) |
| `mandatory_disclosures[6]` | `/categories/6/mandatory_disclosures/6` | string | 시술 후 2주간 큰 입 벌림, 과도한 마사지를 피해야 합니다 |
| `contraindications` | `/categories/6/contraindications` | array · 길이 6 | — |
| `contraindications[0]` | `/categories/6/contraindications/0` | string | 임신 및 수유 중 |
| `contraindications[1]` | `/categories/6/contraindications/1` | string | 시술 부위 활동성 감염 |
| `contraindications[2]` | `/categories/6/contraindications/2` | string | 자가면역 질환 |
| `contraindications[3]` | `/categories/6/contraindications/3` | string | 켈로이드 체질 |
| `contraindications[4]` | `/categories/6/contraindications/4` | string | 항응고제 복용 중 |
| `contraindications[5]` | `/categories/6/contraindications/5` | string | 이전 실리프팅 실이 남아있는 경우(확인 필요) |
| `emergency_signs` | `/categories/6/emergency_signs` | array · 길이 3 | — |
| `emergency_signs[0]` | `/categories/6/emergency_signs/0` | string | 시술 부위 급성 감염 징후(고열, 농, 심한 발적/동통) |
| `emergency_signs[1]` | `/categories/6/emergency_signs/1` | string | 실이 피부 밖으로 돌출 |
| `emergency_signs[2]` | `/categories/6/emergency_signs/2` | string | 안면 비대칭이 점점 심해지는 경우 |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S07-1 | `/categories/6/mandatory_disclosures/0` | 일시적 당김감, 부종, 멍이 발생하며 1-2주 지속됩니다 | '일시적' 이 세 사건 모두 수식하는지 불명. 단정형 '발생하며'. | B |
| S07-2 | `/categories/6/mandatory_disclosures/5` | PDO/PLLA/PCL 등 실 재질에 따라 지속 기간이 다릅니다(6개월-2년) | 재질별 기간 값이 아니라 전체 범위 하나만 있다. 재질↔기간 대응 원문 없음. | B |
| S07-3 | `/categories/6/mandatory_disclosures/4` | 입을 크게 벌리거나 과도한 표정 사용 시 실이 끊어지거나 이동할 수 있습니다 | 조건 두 개(거나) → 결과 두 개(거나). | P |
| S07-4 | `/categories/6/contraindications/5` | 이전 실리프팅 실이 남아있는 경우(확인 필요) | 이전 시술 이력 조건. '확인 필요' 는 절대 금기가 아닌 확인 대상으로 읽힐 수 있다(잠정). | P |
| S07-5 | `/categories/6/emergency_signs/2` | 안면 비대칭이 점점 심해지는 경우 | 진행(점점)이 응급 판단 조건. 같은 구획 mandatory_disclosures/2 비대칭(고지)과 수준 구분. | P |

## S08

**/categories/7 M8 레이저** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/7/id`, `/categories/7/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[7]` | `/categories/7` | object · 길이 5 | — |
| `id` | `/categories/7/id` | string | M8 |
| `name` | `/categories/7/name` | string | 레이저 |
| `mandatory_disclosures` | `/categories/7/mandatory_disclosures` | array · 길이 8 | — |
| `mandatory_disclosures[0]` | `/categories/7/mandatory_disclosures/0` | string | PIH(시술 후 색소침착)가 발생할 수 있으며, 한국인(Fitzpatrick III-IV)에서 위험이 높습니다 |
| `mandatory_disclosures[1]` | `/categories/7/mandatory_disclosures/1` | string | CO2 프락셔널 레이저의 경우 PIH 발생률이 약 50%에 달합니다 |
| `mandatory_disclosures[2]` | `/categories/7/mandatory_disclosures/2` | string | 시술 후 철저한 자외선 차단(SPF 50+)이 필수이며, 최소 4주-3개월간 유지해야 합니다 |
| `mandatory_disclosures[3]` | `/categories/7/mandatory_disclosures/3` | string | 홍반, 부종, 딱지 형성이 정상적인 회복 과정이며, 레이저 종류에 따라 1일-2주 지속됩니다 |
| `mandatory_disclosures[4]` | `/categories/7/mandatory_disclosures/4` | string | 드물게 흉터 형성, 영구적 색소탈실이 발생할 수 있습니다 |
| `mandatory_disclosures[5]` | `/categories/7/mandatory_disclosures/5` | string | 박리성(ablative) 레이저는 감염(HSV 재활성화 포함) 위험이 있습니다 |
| `mandatory_disclosures[6]` | `/categories/7/mandatory_disclosures/6` | string | 치료 결과는 1회로 완성되지 않으며, 보통 3-10회 반복 시술이 필요합니다 |
| `mandatory_disclosures[7]` | `/categories/7/mandatory_disclosures/7` | string | 이소트레티노인 복용력을 반드시 의사에게 알려주세요. 프락셔널/얕은 필링은 복용 중단 후 최소 6개월, 박리성(ablative) 레이저는 12개월 대기가 원칙입니다. 2017 AAD Task Force 이후 비박리성 레이저·얕은 박피는 피부 재생 상태에 따라 의사 판단으로 조기 시술이 고려될 수 있습니다 |
| `contraindications` | `/categories/7/contraindications` | array · 길이 8 | — |
| `contraindications[0]` | `/categories/7/contraindications/0` | string | 활동성 피부 감염(HSV, 세균감염 등) |
| `contraindications[1]` | `/categories/7/contraindications/1` | string | 시술 부위 활동성 피부질환 |
| `contraindications[2]` | `/categories/7/contraindications/2` | string | 이소트레티노인 복용 중 또는 중단 후 6개월 이내의 프락셔널/얕은 필링, 12개월 이내의 박리성(ablative) 레이저 (비박리성 얕은 시술은 의사 판단 하에 조기 시행 고려 가능) |
| `contraindications[3]` | `/categories/7/contraindications/3` | string | 임신 및 수유 중 |
| `contraindications[4]` | `/categories/7/contraindications/4` | string | 광과민성 약물 복용 중 |
| `contraindications[5]` | `/categories/7/contraindications/5` | string | 최근 과도한 자외선 노출 또는 인공 태닝 |
| `contraindications[6]` | `/categories/7/contraindications/6` | string | 켈로이드 체질(박리성 레이저) |
| `contraindications[7]` | `/categories/7/contraindications/7` | string | 매우 어두운 피부(Fitzpatrick V-VI)에서 일부 레이저 금기 |
| `emergency_signs` | `/categories/7/emergency_signs` | array · 길이 4 | — |
| `emergency_signs[0]` | `/categories/7/emergency_signs/0` | string | 시술 부위 수포 형성 및 심한 통증(화상) |
| `emergency_signs[1]` | `/categories/7/emergency_signs/1` | string | 시력 변화(눈 주위 시술 시) |
| `emergency_signs[2]` | `/categories/7/emergency_signs/2` | string | 시술 부위 농성 분비물, 고열(감염) |
| `emergency_signs[3]` | `/categories/7/emergency_signs/3` | string | 점점 넓어지는 흉터 또는 색소탈실 |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S08-1 | `/categories/7/mandatory_disclosures/0` | 한국인(Fitzpatrick III-IV)에서 위험이 높습니다 | 대상 집단 + 피부형 범위(로마 숫자). 'III-IV' 형태소 오분절 후보. | P·K |
| S08-2 | `/categories/7/mandatory_disclosures/1` | PIH 발생률이 약 50%에 달합니다 | 분모·출처 없음. 대상 = CO2 프락셔널 레이저. | B |
| S08-3 | `/categories/7/mandatory_disclosures/2` | 최소 4주-3개월간 유지해야 합니다 | '최소' 가 범위 전체(4주-3개월)에 걸린 구조 — 하한 범위인지 해석 불명. | B |
| S08-4 | `/categories/7/mandatory_disclosures/7` | 프락셔널/얕은 필링은 복용 중단 후 최소 6개월, 박리성(ablative) 레이저는 12개월 대기가 원칙입니다 | 기준 시점 = 이소트레티노인 복용 중단. 시술 종류별 대기 기간. '얕은 필링' 은 레이저 카테고리 밖 시술 언급(원장 간 연결 후속). | F |
| S08-5 | `/categories/7/mandatory_disclosures/7` | 2017 AAD Task Force 이후 비박리성 레이저·얕은 박피는 피부 재생 상태에 따라 의사 판단으로 조기 시술이 고려될 수 있습니다 | 예외 조건(의사 판단·피부 재생 상태). 같은 사실이 contraindications/2 에도 다른 표현('얕은 시술')으로 있다. | I·F |
| S08-6 | `/categories/7/contraindications/2` | 중단 후 6개월 이내의 프락셔널/얕은 필링, 12개월 이내의 박리성(ablative) 레이저 (비박리성 얕은 시술은 의사 판단 하에 조기 시행 고려 가능) | 고지(man/7) 는 '얕은 박피', 금기(con/2)는 '얕은 필링'·'얕은 시술' — 같은 대상인지 확정 불가. 또 S15 contraindications/5 는 같은 약물을 '중간·심부 박피' 6개월로 적어 대상 시술 표현이 다르다. | I·F |
| S08-7 | `/categories/7/contraindications/7` | 매우 어두운 피부(Fitzpatrick V-VI)에서 일부 레이저 금기 | '일부 레이저' 가 어느 레이저인지 원문 없음. | B |
| S08-8 | `/categories/7/contraindications/6` | 켈로이드 체질(박리성 레이저) | 괄호 = 금기 적용 범위 한정(잠정). | P |

## S09

**/categories/8 M9 기기 리프팅** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/8/id`, `/categories/8/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[8]` | `/categories/8` | object · 길이 5 | — |
| `id` | `/categories/8/id` | string | M9 |
| `name` | `/categories/8/name` | string | 기기 리프팅 |
| `mandatory_disclosures` | `/categories/8/mandatory_disclosures` | array · 길이 7 | — |
| `mandatory_disclosures[0]` | `/categories/8/mandatory_disclosures/0` | string | 시술 중 통증이 발생하며, HIFU는 상당한 불편감을 동반할 수 있습니다 |
| `mandatory_disclosures[1]` | `/categories/8/mandatory_disclosures/1` | string | 시술 후 일시적 부종, 홍반, 감각 이상이 발생할 수 있습니다 |
| `mandatory_disclosures[2]` | `/categories/8/mandatory_disclosures/2` | string | 드물게 신경 손상(마비, 감각 저하)이 발생할 수 있으며, 대부분 일시적입니다 |
| `mandatory_disclosures[3]` | `/categories/8/mandatory_disclosures/3` | string | 화상(표면 또는 심부)이 발생할 수 있습니다 |
| `mandatory_disclosures[4]` | `/categories/8/mandatory_disclosures/4` | string | 즉각적인 효과보다 2-3개월에 걸친 점진적 개선이 주된 효과입니다 |
| `mandatory_disclosures[5]` | `/categories/8/mandatory_disclosures/5` | string | 효과 지속 기간은 6-12개월이며, 유지 시술이 필요합니다 |
| `mandatory_disclosures[6]` | `/categories/8/mandatory_disclosures/6` | string | 금속 임플란트(치과 포함)가 있는 경우 반드시 의료진에게 알려야 합니다 |
| `contraindications` | `/categories/8/contraindications` | array · 길이 7 | — |
| `contraindications[0]` | `/categories/8/contraindications/0` | string | 임신 및 수유 중 |
| `contraindications[1]` | `/categories/8/contraindications/1` | string | 시술 부위 금속 임플란트 또는 전자 장치(심박조율기) |
| `contraindications[2]` | `/categories/8/contraindications/2` | string | 시술 부위 활동성 감염 또는 염증 |
| `contraindications[3]` | `/categories/8/contraindications/3` | string | 심한 피부 이완(수술적 교정 필요) |
| `contraindications[4]` | `/categories/8/contraindications/4` | string | 최근 필러 주입 부위(HA 필러 분해 위험, 4주 이상 간격) |
| `contraindications[5]` | `/categories/8/contraindications/5` | string | 조절되지 않는 당뇨 |
| `contraindications[6]` | `/categories/8/contraindications/6` | string | 자가면역 질환 |
| `emergency_signs` | `/categories/8/emergency_signs` | array · 길이 3 | — |
| `emergency_signs[0]` | `/categories/8/emergency_signs/0` | string | 시술 부위 수포 형성, 심한 화상 |
| `emergency_signs[1]` | `/categories/8/emergency_signs/1` | string | 안면 마비 또는 지속적 감각 소실(신경 손상) |
| `emergency_signs[2]` | `/categories/8/emergency_signs/2` | string | 심한 부종이 수일간 악화 |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S09-1 | `/categories/8/mandatory_disclosures/2` | 드물게 신경 손상(마비, 감각 저하)이 발생할 수 있으며, 대부분 일시적입니다 | 빈도(드물게) 와 경과(대부분 일시적) 가 같은 사건에 붙음. '대부분' 은 경과의 비율 수식. | P |
| S09-2 | `/categories/8/mandatory_disclosures/3` | 화상(표면 또는 심부) | 깊이 수식(표면/심부)이 화상의 깊이. 주입 깊이 아님. | P |
| S09-3 | `/categories/8/mandatory_disclosures/6` | 금속 임플란트(치과 포함)가 있는 경우 반드시 의료진에게 알려야 합니다 | contraindications/1 '시술 부위 금속 임플란트' 와 범위가 다르다(치과 포함 vs 시술 부위). 고지·금기 수준 차. | I·F |
| S09-4 | `/categories/8/contraindications/4` | 최근 필러 주입 부위(HA 필러 분해 위험, 4주 이상 간격) | 다른 시술(필러)과의 간격 조건 4주 이상. 기준 시점 = 필러 주입. 선후·간격 관계 후보(원장 간 연결 후속). | F |
| S09-5 | `/categories/8/mandatory_disclosures/0` | HIFU는 상당한 불편감을 동반할 수 있습니다 | 카테고리 이름(기기 리프팅) 아래 특정 기기 계열(HIFU) 언급. | P |

## S10

**/categories/9 M10 HIFES/EMS** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/9/id`, `/categories/9/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[9]` | `/categories/9` | object · 길이 5 | — |
| `id` | `/categories/9/id` | string | M10 |
| `name` | `/categories/9/name` | string | HIFES/EMS |
| `mandatory_disclosures` | `/categories/9/mandatory_disclosures` | array · 길이 5 | — |
| `mandatory_disclosures[0]` | `/categories/9/mandatory_disclosures/0` | string | 시술 중 강한 근수축이 유발되며 불편감을 동반할 수 있습니다 |
| `mandatory_disclosures[1]` | `/categories/9/mandatory_disclosures/1` | string | 시술 후 근육통(DOMS 유사)이 1-3일 발생할 수 있습니다 |
| `mandatory_disclosures[2]` | `/categories/9/mandatory_disclosures/2` | string | 효과 유지를 위해 주기적 반복 시술이 필요합니다(보통 주 2회, 4-6회 코스) |
| `mandatory_disclosures[3]` | `/categories/9/mandatory_disclosures/3` | string | 피하지방 감소 효과는 개인차가 크며, 식이요법·운동 병행 시 효과적입니다 |
| `mandatory_disclosures[4]` | `/categories/9/mandatory_disclosures/4` | string | 드물게 근육 경련, 일시적 감각 이상이 발생할 수 있습니다 |
| `contraindications` | `/categories/9/contraindications` | array · 길이 7 | — |
| `contraindications[0]` | `/categories/9/contraindications/0` | string | 임신 및 수유 중 |
| `contraindications[1]` | `/categories/9/contraindications/1` | string | 시술 부위 금속 임플란트(인공관절 등) |
| `contraindications[2]` | `/categories/9/contraindications/2` | string | 심박조율기 또는 이식형 전자장치 |
| `contraindications[3]` | `/categories/9/contraindications/3` | string | 간질 또는 경련 질환 |
| `contraindications[4]` | `/categories/9/contraindications/4` | string | 최근 수술(시술 부위 6주 이내) |
| `contraindications[5]` | `/categories/9/contraindications/5` | string | 악성 종양 |
| `contraindications[6]` | `/categories/9/contraindications/6` | string | 헤르니아(탈장) |
| `emergency_signs` | `/categories/9/emergency_signs` | array · 길이 3 | — |
| `emergency_signs[0]` | `/categories/9/emergency_signs/0` | string | 심한 근육통 또는 부종이 48시간 이상 악화 |
| `emergency_signs[1]` | `/categories/9/emergency_signs/1` | string | 혈뇨(횡문근융해증 의심 — 극히 드묾) |
| `emergency_signs[2]` | `/categories/9/emergency_signs/2` | string | 시술 부위 감각 소실 |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S10-1 | `/categories/9/mandatory_disclosures/1` | 근육통(DOMS 유사)이 1-3일 발생할 수 있습니다 | '1-3일 발생' — 지속 기간인지 발현 시점인지 원문만으로 불명. | B |
| S10-2 | `/categories/9/mandatory_disclosures/2` | (보통 주 2회, 4-6회 코스) | 빈도(주 2회) 와 총 회차(4-6회). '주' 가 week 로 읽힘(형태소 확인 필요). | P·K |
| S10-3 | `/categories/9/emergency_signs/0` | 심한 근육통 또는 부종이 48시간 이상 악화 | '심한' 이 부종까지 걸리는지 불명. 시간 조건 48시간 이상. | B |
| S10-4 | `/categories/9/emergency_signs/1` | 혈뇨(횡문근융해증 의심 — 극히 드묾) | 빈도(극히 드묾)가 의심 원인(횡문근융해증)에 붙음. 괄호 안 '—'. | P |
| S10-5 | `/categories/9/contraindications/4` | 최근 수술(시술 부위 6주 이내) | '최근' 을 6주 이내로 한정. 다른 구획의 '최근'(S08 con/5, S09 con/4, S14 con/6)은 기간이 각각 다르거나 없다. | F |

## S11

**/categories/10 M11 니들RF** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/10/id`, `/categories/10/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[10]` | `/categories/10` | object · 길이 5 | — |
| `id` | `/categories/10/id` | string | M11 |
| `name` | `/categories/10/name` | string | 니들RF |
| `mandatory_disclosures` | `/categories/10/mandatory_disclosures` | array · 길이 6 | — |
| `mandatory_disclosures[0]` | `/categories/10/mandatory_disclosures/0` | string | 절연침이 피부를 관통하므로 시술 중 통증이 있으며, 마취 크림을 사용합니다 |
| `mandatory_disclosures[1]` | `/categories/10/mandatory_disclosures/1` | string | 시술 후 홍반, 부종, 미세 딱지가 발생하며 3-7일 지속됩니다 |
| `mandatory_disclosures[2]` | `/categories/10/mandatory_disclosures/2` | string | 절연침(insulated needle)은 표피를 우회하여 PIH 위험이 상대적으로 낮으나, 깊은 삽입·고에너지·짙은 피부형에서는 발생할 수 있습니다 |
| `mandatory_disclosures[3]` | `/categories/10/mandatory_disclosures/3` | string | 드물게 흉터 형성, 감염이 발생할 수 있습니다 |
| `mandatory_disclosures[4]` | `/categories/10/mandatory_disclosures/4` | string | 효과 발현에 1-3개월이 소요되며, 3-5회 반복 시술이 권장됩니다 |
| `mandatory_disclosures[5]` | `/categories/10/mandatory_disclosures/5` | string | 시술 후 12-24시간 세안, 화장을 피해야 합니다 |
| `contraindications` | `/categories/10/contraindications` | array · 길이 7 | — |
| `contraindications[0]` | `/categories/10/contraindications/0` | string | 임신 및 수유 중 |
| `contraindications[1]` | `/categories/10/contraindications/1` | string | 시술 부위 활동성 감염 또는 염증 |
| `contraindications[2]` | `/categories/10/contraindications/2` | string | 심박조율기 또는 이식형 전자장치 |
| `contraindications[3]` | `/categories/10/contraindications/3` | string | 시술 부위 금속 임플란트 |
| `contraindications[4]` | `/categories/10/contraindications/4` | string | 켈로이드 체질 |
| `contraindications[5]` | `/categories/10/contraindications/5` | string | 항응고제 복용 중 |
| `contraindications[6]` | `/categories/10/contraindications/6` | string | 시술 부위 최근 실리프팅(2-3개월 이내) |
| `emergency_signs` | `/categories/10/emergency_signs` | array · 길이 3 | — |
| `emergency_signs[0]` | `/categories/10/emergency_signs/0` | string | 시술 부위 농성 분비물, 고열(감염) |
| `emergency_signs[1]` | `/categories/10/emergency_signs/1` | string | 시술 부위 점점 커지는 결절 또는 흉터 |
| `emergency_signs[2]` | `/categories/10/emergency_signs/2` | string | 심한 화상 증상(수포, 궤양) |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S11-1 | `/categories/10/mandatory_disclosures/2` | PIH 위험이 상대적으로 낮으나, 깊은 삽입·고에너지·짙은 피부형에서는 발생할 수 있습니다 | 비교(상대적으로 낮으나 — 비교 대상 원문 없음) + 조건 세 개(깊은 삽입=삽입 깊이, 고에너지, 짙은 피부형=피부 특성). | P·B |
| S11-2 | `/categories/10/mandatory_disclosures/0` | 마취 크림을 사용합니다 | 시술 절차 정보(고지 배열 안). | P |
| S11-3 | `/categories/10/contraindications/6` | 시술 부위 최근 실리프팅(2-3개월 이내) | 다른 시술(실리프팅)과의 간격 조건. 기준 시점 = 실리프팅. 원장 간 연결 후속. | F |
| S11-4 | `/categories/10/mandatory_disclosures/5` | 시술 후 12-24시간 세안, 화장을 피해야 합니다 | 관리 기간. S12 mandatory_disclosures/5 는 같은 기간에 화장만. | P |

## S12

**/categories/11 M12 마이크로니들링(MTS)** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/11/id`, `/categories/11/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[11]` | `/categories/11` | object · 길이 5 | — |
| `id` | `/categories/11/id` | string | M12 |
| `name` | `/categories/11/name` | string | 마이크로니들링(MTS) |
| `mandatory_disclosures` | `/categories/11/mandatory_disclosures` | array · 길이 6 | — |
| `mandatory_disclosures[0]` | `/categories/11/mandatory_disclosures/0` | string | 미세침이 피부를 관통하므로 출혈, 홍반이 정상적으로 발생합니다 |
| `mandatory_disclosures[1]` | `/categories/11/mandatory_disclosures/1` | string | 시술 후 24-72시간 홍반, 부종이 지속되며, 피부가 예민해집니다 |
| `mandatory_disclosures[2]` | `/categories/11/mandatory_disclosures/2` | string | 감염 위험이 있으므로 시술 전후 위생 관리가 중요합니다 |
| `mandatory_disclosures[3]` | `/categories/11/mandatory_disclosures/3` | string | 시술 후 직사광선 노출을 피하고 자외선 차단제를 꼭 사용해야 합니다 |
| `mandatory_disclosures[4]` | `/categories/11/mandatory_disclosures/4` | string | 효과 발현에 2-4주 소요되며, 4-6회 반복 시술이 권장됩니다 |
| `mandatory_disclosures[5]` | `/categories/11/mandatory_disclosures/5` | string | 시술 후 12-24시간 화장을 피해야 합니다 |
| `contraindications` | `/categories/11/contraindications` | array · 길이 6 | — |
| `contraindications[0]` | `/categories/11/contraindications/0` | string | 활동성 여드름 또는 피부 감염 |
| `contraindications[1]` | `/categories/11/contraindications/1` | string | 켈로이드 체질 |
| `contraindications[2]` | `/categories/11/contraindications/2` | string | 항응고제 복용 중 또는 출혈 경향 |
| `contraindications[3]` | `/categories/11/contraindications/3` | string | 임신 및 수유 중 |
| `contraindications[4]` | `/categories/11/contraindications/4` | string | 당뇨병(상처 회복 지연) |
| `contraindications[5]` | `/categories/11/contraindications/5` | string | 면역억제 상태 |
| `emergency_signs` | `/categories/11/emergency_signs` | array · 길이 3 | — |
| `emergency_signs[0]` | `/categories/11/emergency_signs/0` | string | 시술 부위 심한 감염(고열, 농, 봉와직염) |
| `emergency_signs[1]` | `/categories/11/emergency_signs/1` | string | 비정상적으로 지속되는 출혈 |
| `emergency_signs[2]` | `/categories/11/emergency_signs/2` | string | 심한 알레르기 반응(도포 약물에 의한) |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S12-1 | `/categories/11/mandatory_disclosures/0` | 출혈, 홍반이 정상적으로 발생합니다 | '정상적으로' — 부작용이 아닌 예상 반응으로 표시. 같은 구획 emergency_signs/1 '비정상적으로 지속되는 출혈' 과 대비. | P |
| S12-2 | `/categories/11/mandatory_disclosures/1` | 24-72시간 홍반, 부종이 지속되며, 피부가 예민해집니다 | 지속 시간 범위. '예민해집니다' 의 기간은 불명. | B |
| S12-3 | `/categories/11/contraindications/4` | 당뇨병(상처 회복 지연) | S06·S09·S13 은 '조절되지 않는 당뇨', 여기는 '당뇨병' — 수식 차이 보존. 통합 판단은 후속. | F |
| S12-4 | `/categories/11/emergency_signs/2` | 심한 알레르기 반응(도포 약물에 의한) | 원인 = 도포 약물(종류 원문 없음). | B |

## S13

**/categories/12 M13 플라즈마** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/12/id`, `/categories/12/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[12]` | `/categories/12` | object · 길이 5 | — |
| `id` | `/categories/12/id` | string | M13 |
| `name` | `/categories/12/name` | string | 플라즈마 |
| `mandatory_disclosures` | `/categories/12/mandatory_disclosures` | array · 길이 5 | — |
| `mandatory_disclosures[0]` | `/categories/12/mandatory_disclosures/0` | string | 시술 후 미세 딱지(점상 scab)가 형성되며 5-10일간 자연 탈락됩니다 |
| `mandatory_disclosures[1]` | `/categories/12/mandatory_disclosures/1` | string | 딱지를 인위적으로 제거하면 흉터 또는 색소침착이 발생할 수 있습니다 |
| `mandatory_disclosures[2]` | `/categories/12/mandatory_disclosures/2` | string | 일시적 홍반, 부종이 발생하며 수일간 지속됩니다 |
| `mandatory_disclosures[3]` | `/categories/12/mandatory_disclosures/3` | string | PIH가 발생할 수 있으며, 자외선 차단이 필수입니다 |
| `mandatory_disclosures[4]` | `/categories/12/mandatory_disclosures/4` | string | 드물게 화상, 흉터가 발생할 수 있습니다 |
| `contraindications` | `/categories/12/contraindications` | array · 길이 5 | — |
| `contraindications[0]` | `/categories/12/contraindications/0` | string | 임신 및 수유 중 |
| `contraindications[1]` | `/categories/12/contraindications/1` | string | 심박조율기 또는 이식형 전자장치 |
| `contraindications[2]` | `/categories/12/contraindications/2` | string | 시술 부위 활동성 감염 |
| `contraindications[3]` | `/categories/12/contraindications/3` | string | 켈로이드 체질 |
| `contraindications[4]` | `/categories/12/contraindications/4` | string | 조절되지 않는 당뇨 |
| `emergency_signs` | `/categories/12/emergency_signs` | array · 길이 3 | — |
| `emergency_signs[0]` | `/categories/12/emergency_signs/0` | string | 시술 부위 심한 화상(수포, 궤양) |
| `emergency_signs[1]` | `/categories/12/emergency_signs/1` | string | 감염 징후(고열, 농성 분비물) |
| `emergency_signs[2]` | `/categories/12/emergency_signs/2` | string | 점점 넓어지는 흉터 |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S13-1 | `/categories/12/mandatory_disclosures/0` | 미세 딱지(점상 scab)가 형성되며 5-10일간 자연 탈락됩니다 | 기간이 '탈락까지' 인지 '탈락 진행 기간' 인지 불명. | B |
| S13-2 | `/categories/12/mandatory_disclosures/1` | 딱지를 인위적으로 제거하면 흉터 또는 색소침착이 발생할 수 있습니다 | 조건(인위적 제거) → 결과. 관리 행동과 사건의 인과. | P |
| S13-3 | `/categories/12/mandatory_disclosures/2` | 수일간 지속됩니다 | 수치 없는 기간 표현. | P |

## S14

**/categories/13 M14 크라이오리포라이시스** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조(긴 값 man/0 은 문장 단위로 재독))
· 함께 읽은 상위 문맥: `/description`, `/categories/13/id`, `/categories/13/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[13]` | `/categories/13` | object · 길이 5 | — |
| `id` | `/categories/13/id` | string | M14 |
| `name` | `/categories/13/name` | string | 크라이오리포라이시스 |
| `mandatory_disclosures` | `/categories/13/mandatory_disclosures` | array · 길이 7 | — |
| `mandatory_disclosures[0]` | `/categories/13/mandatory_disclosures/0` | string | PAH(역설적 지방 비대, Paradoxical Adipose Hyperplasia)가 발생할 수 있으며, 통합 발생률은 약 0.22%(약 455명 중 1명, 95% CI 0.10-0.47%)로 보고됩니다. 일부 연구에서는 0.05-0.39% 범위이며 과소보고 가능성이 있고, 남성·복부·반복 시술에서 위험 증가 경향은 있었으나 통계적으로 유의하지 않았습니다. PAH 발생 시 지방흡입 수술이 필요할 수 있습니다 |
| `mandatory_disclosures[1]` | `/categories/13/mandatory_disclosures/1` | string | 효과가 나타나기까지 2-3개월이 소요되며, 1회 시술로 약 20-25% 지방 감소가 기대됩니다 |
| `mandatory_disclosures[2]` | `/categories/13/mandatory_disclosures/2` | string | 시술 부위에 일시적 홍반, 부종, 멍, 감각 둔화가 발생하며 수주간 지속될 수 있습니다 |
| `mandatory_disclosures[3]` | `/categories/13/mandatory_disclosures/3` | string | 지방 감소 시술이며 체중 감량 목적이 아닙니다 |
| `mandatory_disclosures[4]` | `/categories/13/mandatory_disclosures/4` | string | 시술 후 해당 부위를 2분간 마사지하면 효과가 향상됩니다 |
| `mandatory_disclosures[5]` | `/categories/13/mandatory_disclosures/5` | string | 드물게 지속적인 통증, 감각 이상이 수개월 지속될 수 있습니다 |
| `mandatory_disclosures[6]` | `/categories/13/mandatory_disclosures/6` | string | 시술 후 식이 조절과 운동을 병행해야 효과가 유지됩니다 |
| `contraindications` | `/categories/13/contraindications` | array · 길이 7 | — |
| `contraindications[0]` | `/categories/13/contraindications/0` | string | 한랭 글로불린혈증(cryoglobulinemia) |
| `contraindications[1]` | `/categories/13/contraindications/1` | string | 한랭 두드러기(cold urticaria) |
| `contraindications[2]` | `/categories/13/contraindications/2` | string | 발작성 한랭 혈색소뇨증 |
| `contraindications[3]` | `/categories/13/contraindications/3` | string | 레이노 현상(중증) |
| `contraindications[4]` | `/categories/13/contraindications/4` | string | 시술 부위 탈장(hernia) |
| `contraindications[5]` | `/categories/13/contraindications/5` | string | 임신 및 수유 중 |
| `contraindications[6]` | `/categories/13/contraindications/6` | string | 시술 부위 최근 수술 또는 흉터 |
| `emergency_signs` | `/categories/13/emergency_signs` | array · 길이 3 | — |
| `emergency_signs[0]` | `/categories/13/emergency_signs/0` | string | 시술 부위가 시술 후 수주-수개월 내 오히려 딱딱하게 커지는 경우(PAH 의심) |
| `emergency_signs[1]` | `/categories/13/emergency_signs/1` | string | 심한 동상 증상(수포, 피부 괴사) |
| `emergency_signs[2]` | `/categories/13/emergency_signs/2` | string | 시술 부위 지속적이고 심한 통증 |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S14-1 | `/categories/13/mandatory_disclosures/0` | 통합 발생률은 약 0.22%(약 455명 중 1명, 95% CI 0.10-0.47%)로 보고됩니다 | 분모 표현(455명 중 1명)·신뢰구간이 있는 유일한 발생률. '통합' 은 메타분석 성격으로 읽히나 출처 원문 없음. | P·B |
| S14-2 | `/categories/13/mandatory_disclosures/0` | 일부 연구에서는 0.05-0.39% 범위이며 과소보고 가능성이 있고 | 같은 사건에 수치 두 종(0.22% 통합 / 0.05-0.39% 일부 연구). 서로 다른 근거 수준을 함께 보존해야 함. | F |
| S14-3 | `/categories/13/mandatory_disclosures/0` | 남성·복부·반복 시술에서 위험 증가 경향은 있었으나 통계적으로 유의하지 않았습니다 | 위험 요인 후보 + 부정(유의하지 않음). 요인으로 확정하면 뜻이 뒤집힌다. | P |
| S14-4 | `/categories/13/mandatory_disclosures/1` | 1회 시술로 약 20-25% 지방 감소가 기대됩니다 | % 는 효과량(지방 감소 비율) — 발생률과 다른 수치 종류. | P |
| S14-5 | `/categories/13/mandatory_disclosures/4` | 시술 후 해당 부위를 2분간 마사지하면 효과가 향상됩니다 | 단정 진술. S03 man/6 는 마사지 효과를 '미입증' 으로 적음(다른 카테고리·다른 마사지라 불일치로 확정하지 않음). | F |
| S14-6 | `/categories/13/emergency_signs/0` | 시술 후 수주-수개월 내 오히려 딱딱하게 커지는 경우(PAH 의심) | '오히려' = 기대 효과(감소)와 반대. 시간 창 수주-수개월. | P |

## S15

**/categories/14 M15 메디컬스킨케어** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조(긴 값 man/3 은 문장 단위로 재독))
· 함께 읽은 상위 문맥: `/description`, `/categories/14/id`, `/categories/14/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[14]` | `/categories/14` | object · 길이 5 | — |
| `id` | `/categories/14/id` | string | M15 |
| `name` | `/categories/14/name` | string | 메디컬스킨케어 |
| `mandatory_disclosures` | `/categories/14/mandatory_disclosures` | array · 길이 7 | — |
| `mandatory_disclosures[0]` | `/categories/14/mandatory_disclosures/0` | string | 케미컬 필링 후 홍반, 각질 탈락, 일시적 피부 민감도 증가가 정상입니다 |
| `mandatory_disclosures[1]` | `/categories/14/mandatory_disclosures/1` | string | TCA 필링(중간-심층)은 PIH 위험이 있으며, 특히 한국인에서 주의가 필요합니다 |
| `mandatory_disclosures[2]` | `/categories/14/mandatory_disclosures/2` | string | 시술 후 자외선 차단이 필수이며, 최소 2-4주간 철저히 해야 합니다 |
| `mandatory_disclosures[3]` | `/categories/14/mandatory_disclosures/3` | string | 이소트레티노인(로아큐탄) 경구 복용은 태아에 심각한 기형을 유발하므로 임신 중 절대 금기이며, 복용 시작 1개월 전부터 복용 중 및 복용 중단 후 1개월까지 확실한 피임이 필요합니다. 임신은 복용 중단 후 최소 1개월(FDA iPLEDGE·EU·MFDS RMP 공통 기준)이 지난 뒤 가능합니다. |
| `mandatory_disclosures[4]` | `/categories/14/mandatory_disclosures/4` | string | 이소트레티노인 복용 중에는 헌혈이 금지되며, 간기능·혈중 지질 정기 검사가 필요합니다 |
| `mandatory_disclosures[5]` | `/categories/14/mandatory_disclosures/5` | string | 레티노이드 사용 시 피부 건조, 홍반, 자극이 나타날 수 있으며 점진적으로 농도를 올려야 합니다 |
| `mandatory_disclosures[6]` | `/categories/14/mandatory_disclosures/6` | string | 하이드라페이셜, 아쿠아필 등 딥클렌징 후에도 일시적 홍반이 발생할 수 있습니다 |
| `contraindications` | `/categories/14/contraindications` | array · 길이 6 | — |
| `contraindications[0]` | `/categories/14/contraindications/0` | string | 임신 및 수유 중(특히 이소트레티노인, 레티노이드 절대 금기) |
| `contraindications[1]` | `/categories/14/contraindications/1` | string | 활동성 피부 감염 또는 개방성 상처 |
| `contraindications[2]` | `/categories/14/contraindications/2` | string | 시술 부위 활동성 습진, 건선 |
| `contraindications[3]` | `/categories/14/contraindications/3` | string | 중증 로사세아(필링 시) |
| `contraindications[4]` | `/categories/14/contraindications/4` | string | 광과민성 질환 |
| `contraindications[5]` | `/categories/14/contraindications/5` | string | 이소트레티노인 복용 중 또는 중단 후 6개월 이내의 중간·심부 박피는 금기. 얕은 박피는 의사 판단 하에 조기 고려 가능(2017 ASDS Task Force(Waldman et al., Dermatol Surg 2017)) |
| `emergency_signs` | `/categories/14/emergency_signs` | array · 길이 4 | — |
| `emergency_signs[0]` | `/categories/14/emergency_signs/0` | string | 필링 후 심한 화학 화상(심부 수포, 궤양) |
| `emergency_signs[1]` | `/categories/14/emergency_signs/1` | string | 이소트레티노인 복용 중 심한 두통, 시력 변화(두개내압 상승 의심) |
| `emergency_signs[2]` | `/categories/14/emergency_signs/2` | string | 심한 알레르기 반응 |
| `emergency_signs[3]` | `/categories/14/emergency_signs/3` | string | 간수치 급격한 상승 징후(황달, 심한 피로, 짙은 소변) |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S15-1 | `/categories/14/mandatory_disclosures/3` | 복용 시작 1개월 전부터 복용 중 및 복용 중단 후 1개월까지 확실한 피임이 필요합니다 | 기준 시점 세 개(시작 전·복용 중·중단 후)로 이루어진 기간. 대상은 시술이 아니라 약물 복용. | P |
| S15-2 | `/categories/14/mandatory_disclosures/3` | (FDA iPLEDGE·EU·MFDS RMP 공통 기준) | 규제 기준 출처 명칭. 원장 안에서 사실 검증 불가. | B |
| S15-3 | `/categories/14/contraindications/5` | 중단 후 6개월 이내의 중간·심부 박피는 금기 | S08 은 '프락셔널/얕은 필링' 6개월, 여기는 '중간·심부 박피' 6개월이고 '얕은 박피는 조기 고려 가능'. 같은 약물에 대한 대상 시술 범위가 구획마다 다르다. | I·F |
| S15-4 | `/categories/14/contraindications/5` | 2017 ASDS Task Force(Waldman et al., Dermatol Surg 2017) | S08 man/7 는 같은 해 'AAD Task Force' 로 적음. 기관명 차이 — 원문 내 불일치 관찰(사실 판정 안 함). | I |
| S15-5 | `/categories/14/contraindications/0` | 임신 및 수유 중(특히 이소트레티노인, 레티노이드 절대 금기) | '특히 … 절대 금기' 가 성분 조건부 강조. 다른 구획의 같은 문구 '임신 및 수유 중' 과 괄호 유무 차이. | P |
| S15-6 | `/categories/14/emergency_signs/1` | 이소트레티노인 복용 중 심한 두통, 시력 변화(두개내압 상승 의심) | 징후의 조건이 시술이 아닌 약물 복용. | P |
| S15-7 | `/categories/14/mandatory_disclosures/1` | TCA 필링(중간-심층) | 괄호 = 깊이 범위(필링 깊이). | P |

## S16

**/categories/15 M16 수액치료** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조)
· 함께 읽은 상위 문맥: `/description`, `/categories/15/id`, `/categories/15/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[15]` | `/categories/15` | object · 길이 5 | — |
| `id` | `/categories/15/id` | string | M16 |
| `name` | `/categories/15/name` | string | 수액치료 |
| `mandatory_disclosures` | `/categories/15/mandatory_disclosures` | array · 길이 6 | — |
| `mandatory_disclosures[0]` | `/categories/15/mandatory_disclosures/0` | string | 정맥주사를 통한 시술이므로 주사 부위 통증, 멍, 부종이 발생할 수 있습니다 |
| `mandatory_disclosures[1]` | `/categories/15/mandatory_disclosures/1` | string | 드물게 알레르기 반응(두드러기, 아나필락시스)이 발생할 수 있습니다 |
| `mandatory_disclosures[2]` | `/categories/15/mandatory_disclosures/2` | string | 효과의 지속 기간은 1-2주로 짧으며, 정기적 시술이 필요합니다 |
| `mandatory_disclosures[3]` | `/categories/15/mandatory_disclosures/3` | string | 과학적 근거가 아직 제한적인 부분이 있으며, 개인차가 큽니다 |
| `mandatory_disclosures[4]` | `/categories/15/mandatory_disclosures/4` | string | 신장 기능이 저하된 경우 과량 투여 시 위험할 수 있습니다 |
| `mandatory_disclosures[5]` | `/categories/15/mandatory_disclosures/5` | string | 비타민C 고용량 투여 시 G6PD 결핍 환자에서 용혈 위험이 있습니다 |
| `contraindications` | `/categories/15/contraindications` | array · 길이 5 | — |
| `contraindications[0]` | `/categories/15/contraindications/0` | string | 시술 성분에 대한 알레르기 병력 |
| `contraindications[1]` | `/categories/15/contraindications/1` | string | G6PD 결핍(비타민C 고용량 시) |
| `contraindications[2]` | `/categories/15/contraindications/2` | string | 심부전 또는 신부전(수분 과부하 위험) |
| `contraindications[3]` | `/categories/15/contraindications/3` | string | 임신 및 수유 중(성분에 따라) |
| `contraindications[4]` | `/categories/15/contraindications/4` | string | 신장석 병력(비타민C 고용량 시 옥살산 결석 위험) |
| `emergency_signs` | `/categories/15/emergency_signs` | array · 길이 3 | — |
| `emergency_signs[0]` | `/categories/15/emergency_signs/0` | string | 아나필락시스(호흡곤란, 혈압 저하, 의식 저하) |
| `emergency_signs[1]` | `/categories/15/emergency_signs/1` | string | 주사 부위 심한 부종 및 통증(혈관외유출 의심) |
| `emergency_signs[2]` | `/categories/15/emergency_signs/2` | string | 흉통, 호흡곤란(수분 과부하 또는 공기색전 의심) |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S16-1 | `/categories/15/mandatory_disclosures/2` | 효과의 지속 기간은 1-2주로 짧으며 | 효과 지속 + 평가어(짧으며). | P |
| S16-2 | `/categories/15/mandatory_disclosures/4` | 신장 기능이 저하된 경우 과량 투여 시 위험할 수 있습니다 | 조건 두 개(환자 상태·투여량). '위험' 의 사건 내용 원문 없음. | B |
| S16-3 | `/categories/15/contraindications/3` | 임신 및 수유 중(성분에 따라) | 다른 구획과 같은 금기가 조건부(성분에 따라)로 완화. 어떤 성분인지 원문 없음. | B |
| S16-4 | `/categories/15/contraindications/1` | G6PD 결핍(비타민C 고용량 시) | 성분·용량 조건부 금기. '고용량' 의 기준 수치 원문 없음. | B |
| S16-5 | `/categories/15/emergency_signs/2` | 흉통, 호흡곤란(수분 과부하 또는 공기색전 의심) | 의심 원인 두 개(또는). | P |

## S17

**/categories/16 M17 줄기세포치료** · 읽기: 직접 읽음 (전체 값 통독 + 구획 표 대조(긴 값 man/0·man/6 은 문장 단위로 재독))
· 함께 읽은 상위 문맥: `/description`, `/categories/16/id`, `/categories/16/name`

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| `categories[16]` | `/categories/16` | object · 길이 5 | — |
| `id` | `/categories/16/id` | string | M17 |
| `name` | `/categories/16/name` | string | 줄기세포치료 |
| `mandatory_disclosures` | `/categories/16/mandatory_disclosures` | array · 길이 7 | — |
| `mandatory_disclosures[0]` | `/categories/16/mandatory_disclosures/0` | string | 주입형 엑소좀·줄기세포 배양액(conditioned media) 제품은 국내에서 '도포용 화장품'으로만 허가되어 있으며 주사제(의약품)로 허가받지 않았습니다. 이를 주사로 체내에 투여하는 시술은 오프라벨·무허가 의약품 사용에 해당해 식약처 규제 대상이며(2025년부터 화장품 표시·광고에서 '엑소좀' 표현 금지), 도포용 화장품을 주사한 의사에게 자격정지 처분이 확정된 판례가 있습니다. 시술 여부는 의료진과 충분히 상담 후 결정하십시오. |
| `mandatory_disclosures[1]` | `/categories/16/mandatory_disclosures/1` | string | 장기 안전성 데이터가 아직 불충분합니다 |
| `mandatory_disclosures[2]` | `/categories/16/mandatory_disclosures/2` | string | 효과의 개인차가 매우 크며, 과학적 근거가 축적 중인 분야입니다 |
| `mandatory_disclosures[3]` | `/categories/16/mandatory_disclosures/3` | string | 줄기세포배양액(conditioned media) 사용 시 감염, 알레르기 반응 가능성이 있습니다 |
| `mandatory_disclosures[4]` | `/categories/16/mandatory_disclosures/4` | string | 엑소좀(exosome) 제품의 품질과 함량이 제조사마다 다르므로 확인이 필요합니다 |
| `mandatory_disclosures[5]` | `/categories/16/mandatory_disclosures/5` | string | 과장 광고에 주의해야 하며, 의료진과 충분한 상담 후 결정해야 합니다 |
| `mandatory_disclosures[6]` | `/categories/16/mandatory_disclosures/6` | string | 화장품은 주사제와 달리 임상시험·멸균·무발열원(항원/발열물질) 공정을 거치지 않아, 주사 시 이물육아종(foreign body granuloma)·흉터·색소침착·감염 등 중대한 부작용이 보고되어 있습니다. |
| `contraindications` | `/categories/16/contraindications` | array · 길이 6 | — |
| `contraindications[0]` | `/categories/16/contraindications/0` | string | 암 환자 또는 암 병력(세포 증식 촉진 우려) |
| `contraindications[1]` | `/categories/16/contraindications/1` | string | 자가면역 질환 |
| `contraindications[2]` | `/categories/16/contraindications/2` | string | 활동성 감염 |
| `contraindications[3]` | `/categories/16/contraindications/3` | string | 임신 및 수유 중 |
| `contraindications[4]` | `/categories/16/contraindications/4` | string | 면역억제 상태 |
| `contraindications[5]` | `/categories/16/contraindications/5` | string | 배양액 성분 과민반응 병력 |
| `emergency_signs` | `/categories/16/emergency_signs` | array · 길이 3 | — |
| `emergency_signs[0]` | `/categories/16/emergency_signs/0` | string | 심한 알레르기 반응(아나필락시스) |
| `emergency_signs[1]` | `/categories/16/emergency_signs/1` | string | 시술 부위 심한 감염(고열, 농, 봉와직염) |
| `emergency_signs[2]` | `/categories/16/emergency_signs/2` | string | 비정상적 조직 성장 또는 종괴 |

**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)

| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |
|---|---|---|---|---|
| S17-1 | `/categories/16/mandatory_disclosures/0` | 국내에서 '도포용 화장품'으로만 허가되어 있으며 주사제(의약품)로 허가받지 않았습니다 | 규제·허가 상태 진술(부정 포함). 임상 부작용이 아닌 법적 정보 종류. | P |
| S17-2 | `/categories/16/mandatory_disclosures/0` | (2025년부터 화장품 표시·광고에서 '엑소좀' 표현 금지) | 시점(2025년부터) 이 붙은 규제 사실. 원장 안에서 검증 불가. | B |
| S17-3 | `/categories/16/mandatory_disclosures/0` | 도포용 화장품을 주사한 의사에게 자격정지 처분이 확정된 판례가 있습니다 | 판례 언급 — 사건·출처 식별 정보 없음. | B |
| S17-4 | `/categories/16/name` | 줄기세포치료 | 카테고리 이름은 줄기세포치료인데 고지 본문은 엑소좀·줄기세포 배양액 제품을 주로 다룬다. 이름과 대상 범위 관계는 후속. | F |
| S17-5 | `/categories/16/mandatory_disclosures/6` | 무발열원(항원/발열물질) 공정을 거치지 않아 | 괄호 안 '/' 는 풀이·나열. 부정(거치지 않아) → 부작용 보고의 원인 진술. | P |
| S17-6 | `/categories/16/contraindications/0` | 암 환자 또는 암 병력(세포 증식 촉진 우려) | 괄호 = 금기 사유(우려 — 가능성 수준). | P |

