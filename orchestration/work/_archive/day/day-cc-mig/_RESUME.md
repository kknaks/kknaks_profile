
# 재개 노트 — day-cc-mig (day)

**지금**: **마감(2026-11-22)** — #265 dev · mediness #954 머지 · Delivery #264 닫음 · dev 업데이트 · 회고 `para/projects/company/day/log/2026-11-20-day-cc-mig.md` · 개념 10 보강 · 아카이브
**다음**: 다음 작업(새 slug) = ext 이관 · 고도화 — 회고 §7 · 이 파일 §2 결정 · 조사 리포트 3개

세팅: `scripts/new-work.sh day day-cc-mig` · 설정 SSOT `config/projects/day.json`
코디handle: `term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/day-cc-mig-spec` (`kknaksss/day-cc-mig-spec` · #954) · delivery(detached ccede286): `…/mediness-mediness/day-cc-mig-delivery`
- 코드: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-cc-mig` (`kknaksss/day-cc-mig` · base origin/dev 844eace4)
- 코디 · researcher 공유: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig` (`kknaksss/day-cc-mig`)
- 읽기 전용 원천: cc-prototype `origin/main` 0553173 · CENTURION_DAY `origin/dev` 844eace4 · mediness `origin/main` products/day/


## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [x] 목록 밖 enum 9줄(URGENT · CANCELED · ONCE_PER_RESERVATION · 예약 규칙 이벤트 5) 0012 에 한 번에 추가 — backend 고침 1
- [ ] (2단계) E3 예약 생성 — DAY 에 예약 생성 기능 · KOS `reserve` 쓰기 없음(origin/dev `writes.py` 18행은 시술 현황 조작뿐). 열지 · 어떻게 열지 2단계에서 결정
- [ ] ext API 하나씩 값 점검(예: visit 상담사 · 원장 = 상담 차트 기준인가)
- [ ] 다음 작업으로 넘김: DAY 예약 현황 화면(이번 서비스 재사용) · KOS 수납 새 창 리다이렉트(수납 URL 캡처 · 결제 설정 저장 N8-6 · N8-8 포함) — ext 에는 수납이 없다(사용자 11-20 지적)
- [ ] baseline → decision → spec(mediness products/day/) → work — 사용자와 닫은 뒤 코드 발주
- [!] `day.medisolveai.com` = DAY prod(Caddy) 확인(리포트 B6) · prod 는 Swagger 꺼짐
- [ ] `CARD` 매핑 — 이 작업 범위(다음 배포)
- [x] HAR 추가 캡처 완료 7개(타이머 · 세션 관리 제외)
- [x] 병원 기본 휴무 확인(`병원휴무.har` · 코디 직접): **요일 체크 해제 = 기본 휴무** = `upsert-default-operation-timetable` 의 요일 `enabled:false` → `get-default-operation-timetable`(P26 · 키 이미 확보). 금요일 끄고 → 다시 켬(데모 원상복구 확인). `get-default-days-off` 는 그대로 빈 배열 → 화면 범례 「병원 특별 휴무」(날짜 지정)로 추정 · 미확인
- [!] 병원 특별 휴무(`get-default-days-off`): **KOS 웹에 입력 입구 없음(사용자 11-20)** → HAR 로 못 본다. 모양 근거는 cc 코드뿐 — `{id, startDateTime, endDateTime}`(cc `service/ext.py:833-842` · DEC-012 D-43 · 실물 근거인지 확인 안 됨). 코디 기본값: 이 세 키로 표를 두고 첫 실값에서 확인
- [x] 예약 그룹 휴무도 입구 없음(사용자 11-20) → 특별 휴무와 같게 처리(K1-2 #30 키 미관찰 · 첫 실값에서 확인). **HAR 캡처 종료**
- [!] 결제 수단 실측 한계(2026-11-20 사용자 · 화면 `reference/2026-11-20-day-cc-mig/2026-11-20-kos-payment-screen.png(기본 체크아웃 · 개인정보 · 커밋 안 함)`): KOS 수납 화면의 결제 수단 = **카드 · 현금 · 계좌이체 · 앱 결제 · 간편결제 · 선불카드** 6개 + 「결제 단말기로 결제하기 / 직접 입력」 + 현금영수증(자진발급). KOS 문자열 확인 = `CARD` · `CASH` · `TRANSFER` · `PREPAID_CARD` 넷. **앱 결제 · 간편결제의 KOS 문자열은 모름**(데모 결제 불가) — 지어내지 않는다. 같은 화면 경로 `get-payment-settings` · `initialize-purchase` · `add-pending-purchase-item` · `register-purchase` 는 다음 대조 후보
- [!] K6-13 KOS 생성 시각 — 코디 추천 created_at ← KOS(연동 기간 원장 = KOS) · 사용자 확인 대기
- [!] Swagger 로그인 방식 사용자 답 대기(리포트 C18 · C19)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-20 | 목표: cc-prototype ext 외부 연동 API 를 DAY 로 옮기고 고도화 | 사용자 |
| 2026-11-20 | 연동 담당자 안내 도메인 = `day.medisolveai.com` | 사용자 |
| 2026-11-20 | KOS 와의 통신은 DAY 만. 흐름 KOS → DAY → 각 서비스. 서비스는 결과를 DAY 에 주고, DAY 가 DB 갱신 후 KOS 동기화 | 사용자 |
| 2026-11-20 | ext 응답 값은 뜻이 맞는 출처여야 한다 — 예: visit 상담사 · 원장은 예약 · 접수 지정이 아니라 상담 차트 기록 | 사용자 |
| 2026-11-20 | Swagger 도 함께 이관 — 필드마다 뜻을 명확히(다른 개발자 요청) · 이번엔 Swagger 에 로그인 | 사용자 |
| 2026-11-20 | 「KOS 가 주는 키는 다 저장」(data_rules 11-03 재확인) — HAR 전수 대조로 DB 확장 범위를 정한다 | 사용자 |
| 2026-11-20 | 결제 수단 `CARD` 매핑을 이 작업에 넣는다 — 아직 운영 카드 결제 없음 · 다음 배포에 같이(핫픽스 아님) | 사용자 |
| 2026-11-20 | 미래 일정 동기화 필요 — **예약 현황 화면도 만든다** · 칸 정원은 병원 설정(예약 그룹 정원)에서 가져온다 (K6-6 · K6-7) | 사용자 |
| 2026-11-20 | 병원 설정(병원 정보 · 기본 운영 시간 · 휴무)은 KOS 값 그대로 DB 에 둔다 — S0:278 「phone · address 두지 않음」 뒤집음 (K6-8) | 사용자 |
| 2026-11-20 | 통화는 KOS 와 같게 — 금액마다 통화 (K6-16) | 사용자 |
| 2026-11-20 | 결제는 DAY 가 하지 않는다 — DAY 에서 KOS 수납 화면을 새 창으로 연다(리다이렉트). 결제 결과는 동기화로 받는다 | 사용자 |
| 2026-11-20 | 미래 일정은 미리 받지 않는다 — DAY 에서 그 날짜를 볼 때(예약 일정 넘김) 그날로 KOS 에 요청해 DB 를 최신화(받은 건 DB 에 저장). 오늘은 기존 10초 동기화 유지 (N8-1 · K6-6) | 사용자 |
| 2026-11-20 | KOS 「받아서 저장」 서비스 3개(날짜 하나 · 고객 하나의 미래 예약 · 예약 하나) — 서비스 로직은 하나, 입구만 내부(DAY 화면) · 외부(ext) 로 나눈다. 같은 대상 10초 안 재요청 안 함 · E6 는 고객 단위로 받아 저장 후 응답 | 사용자 |
| 2026-11-20 | **이번 작업(day-cc-mig) 범위 = ext 만.** DAY 예약 현황 화면은 다음 작업 — 서비스는 화면이 그대로 재사용할 수 있게 둔다 | 사용자 |
| 2026-11-20 | **범위 확정: ① ext API 이관 · 고도화(Swagger 필드 설명 · 로그인 포함) ② 테이블 보충(KOS 키 다 저장 — 칸 · 매퍼 · CARD 매핑).** 그 밖(예약 현황 화면 · 수납 리다이렉트 · 결제 설정)은 다음 작업 | 사용자 |
| 2026-11-20 | **순서: 1단계 테이블 보충(KOS 키 다 저장 — 데이터 먼저) → 2단계 ext 고도화.** 2차 K6 · 3차 N8 의 「다 저장」 기본값은 1단계 기준으로 확정 | 사용자 |
| 2026-11-20 | **정리: 테이블은 KOS 키 전부 다 채운다(2차 · 3차 후보 전체). 기능은 ext 13개만**(E3 예약 생성 포함) — 그 밖 기능(예약 현황 화면 · 수납 · 문진표)은 안 만든다. **이유: 테이블을 지금 다 만들어 두면 나중에 기능 붙일 때 마이그레이션이 준다.** 채우는 건 기존 KOS 동기화 회차 + 매퍼(화면 · 입력 기능 없음). 병원 정보는 `hospital`(brand 1 → hospital N · 병원 = KOS 테넌트)에 붙인다 | 사용자 |
| 2026-11-20 | 연동처(ext) 쓰기의 KOS 토큰 = **시스템 계정** (C6 · DAY-SPEC-001 규칙 4 의 ext 예외) | 사용자 |
| 2026-11-20 | 상태 · 종류 칸은 DAY enum — 관찰된 KOS 값만 정의, 모르는 값은 행 유지 · 그 칸 null + 동기화 경고(CARD 처럼 행째 빠지는 것 방지) · KOS `hospitalId` 는 `external_ref` | 검수 F2 · W1 → 코디 추천 · 사용자 승인 |
| 2026-11-20 | 1단계 진행 승인 · **기존 행 업데이트: 로컬 = 드라이런 → 실제 업데이트 · dev 배포 = 실제 업데이트** | 사용자 |
| 2026-11-20 | 로컬 실물 때 테스트 계정(kos-test-account.env) KOS 기기 제한 → 테스트 계정 세션은 워커가 오래된 것부터 필요한 만큼 해제해도 됨 | 사용자 「테스트 계정 줬잖아」 |
| 2026-11-20 | 이미 있는 행(prod 포함)의 `created_at` 도 KOS 생성 시각으로 덮어쓴다(OQ-4A-11 · 검수 W8) — 지금 코드 그대로 | 사용자 |
| 2026-11-20 | **ext 이관 · 고도화(2단계)는 다음 작업(새 slug)으로.** 이번 day-cc-mig = 테이블 보충(#264 · #265 · mediness #954)까지 — dev 실제 업데이트 확인 뒤 마감. 2단계 재료 = 조사 리포트 3개 · ext 결정 행(서비스 3개 · 입구 내부/외부 · 시스템 계정 토큰 · E3 · Swagger · 문진 health 빈 칸 · reservation_status_at) | 사용자 |
| 2026-11-20 | 문진은 이번 범위 밖 — 문진표 작업 때 `questionnaire_history` 동기화 · ext E8 `health` 를 채운다. 이번 E8 은 `health` 칸을 계약에 두되 비어 있음을 Swagger 에 밝힌다(코디 기본값 — charty 가 E8 사용) | 사용자 |
| 2026-11-20 | HAR 재캡처 = 휴무 둘(병원 기본 휴무 · 예약 그룹 휴무)만. 나머지 빈 키는 테이블 · 칸이 이미 있어 운영 값이 처음 나올 때 매퍼에서 확인 | 사용자 · 코디 정리 |
| 2026-11-20 | 시술 타이머 · 리액션은 KOS 것을 안 쓴다 → `taskTimers[]` · `reactions[]` 범위 밖 · KOS 에 로그인 세션 관리 화면 없음 | 사용자 |
| 2026-11-20 | (기본값 · 코디) 「다 저장」을 K6 원칙 묶음과 「일부러 안 둠」 54행에도 적용 — 사용자 이의 없으면 확정 | 2차 리포트 K6 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| researcher | `term_1b6a31fd-37a4-451d-904f-7a3ee6cfc348` | `task_82c51fdcd1c0` | `ctx_e5ce6d02e675` | `day-cc-mig-research-brief.md` | 완료 (run `run_b2f97043330c`) |
| researcher 2차 | `term_2a6739ed-9738-40ed-9da2-6e34838812e9` | `task_4072235a7191` | `ctx_d2b4ccb4dcae` | `day-cc-mig-research-2-brief.md` | 완료 |
| researcher 3차 | `term_749389fa-9664-4aac-990c-c765f0ea2c5a` | `task_a8b775f030b9` | `ctx_05a8aa0d8969` | `day-cc-mig-research-3-brief.md` (+ `research-3-add1-instructions.md`) | 완료 |
| reviewer | `term_eb269d60-3506-49e8-a774-8c76121da6dd` | `task_3fb98d136259` | `ctx_066265715bf0` | `day-cc-mig-review-brief.md` | 재검수 2 PASS |
| backend | `term_19c73ecd-4bec-48fa-8d75-eb86935ec90d` | `task_13fd64e7a461` | `ctx_74b2d552943f` | `day-cc-mig-be-brief.md` (워크트리 `CENTURION_DAY/day-cc-mig`) | 완료(고침 1 · 2) |
| reviewer_doc | `term_7db2ce1e-b152-4bfc-9263-4ee84d622668` | `task_a9b40a1f7c8c` | `ctx_cbbd9bb23d80` | `day-cc-mig-review-doc-brief.md` | 재검수 2 PASS |
| planner | `term_ec105a90-17de-4228-bf4d-18d2e4b1cef4` | `task_d3e3f0931059` | `ctx_7eea12ceca9e` | `day-cc-mig-spec-brief.md` (워크트리 `mediness-mediness/day-cc-mig-spec`) | #264 승인 반영 완료(delivery-plan:approved) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: mediness #954 머지 `e065e28e` (SPEC-000 §4A · ERD)
- Delivery: CENTURION_DAY#264 (key day/day-cc-mig-tables-2026-11-20 · v1 · plan_digest sha256:730db7fb…7262)
- code PR: CENTURION_DAY #265 → dev **squash 머지 f724b149** · Actions DAY dev 44705368388
- 리포트: `research-cc-ext-report.md` (완료) · 추가 지시 `research-add1-instructions.md`(Swagger D 절) · 2차 `research-kos-keys-report.md`(완료) · 3차 `research-kos-keys-3-report.md`(완료)

## 5. 이력 (최신이 위)

- `2026-11-22` mediness #954 머지 · #264 마감 댓글 · 워커 터미널 10 · 워크트리 3(spec · delivery · code) 정리 · HAR 9 + 결제 화면(개인정보)을 기본 체크아웃 `reference/2026-11-20-day-cc-mig/` 로 · 회고 · 개념 10 · 아카이브
- `2026-11-20` dev kos_keys 업데이트 완료(resume 뒤 재실행 일정 · 구매 · 시술권 · 카드 쓴 행 0) · DB 확인(고객 558 registered_at 558 · 방문 1338 group 1338 · 작업 886 긴급도 861 · 구매 항목 609 통화 609 · 약품/기기 참조 2271 · 병원 운영 시간 7 · 예약 규칙 2 · 이력 19) · 중간에 다른 세션 #266 dev 배포가 겹쳐 업데이트 중단 → 그 배포 취소됨 → resume
- `2026-11-20` #265 dev 머지 · 배포 성공 · dev kos_keys 실제 업데이트 시작
- `2026-11-20` #264 plan 승인(사용자) · backend 발주
- `2026-11-20` 재검수 2 PASS · mediness #954
- `2026-11-20` planner 완료(§4A · 새 표 12) · reviewer_doc 발주
- `2026-11-20` planner 발주(SPEC-000 테이블 보충)
- `2026-11-20` researcher 3차 완료 — 내부 경로에 칸별 예약 수 없음(정원 P03 + 점유 계산) · 수납 딥링크 미관찰 · 휴무류 여전히 빈 값
- `2026-11-20` researcher 3차 발주(새 HAR 7개)
- `2026-11-20` researcher 2차 완료 — 저장됨 769 · 미동기화 95 · 칸 없음 431 · 시점 다름 306 · 일부러 안 둠 54
- `2026-11-20` researcher 2차 발주(KOS 키 전수 · HAR)
- `2026-11-20` researcher 완료 — 리포트 696줄 · B1 있음51/가공65/없음26/시점다름9 · 정할 것 21
- `2026-11-20` 착수 · new-work.sh · researcher 조사 발주(사용자 승인)

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
