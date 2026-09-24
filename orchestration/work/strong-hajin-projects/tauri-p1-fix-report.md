# WORK-006 Phase 1 — 리뷰 W-1 · W-2 수정 보고

- **대상 리뷰**: `review-tauri-p1-report.md` (판정 WARN · FAIL 0건) 의 **W-1 · W-2 만**
- **작업 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · 브랜치 `kknaksss/strong-hajin-projects` · HEAD `a1f6791` (변동 없음)
- **커밋·push·PR**: 하지 않았다
- **범위 밖 손대지 않음**: W-3 ~ W-8 은 건드리지 않았다. 제품 `App.tsx`·`features/**`·`backend/**`·`docs/**` **0줄**

---

## 1. 바뀐 파일 — 3개

| 파일 | 항목 | 성격 |
|---|---|---|
| `frontend/vite.probe.config.ts` | **W-1** | 수정 |
| `frontend/src/dev/ProbePage.tsx` | **W-2** | 수정 |
| `frontend/src/dev/ProbePage.test.tsx` | **W-2** | 신규(회귀 시험 6건) |

전부 Phase 1 allowed_paths(`frontend/src/dev/**` · frontend 전용 fixture 설정) 안이다.
**capability 와 셸 URL 은 지시대로 그대로 두었다** — `probe-fixture.json` 의
`remote.urls`(`https://localhost:5180/*`)와 `lib.rs` 의 `DEFAULT_PROBE_URL` 모두 무변경.

---

## 2. W-1 — fixture 가 셸이 여는 `localhost` 로 닿게

### 리뷰가 지적한 것

`vite.probe.config.ts` 는 `host: "127.0.0.1"` 로 IPv4 하나에만 묶여 있는데 셸은
`https://localhost:5180` 을 연다. 이 기기의 `localhost` 는 **`::1` 을 먼저** 돌려주므로
첫 연결이 거절되고, 살아나는지가 클라이언트 fallback 에 달린다 →
「커맨드 왕복 실패」와 「fixture 에 닿지도 못함」이 섞여 **M-1 의 중단 판정이 틀린다.**

### ⚠ 리뷰의 권장 수정 하나만으로는 안 됐다 — 실측으로 확인

리뷰는 「`host: "localhost"` 로 바꾸면 **vite 가 양쪽 스택에 듣는다**」고 적었다.
**이 기기에서는 사실이 아니었다.** 바꿔서 띄운 뒤 직접 쟀다:

```text
$ lsof -nP -iTCP:5180 -sTCP:LISTEN
node  13190  ...  IPv6  TCP [::1]:5180 (LISTEN)        ← IPv6 한 줄뿐

$ curl --cacert .dev-certs/dev-ca.pem -o /dev/null -w "http=%{http_code}\n" …
https://localhost:5180/probe.html  http=200
https://[::1]:5180/probe.html      http=200
https://127.0.0.1:5180/probe.html  http=000        ← 이번엔 IPv4 가 죽었다
```

node 는 `host` 하나를 **주소 하나**로 잡는다. 그대로 두면 **문제의 방향만 뒤집는 꼴**이라,
`127.0.0.1` 로 접근하는 도구(다른 기기 설정·`/etc/hosts` 차이·구버전 resolver)에서
같은 혼동이 다시 난다.

### 실제로 한 수정

`host: "localhost"` 로 바꾸고, **이미 잡힌 loopback 의 반대쪽을 같은 포트로 마저 여는**
작은 vite 플러그인 `loopbackMirror()` 를 같은 파일에 넣었다.

- 어느 스택이 잡혔는지는 `httpServer.address()` 로 **런타임에 보고 정한다** — 기기가 어느 쪽을
  먼저 주든 반대편을 연다
- 여는 것은 **loopback 둘뿐**(`127.0.0.1` · `::1`). `0.0.0.0`·`::` 로 넓히지 않았으므로
  **LAN·Tailscale 어디에도 열리지 않는다**(코드 `AGENTS.md` 의 로컬 스택 바인딩 규칙과 같은 선)
- **TLS 는 그대로 vite 가 끝낸다.** 이 다리는 **바이트만 그대로 넘기는 TCP 포워더**라
  인증서 검증에 손대지 않는다 — 검증 무력화 우회가 아니다
- 인증서 재발급 **불필요**: leaf SAN 에 `DNS:localhost, IP:127.0.0.1, IP:::1` 이 이미 있다
  (`scripts/dev-https-cert.mjs`)
- 못 열면 **죽지 않고 경고**한다 — 「그 스택으로는 닿지 않는다」를 로그로 알린다

