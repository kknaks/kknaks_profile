# [backend] SC 조직도 시드 — CSV(169행) → ax-workspace dataset 폴더 → 로컬 적재

너는 **sc-ax `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/roles/sc-ax/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `922ed65`)
base 브랜치: `origin/main` → 최종 PR 대상 `main`

**이 태스크는 ax-workspace 코드를 바꾸지 않는다.** 산출물은 (1) 변환 스크립트 1개(프로필 레포), (2) dataset 폴더(Git 밖), (3) 로컬 DB 적재 결과다. 같은 워크트리에 frontend 워커 터미널이 있고 코디가 API 8001·프론트 5176 을 띄워 둔 상태다 — `backend/`·`frontend/` 파일을 만들거나 고치지 마라.

## 1. SSOT — 먼저 읽을 것

- **조사 리포트**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/work/sc-design-system/org-screen-survey-report.md` §「CSV → dataset 매핑표」·「미결」 — 열 단위 매핑과 예상 행수(units 29 · grades 10 · positions 3 · members 165 · memberships 169 · appointments 22 · jobs 0)가 여기 있다. 이 표가 출발점이고, 아래 §3 결정이 미결을 닫는다.
- **원본 CSV**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/reference/2026-09-04-SC-org_data/더에쓰씨_조직도_2026-09-02(검수2)_상세추가.csv` (169행). **개인정보 — 보고·로그·스크립트 주석에 이름·전화·메일·생년월일을 쓰지 마라.** 개수와 구조만.
- **dataset 계약**: `backend/src/ax_workspace/modules/datasets/schema.py`(표·열·enum·unique) · `validation.py`(검사 규칙) · `bootstrap/dataset_import.py`(적재 순서·implied membership 규칙) · `README.md` 「데이터 넣기」.
- **역할 키**: `backend/src/ax_workspace/modules/organization_access/catalog.py` 의 `ROLE_TEMPLATES` — `members.role_key`·`positions.role_key` 는 여기 있는 key 만 통과한다.
- **선행 판정 규칙(참고)**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-org/orchestration/work/_archive/sc-ax/sc-org/output/seed_sc_org.py` 의 `DEPT_SLUGS`·`TEAM_SLUGS`·직급 slug 표와 겸임 병합 조건은 재활용한다. **모델·적재 로직은 쓰지 않는다**(mediness 스키마).

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

조직도 화면을 v3 로 개편하려면 화면에 실제 사람이 있어야 한다. ax-workspace 는 데이터를 리포에 두지 않고 `make dataset-import TARGET=<폴더>` 로 Git 밖 폴더의 CSV 표를 검사 후 한 트랜잭션으로 적재한다. 이 태스크는 SC 조직도 CSV 를 그 폴더 형식으로 변환해 로컬 DB(`postgresql+psycopg://ax:ax@localhost:54329/ax_demo`, 이미 떠 있음)에 넣는다.

## 3. 계약 (사용자 결정 2026-09-07 — 이대로)

- **사번 = 임시 번호.** `members.key` 를 4자리 임시 사번으로 쓴다: 병합 후 사람 순서(CSV 첫 등장 순)로 `1001`부터. 스키마 변경 없음. 화면은 이 key 를 사번 자리에 보여 줄 것이다.
- **겸임자(같은 이름 + 비고 「겸임」, 팀 5곳 팀장 1명)의 주소속 = CSV 에서 먼저 나오는 행의 팀.** 나머지 4곳은 `memberships` kind=additional. 5곳 모두 `appointments` 팀장. sc-org 의 「메모 없는 행」 휴리스틱은 쓰지 않는다.
- **동명이인 2명(국내사업부 직속, 한쪽 메모 「동며이인」)은 별개 인물** — 각자 key. 이름이 같아도 비고 「겸임」이 없으면 병합하지 않는다.
- 조직: 회사 루트 1개(`company`, key `the-sc`) → 부서 10 (`division`) → 팀 18 (`team`). 「경영진」「기타」도 division. 팀이 빈 행은 부서 직속.
- 직급 10 → `grades`(CSV 등장 순 또는 서열 순 — 서열은 sc-org 의 slug 표 순서를 쓴다). 직책: 부서장·팀장·부팀장 → `positions` (부서장 = division/head, 팀장 = team/head, 부팀장 = team/deputy). **팀 없이 부서 단계에서 「팀장」인 행은 부서장 slot** 으로 넣고 보고에 개수를 남긴다. 대표이사는 `role_key` 만 대표 역할, 직책 행 없음.
- `role_key`: 대표이사 → 대표 역할 key, 직책 있는 사람 → 팀장 역할 key, 나머지 → 구성원 key (실제 key 문자열은 `ROLE_TEMPLATES` 에서).
- 고용형태: 정규직 → `regular`, 시간제 → `part_time`, 그 외 값은 보고. 전원 `employment_state=active`. 입사일 있는 15명만 `employed_from`.
- **미반입**: 전화·생년월일·지메일·위하고메일(`logins` 안 만듦)·메모·비고(병합 판정에만)·담당 프로젝트. `jobs`·`job_assignments`·`projects`·`project_assignments`·`logins` 는 헤더만 있는 빈 표.
- 예제 8표(`scenario_*`)는 만들지 않는다 — 조직만 넣는다.

