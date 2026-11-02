# 재개 노트 — docs-v1 (task-management)

**지금**: **09-08 낮 여기까지(사용자 지시).** 문서 커밋 `6047d8a`(para · reference · config — `orchestration/work/` 는 slug 마감 때). 코드 `kknaksss/docs-v1` HEAD `f0d4d46`(WORK-009~015 · 스키마 400 · LineRow · 팝오버 스크롤 — 커밋 9 · PR 안 열었다). 실물 회의 12 에서 **배치 3~11 이 codex 네트워크 오류로 전부 실패**(worker 컨테이너 → chatgpt.com DNS/stream 끊김 · 13:20~13:54 · 코드 아님 · 지금은 resolve 됨) — 최종 ② 도 같은 이유로 실패하면 앱의 「다시 시도」(/finalize).
**PR(09-08 저녁)**: 코드 kknaks/task_management#2(kknaksss/docs-v1 → main · 50 커밋) · 문서 kknaks/kknaks_profile#42(task-management-app → main · 40 커밋 · origin/main 위로 rebase 완료). 전사 md 는 main 에 직접 `e2728e8`. **머지는 사용자 결정 — 머지 뒤 `scripts/archive-work.sh --dry-run task-management docs-v1` → SUMMARY §1~4·§7 → 실행 → 개념 소화.** 워커 터미널 넷 전부 닫음.
**다음**: ① 야간 보고 §1 결정(웜스타트 phase · errorCode 재진입 · progress.phase · 안내 바 시각 · 현재 값 둘 · 본문↔제목 · 「홈」 라우트 · U-3 · null 키 · 입력 레벨 막대 · 무토큰 안내) ② 버그 3 ② 로그 둘 발주(`docs-v1-stream-stall-brief.md` §4) + WORK-015 검수 WARN 2 ③ 워커 codex 네트워크 오류 원인(컨테이너 DNS) ④ PR → slug 마감(archive-work.sh).

세팅: `scripts/new-work.sh task-management docs-v1` · 설정 SSOT `config/projects/task-management.json`
코디handle: `term_98a33032-2134-4bf9-ac48-e9df737f9b8f`

## 워크트리

