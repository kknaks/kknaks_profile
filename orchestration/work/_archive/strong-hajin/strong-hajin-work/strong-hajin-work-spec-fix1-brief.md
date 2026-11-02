# [writer] 최종 업무/요청 생성 모달 프레임을 SPEC-001에 반영

너는 strong-hajin writer 워커다. 역할 문서와 기존 SSOT를 먼저 읽는다:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md`
- 같은 폴더의 `rules.md`, `skills.md`, `tools.md`, `workflow.md`
- `para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`
코드 레포는 read-only. 커밋·push·PR 금지.

## 목적

직전 SPEC-001 v0.3.0에 남은 기존 생성창 문구를 사용자가 확정한 최종 UI 프레임으로 정정한다. 코드 구현은 하지 않는다. 두 문서만 수정한다.

## 확정 계약

상단 생성 갈래는 하나의 모달 안에 유지한다.
- `업무` 선택: 모달 제목 `새 업무 추가`
- `요청` 선택: 모달 제목 `새 업무 요청`
- 상단 `업무 | 요청` 토글은 유지한다.

왼쪽 탭은 두 갈래가 공유한다.
- `필수 > 기본 정보`
- `선택 > 체크리스트 | 업무 연결 | 자료`

`업무` 기본 정보:
- 업무 제목
- 시작일 | 마감일
- 업무 내용
- 참조자(여러 명) | 결재자(한 명)
- 담당자는 현재 사용자가 고정이므로 UI에서 고르지 않는다. 서버에는 현재 사용자를 담당자로 기록한다.

`요청` 기본 정보:
- 요청할 업무 제목
- 시작일 | 희망 기한
- 담당자(한 명)
- 요청 내용
- 참조자(여러 명) | 결재자(한 명)

선택 탭:
- 체크리스트: 단계 추가·삭제
- 업무 연결: 상위 업무(단일 선택) | 프로젝트(단일 선택) | 선행 업무(프로젝트 업무 중 복수 선택)
- 프로젝트가 없으면 선행 업무 선택은 비활성화
- 자료: 생성 시 첨부할 파일
- 참고 업무 연결 UI는 제거한다. 참조자(CC)와 참고 업무는 다른 개념이다.

업무와 요청은 공통 업무 payload를 공유한다. 요청만 `assignee_id` 등 요청 전용 필드를 추가한다. 제목/내용/일정/CC/결재자/연결관계의 API 필드와 UI 라벨이 어긋나지 않게 문서화한다. 결재자·선행 업무의 구현 단계가 아직 코드와 다르면 현행/목표와 WP 경계를 분리해 적고, 이미 확정한 선행업무 계약을 되돌리지 않는다.

## 수정 범위

- `para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`

기존 D-1~D-20과 읽음·선행 계약을 삭제하거나 약화하지 말 것. 모순되는 예전 문구(예: “체크리스트 칸이 없다”, 업무/요청별 공통 프레임이 아닌 생성창 서술)는 최종 계약에 맞춰 갱신하고 변경 근거를 남긴다. 문서 버전을 올린다.

## 검증

- 두 파일 외 변경 금지
- diff에서 기존 계약 삭제·단언 약화 0건
- 기본 정보/선택 탭/업무·요청 차이를 한 곳에서 추적
- frontmatter·관계 링크 확인
- `python3 scripts/lint-pipeline.py --strict` 실행 시 파일 부재는 보고

## 완료 보고

dispatch preamble의 taskId/dispatchId와 코디네이터 핸들을 사용해 worker_done 2채널로 보고한다. 코디네이터 핸들: `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`.
