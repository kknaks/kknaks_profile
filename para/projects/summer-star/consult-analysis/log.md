# Product Log

> 제품 단위 통합 변경 로그. baseline, decision, spec, work 변경 이력을 한 곳에 모은다.

| Date | Entry | Links |
|---|---|---|
| 2026-11-16 | 착수. 원본(인스타그램 DM 내보내기) 실측을 BASE-001 로, 대화에서 닫은 것(두 층 분리 · 예약 성공 = 고객 예약표 회신 · 국적 출처 · SQLite 로컬 · 스크립트는 이 프로젝트)을 DEC-001(proposed)로 | [입력](00-baseline/baseline-001-consult-data.md) · [결정](10-decision/decision-001-two-layers.md) |
| 2026-11-16 | DEC-001 accepted — 사용자 「응 !!」. slug `consult-layer1` 로 SPEC-001 · WORK-001 발주 | [결정](10-decision/decision-001-two-layers.md) |
| 2026-11-16 | DEC-001 D-12 ~ D-15 — reaction 테이블 · 폴더 밖 대화 JSON 포함 · **페이스북 메신저 포함 · 채널 칸**(사용자). BASE-001 페이스북 「대화 없음」 정정(1,405방 · 21,612건) | [결정](10-decision/decision-001-two-layers.md) |
| 2026-11-16 | SPEC-001 0.2.0 accepted — 사용자 「응」(분석의 중심은 고객 문의 · 우리 계정은 발신 구분용). WORK-001 etl 발주 | [스펙](20-spec/spec-001-layer1-schema.md) |
| 2026-11-16 | 2층 분석 착수 — 요구 · 1층 대략치를 BASE-002 로, 판정 방식(규칙 + LLM) · 결과물(보고서 + 차트)을 DEC-002(proposed)로 | [입력](00-baseline/baseline-002-conversion-language.md) · [결정](10-decision/decision-002-layer2-analysis.md) |
| 2026-11-16 | WORK-001 done — 1층 적재(1,916방 · 28,706건 · 첨부 3,461 · 반응 359) · verify 274/274 · 시험 38 · 검수 PASS · WARN 3 반영(SPEC 0.2.1 G-12 확장 · G-13) | [작업](30-work/work-001-layer1-load.md) |
| 2026-11-16 | DEC-002 accepted — 사용자 「그러니까 결과 달라고 이거 하는 거 아니야?」. SPEC-002 · WORK-002 발주 | [결정](10-decision/decision-002-layer2-analysis.md) |
| 2026-11-16 | SPEC-002 accepted · OQ-201 ~ 205 권장 A 로 닫음(DEC-002 D-14 ~ D-18 · claude -p · flow 예약표 포함 · zh 값). WORK-002 WP1 ~ WP3 표본 etl 발주 | [스펙](20-spec/spec-002-layer2-analysis.md) |
| 2026-11-16 | DEC-002 D-14 개정 — LLM 모델 haiku(사용자) · 표본도 haiku 하나 | [결정](10-decision/decision-002-layer2-analysis.md) |
| 2026-11-16 | DEC-002 D-19 ~ D-21 — 사람 확인 15건 판정(성공 92 → 93) · 시술 목록 넓힘 · handoff 낱말 규칙 | [결정](10-decision/decision-002-layer2-analysis.md) |
| 2026-11-16 | SPEC-002 0.2.1 · DEC-002 D-22 — 消脂針 · Tune 목록 추가(OQ-206). etl 전체 라벨 · stats · 보고서 발주 | [스펙](20-spec/spec-002-layer2-analysis.md) |
| 2026-11-16 | SPEC-002 0.2.2 — 이모지 · 사진 통계에서 예약표 회신 메시지 제외(코디 검증: 성공 방 이모지 94.6% → 50.5%). etl 재집계 | [스펙](20-spec/spec-002-layer2-analysis.md) |
| 2026-11-16 | SPEC-002 0.3.0 · DEC-002 D-23 — LLM 입력에서 예약표 메시지 제외 · 전체 다시 라벨(주제 오염) | [스펙](20-spec/spec-002-layer2-analysis.md) |
