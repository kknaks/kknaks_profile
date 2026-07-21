---
type: spec
id: AXKG-SPEC-014
title: "기업 프로젝트 팬아웃: 회사별 origin·baseline·spec 문서화와 기능 dedup"
status: stable
product: ax-knowledge-graph
version: 0.0.1
created_at: 2026-07-21
updated_at: 2026-07-21
tags:
  - product/ax-knowledge-graph
  - doc/spec
  - status/stable
links:
  baselines:
    - "[[baseline-002-enterprise-requirement-project-destination|AXKG-BL-002]]"
  decisions:
    - "[[decision-007-enterprise-project-destination-fanout|AXKG-DEC-007]]"
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
    - "[[decision-001-para-pipeline-and-approval-gates|AXKG-DEC-001]]"
  specs:
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-005-document-link-graph-contract|AXKG-SPEC-005]]"
    - "[[spec-010-document-template-management|AXKG-SPEC-010]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
    - "[[spec-012-source-collection-adapter|AXKG-SPEC-012]]"
  works: []
  releases: []
  related: []
---

# 기업 프로젝트 팬아웃: 회사별 origin·baseline·spec 문서화와 기능 dedup

기업 AX 요구사항 docx가 `project`로 분류되면, flat 한 장이 아니라 **회사 프로젝트 폴더 `projects/{corp}/`** 안의 `origin/`(첨부 원본)·`baseline/`(원본요약 1장)·`spec/`(기능정의서 N장, 요구 1항목=1장)으로 팬아웃되고, 같은 기능이 다른 docx로 다시 들어오면 신규 spec 없이 **기존 `spec/{기능}.md` 하나로 통합·보강(정규화 = 기능 dedup, 부서 무관)** 됨을 보장한다.

> 이 spec은 AXKG-DEC-007의 결정을 **외부 계약**(무엇을 보장하나)으로 내린 문서다. docx 요약①·PARA 분류②·문서화 승인 게이트③의 실행 계약은 각각 AXKG-SPEC-011/001/004가 SSOT이며 여기서 재정의하지 않는다 — 이 spec은 그 흐름 위에 얹히는 **project destination 팬아웃·기능 dedup·회사 프로젝트 스캐폴드**의 외부 계약만 규정한다.

> `projects/{corp}/baseline/`(런타임 산출물 = 넘어온 docx를 요약·정리한 "원본요약")은 제품 설계용 baseline 타입 메타문서(AXKG-BL-002 등)와 **이름만 같고 다른 개념**이다. 아래에서 전자는 항상 `projects/{corp}/baseline/`로 표기한다.

## 1. Context

### Meta

- Decision reference: AXKG-DEC-007(회사별 팬아웃·기능 dedup·slug·map.md 6개 결정), AXKG-DEC-005(4층 지식 아키텍처·파생지식 main+derived·연결 후보 컨텍스트·문서 lifecycle·요약① 적응형), AXKG-DEC-001(PARA 파이프라인·승인 게이트)
- Baseline reference: AXKG-BL-002
- Domain note: `Corp Project`(회사 프로젝트, `{corp}` slug로 식별), `Origin`(첨부 docx **원본 파일** — 손대지 않은 raw, `projects/{corp}/origin/`), `Project Baseline`(원본요약 — docx를 요약①이 정리한 md, document_type `baseline`), `Project Feature Spec`(기능정의서 — 기능 단위 문서, 요구 1항목=1장, document_type `feature_spec`), `Feature Dedup`(기능 정규화 = 같은 기능 재유입 시 신규 문서 없이 기존 spec 하나로 통합·보강, **부서 무관**), `Folder Map`(`map.md` MOC = 폴더 목차)
- Placement: 회사 프로젝트 생성은 "프로젝트 추가" 화면, 팬아웃 결과는 문서화 승인 게이트(③) 승인 후 지식 볼트 `projects/{corp}/` 트리에 나타난다.
- 접근 경계: 문서화 게이트·큐레이션 표면은 admin 전용이다(SSOT는 AXKG-SPEC-008이며 여기서 재서술하지 않는다). 확정 문서 트리 열람 경계는 AXKG-SPEC-013/008을 따른다.
- Corp 진입점(회사를 어떻게 아는가): 회사(`{corp}`)는 사용자가 "프로젝트 추가"로 **수동 생성**해 두고, intake 메모(AXKG-SPEC-003, 항상 요약 컨텍스트)에 적은 **회사명**이 분류 `project` 확정 시 그 기존 `projects/{corp}/`에 매칭돼 팬아웃 대상 corp가 된다. 업로드·분류가 프로젝트를 자동 생성하지 않는다.
- Open questions: 없음(AXKG-BL-002·AXKG-DEC-007에서 slug 충돌·docx 처리 OQ 종료, corp 진입점=intake 메모 회사명으로 확정 2026-07-21).

### Business Requirement

기업은 AX 전환 요구사항을 docx로 준다 — 한 회사가 기능 여러 개를 한 번에, 여러 docx로 나눠, 같은 기능을 반복해서 요구한다. 기존 `project` destination은 분류 시 `projects/{파일명}.md` flat 한 장만 만들어 회사·기능 구분과 반복 요구의 정리를 담지 못했다(AXKG-BL-002 Context). 이 spec은 회사라는 컨테이너, 기능이라는 단위, 같은 기능의 반복 유입을 하나로 합치는 dedup을 제공해, "이 회사가 실제로 뭘 요구했나(원본요약)"와 "그게 어떤 기능들로 쪼개지나(기능정의서)"를 분리 추적하고 회사 안에서 재사용 가능한 **기능 카탈로그**로 키운다. 기능은 특정 부서의 소유가 아니라 프로젝트의 기능 카탈로그다 — 어느 부서가 적었는지로 기능을 빼거나 가르지 않는다. **corp 진입점**: 회사는 사용자가 "프로젝트 추가"로 미리 수동 스캐폴딩해 두고(업로드/분류와 별개), intake 메모에 적은 회사명이 분류 `project` 확정 시 그 기존 `projects/{corp}/`에 매칭돼 팬아웃 대상 corp를 정한다.

