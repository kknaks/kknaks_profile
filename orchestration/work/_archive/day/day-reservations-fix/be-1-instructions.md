# [backend] 예약 현황판 F1 ~ F6 · 문진 6개월 · KOS 문진 읽기 — WP-1 (#300)

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/roles/day/backend/role.md`(+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`).

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservations-fix`(base `origin/dev` `65506f35` → PR `dev` · PR 은 코디)

⚠ 같은 워크트리에서 **frontend 워커**가 `backend/day/routers/`(api 제외) · `templates/` · `static/` · `styles/` 를, **mobile 워커**가 `app/` 을 병렬로 고친다 — 그 자리는 건드리지 마라. 계약은 Issue ① ~ ⑤ 그대로 내라(이름 바꾸면 둘이 깨진다).

## 1. SSOT — 먼저 읽을 것

- **Issue 본문(최종)** `gh issue view 300 -R MediSolveAIDev/CENTURION_DAY` ← 이번 WP 범위 · 완료 조건 · 공통 계약 ① ~ ⑤. **여기 없는 건 발명하지 마라.**
- SPEC(계약 원천 · PR mediness#971 · 미머지): `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservations-fix-spec/products/day/20-spec/spec-006-reservation-board.md`(개정 ⑯ · **Functional Rule 15 ⓐ ~ ⓙ = 배치의 유일한 정의**) · `spec-007-reservation-detail.md`(고침 8 · 규칙 2 · 7 · 9 · §3 KOS 문진 읽기) · `spec-000-data-model.md`(개정 ④) · `spec-002-procedure-board.md` · `spec-003-mobile-app.md`
- 결정 표: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/_RESUME.md` §2(2026-11-27 행 · 위가 아래를 덮음 · 취소선 = 뒤집힘)
- 근거: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/be-f6-debug-1-report.md`(F6 원인) · `be-kos-questionnaire-1-report.md`(KOS 문진 실물) · `review-delivery-1-report.md`(빠진 입구 grep) · `delivery-fix-1-report.md`

기대는 개념: 해당 없음.

## 공통 원칙
- KOS 는 **내부 API 만**(공개 open 새 호출 금지).
- 화면 문구는 SPEC 에 있는 것만(새로 지으면 안 됨 · 없으면 비워 두고 보고). 열린 OQ-D43 · D48 = 지금 글자 그대로.
- 고칠 곳은 Issue 목록이 아니라 **쓰는 곳 전부 grep** 으로 세고 시작해라(목록 밖에서 빠지는 일이 많다).
- 시크릿 · 토큰 · 고객 PII 출력 금지(id 앞 8자만). `~/.config/day/prod-*` 열지 마라 · prod DB · 로그 금지. KOS 는 데모 지점만 · 읽기만(실물 확인이 필요하면).

## 2. 할 것 — Issue #300 범위 · 완료 조건 전부
- F6 상세 모든 경로 origin(`public_origin` 하나 · 4곳 + grep 으로 더 찾기) + GET 라우트 실제 service 시험
- Rule 15 배치 값(`rows` · `cards` · `bands` · 웹 · 앱 같은 함수) · R71 동행 판정은 30분 그대로(함수 · 상수 분리)
- KOS 문진 읽기 별도 태스크(일정 회차 뒤 · 내부 legacy · mapper · `external_ref` = KOS 제출 id · 6개월 안 건너뜀 · 400 = 없음) · `questionnaire.expired` · 다시 보내기 대상 = 제출 행만
- 팝오버 요청 흐름(`display-targets` · `display-requests` · D44)
- migration 은 Issue 대로(필요할 때만 `0032` · head `20261126_0031` 이어짐 확인)

## 5. allowed_paths
- `backend/` 중 frontend 몫(`backend/day/routers/`(api 제외) · `templates/` · `static/` · `styles/`) 제외 · `backend/tests/` 의 BE 테스트
- 웹 라우터(`routers/reservation_detail.py` 등)의 **origin 넘기기 · 새 팝오버 라우트처럼 Issue 가 BE 몫으로 적은 줄**만은 고쳐도 된다 — 고친 줄을 보고에 적고 frontend 와 겹치면 먼저 물어라

## 7. 하지 말 것
SPEC 바꾸기 · 문구 짓기 · 공개 KOS · 커밋 · push · 사용자 포트/프로세스(`start.sh` 로 떠 있는 것) 건드리기.

## 8. 검증
```
cd backend && uv run pytest -q <만들거나 고친 테스트> · uv run ruff check <만진 파일> — 각 1회. 테스트 DB 는 로컬 compose. KOS 문진 읽기 실물 1회(데모 지점 · 읽기만 · 400/200 둘 다 확인 · 결과는 id 앞 8자). 실행 못 한 검증은 사유와 pending
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_99b025fc-f3ef-403e-8162-509c41545e2e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
