import { notFound } from "next/navigation";

import { api } from "@/lib/api";
import { DEFAULT_LANG, isLang, type Lang } from "@/lib/i18n";
import { ProjectDetail } from "@/components/projects/project-detail";

export const dynamic = "force-dynamic";

export default async function ProjectDetailPage({
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

  let projects;
  try {
    projects = await api.projects(lang);
  } catch (err) {
    return (
      <main className="pad-x" style={{ padding: "56px 80px" }}>
        <h1>Projects</h1>
        <p style={{ color: "var(--danger)" }}>
          {t("백엔드 응답 실패", "Backend error")}: {(err as Error).message}
        </p>
      </main>
    );
  }

  const items = projects["projects[]"];
  const sorted = [...items].sort((a, b) =>
    (b.date ?? "").localeCompare(a.date ?? ""),
  );
  const idx = sorted.findIndex((p) => p.id === id);
  if (idx === -1) notFound();

  const item = sorted[idx];
  const newer =
    idx > 0
      ? { id: sorted[idx - 1].id, title: sorted[idx - 1].title }
      : null;
  const older =
    idx < sorted.length - 1
      ? { id: sorted[idx + 1].id, title: sorted[idx + 1].title }
      : null;

  return (
    <main>
      <ProjectDetail item={item} newer={newer} older={older} lang={lang} />
    </main>
  );
}
