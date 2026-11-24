# [planner] Delivery 발행 2 — spec-baseline:pending 으로 시작 · 승인 적용

사용자 결정(2026-11-23): **PR #958 은 머지하지 않는다.** SPEC-006 은 최초 스펙이라 main 에 아직 없다 → 네가 보고에서 「다른 길」로 적은 방식대로 **baseline = fetch 한 origin/main SHA + `spec-baseline:pending`** 으로 Delivery 3개를 시작한다(DAY 첫 Delivery #224 ~ #226 과 같은 방식 — 그 Issue 들을 참고해 request 꼴을 맞춘다). 사용자가 **Delivery 승인도 했다** → apply 뒤 승인 receipt 까지 적용한다.

읽을 것: 네 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery-1-report.md` · request `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery/request-*.json` · `rules/delivery-workflow.md` · `tools/harness/references/requests.md` (pending baseline 규칙 · 나중 재결속 절차)
문서 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` · 코드 워크트리(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation`

## 할 것
1. 세 request 를 pending baseline 방식으로 고쳐 `--plan` → `--apply` → 승인 receipt 적용(규칙이 요구하는 꼴대로 · 규칙이 막으면 우회하지 말고 출력 그대로 보고)
2. 본문에 SPEC 원천을 PR #958 커밋 `1870f68c`(브랜치 `kknaksss/day-reservation-spec`)로 밝히고, #958 머지 뒤 재결속이 필요하다는 것을 규칙대로 남긴다
3. `30-work.md` Spec Coverage 행 = Delivery 번호 · `log.md` 한 줄 — 커밋하지 마라(코디가 #958 에 얹는다)
4. json 은 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery/` 에 · 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery-2-report.md`(Issue 번호 · URL · baseline · 라벨 · 승인 상태 · 재결속 조건) · 완료 보고는 preamble 의 worker_done
금지: 코드 수정 · 커밋 · push · PR 머지 · SPEC 본문 계약 변경.
