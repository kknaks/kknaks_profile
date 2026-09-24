# WORK-006 Phase 6b B-1/B-2 — PRODUCTION 라우트 등록 분리

- **발주**: Phase 6a 설계 §3-4(「라우트 등록과 권한 판정을 분리한다」)
- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **결과**: **완료.** `make test` **exit 0 · 1454 + 130 passed · 실패 0**
- **검수 보정**: 2026-09-22 **22:10 KST** — W-1(WS `CLOSE_UNAUTHORIZED` 단언) · W-2(`/api/work-requests` 커버) · W-3(게이트 둘 구분) 반영
- 커밋 · push · PR · 배포 · 비밀값 **없음**

---

## 1. 한 줄 결론

`create_app` 의 **한 `if` 가 겸하던 두 일**(라우트 등록 · 개발 이음새 부착)을 갈랐다.
이제 **API·WS 라우트는 프로파일과 무관하게 등록**되고, 막는 것은 **종전 그대로 권한 판정**이다.
**공백을 무시한 실제 코드 변경은 7줄 추가 · 2줄 삭제**이고 나머지는 전부 들여쓰기다.

---

## 2. 변경 파일

| 파일 | 변경 |
|---|---|
| `backend/src/ax_workspace/entrypoints/http.py` | 게이트 분리(아래 §3). 실질 **+7 / -2**, 나머지 1920줄은 내어쓰기 |
| `backend/tests/architecture/test_architecture.py` | `test_production_exposes_no_persona_surface_at_all` 을 **새 계약으로** 갱신(§5-1) |
| `backend/tests/contract/test_authentication.py` | `test_production_is_offered_no_accounts_and_no_route` 갱신(§5-2) |
| `backend/tests/contract/test_production_route_registration.py` | **신규** — 시험 9건(§4) |

**건드리지 않은 것**: `http_auth.py`(§3-3) · `settings.py` · 제품 프론트 · 인프라 레포 · SPEC/WORK.

---

## 3. 무엇을 어떻게 갈랐나

### 3-1. 이전 (문제)

```python
if settings.developer_auth_enabled:          # http.py:606
    app.state.developer_auth = DeveloperAuthAdapter(settings)
    app.state.workflow_application = create_workflow_application(...)
    app.state.auth_sessions = create_auth_session_store(settings)
    @app.get("/api/auth/providers")          # …이하 1920줄, 라우트 159개가 전부 이 안
```

`developer_auth_enabled` 는 `profile in {DEVELOPMENT, TEST}` 다 → **PRODUCTION 이면 라우트 0개**,
`/health` 만 남았다.

### 3-2. 지금

```python
# 라우트의 «존재»와 «누가 부를 수 있나»는 다른 질문이다. …
app.state.workflow_application = create_workflow_application(settings, report_provider)
app.state.auth_sessions = create_auth_session_store(settings)
if settings.developer_auth_enabled:
    # 개발·시험 전용 이음새(`X-Demo-Persona`). PRODUCTION 에는 붙이지 않는다.
    app.state.developer_auth = DeveloperAuthAdapter(settings)

@app.get("/api/auth/providers")              # …이하 라우트는 게이트 «밖»
```

#### 게이트가 «둘»이다 — 섞어 읽지 않는다

이 파일에는 프로파일 게이트가 **두 종류**이고, 이번에 건드린 것은 **앞의 하나뿐**이다.

| 게이트 | 줄 | 그 안의 라우트 | 이번 변경 |
|---|---|---|---|
| `if settings.developer_auth_enabled:` | 611..614 | **0개** | **바꿨다** — 라우트 1920줄을 밖으로 냈고, 남은 것은 `developer_auth` 부착 한 줄뿐 |
| `if settings.local_login_enabled:` (providers 응답의 분기) | 625..629 | **0개** | **안 바꿨다** — 데모 계정·비밀번호를 실을지 말지를 가른다 |
| `if settings.local_login_enabled:` (로그인 route) | 633..653 | **1개** — `@app.post("/api/auth/login")` | **안 바꿨다** — PRODUCTION 에서 계속 **등록되지 않는다** |

- → **「게이트 안 라우트 0개」는 `developer_auth_enabled` 게이트에 한정된 말이다.**
  전체로 보면 **`local_login_enabled` 가 여전히 라우트 1개(`/api/auth/login`)를 막고 있고**,
  그것이 「로그인 방식은 이번 작업이 건드리지 않는다」의 실물이다
