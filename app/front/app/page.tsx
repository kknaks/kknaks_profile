import { api } from "@/lib/api";
import { ChatHero } from "@/components/home/chat-hero";
import { LandingPreview } from "@/components/home/landing-preview";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  try {
    const [profile, site, career, projects, notes, contents] = await Promise.all([
      api.profile(),
      api.site(),
      api.career(),
      api.projects(),
      api.notes(5),
      api.contents(5),
    ]);

    return (
      <main className="page-fade">
        {/* 첫 화면은 채팅 히어로 한 화면 — 아래로 스크롤하면 기존 프리뷰가 이어진다
            (KDEV-DEC-025 D1. 히어로 터미널은 폐기했다). */}
        <ChatHero />
        <LandingPreview
          profile={profile}
          site={site}
          career={career}
          projects={projects}
          notes={notes}
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
