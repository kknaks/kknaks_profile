# [researcher] 실버 5단계(단위 시술) 반영 — 앞 단계 정본 보강 포함

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 결정 (정본 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 2026-10-29 행 전부)
- 「5단계 원칙: 클리닉에서 하는 시술은 전부 단위 시술」 행 — step5-research 재추천(J1 안 C · J2 · F1~F3 · F5~F9)
- 「5단계 추가 조사 반영」 행 — step5-research2 U1~U9 + 보정(카복시 · 프로락틴 · 에이팩 · MPE · 이모드)
- F4 의 나머지(사파이어 · 에이팩 · MPE · 이모드 · 수소토닝)는 research2 행선지대로
- 근거: `step5-research.json` · `.md` · `step5-research2.json` · `.md`

## 순서 — 앞 단계 정본을 먼저 고친다 (각 단계의 결정 파일 · 스크립트로 · 결정론 유지)
1. **1단계**: U8 듀오 하이드로젠(new-DEV-041) active 되살림 · U9 파셀라 새 제품 행(허가 못 찾음 = 상태는 1단계 규칙대로) — `step1-apply.py` 입력 · 재실행
2. **2단계**: 계열 N2~N7 추가(이름 · 정의 · 근거 PMID · name_status · evidence_level) · 2단계 「계열 밖」이던 태반 2 · 성장호르몬 · 헤어셀 행을 N5 · N6 · N7 로 · 파셀라 행 M9 — `step2-apply.py` 의 고정 assert(계열 18 등)는 결정에서 계산하도록 바꿔도 된다(바꾼 것 기록)
3. **4단계**: K13 「미세색소주입」 노드 · K06 정의 넓힘 · 계열 기본 기법 N2~N7 — `step4-decisions.json` → `step4-apply.py`
4. **5단계**: 3단계 구조와 같게 `step5-decisions.json` · `step5-apply.py` → `step5-units.json` · `.md`(단위 시술 키 · 이름 · 동의어 · 쓰는 제품 · extracted 붙임 · 시장가 시술 1회 · PIH · 운영 정보 · 4단계 속성 · 원장 521 행선지 · 넘겨받은 것 · 원천 질문 목록 `step5-origin-questions.md`) · 결정 = 데이터 파일 · 고정 숫자 assert 없음 · 결정 없는 것 = open · 고정 시험 「결정 빼면 open」
5. 각 단계 스킬 점검 스크립트로 확인: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/procedure-hub-family-check/scripts/check_families.py` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/procedure-hub-site-check/scripts/check_sites.py` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/procedure-hub-technique-check/scripts/check_techniques.py` — open 0 · 오류 0
- 끝 조건: 1 · 2 · 4 · 5 단계 open 0 · 결정론 · **원장 521 중 시술인 것은 전부 단위 시술(아큐탄 · 성분 17 만 시술 아님)** — 이걸 md 맨 위에 셈으로
- 원천 · DEC 수정 금지 · 결정에 없는 변경 · 추정 금지(성분 미상은 「미상」 그대로)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_c8fcd5df-52e7-4163-8f94-9b880113c6a6 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 5단계 반영" \
  --body "단위 시술 키 N / 원장 521 셈 / 단계별 open / 스킬 점검 결과"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 5단계 반영. 상세는 인박스." --enter
```
