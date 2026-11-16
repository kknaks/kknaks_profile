# [tool_dev] 실버 질문 페이지 v2 — 게이트 탭 없앰 · 8단계 질문 더함

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 고칠 것: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/silver-questions.html` · `silver-questions.json`(v1 — 앞 지시 `phub-recommend-questions-page-brief.md`). 코디가 **같은 URL 로 다시 게시**한다.

## 바뀐 것(10-29 · `_RESUME.md` §2)
- 7단계 사람 확인 게이트 88 → **0**(규칙으로 닫힘) · 7단계 원천 질문도 다시 셈(`step7-origin-questions.md` 지금 판) → **게이트 탭 삭제**
- 8단계 원천 질문 `step8-origin-questions.md` · `step8-relations.json` origin_questions **18** 을 받는 사람대로 의료진 · 병원 탭에 더함. 충돌 질문은 원문 값 둘(이상)을 나란히 보여 주고 [A / B / 조건별로 둘 다 맞음(메모) / 모름] 또는 입력
- 1~7단계 의료진 · 병원 질문 중 지금 결정표 · 산출로 **이미 닫힌 것은 뺀다**(예: s7-Q7-01 보톡스 풀페이스가 아직 열린지 산출에서 확인) — 빼는 근거 한 줄씩 json 에
- 맨 위 문구 「8단계 질문은 나중에 더해진다」 삭제 → 「1~8단계 질문」 · 탭별 개수

## 지킬 것
- **이미 저장된 답 보존**: 남는 항목의 id 는 v1 과 같게(db `answers/<id>` 가 그대로 이어지게). 빠진 항목 id 목록을 json `removed_ids` 에
- 스타일 · 저장 방식 · 테마 토큰 v1 그대로 · node 구문 검사 · U+FFFD 0 · jsdom 스모크
- 실명 · 키 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_2b987ac1-9134-4fe8-9507-b79fb361deef --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "tool_dev 완료: 실버 질문 페이지 v2" --body "탭별 항목 수 / 뺀 N · 더한 N / 검사 결과"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] tool_dev 완료 — 실버 질문 페이지 v2. 상세는 인박스." --enter
```
