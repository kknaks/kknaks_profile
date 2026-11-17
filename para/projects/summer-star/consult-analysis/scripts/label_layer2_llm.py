#!/usr/bin/env python3
"""2층 LLM 라벨 — 방 단위 문의 주제 · 시술 · 본인 국적 언급 · 확정 안내 (SPEC-002 §5 · DEC-002 D-07 · D-08 · D-14).

- 로컬 CLI(`claude -p`)만 부른다. 프롬프트(방 본문)는 표준 입력으로만 — 파일로 쓰지 않는다.
  도구 · MCP · 설정 · 슬래시 명령 · 세션 저장을 끄고, 시스템 프롬프트는 이 스크립트의 짧은 지시문 하나로 바꾼다.
- 결과는 DB `l2_llm_label` 에만. 깨진 JSON · 목록 밖 값은 1번 다시 부르고, 또 실패하면 행을 만들지 않고 건수로 센다.
- 표준 출력에는 건수 · 시간 · 토큰 · 비용만. 본문 · 이름을 찍지 않는다.
- 표본 확인 파일(`--sample-out`)은 본문 앞부분을 담으므로 data/(gitignore) 아래에만 쓴다.
"""

import argparse
import concurrent.futures
import csv
import json
import os
import re
import sqlite3
import statistics
import subprocess
import sys
import tempfile
import time

PROMPT_VERSION = "0.3.0"  # SPEC-002 0.3.0 — 예약표 메시지 제외 · topics 는 고객이 말한 것만
VERSION = "llm-" + PROMPT_VERSION
MAX_CHARS = 6000
HALF = 3000

TOPICS = ("procedure", "price", "schedule", "location", "interpreter", "result", "safety", "promo", "other")
PROCEDURES = ("ulthera", "thermage", "sofwave", "onda", "titanium", "rf_microneedle", "juvelook", "botox",
              "filler", "skinbooster", "laser", "rejuran", "mole_wart_removal", "acne_scar", "pore_texture",
              "eye_area", "fat_dissolving", "tune", "lifting_unspecified", "other")
KEYS = ("topics", "procedures", "procedures_other", "nationality_mention", "staff_confirmed", "confidence",
        "evidence")
OTHER_MAX = 20

# SPEC-002 §5 별칭 표(우리 메시지에 나오는 시술 이름 — 고객 정보 아님)
ALIASES = (
    ("ulthera", "美國音波, 音波, Ulthera, Ultherapy"),
    ("thermage", "鳳凰電波, 鳳凰, 電波, Thermage, 熱瑪吉"),
    ("ulthera+thermage", "電音波 (output both)"),
    ("sofwave", "索夫波, Sofwave"),
    ("onda", "Onda"),
    ("titanium", "鈦提升, 鈦, Titanium, Titan"),
    ("rf_microneedle", "黃金微針, 微針, Potenza"),
    ("juvelook", "喬雅露, Juvelook, 藍瓶"),
    ("rejuran", "麗珠蘭, Rejuran"),
    ("skinbooster", "水光針, 水光, 光針, Skinvive"),
    ("botox", "肉毒, Xeomin, Botox"),
    ("filler", "玻尿酸, Belotero, Restylane, 瑞絲朗"),
    ("laser", "雷射, 皮秒"),
    ("acne_scar", "痘疤, 凹洞"),
    ("pore_texture", "毛孔"),
    ("eye_area", "眼周, 眼下, 黑眼圈, 淚溝, 眼袋"),
    ("mole_wart_removal", "痣, 疣"),
    ("fat_dissolving", "消脂針"),
    ("tune", "Tune"),
)

