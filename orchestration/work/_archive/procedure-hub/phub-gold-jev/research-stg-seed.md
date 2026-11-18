# research — stg 반입 준비(일회성 적재 · 레포 데이터 폴더)

- 2026-11-18 · researcher(read-only · opus) · 브리프 `stg-seed-research-brief.md`
- 근거 기준: 허브 작업 워크트리 `$H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev` HEAD `fdc155b`(미커밋 변경 0) · 원 레포 `origin/stg`=`a3cba75` · `origin/release/v1.2.0`=`3750e4c` · `origin/prod`=`184e47e`(`git ls-remote` 로 원격과 같음을 오늘 확인 — 로컬 ref 가 최신)
- 데이터 `$SM=orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model` · 원장 `orchestration/work/phub-recommend/bronze/phub-ledger`
- stg 서버 · DB · Azure 에 접속하지 않았다. 내부 주소 · 접속 값은 적지 않는다(이름 · 자리만).

## 0. 머리 요약

1. **alembic 체인은 맞다.** `origin/stg` 머리 = `b202610300001`(release/v1.2.0 와 같은 두 파일). 우리 `b202611170001` 의 down = `b202610300001` · `b202611170002` → `b202611170001`. stg 에만 있는 revision 0 · 갈림 0. stg 와 release/v1.2.0 의 트리 차이는 문서 1개(`docs/guides/prod-db-rename.md`)뿐.
2. **새 표는 배포 때 저절로 생긴다.** 이미지 CMD 가 `alembic upgrade head && uvicorn app.main:app`(`backend/Dockerfile:27`). stg 머지 → CD → 컨테이너 시작 때 새 표 76 이 빈 채로 생긴다. 따로 alembic 을 돌릴 자리는 필요 없다.
3. **stg 에는 gold 프로세스가 없다.** stg 가 띄우는 것은 `app.main` 하나(포트 8000 · Gateway `/procedure-hub/*`). gold 는 별개 ASGI `app.gold_main`(`backend/app/gold_main.py:1-6`)이고 `app.main` 에 gold 연결 0(grep). → 적재만 하면 표는 차지만 아무도 읽지 않는다. **gold 를 stg 에서 어떻게 띄우나(SPEC-003 D-7 · 열림)가 반입과 같이 풀어야 할 첫 정할 것.**
4. **적재기는 이미지에 없다.** 이미지에 실리는 것 = `app/` · `alembic/` · 스크립트 3개(`manage_canonical_release.py` · `prepare_legacy_prod.py` · `prod_readiness.py` — `Dockerfile:21-22`). `load_medallion.py` 와 CSV 는 없다. 단 적재기가 import 하는 `app.modules.gold.*` · `app.model.medallion` 과 의존성(asyncpg · sqlalchemy)은 이미지에 다 있다.
5. **적재 자리 추천 = ⓑ 같은 이미지 일회성 컨테이너(VM 에서 `docker run --rm` · 데이터 · 스크립트 읽기 전용 마운트).** 레포 문서에 같은 꼴의 전례가 두 번 있다(alembic 실행 · `import_legacy_corpus.py` 반입 — `docs/guides/deployment.md:318-334` · `458-483`). ADR 0004 는 「startup seed · data-init image」 를 기각했다(`docs/adr/0004-…:293`).
6. **레포 데이터 폴더 추천 = 루트 `data/medallion/`**(backend/ 밖 · `assets/procedure-images/` 와 같은 층). backend/ 밖이면 Docker build context(`.dockerignore` `**`)에도, backend CI · CD 트리거 경로(`backend/**`)에도 안 걸린다. `.gitignore` 영향 0(`git check-ignore` 확인).

## 1. 일곱 항목

### 1-1. stg 배포 구조

