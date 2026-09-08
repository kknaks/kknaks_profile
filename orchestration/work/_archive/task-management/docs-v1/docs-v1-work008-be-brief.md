# [backend] WORK-008 Phase 1·2 — 종료 파이프라인 · 통합 규칙 · 편집 표면

너는 **task-management `backend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`).
**코드 워커는 한 번에 하나만 돈다.** WORK-006·007 이 전부 들어와 있다.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-008-meeting-close.md            ← 네 빌드 계획. Phase 1·2 만
  20-spec/spec-008-meeting-close.md            ← 계약(§4)·Case Matrix·Acceptance(§6 25개)
  10-decision/decision-003-meeting-notes.md    ← 정책 §4·§5·§7
  00-baseline/baseline-003-meeting-notes.md    ← 기획 §Raw L39·L42·L43
  40-architecture/backend/README.md §6·§7·§8-2·§8-3 · database/domains/meeting.md M-19·M-20
```

## 1. 범위 — Phase 1 · 2

```
Phase 1  job 실행기 · 종료 파이프라인 · 통합 규칙 구조 검증 · 한 줄 요약
Phase 2  종료 후 편집 표면 (줄 인라인·종류 전환·삭제 · 안건 이름)
```

**Phase 3·4·6 은 프론트, Phase 5 는 별도 발주다. 건드리지 마라.**

## ⛔ 2. WORK-006·007 이 만든 것 — 다시 만들지 마라

```
build_detail()        meeting_service 의 함수 하나. **여기에 agendas.merged · headline ·
                      mergedSummary · finalBatchState · activeJobId 를 채운다.**
                      새 빌더·표면별 조립 금지 (정적 검사 테스트가 1개를 고정 중)
_assert_allowed       상태 표 한 곳. 여기에 행을 더한다
meeting_router        여기에 표면을 더한다
meeting_batch_service 최종 배치는 이 서비스의 run() 을 쓴다. 두 번째 배치 경로 금지
codex 옵션 빌더        한 함수(build_codex_options). 통합 제출도 여기를 지난다
integrations/agent    AgentClient 싱글턴. resume 으로 회의 세션을 이어 쓴다
task_service          **고치지 마라.** Phase 5 가 소비한다
```

## ⛔ 3. 정본 이름

```
agendas.{human, ai, merged}     latestBatchSeq     invalid_meeting_status
자식 쓰기 응답 = MeetingDetail 전체 · 삭제만 204 · 없는 자식 404
  단 POST …/lines 는 LineItem 을 준다(SPEC-007 §4 — 줄은 초 단위로 쌓인다. 코디 판정)
안건 next 배지                   종료 후 「다음 논의로」 (문구는 프론트 몫)
422 validation_error             field 를 싣는다 (WORK-007 이 규약을 세웠다)
```

## ⛔ 4. 정책이 못박은 것

### 종료 파이프라인 (DEC-003 §4 L101 · §7)

```
/end → job → ① 마지막 배치(AI 탭 전체 재정리) → ② 통합본 생성 + 같은 응답으로 headline
사전 조건        status='recording' 하나. **paused/stream 에서도 받는다**
                 — BE §8-2 의 409 는 오디오 요청뿐이다. 「WS 연결 있음」 조건을 두지 마라
마지막 배치 실패   AI 탭은 회의 중 증분 상태 그대로 유지(버리지 않음)
통합 실패        자동 재시도 2회 → 실패 시 ended + 실패 표시.
                 사람 원본·AI 탭·트랜스크립트·녹음이 다 남아 회의록이 비지 않는다
스피너 타임아웃    무한 대기 금지. 시간 초과도 실패
재생성           없다. 「다시 생성」은 실패 상태에서만
```

### 통합 규칙 — **모델을 믿지 마라. 구조로 검증한다** (DEC-003 §4 L102 · OQ-7 L180)

```
사람 줄 우선      같은 내용이면 **사람이 쓴 문장을 그대로 쓰고**
                 AI 줄에서는 **근거 타임스탬프만** 가져온다
                 AI 가 사람 문장을 다듬거나 바꾸지 않는다
AI 전용 내용      통합본에 **추가로** 붙인다
중복 판정        유사도 임계값이 아니라 **구조** — sourceHumanLineId 계승 +
                 **본문 글자 일치 검증** + **한 사람 줄의 이중 계승 금지**
```

**모델 출력은 참조 id 와 자리만 받는다. 본문은 서버가 복사한다.**
사람 줄 전수 · 이중 계승 · AI 중복 참조 · 참조 없음 · headline 누락/초과 — **실패 5종을 테스트로 고정해라**(WP Done Criteria).

### 한 줄 요약 (DEC-003 §1 표 · ERD M-19)

```
언제      통합 ② 와 **같은 응답**에서 받는다. 별도 호출·별도 엔드포인트 금지
저장      meeting.ai_headline
실패      NULL. 재생성 없음. 사람이 편집하지 않는다
```

### 줄 삭제 · 안건 이름 (DEC-003 §1 표 · §5 · ERD M-20 · M-5-d · M-5-e)

```
삭제 범위     merged 트랙만. human · ai · transcript · 녹음은 남는다
             source_human_line_id · source_ai_line_id 로 이어진 원본을 지우지 않는다
             — 근거 칩이 죽으면 안 된다
