# [tool_dev] 스킬화 — 단위 시술 판정 · 실버 단위 시술 원장 갱신

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 만들 곳 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/` — 이미 있는 스킬 4개(product · family · site · technique-check)와 `README.md` 를 먼저 읽고 **같은 형식**으로.

## 원천 (실제로 한 방법을 옮긴다)
- 과정 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-29-silver-step5-unit.md`
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 2026-10-29 행 전부
- 정본 `step5-units.json` · 결정 `step5-decisions.json`(technique_compat · product_link_rule · product_evidence) · `step5-apply.py` · `step5-fixture-test.py` · `step5-fixtures/` · 검수 `review-step5-report.md` ~ `-v3` · 원천 질문 `step5-origin-questions.md`

## 만들 것
- `procedure-hub-unit-check/SKILL.md` — description: 「새 시술 메뉴 · 원장 항목 · 시장가 · 제품이 들어오거나 바뀌어 단위 시술(계열 × 부위 × 기법)을 세우거나 잇거나, 원천 질문 답이 왔을 때 Procedure Hub 실버 단위 시술 원장(step5-units)을 갱신」. 본문: 언제 · 판정 순서(원장 항목 행선지 → 시술이면 **전부 단위 시술 · 계열이 없으면 계열 판정 스킬로 계열부터** → 키(안 C) → 부위 기본값 · 병변 단위 → 이름 · 동의어 → 붙는 것) · 제품 상속 규칙(기법 근거 · 계열 기법 하나면 계열 기본 · 하위 키 매질만으로 부족한 경우 · 출처가 목적 채우면 잇기 · 확인 불가 = 출처로만 · 도포 가드) · 규칙 체크리스트 + 틀렸던 예(계열 없으면 시술 0 · 버림 · 기법 조건 누락 → 부분 적용 → 하위 키 → 반대 방향 · 성분 미상) · 갱신 방법(결정 한 줄 → step5-apply.py) · **끝 조건: open 0 + 「시술인데 단위 시술 없음 0」 + 「추천 가능 제품인데 단위 시술 0 = 예외 목록뿐」** · 변경 보고
- `references/` — 키 규칙 · 상속 규칙 · 레코드 스키마 + 실제 행 · 틀린 사례 · 원천 질문 다루는 법
- `scripts/check_units.py` — 읽기만: 원장 521 행선지 셈 · 시술인데 키 없음 0 · 상속 쌍 기법 근거 · 추천 가능 제품 단위 시술 0 목록 · open → JSON. 실제 원장으로 1회 돌려 README 에. 가상 문장 시험 넣지 마라
- 기존 스킬 연결 한 줄씩: product-check(새 제품 → 단위 시술 상속은 unit-check) · family-check(새 계열은 unit-check 의 계열 없는 시술에서 옴) · technique-check(장비 속성 = 상속 근거) · `README.md` 지도 · 설치 명령(실행 안 함)

## 금지
사용자 Claude 설정 · 전역 설치 · 원장 · 결정 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_640abbc8-39da-4231-8b49-c70a48995e58 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: 단위 시술 판정 스킬" \
  --body "파일 목록 / 스크립트 실행 결과 / 설치 명령"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] tool_dev 완료 — 단위 시술 판정 스킬. 상세는 인박스." --enter
```
