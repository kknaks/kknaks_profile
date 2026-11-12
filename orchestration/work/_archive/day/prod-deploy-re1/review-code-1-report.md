# 리뷰 리포트 — prod-deploy-re1 / code (2026-11-11)

대상: `CENTURION_DAY/prod-deploy-re1` 워크트리 미커밋 변경(base `origin/dev`) — `backend/day/register_connection.py`(새) ·
`backend/tests/day/test_register_connection.py`(새) · `backend/day/services/crm_connections.py` · `backend/day/public.py` ·
`backend/tests/deploy/test_chat_env_contract.py` · `docs/development/deployment.md` · (`deploy/config/prod.env` 는 이름만 확인 · 값 미출력).
근거: Delivery #243 v1 본문 + v2 request(A2b 거절) · DAY-SPEC-000 :31 · :189 · :205 · :238 · :1384(개정 ④ · OQ-01-2) · be-1 브리프 「코디 결정」.

## 판정: WARN

FAIL 0 · WARN 3 · 계약(migration · 모델 · HTTP API) 변경 0. 거절 = 쓰기 0 · 재실행 행 수 · 방 배정 보존 · 커밋 위치 · 컨테이너 실행 · 문서 절차 4 · 5 는 맞다.
WARN 은 모두 「비밀이 새는 가장자리」와 「스펙에 없는 데모 시드 동작 변화」다 — 첫 등록(빈 `day_prod`)을 막지는 않는다.

## 검증 (이 리뷰에서 직접 · 각 1회)

| 명령 | 결과 |
|---|---|
| `uv run pytest -q backend/tests/deploy backend/tests/day/test_register_connection.py -m "not infra"` | **111 passed**, 4 deselected(infra) |
| `uv run pytest -q backend/tests/architecture` | 30 passed |
| `uv run ruff check backend` · `ruff format --check`(만진 5 파일) | All checks passed · 5 files already formatted |
| `cd backend && env -i … python -c "import day.register_connection, day.public"` (이미지와 같은 cwd · 앱 env 없음) | import ok |
| `cd backend && env -i … python -m day.register_connection --stdin </dev/null` | 필수 이름 7개만 · exit 1 (DB 접속 전 종료 — `day.public` import 도 그 뒤) |
| `… --help` | exit 2 · 값 출력 없음 |
| `git merge-base --is-ancestor origin/prod origin/dev` · `git ls-tree origin/prod .github/workflows` | ancestor 맞음(ff 가능) · 워크플로 파일 없음(문서 4 의 사실과 같음) |

- infra 4개(실제 PostgreSQL)는 사용자 포트 · 프로세스 금지라 다시 돌리지 않았다 — be-1 리포트 격리 스택 수치(대상 19 passed · 전체 1181 passed)를 근거로 둔다. 코드를 읽어 같은 결론을 확인했다(아래 정확성).

## FAIL

없음.

## WARN

### W1. 표준입력 파싱 오류 메시지가 「이름 칸」을 그대로 찍는다 — 줄바꿈된 키 조각이 stderr 로 샌다
- `backend/day/register_connection.py:59-60` — `name` 은 `=` 앞 전부이고, `NAMES` 에 없으면 `모르는 이름 {name}` 으로 찍는다.
- 실측: 값 파일에 키가 두 줄로 잘려 둘째 줄이 `SECRETTAIL==`(base64 패딩) 이면 → `표준입력 2번째 줄: 모르는 이름 SECRETTAIL` (exit 1). `DAY_CONNECT_KOS_OPEN_API_KEY abc=…`(`=` 대신 공백) 도 `abc` 가 이름에 붙어 찍힌다.
- 근거: SPEC-000 :1384 「메시지에 비밀값 없음」 · Delivery A2 「출력 · 로그에 비밀값 없음」 · 코디 결정 「출력에 비밀 없음」.
- 「조용히 통과하는 자리」: `test_register_connection.py:128-139` 의 세 줄은 `_no_secret` 이 **전체 값** 일치만 보므로(`:66-68`) 조각 누출을 잡지 못한다(`"open-key-secret-x"` 는 `=` 가 없어 다른 분기로 감).
- 고칠 방향: 이름이 `DAY_CONNECT_` 로 시작하는 대문자 · `_` 모양일 때만 이름을 찍고, 아니면 `모르는 이름(표시 안 함)` + 줄 번호만. 시험에 `"SECRETTAIL=="` · `"DAY_CONNECT_KOS_OPEN_API_KEY abc=x"` 를 넣고 `"SECRETTAIL"` · `"abc"` 가 err 에 없음을 단언.

