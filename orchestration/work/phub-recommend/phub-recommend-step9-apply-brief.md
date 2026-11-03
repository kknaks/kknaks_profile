# 발주서 — 실버 9단계(설명 사실) 적용(사용자 11-01 「추천으로 데이터 결정하자」)

## 정본
`step9-research.md/.json`(설계 · R9-1~7 · G9-1 · section 표 · 효과 셈) + 아래 결정. 이전 단계 방식 그대로: `step8-decisions.json` · `step8-apply.py` · `step8-fixture-test.py` · 점검 스킬 `reference/2026-10-27-skills-procedure-hub/procedure-hub-*-check/`.

## 결정(D9 · 사용자 승인 = 추천)
- D9-1 합병증 · 부작용 관리 · 예방 → 새 section `safety.management`
- D9-2 적응증 → overview
- **D9-3(코디 추천 · 사용자 승인 · D-13b 방향)**: 같은 노드 · 같은 칸 다른 값 606 을 둘로 나눈다 — ① **포함 관계**(한쪽 문장이 다른 쪽을 정규화 포함 · 또는 숫자 · 단위 집합이 같고 문장만 다름) = 충돌 아님 → 긴 쪽 하나로 합침(짧은 쪽은 same_as) ② **숫자가 진짜 다름** = 하나로 정함(resolved) · 보수 규칙: 지속 · 유지 기간 = 짧은 쪽 · 간격 · 회복 · 다운타임 · 대기 = 긴 쪽 · 시작(onset) = 늦은 쪽 · 그 밖 숫자 = 원천 우선순위(그 노드 자신의 원장 항목 → taxonomy products → 후보) — 다른 값은 `alternatives` 로 보관 · 골드엔 resolved 하나만 나감 ③ 숫자 없는 서로 다른 문장 = 둘 다 실음(서로 다른 사실 · 같은 칸 두 행 · multi_source 표시) — 셈을 ①②③ 별로 결정론 보고
- D9-4 extracted.json 이 정본과 다른 7칸 → 싣지 않음(source_conflict 리포트)
- D9-5 쁘띠 CC 대안 · 상세 → 단위 시술 + cc 조건 표시
- D9-6 5단계 원문 보관 37항목 → 붙이지 않음
- D9-7 값 사전 8 → 시맨틱 값 사전 + 골드 globals
- D9-8 legal_warning 2 → disclosure
- D9-9 하위 분류 description 3 → 계열 overview + sub_family 표시

## 할 일
1. `step9-decisions.json`(D9-1~9 · 규칙 번호) · `step9-apply.py`(결정론 · 두 번 cmp 같음) · `step9-explanations.json/.md`(레코드) · `step9-fixture-test.py`(규칙마다 픽스처) · 충돌 처리 셈 ①②③ 리포트
2. 점검 스킬 새로 `reference/2026-10-27-skills-procedure-hub/procedure-hub-explanation-check/`(SKILL.md · references(rules · record-schema · mistakes) · scripts/check_explanations.py) — 다른 스킬과 같은 꼴 · README 목록 갱신
3. **단계 끝 = open 0**(사람 확인 0 · 미해결 0 · 가드 통과) · 시맨틱(`semantic-build.py`)에 값 사전 반영이 필요하면 같은 결정론으로
4. 로그 `para/projects/company/procedure-hub/log/2026-11-01-silver-step9-explanations.md`(이전 단계 로그 꼴 · 무엇을 왜 · 숫자 · 결정)
5. 효과 재셈: 2차 A 54 · v5a A 30 중 실버 9단계 레코드로 닫히는 행(행 단위 · 조사 셈과 대조)
골드 빌드 · 허브 코드는 손대지 말 것(section `safety.management` 등 골드 반영은 다음 허브 발주 · 코디).

## 제약
원장 · 실버 데이터는 work/ 안(공개 레포 커밋 안 함) · 추측 금지 · worker_done(①②③ 셈 · 레코드 수 · open 0 · 닫히는 A 행 수 · 스킬 · 로그 경로).
