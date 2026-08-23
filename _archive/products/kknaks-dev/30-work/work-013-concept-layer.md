---
type: work
id: KDEV-WORK-013
title: "concept 층 도입 — 4층 재편 · 검증 재정의 · 규칙/템플릿"
status: done
product: kknaks-dev
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: —
  fe: —
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 100
created_at: 2026-07-27
updated_at: 2026-07-27
tags:
  - product/kknaks-dev
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
  decisions:
    - "[[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]"
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
    - "[[spec-002-graph-schema|KDEV-SPEC-002]]"
    - "[[spec-003-knowledge-workflow|KDEV-SPEC-003]]"
    - "[[spec-004-graph-validation|KDEV-SPEC-004]]"
  works:
    - "[[work-012-slack-bridge-absorb|KDEV-WORK-012]]"
  releases: []
  related: []
---

# concept 층 도입 — 4층 재편 · 검증 재정의 · 규칙/템플릿

`permanent/concept/`를 신설하고 그래프를 4층(`source`/`concept`/`synthesis`/`execution`)으로 재편한다. 층별 orphan 판정과 `up:` 방향 반전을 **report-only로 먼저 측정한 뒤** enforce로 넘긴다.

> 만들지 않는 것: 승인 파이프라인. 이 work가 끝나면 concept 노트를 **손으로라도** 쓸 수 있고, WORK-014/015가 그 위에 자동 유입을 얹는다.

## Meta

- Baseline: KDEV-BL-003
- Covers spec: KDEV-SPEC-001·002·003·004
- Depends on work: 없음
- Parallel work: WORK-012 (bridge 흡수 — 서로 독립)
- Follow-up work: WORK-014
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR | main (미커밋 작업트리) |
| Blocker | 없음 |
| Next | WORK-014 큐 + route 게이트 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 층 정의·enforce 시점 판단 | done |
| Design | — | UI 변경 없음 | — |
| FE | — | 변경 없음 (열람 표면은 후속) | — |
| BE | kknaks | 빌더·검증기·로더 | done |
| QA | kknaks | report-only 측정·회귀 | done |
| Ops | kknaks | enforce 전환·kill-switch | done |

## Scope

포함:

- `permanent/concept/` 디렉토리 신설
- `layer` 축 도입 — `type`에서 도출해 `_graph.json` `nodes[].layer`에 담기
- type enum 재편: `concept` 추가, `note` 제거, `product` 정리
- rank 재정의 + **비교 연산자 반전**
- L2 type별 필수 필드(`concept`=`aliases`+`up`, `permanent`=`up`, `idea`=`up` 금지)
- L5 층별 orphan 판정 + `source` orphan을 **미소화 큐 지표**로 분리
- `rules/knowledge-note-pipeline.md` 신규
- `templates/knowledge/` 4종 (idea·reference·concept·permanent)
- 루트 디렉토리 README 개정 (`inbox/`는 "미정제만 보유")

제외:

- 승인 큐·게이트 (WORK-014·015)
- 트리 문서 렌더러 (후속 — SPEC-005)
- 발행 전 검증 훅 (WORK-015 Executor에서 이 검증기를 호출)
- `reference/` 157개 소급 정제 (범위 밖)
- `reference/` group 13종 정리 (범위 밖)

## Code Surface

- Repo / module: `app/back/core`, `app/back/service`, 레포 루트

