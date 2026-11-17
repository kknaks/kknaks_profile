
# [etl] SPEC-002 0.3.0 — LLM 라벨 전체 다시(예약표 메시지 제외) · 재집계 · 보고서

너는 consult-analysis `etl` 워커다. 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석`. 네 오염 점검 4 를 고치는 일이다 — 끝까지 한 번에.

## 입력
- SPEC-002 **0.3.0** §5 입력 줄 · 변경 이력 0.3.0 · DEC-002 D-23
- 네 점검: 성공 방 통역 89 · 일정 93 · 위치 75 · 부작용 36 이 전부 근거에 예약표 메시지

## 할 일
1. `label_layer2_llm.py`: 입력에서 우리 `form_labels ≥ 3` · 고객 `form_filled ≥ 2` 메시지를 뺀다(기존 `auto_kind` 제외는 그대로). 지시문에 「topics 는 고객이 묻거나 말한 주제만 · 우리 안내 · 양식 칸 이름은 주제가 아니다」. 버전 `llm-0.3.0`. 뺀 뒤 고객 본문이 하나도 없는 방은 부르지 않고 건수 보고(행 수 기준이 1,883 에서 바뀌면 그 수를 보고 — 실패와 구분)
2. 표본 30방 먼저(같은 30방 · 5분 안쪽) → 성공 방 `interpreter` · `schedule` 비율이 떨어졌는지 한 줄 확인 → 바로 전체(`--reset` · 5개 동시)
3. 같은 오염 점검을 다시: 성공 방 주제별 「근거에 예약표 메시지」 수 → 0 이어야 함
4. `judge_layer2.py --decisions data/review_decisions.csv` 다시(국적 ②) → `stats_layer2.py` → `stats-001.json` → 보고서 ⑥(주제 · 시술) · 요약 · 한계 갱신(점검 1 ~ 3 의 작은 오염도 한계 절에 한 줄씩 — 고객 메시지 수 · 턴 · 방 언어)
5. `check_report_numbers.py` 0 · 시험 OK · 1층 verify 274/274

## allowed_paths
- `para/projects/summer-star/consult-analysis/scripts/` · `50-report/` · `data/`(생성물)

## 하지 말 것
- SPEC · DEC · WORK 수정 · Opus · sonnet · 고객 정보 출력

## 완료 보고 — 문구 변경 금지
> preamble 의 코디네이터 핸들이 아래와 다르면 preamble 이 맞다.
```bash
orca orchestration send --to term_1e2044b5-cf36-479a-9750-9d7adba63b4c --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "etl 완료: 0.3.0 라벨 다시" --body "표본 전후 / 전체 실패 · 비용 · 시간 · 부르지 않은 방 / 오염 점검 0 / 주제 통계 전후 / 보고서 / 시험"
orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[worker_done] etl 완료 — 0.3.0 라벨 다시. 상세는 인박스." --enter
```
