"""day-app-re1 Delivery 2 (WORK-002) — request JSON 두 개(backend+web · mobile) 생성.

사용: python3 make2.py <out_dir> <origin/main full SHA>
WORK-001(make.py · request-p1-backend.json · request-p2-mobile.json)은 건드리지 않는다.
idempotency key 는 WORK-001 과 겹치지 않게 `day/day-app-re1/work-002/...`.
"""
import json
import os
import sys

OUT, MAIN = sys.argv[1], sys.argv[2]
SRC = "fadb46f66b9f69db125f1d31cb0e18eec58cbc99"  # PR #964 — N1 ~ N6 반영 커밋
CODE = "96036397ba4f7f197cd736dbc0d02dc685862969"  # 코드 워크트리 HEAD(WORK-001 코드 · 미push)

SPECS = ["DAY-SPEC-003", "DAY-SPEC-007", "DAY-SPEC-006", "DAY-SPEC-005", "DAY-SPEC-004", "DAY-SPEC-000"]

RS = (f"SPEC 원천 = DAY-SPEC-003 ㉒ · 007 고침 5(+ 보충 · review-doc-4 N1 ~ N6) · 006 ⑭ · 005 · 004 · 000 2026-11-25 — Mediness PR #964(draft · 머지 전 · 커밋 {SRC}). "
      "target SPEC 여섯은 main 에서 이미 stable → spec-baseline:ready(「stable 고도화」 · 바뀌는 내용 = Target Delta · 계약 W · #281 · #282 와 같은 방식). 머지 뒤 같은 key · version +1 · 새 SHA 로 재결속 가능")
SPLIT = (f"WP 나누기: backend+web 하나 · mobile 하나 — 웹(Jinja)은 앱 상세 JSON 과 같은 service(`reservation_detail.detail_view`) · 같은 router · 띄우기 · 문진 service 를 쓰는 얇은 화면이라 나누면 같은 파일 · 직렬 순서(병렬 이득 없음). mobile = app/ 만(backend 와 안 겹침). "
         f"개발 병렬(계약 W 인터페이스 = 두 Issue 같은 글 · mobile 은 테스트 더블) · 순서 = mobile A4 실물만 backend 뒤. 코드 = CENTURION_DAY kknaksss/day-app-re1(WORK-001 {CODE[:8]} 위 · 미push)")
E2E_RULE = "E2E = 사용자가 시뮬레이터에서 — 로컬 BE 스택 + 시뮬레이터 · Android 에뮬레이터 빌드가 완료 기준 · 카메라 실물 스캔(iPad · 갤럭시 탭) = 사용자 E2E · 배포 · TestFlight 아님 · 머지 나중에 한 번에(사용자)"

NON = [
    "앱 예약 쓰기 11개 · 앱 [다시 보내기](앱 예약현황 = 읽기 전용 · DAY-SPEC-003 U-25)",
    "웹 예약 동작 변경 — 예외 하나: 외국인 여권 스캔 저장 → [상담 대기] · [시술 대기] 신분확인 칸(review-doc-3 U1)",
    "여권 사진 열람 · 삭제(OQ-D34) · cc 스캔 QR 받기(`claim`) · 계정 없는 기기 등록 토큰",
    "WORK-001 차트 계약(#281 · #282) · 원장 호출 · 채팅 푸시 규칙 변경",
    "iOS 카메라 문구 여권 용도(OQ-A79 사용자 문구 대기 — 지금 D15 그대로)",
    "법적 검토 = DAY-ESC-001 참조만(비차단) · 배포 · TestFlight · Play",
]

W0 = ("W0 공통: 인증 /api Bearer(DAY-SPEC-001 · 예외 = 문진 공개 API 둘 · W7) · 오류 `{detail, code, field}`(+`details`) · 검사 401→403→400→404→409 · "
      "권한 = 목록 · 스트림 · 상세 `reservation` view / 보내기 · 닫기 · 기기 목록 · 스캔 저장 · 여권 값 · kos-retry · 다시 보내기 `reservation.detail` edit(새 키 없음) / 메우기 = 로그인 세션 · 자기 기기만 · id = DAY uuid · KOS id 안 실음 · 이름 = 이름 제안(다르면 상대 워커 · 코디에 먼저 알림)")
