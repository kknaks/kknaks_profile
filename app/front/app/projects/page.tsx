import { api } from "@/lib/api";
import { ProjectsGrid } from "@/components/projects/projects-grid";

export const dynamic = "force-dynamic";

export default async function ProjectsPage() {
  let projects;
  try {
    projects = await api.projects();
  } catch (err) {
    return (
      <main className="pad-x" style={{ padding: "56px 80px" }}>
        <h1>Projects</h1>
        <p style={{ color: "var(--danger)" }}>
          백엔드 응답 실패: {(err as Error).message}
        </p>
      </main>
    );
  }

  const subtitle = projects.projects?.subtitle ?? "혼자 만든 것들";

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
          03 / Projects · {subtitle}
        </div>
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
          Projects
        </h1>
      </header>

      <div className="pad-x" style={{ padding: "32px 80px 64px" }}>
        <ProjectsGrid projects={projects} />
      </div>
    </main>
  );
}
