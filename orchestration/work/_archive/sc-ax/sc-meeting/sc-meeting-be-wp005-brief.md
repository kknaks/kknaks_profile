# [backend] WP-005 — 자료 첨부(여러 파일·20MB·PDF/MD) · 공유 목록 · 회의 전사 자료 다리 재건

너는 **sc-ax `backend` 워커**다. WP-001~004·후속 세션 그대로. 작업 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = **96d5312** 후속 커밋). `backend/` 만. frontend 워커·reviewer 와 병렬 — 커밋 금지.

## 0. 선행 1건 (코디 실물 화면 발견 — 먼저 고치고 WP-005 로)

- **evidence 키 투영 불일치**: MeetingDetail 의 Line.evidence 가 `[{from_ms,to_ms}]` 로 나간다(WP-003/004 스키마 내부 이름). 계약(WP-001·SPEC §4.1, FE 소비)은 **`[{start_ms,end_ms}]`** — 화면 근거 칩이 「NaN:NaN」. `_line_view`(및 transcript/export 어디든 evidence 를 내는 자리)에서 `start_ms/end_ms` 로 투영하고, 내부 스키마 이름은 그대로 둔다. 테스트 1: 합성 뒤 detail 의 evidence 키가 start_ms/end_ms.

## 1. SSOT

- **SPEC 0.4.1** §3.2 공유(열람 = 회의록·원문 읽기·내보내기) · §10 자료(20MB · PDF·Markdown · 되는 것만 붙고 실패는 사유) · §11.1 폐기·재건(전사 자료 다리) · §2.2(알림 없음). `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/20-spec/spec-004-meeting-note.md`
- **WP-005** `30-work/work-005-materials-sharing.md` Phase 1·2 검증 = 완료 조건.
- **현행 표면**: 공유는 WP-001 이 이미 `POST /api/meetings/{id}/shares`·`DELETE …/shares/{member_id}` 로 세움(**`/viewers` 아님 — 이 이름 유지**, 문서는 planner 가 맞춘다). 자료는 업무 자료(`/api/tasks/{id}/materials` GET/POST multipart/`{mid}/content`, `platform/native_materials.py`, `AttachmentRecord`·`AttachmentBindingRecord` context_type)를 **같은 결로** 회의에 붙인다. 검색 다리는 `bootstrap/material_sources.py` `SessionMaterialOwners.sources`(task·work_request 갈래)와 `modules/work/material_search.py` `RESOURCE_TYPES`(이미 `meeting` 포함) — WP-002 가 구 회의 갈래(`meeting_raw`·`meeting_refinement`·`meeting_recording`)를 걷었다(`native_materials.py:3`).

## 2. 계약 (코디 확정)

- **자료**: `GET /api/meetings/{id}/materials` → `[MeetingMaterial{material_id, name, content_type, size, uploaded_by, uploaded_at}]` · `POST /api/meetings/{id}/materials` multipart **여러 파일** → 201 `{attached:[MeetingMaterial], failed:[{name, reason:"too_large"|"unsupported_type"}]}`(한 건이라도 붙으면 201, 전부 실패면 422) · `DELETE …/materials/{mid}` 올린 사람만(그 회의 binding 만 끊고 attachment 는 남김) 204 · `GET …/materials/{mid}/content` 열람 축(참석·공유). 게이트: 붙이기·떼기는 참석자, **in_progress 에서는 409**(§10 「진행 중에는 숨김」). 한도 20MB · `application/pdf`·`text/markdown`(확장자 .md 도 인정). 저장은 현행 attachment 저장소 그대로(리포 밖).
- **공유**: 기존 둘 유지 + `GET /api/meetings/{id}/shares` → `[{member_id, name, basis:"attendee"|"share"}]`(참석자는 basis attendee, 공유는 share — 화면 「볼 수 있는 사람」). `POST /shares` 는 여러 명 · 이미 참석·공유인 사람은 조용히 건너뜀 · **알림 없음** · `DELETE` 는 share 근거인 사람만(참석자 409). 공유받은 사람: 목록 「지난」에 열람 배지(WP-001 `viewer_relation`), 캘린더 제외 — 이미 그러한지 확인만.
- **검색 다리**: `material_sources.py` 에 **`meeting_transcript` 갈래** — 회의당 자료 하나(resource_type `meeting`, resource_id = meeting_id, title = 회의 제목|title_candidate|「제목 없는 회의」), 본문 = `meeting_transcripts` 확정 블록 전량을 「화자 N [mm:ss] 텍스트」 줄로 이어붙인 것 · 열람 = 참석·공유(상세와 같은 축, 조직 축 없음) · in_progress 이후 상태만. `/api/materials/search` 결과와 `search-support` 계약(`docs/search-support.md`)을 깨지 않는다. 기존 검색 테스트 회귀 0.

## 3. 먼저 읽을 파일

- `entrypoints/http.py` 업무 자료 라우트 4개 · `platform/native_materials.py` · `platform/attachments*.py` · `bootstrap/material_sources.py` · `modules/work/material_search.py` · `docs/search-support.md` · `tests/contract/test_material_search_public.py`(회귀 기준) · `modules/meetings/application.py`(share·열람 축).

## 4. 단계

1. 자료 4 라우트 + 게이트 + 다중 파일 응답 + 테스트(20MB 초과 · 형식 · 일부 실패 · 진행 중 409 · 올린 사람만 삭제 · 열람 축).
2. `GET /shares` + basis + 중복 건너뜀 + 참석자 삭제 409 + 테스트.
3. `meeting_transcript` 검색 갈래 + 열람 축 + 회귀.
4. 완료 보고(FE 인계: 경로·응답 모양).

## 5. 하지 말 것

- 알림 · 이미지/압축 · 자료 보관/계보(SPEC-006) · 화면. 폐기된 `meeting_raw` 류 복원 금지. Alembic 금지. `make local-stack`·5176/8001 금지. `make reset-demo` 1회 허용.

## 6. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트> tests/contract/test_material_search_public.py tests/contract/test_meeting_core.py tests/architecture -m 'not integration'. 검증 1회
```

## 7. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: WP-005 자료·공유·전사 검색 다리" \
  --body "선행(evidence 키) / 변경 파일 / 구현 요약 / 검증 수치(+검색 회귀) / 계약 준수 / FE 인계 / reset-demo / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — WP-005. 상세는 인박스." --enter
```
