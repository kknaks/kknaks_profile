# WORK-006 Phase 9 — Release 자산 동일성 preflight

- **작성**: 2026-09-23 **00:24 KST**
- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **결과**: 관문 신설. **현재 저장소에서 nonzero** — 올릴 아티팩트도, 통과한 Phase 8 manifest 도 없다
- **하지 않은 것**: 태그 · GitHub Release · 프로필 60-release 문서 · push · 서명 · 공증 · 업데이트 · 빌드

---

## 1. 한 줄 결론

Phase 8 은 **「무엇으로 구울 것인가」**를 보고 끝난다. 그 뒤 **굽고 → 올리는 사이**에 아무도 보지 않는
구간이 있다 — 다시 구운 판, 손으로 고친 파일, 다른 기기에서 가져온 것, 이름만 같은 옛 판.
**이름이 같아도 같은 파일이 아니다.** 그 구간을 **바이트 해시**로 좁히는 관문을 만들었다.

---

## 2. 변경 파일 — 셋뿐이다

| 파일 | 변경 |
|---|---|
| `frontend/scripts/verify-release-artifact.mjs` | **신규** — 관문 + 오류 코드 |
| `Makefile` | `shell-release-preflight` 타깃 + `.PHONY` **한 줄씩** |
| `tauri-p9-release-preflight-report.md` | **신규** — 이 문서 |

**건드리지 않은 것**(확인: `git diff --stat frontend/src-tauri/` **출력 0줄**):
`shell.config.json`(여전히 `operationalOrigin: null`) · capability(여전히 `.invalid`) ·
`tauri.conf.json` · `Cargo.toml` · `src-tauri/src/**` · Phase 7·8 스크립트 · 제품 코드 · backend.
**태그 0 · Release 0 · push 0** — `git tag --points-at HEAD` 출력 없음, HEAD `a1f6791`.

---

## 3. 입력 둘과 manifest 스키마

```
node scripts/verify-release-artifact.mjs --manifest <phase8.json> --candidate <dir>
```

**읽는 열쇠만 적는다** — 모르는 열쇠는 무시하고, 없는 열쇠를 지어내지 않는다.

| 열쇠 | 형 | 쓰임 |
|---|---|---|
| `appVersion` | string(semver) | 조합 대조 |
| `shellApi` | number | 조합 대조 |
| `operationalOrigin` | string(https origin) | 조합 대조 |
| `capabilityRemoteUrl` | string | `<origin>/*` 인지 |
| `originsAgree` | **true 여야 한다** | 아니면 «검증되지 않은 manifest» |
| `rehearsal` | **false 여야 한다** | true 면 연습 기록이다 |
| `artifacts[]` | `{path, sha256, bytes, bundleDir}` | **동일성의 근거** |
| `hostPlatform` | string | 어느 플랫폼이 **미검증**인지 |

**Phase 8 이 통과(exit 0)하며 찍는 manifest 와 같은 모양이다** — 새 형식을 만들지 않았다.

---

## 4. 오류 코드 — 원인마다 다르다

| 코드 | 뜻 | 언제 |
|---|---|---|
| **0** | 동일하다 | 집합·해시·조합이 모두 맞다 |
| **2** | 돌릴 수 없다 | 입력 없음 · 파일/디렉터리 없음 · JSON 아님 |
| **3** | **검증되지 않은 manifest** | `rehearsal: true` · `originsAgree≠true` · origin 빈 값 |
| **4** | **아티팩트가 없다** | `artifacts: []` 또는 **해시가 하나도 없다** |
| **5** | **집합 불일치** | 기록된 파일이 없다 · 기록에 없는 파일이 섞였다 |
| **6** | **해시 불일치** | 이름은 같은데 다른 파일이다 |
| **7** | **조합 불일치** | 판 번호·shell_api·origin·capability 가 지금 트리와 다르다 |

