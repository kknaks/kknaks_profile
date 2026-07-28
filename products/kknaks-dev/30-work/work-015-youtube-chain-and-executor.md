---
type: work
id: KDEV-WORK-015
title: "유튜브 체인 완성 + Apply Executor"
status: todo
product: kknaks-dev
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 0
created_at: 2026-07-27
updated_at: 2026-07-27
tags:
  - product/kknaks-dev
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
  decisions:
    - "[[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]]"
    - "[[decision-011-approval-gate-chain|KDEV-DEC-011]]"
  specs:
    - "[[spec-008-gate-chain|KDEV-SPEC-008]]"
    - "[[spec-010-apply-executor|KDEV-SPEC-010]]"
    - "[[spec-004-graph-validation|KDEV-SPEC-004]]"
  works:
    - "[[work-014-queue-and-route-gate|KDEV-WORK-014]]"
  releases: []
  related: []
---

# 유튜브 체인 완성 + Apply Executor

route 뒤의 게이트 3종(`source_note`·`concept`·`derived`)을 붙이고, 마지막 승인이 **md 여러 장을 한 커밋으로 발행**하게 만든다. 여기까지 오면 유튜브 하나가 끝에서 끝까지 돈다.

> 만들지 않는 것: 커밋·블로그·스케줄 파이프라인, 트리 문서 렌더러, 기존 스케줄 잡의 편입. 이 work는 **유튜브 한 종류를 완주**시키는 것이 목표다.

## Meta

- Baseline: KDEV-BL-003
- Covers spec: KDEV-SPEC-008(전부) · KDEV-SPEC-010(전부) · KDEV-SPEC-004(발행 전 검증)
- Depends on work: WORK-014
- Parallel work: 없음
- Follow-up work: 스케줄 잡 편입, 트리 문서 렌더러, 나머지 파이프라인 정의
- External dependency: open-kknaks, GitHub push 권한(기존 `GH_TOKEN_PERSONAL`), **`templates/knowledge/` (WORK-013 Phase 4 산출물 — 없으면 스테이지 프롬프트를 조립할 수 없다)**

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | todo |
| Progress | 0% |
| Branch/PR | — |
| Blocker | WORK-014 선행 |
| Next | Phase 1 source_note 게이트 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 완주 기준 판단 | todo |
| Design | kknaks | 게이트 스택·diff 표시 | todo |
| FE | kknaks | 게이트 3종 UI | todo |
| BE | kknaks | 스테이지 생성·Executor | todo |
| QA | kknaks | 롤백·검증 거부 시나리오 | todo |
| Ops | kknaks | 실발행 e2e | todo |

## Scope

포함:

- `source_note` 게이트 — reference 초안
- `concept` 게이트 — 개념 추출 + **신규/보충 판정** + 개별 제외 토글
- `derived` 게이트 — 교안 (route에서 켠 경우만)
- 목적지 재검토(route 재오픈 + 뒤 게이트 무효화)
- Apply Executor — 계획 조립·검증 6종·원자적 커밋·전량 롤백·결과 기록
- 발행 전 그래프 검증 (WORK-013의 `validate_graph` 호출)
- 발행 재시도 (AI 미호출)

제외:

- 커밋·블로그·스케줄 파이프라인 정의
- 기존 잔디·algorithm·content_enrich 잡의 Executor 전환
- 트리 문서 렌더러 (SPEC-005)
- 게시 판정 게이트 (`persona/posts/` 배선 선행 필요)

## Code Surface

- Repo / module: `app/back`, `app/front`

| 경로 후보 | 설명 |
|---|---|
| `app/back/alembic/versions/0004_*` | `apply_plans`·`apply_results` |
| `app/back/service/pipeline/stages/` | source_note·concept·derived 스테이지 |
| `app/back/service/pipeline/concept_match.py` | `aliases` 기반 기존 concept 매칭 |
| `templates/knowledge/*.md` | **읽기 전용 입력** — 스테이지 프롬프트에 주입 (WORK-013 산출물) |
| `app/back/service/apply/executor.py` | 계획 조립·검증·쓰기·커밋·롤백 |
| `app/back/core/graph.py` | 발행 전 가상 그래프 검증 진입점 |
| `app/back/service/jobs/git_push.py` | 원자적 커밋·롤백 지원 확장 |
| `app/front/components/admin/` | 게이트 3종 카드, diff 뷰, 제외 토글 |

- Domain / schema note: 마이그레이션 1건(0004). 나머지는 WORK-014에서 생성됨.

## Domain / Schema

| Entity | 역할 |
|---|---|
| `apply_plans` | 발행 계획 (file_actions) |
| `apply_results` | 발행 결과 (커밋 참조·위반·실패 사유) |

