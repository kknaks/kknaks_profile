# WORK-006 Phase 6b 최종 보정 — 독립 검수

- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **검수 대상**: `tauri-p6b-backend-report.md` §4 표기 보정 + 현재 Phase 6b 결과
- **코드·테스트·문서 수정 0줄. 이 검수 보고서 한 파일만 작성.**
- **실측·배포·커밋·push 없음** — `make test` 는 **직전 회차에서 이미 재현한 값**을 인용한다(§4).

---

## 0. 종합 판정 — **PASS · FAIL 0 · WARN 1(표기, 사소) · 차단 1(D-4 유지)**

**여섯 확인 항목이 모두 통과다.** §4 표에 건수 표기가 들어갔고, **표 9행과 test 함수 9개가
이름·순서까지 일치**한다. B-1/B-2 의 실질(분리 · REST 401 · WS 4401 · `/api/work-requests` 커버)이
전부 유지되고, `backend/src` 에서 바뀐 파일은 여전히 **`http.py` 하나뿐**이다.
**D-4 는 차단으로 살아 있다.**

---

## 1. 판정표

| # | 확인 항목 | 판정 |
|---|---|---|
| 1 | §4 표 머리에 **전 9건 · 2b** 표기 | **PASS** (문구는 지시와 다름 — W-1) |
| 2 | 표 **9행** ↔ test 함수 **9개** 일치 | **PASS** (1:1 대응 확인) |
| 3 | 라우트 등록 분리 · REST 401 · WS 4401 · `/api/work-requests` 커버 유지 | **PASS** |
| 4 | `http.py` 외 권한·쿠키·로그인 구현 불필요 변경 없음 | **PASS** (0줄) |
| 5 | `make test` 1454 + 130 · inventory drift 0 | **PASS** |
| 6 | D-4 차단 유지 | **PASS** |

---

## 2. FAIL

**없다.**

---

## 3. 항목별 확인

### 3-1. §4 건수 표기 (PASS)

현재 문구 — `tauri-p6b-backend-report.md` §4:

```
## 4. 추가한 시험 — `test_production_route_registration.py` 9건

| # — **전 9건**(`2b` 가 끼어 마지막 번호는 8 이다) | 시험 | 재는 것 |
```

- 절 제목과 표 머리 **두 곳**에 «9건»이 선다.
- 표 머리는 **왜 마지막 번호가 8인지까지** 설명한다 — 직전 검수 N-1 이 지적한
  「9건인데 마지막이 8이라 한눈에 안 맞는다」가 **원인 표시로 닫혔다.**

### 3-2. 표 9행 ↔ 함수 9개 (PASS — 1:1 대응)

| 표 # | 표의 시험 | 파일의 함수 | 줄 |
|---|---|---|---|
| 1 | 대표 REST 표면 등록 | `test_production_registers_the_rest_surface_the_wrapper_opens` | 38 |
| 2 | 회의 스트림 WS 등록 | `test_production_registers_the_meeting_stream_websocket` | 45 |
| **2b** | 미인증 WS 가 `CLOSE_UNAUTHORIZED`(4401) | `test_the_meeting_stream_refuses_an_unauthenticated_handshake` | 50 |
| 3 | `/health` 게이트 밖 | `test_health_stays_outside_the_profile_gate` | 71 |
| 4 | 등록 ≠ 통과 | `test_registered_does_not_mean_reachable_without_a_session` | 76 |
| 5 | 페르소나 헤더가 증명하지 못한다 | `test_the_development_persona_header_proves_nothing_in_production` | 88 |
| 6 | 로컬 로그인·데모 지름길 폐쇄 | `test_local_login_and_demo_shortcuts_stay_closed_in_production` | 97 |
| 7 | `Secure` 조건 불변 | `test_the_secure_cookie_condition_is_unchanged` | 105 |
| 8 | 개발 회귀 방지 | `test_development_keeps_both_the_routes_and_its_own_seam` | 112 |

- **표 행 9 · `def test_` 9**(기계로 셈) — **개수 일치**
- **순서도 파일 순서 그대로**다. 표를 보고 파일을 찾을 때 어긋나지 않는다
- 누락·중복 **0**

### 3-3. B-1/B-2 실질 유지 (PASS)

| 계약 | 근거 좌표 | 상태 |
|---|---|---|
| **라우트 등록 분리** | `http.py` `git diff -w --stat` → **+7 / -2**(보정으로 늘지 않음) · §3-2 의 게이트 표(`developer_auth_enabled` 611..614 라우트 0 · `local_login_enabled` 633..653 라우트 1) | **유지** |
| **REST 401** | 시험 4 `…:84-85` — `/api/tasks` · `/api/work-requests` · `/api/my-work` · `/api/organization/members` → `status_code == 401` | **유지** |
| **WS `CLOSE_UNAUTHORIZED` 4401** | 시험 2b `…:62,68` — `assert closed.value.code == CLOSE_UNAUTHORIZED` · 페르소나 헤더판도 같은 단언. 상수는 제품에서 import(`…:23`)하고 값은 `stream.py:16` **`CLOSE_UNAUTHORIZED = 4401`** | **유지** |
| **`/api/work-requests` 커버** | 등록 `…:41` · 401 `…:84` · persona 401 `…:93` — **세 축 전부** | **유지** |

