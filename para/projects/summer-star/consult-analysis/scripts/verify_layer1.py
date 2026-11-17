#!/usr/bin/env python3
"""1층 대조 — SPEC-001 §7 건수 기준 · 원본 재집계 · DB 세 값을 줄마다 · 칸(IG · FB · 합)마다 비교.

계약: para/projects/summer-star/consult-analysis/20-spec/spec-001-layer1-schema.md (SPEC-001 0.2.0 §6.3 · §7)

- 적재 코드(load_layer1)를 불러 쓰지 않는다. 원본은 여기서 따로 다시 읽고 센다.
- 전부 같으면 종료 코드 0 · 하나라도 다르면 1.
- 출력은 건수와 규칙 번호만(§6.3).
"""

import argparse
import datetime
import json
import os
import sqlite3
import statistics
import sys

IG, FB = "instagram", "facebook"
ROOTS = {
    IG: "your_instagram_activity/messages",
    FB: "this_profile's_activity_across_facebook/messages",
}
KINDS = ("photos", "videos", "files", "gifs", "audio_files", "sticker")
SHARE_KEYS = ("link", "share_text", "original_content_owner", "profile_share_name", "profile_share_username")
SHARE_COLS = ("share_link", "share_text", "share_original_content_owner",
              "share_profile_share_name", "share_profile_share_username")  # SHARE_KEYS 와 같은 순서
SKIP_DIRS = ("stickers_used",)


def bad_char(s):
    return any(0x80 <= ord(ch) <= 0x9F or ch == "�" for ch in s)


# ================================================================ 원본 재집계

class Tally:
    def __init__(self):
        self.strings = 0
        self.fails = 0
        self.c1 = 0


