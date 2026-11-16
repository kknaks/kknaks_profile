# [frontend] 시술 현황 WORK-008 — WP-FE1 2계층 상태 · WP-FE2 드래그 놓기(W2) · WP-FE3 카드 한글 발음

너는 **cc-prototype `frontend` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/frontend/role.md`(+ 같은 폴더 rules · skills · tools · workflow)와 앞 판 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/overall-board-fe-brief.md`(금지 · 검증 규칙 — 보고 대상은 **아래가 맞다**)를 읽어라.

작업 워크트리(코드): `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` — branch **`kknaksss/overall-board-2`**(최신 `901267f`). **`procedure/front/**` 만**(back · app 금지 — back 변경 없는 판).

## 계약 (SSOT)
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` **0.6.0** — §5.12 · §5.14(대조표 ● 줄 전부) · §6.3 · §9 #27~#32 · 부록 K
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/30-work/work-008-procedure-board-v2.md` — WP-FE1 · FE2 · FE3 줄(대상 파일 · 완료 조건 · 검증)
- 색 원본 = 예약 현황 구현 `procedure/front/components/reservations/view.tsx`(`phaseStyle` 등 — **재사용**할 수 있으면 공용으로 빼되 예약 현황 화면 값은 바뀌면 안 된다)
- **화면 정본 = 지금 배포된 웹 구현**(D-60) — 시안 대조 하지 마라
- reviewer_doc 이 같은 SPEC 을 **병렬로 검수 중** — FAIL 이 나오면 코디가 추가 지시로 보낸다

## 할 일 — 한 워커가 차례로(FE1 → FE2 → FE3 · 같은 파일이라 나누지 않음)
1. **FE1 상태 2계층**: §5.14 대조표 ● 줄 전부 · ○ 줄은 그대로. DS(medikit) 컴포넌트만
2. **FE2 드래그 놓기**: 판(격자 영역) 안 어디에 놓든 마지막 미리보기 자리로 저장 · 판 밖 · Esc = 원래 순서 · 귀가 대기 카드 위 · 틈 · 빈 칸에서 미리보기 유지 · 시작 순서면 저장 없음. 실제 back(데모)으로 끌어 놓기 확인(임시 포트)
3. **FE3 한글 발음**: 이름 오른쪽 · 빈 값이면 요소 없음 · 한 줄 말줄임(발음 먼저) · `title` 전체
4. 스크린샷 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/fe-shots/v2-*.png`(FE1 카드 · 범례 · 시술 줄 · FE2 틈에 놓기 전후 · FE3 발음 있음 · 없음 · 긴 이름) — 실명 금지(가짜 보드 · 지어낸 값)

## 검증 · 금지
- `cd procedure/front && npx tsc --noEmit && npm run lint`(build 는 코디가) · **예약 현황 화면 값 무변경** 확인(한 장)
- 사용자 포트 3700 · 8700 · 그 프로세스 금지(임시 포트는 쓰고 정리) · 커밋 · push 금지 · public 누출 금지 · KOS 쓰기는 FE2 드래그 순서 저장(ccc DB 만 — KOS 반영 없음)뿐
- 보고서 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/procedure-fe-v2-report.md`(바뀐 파일 · 대조표 ● 줄마다 처리 · 검증 수치 · 미결)

## 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 과 다르면 preamble 쪽으로만.

- 커밋·push·PR 금지.

```bash
orca orchestration send \
  --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_40641f63-19f3-4448-80a2-31278568feeb \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "frontend 완료: <한 줄>" \
  --body "보고서 경로 / 바뀐 파일 / 검증 수치 / FAIL·WARN 또는 미결"

orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] frontend: <질문>" --enter`
