# [researcher] 실버 6단계(패키지) 반영

(맥락 없으면 먼저 `step6-research.md` · `step5-decisions.json` · `step5-apply.py` 구조. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`)

결정 `_RESUME.md` §2 2026-10-29 「6단계 패키지 조사 반영」 행(사용자 「추천으로 가자」): R1~R11 · U1~U4 전부 step6-research 추천대로.

1. **5단계 보강 먼저**(U1 · U2): 포토나4D → U5-099 동의어 + 보조 매질 Er:YAG 속성 · 리쥬하이 → U5-018 동의어(쓰는 제품 리쥬란 · HA) — `step5-decisions.json` → `step5-apply.py` 재실행 · open 0 · 원장 행선지 셈 갱신(6단계 18 → 16)
2. **6단계**: 3 · 4 · 5단계와 같은 구조 — `step6-decisions.json` · `step6-apply.py` → `step6-packages.json` · `.md`
   - 패키지 노드 24(id · 이름 · kind(일반 / 회차 묶음 / 병원 시그니처) · 동의어 · 가격 원문 · 원천 설명 · same_day_raw · menu_group · 추천 노출 여부(시그니처 = 기본 제외))
   - 구성 엣지: 패키지 → 단위 시술 키(수량 · 회차 원문 · evidence_level) · 슬롯 9(원문 · 후보 키 · 원천 질문 · missing_unit)
   - 묶음 이름 9 → 7단계 목적 원문 / 패키지 속성(엣지 만들지 않음)
   - 시장가 패키지 행(회차 · 콤보) = 패키지 가격으로 · 5단계 1회 가격과 안 섞음(5단계에서 옮겨 오면 5단계 쪽 셈도 갱신)
   - synergy 대조 38 = 8단계 메모(`step6-to-step8-notes` 칸) · 엣지 만들지 않음
   - 원천 질문 13 → `step6-origin-questions.md` · 원천 수정 후보 1 → `step6-source-fix.md`
   - 결정 = 데이터 파일 · 고정 숫자 assert 없음 · 결정 없는 것 = open · 고정 시험(결정 빼면 open)
3. 끝 조건: open 0 · 패키지인데 구성도 질문도 없음 0 · 결정론(5 · 6 재실행) · 스킬 점검(`reference/2026-10-27-skills-procedure-hub/procedure-hub-unit-check/scripts/check_units.py`) 오류 0 · md 맨 위 셈
원천 · DEC 수정 금지 · 추정 금지.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_0933d258-4d62-4e51-b233-79a7c1ecea09 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 6단계 반영" \
  --body "패키지 N / 구성 엣지 N · 슬롯 N / open N / 5단계 셈 변화"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 6단계 반영. 상세는 인박스." --enter
```
