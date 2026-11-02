
# [backend] WORK002 v2 backend 전량 구현

너는 **strong-hajin `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

같은 코드 워크트리 BE/FE 분담. backend·Makefile은 BE, frontend 전부(api/viewModels 포함)는 FE. W1 미커밋을 보존하고 v2 baseline manifest와 비교한다. 새 워크트리/브랜치 생성 금지.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-002-task-lifecycle-v2.md` ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-003-task-lifecycle-v2.md · /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-002-task-lifecycle-v2.md · /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-002-task-lifecycle-v2.md`

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- 별도 개념 지정 없음. SPEC과 WORK의 판단 근거를 따른다.

기존 Phase0 백엔드 세션 재사용 허용. 이제 읽기전용 제한 대신 이 브리프 allowed_paths 안 구현을 수행한다.

## 2. 배경 / 무엇을 바꾸나

사용자 오늘 구현·자동검증 완료 요청. 계획만 보고 끝내지 말고 지정 Phase 전체를 구현하고 의미있는 회귀까지 완수한다. 브라우저 E2E는 사용자 담당. 코드변경 전 기준선 검증은 이미 코디가 완료(322 unit/976 contract/645 frontend/65 PG 전부 exit0). 같은 기준선 재실행 금지.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

SPEC003 §4 Data Contract와 WORK002 Interface/API·Case Matrix를 정확히 소비/제공한다. Task 외부 state는 open/in_progress/done/cancelled, 내부 completion_submitted는 done+derived.approval=awaiting_review로 투영. derived의 생산자는 BE이며 FE는 권한/완결을 추측하지 않는다. 요청발송은 같은 Task pending/assignee null→수락 active, 관리자직접배정 즉시active 유지. completion/proposal/assignment/reopen 모두 서버 envelope 사용. BE API 계약 정리 후 코디에게 파일/shape/명령을 즉시 공유하고 FE 연결한다. 별도 프로세스로 배포하지 않으므로 I1/I2는 두쪽이 함께 완결된 통합 작업트리에서 검증한다.
OQ203 답대기: 완료보고 시 하위차단 추가없이 현행 보존(새 정책 확정으로 표기 금지). OQ206 답대기: system:meeting 완료확인자를 임의지정/자동승인하지 않는다. 다른 모든 경로 진행. 회의승격 seed 삭제로 미결 숨기지 않는다. 미정 M20~24 처분은 WORK 그대로, 새로운 범위를 발명하지 않는다.

검수 R1~3 반영: 외부 done은 승인대기와 최종완료를 합치므로 재개/완료 명령 노출은 서버 봉투(및 derived.approval)로만 판단한다. state=done 단독으로 재개버튼 노출 금지. BASE U1/U2/U6와 인덱스 실재는 배포직전 실제 데이터 DB에서 재확인해야 하며 빈DB의 0건을 배포통과로 쓰지 않는다. 문의/회신대기/상태메모 원장은 미구현 후속이므로 이번 회귀/배포 통과 대상으로 주장하지 않는다. 새 raw done 조건 사용처를 전수 확인한다.

## 4. 먼저 읽을 핵심 파일

- 코드 AGENTS.md 및 WORK002 Code Surface 표 전부(실제 파일로 확인).
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/v2-be-phase0-report.md · /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/v2-phase0-verification.md · /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-v2-work-report.md 읽기전용.
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/v2-code-baseline/manifest.json 기존 W1 경계.

## 5. allowed_paths — 이 밖은 건드리지 마라

- backend/
- docker-compose.yml
- Makefile
- docs/unified-operations-inventory.json (WORK Phase6에 명시된 예외, 차이난 항목만)
- README.md · docs/domain-model.md (이번 코드의 달라진 동작 설명만)
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/v2-backend-implementation-report.md (완료리포트만, 코드워커의 문서쓰기 예외)

## 6. 구현 단계

1. Phase0 보고를 재사용하며 실제 빈DB를 실데이터 통과로 쓰지 않는다. 테스트용 DB는 이 워크트리 postgres localhost:54329, 명시 DATABASE_URL과 다른 POSTGRES_TEST_URL 사용. 기본5432 다른 프로젝트 접근금지. ax_test_v2 등 격리DB 생성/스키마/fixture 쓰기는 승인됨. 사용자 운영DB reset·수정 금지.
2. WORK Phase1~6 전량 구현. migration 기존인덱스 결손 재현/DDL 반복적용/validity/CONCURRENTLY 격리검증 포함. 담당 현재/대기 분리, 생성/수락/거절/재요청, 재배정 원자성, 재귀구조/자료읽기 전표면, 현재완료회차, open직접완료, 제안동의/재개, REST/MCP/AX/seed/inventory 모두 담당.
3. Phase2 projection/명령계약을 준비하면 코디에게 바로 전달. FE파일 수정금지. Phase5 신규명령도 전달. 기존 테스트를 새계약으로 대체할 때 이전보장과 대체보장 매핑; 삭제/skip/약화 금지.
4. Phase8 BE A1~C2 21건 + example10단계 API 연속흐름 + W1 K1~6/K11 회귀·격리PG 동시성까지 증거 남긴다. 실제 데이터 없는 실측과 검증fixture 결과 분리.
5. 모든 단계의 수행/검증/미완료를 보고서에 표로 제공. WORK 상태는 코디가 갱신한다. 전체 make verify는 코디가 하므로 실행하지 않는다.

## 7. 범위 제약 — 하지 말 것

- commit/push/PR/새발주/리셋/stash/다른워커영역 수정 금지. 사용자 프로세스/포트/스택 기동 금지. 테스트는 격리환경. 미정 정책을 숨기거나 임의로 확정하지 않는다.

## 8. 검증

```
코드 레포 AGENTS.md 준수: backend 테스트는 Makefile 타겟으로만 실행. 변경 단계에 맞게 make test-unit 또는 make test-contract, 최종 코디 검증은 make verify 및 격리 PostgreSQL의 make test-postgres와 관련 acceptance journey. 단계별 전량 반복 금지. tests/architecture 경계 및 operation inventory drift 확인(diff 항목만 패치). 스키마 변경은 reset_demo 전용 경로, 일반 API startup DDL 금지. 기존 실패는 기준선과 분리 보고.
Node 20.20.0 사용. PYTEST_XDIST_AUTO_NUM_WORKERS=4는 부하완화이며 검증 면제 아님. 작은 변경별 관련검증 후 최종 소유스위트 한 번; 이유없는 전량반복 금지.
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
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_c2b0c982-7078-4d5b-b14d-9342eef7f699 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
