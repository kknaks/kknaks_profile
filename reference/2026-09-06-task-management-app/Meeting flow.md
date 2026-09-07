# 회의록 전체 흐름

> 정해진 것과 안 정한 것을 한 곳에 적는다.
> **「정함」은 사용자가 확정한 것만이다.** 코디가 제안한 것은 「제안」이라고 적는다.

---

# 1. 회의 시작

## 1-1. 화면에서 무슨 일이 일어나나

```
회의록 목록
  └ 회의를 고른다 → 우측 미리보기
      └ [회의 입장]                      ← F-6 (scheduled · recording)
          └ 시작 전 화면
              안건을 미리 적어둘 수 있다
              상태 바 「기록 대기 00:00:00」
              └ [회의 시작]
                  → 회의 중 화면으로 바뀐다 (페이지 이동이 아니라 상태 변화)
```

## 1-2. 서버에서 무슨 일이 일어나나

```
POST /api/meetings/{id}/start

  ① 상태 전이   scheduled → recording
                recording_started_at = now()          ← 경과 시간·근거 칩의 기준점
                **한 UPDATE**

  ② 웜스타트를 **큐에 넣는다**

  ③ **즉시 응답**                                      ← 기다리지 않는다

  ④ (나중에) 워커가 끝나면 ai_session_id 를 UPDATE
```

**✅ 정함 — 기다리지 않는다** (2026-09-07)

```
전    /start 가 codex 응답까지 기다렸다 → 실측 13초 스피너
      매 회의마다 걸린다(회의당 세션 하나). 컨텍스트가 클수록 길어진다

후    큐에 넣고 끝

근거  웜스타트에서 받는 것은 **session_id 하나**다. 결과 본문은 버린다
      (meeting_batch_service.py:640 · DEC-003 §STT 「결과 무시」)
      그 id 는 **첫 배치 때까지만** 있으면 된다 —
      첫 배치는 확정 발화 600자가 쌓여야 도니 최소 몇 분 뒤다

함께 닫힘
  D-2/DG-9  워커가 죽어 있어도 **회의는 시작된다.** 배치만 안 돈다
            → 회의가 recording 에 갇히는 일이 없어진다
  W-1       service 가 commit() 할 이유가 없어진다
            (전이만 하고 끝이니 요청 하나 = 트랜잭션 하나)
```

## 1-3. 프론트가 하는 일

```
/start 응답을 받으면
  └ WS 를 연다        ws://…/api/meetings/{id}/stream
      첫 프레임으로 access 토큰 + 오디오 포맷 선언
      → 서버가 ready 를 준다

  └ 마이크를 잡는다    getUserMedia({audio:true})   내 마이크만
      **「재개」를 눌렀을 때만** 부른다 — 권한 프롬프트가 사용자 동작에 붙어야 한다
      실패하면 일시정지 + 사유 배너. 자동 재연결하지 않는다

  └ 오디오를 보낸다    250ms 단위. 서버가 ① 녹음 파일 append → ② Soniox 순으로 흘린다
```

**실물 확인에서 밟은 것 (2026-09-07)**

```
macOS   Info.plist 에 NSMicrophoneUsageDescription 이 없어 권한을 안 물었다
        → 넣었다. tauri dev 실행파일에도 박힌다(tauri-codegen)
CSP     connect-src 에 ws://localhost:8000 이 없어 WS 가 막혔다
        → 넣었다. 3000(Next HMR)만 있었다
Windows WebView2 는 PermissionRequested 를 처리해야 getUserMedia 가 산다
        → 코드는 넣었으나 **실물 확인 못 했다**
```

## 1-4. 웜스타트가 AI 에게 주는 것

**MCP 가 붙으면 컨텍스트를 싣지 않는다.** 역할·규칙·용어·도구만 준다.
프롬프트 초안은 `ai-prompt-draft.md` §A.

```
역할        「회의에 참가하는 두 명 중 하나」 — 사람과 AI 가 각자 쓰고 종료 후 합친다
흐름        발화가 배치로 온다 · 종료 후 통합본 · 사람 트랙은 읽기 전용
용어 다섯    안건(뼈대) → 논의 · 결정 · 액션 · 업무 가 거기서 파생된다
요약 원칙    압축한다 · 이름 안 쓴다(익명 화자) · 숫자는 그대로 · 말 안 한 건 안 채운다
            확실하지 않으면 한 단계 낮춘다(결정 같으면 논의로)
```

**✅ 정함 — 도구는 API 래퍼다. DB 직결이 아니다**

```
get_meeting()          회의 정보
get_account()          사용자 정보
list_agendas()         사람이 적은 안건
list_tasks(projectId?) 업무 목록
get_task(id)           업무 상세 (할일 · 메모 · 연관 · 일정)
list_work_types()      유형 목록 (이름 · 종류 · 설명)
```

**✅ 정함 — 못 쓰게 하는 것은 설정으로 잠근다**

```
프롬프트에도 적지만 실제 차단은 codex 설정이 한다

features.shell_tool=false · web_search="disabled"
features.image_generation=false
features.apps=false          ← 안 걸면 mcp__codex_apps__ 27종이 붙는다(mediness 실측)
sandbox="read-only"
enabled_tools = 우리 툴 6개만    ← **allow list.** 빈 배열이면 하나도 안 열린다
tools.<툴>.approval_mode="approve"   ← **툴별로.** 서버 기본이면 새 툴이 자동 면제된다

deny list 는 없다 — allow list 뿐이다 (codex 0.147.0 실측)
  모르는 키를 넣어도 조용히 통과한다 → disabled_tools 가 안 터진 건 지원한다는 뜻이 아니다
  우리 툴 쪽은 그래서 **안전하다**. 위험은 codex 내장 쪽뿐이고 버전 올릴 때 확인한다
```

**✅ 정함 — 토큰** (mediness landing-chat 방식을 따른다)

```
사용자 세션 JWT 를 그대로 주지 않는다
회의(turn)마다 **본인 계정으로 단명 토큰을 새로 발급**한다
전달    -c mcp_servers.<key>.http_headers={Authorization="Bearer …"}
        (--bearer-token-env-var · OAuth 안 씀 · 설정 파일을 안 만든다)
마감    best-effort 폐기. 실패는 자연 만료로 흡수

권한 경계는 **백엔드가 진다.** MCP 는 두 번째 게이트가 아니다
```

## 1-5. 아직 안 정한 것

```
① MCP 서버 구축이 과제다
   지금 코드는 컨텍스트를 프롬프트에 실어 보낸다. MCP 서버가 없다
   → 별도 work 로 나간다. 만들면서 걸리는 건 그때 고친다

② 우리 백엔드에 토큰 인프라가 있나
   mediness 는 OAuth family · rotation · revocation-list 위에 서 있다
   우리에게 그게 있는지 **확인 안 했다**

③ 웜스타트 실패를 어떻게 다루나
   지금은 전파(설계 밖). 큐로 밀면 배치 실패와 같은 경로(조용히 로그)로 가는 게 자연스럽다
   — 확정 안 함
```
