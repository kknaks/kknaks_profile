import { api } from "@/lib/api";
import { DEFAULT_LANG, isLang, type Lang } from "@/lib/i18n";
import { PostsList } from "@/components/notes/posts-list";

export const dynamic = "force-dynamic";

export default async function NotesPage({
  searchParams,
}: {
  searchParams: Promise<{ lang?: string }>;
}) {
  const { lang: rawLang } = await searchParams;
  const lang: Lang = rawLang && isLang(rawLang) ? rawLang : DEFAULT_LANG;
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);

  let data;
  try {
    data = await api.posts(lang);
  } catch (err) {
    return (
      <main className="pad-x" style={{ padding: "56px 80px" }}>
        <h1>Notes</h1>
        <p style={{ color: "var(--danger)" }}>
          백엔드 응답 실패: {(err as Error).message}
        </p>
      </main>
    );
  }

  const posts = data["posts[]"];

  return (
    <main>
      <header
        className="pad-x m-pad-h"
        style={{
          padding: "56px 80px 32px",
          borderBottom: "1px solid var(--line-1)",
        }}
      >
        <div
          className="mono"
          style={{
            fontSize: 11,
            color: "var(--fg-3)",
            textTransform: "uppercase",
            letterSpacing: "0.14em",
            marginBottom: 12,
          }}
        >
          04 / Notes · {data.posts.subtitle}
        </div>
        <div style={{ display: "flex", alignItems: "baseline", gap: 16, flexWrap: "wrap" }}>
          <h1
            className="m-h1"
            style={{
              fontSize: 56,
              lineHeight: 1.05,
              letterSpacing: "-0.025em",
              margin: 0,
              fontWeight: 600,
            }}
          >
            Notes
          </h1>
          <span className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
            {data.posts.totalCount} {t("글", "posts")}
          </span>
        </div>
      </header>

      <PostsList items={posts} lang={lang} />
    </main>
  );
}
