"""day-app-re1 Delivery 1 — request JSON 두 개(backend · mobile) 생성.

사용: python3 make.py <out_dir> <origin/main full SHA>
"""
import json
import os
import sys

OUT, MAIN = sys.argv[1], sys.argv[2]
SRC = "e7c51875901e0f156951967f7ad1230227901666"

RS = (f"SPEC 원천 = DAY-SPEC-003 개정 ㉑(U-23) + DAY-SPEC-002 개정 ㉚(「차트 · 사진 JSON 짝」) — Mediness PR #964(draft · 브랜치 kknaksss/day-app-re1-spec · 머지 전 · 커밋 {SRC} · 검수 review-doc-2 + fix-2 끝). "
      "main 에 없어 spec-baseline:pending 으로 시작 · PR #964 머지 뒤 같은 idempotency key · contract_version +1 · 새 origin/main SHA 로 재결속(결과 계약 같으면 재승인 없음 — requests.md)")
SPLIT = ("WP 나누기(planner · 코디 브리프 2026-11-25): backend Delivery(앱 /api JSON 짝) · mobile Delivery(앱 차트 화면) 두 개 · **개발은 병렬**(아래 계약 C 를 두 워커가 같은 글로 봄 · 앱은 테스트 더블로) · 의존 = mobile 완료 조건(시뮬레이터 실물 저장 · 사진)만 backend 구현 뒤 · "
         "코드 워크트리 하나(CENTURION_DAY day-app-re1 · 브랜치 kknaksss/day-app-re1 · base origin/dev 55e60aa4) → Code PR 하나에 두 Delivery 를 함께 연결(앞 #275 ~ #278 → #280 과 같은 꼴) · backend = backend/ · deploy/ · mobile = app/ — 서로 안 건드림")
E2E_RULE = "E2E = 사용자가 시뮬레이터에서(TestFlight 대신 · 사용자 2026-11-25) — 로컬 BE 스택 + 시뮬레이터 앱이 완료 기준 · dev 배포 · TestFlight 는 이번 단계 아님 · 머지는 나중에 한 번에(사용자)"

NON = [
    "여권 스캐너 · 문진 QR · 예약 탭(WORK-002 · DAY-SPEC-003 §1 뺌 — 다음 작업)",
    "웹 차트 동작 · 웹 HTML 경로 · 권한 규칙 · 사진 대상 규칙 변경(DAY-SPEC-002 개정 ㉚ 「웹 동작 · 웹 경로 · 권한 · 사진 대상 규칙은 바꾸지 않는다」 · D7 · D8 · C7) — 웹 경로를 Bearer · JSON 협상으로 넓히지 않음",
    "migration · 새 칸 · 새 테이블 · 새 권한 키(DAY-SPEC-002 개정 ㉚ DB · DAY-SPEC-003 「migration 판단 = 없음」)",
    "[고객 차트] 버튼 · 누른 시술 강조 · 지난 방문 차트(DAY-SPEC-003 §1 뺌 · OQ-A63)",
    "dev 배포 · TestFlight · 정식 출시(이번 단계 아님 — 사용자 2026-11-25)",
]

# ── BE ↔ APP 계약 (DAY-SPEC-002 개정 ㉚ §3 「차트 · 사진 JSON 짝」 · DAY-SPEC-003 §3 「차트 · 사진 — 앱이 쓰는 칸」 인용 · 이름 제안) ──
C_COMMON = ("계약 C0(공통 — 두 Delivery 같은 글): 인증 = /api 공통(Bearer · CSRF 안 봄 · DAY-SPEC-001) · 권한 = 보기 `board` view(차트 GET · 사진 목록 · 파일) / 쓰기 `board` edit(탭 저장 · 올리기 · 삭제 · 다시 시도) · `is_admin` = 전부(C7) · "
            "같은 service(board.save_chart_tab · visit_photos.list_photos · upload · delete · retry · open_file · open_tab · visit_photo_import.request_import · wait_imported) · 같은 규칙(규칙 23 대상 방문 · 31 검사 순서 · 충돌 · 39 사진) · 대상 방문 넓히지 않음(D8) · "
            "오류 본문 = /api 공용 `{detail, code, field}`(+ `details`) · 코드 = 웹과 같은 코드: 400 `invalid_request` · `photo_type` · `chart_too_long`(자리만 — 지금 서버는 안 보냄) · 401 `session_expired`(직원 KOS 토큰 없음 포함) · 403 `forbidden` · 404 `not_found`(규칙 23 대상 밖 · 그 방문 줄 · 사진 아님) · "
            "409 `chart_conflict` · `chart_staff_required` · `staff_not_listed` · `doctor_not_listed` · 413 `photo_too_large`(본문 상한 — 장당 초과는 `rejected`) · 409 · 503 `photo_disabled` · `photo_id` = DAY 행 id(`visit_photo.id` · KOS id 안 실음)")