| 무엇 | 사실 | 근거 |
|---|---|---|
| 브랜치 길 | feat → `release/v1.2.0` → `stg`(STG 자동) / `prod`. 문서 그림은 `release/v1.0.0` 으로 낡았으나 본문 · 기본 브랜치는 v1.2.0 | `deployment.md:7-12` · `:72-75` · `:195` · `origin/HEAD → release/v1.2.0` |
| BE CD 트리거 | `stg`/`prod` push 중 `backend/**` · `.dockerignore` · 워크플로 파일 변경. 수동 `workflow_dispatch`(ref = 고른 환경 브랜치여야 함) | `.github/workflows/csp-azure-deploy.yml:3-26` · `:39-52` |
| CD 단계 | verify(=backend-test 재사용: PG 에 `alembic upgrade head` + `alembic check` · ruff · pytest SQLite) → 기존 `:stg` 를 `:stg-rollback` 으로 보존 → 빌드 · ACR push(태그 `:stg` · `:stg-<sha>`) → Bastion 경유 `./deploy.sh procedure-hub stg` → Gateway `health` · `api/v1/products` 확인 → Slack | `csp-azure-deploy.yml:54-160` · `backend-test.yml:66-80` |
| deploy.sh | 레포에 없음(Bastion 의 중앙 스크립트 · 인프라 레포). `/opt/procedure-hub/config/stg.env` 를 `--env-file` 로 연결 · `DATABASE_URL` 없으면 기존 컨테이너 내리기 전에 실패 | `adr/0004:269-271` · `deployment.md:250-261` |
| 실행 꼴 | VM Docker 컨테이너 하나 `procedure-hub` · 호스트 10000 → 8000 · `--restart unless-stopped` · 마운트 없음 | `deployment.md:254-261` · `:128-135` |
| 시작 명령 | **컨테이너 시작마다 `alembic upgrade head` 후 `uvicorn app.main:app`**. 누가: deploy.sh 가 새 컨테이너를 띄울 때(= stg 머지 직후 CD) | `Dockerfile:26-27` |
| env 주입 | VM 파일 `stg.env`(owner azureuser · 600) 하나. 필수 키 `DATABASE_URL` 하나 · 나머지는 코드 기본값. GitHub Actions 는 앱 env 를 넘기지 않는다 | `deployment.md:212-251` |
| 설정 읽기 | 허브 공용 `Settings` · gold `GoldSettings` 모두 `extra="ignore"` → `stg.env` 에 `GOLD_*` 를 더해도 `app.main` 은 무시 | `app/core/config.py:39-43` · `app/modules/gold/config.py` |
| FE | Vercel · `frontend-cd.yml` · BE 와 독립. 「FE 성공 ≠ BE 배포 · migration · 데이터 반입 완료」 | `deployment.md:40-41` |
| 브랜치 보호 | `stg` PR 필수(10/26~) · 관리자 우회 허용 | `deployment.md:88-89` |

### 1-2. stg alembic 위치

| 브랜치 | `backend/alembic/versions` | 머리 |
|---|---|---|
| `origin/stg` (`a3cba75`) | `b202609030001` · `b202610300001` | `b202610300001` |
| `origin/release/v1.2.0` (`3750e4c`) | 같음 | `b202610300001` |
| `origin/prod` (`184e47e`) | 같음 | `b202610300001` |
| 작업 브랜치 `fdc155b` | + `b202611170001`(down `b202610300001`) · `b202611170002`(down `b202611170001`) | `b202611170002` |

