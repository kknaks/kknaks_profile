import { defineConfig } from 'vite';
export default defineConfig({
  esbuild: { jsx: 'automatic' },
  server: { host: '127.0.0.1', port: 13000, strictPort: true, proxy: { '/api': 'http://127.0.0.1:18000' } },
});
