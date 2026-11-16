# review-part-S00 — 최상위 메타 + 루트/카테고리 배열 컨테이너

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/pre-procedure-checklist.json` (sha256 `0de87bff91f721fe685884025d31749017d44da250492b2db9d49109a61e4086`)
- 직접 읽기 상태: **read** — 루트 키 5개·/version·/updated·/description·/category_specific 컨테이너(자식17) 확인
- 소유 Pointer: ``, `/version`, `/updated`, `/description`, `/category_specific` (정확 일치만: ``, `/category_specific`)
- 공동 참조 문맥(소유 아님): 없음
- 열 구분: **원문 값** 칸은 원본 그대로(가공 없음). 관찰은 아래 별도 절에만 있다. 형태소 열은 kiwi 원시 결과(`form/tag`)이며 도메인 정답이 아니다.

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| JSON Pointer | 원본 컬럼명(key/index) | 자료형 | 원문 값 | 분석 적용 | kiwi 원시 토큰(form/tag) |
|---|---|---|---|---|---|
| `(root)` | `(root)` | object(자식 5) | keys=['version', 'updated', 'description', 'universal_checks', 'category_specific'] | — | — |
| `/version` | `version` | string | 1.1 | excluded | — |
| `/updated` | `updated` | string | 2026-04-05 | excluded | — |
| `/description` | `description` | string | 시술 전 체크리스트. 카테고리별 universal + category-specific 확인 항목 | analyzed | 시술/NNG 전/NNG 체크/NNG 리스트/NNG ./SF 카테고리/NNG 별/XSN universal/SL +/SW category/SL -/SO specific/SL 확인/NNG 항목/NNG |
| `/category_specific` | `category_specific` | array(자식 17) |  | — | — |

## 자동 표현 후보 (정규식 일치분만 — 패턴 밖은 아래 수동 절)

- **AP-MODAL** (1): `/description`[48,50) «확인»

## 수동 수집 표현 (직접 읽기 — 원문 구간)

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 메모 |
|---|---|---|---|---|
| `/description` | [0,10) | 시술 전 체크리스트 | 시점(시술 전), 문서 성격 | 원장 전체의 시점 범위 진술 |
| `/description` | [12,53) | 카테고리별 universal + category-specific 확인 항목 | 구조 진술, 기호(+) | '+' 는 두 구획 이름을 잇는다. README 의 시술 '+' 규칙 적용 대상인지 원문에 없음 |
| `/description` | [30,47) | category-specific | 필드명 대응 | 키는 category_specific(밑줄), 설명문은 하이픈 표기 |

## 잠정 관찰 (원문 아님 — 근거 위치 포함)

- P: `/version` 은 문자열 "1.1"(숫자 아님), `/updated` 는 "2026-04-05" 문자열. 형식 규칙은 원문에 없다.
- P: `/description` 이 말하는 'universal'·'category-specific' 은 실제 키 `universal_checks`·`category_specific` 과 표기가 다르다(밑줄/하이픈, _checks 접미). 구조적 대응은 잠정.
- P: '카테고리'(M1–M17)가 다른 원장의 어떤 분류와 같은지 이 파일 안에서는 정의되지 않는다(이름만 있음).

## 이 구획의 미결 (A=추출/해석 오류, B=원문 정보 부족, C=사용자 결정 필요, K=분석 한계, P=잠정, F=후속, I=원문 불일치)

- **F-S00-1** [deferred] category_specific 의 id(M1–M17)·name 이 어떤 분류 체계를 가리키는지 원문 안에 정의 없음 — 다른 원장과의 연결은 21개 비교 후 과제 — 위치: `/category_specific`

## 알려진 형태소 오분절 (K — 출현별)

- `/description` «체크리스트» → 원시 `체크/NNG 리스트/NNG` — 영향: 외래 복합어가 둘로 나뉨 — 의미 손실은 작음(K)
