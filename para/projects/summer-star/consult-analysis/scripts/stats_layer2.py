#!/usr/bin/env python3
"""2층 집계 — SPEC-002 §6 통계 · §7 집계 JSON.

- DB 는 읽기만 한다. 결과 JSON 에는 분류 값과 수만 — 본문 · 이름 · id · raw_value · procedures_other 0.
- 분모는 방. 모든 비율은 {"n", "d", "pct", "small"} — d < 10 이면 small = true(D-11).
- 중앙값 · 사분위는 방 수 n 을 같이 낸다.
- 표준 라이브러리만.
"""

import argparse
import datetime
import json
import os
import sqlite3
import statistics
import sys
from collections import Counter, defaultdict

SMALL = 10
LANGS = ("zh-Hant", "zh-Hans", "zh", "en", "ko", "ja", "other", "none")
CHANNELS = ("instagram", "facebook")
STAGES = ("inquiry", "form_sent", "form_filled")
FIRST_FORMS = ("photo", "share", "sticker_or_none", "short", "question", "statement")
QUESTION_MARKS = ("?", "？", "嗎", "呢", "請問")
WEEKDAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
KST_MS = 9 * 3600 * 1000
TOPICS = ("procedure", "price", "schedule", "location", "interpreter", "result", "safety", "promo", "other")
PROCEDURES = ("ulthera", "thermage", "sofwave", "onda", "titanium", "rf_microneedle", "juvelook", "botox",
              "filler", "skinbooster", "laser", "rejuran", "mole_wart_removal", "acne_scar", "pore_texture",
              "eye_area", "fat_dissolving", "tune", "lifting_unspecified", "other")


# ---------------------------------------------------------------- 수 꼴

def rate(n, d):
    return {"n": n, "d": d, "pct": round(100.0 * n / d, 1) if d else None, "small": d < SMALL}


def dist(values):
    v = sorted(x for x in values if x is not None)
    out = {"n": len(v), "median": None, "q1": None, "q3": None, "small": len(v) < SMALL}
    if not v:
        return out
    out["median"] = round(statistics.median(v), 1)
    if len(v) >= 2:
        q = statistics.quantiles(v, n=4, method="inclusive")
        out["q1"], out["q3"] = round(q[0], 1), round(q[2], 1)
    else:
        out["q1"] = out["q3"] = round(v[0], 1)
    return out


# ---------------------------------------------------------------- 방 특징

def first_form(msg):
    if msg["photo"]:
        return "photo"
    if msg["share"]:
        return "share"
    if msg["n_letters"] == 0:
        return "sticker_or_none"
    if msg["n_letters"] <= 10:
        return "short"
    if msg["content"] and any(q in msg["content"] for q in QUESTION_MARKS):
        return "question"
    return "statement"


def count_turns(msgs):
    """발신자가 바뀔 때까지 이어진 묶음 수(자동응답 메시지는 뺀다)."""
    turns, prev = 0, None
    for m in msgs:
        if m["auto"] is not None:
            continue
        if m["own"] != prev:
            turns += 1
            prev = m["own"]
    return turns


def top_msg_lang(cust):
    """메시지 언어별 글자 수가 가장 많은 언어(번간 미상 흡수 없이 어림 — 민감도 점검용)."""
    c = Counter()
    for m in cust:
        if m.get("lang") and m["n_letters"]:
            c[m["lang"]] += m["n_letters"]
    return c.most_common(1)[0][0] if c else "none"


