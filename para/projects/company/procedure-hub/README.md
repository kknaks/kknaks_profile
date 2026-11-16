# Product Map — procedure-hub

규칙: `para/projects/project.md` (`company/` — `sot: external`)

시술 지식을 조회·관리하고 CHARTY 등 소비 서비스에 API 로 제공하는 내부 서비스 `MediSolveAIDev/PROCEDURE-HUB`.
기획·코드의 원천은 회사 레포에 있고, **여기에는 내 경험(작업 회고)만 쌓인다.**

## 원천 (회사 레포, read-only)

| 무엇 | 어디 |
|---|---|
| 코드 — backend FastAPI · uv · Alembic / frontend Next.js · BFF | `MediSolveAIDev/PROCEDURE-HUB` `release/v1.2.0` (로컬 `/Users/kknaks/git/PROCEDURE-HUB`) |
| 레포 규칙 · 설계 · API 계약 · 배포 | 레포 `AGENTS.md`(스킬 `.agents/skills/`) · `docs/guides/` · `docs/README.md` |
| 기획·스펙 — baseline · decision · SPEC · WP | 메디니스 문서 레포 `MediSolveAIDev/mediness` `products/procedure-hub/` (로컬 `/Users/kknaks/git/harness_works/mediness-mediness`) |

문서 레포는 v1.1.0(2026-07-03)에서 멈춰 있다. v1.2.0 코드와 얼마나 차이 나는지는 아직 대조하지 않았다.

## 이 폴더

```text
procedure-hub/
├── README.md   이 지도
└── log/        작업 회고 — YYYY-MM-DD-<slug>.md (orchestration config `summary_dest` 가 여기를 가리킨다)
    ├── 2026-10-28-silver-step1-product-normalization.md   phub-recommend 실버 1단계(제품 원장) 정규화 과정 — 전후 비교 · 교육 자료
    ├── 2026-10-28-silver-step2-family.md                  phub-recommend 실버 2단계(계열) 정의 · 제품→계열 연결 — 전후 비교 · 규칙 · 계열 판정 스킬 근거
    ├── 2026-10-28-silver-step3-site.md                    phub-recommend 실버 3단계(부위) 노드 53 · 이름 칸 부위 문자열 → 노드 — 전후 비교 · 규칙 · 부위 판정 스킬 근거 · 검수 루프 회고
    ├── 2026-10-28-silver-step4-technique.md               phub-recommend 실버 4단계(기법) 노드 24 · 표현 181 행선지 · 앞서 한 원천 21 행선지 지도 — 전후 비교 · 규칙 · 틀린 것
    ├── 2026-10-29-silver-step5-unit.md                    phub-recommend 실버 5단계(단위 시술) 키 143 · 원장 521 행선지 · 「클리닉 시술은 전부 단위 시술」(계열 24 · 기법 25) · 제품 상속 기법 근거 — 전후 비교 · 규칙 · 틀린 것
    ├── 2026-10-29-silver-step6-package.md                 phub-recommend 실버 6단계(패키지) 입력 36 → 패키지 24 · 구성 엣지 49 · 슬롯 8 · 「패키지」 두 뜻(사이트 추천 패키지 = 7단계) — 전후 비교 · 규칙 · 틀린 것
    ├── 2026-10-29-silver-step7-concern.md                 phub-recommend 실버 7단계(고민 · 목적 · 추천 조합) 고민 노드 55 · 대응표 249(사람 확인 88) · 목적 13 · 엣지 523 · 추천 조합 79 · 5단계 보강(키 162 · 계열 27 · 기법 26) — 전후 비교 · 규칙 · 틀린 것 · 추가: 게이트 → 규칙(R12~R20 · 피부결 · 잇몸미소 · 대응 249 전부 자동)
    ├── 2026-10-29-silver-step8-relation.md                phub-recommend 실버 8단계(관계 · 확인 조건 · 안전 · 근거) 엣지 219 · 주장 395 · 충돌 19+76+1 · 조건 53/373 · 피함 5 · 합병증 65 · 주의 22 · 근거 188 · 숫자 칸만 읽기 — 전후 비교 · 규칙 · 틀린 것
    ├── 2026-10-30-silver-step7-site-rules.md              phub-recommend 7단계 보강 — 부위 규칙 R21~R27 · 판단 ①~③ · 전수 눈검(이상함 105 · 확인 필요 36 → 0) · W2 「후보 전부」 폐기 · 엣지 537 → 427 — 전후 비교 · 규칙 · 틀린 것
    ├── 2026-10-30-semantic.md                             phub-recommend 시맨틱 정의 — 노드 13 · 엣지 21 · 용어 47 · 사전 1962 · id 대응 1071 · 상속 9 · 합병증 65 → 35 · 부작용 72 · B1~B12 · U1~U3 — 조사 → 결정 → 반영 · 틀린 것
    ├── 2026-10-30-quality-eval.md                         phub-recommend 허브 품질 측정 · 수정 — 측정 4 · 목표 6 · 1차 1/6(I-01 31문항 중 맞음 4) · 원인 14 → R28~R32 · 사전 · 안전 원문 · CC 슬롯 · 3차 6/6(CC 없음 4/6) · 다파장 · 같은 질문 전후 · 틀린 것(사람이 찾은 오류 · 측정기 오류 · 순서)
    └── 2026-10-30-gold-decisions.md                       phub-recommend 골드 규칙 판단 — 골드 = 규칙 적용 그래프 + 허브 도구(카드 묶음 아님 · 허브 고정 · 병원 연결 층은 앱) · 조사 G1~G17 · 의도 12 · 도구 9 · U-1 ② · 판단 ①~⑤ · D-01~D-14(D-08 정정) · U-2 · U-3 앱 단계 · KOS 기록만 · 다음 SPEC-005
```

## 오케스트레이션

- 설정 SSOT: `orchestration/config/projects/procedure-hub.json`
- 워커: planner · backend · frontend · reviewer_spec · reviewer_code (역할: `orchestration/roles/procedure-hub/`)
- 진행 중 작업: `orchestration/work/<slug>/_RESUME.md`
