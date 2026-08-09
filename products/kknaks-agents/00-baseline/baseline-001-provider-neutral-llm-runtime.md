---
type: baseline
id: KAG-BL-001
title: "Provider-neutral LLM runtime 라이브러리"
status: accepted
product: kknaks-agents
source:
  type: reference
  ref: "REF-0007 provider-neutral LLM runtime 설계 노트 (오케스트레이션 설정 레포, read-only)"
links:
  baselines: []
  decisions:
    - "[[decision-001-runtime-directory-boundaries|KAG-DEC-001]]"
    - "[[decision-002-turn-runtime-flow|KAG-DEC-002]]"
    - "[[decision-003-core-contract-boundaries|KAG-DEC-003]]"
    - "[[decision-004-process-boundaries|KAG-DEC-004]]"
  specs: []
  works: []
  releases: []
  related: []
created_at: 2026-08-07
updated_at: 2026-08-09
tags:
  - product/kknaks-agents
  - doc/baseline
  - status/accepted
  - llm-runtime
  - provider-neutral
---

# Provider-neutral LLM runtime 라이브러리

LLM을 특정 agent 제품(Claude Code, Codex CLI 등)의 harness에 얹는 대신, 교체 가능한 추론 모듈로 두고 tool·loop·session·context·skill의 소유권을 애플리케이션 쪽에 남기는 최소 Python runtime을 만들자는 입력이다.

> 아직 결정하지 않은 날것의 입력이다. 정리보다 보존이 우선이다. 여기에는 확정 결정, 공개 API, 구현 지시를 두지 않는다.

## Raw

### 지금 구조의 문제

- LLM을 쓰려면 특정 agent 제품의 harness에 올라타게 된다. 그 순간 tool 목록, 실행 권한, 대화 상태, 재개(resume), 압축(compaction)이 전부 그 제품 내부 규칙을 따른다.
- 제품을 바꾸면 애플리케이션 코드가 같이 바뀐다. tool을 어떻게 등록하는지, session이 어디에 남는지, 어디까지가 내 상태인지가 provider마다 다르기 때문이다.
- 권한이 harness 안으로 들어간다. "이 사용자가 이 tool을 쓸 수 있는가"를 내가 판정하지 않고 harness의 설정에 위임하면, 같은 데이터에 대해 REST가 막은 것을 채팅이 우회할 수 있는지 스스로 증명할 수 없다.
- 학습 목적으로도 불리하다. loop·context·compaction이 남의 블랙박스 안에 있으면 무엇이 왜 그렇게 동작하는지 관찰할 수 없다.

### 하고 싶은 것

LLM에게 남기는 일을 좁힌다.

- 사용자 질문 해석
- 허용된 tool 중 사용할 tool 제안
- tool 결과 요약
- 근거 범위 안의 최종 답변 생성

라이브러리와 호스트 애플리케이션이 소유하는 일.

- tool·skill 등록
- tool 입력 검증, 권한 확인, 실행
- model 호출 반복과 종료 조건
- session 원본 상태와 event log
- context 구성과 compaction
- provider 선택과 변환
- 실행 제한, 취소, 감사, 오류 처리

경계 한 줄: **provider는 한 번의 공통 요청을 한 번의 공통 응답으로 바꾸는 adapter다.** provider의 thread, resume, 내장 tool, 내장 skill, 내장 compaction은 공통 계약에 넣지 않는다.

### 첫 실험

첫 backend는 **Codex CLI subprocess**다. session이나 agent runtime으로 쓰지 않고, 매 model step을 독립 subprocess 1회 실행으로 두고 공통 요청을 prompt/JSON 계약으로 투영한 뒤 공통 응답으로 복원한다. 필요한 history는 runtime이 매번 명시적으로 넘긴다.

첫 사례는 **문서 검색·열람 기반 답변 생성**이다. read-only tool 두 개(문서 검색, 문서 열람)만 노출하고, 근거가 연결된 답변을 만든다.

## Context

### 이 입력이 나온 배경

설계 노트 `REF-0007`(오케스트레이션 설정 레포, read-only)에 목적·원칙·디렉터리 구조 가안·동작 흐름·사용법 가안·단계별 구현 범위·보류 결정이 이미 정리돼 있다. 이 baseline은 그 노트를 제품 문서 파이프라인에 등록하는 첫 입력이며, 노트에 없는 제품 결정을 추가하지 않는다.

### 관찰한 사례 1 — 사내 운영 서비스의 server-owned tool loop (read-only)

실제로 운영 중인 서비스에서 서버가 loop를 소유하는 구현을 읽었다. 조직·업무·데이터가 드러나는 내용은 옮기지 않고 구조 패턴만 적는다.

