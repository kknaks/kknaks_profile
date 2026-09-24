# WORK-006 Phase 2 — 1차 실측 기록 (fixture, R1)

> **이 문서는 「이렇게 관측했다」만 적는다.** 추측을 관측값으로 쓰지 않고, 재지 못한 것은
> `미측정` 또는 `검증 불가(장비 없음)`으로 남긴다. **자동 계측 성공으로 실기 항목을 덮지 않는다.**

- **측정 시각**: 2026-09-22 19:40 ~ 19:50 KST · **M-1 재측정 19:54 KST**(§M-1 재측정)
- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
  · 브랜치 `kknaksss/strong-hajin-projects` · **HEAD `a1f6791`** · 제품 코드 diff **0줄**
- **측정 대상**: Phase 1 탐침 셸(`target/debug/scax-probe-shell`) + 계측 페이지(`probe.html`)
- **OS 축**: macOS(실측 가능) · Windows(**장비 없음**)
- **측정 기기 OS**: macOS(Darwin 24.6.0) · arm64

---

## 0. 측정 환경과 그 한계 — 먼저 적는다

### 0-1. CA 신뢰가 설치되어 있지 않다 (M-1 의 전제)

```text
$ security find-certificate -c "SCAX WORK-006 probe local CA" ~/Library/Keychains/login.keychain-db
security: SecKeychainSearchCopyNext: The specified item could not be found in the keychain.

$ security verify-cert -c .dev-certs/localhost.pem
Cert Verify Result: CSSMERR_TP_NOT_TRUSTED
```

**워커는 신뢰 설치를 하지 않았다**(전역 보안 설정 변경 · 브리프 금지). TLS 우회도 만들지 않았다.

### 0-2. 이 기기는 이미 제3자가 절전을 붙들고 있다 (M-9 를 무효로 만든다)

```text
$ pmset -g custom                     $ pmset -g
AC Power:                              sleep  1 (sleep prevented by powerd, caffeinate, Amphetamine)
  sleep         1                      displaysleep 0 (display sleep prevented by Amphetamine)
  displaysleep  0

$ pmset -g assertions
  PreventUserIdleSystemSleep     1
  pid 357(powerd):      PreventUserIdleSystemSleep "Powerd - Prevent sleep while display is on"
  pid 28091(caffeinate):PreventUserIdleSystemSleep "caffeinate command-line tool"
  pid 72245(Amphetamine):PreventUserIdleSystemSleep "Amphetamine (Single-Use - System)"
```

→ §M-9 참조. **절전 설정을 바꾸지 않았다**(브리프 금지).

### 0-3. 평문 localhost 를 쓴 자리와 쓰지 않은 자리

- **M-1 에는 평문을 쓰지 않았다.** https fixture(`https://localhost:5180`)에서만 쟀다
- 웹 API 관측(M-2 ①)은 **평문 `localhost`** 에서 쟀다 — WORK Phase 1 작업 7 이
  「평문 `localhost` 스택은 M-2·M-4 의 마이크·녹음 전용(localhost 는 secure context)」로 허용한 자리다
- 평문 쪽은 **저장소 파일을 한 줄도 바꾸지 않고** 기존 개발 서버로 같은 `probe.html` 을 띄웠다
  (`npx vite` → 5173 점유 중이라 **5174**). 커맨드는 ACL 이 막는다(§M-1 의 `E-06` 관측)

---

## 1. 측정 요약 — OS 축별

| ID | 무엇 | macOS | Windows | 근거 절 |
|---|---|---|---|---|
| **M-1** | 원격 https 문서 ↔ 커맨드 왕복 | **미측정** (TLS 에서 멈춤) · **2026-09-22 19:54 재측정도 동일** | 검증 불가(장비 없음) | §M-1 · §M-1 재측정 |
| **M-2** | 녹음 포맷 (2경로 × 3갈래 = 6칸) | ①지원 **측정** / ②③ **미측정** | 검증 불가(장비 없음) | §M-2 |
| **M-2b** | 만료 넘겨 열린 스트림 유지 | **미측정** | 검증 불가(장비 없음) | §M-2b |
| **M-3** | 네비게이션 훅 발화 | **부분 측정** | 검증 불가(장비 없음) | §M-3 |
| **M-4** | 마이크 권한 프롬프트 | **미측정** (승인 대행 금지) | 검증 불가(장비 없음) | §M-4 |
| **M-5** | 웹뷰 쿠키·저장소 지속 | **미측정** | 검증 불가(장비 없음) | §M-5 |
| **M-6** | 창 닫기 되묻기 | **미측정** | 검증 불가(장비 없음) | §M-6 |
| **M-7** | 연결 실패를 셸이 감지하는가 | **측정 — 감지 수단 없음** | 검증 불가(장비 없음) | §M-7 |
| **M-8** | 외부 링크 | **미측정** (런타임) | 검증 불가(장비 없음) | §M-8 |
| **M-9** | 절전 방지의 경계 | **측정 불가(환경 무효)** | 검증 불가(장비 없음) | §M-9 |

