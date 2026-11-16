# -*- coding: utf-8 -*-
"""ERD v3 §5 충돌 ④⑥⑦⑧⑨ — 생성 · conflict_override · conflict_close(verdict 3) · fold_approve 의 ⑦ 닫힘(V3-10) · ⑨ 결정이 세운 자리(V3-9) · 안정 키."""
from base import ERD, T, build, log
from registry import mark
from synth import dec

RULES = ERD["enums"]["conflict.rule_ref"]
VERDICTS = ERD["enums"]["conflict.close_verdict"]
KIND = {"④": "value_conflict", "⑥": "value_conflict", "⑦": "duplicate_candidate", "⑧": "unregistered_value", "⑨": "unresolved_reference"}
STATUS0 = {"④": "auto_resolved_by_trust", "⑥": "open", "⑦": "open", "⑧": "open", "⑨": "open"}


def pick(S, rr):
    return next(c for c in S.conflicts if c["rule_ref"] == rr and c["status"] == STATUS0[rr])


class Conflicts(T):
    def test_create(self):
        w, S = build("plain")
        for rr in RULES:
            c = pick(S, rr)
            self.assertEqual((c["kind"], c["status"]), (KIND[rr], STATUS0[rr]), rr)
            self.assertEqual(c["stable_key"]["kind"], c["kind"])
            self.assertEqual(c["stable_key"]["locators"], sorted(c["stable_key"]["locators"]))
            self.assertTrue(c["id"].startswith("CFL-"))
            mark(f"conflict:{rr}:create", "test_create")
        # ④ — 높은 순위(products.json mfds = 2) 값 자동 채택 · 낮은 값도 values 에 보관
        c4 = next(c for c in S.conflicts if c["rule_ref"] == "④" and c["field"] == "mfds")
        self.assertEqual(c4["chosen_value"], True)
        self.assertEqual(sorted(v["trust_tier"] for v in c4["values"]), [2, 3])
        # ⑧ 은 조각 값까지 안정 키
        c8 = pick(S, "⑧")
        self.assertIn("value", c8["stable_key"])
        # ⑨ 는 참조 anchor(REF-)를 기록
        self.assertTrue(any(c.get("ref_id") for c in S.conflicts if c["rule_ref"] == "⑨"))
        for s in ("open", "auto_resolved_by_trust"):
            mark(f"conflict:status={s}", "test_create")

    def test_lifecycle(self):
        w0, S0 = build("plain")
        keys = {rr: pick(S0, rr)["stable_key"] for rr in RULES}
        ops = [("conflict_override", None)] + [("conflict_close", v) for v in VERDICTS]
        for op, verdict in ops:
            decs = []
            for rr in RULES:
                did = f"DEC-T-C-{op[9:12]}-{verdict or 'ovr'}-{RULES.index(rr)}"
                nv = {"chosen_value": f"사람 값 {rr}"} if op == "conflict_override" else {"verdict": verdict, "note": "합성"}
                decs.append(dec(did, op, {"conflict_key": keys[rr]}, nv))
            w, S = build(f"life-{op}-{verdict}", decs)
            for rr, d in zip(RULES, decs):
                lg = log(S, d["id"])
                self.assertEqual((lg["result"], lg["stage"]), ("applied", "⑥"), d["id"])
                c = next(c for c in S.conflicts if c["stable_key"] == keys[rr])
                self.assertEqual(c["decision_id"], d["id"])
                if op == "conflict_override":
                    self.assertEqual((c["status"], c["chosen_value"]), ("resolved", f"사람 값 {rr}"))
                    mark(f"conflict:{rr}:conflict_override", "test_lifecycle")
                else:
                    self.assertEqual((c["status"], c["close_verdict"], c["close_note"]), ("dismissed", verdict, "합성"))
                    mark(f"conflict:{rr}:conflict_close={verdict}", "test_lifecycle")
                    mark(f"kind:conflict_close:new_value.verdict={verdict}", "test_lifecycle")
        for i in ("kind:conflict_close", "order:⑥:conflict_close", "conflict:status=resolved", "conflict:status=dismissed"):
            mark(i, "test_lifecycle")

    def test_fold_closes_duplicate_pair(self):
        """V3-10 — fold_approve 가 접는 anchor 쌍의 ⑦ 은 resolved · decision_id. 쌍이 아닌 ⑦(한쪽만 접는 anchor 위치)은 그대로 open."""
        import test_decisions as TD
        w, S = build("tuples", TD.TUPLE_DECS)
        pair = [c for c in S.conflicts if c["kind"] == "duplicate_candidate" and c["field"].endswith("「감마원볼」")][0]
        self.assertEqual((pair["status"], pair["decision_id"], pair["close_verdict"]), ("resolved", "DEC-T-04-FOLD7", None))
        self.assertIn({"conflict": pair["id"], "decision": "DEC-T-04-FOLD7", "anchors": sorted([TD.A_G1, TD.A_G2])}, S.ctx["fold_closed"])
        self.assertEqual(log(S, "DEC-T-04-FOLD7")["closed_duplicates"], 1)
        mark("conflict:⑦:fold_approve_closes_pair", "test_fold_closes_duplicate_pair")
        half = [c for c in S.conflicts if c["kind"] == "duplicate_candidate" and c["field"].endswith("「감마원턱」")][0]
        self.assertEqual(half["status"], "open")       # A_T1 하나만 접는 anchor — 쌍(A_T1·A_T2)이 아니다
        self.assertGreaterEqual(S.ctx["fold_overlap_open"], 1)
        mark("conflict:⑦:fold_approve_not_pair", "test_fold_closes_duplicate_pair")

    def test_no_target(self):
        w, S = build("ck-none", [dec("DEC-T-C-NONE", "conflict_close", {"conflict_key": {"kind": "duplicate_candidate", "locators": ["taxonomy.json:modality[].id@9"]}},
                                     {"verdict": "not_same", "note": "합성"})])
        self.assertEqual(log(S, "DEC-T-C-NONE")["result"], "no_target")
        mark("conflict:stable_key:no_target", "test_no_target")
