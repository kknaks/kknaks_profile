import { api } from "@/lib/api";
import { DEFAULT_LANG, isLang, type Lang } from "@/lib/i18n";
import { HeroTerminal } from "@/components/home/hero-terminal";
import { LandingPreview } from "@/components/home/landing-preview";

export const dynamic = "force-dynamic";

export default async function HomePage({
  searchParams,
}: {
  searchParams: Promise<{ lang?: string }>;
}) {
  const { lang: rawLang } = await searchParams;
  const lang: Lang = rawLang && isLang(rawLang) ? rawLang : DEFAULT_LANG;

  try {
    const [me, career, projects, notesGraph, notesRecent, contents] =
      await Promise.all([
        api.me(lang),
        api.career(lang),
        api.projects(lang),
        api.notesGraph(),
        api.notesRecent(lang, 5),
        api.contents(lang, 5),
      ]);

    return (
      <main className="page-fade">
        <HeroTerminal lang={lang} me={me} />
        <LandingPreview
          lang={lang}
          me={me}
          career={career}
          projects={projects}
          notesGraph={notesGraph}
          notesRecent={notesRecent["notes.recent[]"]}
          contents={contents}
        />
      </main>
    );
  } catch (err) {
    return (
      <main className="pad-x" style={{ padding: "56px 80px" }}>
        <h1 style={{ fontSize: 32, marginBottom: 16 }}>kknaks.dev</h1>
        <p style={{ color: "var(--danger)" }}>
          백엔드 응답 실패: {(err as Error).message}
        </p>
        <p style={{ color: "var(--fg-2)" }}>
          uvicorn 서버가 실행 중인지 확인하세요 (port 48000).
        </p>
      </main>
    );
  }
}
