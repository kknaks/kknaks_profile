# [planner] fix-2 — 재검수 review-doc-2 R1 ~ R3

읽을 것: `review-doc-2-report.md` §4 R1 ~ R3 (이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/`). 워크트리 · allowed_paths · 금지 = 원 브리프 그대로. 네 미커밋 변경 위에서.

- R1: `spec-002` :405 앞 문장 · :778 앞부분(옛 줄 단위 충돌 · 「새 값으로 바꿔 보임」 · 그 토스트 · 200)을 `~~…~~(앞 판 줄 저장 · → C17)` 로. :778 HTTP 칸 = 「~~409 · (개정 ㉘) 200~~ 409」.
- R2: OQ-90 ⓒ 기본값(코디) = **한도가 정해질 때까지 DAY 는 길이 검사를 하지 않는다** · `chart_too_long` 행은 자리만(취소선 아님 · 「한도 정해지면」) · KOS 가 길이로 거절하면 지금 쓰기 큐 실패 처리 그대로. :785 · :1154 문장을 이 기본값과 맞춘다.
- R3: 규칙 31 ⓑ 에 「판정 대상 = 요청 `rows[]` 의 줄 · 보내지 않은 줄은 판정하지 않고 지금 DAY 값으로 그림」(기본값).

lint `--strict` products/day ERROR 0. 커밋 금지. 보고 `planner-fix-2-report.md` + preamble 의 worker_done 두 채널.
