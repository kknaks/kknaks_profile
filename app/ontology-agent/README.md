# ontology-agent — 온톨로지 데모 앱

기록 01~08 이 밟은 구축 순서를 그대로 재현하는 데모. 계획·게이트의 SoT 는
`para/resources/note/ontology/2026-09-01-ontology-09-agent-app-plan.md` (기록 09).

```
db/       커넥션 규약(읽기 전용 포함) + 계층 스키마 부트스트랩
build/    브론즈 적재 + 실버·골드 빌드 DB 이식 (규칙 SoT: 기록 04·05)
tools/    MCP 조회 도구 4종 — query_kpi · query_layer · trace_ontology · get_definition
api/      화면·채팅 API
static/   단일 페이지 (계층 탐색 + KPI + 그래프 + 예보 + 채팅)
tests/    게이트·회귀 테스트
```

- 원천 데이터·DB 는 레포 밖 (`reference/ontology_demo/` — PII, gitignore). 경로는 `config.py` (`ONTOLOGY_DATA_DIR`).
- LLM 은 open-kknaks 경유 (ADR-04). 관계 지식은 프롬프트가 아니라 `ontology_edges` 에 있다 (S-001).

## 빌드 (WORK-001)

SQLite 한 파일에 `bronze_*`(16) → `silver_*`(6) → `gold_*`(5) → `ontology_*`(2) 와
마스킹 뷰 `v_*`(4) 가 전부 들어간다. 계약은 SPEC-001 §4 다.

```bash
export ONTOLOGY_DATA_DIR=<원천 경로>          # bronze/·silver/_scoring/·ontology/ 가 있는 곳
export ONTOLOGY_DB_PATH=<산출 DB 경로>        # 미지정 시 $ONTOLOGY_DATA_DIR/db/ontology_demo.db

uv run python -m build all                    # 부트스트랩 → 적재 → 실버 → 뷰 → 골드 → 온톨로지 → 게이트 1·2·3
uv run python -m build bronze                 # 단계별 실행
uv run python -m build gate2                  # 게이트 단독 재실행 (WORK-005 가 쓴다)
```

게이트 실패는 **exit code ≠ 0** 이고 SPEC-001 §4 Case Matrix 의 코드 **13종**과
기대·실측값을 로그로 남긴다. 로그에 PII 원값은 남지 않는다.

`BRONZE_ROWCOUNT_MISMATCH` · `ENUM_VIOLATION` · `NEGATIVE_AMOUNT` ·
`CLOSED_LIST_VIOLATION` · `REBUILD_MISMATCH` · `ORPHAN_EDGE` · `PII_LEAK` ·
`NODE_ID_MISMATCH` · `REVIEW_SCORE_VIOLATION` · `MASKING_RESIDUE` ·
`AGREEMENT_BELOW_THRESHOLD` · `UNKNOWN_BRANCH` · `SILVER_ROWCOUNT_MISMATCH`

전 게이트를 통과하면 **빌드 표식**(`build_meta` 1행)이 채택 트랜잭션 안에서 찍힌다.
표식이 없는 DB 는 `connect_ro()` 가 열지 않는다 — 「한 번도 안 만든 DB」와 「빌드가 실패한
DB」를 파일 존재만으로는 구분할 수 없기 때문이다.
**단계 단독 실행(`build gold` 등)은 표식을 지운다** — 게이트를 거치지 않은 산출물이
「1,2,3 통과」로 서빙되면 표식이 거짓을 말하게 된다. 다시 서빙하려면 `build all` 을 돌린다.
게이트 단독 재실행(`gate1`~`gate3`)은 읽기만 하므로 표식을 건드리지 않는다.

**소비자(WORK-002~004)는 `db.connect_ro()` + 마스킹 뷰로만 닿는다** — 원 테이블을 직접
읽는 조회 경로를 만들지 않는다(DEC-002). 브론즈는 적재 이후 불변이고, 상위 계층은 바로
아래 계층만 읽는다.
`connect_ro()` 는 **쓰기만** 막으므로 뷰 경유 강제는 커넥션이 아니라 코드로 보장한다 —
`tests/test_w002_ac8_view_only.py` 의 정적 검사가 그 게이트다.

