# [backend] WP-123 구현 — MCP 도서관 발행 창구 (leaf · 전용 라우트 · 툴 · 두 층 차단 테스트)

너는 **mediness `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/mcp-library-publish`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/mcp-library-publish-spec/products/mediness/30-work/work-123-mcp-baseline-publish.md` ← **빌드 계획의 SoT (MEDINESS-WP-123).** 4 phase·Code Surface 12행·비목표. **여기 없는 건 발명하지 마라.**
- 같은 워크트리 `products/mediness/20-spec/spec-013-baseline-publish.md` §3 「MCP 계약」 + §3 API 계약 `agent-publishes` 행 ← **계약의 SoT** (2026-08-28 사용자 확정)
- 같은 워크트리 `products/mediness/20-spec/spec-060-mcp-surface.md` §4 ← 툴 선언 규약

**기대는 개념** — 확정 계약 (변경 금지):
- 전용 라우트 `POST /api/v1/library/baseline/agent-publishes` · 신규 leaf `baseline.publish.agent`(**system_admin 에만 부여**)
- JSON body(content 문자열 + format md|html) · **256 KiB** 상한(back 판정, 초과 400 CONTENT_TOO_LARGE) · operation **upload·update 만** (delete 미개방)
- 발행 로직은 기존 서비스 계층(`prepare_upload` → `BaselinePublisher.publish`) **그대로 경유** — 화이트리스트·slug·frontmatter 주입·publish_lock·git commit/push·`baseline_publishes` 복제·변경 금지
- 툴 `mediness.baseline_publish` — write · 즉시형 · `requires("baseline.publish.agent")` · `requires_tools(product_list)` · taint `TAINT_BEYOND_CALLER`

## 2. 배경 / 무엇을 바꾸나

에이전트가 도서관 문서를 읽을 수만 있고 올릴 수 없다. 웹 발행 창구는 그대로 두고(코드 무변경), 관리자 전용 leaf 뒤에 전용 문을 하나 낸다. WP-123 의 4 phase 순서대로 구현한다.

## 3. 계약 (다른 워커와 합의됨)

FE 없음. MCP 클라이언트가 소비하는 툴 계약은 SPEC-013 §3 MCP 계약이 전부다.

## 4. 먼저 읽을 핵심 파일

WP-123 §Code Surface 가 12행으로 정리해 뒀다 — 그 표를 그대로 따라가라. 핵심만 재확인:

- `back/app/routers/baseline_publish.py` — 기존 3 endpoint·`_Capability` 패턴. 어댑터 분리 지점은 WP-123 명시 위치
- `back/app/services/publish/baseline_publisher.py` · `base_publisher.py` — 재사용할 서비스 계층 (수정 금지 대상인지 WP 대조)
- `back/alembic/versions/` — leaf 시드 migration 선례(0095) · **최신 리비전 실측 후 다음 번호** (재검수 시점 실측 0133)
- `mcp/app/server.py` — `_wrap_write_tool`·툴 등록 패턴 / `mcp/app/tool_access.py` — 선언 규약
- `mcp/tests/test_tool_inventory.py` — `EXPECTED_READ`/`EXPECTED_WRITE` 상수 (write +1 갱신)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/`
- `mcp/`
- `docker-compose.yml`
- `docker-compose.local.yml`

## 6. 구현 단계 (WP-123 4 phase 그대로)

1. **P1 — leaf**: `baseline.publish.agent` 신설 + system_admin 부여 migration (0095 선례·최신 리비전 +1). SPEC-003 카탈로그 정합
2. **P2 — 전용 라우트**: `agent-publishes` (JSON · 256 KiB · upload|update · `require_capability("baseline.publish.agent")`) — 입력 어댑터만 새로, 발행은 기존 경유. 기존 3 endpoint diff 0
3. **P3 — MCP 툴**: `mediness.baseline_publish` — thin wrapper, tool_access 선언(§1 기대 값), 인벤토리 상수 갱신
4. **P4 — 두 층 차단 테스트**: ① 비관리자에게 툴 미노출(allowlist) ② 비관리자 라우트 403 ③ 화이트리스트·256 KiB·operation 범위 케이스 ④ 웹 endpoint 무영향 회귀 1건

## 7. 범위 제약 — 하지 말 것

- WP-123 비목표 그대로: delete 개방 · 카드형 배선 · `baseline_publishes` 스키마/commit message 변경 · 웹 발행 UI/endpoint/leaf 변경 · 공통 에러 enum 수정(OPEN-060-C 는 이 WP 가 해결하지 않는다) · leaf 부여 확대 금지
- 스펙·WP 문서 수정 금지 (mediness-mediness 쪽은 planner 소관)
- git 원격 조작 금지 (도구가 push 하는 기능 자체는 기존 서비스 계층 것을 그대로 쓴다 — 새 git 코드 금지)

## 8. 검증

```
cd back && pytest -q <네가 만들거나 고친 테스트 파일만> (전체 스위트 금지 — 사용자 방침. DATABASE_URL 은 back/pyproject.toml 의 테스트 DB = localhost:25434/mediness_test)
cd mcp && pytest -q <네가 만들거나 고친 테스트 파일만> (test_tool_inventory 포함)
검증은 1회만 — 통과하면 반복하지 마라
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_915b3ecb-68dd-4d26-98f7-ef3f645318fb --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_915b3ecb-68dd-4d26-98f7-ef3f645318fb \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_915b3ecb-68dd-4d26-98f7-ef3f645318fb --text "[질문] backend: <질문>" --enter`
