# kos-signin-limit fe-1 결과 보고 — 웹 기기 선택 단계(U-4)

## 상태: done (커밋 · push 안 함 — 워크트리 변경만)

## 수행 — 변경 파일
- `backend/day/routers/login.py`
  - `_outcome()` — `login` · `choose_device` 결과의 같은 갈래: `status == "choose_device"` → 기기 선택 조각 · `PendingLogin` → 병원 고르기 조각 · 그 밖 → 세션 쿠키 + 이동(`/board`).
  - `_device_card()` — 목록은 KOS 순서 그대로, 각 줄에 `minutes_ago` 를 화면이 계산(`_minutes_ago`: 분 내림 · 1분 미만/시계 어긋남 = 0 → 「방금 전」 · 60분 넘어도 「n분 전」(OQ-K5) · `signed_in_at=None` → 2줄 비움).
  - `POST /login/device` 신설 — 폼 `pending_token` · `device_id` → `auth.choose_device(session, deps, token, device_id)` → `_outcome`. `SessionExpired` → `/login?reason=session_expired`(일반 303 · HTMX 204 `HX-Redirect`), 그 밖 `ServiceError` → 오류 카드(로그인 폼). 빈 `device_id` 도 service 로 넘긴다(토큰 소모 · KOS 미호출은 service 몫). CSRF 없음(스펙).
- `backend/day/templates/partials/login_card.html` — `elif devices` 갈래(병원 고르기와 같은 카드 자리): 제목 · 안내 2줄(`<br>`) · 숨은 칸 `pending_token` 만 · 라디오 카드(`ui.radio` = medikit `ms-radio` · 1줄 `label · ip_address` · 2줄 상대 시각) · 첫 항목 `checked` · 버튼 「계속하기」(`ui.btn` primary l full) · 「처음으로」 없음.
- `backend/day/styles/app.css` — `.day-login__device*` 6줄(병원 고르기 줄 `.day-login__choice` 와 같은 테두리 카드 · medikit 토큰 변수만) → `scripts/build-css.sh` 로 `backend/day/static/day.css` 재생성(손 수정 없음).
- `backend/tests/architecture/test_screen_copy.py` — 근거 표 6줄 추가: 「이미 로그인 중인 기기가 있습니다」 · 안내 2줄 · 「방금 전」 · 「분 전」 · 「계속하기」(전부 SPEC-001 개정 ⑨ 「기기 선택 글자」).
- `backend/tests/day/web/test_login_device.py`(신규 · 13 함수 15 케이스).

## 검증
- `uv run pytest -q backend/tests/day/web/test_login_device.py backend/tests/day/web/test_login_page.py backend/tests/architecture/` → **52 passed**(기기 선택 15 포함). DB · Redis · KOS 없이(`db` · `auth_deps` override + `auth.login` · `auth.choose_device` monkeypatch).
- `uv run ruff check` · `ruff format --check`(바꾼 파일) → 통과.
- `scripts/build-css.sh` → day.css 56.2KB 재생성.
- grep: `login_card.html` 의 `<script` · `style="` = 0. day.js 수정 없음.
- 테스트 내용: HX 조각 · 전체 페이지 렌더 · 글자 6종 · 첫 항목만 checked · 이메일/비밀번호가 조각 · 숨은 칸 · 헤더(location) 어디에도 없음 · 「처음으로」 없음 · 계속하기 → 이동(204/303 + `day_session` 쿠키) · 병원 고르기 조각 · 다시 막히면 새 토큰 조각 · `SessionExpired` → `/login?reason=session_expired` · `kos_unavailable` / `invalid_credentials` → 오류 카드 · CSRF 없이 받음 · 상대 시각 계산 · 시각 None.
- 실행 안 함: infra 테스트 · 전체 스위트 · 실브라우저(로컬 스택 금지).

## 계약 대조 (§3)
| 항목 | 상태 |
|---|---|
| `login` 결과 `status="choose_device"` + `pending_token` · `expires_in_seconds` · `devices[{id,label,ip_address,signed_in_at}]` | 같음 — status 값으로 가름. 테스트는 backend 가 워크트리에 둔 실제 dto `PendingDeviceChoice` · `DeviceChoice`(`day/dtos/auth.py`) 로 만든다 |
| `auth.choose_device(session, deps, pending_token: str, device_id: str) -> LoginOutcome` | 같음 — 위치 인자 그대로 호출. **보고 시점에 `services/auth.py` 에 아직 함수 없음** → 테스트는 `monkeypatch.setattr(..., raising=False)` 가짜 |
| 만료 · 다른 종류 토큰 · 잘못된 device_id → `SessionExpired` | 라우터가 `/login?reason=session_expired` 로 |
| label 은 be · 상대 시각은 fe | 같음 |
| `signed_in_at` 이 None 일 수 있음(be dto) | 2줄을 비움(글자 짓지 않음) |
| 앱 `POST /api/auth/login` 401 `invalid_credentials` | fe 손대지 않음(be 몫) |

## 이슈 · 코디가 확인할 것
- backend 의 `auth.choose_device` 가 생기기 전까지 mypy(쓰면) 가 `login.py` 의 `auth.choose_device` 속성을 못 찾는다 — be 머지 후 해소.
- E2E 에서 만날 자리: ① 실제 KOS 기기 제한 → `/login` 조각 렌더(라벨 · IP · 시각) ② 계속하기 → 해제 · 재 sign-in 소요(최장 ~60초) 동안 버튼 `day-busy` 상태만 — 별도 진행 표시 없음 ③ 5분 넘긴 뒤 계속하기 → `/login` 안내 칸 「로그인 시간이 끝났습니다…」 ④ 연결 병원 여럿 → 병원 고르기 조각으로 이어짐 ⑤ 다시 막힘 → 새 목록.
- 시안 없음 — 라디오 카드 모양(테두리 · 고르면 primary 테두리/옅은 배경)은 병원 고르기 줄과 DS 토큰으로 맞춤. 사용자 눈 확인 권장.
- 무관 실패: 없음(돌린 범위 안).
