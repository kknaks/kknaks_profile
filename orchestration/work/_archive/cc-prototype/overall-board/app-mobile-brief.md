# [mobile] 앱 WORK-009 — WP-APP1 → APP6 (iPhone 시뮬레이터 먼저)

너는 **cc-prototype `mobile` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/mobile/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라. 작업 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` — **`procedure/app/**` 만**.

## 계약 (SSOT)
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` **0.4.1** · `10-decision/decision-007-app-v2.md` · `30-work/work-009-app-v2.md`(내 WP 줄 · 병렬 · 주의)
- 웹 규칙: `20-spec/spec-005-reservation-board.md` 0.4.0 · `spec-003-procedure-board.md` 0.6.0 · KOS 근거 `orchestration/work/overall-board/app-kos-report.md` · `app-wp-kos-report.md`
- 결정: `orchestration/work/overall-board/_RESUME.md` §2 10-27 앱 줄 — **E2E 는 먼저 iPhone 시뮬레이터**
- 코드: `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` branch **`kknaksss/overall-board-2`**(최신 `95c64bc`)
- 앱 시안(배치 정본 · 로컬 · 실명 옮기지 마라): `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/design/Ceramique 모바일 v4.dc.html` · `태블릿 v4` · 흐름 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-27-cc-app/workflow-app.md` · 상태 이름 · 색 = **웹 2계층**(시안과 다르면 웹)

## 할 일 — WORK-009 줄 그대로, 차례로
APP1 새 틀(탭바 · 레일 · 공통 헤더 · 설정 · 첫 화면 예약 현황 · 역할 값) → APP2 웹 따라잡기(2계층 · 되돌리기 · 발음 · 순서) → APP3 예약 · 내원 현황 · 예약 상세(웹 API 그대로 · 수납 · 처방전 버튼 없음) → APP4 알림(둘만) · 상담사 푸시 받기 → APP5 문진 화면(잠금 · 언어 칩 · KOS 양식) → APP6 여권 스캔(가이드 · MRZ · 3번 실패 → 손 입력 · **법적 검토 주석**)
- back 은 **backend 워커가 병렬로** 만든다 — 아직 없는 API 는 가짜 응답으로 화면부터 · back 이 나오면 붙인다(`app-backend-report.md` 를 보라). 모양이 SPEC 과 다르면 멈추고 물어라
- **iPhone 시뮬레이터**로 확인: 화면마다 스크린샷 → `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-shots/APPn-*.png`. 카메라 없음 → APP6 은 손 입력 길 + 견본 MRZ 단위 시험 · 푸시는 `xcrun simctl push` 로 흉내
- 붙일 back = 임시 포트로 띄운 `procedure/back`(사용자 8700 금지) 또는 가짜

## 검증 · 금지
- WP 마다 `cd procedure/app && flutter analyze && flutter test` · 시뮬레이터 스크린샷
- 사용자 포트 · 프로세스 금지 · 실제 여권 · 사람 사진 금지(견본 · 지어낸 값) · public 누출 금지
- 보고서 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-mobile-report.md`

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** **커밋 · push · PR 금지**(코디가 한다).
- WP 하나 끝날 때마다 보고서에 절을 더하고 **아래 (2) 한 줄만** 보내 진행을 알린다. 전부 끝나면 (1) · (2) 둘 다.
```bash
# (1)
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_bc2a2f31-b834-4ae9-8321-ab989eb95662 --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "mobile 완료: <한 줄>" --body "보고서 경로 / 바뀐 파일 / 검증 수치 / 데모 흔적 / 미결"
# (2)
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] mobile — <WP · 한 줄>. 상세는 보고서." --enter
```
- 막히면: `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] mobile: <질문>" --enter`
