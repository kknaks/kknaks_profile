# [reviewer] #233 서버 배포 코드 검수
**읽기 전용** · 커밋 · 수정 금지. **사용자 로컬 compose(day-local · 11040 ~ 11043)를 내리지 마라.**
대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` 미커밋 diff(`git status` · `git diff` · 새 파일 전부). 계약 Issue #233 contract v2 · 정본 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/40-architecture/deployment.md` · 작성 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-233-report.md` · 본 centurion `git -C /Users/kknaks/git/centurion show origin/main:.github/workflows/deploy-stg.yaml` 등.
받은 실제 값(비밀 아님): `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/config/projects/day.json` `infra` — DB 공개 꺼짐(VM 경유) · TLS verify-full · 앱 계정 = 스키마 주인 · migration 도 앱 계정.
볼 것: 계약 Acceptance 전부 증거 · prod 같은 이미지(재빌드 없음 · fast-forward) · migration 순서(prod 승인 · dev revision 확인) · 롤백 · 동시 실행 묶음 · 비밀값 노출(로그 · 히스토리 · 저장소) · 실패 복구가 다른 환경을 안 건드림 · run-command 스크립트 크기 한도 · Key Vault 비밀 이름 · OIDC subject · DB TLS(verify-full · CA) 가 실제 DB 조건과 맞나 · 테스트 분리 규칙 · 앱 기능 변경 없음.
돌릴 것: `uv run pytest -m "not infra" -q` · ruff · shellcheck · actionlint(가능하면) · dry-run.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-233-code-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
