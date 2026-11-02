# Product Map

규칙: `para/projects/project.md`

Tauri 기반 개인 업무 관리 앱. 프론트 Next.js, 백엔드 FastAPI, 타겟은 **macOS · Windows 데스크톱**(macOS 웹뷰가 WebKit 이라 프론트는 Safari 호환 고려). 알림 · 녹음 등 시스템 영역은 Tauri 가 맡는다.

앱은 업무 전용이 아니다 — 홈 · 채팅 · 캘린더 · 내 업무 · 회의록 · 자료함 · 메시지 · 설정 영역이 있고, **영역별 디자인이 완성되는 대로 하나씩 문서화한다.** 각 영역마다 디자인 → 기획(baseline) → 정책(decision) → 스펙(spec) → work 순. 첫 영역은 「내 업무」.

> 제품 전체 지도. 상세 내용은 각 단계 문서에 두고, 여기에는 현재 상태와 어디부터 봐야 하는지만 둔다.

## 코드 레포

코드가 별도 레포에 있으면 위치를 적는다. remote URL 의 SSOT 는 DB `repo` 표다. 여기에는 작업용 local clone 경로를 둔다.

| 항목 | 경로 |
|---|---|
| Remote | `github.com/kknaks/task_management` |
| Local clone | **별도 clone 예정**(2026-09-05 확정) — `kknaks/task_management` 를 받고 config 에 `repos.code` 추가. 이 레포의 `app/back` 은 kknaks_profile 제품이라 쓰지 않는다. 문서/코드 PR 은 레포부터 분리 |
| 문서 SoT | `para/projects/summer-star/task-management/` |

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Design | `00-design/` 완성 패키지(dc.html 8종 + md 00~15) + 프론트 구조 분석 리포트 | 미설계 화면·정정 반영 |
| Baseline | **BASE-001~006 raw** (인증·설정 / 내 업무 / 회의록 / 문서함 / 캘린더 / 메시지함) | 사용자 리뷰 → accepted |
| Decision | **DEC-001~006 proposed** — v1 6영역 정책 완비 | OQ 30건 답(대부분 디자인) → accepted |
| Spec | **SPEC-000~002 draft**(스캐폴딩·로그인/세션·업무 설정) | 배치 ②(003~005 내 업무·문서함) 진행 중 → ③ 회의록 → ④ 캘린더·설정·메시지함 |
| Work | 없음 | spec 뒤 — 코드 스캐폴딩이 첫 work |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | `00-baseline/README.md` |
| 10-decision | `10-decision/README.md` |
| 20-spec | `20-spec/README.md` |
| 30-work | `30-work/README.md` |

## 최근 로그

- 2026-09-01 문서함 생성 — 스택 · 타겟 확정(Tauri / Next.js / FastAPI, iOS · Windows)
