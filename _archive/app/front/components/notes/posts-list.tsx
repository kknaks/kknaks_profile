import Link from "next/link";

import type { Lang } from "@/lib/i18n";
import type { PostItem, PostType } from "@/lib/types";

/**
 * 공개 글 목록 (KDEV-DEC-021).
 *
 * 종전 이 자리에는 force-graph 로 그린 노트 그래프가 있었다. 노드가 늘어도 읽을
 * 것이 늘지 않아서 — 원이 몇 개인지 보이는 것과 무엇을 읽을지 고르는 것은 다르다.
 * 지금은 **읽을 것을 고르는 목록**이고, 상세는 md 를 그대로 렌더한다.
 */

const TYPE_LABEL: Record<PostType, { ko: string; en: string; color: string }> = {
  // 갈리는 기준은 **누가 말한 것인가**다 — 자료의 요지면 스크랩, 내 이해면 공부.
  post_article: { ko: "스크랩", en: "scrap", color: "var(--fg-3)" },
  post_note: { ko: "공부", en: "note", color: "var(--accent)" },
};

export function PostsList({ items, lang }: { items: PostItem[]; lang: Lang }) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);
  const langSuffix = lang === "en" ? "?lang=en" : "";

  if (items.length === 0) {
    return (
      <section className="pad-x" style={{ padding: "80px" }}>
        <p style={{ color: "var(--fg-3)", fontSize: 14, margin: 0 }}>
          {t("아직 정리한 글이 없습니다.", "No posts yet.")}
        </p>
      </section>
    );
  }

  return (
    <section className="pad-x" style={{ padding: "40px 80px 80px" }}>
      <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
        {items.map((post) => {
          const kind = TYPE_LABEL[post.type];
          return (
            <li key={post.id} style={{ borderBottom: "1px solid var(--line-1)" }}>
              <Link
                href={`/notes/${post.id}${langSuffix}`}
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
                  {kind && (
                    <span style={{ color: kind.color }}>
                      ● {t(kind.ko, kind.en)}
                    </span>
                  )}
                  <span>{post.date}</span>
                </div>
                <div
                  style={{
                    fontSize: 18,
                    color: "var(--fg-0)",
                    letterSpacing: "-0.01em",
                  }}
                >
                  {post.title}
                </div>
                {post.summary && (
                  <p
                    style={{
                      margin: "8px 0 0",
                      fontSize: 13,
                      lineHeight: 1.6,
                      color: "var(--fg-2)",
                    }}
                  >
                    {post.summary}
                  </p>
                )}
                {!!post.stack?.length && (
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
                    {post.stack.map((s) => (
                      <span key={s}>{s}</span>
                    ))}
                  </div>
                )}
              </Link>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