def room_features(conv, msgs, booking, lang, nat, label):
    """방 하나 → 특징 dict. msgs 는 seq 순."""
    cust = [m for m in msgs if not m["own"]]
    f = {
        "channel": conv["channel"], "lang": lang, "stage": booking["stage"],
        "success": booking["stage"] == "form_filled", "has_customer": bool(cust),
        "got_auto": booking["got_auto_reply"] == 1, "handoff": booking["handoff_mentioned"] == 1,
        "nationality": nat["nationality"] or "unknown", "nat_source": nat["source"],
        "labeled": label is not None,
        "topics": label["topics"] if label else [], "procedures": label["procedures"] if label else [],
        "staff_confirmed": bool(label and label["staff_confirmed"]),
    }
    if not cust:
        return f
    first_c = cust[0]
    f["n_customer_msgs"] = len(cust)
    f["n_owner_msgs"] = sum(1 for m in msgs if m["own"] and m["auto"] is None)
    f["n_turns"] = count_turns(msgs)
    # 민감도(한계 절용 · 판정은 안 바꿈): 예약표 칸이 든 고객 메시지(form_labels ≥ 1)를 뺐을 때
    keep = [m for m in msgs if m["own"] or m.get("form_labels", 0) < 1]
    f["n_customer_msgs_wo_form"] = sum(1 for m in keep if not m["own"])
    f["n_turns_wo_form"] = count_turns(keep)
    f["top_msg_lang"] = top_msg_lang(cust)
    f["top_msg_lang_wo_form"] = top_msg_lang([m for m in cust if m.get("form_labels", 0) < 1])
    lens = [m["n_letters"] for m in cust if m["form_filled"] < 2]
    f["customer_len_median"] = statistics.median(lens) if lens else None
    f["first_form"] = first_form(first_c)
    reply = next((m for m in msgs if m["own"] and m["auto"] is None and m["seq"] > first_c["seq"]), None)
    f["first_response_min"] = (reply["ms"] - first_c["ms"]) / 60000.0 if reply else None
    t = datetime.datetime.fromtimestamp((first_c["ms"] + KST_MS) / 1000, tz=datetime.timezone.utc)
    f["kst_hour"] = t.hour
    f["kst_weekday"] = WEEKDAYS[t.weekday()]
    f["business_hours"] = t.weekday() < 5 and 10 <= t.hour < 19
    # 0.2.2 — 예약표 칸이 든 고객 메시지(form_labels ≥ 1)는 이모지에서 뺀다(양식 기호 ★ · 📝)
    plain = [m for m in cust if m.get("form_labels", 0) < 1]
    f["emoji_room"] = any(m["n_emoji"] > 0 for m in plain)
    f["emoji_sum"] = sum(m["n_emoji"] for m in plain)
    f["emoji_msgs"] = len(plain)
    f["photo_room"] = any(m["photo"] for m in cust)
    # 0.2.2 — 사진을 예약표 회신(filled_message_id) 앞 · 뒤로도. 회신 메시지 자체는 어느 쪽에도 넣지 않는다
    cut = booking.get("filled_seq") if booking.get("filled_message_id") is not None else None
    f["photo_before"] = any(m["photo"] for m in cust if cut is None or m["seq"] < cut)
    f["photo_after"] = cut is not None and any(m["photo"] for m in cust if m["seq"] > cut)
    if f["success"] and booking["filled_message_id"] is not None:
        upto = [m for m in msgs if m["seq"] <= booking["filled_seq"]]
        f["turns_to_booking"] = count_turns(upto)
        f["hours_to_booking"] = (booking["filled_ms"] - first_c["ms"]) / 3600000.0
    return f


