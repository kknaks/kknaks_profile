# merge-dev-3 결과 보고 — 코드 ← origin/dev(한 번 더) + migration 0029 겹침

## 상태: done (MERGE_HEAD 상태 · 충돌 0 · 전부 `git add` · 커밋 안 함)

| 워크트리 | HEAD | MERGE_HEAD | 결과 |
|---|---|---|---|
| 코드 `CENTURION_DAY/day-app-re1` | `716e89d6` | `4ba07ffe`(origin/dev) | 충돌 3 풀림 · staged 92 파일 |

커밋 · push · stash · reset 은 하지 않았다. 스펙 워크트리 · 로컬 스택(11040) · 로컬 DB · 시뮬레이터도 건드리지 않았다. `check.sh` 는 격리 인프라에서 돌렸다.
dev 의 이번 10 커밋에는 `app/` 변경이 없다. 그래서 flutter analyze · test 는 돌리지 않았다(브리프 조건대로).

## 1. 충돌 3 — 푼 방법

| 파일 | 충돌 | 푼 방법 |
|---|---|---|
| `backend/day/services/reservation_detail.py` | import: 우리 `displays, questionnaire_reads, sessions` 와 dev `sessions` + `from day.services.ext_charty import desk_payments` | 합집합으로 풀었다. `detail_view` 반환 dict 는 git 이 자동으로 합쳤다. 우리 `questionnaire_reads.summary` · `displays` · `can_detail` 와 dev `desk_payments` 가 같이 들어 있다 |
| `backend/tests/migrations/test_alembic.py` | `HEAD =` 우리 `0029_display_questionnaire_kos` 와 dev `0029_partner_charty` | `HEAD = "0030_display_questionnaire_kos"`. 우리 왕복 시험은 `test_0030_…` 로 이름을 바꾸고, downgrade 대상을 `0028_visit_discharge_reason` 에서 `0029_partner_charty` 로 바꿨다(우리 migration 하나만 왕복시킨다) |
| `backend/day/static/day.css` | 생성 파일 | dev 판을 꺼낸 뒤 `scripts/build-css.sh` 로 다시 만들었다(154.1KB). `check.sh` 의 CSS 재현 검사 통과 |

## 2. migration 옮긴 내용

- `git mv` 로 옮겼다: `20261125_0029_display_questionnaire_kos.py` → **`20261125_0030_display_questionnaire_kos.py`**
  - `revision = "0030_display_questionnaire_kos"`, `down_revision = "0029_partner_charty"`, 머리말 `Revision ID` · `Revises` 도 맞춰 고쳤다
  - 머리말의 「0029 에 넣은 것은 0029 가 아직 … 올라가지 않았기 때문」을 0030 으로 고쳤다
- dev `20261125_0029_partner_charty.py` 는 손대지 않았다.
- 문자열 · 주석으로 우리 번호를 부르던 곳을 grep 해서 전부 바꿨다:
  - `backend/tests/migrations/test_alembic.py`: HEAD · 시험 이름 · downgrade 대상
  - `backend/day/models/reception.py:43,99,106`: 「migration 0029」를 0030 으로(주석)
  - `backend/tests/day/column_snapshot_data.py:476`: `crm_status` 주석 0029 를 0030 으로
  - `backend/tests/day/test_enum_labels.py:47`: `questionnaire_crm_status(0029 …)` 주석을 0030 으로
  - 다시 grep 했을 때 `0029_display_questionnaire_kos` 가 남은 곳은 0. 남은 `0029` 는 전부 dev 의 `0029_partner_charty` 다
- `uv run alembic -c backend/migrations/alembic.ini heads` 결과는 `0030_display_questionnaire_kos (head)` **1개**다.
- 두 migration 이 겹치지 않는지 확인했다:
  - dev 0029 가 건드리는 곳: `customer_type.name_observed_at` · `customer.customer_type_observed_at` · `product_option(_composition).visitor_prices` 칸, 새 표 `partner_consultation_start` · `partner_payment_request`(+ `uq_partner_payment_request_…` · `ix_partner_payment_request_visit`) · `partner_agreement_catalog` · `partner_visit_agreements`. enum 은 새로 만들지 않는다
  - 우리 0030 이 건드리는 곳: `display_request.qr_token_hash` · `qr_nonce` nullable, `questionnaire_history.crm_status` · `crm_error` · `crm_sent_at`, enum `questionnaire_crm_status`, 인덱스 `uq_questionnaire_history_display_request_id`
  - 표 · 칸 · 인덱스 이름 · enum 중 겹치는 것이 없다
- 빈 DB 에서 upgrade head → downgrade → upgrade 시험: `test_alembic.py` 전체(`downgrade base` 왕복 + 우리 0030 왕복)가 `check.sh` tests 안에서 통과했다.

## 3. 자동으로 합쳐진 겹침 확인