## 게이트 (WORK-005 P2) — 한 명령

게이트 1~5 와 PII 전면 스캔이 **한 번의 실행으로 전건 판정**된다. 별도 CI 는 두지
않는다(레포 방침) — 사람이 아래 한 줄을 돌리는 것이 실행 경로다.

```bash
ONTOLOGY_DATA_DIR=<원천 경로> uv run pytest -q tests/
```

원천이 없으면 전 테스트가 skip 된다 — 원천 없는 환경에서 빨간 줄을 만들지 않기 위함이다.

| 게이트 | 무엇 | 어디 | 라이브 필요 |
|---|---|---|---|
| 1 | 브론즈 16테이블 행수 대사 | `test_w005_integration.py` · `test_p2_bronze_gate1.py` | 아니오 |
| 2 | 빌드 재현 대조 + 기존 CSV 산출물 셀 대조 | `test_w005_integration.py` · `test_p5_*` | 아니오 |
| 3 | 마스킹 뷰 원값 0건 | `test_w005_integration.py` · `test_p3_masking_views.py` | 아니오 |
| 3+ | **표면 전수 PII 스캔**(API·MCP·채팅·드릴다운·로그) | `test_w005_integration.py` | 아니오 |
| 4 | 회귀 3본(R-1·R-2·R-3) | `test_w003_regression.py` — 기준값 계층 | 아니오 |
| 4 | 회귀 3본 — 실제 답변 단언 | `test_w003_regression.py` — 라이브 계층 | **예** |
| 5 | 근거 무결성 ①citations 재조회 ②used_edges ⊆ 확정 ③마스킹 | `test_w003_answer.py` | 아니오 |
| 5 | 위를 실제 답변에 태운다 | `test_w003_regression.py` — 라이브 계층 | **예** |

**라이브 플래그** — 라이브 계층 5본은 `ONTOLOGY_LIVE_REGRESSION=1` 일 때만 돈다.
redis + ontology-worker + codex 인증이 서 있어야 하고, 없으면 skip 된다.
기준값 계층이 **라이브의 전제**다 — 과녁(DB 실측)이 틀리면 라이브가 통과해도 의미가 없다.

```bash
# 아래 「로컬 E2E」 3~4단계를 먼저 세운 뒤
ONTOLOGY_DATA_DIR=<원천 경로> \
ONTOLOGY_DB_PATH=$PWD/.data/ontology_demo.db \
ONTOLOGY_REDIS_URL=redis://localhost:46379/0 \
ONTOLOGY_MCP_URL=http://host.docker.internal:48081/mcp \
ONTOLOGY_LIVE_REGRESSION=1 uv run pytest -q tests/test_w003_regression.py -s
```

실패는 **어느 게이트가 왜 깨졌는지**를 코드·기대·실측으로 출력한다. 고의 실패 주입
회귀는 `tests/test_fix_gate_enforcement.py` 가 갖는다 — 게이트 2·3 을 각각 깨뜨려
「해당 게이트만 실패하고 **이전 DB 가 그대로 남는지**」까지 본다.

## 배포 전제

- **MCP 도구 서버는 자기 인증을 갖지 않는다.** SPEC-002 가 도구 서버 인증을 Out of scope 로
  두고 배포에 넘겼기 때문이다. 포트(기본 28081)가 노출되면 **비밀번호 없이** `query_layer` 로
  마스킹 브론즈 행을 읽을 수 있다 — 접속 게이트는 HTTP API 앞에만 선다.
  → 포트를 외부에 열지 말고, `ONTOLOGY_MCP_ALLOWED_HOSTS` 를 **명시 주입**한다.
- `mcp_allowed_hosts` 기본값 `["*"]` 는 SDK 의 DNS rebinding 보호를 무력화하는 값이면서
  실제로는 `Invalid Host header` 로 동작하지도 않는다. 배포·로컬 모두 명시가 필요하다.
  예: `ONTOLOGY_MCP_ALLOWED_HOSTS='["ontology-mcp:28081"]'`
- `ONTOLOGY_DEMO_PASSWORD` 미주입이면 인증 발급·검증이 **양쪽 다** 닫힌다(전 API 401).
  기본값이 없다는 것이 「아무나 들어온다」가 되지 않게 한 것이다.
