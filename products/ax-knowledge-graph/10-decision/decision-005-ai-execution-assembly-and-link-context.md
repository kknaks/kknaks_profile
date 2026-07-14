---
type: decision
id: AXKG-DEC-005
title: "AI 실행 파이프라인 계약: 3자 조립·연결 후보 컨텍스트·MVP 문서화 범위 확정"
status: accepted
product: ax-knowledge-graph
created_at: 2026-07-07
updated_at: 2026-07-10
tags:
  - product/ax-knowledge-graph
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-001-para-pipeline-and-approval-gates|AXKG-DEC-001]]"
    - "[[decision-002-markdown-sot-postgres-storage|AXKG-DEC-002]]"
    - "[[decision-003-graph-rag-chat-and-default-claude|AXKG-DEC-003]]"
    - "[[decision-004-mvp-defaults-and-scope|AXKG-DEC-004]]"
  specs:
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-005-document-link-graph-contract|AXKG-SPEC-005]]"
    - "[[spec-009-prompt-dynamic-management|AXKG-SPEC-009]]"
    - "[[spec-010-document-template-management|AXKG-SPEC-010]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
  works: []
  releases: []
  related: []
---

# AI 실행 파이프라인 계약: 3자 조립·연결 후보 컨텍스트·MVP 문서화 범위 확정

구현 착수 전 gap 리뷰(2026-07-07)에서 확인된 blocker를 닫는 결정이다.

## Decision

- **연결 후보 입력 컨텍스트(2단 하이브리드)**: 문서화 게이트(③) 초안 AI가 기존 그래프에서 연결 후보를 만들 때의 입력은 두 단으로 구성한다.
  1. Graph RAG retriever(AXKG-DEC-003의 keyword score + edge distance)를 재사용해 관련 기존 문서 top-N 후보를 추출한다.
  2. documents index 경량 스냅샷(`stem`·`aliases`·`title`·`document_type`)을 항상 함께 주입해, AI가 생성하는 wikilink가 유효한 stem/alias만 가리키게 한다.
  - 외부 그래프 도구(Graphify 등)는 제품 서빙 경로에 도입하지 않는다. Markdown→PostgreSQL 캐시(AXKG-DEC-002)가 유일한 그래프 원천이다. Graphify류 도구의 배치 enrichment 활용은 post-MVP 검토 항목으로 남긴다.
- **실행 입력 3원천의 주체** (2026-07-08 개정, AXKG-WORK-002 Phase 3 라이브 e2e): AI 실행 입력은 소유 주체가 다른 3원천으로 나뉜다.
  1. **방법·배경 지침**은 worker 이미지에 내장된 프로젝트 컨텍스트(진입 `CLAUDE.md → agent.md → context/`)가 담당하고, claude가 실행 작업 디렉토리(`WORK_DIR`)에서 스스로 읽는다 — api는 로드·주입하지 않는다.
  2. **DB 아티팩트**(활성 프롬프트=작업 지시, output_schema, ③ 활성 템플릿)는 api가 DB에서 로드해 submit으로 전달하고 `prompt_version_id`(+③ `template_version_id`)를 스냅샷한다. 템플릿 바인딩은 `ai_task_definitions.template_key`, 사용 버전은 `ai_tasks.template_version_id`.
  3. **런타임 데이터**(① `SourceMaterial` 원문, ③ 연결 후보 컨텍스트)는 api가 런타임 상태에서 구성해 submit으로 전달한다.
  - 개정 전 결정은 "api가 지침까지 프롬프트 한 방에 인라인 조립(`template → prompt → output_schema`)하고 claude엔 프로젝트를 주지 않는" 모델이었다. 프로젝트 컨텍스트는 배포 시 마운트(git pull 런타임 의존)가 아니라 **빌드 시점 이미지 내장**으로 고정한다. 요약 작업용 프로젝트 컨텍스트는 코드레포 `apps/worker/workspace/`에 둔다(profile-be 코드 소관, 병렬 진행).
