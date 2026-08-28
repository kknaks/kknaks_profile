---
type: reference
id: 2026-08-28-action-runtime-engine
title: 워크플로 엔진을 선언으로 조립한 구조 — 커널·조각·선언
summary: 회사 AX 프로젝트에서 결재 게이트 워크플로 엔진을 설계·구현하며 관찰한 것 — 뼈대는 한 번 만들고 무편집, 재사용 조각은 라이브러리, 새 워크플로는 선언 1개 + 등록 1줄로 조립되는 구조
author: 이건학
date: 2026.08.28
tags:
  - 실무기록
  - 설계
  - AI에이전트
stack:
  - Python
links: []
---

# 워크플로 엔진을 선언으로 조립한 구조 — 커널·조각·선언

회사 AX 프로젝트에서 "발생 → AI 처리 → 결재 게이트 → 실행 → 피드백" 모양의 업무 워크플로를
일반화하는 엔진을 만들며 관찰한 기록이다. 출발점의 문제는 단순했다 — 워크플로마다 전용
오케스트레이션 코드를 다시 짜고 있었고(승인 게이트 두 개가 구조는 완전 동형인데 코드 공유 0),
이 방식으로는 워크플로 60여 개 확장이 감당되지 않는다.

북극성은 **새 워크플로 = 선언 1개**. 실제로 두 번째 도메인부터는 "패키지 1개 + 등록 1줄"로
워크플로가 추가됐고, 그 라운드에서 공용층 기존 시그니처 변경이 0이었다.

## 계층 — 뭐가 고정이고 뭐가 자라나

```text
[뼈대 — 한 번 만들고 무편집]
  게이트 커널          결재 카드(Action) 생명주기 기계
  스테이지 그래프 엔진   선언(stages + edges)을 읽어 전이를 구동

[라이브러리 — additive 로만 자람]
  조각(piece)          재사용 스테이지 기계 (ai_draft · regen_gate · gate · task_round · execution)
  엣지 어휘            전이의 "종류" (7종)

[워크플로마다 — 선언(데이터)]
  WorkflowDeclaration  스테이지 = 조각 참조 + 파라미터, 엣지, amendment
```

변경 비용이 계약이다: 대부분은 선언 1개 작성으로 끝나고, 새 외부 행위가 필요할 때만 조각 1개를
라이브러리에 **추가**하며, 엔진에 엣지 어휘를 추가하는 일은 초기 몇 번 후 수렴한다. 모든 추가가
additive 라서 새 워크플로가 기존 워크플로를 회귀시키는 경로가 구조적으로 없다.

## 커널 — 상태는 두 층이고 규칙이 다르다

| 층 | 무엇 | 규칙 |
|---|---|---|
| Action 상태 (게이트 FSM) | needs_approval → approved → executing → done/… | **고정** — 전이 매트릭스 하나. 워크플로가 늘어도 상태를 추가하지 않는다 |
| run 상태 (워크플로) | 지금 어느 스테이지에 있나 | **선언** — 새 상태 = 새 스테이지 선언. 코드 0 |

게이트 FSM 은 11개 상태의 frozenset 전이 매트릭스 하나로 존재하고, 커널의 모든 전이가 이걸
통과한다. 승인 멱등은 2중이다 — 이미 종결된 카드는 그대로 반환(멱등 view), 같은
`(action_id, plan_version)` 의 승인 클릭은 DB 의 `on_conflict_do_nothing` 이 최종 방어선.
승인은 항상 특정 plan version 에 바인딩되므로 오래된 화면에서의 승인은 stale 로 거부된다.

외부 실행 전에 EXECUTING 전이 + 실행 원장 row 를 **먼저 commit** 한다 — 연결이 끊긴 뒤
재승인해도 외부 write 가 중복되지 않게. 실행 결과가 유실되면 외부 시스템 실상과 대조하는
reconcile 이 있는데, 도메인은 "외부에 실제로 있나"만 3분기(confirmed/absent/unknown)로 답하고
전이·원장·audit 은 커널이 소유한다.

### Definition-Driven Dispatch — 커널에 타입 분기가 0