> **Windows 는 한 칸도 실행하지 않았다.** 실기가 없다(OQ-W01). 또한 R2 검수 W-3 이 기록했듯
> **컴파일조차 검증되지 않았다**(호스트에 `llvm-rc` 없음 → `cargo check --target x86_64-pc-windows-msvc` 가
> 빌드 스크립트 단계에서 멈춘다). macOS 결과로 Windows 를 대신 쓰지 않는다.

---

## M-1 · 원격 https 문서에서 커맨드 왕복이 성립하는가 — **미측정**

### 잰 방법

```text
$ npm run probe:fixture            # https fixture (vite, 5180)
  ➜  Local:   https://localhost:5180/
  ➜  Loopback mirror: https://127.0.0.1:5180/

$ lsof -nP -iTCP:5180 -sTCP:LISTEN
  node  26495  IPv6  TCP [::1]:5180 (LISTEN)
  node  26495  IPv4  TCP 127.0.0.1:5180 (LISTEN)
```

**① fixture 에 닿는가 — 닿는다(양쪽 스택).** 검증을 켠 채(`-k` 없이 `--cacert`) 잰 값:

```text
https://localhost:5180/probe.html    http=200 tls_verify=0
https://127.0.0.1:5180/probe.html    http=200 tls_verify=0
https://[::1]:5180/probe.html        http=200 tls_verify=0
```

**② 시스템 신뢰만 쓰는 클라이언트가 보는 것 — 거절된다.**

```text
$ echo | openssl s_client -connect localhost:5180 -servername localhost
depth=0 CN=localhost
verify error:num=20:unable to get local issuer certificate
verify error:num=21:unable to verify the first certificate
Verification error: unable to verify the first certificate
Verify return code: 21 (unable to verify the first certificate)

$ curl https://localhost:5180/probe.html        # --cacert 없이
… establish a secure connection to it …          http=000
```

**③ 셸을 띄웠을 때 — 문서가 열리지 않았다.**

```text
$ ./target/debug/scax-probe-shell
[probe][boot] t=1790073952144 url=https://localhost:5180/probe.html nav_allow=["https://localhost:5180"]
[probe][nav]  t=1790073953119 navigate url=https://localhost:5180/probe.html origin=https://localhost:5180 allowed=true
(이후 아무 줄도 없다 — `[probe][load] started` 가 오지 않는다)
```

화면 관측: 창은 떴고 **내용이 빈 흰 화면**이다. 셸이 만든 안내도, 웹뷰 기본 오류 화면도 없다.

### 관측값

**커맨드 왕복을 한 번도 재지 못했다.** 네비게이션 훅까지는 발화했고(`allowed=true`) 그 다음
문서 로드가 시작되지 않았다.

### 원인 — 「연결 실패」가 아니라 「TLS 거절」로 좁혀진다

| 후보 | 배제 근거 |
|---|---|
| fixture 미기동·포트 오류 | `lsof` 로 두 주소 LISTEN 확인 |
| 주소 스택 불일치(IPv4/IPv6) | **양쪽 다 `http=200`** (R2 검수 W-1 수정으로 두 loopback 모두 열려 있다) |
| 인증서 자체가 깨짐 | `--cacert` 로는 `tls_verify=0` (정상 체인) |
| **CA 미신뢰** | `CSSMERR_TP_NOT_TRUSTED` · 로그인 키체인에 CA 없음 · 시스템 신뢰만 쓰는 클라이언트는 `verify error:num=20/21` 로 거절 |

