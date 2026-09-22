# task-management 참조 조사 — Strong Hajin Tauri 래핑의 입력

> 읽기 전용 조사. 제품 변경 없음. 결정하지 않는다 — 사실과 의도와 미결만 가른다.

## 요약 (10줄)

1. **task_management 는 이미 Tauri 2.x 앱이다.** 추측이 아니라 `src-tauri/` 실물이 있다 — Tauri 2.11.3 · Next.js 정적 export · FastAPI 원격.
2. 그 앱의 형태는 **「FE 번들 동봉 + 원격 API」**다. 셸에 DB·서버를 동봉하지 않는다. 백엔드는 compose 로 서버 1대에 산다.
3. 셸이 가진 것은 **셋뿐**이다 — OS 키체인 커맨드 3개, Windows WebView2 마이크 허용, macOS 마이크 권한 문구. sidecar 없음.
4. **서명·자동업데이트·CI 가 하나도 없다.** `.github/` 자체가 없고 `updater`·서명 설정은 0건이다. 「배포」는 아직 로컬 `tauri build` 까지다.
5. task_management 가 **Bearer + OS 키체인**을 고른 이유가 문서에 박혀 있다 — 앱 창 origin(`tauri://localhost`)과 API origin 이 다르기 때문이다.
6. **Strong Hajin 에는 Tauri 가 0건이다.** 코드에도 문서에도 없다(검색 범위 §4-1).
7. Strong Hajin 은 정반대 전제 위에 있다 — **상대경로 `/api` · `credentials:"same-origin"` · HttpOnly 세션 쿠키 · `window.location.host` 기반 WS**. 전부 same-origin 가정이다.
8. 그래서 **가장 큰 경계는 인증이다.** 쿠키 세션을 `tauri://localhost` 에서 그대로 쓸 수 없고, 백엔드에 **CORS 미들웨어가 아예 없다**.
9. 둘째 경계는 **마이크 포맷**이다 — Strong Hajin 은 `audio/webm;codecs=opus` 를 계약으로 박았고, macOS 웹뷰는 WKWebView 다.
10. 셋째는 **SPA 를 서빙하는 자리가 없다**는 것 — 납품 이미지에 `frontend/dist` 가 들어가지 않고 FastAPI 에 정적 마운트도 없다. 지금 화면을 내보내는 것은 Vite dev 서버뿐이다.

---

## 0. 조사한 체크아웃 상태

| 대상 | 경로 | branch | HEAD | dirty |
|---|---|---|---|---|
| 참조 코드 | `/Users/kknaks/git/toy_pr2/task_management` | `main` | `a720b6ef2c9d7dcfebc2595c4d00cb76621b01d8` | 0건 (clean) |
| 비교 코드 | `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` | `kknaksss/strong-hajin-projects` | `e46ce39c444ee4a5a69d1f8892d51916694fcc0a` | **69건 (작업 중)** |
| 문서 | `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin` | `kknaksss/strong_hajin` | — | 작업 중 |

**기존 변경은 건드리지 않았다.** 읽기만 했고, 이 보고서 한 파일 외에 쓴 것이 없다.

---

## 1. task_management — 무엇이고 어디까지 됐나

### 1-1. 제품

**Tauri 기반 개인 업무 관리 앱.** 타겟은 macOS · Windows 데스크톱.
근거: `/Users/kknaks/git/toy_pr2/task_management/README.md:1-3`, `…/para/projects/summer-star/task-management/README.md:5`

영역은 홈 · 채팅 · 캘린더 · 내 업무 · **회의록** · 자료함 · 메시지 · 설정. v1 구현이 닿은 곳은 화면 트리로 보면 **로그인 · 업무(목록·칸반·상세) · 회의록(준비·라이브·종료) · 설정** 넷이다
(`/Users/kknaks/git/toy_pr2/task_management/app/front/src/app/` 의 라우트 8개).

### 1-2. 문서와 코드의 어긋남 (3건)

