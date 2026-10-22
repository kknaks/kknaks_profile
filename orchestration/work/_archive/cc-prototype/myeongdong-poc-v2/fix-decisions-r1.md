# 리뷰 r1 처분 — 코디 기본값 (2026-10-21)

리포트: `review-wp1-5-report.md`. SPEC 정정은 planner 가 같은 내용으로 SPEC-003 에 반영한다.

| 지적 | 처분(기본값) |
|---|---|
| F1 · F2 · S6 | env 는 루트 `procedure/.env` 하나. compose 가 back + front 를 띄운다 — front 는 `NEXT_PUBLIC_*` 를 **build.args** 로 받는다(compose 가 루트 .env 에서 넘김). front 를 따로 띄울 때는 `procedure/front/.env.local`(gitignore) — README 에 절차. `docker compose up --build` 한 줄로 back 8700 · front 3700 |
| F3 · S9 | SSE `?token` 을 접근 로그에 남기지 않는다 — uvicorn 접근 로그에서 쿼리 문자열을 지우는 필터(또는 `/api/board/stream` 접근 로그 끔). 토큰 방식은 그대로 |
| W1 · S3 | `failed` 뒤에는 **KOS 값을 따른다**(D-09 KOS 기준). 대신 그 visit(카드)에 「KOS 반영 실패」 표시가 **남는다** — 그 visit 의 다음 op 이 성공(confirmed)할 때까지 |
| W2 · S4 | 같은 visit 에서 op 하나가 `failed` 면 **뒤 op 은 보내지 않고 멈춘다**(`blocked` → 결국 failed 로 표시). 담당자 지정 실패 뒤 호출을 보내지 않는다(D-24 순서) |
| W3 · W4 · W5 · S5 | 스냅샷에 기준을 싣는다: `limits: {callMin: 5, anesMin: 20}` + 카드 마취에 `long: bool`. back 은 **조회 시간과 상관없이 10초마다** `board` 를 발행한다(시간 경과 값 갱신). front 는 상수를 지우고 스냅샷 값만 쓴다 |
| W6 | KosError 아닌 예외도 잡아 `sync_state` 오류 · op 실패 경로로 보낸다(삼키지 않는다) · 로그는 클래스 · 상태만(본문 · 토큰 X) |
| W7 · S12 | 시스템 계정 id 를 모르면 원장 목록을 갱신하지 않는다(이전 값 유지) |
| W8 | 서버 시작 때 직원 · 방 조회는 **조회 시간과 상관없이 1회** |
| W9 | 그대로(KOS 는 room 을 지우지 않음 — HAR). 다만 KOS 에서 room 이 비면 카드가 사라지는 건 맞는 동작으로 둔다 |
| W10 · S11 | 가짜 KOS 가 실제 400 조건을 흉내: 같은 단계 flow-step 400 · 귀가 대기 일정의 call 400. 「이미 WAITING/READY 재호출」은 실 데모에서 E2E 때 확인(OQ) |
| W11 · S10 | **날짜가 바뀌면(KST 00:00) 전날 카드를 내린다**(present 끔) |
| W12 | `app = create_app()` 를 모듈 import 때 만들지 않게(팩토리 · uvicorn `--factory`) — 시험이 실 env · 실 DB 를 건드리지 않게 |
| W13 · S7 | `PROC_FAKE_BOARD` 는 개발 전용으로 남기고, 켜지면 **조작 API 를 막는다**(403) · README · `.env.example` 에 「배포에 넣지 않는다」 |
| W14 · S8 | ① front Dockerfile 빌드 인자 기본값을 비우거나 로컬로(배포 주소 X) ② 760px 미만 = 카드만(의국 화면은 넓은 화면 전제) — 그대로 · SPEC 에 적음 |
