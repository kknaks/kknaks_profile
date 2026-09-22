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
| DEC-004 | [「프로젝트」 화면](decision-004-projects.md) | proposed | BASE-004 | **결정 39건** · **뒤집힌 것 둘**(~~D-12~~→D-28 · ~~D-31~~→D-39) | SPEC-005 v0.2.0 |
| DEC-005 | [Tauri 웹 래퍼·배포 방향](decision-005-tauri-wrapper.md) | accepted | 사용자 대화 · 참조 조사 | 방향 확정 · 상세 미결은 SPEC-006 참조 | SPEC-006 draft |

## 미결 사항

spec으로 내리기 전에 판단해야 하는 질문을 적는다.

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ 목록 | [결정 초안의 Open Questions](decision-001-work-page.md#open-questions) | 코디·리뷰어 | 원문으로 해소 가능한 항목과 제품 결정 구분 |
| — | DEC-003 은 미결 **0건** — 조사 24건을 전부 닫았다 | — | 깔고 간 판단 둘은 [Open Questions 절](decision-003-calendar.md#open-questions)에 명시 |
| DEC-004 OQ-604·605 | [2루프가 연 미결](decision-004-projects.md) | 사용자 | 1루프 아홉 건은 2026-09-21 전부 닫혔다(그 경위는 「Open Questions」 절 · 철회한 제안은 「철회」 절). **2루프가 둘을 새로 열었고**, SPEC-005 가 연 둘(OQ-606 접근 값 이름 · OQ-607 `external_key` 노출)까지 합쳐 **미결 4건** |
| DEC-005 OQ-T01~06 | [데스크톱·배포 상세 미결](decision-005-tauri-wrapper.md#open-questions) | 사용자·코디 | OS 둘·Mac Studio·릴리즈 위치 확정. 최소 OS·아키텍처·도메인·서명 등 세부와 실측은 남음 |
