
# [planner] 시안 v1 검수 정정 — F-1·F-2 + W-1~W-6

너는 **mediness `planner` 워커**다. 시안 v1 라운드 검수의 FAIL 2건·WARN 6건을 정정한다 — 좁은 라운드다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/planner/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec` (미커밋 6파일 위에서 작업)

## SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/review-design-report.md` — **F-1·F-2·W-1~W-6 좌표·처분이 전부 있다. 이 문서가 발주의 전부다.**

## 해야 할 일

**F-1 (처분 ① 채택 — 코디 확정)**: spec-154:1639 치수표에서 상단 헤더·좌측 사이드바 항목을 **빼고** SPEC-220 링크만 남긴다 — 폭은 SPEC-220 소유(288 단일, 사용자 확정)라 여기 복제하지 않는다. 시안의 224 는 **규율 교정 항목**(⒜⒝⒞ 계열)에 「시안 224 → 계약은 SPEC-220 소유(288)」로 명시 추가.

**F-2 (리포트 처분대로)**: §4.19.10 `[⋯]` 계약 표에 **재배정** 행 추가(자격·리셋 의미는 §4.8·domains 링크), §4.19.9:2313·AC-3b:2592 열거를 **수정·재배정·취소·삭제 네 항목**으로 동기. 개정 흔적(취소선/노트) 남길 것.

**W-1~W-6**: 리포트 각 항목의 처분대로 — ①§4.19.9 와이어프레임 `메타 340` 잔존+⛔ 배너 ②SPEC-152 「단일 timeline」 활성 서술 크로스 스윕 ③WP-104 「메타 존 340px」 잔존 ④「지남 강조 금지」 WP-114·30-work.md 활성 잔존 ⑤AC-38/WP-130 P7 검증 Given 을 v1 보드에서 도달 가능하게 재서술 ⑥due 3자리 렌더 근거 명시.

**하지 말 것**: 위 좌표 밖 신규 개정 금지. 사용자 판정 6건·gap 판단은 검수 PASS — 건드리지 마라.

## 검증

```
cd /Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec && python3 scripts/lint-pipeline.py --strict
```
mediness ERROR 0 + 정정 후 `[⋯]` 열거·`340`·`224` grep 정합 수치 보고.

## 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "planner 시안 정정 완료: <한 줄>" \
  --body "F/W 별 정정 좌표 / grep 수치 / lint"

orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] planner 시안 정정 완료 — <한 줄>. 상세는 인박스." --enter
```
