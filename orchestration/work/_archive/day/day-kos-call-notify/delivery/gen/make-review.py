import json, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = "backend/tests/day/"
R, N, F, RC = T+"board/test_kos_call_rules.py:", T+"notifications/test_kos_calls.py:", T+"notifications/test_kos_calls_flow.py:", T+"notifications/test_kos_calls_races.py:"
ap = json.load(open(f"{D}/wp1-be-apply-v2.json"))
ALL = "scripts/test.sh 전체 2909 passed · scripts/check.sh --static 통과(PR #285 「검증」 절 · be-fix-1 보고)"
acc = {
 "A1": ("pass", [N+"56", R+"60"]),
 "A2": ("pass", [N+"103", N+"90", R+"65", R+"71"]),
 "A3": ("pass", [N+"168", N+"186", N+"150", R+"76", R+"86"]),
 "A4": ("pass", [N+"211", N+"230", N+"246", F+"231", R+"100", R+"107", R+"113"]),
 "A5": ("pass", [F+"273", F+"330", F+"341", F+"353", RC+"65", RC+"88", F+"193", F+"205"]),
 "A6": ("pass", [F+"65", F+"91"]),
 "A7": ("pass", [F+"109", F+"126", F+"139", R+"124", R+"142"]),
 "A8": ("pass", [F+"152", F+"163", F+"183", F+"193"]),
 "A9": ("pass", [N+"56", N+"118", N+"123", ALL]),
 "A10": ("pass", [
   "e2e-1(로컬 스택 + KOS DEMO · 2026-11-25): 지정 1명 · 전체(calledDoctors []) · 여러 작업 한 요청(같은 ms → 호출 1) · 재호출 사슬 · DAY 호출 메아리 0 · KOS 수락 → doctor_call_accept — 모두 O · 호출마다 call_push 1회 · OQ-99 · OQ-106 실측 닫음",
   "prod 실물(사용자 모니터링 · 코디 prod DB 읽기 2026-11-25 · prod 1b5bba22): KOS 에서 건 호출 3건(15:28:41 · 15:32:41 · 16:42:21 KST · event_log call.create source kos · kind all) → 각 notification 5행(DAY 계정 있는 원장 전부 5명) · DAY 에서 건 호출(14:43 · 14:47)과 같은 5행 · 사용자 「맞아 · 모니터링 중」 → pass 수용(사용자 · 코디)",
   "잔여(이 작업 무관 · 기존): push_log prod 전체 0행 — 유일 등록 기기(iOS · 11-12)의 앱 세션이 살아 있지 않아 보내기 대상 없음 · DAY 호출도 같음 · 푸시 실기기 확인은 잔여"]),
}
r = {"delivery_issue": 283, "contract_digest": ap["contract_digest"], "contract_version": 2,
     "spec_baseline_revision": "bf440f270ffdaaabcbed77415ca403df90e4c172",
     "code_pr": 285, "code_pr_head_sha": "af07e9d765c0de3a7344ca23f9ee73b4791a3601",
     "code_merge_sha": "1b5bba225e82fa6e0d777752b76d39eb37a44947",
     "acceptance": [{"id": k, "result": v[0], "evidence": v[1]} for k, v in acc.items()],
     "per_spec": [{"spec": "DAY-SPEC-002", "result": "none"}, {"spec": "DAY-SPEC-005", "result": "none"}],
     "implementation": "conformant", "merged": True}
json.dump(r, open(f"{D}/review-v2-merged-283.json", "w"), ensure_ascii=False, indent=1)
print("ok")
