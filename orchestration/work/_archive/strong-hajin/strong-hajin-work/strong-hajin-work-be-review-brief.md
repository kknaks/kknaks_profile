# [reviewer] WORK-003 BE API gap read-only 검수

## 대상

- 코드 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
- 기준: `origin/main`과 현재 워크트리 diff. 기존 WORK-003의 다른 미커밋 변경은 이번 구현의 결과로 오인하지 말고 별도 기존 부채로 분리한다.
- 구현 보고서: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-Strong-hajin-strong-hajin-work/a5781f09-e480-462f-b8d4-bd950e5d165e/scratchpad/work003-request-materials-be-report.md`
- SSOT: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`, `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-003-inbox-predecessor-and-create-frame.md`

## 모드와 금지

- backend read-only 리뷰다. 코드·문서·테스트를 수정하지 않는다.
- 테스트·빌드·DB·E2E를 실행하지 않는다. 소스와 diff만 읽는다.
- 유일한 산출물은 `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-be-api-gap-report.md` 한 파일이다.
- 커밋·push·PR·stash·checkout·reset 금지.

## 검수 항목

1. 요청 자료 5개 HTTP route가 기존 attachments/attachment_bindings를 재사용하고 `work_request` context를 일관되게 쓰는가. 새 테이블·임의 생성 payload·댓글/evidence 우회가 없는가.
2. 요청자만 attach/detach, 참여자만 read/download, pending/negotiating 외 상태는 변경 거부라는 권한·상태 경계가 실제 코드에 있는가.
3. 수락 시 원본 request binding 보존 + 같은 attachment의 task binding 추가가 transaction/멱등적으로 연결되는가.
4. 요청 projection의 preceding/reference/materials가 생성·발송·상세·목록 경로에서 shape을 깨지 않는가.
5. 회의 승격 직행/action 경로가 start_date·cc_member_ids·approver_id·reference_task_ids·project_id·parent_task_id·preceding_task_ids를 빠뜨리지 않는가.
6. CC 후보 capability 완화가 task.self_manage 범위로 제한되고 assignee 후보 권한·조직 외 노출을 넓히지 않는가.
7. FastAPI/SQLAlchemy 경계, 예외 매핑, operation inventory, allowed paths, 테스트 존재 여부를 rules.md 체크리스트로 확인한다.
8. 워커가 보고한 checkout 사고와 inventory 복구는 PASS 근거가 아니라 WARN/FAIL 후보로 사실만 기록한다. 복구 여부는 diff/현재 파일로 확인한다.

## 판정

- 계약과 다른 동작·allowed path 이탈·권한 우회·inventory drift는 FAIL.
- 근거가 있는 잔여 위험·검증 한계는 WARN.
- 각 항목은 반드시 `파일:줄` 근거를 쓴다.

## 완료 보고

완료 시 현재 dispatch preamble의 taskId/dispatchId를 사용해 `worker_done`을 인박스와 코디네이터 터미널 양쪽에 보낸다. 코디네이터 handle은 `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`다. 테스트를 실행하지 않았다는 점과 PASS/WARN/FAIL 판정을 보고서에 명시한다.
