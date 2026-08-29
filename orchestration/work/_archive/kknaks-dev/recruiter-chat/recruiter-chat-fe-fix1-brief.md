
# [frontend] 리뷰 반영 수정 1차 — retry 경로 전환 · 토큰 밖 색 (WORK-024 후속)

너는 아까 WORK-024 를 구현한 **kknaks-dev `frontend` 워커**다. 리뷰가 나왔고 spec 이 **v0.0.5** 로 개정됐다. 아래 수정만 한다.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat` (기존 변경 위에 계속)
spec: `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/20-spec/spec-017-recruiter-chat.md` (§3 S-8 3항 · §4 API 표)

## 수정 목록

1. **G1 (W6 — 계약 변경)**: 「다시 시도」를 신규 `POST /api/chat/conversations/{id}/messages/{message_id}/retry` 로 전환. 성공 응답은 200 `{message: assistant(pending)}` — 그 자리의 failed 메시지가 pending 으로 되돌아간다(새 줄 없음). mock 에도 같은 동작 반영. BE 워커가 지금 병렬로 구현 중이다 — 계약대로 만들고 기다리지 마라.
2. **G2 (W7)**: `components/admin/chat-exposure-toggle.tsx:66` 의 `var(--danger, #e5534b)` 에서 fallback hex 제거 — `var(--danger)`.

## 검증

```
cd app/front && npx tsc --noEmit (만진 파일 0 에러). 검증은 1회만
```

## 완료 보고 — 기존과 같은 2채널. 핸들은 dispatch preamble 값이 우선.

```bash
orca orchestration send --to term_53806a6d-ced5-4948-88bd-4181b7ba4323 --from <네 워커handle> \
  --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> \
  --subject "frontend fix1 완료: <한 줄>" --body "G1·G2 요약 / tsc 결과"
orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 \
  --text "[worker_done] frontend fix1 완료 — <한 줄>. 상세는 인박스." --enter
```
