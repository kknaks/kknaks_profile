# WORK-001 검수 리포트

- 대상: 워크트리 `/Users/kknaks/orca/workspaces/task_management/work-001-scaffold`, 브랜치 `kknaksss/work-001-scaffold`
- 범위: `origin/main..HEAD` 커밋 2건 — `2a4d29a`(Phase 1·2 백엔드) · `84882c0`(Phase 3·4 프론트+Tauri). 97 파일 / +15,601. 작업 트리 clean(untracked 없음)
- 판정 기준: DEC-001 · `40-architecture/{backend,frontend,database,system}` · SPEC-000 · WORK-001
- 방식: **read-only.** 코드·문서를 고치지 않았고 테스트·빌드를 돌리지 않았다

## 판정 요약

| 층 | 판정 | 근거 |
|---|---|---|
| **정책** (DEC-001) | **PASS** | 계정 생성 경로가 시드뿐(회원가입 라우터·화면·API 0건) · 비밀번호는 bcrypt 해시만 저장하고 8자+문자·숫자·특수문자를 시드 진입점에서 강제 · 기본 유형 3종이 `is_default=true` 로 시드 · v2 컬럼 없음(A-10 · G-8) · 자동 재시도 없음(`retry:false`) |
| **아키텍처 — 백엔드** | **PASS** (WARN 1) | router→service→repository 한 방향 · ORM 모델이 repository 를 넘지 않음 · schema/dto 분리 · `except Exception` 0건, 포착 2종 전부 구체 타입 · `Settings` 하나 · 비밀값 기본값 없음 · CORS 명시 목록 + `allow_credentials=False`. WARN 은 `alembic/env.py` 주석의 env 이름 오기 1건 |
| **아키텍처 — 프론트** | **WARN** | 정적 빌드 제약·토큰 저장소 격리·전역 상태 없음·hex 0건은 전부 충족. 다만 ① 실패 경로에서 진단 요청 1건이 더 나가고 ② `gutter` 보간값이 FE §7-1 표와 어긋난다(1440 에서 96px, 표는 80px) |
| **SPEC** (SPEC-000) | **WARN** | 헬스 응답 형태·시드 계약·환경변수·CORS·Case Matrix 5행 전부 구현. 다만 §5 「재시도를 걸지 않는다」와 §4 Case Matrix 「CORS 차단 / 네트워크 실패를 다른 문구로」가 코드에서 충돌해 요청 1건이 더 나간다(문서 공백 D-1 과 짝) |
| **WP** (WORK-001) | **PASS** | Phase 1~4 작업 체크리스트가 코드 기준으로 전부 이행 · 범위 밖 침범 없음(백 워커는 `app/front` 를, 프론트 워커는 `app/back` 을 건드리지 않았다) · WORK-002·003 선행 구현 없음. **다만 Phase 검증 항목 중 실행이 필요한 것(빌드·기동·pytest)은 이 리뷰가 확인하지 않았다** — §코디 실행 요청 |

**FAIL 0건 / WARN 3건 / 문서 공백 18건**(워커가 올린 6건 재판정 + 신규 12건)**.**

## FAIL — 반드시 고쳐야 하는 것

없다. 정책·계약 위반과 Phase 검증 항목의 코드 수준 미충족을 찾지 못했다.

## WARN — 규약에서 벗어났으나 동작하는 것