서로 다른 워크플로가 같은 커널 위에서 구르려면 "이 카드 type 이면 이렇게 처리"라는 판단이
커널 코드 분기가 아니라 **정의 조회**여야 한다. 불변식: 커널 코드에 `action.type ==` 값 비교가
grep 0건.

```python
@dataclass(frozen=True)
class ActionDefinition:
    type: str                      # 🟩 데이터 — Discriminator (1 값 = 1 정의)
    gate_policy: str               # 🟩 승인 주체 정책
    expiry: ExpiryPolicy           # 🟩 만료 정책 (none | ttl | 대상 시작 시각)
    surface_contract: ...          # 🟩 카드 최소 판단 요건 (필수 facts · diff)
    approve_inputs: frozenset[str] # 🟩 이 게이트가 받는 승인 파라미터 선언
    handlers: ActionHandlers       # 🟦 before_approve · execute · reconcile · on_reject — 이름→함수 포인터
    pre_approve_guard: ... | None  # 🟦 승인 전 차단 조건
```

분기 3종의 행선지가 정리된다: ① 타입 디스패치("무슨 type 이지")는 레지스트리 조회가 흡수해
**소멸**, ② 스테이지 전이("다음이 뭐지")는 선언 **데이터**로, ③ 도메인 상황 분기("선점됐나")는
핸들러 안에 **남는 게 정상**. 금지되는 것은 커널이 도메인 type 을 알아보는 것뿐이다.

정직한 경계도 계약이다 — 외부 호출(예약 생성·채널 개설)은 실제 행위라 코드고, 정의는 그
핸들러를 이름으로 가리킬 뿐이다. "완전 no-code"가 아니라 **"정책·계약·배선은 데이터, 외부
write 행위는 코드"**.

## 스테이지 그래프 엔진 — 값은 파라미터, 종류만 어휘

엣지 어휘는 발명하지 않고 두 사례(미팅 예약·incident)의 전이 전수 실측에서 출발했다:

```text
트리거:  on_trigger · on_approve · on_reject · on_decision(값) · on_event(이름) · on_all_done · on_timeout
행선지:  go(stage) · loop(stage, round+1) · DONE · FAILED
```

`on_decision("재발행")` 의 "재발행"은 워크플로가 선언하는 **값**이지 어휘 확장이 아니다. 어휘가
느는 것은 전이의 의미 자체가 새로울 때뿐(예: 병렬 join)이고, 엔진에 1회 추가하면 전 워크플로가
쓴다. 실제로 두 번째 도메인은 어휘를 하나도 추가하지 않고 선언됐다.

전이 해석은 순수 함수다 — `resolve(선언, 현재 스테이지, 신호) → 행선지`. 매칭되는 엣지가 없으면
조용한 fallback 이 아니라 `UndeclaredTransition` 예외다. **선언 밖 전이는 엔진이 거부한다** —
상태 전이가 데이터가 되는 동시에 검증 가능해진다. 엔진은 status 문자열 값을 발명하지 않는다 —
도착 스테이지/행선지 선언이 들고 있는 값을 읽어 쓸 뿐이다.

재밌는 선택 하나: run 의 현재 스테이지는 컬럼이 아니라 run metadata dict 의 키 하나다. 완료된
run 에 곁붙는 취소·변경 게이트(amendment)는 스테이지 그래프 밖(off-graph) 카드로 만들어지고,
선언의 `Amendment(reactivate, closed)` 데이터를 엔진이 조회해 run 을 되돌렸다가 닫는다 —
조각 인터페이스는 무변경이다.

## 조각 — 전이를 모르는 스테이지 기계

```python
@runtime_checkable
class StagePiece(Protocol):     # 훅 4종 전부 optional
    async def enter(self, ctx, run, stage) -> Signal | None: ...
    async def on_event(self, ctx, run, stage, event) -> Signal | None: ...
    async def on_verdict(self, ctx, run, stage, verdict) -> Signal | None: ...
    async def on_timeout(self, ctx, run, stage, cause) -> Signal | None: ...
```

규율 세 개가 조각을 어느 워크플로에나 꽂히는 부품으로 만든다.

