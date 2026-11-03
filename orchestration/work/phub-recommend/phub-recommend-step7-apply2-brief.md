# [researcher] 실버 7단계 반영 이어서 — 앞 워커 터미널이 죽음

너는 맥락이 없다. 앞 워커가 `phub-recommend-step7-apply-brief.md` 를 하다가 멈췄다. **처음부터 다시 하지 말고 파일에 남은 상태에서 이어라.**
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md` · 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`
- 먼저 읽을 것: 원래 지시 `phub-recommend-step7-apply-brief.md` · 조사 `step7-research.md` · 결정 `_RESUME.md` §2 2026-10-29 「7단계 조사 반영」 · **「5단계 보강(J7) G1~G10 — 전부 추천대로」** 행
- 앞 워커가 한 것(파일로 확인해라): 5단계에 규칙분(제모 부위 8 · 바디 RF 1) 반영(`step5-units.json` 17:23) · `step7-decisions.json`(17:28) 초안 · 「전부 추천이면 dry-run open 0」까지. G1~G10 질문 원문은 아래

## 남은 일
1. **G1~G10 전부 추천대로 반영**: G1 M9 · M8 정의 대상 넓힘(땀샘 · 피하지방) · 키 3(겨드랑이 마이크로웨이브 · 바디 HIFU · 바디 레이저 지방분해 — 매질 미지정) / G2 M8 하위 엑시머 + 키 / G3 M8 하위 협대역 UVB + 정의 「자외선 광선」 + 키 / G4 N4 · 다리 · K01 다리 경화요법 / G5 N4 정의 냉동 파괴 · 4단계 N4 also K08 · 병변 냉동치료(병변 단위) / G6 새 계열 N8 기계적 흡입 마사지 · 4단계 새 기법 흡입 마사지 · 바디 흡입 마사지 / G7 새 계열 N9 모발이식 · 두피 · K12 · surgery 표시 / G8 새 계열 N10 지방흡입 · 바디 · K12 · surgery 표시 / G9 IPL 제모 = U5-030 · 100 · 101 후보 동의어(새 키 없음) / G10 트라넥삼산 경구 = 시술 아님 · 주사 = U5-018 후보 동의어 + 원천 질문. 각 PMID 는 조사 · 질문에 적힌 것(실재 확인됨) — 2단계 계열 · 정의 · 하위 · 4단계 기법은 각 단계 결정 파일 → apply 재실행
2. **7단계 완성**: 원래 지시 2 그대로(`step7-concerns.json` · `.md` · 원천 질문 · 원천 수정 후보 · 고정 시험)
3. 끝 조건: 2 · 4 · 5 · 7 재실행 · open 0 · 결정론 · 스킬 점검(family · technique · unit · package — `reference/2026-10-27-skills-procedure-hub/*/scripts/check_*.py`) 오류 0 · md 맨 위 셈

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_772590ba-f374-45c4-b667-a1e8fad5de0b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 7단계 반영" \
  --body "5단계 키 N · 계열 N · 기법 N / 고민 N / 대응 N / 목적 N / 엣지 N / 추천 조합 N / open N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 7단계 반영. 상세는 인박스." --enter
```