- 상태 / invariant: 한 발행 = 한 커밋 · 부분 적용 없음 · 이력 불변
- Migration 필요 여부: 필요 (0004)

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| 후속 파이프라인(커밋·블로그) | 스테이지 러너·Executor | 파생 슬롯만 바꿔 재사용한다 |
| 트리 문서 렌더러 | 발행된 md + `_graph.json` | 발행이 돌아야 볼 게 생긴다 |

## Internal Interface Contract

**concept 매칭 결과의 형태**를 고정한다. UI diff와 Executor가 이것만 본다.

```text
concept_result[] = {
  mode: "create" | "supplement",
  stem: <대상 concept stem>,
  matched_by: <어떤 alias로 찾았는지 · create면 null>,
  content: <전문 markdown>,
  excluded: <owner가 제외 토글했는지>
}
```

**발행 계획**의 `file_actions[]`는 SPEC-010 Data Contract를 따른다. AI는 `filename_stem`만 내고 **디렉토리는 시스템이 층·목적지에서 조립**한다.

## Execution

### Phase 1 — source_note 게이트

- **Status**: TODO
- **작업**:
  - [ ] route 승인 후 `source_note` 게이트 자동 생성
  - [ ] **`templates/knowledge/reference.md`를 프롬프트에 주입** (WORK-013 Phase 4 산출물)
  - [ ] reference 초안 생성 (준비 산출물 + route 결과 + 템플릿 입력)
  - [ ] 초안이 `up:`·본문 `[[]]`를 채우도록 프롬프트·검증
  - [ ] 게이트 카드 UI (전문 미리보기 + 저장될 경로)
- **검증**:
  - [ ] route 승인 시 다음 게이트가 열린다
  - [ ] 초안 형식이 템플릿과 일치한다 (섹션 구성·frontmatter 필드)
  - [ ] 초안에 `up:`이 채워진다 (**lineage 생성 의무 충족**)
  - [ ] 승인해도 **아직 파일이 생기지 않는다**
- **완료 증거**: 미작성

### Phase 2 — concept 게이트

- **Status**: TODO
- **설명**: 이 work의 난이도 핵심. 개념 추출보다 **기존 개념 매칭**이 어렵다.
- **작업**:
  - [ ] 개념 추출 스테이지
  - [ ] **`templates/knowledge/concept.md`를 프롬프트에 주입**
  - [ ] 기존 concept 매칭 — stem + `aliases` 인덱스 조회
  - [ ] 신규/보충 판정 + 보충 시 수정 전문 생성
  - [ ] 보충 diff 계산 (표시용)
  - [ ] 개별 제외 토글 UI + 묶음 승인
- **검증**:
  - [ ] 같은 개념의 두 번째 영상이 **새 파일이 아니라 보충**으로 판정된다
  - [ ] `aliases`로만 매칭되는 경우(예: "음성인식" ↔ `stt`)도 잡힌다
  - [ ] 보충 diff에 **사라지는 줄이 보인다**
  - [ ] 제외한 개념이 발행에서 빠진다
  - [ ] 신규 concept 형식이 템플릿과 일치하고 `aliases`·`up:`이 채워진다
  - [ ] 보충 시 대상 노트의 기존 `aliases`가 유실되지 않는다
- **완료 증거**: 미작성

> 템플릿 주입이 빠지면 AI가 매번 다른 형식으로 초안을 만들고, 그중 상당수가 Phase 4의 발행 전 검증(`aliases`·`up:` 필수)에서 거부된다. 템플릿은 참고자료가 아니라 **생성 계약의 일부**다.

### Phase 3 — derived 게이트 + 재오픈

- **Status**: TODO
- **작업**:
  - [ ] `derived` 게이트 (교안) — route에서 켠 경우만 생성
  - [ ] `content_enrich`의 교안 프롬프트 재사용
  - [ ] 목적지 재검토 → route 재오픈 + 뒤 게이트 `cancelled`
  - [ ] 재오픈 시 자동 준비 산출물 재사용
- **검증**:
  - [ ] route에서 교안을 끄면 이 게이트가 생성되지 않는다
  - [ ] 재오픈 시 뒤 게이트가 무효화되고 **기록은 조회 가능**하다
  - [ ] 재오픈이 수집·요약을 다시 실행하지 않는다
  - [ ] 재오픈 후 파생 on/off를 바꾸면 체인 길이가 바뀐다
- **완료 증거**: 미작성

### Phase 4 — Apply Executor

