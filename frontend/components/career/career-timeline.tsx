"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import type { Lang } from "@/lib/i18n";
import type { CareerItem } from "@/lib/types";

export function CareerTimeline({
  items,
  lang,
}: {
  items: CareerItem[];
  lang: Lang;
}) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);
  const [expanded, setExpanded] = useState<Set<number>>(new Set());

  const toggle = (i: number) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(i)) next.delete(i);
      else next.add(i);
      return next;
    });
  };

  return (
    <div style={{ position: "relative", paddingLeft: 28 }}>
      <div
        style={{
          position: "absolute",
          left: 5,
          top: 8,
          bottom: 8,
          width: 1,
          background: "var(--line-2)",
        }}
      />
      {items.map((it, i) => {
        const open = expanded.has(i);
        return (
          <div key={i} style={{ position: "relative", marginBottom: 36 }}>
            <span
              style={{
                position: "absolute",
                left: -28,
                top: 8,
                width: 11,
                height: 11,
                borderRadius: 2,
                background: "var(--bg-0)",
                border: `1px solid ${
                  it.is_current ? "var(--accent)" : "var(--line-3)"
                }`,
                boxShadow: it.is_current
                  ? "0 0 0 3px var(--accent-soft)"
                  : "none",
              }}
            />
            <div
              className="mono"
              style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 6 }}
            >
              {it.period}
              {it.is_current && (
                <span style={{ color: "var(--accent)", marginLeft: 8 }}>
                  ● now
                </span>
              )}
            </div>
            <div
              style={{
                display: "flex",
                alignItems: "baseline",
                gap: 8,
                marginBottom: 6,
                flexWrap: "wrap",
              }}
            >
              <h3
                style={{
                  margin: 0,
                  fontSize: 20,
                  letterSpacing: "-0.01em",
                }}
              >
                {it.title}
              </h3>
              <span style={{ color: "var(--fg-3)" }}>·</span>
              <span style={{ color: "var(--fg-1)", fontSize: 16 }}>
                {it.org}
              </span>
              {it.location && (
                <span
                  className="mono"
                  style={{
                    marginLeft: "auto",
                    fontSize: 11,
                    color: "var(--fg-3)",
                  }}
                >
                  {it.location}
                </span>
              )}
            </div>
            <p
              style={{
                margin: "0 0 10px",
                color: "var(--fg-1)",
                fontSize: 14,
                lineHeight: 1.6,
                maxWidth: 640,
              }}
            >
              {it.summary}
            </p>
            {it.stack && it.stack.length > 0 && (
              <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                {it.stack.map((s) => (
                  <span key={s} className="tag">
                    {s}
                  </span>
                ))}
              </div>
            )}

            {it.body && it.body.trim().length > 0 && (
              <>
                <button
                  type="button"
                  onClick={() => toggle(i)}
                  className="btn ghost"
                  style={{ marginTop: 14, fontSize: 12, padding: "6px 10px" }}
                >
                  {open
                    ? t("접기", "Collapse")
                    : t("상세보기", "Read more")}{" "}
                  <span className="arrow">{open ? "↑" : "↓"}</span>
                </button>
                {open && (
                  <div
                    style={{
                      marginTop: 16,
                      padding: "20px 24px",
                      background: "var(--bg-1)",
                      border: "1px solid var(--line-1)",
                      borderRadius: 6,
                      maxWidth: 720,
                    }}
                  >
                    <ReactMarkdown
                      components={{
                        h1: ({ children }) => (
                          <h2
                            style={{
                              fontSize: 20,
                              fontWeight: 600,
                              marginTop: 0,
                              marginBottom: 12,
                              letterSpacing: "-0.01em",
                            }}
                          >
                            {children}
                          </h2>
                        ),
                        h2: ({ children }) => (
                          <h3
                            style={{
                              fontSize: 15,
                              fontWeight: 500,
                              color: "var(--fg-0)",
                              marginTop: 20,
                              marginBottom: 8,
                            }}
                          >
                            {children}
                          </h3>
                        ),
                        h3: ({ children }) => (
                          <h4
                            style={{
                              fontSize: 14,
                              fontWeight: 500,
                              color: "var(--fg-1)",
                              marginTop: 16,
                              marginBottom: 6,
                            }}
                          >
                            {children}
                          </h4>
                        ),
                        p: ({ children }) => (
                          <p
                            style={{
                              fontSize: 14,
                              lineHeight: 1.7,
                              color: "var(--fg-1)",
                              margin: "0 0 12px",
                            }}
                          >
                            {children}
                          </p>
                        ),
                        ul: ({ children }) => (
                          <ul
                            style={{
                              fontSize: 14,
                              lineHeight: 1.7,
                              color: "var(--fg-1)",
                              paddingLeft: 20,
                              margin: "0 0 12px",
                            }}
                          >
                            {children}
                          </ul>
                        ),
                        li: ({ children }) => (
                          <li style={{ marginBottom: 4 }}>{children}</li>
                        ),
                        code: ({ children }) => (
                          <code
                            style={{
                              fontFamily: "var(--font-mono)",
                              fontSize: 12,
                              background: "var(--bg-2)",
                              padding: "1px 6px",
                              borderRadius: 3,
                            }}
                          >
                            {children}
                          </code>
                        ),
                        a: ({ href, children }) => (
                          <a
                            href={href}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{ color: "var(--accent)" }}
                          >
                            {children}
                          </a>
                        ),
                      }}
                    >
                      {it.body}
                    </ReactMarkdown>
                  </div>
                )}
              </>
            )}
          </div>
        );
      })}
    </div>
  );
}
