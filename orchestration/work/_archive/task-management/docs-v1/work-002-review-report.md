# WORK-002 검수 리포트

- 검수 대상: `37a8ce1`(BE Phase 1) · `c39d501`(.env.example) · `c49ae72`(FE Phase 2·3) — `git diff 84882c0...HEAD` 기준 56파일 / +3519 −57
- 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1` · 작업 트리 clean(`git status --porcelain` 무출력)
- 판정 기준: DEC-001 · SPEC-001 · SPEC-000 §5 · `40-architecture/{backend,frontend,database/domains/account}` · WORK-002
- 검수자는 **코드·문서를 하나도 고치지 않았고 테스트·빌드를 돌리지 않았다.**

---

## 판정 요약

| 층 | 판정 | 근거 |
|---|---|---|
| **정책**(DEC-001) | **WARN** | 세션·전송·「유지」·v2 스코프·잠김 없음·회원가입 부재까지 전부 정확. 다만 DEC-001 §4 가 못박은 「비밀값은 환경에서만」의 취지를 `.env.example` 시드 커밋이 깬다(FAIL-1 은 SPEC-000 §5 로 계상) |
| **아키텍처 — 백** | **PASS** | 계층·ORM 경계·schema/dto·`commit()` 위치·`except Exception` 0건·`persist_changes` 예외 1건(`RefreshTokenReuseError`)·CORS 명시목록/`allow_credentials=False`·env 단일 `Settings`·비밀값 기본값 없음 전부 성립 |
| **아키텍처 — 프론트** | **FAIL** | 정적빌드 제약·상태관리·토큰 저장소 격리·폴백 없음·갱신 1회는 전부 성립하나, **FE §11 「반드시 있어야 하는 테스트」가 0건**이고 러너 자체가 없다(FAIL-2). 그 밖 타이포·radius WARN 2건 |
| **SPEC**(SPEC-001) | **FAIL** | API 표면 4종·Validation·Case Matrix·상태 전이·U-1~U-8 이 거의 그대로 구현됐으나, **로그아웃이 회전 뒤 옛 refresh 를 보내 서버 세션이 살아남는다**(FAIL-3 — §4 API Contract·§5 로그아웃 위반) |
| **WP**(WORK-002) | **WARN** | Phase 1~3 작업 체크리스트 실질 완료, 범위 밖 침범 없음(백↔프론트 교차 0), WORK-003 기능 선구현 없음. Phase 2 검증의 **정적 검사는 통과**(아래 확인), Done Criteria 의 프론트 테스트 항목은 FAIL-2 로 미충족. `alembic/env.py` 주석 정정이 범위 밖(WARN-3) |

**보안 축 별도 총평 — PASS.** 계정 존재 누설(문구·상태코드·bcrypt 더미 검증으로 시간까지) 차단, refresh 평문 미저장(SHA-256 해시만), 회전·재사용 감지 성립(요청 롤백 경계까지 테스트), 401 사유 무구분, 응답 누설 테스트 존재, v2 서버 표면 0건. **다만 FAIL-3 이 「로그아웃 뒤 서버에 유효 세션이 남는다」는 보안 결과를 낸다.**

---

## FAIL — 반드시 고쳐야 하는 것

| # | 파일:줄 | 무엇이 어긋났나 | 어긋난 문서 절 | 어떻게 고치나 |
|---|---|---|---|---|
| **F-1** | `.env.example:37-40` | 시드 계정의 **아이디·평문 비밀번호·이름·이메일**을 레포에 커밋했다(`SEED_LOGIN_ID=kknaks` · `SEED_PASSWORD=dev1234!` · `SEED_NAME=이건학` · `SEED_EMAIL=kknaks@example.com`). 이 값은 그대로 **실행 중인 개발 계정의 로그인 자격 증명**이고, 같은 파일 2줄이 「실제 값을 커밋하지 않는다」라고 스스로 못박고 있다 | **SPEC-000 §5 환경변수 표** `SEED_*` 행 「**소스에 계정 정보를 적지 않는다**」 · SPEC-000 §5 시드 계약 「비밀번호는 해시로만 저장한다. 평문을 로그·DB 어디에도 남기지 않는다」 · `backend/README.md` §11 「비밀값의 기본값을 두지 않는다」 · `.env.example:2` | 네 값을 다시 **빈 값**으로 되돌리고, 개발자는 자기 `.env` 에만 채운다. `make seed` 가 빈 값에서 실패하는 것은 **결함이 아니라 설계된 신호**다(`config.py` 의 `SeedSettings` 가 `min_length=1` 로 그렇게 만들었다). `c39d501` 이 고치려 한 진짜 문제는 「`.env` 를 안 채웠다」이지 「예시가 비어 있다」가 아니다. 커밋 이력에 남은 비밀번호는 개발 계정이므로 **시드를 새 비밀번호로 다시 돌려 무효화**한다. 문서 쪽 보강은 문서공백 G-8 |
| **F-2** | `app/front/package.json:5-11`(scripts) · `app/front/` 전체에 `*.test.*`/`*.spec.*` **0건** | 프론트에 **테스트가 하나도 없고 러너·라이브러리도 없다** — Vitest·React Testing Library·MSW 어느 것도 `devDependencies` 에 없고 `test` 스크립트도 없다. WORK-002 범위에 걸리는 필수 테스트가 **4건 전부** 빠졌다: ④ 401 갱신(refresh 1회 → 재시도 → 두 번째 401 이면 로그인, 루프 없음) ⑤ 토큰 저장소 격리(`persist=false` 로 로그인하면 저장소에 아무것도 남지 않는다) ⑦ v2 게이트(조작해도 **네트워크 요청이 나가지 않는다**) ⑧ 정적 빌드 산출(`out/` · Route Handler·미들웨어·`[…]` 없음) | **`frontend/README.md` §11 「반드시 있어야 하는 테스트 — 없으면 리뷰 반려다」 항목 4·5·7·8** · 같은 절 「러너 = Vitest + RTL」·「네트워크 = MSW 로 `client.ts` 아래에서 가로챈다」 · WORK-002 Done Criteria | Vitest + RTL + MSW 를 붙이고 네 테스트를 쓴다. ④·⑤ 는 `lib/api/client.ts`·`lib/auth/tokenStore.ts` 를 MSW 로 태우면 되고(현재 `tokenStore` 가 `invoke` 를 직접 물고 있으므로 `@tauri-apps/api/core` 를 모듈 목으로 세운다), ⑦ 은 `V2Gate` 로 감싼 버튼 클릭 시 MSW 핸들러가 **호출되지 않음**을 단언한다. ⑧ 은 `next build` 후 `out/` 트리 검사 스크립트 한 줄로도 성립한다. **참고: `tokenStore` 격리의 「정적 검사」 쪽은 이미 통과다**(ESLint `no-restricted-globals`/`-properties` + 파일 예외가 `.eslintrc.json` 에 있고, grep 결과도 0건 — 아래 「확인한 것」). 빠진 것은 **동작 테스트**다 |
| **F-3** | `app/front/src/lib/auth/session.ts:83` (+ `lib/api/client.ts:194,211`) | **로그아웃이 서버 세션을 끊지 못하는 경로가 있다.** `logout()` 이 요청을 만들기 **전에** `tokenStore.get()` 으로 refresh 를 캡처한다(`R1`). 그런데 그 뒤 `apiFetch("/api/auth/logout")` 가 access 만료를 만나면 **파이프라인이 먼저 갱신을 태워 `R1 → R2` 로 회전**시킨다(`client.ts:211`). 본문에는 여전히 `R1` 이 실려 나가고, 서버는 `R1.revoked_at` 이 이미 찍혀 있으므로 `auth_service.logout:128` 에서 **아무것도 하지 않고 204** 를 준다. 결과: 클라이언트는 「로그아웃 완료」로 보이지만 **`R2` 세션이 서버에 7일간 유효하게 남는다.** access 가 없는 경로(`client.ts:194`)도 같다. SPEC-001 S-5 가 그린 「앱을 1시간 이상 켜 둔 뒤 조작」이 바로 이 상태다 | **SPEC-001 §4 API Contract** `POST /api/auth/logout` 「이 세션의 refresh 를 **무효화한다**」 · **§4 Flow**(FE→BE logout → 204 → TS `clear()`) · **§5 로그아웃** 「로그아웃은 **이 세션의 refresh 만** 무효화한다」 · WORK-002 Phase 3 「로그아웃 흐름」 | 「보낼 refresh 를 **파이프라인이 갱신을 끝낸 뒤에** 읽는다」로 순서를 뒤집는다. 최소 수정은 `client.ts` 가 유효 access 를 확보하는 지점을 함수로 빼서(`ensureAccessToken()`) `session.logout()` 이 그것을 먼저 `await` 한 다음 `tokenStore.get()` 을 읽는 것이다. 대안은 `apiFetch` 에 「본문을 요청 직전에 만드는 콜백」을 허용하는 것. **서버를 고쳐 무효인 토큰의 후속 회전 사슬까지 끊는 방식은 쓰지 마라** — A-7 재사용 감지와 구분이 안 되고, 로그아웃이 「이 세션만」이라는 §5 계약을 넘는다 |

---

## WARN — 규약에서 벗어났으나 동작하는 것

| # | 파일:줄 | 무엇이 어긋났나 | 어긋난 문서 절 | 어떻게 고치나 |
|---|---|---|---|---|
| **W-1** | `app/front/src/features/auth/components/BrandPanel.tsx:29` | 헤드라인이 `text-[44px] leading-[1.25] tracking-[-0.03em]` 로 **임의 크기**를 쓴다. `tailwind.config.ts:88-96` 의 타이포 프리셋에 44px 계단이 없다 | `frontend/README.md` §5-1 「타이포 계단은 **Tailwind 유틸 프리셋으로 고정**하고 컴포넌트가 **임의 크기를 쓰지 않는다**」 | `09-design-tokens.md` §타입에 로그인 브랜드 헤드라인 계단이 없으므로, ① 프리셋에 `brand-title` 을 추가하고 컴포넌트는 그 유틸을 쓰거나 ② 기존 `page-title`(28) 로 낮춘다. **어느 쪽인지는 디자인 정본이 정할 문제**라 문서공백 G-9 에도 같이 올렸다 |
| **W-2** | `app/front/src/styles/tokens.css:63` (`--tm-radius-card: 12px`) → `SettingsMenuCard.tsx:65` `rounded-card` | 설정 좌측 메뉴 카드의 radius 가 **12px** 인데 SPEC 은 **16** 으로 못박았다. `ConfirmModal.tsx:60` 은 주석에 「radius 16」이라 적어 놓고 같은 `rounded-card`(12)를 쓴다 — 코드와 주석도 어긋난다 | **SPEC-001 U-4** 「카드(1px `#D9D9D9` · **radius 16** · 흰 배경)」. `09-design-tokens.md` §형태는 「카드 12~16」 **범위**라 SPEC 쪽이 더 좁은 계약이다 | 카드 radius 를 하나로 못박는다. 전 영역이 `--tm-radius-card` 하나를 공유하므로 12→16 으로 올릴지, 「설정 메뉴 카드·모달만 16」인 두 번째 토큰(`--tm-radius-card-lg`)을 둘지는 디자인 판단이다. 최소한 `ConfirmModal.tsx:60` 주석의 「radius 16」은 실제 값과 맞춰야 한다 |
| **W-3** | `app/back/alembic/env.py:27` | 백엔드 Phase 1 커밋(`37a8ce1`)이 WP `Code Surface` 에 없는 파일의 **주석 오타**를 함께 고쳤다(`TEST_DATABASE_URL` → `ALEMBIC_DATABASE_URL`). 내용은 옳고 동작에 영향이 없다 | WORK-002 §Code Surface(만질 파일 후보에 `alembic/env.py` 없음) · 역할 규약 「WARN = 범위 밖 변경」 | 고칠 것 없음. **기록만 남긴다** — 정정 자체는 맞고(WORK-001 잔여 오타), 다음부터는 별도 커밋으로 분리한다 |
| **W-4** | `app/front/src/lib/api/client.ts:206` | 401 을 받으면 **`code` 를 보지 않고 무조건** 갱신 1회를 태운다. 문서는 `401 token_expired` 로 트리거를 특정했다. 지금은 게이트 뒤 401 이 `deps.py:58`·`security.py:107` 의 `token_expired` 하나뿐이라 **동작은 같다** | `frontend/README.md` §4-2 2 「**`401 token_expired`** → `POST /api/auth/refresh` 1회」 · SPEC-001 §5 갱신·재시도 | 둘 중 하나. ① `error.code === API_ERROR_CODE.TOKEN_EXPIRED` 를 조건에 넣어 문서와 코드를 맞춘다. ② **문서를 넓힌다** — 「게이트 뒤의 401 은 코드를 불문하고 갱신 1회를 태운다(백엔드가 사유를 구분해 주지 않기로 했으므로 `code` 로 분기할 수 없다)」. 실은 ②가 §8-2 의 「사유를 흘리지 않는다」와 일관되므로 **문서 쪽 정리를 권한다**(문서공백 G-1 과 같은 뿌리) |

