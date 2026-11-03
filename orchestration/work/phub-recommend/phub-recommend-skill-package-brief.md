# [tool_dev] 스킬화 — 패키지 판정 · 실버 패키지 원장 갱신

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 만들 곳 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/` — 이미 있는 스킬 5개와 `README.md` 를 먼저 읽고 **같은 형식**으로(분량은 6단계 크기에 맞게 작게).

## 원천
- 과정 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-29-silver-step6-package.md`
- 결정 `orchestration/work/phub-recommend/_RESUME.md` §2 2026-10-29 6단계 행 · 정본 `step6-packages.json` · 결정 `step6-decisions.json` · `step6-apply.py` · `step6-fixture-test.py` · `step6-fixtures/` · 검수 `review-step6-report.md`

## 만들 것
- `procedure-hub-package-check/SKILL.md` — description: 「새 패키지 · 묶음 메뉴 · 회차 패키지 · 시장가 패키지 가격이 들어오거나 바뀌어 Procedure Hub 실버 패키지 원장(step6-packages)을 갱신」. 본문: 언제 · 판정 순서(패키지인가 — 이름 있는 묶음 / 회차 / 시그니처 / 묶음 이름(분류) / 단위 시술(한 장비 · 한 시술) → 구성 = 원천 적힌 시술만(적응증 아님) → 단위 시술 키(없으면 단위 시술 스킬로) → 슬롯 + 원천 질문 → 가격 원문 · 같은 날 원문) · 「패키지」 두 뜻(사이트 추천 패키지 = 7단계) · 시너지는 8단계 · 규칙 체크리스트 + 틀렸던 예 · 갱신(결정 한 줄 → step6-apply.py) · 끝 조건(open 0 · 구성도 질문도 없는 패키지 0) · 변경 보고
- `references/` · `scripts/check_packages.py`(읽기만 — 원천 패키지 행 재추출 · 결정 없는 행 = open · 구성 엣지 원문이 원천 이름 · detail · extracted overview/mechanism 에 있는지 · 키 실재 · 시그니처 노출 · 고정 숫자 쓰지 않기) → 실제 원장 1회 실행 결과를 README 에
- unit-check SKILL.md 에 「묶음 판정은 package-check」 한 줄 · README 지도 · 설치 명령(실행 안 함) · **문서에 고정 숫자 박지 마라**(현재 값 = 스크립트 출력)

## 금지
사용자 Claude 설정 · 전역 설치 · 원장 · 결정 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_38dabbf9-b77e-42ea-adcb-75897e3c6874 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: 패키지 판정 스킬" \
  --body "파일 목록 / 스크립트 실행 결과"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] tool_dev 완료 — 패키지 판정 스킬. 상세는 인박스." --enter
```