- **가이드/프롬프트 경계 재정렬** (2026-07-09 개정, PLAN-009-T-007): 위 원천 1의 "방법·배경 지침"을 역할 축으로 재분해한다 — **가이드(원천 1, worker)** = 자료·대상의 정의/정책/판단 규칙(what the material IS, PARA 경계 등), **프롬프트(원천 2, DB)** = 작성 방법(이 실행을 어떻게 작성할지 — 본문 선별·톤·밀도·출력 작성 규율). 종전에 "how는 프로젝트 컨텍스트가 담당"이라던 경계를 뒤집어, 자주 튜닝하는 작성 방법(how)은 DB 프롬프트(즉시 반영)에 두고 worker 가이드에는 안정적 정의·규칙만 남긴다. 3층 taxonomy(가이드/프롬프트/템플릿·스키마)와 경계 테스트의 제품 전체 SSOT는 AXKG-SPEC-011 §4 Layer Taxonomy다. 실제 worker `context/*.md` ↔ DB 프롬프트 코드 재분할은 후속 단계(profile-be 발주 예정)이며, 이 결정은 taxonomy·경계까지만 확정한다.
- **output_schema 경계**: `output_schema`는 게이트 payload envelope(`classification.v1`/`documentation.v1`, AXKG-SPEC-002)의 form/구조 필드 내부만 관장한다. envelope 자체는 코드 고정 계약이다.
- **output_schema 표현 형식**: JSON Schema로 확정한다. 백엔드가 FastAPI/Python(Pydantic ↔ JSON Schema 상호변환)이고 AI provider structured output이 JSON Schema 기반이므로 대안이 없다.
- **AI 실행 파이프라인 spec 신설**: 4개 AI 스테이지(①요약 ②분류 ③문서초안 ④Graph RAG chat)의 공통 실행 계약 — 입력 컨텍스트 구성, 3자 조립, 구조화 출력 파싱·검증, 실패→`ai_tasks` 상태 매핑, 콘텐츠 수집 — 은 AXKG-SPEC-011이 SSOT다. 요약 AI(①)의 실행 계약(AXKG-SPEC-003과 AXKG-SPEC-001 사이에서 소관이 비어 있던 부분)은 SPEC-011 소관으로 확정한다.
- **project destination 문서화 MVP 포함**: project destination의 product 문서(baseline 후보) 초안 생성을 MVP에 포함한다. AXKG-SPEC-010의 템플릿 MVP scope를 `reference`·`permanent`·`project_baseline` 3종으로 확장한다.
- **SPEC-009·010 채택 근거 소급 부여**: 프롬프트·템플릿의 DB 동적 관리(AXKG-SPEC-009/010)는 이 결정으로 채택을 승인한다. AXKG-DEC-004의 "reference note 양식은 별도 template directory를 만들지 않고 문서 링크/frontmatter spec에 포함한다" 항목은 이 결정이 대체한다(supersede) — 파일 template directory를 만들지 않는다는 원칙은 유지하되, 문서 뼈대는 PostgreSQL 템플릿(AXKG-SPEC-010)에서 동적 관리하고 링크/frontmatter 계약의 SSOT는 여전히 AXKG-SPEC-005다.

### 출력양식·저장·버전·문서 lifecycle 정합 (2026-07-09 개정, PLAN-009-T-009)

T-007/008이 세운 3층 taxonomy에서 "출력 양식 층"과 "저장 방식"·"버전 관리"의 일관성이 비어 있어 아래 4개를 정합한다. 스펙 문서만 정정하며 코드는 미착수(재분할·마이그레이션 세부는 후속 발주).

- **A. 출력 양식 층 — 템플릿 ≠ output_schema, 템플릿은 문서화③ 전용**: "출력 양식" 층은 **서로 다른 두 아티팩트**로 구현된다. (1) `output_schema` = 출력 JSON의 **필드 구조(shape)만**(`title`/`summary`/`keywords`/`body_markdown:string` 등 — 작다), (2) **템플릿** = md 산출의 **양식(뼈대)**로 **별도 아티팩트**이며 조립 시 프롬프트에 주입한다(output_schema에 넣지 않는다 — 넣으면 응답 스키마가 비대해진다). 이 두 아티팩트 구분은 유지한다. 단 **템플릿은 문서화③ 전용**이다 — reference/permanent/project_baseline 문서 뼈대. **요약①은 원문(출처)의 자체 구조를 따라가는 적응형 출력**이라(강연이면 강연자소개→목차→주제, 기사면 기사 구조) 고정 뼈대(템플릿)가 맞지 않고 씌우면 현재의 좋은 품질을 오히려 해치므로 템플릿을 두지 않는다. 요약 md의 형식 규약(원문 구조 추종·인용·엔티티 볼드·불확실은 "출처 미상" 정직 표기)은 **프롬프트(작성 방법)**가 담고, `body_markdown`은 output_schema 필드로 출력된다(요약은 md 본문을 출력함 — 템플릿이 없을 뿐). 분류②·채팅④는 md 산출이 없어 템플릿 없이 `output_schema`만 갖는다. 출력양식 층/taxonomy SSOT는 AXKG-SPEC-011 §4 Layer Taxonomy다. **(2026-07-09 PLAN-009-T-011 재정정)** 이 결정이 앞서 "요약①도 템플릿을 가진다(md 산출 스테이지 보편화)"로 본 부분은 폐기한다 — 실제 라이브 요약 출력이 적응형임을 확인해 되돌린 것이며, B/C/D는 그대로 유지한다.
- **B. 저장은 직교 축**: 임시(draft: 요약 payload·게이트 revision)는 **DB(JSONB)**, 확정 문서는 **.md 파일(markdown_root)**에 둔다(현 구조 유지, 명시만 추가). 이 저장 축은 템플릿 유무·lifecycle과 **무관(직교)**하다 — "템플릿이 없어서 DB" 같은 잘못된 결합을 스펙에서 끊는다.
- **C. 버전 박제(immutable versioning) 전 단계 일관**: 피드백 재생성은 덮어쓰기가 아니라 **새 버전을 박제(immutable)로 남긴다**. 게이트 revision은 이미 `version`+`parent_revision_id`+`superseded`로 박제됨(AXKG-SPEC-002) — 유지. **요약 draft(`summary_payload`)는 현재 v2가 v1을 덮어쓰므로 immutable 버전 체인으로 전환**한다(v1 보존, v2 새 버전 — 게이트와 동일한 원칙). 요약 버전의 저장 위치·구조 세부는 코드 소관(OQ), 원칙(박제·비덮어쓰기)은 계약이다.
- **D. 확정 문서 lifecycle 추적**: 확정 문서(`documents`)에 lifecycle을 부여한다 — `status ∈ {current, superseded}` + `version` + **producing revision/source 링크**(어느 게이트 버전이 만들었는지). 피드백/재분류로 재문서화되면 옛 문서는 `superseded`(박제 보존), 새 문서는 `current`가 된다. apply executor의 중복 거부(`write_new`)를 **버전 생성/supersede로 확장**한다(commit 경계 너머로 supersede 모델 확장). 정확한 컬럼·마이그레이션 세부는 코드 소관(OQ).