| # | 어긋남 | 문서 | 코드 |
|---|---|---|---|
| ① | **제품 지도의 「Work 없음」** | `…/task-management/README.md` 현재 상태 표 — Spec `SPEC-000~002 draft` · Work `없음` | `30-work/` 에 WORK-001~015 가 있고 `20-spec/` 에 SPEC-000~011 이 있다. 지도가 2026-09-01 상태에서 멈췄다 |
| ② | **「웹 우선, Tauri 는 마지막 포장」이 남아 있다** | `40-architecture/system/README.md:29-32` mermaid 가 아직 `Tauri 셸 (래핑 후에만)` · `래핑 후 위임` 이고, 같은 문서 §External Integrations 「토큰 저장소」 줄이 **「웹 개발 중에는 브라우저 저장소로 임시 대체」** 라고 쓴다 | 같은 문서 `:22-25` 가 **「처음부터 Tauri 앱으로 개발한다(§C-4, 2026-09-05 번복)」** 로 번복했고, 코드는 번복 쪽이다 — `…/app/front/src/lib/auth/tokenStore.ts:125-129` 는 셸이 없으면 **예외를 던진다.** 브라우저 저장소 폴백이 **없다**. `work-001-scaffold.md:301` 이 이 어긋남을 `S000-OQ-2 미해소` 로 스스로 적어 뒀다 |
| ③ | **코드 레포 위치** | `…/task-management/README.md` 코드 레포 표 — 「별도 clone 예정(2026-09-05 확정)… 이 레포의 `app/back` 은 kknaks_profile 제품이라 쓰지 않는다」 | 실제 코드는 `/Users/kknaks/git/toy_pr2/task_management/app/{back,front,mcp}` 에 있다. clone 은 이미 됐고 표가 안 따라갔다 |

②는 **이번 설계에 직접 걸린다.** 「마지막에 래핑한다」로 읽고 SH 를 설계하면, task_management 가 번복하며 남긴 이유(아래 §3-5)를 그대로 다시 밟는다.

---

## 2. task_management 구조 — 브라우저에서 서버까지

### 2-1. 배치

```
┌─ 클라이언트 (macOS · Windows) ────────────┐      ┌─ 서버 1대 · docker compose ──────────────┐
│  Tauri 셸 (Rust)                          │      │  api      FastAPI :8000                  │
│   └ WKWebView / WebView2                  │      │  db       PostgreSQL 16                  │
│      └ Next.js 정적 번들 (out/)           │─────▶│  redis    open-kknaks 브로커             │
│                                           │ REST │  worker   codex CLI 데몬 (호스트 번들 ro)│
│   커맨드 3개: 키체인 get/set/clear        │  WS  │  mcp      MCP 도구 7개 (별도 이미지)     │
└───────────────────────────────────────────┘      │  volume   storage (녹음 원본 · md)       │
                                                   └──────────────────────────────────────────┘
                                                        │
                                                        └─▶ Soniox (stt-rt-v5 WS · stt-async-v5 REST)
```

근거: `/Users/kknaks/git/toy_pr2/task_management/docker-compose.local.yml` (services: db · redis · api · mcp · worker) ·
`…/para/projects/summer-star/task-management/40-architecture/system/README.md` §런타임 배치.

### 2-2. 표면별 사실

| 층 | 사실 | 근거 |
|---|---|---|
| **FE 런타임** | Next.js 15.5.25 · React 19 · `output:"export"` · `trailingSlash:true` · `images.unoptimized`. **Route Handler · middleware · Server Action · 동적 세그먼트 `[id]` 전부 금지**이고, 그 금지를 테스트가 지킨다 | `…/app/front/next.config.ts:16-22` · `…/app/front/src/test/staticExport.test.ts:36-57` |
| **API 주소** | **빌드 시점 상수.** `NEXT_PUBLIC_API_BASE` 를 읽는 곳이 `lib/env.ts` **하나**이고, 앱 안에서 서버를 바꾸는 화면이 v1 에 없다 | `…/app/front/src/lib/env.ts:22-26` · `…/app/front/.env.example:9` |
| **HTTP** | 모든 호출이 `apiFetch` 하나를 지난다. 절대 URL 조립(`buildUrl`) · Bearer 부착 · 401 갱신 1회 · 재시도 1회 · 실패는 `ApiError{status,code,detail}` | `…/app/front/src/lib/api/client.ts:42-44, 85-121` |
| **WS** | `new WebSocket(` 이 `lib/api/ws.ts` 밖에 0건. URL 은 `env.apiBase` 를 `http→ws` 치환. **헤더를 못 붙이므로 연결 직후 첫 텍스트 프레임에 access 토큰**을 싣는다. `4401` 이면 갱신 1회 → 재연결 1회, 또 실패하면 끝(루프 없음). 재접속·백오프·핑 없음 | `…/app/front/src/lib/api/ws.ts:8-16, 62-64` |
| **인증** | **Bearer.** access 는 메모리만, refresh 는 「유지」 체크일 때만 **OS 키체인**. 브라우저 저장소 폴백 없음 | `…/app/front/src/lib/auth/tokenStore.ts:7-15, 109-139` |
| **CORS** | 명시 목록. `*` 없음, `allow_credentials=False`(쿠키 안 씀) | `…/app/back/main.py:92-98` · `…/.env.example:22` = `http://localhost:3000,tauri://localhost,http://tauri.localhost` |
| **마이크** | 캡처는 **웹 `getUserMedia`** 가 한다. 셸은 **권한만** 연다 | `…/40-architecture/system/README.md` §Components · `…/app/front/src-tauri/src/lib.rs:3-5` |
| **파일** | 업로드 경로가 따로 없다. 녹음은 WS 로 올라온 청크를 서버가 `STORAGE_ROOT/recordings/{id}.{ext}` 에 **append** 한다. DB 는 경로만 든다 | `…/app/back/integrations/storage.py:3-5, 44-56` |
| **AI** | back 은 LLM SDK 를 import 하지 않는다. `Redis → open-kknaks worker → codex CLI`, codex 가 우리 데이터를 읽는 길은 **별도 컨테이너의 MCP 도구 7개(조회 전용)** | `docker-compose.local.yml` worker·mcp 서비스 · `…/40-architecture/system/README.md` §Components |

