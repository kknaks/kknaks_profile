"""통키 요금제 설계 — 계산 · 그래프 · 보고서 생성(손 편집 금지).

입력(같은 폴더):
- usage-logs-cost-probe-2026-11-12.json  Soniox GET /v1/usage-logs 원시 응답 중 cost-probe 항목(키 없음)
- context-chars.json                      count_context.py 출력(통키 main 17c26b5 의 build_context 로 센 글자 수)
출력:
- reference/2026-11-12-interpreter-idea/pricing-design.md · pd-*.png
- results.json(같은 폴더 — 재실행 diff 확인용)

세션 모델은 사용자가 정하지 않았다 — 두 경우를 나란히 계산한다(검수 F1).
  (가) 수동 stop 허용 — 세션 최대 = 발화 수
  (나) 무발화 60초 자동 종료만 — 세션마다 60초 꼬리

실행: python3 calc.py   (레포 루트 기준 경로를 스스로 찾는다)
"""

import itertools
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter, NullFormatter  # noqa: E402

plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = ROOT / "reference" / "2026-11-12-interpreter-idea"
REPORT = OUT / "pricing-design.md"

# ── 근거 표기 ──
T_REAL, T_OFF, T_USER, T_CALC, T_EST, T_CMP, T_OPEN = "〔실측〕", "〔공식〕", "〔사용자 지정〕", "〔계산〕", "〔추정〕", "〔비교용〕", "〔정할 것〕"

# ── 공식 문서(2026-11-12 다시 열어 확인한 실제 주소) ──
PRICING_URL = "https://soniox.com/pricing"
URL_KEEPALIVE = "https://docs.soniox.com/stt/rt/connection-keepalive"
URL_STT_LIMITS = "https://docs.soniox.com/stt/rt/limits-and-quotas"
URL_TTS_LIMITS = "https://docs.soniox.com/tts/rt/limits-and-quotas"
URL_CONTEXT = "https://docs.soniox.com/stt/concepts/context"
URL_MODELS = "https://docs.soniox.com/stt/models"

# ── 공식 단가(USD / 토큰) ──
P_AIN = 2.00e-6    # STT 입력 오디오(실시간)
P_TIN = 4.00e-6    # STT 입력 텍스트(context)
P_TOUT = 4.00e-6   # STT 출력 텍스트(전사 + 번역)
P_TTSIN = 4.00e-6  # TTS 입력 텍스트
P_AOUT = 21.50e-6  # TTS 출력 오디오
AUDIO_TOK_PER_H = 30000  # 공식 환산치: 실시간 오디오 1시간 ≈ 30,000 토큰
A_RATE = AUDIO_TOK_PER_H / 3600  # 토큰/초
STREAM_MAX_MIN = 300  # 공식: STT 스트림 최대 300분(URL_STT_LIMITS)
STT_CONC = 10  # 공식: STT 동시 활성 스트림 10(URL_STT_LIMITS)
TTS_CONC = 3   # 공식: TTS 동시 스트림 3 — 모든 WebSocket 연결 합계(URL_TTS_LIMITS)

# ── 사용자 지정 ──
DAYS = 30
WORK_H = 12
H_RANGE = (1, 12)
D_RANGE = (1, 5)
RHO_RANGE = (0.0, 1.0)
SILENCE_S = 60  # 무발화 1분이면 세션 종료
MARGINS = (0.30, 0.50, 0.70)  # 비교용(사용자가 정하지 않음)
R_CMP = 1400  # 환율 비교용(코디 지시 · 사용자 미정)
REF_KRW = 20000  # 대표 투표 「월 2만원」 — 참고선(입력값으로 쓰지 않는다)

# ── 실측 ──
logs = json.loads((HERE / "usage-logs-cost-probe-2026-11-12.json").read_text())["items"]
ctx = json.loads((HERE / "context-chars.json").read_text())


def pick(ref, model):
    rows = [x for x in logs if x["client_reference_id"] == ref and x["model"] == model]
    assert len(rows) == 1, (ref, model)
    return rows[0]


# 언어쌍은 작성 브리프 §1 · 메모 pricing-function.md §2 의 대응(usage-logs 에는 없다)
CASES = {
    "c": {"name": "상담 1발화", "ref": "cost-probe-2026-11-12-d", "pair": "ko→zh", "lang": "zh"},
    "s": {"name": "간단 통역 1발화", "ref": "cost-probe-2026-11-12-real", "pair": "ko→en", "lang": "en"},
}
for k, c in CASES.items():
    stt, tts = pick(c["ref"], "stt-rt-v5"), pick(c["ref"], "tts-rt-v2")
    c["stt"], c["tts"] = stt, tts
    c["ctx_tok"] = stt["input_text_tokens"]
    c["a_in"] = stt["input_audio_tokens"]
    c["t_out"] = stt["output_text_tokens"]
    c["t_tts"] = tts["input_text_tokens"]
    c["a_tts"] = tts["output_audio_tokens"]
    c["d"] = stt["input_audio_duration_ms"] / 1000  # 발화 하나 연결의 스트림 시간(초)
    c["tts_s"] = tts["output_audio_duration_ms"] / 1000
    c["cost_log"] = float(stt["cost_usd"]) + float(tts["cost_usd"])
    c["cost_fn"] = (P_AIN * c["a_in"] + P_TIN * c["ctx_tok"] + P_TOUT * c["t_out"]
                    + P_TTSIN * c["t_tts"] + P_AOUT * c["a_tts"])
    c["ctx_chars"] = ctx["langs"][c["lang"]]["chars"]
    c["tok_per_char"] = c["ctx_tok"] / c["ctx_chars"]
    # 발화 하나의 변동비(STT 오디오 제외 — 오디오는 스트림 시간으로 따로 셈)
    c["e"] = P_TOUT * c["t_out"] + P_TTSIN * c["t_tts"] + P_AOUT * c["a_tts"]
    c["e_tok"] = c["t_out"] + c["t_tts"] + c["a_tts"]
    c["n_min"] = 3600 / (c["d"] + SILENCE_S)
    c["n_max"] = 3600 / c["d"]

C, S = CASES["c"], CASES["s"]
MAX_LANG = max(ctx["langs"], key=lambda l: ctx["langs"][l]["chars"])
MAX_CHARS = ctx["langs"][MAX_LANG]["chars"]
TPC_MAX = max(C["tok_per_char"], S["tok_per_char"])
TPC_MIN = min(C["tok_per_char"], S["tok_per_char"])
CTX_TOK = round(MAX_CHARS * TPC_MAX)  # 추정
CTX_TOK_LO = round(MAX_CHARS * TPC_MIN)
CTX_USD = CTX_TOK * P_TIN
A_USD_H = AUDIO_TOK_PER_H * P_AIN

# ── 세션 모델 ──
MODELS = {
    "A": ("(가)", "수동 stop 허용 — 세션 최대 = 발화 수"),
    "B": ("(나)", "무발화 60초 자동 종료만"),
}
MSTYLE = {"A": "-", "B": "--"}


def k_min(H):
    return math.ceil(H * 60 / STREAM_MAX_MIN) / H


def per_hour(H, rho, phi, psi, mdl):
    """기기 1대 · 스트림 1시간 원가(USD)와 토큰 수."""
    nc = C["n_min"] + phi * (C["n_max"] - C["n_min"])
    ns = S["n_min"] + phi * (S["n_max"] - S["n_min"])
    n = rho * nc + (1 - rho) * ns
    talk = rho * nc * C["d"] + (1 - rho) * ns * S["d"]  # 시간당 발화 연결이 차지한 초
    km = k_min(H)
    if mdl == "A":
        kx = n
    else:
        kx = max(km, min(n, (3600 - talk) / SILENCE_S))  # 세션마다 60초 꼬리
    k = km + psi * (kx - km)
    cost = A_USD_H + k * CTX_USD + rho * nc * C["e"] + (1 - rho) * ns * S["e"]
    tok = AUDIO_TOK_PER_H + k * CTX_TOK + rho * nc * C["e_tok"] + (1 - rho) * ns * S["e_tok"]
    return {"cost": cost, "tok": tok, "n": n, "k": k, "kx": kx}


def month(v, mdl):
    ph = per_hour(v["H"], v["rho"], v["phi"], v["psi"], mdl)
    hours = DAYS * v["D"] * v["H"]
    return {**ph, "v": v, "hours": hours, "M": ph["cost"] * hours, "TOK": ph["tok"] * hours}


HAPPY = {"H": H_RANGE[0], "D": D_RANGE[0], "rho": RHO_RANGE[0], "phi": 0.0, "psi": 0.0}
WORST = {"H": H_RANGE[1], "D": D_RANGE[1], "rho": RHO_RANGE[1], "phi": 1.0, "psi": 1.0}
SETS = {"happy": ("해피", HAPPY), "worst": ("워스트", WORST)}
VARS = {
    "H": ("하루 실사용 시간 H", "h", [i * 0.5 for i in range(2, 25)]),
    "D": ("동시 사용 대수 D", "대", [1, 2, 3, 4, 5]),
    "rho": ("상담 비율 ρ", "0=간단만 · 1=상담만", [i / 20 for i in range(21)]),
    "phi": ("발화 밀도 φ", "0=공백 최대 · 1=쉼 없음", [i / 20 for i in range(21)]),
    "psi": ("세션 분할 ψ", "0=세션 최소 · 1=세션 최대", [i / 20 for i in range(21)]),
}
VN = {k: v[0] for k, v in VARS.items()}

sweeps = {}
for mdl in MODELS:
    for sk, (_, base) in SETS.items():
        for vk, (_, _, xs) in VARS.items():
            sweeps[(mdl, sk, vk)] = [(x, month({**base, vk: x}, mdl)) for x in xs]

