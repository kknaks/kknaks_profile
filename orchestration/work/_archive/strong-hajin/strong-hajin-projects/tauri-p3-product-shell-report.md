# WORK-006 Phase 3 완료 보고 — 제품 Tauri 셸

- **발주**: `tauri-p3-product-shell-brief.md`
- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · 브랜치 `kknaksss/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **상태**: **완료.** M-7(연결 실패 감지)을 **BLOCKED 로 올리지 않고 구현했다**
- **M-1 은 여전히 미측정** — 이 Phase 에서 최종 통과로 닫지 않았다
- 커밋 · push · PR · Release **없음**

---

## 1. 한 줄 결론

탐침을 제품 셸로 다시 세웠다. **커맨드 넷 · 네이티브 소유 · TTL/renew/refcount 없음 ·
`Op::Shutdown` · 완료 사건 정리 · 허용 목록 둘**을 그대로 지켰고, 탐침 손잡이는 하나도
넘어오지 않았다. **W-4 는 실제 실행으로 해소**했고(재무장이 assertion 을 정말 다시 만든다),
**W-5 는 구조로 해소**했으나 **Windows 는 컴파일조차 되지 않아 실행 증거가 없다.**
**U-2 는 M-7 관측을 설계 입력으로 삼아 「로드 감시 + 연결 전수」 두 신호로 구현**했다.

---

## 2. 변경 파일

**허용 범위 밖은 0줄이다.** `frontend/src/**` · `App.tsx` · `features/**` · `api.ts` ·
`microphone.ts` · `backend/**` · SPEC/WP/index/log **무변경**(§8 의 확인 참조).

### 새로 생긴 것

| 파일 | 역할 |
|---|---|
| `src-tauri/src/connection.rs` | **M-7 흡수** — 로드 감시(`LoadWatch`) + 연결 전수(`probe`) |
| `src-tauri/src/shell_ui.rs` | 셸이 그리는 화면 둘 — **U-2** 와 「주소 미설정」 |
| `src-tauri/src/config.rs` | 여는 주소 · **네비게이션** 허용 목록(커맨드 허용 origin 과 별개) |
| `src-tauri/shell.config.json` | 운영 주소 **설정 자리**. 지금은 `null` |
| `src-tauri/capabilities/product-shell.json` | 제품 capability (`probe-fixture.json` 은 삭제) |
| `src-tauri/shell-noop/index.html` | `frontendDist` 가 실재 경로를 요구해 둔 빈 자리. **화면에 뜨지 않는다** |

### 고친 것

| 파일 | 변경 |
|---|---|
| `src-tauri/src/lib.rs` | 탐침 → **제품 셸**. 커스텀 스킴 화면 · 로드 감시 배선 · 탐침 손잡이 제거 |
| `src-tauri/src/power.rs` | **W-4**(macOS 재무장) · **W-5**(Windows 해제) · 회귀 시험 |
| `src-tauri/src/guard.rs` | 제품이 쓰지 않는 `generation` 장부 제거(죽은 API 를 남기지 않는다) |
| `src-tauri/Cargo.toml` | 패키지명 `strong-hajin-shell` · `native-tls` 추가 |
| `src-tauri/tauri.conf.json` | 제품명 · 식별자 · 창을 Rust 가 만들도록 |
| `src-tauri/src/main.rs` | 크레이트명 변경 반영 |

> `frontend/package.json` 은 **이번에 건드리지 않았다**(Phase 1 상태 그대로).
> ⚠ 다만 Phase 1 이 넣은 `probe:shell` 스크립트(`tauri dev`)는 이제 **제품 셸**을 띄운다.
> 이름이 오해를 부르므로 정리 대상으로 올린다(§9).

---

## 3. 커맨드와 권한 — 세어서 적는다

| 항목 | 수 | 확인 |
|---|---|---|
| 웹에 여는 커맨드 | **4** | `shell_info` · `wake_guard_acquire` · `wake_guard_release` · `open_external` |
| capability 의 권한 | **4** | `allow-shell-info` · `allow-wake-guard-acquire` · `allow-wake-guard-release` · `allow-open-external` |
| 파일·프로세스·범용 셸·`open_path` 권한 | **0** | 시험 `웹에_여는_커맨드는_정확히_넷이다` 가 `fs:`·`shell:`·`process:`·`opener:`·`open-path`·`reveal-item` 을 전수로 막는다 |
| 커맨드 허용 origin | **1** | 와일드카드 서브도메인 없음 |
| `local` | **`false`** | 셸 자기 화면(`stronghajin://`)도 커맨드를 부르지 못한다 — 리뷰 W-6 도 함께 닫혔다 |

`open_external` 은 `http`/`https` 만 받고, **앱 창도 두 번째 웹뷰도 만들지 않는다**
(`tauri_plugin_opener::open_url` 로 OS 기본 브라우저에 넘길 뿐이다).
opener 플러그인의 **권한은 웹에 주지 않았다** — Rust 쪽에서만 쓴다.

### 허용 목록 둘을 갈라 두었다 (SPEC-006 §5)

- **커맨드** 허용 origin → `capabilities/product-shell.json` 의 `remote.urls` **정확히 하나**
- **네비게이션** 허용 origin → `shell.config.json` 의 `navigationAllowlist` + 운영 origin
- 인증 흐름이 거치는 주소가 생기면 **네비게이션 쪽만 넓어지고, 그 주소에 네이티브 권한은 가지 않는다**

### 운영 origin 은 **승격하지 않았다** (OQ-T02)

- `shell.config.json` 의 `operationalOrigin` = **`null`**
- capability 의 `remote.urls` = `https://operational-origin-not-yet-decided.invalid/*`
  (`.invalid` 는 RFC 2606 예약 TLD — **실재할 수 없는 자리표시**)
- 시험 `운영_origin_은_아직_자리로만_있다` 가 **fixture 주소 승격과 운영 도메인 발명을 둘 다 막는다**
- 값이 비어 있으면 셸은 가짜 주소로 도는 대신 **「서버 주소가 설정되지 않았습니다」 화면**을 연다

---

## 4. U-2 — M-7 을 **정직하게** 흡수했다

### 문제 (Phase 2 M-7 관측)

TLS 가 거절되면 `on_page_load` 가 **`Started` 도 `Finished` 도 발화하지 않는다.**
페이지 훅만으로는 「아직 안 왔다」와 「영영 안 온다」를 가를 수 없고, 사용자에게는 **빈 흰 창**만 남는다.

### 구현 — 신호를 둘로 세웠다

1. **로드 감시(`connection::LoadWatch`)** — 네비게이션이 «허용된» 시점에 무장하고
   `PageLoadEvent::Finished` 에서 푼다. `LOAD_DEADLINE`(15초) 안에 안 풀리면
   「로드가 끝나지 않았다」가 **관측 가능한 사건**이 된다.
   회차를 세대 번호로 구분해, **늦게 깨어난 감시가 지금 잘 도는 문서를 덮지 않는다**
2. **연결 전수(`connection::probe`)** — 그 시점에 **같은 주소로 직접 붙어 본다.**
   TCP 연결 + (https 면) TLS 악수까지만 간다. **HTTP 요청은 보내지 않는다** — U-2 가 말하는 것은
   연결 계층의 사실이고, 본문을 받아오면 셸이 원격 문서를 읽는 셈이 된다

### 신뢰 판정의 충실도 — 과장하지 않는다

전수는 `native-tls` 를 쓴다. **macOS 는 Security.framework, Windows 는 SChannel** 로 내려가
**웹뷰와 같은 OS 신뢰 저장소**를 본다. 그래서 「웹뷰가 거절할 인증서」를 셸도 같은 기준으로 거절한다.

> ⚠ **그러나 웹뷰 «자신»이 낸 오류를 받아 온 것은 아니다.** 같은 저장소를 쓰는 **별도 연결**의
> 결과다. 이 구분을 코드 주석(`connection.rs` 머리말)과 여기 양쪽에 적는다.

### 사유를 지어내지 않는다 (SPEC U-2)

- 전수가 **실패**하면 그 사유를 U-2 의 「기술 정보」 줄에 **받아 적는다**
- 전수가 **성공**했는데 문서가 안 떴으면 **원인을 모르는 것**이므로 `detail = None` 으로 두고,
  기술 정보 줄이 **아예 나오지 않는다**. 시험 `사유를_모르면_기술_정보_줄이_아예_없다` 가 지킨다

### U-2 화면은 **IPC 를 쓰지 않는다**

셸 자기 화면은 커스텀 스킴(`stronghajin://`)으로 낸다. capability 가 `local:false` 라
**이 화면은 커맨드를 부를 수 없고, 부를 필요도 없다** — `다시 시도` 는 IPC 가 아니라
**평범한 링크**로 운영 주소로 되돌아가고, 네비게이션 허용 목록이 그 이동을 받는다.
시험 `셸_화면은_커맨드를_부르지_않는다` 가 `<script>`·`invoke`·`__TAURI` 부재를 고정한다.

### ⚠ 이 기한은 «점유»의 TTL 이 아니다

WORK I-3 이 금지한 것은 **절전 방지 점유**의 TTL·주기 갱신·참조계수다.
여기 기한은 **문서 로드**에만 걸리고 **점유를 만들지도 풀지도 않는다.**
`connection.rs` 는 `guard.rs`·`power.rs` 를 **한 줄도 건드리지 않는다.**

---

## 5. 수명 정리 경계 — 그대로 지켰다

| 사건 | 처리 | 근거 |
|---|---|---|
| `CloseRequested`(닫기 **요청**) | **아무것도 풀지 않는다** — 로그만 남긴다 | I-4·I-5 · `E-12` · AC-T36 |
| 막힌 네비게이션(`E-05`) | **아무것도 풀지 않는다.** 기본 브라우저로 넘기고 창은 그대로 | L-11 · AC-T37 |
| `Destroyed`(창이 **실제로** 닫힘) | 그 창의 세션 **전부 해제** | L-06 · AC-T15 |
| `PageLoadEvent::Started`(문서 **실제** 교체) | 그 창의 세션 **전부 해제** | L-09 · AC-T16 |
| 프로세스 종료 | `Op::Shutdown` → 전용 스레드가 **반드시 풀고** 나간다 | L-13 · AC-T18 |

- **네이티브 소유 유지**: 웹이 조용하다는 이유로 푸는 경로가 없다(I-1)
- **TTL·주기 갱신·참조계수 없음**: 세션은 **이름의 집합**이지 숫자가 아니다(I-3)
- **`Op::Shutdown` 보존**: 바깥에 `Sender` 사본이 남아도 스레드가 끝난다(Phase 1 교착의 회귀 시험 유지)
- **늦은 경합의 최종 잔존 0**: 같은 이름을 두 번 넣어도 하나라 중복이 쌓이지 않는다.
  16 스레드 동시 획득·해제 시험이 잔존 0 을 확인한다(I-7)

---

## 6. W-4 · W-5 처리

### W-4 (macOS 재무장) — **해소. 실행으로 증명했다**

- **문제**: `if self.id.is_some() { return Engaged }` — id 를 들고 있는 한 OS 에 되묻지 않아
  `E-09` 의 「그 시점에 걸려 있지 않으면 다시 건다」가 macOS 에서 형식만 남았다
- **해결**: **make-before-break** — 재무장 때 **새 assertion 을 먼저 만들고 옛것을 놓는다.**
  「지금 걸려 있음」이 보장되고, 순서를 뒤집지 않아 **재무장 도중에도 보호가 끊기지 않는다**
- **새로 만들지 못하면**: 옛 id 를 **도로 들고** 정리 손잡이를 지키되, 상태는 낙관하지 않고
  `degraded` 로 답한다(방금 OS 호출이 실패했으므로)
- **증거**: `power::macos_tests::재무장이_assertion_을_실제로_다시_만든다` — **진짜 IOKit 을 불러**
  두 번째 engage 뒤 **assertion id 가 바뀌는 것**을 확인한다. 옛 no-op 으로 되돌아가면 붉어진다.
  **이 기기에서 실행됐다(통과).**

### W-5 (Windows 해제) — **구조로 해소. 실행 증거는 없다**

- **문제**: engage 가 0 을 돌려주면 `engaged=false` 가 되고, `disengage` 는
  `if !self.engaged { return Released }` 로 **아무 호출 없이** 빠져나갔다 →
  ①engage 성공 ②재무장 실패 ③해제 의 경로에서 **OS 요구가 스레드 수명 내내 남았다**
- **해결 둘**:
  1. engage 실패해도 **「요구를 건 적이 있다」 표시를 내리지 않는다**
  2. `disengage` 의 **이른 반환을 없앴다** — 상태를 믿지 말고 **언제나** `SetThreadExecutionState(ES_CONTINUOUS)` 를 부른다. 아무것도 서 있지 않을 때 불러도 무해하다
- **증거**: `power::windows_tests::해제는_engage_성패와_무관하게_요구를_지운다` 를 **작성했다.**
  ⚠ **그러나 이 기기에서 실행되지 않았다** — 아래 §7 의 컴파일 차단 때문이다.
  **코드 구조 검토가 전부이고, 실행 증거가 아니라는 사실을 그대로 적는다.**

---

## 7. 실행한 검사와 결과

| # | 명령 | 결과 |
|---|---|---|
| T-1 | `cargo check --all-targets` | **exit 0 · warning 0 · error 0** |
| T-2 | `cargo clippy --all-targets -- -D warnings` | **통과**(경고를 오류로 돌려도 깨끗) |
| T-3 | `cargo test` | **45 passed · 0 failed** (Phase 1 의 21 → 45) |
| T-4 | `cargo check --locked --target x86_64-pc-windows-msvc` | ❌ **실패 — 우리 소스가 아니다** |
| T-5 | `npx tsc --noEmit` (frontend) | **통과**(출력 0줄) |
| T-6 | `make frontend-test` | **exit 0 · 1040 passed (1040)** — 이번 Phase 가 프론트를 건드리지 않았음을 재확인 |

### T-4 의 실패 원문 — Windows 는 **컴파일도 미검증**이다

```text
thread 'main' panicked at …/tauri-winres-0.3.6/src/lib.rs:543:14:
called `Result::unwrap()` on an `Err` value: NotAttempted("llvm-rc")
```

- 우리 코드의 오류가 **아니다.** 호스트에 `llvm-rc`(LLVM 설치본)가 없어 **빌드 스크립트 단계**에서 멈춘다
- 타깃 자체(`x86_64-pc-windows-msvc`)는 설치돼 있다
- 따라서 `#[cfg(windows)]` 코드 — `power::windows`(W-5) 와 `allow_microphone_on_webview2` — 는
  **컴파일 미검증 · 실행 미검증** 두 칸 모두 비어 있다. T-1 의 exit 0 은 **Windows 코드에 대한 증거가 아니다**
- `llvm-rc` 하나면 열린다. **전역 툴체인 설치라 코디 판단 사항**이다

---

## 8. 인수조건 증거 매핑 (15건)

| AC | 무엇 | 증거 위치 | 상태 |
|---|---|---|---|
| **AC-T12** | 같은 세션 두 번 걸어도 늘지 않고 한 번에 풀린다 | `guard::tests::같은_세션을_두_번_걸어도_한_번_풀면_풀린다` | ✅ 시험 통과 |
| **AC-T13** | 지난 녹음의 늦은 해제가 지금 점유를 풀지 못한다 | `guard::tests::지난_녹음의…` · `tests::지난_녹음의_늦은_해제가_지금_도는_점유를_끄지_않는다` | ✅ |
| **AC-T14** | 모르는·이미 푼 세션으로 풀어도 에러가 아니다 | `guard::tests::모르는_세션으로_풀어도_에러가_아니다` | ✅ |
| **AC-T15** | 웹이 못 풀어도 창이 닫히면 풀린다 | `tests::창이_실제로_닫히면_웹이_못_풀어도_풀린다` + `WindowEvent::Destroyed` 배선 | ✅ 시험 · ⚠ 실기 미관측 |
| **AC-T16** | 문서가 통째로 바뀌면 풀린다 | `on_page_load(Started)` → `clear_window("document-replaced(L-09)")` | ⚠ **코드만** — 실기는 Phase 5 |
| **AC-T17** | 앱 내 화면 전환·같은 문서 주소 변경을 교체로 보지 않는다 | 훅이 `Started` 에만 붙어 있음 · `guard` 에 그 경로 없음 | ⚠ **코드만** — 실측 M-3 잔여 |
| **AC-T18** | 프로세스가 끝나면 OS 절전 방지가 남지 않는다 | `power::tests::스레드가_내려갈_때_반드시_푼다` · `바깥에_sender_사본이…` | ✅ 시험 통과 |
| **AC-T20** | 허용 목록 밖으로 창이 가지 않는다 | `on_navigation` 이 `false` 반환 + 기본 브라우저로 넘김 | ⚠ **코드만** — 실기는 Phase 5 |
| **AC-T21** | 외부 링크가 기본 브라우저에서 열린다 | `open_external` → `opener::open_url` · 두 번째 웹뷰 없음 | ⚠ **코드만** |
| **AC-T22** | `http(s)` 아닌 주소는 열리지 않는다 | `guard::tests::외부_링크는_http_와_https_만_받는다` | ✅ |
| **AC-T23** | 커맨드가 넷뿐 · 파일·프로세스·셸 권한 0 | `tests::웹에_여는_커맨드는_정확히_넷이다` + `capabilities/product-shell.json` | ✅ **정적 검증** |
| **AC-T25** | 셸 프레임워크 2.11.1 이상 | `tests::셸_프레임워크_하한이_2_11_1_이상이다` (`Cargo.lock` 실측 파싱) | ✅ |
| **AC-T31** | 연결 실패 시 U-2 가 보이고 `다시 시도` 가 된다 | `connection.rs` + `shell_ui::connection_error` + `shell_ui::tests` 4건 | ⚠ **구현·단위시험 완료 · 실기 미관측** |
| **AC-T33** | 트레이·백그라운드 상주·추가 창이 없다 | `tests::셸_설정이_제품_정체성을_지킨다`(`trayIcon` 부재 · `app.windows` 비어 있음) | ✅ 정적 |
| **AC-T34** | 앱 식별자가 다른 제품과 겹치지 않는다 | 같은 시험 — `app.stronghajin.desktop` · 참조 `com.kknaks.task-management` 부재 | ✅ 정적 |

**AC-T24**(커맨드를 쓸 수 있는 origin 이 하나)는 `tests::커맨드_허용_origin_은_하나이고…` 로
**정적 확인만** 했다. **최종 통과는 운영 origin 판(Phase 8)** 이다 — 지금 값은 자리표시다.

> **미검증 OS 축**: 위 표 전체가 **macOS 기준**이다. **Windows 는 한 칸도 없다**(§7).

---

## 9. 미결 · 주의점

| # | 내용 | 주인 |
|---|---|---|
| **1** | **M-1 은 여전히 미측정.** 이 Phase 에서 닫지 않았다 — CA 신뢰가 반영된 뒤 별도 기록으로 남긴다 | 사용자 → 코디 |
| **2** | **Windows 컴파일 차단**(`llvm-rc`). W-5 시험과 마이크 권한 코드가 미검증으로 남는다 | 코디(전역 툴체인 판단) |
| **3** | **운영 origin 미정**(OQ-T02). capability·`shell.config.json` 두 자리를 Phase 8 이 함께 채운다. **두 곳이 어긋나면 커맨드가 ACL 에서 거절된다** | Phase 8 |
| **4** | `frontend/package.json` 의 `probe:shell` 이 이제 제품 셸을 띄운다 — 이름 정리 필요 | 후속(작은 정리) |
| **5** | Phase 1 fixture(`vite.probe.config.ts`·`probe.html`·`src/dev/`)는 **그대로 남아 있다.** 이번 범위가 `frontend/src/**` 를 금지해 건드리지 않았다 | 코디 판단 |
| **6** | 아이콘은 **여전히 자리표시**다(Phase 1 생성본). 실제 제품 아이콘은 Phase 7 | Phase 7 |
| **7** | `LOAD_DEADLINE` 15초는 **고른 값**이다. 느린 회선에서 정상 로드를 실패로 읽으면 U-2 가 거짓말을 하므로, Phase 5 실측에서 조정 여지를 본다 | Phase 5 |

---

## 10. 발주 금지 사항 준수

| 금지 | 확인 |
|---|---|
| `frontend/src/**` · `App.tsx` · `features/**` · `api.ts` · `microphone.ts` | **0줄** — `find -newermt` 로 이번 Phase 변경 0건 확인 |
| `backend/**` · SPEC/WP/index/log | **0줄** |
| 탐침 손잡이 복사 | 시험 `제품_셸에_탐침_손잡이가_없다` 가 환경 손잡이·계측 페이지·거울·fixture origin 부재를 전수로 고정 |
| 운영 주소·서명 신원 발명 | 운영 origin `null` + `.invalid` 자리표시. **서명·공증 설정 0건** |
| 커밋 · push · PR · Release · 운영 배포 | 하지 않았다. HEAD `a1f6791` 그대로 |
