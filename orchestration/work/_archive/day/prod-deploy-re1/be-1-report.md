# prod-deploy-re1 backend 결과 보고

## 상태: done (커밋 · push 안 함 — 워크트리 변경만)

## 수행 — 파일 · 모듈

- `backend/day/services/crm_connections.py`
  - `:85` `ConnectionKindConflict(Exception)` — 병원 id 만 싣는다. 접속값은 메시지에 넣지 않는다.
  - `:97` `ensure_connection(..., demo: bool) -> (병원 id, 새로 넣었나)` — 데모 시드와 운영 등록이 같이 쓰는 함수.
    - 브랜드 · 병원 · 연결을 **먼저 찾기만** 한다. 찾은 연결의 `is_demo` 가 `demo` 와 다르면 `ConnectionKindConflict` 를 낸다. 이때 쓰기는 0이다(브랜드 · 병원 · 연결이 이미 다 있는 경우라서 그 전에 쓰는 것이 없다).
    - 다시 돌려도 행이 늘지 않고, 「방 배정」 id 는 그대로 남는다(#239 ⑦ — 기존 로직 그대로).
    - 고칠 때 `is_demo` 는 다시 쓰지 않는다(같은 값만 통과하기 때문).
  - `:159` `ensure_demo_connection` — `ensure_connection(demo=True)` 의 얇은 감싸개. 시그니처 · 돌려주는 값은 그대로다.
- `backend/day/public.py`
  - `:40` `register_kos_connection(*, demo, …) -> (UUID, bool)` 를 새로 두었다.
  - `:81` `seed_demo_kos_connection` 은 위 함수를 `demo=True` 로 부른다(시그니처 그대로).
  - `ConnectionKindConflict` 를 내보낸다(`__all__`).
- `backend/day/register_connection.py` (새 파일) — 운영 등록 진입점 `python -m day.register_connection [--stdin]`
  - env 접두는 **`DAY_CONNECT_*`** 다(`DAY_SEED_*` 재사용 안 함).
    - 필수 7개: `DAY_CONNECT_BRAND_CODE` · `DAY_CONNECT_BRAND_NAME` · `DAY_CONNECT_HOSPITAL_NAME` · `DAY_CONNECT_KOS_OPEN_API_KEY` · `DAY_CONNECT_KOS_TENANT_ID` · `DAY_CONNECT_KOS_SYSTEM_EMAIL` · `DAY_CONNECT_KOS_SYSTEM_PASSWORD`
    - 선택 1개: `DAY_CONNECT_KOS_ROOM_ASSIGN_ETC_TASK_ID`
  - 값은 env 또는 표준입력(`--stdin` · `이름=값` 줄)에서만 받는다. 둘 다 있으면 표준입력이 이긴다.
    - `#` 로 시작하는 줄 · 빈 줄 · `export ` 접두는 건너뛴다. 앞뒤가 같은 따옴표로 감싸져 있으면 벗긴다.
    - 모르는 이름이나 `=` 가 없는 줄은 종료 1로 멈춘다(줄 번호와 이름만 알리고 값은 찍지 않는다). 오타 때문에 값이 조용히 빠지지 않게 하려는 것이다.
  - `--stdin` 이외의 인자는 종료 2로 거부한다(명령줄로 비밀을 받지 않는다).
  - 필수 값이 비면 종료 1이고, stderr 에 빈 이름만 찍는다.
  - 데모 연결과 겹치면 종료 3이고, `hospital_id` 만 찍는다(쓰기 0).
  - 성공하면 stdout 에 `운영 연결 넣음|고침 hospital_id=<uuid>` 한 줄만 찍는다.
  - DB · 암호화 키는 앱 설정(`DATABASE_URL` · `DB_SCHEMA` · `ENCRYPTION_KEY`)을 그대로 쓴다. APP_ENV/DB_SCHEMA 가드는 두지 않았다(코디 결정).
  - 소스에 `is_demo` 라는 이름이 없어서 `tests/architecture/test_demo_flag.py` 를 통과한다(인자 이름은 `demo`).
- `backend/tests/day/test_register_connection.py` (새 파일)
  - DB 없는 시험 9개: 표준입력 · env 처리, 출력에 비밀 없음, `demo=False` 로 부름, 빈 필수 값, 인자 거부, 모르는 이름 3가지, 충돌 종료 3, 접두.
  - infra 시험 4개: 운영 → `is_demo=false` 이고 다시 돌려도 행 수 그대로 · 방 배정 보존 / 데모 → 지금과 같음 / 표시가 다르면 거절 · 쓰기 0(데모→운영, 운영→데모 둘 다).
- `backend/tests/deploy/test_chat_env_contract.py:83` — `test_prod_서버_채팅_설정은_아직_비움` 을 `test_prod_서버는_정식_앱만_받고_공개_주소_데모_넘김_파일_저장소가_있다` 로 바꿨다. 확인하는 것:
  - 허용 앱이 `day.medisolveai` 하나
  - Key ID · Team ID 가 둘 다 있음
  - 공개 주소가 `https://day.medisolveai.com`
  - 데모 넘김 주소가 `https://day-dev.medisolveai.com` 이고 dev.env 공개 주소와 같음
  - 데모 계정 목록이 비지 않음(값은 메시지에 없음)
  - `DAY_CHAT_STORAGE=blob`, 계정 주소 모양, 컨테이너 `prod`
- `docs/development/deployment.md`
  - 「첫 배포 절차」 4 · 5를 실물에 맞게 고쳤다.
    - 4: prod 브랜치가 이미 있으므로 ff push 로 워크플로를 먼저 올린다. 그 push 의 deploy-prod 는 멈춘다(정상). 그 뒤 migrate-prod 를 돌린다.
    - 5: 새 push 를 하지 않는다. 4에서 멈춘 deploy-prod 실행을 **Re-run** 한다(코디 추가 지시 · review-doc-2 N3).
  - 6으로 「운영 연결 등록」을 넣었고, 기존 6은 7이 됐다.
  - 새 절 「운영 연결 등록」(`:138`)을 추가했다. 컨테이너 안에서 실행하는 법, 값은 표준입력으로 넣는다는 것, 출력 · 종료 코드, 「prod 컨테이너인지 먼저 확인」 경고를 적었다.
- 손대지 않은 것: `scripts/seed_demo_connection.py`(공개 함수 시그니처가 같아서 그대로 둠) · `deploy/config/prod.env`(코디 미커밋 그대로).

## 진입점 실행 명령

```sh
docker exec -i <prod api 컨테이너> python -m day.register_connection --stdin < <값 파일(VM · 레포 밖)>
```

## 검증 — 명령과 수치

- `uv run pytest -q -m "not infra" <내 시험 + tests/deploy + tests/architecture>` → **141 passed**
- 격리 스택(`docker compose -p day-be243` · 포트 11142/11143 · scratchpad env · `day-local` 은 건드리지 않음 · 끝나고 `down -v`)으로 돌렸다.
  - `scripts/test.sh -q <test_register_connection · test_room_assign_setting · test_encryption_canary>` → **19 passed**
  - `scripts/test.sh -q`(전체) → **1181 passed**, 0 failed
- `uv run pytest -q backend/tests/deploy` → **102 passed** (prod.env 시험 포함)
- `uv run ruff check backend` → All checks passed. 만진 파일은 `ruff format --check` 도 통과했다.
- 진입점 스모크: env 를 비우고 `python -m day.register_connection --stdin </dev/null` → 이름 7개만 찍고 exit 1.

## 계약 대조

- migration · 모델 · 공개 API(HTTP) 변경 없음. `day.public` 에는 함수 · 예외만 추가했다(기존 시그니처 그대로).
- `is_demo` 로 동작을 가르는 코드는 없다. 등록할 때 표시값을 넣고, 같은지 비교만 한다(SPEC-000 :187).
- 비밀 · 실제 키 · 계정은 코드 · 시험 · 리포트에 없다. 시험 값은 `*-secret-x` 자리 값이다.

## 이슈 · 코디가 확인할 것

- **동작 변경(가장자리)**: 거절은 양방향이다. 데모 시드(`scripts/seed_demo_connection.py`)도 같은 이름의 **운영** 연결을 만나면 이제 덮지 않고 `ConnectionKindConflict` 로 멈춘다. 이전에는 `is_demo=True` 로 덮었다. 평상시 경로(데모 → 데모)는 그대로다.
- 브랜드가 이미 있으면 `brand_name` 은 고치지 않는다(기존 동작 그대로).
- 환경 가드가 없으므로 dev 컨테이너에서 잘못 돌리면 실제 병원 값이 `day_dev` 에 들어간다. 문서에 경고만 적어 두었다.

## 수정 1 (review-code-1 W1 · W3 · 2026-11-11)

- **W1** `backend/day/register_connection.py` (줄 40 116  참고)
  - 표준입력에 모르는 이름이 있을 때, 이름은 `DAY_CONNECT_[A-Z0-9_]+` 모양과 정확히 맞을 때만 찍는다.
  - 모양이 다르면 「모르는 이름(표시 안 함)」과 줄 번호만 찍는다.
  - 시험 추가(parametrize): `SECRETTAIL==` · `DAY_CONNECT_KOS_OPEN_API_KEY abc=x`
    - err 에 `SECRETTAIL` · `abc` · `DAY_SEED_BRAND_CODE` · `brand-x` 가 없다.
    - err 에 「1번째 줄」이 있다.
  - 시험 추가: 모양이 맞는 오타 이름은 이름을 찍는다.
- **W3** 같은 파일 `run`
  - `ConnectionKindConflict` 밖의 `Exception` 을 잡아 `등록 실패: <예외 클래스 이름>` 만 찍고 exit 4 로 끝낸다.
  - 시험 추가: 값이 든 `RuntimeError` 를 던진다 → err 는 정확히 `등록 실패: RuntimeError` 이고 비밀 값이 없다.
- 문서 `docs/development/deployment.md` 「운영 연결 등록」: 종료 코드 0 · 1 · 2 · 3 · 4 를 모두 적었다.
- W2(데모 시드 거절): 코디 결정 (a)대로 코드는 그대로 둔다.
- 검증
  - `uv run pytest -q -m "not infra" backend/tests/day/test_register_connection.py backend/tests/deploy backend/tests/architecture` → **145 passed**(tests/deploy 포함)
  - ruff check · format → 통과
  - infra 경로는 바꾸지 않아 다시 돌리지 않았다.
