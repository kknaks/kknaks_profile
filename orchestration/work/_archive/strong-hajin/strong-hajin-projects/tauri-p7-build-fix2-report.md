# WORK-006 Phase 7 최종 보정 — F-1 · W-1 · W-2

- **작성**: 2026-09-22 **23:44 KST**
- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **결과**: 3건 반영. **설치 · Release · 태그 · push 없음**

---

## 1. 한 줄 결론

strict 가 **영원히 붉을 수밖에 없던 구조**를 고쳤다 — 못 재는 것을 **구성 미비**(채우면 사라진다)와
**호스트 한계**(기기의 성질)로 갈라, strict 는 앞의 것만 승격한다. 그리고 **내가 틀리게 적은
문장 하나**(「`config.rs` 에 recommended 가 없다」)를 사실대로 정정했다 — 그 문장은 **3613 줄에 있고**,
내 인용이 3612 에서 끊겼을 뿐이다.

---

## 2. 변경 파일

| 파일 | 변경 |
|---|---|
| `frontend/scripts/verify-shell-build.mjs` | `unverifiable` / `hostNotes` **분리** · strict 승격 범위 축소 · **`.icns` 매직바이트 인식**(§3-2) |
| `Makefile` | 두 종류 구분 설명 · **태그+strict 조합** 안내 |
| `tauri-p7-build-report.md` | strict 설명을 두 종류로 · **조합 예시 한 줄**과 목적 |
| `tauri-p7-build-fix-report.md` | **F-1 정정**(§3) · §2·§3 정합 · 조합 예시 행(F-4b) |
| `tauri-p7-build-fix2-report.md` | **신규** — 이 문서 |

**건드리지 않은 것**: `tauri.conf.json` · `src-tauri/src/**` · `Cargo.toml` · `shell.config.json` ·
capability · `frontend/src/**` · backend · 인프라 레포.

---

## 3. W-1 — strict 가 «고칠 수 있는 것»만 막는다

### 3-1. 무엇이 문제였나

처음 판은 못 재는 것을 **한 바구니**(`unverifiable`)에 담고 strict 가 그것을 통째로 실패로 올렸다.
그 바구니에는 성질이 다른 둘이 섞여 있었다:

| 종류 | 예 | 고칠 수 있나 |
|---|---|---|
| **구성 미비** | `.icns` 부재 | **있다** — 파일을 채우면 사라진다 |
| **호스트 한계** | 이 기기가 Windows 번들을 못 굽는다 | **없다** — 기기의 성질이다 |

둘을 섞으면 **이 기기에서 strict 는 무엇을 해도 붉다.** 경보가 늘 울리면 아무도 보지 않는다.

### 3-2. 고친 것

- 배열을 둘로 갈랐다 — `unverifiable`(구성 미비) · `hostNotes`(호스트 한계)
- **strict 는 `unverifiable` 만** 실패로 올린다. `hostNotes` 는 **어느 모드에서도 정보(ℹ)**
- 기본 출력이 **두 건수를 각각** 찍는다:
  `문제 0건 · 구성 미비 1건 · 호스트 한계 1건`
- **덤으로 찾은 것**: 아이콘 형식 검사가 PNG·ICO 만 알아서, **실제 `.icns` 를 넣으면 「형식이
  맞지 않는다」로 잡혔다.** 그대로 두면 `.icns` 를 채워도 strict 가 통과할 수 없다 —
  `.icns` 매직바이트(`icns`)를 인식하게 고쳤다(§3-3 이 이것을 실측으로 잡았다)

### 3-3. **「채우면 초록이 된다」를 증명했다** — 저장소에 아이콘을 만들지 않고

요구가 「macOS 에서 `.icns` 를 채우면 strict 가 실제로 초록이 될 수 있어야 한다」였으므로,
**주장하지 않고 재 보았다.** 저장소를 더럽히지 않으려고 `/tmp` 에 **사본**을 만들어 거기서만 채웠다.

| 단계 | 결과 |
|---|---|
| 사본(지금 상태, `.icns` 없음) `--strict` | **exit 1** |
| 사본에 최소 `.icns` 생성 + conf 목록에 추가 → `--strict` | **처음엔 exit≠0** — 「아이콘 형식이 맞지 않는다」 ← **검사기의 구멍을 여기서 찾았다** |
| `.icns` 매직 인식 추가 후 사본 `--strict` | **exit 0 · strict 통과** |

