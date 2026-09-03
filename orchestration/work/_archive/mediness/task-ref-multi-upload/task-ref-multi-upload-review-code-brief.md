
# [reviewer_code] 검수 — 태스크 참고자료 다중 파일 첨부 (frontend 산출물)

너는 **mediness `reviewer_code` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/buf-fix/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

검수 대상 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-ref-multi-upload`
base: `origin/dev` — **워커는 커밋하지 않았다.** 범위 산정은 `git -C <워크트리> diff origin/dev` + untracked(`git status --short`) 로 한다.

## 1. 무엇을 검수하나

frontend 워커 산출물 — 공용 첨부 폼 `TaskReferenceAdder` 다중 파일 첨부(한 번에 N개 선택 → 순차 업로드). 발주 브리프가 계약의 SoT 다:

- `/Users/kknaks/orca/workspaces/kknaks_profile/buf-fix/orchestration/work/task-ref-multi-upload/task-ref-multi-upload-fe-brief.md`

변경 파일(워커 보고): `front/components/tasks/TaskReferenceList.tsx`(수정) · `front/vitest.config.ts`(include 1행) · `front/__tests__/task-reference-multi-upload.test.tsx`(신규).

## 2. 판정 기준 — 브리프 계약 항목별로 본다

1. **allowed_paths**: 변경이 `front/` 밖으로 나가지 않았나.
2. **API 계약 무변경**: 요청당 `file` 1개 유지, `addTaskReferenceFile`·BFF·백엔드 미변경. 업로드는 순차(병렬 아님).
3. **콜사이트 무변경**: `onAddFile(file, title)` 시그니처와 소비자 4곳(CanonicalTaskDetail·task-kanban·WbsGanttEmbed·TaskDetailRail) 미변경, 루프는 폼 내부.
4. **§4.19.1 폼 한 벌**: 표면(레일 다이얼로그/완료 모달 인라인)별 분기·복제가 생기지 않았나. spec: `git -C /Users/kknaks/git/harness_works/mediness-mediness show origin/mediness:products/mediness/20-spec/spec-154-decision-workflow.md`
5. **건별 가드·부분 실패**: 25MB 초과는 그 파일만 거절, 실패 건만 목록에 남고 성공분 롤백 없음, 재시도 시 성공분 중복 업로드 없음.
6. **제목 축**: 1개면 현행(제목 적용), 2개 이상이면 제목 입력 제거·파일명 사용. 폼 안에 role 선택 컨트롤 없음.
7. **범위 제약 준수**: `uploadPendingTaskReferences`·생성 모달 pending queue·랜딩챗·무관 파일 미변경.
8. **테스트 실효성**: 신규 테스트가 순차성(동시 진행 1건)·순서·건별 거절·부분 실패·제목 분기를 실제로 검증하는지, vitest include 에 등재돼 실제로 도는지.
9. 그 외 코드 결함(로직 오류·상태 누수·접근성 회귀 등) — 근거(파일:줄)와 함께.

## 3. 산출물 — 리포트 1개, 그 외 수정·생성 금지

- **read-only** — 리포 파일을 고치지도 만들지도 마라. 테스트도 돌리지 마라(코디가 이미 8/8 확인).
- 리포트 파일 **1개만** 쓴다: `/Users/kknaks/orca/workspaces/kknaks_profile/buf-fix/orchestration/work/task-ref-multi-upload/review-code-report.md`
- 형식: 판정 **PASS / WARN / FAIL** + 근거 목록(파일:줄 + 위반한 계약 항목 번호). WARN 은 머지 가능하되 알아야 할 것, FAIL 은 재작업 필요.

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_432045fc-607c-4547-b2b7-bc6e8e8436da --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch preamble 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch preamble 에 있다> \
  --subject "reviewer_code 완료: <판정> — <한 줄>" \
  --body "판정(PASS/WARN/FAIL) / 위반·주의 목록(파일:줄) / 리포트 경로"

# (2) 직접 주입
orca terminal send --terminal term_432045fc-607c-4547-b2b7-bc6e8e8436da \
  --text "[worker_done] reviewer_code 완료 — <판정> <한 줄>. 상세는 인박스." --enter
```