> ⚠ **웹뷰가 낸 TLS 에러 «원문» 은 얻지 못했다.** 셸이 로드 실패를 관측할 수단이 없어서다
> (그 자체가 §M-7 의 결과다). 위 원문은 **같은 fixture 에 붙은 다른 클라이언트**(openssl·curl·
> `security verify-cert`)의 것이고, 웹뷰의 것이라고 쓰지 않는다.

### 곁가지로 얻은 것 — **구조적 전제 둘은 관측됐다**

평문 origin(`http://localhost:5174`)으로 같은 계측 페이지를 띄웠을 때:

- **IPC 전역이 원격 문서에 주입된다.** 계측 페이지의 「셸 전역 감지」가 **있음**으로 표시됐다.
  조사 §3-5 가 「단정하지 않는다」고 남긴 지점 — *원격 URL 에 `__TAURI_INTERNALS__` 가 오는가* — 은
  **온다**로 관측됐다
- **ACL 경계가 실제로 작동한다(`E-06` · AC-T24).** 그 문서의 `shell_info` 는 거절됐다:

  ```text
  shell_info not allowed on window "main", webview … allowed on: [windows: "main", URL: local],
  [windows: "main", URL: https://localhost:5180/*] … capability: probe-fixture,
  permission: allow-shell-info
  ```

  (가운데 일부는 캡처 시 OS 대화상자에 가려 읽지 못했다 — 가린 만큼만 `…` 로 표시한다)

**이 둘은 M-1 의 «통과» 가 아니다.** 허용 origin(https)에서의 왕복은 여전히 재지 못했다.
다만 **「원격 문서에 IPC 가 닿지 않는다」는 구조적 실패 시나리오는 관측되지 않았다.**

> 부수 관측: 위 거절 메시지에 `URL: local` 이 함께 보인다 — capability 의 `local` 기본값(`true`)이
> 살아 있다는 뜻이다. R2 검수 **W-6** 과 같은 사실이며 이번 범위에서 고치지 않았다.

### 닫는 방법 (사용자 1회 조작)

```bash
security add-trusted-cert -d -r trustRoot -k ~/Library/Keychains/login.keychain-db \
  "<워크트리>/frontend/.dev-certs/dev-ca.pem"
# 되돌리기: security remove-trusted-cert -d "…/dev-ca.pem"
```

---

### M-1 재측정 · 2026-09-22 19:54 KST — **여전히 미측정**

사용자가 **「로컬 CA 신뢰 설치를 마쳤다」**고 알려 와 M-1 만 다시 쟀다.
**결과는 1차와 같다 — 문서가 열리지 않았고 커맨드 왕복을 한 번도 재지 못했다.**

#### ① 신뢰 상태 먼저 확인했다 (읽기전용 · 아무것도 바꾸지 않았다)

```text
$ security verify-cert -c .dev-certs/localhost.pem
Cert Verify Result: CSSMERR_TP_NOT_TRUSTED

$ security find-certificate -a -c "SCAX WORK-006 probe local CA"      → 0건
$ security find-certificate -c "SCAX WORK-006 probe local CA" /Library/Keychains/System.keychain
security: SecKeychainSearchCopyNext: The specified item could not be found in the keychain.

$ security dump-trust-settings          (사용자 도메인)
SecTrustSettingsCopyCertificates: No Trust Settings were found.

$ security dump-trust-settings -d       (관리자 도메인) — 6건, 전부 무관한 제3자 CA
Cert 0: Dreamsecurity ROOT CA   Cert 1: iniLINE CrossEX RootCA2   Cert 2: VERAPORT-CA
Cert 3: 127.0.0.1               Cert 4: INTEREZEN CA              Cert 5: INNORIX.CA
```

leaf 를 직접 신뢰했을 가능성도 봤으나 `localhost` 이름의 인증서가 키체인에 **0건**이다
(우리 leaf 지문 `BD:7B:86:6C:75:EF:C0:64:39:CA:62:7A:60:20:C5:50:54:48:4C:3E`).

→ **이 기기에서 우리 CA 는 어느 키체인·어느 신뢰 도메인에도 없다.** 사용자 보고와 어긋난다.
그래도 **보고를 근거로 실측은 그대로 진행**했다(아래 ②③).

#### ② fixture 기동 — 정상

