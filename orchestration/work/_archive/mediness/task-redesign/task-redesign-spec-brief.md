
# [planner] task·incident 전체 재정비 — 스펙 반영 + WP1(task) 작성

너는 **mediness `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/roles/mediness/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

reviewer_spec 워커가 네 산출물을 나중에 같은 워크트리에서 **read-only** 검수한다 — 충돌 없음.

## 1. SSOT — 먼저 읽을 것

**결정의 SoT (코디 레포, read-only 절대경로 — 여기 없는 건 발명하지 마라):**

- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/_RESUME.md` §2 결정 표 — **모든 설계 결정의 정본.** 이 표와 어긋나는 스펙을 쓰지 마라
- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/research-task-status.md` — task 원장 3벌·상태 정의·사용처·냄새 전수 조사 (§C 대조표 포함)
- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/research-incident.md` — incident 렌즈 6 조사 + 죽은 계약 D-1~D-27 + 코드 충돌 C1~C15 (§C 종합)

**기존 문서의 SoT (이 워크트리):**

- `products/mediness/40-architecture/domains/decision_execution_task.md` — A축 도메인 문서 (폐기 계획 대상)
- `products/mediness/20-spec/spec-152-incident-response-workflow.md` — incident 계약 (재서술 대상)
- `products/mediness/20-spec/spec-125-version-wbs-gantt.md` · `spec-110-decision-lifecycle.md` — stale 정정 대상
- `products/mediness/40-architecture/erd.md` — 재작성 대상

기대는 개념 — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

mediness 의 "task" 는 코드상 3개 원장(RuntimeTask 정본 / VersionWbsTask 미러 / DecisionExecutionTask 레거시)으로 갈라져 있고, incident 워크플로는 개정 8회 누적으로 스펙에 죽은 계약 27건이 잔존하며 코드와 크게 어긋난다 (연구 문서 2건 참조). 이번 작업은 **스펙 층위에서 재정비의 정본을 세우는 것**이다:

1. **task 원장 단일화** — RuntimeTask 를 유일 정본으로. `accept_pending` 제거(5값: todo/in_progress/blocked/done/canceled), 수락·거절 개념 폐기(거절→재배정), 재배정=todo 리셋+started_at 클리어, 착수=명시 시작만(자동전환·즉시 in_progress 폐기, 시스템도 todo 생성 후 시작 **전이**), DecisionExecutionTask 이관·폐기, WBS status 컬럼 제거(phase 는 자체 status 유지), 회의록 어휘 canonical 통일, 한글 라벨 SoT 1벌.
2. **incident 재정비** — 확정 흐름(아래 §3)대로 spec-152 를 재서술. 죽은 계약 D-1~D-27 제거, 스펙 유령 이벤트(workflow_closed·follow_up_task_created·feedback_requested) 는 도입/삭제를 명시 확정, TaskEvent 목록 1벌 확정, 라운드 판정 1벌(활성 라운드 = 최대 round_no 기준), run 감사 도입, 종결 시 추적 테스크 정리 규칙, 슬랙 fail-loud.
3. **문서 층위 복구** — `runtime_task`(필요시 `version_wbs_task`) 도메인 문서 신설, ERD 재작성, spec-110/125 stale 정정. 상태 enum·전이표는 도메인 문서가 SoT, SPEC 은 링크만(A축 선례).

## 3. 계약 (사용자와 합의됨 — 이대로 반영)

**incident 정본 흐름 (확정):**

```
슬랙 이슈 채널 이벤트 (웹훅/수집 — 어댑터 연결은 후속. raise 진입 계약에 source 확장만 열어둠)
→ AI 수집(조사)
→ 제품 대표(product_assignment.is_lead) 승인 게이트
→ 승인: 슬랙 채널 생성(fail-loud — 토큰 미설정이면 실행 실패, 조용한 no-op 금지)
        + 추적 테스크: todo 생성 → 시스템 액터의 시작 전이로 자동 에스컬레이션
        + cc = 해당 버전 참여자들 (해소 규칙은 네가 스펙에서 정의하고 OQ 로 표시)
→ 슬랙 [완료] (완료 표면은 슬랙만 — 웹 완료 버튼 없음)
→ AI 회고 + 후속 테스크 후보 → 승인 게이트 → 담당자 테스크 todo 생성
→ 전부 완료(활성 라운드 기준) → AI 피드백 + 후보 → 승인 게이트 → 테스크 생성 → 루프
→ [완료] 승인 시 종료 + run 감사 기록 + 추적 테스크 정리
```

**범위 제외 (OQ 로 명시하고 넘길 것):** 알림/DM·게이트 방치 에스컬레이션(후속 고도화), 슬랙 인바운드 어댑터 실구현, GitHub/Jira mirror.

