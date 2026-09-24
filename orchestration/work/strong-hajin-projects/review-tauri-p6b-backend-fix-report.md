# WORK-006 Phase 6b backend WARN 보정 — 독립 검수

- **검수 대상**: 보정된 `test_production_route_registration.py` · `tauri-p6b-backend-report.md`
  (직전 검수 `review-tauri-p6b-backend-report.md` 의 **W-1 · W-2 · W-3**)
- **코드**: HEAD `a1f6791`(변동 없음) · **코드 수정 0줄. 이 검수 보고서 한 파일만 작성.**

---

## 0. 종합 판정 — **PASS · FAIL 0 · WARN 1(사소) · 차단 1(D-4 유지)**

**W-1 · W-2 · W-3 이 모두 닫혔다.** 특히 W-1 은 「예외가 나는가」가 아니라
**`CLOSE_UNAUTHORIZED`(4401) 라는 «코드»를 단언**했고, **왜 코드까지 재야 하는지**(4404 참석 ·
4409 상태로 닫혀도 초록이 되면 「인증이 막았다」를 증명하지 못한다)를 docstring 에 적었다 —
지적의 의도를 정확히 읽은 보정이다.

`make test` 를 처음부터 다시 돌려 **exit 0 · 1454 + 130** 을 재현했다. `backend/src` 는
**`http.py` 한 파일만** 바뀌었고 그 diff 는 여전히 **+7 / -2** 다.

---

## 1. 판정표

| # | 발주 확인 항목 | 판정 |
|---|---|---|
| 1 | 미인증 WS 가 **실제 `CLOSE_UNAUTHORIZED` 4401** 단언 | **PASS** |
| 2 | `/api/work-requests` 가 **등록 · 401 · persona 401** 세 곳에 | **PASS** |
| 3 | 보고서가 **두 게이트를 분리해** 설명 | **PASS** |
| 4 | `backend/src` 권한·쿠키·로그인 구현 **무변경** | **PASS** |
| 5 | `make test` **1454 병렬 + 130 직렬** | **PASS** (재현) |
| 6 | **D-4 미결** 유지 | **PASS** |

---

## 2. FAIL

**없다.**

---

## 3. 보정 확인

### 3-1. W-1 — WS 가 «코드까지» 재진다 (PASS)

`test_the_meeting_stream_refuses_an_unauthenticated_handshake` (신규):

```python
with pytest.raises(WebSocketDisconnect) as closed:
    with client.websocket_connect(f"/api/meetings/{uuid4()}/stream") as socket:
        socket.receive_json()
assert closed.value.code == CLOSE_UNAUTHORIZED
```

- **상수를 제품 코드에서 import 한다** — `from ax_workspace.modules.meetings.stream import CLOSE_UNAUTHORIZED`.
  숫자를 시험에 박지 않아 **제품이 값을 바꾸면 시험이 따라온다.**
- **검수가 값을 직접 확인**: `stream.py:16` `CLOSE_UNAUTHORIZED = 4401` ✅
- **「코드까지 재야 한다」는 근거가 실재한다** — 같은 파일에 `CLOSE_NOT_FOUND = 4404`(`:17`) ·
  `CLOSE_CONFLICT = 4409`(`:18`) 가 있다. **막연한 예외 단언이었다면 그 둘로 닫혀도 초록이 됐을 것**이고,
  docstring 이 정확히 그 이유를 적는다.
- **페르소나 헤더를 실은 두 번째 핸드셰이크도 같은 코드**임을 단언 — 개발 이음새가 PRODUCTION 에
  붙지 않는다는 성질을 **WS 쪽에서도** 고정한다. REST 의 시험 5 와 짝이 맞는다.

### 3-2. W-2 — `/api/work-requests` 가 세 곳 모두에 (PASS)

| 시험 | 경로 목록 |
|---|---|
| 1 · 등록 | `/api/tasks` · **`/api/work-requests`** · `/api/my-work` · `/api/meetings` · `/api/organization/members` |
| 4 · 세션 없이 **401** | `/api/tasks` · **`/api/work-requests`** · `/api/my-work` · `/api/organization/members` |
| 5 · **persona 헤더로도 401** | `/api/tasks` · **`/api/work-requests`** · `/api/my-work` |

- **발주가 요구한 세 축(등록 · 401 · persona 401)에 전부 들어갔다.**
- **단언이 공허하지 않다** — `http.py` 에 `/api/work-requests` 라우트 데코레이터가 **22개** 있다
  (검수가 직접 셈). 경로가 실제로 존재하므로 등록 단언이 의미를 갖는다.

### 3-3. W-3 — 게이트 둘이 갈렸다 (PASS)

보고서 §3-2 에 **「게이트가 «둘»이다 — 섞어 읽지 않는다」** 표가 신설됐고, **줄 번호까지 검수가
대조해 전부 맞다**:

| 게이트 | 보고서 | 실제 확인 |
|---|---|---|
| `if settings.developer_auth_enabled:` | 611..614 · 라우트 **0개** · **바꿨다** | `sed -n '611,614p'` → 주석 2줄 + `app.state.developer_auth = ...` 한 줄. **라우트 0** ✅ |
| `if settings.local_login_enabled:` (providers 분기) | 625..629 · 라우트 **0개** · **안 바꿨다** | `625` 가 `if settings.local_login_enabled:`, 본문은 `demo_accounts` 조립. **라우트 0** ✅ |
| `if settings.local_login_enabled:` (로그인 route) | 633..653 · 라우트 **1개** · **안 바꿨다** | `633` 게이트 · `635` `@app.post("/api/auth/login")` ✅ |

- **「게이트 안 라우트 0개」가 `developer_auth_enabled` 에 한정된 말임이 명시**됐고,
  **전체로 보면 `local_login_enabled` 가 여전히 라우트 1개를 막는다**는 사실이 함께 적혔다.
- 「파일 전체 160개 중 **PRODUCTION 에 등록되는 것은 159개**, 빠지는 하나가 `/api/auth/login`」
  이라는 정리도 **검수가 센 값과 일치**한다. 직전 검수에서 모호하던 자리가 **숫자로 닫혔다.**

### 3-4. `backend/src` 무변경 (PASS)

| 파일 | 상태 |
|---|---|
| `entrypoints/http.py` | 수정됨 — `git diff -w --stat` **+7 / -2**(직전과 동일, 이번 보정으로 늘지 않았다) |
| `entrypoints/http_auth.py` | **`git diff` 비어 있음** — 권한 판정·`cookie_secure` 0줄 |
| `bootstrap/settings.py` | **무변경** — `developer_auth_enabled`·`local_login_enabled` 0줄 |
| `modules/meetings/stream.py` | **무변경** — close 코드 상수를 **시험이 읽기만 했다** |

→ `backend/src` 에서 바뀐 파일은 **`http.py` 하나뿐**이다. 보정은 **시험과 문서에서만** 일어났다.

### 3-5. 수치 재현 (PASS)

| 항목 | 보고서 | **재현 결과** | 일치 |
|---|---|---|---|
| `make test` | exit 0 · 병렬 **1454** · 직렬 **130** | **exit 0** · `1454 passed … 356.91s` · `130 passed, 1571 deselected … 311.21s` | ✅ |
| 신규 시험 건수 | **9건** | `--collect-only` → **9 tests collected** | ✅ |
| 증가분 | 1453 → **1454**(WS 시험 +1) | 직전 검수 실측 **1453** → 이번 **1454**. **+1 이 WS 시험 하나와 정확히 맞는다** | ✅ |
| `git diff -w --stat` | +7 / -2 | **+7 / -2** | ✅ |

- **V-5(1453)와 V-8(1454)을 둘 다 남긴 것이 옳다** — 보정 전후를 지우지 않고 회차로 갈랐다.

### 3-6. D-4 미결 유지 (PASS)

보고서 §8 이 **그대로**다 — PRODUCTION 에 `/api/auth/login` 미등록 · OIDC 미구현 ·
**세션을 «발급»하는 route 0개** · 모든 라우트가 401. 「**로그인 수단을 정하기 전에는 운영 배포를
«사용 가능»으로 판정하지 말 것**」이 유지된다. **검수도 같은 판정이다.**

---

## 4. WARN (1건, 사소)

| # | 내용 | 수정 방향 |
|---|---|---|
| **N-1** | **§4 시험표의 번호가 `1 · 2 · 2b · 3 … 8` 이다.** 9건인데 마지막 번호가 8이라, 표만 보면 건수가 한눈에 안 맞는다(실제로는 `2b` 가 그 한 건이다). 내용은 정확하다 | `1~9` 로 다시 매기거나 「9건(2b 포함)」을 표 머리에 덧붙인다 |

> 직전 검수의 「정적 검사(ruff·mypy) 부재」는 **이 저장소의 구조적 특성**이고 이번 보정 범위 밖이라
> 다시 올리지 않는다.

---

## 5. 차단 (이월 아님 — 열려 있는 결정)

**D-4(PRODUCTION 세션 발급 수단 부재)** 는 **차단으로 유지**된다. B-1 이 끝나 라우트는 전부
등록됐지만 **들어갈 방법이 없다.** 이것은 시험이나 문서로 닫을 수 없고 **제품 계약 결정**이다
(OQ-W05) — 코디·사용자의 몫이다.

---

## 6. 한 줄 정리

**세 WARN 이 모두 닫혔고, W-1 은 「예외」가 아니라 「4401 이라는 코드」를 재도록 정확히 보정됐다.**
`backend/src` 는 `http.py` 한 파일뿐이고 diff 는 여전히 +7/-2 이며, `make test` 1454 + 130 을
재현했다. 남은 것은 표 번호 한 줄과 **D-4 결정**이다.
