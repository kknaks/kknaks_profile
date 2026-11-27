# [reviewer_doc] DAY-SPEC-008 (새 · draft) + SPEC-006 ⑭ · 005 · 007 고침 6 · 000 ③ 1차 검수

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation3-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 이 워크트리에는 planner 가 남긴 **미커밋 변경**이 있다 — 그게 검수 대상이다. 파일을 고치지 마라(stash · checkout · reset 금지). planner 터미널이 같은 워크트리에 살아 있지만 지금 쉬고 있다.

## 1. SSOT — 대조 기준

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/reference/2026-11-26-reservation-request/reservation-request-decisions.md` ← **사용자 결정 RQ1 ~ RQ44(정본)**
- 코디 결정 11-26(planner 질문 답 · 정본에 준함): ① 생성 전 `change` = 신규로 기록 · [예약 생성] / 생성 전 `cancel` = 409(철회 경로) ② 새 알림 종류는 앱 unread · 목록에서 뺌(웹만) ③ 재진 고객 그날 예약 있음 = 이번엔 안 막음 · OQ ④ 초진 생성 때 KOS 같은 고객 찾기에 걸리면 생성 막고 「고객 확인 필요」
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/design/20261126_예약현황_시연_v15.html` ← 시안 v15(생김새 · 문구 정본 — base64 빼서 grep) · 같은 폴더 위 `design-1-report.md` ~ `design-6-report.md`(지은 문구 목록)
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/day-reservation3-spec-brief.md` ← planner 가 받은 브리프(범위 · 금지)
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/ext-request-body-draft.md` ← 본문 초안(이름 제안)
- KOS 실물 근거: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/_archive/day/day-reservation2/be-probe-1-report.md` ~ `be-probe-4-report.md`

## 2. 배경

planner 가 `products/day/20-spec/spec-008-reservation-request.md`(새 · draft · 603줄) · SPEC-006 개정 ⑭ · SPEC-005 개정 · SPEC-007 고침 6 · SPEC-000 개정 ③ · `20-spec.md` · `30-work.md` · `10-decision.md` · `log.md` 를 고쳤다(`git status` · `git diff`). 구현 발주 전에 결정 · 시안 · 실물 · 코드에 대조해 판정한다. 사용자는 이 스펙으로 **바로 코드까지** 가기로 했다 — 구현자가 이것만 보고 짤 수 있어야 한다.

## 3. 계약

해당 없음.

## 4. 볼 것 (판정 축)

1. **결정 반영**: RQ1 ~ RQ44 + 코디 결정 ①~④ 가 빠짐 · 틀림 없이 들어갔나(RQ 대조 표를 리포트에)
2. **ext API(E1 ~ E8)**: 본문 · 응답 · 오류 코드 · `Idempotency-Key` · `updated_since` 가 기존 ext 관례(`schemas/ext*.py` camelCase · `ExtErrorResponse` · `FROZEN_FORBID_CONFIG`)와 맞나 · 구현자가 바로 짤 만큼 빠짐 없나
3. **ext 키 병원당 하나(RQ7)**: `partner` 쓰는 곳 전수 — `git -C /Users/kknaks/git/CENTURION_DAY grep -n partner origin/dev -- backend` 결과와 SPEC 표를 한 줄씩 대조(빠진 곳 = FAIL) · DB 칸 · 유일키 · 마이그레이션 · 배포 순서
4. **KOS 쓰기**: 경로 · 본문 키 · 확인 조건 · 순서 묶음이 be-probe · `emr/kos/writes.py` 와 맞나 · 실물 없는 칸을 정해 버린 곳(OQ 여야 함) · 메모 합치기 형식(RQ28)
5. **상태 전이 · 케이스**: 스레드 × 이벤트 표에 구멍(정의 안 된 조합) · 서로 모순
6. **DAY 코드 실물과 어긋남**: 칸 이름 · 테이블 · enum(`NotificationKind`) · `reservation_book.book()` · 웹 알림 `day.js` · 권한 키 · 쓰기 큐
7. **지어낸 정책 · 문구**: 근거 없는 규칙 · 화면 문구(「임시」 표시 없이 정한 것)
8. **문서끼리 어긋남**: 008 ↔ 006 ⑭ ↔ 005 ↔ 007 고침 6 ↔ 000 ③
9. **OQ 품질**: OQ-Q01 ~ Q19 가 정말 열린 것인가 · 사용자 질문 / 코디 기본값 / 구현 때 실물 확인으로 분류 제안
10. `python3 scripts/lint-pipeline.py --strict` 다시 돌려 products/day 범위 0 error 확인

## 5. allowed_paths

- (read-only — 리포 파일 수정·생성 금지. 산출물은 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/review-doc-1-report.md`)

## 6. 리포트

맨 위: 판정(PASS / WARN / FAIL) · FAIL n · WARN n 표(번호 · 파일:줄 · 무엇이 · 근거 · 고칠 방향). 그 아래 RQ 대조 표 · partner 전수 대조 표 · OQ 분류 표.

## 7. 하지 말 것

- 파일 수정 · 커밋 · stash 금지. 결정을 새로 만들지 마라(제안은 「고칠 방향」으로만).

## 8. 검증

```
FAIL · WARN 마다 파일:줄 + 근거(RQ# · be-probe § · 코드 ref). 근거 없는 지적 0
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_5c196973-a9ec-4982-81c2-655361f18aec --from term_1c14d990-5d0b-4793-8bdc-ea1065c21ed1 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5c196973-a9ec-4982-81c2-655361f18aec \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5c196973-a9ec-4982-81c2-655361f18aec --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
