# 리뷰 리포트 — 화면 문구 근거 · SPEC-001 「화면 글자」 · SPEC-002 개정 ⑪ (2026-11-08)

대상: mediness diff(미커밋) — `spec-001-login-session.md` 「화면 글자」 표 · `spec-002-procedure-board.md` 개정 ⑪ 「오류 · 실패 토스트 글자」 표 · 규칙 22 · `log.md`.
기준: 원천 `screen/procedure-board-decisions.md` L93-95 「결정 — 근거 없던 화면 문구」 · 코드 `CENTURION_DAY/day-data-architecture/backend/day/routers/board.py` `MESSAGES`(L92-) · `KOS_FAILED_MESSAGE`(L110).
lint `--strict` → 0 error.

## 판정: PASS

### SPEC-002 토스트 표 ↔ 코드 (글자 대조)

코드의 `MESSAGES` 와 `KOS_FAILED_MESSAGE` 를 파이썬으로 읽고, SPEC 표 「코드 | 토스트 글자」를 줄 단위로 맞춰 봤다.
- **`MESSAGES` 16개 ↔ SPEC 16줄 — 다른 글자 0 · 한쪽에만 있는 코드 0**: `invalid_request` · `not_found` · `visit_home` · `anesthesia_running` · `anesthesia_not_running` · `task_not_pickable` · `doctor_not_listed` · `call_closed` · `nothing_to_accept` · `task_not_waiting` · `call_not_accepted` · `no_doctor` · `task_not_started` · `task_not_doing` · `task_not_done` · `tasks_not_done`.
- **`KOS_FAILED_MESSAGE`** 「KOS 반영 실패 — 데스크에서 KOS 를 확인하세요」 ↔ SPEC `kos_failed` 줄 — 같다(줄표 `—` 포함).

### SPEC-001 화면 글자 ↔ 원천 · 화면

| 글자 | 원천 L95 | SPEC-001 자리 | 템플릿 |
|---|---|---|---|
| 병원 선택 | 병원 고르기 제목 | 병원 고르기 카드 제목 | `partials/login_card.html` 에 있음 |
| 처음으로 | 로그인으로 돌아가기 | 병원 고르기 → 로그인 링크 | 같음 |
| MediSolve AI | 로그인 카드 | 로그인 카드 위 | 같음 |
| DAY | 로그인 카드 | 로그인 카드 제목 | 같음 |

### 새 문구

- 원천이 남긴 네 가지(로그인 글자 4 · 오류 토스트 16 · KOS 실패 토스트 1) 밖의 새 글자는 없다.
- 「이 밖의 글자는 SPEC · 시안에 있는 것만」 줄은 원천 문장 그대로다.
- 401 · 403 은 SPEC-001 「웹 화면」 대응표를 가리킨다. 이미 정해진 글자다.
- 규칙 22 의 「문구는 디자인」은 이 표 참조로 바뀌었다.
