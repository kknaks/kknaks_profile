# [writer] case3 걷기 수집·전달 분리 계약 개정

너는 이 레포의 문서 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다. 이 브리프 한 장으로 작업한다.

## 읽을 것

- `orchestration/roles/procedure-hub/writer/` 역할 문서와 루트 `AGENTS.md`, `orchestration/runbook.md`
- `orchestration/work/phub-recommend/SPEC-006.md` 0.3.9, `WORK-012.md`, `SPEC-005.md` 0.3.9, `WORK-011.md`
- `orchestration/work/phub-recommend/review-info-absence-work011012.md`, `info-absence-remediation-plan.md`
- `reference/2026-10-30-hub-evals/HANDOFF.md` §3~4 (특히 안전 실패 28 중 25가 8KB에서 잘림)
- 앱 코드 읽기만: `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals/clinic_chat/cases/case3.py`와 `config.py`

## 사용자 정정과 작업

사용자는 분명히 말했다: 질문에 필요한 정보가 많으면 그래프를 더 탐색해야 한다. 여러 번 탐색해 노드/이웃/다음 페이지의 사실을 수집하고, 그중 질문에 필요한 사실만 Claude에 넘긴다. 고정 바이트 한도 때문에 탐색이 끝나 `정보 없음`이 되는 설계는 원하지 않는다. 현재 WORK-012는 이 방향을 아직 담지 않았고 SPEC-006의 20/8/15KB·4걸음·80% 종료와 충돌한다.

SPEC-006을 0.3.10으로 개정하고 WORK-012를 그 계약에 맞춰 수정한다. 새 계약에서 **그래프 탐색 종료**와 **Claude 입력 선별**을 분리한다.

- 질문의 명시 대상·필수 facet·안전 항목을 추적하고, 방문 노드/이웃/section/page/pair의 frontier를 중복 없이 여러 순회한다. 4걸음은 초기 탐색 한 차례의 기본값으로만 쓸 수 있고, 필수 근거가 비었는데 중지시키는 전체 상한이 아니다. 안전 8KB·일반 20KB·원문 15KB 및 예산 80%는 탐색 완료/중단/`enough` 조건에서 제거한다. 카테고리별 고정 바이트 장부가 탐색을 막지 않는다.
- Jev는 의도·시작·다음 이웃 선택 역할을 유지한다. 사실 선택/섹션/page 순서는 결정론적 규칙으로 하되, 질문별 정답 ID를 이용한 점프는 하지 않는다. 후보 경로 소진, 사실 조회 완료, 근거 부족, 시간/도구 오류를 구분한다. 시간·모델 컨텍스트 등의 실제 운영 제약으로 멈추면 `blocked/incomplete`이며 사실 부재로 단정하지 않는다. 무한 루프 방지는 방문 tuple·진전 감지로 한다.
- Claude에는 질문 대상·facet에 관련된 인용 가능 fact 원문과 출처, 필수 안전 fact, 적용 범위가 맞는 관계 주장/대안만 중복 제거해 넘긴다. 선택에서 탈락한 사실도 검색 기록에는 남긴다. 입력이 큰 경우 근거를 조용히 버리지 않고 항목별 묶음/분할 처리 또는 `incomplete`로 표시한다. 안전·정확성 모두 검증한다.
- 실제 종료 조건, 관련성 선택 기준, 전달 누락 검증, trace, 개별 재생, 50문항 시험을 SPEC/WORK에 구체적으로 적는다. fullrun-v2 25/28은 안전 근거의 일부이며 전체 회복 수로 쓰지 않는다. 원천/Gold에 없는 사실은 생성하지 않는다.
- 기존 역사적 0.3.8/0.3.9 규정과 새 규정의 우선순위를 명확히 하고, 현재 코드 미구현을 명시한다. 새 설계가 Hub WORK-011 관계 계약과 충돌하지 않게 한다. 기존 SPEC/WORK의 예산 숫자와 종료 문구를 전수 검색해 새 규범으로 읽히지 않도록 고친다.

## 허용 범위와 검증

- 수정 허용: `orchestration/work/phub-recommend/SPEC-006.md`, `WORK-012.md` 두 파일만.
- 다른 문서·외부 코드·서버·DB·평가 기록을 수정하지 않는다. 새 평가를 실행하지 않는다.
- `rg`로 고정 8/20/15KB, 4걸음, budget/enough/80% 관련 문구를 점검하고 현재/역사 구분을 리포트에 남긴다. 작업서의 WP/코드 표면/시험/끝 조건이 새 계약에 대응해야 한다.
- 커밋·push·PR 하지 않는다. 완료 시 dispatch preamble대로 `worker_done`을 정확히 한 번 보낸다.