# 전 조합 격자 — 스윕이 놓친 최대를 잡는다(검수 W2)
GRID_AXES = (range(1, 13), range(1, 6), [i / 10 for i in range(11)], [i / 10 for i in range(11)], [i / 10 for i in range(11)])
grid = {mdl: [month({"H": H, "D": D, "rho": r, "phi": f, "psi": p}, mdl) for H, D, r, f, p in itertools.product(*GRID_AXES)]
        for mdl in MODELS}
SWEEP_PTS = {mdl: [r for (m_, _, _), rows in sweeps.items() if m_ == mdl for _, r in rows] for mdl in MODELS}
POINTS = {mdl: SWEEP_PTS[mdl] + grid[mdl] for mdl in MODELS}  # 가격 역산 범위 = 스윕 점 ∪ 격자 점

KEYS = {"ch": lambda r: r["cost"], "M": lambda r: r["M"], "upt": lambda r: r["cost"] / r["tok"]}
TOP = {mdl: {kk: max(POINTS[mdl], key=f) for kk, f in KEYS.items()} for mdl in MODELS}
BOT = {mdl: {kk: min(POINTS[mdl], key=f) for kk, f in KEYS.items()} for mdl in MODELS}
SWEEP_MAX = {mdl: {kk: max(f(r) for r in SWEEP_PTS[mdl]) for kk, f in KEYS.items()} for mdl in MODELS}
GRID_MAX = {mdl: {kk: max(f(r) for r in grid[mdl]) for kk, f in KEYS.items()} for mdl in MODELS}


def vmax(mdl, kk):
    return KEYS[kk](TOP[mdl][kk])


def vmin(mdl, kk):
    return KEYS[kk](BOT[mdl][kk])


def pt(r):
    v = r["v"]
    return f"H {v['H']:g} · D {v['D']:g} · ρ {v['rho']:g} · φ {v['phi']:g} · ψ {v['psi']:g}"


def price(plan, m, mdl):
    if plan == "hour":
        return vmax(mdl, "ch") / (1 - m)
    if plan == "xmult":
        return 1 / (1 - m)
    if plan == "tok":
        return vmax(mdl, "upt") * 1e6 / (1 - m)
    if plan == "flat":
        return vmax(mdl, "M") / (1 - m)
    raise KeyError(plan)


def revenue(plan, p, r):
    if plan == "hour":
        return p * r["hours"]
    if plan == "xmult":
        return p * r["M"]
    if plan == "tok":
        return p * r["TOK"] / 1e6
    if plan == "flat":
        return p
    raise KeyError(plan)


def margin(plan, p, r):
    rv = revenue(plan, p, r)
    return (rv - r["M"]) / rv


PLANS = {"hour": "시간제", "xmult": "토큰제(원가 배수형)", "tok": "토큰제(단일 단가형)", "flat": "정액제(무제한)"}
UNIT = {"hour": "USD / 기기·시간", "xmult": "× Soniox 원가", "tok": "USD / 1M 토큰", "flat": "USD / 계정·월"}
PLAN_KEY = {"hour": "ch", "tok": "upt", "flat": "M"}

# ── 그래프 ──
COL = {"happy": "#2a7de1", "worst": "#d64545"}
PCOL = {"hour": "#2a9d8f", "xmult": "#e9a23b", "tok": "#8e5bd6", "flat": "#555555"}
MCOL = {0.30: "#2a9d8f", 0.50: "#e9a23b", 0.70: "#d64545"}
pngs = []
comma = FuncFormatter(lambda v, _: f"{v:,.0f}")


def krw_axis(ax):
    sec = ax.secondary_yaxis("right", functions=(lambda u: u * R_CMP, lambda w: w / R_CMP))
    sec.set_ylabel(f"원 (r = {R_CMP:,} 비교용)")
    sec.yaxis.set_major_formatter(comma)
    sec.yaxis.set_minor_formatter(NullFormatter())


def save(fig, name):
    p = OUT / name
    fig.savefig(p, dpi=110)
    plt.close(fig)
    pngs.append(p.name)


def fig_cost():
    fig, axes = plt.subplots(1, 5, figsize=(22, 4.8))
    for ax, (vk, (label, unit, _)) in zip(axes, VARS.items()):
        for mdl, (mtag, _) in MODELS.items():
            for sk, (sname, _) in SETS.items():
                rows = sweeps[(mdl, sk, vk)]
                ax.plot([x for x, _ in rows], [r["M"] for _, r in rows], MSTYLE[mdl], marker="o", ms=3,
                        color=COL[sk], label=f"{mtag} 나머지 {sname} 고정")
        ax.set_yscale("log")
        ax.set_xlabel(f"{label} ({unit})")
        ax.set_ylabel("월 원가 (USD, 로그)")
        ax.set_title(label)
        ax.grid(alpha=0.3, which="both")
        ax.legend(fontsize=7)
        krw_axis(ax)
    fig.suptitle("월 원가 — 변인 1개만 움직이고 나머지는 해피 / 워스트 고정 · 실선 (가) 수동 stop 허용 · 점선 (나) 무발화 60초 자동 종료만")
    fig.tight_layout()
    save(fig, "pd-cost-sweeps.png")


def fig_tornado():
    fig, axes = plt.subplots(2, 2, figsize=(14, 7.5))
    for row, (mdl, (mtag, mdesc)) in enumerate(MODELS.items()):
        for col, (sk, (sname, base)) in enumerate(SETS.items()):
            ax = axes[row][col]
            labels = []
            for i, (vk, (label, _, _)) in enumerate(VARS.items()):
                ys = [r["M"] for _, r in sweeps[(mdl, sk, vk)]]
                ax.barh(i, max(ys) - min(ys), left=min(ys), color=COL[sk], alpha=0.7,
                        label="변인 범위의 월 원가 구간" if i == 0 else None)
                labels.append(label)
            ax.axvline(month(base, mdl)["M"], color="k", ls="--", lw=1, label=f"{sname} 세트 월 원가")
            ax.axvline(vmax(mdl, "M"), color="#d64545", ls=":", lw=1.5, label="범위 최대(스윕 ∪ 격자)")
            ax.set_yticks(range(len(labels)), labels)
            ax.set_xscale("log")
            ax.set_xlabel("월 원가 (USD, 로그)")
            ax.set_title(f"{mtag} {mdesc} · 나머지 {sname} 고정", fontsize=10)
            ax.grid(alpha=0.3, axis="x", which="both")
            ax.legend(fontsize=7, loc="lower right")
    fig.suptitle("어느 변인이 월 원가를 가장 크게 흔드나")
    fig.tight_layout()
    save(fig, "pd-tornado.png")


def fig_rev(sk, m=0.5):
    sname, _ = SETS[sk]
    fig, axes = plt.subplots(2, 5, figsize=(22, 9))
    for row, (mdl, (mtag, mdesc)) in enumerate(MODELS.items()):
        for ax, (vk, (label, unit, _)) in zip(axes[row], VARS.items()):
            rows = sweeps[(mdl, sk, vk)]
            xs = [x for x, _ in rows]
            ax.plot(xs, [r["M"] for _, r in rows], "-", color="k", lw=2.2, label="월 원가")
            for pk, pname in PLANS.items():
                p = price(pk, m, mdl)
                ys = [revenue(pk, p, r) for _, r in rows]
                if pk == "flat":  # 시간제와 겹치는 자리가 있어 굵은 반투명 띠로 그린다(검수 W7)
                    ax.plot(xs, ys, "-", color=PCOL[pk], lw=7, alpha=0.3, label=f"{pname} 매출(굵은 띠)")
                elif pk == "hour":
                    ax.plot(xs, ys, "--", color=PCOL[pk], lw=1.6, marker="^", ms=4, label=f"{pname} 매출(▲)")
                else:
                    ax.plot(xs, ys, "--", color=PCOL[pk], lw=1.4, label=f"{pname} 매출")
            ax.set_yscale("log")
            ax.set_xlabel(f"{label} ({unit})")
            ax.set_ylabel("월 금액 (USD, 로그)")
            ax.set_title(f"{mtag} {label}", fontsize=10)
            ax.grid(alpha=0.3, which="both")
            ax.legend(fontsize=6.5, loc="best", framealpha=0.6)
            krw_axis(ax)
    fig.suptitle(f"매출 vs 원가 — 나머지 {sname} 고정 · 가격 = 마진 m = {int(m * 100)}% 역산값(비교용) · "
                 "윗줄 (가) 수동 stop 허용 · 아랫줄 (나) 무발화 60초 자동 종료만")
    fig.tight_layout()
    save(fig, f"pd-rev-{sk}.png")


def fig_unit():
    """단위당 원가 — 시간제 · 단일 단가 토큰제가 무엇에 깨지나(손익분기 = 가격선)."""
    fig, axes = plt.subplots(4, 5, figsize=(22, 15))
    specs = []
    for mdl in MODELS:
        specs.append((mdl, lambda r: r["cost"], "스트림 1시간 원가 (USD)", "hour"))
        specs.append((mdl, lambda r: r["cost"] / r["tok"] * 1e6, "1M 토큰당 원가 (USD)", "tok"))
    for row, (mdl, key, ylab, pk) in enumerate(specs):
        mtag = MODELS[mdl][0]
        for col, (vk, (label, unit, _)) in enumerate(VARS.items()):
            ax = axes[row][col]
            for sk, (sname, _) in SETS.items():
                rows = sweeps[(mdl, sk, vk)]
                ax.plot([x for x, _ in rows], [key(r) for _, r in rows], "-o", ms=3, color=COL[sk],
                        label=f"원가 · 나머지 {sname} 고정")
            ax.axhline(price(pk, 0.0, mdl), color="k", ls=":", lw=1.2, label="손익분기 가격(m = 0)")
            ax.axhline(price(pk, 0.5, mdl), color=PCOL[pk], ls="--", lw=1.2, label="m = 50% 가격(비교용)")
            ax.set_xlabel(f"{label} ({unit})")
            ax.set_ylabel(ylab)
            ax.set_title(f"{mtag} {'시간제 단위' if pk == 'hour' else '토큰제 단일 단가 단위'} · {label}", fontsize=9)
            ax.grid(alpha=0.3)
            ax.legend(fontsize=6.5)
    fig.suptitle("단위당 원가 vs 가격선 — 가격선은 범위 최대(스윕 ∪ 격자)에서 역산 · 1·2줄 (가) 수동 stop 허용 · 3·4줄 (나) 무발화 60초 자동 종료만")
    fig.tight_layout()
    save(fig, "pd-unit-cost.png")


