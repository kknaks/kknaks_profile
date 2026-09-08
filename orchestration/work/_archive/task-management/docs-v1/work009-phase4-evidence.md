# WORK-009 Phase 4 완료 증거 — 실측 캡처

**언제** 2026-09-07 · 검수 수정(F-1 allowlist · W-1 문구 · W-3 compose · W-4 센티널 · W-5 왕복 테스트) 적용 **이후**
**어디서** `docker-compose.local.yml` 다섯 서비스(db · redis · api · mcp · worker) 전부 healthy
**무엇으로** 워커 컨테이너 안의 codex 0.147.0 에 `build_codex_options()` 가 만드는 `-c` 목록을 **그대로** 넘겨 한 번 돌렸다(임시 · 커밋 안 함)

```
$ docker compose -f docker-compose.local.yml ps --format "table {{.Service}}\t{{.Status}}"
SERVICE   STATUS
api       Up (healthy)
db        Up (healthy)
mcp       Up (healthy)
redis     Up (healthy)
worker    Up (healthy)
```

---

## 1. 도구 호출이 실제로 난다 — `mcp_tool_call` (회의 5)

프롬프트: 「list_agendas 와 list_work_types 를 불러서 이 회의의 안건 제목과 업무 유형 이름만 한 줄로 답해라.」
워커 JSONL 발췌(10줄 중 도구 이벤트 3줄 + 답변):

```json
{"id":"item_0","type":"agent_message","text":"회의 안건과 업무 유형을 조회하겠습니다."}
{"id":"item_1","type":"mcp_tool_call","server":"tm","tool":"list_work_types","arguments":{},"result":null,"error":null,"status":"in_progress"}
{"id":"item_1","type":"mcp_tool_call","server":"tm","tool":"list_work_types","arguments":{},"result":{"content":[{"type":"text","text":"{\n  \"items\": [\n    {\n      \"id\": 1,\n      \"kind\": \"meeting\",\n      \"name\": \"미팅·회의\", …"}]},"status":"completed"}
{"id":"item_2","type":"mcp_tool_call","server":"tm","tool":"list_agendas","arguments":{},"result":{"content":[{"type":"text","text":"{\n  \"id\": 43,\n  \"title\": \"MCP 도구 확인\",\n  \"state\": null,\n  \"track\": \"human\", …"}]},"status":"completed"}
{"id":"item_3","type":"agent_message","text":"MCP 도구 확인, 토큰 확인 — 미팅·회의, 개인 업무, 문서·보고"}
{"type":"turn.completed","usage":{"input_tokens":28932,"cached_input_tokens":9088,"output_tokens":154,"reasoning_output_tokens":21}}
```

→ **codex 0.147.0 이 `-c mcp_servers.tm.url` 로 Streamable HTTP MCP 를 붙이고 실제로 우리 도구를 부른다.**
서버 id 는 `tm` 하나, 도구는 `list_agendas` · `list_work_types` 둘. AI 가 답을 지어내지 않고 도구 결과로 답했다.

## 2. 우리 도구 밖 호출 0건

```
$ for k in command_execution web_search mcp__codex_apps__ mcp__ ; do printf "%-22s %s\n" "$k" "$(grep -c -- "$k" codex_ok.jsonl)"; done
command_execution      0
web_search             0
mcp__codex_apps__      0
mcp__                  0

$ python3 …  # JSONL 의 mcp_tool_call 을 전부 추출
('tm', 'list_work_types', 'in_progress')
('tm', 'list_work_types', 'completed')
('tm', 'list_agendas', 'in_progress')
('tm', 'list_agendas', 'completed')
서버 종류: ['tm']
도구 종류: ['list_agendas', 'list_work_types']
```

→ `features.shell_tool=false` · `web_search="disabled"` · `features.image_generation=false` · `features.apps=false`
· `enabled_tools` 7개 allow list 가 실제로 걸렸다. **우리 7개 밖의 도구 호출이 0건**이다.

## 3. 헤더 토큰 = `auth_session.meeting_token` ≠ 세션 JWT (회의 6)

DB 행(회의 5, 폐기 전 캡처):

```
$ psql -x -c "select … from auth_session where kind='meeting';"
-[ RECORD 1 ]------+--------------------------------------------
id                 | 97
kind               | meeting
account_id         | 1
meeting_id         | 5
meeting_token      | 2-22SODv6UudX_uwwY8CjlM_QzLMG2tXXbFSMWrXXbQ
refresh_token_hash |            ← NULL (A-13)
revoked_at         |            ← NULL (회의 토큰은 이 칸을 안 쓴다)
expires_at         | 2026-09-07 18:29:19.59423+00
```

`-c mcp_servers.tm.http_headers={Authorization="Bearer 2-22SODv…"}` 에 실린 값이 **이 컬럼 값 그대로**다(§1 의 호출이 그 토큰으로 200 을 받았다).

