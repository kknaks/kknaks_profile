import type { NextConfig } from "next";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:48000";

const nextConfig: NextConfig = {
  // SSG/SSR 기본. M8에서 output: "standalone" 검토

  // /assets/* → 백엔드 정적 서빙 (spec-01 §2.5, spec-02 §2)
  // md frontmatter URL 필드(`/assets/profile/me.png`)가 동일 origin으로 풀리도록 proxy.
  async rewrites() {
    return [
      {
        source: "/assets/:path*",
        destination: `${API_BASE}/assets/:path*`,
      },
    ];
  },
};

export default nextConfig;
