"""통키 요금제 설계 2판 — 적정 케이스 기준. 계산 · 그래프 · 보고서 생성(손 편집 금지).

입력(읽기만): ../pricing-calc/usage-logs-cost-probe-2026-11-12.json · ../pricing-calc/context-chars.json
출력: reference/2026-11-12-interpreter-idea/pricing-design.md · pd2-*.png · (같은 폴더) results.json

사용자가 고칠 곳은 아래 「적정 케이스」 블록 하나다. 고치고 `python3 calc2.py` 를 다시 돌리면
보고서 · 그래프 전체가 다시 나온다.
"""

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SRC = HERE.parent / "pricing-calc"
OUT = ROOT / "reference" / "2026-11-12-interpreter-idea"
REPORT = OUT / "pricing-design.md"

# ══ 적정 케이스 〔가정 — 사용자 승인〕 — 이 블록만 고치면 결론이 바뀐다 ══
BASE = {
    "H": 4.0,     # 하루 실사용 시간(h / 일 · 기기 1대)
    "D": 2.0,     # 동시 사용 대수(대)
    "rho": 0.5,   # 상담 비율(시간 기준 · 0 ~ 1)
    "kc": 2.0,    # 상담 1시간의 세션 수(회 / h)
    "nc": 22.0,   # 상담 1시간의 발화 수(개 / h)
    "ks": 10.0,   # 간단 통역 1시간의 세션 수(회 / h)
    "ns": 85.0,   # 간단 통역 1시간의 발화 수(개 / h)
}
RANGE_USER = {"H": (1, 12), "D": (1, 5), "rho": (0, 1), "nc_max": 44, "ns_max": 170}  # 사용자 지정 범위
DAYS = 30            # 한 달(일) — 사용자 지정
SILENCE_S = 60       # 무발화 1분 자동 종료(초) — 사용자 지정 정책. 수동 stop 은 넣지 않는다
FX = 1400            # 환율(원 / USD) — 가정
M_BASE = 0.50        # 마진율 기준 — 가정(사용자 미정)
MARGINS = (0.30, 0.50, 0.70)
REF_KRW = 20000      # 대표 투표 「월 2만원」 — 참고선
STREAM_FULL_HOUR = True  # 「실사용 1시간 = 스트림이 열린 1시간」 가정(미승인). False 면 하한(발화 연결 + 세션당 60초)
ROUND_HOUR, ROUND_TOK, ROUND_FLAT = 100, 100, 10000  # 가격 올림 단위(원) — 가정

# ══ 공식 단가(USD / 토큰) — https://soniox.com/pricing ══
PRICING_URL = "https://soniox.com/pricing"
URL_KEEPALIVE = "https://docs.soniox.com/stt/rt/connection-keepalive"
URL_CONTEXT = "https://docs.soniox.com/stt/concepts/context"
URL_MODELS = "https://docs.soniox.com/stt/models"
P_AIN, P_TIN, P_TOUT, P_TTSIN, P_AOUT = 2.00e-6, 4.00e-6, 4.00e-6, 4.00e-6, 21.50e-6
AUDIO_TOK_PER_H = 30000
A_RATE = AUDIO_TOK_PER_H / 3600

# ══ 실측 2건 ══
logs = json.loads((SRC / "usage-logs-cost-probe-2026-11-12.json").read_text())["items"]
ctx = json.loads((SRC / "context-chars.json").read_text())


def pick(ref, model):
    rows = [x for x in logs if x["client_reference_id"] == ref and x["model"] == model]
    assert len(rows) == 1, (ref, model)
    return rows[0]


CASES = {
    "c": {"name": "상담 1발화", "ref": "cost-probe-2026-11-12-d", "pair": "ko→zh", "lang": "zh"},
    "s": {"name": "간단 통역 1발화", "ref": "cost-probe-2026-11-12-real", "pair": "ko→en", "lang": "en"},
}
for c in CASES.values():
    stt, tts = pick(c["ref"], "stt-rt-v5"), pick(c["ref"], "tts-rt-v2")
    c["ctx_tok"], c["a_in"], c["t_out"] = stt["input_text_tokens"], stt["input_audio_tokens"], stt["output_text_tokens"]
    c["t_tts"], c["a_tts"] = tts["input_text_tokens"], tts["output_audio_tokens"]
    c["d"] = stt["input_audio_duration_ms"] / 1000
    c["cost_log"] = float(stt["cost_usd"]) + float(tts["cost_usd"])
    c["cost_fn"] = (P_AIN * c["a_in"] + P_TIN * c["ctx_tok"] + P_TOUT * c["t_out"]
                    + P_TTSIN * c["t_tts"] + P_AOUT * c["a_tts"])
    c["tpc"] = c["ctx_tok"] / ctx["langs"][c["lang"]]["chars"]
    c["e"] = P_TOUT * c["t_out"] + P_TTSIN * c["t_tts"] + P_AOUT * c["a_tts"]  # 발화 변동비(오디오 입력 제외)
    c["e_tok"] = c["t_out"] + c["t_tts"] + c["a_tts"]
    c["e_aud"] = c["e"] + P_AIN * c["a_in"]  # 코디 방식 대조용(오디오 입력 포함)
C, S = CASES["c"], CASES["s"]
MAX_LANG = max(ctx["langs"], key=lambda l: ctx["langs"][l]["chars"])
MAX_CHARS = ctx["langs"][MAX_LANG]["chars"]
CTX_TOK = round(MAX_CHARS * max(C["tpc"], S["tpc"]))
CTX_USD = CTX_TOK * P_TIN
A_USD_H = AUDIO_TOK_PER_H * P_AIN


# ══ 원가 함수 ══
def stream_s(case, k, n, mode):
    """실사용 1시간 중 스트림이 열린 초. full=1시간 내내 · low=발화 연결 + 세션당 60초 꼬리 · talk=발화 연결만(코디 방식)."""
    if mode == "full":
        return 3600.0
    if mode == "low":
        return min(3600.0, n * case["d"] + k * SILENCE_S)
    return n * case["d"]


def hour_cost(case, k, n, mode=None):
    """한 종류(상담 또는 간단)로 쓴 기기 1대 · 실사용 1시간의 원가(USD)와 토큰 수."""
    mode = mode or ("full" if STREAM_FULL_HOUR else "low")
    sec = stream_s(case, k, n, mode)
    aud_tok = A_RATE * sec
    cost = P_AIN * aud_tok + k * CTX_USD + n * case["e"]
    tok = aud_tok + k * CTX_TOK + n * case["e_tok"]
    return {"cost": cost, "tok": tok, "aud": P_AIN * aud_tok, "fix": k * CTX_USD, "var": n * case["e"], "sec": sec}


def month(v, mode=None):
    hc, hs = hour_cost(C, v["kc"], v["nc"], mode), hour_cost(S, v["ks"], v["ns"], mode)
    hours = DAYS * v["D"] * v["H"]
    mix = v["rho"] * hc["cost"] + (1 - v["rho"]) * hs["cost"]
    mixtok = v["rho"] * hc["tok"] + (1 - v["rho"]) * hs["tok"]
    return {"v": v, "hc": hc, "hs": hs, "hours": hours, "mix": mix, "mixtok": mixtok,
            "M": mix * hours * FX, "TOK": mixtok * hours}  # M = 월 원가(원)


B = month(BASE)


def ceil_to(x, unit):
    return math.ceil(x / unit - 1e-9) * unit


PLANS = {"hour": "시간제", "tok": "토큰제", "flat": "정액제"}


def prices(m):
    return {
        "hour": ceil_to(B["mix"] * FX / (1 - m), ROUND_HOUR),                    # 원 / 기기·시간
        "tok": ceil_to(B["mix"] / B["mixtok"] * 1e6 * FX / (1 - m), ROUND_TOK),  # 원 / 100만 토큰
        "flat": ceil_to(B["M"] / (1 - m), ROUND_FLAT),                           # 원 / 계정·월
    }


def raw_prices(m):
    return {"hour": B["mix"] * FX / (1 - m), "tok": B["mix"] / B["mixtok"] * 1e6 * FX / (1 - m), "flat": B["M"] / (1 - m)}


PR = {m: prices(m) for m in MARGINS}
P = PR[M_BASE]


def revenue(plan, r, p=None):
    p = p or P
    if plan == "hour":
        return p["hour"] * r["hours"]
    if plan == "tok":
        return p["tok"] * r["TOK"] / 1e6
    return p["flat"]


def margin(plan, r, p=None):
    rv = revenue(plan, r, p)
    return (rv - r["M"]) / rv


