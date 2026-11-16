# treatment-optimization.json — 1차 조사 (읽기용 목차)

**상태**: 1차 범위 — 구획 직접 읽기 14/14 · 기계 검증은 [validation.md](./validation.md) · **원장 전체 완료 아님** — 미결은 [issues.md](./issues.md).

> 이 문서와 review-part-*.md 는 **원문 대응**(자동 생성 표)과 **잠정 관찰**(직접 읽기)을 다른 칸·절로 나눈다. 공통 개념 ID·동의어 병합·부위 체계·관계 방향·적용 조건은 정하지 않았다(1차 범위 밖). 최적화 추천 문구를 확정 관계·임상 사실로 승인하지 않는다.

## 0. 원본과 기록 위치

| 항목 | 값 |
|---|---|
| 원본 | `orchestration/work/phub-recommend/bronze/phub-ledger/treatment-optimization.json` |
| 크기 | 22,887 bytes · 14,718 code points · UTF-8 · BOM 없음 · 개행 0 · 백슬래시 0 · BMP 밖 0 |
| sha256 | `07b9ebe0a843280b4eef9487590951932192435ea46284aba425338ab9d9767b` (원장 폴더 HASHES.txt 접두 `07b9ebe0a843280b` 와 일치) |
| 구조·값 | [source-map.json](./source-map.json) — 노드 691 · 키 출현 388 · 필드명 41종 · 중복 키 0 |
| 형태소 | [morphology.json](./morphology.json) — 문자열 455 중 분석 413 / 제외 42 · 비문자열 말단 36 · 필드명 41 · 토큰 3,025 · 알려진 오분절 출현 77 |
| 복합 표현 | [expressions.json](./expressions.json) — 전체 1,758 (자동 정규식 1,114 · 자동 절 231 · 직접 읽기 수동 413) · 자동 오탐 표시 14 · 수식·부정 토큰 점검 206 (미검토 0) |
| 구획·범위 | [coverage.json](./coverage.json) · 진행 기록 [progress.md](./progress.md) |
| 미결 | [issues.md](./issues.md) |
| 검증 | [validation.md](./validation.md) · [verify.py](./verify.py) |
| 재현 | [build.py](./build.py) · 직접 읽기 기록 `manual/seg-00.json`~`seg-13.json` · 오분절 기록 `manual/segmentation-review.json` · 표현 검토 `manual/expression-review.json` · 전역 미결 `manual/global-issues.json` |

구간 기준: source-map 의 `span` 은 파일 전체 디코딩 텍스트의 코드 포인트 `[start,end)`(문자열은 따옴표 포함), `value_span` 은 따옴표 제외. morphology·expressions 의 `start/end`·`span` 은 해당 값 문자열 기준. 바이트 구간은 `byte_span`. 이 원장은 이스케이프 0 이라 JSON 리터럴 내부와 디코딩 문자열이 같다(검증됨).

## 1. 구획 목차와 읽기 상태

