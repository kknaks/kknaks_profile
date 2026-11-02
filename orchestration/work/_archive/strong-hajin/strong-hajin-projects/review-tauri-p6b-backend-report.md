# WORK-006 Phase 6b B-1/B-2 backend — 독립 검수

- **검수 대상**: `tauri-p6b-backend-report.md` ↔ 현재 backend diff
- **코드**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **코드 수정 0줄. 이 검수 보고서 한 파일만 작성.**

---

## 0. 종합 판정 — **PASS · FAIL 0 · WARN 3 · 차단 1(D-4 유지)**

**분리가 정확하고 최소하게 됐다.** `git diff -w` 로 재면 **+7 / -2**, 나머지 1900여 줄은 전부
내어쓰기다. 권한 판정 파일(`http_auth.py`)과 `settings.py` 는 **한 줄도 바뀌지 않았고**,
`local_login_enabled` 게이트도 그대로다 — **권한을 건드리지 않았다는 가장 단단한 증거**다.

**보고된 수치를 전부 재현했다**: `make test` **exit 0 · 1453 passed(병렬) + 130 passed(직렬)** ·
inventory drift **0**. 기존 시험 2건의 갱신도 **보안 의도를 약화시키지 않았다**(§4).

**D-4 는 차단으로 유지한다** — 보고서가 §8 로 스스로 올렸고, 검수도 같은 판정이다.

---

## 1. 판정표

| # | 발주 검수 항목 | 판정 |
|---|---|---|
| 1 | 라우트 등록 게이트 제거 · PRODUCTION 에 REST/WS 등록 | **PASS** |
| 2 | REST 가 404 아닌 **401**(권한 판정)로 도달 | **PASS** |
| 3 | **WS** 가 404 아닌 권한 판정으로 도달 | **PASS(코드)** · 시험 공백 **WARN**(W-1) |
| 4 | `Secure` 쿠키 조건 불변 | **PASS** |
| 5 | `local_login` · developer persona 차단 유지 | **PASS** |
| 6 | 권한 판정 약화 없음 | **PASS** (`http_auth.py` **0줄**) |
| 7 | 기존 구계약 시험 2건 갱신의 의미 | **PASS** (§4) |
| 8 | `make test` 1453 + 130 재현 | **PASS** (정확히 일치) |
| 9 | inventory drift 0 | **PASS** |
| 10 | 허용 파일 밖 변경 · 로그인 방식 발명 · 배포 | **PASS** (전부 없음) |
| 11 | D-4 차단 유지 | **PASS** (§6) |

---

## 2. FAIL

**없다.**

---

## 3. 코드 변경 — 직접 확인

### 3-1. 분리 자체 (PASS)

`git diff -w backend/src/.../http.py` → **7 insertions · 2 deletions**. 실제 변경은 이것뿐이다:

```python
-    if settings.developer_auth_enabled:
-        app.state.developer_auth = DeveloperAuthAdapter(settings)
+    # 라우트의 «존재»와 «누가 부를 수 있나»는 다른 질문이다. …
     app.state.workflow_application = create_workflow_application(settings, report_provider)
     app.state.auth_sessions = create_auth_session_store(settings)
+    if settings.developer_auth_enabled:
+        app.state.developer_auth = DeveloperAuthAdapter(settings)
```

**기계로 센 결과**(검수가 직접):

| 확인 | 값 |
|---|---|
| 파일 전체 라우트 데코레이터 | **160** (`/health` 포함) — 보고서와 일치 |
| **들여쓰기 4칸**(게이트 밖) 라우트 | **159** |
| **들여쓰기 8칸** 라우트 | **1** — `@app.post("/api/auth/login")`(`http.py:635`), `local_login_enabled` 게이트 아래 |
| `developer_auth_enabled` 게이트 본문 | **3줄**(주석 2 + 대입 1) · **라우트 0개** |
| WS | `http.py:1014` `@app.websocket("/api/meetings/{meeting_id}/stream")` — **들여쓰기 4칸(게이트 밖)** |
| `/health` | `http.py:2535` — **들여쓰기 4칸**, 종전대로 게이트 밖 |

→ **보고서 §3-2 의 「게이트 안 라우트 0개」가 사실이다**(단 문구는 W-3).

### 3-2. 권한이 약화되지 않았다 (PASS)

