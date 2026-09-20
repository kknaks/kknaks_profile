# [reviewer] v2 스펙 원문 대조 검수

역할: /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md 및 같은 폴더 rules/skills/tools/workflow를 읽는다.
작업 위치: /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin. 코드 /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work 읽기 전용. 기존 W1 미커밋과 다른 세션 문서·디자인 보존.

## 1. SSOT
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting/ 의 정의_v2.md·생명주기_v2.md·작업계획서_v2.md·example.md 전문. 파일명이 NFD이므로 실물 경로를 찾는다. 사용자 v2 스펙+백엔드 승인, 프론트 제외/E2E 사용자. example도 사용자가 직접 지정한 사례 원문이며 미정/검토안은 확정으로 승격 금지.

## 2. 대상
para/projects/summer-star/strong-hajin/ 아래 BASE-002·DEC-002·SPEC-003 전체 및 SPEC-001·002 상단 대체안내. writer 발주서는 같은 work 폴더 strong-hajin-work-v2-spec-brief.md. 기존 문서와 코드 관측은 참고하되 v2 확정 정책 우선.

## 3. 검수 목적
원문 합의 누락/과잉 확정/문서내 모순을 찾아 실제 구현 가능한 계약인지 판정한다. A1~C2 21건과 원문55ID는 단순 ID 존재가 아닌 의미로 확인. example §10 흐름도 추적. SPEC 양식 및 구현 경로 침범 확인.

## 4. 중점
- 요청 send에 Task 생성, accept는 같은 Task, 거절 cancelled/재요청 새 Task. 기존 active 유지 재배정/수락 원자 교체. 본인직접 하위1단계 vs 재귀 중심 판정. read권한과 act권한 분리, 연결자료/하위만 허용. 하위 승인까지 최종완료 차단, 완료보고/보완은 같은 Task.
- REST/MCP/AX/회의 등 외부 계약의 입력/오류/버전/멱등키가 충돌하지 않는가. 유지한다는 W1 계약이 실제 확정계약과 맞는가.
- 기존 데이터·운영DB 초기화 금지/일괄 pending 변환 금지/수락이력 조작 금지, cutover 및 프론트 후행 경계.
- 코디 의심: DEC OQ-204 '현행 배정=지정→상대 수락'이 W1 미커밋 코드와 다를 가능성. SPEC 대체표의 '배정 수락이 신규로 돌아온다'와 배정 제외 간 충돌 확인.
- OQ-201은 v2 재개 규칙으로 기존 질문을 닫는 데 사용자 재승인이 필요한가? OQ-301은 요청자 최종승인이라는 명시 규칙으로 해소되는가? 과거 OQ ID/의미 실물 대조(허구의 OQ-B~G 보류 금지). OQ-202는 UI후행인데 BE 정리계약은 원문으로 정해졌는가? OQ-203은 진짜 미정이지만 전체차단인지 좁게 구분. OQ-204는 원문 명시적 배정 별도와 사용자 범위에 이미 답이 있는가?
- 미정 기본값이 '답 없으면 합의'가 되지 않도록 기존동작 보존/구현 기술선택/사용자 정책 선택 구분. 사용자가 정하지 않은 정책을 기본값으로 몰래 확정하지 않는다. 원문이 이미 답한 것도 다시 질문하지 않는다.

## 5. allowed_paths
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-v2-spec-report.md 하나만 신규 작성. 모든 대상문서/코드/reference/index/log read-only. commit/push/PR 금지.

## 6. 보고
PASS/WARN/FAIL + 각 지적 근거 파일:줄/원문절 + 최소 정정 방향. 실제 사용자 질문만 별도 표로, 답이 있는 질문은 근거로 해소. 모호한 선택은 범위별 차단 여부 표시. 추측으로 FAIL 부풀리지 않는다.

## 7. 금지
문서 직접수정, WORK 작성, 코드수정, DB접속, 테스트/빌드 실행, UI검증, 공유트리 stash/reset/checkout 금지. 실물DB 미확인은 이후 Phase0에서 닫을 관측이며 현재 SPEC 단계 DB실행을 요구하지 않는다.

## 8. 완료 기준
정책/제안/미정 정합, 원문 인수시나리오 의미추적, 현재계약 대체정합 검수. 실행검증은 하지 않았다고 적는다. 완료 후 두 채널 보고하고 idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_29f98b02-b4b2-4735-8daa-81708cb3dfdc --from term_f58155f6-4cbc-4b9a-b129-4759475fe37a \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_29f98b02-b4b2-4735-8daa-81708cb3dfdc \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_29f98b02-b4b2-4735-8daa-81708cb3dfdc --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