SYSTEM_PROMPT = (
    "You label one clinic DM conversation. Lines are numbered; [C]=customer, [S]=clinic staff.\n"
    "Reply with ONE JSON object only, no other text:\n"
    '{"topics":[],"procedures":[],"procedures_other":[],"nationality_mention":null,"staff_confirmed":false,'
    '"confidence":0.0,"evidence":[]}\n'
    "topics: only what the CUSTOMER [C] asks or says — clinic [S] guidance and form field names are not topics.\n"
    "topics (0+): procedure=asks about a treatment, price=price/budget, schedule=booking/date, "
    "location=address/transport, interpreter=interpreter/language, result=effect/reviews/before-after, "
    "safety=side effects/recovery/contraindication, promo=event/discount, other.\n"
    "procedures (0+): " + ", ".join(PROCEDURES) + " (lifting_unspecified=lifting/拉提 without a named device).\n"
    "aliases: " + "; ".join("%s=%s" % a for a in ALIASES) + "\n"
    "procedures_other: only when procedures has other — the original treatment/device name(s), "
    "each under 20 chars, no sentences; else [].\n"
    "nationality_mention: ISO 3166 alpha-2 code (TW, HK, CN, US ...) only if the customer states their own "
    "nationality or where they live; else null. Do not guess from language.\n"
    "staff_confirmed: true only if [S] confirms a booking with a concrete date and time.\n"
    "confidence: 0..1. evidence: line numbers (integers) that support the labels."
)


class Invalid(Exception):
    pass


# ---------------------------------------------------------------- 입력

def room_lines(con, cid):
    """시간순 [(message_id, tag, 본문)] — 자동응답(우리) · 본문 없는 메시지 · 예약표 메시지(0.3.0) 제외."""
    out = []
    for mid, own, content, auto, labels, filled in con.execute(
            "SELECT m.message_id, m.is_owner, m.content, l.auto_kind, l.form_labels, l.form_filled FROM message m "
            "JOIN l2_message l USING (message_id) WHERE m.conversation_id = ? ORDER BY m.seq", (cid,)):
        if own and auto is not None:
            continue
        if own and labels >= 3:  # 우리 예약표 발송
            continue
        if not own and filled >= 2:  # 고객 예약표 회신
            continue
        if content is None or not content.strip():
            continue
        out.append((mid, "[S]" if own else "[C]", " / ".join(content.split("\n"))))
    return out


def build_input(lines):
    """번호 붙인 본문. 본문 합 > 6,000자면 앞 3,000자 + 뒤 3,000자(번호는 원래대로) → (text, truncated)."""
    total = sum(len(t) for _m, _g, t in lines)
    numbered = [(i, g, t) for i, (_m, g, t) in enumerate(lines, start=1)]
    if total <= MAX_CHARS:
        return "\n".join("%d %s %s" % x for x in numbered), False
    head, used = [], 0
    for i, g, t in numbered:
        if used >= HALF:
            break
        take = t[:HALF - used]
        head.append((i, g, take))
        used += len(take)
    tail, used = [], 0
    for i, g, t in reversed(numbered):
        if used >= HALF or i <= head[-1][0]:
            break
        take = t[-(HALF - used):]
        tail.append((i, g, take))
        used += len(take)
    tail.reverse()
    text = "\n".join("%d %s %s" % x for x in head) + "\n…\n" + "\n".join("%d %s %s" % x for x in tail)
    return text, True


# ---------------------------------------------------------------- 출력 검증

def parse_output(text, n_lines):
    """모델 답 → 검증된 dict. 목록 밖 값 · 깨진 JSON · 빠진 키는 Invalid."""
    s = (text or "").strip()
    m = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", s, re.S)
    if m:
        s = m.group(1)
    try:
        obj = json.loads(s)
    except ValueError:
        raise Invalid("json") from None
    if not isinstance(obj, dict) or set(obj) != set(KEYS):
        raise Invalid("keys")
    for k, allowed in (("topics", TOPICS), ("procedures", PROCEDURES)):
        v = obj[k]
        if not isinstance(v, list) or any(not isinstance(x, str) or x not in allowed for x in v):
            raise Invalid(k)
    po = obj["procedures_other"]
    if (not isinstance(po, list) or any(not isinstance(x, str) or not x.strip() or len(x) > OTHER_MAX for x in po)
            or (po and "other" not in obj["procedures"])):
        raise Invalid("procedures_other")
    nat = obj["nationality_mention"]
    if nat is not None and not (isinstance(nat, str) and re.fullmatch(r"[A-Z]{2}", nat)):
        raise Invalid("nationality_mention")
    if not isinstance(obj["staff_confirmed"], bool):
        raise Invalid("staff_confirmed")
    conf = obj["confidence"]
    if isinstance(conf, bool) or not isinstance(conf, (int, float)) or not 0 <= conf <= 1:
        raise Invalid("confidence")
    ev = obj["evidence"]
    if not isinstance(ev, list) or any(isinstance(x, bool) or not isinstance(x, int) or not 1 <= x <= n_lines
                                       for x in ev):
        raise Invalid("evidence")
    return {
        "topics": sorted(set(obj["topics"]), key=TOPICS.index),
        "procedures": sorted(set(obj["procedures"]), key=PROCEDURES.index),
        "procedures_other": sorted({x.strip() for x in po}),
        "nationality_mention": nat, "staff_confirmed": obj["staff_confirmed"],
        "confidence": float(conf), "evidence": sorted(set(ev)),
    }


