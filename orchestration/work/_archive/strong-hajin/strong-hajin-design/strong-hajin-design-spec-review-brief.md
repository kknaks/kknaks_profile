# [reviewer] SPEC-007 업무 상세 재설계 — 스펙 검수

너는 **strong-hajin `reviewer` 워커**다. 역할 문서를 먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인` (코디 워크트리)

## 0. 읽기 전용이다

문서를 **고치지 마라.** 산출물은 리포트 한 장이다.

- 쓰기: `orchestration/work/strong-hajin-design/review-spec-007-report.md` ← 이 파일 하나만

## 1. 검수 대상

- `para/projects/summer-star/strong-hajin/00-baseline/baseline-005-task-detail.md`
- `para/projects/summer-star/strong-hajin/10-decision/decision-006-task-detail.md`
- `para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md`

## 2. 무엇에 비추어 보나 — 이 넷이 기준이다

| 기준 | 경로 |
|---|---|
| **확정 시안 (화면의 정본)** | `reference/2026-09-10-sc-meeting/package 2/TaskDetail.html` |
| 조사 — 문서 | `orchestration/work/strong-hajin-design/spec-survey-report.md` |
| 조사 — 서버 | `orchestration/work/strong-hajin-design/be-survey-report.md` |
| 조사 — 화면 | `orchestration/work/strong-hajin-design/fe-survey-report.md` |
| 기존 계약 | `20-spec/spec-001-work-management.md` · `spec-003-task-lifecycle-v2.md` · `spec-005-projects.md` |

## 3. 사용자가 확정한 것 — 스펙이 이것과 다르면 FAIL

1. 네 덩어리 — `업무 메타` · `업무 정보` · `연관 업무` · `자료`
2. 세 덩어리 제목은 같은 레벨
3. `업무 정보` 는 1열 (업무 내용 → 체크리스트)
4. `연관 업무` 2열 짝: 상위\|프로젝트 · 하위\|선행 · 참고\|후행
5. `자료` 2열: 참고 자료 \| **결과 자료** (「산출물」 표기 아님)
6. 목록 3행 기본 + 칸 안 스크롤, 머리는 스크롤 밖 고정
7. `업무 메타` 한 줄 압축
8. **후행은 저장하지 않는다** — `task_predecessors` 역방향 읽기
9. 후행에 필요한 것 셋: 역방향 조회 · `predecessor_task_id` 인덱스 · 응답 필드
10. 못 읽는 후행은 **건수만**
11. **선행=시작 막음 / 하위=완료 막음** — 합치지 않는다
12. `연관 업무` 에 연결 편집 입구, 같은 2열 자리
13. 상위·프로젝트=셀렉터 / 하위·선행·참고=해제+추가 / 후행=해제만
14. 「추가」는 글자 + 파란색
15. **유효성은 서버가 판정** — 화면이 미리 막지 않는다
16. 비공개 후행은 해제 단추 없음
17. 상위 변경을 연다 (`parent_for()` 재사용)
18. **상위 이동으로 하위가 V-8 을 어기면 거절** (EU-8 을 이 범위에서 닫음)
19. 후행 해제는 즉시 반영 (제안 아님)
20. **알림은 범위 밖** — 자리만 표시, 설계 금지

## 4. 특히 볼 자리 — 「조용히 통과하는 자리」

테스트가 초록인데 계약이 깨지는 곳을 따로 본다. 스펙에서는 이런 모양이다.

- **시안에 없는 것을 스펙이 슬쩍 요구**하는 곳. Open Question 없이 새 화면 요소가 들어왔나
- **알림을 설계해 버린** 곳 (§3-20 위반). 「알림을 보낸다」 수준을 넘어 종류·문구·전달을 정했나
- **소급 재배치를 설계한** 곳 (EU-8 을 「거절」이 아닌 다른 것으로 닫았나)
- **선행과 하위를 한 덩어리로 서술**한 문장. 「막힘」을 한 낱말로 뭉갠 자리
- **후행을 저장하는 것처럼** 쓴 문장. 새 표·새 쓰기 경로·양방향 저장을 암시하나
- **권한 필터를 빠뜨린** 후행 서술. 「후행 목록을 낸다」만 있고 못 읽는 것 처리가 없나
- 기존 계약(SPEC-001·003·005)과 충돌하는데 **Open Question 없이 덮어쓴** 자리
- `predecessors` 배선 복구가 **빠진** 곳 — 이게 없으면 화면이 그대로 빈다

## 5. 판정

- **FAIL** — 계약과 다른 것이 돈다 (§3 위반, 시안과 불일치, 기존 계약 무단 변경)
- **WARN** — 물어야 할 만큼 모호하다
- **PASS**

각 지적에 **파일:줄 + 근거**. 근거 없는 지적은 쓰지 마라.

## 6. 리포트 형식

```
# SPEC-007 검수

## 0. 판정 (FAIL n · WARN n · PASS)
## 1. FAIL — 각각 파일:줄 · 무엇이 계약과 다른가 · 근거
## 2. WARN
## 3. 조용히 통과하는 자리 (§4) — 봤고 문제 없으면 그것도 적는다
## 4. 시안 대조표 — §3 스무 항목 각각 충족/불충족
## 5. Open Questions 적절성 — 남겨야 할 것을 정해 버렸거나, 정할 수 있는 것을 남겼나
## 6. 검수 한계
```

## 7. 하지 말 것

- 문서를 고치지 마라. 오타도
- 코드를 읽어 「구현이 안 될 것 같다」로 지적하지 마라 — 여기는 계약 검수다
- 근거 없는 취향 지적 금지

## 8. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer SPEC-007 검수 완료: FAIL n · WARN n" \
  --body "리포트 경로 / FAIL 요약 / 시안 대조 불충족 항목 / 검수 한계"

orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] reviewer SPEC-007 검수 완료 — FAIL n · WARN n. 리포트: review-spec-007-report.md" --enter
```
