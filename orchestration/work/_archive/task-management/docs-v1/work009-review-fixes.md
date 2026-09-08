# WORK-009 검수 수정 보고 — FAIL 1 · WARN 6

워크트리 `/Users/kknaks/orca/workspaces/task_management/docs-v1` · **커밋하지 않았다**.
Phase 4 실측 증거: `…/scratchpad/work-009-phase4-evidence.md`(원본 JSONL 셋이 같은 디렉토리에 있다).

## F-1 + W-2 + D-7 — 회의 토큰은 **허용 표면 밖 전부 404**

`api/deps.py` — 규칙을 「쓰기만 막는다」에서 **allowlist** 로 바꿨다. 판정은 `require_context` 한 곳이고,
허용 표면은 **`(메서드, 라우트 경로 템플릿)` 상수 목록 하나**(`_MEETING_TOKEN_SURFACES`)다.

```python
_MEETING_TOKEN_SURFACES = frozenset({
    ("GET", "/api/meetings/current"),
    ("GET", "/api/meetings/current/tasks"),
    ("GET", "/api/meetings/{meeting_id}"),   # 토큰의 회의일 때만 — 아래 대조가 한 번 더 건다
    ("GET", "/api/tasks/{task_id}"),
    ("GET", "/api/work-types"),
    ("GET", "/api/auth/session"),
})
...
route_path = getattr(request.scope.get("route"), "path", None)
if (request.method.upper(), route_path) not in _MEETING_TOKEN_SURFACES:
    raise NotFoundError(_NOT_FOUND)
path_meeting_id = request.path_params.get(_MEETING_PATH_PARAM)
if path_meeting_id is not None and str(path_meeting_id) != str(context.meeting_id):
    raise NotFoundError(_NOT_FOUND)
```

- **FastAPI 가 매칭한 라우트의 `path` 템플릿**으로 판정한다 — URL 문자열을 파싱하지 않으므로 `/api/tasks/8` 과 `/api/tasks` 가 섞이지 않는다.
- `_READ_METHODS` 는 없앴다. 이제 메서드도 표에서 나온다.
- **회의 하위 조회(안건 · 줄 · transcript)는 닫았다** — 도구는 `/current` 상세로 다 본다.
- 라우터는 한 줄도 안 고쳤다. 표면이 새로 생기면 기본이 404 다.

실측(회의 6 · 증거 §4): 허용 여섯 전부 200 / 목록 · `/api/jobs/1` · `/api/tasks` · `…/transcript` · 다른 회의 · 쓰기 전부 404.
세션 JWT 는 목록 200 · `/api/tasks` 200 그대로다(화면 회귀 없음).

## W-1 — 404 문구

`_NOT_FOUND = "찾을 수 없습니다"`(리소스 무언급) · `code` 는 `not_found` 그대로.
이 404 는 업무 · 유형 · job 어디서든 나기 때문에 리소스를 말할 수 없다.
**리소스별 문구는 각 service 의 기존 예외가 그대로 낸다** — `meeting_service._NOT_FOUND`(「회의록을 찾을 수 없습니다」) ·
`job_service._NOT_FOUND`(「작업을 찾을 수 없습니다」)를 건드리지 않았고, 테스트가 세션 JWT 쪽 문구가 그대로임을 확인한다.

## W-3 — compose

`worker.depends_on` 에 `mcp: service_healthy` 추가. 마운트 4종 · `PATH` · `CODEX_HOME` · 브로커 env 는 그대로.

```
api    -> depends_on {'db': 'service_healthy', 'redis': 'service_healthy'}
mcp    -> depends_on {'api': 'service_healthy'}
worker -> depends_on {'mcp': 'service_healthy', 'redis': 'service_healthy'}
```

## W-4 — `"none"` 센티널

`MeetingTaskFilterDTO(project_id: int | None, unassigned_only: bool)` 신규(`dto/meeting.py`) — **세 갈래를 타입으로 나눈다**
(`(None,False)` 생략 = 회의의 프로젝트 · `(None,True)` 무소속 · `(id,False)` 그 프로젝트).
문자열을 푸는 자리는 **라우터 하나**이고 이웃 표면(`list_meetings`)과 같은 규약이다. 리터럴은 `api/meeting_router.py:53 _UNASSIGNED` **한 곳**뿐.
`service/meeting_service.UNASSIGNED_PROJECT` 는 없앴고 `int(project_id)` 도 사라졌다.

