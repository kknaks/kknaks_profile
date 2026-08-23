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
├── 21-html/           # optional, spec HTML 시안 산출물 (검증 대상 아님)
├── 30-work/
├── 40-architecture/   # optional
├── 60-release/        # optional
├── 70-runbook/        # optional
└── _archive/          # optional, 버전 컷오프 동결본 (검증 대상 아님)
```

`_archive/`는 버전 컷오프 시점에 제품 문서 전체를 동결한 읽기 전용 스냅샷이다. 자세한 규약은 아래 **버전 컷오프 (archive)** 섹션 참고.

## 핵심 흐름

제품 문서는 번호 순서대로 구체화된다.

```text
00-baseline
→ 10-decision
→ 20-spec
→ 30-work
→ 60-release
→ log.md
```

| 단계 | 역할 |
|---|---|
| `00-baseline/` | 날것 그대로의 아이디어, 요구, 레퍼런스, 문제, 관찰을 모은다 |
| `10-decision/` | baseline의 내용을 이번 제품/스펙에 어떻게 적용할지 결정한다 |
| `20-spec/` | decision을 user flow, state machine, UI/UX, FE, BE 관점 계약으로 구체화한다 |
| `21-html/` | spec을 시각화한 baseline HTML 시안을 둔다. `spec-to-html` skill이 생성한다. optional |
| `30-work/` | 여러 spec을 조합해 실제 구현 작업, acceptance, 테스트 지시서로 내린다 |
| `40-architecture/` | 여러 spec/work가 공유하는 데이터베이스, 시스템, 배포 구조를 관리한다. optional |
| `60-release/` | 배포 버전별 요약, 상세 수정 사항, 검증/배포 정보를 관리한다. optional |
| `70-runbook/` | 빌드, 서명, 배포, 심사, 운영 등 반복 실행하는 절차를 관리한다. optional |
| `log.md` | baseline, decision, spec, work 변경 이력을 제품 단위로 통합 관리한다 |

## 문서별 역할

| 문서 | 역할 | 넣는 것 | 넣지 않는 것 |
|---|---|---|---|
| `README.md` | 제품 전체 map | 현재 상태, 문서 맵, 코드 레포 위치(local clone·문서 SoT 경로), 최근 로그 링크 | 상세 아이디어, 결정 근거, spec 본문, 작업 지시 |
| `log.md` | 제품 통합 변경 로그 | 문서 변경 이력, 상태 변경, 연결 변경 | 단계별 본문 복사 |
| `00-baseline/README.md` | baseline index | 아이디어 목록, 상태, decision 연결 | 결정 내용 본문 |
| `00-baseline/baseline-*.md` | 날것 입력 1건 | 원문, 배경, 중요성, 가능한 방향 | 확정 결정, 구현 지시 |
| `10-decision/README.md` | decision index | 결정 로그, 미결 사항, baseline/spec 연결 | 기능 계약 본문, 작업 계획 |
| `10-decision/decision-*.md` | 결정 1건 | 선택지, 결정, 미결, 영향 범위, **근거 개념(`up:` + 「근거 개념」 절)** | 상세 구현 단계, 개념 상세 |
| `20-spec/README.md` | spec index | spec 목록, 상태, decision 연결, 영역별 읽는 순서 | work 진행률 상세, owner, blocker, PR |
| `20-spec/spec-*.md` | 기능 계약 1건 | user flow, state machine, UI/UX, API, 데이터 계약, acceptance criteria | PR 계획, 작업 순서, 구현 완료 체크리스트, 특정 work ID 참조 |
| `30-work/README.md` | work index | Status Board, work 목록, spec coverage, release gate | spec 본문 복사 |
| `30-work/work-*.md` | 작업 지시 1건 | scope, code surface, phase별 실행·검증·완료 증거, rollback | 제품 결정 자체, spec 본문 복사 |
| `40-architecture/README.md` | architecture index | database, system, deploy 진입점 | 단일 work 구현 메모 |
| `40-architecture/database/` | database architecture | ERD, 테이블, 도메인 데이터 구조 | migration/schema 전문 복사 |
| `40-architecture/system/` | system architecture | 시스템 구성요소, 외부 연동, 주요 흐름 | 기능 요구사항 본문 |
| `40-architecture/deploy/` | deploy architecture | 배포 환경, back/front 배포 절차 | 임시 배포 로그 |
| `60-release/README.md` | release index | 버전별 release note 목록, 배포 상태, 링크 | work/spec 상세 본문 복사 |
| `60-release/release-*.md` | release note 1건 | 이번 버전 요약, 상세 수정 사항, 검증, 배포/rollback 정보 | 미완료 작업 지시, 다음 버전 scope |
| `70-runbook/README.md` | runbook index | runbook 목록, area, 상태, 링크 | 절차 본문 복사 |
| `70-runbook/runbook-*.md` | 실행 절차 1건 | 목적, 사전 준비, 절차(명령·단계), 검증, 트러블슈팅 | 배포 환경/타겟 정적 구조, 일회성 실행 로그 |

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

## Release 문서 원칙

`60-release/`는 optional이다.

제품이 실제 배포되거나 외부 사용자에게 설치/사용 가능한 버전을 낼 때 release note를 작성한다.

Release note는 “이번 버전에서 무엇이 달라졌는지”를 사용자와 운영자가 빠르게 확인하는 문서다. spec/work의 상세 구현 지시를 다시 복사하지 않고, 배포된 버전의 결과만 요약한다.

Release에 둔다:

- 버전과 배포 일자
- 이번 버전 요약
- 상세 수정 사항
- breaking change와 migration note
- 검증 결과
- 배포 대상과 artifact/link
- rollback 또는 known issue

Release에 두지 않는다:

- 아직 배포되지 않은 다음 버전 작업 계획
- spec/work 본문 복사
- 미결 제품 결정
- 임시 디버깅 로그 전문

## 버전 컷오프 (archive)

`_archive/`는 optional이다.

제품이 한 버전으로 배포·심사에 나간 시점에 제품 문서 전체(00~70)를 `products/<product>/_archive/vX.Y.Z/`로 **동결**한다. live 문서는 다음 버전 작업으로 계속 바뀌므로, "이 버전에 무엇이 나갔는가"를 트리에서 바로 보려고 스냅샷을 남긴다. release note와는 별개다 — release note는 변경 요약, 컷오프는 문서 전체 동결.

컷오프는 단순 백업이 아니라 **릴리즈 게이트**다. 기본 실행은 `product_doc_pipeline.py --strict --release-gate --product <product>`를 먼저 통과해야 한다. 즉 해당 버전의 spec은 구현 완료 상태여야 하고, 연결된 work는 `done`/`progress: 100`이어야 하며, `30-work/README.md`의 work index와 spec coverage도 완료 상태여야 한다. 개발 중 상태를 그대로 박제해야 하는 특수 상황만 `--no-release-gate`로 우회한다.

규약:

- 동결본은 **읽기 전용**이다. 수정하지 않는다. 갱신은 live 문서에서 하고 다음 컷오프에 반영한다. 스크립트는 컷오프 폴더에 `chmod -R a-w`를 적용한다.
- 동결본 frontmatter는 `status: archived` + `original_status` + `archived_version` + `archived_at`로 마킹하고, `tags`의 `status/*`도 `status/archived`로 바꾼다.
- 동결본 `.md` 파일명과 내부 링크(wikilink·마크다운 상대링크)에 버전 prefix를 단다 (`v1.0.1` → `v1_0_1-`). 동일 basename이 live와 archive에 둘 생기면 Obsidian이 wikilink를 전역 basename으로 모호하게 해석해 **live 링크까지 오염**되므로, prefix로 basename을 유니크하게 만들고 아카이브 내부 링크는 같은 버전 사본을 가리키게 한다 → 과거 버전 그래프가 자기완결적으로 탐색된다.
- 같은 버전 폴더는 덮어쓰지 않는다.
- **현재 트리 상태**를 현재 버전으로 동결한다. 이미 지나간 과거 버전은 live 트리에 없으므로 git tag/commit에서 복원해야 한다.
- 기본은 live 문서를 그대로 둔다. 다음 사이클을 명확히 시작하려면 `--reset-current`를 붙인다. 이 옵션은 archive freeze 후 `30-work/README.md`의 work 행을 비우고, `Spec Coverage`를 `(carried @vX.Y.Z)`/`draft`로 전환하며, 방금 archive에 동결된 live `30-work/work-*.md` 파일을 제거한다. spec/decision/architecture/log는 carry-forward한다.
- 검증기는 `products/` 최상위만 제품으로 순회하고 release/work/runbook 글롭이 모두 비재귀라, 중첩된 `_archive/` 동결본은 **재검증되지 않는다**. 검증기에 재귀/wikilink 검증을 추가할 때는 `_archive/`를 제외한다.

실행은 `version-cutoff` skill(`.agent/scripts/product_version_cutoff.py`)로 한다.

## Release work 원칙 (work_type: release)

출시 준비, 스토어 심사 제출, 심사 대응, 운영 체크는 `30-work/`의 work로 추적하되 frontmatter `work_type: release`로 표시한다. 작업 종류 정의는 `context/studio/workflow.md`를 따른다.

세 문서의 역할을 구분한다.

| 무엇 | 어디 | 성격 |
|---|---|---|
| *어떻게* 제출/배포하나 (재사용 절차·런북) | `40-architecture/deploy/` | 재사용, 버전 무관 |
| *이번* 제출 시도의 체크리스트·제출 기록·심사 결과 | `30-work/` release work | 1회성, 버전별 상태 |
| 출시된 *결과* 요약 | `60-release/` | 사후 결과 노트 |

기본 전파 방향:

```text
30-work (work_type: release)
→ (스토어 심사 통과)
→ 60-release
```

규칙:

- release work 문서는 일반 work 템플릿 대신 `templates/product/30-work/work-release.md`를 쓴다.
- 상태는 일반 Work 상태(todo → in_progress → done)를 그대로 쓴다. 심사 단계(제출/심사중/반려/승인)는 본문 `## 심사 결과` 표에 누적한다.
- 필수 섹션: `## 심사 체크리스트`, `## 제출 기록`, `## 심사 결과`.
- 권장 frontmatter: `work_type: release`, `platform`, `target_version`. `tags`에 `work-type/release`를 추가한다.
- 출시가 끝나면 `60-release/`에 release note를 생성하고 release work의 frontmatter `links.releases`로 연결한다.

## Runbook 문서 원칙

`70-runbook/`은 optional이다.

빌드, 서명, 배포, 스토어 심사 제출, 운영 점검처럼 *반복 실행하는 절차*가 생겼을 때 작성한다. 한 번 하고 마는 일은 runbook으로 올리지 않는다.

`40-architecture/deploy/`와 역할을 구분한다.

| 무엇 | 어디 |
|---|---|
| 배포 *구조/환경* (환경 목록, 타겟, 채널, 서명 주체 — 무엇인지) | `40-architecture/deploy/` |
| 실행 *절차* (명령, 단계, 검증, 트러블슈팅 — 어떻게 하는지) | `70-runbook/` |

규칙:

- runbook 문서는 `templates/product/70-runbook/runbook.md`를 쓴다.
- 필수 섹션: `## 목적`, `## 절차`.
- 권장 섹션: `## 사전 준비`, `## 검증`, `## 트러블슈팅`, `## 관련 파일`.
- 권장 frontmatter: `area`(build/deploy/release/ops 등). 상태는 Runbook 상태(draft/active/deprecated)를 쓴다.
- 배포 환경/타겟 같은 정적 구조는 복사하지 않고 `40-architecture/deploy/`를 링크한다.
- 같은 절차는 한 곳(runbook)에만 둔다. deploy 문서나 work 본문에 절차를 중복하지 않는다.

Runbook에 두지 않는다:

- 배포 환경/타겟 정적 구조
- 일회성 실행 로그
- 제품 결정이나 기능 계약

### Runbook 자산 (assets)

스토어 제출용 스크린샷, 앱 아이콘, 프리뷰 영상 같은 바이너리 자산은 해당 절차 옆 `70-runbook/assets/`에 모은다. `products/`에서 바이너리를 두는 유일한 자리다.

- 구조: `70-runbook/assets/<대상>/...` (예: `assets/appstore/icon/`, `assets/appstore/screenshots/`).
- `70-runbook/assets/README.md`는 **manifest**다. 필요한 자산, 규격, 상태(있음/없음/N/A), 위치를 표로 추적한다.
- 자산은 검증(validator) 대상이 아니다. manifest(markdown)만 정합성 관리한다.
- 관련 runbook은 본문에서 manifest를 링크한다.
- 코드 레포에 이미 있는 자산(앱 아이콘 등)은 필요 시 복사해 모으되, manifest에 원본 위치를 함께 적는다.

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
- spec은 decision/baseline을 가리킬 수 있다.
- work는 spec을 가리킨다.
- SPEC → WORK 추적은 SPEC 본문에 특정 work ID를 박지 않고, work frontmatter `links.specs`와 `30-work/README.md`의 Spec Coverage에서 단방향으로 관리한다.
- 상위 문서는 하위 문서의 본문을 복사하지 않고 ID와 링크만 둔다.

## Frontmatter 원칙

모든 개별 문서는 YAML frontmatter를 가진다.

공통 필드:

| 필드 | 설명 |
|---|---|
| `type` | `baseline`, `decision`, `spec`, `work`, `release`, `runbook` 중 하나 |
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

Work 본문은 phase 단위로 진행을 추적한다. 각 phase의 `- **Status**:` 값은 `TODO`, `IN_PROGRESS`, `DONE`, `BLOCKED`, `SUPERSEDED` 중 하나만 쓴다. 완료 날짜, 검증 로그, caveat는 상태 줄에 붙이지 않고 같은 phase의 `완료 증거`에 적는다.

Frontmatter `status`는 phase 상태와 동기화한다.

| Phase 상태 | Work frontmatter status |
|---|---|
| 전 phase가 `TODO` | `todo` |
| 하나라도 `IN_PROGRESS` 또는 `DONE` | `in_progress` |
| 막힌 phase가 있음 | `blocked` |
| 모든 phase가 `DONE` 또는 `SUPERSEDED` | `done` |

`30-work/README.md`의 Status Board는 실행 상태의 owning view다. Work 본문을 수정해 상태, owner, blocker, next가 바뀌면 Status Board / Work List / Spec Coverage도 함께 갱신한다.

### Release

| Status | 의미 |
|---|---|
| `draft` | 배포 노트 초안 |
| `ready` | 배포 전 검토 완료 |
| `released` | 배포 완료 |
| `failed` | 배포 실패 |
| `rolled_back` | 배포 후 rollback 완료 |

### Runbook

| Status | 의미 |
|---|---|
| `draft` | 작성 중 |
| `active` | 현재 유효, 따라 실행 가능 |
| `deprecated` | 더 이상 쓰지 않음 (사유 비고) |

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
release-001-v1-0-0.md
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
  releases:
    - "[[release-001-v1-0-0]]"
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
- **`decision`은 근거 개념 검토 흔적을 남긴다** — frontmatter `up:` 키와 본문 「근거 개념」 절.
  **결론이 「없음」이어도 통과한다**(`up: []` + `없음 — 사유` 한 줄). 요구하는 것은 개념을
  반드시 잇는 것이 아니라 **검토했다는 사실이 문서에 남는 것**이다. 값·범위·UX 결정처럼
  기댈 개념이 없는 문서가 실제로 27건이고, 그것을 억지로 이으면 계보가 거짓이 된다.
  판단 기준은 `rules/knowledge-note-pipeline.md`의 「결정을 쓰다 새 개념이 나오면」.
  **개념이 필요하면 그 결정을 쓰는 쪽이 같은 턴에 만든다** — 에이전트가 결정을 쓰면
  에이전트가 `resources/source/` + `resources/concept/` 까지 만들어 잇는다.
  `product_doc_pipeline.py`가 error로 막고, pre-commit이 `products/**` 변경마다 그것을 부른다.
- **`spec`의 `links.works`는 비워 둔다.** SPEC → WORK 추적은 위 「문서 관계」의 단방향
  규정대로 work의 `links.specs`가 소유하고, spec 중심의 목록은 `30-work/README.md`의
  Spec Coverage가 **derived view**로 만든다. 원본에 복사해 두면 WP가 늘 때마다 두 곳을
  맞춰야 하고 반드시 어긋난다(「한 곳 원칙」). `product_doc_pipeline.py`가 error로 막는다.

## 작업 후 갱신 규칙

문서 작업이 끝나면 아래를 갱신한다.

| 작업 | 반드시 갱신 |
|---|---|
| baseline 추가/수정 | `00-baseline/README.md`, `log.md` |
| decision 추가/수정 | `10-decision/README.md`, 연결된 baseline index, `log.md`, **「근거 개념」 절 + `up:`** |
| spec 추가/수정 | `20-spec/README.md`, 연결된 decision index, `log.md` |
| spec HTML 시안 추가/수정 | `log.md` |
| work 추가/수정 | `30-work/README.md`, spec coverage, `log.md` |
| architecture 추가/수정 | `40-architecture/README.md`, 관련 spec/work link, `log.md` |
| release 추가/수정 | `60-release/README.md`, 제품 `README.md`, `log.md` |
| runbook 추가/수정 | `70-runbook/README.md`, 관련 deploy/work link, `log.md` |
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
- `spec-html-add`
- `spec-html-change`
- `work-add`
- `work-change`
- `architecture-add`
- `architecture-change`
- `release-add`
- `release-change`
- `runbook-add`
- `runbook-change`
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
