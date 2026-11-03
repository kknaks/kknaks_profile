# [writer] case3 정보 없음 WORK-011/012 계획

너는 procedure-hub 문서 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다. 이 브리프 한 장으로 작업한다.

## 읽을 것

- 역할: `orchestration/roles/procedure-hub/writer/`의 역할 문서
- 정본: `orchestration/work/phub-recommend/SPEC-005.md` 0.3.9, `SPEC-006.md` 0.3.9
- 검수: `review-info-absence-spec005006-v2.md`(FAIL 0 · WARN 3), `review-info-absence-spec005006.md`(1차 FAIL 기록)
- 근거: `info-absence-remediation-plan.md`, ignored audit `root-cause-next.md`, `direct-fact-worktable.md`, `partial-claims-worktable.md`
- 양식·전례: `templates/orchestration/` 및 `orchestration/work/phub-recommend/WORK-009.md`, `WORK-010.md`
- 코드 읽기 전용: `~/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend` HEAD 2edc190, `~/orca/workspaces/clinic_chat/hub-evals` HEAD 078ac99

## 작업

두 레포의 의존이 보이는 구현 계획을 작성한다.

- `WORK-011.md`: Hub의 선택 관계 사실 조회·전역 메모 접근 계약, 현재 T4 반환 한계와 새 schema/상한, 결정론 회귀, 골드 빌드/서버 갱신 조건. 005 §5-5·§5-16·§6-9를 근거로 단계·코드 표면·검증·끝 조건을 적는다. 기존 page≥1/12줄은 보존한다.
- `WORK-012.md`: 앱 case3의 뒤 페이지, 명시 대상 queue/resolve, enough/blocked 상태, 안전 8KB와 일반 20KB 및 원문 15KB, 관계 호출 어댑터, 부분 답변, trace·개별 재생·고정 50 검증. 006 §3-4·§4·§7을 근거로 단계·코드 표면·검증·끝 조건을 적는다.
- Hub 계약이 먼저 닫혀야 앱 관계 어댑터를 구현한다. 앱 페이지 수집은 기존 Hub page 계약을 활용할 수 있으나 서버 혼합 실행 중 측정 금지. 코드 구현은 WORK 사용자 리뷰 후에만 발주한다.
- 사용자 결정을 요구하는 안전 추가 페이지 우선순위/예산 전용, retrieval timeout, 50문항 승격 문턱은 **추천값과 영향, 결정 시점**을 구체적으로 표시하되 승인되지 않은 값을 코드 요구로 확정하지 않는다. WORK 안에 결정 전 진행 가능한 WP와 결정 뒤 WP를 분리한다.

## 허용 범위와 검증

- 생성 허용: `orchestration/work/phub-recommend/WORK-011.md`, `WORK-012.md` 두 파일만.
- 외부 코드·서버·DB·평가 기록·SPEC은 수정하지 않는다. 새 평가를 실행하지 않는다.
- SPEC 절 ↔ WP 단계 ↔ 검증 명령/증거 ↔ 코드 레포/허용 경로의 연결을 확인한다. 기존 사용자 포트·`procedure-*` 컨테이너를 건드리지 않는다. 원장 인용을 public 문서에 복사하지 않는다.
- 커밋·push·PR 하지 않는다. 완료 시 dispatch preamble에 따라 `worker_done`을 정확히 한 번 보내고 종료한다.
