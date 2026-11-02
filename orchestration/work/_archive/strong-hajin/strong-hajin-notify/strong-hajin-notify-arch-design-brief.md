# [architect] 알림 시안 — 사이드바 알림 목록 · 설정 알림 (Claude Design 쓰기 작업)

너는 strong-hajin `architect` 워커다. **너는 이 작업의 맥락이 없다** — 먼저 읽어라:

- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/roles/strong-hajin/planner/role.md`
- 결정 원장 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/_RESUME.md` §2 (2026-10-07 행 전부)
- 조사 리포트(읽기만) — 같은 폴더 `be-survey-report.md` §6(사건 × 관련된 사람 표) · `fe-survey-report.md`(사이드바·설정 현재 모양)
- **앞 판 시안 작업 — 같은 방식으로 한다**: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/_archive/strong-hajin/strong-hajin-inbox/design-change-1.md` (원격 쓰기 + 로컬 사본 + 파일별 바이트 표) · `design-change-6.md`

작업 위치: **코디 워크트리** `/Users/kknaks/orca/workspaces/kknaks_profile/beluga` (네 워크트리 없음 — 코디와 같은 트리. 아래 지정 파일만)

## 1. 무엇을

Claude Design `7e839512-977c-4142-b4b5-d992df566ffc`(TheSC AX Design System)에 **알림 시안 둘**을 쓴다. DesignSync 쓰기 — **사용자 승인 받음**(2026-10-07).
로컬 사본 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/reference/2026-09-10-sc-meeting/package 2/` 에 **원격과 같은 바이트**로 둔다.

**먼저 원격과 로컬 사본이 같은지 확인**하고 시작한다(다르면 쓰지 말고 [질문]).
DS 부품(`components/ds/*` · `_ds_bundle.*`) · `scax-ui.jsx` · 다른 화면은 건드리지 마라. 새 부품은 화면 css 안에서 만든다(앞 판처럼).

## 2. 시안 A — 사이드바 알림 → 알림 목록 (새 화면)

- 내비 `handoff/shell/js/nav.js` 의 `alert` 항목에 `href: './Alerts.html'` · **안 읽은 수 배지**(지금 `dot: true` 를 숫자로 — DS `NavItem` 이 숫자를 못 그리면 점 그대로 두고 design-change 에 적는다). id·아이콘·라벨은 그대로
- 새 화면 `Alerts.html` + `handoff/alerts/{js,css}/` (메시지함 `Inbox.html` 의 틀·레일 방식을 참고)
- 머리: 제목 `알림` · 안 읽음 수 · **「모두 읽음」**
- 필터: `전체 · 업무 · 메시지 · 회의` (테마 = 설정의 테마와 같은 셋)
- 한 줄(항목):
  - 테마 표시(아이콘/배지) · 안 읽음 점
  - 문장 = **누가 · 무엇을 · 어디에** (예: 「팀원 A님이 ‘견적서 정리’ 업무를 요청했습니다」)
  - **나와의 관계 표시** — 같은 사건이라도 받는 사람의 관계가 다르다(결정 원장): 업무 `담당` · `요청자` · `참조(CC)` / 메일 `받는 사람` · `참조` / 슬랙 `DM` · `멘션` · `채널` / 회의 `소유자` · `참석자`. 작은 꼬리표로
  - 시각(상대 시각) · 누르면 그 업무·메시지·회의로 간다(시안에서는 링크 모양만)
- 날짜 구분(오늘 · 어제 · 이번 주 · 이전)
- 상태: 빈 목록(전체 / 필터별) · 로딩 · 불러오기 오류 — 앞 판 StateSwitch 방식으로 시안에서 볼 수 있게
- 목데이터: 세 테마 × 관계가 고루 섞이게 15~20개. **가상 인물·가상 회사만**(실명·실제 메일 금지)

## 3. 시안 B — 설정 → 알림 설정 (고치기)

대상: `Settings.html` · `handoff/settings/js/settings.v1.jsx`(`NotifySection` · intro `:684`) · `handoff/settings/js/data.js`(`NOTIFY_GROUPS` · `NOTIFY_CHANNELS`) · `handoff/settings/css/settings.css`. **알림 설정 메뉴만** — 다른 메뉴는 그대로.

- **「받는 경로」(`NOTIFY_CHANNELS` · 앱/메일/슬랙 DM) 줄을 걷는다** — 이번엔 앱 알림만(결정 원장 기본값)
- intro 문구를 받는 경로 없는 뜻으로 고친다(예: 「받을 알림을 고른다. 앱이 켜져 있으면 시스템 알림으로도 뜬다.」)
- 맨 위 **전체 알림 on/off** 스위치 — 끄면 아래 전부 흐려진다(비활성)
- 테마 셋 **업무 · 메시지 · 회의** — 테마 머리에 **테마 on/off 스위치**, 아래에 **항목 체크박스**. 테마를 끄면 그 항목들이 흐려진다
- 항목(목 — 확정은 뒤 DEC 에서. 설명 한 줄씩):
  - 업무: 업무 요청을 받았을 때 · 업무가 배정·넘겨졌을 때 · 내 요청이 수락·거절됐을 때 · 완료 보고를 받았을 때 · 보완 요청을 받았을 때 · 기한·조건이 바뀌었을 때 · 내 업무에 댓글 · 선행 업무가 끝났을 때
  - 메시지: 메일(받는 사람으로) · 메일(참조로) · 슬랙 DM · 슬랙 멘션 · 슬랙 채널 새 메시지 · 카톡 새 메시지 · 연동이 끊기거나 수집이 실패했을 때
  - 회의: 회의에 초대됐을 때 · 회의가 바뀌거나 취소됐을 때 · 회의록 정리 완료 · 회의록 생성 실패 · 회의를 공유받았을 때
- 「기한 하루 전」 · 「일일 요약」 은 **뺀다**(범위 밖 — 결정 원장)
- 스위치: 시안 `.scax-switch` CSS 를 쓴다(FE 조사: CSS 는 있고 컴포넌트는 없음). 체크박스는 DS 에 있으면 DS, 없으면 settings.css 에서

## 4. 그리지 않는 것

- OS 시스템 알림 모양(macOS·Windows 배너) — OS 가 그린다
- 메일·슬랙 DM 받는 경로 · 방해 금지 시간 · 소리 — 범위 밖
- 알림 클릭 뒤 도착 화면 자체(기존 업무·메시지함·회의 화면 그대로)

## 5. 끝나면

1. 고친·새 파일을 로컬 사본 같은 경로로(원격과 같은 바이트 · `cmp` 확인)
2. `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/design-change-1.md` — 바꾼 것 · 파일별 바이트·sha256 앞 12 · 일부러 안 그린 것 · **미결(사용자에게 물을 것)**
3. 위 밖의 파일·레포 금지 · **커밋·push 금지** · index·log 수정 금지

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. preamble 과 다르면 **preamble 이 맞다.**

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_aa9fb9af-eed1-45ee-baad-95e52082321d --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: 알림 시안" \
  --body "바꾼·새 파일 / 요약 / 로컬 사본 cmp / 미결"

# (2) 직접 주입 — 코디네이터를 깨운다
orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d \
  --text "[worker_done] architect 완료 — 알림 시안 둘. 상세는 design-change-1.md" --enter
```

- 막히면: `orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d --text "[질문] architect: <질문>" --enter`