```text
$ node node_modules/vite/bin/vite.js --config vite.probe.config.ts     # PID 31759
  ➜  Local:   https://localhost:5180/
  ➜  Loopback mirror: https://127.0.0.1:5180/

$ lsof -nP -iTCP:5180 -sTCP:LISTEN -a -p 31759
node 31759 … IPv6 TCP [::1]:5180 (LISTEN)
node 31759 … IPv4 TCP 127.0.0.1:5180 (LISTEN)
```

#### ③ 셸 실행 — **nav 까지만. 문서가 열리지 않았다**

```text
$ ./target/debug/scax-probe-shell                                      # PID 31890
[probe][boot] t=1790074496110 url=https://localhost:5180/probe.html nav_allow=["https://localhost:5180"]
[probe][nav]  t=1790074496754 navigate url=https://localhost:5180/probe.html origin=https://localhost:5180 allowed=true

$ grep -c "probe\]\[load\]"  → 0        # 페이지 로드 사건 0건
$ grep -E "probe\]\[(ipc|wake)\]"  → (없음)   # 커맨드 실행 흔적 0건
```

14초 대기 후에도 추가 출력이 없었다(stdout·stderr 합쳐 위 두 줄이 전부).

#### ④ 같은 시점의 TLS 상태 — 1차와 동일

```text
$ openssl s_client -connect localhost:5180 -servername localhost
verify error:num=20:unable to get local issuer certificate
verify error:num=21:unable to verify the first certificate
Verify return code: 21 (unable to verify the first certificate)

$ curl https://localhost:5180/probe.html                  → http=000   (시스템 신뢰만)
$ curl --cacert .dev-certs/dev-ca.pem  …                  → http=200 tls_verify=0   (대조군)
```

**대조군이 200 이라는 것이 핵심이다** — fixture·인증서·양쪽 loopback 은 정상이고,
**막는 것은 오직 「시스템이 이 CA 를 모른다」 하나**다.

#### ⑤ 커맨드 넷의 왕복 — **네 개 모두 미측정**

| 커맨드 | 결과 | 왜 |
|---|---|---|
| `shell_info` | **미측정** | 문서가 안 열려 계측 페이지의 자동 호출이 일어나지 않았다 |
| `wake_guard_acquire` | **미측정** | 〃 (버튼 클릭이 필요하고, 그 이전에 페이지가 없다) |
| `wake_guard_release` | **미측정** | 〃 |
| `open_external` | **미측정** | 〃 |

**성공도 에러 원문도 없다.** 호출이 **발생하지 않았기 때문**이지 실패한 것이 아니다 —
이 둘을 구분해 적는다.

> 1차에서 평문 origin 으로 얻었던 두 가지(전역 주입됨 · ACL 이 origin 으로 거절함)는 그대로
> 유효하지만, **허용 origin(https)에서의 왕복은 이번에도 재지 못했다.**

#### ⑥ 판정 변화 — **없다**

M-1 은 **미측정**을 유지한다. 따라서 §판정의 결론도 그대로다 — **판정 게이트 미도달**
(운영 태세만 «조건부 보완»). Phase 2 Status 는 `IN_PROGRESS`.
**신뢰 설치가 실제로 반영된 뒤 다시 재야 한다.**

- 이번 회차에서 **신뢰를 설치하거나 바꾸지 않았다.** TLS 우회도 만들지 않았다
- 띄운 프로세스는 **내가 만든 둘(31759 · 31890)뿐**이고 **그 PID 만** 종료했다.
  종료 후 5180 listener 0 · 다른 vite 프로세스 0

---

## M-2 · 녹음 포맷 — **두 경로 × 세 갈래 = 6칸**

측정 방법: 탐침 셸(WKWebView) 안에서 계측 페이지가 `MediaRecorder.isTypeSupported` 를 호출한
결과를 화면에서 읽었다. **Safari 가 아니라 앱이 쓰는 시스템 웹뷰에서 잰 값이다.**

### macOS

| 경로 | ① 지원 여부 | ② 장시간 녹음 | ③ 서버 수용 |
|---|---|---|---|
| **회의 라이브** (`microphone.ts` 단일 MIME `audio/webm;codecs=opus`) | **지원** ✅ | **미측정** | **미측정** |
| **브라우저 인터랙션** (후보 셋) | **셋 다 지원** ✅ | **미측정** | **미측정** |

후보별 관측값 (화면 그대로):

```text
회의 라이브 (단일)   audio/webm;codecs=opus   지원
브라우저 후보 1      audio/webm;codecs=opus   지원
브라우저 후보 2      audio/webm               지원
브라우저 후보 3      audio/mp4                지원
브라우저 낙착        audio/webm;codecs=opus
```

