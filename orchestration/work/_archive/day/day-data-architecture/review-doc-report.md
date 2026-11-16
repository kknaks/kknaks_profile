# 리뷰 리포트 — day-data-architecture / doc (2026-11-03)

검수 대상: `mediness-mediness/day-data-architecture-spec` 의 `products/day/` 전부(untracked · 미커밋).
정답지: `kknaks_profile/day/reference/2026-11-03-cc-day/erd/` 9개 파일(아래 「원천」). 경로는 줄 번호까지 적었다.
방법: 원천 9개 파일과 SPEC-000 의 해당 절을 **줄 순서까지 diff** 했다(헤딩 단계만 정규화). 표 행 수와 테이블 수는 내가 직접 다시 셌다. 그다음 SPEC 의 머리 · 메타 · 읽는 법 · §6 OQ와 README · 40-architecture · 10-decision · log · 20-spec.md · 30-work.md 를 원천과 손으로 대조했다.

## 판정: FAIL

표 내용을 옮긴 것은 깨끗하다. 원천의 모든 표 행이 같은 순서 · 같은 글자로 들어 있다(누락 0 · 칸 단위 왜곡 0). 그런데 planner 가 SPEC 머리에 새로 쓴 **「표 읽는 법」 두 줄이 원천에 없는 해석 규칙**이다. 이 규칙대로 읽으면 칸 계약이 바뀐다(FAIL 2건). 둘 다 문장 몇 줄만 고치면 풀린다.

---

## FAIL

### F1. 「묶은 행 = 같은 필수 여부」 규칙을 발명했다. 그대로 읽으면 `deleted_at` 이 NOT NULL 이 된다(§2 와 모순)

- 위치: `products/day/20-spec/spec-000-data-model.md:77` (「한 줄에 여러 칸을 묶은 행은 각 칸이 같은 타입 · 필수 여부를 가진다」), `:74` (「필수 ✓ = NOT NULL」)
- 영향받는 행: `| created_at · updated_at · deleted_at | timestamptz | ✓ |` 형태 **42행**(1차 33 · 04-1 메뉴 9). 예: `spec-000-data-model.md:425, 519, 637, 762, 815, 989, 1011, 1055, 1143` …
- 근거(원천):
  - 원천에는 「필수」의 뜻이나 묶은 행을 읽는 법을 정한 곳이 없다(`erd/README.md:40-56` 공통 규칙 전체).
  - `erd/README.md:56` 「모든 테이블에 `deleted_at`(timestamptz, **null = 살아 있음**)」.
  - 칸을 따로 적은 표에서는 `deleted_at` 의 필수 칸이 비어 있다. `erd/01-hospital.md:22, 33, 47`, `erd/02-customer.md:50`.
- 문제: SPEC 이 F1 규칙을 더하는 바람에 묶은 42행의 `deleted_at` 이 NOT NULL 로 읽힌다. 그러면 §2 「삭제」(`spec-000-data-model.md:99`)와 정면으로 부딪친다. BE 워커가 이 SPEC 으로 migration 을 쓰면 살아 있는 행을 만들 수 없다. 원천의 묶은 행 자체는 모호하다(원천 쪽 모호함). 그 모호함을 잘못된 쪽으로 닫은 것은 옮기는 과정의 발명이다.
- 고칠 방향: `:77` 을 지우거나 「묶은 행의 `deleted_at` 은 §2 「삭제」에 따라 NULL 허용」으로 바꾼다. 묶은 행을 어떻게 읽을지 정하는 것은 OQ 로 올려도 된다. `:74` 의 NOT NULL 정의도 원천에는 없다. 남기려면 「§2 가 우선」을 함께 적는다.

### F2. 「타입 `—` 인 칸 = 만들지 않는다」 규칙을 발명했다. 원천이 1차에 두라고 한 상담 시술 · 지정 의사 연결이 막힌다

- 위치: `spec-000-data-model.md:76` (「타입이 `—` 인 칸 = 아직 테이블 칸으로 정하지 않은 것 … **만들지 않는다**」), `:1196` (「타입 `—` 이면 만들지 않음」), OQ `:1214` (OQ-03-2) · `:1238` (OQ-06-1)
- 근거(원천):
  - 원천에서 타입이 `—` 인 칸은 뜻이 서로 다르다. 보류(`erd/03-visit.md:52-54` + `:130`), 다른 곳으로 보냄(`erd/06-room.md:89-92`, `erd/04-1-menu.md:163-165`), 구조로 푼다고 정한 것(아래 둘)이 섞여 있다.
  - `consultation.procedures` (`erd/03-visit.md:87`) — 「시술 개념 셋」(`erd/03-visit.md:112`)은 `consultation_procedure`(상담 1 : N, 참조 + 이름 · 가격 스냅샷)로 그린다. `erd/04-1-menu.md:5-6` 은 「1차는 … 작업 · 희망 시술 · **상담 시술**에 … 스냅샷으로만 적는다」고 한다. 1차에 상담 시술 스냅샷을 **둔다**는 뜻이다.
  - `visit_occupied_resource.doctor_ids` (`erd/06-room.md:82`) — 「있으면 `visit_occupied_resource_doctor`(N:M)」. 06 은 열린 것이 없는 「정함」이다(`erd/README.md:37`, 06 에는 정할 것 절이 없다).
