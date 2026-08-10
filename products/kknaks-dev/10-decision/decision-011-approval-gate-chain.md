---
type: decision
id: KDEV-DEC-011
title: "승인 게이트 체인 — 소스별 가변 스테이지와 큐 모델"
status: accepted
product: kknaks-dev
created_at: 2026-07-27
updated_at: 2026-07-27
tags:
  - product/kknaks-dev
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
  decisions:
    - "[[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]"
    - "[[decision-005-classification-workflow|KDEV-DEC-005]]"
    - "[[decision-009-app-db-foundation-and-admin-auth|KDEV-DEC-009]]"
  specs:
    - "[[spec-003-knowledge-workflow|KDEV-SPEC-003]]"
  works:
    - "[[work-014-queue-and-route-gate|KDEV-WORK-014]]"
    - "[[work-015-youtube-chain-and-executor|KDEV-WORK-015]]"
  releases: []
  related: []
up:
  - human-in-the-loop
  - workflow-orchestration
  - queue
---

# 승인 게이트 체인 — 소스별 가변 스테이지와 큐 모델 (ADR-011)

AI가 만든 결과물을 바로 커밋하지 않고, **DB 승인 큐 → 스테이지별 게이트 → 발행** 순서로 태운다. 게이트 수는 고정이 아니라 **소스 종류와 첫 게이트의 판단이 파이프라인 길이를 결정**한다.

