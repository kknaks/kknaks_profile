# [backend] origin/dev(f724b149) 위로 rebase · migration 번호 0013 · 0014

같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · 브랜치 `kknaksss/day-mobile-v2`(origin 에 push 됨 `921d88cd` · 16커밋 · base 844eace4). 이번에는 **git 쓰기 허용**(rebase · commit) — 다른 워커 없음. **push 는 하지 마라**(코디가 force push).

## 할 것
1. `git fetch origin` → `git rebase origin/dev`(= `f724b149` · 다른 세션 #265 `0012_kos_keys` 들어옴). 충돌은 양쪽 의도를 살려 푼다(우리 쪽 기능 · 저쪽 기능 둘 다).
2. migration: `20261120_0012_doctor_call_cancel_kind.py` → **0013**(revision 이름 · 파일명 · down_revision = `0012_kos_keys` 의 revision) · `20261120_0013_device_platform_android.py` → **0014**(down_revision = 새 0013). 두 파일을 참조하는 시험(`tests/migrations/test_alembic.py` · `test_doctor_call_cancel_migration.py` · `test_device_platform_android_migration.py` 등)의 이름 · head 도 맞춤. alembic head 1개.
3. 번호를 바꾼 고침은 rebase 끝에 커밋 하나로(`chore(migrations): 0013 · 0014 로 — dev 0012_kos_keys 뒤`).
4. 검증: `scripts/check.sh --static` · 전체 격리 시험 1회 · migration 실제 PG up(0011→0012→0013→0014)/down/up · `cd app && flutter analyze && flutter test` 1회(rebase 로 app 이 바뀌지 않았어도).
5. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-rebase-report.md`: 새 HEAD sha · 충돌 파일과 푼 방법 · 시험 수치.

완료 보고는 dispatch preamble 의 worker_done 그대로.
