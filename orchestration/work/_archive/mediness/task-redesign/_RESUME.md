
# 재개 노트 — task-redesign (mediness)

**지금**: **upstream 동기 완료(2차)** — #137/#665 가 0135·WP-125 선점 → 재번호: migration `0136_task_status_5v`(down=0135_meeting_reservation_uq, 단일 head)·**WP-126(task-ledger)/WP-127(incident)**·DOC-246/247. 코드 90파일·스펙 18파일 치환(upstream 줄 원문 보존), orphan 테스트 backfill 계약으로 갱신(8/8). ⚠ 로컬 DB alembic_version 이 구 id(`0135_task_status_5v`)면 `0136_task_status_5v` 로 UPDATE 필요.
**이전 상태**: 작업 전체 완결 — 사용자 리뷰만 남음. 어댑터까지 착지: 스펙(IB-1~9, #661 커밋 001a214ce·82909d316) + 코드(#136 커밋 fe41eaa1 — 검수 FAIL 1건 R2 정정, 214 passed). 코디handle = `term_9fcc736a-df22-4409-adb4-f46292d5bc72`(재부팅 후).
**다음**: 사용자 #661 → #136 리뷰·머지 → SUMMARY 작성 → archive-work. 배포 사전조건: Slack 토큰·scope 4종 + 봇 #900 초대·`message.channels` 구독·env 2개 + 좌초 responding run 소급 처분.

세팅: `scripts/new-work.sh mediness task-redesign` · 설정 SSOT `config/projects/mediness.json`
코디handle: `term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed`

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec` (branch `task-redesign-spec`, base `origin/mediness` → PR `mediness`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] BE/FE 코드 작업 진행 중 (WP-125) + planner WP2(incident WP) 작성 병행 — 사용자 승인된 파이프라인
- [ ] spec PR #661 (base `mediness`) 머지 대기 — **⚠ base 의 #659 가 WP-124 선점 → 우리 WP 는 125/DOC-245 로 재번호**(rebase 충돌 해소 + 코디 재번호, lint 0 error)
- [ ] **사용자: spec PR #661 · code PR #136 리뷰·머지** (code 는 spec 머지 후 권장)
- [x] #661·#136 **squash 머지 완료**(2026-08-31, 사용자 지시로 코디 실행)
- [ ] **main 릴리스 PR 리뷰·머지(사용자)**: spec [mediness#667](https://github.com/MediSolveAIDev/mediness/pull/667) · code [mediness-app#138](https://github.com/MediSolveAIDev/mediness-app/pull/138) — 배포 주의 4건 본문 기재
- [ ] 머지·배포 후: SUMMARY 작성 → archive-work = 완료선 (⚠ squash 머지됐으므로 archive 전 rebase 금지 — 런북 blob 대조 절차)
- [!] 배포 사전조건: prod `slack_decision_bot_token` + scope 4종 확인(미확인 시 declare 전건 503, retry 표면은 콘솔 미발주라 없음 — OQ-17) · 좌초 responding run 소급 처분 별도 결정
- [!] BE 미결 환류 완료: U-2 문안·resolver 실효 3단 → spec 커밋 7554a1b2f. 배포 전 확인: 좌초 responding run 처분·prod Slack 토큰/scope(OI-8: decision 키 공용 그대로)
- [!] 관측: spec-060 인벤토리 기준수(57) vs 실측(61) 4건 차이 — 타 작업 등재 누락, 이번 범위 밖
- [ ] code PR 머지 후: **WP-126 코드 발주**(BE/FE) → 검수 → PR — 여기까지가 이 작업의 완료선
- [ ] 요청 테스크 = **별도 신규 작업** (new-work 새 slug). 확정 결정 §2 를 그대로 입력으로 사용
- [!] BE P0 실측 게이트: `accepted_at` 스탬프가 `task_accepted` 이벤트와 대응 안 되는 행이 있으면 BE 가 질문해 옴 — drop 진행 여부 판단 필요
- [!] BE 완료 시 검증 항목(FE 미결 이월): ① `canReassignTask` 를 담당자 본인에게 열었는지(거절 대체 동선) ② `blocked→done` 이 allowed_transitions 에서 빠졌는지
- [!] 스펙 정정 대상(다음 spec 커밋에 배치): SPEC-154 §4.19 의 2026-08-14(WP-114) 개정 노트가 «5열·accept_pending·거절» 을 유지 — 08-31 개정과 모순 (FE 보고 ⑶)
- [!] 코디 최종 검증 시 front 는 `npm ci` 선행 필요(워크트리에 node_modules 없음 — FE 는 심링크로 검증 후 제거)
- [!] 코디 직접 정정 3건(검수 후 원라이너, lint 0 error 재확인) + WP-125 재번호는 스펙 커밋에 포함됨
- [!] work-114(in_dev)가 여전히 수락 대기 세계를 계약 — WP-124 착수 전 소유 조정(OI-1)에서 함께 정리 (planner R2 보고)
- [!] 사용자 재확인 대기 항목(planner 보고): **OI-6 `accepted_at` drop 은 이력 복구 불가** — P0 실측 후 확인 / OI-1 WP-114(in_dev)와 FE 파일 충돌 — 착수 전 소유 조정 / OI-5 `task_unblocked` 이벤트 신설(결정 SoT 밖 기계적 파생)
- [!] 파이프라인 합의: WP1 코드 발주 후 병행으로 WP2(incident) 작성 발주 (작업 시간 최소화)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-08-31 | **`accept_pending` 상태 제거.** `runtime_task_status`·`version_wbs_task_status` 동시 cutover(0108 선례), 기존 행은 `todo` 매핑. 생성 초기값 `todo` | 사용자 지시. 근거: 이미 반쯤 무력화(incident round0 우회·WBS 표면 400·phase 도달 불가) — research §B S6 |
| 2026-08-31 | **수락·거절 개념 완전 폐기.** decline 엔드포인트 3곳·`task_declined`/`accepted` 이벤트·`accepted_at` 스탬프·MCP `task_decline` 제거. "배정 거부"는 재배정 요청으로 흡수 | 사용자 지시 (AskUserQuestion) |
| 2026-08-31 | **재배정 = `todo` 리셋 + `started_at` 클리어.** terminal(done/canceled) 재배정 금지 가드(BUG-023)는 유지. 담당자 본인도 재배정 요청 가능해야 함(거절의 대체 통로) | 사용자 지시 (AskUserQuestion) |
| 2026-08-31 | **착수 = 명시 시작만.** WBS 스케줄러의 `todo→in_progress` 자동 전환 폐기 → "시작일 도래 알림"으로 강등. overdue DM 유지 | 사용자 지시 (AskUserQuestion) |
| 2026-08-31 | **시스템 생성 태스크도 예외 없음 — 전부 `todo` 생성.** decision bootstrap(`task_service.py:155`)·incident 추적 카드(`definitions.py:141`)의 즉시 in_progress 폐기. 라운드 종결 판정·추적 UX 파급은 스펙에 명시 | 사용자 지시 (AskUserQuestion) |
| 2026-08-31 | **incident 정본 흐름 확정.** 슬랙 이슈 채널 이벤트(웹훅/수집 — **어댑터 연결은 후속**, 진입 계약만 open) → AI 수집 → **제품 대표(is_lead)** 승인 게이트 → 승인 시 슬랙 채널 생성 + 추적 테스크(todo 생성 → 시스템 시작 전이로 자동 에스컬레이션, **cc = 해당 버전 참여자들**) → 슬랙 [완료] → AI 회고 + 후속 후보 → 승인 → 담당자 테스크 todo 생성 → 전부 완료 → AI 피드백 + 후보 → **승인 게이트 유지** → 테스크 생성 → 루프 → 종료 | 사용자 제시 흐름 + AskUserQuestion |
| 2026-08-31 | **대응 완료 = 슬랙 버튼만 + 슬랙 미연결 시 fail-loud.** 웹 완료 버튼 안 만듦. 토큰 미설정 조용한 no-op 폐기 — declare 승인 실행을 실패시켜 responding 영구 정지 방지 | 사용자 지시 (AskUserQuestion) |
| 2026-08-31 | **요청 테스크(타인에게 요청) 도입 — 게이트 없음 모델.** 요청 = `todo` 로 상대 배정 + 요청자 자동 cc + "내가 요청한 일" 뷰. 수락·검수 게이트 없음(5값 모델 정합), 싫으면 재배정 요청 | 사용자 제기 + AskUserQuestion |
| 2026-08-31 | ~~요청 테스크는 별도 후속 라운드~~ → ~~task-redesign 한 작업 단위 안에서 진행~~ → **재정정: 완전 별도 신규 작업으로 분리.** 기존 작업(WP-125·WP-126)을 먼저 확실히 마무리. 요청 테스크 설계 결정(게이트 없음·파생 구분·member 축·DM·진입점 2곳·페이지 리디자인)은 전부 확정 상태로 신규 작업에 이월 — **code PR 홀드 해제** | 사용자 재정정 (2026-08-31) |
| 2026-08-31 | **요청 전달 = 슬랙 DM + 웹 목록.** 요청 생성 시 수신자에게 DM(요청자·제목·딥링크 1개) — decision notify 인프라(slack_id SoT·규율 3종) 재사용, DM 실패해도 태스크는 생성(graceful) | 사용자 확정 (AskUserQuestion) |
| 2026-08-31 | **요청 진입점 = 내 업무 생성 모달 + landing_chat(AX 채팅) 둘 다.** UI 수정 동반 | 사용자 확정 |
| 2026-08-31 | **워크플로 태스크의 웹 재배정 요청 축 = 요청 테스크 신규 작업으로 이월(코디 판단).** reviewer_code W1 — 웹 [⋯] 재배정 요청은 canonical(비워크플로)만. decision·incident 담당자는 채팅·MCP `ax_task.reassign` 통로 존재(전 계열, 본인 담당). 별도 요청 축 설계는 신규 작업 소관. PR 리뷰 포커스로 노출 — 사용자 뒤집기 가능 | 코디 판단 (2026-08-31) |
| 2026-08-31 | **슬랙 에러 채널 어댑터 소재·결정 확보 (후속 작업 입력).** #900-prod 전건 자동 raise(게이트가 사람 필터 — 사전 필터 없음)·stg 제외·Events API 구독·`source=slack_error_channel`. 형식 실측 2종 → `research-slack-error-adapter.md` | 사용자 샘플 제공 + 확정 |
| 2026-08-31 | **추적 Task cc = declare 의 AI 초대 후보 유지(현행 보존).** 「버전 참여자 전원」은 버전 단위 참여자 축이 시스템에 부재해 실현 불가(BE 실측) — 그 축이 생기면 OQ-13 재정의. spec-152·WP-126 정정 완료 | 사용자 확정 (BE decision_gate) |
| 2026-08-31 | **accepted_at 고아 60건 = 이벤트 소급 backfill 후 drop (OI-6 최종).** 로컬 실측으로 전부 레거시 decision 이관분 확인. 0135 에 backfill 추가, 가드는 재발 방지로 존치. 로컬 검증 완료(backfill 60·enum 5값) | 사용자 확정 (로컬 RAISE 실증) |
| 2026-08-31 | **run 종결 감사 = payload 요구 폐기.** `workflow_run_events` 기존 원장 그대로(payload 의도적 부재·cause 닫힌 어휘 존중, migration 0). 정리된 추적 Task 목록은 각 Task 의 `task_canceled` 이벤트 + execution 사슬 역조회로 충분. spec-152 해당 문장 정정 | 사용자 확정 (WP-126 검수 W1) |
| 2026-08-31 | **decision 쪽 기존 요청/배정 태스크 축 = 레거시, 주석처리만.** 코드 삭제·강한 은퇴가 아니라 비활성(주석처리) 수준으로 남기고, **새 업무 요청 모델이 대체**한다 | 사용자 지시 |
| 2026-08-31 | **채팅(landing_chat) 태스크 생성 = 새 업무 요청으로 확장.** 현재 본인 태스크만 생성 가능 → 타인 지정 요청 가능하게(assignee 지정 + 자동 cc + DM). 진입점 2곳(모달·채팅) 결정과 동일 축 | 사용자 지시 |
| 2026-08-31 | assignee 이중 축·FK 부재는 **문제 아님으로 닫음** — 커널 분리 수명 보장(선언된 경계, erd.md:53). 요청 테스크는 `assignee_member_id` 정본 축 사용 | 사용자 확인 |
| 2026-08-31 | **요청 구분 축 = 파생.** 새 컬럼·새 type 없음(migration 0) — manual·ai 계열 task_type + `created_by ≠ assignee` 면 요청. 워크플로 fanout 오염 없음. 백엔드 잔여 = 요청자 관점 쿼리(created_by 목록+인덱스)·자동 cc 호출·DM 훅 | 사용자 확정 (AskUserQuestion) |
| 2026-08-31 | **태스크 페이지는 디자인을 다시 한다.** "내 할 일 / 내가 요청한 일" 구조·요청 구분 축(파생 vs task_type)은 **페이지 리디자인과 함께 스펙 단계에서 확정** — 디자인은 사용자 주도 | 사용자 확정 |
| 2026-08-31 | **회의록 어휘 canonical 통일.** `meeting_v2_minutes_task` 의 open/in_progress/done → canonical 어휘, default "open" 제거. 박제 성격은 유지. WP1 범위 | 사용자 지시 (AskUserQuestion) |
| 2026-08-31 | **문서 층위 복구 포함.** runtime_task 도메인 문서 신설 + ERD 재작성 + spec-110/125 stale 정정을 이번 스펙 단계에 포함 | 사용자 지시 (AskUserQuestion) |
| 2026-08-31 | **알림/DM 은 후속 고도화로 제외.** 게이트 방치 에스컬레이션·결재 DM 은 이번 범위 밖 (OQ 로 명시하고 넘김) | 사용자 지시 |
| 2026-08-31 | **WP 구성 = WP1 task 수정 → WP2 incident 수정 (직렬, WP1 선행).** incident 의 C1~C15 충돌 수정이 WP1 enum·전이표 변경에 의존 | 사용자 지시 |
| 2026-08-31 | **범위 = 전체 재정비.** ① task 원장 전면 통합 — DecisionExecutionTask 를 canonical 로 이관·폐기, WBS `status` 컬럼 제거(work_item 은 origin 참조, phase 는 자체 status 유지) ② **incident 워크플로 재정비 포함** — spec-152 낡음(개정 6회 누적·되돌림·죽은 경로) | 사용자 지시 ("incident도 너무 낡아서 이번 기회에 전체 재정비") |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner | `term_27a7ad02-3919-43d0-b806-95e8c8eb18cc` | `task_0414df258740` | `ctx_0d59c8744a7f` | `task-redesign-spec-brief.md` | **완료** — 스펙 6건 개정·도메인 2건 신설·ERD 재작성·WP-124 신설. 코디 실물 검증 통과(lint 0 error) |
| reviewer_spec | `term_8412cd16-b0f5-4f5d-a841-da64055e98ba` | `task_83727ae576ae` | `ctx_7cfa56381423` | `task-redesign-review-spec-brief.md` | **완료 — FAIL 6건** (`review-spec-report.md`). 재검수 대기 |
| planner (R2) | `term_8097d7f4-fc31-44ff-90f0-6ac0f0ce72d5` | `task_f3e9331a5b61` | `ctx_97d46faf4cd7` | `task-redesign-spec-fix-brief.md` | **완료** — 22파일 +790/-601, 폐기 활성 잔존 0, lint 0 error. 코디 실물 검증 통과 (`fix-r2-report.md`) |
| reviewer_spec (R2) | `term_8412cd16-b0f5-4f5d-a841-da64055e98ba` | `task_f6e5c6433db5` | `ctx_02c34227fbb5` | `task-redesign-review-spec-r2-brief.md` | **완료 — WARN(진행 가능), 차단 0.** 잔여 수치 오기 3건은 코디가 직접 정정(아래) |
| backend | `term_75b70534-ae89-4f02-ae26-f3c5bf6531db` | `task_446653b50a31` | `ctx_67590378c64e` | `task-redesign-be-brief.md` | **완료** — 81파일(신규: 0135 migration·round_eval.py·test_0135). back 684+mcp 523 passed, 코디 독립 51 passed. OI-6 → migration RAISE 가드 대체(**배포 시 orphan 행 있으면 멈춤 — 배포 담당 인지 필요**) |
| reviewer_code | `term_96c72726-814b-440e-9e29-2da11115ee1d` | `task_63bc073bdb55` | `ctx_aa3ce111d603` | `task-redesign-review-code-brief.md` | **완료 — WARN(진행 가능)·FAIL 0.** W1 이월(코디 판단)·W3/W5 코디 정정·W6 WP-126 이월·code PR #136 |
| frontend | `term_3d56bec5-4301-42ae-9832-d7a07096ac9e` | `task_1b657e66d552` | `ctx_04df4b33d627` | `task-redesign-fe-brief.md` | **완료** — 36파일: 라벨 사전 1벌·칸반 4열·수락/거절 표면 제거·decline BFF 3건 삭제. tsc 0·prettier 통과·vitest 신규 실패 0(기존 8건 baseline 동일 확인). 코디 diff·grep 검증 통과 |
| planner (WP2) | `term_b1761f6d-c81c-4fc1-9d78-f6c23d006422` | `task_042bc89efa63` | `ctx_f49349216567` | `task-redesign-wp2-brief.md` | **완료** — WP-126 신설(7 phase·migration 0·depends WP-125). is_required 계약 오기 실측 발견 → 코디가 WP-125·spec-152 3곳 정정(0066 근거) |
| reviewer_spec (WP-126) | `term_8b0f1b27-4a48-476e-8390-709dbfaf7940` | `task_93c6e76f73e3` | `ctx_15ac48a58339` | `task-redesign-review-wp126-brief.md` | **완료 — WARN(FAIL 0).** W1 run 감사 전제 오류(payload 폐기로 사용자 확정)·W2 죽은코드 재실측·W3 log 행(코디 처리)·W4 좌표 드리프트 |
| planner (WP-126 R2) | `term_dfdb5c31-8161-477f-ab8b-ef30878d94ed` | `task_a5164b61b1c1` | `ctx_9bdd45aae2d3` | `task-redesign-wp2-fix-brief.md` | **완료** — WARN 4건 해소, 코디 검증 후 커밋 `21e409d51` 로 PR #661 갱신 |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/661 — **MERGED**(squash) → main 릴리스 https://github.com/MediSolveAIDev/mediness/pull/667
- code PR: https://github.com/MediSolveAIDev/mediness-app/pull/136 — **MERGED**(squash) → main 릴리스 https://github.com/MediSolveAIDev/mediness-app/pull/138
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-08-31` #661·#136 squash 머지(사용자 지시) → main 릴리스 PR 생성: spec #667(mediness→main)·code #138(dev→main). app 릴리스는 원래 PR 방식(config 의 FF 노트가 낡음 — main 단독 5커밋 전부 과거 release 머지)
- `2026-08-31` upstream 2차 동기: #137/#665 선점 → 0136 재번호·WP-126/127 재번호(코드 90·스펙 18파일, upstream 줄 보존)
- `2026-08-31` 슬랙 에러 어댑터 사이클 완주(사용자 샘플 → 스펙 IB-1~9 → BE 구현 → 검수 FAIL(파서 예외 누출) → R2 정정 → 커밋 fe41eaa1). OQ-10·OQ-15 해소 — incident 트리거 완결
- `2026-08-31` WP-126 코드 사이클 완주: BE 26파일(판정 1벌·실버그 1건 수정·run 감사·fail-loud)·FE 3건·0135 backfill → 검수 WARN(FAIL 0·위반 0) → 커밋 80f50098 → **#136 통합 PR 갱신**. 스펙 환류 3건+OQ-17(커밋 7554a1b2f·a6b12d955)
- `2026-08-31` 로컬 검증: 스냅샷 워크트리 기동(back 200·mcp tools 60·front 23001), DB 고아 리비전 복구, 0135 RAISE 실증→backfill 확정, 사용자 UI 확인 완료
- `2026-08-31` WP-125 코드 사이클 완주: BE 완료(684+523)·코디 독립 51·reviewer_code WARN(FAIL 0)·W 정정(주석 3·수치)·**code PR #136**. W1 은 업무요청 신규 작업 이월
- `2026-08-31` WP-126 사이클 완주(작성→검수 WARN→R2 정정→커밋 21e409d51, PR #661 갱신). run 감사 payload 폐기·is_required 실측 정정 포함. FE(WP-125 P5) 완료·검증 통과
- `2026-08-31` 코드 단계 개시: 스펙 커밋·rebase(#659 와 WP-124 충돌 → 125 재번호)·spec PR #661 → app 워크트리 세팅 → BE/FE 발주 + WP2 planner 병행 발주
- `2026-08-31` 검수 사이클 완주: R1 FAIL(주변 SPEC 잔존 6건) → planner R2 정정(22파일) → 재검수 WARN(진행 가능) → 코디 원라이너 3건 정정. 스펙 단계 산출 완료, 사용자 리뷰 대기
- `2026-08-31` planner 발주 (task_0414df258740 / ctx_0d59c8744a7f / term_27a7ad02…) — 스펙 반영 + WP1 작성. 사용자 지시로 WP1 코드 중 WP2 작성 병행 파이프라인 합의
- `2026-08-31` incident 사전 조사 완료 → `research-incident.md` (슬랙 미연결 시 run 전멸·라운드 판정 3벌·죽은 계약 27건 확인)
- `2026-08-31` 사전 조사 완료 → `research-task-status.md` 작성 (task 원장 3벌 확인, spec-125/110/ERD stale 확인)
- `2026-08-31` new-work.sh 세팅(planner·reviewer_spec, spec 워크트리) + 사전 조사 에이전트 2기 가동

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
