---
type: work
id: WORK-012
title: "고도화 1판 — 운영 버그 · 회의록 생성 고도화 · AX 흐름 · 메시지함→AX · 셸"
status: done
product: strong-hajin
work_type: spec-up
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 0
created_at: 2026-10-07
updated_at: 2026-10-07
tags:
  - product/strong-hajin
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-008-enhance-improvements|BASE-008]]"
    - "[[baseline-007-meeting-creation-improvements|BASE-007]]"
  decisions:
    - "[[decision-009-enhance|DEC-009]]"
  specs:
    - "[[spec-008-external-channels|SPEC-008]]"
    - "[[spec-010-meeting-ax-enhance|SPEC-010]]"
  works:
    - "[[work-011-external-channels|WORK-011]]"
    - "[[work-010-polish3|WORK-010]]"
  releases: []
  related:
    - "[[runbook-002-production-deploy|RUNBOOK-002]]"
sources:
  - orchestration/work/strong-hajin-enhance/_RESUME.md
  - orchestration/work/strong-hajin-enhance/be-survey-report.md
  - orchestration/work/strong-hajin-enhance/fe-survey-report.md
---

# 고도화 1판 — 운영 버그 · 회의록 생성 고도화 · AX 흐름 · 메시지함→AX · 셸

DEC-009(accepted · D-01~D-37 · OQ-901~909 닫힘)가 정한 개선 18건(SH-IMP-001~018 — 019 보류 · 009 완료 · 013① 범위 밖)을 구현한다.
**SPEC-008 v0.6.0**(메시지함·외부 채널) · **SPEC-010 v0.1.0**(회의·회의록·AX) 이 계약의 정본이다.

> **초안이다(`status: todo`).** **검수 fix1(2026-10-07 · `review-spec-work-report.md` FAIL 5·WARN 15 · 코디 판정 `write-fix1-instructions.md`) 반영** — 원본 보기 앱/웹 가르기 · 받기/원본 보기 주소 분리 · AX 수정 카드 편집 계약 신설 + 옛 `meeting.update` 합치기 · `manual` 자리 넷 · timeout 개수(16/3) + `ai.py:23` · 단계별 프로필 · 새 세션 재시도 배치·최종 · KST 셋째 정의 · OQ 전부 닫힘 · 시험 타겟 정정 · E2E 「확인할 것」 H-1~H-10. **SPEC 이 정본이다** — 이 WP 와 SPEC 이 다르면 SPEC 이 맞고, 워커는 코디에게 알린다(Open Issues).
> 근거 줄 번호는 조사 시점(코드 origin/main `f0ad522`) 값이다 — 워커는 **줄이 아니라 심볼로 다시 찾는다**(P-2).
> **Phase 가 그대로 발주 브리프가 된다** — 한 Phase = 한 워커 발주. BE 가 계약을 먼저 고정하고 FE 가 이어받는다.

## Meta

- **SPEC (정본)**
  - SPEC-008 v0.6.0 — §2.2(받기/미리보기) · §2.1 ③ · §4.4(원격 SVG · `integration.changed`) · §2.9 · §4.8(메시지 → AX · 출처 · 「업무 만듦」) · §5(나간 방 · 데스크톱 경계) · AC-23~34
  - SPEC-010 v0.1.0 — §2.1(수정 모달) · §2.2 · §4.1~4.3(회의실) · §2.3 · §4.2(불러오기·안건 출처) · §4.5~4.8(맥락 목록·timeout·정정·보정 표·기한) · §2.4 · §4.4(AX 회의 카드) · AC-01~22
- **Decision**: DEC-009 · **Baseline**: BASE-008(BASE-007 의 네 건 이어받음)
- **코드(읽기만 — 조사 기준)**: `Strong_hajin` origin/main `f0ad522` · 구현 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance`(branch `kknaksss/strong-hajin-enhance`)
- **조사 리포트**: `orchestration/work/strong-hajin-enhance/be-survey-report.md`(BE §n) · `fe-survey-report.md`(FE §n)
- **운영**: RUNBOOK-002 · origin `https://ax.medisolveai.xyz` · 데스크톱 앱 medi-ax

## 이 판의 원칙

| # | 원칙 | 근거 |
|---|---|---|
| P-1 | **구현은 두 판이다.** **1루프** = 계약대로 전 WP 구현 → **사용자 E2E(데스크톱 앱)** → 지적을 **모아서 한 번에** 받아 **2루프**. E2E 도중 단건 발주를 하지 않는다 | `feedback_batch_e2e_feedback` |
| P-2 | **쓰는 곳을 전부 센다.** 아래 Code Surface 의 줄은 출발점 — 같은 심볼·패턴을 **grep 으로 전부** 다시 세고 시작한다. 「고칠 곳 N개」 가 아니라 「그 심볼을 쓰는 곳 전부」. 빠진 자리가 다음 판 FAIL 이다 | `feedback_brief_enumerate_not_list` · WORK-011 P-2 |
| P-3 | **완료 = 앱 실물.** 사용자는 **데스크톱 앱만** 쓴다 — 운영 웹에서 된다는 것은 서버 쪽 근거일 뿐이다(DEC-009 D-03) | `feedback_done_on_user_surface` |
| P-4 | **백엔드를 커밋하면 스택을 재시작한다**(`make local-stack` 재기동 · 워커 포함). 옛 코드가 떠 있으면 「프론트가 안 된다」 로 보인다 | `feedback_restart_stack_after_commit` |
| P-5 | **외부 서비스 경로는 실물 호출 1회가 완료 조건** — The Connect(방 변경·가용) · Gmail(메일 맥락·첨부) · Slack(나간 방·스레드 답글) · Codex/Claude(최종 합성 900초·맥락 목록) | `feedback_real_e2e_before_done` |
| P-6 | **운영과 같은 조건으로 확인한다** — 원격 이미지·첨부 받기는 https 운영 origin 에서(로컬 http 는 셸 TLS 경로를 타지 않는다 — WORK-010 패닉 전례) | `feedback_verify_prod_scheme` |
| P-7 | **워커는 사용자 포트·프로세스를 건드리지 않는다.** 앱 실물·운영 확인은 코디 몫 | `feedback_real_e2e_before_done` |
| P-8 | **디자인 시스템·기존 틀 안에서** — AX 회의 카드는 `AxDraftCard` 틀, 회의실 셀렉트는 부품 하나, 막대 아이콘은 DS 아이콘 단추 | WORK-011 P-5 |
| P-9 | **프론트 시험은 `make frontend-test`**(`vitest run` — 기본이 파일 병렬). **코디·사용자의 로컬 스택이 떠 있는 기계에서는 병렬을 끈다**(`cd frontend && npx vitest run --no-file-parallelism` — 병렬 vitest 가 로컬 스택을 죽인 전례) · 타입 검사는 `make frontend-build`(`tsc` 단독 타겟은 없다) | 사용자 메모 · 검수 W-14 |

## Work Summary

**Phase 순서 = DEC-009 WP 묶음 순서**(WP1 → WP2 → WP3 → WP4 → SHELL). 각 WP 는 **BE → FE**(BE 가 계약을 고정해야 FE 가 붙는다).

| Phase | 워커 | 무엇 | SPEC | 시작 조건 | 병렬 |
|---|---|---|---|---|---|
| **WP1-BE** 운영 버그(서버) | backend | 005 안건 출처(안건별) · 006 기한 규칙 · 014 받기 `download=1` → `attachment` · 018 원격 SVG · 010 `integration.changed` · 002 수정 참석자 합치기 | S10 §4.2 · §4.8 · §4.3(참석자) / S8 §4.4 · §2.2 | SPEC 검수 PASS | WP1-FE 의 「FE 만」 부분과 나란히 |
| **WP1-FE** 운영 버그(화면) | frontend | 002/004 일정 칸 · 참석자 중복 · 005 불러오기 시간·안건 출처 보내기·문구 · 014 받기 링크 · 010 설정 화면(이미 구독 — 확인만) | S10 §2.1 · §2.3 / S8 §2.2 | **002/004 는 즉시**(FE 만) · 005·014 는 WP1-BE 계약 고정 뒤 | WP1-BE 와 파일 안 겹침 |
| **WP2-BE** 회의록 고도화 | backend | 단계별 timeout env · timeout 재시도 = 새 세션 1회 · **AI 맥락 목록 조립 함수**(WP3 도 씀) · 재전사 전체 발화 매번 · 정정 pass + 보정 표(스키마·파서·저장·응답) · 안건 순서 | S10 §4.5~4.7 | WP1-BE 머지 | WP1-FE 와 나란히 가능 |
| **WP2-FE** 회의록 화면 | frontend | 회의록 끝 「용어 보정」 표 · 안건 순서는 서버가 정함(확인) | S10 §2.5 | WP2-BE 계약 고정 | — |
| **WP3-BE** AX 흐름(서버) | backend | 017 AX 대화에 맥락 목록 · 001 회의 생성 카드 계약(초안 저장·거절·근거 자료·탐색 지시) · 003/016 회의실 API(`people`·`meeting_id`·503) · PATCH `room` · Connect 방 변경·새 예약 · AX 수정 카드 `room` | S10 §4.1 · §4.3 · §4.4 · §4.5 | WP2-BE(맥락 목록 함수) | — |
| **WP3-FE** AX 흐름(화면) | frontend | 회의실 셀렉트 부품(네 자리) · 수정 모달 장소 칸 → 셀렉트 · AX 회의 생성 카드를 `AxDraftCard` 틀로 · AX 수정 카드 회의실 | S10 §2.2 · §2.4 | WP3-BE 계약 고정 | WP2-FE 와 나란히 |
| **WP4-BE** 메시지함→AX(서버) | backend | 참고 자료 `inbox_message`(나열 지점 전부) · 맥락 조합 함수 · 업무 출처 메시지 · `made_task_count` · 012 나간 방 이벤트 | S8 §4.8 · §5 동기화 | WP3-BE(맥락 목록이 AX 대화에 실려 있어야) | — |
| **WP4-FE** 메시지함→AX(화면) | frontend | 호버 막대 · 「스레드에 답글」 0개 · 메일 머리 단추 · 서랍 열며 참고 자료 보내기 · 말풍선 아래 참고 자료 한 줄 · 출처 링크 · 「업무 만듦」 | S8 §2.8 · §2.9 | WP4-BE 계약 고정 | WP3-FE 와 `App.tsx` 겹침 — 직렬 |
| **SHELL** 셸 · dmg | frontend(셸) | 011 하위 프레임 `about:*` 허용 · dmg 빌드·서명·공증 · 013 ②③ 사용자 GUI 확인 | S8 §5 데스크톱 경계 | WP1~4 1루프 뒤(dmg 한 번) | — |
| **반영** | 코디 | 1루프 E2E(앱) → 2루프 발주 → 운영 반영 | — | 전 Phase | — |

