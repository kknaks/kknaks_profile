# Decision Index

규칙: `rules/product-doc-pipeline.md`

> baseline을 제품에 어떻게 적용할지 판단한 결정 목록과 아직 풀어야 할 질문을 관리한다.

첫 decision인 KAG-DEC-001이 2026-08-08 사용자 확정으로 `accepted`가 됐다. 확정 범위는 디렉터리 구조와 의존 방향까지이고, 동작 구조는 다음 decision이다. 미래 decision ID를 미리 선점하지 않으므로 다음 decision 문서는 아직 만들지 않는다.

## 결정 로그

decision 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다.

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| KAG-DEC-001 | [Runtime 디렉터리 구조와 의존 경계](decision-001-runtime-directory-boundaries.md) | accepted | KAG-BL-001 | 책임별 package 채택 (flat / ports-adapters 기각). package 이름 `kknaks_agents`, 4단 의존 계층 확정 | - |

## 미결 사항

KAG-DEC-001이 다루기로 한 질문은 그 문서의 Open Questions 표가 owning view다. 아래에는 이 index가 추적할 항목만 요약하고 본문을 복사하지 않는다. 아직 어떤 decision에도 들어가지 않은 질문은 [KAG-BL-001의 Open Questions](../00-baseline/baseline-001-provider-neutral-llm-runtime.md#open-questions)에 남아 있다.

| ID | Question | Owner | Next |
|---|---|---|---|
| KAG-DEC-001 OQ-1 | PyPI 배포명을 import 이름과 같게 갈지 | 사용자 | 첫 배포 검토 시점 |
| KAG-DEC-001 OQ-3 | CLI·queue worker·web server를 언제·어디에 둘지 | 사용자 | 첫 vertical slice 이후 |
| KAG-DEC-001 OQ-8 | `products/open-kknaks/`와의 관계 | 사용자 | 별도 decision |
| (그 외) | KAG-DEC-001 OQ-2·4·5·6·7 | planner | [decision-001](decision-001-runtime-directory-boundaries.md#open-questions) 참조 |
| (미착수) | turn 동작 구조, tool/provider 공개 계약, Codex CLI 격리 옵션 등 | - | KAG-BL-001 Open Questions 참조 |

## Next

KAG-DEC-001 `accepted` 완료. 다음은 동작 구조(turn 반복·종료 조건·tool 실행 되먹임)를 다루는 decision이며, 그 문서는 아직 만들지 않았다. spec은 그 decision이 확정된 뒤에 연다.
