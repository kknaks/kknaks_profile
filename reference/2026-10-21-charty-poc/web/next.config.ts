import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@medisolve-ai/medikit'],
};

export default nextConfig;
