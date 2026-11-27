import json, os

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD = "8a5ee874bed06bef1b4cb9f2dec4105d412bcaf0"
MERGE = "65506f35754f58ee6737fa7354cee61b52534ad1"
BASE = "d0fcc23a4f13593c53a87d3b95b8173cdc779747"
T = "backend/tests/"
CHECK = "scripts/check.sh --pure 전체 통과(be-swagger-2 · fe-nav-1 · Code PR #299 검증 절) · scripts/test.sh 전체 3297 passed(fe-nav-1)"
ACC = {
    "A1": [T + "day/test_reservation_request_flow.py:90", T + "day/test_reservation_request_flow.py:116", T + "day/test_reservation_request_flow.py:133",
           T + "day/test_reservation_request_rules.py:40", T + "day/test_reservation_request_rules.py:49", T + "day/test_reservation_request_rules.py:164",
           T + "day/test_reservation_request_rules.py:187", T + "day/test_reservation_request_rules.py:201", T + "day/test_reservation_request_rules.py:216",
           T + "day/board/test_reservation_request_actions_flow.py:284", T + "day/test_ext_contract.py:50", T + "day/test_ext_contract.py:111", CHECK],
    "A2": [T + "day/test_ext_contract.py:131", T + "migrations/test_alembic.py:350", T + "day/test_ext_writes.py:259",
           T + "day/test_reservation_request_rules.py:53", "PR #299 리뷰(taewoo) · dev Key Vault 새 형식 교체 뒤 새 키 200 · 틀린 키 401 · 옛 문서 아이디 401(코디 2026-11-27)", CHECK],
    "A3": [T + "day/test_reservation_request_rules.py:70", T + "day/test_reservation_request_rules.py:74", T + "day/test_reservation_request_rules.py:90",
           T + "day/test_reservation_request_rules.py:96", T + "day/test_reservation_request_rules.py:104", T + "day/test_reservation_request_rules.py:141",
           T + "day/test_reservation_request_rules.py:208", T + "day/test_reservation_request_rules.py:226", T + "day/test_reservation_request_rules.py:235",
           T + "day/test_reservation_request_flow.py:190", T + "day/test_reservation_request_flow.py:266",
           T + "day/board/test_reservation_request_actions_flow.py:108", T + "day/board/test_reservation_request_actions_flow.py:169",
           T + "day/board/test_reservation_request_actions_flow.py:245", T + "day/board/test_reservation_request_actions_flow.py:338",
           T + "day/board/test_reservation_request_actions_flow.py:388", T + "day/web/test_reservation_requests_screen.py:477", CHECK],
    "A4": [T + "day/emr/test_reservation_request_writes_plan.py:55", T + "day/emr/test_reservation_request_writes_plan.py:75",
           T + "day/emr/test_reservation_request_writes_plan.py:94", T + "day/emr/test_reservation_request_writes_plan.py:108",
           T + "day/emr/test_reservation_request_writes_plan.py:114", T + "day/emr/test_reservation_request_writes_plan.py:123",
           T + "day/emr/test_reservation_request_writes_plan.py:129", T + "day/emr/test_reservation_request_writes_plan.py:139",
           T + "day/board/test_reservation_request_actions_flow.py:429",
           "착수 전 실물 확인 be-probe-1 Q01 · Q02 · Q03 전부 O(2026-11-26 · KOS 데모 지점) · be-probe-2 ② ③(W1 email · counselor: {} 지우기)"],
    "A5": [T + "day/web/test_reservation_requests_screen.py:190", T + "day/web/test_reservation_requests_screen.py:208",
           T + "day/web/test_reservation_requests_screen.py:240", T + "day/web/test_reservation_requests_screen.py:294",
           T + "day/web/test_reservation_requests_screen.py:306", T + "day/web/test_reservation_requests_screen.py:331",
           T + "day/web/test_reservation_requests_screen.py:342", T + "day/web/test_reservation_requests_screen.py:358",
           T + "day/web/test_reservation_requests_screen.py:388", T + "day/web/test_reservation_requests_screen.py:420",
           T + "day/web/test_reservation_requests_screen.py:439", T + "day/web/test_reservations_screen.py:460",
           T + "day/auth/test_web_login.py:44", "scripts/check.sh --pure(인라인 스크립트 · 손 CSS 검사 포함) 통과"],
    "A6": [T + "day/test_reservation_request_flow.py:90", T + "day/web/test_board_feedback.py:292", T + "day/web/test_board_feedback.py:526",
           T + "day/web/test_reservation_requests_screen.py:225"],
    "A7": ["e2e-1(2026-11-26 · 로컬 스택 + KOS 데모 지점 · 데모 확인 뒤만): E1 초진 → 목록 · 창 → [예약 생성] W1 → W2 → W3 → 확정(write_confirmed 1.6s) · KOS 다시 읽기로 상담사 · 유입 · 메모 · reservation_applied · E5 · E4 · 재진 · E2 change → [예약 수정] W4 · 변경 요청 → 새 버전 · 철회 · customer_changed 400 · E2 cancel → [예약 취소] · 정리 — 코드 결함 0 · 발견 4",
           "e2e-2(2026-11-26): 발견 ② 이메일만 초진 = 409 customer_ambiguous(중복 고객 안 생김) · ③ 상담사 비움 = W18 counselor: {} · KOS 다시 읽기 없음 · ④ 예약 현황 먼저 취소 → E2 cancel 202 canceled — 버그 없음",
           "SSE 두 번째 브라우저 따로 기록은 없음 — SSE reservation_request 신호 0.1s 측정(e2e-1 #2) · 사용자 화면 확인 · dev 배포 성공(2026-11-27 · 65506f35)"],
}
r = {
    "delivery_issue": 297,
    "contract_digest": json.load(open(f"{D}/apply-v2-approved.json"))["contract_digest"],
    "contract_version": 2,
    "spec_baseline_revision": BASE,
    "code_pr": 299,
    "code_pr_head_sha": HEAD,
    "code_merge_sha": MERGE,
    "acceptance": [{"id": k, "result": "pass", "evidence": v} for k, v in ACC.items()],
    "per_spec": [{"spec": s, "result": "none"} for s in ["DAY-SPEC-008", "DAY-SPEC-006", "DAY-SPEC-005", "DAY-SPEC-007", "DAY-SPEC-000", "DAY-SPEC-001"]],
    "implementation": "conformant",
    "merged": True,
}
json.dump(r, open(f"{D}/review-v2-merged-297.json", "w"), ensure_ascii=False, indent=1)
print("ok")
