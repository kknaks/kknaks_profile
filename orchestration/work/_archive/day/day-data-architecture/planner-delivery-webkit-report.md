# planner-delivery-webkit 결과 보고 — done (human gate · 승인 안 함)

## Issue

- **[MediSolveAIDev/CENTURION_DAY#229](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/229)** 「DAY v2 웹 기반 — medikit HTMX 컴포넌트(매크로 · 토큰 · 견본 페이지)」 — 새 Issue 1개(idempotency `day/v2-web-kit`).
- 라벨 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending` · `next_action = review-delivery-plan`(human_gate).
- **plan_digest = `sha256:6847d991a7124406a229f3d493b307f1a6c8305f9695056268c10e13cc2c22cc`**
- 요청 `delivery/v2-web-kit.json` → `--plan`(`v2-web-kit.plan.json`) → `--apply`(`v2-web-kit.apply.json`). 방법은 #224 ~ #227 과 같음(이 워크트리 `tools/harness` · code repo = CENTURION_DAY v2-dev 로컬 clone · mediness origin/main `d93b9210…`). mediness 워크트리 파일은 건드리지 않았다.

## 계약 요약

- **target** DAY-SPEC-002(PR #909 워크트리 미커밋 draft → pending) · **위험 L2**(새 웹 공통 기반 = 이후 화면의 모양 계약 · migration · 외부 write · 인증 변경 없음 — #224 뼈대와 같은 등급).
- **Target Delta 8**: 화면보다 기반 먼저(사용자 결정) · centurion 키트 가져오기 + htmx 벤더링 · 라이선스(키트 수정 금지) · `base.html` 셸 G1 · htmx-config · 모달 · 토스트 · CSRF 자리 · `ui.html` 매크로(기존 7 + HTMX 에 없는 6: 툴팁 G3 · 팝오버/목록 G16 · 콤보박스 목록 · 아코디언 G4 · 토스트 · 체크박스 혼합 G11 + 시술 현황 gap: G2 · G5 · G6 · G7 · G8 · G9 · G10 · G12 · G13 · G14 · G17 · 의사 호출 모달(원천 「화면 참고」) · 수납 필요 자리) · DAY 토큰 확장(CRM 브랜드색 · 고객 상태 팔레트) · `static/day.js`(위임 + data-*) · 견본 페이지(dev 전용) · 「키트로 올릴 후보」.
- **Acceptance A1 ~ A8**: 견본에서 매크로 상태별 표시(dev 200 · prod 404) · 손 CSS 0(grep) · 인라인 스크립트 0(grep) · 매크로 ↔ E · G 번호 대응표 · 키트 후보 목록 · htmx 벤더링 · 라이선스 · config · 스크린샷 · 의사 호출 모달 원천 모양.
- **Non-Goals**: 시술 현황 화면 · 업무 라우터 · API · SSE · 로그인 화면 · 앱 · centurion 키트 수정 · 방 옮기기/연결(G15 · U5) · 차트 작성(U11) · prod 배포.
- **Review Surface**: baseline pending · L2 근거 · **빌드 방식 충돌**(AGENTS.md `styles/` tailwind build · 「빌드된 CSS 커밋」 vs 키트 「빌드 없음」) · medikit 1.3.0(키트) vs 1.4.0(DS 조사) · 의존 순서(CSRF `hx-headers` 는 #227 이 PR #228 에 들어온 뒤 · 그 전엔 자리만 · 웹 조립이 #224 에 없으면 이 Delivery 가) · Figma 전용 부품 근사 여부.
- **Execution**: code surface(templates · static · styles · web.py · 견본 라우터 · architecture 테스트) · 의존 #224 · #227(CSRF) · 6 phase · 검증(견본 라우트 dev/prod · grep 테스트 · 스크린샷) · rollback revert · open question = 토큰 확장 방식.
- **담당 워커: frontend** — 계약 스키마에 담당 칸이 없어 이 리포트에만 적는다.

## 참고

- PR #228 브랜치 `backend/day/` 에는 아직 `web.py` · `templates/` · `static/` · `styles/` 가 없다(확인) — 웹 앱 조립이 이 Delivery 몫이 될 수 있어 Review Surface 에 올렸다.

## 다음 (사용자)

1. #229 결과 계약 승인 receipt(plan_digest 위 값).
2. Review Surface 의 빌드 방식(빌드 CSS vs 무빌드) 판단.
