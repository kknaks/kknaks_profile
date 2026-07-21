---
type: decision
id: AXKG-DEC-007
title: "기업 project destination 회사별 팬아웃과 회사 내부 공통기능 정규화"
status: accepted
product: ax-knowledge-graph
created_at: 2026-07-20
updated_at: 2026-07-21
tags:
  - product/ax-knowledge-graph
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-002-enterprise-requirement-project-destination|AXKG-BL-002]]"
  decisions:
    - "[[decision-001-para-pipeline-and-approval-gates|AXKG-DEC-001]]"
    - "[[decision-004-mvp-defaults-and-scope|AXKG-DEC-004]]"
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
  specs:
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-010-document-template-management|AXKG-SPEC-010]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
    - "[[spec-012-source-collection-adapter|AXKG-SPEC-012]]"
    - "[[spec-014-enterprise-project-fanout|AXKG-SPEC-014]]"
  works: []
  releases: []
  related: []
---

# 기업 project destination 회사별 팬아웃과 회사 내부 공통기능 정규화

PARA `project` destination을 flat 한 장에서 **회사별 프로젝트 폴더로 팬아웃**하는 구조를 정식 결정으로 확정한다. 기업의 AX 전환 요구사항 docx가 inbox로 들어와 `project`로 분류되면, 회사 프로젝트 폴더 `projects/{corp}/` 안의 `origin/`(첨부 원본)·`baseline/`(원본요약)·`spec/`(기능정의서)로 다중 문서 팬아웃되고, 같은 기능이 다른 docx로 다시 들어오면 신규 문서 대신 기존 spec 하나로 통합·보강한다(정규화 = 기능 dedup, 부서 무관). 팬아웃/정규화의 상세 외부 계약 SSOT는 AXKG-SPEC-014다.

이 결정은 AXKG-BL-002가 **Resolved Decisions 5건**으로 확정하고 worked example(The_sc, 기능 10개)과 (A)구현 재활용/(B)정규화 정규화로 검증한 설계도를 정식 결정으로 formalize한 것이다. 계약·구현 상세(프롬프트 문구·DB 스키마·API·구현 파일 경로)는 이 결정이 확정하지 않으며 후속 spec/work에 위임한다.

> ⚠️ **용어 주의**: 회사 프로젝트 폴더 안의 `projects/{corp}/baseline/`(런타임 산출물 = 넘어온 docx를 md로 요약·정리한 "원본요약")은, `AXKG-BL-002` 같은 제품 설계용 baseline 타입 메타문서와 **이름만 같고 다른 개념**이다. 아래에서 전자는 항상 `projects/{corp}/baseline/`로 표기한다.

## Decision

### 1. project destination 산출물 구조 = 회사별 프로젝트 팬아웃 (DEC-005 project 부분 supersede)

- **결정**: project로 분류된 산출물은 flat 한 장이 아니라 회사 프로젝트 폴더 `projects/{corp}/` 안에서 `origin/`(첨부 원본)·`baseline/`(원본요약)·`spec/`(기능정의서) **3층 다중 문서**로 팬아웃한다. 요구 1항목 = 기능정의서 1장.
- **근거(왜)**: 기업 AX 요구는 docx로 오며, 한 회사가 기능 여러 개를 한 번에, 부서별로 따로, 같은 기능을 반복 요구한다. flat 한 장(`projects/{파일명}.md`, `project_baseline` 단일 템플릿)에는 회사라는 컨테이너·기능이라는 단위·반복 요구를 합치는 정규화가 모두 담기지 않는다(AXKG-BL-002 Context).
- **영향(무엇을 바꾸나 / supersede)**: **AXKG-DEC-005의 "project destination 산출물 = 단일 baseline 후보 한 장"** 및 그에 딸린 **AXKG-SPEC-010의 `project_baseline` 단일 템플릿 전제**를 이 결정이 **대체(supersede)**한다. project 부분(단일 baseline 한 장·단일 템플릿)을 origin/baseline/spec 팬아웃 구조로 교체하며, 단일 `project_baseline` 템플릿을 **`project_source_summary`(원본요약)·`project_feature_spec`(기능정의서) 2종**으로 대체한다(AXKG-SPEC-010에 정식 등록 완료). 단, DEC-004/DEC-005가 세운 **"파일 template directory를 만들지 않는다"** 원칙과 **문서 뼈대의 DB 동적 템플릿 관리(AXKG-SPEC-010, PostgreSQL 동적)**는 그대로 유지한다 — 팬아웃은 destination→디렉토리 매핑과 템플릿 scope를 바꿀 뿐, 템플릿 관리 방식은 건드리지 않는다.

