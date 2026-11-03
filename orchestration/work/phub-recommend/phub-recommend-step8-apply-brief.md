# [researcher] 실버 8단계 반영 — 관계 · 확인 조건 · 안전 · 근거

- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md` · 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`
- 먼저 읽을 것: 조사 `step8-research.md` · `.json` · `_RESUME.md` §2 2026-10-29 「8단계 조사 반영」 · 「게이트 → 규칙」 · 「7단계 재반영 결과 + 남은 13」 행 · 앞 단계 apply 형식 `step7-apply.py` · `step7-decisions.json`

## 사용자 결정(바꾸지 말 것)
- **G1~G14 추천대로**(조사 ① 표 그대로)
- **U8-1 (나)**: 사람 확인 게이트 없음. 화살표 문장 분해 48 · 원칙/규칙/위험 문장 쌍 38 도 **규칙(사전 · 패턴)으로** 결정론 처리 · 규칙으로 하나로 안 정해지는 것만 원천 질문. 「사람이 쌍을 손으로 옮긴 대응표(manual_map)」를 행별 결정으로 두지 말 것 — 문장 패턴 규칙으로 계산
- **U8-2 (가)**: 고민 조건 금기(「기미에 고에너지 레이저 · IPL 단독 금지」 등) = 7단계 고민 노드(예: 기미 P5-1) → 단위 시술 새 엣지 종류 「피함(금기 조합)」. SPEC-004 개정은 빌드 때(여기선 데이터만 · 엣지 타입 이름 기록)
- **간격 = 규칙 기반 숫자 칸**: 추천 · AI 는 `interval.days` · `first` · `same_day` 만 읽는다. 원문은 보관만. **간격 낱말 사전**을 결정 파일에 둔다 — 「N주/N일/N개월(후 · 이상 · 간격)」 → days · open_high / 「택 1 시술」 → kind 대체 · 간격 비움 / 「동시 금지 · 동시 시술 금지」 → same_day false(+ 「같은 부위」 조건) / 「직후」 → same_day true · days [0,0] / 「…전에」 → first 만 / 「사이사이」 → 반복 표시 · 간격 없음 / 「의료진이 … 평가해 간격 결정」 → 간격 없음 + 의료진 판단 표시. **원문 간격 낱말이 있는데 숫자 칸 · 표시가 비면 open**
- 충돌(순서 · 간격 21 · 조건 등급 76 · 이소트레티노인 1) = 전부 보존 + 충돌 표시 · 자동으로 고르지 않음

## 7단계가 바뀌었다(조사 뒤) — 반드시 다시 읽고 끝점 다시 풀 것
- 7단계 재반영(10-29): 대응 249 규칙화 · 새 노드 **J10-피부결**(상위 없음) · 잇몸미소 고민 항목 · 코성형/코 라인 = P1-1 · 다크서클/눈밑꺼짐 = P1-5 · 주름 중증도 → P2-2/P2-3 · 세션 조합 앵커 `anchor.concern` 이 **설명 문자열 → 고민 id 목록**으로 바뀜. `step8_notes` 245 는 바이트 그대로
- 조사 산출의 고민 · 조합 끝점이 지금 `step7-concerns.json` 과 맞는지 apply 가 대조 — 어긋나면 open

## 만들 것
- `step8-decisions.json`(규칙 · 사전 · 판단) · `step8-apply.py`(결정론) → `step8-relations.json` · `.md`(관계 엣지 · 확인 조건 · 합병증 · site_caution · 근거 · 충돌 · 원천 질문 · 원천 수정 후보) · `step8-origin-questions.md` · `step8-fixture-test.py`
- 같은 성격 전수: 원천 21 파일 중 관계 · 조건 · 안전 · 근거 칸 전부를 `source-map.json` 대로 걷는다(조사가 센 것과 대조 · 빠지면 open)
- 끝 조건: open 0 · 두 번 실행 cmp 같음 · 고정 숫자 assert 금지(결정 파일에서 계산) · 고정 시험(간격 사전 각 갈래 · 결정 빼면 open · 7단계 끝점 어긋남 open · 「피함」 엣지) · 기존 스킬 점검 7종 errors 0 · **새 스킬** `reference/2026-10-27-skills-procedure-hub/procedure-hub-relation-check/`(SKILL.md · scripts/check_relations.py · references/ — 앞 스킬과 같은 꼴 · 틀린 값 넣어 잡히는지까지)
- 원천 · DEC 파일 · 1~7단계 산출 수정 금지(7단계 값이 틀려 보이면 고치지 말고 보고)
- 실명 · 키 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_2ef74262-b2db-4748-88cd-27aed3b50bfe --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "researcher 완료: 실버 8단계 반영" \
  --body "관계 엣지 N · 주장 N · 충돌 N / 조건 N · 피함 N / 합병증 N · 주의 N / 근거 N / 원천 질문 N / open N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — 실버 8단계 반영. 상세는 인박스." --enter
```
