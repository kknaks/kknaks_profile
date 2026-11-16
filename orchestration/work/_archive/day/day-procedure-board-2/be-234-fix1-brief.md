# [backend] #234 리뷰 반영 1차

같은 워크트리 · 같은 규칙(`/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/be-delivery234-brief.md`). 리뷰: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-234-report.md` (WARN 3).

## 고칠 것
- **W2**: `test_board_api.py` A2 테스트에 방 배정 작업이 남은 판으로 [귀가 대기]를 한 번 더해 `cancel-flow-tasks` 가 데모 · 실제 병원 양쪽 op 에 있고 같은지 단언
- **W3**: `tests/architecture/` 에 테스트 — `backend/day` 안에서 `is_demo` 가 나오는 파일이 `models/hospital.py` · `services/crm_connections.py`(시드) · `public.py` 뿐인지(레포 AGENTS.md 「경계는 tests/architecture 가 지킨다」)
- **참고 1**: `writes.py` docstring 에서 지워진 확인 조건(`expect`) 형식 단락 되살리기(#234 무관 삭제)
- W1(dev 데이터 전제)은 코디가 dev DB 로 확인 — 너는 손대지 마라

## 검증
관련 테스트 + `-m 'not infra'` 전체 · ruff 1회. Docker 는 켜지 마라(infra 는 사용자 답 대기 — pending).

## 완료 보고
원 브리프 §9 두 명령, 코디 핸들 `term_b915fb18-742f-4779-962c-79848020b8d5`.
