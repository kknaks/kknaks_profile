
# [frontend] fix3 — 어드민 product(회사 제품) 목록에 chat_exposed 토글

너는 WORK-024 의 **kknaks-dev `frontend` 워커**다. 회사 제품이 chat tool 표면에 추가되면서(spec **v0.0.8** — `list_company_products`/`get_company_product` + `product.chat_exposed`) 어드민 토글 대상이 하나 늘었다. 이것만 한다.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat`

## 수정

1. **product 어드민 목록 화면**(WORK-018 이 만든 제품 레지스트리 관리 화면 — 위치는 `app/front/app/admin/` 아래에서 찾아라)에 기존 careers/projects/problems 와 **같은 방식**으로 `chat-exposure-toggle` 을 단다.
2. API 계약: `PATCH /api/admin/chat-exposure/product/{id}` — BE 워커가 지금 병렬 구현 중이다(kind 만 다르고 동작 동일). 목록 응답의 `chatExposed` 필드도 BE 가 싣는다. 계약대로 만들고 기다리지 마라.

## 검증

```
cd app/front && npx tsc --noEmit (만진 파일 0 에러). 검증은 1회만
```

## 완료 보고 — 2채널, 핸들은 preamble 우선

```bash
orca orchestration send --to term_53806a6d-ced5-4948-88bd-4181b7ba4323 --from <네 워커handle> \
  --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> \
  --subject "frontend fix3 완료: <한 줄>" --body "수정 요약 / tsc"
orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 \
  --text "[worker_done] frontend fix3 완료 — <한 줄>. 상세는 인박스." --enter
```
