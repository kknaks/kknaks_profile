import type { ProjectItem } from "@/lib/types";

const STATUS_COLOR: Record<string, string> = {
  live: "var(--accent)",
  wip: "var(--info)",
  archived: "var(--fg-3)",
};

export function StatusTag({ s }: { s: ProjectItem["status"] }) {
  if (!s) return null;
  const isLive = s === "live";
  return (
    <span
      className="tag"
      style={{
        fontSize: 9,
        padding: "1px 6px",
        ...(isLive
          ? {
              color: "var(--accent)",
              background: "var(--accent-soft)",
              borderColor: "var(--accent-line)",
            }
          : {}),
      }}
    >
      <span
        className="tag-dot"
        style={{ background: STATUS_COLOR[s], width: 4, height: 4 }}
      />
      {s}
    </span>
  );
}
