# Decision Index

규칙: `rules/product-doc-pipeline.md`

> baseline을 제품에 어떻게 적용할지 판단한 결정 목록과 아직 풀어야 할 질문을 관리한다.

첫 decision인 KAG-DEC-001이 2026-08-08 사용자 확정으로 `accepted`가 됐다. 확정 범위는 디렉터리 구조와 의존 방향까지다.

두 번째 decision인 KAG-DEC-002(최소 headless turn runtime 동작 구조)도 2026-08-08 사용자 확정으로 `accepted`가 됐다. 확정 범위는 한 turn의 진행 phase 9 + 종료 state 4 전이, side effect 순서와 불변식, 반복 진입·종료 조건까지이며, 각 문서의 Open Questions는 여전히 미결이다.

세 번째 decision인 KAG-DEC-003(core package 계약 경계)은 2026-08-09 `proposed`로 올라가 **사용자 리뷰 대기** 중이다. 공개 계약을 package 하나씩 내려가기로 해서 이번 대상은 `core/` 하나이며, `tools`·`providers`·`sessions`·`context`·`skills`·`process`·`runtime`의 내부 구조는 다루지 않는다. 확정 전에는 spec·work·코드로 내려가지 않는다.

네 번째 decision인 KAG-DEC-004(process package 실행 격리 경계)도 2026-08-09 `proposed`로 올라가 **사용자 리뷰 대기** 중이다. 의존 그래프의 아래에서 위로 올라가는 순서라 `core`(L0) 다음이 `process`(L1)이며, 이번 대상은 `process/` 하나다. KAG-DEC-004는 KAG-DEC-003을 확정 사실이 아니라 `proposed` 입력으로만 참조하고, `core` 파일 배치와의 연결은 범주 수준으로만 둔다(KAG-DEC-004 OQ-5). 남은 raw 작성 순서는 `providers` → `tools` → `sessions` → `skills` → `context` → `runtime`이다.

## 결정 로그

decision 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다.

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| KAG-DEC-001 | [Runtime 디렉터리 구조와 의존 경계](decision-001-runtime-directory-boundaries.md) | accepted | KAG-BL-001 | 책임별 package 채택 (flat / ports-adapters 기각). package 이름 `kknaks_agents`, 4단 의존 계층 확정 | - |
| KAG-DEC-002 | [최소 headless turn runtime 동작 구조](decision-002-turn-runtime-flow.md) | accepted | KAG-BL-001 | 명시적 phase/state transition을 가진 deterministic turn loop 채택 (불투명 `run()` / middleware-hook pipeline 기각, hook은 후속 확장 후보로 보존). 진행 phase 9 + 종료 state 4, side effect 순서 불변식 3, tool call 직렬 실행, 종료 원인 10종의 terminal/recoverable 판정. `query/` 디렉터리 없이 `runtime`이 흡수. 미결 9건 | - |
| KAG-DEC-003 | [core package 계약 경계 — 파일·타입 범주와 공개 표면](decision-003-core-contract-boundaries.md) | **proposed** (리뷰 대기) | KAG-BL-001 | 단일 `contracts.py` / 관심사별 평면 module / 도메인별 중첩 package+`ports` 3안 비교 후 **평면 module 분리 권고**(나머지 둘 비권고, 중첩은 승격 경로로 보존). core 소유 계약 범주 10종, 파일 후보 10개 + `__init__.py`, 파일별 producer/consumer, core 내부 6단 총순서(`events → responses` 단방향), protocol은 “소비자가 구현 package를 import할 수 없을 때만” 판정(`protocols.py` 후보 2 = 필수 1 model 호출 경계 + 권고 1 tool handler. session store는 `runtime → sessions` 허용이라 core 제외), `core/__init__.py` 선별 재수출 권고, 호환성 원칙 7개(선택적 값 추가와 새 판별값 추가를 구분), DEC-002 phase 매핑. 미결 8건 | - |
| KAG-DEC-004 | [process package 실행 격리 경계 — 파일·보안 불변식·실행 계약](decision-004-process-boundaries.md) | **proposed** (리뷰 대기) | KAG-BL-001 | 단일 runner module / 관심사별 평면 module / backend·플랫폼별 중첩 / `providers`로 접기 4안 비교 후 **평면 module 분리 권고**(단일 runner와 접기는 비권고, 중첩은 기각). process 소유 책임 8종(P1~P8)과 소유하지 않는 것 9종, **최소 보안 경계 13항목 판정**(argv 목록 실행 · shell 미개방 · 필수 cwd · stdin 비상속 · 환경 allowlist · 호출 단위 시간 상한 · 외부 취소 관찰 · stdout/stderr 분리 고정 · 종료 escalation · exit/신호 원시 보고 · 자식 그룹 회수 · 스트림별 byte 상한 · decode 경계)과 미지정 시 fail-closed 해석, 파일 후보 7개 + `__init__.py`(각 파일이 보안 항목을 명시적으로 소유. 개수 1:1은 아니다), process 내부 5단 총순서로 OS 의존을 한 파일에 모아 대체 지점을 안정된 import 경계로 둠, 실행 lifecycle 5국면 = 순차 4 + **동시 감독 구간 1**(stdin 전달 · 두 스트림 동시 drain · 시간 상한 · 취소 관찰 · 자식 종료 관찰이 spawn 직후부터 동시에 진행되고 먼저 발생한 종료 사건 하나가 구간을 끝낸다 — 순차로 쪼개면 멈춘 자식을 끊지 못하고 파이프 교착이 생긴다. 정리 없이 반환 없음 · 부분 출력 보존 + 불완전 표시), turn / provider 호출 / subprocess 실행 3층 책임 분리(process는 turn 종료 state도 provider 오류도 만들지 않는다)와 fail-closed 원칙 6개, KAG-DEC-002와 겹치지 않음의 항목별 확인, 최소 재수출 권고와 테스트 seam 4종, 관측·민감정보 원칙 7개. KAG-DEC-001 OQ-4(process 유지/접기)는 닫지 않음. 미결 10건 | - |