| # | 파일:줄 | 무엇이 어긋났나 | 어긋난 문서 절 | 어떻게 고치나 |
|---|---|---|---|---|
| W-1 | `app/front/src/lib/api/client.ts:34-41` · 호출부 `:73-82` | `fetch` 가 던지면 같은 URL 로 `mode:"no-cors"` 요청을 **한 번 더** 보낸다(CORS 차단과 서버 다운을 구분하려는 진단). 실패 경로에서 「다시 확인」 1회 = 네트워크 탭에 `/api/health` 2건 | WORK-001 Phase 3 검증 「**「다시 확인」은 요청을 한 번만 보낸다**」 · SPEC-000 §5 헬스 규칙 「프론트는 이 호출에 재시도를 걸지 않는다 … 재시도는 사용자가 「다시 확인」을 누를 때만」 | **코드가 아니라 문서를 먼저 정해야 한다**(D-1). 브라우저 `fetch` 는 CORS 차단과 서버 다운을 같은 `TypeError` 로 던져 **한 요청으로는 구분이 불가능**하다 — SPEC-000 §4 가 두 문구를 요구하는 한 진단 요청은 필수다. 코디가 ① §5 에 「진단 요청 1회는 재시도가 아니다」를 명시하고 Phase 검증 문구를 「헬스 요청은 한 번만」으로 다듬거나, ② §4 의 CORS 행을 네트워크 실패 행에 합쳐 진단 요청을 걷어내게 한다 |
| W-2 | `app/front/tailwind.config.ts:114` | `gutter: clamp(48px, calc(48px + (100vw - 1280px) * 0.3), 240px)` — 1280 에서 48 ✓, 1920 에서 240 ✓ 이지만 **1440 에서 96px** 이 나온다. 표의 값은 80 이고, 1280~1439 구간은 48 **고정**이라 단일 clamp 로는 두 구간을 함께 만족시킬 수 없다 | `frontend/README.md` §7-1 세 구간 표 — 「1280~1439: 여백 48」 / 「≥1440: 80 → 240 으로 연속 보간(1440 에서 80, 1920 에서 240)」 | 구간을 나눈다. 예) 기본 `--gutter: 48px`, `@media (min-width:1440px) { --gutter: clamp(80px, calc(80px + (100vw - 1440px) / 3), 240px) }` 로 두고 Tailwind `spacing.gutter` 가 그 변수를 가리키게 한다. 지금은 `ConnectionCheckScreen` 한 곳만 쓰지만 이후 전 화면이 이 값을 탄다 |
| W-3 | `app/back/alembic/env.py:27` vs `:28` | docstring 은 「**`TEST_DATABASE_URL`** 이 이긴다」인데 코드가 읽는 것은 `ALEMBIC_DATABASE_URL` 이다. 주석을 믿고 `TEST_DATABASE_URL` 만 export 한 사람은 운영 DB 에 마이그레이션을 걸게 된다 | — (문서 절 아님. **코드 내부 불일치**다. 참고: SPEC-000 §5 환경변수 표에 두 이름 모두 없다 → D-2) | 주석을 `ALEMBIC_DATABASE_URL` 로 바로잡는다. 이름 자체는 `tests/conftest.py:41` 이 세팅하는 값과 맞아 동작에는 문제가 없다 |

## 문서 공백 — 코드가 아니라 문서를 고쳐야 하는 것

### 코드 워커가 올린 6건 (재판정) + 그와 짝이 되는 신규 1건

