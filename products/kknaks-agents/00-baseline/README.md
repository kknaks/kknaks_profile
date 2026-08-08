# Baseline Index

규칙: `rules/product-doc-pipeline.md`

> 들어온 아이디어, 요구, 레퍼런스, 문제, 관찰의 목록과 상태를 관리한다. 결정 내용 본문은 `10-decision/`에 둔다.

## 아이디어 목록

baseline 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다.

| ID | Title | Source | Status | Decision | File |
|---|---|---|---|---|---|
| KAG-BL-001 | Provider-neutral LLM runtime 라이브러리 | REF-0007 설계 노트 + 운영 사례/clean-room 관찰 | accepted | KAG-DEC-001 (accepted) · KAG-DEC-002 (proposed) | [baseline-001-provider-neutral-llm-runtime.md](baseline-001-provider-neutral-llm-runtime.md) |

## Next

KAG-BL-001의 첫 decision인 KAG-DEC-001(디렉터리 구조와 의존 경계)이 2026-08-08 사용자 확정으로 `accepted`가 되어 baseline도 `accepted`다. 반영 범위는 디렉터리 구조와 의존 방향까지다.

두 번째 decision인 KAG-DEC-002(최소 headless turn runtime 동작 구조)는 `proposed`로 사용자 리뷰 대기 중이다. proposed인 동안 baseline 상태는 `accepted`를 유지한다. 나머지 계약·Open Questions는 이후 decision에서 하나씩 다룬다.
