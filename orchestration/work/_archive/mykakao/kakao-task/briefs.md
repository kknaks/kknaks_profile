# mykakao win_app — 발주 브리프 통합

> work-003 리뉴얼 정리(2026-09-04): 흩어져 있던 발주 브리프 19건을 시간순으로 통합. 원본 폴더는 이 문서로 대체됨.

## 목차
1. 스파이크 1 — 키 유도 (파생식 시도)
2. 스파이크 2 — 키 복구 (메모리)
3. 스파이크 3 — 키 복구 확정
4. WORK-003 — win_app P1 (러스트 착수)
5. P2 — 실시간 후킹
6. P3 — 트레이 + 이름
7. FIX — 이름 해석
8. FIX — WAL 병합
9. 스파이크 4 — 파생식 재도전
10. 스파이크 4b — WinDbg
11. WORK-006 — 로그인 상태 추적
12. WORK-007 — 설정 화면 리디자인
13. FIX — 실시간 전송
14. FIX — 로그인 유저 표시
15. WORK-008 — 사진 수집
16. FIX — 사진/실시간 (콘솔창 제거)
17. FIX — 클릭 수집 스피너
18. 스파이크 — 사진 URL/토큰
19. 스파이크 — .cng 로컬 캐시 (백로그)

---


## 1. 스파이크 1 — 키 유도 (파생식 시도)

<sub>원본: `poc-windows-key-derivation/poc-windows-key-derivation-be-brief.md`</sub>

# [backend] Windows 카톡 로컬 DB 키 유도 가능성 탐색 (spike)

