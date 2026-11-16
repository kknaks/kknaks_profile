# [planner] 되돌리기 기능 — SPEC-003 0.5.0 · WORK-006

너는 **cc-prototype `planner` 워커**다. **앞 판의 맥락이 없다.** 먼저 역할 문서를 읽어라: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` (코디 워크트리 — 코디와 공유)

먼저 읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/_RESUME.md` §2 · `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md`(0.4.3) · `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/30-work/work-005-overall-board-procedure.md`(형식) · 코드 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/`(읽기만 · main 에 올라갈 PR #6 상태)

allowed_paths: `para/projects/summer-star/cc-prototype/20-spec/`(SPEC-003 · SPEC-004 · README) · `para/projects/summer-star/cc-prototype/30-work/`(WORK-006 새 파일 · README). 코드 수정 금지. public — 실명 · 키 · KOS id 0.

---

# planner r5 — 되돌리기 기능 (SPEC-003 0.5.0 · WORK-006)

정본 = `_RESUME.md` §2 **2026-10-26 줄 2개**(되돌리기 · 아이콘 위치). D-28(되돌리기 없음 · DEC-005)과 SPEC-003 §6.3 · §6.7 #3 「되돌리기 없음」을 뒤집는다(취소선).

## 기능
- [시작] 되돌리기 → 그 시술 **시술 대기** · [종료] 되돌리기 → 그 시술 **시술 중**
- ① 상태를 바꾼 직후 토스트에 [되돌리기] — 누르면 바로 되돌림(확인 모달 없음 — 기본값, 근거 적기). 토스트 시간은 기본값으로 정하고 표시
- ② 시술 줄 되돌리기 **아이콘**: 진행 줄 [종료] 왼쪽 · 완료 줄 「완료」 배지 왼쪽 · 대기 줄은 없음. 호버 = 「되돌리기」 툴팁 → 클릭 = **모달** 「시술 대기로 되돌리겠습니까?」 / 「시술 중으로 되돌리겠습니까?」 [취소] [되돌리기] — **medikit 디자인 시스템 모달**(medikit 1.4.0 에 Modal/Dialog 컴포넌트가 있는지 코드 `procedure/front/node_modules/@medisolve-ai/medikit` 로 확인해 이름을 적어라. 없으면 OQ + 시안 모달 틀). 아이콘 모양은 기본값(되돌리기 화살표)
- 웹만. 앱은 이번 판 무변경(OQ)

## 정할 것(근거와 함께 SPEC 에 — 열린 것은 OQ)
1. **KOS 반영**: 지금 [종료] = 내부 `schedule/flow/v1/commands/change-tasks-complete {complete:true}`(코드 `back/app/domain/kos_ops.py:51`). 되돌리기 후보 = 같은 API `complete:false` — **미확인**. [시작]은 KOS 에 무엇을 보내는지 코드에서 확인(`service/actions.py` — ccc `started_at` · 첫 시작이면 `changeFlowStep(PROCEDURE)`). 되돌린 결과 고객 상태가 바뀌면(진행 → 대기 · 귀가 대기 → 진행) flowStep 반영 규칙. **WP 에 「데모 지점에 실호출 1회로 확인」을 완료 조건으로** 넣는다. 안 받으면 어떻게 할지 OQ.
2. 되돌릴 수 있는 범위: 마지막 조작만인지 · 아무 때나인지 · 호출 · 수락 · 담당의는 어떻게 되나 · 귀가 대기 뒤 [종료] 되돌리기 가능한지 · 마취는 범위 밖(기본값).
3. API: 예 `POST /api/procedures/{id}/undo-start` · `/undo-finish` 또는 하나로 — 오류 코드 · 역할 · event_log · SSE. SPEC-004 §3.4 역할 표 줄.
4. 동시성: 다른 화면이 이미 바꾼 뒤 되돌리기(409 등).

## 산출
- SPEC-003 0.4.3 → **0.5.0** (`(r5)` 표기) · 새 절(예: §5.13 되돌리기) · §6.3 · §6.7 · §7.3 · §9 E2E · §10 OQ · 부록 「10-26 반영표」
- SPEC-004 §3.4 한 줄(버전 0.3.2)
- **WORK-006** 새로(`30-work/work-006-overall-board-undo.md`) — WP-BE · WP-FE · WP-E2E. 계약 고정점 표.
- README 인덱스.

검증: 결정 줄 → 절 전수 · 근거 없는 정책 0(기본값은 기본값 표시) · 실명 0. 끝나면 §9 두 채널.


## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --from term_c17ba57b-2643-40e9-9a04-47da3180e273 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
