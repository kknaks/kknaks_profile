# Product Map — ontology-demo

규칙: `para/projects/project.md`

피부과 의원 데이터를 메달리온(브론즈→실버→골드) + 온톨로지 그래프로 쌓고, AI 에이전트가
관계를 근거로 답하는 데모 앱. 기록 01~09(`para/resources/note/ontology/`)를 계약으로 굳혀
구현으로 내리는 단계다.

> 제품 전체 지도. 상세 내용은 각 단계 문서에 두고, 여기에는 현재 상태와 어디부터 봐야 하는지만 둔다.

## 코드 레포

| 항목 | 경로 |
|---|---|
| Remote | `github.com/kknaks/kknaks_profile` (브랜치 `ontology-demo`) |
| 백엔드 | `app/ontology-agent/` (FastAPI + SQLite + open-kknaks) |
| 프론트 | `app/front/` 통합 3페이지 — 채팅 · 모니터링 · 데이터 |
| 문서 SoT | `para/projects/summer-star/ontology-demo/` (이 디렉토리) |
| 원천 데이터 | `reference/ontology_demo/` — **gitignore, 로컬 전용 (PII)** |

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | BASE-001 `accepted` — 기록 09 등재 | 닫힘 (DEC-001~005 로 내려감) |
| Decision | DEC-001~005 `accepted` — DB · PII · LLM 경로 · 웹 형태 · 배포 | 미결 5건 중 **4건 닫힘**. 잔여 1건(DEC-004 OQ-1 화면 상세)의 실체였던 디자인 조정 20건이 design-fix 로 해소 — 계약은 SPEC-004 |
| Spec | **SPEC-001~005 전건 `ready`** — 데이터 계층 · 도구 4종 · API/채팅 · **화면 3페이지** · 에이전트 루프 | 계약 확정. 정본 대조·디자인 조정 반영 완료 |
| Work | **WORK-001~005 `todo`** — 데이터 기반 · 도구/API · 에이전트/채팅 · 프론트 3페이지 · 통합/배포 | phase 단위 발주(총 22 phase). spec 계약이 전부 `ready` 라 착수 선행조건 없음 |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | `00-baseline/README.md` |
| 10-decision | `10-decision/README.md` |
| 20-spec | `20-spec/README.md` |
| 30-work | `30-work/README.md` |

## 최근 로그

- 2026-09-02 design-fix 반영 — SPEC-004 `ready`(디자인 조정 20건 전건 해소) · 좌표 25행 전건 배정.
- 2026-09-02 WORK-001~005 작성(WP 5건 · 22 phase) — 게이트 5종 배치 완료.
- 2026-09-02 SPEC-004 작성(화면 3페이지) · SPEC-001/002/003/005 개정 → `ready`.
- 2026-09-02 SPEC-001·002·003·005 작성(draft) — SPEC-004(화면)는 결번.
- 2026-09-02 DEC-001~005 확정 · BASE-001 `accepted`.
- 2026-09-02 BASE-001 등재 — 기록 09(데모 에이전트 앱 구축 계획)를 날것 입력으로.
- 2026-09-02 제품 디렉토리 스캐폴딩. 전체 이력은 `log.md`.