정합 후속 spec 업데이트(위 T-005 표에 더해):

| Spec | Action (T-009) |
|---|---|
| AXKG-SPEC-011 | update — §4 출력양식 층 정정(A: 템플릿≠output_schema, **템플릿=문서화③ 전용**, 요약①은 적응형이라 템플릿 없음·형식 규약은 프롬프트), 저장 직교 축(B) 명시. ~~요약 템플릿 보편화~~ 폐기(T-011). `body_markdown`은 요약 output_schema 필드로 유지 |
| AXKG-SPEC-010 | update — 템플릿 층 **문서화③ 전용** 유지. ~~요약 `body_markdown` 템플릿 편입~~ 폐기(T-011, 요약은 적응형 출력이라 템플릿 대상 아님·key OQ 철회) |
| AXKG-SPEC-009 | update (T-011) — Data Contract 예시의 요약 output_schema 필드에 `body_markdown` 추가(요약은 md 본문 출력, 형식 규약은 프롬프트 소관) |
| AXKG-SPEC-003 | update — 요약 draft 버전 박제(immutable 체인)로 전환(C), 덮어쓰기 서술 정정 |
| AXKG-SPEC-002 | update — 요약 draft 공유 버전 규칙을 박제(비덮어쓰기)로 명시(C) |
| AXKG-SPEC-004 | update — 확정 문서 lifecycle(status/version/producing 링크) + apply supersede 확장(D) |
| AXKG-SPEC-005 | update — superseded 문서 그래프 노출 제외·producing 링크(D) |

### 파생지식 본문·A1 modify·경로 컨벤션·frontmatter 정합 (2026-07-09 PLAN-009-T-018)

문서화③ 확정 모델을 구현 착수 기준으로 확정한다(스펙 문서만, 코드는 BE T-016/FE T-017 병렬). 6개 항:

- **파생지식 본문 계약**: `derived_suggestions[].draft_markdown`은 **전 `suggestion_type` 공통 필수**다. 종전 스키마/프롬프트가 본문을 산출하지 않아 executor가 전부 `no_draft_markdown`으로 스킵 → 파생 문서가 한 번도 생성되지 않던 갭을 닫는다.
- **A1 modify(supplement_existing_concept) 모델**: diff/patch 적용 엔진을 두지 않는다. 컨텍스트 빌더가 retriever 상위 후보 문서의 **전문**을 (per-doc 길이 cap과 함께) 주입하고, AI는 보충을 반영한 **수정 전문**을 `draft_markdown`으로 출력하며, executor가 대상 문서를 **overwrite**한다. `diff_preview`는 적용 엔진 입력이 아니라 **리뷰 표시용 요지 서술**이다.
- **경로 컨벤션(executor가 `PATH_NOT_ALLOWED`로 강제)**: main reference→`resources/`, main permanent(area)→`permanent/`, main baseline(project)→`projects/`, 파생 `create_new_concept`→`permanent/concepts/`, 파생 `create_project_baseline`→`projects/`, 파생 `supplement`(modify)→기존 문서 경로 그대로. 경로 표의 SSOT는 AXKG-SPEC-005 Path Convention이다.
- **frontmatter `id` 강등**: 필수→선택. 코드의 resolve 우선순위(stem→alias→id)는 유지하되 `id`가 없어도 stem/alias로 resolve되면 유효하다. 문서 템플릿 3종에서 `id`를 제거한다.
- **템플릿 frontmatter 코드 정합**: reference 템플릿 `source_url`→`source`(파서 키), `aliases` 3종 추가, `up`은 list 문법, `created_at` 제거. frontmatter 필드 계약의 SSOT는 AXKG-SPEC-005 Required Frontmatter다.
- **executor 검증 확장**: 파생 `draft_markdown`의 wikilink도 본문 wikilink와 동일하게 `BROKEN_WIKILINK`/`UP_WITHOUT_BODY_LINK` 검증 대상이다. executor의 `ApplyResult.skipped`(적용에서 빠진 항목)는 `apply_plans`에 박제해 관측 가능하게 한다.

