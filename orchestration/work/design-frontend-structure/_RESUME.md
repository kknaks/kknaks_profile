
# 재개 노트 — design-frontend-structure (task-management)

**지금**: designer 워커 발주 완료 — 디자인 패키지 프론트 구조 분석 진행 중
**다음**: worker_done 수신 → 리포트 검증(커버리지 표·OQ 대조·read-only 준수 diff 확인)

세팅: `scripts/new-work.sh task-management design-frontend-structure` · 설정 SSOT `config/projects/task-management.json`
코디handle: `term_e6d07c2f-a88d-46b4-9d0c-3ed44e6c90a2`

## 워크트리

- `docs`: 코디 워크트리 공유 (`workspace: coordinator`) — `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app` (branch `task-management-app`, base `origin/main` → PR `main`). 워커 개별 워크트리 없음.

## 1. 지금

- [~] designer — 00-design 패키지 분석 (페이지 구성 · Next.js 구조 · shadcn 매핑 · 공용 컴포넌트 · 소요)
- [ ] 리포트 수신 후: 작업 소요 검토 → 사용자와 문서화 순서 확정 → writer 발주 (baseline+decision, 영역 1건씩)
- [!] 리포트의 안정 ID(P/C/S/Q-xx)가 이후 baseline/decision 인용 체계 — 검증 시 확인

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-03 | 문서 워커는 workspace=coordinator 로 코디 워크트리에 직접 탑승 (유실 재발 방지) | 사용자 승인 · runbook §workspace |
| 2026-09-03 | 기획서=템플릿+왜+인/아웃바운드+기능명세(기능 단위), 정책서=템플릿+규약(CRUD 기준), 기능정의서=기존 템플릿. 영역 하나씩 진행 | 사용자 지시 |
| 2026-09-03 | designer 역할 = 페이지 구성 + Next.js 구조 + shadcn 컴포넌트 + 공용 컴포넌트 도출 + 소요 파악 | 사용자 지시 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| designer | `term_f7e8b9e4-6379-4ad2-a1f5-8f81804bbfc2` | `task_319a3ee765d4` | `ctx_cb4ec3ab8c8a` | `design-frontend-structure-design-brief.md` | 진행 |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.**

## 4. 산출물

- 리포트: `design-frontend-structure-report.md` (예정 — work/design-frontend-structure/)

## 5. 이력 (최신이 위)

- `2026-09-03` designer 발주 (workspace=coordinator 첫 실전). 추후 참고: sonioc(?)·LLM 채팅 내용 추가 예정 — 사용자와 확인 필요