**같은 파일을 여는 워커를 동시에 태우지 않는다.** BE 는 한 워커가 WP 순서대로 간다(`http_inbox.py`·`bootstrap/application.py`·`codex_cli.py` 를 여러 WP 가 연다).
FE 는 `App.tsx`(WP4-FE · WP3-FE 의 AX 카드 진입) · `MessageList.tsx`(WP3-FE) · `labels.ts`(전 WP) 가 겹친다 — 코디가 조각 순서를 잡는다.

---

## Code Surface — 전수 grep 개수표

조사 리포트 줄을 출발점으로 코디가 `rg` 로 다시 셌다(2026-10-07 · `f0ad522` · `node_modules`·lock 제외). **prod** = 제품 코드, **test** = 시험 파일.
워커는 시작할 때 **같은 패턴으로 다시 센다** — 수가 다르면 코디에게.

### WP1 — 운영 버그

| 무엇 | 패턴(rg) | prod | test | 바뀌는 자리 / 건드리지 않는 자리 |
|---|---|---|---|---|
| 002/004 일정 칸 | `meeting-when\|date-field` | 17줄 / 7파일 | 3줄 / 2파일 | **바뀜**: `styles/meetings.css:148-150`(날짜 `width:200px` 고정) · 쓰는 곳 `MeetingEditModal.tsx:175` · `BookingModal.tsx:362`(같은 클래스 — 생성 모달도 넘치지 않게 확인). **건드리지 않음**: `.date-field` 의 다른 쓰임 — `ds/DateField.tsx:55` · `components.css:584` · `task-detail.css:142-189` · `ax.css:413-422` · `meetings.css:99` |
| 002 참석자 중복 | `PersonSearch\|PickedTags` | 12줄 / 5파일 | 0 | 쓰는 곳 넷: `MeetingEditModal.tsx:219-238` · `BookingModal.tsx:458-498`(+`OrgDirectory`) · `ShareModal.tsx:97-119` · `MeetingDetailPage.tsx:55`(import). 검색은 이미 `excluded` 로 거른다(`PeoplePicker.tsx:14-45`) — **onPick 이 append 만 한다**(`MeetingEditModal.tsx:229`) · 서버: 생성 `commands.py:153-154` 는 합침 / **수정 `MeetingInfoPatch`(`commands.py:163-196`)는 안 합침** → 합친다 |
| 005 ① 시간 | `setFrom\(\|setTo\(\|setDate\(` in `BookingModal.tsx` | 8줄 | — | **바뀜**: `applySuggestion` `:206-208` 셋만. **건드리지 않음**: `:377-378`(시간 고르개) · `:387-389`([지금]) |
| 005 ② 이어온 회의 | `carried_from_meeting_id` | 25줄 / 9파일 | 11줄 / 9파일 | 출처 판정은 `mtg/application.py:415` **한 곳**. 나머지(상세 응답 `:1805` · 합성 `:791-803` · 웜스타트 `:1408-1421` · 다음 회의 `platform/meetings.py:786-794` · 승인 편집기 `actions.py:2093`)는 **출처와 무관 — 바꾸지 않는다**(단 `platform/meetings.py:790` 은 006 기한에서 바뀐다) |
| 005 ② 안건 출처 값 | `"carried"\|source="carried"\|carried if\|AGENDA_SOURCES` | 8줄 / 5파일 | 3줄 / 2파일 | 서버 `mtg/application.py:415` · `domain.py:140,199-200` / 화면 `BookingModal.tsx:42,225`(화면용 출처 — 이제 **보낸다**) · `MeetingDetailPage.tsx:1399`([다음 회의 예약] 입구) · `viewModels.ts:1235` |
| 005 ② **`manual` 을 정하는 자리**(F-4) | `source="manual"\|"manual"` 을 안건에 다는 곳 | 넷 더 | — | `mtg/application.py:467`(빠른 시작 자리표시 안건) · `:564`(메모 폴백 「기존 회의록」) · `:1225`(회의 중 사람 벌 안건 추가) · `BookingModal.tsx:443`(손으로 더한 안건). **값은 그대로 `manual`** 이고, `labels.ts:750` 문구 변경(「새로 추가된 안건」)이 **이 넷 모두에 붙는다**(코디 판정 · S10 §2.3 · E2E 확인 H-4) |
| 005 ② 안건 입력 모델 | `MeetingAgendaDraftInput\|agendas\.map\(` | 13줄 / 7파일 | 0 | **입력 모델 하나를 세 입구가 쓴다** — 생성 `commands.py:127,143` · **회의 중 안건 추가** `mcp.py:905,1779` · `http.py:87` · `bootstrap/application.py:3889`. → **생성 전용 안건 입력 모델을 따로 둔다**(안건별 `source` · 코디 판정 W-r2-5) — 추가 입구 셋(`mcp.py:905,1779` · `http.py:87` · `bootstrap/application.py:3889`)은 옛 모델(`title` 만) 그대로 · 화면 `BookingModal.tsx:251`(제목만 보냄) · `api.ts:1228` |
| 005 ② 문구 | `meetingAgendaSourceText\|직접 입력\|지난 회의에서 넘어옴` | 7줄 / 3파일 | 1줄 / 1파일 | `labels.ts:750`(「직접 입력」 → 「새로 추가된 안건」) · 쓰는 곳 `MeetingDetailPage.tsx:1210` · `BookingModal.tsx:425` |
| 006 기한 | `next_meeting_after\|next_meeting_starts_on\|next_meeting_on\|resolve_due` | 15줄 / 4파일 | (`test_meeting_domain.py`) | `platform/meetings.py:786-803`(규칙) · `finalize.py:203-212`(하한) · `mtg/application.py:790,816-818,835`(날짜 변환 `_aware(...).date()` — KST 아님) · `finalize.py:371`(프롬프트 `next_day`) · `finalize_service.py:261` · 스키마 설명 `schemas/ai_final_output.json:129-130` · 프롬프트 `finalize.py:327` |
| 006 기한 — 날짜 후보 전부 | `due_candidate` | 26줄 / 9파일 | — | 하한은 **최종 결과에 적용**(`finalize.py:263`) — 배치 잠정 후보(`batch.py:90,136` · `ai_batch_output.json`)에도 같은 하한(OQ-1014 닫힘 · S10 §4.8) · 승격 `bootstrap/application.py:2015,3867` 은 그대로 |
| 006 KST 상수 | `OFFICE_TIMEZONE =` | 3줄 / 3파일 | — | 정의 셋: `modules/meetings/rooms.py:24` · `modules/meetings/export.py:34` · **`modules/time_blocks.py:34`**. 고칠 파일 `mtg/application.py:59` 는 **이미 `rooms.OFFICE_TIMEZONE` 을 import** 한다 — 그것을 쓴다(새 상수를 만들지 않는다) |
| 014 받기 링크 | `download[={ ]\|target="_blank"\|\.download ?=` | 14줄 / 8파일 | 2줄 / 1파일 | **다운로드 입구 18곳(FE §1-4) 중 바뀌는 것 넷**: `InboxAttachments.tsx:40`(`DownloadLink` — 쓰임 `:60` `FileCard` · `:146`) · `:80-91`(`downloadAll`) · `MailView.tsx:401` · **`InboxAttachments.tsx:162`(`Thumb` 원본 보기 — 앱이면 받기 주소·같은 탭, 웹이면 지금처럼 새 탭 · OQ-812 닫힘)**. **앱/웹을 가르는 자리**: `lib/shell.ts:70` `hasShell()`(이미 `:104,155,169,186,236,260` 이 같은 판별을 쓴다 · `dev/probeShell.ts:37` 은 탐침 전용 — 쓰지 않는다). **바꾸지 않음**: `:286`(unfurl) · `RoomView.tsx:165,664`(외부 열기) · `KakaoSection.tsx:215` · `WorkModals.tsx:1936,4306,4334` · `MessageList.tsx:782` · `AssistantMarkdown.tsx:199` · `dev/ProbePage.tsx:424` |
| 014 받기 주소 | `inboxMailAttachmentUrl\|inboxRoomAttachmentUrl` | `api.ts:1668-1679` + 쓰임 `MailView.tsx:391,413` · `RoomView.tsx:538-539` | 22줄 / 21파일(주소 문자열 포함) | 받기용 주소(`download=1`)를 만드는 함수를 더한다 — 미리보기(`:539` thumb)는 그대로 |
| 014 **주소 하나를 받기·원본 보기·미리보기가 같이 쓰는 자리**(F-3) | `Linked\|hrefOf\|href=\{file.href\}` | — | — | **방 첨부**: 주소를 만드는 곳은 `RoomView.tsx:538` `hrefOf` **하나** → 항목 모양 `InboxAttachments.tsx:94-95`(`type Linked` — 「원본(누르기·받기)」 주석, `href` 하나) → 받기 `:60` · `:105` · `:118` · `:146` · `:265` / **원본 보기 `Thumb` `:177` · `:194`**(`href={file.href}`). **메일 이미지**: `MailView.tsx:391` 의 `href` 하나가 썸네일 `src`(`:394`)와 받기(`:401`)에 같이 쓰인다. → **`Linked` 에 받기 주소(`downloadHref`)를 따로 두고** `hrefOf` 옆에 받기 주소 함수를 둔다 · 메일도 `src`(미리보기)와 받기 주소를 가른다. `hrefOf` 만 바꾸면 **웹 원본 보기까지 내려받기로 바뀐다** · **더 볼 자리(r2 재계수)**: ① `Linked` 를 **조립하는 곳** = `InboxAttachments.tsx:240-251`(`AttachmentList` 가 `hrefOf` 를 받아 `href` 를 채운다 — **`downloadHref` 를 여기서 채운다**) ② `hrefOf` 를 내려 주는 **prop 길** = `RoomView.tsx:297,307,341,436,447,488,495,706,742`(정의 `:538` 포함 10) — **받기 주소 함수를 같은 길로 같이 내린다** ③ 메일 썸네일 `MailView.tsx:394` 의 `Thumb` 은 `src` 만 받는다 — 앱에서 원본 보기를 받기로 하려면 **받기 주소를 `Thumb` 에 넘기는 자리**를 더한다(S8 §2.2) |
| 014 서버 disposition | `_download\(\|INLINE_IMAGE_TYPES\|inline_media_type\|Content-Disposition` in `entrypoints` | 18줄 / 2파일 | 4파일 | `http_inbox.py:121-134`(`_download`) — 쓰는 곳 **셋**: `:226`(메일 첨부) · `:240`(방 첨부) · `:251`(원격 이미지). `download=1` 은 앞 둘에만. `http.py` 의 회의 자료·업무 첨부 disposition(`:1098,1302-1308,1734,1822,2192,2568,2590`)은 **바꾸지 않는다** |
| 018 원격 SVG | `SVG\|svg\|이미지가 아닙니다\|sniff_raster` | 10줄 / 2파일 | 3파일 | `platform/external_inbox_upstream.py:51-63`(`sniff_raster` — SVG 판정 더함) · `:356-360`(거절) · docstring `:10` · `inbox_html.py:8-9`(옛 「기본 차단 · 이미지 보기」) · `http_inbox.py:80-84`(`RELAY_HEADERS` — 이미 샌드박스 CSP·nosniff) · ⚠ `_download` 는 SVG 를 `INLINE_IMAGE_TYPES` 밖이라 `attachment` 로 낸다 — `<img>` 는 그려도 원격 이미지 응답은 **`inline` + `image/svg+xml`** 로(구현 확인). **건드리지 않음**: `inbox_html.py:54`(인라인 `<svg>` 삭제) · `:73,205,217,257,263`(`data:` 래스터만) |
| 010 사건 | `INTEGRATION_CHANGED\|integration\.changed\|ARRIVAL_EVENTS_PER_SAVE\|def _announce` | 14줄 / 8파일(검수 재계수 12 — `def _announce` 가 `_announce_result`(`inbox.py:921`) 같은 무관 줄을 함께 잡는다 · **사건을 내는 곳은 여섯**: `inbox.py:1057` · `ext/application.py:336,652` · `kakao_ingest.py:323` · `sync_store.py:217`(`_announce`) · `:354`(`_changed` — 부르는 곳 `set_room_access :304` · `mark_disconnected :349` 등 6)) | 2파일 | 서버: `sync_store.py:33,204-220`(`_announce` — 20건 이하 실시간은 `message_arrived` 만) · `:247-263`(`update_integration` — 상태 바뀔 때만) · `:265-281`(`update_room`) · `:354` · `application.py:336,652` · `kakao_ingest.py:241-253,304-325` · `inbox.py:1057` · `events.py:36`. 화면(이미 구독): `SettingsPage.tsx:181-187` · `InboxPage.tsx:143` · `viewModels.ts:1650` |

