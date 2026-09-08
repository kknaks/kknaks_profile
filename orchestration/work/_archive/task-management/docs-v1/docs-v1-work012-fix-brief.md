# [backend] WORK-012 검수 수정 — `except Exception` 좁히기 + 정적 가드 복원 · `finalBatchState` 백엔드 잔재 제거

너는 **task-management `backend` 워커**다. WORK-012 Phase 0~2 를 네가 구현했고 reviewer 검수가 끝났다(FAIL 0 · WARN 4). 그중 코드로 닫을 둘을 이 발주에서 닫는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

## 0. 어디서

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`). 미커밋 상태 그대로 위에서 고친다.
**검수 리포트** — `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/work012-review-report.md` §3 **W-1 · W-3** (읽기 전용).

## 1. 고칠 것 둘

### W-1. `except Exception` 하나 + 삭제된 정적 가드
```
meeting_finalize_service.py:544 근처  revoke_meeting_token best-effort 의 except Exception → 구체 타입으로 좁힌다(sqlalchemy.exc.SQLAlchemyError — DELETE 한 줄이 낼 수 있는 것은 그것뿐이다). BE §8-1 「except Exception 을 쓰지 않는다」. best-effort 의 뜻(MF-4 — 폐기 실패해도 job 불변)은 그대로
test_meeting_finalize.py            네가 지운 test_static_end_has_no_stream_condition_and_no_broad_except 를 되살린다 — 이름은 자유. 잠그는 것 둘:
  ① except Exception · except BaseException 0 in meeting_finalize_service · meeting_edit_service · job_service · meeting_batch_service + job_repository · meeting_line_repository (meeting_merge_service 는 폐기됐으니 목록에서 뺀다)
  ② is_active( · meeting_stream_disconnected 가 meeting_finalize_service 에 0(「WS 연결 있음」을 조건으로 보지 않는다 — SPEC-008 §4)
  (③ ai_headline 단일 writer 는 이미 test_only_the_finalize_service_writes_the_headline_and_terms 가 대체했다 — 그대로)
```

### W-3. `finalBatchState` 백엔드 잔재 — SPEC-008 §7 #3 이 09-07 에 지웠다
```
dto/meeting.py:174 · :185                       final_batch_state 필드 + docstring 언급 삭제
schemas/meeting.py:465 · :484 (+1)               finalBatchState 필드 + docstring 삭제
service/meeting_service.py:189 · :214 · :222 · :223   _final_batch_state() 조회 함수 + 호출 삭제(build_tracks 등 남는 것은 그대로)
service/meeting_batch_service.py:420            주석 — 「종결 정리 실패」·finalBatchState 어휘 삭제(「종결」은 MF-56 으로 사라진 말)
repository/meeting_batch_run_repository.py:54   docstring — finalBatchState · integratedAt · phase='integration' 언급 삭제. latest_by_phase 함수 자체는 phase='final' 용도로 남는다면 남긴다
tests 1곳                                        finalBatchState 단언 삭제
```
프론트 4곳(types.ts · testUtils.tsx · closeFixtures.ts 2)은 **frontend 워커가 뒤이어** 지운다 — `app/front/` 금지.

## 2. 하지 마라
- W-2(progress.phase 파생 규칙 — 성공 경로에서 ② 문구가 안 뜸)는 **문서 결정**이라 이 발주에서 손대지 않는다.
- 그 밖의 리팩터 0. 변경 파일은 위 여섯 + 테스트뿐.

## 3. 검증
```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1 && make test    # 전체 · Errors 0
grep -rnE "except (Base)?Exception" app/back/service app/back/repository --include='*.py'      # 0
grep -rnE "finalBatchState|final_batch_state" app/back --include='*.py'                        # 0
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_fd9fc1ce-619d-4f87-b218-10dfaefaa275 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WORK-012 검수 수정" \
  --body "고친 파일 / make test 수치 / grep 둘 0 확인"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] backend 완료 — WORK-012 검수 수정. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] backend: <질문>" --enter`
