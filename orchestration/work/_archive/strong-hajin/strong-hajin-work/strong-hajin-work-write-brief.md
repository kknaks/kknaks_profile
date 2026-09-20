
# [writer] 업무 페이지 착수 — #7 요구 대조 및 개인 프로젝트 업무 스펙

너는 **strong-hajin `writer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디와 같은 워크트리에서 직렬로 작업한다. 코드 레포는 읽기 전용이다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/source-issue-7.md` — 2026-09-15 조회한 변경 이슈 원문 전체.
- 사용자 지시: strong_hajin을 개인 프로젝트로 혼자 이어간다. 업무 페이지를 먼저 만들고 #7을 반영한다. 개발 주체 변경이지 제품을 1인 전용으로 줄이라는 요구가 아니다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/para.md`, `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/project.md` 및 `templates/projects/`의 해당 단계 양식.
- 기대는 개념: 해당 없음. 이번 작업은 사용자 결정과 원문 계약 정렬이며 새 기술적 결정을 발명하지 않는다.

## 2. 배경 / 무엇을 바꾸나

개인 코드 레포 `/Users/kknaks/git/toy_pr2/Strong_hajin`를 대상으로 한다. 회사 레포에는 변경을 남기지 않는다. 개인 문서 디렉토리는 현재 없으므로 업무 범위에 필요한 baseline·decision·spec을 새 양식으로 작성한다. 원문 회사 기획 전체를 그대로 복사하지 말고 필요한 계약과 출처 revision을 연결한다.
기존 MyWorkPage를 확인한 뒤 W1 생성/타인 요청 즉시 배정, W2 완료/승인/목록을 중심으로 업무 페이지 계약을 작성한다. 이번 발주는 스펙 단계까지만이다. 검수 뒤 WP를 별도 발주하고 사용자 리뷰 뒤 코드를 발주한다.

## 3. 계약

- 본인 명시적 생성, 일반 구성원의 허용된 타인 요청 즉시 Task/활성 담당 생성. 신규 수행자 수락 gate 없음. 기존 업무 재배정 권한과 구분.
- 완료 명령 성공 시 done, 승인자 0..1명, 기존 TaskDelivery/ActionItem 재사용. 현재 유효한 미결 승인만 승인 대기 표시. 승인 시 done 유지, 보완 시 in_progress, 재제출 새 회차. completion_submitted 신규 흐름 제거. AI 실행 확인 유지.
- 업무 페이지의 내 업무·보낸 업무·완료 업무·답하면 끝나는 목록, 상세·생성·완료·문의·기록·자료의 화면과 API 계약 연결. 실제 API/필드/권한 근거 파일:줄과 현행/목표 차이를 명시한다.
- D2는 미결로 유지. D4 기존 데이터 전환/호환 제외. 회의/외부 연동은 연결 영향과 후속 요구로 추적하며 이번 업무 스펙에서 구현하지 않는다.
- PA-01~07은 누락 없이 원문 요구→기존 코드 증거→계약/미결→적용 차수 제안으로 추적. PA-08~14와 M1/X1은 전체 이슈의 잔여 추적을 남긴다. 미결을 확정으로 바꾸거나 기존 충족을 추정하지 않는다.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/git/toy_pr2/Strong_hajin/README.md`, `/Users/kknaks/git/toy_pr2/Strong_hajin/docs/domain-model.md` — 현행 설명과 실제 코드 비교.
- `/Users/kknaks/git/toy_pr2/Strong_hajin/frontend/src/features/work/MyWorkPage.tsx`, `WorkViews.tsx`, `WorkModals.tsx`, 같은 폴더 테스트 — 업무 화면.
- `/Users/kknaks/git/toy_pr2/Strong_hajin/frontend/src/lib/api.ts`, `viewModels.ts` — API와 화면 투영.
- `/Users/kknaks/git/toy_pr2/Strong_hajin/backend/src/ax_workspace/modules/`의 tasks/work_requests/action_items 관련 실제 경로를 rg로 찾아 읽는다. HTTP·MCP·AX·seed·권한·멱등성·테스트 surface를 모두 열거한다.
- 이슈의 고정 revision 링크 기획/SPEC을 gh로 read-only 조회하고 최신 원문과 다르면 날짜와 근거를 적는다. 업무와 관계없는 최신 회의 변경을 #7의 오래된 표현으로 되돌리지 않는다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-002-action-item-review.md`

index·log·발주 문서·회사 원문·코드는 수정 금지. 완료 보고에 추적표와 코드 영향 범위를 포함하고 spec의 검증 절에도 근거를 남긴다. 추가 파일이 꼭 필요하면 먼저 코디에게 알려라.

## 6. 구현 단계

1. 원문과 코드 revision을 확인하고 BASE에 입력/출처, DEC에 사용자 확정 사항과 미결을 구분한다. 모든 신규 문서는 검수 전 초안 상태다.
2. W1/W2를 spec으로 구체화한다. 서버 상태와 화면 표시를 구분하고 권한/오류/동시성/멱등성 및 성공·실패 인수조건을 작성한다.
3. 문서 앞뒤 요구 추적을 점검하고 다음 WP에서 다룰 surface와 미결을 완료 보고한다. WP는 아직 쓰지 않는다.

## 7. 범위 제약 — 하지 말 것

- 코드 구현, 회사 레포 변경, commit/push/PR, DB reset, 실제 메시지/예약, 배포 금지.
- 단독 개발을 이유로 조직·타인 요청·승인을 삭제하지 않는다. 디자인은 기존 부품/시안 근거를 확인하고 없는 부분은 질문으로 남긴다.
- 역할 문서의 오래된 경로/양식 설명과 충돌하면 이 브리프 및 현재 para/projects/project.md를 따른다. 새 기획 전체 이관은 하지 않는다.

## 8. 검증

산출물은 지정한 네 파일만. frontmatter/관계 링크/출처 revision과 W1/W2·PA 추적 누락을 확인한다. 미결을 임의 결정하지 않는다. 코드 실행 테스트는 하지 않는다.
- 통과할 때까지 문서를 고친다. 못 고치면 근거와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_6871326a-9562-4fdd-b810-b485449ae124 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
