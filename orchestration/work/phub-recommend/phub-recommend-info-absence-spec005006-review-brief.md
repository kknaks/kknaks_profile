# [reviewer_doc] case3 정보 없음 정본 SPEC-005/006 개정 검수

너는 procedure-hub 문서 검수 워커다. Orca dispatch preamble의 Task·Dispatch ID와 완료 보고 명령을 우선한다. 이 브리프 한 장으로 작업한다.

## 1. 먼저 읽을 것

- 역할: `orchestration/roles/procedure-hub/reviewer/`의 `role.md`, `rules.md`, `skills.md`, `tools.md`, `workflow.md`
- 검수 대상: `orchestration/work/phub-recommend/SPEC-005.md`(새 0.3.9), `SPEC-006.md`(새 0.3.9)의 2026-11-02 case3 정보 없음 개정 절
- 기준: `info-absence-spec-proposal.md`, `review-info-absence-spec-proposal-v2.md`, `_RESUME.md` 11-01~02 결정, `info-absence-remediation-plan.md`
- 근거: ignored audit `reference/2026-10-30-hub-evals/build-out/info-absence-audit/root-cause-next.md`, `direct-fact-worktable.md`, `partial-claims-worktable.md`
- 코드 확인은 읽기 전용: `~/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend`, `~/orca/workspaces/clinic_chat/hub-evals`

## 2. 검수

두 SPEC의 신규 조항을 이전 정본·제안서·재검수 결과 및 코드 실물에 대조한다. 신규 T4 선택 관계 조회/전역 메모, page/more, 앱 수신 상태와 충분 종료, 예산(안전 8KB·일반 20KB·원문 15KB), 부분 답변, 회귀 관문의 005↔006 정합을 본다. 특히 현재 구현과 신규 계약을 혼동하지 않는지, 미결정이 WORK 구현을 막는지를 판정한다.

각 지적은 파일:줄과 반대 근거를 붙여 FAIL/WARN/PASS로 나눈다. 0.3.9 버전 부여와 이전판 의존 기록도 확인한다. 사용자의 제품 판단과 기술 설계 결정을 따로 모은다.

## 3. 허용 범위와 완료 기준

- 생성 허용: `orchestration/work/phub-recommend/review-info-absence-spec005006.md` 한 파일만.
- SPEC·제안서·외부 코드·DB·서버·평가 기록을 수정하지 않는다. 새 평가를 실행하지 않는다.
- 종합 판정과 구현 전 막는 항목을 맨 위에 둔다. 항목별 근거와 실제 읽은 버전·빌드·코드 commit을 적는다.
- 커밋·push·PR 하지 않는다. 완료 시 dispatch preamble에 따라 `worker_done`을 정확히 한 번 보내고 종료한다.
