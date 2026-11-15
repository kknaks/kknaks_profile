# reviewer_doc 검수 — 요금제 보고서 2판 `pricing-design.md` (Fable 재작성 · 2026-11-12)

대상: `reference/2026-11-12-interpreter-idea/pricing-design.md` + `pd2-*.png` 7장 + `orchestration/work/interpreter-idea/pricing-calc2/`.
**계약 = 재작성 브리프** `orchestration/work/interpreter-idea/rewrite-fable-brief.md` (적정 케이스 표 = 사용자 승인 · 보고서 구조 0 ~ 7 · 쓰는 법).

볼 것:
1. 결론 절만 읽고 「무엇을 · 얼마에 · 왜」가 답해지는가 · 결론 숫자가 본문 · results.json 과 같은가.
2. 적정 케이스 값이 브리프 표와 같은가. 문서가 **더한 가정**(스트림 60분 · 가격 올림 단위 · 정액제 초과 처리 등)이 〔가정〕(미승인)으로 드러나고 §7 에 있는가 · 그 가정이 결론을 얼마나 움직이는가가 적혀 있는가.
3. 모든 숫자에 단위 · 근거 태그 · 기호는 처음에 정의.
4. 재계산 — `calc2.py` 스크래치 복사본 `python3 -I` 재실행 diff · 실측 2건 토큰 × 단가 = cost_usd. Soniox 호출 금지.
5. 민감도(변인 1개 · 나머지 적정 고정) — 변인별 적자 경계가 변인 단위로 쓰였는가 · 그래프 범례 · 축 단위.
6. 사람이 읽을 때 오해할 자리 · 병원 데이터 0 · 키 0.

리포트: `orchestration/work/interpreter-idea/review-pricing-v2-report.md` 1개 — PASS/WARN/FAIL. 수정 금지. 보고는 원 브리프(`interpreter-idea-review-doc-brief.md`) §9 두 채널.
