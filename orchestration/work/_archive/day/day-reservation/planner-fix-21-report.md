# planner-fix-21 결과 보고 — 마감: SPEC-006 R73 ~ R75 · SPEC-000 / SPEC-002 맞추기 · migration 0018 ~ 0023

## 상태: done

- 커밋 안 함. 워크트리 `day-reservation-spec` · HEAD `682f2aed` 위에 커밋하지 않은 변경 6 파일.
- `python3 scripts/lint-pipeline.py --strict` = **0 error · 263 warning**(warning 은 모두 다른 제품 — selly 등).
- 30-work.md 는 건드리지 않음(Delivery 재결속 몫).
- migration 번호 · 칸 이름은 코드 워크트리 `CENTURION_DAY/day-reservation`(rebase 뒤 `4d8878ab` · `a08f1a0b` · base `b2f28990`)의 `migrations/versions/20261123_0018 ~ 0023_*.py` 를 직접 읽어 맞췄다.

| 번호 | revision |
|---|---|
| 0018 | `0018_reservation_permission`(down `0017_ext_catalog`) |
| 0019 | `0019_transaction_status_more` |
| 0020 | `0020_purchase_task_visit_index`(`ix_purchase_visit_id` · `ix_visit_task_visit_id`) |
| 0021 | `0021_notice_permission` |
| 0022 | `0022_companion_tables`(`uq_companion_member_visit_id` · `ix_companion_member_companion_group_id`) |
| 0023 | `0023_companion_permission` |

## SPEC-006 — 개정 ⑪ (`spec-006-reservation-board.md`)

- 머리: last_updated 2026-11-24 · 결정 원천 R39 ~ R75(두 곳) · **개정 ⑪ 노트** · 개정 ⑩ 보충 2 노트의 꼬리표 문장 취소선 + 「→ R75」.
- **R73**
  - U-5 순서 · Rule 15: 닫히지 않은 카드 안에서 동행 그룹 카드 먼저(생긴 순 → 넣은 순) → 그룹 없는 카드(시작 → 생성).
  - U-9 「누가 · 언제」 · Rule 16: 끈 카드 · 놓은 카드 **둘 다** 지난 날 아님 ∧ **같은 날(KST)** · 바꾸기 전에 전부 검사.
  - API 행: 404(없는 방문 · 다른 병원 — 구현 사실) 추가 · 검사 순서 400 → 404 → 409 `companion_past_date` → 409 `companion_condition`(다른 날 포함).
  - 케이스 2줄 추가(하나만 지난 날 · 날짜 다름).
- **R74**: SPEC 에 들어간 적 없음(18px · 책갈피 grep 0) → 노트에 「반영 전 R75 로 뒤집힘」만 적음.
- **R75**: RV-45 · U-9 표시 · S-8 · 케이스 「동행 띠」 · Rule 8 · 시안과 다른 곳 → 진한 primary 굵은 테두리만 · 글자 없음 · 행 높이 = `lines` × 70 그대로. R72 꼬리표는 취소선.
- **migration 번호**: §3 API 권한(0018 · 0021 · 0023) · 거래 매핑(0019) · §4 DB(0018 · 0019 · 0020 · 0022 · 0023).
- **구현과 칸 맞춤**: `companion_member` = `hospital_id` 추가 · ~~`group_id`~~ → `companion_group_id`(DB 표 · 칸 표) · 부분 유일 이름 · 그룹 인덱스.
- 「다른 스펙과 다른 곳」 5줄(거래 상태 · 권한 키 ⑨ · notice · 동행 테이블 · 권한 키 ⑩) = 취소선 + 「DAY-SPEC-000 2026-11-24 개정 ○ / DAY-SPEC-002 개정 ㉗ 에 반영 · 이제 다른 곳 없음」. 머리말 · Domain note 의 「SPEC-000 과 다른 곳 / 아직 없음」도 같이 고침.
- 낡은 문장 grep(「동행그룹」 · 꼬리표 · 걸쳐 · 18px · 책갈피 — 취소선 밖): 살아 있는 낡은 문장 0. 남은 건 개정 노트의 뒤집음 설명 · 「꼬리표 없음」 문장뿐.

