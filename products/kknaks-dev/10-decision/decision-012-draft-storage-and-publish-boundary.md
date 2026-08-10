---
type: decision
id: KDEV-DEC-012
title: "저장·발행 경계 — draft는 DB, 확정은 md, 발행은 원자적"
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
    - "[[decision-011-approval-gate-chain|KDEV-DEC-011]]"
    - "[[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]"
    - "[[decision-009-app-db-foundation-and-admin-auth|KDEV-DEC-009]]"
    - "[[decision-006-validation-gates|KDEV-DEC-006]]"
  specs:
    - "[[spec-004-graph-validation|KDEV-SPEC-004]]"
  works:
    - "[[work-015-youtube-chain-and-executor|KDEV-WORK-015]]"
  releases: []
  related: []
up:
  - transaction
---

# 저장·발행 경계 — draft는 DB, 확정은 md, 발행은 원자적 (ADR-012)

승인 전 초안은 DB에만 두고, 승인된 것만 md 파일로 발행한다. 발행은 **전부 성공하거나 전부 되돌린다** — 반쪽 발행도, origin에 없는 커밋도 서버에 남기지 않는다.

> [[decision-011-approval-gate-chain|KDEV-DEC-011]] D6이 "마지막 게이트 승인이 발행 트리거"까지 정했다. 이 결정은 그 발행이 **무엇을 어떻게 쓰고, 실패하면 어떻게 되는가**를 다룬다.

## Context

- 관련 baseline: [[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]
- [[decision-009-app-db-foundation-and-admin-auth|KDEV-DEC-009]] D1이 이미 경계를 그었다 — **애플리케이션/운영 데이터는 DB, 지식그래프는 파일 SoT.** 승인 큐·게이트·리비전은 전자이고 발행된 노트는 후자다.
- **미커밋 md를 작업트리에 둘 수 없다.** `reload.py:77`의 `_git_pull_rebase()`가 `git fetch origin main` + `git reset --hard origin/main`이다. GitHub webhook이 한 번 오면 커밋되지 않은 변경이 사라진다. 이것이 초안을 DB에 두어야 하는 강제 조건이다.
- **커밋됐지만 push되지 않은 것도 같은 위험에 놓인다.** 같은 `reset --hard`가 origin에 없는 로컬 커밋을 지운다. 현재 `commit_and_push_with_retry`는 3회 재시도 후 `False`를 반환하고 호출자는 로그만 남긴다(`git_push.py:134`, `content_enrich.py:376` 등) — **승인분이 조용히 소실될 수 있는 경로가 열려 있다.**
- 현재 잡들은 **파일당 1커밋**이다(`content_enrich.py:376`은 enrich 실패분까지 `status: error`로 커밋한다).
- owner 요구(BL-003 Raw): *"최종 승인이 나면 업데이트하면서 push해야 로컬 노트북에서도 받아볼 수 있다."* 발행 = 로컬 옵시디언 볼트에 도달하는 것.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[transaction]] — **전부 성공하거나 전부 되돌린다** — 반쪽 발행도, origin 에 없는 커밋도 남기지 않는다는 원자성 요구가 이 결정의 뼈대다

## Options

### 수정(보충) 반영 방식

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| 부분 패치 | diff/patch를 적용 | 변경 최소 | 적용 실패 시 파일이 깨진다. 컨텍스트가 어긋나면 조용히 오적용 | 기각 |
| **전문 교체 + 승인 화면 diff** | AI가 수정 전문을 내고 executor가 덮어쓰되, 승인 화면에 변경분을 보여준다 | 적용이 결정적, 모든 변경이 승인 전에 보인다 | 매번 diff를 확인해야 한다 | **채택** |
| 보호 섹션 | `## 내 메모`를 AI 금지 구역으로 | 대충 승인해도 안전 | 규칙을 프롬프트·검증 양쪽에 이중 유지, 섹션 밖 수정은 여전히 소실 | 기각 (후속 여지) |

