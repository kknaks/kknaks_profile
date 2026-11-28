# 리뷰 리포트 — day-reservations-fix / code 고침 확인 (2026-11-27)

대상: 같은 워크트리 미커밋 변경 · `review-code-1-report.md` 의 F-1 · F-2 · W-1 ~ W-5 만. 기준 = `_RESUME.md` §2 맨 위 행(F-2 두 조각 · W-1 y 매핑 하나) · SPEC `7d99a62e`(Rule 15 ⓖ · ⓚ). read-only.

## 판정: PASS

남은 지적 없음. 참고 4개(아래)는 결정대로이거나 픽셀 차이라 고칠 것 아님.

## 지적별 확인

| 지적 | 고친 곳 | 확인 |
|---|---|---|
| **F-1** 앱 QR 이 opened 재사용 → 닫힘 | `services/displays.py:260,264,288-293` `reuse: bool = False` · 참은 웹 팝오버 라우트만 `routers/reservation_displays.py:127` · 앱 `routers/api/displays.py` 는 기본값(거짓) | 고침. 테스트 `test_reservation_display_popover.py:95` 앱 경로 = opened 있어도 새 pending · `:114` 웹 「링크 열기」는 다시 씀 |
| **F-2** 다섯 자리 덮임 → 겹침 | `policies/reservation_layout.py` `_Column` 에서 `covered` · `strict` 재시도 없앰 · `_place_run` = 빈 줄 나올 때까지(주석 「아직 아무도 없는 줄은 늘 비어 있다」 — 아래 줄은 시작 행 안만 차지하므로 참) · 첫 줄은 행 넘어 한 시간줄로 다음 행 자리 셈 유지 | 고침. 1차 재현(12:30 ~ 13:30 × 6 + 12:40 ~ 12:50, 오픈 12:00) 다시 실행 → 자리는 같으나(`lane 0~4 line 0` · `lane 0 line 1` · `lane 1 line 1`) 두 조각 그림 모형으로 **겹침 0**. 덧붙여 무작위 3000 판(1 ~ 14장 · 길이 15 ~ 150분 · 10분 간격 시작)을 조각 단위(행 · 줄 · 자리 · 분)로 겹침 셈 → **0**. 테스트 `test_reservation_layout.py:189` `test_다섯_자리가_모두_행을_넘어도_겹침_0` |
| F-2 그림 — 웹 | `day.js` `resSpan`(첫 줄 = 지나는 행마다 그 행 첫 줄 띠 한 조각 · 아래 줄 = 시작 행 그 줄 띠 · 행 끝 자름) · `resPlace`(첫 조각 = 요소 자신 · 나머지 = 안쪽 `.day-res-part` · 잘린 쪽 테두리 · 둥글기 0) · 카드 · 띠 · 미리보기(`:3259`) 다 이 식 · 카드 `overflow: hidden` 은 안쪽 칸으로 옮김(`app.css:3479` — 조각이 밖에 보임) | 서버 두 조각과 같은 그림 |
| F-2 그림 — 앱 | `reservation_table.dart` `ResvRows.pieces`(같은 규칙 · 붙은 조각은 하나로 합침) · 카드 조각마다 `ResvCardView(piece: k)`(글자는 0 조각만 · 키 `resv-card-<id>-<k>`) · 띠도 `pieces` | 서버 두 조각과 같은 그림(테두리 모양만 다름 — 참고 1) |
| **W-1** y 매핑 | 웹 `resAt(r, line, min) = r.top + line·band + (min − s)/(e − s)·band` 하나 — 카드 · 띠 · 회색 면(`resGrayPieces` = 그 행 모든 줄 띠) · 현재 시각 선(첫 줄 = 선 · 아래 줄 띠마다 `.day-res-part`) · [+] · 누르기(`resSlotAt` = 누른 줄 띠 안 분 · `line` 돌려줌 · 툴팁 · 자리 셈도 그 줄) · 앱 `inLine(r, line, min) = r.top + line·lineH + (min − s)/60·resHour` · `allLines`(회색 면) · `linesAt`(현재 시각 선) | **웹 = 앱 같은 식**(band = lineH = (e − s)/60 × 기본 높이 → 두 식이 같음) · 카드와도 같음 |
| **W-2** 웹 격자 | `day.js` `--day-res-row-lines` = 행마다 1px 선 그라데이션 · `app.css:3353-3357` 반복 없음 | 고침 — 행 경계에만 선(앱과 같음) |
| **W-3** 클립보드 | `day.js:6085-6106` 누를 때 `navigator.clipboard.write([new ClipboardItem({"text/plain": 응답 Promise})])` · 없으면 응답 뒤 `writeText` · 링크 없으면 Promise reject | 고침(Safari 사용자 동작 안에서 시작) |
| **W-4** 죽은 코드 | `presentation/qr.py` 없음 · `qr_svg` · `.day-res-dp__qr` grep 0 · 「접속 중」 허용 줄 없앰(남은 것은 화면에 **없음**을 확인하는 테스트 `test_reservation_detail_display_screen.py:177`) | 고침 |
| **W-5** 설명 글자 | `schemas/reservation_detail.py:139-141` 「열린(pending · opened)…」 | 고침 |