### 2. 회사 프로젝트 동적 생성

- **결정**: 앱의 "프로젝트 추가" 액션으로 `projects/{corp}/{origin,baseline,spec}/` 폴더와 `baseline/map.md`·`spec/map.md` 스캐폴드를 **동적으로** 생성한다. corp slug는 사용자 입력 회사명(예: "더에스씨")을 시스템이 slugify(`the-sc`)해 정한다. slugify 결과가 **기존 `{corp}`와 충돌하면** 사용자에게 **"기존 `{corp}` 프로젝트에 이 docx를 추가할까요?"** 를 확인한다 — **예 = 기존 `{corp}`에 origin/baseline/spec 추가**(같은 회사로 합류), **아니오 = `{corp}-2` 등 suffix로 새 프로젝트 생성**.
- **근거(왜)**: 회사 경계는 자동 추론으로 흐트러지면 안 되는 축이라, 사람이 명시적으로 통제한다(AXKG-BL-002 Resolved Decisions #4). 회사 목록을 미리 하드코딩하지 않고 요구가 들어오는 대로 스캐폴드를 까는 편이 운영 현실에 맞는다. 충돌 시에도 합류/신규를 사용자에게 물어 회사 경계 판단을 사람이 통제한다.
- **영향**: destination→디렉토리 매핑이 정적 `projects/`에서 사용자 주도 동적 `projects/{corp}/{origin,baseline,spec}/`로 바뀐다(코드레포 소관). slug 충돌 시 합류/suffix 신규 분기 UX가 "프로젝트 추가" 플로우에 포함된다.

### 3. project 층위 = origin + baseline + spec 3층만

- **결정**: 회사 프로젝트 안에는 `origin/`(첨부 원본)·`baseline/`(원본요약)·`spec/`(기능정의서) 3층만 둔다. area(종합 판단)·resource(참고 자료) 성격 자료는 회사 프로젝트 안에 분리 저장하지 않고, 기존 전역 PARA 흐름 그대로 area→`permanent/`, resource→`resources/`에 둔다.
- **근거(왜)**: project 폴더가 PARA 4분류를 통째로 복제하면 전역 지식 아키텍처(AXKG-DEC-005 4층: 출처 기록→원자 개념→종합 노트→실행 문서)와 중복·충돌한다. 회사 프로젝트는 "회사가 준 원본(origin)"·"이 회사가 뭘 요구했나(baseline)"·"그 요구를 기능 단위로 쪼갠 것(spec)"만 담고, 종합·참고 지식은 전역 흐름을 재사용한다(AXKG-BL-002 Resolved Decisions #3).
- **영향**: 회사 프로젝트 내부 3층과 ax-graph 전역 4층은 층위가 다름을 문서화한다 — `projects/{corp}/baseline/`은 전역 4층의 "실행 문서" 층 안에서 다시 열리는 하위 구조다.

### 4. 공통기능 정규화 = 회사 내부 기능 dedup (부서 무관)

- **결정**: 같은 `{corp}` 안에서 같은 기능이 다른 docx로 다시 들어오면 신규 spec을 만들지 않고 **기존 spec 하나로 통합·보강한다(기능 dedup)**. 새 요구가 상세요구·유저플로우 디테일을 더하면 기존 기능정의서를 보강(supplement)한다. **기능은 프로젝트의 기능 카탈로그이며 요청부서·요청 이력을 붙이지 않는다.** **회사를 넘는 전역 capability 레지스터(`capabilities/` 같은 공통 카탈로그)는 도입하지 않는다.** 회사가 다르면 같은 기능이라도 별개 spec이다.
- **근거(왜)**: 재사용 가치는 한 회사 안에서 같은 기능을 여러 번 정의하지 않고 하나로 합쳐 상세를 키우는 데서 나온다. **기능은 프로젝트의 기능 카탈로그라 특정 부서 귀속이 아니다** — 모든 부서에 필요한 기능을 어느 부서가 안 적었다고 빼거나 부서별로 문서를 가르면 안 된다. 그래서 요청부서·요청 이력은 저장하지 않는다. 회사를 가로지르는 정규화는 회사 경계(사람이 통제하는 축)를 무너뜨리고 서로 무관한 요구를 억지로 합친다. AXKG-BL-002 (A) 관찰 노트대로, ax-graph 자체 플랫폼 역량(graph-chat·문서화 게이트·curation)과 겹치는 기능은 **구현 시 재활용은 가능하나 정규화/승격 대상은 아니다** — 각 회사 spec은 별개로 남는다.
- **영향**: dedup 메커니즘은 ax-graph 기존 자산을 `{corp}` 경계 안으로 한정 재사용한다 — index/stem resolution(같은 회사 안 같은 기능 판정), `supplement_existing_feature`(신규 대신 기존 기능정의서 통합·보강), retriever 컨텍스트(같은 회사 폴더 안 유사 기능 탐색). 매칭이 모호하면 신규 spec으로 안전 폴백한다. 회사를 넘는 spec 재사용·통합은 하지 않는다.

### 5. docx intake = 텍스트 추출만 (구조화는 요약①)

- **결정**: docx에 필요한 것은 **본문 텍스트 추출뿐**이다 — 기존 source 수집 어댑터에 **docx 텍스트 추출 경로**를 추가한다. 기능별 구조화(기능 1·2·3… 줄글)는 어댑터가 아니라 기존 **요약① 스테이지**가 담당한다. 요약①은 원문 구조를 따르는 적응형 요약이라 docx의 기능 목록 구조를 그대로 따라 기능별 줄글을 산출하고, 그 산출물이 `projects/{corp}/baseline/` 원본요약이 되어 spec 팬아웃의 입력이 된다.
- **근거(왜)**: 요구 docx는 줄글+목록 중심이라 텍스트 추출로 충분하고, 기능 항목 단위 구조는 이미 적응형인 요약①이 원문 구조를 따라가며 산출한다 — 어댑터에 표 보존·이미지 대체텍스트 같은 파싱 계약을 얹는 것은 과설계다. 적응형 요약은 새 원칙이 아니라 **기존 결정과의 정합**이다 — 요약①은 원문 구조를 따르는 적응형 출력이라 고정 뼈대(템플릿)를 씌우지 않는다(AXKG-SPEC-011 §4 요약① 적응형 출력 규약 / AXKG-DEC-005 A). 표는 텍스트로 딸려 나와도 요약①이 정리한다.
- **영향**: source 수집 어댑터(AXKG-SPEC-012)에 docx **텍스트 추출** 경로가 추가된다. 표 보존·이미지 대체텍스트·병합셀·중첩표·스캔이미지 같은 파싱 계약은 두지 않는다(요약①이 구조화를 담당하므로 불필요).

### 6. map.md(MOC) 자동 갱신

- **결정**: 문서 apply 시점에 파이프라인이 해당 폴더의 `map.md`(MOC = index/목차)를 자동으로 재생성한다(문서 목록 반영). 수동 갱신이 아니다.
- **근거(왜)**: baseline/spec 문서가 팬아웃·dedup 보강으로 계속 늘고 바뀌므로, MOC를 손으로 유지하면 즉시 낡는다. apply 훅에서 재생성하면 항상 현재 상태를 반영한다(AXKG-BL-002 Resolved Decisions #2).
- **영향**: 문서화 게이트 apply 경로에 폴더별 map.md 재생성 훅이 추가된다(코드레포 소관).

### 7. 승인 게이트 팬아웃 메커니즘 = 파생지식 main+derived 재사용

- **결정**: project 문서화 승인 게이트는 새 승인 표면을 만들지 않고 기존 **파생지식 모델(`main_document` + `derived_suggestions[]`, AXKG-SPEC-004)** 을 재사용한다. 한 초안 revision에 `main_document` = 원본요약(→ `baseline/`), `derived_suggestions[]` = 기능별 초안(→ `spec/`, 신규 `create_feature_spec` / 같은 corp 기존 기능과 매칭 시 `supplement_existing_feature`)을 담고, 각 기능 초안의 `## 연결`에는 retriever + documents index로 훑은 ax-graph 기존 역량 차용 wikilink를 제안한다(AXKG-DEC-005 연결 후보 컨텍스트 재사용). admin이 한 게이트 화면에서 원본요약 + N개 기능 초안을 함께 검토·승인하면 apply가 실행된다.
- **근거(왜)**: 팬아웃(1 원본요약 + N 기능)은 이미 게이트가 다루는 "main 문서 + 파생지식" 구조와 동형이다. 새 게이트/승인 API를 만들지 않고 기존 모델을 재사용하면 승인 철학(AI 제안·사용자 확정)·버전 박제·경로 조립 주체를 그대로 물려받는다.
- **영향**: project destination에서 게이트 apply가 origin 보관 + main(원본요약) + derived(기능정의서 N) 팬아웃으로 확장된다. 파생지식 apply 규칙·경로 디렉토리 조립·검증은 AXKG-SPEC-004가 SSOT, 팬아웃 외부 계약(무엇이 나오나)은 AXKG-SPEC-014가 SSOT다.

### 8. origin(첨부 원본) 저장

- **결정**: 첨부 docx **원본 파일**은 요약 md와 별도로 `projects/{corp}/origin/`에 손대지 않은 raw로 보관한다. 회사 프로젝트 구조는 `origin/`(원본)·`baseline/`(원본요약)·`spec/`(기능정의서) 3층이다.
- **근거(왜)**: 원본요약(baseline)은 요약①이 가공한 md라 원문 그대로가 아니다. 감사·역참조·재요약을 위해 손대지 않은 첨부 원본을 별도로 남긴다.
- **영향**: 회사 프로젝트 스캐폴드·apply에 origin 층이 추가된다(Decision 1·3 3층 구조). origin은 요약·가공 대상이 아니라 보관 대상이다.

## Consequences

경로·계약·구현 세부의 확정은 후속 spec/work 소관이며, 이 결정은 영향받는 문서·코드를 짚기까지만 한다.

**spec 갱신 필요**:

| Spec | Action |
|---|---|
| AXKG-SPEC-014 | **신설·SSOT** — 기업 프로젝트 팬아웃의 외부 계약(origin 3층·main+derived 팬아웃·기능 dedup·기능정의서 계약). 아래 나머지 spec은 이 SSOT를 요지+링크로 참조 |
| AXKG-SPEC-004 | update(완료) — 문서화 게이트의 project 산출물을 단일 `create_project_baseline` 한 장에서 origin 보관 + `main_document`(원본요약) + `derived_suggestions[]`(기능정의서, `create_feature_spec`/`supplement_existing_feature`) 팬아웃으로 확장. 상세는 SPEC-014로 위임 |
| AXKG-SPEC-010 | update(완료) — 단일 `project_baseline` 전제를 `project_source_summary`(원본요약)·`project_feature_spec`(기능정의서) **2종으로 정식 등록**(파일 template directory 미신설·PostgreSQL 동적 관리 원칙 유지) |
| AXKG-SPEC-012 | update(완료) — source 수집 어댑터에 docx **텍스트 추출** 경로 추가(본문 텍스트만; 기능별 구조화는 요약① 소관·표/이미지 파싱 계약 없음) |

**코드 영향** (코드레포 소관, 이 문서는 경로만 참조):

- destination→디렉토리 매핑을 flat `projects/`에서 `projects/{corp}/{origin,baseline,spec}/`로 변경(빌더·executor 공용 경로 매핑).
- **문서화 프롬프트 project 분기 + context 가이드 갱신**: project 분류 시 원본요약(main) + 기능정의서(derived) 팬아웃 초안을 내도록 문서화 프롬프트에 project 분기를 추가하고, `context/para-classification`(project 판정)·`context/documentation-guide`(원본요약·기능정의서 산출 규칙)·`context/document-link-rules`(원본요약↔기능정의서 `[[ ]]` 연결·차용 링크)를 갱신한다.
- project 초안 템플릿 시드를 `project_source_summary`·`project_feature_spec` 2종으로 재구성(AXKG-SPEC-010).
- 문서화 게이트의 project 팬아웃 로직과 회사 내부 기능 dedup(`supplement_existing_feature` 방식 통합·보강) 배선.
- origin 첨부 원본 보관(요약 md와 별도) + 문서 apply 시 폴더별 map.md 자동 재생성 훅.
- "프로젝트 추가" 액션의 회사명 slugify → `projects/{corp}/{origin,baseline,spec}/` + map.md 스캐폴드 동적 생성.

## Open Questions

현재 미결 없음 — 계약·구현 상세는 후속 spec(20-spec)/work에서 확정한다.