### Scope

In scope:

- **회사 프로젝트 수동 생성(독립 스캐폴딩)** — "프로젝트 추가"에서 사용자 입력 회사명을 slugify(`더에스씨→the-sc`)해 `projects/{corp}/{origin,baseline,spec}/` + `baseline/map.md`·`spec/map.md` 스캐폴드를 만든다. 이는 **업로드/분류와 별개인 수동·독립 디렉토리 생성 작업**이며 AI가 프로젝트를 자동 생성하지 않는다. slug 충돌 시 사용자 확인(기존 사용/`{corp}-2` 신규 분기).
- **corp 바인딩 = intake 메모 회사명** — intake 메모(AXKG-SPEC-003, 항상 요약 컨텍스트)에 적은 회사명이 분류 `project` 확정 시 기존(수동 생성) `projects/{corp}/`와 매칭돼 팬아웃 대상 corp를 정한다. 매칭 프로젝트가 없는 경우의 처리는 이번 범위 밖(사용자가 프로젝트를 먼저 만들어두는 전제).
- **origin(첨부 원본) 보관** — 첨부 docx **원본 파일**은 요약 md와 별도로 `projects/{corp}/origin/`에 손대지 않은 raw로 보관한다.
- **docx 업로드 → project 팬아웃** — inbox docx 업로드(메모에 회사명) → 요약①(적응형, 기능별 줄글) → PARA `project` 분류(메모 회사명으로 corp 매칭) → 문서화 게이트 승인 시 `baseline/{원본요약}.md` 1장 + `spec/{기능}.md` N장으로 팬아웃. docx는 텍스트 추출만, 기능 구조화는 요약①.
- **승인 게이트 팬아웃 메커니즘(main+derived 재사용)** — 게이트가 초안 revision 1개에 `main_document`(원본요약) + `derived_suggestions[]`(기능별 초안: 신규 `create_feature_spec` / dedup 매칭 `supplement_existing_feature`)를 담아 한 화면에서 검토·승인하게 한다(§4 팬아웃 메커니즘).
- **기능 dedup(정규화)** — 같은 `{corp}` 안에서 같은 기능이 다른 docx로 다시 들어오면 신규 spec 없이 기존 `spec/{기능}.md` 하나로 통합하고, 새 요구가 디테일을 더하면 상세요구/유저플로우를 보강(supplement)한다. **부서 귀속·요청 이력 없음.**
- **기존 개념 차용 링크** — 각 기능정의서의 `## 8. 연결`에 AI가 retriever + documents index로 훑은 ax-graph 기존 역량/문서를 `[[graph-chat]]` 같은 wikilink로 제안한다(AXKG-DEC-005 연결 후보 컨텍스트 재사용).
- **map.md 자동 갱신** — 문서 apply 시점에 `baseline/map.md`·`spec/map.md`(MOC)를 자동 재생성(문서 목록 반영).

Out of scope:

- 요약①·분류②·문서화 게이트③의 실행/승인 계약 자체 — AXKG-SPEC-011/001/004 소관(이 spec은 그 위에 얹힘). 파생지식 apply 규칙·경로 조립 주체는 AXKG-SPEC-004가 SSOT.
- docx 텍스트 추출 어댑터의 수집 계약 세부 — AXKG-SPEC-012 소관(표 보존·이미지 대체텍스트·병합셀 등 파싱 계약은 두지 않음, AXKG-DEC-007 D5).
- 경로 컨벤션·wikilink/frontmatter 계약 세부 — AXKG-SPEC-005 소관.
- 문서 템플릿(원본요약·기능정의서)의 DB 동적 관리·버저닝 세부 — AXKG-SPEC-010 소관.
- 실제 프롬프트 문구, DB 스키마·컬럼, 프론트 컴포넌트 파일·라우트 세부 — 코드/후속 work 소관.
- **회사를 넘는 전역 capability 레지스터**(`capabilities/` 같은 공통 카탈로그) — 도입하지 않음(AXKG-DEC-007 D4).

## 2. UX Contract

### Placement

회사 프로젝트 생성은 "프로젝트 추가" 화면(모달 또는 폼)에서, 팬아웃 결과 열람은 지식 볼트 `projects/{corp}/` 트리에서 이뤄진다. 팬아웃 자체는 기존 문서화 승인 게이트(③, AXKG-SPEC-004) 승인의 결과로 발생한다.

```text
+-----------------------------------------------------------+
| 프로젝트 추가                                              |
+-----------------------------------------------------------+
|  회사명  [ 더에스씨            ]                           |
|  slug 미리보기:  the-sc                                    |
|  ( 충돌 시 )  ⚠ 이미 the-sc 프로젝트가 있습니다            |
|              [ 기존에 추가 ]   [ 새 프로젝트로 (the-sc-2) ] |
|                              [ 취소 ]   [ 만들기 ]         |
+-----------------------------------------------------------+

+---------------------+-------------------------------------+
| Projects 트리       | 선택 문서                            |
| ▾ the-sc/           |  spec/shared-calendar-worklog.md     |
|   ▾ origin/         |  # 부서 공유 캘린더 및 업무일지        |
|     the-sc-req.docx |  > 한 줄 정의 …                      |
|   ▾ baseline/       |  ## 3. 유저 플로우 (표)              |
|     the-sc-요약.md   |  ## 8. 연결  [[the-sc-원본요약]] …    |
|   ▾ spec/           |  <본문 렌더>                         |
|     shared-cal…md   |                                     |
|     hospital-rev…md |                                     |
|   (map.md 자동)     |                                     |
+---------------------+-------------------------------------+
```

### U-1. 프로젝트 추가 — 회사명 입력 · slug 미리보기 (수동·독립 스캐폴딩)

