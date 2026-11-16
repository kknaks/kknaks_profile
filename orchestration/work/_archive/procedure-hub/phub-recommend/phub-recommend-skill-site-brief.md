# [tool_dev] 스킬화 — 부위 판정 · 실버 부위 원장 갱신

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 만들 곳 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/` — 이미 있는 `procedure-hub-product-check/` · `procedure-hub-family-check/` · `README.md` 를 먼저 읽고 **같은 형식**으로.

## 원천 (실제로 한 방법을 옮긴다 — 지어내지 않는다)
- 과정 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-28-silver-step3-site.md`(규칙 · 틀린 것)
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 10-28 3단계 행 전부 — 특히 **부위 = 「어디에 맞냐」 = 몸 겉 · 원천은 이름 칸만 · 해부학 용어 = 기법 · 작용기전 · 안전 · 이름 2벌 · 끝 조건 = 지금 원천 기준(가상 문장 시험 안 함)**
- 정본 `step3-sites.json` · 결정 `step3-decisions.json`(name_fields 17) · 사전 `step3-lexicon.json` · `step3-apply.py` · `step3-fixture-test.py` · `step3-fixtures/` · 검수 `review-step3-report.md` ~ `-v5`

## 만들 것
- `procedure-hub-site-check/SKILL.md` — description: 「새 원천 · 새 시술 메뉴 · 기존 이름 칸이 바뀌어 부위 문자열이 새로 생기거나, 부위 노드 · 동의어 · 전문의 용어를 바꿀 때 Procedure Hub 실버 부위 원장(step3-sites)을 갱신」. 본문:
  1. 언제 — ① 원천 새 스냅샷 · 새 메뉴 ② step3-apply.py 가 open 을 냄 ③ 의료진 · 원장님 답(질문 35) ④ 노드 추가 요청
  2. 판정 순서 — 이름 칸인가(설명 문장이면 부위 아님) → 몸 겉에서 가리키는 자리인가 → 기존 노드 동의어 / 부위+다른 축(D-07) / 새 노드(D-05 쪼개는 규칙) / 부위 아님(행선지)
  3. 규칙 체크리스트 + 틀렸던 예(설명 문장 범위 확대 · 가상 문장 루프 · 치골궁 · 지방흡입술 → 입술 · 코조각주사)
  4. 갱신 방법 — 결정 파일(step3-decisions.json) 한 줄 · 사전(step3-lexicon.json) 패턴 → step3-apply.py 재실행(결정론) → open 0 · fixture
  5. 출력 — 변경 보고
- `references/` — 노드 53 표(일반인 · 전문의 용어 · 상위 · 위험 부위) · 이름 칸 17 · 레코드 스키마 + 실제 행 · 틀린 사례
- `scripts/` — 있으면: 원장 점검(이름 칸 전수 재추출 → 결정 없는 문자열 = open · 노드 근거 · 전문의 용어에 근육 · 뼈 · 혈관 0) → JSON. 실제 원장으로 1회 돌려 결과를 README 에. **가상 문장 · 해부학 목록 확장 시험은 넣지 마라**
- `procedure-hub-family-check/SKILL.md` 갱신 절에 「부위 판정은 site-check」 한 줄 연결(다른 내용 바꾸지 마라) · `README.md` 지도 · 설치 명령(실행 안 함)

## 금지
사용자 Claude 설정 · 전역 스킬 설치 · 원장 · 결정 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_330a3bf4-0c3f-4d81-b3bc-c20ed1c43b1d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: 부위 판정 스킬" \
  --body "파일 목록 / 스크립트 실행 결과 / 설치 명령"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] tool_dev 완료 — 부위 판정 스킬. 상세는 인박스." --enter
```
