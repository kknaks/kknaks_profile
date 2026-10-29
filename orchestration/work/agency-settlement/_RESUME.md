# 재개 노트 — agency-settlement (agency-settlement)

**지금**: 재검수 WARN(FAIL 0 · 앞 판 전부 닫힘) → planner 수정 4판(W-1 첫 승인 달 구멍 3 · W-2) · 역할 문서 W-3 코디 수정 완료
**다음**: 4판 코디 확인(diff) → 사용자에게 SPEC 리뷰 → WP-BE · WP-FE 발주

세팅: 처음엔 `new-work.sh cc-prototype agency-settlement` 로 시작 → 10-29 별도 프로젝트로 옮김. 설정 SSOT **`config/projects/agency-settlement.json`** · 이후 브리프는 `new-work.sh agency-settlement agency-settlement --workers …`
문서: `para/projects/summer-star/agency-settlement/` · 코드: `kknaksss/agency-settlement`(private) · `/Users/kknaks/git/toy_pr2/agency-settlement`
코디handle: `term_d291ae3b-f96b-492e-8274-6c3e14da473f`

## 워크트리

- 코디(문서): `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터` · 브랜치 `kknaksss/kos-병원데이터`

## 1. 지금

- [ ] 사용자 결정 — 리포트 「정할 것」 10개(판정 필드 · 코드 집합 · 선불카드 · 손님 식별 노출 등)
- [!] **public 레포** — `research-agency-attribution.md` 에 실제 에이전시명 · 매출액이 있다(_RESUME 숫자는 지움). 커밋 전 사용자에게 어디에 둘지 확인
- [!] 운영 데이터 — 리포트 · 문서에 개인정보 금지. 원본은 ax-clinic-project gitignore 폴더/scratchpad 에만

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-10-29 | 에이전시 수수료 정산 PoC. 용도 = 병원·에이전시가 「N명 데려옴 · M명 결제 · 결제액 X」를 **서로 확인** | 사용자 지시 |
| 2026-10-29 | 데모 테넌트가 아니라 **운영 명동점 키(`KOS_API_tenent`) 조회 허용** — 조회만(`/queries/`), 개인정보는 집계로만. cc-prototype 의 「운영 키 금지」(kos-demo-api.md §1.2)는 이 작업 조사 단계에 한해 풀림 → **10-29 확장: 이 프로젝트 코드 · WP-LIVE 실물 조회까지 같은 조건(조회만 · 로컬만)** | 사용자 지시(「발주해서 조회만 하고 와바」 · 「운영지점을 봐야」 · 운영 결제로 리스트 페이지 만들자) — 검수 W-2 |
| 2026-10-29 | **에이전시 판정 = 고객의 「최초 유입 채널」(`visitorFunnelName`)**. 예약 유입 아님. 10월 시험 집계는 코디 scratch 에서만(public 레포라 숫자 안 남김) | 사용자 지시(KOS 고객 상세 화면) |
| 2026-10-29 | **1차 목표 = 결제 내역 리스트**(손님 이름 · 방문일 · 결제액 · 산 상품 · 최초 유입 채널). 수수료율(상품별로 다름)은 나중. 보여 주기는 리스트 위 필터로 | 사용자 지시 |
| 2026-10-29 | 원천: `getPurchaseItemStatistics`(품목 · 상품명 · `visitorFunnelName`, 10월 결제 392건 전부 품목 있음) + `getTransactionStatistics`(결제 · 취소) + 이름·방문일은 ~~`getScheduleDetail`~~ → **`findScheduleByPurchaseId`**(10-29 정정: 통계 행에 일정 id 없음 · 같은 일정 모양 · 일정 없으면 `getVisitor`) | 코디 확인(10-28 수집본) · 검수 W-1 · SPEC OQ-903 닫음 |
| 2026-10-29 | 기능 = **월별 매출 조회**(10월 · n월). 디자인 = cc-prototype(`procedure/front` 복사). 로컬만 | 사용자 지시 · 로컬은 코디 기본값 → DEC-001 |
| 2026-10-29 | **분할 결제가 달을 넘는 수납 = 품목 줄은 첫 승인 결제가 있는 달에만**, 다른 달엔 결제 · 취소 줄만(한 품목이 두 달에 전액으로 두 번 나오지 않게) | 코디 기본값 · 사용자에게 통보 — 검수 W-3 |
| 2026-10-29 | ⑤ `getPurchaseSummaries` 추가 승인(W-3 판정용 · 공개 `/queries/`) · **결제일 = ⑤ `transactions[].paymentDateTime.approvedDateTimeUtc`**(취소 줄은 `canceledDateTimeUtc`). `lastUpdatedPaymentDateTimeUtc` 안 씀 — OQ-904 닫음 | 코디 기본값 · 사용자 통보 — 「10월 리스트에 11월 날짜」 방지 |
| ~~2026-10-29~~ | ~~프로젝트는 cc-prototype 에 둔다(새 기능 폴더 `sales/`)~~ — **10-29 뒤집힘**: 「다른 프로젝트인데 cc 같은 거랬지」 | 코디 기본값 → 사용자 정정 |
| 2026-10-29 | **별도 프로젝트 `agency-settlement`** — 코드 레포 `kknaksss/agency-settlement`(private, 루트에 back/ · front/) · 문서 `para/projects/summer-star/agency-settlement/` · 디자인만 cc-prototype `procedure/front` 복사 | 사용자 지시 · 이름 · 레포 선택 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| researcher | `term_54222257-b51f-4f06-9268-dea87de55c5a` | `task_6df5377fd39b` | `ctx_fe12d7f76897` | `agency-settlement-research-brief.md` | 완료 · 검증 |
| planner | `term_d3e67a5e-3ebf-4410-b129-6e9c3058b7f3` | `task_48c52ffbf066` | `ctx_b997a8ea2b2d` | `agency-settlement-spec-brief.md` | 수정 1판 진행 |
| reviewer_doc | `term_35713e41-9a3a-45b1-b65c-235452e0d6d5` | `task_402f39febcfc` | `ctx_735141be6b83` | `agency-settlement-review-doc-brief.md` | 완료 FAIL → 재검수 대기 |

## 4. 산출물

- 리포트: `research-agency-attribution.md` (완료 · 10-01~10-28 운영 수집본 기준)

## 5. 이력 (최신이 위)

- `2026-10-29` reviewer_doc 재검수 WARN(F 0 · W 3) · roles W-3 코디 수정 · planner 수정 4판

- `2026-10-29` cc-prototype → 별도 프로젝트 agency-settlement(레포 생성 · config · roles · 문서 이동 · 번호 재부여) · planner 수정 3판

- `2026-10-29` reviewer_doc FAIL(F-1 400 NotFound) · WARN 6 → _RESUME §2 정정 · planner 수정 1판 발주

- `2026-10-29` planner 완료(SPEC-007 0.1.0 · WORK-011 · OQ 13) · 코디 grep 에이전시명 · 금액 0 · reviewer_doc 발주

- `2026-10-29` DEC-009 작성 · planner 발주(SPEC-007 · WORK-011)

- `2026-10-29` researcher 완료 — 에이전시는 funnel 코드 이름에만 · 결제 연결 끊김 0 · 코디 재계산 일치

- `2026-10-29` researcher 발주 — 운영 KOS 에이전시 유입 조사(조회만)
