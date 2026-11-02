# [reviewer] 참조 수신함 읽음·프로젝트 선행업무 스펙 검수

너는 **strong-hajin reviewer 워커**다. 역할 문서를 먼저 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md`
- 같은 폴더의 `rules.md`, `skills.md`, `tools.md`, `workflow.md`

검수 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`
코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`는 read-only 참고만 한다.

## 1. 대상

이번 writer dispatch가 수정한 두 파일만 검수한다.
- `para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`

기준은 같은 프로젝트의 baseline·기존 decision/spec, writer brief
`orchestration/work/strong-hajin-work/strong-hajin-work-read-predecessor-spec-brief.md`, 그리고 기존 문서 파이프라인 규칙이다.

## 2. 중점

- CC 참고 업무의 읽음은 `work_request_read_receipts`로 사용자별·멱등·관계 불변인지
- 읽음 필터가 수신함의 reference 갈래에만 적용되고 요청 목록/참조업무 탭과 업무 조회를 숨기지 않는지
- 읽음 명령을 MCP/AX에 노출하지 않는 계약과 표면 일치가 모순 없는지
- parent/reference/predecessor 세 관계가 분리되어 있는지
- 선행 관계의 프로젝트 범위, 다중 선택, 자기참조·중복·순환 방어, finish-to-start 시작 차단이 명확한지
- `시작 전 → 완료` 우회로, 프로젝트 변경, 취소된 선행, 시작 후 선행 재개, 동시 저장의 계약이 명시됐는지
- `preceding_task_ids`와 `task_predecessors` 단일안, 제약, 권한, API/REST/MCP/AX/간트 표면 추적이 구현 가능한지
- 사용자 요구 밖 정책을 임의 확정하지 않았는지, Open Questions가 남아 있는지
- 기존 계약 삭제·조용한 의미 변경·출처 없는 단정이 없는지

## 3. 산출물

유일한 산출물은 다음 하나다.
`orchestration/work/strong-hajin-work/review-read-predecessor-spec-report.md`

판정은 PASS/WARN/FAIL 중 하나로 하고, 모든 지적에 파일:줄·근거·최소 수정 방향을 적는다. 기존 문서의 이번 diff 밖 부채는 별도 분리한다.

## 4. 검증

- `git diff`와 `git status`로 이번 두 파일 외 변경이 없는지 확인
- 문서 파이프라인·frontmatter·관계 링크·중복 여부 확인
- `python3 scripts/lint-pipeline.py --strict`를 실행하되 파일이 없으면 그 사실을 WARN/미실행으로 기록
- 코드 테스트·빌드·DB·UI 실행 금지
- 커밋·push·PR 금지

## 5. 완료 보고

dispatch preamble의 taskId/dispatchId와 코디네이터 핸들을 권위로 삼아 orchestration `worker_done`와 코디 터미널 직접 주입 두 채널로 보고한다. 코디 handle은 `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`다.