- **프론트(Vercel)와 API(홈서버)는 항상 다른 오리진이다.** `ONTOLOGY_ALLOWED_ORIGINS` 에
  실제 프론트 주소가 없으면 브라우저가 모든 호출을 막아 **게이트 화면부터 죽는다.**
  `credentials: include` 를 쓰므로 `*` 는 규칙상 못 쓴다. 세션 쿠키의 `SameSite` 는
  `ONTOLOGY_SESSION_COOKIE_SECURE` 에서 파생한다(1 → `None`, 0 → `Lax`) — 교차 사이트에서
  `Lax` 면 쿠키가 실리지 않아 게이트를 통과해도 다음 요청이 401 이다.


## 로컬 E2E — 내일 아침 그대로 따라 하기

한 번에 세 화면과 채팅까지 본다. **명령은 복붙 가능하고, 순서가 곧 의존성이다.**
아래 절차는 2026-09-03 에 실기동으로 1회 검증했다(임시 비밀번호 · 실측 소요는 각 단계에 적음).

전제: 원천 경로(`reference/ontology_demo`)와 `.data/ontology_demo.db`(빌드 산출)가 있고,
맥에 리눅스용 codex 번들(`~/.cache/axkg-live/.claude-tools`)과 codex 로그인이 있다.

```bash
cd app/ontology-agent
export ONT=$PWD
export ONTOLOGY_DATA_DIR=<원천 경로>          # reference/ontology_demo
```

### 1) 비밀번호 한 줄 — `.env`

```bash
cp .env.example .env                          # 아직 없으면
printf 'ONTOLOGY_DEMO_PASSWORD=%s\n' "$(openssl rand -base64 18)" >> .env
grep ONTOLOGY_DEMO_PASSWORD .env              # 값 확인 — 화면 게이트에 이걸 넣는다
```

`.env` 는 gitignore 다. 값은 여기 말고 어디에도 적지 않는다.

### 2) 빌드 — 게이트 1·2·3 까지 한 번에 (~40초)

```bash
uv run python -m build all --db "$ONT/.data/ontology_demo.db"
```

마지막 줄이 `전 게이트 통과 — 산출물 채택` 이어야 한다. 빌드 표식이 없는 DB 는
API 가 열지 않는다(전 조회 503).

### 3) redis + ontology-worker (~30초, 첫 빌드는 더 걸린다)

```bash
docker compose -f docker-compose.local.yml up -d --build
docker logs ontology-demo-worker | tail -3     # worker.started queues=['ontology'] 확인
```

`app/back/docker-compose.yml` 은 **쓰지 않는다** — 그쪽은 postgres·back 까지 요구한다.
로컬은 상주 프로세스 둘(redis·codex 워커)이면 충분하다.

### 4) MCP + API — 호스트에서 uvicorn 둘

```bash
# MCP (터미널 A) — 워커가 host.docker.internal 로 들어오므로 Host 를 명시한다
ONTOLOGY_DB_PATH=$ONT/.data/ontology_demo.db \
ONTOLOGY_MCP_ALLOWED_HOSTS='["host.docker.internal:48081","localhost:48081","127.0.0.1:48081"]' \
uv run uvicorn tools.server:asgi --host 0.0.0.0 --port 48081

# API (터미널 B) — 비밀번호는 .env 에서 온다
ONTOLOGY_DB_PATH=$ONT/.data/ontology_demo.db \
ONTOLOGY_CHAT_DB_PATH=$ONT/.data/ontology_chat.db \
ONTOLOGY_SESSION_COOKIE_SECURE=0 \
ONTOLOGY_REDIS_URL=redis://localhost:46379/0 \
ONTOLOGY_MCP_URL=http://host.docker.internal:48081/mcp \
uv run uvicorn main:app --host 127.0.0.1 --port 48080
```

확인 — 셋 다 통과해야 다음으로 간다:

```bash
curl -s http://127.0.0.1:48081/health                       # {"status":"ok",...,"tools":4}
curl -s http://127.0.0.1:48080/health                       # {"ok":true}
docker exec ontology-demo-worker python -c \
  "import urllib.request; print(urllib.request.urlopen('http://host.docker.internal:48081/health').read())"
```

