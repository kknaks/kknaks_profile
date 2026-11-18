# [코디 추가 지시] 속도 탭 — effort 를 열마다 같게

사용자 질문 「정확도 B·C 랑 속도 B·C 가 같은 조건이야?」 → 아니다: B 계열 = `answer_reasoning`(lowest_effort → low), C · A · B 켬 = `spec("on")`(batch effort medium · `col_c.py:43`). 속도 비교는 effort 가 같아야 한다.

할 것(이번 수정에 함께):
- 속도 탭에 **effort 고르기**(low · medium · high — CLI `--effort` 값) · 기본 **low**. 고른 값을 그 실행의 **모든 열(B 선별 · C · B 전체)에 똑같이** — `/api/ask` · `/api/speed/table` 에 effort 를 받아 runner 로 넘기는 길(열 코드는 effort 인자만 받게 · 걷기 · 답 로직 변경 0).
- 정확도 탭 · CLI · batch 기본 동작은 그대로(SPEC 결정 — B low · A/C medium).
- 기록(runs.jsonl)에 열마다 실제 effort 가 이미 남는지 확인 · 없으면 남기기. 속도 카드 머리 effort 표시는 그 값.
- 시험 추가(effort 가 세 열에 같은 값으로 가는지 · 모의 CLI).