- **Status**: TODO
- **작업**:
  - [ ] Alembic 0004 (`apply_plans`·`apply_results`)
  - [ ] 승인된 게이트 산출물 → 발행 계획 조립 (경로는 시스템 조립)
  - [ ] 검증 6종 (경로 allowlist·층-경로 정합·L1~L6·`up:` 필수·신규 중복·stale 대상)
  - [ ] 원자적 쓰기 + **한 커밋** + push
  - [ ] 실패 시 전량 롤백 (파일 되돌림 + 커밋 되돌림)
  - [ ] 발행 결과 기록 + 재시도(AI 미호출)
  - [ ] reload 요청 (거부돼도 롤백하지 않음)
- **검증**:
  - [ ] 마지막 게이트 승인이 발행을 트리거한다
  - [ ] `reference` + `concept` 신규/보충이 **한 커밋**으로 나간다
  - [ ] 깨진 wikilink를 주입하면 **파일이 하나도 생기지 않고** 거부된다
  - [ ] `up:` 없는 concept를 주입하면 거부된다
  - [ ] push 실패를 강제하면 커밋이 되돌려지고 서버가 origin 상태가 된다
  - [ ] 발행 재시도가 AI를 호출하지 않는다
  - [ ] stale 대상(초안 후 파일 변경)이 거부된다
- **완료 증거**: 미작성

### Phase 5 — 실전 e2e

- **Status**: TODO
- **설명**: 실제 유튜브 1건을 끝까지 돌리고 노트북에서 확인한다. 여기서 나오는 관찰이 보류된 OQ들의 답이 된다.
- **작업**:
  - [ ] 실제 영상 1건으로 접수 → 승인 → 발행
  - [ ] 노트북에서 `git pull` 후 옵시디언 확인
  - [ ] 같은 개념이 나오는 두 번째 영상으로 **보충 경로** 확인
  - [ ] 관찰 결과를 OQ에 환류
- **검증**:
  - [ ] 노트북 옵시디언에서 `permanent/concept/*.md`가 보이고 `up:` 계보가 걸려 있다
  - [ ] 백링크로 이 개념을 인용한 문서가 보인다
  - [ ] 두 번째 영상이 기존 concept를 보충한다
  - [ ] 승인 횟수와 소요 시간을 기록한다 (마찰 실측)
  - [ ] concept 입도가 적절한지 판단해 기록한다
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] `JOB_GIT_PUSH_DRY_RUN`으로 먼저 dry-run 발행을 검증한 뒤 실발행으로 전환
- [ ] 발행이 `origin/main`에 직접 나가므로 첫 실행은 관찰 하에 수행
- [ ] 롤백 경로(파일·커밋)가 실제로 동작하는지 강제 실패로 확인
- [ ] 기존 `content_enrich` 잡과 발행 대상이 겹치지 않는지 확인 (같은 `C-NNN`을 두 경로가 건드리면 충돌)

## Rollback

- Executor를 비활성화하면 게이트는 승인되되 발행이 일어나지 않는다(항목이 `publishing`에서 멈춤).
- Alembic downgrade 0004 → 0003.
- 이미 발행된 노트는 git에 있으므로 되돌리려면 직접 커밋으로 처리한다(발행 후 정정은 제품 기능이 아님 — SPEC-010 D7).

## Done Criteria

- [ ] 모든 Phase가 `DONE`이다.
- [ ] 유튜브 1건이 접수 → 준비 → 게이트 → 발행까지 완주한다.
- [ ] `reference` + `concept`가 한 커밋으로 나가고 노트북에서 확인된다.
- [ ] 같은 개념의 두 번째 출처가 기존 concept를 보충한다.
- [ ] 발행 실패가 조용히 묻히지 않고 재시도할 수 있다.
- [ ] 실측 결과가 보류 OQ(concept 입도·승인 마찰·stale 빈도)에 환류됐다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- **concept 매칭 정확도가 이 파이프라인의 실질 품질을 결정한다.** 매칭이 틀리면 개념이 갈라지거나(놓침) 엉뚱한 노트를 덮어쓴다(오매칭). Phase 2에서 오매칭 쪽을 더 보수적으로 잡을지(의심되면 신규 생성) 판단이 필요하다.
- AI가 신규/보충을 틀렸을 때 owner가 게이트에서 직접 "기존 X에 합쳐라"로 바꿀 수 있어야 하는지 — 지금 계약은 피드백 재생성뿐이다(SPEC-008 §7).
- 발행 커밋 메시지 형식(DEC-012 OQ-1), 실패 알림 임계(DEC-012 OQ-4)를 이 work에서 정한다.
- 가상 그래프 검증을 전체 재조립으로 할지 증분으로 할지(SPEC-010 §7) — 406노드 기준 실측 후 결정.

## Related

- SPEC: frontmatter `links.specs` 참조
- Work: 선행 WORK-014
