"""통키 아이디어 문서(idea.md)의 모식도 · 목업 SVG 생성. 와이어프레임 수준(상자 · 글자 · 화살표).

실행: python3 make_svgs.py  → reference/2026-11-12-interpreter-idea/idea-*.svg
예시 문장은 전부 가짜 일반 문장이다(실제 기록 · 실명 없음).
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[4] / "reference" / "2026-11-12-interpreter-idea"
FONT = "AppleGothic, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"

C = {
    "ink": "#222", "sub": "#666", "line": "#999", "bg": "#f4f5f7", "card": "#fff",
    "pri": "#2498bd", "pri_bg": "#e3f3f8", "pur": "#7a5bd6", "pur_bg": "#efeafb",
    "warn": "#d9822b", "warn_bg": "#fdf1e4", "srv": "#eef0f3", "opt": "#c0392b",
    "crm": "#1e7a46", "crm_bg": "#e6f4ec",
}


class Svg:
    def __init__(self, w, h, title):
        self.w, self.h, self.parts = w, h, []
        self.title = title
        self.markers = set()

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill=C["card"], stroke=C["line"], r=8, dash=False, sw=1.2):
        d = ' stroke-dasharray="6 4"' if dash else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=13, fill=C["ink"], anchor="start", weight="normal", rotate=None):
        tr = f' transform="rotate(180 {x} {y - size / 3:.1f})"' if rotate else ""
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
                 f'font-weight="{weight}"{tr}>{escape(s)}</text>')

    def lines(self, x, y, items, size=12, fill=C["ink"], gap=None, anchor="start"):
        gap = gap or size + 5
        for i, s in enumerate(items):
            self.text(x, y + i * gap, s, size, fill, anchor)

    def arrow(self, x1, y1, x2, y2, color=C["ink"], dash=False, both=False, label=None, lx=None, ly=None, lsize=11):
        d = ' stroke-dasharray="5 4"' if dash else ""
        mid = "ah" + color.lstrip("#")
        self.markers.add(color)
        ms = f' marker-start="url(#{mid})"' if both else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.8"{d}'
                 f' marker-end="url(#{mid})"{ms}/>')
        if label:
            self.text(lx if lx is not None else (x1 + x2) / 2, ly if ly is not None else (y1 + y2) / 2 - 6,
                      label, lsize, color, "middle")

    def bubble(self, x, y, w, s, mine, color, size=12, rotate=False):
        h = size + 14
        bx = x + (w * 0.25 if mine else 0)
        bw = w * 0.75
        fill = color if mine else C["bg"]
        tf = "#fff" if mine else C["ink"]
        self.rect(bx, y, bw, h, fill=fill, stroke=fill, r=10)
        self.text(bx + 10, y + h - 9, s, size, tf, rotate=None)

    def phone(self, x, y, w=260, h=520, label=None):
        self.rect(x, y, w, h, fill="#fff", stroke=C["ink"], r=22, sw=2)
        self.rect(x + 10, y + 14, w - 20, h - 28, fill=C["bg"], stroke=C["bg"], r=12)
        if label:
            self.text(x + w / 2, y + h + 22, label, 13, C["sub"], "middle", "bold")

    def save(self, name):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
                f'font-family="{FONT}">\n<title>{escape(self.title)}</title>\n'
                '<defs>' + "".join(
                    f'<marker id="ah{c.lstrip("#")}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                    f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
                    for c in sorted(self.markers)) + '</defs>\n'
                f'<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>\n')
        (OUT / name).write_text(head + "\n".join(self.parts) + "\n</svg>\n", encoding="utf-8")
        return name


def server(s, x, y, w=220, h=96, extra=None):
    s.rect(x, y, w, h, fill=C["srv"], stroke=C["sub"])
    s.text(x + w / 2, y + 24, "통키 서버", 14, C["ink"], "middle", "bold")
    s.lines(x + w / 2, y + 46, extra or ["말 받기 → 받아쓰기 · 번역", "→ 번역 음성 만들기"], 11, C["sub"], anchor="middle")


def legend(s, x, y, items):
    for i, (color, dash, label) in enumerate(items):
        s.arrow(x, y + i * 20, x + 34, y + i * 20, color, dash)
        s.text(x + 44, y + i * 20 + 4, label, 11, C["sub"])


def caption(s, x, y, s_):
    s.text(x, y, s_, 11, C["sub"])


# ───────────────────────── 0 단계 ─────────────────────────
def stage0_diagram():
    s = Svg(900, 420, "0단계 모식도 — 마주 보고 통역(기기 1대)")
    s.text(24, 34, "0 · 지금 — 한 공간에서 마주 보고, 기기 1대", 17, weight="bold")
    s.rect(24, 60, 560, 330, fill="#fafafa", stroke=C["line"], dash=True)
    s.text(40, 84, "상담 공간(예시)", 12, C["sub"])
    # 직원 · 기기 · 고객 — 화살표 라벨이 상자 사이 빈칸에만 들어가게 간격을 둔다
    s.rect(40, 200, 110, 70, fill=C["pri_bg"], stroke=C["pri"])
    s.lines(95, 228, ["직원", "한국어로 말하고 들음"], 11, anchor="middle")
    s.rect(245, 170, 90, 130, fill="#fff", stroke=C["ink"], r=12, sw=2)
    s.lines(290, 205, ["통키", "기기 1대", "(폰·태블릿)", "마이크 1"], 11, anchor="middle")
    s.rect(430, 200, 140, 70, fill=C["pur_bg"], stroke=C["pur"])
    s.lines(500, 228, ["고객", "외국어로 말하고 들음"], 11, anchor="middle")
    s.arrow(152, 222, 243, 222, C["pri"], label="말", ly=214)
    s.arrow(243, 250, 152, 250, C["pri"], True, label="한국어 자막·음성", ly=268, lsize=10)
    s.arrow(428, 222, 337, 222, C["pur"], label="말", ly=214)
    s.arrow(337, 250, 428, 250, C["pur"], True, label="외국어 자막·음성", ly=268, lsize=10)
    s.text(290, 340, "화면 위쪽 절반이 180° 뒤집혀 맞은편 고객이 읽는다", 11, C["sub"], "middle")
    server(s, 640, 80)
    s.arrow(300, 168, 638, 118, C["ink"], label="두 사람의 말(마이크 하나)", lx=470, ly=124)
    s.arrow(638, 150, 337, 182, C["ink"], True, label="자막 + 번역 음성(같은 기기로)", lx=488, ly=190)
    legend(s, 620, 300, [(C["ink"], False, "음성 보냄"), (C["ink"], True, "자막·음성 돌려받음")])
    return s.save("idea-0-diagram.svg")


def stage0_screen():
    s = Svg(800, 620, "0단계 화면 목업 — 지금 통키 통역 화면(코드 main 17c26b5 기준)")
    s.text(24, 30, "0 · 지금 통키 통역 화면 (코드 기준 · 예시 문장은 가짜)", 15, weight="bold")
    x, y = 40, 50
    s.phone(x, y, 300, 540, "통역 화면")
    ix = x + 22
    # 헤더
    s.text(ix + 4, y + 46, "≡  Tongky", 14, C["pri"], weight="bold")
    # 외국어 영역(뒤집힘)
    s.rect(ix, y + 62, 256, 170, fill="#fff", stroke="#ddd", r=10)
    s.add(f'<g transform="rotate(180 {ix + 128} {y + 147})">')
    s.rect(ix + 10, y + 72, 120, 30, fill="#fff", stroke="#ccc", r=6)
    s.text(ix + 20, y + 92, "English ▾", 12)
    s.rect(ix + 206, y + 72, 36, 30, fill="#fff", stroke="#ccc", r=6)
    s.text(ix + 224, y + 92, "⟳", 14, anchor="middle")
    s.bubble(ix + 10, y + 116, 236, "Please let me know if it hurts.", False, C["pri"], 11)
    s.bubble(ix + 10, y + 150, 236, "Okay, I will.", True, C["pur"], 11)
    s.add("</g>")
    # 가운데 줄
    s.text(ix + 128, y + 252, "● Please speak", 11, C["sub"], "middle", rotate=True)
    s.add(f'<circle cx="{ix + 128}" cy="{y + 290}" r="28" fill="{C["pur"]}"/>')
    s.rect(ix + 2, y + 270, 60, 40, fill="#e6e6e6", stroke="#e6e6e6", r=6)
    s.lines(ix + 32, y + 286, ["자동 듣기", "누르고 말하기"], 8, C["ink"], 12, "middle")
    s.text(ix + 128, y + 336, "말씀하세요", 11, C["sub"], "middle")
    # 한국어 영역
    s.rect(ix, y + 350, 256, 160, fill="#fff", stroke="#ddd", r=10)
    s.bubble(ix + 10, y + 362, 236, "아프면 말씀해 주세요.", True, C["pri"], 11)
    s.bubble(ix + 10, y + 396, 236, "네, 그럴게요.", False, C["pri"], 11)
    # 주석
    nx = 380
    notes = [
        ("① 헤더", "햄버거(로그아웃) · 워드마크"),
        ("② 외국어 영역", "기본 180° 뒤집힘 — 맞은편 고객이 읽음"),
        ("", "언어 드롭다운 · 화면 방향 단추 · 말풍선"),
        ("③ 가운데 줄", "원 위 = 고른 언어 안내(뒤집힘)"),
        ("", "원 = 음량 따라 커짐 · 누르면 멈춤"),
        ("", "왼쪽 = 듣기 방식(자동 / 누르고 말하기)"),
        ("", "원 아래 = 한국어 안내 · 멈춤 때 「초기화」"),
        ("", "번역 음성은 이 기기 스피커로"),
        ("④ 한국어 영역", "직원이 읽음 · 내 말 오른쪽 / 상대 말 왼쪽"),
        ("⑤ 시작 전", "화면 전체 언어 단추 — 누르는 것이 시작"),
    ]
    for i, (a, b) in enumerate(notes):
        s.text(nx, 100 + i * 34, a, 13, C["ink"], weight="bold")
        s.text(nx + 110, 100 + i * 34, b, 12, C["sub"])
    s.arrow(370, 95, ix + 200, y + 42, C["line"], dash=True)
    s.arrow(370, 129, ix + 256, y + 140, C["line"], dash=True)
    s.arrow(370, 197, ix + 160, y + 290, C["line"], dash=True)
    s.arrow(370, 367, ix + 256, y + 420, C["line"], dash=True)
    return s.save("idea-0-screen.svg")


# ───────────────────────── 1 단계 ─────────────────────────
def stage1_diagram():
    s = Svg(1100, 480, "1단계 모식도 — 통역 + 원격 통역(QR = 고객 화면)")
    s.text(24, 34, "1단계 — 고객은 방에서 말하고, 직원은 로비에서 듣고 답한다", 17, weight="bold")
    s.rect(24, 70, 320, 330, fill="#fafafa", stroke=C["line"], dash=True)
    s.text(40, 94, "방(예: 상담실 · 시술실 · 대기 공간)", 12, C["sub"])
    s.rect(44, 150, 110, 60, fill=C["pur_bg"], stroke=C["pur"])
    s.lines(99, 175, ["고객", "외국어로 말함"], 12, anchor="middle")
    s.rect(200, 120, 120, 150, fill="#fff", stroke=C["ink"], r=14, sw=2)
    s.lines(260, 150, ["고객 폰", "= 고객 화면", "(QR 로 열림)", "앱 설치 없음"], 11, anchor="middle")
    s.arrow(156, 168, 198, 168, C["pur"])
    s.arrow(198, 192, 156, 192, C["pur"], True)
    s.rect(44, 296, 280, 84, fill="#fff", stroke=C["warn"], dash=True)
    s.lines(58, 320, ["QR — 찍으면 고객 폰이 고객 화면이 된다", "어디에 두나는 선택지(아래 그림)", "A 방에 고정 · B 직원 화면에 그때그때"], 11, C["warn"])
    server(s, 440, 140, 220, 110, ["고객 말 → 한국어로", "직원 말 → 고객 언어로", "음성은 듣는 쪽 기기로"])
    s.rect(756, 70, 320, 330, fill="#fafafa", stroke=C["line"], dash=True)
    s.text(772, 94, "로비 · 데스크", 12, C["sub"])
    s.rect(780, 120, 120, 150, fill="#fff", stroke=C["ink"], r=14, sw=2)
    s.lines(840, 150, ["직원 기기", "= 직원 화면", "(선택지 A / B)"], 11, anchor="middle")
    s.rect(944, 150, 116, 60, fill=C["pri_bg"], stroke=C["pri"])
    s.lines(1002, 175, ["직원", "한국어로 듣고 답함"], 12, anchor="middle")
    s.arrow(942, 168, 902, 168, C["pri"])
    s.arrow(902, 192, 942, 192, C["pri"], True)
    s.rect(780, 296, 280, 84, fill="#fff", stroke=C["line"])
    s.lines(796, 320, ["마주 보고 통역(0단계)도 그대로 —", "직원 기기 하나로 앞에 온 고객과도"], 11, C["sub"])
    s.arrow(322, 170, 438, 170, C["pur"], label="고객 말", ly=162)
    s.arrow(438, 222, 322, 222, C["pur"], True, label="자막 · 음성", ly=242)
    s.arrow(662, 170, 778, 170, C["pri"], True, label="자막 · 음성", ly=162)
    s.arrow(778, 222, 662, 222, C["pri"], label="직원 말", ly=242)
    legend(s, 420, 310, [(C["pur"], False, "고객 쪽(고객 언어)"), (C["pri"], False, "직원 쪽(한국어)"),
                         (C["ink"], True, "점선 = 돌려받는 자막 · 음성")])
    s.text(24, 446, "※ 지금 통키는 한 대화 = 기기 1대 · 마이크 1. 1단계는 한 대화에 기기 2대(고객 폰 + 직원 기기)가 붙는다.", 12, C["sub"])
    return s.save("idea-1-diagram.svg")


def stage1_qr_options():
    s = Svg(940, 360, "1단계 QR 자리 선택지 — A 방에 고정 / B 직원 화면에 띄움")
    s.text(24, 32, "QR 을 어디에 두나 — 선택지 (결정 아님)", 16, weight="bold")
    for i, (title, lines_, foot) in enumerate([
        ("A · 방에 고정 QR", ["방마다 QR 판 하나(예: 벽 · 테이블)", "고객이 찍으면 「그 방」 대화로 들어감", "직원 화면에는 방 이름으로 보임"],
         "이어지는 것: 방 / 끝나는 때: 방을 나갈 때?"),
        ("B · 직원 화면에 그때그때 QR", ["직원이 「원격 시작」을 누르면 QR 이 뜸", "고객이 자기 폰으로 찍고 방으로 이동", "직원 화면에는 고객(대화)으로 보임"],
         "이어지는 것: 고객 / 끝나는 때: 직원이 닫을 때?"),
    ]):
        x = 24 + i * 460
        s.rect(x, 52, 440, 280, fill="#fafafa", stroke=C["warn"], dash=True)
        s.text(x + 16, 80, title, 14, C["warn"], weight="bold")
        s.lines(x + 16, 108, lines_, 12)
        # 그림
        if i == 0:
            s.rect(x + 40, 180, 110, 110, fill="#fff", stroke=C["ink"])
            s.text(x + 95, 240, "▦ QR", 16, anchor="middle")
            s.text(x + 95, 306, "방 벽의 QR 판", 11, C["sub"], "middle")
            s.rect(x + 260, 170, 80, 130, fill="#fff", stroke=C["ink"], r=12, sw=2)
            s.text(x + 300, 240, "고객 폰", 11, anchor="middle")
            s.arrow(x + 258, 235, x + 152, 235, C["pur"], label="찍기", ly=226)
        else:
            s.rect(x + 40, 170, 130, 130, fill="#fff", stroke=C["ink"], r=10, sw=2)
            s.text(x + 105, 200, "직원 화면", 11, anchor="middle")
            s.text(x + 105, 250, "▦ QR", 16, anchor="middle")
            s.rect(x + 280, 170, 80, 130, fill="#fff", stroke=C["ink"], r=12, sw=2)
            s.text(x + 320, 240, "고객 폰", 11, anchor="middle")
            s.arrow(x + 278, 235, x + 172, 235, C["pur"], label="찍기", ly=226)
        s.text(x + 16, 324, foot, 11, C["sub"])
    return s.save("idea-1-qr-options.svg")


def customer_screen(s, x, y, extra_top=None, call=None, help_btn=False):
    """고객 화면(폰) — 고객 언어만 크게. extra_top = 2단계 동선 카드 그리기 함수."""
    s.phone(x, y, 260, 520)
    ix = x + 20
    s.text(ix + 4, y + 44, "Tongky", 13, C["pri"], weight="bold")
    s.text(ix + 216, y + 44, "English ▾", 10, C["sub"], "end")
    top = y + 58
    if extra_top:
        top = extra_top(s, ix, top)
    if call:
        s.rect(ix, top, 220, 46, fill=C["warn_bg"], stroke=C["warn"], r=8)
        s.text(ix + 10, top + 19, "🔔 " + call[0], 11, C["warn"], weight="bold")
        s.text(ix + 10, top + 37, call[1], 10, C["sub"])
        top += 56
    if help_btn:
        s.rect(ix, top, 220, 36, fill="#fff", stroke=C["opt"], r=18, sw=1.6)
        s.text(ix + 110, top + 23, "🙋 Need help (도움 요청)", 11, C["opt"], "middle", "bold")
        top += 46
    h = y + 400 - top
    s.rect(ix, top, 220, h, fill="#fff", stroke="#ddd", r=10)
    s.bubble(ix + 8, top + 10, 204, "Please let me know if it hurts.", False, C["pri"], 10)
    s.bubble(ix + 8, top + 42, 204, "Where is the restroom?", True, C["pur"], 10)
    s.add(f'<circle cx="{ix + 110}" cy="{y + 440}" r="26" fill="{C["pur"]}"/>')
    s.text(ix + 110, y + 486, "● Please speak", 11, C["sub"], "middle")


def stage1_customer():
    s = Svg(700, 640, "1단계 고객 화면 목업(QR) — 입장 · 대화")
    s.text(24, 30, "1단계 · 고객 화면(QR 로 열림) — 예시 문장은 가짜", 15, weight="bold")
    # 입장
    x, y = 40, 60
    s.phone(x, y, 260, 520, "① QR 찍은 직후 — 언어 고르기")
    ix = x + 20
    s.text(ix + 110, y + 70, "Choose your language", 13, anchor="middle", weight="bold")
    for i, l in enumerate(["English", "日本語", "中国 · 简体中文", "臺灣 · 繁體中文", "ไทย", "Tiếng Việt", "廣東話"]):
        r_, c_ = divmod(i, 2)
        w = 220 if i == 6 else 104
        s.rect(ix + c_ * 116, y + 90 + r_ * 62, w, 50, fill="#fff", stroke="#ccc", r=10)
        s.text(ix + c_ * 116 + w / 2, y + 120 + r_ * 62, l, 11, anchor="middle")
    s.text(ix + 110, y + 380, "No app · No sign-up", 11, C["sub"], "middle")
    s.text(ix + 110, y + 400, "(설치 · 가입 없음)", 10, C["sub"], "middle")
    # 대화
    customer_screen(s, 380, 60)
    s.text(510, 604, "② 대화 — 고객 언어 자막만 · 뒤집힘 없음", 13, C["sub"], "middle", "bold")
    return s.save("idea-1-customer.svg")


def stage1_staff_a():
    s = Svg(760, 640, "1단계 직원 화면 선택지 A — 지금 통키 화면 그대로(원격 1건)")
    s.text(24, 30, "1단계 · 직원 화면 선택지 A — 지금 통키 화면 그대로", 15, weight="bold")
    x, y = 40, 60
    s.phone(x, y, 300, 540, "원격으로 연결된 고객 한 명")
    ix = x + 22
    s.text(ix + 4, y + 46, "≡  Tongky", 14, C["pri"], weight="bold")
    s.rect(ix + 120, y + 30, 136, 24, fill=C["warn_bg"], stroke=C["warn"], r=12)
    s.text(ix + 188, y + 47, "원격 · 상담실(예시)", 10, C["warn"], "middle")
    s.rect(ix, y + 62, 256, 170, fill="#fff", stroke="#ddd", r=10)
    s.text(ix + 10, y + 84, "English", 12)
    s.text(ix + 246, y + 84, "선택지: 고객 화면 미러", 10, C["opt"], "end")
    s.bubble(ix + 10, y + 100, 236, "Where is the restroom?", False, C["pur"], 11)
    s.add(f'<circle cx="{ix + 128}" cy="{y + 290}" r="28" fill="{C["pri"]}"/>')
    s.text(ix + 128, y + 336, "말씀하세요 — 고객 폰으로 갑니다", 11, C["sub"], "middle")
    s.rect(ix, y + 350, 256, 160, fill="#fff", stroke="#ddd", r=10)
    s.bubble(ix + 10, y + 362, 236, "화장실이 어디예요?", False, C["pri"], 11)
    s.bubble(ix + 10, y + 396, 236, "복도 끝 왼쪽이에요.", True, C["pri"], 11)
    nx = 380
    s.lines(nx, 110, [
        "· 화면 구성은 0단계와 같다",
        "· 다른 점: 외국어 영역을 뒤집지 않는다",
        "   (고객은 자기 폰으로 보므로)",
        "· 헤더에 「원격 · 어느 방」 표시",
        "· 고객 말 → 한국어 음성이 이 기기에서",
        "· 직원 말 → 고객 언어 음성이 고객 폰에서",
        "",
        "열린 것(선택지):",
        "· 외국어 영역 — 고객 화면 미러(그림) / 없앰",
        "   (한국어 영역만 남김)",
        "· 한 번에 고객 한 명 — 다른 방 고객이 말하면?",
        "   받지 않음 / 알림만 띄움",
    ], 12, C["ink"], 24)
    return s.save("idea-1-staff-a.svg")


def console(s, x, y, w, h, rooms, sel, chat, extra_col=None, title="여러 방 콘솔", target="방으로만"):
    s.rect(x, y, w, h, fill="#fff", stroke=C["ink"], r=10, sw=2)
    s.rect(x, y, w, 36, fill=C["bg"], stroke=C["ink"], r=10, sw=2)
    s.text(x + 14, y + 24, f"≡  Tongky — {title}", 13, C["pri"], weight="bold")
    lw = 250
    s.add(f'<line x1="{x + lw}" y1="{y + 36}" x2="{x + lw}" y2="{y + h}" stroke="#ddd"/>')
    for i, r in enumerate(rooms):
        ry = y + 46 + i * 66
        fill = C["pri_bg"] if i == sel else "#fff"
        s.rect(x + 10, ry, lw - 20, 58, fill=fill, stroke=C["pri"] if i == sel else "#ddd", r=8)
        s.text(x + 22, ry + 22, r[0], 12, weight="bold")
        s.text(x + 22, ry + 42, r[1], 10, C["sub"])
        if r[2]:
            s.rect(x + lw - 80, ry + 10, 60, 20, fill=C["warn_bg"], stroke=C["warn"], r=10)
            s.text(x + lw - 50, ry + 24, r[2], 9, C["warn"], "middle")
        if extra_col:
            extra_col(s, x + 22, ry, r, i)
    cx = x + lw + 16
    cw = w - lw - 32
    s.text(cx, y + 62, rooms[sel][0] + " · " + rooms[sel][1].split(" · ")[0], 13, weight="bold")
    for i, (txt, mine) in enumerate(chat):
        s.bubble(cx, y + 76 + i * 34, cw, txt, mine, C["pri"] if mine else C["pur"], 11)
    s.add(f'<circle cx="{cx + cw / 2}" cy="{y + h - 60}" r="26" fill="{C["pri"]}"/>')
    s.text(cx + cw / 2, y + h - 18, f"말하면 고른 {target} 갑니다(예시)", 11, C["sub"], "middle")
    s.text(cx + cw / 2 + 50, y + h - 56, "말하기 방식: 자동 듣기 / 누르고 말하기 — 선택지", 10, C["opt"], "start")


def stage1_staff_b():
    s = Svg(900, 520, "1단계 직원 화면 선택지 B — 여러 방 콘솔")
    s.text(24, 30, "1단계 · 직원 화면 선택지 B — 여러 방 콘솔(태블릿 · PC)", 15, weight="bold")
    rooms = [("상담실(예시)", "English · 대화 중", ""), ("시술실(예시)", "日本語 · 새 말", "새 말"),
             ("대기 공간(예시)", "中文 · 조용함", "")]
    console(s, 24, 50, 850, 400, rooms, 0, [
        ("화장실이 어디예요? (Where is the restroom?)", False),
        ("복도 끝 왼쪽이에요.", True),
    ])
    s.lines(24, 478, [
        "· 왼쪽 = QR 로 들어온 방(또는 고객) 목록 · 새 말이 오면 표시  · 오른쪽 = 고른 방의 대화(한국어 + 원문 작게)",
        "· 말은 고른 방으로(예시) · 말하기 방식(자동 듣기 / 누르고 말하기)과 다른 방 말을 소리로 · 글로만 띄울지는 열린 것(의료 p11)",
    ], 11, C["sub"], 18)
    return s.save("idea-1-staff-b.svg")


# ───────────────────────── 2 단계 ─────────────────────────
STEPS = ["접수", "상담", "세안", "시술", "진정", "수납"]
STEPS_EN = ["Check-in", "Consult", "Cleanse", "Treatment", "Soothe", "Payment"]  # 고객 화면 = 고객 언어(번역 예시)


def flow_card(s, ix, top, cur=3, w=220):
    s.rect(ix, top, w, 80, fill="#fff", stroke=C["pri"], r=8)
    s.text(ix + 10, top + 18, "Today (오늘 동선 · 번역 예시)", 10, C["pri"], weight="bold")
    step_w = (w - 20) / len(STEPS)
    for i, st in enumerate(STEPS_EN):
        cx = ix + 10 + step_w * i + step_w / 2
        fill = C["pri"] if i < cur else ("#fff" if i > cur else C["warn"])
        s.add(f'<circle cx="{cx}" cy="{top + 36}" r="7" fill="{fill}" stroke="{C["pri"]}"/>')
        s.text(cx, top + 58 + (i % 2) * 12, st, 8, C["ink"] if i == cur else C["sub"], "middle", "bold" if i == cur else "normal")
    return top + 90


def stage2_diagram():
    s = Svg(1100, 560, "2단계 모식도 — 통역 + 원격 통역 + 오늘 동선 안내 · 호출 · CRM 연동")
    s.text(24, 34, "2단계 — 같은 고객 화면에 「오늘 동선」 과 「호출」 이 더해진다 · 병원 CRM 연동 필수", 17, weight="bold")
    s.rect(24, 70, 320, 330, fill="#fafafa", stroke=C["line"], dash=True)
    s.text(40, 94, "고객이 있는 곳(방 · 대기 공간 · 이동 중)", 12, C["sub"])
    s.rect(90, 110, 180, 260, fill="#fff", stroke=C["ink"], r=14, sw=2)
    s.text(180, 136, "고객 폰 = 고객 화면", 11, anchor="middle")
    s.rect(104, 150, 152, 50, fill="#fff", stroke=C["pri"], r=6)
    s.lines(180, 170, ["오늘 동선", "접수 → … → 수납(예시)"], 10, C["pri"], anchor="middle")
    s.rect(104, 210, 152, 36, fill=C["warn_bg"], stroke=C["warn"], r=6)
    s.text(180, 233, "🔔 호출: 다음 방으로", 10, C["warn"], "middle")
    s.rect(104, 256, 152, 100, fill=C["bg"], stroke="#ddd", r=6)
    s.text(180, 310, "통역(1단계 그대로)", 10, C["sub"], "middle")
    server(s, 440, 140, 220, 130, ["통역(1단계)", "+ 고객별 동선 단계", "+ 호출을 고객 언어로", "   글 · 음성으로"])
    s.rect(756, 70, 320, 330, fill="#fafafa", stroke=C["line"], dash=True)
    s.text(772, 94, "로비 · 데스크", 12, C["sub"])
    s.rect(780, 110, 270, 170, fill="#fff", stroke=C["ink"], r=10, sw=2)
    s.lines(796, 136, ["직원 화면(선택지 A / B)", "· 고객별 지금 단계", "· [다음 단계] · [호출]", "· 통역(1단계 화면)"], 11, C["ink"], 22)
    s.arrow(778, 170, 662, 170, C["warn"])
    s.lines(709, 146, ["단계 바꿈", "· 호출"], 10, C["warn"], 12, "middle")
    s.arrow(438, 170, 272, 170, C["warn"])
    s.lines(392, 146, ["동선 · 호출", "(고객 언어)"], 10, C["warn"], 12, "middle")
    s.arrow(272, 300, 438, 240, C["pur"], True, both=True)
    s.lines(398, 288, ["통역", "(1단계)"], 10, C["pur"], 12, "middle")
    s.arrow(662, 240, 778, 240, C["pri"], True, both=True)
    s.lines(709, 260, ["통역", "(1단계)"], 10, C["pri"], 12, "middle")
    s.rect(440, 340, 220, 76, fill=C["crm_bg"], stroke=C["crm"], sw=1.6)
    s.text(550, 366, "병원 CRM (연동 필수)", 13, C["crm"], "middle", "bold")
    s.lines(550, 388, ["예약 · 접수 · 시술 진행"], 11, C["sub"], anchor="middle")
    s.arrow(550, 338, 550, 272, C["crm"])
    s.lines(612, 300, ["고객별 오늘 동선", "· 지금 단계"], 10, C["crm"], 12, "start")
    legend(s, 780, 300, [(C["warn"], False, "동선 · 호출"), (C["pur"], True, "고객 쪽 통역"), (C["pri"], True, "직원 쪽 통역"), (C["crm"], False, "CRM → 동선")])
    s.text(24, 526, "※ 동선 단계는 일반적인 피부과 흐름 예시(특정 병원 흐름 아님). 고객별 동선은 병원 CRM 에서 받아온다 — 어느 CRM · 어떤 값인지는 열린 것.", 12, C["sub"])
    return s.save("idea-2-diagram.svg")


def stage2_customer():
    s = Svg(720, 650, "2단계 고객 화면 선택지 — A 한 화면 위아래 / B 탭 나눔")
    s.text(24, 30, "2단계 · 고객 화면 선택지 — 예시 문장 · 동선은 가짜", 15, weight="bold")
    customer_screen(s, 40, 60, extra_top=lambda sv, ix, top: flow_card(sv, ix, top),
                    call=("Please come to the treatment room.", "(시술실로 와 주세요)"))
    s.text(170, 604, "A · 한 화면 — 위 동선 · 호출 / 아래 통역", 13, C["sub"], "middle", "bold")
    # B 탭
    x, y = 400, 60
    s.phone(x, y, 260, 520)
    ix = x + 20
    s.text(ix + 4, y + 44, "Tongky", 13, C["pri"], weight="bold")
    s.rect(ix, y + 56, 110, 32, fill=C["pri"], stroke=C["pri"], r=6)
    s.text(ix + 55, y + 77, "Today", 12, "#fff", "middle", "bold")
    s.rect(ix + 110, y + 56, 110, 32, fill="#fff", stroke=C["pri"], r=6)
    s.text(ix + 165, y + 77, "Interpret", 12, C["pri"], "middle")
    for i, st in enumerate(STEPS_EN):
        ry = y + 100 + i * 52
        cur = i == 3
        fill = C["warn_bg"] if cur else "#fff"
        s.rect(ix, ry, 220, 44, fill=fill, stroke=C["warn"] if cur else "#ddd", r=8)
        mark = "✓" if i < 3 else ("▶" if cur else "·")
        s.text(ix + 14, ry + 28, f"{mark}  {st}", 12, C["ink"], weight="bold" if cur else "normal")
        if cur:
            s.text(ix + 206, ry + 28, "Now", 10, C["warn"], "end", "bold")
    s.rect(ix, y + 420, 220, 46, fill=C["warn_bg"], stroke=C["warn"], r=8)
    s.text(ix + 10, y + 448, "🔔 Please come to the treatment room.", 10, C["warn"])
    s.text(530, 604, "B · 탭 — 「오늘」 / 「통역」", 13, C["sub"], "middle", "bold")
    s.text(24, 630, "※ 단계 이름은 고객 언어로 보인다(그림은 English 번역 예시 · 단계 자체도 일반 피부과 흐름 예시)", 11, C["sub"])
    return s.save("idea-2-customer.svg")


def stage2_call_direction():
    s = Svg(900, 660, "2단계 호출 방향 선택지 — 직원 → 고객만 / 고객 → 직원 도움 요청도")
    s.text(24, 30, "2단계 · 호출 방향 — 선택지 (결정 아님 · 예시 문장은 가짜)", 15, weight="bold")
    call = ("Please come to the treatment room.", "(시술실로 와 주세요)")
    customer_screen(s, 40, 60, call=call)
    s.text(170, 604, "A · 직원 → 고객만", 13, C["sub"], "middle", "bold")
    s.text(170, 624, "고객 화면에는 받은 호출만", 11, C["sub"], "middle")
    customer_screen(s, 400, 60, call=call, help_btn=True)
    s.text(530, 604, "B · 고객 → 직원 「도움 요청」도", 13, C["sub"], "middle", "bold")
    s.text(530, 624, "고객이 누르면 직원 화면에 알림", 11, C["sub"], "middle")
    s.rect(720, 150, 160, 90, fill="#fff", stroke=C["ink"], r=10, sw=2)
    s.lines(800, 176, ["직원 화면", "🙋 고객 1(예시)", "도움 요청"], 11, C["opt"], 18, "middle")
    s.arrow(642, 190, 718, 190, C["opt"])
    return s.save("idea-2-call-direction.svg")


def stage2_staff_a():
    s = Svg(900, 520, "2단계 직원 화면 선택지 A — 콘솔에 동선 · 호출 더하기")
    s.text(24, 30, "2단계 · 직원 화면 선택지 A — 1단계 콘솔에 동선 · 호출을 더함", 15, weight="bold")
    rooms = [("고객 1(예시)", "English · 지금: 시술", ""), ("고객 2(예시)", "日本語 · 지금: 상담", "새 말"),
             ("고객 3(예시)", "中文 · 지금: 진정", "")]

    def col(sv, x, ry, r, i):
        pass

    console(s, 24, 50, 850, 400, rooms, 0, [
        ("오늘 동선 : 접수 ✓ 상담 ✓ 세안 ✓ ▶시술 · 진정 · 수납", True),
    ], title="콘솔 + 동선", target="고객에게만")
    bx = 24 + 266
    for j, lab in enumerate(["다음 단계 ▶", "🔔 호출 보내기"]):
        s.rect(bx + j * 150, 160, 136, 34, fill=C["warn_bg"] if j else "#fff", stroke=C["warn"], r=8)
        s.text(bx + j * 150 + 68, 182, lab, 12, C["warn"], "middle", "bold")
    s.rect(bx, 206, 560, 64, fill="#fff", stroke="#ddd", r=8)
    s.text(bx + 10, 226, "호출 문구 — 선택지: ① 정해 둔 문구 고르기 / ② 직원이 말로", 11, C["sub"])
    s.text(bx + 10, 252, "예: 「시술실로 와 주세요」 → 고객 언어 글 + 음성", 11, C["ink"])
    s.lines(24, 478, ["· 왼쪽 목록에 고객마다 「지금 단계」가 붙는다 · [다음 단계] 를 누르면 고객 화면 동선이 한 칸 움직인다",
                      "· 호출이 뜨는 자리는 고객 화면 선택지를 따른다(A 위 배너 / B 「오늘」 탭) · 알림 방식(글 + 음성 / 글 + 진동 / 글만)은 열린 것"], 11, C["sub"], 18)
    return s.save("idea-2-staff-a.svg")


def stage2_staff_b():
    s = Svg(900, 460, "2단계 직원 화면 선택지 B — 동선 보드(단계별 칸)")
    s.text(24, 30, "2단계 · 직원 화면 선택지 B — 동선 보드(단계별 칸에 고객 카드)", 15, weight="bold")
    s.rect(24, 50, 850, 360, fill="#fff", stroke=C["ink"], r=10, sw=2)
    cw = 850 / len(STEPS)
    cards = {1: ["고객 2 · 日本語"], 3: ["고객 1 · English"], 4: ["고객 3 · 中文"]}
    for i, st in enumerate(STEPS):
        x = 24 + i * cw
        s.rect(x + 6, 60, cw - 12, 340, fill=C["bg"], stroke=C["bg"], r=8)
        s.text(x + cw / 2, 84, st + "(예시)", 12, weight="bold", anchor="middle")
        for j, c_ in enumerate(cards.get(i, [])):
            s.rect(x + 14, 100 + j * 90, cw - 28, 80, fill="#fff", stroke=C["pri"], r=8)
            s.text(x + 22, 122 + j * 90, c_, 10, weight="bold")
            s.text(x + 22, 144 + j * 90, "💬 통역 열기", 10, C["pri"])
            s.text(x + 22, 164 + j * 90, "🔔 호출 · ▶ 옮기기", 10, C["warn"])
    s.text(24, 436, "· 카드를 다음 칸으로 옮기면 고객 화면 동선이 바뀐다 · 카드에서 통역을 열면 1단계 화면(A 또는 B)", 11, C["sub"])
    return s.save("idea-2-staff-b.svg")


if __name__ == "__main__":
    names = [stage0_diagram(), stage0_screen(), stage1_diagram(), stage1_qr_options(), stage1_customer(),
             stage1_staff_a(), stage1_staff_b(), stage2_diagram(), stage2_customer(), stage2_call_direction(), stage2_staff_a(), stage2_staff_b()]
    print("\n".join(names))