# ---------------------------------------------------------------- 호출

def call_cli(cli, model, prompt, workdir, effort=None):
    cmd = [cli, "-p", "--model", model] + (["--effort", effort] if effort else []) + [ "--output-format", "json", "--tools", "", "--strict-mcp-config",
           "--setting-sources", "", "--disable-slash-commands", "--no-session-persistence", "--no-chrome",
           "--system-prompt", SYSTEM_PROMPT]
    p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=workdir, timeout=300)
    try:
        env = json.loads(p.stdout)
    except ValueError:
        return None, {}
    usage = env.get("usage") or {}
    meta = {
        "input": usage.get("input_tokens", 0), "output": usage.get("output_tokens", 0),
        "cache_write": usage.get("cache_creation_input_tokens", 0),
        "cache_read": usage.get("cache_read_input_tokens", 0),
        "cost": env.get("total_cost_usd", 0.0) or 0.0,
        "models": list((env.get("modelUsage") or {}).keys()),
    }
    if env.get("is_error"):
        return None, meta
    return env.get("result"), meta


def label_room(cli, model, cid, lines, workdir, effort=None):
    text, truncated = build_input(lines)
    t0 = time.time()
    tries, usage, result, why = 0, [], None, None
    for _ in range(2):  # 처음 + 다시 1번
        tries += 1
        out, meta = call_cli(cli, model, text, workdir, effort)
        usage.append(meta)
        try:
            result = parse_output(out, len(lines))
            break
        except Invalid as e:
            why = str(e)
    return {"cid": cid, "result": result, "why": why, "tries": tries, "usage": usage,
            "secs": time.time() - t0, "truncated": truncated, "lines": lines}


# ---------------------------------------------------------------- DB

DDL = ("CREATE TABLE IF NOT EXISTS l2_llm_label (conversation_id INTEGER PRIMARY KEY REFERENCES conversation "
       "(conversation_id), topics TEXT NOT NULL, procedures TEXT NOT NULL, procedures_other TEXT NOT NULL, "
       "nationality_mention TEXT, "
       "staff_confirmed INTEGER NOT NULL, confidence REAL NOT NULL, model TEXT NOT NULL, "
       "evidence_message_ids TEXT NOT NULL, input_truncated INTEGER NOT NULL, "
       "judge TEXT NOT NULL CHECK (judge IN ('rule', 'llm', 'human')), "
       "evidence_message_id INTEGER REFERENCES message (message_id), version TEXT NOT NULL)")


def target_rooms(con):
    """고객 본문이 있는 방 → {conversation_id: (channel, stage, lang)}."""
    rows = con.execute(
        "SELECT c.conversation_id, c.channel, b.stage, l.lang FROM conversation c "
        "JOIN l2_booking_stage b USING (conversation_id) JOIN l2_conversation_lang l USING (conversation_id) "
        "WHERE EXISTS (SELECT 1 FROM message m WHERE m.conversation_id = c.conversation_id AND m.is_owner = 0 "
        "AND m.content IS NOT NULL AND TRIM(m.content) != '') ORDER BY c.conversation_id").fetchall()
    return {cid: (ch, st, lg) for cid, ch, st, lg in rows}