### 수정 후 실측

```text
$ lsof -nP -iTCP:5180 -sTCP:LISTEN
node  13927  ...  IPv4  TCP 127.0.0.1:5180 (LISTEN)
node  13927  ...  IPv6  TCP [::1]:5180 (LISTEN)

https://localhost:5180/probe.html   http=200  tls=0
https://[::1]:5180/probe.html       http=200  tls=0
https://127.0.0.1:5180/probe.html   http=200  tls=0

loopback 외 바인딩: 없음
```

`tls=0` 은 **검증을 켠 채**(`-k` 없이 `--cacert` 로) 받은 값이다.
vite 출력에도 `➜ Loopback mirror: https://127.0.0.1:5180/` 한 줄이 뜬다.

> **Phase 2 에 대한 리뷰의 요구는 그대로 남는다** — M-1 을 「미측정」으로 닫을 때
> **실패 원문(TLS 에러 코드 또는 연결 거절)을 한 줄이라도 남긴다.** 이번 수정은
> 「닿지 못해서 실패」 가능성을 없앤 것이지, 실패 원문을 대신 만들어 주지 않는다.

---

## 3. W-2 — IPC 실패를 마이크 실패로 적지 않는다

### 리뷰가 지적한 것

`ProbePage.tsx` 가 `getUserMedia`·`MediaRecorder` 와 `guard.acquire` 를 **한 `try`** 에 묶어,
`wake_guard_acquire` 실패(`E-14a`)를 `M-4 마이크 열기 실패(E-13)` 로 찍고 `setMicError` 까지
세웠다. 실제로는 마이크가 열렸고 녹음이 돌고 있다. 갈라야 할 두 사유를 합쳐 찍으면
**Phase 2 기록이 거짓이 되고 중단 판정이 잘못 열린다.**

### 실제로 한 수정

`start()` 를 **두 구간으로 갈랐다.**

| 구간 | 실패하면 | 기록 | 점유 | 녹음 |
|---|---|---|---|---|
| ① `getUserMedia` + `MediaRecorder` + `start()` | `E-13` | `M-4 마이크 열기 실패(E-13) — 점유를 걸지 않았다` | **걸지 않는다**(L-03) | 시작 안 됨 |
| ② `guard.acquire` | `E-14a` | `M-9 wake_guard_acquire 실패(E-14a) — 마이크는 열려 있고 녹음은 계속한다` | 실패 | **계속한다** |

- 구간 ① 이 실패하면 **`return`** 한다 — `acquire` 를 아예 부르지 않는다(L-03)
- `running.current` 는 ① 과 ② **사이**에서 세운다 — ② 가 실패해도 녹음은 살아 있고
  `stop()` 이 정상으로 `release` 를 부른다(모르는 세션이어도 멱등 — `E-08`)
- 화면도 갈랐다: **「마이크 실패(E-13)」**(붉은 줄)과 **「점유 문제 — 마이크는 열려 있고 녹음은
  계속된다」**(주황 줄)가 서로 다른 줄이다
- `degraded` 응답은 **실패가 아니라 상태**로 따로 보인다 — `E-14a` 와 섞지 않았다
  (SPEC-006 §4: `degraded` 는 점유가 섰고 OS 에 못 건 것)

### 회귀 시험 6건 — `src/dev/ProbePage.test.tsx` (신규)

`RecordingPanel` 을 `export` 해 props(`guard`·`onLog`)로 직접 시험한다.
`getUserMedia`·`MediaRecorder` 는 jsdom 스텁을 꽂는다.

| # | 시험 | 지키는 것 |
|---|---|---|
| 1 | `acquire` 가 던지면 **`E-14a` 로 적고 `E-13`·`M-4` 로 적지 않는다**. `getUserMedia` 는 1회 호출됐고 「녹음 시작」 기록이 남는다 | W-2 본체 |
| 2 | 같은 상황에서 화면이 **「점유 문제」**로 보이고 「마이크 실패(E-13)」는 없다. **트랙을 멈추지 않는다** | `E-14a` = 녹음 계속 |
| 3 | `degraded` 응답은 상태로 보이고 `E-13` 기록이 없다 | `degraded` ≠ 실패 |
| 4 | `getUserMedia` 거부 → `E-13` · **`acquire` 미호출** · `E-14a` 없음 | L-03 |
| 5 | `MediaRecorder` 가 던짐 → `E-13` · `acquire` 미호출 · **트랙 stop 호출** | 마이크를 켜진 채 두지 않는다 |
| 6 | `guard` 가 `null`(셸 없음) → 녹음만 돌고 점유 관련 기록 0 | `E-01` |