W1 = ("W1 앱 예약 목록(DAY-SPEC-006 ⑭): `GET /api/reservations?date=&poll=` → 웹과 같은 service · 같은 값(`today` · `date` · `open_min` · `axis` · 열 · 카드 · `rows` · `bands` · 필터 수 · 공지 보기 · 원내 현황) · 쓰기 칸 · KOS id 없음 / "
      "`GET /api/reservations/stream` SSE = `reservation`(version) · `display`(방문 id) · `session_expired` · 규칙 = `/api/board/stream` 과 같음")
W2 = ("W2 앱 상세(DAY-SPEC-007 앱 JSON 짝): `GET /api/reservations/visits/{visit_id}` → `detail_view` 값(「화면이 읽는 칸」) + `displays[]`(종류 · 상태 · 기기 이름 · 시각) + `actions`{questionnaireQr, passportScan, sendToTablet} + 문진 보냄 상태(「보냄」/「실패」 · 멈춘 sending = 실패) · 여권 칸 · 쓰기 칸 · KOS id 없음 · 404")
W3 = ("W3 여권 값(U4 · N1): `GET /api/reservations/visits/{visit_id}/passport` → 7칸 `passportSurname` · `passportGivenNames` · `passportNumber` · `nationality` · `dateOfBirth` · `gender` · `passportExpiryDate`(DAY 사본 · 빈 고객 = 7칸 null) · 확인 화면 열 때만 · 409 = W6 과 같은 조건 · 앱 읽기 실패 = 열 비움 · 7칸 모두 보냄(N2)")
W4 = ("W4 띄우기(DAY-SPEC-007 「태블릿 띄우기」): 기기 목록 웹 `GET /reservations/visits/{id}/display-targets` · 앱 `GET /api/display-targets` → `targets[]{deviceId, name, online}`(tablet · 살아 있는 세션 · 직무 coordinator · 이름 순 · 빈 이름 「태블릿」) / "
      "만들기 웹 `POST /reservations/visits/{id}/display-requests`(form kind · device_id) · 앱 `POST /api/visits/{id}/display-requests` `{kind: questionnaire|scan, deviceId?}` → `{requestId, kind, status, expiresAt, deviceName?, qrUrl?}`(qrUrl = 문진만 · `/q#<토큰>` · scan = deviceId 필수 · 토큰 없음) · 409 `visit_not_today` · `visit_stage_changed` · `reservation_past_date` · 404 목록 밖 기기 · 같은 방문 · 종류 앞 요청 canceled · 10분 / "
      "닫기 웹 `POST /reservations/display-requests/{id}/close`(form status=canceled) · 앱 `POST /api/display-requests/{id}/close` `{status: canceled}`(다른 값 400 · 409 이미 닫힘) / 메우기 `GET /api/display-requests/pending` → `requests[]{requestId, kind, visitId, expiresAt, qrUrl?}`(자기 기기 앞만 · scan 이면 opened) / "
      "상태 pending → opened → done | canceled | expired · 바뀔 때마다 그 방문 신호 `display`(웹 `/reservations/stream` · 앱 `/api/reservations/stream`)")
W5 = ("W5 기기 하나로 닿기(DAY-SPEC-005 「띄우기 — 기기 하나」): `GET /api/notifications/stream` 이벤트 `display` `{requestId, kind, visitId}` — 연결 세션의 기기가 대상일 때만(같은 계정 다른 기기 제외) / 푸시 = 그 기기 하나에 늘 · iOS `aps.alert{title, body}` 소리 없음 · Android FCM data `{kind: display, requestId, environment, hospitalId, title, body}` → 로컬 알림 · 채널 「고객 입력 요청」 · "
      "제목 「고객 입력 요청」(문진) / 「여권 스캔 요청」(스캔) · 본문 「데스크에서 보냈어요」 · notification 행 없음 · push_log `display` / 눌러 들어오면 메우기")
