
# [frontend] 채용담당자 채팅 화면 — 홈 재구성 · /chat · 폴링 대화 표면 (KDEV-WORK-024)

너는 **kknaks-dev `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/orchestration/roles/kknaks-dev/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ **BE 워커가 같은 워크트리의 `app/back/`·`app/mcp/` 에서 병렬 작업 중** — 읽기만 하고 절대 수정하지 마라. BE API 가 아직 없어도 기다리지 마라 — 계약(§3)대로 mock 으로 개발한다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/20-spec/spec-017-recruiter-chat.md` ← **계약의 SoT. 여기 없는 건 발명하지 마라.** (§2 U-1~U-6 화면 계약 · §3 S-1~S-8 · §4 API/에러/폴링)
- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/30-work/work-024-recruiter-chat-frontend.md` ← 빌드 계획 (Phase 1~3 · Code Surface)
- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/21-html/chat-home-mockup.html` ← **시각 정본.** 브라우저로 열어 세 상태(히어로·/chat 빈 상태·대화+사이드바)를 직접 눌러 보라. 마크업·CSS 값은 여기서 그대로 가져온다
- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/10-decision/decision-025-chat-first-home.md` ← 왜 이 구성인지 (D1~D3)

**기대는 개념** — 해당 없음 (UI 이식 작업. 시안과 spec 이 기준의 전부다).

## 2. 배경 / 무엇을 바꾸나

홈 첫 화면의 히어로 터미널(`whoami` 데모)을 **채팅 히어로**로 교체한다 — 인사말 + 터미널
스타일 입력창 하나. 아래 스크롤의 기존 `LandingPreview` 섹션은 그대로 산다. 질문을 보내면
`/chat` 으로 이동해 대화가 시작되고, `/chat` 은 사이드바(＋ 새 대화·대화 목록)와 스레드
(질문 `$ ask` 줄 · 답변 블록 · tool 단계 박스 · 근거 카드)로 구성된다. 실시간처럼 보이는
건 **2초 폴링** — pending 동안 `content`(부분 텍스트)와 `steps` 가 자라난다.

## 3. 계약 (BE 와 합의됨 — 이대로 소비. 필드명 임의 변경 금지)

SPEC-017 §4 가 전문이다. 요지:

- `GET /api/chat/conversations` → 대화 목록(최신순). 쿠키는 브라우저가 알아서 (httpOnly — JS 로 만지지 마라)
- `POST /api/chat/conversations` `{question}` → 201 `{conversation:{id,title,createdAt}, messages:[user, assistant(pending)]}`
- `GET /api/chat/conversations/{id}` → `{conversation, messages}` — message = `{id, role, status(pending|done|failed), content, sources:[{type,slug,title,url}], steps:[{tool,argsSummary,durationMs,calledAt}], createdAt}`
- `POST /api/chat/conversations/{id}/messages` `{question}` → 201. 409 `CONVERSATION_BUSY` 는 컴포저 잠금으로 선차단
- 에러 표시: 422 `QUESTION_TOO_LONG` → 「질문은 1,000자까지 입력할 수 있습니다」(컴포저 아래) · 404 → 빈 상태로 이동 · `failed` → 「답변 생성에 실패했습니다. 다시 시도해 주세요.」 + `다시 시도`(같은 질문 재전송)
- **폴링**: pending assistant 가 있는 동안만 2초 간격, done/failed 로 중단. 언마운트·대화 전환 시 cleanup

BE 가 미완이어도 이 shape 의 fixture mock 으로 개발한다(모의 지연·steps 증가 포함).
mock 은 lib 안에서 갈아끼우기 쉽게 — 통합 시 실 API 로 전환하는 스위치를 남겨라.

## 4. 먼저 읽을 핵심 파일 (워크트리 안)

- `app/front/app/page.tsx` — 현재 홈 조립 (HeroTerminal + LandingPreview)
- `app/front/components/home/hero-terminal.tsx` — 제거 대상. 터미널 창 마크업 관례 참고
- `app/front/components/shell/topnav.tsx` — `00 Ask` 탭 추가 위치
- `app/front/lib/api.ts` — API 클라이언트 관례
- `app/front/app/globals.css` — 디자인 토큰 SSOT (시안도 이 토큰을 쓴다)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/front/`

## 6. 구현 단계 (work-024 의 Phase 그대로)

1. **P1 홈 재구성**: `chat-hero` 컴포넌트(시안 이식 — 100vh·인사말·입력창·scroll 큐·칩 없음) → 질문 전송 시 `/chat?q=` 이동 → `hero-terminal` 제거·`page.tsx` 재배선 → topnav `00 Ask`(+`/chat` 활성 표시)
2. **P2 /chat + 폴링**: 라우트 + 사이드바 + 빈 상태 + 스레드 + 컴포저(pending 중 잠금·placeholder 「답변을 기다리는 중…」) + API 클라이언트·타입·2초 폴링 훅 + `?q=` 첫 질문 자동 전송 + Case Matrix FE 출력
3. **P3 tool 단계·근거·어드민**: steps 증분 렌더(`⚡ tool · N단계`·진행 중/완료 뱃지·완료 후 접힘·0건 미표시) + 근거 카드(type 태그+링크) + 기존 admin 목록에 chat_exposed 토글(관례 따라 최소)
4. work-024 문서의 Phase Status 는 **네가 갱신하지 않는다**(코디네이터 몫) — 보고에 Phase 별 결과만 적어라

## 7. 범위 제약 — 하지 말 것

- `app/back/`·`app/mcp/`·`para/`·`orchestration/` 수정 금지
- 새 색·새 폰트·CSS 프레임워크·차트/애니메이션 라이브러리 도입 금지 — globals.css 토큰만
- spec 문구 임의 변경 금지 · WS/SSE 금지(폴링만) · 모바일 사이드바는 숨김(≤720px, 시안과 동일)
- `npm run build` 전체 빌드 금지 (사용자 방침)

## 8. 검증

```
cd app/front && npx tsc --noEmit (네가 만진 파일 0 에러). 전체 빌드 금지 — 사용자 방침. 검증은 1회만
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_53806a6d-ced5-4948-88bd-4181b7ba4323 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