### W2. 데모 시드 동작이 바뀌었다 — 스펙 · Delivery 에 없는 변화(양방향 거절)
- `backend/day/services/crm_connections.py:127-128` 의 거절이 `ensure_demo_connection`(`:159-178`) · `seed_demo_kos_connection`(`public.py:81-107`) 에도 걸린다. 같은 브랜드 코드 · 병원 이름의 **운영** 연결을 만나면 이제 데모 시드가 `ConnectionKindConflict` 로 멈춘다(이전 = `is_demo=True` 로 덮기). `scripts/seed_demo_connection.py:45-49` 는 이 예외를 잡지 않아 traceback 으로 끝난다(메시지는 `hospital_id` 뿐 — 비밀 없음).
- 근거: SPEC-000 :1384 는 거절을 **운영 등록 진입점**의 규칙으로만 적고, 「데모 시드처럼 덮지 않는다」 — 즉 데모 시드는 덮는 쪽으로 서술돼 있다. Delivery A3 「데모 시드는 그대로」. 코디 결정(브리프 :60)도 「운영 진입점이 그대로 물려받지 않게」.
- 판단: 실해는 없다(오히려 실제 병원 접속값을 데모 키로 덮는 사고를 막는다 · 평상시 데모→데모 경로 그대로 · 기존 시험 통과). 그러나 스펙 문장과 다르므로 **코디가 둘 중 하나를 정한다**: (a) 이대로 두고 SPEC-000 :1384 에 「데모 시드도 같은 이름의 운영 연결은 덮지 않는다」 한 줄(스펙 PR 머지 전 같이) · (b) `ensure_demo_connection` 은 예전처럼 덮기. 권고는 (a).

### W3. DB 오류 traceback 에 평문 접속값이 실릴 수 있다
- `register_connection.py:103-111` 는 `ConnectionKindConflict` 만 잡고, 그 밖의 예외(유일 제약 · 연결 실패 · `ENCRYPTION_KEY` 문제)는 기본 traceback 으로 stderr 에 나간다. 엔진은 `hide_parameters` 없이 만든다(`backend/common/db/session.py:113-120`) — SQLAlchemy `DBAPIError` 문자열에는 `[parameters: …]` 가 붙는다.
- `config` 의 `open_api_key` · `system_email` · `system_password` 는 bind 단계에서 암호화되지만(`models/hospital.py:28` · `EncryptedJSONB`), `tenant_id` 는 평문 키이고 브랜드 코드 · 병원 이름도 평문이다. 브리프 §6-2 는 테넌트도 「찍지 않을 값」으로 든다(SPEC-000 :1384 「메시지에 비밀값 없음」 · 문서 :154 「테넌트 id 를 찍지 않는다」).
- 가능성: 낮다(빈 `day_prod` 첫 등록 · 손으로 1회 · 경합 없음). 그래도 문서가 「출력은 한 줄뿐」이라고 약속하므로 어긋난다.
- 고칠 방향: `run` 에서 `Exception` 을 잡아 `등록 실패: <예외 클래스 이름>` 만 찍고 exit 4(문서에 종료 코드 추가). 시험 1개(가짜 register 가 값이 든 예외를 던짐 → err 에 값 없음).

## 정확성 (PASS 항목 · 근거)

