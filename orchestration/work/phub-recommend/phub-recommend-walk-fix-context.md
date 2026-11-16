# 공통 배경 — case3 걷기 살리기(11-01 사용자 승인 「발주하자」)

rerun-v4(182 · 허브 b031371c cc637a2 · 앱 f8533ff · 배치 b202611011148-c6ed3a) 결과:
- 정확성 case1 83 · case2 58(전 49) · case3 49(전 57) / 안전 89 · 96 · 63(전 79) / 첫 글자 case3 5.5s
- case3 걸음: 걸음 수 중앙 **1** · 멈춤 = 예산 116(64%) · empty 28 · enough 28 · steps 10 · 되돌아감 34
- 원인: expand 한 섹션이 2.6~55KB(fact 메타 포함 원문 전체) → 예산 20KB 를 첫 걸음에 소진 → 답이 많이 있는 **이웃 노드(부위 위험 · 금기 조건 · 쌍 관계)**까지 못 감. peek 의 sections[].bytes 는 원문 글자 합이라 실제 expand 의 3~34배 작음.
- 골드 정확성 실패 중 「자료에 없다」 case3 68/87 · case2 48/75.
- case1 은 회당 판정 15~20% 뒤집힘(흔들림) → 비교는 case1 대비 차 · 결정 전 2회 평균.
- 자료: `reference/2026-10-30-hub-evals/build-out/work006-report.md` · `rerun-v4-vs-v3.*` · `rerun-v4-vs-1030.*` · `verify-b202611011148-c6ed3a.*` · `runs/runs.jsonl`(trace.walk: start_node · steps[] · stop · bytes_total · fact_ids · jev_calls) · 허브 `backend/build-out/work007-report.md`(D-1~D-13 · 더 줄일 자리 6)

목표: **예산 20KB 안에서 걸음 3~4 · 이웃 노드 도달**. 허브는 LLM 없음 · 결정론 유지.
