# [writer] 기록 2 · 스킬 갱신 · 시맨틱 스킬 새로 (10-29 저녁 ~ 10-30)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 1~8단계 기록(`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/`) · 스킬(`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/`)과 같은 형식 · 같은 자리.

## 만들 것
1. 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-30-silver-step7-site-rules.md` — 7단계 부위 규칙 R21~R27 + 전수 눈검: 왜(사용자가 연결 구조 페이지에서 이중턱 → 겨드랑이 마이크로웨이브 · 목주름 → 관자놀이 필러 발견) · W2 「후보 전부」 규칙이 틀린 이유 · R21(상위 부위 · 층 해석 B) · R22(고민 영역) · 전수 눈검 105/36 · R23~R27 · 판단 ①~③ · R7 재생 PRP · 전후 수치(엣지 537 → 427 등) · 틀린 것 · 남은 것. 원천: `step7-siteup-report.md` · `review-step7-sweep.md` · `step7-sweepfix-report.md` · 브리프 `phub-recommend-step7-siteup|sweepfix|r7-brief.md` · `_RESUME.md` §2 10-29 ~ 10-30 행
2. 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-30-semantic.md` — 시맨틱 정의: 왜(층 정의 · 흩어진 사전) · 조사 → 결정(B1~B12 · U1~U3 · 부작용 ≠ 합병증) → 반영 · 노드 13 · 엣지 21 · 사전 · id 대응 · 상속 9 · 합병증 65 → 35 · 부작용 72 · 남은 것. 원천: `semantic-research.md` · `semantic.md` · `semantic.json` · 브리프 `phub-recommend-semantic-*-brief.md`
3. README 지도 두 줄
4. 스킬 갱신: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/procedure-hub-concern-check/SKILL.md` — R21~R27 · 판단 ①~③ · R24 레시피 설명 칸(스크립트 · references 는 이미 고쳐짐 — 설명서만 맞춤)
5. **새 스킬** `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/procedure-hub-semantic-check/`(SKILL.md · scripts/check_semantic.py · references/ — 앞 스킬과 같은 꼴): 실버가 바뀌면 `semantic-build.py` 재생성 · 결정론 · 노드/엣지 종류 셈 · 사전 겹침 · id 대응 빠짐 · 표시 · 상속 규칙 점검 · 틀린 값 넣어 잡히는지(selftest) · README 에 한 줄
- 실명 · 키 금지 · 수치는 파일에서 다시 셈 · 실버 · 시맨틱 데이터 수정 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_363934f5-5539-4df1-93f6-dffb7146b6c9 --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "writer 완료: 기록 2 · 시맨틱 스킬" --body "경로 / 스킬 selftest 결과"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] writer 완료 — 기록 2 · 시맨틱 스킬. 상세는 인박스." --enter
```
