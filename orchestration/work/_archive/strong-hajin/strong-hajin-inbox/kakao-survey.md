# 카카오톡 Mac 조회·발송 가능성 조사 (read-only)

> architect(kakao) · 2026-10-06 · 질문: Strong Hajin 데스크톱 앱(Tauri·Rust)이 **Mac 의 카톡**을
> 조회(수집)·발송(답장)할 수 있나, 할 수 있다면 어떤 방식으로?
>
> 근거 두 축: 우리 과거 작업 `para/projects/summer-star/mykakao/`(대부분 **Windows 판**) · 외부 레포
> `silver-flight-group/kakaocli`(**Mac 전용**, scratchpad 얕은 clone, 읽기만 — 빌드·실행·설치 안 함).
> 이 Mac 은 `ls` 로 **존재 확인만** 했다 — DB 를 열거나 복호·조작·발송하지 않았다.
>
> ⚠ 근거 표기: `kakaocli/<경로>:줄` = 외부 clone(읽기 전용, 실행 안 함) · `para/.../mykakao/...` = 우리 문서
> · `issue #N` = kakaocli GitHub 이슈 · `커밋` = kakaocli git log.

---

## §1. 결론

**조회는 된다. Mac 에서는 Windows 보다 오히려 쉽다.** mykakao 가 Windows 에서 막혔던 벽(오프라인 키
파생 실패 → 실행 중 메모리 회수로 우회 · anti-debug 자폭, `mykakao/00-baseline/baseline-004-offline-key-derivation.md:72-83`)이
**Mac 에는 없다**. Mac 은 키를 **기기 값에서 오프라인으로 유도**한다 — `IOPlatformUUID`(ioreg) + 카톡
`userId`(plist) 두 값만으로 PBKDF2-HMAC-SHA256 을 돌려 SQLCipher 키를 만든다(`kakaocli/Sources/KakaoCore/Database/KeyDerivation.swift:54-81`,
blluv 연구 기반). 카톡이 꺼져 있어도, 메모리를 안 건드려도 로컬 DB(SQLCipher)를 복호해 방 목록·메시지·
검색·임의 SQL 까지 읽는다(`kakaocli/Sources/KakaoCore/Database/DatabaseReader.swift:25-52,92,136`). 이 Mac 에서
실물 확인: 카톡 `26.1.1` 설치됨 · 컨테이너에 78-hex DB 파일 + `-wal`/`-shm` 존재(§2 ls 결과).

**발송도 된다. 단 "API 발송"이 아니라 카톡 창을 손으로 조작하듯 두드리는 UI 자동화다.** macOS 접근성
(Accessibility, AXUIElement)으로 카톡을 실행·로그인시키고, 채팅방 행을 찾아 열고, 입력창에 글자를 넣고
Enter 를 누른다(`kakaocli/Sources/KakaoCore/Automation/KakaoAutomator.swift:12-117`). 조건이 붙는다 — **카톡
앱이 떠 있고 로그인돼 있어야** 하고, 터미널/호스트 앱에 **접근성 권한**이 있어야 하며, **텍스트만** 보낼 수
있다(첨부 발송은 미구현). 오발송·멈춤 위험이 실제로 보고돼 있다(`issue #9` send hang).

**두 줄 요약**: (a) **조회** = 카톡 설치 + 전체 디스크 접근 권한이면 앱 없이도 가능, 텍스트 중심(사진·첨부는
Mac 판 미구현). (b) **발송** = 카톡 실행 + 로그인 + 접근성 권한 + UI 자동화, 텍스트만, 불안정. 둘 다 카카오
**비공식**이고 카톡 버전 업데이트로 깨질 수 있다(§6).

---

## §2. 조회 방식 — mykakao(Windows) vs kakaocli(Mac) 비교

핵심은 **mykakao 문서의 카톡 작업은 거의 전부 Windows 판**이라는 점이다. Mac 판은 mykakao 의 맨 처음
아이디어(BASE-001)와 kakaocli 가 근거다.

