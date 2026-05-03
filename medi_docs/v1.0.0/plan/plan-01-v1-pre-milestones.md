---
id: plan-01
type: plan
title: v1.0-pre 마일스톤 — 셋업부터 production 승격까지
status: draft
created: 2026-05-01
updated: 2026-05-01
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[spec-01-persona-md-format]]"
  - "[[spec-02-api-endpoints]]"
  - "[[spec-03-activity-scheduler]]"
  - "[[spec-04-persona-map]]"
  - "[[adr-01-db-less]]"
  - "[[adr-02-i18n-strategy]]"
  - "[[adr-03-scheduler-attribution]]"
tags: [plan, milestone, setup, deployment]
---

# v1.0-pre 마일스톤

## Summary

문서 단계(planning + spec 4 + adr 3) 완료 후, 코드 + 인프라 단계로 진입. M0(셋업) → M9(production 승격)까지 10 마일스톤. 메모리에 미정으로 남았던 항목 모두 본 plan에서 결정. 마일스톤은 dependency 그래프 — 일부는 병렬 가능.

---

## 1. 미정 항목 결정 (메모리 정리)

| 항목 | 결정 | 근거 |
|---|---|---|
| 페르소나 yaml/md 사전 차단 | **git pre-commit hook**에서 spec-01 §6 검증 실행 (기존 _map 빌드 hook과 합침) | 사용자 PC에서 즉시 피드백. CI도 추가 가능하지만 v1.0-pre엔 hook만 |
| webhook 누락 fallback | **5분 git pull diff check 도입 X** (v1.0-pre엔). 단순 webhook만 | 1인 운영 + 매일 잡 push 1회 → stale 위험 낮음. 향후 webhook 실패 잦으면 추가 |
| 백엔드 git auth | **GitHub deploy SSH key** (write access 체크) | spec-03 §5.1 권장. PAT보다 키 회전·범위 관리 편함 |
| 홈서버 timezone | **KST 박음** (`timedatectl set-timezone Asia/Seoul`) | spec-03 §2.2 TZ 함정 회피. cron + git log 모두 KST 기준 일관 |
| `kknaksss` 계정 본인 거 맞는지 | **사용자 sign-off 필요** (M1에서 확인) | memory에 미확인 박힘. 본인 계정 아니면 spec-03 GH_USERS에서 빼기 |
| `.obsidian/` gitignore | **gitignore에 박음** | 옵시디언 사용자별 설정 — 다른 머신과 분리 (사용자 PC vs 홈서버) |
| `.env` gitignore | **박음** (당연) | secret 누출 방지 |
| `.claude/settings.local.json` gitignore | **박음** | 절대 경로 + 머신별. 이전에 짚었지만 plan에 박혀야 안전 |

---

## 2. 마일스톤 그래프

```
M0 셋업 ─→ M1 페르소나 시드 ─┬─→ M2 백엔드 스켈레톤 ─→ M3 백엔드 확장 ─┬─→ M4 잔디 잡 ──┐
                              │                                            │                │
                              └─→ M6 _map 빌드 + pre-commit ─→ M7 옵시디언 │                │
                                                                            └─→ M5 프론트 ──┤
                                                                                            ↓
                                                                              M8 홈서버 배포 ─→ M9 production
```

병렬 가능: M6은 M1 끝나면 시작. M4/M5는 M3 끝나면 병렬.

---

## 3. 마일스톤 디테일

### 진행 상태 (마일스톤 단위 추적)

| M | 상태 | 시작일 | 완료일 |
|---|---|---|---|
| M0 셋업 | ✅ 완료 (mock) | 2026-05-01 | 2026-05-01 |
| M1 페르소나 시드 | ✅ 완료 (mock) | 2026-05-01 | 2026-05-01 |
| M2 백엔드 스켈레톤 | ✅ 완료 (38 tests + uvicorn 검증) | 2026-05-01 | 2026-05-01 |
| M3 백엔드 확장 | ✅ 완료 (59 tests) | 2026-05-01 | 2026-05-01 |
| M4 잔디 잡 | ✅ 골조 완료 (70 tests · 외부 API stub) | 2026-05-01 | 2026-05-01 |
| M5 프론트 fetcher | 🔄 기반만 (Next.js + lib/{api,types,i18n} + /about mock 1페이지). 디자인 이식·5섹션 풀 페이지·그래프·잔디 미완 | 2026-05-02 | — |
| M6 _map 빌드 + pre-commit | ✅ 완료 (build_persona_map.py + install_hooks.sh + pre-commit 설치) | 2026-05-01 | 2026-05-02 |
| M7 옵시디언 vault | ⏸ 사용자 인프라 작업 (Claude X) | — | — |
| M8 홈서버 배포 | ⏸ 사용자 인프라 작업 (Claude X) | — | — |
| M9 production 승격 | ⏸ 사용자 인프라 작업 + 도메인 (Claude X) | — | — |

