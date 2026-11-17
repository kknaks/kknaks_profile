"""load_layer1 멈추는 자리(SPEC-001 §5.4 G-1 ~ G-12) 시험 · verify_layer1 대조 시험.

가짜 방 JSON 은 임시 폴더에 매번 새로 짓는다. 원본을 복사하지 않는다.
이름은 전부 `<고객N>` · `<우리IG>` 같은 자리표시다.
"""

import contextlib
import copy
import io
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import load_layer1 as L  # noqa: E402
import verify_layer1 as V  # noqa: E402

IG_ROOT = "your_instagram_activity/messages"
FB_ROOT = "this_profile's_activity_across_facebook/messages"
OWNER_IG = "<우리IG>"
OWNER_FB = "<우리FB>"


def enc(s):
    """원본처럼 이중 인코딩한다(UTF-8 바이트를 latin1 글자로)."""
    return s.encode("utf8").decode("latin1")


def deep_enc(v):
    if isinstance(v, str):
        return enc(v)
    if isinstance(v, list):
        return [deep_enc(x) for x in v]
    if isinstance(v, dict):
        return {k: deep_enc(x) for k, x in v.items()}
    return v


def msg(sender, ts, **extra):
    m = {
        "sender_name": sender,
        "timestamp_ms": ts,
        "is_geoblocked_for_viewer": False,
        "is_unsent_image_by_messenger_kid_parent": False,
    }
    m.update(extra)
    return m


def room(thread_path, owner, other, messages, title=None, **extra):
    r = {
        "participants": [{"name": other}, {"name": owner}],
        "messages": messages,
        "title": title if title is not None else other,
        "is_still_participant": True,
        "thread_path": thread_path,
        "magic_words": [],
    }
    r.update(extra)
    return r


def base_rooms():
    """{상대 경로: 방 dict} — 복원 전 값(시험에서 enc 해 쓴다)."""
    return {
        IG_ROOT + "/inbox/p1_1/message_1.json": room(
            "inbox/p1_1", OWNER_IG, "<고객1>", [
                msg(OWNER_IG, 1700000003000, content="<답1>",
                    reactions=[{"actor": "<고객1>", "reaction": "<반응>"}]),
                msg("<고객1>", 1700000002000, content="<문의1>",
                    photos=[{"uri": IG_ROOT + "/inbox/p1_1/photos/a.jpg", "creation_timestamp": 1700000002}],
                    share={"link": "https://example.invalid/x"}),
                msg(OWNER_IG, 1700000001000, content="<인사>"),
            ]),
        IG_ROOT + "/inbox/p2_2/message_1.json": room(
            "inbox/p2_2", OWNER_IG, "<고객2>", [
                msg(OWNER_IG, 1700000005000, content="<답2>"),
                msg("<고객2>", 1700000004000, content="<문의2>"),
            ]),
        IG_ROOT + "/message_requests/p3_3/message_1.json": room(
            "message_requests/p3_3", OWNER_IG, "<고객3>", [
                msg(OWNER_IG, 1700000006000, content="<답3>"),
            ], is_pending=True, joinable_mode={"mode": 1, "link": ""}),
        IG_ROOT + "/message_requests/loose.json": room(
            "message_requests/p4_4", OWNER_IG, "<고객4>", [
                msg("<고객4>", 1700000007000, content="<문의4>"),
            ]),
        FB_ROOT + "/inbox/q1_1/message_1.json": room(
            "inbox/q1_1", OWNER_FB, "<고객5>", [
                msg(OWNER_FB, 1700000009000, sticker={"uri": FB_ROOT + "/stickers_used/s.png", "ai_stickers": []}),
                msg("<고객5>", 1700000008000, content="<문의5>",
                    files=[{"uri": FB_ROOT + "/inbox/q1_1/files/f.pdf", "creation_timestamp": 1700000008}]),
            ], title="<제목5>"),
        FB_ROOT + "/filtered_threads/q2_2/message_1.json": room(
            "filtered_threads/q2_2", OWNER_FB, "<고객6>", [
                msg(OWNER_FB, 1700000011000, content="<답6>"),
                msg(OWNER_FB, 1700000010000, content="<답6b>", call_duration=0),
            ], title="<제목6>"),
    }