> ⚠ **`make` 로 부르면 이 코드들이 전부 2 로 뭉개진다**(GNU make 가 레시피의 nonzero 를 감싼다 —
> Phase 8 W-1 보정에서 실측). **코드를 읽어야 하는 자동화는 스크립트를 직접 부른다.**
> Makefile 타깃 주석에도 같은 말을 적었다.

---

## 5. 설계에서 **거절한 것** 셋

### 5-1. 해시가 없는 항목을 «같다»로 세지 않는다

`.app` 은 디렉터리라 Phase 8 manifest 에 `sha256: null · bundleDir: true` 로 실린다.
이런 항목은 **대조 집합에서 빼고 `ℹ` 로 따로 적는다** — 「해시가 없다」는 「같다」가 아니다.
**기록 전체에 해시가 하나도 없으면 exit 4** 로 끝낸다(잴 근거가 없다).

### 5-2. **기록에 없는 파일이 섞인 것**도 실패다

「빠진 것」만 보면 절반이다. Release 는 **집합**으로 올라가므로, candidate 에 Phase 8 이 본 적 없는
파일이 하나라도 있으면 **그 Release 는 「검증된 자산」이 아니다**. R-11 이 그 경우다(exit 5).

### 5-3. 다시 굽지 않는다

candidate 가 비어 있어도 **빌드하지 않는다.** 이 관문이 굽기 시작하면 「Phase 8 이 본 파일」이라는
전제가 무너진다 — 자기가 만든 것을 자기가 검증하는 꼴이 된다.

---

## 6. 검증 — fixture 11건, **전부 임시 디렉터리에서**

fixture 는 scratchpad 에서만 만들었고 **저장소·Release 에 손대지 않았다.**

| # | 상황 | 종료 코드 | 기대 |
|---|---|---|---|
| R-1 | 입력 없음 | **2** | ✓ |
| R-2 | manifest 파일 없음 | **2** | ✓ |
| R-3 | candidate 디렉터리 없음 | **2** | ✓ |
| R-4 | **연습(rehearsal) manifest** | **3** | ✓ |
| R-5 | **아티팩트 없음** | **4** | ✓ |
| R-6 | 조합 불일치(판 번호 `9.9.9` vs 트리 `0.0.1`) | **7** | ✓ |
| R-7 | **정상 fixture vs 실제 저장소** | **7** | ✓ (§7) |
| R-8 | **정상**(조합이 맞는 트리) | **0** | ✓ |
| R-9 | **해시 불일치** | **6** | ✓ |
| R-10 | candidate 에 파일이 없다 | **5** | ✓ |
| R-11 | **기록에 없는 파일이 섞였다** | **5** | ✓ |

**R-9 출력** — 「이름은 같은데 다른 파일」을 눈으로 보이게 적는다:

```
✗ Strong Hajin_0.0.1_aarch64.dmg
    기록: 0000…0000  (31 bytes)
    실물: 90336712…3591f6  (31 bytes)
```

**R-8 통과 출력** — Windows 는 **자산이 없어도 «미검증»으로 적힌다**:

```
✓ Strong Hajin_0.0.1_aarch64.dmg  90336712…3591f6  (31 bytes)
· macOS(dmg): 검증됨(해시 일치) (자산 1건)
· Windows(msi·nsis): **미검증** — 이 manifest 는 darwin 에서 만들어졌다 (자산 0건)
동일성 확인 — 1건이 Phase 8 기록과 **바이트까지 같다.**
```

### 6-1. R-8 을 어떻게 돌렸는가 — 진짜 트리를 건드리지 않고

조합 대조는 **지금 트리**의 `Cargo.toml` · `lib.rs` · `shell.config.json` · capability 를 읽는다.
이 저장소는 origin 이 `null` 이라 **어떤 manifest 와도 조합이 맞지 않는다**(= R-7).
그래서 Phase 8 V-6 과 같은 방법으로 **스크립트를 scratchpad 에 복사**해, 그 사본 옆에 조합이 맞는
`src-tauri` 사본을 두고 돌렸다. **진짜 워크트리는 한 글자도 바뀌지 않았다.**

