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
