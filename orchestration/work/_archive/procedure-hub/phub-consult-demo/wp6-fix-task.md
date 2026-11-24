# [app] WP-6 검수 고침 (11-20)

너는 WP-6 을 한 앱 워커다. `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 검수 `$W/review-wp6.md`. 스펙 워커가 같은 판단을 0.2.8 로 옮기는 중. 커밋 0 · 서브에이전트 0 · 18222 손대지 마라 · 시험은 관련만.

## 코디 판단 (WP-6 검수 `review-wp6.md` · 11-20)
- **P1-1 (가)** — 프롬프트 보관본(`llm_user_message`)은 LLM 블록 사본이라 가격이 든다(공개 홈페이지 가격) · 스펙 JS6 에 한 줄 · 시험 범위 = `cart` · `rec` · `items` · `consult` 칸 가격 0.
- **S-1 (가) TP14 ⑥** — 규칙이 자동 넘어감(TP3 4 · 표지 없음)으로 new · LLM return + 유효 `to` · 이번 턴 조건 ⊆ 그 `to` 주제 저장 조건 → return(`to_from: llm`). 표지 new(TP3 3)는 규칙 그대로. 시험 둘(6 턴 꼴 → t1 · 반대 꼴 → new).
- **S-2** — pick 규칙 한 줄(시술 없는 「같이 받아도 / 함께 / 동시에」 = 대상 0 · topic continue · follow 안 채움) · LC9 · LC5 예외(같이 받기 표지 + 장바구니 진료항목 둘 이상 → 그 턴 블록에 장바구니 줄 + 쌍 줄 다시) · R10 문구 나눔(이름 없으면 장바구니 쌍 · 같은 시술이면 재시술 간격 · 이름 있으면 그 시술 pair) · 시험.
- P2-1 · P2-3: 검수 「고칠 방향」 대로 · P2-2 는 WP-7 e2e 에서 장부 크기 보고 · 다음 판 열린 것.

완료: 시험 통과 · **실물 6 턴 시나리오 다시**(빈 포트 · 같은 말) — 5 턴 답이 장바구니 쌍(입꼬리 코어톡스 + 하이톡스 재시술 간격)을 근거로 · 6 턴이 t1(보톡스 · 입꼬리 · 국산 7)로 되돌아감 · 스크린숏 `$W/wp6-shots/` 덮어쓰기 · 리포트 `$W/wp6-fix-report.md`(답 글 원문).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: WP-6 고침" --body "시험 / 6 턴"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app WP-6 고침 완료 — <한 줄>. 상세는 인박스." --enter
```
