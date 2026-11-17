"""2층 규칙 · LLM 출력 검증 시험 — 지어낸 문장만 쓴다.

opencc 가 필요한 시험은 scripts/.venv(requirements-layer2.txt)로 돌린다. 없으면 건너뛴다.
"""

import os
import sqlite3
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import judge_layer2 as J  # noqa: E402
import label_layer2_llm as LL  # noqa: E402

try:
    import opencc  # noqa: F401
    HAVE_OPENCC = True
except ImportError:
    HAVE_OPENCC = False


class FakeSplit:
    """번간 없이 글자 종류만 보는 시험용(OpenCC 없음)."""

    def counts(self, han):
        return 0, 0


class FieldCount(unittest.TestCase):
    def test_template_empty(self):
        t = "★ 預約資訊\n姓名：\n生日：\n國籍：\n聯絡電話：\n希望預約日期與時間："
        labels, filled, _v = J.count_fields(t)
        self.assertEqual((labels, filled), (5, 0))

    def test_template_filled(self):
        t = "姓名：<X>\n生日：1990/01/01\n國籍：台灣\n聯絡電話：0912000000\n希望預約日期與時間：12/25 下午"
        self.assertEqual(J.count_fields(t)[:2], (5, 5))

    def test_longest_label_first(self):
        # 希望預約日期與時間 이 預約日期 로 쪼개지지 않는다
        labels, filled, values = J.count_fields("希望預約日期與時間：明天")
        self.assertEqual((labels, filled), (1, 1))
        self.assertEqual(list(values), ["date"])

    def test_paren_and_section_removed(self):
        t = "姓名（請填護照英文）：\n★ 其他\n生日(西元)："
        self.assertEqual(J.count_fields(t)[:2], (2, 0))

    def test_value_until_next_label(self):
        labels, filled, _v = J.count_fields("姓名 國籍 台灣")
        self.assertEqual((labels, filled), (2, 1))

    def test_field_value(self):
        self.assertEqual(J.field_value("國籍：台灣\n電話：", "nationality"), "台灣")

    def test_none(self):
        self.assertEqual(J.count_fields(None)[:2], (0, 0))


class AutoReply(unittest.TestCase):
    def test_static(self):
        self.assertEqual(J.static_auto_kind("目前為非營業時間，請填寫"), "off_hours_form")
        self.assertEqual(J.static_auto_kind("感謝您的訊息，我目前不在線，稍後回覆"), "away")
        self.assertEqual(J.static_auto_kind("您好，小編將於工作日回覆"), "off_hours_prefix")
        self.assertEqual(J.static_auto_kind("Customer님이 무언가를 했습니다"), "system")
        self.assertIsNone(J.static_auto_kind("您好！請問想了解哪個療程呢"))
        self.assertIsNone(J.static_auto_kind(None))

    def test_flow(self):
        convs = {}
        for cid in range(1, 12):
            base = cid * 100000
            convs[cid] = {"ch": "facebook", "msgs": [
                {"id": cid * 10 + 1, "seq": 1, "own": False, "ms": base, "content": "預約"},
                {"id": cid * 10 + 2, "seq": 2, "own": True, "ms": base + (2000 if cid < 11 else 9000),
                 "content": "<흐름 문구>"},
            ]}
        J.judge_messages(convs, FakeSplit())
        self.assertEqual(convs[1]["msgs"][1]["auto"], "flow")
        self.assertIsNone(convs[11]["msgs"][1]["auto"])  # 간격 9초
        self.assertIsNone(convs[1]["msgs"][0]["auto"])  # 고객 메시지

    def test_flow_needs_ten(self):
        convs = {cid: {"ch": "instagram", "msgs": [
            {"id": cid * 10 + 1, "seq": 1, "own": False, "ms": 0, "content": "x"},
            {"id": cid * 10 + 2, "seq": 2, "own": True, "ms": 1000, "content": "<문구>"}]} for cid in range(1, 10)}
        J.judge_messages(convs, FakeSplit())
        self.assertIsNone(convs[1]["msgs"][1]["auto"])


