# be-5 — 시술 현황 보기 = 모든 직군(DAY-SPEC-002 개정 ⑲ · SPEC-001 규칙 9)

워크트리 `prod-deploy-re1` · 커밋 안 함(변경만 남김). 근거: review-doc-9-report.md(재리뷰 PASS) · #245 v6 R1 · A11.

## 고친 것 — `backend/day/services/default_permissions.py` 한 파일

- 판정 ③ 「그 밖은 없음」 → **「그 밖은 보기」**(`board` view). 이름 표에 없고 태그가 없거나 보기 태그만 있는
  직무가 모두 보기다. 어느 갈래(이름 표 · 태그 · 그 밖)든 기본값에 보기가 있다.
- 이름 표 경영지원 · 마케팅 · CS팀(콜센터) = `none` → **`view`**. 줄은 남겼다(빼면 태그 `admin` 으로
  수정 · 수락까지 열린다 — 주석으로 적음). 상담총괄실장 = 보기 · 마취과 = 전부는 그대로.
- `board` edit · `board.accept` edit 은 직군별 그대로(태그 `nurse` · `skincare` · `doctor` · `admin` → 전부).
- 이제 「없음」 갈래가 없으므로 `Grant` 에서 `"none"` 과 `ROWS["none"]`, 쓰지 않게 된 `VIEW_TAGS` 를 뺐다.
  (보기 태그 → 보기는 ③ 과 같은 결과라 따로 둘 이유가 없다.) docstring 표도 맞췄다.
- 시드(`seed`)는 그대로 — 없는 (직무, 키) 행만 넣고(`ON CONFLICT DO NOTHING`) 사람이 고친 행 · 지운 행은
  되살리지 않는다.
- migration · 권한 검사 코드(`sessions.require_permission` · 라우터) · 다른 화면은 건드리지 않았다.

효과: 옛 표 「없음」 직무(CS팀 · 경영지원 · 마케팅 · 촬영팀 · 이름 표에 없고 태그 없는 직무)는 `board` 행이 없으니
다음 기준 정보 동기화 회차가 `board` view 를 넣는다. 사람이 지운 `board` 행이 있는 직무는 그대로 막힌다.

## 시험

- `tests/day/test_default_permissions.py`(DB 없음):
  - 데모 직무 15개 표 — CS팀(콜센터) · 경영지원 · 마케팅 · 촬영팀 = 보기, 나머지 줄 그대로.
  - `grant_of("총무", ()) == "view"`(이름 표에 없고 태그 없음).
  - 새 `test_모든_직무는_보기가_있고_수정_수락은_그대로`: 15개 모두 `board` 있음 · `board.accept` 는 전부 줄만.
    네 갈래 — 마취과 = 전부 · 경영지원/마케팅(태그 admin) = 보기만 · 태그 coordinator = 보기 · 태그 없음 = 보기.
- 새 `tests/day/board/test_board_default_view.py`(infra · 앱 전체):
  - `test_시드_뒤_보기만_직무는_판_200_수정_수락_403`: 로그인 직원 직무를 「경영지원」(태그 admin) · 권한 행 없음 →
    시드 전 `GET /api/board` 403 → 시드 → 행 = `board` view 하나 · 판 200 · 마취 시작(수정) 403 `forbidden` ·
    호출 수락 403 `forbidden`.
  - `test_시드는_있는_edit_행과_지운_행을_그대로_둔다`: 사람이 올린 코디 `board` edit 은 edit 그대로 · 지운 촬영팀
    `board` 행은 지운 채(되살림 · 새 행 없음) · 간호 · 원장 = 전부 · 두 번째 시드는 0행 · 행 그대로.
- 기존 `test_emr_sync_service.py::test_기준_정보_회차가_직무_기본_권한을_채우고_고친_행은_두다` 는 고치지 않고 통과.
- 음성 확인: 옛 모듈로 돌리면 위 4개(표 3 · 시드 뒤 200/403 1)가 실패한다. 「그대로 둔다」 시험은 바뀌지 않은
  동작이라 옛 모듈에서도 통과한다. 확인 뒤 새 모듈로 되돌렸다.

검증: 격리 스택(`day-be245`)에서 관련 파일만 1회 — test_default_permissions · test_board_default_view ·
test_emr_sync_service · test_board_api · test_board_sse · tests/architecture → **109 passed**.
`uv run ruff check backend` 통과 · 바꾼 파일 format 통과 · 스택 `down -v`. 11040 · `day-local` · dev/prod 서버 · DB 는
건드리지 않았다.

## 워크트리 변경(커밋 안 함)

- `backend/day/services/default_permissions.py`
- `backend/tests/day/test_default_permissions.py`
- `backend/tests/day/board/test_board_default_view.py`(새 파일)
