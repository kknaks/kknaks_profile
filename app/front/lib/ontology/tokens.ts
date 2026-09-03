/**
 * 데모 토큰 레이어 — **`globals.css` 를 고치지 않는다**(SPEC-004 AC-3).
 *
 * 포트폴리오 전역 토큰은 dark-first 단일 테마라 여기 값들을 환원할 수 없다. 그래서
 * 데모 컨테이너 스코프(`[data-surface="ontology"]`)에 `--ont-*` 접두로 선언하고,
 * 그 컨테이너에 **`color-scheme: light` 를 재선언**한다 — 재선언하지 않으면 네이티브
 * 위젯(스크롤바·폼 컨트롤)이 다크로 샌다.
 *
 * **값의 SoT 는 디자인 `01-tokens.md` 이고, 코드 안의 단일 정의는 아래 `ONT_HEX` 다.**
 * CSS 변수도 SVG 인코딩도 전부 이 상수에서 나온다 — SPEC-004 가 경고한 「hex 를 두 곳에
 * 두면 반드시 어긋난다」를 구조로 막는다. 새 색을 만들지 않는다(디자인 08 규칙 4).
 *
 * 환원한 것: Mono 폰트(`--font-next-mono`) · 전환 시간 120ms.
 */

export const ONTOLOGY_SURFACE_ATTR = "ontology" as const;

/** 최소 지원 폭 — **데모 컨테이너에만** 건다. 루트(html/body)에 걸지 않는다(U-3). */
export const MIN_WIDTH_PX = 1280;

/**
 * 팔레트 단일 정의(디자인 `01-tokens.md` 전사).
 *
 * CSS 변수를 쓸 수 있는 자리는 `var(--ont-*)` 를 쓰고, **SVG 처럼 `var()` 가 통하지 않거나
 * 계산이 필요한 자리**(마커 id, stroke 색 분기)만 이 상수를 직접 읽는다.
 */
export const ONT_HEX = {
  // 텍스트 · 액션
  primary: "#7181F8",
  primaryHover: "#5F71F5",
  primaryDeep: "#4B52A8",
  primaryFill: "#F1F2FE",
  ink: "#1E1E1E",
  body: "#5F6470",
  label: "#757575",
  muted: "#9EA2AE",
  placeholder: "#B3B3B3",

  // 서피스 · 보더
  surface: "#FFFFFF",
  canvas: "#F9FAFB",
  hover: "#F5F6F8",
  rowDivider: "#F1F2F5",
  rowSelected: "#F8FAFF",
  border: "#EBEBEB",
  borderCard: "#D9D9D9",
  borderHeader: "#E5E7EA",
  graphCanvas: "#FCFCFD",

  // 상태 — 정상은 색을 쓰지 않는다. 색이 보이는 곳이 곧 봐야 할 곳이다.
  alert: "#E2685B",
  alertFill: "#FDEEEC",
  alertText: "#A6382C",
  alertBorder: "#F5C7C1",
  alertSoft: "#FFF8F7",
  watch: "#E3B93C",
  watchFill: "#FEF3C0",
  watchText: "#8A6A11",
  watchBorder: "#F0DC8A",
  watchSoft: "#FFFDF5",
  normal: "#9EA2AE",
  normalFill: "#FFFFFF",
  normalText: "#5F6470",
  unobserved: "#B3B3B3",
  unobservedFill: "#FFFFFF",
  unobservedText: "#B3B3B3",
  info: "#33AAFF",

  // 스파크라인 중간톤
  sparkAlert: "#EE9C92",
  sparkWatch: "#F0DC8A",
  sparkNormal: "#E5E7EA",

  // 계층 배지
  bronzeFill: "#FBF3E3",
  bronzeBorder: "#E8D5A8",
  bronzeText: "#8A6A11",
  bronzeDot: "#8A6A11",
  silverFill: "#F5F6F8",
  silverBorder: "#E5E7EA",
  silverText: "#5F6470",
  silverDot: "#9EA2AE",
  goldFill: "#FEF3C0",
  goldBorder: "#F0DC8A",
  goldText: "#8A6A11",
  goldDot: "#E3B93C",
} as const;

