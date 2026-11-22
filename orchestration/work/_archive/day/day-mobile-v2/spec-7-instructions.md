# [planner] 스펙 7차 — deployment.md 사실 정정 1줄

같은 워크트리 · git 쓰기 허용(커밋 1) · push 금지. HEAD bc3f9669 위에.

`products/day/40-architecture/deployment.md:240` 1행 「2026-11-20 그 dev 배포는 취소됨 · dev DB 는 0012」 는 낡았다. 사실(코디 확인 2026-11-20):
- run 44708143917 1차는 체크 단계에서 취소 · **2차(attempt 2) 성공** → dev 에 `5ece25ea` 배포 · dev `alembic current` = `0014_device_platform_android (head)` · api healthy.
- 그래서 「0012 만 올리면 `f724b149`」는 migrate-prod 의 조건(dev DB revision = 그 이미지 head)을 이제 못 맞춘다(dev DB 가 0014). prod 는 `5ece25ea`(0012 · 0013 · 0014 함께)로 올리는 것이 지금 조건에 맞는 길.
원문은 지우지 말고 취소선 + 「→ 2026-11-22 정정(day-mobile-v2): …」. 정책을 새로 정하지 말고 사실만.

lint --strict products/day ERROR 0 · 커밋 `docs(day): deployment 정정 — #266 dev 배포 2차 성공 · dev DB 0014`. 리포트 없이 worker_done 본문에 새 HEAD sha. 완료 보고는 dispatch preamble 의 worker_done 그대로.