너는 **mykakao `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/orchestration/roles/mykakao/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `C:/Users/sc971/orca/workspaces/mykakao/poc-windows-key-derivation`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (⚠ **이 작업은 PR 을 올리지 않는다** — 탐색이다. 산출물은 리포트 + 최소 실증 코드다)

이 워크트리는 너 혼자 쓴다.

> ⚠ **이건 기능 구현이 아니라 탐색(spike)이다.** "되게 만들라"가 아니라 **"되는지, 되면 어떻게, 안 되면 왜 안 되는지를 근거와 함께 판정하라"**가 임무다. 억지로 동작하는 코드를 지어내지 마라 — 못 되면 "못 된다 + 근거"가 완전한 성공이다.

## 1. SSOT — 먼저 읽을 것

이 작업은 spec 이 아직 없다 (되는지 자체가 미지라 spec 을 쓸 수 없다 — 그래서 spike 다). 대신 아래를 읽어라. 전부 **read-only 절대경로** — 고치지 마라.

- `C:/Users/sc971/OneDrive/Desktop/kknaks/mykakao/backend/extract.py` ← **macOS 키 유도의 정본.** 이 로직을 Windows 로 옮길 수 있는지가 이 작업의 전부다.
- `C:/Users/sc971/OneDrive/Desktop/kknaks/mykakao/README.md` ← "어떻게 동작하나" 절 (파이프라인 전체 그림)
- `C:/Users/sc971/OneDrive/Desktop/kknaks/mykakao/backend/db.py` · `models.py` ← 복호화 후 무엇을 읽는지 (SQLCipher 엔진·ORM 매핑)

**기대는 개념**: 해당 없음 (첫 탐색이라 아직 개념 노트가 없다).

## 2. 배경 / 무엇을 확인하나

**macOS 원본 모델** (`extract.py`):
- 키 `= f(device UUID, user_id)`.
- device UUID = `ioreg` 의 `IOPlatformUUID`.
- user_id = `~/Library/Containers/com.kakao.KakaoTalkMac/.../Preferences/*.plist` 의 `*REVISION:<sha512>` 키에서 **SHA512 preimage 를 brute-force** 해 복구.
- 두 값을 PBKDF2-HMAC-SHA256 으로 섞어 SQLCipher passphrase(256-hex) 를 만든다 (`secure_key`).
- 메시지 DB = 컨테이너 안 78자리 hex 파일 (SQLCipher 암호화).

**이 Windows 머신의 실측** (코디네이터가 발주 전 확인 — 네가 재확인하라):
- KakaoTalk **26.4.0.5128** 설치·실행 중. 실행 파일 `C:/Program Files/Kakao/KakaoTalk/`.
- 데이터 디렉토리: `%LOCALAPPDATA%\Kakao\KakaoTalk\` (= `C:/Users/sc971/AppData/Local/Kakao/KakaoTalk/`).
  - `pref.ini` (LANG·auto_start·main_hwnd 정도)
  - `users\ActionLogDB.edb` (+ `-shm` `-wal`) — 확장자 `.edb` = **Microsoft ESE(JET Blue)** 로 보인다. **SQLCipher/SQLite 가 아니다.** 실행 중이라 파일이 잠겨 있었다.
- macOS 의 78-hex SQLCipher 메시지 DB 는 **여기 없다.**

**즉 핵심 질문**: macOS 의 "device UUID + user_id → PBKDF2 → SQLCipher" 모델이 Windows 에 **대응되기는 하는가?** 아니면 Windows 클라이언트는 로컬 저장 구조 자체가 달라(예: ESE, 혹은 로컬에 대화를 영속 저장하지 않음) 이 접근이 성립하지 않는가?

## 3. 계약

해당 없음 (탐색 — 아직 API 계약 없음).

## 4. 먼저 읽을(또는 조사할) 핵심 대상

- `backend/extract.py:37-77` — `platform_uuid` / `find_db` / `_hashed_uuid` / `db_name` / `secure_key`: macOS 가 무엇을 어떤 순서로 하는지. **이걸 기준으로 Windows 대응물을 하나씩 찾는다.**
- `%LOCALAPPDATA%\Kakao\KakaoTalk\` 전체 — 어떤 파일이 있고 각 포맷이 무엇인지 (매직바이트로 판별).
- Windows 레지스트리 (`HKCU\Software\Kakao\...` 있는지), `%APPDATA%\Kakao` 등 다른 후보 경로.
- device 식별자의 Windows 대응 (예: MachineGuid = `HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid`, 혹은 볼륨 시리얼). **추측만 하지 말고 실제로 그 값이 키에 쓰이는지 근거를 대라.**

## 6. 조사 단계

1. **환경 재확인**: 워크트리에서 `git branch --show-current`. 그다음 위 데이터 경로들을 직접 열거해 코디 관찰과 일치하는지 본다 (파일 잠김이면 잠겼다고 기록).
2. **포맷 판별**: `ActionLogDB.edb` 및 발견한 모든 후보 파일의 매직바이트를 확인해 ESE/SQLite/SQLCipher/기타 중 무엇인지 판정한다. (파일이 잠겨 있으면 카톡 종료 후 읽어야 할 수 있다 — **네가 카톡을 강제 종료하지 마라. 잠김이면 "잠김, 종료 필요"로 보고**하고 코디에게 넘긴다.)
3. **대화 저장 위치 탐색**: 이 머신에서 카톡 대화 로그가 로컬에 **영속 저장되는지** 자체를 확인한다. 저장된다면 어디에 어떤 포맷으로인가. ActionLogDB 가 메시지 저장소인지, 아니면 별개 로그인지 구분한다.
4. **키 유도 대응 시도**: macOS `secure_key`/`db_name` 파생식이 Windows 파일명·암호화에 대응되는 흔적이 있는지 조사한다. device 식별자 후보(MachineGuid 등) + user_id 후보를 넣어 macOS 식으로 파일명이 재현되는지 등, **검증 가능한 실험**을 설계해 돌린다.
5. **최소 실증 코드**: 무언가 되면 `backend/` 아래 작은 조사 스크립트(예: `backend/probe_windows.py`)로 재현 가능하게 남긴다. 순수 함수(포맷 판별·후보 키 생성)는 `backend/tests/` 에 테스트로 남긴다. **아무 값(키·user_id·UUID·대화)도 하드코딩·로깅·커밋하지 마라** — `<redacted>` 로.
6. **판정**: 아래 넷 중 하나로 결론낸다.
   - (A) **된다** — 재현 절차 + 실증 코드 제시.
   - (B) **부분적** — 무엇까지 되고 어디서 막히는지 (예: 파일 접근은 되나 복호화 키 불명).
   - (C) **구조가 달라 다른 접근 필요** — Windows 는 X 방식(근거)이라 macOS 모델은 못 쓴다. 그럼 대안 방향을 근거와 함께 1~2개 제시.
   - (D) **로컬에 없다** — 대화가 로컬에 영속 저장되지 않아 추출 자체가 불가.

## 7. 범위 제약 — 하지 말 것

- **카톡을 종료·재시작·kill 하지 마라.** 파일 잠김은 잠김으로 보고. 프로세스 제어는 코디/사용자 몫.
- **원본 파일에 쓰지 마라.** 읽기만. 필요하면 워크트리 안으로 복사해서 다룬다 (단 대화 원본은 복사도 최소화, 커밋 금지).
- **키·user_id·device UUID·실제 대화 내용을 코드·테스트·리포트·커밋에 남기지 마라.** 값은 `<redacted>`.
- 억지로 동작을 지어내지 마라. 안 되면 (C)/(D) 가 정답이다.
- `frontend/`·`worker/`·compose·문서 SoT 수정 금지. git commit·push·PR 금지.
- `requirements.txt` 에 무거운 의존성을 함부로 추가하지 마라 (ESE 리더 등 꼭 필요하면 **먼저 보고**). sqlcipher3 는 Windows 휠이 없을 수 있다 — 설치 실패하면 그 사실을 기록.

## 8. 검증

```
탐색이라 통상 테스트 스위트가 없다. 대신:
- 순수 함수(포맷 판별·후보 키 생성)를 backend/tests/ 에 테스트로 남기고 `python -m pytest -q backend/tests/<그 파일>` 로 확인 (전체 스위트 금지).
- python 은 있으나(3.12) sqlcipher3 는 미설치일 수 있다 — 설치 시도해 보고, 실패하면 "sqlcipher3 Windows 설치 실패: <에러>" 로 보고. DB 실복호는 그 경우 못 한다고 정직하게 남긴다.
- 조사 스크립트는 재현 절차(명령 한 줄)를 리포트에 적는다.
```

- 못 돌린 검증은 통과했다고 쓰지 마라 — 못 돌렸다고 쓴다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

---

## 2. 스파이크 2 — 키 복구 (메모리)

<sub>원본: `poc-windows-key-re/poc-windows-key-re-be-brief.md`</sub>

# [backend] KakaoTalk.exe 키 파생 리버스 — 라이브 훅으로 키·스키마 포착 (spike 2)

너는 **mykakao `backend` 워커**다. **이건 직전 spike(poc-windows-key-derivation)의 후속이다** — 너는 이미 그 조사를 했으니 맥락을 갖고 있다. 역할 문서를 다시 볼 필요는 없지만 규칙은 그대로 적용된다(안전 규칙 특히).

작업 워크트리: `C:/Users/sc971/orca/workspaces/mykakao/poc-windows-key-derivation` (직전과 **같은 워크트리** — probe_windows.py·PROBE_REPORT.md 가 거기 있다)
base: `origin/main` → ⚠ **PR 없음. 이것도 spike다.**

> ⚠ **목표는 "되게 만들라"가 아니라 "관측하고 판정하라".** KakaoTalk.exe 가 실제로 어떻게 키를 만드는지를 **살아있는 프로세스에서 관측**해, ① SQLCipher 키를 포착하고 ② 그 키로 무엇을(어떤 테이블/DB) 여는지 확인한다. 억지 복호 지어내기 금지.

## 1. 배경 — 직전 spike 결론에서 출발

직전 판정: macOS 파생식은 Windows 에서 22개 후보 전부 복호 실패. `ActionLogDB.edb` 는 SQLCipher(WAL)지만 대화 저장소인지 **미확증**(이름·크기 기반 추정). macOS 78-hex 메시지 DB 는 디스크에 없음.

**사용자 결정: KakaoTalk.exe 의 키 파생을 리버스한다.** 정적 디스어셈블보다 **동적 훅이 우선**이다 — 실행 중 프로세스에서 키와 스키마 접근을 동시에 잡으면, "ActionLogDB 에 대화가 있나"라는 미결까지 한 번에 답이 나온다.

## 2. 방법 — 우선순위대로

**KakaoTalk 26.4.0.5128 이 현재 실행 중이다** (PID 존재 확인됨). 라이브 훅 가능.

1. **동적 훅 (1순위 — Frida)**:
   - `pip install frida-tools` (env 한정 — requirements.txt 에 넣지 마라. 설치 실패하면 그 사실 기록).
   - 실행 중 `KakaoTalk.exe` 에 attach. SQLCipher 진입점을 후킹한다:
     - `sqlite3_key` / `sqlite3_key_v2` (SQLCipher passphrase 진입) — export 되어 있으면 이름으로, 정적링크면 문자열(`PRAGMA key`, `SQLite format 3`, SQLCipher provider 문자열)로 루틴을 찾아 offset 훅.
     - `sqlite3_prepare_v2` / `sqlite3_exec` — 실행되는 SQL·테이블명을 관측 → **ActionLogDB 가 무엇을 담는지, 다른 DB 를 여는지** 드러난다.
     - `sqlite3_open`/`open_v2` 또는 CreateFile — 어떤 DB 파일들을 여는지.
   - 후킹 대상 모듈: `KakaoTalk.exe` 본체 · `Vox.dll`/`Vox3.dll` 등 동봉 DLL 도 후보(SQLCipher 가 어디 링크됐는지 확인).
2. **정적 폴백 (동적이 막히면)**: `strings`/Ghidra 로 `KakaoTalk.exe`·DLL 에서 키 파생 상수·PBKDF2 흔적·macOS 의 `hawawa`/`secure_key` 파생 패턴 대응물을 찾는다.
3동적이 anti-tamper 로 막히면 **막혔다고 보고**하고 정적으로 전환. 무리하게 보호를 무력화하지 마라.

## 3. 안전 규칙 — 반드시

이건 **본인 기기·본인 앱·본인 데이터**다 (레포의 macOS extract.py 도 kakaocli 를 RE 해 얻은 것 — 같은 성격의 개인용 작업이다). 그러나:

- **카톡을 크래시·변조·종료하지 마라.** 관측/훅만. 프로세스 메모리에 Frida 트램폴린 외 쓰기 금지. 끝나면 clean detach.
- **OS 보안을 끄거나 커널로 escalate 하지 마라.** anti-debug 가 attach 를 막으면 그 사실을 보고. 우회에 매달리지 마라.
- **포착한 키·user_id·device UUID·대화 내용을 절대 평문 출력·로깅·커밋하지 마라.** 리포트엔 "키 포착: 예/아니오 (N바이트, 마스킹)" 와 **파생식(입력+공식)** 만. 값은 `<redacted>`.
- 대화 내용이 관측되면 스키마·테이블명·행수만 적고 **본문은 인용 금지**.
- 원본 DB·plist·레지스트리에 쓰기 금지. 읽기만.

## 4. 산출물

- `backend/re_probe.py` (또는 frida 스크립트 `backend/hook_kakao.js` + 러너) — 재현 가능한 훅. 명령 한 줄로 재현되게.
- `backend/RE_REPORT.md` — 판정 + 근거. 직전 PROBE_REPORT.md 를 덮지 말고 별도 파일.
- 순수 함수 있으면 `backend/tests/` 에 테스트.

## 5. allowed_paths

- `backend/`
- (frida-tools 설치는 env 한정 — `requirements.txt` 수정하려면 먼저 보고)

## 6. 판정 (아래 중 하나 + 근거)

- **(A) 키 포착 + 파생식 확인** → Windows 경로 실현 가능. 어떻게인지 명시. + ActionLogDB 실내용(대화 유무).
- **(B) 키는 포착됐으나 ActionLogDB 에 대화 없음** → 직전 (D) 확증: 로컬 추출 무의미. 대화는 어디서 오나(서버/메모리) 관측된 대로.
- **(C) 동적·정적 모두 막힘** → 무엇이(anti-tamper·툴 부재) 막았는지, 뚫으려면 뭐가 필요한지.

## 7. 검증

```
- 순수 함수는 backend/tests/ 에 테스트 + `python -m pytest -q backend/tests/<파일>`.
- 훅 스크립트는 재현 절차(명령)를 리포트에 명시. 실제 키/대화는 마스킹.
- 못 한 것은 못 했다고 쓴다.
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이라 늙었을 수 있다. preamble 과 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만.
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --from <네 워커handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> \
  --dispatch-id <preamble 의 dispatchId> \
  --subject "backend 완료(RE): <한 줄>" \
  --body "판정(A/B/C) / 키 포착 여부(마스킹) / 파생식 / ActionLogDB 대화 유무 / 산출물 / 미결"

orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 \
  --text "[worker_done] backend RE 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --text "[질문] backend: <질문>" --enter`

---

## 3. 스파이크 3 — 키 복구 확정

<sub>원본: `poc-windows-key-recover/poc-windows-key-recover-be-brief.md`</sub>

# [backend] KakaoTalk Windows SQLCipher 키 파생식 회수 (spike 3 — B경로)

너는 **mykakao `backend` 워커**다. **spike 1·2 를 네가 했다** — 맥락 있다. 규칙(특히 안전규칙) 그대로.

작업 워크트리: `C:/Users/sc971/orca/workspaces/mykakao/poc-windows-key-derivation` (spike 1·2 와 **같은 워크트리** — probe_windows.py·mem_probe.py·RE_REPORT.md 있음)
base: `origin/main` → ⚠ **PR 없음. spike 다.**

> ⚠ 목표: **SQLCipher 키 파생식(공식)을 회수**해, 그걸로 실제 `chatLogs_*.edb` 를 복호할 수 있음을 증명한다. 사용자 결정 = **B경로**(A 라이브추출 아님). 이식 가능한 복호가 목표다.

## 1. 판을 바꾼 새 사실 (spike 1·2 이후 변화)

**사용자가 방금 카톡에 로그인했다.** 그 결과 spike 조사 때 없던 것들이 생겼다 — 코디가 확인:

- 계정 데이터 폴더: `%LOCALAPPDATA%\Kakao\KakaoTalk\users\<40hex 계정폴더>\`
- 그 안 `chat_data\` 에 **방별 실제 대화 DB**: `chatLogs_18361720661829832.edb`(1.4MB), `chatLogs_18332626660210452.edb`, `chatLogs_18289824252298381.edb`, `chatListInfo.edb` + 상위에 `TalkUserDB.edb`(712KB)·`CalendarDB.edb`·`emoticon.edb`.
- 이들도 **SQLCipher 암호화 확정** — `chatLogs_18361...edb` 헤더 랜덤, 엔트로피 **7.997**. (spike 2 의 ActionLogDB 와 같은 계열.)
- 레지스트리 `HKCU\Software\Kakao\KakaoTalk\`: `UserAccounts\<계정 이메일>`(uuid_v1_auth), `NewTiara`(tuid/uuid 토큰), `DeviceInfo`(sys_uuid/dev_id/hdd_serial — spike1 확인).

**이게 왜 중요한가**: spike 2 엔 없던 **정답지**가 생겼다. 후보 키/파생식을 만들면 **실제 `chatLogs_*.edb` 사본을 sqlcipher3 로 열어 성공을 즉시 검증**할 수 있다("열려서 테이블·행이 보이면 정답"). 억지 없이 falsification 가능.

## 2. 접근 — 우선순위

**패킹 우회 = 실행중 메모리 덤프**(SAC 안전, passive). **동적 주입(Frida)은 금지**(SAC ENFORCE, spike2 확증).

1. **언패킹된 코드 확보 (1순위)**: KakaoTalk 실행 중(PID 확인) → `mem_probe.py` 식 passive `VM_READ` 로 **KakaoTalk.exe / Vox*.dll 의 언패킹된 코드 섹션을 메모리에서 덤프**(디스크는 패킹돼 문자열 0개였음, RAM 엔 복호본이 있음). 스레드주입·쓰기 없음.
2. **정적 분석**: 덤프에서 SQLCipher 진입(`sqlite3_key`/`PRAGMA key`/`sqlcipher` 문자열·상수·PBKDF2)과 **passphrase 조립 루틴**을 찾는다. macOS `secure_key()`(hawawa·PBKDF2-HMAC-SHA256·salt=uuid 부분열)가 **알려진 reference** — Windows 대응식이 device 식별자(sys_uuid/dev_id/MachineGuid)+user_id 를 어떻게 섞는지 역추적.
3. **서명 계측 (2순위 폴백)**: 정적이 막히면 **WinDbg**(Microsoft 서명 — SAC 이 Frida 처럼 막지 않을 가능성) 로 `sqlite3_key` 호출부에 BP → passphrase 원값 포착 + 그 값을 조립한 코드 역추적. WinDbg 설치·사용은 **먼저 코디에 보고**하고 진행.
4. **SQLCipher 파라미터 규명**: 파생식만이 아니라 **cipher 버전(compat 3 vs 4)·page_size·kdf_iter·HMAC** 도 맞아야 열린다. 파일 헤더 salt(첫 16B)는 KDF 입력. sqlcipher3 로 열 때 `PRAGMA cipher_compatibility`/`cipher_page_size` 조합을 체계적으로 시도.

## 3. 성공 판정 (정답지 활용)

- `chatLogs_18361720661829832.edb` **사본**(워크트리 밖 스크래치패드로 복사 — 원본 쓰기 금지)을 sqlcipher3-wheels 로 열어:
  - `PRAGMA key="<파생키>"` + 맞는 cipher 파라미터 → `SELECT count(*) FROM sqlite_master` 성공 = **키 확인**.
  - 테이블·행수만 보고. **대화 본문은 읽지도 인용하지도 마라.**
- 성공하면 **파생식(입력→공식→파라미터)** 을 재현 가능하게 문서화. 키 원값은 `<redacted>`.

## 4. 안전 규칙 — 반드시 (spike1·2 와 동일)

- 본인 기기·본인 앱·본인 데이터 (레포 macOS extract.py 와 동일 성격의 개인용).
- **카톡 크래시·변조·종료 금지.** passive read 만. 프로세스 메모리 쓰기 금지. **SAC 끄지 마라·건드리지 마라.** anti-tamper 우회 금지.
- **원본 DB·plist·레지스트리 쓰기 금지.** DB 는 **사본으로만** 작업 (스크래치패드, 워크트리 밖, 커밋 금지).
- **키·user_id·device UUID·대화 본문 절대 평문 출력·로깅·커밋 금지.** 리포트엔 파생식 구조·테이블명·행수만. 값 `<redacted>`.
- 무거운 도구(WinDbg·Ghidra) 설치는 **먼저 보고**.

## 5. allowed_paths

- `backend/`
- (sqlcipher3-wheels 는 이미 env 설치됨. WinDbg/Ghidra 등은 보고 후. `requirements.txt` 수정은 보고 후)

## 6. 판정

- **(A) 파생식 회수 + 실복호 성공** → Windows 경로 완성. 파생식·파라미터 명시. mykakao Windows 이식 가능.
- **(B) 키 원값은 포착(WinDbg 등) 했으나 파생식 미완** → 반쪽. 무엇이 남았나.
- **(C) 둘 다 막힘** → 무엇이(패킹 난이도·anti-debug·도구부재) 막았나, 뚫으려면 뭐가 필요한가.

## 7. 검증

```
- 핵심 검증 = chatLogs_*.edb 사본 실복호 성공(테이블/행수 확인, 본문 미열람).
- 순수 함수(파생식 구현·파라미터 판별)는 backend/tests/ 에 테스트 + `python -m pytest -q backend/tests/<파일>` (전체 스위트 금지 — test_summarize.py 는 open_kknaks 미설치라 collection 에러, 무관).
- 못 한 것은 못 했다고. 실복호 성공/실패를 정직히.
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 값을 믿어라.** 아래 코디handle 이 preamble 과 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만.
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --from <네 워커handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> \
  --dispatch-id <preamble 의 dispatchId> \
  --subject "backend 완료(키회수): <판정 A/B/C — 한 줄>" \
  --body "판정 / 파생식 회수 여부 / chatLogs 실복호 성공여부(테이블·행수, 본문 미열람) / 파라미터 / 산출물 / 미결"

orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 \
  --text "[worker_done] backend 키회수 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --text "[질문] backend: <질문>" --enter`

---

## 4. WORK-003 — win_app P1 (러스트 착수)

<sub>원본: `work-003-winapp-p1/work-003-winapp-p1-winapp-brief.md`</sub>

# [winapp] Windows V2 P1 — 방 선택 + 과거 히스토리 복호·저장 (Rust win_app 스캐폴드)

너는 **mykakao `winapp` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/orchestration/roles/mykakao/winapp/role.md` (+ 같은 폴더 rules·skills·tools·workflow)

작업 워크트리: `C:/Users/sc971/orca/workspaces/mykakao/work-003-winapp-p1`
base: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다). 이건 **실제 코드 작업 = 커밋/PR 대상**(spike 아님).

이 워크트리는 너 혼자 쓴다. `win_app/` 은 아직 없다 — **네가 새로 만든다.** macOS `backend/`(Python)·`frontend/` 는 **건드리지 마라.**

## 1. SSOT — 먼저 읽을 것 (전부 read-only 절대경로)

- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/20-spec/spec-003-windows-v2.md` ← **계약 SoT.** API·UX·BE 메커니즘·SQLite 스키마·win_app 레이아웃. **여기 없는 건 발명하지 마라.**
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/10-decision/decision-003-windows-v2-approach.md` ← 4결정(키=메모리회수/저장=SQLite/실시간=파일감시/Rust·win_app). P1 은 실시간(P2)·트레이(P3) 제외.
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/00-baseline/baseline-003-windows-tray-realtime-accumulation.md` ← UX 구조·전체 그림.

**참조 코드 (spike 3 — 알고리즘 포팅 원천, read-only):**
- `C:/Users/sc971/orca/workspaces/mykakao/poc-windows-key-derivation/backend/key_recover.py` ← 메모리 키 회수(ReadProcessMemory) + SQLCipher v4 page-1 HMAC-SHA512 검증. **이걸 Rust 로 포팅.**
- `C:/Users/sc971/orca/workspaces/mykakao/poc-windows-key-derivation/backend/key_analysis.py` ← 실복호·행수 확인 로직.
- `C:/Users/sc971/orca/workspaces/mykakao/poc-windows-key-derivation/backend/KEY_REPORT.md` ← **SQLCipher v4 파라미터 정본** (compat4·page4096·reserve80·HMAC key 유도·page IV).

## 2. 배경 / 무엇을 만드나

Windows 카톡 대화 DB(`chatLogs_<chatId>.edb`, SQLCipher v4)를 실행 중 카톡 메모리에서 회수한 raw key 로 복호해, 선택한 방의 과거 히스토리를 우리 로컬 SQLite 에 저장한다. spike 3 에서 1455행 실복호가 이미 증명됐다 — 그 알고리즘을 **Rust 로 제품화**하는 게 P1 이다.

**P1 범위(이번):** `win_app/` Rust 크레이트 스캐폴드 + 메모리 키회수 + 페이지 복호 + SQLite 저장 + axum API 5개 + 설정 HTML(3섹션+2pane).
**P1 아님:** 실시간 파일감시(P2), 트레이 아이콘(P3).

## 3. 계약 (SPEC-003 §FE/BE Contract 그대로 — 요지)

axum API (응답 키·경로 그대로):
- `GET /api/state` → `{kakao_running, logged_in, recoverable_rooms:[chatId], account?}`
- `GET /api/rooms` → `[{chat_id, title, member_count?, selected}]`
- `POST /api/rooms/select` body `{chat_ids:[...]}` → `{ok, selected:[...]}`
- `POST /api/import` body `{chat_id?}` → `{ok, imported:{chat_id:count}}`
- `GET /api/messages?chat_id=&after=&limit=` → `[{log_id, author_id, author_name?, type, sent_at, text}]`

SQLite 스키마: SPEC-003 §Data Contract (room/message/author, message PK=(chat_id,log_id) 멱등 upsert).

## 4. 복호 전략 (rules.md 참고 — OpenSSL 회피)

- 키는 메모리 raw key(32B) — main key KDF 불필요.
- **순수 Rust 크립토**(`aes`+`cbc`+`hmac`+`sha2`+`pbkdf2`)로 SQLCipher v4 페이지 복호 → **평문 SQLite** 로 떨군 뒤 `rusqlite`(feature `bundled`, 평문)로 연다. **bundled-sqlcipher/OpenSSL 쓰지 마라**(Windows 빌드 지옥).
- 파라미터는 KEY_REPORT.md 정본: compat4, page4096, reserve80(IV16+HMAC64), HMAC key=`PBKDF2-HMAC-SHA512(raw_key, salt⊕0x3a, 2, 32)`, page IV=페이지 reserve 앞16B, AES-256-CBC.
- **이 전략이 막히면 구현 전에 코디에 보고**하고 대안 상의.

## 6. 구현 단계

1. cargo 동작 확인(`cargo --version`; 없으면 `export PATH="$HOME/.cargo/bin:$PATH"`). `win_app/` 크레이트 생성.
2. **복호 코어 먼저**: 메모리 키회수(windows crate) + 페이지 복호(순수 Rust) → 평문 SQLite. 순수 함수(HMAC 검증·페이지 복호)는 **합성 픽스처로 cargo test**.
3. 저장: rusqlite 축적 DB(room/message/author).
4. import: 선택 방 키회수 → 복호 → `chatLogs` 행을 우리 SQLite 에 upsert(logId 커서).
5. axum API 5개 + `ui/` 정적 서빙.
6. `ui/index.html`: 설정 3섹션(로그인 상태 감지 / 대화방 설정 / 채팅 내역 2-pane). vanilla HTML/JS, 계약 키 그대로.

## 7. 범위 제약 — 하지 말 것

- **카톡 크래시·변조·종료 금지.** 메모리 ReadProcessMemory **읽기만**(쓰기·주입 금지). SAC 미변경.
- **원본 DB·레지스트리 쓰기 금지.** 복호는 **사본**(임시, 작업 후 삭제).
- **키·user_id·device UUID·대화 본문·계정 식별자를 로그·테스트·리포트·커밋에 남기지 마라.** 마스킹/`<redacted>`. 계정 폴더 해시는 자동 탐색(하드코딩 금지).
- 실복호 검증 시 **행수만 보고**(spike3처럼), 본문 인용 금지.
- `win_app/` 밖·문서 SoT 수정 금지. P2(파일감시)·P3(트레이) 구현하지 마라. git commit·push·PR 금지.
- 크레이트 추가는 최소로. 무거운 결정은 보고.

## 8. 검증

```
cd win_app && cargo build (에러 0, 경고 허용) + cargo test <네가 만든 테스트>. cargo 는 ~/.cargo/bin, MSVC 링킹 자동.
- 순수 함수(HMAC 검증·페이지 복호)는 합성 픽스처 테스트로 확인(실 DB 불필요).
- 실기동(카톡 대상 실복호·행수)은 하되 **본문 미열람·행수만**. 못 하는 환경이면 못 했다고 보고 — 통과했다 쓰지 마라.
- 검증은 1회만.
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "winapp 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 \
  --text "[worker_done] winapp 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --text "[질문] winapp: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

---

## 5. P2 — 실시간 후킹

<sub>원본: `work-003-winapp-p1/p2/p2-brief.md`</sub>

# [winapp] Windows V2 P2 — 실시간 파일감시 → 델타 복호 → SSE 축적

너는 **mykakao `winapp` 워커**다. **P1 을 네가 방금 완성했다** — 같은 워크트리·같은 크레이트를 이어서 확장한다. 역할 문서 규칙(특히 안전·자원 규칙) 그대로.

작업 워크트리: `C:/Users/sc971/orca/workspaces/mykakao/work-003-winapp-p1` (P1 과 **같은 워크트리**, `win_app/` 이미 있음)
base/브랜치: `work-003-winapp-p1` (P1 커밋 `1fa8a18` 위에 이어서). PR 은 코디.

> 목표: P1 의 과거 import 위에 **실시간 축적**을 얹는다. 카톡이 그 방에 새 메시지를 쓰면 파일 변경을 감지해 **새 행만** 복호·저장하고 화면에 스트리밍한다. **함수 주입 후킹 아님**(SAC) — OS 파일 감시다.

## 1. SSOT — 먼저 읽을 것 (read-only 절대경로)

- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/20-spec/spec-003-windows-v2.md` §BE Contract 「실시간 축적 (P2)」 + §FE Contract `/api/stream` ← **계약 SoT**.
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/10-decision/decision-003-windows-v2-approach.md` 결정3(실시간=파일감시→델타복호→append→SSE) + 결정4.
- **P1 코드**(이 워크트리 `win_app/`): `import.rs`(델타 로직 재사용)·`store.rs`(커서·upsert)·`server.rs`(라우터·AppState).

## 2. 무엇을 만드나

P1 은 수동 import(과거)였다. P2 는 **자동 실시간**:
- 선택된 방들의 `chat_data` 를 감시하다 `chatLogs_<chatId>.edb-wal` 변경 시 → 그 방 델타(logId>커서) 복호 → SQLite append → SSE 로 push.
- 델타 복호는 P1 의 import 로직을 재사용(전체 재복호 금지 — 커서 이후만).

## 3. 계약 (SPEC-003 §FE Contract)

- `GET /api/stream?chat_id=` → SSE, `event: message`, payload = P1 `/api/messages` 행 shape(`{log_id,author_id,author_name?,type,sent_at,text}`). 이벤트명·키 그대로.
- 기존 5개 API 는 불변.

## 4. 구현 (win_app/ 확장)

1. `src/watch.rs` 신규: `notify` crate 로 선택 방들의 `chat_data` dir 감시(내부 ReadDirectoryChangesW). `-wal` 변경 이벤트 → 해당 chat_id 델타 동기 트리거.
2. 델타 파이프: import.rs 의 「키회수 → 복호 → 커서 이후 행 → upsert」를 재사용. **전체 재복호 금지.**
3. SSE: `GET /api/stream`. tokio **broadcast 채널(바운드 용량)** 로 새 행 fan-out. **lagging 수신자는 drop**(무한 버퍼 금지). 연결 종료 시 정리.
4. `ui/index.html`: 채팅 내역 2-pane 에서 선택 방의 `EventSource('/api/stream?chat_id=')` 구독 → 새 말풍선 append. 재연결 처리.
5. 감시 누락 폴백(선택): 저빈도 주기 재동기(옵션, 무한 폴링 아님).

## 5. allowed_paths

- `win_app/` (P1 확장). 밖은 금지.

## 6. 자원·안전 (상주 앱 — 이게 P2 의 핵심 리스크)

- **SSE 무한 버퍼 금지** — bounded broadcast, lagged 수신자 drop. 연결 끊기면 태스크·수신자 정리(누수 금지).
- **파일 워처 수명 관리** — 선택 방만 감시. 선택 변경 시 watcher 재구성(핸들 누적 금지). 종료 시 clean stop.
- **델타만 복호** — 이벤트마다 전체 DB 재복호하지 마라(CPU·임시본 폭증). 커서 이후만.
- **복호 임시본 RAII 삭제**(P1 방식 유지). **키 비상주**(요청/이벤트마다 회수·폐기).
- 카톡 크래시·변조·종료 금지. 원본 읽기만. SAC 미변경. **키·본문·계정 식별자 로그·커밋 비노출**(마스킹).
- 실 스트림 검증 시 **행수/이벤트 수만**, 본문 미열람.

## 7. 하지 말 것

- P3(트레이) 구현 금지. 기존 5개 API·P1 복호 코어 계약 변경 금지(어긋나면 보고).
- 함수 주입 후킹·Frida 금지(SAC). 전체 재복호·무한 폴링·무한 SSE 버퍼 금지.
- `win_app/` 밖·문서 SoT 수정 금지. git commit·push·PR 금지.

## 8. 검증

```
cd win_app && cargo build(에러0) + cargo test<네 테스트>. cargo=~/.cargo/bin.
- 순수/단위 가능한 것(델타 선별·SSE 페이로드 직렬화)은 테스트.
- 실스트림: 서버 띄우고(코디가 실카톡으로 최종 확인 가능) 이벤트 수/행수만. 못 하면 못 했다고.
- 검증 1회.
```

## 9. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 검증·커밋·PR 은 코디.
- 끝나면 **아래 두 명령 모두** 실행.

```bash
orca orchestration send   --to term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --from <네 워커handle>   --type worker_done   --task-id <preamble taskId> --dispatch-id <preamble dispatchId>   --subject "winapp P2 완료: <한 줄>"   --body "구현/파일 / cargo 수치 / SSE·워처 자원처리 / 계약 준수 / 미결"

orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3   --text "[worker_done] winapp P2 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --text "[질문] winapp: <질문>" --enter`

---

## 6. P3 — 트레이 + 이름

<sub>원본: `work-003-winapp-p1/p3/p3-brief.md`</sub>

# [winapp] Windows V2 P3 — 트레이 앱 + 로그인 상태 상시화 (+ 닉네임 조인)

너는 **mykakao `winapp` 워커**다. **P1·P2 를 네가 완성했다** — 같은 워크트리·크레이트를 이어서 마무리한다. 안전·자원 규칙 그대로.

작업 워크트리: `C:/Users/sc971/orca/workspaces/mykakao/work-003-winapp-p1` (P1·P2 와 같은 워크트리)
브랜치: `work-003-winapp-p1` (P2 커밋 `e008fb6` 위에 이어서). PR 은 코디.

> 목표: 지금은 콘솔로 서버가 뜬다. P3 는 이걸 **트레이 상주 앱**으로 만든다 — 작업표시줄(트레이) 아이콘 클릭 → 기본 브라우저로 localhost 설정 페이지 열림. + 로그인 상태 상시 감지. 마지막 마감 단계다.

## 1. SSOT (read-only 절대경로)

- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/20-spec/spec-003-windows-v2.md` §UX Contract + 「P3」 + §Work Handoff(WORK-005 = 트레이 tray-icon + 로그인 상태 상시화).
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/00-baseline/baseline-003-windows-tray-realtime-accumulation.md` §UX 구조(트레이→설정 3섹션).
- **P1·P2 코드**(이 워크트리): `main.rs`(현재 콘솔 기동)·`server.rs`(AppState·/api/state·enrich_titles)·`ui/index.html`(3섹션).

## 2. 무엇을 만드나

1. **트레이 아이콘**(`tray-icon` crate): 상주 앱. 좌클릭(또는 메뉴 "설정 열기") → 기본 브라우저로 `http://127.0.0.1:<port>` 오픈(`open`/`ShellExecute`/`webbrowser`). 우클릭 메뉴 = 「설정 열기」·「종료」.
2. **이벤트 루프 ↔ tokio 공존**: 트레이 이벤트 루프(메인 스레드)와 axum(tokio) 서버가 한 프로세스에서 함께 돌게. 서버는 백그라운드 스레드/런타임, 트레이는 메인. busy-loop 금지.
3. **로그인 상태 상시화**: 설정 페이지 ① 섹션이 `/api/state` 를 **적정 주기**(예 3~5s, 타이트 루프 금지)로 폴링해 카톡 실행/로그인/회수가능 방 수를 갱신. 미실행이면 안내 배너.
4. **콘솔 창**: 트레이 앱이므로 콘솔 숨김 고려(`#![windows_subsystem = "windows"]`). 숨기면 로그는 **파일로**(예 `%LOCALAPPDATA%\mykakao\win_app.log`) — 단 키/본문 절대 로깅 금지. (디버그 편의로 콘솔 유지도 허용 — 판단해 보고.)
5. **닉네임 조인(마감 폴리시)**: 지금 `author_name` 이 null 이다. `TalkUserDB.edb`(`talkUser`: userId·nickName)를 복호해 author_id→nickName 매핑을 `author` 테이블/조인에 채워 채팅 내역에 이름이 뜨게. (본문 아님·닉네임은 표시 목적. 로그 노출 금지.)

## 3. 계약

- 기존 6개 API(state/rooms/rooms.select/import/messages/stream) **불변**. 트레이는 API 를 추가하지 않아도 된다(브라우저 오픈만). 필요 시 `/api/quit` 같은 건 만들지 말고 트레이 메뉴로.
- `/api/messages` 응답의 `author_name` 이 이제 채워짐(계약 shape 동일, null→값).

## 4. allowed_paths

- `win_app/`. 밖 금지.

## 5. 자원·안전 (상주 앱 — P3 핵심)

- **이벤트 루프 busy-loop 금지** — 트레이/이벤트 대기는 블로킹 수신. 폴링 주기 타이트 금지.
- **트레이·아이콘 리소스 정리** — 종료 시 clean. 스레드/런타임 누수 금지.
- 로그인 폴링은 서버 부하 낮게(주기 여유). `/api/state` 는 메모리 스캔을 하므로 P1 의 last_refresh 스로틀 유지·활용.
- 닉네임 조인 시에도 **원본 읽기만·복호 임시본 RAII·키 비상주** 유지. TalkUserDB 도 사본/읽기전용.
- **키·본문·닉네임 원값·계정 식별자 로그·커밋 비노출.** 콘솔 숨기고 파일 로그 쓰면 거기에도 금지.
- 카톡 크래시·변조·종료 금지. SAC 미변경. Windows 시작프로그램 자동등록은 **하지 마라**(시스템 변경 — 원하면 후속/옵션).

## 6. 하지 말 것

- 시작프로그램 레지스트리 자동 등록 금지. 새 무거운 크레이트 남발 금지(tray-icon + 필요한 이벤트루프 정도).
- 기존 API 계약·복호 코어 변경 금지(어긋나면 보고). `win_app/` 밖·문서 SoT 수정 금지. commit·push·PR 금지.

## 7. 검증

```
cd win_app && cargo build(에러0) + cargo test. cargo=~/.cargo/bin.
- 트레이는 GUI라 자동 테스트 어렵다 — 빌드 성공 + 수동 기동으로 트레이 아이콘·브라우저 오픈 동작을 육안 확인(코디가 최종 실기동). 못 한 건 못 했다고.
- 닉네임 조인은 단위 테스트(합성) + 실기동 행수/이름 유무만(본문·닉네임 원값 미출력).
- 검증 1회.
```

## 8. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령 모두** 실행.

```bash
orca orchestration send   --to term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --from <네 워커handle>   --type worker_done   --task-id <preamble taskId> --dispatch-id <preamble dispatchId>   --subject "winapp P3 완료: <한 줄>"   --body "구현/파일 / 트레이·이벤트루프 방식 / 닉네임 조인 / cargo 수치 / 자원처리 / 미결"

orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3   --text "[worker_done] winapp P3 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --text "[질문] winapp: <질문>" --enter`

---

## 7. FIX — 이름 해석

<sub>원본: `work-003-winapp-p1/fix-names/fix-names-brief.md`</sub>

# [winapp] Windows V2 수정 — 방/작성자 실이름 해석 + import 대상·UX

너는 **mykakao `winapp` 워커**다. **P1~P3 를 네가 만들었다** — 같은 워크트리·크레이트를 수정한다. 안전·자원 규칙 그대로.

워크트리: `C:/Users/sc971/orca/workspaces/mykakao/work-003-winapp-p1` (P3 커밋 `3583361` 위에)
브랜치: `work-003-winapp-p1`. PR 은 코디. **커밋 금지.**

> 사용자가 실기동해서 두 결함을 찾았다. 실제 데이터로 검증하며 고쳐라 — 단위테스트만으로 "됐다" 하지 마라.

## 1. 사용자가 발견한 결함 (코디 실측 확인)

**(A) 방/작성자 이름이 전부 난수(chatId·userId)로 뜬다.**
- 코디 진단: `/api/rooms` **51개 방 중 실이름 해석 = 0개** (전부 "대화방 <chatId>" fallback). 네가 P3 에서 넣은 닉네임 조인·enrich_titles 가 **실경로에서 작동 안 함**.
- **데이터는 있다**: `TalkUserDB.edb`(닉네임)·`chat_data/chatListInfo.edb`(방 목록/제목) 둘 다 **카톡이 열고 있어(잠김) 복호 가능**. 즉 못 고칠 문제가 아니라 **코드/스키마 버그**다.
- 사용자 요구: 방 이름이 **단체방인지 1:1인지** 구분되고 실제 이름이 보여야 한다. 1:1 이면 상대 이름, 단체면 방 제목/멤버.

**(B) "과거 가져오기" 가 0행 + 엉뚱한 방을 가져온다.**
- 사용자가 방 `15034819498347`(체크)를 골랐는데 결과는 `#906847525:0`(③에서 보던 방). 즉 **import 가 체크된 방이 아니라 ③ 뷰어의 방을 가져왔다.** 게다가 그 방은 "닫힘"이라 키가 없어 0행.
- 근본 제약: **키는 그 방이 카톡에서 "열림"일 때만 메모리에 있다.** 지금 열린 방은 소수(3개). 닫힌 방은 import 불가.

## 2. 고칠 것

### (A) 실이름 해석 — 최우선
1. `chatListInfo.edb` + `TalkUserDB.edb` 를 **실제 복호해 스키마를 직접 확인**하라(테이블·컬럼). P3 의 가정이 틀렸으니 **실 데이터로 재확인**. (복호는 P1 decrypt 파이프 재사용. 사본·읽기전용·임시본 RAII.)
2. **방 제목 해석**: 단체방 → 제목(subject/title). 1:1 → 상대 userId 의 nickName. **방 타입(group/direct) + 멤버수**를 산출.
3. **작성자 해석**: TalkUserDB userId→nickName 로 `/api/messages`·SSE 의 `author_name` 채움(지금 0개 해석 → 실제 이름).
4. `/api/rooms` 응답에 `title`(실이름) + `kind`("group"/"direct") + `member_count` 추가. UI ②③ 에서 "단체/개인" 과 실이름 표시.

### (B) import 대상 + UX
5. **"과거 가져오기" 는 ② 체크된 방들을 가져온다**(③ 뷰어 방 아님). 여러 개면 각각.
6. **열림 방만 import**. 닫힌 방을 고르면 스킵하고 명확히 안내: "이 방은 닫혀 있음 — 카톡에서 방을 열고 다시 시도". ①/② 에 열림/닫힘을 정확히 표시(이미 badge 있음 — 정확성 확인).
7. (선택) import 버튼 옆 안내: "열린 방만 가져올 수 있어요. 카톡에서 방을 여세요."

## 3. 안전 (불변)

- 실 방제목·닉네임·본문은 **UI 응답에만**. **로그·리포트·커밋·진단출력에 절대 남기지 마라**(마스킹/카운트만). applog 규율 유지.
- 원본 read-only, 복호 사본 RAII 삭제, 키 비상주, 카톡 무변조, SAC 미변경.
- 스키마 확인용 복호 출력도 **컬럼명·행수만**, 값(이름/본문) 미출력.

## 4. allowed_paths / 범위

- `win_app/` 만. 새 crate 추가 금지(SAC — proc-macro/build-script 새로 끌면 또 막힌다). 부득이하면 보고.
- 계약 변경(응답에 필드 추가는 OK, 기존 키 의미 변경은 보고).

## 5. 검증

```
cd win_app && cargo build --release(SAC 통과 필수, 차단0) + cargo test. cargo=~/.cargo/bin.
- **실 데이터 검증**: 열린 방 하나로 /api/rooms 가 실제 방이름·kind·member_count 를 주는지, /api/messages author_name 이 실제 닉네임인지 **개수/유무만** 확인(이름 원값 미출력).
- 닫힌 방 import 시 스킵+안내 동작 확인.
- 검증 1회. 못 한 건 못 했다고.
```

## 6. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령 모두** 실행.

```bash
orca orchestration send   --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle>   --type worker_done   --task-id <preamble taskId> --dispatch-id <preamble dispatchId>   --subject "winapp 이름해석 수정 완료: <한 줄>"   --body "chatListInfo/TalkUserDB 실스키마 / 방이름·kind·author 해석 결과(개수) / import 대상·UX / cargo 수치 / 미결"

orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed   --text "[worker_done] winapp 이름해석 수정 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`

---

## 8. FIX — WAL 병합

<sub>원본: `work-003-winapp-p1/fix-wal/fix-wal-brief.md`</sub>

# [winapp] 긴급 수정 — import 가 WAL 미읽어 활발한 방 0행

너는 **mykakao `winapp` 워커**다. 같은 워크트리. 커밋 금지(코디).

## 증상 (코디 재현 확인)
- 사용자가 **열림·회수가능** 방("딴따라클럽 전체방", chatId 365103356371378)을 과거 가져오기 → **0행**.
- 그 방 파일: `chatLogs_365103356371378.edb` **main 127KB + -wal 482KB**. 데이터는 **대부분 WAL 에 있다.**
- 대조: WAL 작은 방(main 위주)은 정상 import 됨.

## 근본 원인 (코디 확인)
- `src/kakao/import.rs` 의 소스 복호가 `std::fs::read(src)` 로 **main .edb 만 읽는다.** `-wal` 을 안 읽어서, 활발한 방(최근 메시지가 WAL 에 상주, 아직 main 으로 checkpoint 안 됨)은 **0행**.
- 즉 초기 import 이 **WAL-resident 메시지를 누락**한다. (P2 watch 는 WAL 변경을 읽지만, 초기 import 경로는 main 만.)

## 고칠 것
1. **import 이 main + WAL 을 합쳐 현재 상태를 읽게 한다.** SQLCipher v4 는 WAL 프레임 페이지도 같은 방식으로 암호화돼 있다(프레임헤더 24B + 페이지). 접근 예:
   - main 을 평문 SQLite 로 복호 + **-wal 프레임들을 복호해 평문 SQLite -wal 로 재구성**해서 rusqlite(bundled 평문)로 열면 WAL 이 적용된다. 또는 복호한 WAL 페이지를 main 에 반영(apply)해서 읽는다.
   - **P2(watch.rs)의 WAL 프레임 복호 로직을 재사용**하라 — 이미 WAL 을 읽고 있으니 그 코드를 초기 import 에도 쓴다.
   - 원본 -wal 은 **읽기만**(사본). 원본에 쓰지 마라.
2. 검증: 방 365103356371378 을 **커서 0(신규 저장소)**에서 import → **행수 > 0** 이어야 한다(개수만, 본문 미출력).
3. **부가(같이 고쳐라)**: import 완료 후 **③ 채팅 내역이 자동 갱신** 안 된다(`ui/index.html` import 핸들러가 `loadRooms()` 만 하고 현재 방 메시지를 다시 안 읽음). import 끝나면 방금 가져온(또는 현재 선택된 curChat) 방의 메시지를 다시 로드해 ③ 에 바로 보이게 하라.

## 안전 (불변)
- 원본 DB/-wal **읽기만**, 복호 사본 RAII 삭제, 키 비상주, 카톡 무변조, SAC 미변경.
- 키·이름·본문 로그/커밋 비노출. 검증은 개수/유무만.
- 새 crate 금지(SAC). `win_app/` 밖 금지.

## 검증
```
cargo build --release(SAC 통과) + cargo test. 실기동: 저장소 초기화 후 365103356371378 import → 행수>0 확인(본문 미출력). ③ 자동갱신 육안(코디 최종). 검증 1회. SAC 로 test 바이너리 막히면 release+실기동으로 대체하고 보고.
```

## 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 아래 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "winapp WAL import 수정: <한 줄>" --body "원인/수정(main+WAL)/검증 행수/③자동갱신/미결"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] winapp WAL import 수정 완료 — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`

---

## 9. 스파이크 4 — 파생식 재도전

<sub>원본: `work-003-winapp-p1/spike4-derivation/spike4-brief.md`</sub>

# [winapp] spike 4 — SQLCipher 키 파생식 회수 (RE, 속도의 핵심)

너는 **mykakao `winapp` 워커**다. 같은 워크트리. **이건 탐색(spike) — PR 없음. 커밋 금지.**

> 목표: 카톡 SQLCipher 키를 **device/user 식별자에서 직접 계산하는 파생식(공식)** 을 회수한다. 되면 메모리 스캔이 사라져 키를 즉시 계산 → import 가 순식간이 된다. **억지 성공 금지** — 못 하면 "왜 못 하나 + 무엇이 필요한가"가 완전한 결과다.

## 1. 배경 — 왜 이게 속도의 핵심인가

현재 import 이 느린 건 데이터 읽기가 아니라 **키를 몰라서 카톡 메모리(357MB)를 매번 훑어 브루트포스로 찾기 때문**이다(harvest_candidates). 파생식이 있으면 스캔 없이 키를 계산한다.

**spike 3 결과([[baseline-004-offline-key-derivation]] · KEY_REPORT.md)**: raw key(32B) 회수·복호는 됨. 그러나 파생식은 **미회수** — ground-truth 8쌍으로 아래를 전수했으나 전부 불일치:
- `key == PBKDF2-{SHA512/256/1}(식별자, salt=file[:16], iter∈{256000,64000,4000})`
- `key == sha256/sha512/hmac(식별자 ⊕ salt 조합)`, 식별자 2원 조합 포함.
→ 공식이 단순 KDF/해시가 아니다. **바이너리 RE 가 남은 길.**

## 2. 우리의 무기 — 정답지(ground-truth)

너는 이미 **키를 회수하는 코드(memkey.rs)** 와 **복호 파라미터(KEY_REPORT.md)** 를 갖고 있다. 이걸로 검증셋을 만든다:
- 열린 방마다: memkey 로 **raw key(32B)** 회수 + 그 파일 **salt(page1[:16])** + (가능하면) 방 메타(chatId/멤버).
- device/user 식별자: 레지스트리 `HKCU\Software\Kakao\KakaoTalk\DeviceInfo`(sys_uuid/dev_id/hdd_serial), `MachineGuid`, 계정 폴더 해시(40hex), UserAccounts.
- → `(salt, 식별자들) → key` 쌍 여러 개. **어떤 가설이든 이 쌍 전부를 재현해야 정답.** falsification 즉시 가능.
- ⚠ 이 값들(키·salt·식별자)은 **메모리에서만**. 로그·리포트·커밋에 **원값 절대 금지**(마스킹/지문).

## 3. 접근 (우선순위 + SAC 유의)

KakaoTalk PID 2912 실행 중. 온디스크 exe 는 **패킹**돼 문자열 0개(spike 2) — **메모리엔 언패킹본이 있다.**

1. **키의 출처를 좁힌다**: harvest 가 키를 찾는 메모리 영역이 어느 **모듈/힙**인지 확인. 키는 카톡이 파생해 어딘가 저장한 것 — 그 근처에 **파생 입력(passphrase 문자열)이나 중간값**이 있을 수 있다. passive VM_READ 로 키 주변을 덤프해 salt/식별자/상수 흔적을 찾는다.
2. **언패킹 코드 덤프(passive, SAC 안전)**: KakaoTalk.exe·Vox*.dll 의 메모리상 코드 섹션을 VM_READ 로 덤프. 여기서 `sqlite3_key`/`PRAGMA key`/`sqlcipher`/PBKDF 상수를 찾는다(디스크선 0개였지만 언패킹본엔 있을 수 있음).
3. **정적 RE**: 덤프에서 sqlite3_key 호출부 → **passphrase 조립 루틴** 역추적. **Ghidra 등 무거운 도구 설치는 먼저 코디에 보고**하고 승인 후.
4. **동적(서명 도구)**: 필요하면 **WinDbg**(Microsoft 서명 → SAC 이 Frida 처럼 막지 않을 가능성)로 sqlite3_key BP → passphrase 원값 포착 후 그 값을 만든 코드 추적. **설치·사용 먼저 보고.** anti-debug 걸리면 보고(무리한 우회 금지).

## 4. 안전 (불변)

- 본인 기기·본인 앱·본인 데이터(레포 macOS extract.py 와 동일 성격). 그러나:
- **카톡 크래시·변조·종료 금지.** 메모리 **읽기만**(주입·쓰기 금지). SAC **미변경**. anti-tamper 우회 금지.
- **키·salt·user_id·device UUID·passphrase·대화 본문을 로그·리포트·커밋·진단출력에 절대 남기지 마라.** 마스킹/지문/카운트만.
- 무거운 도구(Ghidra/WinDbg) 설치 전 **보고**. 새 Rust crate 는 SAC 리스크 — 보고.

## 5. 산출물 / 범위

- `win_app/` 밖·문서 SoT 수정 금지. **커밋·PR 없음(spike).**
- 조사 스크립트·리포트는 워크트리 안(예 `win_app/research/`)에 두되 커밋은 코디 판단. 리포트에 값 원본 금지.
- 판정:
  - **(A) 파생식 회수** — 공식 + 파라미터 + ground-truth 전부 재현 실증 + (가능하면) Rust `derive()` 초안. → 스캔 제거 가능.
  - **(B) passphrase 원값은 포착(WinDbg 등) 했으나 공식 미완** — 무엇까지, 무엇이 남았나.
  - **(C) 막힘** — 패킹/anti-debug/도구/SAC 중 무엇이 막았고, 뚫으려면 뭐가 필요한가.

## 6. 검증

```
- 가설은 ground-truth 쌍 전부 재현해야 통과(개수만 보고, 값 미출력).
- cargo 를 쓰면 build 만(SAC 로 test 바이너리 팝업 가능 — 무시). 순수 함수는 테스트 가능.
- 못 한 것은 못 했다고. 억지 금지.
```

## 7. 완료 보고 — 문구 변경 금지

- 커밋 금지. 끝나면 아래 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "spike4 파생식: <판정 A/B/C 한 줄>" --body "판정/무엇을 했나/파생식 회수여부/ground-truth 재현/남은 벽/필요조건"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] spike4 파생식 <판정> — <한 줄>. 상세는 인박스." --enter
```
- 막히거나 도구 설치 필요하면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`

---

## 10. 스파이크 4b — WinDbg

<sub>원본: `work-003-winapp-p1/spike4-derivation/spike4b-windbg-brief.md`</sub>

# [winapp] spike 4b — WinDbg 로 passphrase/DPAPI 포착 → 파생식 완성

너는 **mykakao `winapp` 워커**다. 같은 워크트리. **탐색(spike) — PR·커밋 없음.**

> spike 4 후속. **사용자 승인 완료** — WinDbg 진행. 목표: 런타임에 SQLCipher passphrase 와 DPAPI 값을 포착해 파생식(`%s%s` 조립)의 미상 성분을 밝히고, **오프라인 키 계산**을 실증한다. 억지 금지 — 못 하면 "왜/필요조건"이 결과.

## 1. spike4 에서 이미 밝혀진 것

- 키 = SQLCipher raw-key(32B) + PBKDF2. **passphrase = `%s%s` 조립**(한 조각 미상) + **DPAPI(`CryptUnprotectData`) 사용**.
- 단순 식별자 KDF 는 전배터리로 배제됨. 미상 성분은 정적으론 안 잡힘 → 런타임 포착 필요.
- KakaoTalk 실행 중(PID 확인). ground-truth: memkey 로 raw key 회수 + salt(page1[:16]) 확보 가능.

## 2. 접근 — WinDbg/cdb (MS 서명, SAC 안전)

1. **설치**: WinDbg 또는 Debugging Tools(cdb.exe). MS 서명이라 SAC 통과. **cdb**(콘솔 디버거)가 스크립트 자동화에 유리. winget `Microsoft.WinDbg` 등. 설치 자체가 크거나 막히면 보고.
2. **CryptUnprotectData BP (쉬움, export)**: crypt32.dll 의 export 라 이름으로 BP. 호출 시 **입력 blob 과 출력(복호값)** 을 덤프 → DPAPI 보호 성분 정체 파악.
3. **sqlite3_key BP (정적링크, 주소로)**: export 없음 → spike4 에서 찾은 언패킹 모듈 내 함수 주소/시그니처로 BP. 호출 시 **passphrase 인자(포인터+길이)** 를 읽어 실제 문자열 포착.
4. **트리거**: 카톡이 방 DB 를 여는 순간 sqlite3_key 가 불린다. 앱 상호작용(방 열기)으로 트리거하되 **카톡을 크래시내지 마라**.
5. **조립식 복원**: 포착한 passphrase 를 두 조각(`%s%s`)으로 분해 — 어느 부분이 DPAPI 값이고 어느 부분이 상수/식별자인가. PBKDF2 파라미터(KEY_REPORT: compat4 등)로 그 passphrase 가 **ground-truth raw key 를 재현**하는지 검증(개수만).
6. **오프라인 재현 판단**: DPAPI 성분을 우리 코드로 `CryptUnprotectData` 호출해 재현 가능한가? blob 의 출처(어디 저장/어떻게 조립)를 추적. 재현되면 `derive()` 초안.

## 3. 안전 (불변 — 강하게)

- **카톡 크래시·변조·종료 금지.** WinDbg 는 관찰/BP 만 — 카톡 메모리·레지스터를 **쓰지 마라**(읽기만). 끝나면 **clean detach**(카톡 계속 살아있게).
- anti-debug 로 attach 막히거나 카톡이 불안정하면 **즉시 중단·보고**. 우회 강행 금지.
- SAC·OS 보안 미변경. 원본 DB/레지스트리 읽기만.
- **passphrase·DPAPI 값·키·salt·식별자·대화 본문을 로그·리포트·커밋·진단출력에 절대 남기지 마라** — 마스킹/지문/카운트만. WinDbg 로그 파일에도 원값 남기지 말 것(캡처 즉시 마스킹, 원본 로그 삭제).
- `win_app/` 밖·문서 SoT 수정 금지. 커밋·PR 없음.

## 4. 판정

- **(A) 파생식 완성** — passphrase 조립식 + 파라미터 + ground-truth 재현 + 오프라인 derive() 실증 → 스캔 제거 가능.
- **(B) passphrase/DPAPI 포착했으나 오프라인 재현 미완** — 무엇까지, 무엇이 남았나(예: blob 출처 미상).
- **(C) 막힘** — anti-debug/설치/SAC 중 무엇이, 필요조건은.

## 5. 검증

```
- 포착 passphrase → PBKDF2 → ground-truth raw key 재현(개수/일치여부만, 값 미출력).
- derive() 만들면 순수함수 cargo test(합성). cargo build 만(SAC test 팝업 무시).
- 못 한 건 못 했다고.
```

## 6. 완료 보고 — 문구 변경 금지

- 커밋 금지. 끝나면 아래 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "spike4b WinDbg: <판정 A/B/C 한 줄>" --body "설치/BP결과/passphrase·DPAPI 포착여부/조립식/오프라인 재현/남은 벽"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] spike4b WinDbg <판정> — <한 줄>. 상세는 인박스." --enter
```
- 설치·anti-debug·판단 필요하면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`

---

## 11. WORK-006 — 로그인 상태 추적

<sub>원본: `work-003-winapp-p1/work-006-login-state/work-006-brief.md`</sub>

# [winapp] WORK-006 — 로그인 상태 트래킹 + 자동 재조정 + 트레이 상태 메뉴

너는 **mykakao `winapp` 워커**다. P1~P3 를 네가 만들었다. 같은 워크트리 `work-003-winapp-p1`. 커밋·PR 은 코디.

## 1. SSOT (read-only 절대경로)
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/20-spec/spec-004-login-state-tracking.md` ← **계약 SoT.** 3상태·감지·재조정·세션캐싱·트레이메뉴·api. 여기 없는 건 발명 금지.
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/10-decision/decision-004-login-state-tracking.md` / `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/00-baseline/baseline-005-login-state-tracking.md`
- **P1~P3 코드**(이 워크트리): watch.rs(notify)·server.rs(AppState/harvest_candidates/recoverable_cache/state)·store.rs(room.selected/last_synced_id)·tray.rs·import.rs·memkey.rs·kakao/mod.rs.

## 2. 무엇을 만드나 (SPEC-004 요지)

**등록해둔 방을 접근 가능할 때마다 자동으로 최신화**하는 상태 엔진 + 트레이 상태 표시.

1. **3상태 감지** (`src/state.rs` 신규 또는 server 확장):
   - DOWN(프로세스 없음) / UP_LOGGED_OUT(프로세스O·계정DB 미열림) / UP_LOGGED_IN(계정DB 열림·키 회수 가능).
   - 신호: 계정 DB(chatListInfo/TalkUserDB) **열림·잠금** + 키 회수 가능(주), 메인윈도우(보조 교차검증).
   - ⚠ **OQ-1 실측**: 로그아웃 시 계정 DB 가 실제 close 되어 파일 이벤트/잠금해제가 일어나는지 확인. 안 되면 폴백 신호(잠금 시도·키회수) 사용하고 보고.
2. **이벤트 감지** (무거운 건 트리거로만):
   - 로그인/로그아웃·방열림·새메시지 → **notify 파일감시를 계정 폴더까지 확장**(P2 watch.rs 재사용).
   - 카톡 종료(DOWN) → 프로세스 핸들 `WaitForSingleObject`(즉시).
   - 카톡 시작(UP) → 가벼운 프로세스 존재 체크(수 초) 또는 WMI. **harvest 는 로그인/방열림 이벤트에서만.** 폴링 금지.
3. **재조정 루프**:
   - 앱 시작 → `room.selected` 로드 → UP_LOGGED_IN 이면 OPEN 추적 방 **델타 import**(logId>last_synced_id) + 감시 시작.
   - 로그인 이벤트 → 추적 방 OPEN 델타 import + 감시 재개.
   - 방열림 이벤트 → 그 방(추적 대상) 델타 import.
   - 로그아웃/DOWN → 감시 일시정지·상태 갱신(다음 로그인 때 델타로 메꿈).
4. **세션 키 캐싱**: harvest 결과(후보/회수 키)를 **세션 메모리 캐싱**해 재조정 반복 harvest 회피. **키는 RAM only(디스크 금지)**. 카톡 재시작·로그아웃 시 캐시 무효화.
5. **트레이 상태 메뉴** (tray.rs, 우클릭마다 재생성):
   ```
   로그인 상태               (MF_GRAYED 헤더)
     로그인 유저 : <본인 닉네임>  (MF_GRAYED, 로그아웃이면 "-")
     상태 : 🟢 로그인 / ⚪ 로그아웃  (MF_GRAYED)
   ───  환경설정 (클릭→웹)  ───  종료
   ```
   - dot **이모지 우선**, 렌더 불량이면 오너드로우(WM_DRAWITEM). **본인 닉네임**: UserAccounts 로 본인 userId 특정 → TalkUserDB 닉네임(못 구하면 "-").
6. **/api/state 확장**: 기존 + `state`("DOWN"|"UP_LOGGED_OUT"|"UP_LOGGED_IN") + `me`(본인 닉네임). 웹 ①섹션이 반영.