| # | 무엇이 비었나 | 어느 문서 어느 절 | 무엇을 적어야 하나 | 판정 |
|---|---|---|---|---|
| D-1 | **SPEC-000 §4 Case Matrix 가 「CORS 차단」과 「네트워크 실패」를 다른 문구로 요구하는데, 브라우저 `fetch` 는 둘을 구분해 주지 않는다.** 구분하려면 진단 요청이 1건 더 나가야 하고, 그것이 §5 「재시도를 걸지 않는다」와 부딪힌다 | `20-spec/spec-000-scaffold.md` §5 「헬스 규칙」 + §4 Case Matrix + WORK-001 Phase 3 검증 3번째 항목 | 둘 중 하나를 고른다. **(a)** §5 에 「사유를 가르기 위한 **진단 요청 1회**는 재시도가 아니다. 헬스 요청 자체는 한 번만 나간다」를 추가하고 Phase 3 검증 문구를 그에 맞춘다. **(b)** §4 의 CORS 행을 지우고 「서버가 응답하지 않습니다 · <대상 주소>」 한 문구로 합친다 — 대신 **Acceptance 「허용 origin 에서 앱 창 origin 을 빼면 CORS 실패로 뜬다」(§6)** 가 「연결 실패로 뜬다」로 약해진다는 것을 명시한다. **(a) 를 권한다** — 스캐폴딩이 origin 문제를 미리 잡는 자리라는 §5 CORS 절의 목적이 (b) 에서 사라진다 | **신규(이 검수)** — 코드가 아니라 SPEC 이 정할 문제다. W-1 과 짝 |
| D-2 | `APP_VERSION` · `TEST_DATABASE_URL` 이 환경변수 표에 없다 | `20-spec/spec-000-scaffold.md` §5 「환경변수」 표 | 두 행을 추가한다. `APP_VERSION` — 쪽 back / 필수 ✖(기본 `0.1.0`) / 「헬스 응답 `version` 으로 그대로 나가는 배포 단위 버전 문자열」. `TEST_DATABASE_URL` — 쪽 back(테스트) / 필수 ✖(테스트 실행 시 ✔) / 「`make test` 전용 별도 DB」. **`ALEMBIC_DATABASE_URL` 도 같이 넣는다**(아래 D-8) | **유효** |
| D-3 | `DatabaseUnavailableError`(503)를 AppError 5종 밖에 신설했다 | `40-architecture/backend/README.md` §8-2 「도메인 예외 → HTTP」 트리 + code 표 | 예외 트리에 `DatabaseUnavailableError 503` 을 6번째 가지로 넣고, code 표에 `db_unavailable / 503 / DB 왕복 실패 / SPEC-000 §4` 행을 추가한다. **덧붙여 「5종은 도메인 판정, 인프라 가용성 실패는 별개 가지」라는 분류 원칙 한 줄**을 적어 이후 work 가 같은 판단을 반복하지 않게 한다 | **유효** — 코드 쪽은 §8-1 「설계한 실패만」을 오히려 지켰다(SPEC-000 §4 가 명시한 실패다). 지적 아님 |
| D-4 | **시드가 기본 유형 `color_token` 을 재실행 때 덮어쓰지 않는다** — SPEC-000 §5 「값이 다르면 시드 값으로 맞춘다」 vs DEC-001 §4·A-4 「기본 유형은 **색만 편집 가능**」이 충돌 | `20-spec/spec-000-scaffold.md` §5 「시드 계약 · 멱등」 행 | 멱등 행을 조건부로 고쳐 쓴다 — 「이미 있으면 만들지 않는다. **잠긴 값(기본 유형의 이름·종류·`is_default`, 계정의 이름·이메일·비밀번호)만 시드 값으로 맞추고, 사용자가 편집할 수 있는 값(`work_type.color_token`)은 새로 만들 때만 넣는다**」. 코드(`seed/seed.py:59-93`)가 이미 그렇게 돼 있어 문서만 따라오면 된다 | **유효 · 코드가 맞다.** A-4 가 상위 규칙이므로 색을 덮어쓰는 쪽이 정책 위반이 된다 |
| D-5 | CSP `script-src` 에 `'unsafe-inline'` 이 필요하고(정적 export 의 부트스트랩 인라인 스크립트 · 미들웨어가 없어 nonce 자리 없음), `connect-src` 의 API 주소가 빌드 시점 고정이다 | `40-architecture/system/README.md` §Components(Tauri 셸 행) 또는 SYS-3 아래 · `frontend/README.md` §1-3 | CSP 규약 절을 새로 만든다. ① `default-src 'self'` 로 외부 origin 차단이 SYS-3 의 실질 강제 지점이라는 것 ② **`script-src 'unsafe-inline'` 은 정적 export 의 구조적 결과라 허용**하되 외부 스크립트 금지는 유지 ③ `connect-src` 에 API origin 을 적어야 하므로 **`NEXT_PUBLIC_API_BASE` 를 바꾸면 `tauri.conf.json` 도 같이 바꾼다**를 릴리스 체크리스트로 못박는다(현재 `app/front/README.md:48-54` 에만 적혀 있다) | **유효** |
| D-6 | 프론트 버전 핀(Next 15.5.25 · React 19.2.8 · Tailwind **v3** 유지 · Node 20.11+)을 이 work 가 정했다 | `40-architecture/frontend/README.md` §0 다섯 제약 아래 「스택 핀」 표 신설 · WORK-001 §Open Issues 해당 항목 해소 표기 | 표를 옮겨 적고, **Tailwind v3 유지 사유를 FE-OQ-2(브라우저 하한 미정)에 명시적으로 건다** — v4 는 `@property`·`color-mix()` 등 최신 CSS 를 전제하므로 하한이 정해지기 전에는 v3 가 안전하다는 근거. Python 3.12(`app/back/.python-version`)는 아직 어느 README 에도 적히지 않았다(D-7 과 함께 처리) | **유효** |
| D-7 | 루트 `README.md` 가 어느 워커의 allowed_paths 에도 없어 기동 절차가 `app/front/README.md` 에만 있다 | `orchestration/config/projects/task-management.json` 의 워커 allowed_paths + WORK-001 §Code Surface 표(「`README.md` · `Makefile` — 로컬 기동 절차 한 곳」) | ① 다음 work 발주부터 루트 `README.md` 를 **be·fe 양쪽 allowed_paths** 에 넣거나 ops 몫으로 분리한다. ② 이번 건은 코디가 루트 `README.md` 에 4줄 기동 절차(`make up → migrate → seed → app`)와 버전 핀(Node·Python·Rust)을 옮겨 적어 `app/front/README.md` 는 프론트 전용으로 남긴다. WP §Code Surface 가 「기동 절차 한 곳」이라 적었으므로 **현재는 그 계약이 깨져 있다** | **유효** |

### 이 검수에서 새로 찾은 것 (계속)