### WP2 — 회의록 생성 고도화

| 무엇 | 패턴 | prod | test | 자리 |
|---|---|---|---|---|
| timeout 값 | `timeout_seconds\|TIMEOUT_SECONDS\|timeout=` in `codex_cli.py`·`claude_cli.py`·`cli_process.py` | **16줄 / 3파일**(codex 3 · claude 3 · cli_process 10 — 앞 판 「25 / 4」 는 잘못 셌다) + **`modules/ax_execution/ai.py:23` `AiProviderProfileRequest.timeout_seconds`**(요청마다 timeout 을 넘기는 자리 — 지금 아무도 채우지 않는다) | 7파일 | 박힌 값 둘: `codex_cli.py:95`(90) · `claude_cli.py:74`(180). 쓰는 곳 `codex_cli.py:141,222` · `claude_cli.py:108,179` · 러너 `cli_process.py:106-201`(그대로). **`bootstrap/application.py:1039,2344-2352,3578-3583,3652` 의 timeout 은 회의실·자료·영수증 것 — 건드리지 않는다** |
| provider 를 만드는 곳 | `CodexCliProfile\(\|ClaudeCliProviderAdapter\(\|create_conversation_provider\(\|meeting_batch_provider\(` | 13줄 / 3파일 | — | 공장 `bootstrap/application.py:4743-4772` · **호출 넷**: 최종 합성 `:517` · 배치·웜스타트 `:627` · 보고서 `:1003` · 대화 워커 `bootstrap/conversation_worker.py:61` (+ `meeting_batch_provider` `:2093-2100`). 단계 값이 이 넷까지 내려가야 한다 |
| 최종 재시도 | `FINAL_ATTEMPTS\|FinalizeSessionLost\|cold_start\|session_ref` | 27줄 / 3파일 | `test_meeting_finalize_service.py` | `finalize.py:29,46` · `finalize_service.py:81-264`(루프 `:156-171` · 콜드 전환 `:213-227` · 전사 싣기 `:241`) · 워커 `meeting_worker.py:19,25`(`MAX_DELIVERIES`) · timeout 분류 `codex_cli.py:226-227,242-245` · `claude_cli.py:184` |
| 재전사 전체 발화 매번 | — | — | — | `finalize_service.py:241`(`if cold_start else None` 을 걷는다) · docstring `finalize.py:367-368,384-386` |
| 맥락 목록이 들어갈 프롬프트 | `def build_\|_POLICY = \|Context references authorized` | 19줄 / 6파일 | — | 웜스타트 `batch.py:180-233` · 최종 `finalize.py:355-387` · 대화 `codex_cli.py:529-564` / `claude_cli.py:302-344`(WP3) · 재료 `mtg/application.py:774-836,1399-1438` · 도구 레지스트리 `settings.py:13,34,165,208`(그대로) |
| 정정·보정 표 | 스키마·파서·적재·응답 | — | — | `schemas/ai_final_output.json` · `finalize.py:76-163`(파서) · `:166-186`(`_bind_evidence`) · `:245-279` · 프롬프트 `:300-387` · 배치 스키마 `ai_batch_output.json`(보정 표 오면 버림) · 적재 `platform/meetings.py`(최종 벌 저장) · 응답 `mtg/application.py`(상세 뷰 `:1805` 주변 · `_agenda_view` `:1967`) · 화면 `MeetingDetailPage.tsx` · `viewModels.ts`. **내보내기 `export.py` 는 바꾸지 않는다**(OQ-1006) |
| 안건 순서 | `order_index` | — | — | 칸 `persistence.py:357-385`(`order_index`) · 읽기 `platform/meetings.py:392`(`order_by(order_index, created_at)`) · 최종 적재가 근거 시각으로 매긴다 |

### WP3 — AX 흐름

| 무엇 | 패턴 | prod | test | 자리 |
|---|---|---|---|---|
| 회의 생성 Action | `meeting\.reservation\.create` | 22줄 / 6파일 | 4줄 / 3파일 | `action_center.py:788,853` · `confirmation.py:34,39,161` · `mcp.py:223,826,832` · `policy.py:24` · `actions.py:134,302,639,716,1036,1188,1215,1309,1703` · `bootstrap/application.py:3700,3973,4042,4318` |
| 초안 저장·카드 판별 | `DRAFT_SAVE_ACTION_TYPES\|AX_DRAFT_KINDS\|axDraftFromAction\|ActionMeetingCard\|_meeting_edit_contract` | 18줄 / 6파일 | 14줄 / 2파일 | 서버 `policy.py:35,135` · `actions.py:23,536,1704,1857,2064-2103` · `action_center.py:47,580` / 화면 `AxDraftCard.tsx:35-64` · `MessageList.tsx:6-7,295-333` · `ActionMeetingCard.tsx:101~`. **`meeting.info.update` 에는 편집기가 없다**(검수 F-2 확인) — `confirmation.py:29-36` `SUPPORTED_ACTION_TYPES` 에 없어 `actions.py:1678-1679` 가 편집 계약 `None` → 화면 `MessageList.tsx:295-333` 의 어느 갈래에도 안 걸려 **`ActionResultCard`(`:333` · 정의 `:641`)** 로 그린다. 회의 생성은 `AxDraftCard` 틀로 옮기고, **수정 카드는 편집 계약·편집 카드를 새로 만든다**(S10 §2.4 · §4.3) |
| 회의 생성 정책·도구 | `MEETING_CREATION_POLICY` | `codex_cli.py:425-441` · Claude 는 import `claude_cli.py:303` | — | 업무 생성 탐색 지시(`codex_cli.py:404-406,464-469`)와 같은 자료 탐색 지시를 더한다 · 회의 입력 `commands.py:132-160`(`extra=forbid`) |
| 회의실 | `readMeetingRooms\|meetings/rooms\|meeting_room_list\|choose_replacement\|RoomUnavailable\|RoomBookingRefused\|available_rooms` | 34줄 / 9파일 | 26줄 / 8파일 | API `http.py:931-948` · 실패 삼킴 `bootstrap/application.py:1043-1065` · 어댑터 `the_connect.py:82-104,118-121,128-137,170` · 경계 `rooms.py:52-65,209-228,309-332` · 예약 `bootstrap/application.py:1067-1130,1174-1189,1191-1318` · 오류 매핑 `http.py:548-557` · AX 도구 `mcp.py:1706` · `tool_catalog.py:412` / 화면 `api.ts:1468-1471` · `BookingModal.tsx:36-39,124-160,506-525` · 문구 `labels.ts:860,872~` |
| 회의 수정·동기화 | `meeting\.info\.update\|MeetingInfoPatch\|_sync_room_reservation\|gateway\.update\(\|def update\(` | 26줄 / 8파일 | — | `commands.py:163-196` · `rooms.py:224` · `the_connect.py:128` · `bootstrap/application.py:1340-1424,1737-1753,3545,3672,3734-3787` · `http.py:89,965-975` · `mcp.py:92,183,840-847,1744` · `actions.py:136,1181`. 화면 `MeetingEditModal.tsx:119-125,200-212` · `api.ts:1244-1256`(⚠ `ActionMeetingCard.tsx:417-427` 은 **생성 카드의 장소 입력란**이다 — 수정 카드 자리가 아니다). **`modules/work/application.py:529` 의 `update` 는 무관** |
| **AX 수정 카드 편집 계약이 들어갈 자리**(F-2) | `SUPPORTED_ACTION_TYPES\|def _edit_contract\|ActionResultCard\|'meeting.update'` | — | — | `modules/actions/confirmation.py:29-36`(더한다) · `platform/actions.py:1678-1679`(`None` 을 내는 자리) · `:1690-1706`(`_edit_contract` 갈래 — 회의 수정 계약을 세운다) · 화면 `MessageList.tsx:295-333`(갈래 더함) · `:641`(`ActionResultCard` — 이 종류는 더는 여기로 안 간다). **옛 `meeting.update`**: 계약 `modules/ax_execution/command_contracts.py:107`(`editor: "command"`) · 확정 실행 `bootstrap/application.py:3745-3765`(`:3760` 같은 방 PUT) → **새 수정 검증 경로(재확인·409·참석자 합치기)로 합친다**(코디 기본값) |
| 017 대화 프롬프트 | `Context references authorized\|WORK_AND_REPORT_ROUTING_POLICY` | `codex_cli.py:454-485,529-564` · `claude_cli.py:305,339-344` | — | 맥락 목록 덩어리를 대화 프롬프트에 — **매 턴**(OQ-1002 닫힘) |

