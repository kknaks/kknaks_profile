
# [frontend] 태스크 참고자료 다중 파일 첨부 — 한 번에 N개 선택·순차 업로드

너는 **mediness `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/buf-fix/orchestration/roles/mediness/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-ref-multi-upload`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

이 워크트리는 너 혼자 쓴다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/git/harness_works/mediness-mediness/products/mediness/20-spec/spec-154-decision-workflow.md` ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
  ⚠ 이 경로는 사용자의 더티 체크아웃이라 디스크가 낡았을 수 있다 — 반드시 `git -C /Users/kknaks/git/harness_works/mediness-mediness show origin/mediness:products/mediness/20-spec/spec-154-decision-workflow.md` 로 읽어라. 특히:
  - **§4.19.1 「자료 추가 = 자리에 따라 두 표면, 폼 본체는 한 벌」(사용자 확정)** — 레일 발 추가는 중앙 다이얼로그, 완료 모달 안에서만 인라인 행. **갈리는 것은 껍데기뿐, 폼 본체는 한 컴포넌트.** 크기 상한·거절 문구·role 기본값이 자리마다 다르게 굳으면 안 된다.
  - §4.8 — 첨부 계약: 파일당 25MB, **개수 제한은 없다.**

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

prod 실사용 반려: 태스크 완료 시 산출물 파일 3개를 첨부하려면 **1개 올리고 → 업로드 끝나길 기다리고 → 다시 1개** 를 반복해야 한다. 원인은 공용 첨부 폼 `TaskReferenceAdder` 가 모든 층에서 단일 파일이기 때문 — `<input type="file">` 에 `multiple` 없음 → `useState<File | null>` → 요청당 파일 1개.

목표: **파일 선택기에서 한 번에 N개 선택 → 순차 업로드 → 건별 성공/실패 보고.** 백엔드는 이미 「개수 제한 없다」가 계약이고 요청당 1파일 순차 N요청은 계약에 맞다 — **백엔드·API 무변경.**

(참고: 같은 버그 신고의 413(1.4MB) 건은 인그레스 어노테이션 문제로 **별도 인프라 PR 로 이미 처리됐다** — 네 범위 아님.)

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

- API 무변경: `POST /api/ax/tasks/{task_id}/references`, `FormData` 필드 `file` **1개/요청** 유지. 다중은 **순차 루프로 N요청** (병렬 금지 — 기존 코드베이스 패턴이 순차+건별 실패 수집이다).
- 파일당 25MB 클라이언트 가드(`TASK_REFERENCE_MAX_BYTES`) 유지 — 초과 파일만 건별로 거절하고(기존 문구 톤 유지) 나머지는 진행한다.
- `role` 은 폼이 선 자리가 정한다(현행 그대로) — 폼 안에 선택 컨트롤을 만들지 마라.

## 4. 먼저 읽을 핵심 파일

- `front/components/tasks/TaskReferenceList.tsx:270,281,382-399` — 폼 본체 `TaskReferenceAdder`. `onAddFile: (file, title) => Promise<void>` 콜백, `useState<File | null>`, `multiple` 없는 input, 25MB 가드. **수정의 중심.**
- `front/lib/tasks/task-references.ts:104,147-157,196-226` — `TASK_REFERENCE_MAX_BYTES`, `addTaskReferenceFile`(1파일 1요청), `uploadPendingTaskReferences`(순차 루프 + 건별 실패 수집 — **패턴 참조용, 리팩터링 금지**).
- `front/components/tasks/TaskCompletionModal.tsx:211-215` — 완료 모달이 `role="deliverable"` 로 폼을 인라인 렌더.
- 콜사이트 4곳(시그니처 소비자): `front/components/tasks/detail/CanonicalTaskDetail.tsx:550-557` · `front/app/(authenticated)/ax/tasks/task-kanban.tsx:1448` · `front/components/pipeline/WbsGanttEmbed.tsx:1743` · `front/components/tasks/detail/TaskDetailRail.tsx:184-186`
- 다중 첨부 선례: `front/components/landing-chat/Composer.tsx:201-212`(`multiple` + `Array.from`), 테스트 `front/__tests__/wp130-composer-multi-attach.test.tsx`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `front/`

## 6. 구현 단계

1. `TaskReferenceAdder`: input 에 `multiple` 추가, 상태를 `File[]` 로. 선택 시 파일별 25MB 가드 — 초과분만 건별 거절 메시지, 통과분은 목록 유지. 선택된 파일 목록을 UI 에 보여준다(파일명·개별 제거 정도면 충분).
2. 제목(표시 이름) 처리: **1개 선택이면 현행 그대로**(제목 입력 적용), **2개 이상이면 제목 입력을 숨기거나 비활성화하고 파일명을 그대로 쓴다.** 파일별 제목 입력 UI 를 새로 설계하지 마라.
3. 업로드: 폼 내부에서 **파일별로 `onAddFile` 을 순차 호출**한다 — 콜백 시그니처와 콜사이트 4곳은 무변경. 건별 실패를 수집해 실패 파일명+사유를 폼에 표시하고, 성공분은 정상 반영되게 둔다(전체 롤백 없음).
4. **폼 한 벌 원칙(§4.19.1) 유지** — 레일 다이얼로그/완료 모달 표면별 분기·복제 금지. 한 컴포넌트 수정으로 양쪽에 적용돼야 한다.
5. 테스트: `wp130-composer-multi-attach.test.tsx` 패턴으로 폼 다중 첨부 테스트 파일 1개 추가(다중 선택 → 순차 호출 횟수·순서, 초과 파일 건별 거절, 부분 실패 표시). 실행은 **그 파일만.**

## 7. 범위 제약 — 하지 말 것

- 백엔드·BFF·API 계약 변경 금지 (`back/` 은 allowed_paths 밖이기도 하다).
- 병렬 업로드 금지 — 순차.
- `uploadPendingTaskReferences`·생성 모달 pending queue·랜딩챗 리팩터링 금지. 패턴만 빌린다.
- 콜사이트 4곳의 시그니처 변경 금지(루프는 폼 내부).
- 무관 파일 정리·포맷·리팩터링 금지.

## 8. 검증

```
cd front && npx tsc --noEmit (네가 만진 파일 0 에러) + prettier --check <네가 만진 파일만>. 전체 빌드·전체 포맷 검사 금지 — 사용자 방침. 검증은 1회만
```

- 추가로 §6-5 의 새 테스트 파일 1개만 실행해 통과시킨다.
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_432045fc-607c-4547-b2b7-bc6e8e8436da --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_432045fc-607c-4547-b2b7-bc6e8e8436da \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter

# 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
#   orca terminal send --terminal term_432045fc-607c-4547-b2b7-bc6e8e8436da --text "[질문] frontend: <질문>" --enter
#   (orca orchestration ask 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
```