정합 대상: AXKG-SPEC-004(파생지식 본문 필수·A1 overwrite·PATH_NOT_ALLOWED·파생 링크 검증·skipped 박제), AXKG-SPEC-005(id 선택·경로 컨벤션 SSOT 표), AXKG-SPEC-010(템플릿 frontmatter를 SPEC-005 계약에 정합), AXKG-SPEC-011(연결 후보 블록에 modify용 후보 문서 전문 주입 추가). 코드 세부(클래스·시그니처)는 발명하지 않는다.

### 지식 아키텍처: 4층 문서 정체성·SoT 위임·concept 버전/연쇄 (2026-07-09 PLAN-009-T-023)

지식이 `출처 → 원자 개념 → 종합/전략 → 실행` 방향으로 자라는 모델을 확정한다. 스펙 문서만 정정하며 concept 버전 확장(D)·stale 연쇄(E)의 코드는 미착수(후속 WP). 경로 컨벤션(AXKG-SPEC-005 Path Convention)은 **현행 유지 — 변경 없음**. 확정 목록(A~E) 밖 항목·구현 디테일(컬럼·apply action·stale 플래그 명칭)은 발명하지 않는다.

- **A. 4층 지식 아키텍처(문서 유형별 정체성)**: `출처 기록(reference ← resource, resources/) → 원자 개념(concept, permanent/concepts/) → 종합 노트(permanent ← area, permanent/) → 실행 문서(baseline ← project, projects/)` 4층으로 지식이 자란다. 층별 정체성 — 출처 기록 = "이 자료가 무엇을 말했나"(출처 맥락·논지·인용, 자료 단위, 생성 후 거의 고정), 원자 개념 = "이 개념은 무엇인가"(**사실의 SoT**, 출처 독립, 여러 출처가 합류하며 성장), 종합 노트 = "내 전략/종합 판단"(원자 개념이 합쳐져 자라는 살아있는 문서), 실행 문서 = 프로젝트 문서. permanent 안의 두 층(concepts/=원자, 루트=종합)은 합치지 않고 위계를 유지한다. 요약 md(`summaries/`)는 순수 데이터 보관용·그래프 무관(기존 확정 재확인). SSOT: AXKG-SPEC-004.
- **B. SoT 위임(중복 서술 금지)**: 개념 상세의 SoT는 concept 노트 한 곳이다. reference는 개념을 재서술하지 않고 요지 + `[[concept]]` 링크로 위임한다(링크 의미 = "출처가 개념을 인용"). permanent 종합 노트도 개념을 재서술하지 않고 개념들을 엮은 **내 판단/전략**만 소유하며 구성 개념을 `[[concept]]`로 참조한다. 같은 개념에 두 번째 출처가 오면 새 concept 생성이 아니라 기존 concept 보충(`supplement_existing_concept`)으로 합류한다 — 이것이 개념 성장 메커니즘이다. SSOT: AXKG-SPEC-004.
- **C. 템플릿/형식 재배치**: 현행 permanent 템플릿의 "한 줄 주장/맥락/내 결론" 골격은 concept의 모양이므로 **concept 작성 규칙으로 이사**한다. ~~concept는 main이 아니라 파생이라 템플릿 주입 대상이 아니다(형식은 프롬프트 소관)~~ → **T-028에서 개정**(아래 라운드 B 보강): concept도 템플릿(4종째)을 갖고 문서화③ 조립 시 고정 동봉으로 주입된다. permanent(종합) 템플릿은 종합 노트 골격(영역 주제 / 현재 나의 종합·판단 / 구성 개념 `- [[concept]] — 역할` / 열린 질문)으로 재정의한다. 세부 문안은 BE 태스크 소관, 이 결정은 계약 수준까지. SSOT: AXKG-SPEC-010.
- **D. concept 버전 lifecycle 확장(방향 확정, 구현 후속 WP)**: 기존 버전 모델(md=현재본 하나 / 히스토리=DB immutable revision / `documents.version`++, PLAN-009-T-015)을 **파생 concept 문서에도 확장**한다. 현행은 main 문서만 version/producing 스탬프가 적용되고 파생은 overwrite만 되는 갭이 있다(as-is). 파일명 버전(`concept_v1.md`)은 채택하지 않는다 — stem이 바뀌면 기존 `[[ ]]` 링크가 깨지고 "md=현재본 하나" 결정과 충돌한다. **stem 불변 + DB 버전**을 유지하고 그래프는 항상 current만 노출한다. SSOT: AXKG-SPEC-004 Document Lifecycle.
- **E. concept→permanent stale 연쇄 + 재생성 게이트(신규 기능, 구현 후속 WP)**: concept 새 버전 승인 시 backlink(`document_edges`)로 그 concept를 참조하는 permanent 종합 노트를 찾아 "구성 개념 갱신됨" **stale로 표시**한다. 반영은 자동이 아니다 — 사용자가 원할 때 해당 permanent의 **재생성 게이트**를 열어 초안 검토→승인으로 갱신한다(승인 게이트 철학: AI는 제안만, 확정은 사용자). 자동 연쇄 재작성은 하지 않는다. SSOT: AXKG-SPEC-004 Document Lifecycle.

