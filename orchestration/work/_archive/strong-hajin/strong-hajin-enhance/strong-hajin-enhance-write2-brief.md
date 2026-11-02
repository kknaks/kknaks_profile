# [writer] 고도화 2판 — SPEC-008 개정 · SPEC-010 신설 · WORK-012 신설

너는 **strong-hajin `writer` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 문서 규칙: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/para/projects/project.md` · `P/20-spec/README.md`(SPEC 에 둘 것/두지 않을 것) · `P/30-work/README.md`
- **모양의 본보기**: SPEC = `P/20-spec/spec-008-external-channels.md`(§1 Context ~ §7 Open Questions) · WORK = `P/30-work/work-011-external-channels.md`(Meta · 원칙 · Work Summary · Code Surface · Phase 절 · Pre-deploy · Rollback · Done Criteria · Open Issues · Domain/Schema)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2` (코디 워크트리에 직접 탄다)
경로 약어: `P/` = `para/projects/summer-star/strong-hajin/` · `W/` = `orchestration/work/strong-hajin-enhance/` · 코드 `C/` = `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance/`(origin/main `f0ad522`, **읽기만**)

⚠ **코디와 같은 트리다.** allowed_paths 의 파일만 만든다/고친다.

## 1. SSOT — 계약의 근거 (여기 없는 것은 발명하지 마라)

| 원료 | 경로 |
|---|---|
| **결정 — 정본** | `P/10-decision/decision-009-enhance.md` (D-01~ · OQ-901~909 **전부 닫힘** · 범위 밖 · WP 묶음) |
| 입력 | `P/00-baseline/baseline-008-enhance-improvements.md` |
| 항목 상세(동작·문구·셀렉트 모양) | `P/improvements/SH-IMP-0NN-*.md` |
| 현재 코드 — 파일:줄 | `W/be-survey-report.md` · `W/fe-survey-report.md` |
| 고칠 기존 계약 | `P/20-spec/spec-008-external-channels.md`(v0.5.1) |
| 회의 기능 원본 계약(회사 판) | `git -C /Users/kknaks/git/harness_works/mediness-mediness show origin/mediness:products/sc-ax/20-spec/spec-004-meeting-note.md` — **읽기만**(체크아웃·pull 금지). 회의·회의록·종료 합성 용어와 기존 계약의 출처. 이 레포에 회의 SPEC 이 따로 없으므로 SPEC-010 이 그 위에 **바뀌는 것만** 적는다 |
| 메디니스 회의록 방식(정정 pass·보정 표·맥락 목록) | `W/be-survey-report.md` §5.7 (원문이 필요하면 `git -C /Users/kknaks/git/harness_works/mediness-mediness … ` 이 아니라 앱 레포 `git -C /Users/kknaks/git/harness_works/mediness-app show origin/dev:back/app/seeds/prompt_seeds.py` 등 — 읽기만) |

**기대는 개념** — 해당 없음.

## 2. 배경

DEC-009 가 개선 18건(019 보류 · 009 완료 · 013① 범위 밖)의 방향을 정했고 미결 9건도 사용자가 닫았다. 이 판은 그것을 **계약(SPEC)과 실행 계획(WORK)** 으로 내린다. 다음은 바로 **구현 발주**다 — WORK 의 Phase 가 그대로 BE·FE 브리프가 된다.

## 3. 만들 것

### 3-1. `P/20-spec/spec-008-external-channels.md` 개정 → v0.6.0

