# [researcher] 추가 지시 — 예약 등록 모달 · KOS 예약 생성(기존 고객 · 신규 고객) (read-only 조사)

앞 판 `reservation-visitor-update-report.md` 에 이어지는 판이다. 역할 · 금지 · 완료 보고는 `reservation-read-research-instructions.md` §5 · §7 과 같다(보고 대상 = 예약 코디 `term_fa2737b7-e69a-40e1-9fac-019199b9dad3`).

## 1. 무엇을 하나

시안의 **예약 등록 모달**(design-analysis-report §3.5 「예약 등록 (`bk.na`)」 — 왼쪽 고객 검색 · 오른쪽 예약 초안 12필드 + 예약 메모)을 KOS 로 만들 수 있는지 본다.

사용자 결정(2026-10-26 · `_RESUME` §2):
- KOS 신규 고객 구분 규칙 = **이름 + (메인 연락처 · SNS ID · 이메일 · 여권번호 · 생년월일 중 하나 이상)** — KOS 화면 「고객을 구분할 수 있는 정보가 부족합니다」
- 차트번호 정본 = 지금은 KOS(나중에 ccc 자체 CRM 이 부여)
- 스케줄 표 칸 = KOS 예약 그룹 그대로 · 상태 = 2계층 · 고객 데이터 = 신분증 스캔 + 문진

## 2. 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/예약.har` (gitignore · 187항목). 사용자가 데모에서 예약을 **두 번** 만들었다(코디가 본 순서):
  - ① 기존 고객: `get-visitors` → `get-visitor` → … `get-reservation-time-slots` → **`schedule/reservation/v2/commands/reserve`**
  - ② 신규 고객: `find-duplicated-visitor` → **`v1/visitor/commands/create-visitor`** → `get-visitor` → … → **`schedule/reservation/v2/commands/reserve`**
  - 슬롯 · 규칙: `get-reservation-time-slots` · `get-occupied-resources-by-reservation-time-slot` · `reservation-rule/v1/queries/get-reservation-rule(-summaries)` · `get-default-reservation-policy` · `get-reservation-group`
  - **이 목록으로 끝내지 말고 KOS 요청(OPTIONS · js · svg 제외)을 전부 세어** 인벤토리를 만든다
- 앞 판들: `reservation-read-report.md`(§3.3 권역 = 예약 그룹 · Q-4 · Q-5 · Q-20) · `reservation-questionnaire-report.md`(§5 M17 · `reserveV2`) · `reservation-visitor-update-report.md`(§4 중복 확인 · `findDuplicatedVisitorId` · §2 고객 필드)
- 공개 스펙: `searchVisitors` · `reserveV2` · `reserveByVisitorIdV2` · `findDuplicatedVisitorId` · `getReservationSlotsByGroupsV2` 등 예약 · 슬롯 작업 전부

## 3. 할 일

1. **HAR 인벤토리**: KOS 요청 전부 — 메서드 · 경로 · 본문 키 · 응답 모양 · 화면 용도. 두 예약 흐름(기존 · 신규)을 순서대로 나눠 적는다.
2. **내부 `reserve` 해부**(두 건 비교): 본문 전체 — 예약 그룹 · 시각 · 고객 · 담당자 · 상담 필요 · 지정 의사 · 지정 상담사 · 희망 시술(옵션 · 상품 · 가격) · 유입 채널(카테고리 · 채널 · 상세) · 예약 메모 · 귀가 희망 시각 · 수면마취 등. 응답(일정 id 등 — 값 금지).
3. **내부 `create-visitor` 해부**: 본문 필드 · 필수 · 「고객 수가 유형」(KOS 화면 필수) · 구분 규칙(이름 + 다섯 중 하나)이 서버 오류로 오는지 화면 검사인지. 앞 판 `update-visitor-personal-information` 필드와 비교.
4. **공개 짝**: 기존 고객 = `reserveByVisitorIdV2` · 신규 = `reserveV2`(고객 생성 + 예약 한 번에) · 고객 검색 = `searchVisitors`(검색 조건: 이름 · 연락처 · 생년월일 · **차트번호**가 되나). 내부 본문과 필드 차이 · 공개로 시안 모달이 다 되나. **공개 조회는 데모에서 한 번씩 실제로 불러 확인**(`searchVisitors` 로 HAR 에 나온 고객을 이름 · 차트번호로 찾아 보기 등)
5. **슬롯 · 검증**: 예약 가능 시각을 KOS 가 어떻게 정하나(그룹 간격 · 정원 「3명」 · 운영 시간 · 휴무 · 점유). 정원 초과 · 휴무 · 겹침을 서버가 거르나(스펙 오류 코드). 시안의 「칸 [+]」 · 드래그 이동(Q-13)과 비교. 칸 머리 「N명 / 30분」의 정원 필드가 무엇인지(앞 판에서 못 찾음)
6. **모달 필드 대조표**: 시안 예약 초안 필드(예약일 · 시간 · 권역 · 유입 채널 · 이름(여권) · 한글 발음 · 생년월일 · 국적 · 성별 · 통역 · 원장 상담 · 희망 시술/예산 · 예약 메모) + 고객 검색 4칸 + 결과 표(차트번호 · 이름(발음) · 생년월일 · 국적) + 「이름이 같은 기존 고객」 경고 + [예약 등록] 켜짐 조건 → 필드마다 `공개`(작업 · 필드) / `내부`(HAR 필드) / `없음`. 특히 **통역 · 원장 상담 · 희망 시술/예산**이 KOS 예약의 무엇(「상담 필요」 체크 · 「당일 지정 의사」 · 「희망 시술」 · 문진 답)과 맞는지
7. 「정할 것」: 결정하지 마라. Q-50 부터

## 4. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-create-report.md` — 리포트 1개

## 5. 하지 말 것

- **KOS 쓰기 0건** — `reserve` · `create-visitor` · `reserveV2` 등 command 호출 금지. HAR 에 찍힌 것만 해석
- 리포트에 id · 토큰 · 이름 · 연락처 · 여권번호 등 값 금지(모양만)
