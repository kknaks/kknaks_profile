# 리뷰 리포트 — day-reservations-fix / doc (2026-11-27)

대상: mediness `kknaksss/day-reservations-fix-spec` 미커밋 변경(base `origin/main` `b9ac374e`) — `products/day/` 8 파일(10-decision · 20-spec.md · spec-000 · 002 · 003 · 006 · 007 · log). 코드 대조 = CENTURION_DAY `origin/dev` `65506f35`(읽기만). 파일은 고치지 않았다.

## 판정: WARN

FAIL 없음. 공개(open) KOS 호출을 새로 둔 곳 0, 뒤집힌 결정을 옛 쪽으로 쓴 곳 0, 지어낸 화면 문구 0, lint `--strict` products/day ERROR 0 · WARN 0.
WARN 8건. 결정 반영이 빠진 곳 1(기존 공개 호출 목록), 동기화 문서끼리 어긋남 2, 앱 JSON 빈칸 1, 형식 4.

## FAIL

없음.

## WARN

| # | 파일:줄 | 무엇 | 근거 | 고칠 방향 |
|---|---|---|---|---|
| W1 | `spec-002-procedure-board.md:1059` · `spec-007-reservation-detail.md:635` | 결정 「DAY 의 KOS 호출 = 내부 API 만(… **기존 공개 호출은 목록만**)」 중 **목록** 부분이 어디에도 없다. 새 공개 호출을 두지 않는다는 말만 있다. 코드에 남은 공개 호출: `emr/kos/identity.py:29-31`(`visitor/open/v1/queries/get-visitor-questionnaire` · `get-questionnaire-agreements` · `commands/submit-visitor-questionnaire` — 고객 문진 웹 양식 · 동의 · 제출) · `schedule/open/v1/commands/cancel-reservation`(spec-002:1250) · 데모 시드 도구(spec-002:1059 예외) | `_RESUME.md` §2 11-27 첫 행 | spec-002:1059 원칙 문단 뒤에 「지금 남은 공개 호출(목록만 · 이번에 바꾸지 않음)」 한 줄짜리 표를 둔다. 문진 읽기 · 양식 맞춤에는 넣지 않는다고 적는다 |
| W2 | `spec-007:633` · `:658` ↔ `spec-002:1072 · 1074` | KOS 문진 읽기를 **일정 태스크 안에서** 부르는지, 구매 회차처럼 **일정 회차 뒤 별도 태스크**로 부르는지 안 정했다. `:658` 「10초 회차 실행 시간이 늘어나는 것은 알고 감」은 태스크 안에서 부른다는 읽기다. 그런데 spec-002:1072 는 「일정 태스크의 실행 시간 · DB 사용은 새 동기화 전과 같다(검수 3)」 · 「앞 회차가 안 끝난 병원은 그 회차를 건너뛴다」고 한다. 문진 없는 고객이 많은 날엔 일정 회차가 밀린다 | 결정 「10초 일정 동기화에 같이」(어느 태스크인지는 말하지 않음) · spec-002 검수 3 원칙 | 코디 기본값으로 닫기를 권한다: **일정 회차가 끝난 뒤 발행하는 별도 태스크**(구매 회차 ②~④ 와 같은 꼴 · 입력 = 같은 일정 응답의 고객). 그 뒤 spec-007:633 · :658 · spec-002:1075 를 같은 말로 고친다 |
| W3 | `spec-002:1076` | 「오늘 회차 호출 수 = 2 + 바뀐 고객 수 × 2 … 10초마다 오늘 고객 전부를 부르지 않는다(결정 1)」가 그대로다. 이제 회차마다 「제출 없음 · 6개월 경과 고객 수」번이 더 붙는다(spec-007:658). 오늘 고객 대부분이 문진 없는 신규면 사실상 오늘 고객 전부를 10초마다 부른다 — 결정 1 문장과 맞지 않는다 | 결정 「제출 없음 / 6개월 경과 고객만 매 회차 읽음」(사용자가 이 호출량을 받아들임) | :1076 에 「+ 문진 미확인 고객 수(DAY-SPEC-007 고침 8)」를 더하고, 결정 1 의 예외라고 적는다 |
| W4 | `spec-003-mobile-app.md:72` ② · `spec-007:903` OQ-D47 | 앱 JSON 에서 「6개월 경과」를 **어떤 칸으로 싣는지**가 없다. 앱(`app/lib/model/reservation.dart:396` · `ui/reservation_detail.dart:323-`)은 `questionnaire` 가 null 이면 「작성 필요」, 아니면 「제출됨 · HH:MM」을 그린다. 만료 고객은 마지막 행이 실려 앱에 **「제출됨」 + [문진 QR] 보임**(`actions.questionnaireQr = true`)이 같이 뜬다. 앱 화면을 안 고치는 건 맞지만, 서버 JSON 계약이 비어 있어 be 가 추측으로 메워야 한다 | rules 「워커가 추측으로 메워야 하는 빈칸」 · spec-007 Rule 11(`:802`) | spec-007 앱 JSON 짝(`:545`)에 칸 하나를 이름 제안으로 둔다(예: `questionnaire.expired: bool`). 앱이 지금 보이는 모양(「제출됨」 + 버튼)은 OQ-D47 에 「알고 감」으로 적는다 |
| W5 | `spec-000-data-model.md:62` | 기존 「2026-11-24 개정 ②」 단락이 `> > ` 이중 인용으로 바뀌었다(diff `-> 2026-11-24 …` → `+> > 2026-11-24 …`). 내용은 같은데 렌더링이 한 단 들어간다. 의도하지 않은 변경으로 보인다 | git diff | `> ` 하나로 되돌린다 |
| W6 | `spec-002:8` · `spec-003:8` | 두 파일 본문을 바꿨는데 frontmatter `last_updated: 2026-11-26` 그대로 | `rules/document-pipeline.md` §YAML Frontmatter(`last_updated` = 마지막 수정일) | `2026-11-27` 로 |
| W7 | `20-spec.md:17` | 지도 앞부분 「카드 높이 한 줄 고정(R70)」 · 「한 칸 한 줄 최대 5개 · 넘치면 아래 줄(R64)」에 취소선이 없다. 뒤에 「개정 ⑯ … R70 뒤집음」만 붙어 있어서 앞만 읽으면 옛 규칙으로 읽힌다 | 결정 「F2 … R70 뒤집음」 · 지도는 최신 상태만 미러 | `~~카드 높이 한 줄 고정(R70)~~` 로 긋고, R64 는 「OQ-R41」 꼬리표 |
| W8 | `log.md:17` | `PR` 칸이 「근거 … (PR 전 · 코디가 PR)」다. 규칙상 PR 번호나 닿는 링크여야 한다 | `rules/document-pipeline.md` §log.md 「모호한 단어 단독 금지」 | 코디가 PR 을 올릴 때 `#NNN` 으로 바꾼다(지금은 비차단) |

