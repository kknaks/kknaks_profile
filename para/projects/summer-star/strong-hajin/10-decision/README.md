# Decision Index

규칙: `para/projects/project.md`

> baseline을 제품에 어떻게 적용할지 판단한 결정 목록과 아직 풀어야 할 질문을 관리한다.

## 결정 로그

decision 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다.

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| DEC-001 | [업무 페이지 적용](decision-001-work-page.md) | proposed | BASE-001 | 검수 중 | SPEC-001 · SPEC-002 |
| DEC-002 | [업무 v2·프론트 적용](decision-002-task-lifecycle-v2.md) | proposed | BASE-002 | 스펙 검수 후 계획 검수 중 | SPEC-003 |
| DEC-003 | [캘린더 시간 배정](decision-003-calendar.md) | proposed | BASE-003 | 미결 0건 · 사용자 리뷰 대기 | SPEC-004 (예정) |

## 미결 사항

spec으로 내리기 전에 판단해야 하는 질문을 적는다.

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ 목록 | [결정 초안의 Open Questions](decision-001-work-page.md#open-questions) | 코디·리뷰어 | 원문으로 해소 가능한 항목과 제품 결정 구분 |
| — | DEC-003 은 미결 **0건** — 조사 24건을 전부 닫았다 | — | 깔고 간 판단 둘은 [Open Questions 절](decision-003-calendar.md#open-questions)에 명시 |