마지막 줄이 **워커에서 MCP 가 보이는지**다. 여기서 막히면 채팅이 도구를 못 부른다.

### 5) front dev — 실 API 를 보게

```bash
cd ../front
NEXT_PUBLIC_ONTOLOGY_API_BASE=http://127.0.0.1:48080 npm run dev
```

env 가 비면 **mock 모드**로 뜬다(픽스처를 그린다). 실 API 를 보는지 확인:

```bash
curl -s http://localhost:3000/ontology/monitoring \
  | grep -o 'src="[^"]*monitoring/page.js"' | head -1     # 이 청크에 48080 이 박혀 있다
```

### 6) 게이트 로그인 → 세 화면

브라우저로 <http://localhost:3000/ontology> 를 연다.

1. 게이트 화면에 1단계의 비밀번호를 넣는다 → `/ontology/monitoring` 으로 들어간다.
2. **모니터링** — KPI 카드 · 원인 분석 그래프 · 예보 · 엣지 인스펙터
3. **데이터** — 계층 탭(브론즈·실버·골드·온톨로지) · 행 조회 · 계보
   브론즈 예약 테이블에서 `patientName` 이 `김○○`, `phone` 이 `010-****-1234`,
   `birthday` 가 `1990-**-**` 로 보이는지 본다. **원값이 보이면 그 자리에서 멈춘다.**
4. **채팅** — 아래 7단계

세션이 없으면 세 라우트 어디로 들어와도 게이트만 보인다(rewrite — URL 은 안 바뀐다).

### 7) 채팅 — 질문 2건 (각 ~35초)

**두 건을 다 넣는다.** R-1 은 현황 질문(엣지를 안 밟는다), R-2 는 원인 질문이다 —
**게이트 5-③(칩 클릭 → 모니터링 하이라이트)은 R-2 로만 실제로 확인된다.**
R-1 은 `used_edges` 가 비어서 하이라이트할 것이 없다.

#### 7-1. R-1 — `최근 4주 노쇼율 추이는?`

- `pending` 동안 부분 텍스트와 도구 단계가 **자란다**(2초 폴링).
- `done` 이 되면 주별 4행(5.34% · 4.76% · 5.23% · 4.99%)이 나오고 인용 칩이 붙는다.
- 인용 칩은 **수치 출처**를 가리킨다(엣지 칩이 아니다).

#### 7-2. R-2 — `8월 매출이 왜 떨어졌어?`  ← **게이트 5-③ 육안 확인**

전제가 틀린 질문이다. 8월 매출은 **떨어지지 않았다**(7월 대비 +27%). 떨어진 것은
내원(5,428 → 4,196)과 예약(9,057 → 6,852)이다.

봐야 할 것 — **하나라도 어긋나면 그 자리에서 멈춘다**:

1. **전제 교정이 먼저 나온다** — 「매출은 떨어지지 않았다, 떨어진 것은 …」.
   교정 없이 원인부터 설명하면 실패다.
2. **엣지 칩이 붙는다** — 확정 판정(`채택`·`자동 확정`·`선언`)만. `보류`·`기각` 칩이
   보이면 게이트 5-② 위반이다.
3. **엣지 칩을 클릭한다 → 모니터링 그래프의 그 엣지가 하이라이트된다.**
   이것이 게이트 5-③ 이다. 확인할 것:
   - 하이라이트된 엣지 집합이 답변의 엣지 칩과 **정확히 같다**(더도 덜도 아니다)
   - 답변에 없는 엣지가 켜져 있지 않다
   - 칩을 해제하면 하이라이트도 풀린다
4. 인용 수치가 그래프·KPI 카드의 값과 같다.

터미널로 확인하려면(브라우저 없이 — 단, 3번 하이라이트는 화면에서만 보인다):