- **상태**: 입력 대기 / 입력 중(slug 실시간 미리보기) / 충돌 감지 / 생성 중 / 생성 완료 / 권한없음(admin 아님)
- **문구**: 라벨 "회사명", placeholder "회사명을 입력하세요(예: 더에스씨)", 미리보기 "slug 미리보기: `{corp}`". 빈 입력 시 "회사명을 입력해 주세요."
- **CTA**: `만들기`(회사명 trim 후 non-empty일 때 활성), `취소`
- **기대 결과**: 충돌이 없으면 `projects/{corp}/{origin,baseline,spec}/` + 각 `map.md` 스캐폴드가 생성되고 Projects 트리에 `{corp}/`가 나타난다. 충돌이면 U-2 확인 분기로 전환. 이 작업은 **수동·독립 디렉토리 스캐폴딩**이다 — intake(탭+메모)·docx 업로드·분류와 분리되며, 업로드·분류가 프로젝트를 자동 생성하지 않는다. 이후 docx가 이 회사로 팬아웃되려면 intake 메모의 회사명이 이 `{corp}`에 매칭돼야 한다.

### U-2. slug 충돌 확인 모달

- **상태**: 미표시(충돌 없음) / 표시(같은 slug의 회사 프로젝트가 이미 존재)
- **문구**: "이미 `{corp}` 프로젝트가 있습니다. 어떻게 할까요?" — 옵션 설명: 기존 사용 = 기존 `{corp}` 프로젝트를 그대로 씀(중복 생성 안 함), 새 프로젝트 = `{corp}-2` 등 suffix로 분리 생성
- **CTA**: `기존 사용`(기존 corp 재사용), `새 프로젝트로(`{corp}-2`)`(suffix 신규), `취소`
- **기대 결과**: `기존 사용` → 기존 `{corp}` 프로젝트를 그대로 쓴다(스캐폴드 중복 생성 안 함). `새 프로젝트로` → `{corp}-2` 스캐폴드를 새로 만든다. 회사 경계 판단은 사람이 명시적으로 내린다(AXKG-DEC-007 D2). 팬아웃은 이 프로젝트 추가와 별개로, 이후 매칭된 회사명 docx가 문서화 게이트 승인될 때 일어난다.

### U-3. Corp Project 트리 뷰

- **상태**: 정상(문서 있음) / 빈 폴더(스캐폴드만, 문서 0) / 로딩 / 권한없음
- **문구**: `{corp}/` 아래 `origin/`·`baseline/`·`spec/` 하위 트리와 각 항목명(origin=첨부 원본 파일, baseline=원본요약, spec=기능정의서). `map.md`는 자동 생성 항목으로 표시.
- **CTA**: 트리 노드 선택 → 우측 렌더(baseline/spec은 Markdown 본문 렌더, origin은 첨부 원본 — 읽기/다운로드, 열람 경계는 AXKG-SPEC-013/008)
- **기대 결과**: `{corp}` 프로젝트의 첨부 원본(origin)·원본요약(baseline)·기능정의서(spec) 목록을 한 화면에서 조망하고, 선택 문서의 본문을 읽는다. project 층위는 `origin/`+`baseline/`+`spec/` 3층만이며 area/resource는 이 트리에 나타나지 않는다(전역 PARA 흐름 그대로, AXKG-DEC-007 D3).

### U-4. 팬아웃 게이트 결과 (문서화 게이트 승인 후)

- **상태**: 게이트 승인 전(초안 revision 표시) / 승인 후(origin 보관 + baseline 1장 + spec N장 생성·보강) / dedup 매칭(신규 spec 없이 기존 spec 보강)
- **문구**: 문서화 승인 게이트(③) 한 화면에 `main_document`(원본요약) 초안 + `derived_suggestions[]`(기능별 초안 N개) + 각 기능 초안의 차용 링크(`## 8. 연결`)가 함께 표시된다. 신규 기능은 생성될 `.md` 전문 preview로, dedup 매칭 기능은 기존 spec 대비 보강 diff로 표시된다(표시·승인 UI 계약은 AXKG-SPEC-004 U-2~U-5 재사용).
- **CTA**: 없음(팬아웃은 게이트 `승인`의 결과로 실행된다 — 별도 팬아웃 트리거 없음). 개별 기능 초안 승인/보류 버튼 없이 게이트 레벨 `피드백`/`승인`만 존재(AXKG-SPEC-004).
- **기대 결과**: 게이트 승인 시 project apply가 단일 baseline 한 장 대신 origin 보관 + baseline 1 + spec N 팬아웃(또는 기존 spec 보강)으로 적용되고, 해당 폴더 `map.md`가 자동 재생성되며 그래프 엣지가 갱신된다.

### U-5. 기능정의서 문서 뷰

- **상태**: 정상 / 신규 생성분 / dedup 보강분(상세요구·유저플로우가 후속 docx로 자란 문서)
- **문구**: 기능정의서 본문 — 한 줄 정의, 요구 배경, 기능 정의, 유저 플로우(표), 예시, 상세 요구, 수용 기준, `## 8. 연결`(원본요약 `[[{corp}-원본요약]]` + 차용 링크). frontmatter `feature_id`(`{corp}-F-NN`)·`status`(draft|reviewing|confirmed)·`priority`.
- **CTA**: 없음(읽기 전용)
- **기대 결과**: 한 기능이 무엇이고 어떻게 동작하며 어떤 수용 기준을 갖는지 한 문서에서 확인한다. 같은 기능이 여러 docx로 들어왔어도 **하나의 기능정의서**로 통합되어 갈라지지 않는다(부서별로 쪼개지 않음).

## 3. User Scenario

### S-1. Admin — 회사 첫 요구(프로젝트 신규 생성 + 팬아웃)