## 3. 안전 (불변)
- 카톡 크래시·변조·종료 금지. 메모리 읽기만. SAC 미변경. 원본 DB/레지스트리 읽기만.
- **키·본인닉네임·상대닉네임·본문·계정식별자를 로그·리포트·커밋·진단출력에 남기지 마라**(마스킹/카운트). 세션 캐시 키는 RAM only, 디스크·로그 금지.
- 새 crate 금지(SAC). 부득이하면 보고. `win_app/` 밖·문서 SoT 수정 금지.

## 4. 검증
```
cd win_app && cargo build --release(SAC 통과, 차단0) + cargo test<네 테스트>. cargo=~/.cargo/bin. (SAC 로 test 바이너리 팝업 가능 — 무시하고 release+실기동으로 대체 가능, 보고).
- 실기동(개수/유무만, 값 미출력): 앱 시작 시 추적 방 자동 델타 import(수동버튼 없이 행수↑) / 카톡 로그아웃→로그인 후 자동 따라잡기 / 트레이 우클릭에 본인 닉네임+상태 dot(육안) / 재조정 반복 시 세션캐시로 harvest 재실행 안 함.
- OQ-1(로그아웃 신호) 실측 결과 보고. 못 한 건 못 했다고.
```

## 5. 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 아래 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "WORK-006 로그인 상태 트래킹 완료: <한 줄>" --body "3상태감지/재조정/세션캐싱/트레이메뉴/본인닉네임/OQ-1 실측/cargo 수치/미결"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] WORK-006 완료 — <한 줄>. 상세는 인박스." --enter
```
- 막히거나 OQ 판단 필요하면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`

