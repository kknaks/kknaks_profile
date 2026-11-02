
# [writer] REST 멱등 키 헤더 정합 — RF-1 및 RW-1~4 최소 정정

너는 **strong-hajin `writer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디와 같은 워크트리에서 직렬로 작업한다. 코드 레포는 읽기 전용이다.

## 1. SSOT

`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-wp-report.md` 재검수1차의 RF-1 및 RW-1~4. DEC D-3b는 REST 헤더로 이미 결정돼 있다.

## 2. 작업

남은 한 모순과 짧은 WARN만 고친다. 광범위 재작성·추가 조사 불필요.

## 3. 정확한 정정

- SPEC-001 Request/Response 본문 표의 idempotency_key 행을 제거하고 표 위에 **REST 생성 요청은 Idempotency-Key 헤더 필수, JSON 본문 필드 아님** 명시. 본문 idempotency_key는 허용하지 않는다. MCP는 명시 인자 그대로다.
- SPEC Validation의 키 행도 REST 헤더/MCP 인자를 명확히 구분. sequence의 POST 본문 예시를 `body: assignee_id / header: Idempotency-Key`로 정렬한다.
- WORK Phase1 '입력에 수신자·멱등키를 연다'를 내부 입력 수신자와 **REST 헤더에서 키를 수령**하는 것으로 정정. 키를 REST body에 여는 계획 제거.
- RW-1: MU-A/MU-B 기간에는 새 assignee_id REST 입력을 명시적으로 거부하고, 라우트가 값을 소비하는 MU-C와 함께 허용한다. 받아서 무시하는 중간 상태 금지. 내부 입력 모델과 외부 REST 모델/가드를 구분하는 구현 지시 한 줄 및 검증 한 줄.
- RW-2: assigned 전수 목록에 platform/work_tasks.py:901 쓰기, platform/action_center.py:302 읽기 추가.
- RW-3: MCP key 인자 설명/도구 스키마에 한 생성 의도 한 키·재시도 동일키·새 의도 새키를 명시하는 작업 추가.
- RW-4: create_meeting 선례 이름을 create_current_meeting으로, api.ts:715는 요청 댓글임을 정정.

## 4. 범위

승인된 키 필수·scope·MCP resolver·DB 검증·출처·승인 흐름은 바꾸지 않는다.

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-001-task-creation.md`

## 6. 순서

위 최소 정정 → 키 관련 전송 표현 전수 검색 → 완료 보고(파일:줄). SPEC 버전 갱신.

## 7. 금지

코드·다른문서·index/log·config·리뷰 보고서·DB·테스트·커밋/push 금지.

## 8. 검증

REST 키 본문표0, 헤더 일원화, MCP 명시 인자 유지, sequence와 phase 일치, TODO 8개 유지. 리뷰 전 상태 유지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_403d6b6f-69f4-4925-99a7-f5fa9e7573a8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
