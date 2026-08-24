import { notFound } from "next/navigation";

import { api } from "@/lib/api";
import { ContentsDetail } from "@/components/contents/contents-detail";

export const dynamic = "force-dynamic";

export default async function ContentDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;

  let data;
  try {
    data = await api.contentDetail(slug);
  } catch (err) {
    const msg = (err as Error).message;
    if (msg.includes("404")) notFound();
    return (
      <main className="pad-x" style={{ padding: "56px 80px" }}>
        <h1>Contents</h1>
        <p style={{ color: "var(--danger)" }}>
          백엔드 응답 실패: {msg}
        </p>
      </main>
    );
  }

  const item = data["contents.detail"];

  return (
    <main>
      <ContentsDetail item={item} />
    </main>
  );
}
