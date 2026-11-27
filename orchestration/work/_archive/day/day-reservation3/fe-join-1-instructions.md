# [frontend] 이어 붙이기 1 — backend 읽기 서비스 연결 · 문구 · 남은 테스트

맥락: 네 1판 보고 · backend 리포트 `be-1-report.md`(이 폴더 — 읽기 서비스 · 응답 · 오류 코드 · SSE). 같은 워크트리(backend 는 끝남 — 지금은 너 혼자).

1. `routers/reservation_requests.py` 의 자리 함수를 `services/reservation_request_reads.read_list` · `read_window` · `read_day` 로 바꿔 붙인다(dict 모양 = 네 docstring 그대로라고 backend 보고). POST 응답(HX-Trigger `day:res-queued` · 3열 조각 · 창 조각) · SSE `reservation_request` · `kos_failed` 의 `request_id` 가 backend 실제 값과 맞는지 확인 · 어긋나면 화면 쪽을 맞추고 보고(backend 파일은 고치지 마라 — 필요하면 `[질문]`)
2. **사용자 확정 문구(11-26)**: 변경 요청 답 기다림 상태 = 「답변 대기중」 · 변경 요청 거두기 버튼 = [철회] · KOS 쓰기 실패 줄 버튼 = [다시 시도] · [KOS 등록 실패](= 접음). 빈 문구 자리에 넣는다
3. `tests/architecture/test_screen_copy.py` VISIBLE 표 — 네 패치 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/fe-screen-copy-patch.py` + 위 문구(근거 = 「사용자 11-26」) · 고정본 fixture `DAY_UPDATE_FIXTURES=1 uv run pytest backend/tests/day/web/test_reservations_screen.py -k 고정본` · `test_role_structure`(contracts --write) · Taut `routers/reservations.py` `open_request` Query 설명 — 이번에 allowed_paths 에 `backend/tests/architecture/` · `scripts/frontend/tests/fixtures/` · contracts 산출물을 더한다
4. 검증: `cd backend && scripts/test.sh` 전체 1회(실패 0 또는 무관 분리) · 네 화면 테스트 · lint 류 1회

완료 보고 = 1판 브리프 §9 두 명령 · subject `frontend 완료: 이어 붙이기 1`.