- **한 턴 = 하나의 JSON**. 모델은 매 턴 "tool을 부르겠다" 또는 "최종 산출이다" 중 하나만 낸다. 둘이 섞이거나 산문이 섞이면 실패로 처리한다. 실제로 모델이 "아직 tool 결과를 기다리는 중"이라는 산문을 내면서 파서가 죽은 라이브 실패가 있었고, 이미 실행된 tool 결과를 프롬프트에 **또렷한 라벨 블록**으로 다시 보여주는 방식으로 고쳤다.
- **이미 준 결과를 다시 주지 않는다는 신호가 중요하다.** JSON 한 덩어리로 덤프하면 결과가 묻히고, 목록이 비었을 때는 "아직 아무것도 없다"를 명시해야 착각이 줄어든다.
- **프롬프트 비대 방지**를 loop 안에서 한다. 같은 tool을 반복 호출하면 가장 최근 결과만 전문으로 유지하고 이전 것은 식별자 + 발췌 + "이미 읽음"으로 축약한다.
- **tool 실패는 loop에 되먹인다.** 실패했다고 turn을 죽이지 않고 모델이 대안을 찾게 한다. 반면 미등록 tool 호출은 거부로 기록하고 loop는 계속한다.
- **접근 제어와 실행 승인은 별개 축이다.** "누가 이 tool을 쓸 수 있는가"(역할·권한)와 "이 write가 승인됐는가"(승인 게이트)를 분리해 둘 다 실행기가 집행한다. tool의 분류 namespace는 배치 축일 뿐 권한 축이 아니다.
- **모든 tool 호출은 기록에 남는다. 거부도 기록이다.** 어느 축에서 막혔는지(내부 전용/역할/권한) 구분해 남기지 않으면 감사 기록이 무의미해진다.
- **접근 선언에 기본값을 두지 않는다.** 빠뜨리면 "전원 허용"으로 열리기 때문에, 새 tool을 만들 때 접근 범위를 한 번은 반드시 판단하게 강제한다. 권한이 비어 있는 항목은 "누구나"가 아니라 "아직 판단하지 않음"으로 읽고 열지 않는다.
- **노출 목록과 실제 실행 목록은 같은 계산기를 쓴다.** 두 벌이 되면 "보이는데 못 쓰는 tool"이 생기고 어느 쪽이 맞는지 알 수 없게 된다.
- **durable turn과 event folding.** turn을 DB에 남기고, 스트림 이벤트를 접어서 상태로 만든다. 브로커가 재전송하면 처음부터 다시 오므로 folding은 **같은 이벤트를 두 번 받아도 같은 결과**여야 한다 — 누적형은 재생 시작 시 초기화 후 다시 쌓고, tool 이벤트는 호출 ID 기준 멱등 upsert하며, 이미 종료된 turn의 완료 이벤트는 무시한다.
- **순서는 항상 기록 먼저, 알림 나중.** 구독자가 없어도 loop는 끝까지 돌고, 알림을 놓쳐도 기록이 진실을 복원한다.
- **동기화 실패를 "없음"으로 해석하지 않는다.** 카탈로그 조회가 실패했을 때 "tool이 하나도 없다"로 접으면 일시 장애가 전면 비활성으로 번진다. 실패하면 아무것도 건드리지 않는다.
- **상한은 바깥에서 건다.** 스트림이 이벤트를 하나도 내지 않으면 내부 timeout이 발동하지 않을 수 있어 별도로 상한을 건다.

이 사례는 "서버가 loop를 소유하면 실제로 무엇을 감당해야 하는가"의 증거이지, 이 라이브러리가 그 구조를 그대로 복제해야 한다는 뜻은 아니다. 그쪽은 특정 제품의 웹 서비스이고 이쪽은 범용 라이브러리다.

### 관찰한 사례 2 — clean-room 연구 (개념만)

개인 clean-room 연구 자료를 개념 수준에서만 관찰했다. 코드·문자열·식별자를 옮기지 않았고, 파생 문서에서 출처로 인용하지 않는다. 아래는 이 제품의 언어로 다시 쓴 개념이다.

- **대화 하나에 lifecycle 소유자 하나.** 대화 단위 객체가 상태를 들고 있고, 사용자 입력마다 그 안에서 turn이 시작된다. 대화에 걸쳐 남는 상태(메시지, 파일 캐시, 누적 사용량)와 turn마다 초기화되는 상태(이번 turn에 발견한 것들)를 명시적으로 나눈다. 나누지 않으면 turn이 쌓일수록 무한히 커진다.
- **tool 결과는 다음 model 호출 이전에 정규화되어 대화 이력으로 되돌아간다.** 한 응답에 여러 tool 호출이 있으면 결과를 모아 이력에 붙이고 다시 model을 부른다. 즉 tool 실행은 곁가지가 아니라 대화 이력 자체를 만드는 단계다.
- **원본 이력과 model에 보내는 view를 분리할 수 있다.** UI가 있는 경로는 전체 이력을 들고 필요할 때 축약본을 투영하고, 화면이 없는 헤드리스 경로는 메모리 경계를 위해 이력 자체를 자를 수 있다. 즉 "무엇을 보관하는가"와 "무엇을 model에 보내는가"는 같은 결정이 아니다.
- **중단 신호를 lifecycle 소유자가 들고 있다.** 취소는 loop 바깥에서 주입되는 것이 아니라 turn을 소유한 쪽의 상태다.

