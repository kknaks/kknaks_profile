# [researcher] 시맨틱 정의 반영 — 결정(B1~B12 · U1~U3) 적용 + 시맨틱 정본

너는 앞서 `semantic-research.*` 를 쓴 워커다(이어서). 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 작업 폴더 `orchestration/work/phub-recommend/`.

## 사용자 결정(10-30 · 바꾸지 말 것)
B1~B12 · U1~U3 **전부 추천대로**. `_RESUME.md` §2 「시맨틱 조사 반영 — 추천대로」 행.
- U1: gap 17 중 family_text 「부작용 문장」 있는 7계열을 원천 안 문장으로 — serious → 합병증 노드 · common · uncommon → 부작용. 남는 gap 12 유지
- U2 · B1: 부작용 = 계열 속성(+ 제품 · 단위 시술 값 있으면 덮어씀) · 합병증 = severity moderate 이상만(65 → 27) · mild 38 → 부작용 · 예외 9(mild 인데 흔함 아님) → 의료진 질문
- U3 · B3: 끝점 묶음 = 엣지 `candidates[]` 칸(노드 아님)
- B8: 확인 조건 「조건 아님」(상담 · 시술 준비 · 고지) = 계열 원문 속성으로 빼고 엣지 셈에서 제외

## 할 일
1. **실버 반영**: 위 결정 중 실버 데이터가 바뀌는 것(U1 · U2 · B1 · B3 · B8 …)을 해당 단계 **결정 파일 → apply 재실행**으로(손 수정 금지) · open 0 · cmp · 고정 시험 추가 · 스킬 errors 0
2. **시맨틱 정본** `semantic.json` + `semantic.md` + 결정론 생성 `semantic-build.py`(실버 파일에서 계산 · 두 번 실행 cmp 같음):
   - 노드 종류 13 · 엣지 종류 21(B4) — 이름 · 뜻 · 시작 → 끝 · 속성 · 정본 파일 · 칸 경로 · 셈
   - 용어집 47 · 표시 12(B12) · gate_status 3값 · 읽는 규칙(reading_contract · 간격 사전 · by_sub_condition)
   - **사전 하나**(B5): 표현 → targets[] + qualifier · 출처 칸 · 겹침 147 처리 결과
   - **id 규칙**(B6): 실버 파일의 id 를 바꾸지 말고 `semantic.json` 에 정본 id ↔ 실버 id 대응표(골드 · 적재가 이걸 씀)
   - 상속 규칙 9(B7 · 저장 안 하고 골드가 계산) · R21 · R22 부위 규칙 포함
3. `silver-graph-build.py` 가 시맨틱 정본을 읽도록 고칠지는 하지 말 것(다음 단계) — 단, 재생성은 해 둠
- 7단계 `step7-concerns.json` 은 다른 검수 워커가 읽는 중 — 7단계 결정은 이번에 바꾸지 말 것(바꿀 게 있으면 보고만)
- 원천 · DEC 수정 금지 · 가상 문장 시험 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_bed89150-1ed2-4c29-8a92-044bf8ac6ede --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "researcher 완료: 시맨틱 정의 반영" --body "합병증 N · 부작용 N · gap N / 노드 종류 N · 엣지 종류 N · 사전 표현 N / open N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — 시맨틱 정의 반영. 상세는 인박스." --enter
```
