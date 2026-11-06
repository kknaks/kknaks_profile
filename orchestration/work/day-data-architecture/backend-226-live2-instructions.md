# [backend] #226 fix1 뒤 실물 확인 1회 — KOS 데모 지점 · 조회만

너는 #226 을 구현한 day backend 워커다. 같은 워크트리 · 미커밋. **코드 · 테스트를 고치지 마라**(문제가 보이면 리포트만). KOS 쓰기 금지 · 데모 지점 키만 · 값 · 개인정보를 리포트에 남기지 마라 · 포트 11040 · 11042 · 11043 만 · 끝나면 `down`.

목적: fix1 W3 로 바뀐 경로(일정 회차 → 기준 정보 없으면 `needs_master` → 태스크가 기준 정보를 넣음)를 실물로 한 번 본다.
방법: 로컬 `day_dev` 를 건드리지 않게 **빈 스키마**(예: `DB_SCHEMA=day_livecheck` — dev 가드에 맞는 이름으로)에 migrate → 데모 연결 시드 → worker · scheduler 를 띄워 첫 일정 회차가 `needs_master` 를 내고 기준 정보가 들어온 뒤 일정 회차가 `done` 이 되는지 로그 · 건수로. 끝나면 그 스키마를 DROP.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-226-live2-report.md` — 순서 · 로그 줄(값 없이) · 테이블별 건수 · 잠금 skip 여부 · 이상. 완료는 preamble 의 worker_done 절차대로(둘 다).