| 경로 후보 | 설명 |
|---|---|
| `app/back/core/graph.py` | `ALLOWED_NODE_TYPES`·`KNOWLEDGE_NODE_TYPES`·`_TYPE_RANK` + L2/L4/L5 로직 |
| `app/back/service/persona_loader.py` | `permanent/concept/` 순회, `layer` 주입 |
| `app/back/tests/test_graph.py` · `test_graph_enforcement.py` | 층별 판정·rank 반전 테스트 |
| `app/scripts/install_hooks.sh` | pre-commit 트리거에 `permanent`·`inbox` 추가 (기존 구멍) |
| `agent.md` | **지식 노트 작성 라우팅 신설** — 규칙·템플릿으로 가는 진입 경로 |
| `.agent/skills/capture-knowledge/SKILL.md` | 규칙 문서 참조 추가 (형식 규칙 복사 금지 명시) |
| `app/back/tests/test_knowledge_templates.py` | **신규** — 템플릿↔lint 정합 상시 검증 |
| `permanent/concept/` | 신설 (README 포함) |
| `rules/knowledge-note-pipeline.md` | 신규 — `product-doc-pipeline.md`의 대칭 |
| `templates/knowledge/*.md` | 신규 4종 |
| `inbox/README.md` · `reference/README.md` · `permanent/README.md` | 개정 |

- Domain / schema note: **DB 변경 없음.** 파일·빌더·검증기만 다룬다.

## Domain / Schema

해당 없음 (파일 SoT).

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-015 | `validate_graph` | Apply Executor가 발행 전 검증에서 이 함수를 호출한다 |
| 후속 열람 표면 | `_graph.json` `nodes[].layer` | 층 필터가 이 필드를 소비한다 |

## Internal Interface Contract

`_graph.json` `nodes[]`에 `layer` 필드가 추가된다. 값은 `source` · `concept` · `synthesis` · `execution` · `null`(층 없음).

`validate_graph`의 반환에 **미소화 큐 집계**가 더해진다 — `source` orphan은 위반 목록에 넣지 않고 별도로 낸다. 기존 호출부(`_enforce_graph`)가 위반 목록만 보고 차단하므로, 이 분리로 부팅이 막히지 않는다.

## Execution

### Phase 1 — report-only 측정

- **Status**: DONE
- **설명**: 새 규칙을 **차단 없이** 넣고 기존 406노드가 얼마나 위반하는지 잰다. WORK-001~007에서 검증된 순서(report-only → 데이터 정리 → enforce)를 그대로 따른다.
- **작업**:
  - [x] `layer` 도출 매핑 추가 (`type` → `layer`)
  - [x] rank 테이블을 층 순서로 교체하고 **비교 연산자를 `<=`로 반전**
  - [x] L2 type별 필수 필드 규칙 추가
  - [x] L5를 층별 판정으로 교체 + `source` orphan 별도 집계
  - [x] 새 규칙 위반을 **WARN/리포트로만** 내보내도록 임시 처리
- **검증**:
  - [x] 기존 406노드에 대한 신규 위반 수를 측정해 기록 (L2 필수 필드 / L4 반전 각각)
  - [x] L5 WARN이 156건 → 0건이 되고 미소화 큐 지표에 156이 잡힌다
  - [x] 부팅이 막히지 않는다 (`_enforce_graph`가 신규 위반으로 raise하지 않음)
  - [x] 기존 테스트 전부 통과