정합 대상: AXKG-SPEC-004(A 4층 정체성·B SoT 위임·D concept 버전 확장·E stale 연쇄), AXKG-SPEC-010(C permanent=종합 노트 템플릿 계약, concept 형식은 가이드+프롬프트). 경로 컨벤션 표(AXKG-SPEC-005)는 변경 없음. D/E 구현은 후속 WP이며 코드 세부는 발명하지 않는다.

**후속 논의 보강 (2026-07-09 PLAN-009-T-024) — B 범위 정정 + E 동작 계약**:

- **B 범위 정정**: "개념 상세를 재서술하지 않는다"는 **개념의 상세 설명 섹션을 복사하지 않는다**는 뜻이며, permanent 종합 노트의 **판단 문장 안에 개념 요지가 인용되는 것은 허용·필연**이다(예: "성숙도 4단계 기준 우리는 2단계이므로 확산에 집중"). 따라서 concept 개정 시 permanent 판단 문장이 낡은 사실을 담을 수 있고, 이것이 E의 실질 근거다. SoT 위임은 오염 표면적을 줄일 뿐 **구조적으로 0으로 만들지 않는다**(이 서술을 금지 규율로 명문화).
- **E 동작 계약**: ① stale 배지 = "영향 가능성 있음"(참조 기반 과잉 포함), "수정 필요" 판단 아님 — 시스템은 수정 필요를 판단하지 않는다. ② 감지 = concept 새 버전 승인 시 `document_edges` backlink 쿼리(AI 없음), 배지만 부착 + concept 변경 요지 동봉(게이트 payload 재사용). ③ 재생성 = 문서당 독립 태스크(1 프롬프트 = 1 문서, 입력 = 대상 permanent 전문 + 바뀐 concept 전문 + 변경 요지), 일괄 판단 없음. ④ 1 승인 = 1 문서(version++). ⑤ 부분 처리 허용(트랜잭션 아님) — 미처리 stale은 배지 유지, concept v2는 이미 확정 적용됨. ⑥ 출력 규율 = 옛 전제 의존 판단만 수정·미지적 판단 보존(피드백 v2 규율 계열), 암묵 전제 판단도 탐지 대상·최종 방어는 사용자 게이트.
- **E-7 triage OQ**: stale 후보별 영향 유/무 AI 사전 심사는 **v1 제외** — 구현 착수 안 함·조건부 OQ 유지. 종전 "대량 누적 실증 시 도입 검토"의 흐릿한 조건은 구체 트리거로 교체(2026-07-10 PLAN-009-T-043 재논의): 정량(미처리 stale 상시 10건 이상)·정성(dismiss가 처리량 다수)·도입 시 lexical 사전 필터→AI 순서. **기준 상세 SSOT는 AXKG-SPEC-004 §7 OQ** — 여기서는 참조만 둔다(중복 방지).

정합 대상: AXKG-SPEC-004(§4 SoT 위임 B 범위 정정·Document Lifecycle E 서브섹션 E-1~6 보강·§7 OQ에 E-7 triage). 경로 컨벤션·Layer Taxonomy·타 스펙 불변. 구현은 여전히 후속 WP(as-is/to-be 구분 유지), 컬럼·클래스명 발명 금지.

**라운드 B 보강 (2026-07-09 PLAN-009-T-028) — concept 템플릿 신설 + supplement 자발 제안 (라운드 A 라이브 실측)**:

