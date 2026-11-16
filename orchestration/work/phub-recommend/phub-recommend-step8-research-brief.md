# [researcher] 실버 8단계(관계 · 안전 · 확인 조건 · 근거) 조사 (read-only)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 원장 · 결정 · 원천 수정 금지. 산출 2파일만.

## 읽을 것
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 — 특히 10-26 「시너지 · 순서 · 간격 · 금기 = 시술↔시술 엣지 하나의 속성」 · 「안전 엣지는 시술 노드와 항상 같이」 · DEC-001 D-02 · D-03 · D-04 · D-13b(원천 주장 충돌 보존) · 10-28 source-map 승인(B04 · B05 · B06 · B11 · B13 · C4) · 해부학 용어 행 · 10-28 「확인 조건」 이름 · 「단계로 넘길 결정」 줄 · 10-29 행(6 · 7단계 8단계 메모)
- `SPEC-004.md`(procedure_relation · safety · complication · site_caution · 주장 구조 · gate_status · 기본 응답 규칙) · 지도 `source-map.json` · `.md`
- 정본 `step1-products.json` · `step2-families.json` · `step3-sites.json` · `step4-techniques.json` · `step5-units.json` · `step6-packages.json`(step6-to-step8-notes) · `step7-concerns.json`(step8_notes 245)
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`: contraindications · synergy · treatment-sequence · treatment-optimization(combination_rules · contraindicated_combos) · problem-packages(CC combos) · pre-procedure-checklist · consent-checklist · patient-education · post-procedure-timeline · complications · anatomy-danger-zones · pih-risk · literature-evidence · procedure-profiles · taxonomy/extracted(safety · aftercare · contraindications)
- 앞 단계 교훈 `para/projects/company/procedure-hub/log/2026-10-29-silver-step5-unit.md` · `-step7-concern.md` §5 — 지금 원천 기준 · 추정 금지 · 같은 성격 전수 · 가상 문장 없음 · 사이트 용어

## 할 것
A. **시술↔시술 관계**: 원천별 쌍 주장 전수(금기 · 간격 · 같은 날 · 순서 · 시너지 · 대체) → 끝점 해석(계열 / 하위 / 단위 시술 — 이름 해석은 5단계 정본 · 후보 전부 + 표시) · 주장 칸(원천 · 원문 · 등급 · 간격 · 이유) · 충돌(같은 쌍 다른 말) 목록 · 6 · 7단계 메모 245 + 37 반영
B. **확인 조건 원장**: 조건 사전(pre-procedure-checklist 뼈대 — 공통 · 계열별 · type) + 동의서 · 원장 · 계열 금기 문장 · 이소트레티노인 쌍 · 연령대 → 조건 노드 · 시술(계열) → 조건 엣지(금기 / 주의 / 확인만 — 원문 등급) · 원천별 주장
C. **안전**: 합병증 65 노드(complications 정본 · 계열 · 중증도 · 발생률 · 처치) · 위험지대 → site_caution 엣지 속성(혈관 · 신경 · 깊이 · 요령 · 등급 — 3단계 zone 대응 · 4단계 safe_layers) · 계열 안전 · 상담 원문(필수 고지 · 응급 징후 · 환자 교육 · 경과표 · 사후관리 · PIH 위험 요인 · 예방) — 붙는 단위(계열 / 하위 / 단위 시술 상속)
D. **근거 노드**: 문헌(PMID/DOI · 진술 119 · 다국어 환자 문장) · 웹 URL · 가이드 · 합병증 URL · 간격 출처 → 근거 노드 + 주장 ↔ 근거 연결 · 강도는 원문 등급만(숫자 만들지 않음)
E. **못 정하는 것 표 하나**(빈 추천 금지) · 원천 질문(받는 사람 표시 — 의료진 / 병원)

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step8-research.json` · `step8-research.md`. md 맨 위: ① 결정 묶음 ② 사용자 최종 판단 — 한 표 ③ 셈(관계 주장 · 충돌 · 조건 · 합병증 · 주의 엣지 · 근거 · open 후보 전부 해결 안)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_72c018cf-c521-4e14-a657-b6953fadb556 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 8단계 조사" \
  --body "관계 주장 N · 충돌 N / 조건 N / 합병증 N / 근거 N / 사용자 판단 N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 8단계 조사. 상세는 인박스." --enter
```
