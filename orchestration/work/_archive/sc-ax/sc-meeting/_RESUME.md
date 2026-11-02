# 재개 노트 — sc-meeting (sc-ax)

**지금(2026-09-10 밤)**: WP-001(BE)·WP-006 P1·2(FE) 구현·검수 PASS·실물 확인·커밋(app 5751efa). SPEC 0.4.1(D1~D24)·WP 6 커밋(spec a54c2e6e0). 다음: **WP-002 스트림 중계 BE 브리프**(원형 task-management meeting_stream) + WP-005 병렬 검토 → 발주 승인. ~~SPEC-004 0.4.1 + WP-001~006 검수 3 PASS. 시안 2개(회의록·회의실) 확정(D15 디자인 정본). 다음: 사용자 리뷰 → BE/FE 브리프(발주 승인) → 구현. ~~회의록 방향 결정 2건 확정(2026-09-09) — ① STT 는 **백엔드 중계**, ② **실시간 전사가 정본**. 조사 1 리포트 완료. 컨셉 = 나(서기)·AI·조직원이 같은 회의에 참석. 회의 중 서기 노트 탭 / AI 노트 탭 각자 기록, 종료 후 둘을 합쳐 최종 회의록.
**다음**: 두 결정의 파급(아래 §2 비고)을 사용자와 닫고 → planner 발주로 baseline·decision·spec-004 갱신(승인 게이트). 조사 2(프론트 MeetingDrawer 전수) 필요 여부 확인. 발주 전 브리프 승인.

세팅: `scripts/new-work.sh sc-ax sc-meeting --workers planner,backend,frontend` (2026-09-08 재실행) · 설정 SSOT `config/projects/sc-ax.json`
코디handle: **`term_828dfb7e-5785…`**(09-10 저녁 · 이전 `term_42ca89d6…` 도 죽음)(2026-09-10 오후, `orca terminal list` 제목 「회의실 디자인 import」·코디 워크트리로 식별. 이전 `term_a53b7eb6…`·`term_d9153f79…`·env `term_becfca70…` 전부 죽음. 워커 핸들도 회전한다(designer-1: `term_571e4844…`→`term_d40a436a…`). **발주·재개·메시지 전마다 list 로 코디·워커 핸들을 제목으로 다시 찾고, 살아 있는 워커에게 terminal send 로 알린다**)

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec` (branch `kknaksss/sc-meeting-spec`, base `origin/main` **59cd71302** → PR `main`). ~~a8e934970 본은 2026-09-09 orca 정리로 사라짐~~ → 2026-09-10 `new-work.sh --workers planner` 로 재생성. 회의록 문서: `products/sc-ax/20-spec/spec-004-meeting-note.md` · `00-planning/plans/plan-004-meeting-note.md` · `00-baseline/_working/meeting-notes-consolidated.md`
- `app`: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` (branch `kknaksss/sc-meeting`, base `origin/main` → PR `main`)
- ~~생성 후 PR #2 head를 fast-forward로 반영했다. HEAD는 `663319c`.~~ **2026-09-10 origin/main(`a0bcee8`)으로 reset.** PR #2 는 squash `5e2ddec` 로 main 에 들어갔고(우리 11커밋 + 후반 Select·TimeField·Storybook 포함), 그 위에 PR #4(자료 검색) 가 있다. 이제 origin/main 과 동일, ahead 0.
- `branch.kknaksss/sc-meeting.gh-merge-base=main` 설정.

## 1. 지금

- [ ] 기존 Claude Design 디자인 시스템을 바탕으로 회의록 디자인 작업 구체화.
- [ ] 구현 발주 전에 SPEC → WP → 사용자 리뷰 순서를 따른다.
- [!] 현재는 세팅만 완료. 워커 발주·의존성 설치·서버 실행·push·새 PR 생성은 하지 않았다.
- [!] 브리프 3개(spec·be·fe)는 config 값만 채워진 빈 껍데기 — 범위는 SPEC·WP 확정 후 채운다.
- [x] PR #2 는 main 에 squash 머지됨(2026-09-10 확인). 워크트리를 origin/main `a0bcee8` 로 reset — 이제 PR diff 에 선행 PR 이 섞이지 않는다.
- [!] PR #2 조회에는 12커밋이 있었지만 fetch 후 실제 origin/main 대비 HEAD는 ahead 11 / behind 0이다. 현재 main 대상 diff에 선행 PR 변경도 포함된다. PR 생성 시 병합 상태를 다시 확인한다.

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-08 | main에서 새 브랜치를 만들고 PR #2 최신 내용을 이어받는다. 최종 PR 대상은 main. | 사용자 지시 |
| 2026-09-08 | 기존 Claude Design 디자인 시스템으로 회의록을 먼저 디자인한다. 이번 요청은 작업 세팅까지. | 사용자 지시 |
| 2026-09-10 | **목록 화면(SCR-105)은 화면정의서가 정본.** Claude Design 회의록.dc.html 과 다른 7개 지점(메뉴명 「회의 목록」·[회의 시작]+[회의 예약]·예정/지난 두 구획(월 이동·프로젝트 필터·정렬 없음)·행 꼬리표 규칙·패널 머리에 상태 없음·패널은 얇게(원문 탭·파생 업무 표 없음, 후보 건수만)·MOD-102 필드) 전부 화면정의서대로. | 사용자 「화면정의서가 맞는 디자인이야」 |
| 2026-09-10 | **D10 — 이번 데모에서 알림 제외.** 상단 알림·공유 시 알림(MOD-105-T04)·회의 알림 진입(CMP-104)·X-99 알림 셋 전부 데모 범위 밖. 공유는 「받은 사람 목록에 열람으로 담김」까지. planner 에게 terminal send 로 전달(SPEC §2 미제공 + 10-decision D10). | 사용자 「이번 데모에서 알림은 뺄거야」 |
| 2026-09-10 | **D11 — 이번 데모에서 상단 공통 셸의 AI 채팅 입력([묻거나, 받은 내용을 붙여넣으세요]+[보내기]) 제외.** 회의 화면은 상단 바 없이 페이지 제목부터. planner 에 전달. | 사용자 「이것도 빼자」 |
| 2026-09-10 | **D12 — 안건 본문 형식: 한 줄씩.** 종류 배지 없음(우리 회의는 논의 줄뿐). 안건 N. 제목 → 내용 줄 목록 → 「다음 할 일」 테스크 줄 목록(새 후보 + 이미 있는 테스크 「연관 업무 ›」). AI 중간 요약은 줄 증분, 메모도 줄, 합성은 줄 병합. 기획 OQ-006(형식)·spec OQ-306(블록 경계) 을 우리 범위에서 닫음 → planner 재발주 때 SPEC §6·§7·§8 반영. 두 디자이너에 지시. | 사용자 「논의만 있어서 한 줄씩 적어주면 될 거 같아 · 안건/내용1·2·3/다음 할일/테스크1·2/이미 있는 테스크」 |
| 2026-09-10 | **D13 — 상태 여섯: 예정·진행 중·정리 중·완료·실패·취소됨.** 정본 「정리됨」→「완료」로 이름만 바꿈(M7 닫힘). 취소됨 유지(자동 취소 X-185·[회의 취소] 포함). | 사용자 「취소도 있어야지」·상태 목록 |
| 2026-09-10 | **D14 — 바로 시작 회의 처리.** AI 는 자기 트랙에서 회의 중 즉시 안건을 세움(기존 안건 맞으면 그 아래 줄, 안 맞으면 새 안건 — X-94 「기타」 규칙 폐기). 참석자 추측(E61) 없음 — 사람이 조직도/사외 추가로 직접. 제목은 종료 합성 때 AI 후보 → 사람 확정. 장소는 예정·완료 상태의 머리 편집에 글자 칸(회의실 판정 없음 — 코디 판단, 사용자 미이의). | 사용자 「AI 가 자기 나름대로 회의록을 만드는 거」·「참석자는 사람이 직접」·「제목은 최종 때」 |
| 2026-09-10 | **D15 — 디자인이 정본.** `design/회의록.dc.html`·`회의실.dc.html`(+REPORT 2) 가 화면 SoT. SPEC 본문은 디자인대로 쓰고, 기획서와의 차이는 §12 한 줄 목록만(기획자 통보용). 기획 개정 요청을 본문에서 따지지 않는다. | 사용자 「디자인이 이제 정본인데 … 디자인대로 만들면 되잖아」 |
| 2026-09-10 | **WP 작성 지시.** SPEC 0.4.0 과 함께 30-work/ WP 를 쓴다. 백엔드 로직은 task-management 정본(spec-007 + meeting_stream/batch/finalize 코드). 완료 후 reviewer_spec 재검수. | 사용자 「스펙 WP 작성하라고 그리고 리뷰 돌려 · 백엔드 로직은 task-management 참고」 |
| 2026-09-10 | **D16(코디 기본값, 검수 2 반영)** — 회의 정보 편집은 참석자 전원(회의록 편집만 만든 사람) · 「기타」 블록 없음 · 삭제 둘째 갈래 「회의록만 삭제」= 회의록(+자료) 삭제·예약 유지, [회의 취소]= 회의 취소 · 안건 출처 = 직접 입력·지난 회의에서 넘어옴·AI 정리 · 회의실 「가능」 판정·the Connect 연동은 데모 범위 밖(정적 목록) · 화자 매핑 BE=WP-002 · /end=WP-001. | 코디 통보(사용자 미이의 시 확정) |
| 2026-09-10 | **D17 — 안건 결론(concluded) 결정 주체.** 종료 합성(WP-004) 때 AI 가 안건별로 채우고, 만든 사람이 편집 모드에서 뒤집는다(PATCH agendas concluded). 토글 모양 기본값 = 편집 모드에서 제목 옆 「결론 남/안 남」 표시 클릭(R-30 닫힘 후보). 회의 중에는 결론 안 건드림. | 사용자 「응 맞아」 |
| 2026-09-10 | **D18 — 화자는 익명 라벨(「화자 N」)만. 화자 이름 매핑은 데모 범위 밖.** SPEC §2.2 행 추가·WP-002 화자 매핑 제거·WP-006 이름 달기 UI 제거(planner·FE 에 지시). | 사용자 「우리는 화자로만 일단 하자」 |
| 2026-09-10 | **D19 — 후속업무 후보 페이로드 = 업무 생성 컬럼 맞춤.** Todo { title ≤100, description(근거 줄+출처), assignee_candidate(참석자 중), due_candidate, checklist_candidate[], reference{meeting,agenda,line_ids}, linked{task|work_request} }. 승격: **항상 업무 요청(POST /api/work-requests)** — 요청자=누른 참석자, **담당은 AI 후보 없이 사람이 모달에서 직접 고름(참석자 우선 → 조직도)**(2차 정정: 조직 데이터에 역할 설명 없어 추측 금지). assignee_candidate 필드 제거, 수락 시 Task 생성. linked {work_request_id, task_id|null}. (사용자 「회의가 담당자에게 업무 요청을 보내는 느낌」으로 정정) 승격 모달(MOD-101, SCREENDEF-004 소유)은 채워진 채로 연다. SPEC §8·§9·WP-004·WP-006·WP-001 Todo 갱신 planner 에 지시. | 사용자 「업무 컬럼 채울 값을 뽑아 payload 에 실어야」 |
| 2026-09-10 | **D20 — 업무 출처는 열로.** work_requests·tasks 에 source_meeting_id·source_agenda_id 추가, origin_kind 「meeting」. 승격 요청이 두 id 를 실어 보내고 수락 시 Task 로 옮김. Todo.reference = {meeting_id, agenda_id, line_ids[]} 확정. description 출처 줄은 사람용으로 유지. planner 에 지시(SPEC §8.1·§9, WP-004, WP-001). | 사용자 「우리 업무 테이블이 그렇게 간단해?」 → 코디가 테이블 대조 후 결정·통보 |
| 2026-09-10 | **D21 — 후속업무 후보는 최대한 채운다.** description 항상(2~4문장+근거+출처), checklist 항상 제안(2~5단계), due 는 발화 날짜 → 다음 회의 전날 → 없으면 비움. 담당만 사람. planner 에 지시(SPEC §8.1·§8-5·§9-5, WP-004, WP-003). | 사용자 「최대한 많이 채워야 사람이 입력을 안 하지」 |
| 2026-09-10 | **D23 — AI 배치 세션: 웜스타트 + MCP + 중복 방지.** 회의당 provider 세션 유지·배치마다 resume(첫 배치 맥락 적재, 이후 증분). 배치는 scax MCP 붙인 converse(도구: 업무 목록·프로젝트·이전 회의·참석자, 레지스트리로 확장). 기존 업무 있으면 후보 대신 linked. 「회의=구조화 생성」 테스트 고정 폐기. planner 에 지시(SPEC §7·§8·§11·§13, system.md, WP-003·004). | 사용자 「웜스타트 하자, task-management 처럼 · MCP 로 업무 목록 조회 · 툴 리스트 늘어날 수 있어」 |
| 2026-09-10 | **D24 — 「연관 업무 ›」 제거.** 기존 업무와 겹치는 후보는 내지 않음(linked 대체 아님). 승격된 행은 「요청됨」 글자만, 링크 없음. linked 는 역추적 데이터로만. planner·designer-1·2·FE 지시. | 사용자 「연관업무는 뺄거야 … 결과에 있는 게 안 맞아」 |
| 2026-09-09 | **STT 는 백엔드 중계로 전환.** Soniox websocket 세션을 서버가 소유하고, 브라우저는 오디오를 우리 서버로 보낸다. 현행 임시 키 발급·브라우저 직결·확정 구간 POST 경로는 걷어낸다. 근거: AI 가 참석자인 컨셉 — 회의의 귀는 서기 브라우저가 아니라 서버여야 AI 노트·참석자 fan-out·오디오 저장·300분 세션 회전이 한 곳에 모인다. 참조 구현: task_management `app/back/service/meeting_stream_service.py`·`integrations/soniox.py`(실물 회의 3회 검증). | 사용자 결정 「백엔드 중계로 가자」 |
| 2026-09-09 | **실시간 전사가 정본.** 종료 후 파일 재전사(`stt-async-v5` 2-pass)는 정본이 아니다. refinement·summary·근거 칩은 실시간 구간에 결박된다. 현행 「realtime 은 임시, 파일 전사가 대신한다」 규칙(조사 1 §4.1-①·②)은 폐기. | 사용자 결정 「실시간을 정본으로」 |
| 2026-09-08 | **회의 전사는 Soniox 실시간 STT** — 기준 문서 `orchestration/work/_archive/task-management/docs-v1/soniox-study.md`(2026-09-03 조사: 브라우저 직결 direct stream · 백엔드는 temp key 발급만 · `stt-rt-v5` · 확정 append/잠정 갱신 · 화자 라벨→이름 매핑은 우리 몫 · endpoint detection 미사용 · 2-pass 여부는 미결). ax-workspace 현행 코드가 이미 이 구조(조사 1 §4.1-①). | 사용자 지시 「회의 전사는 이걸 쓸거야」 |

