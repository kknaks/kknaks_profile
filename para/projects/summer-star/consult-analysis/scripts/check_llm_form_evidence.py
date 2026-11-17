#!/usr/bin/env python3
"""LLM 라벨 오염 점검 — 성공 방 주제별로 근거 메시지에 예약표 메시지가 든 방 수(SPEC-002 0.3.0).

- 예약표 메시지 = 우리 form_labels ≥ 3(발송) · 고객 form_filled ≥ 2(회신). 0.3.0 부터 LLM 입력에서 빠지므로 0 이어야 한다.
- 참고로 「칸 이름이 하나라도 든 메시지(form_labels ≥ 1)」 기준도 같이 센다(문장 속 칸 낱말 · 칸 1개 회신 포함).
- 출력은 건수만. 0.3.0 기준이 0 이 아니면 종료 1.
"""

import argparse
import json
import os
import sqlite3
import sys

TOPICS = ("procedure", "price", "schedule", "location", "interpreter", "result", "safety", "promo", "other")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    args = ap.parse_args(argv)
    con = sqlite3.connect("file:%s?mode=ro" % os.path.abspath(args.db), uri=True)
    form = {}
    for mid, own, labels, filled in con.execute(
            "SELECT m.message_id, m.is_owner, l.form_labels, l.form_filled FROM message m "
            "JOIN l2_message l USING (message_id)"):
        form[mid] = ((own == 1 and labels >= 3) or (own == 0 and filled >= 2), labels >= 1)
    rows = con.execute("SELECT x.topics, x.evidence_message_ids, b.stage, x.version FROM l2_llm_label x "
                       "JOIN l2_booking_stage b USING (conversation_id)").fetchall()
    con.close()
    print("라벨 방 %d · 판 %s" % (len(rows), ", ".join(sorted({r[3] for r in rows}))))
    print("%-12s %8s %16s %18s" % ("주제", "성공 방", "근거에 예약표", "근거에 칸 낱말≥1"))
    bad = 0
    for t in TOPICS:
        succ = [json.loads(ev) for tp, ev, st, _v in rows if st == "form_filled" and t in json.loads(tp)]
        strict = sum(any(form.get(e, (False, False))[0] for e in ev) for ev in succ)
        loose = sum(any(form.get(e, (False, False))[1] for e in ev) for ev in succ)
        bad += strict
        print("%-12s %8d %16d %18d" % (t, len(succ), strict, loose))
    print("예약표 근거 합 %d" % bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
