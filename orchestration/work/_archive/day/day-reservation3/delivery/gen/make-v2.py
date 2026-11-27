import json, os

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "d0fcc23a4f13593c53a87d3b95b8173cdc779747"
SRC = (
    "SPEC 원천 = DAY-SPEC-008(stable 2026-11-27) + DAY-SPEC-006 개정 ⑮ · DAY-SPEC-005 2026-11-26 개정(U-6) · "
    "DAY-SPEC-007 고침 7 · DAY-SPEC-000 개정 ③ · DAY-SPEC-001 개정 ⑮ — Mediness main d0fcc23a(PR #968 머지 · "
    "spec-baseline ready). main #964 와 번호가 겹쳐 006 ⑭ → ⑮ · 007 고침 6 → 7 로 바꿈. "
    "구현 = Code PR CENTURION_DAY#299(dev 스쿼시 머지 65506f35 · dev 배포 성공 · migration head 20261126_0031_reservation_request · "
    "WP-0 ~ 3 를 한 PR 이 덮음)"
)
DELTA = (
    "2026-11-27 재결속 — baseline = 머지된 Mediness main d0fcc23a(PR #968 — SPEC-008 stable · spec-baseline:pending 뗌). "
    "구현 · 실물(be-probe-1 · 2 · e2e 1 · 2 · be-swagger-1 · 2 · fe-nav-1 · review-doc-5)로 바뀐 계약: "
    "판정 = 이름(대소문자 · 띄어쓰기 무시) + 식별값(생년월일 · 연락처 · SNS · 이메일) 하나 이상 · 국적은 양쪽 있을 때만 · "
    "요청 본문 birthDate 선택 · 식별값 하나 이상 필수(400) · [예약 생성] = W3 reserve 최상위 counselor(W18 없음) · "
    "W18 = [예약 수정]에서 상담사 바꿈 · 지움(counselor: {}) · W1 식별값 + email · W2 email · "
    "예약이 이미 취소된 요청됨 · 확정 스레드 cancel = 202 canceled + reservation_applied cancel · 동기화 자동 취소됨 · "
    "예약 있음에 다른 고객 change = 400 customer_changed(스레드 고객 없음 = 막지 않음) · "
    "Idempotency-Key 재시도 = 처음 응답 그대로(accepted_status · SPEC-000) · 공용 retry 스레드 행 409 request_thread_write · "
    "ext 스웨거에 상태값 뜻 · 상태 × 행동 · 오류 코드 · 흐름 · 문구 「답변 대기중」 · [철회] · [KOS 등록 실패] · "
    "DAY-SPEC-001 개정 ⑮ 로그인 뒤 = 예약 현황 /reservations · 셸 아이콘 줄 「홈」 → 「현황」(키 status · 화면 있는 메뉴 = 고객 · 현황). "
    "실물 e2e 2회 통과 · dev 배포 2026-11-27 · prod 는 다음 배포"
)
ADD = [
    "마감(2026-11-27 · 코드가 맞다): 판정 Rule 1 = 이름 + 식별값 하나 이상 · 국적 양쪽 있을 때만 · birthDate 선택 · 식별값 없음 400 · "
    "W3 counselor · W18 = 수정 때 바꿈 · 지움 · W1 email · 취소된 예약 cancel = 202 canceled · 동기화 자동 취소 · "
    "customer_changed 400 · accepted_status 재시도 · request_thread_write 409 · ext 스웨거 설명",
    "DAY-SPEC-001 개정 ⑮: 로그인 뒤 갈 곳 = 예약 현황 `/reservations`(권한 = reservation view · 모든 직무 기본값) · "
    "셸 아이콘 줄 「현황」(키 status) · 헤더 탭 예약 / 원내 / 시술 현황은 현황 아래 · 화면 있는 메뉴 = 고객 · 현황",
]


def fix(x):
    if isinstance(x, str):
        return (
            x.replace("006 ⑭", "006 ⑮").replace("SPEC-006 개정 ⑭", "SPEC-006 개정 ⑮")
            .replace("SPEC-006 ⑭", "SPEC-006 ⑮").replace("007 고침 6", "007 고침 7")
        )
    if isinstance(x, list):
        return [fix(i) for i in x]
    if isinstance(x, dict):
        return {k: fix(v) for k, v in x.items()}
    return x


r = fix(json.load(open(f"{D}/request-v1-reservation-request.json", encoding="utf-8")))
r["contract_version"] = 2
r["spec_baseline_revision"] = BASE
r["scope_delta"] = DELTA
r["review_surface"][0] = SRC
r["target_delta"] += ADD
if "DAY-SPEC-001" not in r["target_specs"]:
    r["target_specs"].append("DAY-SPEC-001")
r["title"] = r["title"].replace("(DAY-SPEC-008 · 006 ⑮ · 005 · 007 고침 7 · 000 ③)", "(DAY-SPEC-008 · 006 ⑮ · 005 · 007 고침 7 · 000 ③ · 001 ⑮)")
r["execution"]["open_questions"] = [
    "OQ-Q01 · Q02 · Q03(실물 O) · Q12 · Q15 · Q20 · Q21 = 2026-11-27 마감에서 닫음(SPEC-008 §5 「닫힌 OQ → 2026-11-27 마감」)",
    "남은 OQ-Q04(문구) · Q05 · Q08 · Q18 · Q22(기획 정책 15 통보) · Q23(외부 에이전시 페이지 · 범위 밖) = 비차단",
]
r["execution"]["predeploy"] = [
    "dev = 2026-11-27 끝(Key Vault day-dev-ext-partner-grants 병원당 한 줄 새 형식 · 새 키 200 · 틀린 키 401 · deploy-dev 성공)",
    "prod = 다음 배포 — prod 병원 키를 새로 만들어 env DAY_EXT_PARTNER_GRANTS 를 병원당 한 줄로 배포와 동시 교체(옛 형식이면 ext 전체 503) · 링키 · 차티 안내 · migration 유일키 좁히기 전 중복 행 확인",
]
json.dump(r, open(f"{D}/request-v2-reservation-request.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(r["title"])