### 2-3. 앱 창의 origin 세 가지 — 이 표가 핵심이다

| 환경 | 창의 origin |
|---|---|
| `tauri dev` | `http://localhost:3000` (devUrl 을 그대로 문다) |
| 배포 번들 · macOS | `tauri://localhost` |
| 배포 번들 · Windows | `http://tauri.localhost` |

근거: `…/app/front/README.md` §「알아 둘 것 두 가지」 1.
**셋 다 백엔드 `CORS_ORIGINS` 에 있어야 한다.** 그리고 API 주소는 `tauri.conf.json` 의 CSP `connect-src` 에도 박혀 있어, `NEXT_PUBLIC_API_BASE` 를 바꾸면 **CSP 도 같이 고쳐야 한다.**

---

## 3. task_management 의 Tauri 구성 — 전수

### 3-1. 버전과 자리

| 항목 | 값 | 근거 |
|---|---|---|
| Tauri 크레이트 | **2.11.3** | `…/app/front/src-tauri/Cargo.toml:22` |
| `tauri-build` | 2.6.3 | 같은 파일 `:16` |
| `@tauri-apps/cli` | 2.11.4 / `@tauri-apps/api` ^2.11.1 | `…/app/front/package.json` |
| rust-version | 1.77.2 (검증 rustc 1.97) | `Cargo.toml:9` · `…/app/front/README.md` 버전 핀 표 |
| 셸 디렉토리 | `app/front/src-tauri` — **Tauri CLI 관례(프론트 루트의 형제). 아키텍처 문서에 규약이 없어 WORK-001 이 정했다** | `…/30-work/work-001-scaffold.md:299` |
| 번들 identifier | `com.kknaks.task-management` | `…/src-tauri/tauri.conf.json` |

### 3-2. Rust ↔ JS 경계 — 커맨드 정확히 3개

```rust
keychain_get_refresh_token()  -> Result<Option<String>, String>   // 없음은 실패가 아니다
keychain_set_refresh_token(token: String) -> Result<(), String>   // 회전마다 덮어쓴다
keychain_clear_refresh_token() -> Result<(), String>              // 이미 없으면 성공
```
`/Users/kknaks/git/toy_pr2/task_management/app/front/src-tauri/src/lib.rs:22-47, 110-114`

**JS 쪽에서 이 커맨드를 부르는 파일도 하나뿐이다** — `src/lib/auth/tokenStore.ts:20-23`. 그 밖에서 부르면 리뷰 반려로 규약화했고, 셸 유무 판정은 `"__TAURI_INTERNALS__" in window` 다(`tokenStore.ts:50-52`).

### 3-3. 권한 · 플러그인

- **capabilities 는 `core:default` 하나뿐이다** — `…/src-tauri/capabilities/default.json`. fs·dialog·shell 플러그인 권한을 하나도 열지 않았다.
- 플러그인은 `tauri-plugin-log` **하나**, 그것도 `debug_assertions` 일 때만 붙인다(`lib.rs:94-100`).
- **sidecar 가 없다.** `externalBin`·`shell` 플러그인·번들 리소스가 `tauri.conf.json` 에 0건이다. 백엔드를 앱에 동봉하지 않는다는 결정이 설정에 그대로 나타난다.

### 3-4. OS 권한 — 마이크 한 가지, 플랫폼 두 갈래

| 플랫폼 | 하는 일 | 근거 |
|---|---|---|
| macOS | `Info.plist` 의 `NSMicrophoneUsageDescription` 이 프롬프트를 띄운다. 서명본(hardened runtime)에서는 `Entitlements.plist` 의 `com.apple.security.device.audio-input` 이 **없으면 거부**된다. Rust 코드는 할 일이 없다 — wry 의 `WKUIDelegate` 가 WebKit 단계를 Grant 한다 | `…/src-tauri/Info.plist` · `Entitlements.plist` · `lib.rs:55-56` |
| Windows | **셸이 직접 허용한다.** wry 0.55 는 `PermissionRequested` 에서 CLIPBOARD_READ 만 허용하므로, `webview2-com` 으로 `COREWEBVIEW2_PERMISSION_KIND_MICROPHONE` 을 `ALLOW` 로 세운다. 안 걸면 `getUserMedia` 가 **프롬프트 없이** 실패한다 | `lib.rs:49-88` |