1. admin이 "프로젝트 추가"에서 회사명 "더에스씨"를 입력한다(수동·독립 스캐폴딩). 시스템이 실시간으로 slug `the-sc`를 미리보기로 보여준다(U-1).
2. `the-sc`와 충돌하는 기존 프로젝트가 없으므로 `만들기` → `projects/the-sc/{origin,baseline,spec}/` + 각 `map.md` 스캐폴드가 생성된다. 이 단계는 docx와 무관한 디렉토리 생성이다.
3. admin이 회사 요구 docx를 inbox에 업로드한다(`source_channel=upload`, docx 탭 — AXKG-SPEC-003 intake). **이때 intake 메모에 회사명("더에스씨")을 적는다**(항상 요약 컨텍스트로 동반). 첨부 원본은 손대지 않은 raw로 보관 대상이 되고(→ `origin/`), 어댑터는 docx 본문 텍스트만 추출한다(AXKG-SPEC-012, 텍스트 추출 경로).
4. 요약①이 원문 구조를 따라 기능별 줄글(기능 1·2·3…)로 적응형 요약을 만든다(AXKG-SPEC-011 ①, AXKG-DEC-005 A). 이 산출물이 `baseline/{원본요약}.md`의 내용이 된다.
5. 분류②에서 `project` destination으로 승인되면, **메모의 회사명("더에스씨")이 앞서 만든 기존 `projects/the-sc/`에 매칭돼 팬아웃 대상 corp가 `the-sc`로 정해지고**, 그 아래 문서화 승인 게이트(③)가 열린다(AXKG-SPEC-001/004).
6. 게이트가 초안 revision 1개를 낸다 — `main_document` = 원본요약(→ `baseline/`), `derived_suggestions[]` = 기능별 초안 N개(→ `spec/`, 요구 1항목=1장, 전부 신규이므로 `create_feature_spec`). 각 기능 초안의 `## 8. 연결`에는 AI가 retriever + documents index로 훑은 ax-graph 기존 역량 차용 링크(예: `[[graph-chat]]`)가 들어간다. admin은 한 화면에서 원본요약 + N개 기능 초안 + 차용 링크를 함께 검토한다(U-4).
7. admin이 게이트 `승인`을 누르면 같은 승인 단위 안에서 origin 원본 보관 + `baseline/{원본요약}.md` + `spec/{기능}.md` N장 생성 + `baseline/map.md`·`spec/map.md` 자동 재생성 + 그래프 엣지 갱신이 일어난다.
8. Projects 트리(U-3)에 `the-sc/`와 그 origin/baseline/spec 문서들이 나타난다.

### S-2. Admin — 같은 기능이 다른 docx로 다시 들어옴(기능 dedup·보강, 부서 무관)

1. `projects/the-sc/spec/shared-calendar-worklog.md`가 이미 존재한다.
2. 같은 회사의 **다른 docx**(다른 시점·다른 문서)가 inbox에 업로드되어 `the-sc`(기존 프로젝트) 대상으로 요약①·분류②를 거친다. 그 docx에도 "부서 공유 캘린더/업무일지"에 해당하는 요구가 담겨 있다.
3. 문서화 게이트가 초안을 만들 때, 시스템이 같은 `{corp}` 폴더 안 기존 기능정의서와 매칭을 시도한다(index/stem resolution + retriever, AXKG-DEC-007 D4).
4. 기존 `shared-calendar-worklog.md`와 **같은 기능으로 판정되면**, `derived_suggestions[]`의 해당 항목이 신규 `create_feature_spec`이 아니라 **`supplement_existing_feature`**(기존 spec 보강)로 나온다 — **신규 spec을 만들지 않는다.** 새 docx가 상세요구·유저플로우 디테일을 더하면 그 내용을 반영한 **보강 전문**이 초안에 담긴다(부서 귀속·요청 이력을 붙이지 않는다).
5. admin이 게이트 `승인`을 누르면 기존 spec이 보강 전문으로 overwrite되고(수정 전문 overwrite, AXKG-SPEC-004), `spec/map.md`가 자동 재생성된다. 하나의 기능정의서가 상세를 축적하며 자란다(중복 문서로 갈라지지 않음).
6. 같은 내용이 새로 더할 것 없이 또 들어오면 기존 spec은 변하지 않는다(**dedup 멱등**, §5). 다른 회사가 같은 기능을 요구하면 그 회사의 `projects/{다른-corp}/spec/`에 별개 spec으로 생성되며 `the-sc`의 것과 합쳐지지 않는다(회사 넘는 정규화 없음).

### S-3. Admin — 프로젝트 추가 시 이름 충돌(기존 사용/신규 분기)

1. admin이 "프로젝트 추가"에서 이미 존재하는 회사명을 입력해 slug가 기존 `{corp}`와 충돌한다(이 시나리오는 수동 스캐폴딩에 한정 — docx와 무관).
2. 시스템이 충돌을 감지하고 확인 모달을 띄운다: "이미 `{corp}` 프로젝트가 있습니다. 어떻게 할까요?"(U-2).
3. admin이 `기존 사용`을 선택하면 기존 `{corp}` 프로젝트를 그대로 쓴다(스캐폴드 중복 생성 안 함). 이후 이 회사명을 메모에 적은 docx가 이 `{corp}`로 팬아웃된다.
4. admin이 `새 프로젝트로`를 선택하면 `{corp}-2` 등 suffix 스캐폴드가 새로 생성된다(별개 회사로 분리).
5. admin이 `취소`하면 프로젝트가 생성되지 않는다. 회사 경계 판단은 사람이 명시적으로 내리며 시스템이 자동 병합/분리하지 않는다.

### S-4. System — project가 아닌 분류로 확정되면 팬아웃하지 않음

1. 업로드된 docx가 분류②에서 `project`가 아닌 destination(`area`/`resource`/`archive`)으로 승인된다.
2. 이 경우 회사 프로젝트 팬아웃은 일어나지 않는다 — 문서화 게이트는 기존 destination별 단일 산출(area→permanent, resource→reference)을 따른다(AXKG-SPEC-004).
3. 팬아웃·기능 dedup·`projects/{corp}/` map.md 갱신은 **`project` destination에서만** 관찰된다.

## 4. Interface Contract

### API Contract

