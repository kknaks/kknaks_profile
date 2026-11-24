# [backend] DAY 예약 현황 — Delivery #267(조회 · 권한) → #268(다른 날짜 최신화)

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

**frontend 워커가 같은 워크트리에서 병렬로 #269 화면을 만든다** — 너는 frontend 몫(`backend/day/routers/`(api 제외) · `templates/` · `static/` · `styles/`)을 건드리지 않는다. 단 #267 의 조회 라우트 등록이 `routers/` 에 필요하면 **라우터 함수 · view model 은 네가, 템플릿은 frontend 가** — 경계가 애매하면 [질문]. 커밋은 하지 않으니 서로의 미커밋 변경을 지우지 마라(stash · checkout · reset 금지).

## 1. SSOT — 먼저 읽을 것

**너는 앞 맥락이 없다.** 아래가 전부다.

- **Delivery Issue 본문**(계약의 SoT · 결과 계약 · Acceptance · 수정 후보 · 하지 않는 것): `gh issue view <번호> -R MediSolveAIDev/CENTURION_DAY` — 번호는 §2
- **계약 최종 문장**(폴링 구분 신호 · 최신화 task 입구 · view model 표 · 조각 `#reservation-main` 범위): `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery-3-report.md` — Issue 본문과 같아야 한다. 다르면 Issue 가 이긴다 · 다르다고 [질문]
- SPEC: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec/products/day/20-spec/spec-006-reservation-board.md` (DAY-SPEC-006 · stable · mediness PR #958 · 머지 전) — Issue 에 없는 세부는 여기서. **여기 없는 건 발명하지 마라**
- 사용자 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md` (R1 ~ R41)
- 레포 규칙: 작업 워크트리 루트 `AGENTS.md` — 계층 · 이름 · 테스트 규칙(repository 층 없음 · 묶음 조회 = `queries/` 등)

**기대는 개념**: 해당 없음

## 2. 배경 / 무엇을 바꾸나

DAY 웹에 데스크용 「예약 현황」 조회 화면을 새로 만든다. 너는 백엔드 둘을 **순서대로** 한다.

1. **#267** — `GET /reservations`(전체 · HX 조각 · 10초 폴링 — DB 만 · KOS 안 부름) · view model · 권한 키 `reservation`(모든 직무 기본값 행 — `board` 방식) · 오늘 아닌 날짜를 열거나 바꿀 때 최신화 task 를 넣기만(폴링은 안 넣음)
2. **#268** — 다른 날짜 최신화 중앙 작업: (병원, 날짜) 요청 → 그 날 창으로 일정 → KOS 키 보충 → 구매 · 시술권 · 카드(R26) · 같은 (병원, 날짜) 잠금(R40) · 조건 C1(완성 상태만 보임) · C2(오늘 회차 잠금에 조용히 건너뛰지 않음) · C3(구매도 그 날짜 것) · 오늘 10초 회차 회귀 없음

#268 은 지금 동기화 함수(`run_schedules` · `emr_kos_keys.apply_isolated` · `sync_sales_hospital`)의 「오늘」 전제를 건드린다 — 어디서 못 지키는지는 SPEC 사실 표(파일:줄)에 있다. 오늘 회차 동작은 바꾸지 않는다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

`delivery-3-report.md` 의 세 계약을 **문자 그대로**: ① 폴링 구분 신호 ② 최신화 task 입구(이름 · 인자 · 넣고 안 기다림 · 오늘은 안 넣음) ③ view model 표 · 조각 `#reservation-main` 범위. frontend 는 같은 표로 가짜 값 템플릿을 만든다 — 이름 · 모양을 바꾸면 [질문]으로 먼저.

## 4. 먼저 읽을 핵심 파일

- Issue #267 · #268 의 「수정 후보」 전부
- `backend/day/services/emr_sync.py` · `services/emr_kos_keys.py` · `services/emr_sale_sync.py` · `tasks/emr.py` — #268 (SPEC 사실 표 줄)
- `backend/day/routers/board.py` · `services/board.py` · `policies/permissions.py` · `services/default_permissions.py` · `menu.py` — 기존 화면 · 권한 방식의 본

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/ (frontend 몫 — backend/day/routers/(api 제외) · templates/ · static/ · styles/ — 제외) 중 브리프가 지정한 곳`
- `pyproject.toml · uv.lock (의존성 추가가 브리프에 있을 때만)`
- `deploy/ · scripts/ (브리프가 지정할 때만)`

## 6. 구현 단계

1. 작업 워크트리 · base 확인 · `AGENTS.md` · Issue #267 · #268 · `delivery-3-report.md` 를 읽는다
2. #267 구현 + 테스트(Issue Acceptance 그대로)
3. #268 구현 + 테스트(A1 ~ A5 — C1 · C2 · C3 · 동시 1회 · 오늘 회귀) — 실 PostgreSQL · Redis(로컬 compose)
4. §8 검증 — 단계마다 **네가 만든 · 고친 테스트만**
5. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/be-1-report.md`(Delivery 별 Acceptance 체크 · 바꾼 파일 · 테스트 수치 · 계약 준수 · 실물 e2e 못 한 것과 이유)
6. §9 완료 보고 — #267 이 끝나면 중간 보고(`orca terminal send` 로 「#267 끝 — frontend 와 맞출 것」 한 줄) 후 #268 로 이어 간다

## 7. 범위 제약 — 하지 말 것

- KOS 쓰기 · 새 테이블 · 칸 · migration(권한 기본값 행이 migration 으로만 가능하면 [질문])
- 화면 템플릿 · CSS · JS(frontend 몫)
- 오늘 10초 회차 동작 변경 · 주기 재최신화 · 화면 요청에서 KOS 호출(R39 · R40)
- 커밋 · push · PR · 사용자 포트 · 프로세스 · 공유 dev / prod DB

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
  --to term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d --from term_7299f4c4-4ecb-4bf6-a45b-f6f015677756 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
