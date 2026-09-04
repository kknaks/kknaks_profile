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