def fig_flat_q():
    qs = [10 ** (i / 20) for i in range(-20, 66)]  # 0.1 ~ 약 1,778 h(계정 월 최대 30 × 5 × 12 = 1,800 h)
    fig, ax = plt.subplots(figsize=(10, 5.6))
    for mdl, (mtag, _) in MODELS.items():
        for m in MARGINS:
            ax.plot(qs, [q * vmax(mdl, "ch") / (1 - m) for q in qs], MSTYLE[mdl], color=MCOL[m],
                    label=f"{mtag} 최저 월 가격 · m = {int(m * 100)}%(비교용)")
    ax.axhline(REF_KRW / R_CMP, color="k", ls=":", lw=1.8, label=f"월 2만원 참고선(r = {R_CMP:,} 비교용)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,g}"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,g}"))
    ax.set_xlabel("포함량 Q (계정 월 스트림 시간, h, 로그)")
    ax.set_ylabel("정액 월 가격 p_f (USD, 로그)")
    ax.set_title("정액제 + 포함량 — 포함량을 시간으로 잡을 때의 최저 월 가격 · 실선 (가) · 점선 (나)")
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8, loc="upper left")
    krw_axis(ax)
    fig.tight_layout()
    save(fig, "pd-flat-q.png")


fig_cost()
fig_tornado()
fig_rev("happy")
fig_rev("worst")
fig_unit()
fig_flat_q()


# ── 보고서 ──
def u(x, nd=4):
    return f"${x:,.{nd}f}"


def w(x):
    return f"{x * R_CMP:,.0f}원"


L = []
add = L.append
MA, MB = MODELS["A"][0], MODELS["B"][0]
WA, WB = month(WORST, "A"), month(WORST, "B")
HP = month(HAPPY, "A")
assert abs(HP["M"] - month(HAPPY, "B")["M"]) < 1e-12  # 해피 세트는 ψ = 0 → 두 모델 같음

add("# 통키 요금제 설계 — 원가 범위에서 가격을 역산한다")
add("")
add(f"- 작성 2026-11-12 · 실측 조회일 2026-11-12(UTC) · 단가 출처 {PRICING_URL} 〔공식〕")
add("- 숫자 · 그래프는 전부 `orchestration/work/interpreter-idea/pricing-calc/calc.py` 가 뽑았다(손 편집 없음). 〔메타〕")
add(f"- 근거 표기: {T_REAL} Soniox usage-logs · {T_OFF} Soniox 문서 · {T_USER} 사용자가 정한 값 · {T_CALC} 식을 같이 적음 · "
    f"{T_EST} 추정(식과 가정을 적음) · {T_CMP} 비교용(사용자 미정) · {T_OPEN} 근거 없음 · 사용자가 고를 해석. 〔메타〕")
add(f"- 금액은 **USD 로 계산**한다. 원 환산은 환율 r {T_OPEN} — 표의 원 열은 r = {R_CMP:,} {T_CMP}. 〔메타〕")
add("- 특정 병원 · 지점 데이터는 쓰지 않았다. 실사용 패턴 데이터는 없다 — 극값 차이를 그대로 둔다. 〔메타〕")
add("")

# §0 결론(추가 지시 2 — 추천 1개 · 가격 · 이유 · 실제 청구 · 기대는 가정)
M0 = 0.50  # 결론이 가정한 마진율(사용자 미정 → 비교용 셋 중 가운데)
X0 = price("xmult", M0, "A")
add("## 0. 결론")
add("")
add(f"**추천: 토큰제(원가 배수형) — 월 청구 = 그 계정의 그 달 Soniox 원가 × {X0:.2f}** (마진 m = {int(M0 * 100)}% 가정 {T_CMP}). "
    f"고객에게 보이는 값으로 바꾸면 (나) 기준 스트림 1시간당 {u(X0 * vmin('A', 'ch'), 2)} ~ {u(X0 * vmax('B', 'ch'), 2)}({w(X0 * vmin('A', 'ch'))} ~ {w(X0 * vmax('B', 'ch'))}) · "
    f"수동 stop 을 허용하면 최대 {u(X0 * vmax('A', 'ch'), 2)}({w(X0 * vmax('A', 'ch'))}) {T_CALC} §3 1시간 원가 × {X0:.2f} · 원 r = {R_CMP:,} {T_CMP}.")
add("")
add("**왜 이 안인가**")
add("")
add(f"- 시간제는 단가를 범위 최악 1시간 원가에 묶어야 해서 가벼운 고객이 원가의 수십 배를 낸다: 해피 고객 월 {u(revenue('hour', price('hour', M0, 'A'), HP), 2)}({w(revenue('hour', price('hour', M0, 'A'), HP))}) vs 원가 {u(HP['M'], 2)}({w(HP['M'])}) — "
    f"× {revenue('hour', price('hour', M0, 'A'), HP) / HP['M']:.0f} · (나) 로 매겨도 × {revenue('hour', price('hour', M0, 'B'), HP) / HP['M']:.0f} {T_CALC} §7. 단가를 낮추면 ρ · φ · ψ 를 조금만 움직여도 적자다(§5 손익분기 표).")
add(f"- 정액제(무제한)는 범위 최대를 견디는 값이 월 {u(price('flat', M0, 'A'), 2)}((가)) · {u(price('flat', M0, 'B'), 2)}((나)) 라 해피 고객 원가({u(HP['M'], 2)})와 수천 배 차이 {T_CALC} §6. "
    f"단일 토큰 단가형은 마진이 {margin('tok', price('tok', M0, 'A'), min(POINTS['A'], key=lambda r: margin('tok', price('tok', M0, 'A'), r))) * 100:.0f} ~ {margin('tok', price('tok', M0, 'A'), HP) * 100:.0f}% 로 흔들리고 해피 고객 청구가 배수형의 × {revenue('tok', price('tok', M0, 'A'), HP) / revenue('xmult', X0, HP):.2f} {T_CALC} §7.")
add(f"- 원가 배수형은 **범위 안 모든 점에서 마진이 정확히 {int(M0 * 100)}%** 이고, 미정 가정 (가)/(나) · 「1시간」 정의 · context 과금 방식이 바뀌어도 배수 × {X0:.2f} 는 그대로다 — 바뀌는 건 청구액뿐 {T_CALC} §4. 단점: 고객이 월 청구액을 미리 알기 어렵다.")
add("")
add(f"**그 가격에서 고객이 실제로 내는 돈** — 월 · 계정 하나 {T_CALC} · 원 r = {R_CMP:,} {T_CMP}")
add("")
add("| 고객 | 세션 모델 | 조건 | 월 원가 | 월 청구 | 마진 | 근거 |")
add("|---|---|---|--:|--:|--:|---|")
for label, getr in [("해피 세트", lambda mdl: month(HAPPY, mdl)), ("워스트 세트", lambda mdl: month(WORST, mdl)), ("원가 최대 지점", lambda mdl: TOP[mdl]["M"])]:
    for mdl, (mtag, _) in MODELS.items():
        r = getr(mdl)
        rv = revenue("xmult", X0, r)
        add(f"| {label} | {mtag} | {pt(r)} | {u(r['M'], 2)} ({w(r['M'])}) | {u(rv, 2)} ({w(rv)}) | {margin('xmult', X0, r) * 100:.1f}% | {T_CALC} · 원 {T_CMP} |")
add("")
add("**이 결론이 기대는 가정 — 바뀌면 어떻게 되나**")
add("")
add("| 가정(사용자 미정) | 결론에 넣은 값 | 바뀌면 | 근거 |")
add("|---|---|---|---|")
add(f"| 세션 상한 §8 #1 | 무관 — 두 경우 나란히 | 배수는 그대로 {X0:.2f}. 원가 최대 고객 청구만 (가) {u(X0 * vmax('A', 'M'), 2)} / (나) {u(X0 * vmax('B', 'M'), 2)} 월 · "
    f"(참고: 시간제였다면 단가 (가) {u(price('hour', M0, 'A'), 4)} / (나) {u(price('hour', M0, 'B'), 4)} / h) | {T_OPEN} · {T_CALC} |")
