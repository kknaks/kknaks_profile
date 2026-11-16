# S13 — /categories/M13

[← review.md 목차](./review.md)

- 읽기 상태: read_direct · 마지막 읽은 Pointer `/categories/M13/effects`
- 공동 참조 문맥(소유 아님): `/source_method`, `/accuracy_summary`, `/categories/M13/name`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 JSON 리터럴 그대로다(이스케이프 포함). 관찰은 이 표에 섞지 않고 §2 에 둔다. 표현 ID 는 expressions.json.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/M13` | M13 | object | (object, 자식 4) | 84993–85068 |  |  |
| `/categories/M13/name` | name | string | "Plasma skin treatment" | 85001–85024 | excluded | E0660 |
| `/categories/M13/moa` | moa | array | (array, 자식 0) | 85031–85033 |  |  |
| `/categories/M13/adverse_effects` | adverse_effects | array | (array, 자식 0) | 85052–85054 |  |  |
| `/categories/M13/effects` | effects | array | (array, 자식 0) | 85065–85067 |  |  |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

- **S13-O1** [P] `/categories/M13/moa`, `/categories/M13/adverse_effects`, `/categories/M13/effects` — 세 배열 모두 빈 배열. name 'Plasma skin treatment' 만 있다.

## 3. 수동 표현 (직접 읽기에서 수집)

| 표현 ID | Pointer | 구간 | 원문 구절 | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0660 | `/categories/M13/name` | 0–21 | Plasma skin treatment | name_candidate | P |  |

## 4. 미결

- **S13-B1** [B] `/categories/M13/moa`, `/categories/M13/adverse_effects`, `/categories/M13/effects` — 진술 0개.
