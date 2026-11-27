# [frontend] SPEC-008 예약 요청 스레드 — WP-3 화면(오른쪽 목록 · 상세 창 1 · 2 · 3열 · 웹 알림 갈래)

너는 **day `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/roles/day/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation3`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **backend 워커가 같은 워크트리에서 동시에** models · migrations · services · `routers/api/` · `routers/reservation_request_actions.py`(POST 동작) · emr · tests(web 제외)를 만든다 — 건드리지 마라. **너는 앞 맥락이 없다.**

## 1. SSOT — 먼저 읽을 것

- **Delivery Issue #297**(승인됨 · `delivery-plan:approved`) — `gh issue view 297 --repo MediSolveAIDev/CENTURION_DAY`(Target Delta · Acceptance A1 ~ A7 · Non-Goals)
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/delivery-1-report.md` ← **WP-0 ~ WP-3 표 · BE ↔ FE 계약(조각 경로 · 오류 · SSE · 버튼 규칙 · 알림). 둘 사이 계약은 이것**
- SPEC-008 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation3-spec/products/day/20-spec/spec-008-reservation-request.md`(PR #968 · 정본) + 같은 폴더 SPEC-006 ⑭ · 005 · 007 고침 6 · 000 ③(개정 머리의 「계획」 문구는 이번 구현 대상이라는 뜻)
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/reference/2026-11-26-reservation-request/reservation-request-decisions.md`(RQ1 ~ RQ44)
- 시안 v15 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/design/20261126_예약현황_시연_v15.html`(생김새 · 문구 정본 · base64 빼고 grep) · 스크린샷 같은 폴더 `v15-*.png`
- KOS 실물 근거 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/_archive/day/day-reservation2/be-probe-1 ~ 4-report.md`
- 코드 레포 `AGENTS.md`(이 워크트리 루트) · SPEC-007 구현(예약 등록 · 쓰기 큐 · SSE — 이미 dev 에 있음)

**질문하지 말고 기준으로 정해라**: SPEC-008 에 있으면 그대로 · KOS 값 = KOS 를 따른다 · 화면 = 시안 v15 · 글자 = SPEC-008 §2 「임시 글자 목록」(없는 글자는 비움) · 데이터 없는 칸 = 빈 값. 이 기준으로도 안 정해지는 것만 코디에게. **사용자 질문으로 열린 것**(OQ-Q04 문구 · Q05 · Q08 · Q12 · Q15 · Q20)은 SPEC 기본값대로 짜고 막지 마라.

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

예약 현황(SPEC-006) 오른쪽 「예약 요청」 칸은 지금 제목만 있다. 이걸 시안 v15 대로 목록 + 상세 창(1열 고객 · 예약 정보 · 버튼 / 2열 예약 현황 표 · 시간 머리 칩 / 3열 스레드 · 입력부)으로 만든다. 웹 알림을 누르면 그 스레드가 열린다.

## 3. 계약

`delivery-1-report.md` 「BE ↔ FE 계약」 그대로. **GET 조각 라우트**(`GET /reservations/requests` · `/reservations/requests/{id}` · `…/{id}/day?date=&pick=`)는 **네가** `routers/reservation_requests.py` 에 만든다. 그 조각이 부를 읽기 서비스 · POST 동작 · SSE 신호 `reservation_request` 는 backend 몫 — 아직 없으면 **계약 모양대로 가짜(테스트 픽스처)로 먼저 그리고**, backend 보고가 오면 코디가 이어 붙이라고 지시한다. 버튼 보이기는 서버가 준 상태 그대로(U-5 판단을 화면에서 다시 하지 마라).

## 4. 먼저 읽을 핵심 파일

시안 v15(예약 요청 목록 · `rq` 창 · 2열 표 · 3열 스레드 · 칩 · 버튼 줄 · 배지) · `backend/day/templates/` 예약 현황(`reservations*.html` · `partials/reservations_*`) · SPEC-007 예약 상세 모달 템플릿 · `static/day.js`(예약 현황 SSE · :4403 웹 알림 · `NOTIFY_KIND` · onclick) · `styles/`(medikit · 손 CSS 금지) · `routers/reservations.py`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/day/routers/reservation_requests.py`(새) · `routers/reservations.py`(오른쪽 칸 · `?request=&date=` 열기만) · `backend/day/templates/` · `backend/day/static/` · `backend/day/styles/`
- `backend/tests/day/web/` 의 화면 테스트

## 6. 구현 단계

1. 시안 v15 요소 전수 → SPEC-008 「넣음 / 뺌 / 바뀜」 표와 대조(시연 장치 · 투어 · 시연 버튼 뺌)
2. 오른쪽 목록 조각(빨간 점 · 빈 상태 글자) · 상세 창 틀(1160 × 700 · 1열 고정 높이 · 한 줄 말줄임 · 「없음」)
3. 1열(이름 머리 · 고객 정보 7줄 · 구분선 · 「예약 정보」 + 제목 배지(RQ43) · 버튼 줄(U-5 · 높이 유지 · [다시 시도] · [접음])) · 예약 메모 입력칸
4. 2열 예약 현황 표만 · 시간 머리 눌러 칩(여러 개 · 다른 날 ‹ ›) · 3열 버전 카드 · 댓글(`message` · `change_request` 칩 · 대체됨 · 철회 · `reservation_applied`) · 입력부(글 · 변경 요청) · 끝난 스레드 입력 막기(RQ37)
5. SSE `reservation_request` · `write_confirmed` · `kos_failed` 로 목록 · 열린 창 다시 받기(입력 중 글 · 메모 · 칩 유지) · `day.js` 웹 알림 갈래(`reservation_request` → `/reservations?request=&date=`) · 그 쿼리로 창 열기 · 공용 실패 토스트의 다시 시도가 스레드 행이면 스레드 열기
6. §8 검증

## 7. 범위 제약 — 하지 말 것

- 글자 짓기 금지(SPEC-008 §2 임시 목록 · 없으면 비움) · 인라인 스크립트 · 손 CSS 금지 · 새 색 금지(시안 색만)
- backend 파일 · 앱 · 웹 예약 등록 화면 동작 변경 · 커밋 · push · 사용자 포트 · 로컬 스택

## 8. 검증

```
uv run pytest -q <네가 만든 화면 테스트만>(TestClient 로 전체 페이지 · HX 조각 렌더 확인) — 1회. CSS 를 다시 빌드했다면 빌드 명령 1회. 인라인 스크립트 0 · 손 CSS 0(grep). 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_5c196973-a9ec-4982-81c2-655361f18aec --from term_94d78d74-6d0b-46bd-a2b2-b0b8c984bdd4 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5c196973-a9ec-4982-81c2-655361f18aec \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5c196973-a9ec-4982-81c2-655361f18aec --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