---

## 12. WORK-007 — 설정 화면 리디자인

<sub>원본: `work-003-winapp-p1/work-007-settings-redesign/work-007-brief.md`</sub>

# [winapp] WORK-007 — 설정 UI 리디자인 + 수집 큐 + 트레이 오너드로우

너는 **mykakao `winapp` 워커**다. P1~P3+WORK-006 을 네가 만들었다. 같은 워크트리 `work-003-winapp-p1`. 커밋·PR 코디.

## 1. SSOT (read-only 절대경로)
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/20-spec/spec-005-settings-collection-queue.md` ← **계약 SoT.**
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/10-decision/decision-005-settings-collection-queue.md` / `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/00-baseline/baseline-006-settings-redesign-collection-queue.md`
- **승인 목업**: 이 워크트리 `win_app/ui/mockup-reference.html` (내가 복사해 둠). **디자인·레이아웃·아이콘(SVG)의 기준.** 그대로 win_app/ui 에 반영. (작업 후 mockup-reference.html 은 지워도 됨 — 커밋 대상 아님)
- 기존 코드: ui/index.html · server.rs(/api/rooms, /api/state, AppState, 세션캐시) · store.rs(room.selected/last_synced) · state.rs(상태 트래커·이벤트) · watch.rs · tray.rs · import.rs.

