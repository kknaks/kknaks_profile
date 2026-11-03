# [reviewer_spec] case3 정보 없음 WORK-011/012 검수

너는 read-only 계획 검수 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다. 이 브리프 한 장으로 작업한다.

## 읽을 것

- 역할: `orchestration/roles/procedure-hub/reviewer_spec/`의 역할 문서
- 검수 대상: `orchestration/work/phub-recommend/WORK-011.md`, `WORK-012.md`
- 정본: 같은 디렉터리의 `SPEC-005.md`, `SPEC-006.md` 버전 0.3.9
- 앞 검수: `review-info-absence-spec005006-v2.md`
- 근거: `info-absence-remediation-plan.md`, `reference/2026-10-30-hub-evals/build-out/info-absence-audit/root-cause-next.md`
- 런북: `orchestration/runbook.md`의 직렬 파이프라인·WP 검수/사용자 리뷰 규칙

## 작업

두 WORK의 SPEC 정합, Hub→앱 의존 순서, 코드 표면·검증·끝 조건의 실행 가능성, 안전/시간/승격 결정의 미승인 상태, 측정 빌드 일치, 사용자 포트·컨테이너 보호를 검수한다. 각 지적은 FAIL/WARN/PASS, 문서 줄·SPEC 절 근거, 최소 수정안을 적는다. 특히 WORK가 코드 구현을 이미 했다고 오해시키거나, 현 T4를 선택 관계/전역 메모 수신 증거로 오인하거나, partial/blocked를 사실 부재로 확정하는지 확인한다.

## 허용 범위와 보고

- 읽기 전용. 결과 파일 `orchestration/work/phub-recommend/review-info-absence-work011012.md` 하나만 생성 가능하다.
- 코드·SPEC·WORK·서버·DB·평가 기록을 수정하지 않는다. 평가 실행 금지. 원장 인용 본문을 리포트에 복사하지 않는다.
- 마지막에 FAIL/WARN/PASS 개수와 코드 발주 선행 수정 여부를 명시한다.
- 커밋·push·PR 하지 않는다. 완료 시 dispatch preamble에 따라 `worker_done`을 정확히 한 번 보내고 종료한다.
