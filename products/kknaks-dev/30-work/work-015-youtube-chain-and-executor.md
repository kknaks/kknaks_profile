---
type: work
id: KDEV-WORK-015
title: "유튜브 체인 완성 + Apply Executor"
status: doing
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
progress: 20
created_at: 2026-07-27
updated_at: 2026-07-28
tags:
  - product/kknaks-dev
  - doc/work
  - status/doing
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
- External dependency: open-kknaks, GitHub push 권한(기존 `GH_TOKEN_PERSONAL`), **레포 읽기 가능한 worker 실행 환경** — 에이전트가 `rules/`·`templates/` 를 직접 읽어야 한다(WORK-013 산출물)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | doing |
| Progress | 20% (Phase 1/5) |
| Branch/PR | — |
| Blocker | 없음 (WORK-014 done) |
| Next | Phase 2 concept 게이트 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 완주 기준 판단 | todo |
| Design | kknaks | 게이트 스택·diff 표시 | todo |
| FE | kknaks | 게이트 3종 UI | todo |
| BE | kknaks | 스테이지 생성·Executor | doing (체인·source_note done) |
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
| `templates/knowledge/*.md` | **형식의 SoT** — 에이전트가 `agent.md` 라우팅으로 찾아 읽는다 (주입 아님) |
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

- **Status**: DONE
- **작업**:
  - [x] route 승인 후 `source_note` 게이트 자동 생성
  - [x] 스테이지 프롬프트는 **"무엇을 만들라"만** 지시한다 — 형식은 에이전트가 `rules/knowledge-note-pipeline.md` + `templates/knowledge/reference.md` 를 읽어 따른다
  - [x] reference 초안 생성 (준비 산출물 + route 결과 입력)
  - [x] ~~초안이 `up:`을 채우도록~~ → **계획 오류. 아래 참조.** 본문 `[[]]`↔`up:` 정합 검사는 공통부에 구현(concept 스테이지가 쓴다)
  - [x] 게이트 카드 UI (전문 미리보기 + 저장될 경로)
- **검증**:
  - [x] route 승인 시 다음 게이트가 열린다
  - [x] 초안 형식이 템플릿과 일치한다 (섹션 구성·frontmatter 필드)
  - [x] ~~초안에 `up:`이 채워진다~~ → **요구 자체가 틀렸다. 아래 참조.**
  - [x] 승인해도 **아직 파일이 생기지 않는다**
- **완료 증거**:

신규 `service/pipeline/chain.py`, `stages/{common,source_note}.py`, `runtime` 생성기 레지스트리, 게이트 카드 노트 미리보기. 테스트 37건 신규. **502 passed.**

> **계획 오류 정정 — reference 에는 `up:` 이 없다.**
>
> 이 Phase 의 원 계획은 *"초안에 `up:`이 채워진다 (lineage 생성 의무 충족)"* 였는데 **틀렸다.** 4층 모델에서 `reference` 는 **출처 기록층이라 상류가 없다** — `templates/knowledge/reference.md` 도 "`up:` 을 두지 않는다"고 명시한다. 반대로 **concept 가 reference 를 `up:` 으로 가리킨다.**
>
> 그래서 lineage 생성 의무(DEC-010 D4)가 실제로 발현되는 곳은 **Phase 2(concept)** 다. Phase 1 프롬프트는 "frontmatter 에 `up:` 을 두지 않는다"고 반대로 지시한다. `up:`↔본문 링크 정합 검사(`require_up_in_body`)는 공통부에 만들어 뒀고 concept 스테이지가 소비한다.

**체인 길이는 정의만으로 정해지지 않는다.** `next_stage(source_kind, route_payload, after=...)` 가 파이프라인 정의 **순서**와 route 결과 **on/off** 를 함께 본다. 개념을 끄면 `source_note` 다음이 `derived` 가 된다 — 중간이 비어도 건너뛴다. `None` 은 "발행 차례"라는 뜻이다.

**`exclusive`(보류·폐기)면 게이트가 하나도 안 열린다.** 만들 것이 없으니 검토할 것도 없다.

**생성기가 없으면 게이트를 열지 않는다.** 승인할 수 없는 카드를 화면에 남기면 사람이 막힌다. 로그만 남기고 항목은 검토 대기에 머문다.

