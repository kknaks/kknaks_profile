# [researcher] 실버 8단계 검수 FAIL 2 · WARN 2 수정

(맥락 없으면 `review-step8-report.md` 부터 · `step8-decisions.json` · `step8-apply.py`)

1. **F1 피함 엣지 qualifier** — 코디 선택 ⓑ + 질문: 원문에 「고출력 · 고에너지」 같은 출력 한정어가 붙은 피함(AV8-001 · 002 · 004)은 `scope: 조건부 — 단위 시술 미특정` 표시 · **기본 상속에서 뺌**(M8 전체로 열지 않음) · qualifier 원문 보관 · 같은 원문의 「저출력 토닝만 권장」은 7단계 기미 → 토닝 추천과 같은 방향이라 그대로 둔다. 의료진 질문 1(「기미에 피할 고출력 · 고에너지 레이저는 어느 단위 시술인가 — 피코 · Q스위치 고출력 · 프락셔널 · IPL 등」) 추가. **같은 성격 전수**: 피함 · 금기 · 같은 날 불가 주장 전부에서 끝점 앞 한정어(고출력 · 고에너지 · 박리성 · 심부 · 강한 …)를 떼고 계열 전체로 연 것이 있는지 찾아 같은 규칙으로. 결정 파일 규칙 한 줄 + 고정 시험
2. **F2 하위 조건이 갈리는 options** — options 의 sub_condition 이 서로 다르면 겉 `same_day` · `first` · `days` 를 비우고 `by_sub_condition` 표시 · 읽기 규칙(`reading_contract`)에 「겉 칸이 비고 by_sub_condition 이면 options[].sub_condition 별 값을 읽는다」 추가. R8-0003 · R8-0013 · **전수**(sub_condition 갈리는 options 전부). 하위 조건 없는 「또는」(R8-0030 등)은 그대로. 고정 시험 1
3. **W1** `research_diff` 항목별 이유 한 줄(간격 수치 충돌 4 → 2 이유 = open_high 겹침 비교 · 질문 Q8-3 · 4 에 남음 / 조건 378 → 373 = 기미 5 피함 / 묶음 낱말 3 → 2 · 주장 종류 재분배)
4. **W2** 웹 근거 노드: URL 없는 것 = kind 「원문 출처 문자열(내부 · 통설)」 · 「;」 로 이은 URL 2개 = 표시 `multi_url`(쪼개지 않음)
5. 재실행 · open 0 · 결정론 cmp · 고정 시험 · check_relations(+selftest에 F1 · F2 갈래) · 스킬 7종 errors 0 · md 셈. 1~7단계 산출 · 원천 · DEC 수정 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_2ef74262-b2db-4748-88cd-27aed3b50bfe --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "researcher 완료: 실버 8단계 검수 수정" --body "피함 조건부 N · by_sub_condition N / 질문 N / open N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — 실버 8단계 검수 수정. 상세는 인박스." --enter
```