| # | 무엇이 비었나 | 어느 문서 어느 절 | 무엇을 적어야 하나 |
|---|---|---|---|
| D-8 | **compose 전용 변수와 alembic 전용 변수가 환경변수 표에 없다.** 코드가 실제로 요구하는 것: `POSTGRES_USER`·`POSTGRES_PASSWORD`·`POSTGRES_DB`·`POSTGRES_PORT`·`API_PORT`(`docker-compose.local.yml:11-15,35`) · `ALEMBIC_DATABASE_URL`(`app/back/alembic/env.py:28`) | `20-spec/spec-000-scaffold.md` §5 「환경변수」 표 | 표를 **3구획**으로 나눈다 — 「API 프로세스가 읽는 것(`Settings`)」 / 「compose 가 읽는 것」 / 「도구 전용(테스트·마이그레이션)」. 지금은 한 표라 「비밀값 기본값 금지」가 `POSTGRES_PASSWORD` 에도 걸리는지 알 수 없다(현재 `.env.example:7` 은 값이 채워져 있다). **로컬 compose 비밀번호는 예시값을 채워도 되는지**를 그 구획에 명시한다 |
| D-9 | **시드가 기본 유형 3종을 무엇으로 식별하는지 정해져 있지 않다.** 계정은 「로그인 식별자 기준」이라고 적혀 있지만 유형은 없다 — 코드가 **이름**을 키로 골랐다(`app/back/seed/seed.py:68-72`). `work_type` 에는 이름 유니크 제약이 없어(`database/README.md` §4), WORK-003 이 유형 생성을 열면 사용자가 「개인 업무」를 만들었을 때 다음 시드 실행이 그 행을 `is_default=true` 로 뒤집는다 | `20-spec/spec-000-scaffold.md` §5 「시드 계약 · 기본 유형」 행 + `database/domains/account.md` A-4 | 식별 키를 못박는다. 권장 — 「기본 3종은 **`(account_id, is_default=true, kind, name)`** 로 찾는다」 또는 A-4 에 「기본 3종의 이름은 예약어다 — 사용자가 같은 이름의 유형을 만들 수 없다(`work_type_locked` 또는 `409`)」를 추가한다. **후자면 WORK-003 의 검증 항목이 하나 늘어난다** |
| D-10 | **`AsyncSession` 이 router → service → repository 를 그대로 타고 내려간다**(`api/health_router.py:18` → `service/health_service.py:11` → `repository/health_repository.py:12`). §2 표는 router 의 금지 항목으로 「`AsyncSession` 으로 **직접 쿼리**」만 적었고, service 의 금지 목록에는 세션이 없다 — **세션이 어느 층까지 내려가는지가 규약에 없다** | `40-architecture/backend/README.md` §2 계층 표 아래 · §7 트랜잭션 경계 | 한 줄로 못박는다. 권장 — 「**세션 핸들은 층을 탄다.** router 가 `Depends(get_db)` 로 받아 service 에 넘기고 service 가 repository 에 넘긴다. 금지되는 것은 **모델**이 repository 를 넘는 것과 router·service 가 세션으로 **직접 쿼리하는 것**이지 세션을 전달하는 것이 아니다」. 지금 코드는 이 해석과 일치하지만 **규약이 침묵해서 다음 워커가 repository 안에서 세션을 만드는 반대 설계를 고를 수 있다** |
| D-11 | **클라이언트가 만드는 `code` 가 어느 표에도 없다** — `network_unreachable`·`cors_blocked`(`lib/api/errors.ts:37-42`) · `http_<status>`(`lib/api/client.ts:50,56`). FE §3-5 는 「화면은 `code` 로 분기한다」고 하는데 그 표에는 백엔드 code 만 있다 | `40-architecture/frontend/README.md` §3-5 code 표 | 표에 **「클라이언트 생성 code」 구획**을 만든다 — `network_unreachable` / `cors_blocked` / `http_<status>`(백엔드가 `code` 를 안 실은 응답의 폴백). SPEC-000 §4 Case Matrix 의 프론트 전용 두 행에도 이 code 이름을 적어 SPEC 과 아키텍처가 같은 이름을 쓰게 한다 |
| D-12 | **Case Matrix 에 없는 다섯 번째 실패 문구가 코드에 있다** — `ApiError` 가 아닌 예외일 때 「알 수 없는 오류입니다」(`features/health/components/ConnectionCheckScreen.tsx:24-25`) | `20-spec/spec-000-scaffold.md` §4 Case Matrix | 행을 추가하거나(권장 — 「(그 밖 · 클라이언트 예외) → 「서버에 연결하지 못했습니다」 + 「알 수 없는 오류입니다」」) 「§4 는 **서버까지 간 실패**의 SoT 이고 클라이언트 내부 예외는 §3-5 가 덮는다」를 명시한다. 지금은 「**설계한 실패는 이 다섯뿐이다**」(§4 말미)와 코드가 문자 그대로 어긋난다 |
| D-13 | **`invalid_password` code 가 §8-2 code 표에 없다**(`app/back/core/security.py:35`). WORK-001 에서는 시드 CLI 안에서만 쓰여 HTTP 로 나가지 않지만, SPEC-001 의 비밀번호 변경이 그대로 이 예외를 탄다 | `40-architecture/backend/README.md` §8-2 code 표 | `invalid_password / 422 / 비밀번호 규칙(8자+문자·숫자·특수문자) 위반 / DEC-001 §3` 행을 추가한다. **WORK-002 착수 전에 필요하다** — 프론트가 분기할 키다 |
| D-14 | **오버레이 스택 규약이 한 방향만 정한다.** 「드로어 위 모달 금지」는 구현돼 있지만(`lib/overlay/OverlayProvider.tsx:55-70`, 개발 모드 throw / 운영 모드 드로어 교체 — §6-2 그대로) **모달 위에 드로어를 여는 반대 방향**은 규약이 없어 코드가 그냥 쌓는다(`:50-53`) | `40-architecture/frontend/README.md` §6-2 강제 규칙 표 | 한 줄 추가한다 — 「confirm 이 열린 상태에서 `openDrawer` 가 오면 …」. 권장은 「**모달이 열려 있으면 드로어를 열지 않는다**(모달은 결정 하나라 그 위에 편집이 얹힐 자리가 없다)」. 지금 정해 두지 않으면 화면마다 다르게 쌓인다 |
| D-15 | **「다른 파일에서 `process.env` 를 직접 읽지 않는다」의 범위가 불명확하다.** `OverlayProvider.tsx:61` 이 §6-2 의 「**개발 모드에서 throw**」를 구현하려고 `process.env.NODE_ENV` 를 읽는다 — 규칙을 문자 그대로 읽으면 위반이지만, 규칙을 지키면 §6-2 를 구현할 수 없다 | WORK-001 §Internal Interface Contract 「프론트 API 베이스」 행 · `frontend/README.md` §2 디렉토리 규칙 | 범위를 좁혀 적는다 — 「**`NEXT_PUBLIC_*` 를 읽는 곳은 `lib/env.ts` 하나다.** `NODE_ENV` 같은 빌드 상수는 예외」. 이후 work 의 WP 가 같은 문장을 복제하므로 지금 고쳐야 한다 |
| D-16 | **SPEC-000 S000-OQ-2 가 절반만 해소됐다.** `system/README.md` Overview 본문·SYS-9 와 `frontend/README.md` FE-C2 는 「처음부터 Tauri」로 정정됐지만, **같은 문서의 mermaid 다이어그램 subgraph 라벨(「개발은 브라우저 / 배포는 Tauri」·노드 「Tauri 셸 (래핑 후에만)」)** 과 **§Components 표의 「**Tauri 셸** (래핑 후)」**, 그리고 **SYS-3 결정 요약(「래핑 후 OS 키체인 / 웹 개발 중 브라우저 저장소」)** 이 아직 번복 이전이다. 여기에 **DEC-001 §4 「웹 개발 단계 보관」 행**(「Tauri 래핑은 마지막이므로 그동안은 브라우저 저장소를 임시로 쓴다」)도 번복 이전 상태다 | `40-architecture/system/README.md` Overview mermaid · §Components 표 · SYS-3 행 / `10-decision/decision-001-auth-settings.md` §4 「웹 개발 단계 보관」 행 | 넷을 §C-4 번복에 맞춘다. 특히 **DEC-001 §4 는 정책서라 파급이 크다** — 코드(`lib/auth/tokenStore.ts:44-51`)는 FE-C2 를 따라 `persist=true` 를 **브라우저 저장소로 대체하지 않고 예외를 던지도록** 만들어 뒀다. 정책서가 옛 상태로 남아 있으면 WORK-002 워커가 브라우저 저장소 폴백을 되살릴 수 있다 |
| D-17 | **「같은 정적 산출물」의 뜻이 SPEC 안에서 갈린다.** §1 Scope 는 「개발(`tauri dev`)과 배포 번들이 **같은 정적 산출물**을 싣는다」인데, §5 기동 계약과 §4 Flow 주석은 「dev 는 개발 서버」다. 코드는 후자(`tauri.conf.json:7-8` — `frontendDist: ../out` + `devUrl: http://localhost:3000`) | `20-spec/spec-000-scaffold.md` §1 Scope 첫 항목 | §1 을 「개발은 프론트 개발 서버를, 배포 번들은 `out/` 정적 산출물을 싣는다. **둘이 같은 소스·같은 빌드 설정**을 쓴다」로 고친다. 지금 문구는 「dev 에서도 `out/` 을 실어야 한다」로 읽혀 HMR 을 포기하는 구현을 부를 수 있다 |
| D-18 | **버전 문자열의 정본이 어디인지 정해져 있지 않다.** 지금 `0.1.0` 이 다섯 곳에 각각 있다 — `.env.example:32`(`APP_VERSION`) · `app/back/pyproject.toml:3` · `app/front/package.json:3` · `src-tauri/tauri.conf.json:4` · `src-tauri/Cargo.toml:3`. 헬스 응답이 보여 주는 것은 그중 `APP_VERSION` 하나뿐이다 | `20-spec/spec-000-scaffold.md` §4 Request/Response(`version` 설명) 또는 `system/README.md` §런타임 배치 | 「`version` 의 정본은 **`APP_VERSION`** 이고, 릴리스 시 다섯 자리를 함께 올린다」 또는 「백엔드 버전과 앱 번들 버전은 별개 축이다」 중 하나를 못박는다. v1 배포 시점에 반드시 부딪힌다 |

