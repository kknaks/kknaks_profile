# [reviewer] 알림 — SPEC-011 · SPEC-006 v0.7.0 · SPEC-008 v0.7.0 · SPEC-009 v0.6.0 · WORK-013 검수

너는 **strong-hajin `reviewer` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify/AGENTS.md`

경로 약어: `P/` = `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/` · `W/` = `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/` · `D/` = `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/reference/2026-09-10-sc-meeting/package 2/` · 코드 `C/` = `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify/`(origin/main `d2a06fa`)

## 0. 이것은 검수다 — 읽기 전용

판정(PASS / WARN / FAIL)과 근거만 낸다. 문서·코드를 고치지 마라. 산출물은 리포트 한 장.

## 1. 검수 대상

- `P/20-spec/spec-011-notifications.md` (신설 v0.1.0)
- `P/20-spec/spec-006-tauri-wrapper.md` · `spec-008-external-channels.md` · `spec-009-mac-kakao-collector.md` (개정 — `git -C /Users/kknaks/orca/workspaces/kknaks_profile/beluga diff -- <파일>` 로 바뀐 곳)
- `P/30-work/work-013-notifications.md` (신설)

근거: `P/10-decision/decision-010-notifications.md`(**결정 정본** · D-01~D-35 · 사건 × 관계 표 사용자 확정 전 행 · 열린 OQ 0) · `P/00-baseline/baseline-009-notifications.md` · 확정 시안 `D/Alerts.html` · `D/handoff/alerts/` · `D/handoff/settings/js/data.js` · `D/handoff/shell/js/nav.js` · `W/design-change-1~4.md` · 조사 `W/be-survey-report.md` · `W/fe-survey-report.md` · 운영 확인 `W/prod-check-1.md` · 코드 `C/`

## 2. 물음

1. **결정 대응** — DEC-010 D-01~D-35 와 사건 × 관계 표 **전 행**이 SPEC 어느 절에 빠짐없이, **뒤틀림 없이** 들어갔나(관계 · 항목 id · 꼬리표 · 알림/없음 · 우선순위 · 합침 · 예외 D-33). 빠진 것·다르게 적힌 것을 표로
2. **발명** — DEC/원료에 없는 결정·수치·필드가 들어갔나. 특히 writer 가 「제안 기본값으로 구현」 한 **SPEC-011 OQ-1101~1110** — 각각 DEC 와 부딪히지 않나, 사용자에게 물어야 할 만큼 무거운 것이 있나(있으면 WARN 으로 골라라)
3. **범위** — DEC-010 「이번 범위 밖」(기한 하루 전 · 일일 요약 · 메일·슬랙 DM 경로 · 보관 기간 · 방해 금지·소리 · 창 닫아도 받기 · 서버 푸시)이 들어가지 않았나
4. **계약 충돌** — SPEC-008 의 사건 채널 대체가 남은 절(메시지함 실시간 · 연동 상태 · 답장 결과)과 모순되나 · SPEC-006 §2.5·§4 커맨드 표·origin 허용과 SPEC-011 셸 계약이 맞나(개인판/medi-ax 커맨드 수) · SPEC-009 표지 계약이 「출처는 P0 에서」 를 지켰나(추측 금지)
5. **시안 일치** — 알림 목록·설정 알림·사이드바 점 둘이 확정 시안과 맞나(항목 16 id · label · 기본 on · 꼬리표 종류 · 상태 넷)
6. **SSE 계약의 운영 조건** — 프록시(nginx · Cloudflare Tunnel — `P/70-runbook/runbook-002-production-deploy.md`) 버퍼링·유휴 끊김·하트비트 · Last-Event-ID 이어 받기 상한 · 여러 API 프로세스에서 사건이 닿는 길(LISTEN/NOTIFY) · 워커(meeting_worker 등) 게시 길이 실제로 닫히나 · Rollback(WS 라우트 남김)이 말이 되나
7. **백필** — 일회성 수동 SQL 택일의 근거(`C/backend/src/ax_workspace/modules/external_channels/kakao_ingest.py:196-210` 이 기존 `logId` 를 건너뜀)가 맞나 · 실명이 코드·문서에 박히지 않나 · 적용 전 셈 확인 절차 · 슬랙 기존 줄 `from_me` 채우기
8. **WORK Code Surface 전수** — WORK 가 적은 「닿는 곳」 을 **네가 직접 grep 해 다시 세어라**(최소: `user_events.publish` · `UserEventType` 생성 · `USER_EVENTS_CHANNEL` · `useInboxStream(` · `new WebSocket` · `.emit(` 알림 생성 · `append_audit` 등 사건 × 관계 표의 사건 발생 자리 · `author !=` 안 읽음 판정 · `SideNav` 항목 정의 · 셸 `generate_handler` · `window.eval`). 개수가 다르면 FAIL — 빠진 파일:줄을 적어라
9. **Phase 실행 가능성** — P0 조사가 코드 전에 갈라야 할 것(카톡 표지 출처 · 알림 플러그인 클릭 콜백 · 권한/서명)을 다 담았나 · Phase 마다 선후(BE 계약 고정 → FE) · 검증 명령(`C/` Makefile 타겟, Phase 마다 관련 시험만 · `make verify` 마지막 1회) · 앱 기준 Done Criteria · **데스크톱 앱** 기준 사용자 E2E 체크리스트
10. **사람 눈에 이상해 보일 자리** — 계약은 맞는데 실물에서 사용자가 걸릴 자리(예: 같은 사건이 업무 수신함·알림 목록에 둘 다 · 슬랙 채널 합친 줄이 읽은 뒤 다시 생길 때 · 알림을 눌렀는데 대상이 사라졌을 때 · 권한 거절 뒤 · 재연결 직후 OS 알림이 몰려 뜰 때)를 모아라

## 3. allowed_paths

- `W/review-spec-work-report.md` ← **이 파일 하나만 만든다**

## 4. 하지 말 것

- 문서·코드 수정 · 테스트·빌드·서버 실행 · 운영 접속 금지 · 사용자 포트·프로세스 금지
- 실명·메일 금지

## 5. 리포트 형식

```
# 검수 — SPEC-011 · SPEC-006/008/009 개정 · WORK-013
## 0. 판정 (PASS/WARN/FAIL) + 한 줄
## 1~10. 물음별 — 항목마다 판정 · 근거(파일:줄) · 고칠 것
## 11. FAIL 목록(writer 재발주용) · WARN 목록 · 사용자에게 물을 것(있으면)
```

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 코디handle 은 세션 재연결로 바뀐다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_aa9fb9af-eed1-45ee-baad-95e52082321d --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: SPEC·WORK 검수 <판정>" \
  --body "리포트 경로 / 판정 / FAIL n · WARN n / 사용자에게 물을 것"

# (2) 직접 주입
orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d \
  --text "[worker_done] reviewer SPEC·WORK 검수 <판정> — FAIL n · WARN n. 리포트 review-spec-work-report.md" --enter
```

- 막히면: `orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d --text "[질문] reviewer: <질문>" --enter`
