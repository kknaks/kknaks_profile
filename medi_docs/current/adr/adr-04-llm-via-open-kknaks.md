---
id: adr-04
type: adr
title: LLM 호출 = open-kknaks (본인 OSS dogfooding) — Anthropic SDK 미사용
status: accepted
created: 2026-05-02
updated: 2026-05-02
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[adr-03-scheduler-attribution]]"
tags: [adr, llm, open-kknaks, dogfooding, redis]
---

# LLM 호출 = open-kknaks — Anthropic SDK 미사용

## Summary

잔디 잡(spec-03 §3) 및 향후 모든 LLM 가공 작업의 호출은 **본인 OSS 라이브러리 [`open-kknaks`](https://pypi.org/project/open-kknaks/)** 를 통한다. PTY 기반 Claude Code CLI 큐 패턴 — Redis broker + ClaudeWorker. Anthropic API SDK는 사용하지 않는다.

---

## 1. Context

`open-kknaks`는 사용자(이건학) 본인이 작성한 OSS 라이브러리:

- **PTY 기반**으로 `claude` CLI를 프로그램에서 호출
- **Redis broker** + worker 패턴 — 비동기 태스크 큐
- 사용자 본인 Claude Pro/Max 구독을 활용 → **API 호출 비용 0**
- 이벤트 스트리밍 (text/tool_use/thinking/progress/cost 등)
- repo: `/Users/kknaks/git/library/claude_code_pty/open_kknaks`

이 프로젝트(kknaks_profile)는 매일 1회 LLM 가공이 필요(spec-03 잔디 잡). 호출 방식 결정 필요.

---

## 2. Decision

### 2.1 LLM 호출 = open-kknaks

```python
from open_kknaks import ClaudeClient, RedisBroker

broker = RedisBroker(url="redis://localhost:46379", namespace="kknaks-portfolio")
await broker.connect()
client = ClaudeClient(broker=broker)

task_id = await client.submit(
    prompt=prompt,
    model="claude-haiku-4-5-20251001",
    timeout=120,
    max_retries=2,
)
task = await client.result(task_id, timeout=120)
result_text = task.result
```

### 2.2 인프라 (홈서버 docker-compose)

- **redis** 컨테이너 (포트 `46379` — 사용자 컨벤션 4-prefix)
- **back** 컨테이너 (포트 `48000`) — FastAPI + APScheduler
- **worker** 컨테이너 — `open-kknaks` ClaudeWorker (claude CLI host에서 실행 — 즉 worker는 host process로, host에 claude CLI 인증 박혀있어야 함)

→ docker-compose 디테일은 spec-05 §4.

### 2.3 Anthropic SDK 의존성 제거

`back/pyproject.toml`에서 `anthropic` 의존성 제거. 대신 `open-kknaks`, `redis` 추가.

---

## 3. Alternatives Considered

### 3.1 Anthropic SDK (직접 API 호출)
- **장점**: 단순. API key 1개. Redis/worker 인프라 불요
- **단점**:
  - 호출당 비용 발생 (월 단위 적지만)
  - 본인 OSS 활용 차별점 X — 일반 패턴
  - 향후 다른 LLM 잡 추가 시 매번 SDK 호출 boilerplate
- **기각 이유**: 본인 OSS dogfooding 가치 + 큐 패턴 재사용성

### 3.2 직접 `claude` CLI subprocess 호출
- **장점**: 의존성 제로. PTY 처리 직접
- **단점**: open-kknaks가 이미 PTY · streaming · retry · queue를 다 처리. 수동 재구현 = 본인 라이브러리 부정
- **기각 이유**: 자체 라이브러리 활용이 자연스러움

### 3.3 (현 결정) open-kknaks
- **장점**: 비용 0, dogfooding 차별점, 큐 패턴 (재시도/스트리밍/우선순위) 빌트인, 향후 잡 추가 단순
- **단점**: Redis + worker 운영 부담. claude CLI 인증 (host에 Pro/Max 로그인) 필요
- **수용 가능한 이유**: docker-compose로 Redis 한 줄. claude CLI 인증은 1회. 차별점 가치 > 운영 부담

---

## 4. Consequences

### 4.1 즉시 효과
- back 의존성 변경 — `anthropic` 제거, `open-kknaks` + `redis` 추가
- 인프라 +1 컨테이너 (redis) — docker-compose로 묶음
- ClaudeWorker는 host에서 운영 (claude CLI 인증 필요) — docker 안 X
- jobs/llm.py 인터페이스 변경 (sync → async, broker 의존)

### 4.2 코드 영향

```python
# back/jobs/llm.py
from open_kknaks import ClaudeClient

async def summarize_activity(
    today, narrative, notes, contents, commits,
    client: ClaudeClient,  # 의존성 주입
) -> dict:
    prompt = _build_prompt(today, narrative, notes, contents, commits)
    task_id = await client.submit(prompt, model="claude-haiku-4-5-...", timeout=120)
    task = await client.result(task_id, timeout=120)
    return _parse_response(task.result)
```

scheduler.py — broker 연결 lifecycle을 main.py lifespan에 박음:

```python
# back/main.py lifespan
@asynccontextmanager
async def lifespan(app):
    ...
    broker = RedisBroker(url=os.environ["REDIS_URL"], namespace="kknaks-portfolio")
    await broker.connect()
    app.state.claude_client = ClaudeClient(broker=broker)
    ...
    yield
    await broker.close()
```

### 4.3 운영 영향

- **홈서버 셋업** (plan-01 M0/M8):
  - `claude` CLI 설치 + Pro/Max 로그인 (host)
  - docker-compose 셋업 (back + redis 컨테이너)
  - ClaudeWorker host process (systemd unit)
- **로컬 dev**:
  - 로컬 Redis (docker run + port 46379) 또는 docker-compose dev profile
  - claude CLI 로컬 설치

### 4.4 위험 + 완화

| 위험 | 완화 |
|---|---|
| claude CLI 인증 만료 | 만료 시 잡 실패 → 다음 날 재시도. 로그 monitoring 필요 (M8) |
| Redis 다운 | docker restart policy `unless-stopped`. 잡은 어차피 매일 1회라 30분 다운 OK |
| open-kknaks 라이브러리 버그 (본인 OSS — 변경 잦음) | back/pyproject.toml에 버전 pin (`open-kknaks==X.Y.Z`). 업그레이드 시 사이트 검증 |
| ClaudeWorker process 죽음 | systemd auto-restart |
| 비용 0이지만 Pro/Max rate limit | 매일 1회 잡이라 한도 초과 가능성 무시 |

### 4.5 향후 확장

같은 패턴으로 다른 LLM 잡 추가 가능:
- notes 자동 태깅 → `client.submit(태그_프롬프트, queue="tag")`
- contents 영상 transcript → 교안 초안 → `client.submit(...)`
- weekly digest → `client.submit(... priority=Priority.LOW)`

→ Redis broker 1개로 다중 큐 운영. dogfooding 사용 사례가 풍부해짐.

### 4.6 OSS 의도 정합

이 프로젝트(kknaks_profile)는 향후 OSS 가능성 검토 중 (planning-01 §외부 활용). open-kknaks 사용은:
- 본인 OSS를 본인 다른 OSS에 dogfooding — OSS 생태계 자연스러움
- 단, kknaks_profile을 fork한 사람은 본인 Claude Pro/Max 구독 필요 — 진입 장벽
- Anthropic SDK fallback을 향후 옵션으로 둘지는 v1.0-pre 후 재검토
