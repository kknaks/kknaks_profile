# [reviewer] WORK-011 검수 — 배치 입력은 발화뿐 · 스키마 한 벌 · AI 트랙 전량 교체 · 슬래시 5 · 줄 시각 제거

너는 **task-management `reviewer` 워커**다. **read-only** — 코드를 고치지 않고 테스트도 돌리지 않는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

## 0. 범위

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`, HEAD `329fda6` = WORK-010). **아직 커밋 전** — 범위는 미커밋 변경(백 + 프론트) + `ai_schemas/meeting_notes.json`(rename).

```bash
git status --short                      # tauri.conf.json 은 범위 밖
git diff HEAD --stat
git diff HEAD -- app/back app/front
```

**산출물** — `orchestration/work/docs-v1/work011-review-report.md` **1개**.

문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`(읽기 전용)

## 1. 네 층

```
정책       decision-003 §4(배치 입력 = 발화 하나 · 배치 갱신 = 전량 교체 · AI 트랙 안건 축) · §7(회의 중 배치 실패 · JSON 위반 폐기 · 없는 업무 참조 강등 · 회의 중 페이로드 버림) · §STT 배치 입출력 · 트리거
아키텍처    backend/README.md §5-2(배치 입력 발화만 · 출력 AI 트랙 전체 · 전량 교체 · 스키마 파일 하나 · 검증 두 층) · §7 · §8-1 · §8-3 · §12 테스트 6 · 7 · 7-a
           frontend/README.md §8(AI 증분 = 통째 교체 · 줄 시각 없음) · §3-3 · §11 · 금지 목록
           database/domains/meeting.md M-5-b · M-6 · M-7 · M-15 · M-16
SPEC       spec-007 U-2(줄 시각 없음 · 안건 시각 유지) · U-3(슬래시 5 · 좁혀지는 팝오버 · 그 밖은 텍스트 · 안건 이동은 팝오버만 · 안건 없음 규칙) · U-4(트리 통째 교체 · 미확인 점) · §4 「배치 입력」 · 「배치 출력」 · **「검증 순서 0~5」** · WS ai.batch 행 · AI 트랙 항목 형태 · §5 · §6 AC
WP         work-011-meeting-live.md Phase 1~4 · §Internal Interface(스키마 소유 · _parse_output · _demote · _persist · 트리거 · WS · mergeAiBatch · 슬래시 · 과도기 규칙)
결정 원본   Meeting flow.md §2-3 · §2-4 — MF-9 · 10 · 49 · 50 · 51 · 52 · 53
```

## ⛔ 2. 이번에 반드시 볼 축

### 2-1. 배치 입력에 컨텍스트가 0 인가 (MF-50)
```
① _BatchInput 필드 셋(meeting · seq · blocks)뿐 · _load_input 이 안건·줄·업무·유형·화이트리스트를 안 읽나
② build_batch_prompt 출력에 안건 제목 · 사람 줄 본문 · 업무 제목 · 화이트리스트 0(테스트가 단언하나)
③ 조회 순서 지시(list_agendas → get_agenda → 업무 가리킬 때만 list_tasks·get_task·list_work_types)와 「AI 트랙 전체를 다시 정리해라」가 프롬프트에 있나 · 초안 §B 의 「새로 드러난 것만」 이 남아 있으면 FAIL
```

### 2-2. 검증 순서 0~5 가 SPEC 표대로인가 · 전량 교체가 검증 뒤에만 (MF-53 · M-7 · M-16)
```
0 ai_session_id 없음 → 조용히 미제출 + 로그(RuntimeError 아님)
1 워커 오류·120초 → failed · 구간 다음으로
2 스키마 위반 → discarded · 행 0 · AI 트랙 직전 그대로 — 부분 파싱 0
3 업무 참조 사후 검사 — 검사 시점 조회(task_repository.list_meeting_context) · 그 줄만 action 강등 · payload 떼기 · 본문 유지
4 회의 중 payload · headline · termCorrections 버림(null)
5 _persist 한 함수 안에서 DELETE(줄→안건) + INSERT · 검증 전에 DELETE 가 도는 경로 0(정적) · seq 증가 → 커밋 후 push
미러 안건 source_agenda_id + 제목 복사 · 신설은 NULL
```

