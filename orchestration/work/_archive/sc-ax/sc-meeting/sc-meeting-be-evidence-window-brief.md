# [backend] 회의 중 배치 — 근거 검증 구간을 회의 전체로(D5) · 빠른 시작 자리표시 안건 제목을 AI 가 채움(D6)

너는 **sc-ax backend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`. `backend/` 만. 커밋·재기동 금지. 실물 Codex 호출 금지(대역). **D46(task_244a73093469) 완료 보고 뒤에 이어서.**

## 실물 2회차(09-11) 발견 — 사용자 결정
**D5 시간 칩 소실.** 배치는 매번 AI 트랙 전체를 새로 쓴다(유지). 그런데 `batch.demote_line(covered_ms=…)` 의 근거 검증 구간이 **이번 배치의 미처리 발화 구간**(`application.py` 배치 입력 `covered_ms=(blocks[0].at_ms, max end_ms)`)이라, 앞 배치 구간을 근거로 단 줄은 매번 근거를 떼여 칩이 사라진다(화면에서 최신 구간 줄만 칩 남음). **고침**: 검증 구간 = `(0, 지금까지 적재된 확정 발화의 마지막 end_ms)` — 회의 시작부터 이번 배치 끝까지. 최종 합성의 `(0, max end_ms)` 와 같은 결. 프롬프트의 「이번 구간」 표현이 근거를 이번 구간으로 제한하고 있으면 「회의 전체 발화 중 실제 구간」으로 고친다.

**D6 「안건 1. 안건 1」.** 빠른 시작이 메모 대상용으로 만드는 안건(title "안건 1", source manual)을 §7.3 때문에 AI 가 못 바꿔 자리표시가 제목으로 선다. **고침**: 빠른 시작 안건은 자리표시로 만든다 — `meeting_agendas.title_placeholder BOOLEAN NOT NULL DEFAULT false`(additive, sync-demo-schema) true. 배치 적재에서 `title_placeholder=true` 인 안건은 AI 가 낸 제목으로 갱신(매 배치 최신화, source 는 manual 유지). 사람이 `PATCH /agendas/{id}` 로 제목을 고치면 `title_placeholder=false` 로 떨어져 그 뒤 불변. 상세 응답 Agenda 에 `title_placeholder` 실음(FE 는 나중). 최종 합성은 어차피 안건을 새로 잡으므로 손대지 않는다.

## 검증
`cd backend && uv run pytest -q tests/contract/test_meeting_batch*.py tests/contract/test_meeting_core.py -m 'not integration'`. 테스트로: 2회차 배치가 1회차 구간 근거를 단 줄을 내도 근거가 살아남는다 · 적재 범위 밖(미래 시각) 근거는 여전히 떼인다 · 빠른 시작 안건 title_placeholder=true · 배치가 제목을 채우고 다음 배치가 다시 갱신 · PATCH 제목 뒤엔 배치가 못 바꿈.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: 근거 구간·자리표시 안건(D5·D6)" \
  --body "변경 파일 / 요약 / 검증 수치 / sync-demo-schema 필요 여부 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — D5·D6. 상세는 인박스." --enter
```