여기에 붙은 **운영 함정 하나**가 코드 주석에 남아 있다 — `Info.plist` 만 고치면 재컴파일이 안 돼 반영되지 않는다. `lib.rs` 를 건드리거나 `cargo clean -p app` 이 필요하다(`…/app/front/README.md` 표).

### 3-5. 왜 Bearer + 키체인인가 (SH 설계에 그대로 걸리는 근거)

`…/40-architecture/system/README.md` §흐름 ① 이 두 줄로 못박는다.

> ① 정적 번들이 실린 웹뷰의 origin(`tauri://` 계열)과 API origin 이 다르다 — 쿠키를 붙이려면 `SameSite=None; Secure` 에 웹뷰별 3rd-party 쿠키 정책까지 걸린다.
> ② 「앱 종료 시 로그아웃」을 세션 쿠키 수명에 맡기면 **웹뷰 구현에 따라 갈린다.**

그리고 `:22-25` 가 **개발 순서 번복**의 이유를 적는다 — 「마지막에 래핑하면 **마이크·키체인·origin/CORS 가 한꺼번에 터지는데**, 그 셋이 Bearer+키체인을 고른 근거이기도 하다.」

### 3-6. 앱 수명주기 · 업데이트 · 서명 · CI — **없다**

| 항목 | 상태 | 검색 범위 |
|---|---|---|
| 창 | 단일 창 `main` 1440×900 · resizable · fullscreen=false. 트레이·메뉴·다중 창·딥링크 없음 | `tauri.conf.json` `app.windows` |
| 수명주기 훅 | `setup` 하나(로그 플러그인 + Windows 마이크). `on_window_event`·종료 훅·단일 인스턴스 없음 | `lib.rs:92-115` |
| **자동 업데이트** | **0건.** `updater`·`createUpdaterArtifacts`·pubkey 설정이 없다 | 레포 전체 `*.json *.yml *.yaml *.rs *.toml *.md` 에서 `updater\|createUpdaterArtifacts` grep — `node_modules`·`src-tauri/target`·`Cargo.lock` 제외, **0 hit** |
| **서명 / 공증** | **0건.** `signingIdentity`·`notariz`·`APPLE_ID`·`TAURI_SIGNING_*` 없음. macOS 는 `infoPlist`·`entitlements` 지정만 있고 서명 identity 가 없다 | 같은 grep, 0 hit |
| **CI** | **`.github/` 디렉토리 자체가 없다** | `ls -a` 레포 루트 |
| 산출물 | `bundle.targets: "all"`, 아이콘 5종. 굽는 명령은 사람이 로컬에서 `npm run tauri build` | `tauri.conf.json` · `…/app/front/README.md` |
| 빌드 경로 | `Makefile` 의 `app`(= `npm run tauri dev`) · `front-build`(= `out/` 만) 두 개. **`tauri build` 타겟은 Makefile 에 없다** | `…/task_management/Makefile` |

> 즉 **「Tauri 로 앱을 만든다」까지는 실물이 있고, 「앱을 배포한다」는 아직 없다.** 서명·공증·업데이트·CI 는 SH 가 참조할 선례가 **없는** 자리다.

---

## 4. Strong Hajin 현 구조

### 4-1. Tauri 부재 — 검색 범위를 밝힌다

- `grep -rniI "tauri"` — 레포 전체에서 `node_modules`·`.git`·`target` 제외. **0 hit.**
- `find` 로 `Cargo.toml` · `src-tauri` · `tauri.conf.json` — `node_modules` 제외. **0 hit.**
- 문서 `para/projects/summer-star/strong-hajin/` 에서 `tauri|데스크톱|데스크탑|네이티브|오프라인|설치형` — **0 hit.** (`배포` 는 전부 **스키마→코드 순서·롤백** 문맥이고 앱 배포가 아니다.)

**Strong Hajin 은 Tauri 를 쓰지 않고, 데스크톱 앱을 문서에서 다룬 적도 없다.**

### 4-2. 스택