- **파일 전체 라우트 데코레이터: 160개** (`/health` 포함). 그중 **PRODUCTION 에 등록되는 것은 159개** —
  빠지는 하나가 위의 `/api/auth/login` 이다

### 3-3. `http_auth.py` 를 **고칠 필요가 없었다**

권한 판정은 이미 개발 이음새를 **선택적**으로 다루고 있었다:

```python
adapter = getattr(request.app.state, "developer_auth", None)   # http_auth.py
if adapter is not None and header_member: ...
raise HTTPException(401, "로그인이 필요합니다.")
```

PRODUCTION 에는 그 속성이 붙지 않으므로 **페르소나 헤더가 사람을 증명하지 못하고 401 로 떨어진다.**
그래서 이 파일은 **0줄** 바꿨다 — 권한 계약을 건드리지 않았다는 가장 단단한 증거다.

### 3-4. `Secure` 쿠키 — 손대지 않았다

`cookie_secure()` 는 그대로 `profile == PRODUCTION` 이다. 시험으로 세 프로파일을 고정했다(§4).

---

## 4. 추가한 시험 — `test_production_route_registration.py` 9건

| # — **전 9건**(`2b` 가 끼어 마지막 번호는 8 이다) | 시험 | 재는 것 |
|---|---|---|
| 1 | 대표 REST 표면 등록 | `/api/tasks` · **`/api/work-requests`** · `/api/my-work` · `/api/meetings` · `/api/organization/members` |
| 2 | **회의 스트림 WS 등록** | `/api/meetings/{meeting_id}/stream` — 래퍼의 존재 이유가 걸린 자리 |
| 2b | **미인증 WS 핸드셰이크가 `CLOSE_UNAUTHORIZED`(4401)로 닫힌다** | REST 는 401 로 답하지만 WS 는 상태코드를 못 쓴다. **닫는 «코드»까지** 재야 4404·4409 같은 다른 사유와 섞이지 않는다. 페르소나 헤더를 실어도 같은 코드다 |
| 3 | `/health` 는 게이트 밖 그대로 | probe 경로 |
| 4 | **등록 ≠ 통과** | 세션 없이 `/api/tasks` · **`/api/work-requests`** · `/api/my-work` · `/api/organization/members` → **401**(404 아님) |
| 5 | 페르소나 헤더가 PRODUCTION 에서 **아무것도 증명하지 못한다** | `developer_auth` 부재 + 401 |
| 6 | 로컬 로그인·데모 지름길은 계속 닫힘 | `/api/auth/login` 미등록 · providers 가 `{local: False, oidc: False}` |
| 7 | **`Secure` 조건 불변** | PRODUCTION True · DEVELOPMENT/TEST False |
| 8 | 개발 회귀 방지 | 개발에는 라우트 + 로그인 + 페르소나 이음새가 **그대로** |

---

## 5. ⚠ 기존 시험 2건이 «옛 계약»을 명시하고 있었다 — 무엇을 어떻게 바꿨나

발주가 「실패를 숨기지 않는다」고 했으므로 그대로 적는다. 변경 직후 **정확히 2건**이 붉어졌고,
둘 다 **의도적으로 「PRODUCTION 은 아무것도 등록하지 않는다」를 단언**하던 시험이다.

### 5-1. `test_production_exposes_no_persona_surface_at_all` (architecture)

- **옛 단언**: `/api/tasks`·`/api/meetings`·`/api/graph` 가 **등록되지 않는다**, 그 경로는 **404**
- **옛 근거(docstring)**: 「진짜 로그인(Google OIDC)이 아직 없으니 **문을 열어 두느니 아예 없애자**」
- **바꾼 것**: 「경로가 없는가」 → **「세션 없이는 하나도 통과하지 못하는가」**
  - 업무 경로가 **등록되어 있음**을 단언(래퍼가 여는 표면이므로)
  - 그 경로들이 **페르소나 헤더로도 401** 임을 단언
  - `developer`·`persona` 이름의 경로가 **여전히 하나도 없음**은 **그대로 유지**

> **보안 의도를 약화시키지 않았다.** 옛 시험이 지키려던 것은 「신원 없이 들어갈 길이 없다」이고,
> 그 성질은 지금도 성립한다 — 다만 **404(없다)가 아니라 401(누군지 모른다)로** 성립한다.
> 문이 «없는 것»에서 «잠긴 것»으로 바뀌었고, 시험이 그 자물쇠를 잰다.