---

## 문서 공백 — 코드가 아니라 문서를 고쳐야 하는 것

> 앞의 6건은 코드 워커가 올린 것이고 판정을 붙였다. G-7 이후는 이번 검수에서 새로 찾은 것이다.

| # | 무엇이 비었나 | 어느 문서 어느 절 | 무엇을 적어야 하나 |
|---|---|---|---|
| **G-1** | **조작·형식오류 access 에 쓸 코드가 §8-2 표에 없다.** 워커는 헤더없음·만료·서명 위조·형식 오류를 전부 `401 token_expired` 하나로 통일했다(`deps.py:57-60` · `security.py:104-116`) | `backend/README.md` **§8-2 코드 표** `token_expired` 행 · **SPEC-001 §4 Case Matrix** `token_expired` 행 | **판정: 새 코드를 만들지 마라. 문서를 넓혀라.** 코드를 나누면 「401 사유를 구분해 알려주지 않는다」(브리프 §3 보안 · §8-2 「사유를 흘리지 않는다」)가 깨진다. 두 표의 「언제」 칸을 `access 만료` → **「access 가 없거나 · 만료 · 서명 위조 · 형식 오류. 넷을 구분해 알리지 않는다 — 프론트는 갱신 1회로 끝낸다」**로 고친다. 이 문장이 서면 W-4 의 클라이언트 분기 문제도 함께 닫힌다 |
| **G-2** | **WP Phase 1 테스트의 「남의 자원 404」가 이 Phase 에 해당 표면이 없다.** 인증 4표면 중 소유 판정으로 404 를 낼 자원이 없다. 워커는 `test_logout_cannot_kill_another_accounts_session`(남의 refresh 로 로그아웃해도 그 세션이 안 죽는다)으로 대체했다 | **WORK-002 §Execution Phase 1 작업** 마지막 체크박스(`tests/test_auth.py — … 남의 자원 404`) | **판정: 대체가 타당하다.** 그 체크박스를 「**남의 refresh 를 실어 로그아웃해도 그 세션이 죽지 않는다**(소유 검사 — `backend/README.md` §9)」로 고치고, 「남의 자원 404」는 **WORK-003**(유형·프로젝트 — 처음으로 소유 자원이 생긴다)의 테스트 목록으로 옮긴다 |
| **G-3** | **`tokenStore` 인터페이스가 문서의 3개보다 넓다.** 실제는 `getAccess`·`setAccess`·`load`·`get`·`set`·`isPersistent`·`clear` 7개 + `KeychainError` 다(`tokenStore.ts:66-159`) | **`frontend/README.md` §4-1** 「인터페이스는 셋 — `get()`·`set(token, persist)`·`clear()`」 · **WORK-002 §Internal Interface Contract** `tokenStore` 행 | **판정: 확장이 필요하고 규약 위반이 아니다**(교체 지점은 여전히 이 파일 하나이고, 파일 밖 저장소 호출 0건). 두 곳의 인터페이스 목록을 7개 + `KeychainError` 로 갱신하고 각각의 존재 이유를 한 줄씩 적는다 — `load()`=앱 시작 시 키체인 1회 읽기(세션 가드 부트스트랩), `isPersistent()`=**회전 시 되쓸 자리**와 **U-5 경고 슬롯 조건**, `getAccess/setAccess`=access 는 메모리 전용이라 저장소 API 와 갈라 둔 것, `KeychainError`=자격 증명 실패와 **다른 타입**이어야 로그인 화면이 「아이디 또는 비밀번호가…」로 오안내하지 않는다 |
| **G-4** | **`frontend/README.md` §4-1 이 DEC-001 §4 개정 이전 상태다 — 문서끼리 모순.** §4-1 「단계」 표가 아직 「**웹 개발 중(지금)**: `persist=true` → **브라우저 저장소**」라고 적혀 있다. DEC-001 §4(2026-09-05)는 그 폴백을 **폐기**했고 코드는 개정본을 따랐다(`tokenStore.ts:125-129` — 셸이 없으면 던진다) | **`frontend/README.md` §4-1 「단계」 표** (FE-C2 는 이미 개정본이라 **같은 문서 안에서 모순**이다) | 표에서 「웹 개발 중」 행을 지우고 한 행만 남긴다 — 「`persist=true` → **OS 키체인**(셸이 없으면 **예외를 던진다. 브라우저 저장소로 대체하지 않는다**) / `persist=false` → 메모리 변수」. 근거로 DEC-001 §4(2026-09-05 개정) · §C-4 번복을 단다. **이건 우선순위가 높다** — 다음 워커가 §4-1 만 읽으면 폴백을 되살린다 |
| **G-5** | **`ConfirmRequest` 에 `confirmLabel`·`destructive` 가 문서에 없다**(`OverlayProvider.tsx:26-39`) | **`frontend/README.md` §6-1** 의 `openConfirm({ title, summary, warning?, onConfirm })` 시그니처 | **판정: 둘 다 필요하다.** U-5 확인 버튼은 「로그아웃」, U-6 은 「계정 삭제」 + 파괴색(`#E2685B`)이고 U-5 는 「파괴적 색을 쓰지 않는다」라 **문구와 색이 호출자마다 갈린다.** 시그니처를 `openConfirm({ title, summary, warning?, confirmLabel, destructive?, onConfirm })` 으로 갱신하고, 「`confirmLabel` 은 「확인」이 아니라 **하려는 동작**을 적는다 · `destructive` 는 **데이터가 사라지는 결정에만** 켠다」를 붙인다 |
| **G-6** | **인증 호출을 `features/auth/api.ts` 가 아니라 `lib/auth/session.ts` 에 모았다** | **WORK-002 §Code Surface** 표(`features/auth/components/LoginScreen.tsx · api.ts · types.ts`) · **`frontend/README.md` §2** 디렉토리 규칙 | **판정: 규약 위반이 아니다.** FE §2 트리가 `lib/auth/session.ts` 를 「**로그인·갱신·로그아웃 상태**」로 이미 두고 있어 두 자리가 겹쳤을 뿐이다. 게다가 `client.ts` 가 세션 종료를 알려야 해서 `features → lib` 단방향을 지키려면 인증 호출은 `lib` 쪽이 자연스럽다(그래서 `sessionEvents.ts` 로 순환을 끊었다). WORK-002 Code Surface 에서 `features/auth/api.ts` 를 빼고, FE §2 규칙 옆에 「**인증 호출은 `lib/auth/session.ts` 가 갖는다** — `client.ts` 와의 순환을 피하려는 예외이며 `features/auth` 에는 화면·타입만 둔다」 한 줄을 적는다 |
| **G-7** | **macOS dev 는 ad-hoc 서명이라 `src-tauri` 재컴파일마다 키체인 ACL 알림이 뜬다** — 서명 identity 가 빌드마다 달라져 OS 가 다른 앱으로 본다. 개발 중 「유지」 검증을 반복할 때마다 사람이 허용을 눌러야 한다 | **WORK-002 §Open Issues**(「키체인 접근이 macOS·Windows 에서 갈릴 수 있다」 항목 바로 아래) 또는 `40-architecture/system/README.md` 개발 환경 절 | 운영 메모로 한 줄. 「`tauri dev` 는 ad-hoc 서명이라 **재컴파일마다 키체인 접근 알림이 다시 뜬다.** 결함이 아니다 — 서명된 번들에서는 한 번만 뜬다. Phase 2·3 의 「유지」 검증에서 이 알림을 **거부하면** `KeychainError` 경로가 그대로 돌아 로그인이 실패하는 것이 정상 동작이다」 |
| **G-8** | **`.env.example` 의 값 채우기 규칙이 어디에도 없다.** SPEC-000 §5 는 「소스에 계정 정보를 적지 않는다」만 말하고, **빈 예시 파일에서 `make seed` 가 실패하는 것이 정상인지**를 정하지 않아 워커가 예시에 실값을 넣었다(F-1 의 직접 원인) | **SPEC-000 §5 시드 계약** 표 · **WORK-002 §Pre-deploy Check** | 시드 계약에 한 행. 「`.env.example` 은 **템플릿이다 — 비밀값·계정값 자리를 빈 값으로 둔다.** 실제 값은 각자의 `.env` 에만 둔다. **빈 값에서 시드·기동이 실패하는 것은 설계된 신호**이지 결함이 아니다(`Settings`·`SeedSettings` 가 `min_length=1` 로 그렇게 만들었다)」. Pre-deploy Check 의 「`JWT_SECRET` 이 레포에 없고」 항목을 **「`JWT_SECRET`·`SEED_*` 가 레포에 없고」**로 넓힌다 |
| **G-9** | **로그인 브랜드 헤드라인(44px)의 타이포 계단이 없다.** `09-design-tokens.md` §타입 계단은 페이지 타이틀 28 이 최대라 W-1 의 `text-[44px]` 를 담을 자리가 없다 | **`00-design/09-design-tokens.md` §타입** · **SPEC-001 U-1**(브랜드 패널 문구 규격) | 계단에 브랜드 헤드라인 한 줄을 추가하거나(예: `브랜드 헤드라인 44/700/-0.03`), 로그인 패널이 기존 계단을 쓰도록 U-1 을 확정한다. **디자인 정본이 정할 일**이라 코드 지적(W-1)과 분리했다 |
| **G-10** | **`09-design-tokens.md` 에 토스트 규격 절이 아예 없다.** SPEC-001 U-2 는 「규격은 `09-design-tokens` 토스트(**400×56, `#1E1E1E`, 하단 중앙 60px 위, 4초**)」로 참조하는데, 그 문서에는 §색의 「토스트는 오버레이 서피스라 예외」 한 줄뿐이다. 코드(`ui/sonner.tsx:24-27`)는 SPEC 이 **괄호 안에 적어 둔 값**을 정본 삼아 구현했고(하단 중앙·offset 60·4000ms), **폭 400·높이 56 은 적용되지 않았다**(sonner 기본 크기) | **`00-design/09-design-tokens.md` §오버레이 3종** 아래 | 「토스트」 행을 신설한다 — 폭 400 · 높이 56 · 배경 `#1E1E1E` · 하단 중앙 60px 위 · 4초 · **실행취소 버튼은 되돌릴 동작이 있을 때만**. 그리고 SPEC-001 U-2 의 괄호 값은 그 표를 참조만 하게 바꾼다(값이 두 곳에 살아 갈리지 않게). 규격이 서면 `ui/sonner.tsx` 에 폭·높이를 얹는 후속 작업이 하나 생긴다 |
| **G-11** | **`GET /api/auth/session` 의 404 가 Case Matrix 에 없다.** `auth_service.get_account_summary:142` 가 `NotFoundError("계정을 찾을 수 없습니다")` 를 던질 수 있다(유효한 access 인데 계정 행이 없는 경우). v1 에 계정 삭제가 없어 **현재는 도달 불가한 방어 분기**다 | **SPEC-001 §4 Case Matrix** — 「이 spec 의 **모든** 에러·경계가 여기 있다(단일 SoT)」 | 둘 중 하나를 문서에 못박는다. ① Matrix 에 `not_found`(404, 「도달 불가 — 계정 행이 사라진 경우의 방어」) 행을 추가하거나, ② §4 Case Matrix 머리말에 「**도달 불가한 방어 분기는 Matrix 에 싣지 않는다**」 한 줄을 넣어 이후 spec 이 같은 판단을 반복하지 않게 한다. **②를 권한다** — 아니면 모든 spec 의 Matrix 가 방어 코드로 부푼다 |
| **G-12** | **`v2_not_available`(501)은 이 배치에서 절대 발생하지 않는다.** 두 문서가 「v2 게이트가 샜을 때의 안전망」으로 501 을 약속했지만, **v2 엔드포인트를 아예 만들지 않으므로**(SPEC-001 §4 「v2 엔드포인트를 만들지 않는다」) 게이트가 새면 오는 것은 **404** 다. 백엔드에 `v2_not_available` 예외도 없다(있을 이유도 없다) | **SPEC-001 §4 Case Matrix** `v2_not_available` 행 · **`backend/README.md` §8-2** 같은 행 | 두 곳에 한 줄. 「**해당 표면 자체가 없으므로 실제 응답은 404 다.** `v2_not_available` 은 v2 에서 표면이 열린 뒤 그 표면이 아직 닫혀 있을 때를 위한 코드이고, v1 에서는 **발생하지 않는다**」. 프론트의 `API_ERROR_CODE.V2_NOT_AVAILABLE`(`errors.ts:40`)도 그때까지는 미사용 상수로 남는다는 것을 함께 적는다 |
| **G-13** | **사이드바의 캘린더·회의록·자료함·메시지가 404 로 빠지고 정적 export 라 돌아올 길이 없다**(`Sidebar.tsx:33-37` 이 실제 `href` 를 걸었는데 `(app)/` 아래 그 라우트가 없다). **사용자 판단으로 후속 work 까지 보류된 사안**이라 지적하지 않는다 | **`frontend/README.md` §10** 아래 또는 새 `FE-OQ-5` | 보류라는 **사실 자체를 문서에 남긴다** — 「정책서는 있으나 화면이 아직 없는 4메뉴(캘린더·회의록·자료함·메시지)는 배치 순서상 라우트가 생기기 전까지 **404 로 빠지고 정적 export 라 돌아올 길이 없다.** 처리 방식(홈·채팅처럼 `V2Gate` 로 임시 전환 / 빈 셸 라우트 선행 생성 / 그대로 둔다)은 **후속 work 로 보류**(2026-09-05 사용자 판단)」. 적어 두지 않으면 다음 검수가 같은 것을 다시 FAIL 로 올린다 |