C_CHART_GET = ("계약 C1(값 원천 · 이미 있음 · 바꾸지 않음): `GET /api/visits/{visit_id}/chart`(`board` view · routers/api/board.py:149-161) — 앱이 쓰는 칸 = `customer`{name, phoneticName, gender, birthDate, nationality} · `firstTab` · `tasks[]`{id, title, assignee|doctor: {body, staffId, logId, base{body, doctorStaffId}, savedAt, author}} · `staffOptions`{assignee|doctor: [{staffId, name, job}]}")
C_SAVE = ("계약 C2(차트 탭 저장 · 새): `POST /api/visits/{visit_id}/chart` · `board` edit · 요청 JSON `{chart: \"assignee\"|\"doctor\", rows: [{taskId, body, staffId, baseLogId, baseBody, baseDoctorStaffId}]}` — 그 탭 바뀐 줄만(1개 이상 · 그 방문 줄 · 같은 taskId 두 번 안 됨) · "
          "빈 값 = `staffId` · `baseLogId` · `baseDoctorStaffId` 는 uuid 또는 `null` · `body` · `baseBody` = 문자열(빈 문자열 허용) · 칸 생략 · 모르는 칸 = 400 `invalid_request`(extra=forbid) · **`staffId = null` 은 400 이 아니라 서비스까지 가 409 `chart_staff_required`** · "
          "응답 200 `{saved: [taskId], lastSavedAt, tasks: [{id, title, assignee|doctor: {body, staffId, author, savedAt, logId, base}}]}`(그 방문 줄 전부의 요청한 차트 종류 칸 · 저장된 줄은 새 logId · base · 안 보낸 줄은 지금 DAY 값) · "
          "409 `chart_conflict` = 공용 오류 본문 + `details.conflicts: [{taskId, body, staffId, base: {body, doctorStaffId}, baseLogId}]`(아무것도 저장 안 됨 · body = KOS 글 + 줄바꿈 + 내 글 — 서버가 만듦) · 그 밖 거절 = 공용 오류 본문만 · 집도의를 바꾼 저장 = 판 바뀜 → 앱은 SSE `board` 로 받음")
C_PHOTOS = ("계약 C3(사진 · 새 다섯): "
            "① 목록 `GET /api/visits/{visit_id}/photos?poll=&tick=`(`board` view · 없음 = 가져오기 작업 + 최대 3초 · `poll=1` = 다시 읽기만 · `tick=1` = 작업만 넣고 안 기다림) → `{visitId, reread, groups: [{category: \"before\"|\"after\", title, items: [{photoId, shotAt, kosSynced}]}]}`(묶음 둘은 빈 묶음도 늘 · title = 「시술 전」 · 「시술 후」 서버 TITLES · 순서 shot_at 오름차순 · `edit` 칸 안 실음 — 앱은 /me 권한) · "
            "② 올리기 `POST /api/visits/{visit_id}/photos`(`board` edit · multipart `category` + `file` 여러 개 · 장당 5MB · JPEG · PNG · 장 수 한도 없음 · 본문 100MiB = 앞단 Caddy + 서버 BODY_MAX_BYTES) → 200 = 목록 모양 + `kosError`(없으면 null) + `rejected: [code]` · "
            "③ 삭제 `POST /api/visits/{visit_id}/photos/{photo_id}/delete`(`board` edit) → 200 = 목록 모양 + `kosError` · "
            "④ 다시 시도 `POST /api/visits/{visit_id}/photos/{photo_id}/kos-retry`(`board` edit) → 200 = 목록 모양 + `kosError` · "
            "⑤ 파일 `GET /api/visits/{visit_id}/photos/{photo_id}/file`(`board` view · Bearer) → 웹과 같은 바이트 · 머리 `Cache-Control: no-store` · `Content-Disposition: inline` · `X-Content-Type-Options: nosniff` — 웹 사진 GET 둘의 쿠키 전용(`required_web_view`)은 그대로")
