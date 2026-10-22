# KOS 데모 지점 — 접속 정보 · 시술 관련 API 참고

- 조사일: **2026-10-20** · 조사자: cc-prototype `researcher` 워커
- 스펙: `https://developers.kos-solution.com/openapi.yaml` 를 2026-10-20 에 받음. `info.version` **1.0.1** · 작업 **75개**(조회 50 · 쓰기 25). 코디가 받아 둔 사본 `/private/tmp/claude-501/kos-openapi.yaml` 과 바이트 단위로 같았다
- 데모 호출: **조회(`/queries/`)만**, 데모 키로 작업당 한두 번. 쓰기(`/commands/`) 호출 0건, 운영 키 사용 0건
- 이 문서는 public 레포에 있다. 키 · 토큰 · 사람 이름 · 연락처 · 메모 원문은 적지 않았다. 응답은 **모양**(필드 이름 · 타입 · 건수)과 enum 값만 적는다
- 표기: **확인** = 이번에 실제로 불러서 본 것, **스펙** = openapi.yaml 에 적힌 것, **추정** = 해석

---

## 1. 접속 정보

### 1.1 메인 참고처는 ax-clinic-project(private)

키 값과 사용법은 거기 있다. 여기로 옮기지 않는다.

| 무엇 | 경로 |
|---|---|
| 키 값 | `/Users/kknaks/git/ax-clinic-project/scripts/.env` |
| 사용법(호스트 · 인증 · 오류 · 작업 목록) | `/Users/kknaks/git/ax-clinic-project/para/resources/technology/2026-09-18-kos-developers-api-guide.md` |
| 호출 코드(.env 읽기 · 토큰 교환 · 조회 전용 가드) | `/Users/kknaks/git/ax-clinic-project/scripts/kos_collect.py` |

인증 흐름 · 헤더 · 오류 코드는 가이드 **§3 「OpenAPI 사용방법」**에 있다. 작업 목록은 **§4 「OpenAPI 전체 목록」**에 있다. 여기서는 다시 쓰지 않는다. 공식 문서는 [인증](https://developers.kos-solution.com/docs/openapi/authorization)과 [OpenAPI 소개](https://developers.kos-solution.com/docs/openapi)다.

### 1.2 이 PoC 에만 해당하는 것

| 항목 | 값 | 근거 |
|---|---|---|
| 쓸 키 | 위 `.env` 의 **`KOS_API_tenent_dev`**. 이름만 적는다. 값은 파일에서 읽는다 | — |
| **쓰지 말 키** | 같은 파일의 **`KOS_API_tenent`**. 실제 운영 명동점 키다. **절대 쓰지 않는다** | 브리프 · 코디 확인(2026-10-20) |
| 호스트 | **`https://open-api.kos-solution.com`**(운영 호스트). 키 이름에 `_dev` 가 붙어 있어도 dev 서버 키가 아니다. 운영 호스트 안에 따로 있는 **데모 테넌트**다 | **확인**: 아래 두 줄 |
| ↳ `.com` 에서 토큰 교환 | `POST /open/authorization/commands/exchange-token` `{"key": …}` → **200**. 응답 키는 `token` 하나 | 확인 2026-10-20 |
| ↳ `.dev` 에서 토큰 교환(1회) | **400**. 응답 키는 `status · message · className · properties · errorProperties`. 코디가 본 `apiKey NotFound` 와 같은 거절이다(이번 응답에서 `message` 는 비어 있었다) | 확인 2026-10-20 |
| 이후 인증 | `Authorization: <token>`. `Bearer` 를 붙이지 않는다. 작업은 전부 `POST` 다. 가이드 §3 과 같다 | 확인(모든 조회 호출에 이 방식을 썼다) |
| 데모 식별 ① 구역 | `getZones` 결과 **2개**: `4층`(id `6a793cd9bb2d7899923714ed`, `isDefault: true`) · `미사용`(`isDefault: false`) | 확인 |
| 데모 식별 ② 직원 | `getAccounts` 결과 **77건**(`activate: true` 로 거르면 53건). `name` 필드 값이 `KOS-DEMO` 인 계정이 **있다**. 이 계정은 운영에 없다(코디 확인) | 확인 |

**스펙 변경(2026-09-18 가이드 스냅샷 대비)**: 작업이 73개에서 75개로 늘었다. 새로 생긴 작업은 **`getAccounts`**(직원 목록 조회)와 **`changeReservationMemo`**(예약 메모 변경) 둘이다. 없어진 작업은 없다. deprecated 표시가 바뀐 작업도 없다. 두 스펙 파일을 operationId 로 비교해서 확인했다. 가이드의 다른 내용(호스트 · 인증 · 오류)은 지금 스펙과 다른 점을 찾지 못했다.

**공식 문서 URL 규칙**(확인: 75개 전부 HTTP 200):
- 웹 문서: `https://developers.kos-solution.com/docs/openapi/<태그>#<operationId>`. 아래 표의 「문서」 링크가 이 형식이다
- Markdown: `https://developers.kos-solution.com/docs/openapi/<operationId 를 kebab 으로>.md`. `V2` 는 `v-2` 로 바뀐다(예: `reserve-v-2.md`)

---

## 2. 시술 관련 작업 전수표

### 2.1 어떻게 셌나

- 대상: 스펙 75개 작업 전부
- grep 단어(대소문자 무시, `operationId` + 경로 + `summary` 에서 찾음): `procedure` `task` `ticket` `schedule` `flow` `reservation` `purchase` `transaction` `product` `machine` `medicine` `medical` `zone` `account` `visitor` `room` `assignee` `doctor` `시술` `수납` `결제` `구역` `직원` `내원객`
- 결과: **72개**가 걸렸다(조회 49 · 쓰기 23). 아래 표가 그 72개 전부다
- 안 걸린 3개: `exchangeToken`(인증, §1), `generateUploadingImageUrl`(이미지 업로드 URL), `getPrepaidCardChargingEventStatistics`(선불카드 내역 통계). 세 작업의 개별 문서(.md)에도 위 단어가 없었다. 마지막 작업은 선불카드를 수납 수단으로 볼 수도 있어서 한 번 불러 봤다: ✅ 200 · `data[13]` · `totalCount`
- `room`(방)이 경로 · 이름에 들어간 작업은 **0개**다. 방은 일정 `tasks[].room` 으로만 나온다(§3.3)
- 「데모 호출」 칸: ✅ = 이번에 실제로 불렀고 200. ❌ = 불렀는데 실패. 미확인 = 사유를 함께 적었다. 쓰기는 부르지 않았다

#### A. 일정 · 시술 작업(tasks) — 8개

| operationId | 경로 | 종류 | 용도(스펙 summary) | 요청 필수 | 공식 문서 | deprecated | 데모 호출(2026-10-20) |
|---|---|---|---|---|---|---|---|
| `changeFlowStep` | `/schedule/open/v1/commands/change-flow-step` | 쓰기 | 내원흐름단계 변경 | `scheduleId`, `step` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#changeFlowStep) |  | — 쓰기(호출 안 함) |
| `changeReservationMemo` | `/schedule/open/v1/commands/change-reservation-memo` | 쓰기 | 예약 메모 변경 | `scheduleId`, `memo` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#changeReservationMemo) |  | — 쓰기(호출 안 함) |
| `updateScheduleConsultationInfo` | `/schedule/open/v1/commands/update-schedule-consultation-info` | 쓰기 | 스케줄 상담 정보 수정 | `scheduleId` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#updateScheduleConsultationInfo) |  | — 쓰기(호출 안 함) |
| `findScheduleByPurchaseId` | `/schedule/open/v1/queries/find-schedule-by-purchase-id` | 조회 | 수납 ID로 스케줄 조회 | `purchaseId` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#findScheduleByPurchaseId) |  | ✅ 200 · `data{…}` 1건 |
| `getScheduleDetail` | `/schedule/open/v1/queries/get-schedule-detail` | 조회 | 스케줄 상세 조회 | `scheduleId` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getScheduleDetail) |  | ✅ 200 · `data{…}` 1건 |
| `getSchedulesByFlowStep` | `/schedule/open/v1/queries/get-schedules-by-flow-step` | 조회 | 내원 단계와 예약 시작 일시 범위로 스케줄 조회 | `flowStep`, `reservationStartDateTimeUtcFrom`, `reservationStartDateTimeUtcTo` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getSchedulesByFlowStep) |  | ✅ 200 · 단계별 `data[]` — 표 §3.2 |
| `getSchedulesByVisitor` | `/schedule/open/v1/queries/get-schedules-by-visitor` | 조회 | 내원객의 스케줄 목록 조회 | `visitorId` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getSchedulesByVisitor) |  | ✅ 200 · `data[1]` |
| `getSchedulesSummarizedByTask` | `/schedule/open/v1/queries/get-schedules-summarized-by-tasks` | 조회 | 내원객 시술 내역 조회 | `visitorId` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getSchedulesSummarizedByTask) |  | ✅ 200 · `data[1]` |

