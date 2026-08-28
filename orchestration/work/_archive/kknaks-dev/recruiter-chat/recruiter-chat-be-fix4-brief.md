
# [backend] fix4 — 회사 제품 tool 2종 + `product.chat_exposed` (네 fix3 조사의 (b)안 채택)

너는 WORK-023 의 **kknaks-dev `backend` 워커**다. 네 fix3 보고의 후속 결정이 났다 —
**(b) 전용 tool + (3) archive 포함**. spec **v0.0.8** 에 계약으로 반영돼 있다:
`/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/20-spec/spec-017-recruiter-chat.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat`

## 수정 (spec v0.0.8)

1. **migration**: `product` 에 `chat_exposed` boolean 기본 false (다른 셋과 동일 축).
2. **admin**: `PATCH /api/admin/chat-exposure/product/{id}` 허용(kind 확장) + product
   어드민 목록 응답에 `chatExposed` 노출 (careers 등과 같은 방식).
3. **chat-tool API + MCP tool 2종**: `list_company_products`(회사 제품 표면 — 노출 행만,
   product 표에서 **company 소속만**. 소속 구분 컬럼은 코드에서 확인) ·
   `get_company_product(slug)`(showcase md — slug 는 product 의 실제 slug 컬럼).
   tool 설명은 「재직/전 회사에서 만든 제품」임이 모델에게 분명하게.
4. **경로 가드**: `para/archive/company/<제품>/showcase.md` 도 허용 — fix3 의
   `_Root(filename=)` 패턴 그대로(showcase.md 한 파일 · 한 단계 깊이 · 동명 하위 차단).
5. **allowlist**: 제출부 tool allowlist(+approval_mode)에 2종 추가.
6. **테스트**: 노출 토글 반영 · 미노출 404 · archive showcase 통과 · archive 의
   showcase 아닌 파일 404 · admin kind=product 토글.

## 검증

```
cd app/back && uv run pytest -q tests/
cd ../mcp && uv run pytest -q
```

## 완료 보고 — 2채널, 핸들은 preamble 우선

```bash
orca orchestration send --to term_53806a6d-ced5-4948-88bd-4181b7ba4323 --from <네 워커handle> \
  --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> \
  --subject "backend fix4 완료: <한 줄>" --body "수정 요약 / 테스트 수치"
orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 \
  --text "[worker_done] backend fix4 완료 — <한 줄>. 상세는 인박스." --enter
```
