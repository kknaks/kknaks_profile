# [backend] photo fix-1 — 검수 review-code-3 P1 · P4 · P7

**읽을 것**: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/review-code-3-report.md` 의 P1 · P4 · P7

## P1 — 사진 한 장씩 받고 저장한다
- `download_photos` 가 사진마다 결과를 돌려준다: 바이트 또는 실패.
- 받는 즉시 한 장씩 저장하고 커밋한다. 메모리에도 한 장씩만 둔다.
- 실패한 장은 `skipped` 로 센다.
- 테스트: 2장 중 1장이 실패하면 1장은 남는다.

## P4 — 다시 시도 · 올리기에 행 단위 잠금
- 다시 시도 · 올리기의 KOS 단계에 행 단위 Redis 잠금을 둔다(가져오기 잠금과 같은 꼴).
- 테스트: 같은 행을 동시에 등록하면 KOS 등록은 1회만 일어난다.

## P7 — 가져오기 자원
- `_known` 을 그 방문으로 좁힌다.
- 잠금 시간과 작업 시간 상한을 맞춘다(작업에 timeout).
- 받는 원본에 크기 한도를 둔다. 값은 올리기 한도와 같게 — OQ-96 기본값.

## 범위
- P5 는 기록만 하고 고치지 않는다.
- P2 · P3 · P6 은 사용자 확인 뒤에 따로 지시한다 — 건드리지 마라.

## 검증
- `scripts/test.sh -q backend/tests/day/board`
- ruff

## 보고
- 커밋 금지.
- 보고 파일 `be-photo-fix-1-report.md` + preamble worker_done 두 채널.