```bash
PW=$(grep ONTOLOGY_DEMO_PASSWORD .env | cut -d= -f2-)
curl -s -c /tmp/ont.jar -X POST http://127.0.0.1:48080/api/auth/session \
  -H 'Content-Type: application/json' -d "{\"password\":\"$PW\"}"

ask() {
  CID=$(curl -s -b /tmp/ont.jar -X POST http://127.0.0.1:48080/api/chat/conversations \
    -H 'Content-Type: application/json' -d "{\"question\":\"$1\"}" \
    | python3 -c 'import sys,json; print(json.load(sys.stdin)["conversation"]["id"])')
  until curl -s -b /tmp/ont.jar "http://127.0.0.1:48080/api/chat/conversations/$CID" \
    | python3 -c 'import sys,json; m=json.load(sys.stdin)["messages"][-1]; print(m["status"]); exit(m["status"]=="pending")'
  do sleep 2; done
  curl -s -b /tmp/ont.jar "http://127.0.0.1:48080/api/chat/conversations/$CID" \
    | python3 -c '
import sys, json
r = json.load(sys.stdin)["messages"][-1]["result"]
print("교정:", r["premise_correction"])
print("엣지:", [e["edge_id"] for e in r["used_edges"]])   # ← 하이라이트가 이것과 같아야 한다
print("본문:", r["answer"][:200])'
}

ask "최근 4주 노쇼율 추이는?"
ask "8월 매출이 왜 떨어졌어?"
```

마지막 출력의 **엣지 목록이 화면 하이라이트와 같은지**가 게이트 5-③ 판정이다.

### 정리

```bash
cd "$ONT" && docker compose -f docker-compose.local.yml down -v
# 터미널 A·B 의 uvicorn 은 Ctrl+C
```

## 배포 — 홈서버(docker + NPM) + Vercel

**여기 적힌 것은 절차뿐이다. 값은 하나도 적지 않는다**(DEC-005).
프론트는 Vercel(기존 profile 배포에 포함), 백/redis/codex 워커는 홈서버다 —
상주 프로세스는 Vercel 에 올릴 수 없다.

### 1) 홈서버 — DB 사본을 레포 밖에 둔다

빌드는 **원천이 있는 자리에서 사람이** 돌리고, 산출 DB 파일 하나만 서버로 올린다.
원천 데이터는 서버에 올리지 않는다.

```bash
# 로컬 — 게이트 전건 통과본을 만든다
ONTOLOGY_DATA_DIR=<원천 경로> uv run python -m build all --db /tmp/ontology_demo.db

# 서버로 — 레포 밖 경로다(볼륨이 여기를 읽는다)
ssh home-server 'mkdir -p ~/ontology-demo/db'
scp /tmp/ontology_demo.db home-server:~/ontology-demo/db/
```

`ONTOLOGY_DB_DIR` 로 경로를 바꿀 수 있다(기본 `/home/kknaks/ontology-demo/db`).

### 2) 홈서버 — `.env` 에 키 넣기

`app/ontology-agent/.env.example` 을 `.env` 로 복사하고 아래 셋을 채운다.
**compose 는 `app/back/.env` 와 `app/ontology-agent/.env` 를 둘 다 읽는다.**

| 키 | 어디에 | 값 |
|---|---|---|
| `ONTOLOGY_DEMO_PASSWORD` | `app/ontology-agent/.env` | `openssl rand -base64 18` 로 만든 난수 |
| `ONTOLOGY_ALLOWED_ORIGINS` | `app/ontology-agent/.env` | 프론트 주소 JSON 배열 |
| `ONTOLOGY_ALLOWED_ORIGINS` | `app/back/.env` | 위와 같은 값(compose 가 `:?` 로 요구한다) |

```bash
ssh home-server
cd ~/kknaks_profile/app/ontology-agent
cp .env.example .env
printf 'ONTOLOGY_DEMO_PASSWORD=%s\n' "$(openssl rand -base64 18)" >> .env
printf 'ONTOLOGY_ALLOWED_ORIGINS=["https://profile.kknaks.cloud"]\n' >> .env
# compose 의 `:?` 체크용 — app/back/.env 에도 같은 줄
printf 'ONTOLOGY_ALLOWED_ORIGINS=["https://profile.kknaks.cloud"]\n' >> ../back/.env
```

비밀번호는 **여기서 만들고 여기서만 산다.** 공유는 사람이 직접 전달한다.

### 3) 홈서버 — compose 로 3종 기동