| Method | Path | 요약 | 권한 |
|---|---|---|---|
| GET | `/projects:slug-preview?name=` | 입력 회사명 → slug 미리보기 + 충돌 여부 반환 | admin |
| POST | `/projects` | 회사 프로젝트 스캐폴드(`{corp}/{origin,baseline,spec}/` + 각 map.md) 생성. 충돌 시 `on_conflict`로 합류/신규 분기 | admin |
| GET | `/projects` | 회사 프로젝트 목록(트리 루트) 조회 | admin |
| GET | `/projects/{corp}` | 한 회사 프로젝트의 `origin/`·`baseline/`·`spec/` 트리와 문서 목록 조회 | admin |

- docx 업로드는 별도 신규 엔드포인트를 두지 않고 AXKG-SPEC-003 inbox 업로드(`source_channel=upload`, docx 확장 허용)를 재사용한다.
- **팬아웃과 기능 dedup은 별도 API가 없다** — 기존 문서화 승인 게이트(③)의 `POST /gates/{gate_id}/approve`(AXKG-SPEC-004/002 공통 게이트 API) apply 결과로 실행된다. project destination의 apply가 단일 baseline 한 장 대신 origin 보관 + `main_document`(baseline) + `derived_suggestions[]`(spec N) 팬아웃으로 확장된 것이다.
- `map.md` 재생성도 별도 API가 없다 — 문서 apply 시점에 파이프라인이 자동 수행한다.
- 확정 문서 본문 열람은 AXKG-SPEC-013 문서 라이브러리 read-through를 재사용한다.

### 팬아웃 메커니즘 (파생지식 main+derived 재사용)

project로 분류된 source의 문서화 승인 게이트는 ax-graph 기존 **파생지식 모델(`main_document` + `derived_suggestions[]`, AXKG-SPEC-004)** 을 그대로 재사용한다. 이 절은 그 모델이 project destination에서 무엇으로 매핑되는지의 외부 계약이며, **파생지식 apply 규칙·경로 디렉토리 조립 주체·검증은 AXKG-SPEC-004가 SSOT**다.

> **생성 방식 note (2026-07-21, AXKG-DEC-008)**: 아래 draft(원본요약 + 기능정의서 N)의 **생성 메커니즘**은 단일 문서화 task에서 **plan-then-fanout**(① 요약+plan → ② 기능별 독립 task 병렬 → ③ fan-in 조립)으로 리팩터한다(대용량 docx 타임아웃 실측 대응, 구현 AXKG-WORK-012). **이 절의 외부 계약(무엇이 나오나 = main+derived, origin·경로·3층)은 불변**이며 바뀌는 것은 어떻게 만드느냐뿐이다.

- **승인 전(draft)**: 게이트가 초안 revision 1개를 생성한다.
  - `main_document` = **원본요약** → `projects/{corp}/baseline/`. document_type `baseline`, 템플릿 `project_source_summary`(AXKG-SPEC-010). 원본요약의 `## 기능 목록`은 추출된 기능 N개를 각각 `[[기능-spec-stem]]`으로 링크해 baseline↔spec 그래프를 연다.
  - `derived_suggestions[]` = **기능별 초안** → `projects/{corp}/spec/`. document_type `feature_spec`, 템플릿 `project_feature_spec`(AXKG-SPEC-010). suggestion_type은 두 가지 — 신규 기능이면 `create_feature_spec`, 같은 `{corp}`의 기존 기능과 매칭되면 `supplement_existing_feature`(기존 spec 보강).
  - 각 기능 초안의 `## 8. 연결`에는 AI가 retriever + documents index 스냅샷(AXKG-DEC-005 연결 후보 컨텍스트)으로 훑은 ax-graph 기존 역량/문서 차용 링크(`[[graph-chat]]` 등)와 원본요약 링크(`[[{corp}-원본요약]]`)가 wikilink로 들어간다. 그래프 엣지의 단일 소스는 본문 `[[ ]]`다(AXKG-SPEC-005).
- **사용자 검토·승인**: 한 게이트 화면에서 원본요약 + N개 기능 초안 + 차용 링크를 함께 검토하고 게이트 레벨 `승인`/`피드백`으로 처리한다(개별 기능 승인/보류 없음, 새 승인 표면 없음 — 기존 게이트 확장, AXKG-SPEC-004).
- **승인 시 apply(같은 승인 단위)**: origin 원본 보관(→ `origin/`) + `baseline/{원본요약}.md` + `spec/{기능}.md` N장 생성/보강 + `baseline/map.md`·`spec/map.md` 자동 재생성 + 본문 `[[ ]]` 기반 그래프 엣지 갱신을 한 트랜잭션 경계로 처리한다.

### Request / Response

- `GET /projects:slug-preview?name=더에스씨` → `{ "slug": "the-sc", "conflict": false }` (또는 `conflict: true`이면 기존 프로젝트 존재).
- `POST /projects` body → `{ "name": "더에스씨", "on_conflict": "merge" | "create_new" | null }`. 충돌 없으면 `on_conflict` 불요. 성공 → `{ "slug": "the-sc", "created": true }`(신규) / `{ "slug": "the-sc", "merged": true }`(합류) / `{ "slug": "the-sc-2", "created": true }`(suffix 신규).
- `GET /projects/{corp}` → `origin`·`baseline`·`spec` 각 폴더의 항목 목록(문서명 요지). 트리·본문 렌더 계약은 AXKG-SPEC-013.

긴 payload schema는 내부 구현/후속 work 소관이며 여기서는 계약 필드 요지만 둔다.

### Validation

| 필드 | 규칙 |
|---|---|
| `name`(회사명) | trim 후 non-empty. 빈 값은 거부 |
| `slug`(파생) | 시스템이 회사명을 slugify해 생성(사용자 직접 입력 아님). URL-safe(소문자·하이픈) |
| `on_conflict` | 기존 slug와 충돌할 때만 필수. `merge`(합류) 또는 `create_new`(suffix 신규) |
| 업로드 파일 | `.md` 또는 `.docx`만 허용(그 외는 AXKG-SPEC-003 intake validation에서 거부). docx는 텍스트 추출만 |
| 기능 dedup | 같은 `{corp}` 안에서 같은 기능이 다시 들어오면 신규 spec을 만들지 않고 기존 spec을 보강한다. 더할 내용이 없으면 기존 spec 불변(멱등) |

