# [backend] 실물 버그 3 — 일시정지·재개 뒤 실시간 전사가 멈춘다(녹음은 계속) · 조사 → 수정

너는 **task-management `backend` 워커**다. 사용자가 실제 회의(id 12)에서 겪고 있는 버그다. **두 단계**다 — ① 조사(read-only · 지금) ② 수정(코디가 「가라」 한 뒤 — 회의가 끝나야 api 를 재시작할 수 있다).
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

## 0. 어디서

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (HEAD `f0d4d46`). 스택 떠 있음. **⚠ api 는 `--reload` — `app/back` 아래 파일을 지금 고치면 진행 중인 회의 12 의 WS 가 끊긴다. ① 단계에서는 어떤 파일도 쓰지 마라.** 로그 · DB SELECT · 코드 읽기만.

문서(읽기 전용) — `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`
- `20-spec/spec-007-meeting-live.md` §4 WS 프레임(오디오 · 일시정지 · 재개 · 종료 코드 1000/1008/1011) · U-1 일시정지 · §5
- `40-architecture/backend/README.md` §5-1(스트림 · 업스트림 Soniox realtime · 재연결 없음 규칙) · §8-2
- `40-architecture/database/domains/meeting.md` M-11(at_ms 오프셋)

## 1. 코디가 관찰한 것 (회의 12 · 2026-09-08 12:50 시작 · KST)

```
12:50:45  /start 200 · WS accepted #1(포트 22011) · connection open
~12:50~53 오디오 파일 12.bin 은 계속 커진다(2분에 2.1MB) · Soniox TCP established 1 · 전사 블록 0 (2분 30초 동안)
          사용자: 「일시정지했다가 다시 연결」
12:5x     WS accepted #2(45600) · connection open
          전사 블록 2개 생김 — at_ms 90987~97767 · 103047~104247 (55자 · 「안녕하세요. 고객사 대리님 …」 「어떤 내용이 있으신가요?」)
12:55:36  배치 seq 1 succeeded(안건 전환 트리거 추정) — AI 트랙 빈 목록(입력 55자)
12:5x     WS accepted #3(24963) · connection open
12:58     전사 블록 여전히 2개 · max(end_ms) 104247 · 파일 11.7MB · Soniox TCP 1개 · api 로그에 「connection closed」 0회(셋 다) · 예외/WARNING 0
```
회의 10 · 11(같은 오전 · 정지 없음)은 블록 10 · 57 · 배치 2 · 15 로 정상이었다.

## 2. 후보 (검증하라 — 추측으로 고치지 마라)

```
A  두 번째 WS 규칙 — meeting_stream_service.serve(): `if meeting_id in _sessions: 두 번째만 닫는다(CLOSE_CONFLICT stream_active)`. 클라이언트가 재연결(#2, #3)했을 때 옛 세션이 레지스트리에 남아 있으면 새 WS 가 1008 로 닫힌다. 그런데 닫힘 로그가 0회 — uvicorn 이 안 찍는 건지, 실제로 안 닫힌 건지. #2 에서 블록이 생겼으니 #2 는 살았다. #3 은?
B  일시정지/재개 — `_pause()` 가 partial 을 비우고 `_resume()` 이 base_ms 만 옮긴다. 업스트림(Soniox) 세션은 그대로다. 정지 중에도 클라이언트가 오디오를 보내나 · 재개 뒤 업스트림이 토큰을 안 내는데 `_pump_upstream` 도 안 끝나는(그래서 _fail 도 없는) 상태가 가능한가 — Soniox 가 「오디오는 받는데 인식 결과 0」인 조건(컨테이너 헤더 · 코덱 · 무음)
C  클라이언트 recorder — `app/front/src/features/meetings/hooks/audioCapture.ts`(읽기만): 일시정지 = `MediaRecorder.pause()`(같은 컨테이너) · 새 WS = 새 recorder(새 webm 헤더). 새 WS(#2 · #3)에 새 recorder 가 붙었는데 서버가 같은 Soniox 세션에 두 번째 webm 헤더를 이어 붙이면 디코더가 멈출 수 있다. 서버가 WS 당 Soniox 세션을 새로 여나(있으면 A 와 엮인다)
D  파일 저장 — 어느 경로에서든 `storage.append` 는 계속 된다(파일 성장). 전사와 저장이 갈라진 지점을 찾아라
```

## 3. ① 조사 — 산출물

`/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/stream-stall-investigation.md`
- 타임라인(api 로그 · DB `meeting_transcript` at_ms · 파일 크기 · `meeting_batch_run`)을 **초 단위**로 재구성
- 후보 A~D 각각 「맞다/아니다/모른다 + 근거(파일:줄 · 로그 줄)」
- 원인 확정 못 하면 **어떤 로그를 더 찍어야 하는지**(어느 함수에 무슨 필드) — 그것이 ② 의 첫 항목이 된다
- **수정 계획**(파일 · 함수 · 계약 위반 여부 — SPEC-007 §4 「재연결 없음 · 끊김은 세션 삭제」 규칙과 부딪히면 결정 필요로 올려라 · 고치지 마라)

끝나면 §9 로 보고하고 **멈춰라.** 코디가 회의 종료를 확인하고 ② 를 지시한다.

## 4. ② 수정 (코디 지시 뒤)
- 조사에서 확정한 원인만. 프론트 원인이면 코디가 프론트에 따로 발주 — 너는 `app/back/` 만.
- `make test` · 회의 흐름 테스트(정지 → 재개 → 토큰 이어짐 · 재연결 규칙) · 정적.

## 5. 하지 마라
- ① 단계에서 파일 쓰기 0(`app/back` · `app/front` · compose · `.env`). 컨테이너 재시작 0. 회의 12 의 행 UPDATE/DELETE 0.
- `:3000` · 사용자 앱 프로세스 건드리지 마라.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_fd9fc1ce-619d-4f87-b218-10dfaefaa275 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: 전사 멈춤 조사(①)" \
  --body "원인(확정/후보) / 후보 A~D 판정 한 줄씩 / 수정 계획(파일·함수) / 결정 필요 항목 / 리포트 경로"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] backend 완료 — 전사 멈춤 조사. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] backend: <질문>" --enter`