### WP4 — 메시지함 → AX

| 무엇 | 패턴 | prod | test | 자리 |
|---|---|---|---|---|
| 참고 자료 종류 **나열 지점** | `'task', 'work_request'\|"task" \| "work_request"\|unsupported context resource type\|ConversationContextReference` | 35줄 / 12파일(회의 후속 `kind` 등 무관 포함) | 30여 파일(대부분 `resource_type` 이 다른 뜻) | **바꿔야 하는 다섯**(BE §8-pre-1): `conversation_commands.py:20` · `platform/conversations.py:1002-1006`(해석기 — `_task`·`_work_request` 옆에 `_inbox_message`) · `http.py:433-434`(요청 모델 — 정의만, 사용처 없음) · `viewModels.ts:1030-1031` · `tool_catalog.py:54`(설명 문구). **함께 보는 곳**: `conversations.py:41,54,174` · `platform/conversations.py:27,305,993-1052` · `bootstrap/application.py:66,4246` · `useConversations.ts:13,28,83,305,319,384` · `api.ts:44,744-756` · 저장 `persistence.py:735-746`(CHECK 없음). **무관**: `meetings/commands.py:116` · `followups.py` · `notifications.py:77` · `browser_interactions.py:104,121` |
| 프롬프트에 싣는 자리 | `Context references authorized` | `codex_cli.py:558-563` · `claude_cli.py:339-344` | — | 지금 한 줄 요약(`- {type}:{id}: {summary}`) — 메시지 맥락 JSON 은 **덩어리**로 싣는다 |
| 서랍 열며 보내기 | `askAx\|isAxOpen\|sendCurrent\(\|onAskAx` | 14줄 / 2파일 | 7줄 / 2파일 | `App.tsx:186,210,307-317,481,609-650` · `TodayPage.tsx:50,71,290`. 메시지함(`InboxPage`)은 아직 받지 않는다 · 지금 맥락 `[]`(`App.tsx:310,317`) · 말풍선 칩을 그리는 코드 0(FE §6-4) |
| 메시지 행·스레드 | `scax-imsg\|ThreadLine\|onOpenThread\|scax-mail__actions` | 77줄 / 5파일 | 1줄 / 1파일 | 행 `RoomView.tsx:294-357`(`Message`) · 스레드 줄 `:275-290` · `toLine` `:67-126`(답글 0개면 `thread` null — `:87,100-107`) · 패널 `:459,490,499,526,628,709,740` · CSS `inbox.css:133-163,208-212,255`(**`.scax-imsg:hover` 0**) · 메일 머리 `MailView.tsx:358-364` · `inbox.css:217` |
| 메시지 응답 | 방 메시지 뷰 · 메일 뷰 | `inbox.py:606-646`(`messages[]` — `id` 있음) · `:556-580`(메일) | — | `made_task_count` 를 더한다 · 기준 위아래 조회는 저장소 `external_channels_inbox_store.py:210-224` 옆에 **내부 함수**로(공개 API 아님) · 인덱스 `ix_external_messages_room_sent_at` · `_room_thread` 있음 |
| 업무 출처 | `origin\.source\|source\.type\|metaOrigin` / `"action_item"\|source_action_item_id` | 15줄 / 5파일 / 23줄 / 6파일 | — | 서버 출처 조립 `modules/work/application.py:2481-2523` · 업무 생성 경로 `application.py:116,271,307` · `requests.py:125,356,464` · `assignments.py:119,146` · `creation_commands.py:98` · 확정 `actions.py:838-848` · `action_center.py:813-870` / 화면 `WorkModals.tsx:390,2142-2170,2270` · `MyWorkPage.tsx:704-729` · `workRows.ts:208` · **`inbox.message_updated` 를 내는 자리 = 업무 확정 커밋 뒤**(W-r2-7) — 확정 경로 `actions.py:838-848`(실행 분기 · `create_task`) · `action_center.py:813-870`(`_confirm`)에서 원래 메시지가 남은 업무·요청이 **커밋된 뒤** 사건을 낸다(커밋 전에 내면 화면이 다시 읽어도 수가 안 바뀐다) · 사건 타입 `modules/external_channels/events.py:30-36` |
| 012 나간 방 | `_verified_this_run\|handle_slack_event\|tokens_revoked\|slack_fanout_targets\|set_room_access\|member_left\|channel_left\|group_left` | 17줄 / 2파일 | **0**(나간 방 시험 없음) | `sync.py:140,147,221,227-276,314-319,332,439-459` · `sync_store.py:116-127,283-305` · 봉투 `external_slack.py:388-396`. **나간 방 이벤트 처리 0** · 앱 이벤트 구독 정의는 레포에 없다 |

### SHELL

| 무엇 | 패턴 | prod | 자리 |
|---|---|---|---|
| 이동 허용 | `on_navigation\|nav_allow\|about:\|is_api_request` | 17줄 / 3파일 | `lib.rs:435-463`(허용 목록 · `origin_of` 가 `about:*` → `"null"` 로 취소) · `guard.rs:125-135,250` · 시험 `lib.rs:992-998` · `download.rs:54-61,597,611` |

### 운영 인벤토리

- `docs/unified-operations-inventory.json`(HTTP 216건) — **HTTP·MCP 시그니처를 바꾸면** `tests/architecture/test_operation_inventory.py` 가 drift 를 잡는다(코드 `AGENTS.md`). 바뀌는 것: `GET /api/meetings/rooms`(인자) · `PATCH /api/meetings/{id}`(`room`) · `POST /api/meetings`(안건 `source`) · 대화 메시지(참고 자료 종류) · MCP `meeting_room_list` · `meeting_update` · `meeting_create`. **diff 난 항목만 패치**(전체 재작성 금지)

---

## Phase WP1-BE — 운영 버그(서버)

- **Status**: TODO · **워커**: backend · **SPEC**: S10 §4.2 · §4.3(참석자 합치기) · §4.8 / S8 §2.2 · §4.4
- **시작 조건**: SPEC-008 v0.6.0 · SPEC-010 v0.1.0 검수 PASS · 사용자 리뷰
- **계약**
  - [ ] **005 안건 출처**: **생성 전용 안건 입력 모델**(`{title, source?}`)을 새로 두고 생성 입력이 그것을 쓴다 — **안건마다** 저장(없으면 `manual`) · `carried` + 이어온 회의 없음 = `422` · 회의 중 안건 추가 입구는 옛 모델(`title` 만) 그대로라 `carried` 가 들어올 길이 없다 · AX `meeting_create` 도구 입력도 같은 모양
  - [ ] **002 수정 참석자 합치기**: `MeetingInfoPatch` 의 `attendee_ids`·`external_attendees` 를 생성과 같이 순서 유지 중복 제거
  - [ ] **006 기한**(S10 §4.8): 「다음 회의」 = 이월 회의만·취소 제외·뒤에 시작 · 모든 날짜 KST(`OFFICE_TIMEZONE`) · **회의일보다 이른 기한은 비운다**(① 말의 날짜 포함) · 프롬프트·스키마 설명 동기화
  - [ ] **014 받기**: 메일·방 첨부 라우트가 **`?download=1` 이면 언제나 `attachment`** · 없으면 지금 규칙
  - [ ] **018 원격 SVG**: 바이트 SVG 판정 → `image/svg+xml` + 지금 머리(샌드박스 CSP·nosniff·CORP) · HTML 은 거절 유지 · docstring 셋 정정
  - [ ] **010 사건**: 적재 건수·마지막 수집·백필 진행(커서 포함)이 바뀌는 저장마다 `integration.changed` · 같은 연동 사건 묶어 내기(1초에 한 번 — OQ-818 코디 기본값)
  - [ ] **018 응답 disposition**: 원격 이미지 경로(`http_inbox.py:251`)는 래스터·SVG 모두 `inline` — `_download` 의 「허용 목록 밖은 `attachment`」 를 이 경로에 쓰지 않는다
- **완료 조건(실물)**: 운영 로그의 GitHub camo SVG 400 이 로컬 재현에서 200 으로(같은 주소 1회) · 로컬 Gmail 첨부를 `download=1` 로 받으면 `attachment` · 10-07 사례와 같은 모양(같은 owner 같은 날 오후 다른 예약) 회의 합성에서 기한이 회의일보다 이르지 않음
- **시험**: `make test-unit` · `make test-contract` · `make test-postgres`(사건 · `test_external_channels_postgres.py`) · 운영 인벤토리 drift · 마지막에 `make verify`
  - 새 시험: 안건 출처(불러오기·[다음 회의 예약]·`carried` 422·안건 추가 입구 거절) · 수정 참석자 중복 · 기한 경로 (a)(b)(c)(d) 각각(BE §5.5) · `download=1` × 이미지/PDF/기타 · SVG 받음/HTML 거절/인라인 svg 여전히 삭제 · 실시간 1건 저장에 `integration.changed`

