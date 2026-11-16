# [researcher] 추가 지시 — 기존 고객 정보 수정(여권번호 · 국적 등) KOS 경로 (read-only 조사)

앞 판 `reservation-questionnaire-report.md` 에 이어지는 판이다. 역할 · 금지 · 완료 보고는 `reservation-read-research-instructions.md` §5 · §7 과 같다(보고 대상 = 예약 코디 `term_fa2737b7-e69a-40e1-9fac-019199b9dad3`).

## 1. 배경 · 무엇을 하나

사용자 결정(2026-10-26): **고객 데이터 = 신분증 스캔 + 문진.** 국적 · 여권번호 · 신분증은 **데스크가 앱으로 스캐너를 열어 스캔한 값**이다. 앞 판에서 새 고객은 `reserveV2` 로 넣을 수 있지만 **기존 고객의 여권번호 · 국적을 고치는 공개 API 는 없었다**(Q-29).

사용자가 KOS 고객 정보 화면에서 **데모 고객의 정보를 고쳐 저장한 HAR** 을 떴다. 스캔 값(이름 여권 영문 · 여권번호 · 여권 만료일 · 국적 · 생년월일 · 성별 등)을 기존 고객에 넣는 길을 찾는다.

## 2. 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/고객정보 수정.har` (gitignore · 65항목). 코디가 본 핵심: `visitor/v1/queries/find-duplicated-visitor` → **`visitor/v2/commands/update-visitor-personal-information`**(내부 · 쓰기) → `visitor/v2/queries/get-visitor`. 그 밖에 `get-codes` 여러 번 · `procedure-menu/target-countries/v1/queries/get-target-countries` · `visitor/v1/queries/get-custom-attribute-definitions` · `security/v2/queries/check-message-permission` 등. **이 목록으로 끝내지 말고 KOS 요청(OPTIONS · js · svg 제외)을 전부 세어** 인벤토리를 만든다
- 앞 판: `reservation-questionnaire-report.md` §5 M1 · M4 · M6 · M7 · M15 · M16 · Q-29 · Q-35 / `reservation-read-report.md` §3.1 6 · 9 · 12 · 13행
- 공개 스펙: 고객 쓰기 작업 전부(`reserveV2` · `registerVisitorImages` 외에 고객 수정 성격 작업이 정말 없는지 다시 grep)

## 3. 할 일

1. **HAR 인벤토리**: KOS 요청 전부 — 메서드 · 경로 · 본문 키 · 응답 모양 · 화면 용도.
2. **`update-visitor-personal-information` 해부**: 본문 전체 구조(필드마다 이름 · 형식 · 필수인지 · 값 예시는 모양만). 특히 `passportNumber` · `passportExpiryDate` · `passportSurname/GivenNames` · `nationality` · `dateOfBirth` · `gender` · `registrationNumber` · `phoneticName` · `language` · `email` · `snsInfo` · `memo`(주의사항 후보, Q-37) 가 있나. **부분 수정인지 통째로 덮어쓰기인지**(본문에 안 보낸 필드가 지워지나 — 수정 전후 `get-visitor` 응답 비교로 판단)
3. **수정 전후 비교**: HAR 의 앞 `get-visitor` ↔ 뒤 `get-visitor` 에서 무엇이 바뀌었나. 그리고 지금 데모에서 같은 고객을 공개 `getVisitor` · 내부 `get-visitor` 로 **조회**해서 바뀐 값이 공개 쪽에도 보이는지
4. **`find-duplicated-visitor`**: 무엇으로 중복을 찾나(여권번호? 이름+생년월일?) · 응답 모양. 스캔 값으로 기존 고객을 찾는 데 쓸 수 있나(시안 「예약 등록」의 고객 검색 · 「이름이 같은 기존 고객」 경고와 비교)
5. **코드 표**: `get-codes` 의 종류(국적 · 언어 · 고객 분류 등)와 `get-target-countries` — 국적 값이 ISO 코드인지 KOS 코드인지
6. **대조표**: 스캔 값 필드마다 `공개`(작업) / `내부`(`update-visitor-personal-information` 필드) / `없음`. 신분 확인 **상태**를 둘 칸이 이 API · 고객 커스텀 속성(`get-custom-attribute-definitions`)에 있나도 본다
7. 「정할 것」: 결정하지 마라. 앞 판 Q 번호에 이어 Q-39 부터

## 4. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-visitor-update-report.md` — 리포트 1개

## 5. 하지 말 것

- **KOS 쓰기 0건** — `update-visitor-personal-information` 등 command 호출 금지. HAR 에 찍힌 것만 해석
- 리포트에 id · 토큰 · 이름 · 연락처 · 여권번호 · 주소 등 값 금지(모양만)
