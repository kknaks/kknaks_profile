---
type: work
id: KDEV-WORK-003
title: "지식층 scaffold + 작성 규약 (분류·정제·up·archive + agent.md 읽기범위)"
status: done
product: kknaks-dev
work_type: scaffold
owner: "profile-be"
roles:
  pm: ""
  design: ""
  fe: ""
  be: "profile-be"
  qa: ""
  ops: ""
progress: 100
created_at: 2026-06-29
updated_at: 2026-06-29
tags:
  - product/kknaks-dev
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions: []
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
    - "[[spec-003-knowledge-workflow|KDEV-SPEC-003]]"
  works:
    - "[[work-002-validator-refinement|KDEV-WORK-002]]"
  releases: []
  related: []
---

# 지식층 scaffold + 작성 규약 (분류·정제·up·archive + agent.md 읽기범위)

지식 파이프라인 층(inbox/reference/permanent/+archive, persona/posts)을 **빈 디렉토리로 만들고**, 각 층에 "여기 무엇을 어떻게 두는가" 작성 규약을 README로 박는다. `agent.md`에 지식층 읽기범위(archive cold 제외)를 추가한다. 데이터 이동은 없다(WORK-004~006). 여전히 **report-only**.

> 비목표: 실제 콘텐츠 마이그레이션(projects/notes/contents 이동 = WORK-004~006), 라우트/loader 키 신설(WORK-004~006), enforcement ON(WORK-007), 시각화(WORK-008/009). **이 work는 빈 층 + 규약 문서 + agent.md만 만든다.**

## Meta

- Baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- Covers spec: [[spec-001-directory-structure|KDEV-SPEC-001]] (디렉토리 존재·규약), [[spec-003-knowledge-workflow|KDEV-SPEC-003]] (작성 규약 문서화 — 강제는 WORK-007)
- Depends on work: [[work-002-validator-refinement|KDEV-WORK-002]] (navigational 노드 제외 = 이 work의 README가 그래프를 오염시키지 않는 전제)
- Follow-up work: WORK-004(projects→products), WORK-005(notes→reference), WORK-006(contents→reference/posts) — 이 scaffold가 채워질 종착지
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | scaffold |
| Owner | profile-be |
| Status | done |
| Progress | 100% |
| Branch/PR | feat/knowledge-graph (커밋 2751de0) |
| Blocker | - |
| Next | WORK-004~006 마이그레이션 (이 빈 층에 실제 콘텐츠 이동) |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| BE/문서 | profile-be | 디렉토리 scaffold + navigational README + agent.md 읽기범위 | done |
| QA | admin | pytest 게이트(persona_loader/graph build 무영향) + scaffold 확인 | done (260 passed) |

> 코드 변경 없음(app/back 무수정). 순수 디렉토리 + 마크다운. 라우팅은 admin이 발주 직전 확정.

## Scope

포함:
- **루트 지식층 디렉토리 생성**: `inbox/`, `reference/`, `permanent/`, `permanent/archive/`, `persona/posts/`.
  - git이 빈 디렉토리를 추적하지 않으므로 각 디렉토리에 **navigational README**(frontmatter `type` 없음)를 둬서 디렉토리를 실재화한다.
- **각 README = 얇은 작성 규약**: "이 층은 무엇 / 무엇을 두고 안 두나 / type 값 / 규약 SSOT 포인터". SPEC 본문을 복사하지 않는다(아래 §Deliverable Spec).
- **agent.md 읽기범위 규칙**: 평소 스캔은 활성 지식층(inbox/reference/permanent, persona/posts), `permanent/archive/`는 cold = 명시 요청 시만 읽음(D-005).

제외:
- 실제 콘텐츠 이동·삭제(projects/notes/contents) → WORK-004~006
- `/projects`·`/notes`·`/contents`·`/posts`·`/reference` 라우트, loader 키, `jobs/inputs.py` 정합 → WORK-004~006 (이동과 lockstep)
- enforcement(L1~L4 ERROR/fail-fast/CI) → WORK-007
- `reference/archive/` 대칭 디렉토리 — 필요 판단은 WORK-005에서(자료 cold 보관 수요 확인 후). 지금 안 만든다.