## Phase WP1-FE — 운영 버그(화면)

- **Status**: TODO · **워커**: frontend · **SPEC**: S10 §2.1 · §2.3 / S8 §2.2
- **시작 조건**: **002/004 는 바로 — SPEC 검수 무관(CSS·화면만, 계약 변경 없음)** · 그 밖(005·014)은 SPEC 검수 PASS + WP1-BE 계약 고정 뒤
- **계약**
  - [ ] **002/004**: 수정 모달 날짜 칸 폭을 줄여 세 칸이 왼쪽 열 안에 — 생성 모달(같은 클래스)도 넘치지 않음 · 종료 시각 칸이 검색 입력 밑에 깔리지 않음
  - [ ] **002 중복**: 수정 모달 `onPick` 이 이미 있는 사람을 다시 넣지 않는다(검색 `excluded` 는 이미 있음) · 생성·공유 모달도 같은지 확인
  - [ ] **005**: `applySuggestion` 이 날짜·시작·종료를 건드리지 않음 · 제출이 안건마다 `source` 를 보낸다 · [다음 회의 예약] 입구도 · `manual` 문구 = 「새로 추가된 안건」
  - [ ] **014**: 받기 셋(`DownloadLink` · `downloadAll` · 메일 이미지 받기)에서 `download`·`target="_blank"` 를 빼고 `download=1` 주소 · **받기 주소와 원본 보기·미리보기 주소를 가른다**(`Linked` 에 받기 주소 — 조립 `InboxAttachments.tsx:240-251` · `RoomView.tsx` prop 길로 받기 주소 함수 · 메일은 `src` 와 받기 주소 따로, `MailView.tsx:394` `Thumb` 에 받기 주소 — Code Surface F-3) · **이미지 원본 보기(`Thumb`)는 `hasShell()` 이 참(앱)이면 받기 주소·같은 탭, 거짓(웹)이면 지금처럼 새 탭**(OQ-812 닫힘) · 화면 모양 그대로 · 미리보기는 그대로
  - [ ] **010**: 설정 화면은 이미 `integration.changed` 에 다시 읽는다 — 서버 변경 뒤 **새로고침 없이 숫자가 느는지만 확인**(코드 변경 없을 수 있음)
- **완료 조건(실물 · 앱)**: 앱에서 수정 모달 일정 한 줄 · 불러오기 시간 유지 · 출처 문구 둘 · **메일·슬랙·카톡 첨부 받기가 다운로드 폴더에 저장되고 토스트**(SH-007·014 함께 닫힘) · **앱에서 썸네일을 누르면 저장 + 토스트, 웹에서는 새 탭 원본**
- **시험**: `make frontend-test` · `make frontend-build` — 새 시험: 모달 일정 칸 클래스·폭 · 중복 담기 · 불러오기가 시간 유지 · 안건 `source` 전송 · 받기 링크에 `download`/`_blank` 없음 + `download=1` · 원본 보기가 `hasShell()` 에 따라 갈림(셸 전역 대역) · 웹 원본 보기는 내려받기가 아님

## Phase WP2-BE — 회의록 생성 고도화

- **Status**: TODO · **워커**: backend · **SPEC**: S10 §4.5 · §4.6 · §4.7
- **시작 조건**: WP1-BE 머지(같은 `finalize.py`·`mtg/application.py` 를 연다)
- **계약**
  - [ ] **timeout env 넷**(`AX_AI_TIMEOUT_BATCH_SECONDS` 240 · `…_WARMSTART_SECONDS` 240 · `…_FINAL_SECONDS` 900 · `…_CONVERSATION_SECONDS` 180) — `Settings.from_environment()` · Codex·Claude 같은 값 · 숫자 아님·0·음수면 시작 오류(S10 OQ-1015)
  - [ ] **단계 값을 내려보내는 길 = 단계별 프로필**: provider 공장(`create_conversation_provider` · `bootstrap/application.py:4743-4772`)이 **단계 timeout 을 인자로 받아 그 단계의 프로필(Codex `CodexCliProfile(timeout_seconds=…)` · Claude 같은 결)을 만든다** — 호출 넷(최종 `:517` · 배치/웜스타트 `:627` · 보고서 `:1003` · 대화 워커 `conversation_worker.py:61`)이 자기 단계 값을 넘긴다. 배치와 웜스타트가 `:627` 한 자리를 같이 쓰므로 그 자리에서 둘을 가른다. **요청 필드 `ai.py:23 AiProviderProfileRequest.timeout_seconds` 는 쓰지 않는다**(지금 채우는 곳이 없고 어댑터가 읽지 않는다 — 두 길을 섞지 않는다)
  - [ ] **timeout 재시도 = 새 세션 1회 — 배치·웜스타트·최종 모두**(S10 §4.6) · **배치는 회의마다 한 줄**(겹쳐 돌지 않음) · 재시도 중 도착분은 다음 배치에 합침 · 새 세션 참조는 재시도 성공 때 교체: 최종은 timeout 이면 같은 세션 resume 대신 새 세션 1회(전사 전량·맥락 목록) · 배치·웜스타트는 새 세션 1회(웜스타트 맥락 + 맥락 목록 + 그 배치 미처리 구간) 뒤 실패면 지금처럼 다음 배치에 합침 · 그 밖 실패는 지금 규칙 · 워커 재배달 수와 맞춘다(`MAX_DELIVERIES`)
  - [ ] **AI 맥락 목록 조립 함수 하나**(S10 §4.5) — 프로젝트 전부 · 완료·취소 안 된 업무 · 구성원 전부 · 호출 때 DB 조회 · **WP3 가 대화에 쓴다**. 범위 = **조직 전체**(D-13 정본 — S10 OQ-1002 ① 정정) · 상한 없음(코디 기본값 · 크기 관측 — I-6) · **세션을 새로 열 때마다 다시 싣는다**(웜스타트·새 세션 재시도·세션 유실)
  - [ ] 웜스타트·최종 프롬프트에 맥락 목록 · **최종에 재전사 전체 발화 매번**
  - [ ] **정정 pass + 보정 표**: 최종 프롬프트 두 단계 · 출력 스키마에 `term_corrections[{heard, corrected, grade}]` · 파서·검증(형식 오류 항목만 버림) · 저장(보정 표 행 + `term_corrected_at` 같은 트랜잭션) · 회의 상세 응답(`null`/`[]`/행 — S10 §4.7-4) · 배치 출력에 오면 버림 · 원문(스크립트)은 안 바꿈
  - [ ] **안건 순서**: 최종 적재가 가장 이른 근거 시각으로 `order_index` 를 매긴다
- **완료 조건(실물)**: 10-07 주간 회의 원문으로 **재합성 1회**(로컬 DB 사본 · 실명 가림) — 900초 안에 끝남 · 「캐스티」 류가 표에 · 안건이 시간 순 / 30분+ 회의 실물 1회가 90초를 넘겨도 「종료」
- **시험**: `make test-unit`(`test_meeting_finalize_service.py` · 새 파서·순서·하한) · `make test-contract` · **`make test-postgres`**(보정 표 새 표) · 프롬프트 스냅숏(맥락 목록·전체 발화 포함) · timeout 분류(같은 세션 3회 resume 이 안 남) · **배치 재시도 시험 1건**: 배치 timeout → 새 세션 1회 → 그 사이 도착한 발화는 다음 배치로(겹쳐 돌지 않음) · 새 세션 참조는 성공 때만 교체 · 실패면 구간이 다음 배치에 합쳐짐 · `null`/`[]` 응답 구분(`term_corrected_at`)

## Phase WP2-FE — 회의록 화면

- **Status**: TODO · **워커**: frontend · **SPEC**: S10 §2.5
- **시작 조건**: WP2-BE 계약 고정
- **계약**
  - [ ] 최종 회의록 끝 「용어 보정」 표(들린 말 · 바로잡은 말 · 처리 「바꿈」/「표에만」) · 읽기 전용 · **`[]` 이면 「바로잡은 용어 없음」 한 줄, `null` 이면 자리 없음**(H-3)
  - [ ] 안건 순서는 서버가 준 대로(화면이 다시 정렬하지 않음)
- **완료 조건(실물 · 앱)**: 재합성한 회의를 앱에서 열어 표가 끝에 · 「참석 N명」·화자 라벨 그대로
- **시험**: `make frontend-test` · `make frontend-build`

## Phase WP3-BE — AX 흐름(서버)

- **Status**: TODO · **워커**: backend · **SPEC**: S10 §4.1 · §4.3 · §4.4 · §4.5
- **시작 조건**: WP2-BE(맥락 목록 함수) 머지
- **계약**
  - [ ] **017**: AX 대화 프롬프트에 맥락 목록 — **매 턴**(S10 OQ-1002 ② 닫힘) · 업무 생성 정책의 탐색 지시를 「목록에서 먼저, 상세는 도구로」 로
  - [ ] **001**: `meeting.reservation.create` 를 초안 저장 종류에 · 거절 · 편집 계약(회의 고유 필드 + 안건 `source` + `room_id`) · 회의 생성 정책에 자료 탐색 지시 → 근거 자료가 카드에(업무와 같은 경로)
  - [ ] **003/016 목록**: `GET /api/meetings/rooms` 에 `people`·`meeting_id` · 정원 조건 · 자기 예약 점유 제외 · `current`·`unavailable_reason` · **Connect 실패 = `503 ROOM_SERVICE_UNAVAILABLE`**(미설정은 `[]`) · MCP `meeting_room_list` 같은 규칙
  - [ ] **003/016 수정**: `PATCH` 의 `room`(없음=유지·재확인 / `null`=예약 없음 / `n`=변경) · 새 예약은 `Idempotency-Key` + 이중 예약 울타리 재사용 · 방 변경 = Connect PUT `room_id` · 저장 직전 재확인 · `409 ROOM_BOOKING_REFUSED`(+`available_rooms`) · 저장 때 Connect 장애는 **지금 동작 유지 + 실패를 응답에 실어 문구**(OQ-1008)
  - [ ] **016 — AX 회의 수정 카드의 편집 계약을 새로 만든다**: `meeting.info.update` 를 `SUPPORTED_ACTION_TYPES` 에 · `_edit_contract` 갈래에 회의 수정 계약(회의명·목적·날짜·시작·종료·참석자·`room`) · 확정 실행이 위 수정 규칙을 탄다
  - [ ] **옛 `meeting.update`**(`command_contracts.py:107` · `bootstrap/application.py:3745-3765`)를 **같은 수정 검증 경로로 합친다** — 재확인·409·참석자 합치기를 비켜 가지 않는다
  - [ ] 생성의 Connect 실패는 **지금 동작 그대로**(회의는 서고 장소가 빔 — `labels.ts` `roomFailed`) — 바꾸지 않는다(OQ-1008)
