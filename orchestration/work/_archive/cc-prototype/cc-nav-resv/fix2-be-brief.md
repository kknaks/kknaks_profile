# [backend] fix2-BE — 기획자 피드백 반영: 시드 필드 · 응답 필드 · 시술권 차감 시점 · 추가 요청 메모 · 시술 후보 정정

너는 WP4-BE 를 한 그 backend 워커다. 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/cc-nav-resv` — 앞 변경 전부 미커밋, 되돌리지 마라. frontend 워커가 같은 워크트리 `cc/front/` 에서 fix2-FE 를 병렬로 한다 — `cc/front/` 는 건드리지 마라.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/20-spec/spec-002-cc-nav-reservation.md` **0.3.0 — §4 · §5 전부** ← 계약의 SoT. 여기 없는 건 발명하지 마라
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/10-decision/decision-004-cc-nav-reservation.md` D-22 ~ D-35 (D-23: 이 범위만 1차 화면을 고친다 — 그 밖은 무변경)
- 판단 원문: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/00-baseline/baseline-007-planner-feedback.md` 「사용자 판단」 칸 · 「접수 모달」 절
- 목업(참고 · 이 절과 다르면 SPEC 이 맞다): `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/reference/2026-10-12-cc-prototype/CC데모-변경목업.html` · `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/assets/cc-feedback-*.png`
- E2E batch-2: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/work/cc-nav-resv/e2e-feedback-batch-2.md` #1 · #2

## 2. 범위 = SPEC-002 §4 · §5.1

1. **시드**: `cc/back/data/scenario/seed.json`(gitignore 로컬 데이터 — 이번엔 고쳐도 된다)의 visitor 에 `phoneticName` · `phone` · `categories`. 값은 **가짜**: 가짜 이름에 맞춘 한글 읽기, 국가번호 형식만 맞춘 가짜 번호. VIP 1명. `seed build`/`seed save` 가 이 필드를 읽어 상태에 싣게. `*.orig` · `staff-name-map.json` 류(실명)는 만들지도 열지도 마라. 바꾼 고객 · 값 표를 보고에
2. **응답 필드**: 고객이 나오는 응답 전부에 `phoneticName` · `phone` · `vip` — **나오는 곳을 grep 으로 전부 세고** 표로 보고(board customers · reservations · 환자 상세 · 직원 홈 · 예약 상세 …)
3. **시술권 차감 시점**: 지금 어디서 시술권이 사용 처리되는지 먼저 찾아 보고하고, 단계 finish 로 옮긴다. `보유 n/m` 계산 근거도
4. **`POST /api/desk/memo`** + check-in 선택 `memo` — §5.1 그대로. 상담 종료 이벤트 뒤에도 덧붙인 줄 유지. KOS 주석(SPEC-001 §9 형식)
5. **§4 시술 후보 정정**(`service/bundles.py`)
6. 테스트: 각 항목 + 기존 전부 통과

## 3. 하지 말 것

- `cc/front/` · KOS 호출 · 범위 밖 1차 동작 변경
- 사용자 포트 · 프로세스(코디가 8610 · 3610 에 띄운 서버 포함 — 재시작은 코디가 한다)

## 8. 검증

```
cc/back 에서 uv run pytest · uv run ruff check . — 1회씩. 기능 폴더 밖 import 없는지. 실행 못 한 검증은 사유와 함께 pending
```

- 보고에: 바뀐 응답 JSON 예시(board 고객 1건 · reservation 1건 · memo 조작 1건) — front 워커에 넘긴다

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 코디 핸들이 세션 재연결로 바뀌었다(지금 `term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e`). preamble 과 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend(fix2) 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e \
  --text "[worker_done] backend(fix2) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e --text "[질문] backend(fix2): <질문>" --enter`