---

## 확인한 것 (PASS 근거)

**범위 산정** — `git diff 84882c0...HEAD --stat`(56파일) + `git log 84882c0..HEAD`(3커밋) + `git status --porcelain`(무출력, untracked 0). 커밋별 `--name-only` 로 교차 침범 확인: `37a8ce1`·`c39d501` 은 `app/back` + `.env.example` 만, `c49ae72` 는 `app/front` 만. **백↔프론트 교차 0건.**

**아키텍처 — 백엔드**(정적 검사)
- `grep -rn "except Exception\|except:" app/back` → **0건**(§8-1).
- `grep -rn "commit()" app/back` → `api/deps.py:40,42`(요청 경계)와 `seed/seed.py:132`(요청 밖 절차)뿐. **service·repository 에 `commit()` 없음**(§2·§7).
- `grep -rn "fastapi" app/back/service app/back/repository` → 실코드 0건(docstring 문장만). `grep -rn "schemas" app/back/service` → 0건(§3 규칙 1).
- `grep -rn "from models" app/back` → `repository/`·`models/`·`alembic/`·`seed/`·`tests/` 밖 0건. 두 repository 모두 `AuthSessionDTO`·`AccountCredentialDTO`·`AccountSummaryDTO` 만 반환 — **ORM 모델이 repository 를 넘지 않는다**(§2). `AsyncSession` 전달은 규약에 금지 근거가 없어 지적하지 않았다.
- `persist_changes`: `exceptions.py:16`(기본 `False`) · `exceptions.py:35-44`(`RefreshTokenReuseError` **하나만** `True`, 이유를 그 자리에 적었다) · `deps.py:38-41`(구체 타입 `except AppError` → commit → **`raise` 재전파**). §7 신설 규약과 정확히 일치. 편의로 켠 곳 없음.
- 설정: `config.py` 의 `Settings` 하나가 env 를 읽고 `jwt_secret`·`database_url`·`cors_origins`·`storage_root` 는 `Field(min_length=1)` — **비밀값 기본값 없음**, 누락 시 `MissingEnvError` 로 기동 실패(§11 · SPEC-000 §4).
- CORS(`main.py:48-54`): `allow_origins=settings.cors_origin_list`(쉼표 명시 목록) · **`allow_credentials=False`** · `allow_headers=["Authorization","Content-Type"]`. `*` 없음(§9 · SYS-3).
- 인가 게이트(`auth_router.py:24-31`): 라우터를 **둘로 갈라** `login`·`refresh` 만 밖에 두고 `logout`·`session` 은 `dependencies=[Depends(require_account)]` 로 **라우터 단위**에 건다(§9 — 개별 함수 누락 여지 없음).