### 3-4. `http.py` 외 무변경 (PASS)

| 파일 | `git diff` |
|---|---|
| `backend/src/ax_workspace/entrypoints/http.py` | 수정됨(**+7 / -2**, 나머지는 내어쓰기) |
| `backend/src/.../entrypoints/http_auth.py` | **비어 있음** — 권한 판정 · `cookie_secure` **0줄** |
| `backend/src/.../bootstrap/settings.py` | **비어 있음** — `developer_auth_enabled` · `local_login_enabled` **0줄** |
| `backend/src/.../modules/meetings/stream.py` | **비어 있음** — close 코드 상수를 **시험이 읽기만 했다** |

- `git status --porcelain backend/` → 수정 **3**(`http.py` + 시험 2개) · 신규 **1**(신규 시험 파일).
  **`backend/src` 에서 바뀐 파일은 `http.py` 하나뿐**이다.
- **로그인 구현 불변**: `/api/auth/login` 은 `local_login_enabled` 게이트 아래 그대로이고,
  PRODUCTION 에서 계속 **등록되지 않는다**(시험 6).

### 3-5. 수치·drift (PASS)

| 항목 | 보고서 | 검수 확인 |
|---|---|---|
| `make test` | 머리말·V-8: **exit 0 · 1454(병렬) + 130(직렬) · 실패 0** | **직전 회차에서 실제로 재현했다** — `1454 passed … 356.91s` · `130 passed, 1571 deselected … 311.21s` · exit 0. 이번 회차는 코드·시험이 **한 줄도 바뀌지 않았으므로**(§3-4) 그 값이 그대로 유효하다. 발주 「실측 금지」에 따라 **다시 돌리지 않았다** |
| 회차 구분 | V-5 **1453**(보정 전) · V-8 **1454**(보정 후) 둘 다 남김 | **정직하다** — 보정 전후를 지우지 않고 갈랐고, **+1 이 WS 시험 하나와 정확히 맞는다** |
| **inventory drift 0** | V-6 「6 passed — MCP·HTTP 시그니처 drift 0」 | `git status --porcelain docs/` → **비어 있음**. `docs/unified-operations-inventory.json` **무변경** ✅ |

### 3-6. D-4 차단 유지 (PASS)

보고서 **§8 이 그대로 살아 있다**:

- PRODUCTION 은 `local_login_enabled == False` → **`/api/auth/login` 미등록**
- OIDC **코드 없음** — `auth_providers` 가 `oidc: False`
- → **세션을 «발급»하는 route 0개.** 모든 라우트가 등록됐으나 **전부 401**
- 「**로그인 수단을 정하기 전에는 운영 배포를 «사용 가능»으로 판정하지 말 것**」 **유지**

**검수도 같은 판정이다.** 이것은 시험·문서로 닫을 수 없고 **제품 계약 결정**(OQ-W05)이다.

---

## 4. WARN (1건, 표기 — 사소)

| # | 내용 | 수정 방향 |
|---|---|---|
| **W-1** | **지시한 문구와 실제 문구가 다르다.** 발주는 표 머리에 「`전 9건(2b 포함)`」을 기대했는데, 실제는 「**전 9건**(`2b` 가 끼어 마지막 번호는 8 이다)」이다. **의미는 같고 오히려 «왜 8로 끝나는가»까지 설명해 더 낫다** — 그러나 코디가 **리터럴 문자열로 grep 하면 안 잡힌다** | 그대로 두어도 무방하다. 검색 가능성을 원하면 `(2b 포함)` 를 괄호 안에 병기 |

> 직전 검수의 「정적 검사(ruff·mypy) 부재」는 저장소의 구조적 특성이고 이번 범위 밖이라 다시 올리지 않는다.

---

## 5. 차단 (열려 있는 결정 — 이월 아님)

**D-4 · PRODUCTION 세션 발급 수단 부재.** B-1/B-2 로 라우트는 전부 등록됐지만 **들어갈 방법이 없다.**
래퍼가 운영 주소를 열어도 로그인 화면에서 더 나아가지 못한다. **코디·사용자의 결정**이 필요하고,
그 전에는 **운영 배포를 「사용 가능」으로 판정하면 안 된다.**

---

## 6. 한 줄 정리

**표기 보정이 들어갔고 표 9행과 함수 9개가 이름·순서까지 맞는다.** B-1/B-2 의 실질은
한 자리도 흔들리지 않았고(`backend/src` 는 `http.py` 하나, +7/-2), 수치 1454+130 과 drift 0 도
그대로다. **Phase 6b backend 쪽에 남은 기술적 지적은 없다 — 남은 것은 D-4 결정뿐이다.**
