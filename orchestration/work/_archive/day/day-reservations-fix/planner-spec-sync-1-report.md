# planner-spec-sync-1 결과 보고 — 코드 · e2e 에서 정한 것을 SPEC 에 (PR mediness#971)

## 상태: done

커밋 **`df451e4e0b3b55b4b89f7e1b924827878883af28`** → push · PR #971(draft · 머지 안 함 — 코디). 근거 = `_RESUME.md` §2 2026-11-28 행 · 코드 CENTURION_DAY PR #303 `d1ce8ea8`(file:line 은 이 커밋에서 확인). 바꾼 파일 = spec-006 · spec-007 · spec-000 · log.md.

## 고친 줄

| # | 자리 | 내용 |
|---|---|---|
| 1 W-a | spec-006 새 머리 「2026-11-28 spec-sync」 ① · U-10 호버 · 툴팁 시작 · 누름 / spec-007 새 머리 ① · `:109` 표 빈 칸 누르기 | [+] 칸 · 빈 칸 누르기 시각 단위 = **그 열 그룹 간격**(60분 그룹 = 정각만 · 간격 없는 열 = 30분 · 등록 창 시간 늘 골라짐) · **끌어 놓기 단위는 30분 그대로**(옮기기 줄 `spec-007:366` 은 안 바꿈) · 근거 `day.js:2457` · `:3212-3214` · `:3404` |
| 2 D44 시한 | spec-007 머리 ② · 규칙 2 「링크 다시 씀」 괄호 · OQ-D44 닫힘 줄 | 다시 쓰기 = 기기 없는 열린(pending · opened) 문진 요청 중 **여는 시한(`expires_at`) 안**만(`services/displays.py:339-355`) · **웹 팝오버만** — 앱 JSON 경로는 늘 새 요청(F-1 · `routers/api/displays.py:101` · `routers/reservation_displays.py:127` · `services/displays.py:260` · `:288-293`) |
| 3 OQ-D43 | spec-007 머리 ③ · 규칙 7 고침 8 「고른 뒤」 줄 · OQ 표 | 옛 「지금 글자 그대로 = OQ-D43」 취소선 → pending 줄 = 「남은 시간 mm:ss」만 · 카메라 글자 · [QR 닫기] 없앰 · 새 글자 없음(`reservations_display.html:66-67`) · OQ-D43 행 취소선 · 닫음(사용자 2026-11-28) · 복사 알림 = 없음 그대로 |
| 4 crm_error | spec-007 머리 ④ · 고객 문진 웹 표 새 줄 「실패 기록」(「제출 id 남기기」 위) | `crm_error` · 경고 로그 = 예외 이름 · HTTP 상태 · KOS 오류 이름(className 꼬리 · 값 · 개인정보 없음) — `services/questionnaire_kos.py:61-66` `crm_error_of` · `:113` |
| 6-a open_min 없음 | spec-006 머리 ② · Rule 15 ⓐ | 켜진 시간표 운영 시작이 하나도 없으면 행 = 08:00 기준(`policies/reservations.py:54` `DEFAULT_OPEN_MIN` · `:344` · be-1 이슈 4 — SPEC 에 정의 없던 것) |
| 6-b migration | spec-000 개정 ④ 「인덱스 = 구현」 뒤 · spec-007 머리 ⑥ | 구현이 인덱스 migration **0032** 를 더함(`questionnaire_history(customer_id, submitted_at) WHERE deleted_at IS NULL` · 새 칸 · 표 없음 · `backend/migrations/versions/20261127_0032_questionnaire_customer.py`) — 고침 8 머리 「migration 없음」을 바꿈 |
| 7 log | log.md 맨 위 한 줄 | spec-change, open-resolve · SPEC-006 · 007 · 000 |

## 남긴 OQ (열린 채 · spec-007 고침 8 OQ 표 · OQ-D49 아래)

| OQ | 무엇 | 지금 | 근거 |
|---|---|---|---|
| OQ-D50 | KOS 제출 500 인데 KOS 저장 → [다시 보내기] 이중 제출 | 다음 작업(사용자 「ⓑ · ⓒ = 다음 버그 고침 때」) · 후보 = 실패 직후 내부 legacy 읽기 1회 확인 | `e2e-2-report.md` ⓑ |
| OQ-D51 | 고객 웹 휴대폰 국가번호 빈 값(500 유력 원인 · 확정 아님) | 다음 작업 · 후보 = 번호 있으면 국가번호 필수 | `e2e-2-report.md` ⓒ |
| OQ-D52 | 「6개월 경과」 고객 건강정보에 옛 답 보임 | OQ-D49 「건강정보 = 보임」 그대로(다시 열지 않음) · 감출지 = 다음 작업 사용자 | `qa-2-report.md` §관찰 |
| OQ-D53 | D45 · 기기 줄 · 태블릿 = dev 실기기 확인 대기 | 코드 · 화면 테스트대로 · dev 배포 뒤 확인 | `qa-1-report.md` 7 · `qa-2-report.md` · `review-code-2-report.md` |

## 찾았지만 SPEC 에 안 넣은 것(SPEC 이 말하지 않는 구현 세부 · 계약 차이 아님)

- be-1 이슈 5 — KOS 문진 읽기 회차에 고객 수 상한 없음(잠금 TTL 안 못 끝나면 회차 되돌림 · 다음 회차 다시) — SPEC 은 상한을 정하지 않음 · 구현 세부.
- review-code-1 W-3 클립보드(Safari) · W-2 웹 격자 · W-4 죽은 코드 · W-5 API 설명 — 코드에서 고침(review-code-2) · SPEC 문장과 어긋남 없음.
- review-code-1 참고 4 「태블릿에 띄운 채 링크 복사하기 → 태블릿 요청 닫힘」 — SPEC 규칙 2 그대로(기기 없는 열린 요청이 없으면 새로 만들며 같은 종류 열린 요청을 닫음).

## lint

`python3 scripts/lint-pipeline.py --strict` → exit 0 · 0 error · products/day 줄 0.