### 이 시험이 **실제로** 회귀를 잡는지 확인했다 (mutation 검사)

회귀 시험은 「지금 통과한다」만으로는 값을 증명하지 못한다. 그래서 **옛 동작을 일부러
되살려** 돌려 봤다 — 점유 실패를 `M-4`/`E-13` 으로 찍도록 되돌린 판에서:

```text
× acquire 가 실패해도 E-14a 로 적고, E-13 으로 적지 않는다
× acquire 가 실패해도 화면은 마이크 실패가 아니라 점유 문제로 보인다
✓ (나머지 4건)
   Tests  2 failed | 4 passed (6)
```

**정확히 W-2 가 지적한 두 자리에서만 붉어졌다.** 확인 뒤 원본으로 복원했다
(복원본에 `E-14a` 9곳 존재 확인).

---

## 4. 실행한 검증 — 명령과 결과

| # | 명령 | 결과 |
|---|---|---|
| F-1 | `npx tsc --noEmit` | **exit 0 · 출력 0줄** |
| F-2 | `npx vitest run src/dev/` (변경 범위) | **3 files · 23 tests 전건 통과** (기존 17 + 신규 6) |
| F-3 | `npx vitest run src/dev/ProbePage.test.tsx` (mutation 판) | **2 failed · 4 passed** — 회귀 포착 확인 |
| F-4 | `make frontend-test` (1회차) | EXIT=2 — `1 failed | 1039 passed (1040)` → §5 |
| F-5 | `make frontend-test` (2회차) | **EXIT=0 · `73 passed (73)` · `1040 passed (1040)`** |
| F-6 | `npm run build` + 유출 grep | **EXIT=0** · `탐침|probe-root|__TAURI_INTERNALS__|wake_guard|loopback` **0건** |
| F-7 | fixture 기동 · `lsof` · 3주소 curl | §2 「수정 후 실측」 표 그대로 |

- **Rust 는 한 줄도 바꾸지 않아** `cargo check`/`cargo test` 를 다시 돌리지 않았다
  (직전 보고서 V-3·V-4: warning 0 · `21 passed`). W-1·W-2 는 둘 다 프론트 쪽이다
- 테스트 수 변화: **1034 → 1040**. 늘어난 6건이 이번에 추가한 회귀 시험 전부다

---

## 5. 직전 보고서 B-5(이름 미특정 flake)를 **특정했다**

직전 보고서는 「제품 테스트에 시간 의존 flake 가 있을 수 있다 — **이름을 특정하지 못했다**」로
남겨 두었다. 이번에 F-4 에서 같은 형태가 재현돼 **이름을 잡았다.**

```text
FAIL  src/features/work/CreateWork.test.tsx
      > 생성 창의 갈래 — 업무는 내 업무다
      > 실패한 제출을 그대로 다시 누르면 «같은 키» 다 — 두 건이 되지 않는다

TestingLibraryElementError: Unable to find an accessible element
with the role "button" and name "업무 추가"
```

**내 변경과 무관하다는 근거**

- 이 파일은 **이번에도 직전에도 건드리지 않았다**(`git status` — `src/features/**` 0줄)
- 계측 코드는 `src/dev/**` 에만 있고 제품 테스트가 그것을 import 하지 않는다
- `vite.probe.config.ts` 는 **vitest 가 읽지 않는다**(vitest 는 `vite.config.ts` 를 쓴다)
- **단독 5회 연속 실행: `34 passed` × 5 — 한 번도 실패하지 않았다**
- 전체 스위트 2회차(F-5)에서 **1040 전건 통과**

→ **전체 스위트를 함께 돌릴 때만 간헐적으로 나는 제품 테스트 flake**다.
이번 수정의 결과가 아니고, 고치는 것도 이번 범위가 아니다. **코디 판단 사항으로 올린다.**

---

## 6. 하지 않은 것

- **W-3 ~ W-8 미처리** — 지시대로 W-1·W-2 만 했다. 특히 W-4(macOS 재무장이 캐시된 assertion
  앞에서 no-op)는 **점유 계약에 닿는 항목**이라 Phase 3 이 반드시 봐야 한다
- **capability·셸 URL 무변경** — `remote.urls` 와 `DEFAULT_PROBE_URL` 을 건드리지 않았다
- **M-1 측정 안 함** — 로컬 CA 신뢰 설치는 여전히 사용자 조작이고, 하지 않았다.
  **미실측은 여전히 미실측이다**
- **TLS 검증 무력화 없음** — loopback 다리는 바이트만 넘긴다
- **커밋·push·PR·추가 워커 없음**
