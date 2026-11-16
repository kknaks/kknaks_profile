# reservation-spec-r3 결과 보고 — SPEC-005 0.3.0 (E2E batch 1 반영)

## 상태: done

## 수행 내용

- `para/projects/summer-star/cc-prototype/10-decision/decision-006-reservation-board.md` — r3 머리 · **D-51 ~ D-57** 새 절 「E2E batch 1 사용자 결정」 · 뒤집힌 D 의 그 부분 취소선 + 「(2026-10-27 바뀜 → D-nn)」: D-12(세로축) · D-16(② · ⑤ 수면마취 · 지정 의사) · D-18(이름 경고) · D-32(진행 경로 = KOS 체크) · D-45(접수 신분 조건) · D-01 끝(화살표) · D-17 「고객 생성 때만」 · 부록 A 에 10-27 대조표
- `20-spec/spec-005-reservation-board.md` — **0.2.0 → 0.3.0**: 머리말 「0.3.0 변경」 표 · §1 · §3.2 · §4.2 · §5.2 · §5.5 · §5.6 · §5.8 · §5.10 · §5.12 · §5.14 · §6 머리(DS 컨트롤) · §6.2 ~ §6.8(#30 ~ #32 더함) · §7.2 ~ §7.6 · §8 · §9(#3 · #4 · #7 · #8 · #9 · #14 · #19 · #21 · #22 · #28 · #30 · #33 고침 · **#36 ~ #41 더함** · 대조표 · 단위 시험 문단) · §10 · 부록 A(D-51 ~ D-57) · 부록 D(U2 취소선) · **부록 F 「E2E batch 1 반영표」 #1 ~ #23**
- 코디가 전달한 **구현 확정 계약**을 §7 에 그대로 넣음: `reception{roomId, route:'consultation'|'direct'(기본 consultation)}` · `PUT …/route` 없앰 · `POST …/consultation-add`(본문 없음 · `{ok:true}`) · `can.addConsultation` · 등록 본문의 `consultationRequired` · `sedationRequired` · `doctorStaffIds` 없앰(**보내면 422**) · `form.doctors` 없앰 · `form.snsTypes: string[6]` · 상세 `reservation.consultationRequired` 없앰(`sedationRequired` 남김) · `flow.consultation` = ccc 접수 기록(route) + 지금 단계 · 고객 검색 빈 조건 = 목록(page)
- `30-work/work-007-reservation-board.md` — 0.3.0 · **WP-FIX1(E2E batch 1 수정)** 한 줄 · WP-E2E 완료 조건 #1 ~ #41 · 절 → WP 표 · 열린 것
- `20-spec/README.md`(0.3.0) · `30-work/README.md`(WP-FIX1 · SPEC 0.3.0) · `log.md`(2026-10-27 줄)
- `reference/2026-10-26-cc-reservation/workflow-v3.md` — 머리에 r3 · 고침 규칙(v2 와 같은 꼴) 한 줄 · 고친 곳: 원칙 「KOS 에 있으면 칸」(수면 · 지정 의사) · 1 시간축 세로축 · 2 등록 ② · ⑤ · 이름 경고 · 5 끝 단계 · 진행 경로 · 접수 신분 조건 · KOS 반영 표 「진행 경로」 줄

## 검증

**① 23건 → 절**(SPEC-005 부록 F — 23줄 · 빠짐 0): 정해짐 8(#4 D-57 · #8 D-56 · #12 D-54 · #13 D-51 · #15 D-55 · #17 D-52 · #21 · #22 D-53) · 대기 15 — 줄마다 SPEC 절 · §9 # · OQ 를 달았다.

**② `_RESUME` 2026-10-27 줄 → DEC**(DEC-006 부록 A r3 표 · 빠짐 0)

| `_RESUME` | D |
|---|---|
| 50행 진행 경로 ≠ KOS 체크 | D-51 |
| 51행 상세 폴링 5초 · 소켓 따로 | D-52 |
| 52행 등록 모달 칸 셋 뺌 | D-53 |
| 53행 신분 조건 뺌 · [+ 상담 추가] | D-54 · D-55 |
| 54행 이름 같은 고객 경고 뺌 | D-56 |
| 55행 시간축 06–22 | D-57 |
| §1 메모 10-27 소켓 검토 | D-52(뒤 반) · OQ-744 |

**③ 실명 · id grep**: 새/고친 5개(SPEC-005 · DEC-006 · WORK-007 · log · workflow-v3)에 `[0-9a-f]{8}-…` · 24자 hex · 이메일 · `Bearer ` · `eyJ` = **0**(WORK-007 의 1건은 기존 WP-KOS 검증 명령 안의 grep 패턴 문자열). 실명 · 실제 금액 · KOS id 는 더하지 않았다.

- frontmatter: SPEC `version 0.3.0` · `updated_at 2026-10-27` · `sources` 3줄 더함 / DEC · WORK `updated_at` · WORK `sources` 2줄
- 경로 수: `PUT …/route` −1 · `POST …/consultation-add` +1 → **34 그대로**(§7.6)

## 미결 · 주의점

1. **#3 칸 폭 해석(OQ-763 — planner 기본값)**: 시안 식의 `mx` = 한 시각 **겹침** 최대 수(`M:1723-1725`)인데, 사용자 「3명이 한 열에 들어가야 하는데」는 「정원만큼 늘 자리」로도 읽힌다. SPEC 은 시안 식(겹침) 그대로 · 옵션 = `mx = max(겹침, 정원)`. **권장: E2E #3 에서 사용자 눈 확인.**
2. **#7 ↔ #10 같이 지키기(OQ-765)**: 카드 = 2줄 콤팩트 + 줄 경계를 넘지 않음 → 15분 칸(36px)에서는 한 줄 높이 + 2줄 숨김으로 정했다. frontend 결과와 다르면 맞춘다.
3. **[+ 상담 추가] KOS 동작(OQ-767)**: backend 데모 1회 시험 결과 대기 — 안 받으면 §5.8 · §8 줄을 멈춤으로 바꿔야 한다. 켜짐 범위(상담 진행 · 시술 대기 · 시술 진행 · 귀가 대기)는 planner 기본값.
4. 열림(batch 1 보고 대기): OQ-761 고객 검색 빈 조건 · OQ-762 DS 컴포넌트 유무 · OQ-764 접수 측정 수치 · 칸 머리 한 꼴(OQ-758)과 공지 비율(OQ-757 ⑱)은 frontend 결과로 확정.
5. 코디 몫: `_RESUME` 10-26 줄(#51 시간축 · #52 끝 경고 · #59 진행 경로 · #66 ② · U2)의 취소선은 `_RESUME` 를 고치지 않아 남겼다. workflow-v3 「정할 것」의 「[+ 상담 추가]」 줄(「없음 — spec 때」)은 브리프가 고칠 곳으로 지정하지 않아 그대로 뒀다 — 지금은 낡은 줄이다(D-55).