| 층 | task_management | **Strong Hajin** |
|---|---|---|
| FE 빌드 | Next.js 15 정적 export → `out/` | **Vite 7 + React 19 SPA** → `frontend/dist/` |
| 라우팅 | Next App Router, 동적 세그먼트 **금지** | **라우터 없음.** 화면 전환은 React state, 유일한 URL 파라미터가 `?interaction=` |
| BE | FastAPI, `app/back` 단일 서비스 | FastAPI, **modular monolith** `ax_workspace` (modules: work · meetings · actions · reports · jobs · datasets · organization_access · ax_execution) |
| DB | PostgreSQL 16 | PostgreSQL 16.6 (`docker-compose.yml` 은 **postgres 만**) |
| 워커 | Redis 브로커 + open-kknaks 데몬 1종 | **Postgres 테이블이 큐** + 전용 워커 4종 (conversation · material · meeting · report) |
| AI | codex via open-kknaks + **별도 MCP 컨테이너** | codex CLI 직접 + **stdio MCP** (`SCAX_RUNTIME_EXECUTABLE`) |
| STT | Soniox (rt + async) | Soniox (credential 은 런타임 주입) |
| 납품 | compose 로 서버 1대 | **Nuitka 컴파일 보호 이미지** `linux/amd64`, 역할 dispatch (`api` · 워커 4 · `mcp`) |

근거: `…/strong-hajin-projects/frontend/package.json` · `frontend/vite.config.ts` · `backend/pyproject.toml` · `docker-compose.yml` · `delivery/Dockerfile` · `delivery/README.md`.

### 4-3. SH 가 **same-origin 을 전제로** 짜여 있다 (래핑의 핵심)

| 표면 | 코드 | 절대경로:줄 |
|---|---|---|
| REST | `fetch(path, { credentials: "same-origin" })` — **상대경로 그대로.** base URL 주입 지점이 없다 | `…/strong-hajin-projects/frontend/src/lib/api.ts:126-135` |
| 멀티파트 업로드 | `request()` 를 **안 지나고** 직접 `fetch('/api/…', {credentials:'same-origin', body: form})` | 같은 파일 `:103`, `:118` (그리고 FormData 사용처가 더 있다 — 전수조사 필요) |
| WS | `window.location.protocol/host` 로 조립. 주석이 **「같은 오리진이라 세션 쿠키가 핸드셰이크에 실린다 — 토큰을 주소에 붙이지 않는다」** 라고 명시 | `…/frontend/src/features/meetings/stream.ts:70-74` |
| 인증 | **HttpOnly 세션 쿠키** `scax_session` · `samesite="lax"` · `secure` 는 production 프로파일일 때만 | `…/backend/src/ax_workspace/entrypoints/http_auth.py:21-23` · `…/entrypoints/http.py:639-646` |
| WS 인증 | 첫 프레임은 **역할만** 싣고 토큰을 안 싣는다. 사람을 정하는 것은 **쿠키** | `…/entrypoints/http_auth.py:82-90` · `stream.ts:90-93` |
| **CORS** | **미들웨어가 없다.** `create_app()` 에 `add_middleware` 0건 | `…/entrypoints/http.py:605` (검색: 같은 파일 `CORS\|add_middleware\|StaticFiles\|mount` grep → 0 hit) |
| 정적 서빙 | **없다.** FastAPI 에 `StaticFiles` 마운트 0건, 납품 이미지 `.dockerignore` 가 `backend/`·`delivery/` 만 허용해 `frontend/` 가 build context 에 **들어가지 않는다** | 위 grep · `…/strong-hajin-projects/.dockerignore` |
| 백엔드가 만드는 링크 | `open_url = AX_WEB_ORIGIN + '/?interaction=' + id`, 그리고 `AX_WEB_ORIGIN` 은 **「HTTP(S) origin」이어야 한다**고 검증한다 — `tauri://localhost` 를 넣을 수 없다 | `…/backend/src/ax_workspace/modules/ax_execution/browser_interactions.py:318` · `…/bootstrap/settings.py:97-111, 170` |
| 외부 링크 | `window.open(resource.origin, "_blank", …)` — 웹뷰에서 새 창/외부 브라우저 처리가 필요하다 | `…/frontend/src/App.tsx:682` |
| 마이크 | `MediaRecorder` **`audio/webm;codecs=opus`**, 250ms · 64KB 청크. 주석이 **「여기서 고른 것이 곧 계약」**이라 쓴다. 별도 경로(`browser/`)는 mp4 도 받는다 | `…/frontend/src/features/meetings/microphone.ts:11, 17, 37` vs `…/lib/api.ts:102` |
| 브라우저 저장소 | 초안 2종만 `localStorage`(대화 초안 · 액션 초안). 토큰은 안 넣는다(쿠키라서) | `…/frontend/src/features/chat/useConversations.ts:41,55` · `…/features/work/useActionDraft.ts:29,45` |

### 4-4. 프로파일 게이트 — 알아 둘 사실

