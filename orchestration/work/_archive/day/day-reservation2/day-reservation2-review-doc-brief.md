
# [reviewer_doc] DAY-SPEC-007 (새 · draft) + SPEC-006 ⑫ · 002 ㉘ · 000 개정 ② 1차 검수

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation2-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 이 워크트리에는 planner 가 남긴 **미커밋 변경**이 있다 — 그게 검수 대상이다. 파일을 고치지 마라(stash · checkout · reset 금지).

## 1. SSOT — 대조 기준

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-24-reservation-detail/reservation-detail-decisions.md` ← **사용자 결정 D1 ~ D48 + 시술 목록 와이어(정본). 아래 행이 위 행을 덮는다.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-23-reservation/20261124_예약현황_시연.html` ← 시안 v9(생김새 · 문구 정본 · 4MB — base64 빼서 grep)
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-23-reservation/reservation-board-decisions.md` ← 앞 결정 R1 ~ R75
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/day-reservation2-spec-brief.md` ← planner 가 받은 브리프(범위 · 금지)
- KOS 실물 근거: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/be-probe-1-report.md` · `be-probe-2-report.md` · `be-probe-3-report.md` · `research-detail-1-report.md` · HAR `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-24-reservation-detail/*.har`

## 2. 배경

planner 가 `products/day/20-spec/spec-007-reservation-detail.md`(새 · draft) · SPEC-006 개정 ⑫ · SPEC-002 개정 ㉘ · SPEC-000 개정 ② · `20-spec.md` · `30-work.md` · `10-decision.md` · `log.md` 를 고쳤다(`git -C /Users/kknaks/orca/workspaces/mediness-mediness/day-reservation2-spec status` · `git diff`). 구현(WORK · 코드) 발주 전에 결정 · 시안 · 실물 · 코드에 대조해 판정한다.

## 3. 계약

해당 없음.

## 4. 볼 것 (판정 축)

1. **결정 반영**: D1 ~ D48 의 최종 유효 결정이 빠짐 · 틀림 없이 들어갔나(D 번호 대조 표를 리포트에). 뒤집힌 결정(취소선)을 옛 쪽으로 적은 곳
2. **KOS 쓰기 표(W1 ~ W17)**: 경로 · api · 본문 키 · 값 조건 · 확인 조건 · 순서 묶음이 be-probe 리포트 · HAR 와 한 글자씩 맞나. 실물에 없는 칸 · 값을 지어낸 곳
3. **지어낸 정책 · 문구**: 결정 · 시안 · 실물 근거 없는 규칙 · 화면 문구(OQ 로 둬야 할 것을 정해 버린 곳)
4. **DAY 코드 실물과 어긋남**: `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:<path>` — 칸 이름 · 테이블 · enum · `write_open` · 동기화 매핑(지정 의사 `visit_occupied_resource_doctor` 주장 포함 — 실제로 있고 채워지는지) · `visit_task.ticket_id` · `purchase.status/process` · `ticket.status` · `job_role.tags` · `policies/reservation_amounts.py`
5. **문서끼리 어긋남**: SPEC-007 ↔ 006 ⑫ ↔ 002 ㉘ ↔ 000 ② · 앞 결정 R 과 충돌(특히 R57 · R48 상담사 원천 vs OQ-D08)
6. **OQ 품질**: OQ-D01 ~ D21 이 정말 열린 것인가(결정 · 실물에 답이 있는데 OQ 로 둔 것 = FAIL) · 사용자에게 물을 것과 코디 기본값으로 닫을 것 구분 제안
7. 범위: Out Of Scope 가 브리프 §7 과 맞나
8. `python3 scripts/lint-pipeline.py --strict` 다시 돌려 products/day 범위 0 error 확인

## 5. allowed_paths

- (read-only — 리포 파일 수정·생성 금지. 산출물은 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/review-doc-1-report.md`)

## 6. 리포트

맨 위: 판정(PASS / WARN / FAIL) · FAIL n · WARN n 표(번호 · 파일:줄 · 무엇이 · 근거 · 고칠 방향). 그 아래 D 대조 표 · W 대조 표 · OQ 분류 표(사용자 질문 / 코디 기본 / 이미 답 있음).

## 7. 하지 말 것

- 파일 수정 · 커밋 · stash 금지. 결정을 새로 만들지 마라(제안은 「고칠 방향」으로만).

## 8. 검증

```
FAIL · WARN 마다 파일:줄 + 근거(결정 D# · be-probe § · 코드 ref). 근거 없는 지적 0
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --from term_bcd28eb4-3117-4aa1-ba3d-68c3f3073547 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