| 항목 | **Windows** (mykakao V2) | **Mac** (kakaocli = 질문의 대상) |
|---|---|---|
| 근거 | `mykakao/00-baseline/baseline-003-windows-tray-realtime-accumulation.md` · `.../decision-003-windows-v2-approach.md` | `kakaocli/*` (Mac 전용, `README.md:266`) · `mykakao/.../baseline-001-kakao-message-extraction.md:42` |
| DB 위치 | 계정 폴더 `%LOCALAPPDATA%\Kakao\...\chat_data\chatLogs_<chatId>.edb` (**방마다 파일**) (`baseline-003:54-55`) | `~/Library/Containers/com.kakao.KakaoTalkMac/Data/Library/Application Support/com.kakao.KakaoTalkMac/<78-hex>` (**단일 DB**) (`kakaocli/.../DeviceInfo.swift:34-37`) |
| 이 Mac 실측 | — | ✅ 컨테이너 존재 · 78-hex 파일 2개(+`.db`/`-wal`/`-shm`) · 카톡 `26.1.1` 설치 (아래 ls) |
| 암호화 | SQLCipher **v4**, compat4, raw-key 32B (`baseline-003:57-58`) | SQLCipher, **compat 3 먼저 → 4 폴백**, PRAGMA key (`kakaocli/.../DatabaseReader.swift:25-52`) |
| **키 획득** | **오프라인 파생 실패** → **실행 중 메모리 raw-key 회수**(passive VM_READ) (`decision-003:44-52`). 파생식은 anti-debug 로 셸빙 (`baseline-004:72-83`) | **오프라인 파생 성공** — `IOPlatformUUID`+`userId` → PBKDF2-SHA256 100k (`kakaocli/.../KeyDerivation.swift:10-81`). **메모리 안 건드림** |
| 키 입력 필요? | 아니오(메모리에서) | **아니오** — 기기 값에서 자동 유도. 사용자가 키를 넣지 않는다 |
| userId 출처 | — | plist(`com.kakao.KakaoTalkMac.plist`) 4전략: FSChatWindowTransparency 공통접미사 / 직접키 / SHA-512 역추적 / Frame 키 (`kakaocli/.../DeviceInfo.swift:59-108`) |
| 스키마 | `chatRooms`/`chatLogs`/`talkUser` (`baseline-003:59`) | `NTChatRoom`/`NTChatMessage`/`NTUser`/`NTChatContext` (`kakaocli/.../DatabaseReader.swift:92,136,186`) |
| 읽는 범위 | 과거 전체 복호(1455행 실증) | 방 목록·메시지·전문검색·임의 SQL (`kakaocli/.../DatabaseReader.swift` · `README.md:132-140`) |
| 방 목록 | `chatRooms`/`chatListInfo` | `chats` 명령 = NTChatRoom (direct/group/open 구분, `kakaocli/.../Models/Chat.swift:14-18`) |
| **첨부·사진** | talkmedia URL 다운로드로 **수집 구현**(실시간) (`mykakao/.../baseline-007-photo-collection.md` · `decision-006`) | ❌ **미구현** — 메시지의 `message`(텍스트)만 읽음. 사진/영상/파일은 type 으로 분류만, 본문·다운로드 없음 (`kakaocli/.../Models/Message.swift:14-21` · `README.md:272,281`) |
| **실시간 감지** | **파일 변경 감지**(`-wal` watch) → 델타 복호 → append → SSE (`decision-003:64-73`) | **폴링** — `MAX(logId)` 고수위 추적, 기본 2초 간격(`kakaocli/.../Sync/DatabaseWatcher.swift:24-72`). **파일 감시 아님** |
| 과거 범위 한계 | 로컬 `.edb` 에 있는 만큼 | **Mac 에서 연 채팅만** 로컬에 동기화됨 → 안 연 방은 과거가 비어 있음. `harvest --scroll` 로 더 불러오나 **톡드라이브 플러스 페이월**에 막힘 (`README.md:268`) |

