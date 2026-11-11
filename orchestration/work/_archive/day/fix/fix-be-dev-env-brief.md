# [backend] dev 서버 설정 — 앱 로그인(공개 주소) · 푸시(APNs) · 채팅 첨부(Blob)

너는 **day `backend` 워커**다. **너는 앞 판의 맥락이 없다** — 아래 「읽을 것」으로 시작한다.

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 레포 규칙: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix/AGENTS.md`
- 프로젝트 설정: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/config/projects/day.json` 의 `infra` · `apple`
- 배포 계약(읽기만): `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/40-architecture/deployment.md` · `mobile-deployment.md`
- 앱 쪽 앞 판 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-testflight-upload-report.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` (브랜치 `kknaksss/fix` · base `origin/dev` → PR `dev`).
⚠ 같은 워크트리에 mobile 워커의 미커밋 변경(`app/` — 아이콘 · `Info.plist` · `README.md`)이 있다. **`app/` 은 건드리지 마라.**

## 1. 배경

DAY Dev 앱(TestFlight · `day.medisolveai.dev` · release 빌드)이 dev 서버에 로그인하면 `environment_unavailable` 로 막힌다(사용자 실기기 2026-11-11).

원인(코디 확인): `deploy/config/dev.env` 의 `DAY_PUBLIC_API_BASE` 가 비어 있어 앱 로그인 응답에 `api_base_url` 이 안 실린다. release 빌드는 `environment` · `api_base_url` 둘 다 있어야 통과한다(`app/lib/state/session_controller.dart:269-289`). 웹은 이 칸을 쓰지 않아 지금까지 드러나지 않았다.

같은 파일의 채팅 · 푸시 칸도 전부 비어 있어, 로그인이 풀려도 기기 등록(400) · 푸시(`skipped_no_key`) · 채팅 첨부(409 `photo_disabled`)가 꺼져 있다. 사용자는 실기기에서 **알림 · 채팅**을 확인하려 한다. 사용자가 이 설정 작업을 승인했다(2026-11-11).

## 2. 먼저 읽을 핵심 파일

- `deploy/config/dev.env` — 넣을 자리(주석이 각 칸의 규칙을 말한다)
- `scripts/deploy/day_vm.py` — 일반 설정 검사 · 선택 비밀(`OPTIONAL_SECRETS` = `day-<env>-chat-blob-connection-string` · `day-<env>-apns-auth-key`) · 여러 줄 값 처리 · 금지 키
- `backend/common/config.py:140-170` — 각 env 의 뜻 · fail-closed 규칙
- `backend/day/services/apns.py` · `backend/day/services/chat_storage.py` · `backend/day/schemas/devices.py` — 값이 실제로 어떻게 읽히는지(키 형식 · 컨테이너 · topic)
- `backend/tests/deploy/test_day_vm.py` · `test_chat_env_contract.py` — 설정 계약 시험
- `.github/workflows/deploy-dev.yaml` — `dev` push 때 배포. Key Vault 값이 언제 · 누구 권한으로 읽히는지

## 3. 할 것

### A. `deploy/config/dev.env` (레포)

| 키 | 값 |
|---|---|
| `DAY_PUBLIC_API_BASE` | `https://day-dev.medisolveai.com` |
| `DAY_APNS_KEY_ID` | `~/.config/day/apple/credentials.local.json` 의 `apns.key_id` |
| `DAY_APNS_TEAM_ID` | 같은 파일의 `apns.team_id` |
| `DAY_APNS_ALLOWED_APP_IDS` | `day.medisolveai.dev` (dev 서버엔 개발 앱만 — 정식 번들을 넣지 않는다) |
| `DAY_CHAT_STORAGE` | `blob` — **C 가 될 때만** |
| `DAY_CHAT_BLOB_CONTAINER` | C 에서 정해진 컨테이너 이름 — **C 가 될 때만** |

- Key ID · Team ID 는 이 파일에 넣는다(파일이 받게 설계됐고 CENTURION_DAY 는 비공개 — 사용자 확인). 다만 **화면 · 리포트 · 로그에는 값을 내지 않는다**(리포트는 PUBLIC 레포에 간다). 파일에 쓰는 것은 스크립트로 읽어 넣는다.
- `DAY_DEMO_LOGIN_EMAILS` · `DAY_DEMO_API_BASE` 는 dev 에서 비워 둔다(주석 규칙). `prod.env` 는 건드리지 않는다.
- 주석이 「비워 둔다 · 후속」처럼 지금 상태와 달라지면 그 줄만 고친다.

### B. Key Vault — APNs 키

