#!/usr/bin/env python3
"""2층 규칙 판정 — 언어 · 자동응답 · 예약표 칸 · 예약 단계 · 국적(① ② ③) · 사람 확인 큐.

계약: para/projects/summer-star/consult-analysis/20-spec/spec-002-layer2-analysis.md (SPEC-002 0.1.0)
      DEC-002 D-14 ~ D-18 (OQ-201 ~ 205 권장 A)

- 1층 테이블은 읽기만 한다. `l2_` 규칙 테이블 다섯을 지우고 다시 만든다(한 트랜잭션). `l2_llm_label` 은 건드리지 않는다.
- 표준 출력에는 건수만. 본문 · 이름 · thread_path 를 찍지 않는다.
- 외부 패키지: opencc-python-reimplemented (requirements-layer2.txt).
"""

import argparse
import csv
import datetime
import json
import os
import re
import sqlite3
import sys
import unicodedata
from collections import Counter, defaultdict

VERSION = "rule-0.1.0"
QUEUE_LIMIT = 50

# ---------------------------------------------------------------- §2.1 자동응답(우리 계정 상용 문구 머리 — SPEC 에 실린 그대로)
AUTO_CONTAINS = (("off_hours_form", "非營業時間"),)
AUTO_PREFIX = (
    ("away", ("感謝您的訊息，我目前不在線",)),
    ("off_hours_prefix", ("您好，小編將於工作日",)),
    ("system", ("잠재 고객 단계를", "거의 완료되었습니다", "請點按我們提供的其中一個選項", "Customer님이")),
)
FLOW_MIN_REPEAT = 10
FLOW_MAX_GAP_MS = 3000
GOT_AUTO_KINDS = ("off_hours_form", "away", "off_hours_prefix")


def static_auto_kind(content):
    """§2.1 의 문구 규칙(flow 앞까지). 맞는 것이 없으면 None."""
    if not content:
        return None
    for kind, needle in AUTO_CONTAINS:
        if needle in content:
            return kind
    for kind, prefixes in AUTO_PREFIX:
        if content.startswith(prefixes):
            return kind
    return None


# ---------------------------------------------------------------- §2.2 예약표 칸 사전
FIELDS = {
    "date": ("希望預約日期與時間", "預約日期與時間", "來院日期時間", "預約日期", "來院日期"),
    "name": ("護照英文姓名", "姓名", "Name", "이름"),
    "birth": ("西元出生年月日", "西元生日年月日", "出生年月日", "生日年月日", "生日", "Birth", "생년월일"),
    "nationality": ("國籍", "国籍", "Nationality", "국적"),
    "gender": ("性別", "性别", "Gender", "성별"),
    "procedure": ("希望施作項目", "施作項目", "預算"),
    "interpreter": ("是否需要翻譯人員", "是否需要翻譯", "是否需要口譯員", "翻譯", "口譯"),
    "director": ("是否需要院長商談", "院長商談"),
    "phone": ("聯絡電話", "聯繫電話", "聯絡方式", "聯繫方式", "電話"),
    "email": ("Email", "email", "E-mail"),
    "medical": ("施作經歷", "過敏", "蟹足腫", "藥物", "懷孕", "相關施作", "相關施術"),
}
LABELS = sorted(((lab, f) for f, labs in FIELDS.items() for lab in labs), key=lambda x: (-len(x[0]), x[0]))

_PAREN = re.compile(r"（[^（）]{0,40}）|\([^()]{0,40}\)")
_SECTION = re.compile(r"(★|📝)[^\n]*")
_LEAD = re.compile(r"^[\s:：]+")


def is_word_char(ch):
    """숫자 · 라틴 · 한자 · 가나 · 한글."""
    if ch.isdigit():
        return True
    s = script_of(ch)
    return s in ("latin", "han", "kana", "hangul")


def find_labels(text):
    """칸 이름 자리를 긴 것부터 겹치지 않게 찾는다 → [(시작, 끝, 칸)] 시작 순."""
    taken = []
    for lab, field in LABELS:
        start = 0
        while True:
            i = text.find(lab, start)
            if i < 0:
                break
            j = i + len(lab)
            if not any(i < b and a < j for a, b, _f in taken):
                taken.append((i, j, field))
            start = i + 1
    return sorted(taken)