**이 Mac `ls` 실측 (읽기 확인만, 파일 안 엶):**
```
~/Library/Containers/com.kakao.KakaoTalkMac/        → 존재 (drwx------)
  └ Data/Library/Application Support/com.kakao.KakaoTalkMac/
       1196e147…500a816030b8a9d00        (78-hex, 암호 DB 후보)
       1196e147…-shm / -wal              (SQLite WAL — 쓰기 진행 중 흔적)
       b0bae659…21235d99a24ffe7e4049     (78-hex, 두 번째 후보 — 계정/서브 DB로 추정)
       b0bae659…-shm / -wal
/Applications/KakaoTalk.app             → 존재, CFBundleShortVersionString = 26.1.1
```
> 주: 78-hex 파일명은 kakaocli 의 DB 탐색 패턴(`^[0-9a-f]{78}(\.db)?$`, `kakaocli/.../DeviceInfo.swift:130-147`)과
> 정확히 일치한다. 즉 **이 Mac 은 kakaocli 가 가정하는 구조 그대로다.** 설치 버전 `26.1.1` 은 mykakao
> BASE-001 이 기록한 그 버전(`baseline-001:42`)과 같다.

---

## §3. 발송 방식 · 권한 · 위험

### 방식 — 접근성(Accessibility) UI 자동화. API·프로토콜 아님.
`send` 는 카톡 창을 사람이 조작하듯 두드린다(`kakaocli/Sources/KakaoCore/Automation/KakaoAutomator.swift:12-117`):
1. 카톡 실행·로그인 보장(`AppLifecycle.ensureReady`, 없으면 자동 실행 + 저장된 자격증명으로 자동 로그인)
2. 카톡을 전면화(activate) → 메인 윈도우 획득
3. **열려 있던 다른 채팅창을 모두 닫음**(엉뚱한 방 오발송 방지, `:29-35`)
4. 채팅 목록에서 대상 방 행을 찾아 **행 선택 + Enter**(화면 밖이면 스크롤 후 더블클릭 폴백, `:61-77`)
5. 채팅창의 입력 AXTextArea 를 찾아 값 설정 → **Return 키**(`:92-112`)
6. 채팅창 닫음

로그인도 접근성으로: 로그인 화면의 이메일/비번 필드를 채우고 "로그인" 버튼을 누른다
(`kakaocli/.../LoginAutomator.swift:12-131`). 자격증명은 macOS 키체인에 저장
(`security` CLI, `kakaocli/.../CredentialStore.swift:40-84` · `AGENTS.md` Credential Storage).

### 필요한 macOS 권한 (호스트/터미널 앱 기준)
- **Full Disk Access(전체 디스크 접근)** — 암호 DB 읽기. 모든 명령에 필요 (`README.md:80,84`)
- **Accessibility(접근성)** — UI 자동화(발송·harvest·inspect). `send` 에 필수 (`README.md:81,84`)
- 발송 시 **카톡이 실행 중 + 로그인 + 창 표시**여야 함 (`README.md:270` · `AppLifecycle.swift:191-231`)

### 카톡 창이 떠 있어야 하나 · 첨부
- **조회**: 아니오 — 앱 없이도 DB 만 읽으면 됨(`README.md:99,101`). 단 **새 메시지를 로컬에 받으려면** 카톡을
  한 번 열어 서버 동기화가 돼야 함(`README.md:268`).
- **발송**: **예** — 카톡 창 필요(`README.md:270`).
- **첨부 발송**: ❌ **텍스트만**. `send` 에 첨부 경로 없음(`kakaocli/.../SendCommand.swift` 전체 — message 인자 하나).
  → Strong Hajin 결정 "슬랙·메일 첨부 보내기"(`_RESUME.md` §2 2026-10-06)는 **카톡엔 당장 적용 불가**.

