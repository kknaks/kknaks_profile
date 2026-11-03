# [researcher] 실버 7단계 검수 FAIL 2 · WARN 3 수정

(맥락 없으면 `review-step7-report.md` 부터 · `step7-apply.py` · `step7-decisions.json`. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`)

리포트 「고칠 것」 그대로 — 새 사용자 결정 없음(이미 있는 규칙):
1. **F1**(R5 「완전 일치만 자동」): 대응표 #133 · #177 · #218 · #229 → human_check true · 확인 대기 · match_class 를 해당 갈래로. 원인 고침: problem-combos 행 human_check 를 상하위만이 아니라 「완전 일치 아님」 전부로 · 꼬리말 붙은 원천 말은 완전 일치로 적지 않음. **같은 성격 전수**: 249행 전부 「원천 말 == 대상 이름(정규화)」 아니면 자동 아님인지 다시 판정
2. **F2**(「부위로 내림」): `_resolve` sfilter — 이름 · 동의어 · 제품으로 잡은 단위 시술이 앵커 부위와 안 맞으면 같은 계열을 `units_at(계열, 부위)` 로 내림 · 그래도 없으면 W2 경로. P12 바디 CC 9 → U5-152 등 · P13 두피 CC 5 → U5-042 만인지 확인. **같은 성격 전수**: 523 엣지 전부 「단위 시술 부위 ∈ 앵커 부위(또는 하위)」인지 검사를 apply 에 넣기(어긋나면 open)
3. **W1**: 압출 · PDT · 두피엑소좀 ⑤ 엣지 3 에 계열 코드 어긋남 표시 + `step7-source-fix.md` 추가(24)
4. **W2**: 「부위 있는데 그 부위 단위 시술 없음」 = R8 대로 **계열 후보 전부 + no_unit_at_site** 로 통일(① · ③ 계열 코드 경로 포함) — 결정 파일에 규칙 문장
5. **W3**: U5-156 · U5-157 동의어 「백반증」 · 「건선」 ambiguous true(5단계 결정 → step5-apply 재실행)
6. W4 는 기록만(md 「남은 것」)
7. 5 · 7 재실행 · open 0 · 결정론 · 고정 시험(F1 · F2 케이스 추가) · 스킬 점검 4종 · md 셈

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_772590ba-f374-45c4-b667-a1e8fad5de0b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 7단계 검수 수정" \
  --body "사람 확인 N / 엣지 N · 부위 밖 0 / open N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 7단계 검수 수정. 상세는 인박스." --enter
```
