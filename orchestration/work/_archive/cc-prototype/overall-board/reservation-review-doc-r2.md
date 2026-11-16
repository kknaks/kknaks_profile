# 리뷰 리포트 — overall-board 예약 현황 / doc r2 (2026-10-26)

- 대상: SPEC-005 **0.2.0**(1047줄) · DEC-006(D-44 ~ D-50 더함) · WORK-007(r2) · log.md · README 4
- 기준: r1 리포트 `reservation-review-doc-r1.md`(FAIL 3 · WARN 9) · SPEC-005 부록 C · D · E · `_RESUME` §2 「SPEC-005 r1 사용자 결정(U1~U7)」 줄(파일 49행) · `reservation-kos-probe-report.md`(WP-KOS) · 시안 `M:` · 코드 `cc-prototype/overall-board/procedure/`(d05cd88 + 진행 중 작업 트리 — 읽기만)
- 범위: r1 지적이 고쳐졌나 · U1 ~ U7 · WP-KOS 반영 · **새로 생긴 모순만**. r1 PASS 자리는 다시 뒤지지 않았다
- read-only. 이 리포트 말고 고친 파일 없음
- 줄 번호: `spec` = `para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md` · `work` = `30-work/work-007-reservation-board.md` · `dec` = `10-decision/decision-006-reservation-board.md`

## 판정: WARN (FAIL 0 · WARN 6)

r1 FAIL 3 · WARN 9 는 모두 부록 C 처분대로 본문에 들어갔다(아래 §1 줄마다). U1 ~ U7 은 D-44 ~ D-50 · SPEC 본문 · E2E 와 맞고, WP-KOS 판정(「안 받음」 0 · 모양 다름 5)도 §3.3 · §4.2 · §4.4 · §5.6 · §5.10 · §8 에 리포트 그대로 들어갔다. **구현을 멈추게 할 FAIL 은 없다.** WARN 6 중 구현에 바로 넣을 만한 것은 W1(조작 뒤 상세 다시 읽기 지연)과 W2(구역 꺼진 칸 드롭) 두 줄이다. W3(WORK 대상 파일)은 코디가 범위를 넓혀 주지 않으면 코드 리뷰에서 「allowed_paths 이탈」 FAIL 이 잘못 날 자리다.

---

## FAIL

없음.

## WARN

### W1. 조작 뒤 상세는 한 번만 다시 읽는다 — KOS 반영 지연(0 ~ 3초) 때문에 방금 저장한 값이 되돌아간 것처럼 보일 수 있다 (구현 반영 권장)

- 어디: `spec:568`(§6.7) 「상세 모달 = 열 때 · 조작 뒤 · 그리고 … `state` · `flow_step` 이 바뀌었을 때」. 스케줄 표는 「직후 1번 + 2초 뒤 1번」(`spec:567` · `spec:270`)인데 **상세는 직후 1번뿐**이다
- 왜 문제: 쓰기 뒤 반영 지연 0 ~ 3초(`spec:270` · RT§0 · WP-KOS 「1초 첫 번째 다시 읽기에서 보였다」). WP-KOS 는 K6 · K7 을 **2.5초 뒤**에 읽었다(probe §2 머리) — 0초에 보이는지는 확인하지 않았다
  - 고객 정보 [저장](§5.13) → 직후 상세 GET 의 `get-visitor` 가 옛 값이면 `identity.complete` 가 아직 false → **E2E #21(`spec:789`) 「채워 [저장] → 켜짐」이 모달을 다시 열 때까지 안 켜진다**
  - 예약 메모 · 진행 경로 [저장]은 `state` 가 안 바뀌어 폴링으로도 상세를 다시 부르지 않는다 → 옛 메모가 다시 보인다
- 고칠 것(한 줄): §6.7 상세에도 「조작 성공 직후 1번 + 2초 뒤 1번」(스케줄 표와 같은 규칙). FE3 에서 바로 넣을 수 있다