### 실패·오발송 위험 (실제 이슈 포함)
- **발송 멈춤**: `--dry-run` 은 되는데 실제 `send` 가 **hang** — 최신 upstream 에서도 재현(`issue #9`, OPEN).
- **오발송**: 행 선택이 off-screen 에서 어긋나 엉뚱한 방에 갈 소지 → 코드가 "다른 창 닫기 + 행 선택" 으로
  방어하나(`KakaoAutomator.swift:29-35,61-77`) 완전하지 않음. 과거 커밋도 이 문제 수정 이력
  (`커밋 50200bd` "AX row selection instead of double-click for off-screen rows").
- **2FA/OTP**: 자동 로그인 중 인증코드 요구 시 중단, 수동 로그인 필요(`LoginAutomator.swift:153-171`, `otpRequired`).
- **계정당 Mac 1대**: 카톡은 계정당 Mac 하나만 로그인 허용(`README.md:271`) — 자동 로그인이 사용자의 다른
  Mac 세션을 밀어낼 수 있음.
- kakaocli 자체 **안전 규칙**이 "테스트는 `--me`(나와의 채팅) · 발송 전 확인 · 2초 간격 · 심야 금지"를 명시
  (`AGENTS.md` Safety Rules) — 발송이 그만큼 조심스러운 동작이라는 방증.