## Code Surface

| 경로 | 동작 |
|---|---|
| `inbox/README.md` | 신규 — navigational, idea 층 규약 |
| `reference/README.md` | 신규 — navigational, reference 층 규약 |
| `permanent/README.md` | 신규 — navigational, permanent 층 규약 |
| `permanent/archive/README.md` | 신규 — navigational, cold 보관 + 부활 규약 |
| `persona/posts/README.md` | 신규 — navigational, post 층 규약 |
| `agent.md` | 편집 — "지식층 읽기범위" 섹션 추가 |

- Domain/schema note: **app/back 코드 무수정**. README는 frontmatter `type`이 없어 그래프 노드가 아니다(WORK-002 Phase 2: type 없으면 노드 제외). 따라서 빌더/검증기/`_graph.json` 무영향, L5 orphan 여전히 0(지식 노드는 WORK-004~006에서 도착). "디렉토리가 노드 타입 1차 결정"(SPEC-001 §5)은 층에 놓이는 **지식 노트**에 적용되며 층 자신의 README에는 적용되지 않는다 → WORK-007의 L2(type 필수)가 scaffold README에서 터지지 않는다.

## Deliverable Spec — navigational README 내용 규약

각 README는 **얇게**(SSOT = SPEC-001/003, 여기는 운영 quick-reference). 공통 골격:

```markdown
# {층 이름}

{한 줄 정체성}. 노드 타입: `{type}` (또는 navigational).

## 여기 두는 것
- {1~3줄}

## 여기 두지 않는 것
- {1~2줄 + 올바른 위치 포인터}

## 작성 규약 (SSOT)
- 디렉토리 계약: [[spec-001-directory-structure|KDEV-SPEC-001]]
- 생명주기/정제: [[spec-003-knowledge-workflow|KDEV-SPEC-003]]
```

층별 핵심 한 줄(전체 규약은 SPEC 참조, 여기 복붙 금지):

| README | 정체성 | type | 핵심 quick-rule |
|---|---|---|---|
| inbox | 미정제 아이디어 휘발 inbox | idea | 빨리 던진다. 정제 후 종착지로 분류하면 **원본 폐기**. up 대상 아님 |
| reference | 외부 자료(영상·책·아티클) 정리 | reference | 출처는 `source: <url>` 속성. 본문 `[[]]`로 인용됨(종착지 아님) |
| permanent | 내 언어로 정제한 영구노트 | permanent | 한 노트=한 생각. 기반은 `up: [stem]` + 본문 `[[]]`. 안 쓰면 archive/로 |
| permanent/archive | cold 장기기억 | permanent (archived) | stem 유지(링크 보존). 부활=폴더 한 칸 위로. LLM 평소 미스캔 |
| persona/posts | 발행물(영구노트→글) | post | 종착 SSOT. permanent와 평행(중복 아님), `up:`으로 계보 표시 |

- README 자신은 frontmatter `type`을 **달지 않는다**(navigational, 노드 아님). 표의 type은 그 층에 놓이는 노트가 가질 값을 안내하는 것.

## Execution

### Phase 1 — 지식층 디렉토리 + navigational README

- **Status**: DONE
- **설명**: 5개 디렉토리 생성 + 각 navigational README(위 Deliverable Spec 골격).
- **작업**:
  - [x] `inbox/README.md`
  - [x] `reference/README.md`
  - [x] `permanent/README.md`
  - [x] `permanent/archive/README.md`
  - [x] `persona/posts/README.md`
- **검증**:
  - [x] 5개 디렉토리·README 존재, README에 frontmatter `type` 없음(navigational)
  - [x] 각 README가 SPEC-001/003을 본문 복사 없이 포인터로만 참조
- **완료 증거**: 5개 navigational README 생성, `grep '^type:'` 5개 모두 미검출(그래프 노드 아님). 각 README는 얇은 quick-reference로 SPEC-001/003을 본문 복사 없이 `[[]]` 포인터로만 참조. (리포트 PLAN-003-T-006 P1)