## 참고(판정에 안 넣음)

- **U-10 [+] 자리**(`spec-006:319`): 「겹친 카드들의 오른쪽 첫 빈 자리」. 앞 자리가 다시 비는 경우(lane 0 빔 · lane 1 사용 중)에 맨 오른쪽인지, 빈 lane 0 인지가 갈린다. 구현에서 「겹친 카드 lane 최댓값 + 1」로 읽으면 결정(오른쪽 여백 [+])과 맞는다. 결정은 [+] 를 오른쪽 여백 자리로만 말했다. SPEC 은 기존 hint 처럼 열 안 빈 곳 전체로 넓혔는데, 기존 동작(RV-30 열 안 빈 곳 누르면 등록) 그대로라서 지어낸 규칙은 아니다.
- **중복 가르기 빈틈**(`spec-007:625` · `:638`): 고침 8 전에 DAY 웹에서 내 KOS 로 간(`crm_status = sent`) 행에는 `external_ref` 가 없다. 이 고객이 6개월이 지나 다시 읽히면, KOS 가 같은 옛 제출을 돌려줄 때 `read` 행이 하나 더 생긴다. 판정 결과(경과)는 같지만 이력이 두 줄이 된다. 백필할지, 「알고 감」으로 둘지 WORK 에서 한 줄 정하면 된다. OQ-D46 ②(제출 응답 `questionnaireId` = 읽기 `id`?)가 닫혀야 이 가름 전체가 맞다.
- **OQ-D44 의 함정**(`spec-007:752-753`): 지금 규칙대로면 「링크 복사하기」 뒤 「링크 열기」를 누르면 **복사한 링크가 바로 410** 이 된다(같은 종류 열린 요청 취소). 케이스 표에 드러나 있고 OQ 로 열려 있어 판정엔 안 넣었지만, 직원이 처음 쓸 때 바로 부딪칠 자리다.

