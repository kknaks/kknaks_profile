# 작업 요약 — customer-erd (day)

기간: `2026-11-18` ~ `2026-11-19`
결과: 머지 · dev 배포 · dev 백필까지 끝. CENTURION_DAY #260 · #261(dev) · mediness #951 · #952(main) · Delivery #259 닫음. prod 는 2026-11-20 병원 마감 뒤(사용자).

## 1. 무엇을 했나

예약 기능이 DAY 로 넘어오면 DAY 가 고객 · 구매 · 시술권 · 선불카드의 원천이 된다. 그런데 DAY 에는 메뉴 · 결제 테이블이 없었다(「1차는 스냅샷만」). KOS HAR 을 4번 실측해 ERD v1 을 사용자와 닫았고, 이를 메디니스 정본에 옮겼다(SPEC-000 칸 계약 · `erd.md` · 동기화 SPEC-002 개정 ㉔). 그 계약대로 CENTURION_DAY 를 만들었다:

- migration 0010: 새 테이블 28 · `visit_task` nullable 칸 3
- KOS → DAY 동기화: 메뉴 1시간 · 오늘 구매 10초 · 시술권 · 카드는 바뀐 고객만
- 수동 백필 스크립트 + migration 0011

전부 상용 서비스를 멈추지 않는 더하기만으로 했고, 나중에 KOS 를 뗄 수 있는 모양으로 했다. dev 에 배포한 뒤 백필을 실행했다(방문 1,319 · 구매 408 · 시술권 번들 429 · 티켓 536 · 카드 15).

## 2. 적용한 기술·개념

- **외부 시스템을 뗄 수 있는 스키마 — `external_ref` 한 곳에만 외부 id** → [[external-id-mapping-table]] — 새 테이블 28개 어디에도 KOS id 칸을 두지 않았다. 테이블 사이 연결은 DAY id FK 로만 했다. KOS 를 떼면 대응표만 지우면 된다.
  - 왜: 사용자 전제 「나중에 KOS 를 뗀다」. 칸마다 `kos_id` 를 두면 뗄 때 28개 테이블을 다 고쳐야 한다.
  - 어려웠던 것:
    - KOS 가 계산해서 주는 값(카드 총액 · 티켓별 가격)을 칸으로 두고 싶은 유혹이 있었다. 「DAY 가 계산할 수 있는 값은 칸으로 두지 않는다 · KOS 가 해 주던 일을 DAY 칸만으로 할 수 있나」를 테이블마다 표로 검사해 걸렀다.
    - 외부 id 가 행마다 유일하지 않은 경우가 실물에서 나왔다(환불 두 주머니가 같은 `chargingId`). → `chargingId:주머니` 합성 키로 풀었다.
  - 근거: `reference/2026-11-18-day-customer/erd-draft.md` · SPEC-000 §4 「KOS 없이 되는지」 표 · `be-2-report.md` 실물 발견 1
- **상용 서비스 중 스키마 추가 — 더하기만 · 이전 이미지 호환 롤백** → [[online-schema-change]] — 기존 52 테이블의 칸 · 타입 변경은 0 이다. 새 칸은 모두 nullable 이고 데이터 이동은 없다.
  - 왜: dev 는 머지하면 migration 이 자동으로 돌고, 롤백은 이미지만 바꾼다(forward-only). 이전 코드가 새 스키마 위에서도 돌아야 롤백이 성립한다.
  - 판단이 갈린 것: 1:0..1 관계를 DB 유일 제약으로 막을지. `visit_task.ticket_id` 에 걸면 KOS 가 작업을 취소하고 같은 티켓을 다시 쓸 때 **지금 돌고 있는 10초 현황판 동기화가 막힌다**. 그래서 빈 테이블이고 위험이 낮은 `ticket_bundle.purchase_item_id` 하나만 걸었다(검수 1 §5).
  - 근거: `review-code-1-report.md` · `review-code-4-report.md`
- **새 동기화를 기존 회차와 격리** — 메뉴 · 구매 회차는 잠금 · 상한 · 세션 · 예외를 따로 둔다.
  - 오늘 구매는 일정 태스크 안에서 기다리지 않고 별도 태스크(`.kiq`)로 뗐다.
  - `fetch_schedules` 안의 sale 파싱은 `except Exception` 으로 감쌌다.
  - 왜: 새 기능이 실패해도 판(현황판)은 멈추면 안 된다. 같은 프로세스 · DB 풀을 쓰면 시간과 풀이 판 동기화로 번진다(검수 3 WARN-1).
  - 근거: `review-code-3-report.md` · `sync-fix-2.md`