## 확인한 것 (PASS 근거)

**정책 (DEC-001)**

- 계정 생성 경로: `grep -rni "signup|register|/login|auth_router"` → `app/back`·`app/front/src` **0건**. 계정을 만드는 코드는 `seed/seed.py:41-56` 하나뿐이다(DEC-001 §2)
- 비밀번호: `core/security.py:39-41` bcrypt 해시만 저장 · `:21-36` 이 8자·문자·숫자·특수문자를 검사하고 위반 시 `ValidationError` · `run_seed:98` 이 **upsert 앞에서** 부른다(위반이면 행이 하나도 안 들어간다 — `tests/test_seed.py:69-87` 이 검증). 평문은 로그·메시지 어디에도 없다(`seed.py:136-143` 은 행 수만 찍는다)
- 기본 유형 3종: `seed/seed.py:34-38` — 「미팅·회의」(`meeting`) · 「개인 업무」(`task`) · 「문서·보고」(`task`), 셋 다 `is_default=True`(`:82`, 재실행 시 `:88`). SPEC-000 §4 Data Contract 와 일치
- v2 컬럼 없음: `models/account.py` 에 소셜·목소리·연동·계정 삭제·기기 목록 컬럼이 없다(A-10 · G-8). 「업무 시간」 필드도 없다(A-11)
- 소프트 딜리트: `work_type`·`project` 에만 `deleted_at`(§0-1 대상 목록과 일치). `career`·`auth_session`·`account` 에는 없다