add(f"| 「실사용 1시간」 기준 §8 #2 | 무관 — 원가로 청구 | 배수 · 청구 그대로. 시간제를 고를 때만 과금 시간 단위가 갈린다 | {T_OPEN} · {T_CALC} §2 |")
add(f"| 마진율 m | {int(M0 * 100)}% {T_CMP} | m = 30 · 50 · 70% 이면 배수 " + " · ".join(f"× {price('xmult', m, 'A'):.2f}" for m in MARGINS) + f" · 해피 청구 " + " · ".join(w(revenue('xmult', price('xmult', m, 'A'), HP)) for m in MARGINS) + f" | {T_OPEN} · {T_CALC} |")
add(f"| 환율 r | {R_CMP:,} {T_CMP} | USD 청구는 그대로 · 원 금액만 r 에 비례 | {T_OPEN} |")
add(f"| 토큰제의 뜻 §8 #4 | 원가 배수형 | 「토큰제 = 단일 토큰 단가」로 정하면 이 결론 대신 1M 토큰당 {u(price('tok', M0, 'A'), 3)} — 위 둘째 이유의 마진 흔들림을 받아들여야 한다 | {T_OPEN} · {T_CALC} |")
add(f"| 무발화 1분 종료 구현 §8 #5 | 구현 뒤 범위 {T_USER} | 미구현이면 멈춘 시간도 원가 → 청구가 같이 늘지만 마진 {int(M0 * 100)}% 는 유지(배수형이라) | {T_CALC} |")
add(f"| 계정별 원가 측정 | 가능하다고 가정 | 원가 배수형은 계정마다 Soniox 원가를 갈라 재야 한다 — usage-logs 의 `client_reference_id` 에 계정을 넣어야 하고 지금 넣고 있는지는 확인 안 함 | {T_OPEN} §8 #7 |")
add("")
add(f"- 2만원 투표와의 관계: 이 가격에서 해피 고객은 월 {w(revenue('xmult', X0, HP))} 으로 2만원 아래 · 사용량이 늘면 2만원을 넘는다 — 「월 2만원 고정」은 범위 안 원가를 견디지 못한다(정액제 최저가 §6) {T_CALC} · 원 {T_CMP}.")
add(f"- 청구액 예측이 꼭 필요하면 다음 후보는 안 C(정액 + 원가 크레딧 포함량)다 — 이번 판에서는 계산하지 않았다 {T_OPEN} §8 #4.")
add("")

# 요약
bA, bB = TOP["A"]["ch"], TOP["B"]["ch"]
add("## 요약")
add("")
add(f"- 기호: H 하루 실사용 시간 · D 동시 사용 대수 · ρ 상담 비율 — {T_USER}. "
    f"φ 발화 밀도(0 = 발화 사이 공백 60초 직전 · 1 = 쉼 없음) · ψ 세션 분할(0 = 세션 수 하한 · 1 = 상한)은 사용자가 정한 변인이 아니라 **계산으로 끌어낸 변인**이다 {T_CALC} §2.")
add(f"- **가격을 정하는 건 세션 모델이다 — 사용자가 아직 고르지 않았다** {T_OPEN} §8 #1. "
    f"{MA} 수동 stop 허용이면 스트림 1시간 원가 최대 {u(vmax('A', 'ch'))}({pt(bA)}) · "
    f"{MB} 무발화 60초 자동 종료만이면 {u(vmax('B', 'ch'))}({pt(bB)}) — × {vmax('A', 'ch') / vmax('B', 'ch'):.1f} {T_CALC} §5.")
add(f"- **사용자 워스트 세트는 원가 최대가 아니다.** 워스트 세트 월 원가 {MA} {u(WA['M'], 2)} · {MB} {u(WB['M'], 2)} — "
    f"범위 최대는 {MA} {u(vmax('A', 'M'), 2)}(× {vmax('A', 'M') / WA['M']:.2f}, {pt(TOP['A']['M'])}) · "
    f"{MB} {u(vmax('B', 'M'), 2)}(× {vmax('B', 'M') / WB['M']:.2f}, {pt(TOP['B']['M'])}) {T_CALC} §3. 가격은 세트가 아니라 범위 최대에서 역산했다.")
add(f"- 가격을 가르는 미정 해석: 세션 상한 {T_OPEN} §8 #1 · 「실사용 1시간」의 기준 {T_OPEN} §8 #2 · 세션 하한(300분 연속) {T_OPEN} §8 #3 · "
    f"토큰제의 뜻 {T_OPEN} §8 #4 · 마진 m · 환율 r {T_OPEN}.")
add(f"- **이 범위는 무발화 1분 종료 {T_USER} 가 구현된 뒤의 범위다.** 통키 main `17c26b5` 에는 아직 없다 — 멈춤 중에도 keepalive 로 STT 를 열어 둔다(§8 #5). "
    f"지금 그대로면 멈춘 시간도 스트림 시간당 {u(A_USD_H)} 이상 과금되어 §3 범위 밖이다 {T_OFF} {URL_KEEPALIVE}.")
add("")

# §1
add("## 1. 원가 함수")
add("")
add("### 1.1 단가")
add("")
add("| 과금 항목 | 단가(USD / 1M 토큰) | 기호 | 근거 |")
add("|---|--:|---|---|")
for name, p, sym in [("STT 입력 오디오(실시간)", P_AIN, "P_ain"), ("STT 입력 텍스트(context)", P_TIN, "P_tin"),
                     ("STT 출력 텍스트(전사 + 번역)", P_TOUT, "P_tout"), ("TTS 입력 텍스트", P_TTSIN, "P_ttsin"),
                     ("TTS 출력 오디오", P_AOUT, "P_aout")]:
    add(f"| {name} | {p * 1e6:.2f} | {sym} | {T_OFF} {PRICING_URL} |")
add(f"| 실시간 오디오 토큰 환산 | {AUDIO_TOK_PER_H:,} 토큰 / 시간 = {A_RATE:.4f} 토큰 / 초 | a | {T_OFF} 같은 페이지 환산치 · 초당 값은 {T_CALC} {AUDIO_TOK_PER_H:,} ÷ 3,600 |")
add("")
add(f"- STT 는 스트림이 열린 전체 시간을 과금한다 {T_OFF} {URL_KEEPALIVE}")
add(f"- STT 스트림 최대 {STREAM_MAX_MIN}분 · 동시 활성 스트림 {STT_CONC} {T_OFF} {URL_STT_LIMITS}")
add(f"- TTS 동시 스트림 {TTS_CONC}(모든 WebSocket 연결 합계) {T_OFF} {URL_TTS_LIMITS}")
add(f"- context 는 세션 시작 때 한 번 보내고 세션 내내 쓴다 {T_OFF} {URL_CONTEXT}")
add("")
add("### 1.2 식")
add("")
add("```text")
add("cost_usd = P_ain·A_in + P_tin·T_ctx + P_tout·T_out + P_ttsin·T_tts + P_aout·A_tts      〔공식 단가 × 토큰〕")
add("  A_in  = STT 입력 오디오 토큰 = a × 스트림 시간(초)                                   〔공식〕")
add("  T_ctx = context 토큰 — 세션 시작 때 1회 보낸다                                      〔공식 — context 문서〕")
add("          연결이 여러 번일 때 매번 같은 양이 잡히는지는 실측 2건(각 연결 1회)으로 못 보임  〔정할 것 — §8 #8〕")
add("  T_out = 전사 + 번역 토큰 · T_tts = TTS 입력 토큰 · A_tts = TTS 출력 오디오 토큰")
add("cost_krw = r × cost_usd      r = 환율                                                  〔정할 것〕")
add("```")
add("")
add("### 1.3 실측 2건 대입 — 함수 = 청구액")
add("")
add("| 케이스 | client_reference_id | 언어쌍 | T_ctx | A_in | T_out | T_tts | A_tts | 스트림(초) | TTS 음성(초) | 함수 계산 | 로그 cost_usd(STT + TTS) | 차이 | 근거 |")
add("|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|")
for c in (C, S):
    add(f"| {c['name']} | `{c['ref']}` | {c['pair']} | {c['ctx_tok']:,} | {c['a_in']:,} | {c['t_out']:,} | "
        f"{c['t_tts']:,} | {c['a_tts']:,} | {c['d']:.3f} | {c['tts_s']:.3f} | {u(c['cost_fn'], 7)} | {u(c['cost_log'], 7)} | "
        f"{c['cost_fn'] - c['cost_log']:.1e} | 토큰 · 시간 · cost_usd {T_REAL} · 함수 계산 {T_CALC} §1.2 식 |")
add("")
add("- 케이스 이름 · 언어쌍은 usage-logs 에 없다 — 작성 브리프 §1 과 실측 문장 메모(`pricing-function.md` §2)의 대응을 옮겼다. 메모의 글자 수는 계산에 쓰지 않아 싣지 않는다.")
add(f"- 오디오 환산 확인: 상담 {C['a_in']} ÷ {C['d']:.3f} = {C['a_in'] / C['d']:.3f} 토큰 / 초 · 간단 {S['a_in']} ÷ {S['d']:.3f} = {S['a_in'] / S['d']:.3f} 토큰 / 초 — 공식 {A_RATE:.3f} 와 맞다 {T_CALC}.")
add(f"- `…-synth` 항목(입력 음성 합성)은 원가가 아니라 뺐다 {T_REAL}. 원시 응답: `pricing-calc/usage-logs-cost-probe-2026-11-12.json` (키 없음).")
add("")
add("### 1.4 연결 고정비 — context 가 가장 큰 언어로 통일")
add("")
add(f"글자 수는 통키 main `17c26b5` 의 `glossary.build_context` + `context_size`(언어별 줄이기 기준 `langs.CONTEXT_MAX_CHARS` 적용)로 셌다 — 시드 `{ctx['seed_version']}` {T_CALC} `pricing-calc/count_context.py`.")
add("")
add("| 언어 | context 글자 | context 토큰 | 글자당 토큰 | 근거 |")
add("|---|--:|--:|--:|---|")
for lang, info in ctx["langs"].items():
    if lang == C["lang"]:
        add(f"| {lang} | {info['chars']:,} | {C['ctx_tok']:,} | {C['tok_per_char']:.4f} | 글자 {T_CALC} 코드 · 토큰 {T_REAL} `{C['ref']}` · 글자당 {T_CALC} 토큰 ÷ 글자 |")
    elif lang == S["lang"]:
        add(f"| {lang} | {info['chars']:,} | {S['ctx_tok']:,} | {S['tok_per_char']:.4f} | 글자 {T_CALC} 코드 · 토큰 {T_REAL} `{S['ref']}` · 글자당 {T_CALC} 토큰 ÷ 글자 |")
    elif lang == MAX_LANG:
        add(f"| **{lang} (최대)** | **{info['chars']:,}** | **≈ {CTX_TOK:,}** | {TPC_MAX:.4f} | 글자 {T_CALC} 코드 · 토큰 {T_EST} {info['chars']:,} × {TPC_MAX:.4f}(실측 언어 중 큰 글자당 토큰) |")
    else:
        add(f"| {lang} | {info['chars']:,} | — | — | 글자 {T_CALC} 코드 · 토큰 실측 없음 {T_OPEN} |")
