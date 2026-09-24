# WORK-006 Phase 9 Release preflight — 독립 검수

- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **검수 대상**: `frontend/scripts/verify-release-artifact.mjs`(323줄) · `Makefile` `shell-release-preflight` · `tauri-p9-release-preflight-report.md`
- **read-only 검수.** 태그 · GitHub Release · push · 서명 · 공증 · **빌드** · 설정 변경 **없음.**
  돌린 것은 **쓰기 API 가 없는 관문**과 **스크래치패드 fixture** 뿐이다.
- **이 검수 보고서 한 파일만 작성.**

---

## 0. 종합 판정 — **FAIL 0 · WARN 1(높음) · 나머지 PASS**

**관문이 재는 것을 실제로 잰다.** 보고된 fixture 11건을 **전부 재현**했고, 여기에 **검수가 3건을
더해** 14건을 돌렸다. 종료 코드 일곱 갈래(0·2·3·4·5·6·7)가 **원인마다 정확히 갈린다.**

**구조적 안전이 grep 으로 증명된다** — import 는 `readFileSync · existsSync · readdirSync ·
statSync` + `createHash` 뿐이고 **`writeFile`·`mkdir`·`exec`·`spawn`·`fetch` 가 한 건도 없다.**
「굽지 않는다 · 네트워크를 건드리지 않는다 · 저장소를 쓰지 않는다」가 **코드의 성질**이다.

**WARN 1 건이 발주 항목 ③ 에 직접 걸린다** — candidate 에 **기록에 없는 «디렉터리»** 를 두면
**아무 말 없이 exit 0** 이다. 추가 «파일»은 exit 5 로 막는데(R-11), 디렉터리는 집합 대조에서
**빠진다**. 「Release 는 집합으로 올라간다」는 §5-2 의 자기 원칙과 어긋난다.

---

## 1. 판정표

| # | 발주 검수 항목 | 판정 |
|---|---|---|
| 1 | Phase 8 manifest 부재/`artifacts` 빈 상태를 통과로 만들지 않고 nonzero | **PASS** |
| 2 | 정상 fixture 에서 SHA-256 · version · shell_api · origin 조합 · 파일 집합을 정확히 비교 | **PASS** |
| 3 | 누락 · 해시 불일치 · 조합 불일치 · **추가 파일** · **디렉터리 번들** | **PASS** 넷 · **WARN** 「candidate 의 디렉터리」(W-1) |
| 4 | fixture 가 임시 디렉터리에만 생성 · 저장소/Release 에 쓰지 않음 | **PASS** (해시 동일) |
| 5 | Windows 미검증 · D-4 · 운영 origin · M-1/M-5/M-10 을 통과로 바꾸지 않음 | **PASS** |
| 6 | Makefile 자동화 진입점 · 종료 코드 의미가 명확 | **PASS** |

---

## 2. FAIL

**없다.**

---

## 3. 재현한 수치 — **14건**(보고서 11 + 검수 추가 3)

fixture 는 전부 **내 스크래치패드**에서 만들었다. 조합 대조가 지금 트리를 읽으므로,
Phase 8 V-6 과 같은 방식으로 **스크립트 사본 + 조합이 맞는 `src-tauri` 사본**을 옆에 두고 돌렸다.