### §2 비고 — 두 결정의 파급 (2026-09-09 사용자 답)

| 항목 | 결정 | 사용자 말 |
|---|---|---|
| 파일 재전사(`stt-async-v5` 2-pass) | **완전 삭제** | 「완전히 없앨거야」 |
| 오디오 원본 | **보관한다.** 용도는 「나중에 원본이 필요한 경우」 — 구체 용도(재생·감사)는 스펙 Open Question | 「오디오 나중에 원본이 필요한 경우들이 생겨」 |
| 정제 시점·화자 매핑 시점 등 회의 백엔드 플로우 전반 | **task-management 가 정본.** 코드 리포 `main` 브랜치 기준. sc-ax 는 그 플로우를 따라간다 | 「회의 백엔드 플로우는 task-management가 정본이야 main 브랜치 보면 돼」 |
| 참석자 fan-out | **WS** (중계라 어차피 필요) | 「어차피 중계니까 ws 가 필요할걸」 |
| 300분 초과 회의 | **없다고 가정.** 세션 회전 미구현, 스펙에 한도로 명시 | 「300분 이상 회의는 없겟지」 |
| 문서 파급 | spec-004 §4·§5 · system.md §4 · soniox-study 「2-pass 미결」 닫힘 | — |

## 3. 발주 (살아 있는 것만)

- [x] **조사 1 — 백엔드 AI 프로바이더 현황** · `reviewer_code` · read-only · 브리프 `sc-meeting-survey-ai-provider-brief.md` · 산출물 `survey-01-ai-provider-report.md`(372줄) · **완료 2026-09-08** — 양쪽 워크트리 status 빈 것 코디 확인. 워커 터미널 `term_a4d2b3a8…` 은 살려 둠(조사 2 재사용 가능). 발주 2026-09-08 10:58 — task `task_f206a50eb5b0` · dispatch `ctx_97b0b9ca0a50` · 워커 `term_a4d2b3a8-30ab-4731-85f2-5ce199bada6b`(ax-workspace/sc-meeting 트리). 사용자 승인: 「읽기 전용이니까 조사 보내」. 사용자 말: 조사는 여러 번 한다(다음 후보: 프론트 회의 화면 현황, spec-004 ↔ 디자인 대조).

- [x] **planner — 결정 D1~D11 기록 + SPEC-004 재작성(0.2.0→0.3.0, 87→426줄) + system.md §4** · **완료 2026-09-10** — 변경 3파일·`00-planning/` 무변경 코디 확인, lint --strict sc-ax 범위 0. §12 기획 개정 요청 12건(R-1~R-12) · §13 Open Question 16건(OQ-301~310 신규). 다음: reviewer_spec 검수 → 사용자 리뷰. 워커 터미널 `term_e155b48b…` 살아 있음. · 브리프 `sc-meeting-spec-brief.md` · 변경 파일 **3개**(`00-planning/` 은 기획자 소유 — 건드리지 않음, 어긋남은 SPEC §12 「기획 개정 요청」으로) · **발주됨 2026-09-10** — task `task_21bfd9cdc7be` · dispatch `ctx_33b56394c598` · 워커 `term_e155b48b-1a1f-4392-99eb-2889228625e7`(mediness sc-meeting-spec 트리). 사용자 승인 「응 발주 하자」. 통과 후 reviewer_spec 검수 → 사용자 리뷰 → WP 발주.

- [x] **검수 1 — SPEC-004 0.3.0** · `reviewer_spec` · **완료 2026-09-10 — 총평 FAIL(F-1 1건 · WARN 11건)**. F-1: spec-004 §5.3 부근(174·188·189·205·208·209줄)이 기획에 없는 「일시정지·재개·마이크」 조작과 문구 「다른 창에서 기록 중입니다」를 신설 — task-management spec-007 UX 가 WS 계약과 같이 실려옴. 축 1·2·4·5·6 PASS. **사용자 결정 4개**(§7): ① F-1 처리(화면만 걷어냄 / 프레임까지 / §2.2 데모 밖) ② SCAX-ESC-002 재사용 ③ SCR-106-E07 「직원 누구나(X-96)」 뜻 ④ version 필드 정의. 다음: 사용자 답 → planner 수정 재발주 → 재검수. 발주 2026-09-10 — task `task_01957601e2f9` · dispatch `ctx_fa97f1dda175` · 워커 `term_a551cbf0…`(spec 트리 새 세션). 사용자 「검수 보내고」.
- [x] **디자인 — 회의 목록 SCR-105 시안 재작업** · `designer` · **완료 2026-09-10** — `design/회의록.dc.html` 878줄(원본 `.before`), `design/REPORT-회의록-v2.md`. 요소 21·문구 6 전부, MOD-102 드로어 포함. 문법·태그 짝·금지어·클래스 실재·타이포 4단 검증 통과. **결정 필요 3**: 드로어 푸터 primary(둘 다 btn h40 으로 둠) · [내보내기] 숨김 조건에 취소됨 포함 여부 · 예정 회의에 [공유] 노출 여부. 비워 둔 것 7건은 리포트 §6. 아직 Claude Design 에 안 올림(로컬 렌더 불가). 발주 2026-09-10 — task `task_4c7627c7a898` · dispatch `ctx_8ac87a83f5b6` · 워커 `term_571e4844…`. 기준: 화면정의서 SCR-105·MOD-102 + D10·D11. 사용자 「백그라운드로 회의록 페이지 우리 와이어프레임에 맞게 다시 그리라고」.

- [x] **디자인 2 — 회의 상세 SCR-106 시안(`회의실.dc.html`)** · **완료 2026-09-10** — 요소 40/44(없는 4 = E59~E62 바로 시작 회의 머리 편집), 문구 17/24(없는 7 = 실패 경로 T01·T10·TXT-001·TXT-003 + M1 T15·T17·T18), 금지어 0, 6상태×3viewer 18조합 §5.7 일치. 미결 M1~M8(REPORT-회의실-v2 §6) — **M2** 「정리 중」 회의록 구획 문구 정본에 없음 · **M7** 상태명 갈림(목록=「완료」, 상세=「정리됨」) 코디/사용자 판정 필요. · `designer-2`(코디 워크트리 탑승, opus) · 브리프 `sc-meeting-design-detail-brief.md` · 산출물 `design/회의실.dc.html`(원본 `.before`) + `design/REPORT-회의실-v2.md` · **발주 2026-09-10** — task `task_bee4d9901528` · dispatch `ctx_be9d7e6e7bb8` · 워커 `term_52ce3ca7…`. 기준: SCR-106 + D1 두 트랙=탭 둘(진행 중) / 합쳐진 회의록(정리됨) + 6상태×3 viewer + X1 일시정지 금지. 사용자 「디자이너 한 명 더 병렬로, 오퍼스」.
- [x] **디자인 1 후속 — MOD-102 모달 전환 완료(2026-09-10)** — `.modal` 위 폼, max-width 760(와이어프레임 비율 1250 은 판이 돼서 축소, 사용자 확인 필요). 사용자가 워커에 직접 지시한 이탈 누적 6건: ① E05 상태 전부 표시 ② E22 다음 할 일 + E23 건수줄 제거 ③ MOD-102 칸 순서 주제·일시·목적·안건·참석자·장소 ④ 반복 삭제(E17·E28·E29·E30·T22·T23) ⑤ 사외 참석자 칸을 「사외 참석자로 추가」로 접음 ⑥ 참석자 좌(조직)/우(이름 찾기) 2단. → **screen-005 개정 요청 목록**(REPORT-회의록-v2 §6-0). ~~디자인 1 후속~~ · designer-1 에 terminal send(핸들 회전: `term_571e4844…` stale → 제목 「SCR-105 회의 목록 화면 시안 그리기」 세션). 사용자 「모달로 바꿀게」. 정본 §2·5.1 「모달」 — 브리프의 Drawer 지시는 코디 오류.

- [x] **검수 2 완료(2026-09-10) — FAIL 2(F-A 회의 정보 편집 권한 owner↔참석자 · F-B 「기타」 블록 시안 잔존) · WARN 9.** WP 6건 전부 통과(원형 코드 주장까지 실재). 코디 기본값으로 수정 발주: planner(0.4.1 — §3.3 참석자, 삭제 둘째 갈래 「회의록만 삭제」 뜻 확정, 출처 값 3개, 화자 매핑 WP-002, /end 소유 WP-001, 회의실 판정 데모 범위 밖) + designer-2(기타 블록 제거·세트→직접 입력·리포트 표 갱신). ~~검수 2~~ · `reviewer_spec` · 브리프 `sc-meeting-review-spec-2-brief.md` · 산출물 `review-02-spec-004-report.md` · **발주 2026-09-10** · 기준: 시안 정본(D15)·결정·task-management 원형·검수 1 해소. 사용자 「리뷰 돌려」.

- [x] **검수 3 완료(2026-09-10) — PASS(WARN 1).** FAIL 2·WARN 8 전부 해소 확인. WARN 1 = 시안 MOD-102 회의실 「가능」 배지 잔존 → designer-1 제거 + planner R-33 한 줄 지시. **SPEC 0.4.1 + WP-001~006 사용자 리뷰 가능 상태.** ~~검수 3~~ · `reviewer_spec`(검수 2 세션) · 브리프 `sc-meeting-review-spec-3-brief.md` · 산출물 `review-03-spec-004-report.md` · 발주 2026-09-10. PASS 면 → 사용자 리뷰 → BE/FE 브리프.

- [x] **backend — WP-001 도메인·API 완료(2026-09-10)** — 20파일, 226 passed, reset-demo 성공, 계약 diff 0. 주의점: 자동 취소 조회 시점 판정 · 열람 축 조직→참석 · visibility 컬럼 삭제 · 안건 POST 201 · can_edit_note 가 cancelled 에서도 true(SPEC §5.1) · failed→summarizing 허용 · recordings/start·stop 잔존(WP-002 인계). ~~backend~~ · 브리프 `sc-meeting-be-brief.md` · **발주 2026-09-10** · task `task_af42f7154234` · dispatch `ctx_e6c5c0cb1246` · 워커 `term_50bcf0cc-bae5…`(ax-workspace/sc-meeting, `backend/` 만). 사용자 「응 발주해」.
- [x] **frontend — WP-006 Phase 1·2 화면 완료(2026-09-10)** — `frontend/src/meetings/` 8파일 + api/viewModels/labels/App/Calendar. tsc 0 · vitest 65/65. 시안 충족 SCR-105 20/21·MOD-102 18/18·SCR-106 34/40(미충족은 WP-002/003/005 계약 공백·Phase 3). 확인 4: ① 안건 PATCH lines 덮어쓰기 가정 → BE 에 계약 보강 지시 ② 스크립트 탭 빈 상태 문구 워커 창작(확정 문구 없음 → OQ) ③ 장소 잠금은 시안(D16) 우선 ④ 제안 카드 불러오기가 날짜까지 채움(시안). 코드 리뷰·실물 확인은 BE 완료 후. ~~frontend~~ · 브리프 `sc-meeting-fe-brief.md` · **발주 2026-09-10** · task `task_b98ee5965841` · dispatch `ctx_5589cecfd0b9` · 워커 `term_bb3a4c59-dfaf…`(ax-workspace/sc-meeting, `frontend/` 만). 사용자 「응 발주해」.

- [x] **코드 검수 1 완료(2026-09-10) — FAIL(BE 3·FE 2, 합의 2).** 바닥 OK(경계 0·검증 항목 전부 테스트·4종 통과). F1 과거 일시 회의 자동취소 오적용 · F2 Todo 모양 BE(브리프)≠FE(SPEC §8.1) · F3 can_edit_note 가 예정 안건 편집 막음 · F4 목록 패널에 [다음 회의 예약]. **코디 결정 D22**: Todo 정본=SPEC §8.1 · can_edit_agendas 신설(scheduled|done|failed|cancelled, 만든 사람; 진행 중·정리 중 사람 안건 편집 409) · 열람 축 셋째(executive 조직범위) 제거(board/get) · list 자동취소 commit · 공유 토스트 「공유했습니다.」 · domain-model.md 갱신 허용. 브리프 §3 이 틀린 3건(can_edit_note@cancelled·failed→summarizing·403→404)은 코드가 맞음. BE·FE 수정 재발주 + planner(work-001 Open Issue·can_edit_agendas). 다음: diff 한정 재검수. ~~코드 검수 1~~ · `reviewer_code` · 브리프 `sc-meeting-review-code-1-brief.md` · 산출물 `review-code-01-wp001-wp006-report.md` · 발주 2026-09-10. 코디 사전 관찰: FE `createAgenda` 가 `request<MeetingRecord>` 로 받는데 BE 계약은 `Agenda` 응답 — 검수 축 2 에서 잡힐 것.

- [x] **코드 검수 2 완료(2026-09-10) — PASS(WARN 5).** F1~F4 해소+회귀 테스트, D22·D19-3·D24 반영 확인. WARN 이월: N1 FE `reference` 타입 string→객체(WP-006 P3) · W9 `MeetingLine.author` nullable 로(WP-002/003 전) · W5 VersionConflict 422→409 · W6 CreateMeetingRequest extra=forbid. **커밋**: app `5751efa`(WP-001+WP-006 P1·2) · spec `a54c2e6e0`(SPEC 0.4.1+WP 6). push·PR 은 아직. ~~코드 검수 2~~ · `reviewer_code`(검수 1 세션) · 브리프 `sc-meeting-review-code-2-brief.md` · 산출물 `review-code-02-report.md` · 발주 2026-09-10. PASS 면 → WP-002 브리프.

- [~] **backend — WP-002 스트림 중계** · 브리프 `sc-meeting-be-wp002-brief.md` · **발주 2026-09-10 밤**(WP-001 세션 재사용). 코디 확정: WS 인증=세션 쿠키(첫 프레임 accessToken 없음, planner 환류) · close code 4401/4404/4409/1000 · 블록 경계 화자변경/300자/2초 · 이월 WARN W9·W5·W6 포함. 다음: FE Phase 3 병렬 발주.

- [~] **frontend — WP-006 Phase 3 스트림 화면** · 브리프 `sc-meeting-fe-p3-brief.md` · **발주 2026-09-10 밤**(WP-002 와 병렬, WS 모킹). 메모 쓰기 API(`POST …/agendas/{aid}/lines {text}`)는 WP-003 소유 — 코디가 계약 선정의, BE 에 WP-003 때 전달. 구 드로어·liveTranscription 삭제 포함.