- **「바뀐 것만」 폴링과 못 푼 항목의 음성 캐시** → [[polling]] — 시술권 · 카드는 구매나 작업 티켓이 바뀐 고객만 다시 받는다.
  - 막혔다가 푼 것: 「DAY 에 없는 티켓 = 바뀐 고객」 규칙이 문제였다. 출처 구매가 없어 영원히 못 푸는 지난 시술권 때문에 같은 고객을 **10초마다 하루 종일** 다시 불렀다(병원당 최대 40호출/10초).
    - DEMO 오늘 방문에는 작업이 0건이라 실물 확인에서 드러나지 않았고, 코드 검수 3 이 읽어서 잡았다.
    - 못 푼 티켓 id 를 병원별 Redis 집합(그날 끝 TTL)에 두어 풀었다.
  - 근거: `review-code-3-report.md` FAIL-1 · `review-code-4-report.md`
- **비용 기준 API 고르기 — 공개 API 0** → [[public-vs-internal-api]] — 처음 설계는 공개 통계 API 로 5분마다 「오늘 밖 고객의 변경」을 잡았다. 사용자가 「공개 api 비싸」라고 해서 바꿨다.
  - 5분 회차를 통째로 뺐다(OQ-00-4 다시 엶).
  - 진료항목 · 기기 · 약물은 내부 상품 응답 안에서 모으게 했다. 옵션에서 빠졌다고 지우지 않는다.
  - 기존 운영 코드의 구역 목록도 내부 경로로 바꿨다. 운영 루프의 공개 토큰 발급이 0 이 됐다.
  - 근거: `sync-fix-3-internal-only.md` · dev grep(운영 경로 `"open"` 0)
- **외부 API 백필 — 페이싱 · 멱등 · 이어 하기** → [[paced-backfill]] · [[idempotency]] — 수동 스크립트 `python -m runtime.backfill`.
  - `PacedTransport` 로 모든 KOS 요청(재시도 포함)을 1초 이상 간격으로 보낸다.
  - 쓰기는 운영 upsert 를 재사용해 두 번째 실행에서 쓴 행이 0 이다. 진행 위치는 Redis 에 둔다.
  - 세션 표시를 `backfill` 로 해서, 기기 5대 제한의 자동 해제가 운영 세션에 닿지 않게 했다.
  - 왜: 실사용 중인 KOS 계정과 rate limit 를 같이 쓴다. 배포 migration 안에서 KOS 를 부르면 KOS 가 늦을 때 배포가 멈춘다. 그래서 alembic 이 아니라 별도 수동 명령으로 뒀다.
  - 실측: DEMO 1회 752호출 / 750초. 처음 추정 150호출의 5배였다. 고객 목록을 전부 훑는 카드 단계가 대부분(596초)을 차지했다.
  - 근거: `be-3-report.md` · `review-code-6-report.md` · dev 실행 로그
- **HAR 실측으로 스키마 정하기 — 키 대조의 한계** → [[public-vs-internal-api]] — 응답 키 전수 → DB 칸 대조로 빠진 키 11개(초성 검색어 · 노출 국가 · 약품기기 이름 등)를 찾아 보강했다.
  - 한계: 「응답 키에 칸이 있다」는 「값이 온다」가 아니다. `promotionConfigurations` 는 칸이 있었는데 **요청이 `includePromotions:false` 라** 늘 비어서 왔다.
  - 키 대조에는 **요청 파라미터**도 같이 봐야 한다.
  - 「이벤트가」는 프로모션이 아니라 수가 유형 가격(`price.additional[]` · visitorType 「이벤트가」)이었다. 사용자 HAR(`상품가격.har`)로 확인했고 dev DB 1행으로 검증했다.
  - 근거: `menu-keys-addition.md` · `har/상품가격.har`
- **결제 취소 ≠ 환불 모델링** — 결제 취소는 결제 한 건만 되돌린다. 구매는 확정 그대로 미수가 되고 다시 결제한다. 환불은 구매를 되돌리는 것이고, 항목 조정 금액과 회수가 따른다.
  - 처음에는 「취소하면 카드 소프트 딜리트」로 정했다. 사용자 화면(「부족합니다 · 이어서하기」)과 `결제취소2.har`(취소 뒤 카드 잔액 그대로)로 뒤집었다.
  - 근거: `har-check-report-3.md` · erd-draft 「결제 취소 · 환불」 절

## 3. 막혔던 것 / 사고

