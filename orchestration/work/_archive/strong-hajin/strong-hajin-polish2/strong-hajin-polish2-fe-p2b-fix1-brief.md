# [frontend] WORK-009 Phase 2b — 검수 WARN 재수정 (fix1)

앞 판 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-fe-p2b-brief.md` 의 규칙·allowed_paths·검증·완료 보고가 그대로다(subject 「frontend 완료: WORK-009 Phase 2b fix1」). 검수 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/review-fe-p2b-report.md` 를 전부 읽어라.
⚠ backend 워커가 같은 워크트리 `backend/` 에서 Phase 1 중 — `frontend/` 만.

## 고칠 것 (코디 판단)
1. **W1** 출처 줄 글자 계층 — `task-detail.css:109` 의 font-size 가 자식(배지·inline 링크·t-meta)에 닿게. 사실 줄(12px)과 같은 계층으로. DS 토큰·부품 크기 변형으로(새 모양 금지)
2. **W3** `CommandConfirmationForm.tsx:97` 네이티브 date 입력 — 업무 날짜를 받는 칸이면 DS `DateField`(`2026/10/06`)로. 같은 「네이티브 type=date」 를 **전부 grep** 해서 업무 날짜 칸이면 같이
3. **W4** 어순 통일 — 라벨이 붙는 업무 날짜 표시는 **「라벨 값」** 어순 하나(예: 「시작 2026/10/01」·「마감일 2026/10/06」). `labels.ts:1136-1137` · `WorkViews.tsx:153-155`·`:252-253` 출발점, 같은 패턴 전부
4. **W5** 만들기 창 「시작일」 하드코딩(`WorkModals.tsx:5369`·`:5378`) → `taskDateLabel.start` 상수. 미사용 상수가 남지 않게
5. **W2 는 하지 않는다** — `submitted_at`·`valid_until` 은 업무 날짜가 아니다(이번 범위 밖). 보고에 「범위 밖 유지」로만

검증: 직렬 vitest · tsc · build. ActionCenter 흔들림 1건은 단독 재실행으로 판정해 보고.
