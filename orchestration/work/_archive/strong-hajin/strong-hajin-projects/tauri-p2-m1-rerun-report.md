# WORK-006 Phase 2 — M-1 재측정 보고 (2026-09-22 19:54 KST)

- **발주**: 「로컬 CA 신뢰 설치를 마쳤다」는 사용자 보고에 따라 **M-1 만** 다시 측정
- **갱신한 문서**: `tauri-measurement-r1.md` → §「M-1 재측정 · 2026-09-22 19:54 KST」 추가
  (요약표 M-1 행과 머리말 측정 시각도 함께 갱신)
- **결과**: **M-1 은 여전히 미측정.** 판정(**보완 · 조건부**)에 변화 없음
- 코드·package·SPEC/WP **무변경** · 커밋/push/Release **없음**

---

## 1. 한 줄 결론

**문서가 열리지 않았다.** 셸은 네비게이션 훅까지만 발화하고 페이지 로드 사건이 0건이며,
커맨드 넷 중 **하나도 호출되지 않았다.** 원인은 1차와 같다 — **이 기기에서 로컬 CA 가
어느 키체인·어느 신뢰 도메인에도 없다.** 사용자 보고와 기기 상태가 어긋난다.

---

## 2. 먼저 확인한 것 — 신뢰 상태 (읽기전용, 아무것도 바꾸지 않았다)

| 확인 | 결과 |
|---|---|
| `security verify-cert -c .dev-certs/localhost.pem` | **`CSSMERR_TP_NOT_TRUSTED`** |
| `security find-certificate -a -c "SCAX WORK-006 probe local CA"` | **0건** (전 키체인) |
| 같은 검색, `/Library/Keychains/System.keychain` | 없음 |
| `security dump-trust-settings` (사용자 도메인) | `No Trust Settings were found.` |
| `security dump-trust-settings -d` (관리자 도메인) | 6건 — 전부 무관한 제3자 CA<br>`Dreamsecurity ROOT CA` · `iniLINE CrossEX RootCA2` · `VERAPORT-CA` · `127.0.0.1` · `INTEREZEN CA` · `INNORIX.CA` |
| leaf 를 직접 신뢰했을 가능성 (`-c localhost`) | 키체인에 **0건** |

우리 leaf 지문: `BD:7B:86:6C:75:EF:C0:64:39:CA:62:7A:60:20:C5:50:54:48:4C:3E`

> **신뢰 상태가 어긋나 보여도 실측은 그대로 진행했다.** 「설치했다」는 보고를 근거로,
> 기기 상태 판정이 아니라 **실제 셸 동작**으로 답을 내는 것이 맞기 때문이다.

---

## 3. 실행한 명령과 관측값

### ① fixture 기동 — 정상 (PID 31759)

```text
$ node node_modules/vite/bin/vite.js --config vite.probe.config.ts
  ➜  Local:   https://localhost:5180/
  ➜  Loopback mirror: https://127.0.0.1:5180/

$ lsof -nP -iTCP:5180 -sTCP:LISTEN -a -p 31759
node 31759 … IPv6 TCP [::1]:5180 (LISTEN)
node 31759 … IPv4 TCP 127.0.0.1:5180 (LISTEN)
```

**두 loopback 스택 모두 LISTEN** — W-1 수정이 유지되고 있다.

### ② 셸 실행 — 문서가 열리지 않았다 (PID 31890)

```text
$ ./target/debug/scax-probe-shell
[probe][boot] t=1790074496110 url=https://localhost:5180/probe.html nav_allow=["https://localhost:5180"]
[probe][nav]  t=1790074496754 navigate url=https://localhost:5180/probe.html origin=https://localhost:5180 allowed=true
```

14초 대기 후에도 **stdout·stderr 합쳐 위 두 줄이 전부**다.

| 확인 | 결과 |
|---|---|
| `grep -c "probe\]\[load\]"` | **0** — 페이지 로드 사건 없음 |
| `grep -E "probe\]\[(ipc\|wake)\]"` | **(없음)** — 커맨드 실행 흔적 없음 |

> 대조: 1차 회차에서 **평문 origin으로는 같은 셸이** `[probe][load] started` · `finished` 를
> 정상 발화했다. 훅 자체는 살아 있고, 이번엔 **문서가 아예 오지 않은 것**이다.

### ③ 같은 시점의 TLS 상태 — 1차와 동일

```text
$ openssl s_client -connect localhost:5180 -servername localhost
verify error:num=20:unable to get local issuer certificate
verify error:num=21:unable to verify the first certificate
Verify return code: 21 (unable to verify the first certificate)

$ curl https://localhost:5180/probe.html            → http=000        (시스템 신뢰만)
$ curl --cacert .dev-certs/dev-ca.pem …             → http=200 tls_verify=0   (대조군)
```