- [ ] **backend — WP-003 메모 API + AI 배치** · 브리프 `sc-meeting-be-wp003-brief.md` **작성됨, 발주 대기(WP-002 완료 후 — 같은 backend/)**. 코디 확정: 메모 API `POST …/agendas/{aid}/lines {text}` · 트리거 잠정값 600자/안건 전환(80자)/90초 · MCP persona=만든 사람 · 도구 allowlist 레지스트리(task_list·project_list·meeting_get·member_list) · strict 출력 스키마 · 전량 교체·push.

- [ ] **backend — WP-004 합성·승격·내보내기** · 브리프 `sc-meeting-be-wp004-brief.md` **작성됨, 발주 대기(WP-003 뒤)**. 코디 확정: 줄 편집 = 안건 단위 덮어쓰기 하나(줄별 엔드포인트 없음, expected_last_saved_at 409) · 내보내기 HTML 만(pdf·docx 데모 범위 밖) · 승격 `POST …/todos/{todoId}/promote` · 제목 후보 `meetings.title_candidate` · finalize durable job · 세션 resume + 콜드 폴백. planner 정렬 지시.

- [x] **planner — 메모 API 주소·OQ-307/315 잠정값 · 줄 편집=안건 덮어쓰기 · 내보내기 HTML(R-35) · promote 경로·title_candidate** 반영 → 코디 커밋 **df4c93737**(통보 35건, 0.4.1 유지).
- **D25 (2026-09-10, 사용자)**: 화면을 만들며 DS 에 없는 부품은 **재사용 컴포넌트로 만들고 DS 에 올린다**(DS 지속 갱신). 백로그 `design/DS-backlog.md` · FE 완료 보고에 「DS 추가 후보」 표 필수 · 화면 WP 닫힌 뒤 designer 워커가 DS 프로젝트(8fa54d76)에 등록 → 참조본 갱신 커밋.

- [x] **frontend — WP-006 P3 스트림 화면** (task_f18c534a01fc) 완료 → 리포트 `report-fe-p3.md`. 코디 재현: tsc 0 · vitest meetings/ 39 통과(워커 보고 6파일 75). 오디오 = MediaRecorder webm/opus 16k mono 250ms. 삭제: liveTranscription·MeetingDrawer·옛 회의 api 11·타입 13. DS 부품 셋(Composer·GutterList·StatusNote) → DS-backlog. 임시 문구 6(OQ-311) → planner 일괄 통보 대기. 커밋은 WP-002 뒤 검수와 함께.
- **D26 (2026-09-10, 코디)**: FE 미결 해소 — `Line.at_ms`(memo 는 서버 경과 ms) · `GET /api/meetings/{id}/transcript`(끝난 뒤 스크립트 탭 원문, §5.4-7) · `can_write_memo` 게이트 → **WP-003 브리프 §3 에 추가**. BE WP-002 에 인계: 컨테이너 형식은 Soniox `audio_format=auto`(sample_rate 제외) · webm 청크 순서대로 이어 붙임. OQ-305 승계·ai.batch 모양은 WP-003 계약대로.

- [ ] **frontend — WP-006 P4 회의 뒤 배선** 브리프 `sc-meeting-fe-p4-brief.md` **작성됨, 발주 대기(WP-003·004 뒤)**. planner 반영 완료 → 코디 커밋 **37923ac03**(WP-006 Phase 4 10작업·10검증 · WP-003 계약 3건 · SPEC §5.4-7·§6·OQ-311 표).

- ⚠ 로컬 스택(`make local-stack`, 5176/8001) **내려감** — 백그라운드 재기동이 exit 2 로 종료(출력 없음, BE 워커가 backend/ 를 갈아엎는 중이라 예상 범위). WP-002 완료 뒤 `make reset-demo` → `make local-stack` 으로 다시 올린다.

- [x] **backend — WP-002 WS 중계** (task_5dbaa14cb00d) 완료 → `report-be-wp002.md`. 워커 254 통과 · 코디 재현 core+stream+arch **66 통과** · 코디 인계 둘(컨테이너→`audio_format=auto` · 청크 순서) 반영. 폐기 라우트 7·표 4 제거, `/api/materials/search` 회의 내용 일시 빠짐(WP-005 재건). W9 는 FE 몫(`author` null) → 검수 3 항목.
- **실물 e2e (2026-09-10, 로컬 스택, Soniox 키 없음)**: 4401(쿠키 없음·첫 프레임 없음) · 4404 · 4409 `invalid_meeting_status` · subscribe `ready{latestBatchSeq:0,speakerCount:0}` · upstream → `error{reason:"upstream"}`+1011 · `/end`→summarizing — **계약 전부 일치**. 스크립트 `scratchpad/ws_e2e.py`. ⚠ **실제 Soniox 전사는 미확인** — `~/.config/soniox/env` 없음(사용자 키 필요). 발견: MeetingDetail 에 `started_at` 없음 → WP-003 브리프 ③-b 로 추가.
- **커밋 806f52c** (app, WP-002 + FE P3). 스택 재기동됨(5176/8001).
- [ ] **backend — WP-003 메모+AI 배치** · **발주 2026-09-10 08:59** — task `task_0885e63cb8c0` · dispatch `ctx_b0ce4492fc81` · 워커 `term_50bcf0cc…`.
- [ ] **reviewer_code — 코드 검수 3 (WP-002+FE P3 차분, HEAD 기준)** · 브리프 `sc-meeting-review-code-3-brief.md` · **발주 2026-09-10 09:00** — task `task_c8957879602e` · dispatch `ctx_b87d1f146a43` · 워커 `term_9efe51f3…`. 산출물 `review-code-03-report.md`. **완료 — FAIL(F1 1건) + W9 미해소**. F1[BE]: upstream 역할에 소유자 게이트 없음(stream_service.py:134 · application.py stream_admission) → **WP-003 워커에 추가 지시**(D27). W9[FE]: `author: string` + personName null TypeError → **FE W9 완료 → 코디 커밋 **bfc9770**** — tsc 0 · vitest 41 통과 재현. 미결(author=member_id 원문 표시) → FE P4 브리프에 흡수. (`sc-meeting-fe-w9-brief.md` · task `task_3e82a5f11858` · dispatch `ctx_f99f19a1fbb3` · 워커 `term_1cf6a2f6…`). 나머지 1~8 PASS(프레임 계약 키 단위 일치 · e2e 관측 6 일치 · 폐기 잔존 0 · W5/W6 해소). 검수 재현: HEAD 격리본 66 통과 · FE 39 통과.
- **D27 (2026-09-10, 코디)**: subscribe = 참석자 + 공유받은 사람(현행·시안 가시성 표 허용) · upstream = 만든 사람만, 비소유 upstream → 4409 `not_meeting_owner`(오디오·provider 전).

- [ ] **reviewer_code — 코드 검수 4 (WP-003 차분 + F1)** 브리프 `sc-meeting-review-code-4-brief.md` **작성됨, WP-003 커밋 뒤 발주**(범위 `bfc9770..HEAD`).

- [x] **backend — WP-003 메모+AI 배치 (+검수 3 F1)** 완료 → `report-be-wp003.md`. 워커 213 통과 · 코디 재현 core+stream+memo/batch+mcp+arch **106 통과**. **실물 e2e 전부 일치**(scheduled 메모 409 · start 뒤 can_write_memo/started_at · 메모 201 at_ms · 빈 문자열 422 · 비소유 메모 404 · 비소유 upstream 4409 not_meeting_owner · 비소유 subscribe ready · transcript 200 · /end 뒤 409). **실제 Codex 웜스타트 성공** — `meeting_ai_sessions` 1행(시작 20초 뒤, persona yuna). 실제 배치 실행은 Soniox 전사가 있어야 트리거되므로 키 대기. 스크립트 `scratchpad/wp003_e2e.py`. **커밋 80dd097**. 스택 재기동됨.
- [ ] **reviewer_code — 코드 검수 4 (WP-003 차분 `bfc9770..HEAD`, 격리본 필수)** · **발주 2026-09-10** — task `task_eda0c7a4d9c2` · dispatch `ctx_52ee875a4042` · 워커 `term_9efe51f3…`. **완료 — FAIL(F-A 1건)**: 배치 출력 스키마가 provider 에 안 걸림(`AiConversationRequest` 스키마 자리 없음 · converse 경로 `--output-schema` 없음 · 지시문에 JSON 요구 없음 → 실물이면 매 배치 폐기). F1(검수 3)·W9 해소 확인 · 나머지 1~8 PASS · 격리본 90 통과. **F-A → WP-004 워커에 흡수 지시**(합성도 같은 통로) + W-b(실행 중 안건 전환 트리거 기억) + W-c(게이트 테스트 close code 단정). W-a(FE 가 at_ms·can_write_memo·started_at 미소비, 클라이언트 시계 계산) → FE P4 브리프. W-d(도구 필터가 CLI enabled_tools) 수용. **코디 할 일: WP-004 뒤 실제 Codex 배치 1회 확인**(Soniox 없으니 transcript 행을 직접 넣고 schedule 호출).
- [ ] **backend — WP-004 합성·승격·HTML 내보내기** · **발주 2026-09-10** — task `task_7d53256bfaf4` · dispatch `ctx_b9e30e5796ae` · 워커 `term_50bcf0cc…`. 검수 4 와 병렬(같은 트리, 커밋 금지).

- [ ] **reviewer_code — 코드 검수 5 (WP-004 차분 + F-A/W-b/W-c)** 브리프 `sc-meeting-review-code-5-brief.md` **작성됨, WP-004 커밋 뒤 발주**(범위 `80dd097..HEAD`). 사용자 질문(09:45): Codex 는 CLI 로그인(env 불필요, 현재 로그인됨) · Soniox 는 `~/.config/soniox/env` 의 `SONIOX_API_KEY` 필요 — 생성 방법 안내함.

- **Soniox 키 (2026-09-10 09:50, 사용자 「env 에 너가 넣어」)**: task_management 리포의 `.env` 에서 `SONIOX_API_KEY` 줄만 `~/.config/soniox/env`(600) 로 복사(값 미출력). ⚠ `make soniox-smoke` 는 WP-002 가 지운 `modules/meetings/transcription` 을 import 해 깨짐 → **이월: `backend/scripts/soniox_smoke.py` 새 어댑터로 고치거나 삭제(WP-005 또는 검수 5 WARN)**. 대신 실물 확인은 WS upstream 에 macOS `say` 합성 wav(16k mono)를 올려 확정 블록·배치까지 본다(`scratchpad/speech.wav`).

- **실물 Soniox + Codex 배치 (2026-09-10 10:00~)**: 어댑터 직결 프로브 — 40초 한국어 합성 wav 로 확정 토큰 232개, end frame 뒤 finished 정상. 릴레이 경로 — 확정 블록 적재(300자 경계, evidence 905~34985ms) → 메모 → `agenda_switch` 배치 **succeeded** → **AI 트랙 줄 5개**(안건 A 2 · B 3, 근거 구간 결박) — **실제 Codex 배치 1회 확인**(F-A 전 코드인데도 JSON 을 냈다 — F-A 는 견고성 수정으로 유지). **업스트림 끊김 원인 = Soniox 무음 20초 idle → 오류 408**(audio 멈춘 뒤 정확히 20초, 프로브·릴레이 둘 다 재현). 브라우저 MediaRecorder 는 무음도 보내므로 데모 영향은 낮으나 **이월: 오디오가 N초 없으면 Soniox keepalive 프레임 전송(WP-005 또는 검수 5 WARN)**. 테스트 하네스 주의: wav 는 길이 헤더가 있어 `auto` 에서 Soniox 가 끝을 알 수 있음 → 릴레이 e2e 는 raw pcm_s16le 로(`scratchpad/speech.pcm`).

- **실물 e2e 발견 → BE 후속 브리프 `sc-meeting-be-wp002-fix-brief.md` 작성(WP-004 뒤 발주)**: **E1 종료 드레인 누락**(end frame 뒤 `finished` 까지 안 받아 마지막 ~6초·150자 유실 — 3회 모두 280자 블록 하나만 적재, 정상 `/end` 회의 포함) · **E2 Soniox idle 408**(무음 20초 → keepalive 필요) · **E3 soniox_smoke.py 깨짐**. 경계 규칙(300자)은 정상. 정상 종료 e2e(`a1fa7f1e…`): `/end` → 1000 `meeting_ended` → **WP-004 워킹트리 코드가 실제 Codex 합성으로 done + final 줄 1개** 생성(미커밋 코드 미리보기) — 배치는 `/end` 6초 전 메모라 미발행(정상).

- [x] **backend — WP-004 합성·승격·내보내기 (+F-A·W-b·W-c)** 완료 → `report-be-wp004.md`. 워커 305 통과 · 코디 재현 169 통과(회의+work 회귀+arch). **실물 e2e(실제 Codex)**: /end→30초 뒤 done · title_candidate · final 2+4 · todos 2+2 · export html · pdf 422 · promote 자기 201 / 참석자 교차 조직 422(→E4) · PATCH stale 409/fresh 200 · finalize 게이트 409. **커밋 8397d8f**. 스택 재기동됨.
- **D29 (코디)**: 회의 승격은 assignee 가 그 회의 참석자면 조직 경계 무관 eligible. **D30 (코디)**: 팀장 역할에 `work_request.create` 부여(시드). export 미지원 format 422(400 아님). planner 에 §8-10·§9·§8.2(기준일)·R-36·R-37 지시.
- [ ] **reviewer_code — 코드 검수 5 (WP-004 차분 `80dd097..8397d8f`)** · **발주 2026-09-10 10:20** — task `task_4f71fc4607ba` · dispatch `ctx_7c438f33a206` · 워커 `term_9efe51f3…`. **완료 — PASS(WARN 3)**: F-A·W-b·W-c 해소 확인 · e2e 관측 13/13 일치. W-1(422 vs 브리프 400) → 422 로 확정·planner 정렬 완료 → 닫힘 · W-a → FE P4 진행 중 · W-d 기록만. `review-code-05-report.md`.
- [ ] **frontend — WP-006 P4 회의 뒤 화면 배선** · **발주 2026-09-10 10:20** — task `task_829761dc0be9` · dispatch `ctx_2734dd3bc656` · 워커 `term_1cf6a2f6…`. **완료 → 코디 커밋 9644e7c** — tsc 0 · vitest 97 통과(회의 51 + 드로어 영향 5파일 46) 재현. [다시 시도]가 endMeeting 을 부르던 버그 수정 포함. 미결: ① 시각 눈금(경과 mm:ss vs 시안 벽시계) — 코디 결정 필요 ② ai.batch 모양 실물 확인 ③ 승격 422 배너(E4 뒤 해소) ④ 자료·공유 WP-005. 임시 문구 3(savedElsewhere·alreadyRequested·titleCandidate) → planner 일괄. 리포트 `report-fe-p4.md`.
- [ ] **backend — WP-002/004 후속 E1~E6**(드레인·keepalive·스모크·참석자 배정 D29·기준일·팀장 권한 D30) · **발주 2026-09-10 10:20** — task `task_d7f2d312f245` · dispatch `ctx_58ecdb0b4f86` · 워커 `term_50bcf0cc…`. 셋 병렬(같은 트리: reviewer 격리본 · FE frontend/ · BE backend/).
- [x] planner — §8-10 422 · §9-5 D29 · §8.2 기준일 · R-36/R-37(SPEC-001 소유 통보, §12 머리에 소유자 표시) · WP-004 Pre-deploy 선행 조건 · 10-decision D29/D30 → 코디 커밋 **4963c6e76**(통보 37건, 0.4.1).