| # | 상황 | 보고서 | **재현** | 일치 |
|---|---|---|---|---|
| R-1 | 입력 없음 | 2 | **2** — `입력이 모자라다 — …두 쪽이 있어야 잴 수 있다` | ✅ |
| R-2 | manifest 파일 없음 | 2 | **2** | ✅ |
| R-3 | candidate 디렉터리 없음 | 2 | **2** | ✅ |
| R-4 | `rehearsal: true` manifest | 3 | **3** — `**검증되지 않은 manifest 다**` | ✅ |
| R-5 | `artifacts: []` | 4 | **4** — `굽지 않은 기록이다` | ✅ |
| **R-5b** | **기록이 `.app` 하나뿐(해시 0개)** — *검수 추가* | — | **4** — `**해시가 하나도 없다** — 동일성을 잴 근거가 없다` | §5-1 확인 |
| R-6 | 조합 불일치(판 `9.9.9` vs 트리 `0.0.1`) | 7 | **7** | ✅ |
| R-7 | 정상 manifest vs **실제 저장소** | 7 | **7** — `origin — manifest=https://app.example.com · 트리(shell.config.json)=null` | ✅ **문구까지 동일** |
| R-8 | 정상(조합이 맞는 트리) | 0 | **0** — `동일성 확인 — 1건이 Phase 8 기록과 **바이트까지 같다.**` | ✅ |
| R-9 | 해시 불일치 | 6 | **6** — `기록:`/`실물:` 두 줄로 나란히 | ✅ |
| **R-9b** | **해시는 같은데 `bytes` 가 다름** — *검수 추가* | — | **6** — 방어 분기가 산다 | 좋음 |
| R-10 | candidate 가 비었다 | 5 | **5** — `없다 — 기록에는 있는데 candidate 에 없다` | ✅ |
| R-11 | 기록에 없는 **파일**이 섞였다 | 5 | **5** — `기록에 없다 — candidate 에 있는데 Phase 8 이 본 적 없다` | ✅ |
| **R-12** | **기록에 없는 «디렉터리»(`Strong Hajin.app`)가 섞였다** — *검수 추가* | — | **0 · 언급조차 없음** | ❌ **W-1** |
| — | `make shell-release-preflight`(인자 없음) | make 2 | **make 2** | ✅ |

**보고된 11건은 전부 일치한다.** 검수가 더한 셋 중 둘(R-5b·R-9b)은 **설계대로 막혔고**,
하나(R-12)가 **빠져나갔다.**

---

## 4. 항목별 확인

### 4-1. manifest 부재·빈 아티팩트 (PASS)

- `artifacts: []` → **exit 4**, 「**이 스크립트는 해시를 지어내지 않는다**」를 출력에 적는다.
- **해시가 하나도 없는 기록**(전부 `bundleDir`)도 **exit 4** — 「**«해시가 없다»를 «같다»로 바꾸지 않는다**」.
  **R-5b 로 확인**했다. 「잴 근거가 없으면 통과가 아니다」가 코드에 있다.
- `rehearsal: true` · `originsAgree ≠ true` · `operationalOrigin` 빈 값 → **exit 3**,
  「Phase 8 관문을 **exit 0 으로** 통과시킨 뒤 그때 찍힌 manifest 를 쓰세요」.
  → **Phase 8 의 연습(exit 3) 기록이 Release 로 승격되는 길이 막혔다.**

### 4-2. 정상 fixture 의 대조 정확성 (PASS)

- **해시**: `createHash("sha256").update(readFileSync(path))` — 실물 바이트를 직접 읽는다.
- **조합 넷**을 **지금 트리**와 대조한다 — `Cargo.toml` 판 번호 · `lib.rs` `SHELL_API` ·
  `shell.config.json` origin · capability `remote.urls[0]`. **여기에 더해 manifest 내부 정합**
  (`capabilityRemoteUrl === operationalOrigin + "/*"`)까지 본다.
- **집합**: 기록된 이름 ↔ candidate 의 파일 이름을 **양방향**(`missing` · `extra`)으로 본다.
- **크기까지 본다**: 해시가 같아도 `bytes` 가 다르면 불일치로 센다 — 「manifest 쪽 기록이 상한
  것이다 — 조용히 넘기지 않는다」. **R-9b 로 확인**.

### 4-3. 각 실패 유형 (PASS 넷 · WARN 하나)

| 유형 | 결과 |
|---|---|
| 누락 | **5** ✅ |
| 해시 불일치 | **6** ✅ (기록/실물을 나란히 찍어 사람이 판단할 수 있게) |
| 버전·조합 불일치 | **7** ✅ (어느 축이 어긋났는지 축별로 나열) |
| **추가 파일** | **5** ✅ |
| **candidate 의 추가 디렉터리** | **0 — 빠져나간다** ❌ → **W-1** |

