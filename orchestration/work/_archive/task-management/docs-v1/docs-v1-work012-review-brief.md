# [reviewer] WORK-012 검수 — async 재전사 → 최종 회의록 한 번 · 용어 보정 · payload 컬럼 · 종료 화면

너는 **task-management `reviewer` 워커**다. **read-only** — 코드를 고치지 않고 테스트도 돌리지 않는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

## 0. 범위

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`, HEAD `f70a094` = WORK-011). **아직 커밋 전** — 범위는 미커밋 변경 전부(백 + 프론트 + 리비전 0008 + `meeting_transcript_blocks.py` 신설).

```bash
git status --short                      # tauri.conf.json 은 범위 밖
git diff HEAD --stat
git diff HEAD -- app/back app/front
```

**워커 보고** — `orchestration/work/docs-v1/work012-be-report.md` · `work012-fe-report.md` · `work012-sys-oq5-evidence.md`(Soniox async 실물 2회차).
**산출물** — `orchestration/work/docs-v1/work012-review-report.md` **1개**.

문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`(읽기 전용)

## 1. 네 층

```
정책       decision-003 §4(최종 = 재전사 한 번 → 최종 회의록 한 번 · 통합 없음 MF-56) · §7(재전사 실패 fallback 없음 MF-58 · ② 3회 · 용어 보정 auto/guess) · §1 headline
아키텍처    backend/README.md §5-3(종료 파이프라인 ①→② · 외부 호출 중 트랜잭션 0 · 원자성) · §6 job · §7 · §8-3 · §12 테스트 8
           frontend/README.md §8 · §6-1 상단 바 · 금지 목록
           database/domains/meeting.md M-4 · M-7 · M-14(payload 자리 CHECK) · M-17 · M-19 · M-20 / account.md A-13(폐기 = 행 삭제 · 재시도 재발급 2026-09-08)
           system/README.md §③
SPEC       spec-008 U-1(생성중 두 단계 · 경과 · 새로고침) · U-2(실패 배너 · 「다시 시도」 · 사유 툴팁) · U-3 · U-4(한 줄 요약 · 카운트 다섯 = 화면에 그리는 것 MF-25) · U-5 · §4 API(/end · /finalize 202 · job progress.phase 파생 · errorCode 5종 · MergedSummary 다섯) · §「종료 파이프라인」 표 · ② 검증 표 · §5 · §6 AC · **§7 변경 이력 #3(finalBatchState · pendingChange · sourceHumanLineId 는 spec 에서 지워졌다)**
WP         work-012-meeting-close.md Phase 0~3 · §Internal Interface(리비전 0008 · SonioxAsync · build_blocks · _transcribe · run_pipeline · _attempt_final · _commit_success · 토큰 폐기 + **재시도 재발급**) · Open Issues
결정 원본   Meeting flow.md §2-5 · §3-1 — MF-25 · 37 · 52 · 55 · 56 · 57 · 58 · 69
```

## ⛔ 2. 이번에 반드시 볼 축

### 2-1. fallback 0 · 한 번 (MF-56 · 58)
```
① 실패 → ② 로 가는 코드 경로 0(정적 — _transcribe 실패 갈래에 _attempt_final 호출 0)
run_pipeline 스위치 0 — /end 도 /finalize 도 ①부터 · resume 갈래 0
② 는 정확히 최대 3회(재시도 2) · ① 은 0회 · 시도 타임아웃은 실패로 세고 다음
실시간 블록으로 최종을 만드는 경로 0 · 재전사 뒤 실시간 블록 0 · at_ms 기준 동일
```

### 2-2. 리비전 0008 · payload 자리 (M-14)
```
pending_change → payload RENAME(값 살아 옮겨짐) + 자리 CHECK(action/task 줄만) · 자리 밖 옛 값은 먼저 NULL
source_human/ai_line_id + FK2 + 부분 UNIQUE2 + CHECK 삭제 · term_corrections jsonb · batch_run.phase incremental|final · job.error_code 5종
JSONB none_as_null=True — 없으면 None 이 'null' 로 들어가 CHECK 가 멀쩡한 줄을 막는다(워커 실측). payload · term_corrections 둘 다인가
downgrade 가 대칭인가 · 왕복 테스트(0008 · 0007 두 칸)
```

### 2-3. 외부 호출 중 트랜잭션 0 · 원자성 (BE §7 · §5-3)
```
_transcribe: 읽기 → commit → Soniox(폴링) → 새 세션 DELETE+INSERT. 폴링 사이 세션 잡는 코드 0
_attempt_final: codex 대기 중 세션 0
_commit_success 한 트랜잭션 — merged INSERT + auto 치환 + batch_run(final) + ai_headline + term_corrections + ended/succeeded + job. 중간 예외 → 전부 없음(테스트)
AI 트랙 행 불변 · speaker_label 불변 · guess 본문 불변 · 표 밖 치환 0
```

