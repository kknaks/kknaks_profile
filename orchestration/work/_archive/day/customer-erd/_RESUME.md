
# 재개 노트 — customer-erd (day)

**지금**: 전부 머지 · dev 배포 완료 — #260(`945be39b`) · mediness #952(`85bcde17`) · 백필 #261(`844eace4` · 0011 적용 · 이미지에 runtime.backfill) · dev 백필 실행 완료(방문 1319 · 구매 408 · 번들 429 · 티켓 536 · 카드 15 · 이력 33) · Delivery #259 닫음
**다음**: prod = 2026-11-20 병원 마감 뒤(사용자) — migrate-prod 0010·0011 → ff → 구역 수 확인 → 백필 드라이런 · 대조 · 실행. 마감 = SUMMARY 작성 → archive-work.sh → 회고 · 개념

세팅: `scripts/new-work.sh day customer-erd` · 설정 SSOT `config/projects/day.json`
코디handle: `term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- spec: `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec` (`kknaksss/customer-erd-sync` · PR #952)
- delivery(detached · CLI만): `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-delivery` = origin/main `4585fb59`
- code: `/Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd` (`kknaksss/customer-erd` · base origin/dev `bbd9220a` · PR → dev)


## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [ ] mediness PR #952 머지 — https://github.com/MediSolveAIDev/mediness/pull/952
- [ ] 상품 JSON 가이드(`reference/…/kos-product-json-guide.md`) 실 명동점 읽기 — 사용자 허용 확인 대기
- [!] HAR 은 `reference/2026-11-18-day-customer/har/` — `*.har` gitignore · 개인정보 포함 · 공개 레포라 커밋 금지

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-18 | 예약 구현 뒤 DAY 가 고객 · 결제 원천 → KOS 로 전달 | 사용자 |
| 2026-11-18 | 고객 · 메뉴 · 구매 · 시술권 · 선불카드 DAY 테이블로 · 수납 · 처방 화면은 KOS 딥링크 | 사용자 |
| 2026-11-18 | 시술권 · 선불카드는 고객에 붙는다 · 방문 없는 구매 없음(visit_id 필수) | 사용자 |
| 2026-11-18 | ticket 1행 = 시술 1회 · visit_task.ticket_id | 사용자 |
| 2026-11-18 | 상태는 purchase 에(status · process) · 수납 필요 = 열린 구매 | 사용자 · HAR 52건 |
| 2026-11-18 | 유효기간 칸 나중 · 약품 · 기기 넣음 · 처방 최소 테이블 | 사용자 |
| 2026-11-18 | 1차 리포트 정할 것 9건: 추천대로 · 선물(구매자≠소유자) 지금 없음 — 나중 기능 | 사용자 |
| 2026-11-18 | 선불카드 공유 고객 있음 → `prepaid_card_customer` · 이력에 사용자 · ~~상품 구매 취소 시 카드 소프트 딜리트 + KOS 에도 취소~~ → 11-18 뒤집음: 결제 취소는 「다시 결제」용이라 카드 그대로(KOS 실측 `결제취소2.har`) · **환불 완료만** 회수 + 소프트 딜리트 + KOS 환불 명령 | 사용자 |
| 2026-11-18 | 2차 리포트 정할 것 8건 추천대로: `prepaid_card_product` 별도 · `purchase_item.item_type` + 종류별 FK · 충전 두 길 · ledger 칸 · `ticket_set` 단위 · 이름 스냅샷 | 사용자 |
| 2026-11-18 | 3차 리포트 정할 것 8건 추천대로: 상태값(환불됨 · 부분환불 · 환불중) · 조정 금액 5칸 · 결제 완료 = 거래 합계 vs 조정 금액 · 미수 · 과수 안 막음 · 부분 환불 = 계산값 기본 + 직원 수정 · 카드 총액 칸 없음 | 사용자 |
| 2026-11-18 | 결제 취소 ≠ 환불: 취소 = 결제 한 건 되돌림(구매 확정 유지 · 재결제) · 환불 = 구매 되돌림(항목 조정 · 회수) | 사용자 |
| 2026-11-18 | ERD v1 확정 → 메디니스 SPEC-000 · erd.md 까지 완주 · PR. 기준 = 상용 운영 중(더하기만 · 백필) · KOS 뗄 것(external_ref 만 · DAY 말 enum · DAY 가 직접 계산) | 사용자 |
| 2026-11-18 | 검수 판단 4: `purchase_item.count` = 회차(화면 수량 = 행 반복) · `etc_task_type` 도 만든다(04-1 그대로) · SPEC-000 version 0.0.1 유지(규칙) · 백필 의존은 OQ-00-3 | 코디(사용자 위임 「완주」) |
| 2026-11-19 | KOS 조사 계정 = **사용자 테스트 계정**(값은 `~/.config/day/kos-test-account.env` · 레포 금지). 데모 지점 시스템 계정은 DAY 서버 실사용 → 금지. 기기 제한 시 ` (research)` 표시 세션만 해제 | 사용자 |
| 2026-11-19 | ~~백필 이번 작업에 넣음~~ → **백필은 사용자가 직접 한다**(코디 오독 · 「내가 해야할거 같아서」= 사용자 본인). 만든 백필 코드는 `backfill-reference.patch`(→ CENTURION_DAY #261 로 옮김 · 파일 삭제) · `be-3-report.md` 참고로 남기고 PR 에서 뺌(visit 인덱스 포함). PR 에는 검수 4 WARN · 빈 본문 수정만. 방문 없는 고객 고객 목록 넣기 질문도 백필 몫 | 사용자 |
| 2026-11-19 | 백필 스크립트는 레포에 둔다(별도 PR · dev · 브랜치 `kknaksss/customer-erd-backfill` · visit 인덱스는 0011) — prod 도 같은 명령으로. dev 실행은 코디가 VM 에 패치 코드를 얹은 일회성 컨테이너로 진행(드라이런 → 실행) | 사용자 「백필 하라니까」 · 「스크립트로 올려야」 |
| 2026-11-19 | 백필 진행 순서 = 로컬 테스트 → dev 서버 드라이런 → 실행 · **dev 데이터 초기화 안 함**(새 테이블은 빈 채로 생기고 기존 테이블은 external_ref upsert) | 사용자 |
| 2026-11-19 | ~~백필은 다른 담당~~ → **이번 작업에 넣음**(사용자가 맡음): 수동 실행 스크립트 · KOS 1초 1회 · 내부 API 만(get-visitors · 일정 월 단위 · 고객별 시술권 · 카드) · 어제까지 · KOS_CLIENT_TAG=backfill 자기 세션만 해제 · 동기화 upsert 재사용 · 이어 하기 · --dry-run · visit 날짜 인덱스 · dev 배포 뒤 실행 · prod 는 밤에 나눠서 | 사용자 |
| 2026-11-19 | 기존 운영 코드도 공개 API 0 — 구역 목록 공개 → 내부 `schedule/zone/v1/queries/get-zones` · 공개 토큰 발급 없어짐 · open_api_key 필수는 그대로(후속 OQ) · 데모 시드 도구는 범위 밖 | 사용자 |
| 2026-11-19 | **공개 API 0**(비용): 새 동기화는 내부 API 만 · 진료항목/약품/기기 = 내부 get-products 안에서 모음(옵션에서 빠짐 ≠ 삭제) · **5분 회차 뺌**(오늘 밖 변경 = OQ-00-4 다시 열림 · 후보 내부 get-visitors 하루 훑기) · 기존 get-zones 공개 호출은 범위 밖 · `sync-fix-3-internal-only.md` | 사용자 |
| 2026-11-19 | 검수 3: 못 푼 티켓 Redis TTL 집합(무한 재조회 방지) · 오늘 구매 회차 별도 태스크 · schedule_sale except Exception · 5분 카드 id → ④ 직접 · 상한 시 시각 부분 전진 · `sync-fix-2.md` | 코디(사용자 「PR 까지」) |
| 2026-11-19 | 2단계 실물 발견: ledger 외부 id = chargingId:주머니 · 구성 title nullable · ticket canceled 추가 · **pendingItems 받음** · 선불카드 상품 닫힘 포함 두 번 조회 · 지난 시술권은 백필 몫 · `sync-fix-1.md` | 사용자 「나머지 진행 · PR 까지」 |
| 2026-11-19 | OQ-71 기본값: 담당자 없는 거래만 건너뛰고 셈(구매 · 항목은 씀) · 담당자 조회는 소프트 딜리트 staff 포함 · 건너뛴 수 구매 단위 카운트 · staff_id NOT NULL 유지 | 코디(backend 질문) |
| 2026-11-19 | 메뉴 키 보강(KOS 키 전수 대조 — search_phonetic_name · registered_at · cautions · target_country_codes · medicine_and_machine_names · drafted_at · prepaid translations) + ticket_bundle.purchase_item_id 부분 유일만 · 나머지 1:0..1 보류 · FK 인덱스 2단계 · visit_task 잠금 그대로 · `menu-keys-addition.md` | 사용자 「응」 |
| 2026-11-19 | 머지는 spec · code 한 번에 · Delivery Issue 발행 · DB 먼저(1단계 = 마이그레이션 · 모델 · enum, 2단계 = 동기화) | 사용자 |
| 2026-11-19 | 동기화 검수 판단 3 그대로: 5분 회차 구매 항목 통계 포함 · 시술 항목/기기/약물 = 공개 메뉴 API · REFUND → revoke | 코디(사용자 「추천으로」) |
| 2026-11-19 | 목표 = DB 먼저(마이그레이션 · 모델 · 동기화). 직원 동작 감사 로그(결제 · 환불 등)는 그 다음 — 기존 event_log · chart_log 는 이미 있음 | 사용자 |
| 2026-11-19 | 삭제 = 소프트 딜리트만(물리 삭제 금지) · ~~지울 때마다 `event_log` 한 줄~~ → 같은 날 뒤집음: 로그는 다른 데서 남김 · 삭제 로그 안 둠 | 사용자 |
| 2026-11-19 | 이번 작업 = 메디니스 문서(SPEC · WORK) + **코드 · DB 마이그레이션까지**. 코드 전 반드시 dev 최신 fetch | 사용자 |
| 2026-11-19 | 동기화 PR 범위 = 폴링 주기 · 원천 · 매핑 · upsert/삭제(+SPEC-000 칸). **백필은 다른 사람 담당** — OQ-00-3 열어 두고 주의 메모만 | 사용자 |
| 2026-11-19 | 동기화 정할 것 1~9 추천대로(바뀐 고객만 · 5분 병원 전체 증분 · 내부 원천 · 통계는 id 나열만 · 옵션 단위 칸 뺌 · 구성 참조 칸 뺌 · 전체 백필 · 지운 구매 포함) · 두 번째 테넌트 = 실 명동점 → 개발은 DEMO 만 | 사용자 |
| 2026-11-18 | 시술 외 품목 = `etcetera_product_category` · `etcetera_product`(이름 · 가격) · `item_type` 셋으로 닫힘 · 상품 탐색 = 시술 옵션과 같은 종류 | 사용자 · `수납추가.har` |
| 2026-11-18 | 티켓 가격 칸 없음 · 부분 환불 = 번들 ÷ 회차 × 쓴 횟수 → purchase_item 조정 금액 (b) | 사용자 |
| 2026-11-18 | 이름 treatment · treatment_item(피부과엔 「진료」 없음) · 작업 카드 = treatment_item_id + medicines · machines 스냅샷 | 사용자 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| backend | `term_bbe79944-22d5-4480-8435-1776c9ea2198` | — | — | be-1~3 | 완료 · 해제(컨텍스트 거의 참 · 터미널 유지) |
| backend(2) | `term_554e6a04-c9e4-4dca-a57b-f58be57e562a` | — | — | `customer-erd-be-4-brief.md` | 완료 · 해제 · `be-4-report.md` |
| reviewer | `term_899c29c1-703c-4f8e-8075-5087502b7b0e` | — | — | `customer-erd-review-brief.md` | 검수 1~5 PASS · 해제(터미널 유지) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/951 (`b3f99bab` · 브랜치 `kknaksss/customer-erd-spec`)
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/260 (`6b3223da`)
- 리포트: `har-check-report{,-2,-3}.md` · `spec-change-report.md` · `review-spec-report{,-2}.md`
- Delivery Issue: https://github.com/MediSolveAIDev/CENTURION_DAY/issues/259 (`cerd.v1.*` · plan_digest sha256:19b48a8f…)
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-11-19` 마감 시작 — 고객 이름 1곳 가림 · 회사 코드 패치 삭제(#261 로 옮김) · DEMO 컨테이너 · 임시 워크트리 정리 · SUMMARY 작성
- `2026-11-19` dev 백필 실행(748호출/759s · 오류 0) · run.env 삭제 → #261 스쿼시 머지 `844eace4` → deploy-dev 성공 · alembic 0011 · 인덱스 확인 · VM 임시 코드 삭제
- `2026-11-19` 검수 6 PASS(WARN 4 = 실행 수칙) → 백필 PR #261 · dev 드라이런(752호출/750s · 방문 1315 · 구매 447 · 시술권 429 · 카드 36) → 실제 실행 시작 · 이벤트가 = price.additional(수가 유형) dev DB 1행 확인
- `2026-11-19` dev 백필 드라이런 시작(VM `/opt/day-backfill` · 일회성 컨테이너 · run.env 600) · backend(2) 백필 스크립트 레포 PR 작업 발주
- `2026-11-19` CI pass → #260 · #952 스쿼시 머지 → deploy-dev 성공 · dev 로그(구역 2 · 메뉴 804/226/19/44 · 구매 5 · 오류 0) → #259 마감 댓글 · close
- `2026-11-19` backend 백필 분리(backfill-reference.patch 17파일 · 1831 passed) → code PR #260 · spec #952 추가 커밋 · 상호 링크
- `2026-11-19` reviewer 검수 5 PASS(WARN-1 빈 본문 일시 이상 시 그날 unresolved — 사용자 판단) · backend 컨텍스트 1% → 지시를 `backfill-split-instructions.md` 로 고정
- `2026-11-19` backend 3단계 백필 완료(DEMO 3회 · 지난 시술권 21→0) → 사용자 「백필 내가 한다」 → PR 에서 분리 · 참고 패치로 보관 지시
- `2026-11-19` reviewer 검수 4 PASS(WARN A~D · C 는 prod 첫 동기화 때 구역 수 확인) → backend 3단계 발주(A·B·D 같이)
- `2026-11-19` backend 검수 3 + 내부 API 만 반영(1825 passed · 공개 호출 0 · 코디 확인 180 passed) → reviewer 코드 검수 4
- `2026-11-19` 백필을 이번 작업 3단계로(스크립트 · 1초 1회) — 동기화 재검수 뒤 발주
- `2026-11-19` 사용자 「공개 api 비싸」 → 내부 API 만으로 전환 지시(backend · planner)
- `2026-11-19` 내부 고객 목록 `visitor/v2/queries/get-visitors`(페이지 · count) 발견 — 메인 reference/2026-10-23-cc-overall-board/har · 조사 4차가 놓침 → 내부 API 만으로 백필 가능 · OQ-00-3 메모 추가 지시
- `2026-11-19` reviewer 코드 검수 3 FAIL 1(못 푼 티켓 고객 10초 무한 재조회) · WARN 5 → backend · planner 반영 지시
- `2026-11-19` F-1~F-5 반영(planner · backend) · 1815 passed · 닫힌 상품 12 포함 20 · 구성 34 · 코디 확인 48 passed · DELETE 0 → reviewer 코드 검수 3
- `2026-11-19` backend 2단계 완료(1814 passed · DEMO 메뉴 건수 일치 · 판 해시 같음 · ref 2196) → 실물 발견 F-1~F-5 planner · backend 동시 지시
- `2026-11-19` 메뉴 키 보강(11칸 · 번들 유일) 재검수 PASS → backend 2단계 발주
- `2026-11-19` reviewer 코드 검수 1 PASS(WARN 4) · KOS 메뉴 키 대조 → 빠진 키 보강 planner · backend 동시 지시(0010 수정)
- `2026-11-19` backend 1단계 완료(migration 20261119_0010_sale_tables · 모델 5파일 · enum 4 · 범위 밖 kos_board 이름 · taut.toml) → reviewer 발주
- `2026-11-19` Delivery #259 발행(baseline main 4585fb59 ready · #952 먼저 머지 시 v2) · 승인 · backend 1단계 발주
- `2026-11-19` reviewer_doc 동기화 PASS(WARN 6) · W-1 수정 → mediness PR #952 (`4fe24e4b`)
- `2026-11-19` planner 2차 완료(SPEC-002 ㉔ · OQ-69~77 · 백필 제외 · 삭제 로그) · lint 0 error(코디 재실행) → reviewer_doc 발주
- `2026-11-19` 백필 영향 prod 코드 확인(판 = 오늘 창 · mark_absent 창 안 · 알림 없음 · visit 날짜 인덱스 없음) → planner 2차 발주(동기화 SPEC)
- `2026-11-19` mediness PR #951 스쿼시 머지 `4585fb59` (update-branch 뒤 ci-lint pass)
- `2026-11-19` researcher 4차 완료 — 공개 통계 6개로 병원 전체 백필 나열 가능 · 시술권은 내부 고객별 · 카드 이벤트 REFUND/BALANCE 실재 · 테스트 계정에 두 번째 테넌트 접근권(미호출) · 세션 해제 0 남음
- `2026-11-19` researcher 4차 발주 — 동기화 API · 백필 · 변경 감지 · 루프 붙이기 · 공개 API 대체
- `2026-11-18` reviewer_doc 재검수 PASS → mediness PR #951
- `2026-11-18` reviewer_doc FAIL 1(README 메뉴 줄) · WARN 6 · 판단 4 → 코디 추천값으로 정함(count=회차 · etc_task_type 만든다 · version 0.0.1 · OQ-00-3 백필 한 줄) → planner 수정 1차
- `2026-11-18` planner 완료 — SPEC-000 0.0.2 · 새 테이블 28 · visit_task 칸 3 · prod 변경 0 · lint 0 error(코디 재실행) → reviewer_doc 발주
- `2026-11-18` `수납추가.har` — 시술 외 품목 칸 · 상품 탐색 = PRODUCT_OPTION → 초안 반영
- `2026-11-18` 3차 정할 것 · 취소 ≠ 환불 정리 · `결제취소2.har`(취소 뒤 카드 그대로) → ERD 초안 v1
- `2026-11-18` researcher 3차 완료 — 환불 흐름 · adjustedPrice = 남는 금액 · round{5,1} · 카드 상품 환불 = 0 · 공유 owner:false · 워커 해제
- `2026-11-18` researcher 2차 완료 — KOS 다회권 N행 · 선불카드 상품 · 충전 이벤트 · 3차 발주(환불)
- `2026-11-18` researcher 완료 — 취소=음수 거래 · 재결제=같은 구매 · 선불=두 주머니 · 용량=스냅샷 덮어씀 · 티켓 행 수 미확인
- `2026-11-18` 작업 열기 · ERD 초안 v0 · researcher 발주

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
