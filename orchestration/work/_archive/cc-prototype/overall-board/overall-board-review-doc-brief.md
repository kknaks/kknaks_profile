# [reviewer_doc] SPEC-003 0.4.0 · WORK-005 검수 — 전체현황판 시술 현황 반영

너는 **cc-prototype `reviewer_doc` 워커**다. **앞 판의 맥락이 없다.** 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` (코디 워크트리 — **read-only**. 리포트 1개만 만든다)

## 1. SSOT — 대조 기준

- **결정 정본** = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/_RESUME.md` §2 결정 표의 **2026-10-23 줄**(취소선 줄은 뒤집힌 것 — 지금 것만)
- **시안(정본)** = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/design/Ceramique 전체현황판.dc.html` 「시술 현황」(`M:777-1153`) · 헤더(`M:63-92`) / 분석 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/design-analysis-report.md`
- 현재 코드 인벤토리 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/current-board-report.md` · 코드 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/` (읽기만)
- 앞 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/10-decision/decision-005-procedure-board.md`

## 2. 검수 대상

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` (0.3.0 → 0.4.0 — `git -C /Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc diff -- para/` 로 바뀐 줄 확인)
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/30-work/work-005-overall-board-procedure.md` (새로) · 두 README 인덱스
- planner 의 자기 보고 요지: 방 배정 = 방 있는 ETCETERA 를 back `Rules.items` 에서 뺌 · `board_order`(하루 1행 · visit_ids json) · `PUT /api/board/order {visitIds}` · 스냅샷은 `cards[]` 배열 순서 · 새 OQ-520~525

## 3. 계약

해당 없음 (검수).

## 4. 먼저 볼 곳

- SPEC-003 §3.2 · §5.1 · §5.9 · §5.12(새) · §6.2 ~ §6.7 · §7.2 ~ §7.5 · §9 · §10 · 부록 E
- WORK-005 WP 표 · 병렬 고정점

## 5. allowed_paths

- 산출물 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/review-doc-r1.md`. 그 밖 수정 금지.

## 6. 할 일 — 각 지적에 `파일:줄` + 근거 + 판정(FAIL · WARN · PASS)

1. **결정 반영 전수**: 10-23 결정 줄마다 SPEC 의 어느 절에 어떻게 들어갔나. 빠졌거나 다르게 들어갔으면 FAIL. 특히
   - 「방 배정」 줄만 빼고 **다른 ETCETERA(마취 · 시트팩 · 관리 마무리)는 남는다** — SPEC 이 이걸 정확히 지키나. back 에서 빼는 방식이 귀가 대기 때 남은 기타 작업 취소(`open_task_seqs`) · 방 판정(`room` 계산) · 시술실 앱 화면에 부작용이 없는지 코드로 확인
   - 헤더 「현황」 하나 · 입실순/배치순 제거 · KOS 반영 표시 제거 · 드래그 순서 DB 저장(공유 · 그날 단위 · 새 카드 맨 뒤 · 귀가 대기 제외)
2. **시안 대조**: SPEC 이 「시안대로」라고 한 곳이 실제 시안과 맞나(`M:줄`로). 시안과 코드가 다른데 SPEC 이 아무 말도 안 한 자리(조용히 빠진 것)를 찾아라.
3. **결정 밖 정책 발명 여부**: 근거 없이 SPEC 에 새로 들어간 정책. 기본값이면 기본값이라고 표시됐나.
4. **드래그 계약 완결성**: 테이블 · API · 오류 · 동시성 · 스냅샷 · SSE · 날짜 경계(자정) · 귀가 대기로 바뀐 카드 · 목록 밖 카드. BE 와 FE 가 이 계약만 보고 따로 구현할 수 있나.
5. **WORK-005**: WP 마다 대상 파일 · 완료 조건 · 검증 명령이 있나. BE ↔ FE 병렬 고정점이 충분한가. E2E 항목이 사용자가 실물에서 볼 자리를 덮나.
6. 링크 · 인덱스 · 버전 표기 · public(실명 · 키 · KOS id 0 — grep).

## 7. 범위 제약

- 어떤 파일도 고치지 마라. 결정을 대신 내리지 마라 — 결정이 필요한 것은 「사용자 결정 필요」로 따로 모은다.
- 예약 현황 · 원내 현황은 범위 밖.

## 8. 검증

```
SPEC·WORK 를 DEC 에 대조. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

- 리포트 맨 위에 종합 판정(PASS / FAIL)과 FAIL · WARN 개수.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --from term_0c0ac6e2-6a29-499b-9a3d-26fca0fa1784 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
