# [tool_dev] 스킬화 — 제품 탐색 · 허가 확인 · 실버 제품 원장 갱신

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 만들 곳 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/`(비어 있음).

## 사용자 요구(10-28)
「지금 제품 탐색 어떻게 했는지 스킬화 — **새 제품이 들어오거나 수입금지(허가 취소 · 취하 · 만료 등)된 걸 업데이트할 때** 확인하고 실버를 업데이트해야 한다」

## 원천 (읽어라 — 실제로 한 방법을 스킬로 옮긴다, 새로 지어내지 않는다)
- 과정 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-28-silver-step1-product-normalization.md`(규칙 13 · 흐름 · 출처 · 틀린 것 8)
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 결정표 · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json`(레코드 스키마 — 칸 이름 · 상태 6종 · recommendable · line/lines · merged_into · moved_to · history · reference · license_basis)
- 브리프 · 결과: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/phub-recommend-*-brief.md`(d09 · d12 · d17 · d18 · d19 · cancel-recheck · domestic7 · apply · final-apply) · `step1-*-web.md` · `step1-export-recheck.json` · `step1-apply.py`
- 도구 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp/NOTES.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-28-kpic-mcp/NOTES.md`

## 스킬 구성 (Claude Code 스킬 형식: 폴더 + SKILL.md frontmatter name · description)
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/procedure-hub-product-check/SKILL.md` — description 은 「새 시술 제품 추가 · 허가 상태 변경(취소/취하/만료/수출용/재제조) 반영 · 정기 점검으로 Procedure Hub 실버 제품 원장을 갱신할 때」로 트리거되게
- 본문(짧고 단계형):
  1. **언제** — ① 새 제품 1건 추가 ② 정기 점검(전체 허가 상태 재조회 · 변경분만) ③ 외부 소식(수입 중단 · 철수 · 허가 취소 보도)
  2. **찾는 순서** — 이름(한/영 · 띄어쓰기 · 점 표기 변형) → **업체명(제조 · 현 수입사 · 이전 수입사)** → 모델명 → 품목 · emedi 상세(xprtppYn · 비고 · 모델 목록 · 사용목적) → 의약품은 KPIC(이름 · 성분 역조회) → 국내 유통(피부과 홈페이지 · 병원 가격 자료 · 공식 · 보도) → 해외 공식(FDA 등, 국내 허가 증거 아님)
  3. **판정 규칙** — 1단계 규칙 13개를 체크리스트로(정상만 연결 · 이력 · 수출용 → 같은 업체 내수 허가 재탐색 · 재제조 · 비침습 ≠ 허가 대상 아님 · 허가번호 미확인 · 이름 3칸 · 라인/품목 · 업체 역할 여러 개 · 1단계는 제품↔허가만 · 추정 금지) + 각 규칙의 「틀렸던 예」 한 줄
  4. **갱신 방법** — 레코드 스키마대로 행 추가/변경 · 지우지 않고 표시(merged_into · moved_to · history) · apply-log 한 줄 · 변경분만 결정 목록(승인 / 원천 질문 / 최종 판단) · 검수
  5. **출력 형식** — 변경 보고(신규 · 상태 변경 · 추천 여부 변경 · 사람에게 물을 것)
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/procedure-hub-product-check/references/` — 규칙 상세 · 레코드 스키마 예(실제 행 2~3개) · 질의 패턴(MFDS API · emedi POST · KPIC tool 이름과 입력) · 틀린 사례
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/procedure-hub-product-check/scripts/` — 있으면: 정기 점검용 허가 상태 재조회 스크립트(원장의 연결 허가 전부 → MFDS 상태 · xprtppYn 재조회 → 변경분 JSON). 키는 `reference/2026-10-27-mfds-mcp/.env` 를 읽기만 · 출력 · 커밋 금지. 실제로 원장 10행 정도로 1회 돌려 동작 확인
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/README.md` — 이 폴더 지도 · 설치(~/.claude/skills 또는 프로젝트 .claude/skills 로 복사/링크하는 명령만 적기 — 실제 설치는 하지 않음)

## 금지
- 사용자 Claude 설정 · 전역 스킬 설치 건드리지 않기 · 키 값 출력 · 원장 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: 제품 확인 스킬" \
  --body "파일 목록 / 스크립트 실행 결과 / 설치 명령"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] tool_dev 완료 — 제품 확인 스킬. 상세는 인박스." --enter
```