**브라우저 경로는 후보가 내려앉지 않았다** — 1순위 그대로 낙착됐다.

### ②③ 이 미측정인 이유

- **② 장시간 녹음**: `getUserMedia` 가 필요하다 → OS 마이크 프롬프트 승인이 필요하고,
  **워커가 대신 승인하지 않는다**(브리프). §M-4 와 같은 이유다
- **③ 서버 수용**: 실제 녹음 산출물을 WS 스트림(회의) · 멀티파트 업로드(브라우저)로 보내야 한다.
  ② 가 막히면 보낼 원본이 없다

> **`isTypeSupported` 가 참인 것으로 M-2 를 닫지 않는다.** 위 표에서 ①만 채웠고
> ②③ 은 비운 채로 둔다. WORK 측정 규칙 그대로다.

### Windows

**검증 불가(장비 없음).** 6칸 전부 비어 있다.

---

## M-2b · 만료 시각을 넘겨 열린 스트림이 계속 도는가 — **미측정**

- 재려면 **살아 있는 회의 스트림**이 있어야 하고, 그러려면 ① 마이크 승인 ② 계측 화면 조작
  ③ 로컬 스택(API·워커·DB) 이 함께 필요하다. ①이 막혀 있어 성립하지 않는다
- 개발 DB 의 세션 행 `expires_at` 을 과거로 당기는 조작 자체는 가능하지만,
  **확인 대상(열린 스트림)이 없으면 무의미**하다. 제품 코드·비밀값·운영 DB 는 건드리지 않았다
- 막는 인수조건: **AC-T28**

---

## M-3 · 네비게이션 훅이 무엇에 발화하는가 — **부분 측정**

**재는 것은 「셸의 훅이 발화하는가」이지 점유가 남아 있는가가 아니다**(AC-T17).

### 측정된 것 ✅

**① 허용된 첫 이동 → 훅 발화 + 문서 교체 사건 발화**

```text
[probe][nav]  navigate url=http://localhost:5174/probe.html origin=http://localhost:5174 allowed=true
[probe][load] started  window=main generation=1 url=http://localhost:5174/probe.html
[probe][wake] cleanup  window=main cause=document-replaced(L-09) dropped=[] state=Off held=0
[probe][load] finished window=main url=http://localhost:5174/probe.html
```

→ `on_page_load` 의 `Started`·`Finished` 가 **둘 다 발화한다.** L-09 정리가 걸리고,
그 시점 점유가 0이라 `dropped=[]` 로 **아무것도 풀리지 않았다**(정상).

**② 허용 목록 밖 이동 → 취소되고, 아무것도 풀리지 않는다 (`E-05` · L-11)**

```text
$ SCAX_PROBE_NAV_ALLOW="https://example.invalid" … ./scax-probe-shell
[probe][nav] navigate url=http://localhost:5174/probe.html origin=http://localhost:5174 allowed=false
[probe][nav] blocked — 점유는 유지한다(L-11)
(`[probe][load]` 줄이 하나도 없다 · `[probe][wake] cleanup` 도 없다)
```

→ **막힌 이동은 문서 교체로 취급되지 않는다**(L-11 ✅). 해제 트리거가 아니다(I-4 방향 ✅).
셸은 그 주소를 기본 브라우저로 넘겼다.

### 미측정 ❌

**앱 안 화면 전환 · `replaceState` · `pushState` · 해시 변경 · 새로고침** — 계측 페이지의 버튼을
**클릭해야** 한다. 워커는 Tauri 창의 UI 를 조작할 수단이 없다(자동화 도구 없음).
**AC-T17 의 핵심(같은 문서 안 주소 변경이 문서 교체로 안 보이는가)은 아직 비어 있다.**

---

## M-4 · 마이크 권한 프롬프트 — **미측정**

- 재려면 `getUserMedia` 를 실제로 불러 **OS 프롬프트를 띄우고 승인**해야 한다.
  브리프가 「마이크 승인을 워커가 대신하지 않는다」로 못박았고, 몰래 수락하지 않았다.
  **프롬프트를 띄우는 것 자체도 하지 않았다**(사용자 화면에 대화상자를 남기게 된다)
