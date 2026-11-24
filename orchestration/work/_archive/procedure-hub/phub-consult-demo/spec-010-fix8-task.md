# [spec] SPEC-010 고침 8 — 주제 판단 = 규칙 + 이해 호출(LLM) → 0.2.5 (사용자 결정 11-20)

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `$W/SPEC-010-consult-myeongdong.md` 0.2.4 → 0.2.5. 문서 1 개만 · 코드 · 데이터 수정 0 · 커밋 0 · 서브에이전트 0.

## 사용자 결정(11-20)
- 주제 판단은 **규칙(TP2 ~ TP5) + 이해 호출(①)의 판단**. **별도 LLM 호출 없음** — 0.4 의 ① understand(`--output-format json`) 출력 JSON 에 칸 `topic{move: continue · new · return, to: <주제 id 또는 null>}` 하나를 더한다(pick 판 `0.5.0-draft` · 프롬프트에 지금 주제 · 앞 주제 목록(id + 머리 조건 요약)을 넣음 · 규칙 몇 줄).
- **합치기:** 이해 호출 판단과 규칙(A · B 셈 · 표지)이 같으면 그대로. 다르면 **규칙을 따른다** · 장부 `consult.topic{llm_move, rule_move, used}` 표지. 단 「되돌림(return)」 의 **대상 주제 고르기**는 LLM 이 낸 `to` 를 쓴다(규칙 TP5 는 표지 낱말만 알고 어느 주제인지 모름) — `to` 가 없는 주제 id 면 규칙대로(가장 최근 앞 주제).
- 회귀: 0.4 이해 호출 시험 · pick 판 시험 · 장부 시험 목록을 WP-3 에. 시험 T 표에 「LLM new · 규칙 continue → 규칙」 · 「아까 그 볼 필러 말고 그 전에 얘기한 거 → LLM to 로 두 번째 앞 주제」 줄.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d630855d-4002-4ea8-94ec-00c387f4b872 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-010 0.2.5" --body "주제 판단 합치기"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] spec 고침 8 완료 — <한 줄>. 상세는 인박스." --enter
```