- **사용자 말 오독 두 번.**
  1. 「로그를 남기는 방향」을 동기화 삭제 로그(`event_log`)로 읽고 스펙에 넣었다. 사용자 뜻은 직원 동작 감사 로그(의료법 근거 — 이미 있음)였다. 한 판 쓰고 되돌렸다.
  2. 「백필 내가 해야할거 같아서」를 「이번 작업에 넣자」로 읽어 백필 3단계를 발주했다. 사용자 「백필 내가 한다고!」 → 코드를 PR 에서 분리했다. 이어서 「백필 하라니까」 → 결국 별도 PR #261 로 올렸다. **주어(누가)가 빠진 문장은 되묻는다.**
- **확인 없이 단정해 정정 네 번.**
  1. 「결제 취소하면 카드 그대로」 — 표본 없이 말했다. 사용자 스크린샷과 HAR 로 맞긴 했지만 순서가 틀렸다.
  2. 「설명은 KOS 응답에 없다」 — 요약 표만 봤다. 실제로는 상품 48/48 · 옵션 68/68 에 있었다.
  3. 「번역 담을 칸 없다」 — 모델에 `translations` 가 이미 있었다.
  4. 「KOS 키 다 받는다」 — 요청 파라미터로 비워진 프로모션을 놓쳤다.
  - → 상태는 열어 보고 말한다(기존 피드백 그대로 재발).
- **조사 범위 누락** — 조사 4차가 「내부 고객 목록 API 없음」으로 결론냈다. 실제로는 메인 레퍼런스 `2026-10-23-cc-overall-board/har` 에 `visitor/v2/queries/get-visitors` 가 있었다. 사용자가 짚었다. **조사 브리프의 입력에 이번 작업 HAR 만 줬다** — 레포 전체 레퍼런스를 함께 줘야 했다.
- **발주서 머리말 깨짐** — 제가 쓴 파이썬 치환이 빈 줄 기준이라, 제목이 글자마다 끼었다. 2단계 · 코드 검수 · 3단계 브리프 세 개가 깨졌다. 본문은 무사해 워커 결과에는 영향이 없었다. 나중에 복구했다.
- **실물에서만 보인 KOS 동작** — 묶음 구성 `title` 이 비어 옴(34/34) · 티켓 `CANCELED` 상태 · 열린 구매 항목이 `pendingItems` 에만 있음 · 시술권 조회 2xx 빈 본문 · 환불 이벤트 `chargingId` 중복. HAR 표본에는 없었고, DEMO 실호출에서 나왔다. 모두 스펙 · 코드에 반영했다.
- **dev 일회성 컨테이너 첫 실행 실패** — `AppEnvMissingError`. compose 가 주는 환경(`APP_ENV` 등)이 `app.env` 에 없었다. 운영 api 컨테이너 환경을 600 임시 파일로 넘겨 풀었고, 끝난 뒤 삭제했다.
- **공개 레포 노출 위험** — 고객 이름 한 곳(조회 지시서), 회사 코드 패치 1,448줄이 work/ 에 있었다. 마감 grep 으로 잡아 이름은 가리고 패치는 삭제했다.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-18 | 예약 구현 뒤 DAY 가 고객 · 구매 · 시술권 · 선불카드 원천 · KOS 로 전달 | 사용자 |
| 2026-11-18 | 시술권 · 선불카드는 고객에 붙음 · 방문 없는 구매 없음 · 티켓 1행 = 시술 1회 · 가격은 번들에만 | 사용자 |
| 2026-11-18 | 이름 `treatment` · `treatment_item`(피부과엔 「진료」 없음) | 사용자 |
| 2026-11-18 | ~~상품 결제 취소 시 카드 소프트 딜리트~~ → 결제 취소는 카드 그대로 · 환불 완료만 회수 + 소프트 딜리트 + KOS 환불 | 사용자 · `결제취소2.har` |
| 2026-11-19 | ERD → 메디니스 SPEC-000 · erd.md 까지 · 기준 = 상용 운영 중(더하기만) · KOS 뗄 것 | 사용자 |
| 2026-11-19 | 동기화 정할 것 1~9 추천대로 · 테스트 계정은 DEMO 테넌트만(두 번째 테넌트 = 실 명동점) | 사용자 |
| 2026-11-19 | 삭제는 소프트 딜리트만 · ~~동기화 삭제 로그~~(감사 로그는 기존 것) | 사용자 |
| 2026-11-19 | **운영 동기화 공개 API 0**(비용) · 5분 회차 뺌 · 구역 목록 내부 경로 | 사용자 |
| 2026-11-19 | 메뉴 키 보강 11칸 · `ticket_bundle.purchase_item_id` 부분 유일만 | 사용자 「응」 · 검수 1 |
| 2026-11-19 | `pendingItems` 받음 · 구성 title nullable · ticket canceled · 닫힌 선불카드 상품 포함 | 사용자 「나머지 진행」 |
| 2026-11-19 | ~~백필 = 다른 담당~~ → ~~이번 작업~~ → 사용자 담당 → **레포 스크립트로 별도 PR · dev 실행은 코디** | 사용자(세 번 바뀜) |
| 2026-11-19 | 머지는 spec · code 한 번에 · 스쿼시 · dev 데이터 초기화 없음 · prod 는 2026-11-20 병원 마감 뒤 | 사용자 |

