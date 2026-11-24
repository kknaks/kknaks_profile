# [spec] SPEC-010 고침 11 — WP-6 검수 반영 → 0.2.8 (11-20)

너는 SPEC-010 고침 10 을 한 스펙 워커다. `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 검수 `$W/review-wp6.md` · 아래 코디 판단을 `$W/SPEC-010-consult-myeongdong.md` 에 반영해 0.2.8(변경 기록). 앞 검수 남은 것도 같이: D1(LS 로 막은 칸 값은 주제 칸에서 빼고 장부 blocked 에만 — `$W/wp3b-report.md`) · WP-5 검수 P2-3(RC10 문구 — `$W/review-wp5.md`). 문서 1 개만 · 코드 수정 0 · 커밋 0 · 서브에이전트 0. 앱 워커가 같은 판단으로 코드를 고치는 중이다.

## 코디 판단 (WP-6 검수 `review-wp6.md` · 11-20)
- **P1-1 (가)** — 프롬프트 보관본(`llm_user_message`)은 LLM 블록 사본이라 가격이 든다(공개 홈페이지 가격) · 스펙 JS6 에 한 줄 · 시험 범위 = `cart` · `rec` · `items` · `consult` 칸 가격 0.
- **S-1 (가) TP14 ⑥** — 규칙이 자동 넘어감(TP3 4 · 표지 없음)으로 new · LLM return + 유효 `to` · 이번 턴 조건 ⊆ 그 `to` 주제 저장 조건 → return(`to_from: llm`). 표지 new(TP3 3)는 규칙 그대로. 시험 둘(6 턴 꼴 → t1 · 반대 꼴 → new).
- **S-2** — pick 규칙 한 줄(시술 없는 「같이 받아도 / 함께 / 동시에」 = 대상 0 · topic continue · follow 안 채움) · LC9 · LC5 예외(같이 받기 표지 + 장바구니 진료항목 둘 이상 → 그 턴 블록에 장바구니 줄 + 쌍 줄 다시) · R10 문구 나눔(이름 없으면 장바구니 쌍 · 같은 시술이면 재시술 간격 · 이름 있으면 그 시술 pair) · 시험.
- P2-1 · P2-3: 검수 「고칠 방향」 대로 · P2-2 는 WP-7 e2e 에서 장부 크기 보고 · 다음 판 열린 것.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_3d139262-8d63-4045-acb8-cbe37d8d96cb --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-010 0.2.8" --body "반영"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] spec 고침 11 완료 — <한 줄>. 상세는 인박스." --enter
```
