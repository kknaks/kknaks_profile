# [backend] renumber-refs — 코드 주석 · 시험 설명의 옛 스펙 번호를 새 번호로

너는 day `backend` 워커다(역할 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/roles/day/backend/role.md`). 이번만 `app/` 도 건드린다(주석 · 시험 설명 한정).

## 배경

스펙을 main 과 합치며 우리 번호가 다시 매겨졌다(대응표 = `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/merge-dev-2-report.md` §4 · §6-1). 그런데 dev 에 머지된 우리 코드(#295 · CENTURION_DAY dev)는 옛 번호를 인용한다 — 같은 번호가 dev 코드(main 뜻)와 우리 코드(옛 뜻)에서 두 뜻으로 섞였다. **우리가 넣은 인용만** 새 번호로 바꾼다.

## 방법

1. 코드 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1`: `git fetch origin && git checkout -b kknaksss/spec-refs-re1 origin/dev`(지금 브랜치 `kknaksss/app-camera-copy-re1` 은 머지 끝남 · stash · reset 금지 — 워크트리가 깨끗한지 먼저 확인, 아니면 멈추고 보고)
2. 대상 = **우리 변경분이 넣은 줄만**: 우리 작업 커밋 범위 `55e60aa4..1142b480`(합치기 커밋의 dev 쪽 줄 제외 — `git log -p` / `git blame` 으로 우리 줄인지 확인). dev 사람들이 쓴 줄(main 뜻)은 손대지 마라
3. 대응표대로 바꾼다: SPEC-002 개정 ㉚→㉜ · OQ-99/100→119/120 · SPEC-003 개정 ㉑/㉒→㉒/㉓ · U-23~30→U-24~31 · OQ-A63~91→A67~95 · D-7/8→D-8/9 · SPEC-005 OQ-N21/22→N25/26 · SPEC-007 고침 5→6. **기계적 대체 금지 — 바꾸기 전에 그 줄이 어느 SPEC 의 번호인지 본다**(SPEC-002 ㉑ · ㉒ 처럼 안 바뀌는 것 있음 · merge-dev-2 §4 「일부러 안 바꾼 것」)
4. 주석 · docstring · 시험 이름 · 시험 설명 · `test_screen_copy.py` 의 인용 글만. **동작 · 화면 글자 · API · migration 변경 0**(diff 에 코드 줄이 섞이면 실패)

## 검증

`scripts/check.sh` 1회 · `cd app && fvm flutter analyze && fvm flutter test`. 바꾼 뒤 우리 줄에 옛 번호가 남았는지 grep 표. 로컬 스택(11040) · 시뮬레이터 · 실행 중 프로세스 건드리지 마라. 커밋 · push 금지(코디가 PR).

## 보고

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/renumber-refs-report.md` — 번호별 바꾼 수 · 파일 수 · 안 바꾼 것과 이유 · 시험 수치. 완료 = dispatch preamble 의 `worker_done`(`--report-path`) + 직접 주입 `[worker_done] backend 완료: renumber-refs — <한 줄>. 상세는 인박스.`
