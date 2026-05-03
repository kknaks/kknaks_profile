/**
 * Monogram — kk 박스. 헤더 좌측 (FullHeader 44px / CompactHeader 28px).
 * 원본: claude_design/kknaks_profile_v2.0.0/print/components.jsx#Monogram
 */

export function Monogram({ size = 36 }: { size?: number }) {
  return (
    <div
      style={{
        width: size,
        height: size,
        background: "var(--fg-0)",
        color: "#fff",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "var(--font-mono)",
        fontSize: size * 0.42,
        fontWeight: 600,
        letterSpacing: "-0.04em",
        borderRadius: 3,
        flexShrink: 0,
      }}
    >
      kk
    </div>
  );
}