# ══ 민감도 — 변인 1개만 움직인다 ══
KS_MAX = (3600 - BASE["ns"] * S["d"]) / SILENCE_S   # 간단: 세션마다 60초 꼬리가 들어갈 자리
KC_MAX = min(BASE["nc"], (3600 - BASE["nc"] * C["d"]) / SILENCE_S)
NC_FEAS = 3600 / C["d"]   # 실측 연결 시간으로 1시간에 들어가는 상담 발화 최대
NS_FEAS = 3600 / S["d"]
VARS = {
    "H": {"name": "하루 실사용 시간", "unit": "h", "lo": RANGE_USER["H"][0], "hi": RANGE_USER["H"][1], "tag": "〔사용자 지정〕 범위"},
    "D": {"name": "동시 사용 대수", "unit": "대", "lo": RANGE_USER["D"][0], "hi": RANGE_USER["D"][1], "tag": "〔사용자 지정〕 범위"},
    "rho": {"name": "상담 비율", "unit": "%", "lo": RANGE_USER["rho"][0], "hi": RANGE_USER["rho"][1], "scale": 100, "tag": "〔사용자 지정〕 범위"},
    "kc": {"name": "상담 1시간의 세션 수", "unit": "회", "lo": 1, "hi": KC_MAX,
           "tag": "〔사용자 지정〕 1 ~ 최대 · 최대 〔계산〕 = 발화 수(세션은 발화보다 많을 수 없다)"},
    "nc": {"name": "상담 1시간의 발화 수", "unit": "개", "lo": BASE["kc"], "hi": RANGE_USER["nc_max"],
           "tag": "〔사용자 지정〕 ~ 44개 · 아래 끝 〔계산〕 = 세션 수"},
    "ks": {"name": "간단 통역 1시간의 세션 수", "unit": "회", "lo": 1, "hi": KS_MAX,
           "tag": "〔사용자 지정〕 1 ~ 최대 · 최대 〔계산〕 = (3,600초 − 발화 연결 시간) ÷ 60초"},
    "ns": {"name": "간단 통역 1시간의 발화 수", "unit": "개", "lo": BASE["ks"], "hi": RANGE_USER["ns_max"],
           "tag": "〔사용자 지정〕 ~ 170개 · 아래 끝 〔계산〕 = 세션 수"},
}
N_SWEEP = 400
for vk, V in VARS.items():
    sc = V.get("scale", 1)
    xs = [V["lo"] + (V["hi"] - V["lo"]) * i / N_SWEEP for i in range(N_SWEEP + 1)]
    V["rows"] = [(x, month({**BASE, vk: x})) for x in xs]
    V["r_lo"], V["r_hi"] = V["rows"][0][1], V["rows"][-1][1]
    V["cross"] = {}
    for plan in PLANS:
        f = [(x, revenue(plan, r) - r["M"]) for x, r in V["rows"]]
        cr = None
        for (x0, f0), (x1, f1) in zip(f, f[1:]):
            if f0 >= 0 > f1 or f0 < 0 <= f1:
                xc = x0 + (x1 - x0) * f0 / (f0 - f1)
                cr = (xc, "위" if f1 < 0 else "아래")
                break
        V["cross"][plan] = cr
        V.setdefault("minm", {})[plan] = min(margin(plan, r) for _, r in V["rows"])


# 동시 사용 대수는 정수다 — 정수 점에서만 흑자 · 적자를 가른다(W4)
VD = VARS["D"]
VD["int_rows"] = [(float(d), month({**BASE, "D": float(d)})) for d in range(int(VD["lo"]), int(VD["hi"]) + 1)]
VD["int_ok"], VD["int_bad"] = {}, {}
for plan in PLANS:
    bad = [x for x, r in VD["int_rows"] if revenue(plan, r) < r["M"]]
    if bad:
        VD["int_bad"][plan] = min(bad)
        VD["int_ok"][plan] = min(bad) - 1
BEST = "tok"  # 추천안 — 아래 assert 가 근거 숫자를 지킨다


# ══ 표기 ══
def won(x):
    return f"{x:,.0f}원"


def won1(x):
    return f"{x:,.1f}원"


def man(x):
    return f"{x / 10000:,.1f}만원"


def pct(x):
    return f"{x * 100:+.1f}%" if x < 0 else f"{x * 100:.1f}%"


def xfmt(vk, x):
    V = VARS[vk]
    x = x * V.get("scale", 1)
    return f"{x:,.1f}{V['unit']}" if abs(x - round(x)) > 1e-6 else f"{x:,.0f}{V['unit']}"


def cross_txt(vk, plan):
    cr = VARS[vk]["cross"][plan]
    if vk == "D" and cr is not None:
        ok, bad = VD["int_ok"][plan], VD["int_bad"][plan]
        return (f"**{ok:g}대까지 흑자(마진 {pct(margin(plan, month({**BASE, 'D': ok})))}) · "
                f"{bad:g}대부터 적자({pct(margin(plan, month({**BASE, 'D': bad})))})**")
    if cr is None:
        return f"범위 안 적자 없음(마진 최저 {pct(VARS[vk]['minm'][plan])})"
    return f"**{xfmt(vk, cr[0])} {'초과' if cr[1] == '위' else '미만'}에서 적자**"


# ══ 그래프 — 변인별 「월 원가 vs 각 요금제 월 매출」 ══
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
PCOL = {"hour": "#2a78d6", "tok": "#eb6834", "flat": "#1baf7a"}
PSTY = {"hour": "-", "tok": "--", "flat": "-."}
PMARK = {"hour": "o", "tok": "^", "flat": "s"}
POFF = {"hour": 0, "tok": 17, "flat": 33}  # 표지를 엇갈려 찍어 선이 겹쳐도 셋이 다 보이게
PLW = {"hour": 1.8, "tok": 2.6, "flat": 1.8}
DMS = {"hour": 15, "tok": 7, "flat": 7}  # 동시 사용 대수 그래프는 정수 대수에만 표지를 찍는다 — 큰 빈 원 ○ 안에 △ 가 보이게
pngs = []


def overlap_pairs(vk):
    """월 매출 선이 그래프에서 겹쳐 보이는 요금제 쌍(차이가 세로축 높이의 3% 미만)."""
    V = VARS[vk]
    top = max(max(r["M"] for _, r in V["rows"]), max(revenue(pl, r) for pl in PLANS for _, r in V["rows"]))
    out = []
    for a, b in (("hour", "tok"), ("hour", "flat"), ("tok", "flat")):
        if max(abs(revenue(a, r) - revenue(b, r)) for _, r in V["rows"]) < 0.03 * top:
            out.append((a, b))
    return out


def fig_var(vk):
    V = VARS[vk]
    sc = V.get("scale", 1)
    rows = V["int_rows"] if vk == "D" else V["rows"]
    xs = [x * sc for x, _ in rows]
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    fig.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    every = 1 if vk == "D" else None
    ax.plot(xs, [r["M"] / 1e4 for _, r in rows], "-", color=INK, lw=2.8, label="월 원가(Soniox)", zorder=2,
            marker="D" if vk == "D" else None, ms=5)
    for z, (plan, pname) in enumerate(PLANS.items()):
        unit = {"hour": f"기기·시간당 {P['hour']:,}원", "tok": f"100만 토큰당 {P['tok']:,}원", "flat": f"월 {P['flat']:,}원 · 초과 청구 없음"}[plan]
        ax.plot(xs, [revenue(plan, r) / 1e4 for _, r in rows], PSTY[plan], color=PCOL[plan], lw=PLW[plan], zorder=3 + z,
                marker=PMARK[plan], ms=(DMS[plan] if vk == "D" else 8 if plan == "hour" else 6), mfc="#fcfcfb" if plan == "hour" else PCOL[plan], mec=PCOL[plan], mew=1.6,
                markevery=every or (POFF[plan], 50), label=f"{pname} 월 매출({unit})" + (" — 추천" if plan == BEST else ""))
        cr = V["cross"][plan]
        if cr and vk == "D":
            x_ok, x_bad = V["int_ok"][plan], V["int_bad"][plan]
            r_bad = month({**BASE, vk: x_bad})
            ax.annotate(f"{pname}: {x_ok:g}대까지 흑자 · {x_bad:g}대부터 적자", (x_bad, r_bad["M"] / 1e4), textcoords="offset points",
                        xytext=(-190, 14), fontsize=9, color=INK, arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.8})
        elif cr:
            yc = month({**BASE, vk: cr[0]})["M"] / 1e4
            ax.plot([cr[0] * sc], [yc], "X", ms=11, mfc=INK, mec="#fcfcfb", mew=1.2, zorder=9)
            ax.annotate(f"{pname} 적자 전환\n{xfmt(vk, cr[0])}", (cr[0] * sc, yc), textcoords="offset points",
                        xytext=(8, -28), fontsize=9, color=INK)
    bx = BASE[vk] * sc
    ax.axvline(bx, color=MUTED, lw=1, ls=":", zorder=1)
    ax.annotate(f"적정 케이스 {xfmt(vk, BASE[vk])}", (bx, 1), xycoords=("data", "axes fraction"), textcoords="offset points",
                xytext=(4, -12), fontsize=9, color=MUTED)
    ov = overlap_pairs(vk)
    if ov:
        ax.annotate("겹치는 선: " + " · ".join(f"{PLANS[a]} = {PLANS[b]}" for a, b in ov) + (" (같은 점에 겹친다 — 큰 빈 원 ○ 안에 △)" if vk == "D" else " (표지 ○ △ □ 로 구분)"), (0.99, 0.02),
                    xycoords="axes fraction", ha="right", fontsize=8.5, color=MUTED)
    ax.set_xlabel(f"{V['name']} ({V['unit']}) — 나머지 변인은 적정 케이스 고정", color=INK)
    ax.set_ylabel("월 금액 (만원 · 계정 하나 · 환율 1,400원/USD 가정)", color=INK)
    ax.set_title(f"{V['name']}만 움직일 때 — 월 원가 vs 요금제별 월 매출 (마진율 {M_BASE * 100:.0f}% 가격 그대로)", fontsize=11, color=INK, loc="left")
    ax.set_ylim(bottom=0)
    ax.set_xlim(min(xs) - (0.15 if vk == "D" else 0), max(xs) + (0.15 if vk == "D" else 0))
    if vk == "D":
        ax.set_xticks(xs)
    ax.grid(True, color=GRID, lw=0.8)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    for s_ in ("left", "bottom"):
        ax.spines[s_].set_color(GRID)
    ax.tick_params(colors=MUTED)
    ax.legend(fontsize=9, frameon=False, loc="upper left", bbox_to_anchor=(0.0, 0.95) if vk in ("H", "D") else None)
    fig.tight_layout()
    name = f"pd2-{vk}.png"
    fig.savefig(OUT / name, dpi=110, metadata={"Software": None})
    plt.close(fig)
    pngs.append(name)
    return name


