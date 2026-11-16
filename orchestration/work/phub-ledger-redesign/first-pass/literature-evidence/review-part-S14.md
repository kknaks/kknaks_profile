# S14 — /categories/M14

[← review.md 목차](./review.md)

- 읽기 상태: read_direct · 마지막 읽은 Pointer `/categories/M14/effects`
- 공동 참조 문맥(소유 아님): `/source_method`, `/accuracy_summary`, `/categories/M14/name`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 JSON 리터럴 그대로다(이스케이프 포함). 관찰은 이 표에 섞지 않고 §2 에 둔다. 표현 ID 는 expressions.json.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/M14` | M14 | object | (object, 자식 4) | 85075–85142 |  |  |
| `/categories/M14/name` | name | string | "Cryolipolysis" | 85083–85098 | excluded | E0661 |
| `/categories/M14/moa` | moa | array | (array, 자식 0) | 85105–85107 |  |  |
| `/categories/M14/adverse_effects` | adverse_effects | array | (array, 자식 0) | 85126–85128 |  |  |
| `/categories/M14/effects` | effects | array | (array, 자식 0) | 85139–85141 |  |  |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

- **S14-O1** [P] `/categories/M14/moa`, `/categories/M14/adverse_effects`, `/categories/M14/effects` — 세 배열 모두 빈 배열. name 'Cryolipolysis' 만 있다.

## 3. 수동 표현 (직접 읽기에서 수집)

| 표현 ID | Pointer | 구간 | 원문 구절 | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0661 | `/categories/M14/name` | 0–13 | Cryolipolysis | name_candidate | P |  |

## 4. 미결

- **S14-B1** [B] `/categories/M14/moa`, `/categories/M14/adverse_effects`, `/categories/M14/effects` — 진술 0개.
