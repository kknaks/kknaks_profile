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