**아키텍처 — 백엔드**

- 계층: `health_router.py:11` → `service`, `health_service.py:8` → `repository`, `health_repository.py` → SQL. 역방향·건너뛰기 없음. router 만 `schemas/` 를 import 하고(`health_router.py:10`) service 는 `dto` 만 본다(`health_service.py:7`)
- ORM 모델 경계: repository 가 모델을 반환하지 않는다(`ping()` 은 `None`). 모델을 다루는 곳은 `seed/seed.py`(계층 밖 CLI)와 `models/` 뿐
- 실패 처리: `grep -rn "except" app/back --include='*.py'` → 포착 **2곳**. `config.py:88,100`(`PydanticValidationError`) · `health_repository.py:20`(`OperationalError, InterfaceError`). **`except Exception`·bare except 0건**, 둘 다 재전파(`raise … from exc`)한다. 조용한 기본값·임의 재시도 없음(§8-1 · BE-7)
- 설정: env 를 읽는 곳은 `config.py` 하나. 필수 4종(`DATABASE_URL`·`JWT_SECRET`·`CORS_ORIGINS`·`STORAGE_ROOT`)이 `Field(min_length=1)` 이라 **없거나 빈 값이면 기동 실패**하고 누락 이름이 로그·예외 메시지에 남는다(`:75-94`). `.env.example:18,37-40` 이 비밀값을 빈 칸으로 둔다
- CORS: `main.py:33-39` — `allow_origins=settings.cors_origin_list`(쉼표 분해 명시 목록) · **`allow_credentials=False`** · `*` 없음(`tests/test_health.py:68-77` 이 검증)
- 예외 → HTTP: 핸들러는 `main.py:41` **한 곳**. 응답은 `{"detail","code"}` 고정(`:20-23`)
- 스키마: `models/account.py` 5 테이블이 `database/README.md` §1 ERD 컬럼과 1:1. 인덱스 4종이 §4 표와 일치(`uq_account_login_id` · `uq_auth_session_refresh_token_hash` · `(account_id, expires_at)` · `work_type`/`project` 의 `(account_id) WHERE deleted_at IS NULL`). enum 은 varchar+CHECK(G-3), PK 는 `bigint IDENTITY`(G-1), 시각은 `timestamptz`(G-2), 공통 믹스인(G-6), 색은 팔레트 토큰 CHECK(A-5)
- 마이그레이션: 리비전 1건 + `downgrade` 작성(§0-2). CHECK·부분 인덱스가 손으로 들어가 있어 autogenerate 초안을 그대로 커밋하지 않았음이 드러난다. 시드는 리비전에 섞이지 않았다
- 드라이버: 앱 async(`core/db.py:17`)·alembic/시드 sync(`alembic/env.py:48`, `seed.py:128`) 가 **같은 `postgresql+psycopg://`**(§5)

