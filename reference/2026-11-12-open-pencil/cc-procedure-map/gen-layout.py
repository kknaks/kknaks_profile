#!/usr/bin/env python3
"""screens.json · notes.json → layout.json (섹션 영역 · 화면 슬롯 · 메모 슬롯 좌표).
화면 슬롯 크기 = SIZE 표(섹션 스크립트는 이 크기 안에 화면을 짓는다). 메모 슬롯 높이 = 메모 글 길이로 넉넉히 셈.
좌표: 섹션은 페이지 기준, 슬롯은 섹션 프레임 기준. 다시 돌리면 같은 결과."""
import json, math, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open("screens.json")); N = json.load(open("notes.json"))
SIZE = {  # screenId: (w, h) — 시안 크기(방 카드 256×448 · 팝오버 240 · 차트 모달 410 …)에 맞춘 화면 슬롯
 "procedure/board": (1440, 900), "procedure/board/out-of-hours": (1000, 360),
 "procedure/room-slot": (560, 500), "procedure/room-slot/occupied": (280, 470),
 "procedure/customer-card": (300, 560),
 "procedure/customer-card/status-waiting": (280, 470), "procedure/customer-card/status-in-progress": (280, 470),
 "procedure/customer-card/status-discharge-wait": (280, 470), "procedure/customer-card/order-memo": (280, 280),
 "procedure/treatment-line/waiting": (280, 200), "procedure/treatment-line/not-proceeding": (280, 200),
 "procedure/treatment-line/done": (280, 200), "procedure/customer-card/line-changed": (280, 470),
 "procedure/customer-card/new-lines": (280, 470), "procedure/customer-card/call-bar": (280, 470),
 "procedure/chart/change-history": (320, 200),
 "procedure/search": (520, 120), "procedure/search/results": (520, 360), "procedure/search/empty": (520, 200),
 "procedure/customer-card/confirm-flag": (280, 470), "procedure/confirm-needed": (300, 700),
 "procedure/confirm-needed/card": (300, 780), "procedure/toast/alert": (420, 100),
 "procedure/room-move/menu": (240, 200), "procedure/room-move/list": (240, 320),
 "procedure/room-move/list-empty": (240, 160), "procedure/toast/room-full": (420, 100),
 "procedure/customer-card/anesthesia-idle": (280, 140), "procedure/customer-card/anesthesia-running": (280, 140),
 "procedure/treatment-line/calling": (280, 200), "procedure/doctor-list/designate-call": (260, 380),
 "procedure/treatment-line/accepted": (280, 160), "procedure/doctor-list/reassign": (260, 320),
 "procedure/treatment-line/in-progress": (280, 160), "procedure/doctor-list/start-pick": (260, 320),
 "procedure/treatment-line/more-menu": (240, 140), "procedure/confirm/cancel-start": (320, 200),
 "procedure/confirm/cancel-complete": (320, 200),
 "procedure/chart": (600, 1100), "procedure/chart/order-memo": (560, 240), "procedure/chart/doctor-chart": (560, 280),
 "procedure/chart/nursing-chart": (560, 340), "procedure/chart/author-picker": (260, 320),
 "procedure/chart/apply-all-confirm": (320, 200), "procedure/chart/discard-confirm": (320, 200),
 "procedure/chart/conflict-notice": (560, 120), "procedure/chart/past-visits": (560, 320),
 "procedure/customer-card/more-menu": (240, 120),
 "procedure/room-log": (600, 780), "procedure/room-log/date-calendar": (320, 380),
 "procedure/room-log/room-select": (260, 340), "procedure/room-log/room-group": (560, 440),
 "procedure/consultant-call": (280, 200),
 "mobile/call-accept": (375, 420), "mobile/toast/taken": (375, 120), "mobile/toast/canceled": (375, 120),
}
SECTIONS = [  # 캔버스 섹션 = 기획안 절(1~7) + CC 모바일(참고, 가장자리)
 ("1", "1. 시술 현황 보기", ["1-1", "1-2", "1-3"]), ("2", "2. 시술 준비", ["2-1", "2-2"]),
 ("3", "3. 호출", ["3-1", "3-2"]), ("4", "4. 시술 진행", ["4-1", "4-2"]), ("5", "5. 귀가 대기", ["5-1"]),
 ("6", "6. 관리실 기록 보기", ["6-1"]), ("7", "7. 고도화", ["7-1"]), ("M", "CC 모바일(참고)", ["M"]),
]
NOTE_W, CAP_H, GAP_X, GAP_Y, PAD, TITLE_H, MAX_ROW_W = 360, 36, 160, 160, 80, 120, 4400

def note_h(body):
    lines = sum(max(1, math.ceil(len(p) / 24)) for p in body.split("\n"))
    return 12 * 2 + 20 + 6 + lines * 16 + 6 + 14 + 8   # 여백 · 머리 · 본문 · 출처 · 여유

out = {"page": "시술현황 맵", "noteWidth": NOTE_W, "captionHeight": CAP_H, "sections": []}
y0, maxw = 0, 0
for key, title, subs in SECTIONS:
    units = [s for sub in subs for s in S if s["section"] == sub]
    rows, row, roww = [], [], 0
    for s in units:
        w, h = SIZE[s["screenId"]]
        ns = [n for n in N if n["screenId"] == s["screenId"]]
        nh = sum(note_h(n["body"]) for n in ns) + 8 * max(0, len(ns) - 1)
        uw = w + 32 + NOTE_W
        uh = CAP_H + max(h, nh)
        if row and roww + GAP_X + uw > MAX_ROW_W: rows.append(row); row, roww = [], 0
        row.append((s, w, h, uw, uh, nh)); roww += (GAP_X if roww else 0) + uw
    if row: rows.append(row)
    slots, y, secw = [], PAD + TITLE_H, 0
    for r in rows:
        x = PAD
        for s, w, h, uw, uh, nh in r:
            slots.append({"screenId": s["screenId"], "sub": s["section"],
                          "caption": {"x": x, "y": y},
                          "screen": {"x": x, "y": y + CAP_H, "w": w, "h": h},
                          "notes": {"x": x + w + 32, "y": y + CAP_H, "w": NOTE_W, "h": nh}})
            x += uw + GAP_X
        secw = max(secw, x - GAP_X + PAD)
        y += max(u[4] for u in r) + GAP_Y
    sech = y - GAP_Y + PAD
    out["sections"].append({"key": key, "title": title, "subs": subs, "x": 0, "y": y0, "w": secw, "h": sech, "slots": slots})
    if key != "M": y0 += sech + 400; maxw = max(maxw, secw)
for s in out["sections"]:
    if s["key"] == "M": s["x"], s["y"] = maxw + 800, 0   # 가장자리
json.dump(out, open("layout.json", "w"), ensure_ascii=False, indent=1)
print({s["key"]: (s["x"], s["y"], s["w"], s["h"], len(s["slots"])) for s in out["sections"]})
