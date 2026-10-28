# [planner] SPEC-005 0.3.0 → 0.4.0 — E2E batch 2 · 3 · 4 반영 + 10-27 결정

너는 **cc-prototype `planner` 워커**다. **앞 판의 맥락이 없다** — 이 브리프와 아래 파일만 믿어라. 먼저 역할 문서를 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` (코디 워크트리 — 공유. allowed_paths 밖은 건드리지 마라)

## 1. SSOT — 먼저 읽을 것

- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/_RESUME.md` §2 — **2026-10-27 줄 전부**(이번 판 원천). 이 가운데 SPEC-005 에 닿는 것: 부상태 색 규칙 · batch 2 발주 줄(상담사 목록 제외 규칙) · 진행 경로 ≠ KOS 상담 필요 · 모달 폴링 · 등록 모달에서 뺀 칸 · 접수 신분 조건 뺌 · 이름 경고 뺌 · 시간축 06–22 · **웹은 구현본이 정본** · 「KOS-DEMO」(아래 §2)
- E2E 지적 · 처분: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-e2e-feedback.md` — **batch 2(#1~#9) · batch 3(#1~#3) · batch 4(#1)** 와 각 「처리 결과」 줄. batch 1 은 0.3.0 에 이미 들어갔다
- 구현 결과(문서가 맞춰야 하는 실제 동작): `reservation-e2e-batch2-backend-report.md` · `reservation-e2e-batch2-frontend-report.md` · `reservation-e2e-batch3-backend-report.md` · `reservation-e2e-batch3-frontend-report.md`(같은 폴더). 코드 = `/Users/kknaks/orca/workspaces/cc-prototype/overall-board`(branch `kknaksss/overall-board-2` = main `64e1989`) — 읽기만
- 지금 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md`(0.3.0) · `10-decision/decision-006-reservation-board.md` · `30-work/work-007-reservation-board.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-26-cc-reservation/workflow-v3.md`
- 앞 판 지시(형식 참고): `reservation-spec-r3-instructions.md` · `reservation-spec-r3-report.md`

기대는 개념: 해당 없음.

## 2. 이번 판에 새로 정해진 것(위 원천에 없거나 덧붙임)

- **「KOS-DEMO」 상담사 목록**: 데모에서는 **시스템 계정까지 그대로 다 넣는다** · 운영(prod)에서 나중에 뺀다(사용자 10-27). → 제외 목록은 env 로 지점마다 · 데모 기본 = 빈 목록 · 운영 값은 배포 때 — SPEC 에 이 모양으로. 지금 「마취용」 제외 동작은 구현 그대로 적는다(보고서 확인)
- **웹은 구현본이 정본**: SPEC-005 머리말의 「시안이 정본 · 시안과 다르면 시안대로」 류 문장을 「0.4.0 부터 웹 화면은 배포된 구현(`64e1989`)이 정본 · 시안 대조 안 함」으로. 시안 `M:` 근거는 지우지 말고 「1차 근거」로 둔다
- **batch 4 #1 예약 카드 안 잡힘**: SPEC 의 이동(드래그) 계약은 그대로다(KOS 이동 · 정원 찬 칸 미리 막기 · 거절 시 원위치). E2E 시나리오에 「카드를 잡아 끌 수 있다」 단계가 빠져 있으면 넣는다. 원인 · 수정은 구현 몫
- **공지 [수정하기]**: researcher 가 KOS 공지 쓰기를 **병렬로 조사 중**(`reservation-notice-report.md` 예정). 이번 판에는 공지 절에 「[수정하기] 넣음 · KOS 쓰기 = 조사 중」 자리만 두고, 리포트가 오면 코디가 추가 지시로 넘긴다

## 5. allowed_paths

- `para/projects/summer-star/cc-prototype/{20-spec/spec-005-reservation-board.md, 10-decision/decision-006-reservation-board.md, 30-work/work-007-reservation-board.md, 20-spec/README.md, 30-work/README.md, log.md}`
- `reference/2026-10-26-cc-reservation/workflow-v3.md`
- 보고 `orchestration/work/overall-board/reservation-spec-r4-report.md`

## 6. 할 일

1. SPEC-005 0.3.0 → **0.4.0**: 머리말 · 바뀐 절 · 부록 「E2E batch 2 · 3 · 4 반영표」(행 = 지적 #, 열 = 바뀐 절 · 구현 커밋 `09b1edc` · `0fdeeb1`). 보류 · 처분 없음 항목도 행으로(예: batch 2 #3 → 자리만)
2. DEC-006 에 10-27 결정 줄 더함(뒤집힌 D 는 취소선 + 날짜 · 사유)
3. WORK-007 에 WP 두 줄: 「E2E batch 2 · 3 수정(완료 — 커밋)」 · 「E2E batch 4 · 공지 [수정하기](대기)」
4. E2E 시나리오 고침(새 동작 · 뺀 동작)
5. `workflow-v3.md` 해당 줄(상담사 목록 · 부상태 색 · 모달 폴링 · 공지)을 v3 규칙대로
6. 문서와 구현 보고서가 다른 곳이 있으면 **고치지 말고** 리포트 「어긋남」 표에 — 어느 쪽이 맞는지는 코디 · 사용자가 정한다

## 7. 하지 말 것

- 코드 수정 금지. SPEC-003 · SPEC-004 는 이번 판 밖(시술 현황 · 앱은 다음 갈래)
- 실명 · KOS id · 키 · 토큰 금지(public)
- 열린 것을 추측으로 메우지 마라 — OQ 로

## 8. 검증

```
batch 2·3·4 지적 → 절 대조표(빠짐 0) · 10-27 결정 줄 → DEC 대조(빠짐 0) · 실명 · id grep 0
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. preamble 과 다르면 **preamble 이 맞다.** preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_abe51985-8884-4c9e-bc2c-236bb08117b5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

# (2) 직접 주입 — 코디를 깨운다
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 물어라:
  `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] planner: <질문>" --enter`
