# [winapp] 수정 — 대화방 클릭 시 그 방 즉시 수집 시도(스피너)

너는 **mykakao `winapp` 워커**다. 같은 워크트리. 커밋 금지(코디).

## 증상 (사용자 실기동)
- 탭2 "채팅방+채팅목록"에서 방(예: 이건학·조상아)이 **카톡에선 열려 있는데** 앱은 "대기 중·닫힘"으로 표시. 그 방을 클릭해도 **수집을 시도하지 않고** "대기 중" 상태 화면만 보여줌.
- 사용자 기대: **대화방 클릭 = 스피너 돌면서 그 방 즉시 수집.** 열려있으면 수집→대화 렌더, 진짜 닫혔으면 그때 "대기 중".

## 원인
- 백그라운드 재조정(3s open-edge)이 이 방들의 열림을 못 잡음(세션 키캐시에 그 방 키 없음 → "닫힘"으로 봄).
- 탭2 방 클릭(openChat/openRoom) 은 **저장된 상태만 렌더**하고 능동 수집 트리거가 없음.

## 고칠 것
1. **능동 수집 엔드포인트**: `POST /api/collect` body `{chat_id}` → 그 방에 대해 **키 회수(캐시 miss 면 1회 재harvest 허용) + 델타 import**를 즉시 실행 → 결과 상태 반환(`{status:"done|waiting|error", rows}`). 열린 방이면 collecting→done, 못 회수하면 waiting. (process_delta/import 로직 재사용.)
2. **탭2 방 클릭 시**: 그 방이 이미 `done` 이 아니면(또는 항상) → 대화영역에 **"수집 중" 스피너** 표시 → `/api/collect` 호출 → 완료되면 메시지 로드+SSE 구독. `waiting`(닫힘) 이면 기존 "대기 중" 안내. 이미 done 이면 바로 렌더.
3. 스피너/상태 전이가 깔끔하게(중복 호출·플리커 방지). 클릭 연타 안전.

## 검증 (라이브 — 사용자 협조)
- 카톡에서 방 열어둔 상태로 앱 탭2에서 그 방 클릭 → **스피너 → 수집 → 대화 렌더**. 
- 진짜 닫힌 방 클릭 → "대기 중" 안내(무한 스피너 아님).
- cargo build --release + cargo test. 값·URL·토큰 미출력.

## 안전 (불변)
- 원본 읽기만·카톡 무변조·SAC 관계없음(꺼짐)·키 RAM only·키/본문/URL 로그·커밋 비노출. `win_app/` 밖·문서 SoT 수정 금지.

## 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "클릭 수집 완료: <한 줄>" --body "/api/collect/클릭 스피너·수집/닫힘 처리/cargo 수치"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] 클릭 수집 완료 — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`
