# [planner] Delivery(WP) 새로 — DAY 서버 배포(dev · prod 한 VM)

너는 day planner 다. 앞 Delivery 와 같은 방식(`start-delivery` · `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/delivery/`). CENTURION_DAY 새 Issue 하나 · **승인 안 함**. 레포 기본 브랜치는 이제 `dev`(2026-11-08 정리 — v2-dev 없음).
target: `products/day/40-architecture/deployment.md`(PR #909 커밋됨) — 아키텍처 문서라 SPEC 이 아니면 스킬이 허용하는 target 형식을 따른다.
계약에 넣을 것:
- 바뀌는 것: GitHub Actions(dev push → dev 배포 · prod fast-forward → prod 배포 · 롤백 수동 실행 · prod migration 따로 승인) · ACR 이미지(SHA) · VM 배포 스크립트(run-command · Key Vault → env 파일) · compose project 셋(day-edge Caddy · day-dev · day-prod · redis 환경마다 · 메모리 상한) · Caddyfile(`day-dev.medisolveai.com` · `day.medisolveai.com`) · **JSON 로그**(`app_env` 필드) · `APP_ENV` 필수화(배포 env) · offline SQL 등 앞 검수에서 넘긴 것(#225 W5/W8 · W7 키 canary) 중 배포에 필요한 것 · 레포 `AGENTS.md` 의 「v2-dev」 문구 고침.
- 재확인 검수의 가벼운 남은 것 3(`/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-deploy-arch-fix-report.md`: migration 이미지 SHA · 롤백 뒤 브랜치 · 브랜치 만들기/구현 줄)을 계약 문장으로 닫는다.
- 하지 않는 것: Azure 리소스 만들기(사용자 몫 — 목록만) · 운영 KOS 쓰기 켜기 · 앱 배포.
- Acceptance: 로컬에서 prod 모양 compose 로 두 환경 기동(포트 · 메모리 상한) · 워크플로 문법 검사(actionlint 등) · 스크립트 dry-run · JSON 로그 테스트 · **실제 Azure 배포는 사용자 준비 뒤**(그때 dev 1회 → prod 1회 실물).
- 담당: backend(인프라 파일 포함).
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-delivery-deploy-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
