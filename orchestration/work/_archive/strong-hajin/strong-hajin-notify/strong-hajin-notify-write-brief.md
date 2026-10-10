# [writer] 알림 — BASE-009(입력 눕히기) · DEC-010(결정) 작성

너는 **strong-hajin `writer` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 문서 규칙: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/project.md` · 각 폴더 `README.md`(`00-baseline/` · `10-decision/`)
- **모양의 본보기**(바로 앞 판): `P/00-baseline/baseline-008-enhance-improvements.md` · `P/10-decision/decision-009-enhance.md` — 머리(frontmatter)·읽는 규칙·표기·절 구성을 이대로 따른다

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga` (코디 워크트리에 직접 탄다)
경로 약어: `P/` = `para/projects/summer-star/strong-hajin/` · `W/` = `orchestration/work/strong-hajin-notify/` · `D/` = `reference/2026-09-10-sc-meeting/package 2/`

⚠ **코디와 같은 트리다.** 아래 allowed_paths 의 파일만 만든다. 다른 파일(특히 `_RESUME.md` · index·log · 시안 사본)은 **읽기만** 한다.

## 1. SSOT — 원료 (여기 없는 것은 발명하지 마라)

| 원료 | 무엇 | 경로 |
|---|---|---|
| 결정 원장 | 날짜별 사용자 결정 · 코디 기본값(사용자 확정) — **이 판의 정본** | `W/_RESUME.md` §2 (2026-10-07 · 10-08 행 전부. 취소선 행은 뒤집힌 것) |
| BE 조사 | 알림 원천·생성 자리·사건×관련자 표(§6)·실시간 경로·설정 저장 자리 | `W/be-survey-report.md` |
| FE 조사 | 화면 렌더링·실시간 수신·설정·사이드바·Tauri 셸 | `W/fe-survey-report.md` |
| 시안 | 알림 목록 · 설정 알림 — **확정 시안이 정본** | `W/design-change-1.md` · `W/design-change-2.md` · `D/Alerts.html` · `D/handoff/alerts/` · `D/handoff/settings/js/data.js`(`NOTIFY_GROUPS`) · `D/handoff/shell/js/nav.js` |
| 뒤집거나 채울 결정 | 「설정 알림 메뉴 범위 밖」 · 「OS 알림은 래퍼 책임, 알림 시스템은 후속」 · 「만들지 않는 것」 표 | `P/10-decision/decision-008-external-channels.md` D-37 · D-50 · `P/10-decision/decision-005-tauri-wrapper.md` D-04 · `P/20-spec/spec-006-tauri-wrapper.md` §2.5 |

**기대는 개념** — 판단 근거가 된 개념이 `para/areas/area.md` §3.4 맵에 있으면 DEC 의 `up:` 에 링크한다(예: 실시간 전달·이벤트 재전송·human-in-the-loop 류). 맵에 없으면 만들지 말고 보고에 「개념 후보」 로 적는다.

## 2. 배경

사용자가 strong-hajin 에 **알림**을 만든다. 조사(BE·FE) → 시안 둘(알림 목록 · 설정 알림) → 사용자 결정까지 끝났다. 이 판은 그것을 **BASE(입력) → DEC(결정)** 두 문서로 굳힌다. 다음 판이 SPEC 과 WORK 를 쓴다 — **이 판에서는 SPEC·WORK 를 쓰지 않는다.**

## 3. 만들 것

### 3-1. `P/00-baseline/baseline-009-notifications.md` — BASE-009

- **판단하지 않는다.** (사용자) 요구 · (조사) 현재 코드 동작 · (시안) 그린 것을 눕힌다. 근거 표기는 BASE-008 「읽는 규칙」 방식
- 절(제안): 요구 원문 · 지금 있는 알림(1곳·화면 미사용) · 사건과 관련자(BE §6 표를 옮겨 싣는다) · 실시간 경로(WS 2 · 게시 프로세스 · 커서 없음) · 화면(사이드바·설정·메시지함 점 없음) · Tauri 셸(알림 수단 0 · 창 수명) · 시안 · 어긋남(조사·시안·기존 결정 사이) · 실측 필요(FE 조사)
- 가린 것: 사람 실명·메일·토큰 금지

### 3-2. `P/10-decision/decision-010-notifications.md` — DEC-010

- 상태 `accepted`. 결정마다 **D-01 …** 번호 · 근거(사용자 날짜 · 조사 절 · 시안 절). **코디 기본값으로 정해진 것**(원장에 「코디 기본값」·「코디 추천」 으로 적힌 것)은 그렇게 표시
- 담을 결정(원장 그대로 — 빠짐없이):
  - 알림 대상 네 묶음 · 「나와 관련된 것만」 · **받는 사람의 관계에 따라 알림이 다르다**
  - 시스템 알림 = 앱이 켜져 있을 때만 · 웹이 받아 셸(Rust)이 띄운다 · 서버→기기 푸시 없음 · 창 닫으면 끊김
  - 실시간 = **사용자 사건 채널 하나 · SSE** — 지금 `/api/inbox/stream` WS 를 대체 · 알림과 메시지함 사건을 함께 · 회의 WS 는 별개 유지 · 재연결 때 놓친 알림을 다시 준다(사건 id) · 메시지함 외 워커(회의록 등)도 사건을 낼 길을 낸다
  - 사이드바 알림 → 알림 목록 화면 · **알림·메시지함 둘 다 점**(숫자 없음)
  - 설정 알림 = 전체 · 테마(업무·메시지·회의) on/off · 항목 체크 — **항목은 시안 `NOTIFY_GROUPS` 그대로**(업무 8 · 메시지 3(메일·슬랙·카톡) · 회의 5). 연동 끊김은 채널 항목에 딸림
  - 끄면 목록에도 안 쌓인다 · 관계 둘 이상이면 담당 > 요청자 > 참조 꼬리표 하나 · 슬랙 채널은 방별로 안 읽은 동안 한 줄 합침
  - 받는 경로 = 앱만
