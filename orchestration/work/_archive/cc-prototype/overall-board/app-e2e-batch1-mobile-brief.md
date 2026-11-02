# [mobile] 앱 실기기 E2E batch 1 수정

너는 **cc-prototype `mobile` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/mobile/role.md`(+ 같은 폴더 rules · skills · tools · workflow)와 앞 판 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-mobile-report.md`(앱 구조 · 결정)을 읽어라.

작업 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` — branch **`kknaksss/overall-board-3`** · **`procedure/app/**` 만**(backend · frontend 워커가 같은 워크트리에서 back · front 를 고친다).

**할 일 = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-e2e-batch1-instructions.md` 의 「mobile」 절 전부**(#1 installId · #2 첫 로그인 기기 이름 · #3 SSE display 열기 · #5 ccc 딥링크 · #6 AVCaptureSession 연속 MRZ 자동 촬영). 원천 `app-e2e-feedback-batch1.md` · 계약 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` 0.4.1. back 의 installId 모양은 backend 보고(`app-backend-report.md` 「E2E batch 1」 절)를 보고 맞춰라 — 아직 없으면 `installId` 이름으로 보내라.

## 검증 · 금지
- `cd procedure/app && /Users/kknaks/fvm/versions/3.44.8/bin/flutter analyze && /Users/kknaks/fvm/versions/3.44.8/bin/flutter test` · 시뮬레이터 스크린샷(가능한 것만 — 카메라 · 딥링크는 실기기) → `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-shots/B1-*.png`
- 커밋 · push · 업로드 금지 · 사용자 포트 금지 · 실제 여권 · 사람 사진 금지 · 보고서 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-mobile-report.md` 에 「E2E batch 1」 절

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_acf51458-c1c2-4889-afe4-076c1896fb9a --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "mobile 완료: E2E batch 1 <한 줄>" --body "보고서 경로 / 바뀐 파일 / 검증 수치 / 실기기에서 볼 것"
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] mobile 완료 — E2E batch 1 <한 줄>. 상세는 인박스." --enter
```
