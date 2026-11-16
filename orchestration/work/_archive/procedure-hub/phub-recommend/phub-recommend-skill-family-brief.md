# [tool_dev] 스킬화 — 계열 판정 · 실버 계열 원장 갱신

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 만들 곳 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/` — 이미 있는 스킬 `procedure-hub-product-check/` 와 `README.md` 를 먼저 읽고 **같은 형식**으로.

## 사용자 요구(10-28)
새 제품이 들어오거나 기존 제품이 수정되면 업데이트하는 구조. 1단계(제품 확인) 스킬 다음 단계로 **계열 판정**.

## 원천 (실제로 한 방법을 옮긴다 — 새로 지어내지 않는다)
- 과정 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-28-silver-step2-family.md`(규칙 · 흐름 · 틀린 것)
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 10-28 행 · 정본 `step2-families.json`(families 18 · 하위 칸 · product_family 레코드 스키마 · also_families · also_sub_families · evidence_level · pending_director · conflict · technique_hint · deferred) · `step2-apply.py` · 기준 문헌 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/literature-evidence.json`
- 조사 · 검수 `step2-research.*` · `step2-open-resolve.*` · `review-step2*-report.md`

## 만들 것
- `procedure-hub-family-check/SKILL.md` — description: 「새 제품 · 수정된 제품(허가 품목 · 원천 설명 변경)의 계열 · 하위 계열을 정하거나, 계열 정의 · 하위 칸을 바꿀 때 Procedure Hub 실버 계열 원장(step2-families)을 갱신」. 본문:
  1. 언제 — ① 제품 확인 스킬로 새 행이 생김 ② 기존 행의 허가 품목 · 원천 설명 · 정체가 바뀜 ③ 원장님 · 병원 답(pending_director · 근거 약 확인 질문) ④ 계열 · 하위 칸 추가 요청
  2. 판정 순서 — 허가 품목명 · 사용목적 → 원천 설명 → 제조사 사양 → 문헌 정의 대조 → 주 + 보조 → 근거 수준
  3. 판정 규칙 체크리스트(2단계 규칙 전부 + 「틀렸던 예」 한 줄씩) — 새 계열 · 새 하위 칸을 세우는 조건 포함
  4. 갱신 방법 — step2-apply.py 입력에 결정 추가 → 재실행(결정론) · 지우지 않고 표시 · 변경분만 결정 목록(승인 / 원천 질문 / 최종 판단) · 검수 끝 조건 = open 0
  5. 출력 형식 — 변경 보고
- `references/` — 계열 18 정의 · 하위 칸 표(근거 PMID 포함) · 레코드 스키마 + 실제 행 발췌 · 틀린 사례
- `scripts/` — 있으면: 원장 점검(product_family 전수: family/sub_family 가 정의된 칸인지 · also_* 코드 유효 · open 0 · step1 active 와 행 일치 · evidence_level 약 목록) → JSON. 실제 원장으로 1회 돌려 결과를 README 에
- `procedure-hub-product-check/SKILL.md` 의 갱신 절에 「새 행 → 계열 판정은 family-check」 한 줄 연결(다른 내용 바꾸지 마라)
- `README.md` 지도 갱신 · 설치 명령(실행 안 함)

## 금지
사용자 Claude 설정 · 전역 스킬 설치 · 원장 · 결정 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_d1f98233-f7cc-48f1-8b7d-15b1ea0f3345 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: 계열 판정 스킬" \
  --body "파일 목록 / 스크립트 실행 결과 / 설치 명령"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] tool_dev 완료 — 계열 판정 스킬. 상세는 인박스." --enter
```