**대조군이 200 이라는 점이 핵심이다.** fixture·인증서 체인·양쪽 loopback 은 정상이고,
막는 것은 오직 **「시스템이 이 CA 를 모른다」** 하나다.

---

## 4. 커맨드 넷의 왕복 — **네 개 모두 미측정**

| 커맨드 | 성공/에러 | 사유 |
|---|---|---|
| `shell_info` | **미측정** | 문서가 안 열려 계측 페이지의 **자동 호출 자체가 일어나지 않았다** |
| `wake_guard_acquire` | **미측정** | 〃 (버튼 클릭이 필요하고, 그 이전에 페이지가 없다) |
| `wake_guard_release` | **미측정** | 〃 |
| `open_external` | **미측정** | 〃 |

**성공도 에러 원문도 없다.** 호출이 **실패한 것이 아니라 발생하지 않았다** — 이 둘을 구분해 적는다.
「에러 원문」을 요구받았으나 **지어낼 수 없는 자리**라 빈칸으로 둔다.

> 1차에서 평문 origin 으로 얻은 두 관측(**IPC 전역이 원격 문서에 주입된다** ·
> **ACL 이 허용 밖 origin 을 거절한다**)은 그대로 유효하다. 다만 그것은 M-1 의 통과가 아니다 —
> **허용 origin(https)에서의 왕복은 이번에도 재지 못했다.**

---

## 5. 판정 변화 — 없음

- **M-1**: `미측정` 유지
- **Phase 2 판정**: **보완(조건부)** 유지 — 근거(M-7 계약 어긋남)도 그대로다
- Phase 3 는 여전히 **조건부 진행 가능**이며, **M-1 을 닫기 전에는 Phase 3 완료기준을 닫지 않는다**

---

## 6. 다음에 필요한 것

신뢰 설치가 **실제로 반영**되어야 한다. 확인·설치 명령:

```bash
# 지금 상태 확인 (0건이면 미설치)
security find-certificate -a -c "SCAX WORK-006 probe local CA" | head

# 설치 (로그인 키체인)
security add-trusted-cert -d -r trustRoot -k ~/Library/Keychains/login.keychain-db \
  "/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects/frontend/.dev-certs/dev-ca.pem"

# 반영 확인 — 여기서 CSSMERR_TP_NOT_TRUSTED 가 사라져야 한다
security verify-cert -c \
  "/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects/frontend/.dev-certs/localhost.pem"
```

**짚어 둘 가능성 둘** (추측이며 관측이 아니다)

1. 설치 명령이 **다른 키체인/다른 사용자 컨텍스트**에서 실행됐을 수 있다
   (`sudo` 로 System 키체인에 넣었다면 `-k /Library/Keychains/System.keychain` 이 필요하고,
   이번 검색은 그쪽도 0건이었다)
2. **인증서를 다시 발급**했다면(`npm run probe:cert -- --force`) 이전에 신뢰시킨 CA 와
   지금 fixture 가 쓰는 CA 가 다를 수 있다. 현재 leaf 지문은 §2 에 적어 두었다

`verify-cert` 가 통과로 바뀐 뒤 같은 절차를 다시 돌리면 M-1 을 한 번에 닫을 수 있다.

---

## 7. 지시 준수 확인

| 지시 | 이행 |
|---|---|
| M-1 만 재측정 | 다른 M 항목을 다시 재지 않았다 |
| 기존 https fixture·셸 사용 | `vite.probe.config.ts` · `target/debug/scax-probe-shell` 그대로 |
| 신뢰 설치·변경 금지 | **하지 않았다.** `security` 는 조회 계열(`verify-cert`·`find-certificate`·`dump-trust-settings`)만 사용 |
| 코드/package/SPEC/WP 수정 금지 | **0줄.** 이번에 쓴 것은 문서 2개(측정 기록 갱신 + 이 보고서) |
| 무관한 앱이 담긴 스크린샷 금지 | **스크린샷을 한 장도 찍지 않았다.** 증거는 전부 텍스트 로그다 |
| 광범위 `pkill` 금지 · 내 PID 추적 | 내가 띄운 **31759(fixture) · 31890(shell)** 을 파일에 기록하고 **그 PID 만** `kill` 했다 |
| 내 프로세스 종료 | 둘 다 종료 확인 · **5180 listener 0** · 다른 vite 프로세스 0건 (남의 프로세스 건드리지 않음) |
| 커밋·push·Release 금지 | 하지 않았다 |