### Case Matrix

| 에러 코드 | 백엔드 출력 | 프론트 출력 | 표시 위치 |
|---|---|---|---|
| `EMPTY_CORP_NAME` | 회사명 trim 후 empty | 회사명을 입력해 주세요. | 프로젝트 추가(U-1) |
| `SLUG_CONFLICT` (409) | slugify 결과가 기존 `{corp}`와 충돌 + `on_conflict` 미지정 | 기존 `{corp}` 프로젝트에 추가할까요? (합류/새 프로젝트 선택) | slug 충돌 확인 모달(U-2) |
| `INVALID_ON_CONFLICT` | `on_conflict` 값이 `merge`/`create_new`가 아님 | 처리 방식을 다시 선택해 주세요. | slug 충돌 확인 모달(U-2) |
| `UNSUPPORTED_UPLOAD_TYPE` | `.md`/`.docx` 외 업로드(AXKG-SPEC-003) | 지원하지 않는 파일 형식입니다. | inbox 업로드 |
| `NOT_PROJECT_DESTINATION` | project가 아닌 destination으로 분류된 source에 팬아웃 시도 | 회사 프로젝트 팬아웃 대상이 아닙니다. | 문서화 게이트(③) |
| `PROJECT_NOT_FOUND` (404) | 합류 대상 `{corp}` 프로젝트 부재 | 대상 프로젝트를 찾을 수 없습니다. | 프로젝트 추가 / 트리 |
| `FEATURE_MATCH_AMBIGUOUS` | dedup 매칭이 복수 기존 spec과 모호하게 겹침 | 유사 기능이 여러 개입니다. 신규로 생성합니다. | 문서화 게이트(③) 파생지식 |

- `SLUG_CONFLICT`은 하드 에러가 아니라 **사용자 결정을 요구하는 분기**다 — 클라이언트는 U-2 모달을 띄우고 `on_conflict`를 실어 재요청한다.
- `FEATURE_MATCH_AMBIGUOUS`는 dedup(`supplement_existing_feature`) 대신 **신규 spec 생성(`create_feature_spec`)으로 안전하게 폴백**한다 — 잘못 합치는 것보다 갈라두고 사람이 판단하게 둔다. 매칭은 같은 `{corp}` 경계 안으로 한정한다(회사 넘는 정규화 없음).
- 경로 컨벤션 위반(`PATH_NOT_ALLOWED`)·깨진 wikilink(`BROKEN_WIKILINK`) 등 문서 apply 공통 거부 코드는 AXKG-SPEC-004/005가 SSOT이며 여기서 재서술하지 않는다.

### Flow

```mermaid
sequenceDiagram
    actor Admin
    participant FE
    participant BE
    participant AI
    participant Vault as 지식 볼트

    Admin->>FE: "프로젝트 추가" 회사명 입력
    FE->>BE: GET /projects:slug-preview
    BE-->>FE: slug + conflict 여부
    alt slug 충돌
        FE->>Admin: 확인 모달(합류 / 새 프로젝트)
        Admin->>FE: on_conflict 선택
    end
    FE->>BE: POST /projects (name, on_conflict?)
    BE->>Vault: {corp}/{origin,baseline,spec}/ + map.md 스캐폴드 (수동·독립)
    Note over Admin,Vault: 위 프로젝트 추가는 docx와 별개인 수동 스캐폴딩
    Admin->>BE: docx inbox 업로드 (source_channel=upload, 메모=회사명)
    BE->>AI: 텍스트 추출(SPEC-012) → 요약①(적응형 기능별 줄글, SPEC-011; 메모 동반)
    AI-->>BE: 원본요약 + 기능 목록
    BE->>BE: 분류②(project) → 메모 회사명으로 기존 projects/{corp}/ 매칭
    BE->>AI: 문서화 초안 (main_document + derived_suggestions[])
    Note over AI: 기존 기능 매칭 → create_feature_spec / supplement_existing_feature<br/>연결 후보 컨텍스트로 차용 링크 제안
    AI-->>BE: main=원본요약 + derived=기능 초안 N (신규/보강)
    Admin->>BE: 문서화 게이트 approve (SPEC-004)
    BE->>Vault: origin 원본 보관 + baseline/{원본요약}.md + spec/{기능}.md N장 생성·보강
    BE->>Vault: baseline/map.md · spec/map.md 자동 재생성 + 그래프 엣지 갱신
    BE-->>FE: Projects 트리 갱신
```

### State / Lifecycle

회사 프로젝트 문서(원본요약·기능정의서)는 확정 문서 lifecycle(`current`/`superseded`·`version`·producing 링크)을 그대로 따른다 — SSOT는 AXKG-SPEC-004 Document Lifecycle이며 여기서 재정의하지 않는다. 기능 dedup 보강은 상태 전이가 아니라 **문서 전문의 성장(supplement overwrite + version++)** 으로 표현된다. 기능정의서 자체는 frontmatter `status`(draft|reviewing|confirmed)를 갖는다(템플릿 계약, AXKG-SPEC-010). 회사 프로젝트 컨테이너는 별도 상태 머신을 두지 않는다(존재 여부만: 스캐폴드 생성됨 / 없음).

### Data Contract

외부에 드러나는 resource·field만 계약 수준으로 둔다(DB 컬럼/인덱스 전문은 코드/migration이 SoT). 경로 컨벤션·frontmatter 어휘의 SSOT는 AXKG-SPEC-005, 템플릿 계약은 AXKG-SPEC-010이다. **corp 결정의 소스**는 intake 메모의 회사명이다 — 분류 `project` 확정 시 메모 회사명을 기존(수동 생성) `CorpProject.display_name`/`slug`에 매칭해 팬아웃 대상 corp를 정한다(메모 계약은 AXKG-SPEC-003).

