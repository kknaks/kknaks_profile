# cc back 배포 준비 결과 보고 — Dockerfile · GitHub Actions arm64 → GHCR (DEC-003)

## 상태: done

## 수행 — 파일

커밋 · push 없음.

| 파일 | 내용 |
|---|---|
| `cc/back/Dockerfile`(새) | 2단계: `python:3.12-slim` + uv(`ghcr.io/astral-sh/uv:0.9`)로 `uv sync --frozen --no-dev` → 실행 단계 `python:3.12-slim`, **비루트 uid 10001**, 포트 8600, `uvicorn app.main:app --host 0.0.0.0 --port 8600`, 진입 스크립트 |
| `cc/back/.dockerignore`(새) | `data/` · `.env*`(example 빼고) · `.venv` · 캐시 · `tests/` · README — **데이터 · 비밀은 이미지에 없음** |
| `cc/back/docker-entrypoint.sh`(새) | `python -m app.seed ensure` → `exec uvicorn …`. 실패해도 서버는 뜬다 |
| `cc/back/app/seed/__main__.py` | `ensure` 하위 명령 — DB 에 상태(version > 0)가 있으면 건너뜀, 비었으면 `seed.json`(같은 폴더에 있으면) 으로 채우거나 시나리오로 build |
| `cc/back/app/seed/build.py` | 이벤트 파일 **평평한 꼴도 읽음** — 쿠버네티스 Secret 은 하위 폴더(`events/`)를 못 만든다: `event-<scheduleId>.json` · `events.json`({id: 이벤트}) · 기존 `events/` 폴더 셋 다 |
| `.github/workflows/cc-back-image.yml`(새, 레포 루트) | `cc/back/**` · 워크플로 파일 변경 push · 수동 실행 → `ubuntu-24.04-arm` 러너 · buildx · `linux/arm64` → **`ghcr.io/kknaksss/cc-prototype-back:${{ github.sha }}`** 만(latest · main 태그 없음). `permissions: packages: write` · GHA 캐시 |
| `cc/back/tests/test_deploy.py`(새) | 평평한 이벤트 · `seed ensure`(빈 DB → build, 있으면 건너뜀) · 헬스 |
| `cc/back/README.md` | 「배포」 절 — env · 마운트 표 |

`GET /api/health` 는 이미 있었다(`200 {"ok": true, "version": n}`).

## 이미지 · env · 마운트 (infra 워커용)

| 항목 | 값 |
|---|---|
| 이미지 | `ghcr.io/kknaksss/cc-prototype-back:<커밋 sha>`(linux/arm64) |
| 포트 | 컨테이너 8600(HTTP · SSE `/api/events` · WS `/api/interpret`) |
| 실행 사용자 | uid/gid 10001 — PVC 쓰기 권한 필요(`fsGroup: 10001` 권장) |
| 헬스 | `GET /api/health` → 200 (readiness · liveness) |
| 경로 | ingress `/api` → back(앱 경로가 `/api/...` 라 **경로 그대로 전달**, rewrite 없음). SSE · WS 가 끊기지 않게 proxy 버퍼링 끄기 · 읽기 타임아웃 길게 권장 |

| env | 이미지 기본값 | 무엇을 넣나 |
|---|---|---|
| `CC_DB_PATH` | `/data/cc.db` | **PVC** → `/data`(읽기 · 쓰기). `seed.json` · 백업도 같은 폴더에 생긴다 |
| `CC_SCENARIO_DIR` | `/scenario` | **Secret** 마운트(읽기 전용) — 키 `seed.json` + 이벤트 키 `event-<scheduleId>.json`(평평하게) 또는 `events.json`. 지금 시나리오 크기 약 150 KB(Secret 1 MiB 안) |
| `CC_KOS_STAFF_PATH` | `/secrets/kos-staff/kos-staff.json` | **Secret** 마운트(읽기 전용) — 키 `kos-staff.json`(직원 이름 · 이메일 가짜로 바꾼 것, D-04). 약 16 KB |
| `SONIOX_API_KEY` | 없음 | **Secret** env(통역) |
| `CC_FRONT_ORIGIN` | `https://ccc.medisolveai.xyz` | 그대로. 같은 출처라 CORS 는 사실상 안 쓰이고 통역 WS 의 Origin 검사에 쓰인다 |
| `CC_RISK_WORDS` | 코드 기본값 | 선택 |

## 검증

| 항목 | 결과 |
|---|---|
| 로컬 `docker build`(arm64 맥) | 성공 |
| 이미지 안 `data/` | **없음**(`/app` = `app` · `pyproject.toml` · `uv.lock` · `.venv`), `id` = uid 10001 |
| 임시 포트 18620 컨테이너(시나리오 · 직원을 **평평한 Secret 꼴**로 읽기 전용 마운트 + 빈 `/data`) | `/api/health` **200** · 첫 시작에 시나리오로 시드(예약 8 · 직원 14 · 이벤트 8) · `/api/board` 예약 8 · 직원 14 · **재시작 때 「DB 에 상태가 있어 건너뜀」** · CORS 사전 요청 `Access-Control-Allow-Origin: https://ccc.medisolveai.xyz` |
| 마운트 없이(18621) | 시드 실패 로그(「시나리오 seed.json 이 없어요 … CC_SCENARIO_DIR」) 뒤에도 `/api/health` 200 |
| 끝난 뒤 | 두 테스트 컨테이너 삭제 · 18620/18621 비어 있음 · 8600 · 3600 안 건드림 |
| `uv run pytest` | **53 passed** |
| `uv run ruff check .` | **All checks passed** |
| GitHub Actions | push 안 해서 **pending**(코디가 push 하면 돈다) |

## 이슈 · 코디가 확인할 것

1. **이벤트 파일 이름** — Secret 에 넣을 때 `events/<id>.json` 을 `event-<id>.json` 으로 평평하게(또는 하나의 `events.json`). back 은 셋 다 읽는다
2. 시드는 **DB 가 비었을 때 한 번만** 만든다 — 시나리오 · 직원 Secret 을 바꾸면 PVC 의 `cc.db` · `seed.json` 을 지우고 재시작(또는 `kubectl exec … python -m app.seed build` 후 [초기화])
3. 워크플로는 `cc/back/**` 이 바뀐 **모든 브랜치 push** 에서 돈다(브랜치 제한 없음 — 필요하면 `branches:` 추가)
4. GHCR 패키지가 처음 생기면 기본 private 일 수 있다 — 클러스터에서 당기려면 public 으로 바꾸거나 pull secret
5. DEC-003 위험 그대로 — 공개 주소라 통역(Soniox 과금)을 누구나 쓸 수 있다