- **완료 조건(실물 · Connect)**: 수정에서 **방 변경 1회**(Connect 화면에서 방·시간 바뀜 확인) · 예약 없던 회의에 방 추가 1회(중복 예약 없음) · 「예약 없음」 1회(취소) · Connect 끊은 상태에서 목록 503
- **시험**: `make test-contract`(`test_meeting_rooms.py` 확장 — 정원·자기 예약 제외·503·409·멱등) · `test_action_center.py`(회의 초안 저장·거절 · **회의 수정 편집 계약** · 옛 `meeting.update` 가 409 를 탐) · 인벤토리 drift · `make verify`

## Phase WP3-FE — AX 흐름(화면)

- **Status**: TODO · **워커**: frontend · **SPEC**: S10 §2.2 · §2.4
- **시작 조건**: WP3-BE 계약 고정
- **계약**
  - [ ] **회의실 셀렉트 부품 하나** — 생성 모달 · 수정 모달 · AX 생성 카드 · AX 수정 카드. 수정만 맨 위 기존 줄 · 구분선 · 「회의실 예약 없음」 · 가용 목록 · 비활성+이유 · 「가용 없음」/「조회 실패 — 다시 시도」 · 조건 바뀌면 다시 받기(300ms)
  - [ ] 수정 모달 장소 글자 칸 → 셀렉트(OQ-1005 닫힘) · 바뀐 값만 보내기(OQ-1010) · 기존 방 비활성일 때 [저장] 옆 이유 한 줄(H-2 · OQ-1016) · 조회 실패 중 저장 결과 줄(H-1)
  - [ ] **AX 회의 생성 카드를 `AxDraftCard` 틀로** — 쪽 나눔(OQ-1001 닫힘: 기본 정보 · 참석자 · 회의실·안건 · 자료) · AX 배지·회차 · 거절 · 수정(편집 창 → 초안 저장) · 등록 · 접힌 한 줄 「회의 열기」
  - [ ] **AX 회의 수정 카드를 새로 그린다** — 지금은 결과 카드(`ActionResultCard`)라 고칠 칸이 없다. `MessageList.tsx` 갈래에 회의 수정 편집 카드를 더한다(필드 + 회의실 셀렉트 수정 모양 · 장소 글자 칸 없음 · 초안 저장·회차 없음 — S10 §2.4)
  - [ ] 생성 모달 「회의실 선택 안 함」 → 「회의실 예약 없음」
- **완료 조건(실물 · 앱)**: 앱에서 S10 §3 S-2 · S-3 · S-6 · S-7
- **시험**: `make frontend-test`(`ActionMeetingCard.test.tsx` → 새 카드 · `MeetingEditModal.test.tsx` · 셀렉트 상태 넷) · `make frontend-build`

## Phase WP4-BE — 메시지함 → AX(서버)

- **Status**: TODO · **워커**: backend · **SPEC**: S8 §4.8 · §5 동기화
- **시작 조건**: WP3-BE 머지(대화 프롬프트에 맥락 목록)
- **계약**
  - [ ] **`inbox_message` 참고 자료** — **나열 지점 다섯 전부**(표) + 해석기(소유 404 · 소프트 딜리트 404 · 버전 1)
  - [ ] **맥락 조합 함수 하나**(입구와 분리 — 다음 단계 자동 추천이 부른다): 채널 위아래 100줄 · 스레드 답글 = 스레드 전체 · 메일 = 그 메일 · 줄 모양 + `target` · 원문 JSON 제외 · 멘션 이름 풀기 · 메일은 안전본 글자
  - [ ] 프롬프트에 맥락 JSON 을 덩어리로(지금 한 줄 요약 형식과 별도)
  - [ ] **업무 출처**: 그 턴의 참고 자료에 메시지가 있으면 확정된 업무·요청에 원래 메시지를 남김 · 업무 상세 `origin.message` · 방 메시지·메일 응답 `made_task_count`
  - [ ] **`inbox.message_updated` 사건**(S8 §4.4 · H-5): `made_task_count` 가 바뀌면 `{message_id, room_id|null}` — 사용자 사건 채널(`events.py` `UserEventType` 에 더함) · **내는 자리 = 업무 확정 커밋 뒤**(`actions.py:838-848` · `action_center.py:813-870`)
  - [ ] **012**: 나간 방 계열 이벤트 처리(S8 §5) — 그 회원의 방 / 보관·삭제는 고른 회원 전부 · 즉시 `paused` · 사건 · **운영 슬랙 앱 이벤트 구독 추가 목록**을 반영 단계에 넘긴다
- **완료 조건(실물)**: 슬랙 테스트 채널을 **실제로 나가** 그 회원 방이 `paused` · 실메시지 1건으로 맥락 JSON 조합(스레드 답글 1건 · 메일 1건)
- **시험**: `make test-unit` · **`make test-postgres`**(업무·요청의 원래 메시지 칸) · `make test-contract`(참고 자료 다섯 지점 · 남의 메시지 404 · 100줄 경계 · 스레드 · 메일 · 출처 · `made_task_count` · 나간 방 팬아웃 두 회원 대역) · 인벤토리 drift

## Phase WP4-FE — 메시지함 → AX(화면)

- **Status**: TODO · **워커**: frontend · **SPEC**: S8 §2.8 · §2.9
- **시작 조건**: WP4-BE 계약 고정 · WP3-FE 의 `App.tsx` 조각 머지
- **계약**
  - [ ] **호버 막대** — `Message` 한 곳 · 슬랙 셋 / 카톡 둘 · 아이콘만 + 툴팁 · 키보드 포커스 · 패널 안 답글(스레드 아이콘 없음 — OQ-813) · 로컬 줄 없음
  - [ ] **「스레드에 답글」** — 답글 0개도 패널 열기(입구만 더함 — 패널·조회·답장 경로엔 조건 없음)
  - [ ] **메일 머리** [AX 업무 생성][AX 요약][답장][전체 답장]
  - [ ] **서랍 열며 참고 자료 보내기** — `askAx` 를 메시지함이 받도록 넓히고 `context` 를 싣는다 · 말풍선 본문 넷(S8 §2.9 ③) · 말풍선 아래 참고 자료 한 줄
  - [ ] **출처 링크** — 업무 상세 출처 행에 「원래 메시지 · …」(「판단 보기」 와 함께) · 누르면 메시지함의 그 메시지로(스크롤·강조 — OQ-817) · **「업무 만듦」 표지** — `inbox.message_updated` 를 받아 그 방·메일을 다시 읽어 **새로고침 없이** 선다(`viewModels.ts:1650` 사건 타입 · `InboxPage.tsx` 구독)
  - [ ] 말풍선 아래 참고 자료 한 줄 = **실제 실은 범위**(시각 구간·건수 — OQ-816) · 단추마다 새 대화(OQ-815)
- **완료 조건(실물 · 앱)**: S8 §3 S-11 ~ S-14 를 앱에서 · 출처 링크 왕복
- **시험**: `make frontend-test`(막대 아이콘 수·툴팁 문구·패널 안·0개 스레드·서랍 context 전송·출처 링크·표지) · `make frontend-build`

## Phase SHELL — 셸 · dmg *(1루프의 마지막 · dmg 는 이 판에 한 번)*

- **Status**: TODO · **워커**: frontend(셸) · **SPEC**: S8 §5 데스크톱 경계(셸 계약 소유는 SPEC-006 — 다음 개정)
- **시작 조건**: WP1~4 1루프 구현 끝(웹 변경은 dmg 없이 앱에 반영되지만, dmg 는 한 번에)
- **계약**
  - [ ] **011**: 이동 허용에서 `about:blank`·`about:srcdoc` 를 허용(외부 origin 차단·`/api/` 가로채기 그대로) — ⚠ 프레임 구분이 없다(Open Issues I-1)
  - [ ] dmg 빌드·서명·공증(RUNBOOK-002 데스크톱 절)
  - [ ] **013 ②③ 사용자 GUI 확인 체크리스트**를 dmg 와 함께 전달: ☐ 창을 닫은(웹뷰 파괴) 뒤에도 메뉴 막대에 남고 카톡 수집이 이어진다(메시지함에 새 카톡이 쌓임) ☐ 전체 디스크 접근 권한을 끈 상태에서 「카카오톡을 읽을 수 없음 — 권한」 안내가 뜬다. **확인이지 결정이 아니다** — 고칠 것이 나오면 새 SH-IMP 항목
- **완료 조건(실물 · 코디 macOS → 사용자)**: 새 dmg 에서 `about:blank` iframe 시험 페이지가 취소되지 않음 · 기존 기능(내보내기 저장·OAuth 외부 열기·카톡 수집) 회귀 없음
- **시험**: `make shell-verify-strict` · `cargo test`(`lib.rs:992-998` 판별 시험 개정) · `make shell-final-preflight` · `make shell-release-preflight`

## Phase 반영 — 1루프 E2E → 2루프 → 운영

