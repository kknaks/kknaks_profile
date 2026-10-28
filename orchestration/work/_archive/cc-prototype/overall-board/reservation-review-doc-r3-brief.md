# [reviewer_doc] 예약 현황 문서 검수 r3 — SPEC-005 0.4.0 · DEC-006 D-58~61 · WORK-007 WP-FIX2/3

너는 **cc-prototype `reviewer_doc` 워커**다. **앞 판의 맥락이 없다.** 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` (코디 워크트리 — **read-only**. 리포트 1개만 만든다)

## 1. SSOT — 대조 기준

- **결정 정본** = `orchestration/work/overall-board/_RESUME.md` §2 의 **2026-10-27 줄 중 예약 현황에 닿는 것**(취소선 = 뒤집힘). 시술 현황(W2) · 앱 줄은 이번 대상 아님
- **E2E 지적 · 처분** = `orchestration/work/overall-board/reservation-e2e-feedback.md` batch 2 · 3 · 4 와 처리 결과 줄
- **KOS 근거(공지)** = `orchestration/work/overall-board/reservation-notice-report.md`(데모 실호출 확인) · 기본값 = `reservation-spec-r4-addendum-1.md`
- **화면 정본 = 배포된 웹 구현**(10-27 · D-60): 코드 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/`(branch `kknaksss/overall-board-2` = main `64e1989` · 읽기만). 시안은 1차 근거일 뿐 — 시안과 다르다는 이유로 FAIL 하지 마라
- 구현 보고(문서가 맞춰야 하는 동작): `reservation-e2e-batch2-*-report.md` · `reservation-e2e-batch3-*-report.md`

## 2. 검수 대상 (planner 보고 `orchestration/work/overall-board/reservation-spec-r4-report.md` — 추가 지시 1 · 2 반영 절 포함)

- `para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md`(0.3.0 → 0.4.0)
- `para/projects/summer-star/cc-prototype/10-decision/decision-006-reservation-board.md`(D-58 ~ D-61 · D-59 개정)
- `para/projects/summer-star/cc-prototype/30-work/work-007-reservation-board.md`(WP-FIX2 · WP-FIX3)
- `reference/2026-10-26-cc-reservation/workflow-v3.md` · README · log.md
- 바뀐 줄: `git -C /Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc diff b618cf70 -- para/projects/summer-star/cc-prototype reference/2026-10-26-cc-reservation`

## 3. 할 일 — 각 지적에 `파일:줄` + 근거 + 판정(FAIL · WARN · PASS)

1. **반영 전수**: batch 2 · 3 · 4 각 지적 → 부록 G · 절 · 10-27 결정 줄 → DEC. 빠짐 · 다르게 = FAIL
2. **문서 ↔ 구현 대조(코드로)**: 0.4.0 이 「구현 `09b1edc` · `0fdeeb1` 대로」라고 적은 곳이 실제 코드와 맞나. 특히 부상태 색 규칙(귀가 대기 / 완료 색 — planner 어긋남 #4) · 상담사 목록 제외(D-59 · `service/reservations.py`) · 모달 폴링 · 404 `reservation_gone` · `flow.times`
3. **공지 계약(§5.15 · `PUT /api/reservations/notice`)**: 노티스 리포트와 맞나 · 기본값(Q-138~144)이 그대로 들어갔나 · BE ↔ FE 가 SPEC 만 보고 따로 짤 수 있나(요청 · 응답 · 오류 코드 · 지난 날짜 · 빈 저장 = 지우기 · 2000자 · 캐시 비움)
4. **WP-FIX3**(batch 4 #1 예약 카드 드래그 + 공지): 대상 파일 · 완료 조건 · 검증 명령 · E2E 시나리오(#42~#46 등)가 사용자가 실물에서 볼 자리인가. **예약 카드 「잡아 끌기」 단계가 E2E 에 있나**
5. 회귀: SPEC-003(시술 현황) · SPEC-004(앱)과 겹치는 env · API 가 깨지지 않나(`KOS_EXCLUDE_ACCOUNT_IDS` 공유 등)
6. 링크 · 인덱스 · 버전 · **public**(실명 · 키 · KOS id · 토큰 0 — grep)

## 4. allowed_paths

- 산출물 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-review-doc-r3.md`. 그 밖 수정 금지

## 5. 범위 제약

- 어떤 파일도 고치지 마라. 결정을 대신 내리지 마라 — 「사용자 결정 필요」로 따로 모은다
- 이미 PASS 였던 0.3.0 이전 절을 다시 뒤지지 마라 — 0.4.0 에서 바뀐 곳 + 그 회귀만

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 과 다르면 preamble 쪽으로만 보내라.

- 커밋·push·PR 하지 마라.

```bash
orca orchestration send \
  --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_3954e4b8-82fc-43ec-a483-79041a8a360e \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "reviewer_doc 완료: 예약 현황 r3 <판정 한 줄>" \
  --body "리포트 경로 / FAIL n · WARN n / FAIL 목록 한 줄씩 / 사용자 결정 필요 목록"

orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 \
  --text "[worker_done] reviewer_doc 예약 현황 r3 — <판정>. 상세는 reservation-review-doc-r3.md" --enter
```

- 막히면 물어라: `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] reviewer_doc: <질문>" --enter`
