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
