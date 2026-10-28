# [planner] 문서 정리 — SPEC-001 0.4.1 · WORK-001 · 제품 README · 배포 기록

너는 interpret-pwa planner 다. 역할 · 검증 · 보고는 원 브리프 그대로: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/interpret-pwa-poc-spec-brief.md`. allowed_paths 는 이번만 **`/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/README.md`**(제품 README 현재 상태 · 코드 위치 · 배포 칸). log.md · DEC 는 코디 몫 — 건드리지 마라.

## 입력
- DEC-001 D-33 · **D-34**(새) — `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- 배포된 코드 main 9befd18(read-only): `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc/` (frontend 가 지금 D-34 를 같은 워크트리에서 작업 중 — 읽기만)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/wp9-be-report.md` · `wp9-fe-report.md` · `fix-phone3-*` · 백엔드 처분 「한도 20251」
- 배포 사실(코디): 2026-10-26 첫 배포 https://tongky.medisolveai.xyz · 코드 PR #1~#4(main 046eabe → 4ccf905 → d0a91a7 → 9befd18) · infra MediSolveAIDev/k8s_infra_mac PR #25~#28 · ns interpret-pwa-prod · Argo 수동 sync · Secret interpret-pwa-secret(INTERPRET_DEMO_LOGIN=true 데모 중) · ghcr-pull · DNS CNAME tongky

## 고칠 것
1. SPEC 0.4.0 → **0.4.1**: §2.4 한도 기본값 **20251**(시드 실측 ja 22,502 × 0.9 · th 줄이기 0) · §4.2 백엔드가 더한 것(`unknown_field` 오류 · term `note` · 가져오기 `--date`) · §7.3 #1 시작 오버레이 = **언어 단추 7개(D-34)** · §9.5 배포 확인 결과(코디 확인: health · login · manifest · wss ready · demo) · 변경 이력
2. WORK-001: WP7(로컬 E2E — 사용자가 건너뛰고 폰으로 감) · WP8(배포 done · PR 번호) · WP-P(폰 피드백 1~3 done) · WP9 · WP10 done(PR #4) · WP11(재배포 done · 폰 확인 진행 중) · **WP12(D-34 front · design — 진행 중)** · 열린 것(시드 PR 숙제: zh-Hant 현지명 · 구어 별칭 美版/韩版)
3. 제품 README 현재 상태 표(Baseline · Decision D-34 · Spec 0.4.1 · Work) · 배포 주소 · 코드 레포 · 시안 링크 https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd
4. 비밀값 · 계정값 0(grep)

## 완료 보고
원 브리프 §9(코디 핸들은 보고 직전 `orca terminal list --json` 에서 제목에 'Interpretation PWA').
