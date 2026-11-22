# [backend] 고침 2 — F1 검수 FAIL 1 · WARN 3 + 고침 1 남은 infra 시험

같은 워크트리 · 브리프 그대로. 최신 커밋 = 고침 1. ⚠ mobile 이 `app/` 에서 F2 작업 중 — `app/` 금지 · git 읽기만. 디스크가 지금 26GB 비었다(Docker 가능 · 빌드 산출물은 쓰고 지워라).

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-f1-report.md`:
- **FAIL-1** `DAY_FCM_SERVICE_ACCOUNT` — `scripts/deploy/configuration.py` `FORBIDDEN_CONFIG_KEYS` 에도(OPTIONAL_SECRETS 는 고침 1 에서 됨) · `scripts/devtools/environment.py` 로컬 외부연동 가드 · `deploy/local.env.example` · `compose.local.yaml` · 배포 문서(`docs/` 의 deployment) — APNs 키와 같은 꼴(값 없이)
- **W-1** `INVALID_ARGUMENT` 는 토큰 오류(`fieldViolations` field=`message.token`)일 때만 `token_removed`
- **W-2** OAuth 토큰 프로세스 캐시(만료 전 재사용) · 동시 발급 막기
- **W-3** fcm 기본 클라이언트를 bootstrap 에서 주입(apns 와 같은 꼴)
- 고침 1 남은 것: `scripts/test.sh -q backend/tests/day/notifications backend/tests/deploy` infra 재실행(로컬 테스트 스키마 · 사용자 day-local 건드리지 마라)

allowed_paths: `backend/day/adapters/fcm.py` · `backend/day/bootstrap/` · `services/push.py` · `services/notifications.py` · `scripts/deploy/configuration.py` · `scripts/devtools/environment.py` · `deploy/local.env.example` · `compose.local.yaml` · `docs/` 배포 문서 · 관련 테스트. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-fix2-report.md`. 완료 보고는 dispatch preamble 의 worker_done 그대로. 커밋 금지.
