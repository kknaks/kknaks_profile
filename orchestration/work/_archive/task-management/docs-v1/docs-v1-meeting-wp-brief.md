# [architect] 회의록 재작업 WP 5건 — WORK-010 ~ 014

너는 **task-management `architect` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/architect/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app`

**회의록 흐름 결정 34건(MF-1 ~ MF-70)이 계약(SPEC-006/007/008 · DEC-003 · 40-architecture)에 반영됐다.** 그 계약대로 코드를 고치는 **빌드 계획(WP) 다섯**을 쓴다. **WORK-009(MCP · 토큰)는 코디가 이미 썼고 backend 워커가 구현 중이다** — 그 문서가 **형식과 깊이의 표본**이다. 그대로 따라라.

---

## 1. SSOT — 먼저 읽을 것 (전부 이 워크트리 안 · 읽기 전용)

```
para/projects/summer-star/task-management/
  30-work/work-009-mcp-token.md              ← **표본.** frontmatter · Meta · Scope · Code Surface(신규/수정/폐기) · Internal Interface ·
                                                Execution(Phase 마다 작업 · 검증 · 완료 증거) · Rollback · Done Criteria · Open Issues
  30-work/work-006 · 007 · 008               ← 옛 설계. **참고만.** 파일 경로·함수 이름을 빌려 쓰되 내용은 새로 쓴다
  20-spec/spec-006 · 007 · 008               ← 계약. WP 는 **절 번호까지** 가리킨다
  10-decision/decision-003-meeting-notes.md  ← 정책
  40-architecture/backend · frontend · system · database/README · domains/meeting.md · account.md
