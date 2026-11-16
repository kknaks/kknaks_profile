# [backend] 수정 1판 — 리뷰 WARN 34건 문구 수정

너는 cc-prototype `backend` 워커다. 맥락은 파일에 있다 — 아래를 순서대로 읽어라.

1. 원 브리프(계약 · 제약 그대로 유효): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/api-swagger-docs-be-brief.md`
2. 네 1판 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/be-report.md`
3. 리뷰 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/review-report.md` — 판정 WARN(FAIL 0 · WARN 34 · 동작 불변 PASS)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` (네 1판 변경이 미커밋으로 있다 — 그 위에 고친다)

## 할 일

**WARN 34건 전부**를 「코드가 하는 것」 칸대로 설명 문구를 고친다. 리뷰어가 코드 근거(파일:줄)를 달아 두었다 — 고치기 전에 그 근거를 직접 열어 확인하고, 리뷰어가 틀렸다고 보면 고치지 말고 리포트에 이유를 적는다.

- 우선 4건(외부 호출자가 실제로 걸리는 자리)은 **눈에 띄게** 쓴다:
  - W-R2: 예약 · 고객 생성 502 중 KOS 쓰기가 **이미 된 뒤** 나는 것 → 「재시도하면 중복될 수 있음 · 먼저 조회로 확인」
  - W-C3: `since` 에 `updatedAt` 을 넣을 때 URL 인코딩 필요(`+` → `%2B`)
  - W-C2: 지운 메시지 = `deletedAt` 값 있음 · text · photo · video 가 null
  - W-R1: 5초 유지는 상세 GET 단건 재조회만 — 판 · 배경 재읽기는 KOS 값으로 덮을 수 있음
- 「나지 않는 코드」(W-P4 · W-D1)는 응답 표에서 뺀다
- W-R9e · W-Q1(코드 근거 약한 풀이)은 풀이를 빼고 중립 서술로
- 조용히 통과하는 자리 2: **오류 표 회귀 시험 추가** — `require_login` op ↔ 401 표, `require_real_board` op ↔ 403 `fake_board` 표가 일치하는지 `tests/test_openapi_docs.py` 에 고정

## 제약 (원 브리프 §7 그대로)

- 동작 변경 금지(설명 · responses 표 · 시험만). be 리포트 §7 버그는 이번에도 고치지 않는다
- allowed_paths = `procedure/back/` 만 · 커밋 · push 금지 · 서버 띄우지 않기

## 검증 · 보고

- `procedure/back` 에서 `uv run pytest -q` · `uv run ruff check .` 각 1회
- `openapi-after.json` 을 다시 덤프해 같은 폴더에 덮어쓰고, before 와의 구조 비교(1판과 같은 스크립트)를 다시 돌려 PROBLEMS 0 을 확인
- `be-report.md` 맨 아래에 「## 수정 1판」 절을 **덧붙인다**: W 번호별 처리(고침 · 안 고침+이유) 표 · 수치 · 구조 비교 결과
- 완료 보고는 원 브리프 §9 와 같은 두 채널(이번 dispatch 의 taskId · dispatchId 로)
