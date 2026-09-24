# WORK-006 Phase 7 검수 보정 — WARN 3건

- **작성**: 2026-09-22 **23:33 KST**
- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **결과**: WARN 3건 반영. **설치·빌드·Release·태그·push 없음**

---

## 1. 한 줄 결론

「문제 0건」이 「빌드 가능」으로 읽히던 자리를 **strict 모드**로 막았고, 판 번호를 `Cargo.toml`
단일 출처로 둔 선택이 **Tauri 상류의 권고와 반대 방향**이라는 사실을 근거와 함께 보고서에 적었다.
작성 시각 자리표시(`23:2x`)를 실제 값으로 바꿨다.

---

## 2. 변경 파일

| 파일 | 변경 |
|---|---|
| `frontend/scripts/verify-shell-build.mjs` | strict 모드(`--strict` · `SHELL_STRICT=1`) · 못 재는 것의 **건수 출력**(최종 재검수에서 **구성 미비 / 호스트 한계**로 분리 — fix2 참조) |
| `Makefile` | `shell-verify` 에 `SHELL_STRICT` 전달 · `shell-verify-strict` 타깃 신설 · `.PHONY` |
| `tauri-p7-build-report.md` | §3 상류 권고(W-2) · §4·§6 strict(W-1) · 작성 시각(W-3) |
| `tauri-p7-build-fix-report.md` | **신규** — 이 문서 |

**건드리지 않은 것**: `tauri.conf.json` · `src-tauri/src/**` · `Cargo.toml` · `shell.config.json` ·
capability · 제품 프론트 · backend · 인프라 레포.

---

## 3. W-1 — 「문제 0건 = 빌드 가능」 오독을 막았다

### 무엇이 문제였나

기본 실행이 끝에 **「문제 0건」**만 찍어서, 이 스크립트가 **못 재는 것**(`.icns` 부재가 실제
번들을 막는지 · 다른 플랫폼 번들)까지 통과한 것처럼 읽혔다.

### 고친 것 — 관측이 아니라 **판정**을 가르는 모드

| 모드 | 구성 미비 | 호스트 한계 | 종료 코드 |
|---|---|---|---|
| 기본 `make shell-verify` | 경고(⚠) | 정보(ℹ) | **0** |
| `make shell-verify-strict`<br>`SHELL_STRICT=1 make shell-verify`<br>`node … --strict` | **실패로 승격**(✗) | 정보(ℹ) | **≠ 0** |

**두 모드가 같은 것을 재고 항목의 내용도 같다.** 다른 것은 「그것을 통과로 볼 것인가」뿐이다 —
**관측을 바꾸지 않는다.**

> ⚠ **이 표는 최종 재검수(F-1)에서 한 번 더 갈렸다.** 처음에는 못 재는 것을 **한 바구니**로 묶어
> strict 가 «호스트 한계»까지 실패로 올렸는데, 그러면 이 기기에서는 **strict 가 영원히 붉어** 경보로서
> 죽는다. 지금은 **구성 미비**(채우면 사라진다)와 **호스트 한계**(기기의 성질)를 갈라,
> strict 는 **앞의 것만** 승격한다. 상세와 증명은 `tauri-p7-build-fix2-report.md`.

### 유지한 것

**기존 검증 일곱은 그대로다** — 판 번호 단일 출처 · 코드 태그 대조 · **양 플랫폼 번들 타깃** ·
아이콘 실재/형식 · 원격 문서 계약(`shell-noop`) · **권한 경계**(`local:false` · `remote.urls` 하나 ·
와일드카드 없음 · 권한 넷) · 식별자 충돌. **운영 주소도 아이콘도 만들지 않았다.**

---

## 4. W-2 — 상류 권고를 숨기지 않고 적었다

`tauri-p7-build-report.md` §3 에 절을 더했다. 근거는 **`@tauri-apps/cli` 가 싣는 공식 설정 스키마**다:

> App version. … If removed the version number from `Cargo.toml` is used.
> **It's recommended to manage the app versioning in the Tauri config.**
> — `frontend/node_modules/@tauri-apps/cli/config.schema.json` · `properties.version.description`

**즉 상류의 권고는 「`tauri.conf.json` 에서 관리하라」이고, 이번 선택은 그 반대 방향이다.**
보고서에 그 사실과 함께 **이번 회차가 그렇게 고른 이유 둘**을 적었다:

1. **허용 경로** — `src-tauri/Cargo.toml` 이 이번 허용 파일에 없다. 상류 권고대로 가려면
   `tauri.conf.json` 값을 살리고 `Cargo.toml` 을 거기 맞춰야 하는데, 그 파일을 고칠 수 없다
2. **값 선택 미결** — `0.1.0` 과 `0.0.1` 중 어느 것이 맞는 판인지 정해진 바가 없다.
   한쪽을 고르는 것은 **판 번호 정책 결정**이라 이 Phase 의 일이 아니다

→ 그래서 **값을 고르지 않고 출처를 하나로** 만들었고, **Phase 8 이 판 번호 정책을 다시 본다**
(첫 배포판 번호 · 상류 권고대로 되돌릴지 · 코드 태그와 묶는 방식). **되돌리는 비용은 한 줄**임을 적었다.

