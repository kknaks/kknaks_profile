# reservation-spec 결과 보고 — 예약 현황 BASE-009 · DEC-006 · SPEC-005 · WORK-007 (+ workflow-v2 4곳)

## 상태: done

## 수행 내용

새 문서(`para/projects/summer-star/cc-prototype/`):
- `00-baseline/baseline-009-reservation-board.md` — 원천(사용자 대화 10-26 · workflow-v3 · 리포트 15 · HAR 19 이름만) · 이해한 것(AS-IS · KOS 확인 · 방향). 새 결정 없음
- `10-decision/decision-006-reservation-board.md` — **D-01 ~ D-43** · 근거 칸(사용자 지시 / 코디 기본값 / 조사 결과 + `_RESUME 10-26 #행`) · `up: []` + 근거 개념 「없음」 사유 · 부록 A(`_RESUME` 10-26 줄 31 + §1 메모 2 → D 대조) · 부록 B(DEC-005 잇는 곳 — D-10 범위 나눔 · D-09 · D-12 · D-13 · D-14 · D-32/33 2계층)
- `20-spec/spec-005-reservation-board.md` **0.1.0** — 절 = 범위 · 폴더 · 실행 · env · 데이터 모델(사본 6 + ccc 2 · `customer.gender` · 이벤트 type 11) · 코디 역할 · KOS 연동(1시간 목록 · 날짜별 조회 · 상세 조회 · 동기 쓰기) · 상태 · 규칙 §5.1 ~ §5.14 · 화면 §6.1 ~ §6.8(시안 차이 22줄 · 시안 실명 치환 규칙 머리말) · API §7(새 15 · 전체 34) · KOS 반영 표 §8 · E2E §9(32 시나리오 + 「넣는다」 대조표) · OQ-701 ~ OQ-756 · 부록 A(DEC-006 → 절) · 부록 B(v3 「정할 것」 → OQ)
- `30-work/work-007-reservation-board.md` — WP 10(WP-KOS · 게이트 · BE0 ~ BE4 · FE1 ~ FE3 · E2E) · 고정점 · SPEC 절 → WP 표 · 병렬 · 하지 않는 것 · 검증 명령

고친 문서:
- README 4개(목록 한 줄씩) · `log.md`(한 줄) · DEC-005 `links.related` · SPEC-003 · SPEC-004 `links.specs`(frontmatter 만 · 본문 0)
- `reference/2026-10-12-cc-prototype/workflow-v2.md` 남은 4곳(r2 보고 §코디 확인 4): ① 1 정렬 [입실순 | 배치순] 취소선 + 드래그 순서 ② 화면 표 아래 헤더 「시술 현황」 하나 → 「현황」 하나(예약 현황 v3 · SPEC-005) ③ KOS 반영 표에 [시작] 되돌리기 2행 · [종료] 되돌리기 · 카드 드래그 순서 행 ④ 5 에 카드 순서 = 드래그 · ccc DB(KOS 반영 없음)

## 검증

