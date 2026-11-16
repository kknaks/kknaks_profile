# [researcher] 실버 4단계(기법) 반영 — step4-research 결정대로 기법 원장

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 읽을 것
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 10-28 「4단계 기법 조사 반영」 행(사용자 「추천으로 가자」) · 4단계 시작 행 · 해부학 용어 행
- 조사 `step4-research.json` · `.md`(S1~S12 · 노드 24 · 값 사전 · C 표현 181 · D 넘겨받은 것 · E 계열 기본 18 · F 초안 65 · 충돌 X1~X6)
- 구조 참고(같은 방식으로): `step3-decisions.json` · `step3-lexicon.json` · `step3-apply.py` — **결정은 데이터 파일, 스크립트는 읽기만 · 고정 숫자 assert 없음 · 결정 없는 표현 = open**
- 앞 단계 교훈 `para/projects/company/procedure-hub/log/2026-10-28-silver-step3-site.md` §5: 지도가 정한 칸만 · 가상 문장 시험 없음 · 끝 조건 = 지금 원천 기준 open 0

## 반영
- S1~S12 · J1 안 1 그대로: 기법 노드 24(id · 이름(상담 용어) · 상위 · 의학 용어 · 근거) · 값 사전(층 13 · 펄스 3 · 대상 근육 16 · 박피 · 도구) · 표현 181 행선지 · 넘겨받은 것 14줄 · 계열 기본 기법 18 · 초안 65 대응
- **추가**: 3단계 이름 칸 「표정근」(시장가 「안면 EMS (표정근 강화)」) → 대상 근육 값(4단계) — step3 정본은 고치지 말고 4단계 쪽 넘김 받음 기록 + `step4-source-fix.md` 에 「step3 얼굴 노드 해부학 이름 속성에서 빼기」 한 줄
- 코 층: 콧등 = 골막상 · 코끝 = 연골막상 · 코(묶음) = 둘 다(원천 anatomy nose safe_injection_depth 「골막상 (코뼈 부위) 또는 연골막상 (비첨부)」)
- **J2(DEC-002 예시 문구)**: DEC-002.md 는 고치지 마라. `step4-source-fix.md` 에 「D-02 예시 「HA 필러 · 코 · 피하 주입」 → 「HA 필러 · 코 · 주입」(층 속성: 콧등 골막상 · 코끝 연골막상)」 한 줄(코디가 writer 로 반영)
- 산출: `step4-decisions.json` · `step4-lexicon.json`(필요하면) · `step4-apply.py` · `step4-techniques.json` · `.md` · `step4-source-fix.md` · 고정 시험은 「결정 빼면 open」만
- 끝 조건 open 0 · 결정론 · md 맨 위 셈. step1~3 산출 · DEC · 원천 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_9df45969-2b27-42b6-a3b3-3c63335b19f7 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 4단계 반영" \
  --body "노드 N / 표현 행선지 셈 / open N / 결정론"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 4단계 반영. 상세는 인박스." --enter
```