- 판정: **한 줄 체인 · 갈림 0.** stg 에만 있는 revision 0.
- stg ↔ release/v1.2.0: stg 쪽 앞선 커밋 2(머지 커밋 · 같은 #27 내용), release 쪽 앞선 커밋 5 — **트리 차이는 `docs/guides/prod-db-rename.md` 1개**(`git diff --stat origin/stg origin/release/v1.2.0`). release → stg PR 은 코드 충돌 없을 것으로 보인다.
- 작업 브랜치 base = `3750e4c` = 지금 release/v1.2.0 머리(5 커밋 앞섬). release 와 견준 마이그레이션 · Dockerfile · `.dockerignore` · 워크플로 · `.gitignore` 차이 = 새 revision 2 파일뿐.
- 확인 안 된 것: **stg DB 의 실제 `alembic_version` 값**(접속 금지). 문서상 마지막 기록은 9/7 `b202609030001` (`deployment.md:51`) · 그 뒤 `b202610300001` 이 든 이미지가 stg 에 배포됐는지는 레포로 알 수 없다. 반입 전에 사람이 `alembic current` 로 확인할 몫(§2 ①).

### 1-3. 일회성 적재를 어디서 돌리나

| 후보 | 가능? | 근거 | 걸리는 것 |
|---|---|---|---|
| ⓐ 떠 있는 `procedure-hub` 컨테이너 안 `docker exec` | 기술적으로 됨 · **비추천** | 컨테이너에 `app/` · venv 가 있다 | 적재기 · CSV 가 컨테이너에 없음 → `docker cp` 로 서빙 컨테이너를 바꿔야 함. 서빙 컨테이너는 「마운트 없음」 이 전제(`prod-migration.md:273` — prod helper 의 검사) · 재시작하면 사라져 기록이 안 남음 |
| **ⓑ 같은 이미지로 일회성 컨테이너(`docker run --rm`)** | **됨 · 추천** | 전례 둘: alembic 실행(`deployment.md:318-334` — `--env-file stg.env --entrypoint .venv/bin/alembic $IMAGE`) · 반입 CLI(`:458-483` — 스크립트 · corpus 를 VM `/opt/procedure-hub/import/<날짜>/` 에 두고 `-v …:ro` · 스크립트도 `/app/scripts/<이름>.py:ro` 로 꽂음) | VM 에 레포 파일을 옮기는 길(Bastion 경유 복사 — 누가 하나) · VM 에 PG client 없음(`:299`) → 적재기가 이미지 안에서 asyncpg 로 붙으니 상관없음 |
| ⓒ 배포 파이프라인 단계 | **비추천** | ADR 0004 기각: 「startup seed 또는 data-init image 복원 — DB 를 SoT 로 만든 경계를 흐림」(`adr/0004:293`) · 「Runtime image 는 migration 과 API 만」(`deployment.md:279-281`) | GitHub runner 는 DB 에 직접 못 닿음(배포가 Bastion SSH 로만 감) → 새 job · deploy.sh 변경 = 인프라 레포 일. 매 배포마다 돌면 「일회성」 결정과도 어긋남 |
| ⓓ 로컬 기계에서 stg DB 로 직접 | 확인 안 됨 | DB 는 공유 Azure PostgreSQL(`adr/0004:279-283`) · 접속 경로 문서에 없음 | 방화벽 · 접속 권한 미확인 · 회사 접속 값이 로컬로 나옴 |

- **이미지에 CSV 가 실리나**: 안 실린다. 루트 `.dockerignore` 가 `**` 로 다 빼고 `backend/` 만 되살림(`.dockerignore:2-12`) — `assets/` · 루트 `data/` 는 build context 에도 안 든다. backend/ 아래라도 Dockerfile 이 `COPY` 하지 않으면 이미지에 없다(`Dockerfile:9-22`).
  - 참고: `.dockerignore` 의 `!backend/` 가 디렉터리째 되살리므로 backend/ 전체가 build context 에 든다(그래서 화이트리스트에 없는 `prepare_legacy_prod.py` 를 `Dockerfile:22` 가 COPY 할 수 있다). → 데이터를 backend/ 밑에 두면 이미지엔 없어도 build context 업로드 · `backend/**` CD 트리거에 걸린다.
- **적재기에 이미지 쪽 손이 필요한가**: 스크립트를 마운트하면 0(전례 그대로). 이미지에 넣으려면 `Dockerfile` 한 줄(`COPY backend/scripts/load_medallion.py scripts/`) — 문서가 「CLI 를 image 에 포함할지는 팀 결정(Dockerfile · `.dockerignore` 각 한 줄)」 이라 적어 둠(`deployment.md:460-463`). → 정할 것 S-3.
- **적재기 env 주는 법(이름만)**:
  - `DATABASE_URL` — `--env-file /opt/procedure-hub/config/stg.env`(같은 값 재사용 · 손으로 치지 않음). 적재기 · db 판은 `GoldSettings` 에서만 읽고(프로세스 env → `envs/.env.gold`), 이미지에 `envs/` 가 없으니 프로세스 env 만 닿는다(`gold/config.py` 머리 주석). URL 꼴(`postgresql+asyncpg://…?ssl=require`)은 허브 공용 엔진과 같은 `create_async_engine(url)` 로 읽힌다(`medallion_load.py:283-288` · `core/db.py:26-43`) — 실물 TLS 접속은 미확인(dry-run 은 접속 안 함).
  - `GOLD_CSV_DIR` · `GOLD_SILVER_DIR` · `GOLD_LEDGER_CHECK_PATH`(필수) · `GOLD_EXPECTED_HASH`(선택 · 주길 추천 — 지금 판 `8accbb21…`) · `GOLD_IMAGE_DIR`(선택 · V13 그림 대조) — `-e` 로 컨테이너 안 마운트 경로를 준다(`medallion_load.py:106` · `load_medallion.py:4-6`).
- 적재기 동작(코드): 검사 → `--dry-run` 이면 요약만 · DB 접속 0 · exit 0/2. 적재는 L1 새 표 76 다 있나(없으면 「`alembic upgrade head` 먼저」 exit 2) → **한 트랜잭션에서 76 표 전부 DELETE → INSERT → 되읽기 대조(L5) → 커밋**. 실패면 롤백(exit 3 · 이전 판 그대로). NullPool · 요청용 시간 제한 안 물려받음(`medallion_load.py:283-288` · `:310-384`).

### 1-4. 레포 데이터 폴더 자리

| 항목 | 사실 |
|---|---|
| 크기 | silver 59 CSV 5.8MB(가장 큰 `source_ref.csv` 4.15MB) · gold 15 CSV + `questions.csv` 6.1MB(가장 큰 1.4MB) · `notes/ledger-check-list.csv` 236KB · 원장 JSON 21 + README · CHANGELOG · HASHES 1.3MB · 그림 103 SVG 는 이미 `assets/procedure-images/`(6.7MB · 추적 104 파일). 합 약 13.4MB(그림 빼고) · GitHub 파일 한도 · LFS 필요 없음(`.gitattributes` 없음) |
| 레포 관례 | 루트에 비코드 자산 `assets/procedure-images/`(우리 브랜치) · 레포 데이터는 `backend/import-data/canonical-mapping.v1.json` 하나(반입 매핑) · 주간 후보는 봇 브랜치의 `data-candidates/evidence/<날짜>/`(`deployment.md:184`) · `backend/database/` 는 ignore(로컬 스냅숏) · 데이터 전용 `data/` · `fixtures/` 폴더 없음(release 트리 확인) |
| `.gitignore` | csv · json 을 막는 규칙 없음 · `data/medallion/**` · `backend/data/**` 둘 다 ignore 아님(`git check-ignore`) |
| `.dockerignore` | 루트 `data/` = build context 밖 · 이미지 밖. `backend/` 밑 = context 안 · 이미지 밖(COPY 없으면) |
| CI · CD 트리거 | `backend/**` 만 반응 — 루트 `data/` 변경은 BE CI · CD 를 안 돌림. 다만 CI 에 「레포 데이터로 dry-run」 시험을 붙이려면 경로 트리거를 더해야 함 |
| 문서 충돌 | `backend/README.md:91` 「데이터는 저장소에 넣지 않고 경로를 env 로」 — 반입하면 고쳐야 함 · `assets/procedure-images/README.md` 의 대조 표에 데이터 폴더 자리 추가 |

추천 배치(초안 — 결정은 S-1):

```text
data/medallion/
  README.md            판 · gold_hash · aux_hash · 파일 수 · 만든 곳(프로필 archive 경로 · 커밋) · 적재 명령
  silver/              59 CSV  (= GOLD_SILVER_DIR · GOLD_HIERARCHY_DIR · source_ref.csv = GOLD_SOURCE_REF_PATH)
  gold/                15 g_*.csv + questions.csv  (= GOLD_CSV_DIR)
  ledger-check-list.csv                 (= GOLD_LEDGER_CHECK_PATH)
  bronze/phub-ledger/  원장 JSON 21 + README · CHANGELOG · HASHES  (적재기는 안 읽음 · source_ref 가 가리키는 원문)
```

- 판 폴더(`data/medallion/<판>/`)로 쌓지 않고 한 벌만 둔다 추천 — 적재기가 「판 하나 교체」 라 DB 에도 한 판뿐이고, 옛 판은 git 이력이 가진다.
- gold 폴더에 `.py` · `.md` 를 같이 두면 안 된다 — gold 폴더의 계약 밖 CSV 는 `hash_only` 로 해시에 들어가고(`inputs.py:117-120`) silver 폴더의 계약 밖 CSV 는 V3 거부(SPEC-003). 스크립트 · 노트는 CSV 가 아니라 해시엔 안 들지만 폴더를 섞지 않는 편이 안전.

**만드는 스크립트를 같이 넣나** — 의존 실측:

| 스크립트 | 읽는 것 | 레포 안에서 다시 돌아가나 |
|---|---|---|
| `gold/gold-build.py`(1,058줄) | `silver/*` · `notes/relation-conflicts.csv`(28KB) · `notes/ledger-check-list.csv` | **된다** — 두 notes 파일만 같이 오면 |
| `gold/gold-check.py`(448줄) | 위 + `archive/silver-before-gold-final/` · `drafts/gold/` · `drafts/glossary/glossary-build.py` · `drafts/silver-check/` · `notes/same-day-judgment.csv` | 안 된다(archive 153MB · drafts 35MB 에 기댐) |
| `gold/silver-supplement.py`(303줄) | `archive/silver-before-gold-final/silver` · notes 판정 표 | 안 된다 |
| `gold/silver-image.py`(156줄) | 프로필 `reference/2026-11-17-procedure-images` 시드 | 안 된다 |

→ 추천: **이번엔 산출물(CSV · 원장)만 넣고 스크립트는 넣지 않는다.** `README.md` 에 만든 곳(프로필 archive 경로 · 프로필 커밋)과 해시를 적는다. 넣는다면 `gold-build.py` + notes 2 파일만(레포 안 재현 가능한 유일한 것) — S-2.

### 1-5. 그림 서빙 자리(다음 스펙 재료)

| 자리 | 사실 |
|---|---|
| compose | 레포에 compose 파일 0(`find` · maxdepth 3). stg 는 compose 가 아니라 deploy.sh 의 `docker run` |
| 지금 서빙 컨테이너 마운트 | 없음 · `docker run -d --env-file … -p 10000:8000 <image>`(`deployment.md:254-261`) · prod 전환 helper 는 「기존 mounts 없음」 을 검사(`prod-migration.md:273`) |
| VM 디렉터리 전례 | `/opt/procedure-hub/config/`(env) · `/opt/procedure-hub/import/<날짜>/`(반입 CLI 입력 · 일회성 컨테이너에 `:ro`) · `/opt/procedure-hub/cutover/`(덤프) · `/opt/procedure-hub/bin/`(prod helper) |
| 이미지에 싣기 | 지금 막혀 있음(`.dockerignore` · `assets/procedure-images/README.md` 끝줄 「이 폴더는 Docker 이미지에 실리지 않는다」). 싣는다면 `.dockerignore` · Dockerfile 각 한 줄 + 103 SVG 6.9MB 가 매 이미지에 |
| 허브 정적 서빙 코드 | 0(`StaticFiles` · `FileResponse` 0 — `research-images.md` §5 · HEAD 같음) |
| 정리 | 바인드 마운트(VM `/opt/procedure-hub/<자리>/procedure-images:ro`)는 **서빙 컨테이너 쪽 deploy.sh 변경 = 인프라 레포 일**이다. 이미지에 싣기는 레포 안에서 끝나지만 ADR 의 「image 는 migration + API 만」 과 부딪힘. gold 진입점(§1-6)을 어디에 두느냐와 같이 정해야 함 |

### 1-6. 허브 시작 모드(`GOLD_REPOSITORY=db`)

| 항목 | 사실 | 근거 |
|---|---|---|
| stg 에 gold 가 뜨나 | **안 뜬다.** CMD 는 `app.main` 만 · `app.main` 은 gold 를 import 하지 않음 | `Dockerfile:27` · `grep gold app/main.py` 0 |
| db 판 필요 env | `GOLD_REPOSITORY=db` · `DATABASE_URL` · (선택) `GOLD_EXPECTED_HASH` — db 판은 CSV 경로 넷을 읽지 않는다(`db_inputs.py` 가 읽는 설정 = `DATABASE_URL` · `GOLD_EXPECTED_HASH` 뿐) | `gold_main.py:28-42` · `db_inputs.py:95-97,152` |
| 경로 · 마운트 기본값 | REST `GOLD_API_PREFIX=/procedure-hub/gold` · MCP `GOLD_MCP_MOUNT_PATH=/procedure-hub/gold-mcp` — Gateway 의 `/procedure-hub/*` 아래와 모양이 맞음 | `gold/config.py` |
| 지금 stg 허브의 gold env | 레포로는 「없음」 만 알 수 있음(문서상 `stg.env` 필수 키 `DATABASE_URL` 하나 · `deployment.md:231`). VM 파일 실제 키는 접속 금지로 미확인 |
| 빈 표로 gold 가 뜨면 | **시작 실패**: `medallion_build` 0 행 → `F2 medallion_build 0행 — 적재 먼저`(lifespan 예외) | `db_inputs.py:125-130` · `gold_main.py:3-4` |
| 빈 표가 `app.main` 에 주는 영향 | 0 — `app.main` 은 새 표를 안 읽음. 새 표 76 은 기존 167 표와 FK 0(SPEC-003 D-10) |
| 순서 문제 | 새 표는 「배포된 컨테이너가 시작할 때」 생긴다 → 적재는 배포 **뒤**에만 가능. 그러므로 gold 를 **`app.main` 에 묶어 같은 프로세스로 띄우는 설계**면, 그 배포가 빈 표에서 F2 로 죽고 **CD 의 health · products 확인이 실패 → stg 허브 전체가 내려간다**. 막는 길: ⓐ gold 를 별도 프로세스 · 컨테이너로(적재 뒤에 띄움) ⓑ 묶더라도 「끔 → 적재 → 켬」 두 번 배포 ⓒ 빈 표면 gold 만 비활성으로 뜨는 코드(새 동작 · SPEC 몫) ⓓ 배포 전에 후보 이미지로 일회성 `alembic upgrade head` + 적재(문서 전례 `deployment.md:318-321` 꼴) — 단 후보 이미지 `:stg-<sha>` 는 stg push 때만 빌드돼서 머지 전엔 없다(`csp-azure-deploy.yml:100-113`) → 실제로는 직전 이미지가 새 revision 을 몰라 못 함 |
| 지금 코드로 가장 덜 바꾸는 길 | 같은 이미지 · 다른 명령(`uvicorn app.gold_main:app --port <다른 포트>`)의 두 번째 컨테이너 + Gateway 경로 하나 — 코드 0 · 인프라(deploy.sh · Gateway route) 일 |

### 1-7. 되돌리기 · 갱신

| 상황 | 동작 | 근거 |
|---|---|---|
| dry-run 실패 | exit 2 · DB 접속 0 · 할 일 = 데이터 · env 고침 | `medallion_load.py:398-401` |
| 적재 중 실패(접속 · L1 표 없음) | exit 2 · 쓴 것 0 | `:356-366` |
| 쓰기 · 되읽기 · 커밋 실패 | exit 3 · 트랜잭션 롤백 · **이전 판 그대로**(처음 적재면 빈 표 그대로) | `:364-388` |
| 다음 gold 판 갱신 | 레포 `data/medallion/` 갱신 PR → 머지(스키마 안 바뀌면 이미지 재배포 불필요 · 루트 `data/` 는 CD 안 돎) → VM 에 새 판 파일 → 같은 일회성 컨테이너로 dry-run → 적재(76 표 통째 DELETE → INSERT · 한 트랜잭션) → gold 프로세스 재시작(시작 때 한 번 읽음 · 요청은 메모리) → health 의 `gold_hash` 확인 | `load_medallion.py:5-6` · `gold_main.py:3-6` |
| 스키마가 바뀌는 판 | 새 revision(앞으로만) → stg 배포(시작 때 upgrade) → 적재. 표가 늘었는데 스키마가 안 따라오면 V3 로 거부(silver 계약 밖 CSV) | SPEC-003 V3 |
| 판 되돌리기 | 앞 판 CSV(git 이력의 앞 커밋)로 같은 적재를 다시 → 「판 하나 교체」 라 되돌리기 = 앞 판 다시 싣기. **`alembic downgrade` 는 쓰지 않는다**(11-17 로컬 사고: 워커 downgrade 가 표를 내림 · `_RESUME.md:201`) | — |
| 런타임 되돌리기 | CD 가 `:stg-rollback` 을 남김 · 문서 절차(`deployment.md:367-389`). 단 **옛 이미지는 새 revision `b202611170002` 를 모른다** → 새 표가 생긴 DB 에 옛 이미지를 띄우면 시작 때 `alembic upgrade head` 가 「알 수 없는 revision」 으로 실패할 수 있다(문서가 baseline 전환 때 같은 경고 · `:369-371`). 되돌릴 땐 이 점을 먼저 볼 것 | — |
| 서빙 중 갱신 안전 | gold db 판은 반복 읽기 격리 한 스냅숏 + 빌드 기록 앞뒤 대조로 섞인 판을 안 듦(SPEC-003 P8) · 적재 중 gold 재시작이 겹쳐도 한 판만 | `db_inputs.py:109-114` |

## 2. 반입 절차 초안(순서 · 누가 · 승인 지점)

전제: 원천 = 허브 레포. 스키마는 배포가 만들고, 적재는 배포 뒤 일회성 컨테이너가 한다. gold 서빙은 S-4 결정을 따른다(아래는 「별도 컨테이너」 를 가정한 꼴).

| # | 무엇 | 누가 | 승인 |
|---|---|---|---|
| 0 | 데이터 반입 WORK: `data/medallion/` 에 silver 59 · gold 16 · 원장 확인 목록 · (원장 JSON) + README(해시) · `backend/README.md:91` 문장 고침 · (S-3 이면 Dockerfile 한 줄) · 로컬에서 레포 경로로 dry-run · 로컬 DB 적재 → 같은 `gold_hash` | 워커(코드) · 코디 검증 | — |
| 1 | 허브 브랜치 push · PR → `release/v1.2.0` 머지 (CI: PG `alembic upgrade head` + `alembic check` 통과 확인) | 사용자 | **승인 ①** |
| 2 | 반입 전 stg 상태 기록: `alembic current`(= `b202610300001` 기대) · 현재 이미지 digest · **DB 백업**(문서 관례 `deployment.md:90-91` · `:292`) | VM 권한자(인프라 · 사용자) | 확인 |
| 3 | release → `stg` PR 머지 → CD 자동: 이미지 `:stg-<sha>` · 컨테이너 교체 · 시작 때 `alembic upgrade head`(새 표 76 · 빈 표) · Gateway health · products 통과 | 사용자(머지) · CD | **승인 ②** |
| 4 | 배포 확인: `alembic current` = `b202611170002` · 기존 API 응답 그대로 | VM 권한자 | — |
| 5 | VM 에 반입 폴더 `/opt/procedure-hub/import/<날짜>/` 에 같은 커밋의 `data/medallion/` · `assets/procedure-images/` · (S-3 이 「마운트」 면) `backend/scripts/load_medallion.py` | VM 권한자 | — |
| 6 | dry-run: `docker run --rm --env-file stg.env -v <반입>:/import:ro [-v <반입>/load_medallion.py:/app/scripts/load_medallion.py:ro] -e GOLD_CSV_DIR=… -e GOLD_SILVER_DIR=… -e GOLD_LEDGER_CHECK_PATH=… -e GOLD_EXPECTED_HASH=… -e GOLD_IMAGE_DIR=… --entrypoint .venv/bin/python <image:stg-sha> scripts/load_medallion.py --dry-run` → exit 0 · 요약 출력(표 수 · 행 수 · 해시)을 보고서로 남김 | VM 권한자 | 결과를 사용자에게 |
| 7 | 적재: 같은 명령에서 `--dry-run` 뺌 → exit 0 · `loaded tables 76 · rows …` | VM 권한자 | **승인 ③(반입)** |
| 8 | gold 띄우기(S-4): 예) 같은 이미지 · `GOLD_REPOSITORY=db` · `uvicorn app.gold_main:app` 두 번째 컨테이너 + Gateway 경로 · health 의 `gold_hash` = 기대값 · 로컬 18105 와 같은 키 대조 | 인프라 · 코디 검증 | **승인 ④(gold 공개)** |
| 9 | 기록: 적재 보고서 · 해시 · 시각 → `_RESUME` | 코디 | — |

