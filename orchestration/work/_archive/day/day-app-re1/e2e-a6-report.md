# e2e A6 — 로컬 BE(`ab8f6553`) + KOS 데모 지점 실물 호출(코디 · 2026-11-26)

스택: 코드 워크트리 `./start.sh --kos-demo --scheduler` · **`local migrate --kos-demo` 로 0029 적용**(start 는 migrate 안 함 — 처음 상세 500 `UndefinedColumnError questionnaire_history.crm_status` 의 원인) · seed-demo · 앱 로그인 `client=app`(테스트 계정 = 직무 간호 · coordinator 아님).

| # | 호출 | 결과 |
|---|---|---|
| 1 | GET /api/reservations | 200 · 오늘 카드 5 · filter.counts 단계별 |
| 2 | GET /api/reservations/visits/{v} ×5 | 200 · 상세 17키 · 여권번호 없음 · actions 단계대로(예약 = QR · 보내기 true / 상담 대기 = 전부 false / 취소 = false) |
| 3 | GET …/passport(상담 대기 외국인) | 409 `visit_stage_changed`(계약대로) |
| 4 | GET /api/display-targets | 200 `targets: []` — 코디 직무 계정으로 로그인한 기기 없음 |
| 5 | POST /api/visits/{홍길삼}/display-requests `{kind: questionnaire}`(이 기기) | 200 · pending · qrUrl `/q#…` · 10분 |
| 6 | GET /api/public/questionnaire(토큰 헤더) | 200 · **KOS 공개 양식 4쪽 · 약관 1 실물** · prefill 6칸 · `no-store` · `no-referrer` · /q 페이지 200 no-store |
| 7 | POST /api/public/questionnaire(답 15 · 약관 동의) | 200 `{ok}` → DB `crm_status = sent` · `source = web_submit` · 상세 `questionnaire.sendStatus = sent` · `health` 15줄 · 요청 `done` |
| 8 | 같은 토큰 GET 다시 | 409 `q_submitted` · 틀린 토큰 = 404 `q_not_found` · 모르는 본문 = 400 `invalid_request` field |

| 9 | POST /reservations(Bearer · form · 새 고객 홍길사 · TW · 중화권 11:00) | 200 `day:res-queued` → 오늘 예약 · `actions.passportScan = true`(첫 시도 400 = date 를 `2026.11.26` 로 보냄 — 서버는 `YYYY-MM-DD`) |
| 10 | GET …/passport(예약 단계 외국인) | 200 · 7칸(여권 칸 null · 국적 · 생년월일 · 성별은 DAY 사본) |
| 11 | POST /api/visits/{v}/passport-scan(manual · 7칸 · JPEG) | 200 · `identity confirmed app_manual` · **`kos.customer = ok`(KOS 고객 여권 칸 실물 수정)** · `kos.photo = skipped` · DAY 사진 저장(`kosSynced false`) → 상세 `identity.confirmed true` · passport 7칸 = 보낸 값 |

**`kos.photo = skipped`** = KOS 데모 지점에 이미지 분류 「여권」이 없음(be-2 §4-3 예고대로 · 이름으로 찾음). 분류를 KOS 에 만들면 [사진 다시 올리기](`/api/id-photos/{id}/kos-retry`)로 확인.

남은 것: ~~**여권 스캔 저장(KOS 고객 수정 · 사진 「여권」 분류)** ~~(위 9 ~ 11) · KOS 사진 「여권」 분류 · **태블릿 보내기 / 받기** — 코디 직무 계정 로그인 기기 필요.
데모 지점에 남은 것: **새 고객 · 예약 홍길사(TW · 1992.03.15 · 오늘 11:00 중화권 · 메모 없음) · 여권 칸 HONG / GILSA / E2E000001 / 2030-12-31** · 홍길삼 KOS 문진 제출본 1(답 = 각 문항 첫 보기 · 입력칸 「e2e」) · 생년월일 KOS 에 없던 값 `19900101` 로 들어감(KOS 제출 부작용).
