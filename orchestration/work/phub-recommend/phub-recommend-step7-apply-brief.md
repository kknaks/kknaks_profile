# [researcher] 실버 7단계 반영 — 5단계 보강(J7) 먼저

(맥락 없으면 `step7-research.md` · `step5-units.md` 머리 · 스킬 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/procedure-hub-unit-check/SKILL.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/procedure-hub-family-check/SKILL.md` 부터. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`)

결정 `_RESUME.md` §2 2026-10-29 「7단계 조사 반영」 행 — 전부 step7-research 추천대로.

## 1. 5단계 보강(J7) — 단위 시술 스킬 절차대로
- 단위 시술 없는 시술 14묶음(경화요법 · 엔더몰로지 · 미라드라이 · 엑시머 · UVB · 바디 HIFU · 바디 RF · 스컬프슈어 · 냉동 · IPL 제모 · 모발이식 · 지방흡입 등 — step7-research F 표 그대로) + 제모 부위 8(인중 · 구레나룻 · 팔 · 다리 · 비키니 · 수염 · 가슴 · 등)
- 계열은 **기존 24 계열 정의(2단계 · 문헌)에 드는지 먼저** — 드는 것은 그 계열 · 하위 · 기법으로 키를 세운다(근거 기록). 제모 부위는 기존 제모 키 패턴(레이저 × 부위 × K04)
- **기존 계열에 안 들어 새 계열이 필요하거나, 수술(모발이식 · 지방흡입)을 단위 시술로 세울지 정해야 하면 — 반영하지 말고 표 하나로 멈춰서 질문(decision_gate)**: 시술 · 판단 · 추천(2단계 기준 · 문헌 PMID 실재 확인) · 영향. 코디가 사용자에게 한 번에 묻는다
- 처방약 · 외용제 · 실리콘시트 = 시술 아님(5단계 선례)

## 2. 7단계 — 같은 구조로
`step7-decisions.json` · `step7-apply.py` → `step7-concerns.json` · `.md`: 고민 노드 54(+ 자갈턱 J8 · 기타 하위 J2) · 대응표 249(사람 확인 83 = 추천값 초기값 · gate_status) · 목적 노드 13 · 엣지(보강 뒤 다시 내림 · 원천별 · 단위 시술 / 계열만 / 대상 없음 표시) · 추천 조합 79(종류 · 앵커 · 구성 · 등급 · 가격 · 기대 효과 · 영업 문구 보관 기본 제외) · 8단계 메모 245 · 원천 질문 · 원천 수정 후보(계열 코드 어긋남 18)
- 결정 = 데이터 파일 · 고정 숫자 assert 없음 · 결정 없는 것 = open · 고정 시험(결정 빼면 open) · 사이트 용어(화면 코드) 동의어
- 끝 조건: open 0 · 결정론(5 · 7 재실행) · 스킬 점검(unit · package) 오류 0 · md 맨 위 셈
원천 · DEC 수정 금지 · 추정 금지.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_4e939319-a719-42e9-9125-c7796e18a07a \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 7단계 반영" \
  --body "5단계 보강 키 N / 고민 N / 대응 N / 목적 N / 엣지 N / 추천 조합 N / open N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 7단계 반영. 상세는 인박스." --enter
```