**보안**
- **계정 존재 누설 없음**: `auth_service.py:29-34` 가 「아이디 없음」과 「비밀번호 틀림」에 **같은 `UnauthorizedError(401, invalid_credentials)` + 같은 문구**를 쓰고, `security.py:68-74` `burn_password_verification()` 이 아이디가 없을 때도 **같은 cost 의 bcrypt 검증을 태워 시간까지 맞춘다**(더미 해시도 `bcrypt.gensalt()` 기본 cost). 테스트 `test_wrong_password_and_unknown_login_id_are_indistinguishable` 이 이를 잡는다.
- **refresh 평문 미저장**: `security.py:119-126` 이 `secrets.token_urlsafe(48)`(384비트) 원문을 응답으로만 내보내고 저장·조회는 **SHA-256 해시**만 쓴다. bcrypt 를 안 쓴 이유(대조 조회 · 원문이 고엔트로피)를 파일 상단에 근거와 함께 적어 두었다. `test_no_response_leaks_the_password_hash_or_the_stored_refresh` 가 응답 3종과 DB 행을 대조한다.
- **회전·재사용 감지(A-7)**: `auth_service.refresh:88-114` — 없음/만료는 `invalid_refresh_token`, **`revoked_at` 이 찍힌 토큰이 다시 오면** `revoke_all_for_account` 후 `RefreshTokenReuseError`. 응답은 여느 `invalid_refresh_token` 과 **구별되지 않는다**. 트랜잭션 경계까지 테스트가 있다(`test_get_db_keeps_the_writes_of_a_reuse_detection` — 401 인데 commit 1회, 일반 도메인 예외는 commit 0회).
- **401 사유 무구분**: 헤더없음(`deps.py:57`) · 만료·서명 위조·형식 오류(`security.py:104-116`) · `type` 클레임 불일치 · `sub` 형식 오류가 **전부 `401 token_expired` 한 문구**다.
- **v2 서버 표면 0건**: 「다른 기기 모두 로그아웃」·계정 삭제·소셜 로그인 엔드포인트 없음. `revoke_all_for_account` 는 **재사용 감지 경로에서만** 호출된다(`auth_service.py:105`).
- **「로그인 상태 유지」가 서버에 없다**: `schemas/auth.py:24-29` `LoginRequest` 는 `loginId`·`password` 둘뿐(SPEC-001 §4).