### W2. 드래그 미리 막기가 「카드 구역이 꺼진 그룹 칸」을 막지 못한다 (구현 반영 권장)

- 어디: `spec:339` 「행이 없으면 `full = false`」 · `spec:343` 「(그 칸 그룹 · 끄는 카드의 구역) 슬롯이 `full` 이면 놓기 금지」 · `spec:343` 「이동은 구역을 바꾸지 않는다」 · `spec:643` `slots[]` = 「칸 × **켜진 구역**마다」
- 왜 문제: U1(D-44)로 카드가 두 구역에서 온다. 「미사용」 카드를 그 구역이 꺼진 그룹 칸으로 끌면 그 칸에는 그 구역 슬롯 행이 아예 없다 → `full = false` → 놓기 허용 → back 400(`spec:718` 「그 그룹에서 꺼진 구역」) 또는 KOS `ZONE_NOT_IN_RESERVATION_GROUP`(MC§2.2 내부 JS 목록) → 원위치 + 토스트. 깨지지는 않지만 D-20 「미리 막기」와 어긋난다. 그리고 front 는 「규칙 값을 다시 계산하지 않는다」(`spec:296` · `work:62`)라 스스로 막을 근거가 없다
- 고칠 것(한 줄): §5.4 에 「끄는 카드의 구역이 그 칸 `capacities[]` 에 없으면 놓기 금지(빨간 점선)」 — front 는 `columns[].capacities[].zoneId` 로 본다(새 키 필요 없음). `move` 409/400 중 어느 코드인지도 같이(지금 400 `invalid_request`)

### W3. WORK-007 대상 파일 목록이 실제로 손댈 파일보다 좁다 — 진행 중 작업 트리가 이미 밖을 만졌다

- 어디: `work:75` BE0 대상 = `schemas/reservations.py · api/reservations.py · service/fake_reservations.py · main.py` · `work:76` BE1 · `work:80` FE1 대상 = `AppHeader.tsx · app/(main)/reservations/** · components/reservations/** · lib/api.ts · lib/types.ts · lib/session.ts · package.json`
- 코드 작업 트리(`git -C …/cc-prototype/overall-board status`): back **`app/domain/errors.py`**(M · 새 409 코드의 도메인 예외 — SPEC `spec:100` 「도메인 예외」 규약상 피할 수 없음) · front **`app/layout.tsx`**(M — `flag-icons` css) · **`app/globals.css`**(M — `bg-cons` 등 상담 색, `spec:317` 「시안 인라인 클래스 그대로 복사」) · **`lib/hooks.ts`**(M — 폴링) · `package-lock.json`
- 넷 다 SPEC 이 요구하는 것을 하려면 필요한 파일이다. 목록에 없으면 reviewer(code) 가 rules.md 「allowed_paths 이탈은 무조건 FAIL」로 잘못 반려한다
- 고칠 것(코디): BE0 · BE1 에 `domain/errors.py`, FE1 에 `app/layout.tsx` · `app/globals.css` · `lib/hooks.ts` · `package-lock.json` 을 더한다고 워커 · reviewer 에 알린다(문서 개정은 다음 판에 같이 해도 된다)

### W4. 부도 고객 접수 허용(U4) 뒤에 남은 작은 막힘 — 진행 경로 · 예약 메모

