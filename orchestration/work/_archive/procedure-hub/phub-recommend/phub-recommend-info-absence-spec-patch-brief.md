# [writer] case3 정보 없음 정본 SPEC 개정

너는 procedure-hub 문서 워커다. Orca dispatch preamble의 Task·Dispatch ID와 완료 보고 명령을 우선한다. 이 브리프 한 장으로 작업한다.

## 1. 먼저 읽을 것

- 역할: `orchestration/roles/procedure-hub/writer/`의 `role.md`, `rules.md`, `skills.md`, `tools.md`, `workflow.md`
- 변경 기준: `orchestration/work/phub-recommend/info-absence-spec-proposal.md` 및 `review-info-absence-spec-proposal-v2.md`
- 정본: `orchestration/work/phub-recommend/SPEC-005.md`(0.3.5), `SPEC-006.md`(0.3.8)
- 근거: `info-absence-remediation-plan.md`, ignored audit의 `root-cause-next.md`, `direct-fact-worktable.md`, `partial-claims-worktable.md`, `_RESUME.md`의 11-01~02 결정
- 코드 확인은 읽기 전용: `~/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend`, `~/orca/workspaces/clinic_chat/hub-evals`

## 2. 작업

검수된 제안 중 근거가 닫힌 부분을 정본 SPEC-005/006에 반영하고, 미결정은 OQ/결정표에 명확히 남긴다. 기존 조항과 충돌하는 문구를 정리하고 변경 절·버전·의존성을 기록한다.

- 005: 관계 fact의 현재 T4 접근 한계, 필요한 선택 조회 계약과 claim/대안별 출처·생략 쌍 식별, Q139 전역 메모 경로를 구현 가능한 필드·상태로 정의한다. 1쪽 12줄/page/more 정렬은 유지한다. 페이지 비용 metadata 추가 여부는 기존 API 재사용을 우선 검토하고, 선택에 따른 006 비용·timeout 계약을 맞춘다.
- 006: node/section/page 수신 상태, 중복 ID와 실제 응답 바이트, 명시 대상 seed와 `received_supported`/unresolved/blocked/enough, 안전 8KB 우선, 관계 조회 예산 초과 처리, 부분 답변 범위를 필드·전이·종료 조건까지 정의한다.
- 50문항 관문은 고정 분모·안전 회귀·직접 근거 부재 주장 감소를 검증 대상으로 명시한다. 사용자 승인되지 않은 TTFT 허용 악화 폭이나 개선 건수 문턱을 임의로 확정하지 않는다. 기존 W-4 사용자 결정 기록과 정본의 열린 표기를 대조해 정리한다.
- 현 코드와 다른 신규 계약은 **현 구현 아님**이라고 분명히 적고, WORK에서 구현해야 할 범위를 구분한다. 의료 사실·원천 문장을 새로 만들지 않는다.

## 3. 허용 범위와 검증

- 수정 허용: `orchestration/work/phub-recommend/SPEC-005.md`, `SPEC-006.md` 두 파일만. 검수 보고서·제안서·외부 코드·DB·서버·평가 기록은 수정하지 않는다.
- 두 정본의 기존 결정(허브 결정론, Jev 노드 선택, 섹션 양 규칙, 4걸음·20/8/15KB, 안전 사실, D-13b 충돌 해결)을 유지한다.
- 변경 절과 제안·재검수 지적을 1:1 대조하고, 새 OQ·WORK 의존과 수용 사례를 보고한다. 커밋·push·PR을 하지 않는다.
- 완료 시 dispatch preamble에 따라 `worker_done`을 정확히 한 번 보내고 종료한다.
