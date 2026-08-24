"use client";

import { useState } from "react";

/**
 * YouTube lazy embed — 썸네일 → 클릭 시 iframe (재생 상태로 swap).
 * maxresdefault 없으면 hqdefault fallback.
 */
export function YouTubeFrame({ id, title }: { id: string; title: string }) {
  const [playing, setPlaying] = useState(false);
  const [thumbSrc, setThumbSrc] = useState(
    `https://i.ytimg.com/vi/${id}/maxresdefault.jpg`,
  );

  if (playing) {
    return (
      <div
        style={{
          position: "relative",
          aspectRatio: "16/9",
          background: "#000",
          overflow: "hidden",
        }}
      >
        <iframe
          src={`https://www.youtube.com/embed/${id}?autoplay=1`}
          title={title}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          style={{ width: "100%", height: "100%", border: 0 }}
        />
      </div>
    );
  }

  return (
    <button
      onClick={() => setPlaying(true)}
      aria-label={`Play ${title}`}
      style={{
        position: "relative",
        aspectRatio: "16/9",
        background: "#000",
        overflow: "hidden",
        border: 0,
        padding: 0,
        cursor: "pointer",
        width: "100%",
        display: "block",
      }}
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={thumbSrc}
        alt={title}
        onError={() =>
          setThumbSrc(`https://i.ytimg.com/vi/${id}/hqdefault.jpg`)
        }
        style={{ width: "100%", height: "100%", objectFit: "cover" }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          pointerEvents: "none",
        }}
      >
        <div
          style={{
            width: 64,
            height: 64,
            borderRadius: "50%",
            background: "var(--accent)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "0 0 0 6px rgba(0,0,0,0.4)",
          }}
        >
          <div
            style={{
              width: 0,
              height: 0,
              borderLeft: "18px solid var(--accent-ink)",
              borderTop: "12px solid transparent",
              borderBottom: "12px solid transparent",
              marginLeft: 5,
            }}
          />
        </div>
      </div>
      <div
        className="mono"
        style={{
          position: "absolute",
          bottom: 10,
          right: 12,
          fontSize: 11,
          color: "var(--fg-2)",
          background: "rgba(0,0,0,0.5)",
          padding: "3px 8px",
          borderRadius: 3,
        }}
      >
        ▶ {title.length > 40 ? title.slice(0, 40) + "…" : title}
      </div>
    </button>
  );
}
