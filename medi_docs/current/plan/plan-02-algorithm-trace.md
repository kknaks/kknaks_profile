---
id: plan-02
type: plan
title: 알고리즘 트레이서 마일스톤 — 시드부터 일일 자동 생성까지
status: draft
created: 2026-05-06
updated: 2026-05-06
sources:
  - "[[planning-03-algorithm-daily-tab]]"
  - "[[spec-07-algorithms-trace]]"
  - "[[spec-03-activity-scheduler]]"
  - "[[spec-01-persona-md-format]]"
  - "[[adr-08-logic-quiz-format]]"
  - "[[adr-09-trace-yaml-via-settrace]]"
  - "[[plan-01-v1-pre-milestones]]"
tags: [plan, milestone, algorithms, neetcode, scheduler]
---

# 알고리즘 트레이서 마일스톤

## Summary

planning-03 + spec-07 + ADR-08·09 박힌 후 코드·운영 단계. 5 마일스톤 (M0 시드 → M4 출시·자동 생성). 본 plan 은 plan-01 (portfolio v1.0-pre) 의 *후속·병렬 트랙* — 백엔드/프론트 인프라는 plan-01 M2/M3/M5 에서 이미 박힘, 본 plan 은 그 위에 algorithm 카테고리 + 잡 + UI 추가.

---

## 1. 마일스톤 그래프

```
M0 시드 + 형식 박제 ✅ ─→ M1 백엔드 loader + API ─┬─→ M2 프론트 라우트 ─┐
                                                  │                       │
                                                  └─→ M3 스케쥴러 잡 ──────┤
                                                                            ↓
                                                              M4 출시 · NeetCode 150 시퀀스
```

병렬: M2 와 M3 은 M1 끝나면 동시 진행 가능. M3 은 plan-01 M4 (잡 인프라) 의 redis broker · open-kknaks worker 재사용.

---

## 2. plan-01 과의 관계

| 인프라 | plan-01 에서 박음 | 본 plan 에서 활용 |
|---|---|---|
| FastAPI 부팅 + `load_all()` | M2 | M1 — `algorithms/` 카테고리 추가 |
| Next.js scaffold + `lib/api.ts` | M5 | M2 — `/algorithms` 라우트 추가 |
| APScheduler + redis broker + open-kknaks worker | M4 | M3 — `algorithm` 큐 잡 등록 |
| pre-commit hook + `_map.md` 빌드 | M6 | 그대로 (algorithms 도 자동 인식) |

본 plan 은 *새 인프라 X*. 기존 인프라 위에 새 카테고리·잡·라우트만 추가.

---

## 3. 마일스톤 디테일

### 진행 상태

| M | 상태 | 시작일 | 완료일 |
|---|---|---|---|
| M0 시드 + 형식 박제 | ✅ 완료 | 2026-05-05 | 2026-05-06 |
| M1 백엔드 loader + API | ✅ 완료 (18 tests · 129 total) | 2026-05-06 | 2026-05-06 |
| M2 프론트 라우트 + 4섹션 | ✅ 완료 (build 통과 · 모바일 검증) | 2026-05-06 | 2026-05-07 |
| M3 스케쥴러 잡 (5단계) | ⬜ 미시작 | — | — |
| M4 출시 · NeetCode 150 시퀀스 | ⬜ 미시작 | — | — |

> **마커**: ⬜ 미시작 / 🔄 진행 중 / ✅ 완료 / ⏸ 보류

---

### M0 — 시드 + 형식 박제 ✅

**산출물**: planning + spec + ADR + 시드 1개 박제. 형식 라운드트립 검증 완료.

