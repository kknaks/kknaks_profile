# [backend] 전원 위하고 도메인 로그인 — 가짜 도메인 제거 + 「바로 로그인」 나열 도메인을 환경변수로

너는 **sc-ax `backend` 워커**다(같은 세션). 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `7b60932`). 남의 변경(.gitignore·.design-sync/·frontend/*)은 그대로 두고 손대지 마라.

## 1. SSOT
- 프로필 `reference/2026-09-04-SC-org_data/{build_dataset.py, README.md}` (최신 커밋 `02c10e8`)
- `backend/src/ax_workspace/bootstrap/seed.py:45` `DEMO_EMAIL_DOMAIN` · `entrypoints/http.py:489` `/api/auth/providers` · `platform/organization_access.py::demo_accounts` · `bootstrap/settings.py`(env 읽는 자리)

## 2. 배경 / 사용자 결정 (2026-09-07, 강한 지시)
가짜 도메인(`scax.example`) 계정을 **쓰지 않는다.** 로그인 계정 = 위하고 이메일이고 `member_credentials` 하나뿐이다. CSV 에 실제 주소가 15명(companysc.com 13 · wehago.com 2)뿐이므로, 나머지는 **같은 회사 도메인의 임시 주소**로 넣고 실제 주소가 오면 CSV 갱신·재생성으로 덮는다.

## 3. 계약
- `build_dataset.py`: `--test-login` 규칙 전부 **제거**. `logins` 는 165명 전원: 위하고메일이 있으면 그대로(대소문자 정규화만), 없으면 `<사번>@companysc.com`. 임시 주소 개수를 stderr 와 README 에 남긴다. 커밋 CSV 불변. 개인정보 인용 금지.
- ax-workspace(코드 변경 1곳, 최소): `DEMO_EMAIL_DOMAIN` 을 환경변수 `AX_DEMO_EMAIL_DOMAIN`(기본 `scax.example`) 로 읽게 한다 — `settings.py` 패턴을 따르고, `demo_accounts(domain)` 호출과 데모 시드(`seed.py` 의 계정 생성)가 같은 값을 쓰게 한다. production 프로파일에서 providers 가 등록되지 않는 기존 동작은 그대로(`tests/architecture` 로 확인). 계약 테스트 1개: env 를 바꾸면 그 도메인 계정이 나열된다.
- 로컬 실행: 코디가 API 를 `AX_DEMO_EMAIL_DOMAIN=companysc.com` 으로 재시작한다 — 너는 `Makefile` 을 고치지 말고, README(프로필) 에 실행법 한 줄만.
- 적재: `make reset-catalog` → 재생성 → `--dry-run` → `SCAX_DATASET_PASSWORD=scax-demo-1234 make dataset-import TARGET=~/scax-datasets/the-sc`.

## 5. allowed_paths
- `backend/src/ax_workspace/{bootstrap/seed.py, bootstrap/settings.py, entrypoints/http.py, platform/organization_access.py}` 와 관련 `backend/tests/` · 프로필 `reference/2026-09-04-SC-org_data/{build_dataset.py, README.md}` · `~/scax-datasets/the-sc/` · 로컬 DB
- **금지**: `frontend/` · `Makefile` · 남의 파일 · 커밋·push

## 6. 단계 / 8. 검증
1. 테스트 RED → env 도메인 구현 → `uv run pytest -q <만진 테스트> tests/architecture`. 2. 변환기 정리(규칙 제거·전원 로그인, 멱등). 3. reset-catalog → 재생성 → dry-run → import. 4. SQL: members 165 · member_credentials **165**(scax.example **0**, companysc.com 150+13, wehago.com 2) · units 29 · grants 169. 5. 코디가 API 재시작한 뒤가 아니라도 확인 가능하게, in-process TestClient 로 `AX_DEMO_EMAIL_DOMAIN=companysc.com` 일 때 `/api/auth/providers` 가 163개(companysc.com 만) 나열하는지 개수 보고. 6. 대표 1001 · 부서장 1106 · 팀장 1141 · 팀원 1107 로그인 200(이메일은 보고에 쓰지 말고 key 만) + 대표만 access/roles 200. 7. build_dataset.py 2회 diff 없음 · 워크트리 네 변경 = allowed 파일만.

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