for old in OUT.glob("pd2-*.png"):
    old.unlink()
PNG = {vk: fig_var(vk) for vk in VARS}

# ══ 보고서에 쓰는 파생 값 ══
bill = {pl: revenue(pl, B) for pl in PLANS}
mg = {pl: margin(pl, B) for pl in PLANS}
ALT = {mode: month(BASE, mode) for mode in ("full", "low", "talk")}
COORD = {"c": 467, "s": 639, "mix": 553, "M": 133000, "ec": 17.4, "es": 2.5}  # 코디가 브리프에 적은 값(원)
ctx_share = (BASE["rho"] * BASE["kc"] + (1 - BASE["rho"]) * BASE["ks"]) * CTX_USD / B["mix"]
ctx_share_s = B["hs"]["fix"] / B["hs"]["cost"]
STOP = month({**BASE, "kc": BASE["nc"], "ks": BASE["ns"]})  # 수동 stop — 발화마다 세션
stop_m = {pl: margin(pl, STOP) for pl in PLANS}
light = month({**BASE, "H": 1.0, "D": 1.0})
ref_hours_cost = REF_KRW / (B["mix"] * FX)
ref_tok = REF_KRW / P["tok"]  # 2만원으로 사는 토큰(백만 개)
ref_hours_tok = ref_tok * 1e6 / B["mixtok"]
loss_vars = {pl: [vk for vk in VARS if VARS[vk]["cross"][pl]] for pl in PLANS}
min1 = {pl: min((VARS[vk]["minm"][pl], vk) for vk in VARS) for pl in PLANS}  # 변인 1개 민감도의 최저 마진
ACT = {m: {pl: margin(pl, B, PR[m]) for pl in PLANS} for m in MARGINS}       # 올림 뒤 실제 마진(W3)

# 시간제의 청구 시계(W1) — 무엇을 「1시간」으로 재나
METERS = {
    "use": "실사용 시간 — 통역 화면을 켜고 응대한 시간(적정 케이스의 「하루 실사용 시간」과 같은 시계)",
    "stream": "스트림 시간 — STT 연결이 열려 있던 시간(서버가 재는 값 · 원가 시계와 같다)",
    "talk": "발화 시간 — 발화 연결 시간만(발화 사이 공백 · 60초 꼬리 제외)",
}


def meter_min(meter, smode):
    """실사용 1시간(섞음)에 청구 시계가 재는 분."""
    if meter == "use":
        return 60.0
    a = ALT[smode if meter == "stream" else "talk"]
    return (BASE["rho"] * a["hc"]["sec"] + (1 - BASE["rho"]) * a["hs"]["sec"]) / 60


METER = {}
for mt in METERS:
    for sm in ("full", "low"):
        mins = meter_min(mt, sm)
        rev_h = P["hour"] * mins / 60
        cost_h = ALT[sm]["mix"] * FX
        METER[(mt, sm)] = {"min": mins, "rev": rev_h, "cost": cost_h, "margin": (rev_h - cost_h) / rev_h,
                           "need": ceil_to(cost_h / (1 - M_BASE) / (mins / 60), ROUND_HOUR)}
meter_lo = min(v["margin"] for v in METER.values())
meter_hi = max(v["margin"] for v in METER.values())
tok_low_m = margin("tok", ALT["low"])    # 스트림 하한 셈법일 때 토큰제 마진
flat_low_m = margin("flat", ALT["low"])


# 세션 · 발화 · 상담 비율을 한꺼번에 가장 나쁜 쪽으로(실현 가능한 조합만)
def corner(case, n_max):
    best_c, best_r = None, None
    for n in range(1, int(n_max) + 1):
        if n * case["d"] > 3600:
            break
        kmax = min(n, (3600 - n * case["d"]) / SILENCE_S)
        if kmax < 1:
            break  # 세션 1회(60초 꼬리)도 안 들어간다 — 실현 불가(n 이 커질수록 더 안 들어간다)
        for k in (1.0, kmax):
            assert n * case["d"] + k * SILENCE_S <= 3600 + 1e-9 and k <= n
            h = hour_cost(case, k, n)
            if best_c is None or h["cost"] > best_c[0]:
                best_c = (h["cost"], k, n)
            if best_r is None or h["cost"] / h["tok"] > best_r[0]:
                best_r = (h["cost"] / h["tok"], k, n)
    return best_c, best_r


cc_, cr_ = corner(C, RANGE_USER["nc_max"])
sc_, sr_ = corner(S, RANGE_USER["ns_max"])
worst_cost = max((cc_ + ("상담",)), (sc_ + ("간단 통역",)))      # 1시간 원가가 가장 큰 조합
worst_ratio = max((cr_ + ("상담",)), (sr_ + ("간단 통역",)))    # 토큰당 원가가 가장 큰 조합
worst_m = {"hour": 1 - worst_cost[0] * FX / P["hour"], "tok": 1 - worst_ratio[0] * 1e6 * FX / P["tok"],
           "flat": 1 - worst_cost[0] * FX * B["hours"] / P["flat"]}

# 토큰제에서 고객이 실사용 1시간에 내는 돈의 폭(변인 1개 민감도 전체)
tok_per_h = [revenue("tok", r) / r["hours"] for vk in ("rho", "kc", "nc", "ks", "ns") for _, r in VARS[vk]["rows"]]
tok_h_lo, tok_h_hi, tok_h_base = min(tok_per_h), max(tok_per_h), bill["tok"] / B["hours"]

# 결론의 근거가 계산과 어긋나면 멈춘다 — 추천이 토큰제인 이유
assert BEST == "tok"
assert not loss_vars["tok"] and min1["tok"][0] > min1["hour"][0] + 0.2 and min1["tok"][0] > min1["flat"][0] + 0.2
assert stop_m["tok"] > 0.3 > 0 > stop_m["hour"] and stop_m["flat"] < 0
assert worst_m["tok"] > 0 > worst_m["hour"]
assert meter_lo < 0.2 < tok_low_m
for vk in ("H", "D"):
    assert abs(margin("tok", VARS[vk]["r_lo"]) - mg["tok"]) < 1e-9 and VARS[vk]["cross"]["flat"] is not None
assert all(abs(c["cost_fn"] - c["cost_log"]) < 1e-12 for c in CASES.values())
assert abs(C["e_aud"] * FX - COORD["ec"]) < 0.05 and abs(S["e_aud"] * FX - COORD["es"]) < 0.05

T_U, T_A, T_C, T_R, T_O = "〔사용자 지정〕", "〔가정 — 사용자 승인〕", "〔계산〕", "〔실측〕", "〔공식〕"
L = []
w = L.append
m100 = f"{M_BASE * 100:.0f}%"

w("# 통키 요금제 설계 — 적정 케이스에서 가격을 정한다")
w("")
w(f"- 작성 2026-11-12 · 2판(1판은 `orchestration/work/interpreter-idea/pricing-design-v1.md`) · 실측 조회일 2026-11-12 · 단가 출처 {PRICING_URL} {T_O}")
w("- 숫자 · 그래프는 전부 `orchestration/work/interpreter-idea/pricing-calc2/calc2.py` 가 뽑았다(손 편집 없음). 맨 위 「적정 케이스」 블록을 고치고 다시 돌리면 이 문서 전체가 다시 나온다.")
w("- 근거 표기: 〔실측〕 Soniox usage-logs · 〔공식〕 Soniox 문서 · 〔사용자 지정〕 사용자가 정한 값 · 〔가정〕 근거가 약한 값(「사용자 승인」이 붙으면 사용자가 확정한 적정 케이스) · 〔계산〕 식을 같이 적음.")
w(f"- 금액은 원으로 적는다 — USD 원가 × 환율 {FX:,}원/USD 〔가정〕. 특정 병원 · 지점 데이터는 쓰지 않았다.")
w("")

