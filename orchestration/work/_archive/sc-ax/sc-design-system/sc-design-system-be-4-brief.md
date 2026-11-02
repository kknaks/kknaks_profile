# [backend] 테스트 로그인 최소화 — 150개 → 3개 (대표 1 · 인사총무팀 팀장 1 · 팀원 1)

너는 **sc-ax `backend` 워커**다(같은 세션). 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` — **읽기만**, 코드 변경 없음. 남의 변경(.gitignore·.design-sync/·frontend/*)은 그대로.

## 1. SSOT
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/reference/2026-09-04-SC-org_data/build_dataset.py`·`README.md` (프로필 커밋 `130d4c1`)

## 2. 배경 / 사용자 결정 (2026-09-07)
직전 `--test-logins` 는 이메일 없는 150명 전원에게 테스트 주소를 만들었다. 사용자: **역할별 1명씩, 국내사업부·경영관리부만.** 국내사업부는 부서장 1 + 팀원 14 가 실제 위하고메일이라 이미 로그인된다(팀 없음). 경영관리부는 부서장이 없고 인사총무팀·재무회계팀에 팀장이 1명씩이다. 따라서 테스트 주소는 **3개**만:
- 대표이사 1명 (CSV 첫 등장 대표이사)
- 인사총무팀 팀장 1명
- 인사총무팀 팀원 1명 (CSV 첫 등장, 팀장 아닌 사람)

## 3. 계약
- `--test-logins` 를 **반복 가능한 규칙 인자**로 바꾼다: `--test-login executive` · `--test-login team-lead:인사총무팀` · `--test-login member:인사총무팀`. 각 규칙은 CSV 순서로 **첫 1명**에게만 `sc-<사번>@scax.example` 을 만든다(이미 위하고메일이 있으면 건너뛰고 다음 사람). 규칙 없이 `--test-logins` 만 주는 옛 동작은 제거한다.
- 실제 위하고메일 15건 불변, 커밋 CSV 불변. README 갱신(권장 명령 = 위 3개 규칙).
- 적재: `make reset-catalog` → 재생성 → `--dry-run` → `SCAX_DATASET_PASSWORD=scax-demo-1234 make dataset-import TARGET=~/scax-datasets/the-sc`.

## 5. allowed_paths
- 프로필 `reference/2026-09-04-SC-org_data/{build_dataset.py, README.md}` · `~/scax-datasets/the-sc/` · 로컬 DB. **금지**: ax-workspace 수정 · 커밋·push · 개인정보 인용.

## 6. 단계 / 8. 검증
1. 옵션 구현(멱등). 2. reset-catalog → 재생성 → dry-run → import. 3. SQL: members 165 · member_credentials **18**(실제 15 + 테스트 3) · units 29 · grants 169. 4. `GET /api/auth/providers` demo_accounts **3개**, 각 key 와 역할(대표 / 팀장 / 팀원)을 표로 — 이메일은 보고에 쓰지 말고 key 만. 5. 세 계정 login 200 + 대표만 `GET /api/access/roles` 200, 팀장·팀원 403. 6. build_dataset.py 2회 diff 없음 · 워크트리에 네 변경 0.

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
