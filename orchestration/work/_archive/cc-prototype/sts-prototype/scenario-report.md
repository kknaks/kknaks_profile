# 목데이터 시나리오 — 10-09 실데이터 대본 → 시드 + 이벤트 (2026-10-13)

- 작성: cc-prototype `researcher` 워커. KOS 호출 0 · 커밋 0
- 만든 파일(gitignore 폴더): `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back/data/scenario/`
  - `seed.json` — 일정 8 · `staffIds` 14 · `ticketBundles` 1명(2묶음) · `pastSchedules` 1명(1건)
  - `events/<scheduleId>.json` 8개
- 형식: `orchestration/work/sts-prototype/scenario-format.md`(맨 아래 「추가 — staffIds」 포함) 그대로. 고치지 않음
- 원천: 캡처 `reference/2026-10-12-cc-prototype/2026-10-12T161224-5b4603da/raw/` 의 `getScheduleDetail`(대본 일정) · `getPurchaseItemStatistics`(결제 품목) · `getTicketBundlesQuery`(시술권 묶음 모양) · 직원 `kos-staff.json`
- 생성 스크립트는 스크래치에서 한 번 돌렸다(레포 · 데이터 폴더에 두지 않음). 새 id 는 고정 seed 난수(재실행하면 같은 id)

## 시나리오 표

예약 시각은 10-09 KST. 결제 = 대본 일정의 `getPurchaseItemStatistics` 품목 `cost.totalAmount` 합(대본의 승인 거래 합과 8건 모두 같음).

| # | 장면 | 예약(KST) | scheduleId(새) | 가짜 이름 | 대본 `scriptFrom` | 고른 이유 | 시술 | 결제 |
|---|---|---|---|---|---|---|---|---|
| S7 | 시술마다 원장이 다름 | 10:00 | `33218a5e-…` | [TW] LIU JIA HUI | `ff844488-d46c-4bdc-af6f-368577cf7ed3` | 10-09 에서 **원장 2명 이상인 유일한 일정**(임윤서 · 원다은 + 마취용) · 시술 9 · 동행 1 · 「12:30 전 퇴원」 메모 | 9 + 원장 상담 1 | 1,541,100 (9품목) |
| S1 | 대만 첫 방문 기본 | 10:30 | `735f15dd-…` | [TW] CHEN XIAO WEN | `cc0a494e-94c1-43b2-a9c4-60f5e5dc2c97` | TW · 시술 4(울쎄라 100 + 추가 100 · 소프웨이브 150 · 머미팩) · 상담/오더 메모가 양식대로 다 있음 | 4 + 1 | 1,677,500 (4) |
| S8 | 한국 고객(통역 없음) | 11:00 | `e64ef71d-…` | 김하늘 | `9ebbf0d4-5b86-4501-a44e-60cdf03adeac` | KR · 직원 소개 유입 · 「우원장님 지인 10% 할인/민현우」 예약 메모 · 동행 1 | 3 + 1 | 439,000 (2) |
| S2 | **재내원**(지난 상담 + 남은 시술권) | 11:30 | `03c2b54c-…` | [TW] WANG YI TING | `e708db7c-eb5f-4587-a523-9e3daa1c56e4` | 대본의 시술이 블랙필 · 포텐자 펌핑팁 · 쥬베룩 스킨 → 포텐자 · 쥬베룩을 「지난번에 산 회차권」으로 돌리기 좋음. 10-09 의 실제 재방문 1건은 취소 일정(데이터 없음)이라 못 씀 | 1 + 1 (+ 보유 시술권에서 데스크가 고를 2) | 108,900 (블랙필 1) |
| S3 | 홍콩 고객(광둥어 통역) | 13:00 | `1f97ba37-…` | [HK] CHAN MEI LING | `d9d13a62-73aa-4758-b10f-32c3b7bb22a2` | 10-09 의 **유일한 HK** · 써마지 900 · 리쥬란 · 시트팩 | 3 + 1 | 2,354,000 (3) |
| S5 | 수면 시술 고객 | 14:00 | `f37712ea-…` | [TW] LIN YA CHEN | `acd93276-bafd-426d-957d-ad8c6211b835` | 시술 9개 중 **리프팅(써마지 900 · 소프웨이브 50)** + 보톡스 4부위 · 리투오 · 아쿠아필. 「우원장님 지정 희망」 메모 | 9 + 1 | 3,166,790 (7) |
| S4 | 일본 고객 | 15:00 | `75fa2f78-…` | [JP] TANAKA YUKI | `c541efce-ee2a-47b8-ab3e-4d216a0a7c22` | 10-09 의 **유일한 JP** · 체험단(무료) · 물광주사 1 | 1 + 1 | 0 (1품목 0원) |
| S6 | 중간 귀가(상담만) | 15:30 | `fb8e28c4-…` | [TW] HUANG SHU FEN | `616c3279-093a-49dc-96b8-5266adc11144` | 시술 0 · 상담 메모에 「상담만 하심, 시술 안하신다고 함」 · 구매 0품목 | 0 + 1 | 0 (0) |