class Lang(unittest.TestCase):
    def test_scripts(self):
        f = FakeSplit()
        self.assertEqual(J.message_lang(None, f)[0], "none")
        self.assertEqual(J.message_lang("😀😀 123", f)[0], "none")
        self.assertEqual(J.message_lang("안녕하세요 가격 문의", f)[0], "ko")
        self.assertEqual(J.message_lang("こんにちは料金", f)[0], "ja")
        self.assertEqual(J.message_lang("Hello, how much is it?", f)[0], "en")
        self.assertEqual(J.message_lang("Bonjour madame merci", f)[0], "other")
        self.assertEqual(J.message_lang("สวัสดีครับ", f)[0], "other")
        self.assertEqual(J.message_lang("https://example.invalid/abc 好", f)[1], 1)  # URL 은 세지 않는다
        self.assertEqual(J.message_lang("好 😀", f)[4], 1)

    @unittest.skipUnless(HAVE_OPENCC, "opencc 없음 — scripts/.venv 로 돌린다")
    def test_trad_simp(self):
        s = J.HanSplit()
        self.assertEqual(J.message_lang("請問這個療程價格", s)[0], "zh-Hant")
        self.assertEqual(J.message_lang("请问这个疗程价格", s)[0], "zh-Hans")
        self.assertEqual(J.message_lang("你好", s)[0], "zh")


def room(*msgs):
    out = []
    for i, (own, content, auto, labels, filled) in enumerate(msgs, start=1):
        out.append({"id": i, "seq": i, "own": own, "ms": i * 1000, "content": content, "auto": auto,
                    "lang": "zh-Hant", "n": 4, "trad": 1, "simp": 0, "emoji": 0, "labels": labels,
                    "filled": filled})
    return {"ch": "instagram", "msgs": out}


class Stage(unittest.TestCase):
    def test_filled(self):
        c = room((False, "q", None, 0, 0), (True, "form", None, 5, 0), (False, "a", None, 5, 4))
        J.judge_room(c)
        self.assertEqual(c["stage"]["stage"], "form_filled")
        self.assertEqual(c["stage"]["form_source"], "staff")
        self.assertEqual(c["stage"]["filled"], 3)
        self.assertEqual(c["stage"]["evidence"], 3)

    def test_auto_form_not_sent(self):
        c = room((False, "q", None, 0, 0), (True, "form", "off_hours_form", 5, 0))
        J.judge_room(c)
        self.assertEqual((c["stage"]["stage"], c["stage"]["form_source"]), ("inquiry", "auto"))
        self.assertEqual(c["stage"]["got_auto"], 1)

    def test_flow_form_sent(self):
        c = room((False, "q", None, 0, 0), (True, "form", "flow", 4, 0))
        J.judge_room(c)
        self.assertEqual((c["stage"]["stage"], c["stage"]["form_source"]), ("form_sent", "flow"))
        self.assertEqual(c["stage"]["got_auto"], 0)

    def test_filled_on_auto_form(self):
        c = room((True, "form", "off_hours_form", 5, 0), (False, "a", None, 5, 2))
        J.judge_room(c)
        self.assertEqual(c["stage"]["stage"], "form_filled")
        self.assertEqual(c["reason"], "E-3")

    def test_queue_e1(self):
        c = room((True, "form", None, 5, 0), (False, "a", None, 1, 1))
        J.judge_room(c)
        self.assertEqual((c["stage"]["stage"], c["reason"]), ("form_sent", "E-1"))

    def test_e1_needs_form(self):
        c = room((False, "a", None, 1, 1))
        J.judge_room(c)
        self.assertIsNone(c["reason"])

    def test_queue_e2(self):
        c = room((True, "form", None, 5, 0), (False, "WANG XIAOMING 1990/01/01", None, 0, 0))
        J.judge_room(c)
        self.assertEqual(c["reason"], "E-2")

    def test_handoff(self):
        c = room((False, "q", None, 0, 0), (True, "請加LINE聯繫", None, 0, 0))
        J.judge_room(c)
        self.assertEqual(c["stage"]["handoff"], 1)
        c = room((False, "q", None, 0, 0), (True, "we are online now", None, 0, 0))
        J.judge_room(c)
        self.assertEqual(c["stage"]["handoff"], 0)

    def test_room_lang_absorbs_zh(self):
        c = room((False, "a", None, 0, 0), (False, "b", None, 0, 0))
        c["msgs"][0].update(lang="zh", n=10, trad=0, simp=0)
        c["msgs"][1].update(lang="zh-Hant", n=2, trad=1, simp=0)
        J.judge_room(c)
        self.assertEqual(c["lang"]["lang"], "zh-Hant")
        self.assertEqual(c["lang"]["share"], 1.0)

    def test_data_shape(self):
        self.assertTrue(J.looks_like_data("CHEN DAMING 1988-05-06"))
        self.assertTrue(J.looks_like_data("12/25 1990.1.2"))
        self.assertFalse(J.looks_like_data("請問價格多少"))

    def test_nationality_map(self):
        self.assertEqual(J.map_nationality("台灣"), "TW")
        self.assertEqual(J.map_nationality("R.O.C"), "TW")
        self.assertEqual(J.map_nationality("Hong Kong"), "HK")
        self.assertEqual(J.map_nationality("<알 수 없음>"), "other")


