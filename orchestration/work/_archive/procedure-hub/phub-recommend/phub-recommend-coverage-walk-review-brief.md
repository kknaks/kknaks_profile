# [reviewer] SPEC-006 0.3.10 / WORK-012 반복 탐색 검수

너는 read-only 문서 검수 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다.

## 읽을 것

- `orchestration/roles/procedure-hub/reviewer/` 역할 문서, 루트 `AGENTS.md`, `orchestration/runbook.md`
- `orchestration/work/phub-recommend/SPEC-006.md` 0.3.10, `WORK-012.md`, `SPEC-005.md` 0.3.9, `WORK-011.md`
- `review-info-absence-work011012.md`(이전 판), `reference/2026-10-30-hub-evals/HANDOFF.md` §4
- 앱 코드 `clinic_chat/cases/case3.py`, `config.py`, `hub_rest.py` 읽기만 (`/Users/kknaks/orca/workspaces/clinic_chat/hub-evals/`)

## 검수 질문

사용자는 여러 번 그래프를 탐색해 필요한 정보를 찾고, **최종 답에 필요한 자료만 Claude에 넘기라**고 정정했다. 예산 때문에 중간에 멈춰 `정보 없음`이 되는 것을 막아야 한다. 새 SPEC/WORK가 실제로 이를 계약·WP·검증에 반영했는지, 특히 다음을 확인한다.

1. 8/20/15KB, 4걸음, 80%, Jev `enough`가 현행 탐색 hard stop으로 남아 있지 않은가? 역사적 문단/현재 규범 우선순위가 명확한가?
2. 수집과 Claude 입력 선별이 분리되고, 질문 target/facet/안전 관련 근거가 수집→선별→전달→답에서 보존되는가? 관련성 선별에서 근거가 조용히 사라지거나 안전 fact가 누락될 구멍은 없는가?
3. 질문별 필요한 근거가 확인되면 끝낼 수 있고, 아직 못 찾은 항목을 `정보 없음`으로 오인하지 않는가? `unresolved_absence`는 실제 범위 완료 증거가 있는가? 노드·page·관계 frontier가 무한 반복하지 않는가?
4. 운영 timeout/provider 컨텍스트 제한은 실제 장애 안전장치로만 쓰이고, 값은 코드 워커가 측정해 보고할 수 있는가? 사용자에게 숫자 결정을 다시 요청하는 불필요한 관문이 남았는가?
5. Hub WORK-011 관계 계약 의존, 코드 표면, 시험 사례, 고정 50 관문이 실행 가능한가? WORK-012 전체를 발주했을 때 WP-4 선행 조건이 지켜지는가?

각 지적을 FAIL/WARN/PASS와 줄·근거·최소 수정안으로 적고, 코드 발주 선행 수정 여부를 판정한다. 0.3.9 이전 리뷰 수치가 현행 판의 PASS를 뜻하지 않음을 명시한다.

## 허용 범위

- 읽기 전용. 결과 파일 `orchestration/work/phub-recommend/review-coverage-walk-spec-work.md`만 생성 가능.
- 코드·SPEC·WORK·서버·DB·평가 기록 수정/실행 금지. 원장 본문 인용 금지.
- 커밋·push·PR 금지. 완료 시 dispatch preamble대로 `worker_done`을 한 번 보낸다.
