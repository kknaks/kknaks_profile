# Product Map — ax-clinic-project

규칙: `para/projects/project.md` (`company/` — `sot: external`)

병원 AX 전환 사업(회사 업무)의 문서 작업. 지점별 AX 전환 전략(명동 · 안양)을 세우는 일이다 —
현황 · 조사 · KPI · 과제 · 실행계획, 인터뷰 정리. 문서의 원천은 사업 레포 `ax-clinic-project` 이고,
**여기에는 내 경험(작업 회고)만 쌓인다.**

## 원천 (사업 레포, read-only)

| 무엇 | 어디 |
|---|---|
| 문서 레포 — 자체 PARA 구조 · 문서 작성 규칙 · 검사 훅(`check_docs.py`) | `kknaks/ax-clinic-project` `main` (로컬 `/Users/kknaks/git/ax-clinic-project`) |
| 입구 · 규칙 | 레포 `README.md` → `para/para_map.md` · `AGENTS.md` · `rules/document-rules.md` |
| 진행 중 프로젝트 | `para/projects/clinic-myeongdong-ax/`(명동 — 전략 수립) · `para/projects/clinic-anyang-ax/`(안양 — 스캐폴딩) |
| 메디니스 제품 문서 | `para/projects/mediness/products/` — 메디니스 레포 서브모듈, 읽기 전용 |

## 이 폴더

```text
ax-clinic-project/
├── README.md   이 지도
└── log/        작업 회고 — YYYY-MM-DD-<slug>.md (orchestration config `summary_dest` 가 여기를 가리킨다)
```

`showcase.md` 는 아직 없다.

## 오케스트레이션

- 설정 SSOT: `orchestration/config/projects/ax-clinic-project.json`
- 워커: writer(사업 레포 문서) · researcher · reviewer (역할: `orchestration/roles/ax-clinic-project/`)
- 진행 중 작업: `orchestration/work/<slug>/_RESUME.md` — 초기 구성 `clinic-ax-bootstrap` 진행 중
