# delivery-1 결과 보고 — R4-1 · SPEC PR · WP 나누기 · Delivery Issue 발행

## 상태: done (사람 gate 대기 — 승인 receipt 미적용)

| 항목 | 값 |
|---|---|
| R4-1 | spec-006:613 케이스 「시작이 달라 높이가 겹침」 = 「~~→ 행 사이 겹침 없음 — 긴 카드도 시작 행 한 줄(R70 · W12-2)~~ → 개정 ⑯ F2 · 보충 2: 겹치면 옆 자리 · 자기 시작 위치부터 · 행을 넘으면 Rule 15 ⓖ」(그 밖 SPEC 문장 안 바꿈) |
| SPEC PR | **mediness#971**(draft · → main · 미머지) https://github.com/MediSolveAIDev/mediness/pull/971 |
| SPEC 커밋 | `ad317cf4f2e3c6124331db90c09c178697f2131e`(SPEC 고침 1 ~ 4 + R4-1) · `990858664fd2672d73b0704bbf1d274bfde28f8d`(30-work Spec Coverage · log — 같은 PR) |
| request baseline | `b9ac374ebbe60e37c35e0b1c6a48da633ce49848`(origin/main) — 아래 「막힌 것」 · 코디 답 a) |
| Delivery Issue | **CENTURION_DAY#300**(WP-1 BE) · **#301**(WP-2 웹) · **#302**(WP-3 앱) |
| CLI 결과 | 셋 다 `status: created` · `spec_baseline_state: ready` · `execution_state: ready` · `next_action = review-delivery-plan`(human_gate) · task_projection blocked(`delivery-plan-review-required`) |
| digest | #300 `sha256:83f571a7…35fc` · #301 `sha256:f28b7d87…297b` · #302 `sha256:2bf1469f…7ad1`(전체 = delivery/*-apply-v1.json) |
| lint | `--strict` exit 0 · 0 error · products/day 줄 0(두 커밋 다) |

json: `delivery/wp{1-be,2-web,3-app}-{request,plan,apply}-v1.json` · `.err` · 생성기 `delivery/gen.py`.

## 막힌 것 · 처리

