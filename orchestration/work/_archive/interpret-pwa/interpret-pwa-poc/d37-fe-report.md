# D-37 — frontend 결과 보고 (밖으로는 통역에 필요한 최소 정보만)

## 상태: done

워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc`(main 10b4c38 위 · 커밋 없음 · 스테이징 없음). 범위 `front/**` 만(`design/` 의 변경은 designer 것 · 안 건드림).

## 수행

| # | 지시 | 한 일 |
|---|---|---|
| ① | 용어집 메뉴 · 창 · 호출 삭제 | `components/interpret/GlossaryModal.tsx` · `lib/glossary.ts` · `tests/glossary.test.ts` **삭제** · `lib/api.ts` 의 `GlossaryRow` · `GlossaryResult` · `glossary()` 삭제 · `HeaderMenu` = 로그아웃 하나(용어집 항목 · 구분선 · `onGlossary` 삭제) · `InterpretScreen` 의 용어집 상태 · 창 삭제 · `components/icons.tsx` 의 `BookIcon` 삭제 · `app/styles/medikit-patches.css` 의 `[BaseModal-1]`(용어집 창 전용) 삭제 |
| ② | `/api/auth/me` 는 ok(+ expiresAt) 만 | `Me` = `{ok, expiresAt?}`(아이디 필드 없음). 응답 값을 쓰는 곳은 원래 없다 — 401 이면 로그인으로(토큰 확인용) 그대로 |
| ③ | 오류 문구는 back 일반 문구 그대로 · front 에 설정 · env 이름 문구 없음 | `CONFIG_ERROR`(「back 주소(NEXT_PUBLIC_API_BASE_URL)가 비어 있어요 — front/.env.local …」) → 「서버에 연결하지 못했어요」. 서버 `message` 는 그대로 보여 준다(로그인 401 · 429 · WS `error`). 그 밖 front 문구(마이크 권한 안내 · 「통역 서버와 연결이 끊겼어요.」)에는 설정 · env 이름 없음 |
| ④ | 빌드 산출물 grep | 아래 |
| ⑤ | 시험 갱신 | `tests/glossary.test.ts` 삭제 · `tests/minimal-exposure.test.ts`(새) — `lib/api` 에 `glossary` 없음 · 설정 오류 문구가 일반 문구이고 `NEXT_PUBLIC` · `.env` · `SONIOX` · `INTERPRET_` · `localhost` 가 없음 |

- 주석에 남아 있던 「용어집」 3곳(api · HeaderMenu · langs)도 지웠다 — 서버 쪽 소스맵(`.next/server/**/*.js.map`)에 주석이 실리기 때문.

## 검증

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과 |
| `npm run build`(`.next` 지우고 새로) | 통과 |
| `npx vitest run` | 9 파일 · **36 통과**(용어집 2 빠지고 새 2) |
| 클래스 대조 | 177 · 없는 것 0(용어집 창 클래스가 빠져 209 → 177) |

빌드 산출물 grep(`.next` 전체 · `cache` 제외):

| 찾은 말 | `.next/static`(브라우저로 나감) | `.next` 전체 |
|---|---|---|
| `美國音波` · `Thermage` · `써마지` · `koAliases` | 0 | 0 |
| `glossary` · `용어집` | 0 | 0(Next 내장 MIME 표의 `…glossary+xml` · medikit 소스맵 자체 문구는 우리 것이 아니라 뺌) |
| `SONIOX` · `INTERPRET_` | 0 | 0 |
| `NEXT_PUBLIC` | 0 | Next 라이브러리 자체(`next/dist/lib/static-env.js` 등)만 |

## 이슈 · 코디가 확인할 것

1. back 의 `/api/auth/me` 응답이 `{ok}` 만 와도 front 는 같은 동작(401 만 봄) — back D-37 과 순서 상관없음.
2. 화면 문구에서 「용어집」 이 사라졌다 — SPEC §7.6 · 시안 Menu · Glossary 갱신은 코디 → planner · designer(워크트리의 `design/` 변경이 그 작업으로 보임).
