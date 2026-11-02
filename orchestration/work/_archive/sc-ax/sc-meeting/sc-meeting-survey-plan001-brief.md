# [reviewer_code] 조사 2 — 업무 기획안 v1.2.0(plan-001 · screen-004, mediness 313ae36) ↔ 우리(SPEC-004·SPEC-001·코드) 차이 (읽기 전용)

너는 **sc-ax `reviewer_code` 워커**다. **조사만 한다 — 파일 수정·커밋·발주 금지.** 산출물은 리포트 하나.

## 대상

- **기획 정본(최신)**: mediness `origin/main` 커밋 **313ae36** 의 `products/sc-ax/00-planning/plans/plan-001-work-management.md` · `products/sc-ax/00-planning/screens/modules/screen-004-work-management.md`(v1.2.0). 읽는 법: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec` 에서 `git show 313ae36:<path>`(이미 fetch 됨. **pull·checkout 금지**). 직전 판 v1.0.1 은 `59cd713` 같은 경로 — 변경 이력 대조에 쓴다.
- **우리 쪽**: 같은 워크트리의 `products/sc-ax/20-spec/spec-004-meeting-note.md`(0.4.1, 특히 §8.1 Todo 8필드 · §9 승격=업무 요청 · MOD-101 prefill · §12 통보) · `products/sc-ax/20-spec/spec-001-*.md`(업무 모듈 계약 — 파일명 확인) · `30-work/work-004-*.md` · `work-006-*.md` · 코드 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD 1925a76) `frontend/src/WorkModals.tsx`(CreateWorkDrawer) · `frontend/src/meetings/MeetingDetailPage.tsx`(승격 이음매) · `backend/src/ax_workspace/modules/work/requests.py` · `platform/work_tasks.py`.

## 물음 (표로, 항목마다 「기획 v1.2.0 / 우리 / 차이 / 회의 기능 영향」)

1. **MOD-101 업무 만들기** — 칸·순서·이름(승인자·결과·자료·회신 대기 등 새 어휘)·필수 여부. 우리 승격 prefill(title·description·due·checklist, 담당 비움, 참석자 우선)이 v1.2.0 의 MOD-101 에 그대로 맞는가. 「수신함 [내 업무로] 가 업무 만들기 창을 열고 AI 가 뽑은 업무명을 사람이 고친다」 — 우리 승격 흐름과 같은 결인가, 다른가.
2. **상태·어휘 변화**(「나에게」 기준 · 회신 대기 · 승인자 · 결과 · 관리자/구성원 둘 · 메일·그룹웨어)가 SPEC-001 계약·work 모듈 코드(status enum·capability 이름·요청/수락 게이트)와 어디서 어긋나는가. 우리 D29(참석자 배정 예외)·D30(팀장 work_request.create)이 v1.2.0 권한 어휘(관리자·구성원)와 충돌하는가.
3. **업무 상세 구조**(값 없는 줄 안 세움 · 자료 한 구획 · 진행 기록 시간순) — 회의에서 만든 업무 요청이 상세에서 어떻게 보이는가(출처 두 열 `source_meeting_id/agenda_id` 를 어느 줄에 낼지).
4. **수신함(MOD-105)** — 회의 승격 요청이 수신함에 어떻게 서는가(카테고리·건수·읽음). 우리 SPEC-004 에 수신함 언급이 있는가.
5. **회의 목록/상세 화면정의서(screen-005)** 는 이번 개정에 포함됐는가(313ae36 에 변경 있나). 있으면 우리 `design/회의록.dc.html`·`회의실.dc.html`(정본 시안)과의 차이도 표로.
6. 기획자가 「확인 부탁」한 셋(① 나에게 기준 ② 승인 요청 별도 항목 데이터 구조 ③ 보낸 업무에서 회신 대기 제외)에 대해 **개발 관점의 사실**만(가능/불가/비용) — 결정은 코디.

## 산출물

`/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/survey-02-plan001-v120-report.md` — 요약 10줄 · 표 1~5 · 6 의 사실 · 「회의 기능이 바로 고쳐야 하는 것」/「SPEC-001 쪽 일」/「무관」 세 묶음.

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_9efe51f3-aec0-44b1-94ea-f86134b6ddea \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer_code 완료: 조사 2 plan-001 v1.2.0 차이" \
  --body "요약 / 바로 고칠 것 / SPEC-001 쪽 / 무관 / 확인 셋 사실"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] reviewer_code 완료 — 조사 2. 상세는 인박스." --enter
```