**아키텍처 — 프론트**(정적 검사)
- 동적 세그먼트 **0개**(`find src/app -name '*[*'` 무출력) · `app/api/**` 없음 · `middleware.ts` 없음 · Server Action 없음. `next.config.ts` 는 `output:"export"` · `trailingSlash:true` · `images.unoptimized:true`(§1-3).
- **모든 `page.tsx`·`(auth)|(app) layout.tsx` 가 `'use client'`**(10개 전수 확인). 루트 `layout.tsx` 만 서버 컴포넌트인데 §1-3 은 `page.tsx` 를 대상으로 하므로 규약 내.
- 전역 상태 라이브러리 **없음**(`package.json` 에 redux/zustand/jotai 0건). `providers.tsx:20-32` 가 `retry:false` · `refetchOnWindowFocus:false` · `staleTime:0` · `throwOnError:false` + mutations `retry:false`(§3-2).
- **컴포넌트 hex 리터럴 0건**: `grep -rnE "#[0-9A-Fa-f]{3,8}" src --include='*.ts(x)'`(styles 제외) → **무출력**. 브랜드 그라디언트는 `tokens.css` 의 `--tm-brand-gradient` → `tailwind.backgroundImage.brand` → `bg-brand` 로만 닿는다. 인라인 `style={{}}` 0건(§5-3 · §11 금지 4).
- **W-2 gutter 정정 확인**: `tokens.css:87-105` 가 기본 `--tm-gutter:48px` + `@media (min-width:1440px)` 에서 `clamp(80px, calc(80px + (100vw - 1440px)/3), 240px)`. **1440→80 · 1920→240 · 그 위 240 고정**으로 FE §7-1 표와 정확히 일치하고, WORK-001 검수 W-2 의 「1440 에서 96px」이 해소됐다. `tailwind.spacing.gutter` 는 그 변수를 가리키기만 한다(정본 하나).
- **토큰 저장소 격리 통과**: `grep -rn "localStorage\|sessionStorage\|@tauri-apps" src` → **`tokenStore.ts` 뿐**(18행의 `invoke` import 와 상단 주석). `.eslintrc.json` 에 `no-restricted-globals`(fetch·localStorage·sessionStorage) + `no-restricted-properties`(window.localStorage/sessionStorage)가 서 있고 `overrides` 가 `tokenStore.ts`(전부) · `client.ts`(fetch 만)를 예외로 둔다 — 규칙과 예외가 정확히 문서대로다. `grep -rn "fetch("` → `client.ts:47,81` 뿐(§2 규칙 5). `components/ui/dialog` 직접 import 는 `ConfirmModal.tsx` 하나(§6-1 · §11 금지 3).
- **브라우저 저장소 폴백 없음**: `tokenStore.ts:125-129` — 셸이 없는데 `persist=true` 면 **`KeychainError` 를 던진다.** 조용한 대체 경로가 없다. `session.login:34-42` 이 그 예외를 받아 **메모리 토큰까지 걷어내고**(반쯤 로그인된 상태를 남기지 않는다) 다시 던지고, `LoginScreen.tsx:66-69` 가 자격 증명 실패와 **다른 토스트**로 안내한다(DEC-001 §4, 2026-09-05 개정).
- **갱신이 1회로 끝난다**: `client.ts:125-162` 가 진행 중 갱신 Promise 를 공유해 **동시 401 에도 refresh 는 한 번**만 나가고, `client.ts:203-227` 이 갱신 1회 → 원 요청 1회 재시도 → **거기서 끝**(두 번째 401 은 `endSession` + 로그인 이동). 무한 루프 경로 없음.
- **로그아웃 뒤 갱신 재시도 없음**(A-7 자폭 방지): `client.ts:128-133` — refresh 가 없으면 **요청 자체를 보내지 않고** `absent` 로 끝낸다(무효화된 토큰을 다시 보내면 재사용 감지가 걸려 전 세션이 끊긴다). `absent`/`rejected` 를 갈라 **「유지」 미체크 재시작에는 만료 토스트를 띄우지 않는다**(U-7). `SettingsMenuCard.tsx:51`·`(app)/layout.tsx:45` 가 `queryClient.clear()` 로 잔여 쿼리도 막는다.