- 전제조건 하나는 Phase 1 에서 이미 확인됐다 — 실행파일의 `__TEXT,__info_plist` 에
  `NSMicrophoneUsageDescription` 이 박혀 있다(R2 검수 R-6). **그러나 그것은 프롬프트가
  뜬다는 관측이 아니다**
- 막는 인수조건: **AC-T01**(그리고 M-2 ②③)

---

## M-5 · 앱 재시작 후 웹뷰가 저장소를 유지하는가 — **미측정**

- 재려면 ① 계측 페이지에서 표시용 쿠키 심기 버튼 클릭 ② 앱 완전 종료 ③ 재실행 후 다시 읽기 —
  **클릭 왕복**이 필요하다. UI 조작 수단이 없다
- 셸 쪽 전제는 코드로만 확인된다(`incognito(false)`). 관측값이 아니다
- 막는 인수조건: **AC-T26**

---

## M-6 · 웹의 창 닫기 되묻기가 앱 창 닫기에서 도는가 — **미측정**

- 재려면 ① `beforeunload` 가드 체크박스 클릭 ② 창 닫기 클릭 ③ 확인 창이 **하나만** 뜨는지 관찰.
  전부 UI 조작이다
- 막는 인수조건: **AC-T32 · AC-T38**

---

## M-7 · 연결 실패를 셸이 감지할 수 있는가 — **측정됨 · 감지 수단이 없다**

이번 회차에서 **대비가 선명하게 잡혔다.**

| 상황 | `[probe][nav]` | `[probe][load] started` | `[probe][load] finished` | 사용자에게 보이는 것 |
|---|---|---|---|---|
| **TLS 거절** (https, CA 미신뢰) | 발화 `allowed=true` | **없음** | **없음** | **빈 흰 창** |
| 정상 로드 (평문 5174) | 발화 `allowed=true` | 발화 | 발화 | 계측 페이지 |
| 허용 목록 밖 (`E-05`) | 발화 `allowed=false` | 없음 | 없음 | 빈 창(브라우저로 넘김) |

### 관측 결론

**지금 셸은 로드 실패를 관측할 수단이 없다.** `on_page_load` 는 실패 시 아예 발화하지 않으므로
「아직 안 왔다」와 「영영 안 온다」를 구분할 수 없고, **사용자에게는 빈 창만 남는다.**

- SPEC-006 **U-2**(연결 실패 화면)와 **AC-T31**(「빈 창이나 웹뷰 기본 오류 화면이 그대로
  노출되면 실패다」)을 **현재 구조로는 만족시킬 수 없다**
- SPEC U-2 가 「⚠ 실측 전제: 감지 수단이 없다고 판명되면 **구현 차단 사유**이고 조용히 빼지
  않는다」로 표시해 둔 바로 그 자리다
- **계약과 어긋나는 항목**이다 → 보완 조건 ①이 말하는 종류의 어긋남이다.
  다만 **그것만으로 「보완」 칸이 충족되지는 않는다** — 그 칸은 M-1 통과를 선행 전제로 단다(§판정)

### Phase 3 이 정해야 할 것

`on_page_load` 말고 실패를 받을 신호가 필요하다(웹뷰 로드 실패 콜백 · 네비게이션 응답 관측 등).
**수단 선택은 Phase 3 의 몫**이고, 이 문서는 「지금 것으로는 안 된다」까지만 적는다.

---

## M-8 · 외부 링크가 웹뷰에서 무엇을 하는가 — **런타임 미측정**

- 재려면 계측 페이지의 `target=_blank` 링크 · `open_external(http/https)` ·
  `open_external(file://)` 버튼을 **클릭**해야 한다. UI 조작 수단이 없다
- **간접 관측 하나**: `E-05` 경로에서 셸이 막은 주소를 기본 브라우저로 넘기는 코드 경로가
  실행됐다(§M-3 ②). 다만 **브라우저가 실제로 떴는지 확인하지 않았다** — 관측값으로 쓰지 않는다
- 스킴 경계(`http(s)` 만 허용 · `E-04`)는 **Rust 단위시험으로만** 확인돼 있다
  (`외부_링크는_http_와_https_만_받는다`). **이것은 코드 시험이지 런타임 측정이 아니다**
- 막는 인수조건: **AC-T21 · AC-T22**

---

## M-9 · 절전 방지가 실제로 자동 절전만 막는가 — **측정 불가(환경이 무효)**

