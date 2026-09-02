"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/**
 * 짧은 글 렌더러 — 원장 md 가 아니라 **컬럼에 든 글**을 그린다.
 *
 * `career.description` 과 `problem.body` 가 여기 온다. 둘은 detail_path 가 없다
 * (erd.md §career — 짧은 글은 컬럼이 낫다). 그래서 이미지 상대참조도 mermaid 도
 * 없고, 대신 화면 타이포에 맞춘 태그별 스타일이 붙는다.
 *
 * career-view 의 `DetailPanel` 안에 인라인으로 있던 것을 그대로 끌어올렸다 —
 * `/chat` 문서 패널이 career · problem 을 같은 모양으로 그려야 하기 때문이다.
 * 스타일 값은 한 자도 바꾸지 않았다(career 페이지 무회귀).
 */
export function ProseBody({ body }: { body?: string | null }) {
  if (!body || body.trim().length === 0) return null;

  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
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
        li: ({ children }) => <li style={{ marginBottom: 4 }}>{children}</li>,
        strong: ({ children }) => (
          <strong style={{ color: "var(--accent)", fontWeight: 600 }}>
            {children}
          </strong>
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
      {body}
    </ReactMarkdown>
  );
}
