# reservation-spec-r4 결과 보고 — SPEC-005 0.4.0 (E2E batch 2 · 3 · 4 + 10-27 결정 + 공지 계약)

## 상태: done

## 수행 내용

- `para/projects/summer-star/cc-prototype/10-decision/decision-006-reservation-board.md` — r4 머리 · 새 절 「E2E batch 2 · 3 · 4 사용자 결정」 **D-58 ~ D-61**
  - D-58 부상태 색 규칙 · D-59 상담사 목록 제외(데모는 시스템 계정까지 다 넣음 · env 지점마다 · 데모 기본 빈 목록 — 앞 반 「시스템 계정 · 마취용 제외」 취소선) · D-60 웹 = 구현본 정본 · D-61 공지 [수정하기](추가 지시 1 의 Q-138 ~ Q-144 기본값까지)
  - 뒤집은 곳: D-04 앞 반 「시안이 정본이지만」 취소선 + 날짜 · 사유. 좁힌 곳(화살표): D-09 · D-11 · D-36
  - 부록 A 에 r4 표: `_RESUME` 10-27 줄 17개 + §1 메모 1개 → D 대조
- `20-spec/spec-005-reservation-board.md` — **0.3.0 → 0.4.0**
  - 머리말: 「화면 정본 = 시안」 취소선 → 「0.4.0 부터 웹 화면은 배포된 구현(`64e1989`)이 정본 · 시안 대조 안 함」 · `M:` 근거는 「1차 근거」로 둠. 「0.4.0 변경」 표
  - 고친 절: §1.1 · §1.2 · §2.3(`KOS_EXCLUDE_ACCOUNT_IDS`) · §3.2(`notice_save`) · §4.2(공지 다시 읽기) · §5.1(부상태 색) · §5.4(카드 잡기) · §5.7(시술실 팝오버 순서) · §5.8(상담사 제외) · §5.13(이전 방문 한글 · 펼침) · §5.14 · **§5.15 공지 [수정하기] 새로** · §6 머리 · §6.3 · §6.4 · §6.6 · §6.7 · §6.8 머리 · #5 · #20 · §7.2(`noticeEditable`) · §7.3(`flow.times` · 404 `reservation_gone`) · §7.4 · §7.5(`PUT /api/reservations/notice` · `notice_past_date`) · §7.6(경로 35) · §8(공지 4줄)
  - §9: #2 · #6 · #11(「카드를 잡아 끌 수 있다」) · #18 · #20 · #25 · #26 · #32(시안 대조 뺌) 고침, **#42 ~ #46 더함**, 대조표 · 단위 시험 문단도 고침
  - §10: OQ-737 닫음(D-61) · OQ-738 · OQ-757 ③ 고침 · **OQ-768 ~ OQ-772 새로**
  - 부록 A 에 D-58 ~ D-61 더함 · **부록 G 「E2E batch 2 · 3 · 4 반영표」 새로**(13줄)
- `30-work/work-007-reservation-board.md`
  - **WP-FIX2** 「E2E batch 2 · 3 수정」(완료 — `09b1edc` · `0fdeeb1` → main `64e1989`)
  - **WP-FIX3** 「E2E batch 4 · 공지 [수정하기]」(대기 — 계약 있음 · 데모 실물 1회가 완료 조건)
  - 절 → WP 표 · WP-E2E 완료 조건 #1 ~ #46 · 열린 것 r4
- `20-spec/README.md`(0.4.0) · `30-work/README.md` · `log.md`(r4 줄)
- `reference/2026-10-26-cc-reservation/workflow-v3.md`: 머리 r4 · 공지(패널 표 · 1절 · 정할 것 · KOS 반영 표) · 부상태 색 · 상담사 목록 제외 · 정할 것 「수납 정보 조회 주기」 → 모달 5초 폴링 닫힘
- 추가 지시 1(공지 자리만 → 계약)을 반영했다: §5.15 · §7.5 새 경로 1 · §8 · E2E #46(쓰기 · 고치기 · 취소 · 비우기 · 2000자 · 지난 날짜) · DEC D-61 · WP-FIX3 「계약 있음」 · OQ-770(같은 날 둘째 create)

## 검증