class Fixture:
    def __init__(self, rooms, extra_files=(), raw=(), raw_bytes=()):
        self.tmp = tempfile.TemporaryDirectory()
        self.source = os.path.join(self.tmp.name, "src")
        self.db = os.path.join(self.tmp.name, "out", "layer1.sqlite")
        for rel, data in rooms.items():
            self._write(rel, json.dumps(deep_enc(data)))
        for rel, text in raw:
            self._write(rel, text)
        for rel in extra_files:
            self._write(rel, "x")
        for rel, data in raw_bytes:
            p = os.path.join(self.source, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(data)
        for rel in (IG_ROOT + "/inbox/p1_1/photos/a.jpg", FB_ROOT + "/inbox/q1_1/files/f.pdf",
                    FB_ROOT + "/stickers_used/s.png", IG_ROOT + "/secret_conversations.json"):
            if not os.path.exists(os.path.join(self.source, rel)):
                self._write(rel, "x")

    def _write(self, rel, text):
        p = os.path.join(self.source, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="ascii") as fh:
            fh.write(text)

    def close(self):
        self.tmp.cleanup()


def quiet(fn, *a):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = fn(*a)
    return code, out.getvalue(), err.getvalue()


class LoadOk(unittest.TestCase):
    def test_loads_and_is_repeatable(self):
        fx = Fixture(base_rooms())
        try:
            code, out, err = quiet(L.main, ["--source", fx.source, "--db", fx.db])
            self.assertEqual(code, 0, err)
            self.assertFalse(os.path.exists(fx.db + ".tmp"))
            con = sqlite3.connect(fx.db)
            tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
            self.assertEqual(tables, sorted(L.TABLES))
            convs = con.execute("SELECT conversation_id, channel FROM conversation ORDER BY 1").fetchall()
            self.assertEqual([c for _i, c in convs], ["facebook"] * 2 + ["instagram"] * 4)
            # 복원 · seq · 우리 계정
            row = con.execute("SELECT seq, source_idx, is_owner, customer_id, content, sent_at FROM message "
                              "WHERE conversation_id = 3 ORDER BY seq").fetchall()
            self.assertEqual([r[0] for r in row], [1, 2, 3])
            self.assertEqual([r[1] for r in row], [2, 1, 0])
            self.assertEqual([r[2] for r in row], [1, 0, 1])
            self.assertIsNotNone(row[1][3])
            self.assertEqual(row[0][4], "<인사>")
            self.assertEqual(row[0][5], "2023-11-14T22:13:21.000Z")
            self.assertEqual(con.execute("SELECT kind, item_idx, created_at_s FROM attachment WHERE kind='sticker'")
                             .fetchall(), [("sticker", 0, None)])
            dump1 = list(con.iterdump())
            con.close()
            code, _o, err = quiet(L.main, ["--source", fx.source, "--db", fx.db])
            self.assertEqual(code, 0, err)
            con = sqlite3.connect(fx.db)
            self.assertEqual(list(con.iterdump()), dump1)
            con.close()
        finally:
            fx.close()

    def test_output_has_no_names(self):
        fx = Fixture(base_rooms())
        try:
            _c, out, err = quiet(L.main, ["--source", fx.source, "--db", fx.db])
            for word in ("<고객", "<우리", "p1_1", "inbox/", "<문의"):
                self.assertNotIn(word, out + err)
        finally:
            fx.close()

    def test_verify_matches_own_source(self):
        """verify 의 원본 재집계와 DB 읽기가 같은 값을 낸다(기준 값은 실원본용이라 비교하지 않는다)."""
        fx = Fixture(base_rooms())
        try:
            self.assertEqual(quiet(L.main, ["--source", fx.source, "--db", fx.db])[0], 0)
            src, sx = V.normalize_source(fx.source)
            db, dx = V.normalize_db(fx.db)
            fns = [fn if fn is not None else V._uri_exists(fx.source) for *_x, fn in V.LINES]
            for fn in fns:
                for scope in (V.IG, V.FB, "합"):
                    s = V.evaluate(fn, src, sx, scope)
                    d = V.evaluate(fn, db, dx, scope)
                    if fn == "E-04":
                        continue
                    self.assertEqual(s, d, (fn, scope))
        finally:
            fx.close()


class VerifyReadFail(unittest.TestCase):
    def test_verify_stops_with_location(self):
        fx = Fixture(base_rooms())
        try:
            self.assertEqual(quiet(L.main, ["--source", fx.source, "--db", fx.db])[0], 0)
            with open(os.path.join(fx.source, FB_ROOT, "inbox", "q1_1", "message_1.json"), "wb") as fh:
                fh.write(b"{broken")
            code, out, err = quiet(V.main, ["--source", fx.source, "--db", fx.db])
            self.assertEqual(code, 1)
            self.assertIn("G-13 · facebook · inbox · 1번째 방", err)
            self.assertNotIn("예기치 않은", err)
            self.assertNotIn("q1_1", out + err)
        finally:
            fx.close()


class Stops(unittest.TestCase):
    def assertStops(self, rule, rooms=None, mutate=None, **fx_kw):
        rooms = copy.deepcopy(rooms if rooms is not None else base_rooms())
        if mutate:
            mutate(rooms)
        fx = Fixture(rooms, **fx_kw)
        try:
            # 이전 DB 가 있으면 건드리지 않아야 한다
            os.makedirs(os.path.dirname(fx.db), exist_ok=True)
            with open(fx.db, "wb") as fh:
                fh.write(b"previous")
            with self.assertRaises(L.Stop) as cm:
                L.load(fx.source, fx.db)
            self.assertEqual(cm.exception.rule, rule)
            code, out, err = quiet(L.main, ["--source", fx.source, "--db", fx.db])
            self.assertNotEqual(code, 0)
            self.assertIn(rule, err)
            self.assertNotIn("<고객", out + err)
            with open(fx.db, "rb") as fh:
                self.assertEqual(fh.read(), b"previous")
            self.assertFalse(os.path.exists(fx.db + ".tmp"))
        finally:
            fx.close()

    @staticmethod
    def _first_msg(rooms, rel=IG_ROOT + "/inbox/p1_1/message_1.json", i=0):
        return rooms[rel]["messages"][i]

    def test_g1_unknown_message_key(self):
        self.assertStops("G-1", mutate=lambda r: self._first_msg(r).update(unknown_key=1))

    def test_g1_unknown_nested_key(self):
        self.assertStops("G-1", mutate=lambda r: self._first_msg(r, i=1)["photos"][0].update(extra="x"))

    def test_g1_gifs_creation_timestamp(self):
        self.assertStops("G-1", mutate=lambda r: self._first_msg(r).update(
            gifs=[{"uri": "u", "creation_timestamp": 1}]))

    def test_g1_unknown_room_key(self):
        self.assertStops("G-1", mutate=lambda r: r[IG_ROOT + "/inbox/p2_2/message_1.json"].update(other=[]))

    def test_g2_share_is_list(self):
        self.assertStops("G-2", mutate=lambda r: self._first_msg(r).update(share=[{"link": "x"}]))

    def test_g2_sticker_is_list(self):
        self.assertStops("G-2", mutate=lambda r: self._first_msg(r).update(sticker=[{"uri": "x"}]))

    def test_g2_timestamp_is_string(self):
        self.assertStops("G-2", mutate=lambda r: self._first_msg(r).update(timestamp_ms="1"))

    def test_g3_restore_fails(self):
        # 원본 JSON 에 직접 쓴 값: latin1 로 못 바꾸는 글자(인코딩 전 값이 이미 U+00FF 밖)
        rooms = base_rooms()
        rel = IG_ROOT + "/inbox/p2_2/message_1.json"
        data = deep_enc(rooms.pop(rel))
        data["messages"][0]["content"] = "Ā"
        self.assertStops("G-3", rooms=rooms, raw=[(rel, json.dumps(data))])

    def test_g3_invalid_utf8(self):
        rooms = base_rooms()
        rel = IG_ROOT + "/inbox/p2_2/message_1.json"
        data = deep_enc(rooms.pop(rel))
        data["messages"][0]["content"] = "ÿ"
        self.assertStops("G-3", rooms=rooms, raw=[(rel, json.dumps(data))])

    def test_g4_thread_path_mismatch(self):
        self.assertStops("G-4", mutate=lambda r: r[IG_ROOT + "/inbox/p2_2/message_1.json"].update(
            thread_path="inbox/other_9"))

    def test_g4_loose_wrong_box(self):
        self.assertStops("G-4", mutate=lambda r: r[IG_ROOT + "/message_requests/loose.json"].update(
            thread_path="inbox/p4_4"))

    def test_g4_duplicate_thread_path(self):
        self.assertStops("G-4", mutate=lambda r: r[IG_ROOT + "/message_requests/loose.json"].update(
            thread_path="message_requests/p3_3"))

    def test_g5_two_files(self):
        rooms = base_rooms()
        extra = rooms[IG_ROOT + "/inbox/p2_2/message_1.json"]
        rooms[IG_ROOT + "/inbox/p2_2/message_2.json"] = copy.deepcopy(extra)
        self.assertStops("G-5", rooms=rooms)

    def test_g5_no_file(self):
        self.assertStops("G-5", extra_files=[IG_ROOT + "/inbox/p9_9/photos/a.jpg"])

    def test_g6_no_common_owner(self):
        def m(r):
            room_ = r[IG_ROOT + "/inbox/p2_2/message_1.json"]
            room_["participants"] = [{"name": "<고객2>"}, {"name": "<다른계정>"}]
            room_["messages"][0]["sender_name"] = "<다른계정>"
        self.assertStops("G-6", mutate=m)

    def test_g6_owner_not_top_sender(self):
        def m(r):
            rel = FB_ROOT + "/inbox/q1_1/message_1.json"
            r[rel]["messages"] = [msg("<고객5>", 1700000009100 - i) for i in range(10)] + r[rel]["messages"]
        self.assertStops("G-6", mutate=m)

    def test_g7_sender_not_participant(self):
        self.assertStops("G-7", mutate=lambda r: self._first_msg(r).update(sender_name="<남>"))

    def test_g7_actor_not_participant(self):
        self.assertStops("G-7", mutate=lambda r: self._first_msg(r).update(
            reactions=[{"actor": "<남>", "reaction": "<반응>"}]))

    def test_g8_not_descending(self):
        self.assertStops("G-8", mutate=lambda r: self._first_msg(r).update(timestamp_ms=1))

    def test_g9_magic_words(self):
        self.assertStops("G-9", mutate=lambda r: r[IG_ROOT + "/inbox/p2_2/message_1.json"].update(
            magic_words=["<말>"]))

    def test_g9_ai_stickers(self):
        self.assertStops("G-9", mutate=lambda r: r[FB_ROOT + "/inbox/q1_1/message_1.json"]["messages"][0]
                         ["sticker"].update(ai_stickers=["x"]))

    def test_g10_empty_share(self):
        self.assertStops("G-10", mutate=lambda r: self._first_msg(r).update(share={}))

    def test_g11_duplicate_participant(self):
        self.assertStops("G-11", mutate=lambda r: r[IG_ROOT + "/inbox/p2_2/message_1.json"]["participants"]
                         .append({"name": "<고객2>"}))

    def test_g12_unknown_box(self):
        self.assertStops("G-12", extra_files=[IG_ROOT + "/archived/p8_8/message_1.json"])

    def test_g12_plain_file_in_box(self):
        self.assertStops("G-12", extra_files=[IG_ROOT + "/inbox/notes.txt"])

    def test_g12_plain_file_message_shown_without_name(self):
        fx = Fixture(base_rooms(), extra_files=[FB_ROOT + "/filtered_threads/zz_unknown.bin"])
        try:
            code, out, err = quiet(L.main, ["--source", fx.source, "--db", fx.db])
            self.assertNotEqual(code, 0)
            self.assertIn("G-12", err)
            self.assertIn("facebook · filtered_threads", err)
            self.assertNotIn("zz_unknown", out + err)
        finally:
            fx.close()

    def _broken(self, data):
        rooms = base_rooms()
        rel = IG_ROOT + "/inbox/p2_2/message_1.json"
        rooms.pop(rel)
        return rooms, [(rel, data)]

    def test_g13_non_ascii_bytes(self):
        # \uc774\uc2a4\ucf00\uc774\ud504\uac00 \uc544\ub2cc \ub0a0 UTF-8 \ubc14\uc774\ud2b8\uac00 \ub4e0 \ud30c\uc77c(\uadf8 \ubc16\uc740 \uc62c\ubc14\ub978 JSON)
        rooms, rb = self._broken(b'{"title": "\xc3\xa9"}')
        self.assertStops("G-13", rooms=rooms, raw_bytes=rb)

    def test_g13_broken_json(self):
        rooms, rb = self._broken(b'{"participants": [')
        self.assertStops("G-13", rooms=rooms, raw_bytes=rb)

    def test_g13_cannot_open_directory(self):
        # message_1.json 이 파일이 아니라 폴더 — 열기 오류
        rooms = base_rooms()
        rooms.pop(IG_ROOT + "/inbox/p2_2/message_1.json")
        self.assertStops("G-13", rooms=rooms, extra_files=[IG_ROOT + "/inbox/p2_2/message_1.json/x"])

    @unittest.skipIf(hasattr(os, "geteuid") and os.geteuid() == 0, "root 는 권한을 무시한다")
    def test_g13_cannot_open_permission(self):
        fx = Fixture(base_rooms())
        target = os.path.join(fx.source, IG_ROOT, "inbox", "p2_2", "message_1.json")
        try:
            os.chmod(target, 0)
            with self.assertRaises(L.Stop) as cm:
                L.load(fx.source, fx.db)
            self.assertEqual(cm.exception.rule, "G-13")
            self.assertIn("instagram · inbox · 2번째 방", cm.exception.describe())
            self.assertFalse(os.path.exists(fx.db))
        finally:
            os.chmod(target, 0o644)
            fx.close()

    def test_g13_location_in_message(self):
        rooms, rb = self._broken(b"not json")
        fx = Fixture(rooms, raw_bytes=rb)
        try:
            code, out, err = quiet(L.main, ["--source", fx.source, "--db", fx.db])
            self.assertEqual(code, 1)
            self.assertIn("G-13 · instagram · inbox · 2번째 방", err)
            self.assertNotIn("예기치 않은", err)
            self.assertNotIn("p2_2", out + err)
        finally:
            fx.close()

    def test_g6_top_sender_tie(self):
        # FB 우리 계정 발신 3건 — 상대도 3건이 되게 해 최다 발신자 동률
        def m(r):
            rel = FB_ROOT + "/inbox/q1_1/message_1.json"
            r[rel]["messages"] = [msg("<고객5>", 1700000009200), msg("<고객5>", 1700000009100)] + r[rel]["messages"]
        self.assertStops("G-6", mutate=m)

    def test_g6_channel_without_rooms(self):
        rooms = {k: v for k, v in base_rooms().items() if k.startswith(IG_ROOT)}
        fx = Fixture(rooms)
        try:
            shutil.rmtree(os.path.join(fx.source, FB_ROOT, "inbox"))  # FB 메시지 루트 · stickers_used 만 남김
            with self.assertRaises(L.Stop) as cm:
                L.load(fx.source, fx.db)
            self.assertEqual(cm.exception.rule, "G-6")
            self.assertFalse(os.path.exists(fx.db))
        finally:
            fx.close()

    def test_g12_missing_root(self):
        fx_rooms = {k: v for k, v in base_rooms().items() if k.startswith(IG_ROOT)}
        # FB 메시지 루트를 아예 만들지 않는다
        tmp = tempfile.TemporaryDirectory()
        try:
            src = os.path.join(tmp.name, "src")
            for rel, data in fx_rooms.items():
                p = os.path.join(src, rel)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, "w", encoding="ascii") as fh:
                    json.dump(deep_enc(data), fh)
            with self.assertRaises(L.Stop) as cm:
                L.load(src, os.path.join(tmp.name, "x.sqlite"))
            self.assertEqual(cm.exception.rule, "G-12")
            self.assertFalse(os.path.exists(os.path.join(tmp.name, "x.sqlite")))
        finally:
            tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
