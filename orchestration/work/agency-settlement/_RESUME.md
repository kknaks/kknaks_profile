# 재개 노트 — agency-settlement (agency-settlement)

**지금**: 코드 커밋 2b299dc · 코드 PR kknaksss/agency-settlement#1 · back(149 passed) 재시작 · 10월 ⚠ 0 · planner 0.4.3 동기 중
**다음**: 0.4.3 → 문서 커밋 · PR #114 갱신(조사 리포트 제외) · 사용자 화면 확인 · 마감은 사용자 지시 때

세팅: 처음엔 `new-work.sh cc-prototype agency-settlement` 로 시작 → 10-29 별도 프로젝트로 옮김. 설정 SSOT **`config/projects/agency-settlement.json`** · 이후 브리프는 `new-work.sh agency-settlement agency-settlement --workers …`
문서: `para/projects/summer-star/agency-settlement/` · 코드: `kknaksss/agency-settlement`(private) · `/Users/kknaks/git/toy_pr2/agency-settlement`
코디handle: `term_3605662c-607d-4c3e-8480-a4fdce8f45af`(10-29 바뀜)

## 워크트리

- 코디(문서): `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터` · 브랜치 `kknaksss/kos-병원데이터`

## 1. 지금

- [ ] 사용자 결정 — 리포트 「정할 것」 10개(판정 필드 · 코드 집합 · 선불카드 · 손님 식별 노출 등)
- [ ] 사용자 E2E 지적 기록(여기에 모은다): **⑤ 브라우저가 옛 2판 JS 로 「그달 결제 0」 표시 — front dev 재시작으로 해결 · Next dev 「1 Issue」 = AppHeader hydration mismatch(고칠 것)** · **① 좌우 폭이 너무 넓다 → 본문 최대 폭 1600px · 가운데(코디 기본값)** · **② 「그달 결제」가 승인 합(취소 안 뺌)이라 결제→취소→재결제 수납이 2A 으로 보임(실제 순액 A) → 머리 금액 = 순액(승인 + 취소 음수) 제안 · 순액이면 10월 ⚠ 결제≠품목 20 → 0** · **④ 사용자 핵심 지적(10-29): 「손님이 최종 뭘 얼마 결제했나 · 실제로 돈을 냈나」가 중요 — 취소 · 환불 품목은 취소선 + 「취소/환불」 + 0원, 수납 머리는 실결제 순액. 결제 흐름 줄 중심 화면을 품목 중심으로 바꾸는 제안 → 사용자 확인 중** · **③ 취소가 있는 수납은 승인 결제 줄도 보여야 흐름이 읽힘(지금은 취소 줄만) · 0원 구성품 줄이 부모 상품 위에 찍힘(순서)** · 코디 관찰 — 유입 채널 칸 좁아 줄바꿈 · 0원 품목 줄(묶음 구성품) 많음 · 승인≠품목 배지 20 수납(환불 · 예상대로) · `127.0.0.1:3800` 으로 열면 CORS 로 「back 연결 못함」(`localhost:3800` 만 허용 — code r1 실물 자리)
- [ ] WP-LIVE 뒤 planner 한 번에: SPEC §5.4(W-3 at 만 null · 잇기 유지) · §6.2 표(W-1) · §6.7 통화 0개(W-5) · §10.1 SALES_BACK_PORT 뜻(W-6) · 결제 수단 한글 이름(TRANSFER 등)
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
| 2026-10-29 | **시안 v1 채택**(「이 디자인으로 가자」) · 시안 위치는 `dda9a931` 그대로 → DEC-001 D-10 | 사용자 지시 |
| 2026-10-29 | **에이전트별 조회를 이번 판에** — 탭 「에이전시 전체」 + 에이전시마다 탭. 수수료는 다음 판 → D-11 | 사용자 지시 |
| 2026-10-29 | **SQLite 저장 · 다시 부르지 않기** — 지난 달(확정) = 한 번 받으면 다시 안 부름 · 이번 달 = 마지막으로 받은 시각 이후만(겹침 여유) · 메모리 캐시(OQ-105) 대체 → D-12 | 사용자 지시 — 「9월에 이미 확정 난 건데 왜 또 불러와」 · 「10월은 마지막 이후로만」 |
| 2026-10-29 | 저장 뒤 화면 상태 = **받은 시점 기준**(지난 달 품목 배지가 나중 환불로 안 바뀜 · 환불 돈은 취소 행) · [전체 다시 받기]는 사람이 누를 때만 → D-13 | 코디 기본값 · 사용자 통보 |
| 2026-10-29 | **시안 v2 채택** · 시안 정할 것: 탭 목록 = 그 달에 나온 에이전시만 · 탭 글자 「(에이전시)」 뗌(시안대로) · [전체 다시 받기] = 이번 달에도 작게 · 확인 1번 · 「새로 받음」 배지 = 다음 받기 전까지 · 0건 = 「새 결제 없음 · HH:MM 확인」 · 나머지 = 시안 v2 값 | 사용자 「응 그렇게 가자」 · 코디 기본값 |
| 2026-10-29 | **엑셀 내보내기를 이번 판에** — 지금 보는 화면(월 + 탭) 그대로 · 품목 한 줄씩 펼친 xlsx(결제일 · 손님 이름 · 방문일 · 최초 유입 채널 · 수납 · 품목 종류 · 상품 · 옵션 · 품목 금액 · 상태 · 결제 수단) · back 이 SQLite 에서 만든다(KOS 0) · 버튼 툴바 오른쪽 → D-14 | 사용자 지시 · 형식 · 위치는 코디 기본값 |
| 2026-10-29 | **손님 셈 = KOS 손님 id(`visitorId`) 기준** — 동명이인을 하나로 세지 않는다. 시안 v2 · SPEC 0.3.0 OQ-126 의 「이름 기준」을 뒤집음. 손님 id 가 없으면 수납 id | 사용자 지시 — 「동명이인 같이 세면 안 되지 · 손님 기준으로」 |
| 2026-10-29 | **결제 손님 = 결제 0원 · 순액 0 이하 손님도 포함**(OQ-126 닫음) | 사용자 지시(planner 에 직접) — 「결제 0 원도 일단 포함해」 |
| 2026-10-29 | **엑셀 손님 이름은 가리지 않는다**(OQ-130 닫음) | 사용자 지시(planner 에 직접) — 「엑셀 이름 가리지마」 |
| 2026-10-29 | 증분 해석(OQ-123): ① 은 이번 달 전체 1회 · 새 행만 골라 비싼 조회(②③④⑤)는 새 것만 — doc r3 F-2(같은 수단 · 금액 새 거래 버려짐) 때문 | 코디 판단 · 사용자 통보 |
| 2026-10-29 | **품목 중심 · 실결제 화면**(→ D-18): 수납 머리 = 실결제(승인 − 취소 · 환불 순액) · 품목 줄 = 결제 완료 / 환불(취소선 · 「환불」 · 0원 · 원래 금액 회색) / 부분 환불(남은 금액 — 조사 뒤) · **취소된 결제는 취소선 한 줄로만**(승인 + 그 취소를 한 줄 「~~10:56 간편결제 B~~ 취소」) · 살아 있는 승인 결제 줄은 안 보임(실결제에 들어감) · ⚠ 결제≠품목 = 실결제 vs 품목 합 · 0원 구성품은 부모 아래. 취소된 결제의 품목 구성은 공개 API 에 없음(KOS 웹 확인 대기) | 사용자 지시 — 「최종 뭘 얼마 결제했나 · 실제로 돈을 냈나」 · 「취소는 삭선으로 취소된 것만 보여줘」 |
| 2026-10-29 | **D-18 정정 — 최종 결제만 보인다.** 화면 · 엑셀 = 손님이 **최종적으로 어떤 상품을 얼마 냈나**. 취소된 결제 · 전액 환불 품목은 **보이지 않는다**(취소선 줄도 없음). 부분 환불 품목 = 남은 금액만. 수납 머리 = 실결제. 취소 · 환불 건수는 숫자로만(건수 줄 · 「정보」 시트) | 사용자 지시 — 「최종 얼마를 병원에 냈는지가 중요」 · 「어떤 상품을 얼마 냈는지가 · 최종적으로 취소된 거는 필요 없잖아」 |
| 2026-10-29 | OQ-136 = 시안 v3 안 만든다 · SPEC 0.4.0 대로 구현 · 구현본이 정본 | 코디 판단 |
| 2026-10-29 | OQ-132 · r5 F-2 = **앞 달 결제의 이 달 취소는 이 달 화면 · 합 · 엑셀에 음수로**(머리 「실결제 −X」 · 품목 줄 없음 · 「앞 달 결제 취소」). 합 기준 = 품목 실결제 합 + 그 음수 — 화면 · 에이전시 합 · 엑셀이 같은 숫자. 전액 환불로 실결제 0 · 품목 0 인 수납은 머리도 안 보임 | 코디 기본값(추천안) · 사용자에게 두 번 물음 · 답 대기 — 답 오면 고침 |
| 2026-10-29 | 원칙 = **달을 모두 더하면 KOS 최종 금액**. 품목이 다른 달인 수납에 이 달 취소가 있으면 이 달 승인도 더한다(부분 취소 뒤 다른 금액 재승인) · 취소 없는 분할 결제 나머지는 더하지 않는다. 운영 9 · 10월 이 꼴 0 건 | 코디 판단(backend 제안 채택) |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| backend BE3 | `term_c299b474-0715-4348-9ac5-d608f7e3c1b8` | `task_bfec689910a1` | `ctx_d49b314c82db` | `agency-settlement-wp-be3-brief.md` | 완료 · pytest 144 코디 재확인 |
| frontend FE3 | `term_484b0e2e-f6c6-4826-b1af-3fc52ac95bd1` | `task_5738dd8b72bc` | `ctx_cd2ccc067f44` | `agency-settlement-wp-fe3-brief.md` | 완료 · 코디 tsc · `wp-fe3-report.md` · `shots-fe3/` |
| backend BE2 | `term_c299b474-0715-4348-9ac5-d608f7e3c1b8` | `task_8b4921e65716` | `ctx_35f65aaba85e` | `agency-settlement-be2-brief.md` | 완료 · pytest 119 코디 재확인 |
| reviewer code r2 | `term_11ad2b32-9c65-4c6c-93a8-72602ed59884` | `task_2888b97babce` | `ctx_a12414ed947f` | `agency-settlement-review2-brief.md` | 완료 FAIL · `review-code-r2-report.md` |
| frontend FE2 | `term_484b0e2e-f6c6-4826-b1af-3fc52ac95bd1` | `task_07fa5caf328d` | `ctx_87e31a4e67d5` | `agency-settlement-fe2-brief.md` | 수정 1 완료(F-1 · 1600) · 완료 · 코디 tsc · 스크린샷 확인 · `wp-fe2-report.md` · `shots-fe2/` |
| design-v2 | `term_484b0e2e-f6c6-4826-b1af-3fc52ac95bd1` | `task_0e77f034c7c2` | `ctx_7f1dc78c5aa4` | `agency-settlement-design-v2-brief.md` | 완료 · 업로드 75→76 · `design-v2-report.md` |
| spec-v3 | `term_53ce52e0-0768-4aa5-ad16-a1fb4e218878` | `task_62b039e32c5a` | `ctx_73bc031ba111` | `agency-settlement-spec-v3-brief.md` | 완료 0.3.0 |
| reviewer_doc r3 | `term_4a895e68-c8ca-47a9-bc70-df5bc885a07d` | `task_c12ade33a2e0` | `ctx_872a684696a0` | `agency-settlement-review-doc-r3-brief.md` | r4 완료 WARN · `review-doc-r4-report.md` |
| backend | `term_3d2cc1cd-35b6-44d5-a4ba-c91f1360fc67` | `task_968a47fe0e75` | `ctx_d4d15032f3ee` | `agency-settlement-be-brief.md` | 수정 1판 완료 · pytest 67 코디 재확인 |
| reviewer | `term_c40823c2-59cf-42d8-8c37-0351f93b7267` | `task_e6aa7d9ba34f` | `ctx_1843e9246de9` | `agency-settlement-review-brief.md` | 완료 WARN · `review-code-r1-report.md` |
| frontend | `term_eb595f4c-ebea-448b-b27d-7137f208d9e5` | `task_45dedea6ea07` | `ctx_e651c711574d` | `agency-settlement-fe-brief.md` | 완료 → 시안 발주 `task_0106b51884b8` / `ctx_538a7f1ccb72` | 이전: 완료 · 코디 tsc 확인 · 리포트 `wp-fe-report.md` · 스크린샷 `shots-fe/` |
| researcher | `term_54222257-b51f-4f06-9268-dea87de55c5a` | `task_6df5377fd39b` | `ctx_fe12d7f76897` | `agency-settlement-research-brief.md` | 완료 · 검증 |
| planner | `term_d3e67a5e-3ebf-4410-b129-6e9c3058b7f3` | `task_48c52ffbf066` | `ctx_b997a8ea2b2d` | `agency-settlement-spec-brief.md` | 수정 1판 진행 |
| reviewer_doc | `term_35713e41-9a3a-45b1-b65c-235452e0d6d5` | `task_402f39febcfc` | `ctx_735141be6b83` | `agency-settlement-review-doc-brief.md` | 완료 FAIL → 재검수 대기 |

