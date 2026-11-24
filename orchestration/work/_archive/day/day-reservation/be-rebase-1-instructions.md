# [backend] rebase 1 — origin/dev 최신 위로 · migration 번호 이어 붙이기

너는 맥락이 없다고 생각하고 이 파일만 따른다. 코디가 코드를 커밋했다: `4b1d1662`(브랜치 `kknaksss/day-reservation` · 옛 base `5ece25ea`).
그 뒤 origin/dev 가 `a03b83a4`(#270 · 6커밋)로 나갔고, 여기에 `20261122_0015_chart_revision.py` · `20261122_0016_ticket_bundle_unknown_price.py` 가 들어왔다.

할 일
1. 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation` 에서 `git fetch origin dev` → `git rebase origin/dev`.
2. 충돌은 `backend/tests/migrations/test_alembic.py` · `scripts/frontend/package-lock.json` 두 곳(merge-tree 로 미리 봄). 양쪽 다 살린다. package-lock 은 package.json 을 합친 뒤 `npm install --package-lock-only`(scripts/frontend)로 다시 만든다.
3. 우리 migration 을 dev head 뒤로 옮긴다: `20261123_0015_reservation_permission.py` → revision `0017_reservation_permission`(파일 이름도 0017) · down_revision = dev 의 0016 revision 문자열 그대로. 이 revision 이름을 쓰는 곳을 **전부 grep** 해서 고친다(시험 · 다른 파일).
4. `alembic heads` 가 하나인지 확인.
5. 시험: 예약 관련 시험 전부 + `backend/tests/migrations` + `backend/tests/architecture` + node 시험(scripts/frontend). 전체 check.sh 는 안 돌린다.
6. rebase 결과는 **커밋 하나**로 둔다(squash 불필요 · 충돌 해결은 그 커밋에 담김). push 하지 않는다.

금지: 스택(포트 11040 · docker · .run) 건드리지 마라 · 재기동은 코디 · deploy/*.env 읽지도 출력하지도 마라 · push 금지.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/be-rebase-1-report.md`(새 HEAD sha · 충돌 처리 · 시험 결과 숫자) · preamble 의 worker_done.