def load(db):
    con = sqlite3.connect("file:%s?mode=ro" % os.path.abspath(db), uri=True)
    con.row_factory = sqlite3.Row
    convs = {r["conversation_id"]: dict(r) for r in con.execute("SELECT conversation_id, channel FROM conversation")}
    photo = {r[0] for r in con.execute("SELECT DISTINCT message_id FROM attachment WHERE kind = 'photos'")}
    msgs = defaultdict(list)
    for r in con.execute(
            "SELECT m.message_id, m.conversation_id, m.seq, m.is_owner, m.sent_at_ms, m.content, "
            "m.share_link, m.share_text, m.share_original_content_owner, m.share_profile_share_name, "
            "m.share_profile_share_username, l.n_letters, l.n_emoji, l.auto_kind, l.form_filled, l.form_labels, l.lang "
            "FROM message m JOIN l2_message l USING (message_id) ORDER BY m.conversation_id, m.seq"):
        msgs[r["conversation_id"]].append({
            "id": r["message_id"], "seq": r["seq"], "own": r["is_owner"] == 1, "ms": r["sent_at_ms"],
            "content": r["content"], "n_letters": r["n_letters"], "n_emoji": r["n_emoji"],
            "auto": r["auto_kind"], "form_filled": r["form_filled"], "form_labels": r["form_labels"],
            "lang": r["lang"],
            "photo": r["message_id"] in photo,
            "share": any(r[k] is not None for k in ("share_link", "share_text", "share_original_content_owner",
                                                     "share_profile_share_name", "share_profile_share_username")),
        })
    booking = {}
    for r in con.execute("SELECT b.*, m.seq AS filled_seq, m.sent_at_ms AS filled_ms FROM l2_booking_stage b "
                         "LEFT JOIN message m ON m.message_id = b.filled_message_id"):
        booking[r["conversation_id"]] = dict(r)
    lang = {r[0]: r[1] for r in con.execute("SELECT conversation_id, lang FROM l2_conversation_lang")}
    nat = {r["conversation_id"]: dict(r) for r in con.execute("SELECT conversation_id, nationality, source "
                                                                "FROM l2_nationality")}
    labels = {}
    have = con.execute("SELECT 1 FROM sqlite_master WHERE name = 'l2_llm_label'").fetchone()
    versions = {"rule": sorted({r[0] for r in con.execute("SELECT DISTINCT version FROM l2_booking_stage")})}
    if have:
        for r in con.execute("SELECT conversation_id, topics, procedures, staff_confirmed FROM l2_llm_label"):
            labels[r[0]] = {"topics": json.loads(r[1]), "procedures": json.loads(r[2]), "staff_confirmed": r[3]}
        versions["llm"] = sorted({r[0] for r in con.execute("SELECT DISTINCT version FROM l2_llm_label")})
        versions["llm_model"] = sorted({r[0] for r in con.execute("SELECT DISTINCT model FROM l2_llm_label")})
    review = {"queue_rows": 0, "by_reason": {}, "human_decided": 0, "human_changed_stage": 0}
    if con.execute("SELECT 1 FROM sqlite_master WHERE name = 'l2_review_queue'").fetchone():
        review["queue_rows"] = con.execute("SELECT COUNT(*) FROM l2_review_queue").fetchone()[0]
        review["by_reason"] = dict(con.execute("SELECT reason, COUNT(*) FROM l2_review_queue GROUP BY 1 ORDER BY 1"))
        review["human_decided"] = con.execute(
            "SELECT COUNT(*) FROM l2_review_queue WHERE human_stage IS NOT NULL").fetchone()[0]
        review["human_changed_stage"] = con.execute(
            "SELECT COUNT(*) FROM l2_booking_stage WHERE judge = 'human' AND stage != rule_stage").fetchone()[0]
    con.close()
    rooms = [room_features(convs[cid], msgs[cid], booking[cid], lang[cid], nat[cid], labels.get(cid))
             for cid in sorted(convs)]
    return rooms, versions, review


# ---------------------------------------------------------------- 묶음 통계

