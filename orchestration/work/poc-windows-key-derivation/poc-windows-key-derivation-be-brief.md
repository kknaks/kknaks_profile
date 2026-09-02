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