**SPEC-001 대조**
- API 표면 4종 경로·메서드·본문·상태코드가 §4 그대로(`logout` 은 204 무본문). Validation 3종이 `schemas/auth.py:16-21` 에 `strip_whitespace`+`min_length=1`(loginId) · `min_length=1`(password, **trim 안 함**) · `min_length=1`(refreshToken, 형식검사 없음)로 표와 일치.
- Case Matrix 5개 코드가 코드에 실재: `invalid_credentials`(401) · `validation_error`(422 — `main.py:27-38` 이 FastAPI 기본 형태를 `{detail,code}` 로 덮고 **어느 필드가 왜 틀렸는지 싣지 않는다**) · `token_expired`(401) · `invalid_refresh_token`(401, 재사용 감지 포함) · 그 밖 5xx 전파. 프론트 `errors.ts:29-41` 이 같은 목록을 상수로 갖는다. **Matrix 에 없는데 코드에 있는 것은 G-11 하나뿐.**
- 상태 전이(§4 State/Lifecycle): 활성→활성(회전) · 활성→로그아웃됨(모달 확인) · 활성→만료됨(refresh 만료·재사용) 셋 다 구현. 「앱 종료는 전이가 아니다」도 `persist=false`+메모리 보관으로 성립.
- U-1: 라벨 **「아이디」**·플레이스홀더 「아이디를 입력하세요」 · **비밀번호 찾기·회원가입 링크 없음** · 빈 입력 시 버튼 비활성 · 제출 중 `readOnly`+중복 제출 차단 · 실패 시 두 입력 `aria-invalid`+실패색 테두리, **비밀번호 아래 인라인**(`gap-2`(8) + `mt-[4px]` = **12px**), 입력값 유지 · 서버·네트워크 실패는 **토스트**.
- U-2: `V2Gate.tsx` 하나 · children 그대로 · `opacity-45` · `cursor-not-allowed` · `aria-disabled` · 클릭/포인터/Enter/Space 캡처 차단 · 토스트 `id` 고정으로 **연타해도 하나**. 문구 두 가지(`v2`/`soon`)를 **한 컴포넌트**가 갖는다.
- U-3: `(app)/layout.tsx` 가 ① 키체인 1회 읽기 → 없으면 **요청 0건으로** 로그인 이동 ② 있으면 `GET /api/auth/session` ③ 확인 중에는 **셸을 그리고 본문만 로딩**(로그인 화면을 깜빡이지 않는다). 사이드바 계정 이름 표시, **소속 없으면 캡션을 비운다**(`Sidebar.tsx:67-69`).
- U-4: 카드 260 · 항목 38px 3개 · 현재 항목 `bg-row-divider`(`#F1F2F5`)+`font-bold` · 구분선 아래 로그아웃·계정 삭제(hover `text-destructive`) · 버전 캡션 `Managment v{env.appVersion}`(`next.config.ts` 가 `package.json` 에서 주입 — 정본 하나) · **「마지막 저장」 줄은 비어 있다**(「-」·「없음」을 쓰지 않는다).
- U-5: `ConfirmModal` 600(`--tm-modal-width`)·스크림 `rgba(30,30,30,0.36)`(`dialog.tsx:31` `bg-scrim-modal`)·제목/요약/경고 슬롯/취소·확인 · **확인 중 `Esc`·스크림 차단**(`ConfirmModal.tsx:52-66`) · 확인 버튼 **파괴색 아님**(`destructive` 미지정) · 경고 슬롯은 `isSessionPersistent()` 일 때만 · **모달을 지나지 않고 로그아웃되는 경로 없음**(`SettingsMenuCard` 가 `openConfirm` 으로만 부른다).
- U-6: 계정 삭제는 `V2Gate` 안이라 **모달이 열리지 않고 토스트만** 뜬다.
- U-7: `absent`/`expired` 분리로 「유지」 미체크 재시작에 토스트 없음, 만료에는 「로그인이 만료되었습니다…」 **한 문구**(`id` 고정).
- U-8: `BrandPanel` `hidden … wide:flex`(≥1440) + 폭 `40%`/`min-w-480` 유동 · 1280~1439 는 패널 숨김 + 폼 400 중앙 + 로고·헤드라인 1줄(`wide:hidden`) · <1280 은 루트의 `MinWidthGuard` 가 덮는다 · `position:absolute` 로 레이아웃을 박은 곳 없음(눈 아이콘·스크림만).
- §5 인가: 화면 가드와 별개로 **서버가 최종 판정**(라우터 단위 게이트). 로그아웃은 서버 실패에도 **클라이언트 토큰을 반드시 지우고**(`session.logout:99-105`) 실패 토스트를 띄운다.

