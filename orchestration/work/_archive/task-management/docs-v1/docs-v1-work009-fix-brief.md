# [backend] WORK-009 검수 수정 — FAIL 1 · WARN 6

너는 **task-management `backend` 워커**다. **WORK-009 를 네가 구현했고 검수가 끝났다.** 검수 리포트대로 고친다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1`. 네가 남긴 미커밋 변경 위에서 고친다. 커밋하지 마라.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/work009-review-report.md   ← 검수 리포트. §1 F-1 · §2 W-1~W-7 · §4 D-1~D-7
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/30-work/work-009-mcp-token.md   ← WP(코디가 D-2 · D-7 을 고쳐 뒀다)
```

## 1. 고칠 것 — 코디 판정

### F-1 + W-2 + D-7 — **회의 토큰은 허용 표면 밖 전부 404** (코디 확정)

`require_context` 의 회의 범위 검사가 경로 `{meeting_id}` 가 있을 때만 돌아 **`GET /api/meetings`(목록) · `GET /api/jobs/{id}`** 가 회의 토큰에 열려 있다. 규칙을 **allowlist** 로 바꾼다.

```
회의 토큰(ctx.meeting_id 있음)으로 200 이 되는 표면 — 이 여섯뿐
  GET /api/meetings/current
  GET /api/meetings/current/tasks
  GET /api/meetings/{meeting_id}          (토큰의 회의일 때만 — 지금 규칙 유지)
  GET /api/tasks/{task_id}
  GET /api/work-types
  GET /api/auth/session
그 밖은 메서드 불문 404 not_found — 목록 · jobs · 쓰기 · 문서함 · 캘린더 · 프로필 전부
```

- 판정 자리는 **`deps.py` 한 곳**(`require_context`). 라우터마다 흩뿌리지 마라. 허용 표면은 **(method, path pattern) 상수 목록 하나**로 두고 그것으로만 판정한다
- `GET /api/meetings/{meeting_id}/…` 하위 조회(안건·줄·transcript)는 **닫는다** — 도구가 `/current` 상세로 다 본다. 여는 이유가 없다
- 테스트 — 목록 · jobs · 한 쓰기 표면 · 문서함 하나 · 캘린더 하나가 회의 토큰으로 404 (W-6 포함)

### W-1 — 404 문구

`deps.py:32` 의 404 `detail` 이 업무 표면에서도 「회의록을 찾을 수 없습니다」로 나간다. SPEC-006 §4 · SPEC-003 §4 의 `not_found` 문구는 리소스별이다. **회의 토큰 범위 밖 404 는 리소스를 모르므로** `detail` 을 「찾을 수 없습니다」(리소스 무언급)로 하나 두고 `code` 는 `not_found` 그대로. 리소스별 문구는 각 service 의 기존 예외가 낸다 — 거기를 건드리지 마라.

### W-3 — compose

`worker` 에 `depends_on: mcp / condition: service_healthy` 추가. 마운트 · PATH · env 는 그대로.

### W-4 — `"none"` 센티널

`projectId=none` 은 **router 에서 dto 로 바꿀 때** `무소속` 표식으로 변환한다(SPEC-006 목록의 `none` 처리와 같은 자리). service 에 문자열 `"none"` 비교가 남으면 안 된다. 리터럴은 **한 곳**(schemas 또는 router 상수)에만.

### W-5 — 리비전 왕복 테스트

`tests/test_migrations.py`(신규) — 테스트 DB 에서 `upgrade head → downgrade -1 → upgrade head` 를 alembic 명령으로 돌리고, `kind='refresh'` 행이 살아 있고 meeting 행이 downgrade 에서 지워졌음을 단언. 느리면 `@pytest.mark.slow` 로 표시하되 `make test` 에 포함.

### W-7 — Phase 4 실측 증거

네가 이미 실측했다(`mcp_tool_call` · 도구 밖 0건 · 헤더 토큰 = 컬럼값 · revoke 뒤 401). **그 증거를 파일로 남겨라** — `orchestration/…` 는 못 쓰니 코드 워크트리 밖 `/private/tmp/…scratchpad/work-009-phase4-evidence.md` 에 워커 JSONL 발췌(도구 호출 이벤트 3줄 · `command_execution|web_search|mcp__codex_apps__` grep 0 결과 · 토큰 대조 쿼리 결과)를 붙이고 §9 보고에 경로를 적어라. 코디가 WP 완료 증거로 옮긴다.

## 2. 고치지 않는 것

- D-1 · D-2 · D-4 · D-5 · D-6 문서 공백 — 코디가 문서를 고친다. **코드는 문서에 맞춰 두라**: D-4 도구 인자는 `project_id` · `agenda_id` · `task_id` 스네이크 그대로(코디가 SPEC 에 그렇게 적는다) · D-6 부분 인덱스는 **비유니크 그대로**(회의당 하나는 `start()` 상태 게이트)
- D-3 — 워커 JSONL 에 `-c` 원문이 남는 건 설계다. **back 로그**에만 없으면 된다(지금 그대로)
- WORK-010 이후 범위

## 3. allowed_paths

```
app/back/   docker-compose.local.yml   .env.example
```

## 4. 검증

```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1 && make test     # 전체 · Errors 0 · W-5 포함
grep -n '"none"' app/back/service/*.py            # 0
docker compose -f docker-compose.local.yml config | grep -A3 "worker:" | grep -c mcp   # depends 확인
```

회의 토큰으로 `GET /api/meetings` · `GET /api/jobs/1` · `POST /api/meetings/{id}/lines` · `GET /api/documents` · `GET /api/schedules` → 전부 404. 여섯 허용 표면은 그대로 200.

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_fd9fc1ce-619d-4f87-b218-10dfaefaa275 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WORK-009 검수 수정" \
  --body "F-1 · W-1~W-7 각각 무엇을 고쳤나 / make test 수치 / Phase 4 증거 파일 경로 / 미결"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] backend 완료 — WORK-009 검수 수정. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] backend: <질문>" --enter`
