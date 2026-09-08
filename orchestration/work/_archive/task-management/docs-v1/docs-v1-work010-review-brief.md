# [reviewer] WORK-010 검수 — `/start` 는 전이만 · 웜스타트는 컨텍스트 없이 백그라운드

너는 **task-management `reviewer` 워커**다. **read-only** — 코드를 고치지 않고 테스트도 돌리지 않는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

## 0. 범위

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`, HEAD `0b3f7b7` = WORK-009). **아직 커밋 전** — 범위는 미커밋 변경 + untracked.

```bash
git status --short                      # tauri.conf.json 은 범위 밖
git diff HEAD                           # meeting_service.py · meeting_batch_service.py · tests 2
cat app/back/tests/test_meeting_start_warm.py   # 신규
```

**산출물** — `orchestration/work/docs-v1/work010-review-report.md` **1개**.

문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`(읽기 전용)

## 1. 네 층

```
정책       decision-003 §4(회의 시작 — 전이만 · 즉시 응답 · 워커 죽어도 시작) · §7 웜스타트 행(처리 없음 — MF-70) · §8 「AI 도구 연결」 웜스타트가 주는 것(용어 다섯 · 도구 · 컨텍스트 없음)
아키텍처    backend/README.md §5-2(웜스타트는 /start 밖 · 커밋 뒤 백그라운드 · 새 세션에서 UPDATE · 본문 버림) · §5-3 · §7(/start 도 예외 아님 — commit 0) · §8-1 · §8-3 웜스타트 행 · database/domains/meeting.md M-1-a · M-12
SPEC       spec-006 §4 POST /start(200 MeetingDetail · 즉시) · 상태별 허용 표 · 구현 규칙 L647 / spec-007 §4 「웜스타트」 표 5행 · 「AI 도구 7개」 · §5 「웜스타트는 /start 밖」 · 검증 0 · §6 AC 「워커를 내린 채 회의 시작」
WP         work-010-meeting-start.md Phase 1 · 2 · §Internal Interface(트랜잭션 · launch_warm_start · 제출 파라미터 · session_id 저장 · 실패의 결과 · 프롬프트 여섯 절 · 프롬프트에 없는 것)
결정 원본   Meeting flow.md §1-2 · §1-4 · §1-5 — MF-1 · 50 · 55 · 70
```

## ⛔ 2. 이번에 반드시 볼 축

### 2-1. `/start` 트랜잭션 — 전이 + 토큰 INSERT 하나 · commit 0 (MF-1 · BE §7)
```
① meeting_service.py 에 session.commit( 0건인가 · 전이 UPDATE 와 토큰 INSERT 가 한 트랜잭션인가(WORK-009 의 INSERT 줄이 유지됐나)
② 웜스타트가 register_after_commit 로 걸리나 — 커밋 안 되면 안 도는가(테스트가 이를 단언하나)
③ 요청 처리 중 게이트웨이 호출 0 · 응답 뒤 1 (테스트)
④ 외부 호출(codex) 이 요청 안에서 0 — 실측 7ms 근거가 코드에서 성립하나
```

### 2-2. 백그라운드 태스크 · 실패 처리 없음 (MF-70 · BE §8-1)
```
① launch_warm_start 가 create_task 로 즉시 반환 · 예외를 밖으로 안 냄(done 콜백 로그만)
② retry · attempt · 재웜스타트 · warm_start_failed 상태·컬럼·에러코드 0건
③ except Exception 0 · 예외를 삼키는 자리가 done 콜백의 task.exception() 로그 하나뿐인가 — 그 밖에 잡아서 기본값으로 때우는 곳이 있나
④ session_id 저장이 새 세션(session scope)에서 · 제출 대기 중 트랜잭션 0(BE §7)
⑤ 토큰이 None 이면 미제출 + 로그(WORK-009 규칙)
⑥ wait_for_tasks 가 프로덕션 파일에 들어갔다(워커 보고 (2)) — 프로덕션 경로에서 호출 0 인가 · 테스트 전용임이 드러나나
```

### 2-3. 프롬프트 — 컨텍스트 0 · 여섯 절 (MF-50 · 55 · DEC-003 §8)
```
① 프롬프트에 humanAgendas · tasks(도구 이름 list_tasks 제외) · taskWhitelist · project · JSON 블록 0
② 여섯 절(역할 · 흐름 · 안건이 뼈대 + 용어 다섯 · 요약 원칙 · 도구 7 · 금지) 이 DEC-003 §8 문장과 맞나 — 특히 「액션과 업무를 가르는 선」 · 「업무는 실제로 있는 것만」 · 「줄을 만들기 전에 어느 안건인지」
③ 도구 7 이름이 WORK-009 _TOOL_NAMES 와 글자 그대로 · 그 밖의 도구 이름 0
④ 「통합본」 어휘 0(MF-56) · 「준비됨」 지시 있음
⑤ output_schema=None 으로 나가나
```

### 2-4. 범위 준수
```
build_batch_prompt · run_final · _load_final_input · build_final_prompt · _agenda_rows · meeting_finalize_service   diff 0 인가(WORK-011 · 012 몫)
프론트 · compose · env · 리비전 0
삭제한 테스트(500 전파)가 정말 뒤집힌 계약인지 — 아니면 회귀 보호를 잃은 것인지
```

### 2-5. 테스트가 WP 검증 항목을 덮나
WP Phase 1 · 2 검증 체크리스트 ↔ `test_meeting_start_warm.py`(32) 대응표. **BE §12 8-a** 가 정확히 그 문장대로 있나. 없는 항목을 표로.

## 3. 판정
- **PASS / WARN / FAIL**. 항목마다 **파일:줄 + 문서 절 번호**.
- **FAIL** = commit 호출 잔존 · 요청 안 외부 호출 · 실패 처리 갈래 존재 · 프롬프트에 컨텍스트 · 범위 침범(011/012 파일 변경).
- **WARN** = 테스트 공백 · 문구 · 테스트 전용 코드가 프로덕션 파일에.
- **문서 공백** = 별도 절.

## 4. 하지 마라
- 코드 · 문서 수정 금지. 테스트 실행 금지(코디가 돌렸다 — 595 passed).
- 앱 창 실측(SPEC-007 §6 AC)은 이 검수에서 요구하지 않는다 — 코디가 아침 항목으로 넘긴다.
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
  --subject "reviewer 완료: WORK-010 검수" \
  --body "FAIL n · WARN n · 문서 공백 n / 축별 판정 한 줄씩 / 리포트 경로"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] reviewer 완료 — WORK-010 검수 FAIL n · WARN n. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] reviewer: <질문>" --enter`