`create_app()` 의 **`@app.` 데코레이터 160개 중 159개가 `if settings.developer_auth_enabled:` 블록 안**에 있다. 조건 밖에 있는 것은 `/health` 하나뿐이다.
근거: `…/entrypoints/http.py:606` · `:2530` · `developer_auth_enabled` 정의 `…/bootstrap/settings.py:124-126` (= `DEVELOPMENT` 또는 `TEST`).
그리고 `local_login_enabled` 주석이 **「Production 은 외부 provider 로 신원을 증명한다」**고 쓰지만(`settings.py:128-131`), 그 OIDC 경로는 코드에 없다.

> 뜻: **지금 Strong Hajin 을 앱으로 띄우면 그 앱이 붙는 서버는 development/test 프로파일이다.** 「개인용 앱」이면 그래도 되지만, **그것이 선택임을 알고 골라야 한다.** production 프로파일에서는 로그인 자체가 없다.

---

## 5. 비교표 — 그대로 쓸 것 / 바꿔야 할 것

| 축 | task_management (참조) | Strong Hajin (현재) | 래핑 시 |
|---|---|---|---|
| FE 산출물 | 정적 export `out/` | Vite `dist/` | **그대로 쓸 수 있다.** `frontendDist` 에 `dist` 를 주면 된다 |
| 라우팅 | 동적 세그먼트 금지(정적 export 제약) | 라우터 없음 — 애초에 제약이 없다 | **SH 가 더 유리하다.** 단 `?interaction=` 딥링크는 별도 처리 |
| API 주소 | `env.apiBase` 절대 URL, 읽는 곳 **1곳** | 상대경로, **주입 지점 없음** | **바꿔야 한다** — `request()` 하나로는 안 끝난다(멀티파트가 밖에 있다) |
| WS 주소 | `env.apiBase` 치환, `new WebSocket` **1곳** | `window.location.host`, `new WebSocket` 1곳 | **바꿔야 한다** |
| 인증 | Bearer + OS 키체인 (`tauri://` 때문에 고른 것) | **HttpOnly 세션 쿠키** | **가장 큰 경계.** §6 에서 갈린다 |
| CORS | 명시 3-origin, `allow_credentials=False` | **미들웨어 없음** | 쿠키를 유지하면 `allow_credentials=True` + 정확한 origin 이 필요하고, `tauri://` 스킴은 브라우저 CORS 규격 밖이다 |
| 마이크 권한 | Info.plist + Entitlements + WebView2 핸들러 | 없음 (브라우저가 함) | **그대로 이식 가능** — task_management 의 `lib.rs:49-88` · plist 2종이 거의 그대로 쓰인다 |
| 마이크 포맷 | 구현 시점에 고름(아키텍처가 특정 안 함) | **webm/opus 로 계약 고정** | macOS WKWebView 에서 확인 필요. SH 의 `browser/` 경로는 이미 mp4 분기가 있다 |
| 저장소 | OS 키체인 커맨드 3개 | localStorage 초안 2종 | 인증을 어떻게 가느냐에 따라 키체인이 필요할 수도, 전혀 필요 없을 수도 있다 |
| 정적 서빙 | 필요 없음(셸이 싣는다) | **서버가 SPA 를 못 낸다** | 래핑 방식과 무관하게 **한 번은 정해야 한다** |
| 서명·업데이트·CI | **없음** | 없음 | **선례가 없다.** 참조할 것이 없는 유일한 영역 |

### 재사용 가능한 패턴 (task_management 에서 그대로 끌어올 수 있는 것)

1. **셸의 책임을 셋으로 좁히는 규약** — 「데이터·비즈니스 로직·화면은 셸에 없다」(`lib.rs:1-8`). SH 도 이대로 가면 Rust 코드가 100줄을 안 넘는다.
2. **Windows WebView2 마이크 허용 코드** — `lib.rs:49-88` 는 SH 에 그대로 복사 가능한 수준이다(wry 버전 핀 `webview2-com = "0.38"` 포함).
3. **macOS plist 2종과 그 함정 주석** — `Info.plist`·`Entitlements.plist` 및 「plist 만 고치면 반영 안 된다」.
4. **경계를 파일 하나로 좁히는 규칙** — 「`process.env` 를 읽는 곳은 `env.ts` 하나」·「`new WebSocket(` 은 `ws.ts` 밖에 0건」·「키체인을 부르는 곳은 `tokenStore.ts` 하나」. **SH 의 `lib/api.ts` 는 이미 request() 가 있지만 멀티파트가 밖으로 샜다** — 래핑 전에 이 규칙을 먼저 세우면 주소 주입이 한 곳에서 끝난다.
5. **CSP 에 API 주소를 박는 방식과 그 대가** — `connect-src` 에 주소가 박혀 「서버 주소 설정 화면이 없다」와 짝을 이룬다. SH 가 서버 주소를 바꿀 수 있게 하려면 이 짝을 같이 뒤집어야 한다.
6. **origin 3종 표** — 개발·macOS·Windows. CORS·CSP·쿠키 정책이 전부 이 표에 걸린다.