### Phase 2 — agent.md 읽기범위

- **Status**: DONE
- **설명**: agent.md에 지식층 읽기범위 섹션 추가 — 활성 층 평소 스캔, archive는 명시 요청 시만(D-005).
- **작업**:
  - [x] agent.md에 "지식층 읽기범위" 섹션: inbox/reference/permanent + persona/posts = 평소 스캔, `permanent/archive/` = cold 제외
- **검증**:
  - [x] 시작 흐름/Hook 기존 섹션 무손상, 신규 섹션만 추가
- **완료 증거**: `agent.md` +10/-0 (`git diff --numstat` = `10 0 agent.md`). "## 지식층 읽기범위" 섹션만 끝에 추가, 시작 흐름·목적·응답 종료 전 Hook 기존 섹션 전부 무손상. (리포트 PLAN-003-T-006 P2)

### Phase 3 — 회귀 검증 (report-only 유지)

- **Status**: DONE
- **설명**: scaffold가 빌더/로더/그래프에 무영향임을 확인.
- **작업**:
  - [x] `cd app/back && RUN_SCHEDULER=0 uv run python -m pytest` green
  - [x] persona_loader/graph build가 빈 `persona/posts/` + navigational README에 영향 없음(노드 수 무변경, L5 orphan 0 유지)
- **검증**:
  - [x] 여전히 report-only(enforcement 미적용)
  - [x] `_graph.json` 노드 수 회귀 없음
- **완료 증거**: pytest **260 passed**. 동일 빌드 경로(`load_persona()` in-memory) before/after 모두 노드 303·엣지 307·L5 orphan **0** — 무변경. 신규 루트 층·`persona/posts/`는 로더 스캔 대상 아니고 navigational README는 type 없어 노드 제외 → report-only 불변. (리포트 PLAN-003-T-006 P3)

## Pre-deploy Check

- [ ] **report-only** 유지 (enforcement = WORK-007)
- [ ] 콘텐츠 이동 0건 (projects/notes/contents 그대로) — 마이그레이션은 WORK-004~006
- [ ] 라우트/loader 무변경 — 빈 층은 아직 블로그에 안 보임(정상, WORK-004~006에서 배선)

## Rollback

- 신규 디렉토리/README 삭제 + agent.md 섹션 제거. 코드 무변경이라 서비스 영향 0.

## Done Criteria

- [x] inbox/reference/permanent(+archive) + persona/posts 디렉토리 존재 (navigational README로 실재화)
- [x] 각 README에 얇은 작성 규약(분류·정제·up·archive) — SPEC-001/003 포인터, 본문 복사 없음
- [x] agent.md 읽기범위 규칙(archive cold 제외) 추가
- [x] pytest green + persona_loader/graph build 무영향 (report-only)
- [x] 30-work/README·log 갱신 (PLAN-003-T-007)

> ⚠ 미달성 항목 (이 work 비목표 — 혼동 방지): SPEC-001의 마이그레이션 AC(projects→products·notes/contents 재편 완료)와 SPEC-003의 런타임 AC(inbox 미분류만·중복 0·idea up 금지)는 **WORK-004~006이 채우고 WORK-007이 강제**한다. 이 work는 "층 존재 + 규약 문서화"까지만.

## Open Issues

- `reference/archive/` 대칭 보관 디렉토리 필요 여부 — WORK-005(notes→reference) 시 자료 cold 수요 확인 후 결정. 지금은 미생성.
- 발주 라우팅(profile-be vs profile-planner) — 코드 0·순수 문서/디렉토리라 profile-planner 영역에 가깝지만, admin이 발주 직전 확정.

## Related

- Spec: [[spec-001-directory-structure|KDEV-SPEC-001]], [[spec-003-knowledge-workflow|KDEV-SPEC-003]]
- Work: [[work-002-validator-refinement|KDEV-WORK-002]], [[work-001-graph-builder-validator|KDEV-WORK-001]]