| 브리프 §6 | 결과 |
|---|---|
| DEC-006 = `_RESUME` 10-26 예약 결정 줄 전부 | 10-26 줄 31(파일 45 ~ 75) + §1 메모 2 → 부록 A 대조표 · **빠진 줄 0**. 시술 현황 되돌리기 3줄(#45 · #46 · #48)은 「범위 밖 — SPEC-003」로 표기 |
| SPEC-005 KOS 호출마다 근거 리포트 절 | §4.2 표 2개 · §8 표 전 행에 근거 칸(R · C · U · RM · RT · MT · MC · CS · PD · TA · RXD · KDA 행). 「미확인」 줄은 WORK-007 WP-KOS K2 ~ K9 에 하나씩 |
| §9 E2E 가 브리프 §3 「넣는다」를 모두 덮나 | §9 끝 대조표 — 넣는 것 22줄 → # · 빠진 0 |
| WORK-007 WP 가 SPEC 절을 모두 덮나 | WORK-007 「SPEC-005 절 → WP」 표 — §1 ~ §10 · 빠진 0 |
| 실명 · id grep(새 4 + v2) | UUID · 24자 hex · 이메일 · `Bearer` 값 · `eyJ` · 금액 = 0(WORK-007 의 grep 명령 문자열 1건만 — 패턴 자체). 사람 이름 0(v2 의 기존 「박 원장」 예시 · 직함은 안 건드림) |
| frontmatter | 4개 모두 type · id · title · status(raw · proposed · draft · todo) · created/updated · tags · links · (DEC `up`) · (SPEC · WORK `sources`) |
| 린트 | 브리프의 `scripts/lint-pipeline.py` 가 워크트리에 없다 — 실행 못 함 |

숫자: DEC 43줄 · SPEC 절 10 + 부록 2 · API 15(조회 4 · 조작 11 → 경로 34) · E2E 32 · OQ 56(planner 기본값 41 · 열림 7(WP-KOS · E2E 확인) · 이번 판 밖 8) · WP 10.

## planner 기본값 — 사용자 확인 대기(SPEC-005 §10)

굵은 것이 구현 모양을 크게 정한다.
- **OQ-701** 하루 조회 = 내부 `get-schedules-for-reservation` 1번 · 4층만 · 시술 현황 조회와 안 합침(예약 사본 표 따로)
- **OQ-703** 개인정보 저장 = 카드 값만 · 상세 개인정보 · 특이사항 · 문진 답 · 수납은 열 때 KOS 직접(문진 이력만 저장)
- **OQ-704** 갱신 = front 10초 폴링 · back 날짜별 10초 캐시 · SSE 안 씀 · 조회 시간 제한 안 걺
- **OQ-705** 예약 조작 = **동기**(kos_op 대기열 안 씀) — 드래그 거절 원위치(D-20) · 등록 scheduleId 때문
- **OQ-714** 이동 = **내부 `update-reservation`** — 브리프 예시(공개 `updateReservationV2`)와 다르게 골랐다. 근거: 공개는 묶음 id 를 새로 만들고 의사 값을 안 쓴다(MC§2.3 · C§5) → 「당일 지정 의사」가 지워질 위험. 대신 ccc 실호출이 없어 WP-KOS K3 로 먼저 확인
- **OQ-719** [접수 완료] 켜짐 = 예약 + 방 + **신분 확인 완료**(시안 「신분 필드 모두 입력」 대체)
- **OQ-718** 접수 묶음 실패 = 되돌리지 않음 · 다시 누르면 남은 단계부터 · 다시 읽기 1초 × 5
- 그 밖: 702 그룹 id · 묶음당 카드 / 706 검색 내부 / 707 신규 규칙 back 도 / 708 KOS 중복이면 만들지 않음 / 709 신규 Badge / 710 담당자 = 시스템 계정 / 711 uuid4 / 712 길이 / 713 막는 것은 정원뿐 · 휴무 안 칠함 / 715 취소 접수 전만 / 716 부도 접수 막음 / 717 접수 = 내부 recept / 720 사용 중 / 721 방 배정 제목 / 722 데스크 = ccc 로그 / 723 경로 라디오 재진만 / 724 상담 시각 / 725 실장 호출 단계 / 726 금액 / 727 수납 필요 / 728 귀가 공개 / 729 처방전 / 731 확인 필요 글자 / 732 문진 이력 읽기 때 쌓기 / 733 신분 고객 단위 / 734 `flag-icons` / 735 작은 표시 / 736 취소 흐림 / 737 공지 읽기 / 738 이전 방문 글자 / 740 특이사항 직전 다시 읽기 / 741 여권 영문 칸 / 742 코디 = 관리자 권한 / 752 경로 `/reservations/live`

## 미결 · 주의점

- **WP-KOS 가 게이트**: ccc 가 KOS 에 한 번도 안 보낸 쓰기 — 신규 고객 생성 · `reserve` 전 칸(특히 `funnel` 요청 모양 OQ-754 · 동의 플래그 OQ-753) · 내부 이동 · 진행 경로 · 상담사 단독 · 공개 메모 · 고객 개인 정보 수정 · 바로 시술 끝 단계 · 귀가 `COMPLETED`. 하나라도 「안 받음」이면 SPEC-005 §8 개정(planner) — BE0 ~ BE2 · FE 는 기다리지 않음
- 데모 쓰기가 늘어난다(예약 · 고객 생성 · 귀가) — WORK-007 은 「지우지 않고 목록으로 알림」으로 적었다. 지울지는 사용자
- 브리프 §6 린트 명령(`scripts/lint-pipeline.py`)이 이 워크트리에 없어 돌리지 못했다
- `_RESUME` · 리포트 · workflow-v3 와 어긋난 곳은 찾지 못했다. 참고로 `_RESUME` §3 의 이 발주 줄 핸들 · task · dispatch 는 preamble 과 같다
- DEC-005 는 decisions 목록 대신 `links.related` 에 DEC-006 을 넣었다(DEC-005 `decisions` 칸은 앞 결정 목록이라) — 다르게 원하면 한 줄 옮기면 된다
