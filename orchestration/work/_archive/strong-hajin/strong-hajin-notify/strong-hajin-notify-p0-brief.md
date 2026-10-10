# [frontend] 알림 구현 P0 — 코드 전 조사 셋 (읽기 전용)

너는 **strong-hajin `frontend` 워커**다(셸 · Rust 포함). 이 워크트리에서 조사(`fe-survey-report.md`)를 한 그 워커일 수 있다. 맥락이 없으면 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 문서) · 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify/AGENTS.md`
- 조사 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-survey-report.md`
- **할 일 정본**: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/30-work/work-013-notifications.md` **「Phase P0 — 조사」 절** · 계약 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-009-mac-kakao-collector.md` OQ-K01 · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-011-notifications.md` OQ-1108 · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md` 「시스템 알림 수용」 · 운영 기준 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/prod-check-1.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify` — ⚠ backend 워커가 `backend/` 에서 WP1-BE 구현 중. **코드를 고치지 마라(이 판은 조사다).**

## 물음 (WORK-013 P0 그대로)

1. **P0-1 카톡 「내가 보냄」 재료(OQ-K01)** — 이 Mac(사용자 Mac)의 카톡 로컬 DB 를 **수집기와 같은 방식으로, 읽기 전용 사본에서** 연다(`frontend/src-tauri/src/kakao/` 의 읽기 경로를 따라 — 키는 기기에서 유도, Mac 밖으로 내지 않는다). 수집기가 고른 방 3개에서 `authorId == 내 userId`(`NTChatContext` 등 — 실제 이름은 코드에서 확인) 인 줄 수를 1:1 · 단체방별로 센다 → 운영 기준(**본인 14건 · 방 3개**, 단 운영은 수집 시점 이후만 있다 — 로컬은 더 많을 수 있으니 **운영에 있는 logId 범위로 맞춰** 비교)과 **맞음 / 다름 / 열 수 없음**
   - **사람 이름 · 본문 · 키 · 경로의 비밀값을 출력·기록하지 마라 — 개수와 판정만.** 사본은 scratch 에 두고 끝나면 지운다. 실행 중인 카톡 · medi-ax 앱 · 수집기 프로세스는 건드리지 마라
   - 운영 logId 범위가 필요하면 [질문] 으로 코디에게(코디가 운영에서 뽑아 준다)
2. **P0-2 알림 플러그인 클릭 콜백(OQ-1108)** — 쓰려는 Tauri 2 데스크톱 알림 플러그인 판(`tauri-plugin-notification` 등 — 판 번호 명시)이 **macOS 에서 사용자가 알림을 눌렀을 때 앱에 콜백**을 주는가(문서 · 소스 · 이슈 — 링크와 근거 줄). 못 주면 대안(OS 기본 = 앱 활성화 · 웹이 「마지막 알림」 으로 가는 길 · 다른 크레이트) 과 각 비용
3. **P0-3 권한 · 서명 영향** — 미서명 `tauri dev` 와 서명 dmg 에서 권한 프롬프트 · 표시가 어떤지(문서 근거 · 실기는 WP4) · Info.plist 키 필요 여부 · Windows 는 pending

## allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/p0-report.md` 하나만 쓴다(+ scratch 의 임시 사본 — 끝나면 삭제). 코드 수정 · 커밋 금지

## 하지 말 것
- 코드 수정 · 빌드 산출물을 워크트리에 남기기 · 사용자 포트·프로세스 · 운영 접속 · 실명·본문 기록

## 리포트 `W/p0-report.md`
§0 한 줄 요약(P0-1 판정 · P0-2 콜백 있음/없음 · P0-3) · 항목별 근거 · 사용자에게 물을 것

## 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_aa9fb9af-eed1-45ee-baad-95e52082321d --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: P0 조사" \
  --body "리포트 경로 / P0-1 판정 / P0-2 / P0-3 / 물을 것"

orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d \
  --text "[worker_done] frontend P0 조사 완료 — <한 줄 요약>. 리포트 p0-report.md" --enter
```

- 막히면: `orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d --text "[질문] frontend: <질문>" --enter`
