# [frontend] 알림 — 화면·Tauri 셸의 알림 현재 코드 전수조사

너는 **strong-hajin `frontend` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify/AGENTS.md`
- 알림 경계를 그어 둔 문서(읽기만):
  - `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/10-decision/decision-005-tauri-wrapper.md` — D-04 「OS 알림 연결은 래퍼 책임, 알림 시스템은 후속」
  - `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md` §2.5(만들지 않은 것 표) · §4(웹이 부르는 커맨드 표) · 「외부 채널 수집기 수용」 절(트레이·백그라운드 예외)
  - `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/10-decision/decision-008-external-channels.md` D-37 · D-50
- **시안(읽기만)**: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/reference/2026-09-10-sc-meeting/package 2/handoff/`
  - 사이드바: `shell/js/nav.js:5` `{ id: 'alert', label: '알림', icon: 'bell', dot: true }`
  - 설정 알림: `settings/js/settings.v1.jsx`(알림 절 ~`:279`) · `settings/js/data.js`(받는 경로 `앱 알림`「수신함과 좌측 알림에 표시」·`메일`·`슬랙 DM` · 묶음 `업무`·`회의 · 연동`) · `settings/css/settings.css`
  - 시안 조사 선례: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/_archive/strong-hajin/strong-hajin-inbox/design-survey.md` §2.6

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify`
base: `origin/main` (`d2a06fa` — 운영 반영 코드)

⚠ **같은 워크트리에 backend 워커가 동시에 탄다.** 둘 다 읽기 전용 조사이고 서로 다른 리포트 파일 하나씩만 쓴다. `backend/` `frontend/` 어느 쪽도 **고치지 마라.** 네 몫이 아닌 쪽도 답에 필요하면 읽어라(서버 API 모양은 backend 가 자세히 본다 — 너는 화면이 **어떻게 받는지**만).

## 0. 이것은 조사다 — 고치지 마라

**읽기 전용 조사다.** 코드를 한 줄도 바꾸지 않는다. 산출물은 리포트 **한 장**뿐이다.
「이렇게 고치면 된다」는 쓰지 마라 — 사용자가 이 리포트를 보고 계약을 정한다. **지금 무엇이 어떻게 도는지만** 적는다.
테스트·빌드·`cargo` 를 돌리지 마라. 읽어서 답할 수 있는 것만 답하고, 못 답한 것은 「조사 한계」에 적는다.

## 1. 왜 조사하나

사용자가 **알림**을 만든다. 이미 정한 것(2026-10-07 사용자):

- **나와 관련된 것만** 알림이 온다 — 업무 상태 변경 · 메일 · 슬랙 · 카톡 등
- 데스크톱 앱(Tauri)이 **켜져 있을 때만** 시스템 알림을 받는다 — **웹이 지금 있는 실시간 연결로 받아 Rust 로 넘겨 OS 알림을 띄운다**(서버 → 기기 푸시 없음)
- **설정의 알림 메뉴**와 **사이드바(좌측 내비)의 알림**을 이번에 만든다
- 사용자는 **데스크톱 앱만** 쓴다(개인판 `strong-hajin` · 회사판 `medi-ax` 두 판)

빠진 자리가 곧 다음 판의 FAIL 이다 — **시작점에서 멈추지 말고, 같은 심볼·패턴·API 를 쓰는 곳을 grep 으로 전부 세어 숫자로 적어라.**

## 2. 물음 (네 몫 = 화면 렌더링·실시간 수신·Tauri 셸)

### A. 지금 화면의 알림

1. 화면이 알림을 **어디서 받고 어디에 그리나** — `lib/api.ts` · `lib/viewModels.ts` · `lib/labels.ts` · `App.tsx` · `shell/AppShell.tsx` 의 notification 관련 전부(파일:줄). 출발점일 뿐이다
2. 사이드바 `shell/SideNav.tsx` 의 항목 정의 · 점(dot)·숫자 배지를 그리는 부품이 있나 · 시안 `alert` 항목이 지금 코드에 있나/없나
3. 수신함 레일(`shell/InboxRail.tsx`)과 「참고」 카테고리 — 알림과 같은 데이터를 쓰나, 읽음 처리 화면 동작
4. 토스트 등 **앱 안에서 짧게 알리는 부품**이 있나(DS 부품 · 전역 레이어)

### B. 실시간 수신

1. 화면이 서버 실시간 경로(`/api/inbox/stream` 등 SSE·WebSocket)를 **어디서 열고 몇 개 여나** — 연결 소유자(전역/화면별), 화면을 옮겨도 유지되나, 받은 사건을 어디로 나눠 주나(파일:줄)
2. 받는 사건 종류 전부와 각 사건에 화면이 하는 일
3. 끊김·재연결·로그아웃 때 동작

