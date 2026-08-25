"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import type { TimelineItem } from "@/lib/types";

/**
 * `/career` 타임라인. `career` 와 `education` 을 합쳐 받는다 — 화면은 둘을
 * 구분해 보여주지 않는다(database.md §화면에서는 합친다).
 *
 * `isCurrent` · `period` 는 컬럼이 아니라 **백엔드가 계산해 내려준 파생값**이다.
 */
export function CareerTimeline({ items }: { items: TimelineItem[] }) {
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
        // career 항목만 products·problems 를 갖는다 — education 은 body 뿐이다.
        const products = "products" in it ? it.products : [];
        const problems = "problems" in it ? it.problems : [];
        const hasBody = !!it.body && it.body.trim().length > 0;
        const hasDetail = hasBody || products.length > 0 || problems.length > 0;
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
                  it.isCurrent ? "var(--accent)" : "var(--line-3)"
                }`,
                boxShadow: it.isCurrent
                  ? "0 0 0 3px var(--accent-soft)"
                  : "none",
              }}
            />
            <div
              className="mono"
              style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 6 }}
            >
              {it.period}
              {it.isCurrent && (
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

            {hasDetail && (
              <>
                <button
                  type="button"
                  onClick={() => toggle(i)}
                  className="btn ghost"
                  style={{ marginTop: 14, fontSize: 12, padding: "6px 10px" }}
                >
                  {open
                    ? "접기"
                    : "상세보기"}{" "}
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
                      {it.body ?? ""}
                    </ReactMarkdown>

                    {products.length > 0 && (
                      <div style={{ marginTop: hasBody ? 20 : 0 }}>
                        <div
                          className="mono"
                          style={{
                            fontSize: 11,
                            color: "var(--accent)",
                            marginBottom: 10,
                          }}
                        >
                          // 만든 것
                        </div>
                        <div
                          style={{
                            display: "grid",
                            gridTemplateColumns:
                              "repeat(auto-fill, minmax(220px, 1fr))",
                            gap: 12,
                          }}
                        >
                          {products.map((p) => (
                            <div
                              key={p.id}
                              style={{
                                padding: 14,
                                background: "var(--bg-0)",
                                border: "1px solid var(--line-1)",
                                borderRadius: 6,
                              }}
                            >
                              <div
                                style={{
                                  display: "flex",
                                  alignItems: "baseline",
                                  gap: 8,
                                  marginBottom: 6,
                                }}
                              >
                                <span style={{ fontSize: 15, fontWeight: 600 }}>
                                  {p.title}
                                </span>
                                {p.status && (
                                  <span
                                    className="mono"
                                    style={{ fontSize: 10, color: "var(--fg-3)" }}
                                  >
                                    {p.status}
                                  </span>
                                )}
                              </div>
                              {p.summary && (
                                <p
                                  style={{
                                    margin: 0,
                                    fontSize: 13,
                                    lineHeight: 1.6,
                                    color: "var(--fg-1)",
                                  }}
                                >
                                  {p.summary}
                                </p>
                              )}
                              {(p.links?.site || p.links?.docs) && (
                                <div
                                  className="mono"
                                  style={{
                                    marginTop: 8,
                                    fontSize: 11,
                                    display: "flex",
                                    gap: 10,
                                  }}
                                >
                                  {p.links?.site && (
                                    <a
                                      href={p.links.site}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      style={{ color: "var(--accent)" }}
                                    >
                                      site ↗
                                    </a>
                                  )}
                                  {p.links?.docs && (
                                    <a
                                      href={p.links.docs}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      style={{ color: "var(--accent)" }}
                                    >
                                      docs ↗
                                    </a>
                                  )}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {problems.length > 0 && (
                      <div
                        style={{
                          marginTop: hasBody || products.length > 0 ? 20 : 0,
                        }}
                      >
                        <div
                          className="mono"
                          style={{
                            fontSize: 11,
                            color: "var(--accent)",
                            marginBottom: 4,
                          }}
                        >
                          // 해결한 문제
                        </div>
                        {problems.map((pr) => (
                          <div
                            key={pr.id}
                            style={{
                              padding: "10px 0",
                              borderTop: "1px solid var(--line-1)",
                            }}
                          >
                            <div
                              style={{
                                display: "flex",
                                alignItems: "baseline",
                                gap: 8,
                                flexWrap: "wrap",
                              }}
                            >
                              <span style={{ fontSize: 14, fontWeight: 600 }}>
                                {pr.title}
                              </span>
                              {pr.productTitle && (
                                <span
                                  className="mono"
                                  style={{ fontSize: 10, color: "var(--fg-3)" }}
                                >
                                  @ {pr.productTitle}
                                </span>
                              )}
                            </div>
                            {pr.body && (
                              <p
                                style={{
                                  margin: "6px 0 0",
                                  fontSize: 13,
                                  lineHeight: 1.65,
                                  color: "var(--fg-1)",
                                }}
                              >
                                {pr.body}
                              </p>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
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