**아키텍처 — 프론트**

- 정적 빌드: `next.config.ts:11-15` 가 `output:'export'`·`trailingSlash`·`images.unoptimized`. `src/app` 아래 파일은 `layout.tsx`·`page.tsx`·`providers.tsx` **셋뿐** — `app/api/**`·`middleware.ts`·`[id]` 디렉토리·Server Action **0건**. `page.tsx:1` 에 `'use client'`
- 상태: TanStack Query v5 하나. 전역 상태 라이브러리 의존성 없음(`package.json:15-26`). `providers.tsx:20-30` 이 `retry:false`(mutation 포함)·`refetchOnWindowFocus:false`·`throwOnError:false`
- 토큰 저장소 격리: `grep -rn "localStorage|sessionStorage|keyring|keychain|@tauri-apps/api" app/front/src` → **주석 2줄뿐, 호출 0건**. `.eslintrc.json:4-31` 이 `no-restricted-globals`/`no-restricted-properties` 로 규칙화하고 `tokenStore.ts` 만 예외로 둔다(§11 금지 2 → 린트 이관)
- 색: `grep -rnE '#[0-9a-fA-F]{3,8}' app/front/src --include='*.tsx' --include='*.ts'` → **0건**. hex 는 `tokens.css` 에만 있고 `globals.css` 는 전부 `var(--tm-*)` 매핑, 컴포넌트는 Tailwind 유틸만 쓴다(§5-1 2층)
- `--tm-ink`: Tailwind 에 `ink` 로 한 번 노출되고 실제 사용처는 `ui/sonner.tsx:27` 토스트 배경 하나 — §5-2 가 명시한 예외다
- 오버레이: `OverlayProvider.tsx` 가 스택을 들고 `openDrawer`/`openConfirm` 둘만 노출. **드로어 위 모달 금지**가 §6-2 그대로(`:55-70` — 개발 모드 throw, 운영 모드는 드로어를 닫고 연다). 드로어는 동시에 하나(`:52`). `Sheet`/`Dialog` 직접 import 0건
- 규격 상수: `tokens.css:64-69` 가 드로어 840 · 모달 600 · 팝오버 200~400 · 스크림 두 값을 한 곳에 둔다(§6 표와 일치)
- 브레이크포인트: `tailwind.config.ts:15-19` 가 `desk/wide/ultra` 로 **통째 재정의**(sm/md/lg 제거 — §7-1)
- 폰트: `globals.css:10` 이 `node_modules/pretendard` 를 번들에서 끌어온다 — 외부 origin 요청 0건(SPEC-000 §5 CDN 금지 · SYS-3)
- 화면: `ConnectionCheckScreen.tsx` 가 U-1 세 상태(확인 중/연결됨/실패)와 문구·대상 주소·`version`·「다시 확인」(실패에서만)을 SPEC-000 §2 그대로 그린다. **어느 분기에서도 화면이 비지 않는다**(`:82-84` 폴백). `MinWidthGuard.tsx` 가 U-2 를 1280 기준·CTA 없이·resize 즉시 반영으로 구현하고 Tauri `minWidth` 를 쓰지 않는다(FE §7-2)
- Case Matrix 4행이 `failureReason()`(`:23-37`)에 1:1 로 있다 — `db_unavailable` 백엔드 detail · 네트워크 「서버가 응답하지 않습니다 · <주소>」 · CORS 「요청이 서버에서 거부되었습니다(CORS)」 · 그 밖 `HTTP <status>`
- Tauri: `tauri.conf.json:17-19` 창 1440×900, **`minWidth` 없음**(Phase 4 · FE §7-2). `:24` CSP 가 `default-src 'self'` 로 외부 origin 차단. `Cargo.toml:28` `keyring` 의존성만 걸고 `lib.rs` 는 창만 띄운다(WORK-002 몫). CORS 명시 목록에 dev/macOS/Windows 세 origin 이 들어 있다(`.env.example:22`, `app/front/README.md:42-46`)

