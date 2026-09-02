# poc-windows-key-recover — 재개 노트 (spike 3, B경로)

## 발주 (2026-09-02)
- 성격: spike 3 — SQLCipher 키 파생식 회수. 사용자 결정 B경로. PR 없음.
- 판 바뀐 사실: 사용자 로그인 → chat_data\chatLogs_*.edb (실대화 DB, SQLCipher 엔트로피 7.997) 생김 = 실복호 정답지 확보.
- 접근: (1)passive VM_READ 로 언패킹 코드 메모리 덤프(SAC안전) →(2)정적으로 키파생 루틴 →(3)폴백 WinDbg(서명, 보고후) →(4)sqlcipher 파라미터(compat/page/kdf) 규명. 성공판정=chatLogs 사본 실복호(테이블·행수, 본문 미열람).
- Run: run_562b2ec38263 (공유) · Task: task_a0313e967c80 · Dispatch: ctx_60ceb4798005
- 워커handle: term_0f75ed4f-440d-43ef-a670-523b7b65aef7 (spike1·2 동일, context 보존)
- 워크트리: C:/Users/sc971/orca/workspaces/mykakao/poc-windows-key-derivation (공유)
- 코디handle: term_eda12742-b6d9-434d-8eb8-f534be92dcc3
- 완료 캐치: 2채널. 폴링 금지. Frida 금지(SAC). 안전규칙: 키/대화 마스킹·원본 미수정·SAC 미변경.

## §종료 (2026-09-02) — spike 3 done
- 판정 (B): passive VM_READ 로 각 .edb SQLCipher raw key(32B) 회수 → chatLogs_18332…edb 실복호 성공(chatLogs 1455행, 본문 미열람). 8 DB 키 회수, 전부 달라 파일별 키.
- SQLCipher 파라미터 확정: compat=4, page 4096, reserve 80(IV16+HMAC-SHA512 64), raw-key 모드.
- 이식형 파생식(device/user→key) 미회수: ground-truth 8쌍으로 PBKDF2/해시 가설 전수했으나 전부 불일치. 현재 복호는 '카톡 실행중 메모리 회수' 의존(오프라인 이식 불가).
- 검증(코디): 16 passed / 실값유출0 / 스크래치 사본 삭제 / 카톡 생존 / 원본 읽기만.
- 산출물(비커밋): key_recover.py·key_analysis.py·test_key_recover(3)·KEY_REPORT.md.
- 다음(무거움, 별도발주): (a)KakaoTalk.exe 언패킹+Ghidra (b)WinDbg BP on sqlite3_key. 설치 전 보고 필요.
- Task completed / released. PR 없음.