def pick_sample(rooms, n):
    """단계 3종 × 채널 2 칸에 고르게 — 칸마다 id 순으로 같은 간격. 다시 돌려도 같은 방."""
    cells = {}
    for cid, (ch, st, _lg) in sorted(rooms.items()):
        cells.setdefault((ch, st), []).append(cid)
    keys = sorted(cells)
    per = n // len(keys)
    out = []
    for k in keys:
        ids = cells[k]
        take = min(per, len(ids))
        out += [ids[(i * len(ids)) // take] for i in range(take)]
    rest = [c for k in keys for c in cells[k] if c not in out]
    out += rest[:n - len(out)]
    return sorted(out)


def save(con, r, fallback_model):
    res = r["result"]
    ids = [r["lines"][i - 1][0] for i in res["evidence"]]
    first_c = next(m for m, g, _t in r["lines"] if g == "[C]")
    model = ",".join(sorted(set(m for u in r["usage"] for m in u.get("models", [])))) or fallback_model
    con.execute("INSERT INTO l2_llm_label VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (
        r["cid"], json.dumps(res["topics"]), json.dumps(res["procedures"]),
        json.dumps(res["procedures_other"], ensure_ascii=False), res["nationality_mention"],
        int(res["staff_confirmed"]), res["confidence"], model, json.dumps(ids), int(r["truncated"]),
        "llm", ids[0] if ids else first_c, VERSION))
    con.commit()


def main(argv=None):
    ap = argparse.ArgumentParser(description="2층 LLM 라벨 (SPEC-002 §5)")
    ap.add_argument("--db", required=True)
    ap.add_argument("--cli", default="claude")
    ap.add_argument("--model", required=True, help="claude -p 의 --model 값(예: haiku)")
    ap.add_argument("--sample", type=int, help="표본 방 수(단계 × 채널 고르게). 없으면 전체")
    ap.add_argument("--reset", action="store_true", help="있던 라벨을 지운다(없으면 이어 하기)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--effort", help="claude -p 의 --effort 값(예: low)")
    ap.add_argument("--sample-from", help="표본 방 id 를 이 CSV(conversation_id 칸)에서 읽는다 — 같은 방으로 재시험")
    ap.add_argument("--sample-out", help="표본 확인 CSV(본문 앞 300자 포함 · data/ 아래 로컬만)")
    args = ap.parse_args(argv)

    con = sqlite3.connect(args.db)
    con.execute("PRAGMA foreign_keys = ON")
    cols = [r[1] for r in con.execute("PRAGMA table_info(l2_llm_label)")]
    if cols and "procedures_other" not in cols:
        if not args.reset:
            print("중단 — l2_llm_label 이 옛 칸 구성이다. --reset 으로 다시 만든다", file=sys.stderr)
            return 3
        con.execute("DROP TABLE l2_llm_label")
    con.execute(DDL)
    if args.reset:
        con.execute("DELETE FROM l2_llm_label")
    con.commit()
    rooms = target_rooms(con)
    if args.sample_from:
        with open(args.sample_from, newline="", encoding="utf-8") as fh:
            todo = sorted(int(r["conversation_id"]) for r in csv.DictReader(fh))
    elif args.sample:
        todo = pick_sample(rooms, args.sample)
    else:
        todo = sorted(rooms)
    done = {r[0] for r in con.execute("SELECT conversation_id FROM l2_llm_label")}
    todo = [c for c in todo if c not in done]
    lines_of = {cid: room_lines(con, cid) for cid in todo}
    skipped = [c for c in todo if not any(g == "[C]" for _m, g, _t in lines_of[c])]
    todo = [c for c in todo if c not in skipped]
    print("대상 방 %d · 이번에 부를 방 %d · 이미 라벨 %d · 예약표 메시지를 빼니 고객 본문이 없어 부르지 않은 방 %d" % (
        len(rooms), len(todo), len(done), len(skipped)))

    results = []
    fails = 0
    model_names = set()
    with tempfile.TemporaryDirectory() as workdir, \
            concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(label_room, args.cli, args.model, cid, lines_of[cid], workdir, args.effort)
                for cid in todo]
        for k, f in enumerate(concurrent.futures.as_completed(futs), start=1):
            r = f.result()
            results.append(r)
            for u in r["usage"]:
                model_names.update(u.get("models", []))
            if r["result"] is None:
                fails += 1
            else:
                save(con, r, args.model)  # 방마다 바로 저장 — 끊겨도 다시 돌리면 이어 한다
            if k % 100 == 0:
                print("진행 %d / %d · 실패 %d" % (k, len(todo), fails), flush=True)
    results.sort(key=lambda r: r["cid"])

    if args.sample_out:
        os.makedirs(os.path.dirname(os.path.abspath(args.sample_out)), exist_ok=True)
        with open(args.sample_out, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["conversation_id", "channel", "stage", "lang", "ok", "topics", "procedures", "procedures_other",
                        "nationality_mention", "staff_confirmed", "confidence", "input_truncated",
                        "customer_text_300"])
            for r in results:
                ch, st, lg = rooms[r["cid"]]
                res = r["result"] or {}
                ctext = " / ".join(t for _m, g, t in r["lines"] if g == "[C]")[:300]
                w.writerow([r["cid"], ch, st, lg, int(r["result"] is not None),
                            json.dumps(res.get("topics")), json.dumps(res.get("procedures")),
                            json.dumps(res.get("procedures_other"), ensure_ascii=False),
                            res.get("nationality_mention"), res.get("staff_confirmed"), res.get("confidence"),
                            int(r["truncated"]), ctext])

    report(results, fails, model_names, len(rooms))
    con.close()
    return 0 if fails == 0 else 1