> 목적지 taxonomy는 [[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]이 소유한다. 이 결정은 그 목적지로 **어떻게 도달하는가**(큐·게이트·상태기계)를 다룬다. 저장·발행 경계(draft=DB/확정=md, 커밋 단위, push 실패)는 후속 decision이 소유한다.

## Context

- 관련 baseline: [[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]
- 지금 AI 결과물이 사람 검토 없이 `origin/main`에 커밋되는 경로가 4개다(잔디·algorithm·content_enrich·Slack 지식캡처). 개입 지점이 0이고, 피드백은 파일 덮어쓰기라 직전 버전이 사라진다.
- `inbox/README.md`가 규정한 *"주기적으로 리뷰해 종착지로 분류"* 단계가 코드에 없다. 승인 게이트는 새 개념이 아니라 **이미 문서로만 존재하는 계약을 채우는 일**이다.
- [[decision-009-app-db-foundation-and-admin-auth|KDEV-DEC-009]] D1이 "운영 데이터는 DB, 지식그래프는 파일 SoT"로 경계를 그었다. 승인 큐·게이트·리비전은 명백히 운영 데이터다.
- 참조: `ax-knowledge-graph`의 AXKG-DEC-001(2-게이트), AXKG-SPEC-001/002/003/004. 게이트 버전·피드백·resume 규칙은 검증된 계약이 있다.

### 소스마다 산출물이 다르다

owner가 그린 전체 그림(2026-07-27):

| 입력 | 산출물 |
|---|---|
| 유튜브 | **reference + concept** + contents(파생) |
| 커밋(잔디) | **reference** + project + spec(있으면) |
| 블로그 | **reference + concept** + posts(파생, 게시 판정 시) |
| 스케줄 | `persona/career/` 업데이트 |

→ **`reference` + `concept`가 공통 코어이고 소스별 파생물이 하나씩 붙는다.** 파이프라인을 소스마다 새로 짤 필요가 없다.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[human-in-the-loop]] — AI 산출물을 **바로 커밋하지 않고 게이트에서 멈춰 사람을 기다린다.** 자동 스테이지와 게이트 스테이지를 나눈 것이 「어디까지 자동인가」의 눈금이다
- [[workflow-orchestration]] — 게이트를 고정 enum 이 아니라 **파이프라인 정의(스테이지 목록)** 로 표현한 것. 소스 종류가 체인 길이를 정하고, 각 스테이지가 멈춤·관측의 단위가 된다
- [[queue]] — 승인 큐를 **DB 에** 두고 작업트리에 파일을 만들지 않는다 — 대기하는 일감을 어디에 쌓느냐가 이 결정의 첫 항목이다

## Options

### 게이트 수

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| 1-게이트 | 초안 → 승인 → 발행 | 마찰 최소 | 목적지·개념매칭·본문을 한 번에 봐야 해 검토가 부실해진다 | 기각 |
| ax 2-게이트 고정 | 분류 + 문서화 | ax와 동형 | 우리는 산출물이 2~3장이라 문서화 게이트 하나에 다 묶이면 개념 판단이 묻힌다 | 기각 |
| **소스별 가변 스테이지 체인** | 파이프라인 정의가 데이터 | 소스가 늘어도 정의만 추가, 산출물마다 전용 검토 | 상태기계가 (item, stage) 2축 | **채택** |

### 첫 게이트가 정하는 범위

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | 목적지·group·개념매칭·파생여부 전부 | 승인 1회로 계획 확정 | **내용을 보기 전에 개념 매칭을 정해야 한다** — 근거 없이 찍게 됨 | 기각 |
| B | 목적지만 | 판단 시점 최적 | group은 미룰 이유가 없는데 승인만 늘어남 | 기각 |
| **C** | 목적지 + group + 파생 on/off | "어디에 둘까"를 한 덩어리로 결정, 파생 on/off가 체인 길이를 확정 | 개념 판단은 뒤로 | **채택** |

### 역방향 전이

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| a | 되돌리기 없음, 취소 후 재투입 | 상태기계 단순 | group 하나 틀려도 수집·요약부터 다시 | 기각 |
| b | 바로 앞 게이트로 한 칸 | 부분 수정 가능 | **정작 틀리는 건 목적지(G1)인데 거기까지 못 간다** | 기각 |
| **c** | 첫 게이트(경로)까지 재오픈 | 실제 오판 지점을 고칠 수 있고 수집·요약은 재사용 | 뒤 게이트 정리 규칙 필요 | **채택** (ax와 동일) |

### `inbox/` 디렉토리

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| a | 폐지, DB 큐가 완전 대체 | 겹침 없음 | 옵시디언에서 안 보임, "일단 남기고 싶은 것"의 자리 소멸 | 기각 |
| **b** | **보류함으로 격하** — 승인된 idea만 | 옵시디언 가시성 유지, 루트 3층 보존, 기존 4개 유효 | "승인 대기(DB)"와 "보류(폴더)" 구분 필요 | **채택** |
| c | 공존 (수동=파일, Slack=DB) | 손으로 던지는 경로 유지 | 수동분은 게이트를 안 타 결국 안 정리됨 — 현재 문제 반복 | 기각 |

## Decision

### D1. 큐와 `inbox/` 디렉토리를 분리한다

- **승인 큐는 DB에 둔다.** 들어온 입력은 큐 항목(item)으로 적재되고, 승인 전에는 레포에 파일이 생기지 않는다. 미커밋 md는 `reload.py:77`의 `git reset --hard origin/main`에 사라지므로 작업트리에 둘 수 없다.
- **`inbox/` 디렉토리는 "보류함"으로 역할을 바꾼다.** 경로 게이트에서 *"지금은 정제 못 하겠지만 버리긴 아깝다"*로 승인된 idea만 들어간다. 즉 `inbox/`도 **하나의 목적지**이지 대기열이 아니다.
- `inbox/README.md`의 *"inbox는 항상 미분류만 보유"*를 **"미정제만 보유"**로 개정한다. 기존 4개 파일은 그대로 유효하다.
- [[decision-005-classification-workflow|KDEV-DEC-005]]·[[spec-003-knowledge-workflow|KDEV-SPEC-003]]의 "리뷰해 분류하고 원본 idea 폐기" 흐름은 폐기하지 않고 **이 게이트 체인이 그 구현체**가 된다.

### D2. 게이트 체인 = 소스별 파이프라인 정의

- 게이트는 고정 enum이 아니라 **파이프라인 정의(스테이지 목록)** 로 표현한다. ax가 `gate_kind`를 `classification`/`documentation` 2개로 고정한 것과 달리, 여기서는 `(item, stage)` 2축이며 스테이지 목록이 소스 종류마다 다르다.
- 스테이지는 두 종류다.
  - **자동 스테이지** — 승인 대상이 아니다. 수집(yt-dlp·자막·본문 fetch), 요약 등. 실패 시 재시도 대상.
  - **게이트 스테이지** — 사람이 승인/피드백한다.
- 소스가 늘어도 코드에 enum을 추가하지 않고 **파이프라인 정의를 하나 등록**한다.
- 모든 파이프라인은 **공통 코어(`reference` + `concept`)** 를 공유하고 **파생 슬롯**만 다르다.

| 소스 | 파생 슬롯 | 이번 범위 |
|---|---|---|
| 유튜브 | `persona/contents/` (교안) | ✅ 첫 구현 |
| 커밋(잔디) | `products/{제품}/` (project·spec) | 후속 |
| 블로그 | `persona/posts/` (게시 판정 시) | 후속 — posts 배선이 선행([[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] 보류) |
| 스케줄 | `persona/career/` | 후속 |

### D3. 유튜브 파이프라인 정의 (첫 구현)

```text
큐 항목 (유튜브 URL)
   │
   ├─[자동] collect     yt-dlp 메타 + 자막
   ├─[자동] summarize   판단 근거용 요약
   │
   ├─[게이트] route      목적지 + reference group + 파생 on/off
   │                     → 여기서 체인 길이가 확정된다
   ├─[게이트] source_note reference 초안 ("이 영상이 뭐라고 했나")
   ├─[게이트] concept    개념 추출 + 신규 생성 / 기존 보충 판정
   ├─[게이트] derived    교안 — route에서 on일 때만 존재
   │
   └─ 마지막 게이트 승인 → apply (md 여러 장 발행)
```

- **`route` 게이트가 정하는 것**: 목적지 조합(reference·concept·contents·inbox 보류·폐기), `reference` group(13종 중 1), 파생 산출물 on/off.
- **`concept` 게이트가 정하는 것**: 이 자료에서 나오는 개념 목록, 각각에 대해 **신규 생성 vs 기존 concept 보충**. 개념 매칭은 내용을 뽑아본 뒤라야 근거가 생기므로 `route`로 당기지 않는다.
- `route`에서 목적지가 "폐기"면 이후 스테이지 없이 종료한다. "inbox 보류"면 idea 1장만 발행하고 종료한다.
- 자동 스테이지(collect·summarize)는 게이트가 아니다. 실패하면 재시도하며, 재시도는 기존 실행 기록을 덮어쓰지 않는다.

### D4. 게이트 공통 계약 — AXKG-SPEC-002 재사용

게이트 하나하나의 동작은 ax의 검증된 계약을 그대로 가져온다.

- 게이트는 **컨테이너**이고, 사람이 승인·피드백하는 대상은 그 안의 **현재 active revision**이다.
- **피드백 → 새 버전(v2) 생성.** 직전 버전(v1)은 수정하지 않고 read-only로 보존하며, v2는 v1을 `parent`로 참조한다. 되돌리기든 재생성이든 **기록을 지우지 않는다.**
- 재생성은 open-kknaks **세션 resume**으로 이어서 실행한다(원문·지침 재전송 없이 피드백만 반영). resume 원천이 없으면 stateless로 실행하되 이전 payload와 피드백을 컨텍스트에 포함한다. 지식캡처가 이미 쓰는 배선(`runner.py:76`)을 확장한다.
- 새 revision이 검토 가능 상태가 되기 직전, **같은 게이트의 다른 검토 가능 revision을 전부 밀어냄(superseded) 처리**한다 — 게이트당 검토 대상은 항상 하나다.
- 승인된 revision은 불변이며, 한 게이트에 승인 revision은 하나만 존재한다.
- AI 실행 상태(`queued`/`running`/`succeeded`/`failed`)는 게이트 상태와 섞지 않고 별도로 관리한다. 실패한 실행 기록은 보존하고 재시도는 새 실행으로 만든다.

### D5. 역방향 전이는 경로 게이트 재오픈 하나뿐

- 뒤 스테이지에서 **"이 목적지가 아님"** 피드백을 넣으면 `route` 게이트가 재오픈된다. 이것이 **유일한 역방향 전이**다.
- 재오픈 시: 기존 승인 revision을 밀어냄 처리하고 승인 포인터를 해제하며, 뒤에 있던 게이트 스테이지는 무효 처리한다. **revision 내용 자체는 불변으로 남긴다.**
- 자동 스테이지(collect·summarize) 결과는 재사용한다 — 목적지 오판 때문에 자막을 다시 받을 이유가 없다.
- 새 목적지가 승인되면 그에 맞는 스테이지 체인을 새로 생성한다. 파생 on/off가 바뀌면 체인 길이도 바뀐다.
- 그 외 임의의 되감기·건너뛰기는 없다.

### D6. 발행은 마지막 게이트 승인에서 한 번에

- 체인의 **마지막 게이트 승인이 발행(apply) 트리거**다. 중간 게이트 승인은 다음 스테이지를 여는 것이지 파일을 만들지 않는다.
- 따라서 유튜브 하나에서 나오는 `reference` + `concept`(신규/보충) + `contents`가 **한 번에** 발행된다.
- 커밋 단위·push 실패 처리·apply 검증 규칙은 후속 decision(저장·발행 경계)이 소유한다. 이 결정은 "언제 트리거되는가"까지만 정한다.

### 기각

- 1-게이트, ax 2-게이트 고정.
- 첫 게이트에서 개념 매칭까지 정하는 안(A), 목적지만 정하는 안(B).
- 역방향 전이 없음(a), 한 칸 되돌리기(b).
- `inbox/` 폐지(a), 공존(c).
- 게이트별 즉시 발행(중간 승인마다 커밋).

### 보류

- 게이트 UI 배치(인라인 세로 스택 vs 스테이지별 화면 분리) — spec의 UX Contract로 넘긴다.
- 대량 승인(bulk approve) — ax도 후속으로 미뤘다. 큐가 쌓이는 속도를 보고 판단한다.
- 커밋·블로그·스케줄 파이프라인 정의 — 유튜브 체인이 실제로 돈 뒤 같은 틀로 추가한다.

## Rationale

- **판단 기준**: 판단에 필요한 정보가 갖춰진 시점에 그 판단을 하는가, 소스가 늘 때 코드가 아니라 정의가 늘어나는가, 틀렸을 때 되돌릴 수 있는가.
- **가변 스테이지인 이유**: owner의 그림에서 소스 4종의 산출물이 전부 다르다. 고정 enum으로 가면 소스마다 게이트 종류를 추가해야 하고, 공통 코어(reference+concept)가 중복 구현된다. 파이프라인 정의를 데이터로 두면 파생 슬롯만 갈아끼우면 된다.
- **C안인 이유**: "이건 k8s 자료다", "이건 블로그에 올릴 만하다"는 요약 시점에 판단 가능하지만, "이 영상에 STT 말고 VAD도 나오나"는 개념을 뽑아봐야 안다. 두 판단을 한 게이트에 묶으면 뒤쪽이 근거 없는 추측이 된다. 반대로 파생 on/off는 **체인 길이를 결정**하므로 첫 게이트에 있어야 한다.
- **c안인 이유**: 실제로 틀리는 건 거의 항상 목적지다. 그런데 (b)는 그 지점까지 못 가고 (a)는 자막 수집부터 다시 돈다. ax도 같은 결론에 도달해 이 전이 하나만 예외로 열어뒀다.
- **`inbox/` 보류함인 이유**: 노트북에서 옵시디언을 열었을 때 "이런 것도 있었지"가 보여야 한다. 폐지하면 관리자 웹에 들어가야만 볼 수 있다.
- **리스크**:
  - 유튜브 하나에 승인이 3~4번이다. 마찰이 실측으로 크면 게이트 병합이나 자동 승인 규칙을 후속으로 검토한다. ax는 인라인 세로 스택으로 화면 이동을 없애 완화했다.
  - `(item, stage)` 2축은 ax의 고정 enum보다 상태기계가 복잡하다. 첫 파이프라인을 유튜브 하나로 좁혀 검증한 뒤 확장한다.
  - 자동 스테이지 실패(자막 없음, 수집 차단)가 큐를 막을 수 있다. 재시도와 수동 메모 보완 경로가 필요하다(ax의 User Note Fallback 참고).

## Scope

- In: 큐 모델과 `inbox/` 역할 재정의, 게이트 체인 구조(자동/게이트 스테이지), 경로 게이트 범위, 게이트 공통 계약(버전·피드백·resume·sweep), 역방향 전이, 발행 트리거 시점, 유튜브 파이프라인 정의.
- Out:
  - 저장·발행 경계 상세(커밋 단위, push 실패, apply 검증) → 후속 decision
  - 프로세스 경계(Slack bridge 흡수) → 후속 decision
  - 게이트 UI 배치 → spec
  - 커밋·블로그·스케줄 파이프라인 정의
  - 기존 잔디·algorithm 잡의 게이트 편입 시점
- 영향을 받는 spec 후보: [[spec-003-knowledge-workflow|KDEV-SPEC-003]](분류 흐름의 구현체가 게이트 체인으로 확정), 신규 — 승인 큐 spec, 게이트 체인 spec, 게이트 피드백·재생성 spec.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | 자동 스테이지가 실패했을 때(자막 없음·수집 차단) 큐 항목을 어떻게 살릴지 — 수동 메모로 대체 입력을 주는 경로가 필요한가 | kknaks | 큐 spec |
| OQ-2 | `route` 게이트가 목적지를 조합으로 제시하는지(reference O·concept O·contents X) 단일 선택으로 제시하는지 | kknaks | 게이트 체인 spec |
| OQ-3 | concept 게이트에서 개념 N개가 나올 때, 개별 승인인지 묶음 승인인지 | kknaks | 게이트 체인 spec |
| OQ-4 | 승인 3~4회의 실제 마찰 — 실측 후 병합·자동승인 검토 필요 여부 | kknaks | 유튜브 체인 첫 실전 후 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| 승인 큐 spec | create | 큐 항목 intake·상태기계·`inbox/` 보류함 경계 |
| 게이트 체인 spec | create | 파이프라인 정의·스테이지 계약·유튜브 체인·역방향 전이 |
| 게이트 피드백·재생성 spec | create | revision 버전·피드백·session resume·sweep |
| [[spec-003-knowledge-workflow|KDEV-SPEC-003]] | update | 분류·정제 흐름의 구현체를 게이트 체인으로 명시, `inbox/` 역할 개정 |
