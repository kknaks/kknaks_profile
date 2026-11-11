
# [backend] KOS 데모 지점 테스트 데이터 스크립트 — 30분 한 타임 · 국적별 1명 · 시술 대기까지

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

지금 이 워크트리에서 다른 워커는 일하지 않는다. 너는 `scripts/` 에 새 파일만 만든다.

## 1. SSOT — 먼저 읽을 것

- 이 브리프 §2 · §6 이 SoT(사용자 2026-11-09 지시). 스펙 문서는 없다 — 개발용 도구다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/reference/2026-11-09-cc-day/har/고객예약접수시술.har` ← KOS 웹에서 한 명을 접수 → 시술 대기까지 만든 HAR(데모 지점 · 내부 API). **요청 경로 · 본문 모양의 원천.** 여기 없는 경로 · 필드는 지어내지 마라.
- 레포 루트 `AGENTS.md`(외부 CRM 연동 규칙)

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- 해당 없음

## 2. 배경 / 무엇을 바꾸나

DAY 현황판을 시험할 때마다 사용자가 KOS 웹에서 고객을 손으로 만든다. 이걸 스크립트 한 번으로 바꾼다.

**사용자 지시(그대로)**: 30분 한 타임에, 국적별로 한 명씩, 한 타임에 10명 정도를 **시술 대기** 상태까지 만든다. 오더 메모도 넣고, 시술은 아무거나.

**넣는 곳은 KOS 데모 지점**(DAY DB 직접 X — 연동 병원은 KOS 가 원장이라 DAY 는 동기화로 읽어 온다).

**한 명의 흐름(사용자 · HAR 순서)**: 예약 생성 → 접수 → 기타 시술(작업) 생성 + 방 배정 → 시술 담기 · 수납(시술 뒤 수납) → 작업 생성 → 오더 메모 → 단계 시술 대기.
- **예약 생성은 HAR 에 없다**(첫 쓰기가 `recept`). 예약만 **공개 API** `POST /schedule/open/v2/commands/reserve`(reserveV2) 로 만든다(사용자 승인). 몸통은 KOS 공개 API 문서 https://developers.kos-solution.com/openapi.yaml 에서 확인.
- 나머지는 HAR 의 내부 API 순서를 따른다:
  `schedule/v1/commands/recept` → (`schedule/etcetera-tasks/v1/queries/get-etcetera-tasks`) `schedule/v1/commands/add-flow-tasks` → (`schedule/zone/room/v1/queries/get-rooms`) `schedule/flow/v1/commands/change-tasks-room` → `schedule/v1/commands/change-flow-step` → (`procedure-menu/products/v3/queries/get-products` · `product-options/v2/queries/search-product-option-summaries`) `purchase/v1/commands/initialize-purchase` → `add-pending-purchase-items` → `schedule/v1/commands/register-purchase` → `purchase/v1/commands/add-transaction` → `accept-purchase` → `schedule/v1/commands/add-flow-tasks` → `schedule/v1/commands/change-order-memo`.
  HAR 의 `change-flow-step`(04:21:25)이 어느 단계로 바꿨는지 · 마지막에 시술 대기가 되는 호출이 무엇인지는 **본문을 보고 확인**하라. HAR 에 시술 대기 전환이 없으면 DAY `writes.py` 가 쓰는 내부 `change-flow-step` 으로 `PROCEDURE_WAITING` 을 보낸다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음(화면 · API 계약 없음). 스크립트 사용법만 정한다:

```
set -a; . deploy/local.env; set +a
uv run python scripts/seed_demo_board.py [--slot HH:MM] [--date YYYY-MM-DD] [--count 10] [--dry-run]
```
- `--slot` 없으면 지금(KST) 다음 30분 칸. `--date` 없으면 오늘(KST). `--count` 기본 10(국적 수만큼 · 넘으면 국적 반복).
- 국적 기본 10: 한국 · 중국 · 일본 · 대만 · 홍콩 · 미국 · 태국 · 베트남 · 싱가포르 · 몽골 — KOS 국적 코드는 데모 지점 `meta/codes` 조회값으로 맞춘다(지어내지 않는다).
- 고객 이름은 `[TEST]` 를 붙인 가짜 값 · 전화 등 개인 값도 전부 가짜. 오더 메모 = 「테스트 오더 메모 n」. 시술 = 데모 지점 상품 · 옵션 조회 결과에서 아무거나(이름 지어내지 않음). 방 = 조회한 방 중 아무거나.
- 끝에 만든 사람마다 한 줄(국적 · KOS 방문 id 끝 4자리 · 단계) 출력. 이름 · 전화 출력 금지.

## 4. 먼저 읽을 핵심 파일

- `backend/day/emr/kos/client.py` — `KosClient`(open · internal 토큰 · `internal_headers` 브라우저 헤더 · `call`/`open`/`internal`). **이걸 써라 — 새 HTTP 클라이언트를 만들지 마라.** 내부 API 는 브라우저 UA · Origin · kos-client-uri 가 없으면 403
- `backend/day/emr/kos/writes.py` — 공개 `change-flow-step` 몸통 · KOS 단계 이름(`KOS_STEPS`)
- `scripts/seed_demo_connection.py` — 스크립트 모양의 본(env 에서만 읽기 · sys.path · 사용법 docstring)
- `deploy/local.env.example` — env 이름(`DAY_SEED_KOS_*` · `KOS_*_BASE`). 값은 `~/git/CENTURION_DAY/deploy/local.env`(사용자 정본 클론 · 읽기만)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/ (frontend 몫 — backend/day/routers/(api 제외) · templates/ · static/ · styles/ — 제외) 중 브리프가 지정한 곳`
- `pyproject.toml · uv.lock (의존성 추가가 브리프에 있을 때만)`
- `deploy/ · scripts/ (브리프가 지정할 때만)`