### 2-4. 검증 함수 하나 · 스키마 한 벌 (MF-52 · WORK-011 검수 WARN 이관)
```
_parse_output(fill_final=True) 구현됐나 · NotImplementedError 0 · 두 번째 파서 0 · _persist(track='merged') 확장만
meeting_notes.json 하나 · termCorrections 항목 {stt, correct, grade}(SPEC-008 §4 대로 — 011 이 {from,to} 로 둔 것을 고쳤다: 회의 중 경로에 영향 0 인지)
최종 전용 검증 5(사람 안건 전부 정확히 한 번 · headline 1~200 한 문장 · termCorrections/grade · 페이로드 참조 키 null · payload.status done/cancelled 키 제거) · 업무 참조 강등은 011 함수(강등 시 payload 도 뗀다)
build_final_notes_prompt 에 「새로 드러난|추가할 줄」 0 · 재전사 스크립트 하나만 · 컨텍스트 0
find_ai_agenda_by_source 삭제 · meeting_merge_service · meeting_integration.json · run_final 계열 · _agenda_rows · BatchPhase.INTEGRATION 0
「같은 직렬화 함수」 정적 검사가 생겼나(011 WARN 4)
```

### 2-5. 토큰 (A-13 · MF-69)
```
② 종결(성공·실패 무관) revoke best-effort · 폐기 실패해도 job 불변
/finalize 재시도 — finalize() 가 /start 와 같은 issue_meeting_token · 발급 전 revoke 로 남은 행 제거 · 어느 시점에도 회의당 하나 · 두 번째 발급 코드 0 · 전용 테스트
```

### 2-6. 프론트 — 종료 화면 (SPEC-008 U-1 · 2 · 4)
```
① 생성중 두 단계 문구(job.progress.phase 파생 · attempt 「다시 시도 중 (n/2)」) · 경과 화면 계산 · 새로고침 시 activeJobId 폴링 · 폴링 실패는 실패로 꾸미지 않음
② 실패 배너 + 「다시 시도」= POST /finalize · 사유 툴팁 = job.errorCode 5종 · 화면 문구 「종결」·「다시 생성」 0
③ 카운트 다섯 = 화면에 그리는 것(MF-25) · headline = ai_headline · integratedAt 0 · pendingChange 0 · /integrate 0
④ finalizeMeeting 호출자 = api + 훅 둘 · 단계 문구·배너 소유자 = MeetingStatusBar 하나 · TranscriptPanel 종료 후 자동 따라가기 없음
⑤ fetch 직접 0 · hex 0 · Sheet/Dialog 직접 0 · 013/014 범위(편집 · 드로어 · breadcrumb · 헤더) 침범 0 — payload 이름 바꾸기만
```

### 2-7. spec 에서 지워진 것이 코드에 남았나 (SPEC-008 §7 #3)
```
finalBatchState — spec 은 09-07 에 지웠다. 백엔드 dto/schemas/repository 가 아직 내고 프론트 types.ts 에 타입만 남았다(워커 보고). 어디에 남았는지 파일:줄로 전부 세라 → 판정은 WARN(제거 대상 · 코디가 수정 발주)
errorCode 재진입 — 새로고침으로 들어오면 상세에 실패 job 의 errorCode 가 없어 배너에 사유가 안 뜬다(워커 보고). SPEC-008 U-2 표는 「job.errorCode」 · activeJobId 는 queued/running 만. **문서 공백으로 세라** — 결정을 만들지 마라
```

### 2-8. 테스트가 WP 검증 항목을 덮나
Phase 0~3 체크리스트 ↔ 테스트 대응표. **BE §12 8** 문장대로. Soniox 결과 비결정(블록 5~6 — 증거 파일)을 전제한 테스트가 없나. 없는 항목을 표로.

## 3. 판정
- **PASS / WARN / FAIL**. 항목마다 **파일:줄 + 문서 절 번호**.
- **FAIL** = fallback 경로 · 외부 호출 중 트랜잭션 · 원자성 깨짐 · 두 번째 파서/스키마 · 토큰 회의당 둘 · task.status 직접 대입 · 013/014 범위 침범.
- **WARN** = 남은 잔재(finalBatchState 등) · 테스트 공백 · 문구.
- **문서 공백** = 별도 절(errorCode 재진입 포함).

## 4. 하지 마라
- 코드 · 문서 수정 금지. 테스트 실행 금지(코디가 돌렸다 — back 626 · front tsc 0 · vitest 327).
- 앱 창 실측 · 300분 실물은 이 검수에서 요구하지 않는다(아침 항목).
- 새 결정을 만들지 마라.

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_be2a2f22-5ec1-4354-ab88-7ccb824100d3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: WORK-012 검수" \
  --body "FAIL n · WARN n · 문서 공백 n / 축별 판정 한 줄씩 / 리포트 경로"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] reviewer 완료 — WORK-012 검수 FAIL n · WARN n. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] reviewer: <질문>" --enter`
