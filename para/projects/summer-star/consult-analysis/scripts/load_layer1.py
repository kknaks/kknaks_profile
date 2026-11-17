#!/usr/bin/env python3
"""1층 적재 — 상담 DM(인스타그램 · 페이스북 메신저) 원본 → SQLite.

계약: para/projects/summer-star/consult-analysis/20-spec/spec-001-layer1-schema.md (SPEC-001 0.2.0)

- 원본을 펼치기만 한다. 판단 칸(언어 · 국적 · 단계 등)은 없다(2층).
- 표준 라이브러리만. 실행은 `python3 -I`.
- 원본 폴더에는 쓰지 않는다. `<db>.tmp` 에 만들고 다 되면 `<db>` 로 바꿔치기한다(§6.2).
- 출력에는 건수와 규칙 번호만 쓴다(§6.3). 이름 · 본문 · 폴더명 · thread_path · uri 를 찍지 않는다.
"""

import argparse
import datetime
import json
import os
import sqlite3
import sys
from collections import Counter

# §1 — 채널마다 메시지 루트 하나 · 그 아래 보관함
CHANNELS = (
    ("instagram", "your_instagram_activity/messages", ("inbox", "message_requests")),
    ("facebook", "this_profile's_activity_across_facebook/messages", ("inbox", "filtered_threads")),
)
NON_BOX_DIRS = ("stickers_used",)  # §1 — 방이 아닌 폴더
BOXES = ("inbox", "message_requests", "filtered_threads")
ATTACHMENT_KINDS = ("photos", "videos", "files", "gifs", "audio_files", "sticker")  # §4.5 순서
SHARE_KEYS = ("link", "share_text", "original_content_owner", "profile_share_name", "profile_share_username")


class Stop(Exception):
    """§5.4 멈추는 자리. 메시지에는 채널 · 보관함 · 방 순번 · 키 경로 · 규칙 번호만."""

    def __init__(self, rule, where="", key=""):
        self.rule = rule
        self.where = where
        self.key = key
        super().__init__(rule)

    def describe(self):
        parts = [self.rule]
        if self.where:
            parts.append(self.where)
        if self.key:
            parts.append("키 " + self.key)
        return " · ".join(parts)


# ---------------------------------------------------------------- §3 대응표
# 스펙 꼴: "str" | "int" | "bool" | ("empty_list",) | ("list", item) | ("obj", {키: (꼴, 필수)})
# 필수 = SPEC §2 에서 NOT NULL 인 칸으로 가는 키. 필수 키가 없으면 대응표 타입과 다름(G-2).

def _obj(fields):
    return ("obj", fields)


_URI_TS = _obj({"uri": ("str", True), "creation_timestamp": ("int", False)})
_URI_ONLY = _obj({"uri": ("str", True)})

MESSAGE_SPEC = _obj({
    "sender_name": ("str", True),
    "timestamp_ms": ("int", True),
    "is_geoblocked_for_viewer": ("bool", True),
    "is_unsent_image_by_messenger_kid_parent": ("bool", True),
    "content": ("str", False),
    "photos": (("list", _URI_TS), False),
    "reactions": (("list", _obj({"actor": ("str", True), "reaction": ("str", True)})), False),
    "share": (_obj({k: ("str", False) for k in SHARE_KEYS}), False),
    "files": (("list", _URI_TS), False),
    "call_duration": ("int", False),
    "videos": (("list", _URI_TS), False),
    "gifs": (("list", _URI_ONLY), False),
    "audio_files": (("list", _URI_TS), False),
    "sticker": (_obj({"uri": ("str", True), "ai_stickers": (("empty_list",), False)}), False),
})

ROOM_SPEC = _obj({
    "participants": (("list", _obj({"name": ("str", True)})), True),
    "messages": (("list", MESSAGE_SPEC), True),
    "title": ("str", True),
    "is_still_participant": ("bool", True),
    "thread_path": ("str", True),
    "magic_words": (("empty_list",), False),
    "is_pending": ("bool", False),
    "joinable_mode": (_obj({"mode": ("int", False), "link": ("str", False)}), False),
})