담당 상담사(대본 그대로): 민현우(S7 · S8 · S4) · 류하린(S1 · S3) · 오현우(S2 · S5 · S6).

## 각 시나리오에 들어간 것

**seed.json `schedules[]`**: 새 `id`(UUID) · `reservation`(`startDateTime` · `endDateTime`(+30분) · `status: RESERVED` · `reservationMemo`(대본, 이름만 치환) · `reservationGroupId` · `funnel`(대본)) · `visitor`(새 `id`(24자 hex) · 가짜 `name` · `isNew` · `nationality` · `gender` · `dateOfBirth`(대본) · `memo`) · `scenario` · `scriptFrom`.

**events/<scheduleId>.json**
- `consultationDone.consultation` — 대본 `consultations[0]` 의 `counselors` · `content.text`(이름 치환)
- `consultationDone.orderMemo` — 대본 `orderMemo`(이름 치환)
- `consultationDone.tasks` — 대본 `tasks[]` 를 **상담 직후 모양으로 되돌린 것**: `status` = `NOT_STARTED`, **`doctors` · `assignees` · `calledDoctors` = `[]`**(사후 값 금지), `room` = 빈 방(`id` · `zoneId` · `title` 빈 값), 시각 칸(`readyDateTimeUtc` 등) = `""`, `assigneeMemo` · `doctorMemo` = `""`, `paymentRequired` = PROCEDURE `true` · ETCETERA `false`, `procedureConfiguration.ticketConfiguration` = `{}`. `sequence` · `title` · `type` · `procedureConfiguration`(상품 옵션 · 진료 항목) · `etceteraConfiguration` · `anesthesiaType` · `memo` · `order` · `urgencyLevel` 은 대본 그대로
- `consultationDone.payment` — `totalAmount` + `items[]`(`productTitle` · `productOptionTitle` · `cost`, 대본 구매 품목)
- `paymentDone.ticketIdsBySequence` — PROCEDURE 순번마다 **새 UUID**(실제 시술권 id 아님)
- `taskDone.<sequence>.assigneeMemo` — 대본 작업의 담당자 메모(있는 것만. 예: S3 「어시 지민」 · 「시트7"」, S7 「어시 지민\n벨로 소프트」)

## synthetic 으로 만든 것(전부 S2)

| 위치 | 내용 | 표시 |
|---|---|---|
| `seed.schedules[S2].visitor.isNew` | `false`(대본은 첫 방문) | `visitor.synthetic: true` |
| `seed.pastSchedules[<S2 visitorId>]` | 2026-09-12 방문 1건 — 상담 오현우, 상담 메모 · 오더 메모(대본 양식으로 작성: 「포텐자CP팁+쥬스킨2CC 1회차」), `procedures` = 포텐자 펌핑팁 · 쥬베룩 스킨 2cc | `synthetic: true` |
| `seed.ticketBundles[<S2 visitorId>]` | ① `[오픈] 포텐자 펌핑팁 10회` — 10장 중 USED 3 · **AVAILABLE 7**, 장당 60,500 ② `[오픈] 쥬베룩 스킨 2cc 3회` — 3장 중 USED 1 · **AVAILABLE 2**, 장당 217,800. 모양은 `getTicketBundlesQuery.data[]`(`purchaseId` · `purchaseItemId` · `optionConfiguration` · `ticketSets[].procedure/unit/tickets[]` · `price` · `title` · `visitorId`). `optionId` · 시술 id · 단위는 대본 작업의 실제 값, 묶음 이름 · 장수 · 상태 · id 는 만든 값 | 묶음마다 `synthetic: true` |
| `events[S2].consultationDone.tasks` · `payment` | 대본 작업 4개 중 **원장 상담 · 블랙필만** 남김(포텐자 · 쥬베룩은 보유 시술권에서 데스크가 접수 때 고르는 장면). 결제도 블랙필 1품목 108,900 | `payment.synthetic: true` |

그 밖의 7개 시나리오에는 만든 값이 없다(이름 · id 치환만).

## 오늘 근무 직원 `staffIds`(14명, 모두 `kos-staff.json` 활성 직원 · 10-09 일정에 나온 사람)

| 직군 | 인원 | 이름 |
|---|---|---|
| 의사 | 2 | 권태윤(ADMIN · DOCTOR) · 임윤서(DOCTOR) |
| 코디 | 3 | 곽태린 · 심준서 · 주태윤(CALL_COUNSELOR · COUNSELOR · COORDINATOR) |
| 간호사 | 4 | 강도윤 · 류하람 · 유채원 · 서가온(NURSE) |
| 피부관리사 | 2 | 송지호 · 서채원(SKINCARE) |
| 상담사 | 3 | 오현우 · 민현우 · 류하린(COUNSELOR) — 이벤트 상담사 전원 |

「마취용」 제외. 의사 두 명은 S5 「우원장님 지정 희망」 · S8 「우원장님 지인」 메모에 맞춰 권태윤을 넣고, S7 대본 원장인 임윤서를 넣었다. S7 대본의 다른 원장 원다은 · S8 대본 이지우은 목록 밖이다 → 시연에서 데스크가 권태윤 · 임윤서로 나눠 배정한다.

## 시연 순서 제안(예약 시각 = 이 순서)

1. **S7 10:00** — 시술 많고 「12:30 전 퇴원」 → 원장 두 명에게 나눠 배정 · 방 패널 고객 중심 보기
2. **S1 10:30** — 기본 흐름 전체(접수 → 시술실 → 상담 → [결제 완료] → 시술 3+1 → 귀가)
3. **S8 11:00** — 통역 없는 한국 고객 대비
4. **S2 11:30** — 재내원: 지난 상담 · 보유 시술권(포텐자 7/10 · 쥬베룩 2/3)에서 오늘 시술 고르기 + 상담에서 블랙필 추가
5. **S3 13:00** — 홍콩 · 광둥어 통역 모달
6. **S5 14:00** — 수면시술실 이동(원래 방 점유 유지)
7. **S4 15:00** — 일본어 통역 · 0원 결제
8. **S6 15:30** — 상담만 하고 귀가 → 남은 단계 「진행 안 함」

## 주의 · 데이터에 없는 것

- **S5 수면:** 수면 여부는 데이터에 없다(`anesthesiaType` 은 `ANESTHESIA_TYPE_UNSPECIFIED`). 시술이 많고 리프팅이 있어 골랐을 뿐이다. 수면시술실 이동은 시연에서 데스크가 정한다
- **S3 광둥어:** 대본 예약 메모는 「통역 필요(중국어)」다(실값 그대로 둠). 광둥어는 장면 설정일 뿐 데이터에는 없다
- **S7 원장:** 대본에서는 슈링크 3개 작업의 원장이 「마취용」 계정이었다. 이벤트는 doctors 를 비워 두므로 영향 없음
- **S2 순번:** 이벤트 작업 순번은 대본 그대로(원장 상담 1 · 블랙필 2)다. 데스크가 접수 때 보유 시술권에서 넣는 단계와 순번이 겹칠 수 있다 — 관제 DB 순번은 back 이 정할 일
- **S4 · S6 결제 0:** S4 는 품목 1(0원), S6 는 품목 0 · `ticketIdsBySequence` 빈 객체
- **S6 오더 메모:** 빈 문자열(대본 그대로). 상담 메모 아래쪽 오더지 양식도 번호만 있고 비어 있다
- 대본 `orderMemo` 와 상담 메모 사본이 다른 경우도 그대로 뒀다(S7: 오더 메모 「아이리쥬란1cc」 · 상담 메모 「2cc」)

## 검증(`python3` 실행 결과)

- JSON 파싱: `seed.json` + `events/*.json` 8개 모두 정상
- 형식: seed 최상위 `date` · `schedules` · `ticketBundles` · `pastSchedules` · `staffIds` 있음. 일정마다 `id` · `reservation`(`startDateTime` · `status` · `reservationMemo` · `reservationGroupId` · `funnel`) · `visitor`(`id` · `name` · `isNew` · `nationality` · `gender` · `dateOfBirth` · `memo`) · `scenario` · `scriptFrom` 있음. 이벤트마다 `consultationDone`(`consultation` · `orderMemo` · `tasks` · `payment`) · `paymentDone.ticketIdsBySequence` · `taskDone` 있음
- 규칙: 모든 이벤트 작업 `doctors` · `assignees` = `[]` · `status` = `NOT_STARTED`, PROCEDURE 는 `paymentRequired` true · `ticketConfiguration` `{}`. `ticketIdsBySequence` 의 키 = PROCEDURE 순번과 정확히 같음. 이벤트 상담사 3명 모두 `staffIds` 안
- 시나리오 8개: S1~S8 모두 있음, 일정 8 = 이벤트 파일 8
- **실제 고객 이름 0건:** 캡처 177일정의 `visitor.name` · `phoneticName` · `consultations[].visitor.name` · 메모 「이름 :」 값까지 331개와 대조 → 통째로 일치 0. 단 하나 걸린 「이이」는 S7 상담 메모의 「아이이슈링크」 오타 속 글자다(이름 아님). 이름 조각(4자 이상 로마자 · 3자 이상 한글) 일치는 모두 가짜 이름 안의 흔한 성(CHEN · WANG 등)이었고, 가짜 이름을 빼면 0이다. 메모 속 「이름 :」 줄 6개는 모두 가짜 이름(천샤오원 · 왕이팅 ×2 · 찬메이링 · 린야천 · 황수펀)이고, 동행인 3명도 가짜(WU TING · LIN HAO · 이수진)
- **실제 id 0건:** 캡처의 scheduleId · visitorId · 상담 id 전부와 대조 → `scriptFrom` 칸 말고는 0. 시술권 id 도 모두 새로 만들었다
- 전화번호: 출력에 전화 칸 없음 · 메모 속 전화번호 꼴 0(숫자 패턴은 UUID 일부뿐)
- 가짜 이름이 실제 고객 · 직원 이름과 겹치는 것 0