## 4. 산출물

- 코드 PR: https://github.com/kknaksss/agency-settlement/pull/1 (2b299dc)

- 문서 PR: https://github.com/kknaks/kknaks_profile/pull/114
- 코드 워크트리: `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement`(브랜치는 new-work.sh 기본)

- 리포트: `research-agency-attribution.md` (완료 · 10-01~10-28 운영 수집본 기준)

## 5. 이력 (최신이 위)

- `2026-10-29` BE3 수정 2(pytest 149) · back 재시작 · 코드 커밋 · PR #1 · 스키마 백업 파일 지움 · planner 0.4.3 동기 발주

- `2026-10-29` FE3 수정 1 완료(차례 = back · 앞 달 결제 취소 글자 · itemsNowhere 안 숨김 · hydration = hot reload 옛 JS) · 코디 tsc 확인 · BE3 수정 2 대기

- `2026-10-29` BE3 수정 1 완료(pytest 148 코디 재확인) · 수정 2 발주(부분 취소 뒤 재승인)

- `2026-10-29` code r3 FAIL 1 · W 2 → BE · FE 수정 1 발주(착수 확인)

- `2026-10-29` 사용자 화면이 옛 front 번들(그달 결제 0) → 3800 dev 재시작 · 코디 스크린샷으로 3판 확인(SQ 탭 실결제 〈금액4〉 · 〈금액2〉 · 〈금액3〉 · 합 〈금액1〉)