## 2. 무엇을 만드나 (SPEC-005)

### (A) 설정 UI 리디자인 → ui/index.html
- **승인 목업대로**: 전체폭, 카톡 스타일(옐로우·말풍선·SVG 아이콘, **이모지 금지**), 2탭.
- 탭1 **채팅방 설정 = transfer**: 좌"내 카톡 대화방"(클릭→우측 추가) / 우"추적 중인 방"(× 해제 + 상태 뱃지 수집중/대기중/완료). 하단 `[취소][저장]`, **저장은 우측 dirty 시 활성**, 취소=되돌림. 대기 안내 문구.
- 탭2 **채팅방+채팅목록 = 2-pane**: 좌 추적 방(상태 미니표시) / 우 대화. 수집중=스피너("수집 중입니다"), 대기중=안내, 완료=말풍선. (기존 SSE 실시간 append 유지.)
- 목업의 CSS/구조를 실제 API 에 배선. 값(대화·이름)은 실데이터.

### (B) 백그라운드 수집 큐
- 저장(POST /api/rooms/select) → 추적 집합 저장 + **새로 추적된 방마다 큐 행 생성**.
- 백그라운드 처리: 열린 방 → `collecting` → import(main+WAL 델타, 기존 import_room) → `done`(행수). 닫힌 방 → `waiting` → **state.rs 트래커의 방 열림 이벤트 시 `collecting`**(재조정 루프에 큐 연결). 실패 → `error`.
- 큐 **DB 영속**(재시작 재개). 세션 키 캐시(WORK-006) 활용해 반복 harvest 회피.
- `GET /api/rooms` 확장: 각 방 `tracked` + `collect_status`(idle|collecting|waiting|done|error) + `collected_rows`. UI 가 폴링해 상태 뱃지 갱신.

