/**
 * 데모 토큰 레이어 — **`globals.css` 를 고치지 않는다**(SPEC-004 AC-3).
 *
 * 포트폴리오 전역 토큰은 dark-first 단일 테마라 여기 값들을 환원할 수 없다. 그래서
 * 데모 컨테이너 스코프(`[data-surface="ontology"]`)에 `--ont-*` 접두로 선언하고,
 * 그 컨테이너에 **`color-scheme: light` 를 재선언**한다 — 재선언하지 않으면 네이티브
 * 위젯(스크롤바·폼 컨트롤)이 다크로 샌다.
 *
 * **값의 SoT 는 디자인 `01-tokens.md` 다.** 여기 있는 hex 는 그 표의 전사이고,
 * 새 색을 만들지 않는다(디자인 08 규칙 4).
 *
 * 환원한 것: Mono 폰트(`--font-next-mono`) · 전환 시간 120ms.
 */

export const ONTOLOGY_SURFACE_ATTR = "ontology" as const;

/** 최소 지원 폭 — **데모 컨테이너에만** 건다. 루트(html/body)에 걸지 않는다(U-3). */
export const MIN_WIDTH_PX = 1280;

export const ontologySurfaceCss = `
[data-surface="ontology"] {
  /* 전역이 dark 라 여기서 되돌린다 — 빠뜨리면 스크롤바·폼 컨트롤이 다크로 샌다. */
  color-scheme: light;

  /* 텍스트 · 액션 */
  --ont-primary: #7181F8;
  --ont-primary-hover: #5F71F5;
  --ont-primary-deep: #4B52A8;
  --ont-primary-fill: #F1F2FE;
  --ont-ink: #1E1E1E;
  --ont-body: #5F6470;
  --ont-label: #757575;
  --ont-muted: #9EA2AE;
  --ont-placeholder: #B3B3B3;

  /* 서피스 · 보더 */
  --ont-surface: #FFFFFF;
  --ont-canvas: #F9FAFB;
  --ont-hover: #F5F6F8;
  --ont-row-divider: #F1F2F5;
  --ont-row-selected: #F8FAFF;
  --ont-border: #EBEBEB;
  --ont-border-card: #D9D9D9;
  --ont-border-header: #E5E7EA;
  --ont-graph-canvas: #FCFCFD;

  /* 상태 — 정상은 색을 쓰지 않는다. 색이 보이는 곳이 곧 봐야 할 곳이다. */
  --ont-alert: #E2685B;
  --ont-alert-fill: #FDEEEC;
  --ont-alert-text: #A6382C;
  --ont-alert-border: #F5C7C1;
  --ont-alert-soft: #FFF8F7;
  --ont-watch: #E3B93C;
  --ont-watch-fill: #FEF3C0;
  --ont-watch-text: #8A6A11;
  --ont-watch-border: #F0DC8A;
  --ont-watch-soft: #FFFDF5;
  --ont-normal: #9EA2AE;
  --ont-normal-fill: #FFFFFF;
  --ont-normal-text: #5F6470;
  --ont-unobserved: #B3B3B3;
  --ont-unobserved-fill: #FFFFFF;
  --ont-unobserved-text: #B3B3B3;
  --ont-info: #33AAFF;

  /* 스파크라인 중간톤 */
  --ont-spark-alert: #EE9C92;
  --ont-spark-watch: #F0DC8A;
  --ont-spark-normal: #E5E7EA;

  /* 계층 배지 */
  --ont-bronze-fill: #FBF3E3;
  --ont-bronze-border: #E8D5A8;
  --ont-bronze-text: #8A6A11;
  --ont-bronze-dot: #8A6A11;
  --ont-silver-fill: #F5F6F8;
  --ont-silver-border: #E5E7EA;
  --ont-silver-text: #5F6470;
  --ont-silver-dot: #9EA2AE;
  --ont-gold-fill: #FEF3C0;
  --ont-gold-border: #F0DC8A;
  --ont-gold-text: #8A6A11;
  --ont-gold-dot: #E3B93C;

  /* 그라디언트 */
  --ont-grad-logo: linear-gradient(135deg, #7181F8, #A6CDFF);
  --ont-grad-avatar: linear-gradient(140deg, #C3CBFB, #98A6F0);
  --ont-grad-assistant: linear-gradient(140deg, #7B8AFA, #6474F5);

  /* 라이트용 섀도 */
  --ont-shadow-metric: 0 1px 2px rgba(16, 24, 40, 0.04), 0 8px 20px rgba(16, 24, 40, 0.04);
  --ont-shadow-card: 0 1px 2px rgba(16, 24, 40, 0.03);
  --ont-shadow-drop: 0 16px 40px rgba(0, 0, 0, 0.16);
  --ont-shadow-overlay: 0 8px 24px rgba(16, 24, 40, 0.08);
  --ont-focus-ring: 0 0 0 3px rgba(113, 129, 248, 0.16);

  /* 타입 스케일 */
  --ont-t-page: 28px;
  --ont-t-panel: 16px;
  --ont-t-section: 15px;
  --ont-t-body: 14px;
  --ont-t-meta: 13px;
  --ont-t-caption: 12px;
  --ont-t-badge: 11px;

  /* 전환 — 기존 관례(120ms)로 환원 */
  --ont-transition: 120ms ease;

  /* Sans 는 데모 그룹에서만 Pretendard, Mono 는 기존 JetBrains Mono 를 환원한다. */
  --ont-font-sans: var(--font-ont-sans), -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --ont-font-mono: var(--font-next-mono), "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;

  position: relative;
  z-index: 30;
  min-height: 100vh;
  background: var(--ont-canvas);
  color: var(--ont-ink);
  font-family: var(--ont-font-sans);
  font-size: var(--ont-t-body);
  letter-spacing: -0.02em;
  -webkit-font-smoothing: antialiased;
}

/*
 * 포트폴리오 셸 차단 — 루트 레이아웃이 TopNav·PageFooter 를 모든 라우트에 주입하고
 * 그 파일은 **수정 금지 대상**이다(SPEC-004 §5 · 역할 rules). 데모 표면이 문서에
 * 있는 동안에만 두 표면을 가린다. 데모는 자체 h64 헤더를 쓴다(U-1).
 */
body:has([data-surface="ontology"]) > .topnav-wrap,
body:has([data-surface="ontology"]) > footer {
  display: none !important;
}
body:has([data-surface="ontology"]) {
  background: #F9FAFB;
}

[data-surface="ontology"] *,
[data-surface="ontology"] *::before,
[data-surface="ontology"] *::after {
  box-sizing: border-box;
}
[data-surface="ontology"] a {
  color: inherit;
  text-decoration: none;
}
[data-surface="ontology"] button {
  font-family: inherit;
  letter-spacing: inherit;
  cursor: pointer;
}
[data-surface="ontology"] input {
  font-family: inherit;
  letter-spacing: inherit;
}
[data-surface="ontology"] .ont-mono {
  font-family: var(--ont-font-mono);
}

/* 최소 폭 — 컨테이너 스코프. 루트에 걸지 않는다(U-3 · 디자인 07 Responsive). */
[data-surface="ontology"] .ont-app {
  min-width: ${MIN_WIDTH_PX}px;
}
[data-surface="ontology"] .ont-narrow {
  display: none;
}
@media (max-width: ${MIN_WIDTH_PX - 1}px) {
  [data-surface="ontology"] .ont-app {
    display: none;
  }
  [data-surface="ontology"] .ont-narrow {
    display: flex;
    min-width: 0;
  }
}
`;
