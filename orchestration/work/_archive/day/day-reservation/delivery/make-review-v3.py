import json,sys
HEAD="85836b300cb729fb9b4923d05ae9d8bf14bd66f8"; BASE="32b83390eb9fbdcd615f86ecad016b6e9c39ee74"
T="backend/tests/"; F="scripts/frontend/tests/"
mode=sys.argv[1]  # 'probe' or 'final'
e2e_ev=sys.argv[2:] if len(sys.argv)>2 else []
I={
267:("sha256:7bd44234ce9a0108a4ec896d35d79b7847518c1dd97d5a7ff119857b6d257a17",["DAY-SPEC-006","DAY-SPEC-000","DAY-SPEC-002"],{
 "A1":[T+"day/web/test_reservation_page.py:131",T+"day/web/test_reservations_screen.py:277",T+"day/test_reservation_rules.py:113",T+"day/test_reservation_inhouse_rules.py:194"],
 "A2":[T+"day/web/test_reservation_page.py:143",T+"day/web/test_reservation_page.py:152",T+"day/web/test_reservation_page.py:198",T+"day/test_reservation_refresh.py:64"],
 "A3":[T+"day/board/test_reservation_permissions.py:52",T+"day/test_default_permissions.py:75",T+"migrations/test_reservation_permission_migration.py:102"],
 "A4":[T+"day/test_reservation_queries.py:256",T+"day/web/test_reservation_page.py:163",T+"day/test_reservation_rules.py:212",T+"day/test_reservation_rules.py:194",T+"day/test_reservation_layout.py:90"],
 "A5":"E2E",
 "A6":[T+"day/test_reservation_inhouse_queries.py:232",T+"day/test_reservation_amounts.py:205",T+"day/test_reservation_inhouse_rules.py:107"],
 "A7":[T+"day/board/test_reservation_notice.py:167",T+"day/board/test_reservation_notice.py:249",T+"day/board/test_reservation_notice.py:312",T+"day/board/test_reservation_notice.py:358"],
 "A8":[T+"day/board/test_reservation_companions.py:160",T+"day/board/test_reservation_companions.py:231",T+"day/board/test_reservation_companions.py:279",T+"day/test_reservation_layout.py:70",T+"day/test_reservation_layout.py:104"],
 "A9":[T+"migrations/test_reservation_permission_migration.py:102",T+"migrations/test_transaction_status_migration.py:36",T+"migrations/test_purchase_task_visit_index_migration.py:47",T+"migrations/test_reservation_notice_permission_migration.py:84",T+"migrations/test_companion_migration.py:94",T+"migrations/test_companion_migration.py:114",T+"migrations/test_alembic.py:107"]}),
268:("sha256:0e03044b8b5249b04ea565f00a5c50dc92f776fb6edff3de04fa800ff8e537c8",["DAY-SPEC-006","DAY-SPEC-000"],{
 "A1":[T+"day/emr/test_date_sync.py:209",T+"day/emr/test_date_sync_rules.py:106"],
 "A2":[T+"day/emr/test_date_sync.py:235",T+"day/emr/test_date_sync_rules.py:147"],
 "A3":[T+"day/emr/test_date_sync.py:255",T+"day/emr/test_date_sync.py:278",T+"day/emr/test_date_sync.py:296"],
 "A4":[T+"day/emr/test_date_sync.py:320",T+"day/emr/test_date_sync_rules.py:125"],
 "A5":[T+"day/emr/test_date_sync.py:336",T+"day/emr/test_date_sync.py:448",T+"day/emr/test_emr_sync_service.py:177"],
 "A6":"E2E",
 "A7":[T+"day/emr/test_notice_sync.py:44",T+"day/emr/test_notice_sync.py:106",T+"day/emr/test_date_sync_notices.py:49",T+"day/emr/test_date_sync_notices.py:66",T+"day/emr/test_date_sync_notices.py:82"],
 "A8":[T+"day/emr/test_kos_sale_mapper.py:180",T+"day/emr/test_kos_keys_mapper.py:495",T+"day/test_reservation_amounts.py:243"],
 "A9":[T+"day/test_reservation_refresh.py:120",T+"day/emr/test_date_sync.py:362",T+"day/emr/test_date_sync.py:407"]}),
269:("sha256:8811c0d5a4afd3fbdad9a762b4796f9457889da4266ae0c7539cad48bbe852b3",["DAY-SPEC-006"],{
 "A1":[T+"architecture/test_screen_copy.py:226",T+"day/web/test_reservations_screen.py:358",T+"day/web/test_reservations_screen.py:601"],
 "A2":[T+"architecture/test_web_rules.py:101"],
 "A3":[F+"res-browser.test.mjs:8",F+"res-browser.test.mjs:21",F+"res-order.test.mjs:61",T+"day/web/test_reservations_screen.py:288",T+"day/web/test_reservations_screen.py:422"],
 "A4":"E2E",
 "A5":[F+"res-inhouse.test.mjs:30",F+"res-inhouse.test.mjs:67",F+"res-inhouse.test.mjs:101",T+"day/web/test_reservations_screen.py:481"],
 "A6":[F+"res-companion.test.mjs:29",F+"res-companion.test.mjs:56",F+"res-companion.test.mjs:85",F+"res-companion.test.mjs:108",F+"res-companion.test.mjs:134",F+"res-companion.test.mjs:202"],
 "A7":[F+"res-notice.test.mjs:54",F+"res-notice.test.mjs:73",F+"res-notice.test.mjs:92",F+"res-notice.test.mjs:140",F+"res-notice.test.mjs:169"],
 "A8":[F+"res-companion.test.mjs:165",F+"res-companion.test.mjs:246",F+"res-debounce.test.mjs:70"]})}
out=sys.argv[0].rsplit('/',1)[0]
for n,(dg,specs,acc) in I.items():
    a=[]
    ok=True
    for k,v in acc.items():
        if v=="E2E":
            if e2e_ev: a.append({"id":k,"result":"pass","evidence":e2e_ev})
            else: a.append({"id":k,"result":"undetermined","evidence":["PR #272 body 검증 절: 요청 수 · 두 창 동시 e2e 기록 없음"]}); ok=False
        else: a.append({"id":k,"result":"pass","evidence":v})
    r={"delivery_issue":n,"contract_digest":dg,"contract_version":3,"spec_baseline_revision":BASE,"code_pr":272,"code_pr_head_sha":HEAD,"code_merge_sha":None,
       "acceptance":a,"per_spec":[{"spec":s,"result":"none"} for s in specs],"implementation":"conformant" if ok else "conflict","merged":False}
    json.dump(r,open(f"{out}/review-{mode}-{n}.json","w"),ensure_ascii=False,indent=1)
