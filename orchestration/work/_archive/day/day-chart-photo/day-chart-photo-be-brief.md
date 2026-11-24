
# [backend] DAY 차트 탭 저장 · C17 충돌 (WP ①)

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

**frontend 워커가 같은 워크트리에서 병렬로 WP ③(화면)을 만든다** — 서로의 미커밋 변경을 지우지 마라(stash · checkout · reset 금지). 커밋하지 않는다.

## 1. SSOT — 먼저 읽을 것

**너는 앞 맥락이 없다.** 아래가 전부다. Delivery Issue 는 발행하지 않았다(사용자 「PR 은 나중에 머지 · 바로 구현」) — 아래 문서가 Issue 대신이다.

- **WP · 계약 K1 ~ K5 · 공통 e2e**: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/delivery-1-report.md` 「WP 나누기」 · 「BE ↔ FE 계약」 ← 두 워커가 같은 글자로 맞춘다. **계약의 SoT**
- **결과 계약 · Acceptance · 수정 후보 · 하지 않는 것**: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/delivery/request-be-chart.json` · `request-be-photo.json` · `request-fe.json`(Issue 본문이 될 뻔한 것)
- **SPEC**: `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ㉘(U-14 · U-16 · 규칙 31 · 39 · API · 매트릭스 · KOS 사진 표) · `spec-001-login-session.md` 개정 ⑫(U-3) — 커밋 `a896cda0` · mediness PR #960(머지 전). 여기 없는 건 발명하지 마라
- 사용자 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md`(C1 ~ C17)
- 레포 규칙: 워크트리 루트 `AGENTS.md`

**기대는 개념**: 해당 없음

## 2. 배경 / 무엇을 바꾸나

차트 모달 자동 저장(줄 단위 `POST /board/tasks/{id}/chart`)을 **탭 단위 명시적 저장**으로 바꾼다. 이번 판 너의 범위는 **WP ① 만**이다(사진 WP ② 는 사용자 확인 대기 — 하지 마라).

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

delivery-1-report 의 **K1(차트 열기 `base`) · K2(탭 저장 요청) · K3(탭 저장 응답 200/409 · 조각 값) · K5(옛 경로 삭제 — 라우트 · 서비스 쪽)**. 조각 템플릿(`partials/board_chart_tab.html`)은 frontend 가 만든다 — 너는 view model(넘기는 값 이름)을 K3 대로 맞춘다.

## 4. 먼저 읽을 핵심 파일

- `backend/day/services/board_charts.py` · `services/board_chart_writes.py` · `policies/board_chart_rules.py` · `services/board_tasks.py`(:272 · :307 `_change_doctor_rows`) · `emr/kos/`(`fetch_visit_tasks` · mapper) · outbox `_queue` · `routers/board.py`(차트 라우트) · `routers/api/board.py:267`(옛 JSON 경로)
- 테스트: `backend/tests/day/` 의 차트 저장 테스트(옛 줄 저장 — 바꾸거나 지운다)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/ (frontend 몫 — backend/day/routers/(api 제외) · templates/ · static/ · styles/ — 제외) 중 아래`
- `pyproject.toml · uv.lock (의존성 추가가 브리프에 있을 때만)`
- `deploy/ · scripts/ (브리프가 지정할 때만)`

- 이번 지정: `backend/day/services/` · `policies/` · `queries/` · `emr/` · `dtos/` · `backend/tests/day/` · **`backend/day/routers/board.py` 의 차트 라우트 함수(view model · 경로 등록)와 `routers/api/board.py` 옛 차트 경로 삭제** — 템플릿 · static 은 frontend 몫

## 6. 구현 단계

1. K2 요청 파싱 · 검사 순서 400 → 404 → (transaction 밖) KOS 읽기 1회(시스템 계정 · 보낸 줄만) → 충돌 판정(`baseLogId` · `base` vs KOS 지금 값 · 정규화 규칙 SPEC 대로) → 담당자 → 저장
2. C17: 하나라도 걸리면 저장 0(이력 · outbox · event 0) · 409 `chart_conflict` · 걸린 줄 = KOS 글 + 줄바꿈 + 요청 글 · 담당자 KOS 값 · 새 `base`/`baseLogId` · 안 걸린 보낸 줄 = 요청 그대로 · 안 보낸 줄 = DAY 값. KOS 읽기 실패 = DAY 사본만으로 판정 · 저장 진행. 길이 검사는 하지 않는다(OQ-90 ⓒ 기본값)
3. 저장 = 방문 잠금 · transaction 1 · 바뀐 줄마다 이력 · `visit.chart_save` 1행 + outbox intent 전부 그 event 에 · 원장 바뀐 줄은 규칙 27 그대로(`task.doctor_change` 줄마다) · 시술 전 의사차트(결정 (가)) 그대로
4. K1 열기 값 `base` 추가 · K5 옛 경로(`POST /board/tasks/{id}/chart` · `/api/tasks/{id}/chart` · 서비스) 삭제
5. 테스트: A1 ~ A5(응답 모양 · C17 판정 · KOS 읽기 1회 transaction 밖 · event/outbox · 옛 경로 없음) — KOS 는 가짜 클라이언트

## 7. 범위 제약 — 하지 말 것

- 사진(WP ②) · 템플릿 · JS · CSS · migration · 앱(`app/`) · 권한 규칙 변경 · SPEC 에 없는 동작 · KOS 실물 쓰기(실물 e2e 는 코디가 모아서 한다)

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
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
  --to term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 --from term_cfd99c77-dafd-41c1-91a3-0ad1e4c6c1f3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