def restore(s, where, key):
    """§5.1 이중 인코딩 복원. 실패하면 G-3."""
    try:
        return s.encode("latin1").decode("utf8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        raise Stop("G-3", where, key) from None


def walk(value, spec, path, where):
    """대응표대로 값을 확인하고 문자열을 복원한 새 값을 돌려준다."""
    if spec == "str":
        if not isinstance(value, str):
            raise Stop("G-2", where, path)
        return restore(value, where, path)
    if spec == "int":
        if isinstance(value, bool) or not isinstance(value, int):
            raise Stop("G-2", where, path)
        return value
    if spec == "bool":
        if not isinstance(value, bool):
            raise Stop("G-2", where, path)
        return value
    tag = spec[0]
    if tag == "empty_list":
        if not isinstance(value, list):
            raise Stop("G-2", where, path)
        if value:
            raise Stop("G-9", where, path)
        return []
    if tag == "list":
        if not isinstance(value, list):
            raise Stop("G-2", where, path)
        return [walk(v, spec[1], path + "[]", where) for v in value]
    if tag == "obj":
        if not isinstance(value, dict):
            raise Stop("G-2", where, path)
        fields = spec[1]
        for k in value:
            if k not in fields:
                raise Stop("G-1", where, (path + "." if path else "") + k)
        out = {}
        for k, (sub, required) in fields.items():
            sub_path = (path + "." if path else "") + k
            if k not in value:
                if required:
                    raise Stop("G-2", where, sub_path)
                continue
            out[k] = walk(value[k], sub, sub_path, where)
        return out
    raise AssertionError("unknown spec")


# ---------------------------------------------------------------- §1 · §4.1 방 찾기

def _visible(name):
    return not name.startswith(".")


def find_rooms(source):
    """(channel, box, 보관함 안 순번, source_file, 폴더명 또는 None) 목록."""
    rooms = []
    for channel, root_rel, boxes in CHANNELS:
        root = os.path.join(source, root_rel)
        if not os.path.isdir(root):
            raise Stop("G-12", channel)
        for name in sorted(os.listdir(root)):
            full = os.path.join(root, name)
            if not _visible(name) or not os.path.isdir(full):
                continue  # 메시지 루트 바로 아래 파일은 방이 아니다(§1)
            if name in NON_BOX_DIRS:
                continue
            if name not in boxes:
                raise Stop("G-12", channel)
        for box in boxes:
            box_dir = os.path.join(root, box)
            if not os.path.isdir(box_dir):
                continue
            n = 0
            for name in sorted(os.listdir(box_dir)):
                if not _visible(name):
                    continue
                full = os.path.join(box_dir, name)
                if os.path.isdir(full):
                    n += 1
                    where = "%s · %s · %d번째 방" % (channel, box, n)
                    msgs = [f for f in os.listdir(full)
                            if f.startswith("message_") and f.endswith(".json")]
                    if msgs != ["message_1.json"]:
                        raise Stop("G-5", where)
                    rel = "/".join((root_rel, box, name, "message_1.json"))
                    rooms.append((channel, box, n, rel, name))
                elif os.path.isfile(full) and name.endswith(".json"):
                    n += 1  # 보관함 바로 아래 JSON(D-13)
                    rel = "/".join((root_rel, box, name))
                    rooms.append((channel, box, n, rel, None))
                else:
                    # 폴더도 *.json 도 아닌 보통 파일(숨김 아님) — 파일명은 찍지 않는다(§4.1 · G-12)
                    raise Stop("G-12", "%s · %s" % (channel, box))
    return rooms


# ---------------------------------------------------------------- 읽기 · 확인

def read_room(source, channel, box, n, rel, folder):
    where = "%s · %s · %d번째 방" % (channel, box, n)
    try:
        with open(os.path.join(source, rel), "r", encoding="ascii") as fh:
            raw = json.load(fh)
    except (OSError, ValueError):  # 열기 오류 · 비 ASCII 바이트(UnicodeDecodeError) · JSON 깨짐 — §5.1 · G-13
        raise Stop("G-13", where) from None
    room = walk(raw, ROOM_SPEC, "", where)

    # G-10 빈 share
    for m in room["messages"]:
        if "share" in m and not m["share"]:
            raise Stop("G-10", where, "messages[].share")

    # G-4 thread_path 대조
    tp = room["thread_path"]
    if folder is not None:
        if tp != box + "/" + folder:
            raise Stop("G-4", where, "thread_path")
    else:
        if tp.split("/")[0] != box:
            raise Stop("G-4", where, "thread_path")

    # G-11 참가자 이름 겹침
    names = [p["name"] for p in room["participants"]]
    if len(set(names)) != len(names):
        raise Stop("G-11", where, "participants[].name")

    # G-7 발신자 · 반응자가 참가자가 아님
    name_set = set(names)
    for m in room["messages"]:
        if m["sender_name"] not in name_set:
            raise Stop("G-7", where, "messages[].sender_name")
        for r in m.get("reactions", []):
            if r["actor"] not in name_set:
                raise Stop("G-7", where, "messages[].reactions[].actor")

    # G-8 내림차순
    ts = [m["timestamp_ms"] for m in room["messages"]]
    for a, b in zip(ts, ts[1:]):
        if b > a:
            raise Stop("G-8", where, "messages[].timestamp_ms")

    return {"channel": channel, "box": box, "where": where, "source_file": rel, "room": room}


def find_owners(rooms):
    """§4.3 채널별 우리 계정. 정해지지 않으면 G-6."""
    owners = {}
    for channel, _root, _boxes in CHANNELS:
        ch_rooms = [r["room"] for r in rooms if r["channel"] == channel]
        if not ch_rooms:
            raise Stop("G-6", channel)
        common = None
        senders = Counter()
        for room in ch_rooms:
            s = {p["name"] for p in room["participants"]}
            common = s if common is None else common & s
            senders.update(m["sender_name"] for m in room["messages"])
        if len(common) != 1:
            raise Stop("G-6", channel)
        owner = next(iter(common))
        top = senders.most_common(2)
        if not top or top[0][0] != owner or (len(top) > 1 and top[1][1] == top[0][1]):
            raise Stop("G-6", channel)
        owners[channel] = owner
    return owners


# ---------------------------------------------------------------- §5.2 시각

_EPOCH = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


def iso_ms(ms):
    t = _EPOCH + datetime.timedelta(milliseconds=ms)
    return t.strftime("%Y-%m-%dT%H:%M:%S") + ".%03dZ" % (ms % 1000)


def iso_s(s):
    t = _EPOCH + datetime.timedelta(seconds=s)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- §2 스키마

DDL = """
CREATE TABLE conversation (
    conversation_id       INTEGER PRIMARY KEY,
    channel               TEXT    NOT NULL CHECK (channel IN ('instagram', 'facebook')),
    box                   TEXT    NOT NULL CHECK (box IN ('inbox', 'message_requests', 'filtered_threads')),
    thread_path           TEXT    NOT NULL,
    source_file           TEXT    NOT NULL UNIQUE,
    title                 TEXT    NOT NULL,
    owner_name            TEXT    NOT NULL,
    owner_participant_seq INTEGER NOT NULL,
    is_still_participant  INTEGER NOT NULL,
    is_pending            INTEGER,
    joinable_mode         INTEGER,
    joinable_link         TEXT,
    UNIQUE (channel, thread_path)
);
CREATE TABLE customer (
    customer_id     INTEGER PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversation (conversation_id),
    participant_seq INTEGER NOT NULL,
    name            TEXT    NOT NULL,
    UNIQUE (conversation_id, participant_seq)
);
CREATE TABLE message (
    message_id                              INTEGER PRIMARY KEY,
    conversation_id                         INTEGER NOT NULL REFERENCES conversation (conversation_id),
    source_idx                              INTEGER NOT NULL,
    seq                                     INTEGER NOT NULL,
    sender_name                             TEXT    NOT NULL,
    is_owner                                INTEGER NOT NULL,
    customer_id                             INTEGER REFERENCES customer (customer_id),
    sent_at_ms                              INTEGER NOT NULL,
    sent_at                                 TEXT    NOT NULL,
    content                                 TEXT,
    call_duration                           INTEGER,
    is_geoblocked_for_viewer                INTEGER NOT NULL,
    is_unsent_image_by_messenger_kid_parent INTEGER NOT NULL,
    share_link                              TEXT,
    share_text                              TEXT,
    share_original_content_owner            TEXT,
    share_profile_share_name                TEXT,
    share_profile_share_username            TEXT,
    UNIQUE (conversation_id, source_idx),
    UNIQUE (conversation_id, seq)
);
CREATE TABLE attachment (
    attachment_id INTEGER PRIMARY KEY,
    message_id    INTEGER NOT NULL REFERENCES message (message_id),
    kind          TEXT    NOT NULL CHECK (kind IN ('photos', 'videos', 'files', 'gifs', 'audio_files', 'sticker')),
    item_idx      INTEGER NOT NULL,
    uri           TEXT    NOT NULL,
    created_at_s  INTEGER,
    created_at    TEXT,
    UNIQUE (message_id, kind, item_idx)
);
CREATE TABLE reaction (
    reaction_id INTEGER PRIMARY KEY,
    message_id  INTEGER NOT NULL REFERENCES message (message_id),
    item_idx    INTEGER NOT NULL,
    actor       TEXT    NOT NULL,
    is_owner    INTEGER NOT NULL,
    reaction    TEXT    NOT NULL,
    UNIQUE (message_id, item_idx)
);
"""

TABLES = ("conversation", "customer", "message", "attachment", "reaction")


# ---------------------------------------------------------------- 행 만들기 · §4.5 대체 키

def build_rows(rooms, owners):
    # (channel, thread_path) 바이트 오름차순 — 중복이면 G-4
    keyed = sorted(rooms, key=lambda r: (r["channel"].encode("utf8"), r["room"]["thread_path"].encode("utf8")))
    seen = set()
    for r in keyed:
        k = (r["channel"], r["room"]["thread_path"])
        if k in seen:
            raise Stop("G-4", r["where"], "thread_path")
        seen.add(k)

    conv_rows, cust_rows, msg_rows, att_rows, react_rows = [], [], [], [], []
    customer_id = message_id = attachment_id = reaction_id = 0
    for conversation_id, r in enumerate(keyed, start=1):
        room = r["room"]
        owner = owners[r["channel"]]
        names = [p["name"] for p in room["participants"]]
        jm = room.get("joinable_mode")
        conv_rows.append((
            conversation_id, r["channel"], r["box"], room["thread_path"], r["source_file"],
            room["title"], owner, names.index(owner), int(room["is_still_participant"]),
            int(room["is_pending"]) if "is_pending" in room else None,
            jm.get("mode") if jm is not None else None,
            jm.get("link") if jm is not None else None,
        ))
        cust_by_name = {}
        for seq, name in enumerate(names):
            if name == owner:
                continue
            customer_id += 1
            cust_rows.append((customer_id, conversation_id, seq, name))
            cust_by_name[name] = customer_id

        msgs = room["messages"]
        n = len(msgs)
        # message_id 는 (conversation_id, seq) 순 — seq = n - source_idx 이므로 배열을 뒤에서부터
        for source_idx in range(n - 1, -1, -1):
            m = msgs[source_idx]
            message_id += 1
            is_owner = m["sender_name"] == owner
            cid = None
            if not is_owner:
                cid = cust_by_name.get(m["sender_name"])
                if cid is None:
                    raise Stop("G-7", r["where"], "messages[].sender_name")
            share = m.get("share", {})
            msg_rows.append((
                message_id, conversation_id, source_idx, n - source_idx, m["sender_name"],
                int(is_owner), cid, m["timestamp_ms"], iso_ms(m["timestamp_ms"]),
                m.get("content"), m.get("call_duration"),
                int(m["is_geoblocked_for_viewer"]), int(m["is_unsent_image_by_messenger_kid_parent"]),
            ) + tuple(share.get(k) for k in SHARE_KEYS))
            for kind in ATTACHMENT_KINDS:
                if kind not in m:
                    continue
                items = [m[kind]] if kind == "sticker" else m[kind]
                for item_idx, it in enumerate(items):
                    attachment_id += 1
                    cts = it.get("creation_timestamp")
                    att_rows.append((
                        attachment_id, message_id, kind, item_idx, it["uri"],
                        cts, iso_s(cts) if cts is not None else None,
                    ))
            for item_idx, rc in enumerate(m.get("reactions", [])):
                reaction_id += 1
                react_rows.append((
                    reaction_id, message_id, item_idx, rc["actor"],
                    int(rc["actor"] == owner), rc["reaction"],
                ))
    return conv_rows, cust_rows, msg_rows, att_rows, react_rows


def write_db(db, rows):
    tmp = db + ".tmp"
    parent = os.path.dirname(os.path.abspath(db))
    os.makedirs(parent, exist_ok=True)
    for p in (tmp, tmp + "-journal"):
        if os.path.exists(p):
            os.remove(p)
    con = sqlite3.connect(tmp, isolation_level=None)
    try:
        con.execute("PRAGMA foreign_keys = ON")
        con.executescript(DDL)
        con.execute("BEGIN")
        for table, data in zip(TABLES, rows):
            if data:
                marks = ",".join("?" * len(data[0]))
                con.executemany("INSERT INTO %s VALUES (%s)" % (table, marks), data)
        con.execute("COMMIT")
        bad = con.execute("PRAGMA foreign_key_check").fetchall()
        if bad:
            raise RuntimeError("foreign key check")
    except BaseException:
        con.close()
        for p in (tmp, tmp + "-journal"):
            if os.path.exists(p):
                os.remove(p)
        raise
    con.close()
    os.replace(tmp, db)


def load(source, db):
    """적재 본체. 멈추면 Stop 을 던지고 `<db>` 는 건드리지 않는다."""
    found = find_rooms(source)
    rooms = [read_room(source, *f) for f in found]
    owners = find_owners(rooms)
    rows = build_rows(rooms, owners)
    write_db(db, rows)


COUNT_SQL = {
    "conversation": "SELECT c.channel, COUNT(*) FROM conversation c GROUP BY c.channel",
    "customer": "SELECT c.channel, COUNT(*) FROM customer x JOIN conversation c USING (conversation_id) GROUP BY c.channel",
    "message": "SELECT c.channel, COUNT(*) FROM message x JOIN conversation c USING (conversation_id) GROUP BY c.channel",
    "attachment": "SELECT c.channel, COUNT(*) FROM attachment a JOIN message m USING (message_id) "
                  "JOIN conversation c USING (conversation_id) GROUP BY c.channel",
    "reaction": "SELECT c.channel, COUNT(*) FROM reaction r JOIN message m USING (message_id) "
                "JOIN conversation c USING (conversation_id) GROUP BY c.channel",
}


def report(db):
    con = sqlite3.connect("file:%s?mode=ro" % os.path.abspath(db), uri=True)
    try:
        print("1층 적재 완료 — 테이블별 행 수")
        print("%-14s %10s %10s %10s" % ("table", "instagram", "facebook", "합"))
        for t in TABLES:
            by = dict(con.execute(COUNT_SQL[t]).fetchall())
            ig, fb = by.get("instagram", 0), by.get("facebook", 0)
            print("%-14s %10d %10d %10d" % (t, ig, fb, ig + fb))
    finally:
        con.close()


def main(argv=None):
    ap = argparse.ArgumentParser(description="1층 적재 — 상담 DM 원본 → SQLite (SPEC-001)")
    ap.add_argument("--source", required=True, help="원본 루트(두 채널 폴더가 바로 아래)")
    ap.add_argument("--db", required=True, help="SQLite 파일 경로")
    args = ap.parse_args(argv)
    try:
        load(args.source, args.db)
    except Stop as e:
        print("적재 중단 — " + e.describe(), file=sys.stderr)
        return 1
    except Exception as e:  # 예외 문구에는 경로 · 값이 들어갈 수 있어 종류만 찍는다
        print("적재 중단 — 예기치 않은 오류(%s)" % type(e).__name__, file=sys.stderr)
        return 2
    report(args.db)
    return 0


if __name__ == "__main__":
    sys.exit(main())
