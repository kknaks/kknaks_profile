# [reviewer] WORK-009 검수 — MCP 서버 · 회의별 단명 토큰 · codex allow list

너는 **task-management `reviewer` 워커**다. **read-only** — 코드를 고치지 않고 테스트도 돌리지 않는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

## 0. 범위

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`, HEAD `aa98518`). **아직 커밋 전이다** — 범위는 미커밋 변경 + untracked 다.

```bash
git status --short                      # tauri.conf.json 은 이번 범위가 아니다(무시)
git diff HEAD --stat
git diff HEAD                           # 수정 18 파일
ls app/mcp app/back/alembic/versions/0007_* app/back/tests/test_meeting_token.py app/back/tests/test_agent_options.py   # 신규
```

**산출물** — `orchestration/work/docs-v1/work009-review-report.md` **1개**.

문서는 전부 코디 워크트리 절대경로 · 읽기 전용:
`/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

## 1. 네 층

```
정책       10-decision/decision-003 §2(AI 데이터 접근 — 도구 7개 · DB 직결 아님 · 권한은 백엔드) · §8 「AI 도구 연결」(배치 · 토큰 행) · decision-001 §4(세션 · refresh 규칙은 그대로)
아키텍처    40-architecture/system/README.md §codex 설정(allow list 실측 표 · 함정 셋) · Components MCP 행 · 흐름 ③ · 불변식 13 · 14 · 15 · SYS-12 · 15 · 16
           40-architecture/backend/README.md §2(계층) · §3(schema/dto) · §4(app/mcp 별도) · §5-2(옵션 빌더 한 함수 · 토큰 발급·폐기 자리) · §7(트랜잭션) · §8-1(except Exception 금지) · §9(인증) · §11(env)
           40-architecture/database/domains/account.md A-7(refresh 행에만) · **A-13**(회의 토큰 규칙 넷 — 원문 컬럼 · 회의당 하나 · 폐기 = 행 삭제 · revoked_at 안 찍음) · database/README.md §1 ERD auth_session · §4 인덱스
SPEC       20-spec/spec-007 §4 「AI 도구 7개」 표 + 그 아래 「도구 ↔ REST 대응」 불릿(2026-09-07 코디 확정 — /current · /current/tasks · /auth/session) · 「웜스타트」 표 도구·토큰 행 · §6 AC codex 설정 항목
WP         30-work/work-009-mcp-token.md Phase 1~4 · §Internal Interface Contract(config 목록 문자열 · 순서) · §Open Issues(워커 질문 3건 코디 답)
결정 원본   reference/2026-09-06-task-management-app/Meeting flow.md §1-4 MF-2 · 3 · 4 · §1-5 MF-68 · 69(원문 컬럼) · 70
```

## ⛔ 2. 이번에 반드시 볼 축

### 2-1. 권한 경계 — MCP 가 두 번째 게이트가 됐나 (MF-4 · 불변식 14)

```
① app/mcp 에 판정 · 필터 · 가공 · 캐시가 있나 — 있으면 FAIL. REST 응답을 그대로 돌려줘야 한다
② app/mcp 가 back 을 import 하거나 DB 드라이버를 쓰나 — 0 이어야 한다
③ app/mcp 에 쓰기 HTTP 메서드(POST/PATCH/DELETE) 호출이 있나 — 0
④ 401/404 를 빈 배열·기본값으로 바꾸는 코드가 있나 — 있으면 FAIL(BE §8-1)
```

### 2-2. 토큰 — A-13 넷이 코드가 됐나

```
① 원문 저장 — 해시 함수를 안 만들었나. refresh 쪽 해시는 그대로인가(A-7 회귀 0)
② 회의당 하나 — /start 트랜잭션 안 INSERT · 같은 회의 두 번 INSERT 되는 경로가 없나
③ 폐기 = 행 DELETE — revoke_meeting_token 이 revoked_at 을 찍지 않는가 · 0건이어도 예외 없는가 · A-7 재사용 감지에 안 걸리나
④ 검증 — resolve_bearer: JWT 먼저(DB 안 봄) → 실패 시 원문 조회 → 둘 다 아니면 401 token_expired **하나**. 거부 사유를 흘리는 응답이 있나
⑤ 회의 범위 — 회의 토큰으로 다른 회의 404 · 쓰기 표면 전부 404 · 업무·유형·프로필 조회는 계정 범위. 어느 쓰기 라우터가 빠졌나 grep 으로 전수
⑥ 원문 노출 — meeting_token 이 schemas/ · 응답 · 로그 포맷 · MeetingDetail 에 0건
```