| 항목 | 판정 | 근거 |
|---|---|---|
| 거절 = 쓰기 0 | PASS | `crm_connections.py:115-128` — 브랜드 · 병원 · 연결을 **찾기만** 한 뒤 비교. 거절은 셋이 모두 있을 때만 생기므로 그 전 `add`/`flush` 가 없다. 브랜드 · 병원을 먼저 만들고 거절하는 길 없음. 세션 예외 → rollback(`common/db/session.py:134-138`). infra 시험 `:212-229` 양방향 · 행 수 · config 원본 비교 |
| 재실행 행 수 | PASS | 같은 브랜드 코드(`live_unique`) · 브랜드 안 병원 이름으로 찾음 · 연결 PK = hospital_id. infra `:180-199` |
| 방 배정 보존 | PASS | `:136-139` — 값이 비면 넣어 둔 값 유지(#239 ⑦). `public.py:65-66` 빈 값은 config 에 안 넣음. infra `:191,199` |
| `created` 값 | PASS | `:156` `connection is None` — 새로 넣은 분기에서 변수를 다시 쓰지 않으므로 맞다 |
| 커밋 위치 | PASS | `public.py:67-77` — `ensure_connection` 한 번 뒤 `commit` 1회(한 트랜잭션) |
| `is_demo` 로 동작을 가르지 않음 | PASS | 비교는 등록 경로의 거절뿐 — SPEC-000 :1384 가 명시한 규칙. 업데이트 분기는 `is_demo` 를 다시 쓰지 않음(같은 값만 통과) · 진입점 소스에 `is_demo` 이름 없음(`test_demo_flag` 통과) |
| 명령줄로 비밀 받지 않음 | PASS | `register_connection.py:88-90` `--stdin` 외 인자 exit 2 |
| 정상 출력에 값 없음 | PASS | `:112` 병원 id · 넣음/고침만. 빈 필수 = 이름만(`:96-99`) |
| `DAY_SEED_*` 재사용 안 함 · 가드 없음 | PASS | `:24-36` `DAY_CONNECT_*` · `APP_ENV`/`DB_SCHEMA` 분기 없음(코디 결정) |
| 컨테이너 실행 | PASS | 이미지 WORKDIR `/app/backend` · `PATH=/opt/venv/bin`(`deploy/Dockerfile`) · `backend/` 안 모듈 · `scripts/` 의존 없음 · 같은 cwd 로 import 확인. `docker exec` 는 compose `env_file`(`config/prod.env` + `/etc/day/prod/app.env`)의 `DATABASE_URL` · `ENCRYPTION_KEY` 를 그대로 받는다(`deploy/compose.yaml:21-27`) |
| 계약 | PASS | migration · 모델 · HTTP API 변경 0. `day.public` 은 함수 · 예외만 추가(기존 시그니처 그대로) |

## prod 설정 시험 (`test_chat_env_contract.py:83-106`)

PASS. Target Delta 2 의 여섯 조건 모두 단언: 허용 앱 = `day.medisolveai`(정확 일치) · `DAY_PUBLIC_API_BASE` = `https://day.medisolveai.com` · `DAY_DEMO_API_BASE` = dev 공개 주소(문자열 + dev.env 와 교차) · `DAY_CHAT_STORAGE=blob` · `DAY_BLOB_CONTAINER=prod` · APNs Key ID · Team ID 둘 다(모양은 `:76-80` 이 prod 도 돈다). 키 누락은 `KeyError` 로 크게 실패(조용히 통과 없음). 실패 시 pytest 가 보이는 값은 URL · 앱 id · 빈 문자열뿐 — 이메일 목록 값은 단언 비교에 들어가지 않는다(`strip(" ,") != ""` · 메시지 고정).
- 참고: `DAY_ADMIN_EMAILS`(W6 「채움」) · `DB_SCHEMA=day_prod` 는 A4 범위 밖이라 단언 없음 — 원하면 한 줄씩(값 미출력 방식).

## 문서 절차 4 · 5 (`docs/development/deployment.md:129-136`)

PASS(사실 일치).
- 4: `origin/prod` = 옛 commit `8e4fb4b5` · 워크플로 파일 없음 확인. `migrate-prod.yaml:34` `if: github.ref == 'refs/heads/prod'` + workflow_dispatch 는 선택 ref 에 파일이 있어야 하므로 먼저 ff push 가 맞다. `origin/prod` 가 `origin/dev` 의 조상이라 ff 가능 · `check_promotion`(`day-deploy.sh`)의 before 조상 검사도 통과. 그 push 의 deploy-prod 는 VM 의 head 확인에서 멈춤(`deploy-prod.yaml:1-3` 주석 · `remote deploy`).
- 5: 같은 SHA 는 다시 push 해도 새 이벤트가 없으므로 「멈춘 실행 Re-run」이 맞다.
- 참고: `migrate-prod.yaml:88` 요약이 「next: push the same commit to prod」라고 적는다 — 첫 배포에선 이 안내대로 하면 `Everything up-to-date` 로 아무 일도 안 일어난다. 문서 5 가 맞고 워크플로 문구는 이 Delivery 범위 밖(다음에 「또는 멈춘 deploy-prod Re-run」 한 마디).
- 참고: 문서 「운영 연결 등록」은 종료 1 · 3 만 적고 2(인자 거부)는 없다 — W3 고칠 때 같이.

## Delivery Acceptance

| # | 내용 | 판정 | 근거 |
|---|---|---|---|
| A1 | `python -m` → 브랜드 · 병원 · 연결(kos · is_demo=false · 암호화 · 방 배정) · 병원 id 출력 · 재실행 행 그대로 | 충족(코드 · infra 시험 · be-1 수치) | `register_connection.py:104,112` · infra `:180-199`. 로컬 DB 실제 2회 실행(verification.1)은 이 리뷰에서 안 함(DB 금지) |
| A2 | 빈 필수 → 0 아닌 종료 · 쓰기 0 · 메시지 · 출력 · 로그에 비밀 없음 | **부분** | 빈 필수 · 정상 출력은 충족. 파싱 오류(W1) · DB 오류 traceback(W3) 가장자리에 누출 길 |
| A2b | `is_demo` 다른 같은 이름 연결 → 거절 · 0 아닌 종료 · 쓰기 0 · 비밀 없는 메시지 | 충족 | `crm_connections.py:127-128` · 진입점 exit 3 · infra `:212-229` 양방향 · 시험 `:142-147` |
| A3 | 데모 시드 그대로 is_demo=true · 이미지 안 진입점 · import 경계 | 충족(+W2) | `ensure_demo_connection` demo=True · 기존 시험 통과 · architecture 30 passed. 단 운영 연결을 만나면 멈추는 새 동작(W2) |
| A4 | prod 시험 여섯 조건 · 코디 prod.env 로 통과 · 값 미출력 | 충족 | 위 절 · deploy 시험 통과 |
| A5 | not infra · test.sh · ruff · migration 0 · API 0 | 충족 | 이 리뷰 111/30 passed · ruff 통과 · be-1 test.sh 1181 passed |
| A6 | prod 컨테이너 1회 등록 · 첫 동기화 | 해당 없음(사용자 · 배포 뒤) | — |

## 직원이 실물에서 만날 자리

- dev 컨테이너에서 잘못 돌리면 실제 병원 값이 `day_dev` 에 들어간다(가드 없음 = 코디 결정). 문서 경고 :157-158 있음 — 실행 전 `docker exec … printenv DB_SCHEMA` 로 `day_prod` 확인을 한 줄 넣으면 실수가 줄어든다(값 아님).
- 롤백 계획(Delivery rollback.2 = `crm_connection.deleted_at`)으로 지운 연결에 같은 값으로 다시 등록하면 `deleted_at=None` 으로 **되살아난다**(`crm_connections.py:150` · 기존 동작). 출력은 「고침」. 지운 연결이 다른 데모 표시면 거절(exit 3) — `session.get` 이 지운 행도 보기 때문.
- 값 파일에 키가 줄바꿈으로 잘리면 W1 로 조각이 터미널에 찍힌다.

## 참고(기존 부채 · 이번 변경과 무관)

- 병원 「브랜드 안 이름」에 유일 제약이 없어 재실행 멱등은 사전 조회로만 지킨다(AGENTS.md 「백엔드 안전 기준」). 수동 1회라 실해는 낮다 — 기존 `ensure_demo_connection` 부터 같은 모양.
- `tests/architecture/test_demo_flag.py:17` 허용 주석이 「로컬 시드」만 적는다 — 이제 운영 등록 거절 비교도 그 파일에 있다(주석만).
- 브랜드가 있으면 `brand_name` 을 고치지 않는다(기존 동작 · be-1 리포트에 적힘).