| 작업 | 검증 |
|---|---|
| planning-03 박음 (4 섹션, source-first, core region, 결정 박힘 박스) | medi_docs frontmatter 통과 |
| spec-07 박음 (`## Data` 단일 yaml 블록 + 5단계 파이프라인) | sources lineage 일관 |
| ADR-08 (논리 구조 quiz format), ADR-09 (Trace 단순화) | 두 ADR 의 source-first 정합 |
| spec-03 §11 신설 (`neetcode-canonical` 잡 인터페이스) | 잔디 잡과 큐 분리 명시 |
| 디자인 시안 in-place 갱신 — `proto-algorithms.jsx` 4 섹션 | 시안 동작 확인 (Pre-solve · Logic · Trace) |
| 시드 `persona/algorithms/A-001-two-sum.md` | yaml round-trip 파싱 통과 (frontmatter + ## Data) |

**완료**: 2026-05-06 (commit `e85cbea`).

---

### M1 — 백엔드 loader + read API

**산출물**: `algorithms/` 카테고리를 `load_all()` 이 인식 + 2개 API 엔드포인트 응답.

| 작업 | 검증 |
|---|---|
| `back/loader.py` — `algorithms/A-NNN-slug.md` 파싱 함수 추가 (frontmatter + `## Data` yaml 블록 분리) | 단위 테스트: A-001 시드 파싱 → frontmatter 13 키 + data 6 키 |
| 메모리 dict 에 `algorithms` 키 추가 (`{id: {frontmatter, data}}`) | `load_all()` 부팅 → A-001 메모리 적재 |
| `GET /api/algorithms?lang=ko` 핸들러 — 목록 + `today` (frontmatter `today: true` 인 항목, 1개 보장) | curl 응답에 `algorithms[].id="A-001"` 포함 |
| `GET /api/algorithms/{id}?lang=ko` 핸들러 — 디테일 + `newer`/`older` 인접 id (`date` desc 정렬) | curl `/api/algorithms/A-001?lang=ko` 200 + 6 data 키 |
| `apply_i18n` 재귀 wrapper 가 `{ko,en}` 객체 평탄화 | en 응답에 한글 안 섞임 |
| spec-02 §2 엔드포인트 표 행 2 추가 | 같은 PR 안에 |
| 단위 테스트 — algorithms 카테고리 누락 시·잘못된 yaml 시 fail-fast | spec-01 §6 동일 톤 |

**의존**: plan-01 M2 (FastAPI + `load_all`) 완료 가정.

**Exit criteria**: 백엔드 부팅 → A-001 메모리 적재 + 두 엔드포인트 200 응답.

---

### M2 — 프론트 라우트 + 4섹션 컴포넌트

**산출물**: `/algorithms` 라우트 + 상세 페이지 4 섹션 (Problem · Pre-solve · 논리 구조 · Solve·Trace) production.

| 작업 | 검증 |
|---|---|
| Next.js 라우트 — `frontend/app/algorithms/page.tsx` (목록) + `frontend/app/algorithms/[id]/page.tsx` (상세) | `npm run dev` → 두 라우트 200 |
| `claude_design/.../proto-algorithms.jsx` JSX 컴포넌트 이식 (mock data → fetcher 호출) | mock 자리에 백엔드 응답 채워짐 |
| `PreSolvePanel` (Clarifying·Approach 4단계 quiz) — 세션 메모리만 (stateless) | 새로고침 시 초기화. 정답 공개 후 ▾ chevron 으로 이유 펼침 |
| `LogicPanel` (slot quiz, format=slot 만 분기) — `format` 외 값은 `<UnsupportedFormat />` | DP 패턴 (state-first) 도달 시 graceful 안내 |
| `TracePanel` (코드 + cases + worked_example 펼침 + Solution 펼침) — step-by-step UI 없음 | 모바일 한 손 엄지 인터랙션 검증 |
| 모바일 우선 레이아웃 — `m-stack` 클래스 활용. 데스크탑 동일 컴포넌트 반응형 | 360px 폭에서 전 섹션 정상 |
| `proto-shell.jsx` TopNav 의 `algorithms` 탭 라벨 — `algorithms` 유지 | 디자인 결정 박힘 (planning §8) |

**의존**: M1 (API 응답) + plan-01 M5 (Next.js + `lib/api.ts`).

**Exit criteria**: 모바일에서 `/algorithms/A-001` 접근 → 4 섹션 모두 인터랙션 가능. 학습자 입력은 세션 메모리만 (서버 mutation X).

---

### M3 — 스케쥴러 잡 (5단계 파이프라인)

**산출물**: 매일 23:00 UTC 발동 → `persona/algorithms/A-NNN-slug.md` 1개 자동 박힘.

| 작업 | 검증 |
|---|---|
| `back/scheduler.py` 에 `neetcode-canonical` 잡 등록 (spec-03 §11.1) | `add_job` 등록 확인 |
| `back/jobs/algorithms/fetch.py` — LeetCode GraphQL + neetcode-gh raw fetch + redis 캐시 (단계 a, b) | 단위 테스트: A-001 slug → fields 회수 |
| `back/jobs/algorithms/normalize.py` — statement trim · cases 추출 · core region 라인 set 판별 (단계 c) | 단위 테스트: 휴리스틱 (loop body / 재귀 body / 분기) per 패턴 검증 |
| `back/jobs/algorithms/llm_fillgaps.py` — open-kknaks 1 호출 (clarifying·approach·logic distractor·trace worked_example·solution followup) | 통합 테스트: mock prompt → JSON 응답 검증 |
| `back/jobs/algorithms/write.py` — frontmatter + `## Data` yaml 조립 + `today` mutation (이전 today=true → false) (단계 e) | 단위 테스트: 두 번 실행 시 멱등성 |
| 시퀀스 상태 redis (`kknaks-portfolio:neetcode:next_index`) 읽기·쓰기 | 단위 테스트: 잡 후 next_index += 1 |
| `commit_and_push_with_retry` 재사용 (spec-03 §5) — paths = 새 md + 이전 today 갱신된 paths | 잔디 잡 git push 인프라 그대로 |
| 첫 잡 수동 trigger (`target_date=2026-05-06`) | A-002 (NeetCode 150 의 다음 slug) 박힘 + git commit |

**의존**: plan-01 M4 (잡 인프라) 의 redis broker · open-kknaks worker 재사용.

**Exit criteria**: 수동 trigger → A-002 자동 박힘 + commit. 다음 날 23:00 UTC 자동 발동 검증.

---

### M4 — 출시 · NeetCode 150 시퀀스 시작

**산출물**: production 도메인에서 `/algorithms` 접근 가능. 매일 1 항목 자동 누적.

| 작업 | 검증 |
|---|---|
| 홈서버 docker-compose 갱신 (back + redis + worker, plan-01 M8 위에) — `algorithm` 큐 등록 | docker-compose up → 잡 ready |
| Vercel 프론트 배포 — `/algorithms` 라우트 | 도메인 접근 200 |
| 모바일 실기 검증 — 지하철 환경 (3G 시뮬레이션, 한 손 엄지) | Pre-solve · Logic · Trace 모두 동작 |
| 시퀀스 상태 초기화 — redis `next_index = 1` (A-001 시드는 이미 박혔으므로 1 이 다음) | 첫 잡이 A-002 박음 |
| 첫 자동 발동 (23:00 UTC) | A-002 박힘 + 잔디 잡이 다음 날 commit count +1 |
| 검수 — 첫 7일 (Day 02 ~ Day 08) LLM 출력 품질 (clarifying 자연성 · distractor 적절성 · worked_example 정확성) | 매일 1 확인. 부자연스러운 항목은 수동 재생성 트리거 |

**의존**: M2 + M3 + plan-01 M8 (홈서버 배포) + M9 (production 도메인).

**Exit criteria**: 7 일 연속 자동 박힘 + 7 일 모두 모바일 학습 가능 + 잔디에 자연스럽게 +7.

---

## 4. 미정·후속 (이 plan 범위 밖)

- **`logic.format` 의 `ordering`·`state-first` 추가** — adr-08 후속. ~Day 50 (tree·graph 도달) / ~Day 100 (DP 도달).
- **라우트 prefix `A-` → `T-` (Trace) 변경** — planning-03 §9 row 5. 시퀀스 진행 후 검토.
- **노트 승격·Notes 블록 부활** — planning-03 §5 의 *다음 버전*. v2 plan 신설 시.
- **`logic` 컴포넌트 quiz format 분기 (ordering·state-first)** — M2 의 `<UnsupportedFormat />` 부활 시점.
- **trace 정확도 issue 부활** — adr-09 의 sys.settrace 옵션 — 매일 누적 30+ 일 후 felt 시 별도 ADR.