class Rerun(unittest.TestCase):
    """judge 를 두 번 돌리면 규칙 테이블이 같고 l2_llm_label 은 남는다."""

    def test_rerun_same(self):
        tmp = tempfile.TemporaryDirectory()
        try:
            db = os.path.join(tmp.name, "t.sqlite")
            con = sqlite3.connect(db)
            con.executescript(
                "CREATE TABLE conversation (conversation_id INTEGER PRIMARY KEY, channel TEXT);"
                "CREATE TABLE message (message_id INTEGER PRIMARY KEY, conversation_id INTEGER, seq INTEGER, "
                "is_owner INTEGER, sent_at_ms INTEGER, content TEXT);"
                "INSERT INTO conversation VALUES (1, 'instagram'), (2, 'facebook');"
                "INSERT INTO message VALUES (1, 1, 1, 0, 1000, 'Hello, price please'),"
                "(2, 1, 2, 1, 5000, '姓名：\n生日：\n國籍：'), (3, 1, 3, 0, 9000, '姓名：<X>\n生日：1990/1/1\n國籍：台灣'),"
                "(4, 2, 1, 1, 1000, '感謝您的訊息，我目前不在線');")
            con.execute("CREATE TABLE l2_llm_label (conversation_id INTEGER PRIMARY KEY, nationality_mention TEXT, "
                        "confidence REAL, evidence_message_ids TEXT)")
            con.execute("INSERT INTO l2_llm_label VALUES (2, 'US', 0.9, '[4]')")
            con.commit()
            con.close()
            J.run(db, split=FakeSplit())
            con = sqlite3.connect(db)
            dump1 = [r for t in J.RULE_TABLES for r in con.execute("SELECT * FROM %s ORDER BY 1" % t)]
            stage = con.execute("SELECT stage FROM l2_booking_stage WHERE conversation_id = 1").fetchone()[0]
            nat = con.execute("SELECT conversation_id, nationality, source FROM l2_nationality ORDER BY 1").fetchall()
            con.close()
            self.assertEqual(stage, "form_filled")
            self.assertEqual(nat, [(1, "TW", "form"), (2, "US", "self")])
            J.run(db, split=FakeSplit())
            con = sqlite3.connect(db)
            dump2 = [r for t in J.RULE_TABLES for r in con.execute("SELECT * FROM %s ORDER BY 1" % t)]
            self.assertEqual(con.execute("SELECT COUNT(*) FROM l2_llm_label").fetchone()[0], 1)
            con.close()
            self.assertEqual(dump1, dump2)
        finally:
            tmp.cleanup()