- 문제: 원천에 없는 정책(「만들지 않는다」)이 들어갔다. 그 결과 원천이 1차에 두라고 한 상담 시술 스냅샷과, 정해 둔 지정 의사 N:M 이 닫혔다. 그리고 06 에서 닫힌 항목이 OQ-06-1 로 다시 열렸다(rules 「닫힌 것을 다시 연 곳」).
- 고칠 방향: `:76` · `:1196` 의 「만들지 않는다」를 빼고 원천 표기(보류 / 다른 곳으로 / 연결 테이블로)를 그대로 쓴다. OQ-03-2 · OQ-06-1 은 「결정」이 아니라 「원천에 칸 표가 없다 — 칸 표가 필요하다」로 고친다(원천 쪽 빈칸을 코디 · 사용자에게 넘긴다). OQ-06-1 은 「06 은 정함이고 칸 표만 비었다」고 함께 적는다.

---

## WARN

### W1. SPEC 안의 상대 링크 8개가 깨졌다
- `spec-000-data-model.md:61-68` — 「주제와 상태」 표의 `[01-hospital.md](01-hospital.md)` ~ `[07-misc.md](07-misc.md)`. `products/day/20-spec/` 아래에 그런 파일이 없다.
- 근거: 원천 `erd/README.md:31-38` 을 그대로 붙였다. planner 리포트는 원천 링크를 `§2` 로 바꿨다고 했는데 이 표는 빠졌다. lint 는 잡지 않는다(검사 항목에 없다).
- 방향: 링크를 `§3 01` 같은 절 앵커로 바꾸거나 링크 없이 파일 이름만 둔다.

### W2. DAY-ESC-001 의 칸 값은 planner 가 고른 값이다
- `products/day/10-decision.md:34` — 긴급도 `mid` · 결정레벨 `경영지원` · 보고방법 `mediness` · 담당자 `기획`.
- 근거: 원천은 「법적 검토 필요(cc 표시 그대로)」 한 줄뿐이다(`erd/07-misc.md:14`). 형식(8칸 · ID 3자리 · `## 미완료`)은 규칙을 지킨다.
- 방향: 코디 · 사용자가 값을 맞춘다(planner 미결 8 과 같은 항목).

### W3. log 의 PR 칸이 `N/A`
- `products/day/log.md:17-19`. 규칙상 PR 칸은 「`#NNN` 또는 닿는 링크, 모호한 단어 단독 금지」(`rules/document-pipeline.md` §log.md). PR 을 올릴 때 번호로 채워야 한다.

### W4. 03 의 상태 표기가 엇갈린다(원천 쪽 — 그대로 옮김)
- `spec-000-data-model.md:63` 「정함(2026-11-03)」과 `:353` 「사용자와 정하는 중」이 한 문서에 함께 있다.
- 근거: `erd/README.md:33` vs `erd/03-visit.md:3`. 옮긴 것은 맞다. 다만 읽는 사람이 어느 쪽인지 모른다 → 코디 확인 필요.

---

## 주제별 개수 대조표 (리뷰어가 직접 셈)

「행」은 표 데이터 행(머리줄 · 구분줄 제외)이다. 「테이블」은 원천이 정의한 DB 테이블 수다(묶은 헤딩 `machine · medicine` 같은 것은 2개로 셌다).