# ── 0. 결론 ──
w("## 0. 결론")
w("")
w(f"**추천: 토큰제 — 그 달에 쓴 Soniox 토큰 100만 개당 {P['tok']:,}원**(1,000개당 {P['tok'] / 1000:g}원 · 계정별로 합산해 월말 청구) {T_C} §4 · 마진율 {m100} 〔가정〕.")
w("")
w("**왜 토큰제인가** — 실사용 데이터가 하나도 없는 지금, 재지 못한 것에 마진이 걸리지 않는 안이라서다.")
w("")
w(f"1. **변인 하나를 범위 끝까지 밀었을 때 가장 낮은 마진이 {pct(min1['tok'][0])}다.** 같은 조건에서 시간제는 {pct(min1['hour'][0])}({VARS[min1['hour'][1]]['name']} {xfmt(min1['hour'][1], VARS[min1['hour'][1]]['hi'])}) · 정액제는 {pct(min1['flat'][0])}(하루 실사용 12h)다. 세션 · 발화 · 상담 비율을 한꺼번에 가장 나쁜 쪽으로 몰아도 토큰제는 {pct(worst_m['tok'])} · 시간제는 {pct(worst_m['hour'])}다 {T_C} §5.")
w(f"2. **세션 정책이 바뀌어도 버틴다.** 수동 stop 을 허용해 발화마다 세션이 새로 열리면 시간제 {pct(stop_m['hour'])} · 정액제 {pct(stop_m['flat'])} · 토큰제 {pct(stop_m['tok'])}다 — 세션이 늘면 context 토큰이 같이 늘어 매출이 원가를 따라간다 {T_C} §6.")
w(f"3. **무엇을 재서 청구하는지가 이미 정해져 있다.** 토큰은 Soniox 사용 기록의 숫자 그대로다 — 단 그 숫자를 고객 계정별로 가르는 집계는 아직 안 된다(확인 전 · §7 #6). 시간제는 「1시간」을 무엇으로 재느냐(실사용 · 스트림 · 발화 시간)에 따라 같은 {P['hour']:,}원에서 마진이 {pct(meter_hi)} ~ {pct(meter_lo)}로 갈리고, 그 정의는 아직 없다 {T_C} §4.2.")
w("")
w(f"**치르는 값**: 고객이 청구액을 미리 셈하기 어렵다. 같은 1시간을 써도 세션 · 발화가 얼마나 잦으냐에 따라 {won(tok_h_lo)}에서 {won(tok_h_hi)}까지 나온다(적정 케이스 {won(tok_h_base)}) {T_C} §5. 그래서 고객 안내는 「보통 1시간에 약 {round(tok_h_base, -2):,.0f}원」 같은 환산과 사용량 화면으로 덧붙여야 한다 〔가정〕.")
w("")
w("이 표가 보여 주는 것: 세 요금제를 같은 잣대로 놓은 것 — 적정 케이스 청구액은 같고, 적정 케이스를 벗어날 때의 마진과 고객의 셈이 갈린다.")
w("")
w("| 요금제 | 가격 | 적정 케이스 월 청구액 | 변인 1개를 범위 끝까지 — 최저 마진 | 한꺼번에 최악 | 수동 stop 허용 시 | 고객이 미리 셈할 수 있나 | 근거 |")
w("|---|--:|--:|--:|--:|--:|---|---|")
calc_note = {
    "hour": f"청구 시계가 실사용 시간이면 된다(시간 × {P['hour']:,}원) · 스트림 시간이면 어렵다",
    "tok": f"어렵다 — 실사용 1시간에 {won(tok_h_lo)} ~ {won(tok_h_hi)}",
    "flat": "된다 — 매달 같은 금액",
}
price_txt = {"hour": f"기기·시간당 {P['hour']:,}원", "tok": f"100만 토큰당 {P['tok']:,}원", "flat": f"계정당 월 {P['flat']:,}원"}
for pl in ("tok", "hour", "flat"):
    nm = f"**{PLANS[pl]}(추천)**" if pl == BEST else PLANS[pl]
    w(f"| {nm} | {price_txt[pl]} | {won(bill[pl])} | {pct(min1[pl][0])} | {pct(worst_m[pl])} | {pct(stop_m[pl])} | {calc_note[pl]} | {T_C} §4 · §5 · §6 |")
w("")
w("이 표가 보여 주는 것: 적정 케이스 고객(하루 4h · 2대 · 상담 반반) 한 계정이 토큰제로 한 달에 내는 돈과 우리 원가 {T_C} · 조건 {T_A}.".format(T_C=T_C, T_A=T_A))
w("")
w("| 항목 | 값 | 근거 |")
w("|---|--:|---|")
w(f"| 월 사용량 | {B['hours']:,.0f} 기기·시간 · {B['TOK'] / 1e6:,.2f} 백만 토큰 | {T_C} 30일 × 2대 × 4h × 1시간 {B['mixtok']:,.0f} 토큰 · 값은 {T_A} |")
w(f"| 월 청구액 | {won(bill['tok'])} | {T_C} {B['TOK'] / 1e6:,.2f} 백만 토큰 × {P['tok']:,}원 |")
w(f"| 월 원가(Soniox) | {won(B['M'])} | {T_C} §3 |")
w(f"| 월 이익 | {won(bill['tok'] - B['M'])} | {T_C} 청구액 − 원가 |")
w(f"| 마진 | {pct(mg['tok'])} | {T_C} 이익 ÷ 청구액 |")
w("")
w(f"- **월 2만원과의 관계**: 적정 케이스 청구액 {man(bill['tok'])}은 2만원의 {bill['tok'] / REF_KRW:.1f}배다. 2만원으로는 {ref_tok:.2f} 백만 토큰 — 적정 케이스 쓰임새로 월 {ref_hours_tok:.1f} 기기·시간(1대로 하루 {ref_hours_tok / DAYS * 60:.0f}분)을 쓴다. 원가만 따져도 2만원은 월 {ref_hours_cost:.1f} 기기·시간어치라, 「월 2만원 정액」은 적정 케이스에서 매달 {won(B['M'] - REF_KRW)} 적자다 {T_C} · 2만원은 대표 투표 참고선 {T_U}.")
w(f"- **시간제를 고를 수 있게 되는 조건**: ① 청구 시계를 정하고 ② 세션이 무발화 1분 자동 종료로만 끝나며 ③ 실제 세션 수를 재서 간단 통역 1시간 {xfmt('ks', KS_MAX)} 같은 끝이 안 나온다는 것을 확인한 뒤다. 그때는 고객이 셈할 수 있다는 장점이 살아난다 {T_C} §4.2 · §5 · 정책 {T_U}.")
w(f"- 이 결론은 §1 적정 케이스 표 위에 서 있다. 표의 값이 바뀌면 단가가 바뀐다 — 「하루 4h」는 근거가 약하다고 사용자가 밝힌 값이지만, 하루 실사용 시간 · 대수는 토큰제 단가를 바꾸지 않고 월 청구액만 바꾼다 {T_A}.")
w(f"- 2판 첫 원고는 시간제를 추천했다. 검수에서 그 이유 둘(시간 · 대수에 마진 고정 · 범위 안 적자 없음)이 토큰제에도 똑같이 맞고 최저 마진은 토큰제가 높다는 점({pct(min1['tok'][0])} 대 {pct(min1['hour'][0])})이 드러나 추천을 바꿨다 {T_C}.")
w("")

# ── 1. 적정 케이스 ──
w("## 1. 적정 케이스 가정 표")
w("")
w("**이 표만 고치면 결론이 바뀐다.** 아래 값은 스크립트 맨 위 블록에 그대로 들어 있다.")
w("")
w("이 표가 보여 주는 것: 변인마다 「적정 케이스는 이것」으로 놓은 값 · 사용자가 준 범위 · 그렇게 놓은 이유.")
w("")
w("| 변인 | 적정 | 범위 | 이유 | 근거 |")
w("|---|--:|---|---|---|")
w(f"| 하루 실사용 시간(기기 1대) | {BASE['H']:g}h | 1 ~ 12h | 근무 12h 중 외국인 응대 약 1/3 — **근거 약함** | 적정 {T_A} · 범위 {T_U} |")
w(f"| 동시 사용 대수 | {BASE['D']:g}대 | 1 ~ 5대 | 상담실 1대 + 데스크 1대 | 적정 {T_A} · 범위 {T_U} |")
w(f"| 상담 비율(시간 기준) | {BASE['rho'] * 100:g}% | 0 ~ 100% | 범위 가운데 | 적정 {T_A} · 범위 {T_U} |")
w(f"| 상담 1시간 | 세션 {BASE['kc']:g}회 · 발화 {BASE['nc']:g}개 | 세션 1회 ~ 최대 · 발화 ~ 44개 | 1분 넘는 공백 1번 · 밀도 최대(44개)의 절반 | 적정 {T_A} · 범위 {T_U} |")
w(f"| 간단 통역 1시간 | 세션 {BASE['ks']:g}회 · 발화 {BASE['ns']:g}개 | 세션 1회 ~ 최대 · 발화 ~ 170개 | 짧은 응대 6분에 1번 · 밀도 최대(170개)의 절반 | 적정 {T_A} · 범위 {T_U} |")
w(f"| 세션 종료 | 무발화 1분 자동 종료만 | 정책 | 수동 stop 은 넣지 않는다 | {T_U} |")
w(f"| 한 달 | {DAYS}일 | — | — | {T_U} |")
w(f"| 환율 | {FX:,}원/USD | — | 사용자 미정 | 〔가정〕 |")
w(f"| 마진율 | {m100} 기준 · 30% · 70% 병기 | — | 사용자 미정 | 〔가정〕 |")
w("")
w("- 낱말: **세션** = STT 연결 한 번(열 때마다 context 를 보내 연결 고정비가 든다) · **발화** = 한 사람이 한 번 말하고 통역이 나오는 한 덩이 · **기기·시간** = 기기 1대가 1시간 쓴 양(2대가 4h 쓰면 8 기기·시간) 〔계산〕.")
w(f"- **적정 케이스 표에 없어 이 문서가 더한 가정 1개**: 「실사용 1시간」 동안 STT 스트림은 60분 내내 열려 있다고 본다 〔가정〕(미승인 · §3.3 에서 다른 셈법과 비교 · §7 #5).")
w(f"- 발화 범위 끝(44개 · 170개)은 사용자 지정값이다. 실측 연결 시간으로 1시간에 들어가는 최대는 상담 {NC_FEAS:.1f}개 · 간단 통역 {NS_FEAS:.1f}개 {T_C} 3,600초 ÷ 발화 하나 연결 시간(§2) — 상담 44개는 실측 기준으로는 1시간에 다 들어가지 않는다.")
w("")

