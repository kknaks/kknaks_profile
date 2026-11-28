import json
HEAD="d1ce8ea80b6ffa070154fc7d6e403ba45f1ba5a5"; MERGE="7af15621ad067f2edbbeef69ab62901aad57c8c9"; BASE="9bfccfb27be0b50820430d4fee01895a63a7b3bb"
T="backend/tests/"; F="scripts/frontend/tests/"; A="app/test/ui/"
PRV="Code PR CENTURION_DAY#303 본문 「검증」 절 — ./scripts/test.sh --pure 2457 passed · 전체(infra) 3344 passed · web 290 · arch 393 · node 141 · flutter analyze 0 · flutter test +551 −1(base 기존 실패 board_messages_contract_test · PR 무관) · 코드 검수 review-code-1 → review-code-2 PASS"
E2E="Code PR #303 「검증」 절 로컬 e2e(KOS DEMO 실물): F6 4경로 qrUrl · 팝오버 · 배치 웹 = 앱 · 문진 읽기 회차 44회 중복 0 · 제출 id = 읽기 id(D46 ②) · 6개월 — e2e-1-report.md · e2e-2-report.md"
QA="웹 화면 검수 qa-1(headless) · qa-2(headed) — F1 F2 F3 F6(웹) · 링크 복사/열기 · 6개월 · 콘솔 CSP 0(qa-1-report.md · qa-2-report.md)"
PEND="미확인 — 기기 줄 · 태블릿에 띄우기 · 팝오버 연 채 다시 그리기(D45) = 로컬 등록 태블릿 0대 · qa-1-report.md 7 「D45 미검증」 · DAY-SPEC-007 OQ-D53 · dev 배포 7af15621 성공 · 태블릿 실기기 확인 대기"
PENDAPP="미확인 — 앱 태블릿 실기기(또는 에뮬레이터) 배치 · 「6개월 경과」 실물 기록 없음(위젯 테스트만) · DAY-SPEC-007 OQ-D53 · dev 배포 7af15621 성공 · 태블릿 실기기 확인 대기"
I={
300:(["DAY-SPEC-000","DAY-SPEC-002","DAY-SPEC-003","DAY-SPEC-006","DAY-SPEC-007"],"wp1-be",{
 "A1":("pass",[T+"day/board/test_reservation_detail_origin.py:66",T+"day/board/test_reservation_detail_origin.py:71"]),
 "A2":("pass",[T+f"day/test_reservation_layout.py:{n}" for n in (64,68,89,94,100,109,127,151,158,164,189,204,212,220)]+[T+"day/test_reservation_rules.py:145",T+"day/test_reservation_rules.py:159",T+"day/test_reservation_rules.py:310"]),
 "A3":("pass",[T+f"day/emr/test_kos_questionnaire_read.py:{n}" for n in (62,71,77,83,110)]+[T+f"day/board/test_kos_questionnaire_sync.py:{n}" for n in (118,129,142,149)]+[T+"day/emr/test_questionnaire_sync_rules.py:44",T+"day/emr/test_questionnaire_sync_rules.py:105"]),
 "A4":("pass",[T+f"day/test_questionnaire_period_rules.py:{n}" for n in (19,26,32,38,45)]+[T+"day/board/test_kos_questionnaire_sync.py:198",T+"day/board/test_kos_questionnaire_sync.py:218"]),
 "A5":("pass",[T+f"day/board/test_reservation_display_popover.py:{n}" for n in (54,64,81,96,132)]+[T+"day/board/test_kos_questionnaire_sync.py:218"]),
 "A6":("pass",[PRV,T+"migrations/test_alembic.py:107",T+"day/test_display_rules.py:281"]),
 "A7":("pass",[E2E]),
}),
301:(["DAY-SPEC-006","DAY-SPEC-007"],"wp2-web",{
 "A1":("pass",[T+"day/web/test_reservations_companion_screen.py:76",F+"res-display-link.test.mjs:141",QA]),
 "A2":("pass",[F+f"res-companion.test.mjs:{n}" for n in (212,250,280,333)]+[T+"day/web/test_reservations_companion_screen.py:28",T+"day/web/test_reservations_companion_screen.py:44"]),
 "A3":("pass",[T+"day/web/test_reservation_detail_display_screen.py:40",T+"day/web/test_reservation_detail_display_screen.py:68",T+"day/web/test_reservation_detail_display_screen.py:143",F+"res-display-link.test.mjs:34",F+"res-display-link.test.mjs:51",F+"res-display-link.test.mjs:67"]),
 "A4":("pass",[T+"day/web/test_reservation_detail_display_screen.py:87"]),
 "A5":("pass",[PRV]),
 "A6":("undetermined",[PEND,"확인된 부분: 링크 열기 문진 제출 · [+] 예약 등록 = "+QA]),
}),
302:(["DAY-SPEC-003","DAY-SPEC-006","DAY-SPEC-007"],"wp3-app",{
 "A1":("pass",[A+f"reservation_table_test.dart:{n}" for n in (56,93,114,180,214,225,241)]),
 "A2":("pass",[A+"reservation_ui_test.dart:156"]),
 "A3":("pass",[PRV]),
 "A4":("undetermined",[PENDAPP]),
}),
}
for iss,(specs,n,acc) in I.items():
    ap=json.load(open(f"{n}-apply-v3-approved.json"))
    allpass=all(r=="pass" for r,_ in acc.values())
    r={"delivery_issue":iss,"contract_digest":ap["contract_digest"],"contract_version":3,"spec_baseline_revision":BASE,"code_pr":303,"code_pr_head_sha":HEAD,"code_merge_sha":MERGE,
       "acceptance":[{"id":k,"result":v[0],"evidence":v[1]} for k,v in acc.items()],"per_spec":[{"spec":s,"result":"none"} for s in specs],"implementation":"conformant","merged":True}
    json.dump(r,open(f"review-v3-merged-{iss}.json","w"),ensure_ascii=False,indent=1)
print("ok")
