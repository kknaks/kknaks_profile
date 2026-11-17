
# [etl] SPEC-002 0.2.2 — 이모지 · 사진 통계 바로잡기 · 재집계 · 보고서 갱신

너는 consult-analysis `etl` 워커다. 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석`. 짧은 수정이다 — 빨리.

## 왜
코디 검증: 성공 방 「이모지 쓴 방 94.6%」는 고객이 회신한 **예약표의 ★ · 📝 양식 기호**가 이모지로 세인 값이다. 예약표 칸이 든 고객 메시지를 빼면 성공 47/93(50.5%) · 실패 132/1,803(7.3%).

## 할 일
1. `stats_layer2.py` — SPEC-002 **0.2.2** §6: 이모지 집계에서 `form_labels ≥ 1` 인 고객 메시지를 뺀다(방 비율 · 메시지당 평균 모두). 사진은 전체 + 「`filled_message_id` 앞 / 뒤」로 나눠서도(성공 방만 뒤가 있음)
2. 같은 꼴의 오염이 다른 항목에도 있는지 스스로 점검 — 예약표 회신 메시지가 섞여 성공 방 값을 부풀리는 항목(고객 메시지 수 · 턴 · 길이 · 시각 등). 있으면 **고치지 말고** 항목 · 크기를 보고(SPEC 밖 수정 금지)
3. `stats-001.json` 다시 · 보고서 수치 · 문장 갱신(이모지 절 · 요약). `check_report_numbers.py` 0 · 시험 추가(양식 기호 든 회신 메시지를 빼는지) · 전체 시험 OK
4. 보고서 status 는 draft 그대로

## allowed_paths
- `para/projects/summer-star/consult-analysis/scripts/` · `50-report/` · `data/`(생성물)

## 하지 말 것
- SPEC · DEC · WORK 수정 · LLM 다시 부르기 · 고객 정보 출력

## 완료 보고 — 문구 변경 금지
> preamble 의 코디네이터 핸들이 아래와 다르면 preamble 이 맞다.
```bash
orca orchestration send --to term_1e2044b5-cf36-479a-9750-9d7adba63b4c --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "etl 완료: 0.2.2 재집계" --body "바뀐 수 / 다른 오염 점검 결과 / 시험 / check_report_numbers"
orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[worker_done] etl 완료 — 0.2.2 재집계. 상세는 인박스." --enter
```
