# 리뷰 리포트 — day-data-architecture / code · #229 + 웹 로그인 fix1 재검수 (2026-11-06)

대상: 같은 워크트리의 미커밋 변경(fix1 반영 뒤). 근거 문서는 `frontend-229-fix1-instructions.md` · `frontend-229-fix1-report.md`, 새 스크린샷은 `frontend-229-shots/` 40장, 앞 리포트는 `review-229-report.md` 다.
읽기 전용으로 봤다. KOS 호출은 하지 않았다. **compose 는 건드리지 않았다.** 테스트는 `-m "not infra"` 만 돌렸고, infra 316 은 코디 확인 수치를 따른다.

## 판정: PASS (FAIL 0 · WARN 0)

F1 ~ F3 와 W1 · W2, 「조용히 통과」(빌드 신선도)는 모두 닫혔다. 아래 「참고」는 판정 밖이다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **219 passed · 97 deselected / 3.5s**(수정 리포트 219 와 같음) |
| `uv run ruff check backend scripts` | All checks passed |
| 실데이터 grep 전수(추적 · 미추적 파일, 이미지 · 글꼴 · 빌드 산출물 · lock 제외) | 아래 |

### 실데이터 grep 전수

| 대상 | 결과 |
|---|---|
| 지점 · 브랜드(`명동` · `세라미크`) | 코드 · 템플릿 0. 남은 것은 셋 — `scripts/seed_demo_connection.py:5`(금지 문구) · `tests/day/web/test_kit.py:69` · `tests/day/auth/test_web_login.py:70`(「없어야 한다」 단언) |
| 전화번호 꼴(`01x-xxxx-xxxx`) | 0 |
| `deploy/local.env` 의 데모 키 · 테넌트 id · 시스템 이메일 · 비밀번호 | 각 0 |
| 실명 | 견본의 원장 · 고객 이름은 앞 검수에서 실제 HAR 0건임을 확인한 목업 · 지어낸 이름이다(변경 없음) |
| 스크린샷 | 다시 찍은 40장의 머리가 「KOS 데모 지점」(로컬 시드 이름)이다. `l3` · `l6` · `23` 을 직접 확인했다 |

## F · W 별 확인

| | 판정 | 근거 |
|---|---|---|
| F1 | **닫힘** | `routers/kit.py:180` `hospital_name=view.hospital_name`(로그인 세션의 병원). 견본은 W1 로 로그인해야 열려 자리표시가 필요 없다. 테스트 `test_kit.py:69`(견본 · 모달 4개에 지점 이름 없음) · `test_web_login.py:70`. 스크린샷 다시 찍음 |
| F2 | **닫힘** | `schemas/auth.py:25 · 31` `client: Client = "app"`. `client` 없는 JSON 로그인 → 본문 token · 쿠키 없음 · Bearer `/me` 200 회귀 테스트가 있다. 칸을 남긴 것(`client:"web"` 명시 때만 쿠키)은 #232 가 「기본값 app 또는 칸 없음」을 둘 다 허용하므로 계약 안이다 |
| F3 | **닫힘** | `day/web_errors.py` — `Unauthorized` → `/login` · `SessionExpired` → `?reason=session_expired` · `Forbidden` → 권한 없음 화면 403(HTMX 는 조각) · `CsrfFailed` → 토스트(HTMX 200 + `HX-Reswap: none` / 일반 403). `/logout` 의 개별 try/except 를 없애고 `Depends(writable_session)` 하나로 바꿨다(`login.py`). `/` 는 권한 행이 없으면 `Forbidden`(`login.py` `home`). 테스트 `test_web_errors.py` 7개(DB 없이) + infra 2 |
| W1 | **닫힘** | `/dev/kit` 는 라우터 의존성 `dev_only`(prod 404)가 먼저, 그다음 경로 의존성 `required_web_view`(미로그인 → `/login`)다. FastAPI 는 라우터 의존성을 먼저 푼다. 그래서 prod 에서는 로그인 여부와 상관없이 404 다(`test_kit.py`) |
| W2 | **닫힘** | `session.py` `optional_web_view` · `required_web_view` 가 세션 + `me()` 를 DB 세션 하나로 읽어 `WebView` 를 돌려준다. `/` 는 `Depends(db)` 를 더 쓰지 않는다 |
| 빌드 신선도 | **닫힘** | `build.mjs` 가 `day.css` 첫 줄에 `source-sha256:<app.css>` 를 적고, `test_web_rules.py` 가 비교한다. 이어 붙이는 클래스는 구현 리포트가 수동으로 확인했다(낮음 · 수용) |