- **완료 증거**:
  - `core/graph.py` — `_TYPE_LAYER`(type→layer) · `layer_of()` · `_LAYER_RANK`(source 1 → concept 2 → synthesis 3 → execution 4) · `_REQUIRED_FIELDS` · `layer_rules_enforced()` 게이트 추가. 신규 규칙 산출은 detail 을 `[layer]` 로 시작해 식별 가능하게 했다.
  - **기준선(변경 전) 실측**: nodes 419 / edges 506 · ERROR **0** · L5 WARN **157** · lineage **1** · type 분포 reference 157 / 제품문서 261 / permanent 1.
  - **신규 규칙 위반 실측: 단 1건**(예상보다 훨씬 적음). `permanent/ax-needs-information-coherence.md` 의 `up: [baseline-001-repo-knowledge-graph]` — synthesis(3) → execution(4) 로 **하류를 up**. 종전 모델에선 permanent·baseline 이 둘 다 rank 4 라 통과하던 것이 rank 반전으로 드러났다.
  - **L5 성격 전환 확인**: WARN 157 → **INFO 157**(미소화 큐). WARN 총계가 157 → 1(신규 L4)로 떨어졌다.
  - **부팅 비차단 확인**: ERROR 0 유지 — `_enforce_graph` 가 ERROR 만 보므로 신규 규칙이 부팅을 막지 않는다.
  - Phase 2 에 "확인 필요"로 적었던 항목이 실측으로 해소 — **`note`·`product`·`project` 실사용 0건**.
  - **rank 반전 함정 검증**: `concept → reference` 통과 / `reference → concept` 차단을 테스트로 고정(`TestLayerDirection`).
  - **구현 중 결함 1건 발견·수정** — 기존 테스트 `test_l4_downstream_up_forbidden`(spec→note)이 실패하면서, **층이 없는 타입이 `up:` 타겟일 때 검사가 통째로 빠지는 것**이 드러났다. `idea` 도 층이 없으므로 "idea 는 상류가 될 수 없다"(KDEV-DEC-010 D3)를 아무도 안 지키게 된다. `elif src_layer and tgt_layer is None` 분기를 추가하고 `test_layerless_node_cannot_be_upstream` 으로 고정했다.

> **rank 반전 주의**: 테이블만 교체하고 비교를 그대로 두면 L4가 조용히 반대로 동작한다. 현행은 `reference=4` + `up 타겟 rank >= 자기 rank`, 신규는 `reference=1` + `<=`다. Phase 1에서 `concept → reference`가 통과하고 `reference → concept`가 걸리는지 반드시 확인한다.

### Phase 2 — 데이터 정리

- **Status**: DONE
- **설명**: Phase 1이 찾아낸 위반을 해소한다. 위반 수에 따라 범위가 정해지므로 Phase 1 결과를 보고 시작한다.
- **작업**:
  - [x] `note` 타입 잔존 데이터 확인 및 제거 (실사용 0건 예상 — 확인 필요)
  - [x] `permanent` 1건의 `up:` 필수 충족 여부 확인·보정
  - [x] 기존 lineage 1건이 새 방향 규칙을 통과하는지 확인·보정
  - [x] `product` 타입 정리 (showcase는 이미 빌더에서 제외됨 — enum만 정리)
- **검증**:
  - [x] 신규 규칙 위반이 0이 된다
  - [x] 기존 노드 수·엣지 수가 의도치 않게 변하지 않는다
- **완료 증거**:
  - Phase 1 이 찾은 위반 1건이 전부였고, `note`·`product`·`project` 잔존 데이터는 0건이라 정리할 것이 없었다.
  - 그 1건은 **데이터 문제였다** — 본문을 보면 `[[baseline-001-repo-knowledge-graph]]` 는 "## 내가 만든 것과의 대조" 섹션의 **비교 대상**이지 기반이 아니다. `up:` 은 "이것을 기반으로 한다"는 계보이므로 규칙이 맞고 데이터가 틀렸다.
  - 다만 이 노트는 **4층 이전 유물**이었다 — 실제 기반인 유튜브 영상이 `source:` frontmatter 에 URL 로만 있고 reference 노트도 concept 도 없었다. 그래서 Phase 3 와 합쳐 4층으로 정제했다(아래).
  - 결과: `up:` 을 concept 2건으로 교체하고 `[[baseline-...]]` 은 본문 assoc 으로 남겼다. **신규 규칙 위반 0건.**

### Phase 3 — concept 층 실재화

- **Status**: DONE
- **설명**: 디렉토리와 로더 배선. WORK-010의 permanent 배선을 미러한다.
- **작업**:
  - [x] `permanent/concept/` 디렉토리 + README 생성
  - [x] `persona_loader`가 `permanent/concept/`를 순회하고 `type: concept`를 주입
  - [x] `_build_graph_nodes`에 concept 포함
  - [x] `_graph.json` `nodes[]`에 `layer` 필드 추가
  - [x] 샘플 concept 1건을 손으로 작성해 계보 발현 확인