W6 = ("W6 여권 스캔 저장(DAY-SPEC-007): `POST /api/visits/{visit_id}/passport-scan` multipart `fields`(JSON · W3 키 · 바뀐 칸만 · name 없음) · `photo`(JPEG ≤5MB · 손 입력이면 없음) · `manual` · `displayRequestId?` → 200 `{identity, photo: {id, kosSynced}|null, kos: {customer: ok|unchanged, photo: ok|failed|skipped|null}}` · "
      "오류 400 · 413 · 404(displayRequestId 가 이 방문 · 이 기기 · scan 아님) · 409(`visit_not_today` · `visit_stage_changed` · KOS 고객 연결 없음) · 503 `kos_unavailable` · `photo_disabled` / 다시 올리기 `POST /api/id-photos/{photo_id}/kos-retry` → `{photo: {id, kosSynced}, kos: {photo}}`")
W8 = "W8 기기 이름(DAY-SPEC-003 U-30): `PUT /api/devices/{install_id}/name` `{name}` · 빈 값 = 앱이 안 보냄 · 등록 전이면 등록(`PUT /api/devices/{install_id}`) 때 이름 실음(칸 이름 BE)"
W6B = ("W6b 스캔 저장 처리(BE): KOS `get-visitor` 다시 읽기 → `PERSONAL_KEYS` + 바뀐 칸 → `update-visitor-personal-information` · 요청 세션 직원 토큰 직접(태블릿 = 코디 계정) · 실패 = 아무것도 안 남김 → DAY 사진 `identity/{병원}/{무작위}.jpg` + `id_photo`(passport) → KOS 사진 = 규칙 39 경로 · 분류 「여권」(없으면 skipped) · 실패 = kosSynced false · `external_ref` id_photo → "
       "`identity_check`(confirmed · `app_scan`/`app_manual` · device · id_photo · 직원) · `event_log passport_scan` · 요청 done + `display` 신호 → [상담 대기] · [시술 대기] 신분확인(`care_rows.identity_confirmed` · A-77)")
W7 = ("W7 고객 문진 웹(BE · DAY-SPEC-007 「고객 문진 웹」): `GET /q`(Jinja · 로그인 없음 · 토큰 `#` 뒤) · `GET`/`POST /api/public/questionnaire`(헤더 `X-Questionnaire-Token` 만 · Authorization 무시) · 언어 6 · cc `text.ts` 글자 · KOS 양식 · 약관 그대로 · "
      "제출 = DAY `questionnaire_history`(web_submit · kos_status sending) 먼저 · 요청 done + 신호 → KOS 공개 `submit-visitor-questionnaire`(같은 KosClient timeout) → sent | failed · 고객 200 = DAY 저장되면 · 멈춘 sending = 읽을 때 실패(OQ-D41) · 링크 10분 / 60분 / 1회 · "
      "no-store · no-referrer · 속도 제한(IP GET 30 · POST 5 · 토큰 POST 3 · 틀린 토큰 10번 막음 · IP = `ext_peer.ip_key`) · 오류 `q_token_missing` · `q_not_found` · `q_submitted` · `q_submitting` · `q_expired` · `q_canceled` · `too_many_requests` · `invalid_request` · "
      "웹 [다시 보내기] `POST /reservations/visits/{id}/questionnaire/resend`(실패일 때만 · 같은 답 · 동시 한 번 · 아니면 409)")
W9 = "W9 migration 1(0028 뒤): `display_request.qr_token_hash` · `qr_nonce` null 허용 · `questionnaire_history` + `kos_status`(sending · sent · failed) · `kos_error` · `kos_sent_at` · 값만 = display kind · identity method(manual · app_scan · app_manual) · external_ref id_photo · push_log display"
W7_APP = "W7 문진(앱 몫): 공개 페이지 · API 안 부름 · W4 `qrUrl` 을 그리기만 · 결과 = W2 의 초진 문진 · 건강정보 · 「보냄」/「실패」 글자 · [다시 보내기] 없음"
CONTRACT_IF = [W0, W1, W2, W3, W4, W5, W6, W8]  # 두 Delivery 같은 글(인터페이스)
CONTRACT_BE = CONTRACT_IF + [W6B, W7, W9]
CONTRACT_APP = CONTRACT_IF + [W7_APP]