| 구획 | 범위 | 소유 말단 | 기계 추출 | 직접 읽기 | 문서 |
|---|---|---|---|---|---|
| SEG-00 | `/(root, 상위 스칼라·optimization_principles·네 블록 컨테이너 자체)` (상위 메타·원칙) | 7 | done | direct_read_done | [review-part-1.md](./review-part-1.md#seg-00) |
| SEG-01 | `/by_concern/0/**` (by_concern/0) | 33 | done | direct_read_done | [review-part-1.md](./review-part-1.md#seg-01) |
| SEG-02 | `/by_concern/1/**` (by_concern/1) | 33 | done | direct_read_done | [review-part-1.md](./review-part-1.md#seg-02) |
| SEG-03 | `/by_concern/2/**` (by_concern/2) | 32 | done | direct_read_done | [review-part-1.md](./review-part-1.md#seg-03) |
| SEG-04 | `/by_concern/3/**` (by_concern/3) | 36 | done | direct_read_done | [review-part-1.md](./review-part-1.md#seg-04) |
| SEG-05 | `/by_concern/4/**` (by_concern/4) | 37 | done | direct_read_done | [review-part-2.md](./review-part-2.md#seg-05) |
| SEG-06 | `/by_concern/5/**` (by_concern/5) | 37 | done | direct_read_done | [review-part-2.md](./review-part-2.md#seg-06) |
| SEG-07 | `/by_concern/6/**` (by_concern/6) | 30 | done | direct_read_done | [review-part-2.md](./review-part-2.md#seg-07) |
| SEG-08 | `/by_concern/7/**` (by_concern/7) | 34 | done | direct_read_done | [review-part-2.md](./review-part-2.md#seg-08) |
| SEG-09 | `/by_age_group/**` (by_age_group 전체) | 58 | done | direct_read_done | [review-part-3.md](./review-part-3.md#seg-09) |
| SEG-10 | `/combination_rules/**` (combination_rules 전체) | 40 | done | direct_read_done | [review-part-3.md](./review-part-3.md#seg-10) |
| SEG-11 | `/annual_plans/0/**` (annual_plans/0) | 40 | done | direct_read_done | [review-part-4.md](./review-part-4.md#seg-11) |
| SEG-12 | `/annual_plans/1/**` (annual_plans/1) | 38 | done | direct_read_done | [review-part-4.md](./review-part-4.md#seg-12) |
| SEG-13 | `/annual_plans/2/**` (annual_plans/2) | 47 | done | direct_read_done | [review-part-4.md](./review-part-4.md#seg-13) |

읽기 방식: 각 구획을 원문 순서대로 화면에 펼쳐 전 필드·전 배열 원소를 직접 읽고, 읽은 즉시 `manual/seg-XX.json` 에 관찰·수동 구절·미결을 저장했다. 이후 형태소 토큰 전체와 자동 후보·미덮임 어절을 원문과 나란히 다시 대조했다([validation.md](./validation.md) §3). 같은 에이전트의 관점 바꾼 재읽기이며 독립 검토자가 아니다.

## 2. 컬럼 구성 표 (자동 생성 — 원본 컬럼명·경로 패턴 그대로)

배열 인덱스는 `*` 로 묶었다. 같은 패턴이라도 자료형·빈 값 변형은 따로 행을 둔다. 「존재 범위」 가 전체보다 작으면 선택적 필드다.

| 원본 컬럼명 / 경로 패턴 | 자료형·변형 | 중첩 구조 | 출현 수 | 존재 범위 | 원문 예시 (첫 출현) | 예시 Pointer |
|---|---|---|---|---|---|---|
| `/version` | string | 말단 | 1 | 1/1 객체 | "1.4" | `/version` |
| `/updated` | string | 말단 | 1 | 1/1 객체 | "2026-07-26" | `/updated` |
| `/consensus_method` | string | 말단 | 1 | 1/1 객체 | "3-AI Expert Panel Consensus (Perplexity+Gemini+Claude)" | `/consensus_method` |
| `/optimization_principles` | array | 배열 길이 4 | 1 | 1/1 객체 | (컨테이너) | `/optimization_principles` |
| `/optimization_principles/*` | string | 말단 | 4 |  | "안전성 우선 (Do No Harm)" | `/optimization_principles/0` |
| `/by_concern` | array | 배열 길이 8 | 1 | 1/1 객체 | (컨테이너) | `/by_concern` |
| `/by_concern/*` | object | 객체 키: `concern`, `concern_en`, `icon`, `severity_levels` | 8 |  | (컨테이너) | `/by_concern/0` |
| `/by_concern/*/concern` | string | 말단 | 8 | 8/8 객체 | "주름 개선" | `/by_concern/0/concern` |
| `/by_concern/*/concern_en` | string | 말단 | 8 | 8/8 객체 | "Wrinkle Reduction" | `/by_concern/0/concern_en` |
| `/by_concern/*/icon` | string | 말단 | 8 | 8/8 객체 | "wrinkle" | `/by_concern/0/icon` |
| `/by_concern/*/severity_levels` | array | 배열 길이 3 | 8 | 8/8 객체 | (컨테이너) | `/by_concern/0/severity_levels` |
| `/by_concern/*/severity_levels/*` | object | 객체 키: `level`, `optimal_combo`, `sequence`, `rationale`, `expected_sessions`, `total_duration`, `evidence_level`, `contraindicated_combos` | 24 |  | (컨테이너) | `/by_concern/0/severity_levels/0` |
| `/by_concern/*/severity_levels/*/level` | string | 말단 | 24 | 24/24 객체 | "경미 (fine lines)" | `/by_concern/0/severity_levels/0/level` |
| `/by_concern/*/severity_levels/*/optimal_combo` | array | 배열 길이 1~5 | 24 | 24/24 객체 | (컨테이너) | `/by_concern/0/severity_levels/0/optimal_combo` |
| `/by_concern/*/severity_levels/*/optimal_combo/*` | string | 말단 | 74 |  | "레이저토닝" | `/by_concern/0/severity_levels/0/optimal_combo/0` |
| `/by_concern/*/severity_levels/*/sequence` | string | 말단 | 24 | 24/24 객체 | "토닝 먼저 → 2주 후 스킨부스터" | `/by_concern/0/severity_levels/0/sequence` |
| `/by_concern/*/severity_levels/*/rationale` | string | 말단 | 24 | 24/24 객체 | "토닝으로 표피 리뉴얼 후 스킨부스터로 진피 재생" | `/by_concern/0/severity_levels/0/rationale` |
| `/by_concern/*/severity_levels/*/expected_sessions` | string | 말단 | 24 | 24/24 객체 | "토닝 5-10회 + 스킨부스터 3회" | `/by_concern/0/severity_levels/0/expected_sessions` |
| `/by_concern/*/severity_levels/*/total_duration` | string | 말단 | 24 | 24/24 객체 | "3-6개월" | `/by_concern/0/severity_levels/0/total_duration` |
| `/by_concern/*/severity_levels/*/evidence_level` | string | 말단 | 24 | 24/24 객체 | "moderate" | `/by_concern/0/severity_levels/0/evidence_level` |
| `/by_concern/*/severity_levels/*/contraindicated_combos` | empty_array | 배열 길이 0 | 11 | 24/24 객체 | [] | `/by_concern/0/severity_levels/0/contraindicated_combos` |
| `/by_concern/*/severity_levels/*/contraindicated_combos` | array | 배열 길이 1~2 | 13 | 24/24 객체 | (컨테이너) | `/by_concern/0/severity_levels/2/contraindicated_combos` |
| `/by_concern/*/severity_levels/*/contraindicated_combos/*` | string | 말단 | 17 |  | "HA 필러 후 14일 이내 RF/HIFU 금지" | `/by_concern/0/severity_levels/2/contraindicated_combos/0` |
| `/by_concern/*/severity_levels/*/caveats` | array | 배열 길이 2 | 1 | 1/24 객체 (선택적 필드) | (컨테이너) | `/by_concern/3/severity_levels/2/caveats` |
| `/by_concern/*/severity_levels/*/caveats/*` | string | 말단 | 2 |  | "엑소좀: 국내외 미승인 — 美 FDA 미용·치료 목적 승인 0건(경고서한·집행 확대), 韓 MFDS는 2025-01-21부터 화장품 광고 내 'exosome' …(전체는 해당 구획) | `/by_concern/3/severity_levels/2/caveats/0` |
| `/by_age_group` | array | 배열 길이 4 | 1 | 1/1 객체 | (컨테이너) | `/by_age_group` |
| `/by_age_group/*` | object | 객체 키: `age`, `primary_concerns`, `recommended_base`, `avoid`, `maintenance`, `annual_focus` | 4 |  | (컨테이너) | `/by_age_group/0` |
| `/by_age_group/*/age` | string | 말단 | 4 | 4/4 객체 | "20대" | `/by_age_group/0/age` |
| `/by_age_group/*/primary_concerns` | array | 배열 길이 4~5 | 4 | 4/4 객체 | (컨테이너) | `/by_age_group/0/primary_concerns` |
| `/by_age_group/*/primary_concerns/*` | string | 말단 | 17 |  | "여드름/흉터" | `/by_age_group/0/primary_concerns/0` |
| `/by_age_group/*/recommended_base` | array | 배열 길이 4~5 | 4 | 4/4 객체 | (컨테이너) | `/by_age_group/0/recommended_base` |
| `/by_age_group/*/recommended_base/*` | string | 말단 | 17 |  | "스킨부스터" | `/by_age_group/0/recommended_base/0` |
| `/by_age_group/*/avoid` | array | 배열 길이 1~2 | 4 | 4/4 객체 | (컨테이너) | `/by_age_group/0/avoid` |
| `/by_age_group/*/avoid/*` | string | 말단 | 6 |  | "과도한 필러 (자연스러운 노화 중요)" | `/by_age_group/0/avoid/0` |
| `/by_age_group/*/maintenance` | string | 말단 | 4 | 4/4 객체 | "토닝 월 1-2회, 스킨부스터 분기 1회, 필링 월 1회" | `/by_age_group/0/maintenance` |
| `/by_age_group/*/annual_focus` | string | 말단 | 4 | 4/4 객체 | "피부 기초 관리, 여드름/흉터 집중 치료, 자외선 차단 습관화" | `/by_age_group/0/annual_focus` |
| `/by_age_group/*/upgrade` | array | 배열 길이 1~2 | 3 | 3/4 객체 (선택적 필드) | (컨테이너) | `/by_age_group/1/upgrade` |
| `/by_age_group/*/upgrade/*` | string | 말단 | 5 |  | "바이오스티뮬레이터 (콜라겐 예방적 투자)" | `/by_age_group/1/upgrade/0` |
| `/by_age_group/*/note` | string | 말단 | 1 | 1/4 객체 (선택적 필드) | "수술(페이스리프트) 대안 또는 보완으로 비수술 조합. 전체적 조화 중시" | `/by_age_group/3/note` |
| `/combination_rules` | array | 배열 길이 8 | 1 | 1/1 객체 | (컨테이너) | `/combination_rules` |
| `/combination_rules/*` | object | 객체 키: `rule`, `detail`, `evidence`, `consensus`, `priority` | 8 |  | (컨테이너) | `/combination_rules/0` |
| `/combination_rules/*/rule` | string | 말단 | 8 | 8/8 객체 | "열시술 → 주사 순서" | `/combination_rules/0/rule` |
| `/combination_rules/*/detail` | string | 말단 | 8 | 8/8 객체 | "보톡스와 HIFU/RF 열시술은 당일 시술 가능하나 웬만하면 열시술을 먼저 시행. MFU/HIFU는 보톡스 주입 후 2주 이내 효력을 감소시킬 수 있어 HIFU…(전체는 해당 구획) | `/combination_rules/0/detail` |
| `/combination_rules/*/evidence` | string | 말단 | 8 | 8/8 객체 | "MFU-보툴리눔독소 진피내 주입 RCT (J Cosmet Dermatol, PMC11945533); HIFU-HA 필러 열분해 연구(2024); 보툴리눔독소 당…(전체는 해당 구획) | `/combination_rules/0/evidence` |
| `/combination_rules/*/consensus` | string | 말단 | 8 | 8/8 객체 | "근거 기반 임상 권고" | `/combination_rules/0/consensus` |
| `/combination_rules/*/priority` | string | 말단 | 8 | 8/8 객체 | "moderate" | `/combination_rules/0/priority` |
| `/annual_plans` | array | 배열 길이 3 | 1 | 1/1 객체 | (컨테이너) | `/annual_plans` |
| `/annual_plans/*` | object | 객체 키: `plan_name`, `age_group`, `annual_budget_range`, `focus`, `schedule` | 3 |  | (컨테이너) | `/annual_plans/0` |
| `/annual_plans/*/plan_name` | string | 말단 | 3 | 3/3 객체 | "20대 피부관리 베이직 플랜" | `/annual_plans/0/plan_name` |
| `/annual_plans/*/age_group` | string | 말단 | 3 | 3/3 객체 | "20대" | `/annual_plans/0/age_group` |
| `/annual_plans/*/annual_budget_range` | string | 말단 | 3 | 3/3 객체 | "100-250만원" | `/annual_plans/0/annual_budget_range` |
| `/annual_plans/*/focus` | string | 말단 | 3 | 3/3 객체 | "피부 기초 관리, 여드름/흉터 개선, 모공/피부결 관리" | `/annual_plans/0/focus` |
| `/annual_plans/*/schedule` | array | 배열 길이 12 | 3 | 3/3 객체 | (컨테이너) | `/annual_plans/0/schedule` |
| `/annual_plans/*/schedule/*` | object | 객체 키: `month`, `procedures` | 36 |  | (컨테이너) | `/annual_plans/0/schedule/0` |
| `/annual_plans/*/schedule/*/month` | integer | 말단 | 36 | 36/36 객체 | 1 | `/annual_plans/0/schedule/0/month` |
| `/annual_plans/*/schedule/*/procedures` | array | 배열 길이 1~3 | 36 | 36/36 객체 | (컨테이너) | `/annual_plans/0/schedule/0/procedures` |
| `/annual_plans/*/schedule/*/procedures/*` | string | 말단 | 77 |  | "토닝 4회" | `/annual_plans/0/schedule/0/procedures/0` |

### 구조 관찰 (잠정 — 원문 칸과 분리)

- 상위 8키: 스칼라 3(`version`·`updated`·`consensus_method`) + 배열 5(`optimization_principles` 문자열 4 · `by_concern` 객체 8 · `by_age_group` 객체 4 · `combination_rules` 객체 8 · `annual_plans` 객체 3).
- `by_concern/*/severity_levels` 는 모든 고민에서 길이 3(경미·중등도·중증 순). 단계 객체 8필드가 기본이고 `caveats` 는 `/by_concern/3/severity_levels/2` 에만 있다.
- `by_age_group` 의 `upgrade` 는 3/4, `note` 는 1/4 객체에만 있다. `annual_plans/*/schedule` 은 모두 12개월, `month` 는 정수 1~12 오름차순, `procedures` 길이 1~3.
- `contraindicated_combos` 빈 배열 `[]` 은 빈 값 변형 행으로 따로 셌다. 빈 문자열·null·빈 객체는 없다.
- 원장 안에서 서로 다른 블록이 같은 대상을 다른 표기로 부른다(예: 「HIFU(슈링크/울쎄라)」/「HIFU(울쎄라/슈링크)」/「울쎄라 HIFU」). 연결·병합은 하지 않았다(issues F).

## 3. 형태소·표현 수집 범위 (자동과 직접의 구분)

- 자동: 구조 열거·Pointer·구간, Kiwi 형태소 분석(분석 대상 전체 값), 정규식 후보(R01~R20 실제 일치분), 구두점 기준 절 분할, 수동 구절 위치 찾기, 수식·부정 토큰의 수동 표현 포괄 점검.
- 직접: 14구획 원문 통독과 관찰, 수동 구절 수집(패턴 밖 형용사·부사·회피/권고·깊이·속도·근사·수치단위·「후/시」 조건 포함), 토큰 전체 열람 후 오분절 출현 기록, 자동 후보 열람 후 오탐 표시, 수식·부정 토큰 중 수동 구절 밖 토큰의 개별 검토.
- 정규식 후보는 패턴 일치분뿐이다. 수동 구절은 직접 읽기에서 적은 것이며, 이 둘을 합쳐도 원문 전체의 의미 해석이 아니다. 대표 표현으로 모든 복합 표현을 덮었다고 주장하지 않는다 — 덮이지 않은 어절 목록은 expressions.json `uncovered_eojeol`.
- 다국어: 한국어 외 라틴(영어 약어·문헌명·원어 괄호)·한자(美·韓) 구간이 있다. Kiwi 는 이를 SL/SH 토큰으로만 나누며 영어 형태소·기본형은 없다(K-02). 원문은 그대로 보존했다.

