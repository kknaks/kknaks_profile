
# [backend] prod 첫 배포 — 운영 연결 등록 진입점 · prod 설정 시험

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ `deploy/config/prod.env` 는 코디가 채운 **미커밋 변경**이다 — 값을 바꾸지 마라(시험이 이 값을 읽는다).

## 1. SSOT — 먼저 읽을 것

- Delivery Issue: CENTURION_DAY **#243** (`gh issue view 243 -R MediSolveAIDev/CENTURION_DAY`) — Target Delta · Acceptance 가 범위다. v1 승인 전 · 스펙 머지 뒤 v2 로 재결속 예정(범위 같음)
- 문서 리뷰: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/review-doc-1-report.md` (W2 · 열린 질문 1 · 참고 마지막 줄)
- 스펙(개정본 · 미머지): `/Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec/products/day/20-spec/spec-000-data-model.md` OQ-01-2 · `is_demo` · `/Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec/products/day/40-architecture/deployment.md`
- planner 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/delivery-report.md`

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

DAY prod 를 처음 올린다. 남은 코드 두 건.

1. **운영 연결 등록** — `crm_connection` 행을 만드는 길이 데모 시드 하나뿐이고 `is_demo=True` 고정이다. 운영 병원 연결을 `is_demo=false` 로 넣는 길을 만든다. **prod api 컨테이너 안에서 돌아야 한다** — 이미지에는 `backend/` 만 들어간다(`deploy/Dockerfile`). 그래서 진입점은 `backend` 안 모듈(`python -m …`)이어야 한다.
2. **prod 설정 시험** — `backend/tests/deploy/test_chat_env_contract.py:83` 은 prod 채팅 · APNs 6칸이 「비어 있어야」 통과한다(3차 임시 잠금). prod 값이 들어갔으니 확인 내용을 바꾼다.

## 3. 계약

해당 없음 — 공개 API · DB 스키마 · migration 변경 없음.

## 4. 먼저 읽을 핵심 파일

- `backend/day/services/crm_connections.py` — `seed_demo_kos_connection`(:90 ~ :140 · `is_demo=True` 두 곳) · `set_room_assign_id`
- `backend/day/public.py:48` — 시드 공개 함수
- `scripts/seed_demo_connection.py` — REQUIRED · OPTIONAL env 이름 · 값 검사
- `scripts/set_room_assign_etc_task.py`
- `deploy/Dockerfile` — COPY 범위
- `backend/tests/deploy/test_chat_env_contract.py:28 · :83 · :89 ~`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/day/services/crm_connections.py` · `backend/day/public.py`
- 새 진입점 모듈: `backend/day/` 아래 한 곳(이름은 네가 정하되 기존 관례를 따른다)
- `scripts/seed_demo_connection.py`(공통 함수로 바꿀 때만)
- `backend/tests/` 아래 이 작업 시험
- `docs/development/deployment.md`(운영 연결 등록 사용법 몇 줄)

## 6. 구현 단계

1. `seed_demo_kos_connection` 을 「데모 여부」를 받는 공통 함수로 바꾼다(기본 = 지금 동작 그대로 데모). 같은 값으로 다시 돌려도 행이 늘지 않는 성질 · 방 배정 id 보존(#239 ⑦)을 그대로 둔다.
2. 운영 등록 진입점: 값(브랜드 코드 · 브랜드 이름 · 병원 이름 · open 키 · 테넌트 id · 시스템 이메일 · 시스템 비번 · 방 배정 id(선택))을 **env 또는 표준입력에서만** 읽는다. 비밀은 명령줄 인자로 받지 않는다. 필수 값이 비면 이름만 말하고 멈춘다. 결과로 병원 id 와 「운영 연결 넣음/고침」만 출력하고 **값 · 키 · 테넌트 id 를 출력하지 않는다**. `is_demo=false`. DB 접속 · 암호화 키는 앱과 같은 설정(`DATABASE_URL` · `DB_SCHEMA` · `ENCRYPTION_KEY`)을 쓴다 — prod api 컨테이너 안에서 `docker exec … python -m <모듈>` 로 돌릴 수 있어야 한다.
3. 시험: 운영으로 넣으면 `is_demo=false` · 데모로 넣으면 지금과 같음 · 두 번 돌려도 행 수 그대로 · 출력에 비밀값 없음.
4. `test_chat_env_contract.py:83` 을 prod 값 확인으로 바꾼다 — dev 시험(:89) 모양을 따라: 허용 앱 = 정식 앱 `day.medisolveai` 하나 · Key ID 와 Team ID 함께 · 공개 주소 = `https://day.medisolveai.com` · 데모 넘김 주소 = dev 공개 주소(`https://day-dev.medisolveai.com`) · 데모 계정 목록이 비지 않음 · `DAY_CHAT_STORAGE=blob` · 계정 주소 모양 · 컨테이너 `prod`. 실제 이메일 · 계정 이름을 시험 메시지에 찍지 마라.
5. `docs/development/deployment.md` 에 운영 연결 등록 사용법(컨테이너 안 실행 · 값은 표준입력/env)을 몇 줄.

### 코디 결정(리뷰 뒤 · 이대로)

- 같은 브랜드 코드 · 병원 이름의 연결이 이미 있는데 `is_demo` 가 다르면 **거절** — 0 아닌 종료 · 쓰기 0 · 비밀값 없는 메시지. 기존 `ensure_demo_connection`(`crm_connections.py:131-138`)의 「찾으면 덮기」를 운영 진입점이 그대로 물려받지 않게 한다. 시험으로 박는다.
- env 접두는 `DAY_SEED_*` 를 재사용하지 않는다(이름은 네가 정하고 리포트에 적는다). 비밀(open 키 · 시스템 비번)은 **표준입력**으로 받는 길을 둔다(`docker exec -i`).
- APP_ENV/DB_SCHEMA 로 막는 가드는 두지 않는다(사용자 「환경별 가드 금지」).
- `docs/development/deployment.md:129-131` 의 「`prod` 브랜치가 없으면」 분기를 실물로 고친다 — prod 브랜치는 이미 있음(옛 commit · 워크플로 파일 없음) → 먼저 fast-forward push 로 워크플로를 올리고(그 push 의 deploy-prod 는 DB head 아님으로 멈춤 = 정상) 그 뒤 migrate-prod.

## 7. 범위 제약 — 하지 말 것

- migration · 모델 · 공개 API 변경 금지. `is_demo` 로 동작을 가르는 코드 추가 금지(SPEC-000 :187 — 표시일 뿐).
- prod · dev 서버 · DB · Key Vault 접속 금지. 실제 키 · 계정을 코드 · 시험 · 리포트에 넣지 마라.
- `deploy/config/*.env` 값 변경 금지.
- 사용자 포트 · 프로세스(로컬 11040 · `day-local`) 건드리지 마라. DB 시험은 격리 스택(`scripts/test.sh`)으로.

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- `uv run pytest -q backend/tests/deploy` 전체도 1회(prod.env 시험 포함 — 0 실패).
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/be-1-report.md` (변경 파일:줄 · 진입점 실행 명령 · 시험 수치)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_e62e850f-aae8-4092-a945-6f9406c2af07 --from term_662db7ba-7727-4b8a-b65a-fde2f6119683 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
