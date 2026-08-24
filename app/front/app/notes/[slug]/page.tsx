import Link from "next/link";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";

import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

/**
 * 공개 글 상세 — **md 렌더링만** 한다.
 *
 * 본문은 `note.detail_path` 가 가리키는 md 를 백엔드가 읽어 `body` 로 내려준 것이다
 * (erd.md §상세 본문은 DB 에 없다). 여기서 절을 다시 조립하지 않는 이유가 그것이다 —
 * 조립하면 양식 SoT 가 둘이 되고, md 만 고친 날 화면이 조용히 어긋난다.
 */
export default async function NoteDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;

  let data;
  try {
    data = await api.noteDetail(slug);
  } catch {
    notFound();
  }

  const note = data["notes.detail"];

  return (
    <main>
      <header
        className="pad-x m-pad-h"
        style={{
          padding: "40px 80px 32px",
          borderBottom: "1px solid var(--line-1)",
        }}
      >
        <Link
          href="/notes"
          className="mono"
          style={{
            color: "var(--fg-3)",
            fontSize: 12,
            textDecoration: "none",
            display: "inline-block",
            marginBottom: 20,
          }}
        >
          ← 전체 글
        </Link>
        <div
          className="mono"
          style={{
            fontSize: 11,
            color: "var(--fg-3)",
            textTransform: "uppercase",
            letterSpacing: "0.14em",
            marginBottom: 12,
            display: "flex",
            gap: 12,
          }}
        >
          <span>{note.publishedOn ?? ""}</span>
        </div>
        <h1
          className="m-h1"
          style={{
            fontSize: 40,
            lineHeight: 1.15,
            letterSpacing: "-0.02em",
            margin: 0,
            fontWeight: 600,
          }}
        >
          {note.title}
        </h1>
        {!!note.tags?.length && (
          <div
            className="mono"
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: 10,
              marginTop: 16,
              fontSize: 10,
              color: "var(--fg-4)",
            }}
          >
            {note.tags.map((tag) => (
              <span key={tag}>#{tag}</span>
            ))}
          </div>
        )}
      </header>

      <section className="pad-x" style={{ padding: "32px 80px" }}>
        {/* `contents-body` 를 그대로 쓴다 — md 본문 타이포는 한 곳이 정한다. */}
        <article className="contents-body">
          <ReactMarkdown>{note.body}</ReactMarkdown>
        </article>
      </section>

      <nav
        className="pad-x m-stack"
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 16,
          padding: "32px 80px 64px",
          borderTop: "1px solid var(--line-1)",
        }}
      >
        {note.newer ? (
          <NeighborCard
            href={`/notes/${note.newer.slug}`}
            label="← 다음 글"
            title={note.newer.title}
          />
        ) : (
          <div />
        )}
        {note.older ? (
          <NeighborCard
            href={`/notes/${note.older.slug}`}
            label="이전 글 →"
            title={note.older.title}
            alignRight
          />
        ) : (
          <div />
        )}
      </nav>
    </main>
  );
}

function NeighborCard({
  href,
  label,
  title,
  alignRight = false,
}: {
  href: string;
  label: string;
  title: string;
  alignRight?: boolean;
}) {
  return (
    <Link
      href={href}
      className="card"
      style={{
        padding: "20px 24px",
        textAlign: alignRight ? "right" : "left",
        background: "var(--bg-1)",
        border: "1px solid var(--line-1)",
        textDecoration: "none",
        color: "inherit",
      }}
    >
      <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 6 }}>
        {label}
      </div>
      <div style={{ fontSize: 14, color: "var(--fg-0)" }}>{title}</div>
    </Link>
  );
}