---

## 6. 래핑 세 갈래 — 현 코드 기준의 차이

**아직 고르지 않는다.** 아래는 각 갈래가 **현재 코드에 무엇을 요구하는지**다.

### A. 원격 웹 URL 래퍼 (창이 서버의 http origin 을 그대로 연다)

| | 내용 |
|---|---|
| FE 코드 변경 | **거의 0.** 상대경로 `/api`·same-origin 쿠키·`window.location.host` WS 가 **전부 그대로 성립한다** — 문서의 origin 문제가 아예 발생하지 않는다 |
| 백엔드 변경 | **SPA 를 서빙할 자리를 만들어야 한다.** 지금 `dist/` 를 내보내는 것은 Vite dev 서버뿐이고, 납품 이미지에 `frontend/` 가 들어가지 않는다(`.dockerignore`) |
| 막히는 지점 ① | **`getUserMedia` 는 secure context 를 요구한다.** `http://localhost` 는 secure context 지만 `http://<LAN IP>` 는 아니다 — 원격 서버를 평문 HTTP 로 열면 **마이크가 안 열린다.** SH 는 회의 라이브·브라우저 녹음 둘 다 마이크를 쓴다 |
| 막히는 지점 ② | 셸이 **원격 문서**를 싣는다 — 키체인 같은 네이티브 커맨드를 여는 순간 원격 origin 에 네이티브 권한을 주는 셈이다 |
| task_management 선례 | **없다.** task_management 는 이 길을 가지 않았다 |

### B. FE 번들 동봉 + 원격 API (= task_management 방식)

| | 내용 |
|---|---|
| FE 코드 변경 | **주소 주입 전수** — `request()` 1곳 + `request()` 를 우회하는 멀티파트 fetch(최소 `api.ts:103`, `:118`) + WS 1곳. task_management 가 「읽는 곳은 하나」로 규약화한 이유가 여기다 |
| 인증 | **최대 작업.** `tauri://localhost` ↔ `http://server` 는 cross-site 이고 쿠키는 `SameSite=Lax` 다. task_management 는 **이 문제 때문에** 쿠키를 버리고 Bearer + 키체인으로 갔다(`system/README.md` §흐름 ①). SH 는 세션 쿠키 + **쿠키 기반 WS 인증**이라 둘 다 바뀐다 |
| 백엔드 변경 | CORS 미들웨어 신설 + origin 3종 등록 + (쿠키 유지 시) `allow_credentials=True`. `AX_WEB_ORIGIN` 은 http(s) 만 받으므로 `open_url` 딥링크도 정해야 한다 |
| 마이크 | webm/opus 계약을 macOS WKWebView 에서 확인해야 한다. Windows 는 WebView2 권한 핸들러 필요(task_management 코드 이식) |
| task_management 선례 | **전부 있다.** 이 길만이 실물 선례를 가진다 |

### C. 로컬 백엔드 동봉 (sidecar)

| | 내용 |
|---|---|
| 필요한 것 | PostgreSQL 16 · 워커 4종 · codex CLI · Soniox credential · 자료/녹음 볼륨 |
| task_management 의 판단 | **이 길을 명시적으로 기각했다.** 근거 넷 — ① codex 를 기기마다 깔 수 없다 ② 녹음 원본이 영구 보관이다 ③ STT 키는 사용자 기기에 둘 수 없다 ④ 단일 사용자라 서버 1대로 충분하다 (`…/40-architecture/system/README.md` §런타임 배치) |
| SH 는 더 무겁다 | 납품 이미지가 **Nuitka standalone + codex native + Debian runtime** 으로 800MB 대이고(`delivery/README.md` 표), `linux/amd64` 고정이다. macOS·Windows 데스크톱에 얹을 형태가 아니다 |
| 결론 | **현 코드 기준으로 가장 멀다.** 고르려면 SH 백엔드의 배치 전제부터 다시 정해야 한다 |

---

## 7. 이미 답이 난 것 / 사용자에게 물어야 할 것

### 7-1. 조사로 답이 난 것 (다시 논의하지 않는다)

