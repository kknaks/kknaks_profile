# [frontend · 시안 r4b] 방 패널에 상담 결과 · 수납필요 · 미결제 금액 · [결제 완료]

r4 의 연속. 근거: SPEC-001 0.2.1 §0-a(`/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md`) · workflow.md 5단계(같은 프로필 워크트리 `reference/2026-10-12-cc-prototype/workflow.md`).

`Ceramique 현황판 v4` 방 패널(고객 있는 방)에:
1. **상담 결과 줄**: 상담 단계 완료 뒤 — 상담사 · 완료 시각 · [상담 내용 보기](환자 상세 상담 요약 · 오늘 오더로)
2. **상담사가 넣은 시술**: 상담 완료 때 동선에 「예정 · **수납필요**」 배지로 들어온다(시술 1장 = 1줄)
3. **미결제 금액** 줄: `미결제 금액 ₩ 1,280,000 (시술 3건)` + 옆에 **[결제 완료]** — 누르면 수납필요 배지가 사라지고 금액 0 · 줄 숨김(토스트 「결제 완료 · 시술권 연결」)
4. 상태 예시 2장(패널 props): 상담 직후(수납필요 3건 · 미결제) / 결제 완료 뒤
5. 직원 환자 상세(배정형 · 순회형)의 동선에도 「수납필요」 배지 같은 모양

샘플은 r4 와 같은 규칙(10-09 실데이터, 이름만 가짜). 금액은 대본 방문의 실제 결제 금액.
allowed: claude design 의 v4 · 네가 만든 직원 파일 수정 / 리포트 `design-r4b-report.md`(이 폴더). 코드 · 커밋 · KOS 금지.
완료 보고는 WP6 브리프 §5 두 명령 그대로(subject 「frontend(시안 r4b) 완료: …」, taskId/dispatchId 는 WP6 것 task_75dacb3b4227 / ctx_d2aa638cb84a).
6. **[초기화]** — 현황판 v4 헤더 오른쪽(SPEC §3 · §5.4, v3 에 없던 추가 요소). r4 에서 빠졌다
