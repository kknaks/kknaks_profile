# [planner] deployment.md 검수 WARN 반영 — W1 ~ W4

너는 day planner 다. 미커밋 · 커밋 금지. 읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-deploy-arch-report.md` W1 ~ W4.
코디 결정(사용자 결정 「브랜치 dev/prod · prod 는 dev 에서 확인한 같은 이미지」를 지키는 방법 — 새 결정 아님):
- **W1** prod 는 **fast-forward 로만** 올린다(merge · squash 금지) — dev 에서 배포 · 확인한 commit 을 그대로 prod 로(`git push origin <sha>:prod` 또는 승격 워크플로). 브랜치 규칙으로 강제할지는 사용자 준비 목록에(GitHub 설정은 사용자 권한).
- **W2** 롤백 = 수동 실행 워크플로(환경 · 이전 성공 SHA 입력) → 그 이미지로 다시 배포. migration 은 되돌리지 않음(forward-only).
- **W3** prod 순서 = ① prod migration(따로 승인 실행 · dev 에 같은 revision 이 이미 적용됐는지 확인) ② prod 배포(head 확인만 · 다르면 중지). 그림 · 표를 이 순서로.
- **W4** 사용자 준비 목록에 GitHub 쪽: Environments(dev · prod) · OIDC federated credential(브랜치별) · Actions 변수/비밀(비밀값 자체는 Key Vault) · 브랜치 규칙(prod fast-forward · 누가 push).
log · lint. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-deploy-arch-fix-report.md`(짧게). 완료는 preamble 의 worker_done 절차대로(둘 다).
