# [backend] procedure back — Swagger(`/api/docs`) + 엔드포인트 · 반환값 상세 설명

너는 **cc-prototype `backend` 워커**다. **앞 맥락이 하나도 없다** — 이 브리프와 아래 파일만 믿어라. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/roles/cc-prototype/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs`
base 브랜치: `origin/main`(`77173cf`) → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리는 너 혼자 쓴다. 끝난 뒤 reviewer 워커가 같은 워크트리를 read-only 로 본다.

## 1. SSOT — 먼저 읽을 것

**설명의 SoT 는 코드다.** 코드가 실제로 하는 것만 적는다. SPEC 은 「왜 · 무슨 뜻인지」를 풀어 쓸 때 참고로만 본다. SPEC 과 코드가 다르면 **코드대로 쓰고**, 다른 점은 리포트 「SPEC ↔ 코드 차이」에 모아라(고치지 않는다).

- 코드: `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs/procedure/back/app/` (api · schemas · service · domain · repository)
- 참고 SPEC(read-only · 코디 워크트리 절대경로) — `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/para/projects/summer-star/cc-prototype/20-spec/`
  - `spec-003-procedure-board.md` §4 · §7 · §8 — 현황판 · 조작 API
  - `spec-004-procedure-app.md` §3.2~3.4(로그인 · 역할 검사표) · §4.3(통역 WS) · §7(SSE · API)
  - `spec-005-reservation-board.md` §7 — 예약 현황 API
  - `spec-006-customer-questionnaire-web.md` §6 — 공개 문진 API(토큰)
  - `spec-007-internal-chat.md` §6 — 채팅 API
- 지금 있는 정적 레퍼런스(read-only · 비교용): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/reference/2026-10-27-cc-app/api-reference.html` — `bf30db4` 기준, OpenAPI JSON 이 박혀 있다. 엔드포인트 71개 중 설명이 있는 건 28개뿐이고, 응답 필드 664개에는 설명이 하나도 없다. **이 파일은 고치지 않는다.**

**따를 개념** — 해당 없음. 대신 아래 원칙을 지킨다.
- **없는 정보를 짓지 않는다.** 코드에서 확인 못 한 의미 · 단위 · 값은 쓰지 않고 리포트 「확인 못 한 것」에 남긴다. 추정한 설명은 금지한다.
- **동작을 바꾸지 않는다.** 응답 바이트 · 상태 코드 · 오류 코드 · 인증 동작이 전부 그대로여야 한다.

## 2. 배경 / 무엇을 바꾸나

협업자가 운영 서버 `https://ccc.medisolveai.xyz` 의 API 를 호출하려 한다. 그쪽 요청은 두 가지다.
1. 「해당 API 에 대한 명확한 설명」
2. 「반환값에 대한 정의 설명」

지금 운영에는 Swagger 가 안 열린다. `/docs` 는 ingress 에서 front 로 가서 404 가 나고, `/api/openapi.json` 도 404 다. 설명은 함수 이름(`Login`, `Board`) 수준뿐이다.

→ back 에 Swagger 를 `/api` 아래로 열고, **모든 엔드포인트와 모든 요청 · 응답 필드**에 한국어 설명을 단다. 운영 ingress 는 `/api` → back, `/` → front 라서 **인프라 변경 없이** 열린다.

## 3. 계약

- `FastAPI(docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json")`. 인증 없이 연다(데모 · 운영 같은 동작 · 환경 분기 금지)
- `title` 은 사람이 읽을 이름으로 바꾼다(예: 「CCC procedure API」). `version` 은 그대로 둔다. app `description` 에 **공통 규칙**을 쓴다.
  - 호스트(`https://ccc.medisolveai.xyz`)
  - 인증: `POST /api/auth/login` → `Authorization: Bearer <토큰>` · 토큰 수명 · 만료 동작(코드 기준)
  - 역할 다섯(admin · doctor · nurse · coordinator · counselor)과 역할 403
  - 오류 형식 `{"error":{"code","message",...}}` · 요청 검증 오류 = 400 `invalid_request` · 404 `not_found`
  - 공개 문진 = `X-Questionnaire-Token` · SSE = `?token=` · 업로드 = multipart · 다운로드 = 바이너리
  - 시각 · 날짜 형식과 시간대(코드 기준)
  - 통역 WebSocket `WS /api/interpret` 의 연결 · 메시지 모양. FastAPI 는 WS 를 OpenAPI 에 안 싣기 때문에 description 에 적는다
- Swagger 「Authorize」 버튼으로 Bearer 를 넣을 수 있게 `securitySchemes`(HTTP bearer)를 OpenAPI 에 싣는다. **인증 판정 코드(`require_login` 등)와 401 응답 모양은 그대로** 둔다. 문서에만 싣는 방법을 써라(예: `openapi_extra` · `app.openapi` 커스터마이즈 · `dependencies` 에 문서용 security). 어떤 방법을 썼는지와 그 방법이 동작을 안 바꾼다는 근거를 보고한다
- 라우터마다 `tags`(한국어)와 tags 설명을 단다 — 인증 · 현황판 · 조작 · 예약 · 고객 · 알림 · 기기 · 표시 요청 · 공개 문진 · 신분증 사진 · 채팅 · 상태
- **엔드포인트마다**:
  - `summary`: 한국어 한 줄
  - `description`: 무엇을 하는지 · 누가 부르나(허용 역할) · 부수효과(KOS 쓰기 여부 · SSE 이벤트 발행 · 푸시 · DB 변경) · 멱등성 · 주의점
  - `responses`: 이 엔드포인트가 **실제로 낼 수 있는** 오류 코드를 모두 적는다. 코드를 따라가며 raise 되는 `DomainError` 하위를 셀 것. 400 · 401 · 403 · 404 · 409 와 코드 문자열, 언제 나는지
