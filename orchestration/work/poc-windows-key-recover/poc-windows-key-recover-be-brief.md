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
