# architect 리포트 — 회의록 재작업 WP 5건 (WORK-010 ~ 014)

작성 2026-09-07 · 워커 `architect` · 브리프 `docs-v1-meeting-wp-brief.md`
표본 = `30-work/work-009-mcp-token.md`. 산출물은 코디 워크트리에만 남겼다(**커밋·push 안 함**).

## 1. WP 별 요약

| WP | 제목 | Phase | 신규 | 수정 | 폐기 | Open Issues | 코디가 볼 것 |
|---|---|---|---|---|---|---|---|
| **WORK-010** 회의 시작 | `/start` 는 전이만 · 웜스타트는 컨텍스트 없이 백그라운드 | **2**(BE 2) | 3 | 5 | 5 | 3 | **리비전 0건 · 프론트 0건.** `_agenda_rows` 를 여기서 **안 지운다**(011·012 가 아직 쓴다)는 판단이 맞는지 |
| **WORK-011** 회의 중 | 배치 입력은 발화뿐 · AI 트랙 전량 교체 · 슬래시 5 · 줄 시각 제거 | **4**(BE 2 · FE 2) | 1 | 18 | 2 | 4 | **스키마 파일 소유 = 011**(§2). `run_final` 계열을 「빌드만 되게」 남기는 과도기 규칙 |
| **WORK-012** 회의 종료 | async 재전사 → 최종 회의록 한 번 · 용어 보정 · payload | **4**(BE 3 · FE 1) | 2 | 18 | 6 | 5 | **리비전 `0008`** · **SYS-OQ-5 실물 확인이 Phase 1 안에** 들어 있다 · `meeting_merge_service` 폐기 |
| **WORK-013** 편집 · 정리 | payload 드로어 둘 · 칩 둘 갈래 · 자리 유지 · 모달 420 · 유형 설명 | **5**(BE 2 · FE 3) | 4 | 22 | 4 | 4 | **리비전 `0009`** · 드로어 둘은 **수정(폐기 아님)** · `RelationPopover` prop 하나가 「업무 화면 수정」이 아닌 근거를 §Open Issues 에 적었다 |
| **WORK-014** 목록 · 상세 UI | breadcrumb 링크 · 「←」 · 미리보기 패널 · 헤더 순서 | **3**(FE 3) | 2 | 10 | 0 | 4 | **백엔드 변경 0** · `PageHeader.tsx` 가 **없어서** `AppShell` 안에 `DetailHeaderBar` 를 두기로 한 것 |

- 「신규/수정/폐기」는 각 문서 §Code Surface 표의 행 수다(테스트 파일 포함).
- 다섯 문서 모두 WORK-009 와 같은 절 구성 — frontmatter · Meta · Work Summary · Role Assignment · Scope(포함/제외) · Code Surface · Domain/Schema · Dependency · **Internal Interface Contract** · Execution(Phase 마다 작업/검증/완료 증거) · Pre-deploy Check · Rollback · Done Criteria · Open Issues · Related.

## 2. 스키마 파일 소유 — 하나로 정했다

**`app/back/ai_schemas/meeting_notes.json` 은 WORK-011 이 만든다.**

- 011 이 `git mv meeting_batch.json meeting_notes.json` + 모양 재작성(`{headline, termCorrections, agendas[{humanAgendaId, title, lines[]}]}`, 셋 nullable).
- 012 는 **읽기만** 한다(`output_schema` 로 걸고 `_parse_output(fill_final=True)` 로 판다). 012 가 폐기하는 것은 **`meeting_integration.json`** 하나다.
- 근거 — ① 의존 순서가 011 → 012 ② 검증 함수(`_parse_output`·`_demote_if_needed`·`_persist`)도 011 이 만들고 012 가 스위치만 켠다(SPEC-008 §5 「다른 것은 「버리나 채우나」 스위치 하나뿐」). 파일과 함수 소유를 같은 WP 에 뒀다.
- README 「회의록 재작업 그룹」 밑에 이 문장을 한 줄로 박아 뒀다.

## 3. 같은 파일을 두 WP 가 만지는 곳 — 순서를 Depends 에 적었다

