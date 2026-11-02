
# [backend] WP-129 업무 요청 축 — P0~P3 · P5 · P6 구현

너는 **mediness `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

**FE 워커가 같은 워크트리의 `front/` 에서 병렬 작업 중이다 — `front/` 를 건드리지 마라.**

## 1. SSOT — 먼저 읽을 것

**빌드 계획의 SoT (spec 워크트리, read-only 절대경로 — 여기 없는 건 발명하지 마라):**

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec/products/mediness/30-work/work-129-task-request-axis.md` — **이 브리프의 정본.** 네 몫 = **P0(사전 실측) · P1(migration 인덱스) · P2(요청 축 BE) · P3(채팅 담당자 개방) · P5(샤라웃 지시 입구 주석 비활성) · P6 중 BE 항목.** P4(FE)는 FE 워커 몫. Phase 의 작업·검증 체크리스트를 그대로 따른다
- 같은 디렉토리 `../20-spec/spec-154-decision-workflow.md` §4.8 — 요청 판정·입력 개방·DM 계약
- `../20-spec/spec-155-ax-task-draft-workflow.md` §6.1·§7 — 채팅 담당자 해소(발화 명시 시에만·같은 조직 활성 구성원·모호하면 요청자 본인)
- `../20-spec/spec-111-decision-intake-slack.md` · `spec-156-decision-chat-intake-workflow.md` — 지시 입구 차단 좌표
- `../20-spec/spec-119-decision-notify-slack.md` — DM 발송 규율(재사용 — 인프라 신설 금지)

**결정 원문 (필요 시):** `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/_RESUME.md` §2

기대는 개념 — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

업무 요청 = 파생 개념(비워크플로 task_type ∧ `created_by_member_id ≠ assignee_member_id`) — 테이블·컬럼·상태 신설 없이 여는 축이다. 네가 만드는 것: `created_by` 인덱스 1건(유일한 migration), 요청자 관점 조회(scope=requested), 배정 DM 훅(graceful), 요청자 권한(수정·취소), 채팅 담당자 해소, 샤라웃 지시 입구 주석 차단.

## 3. 계약 (핵심 불변 — WP 가 상세를 소유한다)

- **게이트 재도입 금지** — 수락·검수 어떤 형태로도. 거부 = 재배정 요청
- **migration = 인덱스 1건뿐.** P0 실측이 어긋나면(예: `created_by_member_id` 부재) 작업을 멈추고 즉시 보고 — 코디 실측으로는 실재한다(`back/app/models/action_runtime.py:621`)
- **DM graceful** — spec-119 인프라 재사용, DM 실패해도 태스크 생성. incident fail-loud 와 혼동 금지
- **자동 cc 없음** — 요청자를 task_ccs 에 넣지 마라
- **샤라웃 지시 차단은 입구만 주석 비활성** — 내부 로직·원장 삭제 금지, 재활성 가능해야 함. 결정 승인·[후속 실행] 발 부트스트랩은 **살아 있어야 한다**(WP-129 P5 금지선·검증 체크리스트 준수)
- 상태 축·TaskEvent 어휘 불변

## 4. 먼저 읽을 핵심 파일 (워크트리)

- `back/app/services/action_runtime/tasks/manual_surface.py` — 생성·권한 판정 seam (`:437,456,691` creator 자격)
- `back/app/services/action_runtime/tasks/factory.py` — `create_task_with_cc`
- `back/app/models/action_runtime.py:577` — RuntimeTask (인덱스 __table_args__ 선례 `:668`)
- `back/app/routers/action_runtime_v2.py` — 조회·생성 endpoint
- WP-129 §Code Surface 표 — 나머지 좌표 전부

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/` · `mcp/` · `docker-compose.yml` · `docker-compose.local.yml`
- ⛔ `front/` 금지 (FE 워커 병렬 중)

## 6. 구현 단계

WP-129 의 Phase 순서 그대로: P0 실측 → P1 migration → P2 요청 축 → P3 채팅 → P5 입구 차단 → P6 테스트 정리. 각 Phase 의 검증 체크리스트를 통과시키고, **WP 문서의 Status 는 갱신하지 마라**(코디 몫) — 완료 보고에 Phase 별 결과를 적는 것으로 대신한다.

## 7. 범위 제약 — 하지 말 것

- P4(FE)·WP-130 범위(background/goal·task_references·완료 모달) 건드리지 마라
- 전체 테스트 스위트 실행 금지 (사용자 방침)
- 커밋·push·PR 금지 (§9)

## 8. 검증

```
cd /Users/kknaks/orca/workspaces/mediness-app/task-improve/back && pytest -q <네가 만들거나 고친 테스트 파일만>
```

- 전체 스위트 금지 — 사용자 방침. DATABASE_URL 은 back/pyproject.toml 의 테스트 DB = localhost:25434/mediness_test. **검증은 1회만 — 통과하면 반복하지 마라.**
- migration 은 로컬 왕복(upgrade→downgrade→upgrade) 확인.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 브리프 작성 시점 값이라 오래됐을 수 있다 — preamble 값과 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "Phase 별 결과 / 변경 파일 목록 / 검증 수치(pytest N passed) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[질문] backend: <질문>" --enter`
