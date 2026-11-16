# fix-web fe-4 결과 보고 — review-code-3 W2 반영: 「펼치기」를 화면 높이로 (frontend)

## 상태: done (infra 테스트 pending — 앞과 같은 사유)

## 수행
| 파일 | 무엇 |
|---|---|
| `backend/day/templates/ui.html` `memo()` | 서버 줄 수 판정(`text.split('\n')|length > 5`) 삭제. 메모마다 「펼치기」/「접기」 버튼을 늘 두되 `hidden`(펼친 메모는 「접기」 · aria-expanded true) |
| `backend/day/static/day.js` | `fitMemos(root)` — `.day-memo` 마다 `is-open` 이거나 내용 칸 `scrollHeight > clientHeight + 1` 이면 버튼 보임, 아니면 숨김. `init(root)` 맨 앞에서 부름 → 처음 그릴 때(DOMContentLoaded) · `htmx:afterSwap` · `htmx:oobAfterSwap` 뒤. 창 크기 바뀔 때(resize)도 다시 잼 |

### 펼친 상태 복원과의 관계
- 다시 그릴 때 `restoreState`(afterSwap · oobAfterSwap 리스너)가 `init` 리스너보다 먼저 등록돼 먼저 돈다 → 펼침(`is-open`)이 복원된 뒤 `fitMemos` 가 잰다.
- 펼친 메모는 max-height 가 없어 넘침을 잴 수 없으므로 `is-open` 이면 「접기」를 그대로 보인다(펼쳤던 메모는 넘쳤던 메모). 「접기」를 누르면 버튼은 남는다(접힌 뒤에도 넘치므로 다음 fit 에서도 보임).
- 숨은 패널(`display:none`) 안 메모는 높이가 0 이라 버튼이 숨은 채 — 판 카드는 숨은 패널에 있지 않아 영향 없음. resize 때 다시 잰다.

## 검증
- `uv run pytest -q backend/tests/day/web backend/tests/architecture` → **123 passed** — 메모 3장 모두 버튼 1개 · `hidden` · 글자 「펼치기」, 펼친 견본 「접기」 hidden, 짧은 메모도 hidden 버튼 존재, ui.html 에 split 판정 없음, day.js 에 scrollHeight 판정 · `fitMemos(root)`
- `uv run pytest -q -m "not infra" backend/tests` → **933 passed, 319 deselected**
- `ruff check backend` OK · `node --check day.js` OK · `scripts/build-css.sh` 재빌드(CSS 변경 없음)
- 추가 줄 인라인 스크립트 · `style=` · `onclick` · `eval(` grep → 0
- pending: infra(`scripts/test.sh`) · 브라우저 눈 확인(실제 높이 재기는 브라우저에서만 — E2E 에서 6줄 메모 · 긴 한 줄 메모 「펼치기」 확인 권장)