### (C) 트레이 오너드로우 (tray.rs) — 사용자 피드백
현재 MF_GRAYED(회색·이모지 점). 요구:
- **MF_OWNERDRAW** 로 정보 3항목(로그인 상태 / 로그인 유저 : <닉> / 상태) 직접 그림 — **까만(메뉴 기본) 글씨**, 클릭 비활성(하이라이트·커맨드 없음).
- 상태 점 = **초록 #17B26A(로그인) / 빨강 #E5484D(로그아웃)** 원. **이모지 금지.**
- WM_MEASUREITEM/WM_DRAWITEM 구현. 환경설정·종료는 일반(클릭) 항목 유지.
- 다크 테마/하이DPI 에서도 글씨 보이게(시스템 메뉴색 사용 권장).

### (D) 본인 닉네임 조사
- Profile.nickname 비어있음. 대안 조사: 본인 userId 특정(UserAccounts/로그인데이터/내 메시지 authorId) → TalkUserDB nickName. 못 구하면 이메일 또는 "(이름 없음)". `/api/state.me` + 트레이에 반영.

## 3. 안전 (불변)
- 카톡 무변조·메모리 읽기만·SAC 미변경·원본 읽기전용·복호 임시본 RAII.
- **키·본인닉·상대닉·본문·계정식별자 로그·리포트·커밋 비노출**(마스킹/카운트). 세션캐시 키 RAM only.
- **새 crate 금지(SAC).** 부득이하면 보고. `win_app/` 밖·문서 SoT 수정 금지. mockup-reference.html 은 커밋하지 마라.

