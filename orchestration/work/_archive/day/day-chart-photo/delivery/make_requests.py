import json, pathlib, sys

OUT = pathlib.Path("/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/delivery")
BASE = sys.argv[1] if len(sys.argv) > 1 else "a896cda0b9cfcc920b7c76ea1c278e8f697f9d28"
SRC = ("SPEC 원천 = DAY-SPEC-002 개정 ㉘ · DAY-SPEC-001 개정 ⑫(검수 review-doc-3 PASS) — Mediness PR #960 커밋 "
       "a896cda0b9cfcc920b7c76ea1c278e8f697f9d28(브랜치 kknaksss/day-chart-photo-spec · 머지 전). 결정 원천 = chart-photo-decisions.md C1 ~ C17")

# --- 공통 계약 문장 (세 Issue 에 같은 글자) ---
K1 = ("계약 K1(차트 열기 — #① 제공 · #③ 소비): `GET /board/visits/{visit_id}/chart` 는 그대로 · 차트 값의 `tasks[].assignee` · `tasks[].doctor` 에 "
      "`base` = `{body, doctorStaffId}`(그때 DAY 사본 — 간호관리 `assignee_note` · 의사 `doctor_note` + 집도의 · 간호관리는 `doctorStaffId` 없음)를 더한다(SPEC-002 §3 차트 JSON). "
      "탭마다 「최근 저장」 = 그 차트 종류 `tasks[].{chart}.savedAt` 최댓값(새 칸 없음 · 템플릿이 셈 · W9)")
K2 = ("계약 K2(차트 탭 저장 요청 — #③ 보냄 · #① 받음): `POST /board/visits/{visit_id}/chart` · 폼 칸 `chart`(assignee | doctor) + 줄마다 같은 이름 칸을 줄 순서대로 반복 — "
      "`taskId` · `body` · `staffId` · `baseLogId` · `baseBody` · `baseDoctorStaffId`(의사만 · 간호관리는 빈 값) · **바뀐 줄만**(day.js 가 안 바뀐 줄 칸을 disabled 로 빼서 보내지 않음) · "
      "칸 수가 서로 다르면 400 `invalid_request` · HTMX `X-CSRF-Token`(DAY-SPEC-001) · 이름 · 인코딩은 제안 — 두 PR 이 같은 글자로 맞춘다")
K3 = ("계약 K3(차트 탭 저장 응답 — #① 제공 · #③ 소비): 저장됨 200 = 그 탭 조각 `partials/board_chart_tab.html`(이름 제안 · 값 `chart` · `tab` · `saved_at` · 줄마다 다음 저장용 `base` · `baseLogId`) "
      "+ 집도의를 바꿨으면 지금처럼 그 카드 · 원장 상태 OOB(+ `X-Day-Version`) / 충돌 409 `chart_conflict` = **아무것도 저장 안 함** · 같은 탭 조각을 다시 그림 — 걸린 줄 = `conflicts[]`(`body` = 지금 글 + 줄바꿈 + 요청 글 · `staffId` = KOS 값(간호관리는 요청 그대로) · `base` = KOS 지금 값 · `baseLogId` = 지금) · "
      "보낸 안 걸린 줄 = 요청 그대로(바뀐 줄로 남음) · 보내지 않은 줄 = 지금 DAY 값 + 토스트 조각(글자 = SPEC OQ-90 · 비어 있으면 코디에게 물음 — 짓지 않음) / "
      "그 밖 오류 = 지금 오류 토스트 조각(409 `chart_staff_required` · `staff_not_listed` · `doctor_not_listed` · 400 `invalid_request` · 404 `not_found`)")
K4 = ("계약 K4(사진 — #② 제공 · #③ 소비): `GET /board/visits/{visit_id}/photos` → 조각 `partials/board_photos.html`(이름 제안) · 값 `photos` = "
      "`{visit_id, edit(board edit 여부), groups: [{category: before | after, title: 「시술 전」 | 「시술 후」, items: [{image_id(KOS 사진 id), thumb(data: URI — 서버가 받아 실음 · W3), shot_at}]}]}` · "
      "`POST /board/visits/{visit_id}/photos`(multipart `category` · `file` 1장) · `POST /board/visits/{visit_id}/photos/{image_id}/delete` → 성공 = 같은 조각 · 실패 = 오류 토스트 조각 "
      "(400 `invalid_request` · 404 `not_found` · 409 `photo_code_missing` · 401 `session_expired` · 503 `kos_unavailable`) · `GET …/photos/{image_id}/original` → 그림 바이트(`Cache-Control: no-store`) · "
      "썸네일 경로 없음(SPEC-002 §3 API — `…/thumb` 취소선)")