## 고침이 새로 깬 것 — 없음
- 누르기 · 우클릭 · 끌기 · 툴팁: 웹 조각은 카드 · 띠 · 회색 면 요소의 **자식**(`.day-res-part` · `pointer-events: inherit`)이라 `closest("[data-day-res-card]")` · `data-tip` · `.day-res-gray`/`.day-res-band` 빼기가 한 요소처럼 그대로 걸림. 앱 조각은 조각마다 같은 `onTap`(같은 상세) · 흐림 같음.
- 띠: 웹 · 앱 둘 다 카드와 같은 `resSpan`/`pieces` → 행 넘는 띠도 두 조각 · 배지는 첫 조각 왼쪽 위.
- 미리보기(등록 · 옮기기) 카드도 같은 조각 그림(`day.js:3259`).

## 참고(고칠 것 아님)
1. 조각 모양: 웹은 잘린 쪽 테두리 · 둥글기를 없애 「잘린 한 장」으로, 앱은 조각마다 둥근 상자 하나로 그림(`lines ≥ 2` 행만 · ⓗ 「픽셀은 화면마다」 안).
2. 결정대로: 줄 접힌 행에서 6번째 카드는 행 넘는 lane 0 카드의 두 조각 **사이**(시작 행 아래 줄 띠)에 보인다 — 겹치지는 않음.
3. 웹 「링크 열기」는 앱이 띄운 기기 없는 pending QR 도 다시 쓴다(D44 · 테스트 `:114`) → 직원이 열면 opened → 앱 QR 화면은 「고객 폰에서 열렸어요」로 닫힘. 요청이 실제로 열렸으니 맞는 동작.
4. `ClipboardItem` 은 있는데 Promise 값을 못 받는 브라우저면 여전히 조용히 실패(`.catch(() => {})`) — Chromium · Safari 는 받음. 운영 PC 가 그 밖이면 e2e 때 한 번 볼 것.

## 검증(각 1회)

| 명령 | 결과 |
|---|---|
| `./scripts/test.sh --pure -q` | **2455 passed** · 891 deselected · 0 failed |
| node 테스트(스크래치 복사본 `npm ci` · `npm run test`) | **136 / 136 pass** |
| CSS 재현(`build.mjs --check`) · `npm run lint` · `format:check` | 통과 · 통과 · 통과 |
| `flutter analyze` | No issues found |
| `flutter test` | **551 pass** · 81 skip · 1 fail = `board_messages_contract_test`(base 기존 `memo_too_long` — 1차에서 확인 · 이 diff 밖) |
| F-2 재현 + 무작위 3000 판(스크래치 순수 실행) | 조각 겹침 0 |
