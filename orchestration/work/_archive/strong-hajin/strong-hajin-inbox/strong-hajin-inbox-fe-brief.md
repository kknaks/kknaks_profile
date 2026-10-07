
# [frontend] WORK-011 Phase FE-a(메시지함) → FE-b(설정·프로필) — 순서대로

너는 **strong-hajin `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-inbox`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**같은 코드 워크트리에서 backend 워커 둘(BE-2·BE-3)이 `backend/` 를 동시에 고치고 있다. 너는 `frontend/src/` 만(셸 `frontend/src-tauri/` 는 다음 Phase — 건드리지 마라).** 커밋 금지.

## 1. SSOT — 먼저 읽을 것 (너는 맥락이 없다 — 이게 전부다)

- **확정 시안 = 정본** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/reference/2026-09-10-sc-meeting/package 2/` — `Inbox.html`(메시지함) · `Settings.html` + `handoff/inbox/*` · `handoff/settings/*` · `handoff/shell/js/nav.js`. 시안이 기획보다 우선. 시안에 없는 것은 DS-gaps 로 기록(발명 금지)
- 시안 변경 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/design-change-1.md` ~ `design-change-6.md` (어떤 화면·상태가 왜 이렇게 됐나)
- **SPEC-008** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-008-external-channels.md` v0.5.1 — §2 UX Contract · §4 Interface(요청/응답/오류) · HTML 메일 샌드박스 iframe 계약 · 실시간 WS
- **WORK-011** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/30-work/work-011-external-channels.md` — 「Phase FE-a」·「Phase FE-b」 절
- 코드 레포 `AGENTS.md` · 기존 DS(`frontend/src/ds/*` — `DropZone`·`FileList` 등 · `.design-sync/`) · `lib/api.ts` 규칙

**백엔드는 아직 만들어지는 중이다** — API 는 **SPEC §4 모양 그대로** 짜고, 시험은 가짜 응답으로. 실제 서버 붙여 보기는 코디가 BE-3 뒤에 한다.

## 2. 배경

메일·슬랙·카톡이 사람마다 쌓이는 **메시지함**과, 연동·프로필을 다루는 **설정**을 만든다.

## 3. 계약

SPEC-008 §4 그대로. 카톡 방 고르기는 **데스크톱 앱 안에서만**(Tauri 커맨드 `kakao_list_rooms` 등 — SHELL Phase 가 만든다) — 너는 `lib/shell.ts` 에 **그 커맨드를 부르는 자리만** 두고(없으면 「Mac 앱에서 고릅니다」 분기), 실제 커맨드는 다음 Phase.

## 4. 먼저 읽을 핵심 파일

시안 jsx(`handoff/inbox/js/inbox.v1.jsx` · `handoff/settings/js/settings.v1.jsx`) · `frontend/src/App.tsx`(surface 등록) · `frontend/src/shell/*`(내비) · 기존 화면 하나(예: 업무 탭)의 구조 · `features/assistant/AssistantCharacterPicker.tsx`(프로필로 옮길 것)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `frontend/src/` (새 `features/inbox/` · `features/settings/` · `App.tsx`·내비 등록 · `lib/api.ts`·`lib/shell.ts` 추가) · `frontend/` 의 시험 파일
- **금지**: `frontend/src-tauri/` · `backend/`

## 6. 구현 단계

**FE-a 메시지함** (WORK-011 FE-a 전부)
1. 내비 「메시지함」(독립 화면) · 출처 탭 전체/메일/슬랙/카톡 · 카드(메일 한 통 / 방 하나 · 미읽음) · 카드 누르면 원문+읽음 · `모두 읽음으로` · 네 상태
2. 메일 본문: 폭 전체 · 머리 표(보낸·받는·참조·날짜·받은 계정) · **HTML 은 샌드박스 iframe**(SPEC 계약 그대로 — 스크립트 금지·높이 맞춤·링크 새 탭·인용 접기) · 첨부 카드(받기 = API 중계)
3. 슬랙·카톡 본문: 슬랙 대화방처럼(날짜 구분 · 같은 사람 5분 묶음 · blocks 우선/mrkdwn 대체 렌더 · 멘션 이름 · 링크 미리보기 · 이미지/앨범/PDF/파일 카드 · 읽기 전용 리액션 · 봇 `앱` 표시) · **스레드 = 오른쪽 패널 3열** · 카톡은 입력창·스레드 없음 · 만료 첨부 「만료됨」 · 동영상/음성 칩
4. 답장: 슬랙 입력창 + 스레드 패널 입력창 · 메일 답장/전체 답장 작성 칸 · 첨부 `DropZone`+`FileList`(메일 합계 25MB · 슬랙 50MB) · 보내는 중/실패/보냄
5. 실시간: 메시지함 WS 로 새 메시지 반영 · 수집 실패 배너

**FE-b 설정·프로필** (FE-a 끝난 뒤, WORK-011 FE-b 전부)
6. 설정 메뉴: 메일(「Google로 연결」·계정 여러 개·상태·연결 해제) · 슬랙(연결·방 고르기 창 — 채널/비공개/DM/그룹DM·참여자 실명·봇 `앱`) · 카톡(상태 카드 · **데스크톱이면** 방 고르기(셸 커맨드) / 브라우저면 안내 + 서버 고른 방 목록·빼기) · 기기 토큰(발급 → `kakao_store_device_token` 자리 · 철회 · 마지막 사용) · 연결 시작은 **서버가 준 동의 URL 로**(브라우저 이동 / 데스크톱 `open_external`)
7. 프로필 설정: 이름·소속·직책·직무 읽기 전용 · 프로필 이미지(DropZone · 즉시 저장 · 삭제 · 이니셜) · **AX 캐릭터**(기존 피커 이동 + 기존 진입점 둘 제거 — 검수 W14) · 비밀번호 변경

## 7. 범위 제약

- `src-tauri` · 백엔드 금지 · 시안에 없는 화면 발명 금지 · 사용자 포트·프로세스 금지(dev 서버는 다른 포트)

## 8. 검증

```
코드 레포 AGENTS.md 준수: make frontend-test 및 frontend에서 npx tsc --noEmit, 최종 빌드는 make frontend-build 또는 코디의 make verify. 같은 검증 중복 실행 금지. envelope으로 권한 판단, api.ts 밖 fetch 금지, 기존 부품/viewModels 재사용, 시안 부재는 DS-gaps 기록. Tauri/Rust 변경 시 frontend/src-tauri에서 cargo check, 핵심 상태·경합의 cargo test 및 cargo clippy -- -D warnings를 단계 범위에 맞게 실행. OS별 빌드/실측 증거는 분리하며 macOS 통과를 Windows 통과로 대신하지 않는다. 실제 실행하지 못한 검증은 사유와 함께 pending으로 보고.
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
  --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_e3b0bba1-f7c7-47b9-bdff-111d9894557e \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
