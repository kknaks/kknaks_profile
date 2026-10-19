# [frontend] fix3 — E2E batch-3 여덟 건(예약 탭 칸 · 카드 두 줄 · 지연 표시 · VIP 자리 · 접수 모달 예약 메모 · 드롭다운 · 버튼 고정 · 고객 패널 폭)

너는 fix2-FE 까지 한 그 frontend 워커다. 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/cc-nav-resv` — 앞 변경 전부 미커밋, 되돌리지 마라. `cc/back/` 은 건드리지 마라(이번엔 back 변경 없음).

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/20-spec/spec-002-cc-nav-reservation.md` **0.3.1 §5.3** ← 계약. §5.2 와 다르면 §5.3 이 맞다
- 원문 · 원인: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/work/cc-nav-resv/e2e-feedback-batch-3.md` #1 ~ #8
- 데이터: 접수 모달의 예약 메모 · 고객 메모 = 이미 읽는 `GET /api/patients/{id}` 의 `reservationMemo` · `customerMemo`(8610 에서 확인함). 새 API 없음

## 2. 범위 — §5.3 여덟 줄 그대로

자리마다 **쓰는 곳을 grep 으로 전부 세고** 시작하라. 특히: VIP 칩이 들어갈 자리 · 「늦음」 문자열 · 예약 카드를 그리는 곳(Aside 예약 탭 · 폰) · `<select>` 를 쓰는 곳 전부.

## 3. 하지 말 것

- §5.3 밖 변경 · 메모 뽑기/요약(원문 그대로) · `cc/back/` · 사용자 포트 · 프로세스(코디의 3610/8610 포함)

## 8. 검증

```
cc/front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 기능 폴더 밖 import 없는지. 실행 못 한 검증은 사유와 함께 pending
```

- 보고에: #1 ~ #8 ↔ 바뀐 파일 표 · grep 으로 센 자리

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 코디 핸들이 세션 재연결로 바뀌었다(지금 `term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e`). preamble 과 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend(fix3) 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e \
  --text "[worker_done] frontend(fix3) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e --text "[질문] frontend(fix3): <질문>" --enter`
