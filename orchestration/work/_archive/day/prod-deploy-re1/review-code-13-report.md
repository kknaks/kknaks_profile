# 리뷰 리포트 — prod-deploy-re1 / code 13 · BE-5 시술 현황 보기 = 모든 직군 (2026-11-12)

대상: 워크트리 미커밋 backend.
- `backend/day/services/default_permissions.py`(+11 −13)
- `backend/tests/day/test_default_permissions.py`
- 새 `backend/tests/day/board/test_board_default_view.py`(infra)

근거:
- be-5-report.md
- SPEC-002 개정 ⑲ §3 「권한 — 1차 기본」(#934 커밋 `9ddbebeb` · `:535-571`) · 케이스 매트릭스(`:628`)
- SPEC-001 규칙 9
- #245 v6 R1 · A11
- review-doc-9-report.md

## 판정: PASS

FAIL 0 · WARN 0 · 참고 3.

## 검증 (각 1회)

| 명령 | 결과 |
|---|---|
| 격리 스택(`day-rv13` · 127.0.0.1:11152/11153) + `scripts/test.sh` — test_default_permissions · test_board_default_view · test_emr_sync_service · test_board_api · test_board_sse · tests/architecture | **109 passed** (be-5 와 같은 수) |
| `uv run ruff check backend` · `ruff format --check`(세 파일) | 통과 |
| `git diff --stat HEAD -- backend/migrations backend/day/routers backend/day/session.py backend/day/services/sessions.py` | 비어 있음 |
| 스택 `down -v` 뒤 `docker ps` | day-local-* 다섯만 남음 — 11040 · day-local · dev/prod 손대지 않음 |

be-5 의 음성 확인(옛 모듈이면 4개 실패)은 다시 하지 않았다. 코드를 바꿀 수 없어서다.

## 볼 것 — 항목별

| 항목 | 판정 | 근거 |
|---|---|---|
| board view 기본값 = 모든 직무 | PASS | `grant_of`(`default_permissions.py:59-63`)의 끝 갈래가 `"none"` → `"view"` 다. `Grant` 에서 `"none"` · `ROWS["none"]` 이 빠졌다(`:34` · `:51-54`). 그래서 이름 표 · 태그 · 그 밖 어느 갈래도 `board` 행 없이 끝날 수 없다(타입으로 막힘). 스펙 :541 · :561 「③ 그 밖은 보기」와 같다 |
| edit · accept 는 옛 표 그대로 | PASS | `FULL_TAGS`(nurse · skincare · doctor · admin)와 `ROWS["full"]` 은 바뀌지 않았다. `VIEW_TAGS` 를 지운 것은 결과가 ③ 과 같아서다(보기 태그 → 보기). 데모 15직무 표에서 FULL 줄 11개 · VIEW 줄은 옛 표와 같고, 바뀐 것은 옛 NONE 네 줄 → VIEW 뿐이다(`test_default_permissions.py` diff) |
| 경영지원 · 마케팅 = 보기만 · 태그 admin 으로 안 열림 | PASS | 이름 표 `NAME_RULES`(`:43-49`)가 태그보다 먼저 판정하고 `"view"` 다. 줄을 남긴 이유 주석(`:41-42`)이 스펙 :563 과 같다. 단위 시험 `defaults_for("경영지원", ("admin",)) == VIEW`. infra 시험이 실제로 직무를 「경영지원」+태그 admin 으로 바꾸고 시드한다. 그러면 행 = `board` view 하나 · `GET /api/board` 200 · 마취 시작 403 `forbidden` · 수락 403 `forbidden` 이다 |
| 마취과 = 전부 | PASS | 이름 표 `"마취과": "full"` 그대로다. 단위 `defaults_for("마취과", ()) == FULL` · `grant_of(" 마취과 ", ())` 공백 무시도 그대로다. 상담총괄실장 = 보기 · CS팀(콜센터) = 보기도 스펙 이름 표(:553-559)와 같다 |
| 시드 「없는 행만 · 지운 행 안 되살림」 | PASS | `seed`(`:72-94`)는 바뀌지 않았다 — `ON CONFLICT (job_role_id, permission_key) DO NOTHING`. PK 가 지운 행도 잡으므로 되살리지 않는다. infra 시험: 사람이 올린 코디 edit 은 edit 그대로 · 지운 촬영팀 `board` 는 지운 채 · 간호 · 원장 = 전부 · 두 번째 시드 0행 · 행 그대로. 기존 `test_emr_sync_service` 의 「고친 행은 둔다」도 통과한다 |
| 권한 검사 · migration · 다른 화면 변경 없음 | PASS | 위 diff --stat 이 비어 있다. `sessions.require_permission` · 라우터 · 템플릿 · migration 은 바뀌지 않았다. 행 값만 바뀌고 검사 경로는 그대로다(SPEC-001 규칙 9 — 행 · level 로 판정) |
| 시험이 A11 을 판정 | PASS | A11 각 절이 시험에 대응한다. 「모든 직무 board view」 → `test_모든_직무는_보기가_있고_수정_수락은_그대로`. 「경영지원 · 마케팅 · CS팀 · 촬영팀 · 이름 표에 없고 태그 없는 직무 = 보기만」 → DEMO_ROLES 표 + `grant_of("총무", ())`. 「판 200 · 수정 · 수락 403」 → infra 시험 1. 「행 없던 직무는 다음 회차에 view」 → 시드 전 403 → 시드 → view 행(시드는 기준 정보 회차가 부름 · `emr_sync.py:169` · 기존 시험). 「edit 행 그대로 · 지운 행 안 되살림」 → infra 시험 2 |

## 참고

- 참고 1(번짐 — 통역): 통역 핸드셰이크가 같은 `board` view 로 판정한다(`services/interpret/service.py:150-152`). 그래서 이번 변경으로 옛 「없음」 직무(CS팀 · 경영지원 · 마케팅 · 촬영팀 등)도 앱 통역을 쓸 수 있게 된다. SPEC-003 「통역 = 시술 현황에서 그 고객 정보를 볼 수 있는 사람 모두」 규칙대로라 결함은 아니다. 다만 Soniox 사용량 · 개인정보 안내(통역) 대상이 넓어지는 효과라, 사용자에게 한 줄 알릴 만하다.
- 참고 2(배포 뒤 확인): 실물 효과는 다음 기준 정보 회차가 `board` view 를 넣은 뒤다. #245 verification.8 「배포 뒤 dev · prod board 행 없는 직무 0 을 개수로」는 이 리뷰 범위 밖이고 배포 뒤 코디 몫이다. 사람이 지운 `board` 행이 있는 직무는 계속 403 이 정상이다(스펙 :568). 그 직무는 개수에서 따로 셀 수 있게 「행 없음」과 「지운 행」을 나눠 세길 권한다.
- 참고 3(시험 공백 · 작음): 「지운 행 직무는 판 403」을 API 로 판정하는 시험은 없다(행 상태만 단언). 권한 검사 경로가 바뀌지 않았으므로 기존 매트릭스 시험이 덮는다고 본다.
