# Decision Index

규칙: `para/projects/project.md`

> baseline을 제품에 어떻게 적용할지 판단한 결정 목록과 아직 풀어야 할 질문을 관리한다.

## 결정 로그

decision 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다.

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| DEC-001 | 인증·설정 정책 | proposed | BASE-001 | [decision-001-auth-settings.md](decision-001-auth-settings.md) | — |
| DEC-002 | 내 업무 정책 | proposed | BASE-002 | [decision-002-my-tasks.md](decision-002-my-tasks.md) | — |
| DEC-003 | 회의록 정책 | proposed | BASE-003 | [decision-003-meeting-notes.md](decision-003-meeting-notes.md) | — |
| DEC-004 | 문서함 정책 | proposed | BASE-004 | [decision-004-library.md](decision-004-library.md) | — |
| DEC-005 | 캘린더 정책 | proposed | BASE-005 | [decision-005-calendar.md](decision-005-calendar.md) | — |
| DEC-006 | 메시지함 정책 | proposed | BASE-006 | [decision-006-messages.md](decision-006-messages.md) | — |

## 미결 사항

spec으로 내리기 전에 판단해야 하는 질문을 적는다.

| ID | Question | Owner | Next |
|---|---|---|---|
| DEC-001/OQ-1~6 | 업무 설정 화면 시안 확정 · 복구 UI · 모달 2종+1280 · 저장 실패 표시 · 유지 체크 해석 · 디자인 정정 전파 | 사용자 | spec 전 (상세는 DEC-001) |
| DEC-002/OQ-1~5 | 완료 결과 입력 UI(완료 게이트 디자인 정정) · 칸반 DnD 규격 · 미설계 화면 6종 · 삭제 진입점/복구 · 취소 유형 표기 재확인 | 사용자 | spec 전 (상세는 DEC-002) |
| DEC-003/OQ-1~7 | AI 요약 탭 트리 렌더 · 「생성중」 상태 화면 · **WKWebView 마이크 스파이크(코디)** · Soniox 300분 초과 · 녹음 보존 기간 · 미설계 3종 · 통합 규칙 상세 | 사용자 / 코디 | spec 전 (상세는 DEC-003) |
| DEC-004/OQ-1~5 | 휴지통 화면 · **v2 안내 표시 공통 규격** · 폴더 삭제 정책 · 검색 범위 · 양방향 연결 카드 | 사용자 | spec 전 (상세는 DEC-004) |
| DEC-005/OQ-1~5 | 드래그 시각 규격 · 동적 유형 분포 카드 · 기간 일정 카운트 · 겹침 범위 재확인 · 뷰 라우트 | 사용자 | spec 전 (상세는 DEC-005) |
| DEC-006/OQ-1~2 | v1 빈 화면 규격 · 사이드바 메뉴 유지 여부 | 사용자 | spec 전 (상세는 DEC-006) |