### 숫자로 적는다 (브리프 규칙 4)

| 값 | 관측 |
|---|---|
| 설정된 자동 절전 대기시간 `T` (AC) | **1분** (`pmset -g custom` → `sleep 1`) |
| 요구 관찰 시간 `max(3T, 30분)` | **30분** |
| 실제 관찰 시간 | **0분 — 관찰하지 않았다** |

### 왜 무효인가

```text
$ pmset -g
 sleep  1 (sleep prevented by powerd, caffeinate, Amphetamine)

$ pmset -g assertions
 pid 357(powerd)       PreventUserIdleSystemSleep "Powerd - Prevent sleep while display is on"
 pid 28091(caffeinate) PreventUserIdleSystemSleep "caffeinate command-line tool"
 pid 72245(Amphetamine)PreventUserIdleSystemSleep "Amphetamine (Single-Use - System)"
```

**이 기기는 이미 제3자 셋이 `PreventUserIdleSystemSleep` 을 들고 있다.** 이 상태에서 기기가
잠들지 않는 것을 관찰해도 **우리 assertion 때문인지 Amphetamine 때문인지 가를 수 없다.**
AC-T01(잠들지 않는다) · AC-T02(화면은 꺼진다) · AC-T03(수동 잠자기는 막지 않는다) 어느 것도
이 환경에서는 성립을 증명하지 못한다.

또한 `displaysleep 0`(AC)이라 **AC-T02(화면은 평소대로 꺼진다)를 잴 기준 자체가 없다.**

**절전 설정과 제3자 도구를 건드리지 않았다**(브리프 금지). 재려면 사용자가
Amphetamine·caffeinate 를 내리고 `sleep`·`displaysleep` 을 의미 있는 값으로 두어야 한다.

- 막는 인수조건: **AC-T01 ~ AC-T04** (그리고 장시간 축 AC-T05~T07)

---

## 판정 게이트 (WORK-006 §Phase 2 표)

### 표의 조건과 대조

| 판정 | 표의 조건 (인용) | 이번 관측 |
|---|---|---|
| **진행** | 「M-1 왕복 성립(https fixture) **그리고** 회의 라이브 경로의 M-2 세 갈래 모두 통과」 | **미충족.** M-1 은 미측정이고, M-2 는 ①만 통과·②③ 미측정 |
| **중단** | 「M-1 왕복이 성립하지 않는다 **또는** 회의 라이브 경로가 대상 OS 에서 열리지 않는다」 | **미해당.** M-1 은 **「성립하지 않음」이 아니라 「재지 못함」**이다. 회의 라이브 단일 MIME 은 **지원으로 관측**됐다(닫히지 않았다) |
| **보완** | 「**위 둘은 통과했으나** ① M-3 ~ M-9 중 일부가 계약과 어긋난다 …」 — **M-1 통과 + M-2 회의 라이브 통과가 선행 전제** | **전제 미충족.** 어긋남 자체(M-7)는 관측됐으나, **M-1 이 미측정이라 이 칸에 들어갈 수 없다** |

### 결론: **판정 게이트 미도달** — 운영 태세만 «조건부 보완»

**M-1 이 미측정이라 표의 세 조건 중 어느 것도 충족되지 않았다.** 세 칸이 모두 M-1 의
«성립/불성립» 위에 서 있는데 이번 회차는 그 값을 얻지 못했다.

1. **진행 미충족.** M-1 통과를 요구하는데 통과가 없다. 자동 계측(M-2 ①)의 성공으로
   실기 항목을 덮지 않는다
2. **중단 미해당.** 중단은 *성립하지 않음이 관측된* 경우다. M-1 은 TLS 앞에서 멈춰
   **측정 자체를 못 했다.** 미측정을 실패로 바꿔 읽으면 「미실측을 통과로 쓰지 않는다」의
   **반대쪽 잘못**이 된다
3. **보완도 «충족»이 아니다.** 보완은 **「위 둘은 통과했으나」**를 선행 전제로 단다.
   어긋남(M-7)이 관측된 것은 사실이지만, **전제가 서지 않아 그 칸에 들어갈 수 없다**

