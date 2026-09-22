"use client";

import type { CSSProperties, ReactNode } from "react";
import type { Layer, NodeState } from "@/lib/ontology/types";
import { LAYER_LABEL, layerTone, stateTone } from "@/lib/ontology/encoding";

/** 상태 dot — 색이 보이는 곳이 곧 봐야 할 곳이다(디자인 01). */
export function StatusDot({ state, size = 8 }: { state: NodeState | null; size?: number }) {
  const tone = stateTone(state);
  return (
    <span
      aria-hidden
      style={{
        width: size,
        height: size,
        borderRadius: "50%",
        background: tone.dot,
        flexShrink: 0,
        display: "inline-block",
      }}
    />
  );
}

export function LayerBadge({ layer, size = "md" }: { layer: Layer; size?: "sm" | "md" }) {
  const tone = layerTone(layer);
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        height: size === "sm" ? 22 : 26,
        padding: size === "sm" ? "0 8px" : "0 10px",
        borderRadius: 6,
        background: tone.fill,
        border: `1px solid ${tone.border}`,
        color: tone.text,
        fontSize: size === "sm" ? 11 : 12,
        fontWeight: 600,
        whiteSpace: "nowrap",
      }}
    >
      <span style={{ width: 7, height: 7, borderRadius: "50%", background: tone.dot }} />
      {LAYER_LABEL[layer]}
    </span>
  );
}

export function Panel({
  children,
  style,
  padded = true,
}: {
  children: ReactNode;
  style?: CSSProperties;
  padded?: boolean;
}) {
  return (
    <section
      style={{
        borderRadius: 12,
        border: "1px solid var(--ont-border-card)",
        background: "var(--ont-surface)",
        boxShadow: "var(--ont-shadow-card)",
        padding: padded ? 20 : 0,
        minWidth: 0,
        ...style,
      }}
    >
      {children}
    </section>
  );
}

export function SectionLabel({ children }: { children: ReactNode }) {
  return (
    <div
      style={{
        fontSize: 12,
        fontWeight: 700,
        letterSpacing: "0.04em",
        color: "var(--ont-muted)",
      }}
    >
      {children}
    </div>
  );
}

type ButtonTone = "primary" | "secondary" | "ink";

export function OntButton({
  children,
  onClick,
  tone = "secondary",
  disabled,
  height = 34,
  full,
  title,
  submit,
}: {
  children: ReactNode;
  onClick?: () => void;
  tone?: ButtonTone;
  disabled?: boolean;
  height?: number;
  full?: boolean;
  title?: string;
  submit?: boolean;
}) {
  const palette: Record<ButtonTone, CSSProperties> = {
    primary: { background: "var(--ont-primary)", color: "#fff", border: "1px solid var(--ont-primary)" },
    ink: { background: "var(--ont-ink)", color: "#fff", border: "1px solid var(--ont-ink)" },
    secondary: {
      background: "var(--ont-surface)",
      color: "var(--ont-body)",
      border: "1px solid var(--ont-border-card)",
    },
  };

  return (
    <button
      type={submit ? "submit" : "button"}
      onClick={onClick}
      disabled={disabled}
      title={title}
      style={{
        height,
        padding: "0 14px",
        borderRadius: 8,
        fontSize: 13,
        fontWeight: 600,
        width: full ? "100%" : undefined,
        opacity: disabled ? 0.45 : 1,
        cursor: disabled ? "not-allowed" : "pointer",
        transition: `background var(--ont-transition), color var(--ont-transition)`,
        ...palette[tone],
      }}
    >
      {children}
    </button>
  );
}

/** 로딩·에러·빈 결과 — 빈 상자를 그리지 않는다. */
export function StateNote({ children, tone = "muted" }: { children: ReactNode; tone?: "muted" | "alert" }) {
  return (
    <div
      style={{
        padding: "18px 20px",
        fontSize: 13,
        lineHeight: 1.6,
        color: tone === "alert" ? "var(--ont-alert-text)" : "var(--ont-muted)",
        background: tone === "alert" ? "var(--ont-alert-fill)" : "transparent",
        borderRadius: 8,
      }}
    >
      {children}
    </div>
  );
}

export function Mono({ children, style }: { children: ReactNode; style?: CSSProperties }) {
  return (
    <span className="ont-mono" style={style}>
      {children}
    </span>
  );
}
