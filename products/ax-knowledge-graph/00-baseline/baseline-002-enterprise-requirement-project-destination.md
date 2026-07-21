---
type: baseline
id: AXKG-BL-002
title: "기업 AX 전환 요구사항: PARA project destination 팬아웃과 공통기능 정규화"
status: accepted
product: ax-knowledge-graph
source:
  type: idea
  ref: ""
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
    - "[[decision-007-enterprise-project-destination-fanout|AXKG-DEC-007]]"
  specs:
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-010-document-template-management|AXKG-SPEC-010]]"
    - "[[spec-014-enterprise-project-fanout|AXKG-SPEC-014]]"
  works: []
  releases: []
  related: []
created_at: 2026-07-20
updated_at: 2026-07-21
tags:
  - product/ax-knowledge-graph
  - doc/baseline
  - status/accepted
---

# 기업 AX 전환 요구사항: PARA project destination 팬아웃과 공통기능 정규화

ax-graph의 PARA `project` destination을 강화한다. 회사·부서의 AX 전환 요구사항 docx가 inbox로 들어오면 `project`로 분류되어, **회사별 프로젝트 폴더(동적 생성)** 안의 `origin/`(첨부 원본)·`baseline/`(원본요약)·`spec/`(기능정의서)로 팬아웃되고, 같은 기능이 다른 docx로 다시 들어오면 신규 문서 대신 **기존 spec 하나로 통합·보강(기능 dedup, 부서 무관)** 되어 재사용 가능한 project로 완성된다. (확정 외부 계약 SSOT: AXKG-SPEC-014 / 결정: AXKG-DEC-007)

> 이 baseline은 후속 decision/spec/코드수정의 근거가 되는 **설계도 수준**의 입력이다. "무엇을·왜"까지 정의하고, 실제 프롬프트 문구·DB 스키마·API 계약·구현 파일 경로 확정은 후속 문서로 미룬다.

> ⚠️ **용어 주의(중요)**: 이 문서가 설계하는 **회사 프로젝트 폴더 안의 `baseline/`**(앱 런타임 산출물 = 넘어온 docx를 md로 요약·정리한 "원본")은, 이 문서 자신(`AXKG-BL-002`, 제품 설계용 baseline 타입 메타문서)과 **이름만 같고 전혀 다른 개념**이다. 아래에서 전자를 가리킬 때는 항상 `projects/{corp}/baseline/`(런타임 원본요약)으로, 후자는 "이 baseline 문서/AXKG-BL-002"로 구분해 쓴다.

## Context

### 배경 / 문제 정의

현재 PARA `project` destination은 약하다. 분류되면 `projects/{파일명}.md` **flat 한 장(baseline 타입 문서)** 만 생성한다.

- 근거(현재 한계, 코드 위치 참조 — 이 baseline은 경로를 확정하지 않고 as-is를 짚기 위해서만 인용한다): 문서화 게이트(AXKG-SPEC-004)의 project 산출물은 `create_project_baseline` 한 종으로 `projects/`에 단일 md를 만든다. destination→디렉토리 매핑(`services/document_paths.py` 계열, 코드레포 소관)과 project→`project_baseline` 템플릿 바인딩(AXKG-SPEC-010 MVP scope), project 초안 프롬프트/템플릿 시드(코드레포 `apps/api/axkg/seeds.py` 계열)가 모두 "flat 한 장"을 전제한다.
- 이 구조에는 **회사·기능 구분이 없다.** 한 회사가 요구한 여러 기능, 부서별로 따로 들어온 요구, 서로 다른 부서·회사가 반복 요구하는 공통기능을 한 장 안에서 정리·정규화할 수 없다.

기업들은 AX 전환 요구사항을 **docx** 로 준다. 특성상:

- 한 회사가 **기능 여러 개**를 한 번에 요구한다.
- **부서별로 요구가 따로** 들어온다(같은 회사, 다른 시점·다른 부서).
- **같은 회사 안에서 여러 부서가 같은 공통기능**(예: 부서 공유 캘린더-업무일지)을 반복해서 요구한다.

flat 한 장(baseline 타입 문서) 구조로는 이 세 가지를 담지 못한다. 회사라는 컨테이너, 기능이라는 단위, 그리고 **같은 회사 안** 반복 요구를 하나로 합치는 정규화가 모두 필요하다.

