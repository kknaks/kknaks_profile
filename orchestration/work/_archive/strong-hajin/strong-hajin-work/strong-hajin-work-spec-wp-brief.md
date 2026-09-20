# [writer] 최종 업무/요청 프레임 + 참조 읽음·선행업무 SPEC/WP 통합 작성

너는 strong-hajin writer 워커다. 역할 문서와 기존 SSOT를 먼저 읽는다:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md`
- 같은 폴더 `rules.md`, `skills.md`, `tools.md`, `workflow.md`
- `para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `para/projects/summer-star/strong-hajin/30-work/work-001-task-creation.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`
코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`는 read-only. 커밋·push·PR 금지.

## 목표

사용자가 확정한 최종 업무 생성 프레임과 새 참조 읽음·프로젝트 선행업무 기능을 SPEC과 WP에 함께 반영한다. SPEC과 WP를 별도 워커로 쪼개지 않는다.

## 확정 UI/계약

하나의 모달 안에 상단 `업무 | 요청` 토글을 유지한다.
- 업무 선택: 제목 `새 업무 추가`
- 요청 선택: 제목 `새 업무 요청`

좌측 탭:
- 필수: `기본 정보`
- 선택: `체크리스트`, `업무 연결`, `자료`

업무 기본 정보:
- 업무 제목
- 시작일 | 마감일
- 업무 내용
- 참조자(여러 명) | 결재자(한 명)
- 담당자는 현재 사용자 고정이라 UI에서 선택하지 않고 서버가 현재 사용자를 담당자로 기록

요청 기본 정보:
- 요청할 업무 제목
- 시작일 | 희망 기한
- 담당자(한 명)
- 요청 내용
- 참조자(여러 명) | 결재자(한 명)

업무 연결:
- 상위 업무: 단일 선택
- 프로젝트: 단일 선택
- 선행 업무: 선택 프로젝트의 업무 중 복수 선택
- 프로젝트가 없으면 선행 업무 비활성화
- 참고 업무 연결 UI는 제거. 참조자(CC)와 참고 업무는 다른 개념

참조 읽음:
- CC 참조 업무만 읽음 처리 대상
- 사용자별 `work_request_read_receipts`와 `(work_request_id, member_id)` 유니크
- 읽음 API는 멱등, CC 관계·request version 불변
- 읽음 후 수신함 reference 갈래와 뱃지에서만 제외
- 참조 업무 탭과 업무 조회에는 필터 없음
- 읽음 명령은 HTTP에만 두고 MCP/AX에는 명령을 노출하지 않음. MCP/AX 조회 projection은 동일
- 업무 요청 pending/negotiating 수락·거절 흐름은 변경하지 않음

선행 업무:
- `preceding_task_ids`, `task_predecessors`
- 같은 프로젝트, 복수 선택, 자기참조·중복·순환 금지
- finish-to-start; 미완료 선행이면 `start`와 `시작 전→완료`를 `WORK_PREDECESSORS_UNFINISHED` 409로 거부
- 차단 선행 이름 응답, 취소된 선행은 차단하지 않음
- 선행이 남은 업무의 프로젝트 변경 거부
- 시작 후 선행 재개가 후행 상태를 되돌리지는 않음
- 프로젝트 상세 업무 줄에서 선행 배열을 내려 간트가 새 조회 없이 그림

## 산출물/허용 파일

- `para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `para/projects/summer-star/strong-hajin/30-work/work-003-inbox-predecessor-and-create-frame.md`

SPEC에는 API·데이터·권한·동시성·표면 일치·인수조건을 적고, WP에는 BE/FE 분담을 적는다.
WP 분담은 다음을 포함한다.

BE: 읽음 영수증·읽음 API·수신함 필터·뱃지 projection·결재자 저장/조회·선행 테이블/제약·생성/수정 payload·순환/프로젝트 검증·시작 게이트·REST/MCP/AX projection·unit/contract/PostgreSQL 회귀.

FE: 업무/요청 최종 모달 레이아웃·조건부 필드·참조자/결재자 입력·상위/프로젝트/선행 선택·프로젝트 후보 필터·체크리스트/자료 탭·참조 읽음 버튼과 수신함 제거·참조 업무 유지·API 연결·FE/브라우저 회귀.

각 작업의 allowed paths, 의존성, 완료 인수조건, 검증 명령을 WP에 명시한다. BE와 FE 구현은 WP 검수 후 병렬 발주한다.

기존 D-1~D-20 및 읽음·선행 계약을 삭제·약화하지 않는다. 기존 문서의 “체크리스트 없음” 등 이번 확정 프레임과 충돌하는 문구는 정정한다. 새 결정을 임의로 만들지 말고 미정은 Open Questions로 남긴다.

## 검증

- 변경 파일이 위 세 파일뿐인지 확인
- 기존 계약 삭제·약화 0건
- frontmatter·관계 링크·문서 파이프라인 확인
- `python3 scripts/lint-pipeline.py --strict` 실행. 파일 부재 시 보고
- 코드·DB·테스트·UI 실행 금지

## 완료 보고

dispatch preamble의 taskId/dispatchId와 코디네이터 핸들을 사용해 worker_done 두 채널로 보고한다. 코디네이터 핸들: `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`.
