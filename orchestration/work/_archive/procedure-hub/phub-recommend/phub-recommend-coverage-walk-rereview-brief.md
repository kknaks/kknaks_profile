# [reviewer] 반복 탐색 계약 F-1/W-1/W-2 재검수

너는 read-only 문서 검수 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다.

## 읽을 것

- `orchestration/roles/procedure-hub/reviewer/` 역할 문서와 `orchestration/runbook.md`
- `orchestration/work/phub-recommend/review-coverage-walk-spec-work.md`의 F-1/W-1/W-2
- 같은 디렉터리의 `SPEC-006.md` 0.3.10 §3-4-1-5, `WORK-012.md`, `SPEC-005.md` §5-16, `WORK-011.md`

## 작업

1차 FAIL F-1(지원 fact 발견 뒤에도 모든 page/frontier 소진 요구), WARN W-1(허브 WORK의 옛 앱 15KB 설명), WARN W-2(SPEC-005의 옛 앱 참조)가 실제로 닫혔는지 줄·근거로 확인한다. 지원 완료와 부재 완료가 다르고, 앞 page 지원 후 조기 종료/뒤 page 지원/부재 `more=0`/미지원 필수 frontier 잔여 시험이 WORK에 있는지 본다. 사용자 지시인 반복 탐색과 최종 Claude 관련 근거 선별이 유지됐는지도 확인한다. 새 FAIL이 있으면 적는다.

## 허용 범위

- 읽기 전용. 결과 파일 `orchestration/work/phub-recommend/review-coverage-walk-spec-work-v2.md` 한 파일만 생성.
- 코드·SPEC·WORK·서버·DB·평가 실행/수정 금지. 커밋·push·PR 금지.
- 마지막에 FAIL/WARN/PASS 수와 코드 발주 가능 여부를 판정한다. 완료 시 dispatch preamble대로 `worker_done` 한 번.