class LlmInput(unittest.TestCase):
    """0.3.0 — 예약표 발송(우리 form_labels ≥ 3) · 회신(고객 form_filled ≥ 2) · 자동응답은 LLM 입력에서 뺀다."""

    def test_room_lines_skip_forms(self):
        con = sqlite3.connect(":memory:")
        con.executescript(
            "CREATE TABLE message (message_id INTEGER, conversation_id INTEGER, seq INTEGER, is_owner INTEGER, "
            "content TEXT);"
            "CREATE TABLE l2_message (message_id INTEGER, auto_kind TEXT, form_labels INTEGER, form_filled INTEGER);"
            "INSERT INTO message VALUES (1,1,1,0,'<문의>'),(2,1,2,1,'<예약표>'),(3,1,3,0,'<회신>'),"
            "(4,1,4,1,'<자동응답>'),(5,1,5,0,'<칸 하나 든 말>'),(6,1,6,1,'<안내>'),(7,1,7,0,NULL);"
            "INSERT INTO l2_message VALUES (1,NULL,0,0),(2,NULL,5,0),(3,NULL,5,4),(4,'away',0,0),"
            "(5,NULL,1,1),(6,NULL,2,0),(7,NULL,0,0);")
        self.assertEqual([m for m, _g, _t in LL.room_lines(con, 1)], [1, 5, 6])
        self.assertEqual([g for _m, g, _t in LL.room_lines(con, 1)], ["[C]", "[C]", "[S]"])

    def test_prompt_says_customer_topics_only(self):
        self.assertIn("only what the CUSTOMER", LL.SYSTEM_PROMPT)
        self.assertEqual(LL.VERSION, "llm-0.3.0")


class LlmOutput(unittest.TestCase):
    GOOD = ('{"topics":["price"],"procedures":["ulthera"],"procedures_other":[],"nationality_mention":null,'
            '"staff_confirmed":false,"confidence":0.7,"evidence":[1,2]}')

    def test_good(self):
        r = LL.parse_output(self.GOOD, 2)
        self.assertEqual(r["topics"], ["price"])
        self.assertEqual(r["evidence"], [1, 2])

    def test_fenced_ok(self):
        self.assertEqual(LL.parse_output("```json\n" + self.GOOD + "\n```", 2)["procedures"], ["ulthera"])

    def test_broken_json(self):
        with self.assertRaises(LL.Invalid):
            LL.parse_output('{"topics": ["price"', 2)
        with self.assertRaises(LL.Invalid):
            LL.parse_output("Here is the JSON: " + self.GOOD, 2)

    def test_out_of_list(self):
        for bad in (self.GOOD.replace('"price"', '"cost"'), self.GOOD.replace('"ulthera"', '"hifu"'),
                    self.GOOD.replace("null", '"tw-1"'), self.GOOD.replace("0.7", "1.5"),
                    self.GOOD.replace("false", '"no"'), self.GOOD.replace("[1,2]", "[1,9]"),
                    self.GOOD.replace(',"evidence":[1,2]', ""), self.GOOD[:-1] + ',"extra":1}'):
            with self.assertRaises(LL.Invalid):
                LL.parse_output(bad, 2)

    def test_truncate(self):
        lines = [(i, "[C]", "字" * 1000) for i in range(1, 11)]
        text, cut = LL.build_input(lines)
        self.assertTrue(cut)
        self.assertTrue(text.startswith("1 [C]"))
        self.assertIn("10 [C]", text)
        self.assertLessEqual(sum(len(l) for l in text.split("\n")), 6000 + 200)
        self.assertFalse(LL.build_input(lines[:3])[1])


if __name__ == "__main__":
    unittest.main()
