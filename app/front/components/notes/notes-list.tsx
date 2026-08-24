import Link from "next/link";

import type { NoteItem } from "@/lib/types";

/**
 * 공개 글 목록.
 *
 * 종전 이 자리에는 force-graph 로 그린 노트 그래프가 있었다. 노드가 늘어도 읽을
 * 것이 늘지 않아서 — 원이 몇 개인지 보이는 것과 무엇을 읽을지 고르는 것은 다르다.
 * 지금은 **읽을 것을 고르는 목록**이고, 상세는 md 를 그대로 렌더한다.
 *
 * 옛 `post_article` / `post_note` 구분은 없어졌다 — `erd.md` 의 `note` 에는
 * 종류 컬럼이 없다. 분류가 필요하면 `tags` 가 진다.
 */
export function NotesList({ items }: { items: NoteItem[] }) {
  if (items.length === 0) {
    return (
      <section className="pad-x" style={{ padding: "80px" }}>
        <p style={{ color: "var(--fg-3)", fontSize: 14, margin: 0 }}>
          아직 정리한 글이 없습니다.
        </p>
      </section>
    );
  }

  return (
    <section className="pad-x" style={{ padding: "40px 80px 80px" }}>
      <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
        {items.map((note) => (
          <li key={note.slug} style={{ borderBottom: "1px solid var(--line-1)" }}>
            <Link
              href={`/notes/${note.slug}`}
              style={{
                display: "block",
                padding: "22px 0",
                textDecoration: "none",
                color: "inherit",
              }}
            >
              <div
                className="mono"
                style={{
                  display: "flex",
                  gap: 12,
                  fontSize: 11,
                  color: "var(--fg-3)",
                  marginBottom: 8,
                }}
              >
                <span>{note.publishedOn ?? ""}</span>
              </div>
              <div
                style={{
                  fontSize: 18,
                  color: "var(--fg-0)",
                  letterSpacing: "-0.01em",
                }}
              >
                {note.title}
              </div>
              {note.summary && (
                <p
                  style={{
                    margin: "8px 0 0",
                    fontSize: 13,
                    lineHeight: 1.6,
                    color: "var(--fg-2)",
                  }}
                >
                  {note.summary}
                </p>
              )}
              {!!note.tags?.length && (
                <div
                  className="mono"
                  style={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: 8,
                    marginTop: 10,
                    fontSize: 10,
                    color: "var(--fg-4)",
                  }}
                >
                  {note.tags.map((tag) => (
                    <span key={tag}>#{tag}</span>
                  ))}
                </div>
              )}
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}