def metrics(rooms):
    cust = [r for r in rooms if r["has_customer"]]
    d = len(cust)
    sent_up = [r for r in cust if r["stage"] in ("form_sent", "form_filled")]
    succ = [r for r in cust if r["success"]]
    labeled = [r for r in cust if r["labeled"]]
    out = {
        "rooms": {"all": len(rooms), "with_customer": d, "without_customer": len(rooms) - d,
                  "stage": {s: sum(r["stage"] == s for r in cust) for s in STAGES}},
        "conversion": {
            "form_filled": rate(len(succ), d),
            "form_sent_or_more": rate(len(sent_up), d),
            "form_sent_to_filled": rate(len(succ), len(sent_up)),
        },
        "turns_to_booking": dist(r.get("turns_to_booking") for r in succ),
        "hours_to_booking": dist(r.get("hours_to_booking") for r in succ),
        "form_msg_sensitivity": {
            "note": "한계 절용 — 예약표 칸이 든 고객 메시지(form_labels >= 1)를 빼면(판정 · 위 값은 그대로)",
            "rooms_with_form_customer_msgs": sum(r["n_customer_msgs_wo_form"] < r["n_customer_msgs"] for r in cust),
            "form_customer_msgs": sum(r["n_customer_msgs"] - r["n_customer_msgs_wo_form"] for r in cust),
            "customer_msgs": dist(r["n_customer_msgs_wo_form"] for r in cust),
            "turns": dist(r["n_turns_wo_form"] for r in cust),
            "top_msg_lang_changes": sum(r["top_msg_lang"] != r["top_msg_lang_wo_form"] for r in cust),
        },
        "room_size": {
            "customer_msgs": dist(r["n_customer_msgs"] for r in cust),
            "owner_msgs_no_auto": dist(r["n_owner_msgs"] for r in cust),
            "turns": dist(r["n_turns"] for r in cust),
        },
        "customer_msg_length": dist(r["customer_len_median"] for r in cust),
        "first_message_form": {k: rate(sum(r["first_form"] == k for r in cust), d) for k in FIRST_FORMS},
        "first_response": {
            "minutes": dist(r["first_response_min"] for r in cust),
            "within_1h": rate(sum(r["first_response_min"] is not None and r["first_response_min"] <= 60
                                  for r in cust), d),
            "no_response": rate(sum(r["first_response_min"] is None for r in cust), d),
        },
        "inquiry_time": {
            "business_hours": rate(sum(r["business_hours"] for r in cust), d),
            "hour_kst": {str(h): sum(r["kst_hour"] == h for r in cust) for h in range(24)},
            "weekday_kst": {w: sum(r["kst_weekday"] == w for r in cust) for w in WEEKDAYS},
        },
        "emoji": {
            "note": "예약표 칸이 든 고객 메시지(form_labels >= 1)는 뺀다 — SPEC-002 0.2.2",
            "rooms_using": rate(sum(r["emoji_room"] for r in cust), d),
            "per_customer_msg": {"n_emoji": sum(r["emoji_sum"] for r in cust),
                                 "n_msgs": sum(r["emoji_msgs"] for r in cust),
                                 "mean": round(sum(r["emoji_sum"] for r in cust) /
                                               max(1, sum(r["emoji_msgs"] for r in cust)), 3)},
        },
        "photo_use": rate(sum(r["photo_room"] for r in cust), d),
        "photo_use_split": {
            "note": "예약표 회신 메시지 앞 / 뒤(회신 메시지 자체는 뺌 · 회신이 없는 방은 전부 앞) — SPEC-002 0.2.2",
            "before_filled": rate(sum(r["photo_before"] for r in cust), d),
            "after_filled": rate(sum(r["photo_after"] for r in cust), d),
        },
        "auto_reply": {
            "got": rate(sum(r["got_auto"] for r in cust), d),
            "conversion_if_got": rate(sum(r["success"] for r in cust if r["got_auto"]),
                                      sum(r["got_auto"] for r in cust)),
            "conversion_if_not": rate(sum(r["success"] for r in cust if not r["got_auto"]),
                                      sum(not r["got_auto"] for r in cust)),
        },
        "handoff_mentioned": rate(sum(r["handoff"] for r in cust), d),
        "topics": value_stats(labeled, "topics", TOPICS),
        "procedures": value_stats(labeled, "procedures", PROCEDURES),
        "staff_confirmed": {"rooms": rate(sum(r["staff_confirmed"] for r in labeled), len(labeled)),
                            "among_form_filled": rate(sum(r["staff_confirmed"] for r in labeled if r["success"]),
                                                      sum(r["success"] for r in labeled))},
        "nationality": nationality(cust),
        "nationality_source_rooms": dict(sorted(Counter(r["nat_source"] for r in cust).items())),
    }
    return out


