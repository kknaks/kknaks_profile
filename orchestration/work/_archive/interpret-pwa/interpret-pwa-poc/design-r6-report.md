# interpret-pwa 시안 r6 결과 보고 — 시작 오버레이에서 언어 고르기 (D-34)

## 상태: done

## Claude Design 캔버스
- https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd · 버전 `1793065090-39a3`(전 `1793003735-78bb`) · 게시 충돌 없음
- 워크트리는 main `9befd18` 기준. 게시 전 로컬 `State-1-Start`(5588B)가 캔버스와 같은 것을 확인했다.

## 바꾼 화면: `State-1-Start.dc.html` 1개

| 항목 | 전 | 후 |
|---|---|---|
| 오버레이 | 화면 전체가 단추 하나 · 위(Tap to start · 뒤집힘)와 아래(탭해서 통역 시작) 두 언어 | 상담사 방향 하나(바로 · 회전 없음) · `bg-ms-overlay` · 헤더까지 덮음(전과 같음) · `role="dialog"` |
| 문구 | 「탭해서 통역 시작」 | 제목 「통역할 언어를 고르세요」(`title-md-600` 흰색) · 부제 「누르면 그 언어로 바로 통역을 시작해요」 |
| 시작 동작 | 오버레이 탭 | **언어 단추 탭 = 그 언어로 시작**(AudioContext 깨우기 · 마이크 · WS · start) |
| 단추 | — | 7개 · 2열 grid(gap 12px) · 높이 72px · `bg-ms-white text-ms-gray-800 text-typo-title-sm-600` · 모서리 12px · 각 단추에 `lang` 속성. 7번째 廣東話는 두 칸(가운데) |
| 마지막에 쓴 언어 | — | English 예: `bg-primary-100` + 2px `border-primary` + 아래 「최근 사용」(`caption-md-600 text-primary`). 표시만 하고 자동 선택 · 자동 시작 없음 |

- 단추 순서 = front `lib/langs.ts`의 `LANGS`(en · ja · zh · zh-Hant · th · vi · yue) = 드롭다운 · 2-3 언어 목록과 같다. 코디 메시지의 나열(廣東話가 ไทย 앞)과 순서가 다르다. 목록과 한 줄로 맞추려고 LANGS를 따랐다. 바꾸려면 말해 달라.
- 오버레이 아래 통역 화면(원 64px · 원 줄 140px)은 그대로다.
- 백그라운드 복귀(시작 전으로 돌아감)도 같은 화면이다(별도 아트보드 없음).

## 검증
- 캔버스 `State-1-Start.dc.html` 6365B가 로컬과 같다. 나머지 파일은 전 버전 그대로. `git status` 기준 `design/`에서 바뀐 것은 이 파일과 README뿐.
- 쓴 클래스(`border-ms-white` · `border-primary` · `bg-primary-100` · `text-typo-title-sm-600` 등)는 모두 medikit 번들에 있다. 새 hex는 없다.
- 커밋 안 함.

## 코디 · frontend가 볼 것
- SPEC §7.3 #1(시작 전) 「누르면」 칸을 「언어 단추 탭 = 그 언어로 시작」으로, 외국어 안내 칸(Tap to start)은 없앰으로 고쳐야 한다. 오버레이는 상담사 방향 하나다.
- 외국어 영역 안의 드롭다운은 통역 중에 언어를 바꾸는 용도로 남는다(바꾸지 않음).
