# Product Doc Pipeline

## 목적

제품 문서 파이프라인의 목적은 문서를 늘리는 것이 아니라, 날것의 아이디어가 실제 구현 작업으로 내려가는 경로를 고정하는 것이다.

이 문서는 사람이 읽는 제품 문서 작성 규칙이다.

## 적용 범위

이 규칙은 `products/<product>/` 아래의 제품 문서에 적용한다.

```text
products/<product>/
├── README.md
├── log.md
├── 00-baseline/
├── 10-decision/
├── 20-spec/
├── 30-work/
└── 40-architecture/   # optional
```

## 핵심 흐름

제품 문서는 번호 순서대로 구체화된다.

```text
00-baseline
→ 10-decision
→ 20-spec
→ 30-work
→ log.md
```

| 단계 | 역할 |
|---|---|
| `00-baseline/` | 날것 그대로의 아이디어, 요구, 레퍼런스, 문제, 관찰을 모은다 |
| `10-decision/` | baseline의 내용을 이번 제품/스펙에 어떻게 적용할지 결정한다 |
| `20-spec/` | decision을 user flow, state machine, UI/UX, FE, BE 관점 계약으로 구체화한다 |
| `30-work/` | 여러 spec을 조합해 실제 구현 작업, acceptance, 테스트 지시서로 내린다 |
| `40-architecture/` | 여러 spec/work가 공유하는 데이터베이스, 시스템, 배포 구조를 관리한다. optional |
| `log.md` | baseline, decision, spec, work 변경 이력을 제품 단위로 통합 관리한다 |

## 문서별 역할

| 문서 | 역할 | 넣는 것 | 넣지 않는 것 |
|---|---|---|---|
| `README.md` | 제품 전체 map | 현재 상태, 문서 맵, 최근 로그 링크 | 상세 아이디어, 결정 근거, spec 본문, 작업 지시 |
| `log.md` | 제품 통합 변경 로그 | 문서 변경 이력, 상태 변경, 연결 변경 | 단계별 본문 복사 |
| `00-baseline/README.md` | baseline index | 아이디어 목록, 상태, decision 연결 | 결정 내용 본문 |
| `00-baseline/baseline-*.md` | 날것 입력 1건 | 원문, 배경, 중요성, 가능한 방향 | 확정 결정, 구현 지시 |
| `10-decision/README.md` | decision index | 결정 로그, 미결 사항, baseline/spec 연결 | 기능 계약 본문, 작업 계획 |
| `10-decision/decision-*.md` | 결정 1건 | 선택지, 결정, 미결, 영향 범위 | 상세 구현 단계 |
| `20-spec/README.md` | spec index | spec 목록, 상태, decision/work 연결 | work 진행률 상세 |
| `20-spec/spec-*.md` | 기능 계약 1건 | user flow, state machine, UI/UX, FE, BE, API, 데이터 계약, work handoff | PR 계획, 작업 순서, 구현 완료 acceptance, 체크리스트 |
| `30-work/README.md` | work index | work 목록, spec coverage, 상태 | spec 본문 복사 |
| `30-work/work-*.md` | 작업 지시 1건 | scope, 구현 순서, spec 계약에서 파생한 acceptance, 완료 조건, 테스트 | 제품 결정 자체 |
| `40-architecture/README.md` | architecture index | database, system, deploy 진입점 | 단일 work 구현 메모 |
| `40-architecture/database/` | database architecture | ERD, 테이블, 도메인 데이터 구조 | migration/schema 전문 복사 |
| `40-architecture/system/` | system architecture | 시스템 구성요소, 외부 연동, 주요 흐름 | 기능 요구사항 본문 |
| `40-architecture/deploy/` | deploy architecture | 배포 환경, back/front 배포 절차 | 임시 배포 로그 |

작업 종류와 역할/상태 추적 기준은 `context/studio/workflow.md`를 따른다.

## Architecture 문서 원칙

`40-architecture/`는 optional이다.

단일 spec이나 단일 work 안에서 끝나는 구현 메모는 architecture로 올리지 않는다. 여러 spec/work가 반복해서 참조하거나 오래 유지될 구조가 생겼을 때만 `40-architecture/`에 둔다.

기본 전파 방향:

```text
20-spec
→ 40-architecture
→ 30-work
→ code
```

의미:

- spec은 구현의 기준이 되는 제품 계약이다.
- architecture는 spec을 구현하기 위해 여러 작업이 공유해야 하는 장기 구조를 정리한다.
- work는 spec과 architecture를 참고해 실제 작업 지시로 내린다.
- 구현 중 architecture가 바뀌어야 하면 먼저 해당 변경이 spec 계약을 바꾸는지 확인한다.

Architecture에 둔다:

- Mermaid `erDiagram` 기반 ERD
- 테이블 목록과 도메인 데이터 구조
- 세부 도메인 설명
- Mermaid `flowchart` 기반 시스템 아키텍처
- 외부 연동과 주요 시스템 흐름
- backend/frontend 배포 프로세스

Architecture에 두지 않는다:

- 일회성 구현 메모
- PR 작업 순서
- schema/migration 전문 복사
- spec의 기능 요구사항 본문 복사
- 임시 배포 로그

## 매핑 규칙

기본 연결은 아래 방향을 따른다.

```text
BASE-001
→ DEC-001
→ SPEC-001
→ WORK-001
```

- baseline은 decision을 가리킬 수 있다.
- decision은 baseline과 spec을 가리킬 수 있다.
- spec은 decision과 work를 가리킬 수 있다.
- work는 spec을 가리킨다.
- 상위 문서는 하위 문서의 본문을 복사하지 않고 ID와 링크만 둔다.