- [ ] **backend — WP-005 자료·공유·전사 검색 다리** 브리프 `sc-meeting-be-wp005-brief.md` **작성됨, BE 후속(E1~E6) 커밋 뒤 발주**. 코디 결정: 공유 경로는 WP-001 의 `/shares` 유지(`/viewers` 아님) + `GET /shares`(basis attendee|share) · 자료는 업무 자료 결(multipart 다중, `{attached, failed[{name,reason}]}`, in_progress 409) · 검색 갈래 `meeting_transcript`(회의당 하나, 열람=참석·공유).

- [x] **backend — 후속 E1~E6** 완료 → `report-be-followup.md`. 워커 282 통과 · 코디 재현 135 통과. **실물 재확인**: E1 드레인 — transcript 2블록(301자 + 꼬리 34자, 41.4초까지) ✓ · E4 참석자(hyeon) 승격 **201** + work_requests 출처 두 열 ✓ · E5 due `2026-09-17/09-11/09-15` ✓, 스탬프에 제목 후보 ✓ · 중복 승격 409 · 승격된 것 삭제 409. **커밋 96d5312**. 덤: 드레인 취소 시 열린 블록 유실 경로도 막힘(finally flush).
- **화면 실물(playwright, 2026-09-10 19:35)**: 목록·패널·상세·스크립트 정상. **결함 1**: 근거 칩 「NaN:NaN」 — BE evidence 키 `from_ms/to_ms` vs 계약 `start_ms/end_ms` → WP-005 브리프 §0 선행으로. **D31 (코디)**: 시각 눈금은 시안대로 벽시계 HH:MM(started_at + at_ms) → FE 소수정 브리프 `sc-meeting-fe-p4-fix-brief.md`. 스크린샷 `scratchpad/p4-*.png` 사용자 전송.

- [ ] **backend — WP-005 자료·공유·전사 검색 다리 (+§0 evidence 키 투영)** · **발주 2026-09-10 19:40** — task `task_c4142254719b` · dispatch `ctx_8bf933e3d0ec` · 워커 `term_50bcf0cc…`.
- [ ] **frontend — P4 소수정(D31 벽시계·NaN 가드)** · **발주 2026-09-10 19:40** — task `task_03234d70b354` · dispatch `ctx_c5084216bfe6` · 워커 `term_1cf6a2f6…`. **완료 → 코디 커밋 ad4da8a** — tsc 0 · vitest 52 통과 재현. 미결: 분 단위 눈금(시안도 분) · 「담당 비움」 테스트 간헐 흔들림(Select 팝오버 타이밍, 기록만).

- [ ] 브리프 작성됨·발주 대기: **FE P5 자료·공유 배선** `sc-meeting-fe-p5-brief.md`(WP-005 커밋 뒤) · **코드 검수 6** `sc-meeting-review-code-6-brief.md`(WP-005·FE 소수정 커밋 뒤, 범위 8397d8f..HEAD, P5 와 병렬).

- [x] **backend — WP-005 자료·공유·검색 다리 (+§0 evidence 키)** 완료 → `report-be-wp005.md`. 워커 216 통과 · 코디 재현 132 통과. **실물 e2e 전부 일치**(혼합 업로드 201/부분 실패 사유 · 전부 실패 422 · 진행 중 409 · content · shares basis · 참석자 삭제 409 · 열람자 shared·조작 불가 · 검색 소유자/열람자 히트 · evidence `start_ms/end_ms`). 덤: 검색의 회의 열람 축 불일치(공유받은 사람 누락) 수정. **커밋 59e1102**. ⚠ FE 영향: `POST /shares` body `{member_ids}`·응답 목록 → FE P5 브리프에 반영.

- [ ] **frontend — WP-006 P5 자료·공유 배선** · **발주 2026-09-10 20:20** — task `task_ed1dbb626e21` · dispatch `ctx_cecbe8246448` · 워커 `term_1cf6a2f6…`. **완료 → 코디 커밋 eda908e** — tsc 0 · vitest 85 통과 재현. DS 부품 DropZone·FileList 추가(DS-11·12). 미결 ①②(can_detach·shares 삭제 응답) → BE 소수정 발주 · ③ T02 문구 → planner 통보 R-38 · ④ 클라이언트 사전 판정 중복 — 기록만. 리포트 `report-fe-p5.md`.
- [ ] **reviewer_code — 코드 검수 6 (`8397d8f..59e1102`)** · **발주 2026-09-10 20:20** — task `task_71063a4d193c` · dispatch `ctx_9097210cc615` · 워커 `term_9efe51f3…`. **완료 — PASS(WARN 4), 재발주 없음**: NaN 뿌리 한 자리 · E1 드레인 finally · E4/E6 계약 무영향 · keepalive 경합 없음 · 스모크 키 미노출 · W-a 해소 확인. 격리본 BE 198 · FE tsc 0 · vitest 52. **W-2(신규)** MeetingLive.test.tsx socket() 헬퍼 타이밍 간헐 실패(7회 중 2회) → FE P5 소수정 브리프에 흡수(`sc-meeting-fe-p5-fix-brief.md`, BE 소수정 뒤 발주) · W-1 422 확정으로 닫힘 · W-d 기록. `review-code-06-report.md`.

- [ ] **backend — WP-005 소수정(can_detach · shares 삭제 응답 목록)** · **발주 2026-09-10 20:45** — task `task_eabdc9c38402` · dispatch `ctx_1822ab739b5c` · 워커 `term_50bcf0cc…`. **완료 → 코디 커밋 cbb4799**(64 통과 재현). FE P5 소수정 발주(can_detach·shares 응답·W-2). planner R-38·OQ-311 키 셋 반영 → 코디 커밋 **51d05d878**(통보 38건).

- [ ] **frontend — P5 소수정(can_detach·shares 응답·W-2)** · **발주 2026-09-10 20:55** — task `task_26f8b1622758` · dispatch `ctx_f6fc735fbdfc` · 워커 `term_1cf6a2f6…`. **완료 → 코디 커밋 16d249c**(tsc 0 · 61 통과 ×2). 워커 셋 전부 유휴.
- **브라우저 라이브 e2e 1차(playwright 가짜 마이크 wav → MediaRecorder webm/opus, 20:15)**: 상태 줄 「연결하는 중」에서 멈춤 · 스크립트 비어 있음 · `/end` 뒤 정리 중 2분 넘게 지속 — **원인: vite 프록시 문자열형이라 WS 업그레이드 미전달**(서버 WS 접속 0건, transcript 0). 회의는 뒤늦게 done(합성은 됨). → FE 소수정 `sc-meeting-fe-ws-proxy-brief.md` 발주(ws:true + ready 전 닫힘 끊김 표시).

- [ ] **frontend — vite WS 프록시(ws:true)·ready 전 닫힘 끊김 표시** · **발주 2026-09-10 21:25** — task `task_d9ca3f11f303` · dispatch `ctx_e00f290d5939` · 워커 `term_1cf6a2f6…`. 완료 뒤 브라우저 라이브 e2e 재실행(`frontend/shot_live.mjs`).

- [x] **frontend — vite WS 프록시** 완료 → 코디 커밋 **2285277**(tsc 0 · 62 통과). **브라우저 라이브 e2e 2차(20:23)**: WS 접속 1건 · **webm/opus → Soniox 전사 4블록(301·300·300·51자, 116초, 가짜 마이크가 wav 를 반복)** · `/end` 25초 뒤 서버 done(finalize job completed). **결함 3**: ① quick-start 가 `launch_warm_start` 를 안 불러 AI 세션 없음 → 배치 0 ② quick-start 회의 안건 0 → 메모 못 던짐 ③ 화면이 정리 중 동안 폴링 없음(150초+ 스켈레톤). → **D32**(바로 시작은 기본 안건 「안건 1」) · 정리 중 폴링 5초(잠정). BE 브리프 `sc-meeting-be-quickstart-brief.md` · FE 브리프 `sc-meeting-fe-summarizing-poll-brief.md` 발주. planner D32(§3.1-6·§4.1-6, 출처 「직접 입력」)·폴링(§5.1, OQ-317) 반영 → 코디 커밋 **6c1de4ed7**.

- [ ] **backend — quick-start 웜스타트·기본 안건(D32)** · task `task_492b02467c63` · dispatch `ctx_a4c5fe5cda15` · **frontend — 정리 중 폴링** · task `task_1e967bb51a6c` · dispatch `ctx_fd3da0008fbf` · **발주 2026-09-10 21:45** → FE **완료·코디 커밋 f463f5d**(tsc 0 · 63 통과). BE 완료 → 코디 커밋 **20723a7**(74 통과). ⚠ `make local-stack` 의 API 는 --reload 없음 — 코드 바뀌면 스택 재기동 필수(3차 e2e 실패 원인). 라이브 e2e 3차 재실행 중. 완료 뒤 브라우저 라이브 e2e 3차.

- **브라우저 라이브 e2e 3차(20:37, 스택 재기동 뒤)**: 바로 시작 → 기본 안건 「안건 1」 → 전사 3블록(스크립트 탭 벽시계 눈금) → 메모 1 → **웜스타트 세션 + 배치 1회 성공(AI 가 안건 「온보딩 자료」 신설, ai 줄 3) → AI 요약 탭 표시** ✓. **결함 2**: ① 합성 `commit_finalized` **IntegrityError**(AI 안건에 ai 줄이 매달린 채 안건 교체 → FK 위반) ② 실패한 잡이 completed 로 닫혀 회의가 summarizing 에 갇힘(failed 전이·failure_reason 없음) → BE 브리프 `sc-meeting-be-finalize-fk-brief.md`(로그 `live-e2e-3-finalize-error.log`) ③ 안건 번호가 order 값(0부터) → FE 브리프 `sc-meeting-fe-agenda-number-brief.md`. 스크린샷 `live-4-ai.png` 사용자 전송.

- [ ] **backend — 합성 FK·실패 전이** task `task_72218935b1b3` · dispatch `ctx_a96673d53340` · **frontend — 안건 번호** task `task_9769514f8f2b` · dispatch `ctx_f0cab5f4fb76` · **발주 2026-09-10 22:05** → FE **완료·코디 커밋 08f6381**(64 통과 ×3, 담당 비움 테스트 흔들림도 원인 잡음). BE 진행 중. 완료 뒤 스택 재기동(--reload 없음) → 라이브 e2e 4차.

- [x] **backend — 합성 FK·실패 전이** 완료 → 코디 커밋 **1925a76**(86 통과 재현; 워커 114). 원인: replace_track 삭제 순서 + commit_success 가 try 밖 + 워커가 예외를 completed 로. 메모 달린 AI 안건은 보존(코디 채택, 디테일 목록). **브라우저 라이브 e2e 4차(1925a76 스택)**: 바로 시작 → 전사 → 메모 → 배치 1 succeeded → `/end` → **done**(제목 후보 「신규 채용 일정 및 온보딩 자료 논의」 · final 4 · todos 4 · job completed attempt 1) — **1차 파이프라인 끝까지 실물 통과**. 스크린샷 `live-6-done.png`. shot 스크립트는 scratchpad 로 이동(리포 clean).

- **1차 완성 (2026-09-10 22:30, 사용자 「일단 1차적으로 완성하고 디테일을 잡자」)**: **PR 앱 https://github.com/MediSolveAIDev/ax-workspace/pull/5**(kknaksss/sc-meeting → main, 커밋 17, HEAD 1925a76) · **PR 스펙 https://github.com/MediSolveAIDev/mediness/pull/719**(kknaksss/sc-meeting-spec → main, 커밋 8, HEAD 6c1de4ed7). 워커 셋(backend·frontend·reviewer)·planner 유휴. 디테일은 `잔여-디테일.md`. 다음: 사용자 리뷰 → 머지 → `archive-work.sh` 마감.

- **2026-09-11 디자인 수정 라운드 시작(사용자)**: 페이지별로 하나씩. 첫 대상 회의록(목록) 페이지. 절차 = 사용자 내용 → `design/피드백-회의록.md` 에 기록만 → 「수정 시작하자」 신호 뒤 시안(designer 워커)·코드(frontend 워커) 발주. PR #5·#719 는 OPEN 유지.

- [ ] **조사 2 — 업무 기획안 v1.2.0(plan-001·screen-004, mediness 313ae36) ↔ 우리 차이** · reviewer_code read-only · 브리프 `sc-meeting-survey-plan001-brief.md` · **발주 2026-09-11** · 산출물 `survey-02-plan001-v120-report.md`. 사용자: 「이거 보고 다음에 회의목록에서 화면만 읽어오자 — 이게 최종이라 우리랑 조금 다를 수 있어」. 디자인 피드백 12건은 `design/피드백-회의록.md`(기록만, 「수정 시작하자」 대기).

- [x] **조사 2 완료** → `survey-02-plan001-v120-report.md`. 핵심: 313ae36 에 plan-004·screen-005 도 포함 — **우리가 9/9 판으로 이미 반영한 것**(새 내용 아님, §12 통보 미반영, 시안이 앞섬). **MOD-101 v1.2.0 = 내용(한 줄 200자)·기한·승인자, 담당 칸 삭제(「담당은 늘 나」)·요청/수락 게이트 제외·권한 어휘 관리자/구성원 → 우리 승격(담당 고르기·description·checklist·업무 요청)과 정면 충돌** — 회의실 페이지 차례에 결정. 회의 업무는 수신함에 안 서고 업무 상세 출처 구획(E19)에.
- [ ] **디자인 수정 라운드 1 — 회의록 페이지 12건 발주(2026-09-11)**: designer(시안 v3, `sc-meeting-design-list-v3-brief.md`, 워커 `term_70f0f1a7…`) · frontend(`sc-meeting-fe-list-v3-brief.md`, 워커 `term_1cf6a2f6…`) 병렬. **둘 다 완료** — FE: tsc 0 · 143 통과(부품 4종 포함) · 코디 실물 확인(패널 높이·3단·공용 부품·버튼 하나 ✓, 네이티브 select/date 0) → **커밋 61f915b**. designer: `회의록.dc.html` v3(원본 .v2) + `REPORT-회의록-v3.md`(DS 후보 Select·TimeField → DS-13). 후속 2건(텍스트 입력 파란 포커스 링=항목 5 미해소 · FAB 가 패널 푸터 가림=항목 13) → `sc-meeting-fe-list-v3-fix-brief.md` 발주.

