import Link from "next/link";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";

import { api } from "@/lib/api";
import { DEFAULT_LANG, isLang, type Lang } from "@/lib/i18n";

export const dynamic = "force-dynamic";

/**
 * 공개 글 상세 — **md 렌더링만** 한다 (KDEV-DEC-021).
 *
 * 본문 형식은 `templates/persona/post-*.md` 가 정한다(주제 · 개념 · 사용 예시 ·
 * 리스크 · 비슷한 개념). 여기서 절을 다시 조립하지 않는 이유가 그것이다 — 조립하면
 * 양식 SoT 가 둘이 되고, 템플릿만 고친 날 화면이 조용히 어긋난다. 교안(`/contents`)이
 * 섹션 헤더를 코드로 그리는 것과 다른 선택이고, 글은 절 구성이 자유롭기 때문이다.
 */
export default async function PostDetailPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ lang?: string }>;
}) {
  const { id } = await params;
  const { lang: rawLang } = await searchParams;
  const lang: Lang = rawLang && isLang(rawLang) ? rawLang : DEFAULT_LANG;
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);
  const langSuffix = lang === "en" ? "?lang=en" : "";

  let data;
  try {
    data = await api.postDetail(id, lang);
  } catch {
    notFound();
  }

  const post = data["posts.detail"];
  const kind =
    post.type === "post_note" ? t("공부", "note") : t("스크랩", "scrap");

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
          href={`/notes${langSuffix}`}
          className="mono"
          style={{
            color: "var(--fg-3)",
            fontSize: 12,
            textDecoration: "none",
            display: "inline-block",
            marginBottom: 20,
          }}
        >
          ← {t("전체 글", "all posts")}
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
          <span
            style={{
              color: post.type === "post_note" ? "var(--accent)" : "var(--fg-3)",
            }}
          >
            ● {kind}
          </span>
          <span>{post.date}</span>
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
          {post.title}
        </h1>
        {!!post.stack?.length && (
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
            {post.stack.map((s) => (
              <span key={s}>{s}</span>
            ))}
          </div>
        )}
      </header>

      <section className="pad-x" style={{ padding: "32px 80px" }}>
        {/* `contents-body` 를 그대로 쓴다 — md 본문 타이포는 한 곳이 정한다. */}
        <article className="contents-body">
          <ReactMarkdown>{post.body}</ReactMarkdown>
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
        {post.newer ? (
          <NeighborCard
            href={`/notes/${post.newer.id}${langSuffix}`}
            label={`← ${t("다음 글", "newer")}`}
            title={post.newer.title}
          />
        ) : (
          <div />
        )}
        {post.older ? (
          <NeighborCard
            href={`/notes/${post.older.id}${langSuffix}`}
            label={`${t("이전 글", "older")} →`}
            title={post.older.title}
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