- **`http_auth.py` · `settings.py` 는 `git diff` 가 비어 있다** — 0줄.
- `current_principal` 은 **세션 쿠키 우선**, 페르소나 헤더는 `getattr(app.state, "developer_auth", None)`
  가 있을 때만 쓴다. PRODUCTION 은 그 속성을 **붙이지 않으므로** 헤더가 사람을 증명하지 못하고
  **401** 로 떨어진다.
- 이중 방어도 그대로다 — `DeveloperAuthAdapter.__init__` 이 `developer_auth_enabled` 가 아니면
  `RuntimeError` 를 던진다. **속성을 억지로 붙여도 어댑터가 만들어지지 않는다.**
- `cookie_secure()` → `profile == PRODUCTION` **무변경**.
- **`local_login_enabled` 게이트 무변경** — `/api/auth/login` 은 PRODUCTION 에서 계속 미등록이고,
  `auth_providers` 는 `{"local": False, "oidc": False}` 를 답하며 `demo_accounts`·`demo_password`
  를 싣지 않는다.

### 3-3. WS 의 권한 판정 (PASS — 코드 기준)

```python
await websocket.accept()
principal = connection_principal(websocket)
if principal is None:
    await websocket.close(code=CLOSE_UNAUTHORIZED, reason=REASON_UNAUTHORIZED)
    return
```

PRODUCTION 에서 `connection_principal` 은 세션이 없고 어댑터도 없으므로 **`None`** → **인증 거절로
닫힌다.** 404 가 아니라 **권한 판정**이다. **다만 이것을 재는 시험이 없다**(W-1).

---

## 4. 기존 시험 2건 갱신 — 의미 확인 (PASS)

**둘 다 「PRODUCTION 은 아무것도 등록하지 않는다」는 «옛 계약»을 단언하던 시험**이고,
갱신이 **보안 성질을 약화시키지 않았다.**

| 시험 | 옛 단언 | 새 단언 | 검수 판정 |
|---|---|---|---|
| `test_production_exposes_no_persona_surface_at_all` | `/api/tasks`·`/api/meetings`·`/api/graph` **미등록** · 세 경로 **404** | `/api/tasks`·WS **등록됨** · `/api/my-work`·`/api/graph/search` 가 **페르소나 헤더로도 401** · `developer`/`persona` 이름 경로 **여전히 0** · `/api/developer/personas` **404** | **타당.** 지키려던 성질(「신원 없이 들어갈 길이 없다」)이 **404 → 401** 로 형태만 바뀌어 유지된다. 문이 «없는 것»에서 «잠긴 것»으로 바뀌었고 시험이 자물쇠를 잰다 |
| `test_production_is_offered_no_accounts_and_no_route` | `/api/auth/providers` **404** | **200** 이되 `{"local": False, "oidc": False}` · `demo_accounts`·`demo_password` **부재** · `/api/auth/login` **미등록** · `/api/developer/personas` **미등록** | **타당.** 바뀐 것은 **등록**이지 **답의 내용**이 아니다. 오히려 «지름길이 새지 않는가»를 **새로 단언**해 이전보다 촘촘하다 |

→ **두 갱신 모두 계약 완화가 아니라 «같은 성질의 다른 형태»를 잰다.** 보고서 §5 의 설명이 정확하다.

---

## 5. 수치 재현

| # | 명령 | 보고서 | **재현 결과** | 일치 |
|---|---|---|---|---|
| V-5 | `make test` | exit 0 · 병렬 1453 · 직렬 130 | **exit 0** · `1453 passed … 384.62s` · `130 passed, 1570 deselected … 305.49s` | ✅ **정확히 일치** |
| V-2 | 신규 시험 파일 | 8 passed | **8건 수집 확인**(collect-only) · `make test` 안에서 실행됨 | ✅ |
| V-6 | 갱신 2건 + inventory | 6 passed | inventory 4건 + 갱신 2건 = **6** — 수집으로 확인 | ✅ |
| V-7 | `git diff -w --stat` | +7 / -2 | **+7 / -2** | ✅ |
| — | **inventory drift** | 0 | `docs/` **변경 0건**(`git status --porcelain docs/` 비어 있음) · `tests/architecture/` 는 `testpaths=["tests"]` 로 **`make test` 에 포함**되어 통과 | ✅ |

- **정적 검사 부재**: `Makefile`·`pyproject.toml` 에 **ruff·mypy 타겟이 없다**는 보고서의 기술을
  검수도 확인했다. **없는 검사를 돌렸다고 쓰지 않은 것이 정직하다.**

---

## 6. ⚠ D-4 — **차단으로 유지한다**

보고서 §8 이 스스로 올렸고, 검수도 **같은 판정**이다.