업무         줄을 지워도 task 는 지우지 않는다
하드/소프트   자식 행은 하드(DB §0-1). 통합 줄은 파생물이라 원본에서 다시 만들 수 있다
안건         이름만 고친다(PATCH …/agendas/{id} { title }, ended 에서 연다).
             **안건 삭제는 없다** — 줄이 갈 곳이 없다
             (예외: scheduled 의 사람 안건만 — WORK-006 이 이미 만들었다)
줄 순서      변경 없다
되돌리기      없다. 편집은 포커스 해제 자동 저장이고 이력 표가 없다
```

### DEC-003 §7 이 열거한 실패만 처리한다

**그 밖은 fallback 하지 말고 전파**(BASE-003 L43). `except Exception` 금지.
**WORK-007 검수에서 이게 두 번 걸렸다** — 백그라운드 태스크의 예외가 아무 데도 안 드러난 것, 무음 정정.
**백그라운드 job 의 예외도 로그로 드러내라.**

## 5. 지킬 것 — 아키텍처

```
계층·ORM 경계·schema/dto·PATCH Unset·Query(alias)   WORK-006·007 과 같다
트랜잭션      요청 하나가 경계. service·repository 에서 commit() 금지
             ⚠ `meeting_service.start()` 에 예외가 하나 있다(BE §2 vs §7 충돌 — 코디가 문서 정리 중).
               **그 자리를 따라 하지 마라.** 네 코드는 §2 를 지켜라
백그라운드 job  단계마다 세션을 새로 열고 그 단계 끝에 commit (BE §7)
외부 호출      codex 호출 중에 트랜잭션을 열어 두지 마라
LLM SDK       직접 import 금지
```

## ⛔ 6. 검증 — **앱 창 E2E 는 하지 마라**

```bash
cd app/back && uv run pytest -q <네가 만들거나 고친 테스트만>
```

**WP 의 「`curl` 로 …」 항목을 테스트 코드로 옮겨라.**
**통합 규칙 실패 5종 · 삭제 경계(원본·AI·트랜스크립트·녹음·업무 미변경) DB 전후 비교**는 반드시 테스트로.

**테스트로 못 덮은 것은 「실물 확인 필요」 목록으로 보고에 남겨라.** 통과 처리하면 리뷰에서 FAIL 이다.

## 7. 지킬 것 — 일반

1. **`app/back/` 밖을 건드리지 마라**
2. **프론트를 만들지 마라.** Phase 3·4·6 은 다른 워커다
3. **`task_service` 를 고치지 마라.** Phase 5 소관이다
4. **문서를 고치지 마라** · **커밋·push 하지 마라**
5. **WP 범위 밖을 하지 마라.** 발견하면 보고에 적어라
6. **기획·정책에 없는 기능을 만들지 마라.** 시안에 있어도
7. 막히면 물어라 — `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "..." --enter`

## 8. Done Criteria

- [ ] Phase 1·2 의 WP 검증 항목이 전부 통과
- [ ] **`build_detail()` 이 여전히 1개** — `merged`·`headline`·`mergedSummary`·`finalBatchState`·`activeJobId` 를 채웠다
- [ ] **`_assert_allowed` 가 여전히 한 곳**
- [ ] **통합 규칙 실패 5종이 테스트로 고정**됐다. 모델 본문을 읽는 코드 0건(grep)
- [ ] **삭제 경계** — 원본·AI·트랜스크립트·녹음·업무가 안 지워진다는 DB 전후 비교가 있다
- [ ] `headline` 은 통합 ② 와 같은 응답에서만 채워진다. 별도 호출 0
- [ ] `/end` 에 「WS 연결 있음」 조건이 없다
- [ ] `except Exception` 0 · 백그라운드 예외가 로그로 드러난다
- [ ] `app/back/` 밖 변경 0 · 커밋 없음

## 9. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_d77416df-9dc5-4ca7-90de-9b0cdf25533f \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "WORK-008 Phase 1·2 완료" \
  --body "만든 표면 / job 실행기와 종료 파이프라인 구조 / **통합 규칙 구조 검증 5종 테스트** / headline 이 채워지는 자리 / 삭제 경계 DB 전후 비교 / build_detail 에 더한 필드 / pytest 결과 / **실물 확인 필요 목록** / 범위 밖이라 안 한 것 / SPEC·WP 와 어긋나 판단한 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] WORK-008 Phase 1·2 완료. 상세는 인박스." --enter
```
