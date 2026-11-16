# [researcher] 실버 3단계 재검수 v2 지적 수정

`review-step3-v2-report.md` N1 · N2 · W-a · W-b 를 리포트 「고칠 값」 그대로 고친다(`step3-lexicon.json` · `step3-decisions.json` · `step3-apply.py`). 원천 · DEC · step1 · step2 수정 금지.

1. **N1**: 입술 패턴 `(?<!흡)입술` · 「지방흡입술」 처리 → 입술 24
2. **N2**: ① morphemes_ko · stems_en 에 리포트 목록 추가 · 「질」은 문맥 패턴 ② 볼 계열 `(?<![귓귀])` ③ bare 「등」 · 「배」 허용을 패턴형 허용으로 ④ **고정 시험(fixture)**: `step3-fixtures/`(원천 사본에 붙일 문장 파일 + 기대 open 목록) + `step3-apply.py --fixture` 또는 별도 `step3-fixture-test.py` — 리포트 T1~T4 문장 전부 + 쇄골 라인 필러(같은 표면 다른 뜻 → 결정 note) · 실행 결과를 md 에
3. **W-a** 리터럴 제거 · **W-b** kind 정정 + 가드(handoff ⇔ kind D-07)
4. open 0 · 결정론 · md 셈 · 바뀐 행

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_16898dfd-67ba-45ea-81ba-e60d37fd48e4 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 3단계 v2 지적 수정" \
  --body "open N / fixture 결과 / 바뀐 셈"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 3단계 v2 지적 수정. 상세는 인박스." --enter
```