| 주제 | 원천 파일 | 테이블(원천) | 테이블(SPEC) | 표 수 원천 / SPEC | 표 데이터 행 원천 / SPEC | 줄 순서 diff |
|---|---|---|---|---|---|---|
| 공통 | `erd/README.md:27-56` | — | — | 2 / 2 | 21 / 21 | 동일 |
| 01 | `erd/01-hospital.md` | 3 | 3 | 6 / 6 | 31 / 31 | 동일 (정할 것 → §6, phone · address 문장 → `#### 두지 않는 칸`) |
| 02 | `erd/02-customer.md` | 7 (`customer` · `external_ref` · 코드 5) | 7 | 5 / 5 | 60 / 60 | 동일 (README 참조 2곳 → §2 로 바꿈 · 내용 같음) |
| 03 | `erd/03-visit.md` | 4 | 4 | 4 / 4 | 57 / 57 | 동일 (논의 중 → `#### 예약 그룹` + §6) |
| 04 | `erd/04-staff.md` | 7 | 7 | 8 / 8 | 48 / 48 | 동일 |
| 05 | `erd/05-task.md` | 9 | 9 | 10 / 10 | 72 / 72 | 동일 |
| 06 | `erd/06-room.md` | 6 | 6 | 7 / 7 | 38 / 38 | 동일 |
| 07 | `erd/07-misc.md` | 13 | 13 | 13 / 13 | 104 / 104 | 동일 (법적 검토 줄 끝 `→ DAY-ESC-001` 추가) |
| 04-1 (1차 밖) | `erd/04-1-menu.md` | 13 | 13 | 12 / 12 | 81 / 81 | 동일 |
| 합계 | | 1차 49 + 메뉴 13 | 49 + 13 | 67 / 67 | 512 / 512 | |

- 표 바깥 본문 줄도 diff 했다. 다른 곳은 위 괄호 안 항목과 검토표(claude.ai) 링크 제거뿐이다.
- 관계도: 원천 `erd/README.md:64-134` 의 관계 71개 = `40-architecture/erd.md` 1차 62(`:22-83`) + 메뉴 9(`:92-100`). 누락 · 추가 0.
- erd 인벤토리 「핵심 키」 49행을 원천 PK · UNIQUE · 제약 줄과 대조했다(`erd/02-customer.md:77, 102`, `erd/05-task.md:54, 73, 100`, `erd/06-room.md:59, 67`, `erd/07-misc.md:23, 47, 131, 142, 155, 160` 등). 전부 일치한다. 칸 전체 목록은 없다(규칙 준수).
- planner 리포트의 숫자(67 · 512 · 49 + 13)는 실물과 같다.

## 「보류 · 1차 밖 · 범위 밖 · 바로 적용」 표시

| 표시 | 원천 | SPEC | 결과 |
|---|---|---|---|
| 04-1 1차에서 만들지 않음 | `erd/README.md:35`, `erd/04-1-menu.md:5-6` | `spec-000:65, 1017, 1025` · `erd.md:86` · arch README `:36` · 20-spec.md `:34` | 살아 있음 |
| 03 보류(수납 · 처방전 · 반응) | `erd/03-visit.md:130` | OQ-03-1 `:1213` | 살아 있음 |
| 04-1 범위 밖(기타 상품 · 선불카드 …) | `erd/04-1-menu.md:176` | `:1230` | 살아 있음 |
| 07 바로 적용 — 검토는 이후 | `erd/README.md:38`, `erd/07-misc.md:3` | `:68, 828, 830` · OQ-07-3 `:1244` | 살아 있음 |

## 열린 것 → OQ

원천의 「정할 것 · 확인할 것 · 논의 중 · 보류」와 본문 속 「확인할 것」은 **전부** §6 에 있다. 결정된 것처럼 쓴 곳은 없다.
README 소켓 → OQ-00-1 · 01 Vegas → OQ-01-1 · 02 `:147` → OQ-02-1 · 02 `:138` → OQ-02-2 · 03 `:130` → OQ-03-1 · 03 `:128` → (해결) · 04 `:109-110` → OQ-04-1 · 2 · 04-1 `:169-176` → OQ-041-1~6 + 범위 밖 · 05 `:144` → OQ-05-1 · 07 `:14` → OQ-07-1(+ESC) · 07 `:15` → OQ-07-2 · 07 상태 → OQ-07-3.
초과분: OQ-03-2 · OQ-06-1 은 원천에 「정할 것」으로 적힌 항목이 아니다. planner 가 타입 `—` 칸에서 끌어올린 것이다 → F2.

## 문서 규칙

- lint: `python3 scripts/lint-pipeline.py --strict` 1회 → **exit 0 · 0 error · 263 warning**. `products/day/` 범위는 ERROR 0 · WARN 0이다. 263 WARN 은 전부 타 제품(selly 등)의 기존 경고라 **무관**하다.
- frontmatter: SPEC `id · doc_no(DAY-DOC-4) · type · title · status draft · owner TBD · last_updated · version · sources` 를 모두 갖췄다. 10-decision · 20-spec.md · 30-work.md 의 doc_no 는 DAY-DOC-1~3 이고 서로 겹치지 않는다.
- 미러: 20-spec.md SPEC List ↔ SPEC 파일, 30-work.md Spec Coverage ↔ SPEC 이 맞는다(lint 통과).
- ESC 형식: 8칸 · `## 미완료` · `## 로그` 를 갖췄다. SPEC 쪽은 참조만 한다(`spec-000:36, 841, 1242`).
- 40-architecture: 칸 전체 목록이 없다. 테이블 · 관계 · 핵심 키만 있다. `domains/` 는 비어 있다.
- 보안 grep(이메일 · JWT · uuid · 32자 이상 토큰 · Bearer · password= · tenant 값 · claude.ai 링크 · wss): **0건**. KOS 키 이름(`open_api_key` 등)은 칸 이름일 뿐 값이 없다. `erd/README.md:24` 의 소켓 호스트 · 토큰 경로는 OQ-00-1 에서 일반 표현으로 바꿨다.