- `docs`: 코디 워크트리 공유 (`workspace: coordinator`) — `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app` (branch `task-management-app`, base `origin/main` → PR `main`). 문서 워커는 여기 탑승, 개별 워크트리 없음
- `code`: `/Users/kknaks/orca/workspaces/task_management/docs-v1` (branch `kknaksss/docs-v1`, HEAD `f0d4d46` 팝오버 스크롤(WORK-015 `1ca243e` · LineRow `aa375ed` · 스키마 `dd9d861` · WORK-014 `5c72c25` 위), PR 안 열었다). 010 부터 옛 설계를 순서대로 고친다

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [x] **계약 정정 3차 — 끝**(reflow3-report · 코디 직접 확인 · grep 셋 0건 · SPEC-007 잔존 6곳은 코디가 고침). 브리프 `docs-v1-meeting-reflow3-brief.md`(architect · 코디 트리 탑승). 옮길 것 다섯 = MF-64 정정 · MF-66 전파 · MF-67 · 68 · 69 · 70. 산출물 8문서(SPEC-008 · SPEC-003 · DEC-003 · ERD meeting/account/README · backend · system · frontend README). 끝나면 grep 셋(`agendaSlot|taskSelectorSlot` 0 · 「31건」 0 · `submitMode` 자리)으로 코디가 직접 확인
- [x] **WORK-009 done** `0b3f7b7` · **WORK-010 done** `329fda6` · **WORK-011 done** `f70a094` · **WORK-012 done** `0415290` · **WORK-013 done** `bfde960`(검수 FAIL 0 WARN 2 → 파일 이름 둘은 014 Phase 0 · 「현재 값」 둘은 야간 보고 §1). [~] **WORK-014 fe 완료 · 코디 검증 통과(tsc 0 · vitest 360) · reviewer 중**(§3 · 마지막 WP). 아침 결정 항목은 야간 보고 §1. **WORK-010~014 문서 완료**(architect · `docs-v1-meeting-wp-report.md` · 코디 직접 확인 — 새 결정 0 · 스키마 파일 소유 = 011 · 같은 파일 중복 14곳 순서 Depends 에 기록). 코드 발주는 하나씩 — 009 검증 → 010 → 011 → 012 → 013 → 014(014 는 계약상 독립이나 `AgendaLineTree` 때문에 머지는 013 뒤). 순서 WP1 → 2 · 3 → 4 → 5, WP6 은 병렬. 기존 `30-work/work-006/007/008` 은 옛 설계라 참고만 하고 새로 쓴다. 각 WP 의 계약 절·손댈 파일은 아래 표

  | WP | MF | 계약 | 코드(신규 / 수정 / 폐기) |
  |---|---|---|---|
  | 1 MCP + 토큰 | 2 3 4 51 55 68 69 | DEC-003 §2 · §8 · SPEC-007 §4 도구 7개 · system §codex | 신규 `app/mcp/`(별도 컨테이너) · compose 에 mcp · `agent.py build_codex_options` allow list + 헤더 · `auth_session kind='meeting'` 리비전 · 발급/폐기 |
  | 2 회의 시작 | 1 55 70 | SPEC-006 §4 `/start` · SPEC-007 §4 웜스타트 · BE §5-2 · §12 8-a | `meeting_service.start()` commit 제거 · `warm_start()` 컨텍스트 제거 · `load_warm_start_context` 폐기 · 실패 처리 없음 |
  | 3 회의 중 | 9 10 49 50 53 | SPEC-007 U-2 · U-3 · U-4 · §4 · FE §8 | `meeting_batch_service` 600→1000 · `_load_input` 컨텍스트 제거 · `_persist` DELETE+INSERT · front `PromptBar` 슬래시 5 · `LineRow` 시각 제거 · `mergeAiBatch` 교체 |
  | 4 회의 종료 | 37 52 54 56 57 58 59 | SPEC-008 U-1 · U-2 · §4 파이프라인 · Case Matrix · DEC-003 §4 §6 §7 §STT | Phase 0 리비전(`pending_change→payload` · `source_*_line_id` 삭제 · `term_corrections` · `batch_run.phase`) / 1 `soniox.py` async + 블록 묶기 / 2 `finalize_service` ①→② 한 번 · `meeting_notes.json` 한 벌 · **`meeting_merge_service` 폐기** / 3 FE 생성중·실패·카운트 다섯 |
  | 5 편집·정리 | 13 14 21 25 36 60~67 | SPEC-008 U-3 · U-6 ~ U-10 · §4 · SPEC-002 · DEC-001 §3 · FE §6 | `CreateTaskFromLineDrawer` · `LinkTaskDrawer` → **payload 드로어로 수정**(시각은 이미 있는 `TaskCreateDrawer` · `TaskDetailDrawer` 참고, 시안 없음) · `LineKindSelector` 폐기 · `ConfirmModal size` · `schemas/meeting.py` `LineUpdate.kind` 삭제 · payload 두 모양 · `delete_line` 당김 제거 · `work_type.description` 리비전 + 시드 |
  | 6 목록·상세 UI | 5 6 7 8 | SPEC-006 U-1 · U-4 · U-6 · U-8 · FE §6-3 | `AppShell Breadcrumb` 링크 + 「←」 · `MeetingPreviewPanel` CTA · `AgendaLineTree density` · 헤더 순서. **업무 화면은 안 고친다** |