### 언어·라이선스·버전·유지보수
- 언어: **Swift**(Package.swift, `Sources/KakaoCore`·`KakaoCLI`). SQLCipher 는 `brew install sqlcipher` 전제.
- 라이선스: **MIT** (`kakaocli/LICENSE`, `README.md:330`) → **재사용·포팅 가능**(출처 표기).
- 마지막 커밋: **2026-03-31** (`커밋 8b6ffcf`). 최근 6개월 정체 — 최신 카톡에서 깨질 위험(§6).
- 지원 버전 이력: App Store·최신 Mac 버전 대응 커밋 있음(`커밋 03d68aa` #3) but 아래 이슈처럼 버전별 깨짐.

---

## §4. Strong Hajin 에 붙이는 그림 (선택지 — 결정 아님)

`_RESUME.md` §2(2026-10-05)는 이미 방향을 적어 뒀다: **"Tauri 데스크톱 앱(Rust)이 개인 Mac 의 카톡 로컬
DB 를 읽어 가져온다. 서버에는 카톡 연결 정보(복호화 키 · 저장한 채팅방 ID)를 보관."** 이번 조사는 그 그림이
**기술적으로 성립함**을 확인한다. 역할 분담 후보:

```
[사용자 Mac]  Strong Hajin 데스크톱(Tauri·Rust)
   ├─ 키 유도   : IOPlatformUUID + userId → PBKDF2 → SQLCipher 키   (기기 안에서만)
   ├─ DB 읽기   : 컨테이너 78-hex DB 복호 → 방/메시지 추출
   ├─ 실시간    : logId 고수위 폴링(또는 -wal 파일감시) → 새 메시지 수집
   └─ (2단계) 발송 : 접근성 UI 자동화로 카톡 창에 입력
        │
        ▼ (수집한 메시지 업로드 · 개인별)
[서버]  저장·개인별 노출(메일/슬랙과 같은 메시지함 파이프, `_RESUME.md` 2026-10-06 흐름 결정)
   └─ 보관: 연결 정보(저장한 방 ID). 복호화 키 보관 여부는 열린 질문(§5 K-6)
```

### 선택지 A — kakaocli 를 **사이드카로 그대로 실행**
Tauri 는 외부 바이너리를 sidecar 로 번들·호출할 수 있다. Rust 는 `kakaocli chats --json` / `messages --json`
/ `sync --follow`(NDJSON) 을 실행해 stdout 을 파싱.
- **장점**: 이미 검증된 코드, 통합 빠름, JSON 출력이 agent 친화적(`README.md:142` · `AGENTS.md` NDJSON), MIT.
- **단점**: Swift 바이너리 + `sqlcipher` 의존을 앱에 동봉해야 함(정적 링크 안 하면 brew 의존), macOS 빌드 전용,
  별도 프로세스, 발송 불안정(`issue #9`)을 그대로 상속, upstream 정체(2026-03-31) 시 우리가 수선해야 함.

### 선택지 B — **방식만 Rust 로 포팅**(mykakao Windows `win_app/` 가 쓴 전략)
mykakao 는 Windows 에서 spike Python 코드를 **Rust(rusqlite + bundled-sqlcipher)로 포팅**하기로 이미 결정했다
(`mykakao/.../decision-003-windows-v2-approach.md:81-91`). Mac 도 같은 손으로:
- **읽기 포팅은 가볍다**: 키 유도는 순수 PBKDF2/SHA(=`ring`/`sha2`/`pbkdf2` crate), DB 는 `rusqlite` +
  `bundled-sqlcipher`(정적 링크, brew 의존 제거). kakaocli 의 Swift 로직을 1:1 옮기면 됨.
- **발송 포팅은 무겁다**: 접근성(AXUIElement) 제어를 Rust 에서 하려면 `objc2`/`accessibility` 바인딩으로
  AX 트리 탐색·키 이벤트를 다시 짜야 함 — kakaocli 가 Swift 로 400+줄 쓴 부분(`AXHelpers.swift` 435줄,
  `KakaoAutomator.swift` 138줄)을 재구현하는 비용.
- **장점**: 단일 네이티브 앱, 의존성 최소, upstream 독립, 우리 스키마/권한 모델에 맞춤.
- **단점**: 초기 구현 비용(특히 발송), 버전 깨짐을 우리가 직접 추적.

### 선택지 C — **하이브리드 (단계에 맞춤)**
1단계 목표 = **수집(조회)**뿐이고 발송은 2단계다(`_RESUME.md` 2026-10-06 단계 분리). 그래서:
- **1단계**: 읽기만 Rust 네이티브 포팅(선택지 B 의 가벼운 쪽). 발송 코드는 아직 안 짬.
- **2단계**: 발송을 그때 kakaocli 사이드카(A)로 빌릴지, AX 를 Rust 로 포팅(B)할지 다시 판단.
- **근거**: 조회의 기술 난이도는 낮고(키 유도+DB 읽기), 발송은 난이도·위험이 높다(UI 자동화·hang·오발송).
  단계가 이미 갈려 있으니 비용 큰 결정을 2단계로 미룰 수 있다.

> **결정하지 않는다** — 위는 선택지와 근거만. 코디/사용자가 고른다.

---

## §5. 열린 질문 K-1~K-8 과의 관계 · 새 질문

K-1~K-8 은 `design-survey.md:315-322`(시안 카톡 화면 기준) 질문이다. 이번 조사로 바뀌는 답:

| 질문 | 시안 전제 | 이번 조사가 주는 답 |
|---|---|---|
| **K-1** 기기·앱 연결 상태 자리 | 시안에 없음 | **필요.** 조회는 앱 꺼져도 되지만(§2), **새 메시지 로컬 반영은 카톡을 한 번 열어야** 함(`README.md:268`). 상태카드에 「데스크톱 앱 켜짐 · 카톡 설치/로그인 · 마지막 수집」이 와야 함. kakaocli `status`/`login --status` 로 상태 판별 가능(`AGENTS.md` App State Detection) |
| **K-2** 참여자 동의 안내 문구 | "안내 전송·동의 후 적재" | ⚠ **기술적 근거 없음.** 로컬 DB 를 조용히 읽는 방식이라 상대에게 안내를 보내거나 동의를 받는 단계가 **없다**. 시안 문구를 유지하려면 제품이 따로 약속·구현해야 하고(기술이 강제 안 함), 유지 안 하면 §6 윤리·약관 리스크를 그대로 안음. **사용자 판단 필요** |
| **K-3** 방 이름 입력 vs 목록 선택 | 이름 입력 | **목록 선택 가능.** kakaocli `chats` 가 방 목록을 준다(NTChatRoom, `DatabaseReader.swift:92`). 이름 타이핑보다 **읽은 목록에서 고르게** 하는 게 맞음(오타·중복 회피) |
| **K-4** 단체방만 vs 1:1 | "단체방" 고정 | **둘 다 읽힘.** Chat.type = direct/group/open 구분(`Models/Chat.swift:14-18`). 범위는 제품 선택, 기술 제약 아님 |
| **K-5** 수집주기·받아오기 = 서버냐 앱이냐 | 서버 수집 주기처럼 그림 | **앱(데스크톱)이 돈다.** 수집=Mac 로컬 폴링(`DatabaseWatcher.swift`, 기본 2초). 서버에서 누른 "받아오기"는 앱이 서버 명령을 받아야 닿음. 시안의 「15분/1시간…주기」는 **데스크톱 앱 폴링 간격**으로 재해석 |
| **K-6** 복호화 키 화면에서 다루나 | 시안에 자리 없음 | **자리 불필요** — 키는 기기 값에서 **자동 유도**(`KeyDerivation.swift:54-81`), 사용자 입력 없음. 다만 `_RESUME.md` 가 "서버에 키 보관"이라 했는데, **디바이스가 언제든 재유도 가능하므로 서버에 둘 필요가 있는지**가 새 질문(아래 K-10) |
| **K-7** 과거 얼마나 | "동의 이후부터" | **로컬에 있는 만큼.** Mac 은 **이 Mac 에서 연 방**만 과거가 로컬에 있음. 더 불러오려면 `harvest --scroll` 이나 **톡드라이브 플러스 페이월**에 막힘(`README.md:268`). "얼마나"는 우리가 정하는 게 아니라 **카톡이 로컬에 준 만큼**이 상한 |
| **K-8** `대화방 열기` 가 카톡 여나 | — | 메시지함 조회는 **우리 DB 렌더**라 카톡 안 열어도 됨. 발송(2단계)만 카톡 창을 엶(§3). 시안의 `대화방 열기`는 1단계 범위에선 불필요(`_RESUME.md` 2026-10-05: 메시지함은 읽음확인만) |

### 새로 생긴 질문
- **K-9 (첨부·사진)**: kakaocli Mac 판은 **텍스트만** 읽고 사진/첨부는 미구현(§2). Windows mykakao 는
  talkmedia URL 다운로드로 사진 수집을 했다(`baseline-007`). Mac 에서 사진·첨부까지 모으려면 **별도 작업**이
  필요(스키마에 talkmedia 매핑이 있는지 Mac 쪽 재조사). 1단계 범위에 사진을 넣을지?
- **K-10 (키 보관 위치)**: 디바이스가 키를 언제든 재유도할 수 있으니, 서버에 복호화 키를 **보관하지 않는** 선택이
  가능하다(보안상 유리). `_RESUME.md` 의 "서버에 키 보관" 결정을 유지할지 재검토.
- **K-11 (발송 안정성·방식)**: 2단계 답장을 AX 자동화로 갈 경우 hang(`issue #9`)·오발송·카톡 창 점유를
  어떻게 다룰지. 서버가 아니라 **사용자 Mac 에서만** 발송 가능하다는 제약을 UX 가 받아들여야 함.
- **K-12 (멀티계정·여러 Mac)**: 카톡은 계정당 Mac 1대(`README.md:271`). "개인별 노출"(`_RESUME.md` 2026-10-06)은
  각자 자기 Mac 에 데스크톱 앱을 깔아 수집하는 모델이어야 성립 — 서버 중앙 수집이 아님.

---

## §6. 약관 · 안정성 위험

### 비공식 접근 — 카카오 약관·계정 리스크
- kakaocli 는 **카카오와 무관한 비공식 도구**이며, 공식 API 가 아니라 **로컬 DB 읽기 + 네이티브 클라이언트
  UI 자동화**로 동작한다(스스로 명시, `README.md:12,259,285-299`). 카카오 프로토콜(LOCO) 역분석·API 호출은
  안 한다고 선언하지만, **자동화·비공식 접근으로 계정이 제한될 수 있음**을 면책에 적어 둠(`README.md:299`).
- **상대 동의 없이 대화가 읽힘** → K-2 의 시안 문구("참여자 동의 후 적재")와 정면 충돌. 개인용(본인 대화)을
  넘어 제품으로 배포하면 **개인정보·동의 쟁점**이 커진다. mykakao 는 "본인 기기·본인만·외부배포 없음"을 전제로
  달고 출발했다(`baseline-001:37`) — Strong Hajin 이 그 전제를 넘는지 확인 필요.

### 버전 업데이트로 깨짐 — 실제 이슈에서 확인
카톡 Mac 버전이 바뀌면 **키 유도·userId 탐지·앱 실행 경로**가 깨진 전력이 이슈에 쌓여 있다:

| 이슈 | 상태 | 깨짐 |
|---|---|---|
| `#16` | CLOSED | App Store 카톡 **26.3.0(한국어)**에서 userId 자동탐지 실패 — SHA-512 brute force 20B 범위 소진 |
| `#14` | OPEN | userId 자동탐지 실패, 어떤 후보 userId 로도 유효한 키 안 나옴 |
| `#22` | OPEN | 실행 경로 `/Applications/KakaoTalk.app` 하드코딩 → **한국어 설치(`카카오톡.app`)에서 깨짐** |
| `#4`  | OPEN | 큰 userId 에서 SHA-512 brute-force 타임아웃이 너무 짧음 |
| `#9`  | OPEN | **발송**이 `--dry-run` 은 되는데 실제로 hang |
| `#2`,`#1` | CLOSED | FSChatWindowTransparency 키 사라짐 / App Store 버전 지원 문제 |

- 코드가 compat **3→4 폴백**(`DatabaseReader.swift:25-52`), userId **4전략 + SHA-512 역추적**
  (`DeviceInfo.swift:59-108`)을 쌓은 것 자체가 **버전마다 키·plist 구조가 흔들린다**는 증거.
- **마지막 커밋 2026-03-31** 이후 정체 → 최신 카톡은 미검증. 이 Mac 은 `26.1.1`(구버전)이라 당장은 호환
  가능성이 높지만, 사용자가 카톡을 업데이트하면 깨질 수 있다. **우리가 포팅하면 이 추적 부담도 우리 몫.**

### Mac 이 Windows 보다 나은 점 (안정성 측면)
- Windows 는 오프라인 파생이 **막혔고**(anti-debug 자폭, `baseline-004:72-83`) 카톡 실행 중 메모리 회수에
  의존했다. Mac 은 **오프라인 유도가 성립**해 카톡 실행·메모리 접근이 필요 없다(조회 한정) → **덜 깨지고 덜
  침습적**. 발송만 UI 자동화라 불안정 축이 남는다.

---

## 부록 — 조사 경계(무엇을 안 했나)
- kakaocli 는 scratchpad 에 **얕게 clone 해 소스만 읽음**. 빌드·실행·설치·`brew` 안 함. 이 레포 밖으로 아무것도
  설치하지 않음.
- 이 Mac 카톡은 **`ls` 로 존재/버전만 확인**. DB 열기·복호·카톡 조작·메시지 발송 **안 함**.
- GitHub 이슈는 `gh issue list`(읽기)로 제목·상태만 확인.
