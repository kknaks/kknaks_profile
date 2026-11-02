# [backend] WORK-010 Phase 1~2 — `/start` 는 전이만 · 웜스타트는 컨텍스트 없이 백그라운드

너는 **task-management `backend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`). **WORK-009(MCP · 토큰)가 방금 들어왔다** — `git log -1` 로 확인하고, `auth_service.issue_meeting_token()` · `get_meeting_token()` · `build_codex_options(meeting_token=)` 를 **그대로 쓴다.** 코드 워커는 한 번에 하나만 돈다.

문서는 전부 **코디 워크트리 절대경로 · 읽기 전용**이다.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-010-meeting-start.md            ← 네 빌드 계획 전부. Code Surface · Internal Interface · Phase 1 · 2 의 검증 항목이 판정 기준
  30-work/work-009-mcp-token.md                ← 선행 — 토큰 함수 · 옵션 빌더 시그니처
  20-spec/spec-006-meeting-setup.md §4         ← `POST /start` · 상태별 허용 표 · 구현 규칙
  20-spec/spec-007-meeting-live.md §4 · §5     ← 「웜스타트」 표 5행 · 「AI 도구 7개」 표 · 배치 트리거 규칙
  10-decision/decision-003-meeting-notes.md    ← §4 회의 시작 · §7 웜스타트 행 · §8 「AI 도구 연결」(용어 다섯의 뜻)
  40-architecture/backend/README.md            ← §5-2 · §5-3 · §7 · §8-3 · §12 테스트 8-a
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/ai-prompt-draft.md §A   ← 웜스타트 프롬프트 초안
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/Meeting flow.md §1-2 · §1-4 · §1-5   ← MF-1 · 50 · 55 · 70
```

## 1. 범위 — Phase 1 · 2 전부

```
Phase 1  meeting_service.start() 에서 load_warm_start_context · commit · warm_start 대기 · set_ai_session_id 제거 → register_after_commit 로 launch_warm_start
         meeting_batch_service.launch_warm_start() · _warm_start_once() 신규 · warm_start(context) · load_warm_start_context · WarmStartContext · _task_rows · _date 폐기
Phase 2  build_warm_start_prompt() 전면 재작성 — 인자 없음 · 여섯 절(WP §Internal Interface) · 도구 7개 이름은 WORK-009 enabled_tools 와 글자 그대로
```

## ⛔ 2. 하지 말 것 · 이미 있는 것

```
_agenda_rows()            지우지 마라 — build_batch_prompt(011) · build_final_prompt(012) 가 아직 부른다. WORK-012 가 지운다
build_batch_prompt        건드리지 마라(WORK-011)
run_final · _load_final_input · build_final_prompt · meeting_finalize_service   건드리지 마라(WORK-012)
build_codex_options       WORK-009 것. 부르기만 한다. 옵션을 다른 곳에서 만들지 마라
core/db.py register_after_commit · run_after_commit_hooks   이미 있다. 웜스타트 태스크는 이걸로 건다
실패 처리                  만들지 마라(MF-70). 태스크 예외 = done 콜백 로그 한 줄. retry · attempt · 재웜스타트 · 상태 · 컬럼 · 에러코드 0건
프론트 · compose · env · 리비전   변경 없음
```

## 3. 계약

- `/start` = 전이 UPDATE + 토큰 INSERT(WORK-009 가 넣은 줄 유지) **한 트랜잭션**. `session.commit()` 호출 0건. 응답 `MeetingDetail` 그대로
- `launch_warm_start(meeting_id)` — `create_task` 로 즉시 반환. 커밋 안 되면 안 돈다
- 제출 — `session_id=None` · `output_schema=None` · `timeout_sec=settings.ai_timeout_sec` · `meeting_token=get_meeting_token(meeting_id)`(None 이면 제출 안 함 · 로그)
- `session_id` 는 **새 세션**에서 `set_ai_session_id`. 본문은 버린다
- 프롬프트 — 여섯 절. 문자열 안에 `humanAgendas` · `tasks` · `taskWhitelist` · `project` · JSON 블록 0건

## 4. allowed_paths

```
app/back/                  (service · repository · tests)
```
문서 · `app/front/` · `app/mcp/` · compose · env · `tauri.conf.json` 금지.

## 5. 검증

WP §Execution Phase 1 · 2 의 검증 체크리스트 전부. 특히

```bash
cd app/back && make test                       # 전체 · Errors 줄 0
grep -c "session.commit(" service/meeting_service.py            # 0
grep -rn "load_warm_start_context\|WarmStartContext\|_task_rows" service/   # 0
grep -n "retry\|attempt" service/meeting_batch_service.py       # 웜스타트 근처 0(배치 쪽 기존 것은 그대로)
```

**BE §12 8-a** 를 테스트로 고정 — 대역 게이트웨이를 막고 `/start` → 200 · `recording` · `ai_session_id IS NULL` · 트리거 밀어도 제출 0. 게이트웨이 호출이 **응답 뒤**인 것을 단언.

막히면 30분 넘기지 말고 §9 (2) 로 물어라.

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_fd9fc1ce-619d-4f87-b218-10dfaefaa275 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WORK-010 Phase 1~2" \
  --body "변경 파일 목록 / Phase 별 구현 요약 / 검증 결과(수치 · 정적 검사 grep) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] backend 완료 — WORK-010 회의 시작. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
