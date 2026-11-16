# [backend] fix 코드 — WP-BE-1(채팅 · 알림 서버) → WP-BE-2(통역 서버)

너는 **day `backend` 워커**다. 앞 판(같은 터미널 · dev.env 작업)의 맥락이 있더라도 **아래 파일을 기준으로** 한다.

## 먼저 읽을 것

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/roles/day/backend/role.md` (+ 같은 폴더 문서)
- 레포 규칙: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix/AGENTS.md`
- **작업 계획(네 범위 · 파일 목록 · 시험 · 계약 표)**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/wp-plan.md` — §1 · §2 「WP-BE-1」 「WP-BE-2」 · §3 계약 표 · §5 통역 원천 가져오기 · §6 위험
- **계약의 SoT(스펙 — 미커밋 워크트리)**: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/20-spec/` — `spec-004-internal-chat.md`(그룹 이름 #22 · 푸시 받는 사람 · C-A20 · C-A21) · `spec-005-notifications.md`(`chat` 종류 · N-A13) · `spec-003-mobile-app.md` §3 「통역 — 앱 · 서버 계약」 · A-44 · A-45 · A-47 · I-1 ~ I-5 · `spec-000-data-model.md` · `40-architecture/deployment.md`
- 통역 근거: `…/work/fix/research-interpret-report.md` §3 · §4 · §5 · §7
- 스펙에 없는 것은 **발명하지 마라.** 계획과 스펙이 다르면 스펙이 맞다 — 다르다는 것을 보고에 적는다.

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` (`kknaksss/fix` · `origin/dev` 와 같은 자리 — #240 이 이미 dev 에 머지됨).
⚠ **mobile 워커가 같은 워크트리의 `app/` 에서 동시에 일한다.** `app/` 은 읽기만 · 건드리지 마라. `git stash` · `git checkout -- .` · `git clean` 금지.

## 할 것 — 차례로

### 1. WP-BE-1 채팅 · 알림 서버

`wp-plan.md` 「WP-BE-1」 그대로. 끝나면 **BE-2 로 넘어가기 전에** 코디에게 한 줄을 보낸다(앱 워커가 이 계약을 기다린다):

`orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[진행] backend: WP-BE-1 끝 — <시험 수치 한 줄>" --enter`

### 2. WP-BE-2 통역 서버

`wp-plan.md` 「WP-BE-2」 · §5 그대로.

- 원천은 interpret-pwa `origin/main` `17c26b5` — 로컬 canonical 은 뼈대 커밋뿐이니 `git -C /Users/kknaks/git/toy_pr2/interpret-pwa show origin/main:<path>` 로 읽는다. canonical 을 checkout · pull 하지 않는다.
- 기록기(`records`)는 가져오지 않는다. 쿼리 토큰 · Origin 칸을 두지 않는다. 오류 문구에 env 이름 · 받은 값 · 업체 이름을 싣지 않는다.
- 동시 세션 자리는 **어떤 경로로 끝나도 한 번만** 돌려놓는다 — A-44 의 반납 갈래를 전부 시험으로.
- **실물 Soniox(A-45)가 완료 조건이다.** 키는 로컬 `/Users/kknaks/git/toy_pr2/interpret-pwa/.env` 의 `SONIOX_API_KEY`(dev Key Vault 에 넣은 것과 같은 키)를 **프로세스 env 로만** 읽어 쓴다 — 화면 · 로그 · 리포트 · 레포에 값을 내지 않는다. 7개 언어 연결 · 한 언어 왕복 · 멈춤 35초 뒤 두 번째 발화. 호출은 이 확인에 필요한 만큼만(되풀이 금지).
- A-47(키 비운 환경의 `no_api_key` · 권한 없는 계정)은 로컬에서 `error.code` 로 확인한다.

## 범위 제약

- allowed_paths: `backend/` · `scripts/` · `deploy/`(주석 · 설정 칸만 — **값을 바꾸지 않는다**) · 루트 `pyproject.toml` · `uv.lock`(`opencc-python-reimplemented` 추가가 계획에 있다) · `docs/development/`(계획이 지정한 곳).
- 금지: `app/` · `.github/` · migration 추가(계획 = migration 없음 — 필요해 보이면 **멈추고 물어라**) · 배포 · 서버 접속 · Key Vault · Azure · APNs 실제 발송 · KOS 호출(데모 포함 — 이번 작업에 필요 없다).
- **사용자 로컬 스택을 건드리지 않는다**: 컨테이너 `day-local-*` · 포트 11040 · 11042 · 11043 · 그 DB · Redis 를 쓰지도 멈추지도 않는다. infra 시험이 필요하면 **다른 compose 프로젝트 이름 · 다른 포트**로 네 것만 따로 띄우고 끝나면 내린다(볼륨까지). 그게 안 되면 infra 시험은 사유와 함께 pending 으로 보고한다.
- 커밋 · push · PR 금지.

## 검증

- WP 마다: 네가 만들거나 고친 테스트 파일만 `cd backend && uv run pytest -q <파일들>` · `uv run ruff check <만진 파일>` — 각 1회, 통과하면 되풀이하지 않는다.
- 마지막에 한 번: `cd backend && uv run pytest -q -m "not infra"`(전체 회귀) · `test_import_boundaries` 포함 여부 확인 · 위 방식으로 infra 가 가능하면 `scripts/test.sh -q` 를 네 격리 스택으로.
- `uv run python -c "import opencc"` 류로 Python 3.13 에서 OpenCC 가 뜨는지(I-3) · 시드 적재 로그 `glossary seed loaded: version=…`(A-14).
- 깨진 시드 → 기동 실패 시험.

## 보고

리포트 2개(WP 마다 — 워커가 죽어도 남게 끝나는 대로 쓴다):
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/be-1-report.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/be-2-report.md`

각각: 변경 · 새 파일 목록 / 수용 항목 ↔ 시험 이름 표 / 계약 표(wp-plan §3)와 구현이 같은지 필드 단위 / 돌린 명령과 수치 / 실물 결과(A-45 · A-47 — 언어별 한 줄) / 스펙과 달라진 곳 · 물을 것 / pending.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 다르면 preamble 이 맞다.

전부 끝나면 **두 명령 모두**:

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_d8e9c610-96b4-482a-9972-365ca65c1084 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "WP 별 변경 파일 수 / 시험 수치 / 실물 결과 / 스펙과 다른 곳 / pending"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면 30분 넘게 혼자 헤매지 말고: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] backend: <질문>" --enter`
