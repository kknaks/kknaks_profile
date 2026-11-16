# [frontend] 앱 WORK-009 — WP-FE 웹 front 닿는 곳

너는 **cc-prototype `frontend` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/frontend/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라. 작업 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board`(branch `kknaksss/overall-board-2`) — **`procedure/front/**` 만**. mobile 워커가 같은 워크트리 `procedure/app/**` 를 병렬로 고친다 — 건드리지 마라.

## 계약
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` 0.4.1 **§6.17 · §3.4 · §5-3** · `30-work/work-009-app-v2.md` **WP-FE** 줄 · 구현 중 정해진 모양 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-spec-followups.md`(#1 띄우기 pending · claim 등)
- back 은 끝났다 — 실제 모양 = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-backend-report.md`(BE3 띄우기 · BE5 사진 열람 · 역할 `counselor`)
- 화면 정본 = 배포된 웹 구현(D-60) · DS(medikit) 컴포넌트만

## 할 일 — WP-FE 줄 그대로
예약 상세 [QR로 고객 입력 요청] QR 상자 · [태블릿에 띄우기] 기기 목록 · 상태 단계 · [스캔할 기기] 단계 · 사진 썸네일(`fetch` + Bearer → blob URL — 쿠키 없음) · 「{기기}에서 수신」 · KOS 사진 실패 · 역할 값 `counselor`
- 로컬 웹(임시 포트 · 실제 back 임시 포트)에서 띄우기 만들기 · 닫기 · 상태 단계 · 썸네일(가짜 사진) 스크린샷 → `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/fe-shots-reservation/app-fe-*.png` · 예약 현황 그 밖 화면 회귀 없음

## 검증 · 금지
- `cd procedure/front && npx tsc --noEmit && npm run lint` · 사용자 포트 3700 · 8700 금지 · 커밋 · push 금지 · 실제 신분증 · 사람 사진 금지
- 보고서 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-fe-report.md`

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_dedf7aba-d602-4430-b5ae-57f44396cef7 --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "frontend 완료: <한 줄>" --body "보고서 경로 / 바뀐 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