# ── 2. 원가 함수 ──
w("## 2. 원가 함수")
w("")
w("이 표가 보여 주는 것: Soniox 가 돈을 받는 다섯 항목의 단가.")
w("")
w("| 과금 항목 | 단가(USD / 100만 토큰) | 근거 |")
w("|---|--:|---|")
for nm, p_ in (("STT 입력 오디오(실시간)", P_AIN), ("STT 입력 텍스트(context)", P_TIN), ("STT 출력 텍스트(전사 + 번역)", P_TOUT),
               ("TTS 입력 텍스트", P_TTSIN), ("TTS 출력 오디오", P_AOUT)):
    w(f"| {nm} | {p_ * 1e6:.2f} | {T_O} {PRICING_URL} |")
w("")
w(f"- 실시간 오디오는 1시간에 30,000 토큰으로 환산한다 {T_O} {PRICING_URL}. STT 는 스트림이 열려 있는 전체 시간을 과금한다 {T_O} {URL_KEEPALIVE}.")
w("")
w("```text")
w("한 연결의 원가(USD) = 2.00 × 입력 오디오 토큰 + 4.00 × context 토큰 + 4.00 × 출력 텍스트 토큰      〔공식〕 단가")
w("                     + 4.00 × TTS 입력 토큰 + 21.50 × TTS 출력 오디오 토큰      (각 항 ÷ 100만)   〔공식〕 단가 × 토큰")
w("```")
w("")
w(f"이 표가 보여 주는 것: 실측 2건의 토큰을 위 식에 넣으면 Soniox 가 청구한 금액과 같다(식이 맞다는 확인) {T_R} · {T_C}.")
w("")
w("| 실측 | 언어쌍 | context 토큰 | 입력 오디오 토큰 | 출력 텍스트 토큰 | TTS 입력 토큰 | TTS 출력 오디오 토큰 | 스트림 시간 | 식으로 계산 | 로그 청구액 | 근거 |")
w("|---|---|--:|--:|--:|--:|--:|--:|--:|--:|---|")
for c in CASES.values():
    w(f"| {c['name']} | {c['pair']} | {c['ctx_tok']:,}개 | {c['a_in']:,}개 | {c['t_out']:,}개 | {c['t_tts']:,}개 | {c['a_tts']:,}개 | {c['d']:.1f}초 | ${c['cost_fn']:.7f} | ${c['cost_log']:.7f} | 토큰 · 시간 · 청구액 {T_R} · 식 {T_C} |")
w("")
w(f"이 표가 보여 주는 것: 1시간 원가를 만드는 세 부품 — 시간에 붙는 것 · 세션에 붙는 것 · 발화에 붙는 것 {T_C}.")
w("")
w("| 부품 | 무엇에 비례 | 값(USD) | 값(원) | 근거 |")
w("|---|---|--:|--:|---|")
w(f"| 스트림 오디오비 | 스트림이 열린 시간 | ${A_USD_H:.4f} / 시간 | {won1(A_USD_H * FX)} / 시간 | {T_C} 30,000 토큰 × $2.00 ÷ 100만 · 단가 {T_O} |")
w(f"| 연결 고정비 | 세션 수 | ${CTX_USD:.6f} / 세션 | {won1(CTX_USD * FX)} / 세션 | {T_C} context {CTX_TOK:,} 토큰 × $4.00 ÷ 100만 — 토큰 수는 context 가 가장 큰 번체 중국어 기준 〔가정〕(추정 · 1판 §1.4) |")
w(f"| 상담 발화 변동비 | 상담 발화 수 | ${C['e']:.7f} / 발화 | {won1(C['e'] * FX)} / 발화 | {T_C} 실측 토큰 × 단가(출력 텍스트 + TTS 입력 + TTS 출력) · 토큰 {T_R} |")
w(f"| 간단 통역 발화 변동비 | 간단 통역 발화 수 | ${S['e']:.7f} / 발화 | {won1(S['e'] * FX)} / 발화 | {T_C} 같은 식 · 토큰 {T_R} |")
w("")
w(f"- 브리프에 적힌 발화 단가(상담 {COORD['ec']}원 · 간단 통역 {COORD['es']}원)와 위 표가 다른 이유: 브리프 값은 그 발화의 입력 오디오(상담 {C['a_in']:,} 토큰 = {won1(P_AIN * C['a_in'] * FX)} · 간단 통역 {S['a_in']:,} 토큰 = {won1(P_AIN * S['a_in'] * FX)})를 발화에 넣은 것이고, 이 문서는 그것을 스트림 오디오비로 옮겨 셌다. 넣어서 세면 {won1(C['e_aud'] * FX)} · {won1(S['e_aud'] * FX)}이 되어 브리프와 같다 {T_C} · 토큰 {T_R}.")
w("")
w("```text")
w("기기 1대 · 실사용 1시간 원가 = 스트림 오디오비 + 세션 수 × 연결 고정비 + 발화 수 × 발화 변동비      〔계산〕")
w("월 원가 = 30일 × 동시 사용 대수 × 하루 실사용 시간 × (상담 비율 × 상담 1시간 원가 + (1 − 상담 비율) × 간단 통역 1시간 원가)   〔계산〕")
w("```")
w("")

# ── 3. 적정 케이스 원가 ──
w("## 3. 적정 케이스 원가")
w("")
w("### 3.1 1시간 원가")
w("")
w(f"이 표가 보여 주는 것: 적정 케이스의 1시간 원가를 부품별로 쌓은 것(기기 1대 · 원) {T_C}.")
w("")
w("| 종류 | 스트림 오디오비 | 연결 고정비 | 발화 변동비 | **1시간 원가** | 근거 |")
w("|---|--:|--:|--:|--:|---|")
for nm, h, c, k, n in (("상담", B["hc"], C, BASE["kc"], BASE["nc"]), ("간단 통역", B["hs"], S, BASE["ks"], BASE["ns"])):
    w(f"| {nm} 1시간 | {won1(h['aud'] * FX)} | {k:g}회 × {won1(CTX_USD * FX)} = {won1(h['fix'] * FX)} | {n:g}개 × {won1(c['e'] * FX)} = {won1(h['var'] * FX)} | **{won(h['cost'] * FX)}** | {T_C} 세 부품의 합 · 세션 · 발화 수 {T_A} |")
