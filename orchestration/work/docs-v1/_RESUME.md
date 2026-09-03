
# 재개 노트 — docs-v1 (task-management)

> **작업 단위 = 이 워크트리(브랜치 task-management-app) 1개 = 이 slug 1개.**
> v1 문서 파이프라인(디자인 분석 → 영역별 baseline+decision → spec)이 전부 여기서 돈다.
> 워커 추가 발주는 새 slug 를 파지 않고 `new-work.sh task-management docs-v1 --workers <w>` 로 이 폴더에 브리프를 더한다.

**지금**: 리포트 완료·검증 PASS·커밋(3e13975). 사용자 게이트 대기
**다음**: 구조 게이트 답 수신(Q-26 자료함 정본 · Q-27 홈화면 삭제 의도 · Q-28 Tauri export · Q-33 shadcn 도입 · Q-34 좌표 vs 유동 · Q-35 메시지함 범위) → 문서화 순서 확정 → writer 발주

세팅: `scripts/new-work.sh task-management docs-v1` · 설정 SSOT `config/projects/task-management.json`
코디handle: `term_e6d07c2f-a88d-46b4-9d0c-3ed44e6c90a2`

## 워크트리

- `docs`: 코디 워크트리 공유 (`workspace: coordinator`) — `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app` (branch `task-management-app`, base `origin/main` → PR `main`). 워커 개별 워크트리 없음.

## 1. 지금

- [!] 사용자 게이트 — 구조 갈림길 6건(Q-26·27·28·33·34·35). 특히 Q-28(Tauri static export)이 App Router 데이터 계층을 통째로 가름
- [ ] 게이트 답 → 문서화 순서 확정(리포트 §6-3 안: 홈·채팅은 md 자체가 없어 baseline 먼저 필요) → writer 발주
- [!] 홈화면.dc.html 워킹트리 삭제(D) 미커밋 — Q-27 답에 따라 삭제 커밋 or 복원

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-03 | 문서 워커는 workspace=coordinator 로 코디 워크트리에 직접 탑승 (유실 재발 방지) | 사용자 승인 · runbook §workspace |
| 2026-09-03 | 기획서=템플릿+왜+인/아웃바운드+기능명세(기능 단위), 정책서=템플릿+규약(CRUD 기준), 기능정의서=기존 템플릿. 영역 하나씩 진행 | 사용자 지시 |
| 2026-09-03 | designer 역할 = 페이지 구성 + Next.js 구조 + shadcn 컴포넌트 + 공용 컴포넌트 도출 + 소요 파악 | 사용자 지시 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| designer | `term_f7e8b9e4-6379-4ad2-a1f5-8f81804bbfc2` | `task_319a3ee765d4` | `ctx_cb4ec3ab8c8a` | `docs-v1-design-brief.md` | 완료·검증 PASS |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.**

## 4. 산출물

- 리포트: `docs-v1-design-report.md` — P-01~72 · F-1~13 · C-01~49 · S-01~34 · Q-01~42
- 커밋: `3e13975` — 리포트·브리프·_RESUME

## 5. 이력 (최신이 위)

- `2026-09-03` 리포트 완료·검증 PASS·커밋. 총계(참고안 제외) Page 24 · 오버레이 27 · 신규 컴포넌트 ~43 · 공용 34
- `2026-09-03` designer 발주 (workspace=coordinator 첫 실전). 추후 참고: sonioc(?)·LLM 채팅 내용 추가 예정 — 사용자와 확인 필요
