# [planner] Delivery #256 마감 — v2 재결속 · 사용자 승인 receipt · 마감 댓글 · 닫기

너는 앞 맥락이 없다. day planner 역할(`/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/roles/day/planner/role.md` + 같은 폴더)로 일한다. 작업은 끝났다(코드 CENTURION_DAY#257 머지 `a6aa4ba5` · 스펙 mediness#946 머지 `51f85837` · dev 배포 성공). Delivery Issue 만 정리한다.

## 읽을 것
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/` — `_RESUME.md` §2 결정 · `spec-report.md` ~ `spec-4-report.md` · `review-doc-1-report.md` · `review-code-1-report.md`
- v1 요청 · 결과: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/delivery/ksl.v1.*` · Issue `gh issue view 256 -R MediSolveAIDev/CENTURION_DAY`
- 앞 사례(같은 절차): `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/_archive/day/fix-feedback/delivery-close-instructions.md` · `delivery-close-report.md` · `delivery/fb.v2.*`
- 절차: mediness `.claude/skills/start-delivery/SKILL.md` · `tools/harness/references/requests.md`

## 워크트리(전용 · detached · 수정 금지 · CLI 실행만)
- mediness `/Users/kknaks/orca/workspaces/mediness-mediness/kos-signin-limit-delivery` = origin/main `51f85837c11a4c9904a04d6f27da4dc129fe844b`
- 코드 `/Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit-delivery` = origin/dev `a6aa4ba5`

## 할 일
1. v2 요청 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/delivery/ksl.v2.request.json` — 같은 key · contract_version 2 · baseline = 위 full SHA · 결과 계약을 최종 결정으로(K-1 ~ K-5 · 앱 = 지금과 같은 401 invalid_credentials · 시스템 = 가장 오래된 1개 · 기기 선택 웹만 · 「처음으로」 없음 + 같은 PR 의 SPEC-002 ㉓ 화면 변경 — 차트 영역 · 탭 글자) · `scope_delta` 사유 필수 · execution 은 실제 머지된 코드 기준.
2. `--plan` → `--apply`(fb 사례와 같은 CLI 실행 방식) · 새 plan_digest.
3. 승인 receipt — 사용자(GitHub `kknaksss`)가 2026-11-17 코디 대화에서 「회고 개념 정리 다 정리하고 스쿼시 머지 하자」로 이 작업 전체 정리를 지시했고, 로컬에서 직접 확인했다. `ksl.v2.approval-receipt.json` = `{"decision":"approved","reviewer_type":"human","reviewer":"kknaksss","plan_digest":"<새 digest>"}` → `--plan-approval-receipt` 로 plan → apply.
4. 마감 댓글(무엇이 들어갔나 · 검증 · 남은 것 = prod 배포 20시 · 앱 기기 선택 다음 버전 · 배포 뒤 표시 없는 시스템 세션 정리) → `gh issue close 256`(spec-sync 는 #749 제약 — 댓글 + close).
5. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/delivery-close-report.md`. 완료 보고는 preamble 의 worker_done.

## 하지 말 것
- 워크트리 파일 수정 · 커밋 · push · PR · 비밀값 · 이메일 · IP 출력.