w(f"| 섞음(상담 {BASE['rho'] * 100:g}%) | — | — | — | **{won(B['mix'] * FX)}** | {T_C} {BASE['rho']:g} × {won(B['hc']['cost'] * FX)} + {1 - BASE['rho']:g} × {won(B['hs']['cost'] * FX)} |")
w("")
w(f"- 간단 통역이 상담보다 비싸다 — 세션이 1시간에 {BASE['ks']:g}회라 연결 고정비가 1시간 원가의 {ctx_share_s * 100:.0f}%를 차지한다. 섞음 기준으로도 연결 고정비가 {ctx_share * 100:.0f}%다 {T_C}.")
w("")
w("### 3.2 월 원가")
w("")
w("```text")
w(f"월 사용량 = {DAYS}일 × {BASE['D']:g}대 × {BASE['H']:g}h = {B['hours']:,.0f} 기기·시간                         〔계산〕 값은 〔가정 — 사용자 승인〕")
w(f"월 원가   = {B['hours']:,.0f} 기기·시간 × {won(B['mix'] * FX)} = {won(B['M'])} (약 {man(B['M'])})              〔계산〕")
w(f"월 토큰   = {B['hours']:,.0f} 기기·시간 × {B['mixtok']:,.0f} 토큰 = {B['TOK'] / 1e6:,.2f} 백만 토큰                  〔계산〕 토큰제에 쓴다")
w("```")
w("")
w("### 3.3 코디 계산과의 차이 — 스트림 오디오비를 세는 법")
w("")
w(f"코디가 브리프에 적은 값은 상담 {COORD['c']:,}원 · 간단 {COORD['s']:,}원 · 섞음 {COORD['mix']:,}원 / 월 약 {man(COORD['M'])}이다 〔가정〕(코디 계산). 이 문서의 값과 다른 이유는 **하나** — 스트림이 열려 있는 시간을 얼마로 보느냐다. 연결 고정비 · 발화 변동비는 같다 {T_C}.")
w("")
w("이 표가 보여 주는 것: 스트림 시간을 세는 세 가지 법과 그때의 원가. 이 문서는 맨 윗줄을 쓴다.")
w("")
w("| 셈법 | 상담 스트림 | 간단 스트림 | 상담 1시간 | 간단 1시간 | 섞음 1시간 | 월 원가 | 근거 |")
w("|---|--:|--:|--:|--:|--:|--:|---|")
for mode, nm in (("full", "**60분 내내 열림(이 문서)**"), ("low", "하한 — 발화 연결 시간 + 세션마다 60초 꼬리"), ("talk", "발화 연결 시간만(코디 계산과 같음)")):
    a = ALT[mode]
    w(f"| {nm} | {a['hc']['sec'] / 60:.1f}분 | {a['hs']['sec'] / 60:.1f}분 | {won(a['hc']['cost'] * FX)} | {won(a['hs']['cost'] * FX)} | {won(a['mix'] * FX)} | {won(a['M'])} | {T_C} |")
w("")
w(f"- 셋째 줄이 코디 값({COORD['c']:,}원 · {COORD['s']:,}원 · {COORD['mix']:,}원)과 맞는다 — 검산 일치 {T_C}.")
w(f"- 그 셈법을 쓰지 않은 이유: Soniox 는 발화 사이에도 스트림이 열려 있으면 과금하고 {T_O} {URL_KEEPALIVE}, 무발화 1분 자동 종료 {T_U} 는 세션마다 끝에 60초를 더 열어 둔다. 그래서 실제 값은 첫째 줄과 둘째 줄 사이다 {T_C}.")
w(f"- 첫째 줄(상한)을 고른 것은 원가를 낮게 잡지 않기 위해서다 〔가정〕. 둘째 줄이 맞다면 월 원가는 {(1 - ALT['low']['M'] / ALT['full']['M']) * 100:.1f}% 낮고, 토큰제 {P['tok']:,}원에서 마진은 {pct(tok_low_m)}다(오디오 토큰이 줄어 매출도 같이 준다). 시간제는 청구 시계에 따라 갈린다 — §4.2 {T_C}.")
w("")

# ── 4. 요금제 3안 ──
w("## 4. 요금제 3안 — 적정 케이스 기준")
w("")
w("### 4.1 세 안의 가격")
w("")
w(f"가격은 「적정 케이스 고객에게서 마진율을 지키는 값」으로 정한다: **가격 = 적정 케이스 원가 ÷ (1 − 마진율)**, 그리고 시간제 · 토큰제는 {ROUND_HOUR}원, 정액제는 {ROUND_FLAT:,}원 단위로 올림 {T_C} · 올림 단위 〔가정〕.")
w("")
w(f"이 표가 보여 주는 것: 세 요금제의 과금 공식 · 마진율 {m100} 가격 · 적정 케이스 고객의 월 청구액과 마진 {T_C} · 마진율 〔가정〕.")
w("")
w("| 요금제 | 과금 공식 | 올림 전 가격 | **가격** | 적정 케이스 월 청구액 | 월 원가 | 마진 | 근거 |")
w("|---|---|--:|--:|--:|--:|--:|---|")
rp = raw_prices(M_BASE)
w(f"| 시간제 | 월 청구 = 기기·시간 × 단가 | {won1(rp['hour'])} | **기기·시간당 {P['hour']:,}원** | {won(bill['hour'])} | {won(B['M'])} | {pct(mg['hour'])} | {T_C} {won(B['mix'] * FX)} ÷ (1 − {M_BASE:g}) |")
w(f"| 토큰제 | 월 청구 = 쓴 Soniox 토큰(100만 단위) × 단가 | {won1(rp['tok'])} | **100만 토큰당 {P['tok']:,}원** | {won(bill['tok'])} | {won(B['M'])} | {pct(mg['tok'])} | {T_C} 토큰 100만 개 원가 {won(B['mix'] / B['mixtok'] * 1e6 * FX)} ÷ (1 − {M_BASE:g}) |")
w(f"| 정액제 | 월 청구 = 고정액(포함량 {B['hours']:,.0f} 기기·시간) | {won1(rp['flat'])} | **계정당 월 {P['flat']:,}원** | {won(bill['flat'])} | {won(B['M'])} | {pct(mg['flat'])} | {T_C} {won(B['M'])} ÷ (1 − {M_BASE:g}) · 포함량 = 적정 케이스 사용량 |")
w("")
w(f"- 적정 케이스에서는 세 요금제의 청구액이 거의 같다(그렇게 맞춘 가격이라서). **차이는 고객이 적정 케이스에서 벗어날 때** 난다 — §5 {T_C}.")
w(f"- 토큰제의 「토큰」은 Soniox 가 세는 다섯 종류 토큰의 합이다. 종류마다 원가가 100만 개당 $2.00 ~ $21.50 로 달라 {T_O}, 한 단가로 받으면 고객이 무엇을 많이 쓰느냐에 따라 마진이 움직인다 {T_C} §5.")
w(f"- 정액제의 포함량을 넘는 사용을 어떻게 할지는 정하지 않았다(§7 #8). §5 는 「넘어도 추가 청구 없음」으로 계산한다 — 넘는 만큼 시간제 단가로 받으면 그 구간은 시간제와 같아진다 〔가정〕 · {B['hours']:,.0f} 기기·시간 {T_C}.")
w("")
w(f"이 표가 보여 주는 것: 마진율을 30% · 50% · 70% 로 바꿨을 때의 가격과, 올림 때문에 실제로 남는 마진 {T_C} · 마진율 〔가정〕.")
w("")
w("| 목표 마진율 | 시간제(기기·시간당) | 실제 마진 | 토큰제(100만 토큰당) | 실제 마진 | 정액제(계정 · 월) | 실제 마진 | 토큰제 월 청구액 | 월 2만원 대비 | 근거 |")
w("|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|")
for m in MARGINS:
    p = PR[m]
    b = revenue("tok", B, p)
    w(f"| {m * 100:.0f}% | {p['hour']:,}원 | {pct(ACT[m]['hour'])} | {p['tok']:,}원 | {pct(ACT[m]['tok'])} | {p['flat']:,}원 | {pct(ACT[m]['flat'])} | {won(b)} | {b / REF_KRW:.1f}배 | {T_C} 원가 ÷ (1 − 마진율) 뒤 올림 · 마진율 〔가정〕 |")
w("")
rp30 = raw_prices(0.30)
w(f"- 올림이 마진을 가장 크게 움직이는 곳은 목표 30% 의 시간제다 — 올림 전 {won1(rp30['hour'])}이 {PR[0.30]['hour']:,}원이 되어 실제 마진 {pct(ACT[0.30]['hour'])}({(ACT[0.30]['hour'] - 0.30) * 100:+.1f}%p) {T_C} · 올림 단위 〔가정〕.")
w("")
w("### 4.2 시간제의 청구 시계 — 무엇을 「1시간」으로 재나")
w("")
w(f"시간제는 가격만으로 끝나지 않는다. **무엇을 재서 「1시간」이라 부를지**가 정해져야 하고, 지금은 정해져 있지 않다 〔가정〕(미승인 · §7 #5). 후보는 셋이다. 원가 쪽에도 미승인 가정(스트림이 60분 내내 열리나 · §3.3)이 있어 둘을 곱한 표로 본다 {T_C} · 단가 {P['hour']:,}원 그대로.")
w("")
w(f"이 표가 보여 주는 것: 청구 시계 정의 × 스트림 셈법마다, 실사용 1시간에 청구되는 분 · 매출 · 원가 · 마진 · 마진율 {m100} 을 지키려면 필요한 단가(적정 케이스 섞음 · 기기 1대) {T_C}.")
w("")
w("| 청구 시계 | 스트림 셈법(§3.3) | 실사용 1시간에 청구되는 시간 | 매출 | 원가 | 마진 | 마진율을 지키는 단가(청구 시간 1시간당) | 근거 |")
w("|---|---|--:|--:|--:|--:|--:|---|")
for mt, mname in METERS.items():
    for sm, sname in (("full", "60분 내내 열림"), ("low", "하한")):
        x = METER[(mt, sm)]
        w(f"| {mname} | {sname} | {x['min']:.1f}분 | {won(x['rev'])} | {won(x['cost'])} | {pct(x['margin'])} | {x['need']:,}원 | {T_C} 청구 분 ÷ 60 × {P['hour']:,}원 |")