manifest **쪽**의 디렉터리 항목(`.app`)은 올바르게 처리된다 — 혼합 fixture 에서
`-- 해시가 없어 **대조하지 못한** 기록: 1건 --` / `ℹ Strong Hajin.app — 디렉터리 번들이라 해시가
없다. **«같다»고 쓰지 않는다**` 를 재현했다. **문제는 candidate 쪽뿐이다.**

### 4-4. fixture 격리 (PASS)

- 모든 fixture 를 **스크래치패드**에만 만들고 끝나고 지웠다.
- **저장소 설정 해시가 실험 전후 완전히 동일**(`shell.config.json` · `product-shell.json`).
- `git status --porcelain` 에 새 파일 없음 · `git diff --stat frontend/src-tauri/` **0줄**.
- **스크립트에 쓰기 API 가 없다** — 경로를 어디로 주든 쓸 수 없다(§0).

### 4-5. 미검증·미결을 통과로 바꾸지 않는다 (PASS)

**R-8 통과 출력 전문에서 확인**:

```
-- 플랫폼 상태 --
  · macOS(dmg): 검증됨(해시 일치) (자산 1건)
  · Windows(msi·nsis): **미검증** — 이 manifest 는 darwin 에서 만들어졌다 (자산 0건)
  **이 호스트에서 굽지 못한 플랫폼은 이 관문으로 검증되지 않는다 — 상태를 그대로 적는다.**

⚠ **통과가 뜻하지 않는 것**:
  · 서명·공증이 되어 있다 — 이 관문은 서명을 보지 않는다
  · 설치가 된다 — 실기 설치는 사람이 확인한다(M-10 미측정)
  · Release 가 만들어졌다 — **이 관문은 태그도 Release 도 만들지 않는다**
```

- **통과해도 Windows 는 「미검증」**이다 — 자산 0건을 「없어서 통과」로 바꾸지 않는다.
- **서명·공증·M-10 을 통과 화면이 스스로 배제**한다.
- 보고서 §8 이 운영 origin(OQ-T02) · **D-4** · M-1 · M-5 · M-10 · Windows · `.icns` · N-2 를
  **미결 그대로** 유지한다. §7 이 「**현재 저장소에서는 통과할 수 없다**」와 그 이유 둘(Phase 8 이
  아직 exit 0 이 아니다 · 아무것도 굽지 않았다)을 적고, 「여기서 통과를 만들려면 origin 을 지어내거나
  해시를 지어내야 하고, **둘 다 하지 않았다**」로 닫는다 — **정확하다.**

### 4-6. Makefile (PASS)

`Makefile:161-173` 주석이 ① **읽기 전용**(굽지 않고·태그 달지 않고·Release 만들지 않고·서명 안 하고·
네트워크 안 건드림) ② 호출 형태 ③ 「**manifest 가 없거나 아티팩트가 없으면 실패한다 — 자리표시
해시를 만들지 않는다**」 ④ **⚠ 자동화·CI 는 이 타깃을 쓰지 말 것** + **일곱 코드의 뜻** +
**직접 호출 명령**(`cd frontend && node scripts/verify-release-artifact.mjs --manifest <path> --candidate <dir>`)
을 모두 적는다. `.PHONY` 에 `shell-release-preflight` 등록 확인.
**Phase 8 W-1 에서 합의한 진입점 규약이 그대로 이어졌다.**

---

## 5. WARN (1건 · 높음)

### W-1 — candidate 의 **기록에 없는 디렉터리**가 조용히 통과한다

**좌표**: `verify-release-artifact.mjs` 집합 대조부

```js
const present = readdirSync(candidateDir).filter((name) => {
  const info = statSync(join(candidateDir, name));
  return info.isFile();          // ← 디렉터리는 집합에서 아예 빠진다
});
const extra = present.filter((name) => !wanted.has(name));
```