**형식 SoT 충돌을 여기서 정리했다** — 종전 캡처는 `AI → JSON → render.py → md` 였고, `render.py` 의 하드코딩된 섹션 구성이 `templates/knowledge/` 와 나란히 **두 번째 형식 SoT** 였다. 이제 스테이지는 **AI 가 md 전문을 직접** 내고(SPEC-010), 형식은 레포 템플릿 한 곳이 소유한다. `render.py` 는 롤백 경로(`KnowledgeCaptureRunner`)에만 남는다.

**경로는 AI 가 정하지 않는다.** AI 는 `filename_stem` 만 내고 디렉토리는 시스템이 층·목적지에서 조립한다. `stem` 에 `/` 나 `.md` 가 섞이면 거부한다 — 경로를 지어내면 allowlist 밖으로 쓰는 계획이 만들어진다.

**게이트 시점 검사는 가볍게** — stem 규약, frontmatter 파싱, `type` 일치, 필수 필드, `id`=stem. 전체 그래프 검증(L1~L6)은 발행 직전에 가상 그래프로 돈다(Phase 4). 이 시점에는 형제 노트가 아직 없어 링크가 깨져 보이기 때문이다.

부수 — **테스트가 규칙 위반을 잡았다**: `CONCEPT_STEM_RE` 가 `2026-07-28-concept` 를 통과시켰다. "concept 는 날짜를 붙이지 않는다"(개념은 특정 시점에 묶이지 않는다)가 정규식에 반영돼 있지 않았다. 선행 부정으로 날짜 머리만 막고 숫자 자체(`gpt-4`·`http2`)는 허용하도록 고쳤다.

**화면**: 노트 스테이지 카드는 **저장될 경로 + 전문**을 보여준다(24줄 넘으면 접힘). 경로를 감추면 "어디에 생기는지 모른 채 승인"하게 된다.

### Phase 2 — concept 게이트

- **Status**: TODO
- **설명**: 이 work의 난이도 핵심. 개념 추출보다 **기존 개념 매칭**이 어렵다.
- **작업**:
  - [ ] 개념 추출 스테이지
  - [ ] concept 스테이지도 동일 — 프롬프트는 지시만, 형식은 레포에서 읽는다
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

> **형식 규칙을 프롬프트에 복사하지 않는다.** 복사하면 SoT 가 둘(레포 문서 + 프롬프트)이 되고, 규칙이 바뀔 때 한쪽만 고쳐져 조용히 어긋난다. 에이전트는 레포를 읽을 수 있으므로 `agent.md` 라우팅으로 찾아가게 한다. 다만 **찾아가지 않으면 형식이 표류**하므로, 스테이지 프롬프트에 "작성 전 `rules/knowledge-note-pipeline.md` 를 읽으라"는 지시는 반드시 넣는다.

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

- **교안 경로는 공존으로 정했다 (owner 결정, P1).** `derived` 게이트 산출물은 `status: pending` 을 쓰지 않아 `content_enrich` 의 스캔 대상이 되지 않는다. 손으로 `C-NNN-pending.md` 를 만드는 기존 방식도 그대로 살아 있다. 새 경로를 써 보고 옛 경로를 접을지는 나중에 판단한다.
- **concept 매칭 정확도가 이 파이프라인의 실질 품질을 결정한다.** 매칭이 틀리면 개념이 갈라지거나(놓침) 엉뚱한 노트를 덮어쓴다(오매칭). Phase 2에서 오매칭 쪽을 더 보수적으로 잡을지(의심되면 신규 생성) 판단이 필요하다.
- AI가 신규/보충을 틀렸을 때 owner가 게이트에서 직접 "기존 X에 합쳐라"로 바꿀 수 있어야 하는지 — 지금 계약은 피드백 재생성뿐이다(SPEC-008 §7).
- 발행 커밋 메시지 형식(DEC-012 OQ-1), 실패 알림 임계(DEC-012 OQ-4)를 이 work에서 정한다.
- 가상 그래프 검증을 전체 재조립으로 할지 증분으로 할지(SPEC-010 §7) — 406노드 기준 실측 후 결정.

## Related

- SPEC: frontmatter `links.specs` 참조
- Work: 선행 WORK-014
