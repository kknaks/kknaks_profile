
# [backend] W1 업무 생성·즉시 배정 전체 구현

너는 **strong-hajin `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

같은 코드 워크트리에서 BE/FE가 분담한다. 다른 워커 소유 경로 및 사용자 definition.md·lifecycle.md는 건드리지 않는다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-001-task-creation.md` 전체, 특히 Internal Interface Contract, Code Surface, Phase 1~8.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md` v0.2.4 W1 및 `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-002-action-item-review.md`.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`.
- 코드 레포 AGENTS.md 및 해당 디렉토리 규칙. 문서들은 read-only.
- 기대는 개념: WORK-001이 명시한 생성 결정·권한·원자성·멱등성 계약을 따른다. 새 제품 정책 발명 금지.

## 2. 배경 / 무엇을 바꾸나

사용자가 2026-09-16 W1 전체 구현 발주와 코디 검증을 승인했다. 신규 업무가 상대 수락 없이 즉시 업무/활성 담당으로 서도록 구현한다. E2E는 사용자가 직접 한다고 명시했다.

## 3. 공통 계약

WORK-001의 W1 부분 계약이 최종 범위다. SPEC의 W2 전체 응답/완료/문의 개편을 당겨 구현하지 않는다.
POST /api/tasks: assignee_id 없거나 본인이면 self, 타인이면 허용 후보에게 즉시 배정. REST 키는 Idempotency-Key 헤더 필수, JSON 본문 idempotency_key는 거부. approver_id 입력/UI는 W2까지 거부/미노출.
한 생성 의도에 키 하나, 실패 재시도/연타는 동일 키, 새 의도는 새 키. 같은 키 다른 payload 충돌. 현재 권한 재검사. 상세 shape와 에러는 WORK Internal Interface 및 SPEC Case Matrix를 따른다. 계약이 빠졌거나 충돌하면 코디에게 질문한다.
WorkRequest 출처는 assigned(즉시 배정됨), source_work_request_id 보존, 요청자 기반 현행 완료 승인 유지. 기존 다섯 출처 상태는 뜻 유지. 일반 구성원에 task.assign/work_request.decide를 새로 주지 않는다.
마지막 리뷰 비차단 관찰 해소: 헤더 필수화와 FE 키 전송은 같은 통합 변경으로 활성화한다. MU-A/B 단독 배포/머지 금지. 전체 W1 단위만 코디 검증 후 반영한다.

## 4. 먼저 읽을 핵심 파일

WORK-001 Code Surface의 경로 전부를 자기 소유 범위에서 추적한다. backend의 entrypoints/http.py·mcp.py, platform/work_tasks.py·organization_access.py·action_center.py·persistence.py·actions.py, modules/work/·meetings/followups.py; frontend의 lib/api.ts·viewModels.ts·labels.ts·idempotency.ts 및 업무 생성/판단함 컴포넌트. 줄 번호는 현재 파일에서 재확인한다.

## 5. allowed_paths

- backend/
- docker-compose.yml
- Makefile

frontend/와 docs/ 수정 금지. operation inventory drift는 필요한 정확한 diff를 보고한다(코디가 후속 처리). 제품 문서도 수정 필요 목록/대체 문장을 보고한다.

## 6. 구현 단계

WORK-001 Phase 1~6 전체 + Phase8 BE 회귀 테스트. 내부 결정 함수, 원장과 payload 충돌/동시성/활성 담당 DB unique, 권한 후보 일치, 수락 gate 제거와 assigned 출처, 회의 후속 승격, REST/MCP/AX/seed 전체 경로를 완성한다. 4개 W1 MCP만 필수 키를 적용하고 공용 _mutation_key의 타 기능 의미는 바꾸지 않는다.
원자성·동시 실행·권한 상실 receipt·완료 승인 연속성을 실제 테스트로 증명한다. 신규 계약에 맞게 테스트를 고치되 단언 삭제/완화로 초록 만들지 않는다.

## 7. 범위 제약

W2/OQ-A/D2 정책 결정 금지. migration 도입/일반 startup DDL 금지. 사용자 DB ax_demo reset 금지. ax_test_w1 전용 빈 격리 DB에서만 metadata 제약 검증. 기존 DB가 있으면 소유/격리부터 확인한다.
문서 Phase Status 수정 금지. 코드 워커 완료 증거를 코디에게 보고. 커밋/push/PR/배포 없음.

## 8. 검증

AGENTS.md대로 Makefile만 사용. 단계에 맞게 make test-unit, make test-contract, 격리 DB make test-postgres를 수행한다. 최종 make verify는 코디가 BE+FE 통합 후 실행하므로 중복 전량 실행하지 않는다.
사용자 지시 우선: acceptance-e2e 및 브라우저 E2E 실행하지 않는다. E2E는 사용자 담당으로 보고. 테스트별 명령/통과 수/실패 원인/로그 경로와 Phase별 증거 및 남은 inventory·문서 수정 목록을 완료 본문에 남긴다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 --from term_963b7fe7-7f52-49f4-af62-63c8100a091c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