def clean_value(v):
    v = _PAREN.sub("", v)
    v = _SECTION.sub("", v)
    return _LEAD.sub("", v)


def count_fields(text):
    """§2.3-1 → (form_labels, form_filled, {칸: 값 목록})."""
    if not text:
        return 0, 0, {}
    spans = find_labels(text)
    values = defaultdict(list)
    for k, (_i, j, field) in enumerate(spans):
        if k + 1 < len(spans):
            end = spans[k + 1][0]
        else:
            nl = text.find("\n", j)
            end = len(text) if nl < 0 else nl
        values[field].append(clean_value(text[j:end]))
    filled = {f for f, vs in values.items() if any(any(is_word_char(c) for c in v) for v in vs)}
    return len(values), len(filled), dict(values)


def field_value(text, field):
    """그 칸의 채운 값(처음 것 · 앞뒤 공백 정리). 없으면 None."""
    _l, _f, values = count_fields(text)
    for v in values.get(field, []):
        if any(is_word_char(c) for c in v):
            return v.strip()
    return None


# ---------------------------------------------------------------- §3 언어

_URL = re.compile(r"(https?://|www\.)\S+", re.I)
EN_WORDS = frozenset((
    "the", "is", "are", "you", "and", "to", "for", "can", "how", "what", "please", "thanks", "thank",
    "hi", "hello", "i", "my", "me", "do", "does", "want", "would", "like", "much", "price", "have",
    "it", "this", "of", "in",
))
_LATIN_WORD = re.compile(r"[A-Za-z]+")


def script_of(ch):
    o = ord(ch)
    if 0xAC00 <= o <= 0xD7A3 or 0x1100 <= o <= 0x11FF or 0x3130 <= o <= 0x318F or 0xA960 <= o <= 0xA97F:
        return "hangul"
    if 0x3040 <= o <= 0x30FF or 0x31F0 <= o <= 0x31FF or 0xFF66 <= o <= 0xFF9F:
        return "kana"
    if (0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF or 0xF900 <= o <= 0xFAFF
            or 0x20000 <= o <= 0x3FFFF or o == 0x3007):
        return "han"
    cat = unicodedata.category(ch)
    if not cat.startswith("L"):
        return None
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return "other"
    if "LATIN" in name:
        return "latin"
    return "other"


def is_emoji(ch):
    o = ord(ch)
    return 0x1F300 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF


class HanSplit:
    """OpenCC 로 번간 글자 수를 센다."""

    def __init__(self):
        import opencc  # requirements-layer2.txt
        self.t2s = opencc.OpenCC("t2s")
        self.s2t = opencc.OpenCC("s2t")

    @staticmethod
    def _changed(conv, han):
        out = conv.convert(han)
        if len(out) == len(han):
            return sum(a != b for a, b in zip(han, out))
        return sum(conv.convert(c) != c for c in han)

    def counts(self, han):
        if not han:
            return 0, 0
        return self._changed(self.t2s, han), self._changed(self.s2t, han)


def message_lang(content, split):
    """§3 메시지 언어 → (lang, n_letters, han_trad, han_simp, n_emoji)."""
    if not content:
        return "none", 0, 0, 0, 0
    text = _URL.sub(" ", content)
    n_emoji = sum(is_emoji(c) for c in text)
    cnt = Counter()
    han_chars = []
    for c in text:
        s = script_of(c)
        if s:
            cnt[s] += 1
            if s == "han":
                han_chars.append(c)
    n = sum(cnt.values())
    trad, simp = split.counts("".join(han_chars)) if han_chars else (0, 0)
    if n == 0:
        return "none", 0, trad, simp, n_emoji
    H, K, C, L, O = cnt["hangul"], cnt["kana"], cnt["han"], cnt["latin"], cnt["other"]
    if H >= max(C + K, L, O):
        lang = "ko"
    elif K >= 1 and C + K >= max(L, O):
        lang = "ja"
    elif C >= max(L, O):
        lang = "zh-Hant" if trad > simp else "zh-Hans" if simp > trad else "zh"
    elif L >= O:
        words = {w.lower() for w in _LATIN_WORD.findall(text)}
        lang = "en" if words & EN_WORDS else "other"
    else:
        lang = "other"
    return lang, n, trad, simp, n_emoji