## 5. 날짜별 로그

- `2026-11-18` 지금 prod 고객 테이블 ERD · ERD 초안 v0 → v1 · KOS HAR 조사 3차(취소 · 재결제 · 환불 · 부분 환불 · 다회권 · 선불카드 · 공유) · 정할 것 전부 닫음 · mediness #951 PR
- `2026-11-19` #951 머지 · KOS 실호출 조사(테스트 계정 · DEMO) · 상품 JSON 가이드 · 동기화 스펙 #952 · Delivery #259 · DB 0010 · 동기화 · 공개 API 0 전환 · 코드 검수 1~6 · #260 · #952 · #261 스쿼시 머지 · dev 배포 · dev 백필 실행

## 6. 산출물

프로젝트와 당시 작업 문서는 `sync-work-links.py`가 만드는 작업 목차로 연결한다.
아래에는 판단의 근거가 된 리포트·PR·커밋을 구체적으로 남긴다.

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/951 (`4585fb59`) · https://github.com/MediSolveAIDev/mediness/pull/952 (`85bcde17`)
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/260 (`945be39b`) · https://github.com/MediSolveAIDev/CENTURION_DAY/pull/261 (`844eace4`)
- Delivery: https://github.com/MediSolveAIDev/CENTURION_DAY/issues/259 (닫음)

- `kknaksss/customer-erd-sync` → `main`
  - `d9a67758` docs(day): 동기화 스펙 실물 반영 — 공개 API 0 · 메뉴 키 보강 · pendingItems · 5분 회차 뺌 · 백필은 담당 별도
  - `4fe24e4b` docs(day): KOS → DAY 새 테이블 동기화 — SPEC-002 개정 ㉔ · SPEC-000 칸 수정 (2026-11-19)
- `kknaksss/customer-erd-backfill` → `dev`
  - `2aa39bfa` feat: 지난 이력 백필 스크립트(수동) · visit 날짜 인덱스 0011
- 리포트:
  - HAR 조사: `har-check-report.md` ~ `-3.md`
  - KOS 실호출 조사: `kos-sync-research-report.md`
  - 스펙: `spec-change-report.md` · `spec-sync-report.md` · `review-spec-report{,-2}.md` · `review-sync-report.md`
  - 코드: `be-1~4-report.md` · `review-code-1~6-report.md`
  - Delivery: `delivery-start-report.md`
- ERD 초안 · 상품 JSON 가이드: `reference/2026-11-18-day-customer/erd-draft.md` · `kos-product-json-guide.md` · `customer-erd.md`

## 7. 잔여

- **prod(2026-11-20 병원 마감 뒤)**
  - `migrate-prod`(0010 · 0011 — 0011 은 `visit` 쓰기를 잠시 막음)
  - prod fast-forward(dev 에 쌓인 #258 등 다른 커밋도 함께)
  - 첫 기준 정보 회차에서 **구역 수가 이전과 같은지** 확인(검수 4 WARN-C)
  - 백필: 드라이런 → 달별 받은 건수를 KOS 예약 수와 대조 → 실행(검수 6 WARN-1 · 한 번에 하나 · 고객 1만 명이면 3~4시간)
- **후속 판단(OQ)**
  - 방문 이력 없는 고객을 고객 목록(`get-visitors`)에서 넣을지 — DEMO 13명 · 그 고객 카드와 공유 고객이 빠짐
  - 프로모션(`includePromotions`)을 받을지 — 표본 0
  - 메뉴 동기화 주기(지금 1시간) 단축
  - 오늘 밖 고객 변경(OQ-00-4)
  - `open_api_key` 필수 해제(OQ-01-4)
  - 수가 유형 가격의 공급가 · 부가세 칸
  - 가격 조정 칸(OQ-08-4)
- **Delivery 원장**: `review-delivery` · `spec-sync` CLI 기록 없이 마감 댓글 + close 로 닫았다(사용자 「이슈 닫아줘」). mediness MCP 미인증이라 Task projection 은 degraded 다.
- **로컬**: HAR 원본은 `reference/2026-11-18-day-customer/har/` 에 있다(gitignore · 개인정보 · 코디 워크트리에만). 연구 터미널 `term_62a00765…` 은 코디 워크트리에 남아 있다.

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/day/customer-erd/README|customer-erd]]
<!-- work-links:end -->
