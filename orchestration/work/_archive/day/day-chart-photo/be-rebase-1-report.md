# day-chart-photo backend rebase 1 — origin/dev(#274 `fed616a8`) 위로 · migration 0025

## 상태: done (전체 check.sh 녹색)

- 브랜치 `kknaksss/day-chart-photo` · **새 HEAD = `d38d3c92`**(커밋 하나 · 부모 `fed616a8` = origin/dev #274) · 옛 `7e7cb368`(base `4bf0b4a1`)
- push 안 함 · 스택(11040 · docker 스택 · .run) · `deploy/*.env` 안 건드림

## 충돌 처리(9)
| 파일 | 처리 |
|---|---|
| `backend/day/main.py` | 두 import(`customer_router` · `board_photos_router`) 다 살림 — 라우터 목록은 자동 병합으로 둘 다 들어 있음 |
| `backend/day/web.py` | dev 의 `htmx`(fragment · HX-Boosted) · `header_tabs("customer"…)` · `active_menu` 그대로 + 우리 `header_staff` 한 줄 |
| `backend/day/templates/base.html` | dev `#customer-chart-root` + 우리 토스트 `popover="manual"`(모달 층 · e2e 2회차 F1) |
| `backend/day/templates/partials/board_chart_parts.html` | dev 의 「고객 차트」 버튼 살림 · 머리의 옛 `saved_at(chart.visitId, last_saved(chart))` 는 뺌(우리 판에서 탭마다 「최근 저장」으로 옮김 — 같은 파일 `saved_at(… kind …)`) |
| `backend/day/static/day.css` | 손으로 안 합침 — `app.css`(자동 병합 · 충돌 0) 뒤 `./scripts/build-css.sh` 로 다시 빌드(109.5KB) |
| `backend/tests/day/test_column_snapshot.py` | `customer_memo` · `visit_photo` 두 스냅샷 다 |
| `backend/tests/day/test_models.py` | `{"partner_outbox", "customer_memo"}` · `COMPANION_TABLES` · `PHOTO_TABLES` 다 |
| `backend/tests/migrations/test_alembic.py` | `HEAD = "0025_visit_photo"` |
| `scripts/frontend/tests/fixtures/reservations-page.html` | 생성물 — `DAY_UPDATE_FIXTURES=1` 로 그 시험을 돌려 다시 씀(1줄 차이) |

- 자동 병합 확인: `error_codes.py` 코드 108 · 값/이름 중복 0 · `identifiers.py` · `models/__init__.py` · `routers/board.py` · `tasks/__init__.py` · `day.js` · `app.css` · `icons.html` — 충돌 표시 0 · 두 쪽 다 살아 있음(전체 검사로 확인)
- `test_screen_copy.py`(자동 병합) — 우리 쪽이 자동 저장 글자를 지우며 뺀 「저장하지 못했어요. 다시 시도해 주세요.」를 #274 고객 차트 메모(`cc-form-message`)가 쓰므로 근거 표에 되살림

## migration 번호
- dev `20261124_0024_customer_memo`(down `0023_companion_permission`) 뒤로 — 우리 `0024_visit_photo` → **`0025_visit_photo`**
  - 파일 `20261124_0025_visit_photo.py` · `revision = "0025_visit_photo"` · `down_revision = "0024_customer_memo"` · docstring(Revision ID · Revises)
  - 함께: `test_visit_photo_migration.py`(경로 · revision · 시험 이름 · downgrade 대상 `0024_customer_memo`) · `test_alembic` HEAD · `test_column_snapshot` · `test_enum_labels` 주석
- `alembic heads` = **`0025_visit_photo (head)` 하나** · 옛 이름 남은 곳 0

## KOS 경로 확인(#274 KOS 조회 워커 전환)
- `build_adapter(` 전수: `emr/factory.py` 안(캐시가 만드는 자리) · `services/visit_photo_kos.py`(사진 — 직원 토큰) · `services/reservation_notice.py`(공지 저장 — 직원 토큰) 뿐. **#274 가 새로 만든 KOS 클라이언트 생성 경로는 없다** — `services/ext_refresh.py` 는 작업을 넣기만 하고, 워커 `tasks/ext_refresh.py` → `services/ext_sync.py` 가 `adapter_for`(병원별 캐시)를 부른다 → 같은 공유 시스템 토큰(C35)을 쓴다.
- 고친 것(최소 · 아래 검사 때문): `ext_sync` · `emr_sync` · `board_charts` 가 `day.bootstrap.kos_tokens.shared_adapter_for`(= `adapter_for` + 공유 토큰 저장소)를 쓰게 — 이름은 `adapter_for` 로 그대로 import 해 시험 · #274 코드의 monkeypatch 자리는 안 바뀜

## 전체 check.sh 에서 드러나 고친 것(우리 커밋이 원래 갖고 있던 Taut 규칙 위반 13 · rebase 탓 아님)
- `ChartRowInput` → **`ChartRowData`**(DTO 이름 규칙 DTO002)
- C35 토큰 저장소: Redis · 암호화 구현을 `emr/kos/token_store.py`(adapter 역할 — crypto · redis import 금지 ARCH001) → **`day/bootstrap/kos_tokens.py`** 로 · 값 · Protocol(`SystemToken` · `SystemTokenStore` · `TokenKind`)은 `emr/base.py` · 키 자격 표시는 `emr/factory.system_token_tag`(emr 밖은 `emr.kos.*` 를 import 하지 않는다는 구조 시험) · `build_adapter`/`adapter_for` 에 `token_store` 인자
- `taut.toml` `[tool.taut.enum].shared_modules` 에 `day.enums.photo`(ENUM001)
- `ChartStaffRejected` 클래스 코드 `STAFF_NOT_LISTED`(EXC001)
- 사진 탭 GET 의 `session.rollback()` 을 라우터에서 서비스 `visit_photos.open_tab` 으로(TX001)
- 사진 올리기 · 삭제 · 다시 시도 라우트 docstring(API001)
- `test_kos_shared_token.py` open 토큰 시험 = 가짜 KOS transport 로(raw `httpx.AsyncClient` 안 씀 · TEST002)
- `scripts/devtools/verification_concurrency.py` 차트 읽기 = 응답 상태 · `json.loads`(CAT001)
- 정형 결속 `source-map.json` — `save_chart_tab` · `judge_row` · `day_differs` 해시(이름만 바뀐 `ChartRowData` 타입 표기 · 논리 변경 없음)

## 검증 — `./scripts/check.sh`(마감 전 전체 1회 · 마지막 실행)
- **녹색** — `All requested checks passed; evidence: .local/checks/20261124-184102-56786`
- 백엔드 시험 **2746 passed** · Structure · Jinja 623 sources · ruff · format · mypy · Taut audit/check · frontend(ESLint · Stylelint · Prettier · node 시험 · CSS 재현) 통과
- 앞선 두 번(Taut 13 · 정형 해시 3)은 위 고침으로 풀었다

## 주의
- 템플릿 충돌 두 곳(`base.html` · `board_chart_parts.html`)은 frontend 파일이지만 rebase 라 풀었다 — frontend 가 고객 차트 버튼 자리 · 토스트 층을 한 번 볼 것.