**WP 구성:** WP1 = task 수정(선행) → WP2 = incident 수정 (직렬). **이번 발주는 스펙 반영 + WP1 문서 작성까지.** WP2 문서는 후속 발주 — 이번엔 스펙에 예고만 남긴다.

## 4. 먼저 읽을 핵심 파일

- `research-task-status.md` §A-2·§B-1·§B-2 — 상태 정의 3벌과 전이표 정본(machine.py 기준)
- `research-incident.md` §A-7 (D-1~D-27) — spec-152 에서 지워야 할 죽은 계약 목록
- `research-incident.md` §A-9 — 개정 이력 감사. "개정 = 추가 + 구 서술 grep 삭제" 를 이번에 절차로 지켜라
- `research-incident.md` §A-10-7 — 조각 계약 1벌 + 파라미터 표 재서술 권고 (게이트 3벌 중복 서술 접기)
- `products/mediness/20-spec/spec-152-...md` :1480-1511 (§Action.status)·:1798-1831 (§제안 2절) — 초안 화석 3절, 삭제/정리 1순위

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/mediness/`
- `context/`

## 6. 구현 단계

1. 결정 SoT(_RESUME §2)와 연구 문서 2건을 읽고, 반영 대상 문서 목록·순서를 짧게 계획한다
2. **도메인 문서 신설**: `40-architecture/domains/runtime_task.md` (enum 5값·전이표 정본·삭제⟂취소 직교·스탬프·TaskEvent 확정 목록), 필요시 `version_wbs_task.md` (status 컬럼 제거 후의 미러 계약·phase 분리)
3. **task 축 정정**: `decision_execution_task.md` 에 이관·폐기 계획 절 추가, spec-110 stale 정정(exec_type 등), spec-125 정정(어휘 cutover 반영·자동전환→알림 강등·accept_pending 제거), 회의록 어휘 통일 반영
4. **spec-152 재서술**: §3 확정 흐름 기준. 죽은 계약 제거(D-목록), 화석 3절 정리, 스테이지 수·전이표를 코드 실측(8 스테이지·11 엣지)에 맞춰 정본화한 뒤 이번 결정을 얹는다. 개정 노트에 이번 개정을 실제 변경과 1:1 로 기록
5. **ERD 재작성**: 코드 마이그레이션 기준(연구 문서 §B 참조) + 이번 결정 반영본
6. work-074 는 **폐기 표시만** 하고 고치지 않는다 (incident 신규 WP 는 후속 발주)
7. **WP1(task 수정) 문서 작성**: `products/mediness/30-work/` 에 신규 번호(기존 최신 다음 번호)로. 스펙(2~5단계 산출물)을 SoT 로 삼아 코드 변경 단위를 계획한다. 코드 좌표는 `research-task-status.md` §B 를 근거로 쓰되 **계약은 반드시 새 스펙을 가리켜라**(연구 문서는 조사 스냅샷이지 SoT 가 아니다). 포함할 축: enum cutover 마이그레이션(0108 선례·양 enum 동시·기존 행 todo 매핑) / machine·lifecycle 수정(decline 제거·reassign todo 리셋·`_STATUS_EVENT`/`_STAMP` 재정의) / 착수 명시화(스케줄러 강등·즉시 in_progress 폐기 지점 전수) / DecisionExecutionTask 이관·폐기 / WBS status 컬럼 제거 / 회의록 어휘 통일 / round 평가 seam 이동 / FE·MCP 표면 연쇄(칸반 4열·수락/거절 UI·`task_decline` 제거·라벨 SoT) / 테스트 갱신 목록
8. 검증(§8) 통과 확인 후 완료 보고

## 7. 범위 제약 — 하지 말 것

- **코드 레포(mediness-app)를 건드리지 마라** — 이번 발주는 문서만
- WP 문서(30-work/)는 **WP1(task) 1건만** 새로 쓴다. WP2(incident) 는 쓰지 마라 — work-074 폐기 표시만 예외
- 결정 SoT 에 없는 설계를 발명하지 마라 — 애매하면 스펙에 OQ 로 명시하고 코디에게 질문
- 타 제품(products/mediness 밖) 문서를 고치지 마라
- 알림/DM·슬랙 어댑터·에스컬레이션을 스펙 본문 계약으로 넣지 마라 (OQ/후속 절에만)

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict
```

- 이번 제품(mediness) 범위 ERROR 0 을 확인한다. 타 제품 기존 WARN/ERROR 는 "무관"으로 분리 보고한다.
- 추가 자체 점검: 이번에 지운 죽은 계약(D-목록)의 키워드가 products/mediness/ 에 남아 있지 않은지 grep 으로 확인한다 (잔존 시 사유 보고).
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --from term_27a7ad02-3919-43d0-b806-95e8c8eb18cc \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