```text
문제 0건 · 구성 미비 0건 · 호스트 한계 1건
strict 통과 — 구성 미비 0건이다.
ℹ 호스트 한계는 남아 있다(위 ℹ 줄). **이 기기에서 못 구운 플랫폼을 «검증됐다»고 쓰지 않는다**
```

- **사본은 지운다.** 저장소 `src-tauri/icons/` 에는 `.icns` 가 **없다**(확인함) — 제품 아이콘은
  여전히 자리표시이고, **아이콘을 발명하지 않는다**는 금지를 지켰다
- 저장소 현재 상태: 기본 **exit 0** · strict **exit 1**(구성 미비 1건 = `.icns`)

### 3-4. 유지한 것

**기존 7개 검증 그대로** — 판 번호 단일 출처 · 태그 대조 · 양 플랫폼 번들 타깃 · 아이콘 실재/형식 ·
원격 문서 계약 · 권한 경계 · 식별자. **플랫폼 대체 금지 문구도 그대로다** — strict 통과 메시지에
「**이 기기에서 못 구운 플랫폼을 «검증됐다»고 쓰지 않는다**」를 함께 찍어, strict 초록이
「모든 플랫폼이 구워진다」로 읽히지 않게 했다.

---

## 4. F-1 — 내가 틀리게 적은 문장을 정정했다

### 무엇이 틀렸나

직전 보정 보고서에 이렇게 썼다:

> 「`config.rs` 의 주석에는 **「recommended」 문장이 없다**」

**사실이 아니다.** 그 문장은 `config.rs` 에 **있다**:

```rust
// tauri-utils-2.9.3/src/config.rs:3610-3613
/// App version. It is a semver version number or a path to a `package.json` file containing the `version` field.
///
/// If removed the version number from `Cargo.toml` is used.
/// It's recommended to manage the app versioning in the Tauri config.   // ← 3613
```

### 무슨 일이 일어났나

Phase 7 보고서에서 **인용 범위를 `3610-3612` 로 적었고, 권고 문장이 바로 그 다음 줄(3613)이었다.**
한 줄 짧게 읽은 것이다. 그 뒤 스키마에서 같은 문장을 발견했을 때, **「스키마에는 있고 주석에는 없다」**는
잘못된 결론으로 갔다 — 실제로는 **두 출처가 처음부터 같은 말을 하고 있었다.**

### 어떻게 고쳤나

`tauri-p7-build-fix-report.md` §4 의 해당 각주를 **위 사실 그대로** 다시 썼다 —
「없다」가 아니라 **「인용 범위가 3612 에서 끊겨 3613 을 빠뜨렸고, 같은 문장을 스키마에서
인용하도록 정정했다」**로. **두 출처가 어긋난 적이 없다는 것**도 함께 적었다.

> 이 정정은 **결론을 바꾸지 않는다.** 상류 권고가 「`tauri.conf.json` 에서 관리하라」라는 것도,
> 이번 Phase 가 허용 경로·값 미결 때문에 반대 방향을 택했다는 것도 그대로다. 바뀐 것은
> **내가 근거를 잘못 서술했던 한 문장**이다.

---

## 5. W-2 — 태그 + strict 조합

두 보고서의 검증 예시에 한 줄을 더했다:

```bash
SHELL_TAG=v0.0.1 SHELL_STRICT=1 make shell-verify
```

**왜 함께 거나** — 발행 직전에 확인할 것이 **둘**이기 때문이다:

| 무엇 | 누가 답하나 |
|---|---|
| **이 판 번호가 맞는가** | 태그 ↔ `Cargo.toml` ↔ `shell_info.app_version` 대조 |
| **구성이 갖춰졌는가** | 아이콘 · 번들 타깃 · 원격 문서 계약 · 권한 경계 |

따로 돌리면 **한쪽만 보고 넘어가기 쉽다.** 그래서 **발행 관문에서는 이 조합**을 쓴다고 적었다.
`Makefile` 주석에도 같은 목적을 남겼다.

---

## 6. 실행한 검증