def value_stats(labeled, key, values):
    d = len(labeled)
    out = {"labeled_rooms": d, "note": "한 방이 여러 값 — 합이 100% 를 넘는다", "values": {}}
    for v in values:
        has = [r for r in labeled if v in r[key]]
        out["values"][v] = {"rooms": rate(len(has), d),
                            "conversion": rate(sum(r["success"] for r in has), len(has))}
    return out


def nationality(rooms):
    c = Counter((r["nat_source"], r["nationality"]) for r in rooms)
    out = defaultdict(dict)
    for (src, nat), n in sorted(c.items()):
        out[src][nat] = n
    return dict(out)


def build(db):
    rooms, versions, review = load(db)
    stage = {}
    for ch in CHANNELS + ("all",):
        rs = [r for r in rooms if ch == "all" or r["channel"] == ch]
        cust = [r for r in rs if r["has_customer"]]
        stage[ch] = {"rooms": len(rs), "with_customer": len(cust),
                     "stage_all_rooms": {s: sum(r["stage"] == s for r in rs) for s in STAGES},
                     "stage_customer_rooms": {s: sum(r["stage"] == s for r in cust) for s in STAGES},
                     "form_sent_or_more": rate(sum(r["stage"] != "inquiry" for r in cust), len(cust)),
                     "form_filled": rate(sum(r["success"] for r in cust), len(cust)),
                     "form_sent_to_filled": rate(sum(r["success"] for r in cust),
                                                 sum(r["stage"] != "inquiry" for r in cust)),
                     "handoff_mentioned_all_rooms": sum(r["handoff"] for r in rs)}
    outcome = {"success": [r for r in rooms if r["success"]],
               "failure": [r for r in rooms if not r["success"]],
               "form_sent": [r for r in rooms if r["stage"] == "form_sent"]}
    out = {
        "meta": {
            "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "spec": "SPEC-002 0.3.0", "versions": versions, "rooms": len(rooms),
            "rooms_with_customer": sum(r["has_customer"] for r in rooms),
            "labeled_rooms": sum(r["labeled"] for r in rooms),
            "review_queue": review,
            "small_threshold": SMALL,
            "definitions": {"business_hours_kst": {"weekdays": "mon-fri", "from_hour": 10, "to_hour": 19},
                            "first_response_within_minutes": 60, "form_filled_min_fields": 2,
                            "short_message_max_letters": 10},
            "notes": ["분모는 방(고객 메시지가 있는 방)", "비율은 n/d · d < 10 이면 small",
                      "언어권(lang) 은 국적이 아니다", "차이로만 읽는다 — 인과 아님"],
        },
        "stage": stage,
        "by_channel": {ch: metrics([r for r in rooms if ch == "all" or r["channel"] == ch])
                       for ch in CHANNELS + ("all",)},
        "by_lang": {lg: metrics([r for r in rooms if r["lang"] == lg]) for lg in LANGS},
        "by_outcome": {k: metrics(v) for k, v in outcome.items()},
        "lang_x_outcome": {"%s|%s" % (lg, k): metrics([r for r in v if r["lang"] == lg])
                           for lg in LANGS for k, v in outcome.items() if k != "form_sent"},
    }
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="2층 집계 JSON (SPEC-002 §6 · §7)")
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    out = build(args.db)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=False)
        fh.write("\n")
    m = out["meta"]
    print("집계 완료 — 방 %d · 고객 메시지 있는 방 %d · 라벨 방 %d · 묶음: channel %d · lang %d · outcome %d · "
          "lang_x_outcome %d" % (m["rooms"], m["rooms_with_customer"], m["labeled_rooms"], len(out["by_channel"]),
                                  len(out["by_lang"]), len(out["by_outcome"]), len(out["lang_x_outcome"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
