# WORK-006 Phase 7 최종 보정 — 독립 재검수

- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **검수 대상**: `tauri-p7-build-report.md`(보정판) · `tauri-p7-build-fix-report.md`
- **코드·설정·문서 수정 0줄. 이 검수 보고서 한 파일만 작성.**
- **실측·설치·배포 없음.** 돌린 것은 **읽기 전용 검증기**뿐이다(그 자체가 검수 대상).

---

## 0. 종합 판정 — **FAIL 1 · WARN 2 · 나머지 PASS**

**코드 쪽 보정은 전부 옳다.** strict 모드가 세 경로(`--strict` · `SHELL_STRICT=1` ·
`make shell-verify-strict`)로 모두 동작하고, **관측이 아니라 판정만** 바꾸며(`failed =
problems + (strict ? unverifiable : 0)`), 기본 모드는 검증 불가 **건수**와
**「문제 0건 ≠ 빌드 가능」**을 명시한다. 기존 7검증·fixture dry-run·M-10/Windows/D-4 표기도
그대로다.

**FAIL 은 문서 한 자리다** — `tauri-p7-build-fix-report.md` §4 가 「직전 인용(`config.rs`)의
주석에는 **「recommended」 문장이 없다**」고 적었는데, **그 문장은 `config.rs:3613` 에 있다.**
직전 인용이 `3610-3612` 로 **한 줄 앞에서 끊겼을 뿐**이다. 결론(권고를 기록하고 스키마를 인용)은
옳지만, **근거 서술이 사실과 다르다.**

---

## 1. 판정표

| # | 검수 항목 | 판정 |
|---|---|---|
| 1 | 기본 `make shell-verify` 가 **검증 불가 수** + 「문제 0건 ≠ 빌드 가능」 명시 | **PASS** |
| 2 | `--strict` · `SHELL_STRICT=1` · `make shell-verify-strict` 가 승격 · 기본 7검증과 분리 | **PASS** (실효성은 W-1) |
| 3 | 상류 version 권고 출처가 **실제 schema 좌표**로 정정 · Cargo.toml 선택 이유 · Phase 8 재검토 기록 | **PASS**(보고서 §3) · **FAIL**(fix 보고서 §4 의 근거 서술) |
| 4 | 문서 시각이 실제 시각 | **PASS** |
| 5 | 양 플랫폼 · fixture dry-run · 원격 origin/권한 검증 · M-10/Windows/D-4 표기 유지 | **PASS** |
| 6 | 허용 밖 변경 · Release · 태그 · push 없음 | **PASS** |

---

## 2. FAIL

### F-1 — fix 보고서 §4 의 「`config.rs` 주석에 recommended 문장이 없다」가 **사실과 다르다**

**위치**: `tauri-p7-build-fix-report.md` §4 마지막 인용 블록

> ⚠ **직전 보고서의 인용이 부분적이었다.** Phase 7 보고서는 `tauri-utils-2.9.3/src/config.rs:3610-3612`
> 의 Rust 문서 주석을 인용했는데, **그 주석에는 「recommended」 문장이 없다.**

**실제**(검수가 원본을 열어 확인):

```text
/Users/kknaks/.cargo/registry/src/index.crates.io-…/tauri-utils-2.9.3/src/config.rs
3610:  /// App version. It is a semver version number or a path to a `package.json` file …
3611:  ///
3612:  /// If removed the version number from `Cargo.toml` is used.
3613:  /// It's recommended to manage the app versioning in the Tauri config.
```

- **`config.rs:3613` 에 그 문장이 있다.** Rust 주석과 JSON 스키마의 설명은 **같은 문장**이다
  (스키마가 그 주석에서 생성되기 때문이다).
- 직전 Phase 7 보고서의 인용 범위 `3610-3612` 는 **바로 그 다음 줄에서 끊긴 것**이지,
  「없는 곳을 인용한 것」이 아니다.

