# [backend] 4단계 — 백필 스크립트를 레포에(별도 PR · dev)

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

너는 맥락이 없다 — 아래 파일이 전부다. 이 워크트리는 너 혼자 쓴다. base = origin/dev 최신(`945be39b` 이후 — #260 머지됨). **시작 전에 `git fetch origin dev && git log -1 origin/dev` 로 dev 가 더 나아갔는지 보고, 나아갔으면 rebase 한 뒤 시작해라**(사용자 규칙: 코드 작업 전 dev 최신).

## 1. SSOT — 먼저 읽을 것

- 참고 패치(이미 검수 5 · DEMO 3회 · dev 최신에 `git apply --check` 통과): `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/backfill-reference.patch`
- 그 설계 · 결과: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/be-3-report.md` · 발주서 `customer-erd-be-3-brief.md`(지킬 것 1~5 · 계약) · 검수 `review-code-5-report.md`
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/_RESUME.md` §2 — 백필은 수동 실행 스크립트 · KOS 1초 1회 · 내부 API 만 · 어제까지 · 표시 backfill · 운영 스케줄에 안 붙음. 사용자가 레포에 스크립트로 두기로 함(2026-11-19).

**기대는 개념** — 해당 없음.

## 2. 배경

#260(테이블 · 동기화)이 dev 에 머지 · 배포됐다(migration 0010 적용됨). 백필 코드는 그 PR 에서 뺐었다. 이제 같은 코드를 **별도 PR** 로 dev 에 올린다 — prod 에서도 같은 명령으로 돌리기 위해. 지금 dev 서버에서는 이 패치를 임시로 얹어 드라이런 중이다(코디).

## 3. 계약

패치 그대로. 바뀌는 것은 하나:
- 패치의 `0010` 수정(`visit (hospital_id, reserved_start_at) WHERE deleted_at IS NULL` 인덱스)은 **0010 이 이미 dev DB 에 적용**돼 넣을 수 없다 → **새 migration `0011`** 로 옮긴다(down_revision = 0010 · 기존 테이블 인덱스 추가 하나 · 운영 무중단 — 필요하면 `CREATE INDEX CONCURRENTLY` 를 이 레포 관례대로 판단하고 리포트에 이유). 0010 파일은 건드리지 마라. 모델의 `Index` 정의는 패치대로.

## 4. 먼저 읽을 핵심 파일

- `backend/migrations/versions/20261119_0010_sale_tables.py` · 기존 migration 의 인덱스 관례 · `backend/tests/migrations/`(HEAD 테스트 갱신).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/ (frontend 몫 — backend/day/routers/(api 제외) · templates/ · static/ · styles/ — 제외) 중 브리프가 지정한 곳`
- `pyproject.toml · uv.lock (의존성 추가가 브리프에 있을 때만)`
- `deploy/ · scripts/ (브리프가 지정할 때만)` — **이번엔 지정한다**: 백필 실행 진입점을 `scripts/` 관례(또는 `backend/day/…` 명령 모듈 — 관례를 보고 고른다)에 둔다

## 6. 구현 단계

1. `git fetch origin dev` → **새 브랜치 `kknaksss/customer-erd-backfill` 을 origin/dev 최신에서** 만든다(`git switch -c … origin/dev` · 워크트리의 미커밋 변경이 있으면 멈추고 물어라).
2. `git apply` 참고 패치 → 0010 변경분을 되돌리고 같은 인덱스를 새 `20261119_0011_visit_reserved_index.py`(이름은 관례대로)로.
3. 테스트: 패치의 백필 테스트 · migration HEAD · 왕복(0011 up/down) · alembic check · 전체 1회 · `check.sh --pure`.
4. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/be-4-report.md` — 바꾼 점(0011) · 수치 · dev/prod 실행 방법(be-3 §5 그대로 확인).

## 7. 범위 제약

- 패치 밖 기능 추가 · 0010 수정 · 운영 스케줄 연결 · 서버 접속 · 커밋 · push · PR 금지(코디가 한다).

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
  --to term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --from term_554e6a04-c9e4-4dca-a57b-f58be57e562a \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