## DAY-SPEC-000 — 2026-11-24 개정 (`spec-000-data-model.md`)

- frontmatter last_updated · sources(결정 파일) · 개정 노트 ① ~ ⑥.
- 02 `external_ref`: `entity_type` 값 `notice` 단락.
- 03 새 절 `companion_group` · `companion_member`(구현 칸 그대로 · 부분 유일 · 인덱스 · 날짜 칸 없음 · JSON 목록 없음 · KOS / `external_ref` 없음 · event_log `companion_join` / `companion_leave` · 0022).
- 04 `job_role_permission.permission_key`: 목록 정본 = DAY-SPEC-002 · 예약 현황 키 셋 · 데이터 migration.
- 05 `visit_task` · 08 `purchase` 인덱스 줄(0020).
- 07 `notice`: id 설명 = KOS → DAY 동기화 + 공지 저장 · `entity_type = notice` · deleted_at 설명 · 원장 = KOS · **OQ-07-2 닫음**.
- 08 `purchase_transaction.status` enum 5값(+ spent · requested · failed · 0019 · 수납에 세는 값) · `payment_type` KOS 매핑 7종(PLATFORM · EASY_PAY · MEDICAL_LOAN 추가 · enum migration 없음).
- §4A.7: status 행 추가 · payment_type 행 갱신 · **OQ-4A-1 좁힘**(openapi 문자열로 매핑 · 표본 확인은 열림).

## DAY-SPEC-002 — 개정 ㉗ (`spec-002-procedure-board.md`)

- frontmatter · 개정 ㉗ 노트.
- §3 「권한 — 1차 기본」 키 표에 `reservation` view · `reservation.notice` edit · `reservation.companion` edit 추가. 「키 목록은 이 표 한 곳」으로 명시.
- 단락 하나: 셋 다 이름 표 · 태그와 상관없이 모든 직무 기본. 이미 있던 직무 = 데이터 migration 0018 · 0021 · 0023. 되돌리면 그 키 행 삭제. 사람이 지운 행은 되돌리지 않음.
- 근거 = 코드 `policies/permissions.py` ROWS(두 묶음 모두 세 키).
- OQ-02 행에 예약 현황 키 덧붙임.

## 나머지

| 파일 | 바뀐 것 |
|---|---|
| `10-decision.md` | R39 ~ R75 · R73 ~ R75 요약 · R72 꼬리표 취소선(두 곳) · 새 ESC 없음 |
| `20-spec.md` | 예약 현황 줄: 띠 = 진한 파랑 · 글자 없음(R75) · R73 · 개정 ⑪ · migration 0018 ~ 0023 · SPEC-000 / 002 로 옮김 |
| `log.md` | spec-change 1행(영향 SPEC-006 · 000 · 002) |

## planner 가 읽어 넣은 곳 (코디 확인 바람)

1. 결제 수단 PLATFORM · EASY_PAY · MEDICAL_LOAN 은 **표본 없이 openapi 문자열로 매핑**한다(코드 주석 그대로). 그래서 OQ-4A-1 은 닫지 않고 「좁힘」으로 두었다.
2. 404(없는 방문 · 다른 병원)는 결정에 없다. 구현 사실이라 API 행에 적었다.
3. SPEC-000 동행 절은 §3 03(예약 / 방문) 끝에 두었다.

## 남은 것

- `40-architecture/erd.md` 에 동행 두 테이블이 없다. 범위 밖이라 그대로 두었다.
- 30-work Coverage · Delivery #267 ~ #269 재결속은 코디 몫이다.
- 띠 두께 · 둥글기 값은 구현이 정한다.
