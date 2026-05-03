---
id: adr-06
type: adr
title: daily/{date}.md = 잔디 SoT, activity.yaml 폐지
status: accepted
created: 2026-05-03
updated: 2026-05-03
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[spec-01-persona-md-format]]"
  - "[[spec-03-activity-scheduler]]"
  - "[[adr-03-scheduler-attribution]]"
  - "[[adr-05-content-pending-enrich]]"
tags: [adr, persona, activity, scheduler, sot]
---

# daily/{date}.md = 잔디 SoT, activity.yaml 폐지

## Summary

기존 `persona/activity.yaml` (잡 자동 생성 단일 yaml 의 `items[]` 배열) 을 폐지하고, 그날의 활동 데이터를 `persona/daily/{YYYY-MM-DD}.md` 의 frontmatter (`auto`, `counts`, `summary`) 에 박는다. 잔디 viz 응답 (`/api/activity`) 은 `persona_loader` 가 부팅 시 모든 `daily/*.md` frontmatter 를 스캔해 derive 한다. 단일 SoT — 같은 날 데이터가 두 파일에 박히는 중복 제거.

---

## 1. Context

- 기존 `spec-01` §4 + `spec-03` §4: 잔디 잡이 매일 `persona/activity.yaml` 의 `items[]` 에 1 entry upsert. 별도 `daily/{date}.md` 는 본인이 박는 narrative (선택).
- 같은 날 데이터가 두 파일에 분리:
  - `daily/2026-05-02.md` — 본인 narrative (선택, 1순위 LLM 입력)
  - `activity.yaml` items[date=2026.05.02] — 잡 자동 생성 (count, kind, summary)
- 문제:
  - 단일 SoT 위배 — 같은 날 정보가 두 곳. 어디가 진짜인지 모호
  - `kind` 1개 제약 — 그날 commit + note + study 다 해도 1 kind 만 박힘. 다양성 손실 (하루의 본질을 잃음)
  - `daily/*.md` 자동 작성은 spec-03 §11 향후 확장으로 미뤘으나, 본인이 매일 narrative 박기 부담 → 대부분 빈 날 → LLM 이 commit subject 만으로 메마른 요약 생성

---

## 2. Decision

### 2.1 SoT 통합

**그날 = `persona/daily/{date}.md` 한 파일**. frontmatter 가 활동 메타 (counts/summary), 본문이 narrative.

```yaml
---
type: daily
date: "2026.05.02"
auto: true                        # 잡 자동 작성 마커
counts:                           # 활동 분포 (deterministic)
  commit: 19
  note: 0
  study: 9
summary:                          # LLM 1줄 종합
  ko: "..."
  en: "..."
---

# 한 일
## commits
- ...
## notes
- ...
## study
- ...

# 회고 / 다음
(LLM 추론)
```

본문 ≤500자 (frontmatter 제외).

### 2.2 잔디 viz derive

`/api/activity` 응답은 `persona_loader` 가 모든 `daily/*.md` 의 frontmatter 를 스캔해 빌드:

```python
items = sorted(
    [{"date": d["date"], "counts": d.get("counts", {}), "count": sum(d.get("counts", {}).values()), "summary": d.get("summary")} for d in daily_list],
    key=lambda x: x["date"],
)
totalCount = sum(i["count"] for i in items)
```

별도 yaml 파일 없음. 부팅 시점 derive — load_all 호출 시 갱신.

### 2.3 본인 작성 vs 자동 생성 충돌

`auto` 필드로 분기:
- `auto: true` — 잡이 갱신 (overwrite). counts/summary 박혀있어야 valid (spec-01 §6.1 강제)
- `auto: false` 또는 `auto` 미박음 — 본인 작성. **잡 skip**. counts/summary 없어도 valid (잔디에선 count=0, summary=null 로 표시)

### 2.4 다양성 보존 — `kind` → `counts` dict

기존 `kind: commit | note | study | null` (1개 선택) → `counts: {commit, note, study}` (분포).

- 활동 분류는 *source 1:1* 매핑 (notes git log → note, contents git log → study, GitHub commits → commit). LLM 추론 불요 → deterministic
- 잔디 viz: `count = sum(counts.values())` 로 강도, 색상은 향후 dominant kind / stripe 등 표현 자유