**WP 대조**
- Phase 1 작업 6항목 전부 실재. `tests/test_auth.py` 는 로그인 6 · 세션/게이트 5 · 갱신·회전·재사용 5 · 로그아웃 3 · 트랜잭션 경계 3 · 누설 1 = **23 테스트**로 WP 검증 항목(성공 · 자격 증명 실패 · 반복 실패 무잠김 · 만료 → 갱신 · 회전 후 옛 토큰 거부 · 재사용 시 전체 무효 · 토큰 없이 session 401)을 덮는다. 「남의 자원 404」만 G-2 로 대체.
- Phase 2·3 작업 11항목 전부 실재(`tokenStore` · `client` · `features/auth` · `(auth)`·`(app)` 레이아웃 · `tasks` 셸 · `ConfirmModal` · `V2Gate` · `settings/layout` · 로그아웃 흐름 · v2 적용 5곳).
- **범위 밖 선구현 없음**: `/settings/`·`/settings/work/`·`/settings/integrations/`·`/tasks/` 는 제목 한 줄짜리 빈 본문이고, 유형·프로젝트 CRUD(WORK-003)·프로필·경력·비밀번호 변경(SPEC-010) 코드가 **하나도 없다.** 마이그레이션도 추가되지 않았다(WP 「마이그레이션 없음」).
- **정책 확인**: 회원가입·비밀번호 찾기 **라우트·API·화면 0건**. 소셜 로그인은 버튼만(v2 게이트). 계정 생성 경로 없음(`account_repository` 는 **읽기 2개뿐**). 잠김·실패 횟수 코드 없음(A-8).