세션 JWT 와의 대조(회의 6):

```
meeting_token(DB 컬럼) = Hf4k5jdv62wCC2Va-lqufsdlCa-6EMll8tFxHZqQU70     ← 43자 urlsafe · 점 없음
session JWT(앞 40자)   = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ…       ← 3분절 JWT
같은 값인가            = NO
JWT 가 토큰 테이블에 있나 = 0        (select count(*) from auth_session where meeting_token = '<JWT>')
```

→ **도구 호출 헤더의 토큰이 사용자 세션 토큰과 다르다**(SPEC-007 §6 AC).
반대 방향도 성립한다 — 회의 토큰은 JWT 서명이 없어 `decode_access_token` 에서 떨어지고, JWT 로 `/api/meetings/current` 는 404 다(§4 마지막 표).

## 4. 회의 범위 — allowlist 여섯만 200 (회의 6 · 검수 F-1 수정 후)

```
### 회의 토큰으로 — allowlist 여섯
  /api/meetings/current              200
  /api/meetings/current/tasks        200
  /api/meetings/6                    200
  /api/tasks/8                       200
  /api/work-types                    200
  /api/auth/session                  200

### 회의 토큰으로 — allowlist 밖
  /api/meetings?from=…&to=…                            404      ← F-1 이 열려 있던 자리
  /api/jobs/1                                          404      ← W-2
  /api/tasks                                           404      ← 화면 계약(오늘 하루)이라 도구가 안 쓴다
  /api/meetings/6/transcript                           404      ← 회의 하위 조회는 닫는다
  /api/meetings/5                                      404      ← 자기 계정의 다른 회의
  POST /api/meetings/6/lines                           404      ← 쓰기
  본문: {"detail":"찾을 수 없습니다","code":"not_found"}          ← W-1: 리소스를 말하지 않는다

### 세션 JWT 로 — 화면 표면은 그대로다(회귀 없음)
  /api/meetings?from=…&to=…                            200
  /api/tasks                                           200
  /api/meetings/6                                      200
  /api/meetings/current                                404      ← 회의 토큰 전용 표면
```

## 5. 폐기 뒤 같은 토큰 → 401 이 도구 결과에 드러난다 (회의 5)

```
$ auth_service.revoke_meeting_token(meeting_id=5)
deleted: 1
두 번째: 0            ← best-effort · 0건이어도 예외 없음(MF-4)
```

같은 `-c` 목록으로 codex 를 한 번 더 돌린 결과:

```json
{"id":"item_1","type":"mcp_tool_call","server":"tm","tool":"list_agendas","result":{"content":[{"type":"text","text":"Error executing tool list_agendas: backend 401: {\"detail\":\"세션이 만료되었습니다\",\"code\":\"token_expired\"}"}]},"status":"failed"}
{"id":"item_2","type":"mcp_tool_call","server":"tm","tool":"list_work_types","result":{"content":[{"type":"text","text":"Error executing tool list_work_types: backend 401: {\"detail\":\"세션이 만료되었습니다\",\"code\":\"token_expired\"}"}]},"status":"failed"}
{"id":"item_3","type":"agent_message","text":"세션이 만료되어 안건 제목과 업무 유형 이름을 조회할 수 없습니다. 다시 로그인해 주세요."}
```

→ **폐기 = 행 DELETE 가 즉시 듣는다.** 401 본문이 도구 결과에 **그대로** 드러나고(빈 배열로 바뀌지 않는다),
AI 가 「데이터가 없다」가 아니라 「볼 수 없다」로 답한다.

---

## SPEC-007 §6 AC 대조

| AC 항목 | 증거 |
|---|---|
| codex 설정에 `enabled_tools` 7개 | §1 — `-c mcp_servers.tm.enabled_tools=[7개]` 로 나갔고 그 도구가 실제로 불렸다. §2 — 목록 밖 0건 |
| `features.apps=false` | §2 — `mcp__codex_apps__` **0건**(안 걸면 27종이 붙는다) |
| `sandbox="read-only"` | 새 세션 옵션에만 실린다(`test_agent_options.py:56` · resume 엔 없다 `:83`). 실측 호출도 `--sandbox read-only` 로 나갔다 |
| 도구별 `approval_mode="approve"` | §1 — 승인 프롬프트 없이 도구가 완료됐다(`approval_policy="never"` 였다면 «user cancelled» 로 죽는다) |
| 워커 로그에 우리 도구 밖 호출 0건 | §2 |
| 도구 호출 헤더의 토큰 ≠ 사용자 세션 토큰 | §3 |

## 원본 파일

```
codex_ok.jsonl        §1 · §2 의 워커 JSONL 전문(10줄)
codex_revoked.jsonl   §5 의 워커 JSONL 전문
codex_probe2.sh       두 실행에 쓴 codex 명령(빌더가 만든 -c 목록 그대로)
```
같은 scratchpad 디렉토리에 있다.