def report(results, fails, model_names, n_all):
    ok = [r for r in results if r["result"] is not None]
    n = len(results)
    print("부른 방 %d · 라벨 %d · 실패 %d(두 번 다 검증 실패) · 다시 부른 방 %d" % (
        n, len(ok), fails, sum(r["tries"] > 1 for r in results)))
    print("모델: %s" % ", ".join(sorted(model_names)))
    if not results:
        return
    if ok:
        t_other = sum("other" in r["result"]["topics"] for r in ok)
        p_any = [r for r in ok if r["result"]["procedures"]]
        p_other = sum("other" in r["result"]["procedures"] for r in p_any)
        vals = [v for r in ok for v in r["result"]["procedures"]]
        print("topics 에 other 가 든 방 %d / %d · procedures 가 있는 방 %d / %d · 그중 other 가 든 방 %d / %d"
              " · procedures 값 중 other %d / %d" % (t_other, len(ok), len(p_any), len(ok), p_other,
                                                    len(p_any), vals.count("other"), len(vals)))
        print("procedures_other 값 종류 %d(값은 찍지 않는다 — DB 만)" % len(
            {x for r in ok for x in r["result"]["procedures_other"]}))
        print("staff_confirmed = true %d · nationality_mention 있음 %d · 입력 자름 %d" % (
            sum(r["result"]["staff_confirmed"] for r in ok), sum(r["result"]["nationality_mention"] is not None
                                                                 for r in ok), sum(r["truncated"] for r in results)))
    secs = [r["secs"] for r in results]
    print("방당 걸린 시간(초) 평균 %.1f · 중앙값 %.1f · 최대 %.1f" % (
        statistics.mean(secs), statistics.median(secs), max(secs)))
    keys = ("input", "output", "cache_write", "cache_read", "cost")
    tot = {k: sum(u.get(k, 0) for r in results for u in r["usage"]) for k in keys}
    calls = sum(len(r["usage"]) for r in results)
    print("호출 %d번 합 — 입력 %d · 출력 %d · 캐시 쓰기 %d · 캐시 읽기 %d 토큰 · 비용 $%.4f" % (
        calls, tot["input"], tot["output"], tot["cache_write"], tot["cache_read"], tot["cost"]))
    per = {k: tot[k] / n for k in keys}
    print("방당 평균 — 입력 %.0f · 출력 %.0f · 캐시 쓰기 %.0f · 캐시 읽기 %.0f 토큰 · 비용 $%.5f" % (
        per["input"], per["output"], per["cache_write"], per["cache_read"], per["cost"]))
    print("%d방 환산 — 입력 %.0f · 출력 %.0f · 캐시 쓰기 %.0f · 캐시 읽기 %.0f 토큰 · 비용 $%.2f · "
          "시간(작업자 수로 나누기 전) %.0f분" % (n_all, per["input"] * n_all, per["output"] * n_all,
                                       per["cache_write"] * n_all, per["cache_read"] * n_all,
                                       per["cost"] * n_all, statistics.mean(secs) * n_all / 60))


if __name__ == "__main__":
    sys.exit(main())
