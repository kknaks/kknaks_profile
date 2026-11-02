# [writer] 업무 v2 스펙 정리 — 백엔드 선행, 프론트 제외

역할 문서: /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md 및 rules/skills/tools/workflow.
작업 위치: /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin. 코드 조회: /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work 읽기 전용. 기존 W1 미커밋 변경과 다른 세션 디자인 파일 보존.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting/정의_v2.md` 전체.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting/생명주기_v2.md` 전체.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting/작업계획서_v2.md` 전체.

위 세 문서가 최신 사용자 승인 방향이다. 기존 definition/lifecycle 및 SPEC001/002와 충돌하면 v2 방향을 우선하되 과거 기록을 지우지 않는다. reference/example.md는 존재/내용을 확인해 보조로만 읽고 최신 세 문서와 충돌 시 보고한다.
규칙: para/para.md → para/projects/project.md. 양식: templates/projects의 baseline/decision/spec. 기대는 개념: 필요 개념은 실제 기존 규약을 읽어 연결, 출처 없는 개념/합의 발명 금지.

## 2. 배경/승인 범위

2026-09-17 사용자: 프론트 전면 디자인 개편 예정이므로 v2 스펙+백엔드만 먼저 진행 승인. 이번 발주는 스펙 단계만이다. WORK 계획과 코드 구현은 스펙 검수 뒤 별도 발주한다. 프론트/UI/E2E/디자인 싱크 제외. 백엔드 계약·MCP·자동 검증·격리 DB/기존 데이터 호환 설계가 다음 단계 범위다.

## 3. 반드시 반영할 계약

요청 발송시 open Task+상위 연결, 수락시 같은 Task 담당 확정(시작과 별개), 거절 cancelled/재요청 새 Task+이력. 담당 변경은 기존 active 유지→새 담당 수락시 교체, 거절해도 기존 책임/Task 유지. 중심 업무별 직접 작업1단계, 다른 사람이 수락한 요청은 새 중심업무로 재분해 가능. 표시 깊이와 저장 깊이 분리.
요청자는 요청 Task 하위·연결 자료 조회 가능하되 무관 자료 차단. 파일본문/다운로드/검색/미리보기 동일 권한. 완료 보고/보완은 같은 Task, 별도 검토 Task 없음. 취소 제외 미완료 하위가 있으면 최종 완료/승인 차단, 자동 완료 없음. 수락 전 철회/후 취소 동의, 수락 후 조건변경 동의, 무응답/지연 자동전이 없음, 종류별 재개 및 완료 상위 선재개.
work_requests/tasks/task_assignments 역할 공유, active 최대1/멱등성/현재권한 재검사/AX 사람확인/출처 실제 actor 등 W1의 유효 보장 보존. 기존 즉시 active를 일괄 pending으로 변환하거나 수락 이력 조작 금지. 운영/사용자 DB 초기화 금지.
신규 배정·무담당 첫 지정·배정 수정취소재개·체크리스트 강제·중간검토·공동담당/복수부모·자동수락은 미정/범위별도. 이를 요청 정책으로 덮지 않는다. 미정이 독립이면 전체 진행 차단하지 않는다.

## 4. 읽기/관측

기존 SPEC001/002·DEC001·WORK001과 현재 미커밋 코드의 관련 표면을 대조한다. 원문 계획의 코드 현황/DB 미확인은 과거 관측이므로 지금 확인한 사실과 구분. DB접속/테스트/코드수정은 이번 금지. 관측 경로/줄과 불확실성만 기록. 47/1297 등 과거 통과를 v2 통과로 사용하지 않는다.

## 5. allowed_paths

신규 3문서:
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-002-task-lifecycle-v2.md
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-002-task-lifecycle-v2.md
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-003-task-lifecycle-v2.md
기존 SPEC001/002에는 v2가 대체하는 절과 SPEC003 참조를 밝히는 짧은 상단 안내만 허용(기존 본문/버전 이력 지우지 않음). index/log/WORK/reference/코드/디자인 파일 수정 금지.

## 6. 산출물 기준

BASE002에는 사용자 원문 사실·현재 관측 구분. DEC002에는 W1→v2 변경/유지/미정 및 근거. SPEC003에는 백엔드 외부 계약(입력/응답/상태/허용명령/오류/권한/동시성/멱등성/관계 조회)과 작업계획서 A1~C2 전수 추적. UI 동작 원문은 미래 프론트 요구로 보존하되 이번 구현 책임은 API 계약으로 명확히 분리한다.
상태값/관계명 등 기술 선택은 제안인지 확정 정책인지 표시하되 구현 가능한 단일 초안을 제시한다. 사용자 판단이 필요한 업무 정책만 질문으로, 일반 FK/인덱스/transaction 설계 질문을 사용자에게 돌리지 않는다. SPEC에는 코드경로/구현 단계 넣지 말고 BASE에 둔다. 데이터 호환·cutover·미정 경계 명시.

## 7. 금지

새 WORK작성/코드/DB/테스트/배포 없음. stash/reset/checkout 및 사용자 파일 수정 금지. W1 기록을 현재 v2 지원으로 포장하지 않는다. scope 밖 정책을 해결했다고 적지 않는다.

## 8. 검증/완료

세 원문→SPEC 항목/인수조건 추적 누락0, 정의↔생명주기 충돌/미정 목록, 기존 계약 대체 안내 정합, 양식/links/frontmatter 확인. 실행하지 않은 검증 수치 주장 금지. 작성 파일과 검수 포인트/실제 정책 질문만 완료 보고. 승인된 후속 단계가 있으므로 미정의 영향 범위를 좁혀 보고.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_29f98b02-b4b2-4735-8daa-81708cb3dfdc --from term_6e8c0c3c-a880-4dc6-b5bf-9fea4e7023e3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_29f98b02-b4b2-4735-8daa-81708cb3dfdc \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_29f98b02-b4b2-4735-8daa-81708cb3dfdc --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
