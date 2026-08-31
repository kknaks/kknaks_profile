
# [planner] 수정 R3 — WP-125 FAIL 1건(V-3) + 뿌리 1줄(V-3b) + WARN 1건

너는 **mediness `planner` 워커**다. WP-125 가 검수에서 **FAIL 1건** 났다. 이번 발주는 그 해소만 한다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec` (네 미커밋 변경 위에서 계속)

## 1. 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-wp-report.md` ← 이번 발주의 SoT (V-3·V-3b·WARN 의 자리와 권장 수정)

## 2. 고칠 것

**V-3 (FAIL)** — P3 파급 가드가 모달 발 회의를 삼킨다:
- WP-125 P3 의 진입 가드를 「연결 회의 유무」에서 **「자동 등록 회의만(연결 + source 판정)」**으로 좁혀라. 모달 발 회의도 `link_reservation` 으로 `reservation_run_id` 를 가지므로 연결 유무만으로는 못 거른다.
- 「연결 회의가 없으면 no-op(모달 발이 여기 온다)」 서술(:166 괄호)을 사실대로 고쳐라 — 모달 발은 연결이 **있다**.
- **비목표**에 「모달 발로 만들어진 회의의 취소·파급 축(OPEN-031-Y ⓐ·모달 발)」을 추가하고, **P5 테스트 분기**에 「모달 발 예약 취소 시 모달 발 회의 무파급」 케이스를 추가하라.

**V-3b (뿌리)** — SPEC-151 §7.9.5 첫 문장이 source 한정 없이 「연결된 회의는 예약을 따라간다」라 OPEN-031-Y 와 갈린다. **「자동 등록된 회의(§7.9.1 발동 조건으로 만들어진 회의)」로 한정하는 한 줄**로 경계를 명시하라 — 계약 변경이 아니라 의도된 경계의 명문화다. SPEC-031 §3 가산 쪽에 같은 모호함이 있으면 같이 맞춰라.

**WARN** — WP 의 조사 리포트 절 번호 오기(§C-11 → 실제 §3-2 2-b) 정정. log PR 칸은 그대로 «—».

## 3. 하지 말 것

- V-3·V-3b·WARN 외 개정 금지. §7.9 계약 본문·P0~P5 구조 재구성 금지. 코드·커밋·push 금지.

## 4. 검증

```
python3 scripts/lint-pipeline.py --strict → mediness 범위 ERROR 0. 1회만
```

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 preamble 이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ae5c9156-a854-48b7-8f65-528976906150 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "V-3·V-3b·WARN 각각 어디를 어떻게 고쳤나 / lint 결과 / 미결"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 --text "[질문] planner: <질문>" --enter`
