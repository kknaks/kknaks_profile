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
| Decision | DEC-001~005 `accepted` — DB · PII · LLM 경로 · 웹 형태 · 배포 | 미결 5건은 spec 에서 확정 (`10-decision/README.md`) |
| Spec | 없음 | decision 닫혔다 — 분할안 리뷰. 화면 spec 은 디자인 핸드오프 귀환 대기 |
| Work | 없음 | spec 닫힌 뒤 분할안 리뷰 |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | `00-baseline/README.md` |
| 10-decision | `10-decision/README.md` |
| 20-spec | `20-spec/README.md` |
| 30-work | `30-work/README.md` |

## 최근 로그

- 2026-09-02 DEC-001~005 확정 · BASE-001 `accepted`.
- 2026-09-02 BASE-001 등재 — 기록 09(데모 에이전트 앱 구축 계획)를 날것 입력으로.
- 2026-09-02 제품 디렉토리 스캐폴딩. 전체 이력은 `log.md`.