reference/2026-09-06-task-management-app/Meeting flow.md   ← 결정 원본 MF-1~70. 계약과 부딪히면 이게 이긴다
reference/2026-09-06-task-management-app/ai-prompt-draft.md ← 프롬프트 초안 §A 웜스타트 · §B 배치 · §C 최종
orchestration/work/docs-v1/_RESUME.md §1 표  ← WP 별 MF · 계약 절 · 손댈 코드 요약(코디가 실물 확인한 것)
```

**코드 워크트리** `/Users/kknaks/orca/workspaces/task_management/docs-v1`(읽기 전용 · 브랜치 `kknaksss/docs-v1`). **파일 이름 · 함수 이름은 여기서 grep 해서 실물로 적어라.** 짐작으로 경로를 적지 마라.
지금 backend 워커가 `app/back/models/account.py` · `alembic/versions/0007_*` · `app/mcp/` 를 고치고 있다 — 그 파일의 diff 는 무시하고 WORK-009 문서를 기준으로 삼아라.

## 2. 만들 것 — 다섯 파일 + 인덱스 한 줄씩

| 파일 | WP | MF | 계약(절) | 손댈 코드 — 코디가 실물 확인한 것 |
|---|---|---|---|---|
| `30-work/work-010-meeting-start.md` | 회의 시작 | 1 · 55 · 70 | SPEC-006 §4 `POST /start` · SPEC-007 §4 「웜스타트」 표 · §5 · BE §5-2 · §5-3 · §7 · §12 테스트 8-a · DEC-003 §4 · §7 | `service/meeting_service.py start()`(L515~ — `load_warm_start_context → commit → warm_start` 순서를 **전이만 + commit 뒤 백그라운드 제출**로. `core/db.py run_after_commit_hooks` 가 이미 있다) · `meeting_batch_service.warm_start()` · `build_warm_start_prompt()` · **`load_warm_start_context` · `_task_rows` · `_agenda_rows` 폐기** · 프롬프트 = 역할 · 흐름 · 요약 원칙 · 용어 다섯 · 도구 목록(ai-prompt-draft §A) · 실패 처리 **없음**(MF-70 — 로그뿐) |
| `30-work/work-011-meeting-live.md` | 회의 중 | 9 · 10 · 49 · 50 · 51 · 52 · 53 | SPEC-007 U-2 · U-3 · U-4 · §4 「배치 입력」 · 「배치 출력」 · 「검증 순서」 · WS `ai.batch` · §5 · FE §8 · ERD M-6 · M-7 · M-16 | back `meeting_batch_service` — `config.meeting_batch_chars` 600→1000 · `_load_input()` 안건·줄·화이트리스트 제거 · `build_batch_prompt()`(ai-prompt-draft §B — 조회 순서 지시) · `_persist()` INSERT → **DELETE + INSERT 한 트랜잭션**(`run_final` 에 있던 전량 교체를 매 배치로) · `_demote_if_needed` 기준을 검사 시점 조회로 · `ai_schemas/meeting_batch.json` 에 `headline` · `termCorrections` · `payload` nullable(**한 벌 — WORK-012 와 같은 파일 `meeting_notes.json`** 으로 이름 바꿈. 어느 WP 가 이름을 바꾸는지 하나로 정해라) · front `PromptBar.tsx`(슬래시 5개 — 지금 0건) · `LineKindPopover` · `LineRow.tsx` L118 `formatClock(createdAt)` 제거 · `aiBatch.ts mergeAiBatch` 병합 → 통째 교체 · `useMeetingStream.ts` L214 |
| `30-work/work-012-meeting-close.md` | 회의 종료 | 37 · 52 · 54 · 56 · 57 · 58 · 59 · 70 | SPEC-008 U-1 · U-2 · §4 API 표 · `/end` · `/finalize` · `GET /api/jobs` · 「종료 파이프라인」 표 · `context` · 「서버 검증」 표 · 「수치」 · Case Matrix · DEC-003 §4 · §6 · §7 · §STT · ERD M-8 · M-8-a · M-9-a · M-9-b · M-19 · BE §6 · §12 테스트 8 | **Phase 넷으로 갈라라** — ⓪ 리비전 `0008`(`pending_change → payload` · `source_human_line_id` · `source_ai_line_id` + 부분 UNIQUE · CHECK 삭제 · `meeting.term_corrections` 신설 · `batch_run.phase` CHECK 에서 `integration` 제거 · `job.error_code` 5종) ① `integrations/soniox.py` async 갈래(files → transcriptions → 5초 폴링 → tokens · sub-word 를 화자·300자·2초로 블록) · `context` 조립(`terms` 비움) · `meeting_transcript` DELETE+INSERT · **헤더 없는 webm 실물 1건**(SYS-OQ-5) ② `meeting_finalize_service` — `integrate()` → `finalize()` · `run_pipeline` = ① → ② 한 번(`resume` · 재전사 스크립트 하나) · ② 검증(안건 · 업무 · 페이로드 참조 · evidence 범위 · `status≠done`)을 WORK-011 과 **같은 검증 함수** · `auto` 치환 · 한 트랜잭션 · **`meeting_merge_service.py` 폐기** · `run_final` · `_load_final_input` · `ai_schemas/meeting_integration.json` 폐기 · `config.py` 수치(1200 · 300×3 · 2400 · 폴링 1230회) · ② 종결 시 `auth_service.revoke_meeting_token()` 호출(WORK-009 가 만든 함수) ③ front — 생성중 문구 phase 둘 · 실패 배너 「다시 시도」 → `/finalize` · AI 탭 종료 후 「배치 n회」 그대로 · `HeadlineBar` 카운트 다섯(`mergedSummary` 키 둘 추가) · 스크립트 푸터 · `useMeetingFinalizeJob` 상한 1230 |
| `30-work/work-013-meeting-edit.md` | 편집 · 정리 | 13 · 14 · 21 · 25 · 36 · 60 · 61 · 62 · 63 · 64 · 65 · 66 · 67 | SPEC-008 U-3 · U-6 · U-7 · U-8 · U-9 · U-10 · §4 `POST lines` · `PATCH lines` · `DELETE lines` · `…/task` POST·PATCH · Validation · Case Matrix · SPEC-002 §4 `description` · DEC-001 §3 · DEC-003 §5 · ERD M-14 · M-14-a · M-20 · A-12 · FE §2 규칙 8 · §6 · BE §12 8-b · 8-c | back — `schemas/meeting.py` `LineCreate` 에서 `newTask` 삭제 · `payload`(액션 생성분 / 업무 변경분 일곱 — `done`·`cancelled` 422) · `taskId` 를 action·task 줄에만 · `LineUpdate` 에서 `kind` 삭제 · `PendingChange` 3키 → `payload` 두 모양 · `meeting_edit_service.delete_line()` order_index 당김 제거 · `update_line` kind 전환 분기 삭제 · `meeting_task_link_service.apply_pending_change` → 본문 받는 `PATCH …/task` ⑧단계 · `add_task_line` 폐기 · 리비전 `0009 work_type.description` + 시드 문구 2건 · `work_type_service` · front — **`CreateTaskFromLineDrawer.tsx` · `LinkTaskDrawer.tsx` 를 payload 드로어로 수정**(폐기 아님 · 필드 = payload 키 · 헤더 업무 셀렉터 `RelationPopover` 단일 선택 prop · 푸터 `submitMode` · **시각은 이미 있는 `TaskCreateDrawer` · `TaskDetailDrawer` 의 부품을 참고 — 시안 없음 · 업무 드로어 코드 수정 금지**) · `MeetingDetailBody.tsx` L233~285 칩 둘 갈래 · `LineKindSelector.tsx` 폐기 · `AgendaLineTree` `onChangeKind` 제거 · `ConfirmModal` `size:"light"` 420 · `LineDeleteModal` 한 문장 · SPEC-002 인라인 행에 설명 필드 |
| `30-work/work-014-meeting-list-ui.md` | 목록 · 상세 UI | 5 · 6 · 7 · 8 | SPEC-006 U-1 · U-4 · U-6 · U-8 · SPEC-007 U-1 Placement · SPEC-008 U-3 헤더 · FE §2 규칙 7 · §6-3 | `components/shared/AppShell.tsx Breadcrumb`(L28~41 `<span>` → 앞 단계 `<a>` + `backTo` 「←」 — `PageHeader` 는 아직 없다, AppShell 안에 두거나 신설) · `MeetingPreviewPanel.tsx` CTA 상태별 · 패널 안 스크롤 · `AgendaLineTree` `density` prop · `MeetingClosedPage.tsx` · `MeetingScheduledPage.tsx` L106 · `MeetingLiveView` · `MeetingMetaInline` 헤더를 배지 줄 → 제목 → 메타 순서로. **업무 화면은 안 고친다** — 「←」는 공용 부품 덤 |

의존 — **009 → 010 · 011 → 012 → 013. 014 는 독립.** 각 WP 의 Meta 「Depends on work」에 그대로.

`30-work/README.md` 의 「회의록 재작업 그룹」 표 다섯 행 — 제목이 네 문서와 다르면 맞춰라. 그 밖은 손대지 마라.

## 3. WP 하나가 갖춰야 할 것 (WORK-009 와 같은 깊이)

- **어느 SPEC 절을 계약으로 받는가** — 절 번호(U-n · §4 표 이름)까지. MF 번호 병기
- **Phase** — 순서 · Phase 마다 작업 체크리스트 · **「끝났다」의 판정 기준(검증 체크리스트 · 수치 · 정적 검사 grep)** · 완료 증거 자리. 백엔드 Phase 와 프론트 Phase 를 가른다
- **Code Surface 표** — 경로 · **신규 / 수정 / 폐기** 구분 · 한 줄 설명. 폐기는 「폐기」라고 적고 대체 파일을 가리킨다
- **Internal Interface Contract** — Phase 사이 · 후속 WP 가 기대는 함수 이름 · 시그니처 · 규칙(예: 「옵션은 `build_codex_options` 한 함수」 같은 단일화 규칙)
- **테스트** — BE §12 「반드시 있어야 하는 테스트」 번호로 연결 · 프론트 FE §11
- **Depends on work** · **Follow-up work** · **Rollback** · **Done Criteria** · **Open Issues**(SPEC 이 이미 자리를 잡은 OQ-10 · 11 · 12 는 「SPEC 대로」로 적는다 — 새로 묻지 않는다)

## 4. 지킬 것

```
□ 결정을 새로 만들지 마라. MF 번호에 없고 SPEC 에도 없으면 Open Issues 에 「사용자 결정 필요」로 남겨라. 추측으로 메우지 마라
□ 계층 — router → service → repository. ORM 은 repository 를 넘지 않는다. service 는 commit 하지 않는다.
   schemas/ = front 계약(camelCase) · dto/ = 내부(snake_case). Query(alias="camelCase") 는 손으로
