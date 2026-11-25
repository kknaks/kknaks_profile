# [planner] 스펙 개정 r2 — 검수 WARN 9건 반영

너는 **day `planner` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/roles/day/planner/role.md` (+ 같은 폴더 rules · skills · tools · workflow).

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-kos-call-notify-spec` — 네가 r1 에서 남긴 미커밋 변경 위에서 이어 고친다.
base `origin/main` → PR `main`(코디가 올린다).

## 1. SSOT

- r1 발주서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/day-kos-call-notify-spec-brief.md` (§3 결정 그대로 유효 — 아래 §3 에서 바뀌는 것만 예외)
- 검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/review-doc-r1-report.md` — 판정 WARN · W1 ~ W9. **각 지적의 「고칠 방향」과 코드 근거(파일:줄)를 직접 읽어라.**
- 코드(읽기 전용 · `origin/dev` 55e60aa4): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify`

## 2. 배경

r1 은 FAIL 0 · WARN 9. 구현 착수 전에 스펙이 한 가지로 읽히게 닫는다.

## 3. 코디 결정 — 지적마다 이렇게 고친다 (되묻지 마라)

- **W1** 규칙 40 ⑤(KOS 수락 반영)에 메아리 거름을 넣는다: 그 작업 sequence 가 든 `call-tasks-doctors` op 이 `pending` · `sent` 이면 ⑤를 하지 않는다 **그리고** KOS `READY` · `doctors[]` 를 그 호출 `created_at` 뒤 회차에서 본 경우만 수락으로 친다. 두 조건 모두.
- **W2** 규칙 40 은 **작업 쓰기 공통 경로(`_apply_tasks`)** 에서 판정한다. 그 경로를 부르는 모든 커밋(10초 일정 조회 · 예약 상세 반영 연쇄) 뒤, 그 transaction 에서 만든 호출마다 `after_call`(수락 반영이면 기존 수락 뒤 처리). 문장에 두 경로를 이름으로 적는다.
- **W3** ① 에 한 줄: 「비교할 이전 `doctor_called_at` 은 방문 잠금(`board:{visit_id}` · 판 조작과 같은 키)을 잡은 뒤 같은 transaction 에서 읽는다 → 동기화 회차 · 판 조작이 겹쳐도 한 변화에 호출 하나 · migration 없음」.
- **W4** ③ 근거를 「미확인 — 첫 실물로 확인」으로 낮추고 OQ 하나 연다(첫 실물 1회에 **여러 작업 동시 호출** 1건 포함). 기본값 = 같은 회차 · 같은 방문 · 같은 대상이면서 새 시각 차가 ⑥ 허용 오차 안이면 한 호출.
- **W5** 지정 2명 이상 = **그 원장들만**(사용자 결정 A2 를 지킨다). 리포트 OQ-100 ⓐ 안 — migration 없이 받는 사람을 그 호출 작업들의 `called_doctor` 행으로 계산 — 을 기본값으로 한다. `doctor_call.kind` · `target_staff_id` 에 무엇을 넣는지(예: 1명이면 one · 그 원장 / 2명 이상이면 어떤 값으로 두고 받는 사람 계산은 called_doctor 로) · 본문 「지정 호출」 · DAY [재호출]·판 표시 영향까지 코드 사실 위에서 한 가지로 적는다. **새 kind · 새 글자 · migration 이 필요해지면 멈추고 질문으로 보고**. OQ-100 · OQ-N22 는 이 기본값으로 갱신.
- **W6** (라)를 「`failed` 이면서 2xx 를 한 번도 받지 않은 op(보내기 전 막힘)만 KOS 가 안 불렸다고 본다 · 2xx 뒤 `failed` 는 `updated_at` + 허용 오차까지 메아리 창」으로 좁힌다.
- **W7** ④ 에 「prod 동기화가 배포 직전까지 돌고 있었을 때」 조건을 붙이고, 운영 메모에 「배포 전 prod worker 동작 확인 · 멈춰 있었다면 OQ-102(오래된 호출 시각 거르기) 를 배포 전에 닫는다」를 가리킨다.
- **W8** SPEC-006 설정 줄 = 「적지 않음 = 꺼짐(코드 기본 False) · 빈 값은 쓰지 않는다」.
- **W9** ⑨ 의 [재호출] 대상 = 「사슬 맨 처음 호출의 대상(규칙 6 그대로 — KOS 가 이어 받은 호출이라도)」으로 고친다. 사슬은 ④ 대로 잇는다.
- 참고 기존 부채(㉘ 본문 「㉚ C36」 글자)는 건드리지 않는다.

## 4. 먼저 읽을 파일

- 리포트 각 W 의 근거 줄 그대로.

## 5. allowed_paths

- `products/day/`

## 6. 할 일

1. §3 대로 SPEC-002 · 005 · 006 고침. 바뀐 줄의 근거에 「검수 r1 W<n> · 코디 2026-11-25」.
2. `log.md` 는 r1 줄을 고쳐 쓰거나 한 줄 더한다(기존 형식).
3. OQ 표 갱신(새 OQ 번호는 이어서).

## 7. 하지 말 것

- r1 에서 맞다고 판정된 곳을 다시 쓰지 않는다. 새 알림 종류 · 글자 · 스위치 · 환경 분기 · migration 금지(필요하면 질문).
- 코드 레포 수정 · 커밋 · push · PR 금지. 30-work WP 쓰지 않음.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고)
```

- 보고 본문에 W1 ~ W9 각각 → 고친 파일:줄 표.

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