- **concept 템플릿 신설(C항 개정)**: 템플릿 4종째로 `concept`를 추가한다. concept는 고정 골격(정의/맥락/근거 출처)을 가진 문서 타입이라 Layer Taxonomy상 뼈대는 템플릿 소유가 맞다. 파생이라 destination 매핑이 없으므로 main 3종(destination 선택)과 달리 **문서화③ 조립 시 고정 동봉**으로 주입한다. 위 C항의 "concept는 템플릿 대상 아님·형식은 프롬프트 소관"을 이 항이 개정한다(배선 부재 타협 해소). 채우는 작성 방법(how)은 여전히 프롬프트(AXKG-SPEC-009) 소관. SSOT: AXKG-SPEC-010.
- **supplement 자발 제안**: 전문이 연결 후보 컨텍스트로 주입된 기존 concept에 출처가 새 정보를 담고 있으면 AI가 `supplement_existing_concept`를 **자발 제안**한다(`[[concept]]` 링크만 걸고 넘어가지 않음). 라운드 A 실측 근거: 유도 피드백 없이는 supplement가 산출되지 않았다. SSOT: AXKG-SPEC-004(파생지식 계약).
- D(concept 버전 확장) 구현 상태는 코드(T-027) 랜딩 후 admin 별도 확인 예정이므로 **as-is/to-be 구분 유지** — D를 done으로 선언하지 않는다. E(stale) 서술은 이 라운드에서 변경하지 않는다.

정합 대상: AXKG-SPEC-010(템플릿 scope 4종·concept 주입 방식 구분·C항 개정 반영), AXKG-SPEC-004(파생지식 supplement 자발 제안 규칙). 경로 컨벤션·Layer Taxonomy·E 서술 불변, 구현 디테일(클래스·컬럼) 발명 금지.

**문서화③ 라운드 마감 (2026-07-10 PLAN-009-T-037) — D/E 구현 완료 + 신규 에러코드 + 실행 옵션 + 개선 OQ**:

2026-07-10 풀 E2E 완주(4소스, 요약→분류→문서화→supplement→stale→재생성→해제 전 구간 라이브 통과)로 D·E가 코드/검증 완료됐다. 스펙 as-is/to-be를 실물에 정합한다(스펙 문서만, 커밋은 admin/사용자). 목록 밖 첨가·경로 컨벤션·Layer Taxonomy 불변.

- **D(파생 concept 버전 lifecycle) 구현 완료**(코드 PLAN-009-T-027 + 라이브 concept v1→2): create=v1 / supplement=v++ / `producing_revision_id`·`source_id` 스탬프, main 계보 supersede 판단에서 concept 제외. 라운드 B의 "D를 done으로 선언하지 않는다(as-is/to-be 유지)"를 이 amendment가 종료한다. SSOT: AXKG-SPEC-004 Document Lifecycle.
- **E(concept→permanent stale 연쇄) 구현 완료**(BE PLAN-009-T-030 / FE PLAN-009-T-031·032·033 + 라이브: 감지→배지→재생성 게이트→승인→해제). E-1~6 계약 그대로 구현, 저장=`document_stale_marks`(alembic 0018), API 3종(`GET /documents/stale`·dismiss·regenerate=producing source 문서화 게이트 재문서화 재사용). E-7 triage는 v1 제외로 잔존. SSOT: AXKG-SPEC-004.
- **신규 에러코드 정식 등재**(AXKG-SPEC-004 Case Matrix): `SUPPLEMENT_TARGET_NOT_CONCEPT`(422, supplement 대상은 `document_type=concept`만 — reference v2 오염 실측 근거, PLAN-009-T-036), `STALE_REGENERATION_NOT_ALLOWED`(409)·`DOCUMENT_NOT_FOUND`(404, PLAN-009-T-030).
- **실행 옵션 계약**(AXKG-SPEC-007): 문서화(`documentation_gate`) 태스크 정의 seed 기본값 `provider_options.max_turns=12`(`error_max_turns` 실측)·`options.timeout_sec=600`(stale 3입력+연결 후보 전문 주입이 300s 초과 실측), PLAN-009-T-035 시드 반영.
- **개선 OQ 신규 등재(해소 아님 — 관찰 실측, 소유 스펙 §7)**: 경로 시스템 강제(AI가 target_path 디렉토리 오생성 — 빌더/executor가 디렉토리 결정·AI는 파일명만, AXKG-SPEC-004 §7), 파서 wikilink 오탐(코드스팬/펜스 내 `[[ ]]` 파싱 제외, AXKG-SPEC-005 §7), 형제 reviewable revision dangling(승인 시 형제 supersede, AXKG-SPEC-002 §7).

정합 대상: AXKG-SPEC-004(D/E done 전이·Case Matrix 3종·§7 OQ 해소·경로 개선 OQ), AXKG-SPEC-007(문서화 태스크 seed 기본값), AXKG-SPEC-005(파서 wikilink 개선 OQ), AXKG-SPEC-002(형제 supersede 개선 OQ). open_kknaks 라이브러리 result subtype(error_max_turns) 유실로 에러 메시지에 thinking stream 조각이 실리는 건은 **제품 밖 별건**으로 제품 스펙에 등재하지 않는다.

