"use client";

import { useState } from "react";

/**
 * YouTube 썸네일 — 단순 img + onError fallback (maxresdefault → hqdefault).
 * 재생 안 함. 부모 Link 가 클릭 시 상세 페이지 이동 처리.
 */
export function YouTubeThumbnail({
  id,
  title,
}: {
  id: string;
  title: string;
}) {
  const [src, setSrc] = useState(
    `https://i.ytimg.com/vi/${id}/maxresdefault.jpg`,
  );
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={src}
      alt={title}
      onError={() => setSrc(`https://i.ytimg.com/vi/${id}/hqdefault.jpg`)}
      style={{
        width: "100%",
        height: "100%",
        objectFit: "cover",
        display: "block",
      }}
    />
  );
}
