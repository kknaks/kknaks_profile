# interpret-pwa 시안 r2 결과 보고 — 통키(Tongky) 반영 (D-21)

## 상태: done

## Claude Design 캔버스
- 이름: 「Interpret PWA」(그대로) · 설명: 「통키(Tongky) — 상담사와 외국인 환자가 기기 하나로 쓰는 실시간 통역 PWA 화면 시안 (medikit + Ceramique 테마)」
- URL: https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd · 버전 `1792999779-5fe7`(r1 `1792999606-635d`)
- 충돌 없이 반영됐다(r1 이후 캔버스를 손으로 고친 곳 없음, 게시가 거절되지 않음).

## 바꾼 화면 (17개 전부 · 그 밖은 그대로)

| 화면 | 바꾼 것 |
|---|---|
| `Main.dc.html` · `Login-Error.dc.html` · `Login-Locked.dc.html` | 제목 「통역」을 「통키」로(부제 · 나머지 그대로) |
| `Interpret-Flipped` · `Interpret-Upright` · `State-1`~`State-8`(9개 · #4는 a·b) · `Menu` · `Glossary` | 헤더 햄버거 옆에 워드마크 「Tongky」(`text-typo-title-md-600 text-primary` · 20px 굵게라 큰 글자 대비 기준을 넘음) |
| `Captions.dc.html` | 헤더 워드마크 + `final:false` 줄 `text-ms-gray-500`을 `text-ms-gray-600`으로 |

- `canvas.json`(배치 · 제목)은 바꾸지 않았다.
- State-1(시작 전)은 헤더가 오버레이 아래에 있어 워드마크가 어둡게 비친다(오버레이는 그대로).

## 검증
- 캔버스 `project/` 파일 23개와 로컬 `design/project/` 23개의 바이트 수가 모두 같다.
- 새로 쓴 클래스 `text-typo-title-md-600`이 medikit 번들에 있다. 다른 새 색이나 hex는 없다.
- `design/README.md` 갱신(앱 이름 · r2 버전 · 헤더/자막 규칙).

## 코디가 확인할 것
- SPEC §7.5의 `final:false` 색(`text-ms-gray-500`)을 `text-ms-gray-600`으로 고쳐야 한다. §7.1 제목 「통역」과 §7.2 헤더(워드마크)도 D-21에 맞춰 고쳐야 한다.
