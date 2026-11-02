# 작업 type 구분 없애기 — 2026-10-25 (로컬 E2E 중 · 사용자 지시)

결정(`_RESUME.md` §2 2026-10-25 첫 줄): **KOS 작업은 type(PROCEDURE · ETCETERA) 구분 없이 전부 같은 시술 줄이다.** 「방 배정」도 포함. 빼는 것은 KOS `CANCELED` 하나뿐. 10-23 「방 배정 줄만 뺀다」 · 기타 작업 읽기 전용은 뒤집혔다.

## backend (`procedure/back/`)
- `domain/rules.py`: `items` 에서 `is_room_task` 거르기 제거. `procedures()` · `pickable` · `canStart` · `canFinish` · `all_done` · `payment_required` · `canCall` 등 `kind == procedure` 로 거르는 곳을 **전부** grep 해서 type 무관으로. `kind` 필드는 스냅샷 모양 유지를 위해 남겨도 되지만 규칙에서는 쓰지 않는다.
- [귀가 대기] 취소(`service/actions.py` `cancel` = 시술 아닌 남은 작업): 이제 전부 완료여야 귀가 대기이므로 취소 대상 계산이 type 에 기대지 않게 정리(남은 작업 = 완료 아닌 작업 → 전부 완료면 빈 목록). 동작이 바뀌는 곳을 보고서에 적어라.
- KOS 쓰기(시작 · 종료 · 호출 · 방)가 ETCETERA 작업에도 같은 API 로 가는지 코드로 확인. type 으로 거르는 곳이 있으면 같이 없앤다.
- 가짜 보드 · 시험을 새 규칙에 맞게. `uv run ruff check . && uv run pytest -q` 전체 1회.

## frontend (`procedure/front/`)
- `isEtc` · `kind === 'etc'` 로 갈리는 곳 **전부** grep(`OrderCard.tsx` · `view.ts` · `Aside.tsx` …) → 기타 작업도 일반 시술 줄과 똑같이(체크 · 버튼 · 담당 글자 · 고객 탭 번호 원 · 호출 대상). 별도 「읽기 전용 줄」 · `etcStatus` 표시 제거.
- `npx tsc --noEmit && npm run lint && npm run build` 1회.

## 하지 않는 것
- 앱(`procedure/app/`)은 이번에 안 건드린다(코디가 사용자에게 따로 확인).
- 문서(SPEC)는 코디가 뒤에 맞춘다 — 기다리지 마라.
