# [tool_dev] 아티팩트 두 개 최신 구조로 — 연결 구조 페이지(시맨틱 정본 기준) · 질문 페이지 v3

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`. 앞 지시 `phub-recommend-graph-view-brief.md` · `phub-recommend-questions-page2-brief.md`. 코디가 **같은 URL 로 다시 게시**한다.

## 1. 연결 구조 페이지 `silver-graph.html` · `silver-graph-build.py`
- 지금은 페이지가 실버를 따로 뽑아 노드 14 · 엣지 32 종류로 그린다 → **시맨틱 정본 `semantic.json` 기준**으로(노드 13 · 엣지 21 · 표시 12 · 정본 id · 용어 이름). 끝점 묶음은 노드 아닌 엣지 후보 칸(U3) · 부작용 = 계열 속성 · 합병증 35 · 상속 엣지는 「계열에서 상속」 그대로(펼치기는 골드)
- 상세에 용어집 뜻 · 사전 표현(검색) · gate_status · 표시 이름
- 결정론 · 재실행 cmp · 16MB 이하 · 스모크(예시 시작점 · 검색 · 필터 · 이웃 그림 컨테이너)

## 2. 질문 페이지 `silver-questions.html` · `.json` (v3)
- 10-29 v2 뒤에 생긴 질문 더하기: 각 단계 `step*-origin-questions.md` · `step8-relations.json` origin_questions · `semantic.json`(부작용 · 합병증 예외 9 의료진) · 7단계 R26 흉터 필러 · R27 원천 수정 후보 — **지금 파일에서 다시 뽑아** 이미 닫힌 건 빼고(근거 json)
- 남는 항목 id 는 v2 와 같게(저장된 답 보존 · removed_ids)
- 스타일 · 저장 방식 v2 그대로 · 스모크

- 실명 · 키 금지 · 실버 · 시맨틱 데이터 수정 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_f38ee267-9280-40f7-83af-974edb398096 --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "tool_dev 완료: 아티팩트 두 개 최신" --body "그래프 노드 종류 N · 엣지 종류 N / 질문 의료진 N · 병원 N(더한 N · 뺀 N) / 검사"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] tool_dev 완료 — 아티팩트 두 개 최신. 상세는 인박스." --enter
```
