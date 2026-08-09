# Baseline Index

규칙: `rules/product-doc-pipeline.md`

> 들어온 아이디어, 요구, 레퍼런스, 문제, 관찰의 목록과 상태를 관리한다. 결정 내용 본문은 `10-decision/`에 둔다.

## 아이디어 목록

baseline 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다.

| ID | Title | Source | Status | Decision | File |
|---|---|---|---|---|---|
| KAG-BL-001 | Provider-neutral LLM runtime 라이브러리 | REF-0007 설계 노트 + 운영 사례/clean-room 관찰 | accepted | KAG-DEC-001 (accepted) · KAG-DEC-002 (accepted) · KAG-DEC-003 (proposed) · KAG-DEC-004 (proposed) · KAG-DEC-005 (proposed) · KAG-DEC-006 (proposed) · KAG-DEC-007 (proposed) · KAG-DEC-008 (proposed) | [baseline-001-provider-neutral-llm-runtime.md](baseline-001-provider-neutral-llm-runtime.md) |

## Next

KAG-BL-001의 첫 decision인 KAG-DEC-001(디렉터리 구조와 의존 경계)이 2026-08-08 사용자 확정으로 `accepted`가 되어 baseline도 `accepted`다.

두 번째 decision인 KAG-DEC-002(최소 headless turn runtime 동작 구조)도 2026-08-08 사용자 확정으로 `accepted`가 됐다. 반영 범위는 디렉터리 구조와 의존 방향에 더해 **한 turn의 동작 순서(phase 전이·side effect 순서·종료 조건)**까지다.

세 번째 decision인 KAG-DEC-003(core package 계약 경계), 네 번째 decision인 KAG-DEC-004(process package 실행 격리 경계), 다섯 번째 decision인 KAG-DEC-005(providers package 변환 경계), 여섯 번째 decision인 KAG-DEC-006(tools package 등록·허용·검증·실행 경계), 일곱 번째 decision인 KAG-DEC-007(sessions package event 저장·조회 경계), 여덟 번째 decision인 KAG-DEC-008(skills package 등록·선택·prompt 투영 경계)은 여섯 다 2026-08-09 `proposed`로 리뷰 대기 중이다. 확정 전이므로 baseline의 반영 범위는 아직 넓어지지 않았고 상태도 `accepted` 그대로다. KAG-DEC-007이 “session 원본과 model context의 분리” 중 원본 쪽 절반을 제안했으므로 나머지 절반(투영·compaction)은 `context` 상세 decision에 남는다. KAG-DEC-008은 skills를 최소 runtime의 필수 요소로 바꾸지 않고 **추후 조립 가능한 독립 확장 모듈**이라는 분류를 유지했으며, skill 선택 주체를 묻는 Open Question 7은 풀지 않았다. 나머지 계약·Open Questions는 이후 decision에서 package 하나씩 다룬다 — 남은 순서는 `context` → `runtime`이다.
