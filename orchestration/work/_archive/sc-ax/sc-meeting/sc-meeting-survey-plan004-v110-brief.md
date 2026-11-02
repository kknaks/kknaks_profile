# [reviewer_code] 조사 3 — 회의 기획 v1.1.0(plan-004 · screen-005, mediness cbc9712) ↔ 우리(SPEC-004 0.4.2 · 시안 v3 · 코드) 차이 (읽기 전용)

너는 **sc-ax `reviewer_code` 워커**다. **조사만 한다 — 파일 수정·커밋·발주 금지.** 조사 2 는 313ae36 을 봤는데 그건 v1.0.0 이었다. **이번은 v1.1.0(9/10 회의 피드백 반영판, 현재 판)** 이다.

## 대상
- **기획 정본**: mediness `origin/main` — v1.0.0 `868ebaf`(#712) → v1.1.0 `cbc9712`(#715) 의 `products/sc-ax/00-planning/plans/plan-004-meeting-note.md` · `00-planning/screens/modules/screen-005-meeting-note.md`. 읽는 법: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec` 에서 `git show <sha>:<path>` · `git diff 868ebaf..cbc9712 -- <path>`(fetch 됨, **pull·checkout 금지**). 313ae36 도 사이에 있으니 `git log --oneline 868ebaf..cbc9712 -- products/sc-ax/00-planning` 으로 이력을 먼저 세워라.
- **우리**: 같은 워크트리 `20-spec/spec-004-meeting-note.md`(**0.4.2**) · `30-work/work-00{1,2,4,5,6,7}*.md` · 시안 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/design/회의록.dc.html`(v3) · `회의실.dc.html`(v2) · 리포트 `REPORT-회의록-v3.md`·`REPORT-회의실-v2.md` · 코드 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD 83e3d69, `frontend/src/meetings/*` · `backend/src/ax_workspace/modules/meetings/*`).

## 기획자가 말한 v1.0.0→v1.1.0 변경(대조 축 — 각각 「기획 v1.1.0 / 우리 / 차이 / 영향(문서·시안·코드 어디를 고쳐야) / 크기」)
1. 반복 예약 제외(세트로 잇기, 지난 회의 불러오면 일시 = 같은 요일 다음 날짜)
2. **회의록 본문이 항목 단위 — 항목마다 발화 시각 오른쪽, 누르면 그 발화로. 안건 단위 [근거 N] 제거** (우리 = 줄별 evidence 타임칩 벽시계 — 얼마나 같은가)
3. **상태 여섯 → 다섯(예정·진행 중·종료·실패·취소)** — 「정리 중」이 상태가 아니라 회의록 자리 로딩 (우리 D 결정 = 여섯, summarizing 상태·폴링·배지)
4. 회의 목록 「진행 중」 구획 맨 위(0건이면 없음) → 누르면 실시간 회의록
5. 메뉴 두 묶음(홈·업무·캘린더·회의·채팅·수신함 ｜ 진행 현황·자료)
6. 삭제 — 회의실 잡은 회의만 「예약도 취소할까요」, 안 잡은 회의는 확인 하나 (우리 라운드 1 = 「회의를 취소할까요?」[회의 취소] 하나 + WP-007 예약 동반 취소)
7. 공유 — 끝난 뒤에만 [공유] (우리 = 예정·진행 중에도 공유 가능, 시안 v2 가시성 표)
8. 자료 삭제 — 「예정」에서만 (우리 = in_progress 아니면 올린 사람이 뗌, can_detach)
9. 이름·문구 — 「생성」/「예약」 구분: [회의 생성]·[회의만 생성]/[회의실까지 예약] (우리 라운드 1 = [회의 생성] 하나 + 「회의실 선택 안 함」) · 「주제」→「회의명」 · 페이지 「회의 목록」→「회의」
10. 자료 미리보기 — 데모 PDF, 실사용 PDF·DOCX·XLSX·PPT, 조작 = 페이지 이동·확대·전체 화면 (우리 = PDF·MD, 드로어)
11. 기획자 확인 부탁 셋 — ① 반복 제외 ② 항목별 발화 시각(AI 정리가 항목 단위 + 발화 되짚기 = 우리 evidence 로 성립하는가) ③ **회의실 자동 대체**(거절 시 인원 맞는 가장 작은 방으로 대체·알림 — WP-007 계약에 없음) — 개발 관점 사실(가능/비용)만.
12. 위 목록에 없는데 diff 에 있는 변경 전부(요소·문구·상태 전이) — 표로.
13. 우리 §12 통보 R-1~R-45 중 이 판이 **받아들인 것 / 반대로 간 것 / 무응답** 세 묶음.

## 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/survey-03-plan004-v110-report.md` — 요약 10줄 · 축 1~13 표 · 「코디가 정해야 할 것」 목록(판단하지 말고 나열) · 「바로 고칠 것(문서/시안/코드)」 세 묶음.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_9efe51f3-aec0-44b1-94ea-f86134b6ddea \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer_code 완료: 조사 3 plan-004 v1.1.0 차이" \
  --body "요약 / 큰 충돌 / 받아들인 통보 / 코디 결정 목록"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] reviewer_code 완료 — 조사 3. 상세는 인박스." --enter
```