- `2026-10-29` LIVE3 일부: 10월 KOS 0 · ⚠ 0 · 숨김 14 · 반영된 취소 3 · refresh=new 2 calls · 9월 KOS 0 · ⚠ 1 · 접근 로그 agency= 0 · code r3 발주

- `2026-10-29` WP-FE3 완료(스크린샷 12) · 3800 hot reload 로 이미 3판 — 8800 은 2판 back 이라 BE3 전까지 화면 깨질 수 있음

- `2026-10-29` SPEC 0.4.2 · BE3 ∥ FE3 발주(착수 확인)

- `2026-10-29` SPEC 0.4.1 · r6 FAIL 1 · W 5 → planner 0.4.2

- `2026-10-29` SPEC 0.4.0 완료 · r5 발주(task_6a82861b163a · reviewer_doc term_a11a90d7)

- `2026-10-29` BE 수정 1(pytest 122) · back 재시작(재시작 뒤 10월 KOS 0) · LIVE2 일부: 9월 첫 받기 full 657 calls 5.2s · state closed · 다시 열기 · refresh=new 모두 KOS 0 · 엑셀 3종 200(11칸 · datetime/int 셀 · 수식 0) · 접근 로그 agency= 0

- `2026-10-29` 수정 1 발주가 stale 핸들로 가서 유실 → 새 핸들(FE 484b0e2e · BE c299b474)로 다시 보냄 · 둘 다 착수 확인