### C. 설정 화면

1. 지금 설정 화면 구조(`SettingsLanding` 등) · 메뉴 묶음 · **`알림 설정` 자리가 지금 어떻게 되어 있나**(숨김·비활성·없음)
2. 시안 알림 설정(§0 의 `settings.v1.jsx` · `data.js`)과 대조표 — 항목·스위치·문구·부품, 지금 DS·코드에 있는 부품으로 그릴 수 있나(없으면 DS-gaps 후보)
3. 시안의 사이드바 `알림`(bell · dot)을 누르면 **무엇이 열리는지** 시안에 있나 — 없으면 「시안 없음」 이라고만 적는다(지어내지 마라)

### D. Tauri 셸 — 시스템 알림을 띄울 길

1. `frontend/src-tauri/` 의 현재 구조 — `lib.rs` 의 커맨드·플러그인 등록 전부 · `Cargo.toml` 의존 · `capabilities/` · `flavors/<판>/`(`tauri.conf.json` 오버레이 · `shell.config.json` · `capabilities/product-shell.json`)
2. **웹 → 셸 커맨드 경로** — 원격 문서(운영 origin)가 부를 수 있는 커맨드가 어떻게 허용되나(origin 제한 · SPEC-006 §4 의 「커맨드 넷」) · 웹 쪽에서 Tauri 를 부르는 코드 위치와 「Tauri 안인가」 판별 방식(파일:줄)
3. **셸 → 웹 사건 경로**(SPEC-006 저장 결과 사건 등) — 알림 클릭 후 화면 이동(딥링크)에 쓸 수 있는 기존 경로 사실만
4. OS 알림 수단이 지금 있나 — `tauri-plugin-notification` 등 의존 유무 · Info.plist · Entitlements.plist · 서명 설정에서 알림과 닿는 것(macOS 알림 권한·번들 id `app.stronghajin.desktop` / `app.ax.desktop`) · Windows 쪽(AppUserModelID 등) 설정 유무
5. 창을 닫거나 숨기면 프로세스·웹뷰가 살아 있나 — 판별로(개인판 / medi-ax 수집기 트레이 예외) · `shell_ui.rs` · `guard.rs` 의 창 수명 처리. 「앱이 켜져 있다」 가 어떤 상태인지 코드 기준으로
6. 웹뷰가 **포커스 없을 때·숨었을 때** 실시간 연결·JS 타이머가 계속 도나 — 코드·설정으로 확인되는 것만(WKWebView·WebView2 실측은 조사 한계로)

### 공통

- 위 각 자리의 테스트 위치(vitest 파일 · `cargo test` 모듈) — 다음 판이 고칠 테스트 범위를 세기 위해

## 3. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-survey-report.md` ← **이 파일 하나만 만든다**

코드 워크트리·시안은 **읽기만** 한다. 커밋·push·PR 금지.

## 4. 하지 말 것

- 코드·테스트를 고치지 마라. 테스트·빌드·`cargo` 를 돌리지 마라
- **서버·프론트·Tauri 를 띄우지 마라. 사용자 포트와 프로세스를 건드리지 마라** (8001·5176·54329)
- 브라우저를 열지 마라. 운영 서버에 접속하지 마라
- 「이렇게 바꾸자」를 쓰지 마라
- 리포트에 사람 실명·메일을 쓰지 마라(공개 레포로 아카이브된다) — 「팀원 A」처럼 쓴다

## 5. 리포트 형식

```
# 알림 조사 (frontend)

## 0. 한 줄 요약 — A~D 각 한 줄
## 1~. A~D 절 — §2 물음 번호대로 답
## N. 시안 대조표 — 사이드바 알림 · 설정 알림 (시안 · 지금 코드 · 부품 유무)
## N+1. grep 개수표 — 센 심볼과 개수
## N+2. 실측 필요 — 코드로 못 갈리는 것(OS 알림 권한·숨은 웹뷰 동작 등, 판·OS 별)
## N+3. 조사 한계
```

**모든 답에 `파일:줄` 근거를 단다.** 근거 없는 문장은 쓰지 않는다.

## 6. 검증

- 리포트가 위 경로에 있다. §2 의 물음이 하나도 빠지지 않았다(못 답한 것은 조사 한계에)
- `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify status --short` 가 비어 있다

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. preamble 과 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_aa9fb9af-eed1-45ee-baad-95e52082321d --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: 알림 조사" \
  --body "리포트 경로 / A~D 한 줄 요약 / 실측 필요 / 조사 한계"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d \
  --text "[worker_done] frontend 알림 조사 완료 — <한 줄 요약>. 리포트 fe-survey-report.md" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
