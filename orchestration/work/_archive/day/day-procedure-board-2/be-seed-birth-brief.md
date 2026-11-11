# [backend] 시드 스크립트 — 테스트 고객에 생년월일 넣기 (e2e F6)

같은 워크트리 · 같은 규칙. 대상은 `scripts/seed_demo_board.py` · `backend/tests/scripts/test_seed_demo_board.py` 뿐(다른 코드 · 템플릿 손대지 마라 — 다른 작업이 기다리는 중).

사용자: 「테스트 데이터에 생년월일이 없다」 → 카드 바이탈 줄에 만 나이가 안 뜬다. 새로 만드는 테스트 고객에 **가짜 생년월일**을 넣는다.
- 예약 생성(공개 reserveV2)의 고객 칸에 생년월일을 넣을 수 있는지 **KOS 공개 API 문서(https://developers.kos-solution.com/openapi.yaml)로 확인**하고 그 필드로. 없으면 HAR(`/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/reference/2026-11-09-cc-day/har/`)에 고객 생년월일을 넣는 요청이 있는지 보고, 둘 다 없으면 지어내지 말고 보고만
- 값은 사람마다 다르게 · 그럴듯한 성인 나이대(가짜) · 개인 값 출력 금지 규칙 그대로
- 순수 로직 테스트(생년월일 만들기) 추가 · 기존 테스트 유지
- 실물: **데모 지점에 한 칸 1회 실행**(`--slot` 지금 다음 빈 칸 · `set -a; . /Users/kknaks/git/CENTURION_DAY/deploy/local.env; set +a`) → 만든 고객의 생년월일이 KOS 에 들어갔는지 조회로 확인
- 검증: 관련 pytest · ruff 1회 · 커밋 금지

완료 보고: 코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd` — worker_done(+ terminal send) · subject "backend 시드 생년월일". 쓴 필드 · 근거 · 실물 결과.
