
# [reviewer] WORK-001 수정본 재검수 — F-1~6 및 MCP/assigned 정합

너는 **strong-hajin `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이번은 planner 리뷰다. 코드 워크트리에서 실행하되 실제 검수 대상은 아래 코디 문서 4건이다. 모두 read-only, 보고서 1개만 작성한다.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-wp-report.md` 최초 FAIL F-1~6 / WARN W-1~7.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/strong-hajin-work-wp-fix1-brief.md` 및 `strong-hajin-work-wp-fix2-brief.md` — 코디 기술 결정.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-001-task-creation.md` 최신본.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md` v0.2.3, `spec-002-action-item-review.md` v0.2.2 및 DEC/BASE.
- 실제 코드 레포 AGENTS.md·Makefile·schema/권한/완료/생성/MCP 경로, templates/projects/30-work/work.md.

## 2. 배경

WP 필수 수정과 두 추가 정정이 완료됐다. 기존 F/W 해소 여부와 수정으로 생긴 계약 문제만 검수한다. 코드 착수 전 사용자 리뷰용 계획의 실행 가능성이 목적이다. 작업량을 늘리는 취향 지적은 하지 않는다.

## 3. 확정 방향

멱등 명시키 필수, 신규 요청 출처 상태 assigned(수행 상태와 분리), W1에서 요청 출처/source_work_request_id와 현행 요청자 완료 승인 연속성 유지, 선택 승인자 API/FE는 W2와 동시 활성화. 신규 metadata/DB 제약은 새 일회용 격리 DB에서 검증, migration 도입/기존 데이터 전환 없음. 실제 Makefile 검증과 필수 PostgreSQL/acceptance 검증 유지.

## 4. 검수 대상

위 다섯 문서와 코디 index/config 정합. 코드 temp.md·reference task.md 등 타 작업은 제외. 문서에 인용한 코드 근거를 확인한다.

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-wp-report.md` 하나에 `재검수 (1차)` 절 추가. 최초 리뷰 보존.

## 6. 검수 항목

1. F-1~6, W-1~7별 해소·잔여를 파일:줄로 보고. 요구가 축소된 것을 수정 완료로 보지 않는다.
2. assigned 상태가 출처 저장·요청 조회·FE·완료 승인에 일관되게 연결되고, 가짜 수락/판단회차 없는 경로가 가능한지 실제 코드 대조. API/FE에서 승인자 입력을 받아 무시하는 중간 상태가 남는지 확인.
3. MCP 네 생성 도구의 명시 키와 호출자 재시도/동일 turn 다중 의도/권한 재인가·payload 충돌·동시 회의 후보 승격 검증이 닫혔는지. W1 resolver 범위가 다른 mutation에 번지지 않는지.
4. SPEC 요청 본문의 idempotency_key와 WP REST Idempotency-Key 헤더 설명이 같은 wire 계약인지 확인. 두 위치를 지원할 경우 우선순위/불일치 처리 없는 이중 SoT가 되는지, W1→W2 public 필드 경계는 명시됐는지 확인.
5. schema/전용 DB 이름과 reset_demo 안전 가드·Makefile·DB URL 전파·acceptance 격리가 실제 가능하며 기존 사용자 DB에 작용하지 않는지. 테스트 실행 없이 명령/코드로만 확인한다.
6. MU 머지 단위가 필수 키·권한·생성 public 표면을 따로 깨뜨리지 않는지 확인. 논리 phase 자체를 배포 단위로 오인하지 않는다.
7. PASS/WARN이면 사용자에게 리뷰 가능한 구현 범위 5줄과 남은 비차단 사항을 보고한다. FAIL이면 수정에 필요한 최소 diff를 특정한다. 이미 승인된 기술 방향을 새 선택지로 재개방하지 않는다.

## 7. 제약

리뷰 리포트 외 수정·테스트/빌드/DB 실행·커밋/push 금지. OQ-A/D2 임의 확정 금지. 기존 리뷰 판정과 이번 판정 구분.

## 8. 검증

실제 자료 근거로 검수. phase TODO/완료 증거 미작성 유지. 필수 요구 누락·계약 모순 없음을 확인하며 못 확인한 것은 명시한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_c04e3e99-1781-4d5b-97a0-864db71b9293 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