## Frontmatter 원칙

모든 개별 문서는 YAML frontmatter를 가진다.

공통 필드:

| 필드 | 설명 |
|---|---|
| `type` | `baseline`, `decision`, `spec`, `work` 중 하나 |
| `id` | 제품 안에서 유일한 ID |
| `title` | 사람이 읽는 제목 |
| `status` | 문서 유형별 상태 |
| `created_at` | 생성일 |
| `updated_at` | 마지막 수정일 |
| `tags` | 검색과 분류를 위한 태그 |

권장 공통 필드:

| 필드 | 설명 |
|---|---|
| `product` | 제품 slug. 예: `wine-log` |
| `links` | Obsidian wikilink 기반 연결 목록 |

## 상태 값

### Baseline

| Status | 의미 |
|---|---|
| `raw` | 막 들어온 상태 |
| `reviewing` | 검토 중 |
| `accepted` | decision으로 반영됨 |
| `rejected` | 반영하지 않기로 함 |
| `deferred` | 나중에 다시 보기로 함 |

### Decision

| Status | 의미 |
|---|---|
| `proposed` | 제안됨 |
| `accepted` | 채택됨 |
| `rejected` | 기각됨 |
| `pending` | 결정 대기 |
| `superseded` | 다른 결정으로 대체됨 |

### Spec

| Status | 의미 |
|---|---|
| `draft` | 초안 |
| `ready` | 개발 가능 |
| `in_dev` | 개발 중 |
| `implemented` | 구현됨 |
| `deprecated` | 폐기됨 |

### Work

| Status | 의미 |
|---|---|
| `todo` | 해야 함 |
| `in_progress` | 진행 중 |
| `blocked` | 막힘 |
| `review` | 검토 중 |
| `done` | 완료 |

## Obsidian Graph 규칙

제품 문서는 Obsidian 그래프에서 관계를 볼 수 있어야 한다.

### 원칙

- 문서 관계의 SSOT는 frontmatter의 `links` 필드다.
- Obsidian 그래프 시각화를 위해 `links` 하위 값은 wikilink로 적는다.
- 본문에는 관계 링크를 중복 작성하지 않는다.
- 파일명은 Obsidian 그래프에서 읽기 쉬운 slug를 유지한다.
- 기계 검증용 ID는 frontmatter의 `id`에서 관리한다.

### 파일명과 ID

파일명은 사람이 읽기 쉽게 둔다.

```text
baseline-001-label-scan-idea.md
decision-001-label-analysis-scope.md
spec-001-label-analysis.md
work-001-label-analysis-mvp.md
```

ID는 frontmatter에서 관리한다.

```yaml
id: BASE-001
```

### 공통 links 필드

```yaml
links:
  baselines:
    - "[[baseline-001-label-scan-idea]]"
  decisions:
    - "[[decision-001-label-analysis-scope]]"
  specs:
    - "[[spec-001-label-analysis]]"
  works:
    - "[[work-001-label-analysis-mvp]]"
  related:
    - "[[some-related-note]]"
```

문서 유형별로 필요 없는 배열은 비워둔다.

### 태그 규칙

frontmatter의 `tags`는 아래 패턴을 따른다.

```yaml
tags:
  - product/<product-slug>
  - doc/<doc-type>
  - status/<status>
```

예시:

```yaml
tags:
  - product/wine-log
  - doc/baseline
  - status/raw
```

### 정합성

- `links.decisions` 같은 관계 필드에는 ID 문자열이 아니라 Obsidian wikilink를 둔다.
- pipeline은 wikilink 대상 파일의 frontmatter `id`를 읽어 BASE → DEC → SPEC → WORK 관계를 검증한다.
- 관계 링크는 frontmatter `links`에만 둔다.

## 작업 후 갱신 규칙

문서 작업이 끝나면 아래를 갱신한다.

| 작업 | 반드시 갱신 |
|---|---|
| baseline 추가/수정 | `00-baseline/README.md`, `log.md` |
| decision 추가/수정 | `10-decision/README.md`, 연결된 baseline index, `log.md` |
| spec 추가/수정 | `20-spec/README.md`, 연결된 decision index, `log.md` |
| work 추가/수정 | `30-work/README.md`, spec coverage, `log.md` |
| architecture 추가/수정 | `40-architecture/README.md`, 관련 spec/work link, `log.md` |
| 제품 상태 변경 | 제품 `README.md`, `log.md` |

## 통합 로그 규칙

`log.md`는 제품 단위 통합 로그다.

단계별 디렉토리에 별도 로그를 두지 않는다.

권장 컬럼:

```markdown
| Date | Type | IDs | Summary | Links |
|---|---|---|---|---|
```

권장 `Type`:

- `baseline-add`
- `baseline-change`
- `decision-add`
- `decision-change`
- `spec-add`
- `spec-change`
- `work-add`
- `work-change`
- `architecture-add`
- `architecture-change`
- `status-change`
- `mapping-change`

## AI 작업 후 Hook

AI가 `products/**` 문서를 생성하거나 수정한 뒤에는 `.agent/hooks/product-doc-pipeline.md`의 후처리 절차를 따른다.

hook은 이 문서의 규칙을 기준으로 정합성을 검증하고, 가능한 index/status/log 갱신을 수행한다.

## 한 곳 원칙

- 같은 사실은 한 곳에만 둔다.
- index 문서는 본문을 복사하지 않는다.
- 제품 전체 변경 이력은 `log.md` 하나에만 둔다.
- 현재 우선순위와 전체 운영 상태는 `context/studio/current.md`에 둔다.
- 제품별 상세 작업은 `products/<product>/`에 둔다.