| 파일 | dev 쪽 변경 | 판정 |
|---|---|---|
| `templates/partials/reservations_detail.html` | 수납 칸 끝에 `{% if d.desk_payments %}{% include "partials/reservations_payment_requests.html" %}` | 우리 [문진 QR] · [여권 스캔] · [태블릿에 보내기] · 고침 6 자리는 그대로 남았다. dev 는 수납 section 안에만 붙였다. 둘 다 살아 있다 |
| `services/reservation_detail.py` | `desk_payments`(Charty 수납 요청) | 위 충돌 표 참고. 우리 키와 이름이 겹치지 않는다 |
| `emr/base.py` | `EmrAdapter.fetch_agreement_catalog` · `fetch_visit_agreements`(기본은 `EmrError`) | 우리 identity 쓰기(여권 고객 수정 · 사진 · 문진 제출)와 다른 메서드다. 추상 메서드가 아니라서 구현체에는 영향이 없다 |
| `static/day.js` | 고객 차트 이동 · 수납 표 동작 | 바뀐 줄에 reservation · questionnaire · display · scan 관련이 0이다. 프런트 시험 135/135 |
| `styles/app.css` | 고객 차트 · 수납 표 스타일 | 다른 선택자다. Stylelint · CSS 재현 통과 |
| `tests/architecture/test_screen_copy.py` | 차티 수납 요청 · 고객 차트 글자 등록 | 우리 키와 겹치지 않는다. 통과 |
| `tests/day/test_constraints.py` | `partner_payment_request(hospital_id, partner, request_key)` 유일 | 우리 `questionnaire_history.display_request_id` 행 옆에 같이 있다. 통과 |
| `tests/deploy/test_deploy_contract.py` | #294 CI 분리(checks.yaml · dev 배포에서 check 뺌 · prod 는 checks 필요) | 우리 변경과 관계없다. 통과 |
| `scripts/frontend/tests/fixtures/reservations-page.html` | `65b2de5e`: 「예약」 · 「고객」 레일과 「예약 현황」 탭을 `<span>` 에서 `<a>` 로 되돌림 | **dev 그대로 받았다.** 우리 `sse-swap="reservation,write_confirmed,display"` 줄도 남아 있다(1곳) |

## 4. dev 변경이 우리 기능에 주는 영향

- 확인된 동작 영향은 없다. 충돌은 import 와 HEAD 상수뿐이었고, 전체 검사가 통과했다.
- 예약 상세(`detail_view`)가 이제 `desk_payments` 조회를 한 번 더 한다(dev). 우리 쪽 조회(`displays.visit_displays` · 문진 요약)와 같은 세션에서 차례로 돈다. 동시 사용은 없다. query-count 시험도 통과했다.
- `65b2de5e` 로 웹 「예약」 · 「고객」 메뉴가 다시 열렸다. 그래서 예약 화면에서 우리 예약 상세 버튼(문진 QR · 여권 스캔 · 태블릿에 보내기)에 메뉴로 바로 들어갈 수 있다. merge-dev-2 때 「#286 메뉴 막음 그대로」라고 했던 전제는 이번 dev 에서 풀렸다.
- 공유 스펙 번호 문제(merge-dev-2 리포트 6-1: 코드 주석이 옛 스펙 번호를 가리킴)는 이번 범위가 아니라서 그대로 남아 있다.

## 5. 시험 수치

| 검사 | 결과 |
|---|---|
| `alembic heads` | 1개 — `0030_display_questionnaire_kos` |
| `scripts/check.sh`(전체 1회) | **exit 0**. 구조 · Jinja(714 소스) · ruff · format · mypy · taut-audit · taut-check · frontend **135/135** · tests **3211 passed**(422.8s). 증거 `.local/checks/20261126-191400-81523` |
| `fvm flutter analyze` · `test` | 돌리지 않음 — dev 에 `app/` 변경 없음 |

## 6. 로컬 DB revision 바로잡기(코디가 실행)

로컬 DB 는 지금 `0029_display_questionnaire_kos` 에 있을 것이다. 이 id 는 코드에서 사라졌으므로 그대로 `scripts/migrate.sh` 를 돌리면 "Can't locate revision" 으로 실패한다.
우리 칸 · enum 은 이미 들어가 있고 dev 0029(partner 표)만 없다. 아래 순서가 데이터를 지우지 않는 방법이다. 합친 코드에서 실행한다.

```sh
# 0) 지금 상태 확인 (로컬 스키마 이름은 .local 설정의 DB_SCHEMA — 아래 <schema>)
psql "<로컬 DATABASE_URL>" -c "SELECT version_num FROM <schema>.alembic_version"
#    → 0029_display_questionnaire_kos 이어야 아래를 진행

# 1) 버전 표를 갈라지기 전(0028)으로 되돌린다 — 칸은 그대로 둔다
psql "<로컬 DATABASE_URL>" -c "UPDATE <schema>.alembic_version SET version_num = '0028_visit_discharge_reason' WHERE version_num = '0029_display_questionnaire_kos'"

# 2) dev 0029(partner 표)만 적용 → 3) 우리 0030 은 이미 적용돼 있으니 stamp
uv run --frozen python - <<'EOF'
import subprocess, sys
from scripts.devtools.local import ROOT, local_environment
env = local_environment()
def alembic(*a): subprocess.run([sys.executable, "-m", "alembic", "-c", "backend/migrations/alembic.ini", *a], cwd=ROOT, env=env, check=True)
alembic("upgrade", "0029_partner_charty")
alembic("stamp", "0030_display_questionnaire_kos")
alembic("current")
EOF
# → 0030_display_questionnaire_kos (head)
```

다른 방법도 있다(데이터를 조금 잃음). 1)에서 버전을 `0030_display_questionnaire_kos` 로 바꾸고 `downgrade 0029_partner_charty` 를 돌린다. 그다음 버전을 `0028_visit_discharge_reason` 으로 다시 바꾸고 `scripts/migrate.sh` 를 돌린다. 이렇게 하면 우리 downgrade 가 문진 KOS 보냄 상태를 지우고, 토큰 없는 띄우기 행을 `''` 로 채운다.
