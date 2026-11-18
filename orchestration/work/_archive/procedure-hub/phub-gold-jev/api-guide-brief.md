# [writer] 허브 gold REST · MCP 호출 안내 — 다른 서비스용

너는 **procedure-hub `writer` 워커**다. 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/writer/role.md`(+ 같은 폴더 문서).

`P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · `W=$P/orchestration/work/phub-gold-jev` · 허브 코드(읽기만) `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(stg 에 올라간 판 = release/v1.2.0 aa46a86).

## 목적

다른 사내 서비스(앱 · 에이전트)가 **데이터 메달리온 gold** 를 stg 허브에서 REST 또는 MCP 로 불러 쓰게 하는 안내서. 사용자 요청: 「mcp rest api 호출 방법 — 다른 서비스들에도 이 데이터 메달리온 쓸 거라서」.

## 근거(이것만 · 지어내지 마라)

- 계약: `$W/SPEC-001-hub-gold-mcp.md` 0.8.1(도구 9 · 입력 · 출력 필드 · 오류 · cursor · 응답 머리) · `$W/SPEC-003-hub-gold-db.md` 0.2.0 §11(app.main 마운트 · 꺼짐 503 `unavailable`) · `$W/SPEC-007-image-data.md`(그림은 DB 에만 · 출력은 다음 판)
- 코드: `backend/app/modules/gold/*` · `router/gold.py` · `mcp_server.py` · `swagger_docs/gold.py`
- 실물: **stg 는 GET/MCP 읽기로 직접 불러 예시를 실제 응답에서 뽑아라** — REST `https://api-stg-csp.medisolveai.com/procedure-hub/gold/*` · MCP `https://api-stg-csp.medisolveai.com/procedure-hub/gold-mcp/mcp`(streamable HTTP · `Accept: application/json, text/event-stream` · initialize → `mcp-session-id` → notifications/initialized → tools/list · tools/call). 쓰기 요청 없음. 많이 부르지 마라(예시당 1~2 번).
- 상담 앱이 쓰는 꼴(참고): 앱 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev` `clinic_chat/clients/hub_rest.py` · `hub_mcp.py`

## 쓸 것: `$P/para/projects/company/procedure-hub/gold-api-guide.md`

1. 한 줄 요약 · 무엇이 들어 있나(gold 15 표의 뜻 · silver 는 DB 에만 · 데이터 판 = gold_hash) · 공개 정보 · 읽기 전용 · LLM 없음
2. 주소(stg) · 인증(지금 없음) · 상태 확인(`gold/health` — 200 이면 켜짐 · 503 `unavailable` 이면 꺼짐)
3. **시작하는 길**: 이름 → 코드(`resolve` 정확 일치 · 목록 꼴) → 고민 → 시술(`concern_candidates`) → 대상의 정보(`facets` · `scope` · `pair` · `evidence` · `neighbors` · `coverage`) — 흔한 질문 꼴 3~4 개의 호출 순서
4. 도구 9 표: REST 경로 · MCP 이름 · 입력(필수/선택 · 한도) · 출력 핵심 필드 · 쪽 넘김
5. 공통: 응답 머리(`build.gold_hash` · `request` · `total` · `next_cursor`) · 오류 꼴(`invalid_argument` 422 · `not_found` 404 · `unavailable` 503 등 실제 코드대로) · `Server-Timing`
6. 예시: curl(REST) 4~5 개 · MCP(curl 로 세션 열기 · tools/call) · Python(httpx) 하나 · Claude/MCP 클라이언트 설정 한 토막 — **실제 stg 응답을 줄여서**
7. 주의: resolve 는 정확 이름만(문장을 넣으면 0 — 문장 해석은 부르는 쪽 몫) · 데이터 갱신 시 gold_hash 가 바뀜 · 그림은 아직 응답에 없음 · 바뀌는 곳(SPEC 링크 — 경로만)
8. 변경 기록 한 줄(2026-11-18 stg 첫 공개)

꼴: 한국어 · 사람이 읽는 안내서(내부 결정 번호 · 워커 용어 최소) · 표와 코드 블록 위주. 내부 IP · VM 이름 · DB 접속 값 · 키 쓰지 마라(공개 Gateway 주소는 됨).

## allowed_paths

쓰기: 그 파일 1개(+ 같은 폴더 `README.md` 에 링크 한 줄). 그 밖 금지.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer(gold-api-guide) 완료: <한 줄>" \
  --body "변경 파일 / 확인한 실물 호출 수 / 주의점" \
  --outcome succeeded

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] writer(gold-api-guide) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
