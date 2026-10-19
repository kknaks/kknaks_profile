# [frontend] fix4 — E2E batch-4 다섯 건(예약 카드 배치 · 국적 칩 · 첫내원 · 오늘 예약 줄 삭제 · 선택 표시 · 드롭다운 잘림)

너는 fix3 까지 한 그 frontend 워커다. 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/cc-nav-resv` — 앞 변경 전부 미커밋, 되돌리지 마라. `cc/back/` 은 건드리지 마라.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/20-spec/spec-002-cc-nav-reservation.md` **0.3.2 §5.4** ← 계약. §5.3 과 다르면 §5.4 가 맞다
- 원문 · 원인: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/work/cc-nav-resv/e2e-feedback-batch-4.md` #1 ~ #5

## 2. 범위 — §5.4 여섯 줄 그대로

- 「첫 방문」 문자열 · `VisitChip` 을 **grep 으로 전부 세고** 바꿔라(back 이 내려 주는 문구가 있으면 front 에서 바꾸지 말고 보고 — back 은 이번에 안 건드린다)
- 국적 칩은 1차 직원 화면이 쓰는 함수 · 모양을 재사용

## 3. 하지 말 것

- §5.4 밖 변경 · `cc/back/` · 사용자 포트 · 프로세스(코디의 3610/8610 포함)

## 8. 검증

```
cc/front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 기능 폴더 밖 import 없는지. 실행 못 한 검증은 사유와 함께 pending
```

- 보고에: 항목 ↔ 파일 표 · 「첫 방문」 grep 전/후 수

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 코디 핸들이 세션 재연결로 바뀌었다(지금 `term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e`). preamble 과 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend(fix4) 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e \
  --text "[worker_done] frontend(fix4) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e --text "[질문] frontend(fix4): <질문>" --enter`
