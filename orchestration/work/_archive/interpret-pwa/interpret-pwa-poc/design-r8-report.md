# interpret-pwa 시안 r8 결과 보고 — 용어집 화면 · 메뉴 항목 삭제 (D-37)

## 상태: done

## Claude Design 캔버스
- https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd · 버전 `1793073038-3dcb`(전 `1793068035-f0d6`) · 게시 충돌 없음
- 워크트리 main `10b4c38` 기준. 게시 전 로컬 `Menu`(6476B) · `canvas.json`(5413B)이 캔버스와 같은 것을 확인했다.
- 아트보드 22 → 21개.

## 바꾼 것

| 대상 | 처리 |
|---|---|
| `Menu.dc.html`(5-1) | 팝오버에서 「용어집」 항목과 그 아래 구분선을 지움 → 「로그아웃」(빨간 글자) 하나만 남음. 나머지(배경 통역 화면 · 헤더)는 그대로 |
| `Glossary.dc.html`(5-2) | **캔버스에서 지움**(`files` null로 삭제 · `canvas.json`의 `boards` · `order`에서 뺌) · 로컬 `design/project/`에서도 지움 |
| `canvas.json` | 줄 제목 「5 · 햄버거 메뉴 · 용어집」을 「5 · 햄버거 메뉴」로 · 폭 390 |
| `design/README.md` | 화면 목록에서 5-2를 빼고 5-1 설명을 고침 · r8 절 추가 |

## 검증
- 캔버스 `project/` 28개 파일(.dc.html 21 · canvas.json · CSS/폰트 6)과 로컬 28개가 같다. `Menu` 5712B · `canvas.json` 5240B가 캔버스와 로컬에서 같다. 캔버스에 `Glossary.dc.html`이 없다.
- 커밋 안 함.

## 코디가 볼 것
- SPEC §7.6(햄버거 · 용어집 패널)과 §4.6(용어집 메뉴 API)의 화면 쪽 기술을 D-37에 맞춰 정리해야 한다.
