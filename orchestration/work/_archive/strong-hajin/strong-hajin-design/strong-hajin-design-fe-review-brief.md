# [reviewer] WORK-007 Phase F-1·F-2·F-3 — 프론트 구현 검수

너는 **strong-hajin `reviewer` 워커**다. 역할 문서를 먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

읽을 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-design` (브랜치 `kknaksss/strong-hajin-design`)

## 0. 읽기 전용이다

코드를 **한 줄도 고치지 마라.** 산출물은 리포트 한 장이다.

- 쓰기: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/work/strong-hajin-design/review-fe-report.md`

⚠ **이 워크트리에는 backend 변경도 함께 있다.** 그것은 이미 검수를 통과했다(`review-be-report.md` PASS).
**너는 `frontend/` 만 본다.** `backend/` diff 를 지적하지 마라.

## 1. 무엇에 비추어 보나

| 기준 | 경로 |
|---|---|
| **확정 시안 (화면의 정본)** | `reference/2026-09-10-sc-meeting/package 2/TaskDetail.html` |
| **계약 SoT** | `.../20-spec/spec-007-task-detail.md` (v0.2.0) |
| **단계·Acceptance** | `.../30-work/work-007-task-detail.md` F-1(:342) · F-2(:379) · F-3(:416) |
| 서버가 실제로 내는 것 | `.../orchestration/work/strong-hajin-design/be-report.md` |
| 워커 리포트 | `.../orchestration/work/strong-hajin-design/fe-report.md` |
| 착수 전 화면 상태 | `.../orchestration/work/strong-hajin-design/fe-survey-report.md` |

## 2. 진단 — `git diff origin/main -- frontend/` 로 시작한다

워커 리포트를 **믿지 말고** diff 로 확인해라.

## 3. 계약 대조 — 어긋나면 FAIL

### 시안 대조

1. **덩어리 여섯** — 업무 메타 · 업무 정보 · 연관 업무 · 자료 · 진행과 판단 · 이력
2. 세 덩어리 제목(업무 정보·연관 업무·자료)이 **같은 레벨**인가
3. **업무 정보는 1열** (업무 내용 → 체크리스트)
4. **연관 업무 2열 짝** — 상위\|프로젝트 · 하위\|선행 · 참고\|후행
5. **자료 2열** — 참고 자료 \| **결과 자료**(「산출물」 아님, 이 화면만)
6. 목록 **3행 기본 + 칸 안 스크롤**, 머리는 스크롤 밖 고정
7. 「편집」 단추는 **A 에만**
8. 「추가」는 **글자 + 파란색**

### 동작 계약

9. **선행 배선 복구** — 상세 조회가 `predecessors` 를 실제로 채우나.
   **`successors` 도 같은 함정에 빠지지 않았나** (목록에서 연 서랍에서도 서나)
10. **못 읽는 후행은 건수만** — 제목·담당자가 화면 어디에도 안 나오나
11. **못 읽는 선행도 건수만이고 미완으로 센다**
12. **선행=시작 / 하위=완료** — 문구가 갈려 있나. 한 낱말로 뭉갠 자리가 있나
13. **화면이 유효성을 선제로 막지 않는다** — 자기 자신·이미 걸린 항목 **둘만** 거르고 나머지는 다 고를 수 있나
14. **거절 문장을 그대로 보여주나** — 서버는 `detail` 문장 하나만 준다(기계용 `code` 없음)
15. **저장은 칸마다 따로** — 한 칸 거절이 나머지를 되돌리지 않나
16. **비공개 후행에 해제 단추가 없나**
17. **OQ-709** — 못 읽는 선행만 남았을 때 [시작] 을 **막지 않나**
18. `parent_task_id`+`project_id` 를 **한 PATCH 에 같이 보내지 않나** (422)
19. 후행 해제가 **멱등이 아님**(두 번째 404)을 화면이 견디나

## 4. 특히 볼 자리 — 「조용히 통과하는 자리」

- **구획이 이사 가다 사라진 것** — 여섯 덩어리로 재배치하면서 기존 기능이 없어졌나.
  `fe-survey-report.md` §4 의 구획 목록과 **대조해라.** 이것이 이번 판 최대 위험이다
- **`task` prop 과 상세 조회 값이 섞인** 곳 — 하나는 목록 투영이라 값이 없다
- **빈 단언·항상 참인 단언** (앞줄이 `==[]` 인데 뒤에서 포함을 세는 류)
- **폴백이 거절을 삼키는** 곳 — catch 에서 빈 배열로 돌려 「없음」이 되나
- **`api.ts` 밖 fetch**
- **새 DS 부품을 만든** 곳 — 기존 것을 재사용해야 한다
- **`.section-row`·`.material-list` CSS 고침이 다른 화면을 깨뜨렸나** —
  `.section-row` 는 `WorkModals.tsx` 5곳 · `RelationGraphPage.tsx` 1곳이다. 전부 확인해라
- **못 읽는 후행의 `task_id` 가 DOM 에 남아 있나** (`data-*` 속성·key 포함)

## 5. 범위 이탈

- `backend/` 를 건드렸나 (금지였다)
- WORK-007 에 없는 단계를 했나
- 커밋·push 했나 (금지였다)
- 서버·프론트를 띄웠나 / 사용자 포트를 건드렸나 (금지였다)

## 6. 검증 재현

```
make frontend-test · frontend 에서 npx tsc --noEmit
```

- **사용자 포트·프로세스 무접촉** — `8001`·`5176`·`54329`. 죽이거나 재시작 금지
- 전체 스위트는 **시간 의존 불안정**이 알려져 있다(2026-09-24 회고).
  간헐 실패는 **기준선과 분리**해서 적어라 — 같은 테스트를 두 번 돌려 확인해라
- 워커 수치와 다르면 **둘 다** 적어라

## 7. 판정

- **FAIL** — 계약·시안과 다른 것이 돈다
- **WARN** — 물어야 할 만큼 모호하다
- **PASS**

각 지적에 **파일:줄 + 근거**.

## 8. 리포트 형식

```
## 0. 판정 (FAIL n · WARN n)
## 1. 시안 대조표 (§3 여덟 항목)
## 2. 동작 계약 대조표 (§3 아홉~열아홉)
## 3. 구획 이사 대조 — 착수 전 목록과 대조해 «사라진 것»이 있나
## 4. FAIL
## 5. WARN
## 6. 조용히 통과하는 자리 (§4)
## 7. 범위 이탈
## 8. 검증 재현 결과
## 9. 검수 한계
```

## 9. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer FE 검수 완료: FAIL n · WARN n" \
  --body "리포트 경로 / FAIL 요약 / 시안 대조 불충족 / 사라진 구획 / 검증 재현 / 한계"

orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] reviewer FE 검수 완료 — FAIL n · WARN n. review-fe-report.md" --enter
```