- **사건 × 관계 표**(이 판의 핵심): BE §6 의 사건마다 「어떤 관계의 사람에게 · 어느 설정 항목으로 · 어느 테마로 · 알리나/안 알리나」. **원장에 행 단위 결정이 없다** — 그러니 이 표는 **「기본값(코디 제안) — 사용자 검토 대상」** 으로 머리에 표시하고, 원칙만 따른다: ① 내가 한 행동은 나에게 알리지 않는다 ② 설정 항목에 대응이 없는 사건은 알리지 않는다(표에 「알림 없음 — 항목 없음」) ③ 관계가 없는 사람에게는 알리지 않는다. 판단이 갈리는 행은 OQ 로
- **뒤집거나 채우는 결정**을 인용해 적는다(원 파일은 고치지 마라): ~~DEC-008 D-37 설정 알림 메뉴 범위 밖~~ → DEC-010 · DEC-005 D-04 「알림 시스템은 후속」 → 이번 판이 그 후속 · SPEC-006 §2.5 표의 칸 중 이번에 여는 것(권한 요청·표시·이벤트 정의·클릭 딥링크)과 계속 안 여는 것(푸시·트레이·배지)
- **계약 조문(필드·엔드포인트·테이블·SSE 경로 이름)은 쓰지 않는다** — DEC-009 머리말과 같은 선. 「무엇을 채택·버리나」 까지
- 끝에 **「이번 범위 밖」**: 기한 하루 전 · 일일 요약(스케줄러 없음) · 메일·슬랙 DM 받는 경로 · 알림 보관 기간 · 방해 금지·소리 · 창을 닫아도 받기(트레이) · 서버→기기 푸시
- 끝에 **「WP 묶음(제안)」** — 순서만(상세는 WORK 몫): 예) 사건 채널(SSE) 교체 → 알림 생성(사건×관계) + 설정 저장 → 화면(알림 목록·사이드바 점·설정) → 셸 시스템 알림. 원료와 어긋나면 OQ
- **실측 필요**(FE 조사 §실측): OS 알림 권한·서명 영향 · 숨김/최소화 웹뷰의 연결·타이머 — 결정이 아니라 WORK 의 실측 항목으로 넘긴다고 적는다
- Open Questions: OQ-1001~. **추측으로 메우지 마라**

## 4. 먼저 읽을 핵심

- `W/_RESUME.md` §2 — 결정의 정본
- `W/be-survey-report.md` §0 · §6 · `W/fe-survey-report.md` §0 — 한 줄 요약과 사건 표
- `W/design-change-1.md` §2·§3·§6 · `W/design-change-2.md`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `P/00-baseline/baseline-009-notifications.md` (새로 만든다)
- `P/10-decision/decision-010-notifications.md` (새로 만든다)

index(`README.md`)·`log.md`·`_RESUME.md`·시안 사본·다른 DEC/SPEC 은 **고치지 마라** — 코디가 한다. 커밋·push 금지.

## 6. 단계

1. 원료 전부 읽기 → 2. BASE-009 → 3. DEC-010 → 4. 자체 점검(§8)

## 7. 하지 말 것

- SPEC·WORK 를 쓰지 마라. 코드 레포를 고치지 마라(읽기는 된다)
- 원료에 없는 결정·수치를 만들지 마라. 원료끼리 어긋나면 OQ 로 올리고 보고에 적어라
- 운영 서버·DB 에 접속하지 마라

## 8. 검증

- 두 파일이 있다 · frontmatter 가 본보기와 같은 키 · `links` 가 서로를(BASE-009 ↔ DEC-010) 그리고 DEC-008 · DEC-005 · SPEC-006 을 가리킨다
- 원장 §2 의 2026-10-07·10-08 결정 행이 DEC-010 에 **빠짐없이** 나온다 — **행 개수와 D 번호 대응을 세어 보고에 적어라**
- 시안 `NOTIFY_GROUPS` 항목 16개(업무 8 · 메시지 3 · 회의 5)가 사건 × 관계 표에 전부 대응된다 — 대응 없는 항목이 있으면 OQ
- `git -C /Users/kknaks/orca/workspaces/kknaks_profile/beluga status --short` 에 두 파일만 새로 생겼다(코디의 다른 변경은 원래 있던 것)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 코디handle 은 세션 재연결로 바뀐다.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_aa9fb9af-eed1-45ee-baad-95e52082321d --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: BASE-009 · DEC-010" \
  --body "파일 경로 / 결정 개수 · 뒤집은 결정 · 기본값 표시 / 원장 행 대조 / 항목 16 대조 / OQ / 개념 후보"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d \
  --text "[worker_done] writer BASE-009 · DEC-010 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
