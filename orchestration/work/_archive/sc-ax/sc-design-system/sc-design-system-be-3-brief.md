# [backend] SC 단독 시드 — 데모 회사 제거(reset-catalog) + 이메일 없는 구성원에 로컬 테스트 로그인

너는 **sc-ax `backend` 워커**다(같은 세션). 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `7b60932`).
⚠ 남의 변경(`.gitignore`·`.design-sync/`·`frontend/ds-entry.tsx`)은 그대로. **이번엔 ax-workspace 코드를 바꾸지 않는다.**

## 1. SSOT
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/reference/2026-09-04-SC-org_data/build_dataset.py`·`README.md` (프로필 커밋 `55303aa`)
- `Makefile` `reset-catalog`(카탈로그만, 예시 회사 없음) · `dataset-import` · `README.md` 「로그인과 세션」(데모 도메인 계정만 로그인 화면에 나열)
- `bootstrap/dataset_import.py::_import_logins` · `entrypoints/http_auth.py`(providers 목록이 어느 도메인을 나열하는지 확인)

## 2. 배경
권한 패널·역할·범위는 `organization.manage` 보유자에게만 열리는데, SC 로그인 15명은 전부 국내사업부(부서장 1·구성원 14)라 대표·팀장 계정이 없고, 데모 대표 `yuna` 의 권한은 데모 회사 범위라 SC 사람에겐 403 이다. 사용자 결정: **데모 회사를 빼고 SC 만 두며, 테스트를 위해 대표·부서장·팀장·팀원 누구로든 로그인되게 한다.**

## 3. 계약 (사용자 결정 2026-09-07)
- `build_dataset.py` 에 옵션 `--test-logins`(기본 off): 위하고메일이 없는 구성원에게 `sc-<key>@scax.example` 을 `logins` 에 넣는다. 위하고메일이 있는 15명은 실제 주소 그대로. **커밋된 CSV 는 수정하지 않는다.** README 에 「로컬 테스트 전용, 실제 주소가 오면 옵션 없이 재생성」 명시.
- 데모 도메인(`scax.example`)이 로그인 화면 목록에 나열되는지 `http_auth.py` 로 확인 — 다른 도메인이면 그 도메인을 쓴다(보고).
- 적재 순서: `make reset-catalog` → `--test-logins` 로 dataset 재생성 → `--dry-run` → `SCAX_DATASET_PASSWORD=scax-demo-1234 make dataset-import TARGET=~/scax-datasets/the-sc`.
- reset-catalog 가 예시 회사·데모 계정을 정말 안 만드는지 확인(members 에 4자리 key 외 0행). 만들면 **고치지 말고 보고**.

## 4. 핵심 파일
- `backend/src/ax_workspace/entrypoints/reset_demo.py`·`bootstrap/reset.py`·`bootstrap/seed.py` — reset-catalog 경로
- `backend/src/ax_workspace/entrypoints/http_auth.py` — providers 나열 규칙

## 5. allowed_paths
- 프로필 레포 `reference/2026-09-04-SC-org_data/{build_dataset.py, README.md}` · `~/scax-datasets/the-sc/` · 로컬 DB
- **금지**: ax-workspace 워크트리 전체(읽기만) · 커밋·push

## 6. 단계
1. `http_auth.py` 에서 나열 도메인 확인. 2. 옵션 구현(멱등, 2회 diff 없음). 3. reset-catalog → 재생성 → dry-run → import. 4. 검증 SQL: members 165(4자리 key 외 0) · member_credentials 165 · access_grants 169 · 데모 회사 units 0. 5. 로그인 검증: 대표이사 1명(executive grant 보유 key) · 부서장 1 · 팀장 1 · 팀원 1 — 각각 `POST /api/auth/login` 200 후 `GET /api/access/members/<G일본 팀장 key>` 의 상태코드(대표 200 · 나머지 403 기대) 와 `GET /api/access/roles` 상태코드를 표로. 이메일은 보고에 쓰지 말고 key 만. 6. `GET /api/auth/providers` 에 SC 테스트 계정이 나열되는지(개수만).

## 7. 하지 말 것
- ax-workspace 코드·계약 수정 금지. 실제 위하고메일 15건을 바꾸지 마라. 개인정보 인용 금지.

## 8. 검증
```
위 SQL 4개 + 로그인/권한 표(대표·부서장·팀장·팀원 × login/access-members/access-roles) + providers 개수 + build_dataset.py 2회 diff + git -C 워크트리 status 에 네 변경 0
```

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
