# frontend code r4 수정 — W-4

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-code-r4-report.md` W-4: `KeyBy` 에 `product_title` 추가(back schemas 와 같게) · 표시는 `product` 와 같게. 그리고 back 이 상품 받기 응답 · 설정 응답에 `rekeyedItems` · `carriedRates` · `conflicts` 수를 더한다 — 설정 화면 [KOS 상품 다시 받기] 뒤 「키 바뀐 줄 n · 비율 옮김 m · 충돌 k」 한 줄(0 이면 안 보임). back schemas 를 정본으로 맞춰라(BE 가 병렬로 고침 — 이름이 다르면 back 을 따름).
`npx tsc --noEmit && npm run lint` · 3800 · back 건드리지 마라 · WP-FE4 브리프 §9 두 채널(같은 task/dispatch) · subject 「frontend code r4 수정 완료」