- **검증**:
  - [x] concept 노트가 노드로 잡히고 `layer: concept`이 나온다
  - [x] `concept → reference` `up:`이 lineage 엣지로 발현된다 (**lineage 엣지가 1건에서 늘어나는 첫 지점**)
  - [x] `aliases`로 링크한 `[[음성인식]]`이 canonical stem으로 resolve된다
  - [x] 빈 `permanent/concept/`에서도 부팅에 영향이 없다
- **완료 증거**:
  - `permanent/concept/` 디렉토리 + README 생성(flat, `aliases`/`up` 필수 규약 명시).
  - `service/persona_loader.py` — `_load_permanent_notes` 가 `permanent/` · `permanent/concept/` · `permanent/archive/` 3곳을 순회. `_enrich_permanent` 가 경로에 `concept` 가 있으면 기본 type 을 `concept` 로 준다(**디렉토리가 층을 1차 결정**한다는 KDEV-SPEC-001 §5 원칙의 로더 구현). `REQUIRED_FIELDS["concept"]` 추가, `validate_persona` 가 노드 type 으로 카테고리를 고르도록 수정.
  - `_graph.json` `nodes[].layer` 추가(빌더 계산, frontmatter 미기재).
  - **실제 4층 체인을 손으로 구축** — Phase 2 의 위반 1건을 고치면서 Phase 3 의 "샘플 concept 작성"을 함께 수행했다.
    - `reference/ai_skills/2026-07-28-llm-wiki-graphify-integration.md` — 노트에 URL 이 있어 `yt-dlp` + `youtube-transcript-api` 로 **실제 자막(2,480자)을 받아 근거 있게** 작성했다. 홍보 영상이라는 점과 71.5배 토큰 절감 수치가 자사 사례라는 점을 「한계와 검증이 필요한 부분」에 명시.
    - `permanent/concept/structure-content-separation.md` — 구조와 내용의 분리
    - `permanent/concept/deterministic-skeleton-first.md` — 결정론적 뼈대 우선(투패스)
    - `permanent/ax-needs-information-coherence.md` 의 `up:` 을 이 두 concept 로 교체(본문 `[[]]` 동반 — L3 오버레이).
  - **lineage 1건 → 4건.** 4층 체인이 실제로 발현됐다:
    ```
    2026-07-28-llm-wiki-graphify-integration (source)
            ↑ up                        ↑ up
    structure-content-separation   deterministic-skeleton-first  (concept)
            ↑ up                        ↑ up
            ax-needs-information-coherence (synthesis)
    ```
  - 최종: nodes 422 / edges 512 · layer 분포 execution 261 / source 158 / concept 2 / synthesis 1 · **신규 규칙 위반 0** · 미소화 큐 157(새 reference 는 concept 에 인용돼 큐에서 빠짐).

### Phase 4 — 규칙·템플릿 문서

- **Status**: DONE
- **설명**: 사람과 AI가 따를 작성 규칙을 파일로 만든다. AI가 concept 초안을 생성하려면 따를 형식이 파일로 있어야 한다.
- **작업**:
  - [x] `rules/knowledge-note-pipeline.md` 작성 — 4층 모델·SoT 위임·개념 성장·경로/frontmatter·`up:`/`[[]]` 규칙
  - [x] `templates/knowledge/` 4종 작성 (idea·reference·concept·permanent)
  - [x] `inbox/README.md`의 "미분류만 보유" → **"미정제만 보유"** 개정
  - [x] `reference/README.md`·`permanent/README.md`에 층·SoT 위임 반영
  - [x] 각 README가 SPEC이 아니라 `rules/knowledge-note-pipeline.md`를 가리키도록 정리
  - [x] **템플릿을 형식의 SoT로 둔다** — 사람도 AI 도 같은 파일을 본다. 경로를 고정하고 `agent.md` 에서 라우팅한다(프롬프트 주입 아님)