□ 게이트 — task.status 대입은 task_service.change_status() 안에서만. 회의록은 done 을 안 보낸다. 회의록 쪽에 판정 코드 없음(WORK-013)
□ 시안을 판정에 넣지 마라. 기능 = 기획 + 정책, 시각 = 디자인 시스템 + 시안. payload 드로어는 **새 시안 없음** — 업무 드로어 부품 참고(MF-67)
□ 범위를 넓히지 마라. 회의록 얘기다. 업무 화면 · 캘린더 · 문서함을 고치는 항목을 넣지 마라
□ 파일 · 함수 이름은 코드 워크트리에서 grep 한 실물만. 없는 파일은 「신규」로
□ 스키마 한 벌(ai_schemas/meeting_notes.json)의 소유 WP 를 하나로 정해라(011 또는 012) — 둘이 같은 파일을 만들면 안 된다
□ WORK-009 · 010 · 011 · 012 · 013 · 014 가 같은 파일을 두 번 고치면 어느 WP 가 먼저인지 Depends 에 적어라
□ 문서 다섯 + README 표 다섯 행 밖은 손대지 마라. 커밋 · push 금지
```

## 5. 보고

`orchestration/work/docs-v1/docs-v1-meeting-wp-report.md` — WP 마다 「Phase 수 · 신규/수정/폐기 파일 수 · Open Issues 수 · 코디가 볼 것」 표. 스키마 파일 소유 · 같은 파일 중복 수정의 처리를 명시.

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_51dfc31c-7715-4aad-9622-53704c2c5252 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: 회의록 WP 5건" \
  --body "파일 다섯 / WP 별 Phase·파일·OQ 수 / 스키마 소유 · 중복 수정 처리 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] architect 완료 — 회의록 WP 5건(WORK-010~014). 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] architect: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
