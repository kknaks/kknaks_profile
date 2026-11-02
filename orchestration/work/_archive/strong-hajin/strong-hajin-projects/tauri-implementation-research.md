# Tauri 래퍼 적용 조사 — SPEC-006 의 설계 입력

> 읽기 전용 조사. 제품 코드를 고치지 않았고, 빌드·실행·컨테이너 기동을 하지 않았다.
> 앞 조사(`research-task-management-tauri.md`)를 반복하지 않는다. **DEC-005 가 방향 A 를 골랐을 때
> 비로소 열리는 빈칸** — 원격 origin 과 IPC, 절전 방지의 플랫폼 계약, 녹음 수명주기의 실제 상태 —
> 만 채운다.

> ⚠ **§10 을 먼저 보라 (2026-09-22 16시대 보강·정정).** SPEC-006 검수 뒤에 확인한 사실이 있고,
> 그중 하나(**macOS 의 WebM/Opus 녹음 지원**)는 §5-4 의 서술 전제를 바꾼다. §10 이 정본이고
> 아래 본문 중 §10 이 명시적으로 뒤집은 줄은 그쪽을 따른다.

## 0. 조사한 상태 — 기준 HEAD 와 조회 시각

| 대상 | 경로 | branch | HEAD | dirty | 조회 |
|---|---|---|---|---|---|
| 적용 코드 | `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` | `kknaksss/strong-hajin-projects` | `e46ce39c444ee4a5a69d1f8892d51916694fcc0a` | **69건 (작업 중)** | 2026-09-22 15:29 KST |
| 참조 코드 | `/Users/kknaks/git/toy_pr2/task_management` | `main` | `a720b6ef2c9d7dcfebc2595c4d00cb76621b01d8` | 0건 | 2026-09-22 15:33 KST |
| 문서 | `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin` | `kknaksss/strong_hajin` | `069c1ed2bca73dc4fb8b9a688f59064ca8d196bf` | 작업 중 | 2026-09-22 15:29 KST |

**적용 코드가 미커밋 작업 중이다.** 아래 인용은 그 작업 중 상태를 읽은 것이다. 인용한 자리
(`lib/api.ts` 의 `request()` · `stream.ts` · `microphone.ts` · `http_auth.py` · `settings.py`)는 계약에
해당해 잘 바뀌지 않지만, 구현 착수 시 다시 확인하는 편이 안전하다.

웹 리서치는 공식 문서(Tauri v2 · Microsoft Learn · MDN · Apple 오픈소스 헤더)로만 했고
각 사실에 URL 과 확인일을 붙였다. **실행해서 확인한 것은 하나도 없다** — §7 이 실측 미완 목록이다.

---

## 1. 요약 — 이 조사가 새로 세운 것 여덟

1. **방향 A 를 고르면 FE 의 same-origin 전제가 전부 그대로 성립한다.** 창의 문서 origin 이
   운영 https origin 그 자체라, 상대경로 `fetch` 9곳 · `credentials:'same-origin'` · `window.location.host`
   기반 WS 가 **한 줄도 안 바뀐다**(§2).
2. **바로 그 이유로 원격 페이지는 기본적으로 Tauri IPC 를 못 쓴다.** 커맨드를 열려면 capability 에
   `remote.urls` 를 명시해야 한다 — Tauri v2 공식 계약이다(§3-1).
3. **절전 방지의 플랫폼 계약이 DEC-005 D-03 과 정확히 맞는다.** macOS 의 idle-system-sleep 방지
   assertion 과 Windows 의 `ES_SYSTEM_REQUIRED|ES_CONTINUOUS` 는 둘 다 **화면 꺼짐을 허용하고
   수동 절전·덮개 닫기를 막지 않는다**(§4). D-03 이 요구한 경계가 API 경계와 같다.
4. **공식 Tauri 절전 방지 플러그인은 없다.** 커뮤니티 플러그인뿐이다(§4-3). 「플러그인 하나 붙이면
   된다」고 쓸 근거가 없다.
5. **웹 표준 Screen Wake Lock 은 이 문제의 답이 아니다** — 그것은 *화면*을 켜 두는 API 이고,
   DEC-005 는 화면 꺼짐을 허용한다(§4-4). 래퍼가 필요한 이유가 여기서 한 번 더 확인된다.
6. **녹음 수명주기에 「일시정지」가 없다.** 적용 코드의 회의 스트림은 주석과 계약 모두
   pause/resume 을 범위 밖으로 못박았고, 핸들에 `stop` 만 있다(§5-2). DEC-005 D-03 의
   「일시정지 시 해제」는 **아직 없는 상태를 가리킨다** — 조건부 계약으로 두어야 한다.
7. **녹음 표면이 둘이다.** 회의 라이브 업스트림과 브라우저 인터랙션 녹음. 둘째는 오디오를
   **메모리에 통째로 들고 있다가 종료 시에 올린다** — 절전으로 프로세스가 끊기면 잃는 양이 더 크다(§5-3).
8. **운영 프로파일에는 라우트가 하나도 없다.** `@app.` 데코레이터 160개 중 159개가
   `if settings.developer_auth_enabled:` 안이고, 밖에 있는 것은 `/health` 하나다(§6-1).
   **지금 코드로 `AX_PROFILE=PRODUCTION` 을 띄우면 로그인도 API 도 없다.**
   그런데 세션 쿠키의 `Secure` 는 **그 프로파일일 때만** 붙는다(§6-2) — 정면으로 부딪친다.

---

## 2. 방향 A 에서 FE 가 안 바뀌는 이유 — 표면 전수

DEC-005 D-01 은 배포된 HTTPS 웹을 Tauri 창에서 연다. 그러면 **문서의 origin 이
`tauri://localhost` 가 아니라 운영 https origin** 이다. 앞 조사가 「가장 큰 경계」로 꼽았던 인증·CORS
문제가 **발생하지 않는다.**

다음은 그 전제에 기대는 자리 전부다. 「N 곳만 고치면 된다」가 아니라 **전수를 세어 0 임을 보인다.**

### 2-1. HTTP — `fetch(` 호출 9곳, 전부 상대경로 + `same-origin`

`grep -rn 'fetch(' frontend/src` (테스트 파일 제외) 결과:

| 자리 | 내용 |
|---|---|
| `frontend/src/lib/api.ts:127` | 공용 `request<T>()` — `credentials: "same-origin"`, 경로는 호출자가 준 상대경로 |
| `frontend/src/lib/api.ts:103` | `stopBrowserRecording` — 멀티파트, `request()` 우회 |
| `frontend/src/lib/api.ts:118` | `uploadBrowserFile` — 멀티파트, `request()` 우회 |
| `frontend/src/lib/api.ts:277` | 업무 자료 업로드 |
| `frontend/src/lib/api.ts:568` | 업무 요청 자료 업로드 |
| `frontend/src/lib/api.ts:1022` | 자료 업로드 (공용 경로) |
| `frontend/src/lib/api.ts:1099` | 액션 자료 초안 파일 |
| `frontend/src/lib/api.ts:1346` | 회의 자료 업로드 |
| `frontend/src/lib/api.ts:1371` | 회의 자료 본문 읽기 — `credentials:"same-origin"` |

**아홉 곳이 전부 `frontend/src/lib/api.ts` 안에 있고, 전부 상대경로다.** 절대 URL 조립 지점도,
base URL 주입 지점도 없다. 방향 A 에서는 그대로 두는 것이 맞다 — 주소를 주입할 이유가 없다.

> 앞 조사가 「멀티파트가 `request()` 밖으로 샜다」고 지적한 것은 **방향 B(주소 주입)에서만 문제**다.
> 방향 A 에서는 아홉 곳이 같은 origin 을 보므로 샜다는 사실이 아무 대가를 만들지 않는다.
> 다만 훗날 주소를 주입할 일이 생기면 이 아홉 곳이 그대로 비용이다 — 기록해 둔다.

### 2-2. WebSocket — 1곳

`frontend/src/features/meetings/stream.ts:70-74`

