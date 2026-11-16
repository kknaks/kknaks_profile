# S00 — 상위 메타 — / · /version · /updated · /categories 컨테이너

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories`
- 소유 노드 4 · 소유 말단 2 · 공동 참조 문맥(소유 아님): 없음
- 수동 기록 `manual/S00.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/` | (루트) | object | (object, 자식 3) | 0–13043 |  |  |
| `/version` | version | string | "1.3" | 12–15 | 제외(version_code) |  |
| `/updated` | updated | string | "2026-07-26" | 28–38 | 제외(date) |  |
| `/categories` | categories | array | (array, 자식 17) | 53–13042 |  |  |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S00-O1 | P | `/version` | 버전 식별자 "1.3". 언어 텍스트 아님 — 형태소 제외 |
| S00-O2 | P | `/updated` | 날짜 "2026-07-26". 무엇의 갱신일인지(파일 전체/개별 항목) 원문에 범위 표기 없음 |
| S00-O3 | P | `/categories` | 배열 17개, 각 원소는 동일 9키(id·name·patient_name·simple_explanation·how_it_works·duration_simple·pain_level·downtime·common_concerns). common_concerns 는 모두 {q,a} 3개 |
| S00-O4 | F | `/categories` | id(M1~M17)·name 은 다른 원장의 카테고리 체계를 가리키는 것으로 보이나 이 원장 안에는 대응 정의가 없다. 연결은 후속 과제(다른 원장은 열지 않았다) |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

