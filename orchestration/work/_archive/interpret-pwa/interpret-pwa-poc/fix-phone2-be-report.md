# 폰 피드백 2 — backend 결과 보고 (D-30 · D-28 확인)

## 상태: done

폰 피드백 1 변경 위에 이어서 · 커밋 없음 · backend 절만(`back/**` · `.env.example`).

## 수행 — 파일·모듈 목록

| 파일 | 무엇 |
|---|---|
| `back/app/config.py` | `interpret_demo_login: bool = False` (env `INTERPRET_DEMO_LOGIN` · 빈 값 = false) |
| `back/app/service/auth.py` | `demo_enabled` · `demo_login()` — 꺼짐 = `NotFound` · 로그인 env 3개 중 빈 것 = 401 `invalid_credentials` · 켜짐 = env 계정 토큰. 토큰 발급을 `_issue()` 로 빼 `login` 과 같은 형식 · 잠금 · 실패 수와 무관(검사도 안 하고 바꾸지도 않는다) |
| `back/app/domain/errors.py` | `NotFound`(404) |
| `back/app/api/auth.py` · `back/app/schemas/auth.py` | `GET /api/auth/config` → `{"demoLogin": bool}`(인증 없음) · `POST /api/auth/demo` → `{token, expiresAt}`(`/api/auth/login` 과 같은 모양) · 꺼지면 404 `{"error":{"code":"not_found",…}}` |
| `.env.example` | `INTERPRET_DEMO_LOGIN=` 이름 + 주석(기본 false · 데모 끝나면 지우고 재시작) |
| `back/app/service/interpret/langs.py` | D-28 개정 — 주석의 한국어 이름을 「대만어」(zh-Hant) · 「중국어」(zh)로. 「중국어 번체」 표기 삭제 |
| `back/tests/test_auth.py` | 아래 |

## 검증 — 명령과 수치

`cd back && uv run ruff check . && uv run pytest -q` → **All checks passed · 185 passed**(이전 174 + 11)

새 시험:
- 기본(꺼짐): config `{"demoLogin": false}`(토큰 없이 200) · `POST /api/auth/demo` 404 `not_found`
- 켜짐: config `true` · demo 200 `{token, expiresAt}` · 그 토큰으로 `/api/auth/me` = env 아이디 · 응답에 비밀번호 0
- 잠금: 비밀번호 로그인 5회 실패로 잠긴 상태에서 demo 는 200 · demo 뒤에도 비밀번호 로그인은 여전히 429(잠금을 풀지 않음)
- 켜짐 + 로그인 env 3개 각각 빔 → demo 401 `invalid_credentials`(config 는 그대로 true)
- env 파싱 `true` · `1` → 켜짐 · `false` · 빈 값 → 꺼짐

## 계약 대조 — DEC-001 D-30 · D-28

| 항목 | 판정 |
|---|---|
| env 스위치 `INTERPRET_DEMO_LOGIN=true` 일 때만 demo | 같음 |
| 꺼짐 404 | 같음 |
| `GET /api/auth/config` → `{demoLogin}` | 같음 |
| 비밀번호를 front 에 내지 않는다 | 같음 — config 에는 bool 하나뿐 |
| D-28 back 의 한국어 이름 | back 에서 화면에 나가는 문구에 언어 한국어 이름은 없다(오류 문구는 코드 목록 「가능: en, ja, th, vi, yue, zh, zh-Hant」뿐). 주석만 고쳤다 |

## 이슈 · 코디가 확인할 것

1. **데모가 켜지면 주소만 알면 누구나 로그인된다** — 결정대로이며, 데모가 끝나면 운영 Secret 에서 값을 지우고 back 을 재시작해야 한다. k8s 매니페스트(Secret 키 `INTERPRET_DEMO_LOGIN`)는 이 작업 범위 밖이라 손대지 않았다.
2. 404 문구는 다른 404 와 같게 `"Not Found"`(영문)다. front 는 404 를 「데모 꺼짐」으로만 보면 된다.
3. SPEC §2.4 env 표 · §3.3 API 표에 두 줄 추가는 planner 몫.
