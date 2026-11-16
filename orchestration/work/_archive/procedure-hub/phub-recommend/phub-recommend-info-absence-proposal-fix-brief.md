# [writer] case3 정보 없음 계약 변경안 검수 FAIL 수정

너는 procedure-hub 문서 수정 워커다. Orca dispatch preamble의 Task·Dispatch ID와 완료 보고 명령을 우선한다. 이 브리프 한 장으로 작업한다.

## 1. 먼저 읽을 것

- 역할: `orchestration/roles/procedure-hub/writer/`의 `role.md`, `rules.md`, `skills.md`, `tools.md`, `workflow.md`
- 수정 대상: `orchestration/work/phub-recommend/info-absence-spec-proposal.md`
- 검수: `orchestration/work/phub-recommend/review-info-absence-spec-proposal.md`
- 정본: `orchestration/work/phub-recommend/SPEC-005.md`(0.3.5), `SPEC-006.md`(0.3.8)
- 근거: `reference/2026-10-30-hub-evals/build-out/info-absence-audit/root-cause-next.md`, `direct-fact-worktable.md`, `partial-claims-worktable.md`
- 코드: `~/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend`, `~/orca/workspaces/clinic_chat/hub-evals` (읽기 전용)

## 2. 수정 범위

검수 FAIL F-1/F-2/F-3을 실제 Hub·앱 계약과 맞는 문구로 고친다.

1. pair_check 기본/evidence/all의 실물 응답 차이, `alternatives`와 `pairs_more_n`, 전역 메모 Q139의 접근 공백을 정확히 적는다. 현재 API가 못 주는 대안 출처·생략 쌍 ID는 신규 계약 또는 미해결 결정으로 분리한다.
2. `received_supported`와 미수신/미확정/차단 상태를 분리한다. 근거 없이 `enough`가 열리지 않도록 대상·facet별 종료 조건을 닫는다.
3. 관계 응답이 15KB 원문 예산을 넘을 때의 호출 전후 바이트 귀속, 응답 채택/배제, 인용 자격, 필수 대상 blocked 상태와 부분 답변 문구를 닫는다. 임의로 예산을 늘리지 않는다.
4. WARN W-1~W-4도 가능한 범위에서 명확히 하고, 근거가 없는 제품 정책(안전 추가 페이지 우선순위, 50문항 승격 수치)은 열린 결정으로 유지하되 추천안을 검토 가능하게 적는다.

## 3. 허용 범위와 완료 기준

- 수정 허용: `orchestration/work/phub-recommend/info-absence-spec-proposal.md` 한 파일.
- 공식 SPEC, 외부 코드, DB, 서버, 평가 기록은 수정하지 않는다. 새 평가를 실행하지 않는다.
- 보고 시 검수 항목별 처리 표와 남은 열린 결정을 짧게 요약한다. 문서 안에 뒷받침 없는 해결 주장이나 신규 의료 사실을 넣지 않는다.
- 커밋·push·PR 하지 않는다. 완료 시 dispatch preamble에 따라 `worker_done`을 정확히 한 번 보내고 종료한다.
