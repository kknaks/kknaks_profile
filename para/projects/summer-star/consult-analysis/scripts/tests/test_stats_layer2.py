"""stats_layer2 계산 시험 — 지어낸 방만 쓴다."""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import stats_layer2 as S  # noqa: E402

HOUR = 3600 * 1000


def m(seq, own, ms, content="", n_letters=4, auto=None, form_filled=0, photo=False, share=False, n_emoji=0,
      form_labels=None):
    return {"id": seq, "seq": seq, "own": own, "ms": ms, "content": content, "n_letters": n_letters,
            "n_emoji": n_emoji, "auto": auto, "form_filled": form_filled, "photo": photo, "share": share,
            "form_labels": form_labels if form_labels is not None else (5 if form_filled else 0)}


def booking(stage="inquiry", filled=None, got=0):
    b = {"stage": stage, "got_auto_reply": got, "handoff_mentioned": 0, "filled_message_id": None}
    if filled:
        b.update(filled_message_id=filled["id"], filled_seq=filled["seq"], filled_ms=filled["ms"])
    return b


NAT = {"nationality": None, "source": "none"}


class Basics(unittest.TestCase):
    def test_rate_small(self):
        self.assertEqual(S.rate(3, 9), {"n": 3, "d": 9, "pct": 33.3, "small": True})
        self.assertEqual(S.rate(0, 0)["pct"], None)
        self.assertFalse(S.rate(5, 10)["small"])

    def test_dist(self):
        d = S.dist([1, 2, 3, 4, None])
        self.assertEqual((d["n"], d["median"], d["q1"], d["q3"]), (4, 2.5, 1.8, 3.2))
        self.assertEqual(S.dist([])["median"], None)

    def test_turns_skip_auto(self):
        msgs = [m(1, False, 0), m(2, True, 1, auto="away"), m(3, False, 2), m(4, True, 3), m(5, True, 4),
                m(6, False, 5)]
        self.assertEqual(S.count_turns(msgs), 3)

    def test_first_form(self):
        self.assertEqual(S.first_form(m(1, False, 0, photo=True)), "photo")
        self.assertEqual(S.first_form(m(1, False, 0, share=True)), "share")
        self.assertEqual(S.first_form(m(1, False, 0, n_letters=0)), "sticker_or_none")
        self.assertEqual(S.first_form(m(1, False, 0, n_letters=5)), "short")
        self.assertEqual(S.first_form(m(1, False, 0, "<지어낸 질문> ？", n_letters=13)), "question")
        self.assertEqual(S.first_form(m(1, False, 0, "<지어낸 서술문>", n_letters=13)), "statement")


class Room(unittest.TestCase):
    def test_success_room(self):
        # 월요일 01:00 UTC = 10:00 KST(영업시간 안)
        base = 1704070800000  # 2024-01-01T01:00:00Z (월)
        filled = m(5, False, base + 30 * HOUR, form_filled=4, n_letters=40)
        msgs = [m(1, False, base, "請問", n_letters=2), m(2, True, base + 60000, auto="away"),
                m(3, True, base + 30 * 60000), m(4, False, base + 2 * HOUR, n_letters=6, n_emoji=1), filled]
        f = S.room_features({"channel": "instagram"}, msgs, booking("form_filled", filled), "zh-Hant", NAT, None)
        self.assertTrue(f["success"])
        self.assertEqual(f["turns_to_booking"], 3)
        self.assertEqual(f["hours_to_booking"], 30.0)
        self.assertEqual(f["first_response_min"], 30.0)  # 자동응답 뒤 사람 답
        self.assertEqual(f["customer_len_median"], 4)  # 회신 메시지(form_filled 4) 뺌 → median(2, 6)
        self.assertTrue(f["business_hours"])
        self.assertEqual((f["kst_hour"], f["kst_weekday"]), (10, "mon"))
        self.assertTrue(f["emoji_room"])
        self.assertEqual((f["n_customer_msgs"], f["n_owner_msgs"]), (3, 1))

    def test_metrics_excludes_no_customer(self):
        a = S.room_features({"channel": "facebook"}, [m(1, True, 0)], booking("form_sent"), "none", NAT, None)
        b = S.room_features({"channel": "facebook"}, [m(1, False, 0), m(2, True, HOUR * 2)], booking(),
                            "en", NAT, {"topics": ["price"], "procedures": [], "staff_confirmed": 0})
        out = S.metrics([a, b])
        self.assertEqual(out["rooms"]["without_customer"], 1)
        self.assertEqual(out["conversion"]["form_filled"], {"n": 0, "d": 1, "pct": 0.0, "small": True})
        self.assertEqual(out["first_response"]["within_1h"]["n"], 0)
        self.assertEqual(out["topics"]["values"]["price"]["rooms"]["n"], 1)
        self.assertEqual(out["topics"]["labeled_rooms"], 1)

    def test_emoji_skips_form_reply(self):
        """0.2.2 — 예약표 칸이 든 회신(★ · 📝 양식 기호)은 이모지에서 뺀다."""
        filled = m(3, False, 3 * HOUR, "★ <칸> 📝 <칸>", form_filled=4, n_emoji=2)
        msgs = [m(1, False, 0), m(2, True, HOUR), filled]
        f = S.room_features({"channel": "facebook"}, msgs, booking("form_filled", filled), "zh-Hant", NAT, None)
        self.assertFalse(f["emoji_room"])
        self.assertEqual((f["emoji_sum"], f["emoji_msgs"]), (0, 1))
        # 칸 1개만 든 메시지(form_labels 1)도 뺀다
        msgs = [m(1, False, 0, n_emoji=1, form_labels=1), m(2, False, 1, n_emoji=1)]
        f = S.room_features({"channel": "facebook"}, msgs, booking(), "zh-Hant", NAT, None)
        self.assertEqual((f["emoji_sum"], f["emoji_msgs"]), (1, 1))

    def test_photo_split(self):
        filled = m(3, False, 3 * HOUR, form_filled=4, photo=True)
        msgs = [m(1, False, 0), m(2, True, HOUR), filled, m(4, False, 4 * HOUR, photo=True)]
        f = S.room_features({"channel": "facebook"}, msgs, booking("form_filled", filled), "zh-Hant", NAT, None)
        self.assertEqual((f["photo_room"], f["photo_before"], f["photo_after"]), (True, False, True))
        f = S.room_features({"channel": "facebook"}, [m(1, False, 0, photo=True)], booking(), "en", NAT, None)
        self.assertEqual((f["photo_before"], f["photo_after"]), (True, False))

    def test_no_response(self):
        f = S.room_features({"channel": "facebook"}, [m(1, False, 0), m(2, True, 5, auto="system")],
                            booking(), "en", NAT, None)
        self.assertIsNone(f["first_response_min"])


if __name__ == "__main__":
    unittest.main()
