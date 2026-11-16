# [researcher] 1단계 제품 원장 수정 — 검수 FAIL 반영

너는 `step1-products` · `step1-decisions` 를 만든 researcher 다(역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`). 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 읽을 것
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step1-report.md` — 검수 FAIL(빠짐 · 근거 없는 칸 · 사용목적 불일치 · 결정 목록 누락)

## 할 일
1. **빠짐**: taxonomy `modality[].products[]` 59개(M*-P-*)를 원장 id 로 대조하고, 행이 없는 14개(타임버스 · 뉴럭스 · 레티보 · 신펄 · 글로벨라 · 셀피아 · 리젠ACR · 마이셀 · EXOSOME SKIN · 에버라인 · 피코웨이 · 인트라셀 · 큐어스킨 · 에스에프)를 필드 1~7 로 추가(같은 방법 — 식약처 API · emedi · 웹, 근거 필수)
2. **근거 없는 칸**: 정체에 근거가 없는 74행에 근거(원천 필드 · URL · 질의 기록)를 단다. 못 달면 정체 「확인 불가(조사 기록)」. 「(추정)」 표기 2건 제거 — 근거로 확정하거나 확인 불가로
3. **허가 대상 아님 4건**(노보젯 · 벨르업 · 오투덤 · 메소건): 출처 URL 이 있는 근거로 확정하거나, 없으면 「확인 불가」로 바꾼다
4. **사용목적 불일치**(릴리이드M = 내시경 점막 융기 · 비타란 22-99 = 관절강 · 레티젠 · 미라콜 = 인대 · 건 보충): 연결을 풀고 원장에 「연결 후보의 사용목적이 미용 시술과 다름」 표시. 근거가 약한 3건(하이드라페이셜 · 아테콜 · 바이리즌↔비타란)도 표시
5. **결정 목록**: 1번 14건 · 노보젯 · 하이드라페이셜 · 에어젯을 넣고, 사용목적 불일치를 **별도 묶음**으로 분리(이름 일치 묶음 D10 · D25 에서 빼기). 질문은 「무엇이 부족해서 무엇을 정하는지」 한 줄
6. summary 갱신

## 산출 · 제약
- `step1-products.json` · `.md` · `step1-decisions.json` · `.md` 수정만. 키 · 실명 금지 · 추정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 1단계 검수 반영" \
  --body "항목별 처리 수 / 원장 수치 / 결정 묶음 수"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 1단계 검수 반영. 상세는 인박스." --enter
```