- 어디: `spec:456` 진행 경로 라디오 켜짐 = `main = reserved` + 재진 · `spec:462` 예약 메모 [저장] = `main ∉ {canceled, noshow}`
- 왜: D-47(U4)로 부도 카드는 [접수 완료]를 할 수 있게 됐는데(`spec:369` · E2E #33), 접수 전에 진행 경로를 바꾸거나 메모를 고칠 수는 없다. 끝 단계는 `consultationRequired` 로 정해지므로(`spec:384`) **늦게 온 부도 고객의 경로를 ccc 에서 바꿀 길이 없다**(KOS 가 부도 일정의 `update-reservation{consultationRequired}` 를 받는지는 리포트에 없다 — K4 는 `RESERVED` 에서만 시험). 「KOS 그대로」(U4)에 비추면 `noshow` 도 `reserved` 처럼 둘을 여는 쪽이 맞아 보이나, 결정이 없는 자리다
- 처분: planner 기본값으로 한 줄 정하고 OQ-757 묶음에 올린다(① `main ∈ {reserved, noshow}` 로 넓힘 ② 그대로 막음). 사용자 결정까지 필요한 크기는 아님

### W5. 작은 계약 빈칸 둘

- 오류 본문 `fields`: `spec:610`(§7.1) 오류 모양 = `{error:{code, message}}(+ step · candidate)` — **`fields` 가 없다**. `spec:378` · `spec:711` 은 `identity_incomplete(+fields)` 를 쓰고 `work:60` 고정점은 `fields?` 를 적었다. 값이 KOS 키(`passportNumber`)인지 화면 이름(「여권번호」)인지도 없다(`spec:378` 「빈 칸 이름」 ↔ `spec:663` `fields:[{key, label, filled}]`). → §7.1 에 `fields?: [key]`(§7.3 `identity.fields[].key` 와 같은 값) 한 줄
- E2E #34(`spec:802`) 「WP-KOS 가 남긴 … 일정(**오늘** · 「기타」 칸)」 — 그 일정은 **2026-10-26** 일정이다(probe §5). E2E 가 다른 날이면 「오늘」이 아니다. 「2026-10-26 으로 날짜 이동」으로. 원내 현황(오늘만 — `spec:507`)에서는 그날이 지나면 안 보인다는 것도 #28 · #34 준비 줄에

### W6. 인덱스 버전이 0.1.0 그대로 (planner 보고 「미결」과 같음)

- `para/projects/summer-star/cc-prototype/20-spec/README.md:9` SPEC-005 **0.1.0** · `30-work/README.md:11` WORK-007 「todo (2026-10-26 · 문서 검수 전) · SPEC-005 0.1.0」 — 본문은 0.2.0(`spec:5`) · WP-KOS 완료 · 게이트 통과(`work:73-74`). allowed_paths 밖이라 planner 가 못 고쳤다 → 코디 한 줄씩

---

## 1. r1 지적 → 0.2.0 실제 반영 (줄마다)

| r1 | 부록 C 처분 | 본문에서 확인한 줄 | 판정 |
|---|---|---|---|
| **F1** 이어 하기 켜짐 모순 | `RECEPTION`(방 유무 무관) · 0단계 갈래 다시 정함 · 끝 단계 이후 ok · 붙은 방 고정 · 신분 조건 없음 · #23 두 갈래 필수 | `spec:365-372`(두 갈래 표) · `spec:378`(0단계 — KOS 단계로 갈래 · 끝 단계 이후 `{ok:true}` · `room_locked`) · `spec:381-384`(3 · 5 건너뛰기) · `spec:387`(다시 누르면) · `spec:457` · `spec:680-682`(`rooms` · `roomLocked` · `receiveMode`) · `spec:711` · `spec:791`(#23 (a) · (b) 필수) · `spec:562`(팝오버 잠김) | **PASS** — 5 성공 · 6 실패 뒤 `RECEPTION` + 방 있음 → `resume` · 방 고정 · 6 만 감. r1 이 짚은 길이 닫혔다 |
| **F2** `service/actions.py` 누락 | §3.4 전수 줄 · WORK BE1 · E2E #1 | `spec:220` · `spec:121` · `work:76`(대상 파일 · 완료 조건 「코디 수락 = 됨 · `doctorId` 없으면 400」) · `spec:769`(#1) · `spec:835`(단위 시험) | **PASS** |
| **F3** 4층만 ↔ D-10 | U1 → 두 구역 · #2 유지 · #35 | `spec:238` · `spec:242`(`zoneIds` 전부) · `spec:322-323` · `spec:339-340` · `spec:394-395` · `spec:401` · `spec:508-509` · `spec:770`(#2 「두 구역 일정 전부」) · `spec:803`(#35) | **PASS**(새 빈칸은 W2) |
| W1 이동 근거 · 오류 이름 | K3 로 근거 교체 · §4.4 표 · `errorProperties` | `spec:737`(HAR 은 `doctors` 없이 · ccc 는 K3 모양) · `spec:858`(OQ-714 「지워지는지는 시험 안 함」) · `spec:277-286`(문구 표 · 공개 이름은 「공개 · 미확인」 표시) · `spec:110` · `work:76` ②′ | **PASS** — 내부 4xx 본문 꼴은 여전히 실물 0건이지만 KOS 웹 JS 가 내부 오류를 `errorProperties` 키 · 이유로 읽는다(C§2.2 `reservation-create-report.md:212-217`) · 없으면 `className` 으로 떨어진다(`spec:277`) |
| W2 정원 초과 미확인 | §5.4 · #12 필수 + 관찰 · OQ-760 | `spec:346` · `spec:780` · `spec:904` | **PASS** |
| W3 「방 배정」 잇는 키 | §5.9 키 · §5.6 판정 셋 자리 | `spec:408`(`visit.kos_id` · `kos_sequence` · visit 없음 = 호출 0 · `is_room_task` 같은 식) · `spec:389` | **PASS** — 코드 `domain/rules.py:60-68` `is_room_task` = `kind == "etc"` · `room_kos_id` · `_called` 밖과 같은 식. `visit.kos_id` · `procedure.kos_sequence` 열 실재(`repository/db.py:22-39`) |
| W4 §10 밖 기본값 | OQ-757 묶음 16 | `spec:901` · 본문 `spec:314` · `:317` · `:318` · `:325` · `:329` · `:330` · `:487` · `:507` · `:569` · `:690` | **PASS** |
| W5 §6.8 빠진 차이 | #23 ~ #29 · Badge · 국가 이름 · 「n / N 입력」 | `spec:598-604` · `spec:494-495` · `spec:547` · `spec:549` · `spec:585` | **PASS** |
| W6 경로 수 내역 | 19 = 18 + 1 → 34 = 33 + 1 · 시험 이름 | `spec:725` · `work:75` — 코드 `tests/test_order.py:237` `test_route_count_19` 실재 | **PASS** |
| W7 오늘 사본 갱신 | 계산 전 10초 넘으면 오늘 1번 · 상세 · 0단계 | `spec:250` · `spec:378` · `spec:395` · `spec:401` · `spec:691` · `spec:788`(#20) | **PASS** |
| W8 D-38 근거 | 둘 다 | `dec:121` | **PASS** |
| W9 헤더 | U6 → 시술 현황 유지 · 활성 두 경로 | `spec:479-481` · `spec:769` · `work:58` · `work:80` | **PASS** — 코드 `AppHeader.tsx:14` `base: '/procedures'` 를 넓혀야 한다는 줄이 FE1 에 있음 |
| (r1 §5 빈칸 ③) 「그룹 없음」 `columns[]` | 모양 한 줄 | `spec:330` · `spec:625` | **PASS** |

## 2. 사용자 결정 U1 ~ U7 (`_RESUME` 49행)

| U | `_RESUME` | DEC-006 | SPEC-005 | 판정 |
|---|---|---|---|---|
| U1 | KOS 화면처럼 두 구역 전부 · 정원 · 사용 중 구역별 | `dec:139` D-44 | §3.2 `zone` · §4.2 · §5.2 · §5.4 · §5.7 · §6.4 · §7.2 · #2 · #35 | PASS(W2). `get-zones` 는 공개 · 데모 200 `data[2]`(`kos-demo-api.md:123` · R§4 `reservation-read-report.md:233`) — 근거 있음. 「다른 구역 방」 `get-rooms{zoneId}` 는 R§1 #1 과 같은 경로 · 다른 구역 값으로는 실물 0건(planner 보고 「미결」) — BE1 첫 실행에서 보임. 시술 현황은 방을 id 로만 찾는다(코드 `rules.py:84` · `board_service.py:86` · `actions.py:110` · `push.py:91` — 목록으로 거르는 곳 0)라 행이 늘어도 회귀 없음 |
| U2 | KOS 신분 칸(외국인 = 여권 영문명 · 생년월일 · 여권번호) 다 채움 → 켜짐 · ccc 는 표시만 | `dec:140` D-45 | `spec:428-436` · `spec:441` · `spec:663-664` · #14 · #21 | PASS — 시안 `M:2178-2180` `ID_F`(외국인 3칸 · 내국인 생년월일 · 주민등록번호) · `M:1840` `cantReceive` 와 같은 뜻. 「영문명 = 성 · 이름 중 하나 이상」 · 「국적 빈 값 = 외국인」 · 「이어 하기는 신분 조건 없음」은 OQ-759 기본값으로 올라 있다(아래 「사용자 확인 권장」) |
| U3 | 카드 값만 | `dec:141` D-46 | `spec:146` · OQ-703 닫음 | PASS |
| U4 | 부도 접수 허용 | `dec:142` D-47 | `spec:369` · `spec:455` · `spec:747` · #33 | PASS — KOS `recept` 가 `NO_SHOW` 를 받아 `IN_PROGRESS`(CS§2.1 ① `reservation-consultation-report.md:26` · `:98`) 리포트 그대로. 남은 작은 막힘 W4 |
| U5 | 이어 하기 | `dec:143` D-48 | F1 줄 | PASS |
| U6 | 첫 화면 시술 현황 유지 | `dec:144` D-49 | `spec:479-481` · #1 | PASS |
| U7 | 카드 「수납 필요」 | `dec:145` D-50 | `spec:495` · `spec:407-409` · `spec:602` · #34 | PASS — 모양 = 시술 현황 카드와 같은 Badge warning sm(코드 `components/procedures/OrderCard.tsx:97-103` · 시안 `M:826`). 원내 현황 카드는 danger(`spec:511`) — 시안 `M:476` · `M:1963` 원내 현황 Badge 도 danger 라 맞다(두 자리 색이 다른 것은 시안대로) |

`_RESUME` 50행(「코드까지」 범위 · 「신분 확인은 웹 수동 표시」)과도 D-45 「표시만」이 어긋나지 않는다.

## 3. WP-KOS 반영 (`reservation-kos-probe-report.md`)

| probe | SPEC 반영 줄 | 판정 |
|---|---|---|
| 주의 1 · 2 문진 제출본 최상위 · 없음 = 400 + `errorProperties` | `spec:262` · `spec:285` · `spec:423` | PASS |
| 주의 3 `room:{id:""}` | `spec:158` `tasks` · `spec:204` · `spec:382` · `spec:748` | PASS |
| 주의 4 `change-tasks-room` 약 1초 | `spec:270` · `spec:383` · `spec:749` | PASS |
| 주의 5 시각 밀리초 | `spec:199` · `spec:760` | PASS |
| `funnel` 모양 · `funnelCategory` 안 보냄 | `spec:357` · `spec:733` | PASS(probe §0 그대로) |
| K2-2 정보성 알림 동의 = true | `spec:361` · `spec:735` | PASS |
| K3 `doctors` 실어 보냄 · 남음 | `spec:737` | PASS |
| K4 · K5 단독 수정 · 접수 뒤 단계 미시험 | `spec:741` · `spec:752` · #25 | PASS |
| K7 없던 키 안 보냄 | `spec:743` | PASS — §5.13 `spec:447` 「빈 칸으로 고치면 빈 문자열」은 「있던 키를 지울 때」라 모순 아님 |
| K9 · K9b 귀가 · 400 | `spec:416` · `spec:286` · `spec:755` | PASS(이유 못 가름도 그대로 적음) |
| K10 남긴 데모 데이터 | `spec:765` · OQ-751 | PASS(W5 「오늘」) |
| 리포트에 없는 KOS 동작을 지어낸 곳 | — | **0** |
| 남은 「미확인」 = 딥링크 2 · 접수 뒤 [실장 호출] · 정원 초과 | `spec:729` · `spec:753-754` · `spec:752` · OQ-760 | PASS — 전부 E2E 몫으로 이름이 붙어 있다 |

## 4. 계약 완결성 — 새로 본 것만

- BE ↔ FE 고정점(`work:56-65`)과 §7 이 맞는다: `zones` · `capacities` · `cards[].zoneId` · `rows[].plusAllowed` · `identity.fields/complete` · `receiveMode` · `roomLocked` · 409 `identity_incomplete` · `room_locked`. 빈칸은 W2 · W5 둘
- 접수 묶음 갈래가 사본(10초 늦음)과 KOS 실제가 다를 때: 사본 `reserved` · KOS `RECEPTION` → 0단계가 이어 하기로 바꿈 / 사본 `RECEPTION` · KOS 끝 단계 이후 → 보내지 않고 ok(`spec:378`) — 두 방향 다 닫혀 있다
- 시술 현황 회귀: 코디 수락 분기(`spec:220`) · 헤더 항목 · 활성 판정(`spec:480`) · 다른 구역 방 행(위 U1) · 접수 뒤 `tick()` — 새 회귀 자리 없음

## 5. public

새 줄 포함 SPEC · DEC · WORK · log 에서 UUID · 24자 hex · 이메일 · `Bearer <값>` · `eyJ` · 금액 꼴 = 0(WORK `:73` grep 패턴 문자열 1건 — 값 아님 · r1 과 같음). probe 의 시험 고객 지어낸 이름(`WPKOS Probe`)도 SPEC · WORK 에 옮겨지지 않았다(0). 구역 이름 「4층」 · 「미사용」 · 방 이름 「A-레이저실」은 KOS 데모 설정값(SPEC 에는 구역 이름만).

---

## 사용자 결정 필요

새로 사용자 결정이 꼭 필요한 것은 **없다**. 아래는 planner 기본값이지만 U2 · U4 의 테두리를 정하는 자리라 **한 번 확인을 권장**한다(구현은 기본값대로 가도 된다).

| # | 무엇 | 지금(기본값) | 권장 |
|---|---|---|---|
| R1 | 이어 하기(`RECEPTION`)는 신분 칸 조건을 걸지 않는다(OQ-759 · `spec:370`) | KOS 가 이미 접수를 받았으니 ccc 가 막지 않음 | 그대로 — 막으면 ccc 에서 끝 단계로 갈 길이 없다(r1 F1 의 원인). 단 「KOS 에서 신분 없이 접수된 고객도 ccc 에서 상담 대기로 넘어간다」를 사용자가 알고 있어야 |
| R2 | 부도 카드의 진행 경로 · 예약 메모(W4) | 막힘 | `noshow` 도 `reserved` 처럼 열기(U4 「KOS 그대로」) — planner 기본값으로 처리 가능 |

## 고객이 실물에서 만날 자리

- 고객 정보를 채워 [저장]해도 [접수 완료]가 바로 안 켜지고 모달을 다시 열어야 켜질 수 있음 · 예약 메모 저장 직후 옛 글이 다시 보일 수 있음(W1 — E2E #21 · #15)
- 「미사용」 구역 카드를 그 구역이 없는 그룹 칸으로 끌면 놓이는 것처럼 보였다가 원위치 + 토스트(W2 — E2E #35 근처)
- 늦게 온 부도 고객의 「상담 필요 / 바로 시술」을 ccc 에서 못 바꿈(W4 — E2E #33)

## 참고(기존 부채)

- SPEC-003 `:742` 경로 수 내역 「router 18 + health」(r1 과 같음 · SPEC-005 `spec:725` 가 적어 둠)
- DEC-006 `_RESUME 10-26 #n` 번호가 r2 U 줄 때문에 한 행씩 밀림 — `dec:42` 에 적혀 있다(고치지 않음이 맞다)