- **batch 2 · 3 · 4 지적 → 절**(SPEC-005 부록 G — 13줄 · 빠짐 0): b2 #1 ~ #9 · b3 #1 ~ #3 · b4 #1. 줄마다 바뀐 절 · 구현 커밋(`09b1edc` / `0fdeeb1` / 대기) · §9 # · OQ 를 달았다. 보류 · 처분 없음 항목도 행으로 남겼다(b2 #3 = 계약 · 구현 대기, b4 #1 = 대기)
- **10-27 결정 줄 → DEC**(DEC-006 부록 A r4 표 · 빠짐 0): §2 10-27 줄 17개 + §1 24행 메모 1개 = 18
  - 새 D 4: 35 · 42 · 60 · 61행 → D-59 · D-60 · D-58 · D-59/D-61
  - r3 D 6: 62 ~ 67행 → D-51 ~ D-57, 그대로
  - 소켓 메모 1: D-52
  - 이 문서 밖 7: 36행 진행 순서 · 37 ~ 41행 앱 · 43행 시술 카드 드래그 — SPEC-003 · SPEC-004 갈래
- **실명 · id grep**: `git diff` 에서 더한 줄에 UUID · 24자 hex · 이메일 · `Bearer ` · `eyJ` = **0**. 「마취용」 · 「KOS-DEMO」 는 계정 표시 이름이다(사람 실명 아님 · 피드백 문서 그대로)
- frontmatter: SPEC `version 0.4.0` · `sources` 3줄 더함 / WORK `sources` 2줄 더함 / DEC · WORK · SPEC `updated_at` 2026-10-27 그대로
- 경로 수: 34 → **35**(`PUT /api/reservations/notice`). 시험 이름 `test_route_count_35` 는 WP-FIX3 몫

## 어긋남 (문서 ↔ 구현 보고서 — 고치지 않음 · 코디 · 사용자가 정함)

| # | 문서(결정) | 구현(보고서 · 코드) | 어디 |
|---|---|---|---|
| 1 | D-59: 제외 목록 = 지점마다 env · **데모 기본 = 빈 목록**(시스템 계정까지 다 넣는다) | `KOS_EXCLUDE_ACCOUNT_IDS` 는 **시술 현황 원장 목록과 같은 env 하나**다. 지금 데모 env 에 값이 4개 있어 「마취용」이 빠진다(`.env.example` 은 빈 값). 데모 env 를 비우면 시술 현황 원장 목록도 바뀐다 | SPEC §2.3 · §5.8 · OQ-768 |
| 2 | D-59: 데모는 **시스템 계정까지** 다 넣는다 | `_counselors` 가 로그인 시스템 계정(`kos_token.account_kos_id`)을 **env 와 상관없이 늘 뺀다**(`service/reservations.py` 107행). 「KOS-DEMO」 는 다른 id 라 남아 있다 | SPEC §5.8 · OQ-768 |
| 3 | SPEC §5.15: 공지 = 그 날 **첫 번째 하나** | front `ResvAside.tsx` 는 아직 목록을 전부 그린다(WP-FIX3 전이라 예상된 차이) | WP-FIX3 |
| 4 | SPEC §5.1: 귀가 색 = gray-600(대기) / gray-300(완료). 범례 · 막대 · 상세 머리에 해당 | frontend b3 보고: 주 상태 색 「귀가 gray-600」 하나 + 완료 = 회색 규칙. 막대 · 머리에서 gray-300 을 쓰는지는 보고에 없다(코드 대조 안 함) | §5.1 |
| 5 | (낡은 줄) workflow-v3 머리 「화면 정본 = 시안」 · planner `role.md` 「시안이 화면 정본」 | D-60 과 다르다. workflow-v3 머리 줄은 브리프 §6-5 의 고칠 줄 목록에 없어서, `role.md` 는 allowed_paths 밖이어서 그대로 뒀다 | 코디 몫 |

## 미결 · 주의점

1. **OQ-768(권장 = 코디 · 사용자 결정)**: 셋 중 하나를 고른다. 권장은 ②
   - ① 데모 env 를 비운다 — 시술 현황 원장 목록에 마취용이 다시 나온다
   - ② 상담사 · 담당자 전용 env 를 따로 둔다. 데모는 빈 값, 시술 현황은 그대로
   - ③ 지금 구현 그대로 두고 D-59 를 「데모 = 제외 env 값만 뺀다」로 고친다
2. **공지(OQ-770)**: 같은 날 둘째 `create-notice` 와 지난 날짜 고치기를 KOS 서버가 막는지는 모른다. 확인하려면 데모 쓰기 허가가 필요하다
3. **`board.noticeEditable` · 요청 `noticeId` · 오류 `notice_past_date` · 경로 이름 `PUT /api/reservations/notice`** 는 planner 가 고른 이름이다. 추가 지시 1 의 「기존 규칙대로」에 따라 `/api/reservations/*` 아래에 PUT 으로 뒀다. 구현 때 바꾸면 SPEC 을 맞춘다
4. OQ-738: 시술 상태 `READY` 를 「진행」으로 표시하는 것은 구현값이다. KOS 의미는 확인하지 않았다
5. b4 #1(카드 안 잡힘)은 원인이 아직 없다. SPEC 이동 계약은 그대로 두고 §9 #11 에 잡기 단계만 넣었다
6. `_RESUME` 쪽 뒤집힌 줄(61행 「시스템 계정 · 마취용 제외」 · 10-23 「시안이 정본」)의 취소선은 `_RESUME` 주인(코디) 몫이라 손대지 않았다

