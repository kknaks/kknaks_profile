# Decision Index

규칙: `rules/product-doc-pipeline.md`

> baseline을 제품에 어떻게 적용할지 판단한 결정 목록과 아직 풀어야 할 질문을 관리한다.

첫 decision인 KAG-DEC-001이 2026-08-08 사용자 확정으로 `accepted`가 됐다. 확정 범위는 디렉터리 구조와 의존 방향까지다.

두 번째 decision인 KAG-DEC-002(최소 headless turn runtime 동작 구조)는 2026-08-08 `proposed`로 올라와 **사용자 리뷰 대기 중**이다. 본문은 전부 권고안이며 확정 전에는 `accepted`로 올리지 않는다. 세 번째 decision(공개 계약 표면)은 아직 만들지 않는다 — 미래 decision ID를 미리 선점하지 않는다.

## 결정 로그

decision 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다.

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| KAG-DEC-001 | [Runtime 디렉터리 구조와 의존 경계](decision-001-runtime-directory-boundaries.md) | accepted | KAG-BL-001 | 책임별 package 채택 (flat / ports-adapters 기각). package 이름 `kknaks_agents`, 4단 의존 계층 확정 | - |
| KAG-DEC-002 | [최소 headless turn runtime 동작 구조](decision-002-turn-runtime-flow.md) | proposed | KAG-BL-001 | (권고안) 명시적 phase/state transition을 가진 deterministic turn loop 권고. 불투명 `run()` / middleware-hook pipeline 비권고. 진행 phase 9 + 종료 state 4, side effect 순서 불변식 3, tool call 직렬 실행, 종료 원인 10종의 terminal/recoverable 판정. `query/` 디렉터리 없이 `runtime`이 흡수. 미결 9건 | - |

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
| (미착수) | tool/provider 공개 계약, Codex CLI 격리 옵션 등 | - | KAG-BL-001 Open Questions 참조 |

## Next

KAG-DEC-001 `accepted` 완료. KAG-DEC-002는 `proposed` — **사용자 리뷰가 다음 게이트**다. 확정되면 그 위에 공개 계약(요청·응답·tool·event) decision을 열고, spec은 그 뒤에 연다. 확정 전에는 spec·work·코드로 내려가지 않는다.
