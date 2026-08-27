"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import type { HeadlineTone, ProfileResponse, SiteResponse } from "@/lib/types";

const TONE_COLOR: Record<HeadlineTone, string> = {
  muted: "var(--fg-3)",
  default: "var(--fg-0)",
  accent: "var(--accent)",
};

export function HeroTerminal({
  profile,
  site,
}: {
  profile: ProfileResponse;
  site: SiteResponse;
}) {
  const user = profile.profile;
  const copy = site.site;

  // 히어로 문구는 site_config 다 — profile 은 신원·연락만(erd.md §site_config).
  const headline = copy.home?.heroHeadline ?? [];
  const lines = copy.home?.heroTerminal ?? [];

  const [step, setStep] = useState(0);
  useEffect(() => {
    if (step >= lines.length) return;
    const id = setTimeout(() => setStep((s) => s + 1), 700);
    return () => clearTimeout(id);
  }, [step, lines.length]);

  return (
    <section
      className="pad-x m-stack"
      style={{
        padding: "64px 80px 48px",
        display: "grid",
        gridTemplateColumns: "1.2fr 1fr",
        gap: 48,
        alignItems: "center",
        minHeight: 600,
      }}
    >
      <div>
        <div
          className="mono"
          style={{ fontSize: 12, color: "var(--fg-3)", marginBottom: 16 }}
        >
          // {"포트폴리오"} · v0.1.0
        </div>
        <h1
          className="m-display"
          style={{
            fontSize: 68,
            lineHeight: 1.05,
            letterSpacing: "-0.03em",
            margin: "0 0 22px",
            fontWeight: 600,
          }}
        >
          {headline.map((line, i) => (
            <span key={i} style={{ color: TONE_COLOR[line.tone], display: "block" }}>
              {line.text}
            </span>
          ))}
        </h1>
        <p
          style={{
            fontSize: 16,
            color: "var(--fg-1)",
            lineHeight: 1.7,
            margin: "0 0 28px",
            maxWidth: 480,
          }}
        >
          {copy.home?.heroSubline}
        </p>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <Link href="/projects" className="btn primary">
            프로젝트 보기 <span className="arrow">→</span>
          </Link>
          {user.github && (
            <a
              href={`https://${user.github}`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn ghost"
            >
              GitHub <span className="arrow">↗</span>
            </a>
          )}
        </div>
      </div>

      <div
        style={{
          background: "var(--bg-1)",
          border: "1px solid var(--line-1)",
          borderRadius: 6,
          fontFamily: "var(--font-mono)",
          fontSize: 12.5,
          lineHeight: 1.7,
          overflow: "hidden",
          boxShadow: "var(--shadow-card)",
        }}
      >
        <div
          style={{
            display: "flex",
            gap: 6,
            padding: "10px 12px",
            borderBottom: "1px solid var(--line-1)",
            alignItems: "center",
          }}
        >
          <span
            style={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              background: "#3a3f48",
            }}
          />
          <span
            style={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              background: "#3a3f48",
            }}
          />
          <span
            style={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              background: "#3a3f48",
            }}
          />
          <span style={{ marginLeft: 8, color: "var(--fg-3)", fontSize: 11 }}>
            ~/kknaks — zsh
          </span>
        </div>
        <div style={{ padding: 16, color: "var(--fg-1)", minHeight: 280 }}>
          {lines.slice(0, step + 1).map((l, i) => (
            <div key={i} style={{ marginBottom: i < step ? 10 : 0 }}>
              <div>
                <span style={{ color: "var(--accent)" }}>$</span> {l.prompt}
              </div>
              {i < step &&
                l.output.map((o, j) => (
                  <div
                    key={j}
                    style={{
                      color: j === 0 ? "var(--fg-0)" : "var(--fg-1)",
                    }}
                  >
                    {o}
                  </div>
                ))}
              {i === step && (
                <span
                  style={{
                    display: "inline-block",
                    width: 8,
                    height: 14,
                    background: "var(--accent)",
                    verticalAlign: "middle",
                    marginLeft: 4,
                    animation: "blink 1s steps(2) infinite",
                  }}
                />
              )}
            </div>
          ))}
          {step >= lines.length && (
            <div>
              <span style={{ color: "var(--accent)" }}>$</span>{" "}
              <span
                style={{
                  display: "inline-block",
                  width: 8,
                  height: 14,
                  background: "var(--accent)",
                  verticalAlign: "middle",
                  animation: "blink 1s steps(2) infinite",
                }}
              />
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