**영향**
- **결론과 조치는 옳다** — 권고가 Phase 7 보고서 §3 에 기록됐고, 새 인용
  (`config.schema.json` · `properties.version.description`)을 검수가 직접 파싱해
  **두 문장이 모두 들어 있음을 확인**했다. 새 좌표는 **정확하다.**
- 문제는 **왜 출처를 바꿨는가에 대한 서술**이 틀렸다는 것이다. 이 문서들은 감사 기록이므로,
  상류 소스에 대한 사실 주장이 틀린 채 남으면 안 된다.
- **Phase 7 보고서 §3 에는 이 잘못된 주장이 없다**(거기서는 스키마만 인용한다) — **오류는
  fix 보고서 한 곳에 갇혀 있다.**

**수정 방향** — §4 의 한 문장을 사실대로 바꾼다:

> 「그 주석에는 recommended 문장이 없다」
> → 「**직전 인용이 `3612` 에서 끊겨, 바로 다음 줄(`3613`)의 권고 문장이 빠졌다.** 같은 문장이
>    JSON 스키마에도 실려 있어, 인용을 스키마 쪽으로 옮겨 적었다」

---

## 3. WARN

| # | 내용 | 근거 | 수정 방향 |
|---|---|---|---|
| **W-1** | **`shell-verify-strict` 는 어떤 호스트에서도 초록이 될 수 없다.** 「이 호스트에서 구울 수 있는 것 / 없는 것」 줄이 **무조건** `unverifiable` 로 들어가므로(`verify-shell-build.mjs:183-186`) `unverifiable.length ≥ 1` 이 항상 참이고, strict 는 **언제나 실패**한다. 그 증거로 `:216` 의 `"strict 통과 — 검증 불가 항목도 0건이다"` 분기는 **도달할 수 없는 죽은 코드**다. 보고서가 strict 를 「굽기 직전의 관문」으로 제안했는데, **항상 붉은 관문은 관문이 아니다**(곧 무시된다) | `verify-shell-build.mjs:183-186` · `:202` · `:215-217` · 재현: `make shell-verify-strict` → exit 2, 실패 2건(그중 하나가 호스트 줄) | 검증 불가를 **두 갈래로** 나눈다 — ① **고칠 수 있는 것**(`.icns` 부재 등) → strict 에서 실패 ② **호스트 사실**(다른 플랫폼은 여기서 못 굽는다) → strict 에서도 **정보**로 남긴다. 그러면 macOS 에서 `.icns` 를 채우면 strict 가 실제로 초록이 되고, 관문이 의미를 갖는다 |
| **W-2** | **`--strict` 와 `SHELL_TAG` 의 조합이 문서에 없다.** 굽기 직전 관문이라면 태그 대조까지 함께 거는 것이 자연스러운데(`make shell-verify SHELL_TAG=v0.0.1 SHELL_STRICT=1`), Makefile 은 지원하지만(두 인자 독립 전달) 두 보고서 어디에도 그 조합 예시가 없다 | `Makefile` `shell-verify` 레시피 | 보고서 명령 블록에 조합 한 줄 추가 |

---

## 4. PASS — 직접 확인한 것

### 4-1. 기본 모드의 한계 표기 (PASS)

`make shell-verify` **실제 출력**(재현):

```text
-- 검증 불가 / 남는 것: 2건 --
  ⚠ macOS `.icns` 아이콘이 목록에 없다 — …
  ⚠ 이 호스트(darwin)에서 구울 수 있는 것: macOS(app·dmg). Windows(msi·nsis) 는 **이 기기에서 검증 불가** …

문제 0건 · 검증 불가 2건
⚠ **「문제 0건」은 「빌드 가능」이 아니다.** 위 검증 불가 2건은 이 스크립트가 재지 못한 것이고,
  그중 하나라도 실제 번들을 막을 수 있다. 굽기 전에 확인하려면 --strict 로 돌린다.
(설치파일을 굽지 않았고, 아무것도 설치하지 않았다)
```