## 직원이 실물에서 만날 자리

- 「링크 복사하기」를 눌러도 알림 글자가 없다(OQ-D43). 복사됐는지 모른다.
- 복사 → 열기, 또는 복사 → 태블릿 순서로 누르면 앞 링크가 닫힌다(OQ-D44).
- 15분 카드 = 35px. 이름 · 국가 · 담당자 줄이 잘린다(OQ-R42).
- 앱 상세: 6개월 경과 고객에 「제출됨 · HH:MM」과 [문진 QR] 이 같이 보인다(W4 · OQ-D47).
- 앱 예약현황 표: 서버 `lane` 이 겹침 기준이 되면, 앱(`app/lib/ui/reservation_table.dart` — 고정 66 · `lane`/`line` 그대로 그림)에서 시작 행 안에 빈 자리가 생긴다(OQ-R44).
- 지난 방문에 낸 문진(6개월 안)이 「제출됨 · HH:MM」 시각만으로 보여 오늘 낸 것처럼 읽힌다(OQ-D48).

---

## 결정 대조 표 (`_RESUME.md` §2 · 2026-11-27 행 · 위 → 아래)

| 결정 행(요지) | SPEC 반영(파일:줄) | 판정 |
|---|---|---|
| DAY 의 KOS 호출 = 내부 API 만 · 공개 새로 안 둠 · 양식 맞춤도 내부 · 근거 없으면 OQ · **기존 공개 호출은 목록만** | spec-007:63 ⑤ · :635(「공개(open) 경로는 쓰지 않는다」) · :652 · :902 OQ-D46 ① · spec-002:1075 · 10-decision:40 | 반영. **목록은 없음 → W1** |
| KOS 문진 읽기 경로 = 내부 `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy` · 양식 경로 내부 근거 없으면 OQ | spec-007:635(경로 글자 일치) · :652 · :902 · spec-002:1075 · 20-spec.md:18 | 반영 · 경로 한 글자씩 일치 |
| 진행 = SPEC → Issue → 코드 | (절차 — SPEC 내용 아님) | 해당 없음 |
| KOS 문진 동기화 = 10초 일정 동기화(`day.emr.sync_schedules_hospital` · `tasks/emr.py:3`) · 6개월 안 고객 건너뜀 · 제출 없음/경과만 매 회차 · 중복 = `external_ref` · `inputType`·`subText` = 양식 답 id · 400 = 제출 없음 | spec-007:633-641 · :652 · :625(제출 id 남기기) · spec-000:32 ④ · :38(`entity_type` 값) · spec-002:1075 | 반영. 코드 `tasks/emr.py:3-4` · `:47` 일치. 태스크 자리 → W2, 호출 수 → W3 |
| 모달 디자인 = 이번 SPEC 에 안 넣음 | spec-007:63(「모달 디자인은 범위 밖」) | 반영 |
| KOS 문진 실물(공개 경로 · 고객 단위 · 한 건 · `createdDateTimeUtc` UTC · 바뀐 것만 길 없음 · 15/15 · 키 4 다름 · `inputType`·`subText` 없음) | spec-007:634 · :636 · :637 · :646-656 · spec-000:50 | 반영. 경로는 위 행(내부)이 덮음 — 공개 경로를 쓴 곳 없음 |
| F6 원인 확정 · origin 필수 4곳 + GET 실제 service 시험 | spec-007:583 규칙 9 · :545 · :803 Rule 12 · 케이스 :757-759 · spec-003:72 ① | 반영. 코드 4곳(`routers/reservation_detail.py:179 · 327 · 407` · `routers/api/reservations.py:104`) · `services/reservation_detail.py:134` 기본값 `None` · `services/displays.py:132` 일치 |
| 시간 겹침 배치(12:00~13:00 첫 자리 · 12:30~13:30 옆 자리 12:30 부터 · 겹치는 동안만) | spec-006:210 · :732 Rule 15 · 케이스 :620-621 · :378 | 반영(13:00 예시는 「겹치는 동안만」을 그대로 편 것) |
| 팝오버는 한 단계(문진 QR = 링크 복사하기·링크 열기 / 기기 줄 · 여권 = 기기 줄만 · 「태블릿에 띄우기 ▸」 없음 — 앞 행 뒤집음) | spec-007:63 ① · :129 · :577-578 · :523 · 케이스 :751 · :756 · 20-spec.md:18 | 반영. 뒤집힌 아래 행(두 단계 메뉴 · 메뉴 3항목)을 옛 쪽으로 쓴 곳 없음(:575 은 취소선 · :911 대조 표가 덮음을 명시) |
| 문진·여권 방식 통일(같은 기기 팝오버 · 고르면 바로) | spec-007:577-579 · :581 | 반영(메뉴 부분은 위 행이 덮음) |
| 태블릿 흐름 = 고르면 그때 요청 · 바로 보냄 · 웹 「먼저 QR → [태블릿에 보내기]」 없앰 | spec-007:566 규칙 2 · :63 ② · :580 | 반영 |
| F6 증상 정정(QR 잠깐 떴다 사라짐 · 원인 미확인) | spec-007:583(「수십 ms 만에 사라짐」 — 원인은 위 행으로 확정) | 반영 |
| F1 여백 = 카드 반 폭(140 → 70) · 호버 점선 [+] · 툴팁 「그룹 \| 시작 ~ 끝」 · 끝 = 그룹 간격 | spec-006:54 ① · :180 · :316-321 U-10 · :379 · 케이스 :624-626 · :781 | 반영. 코드 `services/reservation_book.py:239`(`end = start + interval_minutes`) 일치 |
| F3 메뉴 · 고른 뒤 요청 · 웹 「이 화면 QR」 없앰 · 링크 10분 | spec-007:566 · :580 · :63 ① | 반영(메뉴 3항목은 위 「한 단계」 행이 덮음) |
| F5 기기 팝오버 · 기기명 · 점(초록 연결 · 빨강 미연결) · 미연결도 보이고 누름 · 여권도 같은 팝오버 | spec-007:579 · 케이스 :755 · 20-spec.md:18 | 반영 |
| F4 6개월 = 고객 마지막 제출일 · 재진에도 · env · 지나면 「6개월 경과」 | spec-007:222 · :226-235 U-3 표 · :481 · :802 Rule 11 · :876 OQ-D27 · 케이스 :760-762 · spec-000:47 | 반영. 고객 차트 원천 `queries/customers.py:448-456` 일치 |
| F4 KOS 문진도 동기화(문항 같음) | spec-007:627-658 | 반영 |
| F2 카드 높이 = 예약 길이 비례(30 = 1칸 · 60 = 2칸 · 15 = 반 칸) · R70 뒤집음 · 겹치면 옆 자리 | spec-006:54 ② · :208 · :211 · :617-619 · :780 · 20-spec.md:17 | 반영. 코드 `_card_span` 「최소 30분」(`policies/reservations.py:206`)을 안 쓰는 것도 명시(:208). 20-spec.md 앞 글 취소선 없음 → W7 |
| 6개월 재작성 정책 필요 | (위 F4 행으로) | 반영 |
| slug | 해당 없음 | — |