1. task_management 는 **Tauri 2.11.3 실물**이 있다. 「Tauri 인가」는 전제가 아니라 확인된 사실이다.
2. 그 앱의 형태는 **B(FE 동봉 + 원격 API)** 이고, **C(백엔드 동봉)는 근거 넷으로 기각**됐다.
3. 그 앱의 인증이 Bearer + OS 키체인인 이유는 **`tauri://` origin 과 API origin 이 다르기 때문**이다. 취향이 아니라 제약이다.
4. task_management 에는 **서명·공증·자동업데이트·CI 가 하나도 없다.** SH 가 이 영역에서 베낄 것은 없다.
5. Strong Hajin 에는 **Tauri 가 코드에도 문서에도 0건**이다.
6. Strong Hajin 은 **same-origin 전제**(상대경로 · 세션 쿠키 · location 기반 WS)이고 **백엔드에 CORS 가 없다.**
7. Strong Hajin 의 **SPA 를 서빙하는 자리가 아직 없다**(FastAPI 정적 마운트 없음 · 납품 이미지에 `frontend/` 없음). 어느 갈래를 골라도 이건 정해야 한다.
8. Strong Hajin 의 마이크 계약은 **webm/opus 로 코드에 고정**돼 있다.
9. Strong Hajin 의 HTTP 표면 **160개 중 159개가 development/test 프로파일 게이트 안**에 있다.
10. task_management 문서에는 **번복이 안 반영된 절이 남아 있다**(§1-2 ②) — `S000-OQ-2` 로 이미 기록된 미해소 항목이다.

### 7-2. 사용자에게 물어야 할 것 (5개 — 이 답이 갈리면 구조가 갈린다)

| # | 질문 | 왜 이게 갈림길인가 |
|---|---|---|
| **Q1** | **서버는 어디서 도나 — 이 맥(로컬)인가, 다른 기기(홈서버 등)인가?** | 로컬이면 `http://localhost` 가 secure context 라 **A(원격 URL 래퍼)가 코드 변경 거의 0으로 성립**한다. 원격이면 HTTPS 가 필요하고(마이크), 그 순간 A 의 매력이 크게 줄어 B 로 기운다 |
| **Q2** | **인증을 쿠키 그대로 둘 것인가, Bearer 로 갈 것인가?** | 쿠키 유지 = A 로 기운다. Bearer 전환 = B 가 열리고 task_management 선례를 그대로 쓸 수 있지만, **REST·WS 인증·백엔드 세션 저장소를 함께 고쳐야 한다**. 이 하나가 작업량을 가장 크게 가른다 |
| **Q3** | **회의 라이브 녹음(마이크)을 앱에서 쓸 것인가?** | 쓰면 → macOS plist·entitlements·Windows WebView2 핸들러가 필요하고, **webm/opus 가 WKWebView 에서 되는지 실측**이 선행 조건이 된다. 안 쓰면 → 셸이 창만 띄우면 되고 Rust 코드가 거의 0이 된다 |
| **Q4** | **타겟 OS 는?** (macOS 만 / macOS + Windows) | Windows 를 넣으면 WebView2 마이크 핸들러·`http://tauri.localhost` origin·Windows 검증 시점이 한꺼번에 따라온다. task_management 도 이걸 `S000-OQ-3` 로 미결로 남겼다 |
| **Q5** | **배포를 어디까지 보나 — 내 기기에서 빌드해 쓰면 끝인가, 서명·자동업데이트까지 가나?** | 「빌드해서 쓴다」면 참조가 충분하다. 서명·공증·업데이트·CI 까지면 **task_management 에 선례가 없어** 이 작업이 새로 설계할 영역이 된다 |

> 보조 질문(설계 때 반드시 닫히지만, 지금 답이 없어도 조사가 막히지 않았다):
> SPA 서빙을 **서버에 붙일지 셸에 실을지**(Q1·Q2 가 정해지면 대부분 따라온다) · 서버 주소를 **앱 안에서 바꿀 수 있게 할지**(task_management 는 「없다」로 갔고 그래서 CSP 에 주소를 박았다) · **`AX_PROFILE` 을 무엇으로 두고 붙을지**(§4-4).

---

## 8. 이 조사의 한계

- **SH 워크트리가 dirty(69건)** 다. 위 SH 인용은 **작업 중 상태의 파일**을 읽은 것이고, FE 작업이 진행 중이라 `frontend/src` 는 변할 수 있다. 계약에 해당하는 인용(`lib/api.ts` 의 `request()`·`stream.ts`·`microphone.ts`)은 성격상 잘 안 바뀌는 자리지만, 설계 착수 시 다시 확인하는 편이 안전하다.
- **부재 주장은 전부 검색 범위를 밝혔다**(§3-6 · §4-1 · §4-3). `node_modules`·`.git`·`target`·`Cargo.lock` 은 제외했다.
- **실행하지 않았다.** 빌드·테스트·컨테이너 기동을 하지 않았으므로, 「webm/opus 가 WKWebView 에서 되는가」 같은 **실측 항목은 답하지 않았다** — 열어 둔다.
- **웹 리서치를 하지 않았다.** Tauri 의 현재 동작에 관한 서술은 전부 레포 안의 코드·주석·문서에서만 가져왔다.
- `.env`·인증서·키 파일은 **열지 않았다.** `.env.example` 의 키 **이름**만 인용했다.
