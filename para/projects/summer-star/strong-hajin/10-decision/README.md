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
| DEC-006 | [업무 상세 재설계](decision-006-task-detail.md) | proposed | BASE-005 | **결정 20건** · 뒤집힌 것 0건 · **연 미결 여섯은 2026-09-28 코디 판정으로 전부 닫힘** | SPEC-007 v0.2.0 |
| DEC-007 | [운영 첫 배포](decision-007-production-deploy.md) | accepted | 사용자 지시 · 배포 리포트 | **결정 11건** · 뒤집힌 것 1건(레지스트리 ~~kknaks~~→kknaksss) · 운영 가동 2026-10-01 | — (SPEC-006 OQ-T02·T03 일부를 닫음) |
| DEC-008 | [외부 채널 연동·메시지함·프로필 설정](decision-008-external-channels.md) | accepted | BASE-006 | **결정 50건** · 뒤집힌 것 3건(~~삭제~~→소프트 딜리트 · ~~사용자 테이블~~→별도 연동 테이블 · ~~서버 키·방 ID~~→로컬) · **미결 0건**(OQ-801~810 → D-41~D-50, 사용자 결정 2026-10-06) · 2단계(AX 판단) 미룸 | SPEC-008 · SPEC-009 |
| DEC-009 | [고도화 — 회의·회의록·AX·메시지함](decision-009-enhance.md) | accepted | BASE-008 | **결정 37건** · 뒤집힌 것 4건(DEC-008 hover 막대 없음 · 2단계 미룸 · 원격 이미지 · …) · OQ-901~909 사용자 결정으로 닫힘 · 019 보류 | SPEC-008 v0.6.0 · SPEC-010 |
| DEC-010 | [알림 — 사건×관계 · SSE · 사이드바 점 · 설정 · 셸 OS 알림](decision-010-notifications.md) | accepted | BASE-009 | **결정 41건** · 사건×관계 68행 사용자 확정 · 뒤집은 것 DEC-008 D-37(설정 알림 메뉴 범위 밖) · DEC-005 D-04 후속 · 열린 OQ 0 | SPEC-011 · SPEC-006 v0.7.0 · SPEC-008 v0.7.0 · SPEC-009 v0.6.0 |

## 미결 사항

spec으로 내리기 전에 판단해야 하는 질문을 적는다.

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ 목록 | [결정 초안의 Open Questions](decision-001-work-page.md#open-questions) | 코디·리뷰어 | 원문으로 해소 가능한 항목과 제품 결정 구분 |
| — | DEC-003 은 미결 **0건** — 조사 24건을 전부 닫았다 | — | 깔고 간 판단 둘은 [Open Questions 절](decision-003-calendar.md#open-questions)에 명시 |
| DEC-004 OQ-604·605 | [2루프가 연 미결](decision-004-projects.md) | 사용자 | 1루프 아홉 건은 2026-09-21 전부 닫혔다(그 경위는 「Open Questions」 절 · 철회한 제안은 「철회」 절). **2루프가 둘을 새로 열었고**, SPEC-005 가 연 둘(OQ-606 접근 값 이름 · OQ-607 `external_key` 노출)까지 합쳐 **미결 4건** |
| DEC-005 OQ-T01~06 | [데스크톱·배포 상세 미결](decision-005-tauri-wrapper.md#open-questions) | 사용자·코디 | OS 둘·Mac Studio·릴리즈 위치 확정. 최소 OS·아키텍처·도메인·서명 등 세부와 실측은 남음 |
| DEC-007 OQ-D7-01~06 | [운영 배포 후 남은 것](decision-007-production-deploy.md#open-questions) | 사용자·코디 | 로그인 시도 제한 · M-5 실기 확인 · 개인판 origin · 운영 DB 실명 정책 · 노드 codex · Releases 발행 |
| — | DEC-006 은 미결 **0건** — 연 여섯(OQ-701~706)이 2026-09-28 코디 판정으로 전부 닫혔다. SPEC-007 이 연 둘(707·708)도 같은 날 닫혔고, **열린 것은 SPEC-007 이 검수 반영에서 새로 연 OQ-709 하나**다 | 사용자 | OQ-709 — 못 읽는 선행만 남았을 때 `[시작]` 을 막을 것인가 |