## 6. 구현 단계

1. HAR 를 읽어 위 순서의 각 쓰기 요청 본문 모양을 정리(필드 이름 · 앞 응답에서 넘겨받는 id). 개인 값은 보지도 옮기지도 마라.
2. **한 명만** 실제로 만든다(데모 지점). 각 단계 응답 2xx 확인 → 공개 조회(또는 내부 `get-reservation-group`)로 그 방문이 시술 대기 · 작업 · 방 · 오더 메모가 붙었는지 확인.
3. 한 명이 되면 `scripts/seed_demo_board.py` 로 묶고 10명(국적별) 반복. 한 명 실패 시 그 사람만 건너뛰고 끝에 실패 사유 출력(전체 중단 X).
4. 실제로 한 타임(10명) 한 번 돌려 결과 표를 보고에 붙인다.
5. 순수 로직(슬롯 계산 · 국적 순환 · 데모 지점 가드)만 테스트 `backend/tests/scripts/test_seed_demo_board.py`(또는 레포 관례 자리) — KOS 호출은 테스트에서 하지 않는다.

## 7. 범위 제약 — 하지 말 것

- **데모 지점에서만.** `DAY_SEED_KOS_TENANT_ID` 가 HAR 의 테넌트(`6a793cd92416d118817a09b1`)가 아니면 바로 종료한다. 명동점 키(ax-clinic-project `KOS_API_tenent`) 사용 금지
- `backend/day/` 앱 코드 · DAY DB · migration 손대지 않는다. 필요한 KOS 호출은 스크립트 안에서 `KosClient.internal`/`open` 으로
- 키 · 토큰 · 고객 값을 레포 · 로그 · 보고에 남기지 않는다. HAR 원문을 레포에 복사하지 않는다
- 사용자 포트 · 프로세스(`day-local` 등)를 건드리지 않는다
- 이미 있는 데모 지점 데이터를 고치거나 지우지 않는다 — 새로 만든 것만
- 커밋 · push · PR 금지

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만>(+ 실물: 데모 지점 한 타임 1회 실행 결과 표) · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
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
  --to term_a2d0aeb3-fd79-4513-a467-f30acd018743 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_a2d0aeb3-fd79-4513-a467-f30acd018743 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_a2d0aeb3-fd79-4513-a467-f30acd018743 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
