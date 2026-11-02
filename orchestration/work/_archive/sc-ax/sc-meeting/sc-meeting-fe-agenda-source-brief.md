# [frontend] D38 — 안건 출처 라벨 다섯 (기획 넷 + AI 정리)

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`. `frontend/` 만. 커밋 금지.

## 할 것 (사용자 결정 D38, 2026-09-11 — 기획 screen-005 E21 의 넷을 받아들임)
- `Agenda.source` 값이 다섯이 된다: `manual`(직접 입력) · `set`(세트) · `carried`(지난 회의에서 넘어옴) · `derived`(다른 회의에서 파생) · `ai`(AI 정리). 표시 라벨을 `labels.ts` 에 다섯으로(문구는 기획 원문 그대로: 「직접 입력」·「세트」·「지난 회의에서 넘어옴」·「다른 회의에서 파생」, AI 는 「AI 정리」 유지). 모르는 값은 빈 라벨(깨지지 않게).
- 안건 블록·AI 요약 탭·패널·회의록 등 출처를 그리는 자리 전부 같은 함수를 쓰게. 기획 E21 「상태와 무관하게 늘 낸다」 — 완료된 회의에서도 출처가 보이는지 확인(안 보이면 보이게).
- 테스트 1(다섯 라벨 + 모르는 값).

## 검증
```
cd frontend && npx tsc --noEmit + npx vitest run src/meetings/. 서버·5176 금지.
```

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 안건 출처 라벨 다섯(D38)" \
  --body "변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — 안건 출처 라벨. 상세는 인박스." --enter
```
