# frontend 3판 수정 1 — code r3 W-1 · NOTE-6 · 사용자 화면

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-code-r3-report.md` W-1 · NOTE-6 을 읽어라.
1. **W-1** — 묶음 차례는 **back 응답 차례 그대로**(front 에서 다시 정렬하지 않는다 — 엑셀과 같은 차례). 「앞 달 결제 취소」 머리의 결제일 칸은 「시각 없음」 대신 「앞 달 결제 취소」 글자
2. **NOTE-6** — `isHidden` 이 itemsNowhere 수납을 숨기지 않게(back 과 같은 규칙 — itemsMissing · itemsNowhere 는 안 숨김)
3. **사용자 화면 경고** — Next dev 「1 Issue」 = `components/common/AppHeader.tsx:45` hydration mismatch(서버 · 클라이언트 렌더가 다름 — 시각 · 브라우저 값 등). 고치고 원인을 보고에
- 3800 · back 건드리지 마라 · `npx tsc --noEmit && npm run lint` · 원 브리프(WP-FE3) §9 두 채널 · subject 「frontend 3판 수정 1 완료」