| Resource | Field | 설명 |
|---|---|---|
| CorpProject | `slug` | `{corp}` 식별자. 회사명 slugify 결과(충돌 시 `-2` 등 suffix) |
| CorpProject | `display_name` | 사용자 입력 원본 회사명 |
| CorpProject | `folders` | `origin/`·`baseline/`·`spec/` 3층(고정). area/resource는 포함하지 않음 |
| Origin | `path` | `{MARKDOWN_ROOT}/projects/{corp}/origin/{원본파일}.docx` — 첨부 docx **원본 raw 파일**. markdown 문서와 **같은 바인드 마운트**(`AXKG_MARKDOWN_ROOT`=컨테이너 `/workspace`, 호스트 `AXKG_WORKSPACE_HOST_PATH` 기본 `./data/documents`)에 저장하되, **그래프 문서 노드가 아니다** — 바이너리라 `documents` 테이블/인덱스/retriever에 편입하지 않는다 |
| ProjectBaseline | `document_type` | `baseline`(원본요약, docx를 요약①이 정리한 원본 SoT) |
| ProjectBaseline | `path` | `projects/{corp}/baseline/{원본요약}.md`(경로 SSOT: AXKG-SPEC-005) |
| ProjectBaseline | `template` | `project_source_summary`(AXKG-SPEC-010). `## 기능 목록`이 각 기능을 `[[기능-spec-stem]]`으로 링크 |
| ProjectFeatureSpec | `document_type` | `feature_spec`(기능정의서, 요구 1항목=1장) |
| ProjectFeatureSpec | `path` | `projects/{corp}/spec/{기능}.md` |
| ProjectFeatureSpec | `template` | `project_feature_spec`(AXKG-SPEC-010) |
| ProjectFeatureSpec | `feature_id` / `status` / `priority` | `{corp}-F-NN` / draft·reviewing·confirmed / high·mid·low(frontmatter, 템플릿 계약) |
| DerivedSuggestion(project) | `suggestion_type` | `create_feature_spec`(신규 기능) 또는 `supplement_existing_feature`(같은 corp 기존 기능 dedup 보강). 파생지식 모델·apply는 AXKG-SPEC-004 SSOT |
| FolderMap | `path` | `projects/{corp}/{baseline,spec}/map.md`. 문서 apply 시 자동 재생성(MOC) |

## 5. Implementation Rules

- **회사 경계는 사용자가 통제한다** — slug는 시스템이 정규화하되, 프로젝트 생성·기존 사용/신규 분기는 사용자 명시 액션으로만 일어난다. 시스템이 회사 경계를 자동 추론하거나 자동 병합하지 않는다(AXKG-DEC-007 D2).
- **corp 바인딩 = intake 메모 회사명, 프로젝트 추가는 수동·독립** — 회사(`{corp}`)는 사용자가 "프로젝트 추가"로 미리 수동 스캐폴딩하고(업로드/분류와 별개, **AI가 프로젝트를 자동 생성하지 않는다**), 분류 `project` 확정 시 intake 메모(AXKG-SPEC-003, 항상 요약 컨텍스트)의 회사명을 기존 `projects/{corp}/`에 매칭해 팬아웃 대상 corp를 정한다. 매칭 프로젝트가 없는 경우의 정교한 처리는 이번 범위 밖이다(사용자가 프로젝트를 먼저 만들어두는 전제).
- **기능은 부서 귀속이 아니라 프로젝트의 기능 카탈로그다** — 기능정의서에 요청부서·요청 이력을 저장하지 않는다. 어느 부서가 적었는지로 기능을 빼거나 부서별로 문서를 가르지 않는다(AXKG-DEC-007, 사용자 승인 2026-07-21).
- **기능 dedup 멱등성** — 같은 `{corp}` 안에서 같은 기능이 다른 docx로 다시 들어오면 신규 spec을 만들지 않고 기존 spec을 보강한다(`supplement_existing_feature`). 새로 더할 상세가 없으면 기존 spec은 변하지 않는다. dedup 매칭은 반드시 같은 `{corp}` 경계 안으로 한정하며, 회사를 넘는 spec 재사용·통합은 하지 않는다(AXKG-DEC-007 D4).
- **팬아웃 = 파생지식 main+derived 재사용** — project 문서화 게이트는 `main_document`(원본요약) + `derived_suggestions[]`(기능별 초안, `create_feature_spec`/`supplement_existing_feature`)를 한 revision에 담는다(§4 팬아웃 메커니즘). 파생지식 apply 규칙·경로 디렉토리 조립 주체·검증은 AXKG-SPEC-004가 SSOT다.
- **기존 개념 차용 링크** — 각 기능 초안의 `## 8. 연결`에는 retriever + documents index 스냅샷(AXKG-DEC-005 연결 후보 컨텍스트)으로 훑은 ax-graph 기존 역량 차용 wikilink와 원본요약 링크가 들어간다. 그래프 엣지의 단일 소스는 본문 `[[ ]]`이며 빈 `[[ ]]`는 두지 않는다(AXKG-SPEC-005).
- **origin 보관 = 바인드 마운트 raw 파일(non-node)** — 첨부 docx 원본 파일은 요약 md와 별도로, markdown 문서와 **같은 바인드 마운트**(`AXKG_MARKDOWN_ROOT`=컨테이너 `/workspace`, 호스트 `AXKG_WORKSPACE_HOST_PATH` 기본 `./data/documents`) 밑 `projects/{corp}/origin/{원본파일}.docx`에 손대지 않은 raw로 저장한다. origin은 **그래프 문서 노드가 아니다** — 바이너리라 `documents` 테이블/인덱스/retriever에 편입하지 않고, 요약·가공 대상이 아니라 감사·역참조용 원본이다.
- **project 분류에서만 팬아웃** — 팬아웃·기능 dedup·`projects/{corp}/` map.md 갱신은 `project` destination으로 승인된 source에서만 발생한다. `area`/`resource`/`archive`는 기존 destination별 단일 산출을 따른다(AXKG-SPEC-004).
- **map.md 자동 갱신** — 문서 apply 시점에 해당 폴더 `map.md`(MOC)를 자동 재생성한다(문서 목록 반영). 수동 갱신이 아니며, 팬아웃/보강 apply와 같은 승인 단위 안에서 갱신된다(부분 갱신으로 목록이 문서 실재와 어긋나지 않는다).
- **docx는 텍스트 추출만** — 어댑터는 docx 본문 텍스트만 추출하고, 기능별 구조화는 어댑터가 아니라 적응형 요약①이 담당한다. 표 보존·이미지 대체텍스트·병합셀·중첩표·스캔이미지 같은 파싱 계약은 두지 않는다(AXKG-DEC-007 D5, 어댑터 계약 SSOT는 AXKG-SPEC-012).
- **기존 게이트 위에 얹는다** — 팬아웃·dedup은 신규 승인 표면을 만들지 않고 문서화 승인 게이트(③) apply를 확장한다. 승인 전에는 어떤 `projects/{corp}/` 문서도 파일로 만들지 않는다(제안 상태로만 존재, AXKG-SPEC-004).
- **경로/링크 계약 준수** — `projects/{corp}/{origin,baseline,spec}/` 경로와 wikilink/frontmatter는 AXKG-SPEC-005 계약을 따른다. 경로 디렉토리는 AI가 아니라 시스템이 조립한다(AXKG-SPEC-004 §4 경로 결정 주체 재사용).
- **접근 경계** — 회사 프로젝트 생성·docx 큐레이션·문서화 게이트 표면은 admin 전용이다(SSOT AXKG-SPEC-008). 확정 문서 트리 열람 경계는 AXKG-SPEC-013/008을 따른다.

