
# [etl] WORK-002 WP3(전체) · WP4 · WP5 — LLM 라벨 전체 · 집계 JSON · 보고서

너는 consult-analysis `etl` 워커다(2층 판정 · 표본을 한 그 워커). 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석`. **사용자가 결과를 기다린다 — 끝까지 한 번에.**

## 입력
- SPEC-002 **0.2.1**(OQ-206 닫힘 · D-22 · 시술 20개)(`para/projects/summer-star/consult-analysis/20-spec/spec-002-layer2-analysis.md`) — §5 목록 · 별칭 · `procedures_other` 칸 · §6 통계 · §7 산출물
- DEC-002 D-14(haiku) · D-22(消脂針 · Tune) · D-19(사람 판정 — `data/review_decisions.csv` 코디가 만들어 둠) · D-20 · D-21
- WORK-002 WP3 ~ WP5 · 수용 기준

## 할 일 (순서대로)
1. `label_layer2_llm.py` 를 SPEC 0.2.1 §5 에 맞춤(목록 · 별칭 · `procedures_other`) · 오버헤드 줄이기 그대로 · `--effort low` 가 되면 써서 출력 토큰 줄이기(JSON 품질이 같을 때만)
2. **표본 30방 재시험**(haiku · `--reset`) → `other` 비율(방 기준 · 값 기준) 보고. 방 기준 30% 이하면 바로 3 으로. 넘으면 `procedures_other` 상위 값을 보고에 적고 **그래도 3 으로 간다**(멈추지 말 것 — 코디가 나중에 판정)
3. **전체 1,883방**(haiku · 5개 동시 · 이어 하기 가능하게). 실패 건수 · 총 비용 · 걸린 시간
4. `judge_layer2.py --decisions data/review_decisions.csv` 다시(국적 ② · 사람 판정 반영 → 성공 93 확인)
5. **WP4** `stats_layer2.py` → `50-report/stats-001.json`(SPEC §6 · §7 전부 · 모든 비율 `n` · `d` · `small`)
6. **WP5** `50-report/report-001-conversion-language.md` + `50-report/README.md` — SPEC §7 절 ① ~ ⑧. 수치는 전부 JSON 에서. 인과 금지 · 차이로만 · `small` 표시. 한계 절에 handoff 29방 · 언어권 ≠ 국적 · 표본 크기. 문체는 리포 `rules/` 를 따른다
7. 단위 시험 추가(stats 계산 몇 개 · 지어낸 자료) · 1층 verify 274/274 다시

## allowed_paths
- `para/projects/summer-star/consult-analysis/scripts/`
- `para/projects/summer-star/consult-analysis/data/` (생성물)
- `para/projects/summer-star/consult-analysis/50-report/`

## 하지 말 것
- SPEC · WORK · DEC 수정 · 1층 수정 · Opus · sonnet 사용
- JSON · 보고서 · 출력에 고객 본문 · 이름 · 계정명 · 폴더명 · `procedures_other` 값 · `raw_value` 0

## 검증
- WORK-002 수용 기준 1 ~ 8 전부(행 수 · 판정 주체 · 고객 정보 0 대조 · 분모 표기 · 다시 돌려도 같음)
- 보고서의 모든 수가 JSON 에 있음(대조 스크립트나 grep 으로 확인 · 방법 보고)

## 완료 보고 — 문구 변경 금지
> preamble 의 코디네이터 핸들이 아래와 다르면 preamble 이 맞다.
```bash
orca orchestration send --to term_1e2044b5-cf36-479a-9750-9d7adba63b4c --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "etl 완료: 라벨 전체 · stats · 보고서" --body "변경 파일 / 표본 other 비율 / 전체 실패 · 비용 · 시간 / 성공 93 확인 / 보고서 요약 숫자 / 수용 기준 / 미결"
orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[worker_done] etl 완료 — 라벨 전체 · stats · 보고서. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[질문] etl: <질문>" --enter`