### push 실패 처리

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| 현행 | 로그만 남기고 종료 | — | **승인분이 조용히 소실**된다 | 기각 |
| a | 커밋 유지 + 재푸시 CTA | 쓴 파일을 살린다 | origin에 없는 커밋이 남는 동안 `reset --hard`가 지울 수 있어 예외 처리를 또 만들어야 한다 | 기각 |
| **b** | **전량 롤백 + `발행 실패` 상태 + 재시도** | 초안이 DB에 있으므로 잃는 게 없다. 서버에 origin 밖 커밋이 절대 안 남는다 | 재시도 시 파일 쓰기부터 다시 (비용 ≈ 0) | **채택** |

## Decision

### D1. 저장 이원화

| 데이터 | SoT | 비고 |
|---|---|---|
| 큐 항목, 게이트, revision, 피드백, AI 실행 이력, 발행 결과 | **PostgreSQL** | 운영 상태 ([[decision-009-app-db-foundation-and-admin-auth|KDEV-DEC-009]] D1) |
| 승인 전 초안(payload) | **PostgreSQL** (박제) | 승인 전에는 레포에 파일이 생기지 않는다 |
| 발행된 노트 본문 | **Markdown 파일** | 지식그래프 SoT. 옵시디언·git·검증기가 같은 파일을 본다 |
| 그래프 엣지 | **Markdown** (`[[]]` / `up:`) | [[decision-004-edge-model-and-schema|KDEV-DEC-004]] 유지 |

- 초안은 **덮어쓰지 않고 버전으로 쌓는다**(v1 read-only + v2 박제, [[decision-011-approval-gate-chain|KDEV-DEC-011]] D4). 어떤 피드백이 무엇을 바꿨는지 추적 가능해야 한다.
- 승인 전 초안은 옵시디언에서 보이지 않는다. 검토 표면은 admin 화면이다.

### D2. AI는 파일과 DB를 직접 건드리지 않는다

- AI 스테이지의 출력은 **발행 계획(apply plan)** 이다 — "어느 경로에 어떤 전문을 쓸지"의 목록. AI가 파일을 쓰거나 DB를 갱신하거나 git을 호출하지 않는다.
- **Apply Executor**가 검증을 통과한 계획만 실행한다. 이것이 안전 경계의 핵심이며, 현재 Slack 캡처가 AI 결과를 곧바로 `atomic_write` + push하는 구조(`runner.py:112-114`)를 대체한다.
- 계획의 파일 액션은 **신규 생성**과 **전문 교체** 두 가지뿐이다. 부분 패치 액션은 두지 않는다.

### D3. 발행 단위 = 승인 1회 = 커밋 1개 (원자적)

- 마지막 게이트 승인 한 번이 **커밋 하나**를 만든다. 유튜브 하나에서 나오는 `reference` + `concept`(신규 또는 보충) + `contents`가 한 커밋에 들어간다.
- 현재의 파일당 1커밋 방식(`content_enrich.py:376`)을 대체한다. 노트북에서 pull하면 **완성된 세트가 한 번에** 온다.
- 한 발행 안에서 **신규 생성과 기존 파일 교체가 섞일 수 있다**(concept 보충이 그렇다). 그래도 한 커밋이다.

### D4. 수정은 전문 교체, 변경분은 승인 화면에서 보여준다

