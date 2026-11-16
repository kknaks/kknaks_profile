# [reviewer_doc] case3 정보 없음 계약 변경안 검수

너는 procedure-hub 문서 검수 워커다. Orca dispatch preamble의 Task·Dispatch ID와 완료 보고 명령을 우선한다. 이 브리프 한 장으로 작업한다.

## 1. 먼저 읽을 것

- 역할: `orchestration/roles/procedure-hub/reviewer/`의 `role.md`, `rules.md`, `skills.md`, `tools.md`, `workflow.md`
- 검수 대상: `orchestration/work/phub-recommend/info-absence-spec-proposal.md`
- 계약 정본: `orchestration/work/phub-recommend/SPEC-005.md`(0.3.5), `SPEC-006.md`(0.3.8), `_RESUME.md`의 2026-11-01~02 결정
- 근거: `orchestration/work/phub-recommend/info-absence-remediation-plan.md`, `reference/2026-10-30-hub-evals/build-out/info-absence-audit/root-cause-next.md`, `direct-fact-worktable.md`, `partial-claims-worktable.md`
- 코드 확인은 읽기 전용: `~/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend`, `~/orca/workspaces/clinic_chat/hub-evals`

## 2. 작업

변경안의 각 계약이 기존 005/006 및 실제 도구·앱 코드와 일치하는지 검수한다. 특히 관계 fact 읽기 경로(pair_check), node expand의 페이지·more 의미, 안전 8KB와 일반 20KB 및 원문 15KB의 예산 소유권, queue/enough 종료, 명시 비교 대상 resolve, 부분 답변의 근거 범위, 50문항 승격 관문을 본다.

각 지적에 **검수 대상 파일:줄 + 반대 근거 파일:줄/실행 기록**을 붙이고 FAIL/WARN/PASS를 판정한다. 구현 전 반드시 닫아야 할 열린 설계 결정과, 사용자가 판단해야 하는 제품 정책을 구분한다. 원장 문장을 근거 없이 일반화하거나 42개 미전달을 42문항 개선으로 읽지 않는다.

## 3. 산출물과 경계

- 생성 허용: `orchestration/work/phub-recommend/review-info-absence-spec-proposal.md` 한 파일만.
- 검수 대상·정본 스펙·코드·DB·서버는 수정하지 않는다. 새 평가를 실행하지 않는다.
- 보고서 맨 위에 종합 판정과 막는 항목을 요약한다. 문제가 없더라도 무엇을 대조했는지 적는다.
- 커밋·push·PR을 하지 않는다. 완료 시 dispatch preamble에 따라 `worker_done`을 정확히 한 번 보내고 종료한다.

## 4. 완료 기준

계약 항목별 검수, 근거 있는 판정, 열린 결정 목록, 실제 읽은 버전·빌드 표시가 모두 보고서에 있다.