## 추가 지시 2 반영 (2026-10-27 · `reservation-spec-r4-addendum-2.md`)

| 어긋남 # | 처분 | 고친 곳 |
|---|---|---|
| 1 · 2 (OQ-768) | **구현이 맞다**(코디 브리프 오기) — 제외 = 로그인 시스템 계정 늘 뺌 + `KOS_EXCLUDE_ACCOUNT_IDS`(시술 현황과 같은 env · 데모 값 그대로 — 「마취용」 빠짐). 「KOS-DEMO」 는 데모에서 보임 · **운영 배포 때 그 지점 시스템 계정 id 를 env 에 더한다**(배포 메모). 「데모 기본 = 빈 목록」 문장 지움(D-59 는 취소선 + 사유) | DEC-006 D-59 · r4 머리 · 부록 A 35행 · 61행 · 합계 / SPEC-005 0.4.0 변경 표 · §2.3 · §5.8 · §9 #45 · OQ-768 **닫음** · 부록 A · 부록 G b2 #5 / WORK-007 WP-FIX2 · 열린 것 / workflow-v3 상담사 제외 줄 / log |
| 3 | 처분 없음 — WP-FIX3 에서 구현 | — |
| 4 | 처분 없음 — reviewer_doc · 구현 리뷰가 코드로 대조(SPEC 그대로) | — |
| 5 | workflow-v3 머리 「화면 정본 = 시안」 · 「시안이 정본」 두 줄 아래에 「0.4.0(10-27)부터 배포된 웹 화면은 구현본이 정본 · 시안은 1차 근거」(D-60 링크) 덧붙임 — 지우지 않음. `role.md` 는 코디가 고침 | `reference/2026-10-26-cc-reservation/workflow-v3.md` |

검증: 문서 안 「데모 기본 빈 목록」 = 취소선 · 처분 주석 안에만 남음(본문 규칙 0) · 더한 줄 id · 토큰 grep 0.

## 추가 지시 3 반영 (2026-10-27 · `reservation-spec-r4-addendum-3.md` · review-doc r3 처분표)

| 리뷰 # | 처분 | 고친 곳 |
|---|---|---|
| F1 귀가 색 | 구현 값으로 — 막대 600/300 · 상세 머리 600/400 · 범례 200 + 800 · 귀가 대기 칩 200 + 700(귀가만 예외) · 완료 칩 100 + 500 (`view.tsx` `barStyle` · `headOf` · `LEGEND` · `MAIN_TONE` · `phaseStyle` 대조) | SPEC-005 §5.1 두 줄 · §9 #42 「귀가 대기 · 완료 칩 구분」 |
| W1 첫 번째 기준 | 화면 · board = 사본 순(`released_at, id`) 첫 번째 · 저장 대상 = 요청 `noticeId` 가 다시 읽은 KOS 목록에 있으면 그것 → 없으면 KOS 첫 번째 → 없으면 create | §5.15 · §7.5 요청 설명 · 단위 시험 문단 |
| W2-1 · W2-2 · W2-3 · W2-4 | 호출 없음 = 로그 없음 · `noticeId` = 저장 뒤 다시 읽은 행 id(create 새 행 · delete 지운 행) · front 글자 수 = trim 길이 · 편집 중 날짜 이동 = 막지 않고 버림 + 토스트 | §3.2 `notice_save` · §5.15 |
| W3 문구 | [수정하기] 다시 부르기 = 사본 다시 읽기(최대 10초) · 기준은 저장 직전 back 다시 읽기 | §5.15 |
| W4 · 결정 2 | §9 #43 = 단위 시험으로 확인 · 실물은 관찰되면 기록(날짜 이동 · 지우기 단계 취소선) | §9 #43 |
| W5 | WP-FIX3 완료 조건에 b4 #1 원인 보고 · 잡기 실물 확인 형식 · 범위 넓힘(`procedure/front/app/**` · 공용 컴포넌트) | WORK-007 WP-FIX3 |
| W6 | §9 #46 (g) 두 브라우저 · (h) 편집 중 날짜 이동 더함 | §9 #46 |
| W7 | WP-FIX1 완료 · WP-E2E 본문 #1 ~ #46 · frontmatter `status: doing`(태그도) | WORK-007 |
| W8 · 결정 1 | SPEC-005 §2.3 배포 메모 = 「사람이 아닌 KOS 계정(KOS-DEMO 류)」 · 원장 목록에서도 같이 빠지는 게 맞다. SPEC-003 §2 env 줄에 「상담사 · 담당자 목록과 같이 씀」 한 줄 + **OQ-519 닫음(D-59)** — SPEC-003 다른 곳 손대지 않음 | SPEC-005 §2.3 · SPEC-003 150행 · 856행 |

