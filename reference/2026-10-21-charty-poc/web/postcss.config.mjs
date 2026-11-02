// base.css 안의 @tailwind 지시문을 처리하려면 import 가 먼저 인라인돼야 한다(SPEC §8-1).
const config = {
  plugins: {
    'postcss-import': {},
    tailwindcss: {},
    autoprefixer: {},
  },
};

export default config;