### 2-3. 옵션 빌더 — 한 함수 · 정확한 문자열 (MF-3 · BE §5-2)

```
① provider_options · "config" · mcp_servers 문자열을 만드는 곳이 integrations/agent.py 한 파일 · build_codex_options 한 함수뿐인가
② WP §Internal Interface 의 config 목록과 문자열 · 순서가 같은가 — features.shell_tool=false / web_search="disabled" / features.image_generation=false / features.apps=false / mcp_servers.tm.url / http_headers / enabled_tools 7 / tools.<7>.approval_mode="approve"
③ enabled_tools 에 tm. 접두가 없나 · approval_policy 키가 어디에도 없나(«user cancelled» 함정)
④ sandbox="read-only" 가 새 세션에만 실리고 resume 에는 없나(open-kknaks 가 버린다)
⑤ 호출부(meeting_batch_service · meeting_finalize_service)가 meeting_token 을 넘기기만 하고 프롬프트 · 입력 · 검증을 건드리지 않았나 — WORK-010/011/012 범위 침범이면 WARN
```

### 2-4. 계층 · 트랜잭션 · 예외 (BE §2 · §7 · §8-1)

```
router 가 ORM · 판정을 하나 · service 가 fastapi · schemas 를 import 하나 · repository 가 ORM 을 밖으로 내나
service 가 commit() 을 부르나(start() 의 기존 commit 은 WORK-010 몫 — 이번에 새로 더한 곳이 있나만)
except Exception · 임의 재시도 · 조용한 기본값
GET /api/meetings/current · /current/tasks — router → service → repository 를 지나나 · /current/tasks 가 사후 검사(M-15)와 같은 repository 함수를 쓰나
```

### 2-5. 리비전 · compose · env

```
0007 — kind server_default 'refresh' · meeting_id FK · meeting_token · 부분 인덱스 (meeting_id) WHERE kind='meeting' · CHECK(kind='meeting' ⇔ meeting_id·meeting_token NOT NULL / refresh 행 해시 NOT NULL) · downgrade 가 meeting 행을 지운 뒤 컬럼 제거
compose — db · redis · api · worker · mcp 다섯 · mcp 가 api 를 기다리나 · worker 마운트·PATH 가 안 바뀌었나
config.py — MCP_SERVER_URL 기본값 없음(비어 있으면 기동 실패) · MEETING_TOKEN_TTL_MIN
.env.example 두 줄
```

### 2-6. 테스트가 WP 검증 항목을 덮나

WP Phase 1~4 의 검증 체크리스트 각 항목에 대응하는 테스트가 `test_meeting_token.py`(24) · `test_agent_options.py`(14) · `app/mcp/tests`(40) 에 있나. **없는 항목을 표로.** 특히 — 만료 토큰 401 · 남의 회의 404 · 쓰기 404 · JWT 로 `/current` 404 · 서로 대신 못 함 · 옵션 문자열 순서 · resume 에 sandbox 없음.

## 3. 판정

- **PASS / WARN / FAIL** 셋. 항목마다 **파일:줄 + 어긋난 문서 절 번호**.
- **FAIL** = 정책·아키텍처 불변식 위반(권한 경계 · 원문 노출 · 옵션 빌더 둘 · except Exception · 계층 위반) · SPEC 계약 불일치(도구 이름 · 대응 표면 · 401 하나).
- **WARN** = 범위 침범 · 테스트 공백 · 이름·주석 불일치.
- **문서 공백** = 코드가 아니라 문서가 빈 것 — 별도 절로. 지적이 아니다.

## 4. 하지 마라

- 코드 · 문서 수정 금지. 테스트 실행 금지(코디가 이미 돌렸다 — 557 passed · mcp 40 · compose 5 healthy).
- WORK-010 이후 범위(웜스타트 프롬프트 · 배치 입력 · 종료 파이프라인 · 프론트)를 이 검수에서 요구하지 마라 — 옛 설계 그대로인 것이 정상이다.
- 새 결정을 만들지 마라. 문서에 없는 것은 「문서 공백」으로.

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_be2a2f22-5ec1-4354-ab88-7ccb824100d3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: WORK-009 검수" \
  --body "FAIL n · WARN n · 문서 공백 n / 축별 판정 한 줄씩 / 리포트 경로"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] reviewer 완료 — WORK-009 검수 FAIL n · WARN n. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] reviewer: <질문>" --enter`
