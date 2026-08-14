---
type: work
id: KDEV-WORK-022
title: "스테이지 사이 세션 이어받기"
status: in_progress
product: kknaks-dev
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: —
  fe: —
  be: kknaks
  qa: kknaks
  ops: —
progress: 80
created_at: 2026-08-13
updated_at: 2026-08-13
tags:
  - product/kknaks-dev
  - doc/work
  - status/in_progress
links:
  baselines:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
  decisions:
    - "[[decision-024-stage-session-inheritance|KDEV-DEC-024]]"
  specs:
    - "[[spec-009-gate-feedback|KDEV-SPEC-009]]"
  works: []
  releases: []
  related: []
---

# 스테이지 사이 세션 이어받기

게이트가 앞 스테이지의 AI 세션을 물고 시작하게 한다. **체인 하나가 한 대화**가 된다.

**만들지 않는 것**: auto 스테이지(`summarize`) 승계, 세션 만료 감지·warm-up, 세션 저장소 자체.

## Meta

- Baseline: [[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]
- Covers spec: [[spec-009-gate-feedback|KDEV-SPEC-009]] (S-6·S-7·S-8 + §5 resume 규칙)
- Depends on work: 없음
- Parallel work: [[work-021-note-output-delimiter|KDEV-WORK-021]]
- Follow-up work: `summarize` 승계 (DEC-024 OQ-1)
- External dependency: open-kknaks 의 `resume` 옵션 — **이미 배선돼 있다**

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | in_progress |
| Progress | 80% |
| Branch/PR |  |
| Blocker |  |
| Next | P5 — 배포 후 재측정 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 승계 규칙 확정 | done |
| Design | — | 화면 없음 | — |
| FE | — | 프론트 변경 없음 | — |
| BE | kknaks | `_resume_session`·`_fail`·`retry`·`context_payload` | done |
| QA | kknaks | 승계·거부 경계 + 실전 재측정 | 경계 done · 재측정 대기 |
| Ops | — | 배포 절차 변경 없음 | — |

## Scope

포함:

- `_resume_session` 에 **앞 게이트** 단계 추가 (DEC-024 D1)
- `cancelled` 게이트 제외 — `AITask.kind` 축을 게이트 축으로 바꾼다 (D2)
- 실패한 실행의 세션 보존 + 재시도에 실패 사유 전달 (D3)
- 이어받을 때 `source_excerpt` 제외 (D5)
- 소요 재측정

제외:

- `summarize`(auto) 승계 — DEC-024 OQ-1
- 세션 만료 감지·미리 데우기 — 관측되기 전에 만들지 않는다
- 잔디 파이프라인 — 게이트가 하나라 이을 자리가 없다

## Code Surface

- Repo / module: `app/back` (백엔드 전용)

| 경로 후보 | 설명 |
|---|---|
| `service/pipeline/gates.py` | **주 변경.** `_resume_session`(151행) · `_fail` · `retry` · `GenerationInput` |
| `service/pipeline/stages/common.py` | `context_payload` — 이어받으면 `source_excerpt` 제외 |
| `service/pipeline/stages/daily.py` | 자체 payload 를 만든다 — `previous_error` 만 같은 규약으로 넣는다 |
| `service/pipeline/definitions.py` | 앞 스테이지 후보를 정의에서 읽는다 (읽기만) |
| `tests/test_pipeline_gates.py` | 승계·거부 경계 테스트 |

- Domain / schema note: **DB 변경 없음.** `AITask.session_ref` 는 이미 있고, 지금까지 실패 경로에서 안 채우던 것을 채우는 것뿐이다.

## Domain / Schema

해당 없음 — 컬럼 추가 없이 기존 컬럼의 쓰임을 넓힌다.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| `AgentStage.submit` | `GenerationInput.session_ref` | 실행기 `resume` 옵션 |
| 스테이지 전부 | `GenerationInput.retry_error` | **신설.** 직전 실패 사유 |
| `context_payload` | `request.session_ref` | 있으면 원문을 뺀다 |

## Internal Interface Contract

```python
@dataclass(frozen=True)
class GenerationInput:
    ...
    session_ref: str | None
    #: 직전 실패 사유. 재시도에서만 채워진다. 사람 피드백(`feedback`)과 섞지 않는다.
    retry_error: str | None = None

async def _resume_session(db, gate) -> str | None:
    """① 이 게이트의 버전 → ② 이 게이트의 실행 → ③ 앞 게이트(정의 역순, cancelled 제외)"""
```

payload 규약:

```python
{"source_excerpt": "...(최대 4만 자)"}   # 세션 없음 — 지금과 같다
{"resumed_session": True}                 # 세션 있음 — 원문 제외, 요약은 유지
{"previous_error": "INVALID_NOTE_OUTPUT: ..."}   # 재시도
```

## Execution

### Phase 1 — 승계 순서에 앞 게이트를 더한다

- **Status**: DONE
- **설명**: DEC-024 D1·D2 가 코드가 되는 자리.
- **작업**:
  - [x] 2단(이 게이트의 실행)을 `AITask.kind` 축에서 **이 게이트의 리비전을 통한 조회**로 바꾼다
  - [x] 3단 신설 — 파이프라인 정의의 게이트 스테이지를 역순으로 훑어 `cancelled` 가 아닌 가장 가까운 게이트의 세션
  - [x] 첫 게이트(`route`)는 앞이 없으므로 `None` → stateless. 그대로 둔다
- **검증**:
  - [x] `source_note` 가 `route` 세션을, `concept` 가 `source_note` 세션을 문다
  - [x] 앞 게이트가 세션을 안 남겼으면 그 앞을 계속 훑는다
  - [x] **가드를 깨뜨려 본다** — 3단을 지우면 승계 테스트가 실패하고, 되돌리면 통과한다
- **완료 증거**: `_gate_session(db, gate_id)` 를 떼어 내고 `_resume_session` 이 그것을 자기 게이트 → 앞 게이트 순서로 부른다.

  **`AITask.kind` 축을 버린 것이 이 phase 의 실질이다.** 그 축은 게이트가 살아 있는지를 모른다 — `(item_id, kind)` 로 찾으면 취소된 옛 게이트의 실행까지 걸린다. 이제 `GateRevision.ai_task_id` 로 조인해 **그 게이트의 실행만** 본다.

  깨뜨려 본 결과: 3단을 `return None` 으로 막으니 승계 테스트 2건이 실패했고(`assert None == 'route-2-sess'`), 되돌리니 통과했다.

### Phase 2 — 재오픈 뒤의 승계

- **Status**: DONE
- **설명**: 지금 코드의 결함(취소된 게이트 세션을 물 수 있다)을 P1 이 구조로 닫는다. 여기서는 그것을 시나리오로 고정한다.
- **작업**:
  - [x] `reopen_route` → 새 목적지 승인 → `source_note` 재개방 → `concept` 까지 한 칸 더 가는 경로의 테스트
- **검증**:
  - [x] 새 `source_note` 게이트가 **취소된 옛 게이트**의 세션을 물지 않는다
  - [x] 대신 살아 있는 route 세션을 문다
  - [x] 그다음 `concept` 도 취소된 쪽이 아니라 **산 자료 노트**의 세션을 문다
  - [x] revision 기록은 그대로 남는다(재오픈 계약 회귀)
- **완료 증거**: `test_cancelled_gate_session_is_not_resumed`. **결함이 실재했다는 것을 역검증으로 확인했다** — 2단을 종전 `AITask.kind` 축으로 되돌리자 새 게이트가 `stale-note-sess`(취소된 자료 노트의 세션)를 물었다. 즉 이 조항은 예방이 아니라 **지금 있는 버그를 닫는 것**이다.

  두 가드가 각각 다른 자리를 막는다. **2단의 게이트 조인**은 같은 스테이지의 취소된 게이트를, **3단의 `live_gate` 필터**는 앞 스테이지의 취소된 게이트를 막는다. 둘을 따로 깨뜨려 각각 테스트가 실패하는 것을 확인했다.

### Phase 3 — 실패 세션 보존과 재시도 사유

- **Status**: DONE
- **설명**: #3880 의 309초가 이 phase 의 표적이다.
- **작업**:
  - [x] `_fail` 이 `session_ref` 를 받아 저장한다 — 파싱·검증 실패 경로에서만 값이 온다
  - [x] `GenerationInput.retry_error` 신설, `retry()` 가 마지막 실패의 `error_message` 를 채운다
  - [x] `context_payload` 와 `daily` payload 에 `previous_error` 를 싣는다
- **검증**:
  - [x] 형식 실패 → 재시도가 그 세션을 물고 `previous_error` 를 받는다
  - [x] 실행 실패(timeout) → 저장된 세션이 없어 새 세션으로 간다
  - [x] **사람 피드백과 섞이지 않는다** — `feedback` 은 여전히 `None`
  - [x] 실패 기록 자체는 여전히 불변이다(SPEC-009 S-4 회귀)
- **완료 증거**: `_fail(..., session_ref=execution.session_ref)` 는 **수확의 파싱 실패 경로에서만** 값을 받는다. 실행 실패 경로는 인자를 안 주므로 자연히 `None` 이 된다 — **사유 코드 목록으로 분기하지 않는다.** 「세션이 저장돼 있는가」가 곧 그 판정이라 코드 목록을 유지보수할 자리가 생기지 않는다.

  깨뜨려 본 결과: `session_ref=` 인자를 빼자 `test_format_failure_keeps_session_and_retry_resumes_it` 이 `AITask.session_ref = None` 으로 실패했다.

  `retry_error` 를 `feedback` 과 **다른 키로 둔 이유**: 섞으면 사람이 하지 않은 말이 「사용자 지적」으로 화면에 남는다. 출처가 다른 것은 자리도 달라야 한다.

### Phase 4 — 이어받으면 원문을 빼고 보낸다

- **Status**: DONE
- **설명**: DEC-024 D5. 실제 절감이 여기서 난다.
- **작업**:
  - [x] `context_payload` — `session_ref` 가 있으면 `source_excerpt` 제외, `resumed_session: True` 추가
  - [x] `summary` 는 **항상** 유지한다
- **검증**:
  - [x] 세션 있음/없음 두 경우의 제출 payload 크기를 재서 기록한다
  - [x] 세션 없이 여는 첫 게이트에는 원문이 그대로 실린다
  - [ ] 원문을 뺀 제출로도 뒤 스테이지 산출물이 성립한다 — **P5 에서 실전으로 확인한다**
- **완료 증거**: 세션이 있으면 `source_excerpt`(상한 40,000자)를 빼고 `resumed_session: True` 를 넣는다.

  **문서와 코드가 갈려 있던 자리였다.** SPEC-009 S-1 5항이 「이어받으면 원문·지침을 다시 보내지 않아도 된다」고 적어 뒀는데, `AgentStage.submit` 이 프롬프트 뒤에 payload 전문을 무조건 붙이기 때문에 **세션을 물어도 매번 4만 자를 다시 보내고 있었다.** 승계만 넣고 이걸 안 고쳤으면 「이어받는데 왜 안 빨라지지」가 됐을 것이다.

  `resumed_session` 플래그를 함께 넣는다 — 안 알려 주면 에이전트가 「자료를 안 줬다」로 읽는다. 테스트는 **실물 타입**(`QueueItem`·`ItemPreparation`)으로 만든다(가짜 dict 를 넘기면 직렬화 결함이 안 잡힌다).

### Phase 5 — 재측정

- **Status**: TODO
- **설명**: **표본 1건으로는 좋아졌다고 말할 수 없다.** 같은 성격의 자료로 다시 잰다. 배포가 선행한다 — P1~P4 는 로컬 회귀(981 passed)까지만 닫혔다.
- **작업**:
  - [ ] 유튜브 자료 1건을 끝까지 태우고 스테이지별 소요를 기록한다
  - [ ] `2026-08-13-knowledge-pipeline-stage-timing` 의 값과 나란히 표로 남긴다
  - [ ] 품질 축도 본다 — `concept`·`derived` 가 앞 산출물을 실제로 딛고 있는지 육안 확인
- **검증**:
  - [x] 스테이지별 소요와 합
  - [x] 세션이 실제로 물렸는지 `ai_tasks.session_ref` 로 확인 (같은 값이 체인에서 이어지는지)
  - [x] 나빠졌으면 **나빠졌다고 적는다.** 숫자를 맞추려고 규칙을 비틀지 않는다
  - [ ] 품질 축 — 뒤 스테이지가 앞 산출물을 실제로 딛는지 육안 확인
- **완료 증거**: item **#3881**.

  **게이트 넷이 한 세션이다.** `ai_tasks.session_ref` 가 `route`·`source_note`·`concept`·`derived` 전부 `506af245-d111-4f33-9d67-89126fef8015` 로 같다. DEC-024 D1 이 실전에서 돈다.

  `summarize` 만 다른 세션(`8bc7a5a6…`)이다 — **의도한 대로**다(OQ-1 로 미뤄 둔 범위).

  | 스테이지 | #3880 (승계 전) | #3881 (승계 후) |
  |---|---|---|
  | `summarize` | 39초 | 42초 |
  | `route` | 75초 | 92초 |
  | `source_note` | **95초 실패 + 309초** | **42초** |
  | `concept` | 135초 | 134초 |
  | `derived` | 125초 | 105초 |
  | **게이트 합** | **644초** (실패 제외) | **373초** |

  **이 표를 개선 수치로 읽으면 안 된다.** 자료가 다르다 — #3881 은 48분 영상이고 #3880 은 그보다 짧다. `route` 는 오히려 17초 늘었다(요약이 두꺼워졌다). 표본은 여전히 각 1건이다.

  **읽을 수 있는 것은 `source_note` 하나다.** 309초 → 42초는 자료 길이 차이로 설명되지 않는 폭이고(이번 자료가 더 길다), 승계가 예측한 방향과 맞는다 — 규칙·양식을 다시 안 읽고 원문 4만 자도 다시 안 받았다. 나머지 스테이지는 승계 전후가 사실상 같다.

  **그런데 그 42초가 대가를 치렀을 수 있다.** 같은 실행의 `source_note` 가 frontmatter `type: reference` 를 빠뜨려 발행이 거부됐다(WORK-021 P5·P6). `type` 이 적힌 자리는 `rules/` 의 층별 필수 필드 표이고, 세션을 물어 규칙을 다시 안 읽은 실행에서 그 필드가 빠졌다. **인과를 단정할 수는 없다** — 표본 1건이고, 템플릿 자체가 `type` 을 안 보여 주고 있었던 것이 더 직접적인 원인이다(그래서 템플릿을 고쳤다). 다만 **「덜 읽어서 빨라진 것」과 「덜 읽어서 빠뜨린 것」이 같은 실행에서 나왔다**는 사실은 남긴다. OQ-1 로 추적한다.

## Rollback

코드 변경만이다. 되돌리면 스테이지마다 새 세션으로 돌아간다 — **진행 중인 항목도 그대로 동작한다**(stateless 폴백이 살아 있기 때문이다). 이것이 D4 를 유지한 실질적 이유이기도 하다.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | **승계가 「덜 읽는」 쪽으로 작용해 규칙 준수가 느슨해지는지** | kknaks | #3881 의 `source_note` 가 42초(309초 대비)로 빨랐고 같은 실행에서 `type` 을 빠뜨렸다. 인과 단정 불가(템플릿 결함이 더 직접적)이나 다음 3건의 실행에서 필수 필드 누락이 또 나오는지 본다 |
| OQ-3 | 긴 체인에서 세션이 압축돼 원문 세부가 사라지는지 | kknaks | DEC-024 OQ-2. #3881(48분 자료)에서는 징후 없음 — `derived` 가 원문 세부를 정확히 다뤘다 |
| OQ-2 | `summarize` 까지 이을지 | kknaks | DEC-024 OQ-1. 게이트 사이가 먼저 돈 뒤 |
