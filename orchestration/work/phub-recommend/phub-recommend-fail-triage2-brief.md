# 발주서 — rerun-v3 뒤 남은 실패 전수 분류(2차 · 읽기 전용 · 코드 · 데이터 수정 금지)

## 목적
rerun-v3(골드 d3a1abd5 · 코드 c95b37a) 뒤에도 실패한 행 325(case2 132 · case3 145 · case1 48 — case1 은 대조용 집계만)을 1차와 같은 결정론 대조로 A/B/C/D 분류하고, **C(허브가 줬는데 답이 놓침)가 얼마나 늘었는지** · B 가 어디에 남았는지를 숫자로 낸다. 결론 · 고칠 안 없음.

## 입력(읽기만)
- `reference/2026-10-30-hub-evals/build-out/rerun-report.md` §5(후에도 실패 325행 · Opus 주장 · 근거 경로) · `rerun-report.json`
- `runs/quality.jsonl`(batch b202610311552-d39a4d 행 · judge.failures[] status valid) · `runs/runs.jsonl`(같은 batch · trace: case2 도구 호출 결과 · case3 trace.hub)
- 새 export `backend/build-out/gold-export.json`(d3a1abd5) · 18005(떠 있음 · 읽기 호출만) · 원장
- 1차 `fail-triage.md` · `fail-triage-scripts/triage.py recheck.py`(같은 판정 식 · import 말고 같은 식으로)

## 분류(1차와 같음 + 세분)
- A 골드에 없음(새 export 기준) · B 골드엔 있는데 허브 응답에 없음 · **C 허브 응답에 있는데 답이 놓침** · D 채점 오류 · 미분류
- C 는 다시: C1 응답 본문(원문)에 있음 / C2 fact id 만(more_ids 등) 있고 원문은 없음 / C3 다른 섹션 · 동봉 깊숙이(응답 바이트 위치 · 전체 크기 함께)
- B 는 1차 「빠진 칸」 20종 그대로 + 「v3 조항이 닿는데 구현이 안 실음 / 닫지 않는 행(19+21) 그대로」 구분
- 나빠진 122행(전 통과 → 후 실패)은 따로: 「엉뚱한 연결」(다른 노드의 fact 를 붙임 — 예 Q003 보톡스 경고 → 실리프팅) 건수 · 그 fact 가 응답 어디(동봉 종류 · 섹션)에서 왔는지
- case2 호출에서 Claude 가 `intent` 를 넘긴 호출 수 / 전체 · case3 응답 크기 분포(중앙 · p95)와 C 비율의 관계(크기 구간별 C 수)

## 산출 `build-out/fail-triage2.md` + `.json`
1. 케이스 × 항목 × A/B/C/D 표(1차 표와 나란히)  2. C 세분 표 + 예  3. B 잔여 표  4. 나빠진 행 · 엉뚱한 연결 표  5. intent 전달 수 · 크기 ↔ C  6. A 잔여(원장 필드별 · 1차 61과 대조)
레포 밖 · 커밋 없음 · 끝나면 worker_done(표 1 요약 + C 비율).
