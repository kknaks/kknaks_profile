# [frontend] fix5 — 현황의 현재 상태 · 경과 시간 두 줄 (E2E batch-5)

너는 fix4 까지 한 그 frontend 워커다. 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/cc-nav-resv` — 앞 변경 전부 미커밋, 되돌리지 마라. `cc/back/` 은 건드리지 마라.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/20-spec/spec-002-cc-nav-reservation.md` **0.3.3 §5.5** ← 계약
- 원문 · 자리 목록: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/work/cc-nav-resv/e2e-feedback-batch-5.md` — 「#1 · #2 확정 문구(두 줄)」. **한 줄로 합치지 마라** — 사용자가 두 줄을 명시했다
- 시간의 뜻: `cc/back/app/domain/board.py` `commit`(상태가 바뀌면 `since = now`) · 상태 라벨 · key 는 같은 파일 `status`

## 2. 범위

- 1줄 · 2줄 문구를 만드는 함수 **하나**를 두고(예: `lib/` 에) 모든 자리가 그것을 쓴다
- 자리: `fmtElapsed` · `fmtMinSec` 를 쓰는 곳을 **grep 으로 전부 세고**, 그중 현황(고객 상태 경과)인 곳을 전부 바꾼다. batch-5 표의 「안 붙은 곳」 5군데 + 이미 앞말이 붙은 곳(접수대기실 목록 · 직원 상세 등)도 같은 두 줄로 맞춘다. 예약 카드 「N분 지연」 · 단계 줄 시작 시각은 대상 아님 — 다른 값이면 보고에 이유
- 오래 기다림 빨강: 대기 계열 30분 이상

## 3. 하지 말 것

- §5.5 밖 변경 · `cc/back/` · 사용자 포트 · 프로세스(코디의 3610/8610 포함 — **지금 사용자가 3610 을 쓰고 있다**)

## 8. 검증

```
cc/front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 기능 폴더 밖 import 없는지. 실행 못 한 검증은 사유와 함께 pending
```

- 보고에: 자리 ↔ 파일:줄 표(전/후 문구) · grep 으로 센 수

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 코디 핸들이 세션 재연결로 바뀌었다(지금 `term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e`). preamble 과 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend(fix5) 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e \
  --text "[worker_done] frontend(fix5) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e --text "[질문] frontend(fix5): <질문>" --enter`
