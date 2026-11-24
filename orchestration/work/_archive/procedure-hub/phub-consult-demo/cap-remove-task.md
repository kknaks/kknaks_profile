# [code] 고정 한도 없애기 — LLM 에 넘기는 · 답이 말하는 양을 숫자로 자르지 않는다 (사용자 지시 11-23)

앞 발주 `fetch-plan-code-task.md` 규칙 그대로(앱 워크트리만 · 커밋 0 · 18222 · 18105 손대지 마라 · 실물은 빈 포트 · 키 출력 0 · 관련 시험 · 전체는 마지막 한 번). `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`

## 사용자 결정(다시 묻지 마라)
**출력 · 재료에 고정 한도를 두지 않는다**(「턴당 상한 고정 금지」 · 「출력 줄이지 않는다」 — 11-23 · 두 번 말함). 지금 문제: 명동점 진료항목을 LLM 에 앞 30 개만 넘겨(`chat_kos_llm_items_max = 30` · `kos_block.py:138` · `cond_view` `list_codes[:items_max]`) 73bd T2 에서 화면 목록 85 개 중 입꼬리 필러가 빠지고 답이 「짚어 드리기 어려워요」. 크기는 **기록만**(장부) — 자르지 않는다. 양을 줄이는 건 「무엇을 싣나」(fetch · 이름만 · 옵션은 필요한 턴만)로만.

## 할 일
1. **전수**: 상담 경로(`clinic_chat/consult/*` · `config.py` · `llm/*` · `prompts/consult.json`)에서 숫자로 자르는 곳을 grep 으로 전부 — `*_max` · `*_MAX` · `[:n]` · `한도` · `too_large` · `overflow`(「그 밖 n 개」) · `OPTIONS_MAX` · `PAIRS_MAX` · `chat_alt_max` · `chat_rec_max` · `answer_input_max_tokens`(테스트 고침 E 의 잘라 답하기) 등. 표: 자리 · 무엇을 자르나 · 답 재료/출력에 닿나.
2. **답 재료 · 출력을 자르는 것은 다 없앤다**: 진료항목 · 옵션 · 쌍 · 다른 계열 · 추천 카드 · 입력 크기로 재료 줄이기 등. 대신 크기가 커지는 곳은 「무엇을 싣나」 로: **진료항목 줄은 전부 싣되 옵션 · 가격은 가격 물음 · 장바구니 · 모달 본 턴만(그 밖은 최저가 한 줄)** — 장부 `material_size` 에 크기만.
3. **행동 횟수 한도**(되묻기 `chat_ask_max` · 잡담 `chat_talk_max` · 턴 한도 CL13 · 화면 주제 수 `chat_topic_max` 등 — 답 재료가 아닌 것)는 **바꾸지 말고 표에만** 적어 코디에게 올린다.
4. 실물: 빈 포트에서 73bd · 03b8 · ecc6 — 73bd T2 에서 입꼬리 필러가 답에 나오나 · 「짚어 드리기 어려워요」 류 0 · 턴별 입력 토큰(calls 네 칸) 전 → 후 · 명동점 블록 크기.

## 산출 · 보고
`$W/cap-remove-report.md`(전수 표 · 바뀐 파일:줄 · 실물 표 · 시험).
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: 고정 한도 없애기" --body "없앤 한도 수 · 남긴 행동 한도 / 73bd T2 / 토큰 전 → 후"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] 고정 한도 없애기 완료 — <한 줄>. 상세는 인박스." --enter
```
