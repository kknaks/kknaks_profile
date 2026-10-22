import { defineConfig, devices } from '@playwright/test';

// 포트 3417 고정(사용자 포트를 건드리지 않는다). 산출물은 node_modules/.cache 아래(커밋 대상 밖).
export default defineConfig({
  testDir: './e2e',
  outputDir: './node_modules/.cache/playwright/results',
  reporter: [['list']],
  timeout: 90_000,
  fullyParallel: false,
  workers: 1,
  use: {
    baseURL: 'http://localhost:3417',
    ...devices['Desktop Chrome'],
    launchOptions: { args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] },
  },
  webServer: {
    command: 'npx next start -p 3417',
    url: 'http://localhost:3417',
    reuseExistingServer: true,
    timeout: 60_000,
  },
});
