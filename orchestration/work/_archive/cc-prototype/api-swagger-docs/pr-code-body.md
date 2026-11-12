## 배경

협업자가 운영 `https://ccc.medisolveai.xyz` 의 procedure API 를 직접 호출하게 됐다. 요청은 「API 에 대한 명확한 설명」과 「반환값 정의」. 지금까지 API 문서는 profile 레포의 정적 `api-reference.html`(11-02 `bf30db4` 기준)뿐이었고, 70 operation 중 설명이 있는 건 27개, 응답 필드 664개는 설명이 0이었다. 운영에서 `/docs` · `/api/openapi.json` 은 404.

사용자 결정: 문서는 **코드 기준**으로, back 에 **Swagger 로 넣고 설명을 자세하게**. 정적 html 을 손으로 고치는 대신 코드에 설명을 붙여 OpenAPI 가 늘 코드와 같이 움직이게 한다.

## 변경 내용

### 1. 문서 경로는 `/api` 아래 — `/api/docs` · `/api/redoc` · `/api/openapi.json`

- 운영 ingress 가 `/api` → back, `/` → front 라서 `/api` 아래에 두면 **인프라 변경 없이** 열린다. 기본값 `/docs` 는 front 로 가서 404 였다.
- 인증 없이 연다. 데모 · 운영을 같은 동작으로 두고 환경 분기는 넣지 않았다.

### 2. 설명은 전부 — 70 operation · 62 파라미터 · 683 필드

- 엔드포인트마다 한국어 summary · description: 허용 역할, 부수효과(KOS 쓰기 · SSE · 푸시 · DB), 멱등성, 주의점. `responses` 에는 코드에서 실제로 raise 되는 오류 코드를 service 까지 따라가며 전부 적었다.
- 모든 요청 · 응답 필드에 `Field(description=…)` 를 달았다. 뜻 · 형식 · 시간대 · enum 값의 뜻 · null 의 뜻 · 정렬을 적었다.
- app description 에 공통 규칙을 적었다: 로그인 → Bearer, 토큰 만료, 역할 다섯, 오류 형식 `{"error":{code,message}}`, 검증 오류 400, 시각 KST `+09:00`, SSE `?token=`, 공개 문진 토큰, 통역 WebSocket 프로토콜. WS 는 OpenAPI 에 안 실리기 때문이다.
- **코드로 뜻을 확인 못 한 값은 짓지 않았다.** KOS 값을 그대로 넘기는 `gender` · `nationality` 같은 칸이 그렇고, 「KOS 값 그대로」로만 적었다.
- 외부 호출자가 실제로 걸릴 자리 4곳은 설명 맨 위에 굵은 **주의**로 올렸다.
  - 예약 · 고객 생성 502 중 일부는 KOS 쓰기가 이미 된 뒤에 난다. 재시도하면 중복될 수 있다.
  - 채팅 `since` 는 `+` 를 `%2B` 로 인코딩해야 한다.
  - 지운 메시지도 `deletedAt` 에는 값이 있다.
  - 접수 뒤 5초 유지는 상세 GET 에만 적용된다.

### 3. 동작은 그대로 — 문서에만 싣는 방식

- `response_model` 은 새로 달지 않았다. 필드 거르기 · 직렬화가 바뀌기 때문이다. dict 를 돌려주는 곳은 문서용 모델을 `responses={200: …}` 로만 실었다.
- Bearer `securitySchemes` 는 `app.openapi` 를 감싸 **스키마 dict 만** 고친다(`app/openapi_docs.py`). `HTTPBearer` 의존성을 넣으면 401 모양과 `WWW-Authenticate` 헤더가 바뀌어서 기각했다.
- FastAPI 기본 `422` 표기와 `HTTPValidationError` 스키마는 문서에서 뺐다. 이 서버는 검증 오류를 400 `invalid_request` 로 바꿔서 422 를 내지 않는다.
- multipart 업로드 3개(`request.form()` 수동 파싱)는 `openapi_extra` 로 requestBody 문서만 붙였다.
- `chat.py` 는 기존 시험(데코레이터 다음 줄 = `async def`) 때문에 설명을 모듈 dict 로 빼서 `**_D_X` 로 실었다.

## 검증

- `uv run pytest -q`: 기준선 536 → **544 passed**. 새 시험 8개(`tests/test_openapi_docs.py`)가 보는 것:
  - 문서 경로 200 · `/docs` 404
  - summary · description · 파라미터 · 모든 property description 이 비면 실패
  - 422 없음
  - Bearer 표시 ⇔ `require_login` 일치(65)
  - 401 모양 그대로
  - 401 · `fake_board` 403 오류 표 ⇔ 의존성 양방향 일치
- `uv run ruff check .` 통과.
- 코디가 독립으로 다시 돌린 결과: 544 passed · ruff 통과.
- before/after OpenAPI 구조 비교(설명 · 예시 키만 빼고 `$ref` 를 풀어서 비교): 경로 64 · operation 70 · 파라미터 · 요청 본문 · 200 응답 스키마 · 기존 스키마 **차이 0**. 라우터 · 스키마 AST 비교에서도 함수 본문 차이 0.
- reviewer 워커 1판: WARN 34(문구가 코드보다 넓거나 좁은 곳). 전부 고친 뒤 재검수 PASS, 34/34 OK.

## 리뷰 포커스

**① 문서 공개** — `/api/docs` 는 인증 없이 열린다. 협업자에게 링크 하나로 주기 위해서다. 닫으려면 `docs_url=None` 으로 끄거나 앞단에 접근 제한을 둔다.

**② FastAPI 비공개 함수 사용** — Bearer 표시 대상을 고르려고 `fastapi.openapi.utils._get_api_route_for_openapi` 를 쓴다. 이 함수가 사라져도 부팅은 그대로고 `/api/openapi.json` 만 500 이 난다. 의미가 바뀌어도 security 개수 시험이 잡는다. fastapi 는 `uv.lock` 으로 0.156.4 에 고정돼 있다.

## ⚠ 배포 주의

동형 전환 — API 동작 무변경 · 배포 공지 없음. 배포 뒤 `https://ccc.medisolveai.xyz/api/docs` · `/api/openapi.json` 이 열리는지 확인한다. back 만 바뀌므로 `back.imageTag` 만 올린다.

## 후속 (이 PR 범위 밖)

- 문서를 쓰다 발견한 동작 문제 — 동작 변경 금지라 문서에 사실대로만 적었다.
  - `POST /api/display-requests/claim` · `/{id}/close` 가 소유를 검사하지 않는다.
  - `POST /api/display-requests` 에 `fake_board` 검사가 없다.
  - `POST /api/notifications/read` 를 조건 없이 부르면 안 읽은 전부를 읽음 처리한다.
  - 예약 생성 중 고객만 KOS 에 남을 수 있다.
  - 그 밖 몇 건.
- 시술 · 상품 종류 API — 아직 없다. KOS `procedure-menu` 공개 API(카테고리 · 상품 · 옵션 · 시술)를 감싸는 엔드포인트가 필요하다.
- profile 레포의 정적 `api-reference.html` 은 이 Swagger 로 대체한다(별도 처리).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