# ---------------------------------------------------------------- §2.4 E-2 자료 꼴

_BIRTH = re.compile(r"(?<!\d)(19[2-9]\d|200\d)\s*[./\-年]?\s*(0?[1-9]|1[0-2])\s*[./\-月]?\s*(0?[1-9]|[12]\d|3[01])(?!\d)")
_DATE = re.compile(r"(?<!\d)(?:20[2-3]\d\s*[./\-年]\s*)?(0?[1-9]|1[0-2])\s*[./\-月]\s*(0?[1-9]|[12]\d|3[01])(?!\d)")
_UPPER_NAME = re.compile(r"\b[A-Z]{2,}[ ,\-]+[A-Z]{2,}\b")


def looks_like_data(text):
    """E-2 의 꼴 — (생년월일 + 대문자 영문 이름) · (날짜 + 대문자 영문 이름) · (날짜 + 생년월일 · 200자 미만)."""
    if not text:
        return False
    birth = bool(_BIRTH.search(text))
    rest = _BIRTH.sub(" ", text)
    date = bool(_DATE.search(rest))
    upper = bool(_UPPER_NAME.search(text))
    return (birth and upper) or (date and upper) or (date and birth and len(text) < 200)


HANDOFF = re.compile(r"(?<![A-Za-z])line(?![A-Za-z])|whatsapp|wechat|카카오", re.I)  # 낱말 = 앞뒤가 라틴 글자가 아님(한자 옆 LINE 도 낱말)


# ---------------------------------------------------------------- §4 국적 대응표 (예약표 國籍 칸 값 → 코드)
NATIONALITY_MAP = (
    ("TW", ("台灣", "臺灣", "台湾", "taiwan", "中華民國", "中华民国", "台", "臺", "roc", "tw")),
    ("HK", ("香港", "hong kong", "hongkong", "hk")),
    ("MO", ("澳門", "澳门", "macau", "macao")),
    ("CN", ("中國", "中国", "china", "大陸", "大陆")),
    ("MY", ("馬來西亞", "马来西亚", "malaysia", "大馬")),
    ("SG", ("新加坡", "singapore")),
    ("US", ("美國", "美国", "usa", "united states", "america")),
    ("CA", ("加拿大", "canada")),
    ("AU", ("澳洲", "澳大利亞", "australia")),
    ("JP", ("日本", "japan")),
    ("KR", ("韓國", "韩国", "korea", "한국")),
    ("TH", ("泰國", "泰国", "thailand")),
    ("VN", ("越南", "vietnam")),
    ("PH", ("菲律賓", "philippines")),
    ("ID", ("印尼", "indonesia")),
    ("GB", ("英國", "英国", "uk", "united kingdom")),
)
LANG_TO_NAT = {"zh-Hant": "TW/HK", "zh-Hans": "CN", "ko": "KR", "ja": "JP"}


def map_nationality(raw):
    v = raw.strip().lower()
    v = re.sub(r"(?<=[a-z])\.(?=[a-z])", "", v)  # R.O.C → roc
    v = re.sub(r"[\s　:：。.,，、]+$", "", v)
    for code, words in NATIONALITY_MAP:
        for w in words:
            if len(w) <= 3 and w.isascii():
                if re.fullmatch(r"[\W_]*" + re.escape(w) + r"[\W_]*", v):
                    return code
            elif w in v:
                return code
    return "other"


# ---------------------------------------------------------------- 스키마

COMMON = ("judge TEXT NOT NULL CHECK (judge IN ('rule', 'llm', 'human')), "
          "evidence_message_id INTEGER REFERENCES message (message_id), version TEXT NOT NULL")