- [!] **실물 확인 1건** — 헤더 없는 webm 을 `stt-async-v5` 가 받나(SYS-OQ-5). WP4 Phase 1 안에서 파일 하나 넣어 본다($0.10)
- [!] **OQ 10 · 11 · 12 는 SPEC 이 자리를 잡았다** — `context.terms` 비움 · 「미팅·회의」 시드 빈 값 · 유형 못 고르면 `null` → 사람이 고른다. WP 에 그대로 옮긴다. 새로 묻지 않는다
- [!] **지킬 것** — 시킨 것만 · 사용자가 답한 것만 적는다 · 워커 보고는 문서를 직접 열어 확인 · 결론 난 것을 다시 묻지 않는다 · 화면 이야기는 **화면 순서로 먼저** 말한다 · 시안은 시각 참조일 뿐 판정에 안 들어온다(기능 정본 = 기획 + 정책)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-03 | 문서 워커는 workspace=coordinator 로 코디 워크트리 탑승(유실 재발 방지) | 사용자 승인 · runbook |
| 2026-09-03 | 영역당 BASE + DEC → SPEC. 6영역 직렬. 문서는 발주하지 않고 논의로 닫아 코디가 쓴다 — 단 **재작성·정정 규모면 architect 발주**(09-06~07 실제) | 사용자 확정 |
| 2026-09-03 | 작업 단위 = 워크트리 1개 = slug 1개 | 사용자 교정 |
| 2026-09-03 | 정책 일괄 확정 — DEC-001~006. 상세는 각 문서 | 사용자 논의 |
| 2026-09-03 | 스택 — Next.js 정적 빌드 · shadcn · 유동 반응형 · Bearer + 키체인 · Soniox 백엔드 중계 · open-kknaks/codex | 사용자 확정 |
| 2026-09-03 | 설계한 실패만 처리, 그 밖은 전파 | 사용자 확정 · DEC-003 §7 |
| 2026-09-05 | ~~웹 우선, Tauri 는 마지막~~ → **처음부터 Tauri 앱 창에서 개발** | 사용자 번복 (§C-4) |
| 2026-09-06 | **정본 축을 나눈다** — 기능 = 기획 + 정책 / 시각 = 디자인 시스템 + 시안. 판정은 기획·정책만. 시안에 있고 기획에 없으면 안 만들고 목록에 올린다. 기획에 있고 시안에 없으면 만든다 | 사용자 교정 |
| 2026-09-06 | 코드 워커 브리프는 「이 파일의 시각만 고쳐라」 — 「처음부터 그려라」 금지 | 사용자 교정 |
| 2026-09-07 | **회의록 흐름 결정 MF-1 ~ MF-66** — 정본 `reference/2026-09-06-task-management-app/Meeting flow.md` §0. 계약과 부딪히면 그쪽이 이긴다 | 사용자 확정(실물 확인 뒤 단계별) |
| 2026-09-07 | `decisions-pending.md` · `walkthrough-fixes.md` 는 **근거로 쓰지 않는다** — 「사용자 확정」 표시에 사용자가 안 한 말이 섞여 있었다 | 사용자 교정 |
| 2026-09-07 | ~~MF-13 · 14 · 65 「업무 탭 드로어 재사용 + 슬롯」~~ → **MF-67 payload 드로어는 회의록 것.** 필드는 payload 키, 시각은 이미 있는 업무 드로어 참고. 업무 드로어 코드는 안 건드린다 | 사용자 뒤집음(저녁) — 성격이 다르다 |
| 2026-09-07 | ~~MF-64 「칩 넷이 같다 · 줄 먼저」~~ → **정정** — 논의·결정 = 줄 추가 드로어 / 액션·업무 = payload 드로어 → 「저장」에 줄 + payload 한 요청 | 사용자(저녁) |
| 2026-09-07 | **MF-69 보강** — 회의 토큰은 **회의당 하나 · 원문을 `auth_session.meeting_token` 컬럼에** 둔다(제출마다 발급은 오버헤드). 해시만 규칙은 refresh 행에만 | 사용자(저녁) |
| 2026-09-07 | **MF-68** MCP 별도 컨테이너 `app/mcp/` · compose 에 back · worker · mcp / **MF-69** 단명 토큰 = `auth_session` 행 / **MF-70** 웜스타트 실패 처리 없음 | 사용자(저녁) — OQ-8 · 9 · SYS-OQ-4 닫힘 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| (대기) backend 버그 3 ② | `term_fd9fc1ce-619d-4f87-b218-10dfaefaa275` | — | — | `docs-v1-stream-stall-brief.md` §4 | 조사 끝 — **코드 정상 · 마이크 입력 레벨 부족.** 회의 12 끝나면 로그 둘(30초 유입량 · 60초 무토큰 WARNING) 발주. (a) 레벨 막대 (b) 무토큰 안내는 사용자 결정(야간 보고 §1) |
| (메모) | — | — | — | — | 다음 백엔드 발주에 얹을 것: WORK-015 검수 WARN 2(옵션 테스트 docstring · `_run_once` `frozenset()` → 「안 본다」 표현) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.**

