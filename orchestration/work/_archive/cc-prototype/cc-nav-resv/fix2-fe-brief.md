# [frontend] fix2-FE — 기획자 피드백 반영: 한글 읽기 · 시간 표기 · 예약 탭 · 검색 · 현황 카드 · 접수대기실→고객 패널 · 접수 모달 · 부연 설명 삭제

너는 WP1~WP4-FE · fix1 을 한 그 frontend 워커다. 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/cc-nav-resv` — 앞 변경 전부 미커밋, 되돌리지 마라. backend 워커가 같은 워크트리 `cc/back/` 에서 fix2-BE 를 병렬로 한다 — `cc/back/` 은 건드리지 마라. 새 응답 필드(`phoneticName` · `phone` · `vip`) · `POST /api/desk/memo` · check-in `memo` 는 §5.1 계약대로 짓고, BE 가 끝나면 코디가 실응답 예시를 보낸다.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/20-spec/spec-002-cc-nav-reservation.md` **0.3.0 — §4 · §5 전부** ← 계약의 SoT. 여기 없는 건 발명하지 마라
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/10-decision/decision-004-cc-nav-reservation.md` D-22 ~ D-35 (D-23: 이 범위만 1차 화면을 고친다 — 그 밖은 무변경)
- 판단 원문: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/00-baseline/baseline-007-planner-feedback.md` 「사용자 판단」 칸 · 「접수 모달」 절
- 목업(참고 · 이 절과 다르면 SPEC 이 맞다): `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/reference/2026-10-12-cc-prototype/CC데모-변경목업.html` · `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/assets/cc-feedback-*.png`
- E2E batch-2: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/work/cc-nav-resv/e2e-feedback-batch-2.md` #1 · #2

## 2. 범위 = SPEC-002 §5.2 (+ §3.3 부연 설명 삭제 = batch-2 #1)

항목마다 **쓰는 곳을 grep 으로 전부 세고** 시작하라(목록을 주면 FAIL 은 목록 밖에서 난다):
1. 한글 읽기 — 영문 이름이 찍히는 자리 전부
2. 경과 시간 — `fmtElapsed` · `fmtMinSec` 를 쓰는 곳 전부 + 그 밖에 시간을 직접 포맷하는 곳
3. 예약 탭 칸 · 필터 · 카드
4. 고객 검색(Aside 탭 위)
5. 현황 탭 고객 카드
6. 접수대기실 → 고객 패널 · [방 배정](접수대기실 고객만)
7. 접수 모달 재배치(지난 방문 · 자동 체크 없음 · 시술권 문구 · 추가 요청 메모 · 순서 미리보기 삭제)
8. 예약관리 부연 설명 삭제 — batch-2 #1 표 + 같은 기준으로 grep

## 3. 하지 말 것

- §5.2 밖의 1차 화면 변경(D-23) · 목업에만 있고 SPEC 에 없는 것(주의사항 · 오늘 받을 시술 · 전화번호 표시 · 보낼 곳 · 호출 · 배정 제안 등)
- `cc/back/` · 사용자 포트 · 프로세스(코디의 3610/8610 포함)

## 8. 검증

```
cc/front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 기능 폴더 밖 import 없는지. 실행 못 한 검증은 사유와 함께 pending
```

- 보고에: 항목 1~8 ↔ 바뀐 파일 대응 표 · grep 으로 센 자리 수 · 목업과 다르게 한 곳

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 코디 핸들이 세션 재연결로 바뀌었다(지금 `term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e`). preamble 과 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend(fix2) 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e \
  --text "[worker_done] frontend(fix2) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e --text "[질문] frontend(fix2): <질문>" --enter`