- [x] **회의록 페이지 라운드 1 마감(2026-09-11)**: 피드백 13건 전부 반영 — FE 커밋 61f915b + **83e3d69**(전역 포커스 테두리 없음·FAB 겹침·항목 6 두 줄), 시안 v3(designer, 항목 6 정정 포함), 스펙 R-39~R-44 **aadd03d4**. 실물 확인 스크린샷 `v3b-*.png` 전송. PR #5·#719 브랜치에 push 는 아직(FE 커밋 2개 로컬).

- **D33 (2026-09-11, 사용자)**: 회의실 예약(THE CONNECT)을 데모 범위 안으로 — 서버가 env 계정(`~/.config/theconnect/env`, TDL_EMAIL/TDL_PASSWORD, mediness-app back/.env 에서 복사·값 미출력)으로 로그인해 예약 · 사내 참석자=회사 계정 · 사외=외부인 등록. **WP-007 발주** `sc-meeting-be-wp007-theconnect-brief.md`(backend, 조사 포함) · planner 완료 → **SPEC 0.4.2** · WP-007(SCAX-DOC-20) 신설 · R-45(R-33 취소선) · 10-decision 갱신 → 코디 커밋 **ddda69ee**(push).

- [ ] **조사 3 — 회의 기획 v1.1.0(plan-004·screen-005, cbc9712 ← 868ebaf) ↔ 우리** · reviewer read-only · `sc-meeting-survey-plan004-v110-brief.md` · **발주 2026-09-11** · 산출물 `survey-03-plan004-v110-report.md`. 사용자 「잘못 줬다 — 이거 발주해서 조사」(조사 2 는 v1.0.0 이었음). 기획자 변경 요지: 반복 제외 · 항목별 발화 시각 · **상태 5(정리 중 제거)** · 목록 「진행 중」 구획 · 메뉴 두 묶음 · 삭제/공유/자료 삭제 시점 · [회의만 생성]/[회의실까지 예약] · 「회의명」·「회의」 · 미리보기 형식 · 확인 셋(반복·발화 시각·회의실 자동 대체).

- [x] **조사 3 완료** → `survey-03-plan004-v110-report.md`. 313ae36·cbc9712 는 평행 PR. v1.1.0 이 우리 통보를 처음 받은 판: 받아들임 9 · 반대 6(R-1 두 트랙·R-16·R-18·R-34·R-41·R-45) · 무응답 10(R-2 Soniox 중계가 가장 무거움). 새 요구 셋(회의실 자동 대체·미리보기 4종·같은 요일 다음 날짜). **D34 (코디 기본값, 2026-09-11)**: 서버 상태 여섯 유지+화면 어휘 다섯(「종료」, 정리 중=로딩) · 두 트랙 유지(재통보) · 항목=줄+우측 시각 · 목록 「진행 중」 구획 · 공유 끝난 뒤만 · 자료 떼기 예정만 · [회의 생성] 하나 유지 · 가능 판정/자동 대체 1차 안 함 · 미리보기 PDF·MD 유지 · 「회의명」·「회의」 · 같은 요일 다음 날짜. planner 완료 → **SPEC 0.4.3**(D34, R-46, R-25 닫힘, 재통보 표시) → 코디 커밋 **7a3e49b7**(push). 화면·코드 변경분은 `피드백-회의록.md` 14~16(라운드 2)과 회의실 페이지 라운드로 — 사용자 「수정 시작」 대기.

- [x] **backend — WP-007 THE CONNECT 예약** 완료 → `report-be-wp007.md`. 조사 사실: 외부인 등록 API 없음(사외는 attendees 표시 문자열 폴백) · 계정 매핑 이메일→이름(데모는 이름 축) · 공용 회의실 id 1~7 · company_id 3. 워커 62 통과 · 코디 재현 62. **실물 왕복 성공**: rooms 7개 → 회의실 2 예약 booked(location 채움) → 회의 취소 → 예약 cancelled 동기. 스키마 `meetings.room_reservation` ALTER(sync-demo-schema). **커밋 d0d5e32 push**. 미결: 회의실 나중에 바꾸기 없음(PATCH 에 room_id 없음, 취소 후 재생성) · 예약 실패 시 최대 20초 대기 · env `~/.config/theconnect/env`(Makefile THECONNECT_ENV_FILE).
- [x] **frontend — WP-007 P3 회의실 배선** 완료 → 코디 커밋 **e740f32**(push) — tsc 0 · 72 통과 · 실물 모달에 실제 회의실 7개 + 「선택 안 함」 확인. 임시 문구 4(예약 실패 사유) → OQ 통보 대기. **회의실 예약 기능 끝까지 연결됨.** 워커 전부 유휴.

- **D35 (사용자, 09-11)**: 승격 = 업무 요청 유지, 「요청됨」 유지(R-18 재통보). **D36 (사용자, 09-11)**: 회의실 자동 대체(정원≥인원 중 가장 작은 방) + 토스트 「회의실 N 으로 예약됐습니다」 · 대체 불가면 **회의 생성 실패**(409 room_unavailable + available_rooms) 토스트 후 모달 유지·입력값 유지·회의실만 재렌더 · `GET /rooms?starts_at&ends_at` 시간대 조회. → BE `sc-meeting-be-wp007-fallback-brief.md` · FE `sc-meeting-fe-rooms-fallback-brief.md` 병렬 발주 · planner §3.1-10·WP-007·R-45/46 취소선 지시.

- **D37 (사용자, 09-11)**: 자료 미리보기 데모 제외(행 클릭 → 새 탭). planner 지시(0.4.4 묶음). FE 브리프 `sc-meeting-fe-no-preview-brief.md` **작성됨 — FE 가 회의실 대체 작업 중이라 그 완료 뒤 발주**.

- [x] FE 회의실 대체·거절 처리 완료 → **82af0b1**(75 통과). planner D35·D36·D37 → **SPEC 0.4.4** 코디 커밋 **98df94f2**(push). FE 미리보기 제외(D37) 발주 `task_10f702832917`. BE 자동 대체 진행 중.

- [x] FE 미리보기 제외(D37) 완료 → **5d3eda9**(75 통과). MaterialDrawer 삭제, 행 클릭 = 새 탭.

- **D38 (사용자, 09-11)**: 안건 출처 = 기획 넷(직접 입력·세트·지난 회의에서 넘어옴·다른 회의에서 파생) + AI 정리 = 다섯 값. set·derived 는 값만 열어 둠(만드는 경로는 범위 밖). BE 큐(자동 대체 뒤) · FE `sc-meeting-fe-agenda-source-brief.md` 발주 · planner §4.1-2·R-19 취소선·R-47 지시.

- **D38 정정 + D39 (사용자, 09-11)**: 출처 종류는 기획 넷만(AI 정리는 「AI 가 세웠다」 표시, 종류 아님) · 데모 생성 경로는 직접·지난 회의 둘 · 세트·파생은 개념만. R-40 선택 안 함 확정. **D39 내보내기 = HTML 유지 + 주제 스레드형 페이지 조판** → designer 템플릿 발주 `sc-meeting-design-export-brief.md`(참고 이미지 `design/ref-export-thread-style.png`) → 뒤에 BE export.py 이식. FE 출처 라벨 커밋(아래).

- [x] planner D38 정정·R-36/37·R-40·D39 → 코디 커밋 **61ea571a**(push). FE 출처 라벨 커밋 **ab1dffc**(5 라벨은 무해 — AI 정리는 표시로 남음). 진행 중: BE 자동 대체(+inline·출처 값), designer 내보내기 템플릿.

- **D38 재정정 (사용자, 09-11)**: 출처 종류 다섯(AI 정리 포함). **D40 (사용자, 09-11)**: 승격 업무 요청의 요청자 = 시스템(회의), 누른 사람 = promoted_by + cc, 담당 후보 조직 경계 없음(D29·R-36 불필요) — 업무 상세 요청자 표시 「회의 · {회의명}」은 SPEC-001 쪽 통보 R-48. planner 지시 완료 · BE 브리프 `sc-meeting-be-system-requester-brief.md` **작성됨, 자동 대체 완료 뒤 발주**. FE 라벨은 이미 다섯(ab1dffc).

- [x] **BE 회의실 자동 대체·거절·시간대 조회 + 자료 inline** 완료 → **e297e1e**(90 통과, push). **실물**: 같은 방 재예약 → 회의실 6 으로 대체(replaced·requested_room_name) · 전부 찬 시간 → 409 room_unavailable + available_rooms [] · 정리 후 7 복구. FE 는 82af0b1 로 이미 배선. **SPEC 0.4.5**(D38 다섯·D40) 커밋·push. **BE D40·D38 발주**(`sc-meeting-be-system-requester-brief.md`). designer 내보내기 템플릿 완료 → `design/export-thread-template.html`(17KB) · `report-designer-export.md` — BE 이식은 D40 뒤.

- [x] FE 목록 패널 내부 스크롤(항목 17) → **51ec0aa**(push). 실측: 회의 20건에서 문서 높이 == 뷰포트(1130). 진행 중: BE D40.

- [x] FE 날짜 칸 아이콘 안쪽(항목 18) → **54a4287**(push, 121 통과). 미결: inline 변형은 타이핑 불가(달력으로만). designer 시안 같은 자리 진행 중. **회의실 페이지 라운드 시작**: `design/피드백-회의실.md`(A 반영만 남은 10 · B 결정 5 · C 사용자 피드백 수집 중) — 모아서 한 번에 발주.

- [x] **BE D40 시스템 요청자** 완료 → **d939dae**(push, 88 재현·워커 164, work 회귀 0). 스키마 `work_requests.promoted_by_member_id` ALTER. **실물**: promote → requester_id `system:meeting`·requester_kind system·promoted_by yuna·cc [yuna]·source_meeting_title. 미결: withdraw HTTP 표면 없음 · graph person:system 노드(→ 내보내기 발주에 덤으로) · FE 업무 화면의 요청자 표시 「회의 · 회의명」(SCR-102 쪽, 나중).
- [ ] **BE 내보내기 스레드형 이식(D39)** `sc-meeting-be-export-template-brief.md` **발주 2026-09-11**.

- [x] **BE 내보내기 스레드형 이식(D39)** 워커 완료 → `report-be-export.md`(71 통과 · 템플릿 `modules/meetings/templates/export_thread.html` · 조각 렌더러 · 서버 장 나눔·쪽 번호 · 요약 자리 = purpose · graph 시스템 행위자 제외). **⚠ 미커밋·미재기동 — 사용자 「일단 기록만」(화면 사용 중)**. 다음: 사용자 신호 → 검증 재현 → 커밋 → 스택 재기동 → 실물 내보내기 렌더 확인 → push. 미결(코디): 요약 자리(합성 요약 필드 없음) · 장 나눔 추정치 · 큰 안건 분할 규칙 · Chrome 인쇄 눈 확인.
- 사용자 실물 확인(09-11): 자료 클릭 새 탭으로 열리긴 하나 **「드로어 떠야 해」 — D37 을 코디가 넓게 읽은 것. 정정 기록(피드백-회의실 C1): 드로어 미리보기(PDF·MD) 복원, 데모 밖은 기획의 4종·조작만**. 회의실 라운드 발주 때 FE 되돌림 + planner 문서 정정.

- [ ] **회의실 페이지 라운드 발주(2026-09-11)**: FE `sc-meeting-fe-detail-v3-brief.md`(A1~A10 + C1 드로어 복원·C2 공유 진행 중 없음·C3 스크립트 메모 제외) · designer(회의록 세션이 회의실.dc.html 도 맡음 — designer-2 세션 없음) `sc-meeting-design-detail-v3-brief.md` task `task_ea68704da7b9` · BE `sc-meeting-be-detail-v3-brief.md`(A4 떼기 예정만, 내보내기 미커밋분 위에) · planner D37 정정+C3. C4 조직도 버그는 b61ba47. **사용자: 전체 다시 볼 때 백엔드 올릴 것(내보내기 이식 반영)**.

- [x] designer 회의실 시안 v3 완료(A1~A6·C2·C3, C1·B4·B5 확인, C4 픽스처 보강) → `회의실.dc.html`(원본 .v2) · `REPORT-회의실-v3.md`. 미결 셋(출처 다섯 픽스처·.share-table·ats 수) 소수정 지시. 스펙 D37 정정·메모 분리 커밋 475e7e3e.

- [x] FE 회의실 v3 완료 → 코디 커밋 **62be71b**(tsc 0 · 104 통과). BE 회의실 v3(A4)·designer 미결 진행 중. **미커밋 BE 내보내기분 + A4 는 BE 완료 뒤 한 커밋** · 백엔드 재기동은 사용자 신호 때.

- [x] BE 회의실 v3(A4 떼기 예정만, attach 는 그대로) + 내보내기 이식분 → 한 커밋 **b0cf1b9**(push, 워커 91·코디 materials+arch 재현). **백엔드 재기동 아직 안 함(사용자 신호 대기) — 내보내기 양식·떼기 규칙은 재기동 뒤 반영.** designer 미결 셋 진행 중.

- [x] designer 회의실 v3 미결 셋 완료(출처 다섯 픽스처·.share-table 정의·ats 정합 + A2 진행 중 쪽 보강). **회의실 라운드 1 전부 반영**(FE 62be71b · BE b0cf1b9 · 시안 v3 · 스펙 475e7e3e). 워커 전부 유휴. 대기: 사용자 전체 점검 → 백엔드 재기동.

- 스택 메모리 부족으로 또 종료 → 최신 커밋(b0cf1b9)으로 재기동(2026-09-11). 실물 내보내기 200(스레드 마크업·@page 포함) → `scratchpad/export-real.{html,png,pdf}`.

- **PR 본문 갱신(2026-09-11)**: 앱 #5(커밋 32, 119파일) · 스펙 #719(커밋 16, SPEC 0.4.5) — WP-007·D33~D40·디자인 라운드 반영. 두 PR OPEN, 브랜치 최신 push(앱 ab8a8ef · 스펙 475e7e3e). 다음: 사용자 리뷰 → 머지 → archive-work.sh.