| # | 명령 | exit | 비고 |
|---|---|---|---|
| G-1 | `make shell-verify` | **0** | 문제 0 · 구성 미비 1 · 호스트 한계 1 |
| G-2 | `make shell-verify SHELL_STRICT=1` | **≠0** | 구성 미비만 승격 |
| G-3 | `make shell-verify-strict` | **≠0** | 위와 같다 |
| G-4 | `make shell-verify SHELL_TAG=v0.0.1` | **0** | 태그 대조 통과 |
| G-5 | **`make shell-verify SHELL_TAG=v0.0.1 SHELL_STRICT=1`** | **≠0** | 태그 통과 + 구성 미비 승격 — **조합 동작 확인** |
| G-6 | `make shell-verify SHELL_TAG=v9.9.9` | **≠0** | 태그 불일치를 여전히 잡는다 |
| G-7 | `make shell-build-fixture SHELL_FIXTURE_ORIGIN=…invalid` | **≠0** | 거부 + 안내 · **굽지 않았다** |
| G-8 | 사본 실험(§3-3) | **0** | **`.icns` 를 채우면 strict 초록** — 증명 |
| G-9 | `cargo check --all-targets` | — | **warning 0 · error 0** |
| G-10 | `cargo test` (`src-tauri`) | — | **45 passed · 0 failed** |
| G-11 | `cargo clippy --all-targets -- -D warnings` | — | **통과** |
| G-12 | `npx tsc --noEmit` | — | **통과**(출력 0줄) |
| G-13 | `make frontend-test` × 3 | **≠0** | §6-1 — **이번 변경과 무관** |

### 6-1. ⚠ 프론트 스위트가 이번에는 3회 모두 실패했다 — 그래도 내 변경이 아니다

| 회차 | 결과 | 실패 파일 |
|---|---|---|
| 1 | `1 failed / 1052` | `Checklist.test.tsx` |
| 2 | `2 failed / 1051` | `MeetingList.test.tsx` · `Checklist.test.tsx` |
| 3 | `1 failed / 1052` | `MeetingList.test.tsx` |

**내 변경이 이 스위트에 닿을 수 없다는 근거 셋** —

1. 이번 회차가 바꾼 파일은 **`Makefile` 과 `frontend/scripts/verify-shell-build.mjs` 둘뿐**이다
   (`find -newermt` 전수). **`frontend/src` 는 한 줄도 건드리지 않았다**
2. `npm test` 는 **`vitest run`** 이고, `Makefile` 은 그것을 부르기만 한다 — 테스트 대상이 아니다
3. `grep -rl "verify-shell-build\|build-shell-fixture" src/` → **참조 0건**. 테스트가 이 스크립트를
   불러오지 않는다

**실패 파일이 매번 다르고**(Checklist · MeetingList), 앞선 회차들에서 **기준선(변경을 되돌린 트리)도
4회 중 2회 실패**로 측정해 둔 것과 같은 형태다.

> **다만 빈도가 전보다 높다** — 직전 회차는 2회 중 1회였는데 이번은 **3회 중 3회**다.
> 같은 기기에서 `cargo`·`clippy`·빌드를 연달아 돌린 뒤라 부하가 겹쳤을 수 있으나 **확인한 바 없다.**
> **「전건 통과」를 만들려고 더 돌리지 않았다** — 그것은 수치를 고르는 일이 된다.
> 사실 그대로 적는다: **이번 회차에서 프론트 전체 통과를 보지 못했다.**

---

## 7. 미측정 / 미결 — 그대로다

| 항목 | 상태 |
|---|---|
| **M-10**(재설치·판 올림 쿠키 유지, AC-T35) | **미측정** — 사람이 설치해야 한다. **strict 통과·사본 실험을 실기 통과로 쓰지 않는다** |
| **Windows 축 전부** | **검증 불가(이 기기)** — 실기 없음 + `llvm-rc` 부재. **macOS 결과로 대체하지 않는다**(strict 메시지에도 명시) |
| **D-4**(PRODUCTION 로그인 수단) | **미결 유지** |
| 실제 설치파일 생성 | **하지 않음** |
| macOS `.icns` | **저장소에 없음** — strict 가 잡는다. **만들지 않았다**(사본 실험은 `/tmp`, 삭제 완료) |
| 운영 origin · 서명 · 공증 · CI · 최소 OS 버전 | **미정 · 발명 0** |
| 판 번호 정책 | **Phase 8 재검토** |
| 프론트 스위트 불안정 | **여전히 있고, 이번 회차엔 3/3 실패**(§6-1) — 코디 판단 사항 |

---

## 8. 금지 사항 준수

| 금지 | 확인 |
|---|---|
| 실제 설치 · Release · 태그 · push | **하지 않았다.** HEAD `a1f6791` 그대로 |
| 아이콘 · 운영 주소 발명 | **0** — `.icns` 는 `/tmp` 사본에만 만들었고 **삭제**했다 |
| 허용 파일 외 변경 | 없다 — 스크립트 1 · `Makefile` · 보고서 3 |