> **그래서 이 회차를 「보완 조건을 충족했다」고 쓰지 않는다.** 판정은 **게이트 미도달**이고,
> **Phase 2 의 Status 는 `IN_PROGRESS`** 다. 게이트는 **M-1 을 실제로 잰 뒤에** 연다.
>
> 다만 **작업 태세**로는 «조건부 보완»을 취한다 — M-7 의 어긋남은 이미 확정 관측이라
> 구현 규칙으로 흡수하며 Phase 3 을 열 수 있다. **이는 표의 칸을 채웠다는 주장이 아니다.**

### Phase 1 「실패 시 다음 조치」 조항 — 왜 발동하지 않는가

WORK-006 §Phase 1 **작업 7** 은 이렇게 적는다:

> 커맨드 왕복 자체가 안 되면 → **그것이 곧 M-1 의 답이다.** Phase 2 로 넘기지 말고
> **즉시 판정 게이트**를 연다(원격 https 문서에 IPC 가 닿지 않으면 SPEC-006 의 구조가
> 성립하지 않는다 — 조사 §3-5 가 **단정하지 않은** 바로 그 지점이다)

**문자 그대로 읽으면 중단 쪽으로 끄는 조항**이라, 왜 해당하지 않는지 밝혀 둔다.
이 조항이 말하는 것은 **「왕복이 안 된다」**이고, 관측된 것은 **「왕복에 닿기 전에 막혔다」**다.

| # | 배제 근거 | 관측 |
|---|---|---|
| 1 | 멈춘 지점이 **IPC 이전(TLS)** 이다 | `[probe][nav] allowed=true` 까지 발화하고 문서가 오지 않았다(`[probe][load]` 0건). IPC 는 문서가 있어야 시작된다 |
| 2 | fixture·체인·경로는 **정상**이다 | 대조군 `curl --cacert` → `http=200 tls_verify=0` · 양쪽 loopback LISTEN. 막는 것은 「시스템이 이 CA 를 모른다」 하나 |
| 3 | **구조적 실패는 관측되지 않았다** | 평문 원격 origin 에서 `__TAURI_INTERNALS__` 주입 확인 · ACL 이 origin 으로 거절. 조사 §3-5 가 단정을 피했던 지점이 **긍정 쪽으로** 관측됐다 |

→ **「원격 https 문서에 IPC 가 닿지 않는다」가 관측된 적이 없다.** 그러므로 이 조항이 여는
즉시 판정 게이트는 **발동하지 않는다.** 동시에 **닿는다는 것도 관측되지 않았다** — 그래서
M-1 은 통과가 아니라 **미측정**이다.

### 다음에 할 일

| # | 할 일 | 주인 |
|---|---|---|
| 1 | **CA 신뢰 설치 후 M-1 재측정**(§M-1 의 명령) — 이것이 조건부를 푸는 열쇠 | 사용자 1회 조작 → 코디 |
| 2 | **M-7 어긋남을 구현 규칙으로 흡수** — 연결 실패 감지 수단을 Phase 3 이 정한다 | Phase 3 |
| 3 | 마이크 승인 후 **M-2 ②③ · M-4 · M-2b** 재측정 | 사용자 + 코디 |
| 4 | UI 조작이 필요한 **M-3 나머지 · M-5 · M-6 · M-8** 재측정 | 사용자 |
| 5 | 제3자 절전 도구를 내리고 `T` 를 정한 뒤 **M-9** 재측정 | 사용자 |
| 6 | Windows 실기 확보 시 **전 항목 Windows 축** (컴파일 포함) | OQ-W01 |

**브라우저 인터랙션 경로 — 절반만 배제됐다.** 표의 보완 ③은 **두 갈래**다
(「**후보 셋 전부 실패** 또는 **서버가 그 업로드를 거부**」).

- **앞 갈래(후보 실패)는 배제된다** — 후보가 내려앉지 않았고 1순위 그대로 낙착됐다(§M-2).
  보완 ②(후보가 내려앉음)도 같은 근거로 배제된다
- **뒷 갈래(서버 수용)는 «미측정»이라 아직 배제할 수 없다** — §M-2 의 ③ 칸이 비어 있다.
  「해당하지 않는다」가 아니라 **「판단할 값이 없다」**가 맞다

---

## 이 회차에서 하지 않은 것

- CA 신뢰 설치 · TLS 검증 무력화 · 마이크 승인 · 절전 설정 변경 · Windows 실기 조작
- 제품 코드 · `src-tauri` · package 파일 · SPEC/WP/index/log 수정 (**diff 0줄**)
- 커밋 · push · PR · Release
