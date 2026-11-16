# [backend] seed_demo_board.py 리뷰 반영 1차

너는 앞 작업(task_8e949d318f19)을 한 day backend 워커다. 같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2`, 같은 규칙(원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/day-procedure-board-2-be-brief.md` §5 · §7 — 커밋 · push · PR 금지).

리뷰 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-seed-demo-board-report.md` — 판정 FAIL 1 · WARN 8. 지적마다 파일:줄 · 고치는 법이 적혀 있다.

## 고칠 것
- **F1**: 쓰기 전에 공개 키가 데모 지점 것인지 확인 — 공개 zone id 가 데모 내부 예약 그룹 `intervalCapacities[].zoneId` 에 없으면 아무것도 쓰지 않고 멈춘다(dry-run 에서도). 리포트의 방법이 아니어도 「공개 키 병원 = 데모」를 쓰기 전에 증명하면 된다
- **W1 · W8**: 실패 줄에 「KOS 에 남았을 수 있음」 표시 · 끝 요약에 실패한 사람의 번호 · 단계 · 사유 다시 출력
- **W2**: 같은 칸을 다시 돌려도 이름이 겹치지 않게(실행마다 다른 짧은 접미어)
- **W3**: `KosError` 밖의 예외도 그 사람만 실패로 남기고 다음 사람으로(예외 이름만 기록 — 값 금지). `usable` 필터가 `procedure` 를 확인하게 해 initialize-purchase 뒤에 멈추는 자리를 없앤다
- **W5 · W6**: 테스트 — run() 이 KosClient 를 만들기 전에 가드로 멈추는지 · F1 확인(FakeKos 로) · detail() 404 재시도 / 다른 상태 바로 실패
- **W7**: 지난 칸이면 거부 · `--count` 상한 30
- **W4(국적 alpha-2)는 그대로 둔다** — 사용자 승인 대기

## 검증
- `uv run pytest -q backend/tests/scripts` · ruff check · format — 각 1회
- **실물(필수)**: 고친 스크립트를 새 칸에서 **처음부터 끝까지 한 번에** 실행 — `--slot 15:30`(지났으면 다음 빈 칸). 10명 전부 시술 대기 · 오더 메모 · 방 · 시술 작업 확인 결과 표. 중간에 이어 붙이지 마라 — 한 번에 끝나는 것을 보는 시험이다
- 실패가 나면 고치고 **다른 새 칸**에서 다시 한 번에(같은 칸 재사용 금지)

## 완료 보고
원 브리프 §9 와 같은 두 명령. 코디 핸들 `term_b915fb18-742f-4779-962c-79848020b8d5`. 지적별 고친 내용(파일:줄) · 테스트 수 · 실물 표.
