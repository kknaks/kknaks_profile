# [planner] 스펙 개정 r3 — 재검수 r2 N1 · N2 · R1 ~ R4 반영

너는 **day `planner` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/roles/day/planner/role.md` (+ 같은 폴더).

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-kos-call-notify-spec` — r2 미커밋 변경 위에서 이어 고친다. base `origin/main`.

## 1. SSOT

- 재검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/review-doc-r2-report.md` (N1 · N2 · R1 · R2 · R3 · R4 — 근거 줄을 직접 읽어라)
- 앞 발주서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/day-kos-call-notify-spec-brief.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/day-kos-call-notify-spec-r2-brief.md`
- 코드(읽기 전용): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify`

## 2. 배경

r2 재검수 WARN · FAIL 0. 남은 6건을 닫으면 구현으로 간다.

## 3. 코디 결정 (되묻지 마라)

- **N1** SPEC-002 ② · SPEC-005 「받는 계정」 두 곳에: 「called_doctor 행으로 받는 사람 계산은 **`kind = one` 인 규칙 40 호출만** · `kind = all` 은 위 「받는 계정」(원장 목록 전부) 그대로」.
- **N2** ③에: 「② 대상이 같다 = 같은 `kind` 이고, 지정이면 원장 목록 원장 **집합**이 같음」.
- **R1** ⑤ (ii)를 **전이 판정**으로 바꾼다: 「잠금 뒤 읽은 이전 DAY 값이 READY 가 아니었다가 이번 회차에 READY · doctors[] 원장(전이)일 때만」. (i)은 그대로 둔다. 코드 사실(op 대기 중 status held · `sync_tasks.py:335-336`)을 근거로 단다.
- **R2** 개정 ㉚ 머리 요약(`spec-002:49` 근처)을 r2 · r3 본문과 맞춘다(허용 오차 묶음 · W1 거름/전이 · 그 원장들만 · 두 경로).
- **R3** (라)에: 「판별 = `last_error` 가 BLOCKED · 토큰 없음이면 보내기 전 · 그 밖 `failed` 는 모두 메아리 창(안전한 쪽)」.
- **R4** ③ · OQ-106: 「시각 차 = 그 묶음의 가장 이른 새 시각과의 차」.

## 5. allowed_paths

- `products/day/`

## 6. 할 일

1. §3 대로 SPEC-002 · 005 고침. 근거 「검수 r2 <id> · 코디 2026-11-25」. 뒤집은 문장은 취소선.
2. `log.md` r3 한 줄.

## 7. 하지 말 것

- 위 6건 밖 문장 손대지 않기. 새 알림 종류 · 글자 · 스위치 · 환경 분기 · migration 금지. 코드 레포 수정 · 커밋 · push · PR 금지.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0
```

- 보고 본문에 6건 → 고친 파일:줄 표.

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
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