C_OPEN = ("계약 남은 선택(이름 제안 — BE 가 코드 확인 뒤 확정 · 다르면 두 워커 · 코디에 먼저 알리고 spec-sync 에서 DAY-SPEC-002 · 003 고침): DAY-SPEC-002 OQ-99(탭 저장 200 `tasks` 칸 · 409 걸린 줄 `details.conflicts` vs 최상위 · 사진 목록 `title`) · OQ-100(PhotoError 413 · photo_type · photo_disabled 가 /api 공용 모양으로 나가는지 — 기본값 = 공용 모양 · 같은 코드)")
CONTRACT = [C_COMMON, C_CHART_GET, C_SAVE, C_PHOTOS, C_OPEN]

SPECS = ["DAY-SPEC-003", "DAY-SPEC-002"]


def req(key, title, risk, delta, acc, non, rsx, ex):
    return {
        "product_id": "day", "document_root": "products/day", "contract_version": 1,
        "spec_baseline_revision": MAIN, "idempotency_key": key, "title": title,
        "risk_level": risk, "target_specs": SPECS, "target_delta": delta,
        "acceptance": acc, "non_goals": NON + non,
        "review_surface": [RS, SPLIT, E2E_RULE] + rsx, "execution": ex,
    }


R = {}
R["p1-backend"] = req(
    "day/day-app-re1/p1-backend",
    "DAY 앱 차트 backend — 앱 /api JSON 짝 6(차트 탭 저장 · 사진 목록 · 올리기 · 삭제 · 다시 시도 · 파일) · Bearer (DAY-SPEC-002 ㉚ · 003 ㉑)",
    "L3",
    ["앱용 `/api` JSON 짝 여섯을 새로 연다(DAY-SPEC-002 개정 ㉚ D7) — 웹 경로와 **같은 service · 같은 규칙 · 같은 오류 코드** · 다른 것은 응답 모양(JSON)뿐 · 웹 HTML 경로 · 웹 사진 GET 쿠키 전용은 그대로",
     *CONTRACT,
     "앞단(Caddy) 본문 상한 100MiB 를 앱 올리기 경로 `/api/visits/*/photos` 에도(C33 짝 · deploy/caddy/Caddyfile · 그 밖 경로 6MiB 그대로) · 서버 BODY_MAX_BYTES 같은 값",
     "routers/api/board.py 머리 주석 「차트 저장 JSON 짝은 없다」 정리 · 옛 `POST /api/tasks/{task_id}/chart` 는 SPEC-002 가 「지우는 대상」 — dev `55e60aa4` 에 이미 없음(확인만)",
     "migration 없음(같은 칸 `visit_task_chart_log` · `visit_task.assignee_note` · `doctor_note` · `visit_photo` · `external_ref`)"],
    ["A1: 여섯 경로가 계약 C2 · C3 의 요청 · 응답 · 오류 코드와 같음(pytest — Bearer 로 각 경로 200 · 보기 권한 계정 쓰기 4경로 403 · 대상 밖 방문 404 · 모르는 칸 400 · `staffId = null` 409 `chart_staff_required` · 저장 충돌 409 `chart_conflict` + `details.conflicts` · 응답 유실 뒤 같은 저장 200(C19) · 사진 형식 · 크기 `rejected` · KOS 실패 `kosError` · 파일 머리 셋)",
     "A2: 웹 경로 회귀 없음 — `POST /board/visits/{id}/chart` · `/board/visits/{id}/photos*` 기존 테스트 그대로 통과 · 웹 사진 GET 둘 Bearer = 401 그대로 · 전체 pytest 회귀 없음 · ruff",
     "A3: Caddyfile 에 `/api/visits/*/photos` 100MiB 줄 · 그 밖 경로 6MiB 그대로(deploy 테스트 있으면 그것으로)",
     "A4: 실물 1회(로컬 BE 스택 · KOS 데모 지점 · check_open_key_is_demo 통과 뒤만 · 앱 로그인 직원 Bearer 토큰으로 curl 등): 차트 GET → 탭 저장 200(KOS 데모 일정 차트 반영 확인) → 사진 올리기 2장(KOS 데모 일정 사진 탭에 보임) → 목록 → 파일 → 삭제 → (KOS 실패 줄 있으면) 다시 시도 — 결과를 Code PR 에 적음"],
    [],
    ["새 공개 API(앱 · Bearer)가 KOS 외부 쓰기(차트 outbox · 사진 등록 · 삭제)를 부름 · 앞단 배포 설정(Caddy) 한 줄 — L3",
     "OQ-99 · OQ-100 응답 모양 확정은 BE 몫 — 이름 제안과 다르면 mobile 워커 · 코디에 먼저 알림"],
    {"code_surface": [
        "backend/day/routers/api/board.py(차트 GET 옆 · 탭 저장 짝) · routers/api/ 사진 짝(새 파일 또는 같은 파일 — 이름 BE 가 정함) · routers/api/__init__.py 등록",
        "backend/day/schemas/board.py · board_responses.py(요청 · 응답 모델 — extra=forbid)",
        "재사용(바꾸지 않음 · 필요하면 반환 값만): backend/day/services/board_charts.py · board_chart_writes.py · visit_photos.py · visit_photo_import.py · visit_photo_kos.py · presentation/photos.py · routers/board.py `_chart_rows` · routers/board_photos.py `BODY_MAX_BYTES` · `_message`",
        "deploy/caddy/Caddyfile(`/api/visits/*/photos` 100MiB)",
        "backend/tests/day/board/test_board_chart_api.py · test_board_photos.py · photo_support.py · board_api_support.py(새 테스트 · 지원 함수)"],
     "domain_candidates": [],
     "dependencies": ["없음(첫 판 · mobile 과 병렬)"],
     "phases": ["P1 차트 탭 저장 JSON 짝 + 테스트", "P2 사진 다섯 JSON 짝 + 파일 Bearer + 테스트", "P3 Caddy 100MiB 줄 · 머리 주석 · 전체 pytest · 실물 1회(로컬 · KOS 데모)"],
     "verification": ["cd backend && uv run pytest -q(새 · 고친 테스트 + 웹 차트 · 사진 회귀) · uv run ruff check", "로컬 BE 스택 + KOS 데모 지점 실물 호출 1회(A4)"],
     "predeploy": ["dev 배포 때 Caddy 설정 반영 확인(이번 단계는 로컬만)"],
     "rollback": ["Code PR revert(경로 · Caddy 줄 제거 — migration 없음 · 데이터 되돌림 없음)"],
     "open_questions": ["DAY-SPEC-002 OQ-99(응답 모양) · OQ-100(PhotoError 모양)"]})