### 2.5 `count` (single) 호환 키

응답 schema 에 `count: sum(counts.values())` 박아 프론트 잔디 색 강도 로직 (`contrib-grass.tsx:levelColor`) 호환 유지 — 프론트 시각 upgrade 는 별 sprint.

---

## 3. Consequences

### 3.1 영향

| 영역 | 변경 |
|---|---|
| `spec-01` §3.6 daily | frontmatter 확장 (auto/counts/summary) + 본문 ≤500자 룰 |
| `spec-01` §4 activity.yaml | 폐지 — derive 명세로 대체 |
| `spec-03` §1~§5 | LLM 책임 (kind 추론 제거 — counts deterministic), output 경로 (`activity.yaml` → `daily/{date}.md`) 전체 변경 |
| `back/service/persona_loader.py` | `activity` derive 로직 추가, daily schema 검증 갱신 |
| `back/service/jobs/main_job.py` | flow 재구성 (read inputs → counts 계산 → LLM body+summary → daily/{date}.md write) |
| `back/service/jobs/llm.py` | prompt — counts 빼고 body+summary 만 요청 |
| `back/service/jobs/upsert.py` | `activity.yaml` upsert 로직 → `daily/{date}.md` upsert 로 대체 (또는 main_job 안 흡수) |
| `back/service/jobs/git_push.py` | paths = `[daily/{date}.md]` |
| `back/api/routers/activity.py` | derived 응답 (`counts` dict 포함) |
| frontend `types.ts` | `kind` 제거, `counts` 추가 |
| 데이터 마이그레이션 | 기존 `persona/activity.yaml` (mock 데이터) 삭제. 기존 `daily/2026-05-01.md` (본인 작성) keep — `auto` 필드 미박음 = false 로 자동 처리 |

### 3.2 트레이드오프

- **장점**:
  - 단일 SoT (그날 = 한 파일)
  - 활동 다양성 보존 (counts dict)
  - LLM 비결정성 감소 (counts 는 코드 계산)
  - 본인 narrative 와 자동 narrative 가 같은 위치 — 본인 검수/수정 자연스러움
- **단점**:
  - 1년 = 365 파일. `daily/` 디렉토리 비대 (현재 1 → 366+)
  - 프론트 시각화 (kind 별 색) 는 별 sprint 로 미룸 — 데이터 풍부해졌으나 viz 는 현행 유지

### 3.3 백필

기존 365 mock entries 는 wipe (mock 임을 사용자가 confirm). 새 잡이 다음 00:05 부터 daily/{date}.md 1개씩 박음 — 잔디는 며칠간 거의 빈 상태. 필요시 GitHub GraphQL `contributionsCollection` 으로 commit count 만 백필 옵션 (spec-03 §7).

---

## 4. 대안 검토

### 4.1 `activity.yaml` 유지 + `kinds` array

`kind` 를 array 로 확장해 다양성 보존, `daily/*.md` 와는 별도 SoT.

**기각 이유**: 같은 날 데이터가 여전히 두 파일. 단일 SoT 원칙 위배. counts dict 만큼 정보 풍부하지도 않음 (있음/없음만).

### 4.2 `activity.yaml` 유지 + `counts` dict

스키마만 dict 로 바꾸고 파일 구조는 그대로.

**기각 이유**: 4.1 과 같은 단일 SoT 위배. `daily/*.md` 와 `activity.yaml` 동기화 부담 (현재 LLM 이 narrative 와 summary 따로 생성 — 두 곳 일관성 보장 X).

### 4.3 채택안 — daily.md SoT + counts dict

위 §2.

---

## 5. 미해결 / 후속

- 프론트 `contrib-grass.tsx` viz upgrade — kind 별 stripe / dominant color (별 sprint)
- daily 본문 ≤500자 enforcement — LLM prompt 룰 vs 코드 truncate vs validation warning (spec-03 결정)
- `daily/` 비대 — 1년 후 365 파일. 운영 부담 작지만 옵시디언 vault 진입 시 노이즈 ↑. 향후 `daily/2026/` 식 연도 파티션 검토 (별 spec)
