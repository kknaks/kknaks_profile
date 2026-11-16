# [researcher] 1단계 제품 원장 — B·C 확인 불가 재조사(emedi) · 세 구간 합치기 · 결정할 것 목록

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 입력 (`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`)
- `step1-products-A.json` · `B.json` · `C.json` (+ 각 .md) — 구간 A 는 **의료기기 전자민원(emedi) 전 모델명 검색**으로 식약처 API 가 못 찾는 허가를 찾았다(방법은 A 의 json/md 질의 기록 참고)
- 브리프 원본 `phub-recommend-step1-A-brief.md`(필드 1~7 · 끝 조건 「미확인 0」)

## 할 일
1. **B · C 의 「확인 불가」(B 35 · C 34)를 A 와 같은 emedi 방법으로 다시 찾는다.** 찾으면 허가 · 업체 역할을 채우고, 못 찾으면 질의 기록을 남겨 「확인 불가」 유지. 식약처 API 는 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp` 패키지(키 출력 금지)
2. 세 구간을 **제품 원장 하나**로 합친다: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` · `.md` — 필드 1~7 그대로, 구간 표시, 중복(같은 허가 · 같은 제품) 정리. 수치 summary
3. **「사람이 정해야 할 것」 목록**을 뽑는다: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-decisions.json` · `.md` — 항목마다 {ledger_id, 제품, 무엇이 부족한가(한 줄), 정할 것(한 줄 질문), 선택지(2~4), 근거 · 후보 요약}. 포함: 구간들의 ⚑/게이트 표시 항목(A 47 · B 22 · C 해당분) · 재조사 후에도 확인 불가인 것 · 기존 결정과 달라진 것(예: 텐쎄라 · 젠틀레이즈 · 디클래씨 · 에이비오톡신) · 현장 기기 원장 추가 여부. **같은 성격은 묶어서** 한 질문으로(예: 「실 메뉴성 이름 15개를 원장에서 뺄까」)

## 제약
- 다른 파일 수정 금지. 키 · 실명 금지. 추정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 1단계 합치기 · 결정 목록" \
  --body "재조사로 찾은 수 / 합친 원장 수치 / 결정할 것 수(묶음 기준)"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 1단계 합치기 · 결정 목록. 상세는 인박스." --enter
```