## KOS 대조 (be-kos-questionnaire-1 리포트 ↔ spec-007)

| 항목 | be-kos | SPEC | 판정 |
|---|---|---|---|
| 경로 | 내부 `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy` 실물 200 · 같은 id · 시각 · 키 · 감싸기 없음 | :635 같은 글자 · body `{visitorId}` | 일치 |
| 응답 키 | `id` · `visitorId` · `visitorName` · `phoneNumber` · `phone{…}` · `address` · `addressDetail` · `dateOfBirth` · `gender` · `phoneticName` · `createdDateTimeUtc` · `answers[]` · `agreements[]` | :636 — 13개 모두 · `phoneNumber` · `phoneticName` · `seq` 안 씀 | 일치 |
| 답 맞춤 | `questionId`→`parentQuestionId` · `questionTitle`→`parentQuestionTitle` · `answerId`→`id` · `answerTitle`→`title` · `memo`→`inputText`(INPUT_BOX 때만) · `inputType`·`subText` 없음 · `seq` 빈 값 | :646-654 같은 짝 · 같은 조건 | 일치 |
| 머리 칸 | `visitorName`→`name` · 나머지 같은 이름 | :655-656 | 일치 |
| 400 | `InvalidRequestException` `visitorId NotFound` = 제출 없음/고객 없음 같은 코드 | :639 | 일치 |
| 제출 id | 제출 응답 `questionnaireId` 를 지금 버림(`emr/kos/identity.py:161-165`) | :625 · OQ-D46 ② | 일치(코드 `submit_questionnaire` = `:162`) |
| 공개 호출 새로 | — | 0곳(양식 공개 경로는 「선택지에 두지 않음」 :902) | **PASS** |