### 5-2. `test_production_is_offered_no_accounts_and_no_route` (contract)

- **옛 단언**: `/api/auth/providers` 가 **404**
- **바꾼 것**: **200 이되 `{"local": False, "oidc": False}`** 이고, `demo_accounts`·`demo_password` 가
  **한 줄도 실리지 않음**을 단언. `/api/auth/login` 미등록도 그대로 유지
- 바뀐 것은 **등록**이지 **답의 내용**이 아니다

---

## 6. 검증 수치

| # | 명령 | 결과 |
|---|---|---|
| V-1 | `python -c "ast.parse(http.py)"` | **구문 OK** |
| V-2 | `uv run pytest tests/contract/test_production_route_registration.py` | **9 passed** |
| V-3 | `make test-unit`(변경 직후, 수정 전) | `1 failed / 380 passed` — §5-1 |
| V-4 | `make test-contract`(변경 직후, 수정 전) | `1 failed / 1065 passed` — §5-2 |
| V-5 | **`make test`**(시험 갱신 후) | **exit 0** · 병렬 **1453 passed** · 직렬 **130 passed** · **실패 0** |
| V-8 | **`make test`**(검수 보정 W-1~W-3 반영 후, 최종) | **exit 0** · 병렬 **1454 passed**(WS 시험 +1) · 직렬 **130 passed** · **실패 0** |
| V-6 | `pytest`(갱신한 2건 + `test_operation_inventory.py`) | **6 passed** — MCP·HTTP 시그니처 **drift 0** |
| V-7 | `git diff -w --stat http.py` | **+7 / -2** — 나머지는 전부 들여쓰기 |

- **정적 검사**: 이 저장소에는 **ruff·mypy 설정과 lint 타겟이 없다**(`Makefile` · `pyproject.toml` 확인).
  그 역할을 `tests/architecture/`(아키텍처 규칙 · operation inventory drift)가 하고, 그것이 V-5·V-6 에 포함된다.
  **없는 검사를 돌렸다고 쓰지 않는다**
- **기준선 대비 새 실패 0** — 최종 상태에서 실패가 하나도 없다

---

## 7. 계약 준수

| 계약 | 지킴 |
|---|---|
| 라우트 등록과 권한 판정 분리 · PRODUCTION 에 API/WS 존재 | §3-2 · 시험 1·2 |
| PRODUCTION `Secure` 쿠키 조건 유지 | `cookie_secure()` **무변경** · 시험 7 |
| DEV/TEST 전용 demo·local login 표면은 계속 닫힘 | `local_login_enabled` 게이트 **무변경** · 시험 6 |
| 새 인증 수단·권한 완화 없음 | `http_auth.py` **0줄** · 권한 판정 로직 **무변경** |
| FE 정적 서빙·인프라 차트 미포함 | 손대지 않았다 |
| `/health` 게이트 밖 유지 | 시험 3 |

---

## 8. ⚠ 미결 — D-4 (PRODUCTION 로그인 수단)

**이 작업이 푼 것은 「라우트가 없다」이지 「로그인할 수 있다」가 아니다.**

- PRODUCTION 은 `local_login_enabled == False` 라 **`/api/auth/login` 이 등록되지 않는다**
- 외부 IdP(OIDC)는 **코드에 없다** — `/api/auth/providers` 가 `oidc: False` 로 답한다
- → **지금 PRODUCTION 에는 세션을 «발급»하는 route 가 하나도 없다.** 모든 라우트는 등록돼
  있으나 **전부 401** 이다. 시험 4·5 가 그 상태를 의도적으로 고정한다

**즉 운영 배포는 이 상태로 «사람이 쓸 수» 없다.** 데스크톱 래퍼가 운영 주소를 열면
**로그인 화면에서 더 나아가지 못한다.**

- 이것이 Phase 6a 의 **D-4** 이고, **새 제품 계약**이라 이 작업 범위 밖이다(OQ-W05)
- **발주의 「필요하면 즉시 올린다」에 따라 올린다** — 로그인 수단을 정하기 전에는
  **운영 배포를 «사용 가능»으로 판정하지 말 것**

---

## 9. 이번 회차에서 하지 않은 것

- 로그인 방식 신설 · 권한 완화 · 외부 IdP
- FE 정적 서빙 · 인프라 차트 · 레지스트리 · 배포
- 비밀값 열람 · 커밋 · push · PR
- `http_auth.py` · `settings.py` **0줄** (필요가 없었다 — §3-3)