- 이름 규칙대로 `day-dev-apns-auth-key` 에 APNs 키(.p8 PEM 본문 · `credentials.local.json` 의 `apns.private_key_path` 파일)를 넣는다. Key Vault 이름 · 구독 등은 `~/.config/day/infra.json` 의 `azure` 에서 읽는다.
- 먼저 그 비밀이 이미 있는지 본다(값은 읽지 않는다 — 존재 · 갱신 시각만). 있으면 덮어쓰지 말고 보고한다.
- 키 내용은 **파일에서 곧바로** 넣는다(`--file` 같은 방식). 변수로 echo · 화면 출력 · 임시 사본 금지.
- 앱이 읽는 형식(여러 줄 PEM · `\n` 처리)이 `day_vm.py` · `apns.py` 와 맞는지 코드로 확인한다.
- `az` 로그인이 안 돼 있거나 권한이 없으면 **멈추고 보고**한다(로그인 · 역할 부여를 네가 하지 않는다).

### C. 채팅 첨부 Blob

- 먼저 조사한다: DAY 리소스 그룹에 채팅 첨부용 Storage 계정 · 컨테이너가 이미 있는지, `day-dev-chat-blob-connection-string` 이 Key Vault 에 있는지, `deployment.md` 가 저장소를 어떻게 정했는지.
- **이미 있으면**: 연결 문자열을 Key Vault 에 넣고(B 와 같은 규칙 · 출력 금지) `dev.env` 두 칸을 채운다.
- **없으면 만들지 않는다.** A 의 채팅 두 칸을 비워 둔 채 「무엇이 없고, 만들려면 무엇을 정해야 하는지(계정 이름 · 지역 · 공개 접근 · 수명 규칙 · 비용)」를 리포트 「정할 것」에 적는다. 리소스 생성은 사용자 승인이 따로 필요하다.

### D. 시험

- 위 변경으로 깨지는 설정 계약 시험이 있으면 계약에 맞게 고친다(빈 값을 단정하던 시험 등). 시험을 지우거나 느슨하게 만들지 않는다.
- 「dev 서버 + `DAY_PUBLIC_API_BASE` 있음 → 앱 로그인 응답에 `api_base_url` · `environment=dev`」를 보는 시험이 이미 있는지 확인하고, 없으면 리포트에 적는다(이번에 새로 짓지 않는다).

## 4. allowed_paths

- `deploy/config/dev.env`
- `backend/tests/deploy/` (D 에 필요한 만큼만)
- 레포 밖: Key Vault 비밀 2개(`day-dev-apns-auth-key` · `day-dev-chat-blob-connection-string`) 쓰기 · Azure 조회(읽기)
- 리포트 1개(§6)

## 5. 하지 말 것

- `backend/` 앱 코드 · `scripts/` · `.github/` · `app/` · `deploy/config/prod*` 수정 금지. 필요해 보이면 멈추고 물어라.
- **배포 · 서버 재시작 · ssh 로 서버 파일 수정 금지.** 배포는 `dev` 머지 때 워크플로가 한다. 서버 조회(ssh 읽기)는 꼭 필요할 때만.
- Azure 리소스 생성 · 삭제 · 역할 부여 · 네트워크 변경 금지. prod Key Vault 값 금지.
- 실제 APNs 발송 금지(실기기 확인은 배포 뒤 사용자와 한다).
- KOS 는 데모 테넌트만. 고객 값 · 키 · 토큰 · 연결 문자열 · Key ID · Team ID · IP · 리소스 ID 를 화면 · 리포트 · 로그에 내지 않는다.
- 사용자 포트(로컬 11040) · 프로세스 금지. 테스트 DB 는 로컬 compose 만. 커밋 · push · PR 금지.

## 6. 검증 · 보고

```
cd backend && uv run pytest -q tests/deploy            # 1회
cd backend && uv run ruff check <만진 파일>              # 1회
```

- `day_vm.py` 의 일반 설정 검사가 새 `dev.env` 를 통과하는지(스크립트가 제공하는 검사 경로로 · 서버 접속 없이).
- Key Vault: 두 비밀의 존재 · 갱신 시각만 재조회(값 조회 금지).
- `git status --short` — 네 변경과 mobile 의 `app/` 변경이 섞이지 않았는지.

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/be-dev-env-report.md`
(변경 파일 · A 표(값은 「설정됨」으로) · B · C 결과 · 시험 결과 · 배포 뒤 확인할 것 · 정할 것 · pending)

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 다르면 preamble 이 맞다. 두 곳에 다 보내지 마라.

끝나면 **두 명령 모두** 실행한다.

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_d8e9c610-96b4-482a-9972-365ca65c1084 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 / A·B·C 결과 / 시험 결과(수치) / 정할 것 / pending"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면 30분 넘게 혼자 헤매지 말고: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] backend: <질문>" --enter`