1. **조각은 다음 스테이지를 모른다.** 신호(APPROVED/REJECTED/DECISION/EVENT/ALL_DONE/TIMEOUT)만
   반환하고, "그 신호면 어디로"는 선언의 엣지가 정하며 엔진이 수행한다. 기존 구현이 재활용
   불가능했던 근본 원인이 조각 안에 전이가 하드코딩된 것이었다.
2. **도메인 가변부는 파라미터 주입.** 도메인이 콜러블 번들(deps)을 만들고 선언이
   `StageDecl(params={...})` 로 꽂는다. 조각은 도메인을 import 하지 않는다.
3. **기계는 이름표를 주입받지 않는다.** audit 라벨은 조각의 모듈 상수, 산출 kind 는 `stage.id`,
   게이트 정책은 정의 조회 — 그래서 워크플로가 늘어도 이벤트 어휘가 늘지 않는다.

조각과 엔진의 유일한 접점은 Signal(조각 6종) ↔ Trigger(엣지 7종) 번역표다. 게이트 결과(Verdict)를
Signal 로 번역하는 것은 조각 소관이라 엔진은 게이트 의미조차 모른다.

배운 것 하나 — **라이브러리에 조각을 세워 두는 것만으로는 계약이 검증되지 않는다.** 소비자 0
인 동안 드러나지 않던 조각 결함(사라진 컬럼을 계속 넘기던 인자)이 두 번째 소비자가 붙는 순간
발각됐다. 두 번째 소비자가 붙기 전까지 조각은 "미검증"으로 취급한다.

## 조립 — 등록 1줄

새 워크플로 = 패키지 1개(선언·정의·도메인 로직·표면 바인딩) + 등록 1줄:

```python
register_workflow(
    C.INCIDENT_WORKFLOW_TYPE,
    DomainSpec(build_domain=..., register_definitions=...),
)
```

등록 트리거는 패키지 import(멱등)이고, 등록부·조립 factory 는 어떤 도메인도 import 하지 않는다.
미등록 type 은 조용한 fallback 없이 명시적 에러. 채팅으로 시작할 수 있는 워크플로는 이 등록
1줄에 capability leaf·시작 콜러블·발화 예시를 얹는다 — 공용 파일에 목록을 중앙 하드코딩하면
도메인 추가마다 공용층을 편집해야 해서 계약이 깨지기 때문이다.

같은 선언 어휘로 2스테이지(게이트→실행) 워크플로와 8스테이지(AI 산출 3회 + 게이트 3회 +
태스크 라운드 + 대기 실행) 워크플로가 표현된다. 후자는 재생성 게이트 조각 1벌이 세 게이트에
3회 인스턴스화된 것이라, "한 번 만든 조각이 코드 재작성 없이 재사용되는가"라는 판정 기준이
실측으로 닫혔다.

## 관찰 명제

1. **상태를 두 층으로 갈라라.** 고정 FSM(게이트)과 선언 상태(워크플로)를 섞으면 워크플로마다
   상태 머신이 자란다.
2. **타입 분기는 레지스트리 조회로 소멸시키되, 도메인 상황 분기는 핸들러에 남는 게 정상이다.**
   전부 데이터화하려는 순간 거짓말이 시작된다.
3. **부품은 다음 단계를 몰라야 부품이다.** 전이 판정이 엣지표 한 곳에만 있어야 어휘가 유한하게
   유지된다.
4. **조용한 fallback 금지.** 선언 밖 전이·미등록 type·미선언 카탈로그 항목은 전부 명시 예외 —
   조용한 제외는 "왜 안 뜨지"로 나타나 아무도 안 고친다.
5. **공용층은 additive 로만 자란다.** 새 도메인이 기존 공용 자산의 시그니처를 바꿔야 한다면
   그것은 주입 경계 설계가 틀렸다는 신호다.

## 자란 개념

이 기록에서 자란 상세는 개념 노트가 소유한다 — [[workflow-orchestration]](스테이지 그래프 선언·조각),
[[human-in-the-loop]](승인 카드·plan version 바인딩·멱등), [[dispatch-table]](커널의 Definition-Driven
Dispatch).

AI 산출·tool 실행 축은 [[2026-08-28-llm-tool-calling]] 에 따로 적었다.