## 4. 검증
```
cd win_app && cargo build --release(SAC 통과·새 crate 0) + cargo test. (SAC test 팝업 무시 가능, 보고).
실기동(개수/유무만, 값 미출력): transfer 좌→우 추가·dirty 저장·취소 / 저장→큐→열린방 수집 done(행수↑)·닫힌방 waiting 유지 / /api/rooms collect_status 전이 / 트레이 까만글씨+초록빨강 점+본인닉(있으면)·정보항목 클릭안됨(육안).
검증 1회. 못 한 건 못 했다고.
```

## 5. 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "WORK-007 설정 리디자인+큐+트레이 완료: <한 줄>" --body "UI 반영/수집 큐 상태/트레이 오너드로우/본인닉네임/cargo 수치/미결"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] WORK-007 완료 — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`

---

## 13. FIX — 실시간 전송

<sub>원본: `work-003-winapp-p1/work-007-settings-redesign/fix-realtime-brief.md`</sub>

# [winapp] 긴급 — 실시간 수집 안정화 (상태 진동 + WAL 파일감시 누락)

너는 **mykakao `winapp` 워커**다. 같은 워크트리. 커밋 금지(코디). **제품 핵심(실시간 축적)이 안 돈다 — 최우선.**

## 증상 (사용자 실기동 + 코디가 win_app.log 로 확진)
- 추적한 개인방(열림)에서 카톡으로 새 메시지 보내도 **앱에 안 쌓인다**(1행에서 안 늘어남). 실시간 미작동.
- "수집 중"이 **계속 반복**해서 뜬다.
- 로그 실측: 상태가 `UP_LOGGED_IN → DOWN → UP_LOGGED_OUT → UP_LOGGED_IN` **반복**, "방 열림 감지: 수집 트리거" **6회**, 수집이 전부 상태-루프 open-edge 에서만 발생(파일감시 이벤트로 인한 델타 없음).

## 근본원인 (코디 진단)
**버그A — 상태/열림 진동 → 반복 수집**
- `state::detect()` 가 `is_running()`(find_pid) 단발 실패 시 즉시 LIFE_DOWN 판정 → `apply` 가 세션 무효화 → 다시 IN → `on_login` 재조정 → 재수집. find_pid 이 순간 실패하면 상태가 튄다.
- `open_tracked`/`open_rooms` 잠금프로브도 진동하면 open-edge 가 반복 발화 → `process_delta` 반복 → `set_collect("collecting")` 반복 → "수집 중" 계속.

**버그B — 실시간 파일감시가 WAL 쓰기를 놓침**
- notify(ReadDirectoryChangesW) 가 KakaoTalk 의 SQLite `-wal` **in-place 쓰기**를 안정적으로 이벤트로 못 낸다(메모리맵/flush 타이밍). 그래서 새 메시지가 파일감시로 안 잡힘. 현재 수집은 3s 상태-open-edge 우연에만 의존.

## 고칠 것
**A. 상태 안정화(진동 제거)**
- `detect()`/전이에 **히스테리시스**: DOWN/OUT 판정은 **연속 N회(예 2~3) 확인 후에만** 확정. 단발 miss 는 무시(이전 상태 유지). 카톡 실행 중 상태가 튀지 않게.
- `process_delta` **멱등화**: done 방을 **새 델타가 실제로 있을 때만** 재수집. 델타 0 이면 `collecting` 찍지 말고 **done 유지**(status flicker 금지). 즉 import 전에 델타 유무(logId>cursor)를 싸게 확인하거나, import 결과 신규 0 이면 상태 안 건드림.
- open-edge 는 **새 델타가 있을 때만** 의미. 열림집합 진동으로 재발화해도 델타 0 이면 조용히 무시.

**B. 실시간을 폴링으로 견고화(핵심)**
- notify 이벤트에만 의존하지 말고, **추적+열린 방에 대해 기본 켜진 짧은 주기 폴링(예 2~3초)** 으로 델타를 확인해 append+SSE. (세션 키캐시로 재복호 저렴 — 전체 harvest 아님.)
- 지금 있는 `WIN_APP_RESYNC_SECS`/`resync_loop` 를 **기본 ON(예 3s)** 으로 켜거나, 그에 준하는 tracked-room 폴링을 상시 돌려라. 새 델타 있으면 append+SSE push, 없으면 done 유지(상태 안 건드림).
- notify 는 보조로 유지(즉시성). 폴링이 놓침 보정.

## 검증 (라이브 — 사용자 협조 가능)
- 열린 추적 방에 카톡으로 **새 메시지 1개** 보냄 → **수초 내** 앱 대화에 append + 좌측 행수 +1 (SSE 로 화면 갱신). 여러 번 보내도 매번 잡힘.
- 상태가 안 튀고("UP_LOGGED_IN" 유지), "수집 중"이 반복 안 뜸(done 유지). 로그로 확인.
- cargo build --release SAC 통과 + cargo test. 값·본문 미출력.

## 안전 (불변)
- 원본 읽기만·카톡 무변조·SAC 미변경·키 RAM only·키/본문/닉 로그·커밋 비노출. 새 crate 금지. `win_app/` 밖 금지.

## 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "실시간 수집 안정화 완료: <한 줄>" --body "상태 히스테리시스/process_delta 멱등/폴링 실시간/검증(새 메시지 append 수초내)/cargo 수치"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] 실시간 수집 안정화 완료 — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`

---

## 14. FIX — 로그인 유저 표시

<sub>원본: `work-003-winapp-p1/work-007-settings-redesign/fix-user-id-brief.md`</sub>

# [winapp] 빠른 수정 — 본인 유저 식별자 표시 (닉네임 없으면 계정 이메일)

너는 **mykakao `winapp` 워커**다. 같은 워크트리 `work-003-winapp-p1`. 커밋 금지(코디).

## 배경
사용자 지적: "닉네임 말고 **유저가 누구인지 식별은 되잖아**, 그걸 넣어라." 맞다 — Profile.nickname 이 비어 me=null 이지만, **UserAccounts 레지스트리에 로그인 계정(이메일)이 있다.** 지금은 "-"/"(이름 없음)" 만 떠서 누군지 안 보인다.

## 고칠 것
- 본인 식별자 해석 우선순위: **① TalkUserDB 닉네임(있으면) → ② 계정 이메일 → ③ "(이름 없음)"**.
- **계정 이메일 소스**: `HKCU\Software\Kakao\KakaoTalk\UserAccounts\<이메일>` — 서브키 이름이 로그인 이메일이다. (또는 로그인 계정 폴더와 연결된 UserAccounts 항목.) 이 이메일을 읽어 반환.
- `/api/state.me` 와 **트레이 "로그인 유저 :"** 에 이 식별자를 표시. state.rs 의 my_profile/me 해석부에 fallback 추가.
- 로그아웃 시엔 "-" (해당 없음).

## 안전 (불변)
- 이메일은 **본인 기기·본인 화면 표시용** — 로그·리포트·커밋에는 남기지 마라(값 마스킹/비노출). UI/트레이 표시에만.
- 레지스트리 **읽기만**. 카톡 무변조. SAC 미변경. 새 crate 금지. `win_app/` 밖 금지.

## 검증
```
cargo build --release(SAC 통과) + cargo test. 실기동: /api/state.me 가 null 대신 계정 이메일/식별자 반환하는지(값은 마스킹 로그 말고, 존재/형태만 확인). 트레이 "로그인 유저"에 뜨는지 육안(사용자). 검증 1회.
```

## 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "유저 식별자 fallback 완료: <한 줄>" --body "소스/우선순위/me 반환 형태/트레이 반영/cargo 수치"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] 유저 식별자 fallback 완료 — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`

---

## 15. WORK-008 — 사진 수집

<sub>원본: `work-003-winapp-p1/work-008-photo/work-008-brief.md`</sub>

# [winapp] WORK-008 — 사진 수집 (URL 다운로드·로컬 저장·미디어 서빙·<img>)

너는 **mykakao `winapp` 워커**다. 같은 워크트리. 커밋·PR 코디.

## 1. SSOT (read-only 절대경로)
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/20-spec/spec-006-photo-collection.md` ← **계약 SoT.**
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/10-decision/decision-006-photo-collection.md` / `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/00-baseline/baseline-007-photo-collection.md`
- 기존 코드: import.rs(델타 수집)·watch.rs(폴링)·server.rs(API/AppState/키캐시)·store.rs·ui/index.html(탭2 렌더).
- 직전 사진 spike 결과(네가 함): talkmedia.edb(chatMsgTokenJunction logId→token, tokenInfo token→url,fileSize,checkSum[SHA1]) memory harvest 키로 복호됨. 채팅사진 URL=talk.kakaocdn.net, **최근=200/오래됨=410**. .cng 복호는 범위 밖(BASE-008 백로그).

## 2. 구현 (SPEC-006)
1. **사진 수집 파이프**: 델타 수집(import_room/폴링)에서 **사진 타입 메시지** 식별(type 코드 — 실데이터로 확인). 그 logId → talkmedia.edb 조회(token→url,fileSize,checkSum). talkmedia 복호는 기존 harvest 키 재사용.
2. **다운로드·저장**: URL GET → 200 이면 바이트 확보 → **checkSum(SHA1)·fileSize 검증** → 로컬 미디어 스토어 저장(예 `%LOCALAPPDATA%\mykakao\media\<chatId>\<logId>.<ext>` 또는 DB blob, 택1). 상태=`saved`. **410/404=`lost`(유실, 재시도 안 함)**. 실패=`pending`(다음 델타에 재시도 가능).
3. **미디어 상태 DB**: `media(chat_id,log_id,mime,status,path/blob)` 또는 message 확장. 우리 SQLite.
4. **서빙**: `GET /api/media/<chatId>/<logId>` → 저장 이미지 바이트(Content-Type mime), 없으면 404.
5. **메시지 표식**: `/api/messages` 사진 메시지에 `kind:"photo"` + `media_status`(saved|lost|pending).
6. **탭2 렌더**(ui/index.html): 사진 메시지 → saved면 `<img src="/api/media/<chatId>/<logId>" loading="lazy" style="max-width">`, pending=로딩, lost="유실됨" placeholder+아이콘. "사진" 텍스트 대체.

## 3. 안전 (불변)
- **URL·토큰·checkSum 원값·이미지 내용을 로그·리포트·커밋에 남기지 마라** — host·status·크기·일치여부·개수만. 이미지는 **로컬 저장·외부 전송 0**(다운로드는 카카오 CDN 에서 GET 만).
- 원본 DB 읽기만·카톡 무변조·SAC 미변경·키 RAM only·복호 임시본 RAII. 미디어 스토어는 우리 것.
- HTTP 다운로드에 새 crate 가 필요하면(reqwest 등) **먼저 보고**(SAC — proc-macro/build-script 리스크; 가능하면 기존/std 로). `win_app/` 밖·문서 SoT 수정 금지.

## 4. 검증 (개수/유무만, 이미지·URL 원값 미출력)
```
cargo build --release(SAC 통과·새 crate 보고) + cargo test. 실기동: 최근 사진 있는 방 수집 → talkmedia URL 200 다운로드 → 로컬 저장 → checkSum 일치 → /api/media 200 image 확인. 탭2 <img> 표시(육안). 만료 사진 → lost "유실됨". 값 미출력. 검증 1회.
```

## 5. 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "WORK-008 사진 수집 완료: <한 줄>" --body "수집 파이프/다운로드·checkSum/미디어 스토어//api/media/탭2 img·유실/새 crate 여부/cargo 수치"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] WORK-008 사진 수집 완료 — <한 줄>. 상세는 인박스." --enter
```
- 막히거나 crate 필요하면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`

---

## 16. FIX — 사진/실시간 (콘솔창 제거)

<sub>원본: `work-003-winapp-p1/work-008-photo/fix-photo-realtime-brief.md`</sub>

# [winapp] 긴급 — 사진 다운로드가 실시간 SSE 막음 + 터미널 창 스폰

너는 **mykakao `winapp` 워커**다. 같은 워크트리. 커밋 금지(코디).

## 증상 (사용자 실기동)
1. **실시간 전송 안 됨** — 새 메시지/사진이 화면에 바로 안 붙고 새로고침해야 렌더됨.
2. **사진 받을 때마다 터미널(콘솔) 창이 뜸.**

