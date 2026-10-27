# Product Log

> 제품 단위 통합 변경 로그. baseline, decision, spec, work 변경 이력을 한 곳에 모은다.

| Date | Entry | Links |
|---|---|---|
| 2026-10-26 | 제품 착수. 사용자 입력(ccc 통역을 떼어 별도 PWA · 실시간 통역 · 로그인 · Procedure Hub 용어집 → Soniox)을 BASE-001 로, 대화에서 닫은 것(양방향 + 시작 때 언어 고르기 · 단일 계정 · medikit · 화면 구성 · 새 레포 · 로컬 확인 뒤 Mac Studio 배포)을 DEC-001(proposed)로. 빈 레포 `kknaksss/interpret-pwa` 생성. 코드 미착수 | [입력](00-baseline/baseline-001-interpret-pwa.md) · [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-26 | DEC-001 accepted — 사용자 「응 그렇게 가」. OQ-001~004 를 기본값으로 닫음(D-13~D-16) | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-26 | DEC-001 D-17 추가 — 중국어 번체는 back 에서 변환(Soniox 는 간체만 · 자막만 번체 · TTS 는 간체, ccc 방식). 사용자 지적 | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-26 | DEC-001 D-18~D-20 — 역방향 용어 포함 · 괄호는 TTS 에서만 뺌(Soniox 실물 확인 결과) · 화면은 Claude Design 전용 프로젝트 시안이 정본(1차 화면에 디자인 누락 지적) | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-26 | 시안 확정(Claude Design 캔버스 「Interpret PWA」 17화면 · `design/` 사본) · DEC-001 D-21 앱 이름 통키(Tongky) | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-26 | DEC-001 D-22 — 원 위에 고른 언어 안내(180° · 상태 8개) · 외국어 카드 안내 줄은 원 위로 이동 | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-26 | DEC-001 D-23 — 원 64px · 원 줄 약 140px · 자막 영역 확대(외부 피드백) | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-26 | DEC-001 D-24 — 자막을 메신저 말풍선으로(보는 사람 기준 내 말 오른쪽 · 상대 왼쪽) | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-26 | DEC-001 D-25 — 자막 자동 스크롤 · 사용자 스크롤 · 「↓ 최신」 단추 | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-26 | DEC-001 D-26 — 배포 도메인 tongky.medisolveai.xyz · cc-prototype 방식 | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-26 | 배포(tongky.medisolveai.xyz) 후 폰 피드백 — DEC-001 D-27 로그인 확대 막기 · D-28 중국어 번체 선택지 | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-27 | DEC-001 D-27~D-33 — 폰 피드백(로그인 확대 · 중국/대만 · 초기화 · 데모 로그인 · 언어 목록 180° · s2twp) · **용어집을 우리 시드 파일로(정규화 · Procedure Hub 는 첫 가져오기만)** | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-27 | 용어집 시드 배포(PR #4) · DEC-001 D-34 시작 오버레이 = 언어 단추 7개(누르면 시작) | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-27 | D-34 배포(PR #5) · 대만 현지명 웹 조사(77/157) · DEC-001 D-35 — 시드 반영 · D-32(s2twp) 뒤집음 → s2tw + 激光→雷射 | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-27 | 운영 끊김 원인(TTS keepalive) 수정 · D-35 배포(PR #6) · DEC-001 D-36 누르고 말하기 모드 | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-27 | D-36 배포(PR #7) · DEC-001 D-37 — 용어집 API · 메뉴 삭제 · 최소 정보만 노출(D-13 뒤집음) | [결정](10-decision/decision-001-interpret-pwa.md) |
| 2026-10-27 | 마감 — 아카이브 · 회고 | [회고](log/2026-10-27-interpret-pwa-poc.md) |
| 2026-10-27 | DEC-001 D-38 — 대만어 사전 2차(대만 클리닉 3곳 대조 · 한국 전용 제품은 영문 · 톡신 대만 허가명) | [결정](10-decision/decision-001-interpret-pwa.md) |