## Why It Matters

- **교체 가능성이 목적이다.** provider를 바꿔도 tool·session·context·runtime 코드가 그대로여야 한다. 그것이 성립하는지는 provider adapter를 두 개 이상 붙여봐야 알 수 있다.
- **권한과 상태의 소유권이 안전 경계다.** model 출력은 명령이 아니라 실행 요청이고, 사용자·tenant·권한은 model이 만든 인자가 아니라 runtime이 주입하는 context여야 한다. 이 경계가 없으면 모델이 자기 권한을 스스로 주장할 수 있게 된다.
- **loop를 소유해야 학습이 된다.** 종료 조건, malformed 응답 처리, tool 실패 되먹임, context 재구성이 내 코드 안에 있어야 관찰하고 바꿀 수 있다.
- **근거 있는 답변이 첫 사례인 이유.** 문서 검색·열람은 read-only이고 근거 ID로 검증 가능해서, 최소 loop의 정확성을 판정할 수 있는 가장 싼 시나리오다.

## Possible Direction

아직 결정이 아니다. decision 단계에서 하나씩 판단한다.

### 책임 분해 (설계 노트의 가안)

`core`(공통 요청·응답·content block·tool call·event 계약) / `runtime`(turn 반복·종료 조건·최종 응답 검증) / `providers`(변환만) / `tools`(등록·schema 검증·policy·실행) / `sessions`(event 저장·조회) / `context`(구성·압축) / `skills`(등록·선택·prompt 투영) / `process`(subprocess 격리·timeout·출력 처리)로 나누는 안. `runtime`과 `core`에는 provider 전용 타입을 두지 않는다.

### 등록과 허용의 분리

애플리케이션 시작 시 실행 가능한 tool을 **등록**하고, 각 turn에서 실제로 model에 공개·실행할 subset을 **허용**으로 따로 정한다. turn 시작 시 tool 이름·버전·registry revision을 snapshot으로 남긴다. server/worker를 나눌 때도 함수 객체를 직렬화하지 않고 이름·버전·revision만 넘긴 뒤 worker가 자기 registry에서 조회한다는 안이 노트에 있다.

### session 원본과 model context의 분리

session event log는 손실 없는 원본으로 두고, context builder가 이번 호출에 필요한 것만 골라 요청을 만든다. compaction은 원본을 지우지 않고 model context만 줄이며, 근거 ID·출처 위치·tool call과 결과의 짝은 보존한다. 요약문을 새로운 사실 원본으로 취급하지 않는다.

### Codex CLI subprocess를 첫 provider로

매 호출을 독립 subprocess로 실행하고, 내부 session/resume/내장 tool/MCP/skill에 의존하지 않으며, stdout은 protocol·stderr는 진단으로 분리하고, timeout·출력 크기·종료 코드를 검사하고, 환경변수는 allowlist만 넘긴다는 안. 다만 Codex CLI가 내부적으로 agent harness를 포함한다는 사실은 남으므로, 이것은 **첫 학습 backend**이고 raw API·local model backend와의 동등성은 별도 contract test로 확인해야 한다.

### 첫 vertical slice의 모습

애플리케이션이 read-only tool 두 개를 등록하고, runtime이 그 turn에 그 둘만 공개하고, 매 step에 공통 JSON 응답 하나를 받고, tool call을 검증·실행해 다음 요청에 포함하고, 제한된 step 안에서 근거가 연결된 최종 응답을 만든다. 없는 tool·잘못된 입력·timeout·malformed 응답이 안전하게 실패하고, 가짜 provider로 외부 프로세스 없이 같은 loop를 재현할 수 있다.

## Reference 경계

이 baseline이 근거로 쓴 자료의 취급 규칙이다. 이후 decision·spec에서도 유지한다.