> **마커**: ⬜ 미시작 / 🔄 진행 중 / ✅ 완료 / ⏸ 보류
> 마일스톤 시작·완료 시 본 표만 갱신 (헤딩은 안 건드림). 다음 세션에서 한눈에 추적.

---

### M0 — 셋업 (코드 0줄)

**산출물**: 운영 가능한 빈 모노레포 + 환경.

| 작업 | 검증 |
|---|---|
| `.gitignore` 박음 (`.env`, `.claude/settings.local.json`, `.obsidian/`, `back/__pycache__/`, `frontend/node_modules/`, `frontend/.next/`) | `git status` 깨끗 |
| 디렉토리 scaffold: `persona/`, `back/`, `frontend/`, `scripts/` | `ls` |
| 홈서버 timezone KST | `timedatectl` 출력에 `Asia/Seoul` |
| GitHub deploy SSH key 생성 + repo 등록 (write access 체크) | 홈서버에서 `git push` 더미 commit 성공 |
| systemd EnvironmentFile (`/etc/kknaks-api.env`, chmod 600) — `GH_TOKEN` + `RELOAD_TOKEN` (ANTHROPIC_API_KEY는 ADR-04로 불요 — open-kknaks가 host claude CLI 사용) | `sudo cat /etc/kknaks-api.env` 확인 |
| GitHub PAT 발급 (REST + GraphQL API 인증용 — SSH key와 별개. 백필의 GraphQL은 인증 필수). scope = `read:user` + `public_repo` (또는 private 활동 잡으려면 `repo`) | PAT 발급 후 `gh auth status` 또는 `curl -H "Authorization: Bearer $GH_TOKEN" https://api.github.com/user` 200 |
| 본인 PC: 개발용 PAT 별도 발급 → `back/.env` 박음 | `back/.env`에 키 박혀있고 git 추적 안 됨 |

**확인 필요 (사용자 sign-off)**: `kknaksss` GitHub 계정이 본인 거 맞는지. 아니면 spec-03 §2.4 `GH_USERS`에서 제거.

### M1 — 페르소나 시드

**산출물**: 백엔드가 부팅해서 응답할 수 있는 최소 페르소나.

| 작업 | 검증 |
|---|---|
| `persona/_meta.yaml` 작성 (projects 카테고리 3종 + notes 클러스터 5종, spec-01 §5) | yaml.safe_load 통과 |
| `persona/profile.md` 1개 (필수 필드만, spec-01 §3.1) | frontmatter 파싱 성공 |
| `persona/career/stealth-ai.md` 1개 (현재 회사) | display_order=1 |
| `persona/projects/homelab-console.md` 1개 (placeholder) | category=web |
| `persona/notes/python-asyncio.md` 1개 (시드 노트) | group=py |
| `persona/contents/C-001-fastapi-di.md` 1개 (시드 contents) | id=C-001 |
| `persona/daily/2026-05-01.md` 1개 (오늘) | date=2026.05.01 |

**검증**: 위 7개 파일을 백엔드(M2)가 메모리에 로드 시 에러 없음.

### M2 — 백엔드 스켈레톤

**산출물**: FastAPI 부팅 + `load_all()` + `i18n` helper + `/api/me` 동작.

