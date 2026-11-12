# 리뷰 리포트 — prod-deploy-re1 / code 재리뷰 4 · 차트 담당자 키 (2026-11-11)

범위(코디 지정 · 전체 재리뷰 아님): review-code-3 W1 이 닫혔나 · 의사 호출 회귀 · 새 어긋남. W2(SPEC-002 개정)는 코디 몫이라 보지 않음.
근거: fe-1-report.md 「수정 2」 · review-code-3 W1 · SPEC-002 :320(의사차트 수락 뒤 고치면 바로 KOS).

## 판정: PASS

FAIL 0 · WARN 0 · 참고 2.

## 검증 (각 1회)

| 명령 | 결과 |
|---|---|
| `node --check backend/day/static/day.js` | ok |
| `uv run pytest -q -m "not infra" backend/tests/day/web backend/tests/architecture` | **113 passed** |
| `uv run ruff check backend` | All checks passed |
| day.js diff `+` 줄의 `<script` · `eval(` · `innerHTML` | 0건 |

## W1 — 닫힘 (PASS)

- `backend/day/static/day.js:904-916` — 담당자 목록(`[data-day-staff-list]`) 라디오에서 ←→ 를 `preventDefault` 하고 `moveInPop`(포커스만)으로 돌린다. ↑↓ 는 `:928-931` 이 원래대로 막는다 → 라디오 기본 동작(옆 줄 checked + change)이 생기지 않으므로 키 하나로 저장 · KOS 쓰기가 나지 않는다.
- Enter · Space(`:907-911`): 막고, 이미 고른 줄이면 저장 없이 닫기 · 아니면 `click()` → change → 기존 저장 경로(`:853-862`). 이미 고른 줄의 `click()` 은 change 가 없으니 저장이 생기지 않는 것도 맞다.
- 다시 누르기(`:760-761`): 줄(label)을 누를 때 라디오가 이미 checked 면 닫기. label 기본 동작은 막지 않지만 그 라디오는 이미 checked 라 change 가 없다 → 저장 0. 다른 줄을 누르면 이 분기를 지나쳐 label → 라디오 click → change → 저장(그대로). 두 번째 click(target = input)은 `instanceof HTMLInputElement` 로 건너뛴다 — 맞다.
- `moveInPop`(`:165-171`)은 예전 ↑↓ 처리와 같은 선택자 · 같은 계산을 한 곳에 모은 것뿐.

## 의사 호출 회귀 — 없음 (PASS)

- 새 키 분기 · 다시 누르기 분기는 모두 `[data-day-staff-list]` 안에서만 걸린다 — 의사 호출 목록(`_call_body` · `day-call__list`)엔 이 속성이 없다(`ui.html` 의 `data-day-staff-list` 는 `staff_picker` 한 곳).
- 의사 호출 창의 ↑↓ 는 `moveInPop` 으로 바뀌었지만 선택자 · 순환 계산이 이전 줄과 같다. ←→ · Enter · Space 는 예전처럼 브라우저 기본(라디오 고르기 — 보내기는 [호출] 버튼)이라 동작 그대로. 웹 시험(의사 호출 포함) 통과.

## 새 어긋남

없음. 참고만:

- 참고 1: Space 를 keydown 에서 막고 `click()` 을 직접 부른다. Chrome · Safari 는 keydown 을 막으면 라디오의 keyup 활성화도 일어나지 않아 한 번만 고른다. 혹시 두 번 click 이 와도 둘째는 이미 checked 라 change 가 없어 저장은 한 번. 실브라우저 e2e 에서 확인 권장(fe-1 pending 과 같음).
- 참고 2: 시험은 day.js 선택자 문자열 확인 수준이다(기존 방식). 실제 키 · 클릭 동작은 fe-1 의 headless 확인(ArrowRight `defaultPrevented=true` · 값 그대로 · 다시 누름 닫힘)과 e2e pending 에 기댄다.
