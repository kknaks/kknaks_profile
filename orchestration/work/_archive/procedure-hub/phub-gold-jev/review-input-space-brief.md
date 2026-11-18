# [reviewer] 조사 검수 — 상담 입력 전수 표 · 실패 층 · 후보 뽑기 다섯 판 비교

너는 **procedure-hub 문서 검수 워커**다(read-only). 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/` 아래 reviewer(없으면 researcher) `role.md` · `rules.md`.

경로: `W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · gold `…/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/gold/`(읽기만) · 앱 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만).

검수 대상: `$W/research-input-space.md` + `$W/research-input-space/`(conversations.jsonl · now-turns.jsonl · fail-by-tag.csv · pick-*-turns.jsonl · fan-*-turns.jsonl · pick-prompt.md · summary.json). 브리프 `$W/input-space-research-brief.md` · `_RESUME.md` §2 맨 위 11-18 행 두 줄.

이 결과로 사용자가 **상담 입구 구조**(소넷이 후보를 뽑고 확정 / Jev fan-out / Jev 확정)를 정한다. 그 판단을 흔들 결함을 찾는 것이 일이다.

## 볼 것

1. **정답 키 치우침**: 정답 키 · 시안 프롬프트 · 채점 스크립트를 한 워커가 지었다. `pick-prompt.md` 규칙이 표의 정답 키 꼴에 맞춰 짜였는지(표에만 맞는 규칙 · 표의 예문이 프롬프트에 들어갔는지) · 정답 키 근거(`basis`)가 gold 로 확인되는지 표본 20 턴(꼴마다 고르게) 직접 대조. 소넷 판 97% 가 과적합인지 판정.
2. **판 사이 공정성**: 다섯 판(지금 · 소넷 · 하이쿠 · 소넷+Jev · Jev fan-out)이 같은 정보(대화 · 객체 · 이번 말)와 같은 채점 규칙을 받았나. 특히 (나) 소넷+Jev 는 옛 `jev_front` 지시문 · 앞 손님 말 3 개만 받았고 (다) fan-out 은 지시문 · 문턱 한 벌만 쟀다 — 이 차이가 결론(U-1 (가) 추천)을 바꿀 만한가. 「윗층 받아 준」 채점(83.7%)이 소넷 판에도 같게 적용됐나.
3. **수 재현**: summary.json · jsonl 에서 §0 · 표 1 · 표 2 의 수를 직접 다시 센다(스크립트는 네 scratchpad). 어긋나면 표로.
4. **표 밖 꼴**: 실제 상담에서 나올 말 가운데 표에 없는 꼴(예: 가격 · 기간 · 부작용 질문 · 여러 문장 긴 말 · 이모지 · 영어 제품명 · 앞 답에 대한 반박 등)이 있나 — 있으면 목록과 그 꼴이 결론을 바꿀 가능성.
5. **측정 한계**: 캐시 · 동시 4 호출 · 앞 답 빈 글이 지연 · 턴 종류 수를 얼마나 흔드나. 2.9초 지연 수치를 실서버 조건에서 믿어도 되나.
6. §4 데이터 보강 · §5 앱 규칙 고칠 곳의 `file:line` 이 실제 코드와 맞나(표본 6).
7. §6 정할 것의 추천이 근거 수와 맞나 · 빠진 정할 것.

## 판정 · 산출

`$W/review-input-space.md` 1개: 머리 = PASS / WARN / FAIL + 한 줄 · 결함 표(번호 · 심각도 · 근거 경로 · 고칠 방향) · 재현한 수 표 · 「결론(U-1 추천)을 바꾸나」 한 문단.

## allowed_paths · 하지 마라

쓰기는 `$W/review-input-space.md` 1개(임시는 scratchpad). 조사 파일 · 앱 · 허브 · gold 수정 금지. 서버 · DB · LLM · Jev 호출 금지(이미 있는 jsonl 로만). 결정하지 마라.

## 완료 보고 — 문구 변경 금지

> 핸들 · taskId · dispatchId 는 dispatch preamble 값을 믿어라.

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer(input-space) 완료: <PASS|WARN|FAIL> <한 줄>" \
  --body "결함 수(심각도별) / 재현 어긋남 / 결론 바뀌나 / 주의점" \
  --outcome succeeded

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] reviewer(input-space) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