K5 = ("계약 K5(옛 경로 정리 — #① 지움 · #③ 지움): 옛 `POST /board/tasks/{task_id}/chart`(`routers/board.py:433`) · `POST /api/tasks/{task_id}/chart`(`routers/api/board.py:267`) · "
      "`partials/board_chart_saved.html` 은 지운다 — 앱(`app/`)은 차트 경로를 부르지 않는다(grep 0 · SPEC-002 API W8). 라우트 · 서비스 쪽은 #①, 템플릿 · day.js 쪽은 #③")
E2E_ORDER = "순서 조건: 실물 e2e 는 #① · #② · #③ 이 모두 들어간 로컬에서 마지막으로 머지되는 Issue 가 1회 돌리고 결과를 세 Issue 에 남긴다"
E2E = ("실물 e2e 1회(로컬 · KOS 데모 지점 · 시험 고객): ⓐ 간호관리차트 여러 줄 쓰고 [저장] → 「최근 저장」 바뀜 · KOS 웹 그 작업 간호관리 메모 = 쓴 글 · 의사차트 탭 따로 저장 "
       "ⓑ 충돌 — 창을 연 뒤 KOS 웹에서 같은 줄 메모를 먼저 고치고 [저장] → 409 · 아무 줄도 저장 안 됨 · 그 줄 칸 = KOS 글 + 줄바꿈 + 내 글 · 다시 [저장] → 저장 · KOS = 이어 붙인 글 "
       "ⓒ 사진 — 「시술 전」 · 「시술 후」에 1장씩 올림 → KOS 웹 그 일정 사진 탭에 보임(분류 · 장비 「태블릿」 · 메모 「{고객 이름} 고객 시술 전 / 후」) · 1장 삭제 → KOS 사진 탭에서 사라짐 "
       "ⓓ 미저장 상태로 ✕ → 확인 창 · 「버리고 닫기」 → 저장 요청 0. " + E2E_ORDER)