## planner 미결 13항 분류

| # | 항목 | 분류 | 메모 |
|---|---|---|---|
| 1 | `visit_requested_procedure.product_option_id` uuid FK 인데 1차에 `product_option` 없음 | **원천 쪽** | `erd/03-visit.md` 표 · `erd/README.md:99` 그대로. 옮기면서 생긴 왜곡 없음 |
| 2 | 타입 `—` 칸 · `consultation_procedure` · `visit_occupied_resource_doctor` 칸 표 없음 | **원천 쪽(칸 표 부재) + 옮기면서(「만들지 않음」 표시)** | 칸 표가 없는 것은 원천 쪽. 「만들지 않는다」로 닫은 것은 planner → F2 |
| 3 | `deleted_at` · `created_at` 예외(`external_outbox` · `event_log` · `push_log` · `crm_connection.connected_at`) | **원천 쪽** | 원천 표 그대로. 다만 묶은 행 해석 규칙은 옮기면서 생긴 문제 → F1 |
| 4 | `visit.room_id` · `visit_task.room_id` 둘 다 | **원천 쪽** | |
| 5 | 03 「정하는 중」 vs README 「정함」 | **원천 쪽** | W4 |
| 6 | 07 「바로 적용 — 검토는 이후」 | **원천 쪽** | 표시가 살아 있다(OQ-07-3) |
| 7 | 열린 enum 값(`display_request.kind` 등) | **원천 쪽** | 그대로 옮겼다 |
| 8 | ESC-001 칸 값 | **옮기면서** | planner 가 고른 값 → W2 |
| 9 | owner TBD · version 0.0.1 | **옮기면서(문서 규칙 쪽)** | 규칙상 TBD 는 허용. version 은 상위기획이 없어 기본값 — 코디 판단 |
| 10 | sources 경로(`erd/` 로 옮겨짐) | **옮기면서 — 문제 아님** | 실제 경로와 맞는다. 외부 레포 경로 표기는 참고 |
| 11 | 검토표(claude.ai) 링크 제거 | **옮기면서 — 문제 아님** | 비공개 artifact 라 빼는 편이 맞다. 추적이 필요하면 kknaks_profile 원천에 남아 있다 |
| 12 | `context/products.md` DAY 행 「비활성」 | **원천과 무관(범위 밖)** | 코디 판단 |
| 13 | 30-work.md Status enum 문구 | **원천과 무관(스캐폴드 템플릿)** | 아래 참고 |

## 직원이 실물에서 만날 자리

- F1 을 고치지 않고 migration 을 만들면 1차 소프트 딜리트 테이블 33곳에서 새 행이 `deleted_at` 없이는 저장되지 않는다. 억지로 값을 넣으면 그 행은 「지워진 것」으로 숨는다. 현황판 · 알림함 · 채팅이 비어 보인다.
- F2 를 고치지 않으면 상담에서 고른 시술(상담 시술 스냅샷)과 예약 칸의 지정 의사가 DAY 에 담기지 않는다. 시술실이 상담 내용을 볼 수 없다.

## 참고(기존 부채 · 설계 판정 아님)

- `40-architecture/system.md:75` 「DB transaction 안에서 외부를 기다리지 않는다」는 erd 원천에 없다. 출처는 CENTURION_DAY `AGENTS.md`(v2-dev) `:74` 이고, system.md `:12` 가 그 문서를 정본으로 가리키므로 발명은 아니다. 출처를 함께 적으면 좋다.
- `products/day/20-spec.md:20` 스캐폴드 문구 「SPEC에 두지 않음: column/index/FK」가 SPEC-000(칸 수준 계약 · selly 선례)과 어긋난다. 템플릿 부채다.
- `products/day/30-work.md:13, 27` 스캐폴드의 Status enum · QA 컬럼이 rules(WP enum `proposed/in_dev/done` · QA 컬럼 금지)와 다르다. 템플릿 부채다(미결 13).
- `40-architecture/*.md` · `README.md` 의 `owner: backend / product` 는 직군 값이다. 개인 owner 규칙은 SPEC · WP 에만 걸리므로 위반은 아니다.