메시지함·외부 채널 쪽 결정만: **014**(받기 = `attachment` / 미리보기 = `inline` 를 주소로 가름 · 프론트 받기 링크는 `download`·`_blank` 없는 같은 탭 링크 — 화면 모양은 그대로) · **018**(원격 이미지 프록시가 SVG 허용 + sandbox CSP + nosniff · 나머지 거절 규칙 유지 · 원격 이미지 절의 옛 「눌러 보기」 문장 정정) · **010**(`/api/inbox/stream` `integration.changed` 를 건수·진행 커서·마지막 수집이 바뀔 때도 낸다) · **012**(슬랙 `member_left_channel`·`channel_left` 등으로 즉시 분배 중단) · **015**(호버 막대 — 슬랙 「스레드에 답글 · AX 업무 생성 · AX 요약」, 카톡 「AX 업무 생성 · AX 요약」 · 아이콘만 + 아이콘 호버 툴팁 · 답글 0개도 스레드 패널 · 표기 OQ-908) · **008**(메일 머리 [AX 업무 생성][AX 요약][답장][전체 답장] · 수동만 · 자동 추천은 범위 밖) · **015/008 공통 맥락 계약**(AX 대화 참고 자료에 「메시지」 종류 · 서버가 DB 에서 조합한 우리 모양 JSON — 줄 = `{at, sender, text, attachments(이름만), thread_reply_count}` + 고른 메시지 `target:true` · 채널 메시지 위아래 100줄 / 스레드 답글이면 스레드 전체 / 메일은 그 메일 · 남의 방 거절 · 말풍선 문구 「(이 메시지/이 메일) 읽고 업무를 생성해 줘」·「… 요약해 줘」) · **OQ-907**(만든 업무 출처 행에 원래 메시지 링크 · 메시지 쪽 「업무 만듦」 표시).
- **DEC-008 「hover 행동 막대 없음」 을 뒤집는다**는 것을 §1 변경 이력과 해당 절에 남긴다. 지운 문장은 ~~취소선~~ 으로 둔다(지우지 않는다)
- 변경 이력(머리)에 0.6.0 한 줄

### 3-2. `P/20-spec/spec-010-meeting-ax-enhance.md` 신설 → v0.1.0

회의·회의록·AX 쪽: **002/004**(일정 칸 겹침 — 날짜 칸 폭 축소 · 참석자 중복 방지만 · OQ-909) · **005**(불러오기는 시간을 복사하지 않음 · 안건 출처 = 안건별: 지난 회의 미결 항목 「지난 회의에서 넘어옴」 · 새로 쓴 것 「새로 추가된 안건」 — 서버가 회의 단위로 일괄 지정하지 않음) · **006**(단계별 timeout env 기본값 OQ-902 · 재시도 = 새 세션 1회 · **AI 맥락 목록**(테이블 없음, 호출 때 DB 조회 — 프로젝트 전부 · 완료·취소 안 된 업무 · 구성원 전부) · 최종 = 정정 pass → 다시 쓰기 · 재전사 전체 발화 매번 · **용어 보정 표**(등급 auto/presumed · 화자 라벨 불변 · 되돌릴 수 있는 쌍 · 회의록 화면 끝에 표시) · 안건 = 처음 나온 시각 순 · 기한 규칙 OQ-903) · **017**(AX 업무 생성이 같은 AI 맥락 목록을 받음 · 도구 조회는 보조) · **001**(AX 회의 생성 = 업무 생성과 **같은 흐름·디자인**(쪽 나눔·거절·초안 저장·단추 모양), **내용은 회의 고유 필드** — OQ-901) · **003/016**(생성·수정 모두 회의실 셀렉트: 수정 때 맨 위 「기존 — 회의실 N (변경 안 함)」 · 구분선 · 「회의실 예약 없음」 · Connect 가용 목록 / 생성 땐 첫 줄 없음 / 새 조건에서 기존 방 불가면 비활성+이유 · 생성 직전 재확인 · 「가용 없음」 vs 「조회 실패」 문구 구분 · 수정은 Connect 예약 수정(방 변경 포함) · AX 수정 카드 `meeting.info.update` 에 회의실 선택). 
- SCAX-SPEC-004 의 어느 절을 바꾸는지 매 조문에 「원본 §n → 이 판」 으로 적는다
- §4 Interface Contract: 바뀌는 API·필드·오류만. 새 테이블(보정 표)은 SPEC 엔 「사용자에게 보이는 보정 표 항목(STT 표기·정확 표기·등급)」 만, 스키마는 WORK 의 Domain/Schema 에

