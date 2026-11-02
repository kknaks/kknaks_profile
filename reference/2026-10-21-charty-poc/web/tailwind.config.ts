import type { Config } from 'tailwindcss';
import { medikitPreset } from '@medisolve-ai/medikit/tailwind';

const config: Config = {
  content: ['./src/**/*.{ts,tsx}', './node_modules/@medisolve-ai/medikit/dist/**/*.{js,mjs}'],
  presets: [medikitPreset],
  theme: { extend: {} },
};

export default config;