**재현(R-12)**: R-8 이 통과하던 candidate 에 `Strong Hajin.app/` 디렉터리 하나를 더했다 →
**exit 0**, 출력에 **언급조차 없다**. 같은 자리에 «파일»을 더하면 **exit 5** 다(R-11).

**왜 문제인가**
- 보고서 §5-2 가 스스로 적은 원칙 —
  「**Release 는 집합으로 올라가므로**, candidate 에 Phase 8 이 본 적 없는 파일이 하나라도 있으면
  **그 Release 는 「검증된 자산」이 아니다**」 — 과 어긋난다.
- macOS 에서 `.app` 은 **실제로 디렉터리**다. candidate 에 `.app` 이 섞이는 것은
  **가장 있을 법한 사고**이고, 바로 그 형태가 안 잡힌다.
- 보고서 §5-1 은 `.app` 을 **manifest 쪽** 처리로만 설명하고, **candidate 쪽이 디렉터리를 무시한다는
  사실은 어디에도 없다.** 읽는 사람은 「집합을 본다」로만 읽는다.

**막지 못하는 범위를 정확히**: 기록된 파일의 바이트 동일성과 **추가 «파일»** 차단은 그대로 유효하다.
새는 것은 **기록에 없는 디렉터리**뿐이다. 그래서 FAIL 이 아니라 WARN 이다 —
다만 **발주 항목 ③ 이 「디렉터리 번들」을 명시했으므로, 그 항목만은 «부분 충족»이다.**

**수정 방향**(택일, 둘 다 한 줄 안팎)
1. `readdirSync` 결과에서 **디렉터리도 수집**해 `extra` 에 넣는다 → R-12 가 **exit 5** 가 된다
2. 최소한 **`ℹ candidate 에 디렉터리 N 건이 있다 — 대조 대상이 아니다`** 를 찍어
   **침묵을 없앤다**(현재는 아무 말도 하지 않는 것이 가장 나쁜 부분이다)

---

## 6. 차단·미결 (이번 회차가 만든 것 아님 — 유지)

| # | 항목 | 주인 |
|---|---|---|
| 1 | **운영 origin**(OQ-T02) — 미정 → Phase 8 이 exit 0 이 아니고, 따라서 **쓸 수 있는 manifest 가 없다** | 사용자·코디 |
| 2 | **D-4** — PRODUCTION 세션 발급 수단 부재 | 코디·사용자(OQ-W05) |
| 3 | **M-1 · M-5 · M-10** — 미측정(실기·설치 필요) | 사용자 |
| 4 | **Windows 자산 전부** — 이 기기에서 굽지 못함(`llvm-rc` 부재) · 통과해도 「미검증」 | OQ-W01 |
| 5 | **서명 · 공증 · 업데이트** — 범위 밖. 관문이 읽지도 않는다 | Phase 10+ |
| 6 | macOS **`.icns`** · **N-2 스위트 불안정** | Phase 7 후속 · 코디 |
| 7 | **의도적 우회**(스크립트를 옮기면 통과를 만들 수 있다) — Phase 8 §6 의 한계를 **§6-1 이 반복해 적었다.** 관문이 막는 것은 실수와 오집계, 의도적 우회는 **리뷰와 서명**의 몫 | 코디 |

---

## 7. 한 줄 정리

**「이름이 같아도 같은 파일이 아니다」를 바이트 해시로 좁힌 관문이고, 14건을 돌려 일곱 코드가
원인마다 갈리는 것을 확인했다** — 빈 기록도 연습 기록도 해시 없는 기록도 전부 nonzero 이고,
통과 화면조차 서명·설치·Windows 를 스스로 배제한다. 남은 것은 **candidate 의 기록에 없는
디렉터리가 조용히 통과한다는 한 자리(W-1)** 이며, 한 줄 수정으로 닫힌다.