- **검증**:
  - [x] 템플릿으로 만든 concept가 검증을 통과한다 (**템플릿과 lint가 어긋나지 않음을 실제로 확인**)
  - [x] 템플릿으로 만든 reference·permanent도 검증을 통과한다
  - [x] 규칙 문서와 SPEC-001/002/004 사이에 중복 서술이 없다 (규칙=쓸 때 / SPEC=검증 계약)
- **완료 증거**:
  - `rules/knowledge-note-pipeline.md` 신규 — `product-doc-pipeline.md` 의 대칭. 4층 모델 · SoT 위임 · 개념 성장 · `up:` 방향 · 오버레이 · 층별 필수 필드 · 검증 규칙 요약 · 자동 유입과의 관계. 규칙(쓸 때)과 spec(검증 계약)의 경계를 첫머리에 명시해 중복 서술을 피했다.
  - `templates/knowledge/` 5개 — `README.md` + `idea`/`reference`/`concept`/`permanent`. 각 템플릿 하단 주석에 **틀리기 쉬운 지점**을 박았다(concept 성장 절차 3단계 / reference 는 `up:` 없음 / permanent 는 제품문서를 up 하지 않음 / idea 는 up 금지).
  - **템플릿↔lint 정합 실증** — 4종의 `<...>` 자리를 채워 실제 `validate_graph` 에 태운 결과 **ERROR/WARN 0**. 템플릿대로 쓰면 검증을 통과한다는 것이 확인됐다(템플릿이 AI 초안 생성의 입력이므로 이 정합이 깨지면 AI 산출물도 전부 거부된다).
  - 루트 README 3종 개정 — `inbox`(**"미분류만 보유" → "미정제만 보유"**, 대기열이 아니라 보류함), `reference`(층 `source` 명시 · SoT 위임 · `up:` 없음 · 미소화 큐는 위반 아님), `permanent`(층 `synthesis` · `up:` 대상은 concept · 제품문서 up 금지). 셋 다 `rules/knowledge-note-pipeline.md` 를 가리키게 했다.

##### 구조 정정 — 규칙은 프롬프트가 아니라 레포에 있다 (owner 지적)

처음에는 템플릿을 **"AI 스테이지가 프롬프트에 주입하는 생성 계약"** 으로 규정하고 그렇게 문서·work 에 써 두었다. **틀렸다.** 이 레포는 에이전트가 진입점에서 **찾아가는** 구조다 — worker 가 repo 를 마운트하고(`.:/repo:ro`) 캡처 호출의 cwd 가 레포 루트라, 에이전트는 `CLAUDE.md → agent.md → rules → templates` 를 스스로 읽을 수 있다. 프롬프트에 복사해 넣으면 **SoT 가 둘이 되고** 규칙이 바뀔 때 한쪽만 고쳐져 조용히 어긋난다.

더 큰 문제는 **만들어놓고 라우팅을 안 건 것**이었다. `agent.md` 가 `rules/` 를 언급하는 곳은 hook 섹션의 `product-doc-pipeline.md` 한 군데뿐이라, 새로 만든 `rules/knowledge-note-pipeline.md` 로 가는 길이 **어디에도 없었다.** 에이전트가 지식 노트를 쓰려 해도 규칙을 찾을 수 없는 상태였다.