- **모든 요청 · 응답 모델의 모든 필드**에 `Field(description=...)`. 뜻 · 단위 · 형식(ISO 시각 · 시간대) · enum 값 각각의 뜻 · `null` 일 때의 뜻 · 배열이면 정렬 순서. 응답 모델이 없어 dict 를 돌려주는 엔드포인트는 **문서용 모델**을 만들어 `responses={200: {"model": ...}}` 로 싣는다. 이때 **`response_model` 을 새로 달지 마라** — 필드 거르기 · 직렬화가 바뀐다. 이미 있는 `response_model` 은 그대로 둔다
- 예시(`examples`)는 **가짜 값만** 쓴다. 실명 · 실 연락처 · KOS id · 키 · 토큰은 쓰지 않는다. public 레포다

## 4. 먼저 읽을 핵심 파일

- `procedure/back/app/main.py:86` — `FastAPI(...)` 생성 · 예외 핸들러(오류 형식) · 라우터 등록
- `procedure/back/app/api/deps.py` — `require_login` · `require_real_board` · 검사 순서(401 → 403 fake_board → 역할 403 → 404 → 409)
- `procedure/back/app/api/*.py` 12개 — 엔드포인트 전부. 각 함수가 부르는 `service/` 를 따라가 반환 모양 · 오류를 확인한다
- `procedure/back/app/schemas/*.py` · `app/domain/` — 지금 요청 · 응답 모델과 alias(camelCase)
- `procedure/back/app/domain/errors.py` — 오류 클래스 · 코드

## 5. allowed_paths — 이 밖은 건드리지 마라

- `procedure/back/` 만
- (`procedure/docker-compose.yml` · `procedure/.env.example` 은 이번엔 바꿀 일이 없다. 바꿔야 하면 먼저 물어라)

## 6. 구현 단계

1. **기준선**: 고치기 전에 `uv run pytest -q` · `uv run ruff check .` 수치를 잰다. 앱을 띄우지 말고 `create_app()` 에서 `app.openapi()` 를 덤프해 `work` 리포트 옆에 `openapi-before.json` 으로 둔다(경로는 §8)
2. `main.py`: 문서 경로 세 개 · title · app description(§3 공통 규칙) · tags 설명 · securitySchemes
3. 라우터 12개: 엔드포인트마다 summary · description · responses(오류 전수)
4. 모델: 모든 필드 description. dict 응답은 문서용 모델 + `responses`
5. **동작 불변 증명**:
   - pytest 전부 통과(기준선과 같은 수)
   - `openapi-after.json` 덤프를 before 와 비교한다. **경로 · 메서드 · 파라미터 · 요청 본문 필드 이름 · 타입이 같아야** 한다(늘어난 건 설명 · 예시 · tags · security · 문서용 응답 모델뿐이어야 한다). 비교 스크립트 결과를 리포트에 붙인다
   - TestClient 로 `GET /api/docs` 200 · `GET /api/openapi.json` 200 · `GET /docs` 404 를 시험으로 추가한다
   - 설명 빠진 곳 0을 시험으로 고정한다: openapi.json 을 돌며 **모든 operation 의 summary · description**, **모든 schema property 의 description** 이 비어 있지 않은지 본다
6. 리포트 작성(§8)

## 7. 범위 제약 — 하지 말 것

- 동작 변경 금지 — 로직 · 응답 모양 · 상태 코드 · 오류 코드 · 인증 · CORS 를 바꾸지 않는다. 설명을 쓰다 버그를 보면 **고치지 말고** 리포트에 적는다
- **시술 · 상품 종류 API 를 새로 만들지 않는다**(미완 — 이번 범위 아님)
- 기존 `response_model` 추가 · 제거 금지. alias · 필드 이름 변경 금지
- `procedure/front` · `procedure/app` · `cc/` · infra · 정적 `api-reference.html` 무수정
- 확인 못 한 의미를 지어 쓰지 않는다 — 「확인 못 한 것」 목록으로
- 사용자 포트 · 프로세스 금지(서버를 띄우지 말고 TestClient · `app.openapi()` 로)
- 커밋 · push · PR 금지

## 8. 검증

```
procedure/back 에서 uv run pytest · uv run ruff check . — Phase 범위에 맞게 1회씩, 통과하면 반복하지 마라. 기능 폴더 밖 import 가 없는지 확인. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

**리포트**(필수): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/be-report.md`. `openapi-before.json` · `openapi-after.json` 도 같은 폴더에 둔다(이 세 파일만 쓴다).
1. 변경 파일 목록
2. 기준선 → 이후 수치(pytest · ruff)
3. before/after OpenAPI 비교 결과 — 구조 변화 0의 증거
4. 커버리지: operation 수 · summary/description 채운 수 · schema property 수 · description 채운 수(**전부 = 전부**)
5. securitySchemes 를 어떻게 실었는지와 동작이 안 바뀐다는 근거
6. 확인 못 한 것(코드로 뜻을 못 정한 필드 · 값)
7. SPEC ↔ 코드 차이 · 보다가 발견한 버그(고치지 않음)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
