# [researcher] 추가 지시 — 예약 상세 모달 · KOS 사전 설문(문진)으로 넣을 수 있는 정보 (read-only 조사)

앞 판 `reservation-read-report.md` 의 이어지는 판이다. 역할 · 금지 · 완료 보고는 `reservation-read-research-instructions.md` §5 · §7 과 같다(보고 대상 = 예약 코디 `term_fa2737b7-e69a-40e1-9fac-019199b9dad3`).

## 1. 무엇을 하나

시안의 **예약 상세 모달**(design-analysis-report §3.4 — 고객 기본 정보 · 신분 확인 · 유입 채널 · 예약 메모 · 건강 정보 · 주의사항)을 KOS 로 채울 수 있는지 본다.

사용자 구상(2026-10-26): **ccc 가 자체 질문지를 갖고, 고객 답을 KOS 사전 질문(문진)에 제출**하는 구조. 그래서 핵심 질문은 **「KOS 문진 제출로 어떤 정보를 넣을 수 있나 · 넣으면 KOS 어디에 보이나」**다.

## 2. 읽을 것 (gitignore · 고객 정보 · 토큰 포함 — 값 옮기지 마라)

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/설문전송.har` — 직원이 KOS 에서 설문 링크를 보내는 쪽(12항목). 코디가 본 KOS 경로: `issue-questionnaire-link`(내부 · 쓰기) · `get-roles` · `get-schedule-summaries` · `get-reservation-group` · `procedure-menu/visitors/queries/get-visitors` · `v1/visitor/queries/get-visitor` · `get-rooms`
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/설문내용.har` — 고객이 설문을 제출한 쪽(2항목). `visitor-api.kos-solution.com/…/submit-questionnaire/legacy`(내부 · 쓰기)
  - 파일 이름과 내용이 엇갈려 보인다(「전송」= 링크 발급, 「내용」= 제출). 직접 확인하고 리포트에 적어라
  - **위 목록으로 끝내지 말고 두 HAR 의 요청을 전부 세어** 인벤토리를 만든다
- 고객용 설문 링크(토큰 포함 · 레포에 옮기지 마라): `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile------poc/0f9e7e83-ce9e-4288-8801-9e1937151012/scratchpad/questionnaire-link.txt` — 페이지와 그 페이지가 부르는 **조회**만 봐도 된다(제출 버튼 금지)
- 앞 판: `orchestration/work/overall-board/reservation-read-report.md` §3.1 13 · 14 · 15 · 18 · 19행 · Q-10 · Q-12 · Q-19
- 공개 API 스펙: `getVisitorQuestionnaire` · `submitVisitorQuestionnaire` · `getQuestionnaireSubmit` · `getVisitor` · `registerVisitorImages`

## 3. 할 일

1. **HAR 인벤토리**: 두 파일의 요청 전부 — 메서드 · 경로(`{tenantId}` 등으로) · 요청 본문 키 · 응답 모양 · 용도.
2. **설문 링크 발급**: `issue-questionnaire-link` 의 요청 · 응답 · 링크 모양(토큰 claim 의 **키 이름**만 — `sub · tid · vid · scope · exp` 등, 값 금지) · 유효 기간. 시안의 「QR로 고객 입력 요청」 · 「링크 복사」 · 「메신저 전송」 · 「10분 유효」와 비교. 공개 API 짝이 있나
3. **제출 본문 해부**: `submit-questionnaire/legacy` 의 본문 구조(페이지 · 질문 · 답 형식 · 선택지 id · 자유 입력 · 주소 등). 공개 `submitVisitorQuestionnaire` 본문과 차이. 내부 · 공개 중 무엇으로 ccc 가 제출할 수 있나
4. **제출 뒤 KOS 에 무엇이 남나 — 데모 조회로 확인**: 사용자가 데모 고객 1명에게 실제로 제출했다(HAR). 그 고객으로 `getQuestionnaireSubmit` · `getVisitor` · `getScheduleDetail` 을 **조회**해서 답이 어디에 어떤 모양으로 오는지, 제출이 **고객 정보 필드(이름 · 생년월일 · 연락처 · 국적 · 언어 등)를 갱신하는지** 확인. 고객 id 는 HAR 에서 찾되 리포트에 적지 마라
5. **모달 필드 대조표**: §3.4 의 필드마다 `문진 제출로 넣음`(질문 · 답 형식) / `고객 정보 API 로 넣음`(공개 · 내부 — 쓰기 작업 이름만, 호출 금지) / `KOS 에 넣을 곳 없음`. 특히 여권번호/주민번호 · 신분 확인 · 이메일 · 주소(자국) · SNS · 건강 7항목 · 주의사항
6. 「정할 것」: 결정하지 마라. 앞 판 Q 번호와 이어지면 표시

## 4. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-questionnaire-report.md` — 리포트 1개

## 5. 하지 말 것 (앞 판 §5 에 더해)

- **KOS 쓰기 0건** — 링크 발급 · 설문 제출 · 고객 수정 모두 호출 금지. 쓰기는 HAR 에 찍힌 것만 해석한다
- 리포트에 테넌트 · 고객 · 일정 id, 토큰, 링크, 이름 · 연락처 · 여권번호 · 주소 값 금지