def req(key, title, risk, delta, acc, non, rsx, ex):
    return {
        "product_id": "day", "document_root": "products/day", "contract_version": 1,
        "spec_baseline_revision": MAIN, "idempotency_key": key, "title": title,
        "risk_level": risk, "target_specs": SPECS, "target_delta": delta,
        "acceptance": acc, "non_goals": NON + non,
        "review_surface": [RS, SPLIT, E2E_RULE] + rsx, "execution": ex,
    }


R = {}
R["p1-backend-2"] = req(
    "day/day-app-re1/work-002/p1-backend",
    "DAY 예약 띄우기 backend+web — 앱 예약 /api · 태블릿 보내기(SSE · 푸시) · 여권 스캔 저장 · 고객 문진 공개 웹 · 웹 [문진 QR] · [여권 스캔] (DAY-SPEC-007 고침 5 · 006 ⑭ · 005 · 000)",
    "L3",
    ["서버(backend) + 웹(Jinja) — 아래 계약 W0 ~ W9 전부(앱 예약 JSON · 띄우기 · 기기 하나 SSE · 푸시 APNs + FCM · 여권 스캔 저장 · 고객 문진 공개 웹 · 기기 이름 · migration 1)",
     "웹 예약 상세(DAY-SPEC-007 RD-02 · RD-03 · U-3 · 「태블릿 띄우기」 규칙 7): [문진 QR] · [여권 스캔] 켬(D55 보이는 조건 그대로) · [문진 QR] = 이 화면 QR + 상태 줄 · 배지 · 「QR 닫기」 · [태블릿에 보내기] 기기 팝오버(「 · 접속 중」 · 목록 실패 글자) → 「{기기}에 표시 중」 · [여권 스캔] = 기기 팝오버 → 진행 줄 「{기기}에 보냈어요 · 여는 중…」 / 「{기기}에서 스캔 중 · 촬영 대기 중…」 · [취소] · 진행 = SSE `display` 로 모달만 다시 받기 · 초진 문진 · 건강정보 = DAY 저장 답 · 「보냄」 / 「실패」 + [다시 보내기] · 신분확인 = 스캔 기록 표시(외국인 스캔 저장 → 「O」 · [상담 대기] · [시술 대기] 켜짐 — U1) · 글자 = cc `Display.tsx` · SPEC 에 있는 것만(없는 것 = OQ-D33 · D17 그대로 비움)",
     *CONTRACT_BE,
     "범위 밖 확인만: WORK-001 앱 차트 경로(#281)는 건드리지 않는다 · 웹 예약 쓰기 경로 동작 그대로(U1 신분확인 칸 하나 예외)"],
    ["A1: 계약 W1 ~ W8 경로마다 pytest — Bearer 200 · 권한 없음 403(`reservation` view / `reservation.detail` edit) · 다른 병원 404 · 조건 밖 409 코드 · 모르는 칸 400 · 응답 칸 · 안 싣는 칸(여권번호 · 쓰기 칸 · KOS id) 없음 · 기기 목록 = 코디 직무 · 태블릿 · 살아 있는 세션만 · 같은 방문 같은 종류 새 요청이 앞 요청 `canceled` · 닫기 `done` 400 · 메우기 = 자기 기기 앞만",
     "A2: 기기 하나로 닿기 — 같은 계정 두 기기 연결 중 대상 기기만 `display` 받음 · 푸시 = 그 기기 하나 · iOS / FCM payload 모양 · 제목 둘 · `notification` 행 0 · `push_log` `display` 1행 (DAY-SPEC-005 A 항목)",
     "A3: 여권 스캔 저장 — KOS 고객 수정 실패 = 아무것도 안 남음 · `unchanged` · 사진 KOS 실패 = `kosSynced=false` 뒤 `kos-retry` 200 · 분류 「여권」 없음 = `skipped` · `identity_check` `app_scan` / `app_manual` · 그 뒤 웹 [상담 대기] · [시술 대기] 신분확인 「O」(A-77)",
     "A4: 고객 문진 — 공개 페이지 · API 가 로그인 없이 · `Authorization` 무시 · 토큰 쿼리 · 경로 거절 · 응답 머리 둘 · 속도 제한 429 · 오류 코드 8 · 제출 = DAY 먼저 저장(KOS 실패여도 행 남음 · `failed`) · 멈춘 `sending` 읽기 「실패」 · [다시 보내기] 실패일 때만 · 같은 답 · 동시 한 번 (A-65 ~ A-67)",
     "A5: 웹 예약 상세 Jinja — [문진 QR] · [여권 스캔] · 「태블릿에 보내기」 · 진행 줄 · 초진 문진 · 건강정보 · [다시 보내기] 렌더 테스트 · 기존 웹 예약 테스트 회귀 없음 · migration upgrade / downgrade · 전체 pytest · ruff",
     "A6: 실물 1회(로컬 BE 스택 · KOS 데모 지점 · check_open_key_is_demo 통과 뒤만): 여권 스캔 저장 1(KOS 데모 고객 여권 칸 바뀜) · 사진 1(KOS 데모 일정 「여권」 분류 · DAY 저장소) · 고객 문진 제출 1(KOS 데모 고객 문진 들어감 · DAY `questionnaire_history` `sent`) — 결과를 Code PR 에 적음"],
    [],
    ["새 **로그인 없는 공개 API** · 고객 건강 문진 · 여권 사진 저장 · KOS 외부 쓰기(고객 수정 · 사진 · 공개 제출) · 푸시 · migration — L3",
     "KOS 공개 문진 경로의 자격(시스템 계정 · OQ-D39) · 속도 제한 자리(OQ-D40) · `online` 판정 자리(OQ-D31) = 기본값으로 진행 · BE 가 코드 확인 뒤 정하고 Code PR 에 적음",
     "DAY-SPEC-001 원칙 예외 — 문진 KOS 제출 · [다시 보내기]는 직원 토큰이 아님(KOS 기록에 직원 안 남음 · review-doc-3 W11) · 태블릿 스캔 KOS 기록 = 코디 계정(알고 감)"],
    {"code_surface": [
        "backend/day/routers/api/ 새 파일(예약 JSON · 띄우기 · 여권 스캔 · 기기 이름 — 나누기 BE) · routers/api/__init__.py 등록 · routers/api/devices.py(이름) · routers/api/notifications.py · streams.py(`display` · 기기 가리기)",
        "backend/day/routers/reservation_detail.py · reservations_streams.py · public_pages.py(`/q`) · templates/partials(예약 상세 RD-02 · RD-03) · templates/public(문진 페이지 6언어)",
        "backend/day/services/reservation_detail.py · reservation_detail_care.py · reservations.py(같은 service) · 새 display · passport_scan · questionnaire service · push.py · devices.py · notification_events.py · visit_photo_kos.py(재사용)",
        "backend/day/emr/kos/(공개 문진 · 고객 수정 호출 · client.py 같은 timeout) · routers/api/ext_peer.py `ip_key`(재사용)",
        "backend/migrations/versions/(0029 — W9) · backend/tests/day/(새 테스트)"],
     "domain_candidates": ["display_request 상태(pending · opened · done · canceled · expired)", "questionnaire_history.kos_status(sending · sent · failed)"],
     "dependencies": ["없음(mobile 과 병렬 · WORK-001 코드 96036397 위)"],
     "phases": ["P1 migration · 앱 예약 목록 · 스트림 · 상세 · 여권 확인 값 JSON(W1 ~ W3 · W9)", "P2 띄우기 요청 · 메우기 · 닫기 · 상태 · SSE 기기 가리기 · 푸시 APNs / FCM · 기기 이름(W4 · W5 · W8)", "P3 여권 스캔 저장 · KOS 고객 수정 · 사진 KOS + DAY · identity_check · kos-retry(W6)", "P4 고객 문진 공개 페이지 · API · KOS 경로 · questionnaire_history · 보냄 상태 · 다시 보내기 · 보안(W7)", "P5 웹 예약 상세 Jinja(문진 QR · 여권 스캔 · 태블릿에 보내기 · 진행 · 문진 값) · 전체 pytest · 실물 1회(A6)"],
     "verification": ["cd backend && uv run pytest -q · uv run ruff check · alembic upgrade / downgrade", "로컬 BE 스택 + KOS 데모 지점 실물 — 고객 수정 · 사진 · 문진 제출 각 1(A6)"],
     "predeploy": ["dev 배포 때 공개 origin 설정 · 앞단 클라이언트 IP 헤더 · APNs · FCM 키 확인(이번 단계는 로컬만)"],
     "rollback": ["Code PR revert + migration downgrade(`display_request` null 허용 되돌리기 전 scan 행 정리 · `questionnaire_history` kos 칸 drop) — KOS 에 이미 쓴 고객 수정 · 사진 · 문진은 되돌리지 않음(KOS 에서 처리)"],
     "open_questions": ["DAY-SPEC-007 OQ-D27 ~ D42(기본값으로 진행 · 비차단)", "DAY-SPEC-005 OQ-N21 · N22(묶음)"]})