- `agent.md` 에 **「지식 노트를 쓸 때」 섹션 신설** — 규칙 → 템플릿 진입 경로와 층별 템플릿·경로 표. "형식을 프롬프트에 복사하지 않는다"를 명시.
- `.agent/skills/capture-knowledge/SKILL.md` 에 **「Repo rules are the SoT」 추가** — skill 은 JSON 계약만 소유하고 4층·SoT 위임·`up:` 규율은 `rules/` 를 읽게 했다. Workflow 0번에 "규칙·템플릿을 먼저 읽는다"를 넣고, Hard Constraints 에 **"형식 규칙을 이 파일에 복사해 두지 않는다"** 를 박았다. `concept` 도 이 skill 의 산출 대상이 아님을 명시(승격은 게이트 소관).
- `rules/`·`templates/README`·WORK-013/015 의 "프롬프트 주입" 서술을 전부 정정.
- WORK-015 작업 항목도 **"프롬프트는 무엇을 만들라만 지시, 형식은 레포에서 읽는다"** 로 교체하되, **"작성 전 규칙을 읽으라"는 지시는 프롬프트에 반드시 넣는다**는 단서를 남겼다 — 찾아가지 않으면 형식이 표류하기 때문이다.

##### 템플릿 보강 + 상시 검증

초안 템플릿이 플레이스홀더 나열 수준이라 빈약했다(owner 지적). 이제 템플릿이 **형식의 유일한 SoT** 이므로 분량이 곧 계약의 밀도다.

- 4종을 40줄 내외 → **48~73줄**로 보강. 각 섹션에 "무엇을 넣고 무엇을 넣지 않는지"를 적고, 하단 주석에 경로·검증 규칙·틀리기 쉬운 지점(개념 성장 4단계 절차, reference 는 `up:` 없음, permanent 는 제품문서 up 금지, idea 는 up 금지)을 박았다.
- `reference.md` 는 **현행 캡처 렌더러(`render.py`)의 검증된 섹션 구조**(개요/출처와 맥락/핵심 주장/주요 개념/근거와 사례/적용 가능성/한계/참고)에 맞추되, 「주요 개념」을 **SoT 위임**(이름+한 줄만, 상세는 concept)으로 바꿨다.
- **신규 테스트 `tests/test_knowledge_templates.py` 11건** — ① frontmatter 파싱(플레이스홀더에 콜론 하나만 들어가도 YAML 이 깨진다 — **실제로 `idea.md` 에서 한 번 깨졌고 이 테스트가 잡았다**) ② 채워 넣은 템플릿이 L1~L6 를 ERROR·WARN 0 으로 통과 ③ 4층 계보가 실제로 발현(concept→reference, permanent→concept) + layer 도출 확인.
  이로써 템플릿↔lint 정합이 일회성 확인이 아니라 **상시 보장**된다.

> 템플릿은 사람용 참고자료가 아니라 **형식의 SoT**다. AI 에이전트는 레포를 읽을 수 있는 상태로 실행되므로(worker repo 마운트 + cwd=레포 루트) 프롬프트에 복사해 넣지 않고 `CLAUDE.md → agent.md → rules → templates` 경로로 **찾아와서** 읽는다. 따라서 템플릿이 검증을 통과하지 못하면 AI 산출물도 통과하지 못한다 — 위 검증 항목이 그 정합을 보장한다.

### Phase 5 — enforce 전환

- **Status**: DONE
- **설명**: 데이터가 green이 된 뒤에 차단을 켠다. 순서를 지키지 않으면 라이브 서버가 부팅에 실패한다.
- **작업**:
  - [x] 신규 L2/L4 위반을 ERROR로 승격
  - [x] `GRAPH_ENFORCE` kill-switch가 신규 규칙에도 적용되는지 확인
  - [x] **pre-commit 훅 트리거 경로 구멍 수정** — `app/scripts/install_hooks.sh:34`의 `^(persona|reference|products)/`에 `permanent`·`inbox` 추가
- **검증**:
  - [x] enforce ON 상태에서 실데이터 부팅 성공
  - [x] `up:` 없는 concept를 주입하면 부팅이 막힌다
  - [x] `reference → concept` `up:`을 주입하면 L4 ERROR가 난다
  - [x] `GRAPH_ENFORCE=0`이면 로드된다
  - [x] 런타임 reload 실패 시 구 데이터가 유지된다
  - [x] **`permanent/concept/` 파일만 고친 커밋이 pre-commit 검증을 탄다**
  - [x] **`permanent/` 루트 파일만 고친 커밋도 검증을 탄다** (기존 구멍 해소 확인)
