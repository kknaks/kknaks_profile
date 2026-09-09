# [backend] members 에 전화·생년월일 옵셔널 컬럼 — 스키마·계약·API 확장 후 SC 조직도 재적재

너는 **sc-ax `backend` 워커**다. 역할 문서는 이미 읽었다(같은 세션). 필요하면 다시:
`/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/roles/sc-ax/backend/`

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `922ed65`)
base 브랜치: `origin/main` → 최종 PR 대상 `main`

⚠ 워크트리에 **네 것이 아닌 변경**이 있다: `.gitignore` 수정, `.design-sync/`, `frontend/ds-entry.tsx` (다른 세션의 디자인 싱크). **건드리지 말고, 되돌리지도 말고, 보고에서 「무관」으로 분리**해라. frontend 워커 터미널이 같은 워크트리에 있으나 지금 idle 이다.

## 1. SSOT — 먼저 읽을 것

- 직전 태스크 산출물: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/reference/2026-09-04-SC-org_data/README.md`·`build_dataset.py` (프로필 레포 커밋 `929872f`). 여기서 확장한다.
- `backend/src/ax_workspace/platform/persistence.py` `members` 모델 · `modules/datasets/schema.py`(`members` 표·`SCHEMA_VERSION`) · `bootstrap/dataset_import.py::_import_members` · `entrypoints/http.py` 의 `MemberResponse` 와 `/api/organization/members*` · `modules/organization_access/` (권한 판정 — capability 이름은 `catalog.py`)
- `bootstrap/schema_sync.py` + `Makefile` `sync-demo-schema`(지우지 않고 열 추가) · `reset-demo`
- `docs/domain-model.md` 「조직·사람·권한」 — MEMBER 행에 새 컬럼을 적는다
- 스펙 근거: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/work/sc-design-system/ref-spec-main/spec-005-organization-people-access.md` §2 「결과 field 는 현재 Principal 의 권한에 맞게 제한한다」

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

SC 조직도 CSV 의 전화·생년월일을 담을 자리가 `members` 에 없어 직전 시드에서 뺐다. 사용자 결정: **옵셔널 컬럼 2개를 members 에 더하고, 계약·적재·API 까지 확장한 뒤 시드를 다시 만든다.** 값은 CSV 에 15명분만 있다 — 나머지는 NULL. 지어내지 않는다.

## 3. 계약 (사용자 결정 2026-09-07)

- `members.phone: str | None` · `members.birth_date: date | None` (nullable, 기본 NULL). 이름은 이 둘로.
- dataset `members` 표에 `phone`(required=False) · `birth_date`(required=False, kind="date") 열 추가, `SCHEMA_VERSION` +1. 기존 dataset 폴더(열 없음)도 계속 통과해야 한다(옵션 열).
- API: `MemberResponse` 에 두 필드 추가하되 **조직 관리 capability 가 있는 Principal 에게만 값을 채우고, 없으면 `null`**(필드 자체는 유지). capability 이름은 `catalog.py` 에서 조직 관리·인사에 해당하는 기존 것을 쓴다 — 새 capability 를 만들지 않는다. 어느 것을 골랐는지 보고.
- 로컬 DB 는 `make sync-demo-schema` 로 열만 추가(파괴 아님). 재적재는 import 가 기존 행을 skip 하므로 **`make reset-demo` 후 `SCAX_DATASET_PASSWORD=scax-demo-1234 make dataset-import TARGET=~/scax-datasets/the-sc`** 로 다시 넣는다(코디 허가 — 로컬 데모 DB). 순서: 코드 → sync → 변환기 확장 → dataset 재생성 → reset → import.
- `build_dataset.py`: `members.csv` 에 phone·birth_date 열을 CSV 의 전화·생년월일에서 채운다(형식은 원문 그대로 정규화 — 날짜는 ISO, 전화는 숫자·하이픈만). 빈 값은 빈 칸. README 갱신.
- 운영 스키마·Alembic 은 이번 범위 밖(별도 gate) — 코드 주석에 「로컬 sync 로만 적용됨, 운영 반영은 별도」 한 줄.

## 4. 먼저 읽을 핵심 파일

- `backend/src/ax_workspace/platform/persistence.py` `MemberRecord`(또는 해당 클래스) · `modules/datasets/schema.py:56-177` · `bootstrap/dataset_import.py:201-240` · `entrypoints/http.py:838-905`
- 기존 계약 테스트: `backend/tests/contract/test_dataset_contract.py` · `test_dataset_import.py` · `test_access_roles.py`(권한별 응답 제한 패턴)
- `backend/tests/unit/test_sync_demo_schema.py` — sync 가 새 열을 어떻게 다루는지

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/src/ax_workspace/{platform/persistence.py, modules/datasets/schema.py, bootstrap/dataset_import.py, entrypoints/http.py}` 와 관련 `backend/tests/` · `docs/domain-model.md`(MEMBER 행 1줄)
- 프로필 레포 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/reference/2026-09-04-SC-org_data/{build_dataset.py, README.md}` · `~/scax-datasets/the-sc/` · 로컬 DB
- **금지**: `frontend/` · `Makefile` · `docker-compose.yml` · `.gitignore`·`.design-sync/`·`frontend/ds-entry.tsx`(남의 것) · 커밋·push

## 6. 구현 단계

1. 계약 테스트 먼저 RED: dataset `members` 표에 두 열이 옵션으로 있고 없어도 통과 / API 가 권한 없는 Principal 에게 두 필드를 null 로 주고 있는 Principal 에게 값을 준다.
2. 모델·계약·적재·응답 구현. `docs/domain-model.md` 한 줄.
3. `make sync-demo-schema` → 열 2개 추가 확인(SQL `\d members`).
4. `build_dataset.py` 확장 → `~/scax-datasets/the-sc/` 재생성 → `--dry-run` 통과.
5. `make reset-demo` → import(비밀번호 env 포함) → SQL 카운트 이전과 동일(SC 29/165/169/22/10/3/15) + `phone`·`birth_date` non-null 각 15.
6. API 확인: SC 관리 권한 있는 계정(없으면 데모 관리자)으로 `/api/organization/members` 에 값이 보이고, 일반 구성원 계정으로는 null.

## 7. 범위 제약 — 하지 말 것

- 새 capability·role 만들지 않는다. 화면(`frontend/`) 안 고친다. Alembic 안 만든다.
- 남의 변경(.gitignore·.design-sync·ds-entry.tsx) 손대지 않는다. `git add`·commit 안 한다.
- CSV 에 없는 값을 채우지 않는다. 보고·로그·테스트 픽스처에 실제 전화·생년월일·이메일·이름을 쓰지 않는다(테스트는 가짜 값).

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> -m 'not integration' + uv run pytest -q tests/architecture. SQL: members 의 phone·birth_date non-null 각 15, SC 카운트 이전과 동일, member_credentials 15(+데모). API 두 Principal 비교 결과. build_dataset.py 2회 diff 없음. git status 에 네 변경 = 위 allowed 파일만(남의 것은 「무관」). 검증은 1회만
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 보고에 고른 capability 이름·변경 파일·SQL 결과·API 비교를 붙인다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_64a88609-f01f-4c9c-942e-e2f3a883dc4d --from term_9ad0847d-9bbf-4d91-aeac-1ba4b4122d36 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_64a88609-f01f-4c9c-942e-e2f3a883dc4d \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_64a88609-f01f-4c9c-942e-e2f3a883dc4d --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