## 3. 정할 것(사용자 몫 · 추천 붙임)

| # | 무엇 | 후보 | 추천 | 까닭 |
|---|---|---|---|---|
| S-1 | 레포 데이터 폴더 자리 | (a) 루트 `data/medallion/{silver,gold,ledger-check-list.csv,bronze/}` (b) `backend/data/medallion/` (c) `backend/import-data/medallion/` | **(a)** | backend/ 밖 = build context · BE CD 트리거 밖 · `assets/` 와 같은 층. (b)(c)는 데이터 PR 마다 BE CI · CD 가 돎 |
| S-2 | 만드는 스크립트 같이 넣나 | (a) 산출물만 + README 에 출처 (b) + `gold-build.py` · notes 2 (c) 스크립트 넷 · 노트 다 | **(a)** | `gold-check` · `silver-supplement` · `silver-image` 는 레포 밖(archive 153MB · drafts · 시드)에 기대 레포 안에서 안 돈다. (b)는 재현 가능하나 검사 없이 빌드만 들어옴 |
| S-3 | 적재기를 이미지에 넣나 | (a) 안 넣고 VM 에서 마운트(문서 전례) (b) Dockerfile 한 줄로 이미지에 | **(b)** | 한 줄 · 데이터는 안 실음 · 적재기와 앱 코드가 늘 같은 커밋(마운트면 버전 어긋날 틈). 문서가 「팀 결정」 으로 열어 둔 자리라 회사 팀 확인 필요 |
| S-4 | stg 에서 gold 를 어떻게 띄우나(SPEC-003 D-7) | (a) 같은 이미지 · 두 번째 컨테이너 `app.gold_main` + Gateway 경로 (b) `app.main` 에 gold 를 붙임(코드) (c) 빈 표면 gold 만 끄고 뜨는 코드 + (b) | **(a)** | 코드 0 · 빈 표 · 적재 실패가 기존 허브를 못 죽임(§1-6 순서 문제). 대신 deploy.sh · Gateway 가 인프라 레포 일 — 회사 인프라 담당 |
| S-5 | 원장 JSON 21 을 레포에 넣나 | (a) 넣음(`bronze/phub-ledger/`) (b) 안 넣음 | **(a)** | 적재기는 안 읽지만 `source_ref` 가 가리키는 원문 · 1.3MB · 공개 정보(사용자 11-17) |
| S-6 | VM 작업 주체 | 사용자 직접 · 회사 인프라 담당 | (확인만) | VM SSH · Bastion · Gateway 는 문서상 인프라 담당 몫(`deployment.md:214-216`) — 사용자가 VM 권한이 있는지 레포로는 모름 |
| S-7 | 그림 서빙 | (a) 바인드 마운트(인프라) (b) 이미지에 실음 | 다음 스펙 · S-4 와 같이 | (b)는 ADR 「image 는 migration + API 만」 과 충돌 · (a)는 서빙 컨테이너 마운트 = deploy.sh 변경 |

## 4. 확인 못 한 것

- stg DB 실제 `alembic_version` · `stg.env` 실제 키 · VM 디렉터리 상태 · deploy.sh 본문(인프라 레포) — 접속 · 열람 금지로 미확인.
- stg DB 로의 TLS URL 을 적재기 · db 판 엔진이 그대로 받는지 실물 — 코드상 허브 공용과 같은 `create_async_engine(url)` 이라 같다고 보지만 실호출 0.
- Gateway 에 새 경로(`/procedure-hub/gold*`)를 더할 수 있는지 · 같은 VM 에 두 번째 포트를 열 수 있는지.
