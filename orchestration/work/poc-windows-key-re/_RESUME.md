# poc-windows-key-re — 재개 노트

## 발주 (2026-09-02)
- 성격: **spike 2** (RE) — poc-windows-key-derivation 후속. PR 없음.
- 결정 근거: spike 1 판정 C+D → 사용자 선택 "KakaoTalk.exe 키파생 RE".
- 접근: 동적 훅 우선(Frida) — 라이브 KakaoTalk.exe 의 sqlite3_key/prepare 후킹 → 키 + 스키마 동시 포착. 정적(Ghidra/strings) 폴백.
- Run: run_562b2ec38263 (spike1 과 공유)
- Task: task_277a7d67c021  · Dispatch: ctx_d6315927dd15
- 워커handle: term_0f75ed4f-440d-43ef-a670-523b7b65aef7 (spike1 과 같은 워커 — context 보존)
- 워크트리: C:/Users/sc971/orca/workspaces/mykakao/poc-windows-key-derivation (spike1 과 공유)
- 코디handle: term_eda12742-b6d9-434d-8eb8-f534be92dcc3
- 판정 목표: (A)키+파생식 (B)키O·대화X→로컬무의미 (C)막힘+필요조건
- 완료 캐치: 2채널. 폴링 금지.

## §종료 (2026-09-02) — spike 2 done
- 판정 (C): SQLCipher 키/파생식 회수 실패 (동적=SAC 차단 확증 3077/3033, 정적=패킹, SQLCipher 정적링크라 passive 훅 불가).
- **중대 정정: spike1 (D) 오답.** 대화 로컬 존재 확증 — ActionLogDB.edb 가 이름과 달리 메인 SQLCipher DB. passive VM_READ 로 복호 sqlite_master 64테이블 관측(chatLogs/chatRooms/talkUser…). macOS NTChat* 와 스키마 다름.
- 남은 단일 벽: **키뿐.** 데이터·경로·스키마 전부 확인됨.
- 산출물(비커밋): mem_probe.py(SAC-safe 핵심)·test_mem_probe(5)·RE_REPORT.md / hook_kakao.js·re_probe.py(SAC로 死코드, 보존)
- 검증(코디): 13 passed / 실값유출0 / 원본DB 미수정 / 카톡 생존
- 다음 후보(무거움, 별도 발주): (a)SAC허용 서명계측으로 sqlite3_key 훅 (b)KakaoTalk.exe 언패킹 후 Ghidra
- Task completed / released. PR 없음.
