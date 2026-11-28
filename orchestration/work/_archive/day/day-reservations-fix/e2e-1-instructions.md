# [backend · e2e-1] 로컬 스택 + KOS DEMO 실물 — #300 · #301 · #302 완료 조건

같은 터미널 · 같은 맥락. **코디가 로컬 스택을 띄워 뒀다**: `http://127.0.0.1:11340`(`--migrate --scheduler --kos-demo` · DEMO 지점 연결 · migration 0032 · 이 워크트리 미커밋 코드). **스택 시작 · 멈춤 · 재시작 · 코드 수정 금지**(버그는 원인 file:line 만). 다른 워크트리 스택(11040 · 11240) 금지. 로컬 DB 는 SELECT 만(`deploy/local.env` · 스키마 `day_dev` · 포트 11342). 로그 `.run/*.log`.

사용자 허락(11-28): KOS 로그인 확인 · e2e 진행 · **데모 지점에 문진 제출 1회(D46 ②)** 포함. KOS 시스템 계정 로그인은 지금 비어 있다(코디 확인: 내부 legacy 읽기 200/400 실물 OK).

## 원칙
- KOS 는 내부 API 만 · DEMO 지점만 · 다른 사람이 쓰는 작업/고객은 건드리지 마라. 테스트 계정 `~/.config/day/kos-test-account.env`(값 출력 금지 · 그 밖 `~/.config/day/` 금지) · 끝나면 네 KOS 로그인 세션 해제(`revoke-active-sign-in`).
- 비밀 · 토큰 · 고객 PII 출력 금지(id 앞 8자).
- 웹 화면은 HTTP(로그인 세션 쿠키)로 조각 HTML 을 받아 확인 · 앱은 앱 JSON API 로 확인. 브라우저 눈 확인이 필요한 항목은 「코디 눈 확인」으로 남겨라.

## 시험 (각 결과 O/X · 수치)
1. **F6**: 오늘 방문 하나에 [문진 QR] 기기 줄 POST → SSE `display` 뒤 `GET /reservations/visits/{id}` 조각에 `qrUrl` 있음 · 동행 저장 · 신분확인 경로도 · 앱 상세 JSON `displays[].qrUrl` 같은 값 · 태블릿(기기) 쪽 표시 API 가 그 요청을 받음.
2. **팝오버**: `GET display-targets` = 요청 0 · 「링크 복사하기/열기」 POST 두 번 = 같은 링크(D44) · 기기 줄 = 앞 요청 취소 → 새 · 앱 경로 = 늘 새 요청(F-1).
3. **배치(Rule 15)**: 웹 조각 · 앱 JSON 의 `rows` · `cards` · `bands` 가 같은 값 · 60분 = 행 하나 · 겹치면 옆 자리 · (가능하면 DEMO 에 이미 있는 예약으로) 6장 이상 / 행 넘는 카드 경우 · 없으면 「데이터 없음」.
4. **KOS 문진 읽기**: 10초 회차 뒤 `day.emr.sync_questionnaires_hospital` 실행 로그 · 제출 있는 고객 = `source = read` 행 + `external_ref` · 다음 회차 중복 0 · 400 고객 = 행 없음 · 6개월 안 고객은 건너뜀(로그/호출 수).
5. **D46 ② 제출 id**: DAY 웹 문진 링크로 DEMO 고객 1명(오늘 방문 · 제출 없음인 사람)에 문진 1회 제출 → DAY 제출 행의 `external_ref` = KOS 제출 응답 id → 다음 회차 읽은 id 와 같음 · read 행 새로 안 생김. **제출 응답에서 id 가 어느 칸에 오는지 그대로 기록**.
6. **6개월**: `questionnaire.expired` — 실데이터 경계가 없으면 DB SELECT 로 판정 근거만(행 날짜 · 오늘 KST) · 웹 조각 「6개월 경과」 / 앱 JSON 같은 값.
7. **D45**: 팝오버 열림 중 SSE 다시 그리기 → 코드 경로 근거 + 「코디 눈 확인」.

## 리포트
`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/e2e-1-report.md` — 맨 위 표(시험 × O/X · 수치 · 비고) · 제출 id 위치 · 남긴 KOS 상태(제출한 고객 id 앞 8자) · 버그면 file:line · 코디 눈 확인 목록. 완료 보고 두 명령(subject 「backend 완료: e2e-1」 · 이번 dispatch 값 · 코디 `term_99b025fc-f3ef-403e-8162-509c41545e2e` — preamble 우선):

```bash
orca orchestration send --to term_99b025fc-f3ef-403e-8162-509c41545e2e --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: e2e-1" --body "<요약>"
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[worker_done] backend 완료 — e2e-1 <한 줄>. 상세는 인박스." --enter
```
