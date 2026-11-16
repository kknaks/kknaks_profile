# [reviewer] 실버 2단계 최종 검수 v4 — open 해결안 반영 · 끝 조건 open 0

너는 v1~v3 를 검수한 reviewer 다(read-only · 산출 리포트 1개). 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.
**이번 판의 끝 조건: `step2-families.json` open[] = 0** — 검수 PASS 는 이것까지 확인해야 나온다. 남는 것은 원장님 문의 3행(pending_director)뿐이어야 한다.

- 결정: `_RESUME.md` §2 10-28 「하위 계열도 주 · 보조로」 · 「2단계 open 40 해결안 반영」 행
- 해결안 `orchestration/work/phub-recommend/step2-open-resolve.json` · `.md` · 지시 `phub-recommend-step2-final-apply-brief.md`
- 볼 것: ① 37행이 해결안 값 그대로(주 · 보조 · 새 하위 칸 2 · conflict 6) ② 근거 약 9행 = 값 + evidence_level 약 + confirm_question ③ pending_director 3(알렉스필 · 더마큐어 · 벨르업) = family null · 1단계 확인 불가 그대로 · 질문 ④ open 0 · 모든 sub_family / also_sub_families 가 families 정의 칸 안 · also_families 유효 ⑤ 해결안 근거 표본이 아니라 **강 28행 전수** 출처 대조(원천 · 허가 · URL) ⑥ 352 셈 · 결정론 · 회귀(v3 PASS 항목 · 이번에 안 건드린 행이 바뀌지 않았는지) ⑦ step2-origin-questions.md 두 절
- 산출 `orchestration/work/phub-recommend/review-step2-v4-report.md` · 맨 위 PASS/FAIL + 「open = N」

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_e935d4d1-c970-4194-b5ff-68be7a928cc5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 2단계 최종 검수 v4 <판정>" \
  --body "open N / FAIL N / WARN N / 회귀 N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 2단계 최종 검수 v4 <판정>. 상세는 인박스." --enter
```
