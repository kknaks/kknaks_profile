# [backend] merge-dev-3 — 코드 브랜치 ← origin/dev 한 번 더(+ migration 0029 겹침)

너는 day `backend` 워커다. 역할 · 방법 · 금지 · 보고 형식은 같은 폴더 `merge-dev-2-instructions.md` 를 그대로 잇는다(먼저 읽어라 · 지난 결과 `merge-dev-2-report.md`). 이번은 **코드 워크트리만**(스펙은 손대지 않음).

- 코드 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` · HEAD `716e89d6`(지난 합치기 커밋) · 대상 `origin/dev` `4ba07ffe`(10 커밋 · 다른 사람 작업 — #293 Charty 파트너 연동 · 고객 차트 · #294 CI 분리 · `65b2de5e` 예약 · 고객 메뉴 다시 엶 → **dev 그대로 받는다**)
- 충돌 3: `backend/day/services/reservation_detail.py` · `backend/day/static/day.css`(build-css.sh 재생성) · `backend/tests/migrations/test_alembic.py`. 자동 겹침(`emr/base.py` · `day.js` · `app.css` · `reservations_detail.html` · `test_screen_copy.py` · `test_constraints.py` · `test_deploy_contract.py` · 예약 픽스처)도 뜻을 열어 본다 — 특히 예약 상세 템플릿 · 서비스는 우리 [문진 QR] · [여권 스캔] · [태블릿에 보내기] · 고침 6 자리와 dev 고객 차트 변경이 둘 다 살아야 한다
- **migration 겹침(핵심)**: dev 에 `20261125_0029_partner_charty.py`(revision `0029_partner_charty` · down `0028_visit_discharge_reason`)가 들어왔다. 우리 `20261125_0029_display_questionnaire_kos.py` 도 0028 에서 갈라진다 → **우리 것을 0030 으로 옮긴다**(파일 이름 · revision id · down_revision = `0029_partner_charty`). 우리 것은 어디에도 배포 안 됨. dev 0029 는 손대지 마라. `alembic heads` = 1 · 빈 DB 에서 upgrade head → downgrade → upgrade 시험(test_alembic) 통과 · 두 migration 이 같은 표 · 이름 · enum 을 건드리지 않는지 확인
- 다른 곳에서 우리 revision id(`0029_display_questionnaire_kos`)를 문자열로 부르는 곳 전부 grep 해서 따라 바꾼다

## 방법 · 검증

`git merge --no-commit --no-ff origin/dev` → 충돌 풀기 → `git add`(MERGE_HEAD 로 둔다 · 커밋 · push · stash · reset 금지). `scripts/check.sh` 1회 전체 · 앱 `fvm flutter analyze` · `fvm flutter test`(dev 에 app 변경이 있을 때만). 로컬 스택(11040) · DB · 시뮬레이터 건드리지 마라 — 로컬 DB revision 바로잡기는 코디가 한다(리포트에 필요한 명령만 적어라).

## 보고

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/merge-dev-3-report.md`(충돌별 푼 방법 · migration 옮긴 내용 · dev 변경이 우리 기능에 주는 영향 · 시험 수치 · 로컬 DB 바로잡기 명령). 완료 = preamble `worker_done`(`--report-path`) + 직접 주입 `[worker_done] backend 완료: merge-dev-3 — <한 줄>. 상세는 인박스.`