| 파일 | 만지는 WP | 순서 · 처리 |
|---|---|---|
| `service/meeting_batch_service.py` | 010(웜스타트) · 011(배치) · 012(`run_final` 폐기) | **010 → 011 → 012.** 각 WP 의 Depends on work 에 적었다 |
| 〃 `_agenda_rows()` | 010 이 호출자 하나를 지움 · 011 이 둘째 · **012 가 최종 폐기** | 브리프는 010 에 「`_agenda_rows` 폐기」로 적었으나 **실물상 011·012 가 아직 부른다**(grep). 010 에서 지우면 011 이 깨진다 → **012 가 폐기**로 옮기고 010 §Open Issues 에 「결정이 아니라 순서 사실」로 기록 |
| 〃 `_task_rows()` · `_date()` | **010 만** | 유일한 호출자가 `build_warm_start_prompt` 였다(grep 확인) → 010 이 폐기 |
| 〃 `_parse_output` · `_demote_if_needed` · `_persist` | 011(신설·재작성) · 012(`fill_final` · `track` 인자 확장) | **011 → 012.** 012 는 **복제하지 않는다**를 Internal Interface 에 못박음 |
| `config.py` | 009(토큰 TTL · 완료) · 011(`meeting_batch_chars` 1000) · 012(재전사·최종 수치) | 011 → 012 |
| `service/meeting_service.py` | 009(토큰 INSERT 한 줄 · 완료) · 010(commit·웜스타트 제거) | 009 → 010. 010 은 **009 가 넣은 줄을 유지**한다 |
| `integrations/agent.py` | **009 만** | 010·011·012 는 `build_codex_options` 를 **부르기만** 한다 |
| `integrations/soniox.py` | 012 만(async 갈래 추가 · 실시간 갈래 불변) | — |
| `components/LineRow.tsx` | 011(시각 제거) · 013(`LineKindSelector` 제거) | **011 → 013** |
| `components/AgendaLineTree.tsx` | 013(`onChangeKind` 제거) · 014(`density` 추가) | **013 → 014.** 014 는 계약상 독립이지만 **머지는 013 뒤** |
| `components/MeetingClosedPage.tsx` | 012(생성중·실패·푸터) · 014(헤더 순서) | **012 → 014** |
| `components/MeetingStatusBar.tsx` | **012 만**(카운트 다섯 · phase 둘 · 「다시 시도」) | 014 는 안 만진다 |
| `components/MeetingDetailBody.tsx` | **013 만** | — |
| `schemas/meeting.py` | 012(`pending_change`→`payload` 이름) · 013(두 모양 · `kind`·`newTask` 제거) | **012 → 013** |
| `models/meeting.py` · alembic | 012(`0008`) · 013(`0009`) | 리비전 체인 `0007`(009) → `0008`(012) → `0009`(013) |

## 4. 브리프와 달라진 것 — 실물 확인으로 고친 이름

| 브리프 표기 | 실물 | 어디에 |
|---|---|---|
| `HeadlineBar` | **`MeetingStatusBar`** (`variant="headline"` · `layout="single"\|"stacked"`) | WORK-012 §Code Surface |
| `useMeetingFinalizeJob` 상한 1230 | 현행 상수는 **`JOB_POLL_MAX_COUNT = 480`** — 1230 으로 올린다 | WORK-012 Phase 3 |
| `PageHeader` | **파일이 없다.** `AppShell.tsx` 가 breadcrumb 슬롯을 갖고 있어 그 안에 **`DetailHeaderBar`(신규)** 를 둔다 | WORK-014 §Code Surface · Open Issues |
| `mergedSummary` 키 둘 추가 | 현행 `{agendaCount, decisionCount, actionCount, integratedAt}` → **`{agendaCount, discussionCount, decisionCount, actionCount, taskCount}`**(`integratedAt` **삭제**) | WORK-012 |
| `meeting_task_link_service.apply_pending_change` | → **`apply_task_update(body)`**. `_stored_change()` 도 함께 폐기(줄의 저장값을 요청으로 쓰지 않는다) | WORK-013 |
| `_demote_if_needed` 기준을 검사 시점 조회로 | `_BatchInput.whitelist` 프로퍼티를 폐기하고 `_run_once` 가 ④ 직전에 조회해 넘긴다 | WORK-011 Internal Interface |
| `job.error_code` 5종 | 현행 enum 은 **3종**(`integration_failed`·`integration_timeout`·`job_timeout`) → 5종 교체 + `JobPhase` 도 `transcription`·`final` 로 | WORK-012 Phase 0 |
| `batch_run.phase` CHECK | 현행 `BatchPhase` 에 `INTEGRATION` 이 **있다** → 삭제. 기존 `integration` 행은 리비전이 지우고 CHECK 재작성 | WORK-012 Phase 0 |

## 5. 새로 만들지 않은 결정 — Open Issues 로 남긴 것