- **건수(2건)가 표제와 요약 줄 양쪽에** 찍힌다 · **한계 문장이 마지막에** 선다 → 직전 W-1 이 닫혔다.
- exit **0** — 기본 모드의 성격(경고)이 유지된다.

### 4-2. strict 세 경로 · 승격 · 분리 (PASS)

| 진입점 | 재현 결과 |
|---|---|
| `make shell-verify-strict` | **exit 2** · `strict 모드 — 검증 불가 항목을 실패로 올렸다` · `실패 2건` |
| `make shell-verify SHELL_STRICT=1` | **exit 2** · 같은 출력 |
| `node scripts/verify-shell-build.mjs --strict` | **exit 1**(make 를 거치지 않은 원 코드) · 같은 출력 |

- **Makefile 이 두 인자를 독립으로 전달**한다:
  `node scripts/verify-shell-build.mjs $(if $(SHELL_TAG),--tag …,) $(if $(SHELL_STRICT),--strict,)`
  이고 `shell-verify-strict: $(MAKE) shell-verify SHELL_STRICT=1` — **중복 구현이 없다.**
- **관측을 바꾸지 않는다**: `const failed = problems.length + (strict ? unverifiable.length : 0)`(`:202`).
  검사 로직은 한 벌이고 **판정 기준만** 갈린다. 글리프도 `⚠`/`✗` 만 바뀐다(`:194`).
- **기본 7검증과 분리**: `fail(...)` 호출 **26곳**이 그대로 살아 있고 strict 와 무관하다.
  `SHELL_TAG=v9.9.9` 같은 **진짜 문제는 기본 모드에서도 여전히 붉어진다**(직전 회차 재현 확인).

### 4-3. 상류 권고 좌표 (PASS — 새 좌표는 정확하다)

검수가 스키마를 직접 파싱했다:

```
node -e "…config.schema.json…properties.version.description"
→ "App version. … If removed the version number from `Cargo.toml` is used.
   It's recommended to manage the app versioning in the Tauri config. …"
```

- **두 문장이 모두 그 자리에 있다.** `frontend/node_modules/@tauri-apps/cli/config.schema.json ·
  properties.version.description` 이라는 좌표는 **정확하다.**
- Phase 7 보고서 §3 이 「**상류의 권고는 반대 방향**이고, 그럼에도 이렇게 고른 이유는 ①허용 경로에
  `Cargo.toml` 이 없다 ②어느 값이 맞는 판인지 미결」 둘을 적고, **「Phase 8 이 판 번호 정책을
  다시 본다(첫 배포판 번호 · 상류 권고로 되돌릴지 · 코드 태그와 묶는 방식) · 되돌리는 비용은
  한 줄」**까지 기록했다 → **요구한 세 가지가 모두 들어갔다.**
- ⚠ 다만 **왜 출처를 바꿨는가의 서술**만 틀렸다 → F-1.

### 4-4. 문서 시각 (PASS)

| 문서 | 시각 |
|---|---|
| `tauri-p7-build-report.md` | 작성 **23:26 KST** · 검수 보정 **23:30 KST** — `23:2x` 자리표시가 사라졌다 |
| `tauri-p7-build-fix-report.md` | 작성 **23:33 KST** |

세 값이 **회차 순서와 일관**된다(작성 → 보정 → 보정 보고).

### 4-5. 기존 검증·미측정 표기 유지 (PASS)

| 항목 | 확인 |
|---|---|
| **양 플랫폼 번들 타깃** | 기본 출력에 `bundle.targets = "all" — macOS(app·dmg) · Windows(msi·nsis) 를 모두 포함한다` 그대로 |
| **fixture dry-run** | `build-shell-fixture.mjs` 는 **이번 회차에 열리지도 않았다**(mtime 0건). 직전 검수에서 확인한 동작(인자 없이 exit 2 · 두 주소 불일치 시 굽지 않고 중단 · `http` 거부 · `--run` 없으면 `cargo tauri build` 미호출)이 **그대로 유효**하다 |
| **원격 origin · 권한 경계** | 기본 출력이 `product-shell.json: 운영 origin 이 아직 자리표시다(…invalid/*)` 를 계속 낸다. capability 검사(`local:false` · `remote.urls` 하나 · 와일드카드 없음 · 권한 넷)도 코드에 그대로 |
| **M-10** | fix 보고서 §7 「**미측정** — 사람이 설치해야 한다. **정적 검증·strict 통과를 실기 통과로 쓰지 않는다**」 |
| **Windows** | 「**검증 불가(이 기기)** — macOS 결과로 대체하지 않는다」 · 스크립트 출력도 매번 같은 말 |
| **D-4** | 「**미결 유지** — 이번 작업이 건드리지 않았다」 |
| `.icns` | 「없음 — strict 에서 실패로 잡힌다. **만들지 않았다**」 |

