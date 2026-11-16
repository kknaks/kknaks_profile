# [writer] 실버 7단계(고민 · 목적 · 추천 조합) 과정 기록 + 5단계 보강

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 1~6단계 기록(`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/` silver-step1~6)과 같은 형식 · 같은 자리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-29-silver-step7-concern.md` · README 지도 한 줄.

## 원천
- 결정 `orchestration/work/phub-recommend/_RESUME.md` §2 2026-10-29 7단계 행 전부(시작 · 조사 반영 J1~J9 · 5단계 보강 G1~G10 · 재검수 v2 · 데이터 끝)
- `step7-research.*` · `step7-decisions.json` · `step7-apply.py` · `step7-concerns.*` · `step7-origin-questions.md` · `step7-source-fix.md` · 검수 `review-step7-report.md` · `-v2` · 브리프 `phub-recommend-step7-*-brief.md` · 5단계 보강(키 143 → 162 · 계열 24 → 27 · 기법 25 → 26 · 앞 워커 터미널 죽어 이어받음)
- 사이트 화면 코드 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/frontend/src/app/recommend` · `optimize` · `compare` · `synergy`

## 담을 것
1. 왜 — 고민 트리 「항목」 117 중 96 이 시술 이름 · 고민 표현이 원천 7곳에 다른 말로 · 사이트 「추천 패키지」 · 목적과 고민 경계
2. 전후 — 수치(고민 117 → 55 · 대응 249 · 사람 확인 88 · 목적 13 · 엣지 523 · 추천 조합 79 · 8단계 메모 245 · 5단계 보강) + 같은 것 전/후 6~8(레이저토닝(고민 항목 → 엣지) · 쁘띠시술 추천 패키지 · 피부결 · 자갈턱 · 제모 · 바디 CC → 바디 RF(F2) · 엔더몰로지 · 모발이식)
3. 정한 규칙 — 고민 정본 = taxonomy problem · 완전 일치만 자동 · 나머지 게이트 · 시술 이름 항목은 엣지 · 목적 노드 · 엣지는 원천 구조만(적응증 아님) · 부위로 내림 · 그 부위 단위 시술 없으면 후보 전부 + 표시 · 추천 조합 원천별 · 영업 문구 기본 제외 · 사이트 용어
4. 과정 — 조사 → 판단 표 → J7 로 5단계 보강(G1~G10 표 한 번) → 반영(워커 교체) → 검수 2판
5. 틀린 것 — 완전 일치 판정 꼬리말(F1) · 부위 밖 내림(F2) · 경로마다 다른 처리(W2) · 질환 이름 동의어 모호 표시(W3)
6. 남은 것 — 사람 확인 88(게이트) · 원천 질문 90 · 원천 수정 후보 24 · 8단계 메모 245 · 이중턱 노드 둘
- 실명 · 키 금지 · 수치는 파일에서 다시 셈 · 추정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_0f037b22-9d92-4088-a1a2-265bd9f851e3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: 7단계 고민 기록" \
  --body "경로 / 섹션 / 전후 수치"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] writer 완료 — 7단계 고민 기록. 상세는 인박스." --enter
```
