# [tool_dev] 스킬화 — 기법 판정 · 실버 기법 원장 갱신

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 만들 곳 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/` — 이미 있는 `procedure-hub-product-check/` · `-family-check/` · `-site-check/` · `README.md` 를 먼저 읽고 **같은 형식**으로.

## 원천 (실제로 한 방법을 옮긴다)
- 과정 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-28-silver-step4-technique.md`
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 10-28 4단계 행 · source-map 승인 행 · 해부학 용어 행
- 정본 `step4-techniques.json` · 결정 `step4-decisions.json` · `step4-apply.py` · `step4-fixture-test.py` · `step4-fixtures/` · 검수 `review-step4-report.md` · 지도 `source-map.json`(4단계 칸 27)

## 만들 것
- `procedure-hub-technique-check/SKILL.md` — description: 「새 원천 · 새 계열 · 새 장비가 들어와 기법 표현이 생기거나, 기법 노드 · 층 · 대상 근육 · 펄스 같은 속성을 바꿀 때 Procedure Hub 실버 기법 원장(step4-techniques)을 갱신」. 본문: 언제 · 판정 순서(지도가 4단계로 정한 칸인가 → 큰 기법(계열 정의 동사 · mechanism 태그) → 세부 노드(부위 쪼개기 규칙) / 단위 시술 속성(층 · 근육 · 도구) / 장비 속성(펄스 · 박피) / 넘김) · 규칙 체크리스트 + 틀렸던 예(J2 골막상 · 연골막상 · pulse_scope 누락 · md 고정 숫자) · 갱신 방법(결정 한 줄 → step4-apply.py) · 변경 보고
- `references/` — 노드 24 표 · 값 사전 · 계열 기본 18 · 레코드 스키마 + 실제 행 · 틀린 사례
- `scripts/` — 있으면: 원장 점검(지도 4단계 칸 재추출 → 결정 없는 표현 = open · 노드 2층 · 값이 사전 안 · 계열 기본 18 = step2 계열) → JSON. 실제 원장으로 1회 돌려 README 에. **가상 문장 시험 넣지 마라**
- `procedure-hub-site-check/SKILL.md` 갱신 절에 「층 · 대상 근육은 technique-check」 한 줄 연결 · `README.md` 지도 · 설치 명령(실행 안 함)

## 금지
사용자 Claude 설정 · 전역 설치 · 원장 · 결정 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_237b242d-9cf1-41a8-acca-d8e4b35ae629 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: 기법 판정 스킬" \
  --body "파일 목록 / 스크립트 실행 결과 / 설치 명령"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] tool_dev 완료 — 기법 판정 스킬. 상세는 인박스." --enter
```