- 기존 문서 보충은 부분 패치가 아니라 **수정 전문 교체**로 적용한다. 패치 적용은 컨텍스트가 어긋나면 실패하거나 조용히 오적용되는데, 발행은 되돌리기 어려운 동작이라 결정적이어야 한다.
- 대신 **승인 화면에 기존 파일 대비 변경분(diff)을 표시**한다. 사람이 손으로 쓴 문장이 사라지는 변경도 승인 전에 눈에 보여야 한다. diff는 **표시용**이며 적용 입력이 아니다.
- 4층 모델상 `concept`는 *"이 개념은 무엇인가"* = 사실의 SoT라 AI가 관리하는 영역이고, *"우리 회사에선 이렇게 쓴다"* 류의 판단은 `permanent/` 종합 노트가 소유한다([[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] D2 SoT 위임). 보호 섹션 없이 diff만 두는 근거다.
- 보호 섹션(`## 내 메모` AI 금지 구역)은 **보류**한다. 실제로 손 수정이 자주 지워지는 게 관찰되면 도입한다.

### D5. 실패하면 전부 되돌린다

발행은 `파일 쓰기 → commit → push → reload` 순서이며, **어느 단계에서 실패해도 전량 롤백**한다.

- 파일 여러 장 중 하나라도 쓰기에 실패하면 이미 쓴 것을 되돌린다. **반쪽 발행을 남기지 않는다.**
- **push가 실패하면 커밋도 되돌려 서버를 origin 상태로 복구한다.** origin에 없는 커밋을 작업트리에 남기지 않는다 — 남기면 다음 webhook의 `reset --hard`가 언제 지울지 모르는 상태가 된다.
- 게이트는 **승인된 채로 `발행 실패` 상태**가 되고, admin에 실패 사유와 **재시도** 액션이 노출된다. 재시도는 파일 쓰기부터 다시 수행한다.
- **AI를 다시 부르지 않는다.** 초안이 DB에 박제돼 있으므로 재발행 비용은 사실상 0이다. 이것이 "붙들지 말고 되돌린다"를 선택할 수 있는 이유다.
- 발행 결과(성공/실패, 사유, 커밋 해시)는 DB에 기록한다. 조용히 실패하는 경로를 남기지 않는다.
- `reload`는 발행 성공 이후 단계다. reload가 거부돼도(그래프 검증 실패) 커밋·push는 이미 유효하므로 롤백하지 않고 경고로 노출한다 — 현재 `reload_data()`가 실패 시 구 데이터를 유지하며 `False`를 반환하는 동작(WORK-007)을 그대로 쓴다.

### D6. Apply Executor 검증

계획은 아래를 **모두** 통과해야 실행된다. 하나라도 위반하면 발행 전체를 거부한다(부분 적용 없음).

| 검증 | 내용 | 근거 |
|---|---|---|
| 경로 allowlist | 목적지 디렉토리 밖 경로 거부. 레포 루트 이탈 거부 | 4층 목적지 ([[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] D1) |
| 층-경로 정합 | `type`/`layer`가 디렉토리와 일치 | [[spec-001-directory-structure|KDEV-SPEC-001]] §5 |
| 그래프 검증 | L1 dead link · L2 스키마/유일성 · L3 오버레이 · L4 방향 · L6 archive 참조 | [[spec-004-graph-validation|KDEV-SPEC-004]], 층 기준 재정의는 [[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] D5 |
| `up:` 필수 | `concept`·`synthesis` 노트에 `up:` 누락 시 거부 | [[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] D4 생성 의무 |
| 신규 중복 | 신규 생성인데 대상 경로에 파일이 이미 있으면 거부 | 현행 `atomic_write(replace=False)` 동작 계승 |
| stale 대상 | 초안 생성 시점 이후 대상 파일이 바뀌었으면 거부하고 재생성 요구 | diff가 낡으면 승인 근거가 무효 (D4) |

거부는 실패로 기록하고 사유를 admin에 노출한다. 그래프 검증은 발행 **전**에 수행한다 — 커밋한 뒤 reload에서 걸리면 이미 origin에 나간 뒤다.

### D7. 발행 후 정정은 제품 기능이 아니다

- 발행된 노트가 틀렸으면 **옵시디언에서 직접 고치고 커밋**한다. 되돌리기 UI를 만들지 않는다.
- 파일이 SoT이고 git이 이미 이력을 갖고 있으므로 별도 버전 관리 기능이 중복된다.
- 발행 **전** 정정은 게이트 피드백으로, 발행 **후** 정정은 직접 편집으로 처리한다. 경계가 명확하다.

### 기각

- 부분 패치 적용, 보호 섹션(보류).
- push 실패 시 커밋 유지 + 재푸시(a), 현행 로그만 남기기.
- 파일당 1커밋 유지.
- 발행 후 되돌리기 UI.

## Rationale

- **판단 기준**: 승인한 것이 조용히 사라지는 경로가 없는가, 반쪽 상태가 남지 않는가, 적용이 결정적인가.
- **롤백을 택한 이유**: 초안이 DB에 박제돼 있어서 **파일은 언제든 다시 만들 수 있다**. 그러니 반쯤 발행된 상태를 붙들 이유가 없고, 붙들면 `reset --hard`와 싸우는 예외 처리를 계속 만들어야 한다. "잃을 게 없으니 깨끗하게 되돌린다"가 가장 단순한 불변식이다.
- **전문 교체인 이유**: 발행은 origin에 나가는 동작이라 되돌리기 비싸다. 패치 오적용으로 파일이 깨지는 것보다, 전문을 쓰고 diff로 검토받는 쪽이 실패 모드가 적다.
- **원자적 커밋인 이유**: 한 자료에서 나온 `reference`·`concept`·`contents`는 서로를 `[[]]`로 참조한다. 나눠 커밋하면 중간 커밋에서 dead link가 생기고, 그 상태로 pull하면 로컬 옵시디언과 검증기가 깨진 그래프를 본다.
- **리스크**:
  - 원자적 커밋은 파일 수가 늘수록 실패 시 되돌릴 게 많다. 발행 단위가 3장 내외라 관리 가능한 규모다.
  - stale 거부가 잦으면 승인이 반복 실패할 수 있다. 대상 파일이 자주 바뀌는 concept에서 관찰이 필요하다.
  - 보호 섹션 없이 diff만으로는 대충 승인 시 손 수정이 지워질 수 있다. 관찰 후 도입 여지를 남겼다.

## Scope

- In: 저장 이원화, AI 출력 = 발행 계획, Apply Executor와 검증 항목, 발행 단위(원자적 1커밋), 수정 방식(전문 교체 + diff), 실패 시 전량 롤백과 재시도, 발행 후 정정 경계.
- Out:
  - 게이트 체인·큐 상태기계 → [[decision-011-approval-gate-chain|KDEV-DEC-011]]
  - 목적지 taxonomy → [[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]
  - 프로세스 경계(Slack bridge 흡수) → 후속 decision
  - 테이블 스키마·컬럼 (spec / 40-architecture)
  - 기존 잔디·algorithm·content_enrich 잡의 발행 경로 전환 시점 (work)
- 영향을 받는 spec 후보: Apply Executor spec(신규), [[spec-004-graph-validation|KDEV-SPEC-004]](발행 전 검증 지점 추가), 40-architecture/database.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | 발행 커밋 메시지 형식 — 자료 제목 기반인지 큐 항목 id 기반인지 | kknaks | Apply Executor spec |
| OQ-2 | stale 거부가 실제로 얼마나 자주 나는지 (concept 보충이 몰릴 때) | kknaks | 유튜브 체인 첫 실전 후 |
| OQ-3 | 보호 섹션(`## 내 메모`) 도입 필요 여부 — 손 수정이 지워지는 사례 관찰 후 | kknaks | 운영 관찰 후 |
| OQ-4 | 발행 실패가 반복될 때 알림(Slack) 임계 | kknaks | Apply Executor spec |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| Apply Executor spec | create | 발행 계획 계약, 검증 항목, 원자적 커밋, 롤백·재시도, 발행 결과 기록 |
| [[spec-004-graph-validation|KDEV-SPEC-004]] | update | 발행 전 검증 지점 추가 (기존 boot·reload 게이트에 더해) |
| 40-architecture/database | update | 발행 결과·apply 기록 테이블 포함 ERD |