**개선 OQ 3건 해소 (2026-07-10 PLAN-009-T-042) — 경로 시스템 강제·파서 오탐·형제 supersede + 경로 결정 주체 이관**:

바로 위 T-037 amendment가 "해소 아님(관찰 실측)"으로 등재했던 개선 OQ 3건이 코드로 해소·라이브 검증(전부 admin 게이트 통과)됐다. 스펙 as-is/to-be를 실물에 정합한다(스펙 문서만·목록 밖 첨가 금지·커밋 admin/사용자).

- **경로 시스템 강제 = 경로 결정 주체 이관(설계 결정, T-040)**: 문서화③ 산출물의 경로 **디렉토리 결정을 AI에서 시스템으로 이관**한다. AI `output_schema`(`documentation_gate` v3)는 파일명/stem만 산출 — `document_draft`는 `filename_candidate`, `derived_suggestions[]`는 create류=`filename_candidate`/supplement=`target_stem`(if/then 강제, `target_path` 제거). 디렉토리 조립·최종 `target_path`는 Phase 2 `wrap_documentation_output` 빌더 소유(main=prior current main 경로 재사용, 파생 create=`suggestion_type` 디렉토리, 파생 modify=resolver로 `target_stem`→기존 경로), 매핑 SSOT=빌더·executor 공용 `services/document_paths.py`. executor `PATH_NOT_ALLOWED`는 안전망 유지, envelope `target_path` 자리는 시스템이 채워 **FE 계약 무변경**·구형 payload 하위호환. 이 이관은 이 결정이 소유한 **output_schema 경계**(위 Decision) 및 3자 조립(BE가 조립·스냅샷)의 직접 연장이라 신규 DEC로 쪼개지 않고 in-place 앵커한다. SSOT: AXKG-SPEC-004 §4 경로 결정 주체.
- **파서 wikilink 코드 영역 제외(T-038)**: `extract_wikilinks`가 코드펜스(` ``` `/`~~~`)·인라인 코드스팬 내부 `[[ ]]`를 파싱 제외 → `BROKEN_WIKILINK` 오탐 해소(원문의 링크 문법 예시가 초안에 복사되는 케이스). 판정 3곳(엣지 빌드·링크 preview·executor 본문 검사) 자동 반영, 링크 정규화 규칙 불변. SSOT: AXKG-SPEC-005 Link Syntax Contract.
- **형제 reviewable supersede sweep(T-039)**: "게이트당 최신 하나만 reviewable" 강제. 새 revision reviewable 전이 직전(분류·문서화 공통) 같은 게이트의 다른 모든 reviewable→superseded sweep(종전=직전 parent 단건), 승인 확정 시점(분류 approve·문서화 apply)에도 동일 sweep=안전망. drafting 미터치. SSOT: AXKG-SPEC-002 §5.

정합 대상: AXKG-SPEC-004(§4 경로 결정 주체 신설·Data Contract `filename_candidate`/`target_stem`·§5 규칙·§7 OQ 해소), AXKG-SPEC-005(Link Syntax 코드 영역 제외 규칙·Path Convention 시스템 조립 각주·§5 규칙·§7 OQ 해소), AXKG-SPEC-002(§5 형제 supersede sweep·§7 OQ 해소·documentation.v1 output_schema 경로 필드 정합 — 이 과정에서 apply_plan file_action의 T-018 이전 잔재 `patch_markdown`→`overwrite_markdown` 동반 정합). 경로 컨벤션 표(디렉토리 매핑) 불변·Layer Taxonomy 불변, 코드 세부(클래스·시그니처) 발명 금지.

## Rationale

- 연결 품질은 제품 핵심 가치(AXKG-BL-001)인데, 초안 AI가 그래프 컨텍스트 없이 wikilink를 생성하면 executor의 깨진 링크 거부(AXKG-SPEC-004)와 구조적으로 충돌한다. retriever 재사용은 새 기계 없이 관련성을, index 스냅샷은 링크 유효성을 보장한다.
- 조립을 AI에게 맡기면 출력 구조 보장이 약해지고 버전 스냅샷 추적이 애매해진다. BE는 DB 아티팩트·런타임 데이터만 조립하고 사용 버전을 스냅샷해 재현성과 감사 추적(`prompt_version_id`+`template_version_id`)을 확보한다.
- **가이드(정의/정책/판단 규칙)**는 자주 바뀌지 않는 코드성 자산이라 DB 동적 관리 대상이 아니다 — worker가 claude를 프로젝트 컨텍스트 안에서 실행하면 매번 인라인 없이 claude가 진입 문서로 읽고, 런타임 git pull 의존을 피하려 빌드 시점 이미지에 내장한다. 반면 **작성 방법(how)**은 자주 튜닝하는 자산이라 worker 이미지에 두면 변경마다 재빌드가 필요하므로 DB 프롬프트(즉시 반영)에 둔다(2026-07-09 경계 재정렬, 위 Decision·AXKG-SPEC-011 §4 Layer Taxonomy).
- 실행 계약이 스펙 없이 아키텍처 문서에만 있으면 요약 스테이지처럼 소관이 비는 구멍이 생긴다. 관리(009/010)와 실행(011)을 분리해 각자 SSOT를 갖게 한다.
- project 문서화를 빼면 수집-분류-문서화 파이프라인이 PARA 4분류 중 하나에서 끊긴다. MVP에서 baseline 후보 한 종으로 좁혀 포함한다.
- **(T-023 지식 아키텍처)** 4층 정체성·SoT 위임은 이미 이 결정이 소유한 destination별 산출물·파생지식 계약(SPEC-004)의 개념적 근거를 명문화한 것이라 신규 DEC로 쪼개지 않고 in-place 앵커한다. concept를 재서술 대신 `[[concept]]` 위임으로 고정하면 개념 상세가 여러 문서에 복제되지 않고(SSOT), 두 번째 출처가 보충으로 합류해 개념이 성장한다. 파일명 버전 대신 stem 불변+DB 버전을 택한 것은 "md=현재본 하나"(T-015) 결정과 `[[ ]]` 링크 안정성 때문이고, stale 연쇄를 자동 재작성이 아니라 재생성 게이트로 둔 것은 "AI는 제안·확정은 사용자"라는 승인 게이트 철학(AXKG-SPEC-002)의 연장이다.
- **(T-009 정합) 출력양식·저장·버전·lifecycle은 이 결정이 세운 실행/조립 계약(3층 taxonomy·3원천)의 직접 파생이라 신규 DEC로 쪼개지 않고 in-place 개정한다** — A는 이 결정이 소유한 taxonomy(SPEC-011 §4)의 정정이고, T-007 경계 재정렬 개정과 같은 계약의 연장이다. `output_schema`에 md 뼈대를 넣으면 응답 스키마가 커지고 자주 튜닝하는 양식이 스키마 검증과 얽히므로, 뼈대는 프롬프트 주입용 별도 템플릿으로 분리한다(문서화③). **(T-011 재정정)** T-009는 이 원칙을 요약①에도 확장해 "요약도 템플릿"으로 봤으나, 실제 라이브 요약 출력이 원문 구조를 따르는 **적응형**이라 고정 뼈대가 오히려 품질을 해침을 확인해 되돌린다 — 요약①은 템플릿 없이 형식 규약을 프롬프트(작성 방법)가 담고, `body_markdown`은 output_schema 필드로 출력된다. 박제(C)·lifecycle(D)은 "재생성은 이전 버전을 감사용으로 보존한다"는 게이트 원칙(AXKG-SPEC-002)을 요약 draft와 확정 문서까지 일관 확장한 것이다.

## Resulting Spec

| Spec | Action |
|---|---|
| AXKG-SPEC-011 | create — AI 실행 파이프라인(4스테이지 공통 실행 계약) |
| AXKG-SPEC-004 | update — 초안 생성 입력 컨텍스트를 SPEC-011 참조로 연결, 템플릿 소비 문구 정리 |
| AXKG-SPEC-005 | update — 연결 후보 컨텍스트(S-1)를 SPEC-011 계약으로 연결 |
| AXKG-SPEC-009 | update — output_schema 형식 JSON Schema 확정, 로드/조립 주체를 SPEC-011로 명시 |
| AXKG-SPEC-010 | update — 3자 조립 OQ 해소, MVP scope에 `project_baseline` 템플릿 추가 |

## Open Questions

- ~~콘텐츠 수집(URL 본문 fetch/유튜브 transcript)의 실행 위치~~ → **AXKG-SPEC-012로 확정**: BE 내 Source Collection Adapter(YouTube/정적 웹/동적 웹)가 수집하고 SourceMaterial로 정규화해 SPEC-011 context builder에 넘긴다. dynamic adapter의 브라우저 실행 분리 여부만 SPEC-012 OQ로 잔존.
- Graphify류 외부 그래프 도구의 배치 enrichment(후보 엣지 제안) 활용은 post-MVP 검토.
- ~~concept 버전 확장(D)·stale 연쇄(E)의 구현(컬럼·apply action·stale 플래그 명칭, 재생성 게이트 배선)은 후속 WP다.~~ → **구현 완료**(2026-07-10 PLAN-009-T-037 amendment): D=PLAN-009-T-027, E=BE PLAN-009-T-030/FE PLAN-009-T-031·032·033, 라이브 검증. 방향(stem 불변+DB 버전, 자동 재작성 없음·재생성 게이트 경유)은 그대로 확정 계약, 세부 명칭·저장(`document_stale_marks`/`supersede_document`)은 AXKG-SPEC-004가 규정.