add("")
add(f"- 최대 언어 = **{MAX_LANG}** {T_CALC}(글자 수 최대). 토큰은 실측 두 언어 글자당 토큰 중 큰 값({C['lang']} {TPC_MAX:.4f})을 썼다 {T_EST}. 작은 값({S['lang']} {TPC_MIN:.4f})이면 {CTX_TOK_LO:,} 토큰 {T_EST}.")
add(f"- **연결 고정비 C = {CTX_TOK:,} × P_tin = {u(CTX_USD, 6)} ({w(CTX_USD)})** {T_EST}(원은 r = {R_CMP:,} {T_CMP}).")
add(f"- {MAX_LANG} 는 시드 전체가 기준을 넘어 줄여 보낸다(빠진 칸: terms {ctx['langs'][MAX_LANG]['dropped_terms']} · 역방향 별칭 {ctx['langs'][MAX_LANG]['dropped_reverse_alias']}) {T_CALC} 코드.")
add("")
add("### 1.5 스트림 1시간 원가 식")
add("")
add("발화 하나의 변동비 — STT 오디오는 스트림 시간으로 따로 세므로 뺀다:")
add("")
add("| 케이스 | e = P_tout·T_out + P_ttsin·T_tts + P_aout·A_tts | 토큰 합 T_out + T_tts + A_tts | 근거 |")
add("|---|--:|--:|---|")
for c in (C, S):
    add(f"| {c['name']} | {u(c['e'], 7)} ({w(c['e'])}) | {c['e_tok']:,} | {T_CALC} §1.3 실측 토큰 × 공식 단가 · 원 {T_CMP} |")
add("")
add("```text")
add("기기 1대 · 스트림 1시간 원가(USD)                                                       〔계산〕")
add("  c_h = a·3600·P_ain + k·C + ρ·n_c·e_c + (1 − ρ)·n_s·e_s                               〔계산 — 3600 = 초 / 시간〕")
add(f"      = {u(A_USD_H, 4)} + k·{u(CTX_USD, 6)} + ρ·n_c·{u(C['e'], 7)} + (1 − ρ)·n_s·{u(S['e'], 7)}      〔계산 — 위 표 · §1.4〕")
add("  k = 시간당 세션(연결) 수 · n_c, n_s = 상담 · 간단 시간당 발화 수 · ρ = 상담 비율 — §2")
add("월 원가 M = 30 × D × H × c_h      (H = 하루 스트림 시간 — 해석은 §2)                      〔계산 · 30일 사용자 지정〕")
add("```")
add("")

# §2
add("## 2. 변인 정의와 범위")
add("")
add(f"**「실사용 1시간」의 기준 — 두 해석** {T_OPEN} §8 #2. 사용자가 정한 것은 「하루 실사용 시간 1 ~ 12h」 {T_USER} 뿐이다.")
add("")
add("| 해석 | 「실사용 1시간」 | 원가 시계와의 관계 | 근거 |")
add("|---|---|---|---|")
add(f"| (i) 스트림 시간 | 기기 1대의 STT 스트림이 열린 1시간 | 원가 시계와 같다 — Soniox 가 이 시간 전체를 과금 {T_OFF} | {T_OPEN} 해석 |")
add(f"| (ii) 앱 사용 시간 | 근무 중 통역 앱을 켜 둔 1시간 | 스트림 시간 = σ × 앱 시간 · σ ∈ (0, 1] — 무발화 60초 {T_USER} 를 넘는 쉼은 스트림에서 빠진다 | {T_OPEN} 해석 · σ 데이터 없음 |")
add("")
add(f"- 아래 계산의 H · 시간은 **스트림 시간**으로 넣었다. 해석 (i) 이면 그대로, (ii) 이면 σ = 1 일 때와 같다 {T_CALC}.")
add(f"- 갈리는 숫자: (ii) 에서 앱 1시간 원가 = σ · c_h ≤ c_h 라 **원가 최대(§5 가격 역산)는 두 해석에서 같다**(쉼 없이 쓰면 σ = 1) {T_CALC}. "
    f"**원가 최소 · 해피 쪽(§3 최소 · §7 해피 마진)은 (ii) 에서 σ 배로 더 낮다** — σ 값이 없어 숫자를 낼 수 없다 {T_OPEN}.")
add("")
add("**실측에서 끌어낸 상수**")
add("")
add("| 값 | 상담 | 간단 통역 | 근거 |")
add("|---|--:|--:|---|")
add(f"| 발화 하나 연결의 스트림 시간 d(초) | {C['d']:.3f} | {S['d']:.3f} | {T_REAL} 실측 1회 STT `input_audio_duration_ms`. 그 안의 말 · 번역 · TTS 재생 · 앞뒤 공백 내역은 로그에 없다 {T_OPEN} §8 #10 |")
add(f"| 시간당 발화 최소 n_min = 3600 ÷ (d + 60) | {C['n_min']:.2f} | {S['n_min']:.2f} | {T_CALC} 발화 사이 공백 < 60초(무발화 1분 종료 {T_USER}) |")
add(f"| 시간당 발화 최대 n_max = 3600 ÷ d | {C['n_max']:.2f} | {S['n_max']:.2f} | {T_CALC} 공백 0 |")
add("")
add("**변인 표** — 해피 · 워스트 세트는 사용자 지정 세트(H · D · ρ) + φ · ψ 의 양 끝이다. "
    "세트의 원가가 범위의 최소 · 최대라는 뜻은 **아니다**(요약 · §3 ⚠).")
add("")
add("| 변인 | 정의 | 해피 | 워스트 | 근거 |")
add("|---|---|--:|--:|---|")
add(f"| H 하루 실사용 시간 | 기기 1대의 하루 스트림 시간(h) · 근무 {WORK_H}h 안 — 해석은 위 | {H_RANGE[0]} | {H_RANGE[1]} | {T_USER} · 스트림 시간으로 읽은 것은 {T_OPEN} §8 #2 |")
add(f"| D 동시 사용 대수 | 같은 계정에서 동시에 쓰는 기기 | {D_RANGE[0]} | {D_RANGE[1]} | {T_USER} · Soniox 한도는 STT {STT_CONC} · TTS {TTS_CONC}(계정 전체) {T_OFF} — D = 4 · 5 가 TTS 한도 안인지는 {T_OPEN} §8 #9 |")
add(f"| ρ 상담 비율 | 스트림 시간 중 상담 발화 시간의 비율(0 = 간단만 · 1 = 상담만) | {RHO_RANGE[0]:.0f} | {RHO_RANGE[1]:.0f} | {T_USER}(0 : 100) · 「시간 기준」은 해석 {T_OPEN} §8 #6 |")
add(f"| φ 발화 밀도 — 계산으로 끌어낸 변인(사용자 지정 아님) | n = n_min + φ·(n_max − n_min) · 0 = 공백 60초 직전까지 · 1 = 쉼 없음 | 0 | 1 | {T_CALC} 위 상수 |")
add(f"| ψ 세션 분할 — 계산으로 끌어낸 변인(사용자 지정 아님) | k = k_min + ψ·(k_max − k_min) · 0 = 세션 최소 · 1 = 세션 최대 | 0 | 1 | {T_CALC} 아래 식 · k_min · k_max 는 {T_OPEN} §8 #1 · #3 |")
add("")
add("```text")
add(f"k_min(H) = ⌈H × 60 ÷ {STREAM_MAX_MIN}⌉ ÷ H     스트림 최대 {STREAM_MAX_MIN}분에서 낸 하루 최소 세션 수 ÷ H      〔공식 한도 · 계산〕")
add(f"           H = 1 → {k_min(1):.2f} · H = 5 → {k_min(5):.2f} · H = 12 → {k_min(12):.2f} (⌈·⌉ 때문에 H 에 단조 아님)       〔계산〕")
add("           이 하한까지 세션을 끊지 않고 연다(ψ = 0)는 것은 사용 가정                            〔정할 것 — §8 #3〕")
add("세션 상한 k_max — 사용자가 정하지 않았다. 두 경우를 나란히 계산한다                          〔정할 것 — §8 #1〕")
add("  (가) 수동 stop 허용         k_max = n            발화마다 stop 후 재연결")
add("  (나) 무발화 60초 자동 종료만  k_max = max(k_min, min(n, (3600 − t) ÷ 60))   t = 시간당 발화 연결 초    〔계산 · 60초 사용자 지정〕")
add("        φ = 0 이면 k_max = n_min · φ = 1(쉼 없음)이면 끊을 틈이 없어 k_max = k_min            〔계산〕")
add("```")
add("")
for sk, (sname, base) in SETS.items():
    parts = []
    for mdl, (mtag, _) in MODELS.items():
        r = month(base, mdl)
        parts.append(f"{mtag} 세션 {r['k']:.2f} · c_h {u(r['cost'], 4)} · 월 원가 {u(r['M'], 2)} ({w(r['M'])})")
    r0 = month(base, "A")
    add(f"- **{sname} 세트**: H {base['H']} · D {base['D']} · ρ {base['rho']:.0f} · φ {base['phi']:.0f} · ψ {base['psi']:.0f} → "
        f"시간당 발화 {r0['n']:.2f} · " + " / ".join(parts) + f" {T_CALC} §1.5 식 · 원 {T_CMP}")
add("")