- `2026-10-29` code r2 FAIL(F-1) · WARN 3 → FE · BE 수정 1 발주

- `2026-10-29` back 8800 2판으로 재시작(사용자 「리뷰 동안 보면 안 되나」) · 10월 첫 받기 full 405 calls 5s · 다시 열기 KOS 0 · 0.04s · 새 결제 받기 incremental 1 call · back/data/sales.sqlite3 (600) · front 3800 은 dev hot reload 로 이미 2판

- `2026-10-29` WP-BE2 완료(pytest 119) · REVIEW2 발주

- `2026-10-29` WP-FE2 완료(시안 v2 · 스크린샷 19) · 결제 수단 이름 7개 BE2 에 중계

- `2026-10-29` doc r4 WARN(F 0) · D-12 근거 보강 · WP-BE2 ∥ WP-FE2 발주

- `2026-10-29` SPEC 0.3.1 완료 · r4 재검수 발주

- `2026-10-29` doc r3 FAIL(F 3 · W 8) → planner 0.3.1

- `2026-10-29` SPEC 0.3.0 완료(OQ-122~131) · reviewer_doc r3 발주

- `2026-10-29` 시안 v2 업로드(sha 4dd74543… · 12장면) · 사용자 확인 대기 · 시안 정할 것 4 은 코디 기본값으로 통보