w("")
w(f"- **스트림 시간으로 재면** 스트림이 실제로 얼마나 열려 있느냐에 따라 같은 단가의 마진이 {pct(METER[('stream', 'full')]['margin'])} ~ {pct(METER[('stream', 'low')]['margin'])}로 벌어진다 — 필요한 단가가 {METER[('stream', 'full')]['need']:,}원 ~ {METER[('stream', 'low')]['need']:,}원 사이 어디인지 데이터 없이는 모른다 {T_C}.")
w(f"- **발화 시간으로 재면** {P['hour']:,}원은 어느 셈법에서도 적자다({pct(METER[('talk', 'full')]['margin'])} · {pct(METER[('talk', 'low')]['margin'])}) {T_C}.")
w(f"- **실사용 시간으로 재면** 마진은 {pct(METER[('use', 'full')]['margin'])} ~ {pct(METER[('use', 'low')]['margin'])}로 안정되지만, 서버가 바로 잴 수 있는 값이 아니다 — 화면을 켜 둔 시간으로 대신하면 응대하지 않은 시간까지 청구된다 〔가정〕 · 마진 {T_C}.")
w(f"- 같은 두 셈법에서 토큰제 마진은 {pct(mg['tok'])} · {pct(tok_low_m)} — 청구 시계를 따로 정할 필요가 없다 {T_C}.")
w(f"- 이 문서의 시간제 숫자(§4.1 · §5 · §6)는 첫 줄(청구 시계 = 실사용 시간 · 스트림 60분)로 계산했다 〔가정〕(미승인) · {T_C}.")
w("")

# ── 5. 민감도 ──
w("## 5. 민감도 — 변인 1개만 움직인다")
w("")
w(f"읽는 법: 변인 하나를 범위 끝에서 끝까지 움직이고 **나머지는 적정 케이스에 고정**한다. 가격은 §4 의 마진율 {m100} 가격 그대로다. 마진이 0% 아래면 적자다. 정액제는 포함량을 넘어도 추가 청구가 없다고 본다 〔가정〕 · 가격 {T_C} §4.")
w("")
w("### 5.1 한눈에 — 어느 값에서 적자로 넘어가나")
w("")
w("이 표가 보여 주는 것: 변인 × 요금제마다 적자로 넘어가는 값(변인의 단위로). 없으면 범위 안에서 가장 낮은 마진.")
w("")
w("| 변인(범위) | 적정 | 시간제 | 토큰제 | 정액제 | 근거 |")
w("|---|--:|---|---|---|---|")
for vk, V in VARS.items():
    w(f"| {V['name']}({xfmt(vk, V['lo'])} ~ {xfmt(vk, V['hi'])}) | {xfmt(vk, BASE[vk])} | {cross_txt(vk, 'hour')} | {cross_txt(vk, 'tok')} | {cross_txt(vk, 'flat')} | {T_C} 매출 = 원가가 되는 점 |")
w("")
n_loss = {pl: len(loss_vars[pl]) for pl in PLANS}
w(f"- 한꺼번에 최악(결론 표의 그 열): 세션 · 발화 수를 실현 가능한 조합(세션 ≤ 발화 · 발화 연결 시간 + 세션마다 60초 ≤ 3,600초) 안에서 가장 나쁜 쪽으로 몬 것이다. 시간제 · 정액제는 1시간 원가가 가장 큰 {worst_cost[3]}만 · 세션 {worst_cost[1]:.1f}회 · 발화 {worst_cost[2]:g}개(1시간 원가 {won(worst_cost[0] * FX)}), 토큰제는 토큰당 원가가 가장 큰 {worst_ratio[3]}만 · 세션 {worst_ratio[1]:.1f}회 · 발화 {worst_ratio[2]:g}개(100만 토큰 원가 {won(worst_ratio[0] * 1e6 * FX)} · 단가 {P['tok']:,}원)에서 난다 {T_C}.")
w(f"- 범위 안에서 적자가 나는 변인 수: 시간제 {n_loss['hour']}개 · 토큰제 {n_loss['tok']}개 · 정액제 {n_loss['flat']}개(변인 {len(VARS)}개 중) {T_C}.")
w("")
for i, (vk, V) in enumerate(VARS.items(), 1):
    w(f"### 5.{i + 1} {V['name']}")
    w("")
    w(f"범위 {xfmt(vk, V['lo'])} ~ {xfmt(vk, V['hi'])} — {V['tag']} · 적정 {xfmt(vk, BASE[vk])} {T_A}.")
    w("")
    w(f"이 표가 보여 주는 것: {V['name']}만 범위 양 끝으로 보냈을 때의 월 원가와 요금제별 월 매출 · 마진 {T_C}.")
    w("")
    w("| 값 | 월 원가 | 시간제 매출 | 시간제 마진 | 토큰제 매출 | 토큰제 마진 | 정액제 매출 | 정액제 마진 | 근거 |")
    w("|--:|--:|--:|--:|--:|--:|--:|--:|---|")
    for lab, x, r in (("범위 아래 끝", V["lo"], V["r_lo"]), ("적정", BASE[vk], B), ("범위 위 끝", V["hi"], V["r_hi"])):
        cells = " | ".join(f"{won(revenue(pl, r))} | {pct(margin(pl, r))}" for pl in PLANS)
        w(f"| {lab} {xfmt(vk, x)} | {won(r['M'])} | {cells} | {T_C} |")
    w("")
    w(f"- 적자 전환: 시간제 — {cross_txt(vk, 'hour')} · 토큰제 — {cross_txt(vk, 'tok')} · 정액제 — {cross_txt(vk, 'flat')} {T_C}.")
    if vk == "nc":
        w(f"- 실측 연결 시간으로는 상담 발화가 1시간에 {NC_FEAS:.1f}개까지만 들어간다 — 그 오른쪽은 사용자 지정 범위(44개)를 그대로 그린 것이다 {T_C}.")
    if vk == "ks":
        w(f"- 범위 위 끝 {xfmt(vk, KS_MAX)}는 발화 {BASE['ns']:g}개의 연결 시간을 뺀 나머지를 60초 꼬리로 다 채운 값이다 — 수동 stop 을 허용하면 이 끝이 발화 수({BASE['ns']:g}회)까지 늘어난다(§6) {T_C}.")
        w(f"- 범위의 끝은 하한 셈법(세션마다 60초 꼬리)으로 「1시간에 들어가는가」를 본 값이고, 원가는 60분 셈법으로 쟀다 — 두 셈법이 이 표에 같이 쓰였다(§3.3) {T_C}.")
    w("")
    w(f"![{V['name']}만 움직일 때 월 원가와 요금제별 월 매출]({PNG[vk]})")
    w("")
    w(f"그래프 읽는 법: 가로축 = {V['name']}({V['unit']}) · 세로축 = 월 금액(만원). 검은 굵은 실선(월 원가)이 요금제 선 위로 올라가는 구간이 적자다. 요금제 선은 표지로 가른다 — 시간제 ○(빈 원 · 실선) · 토큰제 △(굵은 점선) · 정액제 □(일점쇄선). 세로 점선 = 적정 케이스 〔계산〕.")
    ov = overlap_pairs(vk)
    if ov:
        w("")
        w("- 이 그래프에서 겹치는 선: " + " · ".join(f"{PLANS[a]}와 {PLANS[b]}" for a, b in ov) + f" — 적정 케이스 청구액을 같게 맞춘 가격이라 그렇다. " + ("표지를 정수 대수(1 ~ 5대)에만 찍어 두 표지가 같은 점에 겹친다 — 큰 빈 원 ○ 안에 △ 가 들어가 보인다" if vk == "D" else "표지가 엇갈려 찍혀 있다") + f" {T_C}.")
    w("")

# ── 6. 결론을 뒤집는 것 ──
w("## 6. 결론을 뒤집는 것")
w("")
w(f"1. **고객이 토큰 단위 청구를 받아들이지 않는다** — 그러면 시간제({P['hour']:,}원)로 가야 하고, 그 대가로 마진이 세션 수와 청구 시계에 걸린다: 간단 통역 세션 {xfmt('ks', KS_MAX)}/시간에서 {pct(min1['hour'][0])} · 수동 stop 허용 시 섞음 1시간 원가가 {won(B['mix'] * FX)}에서 {won(STOP['mix'] * FX)}까지 뛰어 {pct(stop_m['hour'])}(토큰제는 {pct(stop_m['tok'])}) · 청구 시계가 스트림 시간이면 {pct(METER[('stream', 'low')]['margin'])}까지 {T_C} §4.2 · §5.")
w(f"2. **계정별 토큰을 잴 수 없다** — 토큰제는 고객 계정마다 Soniox 토큰을 갈라 세야 청구할 수 있다. 통키가 지금 사용 기록에 계정 표시를 넣는지는 확인하지 않았다 〔가정〕(§7 #6). 안 되면 서버가 재는 스트림 시간 기준 시간제가 남고, 그 단가는 {METER[('stream', 'full')]['need']:,}원 ~ {METER[('stream', 'low')]['need']:,}원 사이다 {T_C} §4.2.")
w(f"3. **고객이 낼 수 있는 돈이 정말 월 2만원 근처다** — 그러면 요금제 종류가 아니라 사용량이 문제다. 2만원으로 원가를 덮는 사용량은 월 {ref_hours_cost:.1f} 기기·시간(1대 · 하루 {ref_hours_cost / DAYS:.1f}h)뿐이고, 적정 케이스는 그 {B['hours'] / ref_hours_cost:.1f}배를 쓴다. 가격이 아니라 원가를 먼저 줄여야 한다 — 섞음 1시간 원가의 {ctx_share * 100:.0f}%가 세션마다 드는 context 다 {T_C} · 2만원 {T_U}.")
w("")

