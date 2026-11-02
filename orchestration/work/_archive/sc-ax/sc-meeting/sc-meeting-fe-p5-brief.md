# [frontend] WP-006 Phase 5 — 자료 첨부·드로어·공유 실계약 배선 (WP-005 소비)

너는 **sc-ax `frontend` 워커**다. WP-006 세션 그대로. 작업 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = **59e1102** WP-005 커밋). `frontend/` 만. `backend/` 읽기만 — 서버가 있다, `http.py` 실물을 읽고 맞춰라. 커밋 금지.

## 1. SSOT

- **SPEC 0.4.1** §3.2 공유 · §10 자료(20MB · PDF·MD · 되는 것만 붙고 실패는 사유) · §2.2(알림 없음). **WP-005** Interface Contract(정렬됨) · **WP-006** 자료·공유 항목. 시안 `design/회의실.dc.html` MOD-104(자료 첨부: 끌어다 놓기+선택, T01 20MB 초과·T02 형식·T03 토스트·T04 일부 실패)·MOD-105(공유: 검색·조직도·볼 수 있는 사람) · 자료 행 클릭 → **드로어**. `REPORT-회의실-v2.md` M15(T02 문구는 확정 문구라 그대로).
- 워커 리포트 `report-be-wp005.md`(FE 인계 절).

## 2. 계약 (BE 실물)

- `GET /api/meetings/{id}/materials` → `[MeetingMaterial{material_id, name, content_type, size, uploaded_by, uploaded_at}]`
- `POST /api/meetings/{id}/materials` multipart 여러 파일 → 201 `{attached:[…], failed:[{name, reason:"too_large"|"unsupported_type"}]}` · 전부 실패 422 · 진행 중 409. 실패 사유 → 확정 문구 T01/T02, 일부 실패 → T04, 성공 토스트 T03.
- `DELETE …/materials/{mid}` 올린 사람만 204 · `GET …/materials/{mid}/content` 드로어 본문(PDF 는 iframe/object, MD 는 텍스트 렌더 — 시안대로).
- `GET /api/meetings/{id}/shares` → `[{member_id, name, basis:"attendee"|"share"}]`(참석자 먼저) · **⚠ 변경** `POST /shares` body `{member_ids:[…]}`(여러 명, 이미 참석·열람은 건너뜀) → 갱신된 같은 목록(MeetingRow 아님) — P1·2 의 ShareModal 호출을 고쳐라 · `DELETE /shares/{member_id}` → 200 목록(basis share 만 [삭제], 참석자는 409).
- 업로드 multipart 필드 이름 **`files`** · 전부 실패 422 `{detail:{code:"meeting_materials_rejected", failed:[…]}}` · 허용 `application/pdf`·`text/markdown`(확장자 .md/.markdown/.pdf 도 인정) · 열람자는 자료 삭제 404.
- 코디 e2e(실물): 혼합 3파일 → 201 attached 1 · failed [(bad.txt, unsupported_type), (huge.pdf, too_large)] · 진행 중 업로드 409 · content text/markdown · 검색 「온보딩 체크리스트」 소유자·열람자 각 1건. 이미 참석·공유인 사람은 검색·조직도 결과에서 뺀다.
- 가시성: 진행 중에는 첨부·삭제 숨김(서버 409 짝) · 공유받은 사람에겐 조작 0.

## 3. 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run src/meetings/. 검증 1회. 서버·5176 금지. 업로드는 fetch 모킹.
```

- 테스트: 다중 파일 일부 실패 표시 · 전부 실패 422 표시 · 진행 중 첨부 버튼 없음 · 올린 사람만 × · 드로어 열림(인라인 아님) · 공유 목록 basis 별 [삭제] · 이미 있는 사람 제외 · 공유받은 사람 조작 0.
- **D25**: 새 부품(드롭존·파일 행·공유 대상 표 등)은 재사용 컴포넌트로 분리 + 「DS 추가 후보」 표.

## 4. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: WP-006 Phase 5 자료·공유" \
  --body "변경 파일 / 검증 수치 / 계약 준수 / DS 추가 후보 표 / 임시 문구 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — WP-006 Phase 5. 상세는 인박스." --enter
```