- `2026-10-29` 시안 v1 채택 · D-10~D-13 · 시안 v2(에이전시 탭) ∥ SPEC 0.3.0 발주(옛 frontend · planner 터미널 사라짐 → 새로 띄움)

- `2026-10-29` 시안 v1 업로드 완료(sha256 62d318e3…)

- `2026-10-29` 시안 로컬 사본 완료(업로드 보류 — 도구 규칙) → 사용자 「어 올려」 → 업로드 지시(`design-upload-instructions.md`)

- `2026-10-29` WP-LIVE — 운영 키 back/.env(gitignore · 600) · 10월 조회 성공 · 화면 확인(실명 스크린샷은 scratchpad 에만)

- `2026-10-29` WP-BE 완료(pytest 63 · 코디 재확인) · WP-REVIEW 발주

- `2026-10-29` WP-FE 완료(tsc · lint · build 0 · 스크린샷 7) · 코디 tsc 재확인

- `2026-10-29` 문서 커밋 41212d25 · PR #114 · 코드 워크트리 · WP-BE ∥ WP-FE 발주

- `2026-10-29` reviewer_doc 재검수 WARN(F 0 · W 3) · roles W-3 코디 수정 · planner 수정 4판

- `2026-10-29` cc-prototype → 별도 프로젝트 agency-settlement(레포 생성 · config · roles · 문서 이동 · 번호 재부여) · planner 수정 3판

- `2026-10-29` reviewer_doc FAIL(F-1 400 NotFound) · WARN 6 → _RESUME §2 정정 · planner 수정 1판 발주

- `2026-10-29` planner 완료(SPEC-007 0.1.0 · WORK-011 · OQ 13) · 코디 grep 에이전시명 · 금액 0 · reviewer_doc 발주

- `2026-10-29` DEC-009 작성 · planner 발주(SPEC-007 · WORK-011)

- `2026-10-29` researcher 완료 — 에이전시는 funnel 코드 이름에만 · 결제 연결 끊김 0 · 코디 재계산 일치

- `2026-10-29` researcher 발주 — 운영 KOS 에이전시 유입 조사(조회만)