| 자료 | 경계 |
|---|---|
| 설계 노트 (`REF-0007`) | 현재 기준. 여기 없는 제품 결정을 발명하지 않는다. 노트의 코드 예시는 **가안**이며 확정 public API로 승격하지 않는다 |
| 사내 운영 서비스 구현 | read-only. 코드를 수정하지 않는다. 회사명·조직·업무 정보·민감 데이터의 본문을 옮기지 않고, 구조 패턴만 일반화해 적는다 |
| clean-room 연구 아카이브 | 실행하지 않는다. 코드·문자열·식별자를 복사하지 않고, 파생 문서에서 인용·출처 명시를 하지 않는다. 개념은 이 제품 고유 언어로 다시 명명한다 |

## Open Questions

decision으로 내리기 전에 판단이 필요한 것들이다. 아직 답을 정하지 않는다.

| # | 질문 | 왜 지금 못 정하나 |
|---|---|---|
| 1 | 저장소·배포 package의 최종 이름 | 설계 노트의 `llm_runtime`·`llm-runtime-lab`은 가칭이다 |
| 2 | Python 최소 버전과 공개 API의 sync/async 형태 | 사용처가 아직 하나(예제)뿐이라 근거가 없다 |
| 3 | JSON Schema validator 선택 | tool 입력 검증 방식과 의존성 정책이 함께 결정돼야 한다 |
| 4 | Codex CLI의 정확한 격리 옵션과 출력 protocol | 실제 실행 실험 전 |
| 5 | provider capability 표준(native tool call 지원 여부 표현) | provider adapter가 하나뿐이라 비교 대상이 없다 |
| 6 | token 계산 방식과 compaction 진입 기준 | context builder 형태가 정해진 뒤 |
| 7 | skill 선택 주체 — 애플리케이션인가 별도 selector인가 | 첫 사례에 skill이 한 개뿐이라 구분이 드러나지 않는다 |
| 8 | session event에 provider 원문을 보관할지 | 저장 정책·민감도 판단과 묶인다 |
| 9 | 민감 데이터를 외부 provider로 보낼 때의 데이터 등급 정책 | `context/policy.md`와 함께 판단해야 한다 |
| 10 | `products/open-kknaks/`와의 관계 — 대체인가, 상위/하위인가, 무관인가 | 두 제품의 경계를 명시적으로 결정한 적이 없다 |
| 11 | queue·multi-worker·production 배포를 어느 시점에 볼지 | 현재는 MVP 확정 범위가 아니다. 단일 사용자 subprocess 학습 단계에서는 구현하지 않는다 |

## Next

첫 decision(`KAG-DEC-001` — 디렉터리 구조와 의존 경계)이 2026-08-08 사용자 확정으로 `accepted`가 되어, 이 baseline도 `accepted`다. 반영된 것은 **디렉터리 구조와 의존 방향까지**였다.

두 번째 decision(`KAG-DEC-002` — 최소 headless turn runtime 동작 구조)도 2026-08-08 사용자 확정으로 `accepted`가 됐다. 한 turn의 진행 phase 9 + 종료 state 4 전이, side effect 순서와 불변식, 반복 진입·종료 조건이 확정되면서 위 Possible Direction의 “책임 분해” 중 **동작 흐름 부분까지** 반영 범위가 넓어졌다. 이 baseline의 `accepted`는 그대로이고, KAG-DEC-002의 Open Questions 9건은 여전히 미결이다.

세 번째 decision(`KAG-DEC-003` — core package 계약 경계)은 2026-08-09 `proposed`로 올라가 사용자 리뷰를 기다린다. 위 Possible Direction의 “책임 분해” 중 `core`가 담을 계약의 **파일·타입 범주와 공개 표면**을 제안하는 단계이며, 아직 확정이 아니므로 이 baseline의 반영 범위는 넓어지지 않았다. 이 baseline의 `accepted`도 그대로다.

네 번째 decision(`KAG-DEC-004` — process package 실행 격리 경계)도 2026-08-09 `proposed`로 올라가 사용자 리뷰를 기다린다. 위 Possible Direction의 “Codex CLI subprocess를 첫 provider로”가 나열한 격리 항목(cwd·환경 allowlist·timeout·출력 상한·stdout/stderr 분리·종료 코드)을 **provider-neutral한 실행 격리 계약**으로 일반화하고, 파일 배치와 lifecycle과 fail-closed 원칙을 제안하는 단계다. provider 제품명·실행 파일·flag·wire 형식은 여전히 `providers`의 몫으로 남으므로, Open Question 4(Codex CLI의 정확한 격리 옵션과 출력 protocol)는 풀리지 않았다. 확정이 아니므로 이 baseline의 반영 범위는 넓어지지 않았고 `accepted`도 그대로다.

아직 decision으로 내려가지 않은 것: 등록/허용 분리의 계약 표면, session 원본과 model context 분리의 구체 계약, Codex CLI provider 격리 옵션, 첫 vertical slice 범위, 그리고 위 Open Questions 대부분. decision 없이 spec·work·코드로 내려가지 않는다.