- **완료 증거**:
  - `layer_rules_enforced()` 기본값을 `0` → **`1`(enforce)** 로 전환. `GRAPH_LAYER_ENFORCE=0` 이 kill-switch — `GRAPH_ENFORCE` 와 같은 패턴.
  - **`app/scripts/install_hooks.sh` 트리거 구멍 수정** — `^(persona|reference|products)/` → `^(persona|reference|permanent|inbox|products)/`. WORK-010 이 permanent 를 그래프 노드로 배선했으나 훅이 따라가지 않아, permanent 노트만 고친 커밋은 검증을 타지 않고 부팅 시점에야 걸렸다. concept 추가가 그 구멍을 키우므로 함께 막았다.
  - **실측 4종**:
    - 기본(enforce ON) 실데이터 부팅 → **OK · ERROR 0**
    - `GRAPH_LAYER_ENFORCE=0` → OK (kill-switch 동작)
    - `up`/`aliases` 없는 concept 주입 → **`GraphEnforcementError` 로 부팅 차단 ✓** (3건 보고: aliases 필수 / up 필수 / concept orphan)
    - 같은 상태에서 kill-switch 켜면 → 부팅 OK (즉시 해제 가능)
  - 신규 테스트 `tests/test_graph_layers.py` **24건** — layer 도출 4 · 방향 8(양방향 + 층없음 타겟 + idea) · 필수필드 5 · 층별 orphan 5 · enforce/kill-switch 3.

> **기존 구멍**: `install_hooks.sh:34`의 트리거가 `^(persona|reference|products)/`인데 **`permanent/`가 빠져 있다.** WORK-010이 permanent를 그래프 노드로 배선했으나 훅 트리거는 따라가지 않았다. 지금은 permanent 노트만 고쳐 커밋하면 그래프 검증이 돌지 않고 부팅 시점에야 걸린다. `inbox/`(idea 노드)도 같다. concept 추가가 이 구멍을 확대하므로 여기서 함께 막는다.

## Pre-deploy Check

- [ ] Phase 2가 끝나 신규 위반이 0인 상태에서만 Phase 5를 켠다
- [ ] `GRAPH_ENFORCE` kill-switch 동작 확인 (부팅 brick 대비)
- [ ] `_graph.json` 계약 변경(`layer` 추가)이 기존 FE `/graph`를 깨지 않는지 확인 — 추가 필드라 무시되면 정상
- [ ] 기존 156건 L5 WARN이 사라져도 운영 경보 파이프라인에 영향이 없는지 확인

## Rollback

- Phase 5 → `GRAPH_ENFORCE=0`으로 즉시 차단 해제. 부팅이 살아난다.
- Phase 3 → `permanent/concept/`가 비어 있으면 노드 0이라 무영향. 로더 배선만 revert.
- Phase 1 → rank 테이블·연산자를 원복. `layer`는 추가 필드라 소비자가 없으면 무해.
- DB 변경이 없어 migration revert 절차가 없다.

## Done Criteria

