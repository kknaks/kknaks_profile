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
