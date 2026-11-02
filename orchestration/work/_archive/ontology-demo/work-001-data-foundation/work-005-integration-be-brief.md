
# [backend] WORK-005 통합·배포 준비 (P1~P4, work_type: release)

너는 **ontology-demo `backend` 워커**다. 마지막 WP. 같은 워크트리. git 조작 금지. app/front/ 수정 금지(FE 동기는 FE 워커 별도 진행 중).

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline/para/projects/summer-star/ontology-demo/30-work/work-005-integration-and-deploy.md` (P1~P4)
- DEC-005(내부 공유 배포) · SPEC 전건 최신판 · 조사 리포트 §5.1(compose)·§5.6

## 2. P1 통합 검증

- 게이트 1~5 전건 재실행 수치(라이브 게이트 4·5 는 R-1 1회로 대표 — 반복 금지) + **PII 전면 스캔**: API·MCP·채팅 응답 표면 전수(마스킹 표기만·원값 0건, 로그 포함).
- retry 계약 반영: done·pending 메시지 retry → 400 RETRY_NOT_ALLOWED (SPEC-003 v0.0.10, 1줄+회귀).
- FE 빌드 산출물과의 계약 대조는 하지 않는다(FE 워커 몫) — 단 mock 픽스처 3종(kpi·graph·layers)을 실 API 응답과 diff 해 필드 불일치 목록만 보고.

## 3. P2 회귀 자동화 — 게이트를 한 명령으로: `uv run pytest -q tests/` + 라이브 플래그 문서화. 별도 CI 없음(레포 방침).

## 4. P3 배포 구성 (실행은 안 한다 — 구성 파일·절차만)

- compose 에 ontology-mcp·ontology-agent 서비스 추가(검수 W5 이월. 기존 서비스 무변경 원칙 유지, +만).
- `ONTOLOGY_MCP_ALLOWED_HOSTS` 명시 주입 · env 전 키 목록을 `.env.example`(값 없이 키+주석)로.
- NPM 서브도메인·Vercel env(NEXT_PUBLIC_ONTOLOGY_API_BASE)·비번 주입 절차를 README 「배포」 절에 — 홈서버에서 사람이 따라 하는 절차서 수준.

## 5. P4 로컬 E2E 절차서 — **내일 아침 사용자가 그대로 따라 하는 문서** (README 「로컬 E2E」 절):

1) .env 에 ONTOLOGY_DEMO_PASSWORD 난수 1줄 → 2) 빌드(build all) → 3) redis+ontology-worker 기동 → 4) MCP·API 기동 → 5) front dev(실 API env) → 6) 게이트 로그인 → 3페이지 확인 → 채팅 R-1 질문. 각 단계 명령 복붙 가능하게. 실기동으로 절차서 자체를 1회 검증(임시 비번).

## 6. 완료 보고 — 2채널(코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "backend 완료: WORK-005", body: 게이트 전건 수치·PII 스캔 결과·픽스처 diff·절차서 검증 결과·미결.
