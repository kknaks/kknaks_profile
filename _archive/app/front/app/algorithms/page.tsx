import { api } from "@/lib/api";
import { DEFAULT_LANG, isLang, type Lang } from "@/lib/i18n";
import { AlgorithmsList } from "@/components/algorithms/algorithms-list";

export const dynamic = "force-dynamic";

export default async function AlgorithmsPage({
  searchParams,
}: {
  searchParams: Promise<{ lang?: string }>;
}) {
  const { lang: rawLang } = await searchParams;
  const lang: Lang = rawLang && isLang(rawLang) ? rawLang : DEFAULT_LANG;
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);

  let data;
  try {
    data = await api.algorithms(lang);
  } catch (err) {
    return (
      <main className="pad-x" style={{ padding: "56px 80px" }}>
        <h1>Algorithms</h1>
        <p style={{ color: "var(--danger)" }}>
          {t("백엔드 응답 실패", "Backend error")}: {(err as Error).message}
        </p>
      </main>
    );
  }

  const meta = data.algorithms;
  const items = data["algorithms[]"];

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
          06 / Algorithms · {meta.subtitle}
        </div>
        <div
          style={{ display: "flex", alignItems: "baseline", gap: 16, flexWrap: "wrap" }}
        >
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
            Interview Trace
          </h1>
          <span className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
            // neetcode 150 · 키보드 없는 코딩 면접 도장
          </span>
        </div>
        <p
          style={{
            margin: "20px 0 0",
            fontSize: 15,
            color: "var(--fg-1)",
            maxWidth: 720,
            lineHeight: 1.6,
          }}
        >
          {meta.intro}
        </p>
      </header>

      <AlgorithmsList meta={meta} items={items} lang={lang} />
    </main>
  );
}
