# [app] SPEC-010 WP-6 — LLM 블록 · 답 규칙 · 채팅 원리 그림 (11-20)

너는 WP-0 ~ WP-5 를 한 앱 워커다. `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · 정본 `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `$W/SPEC-010-consult-myeongdong.md` 0.2.7(§7 LLM 컨텍스트 · R1 ~ R11 · §4-4 채팅 원리 그림 · §13 WP-6 행 · 주제 TP7 · 장바구니 LC9 pair).

커밋 0 · push 0 · 서브에이전트 0 · 18222 손대지 마라(빈 포트 서버로 실물) · 시험은 `test_v05_llm_block.py` + 관련 0.4 만 · ruff 손댄 파일.

## 할 일
§13 WP-6 행 그대로: 턴 메시지 블록(조건 · 주제 · 진료항목 · 장바구니 · 같이 받기 `pair` 재료 · 경과 줄) · 답 규칙 초안 R1 ~ R11(프롬프트 `0.5.0-draft` — 허브 근거만 · 가격은 JSON 값만 · 확인 필요 진료항목 말하기 · 주제 바뀜 한 줄 · 국가 빠진 수) · 채팅 원리 그림 표지 줄 → 그림.
완료: 시험 통과 · 실물 한 턴 장부 `llm.kos_block` · 장바구니 둘 이상에서 `pair` 재료 줄 · **실물 대화 시나리오 한 번**(빈 포트 · 실제 이해 · 답 호출): 「보톡스 맞고 싶어요」 → 「입꼬리요」 → 「국산으로」 → 담기 · 옵션 → 「기미도 고민이에요」(새 주제) → 「같이 받아도 돼요?」 — 답 글 · 스크린숏 `$W/wp6-shots/`.
리포트 `$W/wp6-report.md`(답 글 원문 · 규칙 어긴 곳 있으면).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: WP-6" --body "파일 / 시험 / 시나리오"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app WP-6 완료 — <한 줄>. 상세는 인박스." --enter
```
