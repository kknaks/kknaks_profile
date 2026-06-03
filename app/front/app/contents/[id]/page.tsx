import { notFound } from "next/navigation";

import { api } from "@/lib/api";
import { DEFAULT_LANG, isLang, type Lang } from "@/lib/i18n";
import { ContentsDetail } from "@/components/contents/contents-detail";

export const dynamic = "force-dynamic";

export default async function ContentDetailPage({
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

  let data;
  try {
    data = await api.contentDetail(id, lang);
  } catch (err) {
    const msg = (err as Error).message;
    if (msg.includes("404")) notFound();
    return (
      <main className="pad-x" style={{ padding: "56px 80px" }}>
        <h1>Contents</h1>
        <p style={{ color: "var(--danger)" }}>
          {t("백엔드 응답 실패", "Backend error")}: {msg}
        </p>
      </main>
    );
  }

  const item = data["contents.detail"];

  return (
    <main>
      <ContentsDetail item={item} lang={lang} />
    </main>
  );
}
