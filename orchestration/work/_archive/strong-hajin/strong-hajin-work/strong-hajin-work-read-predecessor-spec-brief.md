# [writer] 참조 수신함 읽음 처리·프로젝트 선행업무 스펙 갱신

너는 **strong-hajin writer 워커**다. 먼저 역할 문서를 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md`
- 같은 폴더의 `rules.md`, `skills.md`, `tools.md`, `workflow.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`
base: `origin/main` → PR 대상 `main` (커밋·push·PR은 코디네이터가 한다)
코드 레포는 read-only다.

## 1. SSOT와 기존 문서

먼저 읽을 것:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/README.md`
- `00-baseline/`, `10-decision/`, `20-spec/` 인덱스와 관련 문서
- `20-spec/spec-001-work-management.md`
- `10-decision/decision-001-work-page.md`
- 기존 v2 관련 결정·스펙과 코디가 확정한 아래 요구

코드 레포는 다음 경로를 read-only로 확인해 현행과 목표의 차이만 기록한다:
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`

## 2. 이번 스펙에 반영할 확정 요구

### A. 참조 업무 수신함 읽음 처리

- CC 참조자에게 들어온 참고 업무는 수신함에 표시한다.
- 참조자가 읽음 버튼을 누르거나 참고 업무 카드를 열면 읽음 처리한다.
- 읽음 처리된 참고 업무는 수신함 조회에서 사라진다.
- 읽은 업무 자체는 `참조 업무` 탭에서 계속 조회된다.
- 읽음 상태는 사용자별이다. 한 사용자가 읽어도 다른 참조자의 수신함에는 남는다.
- 수신함 뱃지는 현재 사용자 기준 미읽음 참고 항목 수를 표시한다.
- 읽음 API는 멱등적이어야 한다.
- CC 관계를 삭제하지 않고 별도 읽음 상태/영수증으로 숨긴다.
- 이번 절의 대상은 CC 참고 업무다. 업무 요청의 수락·거절 흐름을 이 절에 섞지 않는다.
- HTTP와 화면 조회 계약에서 미읽음 필터가 어디에 적용되는지 명시한다. MCP/AX 표면이 같은 inbox projection을 노출하면 함께 추적한다.

### B. 프로젝트 선행업무

- 상위 업무(parent)와 선행업무(predecessor)는 다른 관계다.
- 참고 업무(reference)는 맥락만 제공하며 시작을 막지 않는다.
- 프로젝트를 선택하면 그 프로젝트에 속한 업무 중에서 선행업무를 여러 개 선택할 수 있다.
- 프로젝트가 선택되지 않으면 선행업무 선택은 비활성화하고 프로젝트 선택을 안내한다.
- 자기 자신, 중복 관계, 순환 관계는 허용하지 않는다.
- 기본 의존성은 finish-to-start로 한다. 선택한 선행업무가 모두 완료되지 않으면 후행 업무의 시작 명령을 거부한다.
- 거부 코드는 기존 상태 충돌 계약과 정합되는 단일 코드로 확정하고, 기존 코드에 없는 경우 Open Questions가 아니라 이번 스펙에서 명시할 목표 계약으로 기록한다.
- 간트/타임라인에는 선행→후행 연결을 표시한다.
- 생성·수정 payload에 선행업무 ID 배열을 추가하고, DB 영속화·권한·동시성·순환 검증을 명시한다.
- 테이블/필드명은 현재 코드에 맞춰 단일안을 고른다. 예시 후보를 나열하지 말고 권장안 하나를 계약으로 쓴다.

## 3. 산출물

다음 기존 문서만 수정한다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`

문서에 다음을 포함한다.
- 사용자 결정과 목표 계약을 현행 동작과 분리
- API 요청/응답, 조회 필터, 읽음 멱등성
- 데이터 모델과 유니크/순환 제약
- 권한 및 오류 코드
- 생성·수정·시작·간트 조회의 적용 범위
- HTTP/MCP/AX surface 추적
- 성공·실패 인수조건과 동시성 고려
- 구현 WP에서 BE/FE가 각각 해야 할 일
- 아직 확정하지 않은 사항은 Open Questions로 남김

## 4. 금지

- 코드 수정 금지
- `orchestration/` 파일 수정 금지
- baseline, 다른 제품 문서, index/log 수정 금지
- 커밋·push·PR 금지
- 사용자 요구를 임의로 넓혀 업무 요청 수락·거절 계약을 변경하지 말 것

## 5. 검증

- 문서 파이프라인 규칙 확인
- frontmatter와 관계 링크 확인
- 기존 spec-001의 기존 계약을 조용히 삭제하지 않았는지 diff 확인
- 읽음 필터가 CC 참고 업무와 요청 업무를 혼동하지 않는지 확인
- parent/reference/predecessor를 구분하는 추적표 확인
- `python3 scripts/lint-pipeline.py --strict` 실행
- 변경 파일이 위 두 파일뿐인지 확인

## 6. 완료 보고

커밋·push·PR 없이 변경 파일, 결정사항, 검증 결과, Open Questions를 보고한다. dispatch preamble의 taskId/dispatchId와 코디네이터 핸들을 사용해 orchestration `worker_done`와 코디 터미널 직접 주입 두 채널로 보고한다.

코디네이터 핸들: `term_9de388d5-58b1-4bbe-8864-5e930def648b`