---

## 코디 실행 요청

리뷰는 read-only 라 아래는 **실행하지 않았다.** 판정에 필요하면 코디가 돌려 주기 바란다.

1. **`cd app/back && uv run pytest`** — 23개 테스트가 실제로 통과하는지. 코드를 읽어 판단한 범위에서는 통과할 형태다. WP Phase 1 검증의 마지막 항목이다.
2. **`cd app/front && npm run typecheck && npm run lint && npm run build`** — ① 타입 통과 ② **ESLint 금지 규칙이 실제로 발화하는지**(격리 검사의 자동화 부분) ③ `out/` 에 `app/api/**`·`middleware.ts`·`[…]` 디렉토리가 없는지(FE §11-8). **F-2 의 대체는 아니다** — 빌드가 통과해도 필수 테스트 4건은 여전히 없다.
3. **`curl` 로 F-3 재현**(권장): 로그인 → `auth_session` 의 `expires_at` 을 건드리지 말고 **access 만 만료시킨 상태**(또는 `ACCESS_TOKEN_TTL_MIN=1` 로 기동)에서 앱의 로그아웃을 태운 뒤, 응답으로 받았던 **회전된 refresh 로 `POST /api/auth/refresh`** 를 부른다. **200 이 오면 F-3 확정**이다.
4. **문서 수정 착수 우선순위**: G-4(문서끼리 모순 — 다음 워커가 폴백을 되살린다) → G-1(§8-2 코드 표) → G-8(`.env.example` 규칙, F-1 의 재발 방지) → G-3·G-5(인터페이스 기록) → 나머지.

---

## 자기 점검

- [x] **네 층 전부에 판정을 냈다** — 정책 WARN / 아키텍처-백 PASS / 아키텍처-프론트 FAIL / SPEC FAIL / WP WARN (+ 보안 축 별도 총평).
- [x] **모든 FAIL·WARN 에 파일:줄 + 어긋난 문서 절을 붙였다** — FAIL 3건, WARN 4건 전부.
- [x] **문서 공백을 지적과 분리했다** — 별도 절 13건. 워커가 올린 6건에 판정을 붙이고 7건을 새로 찾았다(G-4 문서 모순 · G-8 · G-9 · G-10 · G-11 · G-12 · G-13 기록).
- [x] **코드·문서를 하나도 고치지 않았다** — `git status --porcelain` 무출력(리포트는 문서 레포의 `orchestration/work/docs-v1/` 에만 썼다). 테스트·빌드를 돌리지 않았다.
- [x] **근거 없는 추측·취향 지적을 싣지 않았다** — 근거를 못 대는 항목(예: `AsyncSession` 이 계층을 넘는가, `ConfirmModal` 의 언마운트 후 `setState`)은 규약에 조문이 없어 제외했다. WORK-003 이후의 미구현과 사이드바 404 는 FAIL 로 잡지 않았다(후자는 G-13 에 기록만).
