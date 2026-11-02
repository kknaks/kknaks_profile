# [backend] main 머지 뒤 pytest 수집 오류 5개 정리(머지 전 스위트 녹색)

너는 **sc-ax backend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD ec9946b, main 머지됨). `backend/` 만. 커밋·재기동 금지. **이번엔 pytest 돌려라** — 목표: `uv run pytest -q -m 'not integration'` 전체 녹색(수집 오류 0) + `tests/architecture` 통과. 로그 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/be-fail-merge.log`.

## 수집 오류 5(전부 main 이 가져온 테스트가 **옛 회의 모델**을 import)
- `tests/contract/test_action_material_drafts.py` — `MeetingNoteRecord` (persistence 에서 걷은 옛 모델)
- `tests/integration/postgres/test_material_owners.py` · `test_material_upgrade.py` · `test_postgres_integration.py` — `MeetingFinalizationWorker` (bootstrap/meeting_worker 옛 이름)
- `tests/integration/postgres/test_project_participation.py` — `ax_workspace.modules.meetings.transcription` (옛 모듈)

## 원칙
1. **옛 회의 모델은 되살리지 않는다**(SPEC-004 가 대체). 테스트 쪽을 고친다 — 옛 회의 픽스처/헬퍼를 새 모델(`MeetingApplication`·`meeting_worker` 의 현재 클래스·`meetings.stream`)로 바꾸거나, 회의와 무관한 테스트인데 import 만 옛것을 끌어오면 그 import·헬퍼를 걷는다. 건별로 「무엇을 어떻게」 보고에.
2. integration 테스트(postgres)는 `-m integration` 이라 기본 실행에서 빠지지만 **수집은 되어야 한다**(수집 오류가 전체를 막는다). 내용까지 새 모델로 맞추되, 실행은 `not integration` 만.
3. 수집이 풀린 뒤 드러나는 실패도 같은 원칙으로 — 제품 결정이 정본, 실제 회귀면 코드.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: 머지 뒤 스위트 녹색" \
  --body "건별 수정 / pytest 전체 수치 / architecture / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — 스위트 녹색. 상세는 인박스." --enter
```