구현 보고(`reservation-fix3-backend-report.md`)와 대조: §5.15 4갈래 · trim · 2000 · 지난 날짜 409 · 경로 35 · `noticeEditable` 같음. 「호출 없음 = 로그 없음」은 구현 그대로 문서에 맞췄다. W1 저장 대상 · W2-2 `noticeId` 는 backend 추가 지시 1 로 코드가 맞출 몫이다(보고서의 `event_log` 키 `action` · `length` ↔ SPEC `op` 는 코드 리뷰 대조 — 문서는 그대로 `op`). 0.4.0 변경 표에 이 처분 한 줄. 더한 줄 id · 토큰 grep 0.

## 리뷰 r3 수정 (2026-10-27 · `reservation-review-code-r3-fix-instructions.md` — planner 몫 W1 문서)

- SPEC-005 §3.2 `notice_save` 줄 = `{date, noticeId, op, requestedNoticeId, length}` — `requestedNoticeId` = 요청 값(기록용 · null 가능) · `length` = 저장한 글자 수(내용 아님). `noticeId` = 저장 뒤 다시 읽은 행 id 는 그대로
- 0.4.0 변경 표 한 줄 · `log.md` 한 줄(r4 마무리 — review-doc r3 처분 + 이 줄)
- 검증: SPEC 안 `notice_save` 정의 1곳(§3.2) · 다른 절은 이름만 부름 · 더한 줄 id · 토큰 grep 0

## 추가 지시 4 (2026-10-27) — 예약 카드 이동 단계 = KOS 그대로

지시 `reservation-spec-r4-addendum-4.md` · 원천 `reservation-move-stage-report.md`(데모 실호출) · `_RESUME` §2 10-27 「예약 카드 이동 단계 = KOS 그대로」 · E2E batch 5 #1 · 코드 `domain/reservation_rules.py` `DRAG_MAINS`(`901267f`).

| 무엇 | 처분 | 바뀐 곳 |
|---|---|---|
| §5.4 끌 수 있는 카드 | 「`main ∈ {reserved, reception}`」 취소선 → **KOS 가 받은 단계 전부**(주 상태 7개 · `DRAG_MAINS`) · 바뀌는 필드 = 시각 · 그룹뿐 · 시술 대기 미확인(앞뒤가 받아 엶) · 막는 규칙이 생기면 409 `not_movable`(검사 자리 남김) | SPEC-005 §5.4 |
| OQ-714 | 「옮길 수 있는 단계」 부분 **닫음**(D-62) · 이동 길(내부 `update-reservation`)은 그대로 열림 | SPEC-005 §10 |
| DEC-006 | **D-62** 새 절 「E2E batch 5 사용자 결정」 · 부록 A r4 합계 아래 「추가 지시 4」 한 줄 · 뒤집은 D 없음 | DEC-006 |
| §9 #11 | 「상담 대기 카드도 끌어 다른 시각으로 놓으면 옮겨진다(단계 · 칩 그대로)」 단계 | SPEC-005 §9 |
| 0.4.0 변경 표 | 한 줄(추가 지시 4 · b5 #1) | SPEC-005 머리 |
| 부록 G | b5 #1(D-62 · `901267f`) · #2 · #3(고침 · `a7e793c` · 계약 문구 변경 없음) · 합계 아래 batch 5 줄 | SPEC-005 부록 G |
| log | 한 줄 | log.md |

검증: `grep -n "reserved, reception" spec-005` → 취소선 안 1곳만 · `grep -c "D-62"` DEC-006 · SPEC-005 모두 ≥ 1 · 비밀 grep(UUID · 이메일 · Bearer · JWT · 5자리 이상 숫자) 추가 줄 0. 버전은 0.4.0 그대로(지시 = 0.4.0 변경 표에 더함).
미결: 시술 대기 단계 이동은 데모에서 못 봄 — 실 데이터에 시술 대기 카드가 생기면 E2E 에서 한 번 끌어 본다(코디 판단).