- [ ] 코디 `make local-stack`(**백엔드 커밋마다 재시작** — P-4) + `make tauri-local` 로 1차 확인 → **운영 반영 → 사용자 E2E(앱)** — 아래 체크리스트
- [ ] 사용자 지적을 **모아** 2루프 브리프 한 장(P-1)
- [ ] PR(코드) 하나 · 문서 PR 따로
- **운영 반영 순서**
  1. [ ] **manual SQL**(보정 표 · 업무/요청의 원래 메시지 칸 · 인덱스 `.concurrent.sql`)을 이미지보다 먼저
  2. [ ] **env** — 운영 back·워커(meeting·conversation·report)에 timeout 넷(기본값이면 생략 가능하나 명시 권장)
  3. [ ] **슬랙 앱 이벤트 구독**에 나간 방 계열 이벤트 추가(운영 슬랙 앱 설정 — 재설치 필요 여부 확인)
  4. [ ] 이미지 태그(back·front·워커) → Argo 수동 sync
  5. [ ] medi-ax dmg(SHELL) 전달 + 013 ②③ 체크리스트

### 사용자 E2E 체크리스트 (데스크톱 앱)

- ☐ 회의 목록 [수정] — 일정 세 칸 한 줄 · 검색 뒤에 깔린 것 없음 · 같은 사람 두 번 안 담김
- ☐ 수정에서 시간·인원을 바꿔 기존 방 비활성 이유 확인 → 다른 방으로 저장 → The Connect 에서 바뀐 예약 확인
- ☐ 「회의실 예약 없음」 으로 저장 → Connect 예약 사라짐
- ☐ 생성 모달 [불러오기] → 시간 그대로 · 미결 안건 「지난 회의에서 넘어옴」 · 새로 쓴 안건 「새로 추가된 안건」(회의 시작 화면에서)
- ☐ 30분 이상 회의 종료 → 「종료」 · 안건이 이야기한 순서 · 끝에 「용어 보정」 표 · 기한이 회의일보다 앞서지 않음
- ☐ AX 채팅 「회의 잡아 줘」 → 업무 생성 카드 같은 쪽 나눔 카드 · 거절·수정(회차)·등록 · 회의실 고르기
- ☐ AX 채팅으로 회의 시간 변경 → 카드에서 회의실 확인 → Connect 반영
- ☐ AX 채팅 「업무 만들어 줘」 → 프로젝트가 바로 잡힘
- ☐ 메시지함 메일·슬랙·카톡 **첨부 받기 → 다운로드 폴더 + 토스트**
- ☐ GitHub·Vercel 알림 메일 아이콘 보임
- ☐ 설정 연동 숫자가 새로고침 없이 늚
- ☐ 슬랙 메시지 호버 막대(셋)·툴팁 · 카톡(둘) · 답글 0개 메시지 「스레드에 답글」
- ☐ 메시지 「AX 업무 생성」 → 서랍·말풍선·참고 자료 한 줄 → 등록 → 업무 출처 「원래 메시지」 → 눌러서 돌아옴 · 「업무 만듦」
- ☐ 「AX 요약」 · 메일 머리 [AX 업무 생성][AX 요약]
- ☐ (dmg) 창 닫은 뒤 카톡 수집 지속 · 권한 없을 때 안내

**확인할 것 — 동작은 정했지만 사람 눈에 이상해 보일 수 있는 자리**(검수 §7 H-1 ~ H-10 · 사용자 판단을 받는다)

- ☐ **H-1** Connect 가 끊긴 상태에서 수정 모달 「기존 — (확인 못 함)」 을 둔 채 시간을 바꿔 저장 → 결과 줄 「회의실 예약은 확인하지 못했습니다」 가 보이는가 · Connect 에 옛 시각 예약이 남는 것을 받아들일 수 있는가(다시 맞추는 단추 없음)
- ☐ **H-2** 시간·인원을 바꿔 기존 방이 비활성일 때 [저장] 옆 이유 한 줄이 충분한가
- ☐ **H-3** 바로잡을 게 없던 회의 = 「바로잡은 용어 없음」 · 이 판 이전 회의 = 표 자리 없음 — 둘이 구분돼 보이는가
- ☐ **H-4** 빠른 시작의 빈 자리표시 안건 · 메모 폴백 「기존 회의록」 안건에도 「새로 추가된 안건」 이 선다 — 받아들일 수 있는가
- ☐ **H-5** 메시지함을 연 채 서랍에서 [등록] → 「업무 만듦」 이 바로 서는가
- ☐ **H-6** 단추를 누를 때마다 대화가 하나씩 는다 — 대화 목록이 괜찮은가
- ☐ **H-7** 「AX 업무 생성」 의 범위 = 최상위 메시지 위아래 최대 100건 · **답글 달린 메시지를 고르면 답글 본문은 빠진다**(답글까지는 스레드 패널 안 답글에서) — 말풍선 아래 범위 줄과 결과가 기대와 맞는가
- ☐ **H-8** 앱에서 썸네일을 누르면 크게 보기 대신 **파일이 저장되고 토스트** — 웹(새 탭)과 다른 것이 괜찮은가
- ☐ **H-9** 긴 회의의 「정리 중」 이 최대 약 30분(900초 + 새 세션 1회) — 진행 표시 없이 기다릴 수 있는가
- ☐ **H-10** 말에 날짜가 있었는데 회의일보다 이르면 기한이 **조용히 비어 있다** — 이유 표시 없이 괜찮은가

## Pre-deploy Check

- [ ] 모든 Phase 검수 처리 · 코디 `make verify` 통과 · 사용자 E2E(앱) 통과
- [ ] **env 신설 — timeout 넷**: `AX_AI_TIMEOUT_BATCH_SECONDS=240` · `AX_AI_TIMEOUT_WARMSTART_SECONDS=240` · `AX_AI_TIMEOUT_FINAL_SECONDS=900` · `AX_AI_TIMEOUT_CONVERSATION_SECONDS=180` — 로컬 `Makefile` 기본값 · 운영 values(back·meeting-worker·conversation-worker·report-worker)
- [ ] 최종 합성 900초가 **워커 쪽 다른 제한**(재배달 backoff · 영수증 lease · k8s liveness)에 걸리지 않는지 — 대화가 아니라 워커에서 돈다
- [ ] 슬랙 앱 이벤트 구독(나간 방 계열) · Connect 계정 env(`TDL_*`) 운영 설정 확인(BE §10-5)
- [ ] 외부 실물 1회씩: Connect 방 변경 · Codex/Claude 900초 합성 · Slack 나간 방 · Gmail 메일 맥락
- [ ] **운영 SQL 먼저**: `migrations/manual/2026-10-07-meeting-term-corrections.sql` 을 **이미지 반영 전에** 운영 DB 에 적용(새 표 `meeting_term_corrections` · `meetings.term_corrected_at`) · 로컬은 `make sync-demo-schema` 뒤 스택 재시작(검수 WP2 W-8)
- [ ] **AI 프롬프트의 실명** — 웜스타트는 참석자 실명을 싣지 않지만(원본 원칙), **AI 맥락 목록(D-13 「구성원 전부」)이 구성원 실명을 싣는다**. 사용자 결정에 따른 의도된 변화다 — 「웜스타트에 실명 미유출」 점검은 「참석자 → 화자 매핑에 실명 없음」 으로 좁혀 읽는다(검수 WP2 W-7)
- [ ] **프롬프트 크기** — 매번 전사 전량 + 맥락 목록이라 CLI 인자 한도(리눅스 argv 한 칸 128KiB)에 닿을 수 있다 — 1시간 회의 + 운영 조직 규모 최악 바이트 확인 · stdin 전달로 바꿨는지(검수 WP2 W-1 · `be-wp2-fix1-report.md`)

## 반영

- (운영 반영 때 적는다 — PR·이미지 태그·SQL·env·슬랙 앱 설정·dmg)

## Rollback

- 이미지 태그를 직전 값으로 → 수동 sync. **SQL 은 additive 라 남긴다**(새 표·nullable 칸 — 옛 이미지는 모른 채 돈다)
- env 넷은 지워도 기본값(코드)이 같아 무해 — 단 **옛 이미지는 env 를 읽지 않아 90초로 돌아간다**
- 슬랙 이벤트 구독 추가분은 옛 워커가 무시한다(처리하지 않는 이벤트) — 되돌릴 필요 없음
- dmg: 직전 dmg 재설치(셸 변경은 `about:*` 허용 하나)

## Done Criteria

- SPEC-008 AC-23~34 · SPEC-010 AC-01~22 가 채워지고, 외부 서비스 실물 1회 증거(Connect · Codex/Claude 900초 · Slack 나간 방 · Gmail)가 있다
- **사용자 E2E 체크리스트(앱)** 통과 · 2루프 지적 처리
- 운영 반영(web·워커·SQL·env·슬랙 앱 설정·dmg) 뒤 로그 오류 0 · 운영 로그 「remote image refused … 이미지가 아닙니다」(SVG) 0
- improvements SH-IMP-001~008 · 010~012 · 014~018 완료 기록 · 013 ②③ 사용자 확인 결과 기록(코디)

## Open Issues

| ID | 무엇 | 다음 |
|---|---|---|
| **I-1** | **011 — wry 정책 콜백에 프레임 구분이 없다**(FE §0 · §1-2). 「하위 프레임만 `about:*` 허용」 을 그대로 못 짓는다 — 메인 프레임의 `about:blank` 도 함께 허용된다(우리 웹은 메인 프레임을 `about:` 로 보내지 않는다) | 셸 워커가 대안(메인 프레임 판별 가능 여부) 확인 → 없으면 「`about:blank`·`about:srcdoc` 는 프레임 무관 허용」 으로 코디 결정 · SPEC-006 개정 |
| ~~**I-2**~~ | 원격 이미지 SVG 가 `_download` 를 지나면 `attachment` disposition 이 붙는다(`INLINE_IMAGE_TYPES` 밖) — **닫힘(코디 판정 W-8)**: 원격 이미지 응답은 `inline` + `Content-Security-Policy: sandbox; default-src 'none'` + `nosniff`(S8 §4.4 · §5). WP1-BE 가 원격 이미지 경로만 `inline` 으로 | 판정 났음 — WP1-BE 계약 「018 응답 disposition」 대로 구현 |
| ~~**I-3**~~ | `MeetingAgendaDraftInput` 을 생성·회의 중 안건 추가가 같이 쓴다 — `source` 를 더하면 추가 입구가 `carried` 를 받게 된다 | **닫힘(코디 판정 W-r2-5)** — **생성 전용 안건 입력 모델을 따로 둔다**(안건별 `source`). 추가 입구는 옛 모델(`title` 만) 그대로(WP1-BE) |
| ~~**I-4**~~ | `meeting.info.update` 카드가 어느 편집기로 그려지는지 | **닫힘(검수 F-2)** — 편집기가 없다(편집 계약 `None` · 결과 카드). 이 판에서 새로 만든다(WP3-BE · WP3-FE) · 옛 `meeting.update` 는 같은 검증 경로로 합친다 |
| **I-5** | Connect 의 **방 변경 PUT** 은 어댑터 인자만 있고 호출부가 쓴 적이 없다(BE §2.3) — 실제로 방이 옮겨지는지 미검증 | WP3-BE 실물 1회가 완료 조건 |
| **I-6** | 맥락 목록을 실은 프롬프트 크기(조직 규모) — Codex/Claude 입력 한도·속도 실측 없음 | WP2-BE 재합성 실물에서 크기·시간 기록 |
| **I-7** | `integration.changed` 를 자주 내면 설정·메시지함 두 화면이 다시 읽는다 — 묶어 내기 = **같은 연동 1초에 한 번**(S8 OQ-818 코디 기본값) | WP1-BE 실측 뒤 조정 |
| **SPEC OQ** | SPEC-008 OQ-812 ~ OQ-819 / SPEC-010 OQ-1001 ~ OQ-1017 — **전부 닫힘**(코디 기본값 · 사용자 통보 — 바꾸면 다시 연다). OQ-1002 ① 은 **조직 전체**로 정정(D-13 정본) | 사용자가 바꾸면 2루프 |

