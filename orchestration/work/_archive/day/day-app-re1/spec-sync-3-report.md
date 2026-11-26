# spec-sync-3 — review-doc-5 WARN W1 ~ W7 고침

- 워크트리 `day-app-re1-spec` · spec-sync-2 미커밋 변경 위에 이어서(커밋 · push 안 함). 코드 정본 = CENTURION_DAY `a76496c4`(`git show` 로만 읽음).
- 새 규칙 · 새 글자 없음. 리뷰 「고칠 방향」대로만 고쳤고, 근거 코드 줄은 다시 열어 확인했다.

## 처분표

| W | 처분 | 고친 자리(파일:줄) | 근거 코드 @`a76496c4` |
|---|---|---|---|
| W1 OQ-A90 반만 닫힘 | 고침 — 첫 번째 방향(근거 줄 달고 닫음) | SPEC-003 `:669` 본문 「OQ-A90 닫음」 + 근거 · `:1635` OQ-A90 행 「→ **닫음**(2026-11-26 spec-sync-3 · 구현대로)」(SPEC-007 OQ-D29 닫는 꼴) · `20-spec.md:104` 「OQ-A84 ~ A95(~~A90~~ … 닫음)」 | `PassportScanActivity.kt:277-278` · `ScanChannel.kt:125-126` = `ByteArrayOutputStream` · 두 파일에 `File(` · `cacheDir` · `createTempFile` · `FileOutputStream` 0 |
| W2 BW7 줄 번호 낡음 | 고침 | SPEC-007 `:597` `day.js:5473-5487` → `:5643-5653` | `static/day.js:5643-5653`(sessionStorage · replaceState) |
| W3 `canResend` 빠짐 | 고침 | SPEC-003 `:645` questionnaire 칸에 「`canResend`(웹만 — 앱은 안 씀)」 | `schemas/reservation_detail.py:45-47` |
| W4 baseBody null → "" | 고침 — 첫 번째 방향(SPEC-003 에 한 줄) → SPEC-002 `:1685` 「바꿀 것 없음」은 그대로 둬도 맞는 말이 됨 | SPEC-003 `:588` 「단 `base.body` 가 `null` 이면 `baseBody` = `""` — DAY-SPEC-002 OQ-119」 | `app/lib/state/chart_controller.dart:156` · `schemas/board.py:89` |
| W5 서버 쪽 열린 OQ 요약 줄 낡음 | 고침 — `20-spec.md:104` 와 같은 꼴 | SPEC-003 `:1624` 「OQ-D27 ~ D42(… D29 · D30 · D31 · D39 · D42 닫음 · D40 구현값) · ~~OQ-N25~~(닫음) · N26 · OQ-R40」 | — (문서 정합) |
| W6 국적 alpha-2 에 열린 확인 안 이음 | 고침 | SPEC-007 `:571` 「`[A-Z]{2}` — KOS 국적 꼴 확인 = DAY-SPEC-003 OQ-A9 · DAY-SPEC-000 OQ-02-1 열림」 | `services/passport_scan.py:80-87`(값 그대로 · 열린 확인만 이음) |
| W7 503 조건 넓음 | 고침 | SPEC-007 `:573` 「**사진이 있고** 저장소가 설정 안 됨이면 …」 + 「사진 없는 손 입력은 저장소를 보지 않아 꺼져 있어도 KOS 고객 수정을 함」 · 근거에 `:309` 추가 | `passport_scan.py:236-241`(`_storage`) · `:309` `target = _storage() if data is not None else None` |
| (같이) log | 행 추가 | `log.md:17` 2026-11-26 spec-sync-3 행(spec-change, open-resolve) | — |

`last_updated` 는 spec-sync-2 때 이미 2026-11-26 이라 그대로 뒀다. `30-work.md` 는 바꿀 것 없음(상태 `in_dev` 그대로).

## 검증

- `python3 scripts/lint-pipeline.py --strict` → exit 0 · 0 error · 263 warning · **`products/day` 줄 0**(warning 은 모두 다른 제품의 기존 것).
- 번호 참조: 이번에 쓴 ID(OQ-A90 · OQ-A9 · OQ-02-1 · OQ-119 · OQ-D27 ~ D42 · OQ-N25 · N26 · OQ-R40)는 모두 정의가 있다 — SPEC-003 `:1468` OQ-A9 · `:1635` OQ-A90 · SPEC-000 OQ-02-1(`:2401`) · SPEC-002 `:1685` OQ-119 · SPEC-005 `:530` OQ-N26. **끊김 0.**
- 누적 diff(spec-sync-2 + 3): `products/day` 11 파일 · +86 −73.

## 남은 것(열린 채 — review-doc-5 §5 그대로)

1. OQ-D40 — Redis 장애 때 속도 제한 · 거절 기록 간격을 끄는 정책을 유지할지 사용자 확인.
2. 국적 alpha-2 강제 — KOS 가 alpha-3 를 받는지(OQ-A9 · OQ-02-1).
3. OQ-A95 실물 확인 · OQ-A93 출시 전.