```ts
export function meetingStreamUrl(meetingId: string): string {
  // 같은 오리진이라 세션 쿠키가 핸드셰이크에 실린다 — 토큰을 주소에 붙이지 않는다 (§5.3 인증).
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${protocol}//${window.location.host}/api/meetings/${meetingId}/stream`;
}
```

`new WebSocket(` 은 레포 전체에서 `stream.ts:96` 한 곳뿐이다. **https 로 열면 자동으로 `wss:` 가 된다** —
이미 그렇게 짜여 있다.

### 2-3. 네비게이션·딥링크

| 자리 | 코드 | 래퍼에서 생기는 일 |
|---|---|---|
| `frontend/src/App.tsx:60` | `new URLSearchParams(window.location.search).get('interaction')` | 앱 창이 `?interaction=` 이 붙은 주소로 열릴 수 있어야 딥링크가 산다 |
| `frontend/src/App.tsx:399` | `new URL(window.location.href)` | 같은 origin 안의 주소 조작. 그대로 성립 |
| `frontend/src/App.tsx:684` | `window.open(resource.origin, "_blank", "noopener,noreferrer")` | **외부 링크.** 웹뷰 안에서 열리면 앱 창이 남의 사이트가 된다 — §3-3 |
| `frontend/src/features/chat/AssistantMarkdown.tsx:42` | `window.location.origin` 을 base 로 상대 링크 해석 | 그대로 성립 |

백엔드가 만드는 딥링크는 `AX_WEB_ORIGIN + '/?interaction=' + id` 이고, `AX_WEB_ORIGIN` 은
**HTTP(S) origin 이어야 한다**고 검증한다 — `backend/src/ax_workspace/bootstrap/settings.py:97-111`.

```python
raise ... "AX_WEB_ORIGIN must be an HTTP(S) origin without credentials, path, query or fragment"
```

방향 A 는 이 검증을 그대로 통과한다. **방향 B 였다면 `tauri://localhost` 를 넣을 수 없어 딥링크를
따로 설계해야 했다** — 이 자리도 A 가 값을 치르지 않는 곳이다.

### 2-4. 브라우저 저장소

`localStorage` 사용처는 초안 2종뿐이고 토큰을 넣지 않는다(앞 조사 §4-3). 방향 A 에서
`localStorage` 는 **운영 https origin 에 매인다** — 즉 앱과 브라우저가 같은 서버를 보아도
**웹뷰의 저장소는 앱 컨테이너 안에 따로 있다.** 브라우저에서 쓰던 초안이 앱에 보이지 않는다.
DEC-005 가 다루지 않은 사실이라 SPEC 의 미결로 올린다.

---

## 3. 원격 origin 과 Tauri — 공식 계약

### 3-1. 원격 페이지는 capability `remote.urls` 없이는 커맨드를 못 부른다

Tauri v2 Capability 스키마 (확인 2026-09-22):

| 필드 | 공식 문서 문구 |
|---|---|
| `local` | "Whether this capability is enabled for local app URLs or not. Defaults to `true`." |
| `remote` | "Configure remote URLs that can use the capability permissions." |
| `remote.urls` | "Remote domains this capability refers to using the [URLPattern standard](https://urlpattern.spec.whatwg.org/)." |
| `windows` / `webviews` | "List of windows/webviews that are affected by this capability. Can be a glob pattern." |
| `platforms` | "Limit which target platforms this capability applies to." |

출처: <https://v2.tauri.app/reference/acl/capability/> · <https://v2.tauri.app/security/capabilities/> (확인 2026-09-22)

공식 예시가 보이는 모양:

```json
{
  "$schema": "../gen/schemas/remote-schema.json",
  "identifier": "remote-tag-capability",
  "windows": ["main"],
  "remote": { "urls": ["https://*.tauri.app"] },
  "permissions": ["nfc:allow-scan", "barcode-scanner:allow-scan"]
}
```

URLPattern 예시로 `https://*.mydomain.dev`(서브도메인) · `https://mydomain.dev/api/*`(하위 경로)가
문서에 있다. 문서가 같은 자리에서 경고한다 — **"Make sure you understand the security implications
of providing remote sources with local system access."**

> **설계 함의.** 방향 A 에서 커맨드를 여는 것은 「원격 문서에 네이티브 권한을 주는 일」이다.
> 그래서 SPEC-006 은 **여는 커맨드를 최소로 좁히고, `remote.urls` 를 운영 origin 하나로 고정**해야
> 한다. 와일드카드 서브도메인(`https://*.…`)은 그 서브도메인 전부를 신뢰한다는 뜻이라 쓰지 않는다.

또 하나 — 문서가 밝히는 플랫폼 한계: **"On Linux and Android, Tauri is unable to distinguish between
requests from an embedded `<iframe>` and the window itself."** (같은 출처). macOS·Windows 만 노리면
이 한계에 걸리지 않지만, 대상 OS(OQ-T01)가 열려 있으므로 기록해 둔다.

### 3-2. origin 혼동 취약점 — 2.11.1 미만을 쓰지 않는다

GHSA-7gmj-67g7-phm9 「Origin Confusion Allows Remote Pages to Invoke Local-Only IPC Commands」

| 항목 | 값 |
|---|---|
| 영향 | ">=2.0, <=2.11.0" |
| 패치 | ">=2.11.1" |
| 내용 | Windows·Android 에서 `is_local_url()` 이 첫 서브도메인만 보고 로컬로 판정. `http://app.evil.com/` 이 `app://` 스킴 앱의 로컬 검사를 통과 |
| 영향 대상 | **"Apps that load remote URLs in webviews with local-only IPC commands"** — 정확히 이번 방향이다 |

출처: <https://github.com/tauri-apps/tauri/security/advisories/GHSA-7gmj-67g7-phm9> (확인 2026-09-22)

참조 프로젝트가 핀한 버전은 **2.11.3**(`task_management/app/front/src-tauri/Cargo.toml:22`)이라
이미 패치 범위 안이다. **버전 하한을 계승 항목으로 명시하는 근거**가 된다.

### 3-3. 외부 링크를 밖으로 내보내는 공식 수단

`tauri-plugin-opener` 가 정의하는 권한(확인 2026-09-22, <https://v2.tauri.app/plugin/opener/>):

| 식별자 | 문서 문구 |
|---|---|
| `opener:allow-default-urls` | "This enables opening `mailto:`, `tel:`, `https://` and `http://` urls using their default application." |
| `opener:allow-open-url` | "Enables the open_url command without any pre-configured scope." |
| `opener:allow-open-path` | "Enables the open_path command without any pre-configured scope." |
| `opener:allow-reveal-item-in-dir` | "Enables the reveal_item_in_dir command without any pre-configured scope." |

JS API 는 `openUrl(url)` · `openPath(filePath, appName?)`. **path·url 양쪽 다 glob scope 로 좁힐 수 있다.**

> 설계 함의: 외부 링크에 필요한 것은 `open_url` 하나다. `open_path` · `reveal_item_in_dir` 은
> **파일 시스템 표면**이라 이번 범위에서 열 이유가 없다. 범용 `shell` 권한은 말할 것도 없다.

### 3-4. 네비게이션을 취소할 수 있다

`tauri::webview::WebviewWindowBuilder` (docs.rs, 확인 2026-09-22
<https://docs.rs/tauri/latest/tauri/webview/struct.WebviewWindowBuilder.html>):

```rust
pub fn new<L: Into<String>>(manager: &'a M, label: L, url: WebviewUrl) -> Self
pub fn on_navigation<F: Fn(&Url) -> bool + Send + 'static>(self, f: F) -> Self
```

`on_navigation` 문서 문구 — **"Defines a closure to be executed when the webview navigates to a URL.
Returning `false` cancels the navigation."**

그 밖에 같은 빌더가 가진 것 중 이번 설계에 닿는 것:

| 메서드 | 문서 문구 | 왜 관련 있나 |
|---|---|---|
| `incognito(bool)` | "Enable or disable incognito mode for the WebView." | **켜면 안 된다** — 쿠키가 안 남아 재시작마다 로그아웃 |
| `data_store_identifier([u8;16])` | "Initialize the WebView with a custom data store identifier. Can be used as a replacement for data_directory not being available in WKWebView." | 쿠키·저장소가 앉는 자리. macOS ≥14 · iOS ≥17 만 지원 |
| `initialization_script` | "…run after the global object has been created, but before the HTML document has been parsed…" | 셸 존재를 원격 문서에 알리는 자리로 쓸 수 있다 |

### 3-5. 원격 URL 과 IPC — **확정하지 않는다**

검색 중 `WebviewUrl::External` 사용 시 IPC 가 닿지 않는다는 취지의 미해결 이슈
(tauri-apps/tauri#15190, `tauri-cef` 문맥)와 `window.__TAURI__` 주입 요구 이슈(#5088)가 보였다.
**둘 다 내용을 끝까지 읽지 못했고**(이슈 본문 외 코멘트를 받지 못했다), 버전별 동작을 단정할 수 없다.

> **그러므로 이 조사는 「원격 https 문서에서 커맨드 호출이 된다」를 사실로 쓰지 않는다.**
> 공식 문서가 보증하는 것은 **ACL 에 `remote.urls` 라는 자리가 있다**는 것까지다.
> 실제 주입·호출 성립 여부는 **실측 항목**이고, SPEC-006 의 인수조건이 여기에 걸린다(§7 · OQ).

---

## 4. 절전 방지 — 플랫폼 계약

DEC-005 D-03 이 요구한 경계는 셋이다. ① 자동 절전을 막는다 ② **화면 꺼짐은 허용한다**
③ 수동 잠자기·덮개 닫기는 막지 않는다. 두 OS 의 공식 API 가 바로 그 경계를 갖는다.

### 4-1. macOS — IOPMAssertion

`IOKit/pwr_mgt/IOPMLib.h` (Apple 오픈소스 미러, 확인 2026-09-22
<https://github.com/opensource-apple/IOKitUser/blob/master/pwr_mgt.subproj/IOPMLib.h>):

| 상수 | 헤더 문구 |
|---|---|
| `kIOPMAssertionTypePreventUserIdleSystemSleep` | "Prevents the system from sleeping automatically due to a lack of user activity." |
| `kIOPMAssertionTypePreventUserIdleDisplaySleep` | "Prevents the display from dimming automatically." |
| `kIOPMAssertionTypePreventSystemSleep` | "Prevents the system from sleeping and allows the system to reside in Dark Wake for an arbitrary length of time." |
| `kIOPMAssertionTypeNoIdleSleep` | "The system will not idle sleep when enabled (display may sleep)." |
| `kIOPMAssertionTypeNoDisplaySleep` | "The idle display will not sleep when enabled, and consequently the system will not idle sleep." |

```c
IOReturn IOPMAssertionCreateWithName(CFStringRef AssertionType, IOPMAssertionLevel AssertionLevel,
                                     CFStringRef AssertionName, IOPMAssertionID *AssertionID);
IOReturn IOPMAssertionRelease(IOPMAssertionID AssertionID);
```

같은 헤더의 상세 설명(`kIOPMAssertPreventUserIdleSystemSleep` 쪽)이 **무엇을 막지 않는지**를 적는다 —
assertion 이 걸려 있어도 **화면은 dim 되고 잠들 수 있으며, 시스템은 덮개 닫기 · Apple 메뉴 ·
저전력 등 다른 사유로는 여전히 잠든다.**

> **고를 것은 `…PreventUserIdleSystemSleep` 이다.** `…NoDisplaySleep` 계열은 화면까지 켜 두므로
> DEC-005 D-03 의 「화면 꺼짐 허용」을 어긴다. `…PreventSystemSleep`(Dark Wake)은 더 센 것이라
> 이번 요구를 넘는다.

### 4-2. Windows — SetThreadExecutionState

Microsoft Learn, `winbase.h` (확인 2026-09-22
<https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate>):

| 플래그 | 문서 문구 |
|---|---|
| `ES_CONTINUOUS` (0x80000000) | "Informs the system that the state being set should remain in effect until the next call that uses **ES_CONTINUOUS** and one of the other state flags is cleared." |
| `ES_SYSTEM_REQUIRED` (0x00000001) | "Forces the system to be in the working state by resetting the system idle timer." |
| `ES_DISPLAY_REQUIRED` (0x00000002) | "Forces the display to be on by resetting the display idle timer." |
| `ES_AWAYMODE_REQUIRED` (0x00000040) | "Enables away mode. … should be used only by media-recording and media-distribution applications that must perform critical background processing on desktop computers while the computer appears to be sleeping." |

그리고 Remarks 가 못박는 두 문장 — **그대로 옮긴다**:

> "The **SetThreadExecutionState** function cannot be used to prevent the user from putting the computer
> to sleep. Applications should respect that the user expects a certain behavior when they close the lid
> on their laptop or press the power button."

> "Calling **SetThreadExecutionState** without **ES_CONTINUOUS** simply resets the idle timer; to keep the
> display or system in the working state, the thread must call **SetThreadExecutionState** periodically."

해제 방법도 문서 예제가 그대로 보인다 — `SetThreadExecutionState(ES_CONTINUOUS)` 를 단독으로 부른다.

> **고를 것은 `ES_CONTINUOUS | ES_SYSTEM_REQUIRED` 다.** `ES_DISPLAY_REQUIRED` 를 넣으면
> 화면이 안 꺼져 D-03 을 어긴다. `ES_AWAYMODE_REQUIRED` 는 「잠든 것처럼 보이면서 도는」 모드라
> DEC-005 가 요구하지 않은 것이고, 문서 스스로 휴대용 기기에는 쓰지 말라고 한다.
>
> ⚠ **상태가 스레드에 매인다.** "thread's execution requirements" 라는 파라미터 설명 그대로다 —
> 걸고 푸는 것이 **같은 스레드**여야 한다는 제약이 구현에 붙는다. 이것은 SPEC 의 계약이 아니라
> work 의 구현 규칙이다. 여기 적는 이유는 「커맨드 두 개면 끝」이라고 가볍게 잡지 않기 위해서다.

### 4-3. 공식 플러그인이 없다 — 검색 범위를 밝힌다

「Tauri v2 prevent sleep plugin」으로 검색해 나온 것은 전부 커뮤니티 크레이트다 —
`tauri-plugin-nosleep`(pevers) · `tauri-plugin-keepawake`(thewh1teagle) ·
`tauri-plugin-screen-wake-lock`(cijiugechu) · `tauri-plugin-keep-screen-on`.
`tauri-apps/plugins-workspace` 의 공식 플러그인 목록에 절전 방지가 없고, 본체 이슈
tauri-apps/tauri#3697 「[feat] Prevent device from sleeping」이 열려 있다. (확인 2026-09-22)

> 즉 **「공식 플러그인을 켠다」는 선택지가 없다.** 직접 짜거나 커뮤니티 플러그인을 고르는
> 판단이 필요하고, 그 판단은 SPEC 이 아니라 work 의 몫이다. SPEC 은 **계약(무엇이 언제 걸리고
> 언제 풀리나)만 고정**하고 수단을 지정하지 않는다.

### 4-4. 웹 표준 Screen Wake Lock 은 답이 아니다

MDN (확인 2026-09-22 <https://developer.mozilla.org/en-US/docs/Web/API/Screen_Wake_Lock_API>):

> "The **Screen Wake Lock API** provides a way to prevent devices from dimming or locking the screen
> when an application needs to keep running."

타입은 `"screen"` 하나뿐이고, **문서가 보이지 않게 되면 자동으로 풀린다** —
"Only active documents can acquire screen wake locks and previously acquired locks are automatically
released when document becomes inactive."

> 두 번 어긋난다. ① 막는 대상이 **화면**이라 DEC-005 의 「화면 꺼짐 허용」과 반대다.
> ② 시스템 잠자기를 막지 않는다. **웹만으로 이 문제를 풀 수 없다는 것**이 래퍼의 존재 이유이고,
> 이 사실이 그 근거다.

### 4-5. 마이크가 열리려면 secure context 여야 한다

MDN `getUserMedia` (확인 2026-09-22):

> "The `getUserMedia()` method is only available in secure contexts. … If a document isn't loaded in a
> secure context, the `navigator.mediaDevices` property is `undefined`, making access to `getUserMedia()`
> impossible." / "A secure context is, in short, a page loaded using HTTPS or the `file:///` URL scheme,
> or a page loaded from `localhost`."

DEC-005 가 **HTTPS 웹**을 전제한 것이 이 제약과 맞는다. 평문 `http://<LAN IP>` 로 띄우면
`navigator.mediaDevices` 가 아예 없어 `microphone.ts:30` 의 가드가 바로 걸린다.

---

## 5. 녹음 수명주기 — 지금 제품의 실제 상태

### 5-1. 두 표면

| 표면 | 파일 | 오디오가 가는 길 |
|---|---|---|
| **A. 회의 라이브 업스트림** | `frontend/src/features/meetings/stream.ts` + `microphone.ts` | `MediaRecorder` 250ms 청크 → 64KB 로 잘라 → WS 바이너리 프레임 → 서버 |
| **B. 브라우저 인터랙션 녹음** | `frontend/src/features/browser/BrowserRecordingPage.tsx` + `liveTranscription.ts` | `MediaRecorder` 250ms 청크 → **메모리 배열에 쌓기** → 종료 시 `Blob` 합쳐 멀티파트 업로드 |

**B 가 더 위험하다.** 녹음이 끝날 때까지 오디오가 브라우저 메모리에만 있다
(`liveTranscription.ts:17` `const parts: Blob[] = []`). 절전으로 세션이 끊기면 그 회차가 통째로 사라진다.
A 는 250ms 마다 서버로 나가므로 잃는 양이 마지막 몇 청크다.

### 5-2. 표면 A 의 상태와 전이 — pause 가 없다

`stream.ts:167-195` 의 `MeetingStreamState.phase` 는 **넷**이다 —
`"idle" | "connecting" | "live" | "closed"`. **`paused` 가 없다.**

`stream.ts:12-13` 주석이 계약을 못박는다:

> "**자동 재연결·재시도를 두지 않는다** (§5.2-7). 끊기면 그 사실을 그대로 드러낸다.
> 멈췄다 잇는 조작(pause·resume)은 데모 범위 밖이다."

`microphone.ts:19` 의 핸들도 `stop` 하나뿐이다 — `export type MicrophoneHandle = { stop: () => void };`

**마이크가 실제로 열리는 자리와 닫히는 자리 전수** (`stream.ts:236-332`):

| 사건 | 코드 | 마이크 |
|---|---|---|
| `enabled=false` | `:237-241` | 열리지 않음 / 이전 것은 cleanup 에서 닫힘 |
| 소켓 열림 → `auth` 프레임 | `:102-105` | 아직 안 열림 |
| `ready` 프레임 도착 + `effectiveRole==="upstream"` | `:247-259` | **`startMicrophone()` 호출 — 여기가 녹음 시작** |
| 마이크 거부·실패 | `:256-259` | 안 열림. `micDenied: true`. **화면은 계속 live** |
| 어떤 사유로든 소켓 닫힘 (`onClosed`) | `:317-319` | `microphone?.stop()` |
| 업스트림 자리를 남이 가짐(`taken`) | `:322` | `setTakenOver(true)` → effect 재실행 → cleanup 이 닫고 `subscribe` 로 다시 붙음(마이크 없음) |
| effect cleanup (언마운트 · `enabled`·`meetingId`·`role` 변경) | `:327-331` | `microphone?.stop(); socket.close()` |

닫힌 사유는 다섯 가지로 갈린다 (`closureOf`, `:81-87`) —
`ended`(1000) · `unauthorized`(4401) · `not_found`(4404) · `taken`/`stale_status`(4409) · `disconnected`(그 밖).

호출부 (`MeetingDetailPage.tsx:414-419`):

```ts
const stream = useMeetingStream({
  meetingId,
  role: canWriteMemo ? "upstream" : "subscribe",
  enabled: live && attendee,
  onClosed: onStreamClosed,
});
```

`hosting = live && canWriteMemo && !takenElsewhere` (`:434`) 가 「이 창이 회의를 이끄는 창인가」다.
회의 상태 enum 은 `scheduled | in_progress | summarizing | done | failed | cancelled`
(`frontend/src/lib/viewModels.ts:1060`).

> **그래서 D-03 의 「일시정지」는 지금 가리킬 상태가 없다.** SPEC-006 은
> ① 있는 상태(시작·종료·실패·역할 상실·화면 이동)에 대해서는 **확정 계약**을 쓰고
> ② 일시정지·재개에 대해서는 **조건부 계약**으로 쓰되 「그 기능이 생기면」을 명시해야 한다.
> 없는 기능을 있는 것처럼 계약에 넣으면 인수조건을 통과시킬 방법이 없다.

### 5-3. 표면 B 의 상태 — 이미 `beforeunload` 가드가 있다

`BrowserRecordingPage.tsx`:

| 자리 | 코드 | 내용 |
|---|---|---|
| `:20` | `const blocked = busy \|\| session !== null;` | 녹음 중이거나 처리 중 |
| `:22-27` | `window.addEventListener('beforeunload', guard)` | **녹음 중 창을 닫으려 하면 브라우저가 되묻는다** |
| `:28` | `useEffect(() => () => { void capture.current?.stop()… }, [])` | 언마운트 시 마이크 해제 |
| `:48-70` | `start()` | `startBufferedAudioCapture()` → `startBrowserRecording()`. 실패 시 `denied`/`unsupported`/`failed` 로 서버 상태를 되돌린다 |
| `:72-87` | `stop()` | `session.stop()` 으로 Blob 확정 → 업로드. **업로드 실패해도 Blob 을 붙들고 재시도할 수 있다**(`original.current ??=`) |
| `:89-102` | `interrupt()` | 취소·실패 |
| `:30-44` | 2초 폴링 | 서버 상태가 `recording`/`upload_failed` 를 벗어나면 캡처를 닫는다 |

상태 라벨은 `:5-8` 에 여덟 개 —
`waiting` · `recording` · `upload_failed` · `completed` · `denied` · `cancelled` · `failed` · `unsupported`.

> **`beforeunload` 는 Tauri 창 닫기에서 도는가?** 확인하지 못했다. Tauri 는 창 닫기를
> `on_window_event` 의 `CloseRequested` 로 다루고, 웹 문서의 `beforeunload` 가 그 경로에서
> 발화하는지는 **실측 항목**이다. 발화하지 않으면 **녹음 중 창을 닫아도 아무 경고 없이 오디오가
> 사라진다** — 표면 B 는 메모리에만 있으므로 손실이 크다. SPEC 의 계약 항목으로 올린다.

### 5-4. 음성 입력 — 두 제품의 차이 (코디 비교 노트 확인 및 보강)

`orchestration/work/strong-hajin-projects/tauri-audio-comparison-note.md` 의 비교를 코드로 재확인했다.
**일치한다.** 아래는 그 위에 SPEC 이 걸어야 할 지점을 덧붙인 것이다.

| 축 | 참조 (task_management) | **적용 (Strong Hajin)** |
|---|---|---|
| 파일 | `app/front/src/features/meetings/hooks/audioCapture.ts` | `frontend/src/features/meetings/microphone.ts` |
| mime 선택 | `["audio/webm;codecs=opus","audio/webm","audio/mp4","audio/ogg;codecs=opus"]` 를 `isTypeSupported` 로 훑어 **첫 지원 포맷**. 하나도 없으면 브라우저 기본값 (`:22, :39-44`) | **`audio/webm;codecs=opus` 고정.** 후보도 `isTypeSupported` 도 없다 (`:17, :37`) |
| 선언 | `{ format: "auto", sampleRate: 48000, channels: 1 }` (`:16`) — "컨테이너 헤더가 형식을 말한다" | `{ format: "webm/opus", sampleRate: 16000, channels: 1 }` (`:11`) |
| 장치 요청 | `{ audio: true, video: false }` (`:36`) | `{ audio: { channelCount: 1, sampleRate: 16000 } }` (`:31`) — **요청이지 보장이 아니다** |
| 청크 | 250ms (`:19`) | 250ms + **64KB 초과분 분할** (`:14, :22-26`) |
| 핸들 | `pause()` · `resume()` · `stop()` · `stream` (`:24-29`) | **`stop()` 뿐** (`:19`) |
| 트랙 해제 | `releaseMicrophone()` 별도 (`:84-88`) + 트랙 `ended` 감지 | `stop()` 안에서 함께 (`:32-34, :50-53`) |
| 시스템 오디오 | 안 만든다 (`:4`) | 안 만든다 (`:4`) — **양쪽 같다** |

**실패가 갈리는 자리.** 적용 코드는 `new MediaRecorder(stream, { mimeType: "audio/webm;codecs=opus" })`
가 던지면 마이크를 놓고 그대로 예외를 올린다(`microphone.ts:36-41`). 그 예외는 `stream.ts:256-259`
에서 잡혀 **`micDenied: true`** 가 된다 — 화면은 「live」인 채로 남고 스크립트만 안 올라간다.
즉 **포맷 미지원과 권한 거부가 화면에서 같은 결과로 보인다.**

> macOS WKWebView 가 `audio/webm;codecs=opus` 를 `MediaRecorder` 로 지원하는지 **확인하지 않았다.**
> 실행하지 않았고, 웹 문서로도 Tauri 웹뷰의 동작을 단정할 수 없다. **실측 전까지 「macOS 앱에서
> 회의 라이브 녹음이 된다」고 쓰지 않는다.** 이것이 SPEC-006 의 가장 큰 차단 요인이다.

**포맷 fallback 은 FE 한 줄이 아니다.** 후보 목록을 넣는 순간 따라오는 것:
① 첫 프레임의 `audio.format` 선언값이 달라진다 → ② 서버가 그 값을 STT provider 설정으로 옮긴다
(`microphone.ts:6-7` 주석: "서버가 provider 설정에 옮긴다") → ③ 서버가 원본을 저장하는 확장자
(앞 조사: `STORAGE_ROOT/recordings/{id}.{ext}` append)가 달라진다.
**FE·BE·저장 세 곳이 같이 움직인다.** SPEC-006 은 이 변경을 **자기 범위로 삼지 않고** 의존으로만 적는다.

표면 B 는 이미 후보 목록(`webm/opus` → `webm` → `mp4`)을 갖고 있다(`liveTranscription.ts:13-15`).
**같은 앱 안에서 두 녹음 경로의 포맷 정책이 다르다** — 사실로 기록한다. 통일은 이번 범위가 아니다.

---

## 6. 운영 프로파일과 세션 — 두 개의 부딪침

### 6-1. 운영 프로파일에는 라우트가 없다

`backend/src/ax_workspace/entrypoints/http.py` 의 `create_app()` 을 세었다.

```text
@app.  데코레이터 총 160개
  들여쓰기 8칸 158개 ┐
  들여쓰기 12칸  1개 ┘ → 전부 `if settings.developer_auth_enabled:` 블록 안 (:606)
  들여쓰기  4칸  1개   → `@app.get("/health")` (:2530) — 유일하게 블록 밖
```

`developer_auth_enabled` 는 `DEVELOPMENT` 또는 `TEST` 다 (`bootstrap/settings.py:125-126`).
`local_login_enabled` 는 `PRODUCTION 이 아닐 때` 다 (`:129-131`). 그리고 `/api/auth/providers` 는
`{"local": …, "oidc": False}` 를 돌려준다 (`http.py:619`) — **OIDC 경로는 코드에 없다.**

> **결론: 지금 코드로 `AX_PROFILE=PRODUCTION` 을 띄우면 `/health` 하나만 있는 서버가 된다.**
> 로그인도, 회의도, 업무도 없다. **development/test 프로파일을 운영 대안으로 승인하지 않는다**는
> 브리프의 요구는 이 사실 위에 선다 — 지금은 **어느 쪽도 운영 요건을 만족하지 못한다.**
> 무엇을 할지는 사용자 결정이다(OQ-T02).

### 6-2. `Secure` 쿠키와 운영 프로파일이 서로를 막는다

`backend/src/ax_workspace/entrypoints/http_auth.py`:

```python
SESSION_COOKIE = "scax_session"        # :21
SESSION_MAX_AGE = 12 * 60 * 60         # :22  = 12시간

def cookie_secure(settings: Settings) -> bool:
    return settings.profile == RuntimeProfile.PRODUCTION      # :106-107
```

`http.py:639-646` 의 로그인 응답:

```python
response.set_cookie(
    SESSION_COOKIE, str(session_id),
    max_age=SESSION_MAX_AGE, httponly=True, samesite="lax",
    secure=cookie_secure(settings), path="/",
)
```

| 속성 | 값 | 래퍼에 주는 뜻 |
|---|---|---|
| `HttpOnly` | True | JS 가 못 읽는다. **키체인에 옮길 수 없다** — D-02 의 「키체인 전환 안 함」과 결이 같다 |
| `SameSite` | `lax` | 같은 origin 이라 문제 없음. cross-site POST 에 안 실려 CSRF 기본 방어가 된다 |
| `Secure` | **`PRODUCTION` 일 때만** | **HTTPS 로 띄우는데 운영 프로파일을 못 쓰면 `Secure` 가 안 붙는다** |
| `Max-Age` | 12시간 | 세션 쿠키가 아니라 **영속 쿠키**다 — 창을 닫아도 만료 전까지 남는다 |
| `path` | `/` | 전 경로 |

**부딪침.** §6-1 이 보였듯 `PRODUCTION` 에는 로그인 라우트가 없다. 그러면 `Secure` 를 붙일 방법이
현재 코드에 없다. HTTPS 배포에서 `Secure` 없는 세션 쿠키는 평문 경로로 샐 수 있는 자리를 남긴다.
**SPEC 의 계약으로 「운영 배포의 세션 쿠키는 Secure 여야 한다」를 쓰고, 지금 코드가 그 조건을
만족하지 못한다는 사실을 미결로 올린다.** 조용히 넘기지 않는다.

### 6-3. 세션 수명 — 12시간, 슬라이딩 없음

`backend/src/ax_workspace/platform/auth_sessions.py`:

```python
DEFAULT_SESSION_TTL = timedelta(hours=12)                                      # :12
record = AuthSessionRecord(..., expires_at=now + self._ttl)                    # :22
if expires_at <= now: return None                                              # :35-36
```

**`member_for()` 는 `expires_at` 을 늘리지 않는다.** 로그인 시각에서 12시간이 지나면,
쓰고 있는 중이어도 끊긴다.

| 축 | 값 | 근거 |
|---|---|---|
| 쿠키 만료 | 로그인 + 12h | `SESSION_MAX_AGE` |
| 서버 세션 만료 | 로그인 + 12h, **갱신 없음** | `DEFAULT_SESSION_TTL` · `member_for` |
| 만료 시 REST | 401 `"로그인이 필요합니다."` | `http_auth.py:79` |
| 만료 시 WS | close `4401` → `{kind:"unauthorized"}` → `onSessionLost()` | `stream.ts:83` · `MeetingDetailPage.tsx:410` |

> **OQ-T04 의 절반은 이걸로 답이 난다** — 제품이 정한 로그인 유지는 **12시간 고정**이다.
> 남는 것 둘: ① 앱 재시작 후에도 웹뷰가 그 쿠키를 들고 있나(**실측**) ② 12시간이 사용자가
> 원하는 값인가(**사용자**). 12시간을 「앱이라서 더 길게」로 바꾸는 것은 제품 결정이라
> 이 조사가 정하지 않는다.
>
> 그리고 **녹음 중 만료가 실재한다** — 12시간 연속 회의는 없겠지만, 로그인 후 11시간 59분에
> 시작한 회의는 1분 뒤 `4401` 로 끊긴다. 수명주기 계약이 다뤄야 할 경계다.

### 6-4. CORS·정적 서빙 — 방향 A 에서 달라지는 것

- **CORS 미들웨어는 여전히 없다** (`http.py` 에서 `CORS|add_middleware|StaticFiles|mount` grep → 0 hit).
  방향 A 에서는 **필요 없다.** 앱 창의 문서와 API 가 같은 origin 이다.
- **SPA 를 서빙할 자리는 여전히 없다.** 방향 A 는 **이것을 피해 갈 수 없다** — 창이 열 https 주소가
  실재해야 하고, 그 주소가 SPA 를 내야 한다. 방향과 무관하게 정해야 한다는 앞 조사의 결론이
  방향 A 에서는 **선행 조건**으로 승격한다. 이 작업은 SPEC-006 의 범위가 아니라 **전제**다(OQ-T02).
- **CSP.** 참조 프로젝트는 `tauri.conf.json` 의 `csp` 에 API 주소를 박았다
  (`connect-src 'self' ipc: … http://localhost:8000 ws://localhost:8000`). 그 설정은
  **Tauri 가 서빙하는 문서**에 거는 것이다. 방향 A 의 문서는 원격 서버가 내므로
  **CSP 도 서버 응답 헤더가 정한다.** 참조의 「CSP 에 주소를 박고 서버 변경 화면을 없앤다」 짝은
  **그대로 넘어오지 않는다.** 계승 항목에서 빼야 할 자리다.

---

## 7. 실측하지 않은 것 — 보장으로 쓰지 않는다

실행·빌드·설치를 하나도 하지 않았다. 아래는 **문서로 답할 수 없고 실물에서만 답나는** 목록이다.
SPEC-006 의 인수조건은 이 목록을 「검증 절차」로 쓰고, **통과했다고 미리 쓰지 않는다.**

| # | 실측 항목 | 걸려 있는 계약 |
|---|---|---|
| M-1 | 원격 https 문서에서 Tauri 커맨드 호출이 성립하는가 (`remote.urls` 설정 시) | 절전 방지 전체 · §3-5 |
| M-2 | macOS WKWebView 에서 `MediaRecorder` 가 `audio/webm;codecs=opus` 를 지원하는가 | **회의 라이브 녹음 전체** · §5-4 |
| M-3 | macOS 앱 창에서 `getUserMedia` 권한 프롬프트가 뜨는가 (Info.plist 병합 · 미서명 빌드) | 녹음 시작 |
| M-4 | Windows WebView2 에서 마이크 권한 핸들러 없이 `getUserMedia` 가 실패하는가 (참조 `lib.rs:49-88` 이식 필요 여부) | 녹음 시작 (OQ-T01 대상일 때) |
| M-5 | 앱 재시작 후 웹뷰가 `scax_session` 쿠키를 유지하는가 | 로그인 유지 · OQ-T04 |
| M-6 | 문서의 `beforeunload` 가 Tauri 창 닫기에서 발화하는가 | 녹음 중 창 닫기 · §5-3 |
| M-7 | 원격 서버에 닿지 않을 때 창이 무엇을 보이는가 (웹뷰 기본 오류 화면 / 빈 창) | 오프라인 계약 |
| M-8 | `window.open(…, "_blank")` 가 Tauri 웹뷰에서 무엇을 하는가 (새 웹뷰 / 무반응 / 외부 브라우저) | 외부 링크 · `App.tsx:684` |
| M-9 | 절전 방지가 실제로 자동 절전을 막고, 화면은 꺼지며, 수동 잠자기는 되는가 (OS 별) | D-03 인수조건 |
| M-10 | 재설치·업데이트 후 웹뷰 데이터 저장소(쿠키·localStorage)가 남는가 | 설치 계약 · OQ-T03 |

---

## 8. 조사의 한계

- **적용 코드가 dirty(69건)** 다. 작업 중 파일을 읽었다. §0 의 HEAD 와 시각이 기준이다.
- **부재 주장에는 검색 범위를 붙였다** — `fetch(`·`new WebSocket`·`@app.`·`CORS|add_middleware|StaticFiles|mount`
  는 전부 경로와 제외 범위를 §2·§6 에 적었다.
- **실행하지 않았다.** §7 이 그 목록이다.
- **Tauri 의 원격 URL + IPC 동작을 단정하지 않았다**(§3-5). 이슈 본문 외 코멘트를 받지 못했고,
  버전별 차이를 확인할 방법이 문서 조사 범위에 없었다.
- **`.env`·인증서·키 파일을 열지 않았다.** 환경변수는 **이름**만 인용했다(`AX_PROFILE` · `AX_WEB_ORIGIN`).
- **대상 OS·운영 주소·배포 채널·서명 신원을 발명하지 않았다.** 전부 OQ 로 남겼다.

---

## 9. OQ-T01~06 의 처분 — 근거로 닫히는 것과 사람이 정할 것

| OQ | 근거로 닫히는 부분 | 사람이 정할 부분 | 구현 차단 범위 |
|---|---|---|---|
| **OQ-T01** 지원 OS·설치파일 형식 | 없음. 참조의 macOS·Windows 를 자동 확정하지 않는다 | **전부 사용자.** Windows 를 넣으면 WebView2 마이크 핸들러(참조 `lib.rs:49-88`)와 `http://tauri.localhost` origin 이 따라온다 | 빌드 타겟·플랫폼별 권한 코드·검증 매트릭스 전부 |
| **OQ-T02** 운영 주소·프로파일·인증 | **닫힘(사실):** `PRODUCTION` 에는 `/health` 외 라우트가 없고 OIDC 경로가 코드에 없다(§6-1). `Secure` 쿠키는 그 프로파일에서만 붙는다(§6-2). SPA 서빙 자리가 없다(§6-4) | **무엇을 할지는 사용자·코디.** 운영 프로파일을 열 것인지, 인증을 어떻게 증명할 것인지, 주소는 무엇인지 | **창이 열 주소가 없으면 아무것도 못 한다.** 셸 설정·capability `remote.urls`·인수조건 전부 차단 |
| **OQ-T03** 게시·서명·공증·업데이트 | **닫힘(사실):** 참조에 서명·공증·자동업데이트·CI 가 0건이라 계승할 선례가 없다(앞 조사 §3-6) | **전부 사용자·코디** | 릴리즈 검증 기준·배포 절차 문서. **앱이 도는 것 자체는 안 막는다** |
| **OQ-T04** 로그인 유지 기간 | **절반 닫힘:** 제품이 정한 값은 **12시간 · 슬라이딩 없음**(§6-3) | ① 웹뷰 쿠키 지속은 **실측**(M-5) ② 12시간을 바꿀지는 **사용자** | 「재시작 후 로그인 유지」 인수조건만. 나머지는 안 막힌다 |
| **OQ-T05** 녹음 중 창 닫기·종료·실패 | **대부분 닫힘:** 있는 상태와 전이를 전수로 세었다(§5-2·§5-3). 절전 방지의 획득·해제 지점을 그 위에 얹을 수 있다 | ① **일시정지·재개를 만들 것인가**(지금 없다) — 사용자 ② 창 닫기 되묻기는 **실측**(M-6) | 일시정지 관련 계약만 조건부. 시작·종료·실패·역할 상실은 지금 확정 가능 |
| **OQ-T06** 네이티브 기능·허용 origin·버전 호환 | **대부분 닫힘:** 여는 커맨드를 최소로 좁히는 설계가 가능하고(§3-1·§3-3), `on_navigation` 으로 경계를 칠 수 있다(§3-4). 버전 하한은 2.11.1 이상(§3-2) | 허용 origin 의 **값**은 OQ-T02 에 매여 있다 | origin 값만. 계약의 **모양**은 지금 확정 가능 |

**요약 — SPEC-006 이 지금 확정할 수 있는 것:** 셸↔웹 인터페이스의 모양, 절전 방지의 수명주기
계약(일시정지 제외), 네비게이션·외부 링크 경계, 에러·경계 matrix, 쿠키 계약의 요건.
**gate 로 남겨야 하는 것:** 운영 origin 값(OQ-T02), 대상 OS(OQ-T01), 배포·서명(OQ-T03),
일시정지 계약(OQ-T05), 그리고 §7 의 실측 전부.

---

## 10. 보강·정정 — 2026-09-22 16시대 (SPEC-006 검수 이후)

SPEC-006 v0.1.0 검수(`review-tauri-spec-report.md`)가 제기한 지적을 **코드와 공식 문서로 직접
다시 확인**했다. 확인 시각 기준을 새로 적는다 — 적용 코드는 **같은 HEAD `e46ce39c`** 이나
**dirty 가 69 → 72 건**으로 늘었다(2026-09-22 16:01 KST 관측). 여전히 작업 중인 트리다.

### 10-1. 정정 ① — macOS 의 WebM/Opus 녹음은 **이제 지원된다**

**뒤집는 대상**: §5-4 말미의 「macOS WKWebView 가 `audio/webm;codecs=opus` 를 지원하는지
확인하지 않았다」는 서술 자체는 틀리지 않았다(확인하지 않은 것이 맞다). **그러나 그 빈칸을
「WebKit 은 MP4/AAC 만 낸다」는 2020년대 초 문서로 메우려는 판단은 낡았다.**

> *"MediaRecorder in WebKit for Safari 18.4 now supports creating WebM files using the Opus audio
> codec and either VP8 or VP9 for video."*
> — <https://webkit.org/blog/16574/webkit-features-in-safari-18-4/> (확인 2026-09-22)

용례로 *"This makes it possible for web apps that record audio, including popular podcasting apps,
to save WebM files via the MediaRecorder API."* 를 든다.

> ⚠ **2026-09-22 재정정 — 적용 범위를 원문보다 좁게 적었다.** 위 문단의 초판은 적용 범위를
> 「iOS/iPadOS 18.4 · macOS Sequoia 15.4 · visionOS 2.4」로 썼는데, **macOS Sonoma·Ventura 가 빠졌다.**
> 같은 글의 문장은 이렇다 —
> *"Safari 18.4 is available on iOS 18.4, iPadOS 18.4, macOS Sequoia 15.4, **macOS Sonoma,
> macOS Ventura**, and in visionOS 2.4."* (같은 URL 재확인 2026-09-22)
> 방향이 **유리한 쪽으로** 틀렸지만, OQ-T07 이 「대상 기기의 OS 판이 무엇인가」인 이상
> **대상 기기가 더 넓다**는 사실이 실측 계획에 그대로 들어가야 한다.

**그렇다고 「Safari 18.4 가 깔려 있으면 된다」로 넓히지 않는다.** 앱이 쓰는 것은 Safari 가 아니라
**시스템 웹뷰**다. ① 그 웹뷰가 어느 WebKit 판을 쓰는지 ② 그 판이 **정확히 어떤 MIME 문자열**에
참을 답하는지는 **확인하지 않았다.** Safari 설치 여부로 웹뷰의 판이나 지원 MIME 을 단정하지 않는다.

WKWebView 는 시스템 WebKit 을 쓴다. 따라서 **「WebKit 이 할 수 있나」는 더 이상 열린 질문이 아니고,
「대상 기기의 OS 판이 무엇인가」로 바뀐다.**

> Apple 의 Safari 18.4 릴리즈 노트 페이지도 확인을 시도했으나 **본문을 받지 못했다**
> (<https://developer.apple.com/documentation/safari-release-notes/safari-18_4-release-notes>,
> 제목만 반환). 그래서 근거는 WebKit 블로그 하나다 — 두 출처로 교차 확인하지 못한 것을 밝힌다.

**그래도 실측이 없어지지 않는다.** 세 가지를 함께 재야 한다:
① 대상 OS·웹뷰 판에서 `MediaRecorder.isTypeSupported("audio/webm;codecs=opus")` 가 참인가
② **장시간** 녹음이 끊기지 않고 나오는가 ③ **서버가 그 원본을 그대로 받아들이는가**.
①이 참이어도 ②·③이 자동으로 따라오지 않는다.

**포맷 후보 도입(fallback)의 지위도 정정한다.** 「무조건 별도 spec 이 필요하다」가 아니라
**위 실측 결과에 달린 조건부 선행 작업**이다. 결과가 「열린다」면 이번 범위에서 손댈 것이 없다.
결과가 「안 열린다」면 그때는 FE 선언 · STT 설정 · 원본 저장이 함께 움직이므로 별도 작업이 맞다
(그 세 곳이 함께 움직인다는 §5-4 의 서술은 그대로 유효하다).

### 10-2. 정정 ② — 취약점의 영향 플랫폼

§3-2 의 표에 **영향 플랫폼이 빠져 있었다.** GHSA-7gmj-67g7-phm9 의 결함은
`is_local_url()` 이 **Windows·Android 에서** 첫 서브도메인만 보고 로컬로 판정하는 것이다.
영향 범위 `>=2.0, <=2.11.0` · 패치 `>=2.11.1` 은 그대로다.

**하한 2.11.1 자체는 유지가 맞다** — 대상 OS 가 미정(OQ-T01)이고 참조 제품이 이미 2.11.3 이라
비용이 0 이다. **근거 문장에 플랫폼을 적는 것**이 정정이다.

### 10-3. 보강 ① — 네이티브가 관측할 수 있는 수명주기 사건은 **셋**뿐이다

SPEC-006 v0.2.0 이 TTL·갱신 구조를 버리고 「네이티브가 점유 수명을 소유」하는 구조로 간 근거다.
Tauri v2 공개 API 에서 셸이 관측 가능한 사건을 전수로 확인했다(확인 2026-09-22).

| 사건 | API | 문서 문구 |
|---|---|---|
| 창 닫기 요청 | `WindowEvent::CloseRequested` | "The window has been requested to close." (`CloseRequestApi` 로 동작을 바꿀 수 있다) |
| 창 소멸 | `WindowEvent::Destroyed` | "The window has been destroyed." |
| 앱 종료 | `RunEvent::ExitRequested` / `RunEvent::Exit` | "The app is about to exit" / "Event loop is exiting." |
| 문서 로드 | `PageLoadEvent::Started` / `Finished` | "Page started to load." / "Page finished loading." |
| 네비게이션 취소 | `WebviewWindowBuilder::on_navigation` | "Defines a closure to be executed when the webview navigates to a URL. Returning `false` cancels the navigation." |

출처: <https://docs.rs/tauri/latest/tauri/enum.WindowEvent.html> ·
<https://docs.rs/tauri/latest/tauri/enum.RunEvent.html> ·
<https://docs.rs/tauri/latest/tauri/webview/enum.PageLoadEvent.html> ·
<https://docs.rs/tauri/latest/tauri/webview/struct.WebviewWindowBuilder.html>

**없는 것도 적는다.** `RunEvent` 에 `WebviewEvent` 변형이 있으나 위 문서에서
**웹 콘텐츠 프로세스가 죽었다는 사건을 확인하지 못했다.** 플랫폼 층에는 그런 통지가 있지만
(WKWebView 의 콘텐츠 프로세스 종료 델리게이트) **Tauri 공개 API 에서 그것을 받는 경로를
문서로 확인하지 못했다.** 그래서 SPEC-006 은 **「웹이 살아 있는 채로 멈추면 점유가 남는다」를
한계로 적고**, 「반드시 자동 정리된다」고 쓰지 않는다.

**정리하면 네이티브가 확실히 정리할 수 있는 것은 셋이다** —
창 닫기·앱 종료 · 문서 교체 · 프로세스 소멸(OS 가 절전 방지 자원을 회수).
이 셋이 SPEC-006 의 L-06 · L-09 · L-13 이다.

> ⚠ **2026-09-22 보강 — 「요청」과 「완료」를 가려야 한다.** 위 표의 사건 중 둘은 **취소될 수 있다.**
> - `WindowEvent::CloseRequested` 는 문서 문구 그대로 *"The window has been requested to close."*
>   이고, 함께 오는 `CloseRequestApi` 로 **닫기를 막을 수 있다.** 즉 이것은 **요청**이지 완료가 아니다.
>   실제 완료는 `WindowEvent::Destroyed`("The window has been destroyed.") · `RunEvent::Exit` 쪽이다.
> - `on_navigation` 은 *"Returning `false` cancels the navigation."* 이라 **취소된 이동**이 존재한다.
>   문서가 실제로 바뀌는 신호는 `PageLoadEvent::Started` 쪽이고, **취소된 이동에서는 발화하지 않는다.**
>
> `tauri-spec-fix1-report.md` 가 L-06 의 근거로 `CloseRequested` 를 첫머리에 든 것은
> **사건의 종류를 든 것이지 해제 시점을 정한 것이 아니었다.** 해제 시점을 요청 단계에 두면
> 「사용자가 `계속 녹음`을 골랐는데 점유는 이미 풀린」 상태가 된다 — 이 작업이 막으려는 사고 그대로다.
> SPEC-006 v0.2.1 이 L-06·L-09 를 **완료 사건으로** 못박고 L-11 에 **취소된 이동**을 넣은 근거가 이것이다.
> **어느 API 를 쓸지는 구현의 몫이고, SPEC 이 요구하는 것은 「완료에만 푼다」는 관찰 가능한 결과다.**

### 10-4. 보강 ② — 갱신 신호를 보장할 근거가 없다

검수는 「갱신을 타이머가 아니라 녹음 청크에 태우고 TTL 을 최악 스로틀의 3배로 두면 안전하다」고
권했다. **채택하지 않았다.** 근거:

- MDN 의 `dataavailable` 문서는 이 이벤트가 타임슬라이스마다 발생한다고 **설명**하지만,
  **지연 없는 전달을 보증하는 문장이 없다**
  (<https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder/dataavailable_event>, 확인 2026-09-22).
- 검수가 인용한 스로틀 수치(비가시 5분 + 무음 30초 → 분당 1회)는 **Chromium 계열의 규칙**이다.
  이번 대상 웹뷰는 **WebKit(macOS)·WebView2(Windows)** 다. **한 엔진의 수치를 다른 엔진에
  적용해 「3배면 안전」이라고 쓸 근거가 없다.**

즉 어떤 배수를 고르든 **「정상 녹음 중인데 신호가 늦었다」와 「웹이 죽었다」를 가르지 못한다.**
가르지 못하는 판정으로 OS 절전 방지를 **푸는** 것은 이 작업이 막으려는 사고 그 자체다.
**그래서 판정을 계약에서 없앴다** — 이것이 커맨드가 다섯에서 넷으로 준 이유다.

### 10-5. 보강 ③ — 세션 만료가 실제로 하는 일 (검수 F-2·F-3 재확인)

**확인했고, 검수의 사실 주장이 맞다.**

- **WS 인증은 핸드셰이크 한 번뿐이다.** `entrypoints/http.py:1016-1019` — `await websocket.accept()`
  직후 `connection_principal(websocket)` 을 한 번 부르고, `None` 이면 닫는다. 함수 주석도
  「여기서 하는 것은 **인증뿐**이다」(`:1013`)라고 적는다.
- **스트림이 도는 중에 다시 보지 않는다.** `modules/meetings/` 아래에서
  `principal|expire|UNAUTHORIZED|auth` 를 훑었고, `stream_service.py` 에는 **0건**이다
  (다른 파일의 hit 은 회의 자료·후속업무 권한 검사이고 스트림 수명과 무관하다).
- **전역 401 처리가 없다.** `frontend/src` 전체에서 `401` 은 두 곳뿐이다 —
  `lib/api.ts:767`(세션 조회가 `null` 을 돌려주는 자리)과 `features/meetings/stream.ts:83`
  (닫힘 코드 4401 을 `unauthorized` 로 옮기는 자리). 공용 `request()` 는 `ApiError` 를 던질 뿐이다.
- **로그인 화면으로 되돌리는 경로는 둘뿐이다** — `App.tsx:169` 의 첫 세션 확인 실패,
  그리고 `App.tsx:503-506` 의 `onSessionLost`(주석: 「스트림이 인증으로 닫혔다 — 쿠키가 죽었으므로
  로그인 화면으로 돌려보낸다」), 이는 `MeetingDetailPage.tsx:410` 의 `unauthorized` 닫힘에서 온다.

> **뜻**: 12시간이 지났다는 것만으로 **열린 스트림이 닫히지도, 화면이 로그인으로 바뀌지도 않는다.**
> SPEC-006 v0.1.0 이 이것을 「기존 동작」이라고 적은 것은 **틀렸고**, v0.2.0 에서 정정했다.
> 그리고 래퍼가 재인증·자동 로그아웃을 **새로 만들지 않는다** — 점유는 시각이 아니라
> **녹음이 실제로 끝날 때** 풀린다.

### 10-6. 보강 ④ — 두 녹음 표면은 한 창에 공존하지 않는다 (검수 F-4 재확인)

`frontend/src/App.tsx:398` 이 **early return** 이다 —
`if (browserInteractionId) return <BrowserInteractionPage … />;`.
브라우저 인터랙션 화면이 뜨면 앱 트리의 나머지가 통째로 빠지므로 회의 화면은 언마운트되고,
`stream.ts` 의 effect cleanup 이 마이크와 소켓을 닫는다. **동시 녹음은 제품 UI 에서 도달 불가다.**

> **그런데도 SPEC-006 이 「세션 키」를 둔 이유는 동시성이 아니다.** 같은 표면이 **재진입·재시도로
> 두 번 거는 경우**와, **지난 녹음의 늦은 해제가 새 녹음을 끄지 않게** 하려는 것이다.
> 세는 카운터였다면 전자가 누수를 만들고 후자를 막지 못한다. 이름으로 바꾸면 둘 다 닫힌다.
> v0.1.0 의 「표면이 둘이라 동시에 점유할 수 있다」는 근거는 **철회**한다.

### 10-7. 보강 ⑤ — 앱 내 화면 전환은 네비게이션 사건이 아니다 (검수 F-5 재확인)

- 화면 전환은 **React 상태**다 — `App.tsx:73` `const [surface, changeSurface] = useState<ProductSurface>("today")`.
- `pushState|replaceState|location.href=|location.assign|location.replace` 를 `frontend/src` 전체에서
  훑은 결과 **`App.tsx:401` 의 `window.history.replaceState` 한 곳뿐**이고, 그 자리는
  브라우저 인터랙션 화면을 **닫을 때** `?interaction=` 을 지우는 용도다.

> **뜻**: ① 셸의 네비게이션 훅은 **앱 내 화면 전환을 보지 못한다** — 「셸이 마지막 방어선이라
> 점유가 영구히 남는 경로가 없다」는 v0.1.0 의 주장은 과장이었다. ② 반대로 셸이 same-document
> 히스토리 갱신까지 네비게이션으로 보고 해제하면 **녹음 중에 점유가 풀릴 수 있다.**
> SPEC-006 v0.2.0 은 이것을 L-09(문서 교체 · 네이티브) · L-10(앱 내 전환 · 웹) ·
> L-11(같은 문서 주소 변경 · 트리거 아님) 셋으로 갈랐다.

### 10-8. 보강 ⑥ — 개발 환경으로 뗄 수 있는 측정 (검수 W-4)

§7 의 실측 표가 「운영 주소가 없으면 아무것도 못 한다」로 읽힐 수 있었다. **정정한다.**
MDN 이 `localhost` 를 secure context 로 명시하므로(§4-5 인용), **통제된 개발 HTTPS 또는
`localhost` fixture** 만으로 마이크·녹음·절전·창 수명·외부 링크·쿠키 지속을 전부 잴 수 있다.

**운영 주소가 실제로 막는 것은 둘뿐이다** — 원격 origin ACL(M-1)과 쿠키 지속(M-5)의 **«최종»
확인, 그리고 인수조건의 최종 통과.** 구조 확인은 개발 origin 으로도 된다.
그리고 **이 측정 작업 자체를 후속 WP 에 계획할 수 있다** — 「WP 앞에 반드시 실측」이라는
순환 게이트를 SPEC-006 v0.2.0 에서 걷어냈다.

### 10-9. 이번 보강에서도 하지 않은 것

- **실행·빌드·설치·서버 기동을 하지 않았다.** 코드 프로토타입도 만들지 않았다
- **Tauri 의 원격 URL + IPC 성립 여부는 여전히 단정하지 않았다**(§3-5 그대로). M-1 이 그 자리다
- **Apple 릴리즈 노트 본문을 받지 못했다**(§10-1). WebKit 블로그 단일 출처다
- **대상 OS·운영 주소·배포 채널·서명 신원을 발명하지 않았다**
