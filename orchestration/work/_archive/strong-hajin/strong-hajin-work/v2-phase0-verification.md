# v2 Phase0 현재 기준선 검증

2026-09-17 코드변경 전 코디 실행. Node20.20.0, PYTEST_XDIST_AUTO_NUM_WORKERS=4. 코드수정 없음.

| 명령 | 결과 | 로그 |
|---|---|---|
| make test-unit | exit0, 322 passed | v2-phase0-test-unit.log |
| make test-contract | exit0, 976 passed | v2-phase0-test-contract.log |
| make frontend-test | exit0, 645 passed | v2-phase0-frontend-test.log |
| make test-postgres (localhost:54329/ax_test) | exit0, 65 passed | v2-phase0-test-postgres.log |

과거 W1 수치 재사용 아님. 현재 코드에서 4종 직접실행. 실제 업무데이터 ax_demo는 빈DB이므로 데이터이관 검사 완료주장 없음. v2 구현통과를 뜻하지 않음. baseline manifest 82파일 현재sha 일치(별도 관측), 운영적용 없음.