## 코드 실물 대조

| 항목 | SPEC | 코드(`65506f35`) | 판정 |
|---|---|---|---|
| `questionnaire_history.visit_id` null 허용 | spec-000:47 「이미 null 허용」 | `models/reception.py` `fk("visit.id", nullable=True)` | 같음 |
| `source` 값 `read` | spec-000:50 · 「쓰는 코드 없던 값」 | `enums/reception.py:12-15` `READ = "read"` | 같음 |
| `fetched_at` · `crm_status` null | spec-000:55 · :56 | 칸 있음 · nullable | 같음 |
| `external_ref.entity_type` 열린 문자열 · `external_updated_at` · `synced_at` | spec-000:38 · spec-007:637-638 | `models/customer.py:134` String · `:142` · `:143` · 유일키 (hospital, vendor, entity_type, external_id) | 같음 · migration 없음 맞음 |
| `tasks/emr.py:3` · `sync_schedules_hospital` | spec-007:633 | `tasks/emr.py:3-4` · `:47` · `:102` | 같음 |
| origin 없는 detail_view 4곳 | spec-007:583 | `routers/reservation_detail.py:179 · 327 · 407` · `routers/api/reservations.py:104` · 웹 띄우기 `routers/reservation_displays.py:68` 만 origin 넘김 | 같음 |
| 배치 정책 | spec-006:732 · OQ-R41 | `policies/reservation_layout.py:28-29`(`LANES = 5` · `ROW_MINUTES = 30`) · `:119-150` `seat` · `:152-164` `rows` | 바꿀 자리 맞음 |
| 앱 표가 같은 `lane`·`rows` 받음 | spec-006:845 OQ-R44 · spec-003:72 ③ | `schemas/reservations.py:49 · 64` · `app/lib/ui/reservation_table.dart:2-3 · :173 · :249` | 같음(OQ 근거 맞음) |
| 공개 KOS 호출 현황 | (목록 없음) | `emr/kos/identity.py:29-31` 공개 3 | → W1 |

## 문서끼리 대조

- spec-006 ⑯ ↔ spec-007 고침 8 ↔ spec-000 ④: 칸 · 값 · OQ 번호가 서로 맞는다(`visit_id` 빔 · `source = read` · `external_ref` `questionnaire_history` · R70 뒤집음 · U-1 등록 창 RV-30 그대로).
- spec-006 :314 ↔ spec-007 :521: 동행 조건(R71 같은 30분 행 · 저장은 같은 시작 시각)은 둘 다 그대로라 새 어긋남 없음(옛 차이 그대로).
- spec-002 ↔ spec-007: 정본 = spec-007(:63 「어디에 두나」 · R60 선례), spec-002 는 링크 한 줄. 다만 태스크 자리 · 호출 수 → W2 · W3.
- spec-003 :72: 앱 화면 변경 없음 · 같은 service 만. JSON 칸 → W4.
- 10-decision :40: ESC 새로 없음 · DAY-ESC-001 참조만(비차단) — 규칙에 맞음.

## 범위

- 모달 디자인 · 외국인 신분확인 · 기획안(`00-baseline/planning/`) · 다른 제품: **안 건드림**(`git status` = products/day 8 파일 · 신분확인은 F6 origin 한 줄뿐).
- 스크린샷 · 리포트의 이름 · id 원문: 추가 줄에 0건.
- 화면 문구: 새로 쓴 것 = 「링크 복사하기」 「링크 열기」 「6개월 경과」 「연결」 「미연결」 + 기존 SPEC · cc 문구뿐. 「{n}개월 경과」는 OQ-D49 의 물음으로만 나온다(채택 아님).

## lint

