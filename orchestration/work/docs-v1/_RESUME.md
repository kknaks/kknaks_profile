
# 재개 노트 — docs-v1 (task-management)

> **작업 단위 = 이 워크트리(브랜치 task-management-app) 1개 = 이 slug 1개.**
> v1 문서 파이프라인(디자인 분석 → 영역별 baseline+decision → spec)이 전부 여기서 돈다.
> 워커 추가 발주는 새 slug 를 파지 않고 `new-work.sh task-management docs-v1 --workers <w>` 로 이 폴더에 브리프를 더한다.

**지금**: 전체 계획 확정(아래 §0) — Phase 1-1 인증·설정 writer 발주 대기
**다음**: 남은 결정 3건(§1) 닫히는 대로 writer 발주 (BASE-001+DEC-001 인증·설정)

세팅: `scripts/new-work.sh task-management docs-v1` · 설정 SSOT `config/projects/task-management.json`
코디handle: `term_e6d07c2f-a88d-46b4-9d0c-3ed44e6c90a2`

## 워크트리

- `docs`: 코디 워크트리 공유 (`workspace: coordinator`) — `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app` (branch `task-management-app`, base `origin/main` → PR `main`). 워커 개별 워크트리 없음.

## 0. 계획 (2026-09-03 사용자 합의)

범위: 현 패키지 6영역. 홈·채팅 제외(디자인 재입수 시), 자료함은 문서함 확정안.
영역당 문서 세트: **기획서 BASE**(템플릿+왜+기능명세+인/아웃바운드) + **정책서 DEC**(8절, CRUD 규약) → **기능정의서 SPEC**(기존 템플릿). 영역 하나씩 직렬.

### Phase 1 — 영역별 BASE+DEC (writer, 영역당 발주 1회)

| # | 영역 | 문서 | 순서 근거 | 상태 |
|---|---|---|---|---|
| 1 | 인증·설정 | BASE-001+DEC-001 | 프로젝트·유형 관리가 설정 소관 — 업무가 참조하므로 최우선 (사용자 확정) | 대기 |
| 2 | 내 업무 | BASE-002+DEC-002 | 원자 도메인. 설정의 프로젝트·유형 소비 | |
| 3 | 회의록 | BASE-003+DEC-003 | 내 업무 생성/수정 규약 소비 | |
| 4 | 문서함 | BASE-004+DEC-004 | 업무·회의록의 첨부 대상 (확정안 기준) | |
| 5 | 캘린더 | BASE-005+DEC-005 | 업무·회의록 드로어 재사용 — 늦을수록 결정 적음 | |
| 6 | 메시지함 | BASE-006+DEC-006 | 이 차례에 범위(Q-35: AI 추출 포함 여부) 결정 후 진행 | |

영역 사이클: writer 발주 → 코디 검증 → 사용자 리뷰·OQ 답 → accepted → 다음 영역.
임의 결정 금지 — 닫히지 않은 것은 전부 Open Questions.

### Phase 2 — SPEC

- 진입 게이트(사용자): Q-28 Tauri 정적 export · Q-33 shadcn 도입+토큰 매핑 · Q-34 실측좌표 vs 유동
- SPEC-000 공통 기반(토큰·셸·오버레이 3종)부터 → 영역별 SPEC 은 accepted 정책서 순서대로

### Phase 3 — 코드

- `kknaks/task_management` 스캐폴딩이 첫 work. config 에 `repos.code` 추가, 코드 워커는 개별 워크트리 + 문서 경로 배제, 문서/코드 PR 분리.

## 1. 지금

- [!] 남은 결정 3건 (사용자): ① sonioc + LLM 채팅 — 정체·편입 위치(새 영역 문서? 기존 영역 절? v1 여부) ② PR 묶음 단위(제안: Phase 1 완료 시 1회) ③ 메시지함 순서(현재 6번 — 당길지)
- [ ] Phase 1-1 writer 발주 — 인증·설정 BASE-001+DEC-001 (`--workers writer`, 같은 slug)
- [!] designer 터미널(`term_f7e8b9e4…`) 유휴 — writer 는 새 터미널로 (역할 컨텍스트 분리)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-03 | 문서 워커는 workspace=coordinator 로 코디 워크트리에 직접 탑승 (유실 재발 방지) | 사용자 승인 · runbook §workspace |
| 2026-09-03 | 기획서=템플릿+왜+인/아웃바운드+기능명세(기능 단위), 정책서=템플릿+규약(CRUD 기준), 기능정의서=기존 템플릿. 영역 하나씩 진행 | 사용자 지시 |
| 2026-09-03 | designer 역할 = 페이지 구성 + Next.js 구조 + shadcn 컴포넌트 + 공용 컴포넌트 도출 + 소요 파악 | 사용자 지시 |
| 2026-09-03 | 홈화면.dc.html 패키지 제외(홈·채팅은 나중) · 자료함 정본=문서함.dc.html · 메시지함 v1 범위 보류 | 사용자 확정 (Q-27·26·35) |
| 2026-09-03 | ~~문서화는 내 업무부터~~ → **인증·설정부터** (09-03 번복 — 업무가 설정의 프로젝트·유형을 참조하므로 설정 선행) | 사용자 확정 |
| 2026-09-03 | 작업 단위 = 워크트리 1개 = slug 1개. design-frontend-structure+auth-docs → docs-v1 통합 | 사용자 교정 · runbook §workspace |
| 2026-09-03 | Phase 1~3 전체 계획(§0) 합의 | 사용자 승인 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| designer | `term_f7e8b9e4-6379-4ad2-a1f5-8f81804bbfc2` | `task_319a3ee765d4` | `ctx_cb4ec3ab8c8a` | `docs-v1-design-brief.md` | 완료·검증 PASS |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.**

## 4. 산출물

- 리포트: `docs-v1-design-report.md` — P-01~72 · F-1~13 · C-01~49 · S-01~34 · Q-01~42
- 커밋: `3e13975` 리포트 · `e9db33a` 사용자 확정 4건 · `efd54e3` slug 통합

## 5. 이력 (최신이 위)

- `2026-09-03` 전체 계획(§0) 합의, _RESUME 에 등재
- `2026-09-03` 작업 단위 교정 — slug 2개(design-frontend-structure·auth-docs)를 docs-v1 로 통합 (사용자 지적)
- `2026-09-03` 사용자 확정 4건 반영 (홈화면 제외·자료함 정본·메시지함 보류·시작 영역) — 시작 영역은 이후 인증·설정으로 번복
- `2026-09-03` designer 리포트 완료·검증 PASS·커밋. 총계(참고안 제외) Page 24 · 오버레이 27 · 신규 컴포넌트 ~43 · 공용 34
- `2026-09-03` designer 발주 (workspace=coordinator 첫 실전). 추후 참고: sonioc(?)·LLM 채팅 내용 추가 예정 — §1 결정 ① 로 이동