# §3
add("## 3. 원가 범위")
add("")
add(f"변인 하나만 움직이고 나머지는 해피 / 워스트 세트에 고정한 월 원가(계정 하나 = D 대) 구간 {T_USER} 분석 방법 · 세션 모델 (가) · (나) 나란히.")
add("")
add("![월 원가 스윕](pd-cost-sweeps.png)")
add("")
add("| 세션 모델 | 고정 세트 | 움직인 변인 | 범위 | 월 원가 최소(USD) | 최소 지점 | 월 원가 최대(USD) | 최대 지점 | 최대 ÷ 최소 | 최소(원) | 최대(원) | 근거 |")
add("|---|---|---|---|--:|--:|--:|--:|--:|--:|--:|---|")
spread = {}
for mdl, (mtag, _) in MODELS.items():
    for sk, (sname, _) in SETS.items():
        for vk, (label, unit, xs) in VARS.items():
            rows = sweeps[(mdl, sk, vk)]
            lo = min(rows, key=lambda t: t[1]["M"])
            hi = max(rows, key=lambda t: t[1]["M"])
            spread[(mdl, sk, vk)] = hi[1]["M"] / lo[1]["M"]
            add(f"| {mtag} | {sname} | {label} | {xs[0]:g} ~ {xs[-1]:g} | {u(lo[1]['M'], 2)} | {lo[0]:g} | {u(hi[1]['M'], 2)} | {hi[0]:g} | "
                f"{spread[(mdl, sk, vk)]:.2f} | {w(lo[1]['M'])} | {w(hi[1]['M'])} | {T_CALC} §1.5 식 · 원 {T_CMP} |")
add("")
add("![변인별 흔들림](pd-tornado.png)")
add("")
for mdl, (mtag, _) in MODELS.items():
    for sk, (sname, _) in SETS.items():
        order = sorted(VARS, key=lambda vk: -spread[(mdl, sk, vk)])
        add(f"- {mtag} 나머지 {sname} 고정에서 흔드는 순서: " + " > ".join(f"{VN[vk]}(× {spread[(mdl, sk, vk)]:.2f})" for vk in order) + f" {T_CALC}")
for mdl, (mtag, mdesc) in MODELS.items():
    rho_w = sweeps[(mdl, "worst", "rho")]
    phi_w = sweeps[(mdl, "worst", "phi")]
    add(f"- ⚠ {mtag} 나머지 워스트 고정: ρ = 0 에서 {u(rho_w[0][1]['M'], 2)} · ρ = 1 에서 {u(rho_w[-1][1]['M'], 2)} · "
        f"φ = 0 에서 {u(phi_w[0][1]['M'], 2)} · φ = 1 에서 {u(phi_w[-1][1]['M'], 2)} {T_CALC} — 사용자 워스트 세트(ρ = 1 · φ = 1)가 원가 높은 쪽이 아닌 변인이 있다.")
add(f"- 이유 {T_CALC}: 간단 통역은 발화가 짧아 시간당 발화 · 세션이 많고, 세션마다 연결 고정비 C 가 붙는다. "
    f"{MB} 에서는 쉼 없이 말할수록(φ → 1) 세션을 끊을 60초 틈이 없어 세션 상한이 줄어든다(§2 식).")
for mdl, (mtag, _) in MODELS.items():
    add(f"- {mtag} 전체 범위(스윕 ∪ 격자): 월 원가 {u(vmin(mdl, 'M'), 2)} ~ {u(vmax(mdl, 'M'), 2)} (× {vmax(mdl, 'M') / vmin(mdl, 'M'):,.0f}) · "
        f"스트림 1시간 원가 {u(vmin(mdl, 'ch'), 4)} ~ {u(vmax(mdl, 'ch'), 4)} (× {vmax(mdl, 'ch') / vmin(mdl, 'ch'):.1f}) {T_CALC}.")
    add(f"- {mtag} 스윕 최대 vs 전 조합 격자(H 1 ~ 12 · D 1 ~ 5 · ρ · φ · ψ 0.1 간격, {len(grid[mdl]):,}점) 최대: "
        f"1시간 원가 {u(SWEEP_MAX[mdl]['ch'], 4)} vs {u(GRID_MAX[mdl]['ch'], 4)} · 월 원가 {u(SWEEP_MAX[mdl]['M'], 2)} vs {u(GRID_MAX[mdl]['M'], 2)} · "
        f"토큰당 {u(SWEEP_MAX[mdl]['upt'] * 1e6, 3)} vs {u(GRID_MAX[mdl]['upt'] * 1e6, 3)} / 1M {T_CALC}. 가격 역산은 둘 중 큰 값(§5).")
add("")

# §4
add("## 4. 요금제 구조 정의")
add("")
add("가격은 변수 p. 매출 R 은 계정 하나 · 월 기준.")
add("")
add("| 요금제 | 과금 단위 | 매출 공식 | 원가 대비 | 근거 |")
add("|---|---|---|---|---|")
add(f"| 시간제 | 기기·실사용 1시간 — 해석 (i) 스트림 시간 / (ii) 앱 시간 {T_OPEN} §8 #2 | (i) R = p_h × 30 × D × H · (ii) R = p_h × 30 × D × H ÷ σ | (i) R ÷ M = p_h ÷ c_h · (ii) R ÷ M = p_h ÷ (σ·c_h) | {T_CALC} |")
add(f"| 토큰제(원가 배수형) | Soniox 토큰 종류별 단가 × p_x | R = p_x × M | 마진 = 1 − 1 ÷ p_x — 변인과 무관 | {T_CALC} · 형태 구분은 {T_OPEN} §8 #4 |")
add(f"| 토큰제(단일 단가형) | 모든 토큰 합 1M 당 p_t | R = p_t × (토큰 합) ÷ 10⁶ | 토큰 종류 섞임에 달림(오디오 출력 단가가 입력의 몇 배) | {T_CALC} · 형태 구분은 {T_OPEN} §8 #4 |")
add(f"| 정액제(무제한) | 계정 월 | R = p_f | 사용량 전부가 원가 | {T_CALC} |")
add(f"| 정액제 + 포함량 Q | 계정 월 · 스트림 Q 시간까지 | R = p_f · 원가 ≤ Q × c_h | p_f ÷ Q 가 곧 시간제 단가 — Q 를 넘은 뒤 처리(차단 · 초과 과금)는 {T_OPEN} §8 #13 | {T_CALC} |")
add("")
add(f"- 사용자는 「토큰제」라는 이름만 정했다 {T_USER}. 원가 배수형과 단일 단가형은 성질이 반대(마진 고정 vs 토큰 섞임에 달림)라 **둘 다 계산하고 어느 쪽인지는 사용자에게 올린다** {T_OPEN} §8 #4. 요금제 후보 3개는 그대로.")
add("")

# §5
add("## 5. 요금제별 가격 역산")
add("")
add(f"범위 안 모든 점(§3 스윕 점 ∪ 격자 점)에서 (R − M) ÷ R ≥ m 이 되는 최저 p. 식은 p = (그 단위의 원가 최대) ÷ (1 − m) {T_CALC}. 세션 모델 (가) · (나) 나란히.")
add("")
add("| 요금제 | 세션 모델 | 최저 p(m) | 손익분기 p(m = 0) | 손익분기(원) | 최대를 만드는 곳 | 근거 |")
add("|---|---|---|--:|--:|---|---|")
for pk, pname in PLANS.items():
    for mdl, (mtag, _) in MODELS.items():
        if pk == "xmult":
            add(f"| {pname} | {mtag} | p_x = 1 ÷ (1 − m) | × {price('xmult', 0, mdl):.2f} | — | 변인과 무관 | {T_CALC} |")
            continue
        kk = PLAN_KEY[pk]
        top = TOP[mdl][kk]
        if pk == "hour":
            base, unit, nd = vmax(mdl, "ch"), " / h", 4
        elif pk == "tok":
            base, unit, nd = vmax(mdl, "upt") * 1e6, " / 1M", 3
        else:
            base, unit, nd = vmax(mdl, "M"), " / 월", 2
        add(f"| {pname} | {mtag} | p = {u(base, nd)} ÷ (1 − m) | {u(base, nd)}{unit} | {w(base)} | {pt(top)} | {T_CALC} 범위 최대 · 원 {T_CMP} |")
for mdl, (mtag, _) in MODELS.items():
    add(f"| 정액제 + 포함량 Q | {mtag} | p_f = Q × {u(vmax(mdl, 'ch'), 4)} ÷ (1 − m) | Q × {u(vmax(mdl, 'ch'), 4)} | Q × {w(vmax(mdl, 'ch'))} | 시간제와 같음 | {T_CALC} |")
add("")
add(f"- 세션 모델이 시간제 손익분기를 × {vmax('A', 'ch') / vmax('B', 'ch'):.1f} · 정액제(무제한)를 × {vmax('A', 'M') / vmax('B', 'M'):.1f} · "
    f"토큰제(단일 단가형)를 × {vmax('A', 'upt') / vmax('B', 'upt'):.2f} 바꾼다 {T_CALC}. 어느 쪽으로 매길지는 {T_OPEN} §8 #1.")
add(f"- 시간제 · 토큰제 단위 원가는 D 와 무관하고 H 는 k_min 을 거쳐서만 들어간다 — 「최대를 만드는 곳」의 H · D 는 같은 최대값을 내는 점 가운데 처음 찾은 하나다 {T_CALC} §1.5 식.")
add(f"- 시간제는 해석 (ii) 에서도 원가 최대 지점은 σ = 1 이라 위 손익분기가 그대로다 {T_CALC} §2.")
add("")
add("![매출 vs 원가 — 해피 고정](pd-rev-happy.png)")
add("")
add("![매출 vs 원가 — 워스트 고정](pd-rev-worst.png)")
add("")
add(f"- 그래프 읽기: 나머지 워스트 고정에서 시간제 매출과 정액제 매출이 같은 값이 되는 자리가 있다(시간제 ▲ 선이 정액제 굵은 띠 안에 놓인다) {T_CALC}.")
add("")
add("![단위당 원가와 가격선](pd-unit-cost.png)")
add("")
add("**변인별 손익분기 — 가격이 「나머지 해피 고정」 지점 원가로 매겨졌다면 어디서 적자로 넘어가나**")
add("")
add(f"해피 세트 원가에 맞춘 손익분기 가격(m = 0)으로 받을 때, 변인 하나를 해피 값에서 워스트 쪽으로 움직이며 원가가 매출을 넘는 지점. "
    f"해피 세트는 ψ = 0 이라 두 세션 모델에서 원가가 같다 {T_CALC}.")