RULE_TABLES = ("l2_message", "l2_conversation_lang", "l2_booking_stage", "l2_nationality", "l2_review_queue")
DDL = {
    "l2_message": "CREATE TABLE l2_message (message_id INTEGER PRIMARY KEY REFERENCES message (message_id), "
                  "lang TEXT NOT NULL CHECK (lang IN ('zh-Hant','zh-Hans','zh','en','ko','ja','other','none')), "
                  "n_letters INTEGER NOT NULL, han_trad INTEGER NOT NULL, han_simp INTEGER NOT NULL, "
                  "n_emoji INTEGER NOT NULL, auto_kind TEXT CHECK (auto_kind IN "
                  "('off_hours_form','away','off_hours_prefix','system','flow')), "
                  "form_labels INTEGER NOT NULL, form_filled INTEGER NOT NULL, " + COMMON + ")",
    "l2_conversation_lang": "CREATE TABLE l2_conversation_lang (conversation_id INTEGER PRIMARY KEY "
                            "REFERENCES conversation (conversation_id), lang TEXT NOT NULL CHECK (lang IN "
                            "('zh-Hant','zh-Hans','zh','en','ko','ja','other','none')), top_share REAL, "
                            "is_mixed INTEGER NOT NULL, n_letters INTEGER NOT NULL, " + COMMON + ")",
    "l2_booking_stage": "CREATE TABLE l2_booking_stage (conversation_id INTEGER PRIMARY KEY "
                        "REFERENCES conversation (conversation_id), "
                        "stage TEXT NOT NULL CHECK (stage IN ('inquiry','form_sent','form_filled')), "
                        "rule_stage TEXT NOT NULL CHECK (rule_stage IN ('inquiry','form_sent','form_filled')), "
                        "form_source TEXT NOT NULL CHECK (form_source IN ('staff','flow','auto','none')), "
                        "sent_message_id INTEGER REFERENCES message (message_id), "
                        "filled_message_id INTEGER REFERENCES message (message_id), "
                        "filled_fields INTEGER NOT NULL, got_auto_reply INTEGER NOT NULL, "
                        "handoff_mentioned INTEGER NOT NULL, " + COMMON + ")",
    "l2_nationality": "CREATE TABLE l2_nationality (conversation_id INTEGER PRIMARY KEY "
                      "REFERENCES conversation (conversation_id), nationality TEXT, "
                      "source TEXT NOT NULL CHECK (source IN ('form','self','lang','none')), raw_value TEXT, "
                      "llm_confidence REAL, " + COMMON + ")",
    "l2_review_queue": "CREATE TABLE l2_review_queue (queue_id INTEGER PRIMARY KEY, conversation_id INTEGER NOT NULL "
                       "REFERENCES conversation (conversation_id), reason TEXT NOT NULL CHECK (reason IN "
                       "('E-1','E-2','E-3')), rule_stage TEXT NOT NULL, human_stage TEXT CHECK (human_stage IN "
                       "('inquiry','form_sent','form_filled')), decided_at TEXT, " + COMMON + ")",
}


class Halt(Exception):
    pass


# ---------------------------------------------------------------- 판정

def load_l1(con):
    convs = {}
    for cid, ch in con.execute("SELECT conversation_id, channel FROM conversation ORDER BY conversation_id"):
        convs[cid] = {"ch": ch, "msgs": []}
    for mid, cid, seq, own, ms, content in con.execute(
            "SELECT message_id, conversation_id, seq, is_owner, sent_at_ms, content FROM message "
            "ORDER BY conversation_id, seq"):
        convs[cid]["msgs"].append({"id": mid, "seq": seq, "own": own == 1, "ms": ms, "content": content})
    return convs


def judge_messages(convs, split):
    # flow 후보: 같은 채널 · 같은 본문인 우리 메시지 수
    same = Counter()
    for c in convs.values():
        for m in c["msgs"]:
            if m["own"] and m["content"]:
                same[(c["ch"], m["content"])] += 1
    for c in convs.values():
        prev_ms = None
        for m in c["msgs"]:
            kind = None
            if m["own"]:
                kind = static_auto_kind(m["content"])
                if (kind is None and m["content"] and same[(c["ch"], m["content"])] >= FLOW_MIN_REPEAT
                        and prev_ms is not None and m["ms"] - prev_ms <= FLOW_MAX_GAP_MS):
                    kind = "flow"
            m["auto"] = kind
            m["lang"], m["n"], m["trad"], m["simp"], m["emoji"] = message_lang(m["content"], split)
            m["labels"], m["filled"], _v = count_fields(m["content"])
            prev_ms = m["ms"]


