# [reviewer] 최종 업무/요청 프레임 + 읽음·선행업무 SPEC/WP 통합 검수

너는 strong-hajin reviewer 워커다. 먼저 역할 문서를 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md`
- 같은 폴더 `rules.md`, `skills.md`, `tools.md`, `workflow.md`

검수 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`
코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`는 read-only 참고만 한다.

## 대상

writer가 이번 dispatch에서 만든 세 파일만 검수한다.
- `para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `para/projects/summer-star/strong-hajin/30-work/work-003-inbox-predecessor-and-create-frame.md`

기준은 프로젝트 baseline·기존 DEC/SPEC/WP, writer brief `strong-hajin-work-spec-wp-brief.md`, 문서 pipeline 규칙이다.
유일한 산출물은 `orchestration/work/strong-hajin-work/review-spec-wp-report.md` 하나다.

## 검수 중점

1. 최종 모달 프레임이 정확히 계약됐는가: 업무/요청 제목, 기본 정보 필드, 좌측 필수/선택 탭, 상위·프로젝트·선행, 자료, 체크리스트, 참고 업무 UI 제거.
2. 업무 갈래 담당자 숨김·현재 사용자 서버 기록, 요청 갈래 담당자 1명, 참조자 다수·결재자 1명의 payload/권한 정합성.
3. CC 읽음 영수증은 사용자별·멱등·관계 불변이고, 수신함 reference 필터에만 적용되며 참조 업무/업무 조회/요청 결정 흐름을 섞지 않는가.
4. 선행업무가 parent/reference와 분리되고 같은 프로젝트·복수·자기참조/중복/순환·프로젝트 변경·finish-to-start 시작 게이트·시작 전 완료 우회 차단·취소 선행·동시성을 모두 계약하는가.
5. `approver_id`, `preceding_task_ids`, `project_id`, `parent_task_id`, `cc_member_ids`, `checklist`, 일정 필드가 업무/요청 공통 payload와 요청 전용 필드로 정확히 분리됐는가.
6. REST/MCP/AX/회의 후속 승격 surface, 권한, 오류 코드, 인수조건과 BE/FE WP 분담이 구현 가능하게 연결됐는가.
7. OQ-M(요청 확인자 정합성), OQ-N(결재자/승인자 명칭), OQ-L 등 미결을 임의 확정하지 않았는가. gate로 표시된 조각과 나머지 착수 가능 범위가 분리됐는가.
8. 기존 D-1~D-20 및 기존 계약을 삭제·약화하지 않았는가. WP가 테스트·migration·allowed paths·동시성 검증을 포함하는가.
9. allowed_paths 밖 변경, frontmatter·링크·문서 자리·중복·출처 문제.

## 검증

- `git diff`와 `git status --porcelain`로 변경 범위를 확인한다(신규 파일 포함).
- `python3 scripts/lint-pipeline.py --strict` 실행. 파일 자체가 없으면 실행 불가를 WARN으로 기록한다.
- 코드 테스트·빌드·DB·브라우저 실행 금지.

## 판정/보고

리포트에 PASS/WARN/FAIL을 하나로 판정한다. 모든 지적은 파일:줄, 근거, 최소 수정 방향을 쓴다. 기존 diff 밖 부채는 별도 분리한다. FAIL이면 코드 발주를 막고 writer 수정 재발주 대상과 이유를 적는다.

## 완료 보고

dispatch preamble의 taskId/dispatchId와 코디네이터 핸들을 사용해 worker_done 두 채널로 보고한다. 코디네이터 핸들: `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`.