| 작업 | 검증 |
|---|---|
| `back/main.py` FastAPI 앱 + `@startup` `load_all()` | `uvicorn main:app` 부팅 성공 |
| `back/loader.py` — `load_all()` (yaml/md → 메모리 dict, spec-01 §6 검증) | 부팅 시 검증 fail-fast 동작 (의도적 frontmatter 위반 → 부팅 거부) |
| `back/i18n.py` — `i18n(node, lang)` helper (ADR-02 §4.2 + spec-02 §4.1) | 단위 테스트: `{ko, en}` → 한쪽 추출, fallback to ko |
| `/api/me?lang=ko` 핸들러 (spec-02 §3.2) | curl 응답에 `user.handle="kknaks"` |
| 워커 수 검증 (spec-03 §1.2) | `WEB_CONCURRENCY=2 uvicorn ...` → 부팅 거부 |

### M3 — 백엔드 확장 (나머지 엔드포인트)

**산출물**: spec-02의 12개 엔드포인트 모두 동작.

| 작업 | 검증 |
|---|---|
| `/api/site`, `/api/career`, `/api/projects`, `/api/contents`, `/api/contents/{id}` | curl 각각 응답 |
| `/api/notes/graph`, `/api/notes/recent`, `/api/notes/{id}`, `/api/notes/search` | 위키링크 그래프 + 백링크 응답 확인 |
| `/api/activity` (M1 시점엔 `activity.yaml` 없으므로 빈 응답) | `{"activity[]": []}` |
| `apply_i18n` 재귀 wrapper (spec-02 §4.1) | en lang 응답에 한글 안 섞임 |
| 검색 — 메모리 inverted index 빌드 + `/api/notes/search?q=...` | 키워드 매칭 결과 반환 |

### M4 — 잔디 잡 (APScheduler + LLM)

**산출물**: 매일 자동 실행되는 잔디 잡.

| 작업 | 검증 |
|---|---|
| `back/scheduler.py` — APScheduler cron (spec-03 §1.1) | `add_job` 등록 확인 |
| 입력 4개 수집 (`daily.md`, git log notes/contents, GitHub Events) — KST TZ helper (§2.4) | 단위 테스트: KST 자정 직전 push 잡힘 |
| Anthropic Haiku 4.5 호출 (§3.2) | 통합 테스트: mock 입력 → JSON 응답 검증 |
| `upsert_activity` (rolling 365 트림, §4) | 같은 entry 두 번 박아도 결과 동일 |
| `commit_and_push_with_retry` (§5) | 단위 테스트: rebase 충돌 시뮬레이션 |
| 백필 스크립트 (`scripts/backfill_activity.py`, §7) | 1주일 분 백필 → activity.yaml entry 7개 |
| 첫 일별 잡 수동 trigger | activity.yaml에 오늘 entry 1개 박힘 + git push 성공 |

### M5 — 프론트 fetcher (Next.js)

**산출물**: 5섹션 페이지가 백엔드에서 데이터 받아 렌더.

| 작업 | 검증 |
|---|---|
| Next.js scaffold (`frontend/`) — TypeScript, App Router | `npm run dev` |
| `frontend/lib/api.ts` — fetcher (lang 상태 들고 `?lang=` 호출) | `useEffect` + lang 토글 시 refetch |
| `claude_design/` JSX → Next.js 컴포넌트 이식 (mock → 슬롯) | 5섹션 모두 mock 자리에 백엔드 응답 박힘 |
| Notes 그래프 — force-directed 라이브러리 + 위키링크 jump | 노드 클릭 → /api/notes/{id} fetch |
| Contents 영상 + 교안 | YouTube embed + concept/example 섹션 표시 |
| 잔디 — activity[] → 격자 변환 (spec-02 §4.3) | 7×53 격자 렌더 |

### M6 — _map 빌드 + git pre-commit hook

**산출물**: commit 직전 자동 빌드 + 페르소나 검증.

| 작업 | 검증 |
|---|---|
| `scripts/build_persona_map.py` (spec-04 §3) | 직접 실행 → `persona/_map.md` 생성 |
| `scripts/install_hooks.sh` — `.git/hooks/pre-commit` 설치 | `bash scripts/install_hooks.sh` |
| pre-commit hook = `build_persona_map.py` + spec-01 §6 검증 | 의도적 frontmatter 위반 → commit 거부 |
| 백엔드 부팅 시 `build_persona_map()` 호출 (spec-04 §6) | startup 시 `_map.md` 갱신 timestamp 변경 |

### M7 — 옵시디언 vault 셋업

**산출물**: 사용자 PC에서 `persona/`를 옵시디언 vault로 운영.

