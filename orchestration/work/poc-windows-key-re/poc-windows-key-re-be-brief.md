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