add("")
add("| 변인 | 단위 · 값의 뜻 | 해피 값 | 근거 |")
add("|---|---|--:|---|")
add(f"| H | 시간 / 일 — 기기 1대의 하루 스트림 시간 | {HAPPY['H']} | {T_USER} |")
add(f"| D | 대 — 같은 계정에서 동시에 쓰는 기기 수(정수) | {HAPPY['D']} | {T_USER} |")
add(f"| ρ | 0 ~ 1 비율 — 스트림 시간 중 상담 발화가 차지하는 비율 | {HAPPY['rho']:g} | {T_USER} |")
add(f"| φ | 0 ~ 1 비율 — 시간당 발화 수가 최소(공백 60초 직전) ~ 최대(쉼 없음) 사이 어디인가 · 계산으로 끌어낸 변인 | {HAPPY['phi']:g} | {T_CALC} §2 |")
add(f"| ψ | 0 ~ 1 비율 — 시간당 세션 수가 하한 k_min ~ 상한 k_max 사이 어디인가 · 계산으로 끌어낸 변인 | {HAPPY['psi']:g} | {T_CALC} §2 |")
add("")


def boundary(pk, mdl, vk):
    """스윕 첫 적자 칸과 실제 경계(이분법 — D 는 정수라 칸 그대로)."""
    rows = sweeps[(mdl, "happy", vk)]
    deficit = lambda r: revenue(pk, happy_p[pk], r) < r["M"] * (1 - 1e-9)
    idx = next((i for i, (x, r) in enumerate(rows) if deficit(r)), None)
    if idx is None:
        return None, None
    x_hi = rows[idx][0]
    if vk == "D":
        return x_hi, x_hi
    lo, hi = HAPPY[vk], x_hi
    for _ in range(60):
        mid = (lo + hi) / 2
        if deficit(month({**HAPPY, vk: mid}, mdl)):
            hi = mid
        else:
            lo = mid
    return x_hi, lo


def bcell(pk, mdl, vk, unit):
    first, b = boundary(pk, mdl, vk)
    if first is None:
        return "넘어가는 값 없음"
    if vk == "D":
        return f"{first:g} {unit}"
    if abs(b - HAPPY[vk]) < 1e-9:
        return f"첫 칸 {first:g} {unit} · 실제 경계 = 해피 값 {HAPPY[vk]:g} — 조금만 움직여도 적자"
    return f"첫 칸 {first:g} {unit} · 실제 경계 {b:.4f} {unit}"


UNITS = {"H": "h / 일", "D": "대", "rho": "", "phi": "", "psi": ""}
add(f"| 요금제 | 해피 기준 손익분기 p | 움직인 변인 | 적자가 시작되는 값 {MA} | 적자가 시작되는 값 {MB} | 근거 |")
add("|---|--:|---|---|---|---|")
happy_p = {"hour": HP["cost"], "tok": HP["M"] / HP["TOK"] * 1e6, "flat": HP["M"]}
for pk in ("hour", "tok", "flat"):
    for vk, (label, _, xs) in VARS.items():
        cells = [bcell(pk, mdl, vk, UNITS[vk]).replace("  ", " ") for mdl in MODELS]
        pv = u(happy_p[pk], 4 if pk != "flat" else 2) + {"hour": " / h", "tok": " / 1M", "flat": " / 월"}[pk]
        add(f"| {PLANS[pk]} | {pv} | {label} | {cells[0]} | {cells[1]} | {T_CALC} |")
add("")
add(f"- 「첫 칸」은 스윕 간격(H 0.5 h · D 1 대 · ρ · φ · ψ 0.05)에서 처음 적자가 난 칸이다 — 실제 경계는 해피 값과 첫 칸 사이에 있어 이분법으로 따로 구했다 {T_CALC}. "
    f"「실제 경계 = 해피 값」은 해피 지점이 이미 손익분기라 그 변인을 워스트 쪽으로 조금만 움직여도 적자라는 뜻이다.")
add(f"- 「넘어가는 값 없음」: 시간제 · 토큰제는 매출도 사용 시간 H · 대수 D 에 같이 비례해 늘어, H · D 만 움직이면 단위당 원가가 오르지 않는다 {T_CALC}. "
    f"정액제는 매출이 고정이라 H · D 로도 깨진다.")
add("")

# §6
add("## 6. 마진율별 가격표")
add("")
add(f"m 은 사용자가 정하지 않았다 — 30 · 50 · 70% 는 {T_CMP}. 원은 r = {R_CMP:,} {T_CMP}.")
add("")
add("| 요금제 | 세션 모델 | 단위 | m = 30% | m = 50% | m = 70% | 근거 |")
add("|---|---|---|--:|--:|--:|---|")
for pk, pname in PLANS.items():
    for mdl, (mtag, _) in MODELS.items():
        cells = []
        for m in MARGINS:
            p = price(pk, m, mdl)
            if pk == "xmult":
                cells.append(f"× {p:.2f}")
            else:
                nd = 2 if pk == "flat" else 4 if pk == "hour" else 3
                cells.append(f"{u(p, nd)} ({w(p)})")
        add(f"| {pname} | {mtag} | {UNIT[pk]} | " + " | ".join(cells) + f" | {T_CALC} §5 식 · m {T_CMP} |")
for mdl, (mtag, _) in MODELS.items():
    cells = [f"Q × {u(price('hour', m, mdl), 4)}" for m in MARGINS]
    add(f"| 정액제 + 포함량 Q | {mtag} | USD / 계정·월 | " + " | ".join(cells) + f" | {T_CALC} §5 식 · m {T_CMP} · Q 는 변수 |")
add("")
add("![정액제 포함량과 최저 월 가격](pd-flat-q.png)")
add("")
add(f"- 월 2만원은 대표 투표 결과(4명 전원 「잘만 되면 월 2만원도 가능」 {T_USER} · 참고선)다. **그래프에 선으로만 그렸고 가격 · 포함량 계산의 입력으로 쓰지 않았다.** "
    f"2만원 = {u(REF_KRW / R_CMP, 2)} (r = {R_CMP:,} {T_CMP}).")
add("")

# §7
add("## 7. 비교")
add("")
add(f"m = 50% {T_CMP} 가격을 받았을 때 고객 청구액과 실제 마진. 「마진이 가장 낮은 지점」 = 그 요금제의 가격을 정한 범위 최대 지점(사용자 워스트 세트와 다르다) {T_CALC}.")
add("")
add("| 요금제 | 세션 모델 | 고객 월 청구 — 해피 세트 | 그때 마진 | 고객 월 청구 — 워스트 세트 | 그때 마진 | 마진이 가장 낮은 지점 | 그때 고객 월 청구 | 그때 마진 | 근거 |")
add("|---|---|--:|--:|--:|--:|---|--:|--:|---|")
for pk, pname in PLANS.items():
    for mdl, (mtag, _) in MODELS.items():
        p = price(pk, 0.5, mdl)
        hb, wb = month(HAPPY, mdl), month(WORST, mdl)
        rh, rw = revenue(pk, p, hb), revenue(pk, p, wb)
        lo = min(POINTS[mdl], key=lambda r: margin(pk, p, r))
        where = "모든 점 같음" if pk == "xmult" else pt(lo)
        rl = revenue(pk, p, lo)
        add(f"| {pname} | {mtag} | {u(rh, 2)} ({w(rh)}) | {margin(pk, p, hb) * 100:.1f}% | {u(rw, 2)} ({w(rw)}) | {margin(pk, p, wb) * 100:.1f}% | "
            f"{where} | {u(rl, 2)} ({w(rl)}) | {margin(pk, p, lo) * 100:.1f}% | {T_CALC} · 원 {T_CMP} |")
add("")
add(f"- 해석 (ii) 앱 시간이면 해피 세트의 원가가 σ 배로 내려가 해피 마진이 더 높다 — σ 값이 없다 {T_OPEN} §2.")
add("")


def breakers(mdl, kk):
    """단위 원가가 움직이는 변인(스윕 폭 > 0.1%)과 폭."""
    out = []
    for vk in VARS:
        vals = [KEYS[kk](r) for sk in SETS for _, r in sweeps[(mdl, sk, vk)]]
        out.append((max(vals) / min(vals), vk))
    out.sort(reverse=True)
    return " · ".join(f"{VN[vk]}(× {s:.2f})" for s, vk in out if s > 1.001) or "없음"


add("| 요금제 | 고객 쪽 가격 | 적자 위험 | 어느 변인에서 깨지나(그 단위 원가를 움직이는 변인 · 스윕 폭) | 근거 |")
add("|---|---|---|---|---|")
add(f"| 시간제 | 쓴 시간에 비례 · 1시간 원가가 범위 안에서 {MA} × {vmax('A', 'ch') / vmin('A', 'ch'):.1f} · {MB} × {vmax('B', 'ch') / vmin('B', 'ch'):.1f} 벌어져 가벼운 사용자일수록 원가 대비 비싸게 낸다 | "
    f"범위 최대로 매기면 범위 안(스윕 · 격자 점) 적자 0 | {MA} {breakers('A', 'ch')} / {MB} {breakers('B', 'ch')} | {T_CALC} §3 · §5 |")