- **SYS-OQ-5**(헤더 없는 webm 을 `stt-async-v5` 가 받나) — WORK-012 Phase 1 **안에서 파일 하나로 확인**하고, **거절하면 사실만 보고**한다. 녹음 컨테이너를 바꾸는 것은 여기서 하지 않는다(SPEC-007 §C-8 이 포맷을 못박지 않았다 = 사용자 결정 영역)
- **OQ-10 · 11 · 12** — 전부 **「SPEC 대로」**로 적었다. 새로 묻지 않는다. (`context.terms` 비움 → 012 / 「미팅·회의」 시드 빈 값 → 013 / 유형 `null` → 013)
- **드로어 파일 이름** `CreateTaskFromLineDrawer.tsx` · `LinkTaskDrawer.tsx` 는 **그대로 쓴다**(브리프 「수정 · 폐기 아님」). 이름이 새 뜻과 어긋나 보이지만 rename 은 범위 밖 — 013 §Open Issues
- **`ai-prompt-draft.md` §B 와 MF-53 의 어긋남** — 초안은 「새로 드러난 것만 · 앞서 낸 줄은 건드리지 마라」인데 계약(SPEC-007 §4 「배치 입력」)은 「AI 트랙 전체를 다시 정리해라」다. **§B 에서 가져오는 것은 「조회 순서」 절이고 요청 문장은 계약을 따른다** — 초안 < 계약 < `Meeting flow.md` 순서를 적용한 것이라 새 결정이 아니다. 011 §Open Issues 에 명시
- **웜스타트 태스크의 수명** — 프로세스가 죽으면 사라지고 그 회의는 `ai_session_id` `NULL` 로 남는다. **MF-70 대로 아무 처리도 하지 않는다**(job 행이 없어 기동 스윕 대상도 아니다). 010 §Open Issues
- **업무 상세의 `backTo` 한 줄** — 「업무 화면은 안 고친다」의 경계. 공용 부품이 `backTo` 를 요구하므로 넘기지 않으면 업무 상세에 「←」가 없다. MF-7 「공용 부품이라 한 번에 고친다」로 이미 답 — 014 §Open Issues
- **`RelationPopover` 단일 선택 prop** — SPEC-008 §5 · FE §2 규칙 8 이 「그대로 재사용한다(단일 선택 prop 하나만 더한다)」로 이미 허용. 새 결정 아님 — 013 §Open Issues

## 6. 계층 · 게이트 · 시안 규칙 반영

- **계층** — `payload` 를 쓰는 표면 둘(`POST/PATCH …/lines`)은 **`task_service` 를 import 하지 않는다**를 013 Internal Interface + 정적 검사로. 업무를 바꾸는 회의록 코드는 `meeting_task_link_service` 의 **두 함수뿐**
- **게이트** — `payload.status` · `PATCH …/task` 본문 `status` 가 **같은 `Literal["todo","in_progress"]` 를 공유**한다(013). `done`·`cancelled` 는 **스키마 층 422**. 회의록에 판정 코드 없음
- **트랜잭션** — 010(`/start` 는 commit 안 함) · 011(전량 교체 한 트랜잭션 · 검증 뒤에만 DELETE) · 012(①·② 각자 세션 · 외부 호출 중 트랜잭션 0 · ② 성공은 한 트랜잭션) · 013(`PATCH …/task` ①~⑧ 한 트랜잭션)
- **시안** — 013 의 payload 드로어 둘은 **새 시안 없음**을 명시하고 「업무 드로어 부품 규격을 가리켜 조립」 + **`features/tasks` 두 드로어의 `git diff --stat` 0줄**을 정적 검사로 넣었다. 014 도 시안 없이 FE §6-3 · §7-1 조립
- **범위** — 다섯 문서 어디에도 캘린더 · 문서함 · 업무 화면을 고치는 항목이 없다(014 의 공용 `Breadcrumb` 은 MF-7 이 명시적으로 요구한 것)

## 7. 산출물

```
para/projects/summer-star/task-management/30-work/
  work-010-meeting-start.md      (220줄)
  work-011-meeting-live.md       (283줄)
  work-012-meeting-close.md      (308줄)
  work-013-meeting-edit.md       (336줄)
  work-014-meeting-list-ui.md    (239줄)
  README.md                      (회의록 재작업 그룹 표 5행 제목·Depends·Phase 갱신 + 스키마 소유 한 줄)
```

그 밖의 파일은 손대지 않았다. 커밋·push 하지 않았다.