### 2-3. 스키마 한 벌 · WS 프레임 (MF-52 · SPEC-007 §4)
```
ai_schemas/meeting_notes.json 모양 = {headline, termCorrections, agendas[{humanAgendaId, title, lines[{kind, content, detail, evidence, taskId, payload}]}]} · 셋 nullable · aiAgendaId/newTitle/items 없음
meeting_batch.json 없음 · meeting_integration.json 은 아직 있음(012 가 폐기 — 정상)
ai.batch = {type, seq, agendas:[AgendaItem…]} 중첩 · 최상위 lines 없음 · 상세 응답 agendas.ai 와 같은 직렬화 함수
```

### 2-4. 과도기 규칙 — 012 범위를 침범했나 · 깨뜨렸나
```
run_final · _load_final_input · build_final_prompt · _agenda_rows · meeting_finalize_service · meeting_merge_service — 「컴파일만 되게 최소 수정」 인가. 의미를 바꿨으면 WARN. 지웠으면 FAIL
build_warm_start_prompt · launch_warm_start(WORK-010) diff 0
WORK-010 WARN 4 정리(reset_state _tasks · 죽은 import · 단언 · needle)가 됐나
```

### 2-5. 프론트 — 슬래시 · 팝오버 · 통째 교체 · 줄 시각 (MF-9 · 10 · 53)
```
① 슬래시 5개뿐 · 스페이스에서 칩 · 백스페이스 복귀 · 그 밖 /… 는 본문 · 안건 없음에서 /새안건 만 · 안건 이동은 팝오버만 · 팝오버 선택과 명령어가 같은 자리(applyPick)를 지나나
② 서버 요청 body 에 명령어 문자열 0(MSW 단언) · kind · content 만
③ mergeAiBatch = agendas.ai 통째 교체 · orphaned 0 · 재조회 갈래 0 · 펼친 줄 접힘 · 미확인 점
④ LineRow 에 시각 0 · AgendaHeader 안건 시각 유지 · 안내 바·프롬프트 바 시각 유지
⑤ 두 번째 트리 컴포넌트 0 · fetch 직접 0 · hex 0 · Sheet/Dialog 직접 0
⑥ WORK-013/014 범위(편집 · 드로어 · breadcrumb · 헤더) 침범 0
```

### 2-6. 테스트가 WP 검증 항목을 덮나
Phase 1~4 체크리스트 ↔ 테스트 대응표. **BE §12 6 · 7 · 7-a** 문장대로 있나. 트리거 999/1000 경계. 없는 항목을 표로.

## 3. 판정
- **PASS / WARN / FAIL**. 항목마다 **파일:줄 + 문서 절 번호**.
- **FAIL** = 배치 입력에 컨텍스트 · 검증 전 DELETE · 부분 파싱 · 스키마 모양 불일치 · 명령어 문자열이 서버로 · 두 번째 트리 · 012 범위 삭제.
- **WARN** = 과도기 의미 변경 · 테스트 공백 · 문구.
- **문서 공백** = 별도 절.

## 4. 하지 마라
- 코드 · 문서 수정 금지. 테스트 실행 금지(코디가 돌렸다 — back 611 · front tsc 0 · vitest 315).
- 앱 창 실측은 이 검수에서 요구하지 않는다(아침 항목).
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
  --subject "reviewer 완료: WORK-011 검수" \
  --body "FAIL n · WARN n · 문서 공백 n / 축별 판정 한 줄씩 / 리포트 경로"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] reviewer 완료 — WORK-011 검수 FAIL n · WARN n. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] reviewer: <질문>" --enter`