## Domain / Schema (구현 초안 — 전문 SoT 는 코드·migration)

| 무엇 | 초안 | 마이그레이션 |
|---|---|---|
| **용어 보정 표** | 회의 최종 벌에 매달린 표 — 회의 FK · `heard` · `corrected` · `grade`(`auto`\|`presumed`) · 순서. 최종 합성이 성공할 때마다 **그 회의 것을 통째로 갈아 끼운다**(최종 벌 전량 교체와 같은 트랜잭션) · **「정정이 돌았는가」 = 회의(`meetings`)의 nullable 시각 `term_corrected_at`**(코디 판정 N-1) — 정정 pass 가 든 최종 합성이 적재될 때 같은 트랜잭션에서 찍는다. 응답은 이 값이 null 이면 `term_corrections: null`, 있으면 행 목록(0개면 `[]`) · 재시도 [다시 시도]로 최종 벌을 갈아 끼우면 다시 찍는다 | **있음** — 새 표(`backend/migrations/manual/*.sql` + 인덱스 `(meeting_id, order)`) + **`meetings.term_corrected_at` nullable 칸 추가**(additive · 기존 회의는 null) · 로컬 `schema_sync` |
| **안건 출처** | 칸은 이미 있다(`meeting_agendas.source` · 값 `manual`/`carried`) — 값만 안건별로 | 없음 |
| **메시지 참고 자료 종류** | `conversation_context_references.resource_type` 에 `inbox_message` — 칸에 CHECK 없음(`persistence.py:735-746`) | 없음(값만) |
| **업무 출처 — 원래 메시지** | 업무·업무 요청에 **원래 메시지 FK(nullable)** — 메시지 소프트 딜리트와 무관하게 남는다. 확정 때 그 Action 이 나온 턴의 참고 자료에서 찾는다 | **있음** — 두 표에 nullable 칸 + 인덱스(「업무 만듦」 수를 이 칸으로 센다 — 따로 세는 칸을 두지 않는다) |
| **「업무 만듦」** | 파생 — 위 FK 를 메시지별로 센다 | 없음(인덱스만) |
| **AX 회의 초안 저장** | 초안 저장 종류 상수에 회의 생성 더함 · 회차는 기존 제출 판 | 없음 |
| **회의실** | 기존 `meetings.room_reservation` JSON · 생성 이중 예약 울타리 표(`meeting_room_creation_attempts`)를 수정의 새 예약에도 | 없음 |

---

## 부록 — DEC-009 결정 → SPEC 절 (전수 대응표)

**37건 전부**(D-01~D-37) + DEC-009 가 닫은 OQ 아홉. SPEC-008 이 **20건**, SPEC-010 이 **17건**을 받는다.

| D | 무엇 | 받는 SPEC · 절 | Phase |
|---|---|---|---|
| D-01 | 범위(019 보류 · 009 완료 · 013① 뺌) | S8 §6 DEC-009 표(과정) · S10 §1 Scope | 전체 |
| D-02 | 순서 BASE·DEC → SPEC·WORK → 구현 | S8 §6 DEC-009 표(과정) | 전체 |
| D-03 | 완료 = 앱 실물 | S8 §6 v0.6.0 머리 · AC-23·27·29 | P-3 |
| D-04 | AX 회의 생성 = 업무 생성 흐름·디자인 | S10 §2.4 · §4.4 · AC-19 | WP3 |
| D-05 | 참고자료 같은 기준 | S10 §2.4 · §4.4 · AC-20 | WP3 |
| D-06 | 일정 칸 겹침 | S10 §2.1 · AC-01 | WP1 |
| D-07 | 생성·수정 회의실 셀렉트 · Connect 수정 | S10 §2.2 · §4.1 · §4.3 · AC-03~08 | WP3 |
| D-08 | 기존 방 비활성+이유(기본값) | S10 §2.2 · §4.1 · AC-05 | WP3 |
| D-09 | AX 수정 카드 회의실 | S10 §2.4 · §4.3 · AC-21 | WP3 |
| D-10 | 불러오기 시간 안 가져옴(기본값) | S10 §2.3 · AC-09 | WP1 |
| D-11 | 안건 출처 안건마다 · 두 입구 | S10 §2.3 · §4.2 · AC-10·11 | WP1 |
| D-12 | 회의록 고도화 · 단계별 timeout | S10 §4.5~4.7 · AC-12~14 | WP2 |
| D-13 | AI 맥락 목록 | S10 §4.5 · AC-18 | WP2 |
| D-14 | 취소 업무 제외(기본값) | S10 §4.5 | WP2 |
| D-15 | 안건 순서 | S10 §2.5 · §4.7-7 · AC-16 | WP2 |
| D-16 | 정정 pass · 보정 표 · 최종 1회 | S10 §4.7 · AC-15 | WP2 |
| D-17 | 등급(기본값) | S10 §4.7-3 | WP2 |
| D-18 | 보정 표 화면 끝(기본값) | S10 §2.5 · AC-15 | WP2 |
| D-19 | 기한 버그 | S10 §4.8 · AC-17 | WP1 |
| D-20 | AX 업무 생성 맥락 목록 | S10 §4.5 · AC-22 | WP3 |
| D-21 | 첨부 받기 완료 = 앱 | S8 §2.2 · AC-23 | WP1 |
| D-22 | 받기/미리보기 주소 · 링크 속성 | S8 §2.2 · §4.4 · §5 프론트 · AC-23 | WP1 |
| D-23 | 원격 이미지 자동·프록시 | S8 §2.1 ③ · §4.4 · AC-08b | WP1 |
| D-24 | SVG 허용 + 샌드박스 | S8 §4.4 · §5 원격 이미지 프록시 · AC-24 | WP1 |
| D-25 | 연동 상태 사건 · 폴링 없음 | S8 §4.4 · AC-25 | WP1 |
| D-26 | 셸 하위 프레임 허용 | S8 §5 데스크톱 경계(소유 SPEC-006) | SHELL |
| D-27 | 나간 방 즉시 분배 중단 | S8 §5 동기화 · Case Matrix · AC-26 | WP4 |
| D-28 | 셸 dmg 묶음 = 011 + 013②③ 확인 | S8 §5 데스크톱 경계 | SHELL |
| D-29 | 호버 막대 · 두 단계 호버 | S8 §2.9 ① · AC-27 | WP4 |
| D-30 | AX 서랍 · 말풍선 · 기존 흐름 · 요약 저장 안 함 | S8 §2.9 ③ · AC-29·30 | WP4 |
| D-31 | 서버 조합 · 우리 모양 · 남의 방 거절 | S8 §4.8 ①② · AC-32 | WP4 |
| D-32 | 위아래 100줄 · 스레드 전체 · 있는 만큼 | S8 §4.8 ② · AC-32 | WP4 |
| D-33 | 스레드에 답글 · 권한 추가 없음 | S8 §2.9 ① · AC-28 | WP4 |
| D-34 | 시안 없이 슬랙 모양(기본값) | S8 §2.9 ① | WP4 |
| D-35 | 메일 머리 단추 · 같은 흐름 · 그 메일 | S8 §2.8 · §2.9 ② · AC-31 | WP4 |
| D-36 | 단추 순서(기본값) | S8 §2.8 · AC-31 | WP4 |
| D-37 | 자동 추천 다음 · 로직 분리 · 생성만 | S8 §1 Out · §4.8 ② · AC-34 | WP4 |

| 닫힌 OQ | 받는 자리 |
|---|---|
| OQ-901 흐름·디자인만 같게 · 내용은 회의 필드 | S10 §2.4 · §4.4 (쪽 구성은 S10 OQ-1001 로 다시 열림) |
| OQ-902 timeout 240/240/900/180 · 새 세션 1회 | S10 §4.6 |
| OQ-903 이월 회의만 · 취소 제외 · 하한 · KST | S10 §4.8 |
| OQ-904 재전사 전체 발화 매번 | S10 §4.7-1 |
| OQ-905 「참석 N명」 그대로 | S10 §1 Out · §2.5 |
| OQ-906 재확인 · 문구 가르기 · 「회의실 예약 없음」 | S10 §2.2 · §4.1~4.3 |
| OQ-907 출처 링크 · 「업무 만듦」 | S8 §2.9 ④ · §4.8 ③④ |
| OQ-908 「AX 업무 생성 · AX 요약」 · 「스레드에 답글」 | S8 §2.9 ① |
| OQ-909 중복 방지만 | S10 §2.1 |

## Related

- `orchestration/work/strong-hajin-enhance/_RESUME.md` §2 — 결정 원장 · `be-survey-report.md` · `fe-survey-report.md` — 조사
- WORK-011 — 외부 채널 1단계(메시지함·셸 가로채기의 출처) · WORK-010 — 셸 다운로드 가로채기