- [ ] 모든 Phase가 `DONE`이다.
- [ ] `permanent/concept/`에 concept를 쓰면 검증을 통과하고 그래프에 계보로 잡힌다.
- [ ] L5 orphan 156건이 위반이 아니라 미소화 큐 지표로 나온다.
- [ ] `rules/knowledge-note-pipeline.md`와 `templates/knowledge/`가 존재한다.
- [ ] enforce ON 상태에서 실데이터 부팅이 성공한다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- ~~**Phase 1의 측정 결과가 이 work의 실제 범위를 정한다.** L4 반전으로 기존 데이터가 크게 깨지면 Phase 2가 별도 work로 분리될 수 있다.~~ **해소** — 위반 **1건**뿐이라 Phase 2 가 Phase 3 와 자연히 합쳐졌다. 분리 불필요.
- ~~`rules/knowledge-note-pipeline.md`와 SPEC-001/002/004의 경계가 흐려질 위험.~~ **해소** — 규칙 문서 첫머리에 "규칙=쓸 때 / spec=검증 계약" 경계를 명시하고, 검증 규칙은 요약만 두고 SPEC-004 를 가리키게 했다.
- ~~**(신규) `_TYPE_RANK`·`KNOWLEDGE_NODE_TYPES` 가 죽은 코드로 남아 있다.**~~ **해소** — 소비자를 전수 조사한 결과 `KNOWLEDGE_NODE_TYPES` 는 **참조 0**, `_TYPE_RANK` 는 정의부와 주석·테스트 주석뿐이었다(실행 코드 참조 0). 둘 다 제거하고, rank 비교 방향이 뒤집혔다는 경고는 "종전 테이블(제거됨)과 반대"로 고쳐 남겼다 — 되돌리거나 이식할 때 **테이블과 연산자를 함께 보라**는 정보는 코드가 사라져도 유효하다.

- ~~**(잔여) concept 입도 규칙은 아직 없다**(KDEV-DEC-010 OQ-2).~~ **잠정 규칙으로 닫는다.** 표본 2건으로 확정할 수는 없으나, 따를 기준 없이 열어두면 WORK-015 가 매번 즉흥 판단을 하게 된다. 기준과 재검토 트리거를 `rules/knowledge-note-pipeline.md` 에 명시했다.
  - **기준: 독립 재사용 가능성.** 다른 자료·다른 맥락에서 이 개념만 따로 등장할 수 있으면 별개 개념이다.
  - 보조 신호 — `aliases` 를 붙일 수 있는가(이름이 있다 = 독립체다), "X는 ~이다" 한 문장 정의가 써지는가.
  - 이번 2건 검산: "구조와 내용 분리"는 API 설계에서도, "결정론적 뼈대 우선"은 컴파일러 맥락에서도 독립 등장한다 → 분리 타당. 반면 "그래프=위치, 위키=내용"은 전자의 **구성 요소**라 단독으로 등장하지 않는다 → 쪼개지 않는다.
  - **재검토 트리거**: concept 10건 도달 시, 또는 **같은 개념이 두 파일로 갈라진 사례가 처음 나올 때**(입도가 너무 잘다는 신호) 중 먼저 오는 것.

- ~~**(신규) 미소화 큐 157건이 그대로다.**~~ **정책으로 닫는다 — 손으로 소급하지 않고 파이프라인이 소비한다.**
  - **판단 정정**: 처음에는 "부트캠프 필기라 개념 뽑을 가치가 적다"고 적었으나, 파일을 열어보니 틀렸다. `bitcamp` 83 + `BackendSchool` 23 + `network` 7 = **113건이 개념 자료**다(예: `2024-05-24-Day01` = "Web Application의 정의 / 컴퓨터 구성 / Client·Server 구조"). 정제 가치는 충분하다.
  - `codingTest` 27건만 성격이 다르다 — 문제 하나의 풀이 기록이라 개념이 아니라 **사례**다. 뽑는다면 문제가 아니라 "그리디"·"투 포인터" 같은 **패턴**이다. 파이프라인에 태울 때 다른 취급이 필요할 수 있다.
  - **결론**: 157건은 기술부채가 아니라 **파이프라인의 입력 백로그**다. 손으로 일괄 정제하지 않는다 — WORK-014/015 완성 후 큐에서 골라 태운다. 따라서 **큐 크기를 경보로 쓰지 않는다**(줄지 않아도 문제가 아니다).

## Related

- SPEC: frontmatter `links.specs` 참조
- Work: WORK-010(permanent 배선 — 이 work가 미러하는 선례), 후속 WORK-014