def fix(value, tally):
    """모든 문자열 값을 복원하며 센다. 실패는 세고 원래 값을 둔다(대조용 — 적재는 멈춘다)."""
    if isinstance(value, str):
        tally.strings += 1
        try:
            out = value.encode("latin1").decode("utf8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            tally.fails += 1
            return value
        if bad_char(out):
            tally.c1 += 1
        return out
    if isinstance(value, list):
        return [fix(v, tally) for v in value]
    if isinstance(value, dict):
        return {k: fix(v, tally) for k, v in value.items()}
    return value


class ReadFail(Exception):
    """원본 방 JSON 을 못 읽음. 메시지에는 규칙 번호 · 채널 · 보관함 · 방 순번만."""


def source_rooms(source):
    """원본 방 JSON 을 채널 · 보관함과 함께 읽는다."""
    out = []
    tallies = {IG: Tally(), FB: Tally()}
    for ch, root_rel in ROOTS.items():
        root = os.path.join(source, root_rel)
        if not os.path.isdir(root):
            continue
        for box in sorted(os.listdir(root)):
            bdir = os.path.join(root, box)
            if box.startswith(".") or box in SKIP_DIRS or not os.path.isdir(bdir):
                continue
            n = 0
            for entry in sorted(os.listdir(bdir)):
                if entry.startswith("."):
                    continue
                full = os.path.join(bdir, entry)
                if os.path.isdir(full) or entry.endswith(".json"):
                    n += 1
                if os.path.isdir(full):
                    files = sorted(f for f in os.listdir(full) if f.startswith("message_") and f.endswith(".json"))
                    rels = ["/".join((root_rel, box, entry, f)) for f in files]
                elif entry.endswith(".json"):
                    rels = ["/".join((root_rel, box, entry))]
                else:
                    rels = []
                for rel in rels:
                    try:
                        with open(os.path.join(source, rel), encoding="ascii") as fh:
                            raw = json.load(fh)
                    except (OSError, ValueError):  # 열기 오류 · 비 ASCII 바이트 · JSON 깨짐
                        raise ReadFail("G-13 · %s · %s · %d번째 방" % (ch, box, n)) from None
                    data = fix(raw, tallies[ch])
                    out.append((ch, box, rel, data))
    return out, tallies


def ms_to_iso(ms):
    sec, milli = divmod(ms, 1000)
    t = datetime.datetime.fromtimestamp(sec, tz=datetime.timezone.utc)
    return "%04d-%02d-%02dT%02d:%02d:%02d.%03dZ" % (t.year, t.month, t.day, t.hour, t.minute, t.second, milli)


def normalize_source(source):
    raw, tallies = source_rooms(source)
    owners = {}
    for ch in ROOTS:
        common = None
        for c, _b, _r, d in raw:
            if c != ch:
                continue
            names = {p.get("name") for p in d.get("participants", [])}
            common = names if common is None else common & names
        owners[ch] = next(iter(common)) if common and len(common) == 1 else None

    convs = []
    for ch, box, rel, d in raw:
        owner = owners[ch]
        names = [p.get("name") for p in d.get("participants", [])]
        jm = d.get("joinable_mode")
        msgs = []
        for m in d.get("messages", []):
            share = m.get("share") or {}
            atts = []
            for k in KINDS:
                if k in m:
                    items = [m[k]] if k == "sticker" else m[k]
                    for it in items:
                        atts.append((k, it.get("uri"), it.get("creation_timestamp")))
            sender = m.get("sender_name")
            mine = sender == owner
            msgs.append({
                "is_owner": mine,
                "linked": (not mine) and sender in names,
                "ts": m.get("timestamp_ms"),
                "sent_at": ms_to_iso(m["timestamp_ms"]),
                "content": m.get("content"),
                "call": m.get("call_duration"),
                "geo": bool(m.get("is_geoblocked_for_viewer")),
                "kid": bool(m.get("is_unsent_image_by_messenger_kid_parent")),
                "share": tuple(share.get(k) for k in SHARE_KEYS),
                "atts": atts,
                "reacts": [(r.get("actor"), r.get("actor") == owner, r.get("reaction")) for r in m.get("reactions", [])],
            })
        convs.append({
            "ch": ch, "box": box, "thread_path": d.get("thread_path"), "source_file": rel,
            "title": d.get("title"), "owner": owner,
            "owner_seq": names.index(owner) if owner in names else None,
            "still": bool(d.get("is_still_participant")),
            "pending": d.get("is_pending"),
            "jmode": jm.get("mode") if jm else None,
            "jlink": jm.get("link") if jm else None,
            "customers": [n for n in names if n != owner],
            "msgs": msgs,
        })
    extra = {}
    for ch, t in tallies.items():
        extra[ch] = {"E-01": t.c1, "E-03": t.strings, "E-04": t.fails}
    return convs, extra


# ================================================================ DB 읽기

def normalize_db(db):
    con = sqlite3.connect("file:%s?mode=ro" % os.path.abspath(db), uri=True)
    con.row_factory = sqlite3.Row
    try:
        convs = {}
        order = []
        for r in con.execute("SELECT * FROM conversation ORDER BY conversation_id"):
            convs[r["conversation_id"]] = {
                "ch": r["channel"], "box": r["box"], "thread_path": r["thread_path"],
                "source_file": r["source_file"], "title": r["title"], "owner": r["owner_name"],
                "owner_seq": r["owner_participant_seq"], "still": r["is_still_participant"] == 1,
                "pending": r["is_pending"], "jmode": r["joinable_mode"], "jlink": r["joinable_link"],
                "customers": [], "msgs": [],
            }
            order.append(r["conversation_id"])
        for r in con.execute("SELECT conversation_id, name FROM customer ORDER BY customer_id"):
            convs[r["conversation_id"]]["customers"].append(r["name"])
        msgs = {}
        for r in con.execute("SELECT * FROM message ORDER BY message_id"):
            m = {
                "is_owner": r["is_owner"] == 1,
                "linked": r["is_owner"] == 0 and r["customer_id"] is not None,
                "ts": r["sent_at_ms"], "sent_at": r["sent_at"], "content": r["content"],
                "call": r["call_duration"], "geo": r["is_geoblocked_for_viewer"] == 1,
                "kid": r["is_unsent_image_by_messenger_kid_parent"] == 1,
                "share": tuple(r[k] for k in SHARE_COLS),
                "atts": [], "reacts": [],
            }
            msgs[r["message_id"]] = m
            convs[r["conversation_id"]]["msgs"].append(m)
        for r in con.execute("SELECT * FROM attachment ORDER BY attachment_id"):
            msgs[r["message_id"]]["atts"].append((r["kind"], r["uri"], r["created_at_s"]))
        for r in con.execute("SELECT * FROM reaction ORDER BY reaction_id"):
            msgs[r["message_id"]]["reacts"].append((r["actor"], r["is_owner"] == 1, r["reaction"]))

        # E-01 · E-03 — DB 쪽 값
        ch_of_conv = {cid: c["ch"] for cid, c in convs.items()}
        extra = {IG: {"E-01": 0, "E-03": 0, "E-04": None}, FB: {"E-01": 0, "E-03": 0, "E-04": None}}
        tables = {
            "conversation": "SELECT c.conversation_id AS k, c.* FROM conversation c",
            "customer": "SELECT x.conversation_id AS k, x.* FROM customer x",
            "message": "SELECT x.conversation_id AS k, x.* FROM message x",
            "attachment": "SELECT m.conversation_id AS k, a.* FROM attachment a JOIN message m USING (message_id)",
            "reaction": "SELECT m.conversation_id AS k, x.* FROM reaction x JOIN message m USING (message_id)",
        }
        for sql in tables.values():
            for r in con.execute(sql):
                ch = ch_of_conv[r["k"]]
                for v in tuple(r)[1:]:
                    if isinstance(v, str) and bad_char(v):
                        extra[ch]["E-01"] += 1
    finally:
        con.close()

    # 원본 문자열 값 = title · thread_path · 참가자 이름(우리 계정 1 + 상대) · joinable_mode.link
    #   · sender_name · content · share.* · 첨부 uri · reactions[].actor · reactions[].reaction
    for cid in order:
        c = convs[cid]
        n = 3 + (c["jlink"] is not None) + len(c["customers"])
        for m in c["msgs"]:
            n += 1 + (m["content"] is not None) + sum(v is not None for v in m["share"])
            n += len(m["atts"]) + 2 * len(m["reacts"])
        extra[c["ch"]]["E-03"] += n
    return [convs[cid] for cid in order], extra


# ================================================================ §7 의 줄

def _msgs(cs):
    return [m for c in cs for m in c["msgs"]]


def _atts(cs):
    return [(c, m, a) for c in cs for m in c["msgs"] for a in m["atts"]]


def _reacts(cs):
    return [r for c in cs for m in c["msgs"] for r in m["reacts"]]


def _is_loose(c):
    return os.path.dirname(c["source_file"]) == ROOTS[c["ch"]] + "/" + c["box"]


def _median(vals):
    v = statistics.median(vals)
    return int(v) if v == int(v) else v


def _kind(cs, k):
    return sum(1 for _c, _m, a in _atts(cs) if a[0] == k)


def _msgs_with_kind(cs, k):
    return sum(1 for m in _msgs(cs) if any(a[0] == k for a in m["atts"]))


def _photo_count(m):
    return sum(1 for a in m["atts"] if a[0] == "photos")


def _null_cts(cs, k):
    return sum(1 for _c, _m, a in _atts(cs) if a[0] == k and a[2] is None)


def _empty_msg(m):
    return (m["content"] is None and m["call"] is None and all(v is None for v in m["share"])
            and not m["atts"] and not m["reacts"])


def _non_ascii(s):
    return s is not None and any(ord(ch) > 127 for ch in s)


def _uri_exists(source):
    def fn(cs):
        return sum(1 for _c, _m, a in _atts(cs) if os.path.isfile(os.path.join(source, a[1])))
    return fn


STICKER_DIR = ROOTS[FB] + "/stickers_used/"

# (번호, 무엇, 기준 IG, 기준 FB, 기준 합(None = 합 없음), 함수)
LINES = [
    ("C-01", "conversation 행", 511, 1405, 1916, lambda cs: len(cs)),
    ("C-02", "box = inbox", 495, 1404, 1899, lambda cs: sum(c["box"] == "inbox" for c in cs)),
    ("C-03", "box = message_requests", 16, 0, 16, lambda cs: sum(c["box"] == "message_requests" for c in cs)),
    ("C-04", "box = filtered_threads", 0, 1, 1, lambda cs: sum(c["box"] == "filtered_threads" for c in cs)),
    ("C-05", "source_file 이 폴더 밖 JSON", 1, 0, 1, lambda cs: sum(_is_loose(c) for c in cs)),
    ("C-06", "is_still_participant = 1", 511, 0, 511, lambda cs: sum(c["still"] for c in cs)),
    ("C-07", "is_pending NULL 아님", 16, 0, 16, lambda cs: sum(c["pending"] is not None for c in cs)),
    ("C-07", "  └ is_pending = 1", 16, 0, 16, lambda cs: sum(c["pending"] is not None and int(c["pending"]) == 1 for c in cs)),
    ("C-07", "  └ is_pending NULL 아님 · message_requests", 16, 0, 16,
     lambda cs: sum(c["pending"] is not None and c["box"] == "message_requests" for c in cs)),
    ("C-08", "joinable_mode NULL 아님", 16, 0, 16, lambda cs: sum(c["jmode"] is not None for c in cs)),
    ("C-08", "  └ joinable_mode = 1", 16, 0, 16, lambda cs: sum(c["jmode"] == 1 for c in cs)),
    ("C-08", "  └ joinable_link = 빈 문자열", 16, 0, 16, lambda cs: sum(c["jlink"] == "" for c in cs)),
    ("C-08", "  └ joinable_mode NULL 아님 · inbox", 15, 0, 15,
     lambda cs: sum(c["jmode"] is not None and c["box"] == "inbox" for c in cs)),
    ("C-08", "  └ joinable_mode NULL 아님 · message_requests", 1, 0, 1,
     lambda cs: sum(c["jmode"] is not None and c["box"] == "message_requests" for c in cs)),
    ("C-09", "owner_name 값 종류", 1, 1, 2, lambda cs: len({c["owner"] for c in cs})),
    ("C-10", "owner_participant_seq = 1", 497, 1405, 1902, lambda cs: sum(c["owner_seq"] == 1 for c in cs)),
    ("C-10", "owner_participant_seq = 0", 14, 0, 14, lambda cs: sum(c["owner_seq"] == 0 for c in cs)),
    ("C-11", "customer 행", 510, 1405, 1915, lambda cs: sum(len(c["customers"]) for c in cs)),
    ("C-12", "customer.name 값 종류", 501, 1391, None, lambda cs: len({n for c in cs for n in c["customers"]})),
    ("C-13", "customer 행이 없는 conversation", 1, 0, 1, lambda cs: sum(not c["customers"] for c in cs)),
    ("C-14", "title = 그 방 customer.name", 510, 0, 510, lambda cs: sum(c["title"] in c["customers"] for c in cs)),
    ("C-15", "(channel, thread_path) 값 종류", 511, 1405, 1916, lambda cs: len({(c["ch"], c["thread_path"]) for c in cs})),
    ("C-15", "thread_path 값 종류", 511, 1405, 1916, lambda cs: len({c["thread_path"] for c in cs})),

    ("M-01", "message 행", 7094, 21612, 28706, lambda cs: len(_msgs(cs))),
    ("M-02", "inbox 방의 메시지", 7067, 21574, 28641, lambda cs: sum(len(c["msgs"]) for c in cs if c["box"] == "inbox")),
    ("M-03", "message_requests 방의 메시지", 27, 0, 27,
     lambda cs: sum(len(c["msgs"]) for c in cs if c["box"] == "message_requests")),
    ("M-03", "filtered_threads 방의 메시지", 0, 38, 38,
     lambda cs: sum(len(c["msgs"]) for c in cs if c["box"] == "filtered_threads")),
    ("M-04", "is_owner = 1", 4617, 15363, 19980, lambda cs: sum(m["is_owner"] for m in _msgs(cs))),
    ("M-05", "is_owner = 0", 2477, 6249, 8726, lambda cs: sum(not m["is_owner"] for m in _msgs(cs))),
    ("M-05", "  └ is_owner = 0 · customer_id NULL 아님", 2477, 6249, 8726, lambda cs: sum(m["linked"] for m in _msgs(cs))),
    ("M-06", "content NULL 아님", 6374, 19126, 25500, lambda cs: sum(m["content"] is not None for m in _msgs(cs))),
    ("M-07", "call_duration NULL 아님", 3, 33, 36, lambda cs: sum(m["call"] is not None for m in _msgs(cs))),
    ("M-07", "call_duration 0 아님", 0, 1, 1, lambda cs: sum(m["call"] not in (None, 0) for m in _msgs(cs))),
    ("M-08", "is_geoblocked_for_viewer = 1", 0, 0, 0, lambda cs: sum(m["geo"] for m in _msgs(cs))),
    ("M-09", "is_unsent_image_by_messenger_kid_parent = 1", 0, 0, 0, lambda cs: sum(m["kid"] for m in _msgs(cs))),
    ("M-10", "share_* 하나라도 NULL 아님", 107, 51, 158,
     lambda cs: sum(any(v is not None for v in m["share"]) for m in _msgs(cs))),
    ("M-11", "share_link NULL 아님", 104, 51, 155, lambda cs: sum(m["share"][0] is not None for m in _msgs(cs))),
    ("M-11", "share_text NULL 아님", 72, 9, 81, lambda cs: sum(m["share"][1] is not None for m in _msgs(cs))),
    ("M-12", "share_original_content_owner NULL 아님", 50, 0, 50, lambda cs: sum(m["share"][2] is not None for m in _msgs(cs))),
    ("M-12", "share_profile_share_name NULL 아님", 4, 0, 4, lambda cs: sum(m["share"][3] is not None for m in _msgs(cs))),
    ("M-12", "share_profile_share_username NULL 아님", 4, 0, 4, lambda cs: sum(m["share"][4] is not None for m in _msgs(cs))),
    ("M-13", "내용 · 첨부 · 반응 전부 없는 행", 22, 20, 42, lambda cs: sum(_empty_msg(m) for m in _msgs(cs))),
    ("M-14", "방당 메시지 수 최소", 1, 1, None, lambda cs: min(len(c["msgs"]) for c in cs)),
    ("M-14", "방당 메시지 수 중앙값", 7, 9, None, lambda cs: _median([len(c["msgs"]) for c in cs])),
    ("M-14", "방당 메시지 수 최대", 117, 372, None, lambda cs: max(len(c["msgs"]) for c in cs)),
    ("M-15", "같은 방 sent_at_ms 겹쳐 남는 행", 1, 3, 4,
     lambda cs: sum(len(c["msgs"]) - len({m["ts"] for m in c["msgs"]}) for c in cs)),
    ("M-16", "sent_at 최소", "2025-12-26T07:47:20.927Z", "2026-01-09T18:19:11.724Z", None,
     lambda cs: min(m["sent_at"] for m in _msgs(cs))),
    ("M-17", "sent_at 최대", "2026-06-26T06:16:02.338Z", "2026-06-26T06:38:41.939Z", None,
     lambda cs: max(m["sent_at"] for m in _msgs(cs))),
    ("M-18", "메시지 전부 우리 발신인 방", 3, 17, 20,
     lambda cs: sum(bool(c["msgs"]) and all(m["is_owner"] for m in c["msgs"]) for c in cs)),
    ("M-18", "메시지 전부 상대 발신인 방", 17, 10, 27,
     lambda cs: sum(bool(c["msgs"]) and not any(m["is_owner"] for m in c["msgs"]) for c in cs)),

    ("A-01", "photos 행", 690, 2528, 3218, lambda cs: _kind(cs, "photos")),
    ("A-02", "videos 행", 2, 1, 3, lambda cs: _kind(cs, "videos")),
    ("A-03", "files 행", 5, 112, 117, lambda cs: _kind(cs, "files")),
    ("A-04", "gifs 행", 1, 3, 4, lambda cs: _kind(cs, "gifs")),
    ("A-05", "audio_files 행", 1, 3, 4, lambda cs: _kind(cs, "audio_files")),
    ("A-06", "sticker 행", 0, 115, 115, lambda cs: _kind(cs, "sticker")),
    ("A-07", "attachment 행 합", 699, 2762, 3461, lambda cs: len(_atts(cs))),
    ("A-08", "photos 있는 메시지", 680, 2232, 2912, lambda cs: _msgs_with_kind(cs, "photos")),
    ("A-09", "videos 있는 메시지", 2, 1, 3, lambda cs: _msgs_with_kind(cs, "videos")),
    ("A-09", "files 있는 메시지", 5, 112, 117, lambda cs: _msgs_with_kind(cs, "files")),
    ("A-09", "gifs 있는 메시지", 1, 3, 4, lambda cs: _msgs_with_kind(cs, "gifs")),
    ("A-09", "audio_files 있는 메시지", 1, 3, 4, lambda cs: _msgs_with_kind(cs, "audio_files")),
    ("A-09", "sticker 있는 메시지", 0, 115, 115, lambda cs: _msgs_with_kind(cs, "sticker")),
    ("A-10", "첨부 하나라도 있는 메시지", 689, 2466, 3155, lambda cs: sum(bool(m["atts"]) for m in _msgs(cs))),
    ("A-11", "created_at_s NULL · photos", 1, 0, 1, lambda cs: _null_cts(cs, "photos")),
    ("A-11", "created_at_s NULL · videos", 1, 0, 1, lambda cs: _null_cts(cs, "videos")),
    ("A-11", "created_at_s NULL · gifs", 1, 3, 4, lambda cs: _null_cts(cs, "gifs")),
    ("A-11", "created_at_s NULL · sticker", 0, 115, 115, lambda cs: _null_cts(cs, "sticker")),
    ("A-11", "created_at_s NULL · files", 0, 0, 0, lambda cs: _null_cts(cs, "files")),
    ("A-11", "created_at_s NULL · audio_files", 0, 0, 0, lambda cs: _null_cts(cs, "audio_files")),
    ("A-12", "created_at_s NULL 합", 3, 118, 121, lambda cs: sum(1 for _c, _m, a in _atts(cs) if a[2] is None)),
    ("A-13", "sticker 아닌 행의 uri 값 종류", 699, 2647, 3346,
     lambda cs: len({a[1] for _c, _m, a in _atts(cs) if a[0] != "sticker"})),
    ("A-13", "  └ sticker 아닌 행 수", 699, 2647, 3346, lambda cs: sum(1 for _c, _m, a in _atts(cs) if a[0] != "sticker")),
    ("A-14", "sticker 행의 uri 값 종류", 0, 18, 18, lambda cs: len({a[1] for _c, _m, a in _atts(cs) if a[0] == "sticker"})),
    ("A-15", "uri 파일이 원본에 있는 행", 699, 2762, 3461, None),  # 함수는 실행 때 붙인다(--source)
    ("A-16", "sticker 아닌 행 · uri 가 자기 방 폴더 아래", 699, 2647, 3346,
     lambda cs: sum(1 for c, _m, a in _atts(cs)
                    if a[0] != "sticker" and a[1].startswith(os.path.dirname(c["source_file"]) + "/"))),
    ("A-17", "sticker 행 · uri 가 FB stickers_used/ 아래", 0, 115, 115,
     lambda cs: sum(1 for _c, _m, a in _atts(cs) if a[0] == "sticker" and a[1].startswith(STICKER_DIR))),
    ("A-18", "한 메시지 photos 최대", 3, 12, None, lambda cs: max(_photo_count(m) for m in _msgs(cs))),
    ("A-19", "photos 1개인 메시지", 671, 2045, 2716, lambda cs: sum(_photo_count(m) == 1 for m in _msgs(cs))),
    ("A-19", "photos 2개인 메시지", 8, 124, 132, lambda cs: sum(_photo_count(m) == 2 for m in _msgs(cs))),
    ("A-19", "photos 3개 이상인 메시지", 1, 63, 64, lambda cs: sum(_photo_count(m) >= 3 for m in _msgs(cs))),
    ("A-20", "inbox 방의 attachment 행", 692, 2725, 3417, lambda cs: sum(1 for c, _m, _a in _atts(cs) if c["box"] == "inbox")),
    ("A-21", "message_requests 방의 attachment 행", 7, 0, 7,
     lambda cs: sum(1 for c, _m, _a in _atts(cs) if c["box"] == "message_requests")),
    ("A-21", "filtered_threads 방의 attachment 행", 0, 37, 37,
     lambda cs: sum(1 for c, _m, _a in _atts(cs) if c["box"] == "filtered_threads")),

    ("R-01", "reaction 행", 123, 236, 359, lambda cs: len(_reacts(cs))),
    ("R-02", "반응 있는 메시지", 123, 236, 359, lambda cs: sum(bool(m["reacts"]) for m in _msgs(cs))),
    ("R-02", "  └ 메시지당 반응 최대", 1, 1, 1, lambda cs: max(len(m["reacts"]) for m in _msgs(cs))),
    ("R-03", "reaction is_owner = 1", 64, 130, 194, lambda cs: sum(r[1] for r in _reacts(cs))),
    ("R-04", "reaction is_owner = 0", 59, 106, 165, lambda cs: sum(not r[1] for r in _reacts(cs))),
    ("R-05", "reaction 값 종류", 8, 12, None, lambda cs: len({r[2] for r in _reacts(cs)})),

    ("E-01", "C1 제어 문자 · U+FFFD 든 TEXT 값", 0, 0, 0, "E-01"),
    ("E-02", "content 비 ASCII 행", 5988, 18849, 24837, lambda cs: sum(_non_ascii(m["content"]) for m in _msgs(cs))),
    ("E-03", "원본 문자열 값 수", 16706, 49652, 66358, "E-03"),
    ("E-04", "복원 실패", 0, 0, 0, "E-04"),
]


def evaluate(fn, convs, extra, scope):
    cs = convs if scope == "합" else [c for c in convs if c["ch"] == scope]
    if isinstance(fn, str):
        if scope == "합":
            vals = [extra[IG][fn], extra[FB][fn]]
            return None if None in vals else sum(vals)
        return extra[scope][fn]
    try:
        return fn(cs)
    except (ValueError, TypeError, KeyError, AttributeError):
        return "오류"


def main(argv=None):
    ap = argparse.ArgumentParser(description="1층 대조 — SPEC-001 §7 기준 · 원본 재집계 · DB")
    ap.add_argument("--source", required=True, help="원본 루트")
    ap.add_argument("--db", required=True, help="SQLite 파일 경로")
    args = ap.parse_args(argv)
    try:
        src, src_extra = normalize_source(args.source)
        db, db_extra = normalize_db(args.db)
    except ReadFail as e:
        print("대조 중단 — 원본 읽기 실패 " + str(e), file=sys.stderr)
        return 1
    except Exception as e:  # 예외 문구에 경로 · 값이 들어갈 수 있어 종류만 찍는다
        print("대조 중단 — 예기치 않은 오류(%s)" % type(e).__name__, file=sys.stderr)
        return 1

    uri_fn = _uri_exists(args.source)
    fmt = "%-5s %-44s %-5s %26s %26s %26s  %s"
    print(fmt % ("#", "무엇", "칸", "기준", "원본 재집계", "DB", "결과"))
    total = bad = 0
    for code, label, b_ig, b_fb, b_all, fn in LINES:
        if fn is None:
            fn = uri_fn
        for scope, base in ((IG, b_ig), (FB, b_fb), ("합", b_all)):
            if base is None:
                continue
            s = evaluate(fn, src, src_extra, scope)
            d = evaluate(fn, db, db_extra, scope)
            if code == "E-04" and d is None:
                ok = s == base  # 복원 실패는 원본에서만 센다 — DB 에는 실패한 값이 들어갈 수 없다
                d_show = "—"
            else:
                ok = s == base and d == base
                d_show = str(d)
            total += 1
            bad += not ok
            short = {IG: "IG", FB: "FB"}.get(scope, scope)
            print(fmt % (code, label, short, base, s, d_show, "일치" if ok else "불일치"))
    print("칸 %d개 · 일치 %d · 불일치 %d" % (total, total - bad, bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