### 4-6. 허용 범위 (PASS)

**이번 보정 회차에 바뀐 파일은 넷**(`find -newermt "23:26"` · `git status` 대조):

```
Makefile                                   (수정 — SHELL_STRICT 전달 · shell-verify-strict · .PHONY)
frontend/scripts/verify-shell-build.mjs    (수정 — strict 모드 · 건수 출력)
tauri-p7-build-report.md                   (문서 — §3 · §4 · §6 · 시각)
tauri-p7-build-fix-report.md               (문서 — 신규)
```

| 금지 | 확인 |
|---|---|
| `tauri.conf.json` · `src-tauri/src/**` · `Cargo.toml` · `shell.config.json` · capability | **열리지 않았다**(mtime 0건) |
| `build-shell-fixture.mjs` · 제품 프론트 · backend · 인프라 레포 | **무변경** |
| **태그** | `git tag --points-at HEAD` → **없음**. HEAD `a1f6791` 그대로 |
| **CI** | `.github/workflows` **존재하지 않음** |
| Release · push · 커밋 · 설치 · 빌드 | **없음** — 이번 검수도 읽기 전용 검증기만 돌렸다 |

> **방법 주석**: `cargo check/test/clippy` · `tsc` · `make frontend-test` 는 **다시 돌리지 않았다.**
> 발주가 실측을 금했고, 이번 회차가 **컴파일·타입·프론트에 닿는 파일을 한 줄도 바꾸지 않았다**
> (바뀐 것은 Node 스크립트 · Makefile · 문서). 직전 검수에서 재현한 값(45 passed · tsc 0줄 ·
> 1053 passed)이 **그대로 유효**하다.
> fix 보고서 §6-1 의 `frontend-test` 1회 실패도 같은 이유로 **이번 변경과 무관**하고,
> 「기준선 불안정」이라는 판단이 **앞선 회차들의 측정과 일관**된다.

---

## 5. 차단·미결 (이번 회차가 만든 것 아님 — 유지)

| # | 항목 | 주인 |
|---|---|---|
| 1 | **D-4** — PRODUCTION 세션 발급 수단 부재. **운영 배포를 「사용 가능」으로 판정할 수 없다** | 코디·사용자(OQ-W05) |
| 2 | **fixture origin 확정**(두 파일 같은 값) | 사용자·코디(OQ-T02) |
| 3 | **판 번호 정책 · 상류 권고로 되돌릴지** | Phase 8 |
| 4 | **제품 아이콘 세트(`.icns` 포함)** | Phase 7 후속/8 |
| 5 | **M-10 실기 · Windows 실기/빌드 환경** | 사용자 · OQ-W01 |

---

## 6. 한 줄 정리

**strict 보정은 설계·구현·문서 모두 옳게 들어갔고**(세 진입점 · 판정만 변경 · 기본 7검증 분리 ·
한계 문장), 상류 권고와 Phase 8 재검토도 기록됐다. 남은 것은 **fix 보고서 §4 의 사실 오류 한 문장
(F-1)** 과, **strict 가 호스트 사실 때문에 영원히 붉어 관문 구실을 못 한다는 것(W-1)** 이다.
둘 다 고치는 비용이 작고, 둘을 고치면 Phase 7 쪽에 남는 지적이 없다.
