# [planner] 회의·미팅노트 — 결정 반영 + SPEC-004 재작성 (기획서는 기획자 소유 — 건드리지 않는다)

너는 **sc-ax `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/roles/sc-ax/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec` (branch `kknaksss/sc-meeting-spec`)
base 브랜치: `origin/main`(59cd71302) → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리를 쓰는 다른 워커는 없다.

## 1. SSOT — 먼저 읽을 것

**기획 정본 (사용자 지정 2026-09-10)** — 이 둘이 이번 작업의 값의 정본이다. 코디 워크트리에 있다(read-only 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/reference/2026-09-10-sc-meeting/plan-004-meeting-note.md` — PLAN-004 v1.0.0 (2026-09-09). 리포 안의 `products/sc-ax/00-planning/plans/plan-004-meeting-note.md` 는 v0.1.2(2026-08-25)로 **낡았다.** 이 reference 본이 이긴다. **리포의 기획서를 고치거나 교체하지 마라 — 기획자가 올린다.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/reference/2026-09-10-sc-meeting/screen-005-meeting-note.md` — SCREENDEF-005 v1.0.0. 리포에는 아직 없다. **만들지 마라 — 기획자가 올린다.** SPEC 은 이 reference 본의 ID(SCR-105·SCR-106·MOD-102/104/105·요소 ID)를 그대로 인용한다.
- ⚠ 두 문서가 가리키는 `확정사항.md`(`X-###`)·`내부-결정지도.md`(`D-###`)는 **무시한다**(사용자 지시). 코드는 그대로 두되 풀려고 하지 마라. 본문 서술이 값이다.

**현행 코드 사실** — 조사 리포트. 사실만 인용하고 판단은 하지 않았다:

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/survey-01-ai-provider-report.md` — §0 세 줄 요약 · §4 회의 AI 경로 5단계 · §4.4 프로토타입 요구 3건 「없음」 · §6.2 문서≠코드 8건

**회의 백엔드 플로우 정본 = task-management** (사용자 결정 2026-09-09). 코디 워크트리 문서(read-only):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/20-spec/spec-007-meeting-live.md` — §4 「WS 메시지 계약 `WS /api/meetings/{id}/stream`」·「AI 배치 계약」·Case Matrix. **중계 WS·AI 중간 요약의 계약 원형.**
- 같은 폴더 `spec-006-meeting-setup.md` · `spec-008-meeting-close.md`(종료·합성) · `40-architecture/database/domains/meeting.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/_archive/task-management/docs-v1/soniox-study.md` — Soniox 실시간 STT 사실(토큰 모델·화자 분리·한도)

**리포 안 문서** (작업 워크트리):

- `products/sc-ax/20-spec/spec-004-meeting-note.md` — 재작성 대상. 현재 87줄, §1~§7.
- `products/sc-ax/10-decision.md` — 결정 로그 형식(「현재 결론 / 미완료 / 완료 / 로그」)
- `products/sc-ax/40-architecture/system.md` §4 「Meeting provider와 worker」 — 갱신 대상
- `products/sc-ax/00-planning/screens/modules/screen-004-work-management.md` — 화면정의서 자리·형식 선례
- `rules/document-pipeline.md` · `AGENTS.md` — frontmatter·파이프라인

**기대는 개념** — 해당 없음(코디 워크트리 `para/areas/concept/` 에 회의 도메인 개념 문서가 아직 없다).

## 2. 배경 / 무엇을 바꾸나

sc-ax 에 「회의·미팅노트」 1차를 만든다. 기획(PLAN-004·SCREENDEF-005)이 2026-09-09 에 크게 개정됐는데 개발 정본(`products/sc-ax/`)에는 8월 본만 있고, 화면정의서는 아예 없다. 그리고 사용자가 2026-09-09~10 에 기획 위에 결정을 더 얹었다. **역할 경계: 기획서(00-planning/)는 기획자가 소유하고 직접 올린다. 우리(개발)는 스펙부터다.** 이 작업은 **reference 기획서 + 사용자 결정을 기준으로 SPEC-004 를 다시 쓰고, 결정을 기록하고, 아키텍처 §4 를 맞추는 것**이다. 기획서와 어긋나는 결정(D1·D2)은 기획서를 고치지 말고 **「기획 개정 요청」 목록**으로 남겨 기획자에게 넘긴다(SCREENDEF-005 가 `plan-004 #N` 티켓으로 하는 방식과 같다).

현행 코드(ax-workspace)는 회의를 캘린더 안 드로어로 다루고, 브라우저가 Soniox 에 직접 붙고, 실시간 전사를 임시로 두고 녹음 파일을 다시 전사해 정본을 만들며, note 를 version 으로 쌓고 AI 요약을 「채택」해 붙인다. **이 구조는 기획·결정과 전부 어긋나므로 SPEC-004 는 부분 수정이 아니라 재작성이다.**

### 사용자 결정 (2026-09-09 · 09-10) — 그대로 반영한다. 재논의 금지

| # | 결정 | 기획 문서와의 관계 |
|---|---|---|
| D1 | **나와 AI 둘이 회의에 들어간다.** 회의 중 「사람 메모 트랙」과 「AI 중간 요약 트랙」(안건별로 차오름)이 각자 쌓이고, **회의가 끝나면 둘을 합쳐 최종 회의록 한 벌**이 된다. 합치는 것은 자동이고 사람이 「채택」하는 단계는 없다. 합쳐진 뒤 만든 사람이 [수정]/[저장]으로 고친다 | PLAN-004 DEC-003(「한 층 — 노트와 요약을 나누지 않는다」)과 어긋난다. **SPEC 은 D1 을 따르고, 기획서에는 개정 요청으로 남긴다**(기획자 몫). 「판을 쌓지 않는다·덮어쓰기」는 유지 |
| D2 | **STT 는 Soniox, 백엔드가 중계한다.** 브라우저는 오디오를 우리 서버 WS 로 보내고, 서버가 Soniox websocket 세션을 소유한다. 기획의 「소니웍스 PC 음성 인식」= Soniox 다 | PLAN-004 DEC-004·X-197 문구(「우리가 엔진을 붙이지 않는다」)와 표현이 다르나 뜻은 같다 — 개정 요청 목록에 「문구 명확화」로 올린다. OQ-201(실시간 회의록을 개발측이 받나) → SPEC 에서 **받는다** 로 답한다 |
| D3 | **실시간 전사가 정본.** 종료 후 녹음 파일 재전사(현행 `stt-async-v5` 2-pass)는 **완전히 없앤다.** AI 요약의 근거는 실시간 구간에 결박된다 | SPEC-004 §4·§5 재작성 근거 |
| D4 | **오디오 원본은 서버가 보관한다.** 「나중에 원본이 필요한 경우」가 근거. 구체 용도(재생·감사)는 Open Question 으로 남긴다. 화면에는 내지 않는다(기획 X-164) | — |
| D5 | **회의 백엔드 플로우는 task-management 를 따른다** — WS 스트림 계약, AI 중간 배치, 종료 처리. 정제(refinement)·화자 매핑 시점도 그 플로우 | spec-007/008 을 원형으로 SPEC-004 계약을 쓴다 |
| D6 | **참석자에게 실시간 스크립트·AI 요약을 밀어주는 것은 WS.** 중계 WS 와 같은 채널 | — |
| D7 | **300분 초과 회의는 없다고 가정.** Soniox 세션 회전 미구현. SPEC 에 한도로 명시 | — |
| D8 | **기획이 정본.** 판 없음·덮어쓰기(X-136·X-139 폐기), 확정 표시 없음(X-119 폐기), 재생성 없음(X-16 개정), 수정은 만든 사람 하나(DEC-005), 화면에 「녹음」 표기 금지(DEC-009), 메뉴는 「회의 목록」(DEC-015), 상태 6개(예정·진행 중·정리 중·정리됨·실패·취소됨) | 기존 SPEC-004 의 versioned note·finalize·adopt 는 **폐기** |
| D9 | Claude Design 시안(회의실 2탭·회의록 목록)은 **참고용**이다. 정본이 아니다. 워커는 접근할 수 없으므로 참조하지 마라 | — |

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음 — 이 작업이 계약을 **만드는** 자리다. BE/FE 워커는 이 SPEC 이 사용자 리뷰를 통과한 뒤에 발주된다.

## 4. 먼저 읽을 핵심 파일

- reference `plan-004-meeting-note.md` §4 범위 · §6 흐름 B · §7 데이터 요구 · §14 확정된 결정 · §16 미결
- reference `screen-005-meeting-note.md` §3 메뉴 구조 · **SCR-106**(395~858줄: E29 회의록 본문 · E80~E83 메모·진행 중 정리 · E26 스크립트 탭 · §5.7 상태별 표) · §7 미결(OQ-201·OQ-209)
- `survey-01-ai-provider-report.md` §4.1(현행 5단계) · §4.4(없는 것 3건) · §6.2(문서≠코드)
- task-management `spec-007-meeting-live.md` §4 Interface Contract 전체
- `products/sc-ax/20-spec/spec-004-meeting-note.md` 전체(87줄) — 무엇을 버리고 무엇을 남기는지 §6 에서 판단
- `products/sc-ax/10-decision.md` · `40-architecture/system.md:63-72`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/sc-ax/`
- 그 안에서도 이번 작업은 **아래 3개 파일만** 고친다: `20-spec/spec-004-meeting-note.md` · `10-decision.md` · `40-architecture/system.md`(§4 만). **`00-planning/` 은 읽기 전용 — 기획자 소유.** 다른 spec·screen 도 읽기만.

## 6. 작성 단계

1. **결정 기록** — `products/sc-ax/10-decision.md` 「로그」에 2026-09-09·09-10 결정 D1~D8 을 형식대로 추가하고 「현재 결론」을 갱신한다. 폐기되는 기존 결정(versioned note·adopt·2-pass·브라우저 직결)이 있으면 「레거시」로 내린다.
2. **SPEC-004 재작성** — `products/sc-ax/20-spec/spec-004-meeting-note.md` 를 reference 기획서(PLAN-004 v1.0.0·SCREENDEF-005 v1.0.0) + D1~D8 기준으로 다시 쓴다. 문서 ID·frontmatter 는 유지하고 `document_version` 을 올린다. 기획서 인용은 reference 본의 절·ID(`FTR-004-NN`·`SCR-106-E29` 등)로 한다. 골격(제목은 네가 다듬어도 되나 다루는 것은 빠짐없이):
   - §1 제공 범위 / §2 미제공·미결 — 기획 §4 In/Out 과 일치
   - §3 Meeting·참석·열람·공유 — 참석자만 열고 공유가 유일한 예외, 회의록 수정은 만든 사람 하나
   - §4 안건(agenda) — 순서·제목·출처·결론 여부, 회의당 20개, 메모와 AI 요약이 안건에 매달린다
   - §5 회의 진행과 스트림 — 상태 6개 전이, **브라우저→서버 WS 오디오 중계→Soniox**, 실시간 전사 정본, 확정/잠정 토큰, 익명 화자 라벨, 오디오 원본 보관(화면 미노출), 300분 한도, 파일 재전사 **없음**. task-management spec-007 §4 의 WS 메시지 계약을 **sc-ax 이름·권한 모델에 맞춰** 옮긴다(복사 아님)
   - §6 메모 트랙 — 만든 사람만, 안건 선택, 자동 저장, 원문은 근거로 남음
   - §7 AI 중간 요약 트랙 — 안건별 증분, 근거 = 실시간 구간 + 메모, 배치 계약은 spec-007 「AI 배치 계약」 원형
   - §8 종료와 합성 — 「정리 중」에서 두 트랙을 합쳐 안건별 본문·다음 할 일 한 벌 생성, 실패→「실패」+[다시 시도], 합성 뒤 수정은 덮어쓰기(판 없음)
   - §9 Follow-up 승격 — 기존 §6 을 기획 §4.1 「후속업무 후보」에 맞춰 유지
   - §10 Functional Rules — 불변 조건 목록
   - §11 **현행 구현과의 차이** — survey-01 사실을 표로: 무엇이 폐기되고(브라우저 직결·realtime credential·2-pass·note version·adopt·MeetingDrawer) 무엇이 남는지(권한 모델·durable job·evidence 결박 개념)
   - §12 **기획 개정 요청** — 기획자에게 넘길 목록. 최소 ① DEC-003 한 층 → 두 트랙 + 자동 합성(D1) ② DEC-004 문구 「소니웍스 PC 음성 인식」→「Soniox, 우리 백엔드 중계」(D2) ③ OQ-201 종결(받는다) ④ 이 작업에서 발견한 기획 내부 모순이 있으면 추가. 항목마다 「기획서 어디 · 무엇을 · 왜(D#)」
   - §13 Open Questions — 기획 §16 의 OQ-005·OQ-006·OQ-209·미결 #81 + 이 작업에서 생긴 것(오디오 보관 용도·두 트랙 화면 표면·정제 시점·화자 이름 매핑 시점·합성 알고리즘의 입력 순서 등)
3. **아키텍처 한 절** — `products/sc-ax/40-architecture/system.md` §4 를 D2·D3 기준으로 고친다(realtime credential 삭제, WS relay, final transcription path 삭제, 오디오 보관). 다른 절은 손대지 않는다.
4. 각 문서 frontmatter `status: draft`. 사실은 §1 SSOT 에서만. **없는 값은 만들지 말고 §13 Open Question 으로.**

## 7. 범위 제약 — 하지 말 것

- **`00-planning/` 아래 어떤 파일도 만들거나 고치지 않는다.** plan-004·screen-005 는 기획자가 올린다. 어긋남은 SPEC §12 「기획 개정 요청」에만 적는다.
- `X-###`·`D-###` 를 풀거나 새로 부여하지 않는다. SPEC 에서 인용할 때는 코드를 그대로 두고 「정본 `확정사항.md` 는 이 리포에 없다」 한 줄만 남긴다.
- WP(`30-work/`)를 만들지 않는다 — 사용자 리뷰 뒤 별도 발주.
- ERD(`40-architecture/erd.md`)·다른 spec·다른 screen·`21-html/` 을 고치지 않는다. 충돌을 발견하면 §12 에 적는다.
- 화면 표면(두 트랙을 탭으로 할지 분할로 할지, 문구)을 네가 정하지 않는다. 기획이 정한 것만 쓰고 나머지는 Open Question.
- Claude Design·ax-workspace 코드·task_management 코드를 읽으러 가지 않는다. 이 브리프의 문서만이 입력이다.
- 코드·문서 수정 금지 대상: `rules/`·`context/`·`templates/`·타 제품.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict 실행 → products/sc-ax/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 「무관」으로 분리 보고). 3개 파일 frontmatter 최소셋 충족. git status 로 변경 파일이 §5 의 3개뿐이고 `00-planning/` 에 변경이 **없는지** 확인. 검증은 1회만
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
  --to term_a53b7eb6-b86f-4486-850f-3f53f53d161c --from term_e155b48b-1a1f-4392-99eb-2889228625e7 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: 회의·미팅노트 SPEC-004 재작성" \
  --body "변경 파일 3개 / SPEC 버전 / D1~D8 반영 위치 / 기획 개정 요청 목록(§12) / lint 결과 / Open Question 수와 목록 / 00-planning 무변경 확인"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_a53b7eb6-b86f-4486-850f-3f53f53d161c \
  --text "[worker_done] planner 완료 — 회의 SPEC-004 재작성. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_a53b7eb6-b86f-4486-850f-3f53f53d161c --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
