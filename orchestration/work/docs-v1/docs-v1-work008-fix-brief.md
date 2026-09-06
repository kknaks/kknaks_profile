# [frontend+backend] WORK-008 검수 수정 — FAIL 1 · WARN 4

너는 **task-management 코드 워커**다.

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`).
**검수 리포트** — `orchestration/work/docs-v1/work008-review-report.md` **먼저 통째로 읽어라.**
(절대경로: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/work008-review-report.md`)

## ⛔ 1. 닫을 것 — 5건

### F-1 (FAIL) — `features/meetings` → `features/tasks` 배럴 import 4건 · **fe**

```
LinkTaskDrawer.tsx:32       canTransition · fetchRelationCandidates · TaskRelation
useMeetingTaskLink.tsx:33   openTaskDetailDrawer · useTaskDoneToast
```

`frontend/README.md` §2 규칙 4(L163) 「영역 사이 import 금지」.
**예외는 「업무·회의 드로어를 다른 영역이 재사용」 하나뿐**이다.

```
openTaskDetailDrawer            → 예외에 해당한다. **그대로 둬라**
canTransition                   → 로직. lib/ 로 올려라
fetchRelationCandidates         → API. lib/ 로 올려라
useTaskDoneToast                → 훅. lib/ 로 올려라
TaskRelation                    → 타입. 위 셋을 따라간다
```

**WORK-006 검수 W-1 에서 같은 규칙을 닫았고(`618d5bb`) 이번에 다시 열렸다** — 리포트의 G-5 재발이다.
`useRowFailures` · `useWorkSettings` · `inlineErrorMessage` 를 `lib/` 로 올린 것과 **같은 방식**으로 해라.

**정적 검사가 배럴을 못 잡는다.** 리뷰어 판정 — 검사 ⑨ 는 `ac9ee5b` 부터 배럴(`@/features/tasks`)을 통과시키던 **원래 구멍**이다.
**⑨ 의 정규식을 배럴까지 잡게 고쳐라.** 그래야 다음에 또 새지 않는다.
**예외 하나(`openTaskDetailDrawer`)만 허용 목록에 두고 근거 주석을 달아라.**

### W-1 — 목록 미리보기 `ended` 의 통합본 트리가 플레이스홀더 · **fe**

```
MeetingPreviewPanel.tsx:152-153
  <EmptyState message="통합본 트리는 WORK-008 에서 만든다" />
```

**두 WP 가 서로에게 넘겨 아무도 안 만들었다.** WORK-008 Scope L87 이 「목록 → WORK-006」으로 뺐고 WORK-006 은 SPEC-008 로 넘겼다.

```
SPEC-006 §7 L728   ended 통합본 렌더는 SPEC-008 규격을 **읽기 전용으로 그대로** 쓴다
WORK-008 L155      미리보기가 AgendaLineTree(track='merged', editable=false) 를 읽는다
```

**`AgendaLineTree` 를 `agendas={merged}` · 읽기 전용으로 부르면 된다.** 새 컴포넌트를 만들지 마라.
Phase 3·4·6 워커가 「5줄 교체」로 보고한 자리다.

### W-2 — `SurfaceNotImplementedError` 가 죽은 코드 · **be**

Phase 5 가 501 스텁을 교체하면서 사용처가 0이 됐다. **지워라.**

### W-3 — `MeetingStatusPlaceholder.tsx` 죽은 파일 · **fe**

사용처 0. **지워라.**

### W-4 — 「종결 · HH:MM」이 계약 밖 필드를 읽는다 · **fe**

`mergedSummary.integratedAt` 은 통합 시각이지 마지막 배치 시각이 아니다.
**`MeetingDetail` 에 마지막 배치 시각이 없다**(문서 공백 DG-2).

**코드를 새로 만들지 마라.** 지금 동작(`integratedAt ?? updatedAt`)을 두고,
**그 자리에 「계약 공백 — DG-2」 주석만 달아라.** 필드를 추가할지는 문서가 정한다.

## 2. 손대지 마라

```
D-2 / DG-9  AI 세션 없는 회의가 /end 에서 갇힌다 — **사용자 결정 대기.** 새 분기 금지
W-1(007)    meeting_service.start() 의 commit() — 아키텍처 규약 충돌. 문서 대기
DG-1        ERD M-20 「빈 자리 그대로」 ↔ SPEC-008 「뒤 줄 당김」 모순 — 문서가 정한다.
            **코드는 지금 동작(당김)을 유지해라**
DG-5 · DG-6 · DG-13   전부 문서 몫
job 의 _plans 프로세스 메모리   BE §5-3 과의 관계는 문서 몫
```

## 3. 지킬 것

1. **위 5건 밖을 고치지 마라.** 발견하면 보고에 적어라
2. **문서를 고치지 마라** · **커밋·push 하지 마라**
3. **`task_service.py` 를 고치지 마라**
4. **`lib/` 로 올릴 때 업무 화면이 깨지지 않는지 확인해라** — `tasks` 기존 테스트 전부 통과

## ⛔ 4. 검증 — **통과 판정 규칙**

```bash
cd app/back  && uv run pytest -q <고친 테스트>
cd /Users/kknaks/orca/workspaces/task_management/docs-v1 && make test     # 전체. 반드시
cd app/front && npx tsc --noEmit && npx vitest run
```

```
① make test(전체)를 돌려라 — 단독 실행만으로 판정하지 마라
② vitest 출력의 **`Errors` 줄이 0** 인지 확인해라 — passed 숫자만 보지 마라
   이 work 에서 두 번 다 코디가 잡았다
```

**F-1·W-1 은 테스트로 고정해라** — ① `features/*` 사이 import 가 **배럴 포함** 0(예외 1건만) ② 미리보기 `ended` 에 통합본 트리가 그려진다.

## 5. Done Criteria

- [ ] `features/meetings` → `features/tasks` 가 **`openTaskDetailDrawer` 하나만** 남았다
- [ ] **정적 검사 ⑨ 가 배럴 import 를 잡는다** — 일부러 넣어 보고 실패하는지 확인해라
- [ ] 미리보기 `ended` 가 `AgendaLineTree`(merged · 읽기 전용)를 그린다. 새 컴포넌트 0
- [ ] 죽은 코드 2개(`SurfaceNotImplementedError` · `MeetingStatusPlaceholder.tsx`) 사라짐
- [ ] 「종결 · HH:MM」 자리에 DG-2 주석
- [ ] `make test`(전체) 통과 · `tsc` 0 · `vitest` 통과 · **`Errors` 0**
- [ ] `task_service.py` 변경 0 · 커밋 없음

## 6. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_94e2f5ee-ce12-40e8-a5c6-72cad891934a \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "WORK-008 검수 수정 완료" \
  --body "5건 각각 어디를 어떻게(파일:줄) / lib/ 로 올린 것과 업무 화면 회귀 확인 / **정적 검사 ⑨ 가 배럴을 잡는지 일부러 넣어 확인한 결과** / 미리보기 ended 트리 / make test(전체)·tsc·vitest 결과와 **Errors 줄** / 손대지 말라 한 것을 안 건드렸다는 확인 / 범위 밖 발견"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] WORK-008 검수 수정 완료. 상세는 인박스." --enter
```
