# WORK-001 WP10 결과 보고 — front 용어집 메뉴 별칭 · 검수 표시 (D-33)

## 상태: done (실 back(WP9 시드) 스크린샷은 pending — 아래 이슈 1)

워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc`(HEAD 9c9939c · 커밋 없음). 범위 `front/**` 만 — 그 밖 화면은 안 건드림.

## 수행 — 파일

| 파일 | 무엇 |
|---|---|
| `front/lib/api.ts` | `GlossaryRow` = SPEC 0.4.0 §4.7 `{id, category, ko, koAliases, term, aliases, reviewed}` |
| `front/lib/glossary.ts`(새) | `glossaryRowView(row)` — 별칭 줄(빈 값 거르고 「 · 」로 이음 · 없으면 null) · `unreviewed` = `reviewed === false` 일 때만 |
| `front/components/interpret/GlossaryModal.tsx` | 칸 수 · 폭(34/30/36) · 부제(그 언어 `count`) 그대로. 한국어 칸 = `ko` + 아래 줄 `koAliases` · 고른 언어 칸 = `term`(현지명) + `reviewed:false` 면 「검수 전」 꼬리표(`bg-ms-gray-200 text-ms-gray-700 text-typo-caption-md-500` · 둥글기 4 · 안쪽 1/6 · `lang="ko"`) + 아래 줄 `aliases`. 별칭 줄 = `text-typo-caption-md-400 text-ms-gray-600`(§7.6 표). 행 key = `id`. `loaded=false` 문구는 남김(닿지 않는 경로 · 계약 영향 없음) |
| `front/tests/glossary.test.ts`(새) | 별칭 줄(있음 · 비어 있음 · 공백만) · 꼬리표는 `reviewed:false` 에서만 |

## 검증

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과 |
| `npm run build` | 통과 |
| `npx vitest run` | 7 파일 · **30 통과**(새 2) |
| 클래스 대조 | 197 · 없는 것 0(꼬리표 · 별칭 줄 클래스 포함 — 상수 `ALIAS` · `TAG` 도 대조 대상) |

스크린샷 `wp10-fe-shots/`(390 × 844) — **§4.7 모양 목업**(가짜 행 5개 · 시드 값 아님):

| 파일 | 확인 |
|---|---|
| `WP10-glossary-en.png` | 「용어집 · 영어」 · 「5개 · 읽기 전용」 · 별칭 줄(한국어 · 영어) · 꼬리표 0 |
| `WP10-glossary-zh-Hant.png` | 「용어집 · 대만어」 · 꼬리표 4(`reviewed:false` 4행 · `true` 1행엔 없음) · 별칭 줄 |
| `WP10-glossary-ja.png` | 괄호 그대로인 현지명(「ピコトーニング（ピコレーザー）」 · 그 밖 모양 → `reviewed:false`) 2행에만 꼬리표 |

- 방법: `:3800` · `:8800` 을 compose(`interpret-pwa-poc-front-1` · `-back-1`)가 쓰고 있어 포트를 열지 않고 운영 빌드(`.next`)를 헤드리스 Chrome request interception 으로 내줬다 · 서비스 워커 우회 · back 호출은 목업 · WS 는 페이지 안 가짜. compose 는 안 건드림.

## 계약 대조

| SPEC 0.4.0 | front |
|---|---|
| §4.7 응답 필드 · `term` 이름 그대로 · `count` = 그 언어 행 수 | 같음(목업으로 소비) |
| §7.6 별칭 줄 · 「검수 전」 꼬리표 · 칸 · 폭 · 부제 그대로 · 한국어 문구 하나 | 같음 |
| §9.2 클래스 대조 | 0 누락 |

## 이슈 · 코디가 확인할 것

1. **실 back(WP9 시드) 스크린샷 3장 pending** — 이 시점 워크트리에 `back/seed/` 가 아직 없고(WP9 진행 중) 3800 · 8800 은 compose 가 쓰고 있다. WP9 뒤 compose 재빌드(또는 포트가 비면)로 en · zh-Hant · ja 를 다시 찍으면 된다 — 같은 스크립트로 목업만 빼면 된다.
2. 시안 없음 — 꼬리표 · 별칭 줄은 SPEC §7.6 기본값. 시안이 생기면 따른다.
3. 별칭이 길면 칸 안에서 줄바꿈된다(`overflow-wrap:anywhere` 그대로) · 꼬리표는 줄바꿈 안 됨(`whitespace-nowrap`).