#### B. 수납 · 시술권 — 3개

| operationId | 경로 | 종류 | 용도(스펙 summary) | 요청 필수 | 공식 문서 | deprecated | 데모 호출(2026-10-20) |
|---|---|---|---|---|---|---|---|
| `getPurchaseSummaries` | `/purchase/open/v1/queries/get-purchase-summaries` | 조회 | 수납 목록 조회 | `purchaseIds` | [문서](https://developers.kos-solution.com/docs/openapi/purchase#getPurchaseSummaries) |  | ✅ 200 · `data[7]`(요청 id 21개 중) |
| `getPurchaseSummariesByVisitor` | `/purchase/open/v1/queries/get-purchase-summaries-by-visitor-id` | 조회 | 내원객 수납 목록 조회 | `visitorId` | [문서](https://developers.kos-solution.com/docs/openapi/purchase#getPurchaseSummariesByVisitor) |  | ✅ 200 · `data[1]` |
| `getTicketBundlesQuery` | `/ticket/open/v1/queries/get-ticket-bundles` | 조회 | 내원객의 사용 가능한 시술권 묶음 목록 조회 | `visitorId` | [문서](https://developers.kos-solution.com/docs/openapi/ticket#getTicketBundlesQuery) |  | ✅ 200 · 확인 — 9명 중 2명만 `data[]`(묶음 3 · 1), 나머지 7명은 결과 없음(본문을 확인한 1건은 `{}` — `data` 키 없음) |

#### C. 선불카드(수납 수단) — 3개

| operationId | 경로 | 종류 | 용도(스펙 summary) | 요청 필수 | 공식 문서 | deprecated | 데모 호출(2026-10-20) |
|---|---|---|---|---|---|---|---|
| `getPrepaidCardChargingEvents` | `/purchase/open/prepaid-card/v1/queries/get-prepaid-card-charging-events` | 조회 | 선불카드 이벤트 조회 | `id` | [문서](https://developers.kos-solution.com/docs/openapi/prepaid-card#getPrepaidCardChargingEvents) |  | ✅ 200 · `data[3]` |
| `getPrepaidCardSummaries` | `/purchase/open/prepaid-card/v1/queries/get-prepaid-card-summaries` | 조회 | 선불카드 목록 조회 | `visitorId` | [문서](https://developers.kos-solution.com/docs/openapi/prepaid-card#getPrepaidCardSummaries) |  | ✅ 200 · `data[0]` |
| `getVisitorPrepaidCardBalance` | `/purchase/open/prepaid-card/v1/queries/get-visitor-prepaid-card-balance` | 조회 | 내원객 선불카드 합산 잔액 조회 | `visitorId` | [문서](https://developers.kos-solution.com/docs/openapi/prepaid-card#getVisitorPrepaidCardBalance) |  | ✅ 200 · `data{…}` 1건 |

#### D. 통계 — 6개

| operationId | 경로 | 종류 | 용도(스펙 summary) | 요청 필수 | 공식 문서 | deprecated | 데모 호출(2026-10-20) |
|---|---|---|---|---|---|---|---|
| `getProcedureTaskStatistics` | `/statistics/open/v1/queries/get-procedure-task-statistics` | 조회 | 시술 태스크 통계 조회 | `completedDateTimeUtcFrom`, `completedDateTimeUtcTo`, `limit` | [문서](https://developers.kos-solution.com/docs/openapi/statistics#getProcedureTaskStatistics) |  | ✅ 200 · `data[6]` |
| `getPurchaseItemStatistics` | `/statistics/open/v1/queries/get-purchase-item-statistics` | 조회 | 구매 항목 통계 조회 | `createdDateTimeUtcFrom`, `createdDateTimeUtcTo`, `limit` | [문서](https://developers.kos-solution.com/docs/openapi/statistics#getPurchaseItemStatistics) |  | ✅ 200 · `data[6]` |
| `getScheduleStatistics` | `/statistics/open/v1/queries/get-schedule-statistics` | 조회 | 예약 통계 조회 | `limit` | [문서](https://developers.kos-solution.com/docs/openapi/statistics#getScheduleStatistics) |  | ✅ 200 · `data[29]` |
| `getTicketGroupStatistics` | `/statistics/open/v1/queries/get-ticket-group-statistics` | 조회 | 잔여시술권 통계 조회 | `limit` | [문서](https://developers.kos-solution.com/docs/openapi/statistics#getTicketGroupStatistics) |  | ❌ **404** `No static resource` — 스펙엔 있으나 서버에 경로 없음(미확인) |
| `getTransactionStatistics` | `/statistics/open/v1/queries/get-transaction-statistics` | 조회 | 결제 통계 조회 | `createdTimeUtcFrom`, `createdTimeUtcTo`, `limit` | [문서](https://developers.kos-solution.com/docs/openapi/statistics#getTransactionStatistics) |  | ✅ 200 · `data[9]` |
| `getVisitorStatistics` | `/statistics/open/v1/queries/get-visitor-statistics` | 조회 | 내원객 통계 조회 | `limit` | [문서](https://developers.kos-solution.com/docs/openapi/statistics#getVisitorStatistics) |  | ✅ 200 · `data[2]` |

#### E. 시술 메뉴(상품 · 시술 · 기기 · 약물 · 진료항목) — 16개

| operationId | 경로 | 종류 | 용도(스펙 summary) | 요청 필수 | 공식 문서 | deprecated | 데모 호출(2026-10-20) |
|---|---|---|---|---|---|---|---|
| `getCategories` | `/procedure-menu/open/categories/queries/get-categories` | 조회 | 상품 카테고리 목록 조회 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/product#getCategories) |  | ✅ 200 · `data[15]` |
| `getProduct` | `/procedure-menu/open/products/queries/get-product` | 조회 | 상품 조회 | `id` | [문서](https://developers.kos-solution.com/docs/openapi/product#getProduct) |  | ✅ 200 · 최상위 객체 |
| `getProducts` | `/procedure-menu/open/products/queries/get-products` | 조회 | 상품 목록 조회 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/product#getProducts) |  | ✅ 200 · `data[101]` |
| `searchProductOptionSummaries` | `/procedure-menu/open/products/queries/search-product-option-summaries` | 조회 | 상품 옵션 검색 | `searchText` | [문서](https://developers.kos-solution.com/docs/openapi/product#searchProductOptionSummaries) |  | ✅ 200 · `data[279]` |
| `getTargetCountries` | `/procedure-menu/open/target-countries/queries/get-target-countries` | 조회 | 타겟 국가 목록 조회 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/target-country#getTargetCountries) |  | ✅ 200 · `data[4]` |
| `getMachines` | `/procedure-menu/open/v1/machines/queries/get-machines` | 조회 | 기기 목록 조회 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/product#getMachines) |  | ✅ 200 · `data[302]` |
| `getMedicalServices` | `/procedure-menu/open/v1/medical-services/queries/get-medical-services` | 조회 | 진료항목 목록 조회 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/product#getMedicalServices) |  | ✅ 200 · `data[226]` |
| `getMedicines` | `/procedure-menu/open/v1/medicines/queries/get-medicines` | 조회 | 약물 목록 조회 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/product#getMedicines) |  | ✅ 200 · `data[349]` |
| `getProcedures` | `/procedure-menu/open/v1/procedures/queries/get-procedures` | 조회 | 시술 목록 조회 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/product#getProcedures) |  | ✅ 200 · `data[804]` |
| `getProductOptions` | `/procedure-menu/open/v1/product-options/queries/get-product-options` | 조회 | 상품 옵션 목록 조회 | `optionIds`, `includePromotions` | [문서](https://developers.kos-solution.com/docs/openapi/product#getProductOptions) |  | ✅ 200 · `data[5]` |
| `addProductOption` | `/procedure-menu/open/v1/products/commands/add-product-option` | 쓰기 | 상품 옵션 추가 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/product#addProductOption) |  | — 쓰기(호출 안 함) |
| `createProduct` | `/procedure-menu/open/v1/products/commands/create-product` | 쓰기 | 상품 생성 | `title`, `description`, `closed` | [문서](https://developers.kos-solution.com/docs/openapi/product#createProduct) |  | — 쓰기(호출 안 함) |
| `deleteProduct` | `/procedure-menu/open/v1/products/commands/delete-product` | 쓰기 | 상품 삭제 | `productId` | [문서](https://developers.kos-solution.com/docs/openapi/product#deleteProduct) |  | — 쓰기(호출 안 함) |
| `removeProductOption` | `/procedure-menu/open/v1/products/commands/remove-product-option` | 쓰기 | 상품 옵션 삭제 | `id`, `productId` | [문서](https://developers.kos-solution.com/docs/openapi/product#removeProductOption) |  | — 쓰기(호출 안 함) |
| `updateProductInformation` | `/procedure-menu/open/v1/products/commands/update-product-information` | 쓰기 | 상품 정보 수정 | `id`, `title`, `description`, `closed` | [문서](https://developers.kos-solution.com/docs/openapi/product#updateProductInformation) |  | — 쓰기(호출 안 함) |
| `updateProductOption` | `/procedure-menu/open/v1/products/commands/update-product-option` | 쓰기 | 상품 옵션 수정 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/product#updateProductOption) |  | — 쓰기(호출 안 함) |

#### F. 구역 — 2개

| operationId | 경로 | 종류 | 용도(스펙 summary) | 요청 필수 | 공식 문서 | deprecated | 데모 호출(2026-10-20) |
|---|---|---|---|---|---|---|---|
| `getZone` | `/schedule/open/zone/v1/queries/get-zone` | 조회 | 구역 조회 | `zoneId` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getZone) |  | ✅ 200 · `data{…}` 1건 |
| `getZones` | `/schedule/open/zone/v1/queries/get-zones` | 조회 | 구역 전체 조회 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getZones) |  | ✅ 200 · `data[2]` |

#### G. 직원 — 1개

| operationId | 경로 | 종류 | 용도(스펙 summary) | 요청 필수 | 공식 문서 | deprecated | 데모 호출(2026-10-20) |
|---|---|---|---|---|---|---|---|
| `getAccounts` | `/account/open/v1/queries/get-accounts` | 조회 | 직원 목록 조회 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/account#getAccounts) |  | ✅ 200 · `data[77]`(전체) · `activate:true` 53 |

#### H. 내원객 — 10개

| operationId | 경로 | 종류 | 용도(스펙 summary) | 요청 필수 | 공식 문서 | deprecated | 데모 호출(2026-10-20) |
|---|---|---|---|---|---|---|---|
| `registerVisitorImages` | `/image/open/v1/commands/register-visitor-images` | 쓰기 | 내원객 이미지 등록 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/image#registerVisitorImages) |  | — 쓰기(호출 안 함) |
| `disableAdvertisingAgreementToVisitors` | `/visitor/open/v1/commands/disable-advertising-agreement-to-visitors` | 쓰기 | 마케팅 수신 동의 해제 | `phoneNumber` | [문서](https://developers.kos-solution.com/docs/openapi/visitor#disableAdvertisingAgreementToVisitors) |  | — 쓰기(호출 안 함) |
| `submitVisitorQuestionnaire` | `/visitor/open/v1/commands/submit-visitor-questionnaire` | 쓰기 | 내원객 초진 설문지 제출 | `visitorId`, `name`, `dateOfBirth`, `gender` | [문서](https://developers.kos-solution.com/docs/openapi/visitor#submitVisitorQuestionnaire) |  | — 쓰기(호출 안 함) |
| `findDuplicatedVisitorId` | `/visitor/open/v1/queries/find-duplicated-visitor-id` | 조회 | 이미 등록된 내원객 ID 조회 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/visitor#findDuplicatedVisitorId) |  | 미확인 — 검색 입력이 사람 정보(이름 · 전화 · 생년월일 등)라 부르지 않음 |
| `findVisitor` | `/visitor/open/v1/queries/find-visitor` | 조회 | 내원객 검색 | `visitorName` | [문서](https://developers.kos-solution.com/docs/openapi/visitor#findVisitor) | **deprecated** | 미확인 — 입력이 이름(사람 정보) · deprecated |
| `getQuestionnaireAgreements` | `/visitor/open/v1/queries/get-questionnaire-agreements` | 조회 | 초진 설문지 동의항목 조회 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/visitor#getQuestionnaireAgreements) |  | ✅ 200 · `data[1]` |
| `getQuestionnaireSubmit` | `/visitor/open/v1/queries/get-questionnaire-submit` | 조회 | 제출된 초진 설문지 조회 | `visitorId` | [문서](https://developers.kos-solution.com/docs/openapi/visitor#getQuestionnaireSubmit) |  | ❌ 400 `InvalidRequestException` — 제출 건 없는 내원객으로 추정(미확인) |
| `getVisitor` | `/visitor/open/v1/queries/get-visitor` | 조회 | 내원객 정보 조회 | `id` | [문서](https://developers.kos-solution.com/docs/openapi/visitor#getVisitor) |  | ✅ 200 · `data{…}` 1건 |
| `getVisitorQuestionnaire` | `/visitor/open/v1/queries/get-visitor-questionnaire` | 조회 | 내원객 초진 설문지 조회 | `visitorId` | [문서](https://developers.kos-solution.com/docs/openapi/visitor#getVisitorQuestionnaire) |  | ✅ 200 · 최상위 객체 |
| `searchVisitors` | `/visitor/open/v1/queries/search-visitors` | 조회 | 내원객 정보 검색 | `offset`, `limit` | [문서](https://developers.kos-solution.com/docs/openapi/visitor#searchVisitors) |  | ✅ 200 · `data[1]` |

#### I. 예약 · 슬롯 · 예약 그룹 · 만족도 — 23개

| operationId | 경로 | 종류 | 용도(스펙 summary) | 요청 필수 | 공식 문서 | deprecated | 데모 호출(2026-10-20) |
|---|---|---|---|---|---|---|---|
| `cancelReservation` | `/schedule/open/v1/commands/cancel-reservation` | 쓰기 | 예약 취소 | `scheduleId`, `reason` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#cancelReservation) |  | — 쓰기(호출 안 함) |
| `createOccupiedTime` | `/schedule/open/v1/commands/create-occupied-time` | 쓰기 | 시간 점유 생성 | `startDateTimeUtc`, `endDateTimeUtc`, `zoneId`, `reservationGroupId` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#createOccupiedTime) |  | — 쓰기(호출 안 함) |
| `rescheduleByTimeSlot` | `/schedule/open/v1/commands/reschedule-by-time-slot` | 쓰기 | 예약 시간 슬롯 기반 예약 일시 변경 | `scheduleId`, `reservationDateTimeRange` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#rescheduleByTimeSlot) |  | — 쓰기(호출 안 함) |
| `reserveCommand` | `/schedule/open/v1/commands/reserve` | 쓰기 | 새로운 예약 생성 | `visitorName`, `reservationGroupId`, `zoneId`, `startDateTimeUtc`, `endDateTimeUtc` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#reserveCommand) | **deprecated** | — 쓰기(호출 안 함) |
| `reserveByTimeSlot` | `/schedule/open/v1/commands/reserve-by-time-slot` | 쓰기 | 예약 시간 슬롯 기반 새로운 예약 생성 | `reservationDateTimeRange`, `visitorName` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#reserveByTimeSlot) |  | — 쓰기(호출 안 함) |
| `reserveByTimeSlotWithVisitorId` | `/schedule/open/v1/commands/reserve-by-time-slot-with-visitor-id` | 쓰기 | 예약 시간 슬롯 기반 새로운 예약 생성 (내원객 ID 기반) | `reservationDateTimeRange`, `visitorId` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#reserveByTimeSlotWithVisitorId) |  | — 쓰기(호출 안 함) |
| `reserveByVisitorId` | `/schedule/open/v1/commands/reserve-by-visitor-id` | 쓰기 | 기존 내원객 예약 생성 | `visitorId`, `reservationGroupId`, `zoneId`, `startDateTimeUtc`, `endDateTimeUtc` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#reserveByVisitorId) | **deprecated** | — 쓰기(호출 안 함) |
| `updateReservation` | `/schedule/open/v1/commands/update-reservation` | 쓰기 | 예약 정보 수정 | `scheduleId`, `reservationGroupId`, `startDateTime`, `endDateTime`, `zoneId` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#updateReservation) | **deprecated** | — 쓰기(호출 안 함) |
| `getLinkedProducts` | `/schedule/open/v1/linked-products/queries/get-linked-products` | 조회 | 예약 그룹 연결 상품 조회 | `reservationGroupId` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getLinkedProducts) |  | ✅ 200 · `data[0]` |
| `findSatisfactionSurveyAnswers` | `/schedule/open/v1/queries/find-satisfaction-survey-answers` | 조회 | 만족도 조사 응답 목록 조회 | `limit` | [문서](https://developers.kos-solution.com/docs/openapi/satisfactionsurvey#findSatisfactionSurveyAnswers) |  | ✅ 200 · `data[0]` |
| `getReschedulableTimeSlots` | `/schedule/open/v1/queries/get-reschedulable-time-slots` | 조회 | 스케줄 ID로 예약 일정 변경 가능한 예약 시간 슬롯 조회 | `scheduleId`, `dateTimeRangeUtc` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getReschedulableTimeSlots) |  | ✅ 200 · `data[60]` |
| `getReservationGroups` | `/schedule/open/v1/queries/get-reservation-groups` | 조회 | 예약 그룹 목록 조회 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getReservationGroups) |  | ✅ 200 · `data[13]` |
| `getReservationRuleSummaries` | `/schedule/open/v1/queries/get-reservation-rule-summaries` | 조회 | 예약 규칙 목록 조회 | 없음 | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getReservationRuleSummaries) |  | ✅ 200 · `data[2]` |
| `getReservationSlotsByGroup` | `/schedule/open/v1/queries/get-reservation-slots-by-group` | 조회 | 예약 그룹으로 예약 슬롯 조회 | `reservationGroupId`, `startDate`, `endDate`, `timezone` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getReservationSlotsByGroup) |  | ✅ 200 · `data[20]` |
| `getReservationSlotsByProduct` | `/schedule/open/v1/queries/get-reservation-slots-by-product` | 조회 | 상품 옵션으로 예약 슬롯 조회 | `startDateUtc`, `endDateUtc` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getReservationSlotsByProduct) |  | ✅ 200 · `data[20]` |
| `getReservationSlotsByScheduleId` | `/schedule/open/v1/queries/get-reservation-slots-by-schedule-id` | 조회 | 스케줄 ID로 예약 슬롯 조회 | `scheduleId`, `startDateTimeUtc`, `endDateTimeUtc` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getReservationSlotsByScheduleId) | **deprecated** | ✅ 200 · `data[60]` |
| `getReservationTimeSlots` | `/schedule/open/v1/queries/get-reservation-time-slots` | 조회 | 예약 규칙으로 예약 시간 슬롯 조회 | `dateTimeRangeUtc` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getReservationTimeSlots) |  | ✅ 200 · `data[60]` |
| `getReservationTimeSlotsByVisitorId` | `/schedule/open/v1/queries/get-reservation-time-slots-by-visitor-id` | 조회 | 내원객 ID로 예약 규칙 기반 예약 시간 슬롯 조회 | `dateTimeRangeUtc`, `visitorId` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getReservationTimeSlotsByVisitorId) |  | ✅ 200 · `data[60]` |
| `reserveV2` | `/schedule/open/v2/commands/reserve` | 쓰기 | 새로운 예약 생성 | `visitorName`, `zoneId`, `occupiedResources` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#reserveV2) |  | — 쓰기(호출 안 함) |
| `reserveByVisitorIdV2` | `/schedule/open/v2/commands/reserve-by-visitor-id` | 쓰기 | 기존 내원객 예약 생성 | `visitorId`, `zoneId`, `occupiedResources` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#reserveByVisitorIdV2) |  | — 쓰기(호출 안 함) |
| `updateReservationV2` | `/schedule/open/v2/commands/update-reservation` | 쓰기 | 예약 일정 수정 | `scheduleId`, `zoneId`, `occupiedResources` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#updateReservationV2) |  | — 쓰기(호출 안 함) |
| `getReservationSlotsByGroupsV2` | `/schedule/open/v2/queries/get-reservation-slots-by-groups` | 조회 | 여러 예약 그룹의 예약 슬롯 조회 | `reservationGroupIds`, `startDateTimeUtc`, `endDateTimeUtc` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getReservationSlotsByGroupsV2) |  | ✅ 200 · `data[1]` |
| `getReservationSlotsByScheduleIdV2` | `/schedule/open/v2/queries/get-reservation-slots-by-schedule-id` | 조회 | 스케줄 기반 예약 슬롯 조회 | `scheduleId`, `startDateTimeUtc`, `endDateTimeUtc` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#getReservationSlotsByScheduleIdV2) |  | ✅ 200 · `data[1]` |

**합계**: 표 72개 = 조회 49 + 쓰기 23. 조회 49개 중 **47개를 불렀다**. 나머지 2개는 입력이 사람 정보라 부르지 않았다. 불러 본 47개 중 **45개가 200**이다(표 밖에서 부른 `getPrepaidCardChargingEventStatistics` 까지 치면 48개 중 46개). 실패 2개는 이렇다.
- `getTicketGroupStatistics` → **404** `No static resource statistics/open/v1/queries/get-ticket-group-statistics`. 스펙과 공식 문서에는 있지만 서버에 경로가 없다. 운영 호스트에서도 같은지는 확인하지 않았다(운영 키 금지)
- `getQuestionnaireSubmit` → 400 `InvalidRequestException`. 요청 필드는 스펙대로 보냈다(`visitorId`). 제출한 설문이 없는 내원객이라 그런 것으로 추정한다

호출 중에 알게 된 필수 조건. 스펙 `required` 에는 없고 서버 오류나 필드 설명에 나온다.
- `getVisitorStatistics`: `limit` 만 보내면 400 `at least one date time range is required`. 날짜 범위 하나를 같이 보내야 한다(`lastVisitedDateTimeUtcFrom/To` 로 보내서 200)
- `findSatisfactionSurveyAnswers`: `limit` 만 보내면 400 `DateTimeRangeRequired`. 스펙 필드 설명에 「`submittedDateTimeRange` · `reservationDateTimeRange` 중 하나 이상 필수, 범위 3개월 이하」라고 적혀 있다
- `searchVisitors`: `offset` · `limit` 만 보내면 400 `BAD_REQUEST`. 스펙 필드 설명을 보면 `phone` · `chartNumber` · `dateOfBirth` 중 하나가 필요하다. 일정 응답에서 받은 `chartNumber` 를 넣어서 200 이 나왔다
- `getTicketBundlesQuery`: 결과가 없을 때 `{"data": []}` 가 아니라 **`{}`** 가 온 경우를 확인했다(`data` 키가 없다)

---

## 3. 데모 실호출 결과 — 응답 모양

조회 범위: `reservationStartDateTimeUtc` **2026-09-20T00:00Z ~ 2026-10-27T00:00Z**(통계 작업도 같은 범위). 값은 enum · 상태 코드만 적는다.

### 3.1 공통 감싸기

목록 조회는 `{"data": [...]}` 꼴이다. 통계(`/statistics/`) 작업은 여기에 `totalCount` 가 붙는다. 단건 조회는 `{"data": {...}}` 다. 예외는 두 개다. `getProduct` 는 상품 필드가 최상위에 바로 온다. `getVisitorQuestionnaire` 도 최상위에 `name · phoneNumber · … · pages[]` 가 온다.

### 3.2 `getSchedulesByFlowStep` — 단계별 건수(데모, 위 범위)

`flowStep` 마다 한 번씩 불렀다. enum(스펙): `RESERVED · RECEPTION · CONSULTATION_WAITING · CONSULTATION · PROCEDURE_WAITING · PROCEDURE · PROCEDURE_DONE · COMPLETED`(+ `FLOW_STATUS_UNSPECIFIED`).

| flowStep | 일정 | 작업 있는 일정 | 작업(`tasks`) 합 | 작업 상태(`tasks[].status`) | `paymentRequired` true/false | `ticketId` 있는 작업 | `purchaseIds` 있는 일정 |
|---|---|---|---|---|---|---|---|
| RESERVED | 10 | 0 | 0 | — | — | — | 2 |
| RECEPTION | 5 | 1 | 3 | NOT_STARTED 3 | 0/3 | 3 | 2 |
| CONSULTATION_WAITING | 1 | 0 | 0 | — | — | — | 0 |
| CONSULTATION | 2 | 2 | 2 | READY 1 · NOT_STARTED 1 | 1/1 | 1 | 2 |
| PROCEDURE_WAITING | 4 | 4 | 12 | NOT_STARTED 6 · READY 5 · DONE 1 | 11/1 | **0** | 0 |
| PROCEDURE | 3 | 3 | 8 | NOT_STARTED 4 · WAITING 2 · READY 1 · DONE 1 | 6/2 | 1 | 3 |
| PROCEDURE_DONE | 2 | 2 | 6 | DONE 3 · CANCELED 3 | 3/3 | 2 | 1 |
| COMPLETED | 2 | 2 | 5 | CANCELED 4 · DONE 1 | 0/5 | 5 | 1 |

- 작업 `type`: `PROCEDURE`(시술) 대부분. `ETCETERA` 는 3건(PROCEDURE_WAITING · PROCEDURE · PROCEDURE_DONE 에 1건씩)
- 일정의 `purchases[]` 는 **모든 일정에서 비어 있다**. 스펙도 이 필드를 「수납 목록 — Deprecated」로 표시한다. 수납은 `purchaseIds[]` 로 가리킨다
- `reservation.status` 관찰값: `RESERVED · CANCELED · IN_PROGRESS · COMPLETED`(스펙에는 `NO_SHOW` 도 있다)
- `taskTimers[].status` 관찰값: `IN_PROGRESS · COMPLETED · CANCELED`(스펙과 같은 값)
- 데모에 **현황판에 필요한 단계가 모두 들어 있다**(접수 → 상담 → 시술 대기 → 시술 → 귀가 대기 → 귀가)

### 3.3 일정 한 건 모양 — `getScheduleDetail` · `getSchedulesByFlowStep` · `getSchedulesByVisitor` · `findScheduleByPurchaseId` 가 같은 모양

```text
data{
  id, flowStep, flowStepUpdatedDateTimeUtc, createdDateTimeUtc, updatedDateTimeUtc, receptionDateTimeUtc, deleted,
  visitor{id, name, phone{countryCode, phoneNumber}, chartNumber, gender, dateOfBirth, nationality, memo,
          visitorType{id,name}, isNew, categories[], snsInfo{snsType, accountId}, phoneticName},
  reservation{reservationGroupId, startDateTime, endDateTime, consultationRequired, sedationRequired,
              counselor{id,name}, doctor{id,name}, funnel{…}, reservationMemo, zoneId,
              reservationAssignee{id,name}, status, requestedProcedures[{type, optionConfiguration{…}}], connectedChannel},
  consultation{counselor{id,name}, doctor{id,name}, consultationMemo},
  consultations[{id, visitor{id,name,isNew}, scheduleId, consultationStartedDateTimeUtc,
                 counselors[{id,name}], consultationDoctors[], consultationProcedures[], content{text},
                 createdDateTimeUtc, updatedDateTimeUtc}],
  tasks[{                                   ← 시술 작업(동선)
    type(PROCEDURE|ETCETERA), sequence:int, order:int, title, status, paymentRequired:bool,
    assignees[{id,name}], doctors[{id,name}], calledDoctors[],
    room{id, zoneId, title, order},
    assigneeMemo, doctorMemo, memo, anesthesiaType, urgencyLevel,
    readyDateTimeUtc, completedDateTimeUtc, doctorCallDateTime, roomAssignedDateTimeUtc, doctorAssignedDateTimeUtc,
    procedureConfiguration{
      productOptionConfiguration{optionId, optionTitle, productTitle, procedure{id,name,…}, unit{type,value}, medicineAndMachines[]},
      ticketConfiguration{ticketId, round{total, current}},      ← 시술권 연결
      medicalServiceConfiguration{id, code, title, unit, machines[], medicines[], caution}},
    etceteraConfiguration{etceteraTaskId, name},
    translsMap{…}}],
  taskTimers[{id, status, taskSequences[], workSequences[], memo, startedDateTimeUtc, estimatedCompletionDateTimeUtc, endedDateTimeUtc}],
  etceteraWorks[], purchaseIds[str], purchases[](deprecated · 비어 있음), prescriptionIds[],
  zone{id,title}, visitorLocation{zoneId}, orderMemo, reactions[{reaction{id}, accounts[{id,name}]}],
  occupiedResources[{id, type(RESERVATION_GROUP), reservationTime{startDateTimeUtc,endDateTimeUtc}, reservationGroup{…}}]
}
```

`getSchedulesSummarizedByTask` 는 `data[{scheduleId, startDateTimeUtc, endDateTimeUtc, tasks[같은 모양]}]` 이다. 일정을 빼고 작업만 담는다.

관찰한 enum: `tasks[].anesthesiaType` = `ANESTHESIA_TYPE_UNSPECIFIED`, `tasks[].urgencyLevel` = `URGENCY_LEVEL_UNSPECIFIED`, 단위 `unit.type` = `SHOT · UNIT · CC · KJ · PULSE · VIAL · QUANTITY · SYRINGE · MINUTE`.
작업 상태 enum(스펙 `FlowTask.status`): `WAITING`(대기) · `READY`(준비) · `DONE`(완료) · `NOT_STARTED`(시작 전) · `CANCELED`(취소). 데모에서 다섯 값이 모두 나왔다.

### 3.4 수납 · 시술권 · 통계 모양

| 작업 | 응답 모양(최상위 → 주요 필드) | 데모 건수 · enum |
|---|---|---|
| `getPurchaseSummaries` · `getPurchaseSummariesByVisitor` | `data[{id, visitorId, status, process, assignee, assignees[], createdDateTimeUtc, lastUpdatedDateTimeUtc, transactions[{id, price, status, paymentType, assignee, paymentDateTime{approvedDateTimeUtc,…}, …}], items[{id, type, optionConfiguration{id, title, productTitle, optionType, compositions[{procedure{id,name}, count, unit, price, medicalService{…}}]}, price, adjustedPrice, priceV2, basePrice, …}], pendingItems[], revokingItems[], refundingItems[], priceAdjustments[]}]` | 일정들의 `purchaseIds` 21개를 넣었는데 **7건만** 돌아왔다(이유는 문서에 없다). `status`: `ACCEPTED` 4 · `INITIALIZED` 2 · `REFUNDED` 1 / `process`: `NOT_IN_PROCESS` 5 · `PENDING` 2 / `items[].type` = `PRODUCT_OPTION` / `transactions[].status` = `APPROVED · CANCELED`, `paymentType` = `CARD · CASH · TRANSFER` |
| `getTicketBundlesQuery` | `data[{purchaseId, purchaseItemId, visitorId, title, price, optionConfiguration{optionId, optionTitle, productTitle, promotionConfiguration}, ticketSets[{procedure{id,name}, title, ticketGroupId, unit, medicalService{…}, tickets[{id, status, price, createdDateTimeUtc}]}]}]` | 결과가 없을 때 `{}` 가 온 경우를 확인했다. 관찰된 `tickets[].status` 는 `AVAILABLE` 뿐이다(작업 설명이 「**사용 가능한** 시술권 묶음」이다). 스펙 enum: `AVAILABLE · USED · CANCELED · IN_USE` |
| `getProcedureTaskStatistics` | `data[{scheduleId, taskSequence, procedureTaskId, completedDateTimeUtc, productTitle, productOptionTitle, procedureName, title, ticketPriceV2, paymentRequired, roomAssignedDateTimeUtc, doctorAssignedDateTimeUtc, doctorNames, …}]`, `totalCount` | `data[6]`. 완료된 작업만 나온다(필수 조건이 `completedDateTimeUtc` 범위다) |
| `getPurchaseItemStatistics` | `data[{purchaseId, purchaseItemType, purchaseStatus, productTitle, productOptionTitle, productOptionProcedureNames, procedureConfigurations[…], …}]`, `totalCount` | `data[6]` · `purchaseStatus` `ACCEPTED · REFUNDED` |
| `getTransactionStatistics` | `data[{purchaseId, paymentType, status, cost, assigneeName, visitorId, …}]`, `totalCount` | `data[9]` |
| `getScheduleStatistics` | `data[{scheduleId, reservationStartDateTimeUtc, reservationStatus, zoneTitle, reservationGroupTitle, requestedOptionTitles, …}]`, `totalCount` | `data[29]` · `reservationStatus` `RESERVED · IN_PROGRESS · COMPLETED · CANCELED` |
| `getVisitorStatistics` | `data[{visitorId, isCompletedPurchase, isCompletedProcedureTask, totalCompletedScheduleCount, totalTicketCount, …}]`, `totalCount` | `data[2]` |

### 3.5 시술 메뉴 · 구역 · 직원 · 내원객 모양

| 작업 | 모양 | 데모 건수 |
|---|---|---|
| `getProducts` | `data[{id, title, description, categories[], options[{id, title, type, price, count, procedure, compositions[], medicineAndMachines[], displayChannels[], …}], closed, deleted, isEvent, order, …}]` | 101 · `options[].type` `SINGLE · GROUP` |
| `getProduct` | 위 상품 1건이 최상위에 온다(`data` 로 감싸지 않음) | 1 |
| `getProductOptions` | `data[옵션 모양]` | 5(5개 id 를 요청) |
| `searchProductOptionSummaries` | `data[{id, title, type, price, productId, productTitle, compositions[], procedure, medicalService, …}]` | 279(`searchText: "a"`) |
| `getCategories` | `data[{id, name, order, deleted, opened, translsMap}]` | 15 |
| `getProcedures` | `data[{id, name}]` | 804 |
| `getMachines` | `data[{id, name}]` | 302 |
| `getMedicines` | `data[{id, name}]` | 349 |
| `getMedicalServices` | `data[{id, title, status, configuration{code, procedure, machines[], medicines[], unit, healthcareReimbursement, taxation}, description, …}]` | 226 |
| `getZones` · `getZone` | `data[{id, title, order, isDefault}]` | 2 |
| `getAccounts` | `data[{id, name, email, roleTags[], activate}]` | 77 / 활성 53. `roleTags` 값(문자열): `ADMIN` 40 · `COUNSELOR` 21 · `CALL_COUNSELOR` 17 · `SKINCARE` 14 · `COORDINATOR` 14 · `NURSE` 13 · `DOCTOR` 12(한 사람이 여러 태그를 가질 수 있다) |
| `getVisitor` | `data{id, chartNumber, name, phoneNumber, dateOfBirth, gender, nationality}` | 1 |
| `searchVisitors` | `data[{id, chartNumber, name, phoneNumber, dateOfBirth, gender, nationality, passportSurname, passportGivenNames}]` | 1 |
| `getVisitorQuestionnaire` | 최상위 `{name, phoneNumber, phone{…}, address, addressDetail, dateOfBirth, gender, pages[{id, title, questions[…]}], agreements[]}` | pages 4 |
| `getReservationGroups` | `data[{id, title, memo, startDate, intervalMinutes, intervalCapacities, isDefault, operationTimetable, order, …}]` | 13 |
| 슬롯 조회 7종 | `data[{… startDateTimeUtc, endDateTimeUtc, capacity, reservationCount}]` 또는 `data[{dateTimeRangeUtc, available, …}]`, `timeSlotIntervalMinutes` | 표 참고 |

---

## 4. 「수납 → 시술 목록」이 어디서 보이나

데모에서 **연결 고리 하나를 끝까지 확인**했다. 내원객 1명의 id 를 서로 맞대 보았다(값은 적지 않는다).

```text
getPurchaseSummaries        data[].id ─────────────┐        data[].items[].id ─────────┐
                                                   │                                    │
getTicketBundlesQuery       data[].purchaseId ◀────┘        data[].purchaseItemId ◀────┘
                            data[].ticketSets[].tickets[].id ──┐
                                                               │
getScheduleDetail 등        data.tasks[].procedureConfiguration.ticketConfiguration.ticketId ◀──┘
                            data.purchaseIds[]   (← 수납 id 를 담는다)
findScheduleByPurchaseId    수납 id → 그 일정(위와 같은 모양)
```

| 질문 | 답(데모 확인) | 근거 |
|---|---|---|
| 수납이 끝난 건의 **시술 목록**은 어디 있나 | 일정의 **`tasks[]`**(type `PROCEDURE`)에 있다. 한 작업이 시술권 한 장(`ticketConfiguration.ticketId` · `round`)과 이어진다 | `getScheduleDetail` · `getSchedulesByFlowStep` · `findScheduleByPurchaseId` |
| 수납 ↔ 일정 | 일정의 `purchaseIds[]` 에 수납 id 가 들어 있다. 거꾸로 `findScheduleByPurchaseId(purchaseId)` 로 일정을 찾을 수 있다. 환불(`REFUNDED`)이 아닌 수납 1건으로 확인: 일정이 나왔고, 그 일정의 `purchaseIds` 에 그 수납 id 가 있었다 | 확인 |
| 수납 ↔ 시술권 | 시술권 묶음의 `purchaseId` = 수납 `id`, `purchaseItemId` = 수납 `items[].id`. 9명 중 1명에서 셋이 모두 맞았다(묶음 1 · 수납 품목 1 · 작업 ticketId 1) | 확인 |
| 시술권 ↔ 작업 | 묶음의 `tickets[].id` = 작업의 `ticketId`. 묶음이 있는 내원객 2명 중: 작업 ticketId 4개 중 3개, 1개 중 1개가 맞았다 | 확인 |
| 수납한 품목 그 자체(무엇을 샀나) | `getPurchaseSummaries.data[].items[].optionConfiguration{title, productTitle, compositions[{procedure, count, unit}]}` | 확인 |
| 결제 전 작업 | `PROCEDURE_WAITING` 단계 일정 4건의 작업 12개 중 11개가 `paymentRequired: true` 이고 `ticketId` 는 **0개**였다. 시술권 없이 작업이 먼저 동선에 들어갈 수 있다는 뜻이다(v1 workflow 「현장 확인할 것」 첫 줄과 같다). 이 작업들이 수납 뒤에 ticketId 를 받는지는 **미확인**이다(시간을 두고 다시 보지 않았다) | 데모 관찰 |

**주의**
- `getTicketBundlesQuery` 는 **사용 가능한(`AVAILABLE`) 시술권만** 준다. 이미 작업에 들어가 사용 중이거나 사용한 시술권은 빠진다(추정: 9명 중 7명이 결과 없음이었고, 작업 ticketId 4개 중 1개는 묶음에 없었다). 그래서 「작업 → 시술권」을 거꾸로 맞출 때 이 작업만으로는 빠지는 게 생긴다
- 일정의 `purchases[]` 는 deprecated 이고 비어 있다. 쓰지 않는다
- `getPurchaseSummaries` 에 id 21개를 넣었는데 7건만 왔다. 나머지 14개가 어떤 수납인지(삭제됨 · 다른 종류 등)는 **문서에 없음 · 미확인**

---

## 5. 쓰기 작업 — 시술 진행 · 완료 · 배정 · 이동

**호출하지 않았다.** 스펙에 있는 쓰기 25개 중에서 일정 · 동선에 닿는 것만 고른 표다. 나머지(상품 · 이미지 · 내원객 설문 · 마케팅 동의)는 §2 표에 있다.

| 현황판에서 할 법한 조작 | 공개 OpenAPI 작업 | 요청 필수 | 문서 | 비고(스펙) |
|---|---|---|---|---|
| 진료 단계 바꾸기(접수 · 상담 · 시술 대기 · 시술 · 귀가 대기 · 귀가) | `changeFlowStep` | `scheduleId` · `step` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#changeFlowStep) | 400 오류 4종: `ScheduleNotFound` · `CounselorNotFound` · `ProceduresNotFound` · `ProceduresNotCompleted`. 응답은 `protos.Empty` |
| 예약 메모 바꾸기 | `changeReservationMemo` | `scheduleId` · `memo` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#changeReservationMemo) | 09-18 이후 새로 생김. 메모를 **통째로** 바꾼다. 예약 상태와 관계없이 된다 |
| 상담 메모 | `updateScheduleConsultationInfo` | `scheduleId` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#updateScheduleConsultationInfo) | 필드는 `consultationMemo` 하나 |
| 예약 취소 · 노쇼 | `cancelReservation` | `scheduleId` · `reason` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#cancelReservation) | `reason`: `CANCELED` · `NO_SHOW` |
| 시간 점유(구역 · 예약 그룹 시간 막기) | `createOccupiedTime` | `startDateTimeUtc` · `endDateTimeUtc` · `zoneId` · `reservationGroupId` | [문서](https://developers.kos-solution.com/docs/openapi/schedule#createOccupiedTime) | 예약 칸을 막는 것이다. 방 배정이 아니다 |
| 예약 일시 · 구역 변경 | `updateReservationV2` · `rescheduleByTimeSlot` (· `updateReservation` deprecated) | `scheduleId` · `zoneId` · `occupiedResources` / `scheduleId` · `reservationDateTimeRange` | [V2](https://developers.kos-solution.com/docs/openapi/schedule#updateReservationV2) · [슬롯](https://developers.kos-solution.com/docs/openapi/schedule#rescheduleByTimeSlot) | 예약 일정을 바꾸는 작업이다. 동선 작업과는 상관없다 |
| **시술 작업 완료**(DONE · 시술권 차감) | — | — | — | **스펙에 없음** |
| **시술 작업 취소**(단건 · 일괄) | — | — | — | **스펙에 없음**(`cancelReservation` 은 예약 전체를 취소한다) |
| **시술 작업 추가**(시술권을 동선에 넣기) | — | — | — | **스펙에 없음** |
| **작업 순서 바꾸기**(`sequence` · `order` · 우선순위) | — | — | — | **스펙에 없음** |
| **담당자 · 집도의 배정**(`tasks[].assignees` · `doctors`) | — | — | — | **스펙에 없음**(`updateReservation` 의 `counselor` · `doctor` 는 예약 단위 담당이다. deprecated) |
| **방 배정 · 이동**(`tasks[].room`) | — | — | — | **스펙에 없음**. 방 목록 조회도 없다 |
| **상담사 지정**(상담 기록 `counselors`) | — | — | — | **스펙에 없음**. `changeFlowStep(CONSULTATION)` 은 상담 담당이 없으면 `CounselorNotFound` 로 거절한다 |
| 타이머(`taskTimers`) 시작 · 종료 | — | — | — | **스펙에 없음** |

KOS 웹앱 **내부** API(공개 OpenAPI 아님)로 위 「스펙에 없음」 중 일부를 확인한 기록이 1차 조사에 있다. `orchestration/work/_archive/cc-prototype/sts-prototype/research-kos-har-report.md` · `research-kos-har2-report.md` 를 보라. 확인된 것은 `cancel-flow-tasks` · `change-tasks-complete` · `change-tasks-assignees` · `change-tasks-doctors` · `create-consultation` 등이다. 이것들은 호스트(`api.kos-solution.com/tenants/{id}`)와 인증이 공개 API 와 다르다. 이번에 다시 확인하지 않았다.

---

## 6. 정할 것 (결정하지 않고 모음)

1. **현황판이 시술 목록을 어디서 읽나**: 일정의 `tasks[]` 를 쓸지(`getSchedulesByFlowStep` · `getScheduleDetail`), 시술권 묶음을 쓸지(`getTicketBundlesQuery`, `AVAILABLE` 만 나옴), 수납 품목을 쓸지(`getPurchaseSummaries.items[]`), 아니면 섞어 쓸지
2. **어떻게 불러오나**: 단계별 `getSchedulesByFlowStep` 을 8번 부를지, `getScheduleStatistics` 같은 다른 방법을 쓸지. 호출 간격 · 주기도 정해야 한다. 호출 한도(`429`) 수치는 이번에 보지 않았다(문서 「호출 한도」 절)
3. **결제 전 작업**(`paymentRequired: true` · `ticketId` 없음)을 현황판에 띄울지, 어떻게 보일지
4. **쓰기를 어디까지 할지**: `changeFlowStep` 만 공개 API 로 열려 있다. 그런데 `CONSULTATION` 이후 단계는 상담사 · 시술 · 완료 조건 때문에 거절될 수 있다. 데모 지점에서도 쓰기를 해 볼지(이번 브리프는 금지)
5. **공개 API 에 없는 조작**(작업 완료 · 취소 · 추가 · 순서 · 배정 · 방 · 상담사 · 타이머): KOS 에 요청할지, 내부 API 를 쓸지, KOS 화면에서 하게 둘지
6. **방 목록의 출처**: 공개 API 에는 없다. `tasks[].room` 에서 모을지, 다른 방법을 쓸지
7. **`getTicketGroupStatistics` 404**: 스펙과 서버가 다르다. 쓸 일이 있으면 KOS 에 물어볼지
8. **`getPurchaseSummaries` 21 → 7**: 일정의 `purchaseIds` 에 있지만 조회되지 않는 수납이 무엇인지 KOS 에 확인할지
9. **직원 → 화면 직군 매핑**: `getAccounts.roleTags`(문자열 7종, 한 사람이 여러 태그)를 쓸지, `activate` 로 거를지