## 4. 산출물

- 결정 원본: `reference/2026-09-06-task-management-app/Meeting flow.md` · AI 프롬프트 초안 `ai-prompt-draft.md`
- 계약: `20-spec/spec-006/007/008` · `10-decision/decision-003` · `40-architecture/*` (정정 2차까지 반영)
- 정정 리포트: `docs-v1-meeting-reflow-report.md` · `reflow2-report.md` · `reflow3-report.md` · WP 리포트 `docs-v1-meeting-wp-report.md`
- WP: `30-work/work-009-mcp-token.md`(코디) · `work-010 ~ 014`(architect) · `30-work/README.md` 회의록 재작업 그룹
- 검수 리포트: `work00{1,2,3,4,5}-review-report.md` · `work006/007/008-review-report.md`
- 코드 커밋(`kknaksss/docs-v1`): `2a4d29a`~`aa98518` — WORK-001~008 + Tauri 마이크 권한 · **`0b3f7b7` WORK-009**(pytest 564 · mcp 40) · **`329fda6` WORK-010**(pytest 595)
- 검수: `work009-review-report.md` · `work009-review-fixes.md` · `work009-phase4-evidence.md` · `work010-review-report.md`
- 문서 커밋(`task-management-app`): `07ca683` 실물 확인 기록 · `ddcf003` 회의록 발주 기록 · `121bd09` 회의록 SPEC 3 · WP 3

## 5. 이력 (최신이 위)

- `2026-09-07` 밤 — 정정 3차 반영 확인 · WORK-009 코디 작성 + backend 발주 · WORK-010~014 architect 작성 완료. 회의 토큰 = 회의당 하나 · 원문 컬럼(MF-69 보강). 워커 질문 3건 답(`/auth/session` · work-types 통과 · `/current/tasks` 신설)
- `2026-09-07` 저녁 — 33건 전수 대조 완료(전부 계약에 있음). 사용자와 MF-64 정정 · MF-67~70 닫음. Meeting flow.md 갱신, 정정 3차 브리프 작성. 코디가 「업무 드로어 재사용」·「드로어 두 번」을 화면 순서 없이 설명해 사용자가 여러 번 되물었다
- `2026-09-07` 계약 정정 2차(MF-64 · 65 · payload ≠ 업무 생성 · README L74) 반영 — `reflow2-report`
- `2026-09-07` 계약 재작성 1차(MF-1~63, 31건) 반영 — `reflow-report`. 사용자 검수에서 4건 잡힘
- `2026-09-07` 실물 확인 — 회의 1건 전 구간 통과(생성 → STT → 배치 7회 → 종료 → 통합본). 그 자리에서 흐름 결정 33건을 단계별로 닫음. Tauri 마이크 권한 커밋 `aa98518`. `.env` 에 `CODEX_TOOLS_DIR` · `CODEX_AUTH_JSON`
- `2026-09-07` 회의록 코드 완료 — WORK-006 · 007 · 008 + 검수 3회. 이후 결정으로 전부 옛 설계가 됨
- `2026-09-06` SPEC-006 · 007 · 008 1차 폐기 · 재작성(시안을 계약으로 옮긴 사고). 화면 7개 폐기 · 복구(`32f8357` · `faba893`)
- `2026-09-06` WORK-001 ~ 005 완료 · 검수 · 수정
- `2026-09-05` SPEC-000 ~ 011 초안 · 아키텍처 9문서 · Tauri 우선 번복
- `2026-09-03` BASE/DEC-001 ~ 006 · 계획 합의 · designer 리포트