## 근본원인 (코디 진단)
- `src/kakao/photo.rs` `curl_download` 가 `Command::new("curl").output()` — **CREATE_NO_WINDOW 없음** → GUI 앱(콘솔숨김)이 curl 을 띄우면 매번 콘솔 창. (증상2)
- `src/watch.rs` process_delta 가 **collect_room_photos(동기 curl 다운로드)를 SSE tx.send 전에** 호출 → 사진 다운로드가 블로킹/지연되면 그 방의 SSE push 가 늦어짐 → 실시간 안 뜨고 새로고침해야 보임. (증상1)

## 고칠 것
**A. 콘솔 창 제거 + 외부 curl 의존 제거**
- **권장**: curl.exe 대신 **WinHTTP(windows crate — 이미 dep)로 in-process 다운로드**. 창 안 뜨고 curl.exe 존재 의존도 없앤다. (SAC 꺼졌으니 crate/빌드 자유롭지만, WinHTTP 는 crate 추가 없이 windows crate 로 됨.)
- WinHTTP 가 부담이면 최소한 curl Command 에 **CREATE_NO_WINDOW(0x08000000)** `.creation_flags` 적용(std::os::windows::process::CommandExt).

**B. 사진 다운로드가 실시간 SSE 를 막지 않게**
- process_delta 는 **새 메시지 SSE 를 먼저 push**(텍스트·사진 메시지 행 즉시 렌더). 사진 **바이트 다운로드는 그 뒤/백그라운드**로(SSE 를 블로킹하지 마라).
- 사진 행은 SSE 로 보낼 때 media_status(pending/saved) 표식. **다운로드 완료(saved) 시 이미지가 화면에 나타나게**:
  - 방법1: 다운로드 완료 후 그 log_id 에 대해 **SSE 재전송(media 업데이트 이벤트/행)** → UI 가 해당 <img> 갱신.
  - 방법2: UI <img onerror> 로 짧은 재시도(백그라운드 저장 완료되면 /api/media 200) — 간단하지만 방법1 이 확실.
  - 택1 구현(방법1 권장).

## 검증 (라이브 — 사용자 협조 가능)
- 열린 추적 방에 카톡으로 **텍스트 메시지** → **수초 내 화면 append**(새로고침 없이). **사진** → 메시지 즉시 뜨고, 다운로드 완료되면 이미지 나타남. **콘솔 창 안 뜸.**
- cargo build --release + cargo test. 값·URL·토큰 미출력.

## 안전 (불변)
- URL/토큰/이미지 로그·커밋 비노출. 원본 읽기만·카톡 무변조·키 RAM only. `win_app/` 밖·문서 SoT 수정 금지.

## 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "사진 실시간/콘솔창 수정: <한 줄>" --body "다운로드 방식(WinHTTP/no-window)/SSE 선push/사진 saved 반영/cargo 수치"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] 사진 실시간/콘솔창 수정 완료 — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`

---

## 17. FIX — 클릭 수집 스피너

<sub>원본: `work-003-winapp-p1/work-008-photo/fix-click-collect-brief.md`</sub>

# [winapp] 수정 — 대화방 클릭 시 그 방 즉시 수집 시도(스피너)

너는 **mykakao `winapp` 워커**다. 같은 워크트리. 커밋 금지(코디).

## 증상 (사용자 실기동)
- 탭2 "채팅방+채팅목록"에서 방(예: 이건학·조상아)이 **카톡에선 열려 있는데** 앱은 "대기 중·닫힘"으로 표시. 그 방을 클릭해도 **수집을 시도하지 않고** "대기 중" 상태 화면만 보여줌.
- 사용자 기대: **대화방 클릭 = 스피너 돌면서 그 방 즉시 수집.** 열려있으면 수집→대화 렌더, 진짜 닫혔으면 그때 "대기 중".

## 원인
- 백그라운드 재조정(3s open-edge)이 이 방들의 열림을 못 잡음(세션 키캐시에 그 방 키 없음 → "닫힘"으로 봄).
- 탭2 방 클릭(openChat/openRoom) 은 **저장된 상태만 렌더**하고 능동 수집 트리거가 없음.

## 고칠 것
1. **능동 수집 엔드포인트**: `POST /api/collect` body `{chat_id}` → 그 방에 대해 **키 회수(캐시 miss 면 1회 재harvest 허용) + 델타 import**를 즉시 실행 → 결과 상태 반환(`{status:"done|waiting|error", rows}`). 열린 방이면 collecting→done, 못 회수하면 waiting. (process_delta/import 로직 재사용.)
2. **탭2 방 클릭 시**: 그 방이 이미 `done` 이 아니면(또는 항상) → 대화영역에 **"수집 중" 스피너** 표시 → `/api/collect` 호출 → 완료되면 메시지 로드+SSE 구독. `waiting`(닫힘) 이면 기존 "대기 중" 안내. 이미 done 이면 바로 렌더.
3. 스피너/상태 전이가 깔끔하게(중복 호출·플리커 방지). 클릭 연타 안전.

## 검증 (라이브 — 사용자 협조)
- 카톡에서 방 열어둔 상태로 앱 탭2에서 그 방 클릭 → **스피너 → 수집 → 대화 렌더**. 
- 진짜 닫힌 방 클릭 → "대기 중" 안내(무한 스피너 아님).
- cargo build --release + cargo test. 값·URL·토큰 미출력.

## 안전 (불변)
- 원본 읽기만·카톡 무변조·SAC 관계없음(꺼짐)·키 RAM only·키/본문/URL 로그·커밋 비노출. `win_app/` 밖·문서 SoT 수정 금지.

## 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "클릭 수집 완료: <한 줄>" --body "/api/collect/클릭 스피너·수집/닫힘 처리/cargo 수치"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] 클릭 수집 완료 — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`

---

## 18. 스파이크 — 사진 URL/토큰

<sub>원본: `work-003-winapp-p1/photo-spike-brief.md`</sub>

# [winapp] spike — 사진(이미지) 획득 경로 규명 (attachment / .cng / URL)

너는 **mykakao `winapp` 워커**다. 같은 워크트리. **탐색(spike) — PR·커밋 없음.** 조사만.

## 배경
현재 사진 메시지가 화면에 "사진" 텍스트로만 뜬다(우린 message 텍스트 컬럼만 읽음). 실제 이미지를 표시하려면 attachment/캐시를 알아야 한다. 카톡 실행 중(키 회수 가능).

## 조사할 것 (값은 마스킹 — 원본 URL/토큰/이미지 비노출, 구조·필드명·존재여부만)

1. **사진 메시지의 전체 컬럼**: `chatLogs_<chatId>.edb` 복호(기존 decrypt 경로) 후, **type 이 사진인 행**의 모든 컬럼을 본다 — 특히 `attachment`(JSON), `v`, `referer`, `supplement` 등. 사진 메시지의 attachment JSON 에 **뭐가 들었나**: 이미지 URL(호스트/스킴만)·썸네일 URL·width/height·캐시키·파일명. (김태우 방에 사진 메시지 3개 있음 — 그 방 chatId 로.)
2. **로컬 캐시 매핑**: `chat_data\url_image_v2.edb`·`talkmedia.edb`(SQLCipher) 를 복호해 스키마 확인 — attachment/URL → 로컬 `.cng` 파일 매핑이 어떻게 되나(테이블·컬럼명만).
3. **.cng 포맷**: `chat_data\url_image_v2\*.cng` 파일 매직바이트·크기·엔트로피로 암호화 방식 추정. SQLCipher 계열인가, 별도 스킴인가(복호 가능성 판단만, 실제 복호는 하지 마라).
4. **URL 접근성**: attachment 에 이미지 URL 이 있으면, 그게 **직접 열리는지**(HEAD 요청 status 코드만 확인 — 이미지 저장 금지, 토큰/URL 원문 로그 금지) 또는 만료/인증 필요한지. curl 로 status 만.

## 판정
- **(A) URL 경로** — attachment URL 이 직접 접근 가능 → 쉬움. 어떤 필드에 어떻게.
- **(B) 로컬 .cng 복호** — URL 이 안 되거나(만료/인증) 오프라인이 나음 → .cng 복호 필요. 방식·난이도.
- **(C) 하이브리드** — 썸네일은 캐시/URL, 원본은 다른 경로 등.
→ 각 경로의 **구현 난이도 + 다음 스텝**을 근거와 함께.

## 안전 (불변)
- 카톡 무변조·원본 읽기만·SAC 미변경·키 RAM only. 복호 사본 RAII.
- **이미지 원본·URL 원문(토큰 포함)·본문·키를 로그·리포트·커밋·출력에 남기지 마라.** 구조/필드명/status/개수/지문만. 실제 이미지 파일 저장·커밋 금지.
- 새 crate 함부로 추가 금지(HEAD 요청은 std/기존으로, 부득이하면 보고). `win_app/` 밖·문서 SoT 수정 금지.

## 검증
탐색이라 통상 검증 없음. 조사 스크립트는 재현 명령을 리포트에 적고, 값은 마스킹. cargo 쓰면 build 만.

## 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "사진 획득경로 spike: <판정 A/B/C 한 줄>" --body "attachment 구조/캐시 매핑/.cng 포맷/URL 접근성/판정+난이도+다음스텝"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] 사진 spike <판정> — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`

---

## 19. 스파이크 — .cng 로컬 캐시 (백로그)

<sub>원본: `work-003-winapp-p1/cng-spike-brief.md`</sub>

# [winapp] spike — 채팅사진 .cng 복호 가능성 실증 (핵심 리스크 선검증)

너는 **mykakao `winapp` 워커**다. 같은 워크트리. **탐색(spike) — PR·커밋 없음.** 사용자 승인 완료.

## 목표
채팅방 사진 `.cng` 가 실제 이미지(JPEG/PNG/WEBP)로 **복호 가능한지 판정**. 가능하면 방식·난이도, 불가면 대안. 억지 금지 — 못 되면 근거+필요조건이 결과.

## 근거 (직전 사진 spike)
- 채팅사진 원본 URL(talk.kakaocdn.net)=GET 410 Gone(만료) → URL 불가, **로컬 .cng 가 유일 소스**.
- .cng: 매직 없음·엔트로피~8=암호화. 앞16B=IV 추정.
- 매핑 확보(둘 다 memory harvest 키로 복호): `talkmedia.edb` tokenInfo(token→filePath,fileSize,checkSum[SHA1]) + chatMsgTokenJunction(logId→token). (url_image_v2 는 URL 200 이라 별개·쉬움.)

## 조사 스텝
1. 알려진 채팅사진 1개: logId→token→tokenInfo.filePath 로 대응 .cng 특정(mci_v2 등).
2. **AES-128/256-CBC(앞16B IV)** 시도. 키 후보 순서: (a) 이미 harvest 한 메모리 후보(계정/캐시키 우선), (b) checkSum/token 파생, (c) 안되면 KakaoTalk 미디어 복호 루틴 정적 RE(passive 덤프).
3. **성공 판정 = 복호 선두 FFD8(JPEG)/8950(PNG)/RIFF(WEBP) + SHA1==checkSum.** (정답지 = 매직 + SHA1.)
4. 되면 이미지 1장을 **다운로드 폴더 저장까지 PoC**(파일 저장 위치만 보고, 이미지 내용 비노출).

## 판정
- (A) 복호 성공 — 방식(키 출처·AES 모드·IV)·난이도·다음스텝(구현).
- (B) 부분 — 어디까지, 뭐가 막나.
- (C) 막힘 — 왜(키 못 찾음/RE 필요), 필요조건.

## 안전 (불변)
- 원본 읽기만·카톡 무변조·SAC 미변경·키 RAM only·복호 임시본 RAII.
- **이미지·URL·토큰·키·checkSum 원값을 로그·리포트·커밋·출력에 남기지 마라** — 매직바이트·SHA1 일치 여부·개수·지문만.
- 새 crate 금지(부득이하면 보고). 조사 test 는 사후 삭제(프로덕션/커밋 변경 0). **anti-debug 주의**(지속 디버거 attach 시 카톡 크래시 이력 — passive 우선, WinDbg 류 지속 BP 금지).
- `win_app/` 밖·문서 SoT 수정 금지.

## 검증
탐색이라 통상 검증 없음. 재현 명령은 리포트에, 값은 마스킹. cargo 쓰면 build 만.

## 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject ".cng 복호 spike: <판정 A/B/C 한 줄>" --body "특정/키출처/AES모드·IV/매직+SHA1 성공여부/난이도/다음스텝"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] .cng 복호 spike <판정> — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`

---