- PRODUCTION 은 `local_login_enabled == False` → **`/api/auth/login` 미등록**
- OIDC 는 **코드에 없다** — `auth_providers` 가 `oidc: False` 로 답한다(문자열뿐, 구현 없음)
- → **PRODUCTION 에 세션을 «발급»하는 route 가 하나도 없다.** 모든 라우트가 등록됐으나
  **전부 401** 이고, 신규 시험 4·5 가 그 상태를 **의도적으로 고정**한다

> **이 작업이 푼 것은 「라우트가 없다」이지 「로그인할 수 있다」가 아니다.**
> **로그인 수단이 정해지기 전에는 운영 배포를 «사용 가능»으로 판정하면 안 된다.**
> 래퍼가 운영 주소를 열어도 로그인 화면에서 더 나아가지 못한다.

---

## 7. WARN

| # | 내용 | 수정 방향 |
|---|---|---|
| **W-1** | **신규 8건이 WS 의 «등록 ≠ 통과»를 재지 않는다.** REST 는 시험 4·5 가 401 을 단언하는데, WS 는 시험 2 가 **«등록»만** 단언하고 **미인증 핸드셰이크가 거절되는지는 비어 있다.** 코드는 옳지만(§3-3), **이 분리로 WS 가 PRODUCTION 에 처음 «등장»한 표면**이라 오히려 새로 생긴 자리다 | `TestClient(...).websocket_connect(...)` 로 **미인증 핸드셰이크가 `CLOSE_UNAUTHORIZED` 로 닫히는지** 재는 시험 1건 추가 |
| **W-2** | **`/api/work-requests` 가 어느 쪽도 단언되지 않게 됐다.** 옛 architecture 시험은 이 경로의 **미등록**을 단언했는데, 갱신본은 그 단언을 빼면서 대체 단언(`/api/tasks`·WS)에 포함시키지 않았다. `/api/graph/search` 는 401 루프에 들어가 커버되지만 `/api/work-requests` 는 **등록도 401 도 재지 않는다** | 신규 시험 1의 경로 목록이나 시험 4의 401 루프에 `/api/work-requests` 한 줄 추가 |
| **W-3** | **보고서 §3-2 의 「게이트」가 어느 게이트인지 모호하다.** 「게이트 안에 남은 라우트: 0개」는 `developer_auth_enabled` 게이트 기준으로 **맞지만**, 파일에는 여전히 `local_login_enabled` 게이트 아래 라우트가 **1개**(`/api/auth/login`) 있다. 둘이 다른 게이트라 모순은 아니나 읽는 사람이 헷갈릴 수 있다 | 「**`developer_auth_enabled` 게이트** 안에 남은 라우트: 0개(로컬 로그인은 별도 게이트로 계속 닫힘)」로 한정 |

---

## 8. 금지 사항 — 위반 0

| 금지 | 확인 |
|---|---|
| 허용 파일 밖 변경 | backend 변경은 **정확히 4개** — `http.py` · `test_architecture.py` · `test_authentication.py` · 신규 `test_production_route_registration.py`. 그 밖 **0** |
| `http_auth.py` · `settings.py` | **0줄**(`git diff` 비어 있음) |
| **로그인 방식 발명** | `git diff backend/` 에서 `oidc|idp|oauth|jwt` 를 전수 검색 → **신규 구현 0**. 걸린 세 줄은 **기존 `auth_providers` 코드의 재들여쓰기**와 **시험 docstring/단언**뿐 |
| 권한 완화 | 판정 로직 **무변경** |
| 인프라·FE·SPEC/WORK | 손대지 않았다(프론트 변경은 **Phase 4 의 기존 것 그대로**, 이번 회차 아님) |
| 커밋 · push · PR · 배포 · 비밀값 | 없음. HEAD `a1f6791` 그대로 |

---

## 9. 코디에게 올리는 결정거리

1. **D-4 를 여는 결정** — 이것 없이는 운영 배포가 «사람이 쓸 수 없는» 상태다. **B-1 이 끝난 지금이
   가장 늦은 시점**이다(OQ-W05).
2. **W-1** — WS 미인증 거절 시험 1건. 새로 연 표면이라 **가장 값싸고 중요한 보강**이다.
3. **W-2 · W-3** — 시험 한 줄, 보고서 문구 한정. 사소하다.
4. **정적 검사 부재**(ruff·mypy)는 이 저장소의 구조적 특성이고 이번 범위 밖이다 — 이월.