> **정규화 범위(확정)**: dedup/정규화는 **같은 `{corp}` 안에서만**(기능 dedup, 부서 무관) 일어난다. 회사가 다르면 같은 기능이라도 **별개 spec**이며, 회사 밖 전역 capability 레지스터(`capabilities/` 같은 공통 카탈로그)는 두지 않는다(아래 Resolved Decisions #1).

## Why It Matters

- **재사용(회사 내부)**: 같은 회사 안에서 공통기능을 한 번만 정의하면, 같은 기능이 다른 docx로 다시 들어올 때 새로 만들지 않고 기존 기능정의서 하나로 통합·보강해 재사용할 수 있다(부서 귀속·요청 이력 없음). 회사 프로젝트가 요구를 받을수록 그 회사의 기능 카탈로그가 자란다(재사용은 `{corp}` 경계 안에서만).
- **정리**: docx라는 비구조 입력을 회사 → baseline(원본) → spec(기능 단위)의 위계로 팬아웃해, "이 회사가 실제로 뭘 요구했나"와 "그게 어떤 기능들로 쪼개지나"를 분리해 추적한다.
- **ax-graph 자산 활용**: ax-graph가 이미 가진 index/stem resolution, `supplement_existing_concept`(개념 성장), 4층 위계, retriever 컨텍스트를 그대로 차용해 새 기계 없이 요구사항 정규화를 얹는다.

## Possible Direction

### 목표 구조 (동적 생성)

앱에서 "프로젝트 추가"를 할 때 **사용자가 회사명을 입력**하면(예: "더에스씨") 시스템이 slug로 정규화해(`the-sc` = `{corp}`) 회사 스캐폴드를 **동적으로** 깐다. 회사 경계는 자동 추론이 아니라 사람이 명시적으로 통제한다(Resolved Decisions #4).

```text
projects/
  {corp}/                    ← 회사(프로젝트). "추가" 시 사용자 입력 회사명 → slug로 동적 생성
    origin/
      {첨부}.docx            ← 손대지 않은 첨부 원본(raw). 요약 md와 별도 보관
    baseline/
      map.md                 ← baseline 인덱스(MOC). 문서 apply 시 파이프라인이 자동 재생성
      {원본요약}.md            ← 넘어온 docx를 md로 요약·정리한 "원본요약"(source of truth)
    spec/
      map.md                 ← spec 인덱스(MOC). 문서 apply 시 파이프라인이 자동 재생성
      {기능}.md               ← baseline에서 추출한 기능정의서 (요구 1항목 = 1장)
```

- **`projects/{corp}/origin/`** = 첨부 docx **원본 파일**을 손대지 않은 raw로 보관. 원본요약(baseline)은 요약①이 가공한 md라 원문 그대로가 아니므로, 감사·역참조용 원본을 별도로 남긴다.
- **`projects/{corp}/baseline/`** = docx 원본 → md 요약·정리(원본요약). 회사가 실제로 뭘 요구했는지 담는 **원본요약(SoT)**. (다시 강조: 여기서의 `baseline/`은 런타임 산출물이며, 이 문서 AXKG-BL-002 같은 제품 설계 baseline과 다른 개념이다.)
- **`projects/{corp}/spec/`** = 그 원본요약에서 **기능 단위를 추출**한 기능정의서. 요구 1항목 = 1장.
- **`map.md`** = 각 폴더의 목차/지도(MOC). **문서가 apply되는 시점에 파이프라인이 자동으로 재생성**한다(문서 목록 반영). 수동 갱신이 아니다(Resolved Decisions #2).
- **project 층위는 `origin/` + `baseline/` + `spec/` 3층만** 둔다. area(종합 판단)·resource(참고 자료) 성격 자료는 회사 프로젝트 안에 분리 저장하지 않고 **기존 전역 PARA 흐름 그대로**(area→`permanent/`, resource→`resources/`, AXKG-SPEC-004 §4 4층 아키텍처) 둔다(Resolved Decisions #3).

### 파이프라인 (기존 PARA 흐름 위에 얹음)

```text
docx 업로드(inbox) → origin 원본 보관 → 요약 → PARA 분류(project) → baseline/{원본요약}.md
                                                          → (분석/추출) → spec/{기능}.md (여러 장)
                                                              └ 같은 회사 내 같은 기능이면 신규 X,
                                                                기존 spec 하나로 통합·보강(dedup, 부서 무관)
```

- 기존 자산: `upload` 채널 + 요약→분류 흐름은 이미 있다(AXKG-SPEC-003 source inbox, AXKG-SPEC-001 curation pipeline, 실행 계약 AXKG-SPEC-011). 요약→PARA 분류→문서화 게이트(AXKG-SPEC-004)의 골격을 재사용한다.
- 새로 필요한 것 (방향만; 계약·구현은 후속):
  1. **docx 텍스트 추출** — 기존 md 위주 인테이크에 **docx 텍스트 추출 경로**를 추가한다(기존 source 수집 어댑터에 docx 추가). 어댑터는 docx **본문 텍스트만** 추출하고, 기능별 구조화(기능 1·2·3… 줄글)는 어댑터가 아니라 기존 **요약① 스테이지**가 담당한다 — 요약①은 원문 구조를 따르는 적응형 요약이라 docx의 기능 목록 구조를 그대로 따라 기능별 줄글을 산출하고, 그 산출물이 `projects/{corp}/baseline/` 원본요약이 된다(Resolved Decisions #5, 요약① 적응형 출력 규약 AXKG-SPEC-011 §4 / AXKG-DEC-005 A와 정합). 요구 docx는 줄글+목록 중심이라 표는 텍스트로 딸려 나와도 요약①이 정리하며, 표 보존·이미지 대체텍스트 같은 파싱 계약은 두지 않는다.
  2. **project destination 팬아웃** — 분류 시 flat 한 장 대신 `projects/{corp}/`의 `origin/`(원본 보관) + `baseline/`(원본요약, main) + `spec/`(기능정의서, derived) 다중 문서 구조로 팬아웃. 문서화 게이트는 기존 파생지식 모델(`main_document` + `derived_suggestions[]`)을 재사용한다(AXKG-SPEC-014). `{corp}`는 "프로젝트 추가" 시 사용자 입력 회사명을 slugify해 정한다.
  3. **공통기능 dedup(회사 내부, 부서 무관)** — **같은 `{corp}` 안에서** 같은 기능이 다른 docx로 다시 오면 신규 spec 생성이 아니라 기존 기능정의서 하나로 통합·보강(`supplement_existing_feature`). 기능은 프로젝트의 기능 카탈로그이며 요청부서·요청 이력을 붙이지 않는다. 회사가 다르면 별개 spec이다.
  4. **map.md 자동 갱신** — 문서 apply 시점에 해당 폴더 `map.md`(MOC)를 자동 재생성.

### 차용하는 ax-graph 개념 (재사용)

이 설계는 새 기계를 발명하지 않고 ax-graph의 기존 개념을 project destination에 재적용한다.

| ax-graph 개념 | 원래 용도 | 이 설계에서의 재사용 |
|---|---|---|
| **index / stem resolution** | wikilink/문서 매칭(AXKG-DEC-005 연결 후보 컨텍스트, documents index 스냅샷) | 새 요구가 **같은 회사(`{corp}`) 안** 기존 기능 spec과 같은지 매칭(중복 판정) |
| **`supplement_existing_concept`** (→ project는 `supplement_existing_feature`) | 같은 개념에 두 번째 출처가 오면 신규 생성 대신 기존 concept 보충(AXKG-SPEC-004 §4 개념 성장) | **같은 회사 안에서** 같은 기능이면 새 spec 안 만들고 기존 기능정의서 하나로 통합·보강(dedup, 부서 무관) |
| **4층 위계** | 출처 기록 → 원자 개념 → 종합 노트 → 실행 문서(AXKG-DEC-005 A) | `origin/`(raw 보관, 위계 밖) + `baseline/`(원본요약) → `spec/`(추출된 기능정의서)의 지식 2층 위계로 축약 적용 |
| **retriever 컨텍스트** | 초안 AI에 관련 기존 문서 top-N 주입(AXKG-DEC-005 2단 하이브리드) | 새 요구 정규화 시 **같은 회사 폴더 안** 유사 기능을 자동 탐색해 중복/통합 후보 제안 |

> **범위 한정**: 위 매칭·정규화·retriever 탐색은 모두 **`{corp}` 경계 안으로 한정**한다. 회사를 넘는 spec 재사용·통합은 하지 않는다(Resolved Decisions #1).

> 위계 대응 주의: ax-graph의 4층에서 `project → baseline(projects/)`는 "실행 문서" 층이다. 이 설계는 그 project **안에서** 다시 `baseline/`(원본요약)과 `spec/`(기능정의서) 지식 2층을 여는 것이므로(폴더는 raw 보관용 `origin/`을 더해 3층이되, 지식 위계는 baseline→spec 2층), ax-graph 전역 4층과 회사 프로젝트 내부 위계는 층위가 다르다. 회사 프로젝트 내부의 `baseline/`은 "이 회사가 뭘 요구했나"(출처 기록 성격), `spec/`은 "그 요구를 기능 단위로 추출한 것"이다.

### Worked example — The_sc (회사, 기능 10개)

아래 docx가 inbox에 올라오면 `project`로 분류되어 `projects/the-sc/`로 팬아웃된다. 원본요약 1장(`baseline/`)과 기능 spec 10장(`spec/`, 요구 1항목 = 1장)이 산출된다.

```text
projects/
  the-sc/
    origin/
      the-sc-ax-requirements.docx    ← 첨부 원본(raw, 손대지 않음)
    baseline/
      map.md
      the-sc-ax-requirements.md      ← docx 원본요약(회사가 요구한 10개 기능 전부의 원본 맥락)
    spec/
      map.md
      hospital-revenue-analysis.md   ← 1
      memo-meeting-search.md         ← 2  (공통: ax-graph graph-chat/Graph RAG)
      staff-mission-scheduling.md    ← 3
      proposal-writing-assistant.md  ← 4  (공통: ax-graph 문서화 게이트)
      shared-calendar-worklog.md     ← 5  (같은 기능이 여러 docx로 반복 유입되는 대표 기능)
      procedure-knowledge-qa.md      ← 6
      medical-news-digest.md         ← 7  (공통: ax-graph curation 파이프라인)
      sms-dispatch.md                ← 8
      marketing-rank-monitor.md      ← 9
      review-blog-draft-audit.md     ← 10
```

10개 기능(요구 1항목 = spec 1장):

1. **병원 매출 동향 자동 분석** — 지역/진료과목별 매출 트렌드 자동 요약.
2. **메모 & 회의록 자동 찾아주기** — 자유 기록에서 질의로 정확히 검색. (→ ax-graph graph-chat / Graph RAG와 **공통**, AXKG-SPEC-006)
3. **직원 게릴라 미션 및 일정 관리** — 지시사항 → 직원 일정 등록 + 알림.
4. **대화형 제안서 작성 도우미** — 회의록 → AI 인터뷰 → 제안서 생성. (→ ax-graph 문서화 게이트와 **공통**, AXKG-SPEC-004)
5. **부서 공유 캘린더 및 업무일지** — 개인 업무일지 + 부서 달력 + 진행상황판. (→ **같은 기능이 여러 docx로 반복 유입될 대표 기능** — dedup 예시)
6. **신입사원용 피부/성형 시술 지식인** — 시술 지식 검색/대화.
7. **매일 보는 의료 뉴스 모음** — 의료 뉴스 자동 수집·요약 매거진. (→ ax-graph curation 파이프라인과 **공통**, AXKG-SPEC-001)
8. **프로그램 내 문자 발송** — 문자 양식 저장 + 외부 발송 서비스 연동.
9. **마케팅 순위 자동 확인** — 네이버 플레이스/블로그/체험단 순위 매일 자동 체크·리포트.
10. **체험단 블로그 원고 자동 검수** — 가이드라인 준수 + 의료법 위험문구 감지 + 사진 확인.

#### 이 예시가 보여주는 두 가지 — 구현 재활용(A)과 정규화(B)

**(A) ax-graph 플랫폼 역량과 겹치는 기능 — 구현 관점의 관찰 노트(정규화 대상 아님)** — 2·4·7은 ax-graph가 이미 가진 플랫폼 역량과 본질적으로 같은 기능이다:

- 2(메모/회의록 검색) ≈ ax-graph graph-chat / Graph RAG(AXKG-SPEC-006).
- 4(대화형 제안서 작성) ≈ ax-graph 문서화 승인 게이트(AXKG-SPEC-004)의 초안 생성 흐름.
- 7(의료 뉴스 자동 수집·요약) ≈ ax-graph curation 파이프라인(AXKG-SPEC-001, source inbox AXKG-SPEC-003).

→ 이 겹침은 **정규화(dedup) 대상이 아니라 구현 관점의 관찰 노트**다. 회사 spec을 실제로 **구현할 때 그 플랫폼 역량(graph-chat / 문서화 게이트 / curation)을 재활용**할 수 있다는 취지일 뿐이다. 이 spec들은 The_sc의 요구이므로 그대로 `projects/the-sc/spec/`에 **각각 별개 spec**으로 남는다 — 전역 공통기능으로 승격하거나 회사를 가로지르는 공통 카탈로그로 묶지 않는다(Resolved Decisions #1).

**(B) 같은 기능이 다른 docx로 반복 유입 — 실제 정규화(기능 dedup, 부서 무관)** — dedup(신규 생성 대신 기존 기능정의서 하나로 통합·보강) 메커니즘은 **같은 회사 안에서만** 적용된다. 5(부서 공유 캘린더-업무일지)는 The_sc 안에서 **여러 docx로 반복 유입**될 대표 기능이다:

- 첫 요구 docx가 들어와 `projects/the-sc/spec/shared-calendar-worklog.md`가 생성된다.
- 이후 같은 회사의 **다른 docx**에 같은 "부서 공유 캘린더/업무일지" 요구가 담겨 들어오면, retriever가 같은 `{corp}` 폴더 안 기존 `shared-calendar-worklog.md`를 같은 기능으로 탐지 → **신규 spec을 만들지 않고** `supplement_existing_feature` 방식으로 기존 기능정의서를 **통합·보강**한다(새 docx가 상세요구·유저플로우 디테일을 더하면 반영). **요청부서·요청 이력은 붙이지 않는다** — 기능은 프로젝트의 기능 카탈로그이지 부서 소유가 아니다.
- 결과적으로 하나의 기능정의서가 상세를 축적하며 성장한다(중복 문서가 갈라지지 않음).

즉 (A)는 **정규화가 아니라 구현 시 재활용 힌트**이고, (B)만이 **실제 정규화(같은 회사 안 같은 기능 dedup·보강, 부서 무관)**다. 만약 다른 회사가 똑같이 "부서 공유 캘린더"를 요구해도 그 회사의 `projects/{다른-corp}/spec/`에 별개 spec으로 생성되며, The_sc의 것과 합쳐지지 않는다.

### 반드시 담을 설계 요약 표

| 요소 | 내용 |
|---|---|
| 입력 | 회사/부서 요구사항 docx → ax-graph inbox 업로드 |
| 프로젝트 생성 | "추가" 시 사용자 입력 회사명 → slugify(`{corp}`) → `projects/{corp}/{origin,baseline,spec}/` + `map.md` 동적 스캐폴드 |
| origin/ | 첨부 docx 원본(raw, 손대지 않음). 요약 md와 별도 보관 |
| baseline/ | docx를 요약·정리한 원본요약(md, main). 회사가 뭘 요구했는지의 SoT |
| spec/ | baseline에서 추출한 기능정의서(derived). 요구 1항목 = 1장 |
| map.md | 문서 apply 시 파이프라인이 자동 재생성(MOC) |
| project 층위 | `origin/` + `baseline/` + `spec/` 3층만. area/resource는 전역 PARA 흐름 그대로(분리 저장 안 함) |
| PARA project | 분류 시 flat 한 장 → `{corp}` 3층 구조로 팬아웃(main+derived, AXKG-SPEC-014) |
| 공통기능 dedup | **같은 회사 안** 같은 기능 반복 유입 → 신규 X, 기존 기능정의서 하나로 통합·보강(`supplement_existing_feature`, 부서 무관). 회사 넘는 정규화 없음 |
| worked example | The_sc, 기능 10개 |

### Scope

**In** — 위 구조·파이프라인·정규화 방향을 **설계도 수준**으로 정의(무엇을/왜). 후속 decision/spec/코드수정의 근거가 되게 한다.

- 회사별 프로젝트 폴더(`projects/{corp}/`)와 그 안의 `origin/`·`baseline/`·`spec/`·`map.md` 구조(3층 한정).
- docx → origin 보관 → 요약 → project 분류 → 팬아웃(main+derived) 파이프라인의 흐름.
- 회사 내부 공통기능 dedup(같은 기능 통합·보강, 부서 무관)의 방향과 차용할 ax-graph 개념.

**Out** — 아래는 이 baseline에서 확정하지 않는다(→ 후속 decision/spec에서):

- 실제 프롬프트 문구.
- DB 스키마·컬럼.
- API 계약(엔드포인트·payload).
- 구현 파일 경로 확정.
- 단, **현재 한계를 짚기 위해** 관련 코드 위치를 근거로 참조하는 것은 허용한다(위 Context의 as-is 인용).

## Resolved Decisions

이전 초안의 Open Questions 5건은 아래처럼 확정되어 본문에 반영됐다(계약·구현 상세는 후속 decision/spec에서 확정).

1. **공통기능 판정·dedup 범위 = 회사 내부만(부서 무관).** dedup/정규화는 같은 `{corp}` 안에서만 일어나며 같은 기능은 부서와 무관하게 하나의 기능정의서로 통합·보강한다(요청부서·요청 이력 없음 — 기능은 프로젝트의 기능 카탈로그). 회사가 다르면 같은 기능이라도 별개 spec이며, 회사 밖 전역 capability 레지스터(`capabilities/` 같은 공통 카탈로그)는 도입하지 않는다.
2. **map.md 갱신 = 파이프라인 자동.** 문서 apply 시점에 해당 폴더 `map.md`(MOC)를 자동 재생성한다(문서 목록 반영). 수동 갱신 아님.
3. **project 층위 = origin + baseline + spec 3층만.** 회사 프로젝트 안에는 `origin/`(첨부 원본)·`baseline/`(원본요약)·`spec/`(기능정의서)만 둔다. area→`permanent/`, resource→`resources/`는 기존 전역 PARA 흐름 그대로 두고 project 안에 분리 저장하지 않는다.
4. **corp slug = "프로젝트 추가" 시 사용자 입력 → slugify, 충돌 시 사용자 확인.** 사용자가 회사명("더에스씨")을 입력하면 시스템이 slug(`the-sc`)로 정규화한다. slugify 결과가 **기존 `{corp}`와 충돌하면** 사용자에게 **"기존 `{corp}` 프로젝트에 이 docx를 추가할까요?"** 를 확인한다 — **예 = 기존 `{corp}`에 baseline/spec 추가**(같은 회사로 합류), **아니오 = `{corp}-2` 등 suffix로 새 프로젝트 생성**. 회사 경계는 사람이 명시적으로 통제한다.
5. **docx 처리 = 텍스트 추출만.** docx에 필요한 것은 **본문 텍스트 추출뿐**이다(기존 source 수집 어댑터에 docx 경로 추가). 기능별 구조화(기능 1·2·3… 줄글)는 기존 **요약① 스테이지**가 담당한다 — 요약①은 원문 구조를 따르는 적응형 요약이라 docx의 기능 목록 구조를 그대로 따라가 기능별 줄글을 산출하고, 그 산출물이 `projects/{corp}/baseline/` 원본요약이 되어 spec 팬아웃의 입력이 된다(AXKG-SPEC-011 §4 / AXKG-DEC-005 A와 정합). 요구 docx는 줄글+목록 중심이라 표 보존·이미지 대체텍스트·병합셀·중첩표·스캔이미지 같은 파싱 계약은 두지 않는다.
6. **팬아웃 메커니즘·origin·템플릿 확정(AXKG-DEC-007 / 상세 SSOT AXKG-SPEC-014).** ① 승인 게이트 팬아웃은 기존 파생지식 모델(`main_document`=원본요약 + `derived_suggestions[]`=기능별 초안, 신규 `create_feature_spec`/dedup `supplement_existing_feature`)을 재사용해 한 게이트에서 검토·승인→apply한다. ② 첨부 docx 원본은 요약 md와 별도로 `projects/{corp}/origin/`에 raw로 보관(3층). ③ 산출 템플릿은 단일 `project_baseline`이 아니라 `project_source_summary`(원본요약)·`project_feature_spec`(기능정의서) 2종으로 AXKG-SPEC-010에 정식 등록(파일 template directory 미신설·PostgreSQL 동적 관리 원칙 불변).

## Open Questions

현재 미결 없음 — 계약·구현 상세는 후속 spec(20-spec)/work에서 확정한다.