- **D41~D43 (사용자, 09-11)**: 참여자는 웹소켓 없이 폴링(두 탭 읽기 전용) · 종료 합성 = 재료로 새로 쓰기(사람 안건 보존 검사 삭제) · 실패 사유 사람 말. **발주**: FE `sc-meeting-fe-participant-brief.md`(참여자 폴링·구독 폴백 제거·스크립트 세 칸) · BE `sc-meeting-be-finalize-rewrite-brief.md` · planner 0.4.6. 다음 테스트: 유나·지호 회의(참석자 둘) → 끝나면 다른 사람에게 공유. **사용자 신호 때 실행, 화면 같이 봄.** 그 전엔 아무것도 실행하지 않음.

- **D41 정정 (사용자, 09-11)**: 참여자 폴링은 코디 오독. 참여자 = 같은 WS 에 subscribe(읽기 전용)로 붙어 확정·잠정·AI 요약·메모(memo.line 신규)·종료를 실시간 push. 스크립트 세 칸 한 줄은 유지. FE `sc-meeting-fe-participant-ws-brief.md` 발주 · BE 에 memo.line broadcast + partial 전체 송출 큐 · planner 정정.

- [x] **FE 참여자 WS 구독·스크립트 세 칸·memo.line** → **57a4925** · **BE 합성 재작성(D42/43)·memo.line·partial 송출** → **ada1aa9** · 스펙 0.4.6.

- **D44 (사용자, 09-11)**: 실시간 전사는 회의 중 표시용, **종료 시 원본 음원 전체를 Soniox 비동기(stt-async-v5)로 재전사(화자 분리)해 원문을 갈아 끼우고 그 위에서 합성**(task-management 원형 복원). BE `sc-meeting-be-final-transcribe-brief.md` task `task_6ec3d363ce05`.
- **D45 (사용자, 09-11)**: 회의 중 주최자가 「+ 새 안건」으로 안건 추가(메모에서). 방 전체에 `agenda.added{agenda}`. FE `sc-meeting-live-agenda-brief.md` → **b6fc76d**(108 통과) · BE 같은 브리프(터미널 메시지로 큐) · 스펙 0.4.7 **64601f7c**(push).
- [x] **BE D44+D45 완료(09-11)** — 워커 153 통과(446s). 신규 `modules/meetings/retranscribe.py`(포트·상수·REALTIME_NOTICE) · `platform/soniox.py` SonioxFileTranscriber(업로드→transcriptions→폴링 5s/상한 1200s→transcript) · finalize 파이프라인 ①재전사(원문 전량 교체, base_ms 보정, 실패 넷은 실시간 유지)→②합성 · `meetings.transcript_source`(final|realtime, sync-demo-schema 적용됨) · 상세에 `transcript_source`·`can_add_agenda` · POST /agendas in_progress 주최자 허용(편집·삭제 409 유지) · `agenda.added` broadcast(FE 가정 모양과 일치 확인). TEST 프로필은 실물 transcriber None. **미결(워커)**: ① 재전사 context 힌트 미탑재 ② 폴링·상한 상수(env 아님) ③ **finalize lease 600s < 재전사 상한 1200s — 긴 음원이면 다른 워커가 다시 집어 재전사 2회 가능**(env `AX_MEETING_FINALIZE_LEASE_SECONDS` 로 올릴 수 있음, 사용자 결정 대기). 앱 .gitignore 잡음(charty reference 줄) 되돌림.

- **스펙 PR #719 스쿼시 머지 완료(2026-09-12 12:24Z)** → mediness main **8c8cae5e**. 직전 main 머지(충돌 3, planner) 92cb17ad. planner 미결(다음 판): §3.1 번호 9→11 건너뜀 · system.md 70·78줄이 D44·D34 이전 서술 · ESC-006→007 참조 두 곳 · #722 AX 채팅 입력·공유 알림은 SPEC-008/D10 판단 필요. **두 PR 모두 머지됨 — 남은 마감: archive-work.sh.**
- **앱 PR #5 스쿼시 머지 완료(2026-09-12 12:15Z)** → origin/main **0a8a04b**. 직전: FE 스위트 정렬 dd9e2fb(467 통과) · BE 스위트 정렬 e6ab21f(847 통과·architecture 20). 스펙 PR #719 는 아직 OPEN(사용자 결정 대기). 남은 것: archive-work.sh 마감 · 채팅 회의 만들기/공유 새 모델 이관(별도) · 워커 미결(재전사 context 힌트 · 회의 공유 알림).
- **머지 전 전체 스위트(09-12, 사용자 「전체 테스트 한번 돌리고 스쿼시 머지」)**: FE vitest 16 실패(main AX 카드·ActionCenter·App 이 DateField 타이핑 기대 + 포커스 규칙 hover 오탐 + MeetingDetail 드로어 이름) → FE `sc-meeting-fe-suite-fix-brief.md` task_15b635e31617. BE 수집 오류 5(main 테스트가 옛 회의 모델 import) → BE `sc-meeting-be-suite-fix-brief.md` task_6bd3210dddc4. 둘 녹색 → 커밋·push → #5 스쿼시 머지.
- **main 머지 완료(09-12)**: 머지 커밋 **4212691** + 알림 메서드 복원 **ec9946b**(push). PR #5 MERGEABLE. 스키마 동기(main 테이블·열) · 스택 재기동(ec9946b) · 회의/알림/프로젝트 API 200. PR #5 제목·본문 0.4.11·2차·머지 반영(`pr-app-draft.md`). 남은 것: 채팅 [확인] meeting.create/share 새 모델 이관(별도) · 머지 전 전체 스위트 1회(2차 커밋은 e2e 우선, 스위트 미실행).
- **main 머지(09-12)**: PR #5 가 main(#3 채팅 인터랙션·#8 프로젝트 참여 이력)과 충돌 24파일. 코디가 `git merge --no-ff --no-commit origin/main` 걸어 둠 → BE `sc-meeting-be-merge-main-2-brief.md` task_a510cfa16931(backend 13+Makefile) · FE `sc-meeting-fe-merge-main-2-brief.md` task_be80fd33b50a(frontend 10, MeetingDrawer 삭제 유지). 둘 다 add 까지, 커밋은 코디. 그 전: D51 블록 20초 6004fb6 · D10 드로어 15d0cf5 · 앱 19커밋 push(ab8a8ef→6004fb6). 스택은 메모리 부족으로 죽음 — 머지 뒤 재기동.
- **실물 3회차(09-11, 회의 8c63e19b — 재전사 final 성공·칩 D5 확인) → D49·D50**: 근거 칩 전부+TimeChip(FE cf60d06) · 칩 점프 겹침 버그 · 시각 표기 회의 경과 mm:ss(D31 철회) · 업무 생성 드로어 달력 OS 기본/팝오버 카드 안 잘림(DS-17·18). 발주: FE 드로어 task_e6d1b6a19896 → FE 칩 점프·경과 task_970aaebce33c(큐) · planner 0.4.11 task_327b95f5895a. BE D46 c52f94a · D5·D6 cee9bca · 스택 재기동(cee9bca) · 스펙 0.4.10 3f5cada4.
- **실물 2회차(09-11, 지호 실제 회의) 발견 → D47·D48**: 회의 중 AI 요약 시간 칩 소실(근거 검증 구간이 이번 배치 구간뿐) · 빠른 시작 자리표시 안건 「안건 1. 안건 1」. `피드백-회의실.md` D5·D6. **발주**: BE `sc-meeting-be-evidence-window-brief.md` task_59007c820346(D46 뒤 큐) · planner `sc-meeting-planner-d47-brief.md`(0.4.10) task_82c328667258. BE 폴백 폐기 커밋 e252dee(검증 생략, 사용자 지시) · FE D46 d9303b2 · 스펙 0.4.9 a149b3ad. D46 BE task_244a73093469 는 Enter 재전송으로 시작됨.
- **D46 (사용자, 09-11)**: 회의 중 AI 배치도 안건별 「다음 할 일」 후보(읽기 전용, 버튼 없음, provisional, 배치마다 교체, 최종이 지우고 새로). 계약 `sc-meeting-live-todos-contract.md`. **발주**: FE `sc-meeting-fe-live-todos-brief.md` task_8f30a09b7a33 · planner `sc-meeting-planner-d46-brief.md`(0.4.9) task_2bbd6c67fe0b · BE `sc-meeting-be-live-todos-brief.md` task_244a73093469(BE 는 폴백 폐기 task_51fc8000be06 뒤 큐 — dispatch 는 BE 완료 뒤 다시). 스펙 0.4.8 커밋 ef0d19a1(push) · FE 재조회·칩 점프 e7e0cfa.
- **최종 테스트 1회차(09-11, 회의 d6e7b8e0)**: 스택 재기동(b440c6b) 뒤 유나 스크립트(회의명만·안건 없음·참석자 지호·회의실 없음, Charty 음성 1x 6분, 2:30 에 안건 추가) → 사용자 지시로 조기 종료 → done. **발견 D1~D4**(`design/피드백-회의실.md` §D): D1 재전사 결과 GET `IncompleteRead` → 코디 브리프의 폴백이 실시간 원문 위 합성으로 삼킴 → **사용자: 폴백 폐기, 실패는 「실패」** · D2 종료 뒤 스크립트 원문 재조회 없음(2줄/서버 64) · D3 회의 중 칩 점프 없음 · D4 회의 중 다음 할 일 없음(스펙대로). **발주(사용자 「발주해」)**: BE `sc-meeting-be-retranscribe-nofallback-brief.md` task_51fc8000be06 · FE `sc-meeting-fe-script-reload-brief.md` task_d268d948f61a · planner `sc-meeting-planner-d44-fix-brief.md`(0.4.8) task_26bbf527e41a.

계약(상태 wire 값·응답 shape)은 두 브리프 §3 에 동일하게 박음 — 코디 확정. 다음: 둘 완료 → reviewer_code 검수 → 코디 실물 확인(5176/8001) → WP-002 발주.

## 4. 산출물

### 로컬 개발 서버 (2026-09-10 코디가 띄움 — 사용자 눈으로 확인용)

- ax-workspace `sc-meeting` 트리에서 `make install` → `frontend-install` → `postgres-up`(컨테이너 `sc-meeting-postgres-1`, 볼륨 `sc-meeting_ax_demo_postgres`, 54329) → `reset-demo` → `make local-stack`(백그라운드, 로그 `/tmp/claude-501/ax-local-stack.log`).
- 프론트 `http://127.0.0.1:5176` · API `http://127.0.0.1:8001`. 로그인 화면에 데모 계정 목록(`<member>@scax.example` / `scax-demo-1234`).
- ⚠ **로컬 스택 내려감(2026-09-10 저녁)** — 백엔드 워커가 새 스키마로 `reset-demo` 를 돌리는 동안 meeting-worker 가 durable_jobs 조회에서 DB 오류로 죽고 local-stack 이 전부 종료(설계상 하나 죽으면 다 멈춤). 예상된 부작용. **BE 완료 후 코디가 `make reset-demo` → `make local-stack` 재기동**하고 데모 회의를 새 API 로 다시 시딩한다(옛 시딩 스크립트는 note API 를 써서 못 씀).
- 데모 회의 3건을 API 로 시딩(yuna 계정): 「주간 제품 리뷰」(내일·public) · 「DB AX 전환 범위 합의」(2일 전·private·note 초안) · 「AX 파일럿 착수 회의」(5일 전·public·note 확정). UI 에 회의 생성 버튼이 없어 API 로 넣었다. reset-demo 하면 사라진다.
- 디자인 사본 `work/sc-meeting/design/` 12파일(`_MANIFEST.md`). ⚠ 서브에이전트에는 DesignSync 가 없어 실패했고, **코디가 본 세션에서 직접 받아 컨텍스트를 낭비 — 사용자 질책(「백그라운드 태스크로 하라니까」).** 다음부터 DesignSync 가 필요한 작업은 orca 워커 터미널(별도 Claude 세션)에 발주한다. uploads PNG 16장은 제외.
- Soniox 키 파일(`~/.config/soniox/env`) 없음 → 실시간 전사는 「사용 불가」로 뜬다(정상). 내리려면 local-stack 프로세스 Ctrl+C(또는 kill) + `docker stop sc-meeting-postgres-1`.

### 기준점 (사용자 지정 2026-09-10)

