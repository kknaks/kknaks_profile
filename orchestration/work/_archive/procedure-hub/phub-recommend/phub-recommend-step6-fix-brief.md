# [researcher] 실버 6단계 검수 FAIL 1 · WARN 3 — 문구 · 숫자

(맥락 없으면 `review-step6-report.md` 「고칠 것」 부터. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`)

리포트 「고칠 것」 1~4 그대로:
1. **F1**: `step6-decisions.json` non_packages `M9-SIG` · `auto-1775402620` 의 `to` · verdict 를 지금 번호와 셈으로(P6-08 · 09 / P6-12~16 · 「8 중 5 = 패키지 · 리쥬하이 = 단위 시술(U2) · 제네오X · 올타이트 = 1단계 제품」) · `step6-apply.py` 가 non_packages 의 menu_group 대상 id ↔ packages[].menu_group 을 대조해 어긋나면 open
2. **W1**: P6-22~24 notes 「사용자 판단 U4」 → 「U4 결정(10-29)」
3. **W2**: `step5-apply.py` 시장가 사본 문구를 행선지별로(시술 1회 37 · 6단계 1)
4. **W3**: `reference/2026-10-27-skills-procedure-hub/procedure-hub-unit-check/SKILL.md` · `references/inheritance-rules.md` 의 **고정 숫자를 지우고** 「현재 값 = `scripts/check_units.py` 출력」으로(숫자를 다시 박지 마라 — 또 낡는다). 1226 이 된 이유(U2 리쥬란 저장 이동)는 메모로
5. 5 · 6단계 재실행 · open 0 · 결정론 · 고정 시험. 다른 것은 바꾸지 마라

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_91b85aab-8bcc-4e87-bd4c-e346d4952d51 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 6단계 검수 수정" \
  --body "F1 · W1~W3 / open N / 결정론"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 6단계 검수 수정. 상세는 인박스." --enter
```