```bash
cd ~/kknaks_profile/app/back
docker compose up -d --build ontology-mcp ontology-api ontology-worker
docker compose ps ontology-mcp ontology-api ontology-worker
docker compose logs -f ontology-api | head -20
```

**기존 서비스는 건드리지 않는다** — `back`·`worker`·`chat-worker`·`postgres`·`redis`
정의는 한 줄도 바뀌지 않았고, 위 명령은 신규 3종만 올린다.

확인:

```bash
curl -s http://127.0.0.1:48080/health                      # {"ok":true}
docker compose exec ontology-api uv run --no-sync python -m build gate2 \
  --db /data/db/ontology_demo.db                           # 볼륨 DB 로 게이트 2 재실행
docker compose exec ontology-api uv run --no-sync python -m build gate3 \
  --db /data/db/ontology_demo.db
```

게이트 1 은 원천을 다시 세므로 컨테이너에서는 돌지 않는다(원천을 서버에 올리지 않는다).

### 4) NPM — 서브도메인 + 인증서

Nginx Proxy Manager 에서 Proxy Host 를 하나 만든다.

| 항목 | 값 |
|---|---|
| Domain Names | `ontology-api.kknaks.cloud` (기존 `profile-api` 와 별개) |
| Scheme / Forward Host / Port | `http` / 호스트 IP / **48080** |
| Websockets | 끔 (폴링이라 필요 없다) |
| SSL | Let's Encrypt 발급 + **Force SSL** |

- **`ontology-mcp` 는 라우팅하지 않는다.** 포트도 열려 있지 않다 — 도구 서버는 자기
  인증이 없어서, 열리는 순간 비밀번호 없이 마스킹 브론즈 행이 읽힌다.
- Basic Auth 는 **걸지 않는다**(SPEC-003 OQ-4) — 폴링·쿠키와 어긋난다. 가드는
  프론트 미들웨어 + 백 세션 쿠키 양쪽이다.

### 5) Vercel — env 한 줄

기존 profile 프로젝트에 라우트 그룹 `app/(ontology)` 가 이미 포함돼 있다.
Project Settings → Environment Variables 에 **Production** 으로 추가하고 재배포한다.

| 키 | 값 |
|---|---|
| `NEXT_PUBLIC_ONTOLOGY_API_BASE` | `https://ontology-api.kknaks.cloud` |

이 값이 **비면 화면이 mock 모드로 뜬다** — 픽스처가 그려지고 실 데이터가 안 보인다.
`NEXT_PUBLIC_` 접두어라 빌드 시점에 번들에 박히므로 **env 변경 후 재배포가 필요하다.**

### 6) 배포 후 확인

1. <https://profile.kknaks.cloud/ontology> → 게이트 화면
2. 비밀번호 입력 → 모니터링. 브라우저 콘솔에 CORS 에러가 없어야 한다
3. 데이터 페이지 브론즈 예약 → 마스킹 표기(`김○○`·`010-****-1234`·`1990-**-**`).
   차트번호는 숫자 그대로이되 숫자가 아닌 값은 `[비정형]` 이다
4. 채팅 R-1(`최근 4주 노쇼율 추이는?`) 완주 — `pending` 표시 → `done` → 인용 칩
5. 채팅 **R-2**(`8월 매출이 왜 떨어졌어?`) 완주 — 전제 교정 → 엣지 칩 클릭 →
   **모니터링 그래프 하이라이트가 답변 엣지와 정확히 같은지**(게이트 5-③).
   로컬 E2E 7-2 와 같은 판정이다
6. 「실시간」 계열 카피 0건 · 기준일 배지가 전 화면에 있는지

### 롤백

- **프론트**: Vercel 에서 이전 배포로 되돌린다(또는 `NEXT_PUBLIC_ONTOLOGY_API_BASE` 를
  지워 mock 으로 내린다). 포트폴리오 표면은 건드리지 않았으므로 영향 범위가 없다.
- **백**: `docker compose down ontology-api ontology-mcp ontology-worker` + NPM Proxy Host
  삭제. 표면이 사라지고 기존 profile 배포·기존 워커는 계속 돈다.
- DB 산출물은 **재빌드로 복원**된다 — 파괴적 마이그레이션이 없다.
