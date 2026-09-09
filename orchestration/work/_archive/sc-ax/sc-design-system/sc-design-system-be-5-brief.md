# [backend] 「바로 로그인」 목록에 역할 4명 — 대표 · 국내사업부 부서장 · 인사총무팀 팀장 · 국내사업부 팀원

너는 **sc-ax `backend` 워커**다(같은 세션). ax-workspace 워크트리는 **읽기만**. 남의 변경은 그대로.

## 1. SSOT
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/reference/2026-09-04-SC-org_data/build_dataset.py`·`README.md` (프로필 최신 커밋)

## 2. 배경 / 사용자 결정 (2026-09-07)
로그인 화면의 「로컬 실행 전용 · 바로 로그인」 목록은 데모 도메인 계정만 나열한다. 사용자는 이 목록에서 **대표·부서장·팀장·팀원을 클릭해 들어가고 싶다.** 지금은 3명(1001·1141·1142)뿐이고, 국내사업부 부서장·팀원은 실제 위하고메일이 있어 규칙이 건너뛰는 바람에 목록에 없다. 로컬 테스트에서는 그 두 사람의 credential 을 **테스트 주소로 대체**한다(원문 CSV 불변, 로컬 dataset 에서만).

## 3. 계약
- `--test-login` 규칙이 **실제 위하고메일이 있는 사람도 고른다**(건너뛰지 않음). 고른 사람의 `logins.email` 은 `sc-<사번>@scax.example` 로 **대체**한다(한 사람에 credential 하나). 대체된 인원 수를 stderr 경고와 보고에 남긴다.
- 권장 규칙 4개: `executive` · `division-head:국내사업부`(부서장) · `team-lead:인사총무팀` · `member:국내사업부`(부서장 아닌 첫 사람). 부서장 규칙 이름은 positions 의 slot 에 맞춰 정하고 README 에 적는다.
- 고르지 않은 사람 중 실제 위하고메일이 있는 이들(국내사업부 13명)은 그대로 실제 주소로 로그인(목록엔 안 뜸).
- 적재: `make reset-catalog` → 재생성 → `--dry-run` → `SCAX_DATASET_PASSWORD=scax-demo-1234 make dataset-import TARGET=~/scax-datasets/the-sc`.

## 5. allowed_paths
- 프로필 `reference/2026-09-04-SC-org_data/{build_dataset.py, README.md}` · `~/scax-datasets/the-sc/` · 로컬 DB. **금지**: ax-workspace 수정 · 커밋·push · 개인정보 인용.

## 6. 단계 / 8. 검증
1. 규칙 동작 변경(멱등). 2. reset-catalog → 재생성 → dry-run → import. 3. SQL: members 165 · member_credentials **17**(실제 13 + 테스트 4) · units 29 · grants 169. 4. `GET /api/auth/providers` demo_accounts **4개** — key 와 역할(대표/부서장/팀장/팀원)을 표로(이메일·이름은 쓰지 않는다). 5. 네 계정 login 200 · 대표만 `GET /api/access/roles` 200. 6. build_dataset.py 2회 diff 없음 · 워크트리에 네 변경 0.

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
