# [frontend] main 머지 뒤 전체 vitest 실패 16건 정리(머지 전 스위트 녹색)

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD ec9946b, main 머지됨). `frontend/` 만. 커밋 금지. dev 서버·5176 금지. **이번엔 vitest 돌려라** — 목표는 `npx vitest run` 전체 녹색 + `npx tsc --noEmit` 0.

## 실패 목록(16) — 전체 출력 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/fe-fail-merge.log`
- ActionCenter.test.tsx 3 · ActionMeetingCard.test.tsx 4 · ActionTaskCard.test.tsx 4 · App.test.tsx 3 (「creates a work request through the UI…」·「clears a stale report error…」·「ignores a late same-id list snapshot…」) · meetings/MeetingDetail.test.tsx 1(「[업무 생성]은 업무 요청 모달을…」) · meetings/MeetingList.test.tsx 1(「포커스는 칸 모양을 바꾸지 않는다」).

## 원칙
1. **제품 결정이 정본, 테스트가 따라온다.** DateField 는 입력칸 없이 우리 DatePicker 팝오버 하나(DS-17, 사용자 결정) — main 의 AX 카드·ActionCenter·App 테스트가 `input` 에 타이핑하거나 `2026.09.10` 표기를 입력값으로 기대하면 **테스트를 새 상호작용(트리거 클릭 → 날짜 클릭, 또는 컴포넌트 onChange)으로 고친다.** DateField 에 타이핑을 되살리지 마라.
2. 단, 테스트가 드러내는 **실제 회귀**(우리 화면이 깨진 것)는 코드를 고친다 — 어느 쪽인지 건별로 보고에 적어라.
3. MeetingList 「포커스는 칸 모양을 바꾸지 않는다」: main 이 가져온 `.ax-follow-up-candidate:hover…{border-color:var(--accent|--action)}` 규칙이 걸린 것으로 보인다. 그 테스트는 **포커스** 규칙만 보라는 뜻이니 hover 규칙은 통과하게(선택자 필터를 :focus 계열로 좁힘) — 전역 포커스 링 없음 규칙(사용자 결정) 자체는 그대로.
4. MeetingDetail 「[업무 생성]은 업무 요청 모달을…」: 드로어 이름 「업무 요청」(D10)·DateField 새 모양에 맞춘다.
5. ActionMeetingCard/ActionTaskCard 는 main 의 화면이다 — 카드 자체의 동작(점 표기 2026.09.10 · 초기화 아이콘 · 필수 기한)이 DateField 프롭(displaySeparator·pickerIcon·required)으로 살아 있는지 확인하고, 안 살아 있으면 카드 쪽을 고쳐라.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 머지 뒤 스위트 녹색" \
  --body "건별 테스트 수정/코드 수정 구분 / vitest 전체 수치 / tsc / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — 스위트 녹색. 상세는 인박스." --enter
```