def judge_room(c):
    msgs = c["msgs"]
    cust = [m for m in msgs if not m["own"]]
    # 예약표 발송
    first_of = {}
    for m in msgs:
        if m["own"] and m["labels"] >= 3:
            src = "auto" if m["auto"] in ("off_hours_form", "off_hours_prefix") else \
                  "flow" if m["auto"] == "flow" else "staff"
            first_of.setdefault(src, m)
    form_source = next((s for s in ("staff", "flow", "auto") if s in first_of), "none")
    sent = first_of.get(form_source)
    # 회신
    filled_fields = max((m["filled"] for m in cust), default=0)
    filled_msg = None
    for m in cust:
        if m["filled"] >= 2 and (filled_msg is None or m["filled"] > filled_msg["filled"]):
            filled_msg = m
    if filled_msg is not None:
        stage = "form_filled"
    elif "staff" in first_of or "flow" in first_of:
        stage = "form_sent"
    else:
        stage = "inquiry"
    got_auto = int(any(m["own"] and m["auto"] in GOT_AUTO_KINDS for m in msgs))
    handoff = int(stage != "form_filled" and any(m["own"] and m["content"] and HANDOFF.search(m["content"])
                                                  for m in msgs))
    ev = filled_msg or sent or msgs[0]
    c["stage"] = {
        "stage": stage, "form_source": form_source, "sent": sent["id"] if sent else None,
        "filled": filled_msg["id"] if filled_msg else None, "filled_msg": filled_msg,
        "filled_fields": filled_fields, "got_auto": got_auto, "handoff": handoff, "evidence": ev["id"],
    }
    # 방 언어
    per = Counter()
    trad = sum(m["trad"] for m in cust)
    simp = sum(m["simp"] for m in cust)
    zh_to = "zh-Hant" if trad > simp else "zh-Hans" if simp > trad else "zh"
    best_msg = {}
    for m in cust:
        if m["n"] == 0:
            continue
        lang = zh_to if m["lang"] == "zh" else m["lang"]
        per[lang] += m["n"]
        if lang not in best_msg or m["n"] > best_msg[lang]["n"]:
            best_msg[lang] = m
    total = sum(per.values())
    if total == 0:
        lang, share, ev_lang = "none", None, (cust[0]["id"] if cust else None)
    else:
        order = ("zh-Hant", "zh-Hans", "zh", "en", "ko", "ja", "other")
        lang = max(order, key=lambda k: (per[k], -order.index(k)))
        share = per[lang] / total
        ev_lang = best_msg[lang]["id"]
    c["lang"] = {"lang": lang, "share": share, "mixed": int(share is not None and share < 0.8),
                 "n": total, "evidence": ev_lang}
    # 사람 확인 큐
    reason = None
    if form_source != "none" and filled_fields == 1:
        reason = "E-1"
    elif filled_fields < 2 and first_of:
        first_form = min(m["seq"] for m in first_of.values())
        if any(m["seq"] > first_form and m["labels"] == 0 and looks_like_data(m["content"]) for m in cust):
            reason = "E-2"
    if reason is None and 2 <= filled_fields <= 3:
        reason = "E-3"
    c["reason"] = reason


def nationality_rows(convs, llm):
    out = {}
    for cid, c in convs.items():
        st, lg = c["stage"], c["lang"]
        if st["filled_msg"] is not None:
            raw = field_value(st["filled_msg"]["content"], "nationality")
            if raw:
                out[cid] = (map_nationality(raw), "form", raw, None, "rule", st["filled"])
                continue
        if cid in llm and llm[cid][0]:
            code, conf, ev = llm[cid]
            out[cid] = (code, "self", None, conf, "llm", ev if ev is not None else lg["evidence"])
            continue
        code = LANG_TO_NAT.get(lg["lang"])
        out[cid] = (code, "lang" if code else "none", None, None, "rule", lg["evidence"])
    return out


def read_llm(con):
    have = con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='l2_llm_label'").fetchone()
    if not have:
        return {}
    out = {}
    for cid, nat, conf, evs in con.execute(
            "SELECT conversation_id, nationality_mention, confidence, evidence_message_ids FROM l2_llm_label"):
        ids = json.loads(evs) if evs else []
        out[cid] = (nat, conf, ids[0] if ids else None)
    return out


