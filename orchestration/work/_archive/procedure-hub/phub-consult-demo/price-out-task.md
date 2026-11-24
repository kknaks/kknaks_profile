# [code] LLM 에 가격 숫자 넘기지 않기 (사용자 결정 11-23)

앞 발주 `fetch-plan-code-task.md` 규칙 그대로(앱 워크트리만 · 커밋 0 · 18222 · 18105 손대지 마라 · 실물은 빈 포트 · 키 출력 0 · 관련 시험 · 전체는 마지막 한 번). `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`

## 사용자 결정(다시 묻지 마라)
- **가격은 화면(카드 · 모달 · 장바구니 · 최저가)이 보여 준다. LLM(이해 · 답)에는 가격 숫자를 넘기지 않는다.** 진료항목 이름 · 옵션 구성(샷 · 회차 · 용량 · 이벤트 여부 같은 옵션 이름)은 그대로 넘긴다.
- 가격을 물으면 답은 화면을 가리킨다(「가격은 카드 · 장바구니에서 보실 수 있어요」 꼴 · 숫자 0 · 지어내지 않음).
- **그 밖의 답 품질 · 화면 · 장바구니 · 최저가 계산은 건드리지 않는다**(진료항목 수 · 30 한도 · fetch · 말투 규칙 그대로). 이번은 가격 숫자만.

## 할 일
1. LLM 으로 가는 가격 칸 전수(grep `price` · `amount` · `supplied` · `vat` · 「원」 · 최저가 줄 · 장바구니 줄 · `rec` · `cart` · 쌍 줄 · `prompts/consult.json` 가격 규칙) — 표. 빼고, 답 규칙의 가격 줄을 위 결정으로.
2. 장부 `llm_user_message` 에도 가격 숫자 0 이 되나(JS6 시험 범위를 넓힘).
3. **전 → 후 대조**: 빈 포트에서 03b8 · ecc6 · 73bd + 가격 물음 2(「써마지 몇 샷 맞아야 해?」 · 「볼뉴머 얼마야?」) + 장바구니 담은 뒤 「뭐가 제일 싸?」 1 — 턴마다 답 앞 2 줄 전 · 후 · 가격 숫자 0 · 그 밖 정보 빠짐 0 · 명동점 블록 크기 · 입력 토큰(calls 네 칸) 전 → 후. 화면 가격 · 최저가는 그대로인지 스크린숏 `$W/e2e-shots/priceout-*.png`.

## 산출 · 보고
`$W/price-out-report.md`.
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: LLM 가격 빼기" --body "가격 칸 수 / 블록 · 입력 토큰 전 → 후 / 답 빠짐"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] LLM 가격 빼기 완료 — <한 줄>. 상세는 인박스." --enter
```