reqs = {
"be-chart": {
  "title": "DAY 차트 명시적 저장 ① 백엔드 — 탭 저장 · 저장 전 KOS 확인(C17) · 옛 줄 저장 정리 (DAY-SPEC-002 개정 ㉘)",
  "target_specs": ["DAY-SPEC-002"],
  "target_delta": [
    "차트 탭 저장 `POST /board/visits/{visit_id}/chart` — 한 방문 × 한 차트 종류의 바뀐 줄(`rows[]`) · 방문 잠금 한 번 · DB transaction 한 번(규칙 31 · C6)",
    "검사 순서 = 401 → 403 → 400 → 404 → KOS 지금 값 읽기(transaction 밖 · `KosAdapter.fetch_visit_tasks` = `get-schedule-detail` · 시스템 계정 읽기 · 요청당 1회) → 줄마다 충돌(DAY `baseLogId` · KOS 지금 값 vs 요청 `baseBody` · `baseDoctorStaffId`) → 담당자 → 그대로인 줄 건너뜀 → 저장(SPEC-002 매트릭스 「차트 탭 저장 검사 순서」)",
    "충돌(C17) = 한 줄이라도 걸리면 탭 전체 저장 안 함(이력 · outbox · `event_log` 0) · 걸린 줄 = 지금 글 + 줄바꿈 + 요청 글 · 담당자 KOS 값 · 판정 대상 = 요청 `rows[]` 줄만 · 시술 전 의사차트 · 반영 대기 줄은 KOS 판정 안 함 · KOS 읽기 실패 = DAY `baseLogId` 만으로 · 길이 검사 없음(한도 정해질 때까지 · OQ-90 ⓒ)",
    "저장 = 줄마다 이력 1행 · DAY 값 · outbox(앞 판 그대로) · `event_log` 요청당 1행 `visit.chart_save`(제안) · 모든 줄 intent 를 그 event 하나에 묶음(`_queue`) · 규칙 27 `task.doctor_change` 는 줄마다 그대로(W1) · 시술 전 의사차트 결정 (가) 그대로",
    "차트 열기 값에 `base` 더함(계약 K1)",
    K1, K2, K3, K5,
  ],
  "acceptance": [
    "A1: 탭 저장이 계약 K2 를 받고 계약 K3 모양으로 응답한다 — 저장됨 200 · 충돌 409(저장 0 · 이어 붙인 칸 · `base` · `baseLogId` 갱신) · 담당자 409 · 형식 400 · 404",
    "A2: C17 판정을 테스트로 막는다 — KOS 값이 연 때와 다름 → 409 · 탭 전체 0행 · DAY `baseLogId` 다름 → 409 · KOS 읽기 실패 → DAY 검사만으로 저장 · 시술 전 의사차트 줄 · 반영 대기 줄은 KOS 판정 안 함 · 보내지 않은 줄은 판정 안 함 · 다시 저장(갱신된 base) → 저장",
    "A3: KOS 읽기가 DB transaction 밖에서 요청당 1회만 일어난다(테스트 · 호출 수)",
    "A4: 저장된 요청 = `event_log` `visit.chart_save` 1행 + 수락 · 진행중 집도의 변경 줄마다 `task.doctor_change` · outbox 는 그 event 에 묶이고 줄 순서대로 · 바뀐 것 없는 줄은 이력 · op 0",
    "A5: 옛 `POST /board/tasks/{task_id}/chart` · `POST /api/tasks/{task_id}/chart` 가 없다(라우트 · 테스트 정리)",
    "A6: " + E2E,
  ],
  "non_goals": ["템플릿 · day.js · 화면(Delivery ③)", "시술전후사진(Delivery ②)", "직원 앱 차트(C15)", "편집 · 보기 권한 변경(C7)", "새 테이블 · 칸 · migration", "글자 한도 · 화면 글자(OQ-90)"],
  "review_surface": [SRC, "C17 충돌 판정 · 연 때 값(`base`) 비교가 SPEC-002 규칙 31 과 같은지", "KOS 읽기가 transaction 밖인지(DAY-SPEC-000 데이터 규칙)", "event · outbox 묶음(W1)"],
  "execution": {
    "code_surface": [
      "backend/day/services/board_charts.py(save_chart → 탭 저장)",
      "backend/day/services/board_chart_writes.py",
      "backend/day/policies/board_chart_rules.py",
      "backend/day/presentation/board_chart_reads.py(`base`)",
      "backend/day/dtos/board_charts.py · dtos/board_actions.py",
      "backend/day/emr/kos/__init__.py(fetch_visit_tasks 재사용)",
      "backend/day/routers/board.py(차트 저장 라우트 · 옛 경로 지움)",
      "backend/day/routers/api/board.py(옛 JSON 경로 지움)",
      "backend/tests/day/board/test_board_chart_api.py · test_chart_*.py"
    ],
    "domain_candidates": ["visit_task_chart_log · visit_task(assignee_note · doctor_note) · visit_task_staff(doctor) · external_outbox · event_log"],
    "dependencies": ["③ — 계약 K1 · K2 · K3 · K5 만 맞추면 병렬", "실물 e2e 는 ① · ② · ③ 뒤"],
    "phases": ["P1 탭 저장 service(검사 순서 · 충돌 · 저장 묶음)", "P2 KOS 확인(transaction 밖) · 실패 갈래", "P3 라우트 · 응답 조각 값 · `base`", "P4 옛 경로 정리 · 테스트 · 실물 e2e"],
    "verification": ["backend pytest(탭 저장 · C17 · event/outbox · 옛 경로 404)", "실물 e2e(로컬 · KOS 데모)"],
    "predeploy": [],
    "rollback": ["Code PR revert — migration 없음 · 웹 화면(③)과 같이 되돌린다(옛 경로를 지우므로 한쪽만 되돌리면 저장이 깨짐)"],
    "open_questions": ["OQ-90(충돌 토스트 · 길이 한도) · OQ-91(C17 세부 기본값) — SPEC-002 §5"],
  },
},
"be-photo": {
  "title": "DAY 차트 시술전후사진 ② 백엔드 — KOS 내부 이미지 · 직원 토큰 · 서버 경유 (DAY-SPEC-002 개정 ㉘)",
  "target_specs": ["DAY-SPEC-002"],
  "target_delta": [
    "사진 목록 · 올리기 · 삭제 · 원본 — 계약 K4 · 규칙 39 · §3 「KOS 사진 — 직접 호출」(내부 경로 · 직원 토큰 · 쓰기 큐 안 씀 · DAY 저장 없음 · C8 ~ C14)",
    "목록 = `get-visitor-images {visitorId, scheduleId, deleted:false}` → 분류 이름 「시술 전」 · 「시술 후」 두 묶음 → 썸네일 `generate-signed-urls-with-param` 1회 → 서버 GET → `data:` 로 조각에 실음(W3 · 캐시 없음)",
    "올리기 = `get-codes` IMAGE_CATEGORY · IMAGE_EQUIPMENT 이름 매칭(「시술 전」 · 「시술 후」 · 「태블릿」 — 못 찾으면 409 `photo_code_missing` · 아무것도 안 올림) → `generate-presigned-url` → S3 `PUT` → `register-visitor-images`(fileName · visitorId · source HOSPITAL · equipment · scheduleId · shootingDateTimeUtc · memo 「{고객 이름} 고객 시술 전 / 후」 · category) → 목록 다시",
    "삭제 = 목록(그 방문에 그 id) → `delete-visitor-images {ids}` → 목록 다시",
    "토큰 = 그 요청 세션 직원 KOS 토큰 · 없음 · KOS 401 = 401 `session_expired`(공지 저장 코드와 같게) · 그 밖 KOS 실패 · 연결 없음 = 503 `kos_unavailable`(W2)",
    "KOS 호출 동안 DB transaction 을 열지 않음 → 결과 뒤 `event_log` 1행 따로 커밋(`photo.upload` · `photo.delete` · 실패 `kos_rejected` 꼴 — 파일 이름 · 그림 · 서명 주소 · 토큰은 싣지 않음 · W4 · 규칙 39 ⑤ ⑥)",
    K4,
  ],
  "acceptance": [
    "A1: 네 경로가 계약 K4 모양으로 응답하고 권한(보기 = `board` view · 올리기 · 삭제 = `board` edit)을 지킨다",
    "A2: KOS 호출이 §3 「KOS 사진」 표 순서 · 칸과 같다(가짜 KOS 테스트 — 등록 칸 · 메모 · 분류 · 장비 객체 통째 · scheduleId · 목록 1 + 서명 1 + 썸네일 GET N)",
    "A3: 매트릭스 사진 줄(404 · 400 · 409 `photo_code_missing` · 401 `session_expired` · 503)을 테스트로 덮는다 · 시스템 계정 토큰으로 대신 보내지 않음",
    "A4: KOS 호출 동안 열린 DB transaction 이 없고 `event_log` 가 따로 1행 · payload 에 파일 이름 · 서명 주소 · 토큰이 없다(테스트)",
    "A5: DAY DB · Blob · 임시 파일에 사진을 두지 않는다(새 테이블 · 칸 0 · 파일 쓰기 0)",
    "A6: " + E2E,
  ],
  "non_goals": ["사진 탭 화면 · 시안 · 글자(Delivery ③ · OQ-88)", "여러 장 · 크기 · 형식 한도(OQ-86)", "분류 · 장비 코드 테이블(C13)", "직원 앱(C15)", "공개 `generate-uploading-url` 경로(C10 — 병원 공개 키 토큰)"],
  "review_surface": [SRC, "직원 토큰 · 내부 경로(C10) · KOS 쓰기가 쓰기 큐 밖 직접 호출인 것(규칙 39 ⑤)", "고객 이름이 든 fileName 이 로그 · event 에 남지 않는지", "S3 PUT 뒤 등록 실패 파일은 남음(감수 · OQ-89 ⓓ)"],
  "execution": {
    "code_surface": [
      "backend/day/emr/kos/images.py(새 — 내부 이미지 경로 · 직원 토큰 · S3 PUT)",
      "backend/day/emr/kos/staff_client.py(직원 토큰 헤더 꼴 재사용)",
      "backend/day/emr/base.py(어댑터 메서드)",
      "backend/day/services/board_photos.py(새)",
      "backend/day/presentation/board_photos.py(새 — 조각 값)",
      "backend/day/routers/board_photos.py(새 · 화면 라우트)",
      "backend/tests/day/board/test_board_photos*.py(새) · backend/day/emr/kos/demo(가짜 KOS 보충)"
    ],
    "domain_candidates": ["없음(DAY 테이블 없음) — customer · visit external_ref · external_session(직원 토큰) 읽기 · event_log 쓰기"],
    "dependencies": ["③ — 계약 K4 만 맞추면 병렬", "① 과 서로 독립", "실물 e2e 는 ① · ② · ③ 뒤"],
    "phases": ["P1 KOS 이미지 어댑터(7단계 · 직원 토큰)", "P2 service(이름 매칭 · 목록 확인 · transaction 밖 · event)", "P3 라우트 · 조각 값 · 원본 바이트", "P4 테스트 · 실물 e2e"],
    "verification": ["backend pytest(가짜 KOS · 매트릭스 · transaction · event payload)", "실물 e2e(로컬 · KOS 데모 · KOS 웹 일정 사진 탭 눈 확인)"],
    "predeploy": ["데모 실물 1회 — 직원 토큰 + DAY 서버 UA 로 내부 이미지 경로가 받아지는지(OQ-89 ⓐ)"],
    "rollback": ["Code PR revert — migration 없음 · KOS 에 올린 시험 사진은 남음(시험 고객만)"],
    "open_questions": ["OQ-85 · 86 · 87 · 89 · 92 — SPEC-002 §5"],
  },
},
"fe": {
  "title": "DAY 차트 명시적 저장 · 시술전후사진 ③ 화면 — 모달 탭 · [저장] · 확인 창 · 사진 탭 · 헤더 로그인 표시 (DAY-SPEC-002 개정 ㉘ · DAY-SPEC-001 개정 ⑫)",
  "target_specs": ["DAY-SPEC-002", "DAY-SPEC-001"],
  "target_delta": [
    "차트 모달(E55) 탭 셋 [간호관리차트] | [의사차트] | [시술전후사진](C1) · 탭 줄 오른쪽 끝 [저장](E57 · 차트 탭만 · 바뀐 줄 있을 때만 켜짐 · 보내는 동안 꺼짐 · 보기 권한 숨김) · 그 바로 왼쪽 「최근 저장 : HH:MM」(E58 · 탭마다 · W9) — U-14",
    "자동 저장 JS(칸 나갈 때 · 2초 · 줄 저장 · 실패 「다시 시도」 · 「저장하지 않고 닫기」) 걷어냄 · 탭 저장 폼(계약 K2 — 바뀐 줄만)",
    "미저장 닫기 확인 창(E59) — ✕ · Escape = 확인 창 · 바깥 누르기 = 아무 일 없음 · 글자 = 기획 4-2 「저장하지 않고 닫을까요?」 · 「계속 쓰기」 · 「버리고 닫기」(OQ-79 기본값) · 탭 옮겨도 쓴 것 남음(OQ-82)",
    "충돌 응답(계약 K3) 그리기 — 걸린 줄 칸 = 이어 붙인 글 · 담당자 · 다음 저장용 `base` · `baseLogId` 숨은 칸 갱신 · 토스트",
    "시술전후사진 탭(U-16) — 탭을 누를 때 `GET …/photos` 조각 · 두 묶음 · 올리기 · 삭제 · 원본 열기 · 보기 권한이면 올리기 · 삭제 숨김 · **시안 전이라 구조만 · 글자 OQ-88 비움(짓지 않음)**",
    "웹 헤더 로그아웃 왼쪽 로그인한 사람(DAY-SPEC-001 U-3 · C16) — 렌더 공통 값(`web.render`)에 세션 직원 표시 값 · 모양은 OQ-K21 답대로(답 전엔 자리만 · 코디 확인)",
    "옛 줄 저장 조각 `partials/board_chart_saved.html` 지움(계약 K5) · 코드 레포 `.agents/skills/verify-day-web/features/clinical-chart.md` 를 명시적 저장 · 충돌 · 사진 탭으로 갱신(「별도 저장 버튼은 없다」 등)",
    K1, K2, K3, K4, K5,
  ],
  "acceptance": [
    "A1: 모달이 U-14 · U-16 대로 그려진다 — 탭 셋 · [저장] 자리 · 켜짐 조건 · 「최근 저장」 자리 · 탭마다 값 · 사진 탭에는 [저장] 없음",
    "A2: 자동 저장이 없다 — 칸을 나가거나 멈춰도 요청 0 · [저장] 한 번 = 요청 1(바뀐 줄만 · 계약 K2)",
    "A3: 미저장 ✕ · Escape → 확인 창 · 바깥 → 아무 일 없음 · 「계속 쓰기」 = 그대로 · 「버리고 닫기」 = 닫힘 · 요청 0 · 미저장 없으면 바로 닫힘",
    "A4: 409 `chart_conflict` 응답으로 걸린 줄 칸이 이어 붙인 글로 바뀌고 다시 [저장]이 갱신된 `base` · `baseLogId` 를 보낸다",
    "A5: 사진 탭이 계약 K4 조각을 그리고 올리기 · 삭제 · 원본 열기가 동작 · CSP(인라인 스크립트 0 · `img-src 'self' data:`) · medikit 만 · 짓는 글자 0",
    "A6: 헤더 로그인 표시가 모든 세션 화면에 보인다(OQ-K21 답대로)",
    "A7: verify-day-web 차트 기능 문서가 새 동작과 맞다",
    "A8: " + E2E,
  ],
  "non_goals": ["탭 저장 · 사진 서버 로직(Delivery ① · ②)", "직원 앱(C15)", "사진 탭 시안 · 글자(디자이너 · OQ-88)", "확인 창 외 화면 글자 짓기", "권한 변경(C7)"],
  "review_surface": [SRC, "자동 저장이 남지 않았는지", "확인 창 글자 = 기획 4-2 글자(OQ-79 사용자 확인 전)", "사진 탭 글자를 짓지 않았는지", "헤더 표시 모양(OQ-K21)"],
  "execution": {
    "code_surface": [
      "backend/day/templates/partials/board_chart.html · board_chart_parts.html · board_chart_saved.html(지움) · board_chart_tab.html(새 · 이름 제안)",
      "backend/day/templates/partials/board_photos.html(새 · 이름 제안)",
      "backend/day/templates/base.html(헤더 day-header__tools)",
      "backend/day/web.py(render 공통 값 — 헤더 표시)",
      "backend/day/static/day.js(자동 저장 걷어냄 · 탭 저장 · 확인 창 · 사진 탭)",
      "backend/day/styles/app.css(medikit 토큰만)",
      "backend/tests/day/web/test_board_page_chart*.py · scripts/frontend/tests/chart-*.test.mjs · scripts/frontend/bombadil/chart*.mjs",
      ".agents/skills/verify-day-web/features/clinical-chart.md"
    ],
    "domain_candidates": [],
    "dependencies": ["① — 계약 K1 · K2 · K3 · K5(가짜 응답으로 병렬)", "② — 계약 K4(가짜 조각으로 병렬)", "실물 e2e 는 ① · ② · ③ 뒤"],
    "phases": ["P1 탭 셋 · [저장] · 「최근 저장」 · 자동 저장 걷어냄", "P2 미저장 확인 창 · 충돌 그리기", "P3 사진 탭(구조) · 헤더 표시", "P4 테스트 · verify-day-web 문서 · 실물 e2e"],
    "verification": ["backend pytest(web 조각)", "frontend node 테스트(scripts/frontend/tests)", "verify-day-web 차트 기능 실행", "실물 e2e(로컬 · KOS 데모)"],
    "predeploy": [],
    "rollback": ["Code PR revert — ① 과 같이 되돌린다(계약 K5)"],
    "open_questions": ["OQ-79 · 80 · 81 · 82 · 87 · 88 · 90 — SPEC-002 §5 · OQ-K21 — SPEC-001 §5"],
  },
},
}

for key, r in reqs.items():
    body = {
        "product_id": "day",
        "document_root": "products/day",
        "contract_version": 1,
        "target_specs": r["target_specs"],
        "spec_baseline_revision": BASE,
        "idempotency_key": f"day/day-spec-002-r28/{key}",
        "title": r["title"],
        "risk_level": "L2",
        "target_delta": r["target_delta"],
        "acceptance": r["acceptance"],
        "non_goals": r["non_goals"],
        "review_surface": r["review_surface"],
        "execution": r["execution"],
    }
    (OUT / f"request-{key}.json").write_text(json.dumps(body, ensure_ascii=False, indent=2))
    print("wrote", key)