def read_decisions(path):
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            qid = int(row["queue_id"])
            hs = (row.get("human_stage") or "").strip()
            if not hs:
                continue
            if hs not in ("inquiry", "form_sent", "form_filled"):
                raise Halt("decisions: queue_id %d 의 human_stage 값이 목록 밖" % qid)
            out[qid] = hs
    return out


def run(db, queue_out=None, decisions=None, split=None):
    split = split or HanSplit()
    con = sqlite3.connect(db, isolation_level=None)
    con.execute("PRAGMA foreign_keys = ON")
    try:
        convs = load_l1(con)
        judge_messages(convs, split)
        for c in convs.values():
            judge_room(c)
        llm = read_llm(con)
        nat = nationality_rows(convs, llm)
        queue = [(cid, c["reason"], c["stage"]["stage"]) for cid, c in convs.items() if c["reason"]]
        if len(queue) > QUEUE_LIMIT:
            raise Halt("사람 확인 큐 %d건 > %d — 사유별 %s" % (
                len(queue), QUEUE_LIMIT, dict(sorted(Counter(r for _c, r, _s in queue).items()))))
        human = read_decisions(decisions) if decisions and os.path.exists(decisions) else {}
        unknown = set(human) - set(range(1, len(queue) + 1))
        if unknown:
            raise Halt("decisions: 큐에 없는 queue_id %d건" % len(unknown))
        # decided_at = 판정 파일의 수정 시각 — 같은 파일이면 다시 돌려도 같은 값(수용 기준 6)
        now = (datetime.datetime.fromtimestamp(os.path.getmtime(decisions), tz=datetime.timezone.utc)
               .strftime("%Y-%m-%dT%H:%M:%SZ") if human else None)

        con.execute("BEGIN")
        for t in RULE_TABLES:
            con.execute("DROP TABLE IF EXISTS %s" % t)
        for t in RULE_TABLES:
            con.execute(DDL[t])
        con.executemany("INSERT INTO l2_message VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
            (m["id"], m["lang"], m["n"], m["trad"], m["simp"], m["emoji"], m["auto"], m["labels"], m["filled"],
             "rule", m["id"], VERSION) for c in convs.values() for m in c["msgs"]))
        con.executemany("INSERT INTO l2_conversation_lang VALUES (?,?,?,?,?,?,?,?)", (
            (cid, c["lang"]["lang"], c["lang"]["share"], c["lang"]["mixed"], c["lang"]["n"],
             "rule", c["lang"]["evidence"], VERSION) for cid, c in convs.items()))
        stage_human = {}
        qrows = []
        for qid, (cid, reason, rule_stage) in enumerate(queue, start=1):
            hs = human.get(qid)
            if hs:
                stage_human[cid] = hs
            qrows.append((qid, cid, reason, rule_stage, hs, now if hs else None,
                          "human" if hs else "rule", convs[cid]["stage"]["evidence"], VERSION))
        con.executemany("INSERT INTO l2_booking_stage VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
            (cid, stage_human.get(cid, s["stage"]), s["stage"], s["form_source"], s["sent"], s["filled"],
             s["filled_fields"], s["got_auto"], s["handoff"], "human" if cid in stage_human else "rule",
             s["evidence"], VERSION) for cid, c in convs.items() for s in (c["stage"],)))
        con.executemany("INSERT INTO l2_nationality VALUES (?,?,?,?,?,?,?,?)", (
            (cid,) + v[:4] + (v[4], v[5], VERSION) for cid, v in nat.items()))
        con.executemany("INSERT INTO l2_review_queue VALUES (?,?,?,?,?,?,?,?,?)", qrows)
        con.execute("COMMIT")
    except BaseException:
        if con.in_transaction:
            con.execute("ROLLBACK")
        con.close()
        raise
    if queue_out:
        write_queue(con, queue_out)
    con.close()
    return convs, queue