R["p2-mobile-2"] = req(
    "day/day-app-re1/work-002/p2-mobile",
    "DAY 앱 예약현황(읽기 전용) · 문진 QR · 여권 스캐너(iOS Vision · Android CameraX+ML Kit) · 태블릿 받기 · 기기 이름 (DAY-SPEC-003 ㉒)",
    "L2",
    ["하단 메뉴 4(「예약현황」 · 「시술현황」 · 「채팅」 · 「설정」 · 첫 메뉴 시술현황 — U-2 · A-61)",
     "예약현황 탭(U-24 · 웹과 닮게 · 보충 1): 태블릿 = 웹과 같은 시간 × 열 표 · 폰 = 같은 카드를 목록으로 · 날짜 바꾸기 · 신호 `reservation` 뒤 `poll=1` 다시 읽기 · 공지 · 원내 현황 = 태블릿 오른쪽 패널 보기만 · 폰 안 그림(OQ-A80 기본값) · 값 = 계약 W1",
     "예약 상세(U-25 · 읽기 전용): 웹 모달 상자 순서 · 칸 · 글자 · 단계 이름 · 색 그대로 · 쓰기 버튼 · 고르기 · 체크 0 · 누르는 것 = [문진 QR] · [여권 스캔] · [태블릿에 보내기](`actions` 대로) · 진행 `displays[]` · 신호 `display` 로 다시 읽기 · 문진 「보냄」 / 「실패」 글자만 · 값 = 계약 W2",
     "문진 QR(U-26): 흰 전체 화면 QR · 「휴대폰 카메라로 QR 을 찍어 주세요」 · 「Scan with your phone camera」 · 「남은 시간 mm:ss」 / 「시간이 지났어요」 · 화면 꺼짐 막기 · `qrUrl` 로그 · 토스트 금지 · 요청 = W4 만들기 `deviceId` 없이",
     "여권 스캔(U-27 · 「여권 스캔 · QR 네이티브 채널」): 채널 `day/scan` — `scanPassport{windows, windowSec, debug}` · `qrImage{text, size}` · `keepAwake(bool)` · 네이티브 → Dart `checkMrz(lines)` · **iOS** = cc `TextScanner.swift` 꼴(AVCaptureSession · Vision `.accurate` · 매크로 카메라 · CIQRCodeGenerator · 배포 대상 13.0 그대로) · **Android(새로)** = CameraX `ImageAnalysis` + ML Kit 글자 인식 v2 **번들 Latin**(minSdk 24 안 · 오프라인) · QR 그리기 · 꺼짐 막기 네이티브 · `android.permission.CAMERA` 매니페스트 + 실행 중 요청(거부 = `no_camera` → 손 입력) · 파서 = cc `mrz.dart` 그대로(Dart 한 곳) · 실패 3번 · 권한 거부 · 카메라 없음 → [손으로 입력] · 확인 화면(읽은 값 ↔ 「KOS 지금 값」 = W3 · 다른 칸 노란 강조 · 칸 7 · 썸네일 · [다시 찍기] · [저장] · 「저장 중…」 · [다시 저장] · 실패 글자) → 저장 = W6 · 원본 사진 사진첩 · 파일 · 캐시에 안 남김 · `image_picker` 카메라는 스캔에 안 씀",
     "태블릿에 보내기(U-28): 기기 팝오버 = W4 기기 목록 · 요청 = W4 만들기 `deviceId` · 진행 = 상세 `displays[]` · 신호",
     "띄우기 받기(U-29 · 태블릿 쪽): 앱이 열려 있으면 알림 스트림 `display`(W5 스트림) → 메우기(W4 메우기) → 문진 = QR 전체 화면 · 스캔 = 그 방문 상세 읽기 → 스캔 화면 · 이미 연 요청 다시 안 엶 · 한 번에 하나씩 · 뒤 · 꺼짐 = 알림(W5 푸시 · iOS APNs · Android FCM data → 로컬 알림 · 채널 「고객 입력 요청」 · 소리 없음) 누름 → 메우기 → 엶 · 알림 안 누르고 앱 열어도 메우기 · Dart · Android 네이티브 푸시 갈래가 `display` kind 를 앎 · 웹 [취소] · 새 요청 = 앞 화면 닫힘",
     "설정 「이 기기」(U-30): 「기기 이름」 줄 · 창 「이 기기 이름」 · 자리 글 「예: 데스크 아이패드」 · [취소] · [저장] → W8 · 빈 값 = 저장 안 함 · 등록 전에도 누름 · 등록 전엔 「알림을 켜면 웹 기기 목록에 보여요」 줄 더함",
     "권한: Android `CAMERA` 넣음(차트 · 채팅 `image_picker` 카메라 길 영향 확인 = OQ-A91 · A-69) · **iOS 카메라 문구는 지금 D15 그대로**(여권 용도 = OQ-A79 사용자 문구 대기 — 짓지 않음)",
     *CONTRACT_APP],
    ["A1: DAY-SPEC-003 A-61 ~ A-77(개정 ㉒ 줄) 중 앱 몫을 위젯 · 단위 테스트로(테스트 더블 — 계약 W1 ~ W8 모양 fixture): 메뉴 4 · 폰 목록 / 태블릿 표 · 상세 읽기 전용(쓰기 0 · 버튼 셋 `actions`) · 문진 QR 화면 · 남은 시간 · 꺼짐 막기 호출 · 스캔 확인 화면(강조 · 손 입력 · 비교 값 없으면 7칸) · 보내기 팝오버 · 받기(메우기 · 한 번에 하나 · 다시 안 엶) · 기기 이름 · 권한 거부 → 손 입력",
     "A2: MRZ 파서 단위 테스트(cc `mrz.dart` 테스트 이식 — TD3 · 체크 숫자 · 확정 규칙) · 푸시 갈래 `display` 테스트(Dart · Android `PushLogicTest.kt`) · 기존 앱 테스트 회귀 없음 · WORK-001 차트 테스트 그대로",
     "A3: cd app && flutter analyze 0 · flutter test 통과 · flutter build ios --no-codesign 성공 · **flutter build apk(또는 Android 에뮬레이터 빌드) 성공** · Android 매니페스트 `CAMERA` · ML Kit 번들 의존성",
     "A4: 시뮬레이터 실물 1회(로컬 BE 스택 — p1-backend-2 구현 뒤): 예약현황 목록 → 상세 → [문진 QR] 전체 화면 · 손 입력 스캔 저장 1회(카메라 없는 시뮬레이터 → [손으로 입력]) · 웹에서 [태블릿에 보내기] → 시뮬레이터 앱이 받기 1회(열린 상태 · 메우기) + Android 에뮬레이터 빌드 · 실행 · **카메라 실물 스캔(iPad · 갤럭시 탭)은 사용자 E2E**"],
    [],
    ["새 네이티브 채널(iOS Swift · Android Kotlin · CameraX · ML Kit) · Android 새 권한(`CAMERA`) · 예약 탭 신설 · 고객이 보는 QR 화면 — 화면 · 동작 넓은 변경 · KOS 쓰기는 BE 경유만 — L2",
     "화면 글자 = cc 원천 · SPEC 에 있는 것만(없는 것 비움 · OQ) · 세부 모양 = 2루프 E2E · ML Kit 라이선스 · 사용 지표 전송 개인정보 안내(OQ-A89) · 갤럭시 탭 판독률은 실물 확인"],
    {"code_surface": [
        "app/lib/ui/shell.dart(메뉴 4) · 새 예약 화면(목록 · 표 · 상세 — 파일 나누기 mobile) · app/lib/ui/session_nav.dart(띄우는 자리) · theme.dart",
        "app/lib/data/day_api.dart(W1 ~ W8 호출) · event_stream.dart · sse_transport.dart(예약 스트림 · 알림 스트림 `display`) · push_bridge.dart(`display` 갈래)",
        "새 app/lib/scan/(채널 · `mrz.dart` 이식 · 스캔 · 확인 · QR 화면) · app/lib/core/copy.dart(글자)",
        "app/ios/Runner/(새 TextScanner.swift 꼴 · AppDelegate 채널 등록 · Info.plist 그대로)",
        "app/android/app/src/main/kotlin/day/medisolveai/(새 ScanChannel · MainActivity 등록 · PushLogic · DayMessagingService `display` · 채널 「고객 입력 요청」) · app/android/app/build.gradle(CameraX · ML Kit 번들) · AndroidManifest.xml(`CAMERA`)",
        "app/test/ · app/android/app/src/test/kotlin/(PushLogicTest)"],
     "domain_candidates": [],
     "dependencies": ["개발 = p1-backend-2 와 병렬(계약 W 고정 · 테스트 더블) · A4 시뮬레이터 실물만 p1-backend-2 구현(로컬) 뒤 · WORK-001 코드 96036397 위"],
     "phases": ["P1 메뉴 4 · 예약현황 목록(폰) / 표(태블릿) · 예약 스트림", "P2 예약 상세 읽기 전용 · 버튼 셋 · 진행 · 문진 QR 화면", "P3 스캔 채널 iOS(Vision) · Android(CameraX + ML Kit 번들) · MRZ 파서 · 손 입력 · 확인 화면 · 저장", "P4 태블릿에 보내기 · 받기(알림 스트림 · 푸시 갈래 · 메우기) · 설정 「이 기기 이름」", "P5 analyze · test · build ios · build apk · 시뮬레이터 실물 1회(A4)"],
     "verification": ["cd app && flutter analyze · flutter test · flutter build ios --no-codesign · flutter build apk --debug(또는 에뮬레이터 실행)", "Android 단위 테스트(gradle testDebugUnitTest)", "시뮬레이터 + 로컬 BE 스택 실물(QR · 손 입력 스캔 · 받기 1회) · 카메라 실물 = 사용자 E2E"],
     "predeploy": [],
     "rollback": ["Code PR revert(앱 화면 · 네이티브 채널 · 매니페스트 되돌림 — 서버 데이터 영향 없음)"],
     "open_questions": ["DAY-SPEC-003 OQ-A79(iOS 여권 문구 — 사용자) · OQ-A80 ~ A91(기본값으로 진행 · 비차단)"]})

os.makedirs(OUT, exist_ok=True)
for name, body in R.items():
    with open(os.path.join(OUT, f"request-{name}.json"), "w", encoding="utf-8") as f:
        json.dump(body, f, ensure_ascii=False, indent=2)
    print(name, "ok")