라우트·컴포넌트 파일, service/repository 구조, 프롬프트 문구, DB migration은 후속 work·코드 소관이다.

## 6. Verification

### Acceptance Criteria

- [ ] "프로젝트 추가"에서 회사명을 입력하면 slug 미리보기가 실시간으로 보인다.
- [ ] 충돌 없는 회사명으로 `만들기` 시 `projects/{corp}/{origin,baseline,spec}/` + 각 `map.md` 스캐폴드가 생성된다.
- [ ] 빈 회사명은 `EMPTY_CORP_NAME`으로 거부된다.
- [ ] slug가 기존 `{corp}`와 충돌하면 확인 모달이 뜨고, `기존 사용`=기존 corp 재사용 / `새 프로젝트로`=`{corp}-2` suffix 신규로 분기된다.
- [ ] 프로젝트 추가는 수동·독립 디렉토리 스캐폴딩이며, docx 업로드/분류가 프로젝트를 자동 생성하지 않는다.
- [ ] docx 업로드 시 intake 메모의 회사명이 분류 `project` 확정 시 기존 `projects/{corp}/`에 매칭돼 그 corp로 팬아웃된다.
- [ ] docx 업로드가 텍스트 추출만 거쳐(표/이미지 파싱 계약 없음) 요약①에서 기능별 줄글로 구조화된다.
- [ ] 첨부 docx 원본이 요약 md와 별도로 `projects/{corp}/origin/`에 raw로 보관된다.
- [ ] `project`로 승인된 source의 문서화 게이트가 `main_document`(원본요약) + `derived_suggestions[]`(기능별 초안 N개)를 한 revision·한 화면에 담고, 게이트 레벨 `승인`/`피드백`만 노출한다(개별 기능 승인 없음).
- [ ] 각 기능 초안의 `## 8. 연결`에 원본요약 링크와 ax-graph 기존 역량 차용 wikilink가 들어가고, 빈 `[[ ]]`가 없다.
- [ ] 게이트 승인 시 origin 보관 + `baseline/{원본요약}.md` 1장 + `spec/{기능}.md` N장(요구 1항목=1장) 팬아웃 + map.md 재생성 + 그래프 엣지 갱신이 같은 승인 단위에서 일어난다.
- [ ] 같은 `{corp}` 안에서 같은 기능이 다른 docx로 다시 들어오면 신규 spec 없이 기존 `spec/{기능}.md`가 `supplement_existing_feature`로 보강된다(부서 귀속·요청 이력 없음).
- [ ] 더할 상세가 없는 동일 기능 재유입은 기존 spec을 바꾸지 않는다(dedup 멱등).
- [ ] 다른 회사가 같은 기능을 요구하면 `projects/{다른-corp}/spec/`에 별개 spec으로 생성되고 합쳐지지 않는다(회사 넘는 정규화 없음).
- [ ] dedup 매칭이 모호하면 신규 spec으로 폴백한다(`FEATURE_MATCH_AMBIGUOUS`).
- [ ] 문서 apply 시점에 `baseline/map.md`·`spec/map.md`가 자동 재생성되어 문서 목록을 반영한다.
- [ ] 원본요약의 `## 기능 목록`이 각 기능정의서를 `[[기능-spec-stem]]`으로 링크해 baseline↔spec 그래프가 연결된다.
- [ ] `project`가 아닌 destination으로 분류되면 팬아웃·dedup·map.md 갱신이 일어나지 않는다.
- [ ] 회사 프로젝트 트리에 `origin/`·`baseline/`·`spec/` 3층만 나타나고 area/resource는 나타나지 않는다.
- [ ] 회사 프로젝트 생성·문서화 게이트 표면은 admin 전용이다(staff 접근 불가).

## 7. Open Questions

- 없음 — AXKG-BL-002·AXKG-DEC-007에서 slug 충돌 UX와 docx 처리 방향 OQ가 모두 종료됐다. 프롬프트 문구·DB 스키마·컬럼·라우트/컴포넌트 파일·기능 dedup 매칭 임계값 등 구현 세부는 후속 work·코드 소관이다.
