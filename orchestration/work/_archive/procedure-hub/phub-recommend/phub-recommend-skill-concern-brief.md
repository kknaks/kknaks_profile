# [tool_dev] 스킬화 — 고민 · 목적 · 추천 조합 판정 · 실버 7단계 원장 갱신

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 만들 곳 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/` — 이미 있는 스킬 6개와 `README.md` 를 먼저 읽고 **같은 형식**으로.

## 원천
- 과정 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-29-silver-step7-concern.md`
- 결정 `orchestration/work/phub-recommend/_RESUME.md` §2 2026-10-29 7단계 행 · 정본 `step7-concerns.json` · 결정 `step7-decisions.json` · `step7-apply.py` · 고정 시험 · 검수 `review-step7-report.md` · `-v2`

## 만들 것
- `procedure-hub-concern-check/SKILL.md` — description: 「새 고민 · 고민 표현 · 추천 조합(추천 패키지 · 레시피 · 최적화 · 비교)이 들어오거나 바뀌거나, 대응표 사람 확인(게이트) 답이 왔을 때 Procedure Hub 실버 고민 원장(step7-concerns)을 갱신」. 본문: 언제 · 판정 순서(고민 정본 = taxonomy problem → 시술 이름 항목은 엣지 · 고민 대응(완전 일치만 자동 · 나머지 게이트) · 목적 vs 고민 · 엣지는 원천 구조만(적응증 아님) · 부위로 내림 · 그 부위 단위 시술 없으면 후보 전부 + 표시 · 고민 부위 없음 표시 · 추천 조합 원천별 · 영업 문구 기본 제외 · 사이트 용어) · 체크리스트 + 틀렸던 예(F1 꼬리말 완전 일치 · F2 부위 밖 · W2 경로별 처리 · W3 질환 이름) · 갱신(결정 한 줄 → step7-apply.py · 시술이 없으면 unit-check 로) · 끝 조건 · 변경 보고 · 게이트 답 반영 방법
- `references/` · `scripts/check_concerns.py`(읽기만 — 자동 대응 = 완전 일치만 · 엣지 부위 검사 · 엣지 원천 구조 실재 · 적응증 유래 0 · open · 고정 숫자 쓰지 않기) → 실제 원장 1회 실행 결과를 README 에
- unit-check · package-check SKILL.md 에 연결 한 줄씩 · README 지도 · 설치 명령(실행 안 함) · 문서에 고정 숫자 박지 마라

## 금지
사용자 Claude 설정 · 전역 설치 · 원장 · 결정 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_16aedc7e-5d75-445b-a5bb-4c08bb2a1b5f \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: 고민 판정 스킬" \
  --body "파일 목록 / 스크립트 실행 결과"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] tool_dev 완료 — 고민 판정 스킬. 상세는 인박스." --enter
```
