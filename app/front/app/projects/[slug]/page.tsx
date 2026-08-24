import { notFound } from "next/navigation";

import { api } from "@/lib/api";
import { ProjectDetail } from "@/components/projects/project-detail";

export const dynamic = "force-dynamic";

export default async function ProjectDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;

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

  const items = projects["projects[]"];
  const sorted = [...items].sort((a, b) =>
    (b.startedOn ?? "").localeCompare(a.startedOn ?? ""),
  );
  const idx = sorted.findIndex((p) => p.slug === slug);
  if (idx === -1) notFound();

  const item = sorted[idx];
  // 이전/다음은 컬럼이 아니라 정렬의 이웃이다.
  const newer =
    idx > 0 ? { slug: sorted[idx - 1].slug, title: sorted[idx - 1].title } : null;
  const older =
    idx < sorted.length - 1
      ? { slug: sorted[idx + 1].slug, title: sorted[idx + 1].title }
      : null;

  return (
    <main>
      <ProjectDetail item={item} newer={newer} older={older} />
    </main>
  );
}