## 미결 사항

KAG-DEC-001이 다루기로 한 질문은 그 문서의 Open Questions 표가 owning view다. 아래에는 이 index가 추적할 항목만 요약하고 본문을 복사하지 않는다. 아직 어떤 decision에도 들어가지 않은 질문은 [KAG-BL-001의 Open Questions](../00-baseline/baseline-001-provider-neutral-llm-runtime.md#open-questions)에 남아 있다.

| ID | Question | Owner | Next |
|---|---|---|---|
| KAG-DEC-001 OQ-1 | PyPI 배포명을 import 이름과 같게 갈지 | 사용자 | 첫 배포 검토 시점 |
| KAG-DEC-001 OQ-3 | CLI·queue worker·web server를 언제·어디에 둘지 | 사용자 | 첫 vertical slice 이후 |
| KAG-DEC-001 OQ-8 | `products/open-kknaks/`와의 관계 | 사용자 | 별도 decision |
| (그 외) | KAG-DEC-001 OQ-2·4·5·6·7 | planner | [decision-001](decision-001-runtime-directory-boundaries.md#open-questions) 참조 |
| KAG-DEC-002 OQ-8 | 한 응답의 tool call 일부가 거부됐을 때 남은 호출을 계속 실행할지 | 사용자 | 첫 vertical slice 실행 결과 후 |
| (그 외) | KAG-DEC-002 OQ-1~7·9 (malformed repair, provider 재시도, 취소 전파, tool timeout, final 검증 기준, loop 방어, snapshot 기록, 공개 진입점) | planner | [decision-002](decision-002-turn-runtime-flow.md#open-questions) 참조 |
| KAG-DEC-003 OQ-1 | 재수출 이름의 안정 API 약속 수준과 버전 표기·deprecation | 사용자 | 첫 배포 검토 시점. KAG-DEC-001 OQ-1과 함께 |
| KAG-DEC-003 OQ-5 | `core/tooling.py` 이름이 형제 package `tools/`와 충분히 구분되는지 | 사용자 | 첫 파일 생성 직전 |
| (그 외) | KAG-DEC-003 OQ-2·3·4·6·7·8 (session event 저장 경계 형태 → `sessions` 상세 decision, turn 결과 타입 소유, package-root 재수출, evidence 계약, 신뢰 등급 부착 시점, tier 정적 검사) | planner | [decision-003](decision-003-core-contract-boundaries.md#open-questions) 참조 |
| KAG-DEC-004 OQ-4 | shell 실행 경로를 훗날 열 것인지와 그 조건 | 사용자 | 파이프라인이 실제로 필요한 사용처가 생긴 뒤. 그전까지는 열지 않는다 |
| KAG-DEC-004 OQ-10 | 종료 유예·출력 상한·시간 상한의 기본 수치를 라이브러리가 제안할지 | 사용자 | 첫 vertical slice 실행 결과 후 |
| (그 외) | KAG-DEC-004 OQ-1·2·3·5·6·7·8·9 (process 유지/접기 = KAG-DEC-001 OQ-4 유지, HTTP provider 공용 격리, 취소 전달 경로, `core` 참조 여부, 실패의 값/예외 표현, 호출 상한과 turn 상한의 관계, tier 정적 검사, 보안 항목 추가) | planner | [decision-004](decision-004-process-boundaries.md#open-questions) 참조 |
| (미착수) | tool/provider 공개 계약, Codex CLI 격리 옵션 등 | - | KAG-BL-001 Open Questions 참조 |

> KAG-DEC-001 OQ-2(공개 import 표면)는 KAG-DEC-003 §5.2에서 세 조각으로 쪼개졌다. (a) `core/__init__.py` 재수출은 KAG-DEC-003이 권고안으로 다루고, (b) package-root 재수출은 KAG-DEC-003 OQ-4로, (c) 안정 API 약속은 KAG-DEC-003 OQ-1로 이관 제안됐다. KAG-DEC-003이 확정되기 전까지 owning view는 여전히 [decision-001](decision-001-runtime-directory-boundaries.md#open-questions)이다.

## Next

KAG-DEC-001·KAG-DEC-002는 `accepted` 완료. 현재 게이트는 **KAG-DEC-003(core package 계약 경계)과 KAG-DEC-004(process package 실행 격리 경계)의 사용자 리뷰** 두 건이다. 공개 계약은 디렉터리 하나씩 의존 그래프 아래에서 위로 내려가고, 지금까지 raw 제안이 올라온 것은 `core`(L0)와 `process`(L1)다.

남은 raw 작성 순서는 **`providers` → `tools` → `sessions` → `skills` → `context` → `runtime`**이다. `providers`가 다음인 이유는 `core`와 `process` 둘 다 참조하는 유일한 package라 아래 둘이 정리된 직후가 가장 싸기 때문이고, `runtime`이 마지막인 이유는 나머지를 조립하는 자리이기 때문이다. spec은 그 뒤에 연다. 확정 전에는 spec·work·코드로 내려가지 않으며, KAG-DEC-005 이후의 ID를 미리 선점하지 않는다.
