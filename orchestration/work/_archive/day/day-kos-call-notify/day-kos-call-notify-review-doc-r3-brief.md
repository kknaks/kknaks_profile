# [reviewer_doc] 스펙 재검수 r3 — 6건만

너는 **day `reviewer_doc` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더).

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-kos-call-notify-spec` (읽기만) · 코드(읽기 전용): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify`

## 1. SSOT

- 너의 r2 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/review-doc-r2-report.md` (N1 · N2 · R1 · R2 · R3 · R4)
- r3 발주서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/day-kos-call-notify-spec-r3-brief.md` §3(코디 결정)

## 6. 검수 항목

1. 6건이 r3 발주서 §3 대로 고쳐졌나(파일:줄 · 코드 근거) · 닫힘/남음 표.
2. 고친 줄이 새 모순을 만들었나(특히 R1 전이 판정 × W1 (i) · op held 중 status · N1 kind=all 받는 사람).
3. 6건 밖은 다시 보지 마라(r2 에서 닫힌 것 재론 금지). lint `--strict` products/day ERROR 0.

## 5. allowed_paths

- 리포 수정 금지. 산출물 = `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/review-doc-r3-report.md` 1개.

## 8. 판정

PASS / WARN / FAIL. WARN 이면 구현 착수를 막는지(막음/안 막음) 지적마다 적어라.

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
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