### 3-3. `P/30-work/work-012-enhance.md` 신설

- 원칙 절에 고정: **구현은 두 판**(1루프 계약대로 → 사용자 E2E(**데스크톱 앱**) → 2루프) · 완료 = 앱 실물 · 백엔드 커밋 뒤 스택 재시작 · 외부 서비스(Connect·Gmail·Slack·Codex) 경로는 실물 호출 1회가 완료 조건
- **Phase = DEC-009 WP 묶음 순서**: WP1 운영 버그(002/004 · 005 · 006 기한 · 014 · 018 · 010) → WP2 회의록 생성 고도화(006 나머지) → WP3 AX 흐름(017 · 001 · 003/016) → WP4 메시지함→AX(015 · 008 · 012 · 맥락 계약) → SHELL(011 하위 프레임 허용 · dmg — 013② ③ 은 사용자 GUI 확인 체크리스트로). WP 마다 BE·FE 로 나누고 **선후(BE 계약 고정 → FE)** 와 병렬 가능 여부를 적는다
- **Code Surface — 전수**: 각 Phase 가 닿는 파일을 조사 리포트의 파일:줄로 **전부** 센다. 「고칠 곳 N개」 목록이 아니라 **「같은 심볼·패턴을 쓰는 곳 전부」** 를 grep 해 개수와 함께 적어라(예: 참고 자료 `resource_type` 나열 지점 5곳 · 다운로드 입구 18곳 중 바뀌는 것 · `timeout_seconds` 호출 전부 · `next_meeting_after` 호출 전부). 빠진 자리가 다음 판 FAIL 이다
- Phase 마다 **검증**(Makefile 타겟 — 코드 레포 `C/AGENTS.md` 의 규칙) · **Done Criteria**(앱에서 무엇을 보면 끝인가) · 사용자 E2E 체크리스트(앱)
- Domain/Schema 초안: 용어 보정 표 · 안건 출처 · 메시지 참고 자료 종류 · 업무 출처(메시지 링크)·「업무 만듦」 표시 — 마이그레이션 필요 여부
- Pre-deploy(env 신설값 — timeout 넷) · Rollback · Open Issues

## 4. 하지 말 것

- 코드를 고치지 마라(읽기는 된다). DEC 를 고치지 마라 — 결정이 부족하면 SPEC §7 / WORK Open Issues 에 OQ 로 올리고 보고에 적어라(**추측으로 메우지 마라**)
- index(`20-spec/README.md` · `30-work/README.md` · `10-decision/README.md`)·`log.md`·`improvements/`·`_RESUME.md` 를 고치지 마라 — 코디가 한다
- 운영 서버·DB 접속 금지 · 실명·메일·토큰 금지

## 5. allowed_paths

- `P/20-spec/spec-008-external-channels.md` (개정)
- `P/20-spec/spec-010-meeting-ax-enhance.md` (신설)
- `P/30-work/work-012-enhance.md` (신설)

커밋·push 금지.

## 6. 검증

- DEC-009 의 결정 D-01~ 이 SPEC-008·010 어느 한 곳에 **빠짐없이** 대응한다 — 대응표(결정 → SPEC 절)를 WORK 부록에 두고 개수를 보고에 적어라
- WORK Code Surface 의 grep 개수표가 있다
- `git -C /Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2 status --short` 에 위 세 파일만 바뀌었다(`orchestration/work/` 는 코디 몫)

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 코디handle 은 세션 재연결로 바뀐다 — 확실하지 않으면 코디에게 [질문] 으로 묻지 말고 preamble 값을 따르라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_367ca23a-f846-44c0-afc7-07b6655df214 --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: SPEC-008 v0.6.0 · SPEC-010 · WORK-012" \
  --body "파일 경로 / 결정 대응 개수 / Phase 요약 / grep 개수표 요지 / OQ"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_367ca23a-f846-44c0-afc7-07b6655df214 \
  --text "[worker_done] writer SPEC·WORK 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_367ca23a-f846-44c0-afc7-07b6655df214 --text "[질문] writer: <질문>" --enter`