## 4. 먼저 읽을 핵심 파일

- `backend/src/ax_workspace/modules/datasets/schema.py` 전체, `validation.py`(무엇이 걸리는지), `bootstrap/dataset_import.py:93-270`
- `backend/src/ax_workspace/entrypoints/dataset.py:188-250` — `import` 서브커맨드 옵션(`--name`·`--as-of`·`--dry-run`), 폴더가 없을 때 템플릿을 만드는 동작
- `Makefile` 의 `dataset-import`·`reset-demo`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/reference/2026-09-04-SC-org_data/build_dataset.py` (신규 — 변환 스크립트, 표준 라이브러리만) 와 같은 폴더의 `README.md`(신규 — 실행법·결정 요약, 개인정보 없이)
- `~/scax-datasets/the-sc/` (신규 — dataset 폴더, Git 밖)
- 로컬 DB `ax_demo` 쓰기 (적재)
- **금지**: ax-workspace 워크트리의 모든 파일(`backend/`·`frontend/`·`docs/`·`Makefile`). 프로필 레포의 다른 파일. 커밋·push.

## 6. 구현 단계

1. 계약·검사·적재 순서를 읽고, 조사 리포트 매핑표를 §3 결정으로 갱신한 **최종 매핑표**를 만든다(보고에 붙인다).
2. `make dataset-import TARGET=~/scax-datasets/the-sc` 를 한 번 돌려 **템플릿 폴더**를 만들게 한다(폴더 없을 때의 동작 — manifest·빈 표 헤더를 그대로 따른다).
3. `build_dataset.py` 작성: 입력 CSV 경로·출력 폴더를 인자로 받고, §3 규칙으로 표 6개를 채운다. 경고(팀 없는 직책·미지 고용형태·직급 표 밖 값 등)는 stderr 로. 멱등(다시 돌리면 같은 결과).
4. `make dataset-import TARGET=~/scax-datasets/the-sc DATASET_ARGS=--dry-run` → 검사 통과까지 고친다.
5. 실제 적재. reset-demo 의 예시 회사와 key 가 충돌하면 **`make reset-demo` 로 비우고 다시 넣어도 된다**(로컬 데모 DB, 오늘 만든 것 — 코디 허가). 그 경우 보고에 남겨라.
6. 확인: `curl -s http://127.0.0.1:8001/api/organization/tree` 에 `the-sc` 루트와 부서 10·팀 18 이 있는가, `members` 165 인가(SQL 로 카운트). 5176 조직 화면에서 트리·구성원이 보이는지 한 번 연다(로그인은 데모 계정 — SC 인원에겐 계정이 없다).

## 7. 범위 제약 — 하지 말 것

- ax-workspace 코드·계약 수정 금지. 계약이 CSV 를 못 담으면 **고치지 말고 보고**(예: 필요한 enum 값이 없다).
- 사람 수·소속 수를 맞추려고 데이터를 지어내지 마라. 원문에 없는 값(입사일·직무·사번 외)은 비운다.
- 개인정보를 스크립트 상수·보고·로그에 넣지 마라. 겸임자 주소속 판별도 **이름이 아니라 「비고=겸임 + 동일 이름 + CSV 순서」 규칙**으로 코드화한다.
- 커밋·push 금지 (변환 스크립트는 코디가 프로필 레포에 커밋한다).

## 8. 검증

```
(1) dry-run 통과 출력 (2) 적재 결과 JSON 의 표별 made/skipped 카운트 (3) SQL 카운트: organization_units 29 · members 165 · memberships 169 · appointments 22 · grades 10 · positions 3 (다르면 왜) (4) /api/organization/tree 응답에 the-sc 루트 (5) build_dataset.py 를 두 번 돌려 출력이 동일한가(diff) (6) git -C <ax-workspace 워크트리> status 빈 출력 — 여섯 개를 보고에 붙인다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 보고에 최종 매핑표 · 경고 목록(개수) · 결정이 걸린 행 개수(겸임 5·동명이인 2·부서 단계 팀장 N·팀 없는 인원 N)를 붙인다.

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
