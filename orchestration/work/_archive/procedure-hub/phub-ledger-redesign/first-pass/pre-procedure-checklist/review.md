# pre-procedure-checklist.json — 1차 수집 review

## 상태

- **1차 범위 종료: 예** · **원장 전체 완료 아님**(의미 조사·공통 모델·관계 확정은 후속 단계)
- 전수 읽기: 6/6 구획 직접 읽기 완료
- 구조·값 수집: 노드 503 · 말단 331 · 객체 153 · 배열 19 · 빈 컨테이너 0 · 빈 문자열 0 · null 0 · 중복 키 0 · 이스케이프 0
- 형태소·표현 수집: kiwi 적용 문자열 165 · 제외 166(코드값) · 필드명 10종 별도 · 자동 후보 425(정규식 일치분만) · 수동 표현 188
- 기계 검증 / 읽기 검토 / 미결: [validation.md](validation.md) · [issues.md](issues.md) · 재개: [progress.md](progress.md)

## 원본

- 경로 `orchestration/work/phub-recommend/bronze/phub-ledger/pre-procedure-checklist.json` · 14569 bytes · 9629 codepoints · sha256 `0de87bff91f721fe685884025d31749017d44da250492b2db9d49109a61e4086` · UTF-8, BOM 없음, 한 줄(끝 개행 없음), 이스케이프 0, 중복 키 0

## 컬럼 구성 표 (경로 패턴별, 원본 컬럼명 그대로)

| 원본 컬럼명/경로 패턴 | 자료형·중첩 | 출현 수 | 빈 값 수 | 원문 예시 | 예시 위치 |
|---|---|---|---|---|---|
| `(root)` | object | 1 | 0 | (컨테이너) | `—` |
| `/version` | string | 1 | 0 | 1.1 | `/version` |
| `/updated` | string | 1 | 0 | 2026-04-05 | `/updated` |
| `/description` | string | 1 | 0 | 시술 전 체크리스트. 카테고리별 universal + category-specific 확인 항목 | `/description` |
| `/universal_checks` | array(자식 12) | 1 | 0 | (컨테이너) | `—` |
| `/universal_checks/*` | object | 12 | 0 | (컨테이너) | `—` |
| `/universal_checks/*/id` | string | 12 | 0 | allergies | `/universal_checks/0/id` |
| `/universal_checks/*/label` | string | 12 | 0 | 알레르기 병력 | `/universal_checks/0/label` |
| `/universal_checks/*/type` | string | 12 | 0 | must_check | `/universal_checks/0/type` |
| `/universal_checks/*/description` | string | 12 | 0 | 약물/식품/라텍스 알레르기 | `/universal_checks/0/description` |
| `/category_specific` | array | 1 | 0 | (컨테이너) | `—` |
| `/category_specific/*` | object | 17 | 0 | (컨테이너) | `—` |
| `/category_specific/*/id` | string | 17 | 0 | M1 | `/category_specific/0/id` |
| `/category_specific/*/name` | string | 17 | 0 | 보톡스 | `/category_specific/0/name` |
| `/category_specific/*/checks` | array(자식 10), array(자식 11), array(자식 5), array(자식 6), array(자식 7), array(자식 8), array(자식 9) | 17 | 0 | (컨테이너) | `—` |
| `/category_specific/*/checks/*` | object | 123 | 0 | (컨테이너) | `—` |
| `/category_specific/*/checks/*/label` | string | 123 | 0 | 신경근접합부 질환(중증근무력증 등) 확인 | `/category_specific/0/checks/0/label` |
| `/category_specific/*/checks/*/type` | string | 123 | 0 | absolute_contraindication | `/category_specific/0/checks/0/type` |

### 객체 형태 변형·선택적 필드

- `(root)` 객체 1개 · 키 순서 변형 1종: [version, updated, description, universal_checks, category_specific]
- `/universal_checks/*` 객체 12개 · 키 순서 변형 1종: [id, label, type, description]
- `/category_specific/*` 객체 17개 · 키 순서 변형 1종: [id, name, checks]
- `/category_specific/*/checks/*` 객체 123개 · 키 순서 변형 1종: [label, type]
- 선택적 필드(같은 패턴 객체 중 일부에만 있는 키): 없음 — 같은 패턴의 객체는 모두 같은 키 집합
- 구조 차이(원문 사실): `universal_checks/*` 는 id·label·type·description 4키, `category_specific/*/checks/*` 는 label·type 2키(id·description 없음).

### `type` 값 분포 (코드값 — 뜻은 원문에 정의 없음)

| type 원문 값 | universal_checks | category_specific checks |
|---|---|---|
| `must_check` | 8 | 66 |
| `relative_contraindication` | 1 | 0 |
| `counseling` | 1 | 21 |
| `inform` | 1 | 10 |
| `absolute_contraindication` | 1 | 21 |
| `safety_protocol` | 0 | 5 |

## 구획 목차

| 구획 | 범위 | 소유 노드/말단 | 직접 읽기 | 파일 |
|---|---|---|---|---|
| S00 | 최상위 메타 + 루트/카테고리 배열 컨테이너 | 5/3 | read | [review-part-S00.md](review-part-S00.md) |
| S01 | universal_checks 전체 (12항목) | 61/48 | read | [review-part-S01.md](review-part-S01.md) |
| S02 | category_specific M1–M4 (index 0–3) | 100/64 | read | [review-part-S02.md](review-part-S02.md) |
| S03 | category_specific M5–M8 (index 4–7) | 109/70 | read | [review-part-S03.md](review-part-S03.md) |
| S04 | category_specific M9–M13 (index 8–12) | 116/74 | read | [review-part-S04.md](review-part-S04.md) |
| S05 | category_specific M14–M17 (index 13–16) | 112/72 | read | [review-part-S05.md](review-part-S05.md) |

## 구조화 기록

- `source-map.json` — 모든 노드(컨테이너·말단) Pointer·자료형·원문 값·리터럴 구간(cp/byte)·키 구간·문맥 참조·소유 구획
- `morphology.json` — 분석 설정, 문자열별 kiwi 원시 토큰(form/tag/lemma_tool/구간), 문장 분리, 제외 목록(사유), 필드명 별도, 알려진 오분절
- `expressions.json` — 자동 후보(정규식 일치분만)와 수동 수집 표현(직접 읽기)
- `coverage.json` — 구획별 소유 Pointer 집합·읽기 상태·대응 review 파일
