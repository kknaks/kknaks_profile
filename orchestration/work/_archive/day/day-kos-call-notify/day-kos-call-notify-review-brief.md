
# [reviewer] #283 코드 검수 r1 — KOS 호출 → DAY 원장 호출 알림

너는 **day `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

backend 워커는 끝났다(미커밋 변경이 워크트리에 있음) — **읽기만**. 시험 실행은 된다(로컬 compose 시험 스키마 · 사용자 스택 · 포트 손대지 않기).

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/day-kos-call-notify-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ㉚ · **규칙 40 ① ~ ⑨** · OQ-99 ~ 107 ← 계약 SoT
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-kos-call-notify-spec/products/day/20-spec/spec-005-notifications.md` §3 「KOS 에서 건 호출」 · 「받는 계정」
- Delivery #283(`gh issue view 283 -R MediSolveAIDev/CENTURION_DAY`) Acceptance
- 구현 보고: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/be-impl-r1-report.md` (커밋 경로 표 · 주의 사항)
- 문서 검수에서 짚은 경쟁 상황: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/review-doc-r1-report.md` · `r2` · `r3`

기대는 개념: 해당 없음.

## 2. 배경

간호사가 KOS 에서 원장을 호출해도 DAY 알림 · 푸시가 0 이던 것을, 동기화가 KOS 호출을 DAY `doctor_call` 로 만들고 기존 `after_call` 을 태우게 고쳤다. **핫픽스 — 이 코드가 dev 배포 뒤 prod 로 바로 나간다.** 정식 앱 0.1.0 이 받는 모양이 바뀌면 안 된다.

## 3. 계약

해당 없음(BE 단독).

## 4. 먼저 볼 것

- `git -C /Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify diff` + 새 파일 `backend/day/policies/kos_calls.py` · `backend/day/services/kos_calls.py` · 시험 4개.

## 5. allowed_paths

- 리포 수정 금지. 산출물 = `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/review-code-r1-report.md` 1개.

## 6. 검수 항목

1. 규칙 40 ① ~ ⑨ 와 ext_sync 확장(코디 결정)이 빠짐없이 · 스펙대로 구현됐나(규칙마다 코드 파일:줄 대응표).
2. **같은 KOS 호출 → doctor_call 1개 · 원장 계정당 알림 1 · 푸시 1** 이 실제로 보장되나. 보고서 주의 「겹침 시험이 Refs.link 행 잠금 때문에 방문 잠금 없이도 통과」 — 방문 잠금(`board:{visit_id}`) 이 판정 · 생성 구간을 실제로 감싸는지, 판 조작(DAY call/recall/accept/cancel)과 겹칠 때 깨지는 순서가 있는지 코드로 따져라. 시험이 그걸 판별 못 하면 지적.
3. 커밋 뒤 `after_call` 이 모든 커밋 경로(보고서 표)에서 정확히 한 번 · 롤백 때 안 불림 · 예외가 동기화 회차를 죽이지 않음.
4. 메아리 창 (가) ~ (라) · `last_error` 판별 · KOS 수락 W1 (i) + 전이 · 늦은 관측 거름 · 묶음(같은 kind + 집합 · 가장 이른 시각 30초) — 경계값.
5. `_recipients` 변경이 DAY 에서 누른 호출(시스템 계정이 아닌 호출 · kind one/all)의 기존 받는 사람을 바꾸지 않나. 시스템 계정으로 DAY 로그인해 누른 호출(OQ-107 ⓒ) 영향.
6. 0.1.0 호환: 알림 행 · payload · 판 DTO 모양 무변경.
7. 성능: 10초 회차에 추가 쿼리 수 · N+1.
8. 시험 판별력 — 핵심 규칙 하나씩 일부러 깨면(머릿속 변이) 시험이 잡나. 빠진 시험.
9. `cd backend && uv run pytest -q <새 시험 4개 + 동기화 · 판 호출 · 알림 기존 시험>` 1회 · `uv run ruff check <바뀐 파일>`.

## 7. 범위 제약

- 고치지 마라 — 지적만. 커밋 · push 금지. 사용자 스택 · 포트 · 공유 DB 금지.

## 8. 검증

판정 PASS / WARN / FAIL + 지적마다 [심각도 · 파일:줄 · 근거 · 고칠 방향]. FAIL = prod 에서 알림 누락 · 중복 · 엉뚱한 수락 · 동기화 장애가 날 지적이 하나라도. 마지막에 「사용자가 실물에서 만날 자리」.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