# ── 7. 정할 것 ──
w("## 7. 정할 것 · 조사할 것")
w("")
w("이 표가 보여 주는 것: 사용자가 정해야 결론이 굳는 것과, 데이터를 모아야 좁혀지는 것.")
w("")
w("| # | 항목 | 지금 넣은 값 | 바뀌면 | 누가 · 무엇으로 | 근거 |")
w("|--:|---|---|---|---|---|")
w(f"| 1 | 마진율 | {m100} | 토큰제 단가 {PR[0.30]['tok']:,}원(30%) ~ {PR[0.70]['tok']:,}원(70%) / 100만 토큰 | 사용자 결정 | 〔가정〕 · {T_C} §4.1 |")
w(f"| 2 | 환율 | {FX:,}원/USD | 원 금액 전부가 환율에 비례 | 사용자 결정 | 〔가정〕 |")
w(f"| 3 | 수동 stop 정책 | 넣지 않음(무발화 1분 자동 종료만) | 허용하면 시간제 {pct(stop_m['hour'])} · 정액제 {pct(stop_m['flat'])} · 토큰제 {pct(stop_m['tok'])} — 토큰제 추천은 그대로, 고객 청구액은 세션만큼 는다 | 사용자 결정(허용 여부 · 재연결 횟수 제한) | {T_U} · {T_C} |")
w(f"| 4 | 실사용 데이터 | 없음 — 적정 케이스 7개 값 전부 가정 | 하루 실사용 시간 · 대수는 청구액을, 세션 · 발화 수는 단가를 바꾼다 | 계정 · 기기별로 세션 시작 · 끝 시각과 발화 수를 서버에 기록(2 ~ 4주) | {T_A} |")
w(f"| 5 | 시간제의 청구 시계 · 「실사용 1시간」 = 스트림 60분 | 청구 시계 = 실사용 시간 · 스트림 60분 내내 열림(상한) | 시간제 마진 {pct(meter_hi)} ~ {pct(meter_lo)} · 스트림 시간 기준 단가 {METER[('stream', 'full')]['need']:,}원 ~ {METER[('stream', 'low')]['need']:,}원 — §4.2. 결론(토큰제)은 바뀌지 않는다: 토큰제 마진 {pct(mg['tok'])} ~ {pct(tok_low_m)} · 월 원가는 하한이면 {(1 - ALT['low']['M'] / ALT['full']['M']) * 100:.1f}% 감소 | 사용자 결정(시간제를 고를 때) + 4번 기록으로 실제 스트림 시간 측정 | 〔가정〕(미승인) · {T_C} |")
w(f"| 6 | 계정별 토큰 집계 | 된다고 보고 계산 | 안 되면 토큰제로 청구할 수 없다 — §6 둘째 | 통키 서버가 Soniox 연결에 계정 표시를 넣는지 코드 확인 · 필요하면 구현 | 〔가정〕 |")
w(f"| 7 | 토큰제 고객 안내 방식 | 정하지 않음 | 고객이 보는 것은 1시간 {won(tok_h_lo)} ~ {won(tok_h_hi)}의 폭 — 환산 안내 · 사용량 화면 · 선불 충전 여부 | 사용자 결정 | 〔가정〕 · 폭 {T_C} |")
w(f"| 8 | 정액제 포함량 초과 처리 | 추가 청구 없음으로 계산 | 초과분을 시간제 단가로 받으면 §5 정액제 적자가 사라진다 | 사용자 결정(정액제를 고를 때) | 〔가정〕 · 포함량 {B['hours']:,.0f} 기기·시간 {T_C} |")
w(f"| 9 | 가격 올림 단위 | 시간제 · 토큰제 {ROUND_HOUR}원 · 정액제 {ROUND_FLAT:,}원 | 목표 50% · 70% 에서는 1%p 안쪽이지만, 목표 30% 에서는 시간제 실제 마진 {pct(ACT[0.30]['hour'])}({(ACT[0.30]['hour'] - 0.30) * 100:+.1f}%p) · 정액제 {pct(ACT[0.30]['flat'])}({(ACT[0.30]['flat'] - 0.30) * 100:+.1f}%p) · 토큰제 {pct(ACT[0.30]['tok'])} — §4.1 | 사용자 결정 | 〔가정〕 · {T_C} |")
w(f"| 10 | 무발화 1분 자동 종료 구현 | 구현된 것으로 계산 | 통키 main `17c26b5` 는 멈춘 동안에도 연결을 유지한다 — 그대로면 멈춘 시간도 시간당 {won1(A_USD_H * FX)} 원가 · 토큰제에서는 그 오디오 토큰이 고객 청구에도 들어간다 | 구현 · 배포 | {T_U} 정책 · {T_C} · {T_O} {URL_KEEPALIVE} |")
w(f"| 11 | context 가 세션마다 같은 양으로 과금되는가 | 매 세션 {CTX_TOK:,} 토큰(번체 중국어 추정) | 연결 고정비(섞음 원가의 {ctx_share * 100:.0f}%) 전체 | 같은 언어로 2회 이상 연결한 usage-log 확인 | 〔가정〕 · 문서는 「세션 시작 때 한 번」 {T_O} {URL_CONTEXT} |")
w(f"| 12 | 실측이 종류별 1건뿐 | 상담 {C['d']:.1f}초 · 간단 {S['d']:.1f}초짜리 발화 1건씩 | 발화 변동비 · 1시간에 들어가는 발화 수 | 발화 길이 분포 실측 | {T_R} 1건씩 |")
w(f"| 13 | STT 모델 교체 | `stt-rt-v5` 단가 | v5 는 2026-12-15 제거 예정 — 종류별 단가가 바뀌면 단가를 다시 계산 | 전환 뒤 usage-log | {T_O} {URL_MODELS} |")
w(f"| 14 | 부가세 · 결제 수수료 · 서버비 | 0원(Soniox 원가만) | 원가가 올라 같은 단가의 마진이 줄어든다 | 사용자 · 회계 결정 | 〔가정〕 |")
w("")

REPORT.write_text("\n".join(L) + "\n")

results = {
    "base": BASE, "fx": FX, "hour_cost_krw": {"consult": B["hc"]["cost"] * FX, "simple": B["hs"]["cost"] * FX, "mix": B["mix"] * FX},
    "month_hours": B["hours"], "month_cost_krw": B["M"], "month_tokens": B["TOK"],
    "prices": {str(m): PR[m] for m in MARGINS}, "bill": bill, "margin": mg,
    "alt_stream": {k: {"consult": a["hc"]["cost"] * FX, "simple": a["hs"]["cost"] * FX, "mix": a["mix"] * FX, "M": a["M"]} for k, a in ALT.items()},
    "cross": {vk: {pl: V["cross"][pl] for pl in PLANS} for vk, V in VARS.items()},
    "min_margin": {vk: V["minm"] for vk, V in VARS.items()},
    "ends": {vk: {"lo": V["lo"], "hi": V["hi"], "M_lo": V["r_lo"]["M"], "M_hi": V["r_hi"]["M"]} for vk, V in VARS.items()},
    "recommend": BEST, "manual_stop": {"mix": STOP["mix"] * FX, "margin": stop_m},
    "min_margin_1var": {pl: {"margin": min1[pl][0], "var": min1[pl][1]} for pl in PLANS}, "worst_corner_margin": worst_m,
    "worst_corner": {"cost": worst_cost[1:], "ratio": worst_ratio[1:]},
    "meter": {f"{mt}/{sm}": x for (mt, sm), x in METER.items()}, "tok_margin_low_stream": tok_low_m,
    "actual_margin": {str(m): ACT[m] for m in MARGINS}, "tok_per_use_hour": [tok_h_lo, tok_h_base, tok_h_hi],
    "D_int": {"ok": VD["int_ok"], "bad": VD["int_bad"]},
    "pngs": pngs,
}
(HERE / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1) + "\n")
print(f"월 원가 {B['M']:,.0f}원 · 1시간 상담 {B['hc']['cost'] * FX:.1f} / 간단 {B['hs']['cost'] * FX:.1f} / 섞음 {B['mix'] * FX:.1f}원")
print("가격", P, "· 마진", {k: round(v, 4) for k, v in mg.items()})
print("적자 변인", loss_vars)
print("보고서", REPORT.relative_to(ROOT), f"{len(L)}줄 · 그래프 {len(pngs)}장")