R["p2-mobile"] = req(
    "day/day-app-re1/p2-mobile",
    "DAY 앱 차트 mobile — 차트 = 웹과 같은 기능(탭 셋 · 탭별 저장 · 사진 탭) · 세션 Navigator · 까만 줄 · iOS 권한 문구 (DAY-SPEC-003 ㉑ U-23 · 002 ㉚)",
    "L2",
    ["차트 화면(DAY-SPEC-003 U-23): 여는 곳 그대로(룸 상세 시술 줄) · 값 원천 = 계약 C1 `GET /api/visits/{id}/chart` 한 번(스냅샷 노트 안 씀 · 시술 전 의사차트 보임 · D11) · 머리 = 이름 · 발음 · 바이탈 줄 · [✕] · 탭 셋 「간호관리차트」 · 「의사차트」 · 「시술전후사진」(D13) · 처음 탭 = `firstTab` · 차트 탭 줄 = 시술명 · 담당자 · 차트 내용",
     "탭별 [저장] + 「최근 저장 : HH:MM」(D2 · 병원 현지 시각 `ui/format.dart` `hm`) · 바뀐 줄만 계약 C2 한 요청(줄바꿈 정규화 · 앞뒤 빈칸 빼기 비교 C20) · 보내는 동안 [저장] 꺼짐 + 그 탭 칸 잠금 · 15초 넘김 · 200 = 응답 `tasks` 로 줄 바꿈 · 창 안 닫음 · 성공 토스트 없음 · 409 `chart_conflict` = `details.conflicts` 줄만 바꿈 · 토스트 C29 · 그 밖 거절 글자(U-23 · `core/copy.dart` 맞춤 · 계약 시험 포함) · 보기 권한 = 읽기만",
     "담당자 고르기 = 원장 고르기 드로어(`doctor_picker.dart` · 폰 시트 / 아이패드 팝오버 · D5) · 목록 = 그 칸 `staffOptions` · 직군 글자 · 목록 밖 `staffId` = 빈칸",
     "닫기(D6′ · D12 — U-23 닫기 표): 미저장 없으면 ✕ · 뒤로 가기 · 끌어 내림 · 바깥 누름 다 닫힘 · 미저장 있으면 ✕ · Android 뒤로 = 확인 창(「저장하지 않고 닫을까요?」 · [계속 쓰기] · [버리고 닫기]) · 끌어 내림 · 바깥 누름 = 안 닫힘 · iOS 가장자리 밀기 = 막힘 · 탭 옮기기 = 경고 없음 · 세션 끝 = 함께 닫힘",
     "사진 탭(U-23 · 계약 C3): 두 묶음 · 탭 고를 때마다 목록(`reread` 면 5초 뒤 `poll=1`) · 보이는 동안 10초 `tick=1`(다른 탭 · 닫힘 · 백그라운드 · 고르는 중 · 올리는 중 = 건너뜀) · 올리기 여러 장(채팅 `chat/photo_pick.dart` · JPEG · OQ-A73 기본값 = 카메라 1장 / 앨범 여러 장) · 삭제 확인 창 「사진을 삭제할까요?」 · 「KOS 미반영」 + [다시 시도] · 크게 보기(`chat_photo_screen.dart` 재사용) · 파일 = Bearer 바이트 메모리만(`chat_media.dart` 꼴 · `Image.network` 안 씀) · 토스트 글자 C27 · C36 · `photo_disabled`",
     "띄우는 자리 = 세션(루트) Navigator(D4 · `shell.dart` `_sessionNav`) · 폰 = 전체 화면 · 아이패드 = 가운데 창(지금 410×640 · D3) · 차트 위에 뜨는 것도 같은 Navigator · 토스트 = 차트 창 위 층(U-13)",
     "까만 줄 = `ui/theme.dart` 탭 구분선 색을 DAY 토큰으로(D9) · 탭바 겹침 = 원장 고르기 드로어(`doctor_picker.dart:93`) · 확인 시트(`room_screen.dart:753`) · 아이패드 팝오버(`doctor_picker.dart:83` · 투명 덮개 그대로) · 확인 창(`room_screen.dart:742`)도 세션 Navigator 로(D9 · D14) · 통역 시트 둘은 그대로(OQ-A77)",
     "iOS 권한 문구(D15 · `app/ios/Runner/Info.plist`) = DAY-SPEC-003 §4 Frontend 「iOS 권한 문구(D15)」 표 글자 그대로 · 마이크 그대로 · Android 해당 없음 · 새 권한 없음",
     *CONTRACT],
    ["A1: DAY-SPEC-003 A-51 ~ A-60 · A-17 · A-38(개정 ㉑ 줄)이 위젯 · 단위 테스트로(테스트 더블 — 계약 C1 ~ C3 모양 fixture): 세션 Navigator · 폰 전체 화면 / 아이패드 가운데 창 · 탭 셋 글자 · 저장 켜짐 · 바뀐 줄만 · 충돌 · 거절 글자 · 닫기 표 다섯 갈래 × 미저장 있음 / 없음 · 담당자 고르기 · 사진 목록 · 10초 tick 멈춤 · 올리기 · 삭제 확인 · 다시 시도 · 보기 권한",
     "A2: 까만 줄 없음 · 원장 고르기 · 확인 시트 / 팝오버 · 창이 탭바 · 레일을 덮음(A-52) · Info.plist 두 문구 = SPEC 글자(A-17 빌드 검사) · `board_messages_contract_test.dart` 통과 · 기존 앱 테스트 회귀 없음",
     "A3: cd app && flutter analyze 0 · flutter test 통과 · flutter build ios --no-codesign 성공",
     "A4: 시뮬레이터 실물 1회(로컬 BE 스택 — p1-backend 구현 뒤 · KOS 데모 지점): 룸 상세 시술 줄 → 차트(세션 Navigator · 탭바 덮음) → 간호관리차트 담당자 · 글 → [저장] 200 · 「최근 저장」 → 사진 탭 → 앨범 2장 올리기 → KOS 데모 일정 사진 탭에 보임 → 크게 보기 → 삭제 — 뒤 사용자 시뮬레이터 E2E"],
    [],
    ["앱 화면 · 동작 넓은 변경(차트 쓰기 · 사진 · 세션 Navigator 로 시트 옮김 · 테마) · KOS 쓰기는 BE 경유만 — L2",
     "화면 글자 = SPEC 에 있는 것만(없는 것 OQ-A67 · OQ-A78 = 비움) · 세부 모양은 2루프 E2E(D3)"],
    {"code_surface": [
        "app/lib/ui/chart_sheet.dart(차트 창 · 탭 셋 · 저장 · 사진 탭 — 파일 나누기는 mobile 이 정함)",
        "app/lib/ui/room_screen.dart(여는 곳 :583-587 · 확인 시트 :742 · :753 → 세션 Navigator) · app/lib/ui/doctor_picker.dart(:83 · :88 · :93) · app/lib/ui/shell.dart(`_sessionNav`)",
        "app/lib/ui/theme.dart(탭 구분선) · app/lib/ui/format.dart(`hm`)",
        "app/lib/data/day_api.dart(계약 C1 ~ C3 호출) · app/lib/core/copy.dart(C27 · C29 · C36 글자)",
        "재사용: app/lib/chat/photo_pick.dart · chat/screens/chat_photo_screen.dart · chat/widgets/chat_media.dart · chat/screens/chat_attach_sheet.dart",
        "app/ios/Runner/Info.plist(:52-57 · D15)",
        "app/test/ui/ · app/test/core/board_messages_contract_test.dart · app/test/support/(테스트 더블)"],
     "domain_candidates": [],
     "dependencies": ["개발 = p1-backend 와 병렬(계약 C 고정 · 테스트 더블) · A4 시뮬레이터 실물만 p1-backend 구현(로컬) 뒤"],
     "phases": ["P1 세션 Navigator 로 차트 · 시트 · 팝오버 · 창 옮김 · 까만 줄 테마 · Info.plist", "P2 차트 탭 — 값 원천 차트 JSON · 담당자 고르기 · 탭별 저장 · 충돌 · 거절 · 닫기 표", "P3 사진 탭 — 목록 · 10초 tick · 올리기 · 삭제 · 다시 시도 · 크게 보기", "P4 analyze · test · build ios --no-codesign · 시뮬레이터 실물 1회(로컬 BE)"],
     "verification": ["cd app && flutter analyze · flutter test · flutter build ios --no-codesign", "시뮬레이터 + 로컬 BE 스택 실물 저장 · 사진 1회(A4) · 뒤 사용자 시뮬레이터 E2E"],
     "predeploy": [],
     "rollback": ["Code PR revert(앱 화면 · 테마 · Info.plist 되돌림 — 서버 · 데이터 영향 없음)"],
     "open_questions": ["DAY-SPEC-003 OQ-A66 ~ A70 · A72 · A73 · A74 · A75 · A77 · A78(기본값으로 진행 · 비차단)"]})

os.makedirs(OUT, exist_ok=True)
for name, body in R.items():
    with open(os.path.join(OUT, f"request-{name}.json"), "w", encoding="utf-8") as f:
        json.dump(body, f, ensure_ascii=False, indent=2)
    print(name, "ok")
