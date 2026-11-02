# [planner] MCP 도서관 발행 도구 — SPEC-060·SPEC-013 개정 초안

너는 **mediness `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/roles/mediness/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/mcp-library-publish-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

- `products/mediness/20-spec/spec-060-mcp-surface.md` ← MCP 도구 표면의 SoT. 도구 인벤토리·권한 선언 규약(§4)·OQ-10(leaf 쪼개기 예정 경로)
- `products/mediness/20-spec/spec-013-baseline-publish.md` ← baseline 발행의 SoT. path 화이트리스트·발행 로그·git push 규약
- `products/mediness/20-spec/spec-230-landing-agent-chat.md` ← tool_access 선언 seam 의 근거 (§3 D16) — 개정 대상은 아니고 참조
- 구현 실물 (읽기 전용 참고): `/Users/kknaks/git/harness_works/mediness-app/mcp/app/tool_access.py` (선언 규약 주석) · `mcp/app/tools/` (기존 도구 패턴) · `back/app/routers/baseline_publish.py` (현행 REST — `require_capability("baseline.publish.basic")`) · `back/app/services/publish/baseline_publisher.py` (화이트리스트)

**기대는 개념** — 사용자 확정 요구 (재논의 금지):

1. **MCP 에 도서관 문서 발행 도구를 연다** — 기존 REST `POST /library/baseline/publishes` 의 thin wrapper. 화이트리스트·발행 로그·git 동작은 SPEC-013 그대로, 새 정책 발명 없음.
2. **MCP 경유 발행은 시스템 관리자 capability 일 때만 가능하다.** 두 층 모두 — tool_access `requires()` 선언(노출 제한) **그리고 back 재판정(실행 게이트)**. 웹 화면 발행은 현행 `baseline.publish.basic` 그대로 유지한다 — 조이지 않는다.

## 2. 배경 / 무엇을 바꾸나

MCP 도구 표면에 도서관 쓰기 도구가 없어 에이전트가 도서관에 문서를 올릴 수 없다. REST 발행 창구(SPEC-013)는 이미 있으므로 MCP 도구로 여는 것인데, MCP 경유는 에이전트가 호출하는 경로라 사람 화면보다 좁게 — 시스템 관리자 capability 전용으로 — 연다. SPEC-060 §4 원칙(툴 계층은 게이트가 아니다 — back 이 재판정)과 OQ-10(운영 요구가 생기면 leaf 를 쪼갠다)이 이 개정의 근거 프레임이다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음 — 코드 계약은 WP 단계에서. 이번 태스크는 스펙 개정 초안까지다.

## 4. 먼저 읽을 핵심 파일

- `products/mediness/20-spec/spec-060-mcp-surface.md` §4 (권한 선언) · §5 OQ-10 — 개정이 앉을 자리
- `products/mediness/20-spec/spec-013-baseline-publish.md` §Functional Rule / §Path Guard — MCP 경유 조항이 앉을 자리
- `products/mediness/20-spec.md` — spec map·변경 이력 미러 (개정 시 동기)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/mediness/`
- `context/`

## 6. 구현 단계

1. SPEC-060 개정 초안: `library_publish`(이름은 기존 도구 명명 규칙에 맞춰 확정) 도구를 인벤토리에 추가. 선언 leaf = **시스템 관리자 capability 계열** — 기존 capability 체계에서 실제 leaf 이름을 확인해 쓰고, 없으면 OQ-10 경로대로 신설 leaf 를 정의한다 (이름·부여 대상 명시)
2. SPEC-013 개정 초안: 「MCP 경유 발행」 조항 신설 — back 재판정이 시스템 관리자 leaf 로 이뤄지는 판정 위치(전용 판정 분기 또는 전용 라우트 — 스펙이 하나로 정한다), 웹 발행(`baseline.publish.basic`)과의 관계 명시. 화이트리스트·로그·git 은 변경 없음을 명시
3. 개정 중 정할 설계 항목 (스펙 본문에 답을 적는다. 정할 수 없으면 OQ 로 남긴다):
   - 콘텐츠 전달 방식과 크기 상한 (md/html 본문 인자)
   - operation 범위 — 현행 REST 가 받는 것(create/update/delete 여부 확인) 중 MCP 에 여는 범위
   - 감사 로그에 MCP 경유 여부를 남길지
4. spec map(`20-spec.md`)·변경 이력 동기, frontmatter·lineage 규약 준수
5. 개정은 **draft 상태**로 둔다 — accepted 단정 금지 (사용자 리뷰 전)

## 7. 범위 제약 — 하지 말 것

- WP·코드 작성 금지 — 이번 태스크는 스펙 개정 초안까지
- SPEC-230 본문 수정 금지 (참조만)
- 웹 발행 권한(`baseline.publish.basic`) 축소 금지
- `products/mediness/` 밖 타 제품 문서 수정 금지

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/mediness/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관' 분리 보고)
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
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_915b3ecb-68dd-4d26-98f7-ef3f645318fb \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_915b3ecb-68dd-4d26-98f7-ef3f645318fb --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