def write_queue(con, path):
    """사람 확인용 — 본문 포함 · 로컬(data/ gitignore)만. 이름은 넣지 않고 [C]/[S] 머리표."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    rows = con.execute("SELECT queue_id, conversation_id, reason, rule_stage, human_stage FROM l2_review_queue "
                       "ORDER BY queue_id").fetchall()
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["queue_id", "conversation_id", "reason", "rule_stage", "human_stage", "transcript"])
        for qid, cid, reason, rs, hs in rows:
            lines = []
            for own, content, auto in con.execute(
                    "SELECT m.is_owner, m.content, l.auto_kind FROM message m JOIN l2_message l USING (message_id) "
                    "WHERE m.conversation_id = ? ORDER BY m.seq", (cid,)):
                tag = "[S]" if own else "[C]"
                if auto:
                    tag = "[S:auto]"
                lines.append("%s %s" % (tag, content if content is not None else "(본문 없음)"))
            w.writerow([qid, cid, reason, rs, hs or "", "\n".join(lines)])


# ---------------------------------------------------------------- 보고(건수만)

def report(db):
    con = sqlite3.connect("file:%s?mode=ro" % os.path.abspath(db), uri=True)
    q = lambda sql: con.execute(sql).fetchall()  # noqa: E731
    J = "JOIN conversation c USING (conversation_id)"

    def by_ch(sql):
        d = defaultdict(dict)
        for ch, k, n in q(sql):
            d[k][ch] = n
        return d

    def line(label, row):
        ig, fb = row.get("instagram", 0), row.get("facebook", 0)
        print("  %-34s IG %6d · FB %6d · 합 %6d" % (label, ig, fb, ig + fb))

    print("2층 규칙 판정 완료 (%s)" % VERSION)
    for t in RULE_TABLES:
        print("  %-22s %6d 행" % (t, q("SELECT COUNT(*) FROM %s" % t)[0][0]))
    print("[단계] SPEC §2.3 기준: form_filled 40/52/92 · form_sent 24/134/158 · inquiry 447/1219/1666")
    st = by_ch("SELECT c.channel, b.rule_stage, COUNT(*) FROM l2_booking_stage b %s GROUP BY 1, 2" % J)
    for k in ("form_filled", "form_sent", "inquiry"):
        line("rule_stage = " + k, st[k])
    fs = by_ch("SELECT c.channel, b.form_source, COUNT(*) FROM l2_booking_stage b %s GROUP BY 1, 2" % J)
    for k in ("staff", "flow", "auto", "none"):
        line("form_source = " + k, fs[k])
    line("예약표 발송 방(staff) — 기준 60/152", fs["staff"])
    line("flow 만 — 기준 0/27", fs["flow"])
    auto_room = by_ch("SELECT c.channel, 'x', COUNT(DISTINCT m.conversation_id) FROM l2_message l "
                      "JOIN message m USING (message_id) %s WHERE l.form_labels >= 3 AND m.is_owner = 1 "
                      "AND l.auto_kind IN ('off_hours_form', 'off_hours_prefix') GROUP BY 1" % J)
    line("자동응답 빈 표 받은 방 — 기준 150/136", auto_room["x"])
    ff_src = by_ch("SELECT c.channel, b.form_source, COUNT(*) FROM l2_booking_stage b %s "
                   "WHERE b.rule_stage = 'form_filled' GROUP BY 1, 2" % J)
    line("form_filled · staff/flow — 기준 36/45", {k: ff_src["staff"].get(k, 0) + ff_src["flow"].get(k, 0)
                                                   for k in ("instagram", "facebook")})
    line("form_filled · auto 만 — 기준 4/5", ff_src["auto"])
    line("form_filled · 표 없음 — 기준 0/2", ff_src["none"])
    nat_f = by_ch("SELECT c.channel, 'x', COUNT(*) FROM l2_nationality n %s WHERE n.source = 'form' GROUP BY 1" % J)
    line("form_filled 중 國籍 칸 채움 — 기준 39/49", nat_f["x"])
    ffb = by_ch("SELECT c.channel, CASE WHEN filled_fields = 0 THEN '0' WHEN filled_fields = 1 THEN '1' "
                "WHEN filled_fields <= 3 THEN '2-3' ELSE '4+' END, COUNT(*) FROM l2_booking_stage b %s GROUP BY 1, 2" % J)
    for k, base in (("0", "460/1330"), ("1", "11/23"), ("2-3", "0/2"), ("4+", "40/50")):
        line("채운 칸 최대 %s — 기준 %s" % (k, base), ffb[k])
    print("[자동응답 메시지 · 방] SPEC §2.1 기준(메시지 IG/FB · 방 IG/FB): off_hours_form 179/150 · 150/125 · "
          "away 188/350 · 148/268 · off_hours_prefix 22/165 · 20/111 · system 0/456 · 0/354")
    ak = by_ch("SELECT c.channel, l.auto_kind, COUNT(*) FROM l2_message l JOIN message m USING (message_id) %s "
               "WHERE l.auto_kind IS NOT NULL GROUP BY 1, 2" % J)
    akr = by_ch("SELECT c.channel, l.auto_kind, COUNT(DISTINCT m.conversation_id) FROM l2_message l "
                "JOIN message m USING (message_id) %s WHERE l.auto_kind IS NOT NULL GROUP BY 1, 2" % J)
    for k in ("off_hours_form", "away", "off_hours_prefix", "system", "flow"):
        line("메시지 auto_kind = " + k, ak[k])
        line("방     auto_kind = " + k, akr[k])
    line("got_auto_reply = 1 — 기준 IG 300", by_ch(
        "SELECT c.channel, 'x', COUNT(*) FROM l2_booking_stage b %s WHERE got_auto_reply = 1 GROUP BY 1" % J)["x"])
    line("handoff_mentioned = 1 — 기준 21/73", by_ch(
        "SELECT c.channel, 'x', COUNT(*) FROM l2_booking_stage b %s WHERE handoff_mentioned = 1 GROUP BY 1" % J)["x"])
    print("[방 언어]")
    lg = by_ch("SELECT c.channel, l.lang, COUNT(*) FROM l2_conversation_lang l %s GROUP BY 1, 2" % J)
    for k in ("zh-Hant", "zh-Hans", "zh", "en", "ko", "ja", "other", "none"):
        line("lang = " + k, lg[k])
    line("is_mixed = 1 — (문자 종류 기준 105/92)", by_ch(
        "SELECT c.channel, 'x', COUNT(*) FROM l2_conversation_lang l %s WHERE is_mixed = 1 GROUP BY 1" % J)["x"])
    ml = by_ch("SELECT c.channel, l.lang, COUNT(*) FROM l2_message l JOIN message m USING (message_id) %s "
               "WHERE m.is_owner = 0 GROUP BY 1, 2" % J)
    for k in ("zh-Hant", "zh-Hans", "zh"):
        line("고객 메시지 lang = " + k, ml[k])
    print("[국적]")
    nt = by_ch("SELECT c.channel, n.source || ':' || COALESCE(n.nationality, 'NULL'), COUNT(*) "
               "FROM l2_nationality n %s GROUP BY 1, 2" % J)
    for k in sorted(nt):
        line(k, nt[k])
    print("[사람 확인 큐] SPEC §2.4 기준: E-1 3/12 · E-2 1/3 · E-3 0/2 · 합 21")
    rq = by_ch("SELECT c.channel, r.reason, COUNT(*) FROM l2_review_queue r %s GROUP BY 1, 2" % J)
    for k in ("E-1", "E-2", "E-3"):
        line("reason = " + k, rq[k])
    print("  사람 판정 반영: %d건" % q("SELECT COUNT(*) FROM l2_review_queue WHERE human_stage IS NOT NULL")[0][0])
    con.close()


def main(argv=None):
    ap = argparse.ArgumentParser(description="2층 규칙 판정 (SPEC-002)")
    ap.add_argument("--db", required=True)
    ap.add_argument("--queue-out", help="사람 확인 큐 CSV(본문 포함 · data/ 아래 로컬만)")
    ap.add_argument("--decisions", help="사람 판정 CSV(queue_id,human_stage) — 있으면 덮는다")
    args = ap.parse_args(argv)
    try:
        run(args.db, args.queue_out, args.decisions)
    except Halt as e:
        print("판정 중단 — " + str(e), file=sys.stderr)
        return 3
    except Exception as e:  # 예외 문구에 값이 들어갈 수 있어 종류만
        print("판정 중단 — 예기치 않은 오류(%s)" % type(e).__name__, file=sys.stderr)
        return 2
    report(args.db)
    return 0


if __name__ == "__main__":
    sys.exit(main())