| 무엇 | 어디 | 비고 |
|---|---|---|
| **기획·정책 정본** | 코디 워크트리 `reference/2026-09-10-sc-meeting/` — `plan-004-meeting-note.md`(PLAN-004, 조아이보리, v1.0.0 2026-09-09) · `screen-005-meeting-note.md`(SCREENDEF-005) | `확정사항.md`(X-###)·`내부-결정지도.md`(D-###)는 **무시한다**(사용자 2026-09-10). X-### 참조는 풀지 않고 plan-004·screen-005 본문만 정본으로 읽는다 |
| **코드 구현** | ax-workspace `sc-meeting` 워크트리(origin/main a0bcee8) | 현행 회의 모듈·MeetingDrawer 를 대체 |
| **회의실 중계 참고** | `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app` — **문서**: `para/projects/summer-star/task-management/20-spec/spec-007-meeting-live.md`(§4 WS 메시지 계약 `WS /api/meetings/{id}/stream` · AI 배치 계약) · spec-006/008 · `40-architecture/database/domains/meeting.md`. 이 워크트리의 `app/` 은 kknaks_profile 사이트 코드라 회의 코드가 **없다** — 코드는 `/Users/kknaks/git/toy_pr2/task_management` main(a720b6e) `app/back/api/meeting_stream_router.py` · `service/meeting_stream_service.py` | 사용자가 「task-management-app 참고」라 했으나 코드는 task_management 리포에 있음 |

### PLAN-004·SCREENDEF-005 와 앞선 결정·디자인의 충돌 (사용자가 가려야 함)

| # | 기획 문서 | 충돌 상대 |
|---|---|---|
| A | **회의록은 한 층**(DEC-003·X-136): 서기 노트·AI 요약을 나누지 않고, 메모는 안건 요약의 재료로 녹는다. 「채택」 없음 | **2026-09-10 사용자 확정: 컨셉이 이긴다 — 「나와 AI 둘이 회의에 들어간다」.** 회의 중 내 메모 트랙 + AI 중간 요약 트랙(안건마다 차오름) 각자, 종료 후 둘을 합쳐 최종 회의록. Claude Design 회의실 2탭 구조가 맞음. → **PLAN-004 DEC-003·X-136 은 개정 대상**(planner 발주 범위). 중간 요약 배치는 task-management spec-007 §4 AI 배치 계약(MF-71) 참고 |
| B | **음성은 소니웍스 PC 음성 인식**(DEC-004·X-197) | **2026-09-10 사용자 확정: 소니웍스 = Soniox, 백엔드 중계와 같은 말.** 충돌 아님. OQ-201(실시간 회의록을 개발측이 받나)은 「받는다」로 닫힘 |
| C~E | 기획이 정본 — 기획대로 간다(사용자 「기획/정책은 reference 보고」). spec-004·현행 코드·디자인이 기획과 다르면 기획 쪽으로 맞춘다. **디자인(Claude Design)은 참고용**(사용자 2026-09-10) |
| C | **판을 쌓지 않는다·덮어쓰기**(X-136·X-139 폐기), 확정 표시 없음(X-119 폐기), 재생성 없음(X-16 개정) | spec-004 versioned note·finalize · 현행 코드 note_versions·adopt_summary |
| D | 수정 권한은 **만든 사람 하나**(DEC-005·X-186), 「녹음」이라는 말 금지(DEC-009), 녹음 원본 화면에 안 냄(X-164) | 디자인의 「서기」 역할 표기 · 현행 녹음 시작/종료 UI |
| E | 메뉴 「회의 목록」 8개 메뉴(X-39) · SCR-105 목록 + SCR-106 상세 + MOD-102/104/105 | 디자인 rail 7개(홈·채팅·캘린더·내 업무·회의록·자료함·설정) · 현행 rail 7개(회의 메뉴 없음) |

- **조사 1 리포트** `survey-01-ai-provider-report.md` — 핵심 사실: ① 외부 AI 는 Codex CLI subprocess(LLM, `platform/codex_cli.py:69`, 모델 `gpt-5.6-terra` 하드코딩·90s·generate 취소 불가)와 Soniox(STT, REST+ws 임시키, 브라우저가 직접 ws 연결) 둘뿐, SDK 의존 0 ② 회의 refinement·summary 는 일일보고와 같은 `_report_provider` 인스턴스, `modules/meetings` 는 AI port 를 안 들고 bootstrap 층에서 호출 ③ 프로토타입 요구 3건(회의 중 실시간 AI 노트·종료 후 합성 초안·안건 구조) **전부 없음** — provisional summary 는 슬롯(kind·DB·뷰·프론트 라벨)만 있고 생산자 없음, adopt_summary 는 AI 본문을 그대로 note version 으로 append ④ 문서≠코드 8건(§6.2) ⑤ 사용자 질문 8개(§9).

- 출발 PR: https://github.com/MediSolveAIDev/ax-workspace/pull/2
- 출발 커밋: `663319c38b9f39c1a9894375bc6c02f5b37e3999`
- 디자인 참조: 코드 워크트리의 `.design-sync/config.json`, `.design-sync/NOTES.md`, `frontend/ds-entry.tsx`, `docs/design/design-system-v2.dc.html`
- **회의 백엔드 플로우 정본 = task-management** (사용자 결정 2026-09-09). 문서(코디 워크트리, read-only 절대경로로 브리프에 박는다): `para/projects/summer-star/task-management/` 의 `00-baseline/baseline-003-meeting-notes.md` · `10-decision/decision-003-meeting-notes.md` · `20-spec/spec-006-meeting-setup.md` · `spec-007-meeting-live.md` · `spec-008-meeting-close.md` · `40-architecture/database/domains/meeting.md` · `30-work/work-006~015`. 코드: `/Users/kknaks/git/toy_pr2/task_management` `main`(a720b6e) — `app/back/service/meeting_stream_service.py`(WS 중계) · `meeting_batch_service.py`(AI 중간 배치) · `meeting_finalize_service.py`(종료·합성) · `integrations/soniox.py`. 사용자 canonical 체크아웃 — pull/checkout 금지, 읽기만.
- **the Connect 인증·회의실 예약 기존 구현 = mediness-app**(사용자 2026-09-10): `/Users/kknaks/git/harness_works/mediness-app/back/app/clients/the_connect.py`(클라이언트) · `routers/meetings_v2.py`·`meetings.py` · `repositories/meeting_v2_repo.py` · `config.py`(CONNECT 설정) · 스펙 `mediness-mediness/products/mediness/20-spec/spec-151-ax-assistant-reservation.md`. sc-ax 에 회의실 판정·예약을 붙일 때 원형. 지금은 데모 범위 밖(D16) 유지 — 사용자가 넣자고 하면 WP-005 또는 신규 WP 로.
- 회의록 화면 디자인: Claude Design 프로젝트 「SCAX 회의록 프로토타입」 `3f12e84a-b1ed-4a27-ab33-bd228dcbf71f` — `회의실.dc.html`(회의 진행: 시작 전·기록 중·통합 작성 3모드, 노트/AI 노트 + 스크립트/첨부 2패널, `/` 종류 선택 입력창, 첨부 Drawer) · `회의록.dc.html`(목록). DS 번들은 SCAX `8fa54d76` 과 동일. DesignSync `get_file` 로 읽는다.

## 5. 이력 (최신이 위)

- `2026-09-10` spec 커밋 d79cb80ba(쿠키 인증·WP-002·WP-005). WP-003 브리프 작성(발주 대기). planner 에 메모 API 형태·트리거 잠정값·persona 환류.
- `2026-09-10` BE WP-002 질문 → A: 회의 native 자료 검색 다리 폐기(테이블과 함께), promote 라우트 제거(WP-004 인계), 회의 전사 검색은 WP-005 가 MeetingTranscript 위에 재건(planner 에 Scope 추가 지시). 데모 중 /api/materials/search 에 회의 내용 일시 부재.
- `2026-09-10` planner WS 쿠키 인증 환류 완료. FE Phase 3 병렬 발주.
- `2026-09-10` 사용자 「왜 작업 하나에 오래 걸려」 → 원인(결정 13건 중간 유입·직렬 검수·코디 오버헤드) 설명, 개선(결정 묶음 전달·diff 재검수·BE/FE 병렬). WP-002 발주.
- `2026-09-10` 코드 검수 2 PASS → app·spec 워크트리 커밋(체크포인트). 다음 WP-002 브리프.
- `2026-09-10` planner D23·D24 완료 — SPEC §7.1 세션·§7.2 도구 레지스트리(넷이 바닥)·§8-3 같은 세션·§11.1 구조화 고정 폐기·§8.1 중복 방지·§9-6 요청됨·R-18 교체·OQ-315/316, system.md §4·§5, WP-003(웜스타트·도구·Open Issue 3)·WP-004·WP-006. M16 한 줄 추가 지시.
- `2026-09-10` D24 세 워커 완료(designer-1·2, FE). 디자이너 미결 M16: SCR-106→SCR-102 진입 경로 소멸(정본 레지스트리·전이 맵의 「업무로 섬」 경로) — 기획 통보 목록(R-##)에 planner 가 D24 처리 때 넣게 함. 세 파일 모두 「연관 업무」 잔존 0.
- `2026-09-10` 스택 재기동·재시딩·실물 재확인 통과(F1 과거 일시 scheduled 유지 · can_edit_agendas · 진행 중 안건 409 · 비참석 404/0건). FE D24 완료(요청됨 텍스트) · designer-2 D24 완료(M16: SCR-102 진입 경로 소멸 기록). 코드 검수 2(diff 한정) 발주.
- `2026-09-10` BE 검수 1 수정 완료(F1 created_at 예외 · F2 Todo 8필드 · F3 can_edit_agendas + 진행 중 안건 409 · 열람 축 셋째 제거(캘린더 list 만 유지) · list commit · domain-model.md). 220 passed. 스택 재기동 → 재시딩 → 실물 재확인 → FE D24 후 코드 검수 2(diff 한정).
- `2026-09-10` 로컬 스택 2차 종료 — BE 워커의 reset-demo 재실행 중 durable_jobs 부재로 meeting-worker 사망. BE 수정 완료 후 코디가 재기동·재시딩·실물 재확인.
- `2026-09-10` FE 검수 1 수정 완료(F4 제거·can_edit_agendas 분리·[수정]은 둘 중 하나·토스트·W8). tsc 0·vitest 56/56. D23 planner 지시. BE 수정 대기.
- `2026-09-10` planner 코드 검수 후속 완료: can_edit_agendas 를 SPEC §3.3·§4.1-5 + WP-001 계약에, work-001 Open Issue(조회 시점 자동 취소·트랜잭션 경계). 문서 대기 없음. 사용자 질문(AI MCP 조회·세션 id) 답변: 회의 배치는 generate(도구 없음), 세션 ref 는 provenance 로 이미 옴 — WP-003 발주 때 「중간 요약 세션 유지·도구 없음 / 합성만 MCP」 기본값 제안.
- `2026-09-10` planner D21 반영 완료(§8.1 세 행 조건 해제, 원칙 두 줄: 「최대한 채운다」+「담당·기한은 지어내지 않는다」). 다음: planner 코드 검수 후속(can_edit_agendas·work-001 Open Issue) 대기.
- `2026-09-10` 코드 검수 1 FAIL → D22 기본값으로 BE·FE·planner 수정 발주.
- `2026-09-10` planner D20 반영 완료(SPEC §8.1 reference 형·§9-5 두 id·§9-7 양방향 역추적, WP-004 스키마 요청·Pre-deploy 2줄, WP-001 Todo 8필드). 소유 경계: 출처 열 계약은 SCAX-SPEC-001. 문서 대기 없음.
- `2026-09-10` FE D19-3 완료: Todo 계약 교체(담당 제거), 다음 할 일 행 = 할 일·기한·[업무 생성]·×, [업무 생성]→현행 CreateWorkDrawer(요청만, 담당 비움·참석자 우선). tsc 0 · vitest 75/75. 미결: reference 필드 형 미정(소비 안 함) · 후보 × API 없음(TODO WP-004/005). 코드 검수 1 은 이 변경 이전 diff 기준 — 결과 뒤 diff 한정 재검수 필요.
- `2026-09-10` designer-2 D19-3 완료(회의실 + 회의록 둘 다). ⚠ 코디가 같은 지시를 두 디자이너에게 보내 회의록.dc.html 을 둘이 건드림 — 코디 검증: 두 파일 스크립트 파싱 OK, T(what,due,linked) 일관, 담당 잔존 0. 교훈: 파일 소유 워커 한 명에게만 보낸다.
- `2026-09-10` designer-1 D19-3 완료(목록 패널 다음 할 일 = 할 일·기한, 담당 제거; 읽기 전용이라 [업무 생성]·× 없음 — 사용자 앞선 확인). planner D19 2차 반영 완료(R-34 추가). 대기: designer-2·FE D19-3, 코드 검수 1.
- `2026-09-10` D19-3: 다음 할 일 행 = 할 일·기한·[업무 생성]·× (담당 표기 제거). designer-1·2·FE 에 지시. **실물 확인 1차(코디)**: 새 API 로 회의 3건 생성 201, start 200, 목록 두 구획·행/상세/안건 키 계약과 일치, PATCH 409 게이트 OK, 안건 POST 201. 지난 날짜 scheduled 회의는 조회 시 자동 취소됨(WP 규칙대로).
- `2026-09-10` planner D19 정정 반영 완료 — 승격 단일 경로(업무 요청), linked {work_request_id, task_id|null}. SPEC·WP-004·WP-006·10-decision. lint 0. **문서 쪽 대기 없음.**
- `2026-09-10` planner D19 1차 반영 완료(SPEC §8.1 Todo 표 신설·§9 두 갈래·WP-004/006/001). **정정(항상 업무 요청) 반영은 이어서** — 완료 보고 대기.
- `2026-09-10` FE D18 반영 완료(E57 UI 원래 없음, 문구 4 제거). D19 Todo 페이로드 확장 → planner 에 지시(D18 과 묶음).
- `2026-09-10` FE(WP-006 P1·2) 완료. BE 에 안건 PATCH `lines` 계약 보강 전달. 사용자 질문 「다음 회의 안건 컬럼」 → concluded·source=carried·carried_from 으로 갈음(코디 통보).
- `2026-09-10` BE(WP-001)·FE(WP-006 P1·2) 병렬 발주. 사용자 확인: 프론트 범위 = 목록 + 예약 모달(정적 회의실) + 상세 읽기/편집.
- `2026-09-10` BE 브리프(WP-001, 계약 JSON 코디 확정 — 상태 wire 값 OQ-301 닫음)·FE 브리프(WP-006 Phase 1·2, 같은 계약, 백엔드 없이 vitest 모킹) 작성. 사용자 승인 대기. 사용자 「메디니스 앱에 인증/회의실 예약 있어」 → 원형 위치 기록.
- `2026-09-10` designer-1 완료: MOD-102 회의실 정적 목록(가능 배지·잠금·T19 제거). planner R-33. **시안 2 + SPEC 0.4.1 + WP 6 전부 정리 끝 — BE/FE 브리프 작성 단계.**
- `2026-09-10` 검수 3 PASS(WARN 1 — 회의실 가능 배지 잔존, 뒷정리 지시). 스펙·WP 사용자 리뷰 단계.
- `2026-09-10` planner 완료: SPEC 0.4.1 — F-A·F-B·WARN 9 코디 결정대로 해소, §12 R-31·R-32 추가(32건), WP-001/002/004/006 갱신(화자 매핑 WP-002, /end 소유, 회의실 판정 제거). 검수 3(diff 한정) 발주.
- `2026-09-10` designer-2 완료: 「완료」 통일(M7 닫힘) · 머리 편집 장소 글자 칸, 예정·완료에서만(M14③ 닫힘) · 「기타」 블록 제거 · 출처 값 셋(M10 닫힘) · 리포트 §1·§3 표 갱신. 검증 재통과. 남은 미결 M9·M11①③·M12·M13·M14①②·M15 — 전부 시안 유지, 기획자 통보용.
- `2026-09-10` 검수 2 FAIL 2·WARN 9 → 코디 기본값 D16 으로 planner 0.4.1·designer-2 수정 발주. 완료 후 검수 3(diff 한정) 예정.
- `2026-09-10` 사용자 질책(질문 반복·기획 개정 요청 프레임). D15 디자인 정본 확정. planner 에 SPEC+WP 지시. 코디 규칙: 이후 결정은 기본값으로 정하고 통보, 질문 최소화.
- `2026-09-10` D13(상태 6·「완료」)·D14(바로 시작) 확정. designer-2 에 「완료」 개명 + 장소 글자 칸 지시. 사용자가 질문 반복에 불편 표시 — 이후 결정은 코디가 기본값 정하고 통보.
- `2026-09-10` designer-2 수정 13: 머리 편집 중 [회의 시작] 비활성(고치다 만 값으로 안 엶) · E85 목적을 좌우 두 칸 위 전체 폭으로(왼쪽·오른쪽 패널 머리 같은 줄). 검증 재통과.
- `2026-09-10` designer-2 수정 12: 머리 편집 2:3(제목·일시 | 참석자 태그·검색), [취소][저장]을 「회의 정보」 라벨 옆 h22 로. 진행 중 primary 둘(회의 종료+메모 던지기) → 던지기 secondary 로 내려 화면당 primary 1 준수. 검증 재통과.
- `2026-09-10` designer-2 수정 11(사용자 직접): 회의 정보 머리 편집을 제목|일시|참석자 한 줄 그리드로. 조직 귀속 제거(정본 E03 과 다름 — 개정 요청 후보) · 일시 칸 신설(I22→MOD-102 를 안 쓰기로 해 여기서 고침, 30분 단위) · **장소는 못 옮김**(회의실 판정 MOD-102-E04·X-190 종속) → M14 ③ 어디서 고칠지 확정 필요.
- `2026-09-10` designer-2 수정 10: 회의 정보 [수정] 글자 → 연필 아이콘(DS Icon 세트에 pencil 없음 → 페이지 안 인라인 SVG, Icon 규격 준수). DS 등록 요청 후보(pencil 글리프). M14 ①.
- `2026-09-10` **바로 시작 논의 중**(사용자 방향): AI 는 안건을 참고만 하고 대화에서 안건을 세운다(「기타」 블록 규칙 X-94 폐기 방향) · 참석자 추측(E61) 없음 — 조직도/사외 추가로 사람이 직접 · 제목은 종료 합성 때 AI 후보 → 사람 확정. 미정: AI 가 새 안건을 만드는 시점(회의 중 즉시 vs 종료 합성 때 확정 — 코디 추천 후자). 확정되면 스펙 §4·§7·§8 + 시안 M1 발주.
- `2026-09-10` designer-2 수정 9: 자료 드로어 drawer-facts 제거(올린 사람만 header-extra) · 본문 편집을 textarea 한 덩어리 → 줄 단위 행(line-edit h30 + 줄 × + [내용 줄 추가]). **정본 §5.4 E29 「여러 줄 한 칸·10000자」와 갈림 — D12 파생, 미결 M13 → 개정 요청 후보(E29 입력 형식·줄 추가/삭제 요소화).** 검증 재통과.
- `2026-09-10` designer-2 수정 8: MOD-105 공유 모달을 MOD-102 참석자 자리와 같은 모양(검색 팝오버·조직도 2단·볼 수 있는 목록 표)으로 재작성. 이미 참석·열람인 사람 제외(E02). 표 th34/td40 축소·폭 680. 검증 재통과.
- `2026-09-10` designer-2 완료: 회의실 D12 반영(6상태 동일 줄 블록, 들여쓰기 3단, 편집은 textarea 한 칸·줄바꿈=내용 줄, 실패엔 결론 표시 없음). 검증 재통과. **두 시안 모두 D12 반영 완료.** 남은 사용자 결정: M12 근거 칩 자리·표기 · M11 예정 [수정]/[공유] · M9/M10(기획자 문의 중).
- `2026-09-10` designer-1 완료: 목록 패널 안건 블록 D12 반영(줄 배열 데이터, 「다음 할 일」 테스크 줄, 연관 업무 ›). REPORT §6-0(e) 에 E29·E40·E41·E43·SCR-105-E22 갱신 대상 기록. 검증 재통과.
- `2026-09-10` D12 안건 본문 한 줄씩 결정 → designer-1·2 에 지시. designer-2 수정 7: 근거를 본문 뒤·다음 할 일 앞 타임칩으로(정본 변형3·E31 건수와 다름 — 사용자 결정 대기) · **MOD-105 공유 모달 구현(브리프 §7 제외 범위 → 사용자 요구로 범위 확대, 코디 승인 기록)** · 예정 [수정]/[공유]·진행 중 [수정] 와이어↔표 어긋남 M11 로 묶음.
- `2026-09-10` designer-2 수정 6: 후속업무 후보 행 — E43 승격 표시 「업무로 섬」→「연관 업무 ›」(정본 요소표 표기와 다르나 §5.8 확정 문구 아님 → M9 묶음, 개정 요청 후보에 문구 T-ID 부여 항목으로 포함) · SCR-102 링크는 SCREENDEF-004 소유라 미연결 · 버튼 무게 h30 통일, 조작 자리 폭 116 고정. 검증 재통과.
- `2026-09-10` designer-2 수정 5: 정리 중→정리됨 자동 전이(1초, 합성은 자동이라 버튼 없음 — spec §8). 예정→진행 중→정리 중→정리됨 흐름이 화면 안에서 끊기지 않음. 프롭으로 「정리 중」 직접 선택 시엔 유지. 검증 재통과.
- `2026-09-10` designer-2 확인: 스크립트 탭에 메모 표시는 정본대로(E26·E31·spec §5.4-8). E31 의 «적은 사람» 누락을 보완 — 메모 줄 「메모 / 이름 / 시각」. 검증 재통과.
- `2026-09-10` designer-2 수정 4(사용자 직접): 예정 상태에 안건 편집 추가 — E77 [수정] 이 진행 중·정리 중 뺀 네 상태에서 서고, 예정·취소됨은 «안건 편집»(E71 ×·E35 추가), 정리됨·실패는 본문 편집. 정본 자체가 어긋남(§5.7 예정은 회의록 수정 제한 vs §5.2 와이어프레임 변형1 에 [수정] 있음) → 와이어프레임 쪽. 미결 M11 → 개정 요청 후보(§5.7 갱신).
- `2026-09-10` designer-1 완료: 삭제 모달 머리 ×, 푸터 [회의록만 삭제]·[회의 취소]. ×·Esc·바깥 클릭 닫기, 초기 포커스 ×. REPORT §6-0(d) 에 정본 갱신 대상(T08·T09·T10·E15·I15·I16) 기록. 검증 재통과.
- `2026-09-10` designer-2 발견 M10: SCR-106-E21 안건 출처 네 값(직접 입력·세트·지난 회의에서 넘어옴·다른 회의에서 파생) 중 「세트」·「다른 회의에서 파생」은 붙을 경로가 정본 어디에도 없음(세트가 나르는 건 MOD-102-E25 기본 인원뿐, E07 은 둘만). 기획 내부 모순 → 개정 요청 후보. 시안 안건 3 이 「세트」 사용 — 값 삭제 여부 사용자 판단 대기.
- `2026-09-10` 사용자 「삭제 모달도 × 넣는 게 깔끔」 → designer-1 에 지시: 머리 ×, 푸터 [회의록만 삭제]·[회의 취소] 둘(정본 T08 3버튼과 다름 — 이탈 목록에 기록, 기획자도 × 를 물었으니 합의로 본다).
- `2026-09-10` designer-2 확인: 「지난 회의에서 넘어옴」은 정본 E21·MOD-102-E07·spec §4-2 에 있으나 §5.8 문구표에 T-ID 없음 → 미결 M9(기획 공백 — 개정 요청 후보: 출처 표기 문구에 T-ID 부여).
- `2026-09-10` designer-1 완료: 삭제 확인 문구·버튼명([취소]·[회의록만 삭제]·[회의 취소]) 반영, 취소는 이미 푸터 버튼(× 없음 — 정본 T08 3버튼과 일치), 예약 모달은 반대로 머리 × 만(MOD-102-I10). 예약/문서만 갈래는 미결(§6-8). 목록 높이 flex 전환 완료.
- `2026-09-10` designer-2 수정 3(사용자 직접): 자료 탭 인라인 미리보기 → 행 클릭 시 Drawer 로 하나만(PDF·Markdown 만, 표·이미지·압축 갈래 삭제) — **정본 E64·X-142(탭 안에서 본다)와 다름, 개정 요청 후보** · 진행 중 메모 탭을 안건 블록 모양으로 통일(6상태 동일 블록).
- `2026-09-10 13:2x` **기획자 피드백**(사용자 전달): 삭제 확인 T08 문구 → 「회의 삭제 시 회의 자료가 삭제되고 회의도 취소됩니다.」 · [자료만 삭제]→[회의록만 삭제] · [회의 삭제]→[회의 취소] · 취소 버튼이 × 가 아니라 하단 배치인지 확인 요청 · 예약 포함/문서만 생성에 따라 갈릴 수 있음(기획안 갱신 후 재공유 예정). designer-1 에 반영 지시 + 목록 높이 고정값 수정 동봉. **기획자가 기획안을 직접 갱신하므로 이 건은 개정 요청 목록에서 제외.**
- `2026-09-10` designer-2 수정 2: 회의실 패널 아래 빈 띠 제거 — `calc(100vh - 260px)` 매직 숫자 → canvas/page-surface flex 기둥 + 그리드 flex:1, 아래 여백 64→24. 목록 시안(회의록.dc.html)에도 같은 `calc(100vh - 214px)` 가 있어 같은 수정 필요(미적용).
- `2026-09-10` designer-2 수정: 회의실 진입 기본값 「진행 중」→「예정」. 파일 열면 회의 전 화면, [회의 시작]→진행 중→[회의 종료]→정리 중→정리됨/실패→[다시 시도] 흐름을 화면 안에서 밟음. 검증 재통과.
- `2026-09-10` designer-2 완료(회의실 SCR-106 시안). 두 시안 어휘 갈림(완료/정리됨) 판정 대기.
- `2026-09-10` designer-1 모달 전환 완료. 목록 시안 정본 이탈 6건 확정(사용자 직접 지시) — 기획 개정 요청으로 planner 재발주 때 SPEC §12 에 실을 것.
- `2026-09-10` designer-2(회의실 SCR-106) 발주 · designer-1 에 모달 전환 지시. 워커 핸들도 회전함(designer-1 stale) — 워커 메시지는 `terminal list` 제목으로 찾아 보낸다.
- `2026-09-10` **회의 목록 시안 완성**(사용자 「이정도로 목록은 완성」, 918줄). 정본 대비 의도적 이탈 = 기획 개정 요청 후보: ① E05·§5.7·X-133 상태 전부 표시(예정·정리 중·완료·실패·취소됨, 열람은 배지) ② E22 안건 블록에 본문+「다음 할 일」(SCR-106-E40 모양) ③ E23 후보 건수 줄 삭제(안건 안으로). 미결: 상태명 「완료」/「정리됨」 · 패널 머리줄(E66 마지막 저장) · 드로어 푸터 primary · 취소됨 [내보내기] · 예정 [공유].
- `2026-09-10` designer 피드백 2: 패널 안건 블록을 SCR-106 모양(제목·결론·본문·다음 할 일)으로 키움 — **SCR-105-E22·E23 과 어긋남**(정본은 안건+결론, 후보는 건수만). 미결: 「AI 회의록 · 마지막 저장」 머리줄(E66) 넣을지. 사용자가 designer 와 직접 반복 중 — 개정 요청 후보 누적: E05·§5.7·X-133(상태 전부) · E22·E23(패널 깊이).
- `2026-09-10` designer 가 사용자 직접 피드백으로 목록 행에 상태 전부(예정·정리 중·완료·실패·취소됨 + 열람 배지) 표시 — **SCR-105-E05·§5.7·X-133 과 어긋남**(정본은 「기본이 아닌 것만」). 시안이 정본보다 앞섬. 미결: 이 변경을 기획 개정 요청으로 올릴지, 상태명 「완료」 vs 「정리됨」.
- `2026-09-10` designer 완료(회의 목록 시안 v2). 결정 3개 대기. 시각 확인 경로(Claude Design 되올리기 vs 새 캔버스) 미정.
- `2026-09-10` 검수 1 완료: FAIL 1(일시정지·재개 UX 발명) · WARN 11. 사용자 결정 4개 대기.
- `2026-09-10` reviewer_spec(검수 1) · designer(회의 목록 시안) 동시 발주. 둘 다 orca 워커 세션.
- `2026-09-10` planner 완료(SPEC-004 0.3.0). 디자인 사본 12파일 저장 — 코디 직접 처리로 세션 낭비, 사용자 질책. 교훈: DesignSync 작업은 orca 워커로.
- `2026-09-10` 로컬 개발 서버 기동(5176/8001/54329). 코디가 직접(사용자 확인용 — 워커 금지 규칙과 별개).
- `2026-09-10` 목록 화면 논의: 디자인 vs SCR-105 차이 7개 정리 → 화면정의서 정본 확정. D10 알림 제외(데모). planner 에 즉시 전달.
- `2026-09-10` 코디 핸들 재변경 감지(`term_d9153f79…` → `term_a53b7eb6…`). planner 워커에게 terminal send 로 통지, 브리프 3개 핸들 교체.
- `2026-09-10` planner 발주(SPEC-004 재작성). 워커 주입·제출 확인.
- `2026-09-10` 역할 경계 교정: 사용자 「나는 스펙부터 작성 담당, 기획서는 기획자가 올려줄거야」 → 브리프에서 기획 착지(plan-004·screen-005) 제거. 개발은 `20-spec/` 부터.
- `2026-09-10` spec 워크트리 소실 발견(09-09 정리) → 재생성(base 59cd71302). planner 브리프 작성 착수.
- `2026-09-10` 충돌 B 해소: 소니웍스 = Soniox = 백엔드 중계. 확정사항.md 무시. 디자인은 참고용. C~E 는 기획대로.
- `2026-09-10` 충돌 A 해소: 사용자 「2명이서 회의 들어가는 컨셉이 맞아」 → 나·AI 두 트랙(메모 / AI 중간 요약) + 종료 후 합침. PLAN-004 DEC-003 개정 필요. (코디가 처음에 「기획대로 한 층」으로 잘못 적었다가 정정.)
- `2026-09-10` 사용자가 기준점 3개 지정(기획 reference/2026-09-10-sc-meeting · 코드 ax-workspace · 중계 참고 task-management-app). 코디가 PLAN-004·SCREENDEF-005 읽고 앞선 결정과의 충돌 A~E 정리(§4). 확정사항.md 부재 확인.
- `2026-09-10` ax-workspace 워크트리 origin/main `a0bcee8` 로 reset(PR #2 squash 머지 확인, 우리 브랜치 고유 커밋 0). task_management main = origin/main `a720b6e` 동일 확인. 조사 2(참고 레포 검토) 브리프 작성 착수 전.
- `2026-09-09` 사용자 결정 2건: STT 백엔드 중계 · 실시간 전사 정본. 컨셉(나·AI·조직원 참석, 노트 탭 2개, 종료 후 합성) 확인. 코디가 회의 코드 동작·프론트 진입점(캘린더 안 회의 목록 탭)·실시간 전사 위젯 존재를 설명.
- `2026-09-08 10:58` 조사 1(AI 프로바이더) reviewer_code 발주. 워커 heartbeat 의 코디 핸들 `term_d9153f79…` 가 실제(list 확인). env 의 `term_becfca70…` 는 stale — 브리프 4개 핸들 전부 교체.
- `2026-09-08` planner·backend·frontend 3워커로 재세팅. spec 워크트리 `sc-meeting-spec` 신규(base a8e934970), app 워크트리 재사용. 브리프 3개 생성(범위 미기입). Claude Design 회의실 화면 읽기 확인.
- `2026-09-08` origin/main에서 Orca 워크트리 생성 후 PR #2 head까지 fast-forward. 새 코드 변경 없이 세팅 완료.