> Phase 8 §6 에 적은 **잔여 우회**가 여기에도 그대로 있다: 스크립트를 옮기면 통과를 만들 수 있다.
> **이 관문이 막는 것은 실수와 자동화의 오집계**이고, **의도적 우회는 리뷰와 서명의 몫**이다.
> 같은 한계를 Phase 9 에서도 **숨기지 않고 반복해 적는다.**

---

## 7. 현재 저장소에서는 **통과할 수 없다** — 기록해 둔다

| 실행 | 결과 |
|---|---|
| `make shell-release-preflight`(인자 없음) | **make exit 2** · 스크립트 **exit 2** — 입력이 없다 |
| 정상 fixture manifest + 실제 트리 | **exit 7** — `origin — manifest=https://app.example.com · 트리(shell.config.json)=null` |

**이유는 둘이고, 둘 다 미결이라 이번 Phase 가 풀 수 없다**:

1. **Phase 8 관문이 아직 exit 0 이 아니다**(운영 origin 미정) → 통과한 manifest 가 존재하지 않는다
2. **아무것도 굽지 않았다** → `target/release/bundle` 이 없어 `artifacts` 가 빌 수밖에 없다

**그래서 nonzero 가 옳은 상태다.** 여기서 통과를 만들려면 origin 을 지어내거나 해시를 지어내야 하고,
**둘 다 하지 않았다.**

---

## 8. 남은 미결 — 그대로 유지한다

| 항목 | 상태 |
|---|---|
| **운영 origin**(OQ-T02) | **미정** — `operationalOrigin: null` · capability `…not-yet-decided.invalid/*` |
| **D-4** PRODUCTION 로그인 수단 | **미결** — 운영 프로파일에 세션을 발급하는 경로가 없다 |
| **M-10**(재설치·판 올림 쿠키 유지, AC-T35) | **미측정** — 사람이 설치해야 한다. **이 관문의 통과를 설치 성공으로 쓰지 않는다** |
| **Windows 자산 전부** | **미검증** — 이 기기에서 굽지 못한다(`llvm-rc` 부재). 관문이 통과해도 **상태를 «미검증»으로 적는다** |
| **M-1**(https 신뢰) · **M-5**(재시작 후 쿠키 유지) | **미측정** |
| 서명 · 공증 · 업데이트 | **범위 밖** — 이 관문은 서명을 보지 않는다(통과 화면이 그렇게 말한다) |
| macOS `.icns` | **없음** — `make shell-verify SHELL_STRICT=1` 이 잡는다 |
| **N-2 프론트 스위트 불안정** | **이월** — 이번 회차는 `frontend/src` 를 건드리지 않았고 **재실행하지 않았다** |

---

## 9. 금지 사항 준수

| 금지 | 확인 |
|---|---|
| 태그 · GitHub Release · push | **없음** — `git tag --points-at HEAD` 출력 없음 · HEAD `a1f6791` |
| 프로필 60-release 문서 수정 | **없음** |
| 서명 · 공증 · 업데이트 | **없음** — 관문은 서명을 읽지도 않는다 |
| 빌드 · 설치 | **없음** — candidate 가 비어도 굽지 않는다 |
| placeholder/임의 해시 생성 | **0** — 아티팩트가 없으면 **exit 4 로 끝낸다** |
| Windows 미검증을 검증됨으로 | **하지 않았다** — 통과 화면에도 «미검증»으로 적힌다 |
| 저장소·설정 수정 | **없음** — `git diff --stat frontend/src-tauri/` 출력 0줄 |
| 허용 경로 밖 변경 | 없다 — 스크립트 1(신규) · Makefile(타깃 1 + `.PHONY`) · 보고서 1 |