| 작업 | 검증 |
|---|---|
| 옵시디언에서 `persona/` open vault | `_map.md`가 진입점으로 표시 |
| 그래프 뷰 활성화 | `[[id]]` 위키링크가 노드/엣지로 표시 |
| `.obsidian/` gitignore 박음 (M0에서 박혔으면 OK) | `git status`에 `.obsidian/` 안 보임 |
| README 또는 `persona/README.md`에 옵시디언 셋업 안내 | (선택) |

### M8 — 홈서버 배포 + webhook

**산출물**: 홈서버에서 백엔드 + 프론트 + 웹훅 서빙.

| 작업 | 검증 |
|---|---|
| 호스트에서 `setup.sh` 1회 — Linux Node.js + Claude Code CLI 바이너리를 `.claude-tools/` 에 박음 (ADR-04 §2.2) | `.claude-tools/node/bin/node --version` 출력 OK |
| `claude setup-token` 으로 OAuth 토큰 발급 → `.env` 의 `CLAUDE_CODE_OAUTH_TOKEN` 에 저장 | `cat .env \| grep CLAUDE_CODE_OAUTH_TOKEN` 값 존재 |
| `docker compose up -d` (back + redis + **worker**) | `docker compose ps` 셋 다 healthy, worker 가 broker 큐 listen 로그 출력 |
| nginx reverse proxy (`/api/* → 48000`, `/ → 3000`) | curl https://kknaks.dev/api/me 200 |
| GitHub webhook → `/admin/reload` HMAC 검증 (token 방식 → HMAC 강화, advisor §4.3 nit) | 페르소나 push → 5초 내 reload 발동 |
| HTTPS (Let's Encrypt) | https 접속 가능 |
| Next.js production build + 배포 | `npm run build && npm start` |

### M9 — production 승격

**산출물**: kknaks.dev 도메인에서 v1.0-pre 운영.

| 작업 | 검증 |
|---|---|
| DNS A 레코드 → 홈서버 IP | `dig kknaks.dev` |
| 사이트 외부 접근 확인 | 모바일/외부 네트워크에서 정상 표시 |
| 잔디 잡 첫 production 실행 (자정 기다림) | activity.yaml 자동 push 확인 |
| sign-off (사용자) — "v1.0-pre 완료" 선언 | medi-version-cut 으로 v1.0-pre 박제 |

---

## 4. 의존성 + 추정

| M | 추정 시간 | 차단 의존 |
|---|---|---|
| M0 | 2시간 | — |
| M1 | 1시간 (시드만) | M0 |
| M2 | 1일 | M1 |
| M3 | 2일 | M2 |
| M4 | 2일 (LLM 프롬프트 튜닝 포함) | M3 |
| M5 | 3-5일 (디자인 이식 + Notes 그래프) | M3 |
| M6 | 반나절 | M1 |
| M7 | 30분 | M6 |
| M8 | 1일 | M3 + M5 |
| M9 | 사이클 1회 (자정 기다림) | M8 |

**총 추정**: 1-2주 (병렬 진행 시).

---

## 5. risk + 완화

| risk | 완화 |
|---|---|
| LLM 프롬프트가 의도와 다른 kind 결정 (M4) | 첫 1주는 매일 결과 사용자 검토. 프롬프트 튜닝 후 자동화 |
| Notes 그래프 인터랙션 복잡도 (M5) | 라이브러리 선정 (`react-force-graph` 등) 시점에 PoC 1일 |
| 홈서버 다운타임 (M8) | systemd auto-restart + 외부 monitoring(uptime-kuma 등) — v1.0-pre 범위 X, 향후 |
| 페르소나 yaml 형식 위반으로 백엔드 부팅 실패 | M6 pre-commit hook이 사전 차단 + spec-01 §6 부팅 검증으로 fail-fast |

---

## 6. v1.0-pre 이후 (이 plan 범위 밖)

- v1.1: 동적 기능 (방문자 카운트, 댓글) 도입 시 sqlite 마이그레이션 (ADR-01 §4.3)
- v1.2: 페르소나 비-포트폴리오 활용 (이력서 자동 생성 등)
- v2.0: 검색 임베딩 도입 (notes 만 단위 도달 시)
