# [researcher] 실버 5단계 재검수 v2 F1 — 하위 키 안 기법 근거 · 남은 20쌍

(맥락이 없으면 먼저 `review-step5-v2-report.md` · `step5-decisions.json` technique_compat · `step5-apply.py` 상속 부분 · 앞 브리프 `phub-recommend-step5-fix3-brief.md` 를 읽어라. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`)

결정(이미 있음 · _RESUME §2 10-29): 「근거 없으면 상속 안 함」 · 「클리닉에서 쓰는 장비 → 시술은 전부 단위 시술」. 리포트 F1 「닫는 결정」 추천을 그대로 쓴다:
1. **하위 키라도** 그 매질의 키 기법이 둘 이상이거나 기법에 조건(requires — K04a 펄스 · K04b 프락셔널 등)이 있으면 **매질 일치를 근거로 치지 않는다**. 근거 = 4단계 장비 속성 · **1단계 detail · 허가 사용목적 · 모델명 · evidence 출처**(예: 스플렌더 X detail 「… 제모 레이저」 · 젠틀레이즈 허가 모델) — 그 기법(또는 목적 「제모」 키)을 채울 때만. 엔디야그 K04a 는 펄스 사전 전부라 매질로 충분(리포트대로)
2. **M5 「확인 불가」 제품**(셀엑소좀 · 카탈리스트 · 드원셀)은 M17 과 같이 **출처로만**(주입 출처 → K01 · 도포 출처 → K09 · 없으면 상속 안 함 + 원천 질문)
3. 결과로 **단위 시술 0 이 된 추천 가능 제품**(리포트 예상 젠틀레이즈 · 스마트자이드 외 전부)은 1단계 출처로 맞는 키(제모 부위 키 · 프락셀 등)에 잇는다. 출처로 안 닫히면 예외 + 원천 질문(미라셀과 같음). 추정 금지
4. 다시 셈: 상속 쌍 · 기법 근거 없는 쌍 0 · 추천 가능 제품 중 단위 시술 0 목록(진단 장비 2 + 예외들 — 각 이유) · open 0 · 결정론 · 고정 시험(케이스 추가) · md 맨 위
다른 것은 바꾸지 마라.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_d7588d69-6575-431c-b173-9f07f514bd32 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 5단계 v2 F1 수정" \
  --body "상속 쌍 전후 / 근거 없는 쌍 0 / 단위 시술 0 추천 제품 목록 / open N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 5단계 v2 F1 수정. 상세는 인박스." --enter
```
