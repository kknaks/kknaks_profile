
# [writer] 실제 유저 시드 — 코드 조사 + 사용자가 채울 시드 양식

너는 **strong-hajin `writer` 워커**다. **너는 앞 맥락이 하나도 없다** — 아래 「읽을 것」이 전부다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy/AGENTS.md`

작업 워크트리(문서 산출물): `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포`
코드 조사 대상(**read-only**): `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy` (= Strong_hajin `origin/main` 0a2a5a3)

이 워크트리는 코디네이터와 공유한다 — 아래 §5 의 파일 외에는 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포/para/projects/summer-star/strong-hajin/40-architecture/deploy/environments.md` ← 배포 현황. 「아직 배포할 수 없는 이유」 2번(PRODUCTION 로그인 부재)이 이 작업과 맞닿는다
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포/reference/2026-09-04-SC-org_data/README.md` + `build_dataset.py` ← **선례.** 회사 조직도 CSV → `make dataset-import` 로 넣은 경로. 이번 양식도 이 경로를 1순위로 검토한다
- 기대는 개념: 해당 없음

## 2. 배경 / 무엇을 바꾸나

배포 전에 목데이터(예시 회사 SCAX·데모 계정)를 빼고 **실제 유저**를 넣는다. 사용자는 **유저 정보만** 줄 것이다.
네 일은 두 가지다:
1. 코드가 지금 유저·조직을 어떤 경로로 넣는지 조사해 「실제 유저를 어떻게 넣을지」 리포트를 쓴다
2. 사용자가 채울 **시드 양식**을 `reference/2026-09-30-strong-hain-seed/` 에 만든다 (지금 빈 폴더)

코드는 고치지 않는다. 조사·양식만.

## 3. 계약

해당 없음 (코드 변경 없음). 단 양식은 **코드가 실제로 읽는 형식**(dataset 표의 열 이름·필수 여부·값 규칙)을 그대로 따라야 한다 — 추측한 열 금지, 전부 `파일:줄` 근거.

## 4. 먼저 읽을 핵심 파일 (전부 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy/backend/src/ax_workspace/` 아래)

- `entrypoints/dataset.py` — dataset import: 표 목록·열·검증·`--dry-run`·`SCAX_DATASET_PASSWORD`
- `bootstrap/seed.py` — `seed_catalog(demo_organization=...)`, `_seed_local_credentials`, `DEMO_PASSWORD`, `SEEDED_MEMBERS`
- `bootstrap/demo_work.py` · `bootstrap/reset.py` · `entrypoints/reset_demo.py` — 데모 업무·리셋 (운영 DB 에서 막히는지)
- `bootstrap/settings.py:120-140` — `developer_auth_enabled` · `local_login_enabled` · `demo_email_domain`
- `entrypoints/http.py:610-660` (`/api/auth/providers`) · `entrypoints/http_auth.py` — 로그인 경로와 PRODUCTION 분기
- `modules/organization_access/` (credentials·catalog·application) · `platform/persistence.py` 의 Member/Membership/Credential/AccessGrant 레코드
- `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy/Makefile` — `dataset-import` · `reset-catalog` · `reset-demo` 타겟
- 프론트 로그인 화면(데모 계정 바로가기) — `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy/frontend/src` 에서 `demo_accounts` grep

위는 출발점이다. **유저·조직·자격증명이 만들어지는 곳을 grep 으로 전부 세라** (`MemberRecord(` · `MemberCredentialRecord(` · `hash_password` · `SEEDED_MEMBERS` · `demo`). 목록 밖에서 나온 것도 리포트에 넣는다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포/orchestration/work/strong-hajin-deploy/research-seed-path.md` (리포트, 새로 만든다)
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포/reference/2026-09-30-strong-hain-seed/` 아래 새 파일 (양식 + README.md)
- 커밋·push 금지. 코드 워크트리는 **읽기만**(테스트·make 실행도 하지 않는다 — DB 를 건드리는 타겟이 섞여 있다)

## 6. 구현 단계

1. 위 파일 읽고 grep 전수조사
2. `research-seed-path.md` 작성 — 절:
   - §1 결론 한 문단: 실제 유저를 넣는 권장 경로(명령 순서 포함)
   - §2 현재 경로 지도: seed / reset-demo / reset-catalog / dataset import 각각 무엇을 만들고 무엇을 지우는지, 운영 DB 에서 돌 수 있는지 (`파일:줄`)
   - §3 유저 1명이 로그인해서 쓰려면 필요한 최소 레코드 (조직 단위·멤버십·역할/권한·자격증명) — 어떤 게 양식에서 받고 어떤 게 기본값/카탈로그에서 오는지
   - §4 목데이터 표면 전수: 예시 회사·데모 계정·데모 업무·`/api/auth/providers` demo_accounts·프론트 바로가기·`demo_email_domain` — 운영에서 새어 나오는 곳이 있는지
   - §5 PRODUCTION 로그인 공백: 지금 코드로 실제 유저가 운영에서 로그인할 수 있는지, 없으면 막힌 자리(`파일:줄`)와 선택지(판정은 하지 말고 나열)
   - §6 Open Questions — 비밀번호 전달 방식, 조직 구조를 양식에 받을지 기본값으로 둘지 등 **네가 정하지 못한 것 전부**
3. `reference/2026-09-30-strong-hain-seed/` 에 양식:
   - dataset import 가 읽는 형식이 맞으면 그 형식(CSV 등)의 **빈 표**. 사용자는 「유저 정보만」 채운다 — 유저 외 필요한 값(조직 단위·역할 등)은 양식 README 에 「코디가 채울 칸 / 기본값 제안」으로 분리한다
   - `README.md`: 열마다 이름·필수 여부·값 규칙·코드 근거(`파일:줄`), 채우는 법, 채운 뒤 넣는 명령(참고용 — 실행은 나중)
   - 예시 행은 `예시-삭제` 처럼 **누가 봐도 가짜인 자리표시**만. 실존 인물·도메인 발명 금지. 비밀번호 칸이 필요하면 평문을 받지 말지 README 에 OQ 로 남긴다

## 7. 범위 제약 — 하지 말 것

- 코드·Makefile·para 문서 수정 금지. make·DB 명령 실행 금지
- 로그인 방식·비밀번호 정책을 **결정하지 마라** — 선택지와 근거만
- 실존 개인정보를 문서에 적지 마라 (선례 README 규칙과 같다)

## 8. 검증

```
산출물은 브리프가 지정한 파일들뿐. 정하지 못한 것은 Open Questions 로 남기고 임의 결정 금지. 모든 결정에 근거 병기
```

- 양식의 열 하나하나가 코드의 읽는 자리(`파일:줄`)와 대응하는지 스스로 대조표를 리포트 끝에 붙인다
- `git -C /Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포 status` 로 §5 밖 변경이 없는지 확인

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_8d586fcb-a104-4f31-9f5f-fd3b659a1d24 --from term_6ce571a1-fc6f-41fc-9bf6-468fac93e99b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_8d586fcb-a104-4f31-9f5f-fd3b659a1d24 \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_8d586fcb-a104-4f31-9f5f-fd3b659a1d24 --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
