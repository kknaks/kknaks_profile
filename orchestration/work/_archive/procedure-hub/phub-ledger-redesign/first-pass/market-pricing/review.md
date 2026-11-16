# market-pricing.json — 1차 조사 (읽기용)

**1차 범위 종료: 예 (근거 validation.md) · 원장 전체 완료 아님** — 열린 미결은 [issues.md](issues.md).

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/market-pricing.json` · 12,214 bytes · sha256 `601d7e7b4db29731bf15304ff3ec9489ba38838e9f5ba2144c2c181cfd15e477`
- 노드 806 (말단 648 · 컨테이너 158 · 빈 컨테이너 0 · 빈 문자열 0 · null 0) · 중복 키 0 · 백슬래시 이스케이프 0
- 구획: 루트 메타 S00 + 카테고리별 S01~S17 (전부 직접 읽음 — coverage.json `direct_read`)
- 기계 기록: source-map.json(구조·값·구간) · morphology.json · expressions.json · coverage.json · 검증 validation.md

## 상태

| 항목 | 상태 |
|---|---|
| 전수 읽기 | S00~S17 18구획 전부 직접 읽음(구획별 manual/S*.json 저장) |
| 구조·값 수집 | 노드 806 · 키 출현 666 · 모든 말단 값 원문·Pointer·리터럴 구간 기록 |
| 형태소·표현 수집 | Kiwi 0.24.1(cong, 1스레드) 텍스트 262값 988토큰 · 제외 문자열 20 · 숫자 말단 366(분석 대상 아님) · 알려진 오분절 출현 21 · 자동 후보 348 · 직접 읽기 표현 250 |
| 기계 검증 | validation.md 참조 (verify.py) |
| 읽기 검토 | 작성자 구획별 직접 읽기 + 표현 재대조(validation.md §읽기 검토). 독립 검토는 코디 몫 |
| 알려진 분석 오류 | issues.md K 절 |
| 열린 미결 | issues.md (B·I·P·F·K, C 0) |
| 후속 의미 조사 | 시작 안 함 |

## 컬럼 구성

원본 키 이름 그대로. 모든 카테고리·항목이 같은 키 집합을 가진다(선택적 필드 없음 — 기계 확인).

| 원본 컬럼(경로 패턴) | 자료형 | 중첩 구조 | 출현 수 | 원문 예시 | 예시 위치 |
|---|---|---|---|---|---|
| `version` (`/version`) | string | 루트 객체 키 | 1 | `"1.1"` | `/version` |
| `updated` (`/updated`) | string(날짜 형태) | 루트 객체 키 | 1 | `"2026-07-26"` | `/updated` |
| `currency` (`/currency`) | string(코드) | 루트 객체 키 | 1 | `"KRW"` | `/currency` |
| `note` (`/note`) | string(문장 3개) | 루트 객체 키 | 1 | `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.` | `/note` |
| `categories` (`/categories`) | array[17] of object | 루트 객체 키 | 1 | (객체 17개) | `/categories` |
| `categories[].id` (`/categories/{i}/id`) | string | 카테고리 객체 | 17 | `"M1"` | `/categories/0/id` |
| `categories[].name` (`/categories/{i}/name`) | string | 카테고리 객체 | 17 | `"보톡스"` | `/categories/0/name` |
| `categories[].items` (`/categories/{i}/items`) | array[6~10] of object | 카테고리 객체 | 17 (원소 합 122) | (객체 10개) | `/categories/0/items` |
| `items[].name` (`/categories/{i}/items/{j}/name`) | string | 항목 객체 | 122 | `"이마 주름 (수입)"` | `/categories/0/items/0/name` |
| `items[].unit` (`/categories/{i}/items/{j}/unit`) | string | 항목 객체 | 122 | `"1회"` | `/categories/0/items/0/unit` |
| `items[].low` (`/categories/{i}/items/{j}/low`) | integer | 항목 객체 | 122 | `50000` | `/categories/0/items/0/low` |
| `items[].mid` (`/categories/{i}/items/{j}/mid`) | integer | 항목 객체 | 122 | `100000` | `/categories/0/items/0/mid` |
| `items[].high` (`/categories/{i}/items/{j}/high`) | integer | 항목 객체 | 122 | `200000` | `/categories/0/items/0/high` |

### `unit` 값의 형태 변형 (원문 값 전부)

| `unit` 원문 값 | 출현 수 | 첫 위치 |
|---|---|---|
| `1회` | 87 | `/categories/0/items/0/unit` |
| `1cc` | 9 | `/categories/1/items/0/unit` |
| `2cc` | 6 | `/categories/1/items/4/unit` |
| `1바이알` | 1 | `/categories/2/items/0/unit` |
| `3회` | 2 | `/categories/2/items/1/unit` |
| `4cc` | 1 | `/categories/2/items/5/unit` |
| `1.5cc` | 1 | `/categories/2/items/6/unit` |
| `2ml` | 1 | `/categories/3/items/4/unit` |
| `부위/1회` | 1 | `/categories/3/items/5/unit` |
| `10줄` | 1 | `/categories/6/items/0/unit` |
| `8줄` | 1 | `/categories/6/items/1/unit` |
| `1개` | 2 | `/categories/7/items/8/unit` |
| `900샷` | 1 | `/categories/8/items/5/unit` |
| `450샷` | 1 | `/categories/8/items/6/unit` |
| `4회` | 1 | `/categories/9/items/3/unit` |
| `1부위` | 3 | `/categories/13/items/0/unit` |
| `양쪽` | 3 | `/categories/13/items/1/unit` |

빈 값(빈 문자열·빈 배열·빈 객체·null): 없음(기계 확인). 숫자는 모두 정수, 통화 기호·천 단위 구분 없음.

## 구획 목차

| 구획 | 범위 | 소유 말단 | 직접 읽기 | 문서 |
|---|---|---|---|---|
| S00 | 루트 메타 (version·updated·currency·note) + 루트 객체·categories 배열 컨테이너 | 4 | ○ | [review-part-S00.md](review-part-S00.md) |
| S01 | M1 보톡스 (10항목) | 52 | ○ | [review-part-S01.md](review-part-S01.md) |
| S02 | M2 필러 (8항목) | 42 | ○ | [review-part-S02.md](review-part-S02.md) |
| S03 | M3 바이오스티뮬레이터/콜라겐부스터 (7항목) | 37 | ○ | [review-part-S03.md](review-part-S03.md) |
| S04 | M4 스킨부스터 (7항목) | 37 | ○ | [review-part-S04.md](review-part-S04.md) |
| S05 | M5 PRP/엑소좀 (6항목) | 32 | ○ | [review-part-S05.md](review-part-S05.md) |
| S06 | M6 지방이식 (7항목) | 37 | ○ | [review-part-S06.md](review-part-S06.md) |
| S07 | M7 실리프팅 (7항목) | 37 | ○ | [review-part-S07.md](review-part-S07.md) |
| S08 | M8 레이저 (10항목) | 52 | ○ | [review-part-S08.md](review-part-S08.md) |
| S09 | M9 에너지기기(HIFU/RF) (8항목) | 42 | ○ | [review-part-S09.md](review-part-S09.md) |
| S10 | M10 HIFES/EMS (6항목) | 32 | ○ | [review-part-S10.md](review-part-S10.md) |
| S11 | M11 니들RF (7항목) | 37 | ○ | [review-part-S11.md](review-part-S11.md) |
| S12 | M12 마이크로니들링(MTS) (6항목) | 32 | ○ | [review-part-S12.md](review-part-S12.md) |
| S13 | M13 플라즈마 (6항목) | 32 | ○ | [review-part-S13.md](review-part-S13.md) |
| S14 | M14 크라이오리포라이시스 (6항목) | 32 | ○ | [review-part-S14.md](review-part-S14.md) |
| S15 | M15 메디컬스킨케어 (7항목) | 37 | ○ | [review-part-S15.md](review-part-S15.md) |
| S16 | M16 수액치료 (8항목) | 42 | ○ | [review-part-S16.md](review-part-S16.md) |
| S17 | M17 줄기세포치료 (6항목) | 32 | ○ | [review-part-S17.md](review-part-S17.md) |

각 구획 문서는 ①상위 문맥 ②원문 값 표(원본 컬럼명·자료형·Pointer) ③잠정 관찰(원문과 분리) ④직접 읽기 표현 ⑤자동 후보 ⑥형태소 ⑦미결 순서다.