```
$ grep -c '"none"' app/back/service/*.py   →  전부 0
```

## W-5 — 리비전 왕복 테스트

`app/back/tests/test_migrations.py`(신규 · `@pytest.mark.slow` · `make test` 에 포함).
`pyproject.toml` 에 `markers` 등록(표시일 뿐 — 제외하지 않는다).

커밋된 행(account · work_type · meeting · refresh 세션 · meeting 토큰)을 심고 실제 alembic 명령으로 `downgrade -1 → upgrade head` 를 돈 뒤 —
- 되감긴 스키마에 `kind` · `meeting_id` · `meeting_token` **없음**, `refresh_token_hash` 가 `is_nullable = NO` 로 복구
- `kind='refresh'` 행 **살아 있음**, 다시 올린 뒤 `kind='refresh'`
- meeting 토큰 행은 downgrade 가 지웠고 되살아나지 않음
`finally` 에서 심은 행을 전부 지운다 — 공유 테스트 DB 라 「회의 토큰 행이 정확히 하나」를 세는 테스트가 남의 행을 보면 안 된다.

## W-6 — 회의 목록 테스트

`test_meeting_token.py` 에 넷 추가 —
- `test_the_six_allowed_surfaces_stay_open_for_a_meeting_token` — 허용 여섯 전부 200
- `test_reads_outside_the_allowlist_are_404_for_a_meeting_token` — 목록 · `/api/jobs/1` · `/api/tasks` · `…/transcript`.
  본문까지 대조한다(`{"detail":"찾을 수 없습니다","code":"not_found"}`) — **게이트에서 떨어졌다**는 것까지 본다
  (`/api/jobs/1` 은 service 까지 가면 「작업을 찾을 수 없습니다」가 나온다)
- `test_the_meeting_list_never_leaks_other_meetings_to_a_meeting_token` — F-1 회귀. 회의 토큰 404 · 세션 JWT 200(항목 2개 이상)
- `test_the_not_found_body_names_no_resource` — W-1

기존 `test_account_scoped_reads_stay_open_for_a_meeting_token`(`/api/tasks` 목록 200 을 기대하던 것)은 허용 여섯 테스트로 교체했다.

**문서함 · 캘린더 라우터는 아직 코드에 없다**(`api/` 에 auth · deps · health · job · meeting · meeting_stream · setting · task 뿐).
allowlist 는 화이트리스트라 그 표면이 생기는 순간 기본이 404 다 — 테스트를 미리 쓸 대상이 없어 넣지 않았다.

## W-7 — Phase 4 실측 증거

`…/scratchpad/work-009-phase4-evidence.md` — **검수 수정을 적용한 뒤** 다시 돌려 잡았다.
① `mcp_tool_call server="tm"` 두 도구 완료 ② `command_execution` · `web_search` · `mcp__codex_apps__` · `mcp__` **전부 0건**,
호출된 서버 `['tm']` · 도구 `['list_agendas','list_work_types']` ③ 헤더 토큰 = `auth_session.meeting_token` 컬럼값이고 세션 JWT 와 다름
(JWT 는 토큰 테이블에 0건) ④ allowlist 여섯 200 / 밖 전부 404 ⑤ `revoke` 뒤 같은 토큰 → 도구 결과에 `backend 401 token_expired`,
codex 가 「세션이 만료되어 …」로 답한다. SPEC-007 §6 AC 여섯 항목 대조표도 파일 안에 있다.

## 안 고친 것 (지시대로)

- D-1 · D-2 · D-4 · D-5 · D-6 문서 공백 — 코디 몫. 코드는 문서에 맞춰 뒀다(도구 인자 스네이크 유지 · 부분 인덱스 비유니크 유지)
- D-3 — 워커 JSONL 의 `-c` 원문은 설계. back 로그에는 없다(`test_agent_options.py:171` 정적 검사)
- WORK-010 이후 범위 · 프롬프트 · 배치 입력 · 종료 파이프라인