### `web_errors` — `/api/` 와 화면 가르기

- `is_api` = 경로가 `/api/` 로 시작하는가(`web_errors.py:34-35`). JSON 쪽은 `exc.to_body()` 를 그대로 써서 공용 `ServiceError` 핸들러와 같은 모양이다. `test_web_errors.py` 가 `/api/` 에서 네 오류 모두 JSON 인 것을 본다. 하네스의 시험 경로도 `/api/test/…` 로 옮겨 JSON 계약 테스트가 계속 JSON 을 본다.
- 핸들러 우선순위: Starlette 는 예외 클래스의 MRO 를 따라 가장 가까운 핸들러를 고른다. 그래서 `Forbidden` 등 하위 클래스 핸들러가 공용 `ServiceError` 핸들러보다 먼저 잡는다. 맞다.
- 가르지 않는 오류: 화면 경로에서 이 넷 밖의 `ServiceError`(예: `KosUnavailable`)가 나면 여전히 공용 JSON 핸들러로 간다. 지금 화면 라우트 중 그런 오류가 밖으로 나가는 곳은 없다. 로그인 오류는 `login.py` 안에서 카드로 그린다. 업무 화면(#231)이 KOS 를 부르게 되면 그때 화면용 처리를 더할 것(참고 1).

## 조용히 통과하는 자리

새로 찾은 것 없음. 앞 리포트의 넷(빌드 신선도 · echo CSRF 무표시 · E04 문서 불일치 · 클래스 추출)은 닫히거나 수용됐다. 아래 하나만 참고로 둔다.

- `test_kit.py:69` · `test_web_login.py:70` 은 **금지어 목록**(`명동` · `세라미크`) 검사다. 다른 실데이터가 들어오면 못 잡고, 실제 브랜드 이름이 테스트 파일에 남는다. 「머리 병원 이름 = 세션 병원 이름(테스트가 만든 이름)」을 양성으로 단언하는 쪽이 더 튼튼하다(참고 2).

## 참고 (판정만 · 질문 항목)

**데모 계정(권한 행 0)이 `/` 에서 권한 없음 화면을 보는 것 — 계약 · SPEC 상 맞다.**
- SPEC-001 규칙 9 는 「권한 행이 없는 직무는 아무것도 못 한다(forbidden)」다. 「케이스 매트릭스 → 웹 화면 처리」 `forbidden` 줄은 「권한 행이 없는 직무는 **로그인 직후에도** 이 화면」이다. #232 A3 는 「forbidden → 권한 없음 화면」이다. 구현(`/` 가 `view.permissions` 가 비면 `Forbidden`)은 이 문장 그대로다. 스크린샷 `l6` 에 셸 · 병원 이름 · [로그아웃]이 보인다.
- dev 에서는 로그인 뒤 갈 곳이 `/dev/kit` 라 사용자 흐름(로그인 → 견본 → 로그아웃)이 막히지 않는다. 견본은 개발 도구라 권한을 보지 않는다. 받아들인다.
- **운영 함의(코디 · 사용자에게)**: `permission_key` 목록(SPEC-000 OQ-04-2)과 직무별 권한 행 넣는 길이 아직 없다. 그래서 **dev 가 아닌 서버에서는 모든 직원이 로그인 직후 권한 없음 화면을 본다.** 계약대로이지만, 시술 현황(#231)이나 stg 를 열기 전에 OQ-04-2(키 목록 + 기본 직무 권한 시드)를 닫아야 한다.

그 밖:
1. 화면 경로의 그 밖 `ServiceError` → 지금은 JSON(위). 업무 화면 Delivery 에서 「알 수 없는 오류 토스트」 처리를 하나 더할 것.
2. 금지어 테스트를 양성 단언으로 바꾸면 실제 브랜드 문자열을 테스트에서도 뺄 수 있다.
3. 「코디 확인」 1(로그인 카드 문구) · 7(Safari `Secure` 쿠키)은 사용자 확인 몫으로 그대로 남아 있다.