**WP 범위**

- 커밋별 파일 목록으로 확인: `2a4d29a` 는 `app/back/**` + 루트 ops 파일(`.env.example`·`Makefile`·`docker-compose.local.yml`·`.gitignore`)만, `84882c0` 은 `app/front/**` + `Makefile`·`.gitignore` 만 건드렸다. **백 워커가 `app/front` 를, 프론트 워커가 `app/back` 을 만진 흔적이 없다**(공유한 두 파일은 WP §Code Surface 가 양쪽에 배정한 파일이다)
- 선행 구현 없음: 로그인·refresh·유형/프로젝트 CRUD 라우터·화면 0건. `deps.py:27-33` `require_account` 는 **시그니처만**(`-> int`, 본문은 `NotImplementedError`), `tokenStore.ts` 는 자리만, `queryKeys.ts` 는 `health` 하나만 — 셋 다 WP §Internal Interface Contract 가 요구한 형태다
- Pre-deploy Check 3항목: `.env` 미추적(`git ls-files | grep env` → `.env.example` 2개뿐) · 시드 비밀번호 평문 없음 · 헬스 응답에 버전 외 정보 없음(`schemas/health.py:11-14` 가 `status`·`version`·`database` 로 고정)

## 코디 실행 요청

리뷰는 read-only라 아래는 확인하지 못했다. Phase 검증·Acceptance 중 **실행이 있어야 판정되는 항목**들이다.

1. `make up && make migrate && make seed` — 오류 없이 끝나는가. **`make seed` 2회 실행 후 행 수가 그대로인가**(Phase 2 검증)
2. `make test-db && make test` — pytest 전부 통과하는가(Phase 1 검증). 특히 `test_health.py:27` 의 503 경로가 실제 psycopg3 에서 `OperationalError`/`InterfaceError` 로 떨어지는지(다른 예외 타입이면 500 으로 샌다 — 이 리뷰가 **정적으로만** 확인했다)
3. `alembic downgrade -1 → upgrade head` 왕복(Phase 2 검증)
4. `.env` 에서 `JWT_SECRET` 을 지우고 `make up` — API 가 기동하지 않고 로그에 `JWT_SECRET` 이 남는가(Phase 1 검증)
5. `cd app/front && npm run build` — `out/` 이 생기고 산출물에 `app/api/**`·`middleware.ts`·동적 세그먼트 디렉토리가 없는가. **네트워크 탭에 자기 origin 요청만 있는가**(Phase 3 검증 · Acceptance 9번)
6. `make app` — 앱 창이 뜨고 「서버에 연결되었습니다」가 보이는가. `CORS_ORIGINS` 에서 앱 창 origin 을 빼면 **CORS 실패 문구**로 뜨는가(Phase 4 검증 · Acceptance 8번). **W-1/D-1 을 판단할 실측 자료가 여기서 나온다** — 이때 네트워크 탭의 `/api/health` 요청 수를 함께 세어 주면 좋다
7. `npm run lint` · `npm run typecheck` — 통과하는가(레포에 CI 가 아직 없다)

## 자기점검

- **네 층 전부에 판정을 냈나** — 냈다(정책 PASS · 아키텍처-백 PASS · 아키텍처-프론트 WARN · SPEC WARN · WP PASS)
- **모든 FAIL·WARN 에 파일:줄 + 문서 절이 붙었나** — 붙었다. W-3 만 문서 절이 아니라 **코드 내부 불일치**임을 표에 명시했다(문서에 근거가 없어 그렇게 표기했다)
- **문서 공백이 지적과 분리됐나** — 분리했다. 워커가 올린 6건(D-2~D-7)을 재판정(전부 유효, D-3·D-4 는 **코드가 맞고 문서가 틀렸다**)하고 12건(D-1 · D-8~D-18)을 더했다
- **코드·문서를 하나도 고치지 않았나** — `git status` clean(`--porcelain` 출력 없음). 문서 레포에서는 이 리포트 파일 1개만 새로 썼다. 테스트·빌드를 돌리지 않았다