add(f"| 토큰제(원가 배수형) | 고객 청구가 Soniox 원가에 그대로 따라간다 — 사전에 금액 예측 어려움 | 범위 밖에서도 적자 0 | 깨지는 변인 없음 | {T_CALC} §4 |")
add(f"| 토큰제(단일 단가형) | 토큰 수로 보인다 · 토큰당 원가 폭 {MA} × {vmax('A', 'upt') / vmin('A', 'upt'):.2f} · {MB} × {vmax('B', 'upt') / vmin('B', 'upt'):.2f} | "
    f"범위 최대(격자 포함)로 매기면 범위 안(스윕 · 격자 점) 적자 0 · 스윕 최대만으로 매기면 격자 점에서 소폭 적자(§3 스윕 vs 격자) | {MA} {breakers('A', 'upt')} / {MB} {breakers('B', 'upt')} | {T_CALC} §3 · §5 |")
add(f"| 정액제(무제한) | 한 값 · 최저 {MA} {u(price('flat', 0.5, 'A'), 2)} · {MB} {u(price('flat', 0.5, 'B'), 2)} / 월(m = 50%) | "
    f"월 원가 폭 {MA} × {vmax('A', 'M') / vmin('A', 'M'):,.0f} · {MB} × {vmax('B', 'M') / vmin('B', 'M'):,.0f} — 범위 최대에 맞추면 가격이 크고, 낮추면 어느 변인으로든 깨진다 | "
    f"{MA} {breakers('A', 'M')} / {MB} {breakers('B', 'M')} | {T_CALC} §3 |")
add(f"| 정액제 + 포함량 Q | 한 값 + 상한 · p_f ÷ Q = 시간제 단가 | Q 안이면 적자 0 · Q 초과 처리 {T_OPEN} §8 #13 | Q 를 시간으로 잡으면 시간제와 같다 | {T_CALC} §5 |")
add("")
add("**안** (추천은 §0 결론)")
add("")
add(f"- 안 A · 시간제: 단가 = 1시간 원가 최대 ÷ (1 − m). 단순하지만 1시간 원가 폭이 남는 동안 가벼운 사용자에게 비싸다 {T_CALC} §3. 단가는 세션 모델 {T_OPEN} §8 #1 에 따라 갈린다. 〔안〕")
add("- 안 B · 토큰제(원가 배수형): 마진이 변인과 무관하게 고정. 고객이 미리 청구액을 알기 어렵다. 〔안〕")
add(f"- 안 C · 정액제 + 포함량: 포함량을 시간이 아니라 **원가(크레딧)** 로 잡으면 안 B 의 성질 + 정액의 예측성. 이 구조는 §4 ~ §6 에서 계산하지 않았다 — 포함량 단위부터 정해야 한다 {T_OPEN} §8 #4. 〔안〕")
add("- 안 D · 정액제(무제한): 범위 전체를 견디는 가격이 커서 참고선과 거리가 멀다 — 범위를 데이터로 좁힌 뒤에 다시 볼 안. 〔안〕")
add("")

# §8
add("## 8. 근거 없는 것 · 조사할 것")
add("")
add("| # | 근거 없는 것 | 영향 | 좁히려면 필요한 것 | 근거 |")
add("|---|---|---|---|---|")
items = [
    ("세션 상한 — (가) 발화마다 수동 stop 후 재연결(k ≤ n) vs (나) 무발화 60초 자동 종료만(k ≤ (3600 − t) ÷ 60). 통키에 stop 이 있다는 것은 코드 사실이지만, 사용자가 발화마다 stop 하는지는 사용 패턴이다",
     f"시간제 손익분기 {u(vmax('A', 'ch'))} vs {u(vmax('B', 'ch'))} / h · 정액제 {u(vmax('A', 'M'), 2)} vs {u(vmax('B', 'M'), 2)} / 월 — §5 · §6 · §7 전부 {T_CALC}",
     "사용자 결정(어느 쪽으로 가격을 매기나 · 재연결 빈도 제한을 둘지) + 세션별 연결 시작 · 끝 기록", T_OPEN),
    ("「실사용 1시간」의 기준 — (i) STT 스트림 시간 vs (ii) 앱 사용 시간",
     f"원가 최대 · 가격 역산은 같고, 최소 · 해피 쪽과 시간제 과금 단위(고객이 체감하는 시간)가 갈린다 {T_CALC} §2", "사용자 결정 + 앱 시간 대비 스트림 시간 비율 σ 기록", T_OPEN),
    (f"세션 하한 — 공식 한도 {STREAM_MAX_MIN}분까지 한 세션을 끊지 않고 연다(ψ = 0)는 가정",
     f"ψ = 0 쪽 전부 — 토큰제(단일 단가형) 최대 단가 지점 · 해피 쪽 1시간 원가 최소 {T_CALC} §3 · §5", "세션 길이 분포 기록", T_OPEN),
    ("토큰제의 뜻 — 원가 배수형 vs 단일 토큰 단가형 · 안 C 의 원가(크레딧) 포함량 구조",
     "토큰제 가격 형태 · 안 C 는 미계산", "사용자 결정", T_OPEN),
    (f"무발화 1분 종료 {T_USER} 미구현 — 사실: 통키 main `17c26b5` 는 멈춤 중에도 keepalive 로 STT 연결을 유지한다(`session.py` `_keepalive`)",
     f"§3 범위 전체가 이 정책을 전제 — 지금 그대로면 멈춘 시간도 스트림 시간당 {u(A_USD_H)} 이상 {T_OFF} {URL_KEEPALIVE}", "구현 · 배포", T_USER + " 정책 · 구현 여부는 코드 사실"),
    ("상담 비율 ρ 의 기준(시간 vs 발화 수) · 실제 값", "§3 ρ 방향", "사용자 확인 + 발화별 길이 기록", T_OPEN),
    ("발화 밀도 φ · 세션 분할 ψ 의 실제 분포",
     f"1시간 원가 폭 {MA} × {vmax('A', 'ch') / vmin('A', 'ch'):.1f} · {MB} × {vmax('B', 'ch') / vmin('B', 'ch'):.1f} 의 대부분 {T_CALC}",
     "세션별 `client_reference_id` 를 넣고 연결 시작 · 끝 · 발화 수를 back 에서 기록", T_OPEN),
    ("context 가 연결마다 같은 양으로 과금되는가 — 공식 문서는 「세션 시작 때 한 번」, 실측 2건은 각 연결 1회",
     "연결 고정비 C × 세션 수 k 항 전체", "같은 언어로 2회 이상 연결한 세션의 usage-log", T_OPEN),
    (f"동시 사용 D = 4 · 5 와 Soniox 동시 한도 — TTS 동시 스트림 {TTS_CONC} · STT {STT_CONC} 은 Soniox 계정 전체 기준 {T_OFF} {URL_TTS_LIMITS}",
     "고객 계정 여럿이 Soniox 계정 하나를 나눠 쓰면 한도가 더 좁다 — 한도 초과 시 동작 · 한도 증설 비용은 이 보고서 밖", "동시 TTS 생성 기기 수 기록 · 한도 정책 결정", T_OPEN),
    ("발화 하나 연결의 스트림 시간 d 의 내역 · 대표성",
     "n_min · n_max — d 안에 말 · 번역 · TTS 재생 · 앞뒤 공백이 얼마씩인지 모른다 · 실측 1건씩뿐", "스트림 시각과 발화 시각 대조 · 실제 발화 길이 분포", T_OPEN),
    (f"{MAX_LANG} context 토큰", f"연결 고정비 C(추정 {CTX_TOK:,} · 작은 값 {CTX_TOK_LO:,}) {T_EST}", f"{MAX_LANG} 로 1회 연결한 usage-log", T_OPEN),
    ("th context 토큰", f"th 글자 {ctx['langs']['th']['chars']:,}(두 번째로 큼) {T_CALC} — 글자당 토큰이 크면 최대 언어가 바뀐다", "th 로 1회 연결한 usage-log", T_OPEN),
    ("포함량 Q 초과 처리", "정액제 + 포함량", "사용자 결정", T_OPEN),
    ("환율 r", "원 환산 전부", "사용자 결정", T_OPEN),
    ("마진율 m", "§5 · §6 가격", "사용자 결정", T_OPEN),
    ("하루 실사용 H · 동시 대수 D 분포", "정액제 월 원가 폭", "계정 · 기기별 스트림 시간 일 합계", T_OPEN),
    ("`stt-rt-v5` → `stt-rt-v6` 단가", f"전체 — v5 는 2026-12-15 제거 {T_OFF} {URL_MODELS}", "전환 뒤 usage-log", T_OPEN),
    ("부가세 · 결제 수수료 · 서버비", "원가 하한", "사용자 · 회계 결정", T_OPEN),
]
for i, (a, b, c, tag) in enumerate(items, 1):
    add(f"| {i} | {a} | {b} | {c} | {tag} |")
add("")
add("— 끝 〔메타〕")

REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")


def slim(r):
    return {k: r[k] for k in ("v", "cost", "M", "tok", "TOK", "k", "n")}


results = {
    "cases": {k: {kk: v for kk, v in c.items() if kk not in ("stt", "tts")} for k, c in CASES.items()},
    "ctx_tok_max": CTX_TOK, "ctx_usd": CTX_USD,
    "models": {mdl: {"top": {kk: slim(TOP[mdl][kk]) for kk in KEYS}, "bot": {kk: slim(BOT[mdl][kk]) for kk in KEYS},
                     "sweep_max": SWEEP_MAX[mdl], "grid_max": GRID_MAX[mdl],
                     "prices": {pk: {str(m): price(pk, m, mdl) for m in (0.0, *MARGINS)} for pk in PLANS}}
               for mdl in MODELS},
    "pngs": pngs,
}
(HERE / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
print("ok", REPORT, pngs)