> ⚠ **정정 — 내가 틀리게 적었다.** 이 보고서의 앞선 판은 「`config.rs` 의 주석에는 recommended
> 문장이 **없다**」고 썼다. **사실이 아니다.** 그 문장은 `config.rs` 에 **있다**:
>
> ```rust
> // tauri-utils-2.9.3/src/config.rs:3610-3613
> /// App version. It is a semver version number or a path to a `package.json` file containing the `version` field.
> ///
> /// If removed the version number from `Cargo.toml` is used.
> /// It's recommended to manage the app versioning in the Tauri config.   // ← 3613
> ```
>
> 일어난 일은 **인용 범위를 3612 에서 끊어 3613 한 줄을 빠뜨린 것**이다. 놓친 줄이 바로 권고 문장이라,
> 「주석에 없다」는 **잘못된 결론**까지 갔다. 지금은 **같은 문장을 JSON 스키마에서 인용**하도록
> 정정해 두었고(§4), `config.rs` 에도 같은 문장이 있다는 사실을 여기 적는다.
> **두 출처가 어긋난 적이 없다 — 내가 한쪽을 덜 읽었을 뿐이다.**

---

## 5. W-3 — 작성 시각

`- **작성**: 2026-09-22 23:2x KST` → **`2026-09-22 23:26 KST`**(실제 값, `TZ=Asia/Seoul date` 로 확인).
보정 회차 줄도 함께 더했다(`23:30 KST`).

---

## 6. 재실행한 검증

| # | 명령 | 결과 |
|---|---|---|
| F-1 | `make shell-verify` | **exit 0** · 문제 0건 · **구성 미비 1건(경고)** · **호스트 한계 1건(정보)** |
| F-2 | `make shell-verify SHELL_STRICT=1` | **exit≠0** — **구성 미비 1건만 승격** · **호스트 한계 1건은 정보** |
| F-3 | `make shell-verify-strict` | **exit≠0** — 위와 같다 |
| F-4 | `make shell-verify SHELL_TAG=v0.0.1` | 태그 대조 통과(기존 기능 유지) |
| F-4b | **`SHELL_TAG=v0.0.1 SHELL_STRICT=1 make shell-verify`** | 태그 대조 통과 + **구성 미비 1건을 실패로 승격** → exit≠0. **발행 직전 관문**으로 쓰는 조합이다 — 「**이 판 번호로, 구성이 갖춰진 채**」를 한 번에 본다 |
| F-5 | `make shell-verify SHELL_TAG=v9.9.9` | **exit≠0** — 불일치를 여전히 잡는다 |
| F-6 | `make shell-build-fixture SHELL_FIXTURE_ORIGIN=https://fixture.example.invalid` | **거부 + 안내** · **굽지 않았다** |
| F-7 | `cargo check --all-targets` | **warning 0 · error 0** |
| F-8 | `cargo test` (`src-tauri`) | **45 passed · 0 failed** |
| F-9 | `cargo clippy --all-targets -- -D warnings` | **통과** |
| F-10 | `npx tsc --noEmit` | **통과**(출력 0줄) |
| F-11 | `make frontend-test` | 1회차 `1 failed / 1052` → **재실행 exit 0 · 1053 passed** (§6-1) |

### 6-1. F-11 의 1회 실패는 **기준선 불안정**이다

- 실패 파일: `src/features/work/CreateWork.test.tsx` — **이번 변경과 접점이 없다**
- 이번 회차에 `frontend/src` 를 **한 줄도 건드리지 않았다**(`find -newermt` 확인).
  바꾼 것은 `frontend/scripts/` · `Makefile` · 문서뿐이다
- 앞선 회차들에서 **기준선(변경을 되돌린 트리)도 4회 중 2회 실패**로 측정해 둔, 파일이 매번 다른
  스위트 전반의 시간 의존 불안정과 같은 형태다
- 재실행에서 **1053 전건 통과** — 기준선 대비 **새 실패 0**

---

## 7. 미측정 / 미결 — 그대로다

| 항목 | 상태 |
|---|---|
| **M-10**(재설치·판 올림 쿠키 유지, AC-T35) | **미측정** — 사람이 설치해야 한다. **정적 검증·strict 통과를 실기 통과로 쓰지 않는다** |
| **Windows 축 전부** | **검증 불가(이 기기)** — 실기 없음 + 교차 컴파일 `llvm-rc` 부재. macOS 결과로 대체하지 않는다 |
| **D-4**(PRODUCTION 로그인 수단) | **미결 유지** — 이번 작업이 건드리지 않았다 |
| 실제 설치파일 생성 | **하지 않음** |
| 운영 origin · 도메인 · 서명 · 공증 · CI · 최소 OS 버전 | **미정 · 발명 0** |
| macOS `.icns` 아이콘 | **없음** — strict 에서 실패로 잡힌다. 제품 아이콘 자체가 자리표시라 만들지 않았다 |
| 판 번호 정책 | **Phase 8 재검토**(§4) |

---

## 8. 금지 사항 준수

| 금지 | 확인 |
|---|---|
| 실제 설치 · 빌드 | **하지 않았다.** fixture 스크립트는 기본 dry-run이고 이번에도 `--run` 을 주지 않았다 |
| Release · 태그 · push · 커밋 | 하지 않았다. HEAD `a1f6791` 그대로 |
| 운영 주소 · 아이콘 발명 | **0** — placeholder 그대로, `.icns` 도 만들지 않고 경고/실패로만 드러낸다 |
| 허용 파일 외 변경 | 없다 — 스크립트 1 · Makefile · 보고서 2 |
