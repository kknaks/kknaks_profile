import type { Metadata } from "next";
import localFont from "next/font/local";
import { ontologySurfaceCss } from "@/lib/ontology/tokens";

/**
 * 데모 라우트 그룹 셸 — 포트폴리오와 데모를 가르는 경계.
 *
 * - 토큰은 **컨테이너 스코프**(`[data-surface="ontology"]`)에만 선언한다.
 *   `globals.css` 는 한 줄도 건드리지 않는다(SPEC-004 AC-3·AC-4).
 * - Pretendard 는 **next/font** 로 넣는다 — CDN `@import` 를 쓰지 않는다(AC-5).
 *   Mono 는 루트 레이아웃의 JetBrains Mono(`--font-next-mono`)를 그대로 환원한다.
 * - `min-width: 1280px` 는 **데모 컨테이너에만** 걸린다(U-3 · AC-7).
 *
 * 헤더(h64 탭 셸)는 화면마다 `OntologyShell` 이 그린다 — 접속 게이트에는 셸이 없기
 * 때문에 레이아웃이 헤더를 강제하지 않는다(디자인 02 접속 게이트).
 */

const pretendard = localFont({
  src: "./fonts/PretendardVariable.woff2",
  weight: "45 920",
  style: "normal",
  display: "swap",
  variable: "--font-ont-sans",
});

export const metadata: Metadata = {
  title: "Ontology — 내부 공유 데모",
  description: "메달리온 계층과 온톨로지 그래프를 근거로 답하는 내부 공유용 데모",
  robots: { index: false, follow: false },
};

export default function OntologyLayout({ children }: { children: React.ReactNode }) {
  return (
    <div data-surface="ontology" className={pretendard.variable}>
      <style dangerouslySetInnerHTML={{ __html: ontologySurfaceCss }} />

      {/* 1280px 미만 — 화면 대신 안내. 포트폴리오는 영향받지 않는다. */}
      <div
        className="ont-narrow"
        style={{
          minHeight: "100vh",
          alignItems: "center",
          justifyContent: "center",
          padding: 24,
          background: "var(--ont-canvas)",
        }}
      >
        <div
          style={{
            width: 400,
            maxWidth: "100%",
            borderRadius: 12,
            background: "var(--ont-surface)",
            border: "1px solid var(--ont-border-card)",
            boxShadow: "var(--ont-shadow-card)",
            padding: 32,
            display: "flex",
            flexDirection: "column",
            gap: 16,
          }}
        >
          <OntologyWordmark />
          <p style={{ margin: 0, fontSize: 15, lineHeight: 1.6, color: "var(--ont-body)" }}>
            이 데모는 데스크톱 화면(가로 1280px 이상)에 맞춰 만들었습니다. 창을 넓히거나
            데스크톱에서 열어 주세요.
          </p>
        </div>
      </div>

      <div className="ont-app">{children}</div>
    </div>
  );
}

function OntologyWordmark() {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <span
        style={{
          width: 26,
          height: 26,
          borderRadius: 6,
          background: "var(--ont-grad-logo)",
          color: "#fff",
          fontSize: 13,
          fontWeight: 800,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        O
      </span>
      <span style={{ fontSize: 17, fontWeight: 800, letterSpacing: "-0.01em" }}>Ontology</span>
    </div>
  );
}
