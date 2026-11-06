# [reviewer · 문서] DAY-SPEC-002 시술 현황(1차) 검수

너는 day reviewer 워커(문서 검수)다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/reviewer/`. **읽기 전용** — 파일 수정 · 커밋 금지. 산출물은 리포트 1개.
검수 대상: `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/20-spec/spec-002-procedure-board.md`(새 파일) + 같은 워크트리의 SPEC-000 · 20-spec.md · 30-work.md · log.md 변경(`git -C /Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec diff`).

## 기준 (위가 이긴다)

1. 사용자 결정 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md` — U1 ~ U12 · 「다음 스펙으로」(U5 · U11 범위 밖) · 추정 금지 7
2. 시안(생김새) `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html` · 요소 번호 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-ds-research-report.md`
3. cc 기존 로직 `/Users/kknaks/git/toy_pr2/kknaks_profile/para/projects/summer-star/cc-prototype/10-decision/decision-005-procedure-board.md` · `/Users/kknaks/git/toy_pr2/kknaks_profile/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-10-12-cc-prototype/workflow-v2.md`
4. 앞 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-screen-procedure-report.md` · 작성 지시 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec002-instructions.md` · 작성 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec002-report.md`
5. DAY 기존 계약 SPEC-000 · SPEC-001 · `40-architecture/system.md` · `code-structure.md`
6. KOS 쓰기 근거 HAR(main 체크아웃 · gitignore) `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-12-cc-prototype/*.har` — 경로 · 요청 칸 이름만 대조, 값은 옮기지 마라

## 볼 것

1. **결정 U1 ~ U12 가 빠짐없이 · 바뀌지 않고 들어갔나** — 특히 U2(cc 팝오버) · U3(새 행 + 기존 호출 닫음) · U4(남기는 건 수락한 의사만) · U6(카드 생성 순 + D&D · 빈 방 안 보임) · U12(마취 · 호출만). 범위 밖(U5 · U11 · 앱)이 새어 들어왔나.
2. **발명** — 정본에 없는 동작 · 칸 · 값 · KOS 요청 모양. 작성 리포트가 「브리프 범위 목록에 없던 시작/완료 취소를 시안 E50 · cc §5.13 근거로 넣었다」고 한다 — 근거가 맞는지 판정.
3. **KOS 쓰기 표** — 「HAR 확인됨」이라 적은 것이 실제 HAR 경로 · 요청 칸과 맞나, 확인 안 된 것이 OQ 로 갔나.
4. **SPEC-001 과 충돌** — 작성 리포트 OQ-05(수락 시 KOS 토큰 — U4 대리 수락 vs SPEC-001 규칙 4) 같은 것 · 오류 코드 · 권한 · CSRF.
5. **SPEC-000 변경** — `doctor_call.closed_at` 이 U3 를 담는지, 다른 표와 맞는지.
6. **작성 리포트의 사용자 결정 OQ 8건** — 각각 정말 사용자 몫인가(원천 · cc 로 이미 답이 있는 것은 「답 있음」으로), 추천이 근거에 맞나.
7. 케이스 매트릭스 · 상태 전이의 빈칸 · 모순. 「조용히 통과」(문서상 정해진 것 같지만 구현자가 고르게 되는 자리).

가상 시나리오로 실패를 세지 마라 — 지금 원천이 말하는 것만.

## 보고

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec002-report.md` — 판정(PASS · WARN · FAIL) · 지적마다 SPEC 줄 + 근거(원천 파일:줄 / HAR 경로) + 고칠 방향 · OQ 8건 판정표(사용자 몫 / 답 있음 + 그 답). 완료는 preamble 의 worker_done 절차대로(`orca orchestration send` 와 `orca terminal send` 둘 다).