1. **baseline**: 지시대로 baseline = SPEC 커밋 `ad317cf4` 로 `--plan` → exit 2 `{"error": "requested SPEC baseline is not the fetched latest origin/main revision", "status": "conflict"}`(CLI 규칙: `spec_baseline_revision` = fetch 한 origin/main). 우회하지 않고 코디에 ask → 답 a): baseline = origin/main `b9ac374e` + 계약 원천 줄(PR #971 `ad317cf4` · main 판은 개정 전이라 근거 아님 · 머지 뒤 v2 재결속) — target_delta · review_surface 첫 줄. (앞 day-room-board #289 ~ 291 과 같은 방식.)
2. **pending 아님**: CLI 가 `spec_baseline_state` 를 **ready** 로 정함(main 판 target SPEC 이 stable 이라). request 에 pending 을 지정하는 칸이 없어 그대로 둠 — 계약 원천 줄로 「main 판 근거 아님 · 머지 뒤 v2」를 밝힘. 다르게 원하면 코디 판단.
3. **승인 receipt 적용 안 함**(L2 · 사용자 몫) · Task projection 안 함(승인 전 blocked).
4. 30-work.md 의 「Delivery Issues (derived)」 표(`mediness:delivery-dashboard` 마커 블록)는 도구가 만드는 블록이라 손대지 않음 — Spec Coverage 행만.

## WP 표 (병렬 — 의존은 실제 순서만)

| WP | Issue | 범위 | 의존 |
|---|---|---|---|
| WP-1 BE | #300 | F6 origin 필수 · 4곳(`routers/reservation_detail.py:179` · `:327` · `:407` · `routers/api/reservations.py:104`) + GET 라우트 실제 service 시험 · Rule 15 배치 값(`rows` · `lane` · `line` · `start_min` · `end_min` · 웹 · 앱 같은 함수) · 열 그룹 이름 · 간격 · `open_min = 0` 그룹 확인 · KOS 문진 읽기 별도 태스크(내부 legacy · mapper · `external_ref` · 기간 안 건너뜀 · 400 = 없음) · 제출 id 남기기 · 문진 6개월 `questionnaire.expired` · 팝오버 요청 흐름(기기 목록 · 고르면 그때 생성 · D44) | 없음(먼저 머지) |
| WP-2 웹 | #301 | F1 오른쪽 70 · 점선 [+] · 툴팁 · 등록 창 · Rule 15 그리기(1시간 행 140 · 줄 접기 · 행 넘는 카드) · [문진 QR] 한 단계 팝오버 · [여권 스캔] 기기 팝오버 · F5 모달 기기 카드 · 이 화면 QR 없앰 · 「6개월 경과」 · D45 | 계약 고정 → 병렬 구현 · e2e 는 BE 머지 뒤 |
| WP-3 앱 | #302 | 예약현황 표 Rule 15(1시간 행 = 지금 30분 칸 × 2 · 줄 접기 · 행 넘는 카드 · `reservation_table.dart` 고정 66 바꿈) · 상세 「6개월 경과」 | 계약 고정 → 병렬 · e2e 는 BE 머지 뒤 |

각 Issue 에: 범위(target_delta) · BE ↔ 웹/앱 계약(SPEC 절 인용) · 완료 조건(acceptance — 로컬 KOS 데모 지점 실물 e2e 1회 · BE A7 = D46 ② 제출 id = 읽은 id · 웹 A6 = D45 팝오버 안 닫힘) · non_goals · execution(code surface · phase · verification · predeploy · rollback).

## BE ↔ 웹/앱 계약 (세 Issue 공통 · 이름 고정)

① 배치 값 = DAY-SPEC-006 Functional Rule 15 ⓐ ~ ⓙ: `rows[] {start_min, end_min, lines}` · `cards[] {lane 0 ~ 4, line, start_min, end_min}`(앱 JSON camelCase `startMin` · `endMin`) · 놓는 순서 = 시작 시각 → 같은 시작이면 R73 · 5 자리 넘치면 그 행 아래 줄 · 행 넘는 카드 ⓖ · 열 폭 상한 5 + 오른쪽 70 · 픽셀만 화면마다(웹 140 · 앱 30분 칸 × 2) · 화면은 다시 계산 안 함.
② 열에 [+] 툴팁용 그룹 이름 · `interval_minutes`(칸 이름 = BE 가 정해 Issue 에 적음).
③ 상세 `questionnaire.expired: bool`(DAY-SPEC-007 앱 JSON 짝 · 고객 단위 · env 기본 6개월 · D49) · 글자 「6개월 경과」 · `actions.questionnaireQr` 같은 조건.
④ 팝오버: `GET /reservations/visits/{id}/display-targets?kind=` · `POST /reservations/visits/{id}/display-requests`(링크 = device 없는 요청 · 열린 링크 다시 씀 D44 · 기기 줄 = 앞 요청 취소 → 새 요청 · 고르면 그때 생성 · DAY-SPEC-007 규칙 2 · 7).
⑤ F6: 상세 모든 경로 origin → `displays[].qrUrl` 같음(DAY-SPEC-007 규칙 9).

## migration

없음(DAY-SPEC-000 개정 ④ — 새 칸 · 테이블 없음). 고객 판정 인덱스(`customer_id`, `submitted_at`)가 필요하면 alembic head `20261126_0031` 다음 `0032` 로 — BE Issue A6 · rollback 에 적음.

## 되돌리기

BE = Code PR revert(인덱스 넣었으면 downgrade · `source = read` 행은 남아도 무해) · 웹 = 템플릿 · 정적 파일 revert · 앱 = 앱 코드 revert(서버 값은 새 칸 추가라 하위 호환).

## 남은 사람 gate

- L2 결과 계약 승인 3건(#300 · #301 · #302 — 사용자 · receipt 는 코디/사용자가 적용)
- SPEC PR #971 머지(구현 끝난 뒤) → 같은 key · contract_version 2 · 새 main SHA 로 재결속
- 열린 문구 OQ-D43 · D48(사용자 글자)
