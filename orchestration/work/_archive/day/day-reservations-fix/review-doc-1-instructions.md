# [reviewer_doc] 예약 현황판 F1 ~ F6 · 문진 6개월 · KOS 문진 읽기 — SPEC 개정 1차 검수

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservations-fix-spec` — planner 가 남긴 **미커밋 변경**이 검수 대상(`git status` · `git diff` · base `origin/main` `b9ac374e`). **파일을 고치지 마라**(stash · checkout · reset 금지).

## 1. SSOT — 대조 기준

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/_RESUME.md` **§2 결정 표 2026-11-27 행** ← 사용자 결정(정본 · 위 행이 아래 행을 덮음 · 취소선 = 뒤집힘). §1 F1 ~ F6 = 피드백 원문
- planner 가 받은 지시서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/planner-1-instructions.md`(범위 · 금지)
- 근거 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/research-1-report.md` · `be-f6-debug-1-report.md` · `be-kos-questionnaire-1-report.md`(KOS 경로 · 키 · 답 대조 — 실물 정본)
- 스크린샷: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/f1-kos-add-slot.png` · `f3-*.png` · `f5-*.png`
- 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservations-fix` (CENTURION_DAY `origin/dev` `65506f35`)

## 2. 볼 것 (판정 축)

1. **결정 반영**: 결정 표 11-27 행마다 SPEC 의 어느 문장(파일:줄)에 들어갔나 — 대조 표를 리포트에. 뒤집힌 행을 옛 쪽으로 적은 곳
2. **KOS**: 경로 = 내부 `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy` · 키 · 답 맞춤 표가 be-kos 리포트와 한 글자씩 맞나. **공개(open) 호출을 새로 둔 곳 = FAIL**(사용자 결정 「내부 API 만」)
3. **지어낸 정책 · 문구**: 결정 · 리포트 근거 없는 규칙 · 화면 문구(허용 문구 = 「링크 복사하기」 「링크 열기」 「6개월 경과」 「연결」 「미연결」 + 기존 SPEC 문구)
4. **코드 실물과 어긋남**: 칸 · 테이블 · enum(`source` 값 · `external_ref` entity_type) · `questionnaire_history` · `tasks/emr.py` · `routers/reservation_detail.py` origin 4곳 · `policies/reservation_layout.py` · `day.js` 토큰
5. **문서끼리 어긋남**: spec-006 개정 ⑯ ↔ spec-007 고침 8 ↔ spec-000 개정 ④ ↔ spec-002 · 003 — 특히 R64 · R70 · R71 · R41 ~ R44 와 새 배치 규칙
6. **OQ 품질**: OQ 가 정말 열린 것인가(결정 · 리포트에 답이 있는데 OQ = FAIL). 각 OQ 를 「사용자에게 물을 것 / 코디 기본값으로 닫을 것」으로 나누고, 닫을 것은 기본값 제안 · **구현을 막는 OQ** 표시
7. 범위: 모달 디자인 · 외국인 신분확인 · 기획안을 안 건드렸나
8. `python3 scripts/lint-pipeline.py --strict` 다시 돌려 products/day 범위 ERROR 0

## 3. allowed_paths

- 리포트 1개만 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/review-doc-1-report.md`

## 4. 하지 말 것

- 파일 수정 · 커밋 · push 금지. KOS 호출 · dev / prod 접속 금지.

## 5. 리포트 모양

맨 위: 판정(PASS / WARN / FAIL) 한 줄 · FAIL / WARN 목록(파일:줄 · 근거 · 고칠 방향) → 결정 대조 표 → OQ 분류 표.

## 6. 검증

```
SPEC·WORK 를 DEC·baseline 에 대조. lint-pipeline --strict 로 products/day/ ERROR 0. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_99b025fc-f3ef-403e-8162-509c41545e2e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