`python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning. products/day 줄 0건(ERROR · WARN 모두). 다른 제품 경고(selly frontmatter 등)는 무관.

---

## OQ 분류 표 (고침 8 · 개정 ⑯ 새 OQ 11개 + W2)

| OQ | 정말 열렸나 | 분류 | 기본값 제안(코디가 닫을 것) | 구현 막음 |
|---|---|---|---|---|
| OQ-R41 R64 와 길이 비례 · 동시 6장 이상 · `lines` 남나 | 열림(research Q2 「추천 없음」 · 결정 없음) | **사용자에게** | 물을 때 추천: (a1) 상한 풀고 열 폭 늘림 · `lines` 늘 1 — 길이 비례 top 계산(Rule 15)과 맞는 건 (a1)뿐 | **막음**(열 폭 식 · `rows` · Rule 15 top) |
| OQ-R42 짧은 카드 글자 · 최소 높이 | 열림 | 코디 기본값 | SPEC 기본값 그대로(길이 그대로 · 넘치는 글자 잘림 · 모달 디자인 때 시안) | 아니오 |
| OQ-R43 같은 시작 순서 · 동행 이웃 자리 · 띠 모양 | 열림 | 코디 기본값 | SPEC 기본값 그대로(R73 순서 · 이어진 빈 자리 첫 묶음 · 멤버 다 감싸는 상자) | 아니오 |
| OQ-R44 앱 예약현황 `lane`·`rows` | 열림 | **사용자에게** | 물을 때 후보: 앱 JSON 은 같은 값 · 앱 화면은 안 고침(시작 행 안 빈 자리 생김 「알고 감」) / 앱 JSON 에 옛 배치 따로 | **막음**(서버 API 모양) |
| OQ-D43 진행 칸 글자 · 복사 알림 | 열림(글자 = 사용자 몫) | **사용자에게**(글자) | 그 전까지 지금 글자 · 복사 알림 없음 | 아니오 |
| OQ-D44 링크 요청과 「열린 요청 취소」 규칙 | 열림 | 코디 기본값(사용자 확인 권장) | **기기 없는 열린 문진 요청이 있으면 「링크 복사하기」 · 「링크 열기」는 새로 만들지 않고 그 링크를 다시 씀**(토큰은 nonce 로 다시 만들 수 있음 — research §3.3). 기기 줄을 누르면 지금 규칙대로 취소 → 새 요청 | 아니오(규칙 2 문장만 바뀜) |
| OQ-D45 SSE 다시 그리기가 팝오버를 닫나 | 열림(be-f6 §4 「코드상 추정」) | 코디 기본값 | SPEC 기본값(닫지 않게 · 방법 = 구현) · e2e 확인 항목 | 아니오 |
| OQ-D46 ① 양식 보기 id ↔ `answerId` · 양식 내부 경로 | 열림(be-kos 「미확인」 · 결정 「근거 없으면 OQ」) | 코디 기본값 | **(b)** `inputType`·`subText` 비우고 `health_lines` 의 INPUT_BOX 판정을 `memo` 유무로. (a) 내부 양식 경로가 HAR 로 나오면 그때 바꿈. 공개 호출은 안 씀 | 답 맞춤 일부만(읽기 · 저장은 안 막음) |
| OQ-D46 ② `questionnaireId` = 읽기 `id`? | 열림(KOS 쓰기 필요) | 코디 기본값 | 로컬 e2e(데모)에서 고객 웹 1회 제출로 확인 · 그 전엔 SPEC 대로 저장 | 아니오(중복 가르기 정확도) |
| OQ-D46 ③ 여러 번 낸 고객 | 열림 | 코디 기본값 | 「받은 한 건 = 마지막」으로 읽고 알고 감 | 아니오 |
| OQ-D46 ④ 400 밖 실패 · 사라진 제출 | 열림(결정은 400 만) | 코디 기본값 | SPEC 기본값(그 고객만 건너뜀 · 회차 정상 · 행 안 지움) | 아니오 |
| OQ-D47 앱 「6개월 경과」 | 열림(앱 화면 범위 밖) | 코디 기본값 + W4 | 앱 화면은 다음 앱 작업. **JSON 칸은 지금 정함**(W4 — 예 `questionnaire.expired`) | JSON 칸 이름만(W4) |
| OQ-D48 다른 날 낸 문진 글자 | 열림(글자) | **사용자에게**(글자) | 그 전까지 지금 글자 | 아니오 |
| OQ-D49 세는 법 · 글자 고정 · 건강정보 보임 | 열림 | 코디 기본값 | SPEC 기본값(KST 날짜 + n 개월 달력 · 「6개월 경과」 고정 · 건강정보 보임) | 아니오 |
| (W2) 문진 읽기 태스크 자리 | SPEC 에 OQ 로도 없음 | 코디 기본값 | 일정 회차 뒤 별도 태스크(구매 회차 꼴) | 아니오(닫으면 바로 됨) |

결정 · 리포트에 이미 답이 있는데 OQ 로 남긴 것: **없음.**
구현을 막는 OQ: **OQ-R41 · OQ-R44**(사용자 확인). W4 는 JSON 칸 이름 하나만 정하면 풀린다.
