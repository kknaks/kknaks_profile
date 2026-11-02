# 폰 피드백 1 — frontend 결과 보고 (D-27 · D-28)

## 상태: done (화면 · 실기기 확인은 pending — 아래)

워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc`(main 046eabe 위 · 커밋 없음). 범위 `front/**` 만(backend 절은 backend 워커 — 코디 지시). back 의 lang 값 `'zh-Hant'` 에 맞춤.

## 수행 — 파일

| 파일 | 무엇 |
|---|---|
| `front/lib/langs.ts` | **D-28** `LANGS` 에 `'zh-Hant'`(순서 en · ja · zh · **zh-Hant** · th · vi · yue — 드롭다운 「中文(简体)」 · 「中文(繁體)」 붙여 둠 · 「廣東話」 끝) · `LANG_LABEL['zh-Hant']` = 「中文(繁體)」 · `LANG_KO` 「중국어(번체)」 · 외국어 안내 문구 번체 한 벌(출력 언어 이름 「中文」 — TTS 는 만다린) · `htmlLang()` 을 여기로(zh-Hant · yue → `lang="zh-Hant"`) |
| `front/components/interpret/InterpretScreen.tsx` · `GlossaryModal.tsx` | 공용 `htmlLang` 사용(용어집 칸 · 영역 · 안내 `lang` 속성). 용어집 패널은 `GET /api/glossary?lang=zh-Hant` 를 그대로 부름(번체 표시는 back) · 제목 「용어집 · 中文(繁體)」 |
| `front/app/login/page.tsx` | **D-27** 아이디 · 비밀번호 medikit `Input` 에 `inputClassName="text-typo-heading-md-400"`(16px). viewport `maximumScale` · `userScalable` 안 씀(`layout.tsx` 그대로) |
| `front/tests/langs.test.ts`(새) | zh-Hant 표기 · `isLang` · 번체 안내 · 출력 언어 · 7개 언어 문구 빠짐 없음 · `htmlLang` |

- 그 밖 입력: 앱에 텍스트 입력은 로그인 두 칸뿐. 언어 `ComboBox` 는 검색 끔(`hasSearch=false`)이라 입력 칸이 없는 단추 — iOS 확대 대상 아님.

## 검증 — 명령과 결과

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과 |
| `npm run build` | 통과 |
| `npx vitest run` | 5 파일 · **27 통과**(새 4) |
| 클래스 대조 `node scripts/check-classes.mjs` | 166 · 없는 것 0 · `text-typo-heading-md-400` 빌드 CSS 에 있음(`font-size:16px`) |
| 16px 실제 적용 | medikit `cn`(tailwind-merge)으로 Input 의 기본 `text-typo-heading-sm-400`(14px)과 합치면 **`text-typo-heading-md-400` 만 남는다**(node 로 확인) — CSS 순서와 무관하게 16px |

## 계약 대조

| DEC | 같음 / 다름 |
|---|---|
| D-27 입력 16px 이상 · 확대 막는 viewport 안 씀 | 같음 |
| D-28 드롭다운 「中文(简体)」 · 「中文(繁體)」 · 「廣東話」 · start `lang:"zh-Hant"` · 용어집 zh-Hant | 같음(front 쪽) — 자막 번체 · TTS 간체 · 용어집 표시 번체는 back |

## 이슈 · 코디가 확인할 것

1. **브라우저 · 화면 확인 못 함**: `:3800` · `:8800` 을 코디의 compose(`interpret-pwa-poc-front-1` · `-back-1` · 046eabe 이미지)가 쓰고 있다. 이 레포는 두 포트만 쓰므로 내 dev 서버는 뜨지 않았다(EADDRINUSE · 남은 프로세스 없음 · compose 는 건드리지 않음). → compose 를 이 변경으로 다시 빌드하면 확인 가능: 드롭다운 7개 · zh-Hant 오버레이 「點擊開始」 · 용어집 zh-Hant(back 반영 뒤) · iPhone 로그인 포커스 확대 없음.
2. **실기기 pending**: iOS Safari 포커스 확대(D-27)는 휴대폰에서만 확인된다.
3. 새 문구(zh-Hant 안내 10개)는 zh 간체를 번체로 옮긴 값 — 원어민 검수 없음(OQ-006 범위). 「韓語」(대만식) — yue 는 「韓文」 그대로 둠.
4. `LANG_KO['zh-Hant']` = 「중국어(번체)」 → 원 아래 「중국어(번체)로 출력 중」 · 「중국어(번체) 듣는 중」.
