# Decision Index

규칙: `para/projects/project.md`

> baseline을 제품에 어떻게 적용할지 판단한 결정 목록과 아직 풀어야 할 질문을 관리한다.

## 결정 로그

decision 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다.

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| DEC-001 | 인증·설정 정책 | proposed | BASE-001 | [decision-001-auth-settings.md](decision-001-auth-settings.md) | — |
| DEC-002 | 내 업무 정책 | proposed | BASE-002 | [decision-002-my-tasks.md](decision-002-my-tasks.md) | — |

## 미결 사항

spec으로 내리기 전에 판단해야 하는 질문을 적는다.

| ID | Question | Owner | Next |
|---|---|---|---|
| DEC-001/OQ-1~6 | 업무 설정 화면 시안 확정 · 복구 UI · 모달 2종+1280 · 저장 실패 표시 · 유지 체크 해석 · 디자인 정정 전파 | 사용자 | spec 전 (상세는 DEC-001) |
| DEC-002/OQ-1~5 | 완료 결과 입력 UI(완료 게이트 디자인 정정) · 칸반 DnD 규격 · 미설계 화면 6종 · 삭제 진입점/복구 · 취소 유형 표기 재확인 | 사용자 | spec 전 (상세는 DEC-002) |