export const ontologySurfaceCss = `
[data-surface="ontology"] {
  /* 전역이 dark 라 여기서 되돌린다 — 빠뜨리면 스크롤바·폼 컨트롤이 다크로 샌다. */
  color-scheme: light;

  /* 텍스트 · 액션 */
  --ont-primary: ${ONT_HEX.primary};
  --ont-primary-hover: ${ONT_HEX.primaryHover};
  --ont-primary-deep: ${ONT_HEX.primaryDeep};
  --ont-primary-fill: ${ONT_HEX.primaryFill};
  --ont-ink: ${ONT_HEX.ink};
  --ont-body: ${ONT_HEX.body};
  --ont-label: ${ONT_HEX.label};
  --ont-muted: ${ONT_HEX.muted};
  --ont-placeholder: ${ONT_HEX.placeholder};

  /* 서피스 · 보더 */
  --ont-surface: ${ONT_HEX.surface};
  --ont-canvas: ${ONT_HEX.canvas};
  --ont-hover: ${ONT_HEX.hover};
  --ont-row-divider: ${ONT_HEX.rowDivider};
  --ont-row-selected: ${ONT_HEX.rowSelected};
  --ont-border: ${ONT_HEX.border};
  --ont-border-card: ${ONT_HEX.borderCard};
  --ont-border-header: ${ONT_HEX.borderHeader};
  --ont-graph-canvas: ${ONT_HEX.graphCanvas};

  /* 상태 */
  --ont-alert: ${ONT_HEX.alert};
  --ont-alert-fill: ${ONT_HEX.alertFill};
  --ont-alert-text: ${ONT_HEX.alertText};
  --ont-alert-border: ${ONT_HEX.alertBorder};
  --ont-alert-soft: ${ONT_HEX.alertSoft};
  --ont-watch: ${ONT_HEX.watch};
  --ont-watch-fill: ${ONT_HEX.watchFill};
  --ont-watch-text: ${ONT_HEX.watchText};
  --ont-watch-border: ${ONT_HEX.watchBorder};
  --ont-watch-soft: ${ONT_HEX.watchSoft};
  --ont-normal: ${ONT_HEX.normal};
  --ont-normal-fill: ${ONT_HEX.normalFill};
  --ont-normal-text: ${ONT_HEX.normalText};
  --ont-unobserved: ${ONT_HEX.unobserved};
  --ont-unobserved-fill: ${ONT_HEX.unobservedFill};
  --ont-unobserved-text: ${ONT_HEX.unobservedText};
  --ont-info: ${ONT_HEX.info};

  /* 스파크라인 중간톤 */
  --ont-spark-alert: ${ONT_HEX.sparkAlert};
  --ont-spark-watch: ${ONT_HEX.sparkWatch};
  --ont-spark-normal: ${ONT_HEX.sparkNormal};

  /* 계층 배지 */
  --ont-bronze-fill: ${ONT_HEX.bronzeFill};
  --ont-bronze-border: ${ONT_HEX.bronzeBorder};
  --ont-bronze-text: ${ONT_HEX.bronzeText};
  --ont-bronze-dot: ${ONT_HEX.bronzeDot};
  --ont-silver-fill: ${ONT_HEX.silverFill};
  --ont-silver-border: ${ONT_HEX.silverBorder};
  --ont-silver-text: ${ONT_HEX.silverText};
  --ont-silver-dot: ${ONT_HEX.silverDot};
  --ont-gold-fill: ${ONT_HEX.goldFill};
  --ont-gold-border: ${ONT_HEX.goldBorder};
  --ont-gold-text: ${ONT_HEX.goldText};
  --ont-gold-dot: ${ONT_HEX.goldDot};

  /* 그라디언트 */
  --ont-grad-logo: linear-gradient(135deg, ${ONT_HEX.primary}, #A6CDFF);
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
  background: ${ONT_HEX.canvas};
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
