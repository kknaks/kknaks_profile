# [backend · 기능 1] 예약 등록 · 예약 상세 — 서비스 · 라우터(API) · 예약 현황 SSE · 읽기

**기반 1(be-found-1) 을 끝낸 다음 같은 터미널에서 이어서 한다.** 기반 1 완료 보고를 먼저 보내고 이걸 시작해라.

## SSOT

- **SPEC-007 (계약 · 지금 판 그대로 따른다)**: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation2-spec/products/day/20-spec/spec-007-reservation-detail.md` — §3 API 계약(이름 제안 → 이름 그대로 쓴다) · 화면이 읽는 칸 · KOS 쓰기 W 표 · 케이스 매트릭스 · 실시간 갱신(D52) · §4 Functional Rule · DB
- SPEC-006 개정 ⑫ · SPEC-002 개정 ㉘ · SPEC-000 개정 ② (같은 폴더)
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-24-reservation-detail/reservation-detail-decisions.md`(D1 ~ D54 · D53 = 다음 스펙)
- 실물 `be-probe-1 ~ 4-report.md`(이 폴더)
- 검수 2차가 동시에 돌고 있다 — SPEC 이 나중에 조금 바뀌면 고침으로 따로 준다. **지금 판 그대로 구현한다.**

## 할 일 (backend 몫 전부)

1. 예약 등록: 같은 고객 찾기(R39 예외 · 저장 요청 안) · 새 고객(쓰기 큐 순서 묶음 · duplicate_token) · 예약 만들기 · 열/구역 · 담당자 = 로그인 직원 · 지정 의사 · 유입 · 메모
2. 예약 상세 읽기(모달 JSON/조각 데이터): 단계 · 날짜 경계 · 고객 정보 · 예약 정보 · 동행 · 상담 정보 · 시술 목록(지난 시술권 + 이번 구매 · 오늘 ✓ · 상태 4 · n/m회) · 수납 정보(원내 현황 금액 + 할인 전 가격) · 수납 버튼 상태(KOS 수납 중) · 딥링크 2 · 이전 방문 · 상담사 / 의사 / 관리실 목록
3. 쓰기 동작: 접수 · 신분증 확인(true/false) · 상담사 지정 / 바꾸기 · 관리실 · [상담 대기] 연쇄 · 시술만 진행 [시술 대기] 연쇄 · 오더 메모 · 의사 지정 · 귀가 처리(단계별 · 사유) · 예약 변경(우클릭 옮기기 · 창) · 예약 취소 · 동행 저장(모달 체크 · 묶음 통째) — 전부 기반 1 의 쓰기 계획 · 쓰기 큐 위에서
4. **예약 현황 SSE** `/reservations/stream`(시술 현황 `routers/board_streams.py` 본뜸 · 이벤트 = SPEC-007 실시간 갱신 절) · R41 10초 조각 폴링 대체
5. 끌어 놓아 동행 묶기 입구 제거(SPEC-006 ⑫ · D45) — 기존 `PUT /reservations/companions` · `/leave` 처리는 SPEC 대로
6. 지정 의사 읽는 자리(SPEC-000 ② · 동기화 매핑)

## 계약 (frontend 와)

SPEC-007 §3 API 계약 · 화면이 읽는 칸 · 실시간 갱신 절이 계약이다. frontend 워커가 같은 워크트리에서 템플릿 · static 을 동시에 만든다. 템플릿 조각에 넘길 값 이름이 SPEC 에 없으면 먼저 정해 `contract-v1.md`(이 폴더)에 적고 코디에게 알려라.

## allowed_paths

- `backend/` 에서 **frontend 몫(`backend/day/routers/`(api 제외) 의 화면 라우터 · `templates/` · `static/` · `styles/`)은 빼고**. 화면 라우터가 꼭 필요하면 frontend 와 `contract-v1.md` 로 맞춰라
- `backend/migrations/versions/` · `backend/tests/`

## 하지 말 것

KOS 실제 호출(테스트는 가짜) · `deploy/*.env` · 로컬 스택 · 사용자 포트 · 커밋 · push · D53(즉시 다시 읽기 일반화) · 화면 문구 짓기.

## 검증 · 보고

`cd backend && uv run pytest -q <만든/고친 테스트만>` · `uv run ruff check <만진 파일>` 각 1회. 완료 보고는 be-found-1 §9 두 명령 그대로(subject 「backend 완료: 기능 1」 · task-id · dispatch-id 는 이번 dispatch 값).
