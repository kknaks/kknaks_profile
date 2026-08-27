---
type: spec
id: KDEV-SPEC-004
title: "그래프 검증 게이트 — L1~L6"
status: draft
product: kknaks-dev
version: 0.0.6
created_at: 2026-06-29
updated_at: 2026-08-10
tags:
  - product/kknaks-dev
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
  decisions:
    - "[[decision-006-validation-gates|KDEV-DEC-006]]"
    - "[[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]"
    - "[[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]]"
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
    - "[[spec-002-graph-schema|KDEV-SPEC-002]]"
    - "[[spec-003-knowledge-workflow|KDEV-SPEC-003]]"
  works: []
  releases: []
  related: []
---

# 그래프 검증 게이트 — L1~L6

지식그래프는 SoT라 정합성이 자동 검증되어야 한다. lint 규칙 6개와 실행 지점, report-only→enforce 순서에 대한 계약.

> v0.0.6 — [[decision-019-drop-synthesis-layer|KDEV-DEC-019]] 반영. **판단층(`synthesis`/`permanent`)을 폐기**하고 지식층을 `source → concept → execution` 3층으로 줄인다.
>
> v0.0.5 — [[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] D5(층별 orphan 재정의)·D4(`up:` 생성 의무)와 [[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]] D6(발행 전 검증 지점) 반영. **L5가 층마다 다른 의미를 갖게 되고, orphan 156건이 위반이 아니라 작업 큐로 뒤집힌다.**

## 1. Context

### Meta

- Decision reference: [[decision-006-validation-gates|KDEV-DEC-006]], [[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]], [[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]]
- Baseline reference: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]], [[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]
- Domain note: 레벨 = ERROR(차단) / WARN(리포트) / INFO(집계). 실행 = pre-commit · **발행 전** · 부팅.
- Open questions: §7

### Business Requirement

깨진 링크·잘못된 분류·SSOT 중복을 사람이 수동 추적하지 않고 자동 차단한다.

여기에 더해 **경보가 실제 신호를 내야 한다.** WORK-005에서 `persona/notes/` 157개를 `reference/`로 재타이핑한 뒤 L5 orphan이 156건 WARN으로 고정됐다. 모든 자료가 orphan인 상태에서 orphan 경보는 정보가 아니다 — 켜 두면 무시하게 되고, 그러면 진짜 위반도 같이 묻힌다. 층마다 orphan의 의미가 다르므로 판정을 분리한다.

그리고 승인 파이프라인이 도입되면 **AI가 만든 노트가 발행되기 전에** 검증돼야 한다. 커밋한 뒤 부팅 검증에서 걸리면 이미 origin에 나간 뒤다.

### Scope

In scope: 규칙 정의, 레벨, 층별 판정, 실행 지점(발행 전 포함), enforcement 적용 순서.
Out of scope:
- 검증 함수 구현(work)
- 스키마·`layer` 도출·rank 정의([[spec-002-graph-schema|KDEV-SPEC-002]])
- 디렉토리-층 매핑([[spec-001-directory-structure|KDEV-SPEC-001]])
- 발행 계획 자체의 검증(경로 allowlist·신규 중복·stale 대상) → Apply Executor spec. **이 spec은 그중 L1~L6만 소유한다.**

## 2. UX Contract

해당 없음 (lint 리포트는 콘솔/CI 출력).

## 3. User Scenario

### S-1. 작성자 — 커밋 시 검증

1. 노트를 커밋하면 pre-commit이 lint 실행.
2. ERROR(L1~L4)가 있으면 커밋 거부 + 위반 목록 출력.
3. WARN(L5/L6)은 리포트만, 커밋 통과.

### S-2. 시스템 — 부팅 시 검증

1. 백엔드 부팅 시 `persona_loader`가 그래프 검증.
2. ERROR면 fail-fast (오염된 SoT로 서버 안 뜸).

### S-3. 시스템 — 발행 전 검증

1. 승인 게이트의 마지막 승인으로 Apply Executor가 발행 계획을 받는다.
2. 계획대로 적용했을 때의 그래프를 **가상으로 조립해** L1~L6를 돌린다.
3. ERROR가 하나라도 있으면 **발행 전체를 거부**한다(부분 적용 없음). 사유를 admin에 노출하고 게이트는 승인 상태를 유지한다.
4. 통과하면 파일을 쓰고 커밋·push한다.

> 검증을 커밋 **전**에 두는 이유: 커밋한 뒤 부팅 검증에서 걸리면 이미 origin에 나간 뒤다. 되돌리려면 git 히스토리를 건드려야 한다.

## 4. Interface Contract

### Data Contract — 규칙

| ID | 검사 | 레벨 |
|---|---|---|
| L1 dead link | 본문 `[[stem]]`·`up:` 타겟이 실존 | ERROR |
| L2 노드 스키마 | `id`/`type` 필수, type 허용값, **type별 필수 필드**, 파일명 stem·alias 전역 유일(=SSOT 중복 금지) | ERROR |
| L3 오버레이 정합 | `up:`의 모든 stem이 본문 `[[]]`에도 존재 | ERROR |
| L4 방향 정합 | `up:` 타겟의 rank ≤ 자기 rank, `idea` up 금지 | ERROR |
| L5 orphan | 엣지 0개 노드 — **층별로 판정이 다르다**(아래) | 층별 |
| L6 archive 참조 | 활성 노트가 `archived`를 `up`으로 의존 | WARN |

#### L2 — type별 필수 필드 (v0.0.5 신규)

| type | 추가 필수 필드 | 근거 |
|---|---|---|
| `concept` | `aliases`, `up` | 개념 중복 방지 + 출처 없는 개념은 성립하지 않음 |
| `idea` | (`up` **금지**) | 휘발이라 상류가 될 수 없음 |

`up:` 생성 의무([[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] D4)는 파이프라인 생성 계약이자 **여기 L2 규칙으로도 강제**된다. 손으로 쓴 노트든 AI가 만든 노트든 같은 기준을 받는다.

#### L5 — 층별 orphan 판정 (v0.0.5 재정의)

| `layer` | orphan이 뜻하는 것 | 판정 |
|---|---|---|
| `source` (`reference`) | 아직 개념으로 올라가지 않은 자료 | **INFO** — 위반이 아니라 **미소화 큐**로 집계 |
| `concept` | — | **L2가 커버**(아래 주) |
| `execution` | 제품 파이프라인이 관리 | 검사 제외 |
| 층 없음 (`idea`) | 휘발이라 연결 의무 없음 | 검사 제외 |
| 그래프 밖 | — | 노드가 아님 |

> **concept의 orphan은 L5가 아니라 L2가 잡는다.** concept는 `up:`이 필수이고, `up:` 타겟이 실존하면 엣지가 생겨 orphan이 될 수 없다. 타겟이 실존하지 않으면 L1이 잡는다. 따라서 "출처도 없고 쓰이지도 않는 concept"는 **`up:` 누락 = L2 ERROR**로 도달하는 것이 유일한 경로다. [[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] D5가 `concept` orphan을 ERROR로 규정한 취지는 L2 필수 필드로 이행한다 — 도달 불가능한 L5 규칙을 따로 두지 않는다.

`source` orphan은 **위반 카운트에 넣지 않고 별도 지표로 낸다.** 이 숫자가 곧 "소화되지 않은 자료" 목록이며, 승인 파이프라인의 입력 후보다. 특정 숫자를 계약으로 고정하지 않는다(§7).

### Data Contract — 실행 지점

| 지점 | 대상 | 차단 |
|---|---|---|
| pre-commit | 작업트리 | ERROR → 커밋 거부 |
| **발행 전 (Apply Executor)** | 계획 적용 후의 가상 그래프 | ERROR → **발행 전체 거부** |
| 백엔드 부팅 | 로드된 그래프 | ERROR → fail-fast |
| 런타임 reload | 로드된 그래프 | ERROR → 구 데이터 유지 + `False` 반환 |
| CI | — | PR 플로 없어 보류(§7) |

## 5. Implementation Rules

- L1~L4 = ERROR(차단), L6 = WARN(리포트). **L5는 층별**(§4).
- **enforcement 적용 순서 (라이브 서버 brick 방지)**: 검증기는 먼저 **report-only**로 도입 → 레포 데이터 정리 후 → **맨 마지막에** ERROR/fail-fast 전환. report-only 출력이 마이그레이션 작업목록이 된다. **v0.0.5의 L2 type별 필수 필드와 L4 방향 반전에도 같은 순서를 적용한다** — 기존 데이터가 새 규칙을 통과하지 못할 수 있으므로 report-only로 먼저 측정한다.
- **L4 rank 비교 방향**(v0.0.5): `up:` 타겟의 rank가 자기 rank **이하**여야 한다. rank는 [[spec-002-graph-schema|KDEV-SPEC-002]]의 층 순서에서 나온다(`source 1 → concept 2 → execution 3`). **현행 코드는 `reference=4`에 `>=` 비교라 방향이 반대다** — rank 테이블만 교체하면 L4가 조용히 역동작하므로 비교 연산자까지 함께 바꾼다.
- **L2 노드 자격**(WORK-002 확정, 0014790): 그래프 노드 자격 = frontmatter `type` 보유. `type` 없는 navigational/legal 파일(README/log/privacy/support 및 그 아카이브 사본)은 노드가 아니다 → 중복 stem(L2)·orphan(L5) 검사 대상에서도 제외. (persona notes 는 항상 type 보유 → 무영향.)
- **L5 orphan 대상**(v0.0.5 개정): 층이 있는 노드만 대상이며 판정은 층별이다(§4). `idea`(층 없음)·`daily`·`algorithm`·`career`·`profile`·`content` 등은 제외한다. `note`는 type enum에서 제거됐다([[spec-002-graph-schema|KDEV-SPEC-002]] v0.0.3). 종전 "대상 = `reference`/`permanent`/`post`/`product` 전체에 동일 WARN" 규칙을 대체한다.
- **미소화 큐 집계**(v0.0.5 신규): `source` orphan은 위반 목록이 아니라 별도 지표로 낸다. 검증 결과 소비자(부팅·pre-commit)는 이 값으로 차단하지 않는다.
- **발행 전 검증**(v0.0.5 신규): Apply Executor는 계획을 적용한 **가상 그래프**에 L1~L6를 돌린다. ERROR가 있으면 파일을 쓰기 전에 거부한다. 경로 allowlist·층-경로 정합·신규 중복·stale 대상 검증은 Apply Executor spec이 소유하며 이 spec의 규칙이 아니다.
- **archived 노드 id/alias 면제**(WORK 후속 확정, 6f823e4): archived 노드(동결 스냅샷)는 id/alias 전역 유일(L2) 검사에서 면제한다. canonical id/alias는 live가 소유, archived는 자기 stem(`v1_0_1-*`)으로만 resolve(`build_alias_index`가 archived는 stem만 등록). → `v1_0_1-X` 사본이 live `X`와 id를 공유해도 L2 충돌 0.
- 검증 함수 구현 위치·시그니처는 work (기존 `wikilinks.dead_links()` 확장).

## 6. Verification

### Acceptance Criteria

- [ ] dead link가 있으면 ERROR로 차단된다.
- [ ] 같은 stem이 두 곳에 있으면 L2 ERROR.
- [ ] `up:`이 본문에 없으면 L3 ERROR.
- [ ] idea를 up하면 L4 ERROR.
- [ ] enforcement는 데이터 green 이후에 켜진다(부팅 brick 없음).
- [ ] `concept`에 `aliases` 또는 `up`이 없으면 L2 ERROR.
- [ ] `reference`가 `concept`를 `up`하면 L4 ERROR (rank 1 < 2, 상류 아님).
- [ ] `concept`가 `reference`를 `up`하면 통과한다.
- [ ] `reference` orphan은 위반 목록에 안 들어가고 미소화 큐 지표로만 집계된다.
- [ ] 발행 계획이 dead link를 만들면 파일을 쓰기 **전에** 거부된다.
- [ ] 발행 거부 시 부분 적용된 파일이 남지 않는다.

## 7. Open Questions

- ~~(구현 OQ, work) 검증 함수 시그니처, 리포트 출력 포맷.~~ **해소(WORK-001, abcfbc4)** — `validate_graph(nodes, duplicate_stems=None) -> list[{rule,level,node,detail}]` + `summarize()`(rule/level별 카운트). 상세 [[spec-002-graph-schema|KDEV-SPEC-002]] §4.
- ~~(OPEN, WORK-007) pre-commit/CI 훅 배선 + ERROR/fail-fast 전환 — enforcement ON 시점.~~ **해소(WORK-007, cd4e453)** — 단일 enforce 지점=`load_persona`의 `_enforce_graph`(ERROR-level만 차단, L5 WARN 통과). 3지점: pre-commit(`persona|reference|products` 트리거)+boot fail-fast(=deploy 게이트)+kill-switch `GRAPH_ENFORCE`(기본 1). boot=propagate, runtime reload=catch(구 데이터 유지). 메커니즘 4종 실증·278 passed. **CI PR merge-gate는 PR 플로 없어 보류**(boot-fail-fast-at-deploy가 deploy 게이트 역할 — PR 플로 생기면 별도).
- ~~(OPEN, WORK-002) L2 navigational 파일 처리 — 노드 제외 vs frontmatter type 부여 택일.~~ **해소(WORK-002, 0014790)** — §5 확정: 노드 자격 = frontmatter `type` 보유, type 없는 navigational 은 노드 아님. probe L2 154→34.
- ~~(OPEN, WORK-002) L5 orphan 적용 범위 — daily/학습노트 제외 여부.~~ **해소(WORK-002, 0014790)** — §5 확정: orphan 대상 = 지식 노드(reference/permanent/post/product)만. probe L5 196→0.
- ~~(메모, WORK-005) **L5 orphan baseline은 변동값** — WORK-005 reference 재타이핑 후 측정 156(미인용 자료노트, report-only WARN). 강제 해소 대상 아님 — 연결은 사람 정제(S3).~~ **성격 전환(v0.0.5)** — 이 156건은 이제 WARN이 아니라 **`source` 층 미소화 큐 지표**다([[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] D5). 위반 목록에서 빠지고 별도 집계로 나가며, 승인 파이프라인의 입력 후보가 된다. **여전히 특정 숫자를 계약으로 고정하지 않는다.**
- **(OPEN, v0.0.5)** L2 type별 필수 필드와 L4 방향 반전을 기존 데이터에 적용했을 때의 위반 수 — 미측정이다. `permanent`는 라이브 1건뿐이라 `up` 필수의 영향이 작을 것으로 보이나, L4 반전은 기존 `up:` 사용처(라이브 lineage 1건)를 재검토해야 한다. report-only로 먼저 측정한 뒤 enforce로 넘긴다.
- **(OPEN, v0.0.5)** 발행 전 검증의 "가상 그래프 조립" 비용 — 발행마다 전체 그래프를 다시 조립할지, 변경분만 증분 검증할지. 현재 노드 406 규모에서는 전체 재조립도 감당 가능해 보이나 실측이 필요하다. 구현 방식은 Apply Executor spec / work 소관.
- ~~(OPEN, WORK-004~006 또는 별도) **L2=34 아카이브 사본 id 충돌** — `v1_0_1-X`(version-cutoff 동결 사본)가 live `X`와 같은 frontmatter `id`를 공유해 alias/id 전역유일(L2) 위반.~~ **해소(WORK 후속, 6f823e4)** — Option 2(검증기가 `archived` 노드를 id/alias 유일성 검사에서 면제) 채택. `build_alias_index`가 archived는 stem만 등록(frontmatter id/aliases 미등록) → §5 규칙으로 명문화. **L2 34→0**(ERROR 합계 0, L1/L2/L3/L4=0), L5=156 불변, 266 passed. 아카이브 노드 34·엣지 81 생존. WORK-007 enforcement 프리req 충족.
