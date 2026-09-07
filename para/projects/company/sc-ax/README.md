# Product Map — sc-ax

규칙: `para/projects/project.md` (`company/` — `sot: external`)

SCAX 상용 시스템. 고객사(SC) 조직·업무·요청·판단·회의·자료·보고와 내장 AX 대화를 하나의 원장 위에 올리는
회사 제품이다. 기획·스펙·ERD 의 원천은 회사 레포에 있고, **여기에는 내 경험(작업 회고)만 쌓인다.**

## 원천 (회사 레포, read-only)

| 무엇 | 어디 |
|---|---|
| 기획·정책·SPEC·화면·ERD | `MediSolveAIDev/mediness` `main` · `products/sc-ax/` |
| 코드 (modular monolith — FastAPI + SQLAlchemy / React + Vite) | `MediSolveAIDev/ax-workspace` `main` |
| ERD ↔ 구현 대조표 · 디자인 시스템 참조본 | ax-workspace `docs/domain-model.md` · `docs/design/` |

## 이 폴더

```text
sc-ax/
├── README.md   이 지도
└── log/        작업 회고 — YYYY-MM-DD-<slug>.md (orchestration config `summary_dest` 가 여기를 가리킨다)
```

`showcase.md` 는 아직 없다 — 공개 카드로 올릴 만큼 쌓이면 mediness 처럼 만든다.

## 오케스트레이션

- 설정 SSOT: `orchestration/config/projects/sc-ax.json`
- 워커: planner(spec) · backend · frontend · reviewer_spec · reviewer_code
- 진행 중 작업: `orchestration/work/<slug>/_RESUME.md` · 끝난 작업: `orchestration/work/_archive/sc-ax/`
