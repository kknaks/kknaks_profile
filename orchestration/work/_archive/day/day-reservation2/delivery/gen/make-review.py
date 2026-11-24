import json, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD="a0b42a3618e7bc271c42b03c3029266a30ac41ec"; MERGE="55e60aa4d6f3be048bc7e933ee5dbd5f74456bfc"; BASE="29480cfd9062e4d40ab0d273874ac42193dce98d"
T="backend/tests/"
E2E=["사용자 화면 확인 — 로컬 KOS 데모 지점 · 판 1 ~ 4 · 화면 확인 목록 e2e-1-feedback.md B1 ~ B41 고침(2026-11-24 · SPEC-007 고침 4 로 계약 반영)",
     "Code PR CENTURION_DAY#280 본문 「검증」 절 — scripts/check.sh 전체 통과 · 사용자 화면 확인 · dev 스쿼시 머지 55e60aa4 · dev 배포 success · migration head 0028_visit_discharge_reason"]
A2=[T+"architecture/test_screen_copy.py:479",T+"architecture/test_screen_copy.py:487"]
A3=[T+"day/emr/test_reservation_writes_plan.py:124",T+"day/emr/test_outbox_reservation_rules.py:83",T+"day/test_reservation_confirm_loop.py:90",T+"day/test_reservation_confirm_loop.py:98",T+"day/test_reservation_care_rules.py:162",T+"day/test_reservation_care_rules.py:320","scripts/check.sh 전체 통과(PR #280 검증 절)"]
I={
"p1-reservation":(275,["DAY-SPEC-007","DAY-SPEC-006","DAY-SPEC-002","DAY-SPEC-000"],{
 "A1":[T+"day/web/test_reservation_detail_screen.py:272",T+"day/web/test_reservation_detail_screen.py:387",T+"day/web/test_reservation_detail_screen.py:456",T+"day/web/test_reservation_detail_screen.py:571",T+"day/web/test_reservation_detail_screen.py:678",T+"day/test_reservation_detail_rules.py:32",T+"day/test_reservation_detail_rules.py:53"],
 "A2":A2,
 "A3":A3+[T+"day/emr/test_reservation_writes_plan.py:74",T+"day/emr/test_reservation_writes_plan.py:129",T+"day/emr/test_reservation_writes_plan.py:211",T+"day/emr/test_reservation_writes_plan.py:241",T+"day/board/test_reservation_writes_flow.py:144",T+"day/board/test_reservation_writes_flow.py:234",T+"day/board/test_reservation_writes_flow.py:278",T+"migrations/test_detail_permission_migration.py:42"],
 "A4":[T+"day/web/test_reservation_detail_screen.py:642",T+"day/test_reservation_stream.py:52",T+"day/test_reservation_signal_rules.py:23",T+"day/test_reservation_signal_rules.py:39",T+"day/web/test_reservations_companion_screen.py:44",T+"day/test_reservation_inhouse_rules.py:76"],
 "A5":E2E}),
"p2-reception":(276,["DAY-SPEC-007","DAY-SPEC-002","DAY-SPEC-000"],{
 "A1":[T+"day/web/test_reservation_detail_stages_screen.py:115",T+"day/web/test_reservation_detail_stages_screen.py:163",T+"day/web/test_reservation_detail_stages_screen.py:179",T+"day/web/test_reservation_detail_stages_screen.py:374",T+"day/web/test_reservation_detail_stages_screen.py:412",T+"day/test_reservation_care_rules.py:52"],
 "A2":A2,
 "A3":A3+[T+"day/test_reservation_care_rules.py:212",T+"day/board/test_reservation_writes_flow.py:392"],
 "A4":[T+"day/test_reservation_inhouse_rules.py:134",T+"day/web/test_reservation_detail_stages_screen.py:326"],
 "A5":E2E}),
"p3-procedure":(277,["DAY-SPEC-007","DAY-SPEC-002","DAY-SPEC-000"],{
 "A1":[T+"day/web/test_reservation_detail_stages_screen.py:186",T+"day/web/test_reservation_detail_stages_screen.py:389",T+"day/test_reservation_care_rules.py:78",T+"day/test_reservation_care_rules.py:112",T+"day/test_reservation_care_rules.py:300",T+"day/test_reservation_care_rules.py:125"],
 "A2":A2,
 "A3":A3+[T+"day/test_reservation_care_rules.py:248",T+"day/test_reservation_care_rules.py:271",T+"day/web/test_reservation_detail_stages_screen.py:334"],
 "A4":[T+"day/test_reservation_care_rules.py:331",T+"day/test_reservation_inhouse_rules.py:152",T+"migrations/test_alembic.py:94",T+"migrations/test_alembic.py:107"],
 "A5":E2E}),
"p4-discharge":(278,["DAY-SPEC-007","DAY-SPEC-002"],{
 "A1":[T+"day/web/test_reservation_detail_stages_screen.py:228",T+"day/web/test_reservation_detail_stages_screen.py:255",T+"day/web/test_reservation_detail_stages_screen.py:405",T+"day/test_reservation_care_rules.py:202"],
 "A2":A2,
 "A3":A3,
 "A4":[T+"day/test_reservation_care_rules.py:162",T+"day/test_reservation_inhouse_rules.py:76"],
 "A5":E2E}),
}
for n,(iss,specs,acc) in I.items():
    ap=json.load(open(f"{D}/apply-v2-approved-{n}.json"))
    r={"delivery_issue":iss,"contract_digest":ap["contract_digest"],"contract_version":2,"spec_baseline_revision":BASE,"code_pr":280,"code_pr_head_sha":HEAD,"code_merge_sha":MERGE,
       "acceptance":[{"id":k,"result":"pass","evidence":v} for k,v in acc.items()],"per_spec":[{"spec":s,"result":"none"} for s in specs],"implementation":"conformant","merged":True}
    json.dump(r,open(f"{D}/review-v2-merged-{iss}.json","w"),ensure_ascii=False,indent=1)
print("ok")
