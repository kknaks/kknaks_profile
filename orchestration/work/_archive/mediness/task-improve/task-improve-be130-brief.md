
# [backend] WP-130 상세 5부 통일 + 완료 근거 — P0~P4 · P6(BE) · P8(BE)

너는 **mediness `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve`
base 브랜치: `origin/dev` → PR `dev` (PR 은 코디네이터가 올린다)
**주의**: 이 브랜치에 WP-129 커밋(5b98247a, code PR #140)이 이미 있다 — 그 위에 작업한다.
**FE 워커가 같은 워크트리 `front/` 에서 병렬 작업 중 — `front/` 금지.**

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec/products/mediness/30-work/work-130-task-detail-unification.md` — **정본. 네 몫 = P0(실측 재확인)·P1(migration 컬럼2+테이블1)·P2(본문 5부 BE)·P3(완료 등록 근거)·P4(task_references CRUD+storage)·P6 중 BE 항목(채팅 초안 채움·첨부 스테이징)·P8 중 BE.** phase 의 작업·검증 체크리스트를 그대로 따른다
- `../20-spec/spec-154-decision-workflow.md` §4.8(본문 컬럼·완료 422 계약)·§4.10(DM)·§4.19.13(projection gap 표 — «2026-09-01 2차 신규 gap 없음»)
- `../20-spec/spec-155-ax-task-draft-workflow.md` — 채팅 초안 필수 채움(배경·목표·체크리스트)·첨부 스테이징 §6.12
- `../20-spec/spec-127-department-document-storage.md` — 파일 storage path-guard 선례(재사용할 패턴)
- `../40-architecture/domains/runtime_task.md` — task_references 스키마·완료 근거 불변식·migration 절
- 결정 원문: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/_RESUME.md` §2

기대는 개념 — 해당 없음.

## 2. 핵심 계약 (WP 가 상세를 소유 — 어기면 검수 FAIL)

- **migration = 컬럼 2(tasks.background·goal, nullable text) + 테이블 1(task_references) 정확히.** 그 이상 늘리지 마라. 왕복(upgrade→downgrade→upgrade) + 생성 객체 수 테스트
- **task_references**: role(reference/deliverable) × kind(link/file)·soft delete(deleted_at)·created_by_member_id. **출처는 행으로 저장 금지**(execution 사슬이 정본)
- **파일 storage**: env `TASK_REFERENCE_STORAGE_ROOT` 기본 `/app/var/task-references`, 레이아웃 `{task_id}/{reference_id}_{원본파일명}`, **부서공간 path-guard 패턴 재사용**(traversal 차단), DB 엔 상대경로만. 파일당 25MB·실행파일류 denylist·`Content-Disposition: attachment`
- **완료 등록**: 사람 액터의 →done 전이는 **완료기록(payload) 또는 deliverable 1건 없으면 422**. **시스템 액터(워크플로 멱등 완료·슬랙 [완료])는 예외** — 기존 자동 완료 경로가 깨지면 안 된다(회귀 테스트)
- **원장 렌더 폐지 대체**: decision/incident 태스크 생성부가 배경·목표·체크리스트를 **스냅샷 저장**. description 은 legacy fallback(background/goal 비면 표시용으로 응답에 유지)
- **채팅 초안**: 배경·목표·체크리스트 필수 산출(부족하면 되물음 — SPEC-155 계약), 첨부는 `drafts/{draft_id}/` 스테이징 → 승인 시 task_references 귀속·경로 이동, 폐기 시 정리
- 상태 축·TaskEvent 어휘 불변 · 권한은 v1 «볼 수 있으면 고칠 수 있다» — **역할별·상태별 게이팅 만들지 마라(v2)**

## 3. allowed_paths

- `back/` · `mcp/` · `docker-compose.yml` · `docker-compose.local.yml` — ⛔ `front/` 금지

## 4. 검증

```
cd /Users/kknaks/orca/workspaces/mediness-app/task-improve/back && uv run pytest -q <네가 만들거나 고친 테스트 파일만>
```
- 전체 스위트 금지(사용자 방침)·검증 1회만·migration 왕복 확인. 기존 무관 실패는 «무관» 분리(stash 실측 선례).

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 값과 다르면 preamble 이 맞다.

- **커밋·push·PR 금지.** 끝나면 두 명령 모두:

```bash
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "Phase 별 결과 / 변경 파일 / 검증 수치 / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] backend(WP-130) 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[질문] backend: <질문>" --enter`
