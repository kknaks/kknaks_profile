
# [backend] 앱 차트 · 사진 /api JSON 짝 6 — Delivery #281

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

**같은 코드 워크트리를 다른 워커와 나눠 쓴다** — backend 는 `backend/` · `deploy/` 만, mobile 은 `app/` 만. 상대 영역은 건드리지 마라. git stash · checkout · reset 금지.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/delivery-1-report.md` §「BE ↔ APP 계약 전문」 C0 ~ C3 ← **두 워커가 같은 계약을 본다. 이대로 만든다.** 이름 제안과 달라져야 하면 멈추고 코디에게 먼저 알린다(§9 (2) 질문)
- Delivery Issue: MediSolveAIDev/CENTURION_DAY#281(backend) · #282(mobile) — `gh issue view <N> -R MediSolveAIDev/CENTURION_DAY` (읽기만 · 댓글 · 라벨 · 승인 건드리지 마라)
- SPEC(원천 · 읽기만): `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec/products/day/20-spec/spec-002-procedure-board.md`(개정 ㉚ · §3 차트 · 사진 JSON 짝 · 규칙 23 · 31 · 39) · `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec/products/day/20-spec/spec-003-mobile-app.md`(개정 ㉑ · U-23 · A-51 ~ A-60 · OQ 기본값)
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/_RESUME.md` §2(D1 ~ D15 · D6′)
- 조사: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/research-1-report.md`(근거 파일:줄 @`55e60aa4`)

**기대는 개념**: 해당 없음

## 2. 배경 / 무엇을 바꾸나

직원 앱 차트를 웹과 같은 기능으로 올린다(SPEC-003 ㉑). 웹 차트 저장 · 사진 다섯 경로는 HTML 조각 라우트뿐이고 사진 GET 둘은 쿠키 전용이라, 앱(Bearer)이 부를 **JSON 짝**을 `/api` 에 만든다. 서비스 · 규칙 · 오류 코드는 웹과 같다 — 새 업무 규칙 없음 · migration 없음 · 웹 경로 동작 그대로.

## 3. 계약

위 §1 의 C0 ~ C3 그대로.

## 4. 먼저 읽을 핵심 파일

코드 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1`(`kknaksss/day-app-re1` · base origin/dev `55e60aa4`):
- `backend/day/routers/api/board.py`(:149-161 차트 GET — 같은 파일에 짝을 둔다) · `backend/day/routers/api/` 의 공용 오류 · 인증 · 권한 의존
- `backend/day/routers/board.py`(웹 차트 저장 · 사진 다섯 라우트 — 같은 서비스를 어떻게 부르는지)
- `backend/day/services/board_chart*.py` · 사진 서비스(`visit_photos` · `visit_photo_import`) · `backend/day/dtos/board_charts.py` · `backend/day/policies/board_chart_rules.py`
- `deploy/` 의 Caddy 설정(사진 경로만 100MiB — 웹 사진 경로가 이미 그렇게 되어 있는 자리)
- 기존 테스트(`backend/tests/` 의 차트 · 사진 · api 테스트) — 모양을 따른다

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/ (frontend 몫 — backend/day/routers/(api 제외) · templates/ · static/ · styles/ — 제외) 중 브리프가 지정한 곳`
- `pyproject.toml · uv.lock (의존성 추가가 브리프에 있을 때만)`
- `deploy/ · scripts/ (브리프가 지정할 때만)`

## 6. 구현 단계

1. 계약 C2 탭 저장 · C3 ① ~ ⑤ 를 `/api` 에 만든다 — 라우터는 얇게, 서비스는 웹과 같은 것을 부른다(복사 금지). 요청 DTO extra=forbid · null 규칙(C2) 그대로
2. 오류 = /api 공용 `{detail, code, field}`(+ `details`) · 409 `chart_conflict` 의 `details.conflicts` · PhotoError → 공용 모양(OQ-100 기본값)
3. 권한: 보기 = `board` view · 쓰기 = `board` edit · `is_admin` 전부(C0)
4. Caddy: `/api/visits/*/photos` 본문 100MiB(웹 사진 경로와 같은 방식) — 다른 경로 상한 그대로
5. 옛 `POST /api/tasks/{task_id}/chart` 가 남아 있지 않은지 확인만
6. 테스트: 새 경로 계약 테스트(성공 · 각 오류 코드 · 권한 · Bearer · 쿠키로는?) + 웹 경로 회귀 — KOS 는 기존 테스트처럼 가짜
7. 이름 제안(OQ-99 · OQ-100)에서 달라진 것이 있으면 리포트 맨 위에 「계약 차이」로 적는다
8. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/be-1-report.md`(변경 파일 · 경로 표(메서드 · 경로 · 권한 · 응답 · 오류) · 테스트 수치 · 계약 차이 · 코디가 실물 확인할 순서)

## 7. 범위 제약 — 하지 말 것

- KOS 실물 호출 · 로컬 스택 띄우기 · `deploy/*.env` 값 · 사용자 포트 · 프로세스(실물 e2e 는 코디가 한다)
- 웹 경로 · 템플릿 · static 수정 · migration · 새 업무 규칙
- `app/` 건드리기 · 커밋 · push · PR · Issue 라벨 / 댓글

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **(코디 추가 · 2026-11-25)** 이번 발주는 orca Run(`worker-start`)으로 나간다. **dispatch preamble 에 적힌 `worker_done` 명령(Task · Dispatch ID · `--outcome` · `--report-path`)이 아래 (1)보다 우선**이다. (2) 직접 주입은 그대로 해도 된다.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_414d6113-407d-486b-ab54-10a4a6b455cb --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_414d6113-407d-486b-ab54-10a4a6b455cb \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_414d6113-407d-486b-ab54-10a4a6b455cb --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
